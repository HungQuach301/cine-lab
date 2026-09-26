"""H1 — không chuyển động tuyến tính ở bộ phận nhân vật, đo từ dữ liệu chuyển động bake.

Định dạng <video>.motion.json:
  {"fps": 24, "channels": [
     {"id": "hero/forearm_L.rot", "class": "character_part", "first_frame": 0,
      "values": [[x, y, z], ...]  # một giá trị (số hoặc vectơ) mỗi khung, bake từ phần mềm dựng
     },
     {"id": "clock/hand.rot", "class": "mechanical", "reason": "kim đồng hồ quay đều có chủ ý", ...}]}
Lớp: character_part (bị kiểm), character_root, mechanical, camera, prop (miễn H1; camera thuộc F3).
"""
import json

import numpy as np

from .common import FAIL, metric, result

MIN_RUN = 8        # số bước tốc độ liên tiếp tối thiểu (1/3 giây ở 24 fps)
REL_TOL = 0.03     # ±3% quanh tốc độ trung bình của chuỗi
LONG_RUN = 24      # tốc độ không đổi suốt 1 giây thì tính là tuyến tính dù có easing hai đầu
MOVING = 0.02      # đang chuyển động khi tốc độ > 2% tốc độ lớn nhất của kênh
CHECKED = {"character_part"}
EXEMPT = {"character_root", "mechanical", "camera", "prop"}


def linear_runs(values):
    """Đoạn tuyến tính: chuỗi ≥ MIN_RUN bước tốc độ không đổi (±3%) bắt đầu ngay sau một lần
    đứng yên hoặc kết thúc ngay trước một lần đứng yên (khởi/dừng đột ngột, không easing);
    hoặc chuỗi tốc độ không đổi dài ≥ LONG_RUN bước ở bất kỳ đâu."""
    v = np.asarray(values, dtype=np.float64)
    if v.ndim == 1:
        v = v[:, None]
    if len(v) < MIN_RUN + 1:
        return []
    sp = np.linalg.norm(np.diff(v, axis=0), axis=1)
    top = sp.max()
    if top <= 1e-9:
        return []
    moving = sp > MOVING * top
    n = len(sp)
    runs, i = [], 0
    while i < n:
        if not moving[i]:
            i += 1
            continue
        j = i + 1  # chuỗi dài nhất từ i mà mọi tốc độ trong ±3% trung bình
        while j < n and moving[j]:
            seg = sp[i:j + 1]
            mu = seg.mean()
            if np.max(np.abs(seg - mu)) > REL_TOL * mu:
                break
            j += 1
        length = j - i
        onset = i > 0 and not moving[i - 1]
        offset = j < n and not moving[j]
        if (length >= MIN_RUN and (onset or offset)) or length >= LONG_RUN:
            runs.append((i, j))  # bước i..j-1 ⇒ khung i..j
            i = j
        else:
            i += 1
    return runs


def check_h1(video, profile, motion_path=None):
    spec = json.load(open(motion_path, encoding="utf-8"))
    fps = spec.get("fps")
    notes = []
    if fps != 24:
        return result("H1", FAIL, notes=[f"Dữ liệu chuyển động không ở 24 fps (fps={fps})."])
    checked, exempt, found, unknown = 0, [], [], []
    for ch in spec.get("channels", []):
        cls = ch.get("class")
        if cls in EXEMPT:
            exempt.append(dict(id=ch.get("id"), lop=cls, ly_do=ch.get("reason", "")))
            continue
        if cls not in CHECKED:
            unknown.append(ch.get("id"))
            continue
        checked += 1
        f0 = int(ch.get("first_frame", 0))
        for a, b in linear_runs(ch["values"]):
            found.append(dict(kenh=ch["id"], tu_khung=f0 + a, den_khung=f0 + b, so_khung=b - a + 1))
    no_reason = [e["id"] for e in exempt if e["lop"] == "mechanical" and not e["ly_do"].strip()]
    ms = [metric("đoạn tuyến tính ở bộ phận nhân vật", len(found), "<=", 0, "đoạn"),
          metric("kênh 'mechanical' thiếu lý do", len(no_reason), "<=", 0, "kênh"),
          metric("kênh có lớp không hợp lệ", len(unknown), "<=", 0, "kênh")]
    if checked == 0:
        notes.append("Không có kênh 'character_part' nào: shot không có nhân vật, hoặc dữ liệu thiếu.")
    return result("H1", None, ms, notes,
                  evidence=dict(kenh_kiem=checked, doan_tuyen_tinh=found[:100], kenh_mien=exempt,
                                kenh_lop_la=unknown, kenh_mechanical_thieu_ly_do=no_reason))
