"""V5b-1b · test đo chuẩn hình (measure_look): ảnh xám → bão hoà 0, colorfulness 0, chi tiết 0; ô bàn cờ đỏ/xanh → colorfulness cao, chi tiết > 0; cháy sáng đếm đúng."""
import sys, tempfile, os
import numpy as np, cv2
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from measure_look import measure
d = tempfile.mkdtemp()
g = np.full((1080, 1920, 3), 128, np.uint8); cv2.imwrite(f"{d}/g.png", g); m = measure(f"{d}/g.png")
assert m["sat_med"] == 0 and m["colorful"] == 0 and m["detail"] == 0 and m["clip_pct"] == 0, m
c = np.zeros((1080, 1920, 3), np.uint8); yy, xx = np.mgrid[:1080, :1920]; k = ((yy // 60 + xx // 60) % 2).astype(bool)
c[k] = (40, 40, 220); c[~k] = (220, 120, 30); c[:108] = 255; cv2.imwrite(f"{d}/c.png", c); m = measure(f"{d}/c.png")
assert m["sat_med"] > 0.7 and m["colorful"] > 60 and m["detail"] > 1 and abs(m["clip_pct"] - 10.0) < 0.6, m
print("test_look OK", m)
