"""V5b-1 · hình học địa lý dùng chung cho công cụ xương sống thời gian (không cần pyproj/GDAL — môi trường không có, đo 15/10).
- UTM (WGS84) thuận/nghịch theo chuỗi Krüger bậc 6 (sai số < 1 mm trong múi); ETRS89-UTM (Catastro EPSG:25830) coi trùng WGS84-UTM (< 1 m).
- Lấy mẫu raster GeoTIFF theo ModelTiepoint/PixelScale (PixelIsArea = góc ô; PixelIsPoint = tâm ô)."""
import math
import numpy as np

A, F = 6378137.0, 1 / 298.257223563
K0, E0, N = 0.9996, 500000.0, F / (2 - F)
_A = A / (1 + N) * (1 + N**2 / 4 + N**4 / 64)
_al = [N / 2 - 2 * N**2 / 3 + 5 * N**3 / 16, 13 * N**2 / 48 - 3 * N**3 / 5, 61 * N**3 / 240]
_be = [N / 2 - 2 * N**2 / 3 + 37 * N**3 / 96, N**2 / 48 + N**3 / 15, 17 * N**3 / 480]
_de = [2 * N - 2 * N**2 / 3 - 2 * N**3, 7 * N**2 / 3 - 8 * N**3 / 5, 56 * N**3 / 15]


def utm(lon, lat, zone=30):
    """(lon, lat) độ → (E, N) mét, bán cầu bắc. Nhận số hoặc mảng numpy."""
    lon, lat = np.asarray(lon, float), np.asarray(lat, float)
    l0 = math.radians(zone * 6 - 183)
    ph, la = np.radians(lat), np.radians(lon) - l0
    t = np.sinh(np.arctanh(np.sin(ph)) - 2 * math.sqrt(N) / (1 + N) * np.arctanh(2 * math.sqrt(N) / (1 + N) * np.sin(ph)))
    xi, eta = np.arctan2(t, np.cos(la)), np.arctanh(np.sin(la) / np.sqrt(1 + t * t))
    x, y = eta.copy(), xi.copy()
    for j, a in enumerate(_al, 1):
        x = x + a * np.cos(2 * j * xi) * np.sinh(2 * j * eta); y = y + a * np.sin(2 * j * xi) * np.cosh(2 * j * eta)
    return E0 + K0 * _A * x, K0 * _A * y


def utm_inv(E, Nn, zone=30):
    E, Nn = np.asarray(E, float), np.asarray(Nn, float)
    xi, eta = Nn / (K0 * _A), (E - E0) / (K0 * _A)
    x, y = eta.copy(), xi.copy()
    for j, b in enumerate(_be, 1):
        x = x - b * np.cos(2 * j * xi) * np.sinh(2 * j * eta); y = y - b * np.sin(2 * j * xi) * np.cosh(2 * j * eta)
    chi = np.arcsin(np.sin(y) / np.cosh(x))
    ph = chi.copy()
    for j, d in enumerate(_de, 1):
        ph = ph + d * np.sin(2 * j * chi)
    la = np.arctan2(np.sinh(x), np.cos(y))
    return np.degrees(la) + zone * 6 - 183, np.degrees(ph)


class Raster:
    """Raster GeoTIFF 2D/3D (đọc trọn bằng tifffile, hoặc cửa sổ hàng/cột để tiết kiệm RAM)."""
    def __init__(self, path, window=None):
        import tifffile
        with tifffile.TiffFile(path) as t:
            p = t.pages[0]; tg = p.tags
            tie, sc = tg['ModelTiepointTag'].value, tg['ModelPixelScaleTag'].value
            gk = list(tg['GeoKeyDirectoryTag'].value)
            ras = 1
            for i in range(4, len(gk), 4):
                if gk[i] == 1025: ras = gk[i + 3]
            arr = p.asarray()
        self.x0, self.y0, self.dx, self.dy = tie[3], tie[4], sc[0], sc[1]
        self.half = 0.5 if ras == 1 else 0.0   # PixelIsArea: tâm ô ở +0,5
        if window:   # (r0, r1, c0, c1)
            r0, r1, c0, c1 = window; arr = arr[r0:r1, c0:c1]; self.x0 += c0 * self.dx; self.y0 -= r0 * self.dy
        self.a = arr

    def rc(self, x, y):
        return (self.y0 - np.asarray(y)) / self.dy - self.half, (np.asarray(x) - self.x0) / self.dx - self.half

    def window_for(self, x0, y0, x1, y1, pad=4):
        r0, c0 = self.rc(x0, y1); r1, c1 = self.rc(x1, y0)
        return int(max(0, np.floor(r0) - pad)), int(min(self.a.shape[0], np.ceil(r1) + pad)), int(max(0, np.floor(c0) - pad)), int(min(self.a.shape[1], np.ceil(c1) + pad))

    def sample(self, x, y, order=1):
        from scipy.ndimage import map_coordinates
        r, c = self.rc(x, y); a = self.a
        if a.ndim == 2:
            return map_coordinates(a.astype(np.float32), [r, c], order=order, mode='nearest')
        return np.stack([map_coordinates(a[..., k].astype(np.float32), [r, c], order=order, mode='nearest') for k in range(a.shape[2])], -1)
