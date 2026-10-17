#!/var/tmp/cine-out/segvenv/bin/python
"""KÊNH 2 · ẢNH HÀNG KHÔNG cho ZOOM NHIỀU TẦNG (Kinh thánh §4, F4 — chủ dự án duyệt 14/10/2026 22:11; phiên V4).
Nguồn: USDA NAIP (National Agriculture Imagery Program) qua dịch vụ ảnh USGS The National Map `USGSNAIPPlus` (ArcGIS ImageServer, exportImage).
NAIP do USDA FSA thu — tác phẩm chính phủ Mỹ, tài sản công (giấy phép đọc ngày 14/10/2026: channel-k2/k2v4-mau/licenses/NAIP.txt; RIGHTS.md K2V4-AER-*).
Chạy bằng venv /var/tmp/cine-out/segvenv (cần scikit-image cho Lab). Media KHÔNG commit: ảnh tầng ở $K2V_CACHE/aerial/<tên>/t<i>.png (RGBA: ô không có ảnh → trong suốt); SHA + tham số ghi vào <tên>/meta.json và channel-k2/k2v4-mau/aerial-<tên>-meta.json (commit).

  aerial.py fetch --name lockport --center -78.6906,43.1703 --tiers 48:2048,9:2048,1.6:2048 [--relief erie] [--match 0.6]
     mỗi tầng 'km:px' = ô vuông cạnh km quanh tâm, px điểm ảnh (exportImage, EPSG:4326 → bbox theo độ, ô vuông theo km thật).
     --match a: chuyển màu (Reinhard trên Lab) tầng xa nhất về phía bảng màu TỰ NHIÊN của nền relief cùng vùng với độ mạnh a (0..1),
                các tầng gần chuyển theo cùng phép biến đổi → nối tầng không nhảy màu. Chỉ chỉnh màu toàn cục, không vẽ thêm gì.
"""
import hashlib, io, json, math, os, sys, time, urllib.parse, urllib.request
import numpy as np
from PIL import Image

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
CACHE = os.environ.get('K2V_CACHE', '/var/tmp/cine-out/k2v-cache')
SVC = 'https://imagery.nationalmap.gov/arcgis/rest/services/USGSNAIPPlus/ImageServer'
UA = 'cine-lab/1.0 (channel research)'


def arg(k, d=None):
    return sys.argv[sys.argv.index('--' + k) + 1] if '--' + k in sys.argv else d


def sha(b):
    return hashlib.sha256(b).hexdigest()


def get(url, tries=4):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=120) as r: return r.read()
        except Exception as e:
            if i == tries - 1: raise
            time.sleep(2 ** (i + 1))


def bbox_km(lon, lat, km):
    dlat = km / 2 / 110.57; dlon = km / 2 / (111.32 * math.cos(math.radians(lat))); return [lon - dlon, lat - dlat, lon + dlon, lat + dlat]


def export(bb, px):
    q = dict(bbox=','.join(f'{v:.6f}' for v in bb), bboxSR=4326, imageSR=4326, size=f'{px},{px}', format='jpgpng', f='image', interpolation='RSP_BilinearInterpolation')
    return get(SVC + '/exportImage?' + urllib.parse.urlencode(q))


def acq(bb):
    """năm/độ phân giải NAIP tại tâm ô (identify → catalog item)"""
    lon, lat = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
    q = dict(geometry=json.dumps({'x': lon, 'y': lat, 'spatialReference': {'wkid': 4326}}), geometryType='esriGeometryPoint', returnCatalogItems='true', returnGeometry='false', f='json')
    try:
        j = json.loads(get(SVC + '/identify?' + urllib.parse.urlencode(q))); items = (j.get('catalogItems') or {}).get('features') or []
        return [{k: v for k, v in it.get('attributes', {}).items() if k.lower() in ('name', 'year', 'acquisitiondate', 'acq_date', 'lowps', 'highps', 'resolution', 'state', 'productname', 'category', 'srcdate', 'dataset_name')} for it in items[:6]]
    except Exception as e:
        return [{'loi': str(e)[:200]}]


def lab(a):
    from skimage import color
    return color.rgb2lab(a / 255.0)


def unlab(L):
    from skimage import color
    return np.clip(color.lab2rgb(L) * 255, 0, 255)


def main():
    if sys.argv[1] != 'fetch': sys.exit(__doc__)
    name = arg('name'); lon, lat = map(float, arg('center').split(',')); out = os.path.join(CACHE, 'aerial', name); os.makedirs(out, exist_ok=True)
    tiers = [tuple(map(float, t.split(':'))) for t in arg('tiers').split(',')]; strength = float(arg('match', 0.6)); M = dict(name=name, center=[lon, lat], service=SVC, tiers=[])
    tf = None
    for i, (km, px) in enumerate(tiers):
        bb = bbox_km(lon, lat, km); rf = os.path.join(out, f't{i}-raw.jpg')
        raw = open(rf, 'rb').read() if os.path.exists(rf) and '--cached' in sys.argv else export(bb, int(px)); open(rf, 'wb').write(raw)
        im = Image.open(io.BytesIO(raw)).convert('RGB'); a = np.asarray(im, np.float32)
        from scipy import ndimage
        nod = a.sum(2) < 20; lb, nn = ndimage.label(nod)
        if nn: sz = ndimage.sum(nod, lb, range(1, nn + 1)); nod = np.isin(lb, 1 + np.nonzero(sz >= 0.001 * nod.size)[0])   # chỉ vùng trống lớn; bóng đen nhỏ trong ảnh giữ nguyên
        nod = ndimage.binary_dilation(nod, iterations=4)   # ô không có ảnh (mặt hồ ngoài vùng NAIP) = đen → trong suốt, mép mờ
        alpha = np.clip(1 - ndimage.gaussian_filter(nod.astype(np.float32), 10) * 1.6, 0, 1) * (~nod); valid = ~nod
        if i == 0 and arg('relief'):   # phép chuyển màu: thống kê Lab tầng xa → thống kê Lab nền relief TỰ NHIÊN cùng ô (bảng màu kênh)
            rm = json.load(open(os.path.join(CACHE, 'relief', arg('relief'), 'meta.json'))); R = Image.open(os.path.join(CACHE, 'relief', arg('relief'), 'natural.jpg'))
            L0, A0, L1, A1 = rm['bbox']; W, H = R.size; box = ((bb[0] - L0) / (L1 - L0) * W, (A1 - bb[3]) / (A1 - A0) * H, (bb[2] - L0) / (L1 - L0) * W, (A1 - bb[1]) / (A1 - A0) * H)
            ref = lab(np.asarray(R.crop(tuple(round(v) for v in box)).resize(a.shape[1::-1], Image.BILINEAR).convert('RGB'), np.float32)); src = lab(a)
            mu_s, sd_s, mu_r, sd_r = src[valid].mean(0), src[valid].std(0), ref[valid].mean(0), ref[valid].std(0)   # chỉ vùng có ảnh, cùng vùng trên nền relief
            k = sd_r / np.maximum(sd_s, 1e-3); k[0] = max(k[0], 0.85)   # giữ tương phản sáng của ảnh (không làm bệt chi tiết)
            tf = dict(mu_s=mu_s.tolist(), mu_r=mu_r.tolist(), k=k.tolist(), strength=strength)
        if arg('relief'):   # mặt nước lấy theo nền relief (Natural Earth): nước → trong suốt, để hồ/sông của bản đồ hiện qua; ranh ảnh NAIP trên mặt hồ không lộ khối
            rm = json.load(open(os.path.join(CACHE, 'relief', arg('relief'), 'meta.json'))); R = Image.open(os.path.join(CACHE, 'relief', arg('relief'), 'natural.jpg')); L0, A0, L1, A1 = rm['bbox']; W, H = R.size
            box = ((bb[0] - L0) / (L1 - L0) * W, (A1 - bb[3]) / (A1 - A0) * H, (bb[2] - L0) / (L1 - L0) * W, (A1 - bb[1]) / (A1 - A0) * H)
            rc = np.asarray(R.crop(tuple(round(v) for v in box)).resize(a.shape[1::-1], Image.BILINEAR).convert('RGB'), np.float32)
            wat = ndimage.binary_opening(((rc[..., 2] > rc[..., 0] + 12) & (rc[..., 2] >= rc[..., 1] - 4)) | ((a[..., 2] > a[..., 1] + 4) & (a[..., 2] > a[..., 0] + 12)), iterations=3)   # nước theo relief HOẶC theo màu ảnh (xanh lam)
            lab_, nw = ndimage.label(wat)
            if nw: sz = ndimage.sum(wat, lab_, range(1, nw + 1)); wat = np.isin(lab_, 1 + np.nonzero(sz >= 0.002 * wat.size)[0])   # chỉ mặt nước lớn (hồ, sông rộng) — mái nhà xanh, bóng đổ không tính
            if wat.mean() > 0.002: wa = np.clip(1 - ndimage.gaussian_filter(ndimage.binary_dilation(wat, iterations=3).astype(np.float32), 6) * 1.3, 0, 1); alpha = alpha * wa
        if tf:
            L = lab(a); T = (L - np.array(tf['mu_s'])) * np.array(tf['k']) + np.array(tf['mu_r']); L2 = L + strength * (T - L); a = unlab(L2)
        fp = os.path.join(out, f't{i}.png'); Image.fromarray(np.dstack([a, alpha * 255]).astype(np.uint8), 'RGBA').save(fp, optimize=False, compress_level=3)
        M['tiers'].append(dict(i=i, km=km, px=int(px), m_per_px=round(km * 1000 / px, 2), bbox=[round(v, 6) for v in bb], raw_sha256=sha(raw), sha256=sha(open(fp, 'rb').read()), file=f't{i}.png', nodata_pct=round(100 * float(nod.mean()), 1), naip=acq(bb)))
        print(json.dumps(M['tiers'][-1], ensure_ascii=False), file=sys.stderr)
    M['color_match'] = tf; M['license'] = 'USDA FSA NAIP — public domain (U.S. Government work); xem channel-k2/k2v4-mau/licenses/NAIP.txt'
    json.dump(M, open(os.path.join(out, 'meta.json'), 'w'), indent=1)
    dst = os.path.join(REPO, arg('meta-dir', 'channel-k2/k2v4-mau'), f'aerial-{name}-meta.json')   # T2: --meta-dir <thư mục tập> (không ghi vào cuộn V4)
    os.makedirs(os.path.dirname(dst), exist_ok=True); json.dump(M, open(dst, 'w'), indent=1, ensure_ascii=False)
    print(json.dumps(M, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
