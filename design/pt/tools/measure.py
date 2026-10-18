"""PT việc 7 — đo khung tĩnh 1080p (không chữ): hai cách, ghi cả hai để so với mốc đối thủ do điều phối cung cấp.
 M1 = scripts/k2tl/measure_look.measure (chuẩn cổng điều phối 16/10: thu về 640×360, vùng giữa 15–85 %; chi tiết = |Laplace| TB).
 M2 = cắt ĐÚNG vùng giữa 640×360 của khung 1920×1080 (không thu nhỏ): bão hoà HSV trung vị, colorfulness Hasler–Süsstrunk,
      chi tiết = trung bình PIL ImageFilter.FIND_EDGES trên độ sáng (0..255).
  python -I measure.py <ảnh…> --json ra.json"""
import sys, os, json, numpy as np, cv2
from PIL import Image, ImageFilter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'scripts', 'k2tl'))
from measure_look import measure as m1
def m2(p):
    im = Image.open(p).convert('RGB'); W, H = im.size; x0, y0 = (W - 640) // 2, (H - 360) // 2; c = im.crop((x0, y0, x0 + 640, y0 + 360))
    a = np.asarray(c); hsv = cv2.cvtColor(a, cv2.COLOR_RGB2HSV); sat = float(np.median(hsv[..., 1]) / 255)
    r, g, b = [a[..., k].astype(np.float64) for k in range(3)]; rg, yb = r - g, 0.5 * (r + g) - b
    col = float(np.sqrt(rg.std() ** 2 + yb.std() ** 2) + 0.3 * np.sqrt(rg.mean() ** 2 + yb.mean() ** 2))
    fe = np.asarray(c.convert('L').filter(ImageFilter.FIND_EDGES)).astype(np.float64)[1:-1, 1:-1].mean()
    return dict(sat_med=round(sat, 3), colorful=round(col, 1), detail_find_edges=round(float(fe), 1))
args = [a for a in sys.argv[1:] if not a.startswith('--')]; out = sys.argv[sys.argv.index('--json') + 1] if '--json' in sys.argv else None
if out in args: args.remove(out)
rows = []
for p in args:
    r = {'file': os.path.basename(p), 'M1': {k: v for k, v in m1(p).items() if k != 'file'}, 'M2': m2(p)}; rows.append(r)
    print(f"{r['file']:34s} M1 {r['M1']['sat_med']:.3f}/{r['M1']['colorful']:5.1f}/{r['M1']['detail']:5.1f}  M2 {r['M2']['sat_med']:.3f}/{r['M2']['colorful']:5.1f}/{r['M2']['detail_find_edges']:5.1f}")
if out: json.dump(rows, open(out, 'w'), indent=1, ensure_ascii=False)
