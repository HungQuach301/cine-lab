"""Test geo.py: UTM thuận/nghịch khớp điểm chuẩn và khứ hồi < 1 mm."""
import sys, unittest, numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import geo

class T(unittest.TestCase):
    def test_roundtrip(self):
        lon, lat = np.array([-5.3487, -5.9, -3.1]), np.array([36.1513, 36.9, 40.0])
        E, N = geo.utm(lon, lat); lo, la = geo.utm_inv(E, N)
        self.assertLess(np.abs(lo - lon).max() * 111e3, 1e-3); self.assertLess(np.abs(la - lat).max() * 111e3, 1e-3)
    def test_central_meridian(self):   # trên kinh tuyến trục -3°: E = 500 000 đúng
        E, N = geo.utm(-3.0, 36.0); self.assertAlmostEqual(float(E), 500000.0, places=3)
        self.assertAlmostEqual(float(N), 0.9996 * 3985542.6, delta=1.0)   # 36°N: cung kinh tuyến WGS84 3 985 542,6 m × k0
if __name__ == "__main__":
    unittest.main()
