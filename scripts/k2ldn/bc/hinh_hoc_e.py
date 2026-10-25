#!/opt/cine/bin/python
"""BAN-CUOI-T4-A · hình học look3d (THU-B D, chạy ĐÚNG scripts/k2ldn/thu-b/hinh_hoc_thub.py d — không sửa tệp đó) + mã TOÀ OSM CÓ TÊN cho mặt nạ `mat_na_ct` (LUẬT E, RULES 1.17.8 (f)).
Ra thêm trong $LDN_DATA/look3e/: hid.f32 = mã toà có tên (1…n, 0 = khác; cùng thứ tự đỉnh ldn2.bin của look3d) + ten.json [{ma, ten, osm_id, E, N, y1}];
mọi tệp khác của look3e là liên kết tới look3d → dựng `--mask 3 --lk look3e/` (look3.js mã hoá 24 bit vHid) cho ra mặt nạ mã toà có tên ĐÚNG che khuất.
  hinh_hoc_e.py           (≈ thời gian hinh_hoc_thub d)"""
import json, os, sys
sys.argv = [sys.argv[0], 'd']
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'thu-b'))
import hinh_hoc_thub as T          # noqa: E402  (MODE d; vá M.house/M.prism như bản gốc)
import numpy as np, cv2            # noqa: E402

T.HL.main()
J = os.path.join(T.HL.OUT, 'ldn2.json'); meta = json.load(open(J)); meta['phien_ban'] = 'look-v2 + cong-trinh-v2 (LOOK-T4-V2) — bản THU-B d'; json.dump(meta, open(J, 'w'), ensure_ascii=False, indent=1)
T.sau_main()
H = T.ARR['H']; K = T.ARR['K']; Ht = H[::3]; Kt = K[::3]
named = T.ten_toa(); ten = []; hid2ma = {}
for hid, inf in T.INFO.items():
    if inf['k'] != 4 or 'ring' not in inf: continue
    rr = np.array(inf['ring'], np.float32).reshape(-1, 1, 2)
    for (a, b, nm, oid) in named:
        if cv2.pointPolygonTest(rr, (float(a), float(b)), False) >= 0:
            ma = len(ten) + 1; hid2ma[hid] = ma
            ten.append(dict(ma=ma, ten=nm, osm_id=oid, E=round(inf['x'] + T.HL.E0, 1), N=round(-inf['z'] + T.HL.N0, 1), y1=round(inf['y1'], 1))); break
ids = np.zeros(len(Ht), np.float64)
sel = (Kt == 4) & np.isin(Ht, np.array(sorted(hid2ma), np.int64))
lut = {h: m for h, m in hid2ma.items()}
ids[sel] = [lut[h] for h in Ht[sel]]
E = os.path.join(T.HL.H0.DATA, 'look3e'); os.makedirs(E, exist_ok=True)
for f in os.listdir(T.HL.OUT):
    if f == 'hid.f32': continue
    d = os.path.join(E, f)
    if os.path.lexists(d): os.remove(d)
    os.symlink(os.path.join(T.HL.OUT, f), d)
np.repeat(ids, 3).astype(np.float32).tofile(os.path.join(E, 'hid.f32'))
json.dump(ten, open(os.path.join(E, 'ten.json'), 'w'), ensure_ascii=False, indent=1)
print(json.dumps(dict(toa_co_ten=len(ten), tam_giac_co_ten=int(sel.sum())), ensure_ascii=False))
