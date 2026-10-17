"""R&D City Timelapse 3D — teardown cầu bằng YouTube Data API v3 (proxy gắn khoá; không có khoá trong mã).
Số liệu thô (kể cả văn bản bình luận) lưu NGOÀI git ở $TL_DATA (mặc định ~/.cache/cine-timelapse).
Trần quota phiên: 400 đơn vị. Mỗi lời gọi ghi đơn vị vào $TL_DATA/quota.jsonl; vượt 400 → dừng."""
import json, os, re, sys, time, datetime as dt
from pathlib import Path
import requests

API = "https://www.googleapis.com/youtube/v3/"
DATA = Path(os.environ.get("TL_DATA", Path.home() / ".cache/cine-timelapse"))
DATA.mkdir(parents=True, exist_ok=True)
QLOG = DATA / "quota.jsonl"
CAP = 400
COST = {"search": 100}

def used():
    return sum(json.loads(l)["u"] for l in QLOG.read_text().splitlines()) if QLOG.exists() else 0

def get(ep, cache, **p):
    f = DATA / f"{cache}.json"
    if f.exists():
        return json.loads(f.read_text())
    u = COST.get(ep, 1)
    if used() + u > CAP:
        raise SystemExit(f"trần quota: đã dùng {used()}, cần thêm {u}")
    for i in range(4):
        try:
            r = requests.get(API + ep, params=p, timeout=60)
        except requests.RequestException as e:
            print(f"{ep}: {type(e).__name__}", file=sys.stderr); time.sleep(2 ** (i + 1)); continue
        with open(QLOG, "a") as q:
            q.write(json.dumps({"ep": ep, "u": u, "cache": cache, "code": r.status_code}) + "\n")
        if r.status_code == 200:
            j = r.json(); f.write_text(json.dumps(j)); return j
        if r.status_code in (403, 404):
            print(f"{ep}: HTTP {r.status_code} {r.text[:200]}", file=sys.stderr); return {}
        time.sleep(2 ** (i + 1))
    raise SystemExit(f"{ep}: thất bại sau 4 lần")

def dur(s):
    m = re.match(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", s or "")
    d, h, mi, se = (int(x or 0) for x in m.groups()) if m else (0,) * 4
    return d * 86400 + h * 3600 + mi * 60 + se

def videos(ids, tag):
    out = []
    for i in range(0, len(ids), 50):
        j = get("videos", f"vid_{tag}_{i}", part="snippet,contentDetails,statistics", id=",".join(ids[i:i+50]), maxResults=50)
        for v in j.get("items", []):
            s, c = v["snippet"], v.get("statistics", {})
            out.append(dict(id=v["id"], ch=s["channelId"], chname=s["channelTitle"], title=s["title"],
                            desc=s.get("description", "")[:2000], pub=s["publishedAt"], tags=s.get("tags", [])[:30],
                            lang=s.get("defaultAudioLanguage"), dur=dur(v["contentDetails"].get("duration")),
                            views=int(c.get("viewCount", 0)), likes=int(c.get("likeCount", 0)),
                            comments=int(c.get("commentCount", 0))))
    return out

def channels(ids, tag):
    out = {}
    for i in range(0, len(ids), 50):
        j = get("channels", f"ch_{tag}_{i}", part="snippet,statistics,contentDetails", id=",".join(ids[i:i+50]), maxResults=50)
        for c in j.get("items", []):
            out[c["id"]] = dict(id=c["id"], name=c["snippet"]["title"], handle=c["snippet"].get("customUrl"),
                                created=c["snippet"]["publishedAt"], country=c["snippet"].get("country"),
                                subs=int(c["statistics"].get("subscriberCount", 0)), vids=int(c["statistics"].get("videoCount", 0)),
                                views=int(c["statistics"].get("viewCount", 0)),
                                uploads=c["contentDetails"]["relatedPlaylists"]["uploads"])
    return out

def uploads(pl, tag, pages=1):
    ids, tok = [], None
    for k in range(pages):
        p = dict(part="contentDetails", playlistId=pl, maxResults=50)
        if tok: p["pageToken"] = tok
        j = get("playlistItems", f"pl_{tag}_{k}", **p)
        ids += [it["contentDetails"]["videoId"] for it in j.get("items", [])]
        tok = j.get("nextPageToken")
        if not tok: break
    return ids

def comments(vid, n=100):
    j = get("commentThreads", f"cm_{vid}", part="snippet", videoId=vid, order="relevance", maxResults=n, textFormat="plainText")
    return [dict(text=it["snippet"]["topLevelComment"]["snippet"]["textDisplay"],
                 likes=it["snippet"]["topLevelComment"]["snippet"].get("likeCount", 0),
                 replies=it["snippet"].get("totalReplyCount", 0)) for it in j.get("items", [])]

QUERIES = ["3D timelapse city grow", "city growth timelapse", "watch city grow from to 2026 3D timelapse"]

def main():
    step = sys.argv[1]
    if step == "latos":
        j = get("channels", "latos_handle", part="snippet,statistics,contentDetails", forHandle="latoscharts")
        cid = j["items"][0]["id"]
        ch = channels([cid], "latos")
        vids = videos(uploads(ch[cid]["uploads"], "latos"), "latos")
        (DATA / "latos.json").write_text(json.dumps(dict(channel=ch[cid], videos=vids)))
    elif step == "search":
        hits = {}
        for k, q in enumerate(QUERIES):
            j = get("search", f"search_{k}", part="snippet", q=q, type="video", maxResults=50, order="relevance")
            for it in j.get("items", []):
                hits.setdefault(it["id"]["videoId"], []).append(k)
        vids = videos(list(hits), "search")
        for v in vids: v["q"] = hits[v["id"]]
        (DATA / "search.json").write_text(json.dumps(vids))
    elif step == "chans":       # kênh cùng dạng: id truyền qua argv
        ids = sys.argv[2].split(",")
        ch = channels(ids, "comp")
        allv = {}
        for cid, c in ch.items():
            allv[cid] = videos(uploads(c["uploads"], cid[:10]), cid[:10])
        (DATA / "comp.json").write_text(json.dumps(dict(channels=ch, videos=allv)))
    elif step == "comments":
        out = {vid: comments(vid) for vid in sys.argv[2].split(",")}
        (DATA / "comments.json").write_text(json.dumps(out))
    print("quota đã dùng:", used())

if __name__ == "__main__":
    main()
