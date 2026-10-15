#!/opt/cine/bin/python
"""Q35 nhãn loại số (D5) + Q36 chữ trên màn hình — luật khoá bản 1.11.0 (phiên K, 15/10/2026). Kênh 2, từ K2 tập 3 (16:9, phim chính).
Căn cứ: chủ dự án V2b 14/10/2026 18:08 D5 ("nhãn ACTUAL số lịch sử chuyển phiên K"), chấm mù V2/V3 (ACTUAL lặp 2–3 lần một khung = nhiễu),
T2 lib/k2.js (nhãn ESTIMATE, origin/k2c-t2 @8ec1063); Kinh thánh kênh 2 §4 (dòng nguồn ngắn ≥ 38 px, duyệt 14/10 20:45; "Facts as of" chỉ với
luật đang hiệu lực). Định nghĩa: checks/ll/RULES-LL.md (Q35, Q36).

  q_chu.py <episode.yaml> --tl <timeline.json> [--logs <thư mục log render *.log.json>] [--json ra.json]

NGUỒN SỐ. (1) Có log render (render.js: chữ thật ở khung mẫu mỗi 12 khung) → đo trên log (chính thức ở G2).
(2) Không có log → MÔ HÌNH theo đặc tả + timeline (quy tắc vẽ nhãn của lib/k2.js @T2: mỗi shot plate có số actual/projection được một nhãn
góc; nhãn của từng tag/thẻ có `kind`; ESTIMATE chỉ ở tag/thẻ khai estimate) — dùng cho chạy thử trước render; cỡ chữ không đo được → THIẾU.

Q35 — TRƯỢT khi, ở một khung (thời điểm) bất kỳ:
  (a) số `actual` đang hiện mà không có nhãn ACTUAL trong khung, TRỪ KHI số có mốc thời gian rõ ràng: `numbers.<k>.year` (hoặc `date`)
      khai và năm/ngày đó hiện thành chữ trong cùng khung (chip năm, chữ nhãn, chữ phụ, chú thích, thẻ) → không bắt buộc ACTUAL
  (b) nhãn ACTUAL hiện > 1 lần trong khung
  (c) số `estimate` đang hiện mà khung không có nhãn ESTIMATE; số `projection` đang hiện mà không có PROJECTION
  (d) tag/thẻ khai `kind` khác `numbers.<num>.kind` của số đi kèm; shot hiện ESTIMATE/PROJECTION mà không có số loại đó hiện trong shot
Q36 — TRƯỢT khi:
  (a) dòng nguồn (16:9: `cap[].src` hoặc `p.src`, nối `· p.credit` như khi vẽ; nguồn của thẻ; chân bảng điểm) dài > 70 ký tự; có log:
      cỡ chữ < 38 px (cỡ = chiều cao chữ hoa log / 0,727) hoặc xuống > 1 dòng; không log → cỡ/dòng THIẾU (không ĐẠT)
  (b) khung hiện "Facts as of" mà shot không dẫn nguồn là LUẬT/CHÍNH SÁCH ĐANG HIỆU LỰC: một khoá `sources` (khớp chữ `short`/`short9`
      trên dòng nguồn của shot, `src` của số đang hiện, hoặc `p.luat`) có `loai` ∈ {luat, chinh_sach, quy_dinh} và `hieu_luc`
      (true hoặc ngày YYYY-MM-DD ≤ ngày "as of"), không có `het_hieu_luc` ≤ ngày "as of".
      1.11.1 (chủ dự án 15/10/2026, O3): NGOẠI LỆ — "Facts as of" trong CÂU MIỄN TRỪ trên hình (chú thích `cap` có `mien_tru: true`, hoặc
      shot khai `p.mien_tru: true`) được phép MỘT lần, hiện trọn trong 0:00–0:15 phim chính (cùng câu nối qua các shot liền nhau = một lần).
      Lần thứ hai, hoặc ngoài 0:00–0:15 → TRƯỢT. Ngoài câu miễn trừ: giữ luật trên.
"""
import glob, json, os, re, sys
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from checks.ll import base  # noqa: E402

SRC_MAX_CHARS, SRC_MIN_PX, CAP_RATIO = 70, 38.0, 0.727
MIEN_WIN = 15.0   # 1.11.1 (O3): câu miễn trừ có "Facts as of" chỉ ở 0:00–0:15, một lần
LBL = {'actual': 'ACTUAL', 'projection': 'PROJECTION', 'estimate': 'ESTIMATE'}
POLICY = {'luat', 'chinh_sach', 'quy_dinh'}
MON = {m: i + 1 for i, m in enumerate('jan feb mar apr may jun jul aug sep oct nov dec'.split())}


def mmss(t): return f'{int(t // 60)}:{t % 60:04.1f}'


def num(v): return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def _n(v): return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def vis(t, at, out=None, t0=0.0):
    a = num(at); a = t0 if a is None else a; o = num(out)
    return t >= a - 1e-6 and (o is None or t < o - 1e-6)


def kinds_in(x, acc):
    if isinstance(x, dict):
        if x.get('kind') in LBL: acc.add(x['kind'])
        for v in x.values(): kinds_in(v, acc)
    elif isinstance(x, list):
        for v in x: kinds_in(v, acc)
    return acc


def corner(p):
    """nhãn góc của shot plate (lib/k2.js @T2: JSON.stringify(p) có "kind":"projection" → PROJECTION, không thì "kind":"actual" → ACTUAL)"""
    k = kinds_in(p, set())
    return 'projection' if 'projection' in k else 'actual' if 'actual' in k else None


def src_lines(sh, p):
    """dòng nguồn 16:9 của shot (như lib/k2.js caps()/srcLine): [(chuỗi, từ giây, tới giây)]"""
    t0, t1 = sh['t0'], sh['t1']; out = []
    cred = p.get('credit')
    join = lambda s: (str(s) + ' · ' + str(cred)) if cred and s and str(s).strip() else (cred if cred else s)
    if p.get('card'):
        if p.get('src'): out.append((str(p['src']), t0, t1))
    else:
        caps = [c for c in p.get('cap') or [] if isinstance(c, dict)]
        if caps:
            if p.get('src') and num(caps[0].get('at')) is not None and caps[0]['at'] > t0: out.append((str(join(p['src'])), t0, caps[0]['at']))
            for i, c in enumerate(caps):
                s = join(c.get('src') or p.get('src')); a = num(c.get('at')); a = t0 if a is None else a
                b = num(caps[i + 1].get('at')) if i + 1 < len(caps) else t1
                if s and str(s).strip(): out.append((str(s), max(a, t0), b if b is not None else t1))
        elif p.get('src') or cred: out.append((str(join(p.get('src'))), t0, t1))
    foot = ((p.get('score') or {}).get('board') or {}).get('foot')
    if foot: out.append((str(foot), t0, t1))
    return [(s, a, b) for s, a, b in out if s and s.strip() and b > a]


def card_texts(c, t):
    S, N = [], []
    for k in ('title', 'big', 'sub', 'note', 's'):
        if isinstance(c.get(k), str): S.append(c[k])
    for it in c.get('items') or []:
        if isinstance(it, dict) and vis(t, it.get('at')):
            S += [str(it[k]) for k in ('s', 'sub', 'label', 'text', 'date', 'big') if it.get(k) is not None]
            N += base.nums_in(it, [], True)
    N += [c['num']] if isinstance(c.get('num'), str) else []
    return S, N


def model_frames(E, TL):
    """→ [(đoạn, i, t (giây trong đoạn), [chữ], {khoá số đang hiện}, [(nhãn, nguồn)])] theo mô hình đặc tả"""
    out = []
    for s in TL['segments']:
        for i, sh in enumerate(s['shots']):
            p = sh.get('p') or {}; c = p.get('card'); t0, t1 = sh['t0'], sh['t1']
            els = [x for k in ('tags', 'places') for x in (p.get(k) or []) if isinstance(x, dict)]
            ts = {t0 + 0.01, t1 - 0.01}
            for x in els + [p.get('year') if isinstance(p.get('year'), dict) else {}] + [x for x in p.get('cap') or [] if isinstance(x, dict)]:
                for k in ('at', 'out'):
                    v = num(x.get(k))
                    if v is not None and t0 < v < t1: ts.add(v + 0.01)
            if c:
                for it in c.get('items') or []:
                    v = num((it or {}).get('at')) if isinstance(it, dict) else None
                    if v is not None and t0 < v < t1: ts.add(v + 0.01)
            kd = corner(p)
            for t in sorted(ts):
                S, N, L = [], set(), []
                if c:
                    if vis(t, c.get('in'), c.get('out'), t0):
                        cs, cn = card_texts(c, t); S += cs; N |= set(cn)
                        if c.get('kind') in LBL and c.get('big'): L.append((LBL[c['kind']], 'thẻ'))
                        if kd: L.append((LBL[kd], 'góc'))
                else:
                    if kd: L.append((LBL[kd], 'góc'))
                    if isinstance(p.get('year'), dict) and vis(t, p['year'].get('at'), p['year'].get('out'), t0): S.append(str(p['year'].get('s', '')))
                    caps = [x for x in p.get('cap') or [] if isinstance(x, dict) and vis(t, x.get('at'), None, t0)]
                    if caps and caps[-1].get('s'): S.append(str(caps[-1]['s']))
                    for x in els:
                        if not vis(t, x.get('at'), x.get('out'), t0): continue
                        S += [str(x[k]) for k in ('s', 'sub') if x.get(k)]
                        if isinstance(x.get('num'), str): N.add(x['num'])
                        if x.get('kind') in LBL: L.append((LBL[x['kind']], f"tag \"{str(x.get('s', ''))[:20]}\""))
                if p.get('asof') and vis(t, p.get('asofAt'), None, t0): S.append(p['asof'] if isinstance(p['asof'], str) else 'Facts as of')
                S += [l for l, _ in L]
                out.append((s['id'], i, t, S, N, L))
    return out


def log_frames(E, TL, logdir):
    """→ cùng dạng model_frames, từ log render (chữ thật ở khung mẫu); số đang hiện = khoá trong shot có `text` hiện nguyên văn"""
    N = E.get('numbers') or {}; L = {}
    for f in glob.glob(os.path.join(logdir, '*.log.json')):
        try: J = json.load(open(f))
        except (OSError, ValueError): continue
        if J.get('fmt', '16x9') == '16x9' and J.get('id'): L[str(J['id'])] = J
    out = []
    for s in TL['segments']:
        J = L.get(str(s['id']))
        if not J: continue
        for e in J.get('text') or []:
            t = e['f'] / 24; i = next((j for j, sh in enumerate(s['shots']) if sh['t0'] <= t < sh['t1']), None)
            if i is None: continue
            S = [str(it.get('s', '')) for it in e.get('items') or []]; cand = set(base.nums_in(s['shots'][i].get('p') or {}, [], True))
            nv = {k for k in cand if str((N.get(k) or {}).get('text') or '')[:40] and any(str(N[k]['text'])[:40] in x for x in S)}
            out.append((s['id'], i, t, S, nv, [(x, 'log') for x in S if x in LBL.values()], e.get('items') or []))
    return out, L


def dated(n, S):
    """số có mốc thời gian rõ ràng: year/date khai VÀ hiện thành chữ trong khung"""
    for k in ('year', 'date'):
        v = n.get(k)
        if v is not None and str(v).strip() and any(str(v).strip()[:10] in x for x in S): return True
    return False


def q35(E, TL, logdir=None):
    N = E.get('numbers') or {}; P = {k: [] for k in 'abcd'}
    fr, logs = (log_frames(E, TL, logdir) if logdir else (None, None))
    if fr is None or not fr: fr = [x + ([],) for x in model_frames(E, TL)]; mode = 'mô hình đặc tả'
    else: mode = f'log render ({len(logs)} đoạn)'
    # (d) khai kind lệch số
    for s in TL['segments']:
        for i, sh in enumerate(s['shots']):
            def walk(x):
                if isinstance(x, dict):
                    if x.get('kind') in LBL and isinstance(x.get('num'), str) and (N.get(x['num']) or {}).get('kind') and N[x['num']]['kind'] != x['kind']:
                        P['d'].append(f"{s['id']}/{i} @{mmss(s['t0'] + sh['t0'])}: \"{str(x.get('s', ''))[:24]}\" khai {x['kind']} nhưng {x['num']} là {N[x['num']]['kind']}")
                    for v in x.values(): walk(v)
                elif isinstance(x, list):
                    for v in x: walk(v)
            walk(sh.get('p') or {})
    seen = set(); shown_lbl = {}; nmax = 0; at_max = None; tseg = {s['id']: s['t0'] for s in TL['segments']}
    for sid, i, t, S, NV, L, *_ in fr:
        w = f'{sid}/{i} @{mmss(tseg[sid] + t)}'; lab = [l for l, _ in L]; na = lab.count('ACTUAL')
        if na > nmax: nmax, at_max = na, w
        def once(k, msg):
            if (k, sid, i) not in seen: seen.add((k, sid, i)); P[k].append(msg)
        if na > 1: once('b', f'{w}: ACTUAL hiện {na} lần ({", ".join(src for l, src in L if l == "ACTUAL")})')
        kinds = {}
        for k in NV:
            kd = (N.get(k) or {}).get('kind')
            if kd: kinds.setdefault(kd, []).append(k)
        for k in kinds.get('actual', []):
            if 'ACTUAL' not in lab and not dated(N[k], S): once('a', f'{w}: số {k} ({N[k].get("text")}) actual không có nhãn ACTUAL và không có năm/ngày rõ ràng trên khung')
        for kd in ('estimate', 'projection'):
            for k in kinds.get(kd, []):
                if LBL[kd] not in lab: once('c', f'{w}: số {k} ({N[k].get("text")}) là {kd} mà khung không có nhãn {LBL[kd]}')
            if LBL[kd] in lab: shown_lbl.setdefault((sid, i), [w, set(), set()])[1].add(kd)
            if kinds.get(kd): shown_lbl.setdefault((sid, i), [w, set(), set()])[2].add(kd)
    for (sid, i), (w, lb, nk) in shown_lbl.items():   # (d) theo SHOT: nhãn góc hiện cả shot, số có thể hiện muộn hơn nhãn
        for kd in sorted(lb - nk): P['d'].append(f'{w}: shot hiện nhãn {LBL[kd]} mà không có số {kd} nào hiện trong shot')
    loi = [f'({k}) {x}' for k in 'abcd' for x in P[k]]
    return dict(ok=not loi, loi=loi, muc=P, nguon=mode, note='; '.join(loi[:6]),
                val=f'{mode} · {len(fr)} khung xét · ACTUAL nhiều nhất {nmax}/khung' + (f' ({at_max})' if nmax > 1 else '') + f' · lỗi a {len(P["a"])} · b {len(P["b"])} · c {len(P["c"])} · d {len(P["d"])}')


def asof_date(s):
    m = re.search(r'as of\s+(\d{1,2})\s+([A-Za-z]{3})[a-z]*\.?\s+(\d{4})', s, re.I)
    if m and m.group(2).lower()[:3] in MON: return date(int(m.group(3)), MON[m.group(2).lower()[:3]], int(m.group(1)))
    m = re.search(r'as of\s+([A-Za-z]{3})[a-z]*\.?\s+(\d{1,2}),?\s+(\d{4})', s, re.I)
    if m and m.group(1).lower()[:3] in MON: return date(int(m.group(3)), MON[m.group(1).lower()[:3]], int(m.group(2)))
    return None


def _d(v):
    try: return date.fromisoformat(str(v)[:10])
    except ValueError: return None


def in_force(src, when):
    if str(src.get('loai') or '') not in POLICY: return False
    h = src.get('hieu_luc'); het = src.get('het_hieu_luc')
    if h is None or h is False: return False
    if h is not True:
        d = _d(h)
        if d is None or (when and d > when): return False
    if het:
        d = _d(het)
        if d is None or not when or d <= when: return False
    return True


def q36(E, TL, logdir=None):
    SRC = E.get('sources') or {}; N = E.get('numbers') or {}; P = {'a': [], 'b': []}; thieu = []; near = []
    logs = {}
    if logdir:
        for f in glob.glob(os.path.join(logdir, '*.log.json')):
            try: J = json.load(open(f))
            except (OSError, ValueError): continue
            if J.get('fmt', '16x9') == '16x9' and J.get('id'): logs[str(J['id'])] = J
    nlines = 0; longest = (0, ''); done = set(); mien = dict(n=0, last=None)
    for s in TL['segments']:
        J = logs.get(str(s['id']))
        for i, sh in enumerate(s['shots']):
            p = sh.get('p') or {}; w = f"{s['id']}/{i} @{mmss(s['t0'] + sh['t0'])}"
            SL = src_lines(sh, p)
            for line, a, b in SL:
                nlines += 1; n = len(line)
                if n > longest[0]: longest = (n, f'{w} "{line}"')
                if (w, line) in done: continue
                done.add((w, line))
                if n > SRC_MAX_CHARS: P['a'].append(f'{w}: dòng nguồn {n} ký tự > {SRC_MAX_CHARS}: "{line}"')
                elif n >= SRC_MAX_CHARS * 0.95: near.append(f'{w}: dòng nguồn {n} ký tự (ngưỡng {SRC_MAX_CHARS})')
                if not J: continue
                fr = [e for e in J.get('text') or [] if a * 24 <= e['f'] < b * 24]
                hits = [(e, it) for e in fr for it in e.get('items') or [] if str(it.get('s', '')) == line[:40]]
                if not fr: continue
                if not hits: thieu.append(f'{w}: log không có dòng nguồn "{line[:40]}" ở các khung mẫu trong shot'); continue
                px = min(float(it.get('cap', 0)) / CAP_RATIO for e, it in hits)
                if px < SRC_MIN_PX - 0.5: P['a'].append(f'{w}: dòng nguồn cỡ {px:.1f} px < {SRC_MIN_PX:g} px')
                elif px < SRC_MIN_PX * 1.05: near.append(f'{w}: dòng nguồn {px:.1f} px (ngưỡng {SRC_MIN_PX:g})')
                e, it = hits[0]; y0 = it['box'][1]
                more = [x for x in e.get('items') or [] if x is not it and abs(float(x.get('cap', 0)) - float(it.get('cap', 0))) < 0.6
                        and str(x.get('s', '')) and str(x.get('s', '')) in line and str(x.get('s', '')) != line[:40] and abs(x['box'][0] - it['box'][0]) <= 3]
                if more or (len(line) > 40 and not any(len(str(x.get('s', ''))) >= 40 for _, x in hits)): P['a'].append(f'{w}: dòng nguồn xuống {1 + len(more)} dòng')
            if SL and not J: thieu.append(f'{w}: cỡ chữ/số dòng của dòng nguồn: không có log render')
            # (b) Facts as of
            texts = [str(p.get('asof') if isinstance(p.get('asof'), str) else ('Facts as of' if p.get('asof') else ''))]
            caps = [c for c in p.get('cap') or [] if isinstance(c, dict)]
            for j, cp in enumerate(caps):   # 1.11.1 (O3): câu miễn trừ có "Facts as of" được MỘT lần ở 0:00–0:15
                cs = str(cp.get('s', ''))
                if not re.search(r'facts as of', cs, re.I): continue
                if p.get('mien_tru') is True or cp.get('mien_tru') is True:
                    at = _n(cp.get('at')); a0 = s['t0'] + max(sh['t0'], at if at is not None else sh['t0'])
                    nx = next((_n(c2.get('at')) for c2 in caps[j + 1:] if _n(c2.get('at')) is not None), None)
                    a1 = s['t0'] + min(sh['t1'], nx if nx is not None else sh['t1'])
                    if mien['last'] and mien['last'][0] == cs and a0 <= mien['last'][1] + 0.1:   # cùng câu nối sang shot kế: một lần hiện
                        mien['last'] = (cs, a1)
                        if a1 > MIEN_WIN + 0.05: P['b'].append(f'{w}: câu miễn trừ có "Facts as of" kéo quá 0:{MIEN_WIN:02.0f} (tới {mmss(a1)})')
                        continue
                    if a0 < -1e-6 or a1 > MIEN_WIN + 0.05: P['b'].append(f'{w}: câu miễn trừ có "Facts as of" hiện {mmss(a0)}–{mmss(a1)}, ngoài 0:00–0:{MIEN_WIN:02.0f}'); continue
                    mien['n'] += 1; mien['last'] = (cs, a1)
                    if mien['n'] > 1: P['b'].append(f'{w}: "Facts as of" trong câu miễn trừ lần thứ {mien["n"]} (chỉ được một lần)')
                    continue
                texts.append(cs)
            c = p.get('card') or {}
            texts += [str(c.get(k, '')) for k in ('title', 'note', 'sub') if isinstance(c.get(k), str)]
            fa = [x for x in texts if re.search(r'facts as of', x, re.I)]
            if not fa: continue
            when = asof_date(fa[0]) or _d(E.get('asof'))
            keys = set()
            for line, _, _ in SL:
                for k, v in SRC.items():
                    if any(str(v.get(f) or '').strip() and re.search(r'(?<![\w])' + re.escape(str(v[f]).strip()) + r'(?![\w])', line) for f in ('short', 'short9')): keys.add(k)   # 1.11.1: trọn từ
            for k in base.nums_in(p, [], True): keys |= {x.strip() for x in str((N.get(k) or {}).get('src') or '').replace(',', ' ').split() if x.strip()}
            for k in (p.get('luat') if isinstance(p.get('luat'), list) else [p.get('luat')] if p.get('luat') else []): keys.add(k)
            ok = [k for k in keys if k in SRC and in_force(SRC[k], when)]
            if not ok:
                P['b'].append(f'{w}: "{fa[0][:60]}" mà shot không dẫn nguồn luật/chính sách đang hiệu lực (nguồn của shot: {", ".join(sorted(keys)) or "không có"}; '
                              f'cần sources.<k>.loai ∈ luat/chinh_sach/quy_dinh + hieu_luc)')
    loi = [f'({k}) {x}' for k in 'ab' for x in P[k]]
    return dict(ok=not loi and not thieu, loi=loi, thieu=thieu, muc=P, sat_nguong=near, note='; '.join((loi + thieu)[:6]),
                val=f"{nlines} dòng nguồn · dài nhất {longest[0]} ký tự · {'log ' + str(len(logs)) + ' đoạn' if logs else 'không có log (cỡ chữ THIẾU)'}"
                    f" · lỗi a {len(P['a'])} · b {len(P['b'])} · thiếu {len(thieu)}")


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    g = lambda k: a[a.index('--' + k) + 1] if '--' + k in a else None
    E = base.load(a[0]); TL = json.load(open(g('tl') or os.path.join(E['out'], 'timeline.json')))
    r5, r6 = q35(E, TL, g('logs')), q36(E, TL, g('logs'))
    for nm, r in (('Q35', r5), ('Q36', r6)):
        print(f"{nm} {'ĐẠT' if r['ok'] else 'TRƯỢT'} · {r['val']}" + ''.join('\n  ' + x for x in (r['loi'] + r.get('thieu', []))[:25])
              + (f"\n  … {len(r['loi']) + len(r.get('thieu', [])) - 25} mục nữa" if len(r['loi']) + len(r.get('thieu', [])) > 25 else '')
              + ('\n  sát ngưỡng: ' + '; '.join(r['sat_nguong'][:6]) if r.get('sat_nguong') else ''))
    if g('json'): json.dump(dict(Q35=r5, Q36=r6), open(g('json'), 'w'), ensure_ascii=False, indent=1)
    sys.exit(0 if r5['ok'] and r6['ok'] else 1)
