#!/opt/cine/bin/python
"""NC-H1…NC-H5 luật hình "nơi chốn" rút từ đánh giá T2 của chủ dự án — bản 1.13.0 (phiên K, 17/10/2026); 1.14.0: loại `strategic` (B3). Mặc định CHỈ BÁO (cấp đề xuất:
reports/K-1.13-BAO-CAO.md, cap112.py). Căn cứ: reports/NC-LICH-SU-BAO-CAO.md §6 (origin/nc-lich-su @a30af04): chủ dự án xem T2 "Shipbuilding" —
(1) nơi thành phố chỉ là địa hình, không có nhà; (2) địa cầu/độ cao lớn không cần thiết. Định nghĩa: checks/ll/RULES-LL.md mục "1.13".

  q_noi.py <episode.yaml> --tl <timeline.json> [--json ra.json]          tập kênh 2 (bản đồ nổi / địa cầu / cảnh 3D)
  q_noi.py --bo-tl <bo-tl.json> [--json ra.json]                          bộ timelapse (campath + mặt nạ mọi khung + log chữ)

ĐỘ CAO (AGL, km) MỖI KHUNG — bản sao độc lập của máy quay bộ dựng (đổi trình dựng không đổi nghĩa luật):
  bộ timelapse: `campath[].agl` (mét) của grammarLog (design/k2v/tl/campath.js).
  tập kênh 2: shot bản đồ — giây cảnh τ = (giây đoạn − đầu shot)·speed + frame0/24 (p.frame0, không có thì p.off — ll.py đổi tên), mốc
    `heroes.<k>.opt.cam` của timeline (mốc "@từ" đã giải; `t` giây cảnh, hoặc `u`·dur):
    relief/* (design/k2v/relief.js): Hermite bậc 3 tiếp tuyến Catmull-Rom theo thời gian, log(dist); AGL = dist·cos(tilt) (km, độ cao
      trên điểm nhìn; dist km theo X() = (lon − lonc)·111,32·cos φ).
    map/globe (design/k2v/map.js): mốc nội suy easeIO, log(alt); R = 10 đơn vị = 6 371 km; AGL = (|T + alt·(cos tilt·n − sin tilt·h)| − R)
      · 637,1 km. Không có `opt.cam` → mốc của preset MAP_PRESETS (orbit, flyto, pullback, tilt-low, top, pan, pair: alt theo `opt.alt`; `pair`
      mốc giữa max(6, d·0,11) lấy cận dưới 6). Cảnh 3D không địa lý (k2g01/…, ảnh, footage, thẻ) → không có AGL (không tính "3D địa lý").
  Bộ dựng ghi `agl` (km) vào meta/timeline của shot (V5b-2b) → dùng số đó, thay số suy.

NC-H1 Thành phố có nhà. Đơn vị = shot (tập) hoặc cửa sổ `noi` (bộ timelapse: bo-tl.noi [{t: [t0, t1], noi}]).
  Đơn vị là THÀNH PHỐ khi khai `noi: thanh_pho` (shot, p, heroes.<k>.opt, bo-tl.noi). Không khai (tập/bộ cũ) → SUY: AGL ≤ 3 km ở ≥ 1 khung
  (bộ timelapse: mọi khung AGL ≤ 3 km, vì không có polygon đô thị OSM trong bộ — ghi "suy") HOẶC chip nơi `p.where` dạng thành phố
  ("Tên, Bang." hoặc "Tên area"; trừ tên có Bay/River/Valley/Sea/Gulf/Coast/Island/Strait/Ocean/Lake).
  Đo (mặt nạ mọi khung `fabric_pct` = nhà + đường):
  (a) trung vị fabric_pct trong đơn vị < FAB_MED % → TRƯỢT
  (b) có khung fabric_pct < FAB_MIN %, TRỪ khung trong ≤ REVEAL_TAIL s cuối một cú reveal kéo lùi (bo-tl.reveal kieu keo_lui) → TRƯỢT
  Tập không có mặt nạ fabric: shot thành phố có lớp nhà khai (opt.aerial ảnh hàng không, opt.city/buildings/ghost, ảnh/footage) → "khai, không
  đo fabric" (ĐẠT theo đặc tả, ghi THIẾU số đo); bản đồ nổi/địa cầu không lớp nhà → fabric = 0 theo đặc tả → TRƯỢT (a).
1.14 (chủ dự án duyệt B3 17/10): shot `type: strategic` ĐẠT định nghĩa BD-1 (e) (q_bando.strat_info: nghiêng ≤ 30°, bề ngang 300–5 000 km,
  không phải map/globe) KHÔNG tính vào NC-H2 và bị loại khỏi CẢ tử số LẪN mẫu số NC-H3 (mẫu số = thời lượng 3D địa lý trừ shot strategic hợp lệ;
  nên bản đồ phẳng tầm cao không kéo tỷ lệ AGL thấp xuống, và cũng không có giây nào được cộng vào phần "AGL thấp"). Shot strategic SAI định nghĩa
  tính như cảnh bản đồ thường (NC-H2/H3 áp đủ). Mọi shot type strategic (đúng hay sai định nghĩa) KHÔNG bao giờ là đơn vị "thành phố" của NC-H1.
NC-H2 Địa cầu. Khung AGL > GLOBE_KM km là "địa cầu". Một LẦN = chuỗi khung địa cầu liền nhau (qua mối cắt vẫn là một lần).
  (a) > GLOBE_N lần/tập → TRƯỢT;  (b) một lần dài > GLOBE_S s → TRƯỢT. Báo kèm: lần nào là map/globe, lần nào là bản đồ nổi tầm cao.
NC-H3 Tầm mặc định. Trên thời lượng 3D địa lý (khung có AGL): (a) phần AGL ≤ RANGE_KM km < RANGE_PCT % → TRƯỢT;
  (b) tập có thành phố (NC-H1 có ≥ 1 đơn vị thành phố, khai hoặc suy) mà phần AGL ≤ CITY_KM km < CITY_PCT % → TRƯỢT.
NC-H4 Nơi có tên. Mọi shot bản đồ (type map/timelapse; cảnh relief/*, map/globe) phải hiện chip nơi (`p.where`) hoặc nhãn địa danh: chữ hiện
  trong shot (log chữ nếu có: role where/place/label/tag/card; không log: p.tags/p.places/heroes.<k>.opt.places/pins/labels/regions) trùng
  một địa danh của tập (`places`, `opt.places[].name`, `opt.focus/from/to`, mục `where` của mọi shot). Thiếu cả hai → TRƯỢT (shot nêu tên).
  Bộ timelapse: log chữ role where/place, hoặc chữ trùng `bo-tl.dia_danh`; thiếu → TRƯỢT.
NC-H5 Đúng thời kỳ (bộ timelapse; tập không có bộ đếm năm → không áp).
  (a) khung có toà/đường mang năm xây > năm bộ đếm → TRƯỢT. Đầu vào: bo-tl.nam_khung [{f, nam_max: {lớp: năm}}] (năm xây lớn nhất của phần tử
      ĐANG HIỆN theo lớp; tầng ghost không tính) so với campath[].year (giảm năm: so floor). Không có → THIẾU.
  (b) lần đầu ghost hiện (mặt nạ `ghost_pct` > GHOST_MIN %) phải có nhãn nguồn ghost (log chữ role ghost_src, hoặc chữ chứa
      "reconstructed"/"ghost"/"footprint"/"conjectural") cỡ ≥ SRC_PX px, hiện liền ≥ GHOST_S s, bắt đầu không muộn hơn 0,5 s sau ghost.
      Không có ghost_pct → THIẾU (báo kèm nhãn ghost tìm thấy); riêng khi log CÓ nhãn nguồn ghost (⇒ phim có ghost) mà không nhãn nào
      ≥ SRC_PX px liền ≥ GHOST_S s → TRƯỢT (lần đầu cũng không thể đủ).
Trong ±5 % quanh ngưỡng: nêu tên.
"""
import json, math, os, re, statistics, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

FAB_MED, FAB_MIN, REVEAL_TAIL = 25.0, 15.0, 3.0          # NC-LS §6.2 (đề xuất, hiệu chuẩn trên gib20 V5b-2a: báo cáo K-1.13 §3)
GLOBE_KM, GLOBE_N, GLOBE_S = 50.0, 1, 3.0                 # NC-LS §6.1 (b): "tối đa 1 lần/tập, ≤ 3 s"
RANGE_KM, RANGE_PCT, CITY_KM, CITY_PCT = 60.0, 70.0, 3.0, 40.0
GHOST_MIN, SRC_PX, GHOST_S = 0.5, 38.0, 3.0
STEP = 0.25                                                # bước lấy mẫu AGL của tập (s)
R_GLOBE, KM_UNIT = 10.0, 637.1
NOT_CITY = re.compile(r'\b(bay|river|valley|sea|gulf|coast|island|islands|strait|ocean|lake|delta|sound|peninsula|mountains?)\b', re.I)
CITY_CHIP = re.compile(r'^\s*[A-Z][\w .\'-]*?(,\s*[A-Z][\w.]*\.?|\s+area)\s*$')
GHOST_TXT = re.compile(r'reconstruct|ghost|footprint|conjectur', re.I)


def mmss(t): return f'{int(t // 60)}:{t % 60:04.1f}'


def _n(v): return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def r(ok, loi=None, thieu=None, val='', **kw):
    loi = loi or []; thieu = thieu or []
    if thieu and not loi and 'ket_qua' not in kw: kw['ket_qua'] = 'THIẾU'
    return dict(ok=ok and not loi and not thieu, loi=loi, thieu=thieu, val=val, note='; '.join((loi + thieu)[:5]), **kw)


def _sat(name, v, thr):
    return [f'{name} {v} (ngưỡng {thr})'] if thr and abs(v - thr) <= 0.05 * abs(thr) else []


# ================================================================ máy quay → AGL (km)
def _ease(u):
    u = min(1.0, max(0.0, u)); return 4 * u ** 3 if u < 0.5 else 1 - (-2 * u + 2) ** 3 / 2


def _keys(keys, dur):
    return sorted([dict(k, t=_n(k.get('t')) if _n(k.get('t')) is not None else (_n(k.get('u')) or 0.0) * dur) for k in keys
                   if isinstance(k, dict) and (_n(k.get('t')) is not None or _n(k.get('u')) is not None or 't' not in k)], key=lambda k: k['t'])


def relief_at(keys, dur, t):
    """relief.js spline(): Hermite, tiếp tuyến Catmull-Rom theo thời gian, dist theo log → (dist km, tilt°)"""
    K = _keys(keys, dur)
    if not K: return None
    val = lambda k, f: math.log(max(_n(k.get('dist')) or 600.0, 1e-6)) if f == 'dist' else (_n(k.get(f)) or 0.0)
    if len(K) == 1: return math.exp(val(K[0], 'dist')), val(K[0], 'tilt')
    i = 0
    while i < len(K) - 2 and t > K[i + 1]['t']: i += 1
    a, b = K[i], K[i + 1]; h = (b['t'] - a['t']) or 1e-9; u = (t - a['t']) / h; out = []
    for f in ('dist', 'tilt'):
        p0, p1 = val(a, f), val(b, f)
        m0 = (p1 - val(K[i - 1], f)) / ((b['t'] - K[i - 1]['t']) or 1e-9) if i > 0 else (p1 - p0) / h
        m1 = (val(K[i + 2], f) - p0) / ((K[i + 2]['t'] - a['t']) or 1e-9) if i + 2 < len(K) else (p1 - p0) / h
        u2, u3 = u * u, u * u * u
        out.append((2 * u3 - 3 * u2 + 1) * p0 + (u3 - 2 * u2 + u) * h * m0 + (-2 * u3 + 3 * u2) * p1 + (u3 - u2) * h * m1)
    return math.exp(out[0]), out[1]


PRESET_ALT = {   # map.js MAP_PRESETS: [(u, alt | ('o', mặc định, hệ số), tilt)]
    'orbit': [(0, 26, 0), (1, 24, 0)], 'flyto': [(0, 28, 0), (0.25, 22, 0), (1, ('o', 2.6, 1), 32)],
    'pullback': [(0, ('o', 2.4, 1), 34), (1, 22, 0)], 'tilt-low': [(0, ('o', 3, 1.1), 50), (1, ('o', 3, 1), 54)],
    'top': [(0, ('o', 5, 1.08), 0), (1, ('o', 5, 1), 0)], 'pan': [(0, ('o', 6, 1), 30), (1, ('o', 6, 1), 30)],
    'pair': [(0, 24, 0), (0.33, 2.8, 34), (0.45, 3.0, 34), (0.62, 6, 18), (0.85, 2.8, 36), (1, 2.5, 38)]}


def globe_keys(o):
    if isinstance(o.get('cam'), list) and o['cam']: return o['cam'], 'opt.cam'
    P = PRESET_ALT.get(str(o.get('preset') or 'default'))
    if P is None: return [dict(u=0, alt=26, tilt=0), dict(u=1, alt=24, tilt=0)], 'mặc định map.js'
    oa = _n(o.get('alt'))
    return [dict(u=u, alt=(a if not isinstance(a, tuple) else (oa or a[1]) * a[2]), tilt=tl) for u, a, tl in P], f"preset {o.get('preset')}"


def globe_at(keys, dur, t):
    """map.js keyTrack(): easeIO giữa hai mốc, alt theo log → AGL km trên mặt cầu"""
    K = _keys(keys, dur)
    if not K: return None
    if len(K) == 1 or t <= K[0]['t']: a = b = K[0]; u = 0.0
    else:
        i = 0
        while i < len(K) - 2 and t > K[i + 1]['t']: i += 1
        a, b = K[i], K[i + 1]; u = _ease((t - a['t']) / (b['t'] - a['t'])) if b['t'] > a['t'] else 1.0
    alt = math.exp((1 - u) * math.log(_n(a.get('alt')) or 26) + u * math.log(_n(b.get('alt')) or 26))
    tl = math.radians((1 - u) * (_n(a.get('tilt')) or 0) + u * (_n(b.get('tilt')) or 0))
    d = math.sqrt(R_GLOBE ** 2 + alt ** 2 + 2 * R_GLOBE * alt * math.cos(tl))
    return (d - R_GLOBE) * KM_UNIT


def _geo(scene):
    s = str(scene or '')
    return 'globe' if s.startswith('map/globe') else ('relief' if s.startswith('relief/') else None)


# ================================================================ dữ liệu tập kênh 2
def shots(E, TL):
    """→ [dict(seg, i, t0, t1, ty, scene, geo, hero, p, h, spec, agl=[(t, km)], noi, where)] phim chính"""
    from checks.ll import q_k2var
    TH = TL.get('heroes') or {}; out = []
    for z in q_k2var.shots(E, TL):
        p = z['sh'].get('p') or {}; k = z['hero']; h = dict((E.get('heroes') or {}).get(k) or {}, **(TH.get(k) or {}))   # timeline thắng: mốc "@từ" đã giải
        o = h.get('opt') or {}; sc = z['scene'] if z['scene'] not in (None, 'None') else str(h.get('hero') or '')
        geo = _geo(h.get('hero') or sc) or ('tl' if z['ty'] == 'timelapse' else None)
        if z['ty'] == 'card': geo = None
        noi = z['spec'].get('noi') or (z['spec'].get('p') or {}).get('noi') or p.get('noi') or o.get('noi')
        agl, src = [], ''
        st = z['sh'].get('t0') or 0.0; f0 = _n(p.get('frame0')) if _n(p.get('frame0')) is not None else (_n(p.get('off')) or 0.0)
        sp = _n(p.get('speed')) or 1.0; dur = _n(h.get('dur')) or (z['t1'] - z['t0'])
        if isinstance(p.get('agl'), list):   # bộ dựng ghi AGL mỗi mốc (V5b-2b): [[giây trong shot, km], …]
            agl = [(z['t0'] + float(a), float(b)) for a, b in p['agl']]; src = 'agl khai'
        elif geo in ('relief', 'globe'):
            keys, src = (o.get('cam'), 'opt.cam') if geo == 'relief' else globe_keys(o)
            n = max(1, int(round((z['t1'] - z['t0']) / STEP)))
            for j in range(n + 1):
                tt = z['t0'] + min(j * STEP, z['t1'] - z['t0']); tau = (tt - z['t0']) * sp + f0 / 24
                if geo == 'relief':
                    v = relief_at(keys or [dict(u=0, dist=600, tilt=25), dict(u=1, dist=560, tilt=28)], dur, tau)
                    km = v[0] * math.cos(math.radians(v[1])) if v else None
                else: km = globe_at(keys, dur, tau)
                if km is not None: agl.append((round(tt, 3), round(km, 3)))
        from checks.ll import q_bando
        sok, swhy = q_bando.strat_info(z['ty'], sc, z['spec'], p, o)
        out.append(dict(seg=z['seg'], i=z['i'], t0=z['t0'], t1=z['t1'], ty=z['ty'], scene=sc, geo=geo, hero=k, p=p, h=h, o=o, spec=z['spec'],
                        agl=agl, agl_src=src, noi=noi, where=str(p.get('where') or '').strip(), strat=z['ty'] == 'strategic', strat_ok=sok, strat_why=swhy))
    return out


def _w(z): return f"{z['seg']}/{z['i']} {z['hero'] or z['ty']} @{mmss(z['t0'])}"


def city_chip(s):
    return bool(s) and bool(CITY_CHIP.match(s)) and not NOT_CITY.search(s)


def layer_of(z, v117=False):
    """lớp nhà khai của shot thành phố (tập không có mặt nạ fabric). v117 (1.17, CHỈ tập từ T3 — V7C-D5): thêm khoá lớp nhà của cảnh tl/*
    (opt.bfile, cityOpt, pre1704town, pho2026) và trường chung `lop_nha` (q_k117.co_lop_nha)."""
    o = z['o']
    if z['ty'] in ('photo', 'document', 'record', 'footage'): return 'ảnh/footage'
    for k in ('aerial', 'city', 'buildings', 'ghost', 'fabric'):
        if o.get(k) or z['p'].get(k): return {'aerial': 'ảnh hàng không'}.get(k, k)
    if v117:
        from checks.ll import q_k117
        return q_k117.co_lop_nha(z)
    return None


def _segs_from_frames(frames, dt):
    """[(t, x)] (x bool) → [(t0, t1)] quãng x liền nhau; khoảng lấy mẫu ≤ 1,5·dt coi là liền"""
    S = []
    for t, x in frames:
        if not x: continue
        if S and t - S[-1][1] <= 1.5 * dt + 1e-6: S[-1][1] = t
        else: S.append([t, t])
    return [(a, b + dt) for a, b in S]


# ================================================================ NC-H1 … NC-H4 trên tập
def nc_tap(E, TL):
    S = shots(E, TL); T = float(TL['tong_s'])
    geo = [z for z in S if z['agl'] and not z['strat_ok']]   # 1.14: strategic hợp lệ ra khỏi NC-H2/H3
    so = [z for z in S if z['strat_ok']]; sx = (f" · loại strategic hợp lệ {len(so)} shot ({sum(z['t1'] - z['t0'] for z in so):.1f} s) khỏi NC-H2/H3"
                                               if any(z['strat'] for z in S) else '')
    # ---- NC-H1
    from checks.ll import q_k116
    v117 = q_k116.ap_116(E)   # 1.17 (V7C-D5): lớp nhà khai của cảnh tl/* — chỉ tập từ T3
    L1, th1, units, rows1, near1 = [], [], [], [], []
    for z in S:
        if z['strat']: continue   # 1.14: bản đồ chiến lược không bao giờ là cảnh thành phố
        if z['geo'] is None and not z['noi']: continue
        lowalt = any(km <= CITY_KM for _, km in z['agl'])
        if z['noi']: city, why = str(z['noi']).strip().lower() in ('thanh_pho', 'thành phố', 'city'), f"khai noi: {z['noi']}"
        elif lowalt: city, why = True, f'suy: AGL ≤ {CITY_KM:g} km'
        elif city_chip(z['where']): city, why = True, f'suy: chip "{z["where"]}"'
        else: continue
        if not city: continue
        units.append(z); lay = layer_of(z, v117); fab = z['p'].get('fabric_pct') if isinstance(z['p'].get('fabric_pct'), list) else None
        if fab:
            med = statistics.median(fab); mn = min(fab)
            rows1.append(f"{_w(z)} ({why}): fabric trung vị {med:.1f} %, min {mn:.1f} %")
            if med < FAB_MED: L1.append(f"(a) {_w(z)} ({why}): fabric_pct trung vị {med:.1f} % < {FAB_MED:g} %")
            if mn < FAB_MIN: L1.append(f"(b) {_w(z)} ({why}): khung fabric_pct {mn:.1f} % < {FAB_MIN:g} %")
            near1 += _sat(f'{_w(z)} fabric trung vị', round(med, 1), FAB_MED)
        elif lay:
            rows1.append(f"{_w(z)} ({why}): lớp nhà khai = {lay} (không đo fabric)"); th1.append(f"{_w(z)}: fabric_pct không đo (lớp khai: {lay}; cần mặt nạ mọi khung)")
        else:
            rows1.append(f"{_w(z)} ({why}): {z['scene']} không có lớp nhà → fabric 0 % theo đặc tả")
            L1.append(f"(a) {_w(z)} ({why}): cảnh {z['scene']} không có lớp nhà/đường (fabric 0 % theo đặc tả) < {FAB_MED:g} %")
    tl1 = sum(z['t1'] - z['t0'] for z in units)
    H1 = r(True, L1, [], val=f"{len(units)} shot thành phố ({tl1:.1f} s; khai {sum(1 for z in units if z['noi'])}, suy {sum(1 for z in units if not z['noi'])})"
                           f" · có lớp nhà khai {sum(1 for z in units if layer_of(z, v117))} · không lớp nhà {sum(1 for z in units if not layer_of(z, v117) and not isinstance(z['p'].get('fabric_pct'), list))}"
                           f" · không đo fabric {len(th1)}", sat_nguong=near1, chi_tiet=rows1, khong_do=th1)
    # ---- NC-H2
    fr = sorted(((t, km, z) for z in geo for t, km in z['agl']), key=lambda x: x[0])
    runs = []
    for t, km, z in fr:
        if km <= GLOBE_KM: continue
        if runs and t - runs[-1]['t1'] <= 1.5 * STEP + 1e-6: runs[-1]['t1'] = t; runs[-1]['z'].add(_w(z)); runs[-1]['max'] = max(runs[-1]['max'], km); runs[-1]['geo'].add(z['geo'])
        else: runs.append(dict(t0=t, t1=t, z={_w(z)}, max=km, geo={z['geo']}))
    for x in runs: x['t1'] = min(x['t1'] + STEP, T); x['d'] = round(x['t1'] - x['t0'], 2)
    L2, near2 = [], []
    if len(runs) > GLOBE_N: L2.append(f"(a) {len(runs)} lần địa cầu (AGL > {GLOBE_KM:g} km) > {GLOBE_N}/tập")
    for x in runs:
        if x['d'] > GLOBE_S: L2.append(f"(b) {mmss(x['t0'])}–{mmss(x['t1'])} {x['d']} s > {GLOBE_S:g} s · cao nhất {x['max']:,.0f} km · {'/'.join(sorted(x['geo']))} · {', '.join(sorted(x['z']))}")
        near2 += _sat(f"lần địa cầu {mmss(x['t0'])}", x['d'], GLOBE_S)
    tg = sum(x['d'] for x in runs)
    H2 = r(True, L2, [] if geo else ['không có shot bản đồ/địa cầu có máy quay đọc được'],
           val=f"{len(runs)} lần · {tg:.1f} s ({100 * tg / T:.1f} % phim) · map/globe {sum(x['d'] for x in runs if x['geo'] == {'globe'}):.1f} s"
               f" · bản đồ nổi tầm cao {sum(x['d'] for x in runs if 'relief' in x['geo']):.1f} s · dài nhất {max([x['d'] for x in runs] or [0])} s" + sx, sat_nguong=near2, lan=runs and [
               dict(t0=round(x['t0'], 2), t1=round(x['t1'], 2), d=x['d'], max_km=round(x['max']), geo=sorted(x['geo']), shot=sorted(x['z'])) for x in runs])
    # ---- NC-H3
    d3 = len(fr) * STEP; lo = sum(STEP for _, km, _ in fr if km <= RANGE_KM); ci = sum(STEP for _, km, _ in fr if km <= CITY_KM)
    p_lo, p_ci = (100 * lo / d3, 100 * ci / d3) if d3 else (0.0, 0.0); L3 = []
    if d3 and p_lo < RANGE_PCT: L3.append(f"(a) AGL ≤ {RANGE_KM:g} km {p_lo:.1f} % thời lượng 3D địa lý < {RANGE_PCT:g} %")
    if d3 and units and p_ci < CITY_PCT: L3.append(f"(b) tập có thành phố ({len(units)} shot): AGL ≤ {CITY_KM:g} km {p_ci:.1f} % < {CITY_PCT:g} %")
    H3 = r(True, L3, [] if d3 else ['không có thời lượng 3D địa lý'], val=f"3D địa lý {d3:.1f} s · AGL ≤ {RANGE_KM:g} km {p_lo:.1f} % · ≤ {CITY_KM:g} km {p_ci:.1f} %"
           f" · có thành phố: {'có' if units else 'không'}" + sx, sat_nguong=_sat('AGL ≤ 60 km %', round(p_lo, 1), RANGE_PCT) + (_sat('AGL ≤ 3 km %', round(p_ci, 1), CITY_PCT) if units else []),
           pct_60=round(p_lo, 1), pct_3=round(p_ci, 1), giay_3d=round(d3, 2))
    # ---- NC-H4
    names = {str(x).strip().lower() for x in E.get('places') or [] if str(x).strip()}
    names |= {re.sub(r"'s$", '', n) for n in names}
    for z in S:
        o = z['o']
        for x in o.get('places') or []:
            if isinstance(x, dict) and x.get('name'): names.add(str(x['name']).strip().lower())
        for k in ('focus', 'from', 'to'):
            if isinstance(o.get(k), str): names.add(o[k].strip().lower())
        if z['where']: names.add(z['where'].lower())
    names = {n for n in names if len(n) >= 3}
    L4, ok4, mp = [], [], [z for z in S if z['geo'] in ('relief', 'globe', 'tl') or z['ty'] in ('map', 'timelapse')]
    for z in mp:
        if z['where']: ok4.append((z, f'chip "{z["where"]}"')); continue
        o, p = z['o'], z['p']; T4 = []
        for x in (p.get('tags') or []) + (p.get('places') or []) + (o.get('places') or []) + (o.get('pins') or []) + (o.get('labels') or []) + (o.get('regions') or []):
            if isinstance(x, dict): T4 += [str(x[k]) for k in ('s', 'name', 'label', 'text', 'sub') if isinstance(x.get(k), str)]
            elif isinstance(x, str): T4.append(x)
        hit = next((s for s in T4 if any(re.search(r'(?<![\w])' + re.escape(n) + r'(?![\w])', s.lower()) for n in names)), None)
        if hit: ok4.append((z, f'nhãn "{hit[:30]}"'))
        else: L4.append(f"{_w(z)} ({z['scene']}): không có chip nơi hay nhãn địa danh")
    H4 = r(True, L4, [], val=f"{len(mp)} shot bản đồ · chip nơi {sum(1 for _, w in ok4 if w.startswith('chip'))} · nhãn địa danh {sum(1 for _, w in ok4 if w.startswith('nhãn'))}"
           f" · thiếu {len(L4)} (nguồn: đặc tả, không log chữ)", co=[f'{_w(z)}: {w}' for z, w in ok4])
    H5 = r(True, [], [], val='không áp (tập không có bộ đếm năm/timelapse)', ket_qua='KHÔNG ÁP')
    return {'NC-H1': H1, 'NC-H2': H2, 'NC-H3': H3, 'NC-H4': H4, 'NC-H5': H5}


# ================================================================ NC-H1 … NC-H5 trên bộ timelapse
def nc_bo(B, base='.'):
    from checks.ll import q_tl
    F = q_tl._frames(q_tl._ld(base, B['campath'])); fps = B.get('fps', q_tl.FPS); T = len(F) / fps
    M = q_tl._ld(base, B.get('mat_na')) if B.get('mat_na') else None
    if isinstance(M, dict): M = M.get('frames') or M.get('khung')
    M = {int(m['f']): m for m in M or []}
    agl = [(_n(f.get('agl')) / 1000 if _n(f.get('agl')) is not None else None) for f in F]
    tt = lambda i: i / fps
    # ---- đơn vị NC-H1
    NOI = B.get('noi') or []
    def noi_of(i):
        t = tt(i)
        for w in NOI:
            if w['t'][0] - 1e-6 <= t < w['t'][1] - 1e-6: return str(w.get('noi')).strip().lower()
        return None
    city = []
    for i in range(len(F)):
        nv = noi_of(i)
        if nv is not None: city.append(nv in ('thanh_pho', 'thành phố', 'city'))
        else: city.append(agl[i] is not None and agl[i] <= CITY_KM)
    suy = not NOI
    exempt = set()
    for rv in B.get('reveal') or []:
        if rv.get('kieu') == 'keo_lui':
            a, b = rv['t']; exempt |= {i for i in range(len(F)) if b - REVEAL_TAIL - 1e-6 <= tt(i) < b}
    L1, th1, near1 = [], [], []; ci = [i for i in range(len(F)) if city[i]]
    if not M: th1.append('không có mặt nạ mọi khung (mat_na) — fabric_pct không đo')
    fab = {i: _n(M[i].get('fabric_pct')) for i in ci if i in M and _n(M[i].get('fabric_pct')) is not None} if M else {}
    if M and ci and len(fab) < len(ci): th1.append(f'mặt nạ thiếu fabric_pct ở {len(ci) - len(fab)}/{len(ci)} khung thành phố')
    if fab:
        med = statistics.median(fab.values())
        if med < FAB_MED: L1.append(f"(a) fabric_pct trung vị {med:.1f} % < {FAB_MED:g} % (khung thành phố {len(ci)})")
        near1 += _sat('fabric trung vị', round(med, 1), FAB_MED)
        low = _segs_from_frames([(tt(i), fab.get(i, 99) < FAB_MIN and i not in exempt) for i in ci], 1 / fps)
        for a, b in low:
            ii = [i for i in ci if a - 1e-6 <= tt(i) < b]; mn = min(fab[i] for i in ii if i in fab)
            L1.append(f"(b) {mmss(a)}–{mmss(b)} ({b - a:.2f} s): fabric_pct thấp nhất {mn:.1f} % < {FAB_MIN:g} % (khung {ii[0]}–{ii[-1]}"
                      f"{', pha ' + '/'.join(sorted({str(F[i].get('phase')) for i in ii})) if 'phase' in F[0] else ''})")
        val1 = (f"{len(ci)}/{len(F)} khung thành phố ({'suy AGL ≤ 3 km' if suy else 'khai noi'}) · fabric trung vị {med:.1f} % · min {min(fab.values()):.1f} %"
                f" · khung < {FAB_MIN:g} % (ngoài đuôi reveal) {sum(1 for i in ci if fab.get(i, 99) < FAB_MIN and i not in exempt)}")
    else: val1 = f"{len(ci)}/{len(F)} khung thành phố · fabric không đo"
    H1 = r(True, L1, th1, val=val1, sat_nguong=near1)
    # ---- NC-H2 / H3
    have = [i for i in range(len(F)) if agl[i] is not None]
    runs = _segs_from_frames([(tt(i), agl[i] > GLOBE_KM) for i in have], 1 / fps); L2 = []
    if len(runs) > GLOBE_N: L2.append(f"(a) {len(runs)} lần địa cầu (AGL > {GLOBE_KM:g} km) > {GLOBE_N}")
    L2 += [f"(b) {mmss(a)}–{mmss(b)} {b - a:.2f} s > {GLOBE_S:g} s" for a, b in runs if b - a > GLOBE_S]
    H2 = r(True, L2, [] if have else ['campath không có agl'], val=f"{len(runs)} lần · AGL cao nhất {max([agl[i] for i in have] or [0]):.2f} km")
    p_lo = 100 * sum(1 for i in have if agl[i] <= RANGE_KM) / len(have) if have else 0.0
    p_ci = 100 * sum(1 for i in have if agl[i] <= CITY_KM) / len(have) if have else 0.0
    L3 = ([f"(a) AGL ≤ {RANGE_KM:g} km {p_lo:.1f} % < {RANGE_PCT:g} %"] if have and p_lo < RANGE_PCT else []) + \
         ([f"(b) AGL ≤ {CITY_KM:g} km {p_ci:.1f} % < {CITY_PCT:g} %"] if have and ci and p_ci < CITY_PCT else [])
    H3 = r(True, L3, [] if have else ['campath không có agl'], val=f"3D {len(have) / fps:.1f} s · AGL ≤ {RANGE_KM:g} km {p_lo:.1f} % · ≤ {CITY_KM:g} km {p_ci:.1f} %",
           pct_60=round(p_lo, 1), pct_3=round(p_ci, 1))
    # ---- log chữ
    LC = q_tl._ld(base, B.get('log_chu')) if B.get('log_chu') else None
    LC = (LC.get('frames') if isinstance(LC, dict) else LC) or []
    items = [(int(e['f']), x) for e in LC for x in e.get('text') or []]
    # ---- NC-H4
    names = {str(x).strip().lower() for x in B.get('dia_danh') or [] if str(x).strip()}
    hits = [x for _, x in items if x.get('role') in ('where', 'place') or (names and any(n in str(x.get('s', '')).lower() for n in names))]
    H4 = r(True, [] if hits else ['bộ timelapse: không có chip nơi (role where/place) hay nhãn trùng địa danh (bo-tl.dia_danh) trong log chữ'],
           [] if LC else ['không có log chữ'], val=f"{len(hits)} mục chữ nơi/địa danh trong log · role: {', '.join(sorted({str(x.get('role')) for _, x in items})) or '—'}")
    # ---- NC-H5
    L5, th5 = [], []
    NK = q_tl._ld(base, B.get('nam_khung')) if B.get('nam_khung') else None
    if NK is None: th5.append('(a) không có nam_khung (năm xây lớn nhất của phần tử đang hiện theo lớp, mỗi khung) — "mọc trước" không đo')
    else:
        bad = []
        for e in NK:
            f = int(e['f'])
            if f >= len(F): continue
            y = math.floor(_n(F[f].get('year')) or 0)
            for lop, ny in (e.get('nam_max') or {}).items():
                if _n(ny) is not None and ny > y: bad.append((f, lop, ny, y))
        for a, b in _segs_from_frames([(tt(f), True) for f, *_ in bad], 1 / fps):
            z = [x for x in bad if a - 1e-6 <= tt(x[0]) < b]
            L5.append(f"(a) {mmss(a)}–{mmss(b)}: {len(z)} khung có phần tử năm xây > bộ đếm ({z[0][1]} {z[0][2]} > {z[0][3]})")
    gl = [(f, x) for f, x in items if x.get('role') == 'ghost_src' or GHOST_TXT.search(str(x.get('s', '')))]
    gspan = _segs_from_frames(sorted({(tt(f), True) for f, x in gl if (_n(x.get('px1080')) or 0) >= SRC_PX - 0.5}), max(1 / fps, _step(LC) / fps))
    gtxt = '; '.join(sorted({f"\"{str(x.get('s'))[:40]}\" {x.get('px1080')} px" for _, x in gl}))[:160]
    first = next((i for i in sorted(M) if (_n(M[i].get('ghost_pct')) or 0) > GHOST_MIN), None) if M and any('ghost_pct' in m for m in M.values()) else None
    if M and any('ghost_pct' in m for m in M.values()):
        if first is None: pass
        else:
            t0 = tt(first); sp = next(((a, b) for a, b in gspan if a <= t0 + 0.5 and b - max(a, t0) >= GHOST_S - 1e-6), None)
            if not sp: L5.append(f"(b) ghost hiện lần đầu {mmss(t0)} (khung {first}) mà không có nhãn nguồn ghost ≥ {SRC_PX:g} px liền ≥ {GHOST_S:g} s từ ≤ 0,5 s sau đó"
                                 f" (nhãn tìm thấy: {', '.join(f'{mmss(a)}–{mmss(b)}' for a, b in gspan) or 'không'})")
    else:
        th5.append('(b) mặt nạ không có ghost_pct — lần đầu ghost hiện không đo')
        if gl and not any(b - a >= GHOST_S - 1e-6 for a, b in gspan):   # có nhãn nguồn ghost ⇒ phim có ghost; không nhãn nào đủ 3 s thì lần đầu cũng không đủ
            L5.append(f"(b) có ghost (nhãn nguồn ghost trong log) nhưng không nhãn nào ≥ {SRC_PX:g} px hiện liền ≥ {GHOST_S:g} s (dài nhất "
                      f"{max([b - a for a, b in gspan] or [0]):.2f} s)")
    H5 = r(True, L5, th5, val=f"nhãn ghost: {gtxt or 'không có'} · quãng ≥ {SRC_PX:g} px: {', '.join(f'{mmss(a)}–{mmss(b)} ({b - a:.2f} s)' for a, b in gspan) or '—'}"
                              f" · ghost lần đầu: {mmss(tt(first)) if first is not None else 'không đo'}")
    return {'NC-H1': H1, 'NC-H2': H2, 'NC-H3': H3, 'NC-H4': H4, 'NC-H5': H5}


def _step(LC):
    fs = sorted({int(e['f']) for e in LC}); d = [b - a for a, b in zip(fs, fs[1:]) if b > a]
    return statistics.median(d) if d else 1


def main():
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    g = lambda k: a[a.index('--' + k) + 1] if '--' + k in a else None
    if g('bo-tl'):
        p = g('bo-tl'); R = nc_bo(json.load(open(p)), os.path.dirname(os.path.abspath(p)))
    else:
        from checks.ll import base
        E = base.load(a[0]); E['_path'] = os.path.abspath(a[0]); R = nc_tap(E, json.load(open(g('tl') or os.path.join(E['out'], 'timeline.json'))))
    for k, v in R.items():
        kq = v.get('ket_qua') or ('ĐẠT' if v['ok'] else ('THIẾU' if not v['loi'] else 'TRƯỢT'))
        print(f"{k} {kq} · {v['val']}" + ''.join('\n  ' + x for x in (v['loi'] + v['thieu'])[:20]))
    if g('json'): json.dump(R, open(g('json'), 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
