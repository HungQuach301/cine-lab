"""V5b-2b (T3 P0, M9) · BỘ NẠP FOOTPRINT CHUNG: GeoJSON bất kỳ (OSM xuất, Catastro, ghost của phiên SH) hoặc way OSM theo id từ ô thô
→ lớp nhà của gói cảnh tl: $K2TL_CACHE/scene/<gói>/pack/layers/<tên>.json (trang tl nạp qua opt.layers).

Bản ghi toà giống buildings.json + phần tử 8 = THỜI KỲ mái (city.js styleOf): 0 = 1704–1782 · 1 = 1900–1943 · 2 = 2026.
  [năm, năm_ghost, cao, cốt_chân (null → trang lấy theo DTM), mái 0|1, vùng 0 La Línea | 1 Gibraltar, vòng [[E,N]…], thời kỳ]
Thuộc tính GeoJSON được đọc (nếu có): height | building:levels | levels (× 3 m) | h ; start_date | year ; roof (flat|pitched).
Lớp `--kind ghost` = khối TÁI DỰNG (không phải toà cụ thể): năm = 9999 (không bao giờ "mọc thật"), năm_ghost = đầu cửa sổ → dựng bằng nhà đầy đủ
cao 2–4 tầng theo thời kỳ, giảm bão hoà 22 %; nhãn nguồn bắt buộc (`--src`, hiện trên hình, role ghost_src). Cửa sổ năm hiện lớp: --years y0 y1.
KHÔNG vẽ ghost ở đây — chỉ nạp dữ liệu đã số hoá có nguồn (việc số hoá: phiên SH).

  load_footprints.py --pack gib --name ghost1782 --geojson channel-k2/k2c-t3-01/ghost/1782/*.geojson --kind ghost --period 0 --years 1779 1783 --src "Town: reconstructed from Drinkwater 1786 plan"
  load_footprints.py --pack gib --name osm2026 --osm-bbox -5.356,36.1335,-5.347,36.1455 --period 2 --years 2000 2100 --src "Map data from OpenStreetMap (ODbL)"
  load_footprints.py --pack gib --name kings_bastion --osm-ways 952588383 --period 0 --years 1773 2100 --src "OSM way 952588383"
"""
import argparse, glob, json, os, re, sys, xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geo  # noqa: E402

CACHE = Path(os.environ.get("K2TL_CACHE", "/var/tmp/cine-out/k2tl-cache"))
ORIGIN = {"gib": (-5.3487, 36.1513)}   # khớp build_vectors.SCENES (origin_ll trong meta.json của gói)
H_DEF = {0: 7.5, 1: 10.0, 2: 10.0}   # cao mặc định khi nguồn không có (m): ước theo thời kỳ, ghi trong lớp


def enu(pack, lon, lat):
    m = CACHE / "scene" / pack / "pack" / "meta.json"
    o = json.loads(m.read_text())["origin_ll"] if m.exists() else ORIGIN[pack]
    OE, ON = geo.utm(*o); E, N = geo.utm(np.asarray(lon), np.asarray(lat)); return np.asarray(E) - OE, np.asarray(N) - ON


def height_of(pr, period):
    for k in ("height", "h"):
        try: return float(re.sub(r"[^\d.]", "", str(pr[k]))), k
        except (KeyError, ValueError): pass
    for k in ("building:levels", "levels"):
        try: return 3.0 * float(pr[k]) + 1.0, k
        except (KeyError, ValueError): pass
    return H_DEF[period], "mặc định thời kỳ"


def year_of(pr):
    for k in ("start_date", "year", "dateOfConstruction"):
        m = re.search(r"\d{4}", str(pr.get(k, "")))
        if m: return int(m.group())
    return None


def rings_geojson(paths):
    for p in paths:
        G = json.loads(Path(p).read_text())
        for f in G.get("features", [G] if G.get("type") == "Feature" else []):
            g, pr = f.get("geometry") or {}, f.get("properties") or {}
            polys = [g["coordinates"]] if g.get("type") == "Polygon" else g.get("coordinates", []) if g.get("type") == "MultiPolygon" else []
            for poly in polys:
                if poly and len(poly[0]) >= 4: yield poly[0], pr, os.path.basename(p)


def rings_osm(ways=None, bbox=None):
    nodes, out, seen = {}, [], set()
    for t in sorted(glob.glob(str(CACHE / "osm" / "gib" / "*.osm"))):
        root = ET.parse(t).getroot()
        for n in root.iter("node"): nodes[n.get("id")] = (float(n.get("lon")), float(n.get("lat")))
        for w in root.iter("way"):
            wid = w.get("id"); tags = {x.get("k"): x.get("v") for x in w.iter("tag")}
            if wid in seen or (ways and wid not in ways) or (not ways and "building" not in tags): continue
            seen.add(wid); out.append((wid, [nd.get("ref") for nd in w.iter("nd")], tags))
    for wid, refs, tags in out:
        pts = [nodes[r] for r in refs if r in nodes]
        if len(pts) < 4 or pts[0] != pts[-1]: continue
        if bbox and not all(bbox[0] <= x <= bbox[2] and bbox[1] <= y <= bbox[3] for x, y in pts): continue
        yield pts, dict(tags, osm_way=wid), "osm"


def main():
    a = argparse.ArgumentParser(); a.add_argument("--pack", default="gib"); a.add_argument("--name", required=True)
    a.add_argument("--geojson", nargs="*"); a.add_argument("--osm-ways"); a.add_argument("--osm-bbox")
    a.add_argument("--kind", choices=["real", "ghost"], default="real"); a.add_argument("--period", type=int, choices=[0, 1, 2], required=True)
    a.add_argument("--years", type=float, nargs=2, required=True); a.add_argument("--src", required=True); a.add_argument("--region", type=int, default=1)
    A = a.parse_args()
    if A.geojson: it = rings_geojson(A.geojson)
    else: it = rings_osm(set(A.osm_ways.split(",")) if A.osm_ways else None, [float(v) for v in A.osm_bbox.split(",")] if A.osm_bbox else None)
    recs, hsrc, n_year = [], {}, 0
    for ring, pr, srcf in it:
        lon, lat = zip(*[(float(x), float(y)) for x, y in ring]); E, N = enu(A.pack, lon, lat)
        h, hk = height_of(pr, A.period); hsrc[hk] = hsrc.get(hk, 0) + 1; y = year_of(pr)
        if A.kind == "ghost": yr, gy = 9999, A.years[0]
        else: yr, gy = (y if y else A.years[0]), 0; n_year += bool(y)
        roof = 1 if str(pr.get("roof", pr.get("roof:shape", ""))).lower() in ("pitched", "gabled", "hipped", "1") else 0
        recs.append([yr, gy, round(h, 1), None, roof, A.region, [[round(float(e), 2), round(float(n), 2)] for e, n in zip(E, N)], A.period])
    if not recs: sys.exit("LỖI: không có footprint nào (kiểm đường dẫn/id/bbox)")
    out = CACHE / "scene" / A.pack / "pack" / "layers"; out.mkdir(parents=True, exist_ok=True)
    L = dict(name=A.name, kind=A.kind, period=A.period, years=A.years, src=A.src, n=len(recs), height_src=hsrc, n_with_year=n_year,
             input=[os.path.relpath(p) for p in (A.geojson or [])] or ("osm ways " + A.osm_ways if A.osm_ways else "osm bbox " + str(A.osm_bbox)), records=recs)
    (out / f"{A.name}.json").write_text(json.dumps(L, ensure_ascii=False))
    print(json.dumps({k: v for k, v in L.items() if k != "records"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
