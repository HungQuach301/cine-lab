#!/opt/cine/bin/python
"""TIEN-KY-T4 · NƯỚNG SẴN lửa/khói THỂ TÍCH → atlas flipbook cho cách A (bản thử T1 (i)).
  nuong_flipbook.py <ra_thư_mục> [nx=40] [nz=96] [khung=64] [o_px=128]
Mô phỏng khí 3D tối giản bằng numpy (trường vận tốc curl-noise không phân kỳ + nổi do nhiệt + gió ngang; đối lưu bán-Lagrange cho mật độ khói,
nhiên liệu và nhiệt; nguồn = khối nhà gỗ đang cháy ở đáy), rồi DỰNG bằng dò tia phát xạ–hấp thụ (nhìn ngang, trực giao) + tán xạ đơn từ nắng.
  lua.png  : atlas 8×8 lửa phát xạ (RGB tuyến tính → sRGB, nền đen; cộng dồn trong three.js)
  khoi.png : atlas 8×8 khói (R = alpha, G = phần được nắng chiếu, B = phần sáng do lửa bên dưới)
(Mantaflow trong bpy 5.2.2 lỗi 'LevelsetGrid.setConst' 2/2 lần → đổi cách theo luật "cùng lỗi ≥ 3 → đổi"; xem báo cáo §sự cố.) Tất định (seed 1666)."""
import sys, os, json, time
import numpy as np
from scipy.ndimage import map_coordinates, gaussian_filter
from PIL import Image
a = sys.argv[1:]; OUT = os.path.abspath(a[0]); NX = int(a[1]) if len(a) > 1 else 40; NZ = int(a[2]) if len(a) > 2 else 96
NF = int(a[3]) if len(a) > 3 else 64; PX = int(a[4]) if len(a) > 4 else 128
os.makedirs(OUT, exist_ok=True); T0 = time.time(); rng = np.random.default_rng(1666)
NY = NX
def noise3(shape, s):
    return gaussian_filter(rng.standard_normal(shape), s, mode='wrap')
# trường thế ngẫu nhiên → curl (3 thành phần), 2 tầng tỷ lệ, trôi theo thời gian bằng nội suy giữa 2 trường
P = [np.stack([noise3((NZ, NY, NX), sc) for _ in range(3)]) for sc in (3.0, 6.0) for _ in range(2)]
def curl(psi):
    dz, dy, dx = np.gradient(psi[0]), np.gradient(psi[1]), np.gradient(psi[2])
    # psi = (A_z, A_y, A_x) theo trục (z, y, x)
    Az, Ay, Ax = psi[0], psi[1], psi[2]
    vx = np.gradient(Az, axis=1) - np.gradient(Ay, axis=0)
    vy = np.gradient(Ax, axis=0) - np.gradient(Az, axis=2)
    vz = np.gradient(Ay, axis=2) - np.gradient(Ax, axis=1)
    return vz, vy, vx
Cs = [curl(p) for p in P]
for c in Cs:
    m = max(np.abs(x).max() for x in c)
    for x in c: x /= m
Z, Y, X = np.meshgrid(np.arange(NZ), np.arange(NY), np.arange(NX), indexing='ij')
rho = np.zeros((NZ, NY, NX)); fuel = np.zeros_like(rho); T = np.zeros_like(rho)
src = ((Z < 6) & (np.abs(X - NX / 2) < NX * 0.22) & (np.abs(Y - NY / 2) < NY * 0.22))
dt = 1.0
frames_f, frames_s = [], []
def step(k):
    global rho, fuel, T
    w = 0.5 + 0.5 * np.sin(k * 0.05)
    turb = 1.6 + 0.8 * (Z / NZ)
    vz = 0.7 + 1.6 * T + turb * (w * Cs[0][0] + (1 - w) * Cs[1][0]) * 1.2 + 0.7 * (Cs[2][0] * np.cos(k * 0.03) + Cs[3][0] * np.sin(k * 0.03))
    vy = turb * (w * Cs[0][1] + (1 - w) * Cs[1][1]) * 1.2
    vx = 0.35 * (Z / NZ) * 2.0 + turb * (w * Cs[0][2] + (1 - w) * Cs[1][2]) * 1.2      # gió ngang tăng theo độ cao
    coords = [np.clip(Z - vz * dt, 0, NZ - 1), np.clip(Y - vy * dt, 0, NY - 1), np.clip(X - vx * dt, 0, NX - 1)]
    rho = map_coordinates(rho, coords, order=1, mode='nearest'); fuel = map_coordinates(fuel, coords, order=1, mode='nearest'); T = map_coordinates(T, coords, order=1, mode='nearest')
    flick = 0.75 + 0.25 * rng.random()
    fuel[src] = np.maximum(fuel[src], flick * (0.6 + 0.4 * rng.random(src.sum())))
    burn = np.minimum(fuel, 0.22 * fuel + 0.02)
    fuel -= burn; T += 2.6 * burn; rho += 0.16 * burn
    T *= 0.84; rho *= 0.985
    for g in (rho, T, fuel): g[-3:] = 0; g[:, :2] = 0; g[:, -2:] = 0; g[:, :, :2] = 0; g[:, :, -2:] = 0   # thoát ở biên
def render():
    s_ext = 0.30
    tau = np.cumsum(rho * s_ext, axis=1)                         # nhìn dọc trục y
    trans = np.exp(-tau)
    flame = np.clip((T - 0.45) * 1.3, 0, None)
    # màu vật đen gần đúng theo nhiệt (đỏ → cam → vàng)
    temp = np.clip(T / 1.6, 0, 1)
    col = np.stack([np.ones_like(temp), 0.18 + 0.62 * temp ** 1.3, 0.02 + 0.30 * temp ** 3], -1)
    E = (flame[..., None] * col * trans[..., None]).sum(axis=1) * 0.16
    alpha = 1 - trans[:, -1, :]
    # tán xạ đơn: nắng từ trên-bên (che theo cột z ngược) + sáng lửa từ dưới
    tl = np.exp(-np.cumsum((rho * s_ext)[::-1], axis=0)[::-1])
    lit = (rho * tl * trans).sum(axis=1) / np.maximum((rho * trans).sum(axis=1), 1e-6)
    fb = gaussian_filter(T, 3)
    fire_lit = (rho * fb * trans).sum(axis=1) / np.maximum((rho * trans).sum(axis=1), 1e-6)
    return E[::-1], alpha[::-1], lit[::-1], fire_lit[::-1]
for k in range(40): step(k)
for f in range(NF):
    step(40 + 3 * f); step(41 + 3 * f); step(42 + 3 * f)
    E, al, li, fl = render()
    frames_f.append(E); frames_s.append(np.stack([al, li, np.clip(fl, 0, 1)], -1))
def atlas(frames, name, kind):
    H, W = frames[0].shape[:2]; tw, th = PX // 2, PX
    A = np.zeros((8 * th, 8 * tw, 3), np.float32)
    for i, fr in enumerate(frames[:64]):
        im = Image.fromarray(np.clip(fr * 255 if kind == 's' else (np.clip(fr, 0, 1) ** (1 / 2.2)) * 255, 0, 255).astype(np.uint8)).resize((tw, th), Image.BICUBIC)
        r, c = divmod(i, 8); A[r * th:(r + 1) * th, c * tw:(c + 1) * tw] = np.asarray(im)
    Image.fromarray(A.astype(np.uint8)).save(os.path.join(OUT, name), optimize=True)
atlas(frames_f, 'lua.png', 'f'); atlas(frames_s, 'khoi.png', 's')
res = {'luoi': [NX, NY, NZ], 'khung': NF, 'o_px': [PX // 2, PX], 'giay': round(time.time() - T0, 1), 'luu_y': 'mô phỏng numpy (curl-noise + nổi nhiệt) — không phải CFD đầy đủ'}
json.dump(res, open(os.path.join(OUT, 'nuong.json'), 'w'), indent=1); print('NUONG', json.dumps(res, ensure_ascii=False))
