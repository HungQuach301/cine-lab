"""V5b-1b · đo CHUẨN HÌNH trên khung tĩnh (cách đo của cổng điều phối 16/10): ảnh thu về 640×360 (INTER_AREA), lấy VÙNG GIỮA
(x 15–85 %, y 15–85 % — ngoài hộp năm dưới-trái, chỉ số trên-phải, dải nguồn dưới), khung dựng KHÔNG lớp chữ (render.js override noText).
Chỉ số:
  sat_med   — trung vị độ bão hoà HSV (S ∈ 0..1, OpenCV)
  colorful  — Hasler & Süsstrunk 2003: sqrt(σ_rg² + σ_yb²) + 0,3·sqrt(μ_rg² + μ_yb²), rg = R − G, yb = (R + G)/2 − B (thang 0..255)
  detail    — trung bình |Laplace| (nhân 3×3 4-lân cận, cv2.Laplacian ksize=1) trên độ sáng Y (0..255)
  clip_pct  — % điểm ảnh cháy sáng (kênh lớn nhất ≥ 250) trên CẢ khung 640×360
  content   — (tuỳ chọn) % diện tích vùng giữa là nội dung có nghĩa theo mặt nạ id từ render.js --ids (không tự khai)
Dùng: measure_look.py <ảnh…> [--json ra.json] [--label nhãn]   → bảng + JSON"""
import argparse, json, sys
import cv2, numpy as np

BOX = (0.15, 0.15, 0.85, 0.85)


def measure(path, box=BOX):
    im = cv2.imread(path, cv2.IMREAD_COLOR)
    if im is None: raise SystemExit("không đọc được " + path)
    im = cv2.resize(im, (640, 360), interpolation=cv2.INTER_AREA)
    clip = float((im.max(-1) >= 250).mean() * 100)
    x0, y0, x1, y1 = int(box[0] * 640), int(box[1] * 360), int(box[2] * 640), int(box[3] * 360)
    c = im[y0:y1, x0:x1]
    hsv = cv2.cvtColor(c, cv2.COLOR_BGR2HSV); sat = float(np.median(hsv[..., 1]) / 255)
    b, g, r = [c[..., k].astype(np.float64) for k in range(3)]
    rg, yb = r - g, 0.5 * (r + g) - b
    colorful = float(np.sqrt(rg.std() ** 2 + yb.std() ** 2) + 0.3 * np.sqrt(rg.mean() ** 2 + yb.mean() ** 2))
    Y = cv2.cvtColor(c, cv2.COLOR_BGR2GRAY).astype(np.float32)
    det = float(np.abs(cv2.Laplacian(Y, cv2.CV_32F, ksize=1)).mean())
    return dict(file=path, sat_med=round(sat, 3), colorful=round(colorful, 1), detail=round(det, 1), clip_pct=round(clip, 2), lum_mean=round(float(Y.mean()), 1))


if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("img", nargs="+"); a.add_argument("--json"); a.add_argument("--label", default="")
    o = a.parse_args(); rows = [measure(p) for p in o.img]
    for r in rows: print(f"{r['sat_med']:.3f}  {r['colorful']:6.1f}  {r['detail']:5.1f}  clip {r['clip_pct']:5.2f}%  L {r['lum_mean']:5.1f}  {r['file']}")
    if rows:
        med = {k: round(float(np.median([r[k] for r in rows])), 3) for k in ("sat_med", "colorful", "detail", "clip_pct")}
        print("TRUNG VỊ", med)
    if o.json: json.dump(dict(label=o.label, box=BOX, rows=rows), open(o.json, "w"), indent=1, ensure_ascii=False)
