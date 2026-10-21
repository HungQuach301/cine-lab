#!/opt/cine/bin/python
"""ĐÓNG-GÓI-T3 · gọi YouTube Data API v3 (khoá do proxy gắn; không in/ghi khoá; UA trung tính, không email).
Ghi mỗi lệnh gọi + đơn vị ước (search 100, các lệnh khác 1) vào nhật ký đơn vị; dừng khi vượt TRAN."""
import json, os, time, urllib.parse, urllib.request
from pathlib import Path
UA = "CineLab-research (+https://github.com/HungQuach301/cine-lab)"
LOG = Path(os.environ.get("YT_LOG", "/tmp/yt-units.jsonl")); TRAN = int(os.environ.get("YT_TRAN", "2000"))
COST = {"search": 100}
def used():
    return sum(json.loads(l)["u"] for l in LOG.read_text().splitlines()) if LOG.exists() else 0
CACHE = Path(os.environ.get("YT_CACHE", "/tmp/yt-cache"))
def get(ep, **p):
    import hashlib
    CACHE.mkdir(parents=True, exist_ok=True); ck = CACHE / (ep + "-" + hashlib.sha1(json.dumps(p, sort_keys=True).encode()).hexdigest() + ".json")
    if ck.exists(): return json.loads(ck.read_text())   # bộ đệm: chạy lại không tốn đơn vị
    u = COST.get(ep, 1)
    if used() + u > TRAN: raise SystemExit(f"dừng: vượt trần {TRAN} đơn vị (đã {used()})")
    url = f"https://www.googleapis.com/youtube/v3/{ep}?" + urllib.parse.urlencode(p)
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60) as r:
                d = json.load(r); break
        except Exception as e:
            if i == 3: raise
            time.sleep(2 ** (i + 1))
    with open(LOG, "a") as f: f.write(json.dumps({"ep": ep, "u": u, "t": time.strftime("%H:%M:%S")}) + "\n")
    ck.write_text(json.dumps(d))
    return d
