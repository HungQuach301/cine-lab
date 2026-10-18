#!/opt/cine/bin/python
"""V5b-2d · DỰNG LẠI đầu vào vector cho hist_borders.py / route_coast.py trong container mới (bộ đệm ngoài git trống).
  - Natural Earth 1:10m (PD) zip (naciscdn.org, cùng URL relief_build.py) → <raw>/ne_10m_land.geojson, ne_10m_minor_islands.geojson
  - <bd>/fr-metro.geojson: nước Pháp CHÍNH QUỐC (NE 1:10m admin_0_countries 'France' cắt theo hộp −6…10°Đ, 41…52°B = bỏ lãnh thổ hải ngoại)
    với tên đúng khoá `giao_ohm` của design/k2v/hist/sm3-1941.json: 'France (metropolitan, NE 1:10m — chỉ để cắt)', không ngày (luôn hiệu lực) → CHỈ ĐỂ CẮT vùng Đức chiếm.
  Cách tạo fr-metro gốc của V5b-2c không được ghi trong repo; đây là tái dựng theo mô tả trong sm3-1941.json ('giao_ohm', 'ghi_cong').
Dùng: bd_raw_prep.py [--ne-zip <thư mục zip NE>] [--raw /var/tmp/cine-out/bd/raw] [--bd /var/tmp/cine-out/bd]"""
import argparse, json, os, subprocess, zipfile, tempfile
import shapefile
from shapely.geometry import shape, mapping, box

NEURL = 'https://naciscdn.org/naturalearth/10m/{k}/{n}.zip'
FR_NAME = 'France (metropolitan, NE 1:10m — chỉ để cắt)'


def get_zip(d, k, n):
    z = os.path.join(d, n + '.zip')
    if not (os.path.exists(z) and os.path.getsize(z) > 0):
        os.makedirs(d, exist_ok=True); subprocess.run(['curl', '-sS', '-f', '-m', '600', '-o', z, NEURL.format(k=k, n=n)], check=True)
    return z


def read(z, n):
    t = tempfile.mkdtemp(prefix='ne_'); zipfile.ZipFile(z).extractall(t)
    r = shapefile.Reader(os.path.join(t, n), encoding='latin1')
    return [dict(type='Feature', properties=sr.record.as_dict(), geometry=sr.shape.__geo_interface__) for sr in r.iterShapeRecords() if sr.shape.points]


def main():
    a = argparse.ArgumentParser(); a.add_argument('--ne-zip', default=os.path.join(os.environ.get('K2V_CACHE', '/var/tmp/cine-out/k2v-cache'), 'ne'))
    a.add_argument('--raw', default='/var/tmp/cine-out/bd/raw'); a.add_argument('--bd', default='/var/tmp/cine-out/bd'); A = a.parse_args()
    os.makedirs(A.raw, exist_ok=True)
    for n in ('ne_10m_land', 'ne_10m_minor_islands'):
        F = read(get_zip(A.ne_zip, 'physical', n), n)
        json.dump(dict(type='FeatureCollection', features=F), open(os.path.join(A.raw, n + '.geojson'), 'w'), separators=(',', ':')); print('ghi', n, len(F))
    F = [f for f in read(get_zip(A.ne_zip, 'cultural', 'ne_10m_admin_0_countries'), 'ne_10m_admin_0_countries') if f['properties'].get('ADMIN') == 'France']
    g = shape(F[0]['geometry']); g = (g if g.is_valid else g.buffer(0)).intersection(box(-6.0, 41.0, 10.0, 52.0))
    json.dump(dict(type='FeatureCollection', features=[dict(type='Feature', properties={'name': FR_NAME, 'name:en': FR_NAME, 'nguon': 'Natural Earth 1:10m admin_0_countries ADMIN=France ∩ hộp [-6,41,10,52] (PD)'}, geometry=mapping(g))]),
              open(os.path.join(A.bd, 'fr-metro.geojson'), 'w'), ensure_ascii=False); print('ghi fr-metro', g.bounds, round(g.area, 2))


if __name__ == '__main__':
    main()
