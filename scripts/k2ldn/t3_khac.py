#!/opt/cine/bin/python
"""TIEN-KY-T4 · BẢN THỬ T3 — tranh khắc/bản vẽ Hollar "Old St Paul's seen from the East" (Met 2010.529, CC0) hoà vào 3D cùng góc.
  t3_khac.py <thư mục khung 3D (render_ldn.js + log.json)> <ra> [--hoa 3.0:5.0]
Không AI chạm tư liệu. Thao tác cho phép: (1) phép chiếu phối cảnh (homography) 4 điểm của mặt đông để đăng ký tranh lên mặt đông của mô hình — đo và ghi sai lệch
từng điểm; (2) thị sai 2,5D THỦ CÔNG: mặt nạ toà nhà vẽ tay bằng đa giác (toạ độ ghi trong tệp này), lớp nền giấy/trời phóng chậm hơn lớp nhà;
(3) hoà mờ tranh → 3D. Bản vẽ gốc giữ nguyên nét (lấy mẫu song tuyến)."""
import json, os, sys
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
SRC = os.environ.get('LDN_SRC', '/var/tmp/ldn/tu-lieu'); DATA = os.environ.get('LDN_DATA', '/var/tmp/ldn')
IN, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
h0, h1 = (float(x) for x in (sys.argv[sys.argv.index('--hoa') + 1] if '--hoa' in sys.argv else '3.0:5.0').split(':'))
LOG = json.load(open(os.path.join(IN, 'log.json'))); W, H = LOG['W'], LOG['H']; FPS = LOG['shot'].get('fps', 24)
D = cv2.imread(os.path.join(SRC, 'met-395057-0.jpg'))[:, :, ::-1].astype(np.float32) / 255.0; DH, DW = D.shape[:2]; s = DW / 2000.0   # toạ độ ghi theo bản xem 2000 px
# 4 điểm mặt đông trên tranh (bản xem 2000 px): chân trụ trái, chân trụ phải, đỉnh trụ trái ở mép mái, đỉnh trụ phải — đọc tay
Q_TRANH = np.array([[1000, 1525], [1655, 1525], [1135, 470], [1445, 470]], float) * s   # chân tường gian bên trái/phải · mép mái thân giữa trái/phải
# cùng 4 điểm trên mô hình (u, v, y) theo trục Old St Paul's (hinh_hoc.py: nhà 176 m, gian bên ±21 m, tường gian bên 16 m)
Q_MOHINH = [(88.0, -16.0, 0.0), (88.0, 16.0, 0.0), (88.0, -7.0, 28.0), (88.0, 7.0, 28.0)]
# mặt nạ toà nhà vẽ tay (đa giác, bản xem 2000 px) — lớp trước cho thị sai 2,5D
POLY = np.array([[60, 1570], [60, 560], [180, 470], [640, 470], [700, 380], [760, 60], [940, 30], [1150, 160], [1180, 380], [1280, 380], [1460, 470], [1760, 470], [1880, 560], [1880, 1570]], float) * s
M = json.load(open(os.path.join(DATA, 'canh/ldn.json'))); c = np.array(M['old_st_pauls_EN'])
ax = np.array([0.98949186, 0.14458857]); vv = np.array([-ax[1], ax[0]])
dtm = np.load(os.path.join(DATA, 'lidar/dtm_kham_1m.npy')); g = float(dtm[int(182500 - c[1]), int(c[0] - 529500)])
def proj(r, u, v, y):
    e = c + ax * u + vv * v; X = np.array([e[0] - 532000, g + y, -(e[1] - 180800), 1.0])
    V = np.array(r['view']).reshape(4, 4).T; P = np.array(r['proj']).reshape(4, 4).T; q = P @ V @ X; q = q[:3] / q[3]
    return [(q[0] + 1) / 2 * W, (1 - q[1]) / 2 * H]
mask = np.zeros((DH, DW), np.float32); cv2.fillPoly(mask, [POLY.astype(np.int32)], 1.0); mask = cv2.GaussianBlur(mask, (0, 0), 3 * s)
frames = sorted(LOG['frames'], key=lambda r: r['f']); log = {'hoa_s': [h0, h1], 'diem_tranh': Q_TRANH.tolist(), 'diem_mohinh_uvy': Q_MOHINH}
for r in frames:
    f = r['f']; t = f / FPS; im3 = cv2.imread(os.path.join(IN, f'{f:05d}.jpg'))[:, :, ::-1].astype(np.float32) / 255.0
    q3 = np.array([proj(r, *q) for q in Q_MOHINH], np.float32)
    Hm = cv2.getPerspectiveTransform(Q_TRANH.astype(np.float32), q3)
    if f == frames[0]['f']: log['homography_khung0'] = Hm.tolist(); log['diem_3d_khung0_px'] = q3.tolist()
    if t < h1:
        # thị sai 2,5D thủ công trước lúc hoà: nền giấy phóng 1,000 → 1,004, lớp nhà 1,000 → 1,014 (quanh tâm mặt đông)
        u = min(1.0, t / max(h0, 1e-3)); cx, cy = q3[:, 0].mean(), q3[:, 1].mean()
        def S(k): return np.array([[k, 0, cx * (1 - k)], [0, k, cy * (1 - k)], [0, 0, 1]])
        bg = cv2.warpPerspective(D, S(1 + 0.004 * u) @ Hm, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0.86, 0.80, 0.68))
        fg = cv2.warpPerspective(D, S(1 + 0.014 * u) @ Hm, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0.86, 0.80, 0.68))
        mk = cv2.warpPerspective(mask, S(1 + 0.014 * u) @ Hm, (W, H), flags=cv2.INTER_LINEAR)[..., None]
        dr = bg * (1 - mk) + fg * mk
        k = 0.0 if t < h0 else (t - h0) / (h1 - h0); k = k * k * (3 - 2 * k)
        out = dr * (1 - k) + im3 * k
    else:
        out = im3
    Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).save(os.path.join(OUT, f'{f:05d}.jpg'), quality=92)
# sai lệch đăng ký: đỉnh hồi mặt đông + tâm cửa sổ hoa hồng + đỉnh tháp (không dùng để khớp) sau homography so với chiếu mô hình
r0 = frames[0]; Hm = np.array(log['homography_khung0'])
chk = {'dinh_hoi_dong': ((1278, 388), (88.0, 0.0, 40.0)), 'tam_cua_so_hoa_hong': ((1310, 860), (88.5, 0.0, 17.3)), 'dinh_thap': ((938, 38), (10.0, 0.0, 91.0))}
log['sai_lech_px'] = {}
for k, (pt, uvy) in chk.items():
    p = Hm @ np.array([pt[0] * s, pt[1] * s, 1.0]); p = p[:2] / p[2]; q = proj(r0, *uvy); log['sai_lech_px'][k] = round(float(np.hypot(p[0] - q[0], p[1] - q[1])), 1)
json.dump(log, open(os.path.join(OUT, 't3.json'), 'w'), ensure_ascii=False, indent=1); print(json.dumps(log['sai_lech_px'], ensure_ascii=False))
