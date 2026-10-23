#!/opt/cine/bin/python
"""TIEN-KY-T4 · khớp toạ độ bản đồ cổ ↔ EPSG:27700 (OSM 2026) bằng điểm khống chế ghi tay.
  khop_ban_do.py channel-k2/k2c-t4-02/mo-hinh/khop-<bản đồ>.json
Tệp vào: {"anh": <tệp + SHA>, "diem": [{"ten", "px":[x,y], "en":[E,N], "nguon_en", "dung": true|false}]}
Ra: thêm "affine", "poly2" (hệ số px→EN), sai số từng điểm (m), RMS, lỗi bỏ-một (LOO) — ghi lại vào chính tệp."""
import json, sys, numpy as np
def design(px, order):
    x, y = px[:, 0] / 1000, px[:, 1] / 1000
    cols = [np.ones_like(x), x, y] + ([x * x, x * y, y * y] if order == 2 else [])
    return np.stack(cols, 1)
def fit(px, en, order):
    A = design(px, order); c, *_ = np.linalg.lstsq(A, en, rcond=None); return c
def apply(c, px, order): return design(np.atleast_2d(px), order) @ c
f = sys.argv[1]; J = json.load(open(f))
D = [d for d in J['diem'] if d.get('dung', True)]; px = np.array([d['px'] for d in D], float); en = np.array([d['en'] for d in D], float)
out = {}
for name, order in (('affine', 1), ('poly2', 2)):
    c = fit(px, en, order); res = np.linalg.norm(apply(c, px, order) - en, axis=1)
    loo = []
    for i in range(len(D)):
        m = np.arange(len(D)) != i; ci = fit(px[m], en[m], order); loo.append(float(np.linalg.norm(apply(ci, px[i], order)[0] - en[i])))
    out[name] = {'he_so': c.tolist(), 'rms_m': float(np.sqrt((res ** 2).mean())), 'max_m': float(res.max()), 'loo_rms_m': float(np.sqrt(np.mean(np.square(loo)))),
                 'loo_max_m': float(max(loo)), 'du': {d['ten']: [round(float(r), 1), round(l, 1)] for d, r, l in zip(D, res, loo)}}
    # điểm kiểm (dung=false) đo bằng mô hình này
    out[name]['kiem'] = {d['ten']: round(float(np.linalg.norm(apply(c, d['px'], order)[0] - np.array(d['en']))), 1) for d in J['diem'] if not d.get('dung', True)}
    print(name, 'RMS %.1f m · max %.1f · LOO RMS %.1f · LOO max %.1f' % (out[name]['rms_m'], out[name]['max_m'], out[name]['loo_rms_m'], out[name]['loo_max_m']), 'kiểm', out[name]['kiem'])
c = np.array(out['affine']['he_so']); sx = np.hypot(c[1, 0], c[1, 1]) / 1000; sy = np.hypot(c[2, 0], c[2, 1]) / 1000
out['affine']['m_moi_px'] = [round(sx, 3), round(sy, 3)]; out['affine']['xoay_do'] = round(float(np.degrees(np.arctan2(c[1, 1], c[1, 0]))), 2)
print('m/px', out['affine']['m_moi_px'], 'xoay', out['affine']['xoay_do'])
J['ket_qua'] = out; json.dump(J, open(f, 'w'), ensure_ascii=False, indent=1)
