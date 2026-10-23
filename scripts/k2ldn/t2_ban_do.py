#!/opt/cine/bin/python
"""TIEN-KY-T4 · BẢN THỬ T2 — bản đồ cổ hoạt hoá: Doornick 1666 (Rijks RP-P-OB-82.345, PDM) làm nền, vùng cháy lan theo ngày 2→6/9 trên chính bản đồ,
máy đẩy nhẹ, rồi chuyển mượt sang 3D CÙNG TOẠ ĐỘ (bản đồ được chiếu vào đúng máy 3D bằng ma trận máy từng khung + TPS 13 điểm khớp).
  t2_ban_do.py <thư mục khung 3D (render_ldn.js, có log.json)> <ra thư mục> [--map-end 6.0] [--fade 1.5]
Hoạt hoá CHỈ theo dữ kiện có nguồn: giờ bén lửa = lưới luoi_chay (tên nơi theo ngày bậc 2 × vị trí bậc 1; nội suy bậc 5 = "ước lượng", ghi trong log).
Không AI chạm vào bản đồ: chỉ lấy mẫu điểm ảnh (nội suy song tuyến) + phủ màu lửa (nhân) + nét viền ranh. Chữ: bộ đếm ngày + ≤ 3 tên nơi."""
import json, os, sys, math
import numpy as np, cv2
from scipy.interpolate import RBFInterpolator
from PIL import Image, ImageDraw, ImageFont
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.environ.get('LDN_DATA', '/var/tmp/ldn'); SRC = os.environ.get('LDN_SRC', '/var/tmp/ldn/tu-lieu')
IN, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
arg = lambda k, d: float(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
MAP_END, FADE = arg('--map-end', 6.0), arg('--fade', 1.5)
LOG = json.load(open(os.path.join(IN, 'log.json'))); W, H = LOG['W'], LOG['H']; FPS = LOG['shot'].get('fps', 24)
K = json.load(open(os.path.join(REPO, 'channel-k2/k2c-t4-02/du-lieu/khop-doornick.json'))); KD = [d for d in K['diem'] if d.get('dung', True)]
TPSi = RBFInterpolator(np.array([d['en'] for d in KD], float), np.array([d['px'] for d in KD], float), kernel='thin_plate_spline')
MAPIM = cv2.imread(os.path.join(SRC, 'rijks-doornick-0.jpg'))[:, :, ::-1].astype(np.float32) / 255.0
M = json.load(open(os.path.join(DATA, 'canh/ldn.json'))); LC = M['luoi_chay']
TG = np.fromfile(os.path.join(DATA, 'canh/luoi_chay.f32'), '<f4').reshape(LC['nz'], LC['nx'])
FONT = None
for f in ('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf'):
    if os.path.exists(f): FONT = f; break
def ground_EN(view, proj, gy=12.0, step=4):
    """mỗi điểm ảnh (lưới thưa step px) → giao tia máy với mặt y = gy → (E, N)."""
    V = np.array(view).reshape(4, 4).T; P = np.array(proj).reshape(4, 4).T; inv = np.linalg.inv(P @ V)
    xs, ys = np.meshgrid(np.arange(0, W + step, step), np.arange(0, H + step, step))
    ndc = np.stack([xs / W * 2 - 1, 1 - ys / H * 2], -1)
    def unp(z):
        q = np.concatenate([ndc, np.full(ndc.shape[:2] + (1,), z), np.ones(ndc.shape[:2] + (1,))], -1) @ inv.T; return q[..., :3] / q[..., 3:]
    a, b = unp(-1.0), unp(1.0); d = b - a; t = (gy - a[..., 1]) / np.where(np.abs(d[..., 1]) < 1e-9, 1e-9, d[..., 1])
    p = a + d * t[..., None]; E = p[..., 0] + 532000; N = 180800 - p[..., 2]
    return E, N, t > 0
def bilinear(grid, gx, gy):
    return cv2.remap(grid.astype(np.float32), gx.astype(np.float32), gy.astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=1e6)
def hour_of(t, t_map):   # đồng hồ bản đồ: 0 → 100 giờ trong t_map giây (2/9 00:00 → 6/9 04:00), chậm ở đầu cho kịp đọc
    u = min(1.0, max(0.0, t / t_map)); return 100.0 * (u ** 1.15)
DAYS = [(0, 'SUN 2 SEPT 1666'), (24, 'MON 3 SEPT'), (48, 'TUE 4 SEPT'), (72, 'WED 5 SEPT'), (96, 'THU 6 SEPT')]
LABELS = [('Pudding Lane', 532955, 180762), ("St Paul's", 532060, 181180), ('Temple', 531200, 181030)]
def text(img, s, xy, size, fill=(240, 232, 214), stroke=(30, 22, 16)):
    d = ImageDraw.Draw(img); f = ImageFont.truetype(FONT, size) if FONT else None
    d.text(xy, s, font=f, fill=fill, stroke_width=max(1, size // 14), stroke_fill=stroke)
frames = sorted(LOG['frames'], key=lambda r: r['f']); meta = {'map_end_s': MAP_END, 'fade_s': FADE, 'khung': len(frames), 'nguon_ban_do': K['ban_do'], 'bac_ranh_ngay': '2 (tên nơi theo ngày, LUAT-N2P a01–a17) × 1 (vị trí); nội suy = 5 ước lượng', 'rms_khop_m': K['ket_qua']['affine']['rms_m']}
for r in frames:
    f = r['f']; t = f / FPS; im3 = cv2.imread(os.path.join(IN, f'{f:05d}.jpg'))[:, :, ::-1].astype(np.float32) / 255.0
    if t >= MAP_END + FADE:
        out = im3
    else:
        E, N, ok = ground_EN(r['view'], r['proj'])
        px = TPSi(np.stack([E.ravel(), N.ravel()], 1)).reshape(E.shape + (2,))
        mx = cv2.resize(px[..., 0].astype(np.float32), (W, H), interpolation=cv2.INTER_LINEAR); my = cv2.resize(px[..., 1].astype(np.float32), (W, H), interpolation=cv2.INTER_LINEAR)
        mp = cv2.remap(MAPIM, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0.93, 0.90, 0.82))
        # giờ bén lửa tại mỗi điểm ảnh
        gxs = (cv2.resize(E.astype(np.float32), (W, H)) - LC['E0']) / LC['buoc']; gys = (LC['N0'] - cv2.resize(N.astype(np.float32), (W, H))) / LC['buoc']
        ign = bilinear(np.where(TG < 0, 1e6, TG), gxs, gys)
        h = hour_of(t, MAP_END)
        burnt = np.clip((h - ign) / 2.5, 0, 1); burnt[ign > 5e5] = 0
        front = np.clip(1 - np.abs(h - ign) / 2.0, 0, 1) * (ign < 5e5)
        tint = np.array([0.86, 0.36, 0.14], np.float32)
        mp2 = mp * (1 - 0.55 * burnt[..., None]) + mp * tint * 0.55 * burnt[..., None]          # nhân màu: nét khắc gốc vẫn đọc được
        mp2 = np.clip(mp2 + front[..., None] * np.array([1.0, 0.55, 0.15]) * 0.65, 0, 1)
        k = 0.0 if t < MAP_END else min(1.0, (t - MAP_END) / FADE); k = k * k * (3 - 2 * k)
        out = mp2 * (1 - k) + im3 * k
        img = Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8))
        if k < 0.6:
            day = [s for hh, s in DAYS if h >= hh][-1]; sz = max(14, H // 22)
            text(img, day, (int(W * 0.04), int(H * 0.88)), sz)
            V = np.array(r['view']).reshape(4, 4).T; P = np.array(r['proj']).reshape(4, 4).T
            for nm, e, nn in LABELS[:3]:
                q = P @ V @ np.array([e - 532000, 15.0, -(nn - 180800), 1.0]); q = q[:3] / q[3]
                x, y = (q[0] + 1) / 2 * W, (1 - q[1]) / 2 * H
                if 0 < x < W * 0.95 and 0 < y < H * 0.95: text(img, nm, (int(x) + 6, int(y) - sz // 2), int(sz * 0.8))
        out = np.asarray(img).astype(np.float32) / 255.0
    Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).save(os.path.join(OUT, f'{f:05d}.jpg'), quality=92)
json.dump(meta, open(os.path.join(OUT, 't2.json'), 'w'), ensure_ascii=False, indent=1); print(json.dumps(meta, ensure_ascii=False))
