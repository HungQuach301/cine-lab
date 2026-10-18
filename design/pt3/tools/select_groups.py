"""PT3 · chọn nhóm mặt cần vân HC7 từ lượt probe (mã nhóm ở khung mẫu dọc cú máy, 480×270).
street: nhóm 'elev' được chọn nếu ở ÍT NHẤT một khung mẫu nó chiếm ≥ NGUONG (0,2 % khung; phủ 84 % điểm ảnh mặt tường) — nhóm nhỏ hơn giữ vân A.
kb: công trình điểm nhấn → MỌI nhóm của bastion (bid 8000) thấy được ở ≥ 1 khung mẫu, dù nhỏ; toà phố 1782 quanh bastion giữ A (chỉ một công trình nhận HC7).
  /opt/cine/bin/python -I select_groups.py <thư mục probe> <site> <ra groups.json>"""
import sys, os, json, glob, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scene'))
import exr, cams as CM
D, site, OUT = sys.argv[1], sys.argv[2], sys.argv[3]; NGUONG = 0.002
meta = json.load(open(os.path.join(D, 'meta.json'))); G = meta['groups']; st = CM.SITE[site]
mx = collections.Counter(); top_px = 0; fr = 0
for p in sorted(glob.glob(os.path.join(D, 'probe*_grp.exr'))):
    g = np.rint(exr.read(p, 'R')[..., 0]).astype(int); n = g.size; fr += 1
    v, c = np.unique(g, return_counts=True)
    for vv, cc in zip(v, c):
        if vv >= 3: mx[int(vv) - 2] = max(mx[int(vv) - 2], float(cc) / n)
    top_px = max(top_px, int((g == 1).sum()))
px = collections.Counter()
for p in sorted(glob.glob(os.path.join(D, 'probe*_grp.exr'))):
    g = np.rint(exr.read(p, 'R')[..., 0]).astype(int); v, c = np.unique(g, return_counts=True)
    for vv, cc in zip(v, c):
        if vv >= 3: px[int(vv) - 2] += int(cc)
if site == 'kb': sel = sorted(k for k in range(1, len(G)) if G[k]['bid'] == 8000 and mx.get(k, 0) > 0 and G[k]['z1'] - G[k]['z0'] > 4.0)   # trừ tường thấp phía đất (cao 2,2 m, quay vào phố) — giữ A   # mọi mặt bastion THẤY ĐƯỢC ở ≥ 1 khung mẫu hoặc góc tấm chiếu
else: sel = sorted(k for k, f in mx.items() if f >= NGUONG)
phu = round(sum(px[k] for k in sel) / max(1, sum(px.values())), 3) if site != 'kb' else round(sum(px[k] for k in sel if G[k]['bid'] == 8000) / max(1, sum(v for k, v in px.items() if G[k]['bid'] == 8000)), 3)
elev = collections.defaultdict(list)
for k in sel: elev[str(G[k]['bid'])].append(k)
for b in elev: elev[b].sort(key=lambda k: G[k]['order'])
req = {'site': site, 'ppm': st['ppm_elev'], 'elev': dict(elev), 'top': {'rect': list(st['top_rect']), 'ppm': st['ppm_top']},
       'thong_ke': {'khung_mau': fr, 'nhom_thay': len(mx), 'nhom_chon': len(sel), 'toa_chon': len(elev), 'nguong_phan_khung': NGUONG,
                    'nhom_bo_vi_nho': sum(1 for k in mx if k not in sel), 'phu_diem_anh_tuong': phu, 'tong_dai_m': round(sum(G[k]['L'] for k in sel), 1), 'top_px_max': top_px,
                    'phan_khung_max': {str(k): round(mx.get(k, 0), 4) for k in sel}}}
json.dump(req, open(OUT, 'w'), indent=1); print(json.dumps(req['thong_ke'], ensure_ascii=False)[:600]); print({b: len(v) for b, v in elev.items()})
