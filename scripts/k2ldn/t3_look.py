#!/opt/cine/bin/python
"""LOOK-T4 · VIỆC 5 (D7) — làm lại bản thử T3 tranh khắc với OLD ST PAUL'S MỚI (hinh_hoc_look.py, theo Hollar/Dugdale 1658):
  t3_look.py may <ra shot.json> <ra do.json> [--W 1280 --H 720 --dur 8]     giải máy 3D trùng góc bản vẽ Hollar "Old St Paul's seen from the East" (Met 2010.529, CC0)
  t3_look.py khac <thư mục khung 3D (render_look.js)> <ra> [--H 720]           đăng ký điểm + thị sai 2,5D thủ công + hoà mờ (không AI)
Cùng thuật toán bản tiền kỳ (t3_may.py, t3_khac.py — không sửa), chỉ đổi: (a) mô hình Old St Paul's mới → toạ độ điểm mô hình theo kích thước mới
(mặt đông u = 86 m, gian bên v ±6,5…15,5 m cao 19 m, tường thân 31 m, đỉnh hồi 39,3 m, tháp giao điểm u = 0 tới 60 m, cánh ngang v ±44 m; v + = bắc);
(b) trục + tâm lấy từ ldn2.json; (c) dựng bằng look.js (1/9/1666 J. 9:00 sáng, nắng từ phía đông như tranh)."""
import json, os, sys
import numpy as np
DATA = os.environ.get('LDN_DATA', '/var/tmp/ldn'); SRC = os.environ.get('LDN_SRC', '/var/tmp/ldn/tu-lieu')
def arg(k, d): return type(d)(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
DW, DH = 2000.0, 1554.0                                                  # toạ độ đọc tay theo bản xem 2000 px
# (tên, điểm tranh px bản 2000, điểm mô hình u, v, y) — cùng điểm tranh như tiền kỳ, điểm mô hình theo Old St Paul's mới
PTS = [('chân góc đông-nam gian bên nam', (1000, 1500), (86.0, -15.5, 0.0)),
       ('chân góc đông-bắc gian bên bắc', (1714, 1500), (86.0, 15.5, 0.0)),
       ('đỉnh tường gian bên nam (mép thân giữa)', (1186, 1000), (86.0, -6.5, 19.0)),
       ('đỉnh tường gian bên bắc (mép thân giữa)', (1457, 1000), (86.0, 6.5, 19.0)),
       ('chân hồi mặt đông trái', (1214, 671), (86.0, -6.5, 31.0)),
       ('chân hồi mặt đông phải', (1429, 671), (86.0, 6.5, 31.0)),
       ('đỉnh hồi mặt đông', (1293, 393), (86.0, 0.0, 39.3)),
       ('tâm đỉnh tháp giao điểm', (971, 64), (0.0, 0.0, 60.0)),
       ('chân góc đông-nam cánh ngang nam', (64, 1264), (12.0, -44.0, 0.0))]
FACE = [(p, m) for _, p, m in PTS[:7]]
KHAC = {'tam_cua_so_hoa_hong': ((1314, 871), (86.1, 0.0, 20.15)), 'tam_dinh_thap': ((971, 64), (0.0, 0.0, 60.0)), 'chan_canh_ngang_nam': ((64, 1264), (12.0, -44.0, 0.0))}
M = json.load(open(os.path.join(DATA, 'look/ldn2.json'))); c = np.array(M['old_st_pauls_EN']); ax = np.array(M['old_st_pauls_truc']); vv = np.array([-ax[1], ax[0]])
dtm = np.load(os.path.join(DATA, 'lidar/dtm_kham_1m.npy')); g = float(np.clip(dtm[int(182500 - c[1]), int(c[0] - 529500)], 0.5, 40.0))

def may():
    from scipy.optimize import least_squares
    W, H, DUR = arg('--W', 1280), arg('--H', 720), arg('--dur', 8.0)
    X = np.array([[*(c + ax * u + vv * v), g + y] for _, _, (u, v, y) in PTS]); x2 = np.array([p for _, p, _ in PTS], float); CX = DW / 2
    def project(q, X):
        E, N, h, yaw, f, cy = q; d = np.array([np.cos(yaw), np.sin(yaw)]); r = np.array([d[1], -d[0]])
        rel = X[:, :2] - [E, N]; zc = rel @ d; xc = rel @ r; yc = X[:, 2] - h
        return np.stack([CX + f * xc / zc, cy - f * yc / zc], 1)
    def res(q): return (project(q, X) - x2).ravel()
    best = None
    for dist in (60, 90, 130, 180):
        for off in (-30, -10, 10):
            for hh in (10, 25, 40):
                p0 = c + ax * (86 + dist) + vv * off; yaw0 = np.arctan2(*(-ax)[::-1])
                try: s = least_squares(res, [p0[0], p0[1], g + hh, yaw0, 1500.0, 800.0], loss='soft_l1', f_scale=20.0, max_nfev=4000)
                except Exception: continue
                if s.x[4] > 100 and (best is None or s.cost < best.cost): best = s
    q = best.x; e = project(q, X) - x2; err = np.hypot(e[:, 0], e[:, 1])
    E, N, h, yaw, f, cy = q; d = np.array([np.cos(yaw), np.sin(yaw)])
    k = H / DH; fpx = f * k; ppy = cy * k
    dy = ppy - H / 2; H2 = int(round(H + 2 * dy)) // 2 * 2; fov = float(np.degrees(2 * np.arctan(H2 / 2 / fpx)))   # dịch ống kính dọc = khung cao H2 rồi cắt H dòng trên
    L = [E + d[0] * 200, N + d[1] * 200, h]; P0 = [E, N, h]; P1 = [E - d[0] * 6, N - d[1] * 6, h]
    key = lambda t, p, hr: {'t': t, 'p': p, 'l': L, 'fov': fov, 'year': 1666.62, 'date': [1666, 9, 11, hr], 'tz': -0.0065, 'leaf': 1}
    shot = {'fps': 24, 'dur': DUR, 'spp': 4, 'W': W, 'H': H2, 'cat_H': [W, H2, H], 'keys': [key(0, P0, 9.0), key(5.0, P0, 9.05), key(DUR, P1, 9.1)],
            'look': {'haze': [1 / 16000, 0.66, 0.74, 0.84], 'hazeH': 700, 'sunK': 3.0, 'hemiK': 0.62, 'cloud': 0.3, 'exposure': 0.95, 'chim': 0.3},
            'bake': {'url': '/data/look/bake_1666.6.png', 'box': [530800, 179700, 534000, 182000]}}
    json.dump(shot, open(sys.argv[2], 'w'), indent=1)
    do = {'mo_hinh_may': 'trục nhìn ngang + dịch ống kính (phối cảnh kiến trúc của bản vẽ)', 'mo_hinh_old_st_pauls': 'look-v2 (Hollar/Dugdale 1658)', 'may_EN_h': [round(E, 1), round(N, 1), round(h - g, 1)],
          'khoang_cach_toi_mat_dong_m': round(float(np.linalg.norm(c + ax * 86 - [E, N])), 1), 'yaw_do_tu_dong': round(float(np.degrees(yaw)), 2), 'f_px_ban2000': round(f, 1),
          'fov_doc_khung_cao': round(fov, 2), 'khung_dung_W_H2_cat_H': [W, H2, H], 'sai_lech_px_ban2000': {n: round(float(v), 1) for (n, _, _), v in zip(PTS, err)},
          'rms_px_ban2000': round(float(np.sqrt((err ** 2).mean())), 1), 'trung_vi_px_ban2000': round(float(np.median(err)), 1), 'px_khung_tren_px_ban2000': round(k, 4)}
    json.dump(do, open(sys.argv[3], 'w'), ensure_ascii=False, indent=1); print(json.dumps(do, ensure_ascii=False))

def khac():
    import cv2
    from PIL import Image
    IN, OUT = sys.argv[2], sys.argv[3]; os.makedirs(OUT, exist_ok=True)
    def rng(k, d): return [float(x) for x in (sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d).split(':')]
    u0, u1 = rng('--uon', '1.5:3.0'); h0, h1 = rng('--hoa', '3.0:5.0')
    LOG = json.load(open(os.path.join(IN, 'log.json'))); W, H2 = LOG['W'], LOG['H']; FPS = LOG['shot'].get('fps', 24); H = arg('--H', int(round(W * 9 / 16)))
    D = cv2.imread(os.path.join(SRC, 'met-395057-0.jpg'))[:, :, ::-1].astype(np.float32) / 255.0; dh, dw = D.shape[:2]; s = dw / 2000.0
    PAPER = (0.86, 0.80, 0.68)
    POLY = np.array([[60, 1500], [60, 520], [180, 470], [640, 470], [700, 380], [760, 60], [1110, 60], [1150, 380], [1280, 380], [1460, 470], [1760, 470], [1880, 560], [1880, 1500]], float) * s
    def proj(r, u, v, y):
        e = c + ax * u + vv * v; Xh = np.array([e[0] - 532000, g + y, -(e[1] - 180800), 1.0])
        V = np.array(r['view']).reshape(4, 4).T; P = np.array(r['proj']).reshape(4, 4).T; q = P @ V @ Xh; q = q[:3] / q[3]
        return [(q[0] + 1) / 2 * W, (1 - q[1]) / 2 * H2]
    k = H / (dh / s); S0 = np.array([[k / s, 0, (W - 2000 * k) / 2], [0, k / s, 0], [0, 0, 1]])
    src_pts = np.array([p for p, _ in FACE], float) * s; CORN = np.array([[0, 0], [dw, 0], [dw, dh], [0, dh]], np.float32)
    def tf(Hm, pts): p = np.c_[pts, np.ones(len(pts))] @ Hm.T; return p[:, :2] / p[:, 2:]
    def sm(x): x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)
    mask = np.zeros((dh, dw), np.float32); cv2.fillPoly(mask, [POLY.astype(np.int32)], 1.0); mask = cv2.GaussianBlur(mask, (0, 0), 3 * s)
    frames = sorted(LOG['frames'], key=lambda r: r['f']); log = {'uon_s': [u0, u1], 'hoa_s': [h0, h1], 'khung': [W, H2, H], 'diem_mat_dong': FACE}
    for r in frames:
        f = r['f']; t = f / FPS; im3 = cv2.imread(os.path.join(IN, f'{f:05d}.jpg'))[:H, :, ::-1].astype(np.float32) / 255.0
        q3 = np.array([proj(r, *m) for _, m in FACE], np.float32)
        xm, ym = src_pts.mean(0), q3.mean(0); sc = float(((src_pts - xm) * (q3 - ym)).sum() / ((src_pts - xm) ** 2).sum())
        Hk = np.array([[sc, 0, ym[0] - sc * xm[0]], [0, sc, ym[1] - sc * xm[1]], [0, 0, 1]])
        if f == frames[0]['f']:
            log['sai_lech_mat_dong_sau_uon_px'] = [round(float(x), 1) for x in np.hypot(*(tf(Hk, src_pts) - q3).T)]
            log['sai_lech_mat_dong_truoc_uon_px'] = [round(float(x), 1) for x in np.hypot(*(tf(S0, src_pts) - q3).T)]
            log['sai_lech_diem_khac_sau_uon_px'] = {n: round(float(np.hypot(*(tf(Hk, np.array([p], float) * s)[0] - proj(r, *m)))), 1) for n, (p, m) in KHAC.items()}
        if t < h1:
            w = sm((t - u0) / (u1 - u0)); cw = (1 - w) * tf(S0, CORN) + w * tf(Hk, CORN); Ht = cv2.getPerspectiveTransform(CORN, cw.astype(np.float32))
            pz = sm(t / max(u0, 1e-3)) * (1 - w); cx, cy = W / 2, H / 2
            def Sk(kk): return np.array([[kk, 0, cx * (1 - kk)], [0, kk, cy * (1 - kk)], [0, 0, 1]])
            bg = cv2.warpPerspective(D, Sk(1 + 0.003 * pz) @ Ht, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=PAPER)
            fg = cv2.warpPerspective(D, Sk(1 + 0.012 * pz) @ Ht, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=PAPER)
            mk = cv2.warpPerspective(mask, Sk(1 + 0.012 * pz) @ Ht, (W, H), flags=cv2.INTER_LINEAR)[..., None]
            dr = bg * (1 - mk) + fg * mk; kk = sm((t - h0) / (h1 - h0)); out = dr * (1 - kk) + im3 * kk
        else: out = im3
        Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).save(os.path.join(OUT, f'{f:05d}.jpg'), quality=92)
    json.dump(log, open(os.path.join(OUT, 't3.json'), 'w'), ensure_ascii=False, indent=1)
    print(json.dumps({k_: log[k_] for k_ in ('sai_lech_mat_dong_truoc_uon_px', 'sai_lech_mat_dong_sau_uon_px', 'sai_lech_diem_khac_sau_uon_px')}, ensure_ascii=False))

if __name__ == '__main__':
    may() if sys.argv[1] == 'may' else khac()
