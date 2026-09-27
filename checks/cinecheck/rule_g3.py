"""G3 — banding trên gradient, đo trên luma của file đã render."""
import cv2
import numpy as np

from .common import metric, read_luma, result

FLAT = 5          # mảng phẳng tuyệt đối FLAT×FLAT
WIN = 95          # cửa sổ ngữ cảnh
MAX_STEP = 2      # bước nhảy tối đa (mã, quy về 8 bit) giữa điểm kề trong vùng bậc thang
MAX_RANGE = 24    # biên độ luma tối đa trong cửa sổ (mã 8 bit)
MIN_LEVELS = 3    # số mức mảng phẳng tối thiểu để gọi là bậc thang
THRESH_PCT = 0.2  # ngưỡng diện tích banding (% khung)


def banding_map(y, depth):
    """y: luma float ở mã gốc. Trả về mặt nạ bool các điểm banding."""
    q = np.round(y).astype(np.int32)
    k = np.ones((FLAT, FLAT), np.uint8)
    qf = q.astype(np.float32)
    mx = cv2.dilate(qf, k)
    mn = cv2.erode(qf, k)
    plateau = (mx - mn) == 0
    scale = 2 ** (depth - 8)
    # bước nhảy lớn nhất giữa điểm kề (ngang/dọc), quy về mã 8 bit
    dx = np.zeros_like(qf)
    dy = np.zeros_like(qf)
    dx[:, 1:] = np.abs(np.diff(qf, axis=1))
    dy[1:, :] = np.abs(np.diff(qf, axis=0))
    step = np.maximum(dx, dy) / scale
    kw = np.ones((WIN, WIN), np.uint8)
    smooth = cv2.dilate(step, kw) <= MAX_STEP
    rng = (cv2.dilate(qf, kw) - cv2.erode(qf, kw)) / scale
    smooth &= rng <= MAX_RANGE
    cand = plateau & smooth
    if not cand.any():
        return cand
    # đếm số mức mảng phẳng khác nhau trong cửa sổ (trên lưới thu nhỏ 1/2 cho nhanh)
    small = lambda a: cv2.resize(a.astype(np.uint8), (a.shape[1] // 2, a.shape[0] // 2),
                                 interpolation=cv2.INTER_NEAREST)
    levels = np.unique(q[plateau & smooth])
    count = np.zeros((q.shape[0] // 2, q.shape[1] // 2), np.float32)
    kh = np.ones((WIN // 2, WIN // 2), np.uint8)
    for lv in levels:
        pres = cv2.dilate(small(plateau & (q == lv)), kh)
        count += pres
    count = cv2.resize(count, (q.shape[1], q.shape[0]), interpolation=cv2.INTER_NEAREST)
    return cand & (count >= MIN_LEVELS)


def check_g3(path, profile):
    frames, depth = read_luma(path)
    worst, worst_idx, pcts = 0.0, None, []
    for idx, y in frames:
        pct = 100.0 * float(np.mean(banding_map(y, depth)))
        pcts.append(pct)
        if pct > worst:
            worst, worst_idx = pct, idx
    bad = [(idx, round(p, 3)) for (idx, _), p in zip(frames, pcts) if p > THRESH_PCT]
    ms = [metric("diện tích banding lớn nhất", worst, "<=", THRESH_PCT, "% khung")]
    ev = dict(khung_lay_mau=len(frames), bit_depth=depth, khung_te_nhat=worst_idx,
              khung_vuot_nguong=bad[:50], trung_binh_pct=round(float(np.mean(pcts)) if pcts else 0, 4))
    return result("G3", None, ms, evidence=ev)
