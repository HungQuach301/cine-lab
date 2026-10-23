#!/opt/cine/bin/python
"""LOOK-T4-V2 · ĐO CÔNG TRÌNH BIỂU TƯỢNG ở 1080p từ điểm máy P1 (Bankside cao, [532330, 180250, 230]).
  do_cong_trinh.py khai      → channel-k2/k2c-t4-02/look/may-v2/do-*.json (máy đo: P1 nhìn thẳng từng công trình, fov 50° và 36°; + khung M4-rong/M3-rong như tờ so)
  do_cong_trinh.py do <thư mục dựng>   → reports/look-t4-v2/do/cong-trinh.json + reports/look-t4-v2/cong-trinh/*.jpg (ô cắt 1080p phóng ×3 lân cận gần nhất)
Mặt nạ mã công trình (look2.js uMask 2): điểm ảnh lớp 5 mang mã q = round(2·năm bắt đầu) (R = q div 256, G = q mod 256, B = 255); có che khuất thật.
Mã: St Paul's — 1675,5 thân · 1697 trống + hàng cột · 1707 tháp tây · 1708,5 vỏ vòm chì · 1708,8 Golden Gallery + đèn lồng + cầu + thập giá;
Monument — 1671,5 đế + bệ · 1672,5 thân cột · 1676,5 đầu cột + ban công + nón · 1676,9 bầu lửa; White Tower — 1100 khối chính · 1100,5 tháp góc + mũ chì."""
import json, os, sys, glob
import numpy as np, cv2
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MAY = os.path.join(REPO, 'channel-k2/k2c-t4-02/look/may-v2'); RD = os.path.join(REPO, 'reports/look-t4-v2')
P1 = [532330, 180250, 230]
TGT = {'stpauls': [532102, 181122, 70], 'monument': [532923, 180761, 45], 'tower': [533623, 180553, 22]}
NHOM = {'stpauls': {'vom': [1708.5], 'trong': [1697.0], 'den_long': [1708.8], 'thap_tay': [1707.0], 'than': [1675.5]},
        'monument': {'ca': [1671.5, 1672.5, 1676.5, 1676.9], 'be': [1671.5], 'cot': [1672.5], 'bau_lua': [1676.9], 'non': [1676.5]},
        'tower': {'ca': [1100.0, 1100.5], 'khoi': [1100.0], 'thap_goc': [1100.5]}}


def khai():
    base = json.load(open(os.path.join(MAY, 'M4-rong.json'))); n = 0
    for t, l in TGT.items():
        for fov in (50, 36):
            sh = json.loads(json.dumps(base)); k = sh['keys'][0]; k['p'] = P1; k['l'] = l; k['fov'] = fov; sh['vai'] = f'ĐO: P1 nhìn thẳng {t}, fov {fov}°, 2026 ngày'; sh['hero_EN'] = l
            json.dump(sh, open(os.path.join(MAY, f'do-{t}-{fov}.json'), 'w'), ensure_ascii=False, indent=1); n += 1
    print(n, 'máy đo')


def decode(png):
    im = cv2.imread(png)[:, :, ::-1].astype(np.int32)
    ok = im[..., 2] == 255; q = im[..., 0] * 256 + im[..., 1]; yr = np.where(ok, q / 2.0, -1.0); return yr


def rong(yr, codes):
    m = np.isin(yr, codes)
    if not m.any(): return None
    ys, xs = np.nonzero(m); row = np.bincount(ys, minlength=yr.shape[0])
    best = 0
    for y in np.unique(ys):
        xx = xs[ys == y]; best = max(best, int(xx.max() - xx.min() + 1))
    return {'rong_max_px': best, 'cao_px': int(ys.max() - ys.min() + 1), 'diem_anh': int(m.sum()), 'hop': [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]}


def do(root):
    out = {}; os.makedirs(os.path.join(RD, 'cong-trinh'), exist_ok=True); os.makedirs(os.path.join(RD, 'do'), exist_ok=True)
    for d in sorted(glob.glob(os.path.join(root, '*-mask2'))):
        name = os.path.basename(d)[:-6]; yr = decode(os.path.join(d, '00000.png')); rec = {}
        for t, groups in NHOM.items():
            r = {g: rong(yr, c) for g, c in groups.items()}
            if any(v for v in r.values()): rec[t] = r
        out[name] = rec
        jpg = os.path.join(root, name, '00000.jpg')
        if os.path.exists(jpg):
            im = cv2.imread(jpg)
            for t, r in rec.items():
                hb = next((v['hop'] for v in r.values() if v), None)
                if not hb: continue
                x0, y0, x1, y1 = hb; cx, cy = (x0 + x1) // 2, (y0 + y1) // 2; hw = max(60, (x1 - x0) // 2 + 30); hh = max(40, (y1 - y0) // 2 + 30)
                crop = im[max(0, cy - hh):cy + hh, max(0, cx - hw):cx + hw]
                cv2.imwrite(os.path.join(RD, 'cong-trinh', f'{name}-{t}-x3.jpg'), cv2.resize(crop, None, fx=3, fy=3, interpolation=cv2.INTER_NEAREST), [cv2.IMWRITE_JPEG_QUALITY, 90])
    json.dump(out, open(os.path.join(RD, 'do/cong-trinh.json'), 'w'), ensure_ascii=False, indent=1); print(json.dumps(out, ensure_ascii=False)[:3000])


if __name__ == '__main__':
    khai() if sys.argv[1] == 'khai' else do(sys.argv[2])
