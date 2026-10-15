"""Căn góc máy 'then/now' TỪ ĐIỂM KHỐNG CHẾ: ảnh Rijksmuseum RP-F-00-568 (1886, CC0) ↔ chân móng Cung điện (BAG 0363100012167579, 3DBAG lod12).
Ẩn: vị trí máy (x, y; z cố định 1,7 m — mắt người), yaw/pitch/roll, tiêu cự f (px), độ cao đỉnh tường H, độ cao gờ mái giữa Hc,
độ cao đỉnh tam giác đầu hồi Hp, và vị trí t của 3 điểm trên cạnh nam. Điểm ảnh đo tay trên lưới 100 px (ảnh 1200×1114).
Ra: $TL_DATA/photo/pose.json (vị trí, điểm nhìn, fov dọc) + sai số chiếu lại."""
import json, numpy as np
from pathlib import Path
from scipy.optimize import least_squares
D = Path.home() / ".cache/cine-timelapse/photo"
W, Hh = 1200, 1114
SW, NW, NE = np.array([-136.0, -27.9]), np.array([-133.2, 52.3]), np.array([-75.8, 50.3])   # góc thật của vòng chân móng (không dùng hình chữ nhật bao)
# Đã sửa (lần 2): góc gần = TÂY-BẮC; mặt trái = mặt BẮC chạy về Nhà thờ Mới; mặt phải = mặt TÂY ("Achterzijde"),
# máy đứng trên Nieuwezijds Voorburgwal (kênh lấp 1884). Lần 1 nhận nhầm góc tây-nam → máy rơi vào khối nhà hiện đại.
OBS = [  # (mô tả, u, v, hàm 3D theo tham số)
    ("góc TB chân (gần)", 790, 700, lambda q: [*NW, 0]),
    ("góc ĐB chân (xa trái)", 272, 690, lambda q: [*NE, 0]),
    ("góc ĐB đỉnh tường", 272, 318, lambda q: [*NE, q["H"]]),
    ("gờ mặt tây gần", 800, 250, lambda q: [*(NW + q["t1"] * (SW - NW)), q["Hc"]]),
    ("gờ mặt tây xa", 1190, 298, lambda q: [*(NW + q["t2"] * (SW - NW)), q["Hc"]]),
    ("chân mặt tây xa", 1190, 705, lambda q: [*(NW + q["t2"] * (SW - NW)), 0]),
    ("đỉnh đầu hồi mặt bắc", 432, 95, lambda q: [*((NW + NE) / 2), q["Hp"]]),
]
NAMES = ["x", "y", "yaw", "pitch", "roll", "f", "H", "Hc", "Hp", "t1", "t2"]

def R(yaw, pitch, roll):   # hệ máy: x phải, y lên, z ra sau (như three.js); thế giới: E, N, U
    fwd = np.array([np.sin(yaw) * np.cos(pitch), np.cos(yaw) * np.cos(pitch), np.sin(pitch)])
    right = np.array([np.cos(yaw), -np.sin(yaw), 0.0])
    up = np.cross(right, fwd)
    c, s = np.cos(roll), np.sin(roll)
    return fwd, c * right + s * up, -s * right + c * up

def proj(p, q):
    fwd, right, up = R(q["yaw"], q["pitch"], q["roll"])
    d = np.array(p) - np.array([q["x"], q["y"], 1.7])
    z = d @ fwd
    return np.array([W / 2 + q["f"] * (d @ right) / z, Hh / 2 - q["f"] * (d @ up) / z])

def res(v):
    q = dict(zip(NAMES, v))
    r = []
    for _, u, w, fn in OBS:
        r += list(proj(fn(q), q) - [u, w])
    r += [(q["H"] - 26) * 0.5, (q["Hp"] - q["H"] - 9) * 0.3]     # tiền nghiệm mềm (mặt tường ~26 m, đầu hồi cao hơn ~9 m)
    return r

best = None
for x0 in (-260, -210, -170):
    for y0 in (90, 130, 170):
        v0 = [x0, y0, np.radians(120), np.radians(8), 0, 900, 26, 14, 35, 0.05, 0.6]
        s = least_squares(res, v0, bounds=([-450, 55, -3.2, -0.2, -0.2, 300, 15, 5, 20, 0, 0.1], [-138, 400, 3.2, 0.8, 0.2, 4000, 40, 30, 50, 0.4, 1]))
        if best is None or s.cost < best.cost: best = s
q = dict(zip(NAMES, best.x))
err = [float(np.hypot(*(proj(fn(q), q) - [u, w]))) for _, u, w, fn in OBS]
fwd, _, up = R(q["yaw"], q["pitch"], q["roll"])
cam = [q["x"], q["y"], 1.7]; look = list(np.array(cam) + 100 * fwd)
fov = float(np.degrees(2 * np.arctan(Hh / 2 / q["f"])))
out = dict(method="điểm khống chế (7 điểm đo tay) + bình phương tối thiểu, scipy least_squares", image="Rijksmuseum RP-F-00-568 (1886), CC0",
           cam_enu=cam, look_enu=look, up_enu=list(up), fov_v_deg=fov, aspect=W / Hh, params={k: float(v) for k, v in q.items()},
           reproj_px=dict(zip([o[0] for o in OBS], [round(e, 1) for e in err])), reproj_rms_px=float(np.sqrt(np.mean(np.square(err)))))
(D / "pose.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
print(json.dumps(out, ensure_ascii=False, indent=1))
