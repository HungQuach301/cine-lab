"""P0 — máy dò chữ độc lập trên khung render. Không dựa vào matte: chữ dò được mà không có matte
tương ứng trong <video>.text/ thì trượt (vá giới hạn 2 của v0: P1/G4 chỉ thấy chữ có matte)."""
import numpy as np
import cv2

from .common import frame_count, metric, read_rgb, result
from .textdet import detect, is_latin_text, recognize, solidity

STEP = 12          # 2 khung/giây
MAX_FRAMES = 240
MIN_COVER = 0.5    # tỷ lệ diện tích hộp chữ nằm trong vùng matte (nét nới) để coi là có matte
MIN_DET = 0.6      # điểm hộp tối thiểu của mô hình dò
MIN_REC = 0.8      # độ tin nhận dạng tối thiểu để xác nhận là chữ Latin
SOLID_MAX = 0.85   # ký tự có nét (độ đặc 0,4–0,7 đo được); ô cửa sổ/lưới là khối đặc (≈ 1,0)


def _sample(n):
    step = STEP if n // STEP <= MAX_FRAMES else int(np.ceil(n / MAX_FRAMES))
    idx = list(range(0, n, step))
    if n and idx[-1] != n - 1:
        idx.append(n - 1)
    return idx


def _matte_zone(els, i, shape, box_h):
    from .rules_text import active, matte
    zone = np.zeros(shape[:2], np.uint8)
    for e in active(els, i):
        zone |= (matte(e, i)[..., 3] >= 0.02).astype(np.uint8)
    k = max(3, int(round(0.35 * box_h)) | 1)
    return cv2.dilate(zone, np.ones((k, k), np.uint8)).astype(bool)


def check_p0(video, profile, text_dir=None):
    from .rules_text import load_elements
    els = load_elements(text_dir) if text_dir is not None else []
    n = frame_count(video)
    idxs = _sample(n)
    frames = read_rgb(video, idxs)
    unmatted, matted, rejected, solid = [], 0, 0, []
    seen_ids = set()
    for i in idxs:
        f = frames.get(i)
        if f is None:
            continue
        for d in detect(f, min_score=MIN_DET):
            s, conf = recognize(f, d["box"])
            if not is_latin_text(s, conf, MIN_REC):
                rejected += 1
                continue
            sol = solidity(f, d["box"])
            if sol is not None and sol >= SOLID_MAX:
                solid.append(dict(khung=i, hop=d["box"], chu=s[:40], do_tin=round(conf, 2), do_dac=round(sol, 2)))
                continue
            x0, y0, x1, y1 = d["box"]
            cover = 0.0
            if els:
                z = _matte_zone(els, i, f.shape, y1 - y0)
                cover = float(z[y0:y1 + 1, x0:x1 + 1].mean())
            if cover >= MIN_COVER:
                matted += 1
                from .rules_text import active
                seen_ids.update(e["id"] for e in active(els, i))
            else:
                unmatted.append(dict(khung=i, hop=d["box"], chu=s[:80], do_tin=round(conf, 2),
                                     phu_matte=round(cover, 2)))
    unseen = sorted({e["id"] for e in els} - seen_ids)
    ms = [metric("vùng chữ dò được không có matte", len(unmatted), "<=", 0, "vùng·khung")]
    notes = [f"Lấy mẫu {len(idxs)} khung (≈ 2 khung/giây). Vùng máy dò nghi là chữ nhưng nhận dạng "
             f"không xác nhận chữ Latin (cửa sổ, lưới, hoa văn): {rejected} (bỏ qua)."]
    if solid:
        notes.append(f"Vùng đọc ra chữ nhưng là khối đặc (độ đặc ≥ {SOLID_MAX}, cửa sổ/lưới), bị loại: {len(solid)} "
                     "(liệt kê trong bằng chứng để người duyệt soi).")
    if not els:
        notes.append("Không có matte chữ (thiếu <video>.text/ hoặc elements rỗng): mọi chữ dò được đều trượt.")
    if unseen:
        notes.append("Phần tử có matte nhưng máy dò không thấy ở khung mẫu nào (tham khảo, không trượt): "
                     + ", ".join(unseen))
    return result("P0", None, ms, notes,
                  evidence=dict(chu_khong_matte=unmatted[:60], vung_co_matte=matted,
                                vung_bi_loai=rejected, vung_khoi_dac=solid[:60], khung_lay_mau=len(idxs),
                                phan_tu_may_do_khong_thay=unseen))
