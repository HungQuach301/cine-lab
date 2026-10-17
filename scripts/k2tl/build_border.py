"""V5b-2a · RANH GIỚI THẬT cho preset "boundary trace": biên giới đất liền Gibraltar – Tây Ban Nha qua eo đất, lấy từ quan hệ OSM
`type=boundary, boundary=administrative, admin_level=2` (OSM © OpenStreetMap contributors, ODbL 1.0). Ghi vào gói cảnh: lines.json["border"]
(polyline [E, N] m quanh gốc gói cảnh, sắp theo E) + border.json (nguồn, id quan hệ/đường, độ dài). OSM ghi chú các đoạn trên biển "not the definitive
boundary" → chỉ giữ đoạn trên ĐẤT eo đất (hộp N 300…1 200 m, E −1 500…1 500 m quanh giao lộ). Dùng: build_border.py [--name gib]"""
import argparse, json, os, sys, xml.etree.ElementTree as ET
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import geo
CACHE = Path(os.environ.get("K2TL_CACHE", "/var/tmp/cine-out/k2tl-cache"))


def main(name):
    nodes, ways, rels = {}, {}, {}
    for f in sorted((CACHE / "osm" / name).glob("t_*.osm")):
        r = ET.parse(f).getroot()
        for n in r.iter("node"): nodes[n.get("id")] = (float(n.get("lon")), float(n.get("lat")))
        for w in r.iter("way"): ways[w.get("id")] = [nd.get("ref") for nd in w.iter("nd")]
        for rel in r.iter("relation"):
            t = {x.get("k"): x.get("v") for x in rel.iter("tag")}
            if t.get("type") == "boundary" and t.get("admin_level") == "2" and t.get("boundary") == "administrative":
                rels.setdefault(rel.get("id"), (t.get("name", ""), set()))[1].update(m.get("ref") for m in rel.iter("member") if m.get("type") == "way")
    pack = CACHE / "scene" / name / "pack"; meta = json.loads((pack / "meta.json").read_text()); O = geo.utm(*meta["origin_ll"])
    seg, used = [], []
    for rid, (rname, wids) in rels.items():
        for wid in wids:
            pts = [geo.utm(*nodes[k]) for k in ways.get(wid, []) if k in nodes]
            loc = [(round(e - O[0], 1), round(n - O[1], 1)) for e, n in pts]
            keep = [p for p in loc if 300 <= p[1] <= 1200 and -1500 <= p[0] <= 1500]
            if len(keep) >= 2: seg += keep; used.append(dict(relation=rid, name=rname, way=wid, pts=len(keep)))
    seg = sorted(set(seg)); line = [list(p) for p in seg]
    L = sum(((line[i][0] - line[i - 1][0]) ** 2 + (line[i][1] - line[i - 1][1]) ** 2) ** 0.5 for i in range(1, len(line)))
    lines = json.loads((pack / "lines.json").read_text()); lines["border"] = line; (pack / "lines.json").write_text(json.dumps(lines))
    rep = dict(nguon="OSM admin_level=2 boundary (Gibraltar – España), © OpenStreetMap contributors ODbL 1.0", ways=used, n=len(line), len_m=round(L, 1),
               e=[line[0][0], line[-1][0]] if line else None, n_range=[min(p[1] for p in line), max(p[1] for p in line)] if line else None)
    # số cho "hai bên đổi màu theo số": số toà ĐANG ĐỨNG mỗi năm theo vùng của gói cảnh (0 = La Línea, Catastro năm từng toà; 1 = Gibraltar, tầng chuẩn theo mốc;
    # toà tái dựng tính từ năm tái dựng) — số đếm từ dữ liệu cảnh, không tự đặt
    B = json.loads((pack / "buildings.json").read_text()); cnt = {"0": [], "1": []}
    for Y in range(1880, 2027, 2):
        for reg in (0, 1): cnt[str(reg)].append([Y, sum(1 for b in B if b[5] == reg and ((b[1] and b[1] <= Y) or (b[0] and b[0] <= Y)))])
    rep["toa_dung"] = dict(nguon="buildings.json gói cảnh: 0 = La Línea (Catastro INSPIRE dateOfConstruction), 1 = Gibraltar (OSM, mốc 1704/1880/1913/1987/2026)", nam=cnt)
    (pack / "border.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1)); print(json.dumps({k: v for k, v in rep.items() if k != "toa_dung"}, ensure_ascii=False)); print({k: [v[0], v[30], v[-1]] for k, v in cnt.items()})


if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("--name", default="gib"); main(a.parse_args().name)
