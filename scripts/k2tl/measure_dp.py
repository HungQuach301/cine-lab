"""V5b-2c (lệnh V0 mục e) · đo khung tĩnh ĐÚNG CÁCH ĐIỀU PHỐI (cổng chuẩn hình §11.3, 18/10): ảnh thu về 640×360, vùng giữa y 60–300 (cả bề ngang),
  sat_med  — trung vị độ bão hoà HSV (PIL, 0..1)
  colorful — Hasler & Süsstrunk 2003 trên vùng đó (thang 0..255)
  edges    — trung bình PIL ImageFilter.FIND_EDGES trên ảnh xám vùng đó (0..255)
  clip_pct — % điểm ảnh có kênh lớn nhất ≥ 250 (cả khung 640×360; "không cháy sáng")
Khác measure_look.py (V5b-1b: hộp 15–85 %, OpenCV, |Laplace|) — giữ cả hai, báo cáo ghi rõ cách nào.
Dùng: measure_dp.py <ảnh…> [--json ra.json]"""
import argparse, json
import numpy as np
from PIL import Image, ImageFilter


def measure(p):
    im = Image.open(p).convert("RGB").resize((640, 360), Image.LANCZOS)
    a = np.asarray(im).astype(np.float64)
    clip = float((a.max(-1) >= 250).mean() * 100)
    c = im.crop((0, 60, 640, 300))
    s = np.asarray(c.convert("HSV"))[..., 1] / 255.0
    r, g, b = [np.asarray(c)[..., k].astype(np.float64) for k in range(3)]
    rg, yb = r - g, 0.5 * (r + g) - b
    col = float(np.sqrt(rg.std() ** 2 + yb.std() ** 2) + 0.3 * np.sqrt(rg.mean() ** 2 + yb.mean() ** 2))
    e = float(np.asarray(c.convert("L").filter(ImageFilter.FIND_EDGES)).mean())
    return dict(file=p, sat_med=round(float(np.median(s)), 3), colorful=round(col, 1), edges=round(e, 1), clip_pct=round(clip, 2))


if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("img", nargs="+"); a.add_argument("--json")
    o = a.parse_args(); rows = [measure(p) for p in o.img]
    for r in rows: print(f"{r['sat_med']:.3f}  {r['colorful']:6.1f}  {r['edges']:5.1f}  clip {r['clip_pct']:5.2f}%  {r['file']}")
    med = {k: round(float(np.median([r[k] for r in rows])), 3) for k in ("sat_med", "colorful", "edges", "clip_pct")}
    print("TRUNG VỊ", med)
    if o.json: json.dump(dict(cach="dieu-phoi: 640x360, y 60-300, PIL HSV/FIND_EDGES", rows=rows, trung_vi=med), open(o.json, "w"), indent=1, ensure_ascii=False)
