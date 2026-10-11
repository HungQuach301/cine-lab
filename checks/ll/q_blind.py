#!/opt/cine/bin/python
"""Q27 chấm hình mù · Q31 xem liền mạch mù · kiểm mù kịch bản G1 — luật khoá LL v3 (phiên K, 07/10/2026; sửa sau tập 7, 09/10/2026;
1.9.0, 11/10/2026: người chấm qua Claude API, Q27 chấm theo manifest). Định nghĩa: checks/ll/RULES-LL.md.

K CỐ ĐỊNH: đề bài (checks/ll/blind/Q27-R*.txt, Q31-R*.txt, khoá SHA cùng checks/), cách lấy và trộn mẫu, số người chấm (3), mô hình
(claude-sonnet-5-5 qua Claude API, judge.py), ngưỡng. P KHÔNG sửa đề bài: chỉ thay {DIR} bằng thư mục bộ ảnh; câu trả lời ghi lại SHA-256 của tệp đề bài.

  q_blind.py ref-fetch                                   tải master tập 1 1080p (đối chứng Q27) và tập 8 bản phát hành (mốc Q27, 1.9.1), kiểm SHA
  q_blind.py q27-set <thư mục> --new <master 1080p>      bộ 60 ảnh F01–F60 (30 bản cuối + 30 tập 1 1080p, trộn; Q-L27 = B) + đề bài đã điền
  q_blind.py q31-set <thư mục> --video <video…> --tl <timeline.json> [--tu-nhap <thư mục q31 của nháp>]
                                                         dải chuyển đoạn T## + dải tổng quan R## + transitions.txt
  q_blind.py q27-run|q31-run <thư mục>                   3 người chấm qua Claude API → R1–R3.json + `cham` trong manifest (fail closed);
                                                         q27-run chấm cả bộ mốc tập 8 <thư mục>-moc (1.9.1)
  q_blind.py g1-run <thư mục> --prompt <đề bài> [--n 3]  kiểm mù kịch bản G1 qua Claude API → R1..Rn.md + manifest
  q_blind.py q27-score <thư mục> --new <master 1080p> [--plan-sau <PLAN.md tập sau>]   chấm (R1–R3.json); mã thoát 0 = ĐẠT
  q_blind.py q31-score <thư mục> --video <video…> --tl <timeline.json>

Thư mục bộ ảnh phải nằm NGOÀI repo (ví dụ <out>/blind/q27): người chấm chỉ đọc được tệp trong thư mục đó.
Q27 không ghi tệp khoá giải mã: thứ tự trộn suy lại được từ SHA-256 của video mới (hạt giống), nên không có gì để lộ cho người chấm.
Q27 (1.9.0): q27-score gán khung theo hạt giống ghi trong manifest của lần chấm; video hiện tại khác SHA trong manifest → TRƯỢT
"bộ chấm thuộc bản khác" (số in ra là của bản trong manifest); đổi master sau Q27 phải chấm lại.
Q27 (1.9.1, ĐẶT LẠI MỐC): q27-set dựng kèm bộ tập 8 bản phát hành vs tập 1 ở <thư mục>-moc; q27-score báo tập mới − tập 1 (ngưỡng),
tập 8 − tập 1 và tập mới − tập 8; bộ mốc thiếu hoặc không hợp lệ → TRƯỢT.
Q27 (sau tập 7): chỉ chấm CHÍNH THỨC trên bản cuối 1920×1080 so với master tập 1 1920×1080; bản nháp không chấm. ĐẠT khi tập mới ≥ tập 1 − SE27;
chênh trong ±SE27 là SÁT NGƯỠNG và PLAN tập sau phải có mục "Cải thiện hình".
Q31 tính VÒNG theo từng tập (Q-L31, chủ dự án 07/10/2026): q31-set chuyển lần xem trước sang <thư mục>-lich-su/vong-NN; vòng 1 chặn
điểm đứt mạch ≥ 2/3; từ vòng 2 chỉ chặn điểm 3/3, điểm 2/3 phải có giải trình trong <thư mục>/giai-trinh.json (chép vào báo cáo G2).
Q31 (sau tập 7): sổ vòng nháp chỉ chuyển sang bản cuối khi bản cuối KHÔNG đổi lời/cấu trúc so với nháp cuối cùng đã chấm (dấu vân trong
manifest); đổi thì bản cuối đếm lại từ vòng 1. Sổ vòng (<thư mục>-lich-su/) không bao giờ bị xoá: manifest ghi SHA từng vòng, thiếu là TRƯỢT.
"""
import hashlib, json, os, random, re, shutil, subprocess, sys, tempfile, unicodedata

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'blind')
RATERS = ('R1', 'R2', 'R3')
sys.path.insert(0, REPO)
from checks.ll import judge  # noqa: E402  người chấm qua Claude API (1.9.0)
MODEL = judge.MODEL   # ghim: claude-sonnet-5-5 (1.9.0; trước đó subagent 'sonnet')
N27 = 30            # Q-L27 = B (chủ dự án 07/10/2026): 30 khung tập mới + 30 khung tập 1
# Tập 1 bản m23, MASTER 1080p (chủ dự án 09/10/2026: so 1080p với 1080p). Cùng SHA với master m23 (M2-3-MASTER-SHORTS.md) và với
# ll-ep01-v1-master-1080p.mp4 của nhánh release-ll-ep01-v1. Ngoài repo (853 MB, LFS): `q_blind.py ref-fetch`. (đường dẫn, SHA-256, thời lượng s)
REF27 = [('/var/tmp/cine-out/ref/ll-ep01-v1-master-1080p.mp4', '9c3825387345ec0af6c035ec3f94809644ca7767d1ecbafcaed4710480113942', 602.583333)]
REF27_URL = 'https://media.githubusercontent.com/media/HungQuach301/cine-lab/release-ll-ep01-v1/ll-ep01-v1-master-1080p.mp4'
# 1.9.1 (chủ dự án 11/10/2026, Q27 qua API = phương án A + ĐẶT LẠI MỐC): từ tập 9 mỗi lần chấm chính thức chấm KÈM tập 8 bản phát hành
# (release-ll-ep08-v1, master d22d7d6e…) so với tập 1 trên cùng đường API, ở thư mục <thư mục>-moc. Ngưỡng đạt vẫn tính trên tập mới − tập 1.
MOC27 = [('/var/tmp/cine-out/ref/ll-ep08-v1-master.mp4', 'd22d7d6e640dc6f0f0dfe0237cfd262f809e768eb78c59f0528f03f758c9c854', 607.958333)]
MOC27_URL = 'https://media.githubusercontent.com/media/HungQuach301/cine-lab/release-ll-ep08-v1/ll-ep08-v1-master.mp4'
SIZE27 = (1920, 1080)   # chỉ chấm chính thức bản cuối 1080p; bản nháp không chấm
# Sai số chuẩn của chênh lệch (tập mới − tập 1) trong MỘT lần chấm 30 + 30, đo trên dữ liệu thật đã có (6 lần chấm hợp lệ: tập 6 v1, v2;
# tập 7 nháp lần 2, 3, 4b, chính thức): bootstrap hai tầng (người chấm × khung), căn bậc hai trung bình bình phương = 0,273.
# Hàm se27() tính lại từ checks/ll/fixtures; selftest đối chiếu. Báo cáo: reports/checks-ll-v3/BAO-CAO.md mục 13.
SE27 = 0.27
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
def strat(L, n, R):
    """n thời điểm phân tầng đều trên tổng thời lượng dùng được (mỗi tầng một điểm ngẫu nhiên); L = [(video, thời lượng s)]"""
    tot = sum(d - 2 * EDGE for _, d in L); out = []
    for k in range(n):
        x = (k + R.random()) / n * tot
        for v, d in L:
            if x < d - 2 * EDGE: out.append((v, round(EDGE + x, 3))); break
            x -= d - 2 * EDGE
    return out


def plan27(new):
    seed = hashlib.sha256(''.join(sha_file(v) for v in new).encode()).hexdigest()
    R = random.Random(int(seed[:16], 16))
    items = [('new', v, t) for v, t in strat([(v, dur(v)) for v in new], N27, R)] + [('ref', v, t) for v, t in strat([(v, d) for v, _, d in REF27], N27, R)]
    R.shuffle(items)
    return seed, {f'F{i:02d}': it for i, it in enumerate(items, 1)}


def sets_from_seed(seed):
    """{F##: 'new'|'ref'} suy lại từ hạt giống (strat rút đúng N27 + N27 số ngẫu nhiên trước khi trộn): dùng cho dữ liệu chấm đã lưu"""
    R = random.Random(int(seed[:16], 16))
    for _ in range(2 * N27): R.random()
    items = ['new'] * N27 + ['ref'] * N27; R.shuffle(items)
    return {f'F{i:02d}': k for i, k in enumerate(items, 1)}


def size(v):
    w, h = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', P(v)],
                          capture_output=True, text=True, check=True).stdout.strip().split(',')[:2]
    return int(w), int(h)


def ref_ok(L=None):
    bad = [v for v, h, _ in (REF27 if L is None else L) if not os.path.exists(P(v)) or sha_file(v) != h]
    return bad


def moc_dir(out): return out.rstrip('/') + '-moc'


def ref_fetch():
    for L, url in ((REF27, REF27_URL), (MOC27, MOC27_URL)):
        v, h, _ = L[0]
        if not ref_ok(L): print(f'đã có {v} (SHA khớp)'); continue
        os.makedirs(os.path.dirname(v), exist_ok=True)
        subprocess.run(['curl', '-sSL', '--fail', '-o', v + '.tai', url], check=True); os.replace(v + '.tai', v)
        if ref_ok(L): raise SystemExit(f'{v}: SHA khác {h}')
        print(f'{v}: SHA khớp')


def draft27(new):
    """bản nháp (khác 1920×1080) không chấm Q27"""
    return [f'{os.path.basename(v)} {w}×{h}' for v in new for w, h in [size(v)] if (w, h) != SIZE27]


def _set27(out, new, moc=False):
    os.makedirs(out, exist_ok=True); seed, plan = plan27(new); img = {}
    for name, (_, v, t) in plan.items():
        f = os.path.join(out, name + '.jpg'); grab(v, t, f); img[name] = sha_file(f)
    render_prompts(out, 'Q27')
    json.dump(dict(rule='Q27', moc=moc, seed=seed, new=[dict(video=os.path.basename(v), sha256=sha_file(v), size=list(size(v))) for v in new],
                   ref=[dict(video=os.path.basename(v), sha256=h) for v, h, _ in REF27], images=img,
                   prompts={r: prompt_sha(f'Q27-{r}.txt') for r in RATERS}, model=MODEL), open(os.path.join(out, 'manifest.json'), 'w'), indent=1)


def need_moc(new): return [sha_file(v) for v in new] != [h for _, h, _ in MOC27]


def q27_set(out, new):
    """bộ chính thức (tập mới vs tập 1) và, từ 1.9.1, bộ MỐC (tập 8 bản phát hành vs tập 1) ở <thư mục>-moc"""
    if ref_ok(): raise SystemExit(f'tập 1 1080p tham chiếu thiếu hoặc không khớp SHA: {ref_ok()} — chạy `q_blind.py ref-fetch`')
    if draft27(new): raise SystemExit(f'Q27 chỉ chấm chính thức bản cuối 1920×1080; bản nháp không chấm: {draft27(new)}')
    mo = need_moc(new)
    if mo and ref_ok(MOC27): raise SystemExit(f'tập 8 bản phát hành (mốc Q27) thiếu hoặc không khớp SHA: {ref_ok(MOC27)} — chạy `q_blind.py ref-fetch`')
    if mo and os.path.exists(os.path.join(moc_dir(out), 'manifest.json')): raise SystemExit(f'{moc_dir(out)} đã có bộ mốc: dùng thư mục mới cho lần chấm mới')
    _set27(out, new)
    if mo: _set27(moc_dir(out), [v for v, _, _ in MOC27], moc=True)


def _replies(out, rule):
    """R1–R3.json của một bộ chấm. 1.9.0: mỗi trả lời phải do judge.py ghi (backend 'api', mô hình MODEL), khớp SHA với bản ghi lần chấm
    trong manifest (`cham`), và mọi lần gọi của người đó chỉ chạy MODEL. Lỗi API/hết credit ghi trong manifest → TRƯỢT kèm lý do."""
    bad, R = [], {}
    ch = _man(out).get('cham') or {}
    if not ch: bad.append('chưa chấm qua Claude API (manifest không có bản ghi `cham`; chạy q_blind.py ' + rule.lower() + '-run)')
    for e in ch.get('loi') or []: bad.append(f'lần chấm: {e}')
    for r in RATERS:
        f = os.path.join(out, f'{r}.json'); rec = (ch.get('raters') or {}).get(r) or {}
        for t in rec.get('tries') or []:
            if t.get('loi') and rec.get('ok') is False: bad.append(f"{r} lần {t['lan']}: {'; '.join(t['loi'])}")
        if not os.path.exists(f): bad.append(f'thiếu {r}.json'); continue
        try: x = json.load(open(f))
        except Exception as e: bad.append(f'{r}.json không đọc được ({e})'); continue
        if x.get('prompt_sha256') != prompt_sha(f'{rule}-{r}.txt'): bad.append(f'{r}: đề bài khác bản khoá (prompt_sha256)')
        if x.get('model') != MODEL or x.get('backend') != 'api': bad.append(f"{r}: mô hình/đường chấm {x.get('model')!r}/{x.get('backend')!r}, cần {MODEL!r}/'api'")
        if ch and (not rec.get('ok') or rec.get('reply_sha256') != sha_file(f)): bad.append(f'{r}.json khác bản ghi lần chấm trong manifest')
        for t in rec.get('tries') or []:
            if judge.model_errors(t.get('model_usage')) and rec.get('ok'): bad.append(f"{r} lần {t['lan']}: {'; '.join(judge.model_errors(t.get('model_usage')))}")
        R[r] = x
    return R, bad


def blind_run(out, rule):
    """chấm một bộ (Q27/Q31) bằng 3 người chấm qua Claude API (judge.py). Mỗi bộ chấm MỘT lần: đã có trả lời hoặc bản ghi thì từ chối
    (muốn chấm lại: dựng bộ mới bằng q27-set/q31-set). Ghi R1–R3.json + `cham` trong manifest (mô hình thực chạy, chi phí, lỗi)."""
    mf = os.path.join(out, 'manifest.json'); man = json.load(open(mf))
    if man.get('rule') != rule: raise SystemExit(f"manifest là của {man.get('rule')}, không phải {rule}")
    if man.get('cham') or any(os.path.exists(os.path.join(out, f'{r}.json')) for r in RATERS):
        raise SystemExit('bộ này đã chấm (có R*.json hoặc bản ghi `cham`): mỗi bộ chỉ chấm một lần; dựng bộ mới để chấm lại')
    need = [os.path.join(out, n + '.jpg') for n in sorted(man['images'])] if rule == 'Q27' else \
           [os.path.join(out, f) for f in sorted(man['files'])]
    P_ = {}
    for r in RATERS:
        want = open(os.path.join(HERE, f'{rule}-{r}.txt'), encoding='utf-8').read().replace('{DIR}', out)
        got = open(os.path.join(out, f'PROMPT-{r}.txt'), encoding='utf-8').read()
        if got != want: raise SystemExit(f'PROMPT-{r}.txt khác đề bài khoá đã điền')
        P_[r] = want
    ch = dict(backend='api', model=MODEL, cli=judge.cli_version(), bat_dau=judge.now(), loi=[], raters={})
    def save():
        ch['cost_usd'] = round(sum(t.get('cost_usd') or 0 for x in ch['raters'].values() for t in x['tries']) + ((ch.get('probe') or {}).get('cost_usd') or 0), 4)
        man['cham'] = ch; json.dump(man, open(mf, 'w'), indent=1, ensure_ascii=False)
    try: ch['probe'] = judge.probe()
    except judge.JudgeError as e:
        ch['loi'].append(str(e)); ch['xong'] = judge.now(); save(); raise SystemExit(f'{rule}: DỪNG — {e}')
    for r in RATERS:
        rep_, tries = judge.run_rater(rule, r, P_[r], out, need)
        rec = dict(ok=rep_ is not None, tries=tries)
        if rep_ is not None:
            rep_.update(prompt_sha256=prompt_sha(f'{rule}-{r}.txt'), model=MODEL, backend='api')
            f = os.path.join(out, f'{r}.json'); json.dump(rep_, open(f, 'w'), indent=1, ensure_ascii=False); rec['reply_sha256'] = sha_file(f)
        else: ch['loi'].append(f"{r}: {'; '.join(tries[-1]['loi'])}")
        ch['raters'][r] = rec; save()
    ch['xong'] = judge.now(); save()
    print(f"{rule}: {sum(x['ok'] for x in ch['raters'].values())}/3 người chấm hợp lệ · chi phí ${ch['cost_usd']:.4f}"
          + ('' if not ch['loi'] else ' · LỖI: ' + '; '.join(ch['loi'])))
    if ch['loi']: raise SystemExit(2)


def g1_run(out, prompt_file, n=3):
    """kiểm mù kịch bản G1 qua Claude API: n người chấm độc lập, cùng đề bài của P (nguyên văn, ghi SHA), chỉ đọc tệp trong <out>
    (ngoài repo, P chép lời vào đó). Ghi R1..Rn.md + manifest (mô hình, chi phí). Fail closed như Q27/Q31."""
    os.makedirs(out, exist_ok=True); prompt = open(prompt_file, encoding='utf-8').read(); mf = os.path.join(out, 'manifest.json')
    if os.path.exists(mf): raise SystemExit(f'{out} đã chấm (có manifest.json): mỗi bộ chỉ chấm một lần; dùng thư mục mới')
    need = judge._need_reads(prompt, out)
    if not need: raise SystemExit(f'đề bài phải nêu đường dẫn tuyệt đối tệp cần đọc trong {out}')
    for f in need:
        if not os.path.exists(f): raise SystemExit(f'đề bài nêu {f} nhưng tệp không có')
    man = dict(rule='G1', prompt_file=os.path.abspath(prompt_file), prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),
               files={os.path.basename(f): sha_file(f) for f in need}, n=n)
    ch = dict(backend='api', model=MODEL, cli=judge.cli_version(), bat_dau=judge.now(), loi=[], raters={})
    def save():
        ch['cost_usd'] = round(sum(t.get('cost_usd') or 0 for x in ch['raters'].values() for t in x['tries']) + ((ch.get('probe') or {}).get('cost_usd') or 0), 4)
        man['cham'] = ch; json.dump(man, open(mf, 'w'), indent=1, ensure_ascii=False)
    try: ch['probe'] = judge.probe()
    except judge.JudgeError as e:
        ch['loi'].append(str(e)); ch['xong'] = judge.now(); save(); raise SystemExit(f'G1: DỪNG — {e}')
    for k in range(1, n + 1):
        r = f'R{k}'; txt, tries = judge.run_rater('G1', r, prompt, out, need, parse=False); rec = dict(ok=txt is not None, tries=tries)
        if txt is not None:
            f = os.path.join(out, f'{r}.md'); open(f, 'w', encoding='utf-8').write(txt.strip() + '\n'); rec['reply_sha256'] = sha_file(f)
        else: ch['loi'].append(f"{r}: {'; '.join(tries[-1]['loi'])}")
        ch['raters'][r] = rec; save()
    ch['xong'] = judge.now(); save()
    print(f"G1: {sum(x['ok'] for x in ch['raters'].values())}/{n} người chấm hợp lệ · chi phí ${ch['cost_usd']:.4f}" + ('' if not ch['loi'] else ' · LỖI: ' + '; '.join(ch['loi'])))
    if ch['loi']: raise SystemExit(2)


def seed_of(shas): return hashlib.sha256(''.join(shas).encode()).hexdigest()


def q27_sets(man, cur):
    """phép gán F## ↔ new/ref của MỘT lần chấm, lấy từ manifest của lần chấm đó (hạt giống ghi lúc q27-set), KHÔNG từ video hiện có
    (khiếu nại P 10/10/2026: chấm lại theo SHA master mới gán sai khung, in +0,06 thay vì −0,31). cur = SHA video mới đang có.
    Trả về (sets, lỗi, cùng_bản)."""
    bad, ms = [], [x.get('sha256') for x in man.get('new') or []]
    seed = man.get('seed') or ''
    if not ms or seed != seed_of(ms): bad.append('manifest hỏng: hạt giống không khớp SHA video ghi trong manifest')
    same = list(cur) == ms
    if not same:
        bad.append(f"bộ chấm thuộc bản khác: manifest {', '.join(x[:12] + '…' for x in ms)}, video hiện tại {', '.join(x[:12] + '…' for x in cur)}. "
                   'Số dưới đây là của bản trong manifest (gán khung theo hạt giống của lần chấm); master đổi sau Q27 phải chấm lại (q27-set + q27-run)')
    return sets_from_seed(seed) if re.fullmatch(r'[0-9a-f]{64}', seed) else {}, bad, same


def _check27(out, new_sha, new=None):
    """bộ Q27 ở out hợp lệ không: (phép gán, lỗi). new = video để dựng lại ảnh (chỉ khi cùng bản với manifest)"""
    bad = []
    man = json.load(open(os.path.join(out, 'manifest.json')))
    sets, b1, same = q27_sets(man, new_sha); bad += b1
    if [x.get('sha256') for x in man.get('ref') or []] != [h for _, h, _ in REF27]: bad.append('bộ ảnh không dựng với tập 1 1080p (bản luật trước 1.8: tập 1 720p) — dựng lại bằng q27-set')
    for name in sorted(man.get('images') or {}):
        f = os.path.join(out, name + '.jpg')
        if not os.path.exists(f) or sha_file(f) != man['images'][name]: bad.append(f'{name}.jpg khác manifest')
    if same and new:   # cùng bản: dựng lại ảnh từ video, so SHA (không đổi ảnh được)
        _, plan = plan27(new)
        if {k: v[0] for k, v in plan.items()} != sets: bad.append('phép gán khung dựng lại từ video khác phép gán theo hạt giống')
        with tempfile.TemporaryDirectory() as td:
            for name, (_, v, t) in plan.items():
                f = os.path.join(td, name + '.jpg'); grab(v, t, f)
                if sha_file(f) != man['images'].get(name): bad.append(f'{name}.jpg khác ảnh dựng lại')
    return sets, bad


def moc27(out, video=True):
    """bộ mốc tập 8 (<thư mục>-moc): dict(chenh, val, loi). loi = lỗi hợp lệ của bộ (không tính ngưỡng: mốc chỉ để báo)"""
    if not os.path.exists(os.path.join(out, 'manifest.json')):
        return dict(chenh=None, val='không có', loi=[f'thiếu bộ mốc tập 8 ({os.path.basename(out)}): dựng bằng q27-set, chấm bằng q27-run'])
    vids = [v for v, _, _ in MOC27]
    sets, bad = _check27(out, [h for _, h, _ in MOC27], vids if video and not ref_ok(MOC27) else None)
    if video and ref_ok(MOC27): bad.append('tập 8 bản phát hành thiếu hoặc không khớp SHA (q_blind.py ref-fetch)')
    R, b2 = _replies(out, 'Q27'); r = agg27(sets, R, bad + b2)
    loi = [e for e in r['loi'] if not e.startswith(('tập mới kém tập 1', 'SÁT NGƯỠNG'))]
    if len([1 for x in R if x]) < 3 and not loi: loi.append('bộ mốc chưa đủ 3 người chấm')
    return dict(chenh=r['chenh'], val=r['val'].split(' (SE')[0].replace('tập mới', 'tập 8'), loi=loi)


def them_moc(r, m):
    """gắn kết quả mốc tập 8 vào kết quả Q27: báo cả hai chênh và hiệu; ngưỡng vẫn trên tập mới − tập 1; bộ mốc lỗi → TRƯỢT"""
    r = dict(r); r['chenh_moc'] = m['chenh']; r['hieu_moc'] = None if m['chenh'] is None else round(r['chenh'] - m['chenh'], 6)
    if m['loi']:
        r['loi'] = r['loi'] + ['mốc tập 8: ' + e for e in m['loi']]; r['ok'] = False
        r['note'] = '; '.join(x for x in [r['note'], 'mốc tập 8: ' + '; '.join(m['loi'][:3])] if x)
    r['val'] += (f" · mốc: {m['val']} · tập mới − tập 8 {r['hieu_moc']:+.2f}" if r['hieu_moc'] is not None else ' · mốc tập 8: không có')
    return r


def q27_score(out, new, plan_sau=None):
    bad = ref_ok() and ['tập 1 1080p tham chiếu thiếu hoặc không khớp SHA (q_blind.py ref-fetch)']
    bad = list(bad or [])
    if draft27(new): bad.append(f'bản nháp không chấm (chỉ bản cuối 1920×1080): {draft27(new)}')
    sets, b1 = _check27(out, [sha_file(v) for v in new], new); bad += b1
    R, b2 = _replies(out, 'Q27'); bad += b2
    r = agg27(sets, R, bad, plan_sau=plan_sau)
    return them_moc(r, moc27(moc_dir(out))) if need_moc(new) else r


def muc_cai_thien_hinh(path):
    """PLAN tập sau có mục (tiêu đề markdown) chứa "cải thiện hình" với nội dung ≥ 40 ký tự; trả về lỗi hoặc None"""
    if not path or not os.path.exists(P(path)): return f'không có PLAN tập sau ({path})'
    L = unicodedata.normalize('NFC', open(P(path), encoding='utf-8').read()).split('\n')
    for i, ln in enumerate(L):
        m = re.match(r'(#{1,6})\s', ln)
        if m and 'cải thiện hình' in ln.lower():
            body = []
            for x in L[i + 1:]:
                n = re.match(r'(#{1,6})\s', x)
                if n and len(n.group(1)) <= len(m.group(1)): break
                body.append(x)
            if len(re.sub(r'\s', '', ''.join(body))) >= 40: return None
            return f'mục "{ln.strip()}" trong {os.path.basename(path)} chưa có nội dung (≥ 40 ký tự)'
    return f'{path}: thiếu mục "Cải thiện hình"'


def agg27(sets, R, bad=(), plan_sau=None):
    """sets: {F##: 'new'|'ref'}; R: {R1: trả lời, …}. ĐẠT khi đủ 3 người chấm hợp lệ và trung bình tập mới ≥ tập 1 − SE27.
    Chênh trong ±SE27: SÁT NGƯỠNG, và PLAN tập sau (plan_sau) phải có mục "Cải thiện hình" (không có thì TRƯỢT)."""
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
    d = round(mn - mr, 6); sat = bool(per) and abs(d) <= SE27
    if per and d < -SE27: bad.append(f'tập mới kém tập 1 quá sai số: chênh {d:+.2f} < −{SE27}')
    if sat and not bad:
        e = muc_cai_thien_hinh(plan_sau)
        if e: bad.append(f'SÁT NGƯỠNG (chênh {d:+.2f} trong ±{SE27}) nhưng {e}')
    ok = not bad and len(per) == 3
    near = [f'SÁT NGƯỠNG: chênh {d:+.2f} trong ±SE {SE27} (tập mới {mn:.2f}, tập 1 {mr:.2f}); PLAN tập sau phải có mục "Cải thiện hình"'] if sat else []
    return dict(ok=ok, val=f"tập mới {mn:.2f} · tập 1 {mr:.2f} · chênh {d:+.2f} (SE {SE27}){' · SÁT NGƯỠNG' if sat else ''} ("
                + ', '.join(f'{r} {a:.2f}/{b:.2f}' for r, (a, b) in per.items()) + ')',
                note='; '.join(bad[:6]), loi=bad, sat_nguong=near, chenh=d, sat=sat)


def se27(runs, B=4000, seed=27):
    """SE của chênh lệch trong một lần chấm, đo trên dữ liệu thật: runs = [(sets, replies)]. Mỗi lần: bootstrap hai tầng
    (lấy lại 3 người chấm có hoàn lại × lấy lại khung trong từng bộ), lấy độ lệch chuẩn của chênh; gộp các lần bằng căn trung bình bình phương."""
    import statistics as st
    G = random.Random(seed); out = []
    for sets, R in runs:
        rs = sorted(R); g = {k: [f for f in sorted(sets) if sets[f] == k] for k in ('new', 'ref')}
        sc = {r: {f: sum(R[r]['scores'][f][c] for c in CRIT) / 3 for f in sets} for r in rs}; ds = []
        for _ in range(B):
            rr = [G.choice(rs) for _ in rs]; m = {}
            for k in g:
                fs = [G.choice(g[k]) for _ in g[k]]; m[k] = sum(sc[r][f] for r in rr for f in fs) / (len(rr) * len(fs))
            ds.append(m['new'] - m['ref'])
        out.append(st.stdev(ds))
    return (sum(x * x for x in out) / len(out)) ** 0.5, out


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


def dau_van(TL):
    """dấu vân LỜI (chữ lời từng đoạn, theo căn chữ) và CẤU TRÚC (thứ tự đoạn; mỗi đoạn: chuỗi shot theo mẫu, cảnh đinh/khoá, ảnh tư liệu,
    kiểu vào). Không tính thời điểm và nội dung vẽ trong cảnh đinh: sửa ánh sáng/chi tiết nội thất không đổi dấu vân."""
    loi, ct = [], []
    for s in TL['segments']:
        t = None
        if s.get('vo_file'):
            f = P(s['vo_file'].replace('.mp3', '.align.json'))
            t = ''.join(json.load(open(f))['characters']) if os.path.exists(f) else None
            if t is None: return None
        loi.append([s['id'], t])
        sh = []
        for x in s['shots']:
            p = x.get('p') or {}; i = x.get('in')
            sh.append([x['tpl'], p.get('hero'), (p.get('left') or {}).get('hero'), (p.get('right') or {}).get('hero'), p.get('rid'),
                       (i or {}).get('type') if isinstance(i, dict) else i])
        ct.append([s['id'], s.get('part'), sh])
    H = lambda x: hashlib.sha256(json.dumps(x, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    return dict(loi=H(loi), cau_truc=H(ct))


def _final(m): return tuple(m.get('size') or ()) == SIZE27


def _man(d):
    f = os.path.join(d, 'manifest.json')
    try: return json.load(open(f))
    except Exception: return {}


def vong31(hist_mans, cur):
    """Đếm vòng của bộ hiện tại: hist_mans = manifest các vòng đã chấm đủ 3 người (theo thứ tự). Vòng tính theo tập, NHƯNG khi chuyển
    từ nháp sang bản cuối (1920×1080), sổ vòng nháp chỉ được chuyển nếu bản cuối có cùng dấu vân lời VÀ cấu trúc với nháp cuối cùng đã
    chấm; khác (hoặc thiếu dấu vân) thì bản cuối đếm lại từ vòng 1. Trả về (vòng, ghi chú)."""
    n, prev, note = 0, None, []
    for i, m in enumerate(list(hist_mans) + [cur]):
        if prev is not None and _final(m) and not _final(prev):
            a, b = prev.get('dau_van') or {}, m.get('dau_van') or {}
            if not a or not b or a.get('loi') != b.get('loi') or a.get('cau_truc') != b.get('cau_truc'):
                why = 'nháp thiếu dấu vân' if not a or not b else '/'.join(k for k, w in (('lời', 'loi'), ('cấu trúc', 'cau_truc')) if a.get(w) != b.get(w)) + ' khác'
                note.append(f'bản cuối đếm lại từ vòng 1 ({why} so với nháp cuối đã chấm, vòng {n})'); n = 0
            else: note.append(f'sổ {n} vòng nháp chuyển sang bản cuối (cùng lời, cùng cấu trúc)')
        n += 1; prev = m
    return n, note


def _import_nhap(out, src):
    """chép (KHÔNG chuyển, KHÔNG xoá) sổ vòng của thư mục nháp sang sổ vòng bản cuối: các vòng của <src>-lich-su rồi bộ hiện tại của src"""
    h = _hist(out); os.makedirs(h, exist_ok=True)
    have = {sha_file(os.path.join(h, d, 'manifest.json')) for d in os.listdir(h) if os.path.exists(os.path.join(h, d, 'manifest.json'))}
    sh = _hist(src); srcs = [os.path.join(sh, d) for d in sorted(os.listdir(sh)) if re.fullmatch(r'vong-\d\d', d)] if os.path.isdir(sh) else []
    if os.path.exists(os.path.join(src, 'manifest.json')): srcs.append(src)
    for d in srcs:
        mf = os.path.join(d, 'manifest.json')
        if os.path.exists(mf) and sha_file(mf) in have: continue
        n = len([x for x in os.listdir(h) if x.startswith('vong-')]) + 1
        shutil.copytree(d, os.path.join(h, f'vong-{n:02d}'))
        open(os.path.join(h, f'vong-{n:02d}', 'NGUON.txt'), 'w').write(f'chép từ {os.path.abspath(d)}\n')


def _ledger(out):
    """SHA manifest của mọi vòng trong sổ (kể cả vòng chấm dở): ghi vào manifest để phát hiện sổ bị xoá/sửa"""
    h = _hist(out)
    if not os.path.isdir(h): return []
    return [dict(dir=d, manifest_sha256=sha_file(os.path.join(h, d, 'manifest.json')) if os.path.exists(os.path.join(h, d, 'manifest.json')) else None)
            for d in sorted(os.listdir(h)) if re.fullmatch(r'vong-\d\d', d)]


def ledger_errors(out, man):
    """sổ vòng không bao giờ bị xoá: mọi vòng ghi trong manifest lúc dựng bộ phải còn nguyên (thư mục và SHA manifest)"""
    h, bad = _hist(out), []
    for e in man.get('lich_su') or []:
        f = os.path.join(h, e['dir'], 'manifest.json')
        if not os.path.isdir(os.path.join(h, e['dir'])) or (e.get('manifest_sha256') and (not os.path.exists(f) or sha_file(f) != e['manifest_sha256'])):
            bad.append(f"sổ vòng thiếu hoặc bị sửa: {os.path.basename(h)}/{e['dir']} (không bao giờ xoá {os.path.basename(h)}/)")
    return bad


def q31_set(out, videos, TL, tu_nhap=None):
    if tu_nhap: _import_nhap(out, os.path.abspath(tu_nhap))
    if os.path.exists(os.path.join(out, 'manifest.json')):   # lần xem trước của tập này → lịch sử (vòng tính theo từng tập)
        h = _hist(out); os.makedirs(h, exist_ok=True); n = len([d for d in os.listdir(h) if d.startswith('vong-')]) + 1
        shutil.move(out, os.path.join(h, f'vong-{n:02d}'))
    cur = dict(size=list(size(videos[0])), dau_van=dau_van(TL))
    vong, vnote = vong31([_man(os.path.join(_hist(out), d)) for d in _rounds(out)], cur)
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
    json.dump(dict(rule='Q31', vong=vong, vong_ghi_chu=vnote, size=cur['size'], dau_van=cur['dau_van'], lich_su=_ledger(out),
                   videos=[dict(video=os.path.basename(v), sha256=sha_file(v)) for v in videos], files=img,
                   prompts={r: prompt_sha(f'Q31-{r}.txt') for r in RATERS}, model=MODEL), open(os.path.join(out, 'manifest.json'), 'w'), indent=1)
    print(f'Q31 vòng {vong}' + (' · ' + '; '.join(vnote) if vnote else ''))


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
    h = _hist(out); bad += ledger_errors(out, man)
    if man.get('dau_van') != dau_van(TL): bad.append('dấu vân lời/cấu trúc của timeline khác manifest (bộ xem dựng từ timeline khác)')
    if tuple(man.get('size') or ()) != size(videos[0]): bad.append('cỡ khung video khác manifest')
    vong, _ = vong31([_man(os.path.join(h, d)) for d in _rounds(out)], man)
    if int(man.get('vong') or 0) != vong: bad.append(f"vòng {man.get('vong')} khác sổ vòng (tính lại: vòng {vong}, {len(_rounds(out))} vòng đã chấm trong {os.path.basename(h)})")
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
    a = sys.argv[1:]
    if a[0] == 'ref-fetch': ref_fetch(); sys.exit(0)
    mode, out = a[0], os.path.abspath(a[1])

    def lst(flag):
        if flag not in a: return []
        i = a.index(flag) + 1; o = []
        while i < len(a) and not a[i].startswith('--'): o.append(a[i]); i += 1
        return o
    if out.startswith(REPO + os.sep) and (mode.endswith('-set') or mode.endswith('-run')): raise SystemExit('thư mục bộ ảnh phải nằm ngoài repo (người chấm không được thấy repo)')
    if mode == 'q27-run':
        todo = [d for d in (out, moc_dir(out)) if os.path.exists(os.path.join(d, 'manifest.json')) and not _man(d).get('cham')]   # 1.9.1: kèm bộ mốc tập 8
        if not todo: raise SystemExit('bộ chính thức và bộ mốc đều đã chấm: dựng bộ mới để chấm lại')
        for d in todo: blind_run(d, 'Q27')
        sys.exit(0)
    if mode == 'q31-run': blind_run(out, 'Q31'); sys.exit(0)
    if mode == 'g1-run': g1_run(out, lst('--prompt')[0], int((lst('--n') or [3])[0])); sys.exit(0)
    if mode == 'q27-set': q27_set(out, lst('--new'))
    elif mode == 'q31-set': q31_set(out, lst('--video'), json.load(open(lst('--tl')[0])), tu_nhap=(lst('--tu-nhap') or [None])[0])
    else:
        r = q27_score(out, lst('--new'), plan_sau=(lst('--plan-sau') or [None])[0]) if mode == 'q27-score' else q31_score(out, lst('--video'), json.load(open(lst('--tl')[0])))
        print(('Q27 ' if mode == 'q27-score' else 'Q31 ') + ('ĐẠT' if r['ok'] else 'TRƯỢT') + ' · ' + r['val'] + ('\n  ' + r['note'] if r['note'] else ''))
        sys.exit(0 if r['ok'] else 1)
