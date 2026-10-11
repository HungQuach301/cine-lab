"""Gói kênh 2 — HIỆU CHUẨN thước cầu bằng Last Lamplighters (chủ dự án 11/10 20:00).
Thước cầu hiện hành = current.py: video ≥ 8 phút đăng trong 90 ngày (US), Sonnet chấm "đối thủ trực tiếp" trên video ≥ 50 nghìn;
≥ 2 → Mạnh, 1 → Yếu, 0 → Không. Ở đây ≤ 3 câu/đề tài (current.py dùng 6), nên nhãn có thể thấp hơn một bậc — ghi rõ.
Video LL lấy từ uploads của kênh (channels.list forHandle=@lastlamplighters, 1 đơn vị), không đoán.
Mọi chỉ số: tự tính, không phải chỉ số YouTube. Dùng: K2C_NOWAIT=1 python calib.py"""
import json, sys, statistics as st, datetime as dt
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import collect, current
from collect import DATA, LONG_S, get, videos, purge

NOW_REAL = dt.datetime(2026, 10, 12, 7, 0, tzinfo=dt.timezone.utc)   # mốc tính lượt xem/ngày (lúc đo)
HANDLE = "@lastlamplighters"
# 8 đề tài LL (tiêu đề lấy từ release-ll-epXX/…youtube-description.txt), 3 câu hỏi khán giả mỗi đề tài
LL = {
 "ep01-lamplighters": ("London Still Has 5 Lamplighters. Who Are the Last of Our Time?",
                       ["which jobs will ai replace history", "jobs that disappeared because of technology", "london lamplighters history"]),
 "ep02-phone-operators": ("Automation Hurt the Phone Operators. Not the Next Generation. What About Us?",
                          ["what happened to telephone switchboard operators", "how automation replaced telephone operators", "history of telephone operators"]),
 "ep03-bank-teller": ("The ATM Didn't Kill the Bank Teller. Will AI?",
                      ["did atms replace bank tellers", "will ai replace bank tellers", "history of the atm and bank jobs"]),
 "ep04-typewriter": ("The Typewriter Opened a Door for Millions of Women. Who Gets the Next One?",
                     ["how the typewriter changed women's work", "history of secretaries and typists", "how office work changed for women"]),
 "ep05-insurance": ("In 1966, Computers Couldn't Judge an Insurance Claim. Now Software Prices the Wreck",
                    ["will ai replace insurance adjusters", "how computers changed the insurance industry", "how insurance claims are processed by ai"]),
 "ep06-typesetter": ("The Computer Replaced the Typesetter and Made the Designer. Now AI Can Draw",
                     ["will ai replace graphic designers", "what happened to typesetters", "how computers changed graphic design"]),
 "ep07-human-computers": ("When Computers Were People: One Word, Three Jobs",
                          ["when computers were people", "history of human computers", "women human computers nasa history"]),
 "ep08-translators": ("From Headphones to Machine Drafts: How Translators' Work Changed",
                      ["will ai replace translators", "how machine translation changed translators", "history of interpreters and translators"]),
}
# video dài đã đăng trên kênh ↔ đề tài (khớp tiêu đề tải lên; tập 2–5 chưa có trên kênh lúc đo)
PUB = {"PqS6vL7yaUk": "ep01-lamplighters", "nBY2-E9lUt8": "ep06-typesetter", "Xg1nIQOQMOY": "ep07-human-computers",
       "hm-pBARZYag": "ep08-translators"}

def rank(xs):
    o = sorted(range(len(xs)), key=lambda i: xs[i]); r = [0.0] * len(xs); i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and xs[o[j + 1]] == xs[o[i]]: j += 1
        for k in range(i, j + 1): r[o[k]] = (i + j) / 2
        i = j + 1
    return r

def spearman(a, b):
    ra, rb = rank(a), rank(b)
    ma, mb = st.mean(ra), st.mean(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** .5
    return round(num / den, 2) if den else None

def main():
    purge()
    f = DATA / "calib.json"
    if f.exists(): print(f.read_text()[:3000]); return
    ch = get("channels", part="snippet,contentDetails,statistics", forHandle=HANDLE)["items"][0]
    up = get("playlistItems", part="contentDetails", playlistId=ch["contentDetails"]["relatedPlaylists"]["uploads"], maxResults=50)
    ll = videos([i["contentDetails"]["videoId"] for i in up["items"]])
    longs = [v for v in ll if v["dur"] >= LONG_S]
    for v in longs:
        days = (NOW_REAL - current.pubdt(v["pub"])).total_seconds() / 86400
        v.update(topic=PUB.get(v["id"]), days=round(days, 2), vpd=round(v["views"] / max(days, .5), 1))
    res = {}
    for slug, (title, qs) in LL.items():
        current.Q[slug], current.TITLE[slug] = qs, title          # dùng đúng search_topic + relevance của current.py
        lv = current.search_topic(slug)
        big = sorted([v for v in lv if v["views"] >= current.BIG], key=lambda v: -v["views"])
        rel = current.relevance(slug, big)
        on = [v for v in big if rel.get(v["id"], {}).get("on_topic")]
        res[slug] = dict(title=title, n_long=len(lv), n_big_raw=len(big), n_big=len(on),
                         label="Mạnh" if len(on) >= 2 else ("Yếu" if len(on) == 1 else "Không"),
                         med_min_on=round(st.median(v["dur"] for v in on) / 60, 1) if on else None,
                         med_min_long=round(st.median(v["dur"] for v in lv) / 60, 1) if lv else None,
                         top_on=[dict(title=v["title"], views=v["views"], ch=v["chname"], min=round(v["dur"] / 60, 1)) for v in on[:3]])
        print(slug, res[slug]["label"], res[slug]["n_big"], collect.calls, flush=True)
    pubd = [v for v in longs if v["topic"]]
    score = {"Mạnh": 2, "Yếu": 1, "Không": 0}
    rho = spearman([score[res[v["topic"]]["label"]] + res[v["topic"]]["n_big"] / 100 for v in pubd], [v["vpd"] for v in pubd]) if len(pubd) >= 3 else None
    out = dict(channel=dict(id=ch["id"], title=ch["snippet"]["title"], videos=ch["statistics"].get("videoCount")),
               ll_long=[dict(id=v["id"], title=v["title"], pub=v["pub"], min=round(v["dur"] / 60, 1), views=v["views"],
                             days=v["days"], vpd=v["vpd"], topic=v["topic"]) for v in longs],
               topics=res, spearman_label_vs_vpd=rho, n_pub=len(pubd), calls=dict(collect.calls))
    f.write_text(json.dumps(out, ensure_ascii=False))
    print(json.dumps({k: v for k, v in out.items() if k != "topics"}, ensure_ascii=False))
    print(json.dumps({s: {k: r[k] for k in ("label", "n_big", "n_big_raw", "n_long", "med_min_on", "med_min_long")} for s, r in res.items()}, ensure_ascii=False))

if __name__ == "__main__":
    main()
