#!/opt/cine/bin/python
"""ĐÓNG-GÓI-T3 · đo số trên ảnh thumbnail (đối thủ: thư mục tạm ngoài git, xoá sau khi đo; của ta: thumbnail ứng viên).
Mỗi ảnh → 640×360 (cắt khung 4:3 có viền đen về 16:9): độ sáng L* TB, bão hoà HSV TB, tương phản RMS (độ lệch L*/100), độ màu Hasler–Süsstrunk,
tỷ lệ điểm ảnh ấm (đỏ–cam–vàng, S > 0,35), tỷ lệ "đêm" (L* < 25), phần trên 1/3 giống trời (xanh/xám sáng, ít cạnh),
OCR (RapidOCR, chạy cục bộ): diện tích hộp chữ / khung, số từ, chiều cao chữ lớn nhất / chiều cao khung.
Dùng: PYTHONPATH=<ocr> do_anh.py <thư mục ảnh> <out.json>"""
import json, sys
from pathlib import Path
import numpy as np, cv2
from rapidocr_onnxruntime import RapidOCR
ocr = RapidOCR()
def load(p):
    im = cv2.imread(str(p)); h, w = im.shape[:2]
    if abs(w / h - 4 / 3) < 0.02:   # sddefault/hqdefault: 16:9 nằm giữa, viền đen trên/dưới
        hh = int(w * 9 / 16); y = (h - hh) // 2; im = im[y:y + hh]
    return cv2.resize(im, (640, 360), interpolation=cv2.INTER_AREA)
def measure(p):
    im = load(p); lab = cv2.cvtColor(im, cv2.COLOR_BGR2LAB).astype(np.float32); L = lab[..., 0] * 100 / 255
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV).astype(np.float32); H, S, V = hsv[..., 0] * 2, hsv[..., 1] / 255, hsv[..., 2] / 255
    b, g, r = [im[..., i].astype(np.float32) for i in range(3)]; rg = r - g; yb = 0.5 * (r + g) - b
    colorful = float(np.hypot(rg.std(), yb.std()) + 0.3 * np.hypot(rg.mean(), yb.mean()))
    warm = float(((((H < 50) | (H > 340)) & (S > 0.35) & (V > 0.25))).mean())
    top = im[:120]; th = hsv[:120]; edges = cv2.Canny(cv2.cvtColor(top, cv2.COLOR_BGR2GRAY), 80, 160).mean() / 255
    skyish = float((((th[..., 0] * 2 > 180) & (th[..., 0] * 2 < 260) & (th[..., 2] > 110)) | ((th[..., 1] < 40) & (th[..., 2] > 170))).mean())
    res, _ = ocr(str(p)) if True else (None, None)
    # OCR trên ảnh gốc → quy về khung 16:9 640×360
    raw = cv2.imread(str(p)); h0, w0 = raw.shape[:2]; yoff = (h0 - int(w0 * 9 / 16)) // 2 if abs(w0 / h0 - 4 / 3) < 0.02 else 0; sc = 640 / w0
    area = 0.0; words = 0; hmax = 0.0; boxes = []
    for box, txt, conf in (res or []):
        if float(conf) < 0.6 or len(txt.strip()) == 0: continue
        pts = np.array(box, np.float32); pts[:, 1] -= yoff; pts *= sc
        x0, y0 = pts.min(0); x1, y1 = pts.max(0)
        if y1 < 0 or y0 > 360: continue
        boxes.append([float(x0), float(y0), float(x1), float(y1)]); words += len(txt.split()); hmax = max(hmax, (y1 - y0) / 360)
    m = np.zeros((360, 640), np.uint8)
    for x0, y0, x1, y1 in boxes: m[max(0, int(y0)):int(y1), max(0, int(x0)):int(x1)] = 1
    area = float(m.mean())
    return {"L_mean": round(float(L.mean()), 1), "sat_mean": round(float(S.mean()), 3), "contrast_rms": round(float(L.std() / 100), 3), "colorfulness": round(colorful, 1),
            "warm_frac": round(warm, 3), "night_frac": round(float((L < 25).mean()), 3), "top_sky_frac": round(skyish, 3), "top_edge": round(float(edges), 3),
            "text_area": round(float(area), 3), "text_words": int(words), "text_hmax": round(float(hmax), 3), "_ocr_txt": [t for _, t, c in (res or []) if float(c) >= 0.6]}
if __name__ == "__main__":
    d = Path(sys.argv[1]); out = {p.stem: measure(p) for p in sorted(d.glob("*.jpg")) + sorted(d.glob("*.png"))}
    Path(sys.argv[2]).write_text(json.dumps(out, indent=1, ensure_ascii=False)); print(len(out), "ảnh")
