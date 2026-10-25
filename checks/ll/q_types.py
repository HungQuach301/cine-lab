#!/opt/cine/bin/python
"""Q34 loại shot — luật khoá bản 1.10.1 (phiên K, 12/10/2026; chủ dự án xem Steel); 1.10.2 (13/10/2026): khiếu nại V về (c).
Áp kênh 2 (từ K2 tập 2), đọc ĐẶC TẢ.
Định nghĩa: checks/ll/RULES-LL.md (dòng Q34).

  q_types.py <episode.yaml> [--tl timeline.json] [--json ra.json]

Mỗi shot của phim chính khai `type` (cùng cấp với `tpl` trong đặc tả; `p.type` cũng nhận) ∈ TYPES.
Đặc tả khai thêm:
  places: [tên | {name, say}]                         say = cụm đọc đúng như lời (mặc định name)
  people: [{name, say, photo: <rid RIGHTS.md | clip_id SOURCES-FOOTAGE.csv>, ly_do: "…"}]
  anchors: [khoá numbers]                             số neo; không khai → mọi khoá `numbers` có hiện trên hình
Shot `photo` trỏ ảnh bằng `p.photo` (hoặc `p.rid`, `p.clip`). Shot `document`: `p.paper` (tên báo) + `p.date` (YYYY-MM-DD).
TRƯỢT khi:
  (0) shot thiếu `type` hoặc `type` ngoài TYPES; số shot đặc tả ≠ timeline. 1.12.1 (chủ dự án 16–17/10): thêm `timelapse` (cảnh xương sống
      thời gian `tl/<cảnh>`); số trên shot timelapse là lớp chữ 2D (bộ đếm), KHÔNG tính là hiện bằng 3D ở (c). ML1 vẫn nhận `tl: true`.
      1.14 (chủ dự án duyệt B3 17/10): thêm `strategic` (bản đồ chiến lược 2D/2.5D; luật riêng BD-1…BD-8, q_bando.py); tính là shot bản đồ ở (a).
      1.17.8 (khiếu nại ANIMATIC-T4-V2 §8, CHỈ tập từ T4 — `kenh2_tu_t4`/`n2p`): thêm `minh_hoa` (đoạn M-d, luật MINH-HOA/N2P/KIEM-2-MUC), `tu_lieu`
      (tư liệu/khắc toàn khung, luật TU-LIEU-10/OMNI), `that` (ảnh/footage thật, TU-LIEU-THAT). Không tính vào (c) 3D, không vào EXT của Q32.
  (a) một địa danh không có shot `map` giao [t − 6 s, t + 6 s], t = lần đầu lời nhắc tên; tên không có trong lời
  (b) một nhân vật có ảnh hợp lệ (rid trong RIGHTS.md hoặc clip_id trong sổ footage) mà không có shot `photo` ảnh đó giao ±6 s quanh lần nhắc đầu;
      không có ảnh hợp lệ mà không ghi `ly_do` (≥ 20 ký tự)
  (c) số neo hiện bằng chart3d/scene3d < 60 %, hoặc chỉ bằng card > 40 % (số neo không hiện: tính là không 3D).
      1.10.2 (khiếu nại V 12/10, chấp nhận): số trên shot `map` tính là hiện bằng 3D CHỈ KHI nhãn số bám neo `col:<id>` (đỉnh cột số liệu
      3D nhô khỏi địa cầu) VÀ `<id>` là một cột khai trong `heroes.<p.hero>.opt.cols` (timeline, không có thì đặc tả). Số in chữ trên
      bản đồ, nhãn địa danh/ghim, neo `col:` không có cột khai → không tính 3D
  (d) shot `document` > 3 s, hoặc thiếu tên báo/ngày. Thời lượng photo/document/footage cộng vào trần 40 % của Q32 (q_footage.py)
      1.11.0 (chủ dự án 15/10/2026, Q34(d)): `p.date` chỉ có năm (YYYY) HỢP LỆ khi nguồn chỉ ghi năm — khai `p.date_chi_nam`: lý do ≥ 20 ký tự
      (trích chỗ nguồn ghi năm, vd "masthead chỉ in 'Spring 1926'"); không khai → vẫn TRƯỢT như 1.10.1. Ngày đủ YYYY-MM-DD giữ nguyên.
      Trần 3 s của (d) chỉ dành cho `document` = ảnh chụp báo hiện đại.
  (e) 1.11.1 (chủ dự án 15/10/2026, O2-B): shot `record` = VĂN BẢN GỐC (Federal Register, luật, thư, hợp đồng) TRƯỢT khi
      > 12 s; không có dòng tô `hl` HIỆN TRONG SHOT — `p.hl: [{at: giây trong đoạn | [t0, t1]}]` hoặc `heroes.<p.hero>.opt.hl` (giờ cảnh, quy
      về giờ đoạn theo off/frame0 và speed của shot); không dẫn nguồn (khoá `sources` khớp `short`/`short9` trên dòng nguồn `p.src`/`cap[].src`,
      hoặc `p.nguon`/`p.luat`); nguồn là luật (`p.luat`, hoặc `sources.<k>.loai` ∈ luat/chinh_sach/quy_dinh) mà thiếu `loai`/`hieu_luc`.
"""
import json, os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from checks.ll import base  # noqa: E402

TYPES = ('scene3d', 'map', 'chart3d', 'photo', 'document', 'footage', 'card', 'record', 'timelapse', 'strategic')   # 1.11.1: record = văn bản gốc (O2-B); 1.12.1: timelapse (xương sống thời gian, design/k2v/tl); 1.14: strategic (bản đồ chiến lược, B3; luật BD-1…BD-8)
EXT = ('photo', 'document', 'footage', 'record')      # tính chung trần nguồn ngoài của Q32
WIN = 6.0
MIN_3D, MAX_CARD = 60.0, 40.0
DOC_MAX = 3.0
YEAR_ONLY_WHY = 20
REC_MAX = 12.0                             # 1.11.1 (O2-B): trần một shot `record` (văn bản gốc)
POLICY = {'luat', 'chinh_sach', 'quy_dinh'}                         # 1.11.0: lý do tối thiểu khi ngày chỉ có năm (nguồn chỉ ghi năm)
COL = 'col:'                                # 1.10.2: neo đỉnh cột số liệu 3D của bản đồ (design/k2v/map.js `cols`)


def map_col_nums(sh, heroes):
    """1.10.2 → khoá số của shot `map` có nhãn bám neo `col:<id>` với <id> là cột 3D khai trong heroes.<p.hero>.opt.cols"""
    p = sh.get('p') or {}; h = heroes.get(p.get('hero')) or {}
    ids = {str(c.get('id', i)) for i, c in enumerate((h.get('opt') or {}).get('cols') or []) if isinstance(c, dict)}
    out = []
    def walk(x):
        if isinstance(x, dict):
            a = x.get('a')
            if isinstance(x.get('num'), str) and isinstance(a, str) and a.startswith(COL) and a[len(COL):] in ids: out.append(x['num'])
            for v in x.values(): walk(v)
        elif isinstance(x, list):
            for v in x: walk(v)
    walk(p); return out


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


def cites(short, line):
    """tên nguồn ngắn có trên dòng nguồn, trọn từ (\"90 FR 1\" không khớp \"90 FR 17114\")"""
    return bool(re.search(r'(?<![\w])' + re.escape(short) + r'(?![\w])', line))


def as_list(v): return v if isinstance(v, list) else [v] if v else []


def _num(v): return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def hl_in_shot(p, HE, t0, t1):
    """(e) có dòng tô hiện trong shot [t0, t1) (giây trong đoạn): p.hl (giây đoạn) hoặc opt.hl của cảnh (giờ cảnh → giờ đoạn)"""
    first = lambda x: x[0] if isinstance(x, list) and x else x
    for x in as_list(p.get('hl')):
        at = _num(first(x.get('at'))) if isinstance(x, dict) else None
        if at is None or t0 - 1e-6 <= at < t1: return True
    o = ((HE.get(p.get('hero')) or {}).get('opt') or {}); f0 = (_num(p.get('frame0', p.get('off', 0))) or 0.0) / 24; sp = _num(p.get('speed', 1)) or 1.0
    for x in o.get('hl') if isinstance(o.get('hl'), list) else []:
        tau = _num(first(x.get('at'))) if isinstance(x, dict) else None
        if tau is None: continue
        t = t0 + (tau - f0) / sp
        if tau >= f0 and t < t1: return True
    return False


def types_tap(E):
    """1.17.8: danh mục `type` của tập — từ T4 thêm minh_hoa, tu_lieu, that (q_k1178.TYPES_T4); tập trước giữ TYPES"""
    if E.get('kenh2_tu_t4') or E.get('n2p'):
        from checks.ll import q_k1178
        return TYPES + q_k1178.TYPES_T4
    return TYPES


def q34(E, TL, ep_dir=None):
    from checks.ll import q_rights, q_footage
    S, P0 = typed(E, TL); P = {k: [] for k in 'abcde'}; TY = types_tap(E)
    P0 += [f"{sid}/{i} @{mmss(a)}: thiếu type" if not t else f"{sid}/{i}: type {t} ngoài {'/'.join(TY)}" for sid, i, a, b, t, *_ in S if t not in TY]
    W = None
    # (a) địa danh → map ±6 s
    for pl in E.get('places') or []:
        nm, say = (pl, pl) if isinstance(pl, str) else (pl.get('name'), pl.get('say') or pl.get('name'))
        W = W if W is not None else _words(TL); t = first_say(W, say)
        if t is None: P['a'].append(f'{nm}: không thấy "{say}" trong lời'); continue
        if not any(ty in ('map', 'strategic') and b >= t - WIN and a <= t + WIN for _, _, a, b, ty, *_ in S): P['a'].append(f'{nm} @{mmss(t)}: không có shot map trong ±{WIN:g} s')   # 1.14: strategic là shot bản đồ
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
    shown = {}; HE = dict(E.get('heroes') or {}, **(TL.get('heroes') or {}))
    for _, _, a, b, ty, sh, spec in S:
        for k in set(base.nums_in(sh.get('p') or {}, [], True)): shown.setdefault(k, set()).add(ty)
        if ty == 'map':
            for k in set(map_col_nums(sh, HE)): shown[k].add('map3d')   # 1.10.2: số bám đỉnh cột 3D của bản đồ = hiện bằng 3D
    A = list(E.get('anchors') or sorted(shown))
    n3 = sum(1 for k in A if shown.get(k, set()) & {'chart3d', 'scene3d', 'map3d'}); nc = sum(1 for k in A if shown.get(k) and shown[k] <= {'card'})
    s3, sc = (100 * n3 / len(A), 100 * nc / len(A)) if A else (100.0, 0.0)
    if A and s3 < MIN_3D: P['c'].append(f'số neo hiện bằng chart3d/scene3d/cột 3D bản đồ {n3}/{len(A)} = {s3:.0f} % < {MIN_3D:g} %')
    if A and sc > MAX_CARD: P['c'].append(f'số neo chỉ hiện bằng card {nc}/{len(A)} = {sc:.0f} % > {MAX_CARD:g} %')
    near = [f'số neo 3D {s3:.0f} % (ngưỡng {MIN_3D:g} %)'] if A and abs(s3 - MIN_3D) <= 0.05 * MIN_3D else []
    near += [f'số neo card {sc:.0f} % (ngưỡng {MAX_CARD:g} %)'] if A and abs(sc - MAX_CARD) <= 0.05 * MAX_CARD else []
    # (d) document
    for sid, i, a, b, ty, sh, spec in S:
        if ty != 'document': continue
        p = sh.get('p') or {}
        if b - a > DOC_MAX + 1e-6: P['d'].append(f'{sid}/{i} @{mmss(a)}: document {b - a:.1f} s > {DOC_MAX:g} s')
        dt = str(p.get('date') or '').strip(); why = str(p.get('date_chi_nam') or '').strip()
        if not str(p.get('paper') or '').strip(): P['d'].append(f'{sid}/{i} @{mmss(a)}: document thiếu tên báo (p.paper)')
        if re.fullmatch(r'\d{4}-\d\d-\d\d', dt): pass
        elif re.fullmatch(r'\d{4}', dt):
            if len(why) < YEAR_ONLY_WHY: P['d'].append(f'{sid}/{i} @{mmss(a)}: ngày chỉ có năm ({dt}) mà không khai p.date_chi_nam (nguồn chỉ ghi năm, lý do ≥ {YEAR_ONLY_WHY} ký tự)')
        else: P['d'].append(f'{sid}/{i} @{mmss(a)}: document thiếu ngày (p.date YYYY-MM-DD, hoặc YYYY khi nguồn chỉ ghi năm)')
    # (e) record — văn bản gốc (1.11.1, O2-B)
    SRC = E.get('sources') or {}
    for sid, i, a, b, ty, sh, spec in S:
        if ty != 'record': continue
        p = sh.get('p') or {}; w = f'{sid}/{i} @{mmss(a)}'; t0, t1 = sh['t0'], sh['t1']
        if b - a > REC_MAX + 1e-6: P['e'].append(f'{w}: record {b - a:.1f} s > {REC_MAX:g} s')
        elif b - a >= 0.95 * REC_MAX: near.append(f'{w}: record {b - a:.1f} s (ngưỡng {REC_MAX:g} s)')
        if not hl_in_shot(p, HE, t0, t1): P['e'].append(f'{w}: record không có dòng tô (p.hl hoặc opt.hl của cảnh) hiện trong shot')
        lines = [str(p.get('src') or '')] + [str(c.get('src') or '') for c in p.get('cap') or [] if isinstance(c, dict)]
        keys = {k for k, v in SRC.items() for f in ('short', 'short9') if str(v.get(f) or '').strip() and any(cites(str(v[f]).strip(), l) for l in lines)}
        law = set(as_list(p.get('luat'))); keys |= set(as_list(p.get('nguon'))) | law
        if not keys: P['e'].append(f'{w}: record không dẫn nguồn (sources khớp dòng nguồn, hoặc p.nguon/p.luat)'); continue
        for k in sorted(keys):
            v = SRC.get(k)
            if v is None: P['e'].append(f'{w}: nguồn {k} không có trong sources'); continue
            is_law = k in law or str(v.get('loai') or '') in POLICY
            if is_law and (str(v.get('loai') or '') not in POLICY or v.get('hieu_luc') in (None, False, '')):
                P['e'].append(f'{w}: nguồn luật {k} thiếu loai (luat/chinh_sach/quy_dinh) hoặc hieu_luc')
    T = float(TL['tong_s']); dur = {t: 0.0 for t in TY}
    for _, _, a, b, ty, *_ in S:
        if ty in dur: dur[ty] += b - a
    loi = [f'(0) {x}' for x in P0] + [f'({k}) {x}' for k in 'abcde' for x in P[k]]
    return dict(ok=not loi, loi=loi, muc=dict(P, **{'0': P0}), sat_nguong=near, note='; '.join(loi[:6]),
                ty_le={t: round(100 * v / T, 1) for t, v in dur.items() if v}, so_neo=dict(n=len(A), ba_d=n3, card=nc),
                val=f"{sum(1 for x in S if x[4] in TY)}/{len(S)} shot có type · " + ' · '.join(f'{t} {100 * v / T:.1f} %' for t, v in dur.items() if v)
                    + f" · số neo 3D {s3:.0f} %, chỉ card {sc:.0f} % ({len(A)} số) · địa danh {len(E.get('places') or [])} · nhân vật {len(E.get('people') or [])}")


if __name__ == '__main__':
    a = sys.argv[1:]; E = base.load(a[0])
    tl = a[a.index('--tl') + 1] if '--tl' in a else os.path.join(E['out'], 'timeline.json')
    r = q34(E, json.load(open(tl)), os.path.dirname(os.path.abspath(a[0])))
    print('Q34 ' + ('ĐẠT' if r['ok'] else 'TRƯỢT') + ' · ' + r['val'] + ''.join('\n  ' + x for x in r['loi'][:40]) + (f"\n  … {len(r['loi']) - 40} lỗi nữa" if len(r['loi']) > 40 else ''))
    if '--json' in a: json.dump(r, open(a[a.index('--json') + 1], 'w'), ensure_ascii=False, indent=1)
    sys.exit(0 if r['ok'] else 1)
