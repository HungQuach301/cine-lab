#!/opt/cine/bin/python
"""Q37 nhịp thị giác kênh 2 — luật khoá bản 1.11.0 (phiên K, 15/10/2026). Căn cứ: Kinh thánh kênh 2 §4 (chủ dự án 14/10/2026 18:08):
"trung bình ≤ 3,5 s có một biến cố hình mới …; không giữ khung tĩnh > 6 s". Áp kênh 2 từ K2 tập 3. Thay Q14–Q18 (luật nhịp LL) cho kênh 2.

Nguồn số: cùng định nghĩa với thước của xưởng `scripts/k2/rhythm.py` (bản T2 G1b, origin/k2c-t2 @8ec1063: mốc opt quy theo frame0/speed,
hl/arcs/cols.grow/p.title). K giữ BẢN SAO ĐỘC LẬP dưới đây (đổi thước của xưởng không đổi nghĩa luật); selftest đối chiếu số của bản sao
với số rhythm.py đã ghi trong repo (cuộn K2V4 `rhythm-v4.json`) — phải trùng từng số. KHÁC rhythm.py @T2 ở một chỗ (sửa lỗi, có bằng chứng):
khung bắt đầu của cảnh dùng lại đọc `p.frame0`, KHÔNG có thì `p.off` — scripts/ll/ll.py load() đổi tên frame0 → off, nên trên đặc tả đã giải
(est.py T2) rhythm.py @T2 coi mọi cảnh dùng lại bắt đầu ở khung 0 (đo 15/10 trên T2: 4 biến cố khai lệch mốc thật).

  q_nhip.py <spec.yaml>                              đặc tả có segments[].dur và beats (định dạng rhythm.py: cuộn mẫu, tờ khung)
  q_nhip.py <episode.yaml> --tl <timeline.json>      tập: thời lượng + mốc lớp 2D/cảnh lấy từ timeline (đã quy giây), beats từ đặc tả
            [--mp4 <master.mp4>] [--bo-tl bo-tl.json …] [--json ra.json]     (--bo-tl: 1.15 biến cố cảnh tl; dùng được cả ở chế độ đặc tả)

Biến cố khai ở đặc tả: segments[].beats: [{t (giây trong đoạn, SỐ), k: cut|cam|region|route|ring|sticker|number|label|text|palette|score, s}].
TRƯỢT khi:
  (a) một biến cố khai không khớp mốc thật nào của đặc tả (±0,3 s); đoạn thiếu biến cố `cut` ở 0; đoạn không khai beats
  (b) khoảng biến cố trung bình (thời lượng / số biến cố sau khi gộp biến cố cách nhau < 0,25 s) > 3,5 s
  (c) khoảng dài nhất giữa hai biến cố (kể cả tới cuối phim) > 6 s
  (d) có master: khung tĩnh — chuỗi khung liền có sai khác trung bình < 0,6/255 (xám 160×90) dài nhất > 6 s
      1.13 (khiếu nại T2 G2 §14.5, đo trên điểm ảnh trong checks — không dựa scripts/k2/rhythm.py): KHUNG TĨNH = quãng mà MỌI khung khác
      KHUNG ĐẦU QUÃNG < STATIC_ANCHOR/255 (xám 160×90, mốc neo mỗi 0,5 s): ảnh không đổi rõ so với lúc bắt đầu. Ngưỡng 2,0 ≈ dịch 0,3 % bề
      ngang hay zoom 0,6 % trên khung T2 (trung vị; nền nhiễu mã hoá 0,25–0,3). Thước cũ (từng khung liền < 0,6) coi máy trôi chậm là tĩnh:
      T2 L5 r02_subsidy 3:01–3:12 "tĩnh 11,79 s" nhưng khung cuối khác khung đầu 10,6/255 (máy lùi 62 → 70 km). Mọi quãng > 6 s đều liệt kê
      (trước chỉ báo quãng dài nhất nên che quãng sau); quãng "trôi chậm" (thước cũ > 6 s, không tĩnh) báo kèm, không tính lỗi.
Không khai beats (tập cũ): báo thêm số đo "mốc đặc tả" (mọi mốc thật, cận trên số biến cố) để tham khảo — không thay được beats.
Trong ±5 % quanh 3,5 s và 6 s: nêu tên.
1.15 (I8, chủ dự án duyệt 18/10; V5B2B §10.5): BIẾN CỐ CẢNH TL — với mỗi bộ timelapse (k2check --bo-tl), biến cố thị giác bên trong cảnh tl được
      ĐO (không khai) và cộng vào (b), (c):
      · đổi pha máy sang một pha thuộc PHASE_EV (ramp, orbit, pin, crane, reveal): `campath.shots[].phases` [{k|kind|phase, t: [a, b] giây cảnh
        | f: [a, b] khung cảnh}] nếu có, không thì chuyển pha giữa hai khung liền của `campath.frames[].phase` (cùng `canh`);
      · đồng hồ dừng: nhãn đồng hồ không đổi ≥ CLOCK_MIN_S (1,0 s) VÀ ≥ CLOCK_K (2) × trung vị độ dài các quãng nhãn của cảnh đó (đồng hồ chạy
        1 phút/s không bị tính là dừng). Nguồn nhãn: `campath.frames[].clock` → `frames_meta` (bo-tl: {canh: meta.json của hero.js}, khoá
        frames_meta[f].clock) → log chữ của bộ (role clock, mẫu thưa; độ dài quãng tính theo bước mẫu). Biến cố = khung đầu quãng dừng.
      Ánh xạ khung cảnh → giây phim qua shot đặc tả/timeline có `p.hero` (hoặc `p.dir` = heroes[k].dir) = `canh`: t = đầu shot +
      (f_cảnh − frame0) / (24 · speed), chỉ trong khung shot. Campath không có `canh` → không ánh xạ (không thêm biến cố). Biến cố đo không qua (a).
"""
import json, os, subprocess, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from checks.ll import base  # noqa: E402

TOL, MERGE, MEAN_MAX, GAP_MAX, STATIC_MAX, STATIC_DIFF = 0.3, 0.25, 3.5, 6.0, 6.0, 0.6
STATIC_ANCHOR, ANCHOR_STEP = 2.0, 12   # 1.13: khung tĩnh theo khung neo (mỗi 12 khung = 0,5 s)
PHASE_EV, CLOCK_MIN_S, CLOCK_K = ('ramp', 'orbit', 'pin', 'crane', 'reveal'), 1.0, 2.0   # 1.15 (I8): biến cố cảnh tl


def num(v): return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def lst(v):
    """danh sách mốc; khoá trùng tên mà khác kiểu (vd opt.hl là số ở cảnh T1) → không có mốc (rhythm.py @T2 lỗi kiểu ở đây)"""
    return [x for x in v if isinstance(x, dict)] if isinstance(v, list) else []


def spec_times(heroes, shots, dur):
    """mọi mốc (giây trong đoạn) mà đặc tả làm xuất hiện/đổi cái gì đó. shots: [{at, p}] (at = đầu shot trong đoạn)."""
    T = {0.0}
    for j, sh in enumerate(shots):
        off = num(sh.get('at', 0)) or 0.0; T.add(off); p = sh.get('p') or {}; h = heroes.get(p.get('hero')) or {}; o = h.get('opt') or {}
        end = num(shots[j + 1].get('at')) if j + 1 < len(shots) else num(dur)
        f0 = (num(p.get('frame0', p.get('off', 0))) or 0.0) / 24; sp = num(p.get('speed', 1)) or 1.0

        def add(v, base_=off, f0=f0, sp=sp, end=end):   # mốc opt là giờ CẢNH → giờ đoạn = at + (τ − frame0/24)/speed, chỉ trong khung shot
            if num(v) is None or v < f0: return
            t = base_ + (v - f0) / sp
            if end is None or t < end: T.add(t)
        first = lambda x: x[0] if isinstance(x, list) and x else x
        for k in ('sepia', 'natural'):
            if isinstance(o.get(k), list): add(first(o[k]))
        for r in lst(o.get('regions')): add(first(r.get('at')))
        for r in lst(o.get('routes')): add(first(r.get('draw')))
        for r in lst(o.get('rings')): add(r.get('t'))
        for c in lst(o.get('cols')): add(first(c.get('t') or [None]))
        for c in lst(o.get('cam')): add(c.get('t'))
        for w in lst(o.get('walkers')): add(first(w.get('t') or [None]))
        for q in lst(o.get('props')): add(q.get('t'))
        if isinstance(o.get('close'), dict): add(first(o['close'].get('at') or [None]))
        for x in lst(o.get('hl')):
            if isinstance(x, dict): add(first(x.get('at')))
        for x in lst(o.get('arcs')): add(first(x.get('draw')))
        for x in lst(o.get('cols')):
            if isinstance(x.get('grow'), list): add(x['grow'][0])

        def add2(v):   # mốc lớp 2D (p.*) là giây TRONG ĐOẠN
            if num(v) is not None and v >= 0: T.add(v)
        for k in ('places', 'tags', 'stickers', 'labels'):
            for x in p.get(k, []) or []:
                if isinstance(x, dict): add2(x.get('at'))
        for c in p.get('cap', []) or []:
            if isinstance(c, dict): add2(c.get('at'))
        for k in ('year', 'title'):
            if isinstance(p.get(k), dict): add2(p[k].get('at'))
        sd = p.get('side') or {}
        add2(sd.get('at'))
        for l in sd.get('lines', []) or []: add2(l.get('at'))
        sc = p.get('score') or {}
        for part in ('corner', 'board'):
            if sc.get(part): add2(sc[part].get('at'))
        for r in (sc.get('board') or {}).get('rows', []) or []: add2(r.get('at'))
        for sd2 in (sc.get('corner') or {}).get('sides', []) or []:
            if isinstance(sd2.get('n'), list):
                for e in sd2['n']: add2(e.get('t'))
    return sorted(T)


def view(E, TL=None):
    """→ [(id, dur, heroes, shots[{at,p}], beats)] — spec mode hoặc episode+timeline"""
    if TL is None:
        HZ = E.get('heroes') or {}
        return [(s['id'], float(s['dur']), HZ, s.get('shots', []), s.get('beats')) for s in E['segments']]
    HZ = dict(E.get('heroes') or {}, **(TL.get('heroes') or {})); SP = {s['id']: s for s in E.get('segments') or []}
    return [(s['id'], float(s['t1'] - s['t0']), HZ, [dict(at=sh['t0'], p=sh.get('p') or {}) for sh in s['shots']], (SP.get(s['id']) or {}).get('beats'))
            for s in TL['segments']]


_G = {}


def gray160(mp4):
    import numpy as np
    k = (os.path.abspath(mp4), os.path.getmtime(mp4))
    if k in _G: return _G[k]
    _G.clear()
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-nostdin', '-i', mp4, '-map', '0:v:0', '-vf', 'scale=160:90,format=gray', '-f', 'rawvideo', '-'],
                         capture_output=True, check=True).stdout
    _G[k] = np.frombuffer(raw, np.uint8).reshape(-1, 90, 160).astype(np.float32); return _G[k]


def static_run(mp4, F=None):
    """thước cũ (1.11.0): chuỗi khung liền sai khác < STATIC_DIFF → (dài nhất s, từ s)"""
    import numpy as np
    F = gray160(mp4) if F is None else F; d = np.abs(np.diff(F, axis=0)).mean(axis=(1, 2))
    best = run = at = 0
    for i, v in enumerate(d):
        run = run + 1 if v < STATIC_DIFF else 0
        if run > best: best, at = run, i - run + 1
    return round(best / 24, 2), round(at / 24, 2)


def _runs_cu(F, lim):
    import numpy as np
    d = np.abs(np.diff(F, axis=0)).mean(axis=(1, 2)); R, run = [], 0
    for i, v in enumerate(list(d) + [99]):
        if v < STATIC_DIFF: run += 1
        else:
            if run / 24 > lim: R.append((round(run / 24, 2), round((i - run) / 24, 2)))
            run = 0
    return R


def static_anchor(F, th=STATIC_ANCHOR, step=ANCHOR_STEP, fps=24):
    """1.13: mốc neo a (mỗi `step` khung) → khung đầu tiên sau a có |F − F[a]| trung bình ≥ th; quãng tĩnh = [a, đó).
    → [(dài s, từ s)] mọi quãng tĩnh cực đại (không chồng), giảm dần theo độ dài"""
    import numpy as np
    n = len(F); best = []
    for a in range(0, max(n - 1, 0), step):
        e, CH = a + 1, 48
        while e < n:
            d = np.abs(F[e:e + CH] - F[a]).mean(axis=(1, 2)); k = np.nonzero(d >= th)[0]
            if len(k): e += int(k[0]); break
            e += CH
        e = min(e, n); best.append((e - a, a))
    best.sort(key=lambda z: -z[0]); out, used = [], []
    for L, a in best:
        if L < 2 or any(a < u1 and a + L > u0 for u0, u1 in used): continue
        used.append((a, a + L)); out.append((round(L / fps, 2), round(a / fps, 2)))
    return out


# ------------------------------------------------------------------ 1.15 (I8): biến cố cảnh tl
def _clock_runs(seq, step_f, fps=24):
    """seq: [(f, nhãn)] tăng dần theo f (một cảnh) → [(f đầu, f cuối, nhãn, dài s)] các quãng nhãn không đổi"""
    out, i = [], 0
    while i < len(seq):
        j = i
        while j + 1 < len(seq) and seq[j + 1][1] == seq[i][1] and seq[j + 1][0] - seq[j][0] <= 1.5 * step_f: j += 1
        out.append((seq[i][0], seq[j][0], seq[i][1], (seq[j][0] - seq[i][0] + step_f) / fps)); i = j + 1
    return out


def clock_stops(seq, step_f, fps=24):
    """quãng đồng hồ dừng của một cảnh: dài ≥ CLOCK_MIN_S và ≥ CLOCK_K × trung vị độ dài quãng nhãn → [(f đầu, f cuối, nhãn, dài s)]"""
    import statistics
    R = _clock_runs(seq, step_f, fps)
    if len(R) < 2: return []
    md = statistics.median(x[3] for x in R)
    return [x for x in R if x[3] >= CLOCK_MIN_S and x[3] >= CLOCK_K * md]


def _ld(base, p):
    if p is None or isinstance(p, (list, dict)): return p
    q = p if os.path.isabs(p) else os.path.join(base, p)
    if q.endswith('.gz'):
        import gzip; return json.load(gzip.open(q))
    return json.load(open(q))


def tl_su_kien(B, base, fps=24):
    """một bộ timelapse → {canh: [(f_cảnh, loại, mô tả)]} biến cố thị giác đo được trong cảnh tl (pha máy + đồng hồ dừng)"""
    CP = _ld(base, B.get('campath')); F = CP['frames'] if isinstance(CP, dict) and 'frames' in CP else (CP or [])
    SH = CP.get('shots') if isinstance(CP, dict) else None; ev = {}
    has_ph = [s for s in SH or [] if isinstance(s, dict) and isinstance(s.get('phases'), list) and s.get('canh')]
    for s in has_ph:
        for p in s['phases']:
            k = p.get('k') or p.get('kind') or p.get('phase')
            a = (p.get('f') or [None])[0] if p.get('f') else (round(float(p['t'][0]) * fps) if p.get('t') else None)
            if k in PHASE_EV and a is not None: ev.setdefault(s['canh'], []).append((int(a), f'pha {k}', 'campath.shots[].phases'))
    done = {s['canh'] for s in has_ph}
    for x, y in zip(F, F[1:]):
        c = y.get('canh')
        if c is None or c in done or x.get('canh') != c or y.get('phase') == x.get('phase') or y.get('phase') not in PHASE_EV: continue
        if y.get('f_canh') is None: continue
        ev.setdefault(c, []).append((int(y['f_canh']), f"pha {y['phase']}", 'campath.frames[].phase'))
    # đồng hồ
    seqs, step = {}, 1
    if any(f.get('clock') for f in F):
        for f in F:
            if f.get('clock') and f.get('canh') is not None and f.get('f_canh') is not None: seqs.setdefault(f['canh'], []).append((int(f['f_canh']), str(f['clock'])))
        src = 'campath.frames[].clock'
    elif B.get('frames_meta'):
        FM = B['frames_meta']; src = 'frames_meta'
        for c, m in (FM.items() if isinstance(FM, dict) else []):
            M = _ld(base, m); M = M.get('frames_meta', M) if isinstance(M, dict) else {}
            seqs[c] = sorted((int(k), str(v['clock'] if not isinstance(v['clock'], dict) else v['clock'].get('s'))) for k, v in M.items() if isinstance(v, dict) and v.get('clock'))
    elif B.get('log_chu'):
        L = _ld(base, B['log_chu']); L = L['frames'] if isinstance(L, dict) and 'frames' in L else L; byf = {f.get('f'): f for f in F}; src = 'log chữ (role clock, mẫu thưa)'
        fs = sorted(int(x['f']) for x in L or [])
        step = min((b - a for a, b in zip(fs, fs[1:]) if b > a), default=1)
        for x in L or []:
            c = next((it.get('s') for it in x.get('text') or x.get('items') or [] if it.get('role') == 'clock'), None); m = byf.get(x['f'])
            if c and m and m.get('canh') is not None and m.get('f_canh') is not None: seqs.setdefault(m['canh'], []).append((int(m['f_canh']), str(c)))
    else: src = None
    for c, sq in seqs.items():
        for a, b, lab, d in clock_stops(sorted(sq), step, fps): ev.setdefault(c, []).append((a, 'đồng hồ dừng', f'"{lab}" {d:.2f} s ({src})'))
    return ev


def tl_bien_co(V, bundles, heroes=None, fps=24):
    """V = view(); bundles = [(B, base)] → [(giây phim, đoạn, loại, mô tả)] biến cố cảnh tl ánh xạ qua shot có p.hero = canh"""
    EV = {}
    for B, base in bundles or []:
        for c, xs in tl_su_kien(B, base, fps).items(): EV.setdefault(c, []).extend(xs)
    if not EV: return []
    dir2k = {str(h.get('dir')): k for k, h in (heroes or {}).items() if isinstance(h, dict) and h.get('dir')}
    out, t_abs = [], 0.0
    for sid, dur, HZ, shots, _ in V:
        for j, sh in enumerate(shots):
            p = sh.get('p') or {}; c = p.get('hero') if p.get('hero') in EV else dir2k.get(str(p.get('dir')))
            if c not in EV: continue
            at = num(sh.get('at', 0)) or 0.0; end = num(shots[j + 1].get('at')) if j + 1 < len(shots) else dur
            f0 = num(p.get('frame0', p.get('off', 0))) or 0.0; sp = num(p.get('speed', 1)) or 1.0
            for fc, k, s in EV[c]:
                t = at + (fc - f0) / (fps * sp)
                if fc >= f0 and at <= t < end: out.append((round(t_abs + t, 3), sid, f'tl:{k}', f'{c} khung {fc}: {s}'))
        t_abs += dur
    return sorted(set(out))


def stats(ev, total):
    ev.sort(); U = []
    for e in ev:
        if not U or e[0] - U[-1][0] >= MERGE: U.append(e)
    if not U: return None
    gaps = [b[0] - a[0] for a, b in zip(U, U[1:])] + [total - U[-1][0]]
    g = max(gaps); i = gaps.index(g)
    return dict(n=len(ev), gop=len(U), tb=round(total / len(U), 2), dai_nhat=round(g, 2), dai_nhat_tu=f'{U[i][1]} {U[i][0]:.2f}s ({U[i][2]})')


def q37(E, TL=None, mp4=None, F=None, v113=False, tl=None):
    """v113=True: (d) khung tĩnh theo khung neo (1.13) — CHỈ BÁO (k2check hàng "Q37 (1.13)") tới khi chủ dự án duyệt; mặc định thước 1.11.0.
    tl = [(bộ timelapse, thư mục)] (1.15, I8): cộng biến cố đo trong cảnh tl vào (b), (c)."""
    V = view(E, TL); bad, ev, mk, t_abs, nob = [], [], [], 0.0, []
    for sid, dur, HZ, shots, B in V:
        T = spec_times(HZ, shots, dur); mk += [(t_abs + x, sid, 'mốc', '') for x in T if x < dur]
        if not B: nob.append(sid)
        else:
            if not any(b.get('k') == 'cut' and num(b.get('t')) == 0 for b in B): bad.append(f'(a) {sid}: thiếu biến cố cut ở 0 (đầu đoạn = cắt cảnh)')
            for b in B:
                t = num(b.get('t'))
                if t is None: bad.append(f'(a) {sid}: biến cố {b.get("k")} "{b.get("s")}" t = {b.get("t")!r} không phải số giây'); continue
                if not any(abs(t - x) <= TOL for x in T): bad.append(f'(a) {sid} {t:.2f}s {b.get("k")} "{b.get("s")}": không khớp mốc nào trong đặc tả (±{TOL} s)')
                ev.append((t_abs + t, sid, b.get('k'), b.get('s')))
        t_abs += dur
    if nob: bad.append(f'(a) {len(nob)}/{len(V)} đoạn không khai beats ({", ".join(nob[:6])}{"…" if len(nob) > 6 else ""})')
    TE = tl_bien_co(V, tl, dict(E.get('heroes') or {}, **((TL or {}).get('heroes') or {}))) if tl else []
    ev += [(t, sid, k, s) for t, sid, k, s in TE]
    S = stats(ev, t_abs) if ev else None; M = stats(mk, t_abs); near = []
    if S:
        if S['tb'] > MEAN_MAX: bad.append(f"(b) khoảng biến cố trung bình {S['tb']} s > {MEAN_MAX} s")
        if S['dai_nhat'] > GAP_MAX: bad.append(f"(c) khoảng dài nhất {S['dai_nhat']} s > {GAP_MAX} s (từ {S['dai_nhat_tu']})")
        near += [f"TB {S['tb']} s (ngưỡng {MEAN_MAX})"] if abs(S['tb'] - MEAN_MAX) <= 0.05 * MEAN_MAX else []
        near += [f"khoảng dài nhất {S['dai_nhat']} s (ngưỡng {GAP_MAX})"] if abs(S['dai_nhat'] - GAP_MAX) <= 0.05 * GAP_MAX else []
    st = None; troi = []; st_cu = None
    if mp4 and os.path.exists(mp4) or F is not None:
        F = gray160(mp4) if F is None else F
        st_cu = static_run(None, F); A = static_anchor(F) if v113 else [st_cu]; st = A[0] if A else (0.0, 0.0)
        for L, a in A:
            if L > STATIC_MAX: bad.append(f'(d) khung tĩnh {L} s > {STATIC_MAX} s (từ {int(a // 60)}:{a % 60:04.1f})')
            elif abs(L - STATIC_MAX) <= 0.05 * STATIC_MAX: near.append(f'khung tĩnh {L} s từ {int(a // 60)}:{a % 60:04.1f} (ngưỡng {STATIC_MAX})')
        troi = [x for x in _runs_cu(F, STATIC_MAX) if not any(L > STATIC_MAX and a <= x[1] + x[0] and x[1] <= a + L for L, a in A)] if v113 else []
    val = (f"{t_abs:.1f} s · " + (f"biến cố khai {S['n'] - len(TE)}{' + đo cảnh tl ' + str(len(TE)) if TE else ''} (gộp {S['gop']}) · TB {S['tb']} s · dài nhất {S['dai_nhat']} s" if S else 'không khai beats')
           + (f" · khung tĩnh ({'neo, < ' + str(STATIC_ANCHOR) + '/255' if v113 else 'khung liền < ' + str(STATIC_DIFF) + '/255'}) dài nhất {st[0]} s (từ {int(st[1] // 60)}:{st[1] % 60:04.1f})"
              + (f" · trôi chậm (thước cũ > {STATIC_MAX:g} s, không tĩnh): {len(troi)} quãng, dài nhất {max(troi)[0]} s từ {int(max(troi)[1] // 60)}:{max(troi)[1] % 60:04.1f}" if troi else '')
              if st else ' · khung tĩnh: không đo (không có master)')
           + (f" · tham khảo mốc đặc tả: TB {M['tb']} s, dài nhất {M['dai_nhat']} s ({M['dai_nhat_tu']})" if M and not S else '')
           + (f" · biến cố cảnh tl (đo, I8): {len(TE)} (" + ', '.join(f'{k[3:]} {sum(1 for x in TE if x[2] == k)}' for k in sorted({x[2] for x in TE})) + ')' if TE else ''))
    return dict(ok=not bad, loi=bad, val=val, note='; '.join(bad[:5]), sat_nguong=near, bien_co=S, moc_dac_ta=M, khung_tinh=st, khung_tinh_cu=st_cu,
                troi_cham=troi, tong_s=round(t_abs, 2), bien_co_tl=TE)


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    g = lambda k: a[a.index('--' + k) + 1] if '--' + k in a else None
    E = base.load(a[0]); TL = json.load(open(g('tl'))) if g('tl') else None
    BT = [(json.load(open(a[i + 1])), os.path.dirname(os.path.abspath(a[i + 1]))) for i, x in enumerate(a) if x == '--bo-tl']
    r = q37(E, TL, g('mp4'), tl=BT or None)
    print('Q37 ' + ('ĐẠT' if r['ok'] else 'TRƯỢT') + ' · ' + r['val'] + ''.join('\n  ' + x for x in r['loi'][:30])
          + ('\n  sát ngưỡng: ' + '; '.join(r['sat_nguong']) if r['sat_nguong'] else ''))
    if g('json'): json.dump(r, open(g('json'), 'w'), ensure_ascii=False, indent=1)
    sys.exit(0 if r['ok'] else 1)
