#!/opt/cine/bin/python
"""Q26b đa dạng bối cảnh — luật khoá LL v3 (phiên K, 09/10/2026, sau tập 7). Định nghĩa: checks/ll/RULES-LL.md.

  q_setting.py <timeline.json> [--json ra.json]      in bảng nhãn bối cảnh từng shot và kết luận

Lý do: tập 7 (Q31 vòng 5) — người xem cùng thấy "chán" ở văn phòng tối dùng lại nhiều lần (khoảng 8:00–9:20). Q26 đo đa dạng
KHUNG NHÌN (điểm ảnh), không thấy được việc phim đứng lâu ở cùng một nơi với nhiều góc máy khác nhau.

Nhãn bối cảnh (từ timeline, mỗi shot):
  plate      → cảnh đinh `heroes.<khoá>.hero` (vd ep07/tower): mọi góc máy (variant) của cùng một cảnh 3D là MỘT bối cảnh
  diptych    → hai nửa (`p.left.hero`, `p.right.hero`), mỗi nửa nặng 1/2 thời lượng shot (hai nửa cùng cảnh: cả shot)
  cảnh 2D toàn khung (street, office, rows, teller, desk, sign, stack, inspect, jobboard, pasteup, filmstrip) → "2d/<mẫu>"
  còn lại (thẻ số, chữ, trích dẫn, isotype, bản đồ, ảnh tư liệu archive, thẻ kết) → TRUNG TÍNH: không là bối cảnh
Ba điều kiện chặn (chủ dự án, 09/10/2026):
  (a) một bối cảnh chiếm > 25 % thời lượng phim (tong_s);
  (b) một bối cảnh hiện LIÊN TỤC > 90 s. Một quãng liên tục của X kéo dài qua các shot có X (cả diptych có một nửa là X) và qua
      shot trung tính; dứt khi gặp shot có bối cảnh khác mà không có X, hoặc khi chuỗi shot trung tính liền nhau dài > 8 s
      (= trần Q15 cho quãng không đổi hình: người xem đã rời nơi đó). Độ dài = từ đầu shot X đầu tiên tới cuối shot X cuối cùng;
  (c) nửa sau phim (t ≥ tong_s / 2) có < 3 bối cảnh; một bối cảnh chỉ được đếm khi hiện ≥ 3 s trong nửa sau (chớp 1 shot
      ngắn để đủ số không tính; luật cứng: không thêm phần tử chỉ để vượt ngưỡng).
Trong ±5 % quanh ngưỡng (a), (b) và (c) bằng đúng 3: nêu tên (sát ngưỡng).
"""
import json, os, sys

SCENE2D = ('street', 'office', 'rows', 'teller', 'desk', 'sign', 'stack', 'inspect', 'jobboard', 'pasteup', 'filmstrip')
MAX_SHARE = 25.0      # % thời lượng phim
MAX_RUN = 90.0        # s liên tục
MIN_HALF = 3          # bối cảnh trong nửa sau
HALF_MIN_S = 3.0      # s tối thiểu để một bối cảnh được đếm trong nửa sau
NEUTRAL_GAP = 8.0     # s trung tính liền nhau làm dứt quãng liên tục (trần Q15)


def label(sh, heroes):
    """→ {bối cảnh: trọng số} của một shot ({} = trung tính)"""
    p = sh.get('p') or {}; t = sh['tpl']
    hn = lambda k: (heroes.get(k) or {}).get('hero') or k
    if t == 'plate' and p.get('hero'): return {hn(p['hero']): 1.0}
    if t == 'diptych':
        hs = [hn(x['hero']) for x in (p.get('left'), p.get('right')) if isinstance(x, dict) and x.get('hero')]
        out = {}
        for h in hs: out[h] = out.get(h, 0) + 1.0 / len(hs)
        return out
    if t in SCENE2D: return {f'2d/{t}': 1.0}
    return {}


def shots(TL):
    """→ [(t0, t1, {bối cảnh: trọng số}, mẫu)] theo thời gian tuyệt đối (chỉ phim chính, không Shorts)"""
    H = TL.get('heroes') or {}; out = []
    for s in TL['segments']:
        for sh in s['shots']:
            a, b = s['t0'] + sh['t0'], s['t0'] + sh['t1']
            if b > a: out.append((round(a, 3), round(b, 3), label(sh, H), sh['tpl']))
    return out


def runs(S, x):
    """các quãng liên tục của bối cảnh x: [(đầu, cuối)]"""
    R, st, last, gap0 = [], None, None, None
    for a, b, L, _ in S:
        if x in L:
            if st is None: st = a
            last, gap0 = b, None
        elif not L:
            if st is not None:
                gap0 = a if gap0 is None else gap0
                if b - gap0 > NEUTRAL_GAP: R.append((st, last)); st, gap0 = None, None
        else:
            if st is not None: R.append((st, last)); st, gap0 = None, None
    if st is not None: R.append((st, last))
    return R


def mmss(t): return f'{int(t // 60)}:{t % 60:04.1f}'


def q26b(TL):
    S = shots(TL); T = float(TL['tong_s']); half = T / 2
    tot, sec = {}, {}
    for a, b, L, _ in S:
        for x, w in L.items():
            tot[x] = tot.get(x, 0) + w * (b - a)
            if b > half: sec[x] = sec.get(x, 0) + w * (b - max(a, half))
    share = {x: 100 * v / T for x, v in tot.items()}
    longest = {x: max((e - s_, s_, e) for s_, e in runs(S, x)) for x in tot}
    half_set = sorted(x for x, v in sec.items() if v >= HALF_MIN_S)
    bad, near = [], []
    for x, v in sorted(share.items(), key=lambda z: -z[1]):
        if v > MAX_SHARE: bad.append(f'{x} chiếm {v:.1f} % thời lượng (> {MAX_SHARE:g} %)')
        elif abs(v - MAX_SHARE) <= 0.05 * MAX_SHARE: near.append(f'{x} {v:.1f} % (ngưỡng {MAX_SHARE:g} %)')
    for x, (d, s_, e) in sorted(longest.items(), key=lambda z: -z[1][0]):
        if d > MAX_RUN: bad.append(f'{x} liên tục {d:.1f} s ({mmss(s_)}–{mmss(e)}, > {MAX_RUN:g} s)')
        elif abs(d - MAX_RUN) <= 0.05 * MAX_RUN: near.append(f'{x} liên tục {d:.1f} s ({mmss(s_)}–{mmss(e)}; ngưỡng {MAX_RUN:g} s)')
    if len(half_set) < MIN_HALF: bad.append(f'nửa sau ({mmss(half)}–{mmss(T)}) chỉ có {len(half_set)} bối cảnh (≥ {HALF_MIN_S:g} s): {", ".join(half_set) or "—"}')
    elif len(half_set) == MIN_HALF: near.append(f'nửa sau đúng {MIN_HALF} bối cảnh (bằng ngưỡng)')
    top = max(share.items(), key=lambda z: z[1]) if share else ('—', 0.0)
    lr = max(longest.items(), key=lambda z: z[1][0]) if longest else ('—', (0.0, 0.0, 0.0))
    trung_tinh = sum(b - a for a, b, L, _ in S if not L)
    return dict(ok=not bad, loi=bad, sat_nguong=near, note='; '.join(bad),
                val=f'{len(tot)} bối cảnh · lớn nhất {top[0]} {top[1]:.1f} % · liên tục dài nhất {lr[0]} {lr[1][0]:.1f} s · nửa sau {len(half_set)}'
                    f' · trung tính {100 * trung_tinh / T:.1f} %',
                ty_le={x: round(v, 1) for x, v in sorted(share.items(), key=lambda z: -z[1])},
                lien_tuc={x: [round(d, 1), mmss(s_), mmss(e)] for x, (d, s_, e) in sorted(longest.items(), key=lambda z: -z[1][0])},
                nua_sau={x: round(sec[x], 1) for x in sorted(sec, key=lambda z: -sec[z])},
                nhan=[[mmss(a), round(b - a, 1), tpl, {x: round(w, 2) for x, w in L.items()} or 'trung tính'] for a, b, L, tpl in S])


if __name__ == '__main__':
    a = sys.argv[1:]; TL = json.load(open(a[0])); r = q26b(TL)
    for row in r['nhan']: print(f'  {row[0]:>7}  {row[1]:>5} s  {row[2]:<9} {row[3]}')
    print(json.dumps(dict(ty_le=r['ty_le'], lien_tuc=r['lien_tuc'], nua_sau=r['nua_sau']), ensure_ascii=False, indent=1))
    print('Q26b ' + ('ĐẠT' if r['ok'] else 'TRƯỢT') + ' · ' + r['val'] + ('\n  ' + r['note'] if r['note'] else '')
          + ('\n  sát ngưỡng: ' + '; '.join(r['sat_nguong']) if r['sat_nguong'] else ''))
    if '--json' in a: json.dump(r, open(a[a.index('--json') + 1], 'w'), ensure_ascii=False, indent=1)
    sys.exit(0 if r['ok'] else 1)
