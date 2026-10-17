#!/opt/cine/bin/python
"""TL-Q1…TL-Q9 + Q35-TL dạng tập timelapse thành phố — luật khoá bản 1.12.0 (phiên K, 16/10/2026; chủ dự án duyệt luật 16/10); 1.12.1 (17/10/2026;
chủ dự án duyệt 16–17/10: HH2, HH3, MM1–MM3, JJ1/KK1). Mặc định CHỈ BÁO (cấp: cap112.py).
Nguồn ngưỡng: research/timelapse/BAO-CAO.md §6.8 (nhánh timelapse-rd, TL-Q1…Q5) + TL-Q6 (lệnh chủ dự án 16/10). Định nghĩa: RULES-LL.md.

  q_tl.py <bo-tl.json> [--json ra.json]

Đầu vào = một "bộ timelapse" (JSON), mọi đường dẫn tương đối theo thư mục của tệp:
  campath   campath.json của bộ dựng: [{f, year, pos, look, fov?, dev_m?}] (hoặc {frames: [...]}); fps (mặc định 24)
  mat_bang  "x-z" (three.js: x đông, z = −bắc) | "xz" (x đông, z bắc) — toạ độ mặt bằng từ pos
  ngan_sach ngân sách chữ MỖI khung: [{f?, pct, center_unanchored_pct, cards?, min_px?}]
  log_chu   log chữ (lấy mẫu): [{f, text: [{s, role, px1080, ratio}]}] (render-log.json "frames" cũng nhận)
  tuyen     [{t: [t0, t1], pts: [[đông, bắc], …] | dung_dev_m: true, nguon, dich: [x, y, z]}]          TL-Q2
  reveal    [{t: [t0, t1], dich: [x, y, z] | truong: <khoá khoảng cách trong campath, vd d_tower>, kieu: keo_lui | zoom_in}]  TL-Q3
  anh       [{id, rights: <tệp RIGHTS.md>, neo_px_loi?: [px…]}]; then_now: {pose, phu: [t0, t1], hoa: [t0, t1], anh_chong} TL-Q4
  ket       [t0, t1] màn kết (mặc định 6 s cuối); nhan_sang: [{t: [t0,t1], ti_le}] (TL-Q1c, từ mặt nạ công trình)
  nam_toa   {lop: {<tên>: {loai: so_dang_ky | tang_chuan, nguon, nam: {năm: số toà}}}, moc: {năm: nguồn}, gia: [năm giả]}  TL-Q6
  1.12.1: mat_na (mặt nạ nội dung MỌI khung [{f, content_pct, hero_pct…}]) TL-Q8 · dia_hinh {tep, ext, buoc, shape, nguon} TL-Q2/Q7/Q8 ·
          hero_anh {khung, mat_na, hero_id, min_pct?} TL-Q1c · tuyen[].loai (pho | eo_dat | song | dai_lo), tuyen[].cao_do_m TL-Q2 ·
          campath: phase, preset, vai, agl, shots[].route_type, cuts (grammarLog của design/k2v/tl/campath.js)
Mục nào thiếu đầu vào → THIẾU (không ĐẠT), ghi rõ trong `thieu`.

TL-Q1 mốc đinh: mốc = quãng năm KHÔNG ĐỔI ≥ 1,0 s (bỏ quãng chạm khung đầu/cuối phim). (a) mỗi mốc 1,5–2,0 s; (b) cỡ chữ năm trong mốc
       / trung vị ngoài mốc ≥ 1,4×; (c) sáng TB trong mặt nạ công trình / phần còn lại ≥ 1,5; (d) có thẻ (cards > 0) giao mốc, liền ≥ 3 s,
       dòng nguồn (role src) không rỗng ≥ 38 px; (e) số mốc ≥ ⌈thời lượng / 180 s⌉.
TL-Q2 bay dọc phố/sông: ≥ 3 s liên tục máy cách tuyến (mặt bằng) ≤ 15 m và AGL ≤ trần loại tuyến (1.12.1, HH2: pho 120 m; eo_dat/song/dai_lo
       300 m; thiếu loại → pho); tuyến có nguồn; cuối quãng, đích lệch trục nhìn ≤ 10°.
TL-Q1(c) 1.12.1 (MM3): tương phản cục bộ hero ↔ vành 1,5× (Weber đối xứng, độ chói tuyến tính) ≥ 1,3 HOẶC L_hero mốc / L_hero ngoài mốc ≥ 1,3.
Q35-TL (HH3): bộ đếm "≈" không ESTIMATE chỉ ĐẠT khi dòng phương pháp "≈ = interpolated between counts" trong 6 s đầu.
TL-Q7 (MM2): năm/s cửa sổ 0,5 s: AGL ≤ 150 m → ≤ 10; crane/reveal → ≤ 20.   TL-Q8 (MM1): bay thấp cú liên hoàn content_pct trung vị ≥ 30 %.
TL-Q9 (JJ1/KK1, cấp tập): ≤ 2 liên hoàn, ≤ 1 vertigo, vai mọi pha, orbit 4–6 s, ≤ 90 °/s.
TL-Q3 reveal: trong 2–8 s, khoảng cách tới đích tăng ≥ 5× (kéo lùi) hoặc giảm ≥ 5× (zoom-in), không cắt (bước máy một khung ≤ max(50 m, 6×
       trung vị bước trong quãng)).
TL-Q4 ảnh lịch sử: (a) mỗi ảnh có dòng RIGHTS.md chứa id + giấy phép PD/CC0/CC BY + URL + SHA-256; (b) ảnh neo: đầu đường dẫn lệch điểm
       chiếu ≤ 1 % rộng khung mọi khung; (c) then/now: ≥ 6 điểm khống chế, RMS chiếu lại ≤ 1 % rộng ảnh (rộng = aspect · 2f·tan(fov/2)), có
       ảnh chồng 50 % cho người kiểm, máy đứng yên ≥ 0,8 s trong lúc ảnh phủ, hoà 0,6–1,5 s, ghi phương pháp.
TL-Q5 ngân sách chữ: (a) ≤ 15 % khung thường, ≤ 25 % khung mốc đinh (= quãng năm dừng ∪ quãng thẻ giao nó; không có số thẻ:
       năm dừng ± 0,5 s); (b) vùng giữa không có chữ không neo; (c) ≤ 1 thẻ/khung, mỗi thẻ 3–5 s,
       tiêu đề ≤ 10 từ; (d) ≤ 2 lớp thường trực (role year/index); (e) dòng phương pháp (role method) chỉ trong 6 s đầu + màn kết;
       (f) chữ ≥ 38 px@1080, tương phản ≥ 4,5:1.
TL-Q6 năm giả không mọc: lớp `so_dang_ky` không có toà nào mang năm giả (`gia`, mặc định 1005 BAG, 1812 GWR, 9999, 0) hay năm > năm hiện tại;
       lớp `tang_chuan` chỉ đổi trạng thái tại năm mốc có nguồn (`moc`, nguồn không rỗng).
"""
import json, math, os, re, statistics, sys

FPS = 24
GIA = (0, 1005, 1812, 9999)
LIC = re.compile(r'\b(CC0|CC[ -]BY(?![ -](?:NC|ND|SA-NC))|public domain|PD(?:-[A-Za-z]+)*)\b', re.I)


def _ld(base, p):
    if p is None or isinstance(p, (list, dict)): return p
    q = p if os.path.isabs(p) else os.path.join(base, p)
    if q.endswith('.gz'):
        import gzip; return json.load(gzip.open(q))
    return json.load(open(q))


def _frames(x): return x['frames'] if isinstance(x, dict) and 'frames' in x else x


def mmss(t): return f'{int(t // 60)}:{t % 60:04.1f}'


def r(ok, loi=None, thieu=None, val='', **kw):
    loi, thieu = loi or [], thieu or []
    kq = 'THIẾU' if thieu and not loi else None
    return dict(ok=ok and not loi and not thieu, ket_qua=kq, loi=loi, thieu=thieu, val=val, **kw)


def pins(F, fps):
    """quãng năm không đổi ≥ 1,0 s, bỏ quãng chạm khung đầu/cuối → [(f0, f1)]"""
    out, i, n = [], 0, len(F)
    while i < n:
        j = i
        while j + 1 < n and round(F[j + 1]['year'], 2) == round(F[i]['year'], 2): j += 1
        if (j - i + 1) / fps >= 1.0 and i > 0 and j < n - 1: out.append((F[i]['f'], F[j]['f']))
        i = j + 1
    return out


def _text(L):
    L = _frames(L) or []
    return {x['f']: x.get('text') or x.get('items') or [] for x in L if x.get('text') or x.get('items')}


TP_MIN, VANH_K = 1.3, 1.5   # 1.12.1 (MM3): tương phản cục bộ hero ↔ vành, hoặc hero ở mốc / hero ngoài mốc


def _lum(img_bgr):
    """độ chói tương đối TUYẾN TÍNH (sRGB → tuyến tính, hệ số Rec.709 — cùng định nghĩa với tương phản WCAG của TL-Q5f)"""
    import numpy as np
    x = img_bgr[..., ::-1].astype(np.float64) / 255.0
    x = np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)
    return 0.2126 * x[..., 0] + 0.7152 * x[..., 1] + 0.0722 * x[..., 2]


def weber(a, b):
    """|L_a − L_b| / min(L_a, L_b) trên độ chói tuyến tính (sàn 0,005 tránh chia cho 0 ở vùng đen tuyệt đối)"""
    return abs(a - b) / max(min(a, b), 0.005)


def do_hero(khung, mat_na, hero_id):
    """một khung không chữ + ảnh mặt nạ render.js --maskpng (R > 128 & G < 90 = nội dung; B = id hero) → số đo hero/vành, hoặc None nếu
    không có điểm ảnh hero. Vành = điểm ảnh trong hộp bao hero phóng 1,5× quanh tâm (cắt theo khung), KHÔNG thuộc hero."""
    import cv2, numpy as np
    im = cv2.imread(khung, cv2.IMREAD_COLOR); mk = cv2.imread(mat_na, cv2.IMREAD_COLOR)
    if im is None or mk is None: raise FileNotFoundError(khung if im is None else mat_na)
    mk = cv2.resize(mk, (im.shape[1], im.shape[0]), interpolation=cv2.INTER_NEAREST)
    b, g, rr = mk[..., 0].astype(int), mk[..., 1].astype(int), mk[..., 2].astype(int)
    hero = (rr > 128) & (g < 90) & (np.abs(b - int(hero_id)) < 1)
    if hero.sum() == 0: return None
    ys, xs = np.nonzero(hero); y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max(); cy, cx = (y0 + y1) / 2, (x0 + x1) / 2
    hh, hw = (y1 - y0 + 1) * VANH_K / 2, (x1 - x0 + 1) * VANH_K / 2
    Y0, Y1, X0, X1 = max(0, int(round(cy - hh))), min(im.shape[0], int(round(cy + hh)) + 1), max(0, int(round(cx - hw))), min(im.shape[1], int(round(cx + hw)) + 1)
    box = np.zeros_like(hero); box[Y0:Y1, X0:X1] = True; vanh = box & ~hero
    L = _lum(im); lh, lv = float(L[hero].mean()), float(L[vanh].mean()) if vanh.any() else float('nan')
    return dict(hero_pct=round(100 * hero.mean(), 2), l_hero=round(lh, 4), l_vanh=round(lv, 4), tuong_phan=round(weber(lh, lv), 3) if vanh.any() else None,
                vanh_pct=round(100 * vanh.mean(), 2), hop=[int(X0), int(Y0), int(X1), int(Y1)])


def tuong_phan_hero(H, base, P):
    """H = `hero_anh`: {khung: thư mục khung KHÔNG CHỮ (%05d.jpg|png), mat_na: thư mục mặt nạ (%05d.png), hero_id: số kênh B, ten?, min_pct?: 0,5}.
    Mỗi mốc đinh (P) ĐẠT nếu (i) trung vị tương phản cục bộ hero ↔ vành ≥ 1,3 trên các khung của mốc, HOẶC (ii) L_hero trung vị trong mốc /
    L_hero trung vị ngoài mốc (khung có hero ≥ min_pct % khung) ≥ 1,3 (hero được nhấn sáng hơn chính nó khi không ở mốc)."""
    import glob as _g
    th, rows, sat = [], {}, []
    kd = H['khung'] if os.path.isabs(H['khung']) else os.path.join(base, H['khung']); md = H['mat_na'] if os.path.isabs(H['mat_na']) else os.path.join(base, H['mat_na'])
    for mp in sorted(_g.glob(os.path.join(md, '*.png'))):
        f = int(os.path.splitext(os.path.basename(mp))[0]); kp = next((q for q in (os.path.join(kd, f'{f:05d}{e}') for e in ('.png', '.jpg')) if os.path.exists(q)), None)
        if kp:
            x = do_hero(kp, mp, H['hero_id'])
            if x: rows[f] = x
    mn = float(H.get('min_pct', 0.5)); out = []
    for a, b in P:
        IN = [rows[f] for f in sorted(rows) if a <= f <= b]; OUT = [rows[f] for f in sorted(rows) if not a <= f <= b and rows[f]['hero_pct'] >= mn]
        if not IN: th.append(f'(c) mốc khung {a}–{b}: không có khung không chữ + mặt nạ hero trong mốc'); out.append(dict(moc=(a, b), dat=None)); continue
        tv = statistics.median(x['tuong_phan'] for x in IN if x['tuong_phan'] is not None)
        tm = statistics.median(x['l_hero'] for x in IN) / max(statistics.median(x['l_hero'] for x in OUT), 0.005) if OUT else None
        dat = tv >= TP_MIN or (tm is not None and tm >= TP_MIN)
        for nm, v in (('tương phản hero ↔ vành', tv), ('hero mốc / hero ngoài mốc', tm)):
            if v is not None and abs(v - TP_MIN) <= 0.05 * TP_MIN: sat.append(f'(c) mốc {a}–{b}: {nm} {v:.3f} (ngưỡng {TP_MIN})')
        why = (f"tương phản cục bộ hero ↔ vành trung vị {tv:.2f} < {TP_MIN} và hero mốc / ngoài mốc "
               + (f'{tm:.2f} < {TP_MIN}' if tm is not None else 'không đo được (không có khung hero ngoài mốc)'))
        if not dat and tm is None: th.append(f'(c) mốc khung {a}–{b}: không có khung hero ngoài mốc để đo cách (ii)')
        out.append(dict(moc=(a, b), dat=dat, tuong_phan_vanh=round(tv, 3), ti_le_moc=None if tm is None else round(tm, 3), n_trong=len(IN), n_ngoai=len(OUT),
                        l_hero_moc=round(statistics.median(x['l_hero'] for x in IN), 4), l_vanh_moc=round(statistics.median(x['l_vanh'] for x in IN), 4),
                        l_hero_ngoai=round(statistics.median(x['l_hero'] for x in OUT), 4) if OUT else None, ly_do=why))
    val = '; '.join(f"mốc {o['moc'][0]}–{o['moc'][1]}: hero↔vành {o['tuong_phan_vanh']} (L {o['l_hero_moc']}/{o['l_vanh_moc']}), hero mốc/ngoài {o['ti_le_moc']} "
                    f"({o['n_trong']}/{o['n_ngoai']} khung) → {'ĐẠT' if o['dat'] else 'TRƯỢT'}" for o in out if o.get('dat') is not None) or 'không đo được'
    return dict(moc=out, khung=rows, thieu=th, sat=sat, val=val)


def tlq1(B, F, fps, T):
    P = pins(F, fps); M = {k: [] for k in 'abcde'}; th = []; TX = _text(B.get('log_chu')); NS = B.get('ngan_sach')
    for f0, f1 in P:
        d = (f1 - f0 + 1) / fps
        if not 1.5 <= d <= 2.0: M['a'].append(f'mốc {F[f0]["year"]:.0f} khung {f0}–{f1}: năm dừng {d:.2f} s ngoài 1,5–2,0 s')
    if TX:
        yo = [t['px1080'] for f, its in TX.items() for t in its if t.get('role') == 'year' and not any(a <= f <= b for a, b in P)]
        for f0, f1 in P:
            yi = [t['px1080'] for f, its in TX.items() if f0 <= f <= f1 for t in its if t.get('role') == 'year']
            if not yi or not yo: th.append(f'(b) mốc khung {f0}–{f1}: log chữ không có mẫu chữ năm trong/ngoài mốc')
            elif max(yi) / statistics.median(yo) < 1.4: M['b'].append(f'(b) mốc khung {f0}–{f1}: chữ năm {max(yi):.0f} px / {statistics.median(yo):.0f} px = {max(yi) / statistics.median(yo):.2f}× < 1,4×')
    else: th.append('(b), (d) dòng nguồn: không có log chữ')
    TC = None
    if B.get('hero_anh'):   # 1.12.1 (MM3): K đo tương phản cục bộ trên khung không chữ + mặt nạ hero
        TC = tuong_phan_hero(B['hero_anh'], B['_base'], P)
        th += TC['thieu']
        for x in TC['moc']:
            if x['dat'] is False: M['c'].append(f"(c) mốc khung {x['moc'][0]}–{x['moc'][1]}: " + x['ly_do'])
    else: th.append('(c) không có khung không chữ + mặt nạ hero (hero_anh) để đo tương phản cục bộ (1.12.1; nhan_sang sáng trong/ngoài không còn dùng)')
    if NS and all('cards' in z for z in NS):
        c = [bool(z.get('cards')) for z in NS]
        for f0, f1 in P:
            runs, i = [], 0
            while i < len(c):
                if c[i]:
                    j = i
                    while j + 1 < len(c) and c[j + 1]: j += 1
                    if j >= f0 and i <= f1: runs.append((i, j))
                    i = j + 1
                else: i += 1
            best = max(((j - i + 1) / fps for i, j in runs), default=0.0)
            if best < 3.0: M['d'].append(f'(d) mốc khung {f0}–{f1}: thẻ giao mốc dài nhất {best:.2f} s < 3 s')
            if TX:
                src = [t for f, its in TX.items() if any(i <= f <= j for i, j in runs) for t in its if t.get('role') == 'src']
                if not src: th.append(f'(d) mốc khung {f0}–{f1}: log chữ không có dòng nguồn của thẻ trong quãng thẻ')
                elif any(not str(t.get('s') or '').strip() or t['px1080'] < 38 for t in src): M['d'].append(f'(d) mốc khung {f0}–{f1}: dòng nguồn rỗng hoặc < 38 px')
    else: th.append('(d) ngân sách chữ không có số thẻ mỗi khung (cards)')
    need = max(1, math.ceil(T / 180.0))
    if len(P) < need: M['e'].append(f'(e) {len(P)} mốc đinh < {need} (≥ 1 mỗi 3 phút, phim {T:.1f} s)')
    loi = sum(M.values(), [])
    sat = TC['sat'] if TC else []
    return r(True, loi, th, sat_nguong=sat, val=f"{len(P)} mốc: " + ', '.join(f"{F[a]['year']:.0f} {(b - a + 1) / fps:.2f} s (khung {a}–{b})" for a, b in P)
             + (f" · (c) {TC['val']}" if TC else ''), muc=M, moc=P, tuong_phan=TC)


def _plan(p, mb): return (p[0], -p[2]) if mb == 'x-z' else (p[0], p[2])


def _dseg(px, py, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]; u = max(0.0, min(1.0, ((px - a[0]) * dx + (py - a[1]) * dy) / ((dx * dx + dy * dy) or 1)))
    return math.hypot(px - a[0] - u * dx, py - a[1] - u * dy)


def _offaxis(fr, tgt):
    v = [fr['look'][i] - fr['pos'][i] for i in range(3)]; w = [tgt[i] - fr['pos'][i] for i in range(3)]
    c = sum(a * b for a, b in zip(v, w)) / (math.hypot(*v) * math.hypot(*w) or 1); return math.degrees(math.acos(max(-1, min(1, c))))


ALT_MAX = {'pho': 120.0, 'eo_dat': 300.0, 'song': 300.0, 'dai_lo': 300.0}   # 1.12.1 (HH2): độ cao SO MẶT ĐẤT theo loại tuyến; thiếu loại → pho


def dia_hinh(B, base):
    """lưới địa hình của bộ (`dia_hinh`: {tep, ext: [đông0, bắc0, đông1, bắc1], buoc, shape: [hàng, cột], nguon}; hàng 0 = bắc1, như
    design/k2v/tl/terrain.js hAt) → hàm h(đông, bắc) nội suy song tuyến, hoặc None"""
    D = B.get('dia_hinh')
    if not D: return None
    H = _ld(base, D['tep']); H = H['h'] if isinstance(H, dict) else H
    e0, n0, e1, n1 = D['ext']; R, C = D['shape']; st = float(D['buoc'])

    def h(e, n):
        fc = max(0.0, min(C - 1.001, (e - e0) / st)); fr = max(0.0, min(R - 1.001, (n1 - n) / st)); c, r = int(fc), int(fr); a, b = fc - c, fr - r
        g = lambda rr, cc: H[rr * C + cc]
        return (g(r, c) * (1 - a) + g(r, c + 1) * a) * (1 - b) + (g(r + 1, c) * (1 - a) + g(r + 1, c + 1) * a) * b
    return h


def agl_cua(B, F, base, x, mb):
    """(hàm AGL theo khung, cách đo) — ưu tiên: (1) địa hình trong bộ (K tính), (2) `agl` mỗi khung của campath (bộ dựng tính từ địa hình),
    (3) độ cao tuyệt đối − cao độ tuyến (`tuyen[].cao_do_m`, hoặc toạ độ thứ 3 của pts), (4) độ cao tuyệt đối (cao độ tuyến không khai → coi 0 m:
    chặt hơn khi mặt đất > 0)"""
    h = dia_hinh(B, base)
    if h:
        def f(fr):
            e, n = _plan(fr['pos'], mb); return fr['pos'][1] - h(e, n)
        return f, f"AGL K tính từ địa hình của bộ ({(B['dia_hinh'].get('nguon') or 'không ghi nguồn')[:40]})"
    if F and all('agl' in fr for fr in F): return (lambda fr: fr['agl']), 'AGL của campath (bộ dựng tính từ địa hình)'
    z = x.get('cao_do_m')
    if z is None and x.get('pts') and all(len(p) >= 3 for p in x['pts']): z = statistics.mean(p[2] for p in x['pts'])
    if z is not None: return (lambda fr, z=float(z): fr['pos'][1] - z), f'độ cao tuyệt đối − cao độ tuyến {float(z):.1f} m'
    return (lambda fr: fr['pos'][1]), 'độ cao tuyệt đối (không có địa hình/cao độ tuyến → coi mặt đất 0 m)'


def loai_tuyen(B, x):
    """loại tuyến khai trong bộ: `tuyen[].loai`, không có → `campath.shots[].route_type` của cú phủ quãng tuyến; thiếu → pho"""
    if x.get('loai') in ALT_MAX: return x['loai'], 'tuyen.loai'
    if x.get('loai'): return 'pho', f"loại '{x['loai']}' không rõ → coi pho"
    for s in B.get('_shots') or []:
        t = s.get('t') or [0, 0]
        if s.get('route_type') in ALT_MAX and t[0] - 1e-6 <= x['t'][0] and x['t'][1] <= t[1] + 1e-6: return s['route_type'], 'campath.shots.route_type'
    return 'pho', 'không khai loại → coi pho'


def tlq2(B, F, fps, base='.'):
    TU = B.get('tuyen')
    if not TU: return r(True, thieu=['không khai tuyến bay (tuyen)'], val='—')
    loi, th, out, sat = [], [], [], []; mb = B.get('mat_bang', 'xz')
    for k, x in enumerate(TU):
        f0, f1 = round(x['t'][0] * fps), min(len(F) - 1, round(x['t'][1] * fps)); W = F[f0:f1 + 1]
        if x.get('pts'):
            d = [min(_dseg(*_plan(fr['pos'], mb), x['pts'][i][:2], x['pts'][i + 1][:2]) for i in range(len(x['pts']) - 1)) for fr in W]; cach = 'K tính từ hình học tuyến'
        elif x.get('dung_dev_m'):
            d = [fr.get('dev_m', math.inf) for fr in W]; cach = 'dev_m của campath (bộ dựng tính; tuyến không có trong repo)'
        else: th.append(f'tuyến {k}: không có hình học tuyến (pts) hay dev_m'); continue
        lt, lt_src = loai_tuyen(B, x); amax = ALT_MAX[lt]; ag, ag_src = agl_cua(B, F, base, x, mb); A = [ag(fr) for fr in W]
        best, cur, bi = (0, None), 0, None
        for i, (di, ai) in enumerate(zip(d, A)):
            if di <= 15.0 and ai <= amax:
                cur += 1; bi = i if cur == 1 else bi
                if cur > best[0]: best = (cur, (bi, i))
            else: cur = 0
        n_on = sum(di <= 15.0 for di in d); alt = [ai for di, ai in zip(d, A) if di <= 15.0]
        s = best[0] / fps
        if s < 3.0:
            why = f'chỉ {s:.2f} s liên tục ≤ 15 m và AGL ≤ {amax:.0f} m ({lt})' + (f' (≤ 15 m: {n_on / fps:.2f} s, nhưng AGL {min(alt):.0f}–{max(alt):.0f} m)' if alt and max(alt) > amax else '')
            loi.append(f'tuyến {k} {x["t"]}: {why}')
        if not str(x.get('nguon') or '').strip(): loi.append(f'tuyến {k}: không ghi nguồn hình học')
        oa = None
        if x.get('dich'):
            oa = _offaxis(W[best[1][1]] if best[1] else W[-1], x['dich'])
            if oa > 10.0: loi.append(f'tuyến {k}: cuối quãng đích lệch trục nhìn {oa:.1f}° > 10°')
        else: th.append(f'tuyến {k}: không khai đích (dich)')
        ins = [di for di in d if di <= 15.0]
        if best[1]:
            am = max(A[best[1][0]:best[1][1] + 1])
            if am >= 0.95 * amax: sat.append(f'tuyến {k}: AGL max trong quãng {am:.1f} m (trần {amax:.0f} m, {lt})')
        if 2.85 <= s <= 3.15: sat.append(f'tuyến {k}: quãng liên tục {s:.2f} s (ngưỡng 3 s)')
        out.append(dict(t=x['t'], lien_tuc_s=round(s, 2), cach=cach, loai=lt, loai_nguon=lt_src, tran_agl=amax, agl_cach=ag_src,
                        lech_tb=round(statistics.mean(ins), 2) if ins else None, lech_max=round(max(ins), 2) if ins else None,
                        agl=[round(min(alt), 1), round(max(alt), 1)] if alt else None, cao_tuyet_doi=[round(min(fr['pos'][1] for fr in W), 1), round(max(fr['pos'][1] for fr in W), 1)],
                        lech_truc=None if oa is None else round(oa, 1)))
    return r(True, loi, th, sat_nguong=sat, val='; '.join(f"{o['t']}: {o['lien_tuc_s']} s ≤ 15 m/AGL ≤ {o['tran_agl']:.0f} m ({o['loai']}: {o['loai_nguon']}), lệch TB {o['lech_tb']} m, max {o['lech_max']} m, "
                                         f"AGL {o['agl']} ({o['agl_cach']}), đích {o['lech_truc']}° ({o['cach']})" for o in out), tuyen=out)


def tlq3(B, F, fps):
    RV = B.get('reveal')
    if not RV: return r(True, thieu=['không khai reveal'], val='—')
    loi, out = [], []
    for x in RV:
        f0, f1 = round(x['t'][0] * fps), min(len(F) - 1, round(x['t'][1] * fps)); W = F[f0:f1 + 1]; dur = (f1 - f0) / fps
        dd = (lambda fr: fr[x['truong']]) if x.get('truong') else (lambda fr: math.dist(fr['pos'], x['dich']))
        d0, d1 = dd(W[0]), dd(W[-1])
        st = [math.dist(W[i]['pos'], W[i - 1]['pos']) for i in range(1, len(W))]; med = statistics.median(st) if st else 0
        cut = [W[i]['f'] for i in range(1, len(W)) if st[i - 1] > max(50.0, 6 * med)]
        kieu = x.get('kieu') or ('keo_lui' if d1 > d0 else 'zoom_in'); ti = d1 / d0 if kieu == 'keo_lui' else d0 / d1
        if ti < 5.0: loi.append(f"{kieu} {x['t']}: {d0:.0f} → {d1:.0f} m = ×{ti:.2f} < 5×")
        if not 2.0 <= dur <= 8.0: loi.append(f"{kieu} {x['t']}: dài {dur:.2f} s ngoài 2–8 s")
        if cut: loi.append(f"{kieu} {x['t']}: cắt/nhảy máy ở khung {cut[:3]}")
        out.append(f"{kieu} {x['t'][0]}–{x['t'][1]} s: {d0:.0f} → {d1:.0f} m ×{ti:.1f} trong {dur:.1f} s")
    return r(True, loi, val='; '.join(out))


def _still(F, fps, t0, t1):
    """giây dài nhất máy đứng yên (pos, look trùng khung trước) trong [t0, t1]"""
    best = cur = 0
    for i in range(max(1, round(t0 * fps)), min(len(F), round(t1 * fps) + 1)):
        same = F[i]['pos'] == F[i - 1]['pos'] and F[i]['look'] == F[i - 1]['look']; cur = cur + 1 if same else 0; best = max(best, cur)
    return (best + 1) / fps if best else 0.0


def tlq4(B, F, fps, base):
    loi, th, v = [], [], []
    for a in B.get('anh') or []:
        rp = a.get('rights'); txt = open(rp if os.path.isabs(rp) else os.path.join(base, rp)).read() if rp and os.path.exists(rp if os.path.isabs(rp) else os.path.join(base, rp)) else None
        if txt is None: th.append(f"(a) {a['id']}: không có tệp RIGHTS để kiểm"); continue
        ln = [l for l in txt.splitlines() if a['id'] in l]
        good = [l for l in ln if LIC.search(l) and re.search(r'https?://', l) and re.search(r'\b[0-9a-f]{64}\b', l)]
        if not good: loi.append(f"(a) {a['id']}: RIGHTS.md " + ('không có dòng nào' if not ln else 'có dòng nhưng thiếu giấy phép PD/CC0/CC BY, URL hoặc SHA-256 đủ 64 ký tự'))
        v.append(f"{a['id']}: RIGHTS {'đủ' if good else 'thiếu'}")
        if a.get('neo'):
            e = a.get('neo_px_loi')
            if e is None: th.append(f"(b) {a['id']}: không có log lệch đầu đường dẫn ↔ điểm chiếu 3D theo khung")
            elif max(e) > 0.01 * B.get('rong_khung', 1920): loi.append(f"(b) {a['id']}: lệch {max(e):.1f} px > 1 % rộng khung")
    tn = B.get('then_now')
    if tn:
        P = _ld(base, tn['pose']); n = len(P.get('reproj_px') or {}); rms = P.get('reproj_rms_px')
        w = P['aspect'] * 2 * P['params']['f'] * math.tan(math.radians(P['fov_v_deg']) / 2); pct = 100 * rms / w
        if n < 6: loi.append(f'(c) then/now: {n} điểm khống chế < 6')
        if pct > 1.0: loi.append(f'(c) then/now: RMS {rms:.1f} px = {pct:.2f} % rộng ảnh > 1 %')
        if not str(P.get('method') or '').strip(): loi.append('(c) then/now: không ghi phương pháp căn góc')
        ac = tn.get('anh_chong')
        if not ac or not os.path.exists(ac if os.path.isabs(ac) else os.path.join(base, ac)): th.append('(c) then/now: không có ảnh chồng 50 % cho người kiểm trong repo')
        s = _still(F, fps, *tn['phu']); hd = tn['hoa'][1] - tn['hoa'][0]
        if s < 0.8: loi.append(f'(c) then/now: máy đứng yên {s:.2f} s < 0,8 s trong lúc ảnh phủ {tn["phu"]}')
        if not 0.6 <= hd <= 1.5: loi.append(f'(c) then/now: hoà {hd:.2f} s ngoài 0,6–1,5 s')
        v.append(f'then/now {n} điểm, RMS {rms:.1f}/{w:.0f} px = {pct:.2f} %, máy yên {s:.2f} s khi ảnh phủ, hoà {hd:.2f} s')
    if not B.get('anh') and not tn: th.append('không khai ảnh lịch sử')
    return r(True, loi, th, val='; '.join(v))


def tlq5(B, F, fps, T, moc):
    NS = B.get('ngan_sach'); TX = _text(B.get('log_chu')); loi, th = [], []
    if not NS: return r(True, thieu=['không có ngân sách chữ mỗi khung'], val='—')
    W = []   # khung mốc đinh = quãng năm dừng ∪ quãng thẻ giao nó (cards); không có số thẻ → quãng năm dừng ± 0,5 s (phóng/thu bộ đếm)
    for a, b in moc:
        if 'cards' in NS[0]:
            c = [bool(z.get('cards')) for z in NS]; lo, hi = a, b
            while lo - 1 >= 0 and c[lo - 1] and c[lo]: lo -= 1
            while hi + 1 < len(c) and c[hi + 1] and c[hi]: hi += 1
            W.append((lo, hi))
        else: W.append((a - round(0.5 * fps), b + round(0.5 * fps)))
    inpin = lambda f: any(a <= f <= b for a, b in W)
    nor = [z['pct'] for i, z in enumerate(NS) if not inpin(z.get('f', i))]; pin = [z['pct'] for i, z in enumerate(NS) if inpin(z.get('f', i))]
    o15 = [z.get('f', i) for i, z in enumerate(NS) if not inpin(z.get('f', i)) and z['pct'] > 15.0]; o25 = [z.get('f', i) for i, z in enumerate(NS) if inpin(z.get('f', i)) and z['pct'] > 25.0]
    if o15: loi.append(f'(a) {len(o15)} khung thường > 15 % (đầu: {o15[:3]}, max {max(nor):.1f} %)')
    if o25: loi.append(f'(a) {len(o25)} khung mốc đinh > 25 %')
    ce = [z.get('f', i) for i, z in enumerate(NS) if (z.get('center_unanchored_pct') or 0) > 0]
    if ce: loi.append(f'(b) {len(ce)} khung có chữ không neo ở vùng giữa (đầu: {ce[:3]})')
    sat = [f'(a) khung thường cao nhất {max(nor):.1f} % (trần 15 %)'] if nor and max(nor) >= 14.25 else []
    n_sat = sum(14.25 <= x <= 15.75 for x in nor)
    if 'cards' in NS[0]:
        c = [z.get('cards') or 0 for z in NS]
        if max(c) > 1: loi.append(f'(c) có khung {max(c)} thẻ cùng lúc')
        i = 0
        while i < len(c):
            if c[i]:
                j = i
                while j + 1 < len(c) and c[j + 1]: j += 1
                d = (j - i + 1) / fps
                if not 3.0 - 1e-6 <= d <= 5.0 + 1e-6: loi.append(f'(c) thẻ khung {i}–{j} dài {d:.2f} s ngoài 3–5 s')
                i = j + 1
            else: i += 1
    else: th.append('(c) ngân sách chữ không có số thẻ mỗi khung')
    if TX:
        cards = [t for its in TX.values() for t in its if t.get('role') == 'card']
        long_ = [t['s'] for t in cards if len(str(t['s']).split()) > 10]
        if long_: loi.append(f'(c) tiêu đề thẻ > 10 từ: {long_[0][:60]!r}')
        per = max((sum(1 for t in its if t.get('role') in ('year', 'index')) for its in TX.values()), default=0)
        if per > 2: loi.append(f'(d) {per} lớp thường trực cùng khung > 2')
        ket = B.get('ket') or [T - 6.0, T]
        bad = sorted({f for f, its in TX.items() for t in its if t.get('role') == 'method' and not (f / fps <= 6.0 or ket[0] <= f / fps <= ket[1])})
        if bad: loi.append(f'(e) dòng phương pháp ngoài 6 s đầu + màn kết ở khung {bad[:4]}')
        small = [(f, t['s'][:30], t['px1080']) for f, its in TX.items() for t in its if t.get('px1080') is not None and t['px1080'] < 38]
        lowc = [(f, t['s'][:30], t['ratio']) for f, its in TX.items() for t in its if t.get('ratio') is not None and t['ratio'] < 4.5]
        if small: loi.append(f'(f) chữ < 38 px@1080: {small[:2]}')
        if lowc: loi.append(f'(f) tương phản < 4,5:1: {lowc[:2]}')
        mr = min((t['ratio'] for its in TX.values() for t in its if t.get('ratio') is not None), default=None)
        mp = min((t['px1080'] for its in TX.values() for t in its if t.get('px1080') is not None), default=None)
        if mp is not None and mp <= 38 * 1.05: sat.append(f'(f) chữ nhỏ nhất {mp} px (ngưỡng 38 px)')
    else:
        th.append('(c) tiêu đề, (d), (e), (f): không có log chữ'); mr = mp = None
    if B.get('tuong_phan_min') is not None and mr is None: mr = B['tuong_phan_min']
    return r(True, loi, th, sat_nguong=sat, val=f"khung thường max {max(nor):.1f} % (trung vị {statistics.median(nor):.1f} %; {n_sat} khung trong ±5 % của 15 %)"
             + (f" · mốc đinh max {max(pin):.1f} %" if pin else '') + f" · vùng giữa không neo {len(ce)} khung" + (f" · chữ min {mp} px, tương phản min {mr}" if mp else ''))


def tlq6(B):
    N = B.get('nam_toa')
    if not N: return r(True, thieu=['không có bảng năm toà nhà theo lớp (nam_toa)'], val='—')
    loi, th, v = [], [], []; moc = {int(k): s for k, s in (N.get('moc') or {}).items()}; gia = set(N.get('gia') or GIA); now = int(N.get('nam_hien_tai', 2026))
    for y, s in moc.items():
        if not str(s or '').strip(): loi.append(f'mốc {y}: không có nguồn')
    for ten, L in (N.get('lop') or {}).items():
        H = {int(k): int(c) for k, c in (L.get('nam') or {}).items() if int(c) > 0}
        if L.get('loai') == 'so_dang_ky':
            bad = {y: c for y, c in H.items() if y in gia or y > now or y <= 0}
            if bad: loi.append(f'{ten}: {sum(bad.values())} toà mang năm giả/không hợp lệ vẫn mọc {dict(sorted(bad.items())[:4])}')
            if not H: th.append(f'{ten}: không có phân bố năm (chỉ có tổng)')
        elif L.get('loai') == 'tang_chuan':
            bad = sorted(y for y in H if y not in moc)
            if bad: loi.append(f'{ten}: đổi trạng thái ở năm không phải mốc có nguồn {bad[:6]}')
        else: th.append(f'{ten}: loại lớp không rõ')
        v.append(f"{ten} ({L.get('loai')}): {sum(H.values())} toà, năm {sorted(H)[:6]}{'…' if len(H) > 6 else ''}")
    return r(True, loi, th, val='; '.join(v))


# ---------------------------------------------------------------- 1.12.1 (chủ dự án duyệt 16–17/10: HH3, MM1, MM2, JJ1/KK1)
XAP_XI = re.compile(r'≈\s*=\s*interpolated between counts', re.I)
NAM_S_THAP, NAM_S_CAO, AGL_THAP = 10.0, 20.0, 150.0   # MM2: năm/s pha bay thấp (AGL ≤ 150 m) / pha crane, reveal
CONTENT_THAP = 30.0                                    # MM1: content_pct trung vị pha bay thấp của cú liên hoàn
LH_MAX, VERTIGO_MAX, ORBIT_S, W_MAX = 2, 1, (4.0, 6.0), 90.0   # JJ1/KK1 tiết chế máy


def q35_tl(B, fps):
    """Q35(c) trên bộ timelapse (HH3): bộ đếm liên tục (role index) hiện số có dấu "≈" mà khung không có chữ ESTIMATE → chỉ ĐẠT khi dòng phương
    pháp (role method) chứa "≈ = interpolated between counts" hiện trong 6 s đầu phim. Chữ "≈" ở vai khác (tag, thẻ…) vẫn cần ESTIMATE."""
    TX = _text(B.get('log_chu'))
    if not TX: return r(True, thieu=['không có log chữ'], val='—')
    est = sorted(f for f, its in TX.items() if any('≈' in str(t.get('s', '')) and t.get('role') != 'method' for t in its)
                 and not any('ESTIMATE' in str(t.get('s', '')).upper() for t in its))
    if not est: return r(True, val='không có số "≈" thiếu ESTIMATE')
    dong = sorted(f for f, its in TX.items() if f / fps <= 6.0 + 1e-9 for t in its if t.get('role') == 'method' and XAP_XI.search(str(t.get('s', ''))))
    khac = sorted({(f, t['role']) for f in est for t in TX[f] if '≈' in str(t.get('s', '')) and t.get('role') not in ('index', 'method')})
    loi = []
    if khac: loi.append(f'(c) chữ "≈" ở vai không phải bộ đếm liên tục (index) mà không có ESTIMATE: khung/vai {khac[:3]}')
    if not dong: loi.append(f'(c) {len(est)} khung bộ đếm "≈" không có ESTIMATE (đầu: {est[:3]}) và không có dòng phương pháp '
                            f'"≈ = interpolated between counts" trong 6 s đầu')
    return r(True, loi, val=f'{len(est)} khung bộ đếm "≈" (khung {est[0]}–{est[-1]})' + (f' · dòng phương pháp "≈ = interpolated…" khung {dong[0]} ({dong[0] / fps:.2f} s)' if dong else ' · KHÔNG có dòng phương pháp "≈ = …" trong 6 s đầu'))


def _vdir(fr):
    v = [fr['look'][i] - fr['pos'][i] for i in range(3)]; n = math.hypot(*v) or 1.0; return [x / n for x in v]


def _cuts(F, CP):
    """khung bắt đầu cú mới sau cắt (`cuts` của campath, giây hoặc khung; hoặc bước máy > max(50 m, 6× trung vị))"""
    c = set()
    for x in (CP.get('cuts') if isinstance(CP, dict) else None) or []:
        c.add(round(x * FPS) if isinstance(x, float) else int(x))
    st = [math.dist(F[i]['pos'], F[i - 1]['pos']) for i in range(1, len(F))]; med = statistics.median(st) if st else 0
    c |= {i for i in range(1, len(F)) if st[i - 1] > max(50.0, 6 * med)}
    return c


NAM_CUA = 0.5   # MM2: năm/s đo trên cửa sổ trượt 0,5 s (12 khung) — năm trong campath làm tròn 0,01 → sai số bước 1 khung tới ±0,24 năm/s


def tlq7(B, F, fps, base):
    """MM2 năm/s theo pha (Chặn): năm/s = |năm(i+n) − năm(i)| / (n/fps), n = 0,5 s, do K TÍNH từ campath (không dùng yr_s tự khai), cửa sổ không
    qua cắt. Cửa sổ có khung AGL ≤ 150 m (pha bay thấp — mọi pha, kể cả ngoài cú) → ≤ 10 năm/s; cửa sổ còn lại có khung pha crane/reveal → ≤ 20 năm/s."""
    ag, ag_src = agl_cua(B, F, base, {}, B.get('mat_bang', 'xz'))
    if 'phase' not in F[0] or ag_src.startswith('độ cao tuyệt đối'):
        return r(True, thieu=['campath không có pha (grammarLog phase) hoặc không có AGL theo địa hình (agl / dia_hinh) — không phân được pha bay thấp'], val='—')
    n = max(1, round(NAM_CUA * fps)); cut = sorted(_cuts(F, B.get('_cp'))); A = [ag(fr) for fr in F]
    loi, sat, run, mx = [], [], [], dict(thap=(0, None), cao=(0, None))
    for i in range(len(F) - n):
        if any(i < c <= i + n for c in cut): continue
        y = abs(F[i + n]['year'] - F[i]['year']) * fps / n; ph = {F[j].get('phase') for j in range(i, i + n + 1)}
        lim, k = (NAM_S_THAP, 'thap') if min(A[i:i + n + 1]) <= AGL_THAP else ((NAM_S_CAO, 'cao') if ph & {'crane', 'reveal'} else (None, None))
        if lim is None: continue
        if y > mx[k][0]: mx[k] = (y, i)
        if y > lim + 1e-6: run.append((i, k, y, ph, min(A[i:i + n + 1]), max(A[i:i + n + 1])))
    gr = []
    for x in run:   # gom các cửa sổ vượt liền nhau
        if gr and x[0] == gr[-1][-1][0] + 1 and x[1] == gr[-1][-1][1]: gr[-1].append(x)
        else: gr.append([x])
    for g in gr:
        k = g[0][1]; lim = NAM_S_THAP if k == 'thap' else NAM_S_CAO; f0, f1 = g[0][0], g[-1][0] + n
        loi.append(f"khung {f0}–{f1} ({f0 / fps:.2f}–{(f1 + 1) / fps:.2f} s, năm {F[f0]['year']:.0f}–{F[f1]['year']:.0f}, pha {sorted(set().union(*[x[3] for x in g]), key=str)}, "
                   + (f"AGL {min(x[4] for x in g):.0f}–{max(x[5] for x in g):.0f} m, có khung ≤ {AGL_THAP:.0f} m" if k == 'thap' else 'crane/reveal')
                   + f"): năm/s tới {max(x[2] for x in g):.2f} > {lim:.0f}")
    for k, lim in (('thap', NAM_S_THAP), ('cao', NAM_S_CAO)):
        if mx[k][1] is not None and abs(mx[k][0] - lim) <= 0.05 * lim: sat.append(f"năm/s max pha {'bay thấp' if k == 'thap' else 'crane/reveal'} {mx[k][0]:.2f} (trần {lim:.0f}, cửa sổ từ khung {mx[k][1]})")
    return r(True, loi, sat_nguong=sat, val=f"năm/s max (cửa sổ {NAM_CUA} s): bay thấp (AGL ≤ {AGL_THAP:.0f} m) {mx['thap'][0]:.2f} (từ khung {mx['thap'][1]}) · crane/reveal "
             f"{mx['cao'][0]:.2f} (từ khung {mx['cao'][1]}) · {ag_src}")


def _cu(F, preset):
    """các cú (khung đầu, khung cuối) có preset = preset liền nhau"""
    out, i = [], 0
    while i < len(F):
        if F[i].get('preset') == preset:
            j = i
            while j + 1 < len(F) and F[j + 1].get('preset') == preset: j += 1
            out.append((i, j)); i = j + 1
        else: i += 1
    return out


def tlq8(B, F, fps, base, moc=()):
    """MM1 (Cảnh báo): trong pha bay thấp của cú liên hoàn (khung preset lien-hoan có AGL ≤ 150 m), content_pct (mặt nạ nội dung hình học
    MỌI khung, `mat_na`) trung vị ≥ 30 %. Báo kèm các quãng liên tục < 30 % (mốc đinh không miễn: chỉ số là trung vị cả pha)."""
    if not B.get('mat_na'): return r(True, thieu=['không có mặt nạ nội dung mỗi khung (mat_na)'], val='—')
    M = {int(x['f']): x for x in _ld(B['_base'], B['mat_na'])}; ag, ag_src = agl_cua(B, F, base, {}, B.get('mat_bang', 'xz'))
    if ag_src.startswith('độ cao tuyệt đối'): return r(True, thieu=['không có AGL theo địa hình'], val='—')
    loi, th, v, sat = [], [], [], []
    CU = _cu(F, 'lien-hoan')
    if not CU: return r(True, val='không có cú liên hoàn')
    for a, b in CU:
        L = [f for f in range(a, b + 1) if ag(F[f]) <= AGL_THAP]
        if not L: v.append(f'cú {a}–{b}: không có khung bay thấp'); continue
        miss = [f for f in L if f not in M]
        if miss: th.append(f'cú {a}–{b}: mặt nạ thiếu {len(miss)}/{len(L)} khung bay thấp'); continue
        md = statistics.median(M[f]['content_pct'] for f in L)
        q, i = [], 0
        while i < len(L):
            if M[L[i]]['content_pct'] < CONTENT_THAP:
                j = i
                while j + 1 < len(L) and L[j + 1] == L[j] + 1 and M[L[j + 1]]['content_pct'] < CONTENT_THAP: j += 1
                if (j - i + 1) / fps >= 0.5: q.append((L[i], L[j]))
                i = j + 1
            else: i += 1
        qs = ', '.join(f"khung {x}–{y} ({x / fps:.1f}–{(y + 1) / fps:.1f} s, năm {F[x]['year']:.0f}–{F[y]['year']:.0f}, min {min(M[f]['content_pct'] for f in range(x, y + 1))} %)" for x, y in q)
        if md < CONTENT_THAP: loi.append(f'cú liên hoàn {a}–{b}: pha bay thấp {len(L) / fps:.2f} s, content_pct trung vị {md:.1f} % < {CONTENT_THAP:.0f} % — quãng < 30 %: {qs}')
        if abs(md - CONTENT_THAP) <= 0.05 * CONTENT_THAP: sat.append(f'cú {a}–{b}: content_pct trung vị bay thấp {md:.1f} % (ngưỡng 30 %)')
        v.append(f'cú {a}–{b}: bay thấp {len(L)} khung ({len(L) / fps:.2f} s), content trung vị {md:.1f} %' + (f'; quãng < 30 %: {qs}' if q and md >= CONTENT_THAP else ''))
    return r(True, loi, th, sat_nguong=sat, val='; '.join(v))


def tlq9(BS):
    """JJ1/KK1 tiết chế máy trên MỘT TẬP (danh sách bộ timelapse của tập): (a) ≤ 2 cú liên hoàn, (b) ≤ 1 vertigo — Cảnh báo; (c) mỗi cú liên hoàn
    khai `vai` ∈ {co-che, buoc-ngoat, he-qua} ở MỌI khung (mọi pha); (d) orbit (khung pha orbit/pin đầu → cuối trong cú) 4–6 s — Cảnh báo;
    (e) tốc độ góc hướng nhìn ≤ 90 °/s mọi bước khung (K tính từ pos/look, không qua cắt) — Chặn."""
    VAI = {'co-che', 'buoc-ngoat', 'he-qua'}; M = {k: [] for k in 'abcde'}; v, sat, nlh, nvt, wmax = [], [], 0, 0, (0.0, None)
    for name, B, F, fps in BS:
        lh, vt = _cu(F, 'lien-hoan'), _cu(F, 'vertigo'); nlh += len(lh); nvt += len(vt)
        for a, b in lh:
            bad = sorted({F[f].get('phase') for f in range(a, b + 1) if F[f].get('vai') not in VAI}, key=str)
            if bad: M['c'].append(f'{name} cú liên hoàn khung {a}–{b}: pha {bad} không khai vai hợp lệ')
            ob = [f for f in range(a, b + 1) if F[f].get('phase') in ('orbit', 'pin')]
            if not ob: M['d'].append(f'{name} cú liên hoàn {a}–{b}: không có pha orbit')
            else:
                d = (ob[-1] - ob[0] + 1) / fps
                if not ORBIT_S[0] - 1e-6 <= d <= ORBIT_S[1] + 1e-6: M['d'].append(f'{name} cú liên hoàn {a}–{b}: orbit {d:.2f} s ngoài 4–6 s')
                v.append(f'{name} liên hoàn {a}–{b}: orbit {d:.2f} s')
        cut = _cuts(F, B.get('_cp')); run = []
        for i in range(1, len(F)):
            if i in cut: continue
            a, c = _vdir(F[i - 1]), _vdir(F[i]); w = math.degrees(math.acos(max(-1.0, min(1.0, sum(x * y for x, y in zip(a, c)))))) * fps
            if w > wmax[0]: wmax = (w, f'{name} khung {i}')
            if w > W_MAX: run.append((i, w))
        if run: M['e'].append(f'{name}: {len(run)} bước khung > {W_MAX:.0f} °/s (đầu: khung {run[0][0]}, max {max(w for _, w in run):.1f} °/s)')
    if nlh > LH_MAX: M['a'].append(f'{nlh} cú liên hoàn trong tập > {LH_MAX}')
    if nvt > VERTIGO_MAX: M['b'].append(f'{nvt} vertigo trong tập > {VERTIGO_MAX}')
    if wmax[1] and wmax[0] >= 0.95 * W_MAX: sat.append(f'tốc độ góc max {wmax[0]:.1f} °/s (trần 90, {wmax[1]})')
    loi = [f'({k}) {x}' for k in 'abcde' for x in M[k]]
    canh, chan = [x for x in loi if not x.startswith('(e)')], [x for x in loi if x.startswith('(e)')]
    return dict(ok=not loi, ket_qua=None, loi=loi, thieu=[], muc=M, sat_nguong=sat, canh_bao=canh, chan=chan,
                val=f"{nlh} cú liên hoàn · {nvt} vertigo · tốc độ góc max {wmax[0]:.1f} °/s ({wmax[1]})" + (' · ' + '; '.join(v) if v else ''))


def check(B, base='.'):
    fps = B.get('fps', FPS); CP = _ld(base, B['campath']); F = _frames(CP); T = len(F) / fps
    B['_base'] = base; B['_shots'] = CP.get('shots') if isinstance(CP, dict) else None
    for k in ('ngan_sach', 'log_chu'): B[k] = _frames(_ld(base, B.get(k))) if B.get(k) else None
    B['_cp'] = CP if isinstance(CP, dict) else None
    q1 = tlq1(B, F, fps, T)
    return {'TL-Q1': q1, 'TL-Q2': tlq2(B, F, fps, base), 'TL-Q3': tlq3(B, F, fps), 'TL-Q4': tlq4(B, F, fps, base), 'TL-Q5': tlq5(B, F, fps, T, q1['moc']), 'TL-Q6': tlq6(B),
            'Q35-TL': q35_tl(B, fps), 'TL-Q7': tlq7(B, F, fps, base), 'TL-Q8': tlq8(B, F, fps, base, q1['moc']), 'TL-Q9': tlq9([(B.get('ten') or 'bộ', B, F, fps)])}


def main():
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    B = json.load(open(a[0])); R = check(B, os.path.dirname(os.path.abspath(a[0])))
    for k, x in R.items():
        print(f"{k}: {x.get('ket_qua') or ('ĐẠT' if x['ok'] else 'TRƯỢT')} — {x['val']}"); [print('   ', y) for y in x['loi'] + x['thieu']]
    if '--json' in a: json.dump(R, open(a[a.index('--json') + 1], 'w'), ensure_ascii=False, indent=1, default=str)


if __name__ == '__main__':
    main()
