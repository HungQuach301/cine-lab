#!/opt/cine/bin/python
"""Đóng gói lớp Natural Earth (PD) cho BD-5/BD-6 (phiên K, 1.14.0). Chỉ phiên K chạy; luật đọc tệp .npz đã khoá SHA trong LOCK.

  ne_build.py <ne_10m_admin_0_disputed_areas.geojson> <ne_10m_land.geojson> <thư mục ra>

Định dạng .npz: lượng tử 1e-5° (≈ 1,1 m, dưới sai số 1:10m), mỗi vòng (ring) = int32 điểm đầu + int32 sai phân.
  ring_off[k]: chỉ số điểm đầu vòng k trong xy; ring_poly[k]: polygon chứa vòng k; poly_feat[p]: feature chứa polygon p.
  disputed còn `ten` (BRK_NAME) theo feature. Toạ độ khôi phục bằng q_bando._ne_load().
"""
import json, sys
import numpy as np

Q = 1e5


def pack(path, name_key=None):
    G = json.load(open(path)); xy, roff, rpoly, pfeat, names = [], [], [], [], []
    for fi, f in enumerate(G['features']):
        g = f['geometry']; P = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        names.append(str((f.get('properties') or {}).get(name_key) or '') if name_key else '')
        for poly in P:
            pid = len(pfeat); pfeat.append(fi)
            for ring in poly:
                roff.append(sum(len(a) for a in xy)); rpoly.append(pid)
                a = np.round(np.asarray(ring, float)[:, :2] * Q).astype(np.int64)
                d = np.vstack([a[:1], np.diff(a, axis=0)]); xy.append(d.astype(np.int32))
    return dict(xy=np.vstack(xy), ring_off=np.asarray(roff, np.int64), ring_poly=np.asarray(rpoly, np.int32),
                poly_feat=np.asarray(pfeat, np.int32), ten=np.asarray(names))


if __name__ == '__main__':
    if len(sys.argv) != 4: sys.exit(__doc__)
    np.savez_compressed(f'{sys.argv[3]}/ne10m-disputed.npz', **pack(sys.argv[1], 'BRK_NAME'))
    np.savez_compressed(f'{sys.argv[3]}/ne10m-land.npz', **pack(sys.argv[2]))
