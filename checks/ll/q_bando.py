#!/opt/cine/bin/python
"""BD-1…BD-8 luật "bản đồ chiến lược" + inset + ranh giới lịch sử — bản 1.14.0 (phiên K, 17/10/2026). Mặc định CHỈ BÁO trong k2check
(cấp: cap112.py; đề xuất mức cuối: reports/K-1.14-BAO-CAO.md). Căn cứ: reports/NC-BAN-DO-BAO-CAO.md §3, §3.4 (origin/nc-ban-do @83dca2d5);
chủ dự án duyệt B1–B8 ngày 17/10 (B4: inset GÓC TRÊN TRÁI). Định nghĩa: checks/ll/RULES-LL.md mục "1.14".

  q_bando.py <episode.yaml> --tl <timeline.json> [--logs <thư mục *.log.json của k2.js>] [--json ra.json]

ĐẦU VÀO (đường dẫn tương đối thư mục episode.yaml; khối `ban_do:` của episode.yaml):
  shot `type: strategic` (đặc tả shot; `p.*` cũng nhận): `nghieng` (độ, ≤ 30), `be_ngang_km` (số hoặc [đầu, cuối], 300–5 000),
    `dong` [{loai: route|arrow|fleet|front|blockade, t: [a, b]}] (giây trong shot), `chu_giai` [{faction_id, mau, nhan}], `chi_toi` [tên nơi],
    `lop` [id lớp ranh hiện trong shot], `nam`/`year`/`dem_ngay` (nhãn mốc thời gian, khi không có log chữ).
  ban_do.lop    manifest lớp ranh JSON {W: 1920, lop: [{id, loai: bien_gioi_lich_su|bien_gioi_hien_dai|…, nam, nguon, nguon_doi_chieu,
                lech_tb_px, giay_phep, kieu_mep, km_px | be_ngang_km, shot: ["seg/i"], t: [a, b] (giây trong shot), hinh: <geojson> | features}]}.
                Feature: properties faction_id, fill (#rrggbb | gach:#…,#…), fill_the, ten, ban_dia (bool), ve (diem|polygon).
  ban_do.tuyen  routes.geojson: LineString/MultiLineString đã vẽ (toạ độ dày theo đường thật trên hình), properties {id, mode: sea|land|air,
                claims: [id], cang: [[lon, lat], …]}. Đầu và cuối tuyến luôn là cảng.
  ban_do.inset  log 2D inset JSON {W, H, inset: [{id, t: [a, b] (giây phim), box: [x0, y0, x1, y1] | khung: [{t, box}], inset_goc, ly_do}]}.
  ban_do.claims claims.json ({claims: [{id, …}]} hoặc danh sách) để BD-6 (c) kiểm id có thật.
  --logs        log chữ k2.js (`<đoạn>.log.json`: text [{f, items [{s (≤ 40 ký tự), cap, box [x0, y0, x1, y1]}], occ?}]); px = cap / 0,727.
  Natural Earth 1:10m (PD) đóng gói trong checks/ll/data/ (ne_build.py; nguồn + SHA ở data/NGUON.md): disputed (BD-5), land (BD-6).

BD-1 Tỷ trọng + định nghĩa (shot type strategic). (a) tổng > STRAT_PCT % thời lượng phim; (b) một shot > STRAT_S s; (c) > STRAT_CH shot/chương
     (chương = `chuong` của đoạn, không có → id đoạn); (d) hai shot strategic liền nhau; (e) ngoài định nghĩa: thiếu/sai `nghieng` ≤ 30°,
     `be_ngang_km` 300–5 000, hoặc cảnh map/globe; (f) thiếu bắt buộc: nhãn mốc thời gian (log: chữ CHỈ là năm/ngày/"Day n" — TIME_RE; không log: p.nam/
     year/dem_ngay), chú giải ≤ 3 phe (đếm faction_id của chu_giai ∪ lớp trong shot), shot kề trước/sau CÙNG chương là cảnh 3D (scene3d/timelapse/
     relief) tại một nơi trong `chi_toi`. Shot strategic ĐẠT (e) mới được loại khỏi NC-H2/NC-H3 (q_noi.py); không bao giờ là "thành phố" (NC-H1).
BD-2 Chuyển động. Mỗi shot strategic có ≥ 1 phần tử `dong` bắt đầu ≤ MOVE_T0 s và chạy ≥ MOVE_PCT % thời lượng shot.
BD-3 Nhãn ranh. Mỗi shot có lớp `bien_gioi_lich_su`: trong các khung log của khoảng lớp hiện, ≥ LBL_PCT % khung có chữ khớp LBL_RE cỡ ≥ LBL_PX px.
     (c) năm trong nhãn ≠ `nam` của lớp (K thêm, đề xuất). Không có log của đoạn → THIẾU.
BD-4 Manifest lớp ranh. Lớp bien_gioi_lich_su: (a) đủ nam, nguon, nguon_doi_chieu, lech_tb_px, giay_phep; (b) giay_phep ∈ LICENSES;
     (c) lech_tb_px > EDGE_PX → kieu_mep ∈ {mem, gach}; (d) nguon_doi_chieu ≠ nguon. Shot trỏ lớp không có trong manifest → (a).
BD-5 Tranh chấp hiện đại. (a) lớp bien_gioi_hien_dai ∩ (NE disputed ⊕ DISP_KM km) = ∅ (giao hình học: đỉnh trong polygon, cắt cạnh, hoặc
     khoảng cách đoạn–đoạn ≤ DISP_KM); (b) lãnh thổ (polygon, ve ≠ diem) có bbox lớn nhất < SMALL_PX px ở km_px của lớp → phải vẽ điểm.
BD-6 Tuyến biển. (a) tuyến mode sea ∩ đất NE 1:10m, trừ PORT_KM km quanh cảng = ∅; (b) mỗi tuyến ≥ 1 claim id; (c) claim id có trong claims.
BD-7 Màu phe. (a) cùng faction_id → một mã màu trong cả tập (lớp + chú giải); (b) fill là cờ/biểu tượng (fill_the ∈ FLAG_TAGS); (c) B8: thực thể
     bản địa có tên (ban_dia + ten) mà fill rỗng/trong suốt/trùng màu đất trống của lớp (`nen_trong`) — chỉ báo khi manifest có.
BD-8 Inset. (a) bbox > INSET_PCT % khung; (b) không nằm GÓC TRÊN TRÁI trong vùng an toàn SAFE (trên phải chỉ khi inset_goc: tren_phai + ly_do);
     (c) thời lượng ngoài INSET_S; (d) giao hộp chữ (chip nơi, dòng nguồn, nhãn…) hoặc LL.occ của khung log (hộp nằm trọn trong inset là chữ của
     inset, không tính); (e) trong shot liên hoàn (`lien_hoan`), thẻ số (card), ảnh lưu trữ (photo/document/record/footage) hoặc ≤ CUT_S s sau
     cắt cứng (shot `in.type` cut/không khai; đầu đoạn không fadeIn).
Trong ±5 % quanh ngưỡng: nêu tên (sat_nguong).
"""
import glob, json, math, os, re, sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

STRAT_PCT, STRAT_S, STRAT_CH, TILT_MAX, WIDTH_KM = 15.0, 8.0, 2, 30.0, (300.0, 5000.0)   # B3 (chủ dự án 17/10)
MOVE_T0, MOVE_PCT, LEGEND_MAX = 1.5, 60.0, 3
LBL_RE = re.compile(r'^approx\. borders c\. (\d{3,4}) — .+')                                # B5 / BD-3
LBL_PX, LBL_PCT, CAP_RATIO = 38.0, 95.0, 0.727
LICENSES, EDGE_PX, EDGE_KIEU = {'CC0', 'PD', 'CC-BY-4.0'}, 4.0, {'mem', 'gach'}
DISP_KM, SMALL_PX, PORT_KM = 10.0, 8.0, 5.0
FLAG_TAGS = {'co', 'co_lich_su', 'bieu_tuong', 'ton_giao', 'cuc_doan', 'flag', 'symbol'}
INSET_PCT, SAFE, INSET_S, CUT_S = 12.0, 0.05, (2.5, 4.0), 2.0                               # B4
MOVE_KINDS = {'route', 'arrow', 'fleet', 'front', 'blockade'}
SOFT_IN = {'dissolve', 'fade', 'hoa', 'zoom', 'mix', 'xfade', 'wipe'}
ARCHIVE = {'photo', 'document', 'record', 'footage'}
KY = 110.574
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
MON = r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?'
TIME_RE = re.compile(r'^\s*(?:c\.\s*)?(?:\d{1,2}\s+' + MON + r'\s+|' + MON + r'\s+(?:\d{1,2},?\s+)?)?\d{3,4}(?:\s*[–—-]\s*\d{2,4})?\s*$'
                     r'|^\s*day\s+[\d,]+\b', re.I)   # nhãn mốc thời gian = chữ CHỈ là năm/ngày/bộ đếm ngày (dòng nguồn có năm không tính)


def mmss(t): return f'{int(t // 60)}:{t % 60:04.1f}'


def _n(v): return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def r(ok, loi=None, thieu=None, val='', **kw):
    loi = loi or []; thieu = thieu or []
    if thieu and not loi and 'ket_qua' not in kw: kw['ket_qua'] = 'THIẾU'
    return dict(ok=ok and not loi and not thieu, loi=loi, thieu=thieu, val=val, note='; '.join((loi + thieu)[:5]), **kw)


def _sat(name, v, thr):
    return [f'{name} {v} (ngưỡng {thr})'] if thr and abs(v - thr) <= 0.05 * abs(thr) else []


def khong_ap(why): return r(True, val=why, ket_qua='KHÔNG ÁP')


# ================================================================ shot strategic
def get(spec, p, o, k):
    for d in (spec, (spec or {}).get('p'), p, o):
        if isinstance(d, dict) and d.get(k) is not None: return d[k]
    return None


def strat_info(ty, scene, spec, p, o):
    """→ (hợp lệ theo định nghĩa B3, [lý do sai]) cho shot type strategic; shot khác → (False, [])"""
    if ty != 'strategic': return False, []
    why = []; tl = _n(get(spec, p, o, 'nghieng')); w = get(spec, p, o, 'be_ngang_km')
    if str(scene or '').startswith('map/globe'): why.append('cảnh map/globe (NC-H2 vẫn áp)')
    if tl is None: why.append('thiếu nghieng')
    elif tl > TILT_MAX: why.append(f'nghiêng {tl:g}° > {TILT_MAX:g}°')
    ws = [w] if _n(w) is not None else (w if isinstance(w, list) else [])
    ws = [_n(x) for x in ws]
    if not ws or any(x is None for x in ws): why.append('thiếu be_ngang_km')
    elif any(not WIDTH_KM[0] <= x <= WIDTH_KM[1] for x in ws): why.append(f"bề ngang {'–'.join(f'{x:g}' for x in ws)} km ngoài {WIDTH_KM[0]:g}–{WIDTH_KM[1]:g} km")
    return not why, why


def _shots(E, TL):
    from checks.ll import q_k2var
    chu = {s['id']: str(s.get('chuong') or s['id']) for s in E.get('segments') or [] if isinstance(s, dict) and 'id' in s}
    seg = {s['id']: s for s in TL['segments']}
    out = []
    for z in q_k2var.shots(E, TL):
        p = z['sh'].get('p') or {}; o = (z['h'] or {}).get('opt') or {}
        ok, why = strat_info(z['ty'], z['scene'], z['spec'], p, o)
        out.append(dict(z, p=p, o=o, chuong=chu.get(z['seg'], str(z['seg'])), strat=z['ty'] == 'strategic', strat_ok=ok, strat_why=why,
                        g=lambda k, z=z, p=p, o=o: get(z['spec'], p, o, k), segd=seg[z['seg']]))
    return out


def _w(z): return f"{z['seg']}/{z['i']} @{mmss(z['t0'])}"


# ================================================================ log chữ k2.js
def load_logs(logdir):
    L = {}
    for f in glob.glob(os.path.join(logdir, '*.log.json')) if logdir else []:
        try: J = json.load(open(f))
        except (OSError, ValueError): continue
        if J.get('fmt', '16x9') == '16x9' and J.get('id'): L[str(J['id'])] = J
    return L


def frames_in(L, z, a=None, b=None):
    """khung log của đoạn chứa shot z trong [t0 + a, t0 + b) (giây trong shot; mặc định cả shot) → [(t phim, items, occ)]"""
    J = L.get(str(z['seg']))
    if not J: return None
    s0 = z['segd']['t0']; lo = z['t0'] + (a or 0.0); hi = z['t0'] + b if b is not None else z['t1']; hi = min(hi, z['t1'])
    return [(s0 + e['f'] / 24, e.get('items') or [], e.get('occ') or []) for e in J.get('text') or [] if lo - 1e-6 <= s0 + e['f'] / 24 < hi - 1e-6]


def px(it): return (_n(it.get('cap')) or 0.0) / CAP_RATIO


# ================================================================ dữ liệu bản đồ
def _ld(base, x):
    if x is None: return None
    if isinstance(x, (dict, list)): return x
    p = x if os.path.isabs(x) else os.path.join(base, x)
    return json.load(open(p))


def cfg_of(E, ep_dir, over=None):
    C = dict(E.get('ban_do') or {}); C.update(over or {}); base = ep_dir or '.'
    M = _ld(base, C.get('lop')); mbase = os.path.dirname(os.path.join(base, C['lop'])) if isinstance(C.get('lop'), str) else base
    if isinstance(M, list): M = dict(lop=M)
    for L in (M or {}).get('lop') or []:
        h = L.get('hinh'); G = _ld(mbase, h) if h is not None else None
        if isinstance(G, dict) and G.get('type') == 'FeatureCollection': L['_features'] = G['features']
        elif isinstance(G, dict) and G.get('type') == 'Feature': L['_features'] = [G]
        else: L['_features'] = L.get('features') or []
    cl = _ld(base, C.get('claims')); cl = cl.get('claims') if isinstance(cl, dict) else cl
    return dict(lop=M, tuyen=_ld(base, C.get('tuyen')), inset=_ld(base, C.get('inset')), claims=cl, co_cfg=bool(C))


def _rings(geom):
    """geometry GeoJSON → [(np.array (n, 2) lon/lat, là_polygon)]"""
    t = (geom or {}).get('type'); c = (geom or {}).get('coordinates') or []
    if t == 'LineString': return [(np.asarray(c, float)[:, :2], False)]
    if t == 'MultiLineString': return [(np.asarray(x, float)[:, :2], False) for x in c]
    if t == 'Polygon': return [(np.asarray(x, float)[:, :2], True) for x in c]
    if t == 'MultiPolygon': return [(np.asarray(x, float)[:, :2], True) for P in c for x in P]
    return []


_NE = {}


def ne_load(name):
    """checks/ll/data/ne10m-<name>.npz → dict(feat=[[ring (n, 2) độ]], ten, edges (N, 4), ebox)"""
    if name in _NE: return _NE[name]
    with np.load(os.path.join(DATA, f'ne10m-{name}.npz')) as Z: Z = {k: Z[k] for k in Z.files}   # NpzFile giải nén lại mỗi lần truy cập
    xy = Z['xy'].astype(np.int64); off = list(Z['ring_off']) + [len(xy)]; rings = []   # mỗi vòng: điểm đầu + sai phân → cộng dồn
    for k in range(len(off) - 1): rings.append(np.cumsum(xy[off[k]:off[k + 1]], axis=0) / 1e5)
    feat = [[] for _ in range(int(Z['poly_feat'].max()) + 1)]
    for k, rg in enumerate(rings): feat[int(Z['poly_feat'][int(Z['ring_poly'][k])])].append(rg)
    E = np.vstack([np.hstack([rg[:-1], rg[1:]]) for rg in rings if len(rg) > 1])
    eb = np.stack([np.minimum(E[:, 0], E[:, 2]), np.minimum(E[:, 1], E[:, 3]), np.maximum(E[:, 0], E[:, 2]), np.maximum(E[:, 1], E[:, 3])], 1)
    _NE[name] = dict(feat=feat, ten=[str(x) for x in Z['ten']], edges=E, ebox=eb)
    return _NE[name]


def pip(pts, E):
    """điểm (m, 2) trong tập cạnh E (n, 4) theo chẵn–lẻ → bool (m,)"""
    out = np.zeros(len(pts), bool)
    for k, (x, y) in enumerate(pts):
        c = (E[:, 1] > y) != (E[:, 3] > y)
        if not c.any(): continue
        e = E[c]; xi = e[:, 0] + (y - e[:, 1]) * (e[:, 2] - e[:, 0]) / (e[:, 3] - e[:, 1])
        out[k] = bool(np.count_nonzero(x < xi) % 2)
    return out


def _cross(ax, ay, bx, by): return ax * by - ay * bx


def seg_hits(p0, p1, E):
    """tham số t ∈ [0, 1] trên đoạn p0→p1 nơi cắt các cạnh E (n, 4) (u ∈ [0, 1) trên cạnh)"""
    if not len(E): return np.zeros(0)
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]; ex, ey = E[:, 2] - E[:, 0], E[:, 3] - E[:, 1]
    den = _cross(dx, dy, ex, ey); qx, qy = E[:, 0] - p0[0], E[:, 1] - p0[1]
    with np.errstate(divide='ignore', invalid='ignore'):
        t = _cross(qx, qy, ex, ey) / den; u = _cross(qx, qy, dx, dy) / den
    ok = (den != 0) & (t >= 0) & (t <= 1) & (u >= 0) & (u < 1)
    return np.sort(t[ok])


def _ptseg(px_, py_, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay; L2 = dx * dx + dy * dy
    with np.errstate(divide='ignore', invalid='ignore'):
        u = np.where(L2 > 0, ((px_ - ax) * dx + (py_ - ay) * dy) / L2, 0.0)
    u = np.clip(u, 0, 1); return np.hypot(px_ - (ax + u * dx), py_ - (ay + u * dy))


def segseg_min(A, B):
    """khoảng cách nhỏ nhất giữa hai tập đoạn (km) A (n, 4), B (m, 4); 0 khi cắt nhau"""
    if not len(A) or not len(B): return math.inf
    best = math.inf
    for k in range(0, len(A), 512):
        a = A[k:k + 512][:, None, :]; b = B[None, :, :]
        d1 = _ptseg(a[..., 0], a[..., 1], b[..., 0], b[..., 1], b[..., 2], b[..., 3]); d2 = _ptseg(a[..., 2], a[..., 3], b[..., 0], b[..., 1], b[..., 2], b[..., 3])
        d3 = _ptseg(b[..., 0], b[..., 1], a[..., 0], a[..., 1], a[..., 2], a[..., 3]); d4 = _ptseg(b[..., 2], b[..., 3], a[..., 0], a[..., 1], a[..., 2], a[..., 3])
        d = np.minimum(np.minimum(d1, d2), np.minimum(d3, d4))
        o1 = _cross(a[..., 2] - a[..., 0], a[..., 3] - a[..., 1], b[..., 0] - a[..., 0], b[..., 1] - a[..., 1])
        o2 = _cross(a[..., 2] - a[..., 0], a[..., 3] - a[..., 1], b[..., 2] - a[..., 0], b[..., 3] - a[..., 1])
        o3 = _cross(b[..., 2] - b[..., 0], b[..., 3] - b[..., 1], a[..., 0] - b[..., 0], a[..., 1] - b[..., 1])
        o4 = _cross(b[..., 2] - b[..., 0], b[..., 3] - b[..., 1], a[..., 2] - b[..., 0], a[..., 3] - b[..., 1])
        d = np.where((o1 * o2 < 0) & (o3 * o4 < 0), 0.0, d); best = min(best, float(d.min()))
    return best


def km_xy(P, lat0):
    P = np.asarray(P, float); return np.stack([P[..., 0] * 111.32 * math.cos(math.radians(lat0)), P[..., 1] * KY], -1)


def line_vs_disputed(rings, buf=DISP_KM):
    """[(ring (n, 2), là_polygon)] → [(tên vùng NE, khoảng cách km)] các vùng tranh chấp trong ≤ buf km"""
    D = ne_load('disputed'); out = []
    segs = np.vstack([np.hstack([rg[:-1], rg[1:]]) for rg, _ in rings if len(rg) > 1]) if rings else np.zeros((0, 4))
    pts = np.vstack([rg for rg, _ in rings]) if rings else np.zeros((0, 2))
    for fi, F in enumerate(D['feat']):
        allp = np.vstack(F); lat0 = float(allp[:, 1].mean()); dlon = buf / (111.32 * max(0.05, math.cos(math.radians(lat0)))) * 1.2; dlat = buf / KY * 1.2
        x0, y0 = allp.min(0) - (dlon, dlat); x1, y1 = allp.max(0) + (dlon, dlat)
        sel = segs[(np.maximum(segs[:, 0], segs[:, 2]) >= x0) & (np.minimum(segs[:, 0], segs[:, 2]) <= x1) & (np.maximum(segs[:, 1], segs[:, 3]) >= y0) & (np.minimum(segs[:, 1], segs[:, 3]) <= y1)]
        if not len(sel): continue
        Ep = np.vstack([np.hstack([rg[:-1], rg[1:]]) for rg in F if len(rg) > 1])
        pin = pts[(pts[:, 0] >= x0) & (pts[:, 0] <= x1) & (pts[:, 1] >= y0) & (pts[:, 1] <= y1)]
        if len(pin) and pip(pin, Ep).any(): out.append((D['ten'][fi], 0.0)); continue
        A = np.hstack([km_xy(sel[:, :2], lat0), km_xy(sel[:, 2:], lat0)]); B = np.hstack([km_xy(Ep[:, :2], lat0), km_xy(Ep[:, 2:], lat0)])
        d = segseg_min(A, B)
        if d <= buf: out.append((D['ten'][fi], round(d, 2)))
    return out


def _hav(a, b):
    la1, la2 = math.radians(a[1]), math.radians(b[1]); dl = math.radians(b[0] - a[0])
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin(dl / 2) ** 2
    return 2 * 6371.0 * math.asin(min(1.0, math.sqrt(h)))


def route_land(line, ports, step=0.25):
    """polyline lon/lat (n, 2) → [(km đất ngoài vùng đệm cảng, [lon, lat] điểm đầu)] từng đoạn đất; đất = NE 1:10m chẵn–lẻ toàn cầu"""
    Ld = ne_load('land'); E, eb = Ld['edges'], Ld['ebox']; out = []
    for k in range(len(line) - 1):
        p0, p1 = line[k], line[k + 1]
        bx0, by0 = min(p0[0], p1[0]), min(p0[1], p1[1]); bx1, by1 = max(p0[0], p1[0]), max(p0[1], p1[1])
        sel = E[(eb[:, 2] >= bx0) & (eb[:, 0] <= bx1) & (eb[:, 3] >= by0) & (eb[:, 1] <= by1)]
        ts = list(seg_hits(p0, p1, sel)); inside = bool(pip(np.asarray([p0]), E)[0])
        L = _hav(p0, p1); cuts = [0.0] + ts + [1.0]
        for a, b in zip(cuts, cuts[1:]):
            if inside and b > a:
                n = max(2, int(math.ceil((b - a) * L / step)) + 1); land = 0.0; first = None
                for u in np.linspace(a, b, n):
                    q = (p0[0] + u * (p1[0] - p0[0]), p0[1] + u * (p1[1] - p0[1]))
                    if all(_hav(q, c) > PORT_KM for c in ports):
                        land += (b - a) * L / (n - 1); first = first or [round(float(q[0]), 4), round(float(q[1]), 4)]
                if first and land > step: out.append((round(float(land), 2), first))
            inside = not inside
    return out


# ================================================================ luật
def check(E, TL, ep_dir=None, logdir=None, over=None):
    S = _shots(E, TL); T = float(TL['tong_s']); C = cfg_of(E, ep_dir, over); L = load_logs(logdir)
    ST = [z for z in S if z['strat']]; M = C['lop'] or {}; LOP = {str(x.get('id')): x for x in M.get('lop') or []}
    W = _n(M.get('W')) or 1920.0
    R = {}
    # ---------------------------------------------------------------- BD-1
    if not ST: R['BD-1'] = khong_ap('không có shot type strategic')
    else:
        P, near = {k: [] for k in 'abcdef'}, []
        tot = sum(z['t1'] - z['t0'] for z in ST); pct = 100 * tot / T
        if pct > STRAT_PCT: P['a'].append(f'(a) strategic {tot:.1f} s = {pct:.1f} % thời lượng > {STRAT_PCT:g} %')
        near += _sat('strategic % thời lượng', round(pct, 1), STRAT_PCT)
        for z in ST:
            d = z['t1'] - z['t0']
            if d > STRAT_S + 1e-6: P['b'].append(f'(b) {_w(z)}: {d:.2f} s > {STRAT_S:g} s')
            near += _sat(f'{_w(z)} dài', round(d, 2), STRAT_S)
            if z['strat_why']: P['e'].append(f"(e) {_w(z)}: ngoài định nghĩa strategic — {'; '.join(z['strat_why'])}")
        by = {}
        for z in ST: by.setdefault(z['chuong'], []).append(z)
        for ch, zs in by.items():
            if len(zs) > STRAT_CH: P['c'].append(f"(c) chương {ch}: {len(zs)} shot strategic > {STRAT_CH} ({', '.join(_w(z) for z in zs)})")
        for a, b in zip(S, S[1:]):
            if a['strat'] and b['strat'] and abs(b['t0'] - a['t1']) <= 1 / 24 + 1e-3: P['d'].append(f'(d) {_w(a)} và {_w(b)}: hai shot strategic liền nhau')
        for k, z in enumerate(S):
            if not z['strat']: continue
            # nhãn mốc thời gian
            fr = frames_in(L, z)
            if fr:
                hit = sum(1 for _, it, _ in fr if any(TIME_RE.match(str(x.get('s', ''))) for x in it))
                if not hit: P['f'].append(f'(f) {_w(z)}: log chữ không có nhãn mốc thời gian (năm/ngày) ngoài nhãn ranh')
            elif not any(z['g'](x) for x in ('nam', 'year', 'dem_ngay', 'date', 'counter')):
                P['f'].append(f'(f) {_w(z)}: không có nhãn mốc thời gian (khai nam/year/dem_ngay hoặc log chữ)')
            # chú giải ≤ 3 phe
            cg = z['g']('chu_giai') or []; fac = {str(x.get('faction_id')) for x in cg if isinstance(x, dict) and x.get('faction_id')}
            for lid in _lops_of(z, LOP):
                fac |= {str((f.get('properties') or {}).get('faction_id')) for f in LOP[lid]['_features'] if (f.get('properties') or {}).get('faction_id')}
            if len(fac) > LEGEND_MAX: P['f'].append(f"(f) {_w(z)}: {len(fac)} phe > {LEGEND_MAX} ({', '.join(sorted(fac))})")
            if fac and not cg: P['f'].append(f'(f) {_w(z)}: có {len(fac)} phe tô màu mà không có chú giải (chu_giai)')
            # shot kề cùng chương là 3D tại nơi được chỉ tới
            ct = [str(x).strip().lower() for x in (z['g']('chi_toi') or []) if str(x).strip()]
            nb = [y for y in (S[k - 1] if k else None, S[k + 1] if k + 1 < len(S) else None) if y and y['chuong'] == z['chuong']]
            if not ct: P['f'].append(f'(f) {_w(z)}: thiếu chi_toi (nơi bản đồ chỉ tới)')
            elif not any(_is3d(y) and _place_hit(y, ct) for y in nb):
                P['f'].append(f"(f) {_w(z)}: không shot kề cùng chương là cảnh 3D tại {'/'.join(ct)} (kề: {', '.join(f'{_w(y)} {y['ty']} {y['scene']}' for y in nb) or 'không có'})")
        loi = [x for k in 'abcdef' for x in P[k]]
        R['BD-1'] = r(True, loi, [], val=f'{len(ST)} shot strategic · {tot:.1f} s = {pct:.1f} % phim · dài nhất {max(z["t1"] - z["t0"] for z in ST):.2f} s'
                                       f' · nhiều nhất/chương {max(len(v) for v in by.values())} · hợp lệ định nghĩa {sum(1 for z in ST if z["strat_ok"])}', sat_nguong=near,
                      pct=round(pct, 2))
    # ---------------------------------------------------------------- BD-2
    if not ST: R['BD-2'] = khong_ap('không có shot type strategic')
    else:
        loi, th, near = [], [], []
        for z in ST:
            d = z['t1'] - z['t0']; el = z['g']('dong') or z['g']('chuyen_dong') or []
            el = [x for x in el if isinstance(x, dict) and str(x.get('loai', '')).lower() in MOVE_KINDS]
            if not el: loi.append(f'(a) {_w(z)}: không có phần tử chuyển động ({"/".join(sorted(MOVE_KINDS))})'); continue
            iv = []
            for x in el:
                t = x.get('t') or x.get('draw') or x.get('walk')
                if isinstance(t, list) and len(t) == 2 and all(_n(v) is not None for v in t): iv.append((float(t[0]), min(float(t[1]), d), x.get('loai')))
                else: th.append(f'{_w(z)}: phần tử {x.get("loai")} không có t [a, b] số')
            good = [v for v in iv if v[0] <= MOVE_T0 + 1e-6 and 100 * (v[1] - v[0]) / d >= MOVE_PCT - 1e-6]
            if iv and not good:
                b = max(iv, key=lambda v: (v[0] <= MOVE_T0 + 1e-6, v[1] - v[0]))
                loi.append(f'({"b" if b[0] > MOVE_T0 + 1e-6 else "c"}) {_w(z)}: phần tử tốt nhất {b[2]} {b[0]:.2f}–{b[1]:.2f} s'
                           f' (bắt đầu ≤ {MOVE_T0:g} s, phủ {100 * (b[1] - b[0]) / d:.0f} % ≥ {MOVE_PCT:g} %)')
            for v in good[:1]:
                near += _sat(f'{_w(z)} phủ %', round(100 * (v[1] - v[0]) / d, 1), MOVE_PCT) + _sat(f'{_w(z)} bắt đầu', round(v[0], 2), MOVE_T0)
        R['BD-2'] = r(True, loi, th, val=f'{len(ST)} shot strategic · đạt {len(ST) - len(loi)}', sat_nguong=near)
    # ---------------------------------------------------------------- BD-3
    hist = {k: v for k, v in LOP.items() if v.get('loai') == 'bien_gioi_lich_su'}
    pairs = [(z, lid) for z in S for lid in _lops_of(z, LOP) if lid in hist]
    if not pairs: R['BD-3'] = khong_ap('không có lớp bien_gioi_lich_su hiện trong shot nào')
    else:
        loi, th, near, rows = [], [], [], []
        for z, lid in pairs:
            Ly = hist[lid]; t = Ly.get('t') if isinstance(Ly.get('t'), list) else [None, None]
            fr = frames_in(L, z, _n(t[0]), _n(t[1]))
            if fr is None: th.append(f'(a) {_w(z)} lớp {lid}: không có log chữ của đoạn {z["seg"]}'); continue
            if not fr: th.append(f'(a) {_w(z)} lớp {lid}: không có khung log trong khoảng lớp hiện'); continue
            ok_n, small, yrs = 0, [], set()
            for _, it, _ in fr:
                m = [(x, LBL_RE.match(str(x.get('s', '')))) for x in it]; m = [(x, g) for x, g in m if g]
                if any(px(x) >= LBL_PX - 0.5 for x, _ in m): ok_n += 1
                small += [px(x) for x, _ in m if px(x) < LBL_PX - 0.5]; yrs |= {g.group(1) for _, g in m}
            pc = 100 * ok_n / len(fr); rows.append(f'{_w(z)} lớp {lid}: {ok_n}/{len(fr)} khung = {pc:.1f} %')
            if pc < LBL_PCT: loi.append(f'(a) {_w(z)} lớp {lid}: nhãn "approx. borders c. YYYY — nguồn" ≥ {LBL_PX:g} px ở {ok_n}/{len(fr)} khung = {pc:.1f} % < {LBL_PCT:g} %'
                                        + (f' (nhãn nhỏ nhất {min(small):.1f} px)' if small else ''))
            near += _sat(f'{_w(z)} lớp {lid} khung có nhãn %', round(pc, 1), LBL_PCT)
            if small and min(small) >= LBL_PX * 0.95 - 0.5: near.append(f'{_w(z)} nhãn ranh {min(small):.1f} px (ngưỡng {LBL_PX:g})')
            if _n(Ly.get('nam')) is not None and yrs and str(int(Ly['nam'])) not in yrs:
                loi.append(f"(c) {_w(z)} lớp {lid}: năm trên nhãn {'/'.join(sorted(yrs))} ≠ nam lớp {int(Ly['nam'])}")
        R['BD-3'] = r(True, loi, th, val=f'{len(pairs)} cặp shot–lớp ranh · ' + '; '.join(rows[:4]), sat_nguong=near)
    # ---------------------------------------------------------------- BD-4
    ref = {lid for z in S for lid in _lops_of(z, LOP, all_=True)}
    if not LOP and not ref: R['BD-4'] = khong_ap('không có manifest lớp ranh và không shot nào trỏ lớp')
    else:
        loi, near = [], []
        for lid in sorted(ref - set(LOP)): loi.append(f'(a) lớp {lid} được shot trỏ tới nhưng không có trong manifest lớp ranh')
        for lid, Ly in LOP.items():
            if not Ly.get('loai'): loi.append(f'(a) lớp {lid}: thiếu loai'); continue
            if Ly['loai'] != 'bien_gioi_lich_su': continue
            miss = [k for k in ('nam', 'nguon', 'nguon_doi_chieu', 'lech_tb_px', 'giay_phep') if Ly.get(k) in (None, '', [])]
            if miss: loi.append(f"(a) lớp {lid}: thiếu {', '.join(miss)}")
            gp = Ly.get('giay_phep'); gp = gp if isinstance(gp, list) else ([gp] if gp else [])
            bad = [g for g in gp if _lic(g) not in LICENSES]
            if bad: loi.append(f"(b) lớp {lid}: giấy phép {', '.join(map(str, bad))} ngoài {{{', '.join(sorted(LICENSES))}}}")
            lt = _n(Ly.get('lech_tb_px'))
            if lt is not None:
                if lt > EDGE_PX and str(Ly.get('kieu_mep') or '').lower() not in EDGE_KIEU:
                    loi.append(f"(c) lớp {lid}: lech_tb_px {lt:g} > {EDGE_PX:g} mà kieu_mep = {Ly.get('kieu_mep') or 'không khai'} (cần mem/gach)")
                near += _sat(f'lớp {lid} lech_tb_px', lt, EDGE_PX)
            if Ly.get('nguon') and str(Ly.get('nguon')).strip().lower() == str(Ly.get('nguon_doi_chieu') or '').strip().lower():
                loi.append(f'(d) lớp {lid}: nguon_doi_chieu trùng nguon (không phải hai nguồn kiểm chéo)')
        R['BD-4'] = r(True, loi, [], val=f'{len(LOP)} lớp · bien_gioi_lich_su {len(hist)} · shot trỏ {len(ref)}', sat_nguong=near)
    # ---------------------------------------------------------------- BD-5
    if not LOP: R['BD-5'] = khong_ap('không có manifest lớp ranh')
    else:
        loi, th, near, nm = [], [], [], 0
        for lid, Ly in LOP.items():
            if Ly.get('loai') == 'bien_gioi_hien_dai':
                rg = [x for f in Ly['_features'] for x in _rings(f.get('geometry'))]; nm += 1
                for ten, d in line_vs_disputed(rg): loi.append(f'(a) lớp {lid} (bien_gioi_hien_dai): cách vùng tranh chấp NE "{ten}" {d:g} km ≤ {DISP_KM:g} km')
            kp = _n(Ly.get('km_px')) or ((_n(Ly.get('be_ngang_km')) or 0) / W or None)
            polys = [f for f in Ly['_features'] if (f.get('geometry') or {}).get('type') in ('Polygon', 'MultiPolygon') and str((f.get('properties') or {}).get('ve') or 'polygon') != 'diem']
            if polys and not kp: th.append(f'lớp {lid}: thiếu km_px/be_ngang_km — không đo cỡ lãnh thổ'); continue
            for f in polys:
                P_ = np.vstack([g for g, _ in _rings(f['geometry'])]); lat0 = float(P_[:, 1].mean()); K_ = km_xy(P_, lat0)
                ext = float(max(K_[:, 0].max() - K_[:, 0].min(), K_[:, 1].max() - K_[:, 1].min())) / kp
                nmf = (f.get('properties') or {}).get('ten') or (f.get('properties') or {}).get('faction_id') or '?'
                if ext < SMALL_PX: loi.append(f'(b) lớp {lid} "{nmf}": lãnh thổ {ext:.1f} px < {SMALL_PX:g} px vẽ polygon (phải vẽ điểm)')
                near += _sat(f'lớp {lid} "{nmf}" px', round(ext, 1), SMALL_PX)
        R['BD-5'] = r(True, loi, th, val=f'{nm} lớp bien_gioi_hien_dai · đệm {DISP_KM:g} km quanh NE disputed 1:10m', sat_nguong=near)
    # ---------------------------------------------------------------- BD-6
    TU = C['tuyen']; feats = (TU or {}).get('features') or [] if isinstance(TU, dict) else (TU or [])
    wants = any(str(x.get('loai', '')).lower() == 'route' for z in ST for x in (z['g']('dong') or []) if isinstance(x, dict))
    if not feats:
        R['BD-6'] = r(True, [], ['shot strategic có phần tử route mà không có routes.geojson (ban_do.tuyen)']) if wants else khong_ap('không có tuyến')
    else:
        loi, th = [], []; cid = {str(c.get('id')) for c in C['claims'] or [] if isinstance(c, dict)}; nsea = 0
        if C['claims'] is None: th.append('không có claims (ban_do.claims) — (c) không kiểm id')
        for f in feats:
            pr = f.get('properties') or {}; rid = pr.get('id') or '?'; cl = pr.get('claims') or ([pr['claim']] if pr.get('claim') else [])
            if not cl: loi.append(f'(b) tuyến {rid}: không có claim id')
            elif C['claims'] is not None:
                miss = [c for c in cl if str(c) not in cid]
                if miss: loi.append(f"(c) tuyến {rid}: claim {', '.join(map(str, miss))} không có trong claims")
            if str(pr.get('mode') or '').lower() not in ('sea', 'bien'): continue
            nsea += 1
            for rg, _ in _rings(f.get('geometry')):
                ports = [tuple(rg[0]), tuple(rg[-1])] + [tuple(c[:2]) for c in pr.get('cang') or []]
                for km, at in route_land(rg, ports): loi.append(f'(a) tuyến biển {rid}: cắt đất {km:g} km (ngoài đệm {PORT_KM:g} km quanh cảng), từ {at}')
        R['BD-6'] = r(True, loi, th, val=f'{len(feats)} tuyến · biển {nsea} · đất NE 1:10m, đệm cảng {PORT_KM:g} km')
    # ---------------------------------------------------------------- BD-7 (+ B8)
    col, fl, b8 = {}, [], []
    for lid, Ly in LOP.items():
        for f in Ly['_features']:
            pr = f.get('properties') or {}
            if pr.get('faction_id') and isinstance(pr.get('fill'), str) and pr['fill'].startswith('#'): col.setdefault(str(pr['faction_id']), {}).setdefault(pr['fill'].lower(), []).append(f'lớp {lid}')
            if str(pr.get('fill_the') or '').lower() in FLAG_TAGS: fl.append(f"(b) lớp {lid} \"{pr.get('ten') or pr.get('faction_id') or '?'}\": fill là {pr['fill_the']} (cờ/biểu tượng)")
            if pr.get('ban_dia') and pr.get('ten'):
                fill = str(pr.get('fill') or '').strip().lower(); nen = str(Ly.get('nen_trong') or '').strip().lower()
                if fill in ('', 'none', 'transparent') or (nen and fill == nen):
                    b8.append(f"(c) lớp {lid}: thực thể bản địa \"{pr['ten']}\" tô như đất trống (fill {fill or 'rỗng'}{' = nen_trong' if nen and fill == nen else ''})")
    for z in S:
        for x in z['g']('chu_giai') or []:
            if isinstance(x, dict) and x.get('faction_id') and isinstance(x.get('mau'), str): col.setdefault(str(x['faction_id']), {}).setdefault(x['mau'].lower(), []).append(f'chú giải {_w(z)}')
            if isinstance(x, dict) and str(x.get('fill_the') or '').lower() in FLAG_TAGS: fl.append(f"(b) chú giải {_w(z)} \"{x.get('faction_id')}\": {x['fill_the']}")
    if not col and not fl and not b8: R['BD-7'] = khong_ap('không có phe tô màu')
    else:
        loi = [f"(a) faction_id {k}: {len(v)} màu ({'; '.join(f'{c} ở {', '.join(sorted(set(w))[:3])}' for c, w in v.items())})" for k, v in sorted(col.items()) if len(v) > 1]
        R['BD-7'] = r(True, loi + fl + b8, [], val=f'{len(col)} phe · đổi màu {len(loi)} · fill cờ/biểu tượng {len(fl)} · bản địa tô trống {len(b8)}')
    # ---------------------------------------------------------------- BD-8
    IN = C['inset'] or {}; ins = IN.get('inset') if isinstance(IN, dict) else IN
    if not ins: R['BD-8'] = khong_ap('không có log inset')
    else:
        Wi, Hi = _n(IN.get('W')) or 1920.0, _n(IN.get('H')) or 1080.0; loi, near = [], []
        cuts = [0.0]
        for k, z in enumerate(S):
            if k == 0: continue
            first = z['i'] == 0; tr = (z['sh'].get('in') or {}).get('type') if isinstance(z['sh'].get('in'), dict) else z['sh'].get('in')
            soft = (str(tr or '').lower() in SOFT_IN) if not first else ((_n(z['segd'].get('fadeIn')) or 0) > 0)
            if not soft: cuts.append(z['t0'])
        for x in ins:
            iid = x.get('id') or '?'; t = x.get('t') or [0, 0]; a, b = float(t[0]), float(t[1])
            bx = [x['box']] if x.get('box') else [k['box'] for k in x.get('khung') or [] if k.get('box')]
            if not bx: loi.append(f'(a) inset {iid}: không có box'); continue
            x0, y0, x1, y1 = min(q[0] for q in bx), min(q[1] for q in bx), max(q[2] for q in bx), max(q[3] for q in bx)
            ar = 100 * max(((q[2] - q[0]) * (q[3] - q[1])) for q in bx) / (Wi * Hi)
            if ar > INSET_PCT: loi.append(f'(a) inset {iid} @{mmss(a)}: {ar:.1f} % khung > {INSET_PCT:g} %')
            near += _sat(f'inset {iid} % khung', round(ar, 1), INSET_PCT)
            tr_ = str(x.get('inset_goc') or '').lower() == 'tren_phai'
            if tr_ and len(str(x.get('ly_do') or '').strip()) < 10: loi.append(f'(b) inset {iid}: inset_goc tren_phai mà không ghi ly_do'); tr_ = False
            sx, sy = SAFE * Wi, SAFE * Hi
            okpos = (y0 >= sy - 0.5 and y1 <= Hi / 2 and ((x0 >= Wi / 2 and x1 <= Wi - sx + 0.5) if tr_ else (x0 >= sx - 0.5 and x1 <= Wi / 2)))
            if not okpos: loi.append(f"(b) inset {iid} @{mmss(a)}: box [{x0:g}, {y0:g}, {x1:g}, {y1:g}] không nằm góc trên {'phải' if tr_ else 'trái'} trong vùng an toàn {100 * SAFE:g} %")
            d = b - a
            if not INSET_S[0] - 1e-6 <= d <= INSET_S[1] + 1e-6: loi.append(f'(c) inset {iid} @{mmss(a)}: {d:.2f} s ngoài {INSET_S[0]:g}–{INSET_S[1]:g} s')
            near += _sat(f'inset {iid} s', round(d, 2), INSET_S[0]) + _sat(f'inset {iid} s', round(d, 2), INSET_S[1])
            hitz = []
            for z in S:
                if z['t1'] <= a or z['t0'] >= b: continue
                for tt, it, occ in frames_in(L, z) or []:
                    if not a - 1e-6 <= tt < b: continue
                    for q in [(o_, 'LL.occ') for o_ in occ] + [(i_.get('box'), f'chữ "{str(i_.get("s", ""))[:24]}"') for i_ in it if i_.get('box')]:
                        bb, nmq = q
                        if bb[0] >= x0 and bb[1] >= y0 and bb[2] <= x1 and bb[3] <= y1: continue   # chữ của chính inset
                        if bb[0] < x1 and bb[2] > x0 and bb[1] < y1 and bb[3] > y0: hitz.append(f'{mmss(tt)} {nmq}')
            if hitz: loi.append(f"(d) inset {iid}: giao {len(hitz)} hộp ({', '.join(sorted(set(hitz))[:3])})")
            for z in S:
                if z['t1'] <= a + 1e-6 or z['t0'] >= b - 1e-6: continue
                why = 'liên hoàn' if (z['g']('lien_hoan') or z['g']('vertigo')) else 'thẻ số' if z['ty'] == 'card' else 'ảnh/văn bản lưu trữ' if z['ty'] in ARCHIVE else None
                if why: loi.append(f'(e) inset {iid} @{mmss(a)}: trong {why} {_w(z)}')
            for c in cuts:
                if a < c + CUT_S - 1e-6 and b > c + 1e-6: loi.append(f'(e) inset {iid} @{mmss(a)}: trong {CUT_S:g} s sau cắt cứng {mmss(c)}'); break
        R['BD-8'] = r(True, loi, [] if L else ['không có log chữ — (d) không đo giao hộp chữ'], val=f'{len(ins)} inset · {Wi:g}×{Hi:g}', sat_nguong=near)
    return R


def _lic(g): return re.sub(r'[\s_]+', '-', str(g).strip().upper()).replace('CC-BY4.0', 'CC-BY-4.0')


def _lops_of(z, LOP, all_=False):
    ids = [str(x) for x in (z['g']('lop') or [])]
    ids += [lid for lid, Ly in LOP.items() if f"{z['seg']}/{z['i']}" in [str(s) for s in Ly.get('shot') or []]]
    return list(dict.fromkeys(ids)) if all_ else [x for x in dict.fromkeys(ids) if x in LOP]


def _is3d(y):
    return y['ty'] in ('scene3d', 'timelapse') or str(y['scene']).startswith(('relief/', 'tl/')) and y['ty'] != 'strategic'


def _place_hit(y, ct):
    txt = ' '.join(str(v) for v in (y['g']('where'), y['g']('noi_ten'), y['g']('focus'), y['scene'], y['g']('vung'), y.get('vung'))).lower()
    txt += ' ' + ' '.join(str(x.get('name') if isinstance(x, dict) else x) for x in (y['g']('places') or [])).lower()
    return any(c in txt for c in ct)


def main():
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    g = lambda k: a[a.index('--' + k) + 1] if '--' + k in a else None
    from checks.ll import base
    E = base.load(a[0]); E['_path'] = os.path.abspath(a[0])
    R = check(E, json.load(open(g('tl') or os.path.join(E['out'], 'timeline.json'))), os.path.dirname(os.path.abspath(a[0])), g('logs'))
    for k, v in R.items():
        kq = v.get('ket_qua') or ('ĐẠT' if v['ok'] else 'TRƯỢT')
        print(f"{k} {kq} · {v['val']}" + ''.join('\n  ' + x for x in (v['loi'] + v['thieu'])[:20]))
    if g('json'): json.dump(R, open(g('json'), 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
