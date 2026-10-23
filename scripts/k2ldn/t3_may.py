#!/opt/cine/bin/python
"""TIEN-KY-T4 · BẢN THỬ T3 — giải máy 3D trùng góc bản vẽ Hollar "Old St Paul's seen from the East" (Met 2010.529).
Bản vẽ dùng phối cảnh kiến trúc (đường đứng song song) → mô hình máy: trục nhìn NẰM NGANG (pitch = 0, roll = 0) + dịch ống kính (tâm ảnh lệch).
Ẩn: E, N, h, hướng (yaw), tiêu cự f, tâm ảnh dọc cy — 6 ẩn (cx giữ ở giữa tranh: dịch ngang làm bài toán suy biến); 9 điểm đọc tay (toạ độ bản xem 2000 px) ↔ điểm mô hình (u, v, y) trục Old St Paul's
(hinh_hoc.py; v + = bắc). Bình phương tối thiểu (scipy least_squares, mất mát soft_l1) → ghi sai lệch từng điểm (px trên bản 2000 px) và shot.json
cho render_ldn.js (fov dọc + dịch ống kính sx, sy theo khung 16:9 khi bản vẽ đặt vừa chiều cao).
  t3_may.py <ra shot.json> <ra do.json> [--W 1280 --H 720 --dur 8]"""
import json, os, sys
import numpy as np
from scipy.optimize import least_squares
DATA = os.environ.get('LDN_DATA', '/var/tmp/ldn')
def arg(k, d): return type(d)(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
W, H, DUR = arg('--W', 1280), arg('--H', 720), arg('--dur', 8.0)
DW, DH = 2000.0, 1554.0
# (tên, điểm tranh px bản 2000, điểm mô hình u, v, y)
PTS = [('chân góc đông-nam gian bên nam', (1000, 1500), (88.0, -16.0, 0.0)),
       ('chân góc đông-bắc gian bên bắc', (1714, 1500), (88.0, 16.0, 0.0)),
       ('đỉnh tường gian bên nam (mép thân giữa)', (1186, 1000), (88.0, -7.0, 15.0)),
       ('đỉnh tường gian bên bắc (mép thân giữa)', (1457, 1000), (88.0, 7.0, 15.0)),
       ('chân hồi mặt đông trái', (1214, 671), (88.0, -7.0, 28.0)),
       ('chân hồi mặt đông phải', (1429, 671), (88.0, 7.0, 28.0)),
       ('đỉnh hồi mặt đông', (1293, 393), (88.0, 0.0, 40.0)),
       ('tâm đỉnh tháp giao điểm', (971, 64), (10.0, 0.0, 87.0)),
       ('chân góc đông-nam cánh ngang nam', (64, 1264), (19.0, -44.0, 0.0))]
M = json.load(open(os.path.join(DATA, 'canh/ldn.json'))); c = np.array(M['old_st_pauls_EN'])
ax = np.array([0.98949186, 0.14458857]); vv = np.array([-ax[1], ax[0]])
dtm = np.load(os.path.join(DATA, 'lidar/dtm_kham_1m.npy')); g = float(dtm[int(182500 - c[1]), int(c[0] - 529500)])
X = np.array([[*(c + ax * u + vv * v), g + y] for _, _, (u, v, y) in PTS])          # E, N, cao độ tuyệt đối
x2 = np.array([p for _, p, _ in PTS], float)
CX = DW / 2
def project(q, X):
    E, N, h, yaw, f, cy = q; cx = CX; d = np.array([np.cos(yaw), np.sin(yaw)]); r = np.array([d[1], -d[0]])   # d: hướng nhìn (EN), r: phải
    rel = X[:, :2] - [E, N]; zc = rel @ d; xc = rel @ r; yc = X[:, 2] - h
    return np.stack([cx + f * xc / zc, cy - f * yc / zc], 1)
def res(q): return (project(q, X) - x2).ravel()
best = None
for dist in (60, 90, 130, 180):                    # nhiều điểm khởi đầu: máy phía đông, hơi chếch nam
    for off in (-30, -10, 10):
        for hh in (10, 25, 40):
            p0 = c + ax * (88 + dist) + vv * off; yaw0 = np.arctan2(*(-ax)[::-1])
            q0 = [p0[0], p0[1], g + hh, yaw0, 1500.0, 800.0]
            try: s = least_squares(res, q0, loss='soft_l1', f_scale=20.0, max_nfev=4000)
            except Exception: continue
            if s.x[4] > 100 and (best is None or s.cost < best.cost): best = s
q = best.x; e = project(q, X) - x2; err = np.hypot(e[:, 0], e[:, 1])
E, N, h, yaw, f, cy = q; cx = CX; d = np.array([np.cos(yaw), np.sin(yaw)])
k = H / DH; ox = (W - DW * k) / 2; fpx = f * k; ppx, ppy = cx * k + ox, cy * k
# dịch ống kính dọc = dựng khung CAO hơn (H2) với tâm ảnh ở giữa rồi cắt H dòng trên cùng (post.js đặt lại ma trận chiếu khi khử răng cưa → không chỉnh ma trận được)
dy = ppy - H / 2; H2 = int(round(H + 2 * dy)) // 2 * 2; fov = float(np.degrees(2 * np.arctan(H2 / 2 / fpx))); sx, sy = 0.0, round(-dy / (H / 2), 4)
L = [E + d[0] * 200, N + d[1] * 200, h]
# máy: giữ nguyên góc tranh đến hết hoà mờ (5 s), rồi đẩy vào chậm 6 m (§19: ≤ 1,5 %/s khung); dựng W × H2, cắt H dòng trên
P0 = [E, N, h]; P1 = [E - d[0] * 6, N - d[1] * 6, h]
shot = {'fps': 24, 'dur': DUR, 'spp': 4, 'keys': [
    {'t': 0, 'p': P0, 'l': L, 'fov': fov, 'year': 1666.62, 'hod': 9.0},
    {'t': 5.0, 'p': P0, 'l': L, 'fov': fov, 'year': 1666.62, 'hod': 9.1},
    {'t': DUR, 'p': P1, 'l': L, 'fov': fov, 'year': 1666.62, 'hod': 9.2}], 'cat_H': [W, H2, H]}
json.dump(shot, open(sys.argv[1], 'w'), indent=1)
do = {'mo_hinh_may': 'trục nhìn ngang + dịch ống kính (phối cảnh kiến trúc của bản vẽ)', 'may_EN_h': [round(E, 1), round(N, 1), round(h - g, 1)], 'cao_do_nen_m': round(g, 2),
      'khoang_cach_toi_mat_dong_m': round(float(np.linalg.norm(c + ax * 88 - [E, N])), 1), 'yaw_do_tu_dong': round(float(np.degrees(yaw)), 2),
      'f_px_ban2000': round(f, 1), 'tam_anh_ban2000': [round(cx, 1), round(cy, 1)], 'fov_doc_khung_cao': round(fov, 2), 'khung_dung_W_H2_cat_H': [W, H2, H], 'dich_ong_kinh_tuong_duong_sy': sy,
      'sai_lech_px_ban2000': {n: round(float(v), 1) for (n, _, _), v in zip(PTS, err)}, 'rms_px_ban2000': round(float(np.sqrt((err ** 2).mean())), 1),
      'trung_vi_px_ban2000': round(float(np.median(err)), 1), 'px_khung_tren_px_ban2000': round(k, 4)}
json.dump(do, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1); print(json.dumps(do, ensure_ascii=False))
