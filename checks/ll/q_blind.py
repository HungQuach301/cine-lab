#!/opt/cine/bin/python
"""Q27 chấm hình mù · Q31 xem liền mạch mù — luật khoá LL v3 (phiên K, 07/10/2026). Định nghĩa: checks/ll/RULES-LL.md.

K CỐ ĐỊNH: đề bài (checks/ll/blind/Q27-R*.txt, Q31-R*.txt, khoá SHA cùng checks/), cách lấy và trộn mẫu, số người chấm (3), mô hình
(subagent Sonnet), ngưỡng. P KHÔNG sửa đề bài: chỉ thay {DIR} bằng thư mục bộ ảnh; câu trả lời ghi lại SHA-256 của tệp đề bài.

  q_blind.py q27-set <thư mục> --new <video…>            bộ 60 ảnh F01–F60 (30 tập mới + 30 tập 1, trộn; Q-L27 = B) + đề bài đã điền
  q_blind.py q31-set <thư mục> --video <video…> --tl <timeline.json>   dải chuyển đoạn T## + dải tổng quan R## + transitions.txt
  q_blind.py q27-score <thư mục> --new <video…>          chấm (đọc R1.json, R2.json, R3.json); mã thoát 0 = ĐẠT
  q_blind.py q31-score <thư mục> --video <video…> --tl <timeline.json>

Thư mục bộ ảnh phải nằm NGOÀI repo (ví dụ <out>/blind/q27): subagent chỉ được đọc tệp nêu trong đề bài.
Q27 không ghi tệp khoá giải mã: thứ tự trộn suy lại được từ SHA-256 của video mới (hạt giống), nên không có gì để lộ cho người chấm.
Q31 tính VÒNG theo từng tập (Q-L31, chủ dự án 07/10/2026): q31-set chuyển lần xem trước sang <thư mục>-lich-su/vong-NN; vòng 1 chặn
điểm đứt mạch ≥ 2/3; từ vòng 2 chỉ chặn điểm 3/3, điểm 2/3 phải có giải trình trong <thư mục>/giai-trinh.json (chép vào báo cáo G2).
"""
import hashlib, json, os, random, re, shutil, subprocess, sys, tempfile

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'blind')
RATERS = ('R1', 'R2', 'R3')
MODEL = 'sonnet'
N27 = 30            # Q-L27 = B (chủ dự án 07/10/2026): 30 khung tập mới + 30 khung tập 1
REF27 = [('screening/ll-ep01-m23-p1.mp4', '4c8b71e9bace1648a27851113271704e8b8233e696f79949fba61e581f9338a5'),
         ('screening/ll-ep01-m23-p2.mp4', '9a258f6b4d3b658702adfcefe84ee5d260574604db733d69cf4b6ac4c670e5d5'),
         ('screening/ll-ep01-m23-p3.mp4', 'aac50b57d69f81ab885d9c906a584df8c7fe5653832e06b517d9bb84a5c5af4f')]   # tập 1 bản m23 (chuẩn gốc)
CRIT = ('beauty', 'detail', 'light')
EDGE = 1.0          # bỏ 1 s đầu/cuối mỗi phần
WIN31 = (-2.5, -1.5, -0.5, 0.5, 1.5, 2.5)
STRIP_STEP, STRIP_N = 4, 8
NEAR31 = 4.0        # hai vị trí cách ≤ 4 s là cùng một điểm
GT_MIN = 20         # giải trình điểm 2/3 (từ vòng 2): ≥ 20 ký tự


def P(p): return p if os.path.isabs(p) else os.path.join(REPO, p)


def sha_file(p):
    h = hashlib.sha256()
    with open(P(p), 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def dur(v): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', P(v)], capture_output=True, text=True, check=True).stdout)


def grab(v, t, out, w=1280):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', P(v), '-frames:v', '1', '-vf', f'scale={w}:-2', '-q:v', '3', out], check=True)


def prompt_sha(name): return sha_file(os.path.join(HERE, name))


def render_prompts(out, rule):
    for r in RATERS:
        tpl = open(os.path.join(HERE, f'{rule}-{r}.txt'), encoding='utf-8').read()
        open(os.path.join(out, f'PROMPT-{r}.txt'), 'w', encoding='utf-8').write(tpl.replace('{DIR}', out))


# ---------------------------------------------------------------- Q27
def strat(vids, n, R):
    """n thời điểm phân tầng đều trên tổng thời lượng dùng được (mỗi tầng một điểm ngẫu nhiên)"""
    L = [(v, dur(v)) for v in vids]; tot = sum(d - 2 * EDGE for _, d in L); out = []
    for k in range(n):
        x = (k + R.random()) / n * tot
        for v, d in L:
            if x < d - 2 * EDGE: out.append((v, round(EDGE + x, 3))); break
            x -= d - 2 * EDGE
    return out


def plan27(new):
    seed = hashlib.sha256(''.join(sha_file(v) for v in new).encode()).hexdigest()
    R = random.Random(int(seed[:16], 16))
    items = [('new', v, t) for v, t in strat(new, N27, R)] + [('ref', v, t) for v, t in strat([v for v, _ in REF27], N27, R)]
    R.shuffle(items)
    return seed, {f'F{i:02d}': it for i, it in enumerate(items, 1)}


def ref_ok():
    bad = [v for v, h in REF27 if not os.path.exists(P(v)) or sha_file(v) != h]
    return bad


def q27_set(out, new):
    if ref_ok(): raise SystemExit(f'tập 1 tham chiếu không khớp SHA: {ref_ok()}')
    os.makedirs(out, exist_ok=True); seed, plan = plan27(new); img = {}
    for name, (_, v, t) in plan.items():
        f = os.path.join(out, name + '.jpg'); grab(v, t, f); img[name] = sha_file(f)
    render_prompts(out, 'Q27')
    json.dump(dict(rule='Q27', seed=seed, new=[dict(video=os.path.basename(v), sha256=sha_file(v)) for v in new], images=img,
                   prompts={r: prompt_sha(f'Q27-{r}.txt') for r in RATERS}, model=MODEL), open(os.path.join(out, 'manifest.json'), 'w'), indent=1)


def _replies(out, rule):
    bad, R = [], {}
    for r in RATERS:
        f = os.path.join(out, f'{r}.json')
        if not os.path.exists(f): bad.append(f'thiếu {r}.json'); continue
        try: x = json.load(open(f))
        except Exception as e: bad.append(f'{r}.json không đọc được ({e})'); continue
        if x.get('prompt_sha256') != prompt_sha(f'{rule}-{r}.txt'): bad.append(f'{r}: đề bài khác bản khoá (prompt_sha256)')
        if str(x.get('model', '')).lower().find(MODEL) < 0: bad.append(f"{r}: mô hình {x.get('model')!r}, cần {MODEL}")
        R[r] = x
    return R, bad


def q27_score(out, new):
    bad = ref_ok() and [f'tập 1 tham chiếu không khớp SHA']
    bad = list(bad or [])
    seed, plan = plan27(new); man = json.load(open(os.path.join(out, 'manifest.json')))
    if man.get('seed') != seed: bad.append('bộ ảnh không dựng từ đúng video mới (hạt giống khác)')
    with tempfile.TemporaryDirectory() as td:   # dựng lại ảnh, so SHA: không đổi ảnh được
        for name, (_, v, t) in plan.items():
            f = os.path.join(td, name + '.jpg'); grab(v, t, f)
            if sha_file(f) != man['images'].get(name) or not os.path.exists(os.path.join(out, name + '.jpg')) or sha_file(os.path.join(out, name + '.jpg')) != man['images'].get(name):
                bad.append(f'{name}.jpg khác ảnh dựng lại')
    R, b2 = _replies(out, 'Q27'); bad += b2
    return agg27({k: v[0] for k, v in plan.items()}, R, bad)


def agg27(sets, R, bad=()):
    """sets: {F##: 'new'|'ref'}; R: {R1: trả lời, …}. ĐẠT khi đủ 3 người chấm hợp lệ và trung bình tập mới ≥ tập 1"""
    bad = list(bad); per = {}
    for r, x in R.items():
        sc = x.get('scores') or {}; s = {'new': [], 'ref': []}
        for name, k in sets.items():
            c = sc.get(name) or {}
            vals = [c.get(q) for q in CRIT]
            if not all(isinstance(v, int) and 1 <= v <= 10 for v in vals): bad.append(f'{r} {name}: điểm thiếu hoặc ngoài 1–10'); continue
            s[k].append(sum(vals) / 3)
        if s['new'] and s['ref']: per[r] = (sum(s['new']) / len(s['new']), sum(s['ref']) / len(s['ref']))
    mn = sum(a for a, _ in per.values()) / len(per) if per else 0.0; mr = sum(b for _, b in per.values()) / len(per) if per else 0.0
    ok = not bad and len(per) == 3 and mn >= mr
    near = [f'tập mới {mn:.2f} so với tập 1 {mr:.2f}'] if per and abs(mn - mr) <= 0.05 * mr else []
    return dict(ok=ok, val=f"tập mới {mn:.2f} · tập 1 {mr:.2f} (" + ', '.join(f'{r} {a:.2f}/{b:.2f}' for r, (a, b) in per.items()) + ')',
                note='; '.join(bad[:6]), loi=bad, sat_nguong=near)


# ---------------------------------------------------------------- Q31
def _words(TL):
    sys.path.insert(0, REPO); from checks.ll import base
    W = []
    for s in TL['segments']:
        if s.get('vo_file'):
            al = json.load(open(P(s['vo_file'].replace('.mp3', '.align.json'))))
            W += [(s['t0'] + s['vo_offset'] + w[1], w[3]) for w in base.words(al)]
    return W


def _at(videos, t):
    for v in videos:
        d = dur(v)
        if t < d: return v, t
        t -= d
    return videos[-1], dur(videos[-1]) - 0.05


def plan31(TL):
    cuts = [b['t0'] for b in TL['segments'][1:]]
    strips = list(range(2, int(TL['tong_s']), STRIP_STEP))
    return cuts, strips


def _hist(out): return out.rstrip('/') + '-lich-su'


def _rounds(out):
    """các vòng đã chấm đủ 3 người của tập này (thư mục lịch sử cạnh thư mục bộ ảnh)"""
    h = _hist(out)
    if not os.path.isdir(h): return []
    return sorted(d for d in os.listdir(h) if re.fullmatch(r'vong-\d\d', d) and all(os.path.exists(os.path.join(h, d, f'{r}.json')) for r in RATERS))


def q31_set(out, videos, TL):
    if os.path.exists(os.path.join(out, 'manifest.json')):   # lần xem trước của tập này → lịch sử (vòng tính theo từng tập)
        h = _hist(out); os.makedirs(h, exist_ok=True); n = len([d for d in os.listdir(h) if d.startswith('vong-')]) + 1
        shutil.move(out, os.path.join(h, f'vong-{n:02d}'))
    vong = len(_rounds(out)) + 1
    os.makedirs(out, exist_ok=True); W = _words(TL); cuts, strips = plan31(TL); txt = []
    for k, c in enumerate(cuts, 1):
        names = []
        for j, dt in enumerate(WIN31):
            nm = os.path.join(out, f'_T{k:02d}_{j}.jpg'); v, lt = _at(videos, max(0.0, c + dt)); grab(v, lt, nm, 640); names.append(nm)
        subprocess.run(['ffmpeg', '-v', 'error', '-y'] + sum([['-i', x] for x in names], []) + ['-filter_complex', f'hstack={len(names)}', os.path.join(out, f'T{k:02d}.jpg')], check=True)
        for x in names: os.remove(x)
        said = ' '.join(w for t, w in W if c + WIN31[0] <= t <= c + WIN31[-1])
        txt.append(f'T{k:02d} (cut at {int(c // 60)}:{c % 60:04.1f}; frames at −2.5, −1.5, −0.5, +0.5, +1.5, +2.5 s): narration spoken within ±2.5 s of the cut: "{said}"')
    fr = []
    for i, t in enumerate(strips):
        nm = os.path.join(out, f'_S{i:03d}.jpg'); v, lt = _at(videos, t); grab(v, lt, nm, 320); fr.append(nm)
    blk = os.path.join(out, '_BLACK.jpg')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'color=black:s=320x180', '-frames:v', '1', blk], check=True)
    rows = [fr[i:i + STRIP_N] for i in range(0, len(fr), STRIP_N)]
    for i, row in enumerate(rows):
        row = row + [blk] * (STRIP_N - len(row))
        subprocess.run(['ffmpeg', '-v', 'error', '-y'] + sum([['-i', x] for x in row], []) + ['-filter_complex', f'hstack={STRIP_N}', os.path.join(out, f'R{i:02d}.jpg')], check=True)
    for x in fr + [blk]: os.remove(x)
    open(os.path.join(out, 'transitions.txt'), 'w').write('\n'.join(txt) + f'\n\nOverview strips R00…R{len(rows) - 1:02d}: one frame every 4 s from 0:02, 8 frames per strip, left to right, strips in order.\n')
    render_prompts(out, 'Q31')
    img = {f: sha_file(os.path.join(out, f)) for f in sorted(os.listdir(out)) if re.fullmatch(r'[TR]\d\d\.jpg|transitions\.txt', f)}
    json.dump(dict(rule='Q31', vong=vong, videos=[dict(video=os.path.basename(v), sha256=sha_file(v)) for v in videos], files=img,
                   prompts={r: prompt_sha(f'Q31-{r}.txt') for r in RATERS}, model=MODEL), open(os.path.join(out, 'manifest.json'), 'w'), indent=1)


def where_t(w, cuts):
    m = re.fullmatch(r'\s*T(\d+)\s*', str(w))
    if m and 1 <= int(m.group(1)) <= len(cuts): return cuts[int(m.group(1)) - 1], f'T{int(m.group(1)):02d}'
    m = re.fullmatch(r'\s*R(\d+)\.(\d)\s*', str(w))
    if m and 1 <= int(m.group(2)) <= STRIP_N: return 2 + STRIP_STEP * (STRIP_N * int(m.group(1)) + int(m.group(2)) - 1), None
    return None, None


def q31_score(out, videos, TL):
    bad = []; man = json.load(open(os.path.join(out, 'manifest.json'))); cuts, _ = plan31(TL)
    if [x['sha256'] for x in man.get('videos', [])] != [sha_file(v) for v in videos]: bad.append('bộ ảnh không dựng từ đúng video')
    for f, h in (man.get('files') or {}).items():
        if not os.path.exists(os.path.join(out, f)) or sha_file(os.path.join(out, f)) != h: bad.append(f'{f} khác manifest')
    if len([f for f in man.get('files') or {} if f.startswith('T')]) != len(cuts): bad.append('số dải chuyển đoạn khác timeline')
    vong = int(man.get('vong') or 0)
    if vong != len(_rounds(out)) + 1: bad.append(f'vòng {vong} khác lịch sử ({len(_rounds(out))} vòng đã chấm trong {os.path.basename(_hist(out))})')
    gt = json.load(open(os.path.join(out, 'giai-trinh.json'))) if os.path.exists(os.path.join(out, 'giai-trinh.json')) else {}
    R, b2 = _replies(out, 'Q31'); bad += b2
    return agg31(cuts, R, bad, vong=max(1, vong), giai_trinh=gt)


def agg31(cuts, R, bad=(), vong=1, giai_trinh=None):
    """cuts: giây các điểm chuyển đoạn (T01…); R: {R1: trả lời, …}; vong: vòng xem mù của tập (1, 2, …).
    Vòng 1: ĐẠT khi đủ 3 người hợp lệ và không điểm nào được ≥ 2 người khác nhau cùng nêu là đứt mạch.
    Từ vòng 2: chỉ chặn điểm 3/3; mỗi điểm 2/3 phải có giải trình (giai_trinh: {mốc: chữ}, mốc = T## hoặc m:ss.s của điểm) ≥ 20 ký tự."""
    bad = list(bad); items = []
    for r, x in R.items():
        if not str(x.get('question') or '').strip(): bad.append(f'{r}: thiếu câu trả lời "câu hỏi của phim"')
        if not (isinstance(x.get('score'), int) and 1 <= x['score'] <= 10): bad.append(f'{r}: score ngoài 1–10')
        for it in x.get('issues') or []:
            t, tag = where_t(it.get('where'), cuts)
            if t is None or it.get('kind') not in ('break', 'boring'): bad.append(f"{r}: vị trí/loại không đọc được {it.get('where')!r}/{it.get('kind')!r}"); continue
            items.append(dict(r=r, t=t, tag=tag, kind=it['kind'], where=it['where'], note=str(it.get('note', ''))[:120]))
    # gom điểm: cùng T## hoặc cách ≤ 4 s; điểm đồng thuận = ≥ 2 trong 3 người nêu
    items.sort(key=lambda z: z['t']); groups = []
    for it in items:
        g = next((g for g in groups if any((it['tag'] and it['tag'] == z['tag']) or abs(it['t'] - z['t']) <= NEAR31 for z in g)), None)
        (g.append(it) if g is not None else groups.append([it]))
    cons = [g for g in groups if len({z['r'] for z in g}) >= 2]
    brk = [g for g in cons if len({z['r'] for z in g if z['kind'] == 'break'}) >= 2]
    fmt = lambda g: f"{int(g[0]['t'] // 60)}:{g[0]['t'] % 60:04.1f} [{'/'.join(sorted({z['where'] for z in g}))}] " \
                    f"{len({z['r'] for z in g})}/3 {'/'.join(sorted({z['kind'] for z in g}))}: {next((z for z in g if z['kind'] == 'break'), g[0])['note']}"
    nb = lambda g: len({z['r'] for z in g if z['kind'] == 'break'})
    GT = {str(k).strip(): str(v).strip() for k, v in (giai_trinh or {}).items()}
    keys = lambda g: {z['tag'] for z in g if z['tag']} | {f"{int(g[0]['t'] // 60)}:{g[0]['t'] % 60:04.1f}"}
    if vong <= 1: block, need = brk, []
    else: block, need = [g for g in brk if nb(g) >= 3], [g for g in brk if nb(g) == 2]
    nogt = [g for g in need if not any(len(GT.get(k, '')) >= GT_MIN for k in keys(g))]
    ok = not bad and len(R) == 3 and not block and not nogt
    q = {r: x.get('question') for r, x in R.items()}
    return dict(ok=ok, val=f"vòng {vong} · điểm liền mạch {[R[r].get('score') for r in R]} · đồng thuận ≥ 2/3: {len(cons)} điểm, đứt mạch {len(brk)}"
                + (f" (3/3: {len(block)}, 2/3 có giải trình {len(need) - len(nogt)}/{len(need)})" if vong > 1 else ''),
                note='; '.join(bad[:4] + ['ĐỨT MẠCH ' + fmt(g) for g in block] + ['2/3 chưa giải trình ' + fmt(g) for g in nogt]
                               + ['2/3 đã giải trình ' + fmt(g) for g in need if g not in nogt] + ['chán ' + fmt(g) for g in cons if g not in brk]),
                loi=bad + ['đứt mạch ' + fmt(g) for g in block] + ['2/3 chưa giải trình ' + fmt(g) for g in nogt],
                dong_thuan=[fmt(g) for g in cons], cau_hoi=q, vong=vong)


if __name__ == '__main__':
    a = sys.argv[1:]; mode, out = a[0], os.path.abspath(a[1])

    def lst(flag):
        if flag not in a: return []
        i = a.index(flag) + 1; o = []
        while i < len(a) and not a[i].startswith('--'): o.append(a[i]); i += 1
        return o
    if out.startswith(REPO + os.sep) and mode.endswith('-set'): raise SystemExit('thư mục bộ ảnh phải nằm ngoài repo (subagent không được thấy repo)')
    if mode == 'q27-set': q27_set(out, lst('--new'))
    elif mode == 'q31-set': q31_set(out, lst('--video'), json.load(open(lst('--tl')[0])))
    else:
        r = q27_score(out, lst('--new')) if mode == 'q27-score' else q31_score(out, lst('--video'), json.load(open(lst('--tl')[0])))
        print(('Q27 ' if mode == 'q27-score' else 'Q31 ') + ('ĐẠT' if r['ok'] else 'TRƯỢT') + ' · ' + r['val'] + ('\n  ' + r['note'] if r['note'] else ''))
        sys.exit(0 if r['ok'] else 1)
