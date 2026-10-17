"""Test calib.py trên dữ liệu tổng hợp: máy biết trước → chiếu 8 điểm + nhiễu 1 px → giải lại phải khớp; < 6 điểm phải dừng."""
import sys, unittest, numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import calib

class T(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(3); self.cam = np.array([-172.0, 80.0, 1.7]); yaw, pitch, roll, f, w, h = np.radians(118), np.radians(9), np.radians(0.6), 1450.0, 1200, 1114
        P = np.array([[-136, -28, 0], [-133, 52, 0], [-76, 50, 0], [-76, 50, 26], [-133, 52, 26], [-110, 40, 31], [-136, -28, 26], [-100, 51, 14]], float)
        uv, _ = calib.project(P, self.cam, yaw, pitch, roll, f, w, h); uv += rng.normal(0, 1.0, uv.shape)
        self.spec = dict(image=dict(w=w, h=h), eye_h=1.7, init=dict(E=-160, N=95), points=[dict(name=str(i), uv=u.tolist(), enu=p.tolist()) for i, (u, p) in enumerate(zip(uv, P))])
    def test_recover(self):
        r = calib.solve(self.spec)
        self.assertLess(np.hypot(*(np.array(r["cam_enu"][:2]) - self.cam[:2])), 2.0); self.assertLess(r["rms_px"], 2.0); self.assertLess(r["rms_pct_width"], 1.0)
    def test_min_points(self):
        s = dict(self.spec, points=self.spec["points"][:5])
        with self.assertRaises(SystemExit): calib.solve(s)
if __name__ == "__main__":
    unittest.main()
