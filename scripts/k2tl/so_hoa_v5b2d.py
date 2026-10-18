"""V5b-2d · VẬT MỚI SỐ HOÁ THÊM trên bản đồ Drinkwater 1786 "Plan of the Batteries … 13 Sept 1782" (cùng ảnh + điểm khống chế của phiên SH).
Vào: design/k2v/tl/data/so-hoa-v5b2d-px.json (px bản quét gốc 3995×2837, vùng nắn pho | eo_dat | giua như ghost SH).
Nắn bằng chính mã SH (channel-k2/k2c-t3-01/ghost/tools/ghost.py — Fit/zones, đọc từ bản git archive, không sửa), sai số ước = LOO-RMS của vùng
(dải giữa: max với chênh biến đổi đối chứng eo_dat, như ghost.py build). Ra lớp gói cảnh ENU:
  {name, src, features: [{id, loai, do_tin, ten, ring:[[E,N]…], sai_so_m, dien_tich_m2}], landmarks: {id: {ten, ring}}}
loai: vuon (luống vườn có trên bản đồ) | nha_vuon (ô nhà nhỏ trong GARDENS). landmarks = feature có sẵn của ghost-1782 (nhà thờ, dinh Thống đốc).
  so_hoa_v5b2d.py --ghost-dir <ghost SH> --px <so-hoa-v5b2d-px.json> --out <pack/layers/extra1782.json>"""
import argparse, json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import geo  # noqa: E402

ORIGIN = (-5.3487, 36.1513)   # khớp load_footprints.ORIGIN / meta.json gói gib


def main():
    a = argparse.ArgumentParser(); a.add_argument("--ghost-dir", required=True); a.add_argument("--px", required=True); a.add_argument("--out", required=True)
    A = a.parse_args()
    sys.path.insert(0, os.path.join(A.ghost_dir, "tools")); import ghost  # noqa: E402  (mã SH)
    S = json.load(open(A.px)); G = json.load(open(os.path.join(A.ghost_dir, S["gcp"]))); Z = ghost.zones(G)
    OE, ON = geo.utm(*ORIGIN)
    out = []
    for f in S["features"]:
        z = Z[f["vung"]]; en = z["f"](f["px"]); sai = z["loo"]
        if f["vung"] == "giua": sai = max(sai, float(np.hypot(*(Z["eo_dat"]["f"](f["px"]) - en).T).max()))
        ring = [[round(float(e - OE), 1), round(float(n - ON), 1)] for e, n in en]
        out.append(dict(id=f["id"], loai=f["loai"], do_tin=f["do_tin"], ten=f["ten"], vung=f["vung"], ring=ring, sai_so_m=round(sai), dien_tich_m2=round(ghost.ring_area(en))))
    lm = {}
    g82 = json.load(open(os.path.join(A.ghost_dir, "ghost-1782.geojson")))["features"]
    for f in g82:
        p = f["properties"]
        if p["id"] in S.get("landmarks", []):
            lon, lat = zip(*f["geometry"]["coordinates"][0]); E, N = geo.utm(np.asarray(lon), np.asarray(lat))
            lm[p["id"]] = dict(ten=p.get("ten"), do_tin=p["do_tin"], ring=[[round(float(e - OE), 1), round(float(n - ON), 1)] for e, n in zip(E, N)][:-1], sai_so_m=p.get("sai_so_vi_tri_uoc_m"))
    os.makedirs(os.path.dirname(A.out), exist_ok=True)
    json.dump(dict(name="extra1782", src="Gardens: Drinkwater 1786 plan", nguon=S["nguon_id"], features=out, landmarks=lm), open(A.out, "w"), ensure_ascii=False)
    for o in out: print(o["id"], o["loai"], o["do_tin"], "sai ±%d m" % o["sai_so_m"], "%d m²" % o["dien_tich_m2"], [round(v) for v in np.mean(o["ring"], 0)])
    for k, v in lm.items(): print(k, v["ten"], [round(x) for x in np.mean(v["ring"], 0)])


if __name__ == "__main__":
    main()
