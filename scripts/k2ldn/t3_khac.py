#!/opt/cine/bin/python
"""TIEN-KY-T4 · BẢN THỬ T3 (v2) — bản vẽ Hollar "Old St Paul's seen from the East" (Met 2010.529, CC0) hoà vào 3D CÙNG GÓC.
  t3_khac.py <thư mục khung 3D (render_ldn.js + log.json; khung W × H2, cắt H dòng trên)> <ra> [--H 720] [--uon 1.5:3.0] [--hoa 3.0:5.0]
Máy 3D giải từ bản vẽ bằng scripts/k2ldn/t3_may.py (trục ngang + dịch ống kính). KHÔNG AI chạm tư liệu. Thao tác cho phép, đều là biến đổi hình học/độ mờ:
 (1) tranh đặt nguyên khung (đồng dạng: vừa chiều cao, giữa khung) — nét gốc giữ nguyên (lấy mẫu song tuyến);
 (2) thị sai 2,5D THỦ CÔNG trong đoạn tĩnh: mặt nạ toà nhà vẽ tay bằng đa giác (toạ độ trong tệp), lớp nhà phóng 1,000 → 1,012, nền giấy 1,000 → 1,003;
 (3) UỐN dần (đoạn --uon) từ phép đồng dạng sang phép chiếu phối cảnh (homography) khớp 7 điểm mặt đông của tranh lên chính các điểm đó của mô hình chiếu qua máy
     từng khung (nội suy 4 góc tranh) → mặt đông nằm đúng mô hình trước lúc hoà;
 (4) hoà mờ tranh → 3D (đoạn --hoa). Ghi sai lệch đăng ký từng điểm (px khung) vào t3.json."""
import json, os, sys
import numpy as np, cv2
from PIL import Image
SRC = os.environ.get('LDN_SRC', '/var/tmp/ldn/tu-lieu'); DATA = os.environ.get('LDN_DATA', '/var/tmp/ldn')
IN, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
def rng(k, d): return [float(x) for x in (sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d).split(':')]
u0, u1 = rng('--uon', '1.5:3.0'); h0, h1 = rng('--hoa', '3.0:5.0')
LOG = json.load(open(os.path.join(IN, 'log.json'))); W, H2 = LOG['W'], LOG['H']; FPS = LOG['shot'].get('fps', 24)
H = int(sys.argv[sys.argv.index('--H') + 1]) if '--H' in sys.argv else int(round(W * 9 / 16))
D = cv2.imread(os.path.join(SRC, 'met-395057-0.jpg'))[:, :, ::-1].astype(np.float32) / 255.0; DH, DW = D.shape[:2]; s = DW / 2000.0   # toạ độ đọc tay theo bản xem 2000 px
PAPER = (0.86, 0.80, 0.68)
# 7 điểm mặt đông (tranh bản 2000 px ↔ mô hình u, v, y; v + = bắc) — cùng bộ với t3_may.py
FACE = [((1000, 1500), (88.0, -16.0, 0.0)), ((1714, 1500), (88.0, 16.0, 0.0)), ((1186, 1000), (88.0, -7.0, 15.0)), ((1457, 1000), (88.0, 7.0, 15.0)),
        ((1214, 671), (88.0, -7.0, 28.0)), ((1429, 671), (88.0, 7.0, 28.0)), ((1293, 393), (88.0, 0.0, 40.0))]
KHAC = {'tam_cua_so_hoa_hong': ((1314, 871), (88.5, 0.0, 17.3)), 'tam_dinh_thap': ((971, 64), (10.0, 0.0, 87.0)), 'chan_canh_ngang_nam': ((64, 1264), (19.0, -44.0, 0.0))}
# mặt nạ toà nhà vẽ tay (đa giác, bản 2000 px) — lớp trước cho thị sai
POLY = np.array([[60, 1500], [60, 520], [180, 470], [640, 470], [700, 380], [760, 60], [1110, 60], [1150, 380], [1280, 380], [1460, 470], [1760, 470], [1880, 560], [1880, 1500]], float) * s
M = json.load(open(os.path.join(DATA, 'canh/ldn.json'))); c = np.array(M['old_st_pauls_EN'])
ax = np.array([0.98949186, 0.14458857]); vv = np.array([-ax[1], ax[0]])
dtm = np.load(os.path.join(DATA, 'lidar/dtm_kham_1m.npy')); g = float(dtm[int(182500 - c[1]), int(c[0] - 529500)])
def proj(r, u, v, y):
    e = c + ax * u + vv * v; X = np.array([e[0] - 532000, g + y, -(e[1] - 180800), 1.0])
    V = np.array(r['view']).reshape(4, 4).T; P = np.array(r['proj']).reshape(4, 4).T; q = P @ V @ X; q = q[:3] / q[3]
    return [(q[0] + 1) / 2 * W, (1 - q[1]) / 2 * H2]          # px khung cao; cắt H dòng trên → cùng toạ độ
k = H / (DH / s) * 1.0; S0 = np.array([[k / s, 0, (W - 2000 * k) / 2], [0, k / s, 0], [0, 0, 1]])   # tranh (px gốc) → khung, vừa chiều cao
src_pts = np.array([p for p, _ in FACE], float) * s
CORN = np.array([[0, 0], [DW, 0], [DW, DH], [0, DH]], np.float32)
def tf(Hm, pts): p = np.c_[pts, np.ones(len(pts))] @ Hm.T; return p[:, :2] / p[:, 2:]
def sm(x): x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)
mask = np.zeros((DH, DW), np.float32); cv2.fillPoly(mask, [POLY.astype(np.int32)], 1.0); mask = cv2.GaussianBlur(mask, (0, 0), 3 * s)
frames = sorted(LOG['frames'], key=lambda r: r['f']); log = {'uon_s': [u0, u1], 'hoa_s': [h0, h1], 'khung': [W, H2, H], 'diem_mat_dong': FACE}
for r in frames:
    f = r['f']; t = f / FPS; im3 = cv2.imread(os.path.join(IN, f'{f:05d}.jpg'))[:H, :, ::-1].astype(np.float32) / 255.0
    q3 = np.array([proj(r, *m) for _, m in FACE], np.float32)
    Hk, _ = cv2.findHomography(src_pts.astype(np.float32), q3, 0)
    if f == frames[0]['f']:
        e = np.hypot(*(tf(Hk, src_pts) - q3).T); log['homography_khop_khung0'] = Hk.tolist()
        log['sai_lech_mat_dong_sau_uon_px'] = [round(float(x), 1) for x in e]
        log['sai_lech_mat_dong_truoc_uon_px'] = [round(float(x), 1) for x in np.hypot(*(tf(S0, src_pts) - q3).T)]
        log['sai_lech_diem_khac_sau_uon_px'] = {n: round(float(np.hypot(*(tf(Hk, np.array([p], float) * s)[0] - proj(r, *m)))), 1) for n, (p, m) in KHAC.items()}
    if t < h1:
        w = sm((t - u0) / (u1 - u0)); cw = (1 - w) * tf(S0, CORN) + w * tf(Hk, CORN); Ht = cv2.getPerspectiveTransform(CORN, cw.astype(np.float32))
        pz = sm(t / max(u0, 1e-3)) * (1 - w)                        # thị sai chỉ trong đoạn tĩnh, tắt dần khi uốn
        cx, cy = W / 2, H / 2
        def Sk(kk): return np.array([[kk, 0, cx * (1 - kk)], [0, kk, cy * (1 - kk)], [0, 0, 1]])
        bg = cv2.warpPerspective(D, Sk(1 + 0.003 * pz) @ Ht, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=PAPER)
        fg = cv2.warpPerspective(D, Sk(1 + 0.012 * pz) @ Ht, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=PAPER)
        mk = cv2.warpPerspective(mask, Sk(1 + 0.012 * pz) @ Ht, (W, H), flags=cv2.INTER_LINEAR)[..., None]
        dr = bg * (1 - mk) + fg * mk; kk = sm((t - h0) / (h1 - h0)); out = dr * (1 - kk) + im3 * kk
    else:
        out = im3
    Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).save(os.path.join(OUT, f'{f:05d}.jpg'), quality=92)
json.dump(log, open(os.path.join(OUT, 't3.json'), 'w'), ensure_ascii=False, indent=1)
print(json.dumps({k_: log[k_] for k_ in ('sai_lech_mat_dong_truoc_uon_px', 'sai_lech_mat_dong_sau_uon_px', 'sai_lech_diem_khac_sau_uon_px')}, ensure_ascii=False))
