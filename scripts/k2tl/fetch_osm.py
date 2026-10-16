"""V5b-1 · tải OSM (API 0.6 /map, chia ô thích nghi) cho vùng cảnh → $K2TL_CACHE/osm/<tên>/t_*.osm.
OSM © OpenStreetMap contributors, ODbL 1.0 — ghi công trên hình/mô tả. Overpass bị 504/ngắt ở proxy (đo 15/10), nên dùng API /map
(giới hạn 50 000 nút/lượt → ô quá đầy trả 400 thì chia 4). Dùng: fetch_osm.py --name gib --bbox -5.385,36.105,-5.320,36.185 [--step 0.02]"""
import argparse, os, subprocess, time, sys
from pathlib import Path
CACHE = Path(os.environ.get("K2TL_CACHE", "/var/tmp/cine-out/k2tl-cache"))
UA = "cine-lab/1.0 (channel research)"

def get(b, out):
    u = "https://api.openstreetmap.org/api/0.6/map?bbox=%.5f,%.5f,%.5f,%.5f" % b
    r = subprocess.run(["curl", "-s", "-m", "180", "-A", UA, "-o", str(out), "-w", "%{http_code}", u], capture_output=True, text=True)
    return r.stdout.strip()

def tile(b, d, depth=0):
    out = d / ("t_%.4f_%.4f_%.4f_%.4f.osm" % b)
    if out.exists() and out.stat().st_size > 200: return 1
    for k in range(4):
        code = get(b, out); time.sleep(1.0)
        if code == "200": return 1
        if code == "400" and depth < 4:   # quá 50 000 nút
            out.unlink(missing_ok=True); x0, y0, x1, y1 = b; xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
            return sum(tile(q, d, depth + 1) for q in [(x0, y0, xm, ym), (xm, y0, x1, ym), (x0, ym, xm, y1), (xm, ym, x1, y1)])
        time.sleep(2 ** (k + 1))
    raise SystemExit(f"LỖI tải ô {b}: {code}")

if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("--name", required=True); a.add_argument("--bbox", required=True); a.add_argument("--step", type=float, default=0.02)
    o = a.parse_args(); x0, y0, x1, y1 = map(float, o.bbox.split(",")); d = CACHE / "osm" / o.name; d.mkdir(parents=True, exist_ok=True)
    n = 0; y = y0
    while y < y1 - 1e-9:
        x = x0
        while x < x1 - 1e-9:
            n += tile((x, y, min(x1, x + o.step), min(y1, y + o.step)), d); x += o.step
        y += o.step
    print(n, "ô", sum(f.stat().st_size for f in d.glob("t_*.osm")) // 1e6, "MB")
