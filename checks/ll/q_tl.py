#!/opt/cine/bin/python
"""TL-Q1…TL-Q6 dạng tập timelapse thành phố — luật khoá bản 1.12.0 (phiên K, 16/10/2026; chủ dự án duyệt luật 16/10). Mặc định CHỈ BÁO.
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
Mục nào thiếu đầu vào → THIẾU (không ĐẠT), ghi rõ trong `thieu`.

TL-Q1 mốc đinh: mốc = quãng năm KHÔNG ĐỔI ≥ 1,0 s (bỏ quãng chạm khung đầu/cuối phim). (a) mỗi mốc 1,5–2,0 s; (b) cỡ chữ năm trong mốc
       / trung vị ngoài mốc ≥ 1,4×; (c) sáng TB trong mặt nạ công trình / phần còn lại ≥ 1,5; (d) có thẻ (cards > 0) giao mốc, liền ≥ 3 s,
       dòng nguồn (role src) không rỗng ≥ 38 px; (e) số mốc ≥ ⌈thời lượng / 180 s⌉.
TL-Q2 bay dọc phố/sông: ≥ 3 s liên tục máy cách tuyến (mặt bằng) ≤ 15 m và cao ≤ 120 m; tuyến có nguồn; cuối quãng, đích lệch trục nhìn ≤ 10°.
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
    ns = B.get('nhan_sang')
    if ns is None: th.append('(c) không có số đo sáng trong mặt nạ công trình (cần mặt nạ hero theo khung)')
    else:
        for x in ns:
            if x['ti_le'] < 1.5: M['c'].append(f"(c) {x['t']}: sáng trong/ngoài công trình {x['ti_le']:.2f} < 1,5")
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
    return r(True, loi, th, val=f"{len(P)} mốc: " + ', '.join(f"{F[a]['year']:.0f} {(b - a + 1) / fps:.2f} s (khung {a}–{b})" for a, b in P), muc=M, moc=P)


def _plan(p, mb): return (p[0], -p[2]) if mb == 'x-z' else (p[0], p[2])


def _dseg(px, py, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]; u = max(0.0, min(1.0, ((px - a[0]) * dx + (py - a[1]) * dy) / ((dx * dx + dy * dy) or 1)))
    return math.hypot(px - a[0] - u * dx, py - a[1] - u * dy)


def _offaxis(fr, tgt):
    v = [fr['look'][i] - fr['pos'][i] for i in range(3)]; w = [tgt[i] - fr['pos'][i] for i in range(3)]
    c = sum(a * b for a, b in zip(v, w)) / (math.hypot(*v) * math.hypot(*w) or 1); return math.degrees(math.acos(max(-1, min(1, c))))


def tlq2(B, F, fps):
    TU = B.get('tuyen')
    if not TU: return r(True, thieu=['không khai tuyến bay (tuyen)'], val='—')
    loi, th, out = [], [], []; mb = B.get('mat_bang', 'xz')
    for k, x in enumerate(TU):
        f0, f1 = round(x['t'][0] * fps), min(len(F) - 1, round(x['t'][1] * fps)); W = F[f0:f1 + 1]
        if x.get('pts'):
            d = [min(_dseg(*_plan(fr['pos'], mb), x['pts'][i], x['pts'][i + 1]) for i in range(len(x['pts']) - 1)) for fr in W]; cach = 'K tính từ hình học tuyến'
        elif x.get('dung_dev_m'):
            d = [fr.get('dev_m', math.inf) for fr in W]; cach = 'dev_m của campath (bộ dựng tính; tuyến không có trong repo)'
        else: th.append(f'tuyến {k}: không có hình học tuyến (pts) hay dev_m'); continue
        best, cur, bi = (0, None), 0, None
        for i, (fr, di) in enumerate(zip(W, d)):
            if di <= 15.0 and fr['pos'][1] <= 120.0:
                cur += 1; bi = i if cur == 1 else bi
                if cur > best[0]: best = (cur, (bi, i))
            else: cur = 0
        n_on = sum(di <= 15.0 for di in d); alt = [fr['pos'][1] for fr, di in zip(W, d) if di <= 15.0]
        s = best[0] / fps
        if s < 3.0:
            why = f'chỉ {s:.2f} s liên tục ≤ 15 m và ≤ 120 m' + (f' (≤ 15 m: {n_on / fps:.2f} s, nhưng cao {min(alt):.0f}–{max(alt):.0f} m)' if alt and max(alt) > 120 else '')
            loi.append(f'tuyến {k} {x["t"]}: {why}')
        if not str(x.get('nguon') or '').strip(): loi.append(f'tuyến {k}: không ghi nguồn hình học')
        oa = None
        if x.get('dich'):
            oa = _offaxis(W[best[1][1]] if best[1] else W[-1], x['dich'])
            if oa > 10.0: loi.append(f'tuyến {k}: cuối quãng đích lệch trục nhìn {oa:.1f}° > 10°')
        elif not x.get('dich'): th.append(f'tuyến {k}: không khai đích (dich)')
        ins = [di for di in d if di <= 15.0]
        out.append(dict(t=x['t'], lien_tuc_s=round(s, 2), cach=cach, lech_tb=round(statistics.mean(ins), 2) if ins else None, lech_max=round(max(ins), 2) if ins else None,
                        cao=[round(min(alt), 1), round(max(alt), 1)] if alt else None, lech_truc=None if oa is None else round(oa, 1)))
    return r(True, loi, th, val='; '.join(f"{o['t']}: {o['lien_tuc_s']} s ≤ 15 m/≤ 120 m, lệch TB {o['lech_tb']} m, max {o['lech_max']} m, cao {o['cao']}, đích {o['lech_truc']}° ({o['cach']})" for o in out), tuyen=out)


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


def check(B, base='.'):
    fps = B.get('fps', FPS); F = _frames(_ld(base, B['campath'])); T = len(F) / fps
    for k in ('ngan_sach', 'log_chu'): B[k] = _frames(_ld(base, B.get(k))) if B.get(k) else None
    q1 = tlq1(B, F, fps, T)
    return {'TL-Q1': q1, 'TL-Q2': tlq2(B, F, fps), 'TL-Q3': tlq3(B, F, fps), 'TL-Q4': tlq4(B, F, fps, base), 'TL-Q5': tlq5(B, F, fps, T, q1['moc']), 'TL-Q6': tlq6(B)}


def main():
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    B = json.load(open(a[0])); R = check(B, os.path.dirname(os.path.abspath(a[0])))
    for k, x in R.items():
        print(f"{k}: {x.get('ket_qua') or ('ĐẠT' if x['ok'] else 'TRƯỢT')} — {x['val']}"); [print('   ', y) for y in x['loi'] + x['thieu']]
    if '--json' in a: json.dump(R, open(a[a.index('--json') + 1], 'w'), ensure_ascii=False, indent=1, default=str)


if __name__ == '__main__':
    main()
