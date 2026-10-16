"""V5b-1 · bước 2 gói cảnh: vector ENU cục bộ từ OSM (© OpenStreetMap contributors, ODbL) + Catastro INSPIRE BU (D.G. del Catastro).
Ra $K2TL_CACHE/scene/<tên>/v_osm.json (toà, đường, đường băng, tường thành, cây…) và v_catastro.json (phần toà: vòng, năm xây, số tầng).
Toạ độ: m quanh gốc của build_rasters.py (E đông, N bắc)."""
import argparse, glob, json, os, re, collections
import xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
import geo
from build_rasters import SCENES, CACHE

def load_osm(d):
    nodes, ways, rels = {}, {}, {}
    for f in sorted(glob.glob(str(d / "t_*.osm"))):
        for e in ET.parse(f).getroot():
            if e.tag == "node": nodes[e.get("id")] = (float(e.get("lon")), float(e.get("lat")), {t.get("k"): t.get("v") for t in e.findall("tag")})
            elif e.tag == "way": ways[e.get("id")] = ([n.get("ref") for n in e.findall("nd")], {t.get("k"): t.get("v") for t in e.findall("tag")})
            elif e.tag == "relation": rels[e.get("id")] = ([(m.get("type"), m.get("ref"), m.get("role")) for m in e.findall("member")], {t.get("k"): t.get("v") for t in e.findall("tag")})
    return nodes, ways, rels

def main(name):
    S = SCENES[name]; out = CACHE / "scene" / name; OE, ON = map(float, geo.utm(*S["origin_ll"])); e0, n0, e1, n1 = S["ext"]
    nodes, ways, rels = load_osm(CACHE / "osm" / name)
    ids = sorted(nodes); ll = np.array([nodes[i][:2] for i in ids]); E, N = geo.utm(ll[:, 0], ll[:, 1])
    P = {i: (round(float(x - OE), 2), round(float(y - ON), 2)) for i, x, y in zip(ids, E, N)}
    def line(nd): return [P[n] for n in nd if n in P]
    R = collections.defaultdict(list)
    used = set()
    for wid, (nd, t) in ways.items():
        pts = line(nd)
        if len(pts) < 2: continue
        rec = dict(id=wid, p=pts, t={k: v for k, v in t.items() if k in ("building", "building:levels", "height", "roof:shape", "name", "highway", "width", "lanes", "aeroway", "historic", "barrier", "natural", "landuse", "leisure", "start_date", "layer", "tunnel", "bridge", "man_made", "runway", "surface", "castle_type", "defensive_works", "amenity", "parking", "sport", "railway")})
        if "building" in t: R["building"].append(rec)
        elif "highway" in t: R["highway"].append(rec)
        elif "aeroway" in t: R["aeroway"].append(rec)
        elif t.get("barrier") in ("city_wall", "wall", "fence", "retaining_wall") or t.get("historic") in ("citywalls", "fort", "castle"): R["wall"].append(rec)
        elif t.get("natural") in ("coastline",): R["coast"].append(rec)
        elif "natural" in t or "landuse" in t or "leisure" in t or t.get("amenity") in ("parking", "school", "hospital") or t.get("place") == "square": R["area"].append(rec)   # V5b-1b: + bãi đỗ, sân trường (phân lớp nền)
        elif t.get("man_made") in ("breakwater", "pier", "groyne"): R["pier"].append(rec)
    for rid, (mem, t) in rels.items():   # toà multipolygon: chỉ vòng ngoài
        if "building" in t:
            for ty, ref, role in mem:
                if ty == "way" and role == "outer" and ref in ways: R["building"].append(dict(id="r" + rid, p=line(ways[ref][0]), t={k: v for k, v in t.items() if k in ("building", "building:levels", "height", "name")}))
    R["tree"] = [P[i] for i in ids if nodes[i][2].get("natural") == "tree"]
    (out / "v_osm.json").write_text(json.dumps(R, separators=(",", ":")))
    print({k: len(v) for k, v in R.items()})
    # ---- Catastro: toà (năm) + phần toà (số tầng, vòng)
    gml = CACHE / "catastro"
    bt = (gml / "A.ES.SDGC.BU.11022.building.gml").read_text(encoding="utf-8")
    year = {}
    for m in re.finditer(r'<bu-ext2d:Building gml:id="ES\.SDGC\.BU\.([^"]+)">(.*?)</bu-ext2d:Building>', bt, re.S):
        y = re.search(r"<bu-core2d:beginning>(\d{4})", m.group(2)); use = re.search(r"<bu-ext2d:currentUse>([^<]*)", m.group(2))
        year[m.group(1)] = (int(y.group(1)) if y else 0, use.group(1) if use else "")
    pt = (gml / "A.ES.SDGC.BU.11022.buildingpart.gml").read_text(encoding="utf-8")
    parts = []; skip = collections.Counter()
    for m in re.finditer(r'<bu-ext2d:BuildingPart gml:id="ES\.SDGC\.BU\.([^"]+)">(.*?)</bu-ext2d:BuildingPart>', pt, re.S):
        pid, body = m.group(1), m.group(2); bid = pid.split("_part")[0]
        fl = re.search(r"<bu-ext2d:numberOfFloorsAboveGround>(\d+)", body); fl = int(fl.group(1)) if fl else 0
        pos = re.search(r"<gml:exterior>.*?<gml:posList[^>]*>([^<]+)</gml:posList>", body, re.S)
        if not pos: skip["nogeom"] += 1; continue
        v = np.array(pos.group(1).split(), float).reshape(-1, 2); v[:, 0] -= OE; v[:, 1] -= ON
        cx, cy = v[:, 0].mean(), v[:, 1].mean()
        if not (e0 < cx < e1 and n0 < cy < n1): skip["out"] += 1; continue
        if fl <= 0: skip["0floor"] += 1; continue
        y, use = year.get(bid, (0, ""))
        parts.append(dict(b=bid, y=y, f=fl, u=use, p=[[round(a, 2), round(b, 2)] for a, b in v[:-1]]))
    (out / "v_catastro.json").write_text(json.dumps(parts, separators=(",", ":")))
    ys = [p["y"] for p in parts if p["y"]]
    print("catastro parts", len(parts), dict(skip), "years", min(ys), max(ys), "pre1900", sum(y < 1900 for y in ys), "buildings", len({p['b'] for p in parts}))

if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("--name", default="gib"); main(a.parse_args().name)
