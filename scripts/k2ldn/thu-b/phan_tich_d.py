#!/opt/cine/bin/python
"""THU-B-T4 · tách nguyên nhân phép (d) quỹ đạo sáng (BAI-HOC-K2 K48) cho cách chiếu theo tỉ số bóng: e_h = max_t |ln(C̄_h(t)/C̄_h(0)) − ln(R̄_h(t)/R̄_h(0))| (độ sáng tuyến tính TB mỗi nhà,
như RULES 1.17.5 (d)) tính lại trên khung PNG (không mã hoá) → so với (1) độ quét bóng trong nhà sd(ln q_h(T)) và (2) độ đổi albedo AI sd(ln I/R0) trong nhà.
  phan_tich_d.py <khung> <tag>  → $THUB/bp/<khung>/<tag>/phan-tich-d.json"""
import json, os, subprocess, sys
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import bmn_thub as B
k, tag = sys.argv[1], sys.argv[2]; o = f'{B.BP}/{k}'; t = f'{o}/{tag}'
IID = cv2.resize(B.dec24(cv2.imread(f'{o}/mat_na_nha.png')).astype(np.float32), (640, 360), interpolation=cv2.INTER_NEAREST).astype(np.int64)
MM = cv2.resize((cv2.imread(f'{o}/do-duoc.png', 0) > 127).astype(np.uint8), (640, 360), interpolation=cv2.INTER_NEAREST) > 0
IID[~MM] = 0; ids = [i for i in np.unique(IID) if i > 0]
I = cv2.resize(cv2.imread(f'{t}/nen.png' if k in B.SONG else f'{t}/ghep.png'), (640, 360), interpolation=cv2.INTER_AREA).astype(np.float64)
src = f'{B.RR}/tl-{k}-v2-kk' if k in B.SONG else f'{B.RR}/tl-{k}-v2'; n = len([x for x in os.listdir(src) if x.endswith('.png')])
Y = lambda x: (B.s2l(x) @ np.array([0.0722, 0.7152, 0.2126]))
tmp = f'{t}/pt-tmp.png'; R0 = None; e = {i: 0.0 for i in ids}; Ri0 = {}; Ci0 = {}
for f in range(n):
    B.lut(f'{src}/{f:05d}.png', tmp); Rb = cv2.imread(tmp).astype(np.float64)
    if R0 is None: R0 = Rb.copy()
    q = (B.s2l(Rb) + 1e-3) / (B.s2l(R0) + 1e-3); C = np.round(B.l2s(B.s2l(I) * q)); yR, yC = Y(Rb), Y(C)
    for i in ids:
        m = IID == i; r, c = yR[m].mean(), yC[m].mean()
        if f == 0: Ri0[i], Ci0[i] = r, c
        else: e[i] = max(e[i], abs(np.log(c / Ci0[i]) - np.log(r / Ri0[i])))
    if f == n - 1: lq = np.log(np.clip(Y(Rb), 1e-4, None) / np.clip(Y(R0), 1e-4, None)); la = np.log(np.clip(Y(I), 1e-4, None) / np.clip(Y(R0), 1e-4, None))
os.remove(tmp)
rows = [dict(id=int(i), e=round(e[i], 3), quet_bong=round(float(lq[IID == i].std()), 3), doi_albedo=round(float(la[IID == i].std()), 3), px=int((IID == i).sum())) for i in ids]
bad = [r for r in rows if r['e'] > 0.10]; good = [r for r in rows if r['e'] <= 0.10]
md = lambda L, k_: round(float(np.median([r[k_] for r in L])), 3) if L else None
out = dict(khung=k, tag=tag, nha=len(rows), lech_gt_010=len(bad), pct=round(100 * len(bad) / max(1, len(rows)), 1),
           trung_vi_quet_bong={'lech': md(bad, 'quet_bong'), 'khong_lech': md(good, 'quet_bong')}, trung_vi_doi_albedo={'lech': md(bad, 'doi_albedo'), 'khong_lech': md(good, 'doi_albedo')},
           ghi_chu='e tính lại trên khung PNG (không mã hoá) theo chữ RULES 1.17.5 (d); số của k2check đo trên video', nha_lech=sorted(bad, key=lambda r: -r['e'])[:15])
json.dump(out, open(f'{t}/phan-tich-d.json', 'w'), ensure_ascii=False, indent=1); print(json.dumps({k_: out[k_] for k_ in ('nha', 'lech_gt_010', 'pct', 'trung_vi_quet_bong', 'trung_vi_doi_albedo')}, ensure_ascii=False))
