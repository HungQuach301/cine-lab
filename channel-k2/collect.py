"""Gói kênh 2 — thu dữ liệu cho mốc 1 (nhãn cầu đề tài mới, kiểm tên kênh) và mốc 2 (hồ sơ cầu).
YouTube Data API v3 qua proxy gắn khoá (không có khoá trong mã, không in URL). AI: `claude -p` (Haiku/Sonnet) với
ANTHROPIC_API_KEY=$CONSOLE_API_KEY, không subagent, trần $5 (dừng khi cost.jsonl vượt).
Số liệu thô (kể cả bình luận) lưu NGOÀI git ở $K2C_DATA; mỗi lần chạy tự xoá file > 30 ngày.
Mọi chỉ số tính ra là "tự tính, không phải chỉ số YouTube".
Dùng: python collect.py labels | durable | names | demand | all | purge (chỉ xoá số liệu thô > 30 ngày)"""
import json, os, re, subprocess, sys, time, hashlib, datetime as dt
from pathlib import Path
import requests

API = "https://www.googleapis.com/youtube/v3/"
DATA = Path(os.environ.get("K2C_DATA", Path.home() / ".cache/cine-channel-k2"))
DATA.mkdir(parents=True, exist_ok=True)
NOW = dt.datetime(2026, 10, 11, tzinfo=dt.timezone.utc)
LONG_S = 480            # video dài ≥ 8 phút (cùng định nghĩa market-k2)
COST_CAP = 5.0
LOG = DATA / "cost.jsonl"
calls = {"search.list": 0, "other": 0}

def purge():
    for f in DATA.glob("*"):
        if f.is_file() and f.name != "cost.jsonl" and time.time() - f.stat().st_mtime > 30 * 86400:   # giữ sổ chi phí AI
            f.unlink()

def spent():
    if not LOG.exists(): return 0.0
    return sum(json.loads(l).get("usd", 0) for l in LOG.read_text().splitlines() if l.strip())

def get(ep, **p):
    key = DATA / f"api_{ep}_{hashlib.sha1(json.dumps(p, sort_keys=True).encode()).hexdigest()[:12]}.json"
    if key.exists():
        return json.loads(key.read_text())
    i = waits = 0
    while i < 4:
        try:
            r = requests.get(API + ep, params=p, timeout=60)
        except requests.RequestException as e:          # chỉ in tên lỗi, không in URL
            print(f"{ep}: {type(e).__name__}", file=sys.stderr); i += 1; time.sleep(2 ** i); continue
        if r.status_code == 200:
            calls["search.list" if ep == "search" else "other"] += 1
            key.write_text(r.text)
            return r.json()
        if r.status_code == 403 and ep == "commentThreads":   # bình luận bị tắt: ghi rỗng, đi tiếp
            j = {"items": [], "disabled": True}; key.write_text(json.dumps(j)); return j
        if r.status_code in (400, 404):
            raise SystemExit(f"{ep}: HTTP {r.status_code}")
        if r.status_code == 429 and waits < 48:     # hết quota ngày: chờ 5 phút rồi thử lại (tối đa 4 giờ)
            waits += 1; time.sleep(300); continue
        i += 1; time.sleep(2 ** i)
    raise SystemExit(f"{ep}: thất bại sau 4 lần")

def dur(s):
    m = re.match(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", s or "")
    d, h, mi, se = (int(x or 0) for x in m.groups()) if m else (0,) * 4
    return d * 86400 + h * 3600 + mi * 60 + se

def videos(ids):
    out = {}
    for i in range(0, len(ids), 50):
        j = get("videos", part="snippet,contentDetails,statistics", id=",".join(ids[i:i+50]), maxResults=50)
        for v in j.get("items", []):
            s, c = v["snippet"], v.get("statistics", {})
            out[v["id"]] = dict(id=v["id"], ch=s["channelId"], chname=s["channelTitle"], title=s["title"],
                                desc=s.get("description", "")[:1200], pub=s["publishedAt"],
                                dur=dur(v["contentDetails"].get("duration")), views=int(c.get("viewCount", 0)),
                                likes=int(c.get("likeCount", 0)), comments=int(c.get("commentCount", 0)))
    return [out[i] for i in ids if i in out]

def ai(prompt, tag, model="claude-haiku-5-5"):
    """Gọi claude -p (prompt qua stdin). Trả JSON đầu tiên trong câu trả lời, hoặc {} nếu hỏng 3 lần."""
    if spent() > COST_CAP:
        raise SystemExit(f"vượt trần ${COST_CAP}")
    env = dict(os.environ, ANTHROPIC_API_KEY=os.environ["CONSOLE_API_KEY"])
    for _ in range(3):
        r = subprocess.run(["claude", "-p", "--model", model, "--output-format", "json"], input=prompt,
                           capture_output=True, text=True, env=env, cwd=str(DATA), timeout=900)
        try:
            d = json.loads(r.stdout)
        except Exception:
            continue
        with open(LOG, "a") as f:
            f.write(json.dumps({"tag": tag, "model": model, "usd": d.get("total_cost_usd", 0)}) + "\n")
        m = re.search(r"[\{\[].*[\}\]]", d.get("result", ""), re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                pass
    return {}

# ---------- Mốc 1: nhãn cầu cho đề tài CHƯA có nhãn ở market-k2 (cùng định nghĩa, cửa sổ 90 ngày) ----------
LABEL_Q = {
    "card-networks": "how do visa and mastercard make money",
    "swift": "how does swift international money transfer work",
    "atm": "how do atm machines make money",
    "supermarkets": "how do supermarkets make money",
    "factory-town": "how a factory changed a small town",
}

def gap_check(tag, vids):
    lines = [f'{v["id"]} | {v["title"]} | {v["desc"][:500]!r}' for v in vids]
    p = ("For each YouTube video (title + description), judge ONLY from the text whether it shows evidence of using "
         "real, named data sources (e.g. cites statistics agencies, company filings, central bank data, academic papers, "
         "or lists sources). Return ONLY JSON {\"<videoId>\": {\"real_data\": true|false}}.\n\n" + "\n".join(lines))
    return ai(p, f"gap-{tag}")

def labels():
    after = (NOW - dt.timedelta(days=90)).strftime("%Y-%m-%dT%H:%M:%SZ")
    out = {}
    for tag, q in LABEL_Q.items():
        j = get("search", part="id", q=q, type="video", maxResults=25, publishedAfter=after,
                regionCode="US", relevanceLanguage="en", order="relevance")
        ids = [it["id"]["videoId"] for it in j.get("items", [])]
        lv = [v for v in videos(ids) if v["dur"] >= LONG_S and (NOW - dt.datetime.fromisoformat(v["pub"].replace("Z", "+00:00"))).days >= 14]
        top = sorted(lv, key=lambda v: -v["views"])
        g = gap_check(tag, top[:5]) if top else {}
        out[tag] = dict(q=q, n_long=len(lv), max_views=top[0]["views"] if top else 0,
                        n_500k=sum(v["views"] >= 500_000 for v in lv), n_10_50k=sum(10_000 <= v["views"] < 50_000 for v in lv),
                        n_50k=sum(v["views"] >= 50_000 for v in lv),
                        top5_real_data=sum(bool(g.get(v["id"], {}).get("real_data")) for v in top[:5]),
                        top5_gap_cov=sum(v["id"] in g for v in top[:5]), n_top5=len(top[:5]),
                        top=[dict(title=v["title"], views=v["views"], min=round(v["dur"] / 60, 1), ch=v["chname"]) for v in top[:5]])
    (DATA / "labels.json").write_text(json.dumps(out, indent=1))
    return out

# ---------- Mốc 1: nhãn Cầu-bền (top 5 video dài toàn thời gian theo độ liên quan) ----------
DURABLE_Q = {"swift": "how does swift international money transfer work", "atm": "how do atm machines make money",
             # vòng 2 (11/10): đề tài cơ chế tài chính thay thế khi SWIFT/ATM trượt Cầu-bền
             "banks": "how do banks actually make money", "card-rewards": "who pays for credit card rewards",
             "bank-transfer": "how does money move between banks", "exchange": "how does the stock exchange make money",
             "insurance": "how do insurance companies make money"}

def durable():
    out = {}
    for tag, q in DURABLE_Q.items():
        j = get("search", part="id", q=q, type="video", maxResults=15, regionCode="US", relevanceLanguage="en", order="relevance")
        top = [v for v in videos([it["id"]["videoId"] for it in j.get("items", [])]) if v["dur"] >= LONG_S][:5]
        g = gap_check(f"dur-{tag}", top) if top else {}
        out[tag] = dict(q=q, n_500k=sum(v["views"] >= 500_000 for v in top),
                        top5_real_data=sum(bool(g.get(v["id"], {}).get("real_data")) for v in top), gap_cov=sum(v["id"] in g for v in top),
                        top=[dict(title=v["title"], views=v["views"], min=round(v["dur"] / 60, 1), ch=v["chname"], pub=v["pub"][:10]) for v in top])
    (DATA / "durable.json").write_text(json.dumps(out, indent=1))
    return out

# ---------- Mốc 1: kiểm tên kênh (≤ 3 search.list + forHandle 1 đơn vị/lượt) ----------
NAMES = {"Moving Parts": ["@movingpartsecon", "@movingpartsfilms"],
         "Load Bearing": ["@loadbearingecon", "@loadbearingfilms"],
         "Throughput": ["@throughputecon", "@throughputfilms"]}

def names():
    out = {}
    for name, handles in NAMES.items():
        j = get("search", part="snippet", q=name, type="channel", maxResults=10, regionCode="US")
        ids = [it["snippet"]["channelId"] for it in j.get("items", [])]
        chans = []
        if ids:
            cj = get("channels", part="snippet,statistics", id=",".join(ids), maxResults=50)
            for c in cj.get("items", []):
                chans.append(dict(title=c["snippet"]["title"], handle=c["snippet"].get("customUrl"),
                                  subs=int(c["statistics"].get("subscriberCount", 0) or 0),
                                  videos=int(c["statistics"].get("videoCount", 0) or 0)))
        hs = {}
        for h in handles:
            hj = get("channels", part="id", forHandle=h)
            hs[h] = "đã có kênh" if hj.get("items") else "chưa thấy kênh"
        out[name] = dict(channels=sorted(chans, key=lambda c: -c["subs"]), handles=hs)
    (DATA / "names.json").write_text(json.dumps(out, indent=1))
    return out

# ---------- Mốc 2: hồ sơ cầu ----------
TOPICS = {
    "container": ("The Steel Box That Rewired World Trade",
                  ["how shipping containers changed the world", "how does container shipping work",
                   "why is shipping so cheap"]),
    "jet-airliner": ("Why Only Two Companies Can Still Build a Jet Airliner",
                     ["why are there only two airplane manufacturers", "why can't anyone compete with boeing and airbus",
                      "how hard is it to build a commercial airplane"]),
    "card-networks": ("How Visa and Mastercard Make Money Without Lending a Cent",
                      ["how do visa and mastercard make money", "what happens when you swipe a credit card",
                       "who pays credit card swipe fees"]),
}
TOP_N, N_COMMENTS = 5, 50
KINDS = ("question", "situation", "rebuttal", "request")

def classify(tag, items):
    """Haiku: 4 loại + bỏ spam/khen chung; tóm ý bằng tiếng Anh, KHÔNG chép tên người."""
    out = {}
    for i in range(0, len(items), 60):
        b = items[i:i+60]
        lines = [f'{c["cid"]} | {c["text"][:450]!r}' for c in b]
        p = ("You label YouTube comments left under explainer videos about an industry. For each comment choose ONE kind:\n"
             "question = asks something about how the industry/mechanism works; situation = describes the commenter's own "
             "job, workplace, town or personal experience related to the topic; rebuttal = disputes, corrects or adds a "
             "missing fact to the video; request = asks the creator for a future video/topic or more detail; "
             "drop = spam, generic praise, jokes, insults, off-topic, politics without substance.\n"
             "Also write gist: a neutral paraphrase in <= 18 words, no names, no usernames, no quotes.\n"
             "Return ONLY JSON {\"<id>\": {\"k\": \"question|situation|rebuttal|request|drop\", \"gist\": \"...\"}}.\n\n"
             + "\n".join(lines))
        r = ai(p, f"cls-{tag}-{i}")
        out.update({k: v for k, v in r.items() if isinstance(v, dict)})
    return out

def classify_all(tag, items):
    """Gắn nhãn, rồi gắn lại tối đa 2 lượt cho bình luận Haiku bỏ sót (lô hỏng JSON)."""
    lab = classify(tag, items)
    for n in range(2):
        miss = [c for c in items if c["cid"] not in lab]
        if not miss: break
        lab.update(classify(f"{tag}-retry{n}", miss))
    return lab

def synth(slug, title, buckets, comp):
    p = (f"Planned episode: \"{title}\" for a faceless, data-driven explainer channel about the economic mechanisms of "
         "industries. Below are labelled viewer comments from the top competing videos, as weighted gists "
         "(weight = 1 + likes + replies). Write in Vietnamese (keep English titles/terms). Do NOT state any numeric fact "
         "about the world as true; when a number would be needed, list it as an anchor to source. Do not name commenters. "
         "Return ONLY JSON with keys: top_questions (5 items: {q_en, why_vi, weight}), situations (3 items: {vi, weight}), "
         "competitor_weaknesses (3-6 items: {vi, evidence_vi}), anchors_to_source (6-10 items: {need_vi, likely_source_type}), "
         "requests (<=5 items: {vi, weight}).\n\nCOMPETITOR VIDEOS:\n" + json.dumps(comp, ensure_ascii=False) +
         "\n\nCOMMENTS BY KIND:\n" + json.dumps(buckets, ensure_ascii=False))
    return ai(p, f"synth-{slug}", model="claude-sonnet-5-5")

def demand():
    res = {}
    for slug, (title, qs) in TOPICS.items():
        f = DATA / f"demand_{slug}.json"
        if f.exists():
            res[slug] = json.loads(f.read_text()); continue
        per_q, allv = {}, {}
        for q in qs:
            j = get("search", part="id", q=q, type="video", maxResults=15, regionCode="US",
                    relevanceLanguage="en", order="relevance")
            ids = [it["id"]["videoId"] for it in j.get("items", [])]
            top = [v for v in videos(ids) if v["dur"] >= LONG_S][:TOP_N]   # giữ thứ tự relevance
            per_q[q] = [v["id"] for v in top]
            for v in top: allv[v["id"]] = v
        comments = []
        for vid in allv:
            j = get("commentThreads", part="snippet", videoId=vid, maxResults=N_COMMENTS, order="relevance", textFormat="plainText")
            for it in j.get("items", []):
                s = it["snippet"]; tl = s["topLevelComment"]["snippet"]
                comments.append(dict(cid=it["id"], vid=vid, text=tl.get("textDisplay", ""), likes=int(tl.get("likeCount", 0)),
                                     replies=int(s.get("totalReplyCount", 0))))
        lab = classify_all(slug, comments)
        cov = sum(c["cid"] in lab for c in comments)
        if comments and cov < 0.95 * len(comments):
            raise SystemExit(f"nhãn thiếu {slug}: {cov}/{len(comments)}")
        buckets = {k: [] for k in KINDS}
        for c in comments:
            l = lab.get(c["cid"], {})
            if l.get("k") in KINDS:
                buckets[l["k"]].append(dict(w=1 + c["likes"] + c["replies"], gist=l.get("gist", ""), vid=c["vid"]))
        for k in buckets: buckets[k].sort(key=lambda x: -x["w"])
        comp = [dict(id=v["id"], title=v["title"], ch=v["chname"], views=v["views"], min=round(v["dur"] / 60, 1),
                     pub=v["pub"][:10], desc=v["desc"][:300]) for v in allv.values()]
        sy = synth(slug, title, {k: buckets[k][:60] for k in KINDS}, comp)
        res[slug] = dict(title=title, queries=per_q, videos=comp, n_comments=len(comments), label_cov=cov,
                         kinds={k: len(v) for k, v in buckets.items()}, n_drop=len(comments) - sum(len(v) for v in buckets.values()),
                         buckets={k: v[:25] for k, v in buckets.items()}, synth=sy)
        f.write_text(json.dumps(res[slug], indent=1, ensure_ascii=False))
        print(slug, len(allv), "videos", len(comments), "comments", res[slug]["kinds"], calls, f"${spent():.2f}", flush=True)
    return res

if __name__ == "__main__":
    purge()
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("labels", "all"): print(json.dumps(labels(), indent=1)[:6000])
    if what in ("durable", "all"): print(json.dumps(durable(), indent=1))
    if what in ("names", "all"): print(json.dumps(names(), indent=1, ensure_ascii=False))
    if what in ("demand", "all"): demand()
    (DATA / f"calls_{what}.json").write_text(json.dumps(calls))
    print("calls", calls, f"AI ${spent():.2f}")
