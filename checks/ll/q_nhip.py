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
            [--mp4 <master.mp4>] [--json ra.json]

Biến cố khai ở đặc tả: segments[].beats: [{t (giây trong đoạn, SỐ), k: cut|cam|region|route|ring|sticker|number|label|text|palette|score, s}].
TRƯỢT khi:
  (a) một biến cố khai không khớp mốc thật nào của đặc tả (±0,3 s); đoạn thiếu biến cố `cut` ở 0; đoạn không khai beats
  (b) khoảng biến cố trung bình (thời lượng / số biến cố sau khi gộp biến cố cách nhau < 0,25 s) > 3,5 s
  (c) khoảng dài nhất giữa hai biến cố (kể cả tới cuối phim) > 6 s
  (d) có master: khung tĩnh — chuỗi khung liền có sai khác trung bình < 0,6/255 (xám 160×90) dài nhất > 6 s
Không khai beats (tập cũ): báo thêm số đo "mốc đặc tả" (mọi mốc thật, cận trên số biến cố) để tham khảo — không thay được beats.
Trong ±5 % quanh 3,5 s và 6 s: nêu tên.
"""
import json, os, subprocess, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from checks.ll import base  # noqa: E402

TOL, MERGE, MEAN_MAX, GAP_MAX, STATIC_MAX, STATIC_DIFF = 0.3, 0.25, 3.5, 6.0, 6.0, 0.6


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


def static_run(mp4):
    import numpy as np
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-nostdin', '-i', mp4, '-map', '0:v:0', '-vf', 'scale=160:90,format=gray', '-f', 'rawvideo', '-'],
                         capture_output=True, check=True).stdout
    F = np.frombuffer(raw, np.uint8).reshape(-1, 90, 160).astype(np.float32); d = np.abs(np.diff(F, axis=0)).mean(axis=(1, 2))
    best = run = at = 0
    for i, v in enumerate(d):
        run = run + 1 if v < STATIC_DIFF else 0
        if run > best: best, at = run, i - run + 1
    return round(best / 24, 2), round(at / 24, 2)


def stats(ev, total):
    ev.sort(); U = []
    for e in ev:
        if not U or e[0] - U[-1][0] >= MERGE: U.append(e)
    if not U: return None
    gaps = [b[0] - a[0] for a, b in zip(U, U[1:])] + [total - U[-1][0]]
    g = max(gaps); i = gaps.index(g)
    return dict(n=len(ev), gop=len(U), tb=round(total / len(U), 2), dai_nhat=round(g, 2), dai_nhat_tu=f'{U[i][1]} {U[i][0]:.2f}s ({U[i][2]})')


def q37(E, TL=None, mp4=None):
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
    S = stats(ev, t_abs) if ev else None; M = stats(mk, t_abs); near = []
    if S:
        if S['tb'] > MEAN_MAX: bad.append(f"(b) khoảng biến cố trung bình {S['tb']} s > {MEAN_MAX} s")
        if S['dai_nhat'] > GAP_MAX: bad.append(f"(c) khoảng dài nhất {S['dai_nhat']} s > {GAP_MAX} s (từ {S['dai_nhat_tu']})")
        near += [f"TB {S['tb']} s (ngưỡng {MEAN_MAX})"] if abs(S['tb'] - MEAN_MAX) <= 0.05 * MEAN_MAX else []
        near += [f"khoảng dài nhất {S['dai_nhat']} s (ngưỡng {GAP_MAX})"] if abs(S['dai_nhat'] - GAP_MAX) <= 0.05 * GAP_MAX else []
    st = None
    if mp4 and os.path.exists(mp4):
        st = static_run(mp4)
        if st[0] > STATIC_MAX: bad.append(f'(d) khung tĩnh {st[0]} s > {STATIC_MAX} s (từ {st[1]} s)')
        elif abs(st[0] - STATIC_MAX) <= 0.05 * STATIC_MAX: near.append(f'khung tĩnh {st[0]} s (ngưỡng {STATIC_MAX})')
    val = (f"{t_abs:.1f} s · " + (f"biến cố khai {S['n']} (gộp {S['gop']}) · TB {S['tb']} s · dài nhất {S['dai_nhat']} s" if S else 'không khai beats')
           + (f" · khung tĩnh {st[0]} s (từ {int(st[1] // 60)}:{st[1] % 60:04.1f})" if st else ' · khung tĩnh: không đo (không có master)')
           + (f" · tham khảo mốc đặc tả: TB {M['tb']} s, dài nhất {M['dai_nhat']} s ({M['dai_nhat_tu']})" if M and not S else ''))
    return dict(ok=not bad, loi=bad, val=val, note='; '.join(bad[:5]), sat_nguong=near, bien_co=S, moc_dac_ta=M, khung_tinh=st, tong_s=round(t_abs, 2))


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    g = lambda k: a[a.index('--' + k) + 1] if '--' + k in a else None
    E = base.load(a[0]); TL = json.load(open(g('tl'))) if g('tl') else None
    r = q37(E, TL, g('mp4'))
    print('Q37 ' + ('ĐẠT' if r['ok'] else 'TRƯỢT') + ' · ' + r['val'] + ''.join('\n  ' + x for x in r['loi'][:30])
          + ('\n  sát ngưỡng: ' + '; '.join(r['sat_nguong']) if r['sat_nguong'] else ''))
    if g('json'): json.dump(r, open(g('json'), 'w'), ensure_ascii=False, indent=1)
    sys.exit(0 if r['ok'] else 1)
