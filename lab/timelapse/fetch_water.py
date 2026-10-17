"""Mặt nước BGT (Kadaster/PDOK OGC API, CC0) trong bbox RD New → $TL_DATA/ams/water_*.json (ngoài git)."""
import json, os, sys, time
from pathlib import Path
import requests
DATA = Path(os.environ.get("TL_DATA", Path.home() / ".cache/cine-timelapse")) / "ams"
URL = "https://api.pdok.nl/lv/bgt/ogc/v1/collections/waterdeel/items"
RD = "http://www.opengis.net/def/crs/EPSG/0/28992"
def main():
    x0, y0, x1, y1 = sys.argv[1:5]
    url, p, k = URL, dict(f="json", limit=1000, bbox=f"{x0},{y0},{x1},{y1}", **{"bbox-crs": RD, "crs": RD}), 0
    while url:
        f = DATA / f"water_{k:04d}.json"
        if f.exists():
            j = json.loads(f.read_text())
        else:
            for i in range(4):
                r = requests.get(url, params=p, timeout=300)
                if r.status_code == 200: break
                time.sleep(2 ** (i + 1))
            j = r.json(); f.write_text(r.text)
        print(k, len(j["features"]), flush=True)
        nxt = [l["href"] for l in j.get("links", []) if l["rel"] == "next"]
        url, p, k = (nxt[0] if nxt else None), None, k + 1
if __name__ == "__main__":
    main()
