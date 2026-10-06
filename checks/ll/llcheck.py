"""Last Lamplighters — luật khoá v2 (phiên K, 06/10/2026). Mỗi hàm trả danh sách lỗi (rỗng = ĐẠT).

  q7(E, TL, logs)        nhãn ACTUAL/PROJECTION: hiện đủ nhãn của loại số có trong shot VÀ không hiện nhãn của loại không có;
                         tham số `kind` khai trên mẫu phải trùng loại của `num` đi kèm (lỗi S2 tập 2: ACTUAL trên −5,3 % dự báo)
  q12(paths)             thumbnail 1280×720, hộp chữ trong lề an toàn 5 % (lỗi T1 tập 2: chữ S bị cắt)
  q13(E, D, thumbs)      số trên tiêu đề/thumbnail/mô tả/Shorts truy về `numbers`; đúng dấu; số dự báo có dấu hiệu dự báo
  q20(logs, iso)         chữ không đè hình: cờ `hit` của log = 0 và (khi log có `zones`) mọi hộp chữ không giao vùng hình
  q23(E, TL, frames)     câu/thẻ nhiều số: cùng đối tượng (nguồn), cùng loại, cùng kỳ, cùng cơ sở phân loại — khác thì khung riêng
  q24(E, TL)             nhãn "(YYYY classification)" trên hình phải khớp cơ sở phân loại của số nó gắn (lỗi HSUS 135 nghìn, tập 3)
  q25(TL, logs)          thẻ khoảng số ("50–80 %") không hiện số trung gian (lỗi thẻ 50–80 % tập 2)
Định nghĩa chi tiết: checks/ll/RULES-LL.md.
"""
import glob, json, os, re

from checks.ll import base

PM = re.compile(r'project|forecast|expect|\bby 20\d\d|\(proj', re.I)        # dấu hiệu dự báo (K v2: bỏ "?" — câu hỏi không phải nhãn dự báo)
NUMRE = re.compile(r'(?<![\w.])([-+])?((?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?)(\s*%| ?million| ?percent|k\b)?')
NUMWORD = {'point', 'hundred', 'thousand', 'million', 'and', 'a'} | {w + s for w in ('twen', 'thir', 'for', 'fif', 'six', 'seven', 'eigh', 'nine') for s in ('ty',)}


def _dash(t): return (t or '').replace('−', '-').replace('–', '-').replace('—', '-')


# ---------- thuộc tính số ----------
def kind(N, k): return (N.get(k) or {}).get('kind')


def period(N, k):
    n = N.get(k) or {}
    m = re.search(r'(\d{4})\s*[-–]\s*(\d{2,4})', _dash(str(n.get('period') or '')) or '') or \
        (None if n.get('year') else re.search(r'(\d{4})\s*[-–]\s*(\d{2,4})', _dash(str(n.get('note') or ''))))
    if m:
        a, b = m.group(1), m.group(2); b = a[:4 - len(b)] + b; return (int(a), int(b))
    return (int(n['year']), int(n['year'])) if n.get('year') else None


def basis(N, k):
    n = N.get(k) or {}
    if n.get('basis'): return str(n['basis'])
    m = re.search(r'(\d{4}) classification', str(n.get('note') or '')); return m.group(1) if m else None


def is_change(N, k):   # tỷ lệ thay đổi: đơn vị '%' và chữ hiện có dấu +/− (32 % 'tỷ phần' không phải thay đổi)
    n = N.get(k) or {}; return str(n.get('unit', '')) == '%' and _dash(str(n.get('text', ''))).strip()[:1] in '+-'


def keys_in_text(N, s, prefer=()):
    """Khoá số mà chuỗi hiện nguyên văn `text` của số đó (ranh giới số, không dính dấu). Bỏ số nguyên trần < 100 (dễ trùng);
    chữ trùng nhiều khoá: lấy khoá đã khai trong `prefer`, không có thì bỏ (không đoán)."""
    s = _dash(s); out = set()
    by = {}
    for k, n in N.items(): by.setdefault(_dash(str(n.get('text', ''))), []).append(k)
    for t, ks in by.items():
        if not re.search(r'\d', t) or re.fullmatch(r'\d{1,2}', t): continue
        if re.search(r'(?<![\d,.+\-])' + re.escape(t) + r'(?![\d,])', s):
            if len(ks) == 1: out.add(ks[0])
            else: out |= set(ks) & set(prefer)
    return out


def keys_spoken(N, sent):
    """Khoá số mà câu lời nói đúng cụm `say`. Cụm phải đứng trọn (không dính số liền trước/sau: 'thirty-one point five percent'
    không chứa 'five percent'; 'thirteen percent' không chứa 'thirteen'); cụm nằm gọn trong cụm dài hơn của số khác thì bỏ."""
    w = [base.norm(x) for x in sent.split()]; w = [x for x in w if x]; sp = {}
    numw = lambda x: x in NUMWORD or x.endswith(('ty', 'teen')) or x in ('percent', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve')
    for k, n in N.items():
        sw = [base.norm(x) for x in str(n.get('say') or '').split()]; sw = [x for x in sw if x]
        for i in range(len(w) - len(sw) + 1) if sw else []:
            j = i + len(sw)
            if w[i:j] == sw and (i == 0 or not numw(w[i - 1]) or not numw(sw[0])) and (j == len(w) or not numw(w[j]) or not numw(sw[-1])):
                sp.setdefault(k, []).append((i, j))
    out = set()
    for k, L in sp.items():
        if any(not any((k2 != k and a2 <= a and b <= b2 and (b2 - a2) > (b - a)) for k2, L2 in sp.items() for a2, b2 in L2) for a, b in L): out.add(k)
    return out


def sentences(t): return [x.strip() for x in re.split(r'(?<=[.!?])\s+', (t or '').strip()) if x.strip()]


# ---------- Q7 ----------
def q7(E, TL, logs):
    N, bad = E.get('numbers', {}), []
    def walk(x, path):
        if isinstance(x, dict):
            if x.get('kind') in ('actual', 'projection') and isinstance(x.get('num'), str) and kind(N, x['num']) and kind(N, x['num']) != x['kind']:
                bad.append(f"{path}: khai kind={x['kind']} nhưng {x['num']} là {kind(N, x['num'])}")
            sub = base.nums_in(x.get('nums', []), [], True)
            if x.get('kind') in ('actual', 'projection') and sub and 'num' not in x and any(kind(N, k) and kind(N, k) != x['kind'] for k in sub):
                bad.append(f"{path}: khai kind={x['kind']} cho {', '.join(k for k in sub if kind(N, k) != x['kind'])} ({'/'.join(sorted({kind(N, k) for k in sub}))})")
            for kk, v in x.items(): walk(v, path)
        elif isinstance(x, list):
            for v in x: walk(v, path)
    for kd in ('segments', 'shorts'):
        for sg in TL.get(kd, []):
            for sh in sg['shots']:
                walk(sh.get('p', {}), f"{sg['id']}/{sh['tpl']}@{sh['t0']:.1f}")
                L = logs.get(sg['id'])
                if not L: continue
                ks = {kind(N, k) for k in base.nums_in(sh.get('p', {}), [], True)} - {None}
                ks |= set(re.findall(r"'kind': '(actual|projection)'", str(sh.get('p'))))
                win = [e for e in L.get('text', []) if sh['t0'] * 24 <= e['f'] < sh['t1'] * 24]
                if not win: continue   # không có khung mẫu trong shot: không đo được ở đây
                seen = ' '.join(it['s'] for e in win for it in e['items'])
                tags = set(re.findall(r'\b(ACTUAL|PROJECTION)\b', seen))
                for kd2 in ks:
                    if kd2.upper() not in tags: bad.append(f"{sg['id']}/{sh['tpl']}@{sh['t0']:.1f}: thiếu nhãn {kd2.upper()}")
                for tg in tags:
                    if tg.lower() not in ks: bad.append(f"{sg['id']}/{sh['tpl']}@{sh['t0']:.1f}: hiện nhãn {tg} mà shot không có số {tg.lower()}")
    return sorted(set(bad), key=bad.index)


# ---------- Q12 ----------
TW, TH, SAFE = 1280, 720, 0.05


def q12(paths):
    err = []
    for p in paths:
        try:
            from PIL import Image
            if not p.endswith('.boxes.json') and os.path.exists(p) and Image.open(p).size != (TW, TH): err.append(f'{os.path.basename(p)}: kích thước ≠ 1280×720')
        except ImportError: pass
        b = p + '.boxes.json' if not p.endswith('.boxes.json') else p
        if not os.path.exists(b): err.append(f'{os.path.basename(p)}: thiếu .boxes.json'); continue
        B = json.load(open(b)); x0s, x1s, y0s, y1s = TW * SAFE, TW * (1 - SAFE), TH * SAFE, TH * (1 - SAFE)
        if B.get('size', [TW, TH]) != [TW, TH]: err.append(f'{os.path.basename(p)}: hộp chữ đo trên khung {B.get("size")}')
        for x in B.get('boxes', []):
            a, b0, c, d = x['box']
            if a <= x0s or b0 <= y0s or c >= x1s or d >= y1s: err.append(f'{os.path.basename(p)} “{x["s"]}” hộp {x["box"]} chạm/vượt lề 5 %')
    return err


# ---------- Q13 ----------
def surfaces(E, D, thumbs):
    """Các dòng chữ phát hành: (nơi, chữ)."""
    items = [('tiêu đề', E.get('title') or '')] + [(f"hook {sh['id']}", sh.get('hook') or '') for sh in E.get('shorts', [])]
    for b in thumbs:
        b = b if b.endswith('.boxes.json') else b + '.boxes.json'
        if os.path.exists(b): items.append((os.path.basename(b)[:-11], ' '.join(x['s'] for x in json.load(open(b))['boxes'])))
    for f in sorted(glob.glob(os.path.join(D, '*description*.txt'))):
        t = open(f).read(); m = re.search(r'DESCRIPTION\n(.*?)\n(?:Chapters|Sources)\n', t, re.S)
        items += [(os.path.basename(f), x) for x in sentences(m.group(1) if m else '')]
    for f in sorted(glob.glob(os.path.join(D, '*shorts-text*.txt'))):
        items += [(os.path.basename(f), ln.split('#')[0].strip()) for ln in open(f) if ln.strip() and not re.match(r'\s*(Source|Music|Narration)', ln)]
    return items


def match_surface(E, txt):
    """→ (khoá khớp theo từng số, lỗi). Năm 1800–2100 phải có trong lời/số; đếm nhỏ < 10 không xét."""
    N = E.get('numbers', {}); vo = ' '.join((x.get('vo') or '') for x in E.get('segments', []) + E.get('shorts', []))
    years = set(int(y) for y in re.findall(r'\b(1[89]\d\d|20\d\d)\b', vo + ' ' + json.dumps(N, ensure_ascii=False)))
    t = re.sub(r'\b(\d{4})-(\d{2})\b', r'\1', _dash(txt)); hits, bad = [], []
    for m in NUMRE.finditer(t):
        sign, raw, suf = m.group(1), m.group(0).strip(), (m.group(3) or '').strip()
        v = float(m.group(2).replace(',', '')) * (1e6 if 'million' in suf else 1e3 if suf == 'k' else 1)
        if not suf and v == int(v) and 1800 <= v <= 2100 and ',' not in m.group(2):
            if int(v) not in years: bad.append(f'năm {raw} không có trong lời/số')
            continue
        if not suf and v < 10 and ',' not in m.group(2): continue
        pct = '%' in suf or 'percent' in suf
        tol = lambda n: 0.051 * abs(n) if suf in ('million', 'k') else 0.5
        hit = [k for k, n in N.items() if isinstance(n.get('v'), (int, float)) and abs(abs(v) - abs(float(n['v']))) <= max(tol(float(n['v'])), 1e-9)
               and (pct == str(n.get('unit', '')).startswith('%') or suf in ('million', 'k'))]
        if not hit: bad.append(f'"{raw}" không truy được về numbers'); continue
        if sign:   # K v2: dấu hiện trên chữ phải trùng dấu của số
            hs = [k for k in hit if (float(N[k]['v']) < 0) == (sign == '-')]
            if not hs: bad.append(f'"{raw}" sai dấu so với {hit[0]} ({N[hit[0]]["text"]})'); continue
            hit = hs
        if all(N[k]['kind'] == 'projection' for k in hit) and not PM.search(txt): bad.append(f'"{raw}" là số dự báo nhưng thiếu dấu hiệu dự báo')
        hits.append(hit)
    return hits, bad


def q13(E, D, thumbs):
    bad = []
    for where, txt in surfaces(E, D, thumbs):
        bad += [f'{where}: {b}' for b in match_surface(E, txt)[1]]
    return bad


# ---------- Q20 ----------
def _inter(a, b): return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def q20(logs, iso_ids=(), need_zones=False):
    """iso_ids: đoạn có cảnh isotype (vùng hình). need_zones: từ tập 6, log của các đoạn đó phải ghi `zones` (đo độc lập cờ hit)."""
    bad = []
    for k, L in logs.items():
        h = str(L.get('hit', '')).count('1')
        if h: bad.append(f'{k}: cờ va chạm ở {h} khung mẫu')
        if need_zones and k in iso_ids and not any('zones' in e for e in L.get('text', [])):
            bad.append(f'{k}: log thiếu `zones` (từ tập 6 bắt buộc với đoạn có isotype)')
        for e in L.get('text', []):
            for z in e.get('zones', []):
                for it in e['items']:
                    if _inter(it['box'], z): bad.append(f"{k} f{e['f']} “{it['s'][:30]}” đè vùng hình {z}"); break
    return bad


# ---------- Q23 ----------
def own_labeled(N, p):
    """Số MỨC (không phải tỷ lệ thay đổi) có nhãn riêng ghi năm của nó ngay trên mục (label/years/name): coi là khung riêng."""
    out = set()
    def walk(x):
        if isinstance(x, dict):
            k = x.get('num')
            if isinstance(k, str) and k in N and not is_change(N, k) and period(N, k):
                lab = ' '.join(str(x.get(f, '')) for f in ('label', 'years', 'name', 'title'))
                ys = [int(y) for y in re.findall(r'\b(1[89]\d\d|20\d\d)\b', lab)]
                if any(period(N, k)[0] <= y <= period(N, k)[1] for y in ys): out.add(k)
            for v in x.values(): walk(v)
        elif isinstance(x, list):
            for v in x: walk(v)
    walk(p); return out


def frames(E, TL):
    """Mọi 'khung' một câu/thẻ: (nơi, tập khoá số, chữ hiện trong khung)."""
    N, out = E.get('numbers', {}), []
    for kd in ('segments', 'shorts'):
        for sg in E.get(kd, []):
            for s in sentences(sg.get('vo')): out.append((f"lời {sg['id']}", keys_spoken(N, s), s, set()))
    for kd in ('segments', 'shorts'):
        for sg in TL.get(kd, []):
            for sh in sg['shots']:
                p = dict(sh.get('p', {})); caps = p.pop('cap', None) or []
                txt = json.dumps(p, ensure_ascii=False)
                out.append((f"thẻ {sg['id']}/{sh['tpl']}@{sh['t0']:.1f}", set(base.nums_in(p, [], True)), txt, own_labeled(N, p)))
                for c in caps:
                    s = c.get('s') or ''
                    out.append((f"chú thích {sg['id']} “{s[:40]}”", {c['num']} if c.get('num') else set(), s, set()))
    for where, txt in surfaces(E, os.path.join(os.path.dirname(E.get('_path', '')), 'phat-hanh'), E.get('_thumbs', [])):
        hits, _ = match_surface(E, txt)
        if len(hits) >= 2 and all(len(h) == 1 for h in hits): out.append((where, {h[0] for h in hits}, txt, set()))
    return out


def family(S, src):
    """Họ nguồn = cơ quan phát hành (chữ đầu của `short`, vd 'BLS'); không khai thì chính khoá nguồn."""
    sh = str((S.get(src) or {}).get('short') or src or ''); m = re.match(r'[A-Za-z&.]+', sh); return m.group(0).rstrip('.,') if m else str(src)


def frame_errors(N, K, txt='', S=None, own=()):
    S = S or {}
    K = {k for k in K if k in N}
    C0 = [k for k in K if is_change(N, k)]
    if own and len(K - set(own)) <= 1 and not C0: return []   # mọi số mức (trừ tối đa một) đều có nhãn năm riêng: khung riêng
    if len(K) < 2: return []
    err = []
    fam = {family(S, N[k].get('src')) for k in K}
    if len(fam) > 1: err.append(f"khác đối tượng (nguồn {'/'.join(sorted(map(str, fam)))})")
    A = [k for k in K if kind(N, k) == 'actual']; P = [k for k in K if kind(N, k) == 'projection']
    if A and P:
        ps = {period(N, k)[0] for k in P if period(N, k)}
        base_ok = lambda a: not is_change(N, a) and period(N, a) and period(N, a)[0] in ps and len(ps) == 1 and N[a].get('src') in {N[k].get('src') for k in P}
        nb = [a for a in A if not base_ok(a)]
        if nb: err.append(f"trộn ACTUAL ({', '.join(sorted(nb))}) với PROJECTION ({', '.join(sorted(P))}) không phải điểm gốc dự báo")
    C = [k for k in K if is_change(N, k)]
    if len({(kind(N, k), period(N, k)) for k in C}) > 1:
        err.append('tỷ lệ thay đổi khác loại/kỳ: ' + ', '.join(f"{N[k]['text']} ({kind(N, k)} {period(N, k)})" for k in sorted(C)))
    L = [k for k in K if not is_change(N, k)]; bs = {basis(N, k) for k in L} - {None}
    labelled = set(re.findall(r'(\d{4}) classification', txt))
    if len(bs) > 1 and not bs <= labelled:
        err.append(f"khác cơ sở phân loại ({'/'.join(sorted(bs))}) mà không ghi riêng từng cơ sở")
    elif bs and any(basis(N, k) is None and N[k].get('src') in {N[j].get('src') for j in L if basis(N, j)} for k in L) and not re.search(r'classification|basis', txt, re.I):
        err.append(f"số cùng nguồn có số khai cơ sở phân loại ({'/'.join(sorted(bs))}), có số không khai, mà khung không ghi rõ cơ sở")
    return err


def q23(E, TL):
    N, bad = E.get('numbers', {}), []
    for where, K, txt, own in frames(E, TL):
        bad += [f'{where}: {e}' for e in frame_errors(N, K, txt, E.get('sources', {}), own)]
    return bad


# ---------- Q24 ----------
def q24(E, TL):
    N, bad = E.get('numbers', {}), []
    def walk(x, where):
        if isinstance(x, dict):
            for se in x.get('series', []) or []:
                for i, lt in enumerate(se.get('ltext') or []):
                    nm = f"{se.get('name', '')} {lt}"
                    m = re.findall(r'(\d{4}) classification', nm)
                    if not m or i >= len(se.get('points', [])): continue
                    v = se['points'][i][1]; ks = [k for k, n in N.items() if n.get('v') == v]
                    for k in ks:
                        b = basis(N, k)
                        if b is None: bad.append(f"{where}: “{lt or v}” ghi {m[-1]} classification nhưng {k} không khai cơ sở phân loại")
                        elif b != m[-1] and (m[-1] in re.findall(r'(\d{4}) classification', lt) or not re.findall(r'(\d{4}) classification', lt)):
                            bad.append(f"{where}: “{lt or v}” ghi {m[-1]} classification nhưng {k} thuộc {b} classification")
            for v in x.values(): walk(v, where)
        elif isinstance(x, list):
            for v in x: walk(v, where)
    for kd in ('segments', 'shorts'):
        for sg in TL.get(kd, []):
            for sh in sg['shots']: walk(sh.get('p', {}), f"{sg['id']}/{sh['tpl']}@{sh['t0']:.1f}")
    return bad


# ---------- Q25 ----------
RANGE = re.compile(r'\d\s*[–-]\s*\d')


def q25(TL, logs):
    bad = []
    for kd in ('segments', 'shorts'):
        for sg in TL.get(kd, []):
            L = logs.get(sg['id'])
            for sh in sg['shots']:
                p = sh.get('p', {})
                if sh['tpl'] != 'bignum' or not (p.get('range') or isinstance(p.get('value'), list) or RANGE.search(str(p.get('text', '')))): continue
                if not L: continue
                allowed = _dash(json.dumps(p, ensure_ascii=False))
                for e in L.get('text', []):
                    if not sh['t0'] * 24 <= e['f'] < sh['t1'] * 24: continue
                    for it in e['items']:
                        s = _dash(it['s']).strip()
                        if re.search(r'\d', s) and s not in allowed:
                            bad.append(f"{sg['id']}/bignum@{sh['t0']:.1f} f{e['f']}: hiện “{it['s']}” ngoài khoảng {p.get('text')}"); break
    return bad
