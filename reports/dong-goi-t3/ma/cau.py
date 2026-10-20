#!/opt/cine/bin/python
"""ĐÓNG-GÓI-T3 việc 1 · kiểm cầu: 1 truy vấn "gibraltar" (2 năm, xếp theo lượt xem) + lọc cục bộ cửa sổ 90 ngày;
các truy vấn siege/border/Gibraltar-history lấy lại từ quét ngách (đã có, không tốn thêm đơn vị). Ghi thô ra thư mục tạm (đối số 1)."""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import yt
OUT = Path(sys.argv[1])
r = yt.get("search", part="snippet", q="gibraltar", type="video", maxResults=50, publishedAfter="2024-10-19T00:00:00Z", order="viewCount")
ids = [it["id"]["videoId"] for it in r.get("items", [])]
def dur_s(iso):
    m = re.match(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or ""); d, h, mi, s = (int(x or 0) for x in m.groups()); return d * 86400 + h * 3600 + mi * 60 + s
out = []
for it in yt.get("videos", part="snippet,statistics,contentDetails", id=",".join(ids), maxResults=50)["items"]:
    out.append({"id": it["id"], "title": it["snippet"]["title"], "ch": it["snippet"]["channelId"], "pub": it["snippet"]["publishedAt"][:10],
                "views": int(it["statistics"].get("viewCount", 0)), "dur": dur_s(it.get("contentDetails", {}).get("duration"))})
json.dump(out, open(OUT / "cau-gibraltar-raw.json", "w"), ensure_ascii=False, indent=1); print(len(out), "video; đơn vị", yt.used())
