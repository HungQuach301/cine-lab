#!/opt/cine/bin/python
"""BAN-CUOI-T3 · NHỊP (F1/R3): khoảng giữa các biến cố hình khai trong log shot (đầu shot, cắt góc, su_kien, bước năm tl_buoc, minh hoạ, cú lặn) — tính cả đầu/cuối shot.
In shot có khoảng > 6 s và tổng: TB s/biến cố, dài nhất. Chỉ là số TỰ KHAI (đo thật ở k2check).  cuoi_nhip.py <log-shot.json> [--tran 6]"""
import json, sys
L = [x for x in json.load(open(sys.argv[1])) if 'kieu_khung' in x]; TR = float(sys.argv[sys.argv.index('--tran') + 1]) if '--tran' in sys.argv else 6.0
allg, n = [], 0
for x in L:
    d = x['dur']; ev = {0.0, d}
    ev |= {float(c) for c in x.get('cat_trong_shot') or []}
    ev |= {float(e['t']) for e in x.get('su_kien') or [] if e.get('t') is not None}
    ev |= {float(b['t']) for b in x.get('tl_buoc') or []}
    ev |= {float(m['t0']) for m in x.get('minh_hoa') or []}
    if x.get('lan'): ev.add(float(x['lan']['t']))
    ev = sorted(e for e in ev if 0 <= e <= d); g = [(round(b - a, 2), round(a, 2)) for a, b in zip(ev, ev[1:]) if b - a > 1e-3]
    n += len(ev) - 1; allg += [gg for gg, _ in g]
    big = [(gg, a) for gg, a in g if gg > TR]
    if big: print(f"{x['ma']:7s} {d:6.2f}s  khoảng > {TR:g} s: " + ', '.join(f'{gg} s từ {a}' for gg, a in big))
print(f'biến cố {n} · TB {sum(allg) / max(1, len(allg)):.2f} s · dài nhất {max(allg):.2f} s · số khoảng > {TR:g} s: {sum(1 for g in allg if g > TR)}')
