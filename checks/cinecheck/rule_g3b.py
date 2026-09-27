"""G3b — grain cố định: grain phải có, ổn định theo thời gian trong shot và giữa các shot, và
chuyển động theo khung (không phải lớp nhiễu đứng yên dán lên màn hình). Đo trên luma file render."""
import math
import subprocess

import cv2
import numpy as np

from .common import metric, probe, result, stream

STEP = 12            # cặp khung (n, n+1) mỗi 12 khung (2 cặp/giây)
MAX_PAIRS = 240
BLOCK = 32
FLAT_STD = 1.5       # khối "phẳng": độ lệch chuẩn của ảnh đã làm mờ (σ=2) ≤ 1,5 mã 8 bit
LUMA_BAND = (40, 210)  # chỉ đo khối trung tính (tránh vùng kẹp đen/trắng; grain thường theo độ sáng)
MIN_BLOCKS = 20      # khung cần ≥ 20 khối phẳng mới đo được
PRESENT_MIN = 0.8    # σ grain tối thiểu (mã 8 bit), trung vị theo shot (nội bộ)
CV_MAX = 0.20        # hệ số biến thiên σ theo thời gian trong shot (nội bộ)
SHOT_RATIO_MAX = 1.30  # σ shot lớn nhất / nhỏ nhất (nội bộ)
FROZEN_MAX = 0.50    # tương quan phần dư giữa 2 khung kề ở khối phẳng (nội bộ)


def _pairs(path):
    """Sinh (chỉ số khung, luma khung n, luma khung n+1) quy về thang 8 bit, đọc tuần tự."""
    info = probe(path)
    v = stream(info, "video")
    w, h = int(v["width"]), int(v["height"])
    pix = v.get("pix_fmt", "")
    depth = 10 if "10" in pix else (12 if "12" in pix else 8)
    fmt = {10: "gray10le", 12: "gray12le"}.get(depth, "gray")
    n = int(v.get("nb_frames") or 0)
    step = STEP
    if n and n // step > MAX_PAIRS:
        step = int(math.ceil(n / MAX_PAIRS))
    cmd = ["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:v:0", "-vf",
           f"select='lt(mod(n\\,{step})\\,2)',extractplanes=y", "-fps_mode", "passthrough",
           "-f", "rawvideo", "-pix_fmt", fmt, "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    bpp = 1 if depth == 8 else 2
    per = w * h * bpp
    k = 0
    prev = None
    while True:
        buf = p.stdout.read(per)
        if len(buf) < per:
            break
        y = np.frombuffer(buf, np.uint8 if bpp == 1 else np.uint16).reshape(h, w).astype(np.float32)
        y /= 2 ** (depth - 8)
        if k % 2 == 0:
            prev = y
        else:
            yield (k // 2) * step, prev, y
        k += 1
    p.wait()


def _blocks(a):
    h, w = a.shape
    H, W = h // BLOCK, w // BLOCK
    return a[:H * BLOCK, :W * BLOCK].reshape(H, BLOCK, W, BLOCK).swapaxes(1, 2).reshape(H, W, -1)


def grain_frame(y):
    """σ grain của khung (mã 8 bit) và mặt nạ khối phẳng. σ = 1,4826·MAD phần dư sau làm mờ σ=1,5."""
    r = y - cv2.GaussianBlur(y, (0, 0), 1.5)
    s = cv2.GaussianBlur(y, (0, 0), 2.0)
    sb, rb, yb = _blocks(s), _blocks(r), _blocks(y)
    flat = (sb.std(-1) <= FLAT_STD) & (yb.mean(-1) >= LUMA_BAND[0]) & (yb.mean(-1) <= LUMA_BAND[1])
    if flat.sum() < MIN_BLOCKS:
        return None, flat, r
    med = np.median(rb[flat], axis=-1, keepdims=True)
    sig = 1.4826 * np.median(np.abs(rb[flat] - med), axis=-1)
    return float(np.median(sig)), flat, r


def _corr(ra, rb, flat):
    a, b = _blocks(ra)[flat].ravel(), _blocks(rb)[flat].ravel()
    a, b = a - a.mean(), b - b.mean()
    d = math.sqrt(float((a * a).sum() * (b * b).sum()))
    return float((a * b).sum() / d) if d > 0 else 0.0


def shots(path):
    """Ranh giới shot (khung đầu mỗi shot) bằng PySceneDetect ContentDetector mặc định."""
    from scenedetect import ContentDetector, detect
    sc = detect(str(path), ContentDetector())
    return [0] + [s[0].frame_num for s in sc[1:]] if sc else [0]


_cache = {}


def measure(path):
    """Số đo grain theo shot, dùng chung cho G3b và N3 (v1.1: bitrate master khi có grain).
    Nhớ đệm theo (đường dẫn, kích thước, mtime) để không giải mã hai lần trong một lần chạy."""
    import os
    st = os.stat(path)
    key = (str(path), st.st_size, st.st_mtime_ns)
    if key not in _cache:
        _cache.clear()
        _cache[key] = _measure(path)
    return _cache[key]


def grain_present(path):
    """σ grain lớn nhất theo shot (trung vị trong shot), None nếu không đo được."""
    m = measure(path)
    meds = [x["sigma_trung_vi"] for x in m["stats"].values()]
    return max(meds) if meds else None


def _measure(path):
    starts = shots(path)
    rows = []
    for idx, a, b in _pairs(path):
        sig, flat, ra = grain_frame(a)
        if sig is None:
            rows.append((idx, None, None))
            continue
        sig_b, _, rb = grain_frame(b)
        c = _corr(ra, rb, flat)
        rows.append((idx, sig, c))
        if sig_b is not None:  # cả khung n+1: bắt grain dao động theo loại khung mã hoá (I/P/B)
            rows.append((idx + 1, sig_b, c))
    shot_of = lambda i: max(k for k, s in enumerate(starts) if s <= i)
    per = {}
    for idx, sig, c in rows:
        if sig is not None:
            per.setdefault(shot_of(idx), []).append((idx, sig, c))
    unmeasured = sum(sig is None for _, sig, _ in rows)
    stats = {}
    for k, v in per.items():
        s = np.array([x[1] for x in v])
        c = np.array([x[2] for x in v])
        stats[k] = dict(tu_khung=starts[k], so_khung_do=len(v), sigma_trung_vi=round(float(np.median(s)), 3),
                        cv=round(float(s.std() / s.mean()) if s.mean() > 0 else 0.0, 3),
                        tuong_quan_khung_ke=round(float(np.median(c)), 3))
    return dict(starts=starts, rows=len(rows), unmeasured=unmeasured, stats=stats)


def check_g3b(path, profile):
    m = measure(path)
    starts, stats, unmeasured = m["starts"], m["stats"], m["unmeasured"]
    if not stats:
        return result("G3b", "FAIL", notes=["Không khung nào có đủ khối phẳng trung tính để đo grain "
                                           f"({m['rows']} khung đo). Không chứng minh được grain."])
    meds = [x["sigma_trung_vi"] for x in stats.values()]
    ratio = max(meds) / min(meds) if min(meds) > 0 else float("inf")
    ms = [metric("σ grain nhỏ nhất theo shot", min(meds), ">=", PRESENT_MIN, "mã 8 bit"),
          metric("biến thiên σ theo thời gian (CV) lớn nhất trong shot", max(x["cv"] for x in stats.values()),
                 "<=", CV_MAX),
          metric("σ shot lớn nhất / nhỏ nhất", ratio, "<=", SHOT_RATIO_MAX),
          metric("tương quan grain giữa 2 khung kề (trung vị, shot tệ nhất)",
                 max(x["tuong_quan_khung_ke"] for x in stats.values()), "<=", FROZEN_MAX)]
    notes = [f"{len(starts)} shot (PySceneDetect); {m['rows']} khung đo, {unmeasured} khung không đủ khối phẳng."]
    if len(stats) < len(starts):
        notes.append(f"{len(starts) - len(stats)} shot không đo được grain (không có khung đủ khối phẳng).")
    return result("G3b", None, ms, notes, evidence=dict(theo_shot=stats, shot_bat_dau=starts[:200]))
