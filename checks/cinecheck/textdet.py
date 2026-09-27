"""Máy dò chữ độc lập cho P0: PP-OCRv4 det (DB, PaddleOCR, Apache-2.0) chạy bằng onnxruntime.

Mô hình ghim trong checks/models/ (SHA nằm trong checks/LOCK). Không dùng matte chữ do render xuất.
Hậu xử lý DB viết lại tối giản: bản đồ xác suất → ngưỡng → thành phần liên thông → điểm hộp = trung
bình xác suất trong thành phần → nới hộp theo tỷ lệ unclip.
"""
from pathlib import Path

import cv2
import numpy as np

MODEL = Path(__file__).resolve().parent.parent / "models" / "ch_PP-OCRv4_det_infer.onnx"
MAX_SIDE = 1344      # cạnh dài tối đa khi suy luận (bội 32); 1080p → 1344×768
BIN_THRESH = 0.3     # ngưỡng nhị phân bản đồ xác suất (mặc định PaddleOCR)
UNCLIP = 1.6         # tỷ lệ nới hộp (mặc định PaddleOCR)

_sess = None


def _session():
    global _sess
    if _sess is None:
        import onnxruntime as ort
        so = ort.SessionOptions()
        so.intra_op_num_threads = 4
        so.log_severity_level = 3
        _sess = ort.InferenceSession(str(MODEL), so, providers=["CPUExecutionProvider"])
    return _sess


def prob_map(rgb):
    """rgb uint8 (h, w, 3) → bản đồ xác suất chữ float32 cùng kích thước khung."""
    h, w = rgb.shape[:2]
    s = min(1.0, MAX_SIDE / max(h, w))
    nh, nw = max(32, int(round(h * s / 32)) * 32), max(32, int(round(w * s / 32)) * 32)
    x = cv2.resize(rgb, (nw, nh), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
    x = (x[..., ::-1] - 0.5) / 0.5  # mô hình Paddle nhận BGR, chuẩn hoá (x-0.5)/0.5
    x = np.ascontiguousarray(x.transpose(2, 0, 1)[None])
    p = _session().run(None, {"x": x})[0][0, 0]
    return cv2.resize(p, (w, h), interpolation=cv2.INTER_LINEAR)


def detect(rgb, min_score=0.6, min_h=8):
    """Trả về list dict(box=[x0,y0,x1,y1], score, area) cho các vùng chữ dò được."""
    p = prob_map(rgb)
    binm = (p > BIN_THRESH).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(binm, connectivity=8)
    out = []
    H, W = binm.shape
    for i in range(1, n):
        x, y, w, h, a = stats[i]
        if a < 12 or min(w, h) < 3:
            continue
        comp = lab[y:y + h, x:x + w] == i
        score = float(p[y:y + h, x:x + w][comp].mean())
        if score < min_score:
            continue
        # nới hộp: d = A·r / L (công thức unclip của DB) trên hộp bao
        d = a * UNCLIP / max(1.0, 2.0 * (w + h))
        x0, y0 = max(0, int(x - d)), max(0, int(y - d))
        x1, y1 = min(W - 1, int(x + w + d)), min(H - 1, int(y + h + d))
        if y1 - y0 < min_h:
            continue
        out.append(dict(box=[x0, y0, x1, y1], score=round(score, 3), area=int(a)))
    return out


# ------------------------------------------------------------------ xác nhận bằng mô hình nhận dạng
REC_MODEL = MODEL.parent / "ch_PP-OCRv4_rec_infer.onnx"
REC_H = 48
_rec = None
_chars = None


def _rec_session():
    global _rec, _chars
    if _rec is None:
        import onnxruntime as ort
        so = ort.SessionOptions()
        so.intra_op_num_threads = 4
        so.log_severity_level = 3
        _rec = ort.InferenceSession(str(REC_MODEL), so, providers=["CPUExecutionProvider"])
        _chars = ["<blank>"] + _rec.get_modelmeta().custom_metadata_map["character"].splitlines() + [" "]
    return _rec, _chars


def recognize(rgb, box):
    """Đọc dòng chữ trong hộp (giải mã CTC tham lam). Trả về (chuỗi, độ tin trung bình)."""
    sess, chars = _rec_session()
    x0, y0, x1, y1 = box
    crop = rgb[y0:y1 + 1, x0:x1 + 1]
    h, w = crop.shape[:2]
    if h < 4 or w < 4:
        return "", 0.0
    nw = int(min(1600, max(16, round(w * REC_H / h))))
    x = cv2.resize(crop, (nw, REC_H), interpolation=cv2.INTER_LINEAR).astype(np.float32) / 255.0
    x = (x[..., ::-1] - 0.5) / 0.5
    out = sess.run(None, {"x": np.ascontiguousarray(x.transpose(2, 0, 1)[None])})[0][0]
    idx, pr = out.argmax(1), out.max(1)
    txt, confs, prev = [], [], 0
    for i, p in zip(idx, pr):
        if i != 0 and i != prev:
            txt.append(chars[i] if i < len(chars) else "")
            confs.append(float(p))
        prev = i
    return "".join(txt), (float(np.mean(confs)) if confs else 0.0)


def is_latin_text(s, conf, min_conf=0.8):
    """Chữ phim (tiếng Anh): ≥ 2 ký tự Latin/số, chiếm ≥ 60% ký tự không trắng, độ tin ≥ min_conf."""
    s = s.strip()
    core = [c for c in s if not c.isspace()]
    lat = sum(c.isascii() and c.isalnum() for c in core)
    return lat >= 2 and lat >= 0.6 * max(1, len(core)) and conf >= min_conf


def solidity(rgb, box, min_area=20):
    """Trung vị độ đặc (diện tích / diện tích hộp bao) của các thành phần tiền cảnh trong hộp.
    Tiền cảnh = phía thiểu số sau ngưỡng Otsu. Ký tự có nét (thường 0,2–0,7); ô cửa sổ, lưới là khối
    đặc (≈ 1). Trả None nếu không có thành phần."""
    x0, y0, x1, y1 = box
    g = cv2.cvtColor(np.ascontiguousarray(rgb[y0:y1 + 1, x0:x1 + 1]), cv2.COLOR_RGB2GRAY)
    if g.size < 64:
        return None
    _, b = cv2.threshold(g, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    if b.mean() > 0.5:
        b = 1 - b
    n, _, st, _ = cv2.connectedComponentsWithStats(b.astype(np.uint8), connectivity=8)
    fills = [st[i, 4] / float(st[i, 2] * st[i, 3]) for i in range(1, n)
             if st[i, 4] >= min_area and st[i, 2] < b.shape[1] and st[i, 3] < b.shape[0]]
    return float(np.median(fills)) if fills else None
