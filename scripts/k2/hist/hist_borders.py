#!/opt/cine/bin/python
"""V5b-2c · M13-lite — CHUẨN HOÁ RANH GIỚI LỊCH SỬ cho bản đồ chiến lược (tổng quát hoá reports/nc-ban-do/py/{clio,ohm_build,cmp}.py của NC-BD).

Một tệp đặc tả lớp (JSON) → raster cho relief.js (opt.borders) + manifest BD-4 cho K + dòng ghi công:
  1. LỌC theo năm/ngày: Cliopatria v0.2.1 (FromYear ≤ năm ≤ ToYear) · OHM (start_date ≤ ngày < end_date; tệp đã ghép polygon của NC-BD hoặc Overpass)
  2. CẮT theo đất Natural Earth 1:10m (land + minor islands) trong bbox (biển không tô — ranh "3 hải lý" của OHM bị bỏ)
  3. ĐƠN GIẢN theo km/px của khung đầu ra (dung sai 0,5 px)
  4. lãnh thổ có cạnh bao lớn nhất < 8 px ở khung đầu ra → ĐIỂM (không vẽ polygon; B5/BD-5b)
  5. ĐO LỆCH hai nguồn: trung bình khoảng cách điểm biên TRÊN ĐẤT (không tính bờ biển) của nguồn chính → biên nguồn đối chiếu, đổi ra px ở khung đầu ra
     (LAEA EPSG:3035); > 4 px → kieu_mep 'mem' (mép mềm 8–12 px) (B5/BD-4)
  6. CHỈNH TAY theo claim (đặc tả `sua`): gộp/đổi tên, tách đảo đổi chủ theo ngày (Minorca 1782-02-05, T020), bỏ thực thể sai thời điểm
Ra (<out>/): idx.png (RGB = chỉ số thực thể + 1, 0 = không thuộc ai/biển), edge.png (khoảng cách tới biên gần nhất, 0..255 = 0..25,5 px raster),
  entities.json (chỉ số → tên, phe, màu, kiểu, đổi chủ theo ngày), points.json, lop-ranh.json (manifest BD-4), meta.json (bbox, cỡ, SHA nguồn).
Dùng: hist_borders.py <dac-ta.json> --out <thư mục> [--clio <cliopatria_polities_only_v021.geojson>] [--ne <thư mục NE geojson>]"""
import argparse, hashlib, json, math, os, sys, warnings
import numpy as np
from PIL import Image
from scipy import ndimage
import shapely
from shapely.geometry import shape, box, mapping, Point
from shapely.ops import unary_union
from pyproj import Transformer
warnings.filterwarnings('ignore')
T3035 = Transformer.from_crs(4326, 3035, always_xy=True)


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def proj(g): return shapely.ops.transform(T3035.transform, g)


def load_clio(path, year, bb):
    out = {}
    for f in json.load(open(path))['features']:
        p = f['properties']
        if not (p['FromYear'] <= year <= p['ToYear']): continue
        g = shape(f['geometry']); g = g if g.is_valid else g.buffer(0)
        if g.intersects(bb): out.setdefault(p['Name'], []).append(g)
    return {k: unary_union(v) for k, v in out.items()}


def load_ohm(path, date, bb):
    out = {}
    for f in json.load(open(path))['features']:
        p = f['properties']; s, e = str(p.get('start_date') or '0000'), str(p.get('end_date') or '9999')
        if not (s[:len(date)] <= date < e.ljust(len(date), '9') if len(e) < len(date) else s <= date < e): continue
        g = shape(f['geometry']); g = g if g.is_valid else g.buffer(0)
        if g.intersects(bb): out.setdefault(p.get('name:en') or p.get('name'), []).append(g)
    return {k: unary_union(v) for k, v in out.items()}


def main():
    a = argparse.ArgumentParser(); a.add_argument('spec'); a.add_argument('--out', required=True)
    a.add_argument('--clio', default='/var/tmp/cine-out/bd/raw/clio/cliopatria_polities_only_v021.geojson'); a.add_argument('--ne', default='/var/tmp/cine-out/bd/raw')
    A = a.parse_args(); S = json.load(open(A.spec)); os.makedirs(A.out, exist_ok=True)
    bb = box(*S['bbox']); lon0, lat0, lon1, lat1 = S['bbox']; RW = S.get('raster_w', 3000); RH = round(RW * (lat1 - lat0) / (lon1 - lon0) / math.cos(math.radians((lat0 + lat1) / 2)))
    kmpx = S['khung_rong_km'] / S.get('khung_px', 1920)   # km / px ở khung đầu ra 1080p
    tol_deg = 0.5 * kmpx / 111.0
    land = unary_union([shape(f['geometry']) for n in ('ne_10m_land', 'ne_10m_minor_islands') for f in json.load(open(os.path.join(A.ne, n + '.geojson')))['features'] if shape(f['geometry']).intersects(bb)]).intersection(bb)
    P = load_clio(A.clio, S['nam'], bb); Q = load_ohm(S['doi_chieu']['tep'], S['doi_chieu']['ngay'], bb) if S.get('doi_chieu') else {}
    for extra in S.get('cat_them', []): Q.update(load_ohm(extra, S['doi_chieu']['ngay'], bb))   # hình cắt phụ (vd nước Pháp chính quốc NE 1:10m — chỉ để cắt vùng chiếm đóng, không vẽ)
    print('[hist] Cliopatria', S['nam'], sorted(P)); print('[hist] OHM', S.get('doi_chieu', {}).get('ngay'), sorted(Q))
    ents, pts, manifest, log = [], [], [], []
    taken = shapely.Polygon()
    for i, E in enumerate(S['thuc_the']):
        if E.get('diem'): continue
        g = unary_union([P[n] for n in E.get('cliopatria', []) if n in P]) if E.get('cliopatria') else None
        if E.get('ll'): g = shapely.geometry.Polygon(E['ll'])   # hình học cho trước (vd hộp đảo) → cắt theo đất
        if g is None or g.is_empty: log.append(f"BỎ {E['id']}: không có hình học"); continue
        if E.get('giao_ohm') and Q: g = g.intersection(unary_union([Q[n] for n in E['giao_ohm'] if n in Q]))   # vd vùng Đức chiếm ở PHÁP = 'Nazi Germany' (Cliopatria) ∩ 'French State' (OHM)
        if E.get('giao_ll'): g = g.intersection(shapely.geometry.Polygon(E['giao_ll']))   # vd phần châu Phi của 'Francoist Spain' = Ma-rốc thuộc TBN (tô pha 85 %)
        if E.get('tru_cliopatria'): g = g.difference(unary_union([P[n] for n in E['tru_cliopatria'] if n in P] or [shapely.Polygon()]))
        g = g.intersection(land)
        for m in E.get('tru', []): g = g.difference(shapely.geometry.Polygon(m))   # vd bỏ đảo Minorca khỏi Tây Ban Nha (đảo là thực thể riêng)
        g = g.difference(taken); taken = taken.union(g)
        g = g.simplify(tol_deg, preserve_topology=True)
        if g.is_empty: continue
        bx = g.bounds; side_px = max((bx[2] - bx[0]) * 111.32 * math.cos(math.radians((bx[1] + bx[3]) / 2)), (bx[3] - bx[1]) * 110.57) / kmpx
        # đo lệch hai nguồn: biên TRÊN ĐẤT (bỏ phần trùng bờ biển ± 2 km)
        lech = None
        if E.get('ohm') and Q:
            h = unary_union([Q[n] for n in E['ohm'] if n in Q])
            if not h.is_empty:
                cb = box(*S['doi_chieu'].get('bbox', S['bbox'])).intersection(bb)   # vùng CHUNG hai nguồn (mẫu OHM có bbox riêng): bỏ cạnh hộp cắt nhân tạo
                if E.get('vung_do'): cb = cb.intersection(unary_union([box(*b) for b in E['vung_do']]))   # đo theo HÀNH LANG biên đang kể (vd Tây Ban Nha–Bồ Đào Nha): khác biệt ở chỗ khác (presidio Oran) ghi riêng
                gg, h = g.intersection(cb), h.intersection(land).intersection(cb); coast = proj(land.boundary).buffer(2000).union(proj(cb.boundary).buffer(5000))
                la = proj(gg.boundary).difference(coast); lb = proj(h.boundary).difference(coast)
                oth = unary_union([v for k, v in P.items() if k not in E.get('cliopatria', [])]).intersection(land)   # chỉ biên GIỮA HAI THỰC THỂ (bỏ bờ biển/cửa sông Cliopatria vẽ lệch NE)
                la = la.intersection(proj(oth).buffer(3000))
                if not la.is_empty and not lb.is_empty:
                    cs = shapely.get_coordinates(la)[::3]; d = [lb.distance(Point(c)) for c in cs]
                    lech = dict(tb_km=round(float(np.mean(d)) / 1000, 2), max_km=round(float(np.max(d)) / 1000, 2), n_diem=len(d), lech_tb_px=round(float(np.mean(d)) / 1000 / kmpx, 2), lech_max_px=round(float(np.max(d)) / 1000 / kmpx, 1))
                    lech['dt_lech_pct'] = round(proj(gg).symmetric_difference(proj(h)).area / max(1, proj(gg).area) * 100, 1)
        kieu_mep = E.get('kieu_mep') or ('mem' if lech and lech['lech_tb_px'] > 4 else 'lien')
        ents.append(dict(id=E['id'], ten=E['ten'], faction_id=E['faction_id'], fill=E['mau'], ve=E.get('ve', 'dac'), ban_dia=E.get('ban_dia', False), doi_chu=E.get('doi_chu', []),
                         geom=g, side_px=round(side_px, 1), kieu_mep=kieu_mep, lech=lech, claims=E.get('claims', [])))
        if side_px < 8: log.append(f"CẢNH BÁO {E['id']}: cạnh {side_px:.1f} px < 8 → nên là ĐIỂM")
    for E in S['thuc_the']:
        if E.get('diem'): pts.append(dict(id=E['id'], ten=E['ten'], ll=E['diem'], faction_id=E['faction_id'], fill=E['mau'], doi_chu=E.get('doi_chu', []), claims=E.get('claims', []), ly_do=E.get('ly_do_diem', '< 8 px ở khung đầu ra')))
    # raster: chỉ số thực thể + khoảng cách tới biên (px raster)
    from PIL import ImageDraw
    idx = Image.new('RGB', (RW, RH), (0, 0, 0)); dr = ImageDraw.Draw(idx)
    X = lambda lo, la: ((lo - lon0) / (lon1 - lon0) * RW, (lat1 - la) / (lat1 - lat0) * RH)
    for k, e in enumerate(ents):
        col = ((k + 1) & 255, ((k + 1) >> 8) & 255, 0)
        for poly in (e['geom'].geoms if hasattr(e['geom'], 'geoms') else [e['geom']]):
            if poly.geom_type != 'Polygon': continue
            dr.polygon([X(*c) for c in poly.exterior.coords], fill=col)
            for hole in poly.interiors: dr.polygon([X(*c) for c in hole.coords], fill=(0, 0, 0))
    I = np.asarray(idx)[..., 0].astype(np.int32) + (np.asarray(idx)[..., 1].astype(np.int32) << 8)
    edge = np.zeros(I.shape, bool); edge[:, 1:] |= I[:, 1:] != I[:, :-1]; edge[1:, :] |= I[1:, :] != I[:-1, :]
    both = edge & (I > 0)   # chỉ biên giữa hai thực thể hoặc thực thể ↔ không thuộc ai trên ĐẤT; bờ biển (thực thể ↔ biển) không vẽ thành nét ranh
    landm = np.asarray(Image.new('L', (RW, RH)))
    lm = Image.new('L', (RW, RH), 0); dl = ImageDraw.Draw(lm)
    for poly in (land.geoms if hasattr(land, 'geoms') else [land]):
        if poly.geom_type == 'Polygon': dl.polygon([X(*c) for c in poly.exterior.coords], fill=255)
    L = np.asarray(lm) > 0; inner = ndimage.binary_erosion(L, iterations=2)
    border = edge & inner
    D = ndimage.distance_transform_edt(~border); Image.fromarray(np.clip(D * 10, 0, 255).astype(np.uint8)).save(os.path.join(A.out, 'edge.png'))
    idx.save(os.path.join(A.out, 'idx.png'))
    E_json = [dict({k: v for k, v in e.items() if k != 'geom'}, i=k + 1) for k, e in enumerate(ents)]
    json.dump(dict(entities=E_json, points=pts), open(os.path.join(A.out, 'entities.json'), 'w'), ensure_ascii=False, indent=1)
    # manifest BD-4 (định dạng K-1.14 §3.2/§9: lop-ranh.json)
    lop = dict(id=S['id'], loai='bien_gioi_lich_su', nam=S['nam'], ngay=S.get('ngay_ranh'), nguon=S['nguon_ngan'], nguon_doi_chieu=S.get('doi_chieu', {}).get('ten'), giay_phep=S['giay_phep'],
               giay_phep_doi_chieu=S.get('doi_chieu', {}).get('giay_phep'), nhan=S['nhan'], khung_rong_km=S['khung_rong_km'], km_px=round(kmpx, 3),
               lech_tb_px=max([e['lech']['lech_tb_px'] for e in ents if e['lech']] or [0]), kieu_mep='mem' if any(e['kieu_mep'] == 'mem' for e in ents) else 'lien',
               features=[dict(id=e['id'], ten=e['ten'], faction_id=e['faction_id'], fill=e['fill'], ve=e['ve'], ban_dia=e['ban_dia'], side_px=e['side_px'], kieu_mep=e['kieu_mep'], lech=e['lech'], doi_chu=e['doi_chu'], claims=e['claims']) for e in ents],
               diem=pts, chinh_tay=S.get('chinh_tay', []), ghi_cong=S['ghi_cong'], log=log)
    json.dump(lop, open(os.path.join(A.out, 'lop-ranh.json'), 'w'), ensure_ascii=False, indent=1)
    meta = dict(bbox=S['bbox'], raster=[RW, RH], km_px_khung=kmpx, nguon=dict(cliopatria=dict(tep=os.path.basename(A.clio), nam=S['nam']), ohm=S.get('doi_chieu')), ne_sha={n: sha(os.path.join(A.ne, n + '.geojson')) for n in ('ne_10m_land', 'ne_10m_minor_islands')})
    json.dump(meta, open(os.path.join(A.out, 'meta.json'), 'w'), ensure_ascii=False, indent=1)
    # GeoJSON đã chỉnh (để kiểm/ xem trước; lớp vẽ thật là raster)
    json.dump(dict(type='FeatureCollection', features=[dict(type='Feature', properties=dict(id=e['id'], ten=e['ten'], faction_id=e['faction_id']), geometry=mapping(shapely.set_precision(e['geom'], 1e-4))) for e in ents]), open(os.path.join(A.out, 'ranh.geojson'), 'w'))
    for e in ents: print(f"  {e['id']:12} {e['ten'][:26]:26} {e['faction_id']:10} cạnh {e['side_px']:7.1f} px  mép {e['kieu_mep']:4}  lệch {e['lech']}")
    for p in pts: print('  ĐIỂM', p['id'], p['ten'], p['ll'])
    for l in log: print(' ', l)


if __name__ == '__main__':
    main()
