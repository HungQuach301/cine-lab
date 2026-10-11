"""Kênh 2 — vòng xác nhận B vs A: thu mẫu mới (16 câu hỏi khán giả MỚI/ngách) + thu lại mẫu cũ (8 câu cũ).
Dùng lại get/videos/haiku/bộ lọc của collect.py; số liệu thô ở $K2_DATA (ngoài git), tự xoá sau 30 ngày.
Ngân sách mới: 32 search.list (16 × A, B), 25 kết quả/lượt, ≤ 30 kênh/ngách, ≤ 50 video dài/kênh.
Mẫu cũ: số liệu thô vòng trước đã mất cùng container, nên chạy lại đúng 8 câu cũ/ngách, cùng NOW, cùng luật (≤ 15 kênh)."""
import json, sys, time, hashlib, datetime as dt
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import collect
from collect import DATA, NOW, LONG_S, MAX_VID, NICHES, get, videos, classify_channels, purge

NEW_Q = {
 "A": ["how does inflation work explained", "why do banks fail", "what caused the great depression",
       "how did the federal reserve start", "what is fractional reserve banking", "how does the bond market work",
       "why did silicon valley bank collapse", "history of money from barter to bitcoin",
       "how do central banks control interest rates", "what caused the 1929 stock market crash",
       "how did the bretton woods system work", "why does the us have so much debt",
       "how do credit card companies make money", "what is the petrodollar",
       "how did the euro crisis happen", "how does quantitative easing work"],
 "B": ["why are there only two airplane manufacturers", "how shipping containers changed global trade",
       "why is it so hard to make semiconductors", "how do supermarkets make money",
       "why are american malls dying", "how does amazon actually make money", "what happened to toys r us",
       "how did mcdonalds become so successful", "why did general electric collapse",
       "how does the car industry work", "why is boeing struggling", "how do airlines make money",
       "why did nokia fail", "how does the diamond industry work", "why are drug prices so high in america",
       "how did ikea become so big"],
}

def sample(key, tag, qs, max_ch):
    f = DATA / f"k2v2_{tag}_{key}.json"
    if f.exists():
        return json.loads(f.read_text())
    after = (NOW - dt.timedelta(days=90)).strftime("%Y-%m-%dT%H:%M:%SZ")
    hits = []
    for q in qs:
        qf = DATA / f"search_{hashlib.sha1(q.encode()).hexdigest()[:10]}.json"
        if qf.exists():
            j = json.loads(qf.read_text())
        else:
            j = get("search", part="id", q=q, type="video", maxResults=25, publishedAfter=after,
                    regionCode="US", relevanceLanguage="en", order="relevance")
            qf.write_text(json.dumps(j))
        hits += [(q, it["id"]["videoId"]) for it in j.get("items", [])]
    ids = list(dict.fromkeys(v for _, v in hits))
    qof = {}
    for q, v in hits: qof.setdefault(v, q)
    sv = [v for v in videos(ids) if v["dur"] >= LONG_S]
    for v in sv: v["q"] = qof[v["id"]]
    cands = {}
    for v in sorted(sv, key=lambda x: -x["views"]):
        cands.setdefault(v["ch"], []).append(v)
    cls = classify_channels(f"{tag}-{key}", cands)
    if len(set(cls) & set(cands)) < 0.95 * len(cands):   # Haiku hỏng → dừng, không chọn kênh trên nhãn thiếu
        raise SystemExit(f"phân loại kênh thiếu: {tag}-{key} {len(set(cls) & set(cands))}/{len(cands)}")
    keep = [c for c in cands if cls.get(c, {}).get("faceless_explainer")]
    keep.sort(key=lambda c: (-len(cands[c]), -sum(v["views"] for v in cands[c])))   # luật chọn cũ
    keep = keep[:max_ch]
    chans = {}
    for i in range(0, len(keep), 50):
        j = get("channels", part="snippet,statistics,contentDetails", id=",".join(keep[i:i+50]), maxResults=50)
        for c in j.get("items", []):
            chans[c["id"]] = dict(name=c["snippet"]["title"], created=c["snippet"]["publishedAt"],
                country=c["snippet"].get("country"), subs=int(c["statistics"].get("subscriberCount", 0) or 0),
                hidden_subs=c["statistics"].get("hiddenSubscriberCount", False),
                uploads=c["contentDetails"]["relatedPlaylists"]["uploads"])
    for cid, c in chans.items():
        cf = DATA / f"chan_{cid}.json"
        if cf.exists():
            c["videos"] = json.loads(cf.read_text()); continue
        longv, tok, pages = [], None, 0
        while len(longv) < MAX_VID and pages < 6:
            p = dict(part="contentDetails", playlistId=c["uploads"], maxResults=50)
            if tok: p["pageToken"] = tok
            j = get("playlistItems", **p)   # lỗi → dừng hẳn, không ghi chan_*.json dở dang
            ids2 = [i["contentDetails"]["videoId"] for i in j.get("items", [])]
            longv += [v for v in videos(ids2) if v["dur"] >= LONG_S]
            tok, pages = j.get("nextPageToken"), pages + 1
            if not tok: break
        c["videos"] = sorted(longv, key=lambda v: v["pub"], reverse=True)[:MAX_VID]
        cf.write_text(json.dumps(c["videos"]))
    out = dict(name=NICHES[key][0], tag=tag, queries=qs, search_videos=sv, n_search_ids=len(ids),
               n_candidates=len(cands), classified=cls, channels=chans)
    f.write_text(json.dumps(out))
    print(tag, key, "ids", len(ids), "long", len(sv), "cands", len(cands), "passed",
          sum(1 for x in cls.values() if x.get("faceless_explainer")), "kept", len(chans), collect.calls, flush=True)
    return out

def main():
    purge()   # collect.purge xoá cả file vòng xác nhận > 30 ngày
    for k in "AB":
        assert not set(NEW_Q[k]) & set(NICHES[k][1]) and len(NEW_Q[k]) == 16
    for k in "AB": sample(k, "new", NEW_Q[k], 30)
    for k in "AB": sample(k, "old", NICHES[k][1], 15)
    calls_f = DATA / "calls_v2.json"
    prev = json.loads(calls_f.read_text()) if calls_f.exists() else {"search.list": 0, "other": 0}
    calls_f.write_text(json.dumps({k: prev[k] + collect.calls[k] for k in prev}))

if __name__ == "__main__":
    main()
