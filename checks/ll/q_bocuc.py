#!/opt/cine/bin/python
"""BC2…BC4 bố cục cảnh timelapse (I3) — bản 1.15.0 (phiên K, 18/10/2026; chủ dự án duyệt I3 ngày 18/10). Mức CẢNH BÁO tới khi hiệu chuẩn trên
đoạn thử V5b-2c (mọi ngưỡng dưới đây là ngưỡng lệnh/tạm, chưa hiệu chuẩn trên hình thật). Định nghĩa: RULES-LL.md mục "1.15".

  q_bocuc.py <bo-tl.json> [--json ra.json]

Đầu vào = bộ timelapse (như q_tl.py; đường dẫn tương đối thư mục bộ):
  mat_na     mặt nạ nội dung MỌI khung của k2_measure ([{f, noi?, content_pct, fabric_pct?, nuoc_pct?, co_trong_pct? | trong_pct?, troi_pct?}])
  noi        [{t: [a, b], noi}] cửa sổ nơi theo shot (k2_measure); không có thì lấy `noi` từng khung của mat_na
  log_vat    log vật theo khung [{f, vat: [{id, loai: quan|tau|…, h_px (@1080) | box [x0, y0, x1, y1] (+ H), hien?: true}]}]
  hero_anh   {khung, mat_na, hero_id, min_pct?, phap_tuyen?} (như TL-Q1c; phap_tuyen = thư mục lượt pháp tuyến %05d.png, RGB = (n + 1) / 2)
BC2 (a) mỗi shot `noi: thanh_pho`: content_pct trung vị ≥ CONTENT_MIN (50 %) khung; (b) nước + cỏ/đất trống trung vị ≤ EMPTY_MAX (1/3)
    — cần trường nuoc_pct + co_trong_pct (hoặc trong_pct) trong mặt nạ; không có → THIẾU (mặt nạ k2v hiện chỉ có content/fabric/hero/ghost).
BC3 khối quân/tàu (loai quan | tau | quan_* | tau_*) đang hiện cao ≥ UNIT_PX (6 px @1080p); lỗi khi một vật thấp hơn liên tục > UNIT_RUN_S
    (0,5 s — bỏ quãng vào/ra khung); không có log_vat → THIẾU.
BC4 hero không "tấm phẳng" (CHỈ BÁO): mỗi quãng khung có hero (≥ min_pct % khung, mặc định 0,5): (a) chi tiết vùng hero = TB |Laplace 3×3| trên Y
    (thước MAU1, 640×360) trong mặt nạ hero co 2 px, trung vị ≥ HERO_DET (16); (b) nếu có lượt pháp tuyến: lệch góc TB của pháp tuyến so với
    pháp tuyến trung bình vùng hero, trung vị ≥ NORM_DEG (10°). Không có hero_anh → THIẾU.
Trong ±5 % quanh ngưỡng: nêu tên.
"""
import glob, json, os, statistics, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

FPS = 24
CONTENT_MIN, EMPTY_MAX = 50.0, 100.0 / 3
UNIT_PX, UNIT_RUN_S = 6.0, 0.5
HERO_DET, NORM_DEG, HERO_MIN = 16.0, 10.0, 0.5


def _ld(base, p):
    if p is None or isinstance(p, (list, dict)): return p
    q = p if os.path.isabs(p) else os.path.join(base, p)
    if q.endswith('.gz'):
        import gzip; return json.load(gzip.open(q))
    return json.load(open(q))


def r(loi=None, thieu=None, val='', **kw):
    loi, thieu = loi or [], thieu or []
    kq = kw.pop('ket_qua', None) or ('THIẾU' if thieu and not loi else None)
    return dict(ok=not loi and not thieu, ket_qua=kq, loi=loi, thieu=thieu, val=val, **kw)


def sat(name, v, thr): return [f'{name} {v} (ngưỡng {thr:g})'] if v is not None and abs(v - thr) <= 0.05 * abs(thr) else []


def mmss(t): return f'{int(t // 60)}:{t % 60:04.1f}'


# ------------------------------------------------------------------ BC2
def bc2(B, base, fps=FPS):
    if not B.get('mat_na'): return r(thieu=['không có mat_na (mặt nạ nội dung mọi khung của k2_measure)'], val='—')
    M = sorted(_ld(base, B['mat_na']), key=lambda x: x['f'])
    W = B.get('noi')
    if W: S = [(float(w['t'][0]), float(w['t'][1]), w['noi']) for w in W]
    else:
        S, cur = [], None
        for x in M:
            n = x.get('noi')
            if cur and n == cur[2] and x['f'] == cur[3] + 1: cur[1], cur[3] = (x['f'] + 1) / fps, x['f']
            else:
                if cur: S.append(tuple(cur[:3]))
                cur = [x['f'] / fps, (x['f'] + 1) / fps, n, x['f']]
        if cur: S.append(tuple(cur[:3]))
    TP = [(a, b) for a, b, n in S if n == 'thanh_pho']
    if not TP: return r(val='không có shot noi: thanh_pho', ket_qua='KHÔNG ÁP')
    loi, th, near, vs = [], [], [], []
    for a, b in TP:
        xs = [x for x in M if a <= x['f'] / fps < b]
        if not xs: th.append(f'shot thành phố {mmss(a)}–{mmss(b)}: mặt nạ không có khung'); continue
        c = [x['content_pct'] for x in xs if x.get('content_pct') is not None]
        if len(c) < len(xs): th.append(f'(a) shot {mmss(a)}–{mmss(b)}: {len(xs) - len(c)} khung thiếu content_pct')
        if c:
            md = statistics.median(c); fb = [x['fabric_pct'] for x in xs if x.get('fabric_pct') is not None]
            vs.append(f"{mmss(a)}–{mmss(b)}: nội dung trung vị {md:.1f} % (min {min(c):.1f}, < {CONTENT_MIN:g} %: {sum(1 for v in c if v < CONTENT_MIN)}/{len(c)} khung)"
                      + (f", fabric {statistics.median(fb):.1f} %" if fb else ''))
            if md < CONTENT_MIN: loi.append(f'(a) shot thành phố {mmss(a)}–{mmss(b)}: nội dung trung vị {md:.1f} % < {CONTENT_MIN:g} % khung')
            near += sat(f'(a) {mmss(a)} nội dung trung vị', round(md, 1), CONTENT_MIN)
        ok_e = all(x.get('nuoc_pct') is not None and (x.get('co_trong_pct') is not None or x.get('trong_pct') is not None) for x in xs)
        if not ok_e: th.append(f'(b) shot {mmss(a)}–{mmss(b)}: mặt nạ không có nuoc_pct + co_trong_pct/trong_pct — không đo được nước/cỏ trống'); continue
        md = statistics.median(x['nuoc_pct'] + (x['co_trong_pct'] if x.get('co_trong_pct') is not None else x['trong_pct']) for x in xs)
        vs.append(f'{mmss(a)}–{mmss(b)}: nước + trống trung vị {md:.1f} %')
        if md > EMPTY_MAX: loi.append(f'(b) shot thành phố {mmss(a)}–{mmss(b)}: nước + cỏ/đất trống trung vị {md:.1f} % > 1/3 khung')
        near += sat(f'(b) {mmss(a)} nước + trống', round(md, 1), EMPTY_MAX)
    return r(loi, th, '; '.join(vs) or '—', sat_nguong=near)


# ------------------------------------------------------------------ BC3
def _is_unit(v): return str(v.get('loai') or '').split('_')[0] in ('quan', 'tau')


def bc3(B, base, fps=FPS):
    if not B.get('log_vat'): return r(thieu=['không có log_vat (log vật theo khung: id, loai quan|tau, h_px @1080 hoặc box)'], val='—')
    L = sorted(_ld(base, B['log_vat']), key=lambda x: x['f']); H = float(B.get('H_log_vat', 1080))
    fs = [x['f'] for x in L]; step = min((b - a for a, b in zip(fs, fs[1:]) if b > a), default=1)
    low, hs, nv = {}, [], set()
    for x in L:
        for v in x.get('vat') or []:
            if not _is_unit(v) or v.get('hien') is False: continue
            h = v.get('h_px')
            if h is None and v.get('box'): h = (v['box'][3] - v['box'][1]) * 1080.0 / H
            if h is None: continue
            nv.add(str(v.get('id'))); hs.append(h)
            low.setdefault(str(v.get('id')), []).append((x['f'], h < UNIT_PX, h, v.get('loai')))
    if not hs: return r(thieu=['log_vat không có khối quân/tàu nào đang hiện có chiều cao'], val='—')
    loi = []
    for i, xs in low.items():
        best, at, mn, s0, prev = 0, None, None, None, None
        for f, lo, h, _ in xs:
            s0 = (s0 if (s0 is not None and prev is not None and f - prev <= step) else f) if lo else None
            if lo and f - s0 + step > best: best, at, mn = f - s0 + step, f, h
            prev = f
        if best / fps > UNIT_RUN_S: loi.append(f'{xs[0][3]} {i}: cao < {UNIT_PX:g} px liên tục {best / fps:.2f} s (tới khung {at}, {mn:.1f} px)')
    return r(loi, [], f'{len(nv)} khối quân/tàu · cao nhỏ nhất {min(hs):.1f} px · trung vị {statistics.median(hs):.1f} px · < {UNIT_PX:g} px: {sum(1 for h in hs if h < UNIT_PX)}/{len(hs)} mẫu',
             sat_nguong=sat('cao nhỏ nhất px', round(min(hs), 1), UNIT_PX))


# ------------------------------------------------------------------ BC4
def do_phang(khung, mat_na, hero_id, phap_tuyen=None):
    """→ dict(hero_pct, chi_tiet, lech_phap_tuyen_deg?) hoặc None khi khung không có hero"""
    import cv2, numpy as np
    im = cv2.imread(khung, cv2.IMREAD_COLOR); mk = cv2.imread(mat_na, cv2.IMREAD_COLOR)
    if im is None or mk is None: raise FileNotFoundError(khung if im is None else mat_na)
    mk = cv2.resize(mk, (im.shape[1], im.shape[0]), interpolation=cv2.INTER_NEAREST)
    hero = (mk[..., 2] > 128) & (mk[..., 1] < 90) & (np.abs(mk[..., 0].astype(int) - int(hero_id)) < 1)
    if not hero.any(): return None
    out = dict(hero_pct=round(100 * float(hero.mean()), 2))
    y = cv2.cvtColor(cv2.resize(im, (640, 360), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2YCrCb)[..., 0].astype(np.float32)
    lap = np.abs(cv2.Laplacian(y, cv2.CV_32F, ksize=1))
    h2 = cv2.erode(cv2.resize(hero.astype(np.uint8), (640, 360), interpolation=cv2.INTER_NEAREST), np.ones((5, 5), np.uint8)) > 0
    out['chi_tiet'] = round(float(lap[h2].mean()), 2) if h2.sum() >= 20 else None
    if phap_tuyen and os.path.exists(phap_tuyen):
        N = cv2.imread(phap_tuyen, cv2.IMREAD_COLOR)
        if N is not None:
            N = cv2.resize(N, (im.shape[1], im.shape[0]), interpolation=cv2.INTER_NEAREST)[..., ::-1].astype(np.float64) / 127.5 - 1.0
            v = N[hero]; v = v / np.maximum(np.linalg.norm(v, axis=1, keepdims=True), 1e-6); m = v.mean(axis=0); m /= max(np.linalg.norm(m), 1e-6)
            out['lech_phap_tuyen_deg'] = round(float(np.degrees(np.arccos(np.clip(v @ m, -1, 1))).mean()), 2)
    return out


def bc4(B, base, fps=FPS):
    H = B.get('hero_anh')
    if not H: return r(thieu=['không có hero_anh (khung không chữ + mặt nạ hero; tuỳ chọn phap_tuyen)'], val='—')
    P = lambda k: H[k] if os.path.isabs(H[k]) else os.path.join(base, H[k])
    kd, md, nd = P('khung'), P('mat_na'), P('phap_tuyen') if H.get('phap_tuyen') else None
    rows = {}
    for mp in sorted(glob.glob(os.path.join(md, '*.png'))):
        f = int(os.path.splitext(os.path.basename(mp))[0])
        kp = next((q for q in (os.path.join(kd, f'{f:05d}{e}') for e in ('.png', '.jpg')) if os.path.exists(q)), None)
        if not kp: continue
        x = do_phang(kp, mp, H['hero_id'], os.path.join(nd, f'{f:05d}.png') if nd else None)
        if x and x['hero_pct'] >= float(H.get('min_pct', HERO_MIN)) and x['chi_tiet'] is not None: rows[f] = x
    if not rows: return r(thieu=['không có khung nào có hero ≥ min_pct'], val='—')
    fs = sorted(rows); runs, cur = [], [fs[0]]
    gap = max(1, min((b - a for a, b in zip(fs, fs[1:])), default=1))
    for f in fs[1:]:
        if f - cur[-1] <= 2 * gap: cur.append(f)
        else: runs.append(cur); cur = [f]
    runs.append(cur); loi, vs, near = [], [], []
    for R in runs:
        d = statistics.median(rows[f]['chi_tiet'] for f in R); n = [rows[f]['lech_phap_tuyen_deg'] for f in R if rows[f].get('lech_phap_tuyen_deg') is not None]
        nm = f'khung {R[0]}–{R[-1]} ({len(R)} mẫu)'
        vs.append(f'{nm}: chi tiết hero {d:.1f}' + (f', lệch pháp tuyến {statistics.median(n):.1f}°' if n else ''))
        if d < HERO_DET: loi.append(f'(a) {nm}: hero "tấm phẳng" — chi tiết trung vị {d:.1f} < {HERO_DET:g} (thước MAU1, trong mặt nạ hero)')
        if n and statistics.median(n) < NORM_DEG: loi.append(f'(b) {nm}: hero "tấm phẳng" — lệch pháp tuyến trung vị {statistics.median(n):.1f}° < {NORM_DEG:g}°')
        near += sat(f'(a) {nm} chi tiết', round(d, 1), HERO_DET) + (sat(f'(b) {nm} pháp tuyến', round(statistics.median(n), 1), NORM_DEG) if n else [])
    return r(loi, [], '; '.join(vs), sat_nguong=near, khung=rows)


def check(B, base='.'):
    return {'BC2': bc2(B, base, B.get('fps', FPS)), 'BC3': bc3(B, base, B.get('fps', FPS)), 'BC4': bc4(B, base, B.get('fps', FPS))}


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    g = lambda k: a[a.index('--' + k) + 1] if '--' + k in a else None
    B = json.load(open(a[0])); R = check(B, os.path.dirname(os.path.abspath(a[0])))
    for k, v in R.items():
        print(f"{k} {v.get('ket_qua') or ('ĐẠT' if v['ok'] else 'CẢNH BÁO')} · {v['val']}" + ''.join('\n  ' + x for x in (v['loi'] + v['thieu'])[:20])
              + ('\n  sát ngưỡng: ' + '; '.join(v['sat_nguong']) if v.get('sat_nguong') else ''))
    if g('json'): json.dump({k: {kk: vv for kk, vv in v.items() if kk != 'khung'} for k, v in R.items()}, open(g('json'), 'w'), ensure_ascii=False, indent=1)
