#!/opt/cine/bin/python
"""FT1 chỉ báo footage/ảnh — luật khoá bản 1.12.0 (phiên K, 16/10/2026; chủ dự án duyệt luật 16/10). Mặc định CHỈ BÁO.
Định nghĩa: checks/ll/RULES-LL.md. Đọc ĐẶC TẢ + timeline (cùng cách ghép shot như Q34).

  q_ftg.py <episode.yaml> [--tl timeline.json] [--json ra.json]

Shot footage/ảnh = `type` ∈ {footage, photo, document} (hoặc tpl footage/archive, p.clip).
(a) tổng thời lượng footage/ảnh ≤ 20 % phim — TRẦN, không phải mục tiêu;
(b) mỗi shot footage/ảnh khai `ly_do_hinh` ∈ {bang_chung, con_nguoi, quy_mo, khoanh_khac} (bằng chứng · con người · quy mô · khoảnh khắc);
Không tính: ảnh có chú thích chiếm ≤ 1/3 khung (`p.ti_le_khung` ≤ 0,334, khai bởi bộ dựng) và hiện ≤ 6 s.
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from checks.ll import base, q_types  # noqa: E402

TRAN, NHO, NHO_S = 20.0, 1 / 3 + 1e-3, 6.0
LY_DO = ('bang_chung', 'con_nguoi', 'quy_mo', 'khoanh_khac')
LOAI = ('footage', 'photo', 'document')


def _f(x, k): return x.get(k) if x.get(k) is not None else (x.get('p') or {}).get(k)


def ft1(E, TL):
    S, bad = q_types.typed(E, TL); T = float(TL['tong_s']); M = {'a': [], 'b': []}; tinh = mien = 0.0; n = 0; ly = {}
    for sid, i, a, b, t, sh, spec in S:
        p = sh.get('p') or {}
        if not (t in LOAI or sh.get('tpl') in ('footage', 'archive') or p.get('clip')): continue
        n += 1; d = b - a; tl = _f(spec, 'ti_le_khung') or p.get('ti_le_khung')
        if t == 'photo' and tl is not None and float(tl) <= NHO and d <= NHO_S: mien += d; continue
        tinh += d; y = _f(spec, 'ly_do_hinh')
        ly[y] = ly.get(y, 0) + 1
        if y not in LY_DO: M['b'].append(f'{sid}/{i} @{q_types.mmss(a)} ({t}, {d:.1f} s): ' + ('không khai ly_do_hinh' if y is None else f'ly_do_hinh {y!r} ngoài {"/".join(LY_DO)}'))
    pct = 100 * tinh / T if T else 0.0
    if pct > TRAN: M['a'].append(f'footage/ảnh {tinh:.1f} s = {pct:.1f} % > {TRAN:.0f} %')
    sat = [f'(a) footage/ảnh {pct:.2f} % (trần {TRAN:.0f} %)'] if abs(pct - TRAN) <= 0.05 * TRAN else []
    loi = bad + M['a'] + M['b']
    return dict(ok=not loi, loi=loi, muc=M, sat_nguong=sat, pct=round(pct, 2), giay=round(tinh, 2), mien_s=round(mien, 2), ly_do=ly,
                val=f'{n} shot footage/ảnh · tính {tinh:.1f} s = {pct:.1f} % (miễn ảnh nhỏ {mien:.1f} s) · khai lý do: {sum(v for k, v in ly.items() if k in LY_DO)}/{sum(ly.values())}')


def main():
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    g = lambda k: a[a.index('--' + k) + 1] if '--' + k in a else None
    E = base.load(a[0]); TL = json.load(open(g('tl') or os.path.join(E['out'], 'timeline.json'))); R = ft1(E, TL)
    print(f"FT1: {'ĐẠT' if R['ok'] else 'TRƯỢT'} — {R['val']}"); [print('   ', x) for x in R['loi'][:30]]
    if g('json'): json.dump(R, open(g('json'), 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
