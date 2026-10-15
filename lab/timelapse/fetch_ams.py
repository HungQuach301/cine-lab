"""Tải chân móng LoD1.2 + chiều cao + năm xây (3DBAG WFS, CC BY 4.0; dữ liệu nền BAG của Kadaster, CC0) cho một bbox RD New.
Dữ liệu thô ở ngoài git: $TL_DATA/ams/raw_*.json. Dùng: fetch_ams.py x0 y0 x1 y1"""
import json, os, sys, time
from pathlib import Path
import requests

DATA = Path(os.environ.get("TL_DATA", Path.home() / ".cache/cine-timelapse")) / "ams"
DATA.mkdir(parents=True, exist_ok=True)
URL = "https://data.3dbag.nl/api/BAG3D/wfs"
PROPS = "geom,identificatie,oorspronkelijkbouwjaar,b3_h_70p,b3_h_maaiveld,status,b3_pand_deel_id"
PAGE = 5000

def main():
    x0, y0, x1, y1 = sys.argv[1:5]
    start = 0
    while True:
        f = DATA / f"raw_{start:07d}.json"
        if not f.exists():
            p = dict(request="getfeature", service="wfs", version="2.0.0", typenames="BAG3D:lod12",
                     bbox=f"{x0},{y0},{x1},{y1}", outputFormat="application/json", count=PAGE, startIndex=start,
                     propertyName=PROPS, sortBy="fid")
            for i in range(4):
                try:
                    r = requests.get(URL, params=p, timeout=300)
                    if r.status_code == 200:
                        break
                except requests.RequestException as e:
                    print(type(e).__name__, file=sys.stderr)
                time.sleep(2 ** (i + 1))
            f.write_text(r.text)
        n = len(json.loads(f.read_text())["features"])
        print(start, n, flush=True)
        if n < PAGE:
            break
        start += PAGE

if __name__ == "__main__":
    main()
