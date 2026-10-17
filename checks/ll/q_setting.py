#!/opt/cine/bin/python
"""Q26b đa dạng bối cảnh — luật khoá LL v3 (phiên K, 09/10/2026, sau tập 7; quãng liên tục theo chủ dự án 09/10/2026, 1.8.1;
đọc định dạng kênh 2 vshot/episode 1.10.2).
Định nghĩa: checks/ll/RULES-LL.md.

  q_setting.py <timeline.json> [--json ra.json]                     in bảng nhãn bối cảnh từng shot và kết luận
  q_setting.py <episode.yaml> [--tl timeline.json] [--json ra.json]  (1.10.2) như q_types/q_scene/q_footage: mặc định <out>/timeline.json;
                                                                     `type` khai trong đặc tả được ghép vào shot timeline (đoạn, thứ tự)

Lý do: tập 7 (Q31 vòng 5) — người xem cùng thấy "chán" ở văn phòng tối dùng lại nhiều lần (khoảng 8:00–9:20). Q26 đo đa dạng
KHUNG NHÌN (điểm ảnh), không thấy được việc phim đứng lâu ở cùng một nơi với nhiều góc máy khác nhau.

Nhãn bối cảnh (từ timeline, mỗi shot):
  plate      → cảnh đinh `heroes.<khoá>.hero` (vd ep07/tower): mọi góc máy (variant) của cùng một cảnh 3D là MỘT bối cảnh
  diptych    → hai nửa (`p.left.hero`, `p.right.hero`), mỗi nửa nặng 1/2 thời lượng shot (hai nửa cùng cảnh: cả shot)
  cảnh 2D toàn khung (street, office, rows, teller, desk, sign, stack, inspect, jobboard, pasteup, filmstrip) → "2d/<mẫu>"
  footage    → (1.10.0, Q32f) `p.setting` theo nội dung hình: khoá/tên cảnh đinh nếu cùng nơi với cảnh 3D, không thì nhãn tự do;
               không khai → gộp chung "ft/(chưa khai)" (Q32f TRƯỢT)
  thẻ/đồ hoạ phẳng → (1.10.1) MỘT bối cảnh riêng "the": shot có `p.card` (kênh 2: thẻ trên nền cảnh mờ, cả shot) hoặc mẫu thẻ giấy LL
               (bars, line, compare, quote, bignum, text). Trần (a) 25 %, (b) 90 s liên tục như mọi bối cảnh; KHÔNG tính vào (c)
               (chủ dự án 12/10/2026: Steel — người xem thấy "thẻ" là một bối cảnh; luật cũ tính theo cảnh nền nên đạt sai)
  còn lại (thẻ số, chữ, trích dẫn, isotype, bản đồ, ảnh tư liệu archive, thẻ kết) → TRUNG TÍNH: không là bối cảnh
  kênh 2 (1.10.2): mọi shot là `plate` + `type` (Q34; ở shot timeline do vshot ghi, hoặc ở đặc tả) — đọc theo `type` cùng nghĩa trên:
               card → "the"; footage → như footage; map, photo, document → TRUNG TÍNH (bản đồ, ảnh tư liệu); scene3d, chart3d,
               không khai → như plate (cảnh đinh `heroes.<khoá>.hero`)
Ba điều kiện chặn (chủ dự án, 09/10/2026; 1.10.1: "the" có trần (a), (b) riêng; với quãng (b) của bối cảnh khác, shot "the" vẫn
là trung tính như 1.8.1 — không làm dứt và không tính — để luật liên tục không bị nới):
  (a) một bối cảnh chiếm > 25 % thời lượng phim (tong_s);
  (b) một bối cảnh hiện LIÊN TỤC > 90 s. Quãng của X bắt đầu ở shot X đầu tiên (diptych có một nửa là X tính là có X). Shot trung
      tính KHÔNG làm dứt quãng. Quãng chỉ dứt khi các shot có bối cảnh khác X cộng dồn ≥ 8 s tính từ lần X xuất hiện gần nhất; X
      xuất hiện lại thì bộ đếm cộng dồn về 0. Độ dài quãng = từ đầu shot X đầu tiên tới cuối shot X cuối cùng, TRỪ thời lượng các
      shot trung tính nằm trong đó (shot bối cảnh khác < 8 s nằm giữa quãng vẫn tính);
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
CARD_TPL = ('bars', 'line', 'compare', 'quote', 'bignum', 'text')   # LL: mẫu thẻ giấy (kind 'card' trong scripts/ll/lib/charts.js)
THE = 'the'          # 1.10.1 (chủ dự án 12/10/2026, bài học Steel G2 §5.3): bối cảnh "thẻ"
OTHER_BREAK = 8.0     # s bối cảnh khác X cộng dồn (từ lần X gần nhất) làm dứt quãng của X
K2_NEUTRAL = ('map', 'photo', 'document', 'record')   # 1.11.1: record (văn bản gốc) như document. 1.10.2: kênh 2 `type` bản đồ / ảnh tư liệu / ảnh chụp báo → trung tính (cùng nghĩa map, archive của LL)


def stype(sh, spec=None):
    """`type` kênh 2 của một shot: shot timeline (vshot ghi cùng cấp `tpl`), `p.type`, rồi đặc tả (như q_types.stype)"""
    spec = spec or {}
    return sh.get('type') or (sh.get('p') or {}).get('type') or spec.get('type') or (spec.get('p') or {}).get('type')


def label(sh, heroes, spec=None):
    """→ {bối cảnh: trọng số} của một shot ({} = trung tính); spec = shot cùng vị trí trong đặc tả (kênh 2, để đọc `type`)"""
    p = sh.get('p') or {}; t = sh['tpl']; ty = stype(sh, spec)
    hn = lambda k: (heroes.get(k) or {}).get('hero') or k
    if p.get('card') or t in CARD_TPL or ty == 'card': return {THE: 1.0}   # 1.10.1: thẻ/đồ hoạ phẳng (K2 p.card trên nền mờ; LL thẻ giấy) = MỘT bối cảnh "the"
    if t == 'footage' or p.get('clip') or ty == 'footage':                 # 1.10.0 (Q32f): footage nguồn ngoài là bối cảnh theo NỘI DUNG HÌNH (`p.setting`)
        return {hn(str(p['setting']).strip()) if str(p.get('setting') or '').strip() else 'ft/(chưa khai)': 1.0}
    if ty in K2_NEUTRAL: return {}                        # 1.10.2: kênh 2 bản đồ / ảnh tư liệu / ảnh chụp báo → trung tính
    if t == 'plate' and p.get('hero'): return {hn(p['hero']): 1.0}
    if t == 'diptych':
        hs = [hn(x['hero']) for x in (p.get('left'), p.get('right')) if isinstance(x, dict) and x.get('hero')]
        out = {}
        for h in hs: out[h] = out.get(h, 0) + 1.0 / len(hs)
        return out
    if t in SCENE2D: return {f'2d/{t}': 1.0}
    return {}


def shots(TL, E=None):
    """→ [(t0, t1, {bối cảnh: trọng số}, mẫu)] theo thời gian tuyệt đối (chỉ phim chính, không Shorts); E = đặc tả (kênh 2) nếu có"""
    H = TL.get('heroes') or {}; out = []
    SP = {s['id']: s.get('shots') or [] for s in (E or {}).get('segments') or [] if isinstance(s, dict) and 'id' in s}
    for s in TL['segments']:
        sp = SP.get(s.get('id'), [])
        for i, sh in enumerate(s['shots']):
            a, b = s['t0'] + sh['t0'], s['t0'] + sh['t1']
            if b > a: out.append((round(a, 3), round(b, 3), label(sh, H, sp[i] if i < len(sp) else None), sh['tpl']))
    return out


def runs(S, x):
    """các quãng liên tục của bối cảnh x: [(độ dài trừ trung tính, đầu, cuối, trung tính trong quãng)]"""
    R, cur = [], None
    for a, b, L, _ in S:
        d = b - a
        if x in L:
            if cur is None: cur = dict(s=a, n=0.0, pend=0.0, other=0.0)
            cur['n'] += cur['pend']; cur['pend'] = cur['other'] = 0.0; cur['e'] = b
        elif cur is None: continue
        elif not L or (x != THE and set(L) == {THE}): cur['pend'] += d   # trung tính (và, 1.10.1, thẻ "the" với quãng của bối cảnh KHÁC): không dứt, không tính
        else:
            cur['other'] += d
            if cur['other'] >= OTHER_BREAK: R.append(cur); cur = None
    if cur is not None: R.append(cur)
    return [(c['e'] - c['s'] - c['n'], c['s'], c['e'], c['n']) for c in R]


def mmss(t): return f'{int(t // 60)}:{t % 60:04.1f}'


def q26b(TL, E=None):
    S = shots(TL, E); T = float(TL['tong_s']); half = T / 2
    tot, sec = {}, {}
    for a, b, L, _ in S:
        for x, w in L.items():
            tot[x] = tot.get(x, 0) + w * (b - a)
            if b > half: sec[x] = sec.get(x, 0) + w * (b - max(a, half))
    share = {x: 100 * v / T for x, v in tot.items()}
    longest = {x: max(runs(S, x)) for x in tot}
    half_set = sorted(x for x, v in sec.items() if v >= HALF_MIN_S and x != THE)   # 1.10.1: "the" có trần (a), (b) như mọi bối cảnh nhưng KHÔNG được đếm vào (c)
    bad, near = [], []
    for x, v in sorted(share.items(), key=lambda z: -z[1]):
        if v > MAX_SHARE: bad.append(f'{x} chiếm {v:.1f} % thời lượng (> {MAX_SHARE:g} %)')
        elif abs(v - MAX_SHARE) <= 0.05 * MAX_SHARE: near.append(f'{x} {v:.1f} % (ngưỡng {MAX_SHARE:g} %)')
    for x, (d, s_, e, n) in sorted(longest.items(), key=lambda z: -z[1][0]):
        w = f'{mmss(s_)}–{mmss(e)}, đã trừ {n:.1f} s trung tính'
        if d > MAX_RUN: bad.append(f'{x} liên tục {d:.1f} s ({w}; > {MAX_RUN:g} s)')
        elif abs(d - MAX_RUN) <= 0.05 * MAX_RUN: near.append(f'{x} liên tục {d:.1f} s ({w}; ngưỡng {MAX_RUN:g} s)')
    if len(half_set) < MIN_HALF: bad.append(f'nửa sau ({mmss(half)}–{mmss(T)}) chỉ có {len(half_set)} bối cảnh (≥ {HALF_MIN_S:g} s): {", ".join(half_set) or "—"}')
    elif len(half_set) == MIN_HALF: near.append(f'nửa sau đúng {MIN_HALF} bối cảnh (bằng ngưỡng)')
    top = max(share.items(), key=lambda z: z[1]) if share else ('—', 0.0)
    lr = max(longest.items(), key=lambda z: z[1][0]) if longest else ('—', (0.0, 0.0, 0.0, 0.0))
    trung_tinh = sum(b - a for a, b, L, _ in S if not L)
    return dict(ok=not bad, loi=bad, sat_nguong=near, note='; '.join(bad),
                val=f'{len(tot)} bối cảnh · lớn nhất {top[0]} {top[1]:.1f} % · liên tục dài nhất {lr[0]} {lr[1][0]:.1f} s · nửa sau {len(half_set)}'
                    f' · trung tính {100 * trung_tinh / T:.1f} %',
                ty_le={x: round(v, 1) for x, v in sorted(share.items(), key=lambda z: -z[1])},
                lien_tuc={x: [round(d, 1), mmss(s_), mmss(e), round(n, 1)] for x, (d, s_, e, n) in sorted(longest.items(), key=lambda z: -z[1][0])},
                nua_sau={x: round(sec[x], 1) for x in sorted(sec, key=lambda z: -sec[z])},
                nhan=[[mmss(a), round(b - a, 1), tpl, {x: round(w, 2) for x, w in L.items()} or 'trung tính'] for a, b, L, tpl in S])


def load_input(a):
    """1.10.2: đối số đầu là timeline.json (như cũ) hoặc episode.yaml (như các luật kênh 2) → (TL, E | None)"""
    if not a[0].lower().endswith(('.yaml', '.yml')): return json.load(open(a[0])), None
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
    from checks.ll import base
    E = base.load(a[0]); tl = a[a.index('--tl') + 1] if '--tl' in a else os.path.join(E['out'], 'timeline.json')
    if not os.path.exists(tl): sys.exit(f'Q26b: không thấy timeline {tl} (đặc tả {a[0]}); dựng trước hoặc chỉ rõ --tl <timeline.json>')
    return json.load(open(tl)), E


if __name__ == '__main__':
    a = sys.argv[1:]; TL, E = load_input(a); r = q26b(TL, E)
    for row in r['nhan']: print(f'  {row[0]:>7}  {row[1]:>5} s  {row[2]:<9} {row[3]}')
    print(json.dumps(dict(ty_le=r['ty_le'], lien_tuc=r['lien_tuc'], nua_sau=r['nua_sau']), ensure_ascii=False, indent=1))
    print('Q26b ' + ('ĐẠT' if r['ok'] else 'TRƯỢT') + ' · ' + r['val'] + ('\n  ' + r['note'] if r['note'] else '')
          + ('\n  sát ngưỡng: ' + '; '.join(r['sat_nguong']) if r['sat_nguong'] else ''))
    if '--json' in a: json.dump(r, open(a[a.index('--json') + 1], 'w'), ensure_ascii=False, indent=1)
    sys.exit(0 if r['ok'] else 1)
