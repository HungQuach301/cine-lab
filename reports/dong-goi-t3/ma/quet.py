#!/opt/cine/bin/python
"""ĐÓNG-GÓI-T3 việc 0 · quét ngách: 8 truy vấn × ≤ 50 video (đăng từ 2023-01-01), thống kê video + kênh,
điểm vượt trội = lượt xem / trung vị lượt xem 20 video gần nhất của kênh (danh sách uploads).
Ghi dữ liệu thô (CÓ tiêu đề đối thủ) vào thư mục tạm ngoài git (đối số 1). Repo chỉ nhận số + đặc trưng (dactrung.py)."""
import json, re, statistics, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import yt
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
# Lượt 1 (8 truy vấn) mất dữ liệu do lỗi KeyError 'duration' sau khi đã tiêu 1 121 đơn vị → lượt 2 gọn 6 truy vấn để giữ trần 2 000.
Q = {"q1_3d_timelapse_city": "3d time lapse city", "q2_watch_grow": "watch city grow timelapse",
     "q3_history_animated": "history of the city animated", "q4_siege": "siege history animated",
     "q5_contested_border": "contested territory border history", "q6_gibraltar": "gibraltar history"}
def dur_s(iso):
    m = re.match(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or ""); d, h, mi, s = (int(x or 0) for x in m.groups()); return d * 86400 + h * 3600 + mi * 60 + s
hits = {}
for k, q in Q.items():
    r = yt.get("search", part="snippet", q=q, type="video", maxResults=50, publishedAfter="2023-01-01T00:00:00Z", order="relevance", relevanceLanguage="en")
    for rank, it in enumerate(r.get("items", [])):
        hits.setdefault(it["id"]["videoId"], []).append([k, rank])
ids = list(hits)[:300] if len(hits) > 300 else list(hits)
# ưu tiên giữ đủ mỗi truy vấn nếu > 300: cắt theo hạng thấp nhất
if len(hits) > 300:
    ids = sorted(hits, key=lambda v: min(r for _, r in hits[v]))[:300]
vids = {}
for i in range(0, len(ids), 50):
    for it in yt.get("videos", part="snippet,statistics,contentDetails", id=",".join(ids[i:i + 50]), maxResults=50)["items"]:
        s = it["statistics"]; vids[it["id"]] = {"id": it["id"], "title": it["snippet"]["title"], "ch": it["snippet"]["channelId"], "chname": it["snippet"]["channelTitle"],
            "pub": it["snippet"]["publishedAt"][:10], "views": int(s.get("viewCount", 0)), "likes": int(s.get("likeCount", 0) or 0), "comments": int(s.get("commentCount", 0) or 0),
            "dur": dur_s(it.get("contentDetails", {}).get("duration")), "q": hits[it["id"]], "lang": it["snippet"].get("defaultAudioLanguage") or it["snippet"].get("defaultLanguage")}
chs = sorted({v["ch"] for v in vids.values()}); cinfo = {}
for i in range(0, len(chs), 50):
    for it in yt.get("channels", part="statistics,contentDetails", id=",".join(chs[i:i + 50]), maxResults=50)["items"]:
        cinfo[it["id"]] = {"subs": int(it["statistics"].get("subscriberCount", 0) or 0), "hidden": it["statistics"].get("hiddenSubscriberCount", False),
                           "nvid": int(it["statistics"].get("videoCount", 0) or 0), "uploads": it["contentDetails"]["relatedPlaylists"]["uploads"]}
json.dump(list(vids.values()), open(OUT / "videos-raw.json", "w"), ensure_ascii=False, indent=1)
# mốc kênh chỉ cho kênh có video dài (> 180 s) trong mẫu — tiết kiệm đơn vị; Shorts không vào phân tích
need = {v["ch"] for v in vids.values() if v["dur"] > 180}
recent = {}
for c, ci in cinfo.items():
    if c not in need: continue
    try:
        r = yt.get("playlistItems", part="contentDetails", playlistId=ci["uploads"], maxResults=20)
        recent[c] = [x["contentDetails"]["videoId"] for x in r.get("items", [])]
    except Exception as e:
        recent[c] = []
allr = sorted({v for l in recent.values() for v in l}); rv = {}
for i in range(0, len(allr), 50):
    for it in yt.get("videos", part="statistics,contentDetails", id=",".join(allr[i:i + 50]), maxResults=50)["items"]:
        rv[it["id"]] = (int(it["statistics"].get("viewCount", 0)), dur_s(it.get("contentDetails", {}).get("duration")))
for v in vids.values():
    ci = cinfo.get(v["ch"], {}); lst = [rv[x][0] for x in recent.get(v["ch"], []) if x in rv]
    med = statistics.median(lst) if lst else None
    v.update(subs=ci.get("subs"), subs_hidden=ci.get("hidden"), ch_n_recent=len(lst), ch_median20=med, outlier=(v["views"] / med) if med else None)
json.dump(list(vids.values()), open(OUT / "videos-raw.json", "w"), ensure_ascii=False, indent=1)
print(len(hits), "kết quả;", len(vids), "video;", len(cinfo), "kênh; đơn vị đã dùng", yt.used())
