#!/opt/cine/bin/python
"""ML1–ML3 mạch truyện và lời — luật khoá bản 1.12.0 (phiên K, 16/10/2026; chủ dự án duyệt luật 16/10). Mặc định CHỈ BÁO.
Định nghĩa: checks/ll/RULES-LL.md (mục 1.12.0). Áp kênh 2.

  q_mach.py <episode.yaml> [--tl timeline.json] [--root <gốc repo chứa vo/>] [--khai mach.yaml] [--api] [--json ra.json]

Câu lời: tách từ căn chữ ElevenLabs (`<vo_file>.align.json` của từng đoạn trong timeline) theo dấu . ! ? cuối từ (trừ viết tắt U.S., Mr.,
chữ cái tắt "J."); giây tuyệt đối = t0 đoạn + vo_offset + giây trong căn chữ.

Khai trong đặc tả (khoá `mach:` ở gốc episode.yaml, hoặc tệp --khai):
  tom_tat: {tu: "<đầu câu đầu>", den: "<đầu câu cuối>"}       đoạn tóm tắt cuối (≤ 75 s, kết thúc trong 120 s cuối phim)
  luan_diem_chinh: [{claim: C22, cau: "<đầu câu>"}]          câu mang claim "luận điểm chính"
Shot khai `cau: "<đầu câu>"` hoặc `claim: <id>` (cùng cấp `tpl`, hoặc trong `p`). "<đầu câu>" = ≥ 12 ký tự đầu của câu, nguyên văn.

ML1 mạch truyện — (a) mỗi shot không phải timelapse gắn 1 câu lời hoặc 1 claim id: khai `cau`/`claim`, hoặc shot đặt bằng mốc lời
     `at: "@từ"` (suy: câu đang đọc lúc shot vào); (b) tổng thời lượng shot timelapse "trôi" (không gắn câu/claim nào) ≤ 15 % thời lượng
     phim; (c) `cau` không khớp câu nào trong lời, `claim` không có trong claims.md cạnh đặc tả. Shot timelapse = `type: timelapse`,
     `tl: true` (shot hoặc p), hoặc cảnh `heroes.<p.hero>.hero` bắt đầu "tl/".
ML2 lời lặp ý — một ý nói ≥ 2 lần ngoài đoạn tóm tắt cuối. Hai tầng: (1) ứng viên theo từ: cặp câu (i < j, không liền nhau, câu sau không
     nằm trong `tom_tat`) có điểm IDF-cosin từ nội dung ≥ 0,25, hoặc ≥ 0,15 và chung ≥ 1 bộ 3 từ liền (≥ 2 từ nội dung); tối đa 40 cặp điểm cao nhất;
     (2) chấm ngữ nghĩa từng cặp bằng Claude API, mô hình ghim (judge.MODEL), một lần gọi cho cả phim, trần $0,40/lần + $0,05 gọi thử; câu
     trả lời lưu theo SHA cặp câu (bộ nhớ đệm → tự kiểm không gọi API). Lặp = câu sau nói lại ý câu trước mà không thêm gì.
     Không chấm được (không API, lỗi) → THIẾU, không ĐẠT.
ML3 lời mời đăng ký — câu lời có "subscrib…/hit the bell/notification bell/join the channel/follow the channel": (a) phải nằm trọn trong
     60 s cuối phim, hoặc trọn trong ±5 s quanh một ranh chương (t0 các đoạn trừ đoạn đầu); (b) không câu "luận điểm chính" nào bắt đầu
     trong 20 s sau khi câu mời kết thúc. Không khai `luan_diem_chinh` → (b) THIẾU.
"""
import collections, hashlib, json, math, os, re, sys, tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from checks.ll import base, q_types  # noqa: E402

ABBR = {'u.s.', 'u.k.', 'mr.', 'mrs.', 'ms.', 'dr.', 'st.', 'no.', 'vs.', 'e.g.', 'i.e.', 'jr.', 'sr.', 'a.m.', 'p.m.', 'inc.', 'co.'}
ML1_PCT, ML2_MIN, ML2_NG, ML2_MAX, ML3_END, ML3_RANH, ML3_TRUOC = 15.0, 0.25, 0.15, 40, 60.0, 5.0, 20.0
TT_MAX, TT_END = 75.0, 120.0
SUB = re.compile(r"\bsubscrib|\bhit the bell|\bnotification bell|\blike and subscribe|\bjoin (?:us|the channel)\b|\bfollow (?:us|the channel)\b", re.I)
SW = set("""a an the and or but if of to in on at by for from with as is are was were be been being it its this that these those there here
they them their theirs we our us you you'll your i he she his her him who whom which what when where why how than then so not no nor do does did
has have had will would can could should may might must also just only even more most less very about into over under up down out off again
one ones like said says say""".split())


def norm(s): return re.sub(r'\s+', ' ', re.sub(r"[“”\"‘’'`]", "'", s)).strip()


def _end(raw):
    r = raw.strip('"\'”’)]»')
    if not re.search(r'[.!?]$', r): return False
    lo = r.lower()
    return not (lo in ABBR or re.fullmatch(r'[A-Z]\.', r) or re.fullmatch(r'(?:[A-Za-z]\.){2,}', r))


def cau_tu_loi(TL, root=None):
    """→ [dict(i, seg, part, t0, t1, s)] — câu lời có giây tuyệt đối (từ căn chữ của từng đoạn)"""
    root = root or base.REPO; out = []
    for sg in TL['segments']:
        vf = sg.get('vo_file')
        if not vf: continue
        p = os.path.join(root, re.sub(r'\.(mp3|wav|flac)$', '', vf) + '.align.json')
        if not os.path.exists(p): raise FileNotFoundError(f'thiếu căn chữ {p}')
        W = base.words(json.load(open(p))); off = sg['t0'] + float(sg.get('vo_offset') or 0); cur = []

        def flush():
            out.append(dict(i=len(out), seg=sg['id'], part=sg.get('part'), t0=round(off + cur[0][1], 3), t1=round(off + cur[-1][2], 3), s=' '.join(x[3] for x in cur)))
        for w in W:
            cur.append(w)
            if _end(w[3]): flush(); cur = []
        if cur: flush()
    return out


def tim_cau(C, dau):
    """chỉ số câu bắt đầu bằng "<đầu câu>" (≥ 12 ký tự, so sau chuẩn hoá dấu nháy/khoảng trắng); không thấy / mơ hồ → None"""
    d = norm(str(dau or '')).lower()
    if len(d) < 12: return None
    hit = [c['i'] for c in C if norm(c['s']).lower().startswith(d)]
    return hit[0] if len(hit) == 1 else None


def claims_md(ep_dir):
    p = os.path.join(ep_dir or '', 'claims.md')
    if not ep_dir or not os.path.exists(p): return None
    return set(re.findall(r'^\|\s*(C\d+[a-z]?)\s*\|', open(p).read(), re.M))


def _f(x, k): return x.get(k) if x.get(k) is not None else (x.get('p') or {}).get(k)


def is_tl(spec, sh, HE):
    t = spec.get('type') or (spec.get('p') or {}).get('type') or sh.get('type')
    hero = (HE.get((sh.get('p') or {}).get('hero')) or {}).get('hero') or ''
    return t == 'timelapse' or bool(_f(spec, 'tl')) or bool(_f(sh, 'tl')) or str(hero).startswith('tl/')


def ml1(E, TL, C, ep_dir=None, claims=None, v117=False):
    """v117 (1.17, CHỈ tập từ T3 — khiếu nại animatic T3): `cau: ""` = không gắn câu (không phải câu sai)."""
    S, bad = q_types.typed(E, TL); HE = TL.get('heroes') or E.get('heroes') or {}
    CL = set(claims) if claims is not None else claims_md(ep_dir); T = float(TL['tong_s']); M = {k: [] for k in 'abc'}; rows = []; tl_troi = 0.0; tl_all = 0.0; n_moc = 0
    for sid, i, a, b, t, sh, spec in S:
        tl = is_tl(spec, sh, HE); dau, cid = _f(spec, 'cau'), _f(spec, 'claim'); gan = None
        if v117 and isinstance(dau, str) and not dau.strip(): dau = None
        if dau is not None:
            k = tim_cau(C, dau)
            if k is None: M['c'].append(f"{sid}/{i}: cau {str(dau)[:40]!r} không khớp đúng một câu trong lời")
            else: gan = f'câu {k}'
        if cid is not None:
            if CL is None: M['c'].append(f'{sid}/{i}: claim {cid} — không có claims.md cạnh đặc tả để kiểm')
            elif str(cid) not in CL: M['c'].append(f'{sid}/{i}: claim {cid} không có trong claims.md')
            else: gan = gan or f'claim {cid}'
        if gan is None and isinstance(spec.get('at'), str) and '@' in spec['at']:
            k = next((c['i'] for c in C if c['t0'] - 0.35 <= a + 0.05 <= c['t1'] + 0.35), None)
            if k is not None: gan = f'câu {k} (suy từ mốc {spec["at"]})'; n_moc += 1
        rows.append(dict(shot=f'{sid}/{i}', t0=round(a, 2), t1=round(b, 2), tl=tl, gan=gan))
        if tl:
            tl_all += b - a
            if gan is None: tl_troi += b - a
        elif gan is None: M['a'].append(f'{sid}/{i} @{q_types.mmss(a)} ({t}, {b - a:.1f} s): không gắn câu lời hay claim')
    pct = 100 * tl_troi / T if T else 0.0
    if pct > ML1_PCT: M['b'].append(f'timelapse trôi {tl_troi:.1f} s = {pct:.1f} % > {ML1_PCT:.0f} %')
    sat = [f'(b) timelapse trôi {pct:.2f} % (ngưỡng {ML1_PCT:.0f} %)'] if abs(pct - ML1_PCT) <= 0.05 * ML1_PCT and tl_all else []
    loi = bad + M['a'] + M['b'] + M['c']
    n_gan = sum(r['gan'] is not None for r in rows)
    return dict(ok=not loi, loi=loi, muc=M, shots=rows, sat_nguong=sat, tl_troi_s=round(tl_troi, 2), tl_s=round(tl_all, 2), tl_troi_pct=round(pct, 2),
                val=f"{n_gan}/{len(rows)} shot gắn ({n_moc} suy từ mốc @từ) · timelapse {tl_all:.1f} s, trôi {pct:.1f} %")


# ---------------------------------------------------------------- ML2
def toks(s):
    out = []
    for x in re.findall(r"[a-z0-9]+(?:'[a-z]+)?", s.lower().replace('’', "'")):
        x = re.sub(r"'s$", '', x)
        if len(x) > 4 and x.endswith('ies'): x = x[:-3] + 'y'
        elif len(x) > 3 and x.endswith('s') and not x.endswith('ss'): x = x[:-1]
        out.append(x)
    return out


def content(s): return [x for x in toks(s) if x not in SW and not (len(x) == 1 and x.isalpha())]


def tom_tat(C, khai, T):
    """(tập chỉ số câu tóm tắt, lỗi khai)"""
    tt = (khai or {}).get('tom_tat')
    if not tt: return set(), []
    a, b = tim_cau(C, tt.get('tu')), tim_cau(C, tt.get('den'))
    if a is None or b is None or b < a: return set(), [f"tom_tat: không tìm thấy đúng câu đầu/cuối ({tt.get('tu')!r} … {tt.get('den')!r})"]
    d = C[b]['t1'] - C[a]['t0']
    if d > TT_MAX: return set(), [f'tom_tat dài {d:.1f} s > {TT_MAX:.0f} s — không miễn']
    if C[b]['t1'] < T - TT_END: return set(), [f"tom_tat kết thúc ở {q_types.mmss(C[b]['t1'])}, ngoài {TT_END:.0f} s cuối — không miễn"]
    return set(range(a, b + 1)), []


def ung_vien(C, mien=()):
    df = collections.Counter(w for c in C for w in set(content(c['s']))); N = len(C)
    idf = {w: math.log(N / df[w]) for w in df}; out = []
    for j in range(N):
        if j in mien: continue
        for i in range(j - 1):
            A, B = set(content(C[i]['s'])), set(content(C[j]['s'])); sh = A & B
            if not sh: continue
            sc = sum(idf[w] for w in sh) / math.sqrt(sum(idf[w] for w in A) * sum(idf[w] for w in B) or 1)
            ta, tb = toks(C[i]['s']), toks(C[j]['s'])
            ng = {g for g in set(zip(ta, ta[1:], ta[2:])) & set(zip(tb, tb[1:], tb[2:])) if sum(w not in SW for w in g) >= 2}
            if sc >= ML2_MIN or (ng and sc >= ML2_NG): out.append(dict(i=i, j=j, diem=round(sc, 3), bo3=len(ng), chung=sorted(sh)))
    out.sort(key=lambda r: (-r['diem'], -r['bo3'], r['i'], r['j']))
    return out[:ML2_MAX], len(out)


PROMPT_VER = 'ML2-v1'
PROMPT = """You check a documentary narration for REDUNDANT REPETITION: the viewer hears the same point twice.
Each item gives an earlier sentence A and a later sentence B (seconds in the film), each with its neighbouring sentences for context.
For each item answer repeat=true only if B restates an idea, claim or quotation already made in A and adds nothing new for the viewer.
NOT a repetition: a short hook or teaser that is developed in detail later; a callback that uses the earlier point to make a new point;
a deliberate comparison of two different values (then vs now); the same person, term or number used for a different point.
Reply with ONLY one JSON object: {"pairs":[{"id":"P1","repeat":true,"why":"<at most 15 words>"}, ...]} covering every id.

"""


def _key(a, b, model): return hashlib.sha256(f'{PROMPT_VER}|{model}|{norm(a)}|{norm(b)}'.encode()).hexdigest()


def _ctx(C, k): return ' '.join(f'[{x["s"]}]' if x['i'] == k else x['s'] for x in C[max(0, k - 1):k + 2])


def cham_api(C, pairs, out_dir=None, cap=0.40):
    """MỘT lần gọi Claude API (mô hình ghim judge.MODEL, fail closed) → ({id: (repeat, why)}, bản ghi chi phí)"""
    from checks.ll import judge
    body = PROMPT + '\n'.join(f"P{n + 1}. A ({C[p['i']]['t0']:.1f} s): {C[p['i']]['s']}\n    context A: {_ctx(C, p['i'])}\n"
                              f"    B ({C[p['j']]['t0']:.1f} s): {C[p['j']]['s']}\n    context B: {_ctx(C, p['j'])}" for n, p in enumerate(pairs))
    d = tempfile.mkdtemp(prefix='ml2-'); ghi = dict(model=judge.MODEL, prompt_ver=PROMPT_VER, prompt_sha256=hashlib.sha256(body.encode()).hexdigest(), n=len(pairs))
    pr = judge.probe(); ghi['probe_usd'] = pr['cost_usd']
    r = judge.call(body, d, cap); ghi.update(usd=r.get('cost_usd'), served=sorted((r.get('model_usage') or {}).keys()), secs=r.get('secs'))
    e = ([r['error']] if r['is_error'] else []) + judge.model_errors(r.get('model_usage'))
    js = judge.parse_json(r.get('result'))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True); open(os.path.join(out_dir, f"ml2-{ghi['prompt_sha256'][:12]}.jsonl"), 'w').write(r.get('transcript') or '')
    if e or not js or not isinstance(js.get('pairs'), list): raise RuntimeError('ML2 chấm ngữ nghĩa hỏng: ' + '; '.join(e or ['trả lời không phải JSON đúng dạng']))
    got = {str(x.get('id')): (bool(x.get('repeat')), str(x.get('why') or '')[:200]) for x in js['pairs'] if isinstance(x, dict)}
    miss = [f'P{n + 1}' for n in range(len(pairs)) if f'P{n + 1}' not in got]
    if miss: raise RuntimeError(f'ML2: câu trả lời thiếu {miss[:5]}')
    return got, ghi


def ml2(C, T, khai=None, cache=None, api=False, out_dir=None):
    """cache: dict SHA cặp → {repeat, why, model}; api=True → chấm cặp chưa có trong cache (ghi thêm vào cache)"""
    from checks.ll import judge
    mien, le = tom_tat(C, khai, T); P, n_all = ung_vien(C, mien); cache = cache if cache is not None else {}
    need = [p for p in P if _key(C[p['i']]['s'], C[p['j']]['s'], judge.MODEL) not in cache]; ghi = None
    if need and api:
        got, ghi = cham_api(C, need, out_dir)
        for n, p in enumerate(need):
            rp, why = got[f'P{n + 1}']; cache[_key(C[p['i']]['s'], C[p['j']]['s'], judge.MODEL)] = dict(repeat=rp, why=why, model=judge.MODEL, a=C[p['i']]['s'][:80], b=C[p['j']]['s'][:80])
        need = []
    lap, thieu = [], []
    for p in P:
        v = cache.get(_key(C[p['i']]['s'], C[p['j']]['s'], judge.MODEL))
        if v is None: thieu.append(p); continue
        p['repeat'], p['why'] = v['repeat'], v.get('why', '')
        if v['repeat']: lap.append(p)
    fm = lambda p: (f"{q_types.mmss(C[p['i']]['t0'])}–{q_types.mmss(C[p['i']]['t1'])} ↔ {q_types.mmss(C[p['j']]['t0'])}–{q_types.mmss(C[p['j']]['t1'])}: "
                    f"{C[p['j']]['s'][:70]!r} nói lại {C[p['i']]['s'][:50]!r} ({p.get('why', '')})")
    loi = le + [fm(p) for p in lap]
    th = [f'{len(thieu)}/{len(P)} cặp ứng viên chưa chấm ngữ nghĩa (không có câu trả lời đã lưu; chạy --api)'] if thieu else []
    kq = 'THIẾU' if thieu and not loi else None
    return dict(ok=not loi and not thieu, ket_qua=kq, loi=loi, thieu=th, lap=lap, ung_vien=P, n_ung_vien=n_all, mien_tom_tat=sorted(mien), api=ghi,
                val=f"{len(C)} câu · {n_all} cặp ứng viên (chấm {len(P) - len(thieu)}) · {len(lap)} lặp ý" + (f" · tóm tắt {len(mien)} câu" if mien else ' · không khai tóm tắt'))


# ---------------------------------------------------------------- ML3
def ml3(C, TL, khai=None):
    T = float(TL['tong_s']); R = [float(s['t0']) for s in TL['segments'][1:]]; M = {'a': [], 'b': []}; thieu = []
    sub = [c for c in C if SUB.search(c['s'])]
    ldc = []
    for x in (khai or {}).get('luan_diem_chinh') or []:
        k = tim_cau(C, x.get('cau'))
        if k is None: thieu.append(f"luan_diem_chinh {x.get('claim')}: không khớp đúng một câu ({str(x.get('cau'))[:40]!r})")
        else: ldc.append((k, x.get('claim')))
    if not (khai or {}).get('luan_diem_chinh') and sub: thieu.append('không khai luan_diem_chinh → (b) không kiểm được')
    for c in sub:
        cuoi = c['t0'] >= T - ML3_END
        ranh = next((b for b in R if b - ML3_RANH <= c['t0'] and c['t1'] <= b + ML3_RANH), None)
        if not cuoi and ranh is None:
            M['a'].append(f"{q_types.mmss(c['t0'])}–{q_types.mmss(c['t1'])} {c['s'][:60]!r}: không trong {ML3_END:.0f} s cuối (từ {q_types.mmss(T - ML3_END)}) "
                          f"và không trong ±{ML3_RANH:.0f} s quanh ranh chương")
        for k, cid in ldc:
            g = C[k]['t0'] - c['t1']
            if 0 <= g <= ML3_TRUOC:
                M['b'].append(f"{q_types.mmss(c['t0'])} lời mời đăng ký kết thúc {g:.1f} s trước luận điểm chính {cid} ({C[k]['s'][:50]!r} @{q_types.mmss(C[k]['t0'])})")
    loi = M['a'] + M['b']; kq = 'THIẾU' if thieu and not loi else None
    vt = '; '.join(f"{q_types.mmss(c['t0'])}" + (' (60 s cuối)' if c['t0'] >= T - ML3_END else '') for c in sub) or 'không có'
    return dict(ok=not loi and not thieu, ket_qua=kq, loi=loi, thieu=thieu, muc=M, cau_moi=[dict(t0=c['t0'], t1=c['t1'], s=c['s']) for c in sub],
                val=f'{len(sub)} câu mời: {vt} · {len(ldc)} luận điểm chính khai')


def main():
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    g = lambda k: a[a.index('--' + k) + 1] if '--' + k in a else None
    E = base.load(a[0]); TL = json.load(open(g('tl') or os.path.join(E['out'], 'timeline.json')))
    import yaml
    khai = yaml.safe_load(open(g('khai'))) if g('khai') else (E.get('mach') or {})
    C = cau_tu_loi(TL, g('root')); ep = os.path.dirname(os.path.abspath(a[0]))
    cp = os.path.join(E['out'], 'ml2-cache.json'); cache = json.load(open(cp)) if os.path.exists(cp) else {}
    R = dict(ML1=ml1(E, TL, C, ep), ML2=ml2(C, float(TL['tong_s']), khai, cache, api='--api' in a, out_dir=E['out']), ML3=ml3(C, TL, khai))
    if '--api' in a: json.dump(cache, open(cp, 'w'), ensure_ascii=False, indent=1)
    for k, r in R.items():
        print(f"{k}: {r.get('ket_qua') or ('ĐẠT' if r['ok'] else 'TRƯỢT')} — {r['val']}"); [print('   ', x) for x in (r['loi'] + r.get('thieu', []))[:30]]
    if g('json'): json.dump(R, open(g('json'), 'w'), ensure_ascii=False, indent=1, default=str)


if __name__ == '__main__':
    main()
