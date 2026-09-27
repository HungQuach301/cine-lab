"""H1b — đối chiếu dữ liệu chuyển động bake với luồng quang học trên hình render, ở vùng nhân vật.

Cần <video>.motion.json (định dạng H1) có thêm "screen_tracks": vị trí điểm ảnh (x, y) theo từng khung
của các khớp nhân vật, chiếu từ rig sau mọi ràng buộc qua máy quay render; null khi bị che/ra khỏi khung.
  {"screen_tracks": [{"id": "hero/hand_R", "first_frame": 0, "values": [[812.4, 530.1], null, ...]}]}
Máy tính luồng quang học DIS (OpenCV) giữa khung n và n+1 của file render; tại mỗi điểm, lấy trung vị
luồng trong đĩa bán kính 4 px, so với dịch chuyển khai báo p(n+1) − p(n).
"""
import json
import subprocess

import cv2
import numpy as np

from .common import FAIL, metric, probe, result, stream

RADIUS = 4            # px ở độ phân giải khung
ABS_TOL = 1.5         # px
REL_TOL = 0.25        # × độ dài dịch chuyển khai báo
MIN_AGREE = 90.0      # % cặp khung khớp, mỗi track (nội bộ)
MAX_PAIRS = 480
FLOW_MAX_W = 1280     # tính luồng ở độ phân giải ≤ 1280 px rộng rồi quy đổi


def _gray_frames(path, wanted):
    v = stream(probe(path), "video")
    w, h = int(v["width"]), int(v["height"])
    cmd = ["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:v:0", "-fps_mode", "passthrough",
           "-f", "rawvideo", "-pix_fmt", "gray", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    i = 0
    last = max(wanted) if wanted else -1
    while i <= last:
        buf = p.stdout.read(w * h)
        if len(buf) < w * h:
            break
        if i in wanted:
            yield i, np.frombuffer(buf, np.uint8).reshape(h, w)
        i += 1
    p.stdout.close()
    p.kill()
    p.wait()


def _flow(a, b):
    h, w = a.shape
    s = min(1.0, FLOW_MAX_W / w)
    if s < 1:
        a = cv2.resize(a, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA)
        b = cv2.resize(b, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA)
    dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
    f = dis.calc(a, b, None)
    return f / s, s


def _at(flow, s, x, y):
    fx, fy = x * s, y * s
    r = max(1, int(round(RADIUS * s)))
    h, w = flow.shape[:2]
    x0, x1 = max(0, int(fx) - r), min(w, int(fx) + r + 1)
    y0, y1 = max(0, int(fy) - r), min(h, int(fy) + r + 1)
    if x0 >= x1 or y0 >= y1:
        return None
    yy, xx = np.mgrid[y0:y1, x0:x1]
    m = (xx - fx) ** 2 + (yy - fy) ** 2 <= r * r
    patch = flow[y0:y1, x0:x1][m]
    return np.median(patch, 0) if len(patch) else None


def check_h1b(video, profile, motion_path=None):
    spec = json.load(open(motion_path, encoding="utf-8"))
    if spec.get("fps") != 24:
        return result("H1b", FAIL, notes=[f"Dữ liệu chuyển động không ở 24 fps (fps={spec.get('fps')})."])
    chars = sorted({c["id"].split("/")[0] for c in spec.get("channels", []) if c.get("class") == "character_part"})
    tracks = spec.get("screen_tracks", [])
    tracked = {t["id"].split("/")[0] for t in tracks}
    no_track = [c for c in chars if c not in tracked]
    v = stream(probe(video), "video")
    W, H = int(v["width"]), int(v["height"])
    # cặp khung cần tính: mọi n mà ít nhất một track có điểm ở n và n+1
    need = {}
    for t in tracks:
        f0 = int(t.get("first_frame", 0))
        vals = t["values"]
        for k in range(len(vals) - 1):
            if vals[k] is not None and vals[k + 1] is not None:
                need.setdefault(f0 + k, []).append((t["id"], vals[k], vals[k + 1]))
    pairs = sorted(need)
    if len(pairs) > MAX_PAIRS:
        pairs = sorted(set(np.linspace(pairs[0], pairs[-1], MAX_PAIRS).round().astype(int)) & set(need))
    pairs = set(pairs)
    wanted = pairs | {p + 1 for p in pairs}
    stats = {t["id"]: dict(cap=0, khop=0, epe=[], te_nhat=None) for t in tracks}
    prev = {}
    for i, g in _gray_frames(video, wanted):
        prev[i] = g
        if (i - 1) in pairs and (i - 1) in prev:
            flow, s = _flow(prev[i - 1], g)
            for tid, p, q in need[i - 1]:
                x, y = p
                if not (0 <= x < W and 0 <= y < H):
                    continue
                fv = _at(flow, s, x, y)
                if fv is None:
                    continue
                d = np.array(q, float) - np.array(p, float)
                e = float(np.linalg.norm(fv - d))
                st = stats[tid]
                st["cap"] += 1
                ok = e <= max(ABS_TOL, REL_TOL * float(np.linalg.norm(d)))
                st["khop"] += ok
                st["epe"].append(e)
                if not ok and (st["te_nhat"] is None or e > st["te_nhat"]["epe"]):
                    st["te_nhat"] = dict(khung=i - 1, epe=round(e, 2), khai=[round(float(c), 2) for c in d],
                                         luong=[round(float(c), 2) for c in fv])
        prev.pop(i - 2, None)
    per = {}
    for tid, st in stats.items():
        if st["cap"]:
            per[tid] = dict(cap_khung=st["cap"], khop_pct=round(100.0 * st["khop"] / st["cap"], 1),
                            epe_trung_vi=round(float(np.median(st["epe"])), 2), lech_lon_nhat=st["te_nhat"])
    worst = min([x["khop_pct"] for x in per.values()], default=100.0 if not tracks and not chars else 0.0)
    unmeasured = [t["id"] for t in tracks if t["id"] not in per]
    ms = [metric("nhân vật có kênh bộ phận nhưng không có screen track", len(no_track), "<=", 0, "nhân vật"),
          metric("tỷ lệ cặp khung khớp luồng quang học, track tệ nhất", worst, ">=", MIN_AGREE, "%")]
    notes = [f"{len(tracks)} track, {len(pairs)} cặp khung đo. Khớp khi |luồng − khai báo| ≤ "
             f"max({ABS_TOL} px, {REL_TOL:.0%} × độ dài dịch chuyển)."]
    if not tracks and chars:
        notes.append("Không có screen_tracks: không đối chiếu được chuyển động khai báo với hình render.")
    if not tracks and not chars:
        notes.append("Không có kênh bộ phận nhân vật và không có track: shot không có nhân vật.")
    ms.append(metric("track không đo được cặp khung nào (toàn null/ngoài khung)", len(unmeasured), "<=", 0, "track"))
    return result("H1b", None, ms, notes, evidence=dict(theo_track=per, nhan_vat_thieu_track=no_track))
