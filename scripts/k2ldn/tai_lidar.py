#!/opt/cine/bin/python
"""TIEN-KY-T4 · LiDAR Composite 1 m của Environment Agency (OGL v3) qua WCS 2.0.1 → ô 1 km GeoTIFF (EPSG:27700) → khảm.
  tai_lidar.py [E0 E1 N0 N1]   (mặc định 529500 535500 179500 182500 = City + Bankside)
Ra: $LDN_DATA/lidar/{dtm,dsm}_<E>_<N>.tif ; khảm {dtm,dsm}_khảm_1m.npy (float32, hàng 0 = bắc) + meta.json. Ngoài git, tái tạo bằng lệnh này."""
import json, os, sys, time, urllib.request, numpy as np
D = os.path.join(os.environ.get('LDN_DATA', '/var/tmp/ldn'), 'lidar'); os.makedirs(D, exist_ok=True)
UA = 'CineLab-research (+https://github.com/HungQuach301/cine-lab)'
SV = {'dtm': ('lidar-composite-digital-terrain-model-dtm-1m', '13787b9a-26a4-4775-8523-806d13af58fc__Lidar_Composite_Elevation_DTM_1m'),
      'dsm': ('lidar-composite-digital-surface-model-first-return-dsm-1m', 'df4e3ec3-315e-48aa-aaaf-b5ae74d7b2bb__Lidar_Composite_Elevation_FZ_DSM_1m')}
def get(u):
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA}), timeout=300) as r: return r.read()
        except Exception as e: err = e; time.sleep(4 * (i + 1))
    raise err
def main(E0=529500, E1=535500, N0=179500, N1=182500):
    import tifffile
    meta = {'nguon': 'Environment Agency LiDAR Composite 1m (2022), Open Government Licence v3', 'bbox27700': [E0, N0, E1, N1], 'sv': SV}
    for k, (svc, cov) in SV.items():
        W, H = E1 - E0, N1 - N0; M = np.full((H, W), np.nan, np.float32)
        for e in range(E0, E1, 1000):
            for n in range(N0, N1, 1000):
                p = os.path.join(D, f'{k}_{e}_{n}.tif')
                if not os.path.exists(p):
                    b = get(f'https://environment.data.gov.uk/spatialdata/{svc}/wcs?service=WCS&version=2.0.1&request=GetCoverage&CoverageId={cov}&format=image/tiff&subset=E({e},{e+1000})&subset=N({n},{n+1000})')
                    open(p, 'wb').write(b)
                a = tifffile.imread(p).astype(np.float32); a[a < -100] = np.nan
                r0 = N1 - (n + 1000); M[r0:r0 + 1000, e - E0:e - E0 + 1000] = a[:1000, :1000]
        np.save(os.path.join(D, f'{k}_kham_1m.npy'), M)
        meta[k] = {'nan_pct': float(np.isnan(M).mean() * 100), 'min': float(np.nanmin(M)), 'max': float(np.nanmax(M))}
        print(k, meta[k])
    json.dump(meta, open(os.path.join(D, 'meta.json'), 'w'), indent=1)
if __name__ == '__main__': main(*map(int, sys.argv[1:5])) if len(sys.argv) > 4 else main()
