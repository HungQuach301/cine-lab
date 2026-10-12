#!/opt/cine/bin/python
"""Q34 loại shot — luật khoá bản 1.10.1 (phiên K, 12/10/2026; chủ dự án xem Steel). Áp kênh 2 (từ K2 tập 2), đọc ĐẶC TẢ.
Định nghĩa: checks/ll/RULES-LL.md (dòng Q34).

  q_types.py <episode.yaml> [--tl timeline.json] [--json ra.json]

Mỗi shot của phim chính khai `type` (cùng cấp với `tpl` trong đặc tả; `p.type` cũng nhận) ∈ TYPES.
Đặc tả khai thêm:
  places: [tên | {name, say}]                         say = cụm đọc đúng như lời (mặc định name)
  people: [{name, say, photo: <rid RIGHTS.md | clip_id SOURCES-FOOTAGE.csv>, ly_do: "…"}]
  anchors: [khoá numbers]                             số neo; không khai → mọi khoá `numbers` có hiện trên hình
Shot `photo` trỏ ảnh bằng `p.photo` (hoặc `p.rid`, `p.clip`). Shot `document`: `p.paper` (tên báo) + `p.date` (YYYY-MM-DD).
TRƯỢT khi:
  (0) shot thiếu `type` hoặc `type` ngoài TYPES; số shot đặc tả ≠ timeline
  (a) một địa danh không có shot `map` giao [t − 6 s, t + 6 s], t = lần đầu lời nhắc tên; tên không có trong lời
  (b) một nhân vật có ảnh hợp lệ (rid trong RIGHTS.md hoặc clip_id trong sổ footage) mà không có shot `photo` ảnh đó giao ±6 s quanh lần nhắc đầu;
      không có ảnh hợp lệ mà không ghi `ly_do` (≥ 20 ký tự)
  (c) số neo hiện bằng chart3d/scene3d < 60 %, hoặc chỉ bằng card > 40 % (số neo không hiện: tính là không 3D)
  (d) shot `document` > 3 s, hoặc thiếu tên báo/ngày. Thời lượng photo/document/footage cộng vào trần 40 % của Q32 (q_footage.py)
"""
import json, os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from checks.ll import base  # noqa: E402

TYPES = ('scene3d', 'map', 'chart3d', 'photo', 'document', 'footage', 'card')
EXT = ('photo', 'document', 'footage')      # tính chung trần nguồn ngoài của Q32
WIN = 6.0
MIN_3D, MAX_CARD = 60.0, 40.0
DOC_MAX = 3.0


def stype(spec, sh):
    return spec.get('type') or (spec.get('p') or {}).get('type') or (sh.get('p') or {}).get('type')


def typed(E, TL):
    """→ ([(đoạn, i, t0 tuyệt đối, t1, loại, shot timeline, shot đặc tả)], [lỗi ghép])"""
    out, bad = [], []
    SP = {s['id']: s.get('shots') or [] for s in E.get('segments') or []}
    for s in TL['segments']:
        sp = SP.get(s['id'], [])
        if len(sp) != len(s['shots']): bad.append(f"đoạn {s['id']}: đặc tả {len(sp)} shot ≠ timeline {len(s['shots'])}")
        for i, sh in enumerate(s['shots']):
            spec = sp[i] if i < len(sp) else {}
            out.append((s['id'], i, s['t0'] + sh['t0'], s['t0'] + sh['t1'], stype(spec, sh), sh, spec))
    return out, bad


def ext_seconds(E, TL):
    """giây photo/document/footage khai trong đặc tả mà Q32 chưa tính (Q32 đã tính tpl footage, p.clip, archive)"""
    if not E.get('segments'): return 0.0
    S, _ = typed(E, TL)
    return sum(b - a for _, _, a, b, t, sh, _ in S if t in EXT and sh.get('tpl') not in ('footage', 'archive') and not (sh.get('p') or {}).get('clip'))


def _words(TL):
    from checks.ll import q_av
    W = []
    for L in q_av.flat_words(TL).values(): W += [(w, a) for w, a, *_ in L]
    return sorted(W, key=lambda z: z[1])


def first_say(W, say):
    q = [base.norm(x).strip("'") for x in re.split(r"[\s\-‐–—]+", str(say)) if base.norm(x)]
    for i in range(len(W) - len(q) + 1):
        if [w for w, _ in W[i:i + len(q)]] == q: return W[i][1]
    return None


def mmss(t): return f'{int(t // 60)}:{t % 60:04.1f}'


def _photo_id(sh): p = sh.get('p') or {}; return p.get('photo') or p.get('rid') or p.get('clip')


def q34(E, TL, ep_dir=None):
    from checks.ll import q_rights, q_footage
    S, P0 = typed(E, TL); P = {k: [] for k in 'abcd'}
    P0 += [f"{sid}/{i} @{mmss(a)}: thiếu type" if not t else f"{sid}/{i}: type {t} ngoài {'/'.join(TYPES)}" for sid, i, a, b, t, *_ in S if t not in TYPES]
    W = None
    # (a) địa danh → map ±6 s
    for pl in E.get('places') or []:
        nm, say = (pl, pl) if isinstance(pl, str) else (pl.get('name'), pl.get('say') or pl.get('name'))
        W = W if W is not None else _words(TL); t = first_say(W, say)
        if t is None: P['a'].append(f'{nm}: không thấy "{say}" trong lời'); continue
        if not any(ty == 'map' and b >= t - WIN and a <= t + WIN for _, _, a, b, ty, *_ in S): P['a'].append(f'{nm} @{mmss(t)}: không có shot map trong ±{WIN:g} s')
    # (b) nhân vật → photo ±6 s
    ok_ids = set(q_rights.rows()) | (set(q_footage.load_so(os.path.join(ep_dir, q_footage.SO))[0]) if ep_dir else set())
    for pe in E.get('people') or []:
        pe = {'name': pe} if isinstance(pe, str) else pe; nm = pe.get('name'); ph = pe.get('photo')
        if not ph or ph not in ok_ids:
            if len(str(pe.get('ly_do') or '').strip()) < 20: P['b'].append(f'{nm}: không có ảnh hợp lệ ({ph or "chưa khai"}) và không ghi ly_do (≥ 20 ký tự)')
            continue
        W = W if W is not None else _words(TL); t = first_say(W, pe.get('say') or nm)
        if t is None: P['b'].append(f'{nm}: không thấy "{pe.get("say") or nm}" trong lời'); continue
        if not any(ty == 'photo' and _photo_id(sh) == ph and b >= t - WIN and a <= t + WIN for _, _, a, b, ty, sh, _ in S):
            P['b'].append(f'{nm} @{mmss(t)}: có ảnh hợp lệ {ph} nhưng không có shot photo ảnh đó trong ±{WIN:g} s')
    # (c) số neo
    shown = {}
    for _, _, a, b, ty, sh, spec in S:
        for k in set(base.nums_in(sh.get('p') or {}, [], True)): shown.setdefault(k, set()).add(ty)
    A = list(E.get('anchors') or sorted(shown))
    n3 = sum(1 for k in A if shown.get(k, set()) & {'chart3d', 'scene3d'}); nc = sum(1 for k in A if shown.get(k) and shown[k] <= {'card'})
    s3, sc = (100 * n3 / len(A), 100 * nc / len(A)) if A else (100.0, 0.0)
    if A and s3 < MIN_3D: P['c'].append(f'số neo hiện bằng chart3d/scene3d {n3}/{len(A)} = {s3:.0f} % < {MIN_3D:g} %')
    if A and sc > MAX_CARD: P['c'].append(f'số neo chỉ hiện bằng card {nc}/{len(A)} = {sc:.0f} % > {MAX_CARD:g} %')
    near = [f'số neo 3D {s3:.0f} % (ngưỡng {MIN_3D:g} %)'] if A and abs(s3 - MIN_3D) <= 0.05 * MIN_3D else []
    near += [f'số neo card {sc:.0f} % (ngưỡng {MAX_CARD:g} %)'] if A and abs(sc - MAX_CARD) <= 0.05 * MAX_CARD else []
    # (d) document
    for sid, i, a, b, ty, sh, spec in S:
        if ty != 'document': continue
        p = sh.get('p') or {}
        if b - a > DOC_MAX + 1e-6: P['d'].append(f'{sid}/{i} @{mmss(a)}: document {b - a:.1f} s > {DOC_MAX:g} s')
        if not str(p.get('paper') or '').strip() or not re.fullmatch(r'\d{4}-\d\d-\d\d', str(p.get('date') or '')): P['d'].append(f'{sid}/{i} @{mmss(a)}: document thiếu tên báo (p.paper) hoặc ngày (p.date YYYY-MM-DD)')
    T = float(TL['tong_s']); dur = {t: 0.0 for t in TYPES}
    for _, _, a, b, ty, *_ in S:
        if ty in dur: dur[ty] += b - a
    loi = [f'(0) {x}' for x in P0] + [f'({k}) {x}' for k in 'abcd' for x in P[k]]
    return dict(ok=not loi, loi=loi, muc=dict(P, **{'0': P0}), sat_nguong=near, note='; '.join(loi[:6]),
                ty_le={t: round(100 * v / T, 1) for t, v in dur.items() if v}, so_neo=dict(n=len(A), ba_d=n3, card=nc),
                val=f"{sum(1 for x in S if x[4] in TYPES)}/{len(S)} shot có type · " + ' · '.join(f'{t} {100 * v / T:.1f} %' for t, v in dur.items() if v)
                    + f" · số neo 3D {s3:.0f} %, chỉ card {sc:.0f} % ({len(A)} số) · địa danh {len(E.get('places') or [])} · nhân vật {len(E.get('people') or [])}")


if __name__ == '__main__':
    a = sys.argv[1:]; E = base.load(a[0])
    tl = a[a.index('--tl') + 1] if '--tl' in a else os.path.join(E['out'], 'timeline.json')
    r = q34(E, json.load(open(tl)), os.path.dirname(os.path.abspath(a[0])))
    print('Q34 ' + ('ĐẠT' if r['ok'] else 'TRƯỢT') + ' · ' + r['val'] + ''.join('\n  ' + x for x in r['loi'][:40]) + (f"\n  … {len(r['loi']) - 40} lỗi nữa" if len(r['loi']) > 40 else ''))
    if '--json' in a: json.dump(r, open(a[a.index('--json') + 1], 'w'), ensure_ascii=False, indent=1)
    sys.exit(0 if r['ok'] else 1)
