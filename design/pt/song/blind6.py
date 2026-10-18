#!/opt/cine/bin/python
"""V6 · CHẤM MÙ khung neo (giao thức blind4.py PT4): `claude -p` GHIM claude-sonnet-5-5, chỉ công cụ Read, thư mục tạm chỉ có X.jpg/Y.jpg (không chữ),
3 vai nguyên văn channel-k2/k2v2-mau/blind_v2.py, nhãn bản ẨN, thứ tự X/Y theo hạt giống 20261018, đề bài nguyên văn PT4 (craft/detail/period/ai_look/toy_like).
Hai bộ khai TRƯỚC: (1) 'pt4-sx'  = 6 khung ngày PT4 LAI (reports/pt4/khung/*-LAI-notext.jpg) vs V6 SẢN XUẤT cùng khung neo × giờ;
                   (2) 'tn-sx'   = 2 khung trưa V6 TỐT NHẤT (người 3D, Cycles cao) vs V6 SẢN XUẤT.
Hai bản qua CÙNG bước ffmpeg 1280 px q3. KHÔNG khung đối thủ. KHÔNG dùng để kiểm dữ kiện. Sổ chi phí <OUT>/cost.jsonl (usd thật = total_cost_usd);
mốc theo dõi phần phiên con ≤ ~$2 → dừng trước lệnh khi tổng sổ ≥ $1,9.
  blind6.py set <bộ> <thư mục V6 sx> [<thư mục V6 tốt nhất>] · run <bộ> · score <bộ>      (V6_VONG=v1|v2 → thư mục con)"""
import importlib.util, json, os, random, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SHARED = '/home/user/cine-lab'
BASE = os.path.join(REPO, 'reports', 'v6', 'khung-neo', 'kiem-mu'); VONG = os.environ.get('V6_VONG', 'v1')
spec = importlib.util.spec_from_file_location('bv2', os.path.join(SHARED, 'channel-k2', 'k2v2-mau', 'blind_v2.py')); BV2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(BV2)
RATERS, MODEL = BV2.RATERS, BV2.MODEL; assert MODEL == 'claude-sonnet-5-5'
STOP = float(os.environ.get("V6_STOP", "1.9"))
bp = importlib.util.spec_from_file_location('b4', os.path.join(HERE, 'blind4.py'))
PROMPT = open(os.path.join(HERE, 'blind4.py')).read().split('PROMPT = """', 1)[1].split('"""', 1)[0]   # đề bài nguyên văn PT4
YEAR = {'1782': 'a narrow lane in the town of Gibraltar in September 1782, during the Great Siege', '1943': 'Commercial Square by Main Street, Gibraltar, in September 1943'}
BO = {'pt4-sx': ([f'{e}-{t}' for t in ('trua', 'sang', 'chieu') for e in (1782, 1943)], ('PT4', 'V6sx')),
      'tn-sx': ([f'{e}-trua' for e in (1782, 1943)], ('V6tn', 'V6sx'))}
def out(bo): return os.path.join(BASE, VONG, bo)
def spent():
    t = 0.0
    for root, _, fs in os.walk(BASE):
        if 'cost.jsonl' in fs: t += sum(json.loads(l)['usd'] for l in open(os.path.join(root, 'cost.jsonl')))
    return t
def setup(bo, sx, tn=None):
    FR, (b1, b2) = BO[bo]; O = out(bo); os.makedirs(O, exist_ok=True); R = random.Random(20261018); key = {}
    src = {'PT4': lambda f: os.path.join(SHARED, 'reports', 'pt4', 'khung', f'{f}-LAI-notext.jpg'), 'V6sx': lambda f: os.path.join(sx, f'{f}-LAI-notext.png'),
           'V6tn': lambda f: os.path.join(tn, f'{f}-LAI-notext.png')}
    for f in FR:
        swap = R.random() < 0.5; X, Y = (b2, b1) if swap else (b1, b2); od = os.path.join(O, f); os.makedirs(od, exist_ok=True)
        for b, n in ((X, 'X.jpg'), (Y, 'Y.jpg')):
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src[b](f), '-vf', 'scale=1280:-2', '-q:v', '3', os.path.join(od, n)], check=True)
        key[f] = {'X': X, 'Y': Y, 'year': YEAR[f[:4]]}
    json.dump(key, open(os.path.join(O, 'key.json'), 'w'), indent=1, ensure_ascii=False); print(key)
def call(bo, f, rk):
    if spent() >= STOP: return 'dung-tran'
    O = out(bo); k = json.load(open(os.path.join(O, 'key.json')))[f]; prompt = PROMPT.format(persona=RATERS[rk], year=k['year'])
    env = dict(os.environ, ANTHROPIC_API_KEY=os.environ['CONSOLE_API_KEY'])
    with tempfile.TemporaryDirectory() as cwd:
        for s_ in ('X.jpg', 'Y.jpg'): shutil.copy(os.path.join(O, f, s_), cwd)
        for _ in range(2):
            r = subprocess.run(['claude', '-p', '--model', MODEL, '--output-format', 'json', '--allowedTools', 'Read'], input=prompt, capture_output=True, text=True, env=env, cwd=cwd, timeout=900)
            try: d = json.loads(r.stdout)
            except Exception: continue
            with open(os.path.join(O, 'cost.jsonl'), 'a') as fh:
                fh.write(json.dumps({'tag': f'v6:{bo}:{f}-{rk}', 'model': MODEL, 'served': sorted(d.get('modelUsage', {})), 'usd': d.get('total_cost_usd', 0)}) + '\n')
            open(os.path.join(O, f, f'{rk}.raw.txt'), 'w').write(d.get('result', ''))
            m = re.search(r'\{.*\}', d.get('result', ''), re.S)
            if m:
                try: json.dump(json.loads(m.group(0)), open(os.path.join(O, f, f'{rk}.json'), 'w'), indent=1); return True
                except Exception: pass
    return False
def run(bo):
    FR, _ = BO[bo]
    for f in FR:
        if spent() >= STOP: print('DỪNG mốc', round(spent(), 3)); break
        jobs = [rk for rk in RATERS if not os.path.exists(os.path.join(out(bo), f, f'{rk}.json'))]
        with ThreadPoolExecutor(3) as ex: res = list(ex.map(lambda rk: call(bo, f, rk), jobs))
        print(f, res, round(spent(), 3), flush=True)
def score(bo):
    O = out(bo); FR, BB = BO[bo]; key = json.load(open(os.path.join(O, 'key.json'))); rows = {}; M = ('craft', 'detail', 'period', 'ai_look', 'toy_like')
    tot = {b: {m: [] for m in M} for b in BB}; per = {e: {b: {m: [] for m in M} for b in BB} for e in ('1782', '1943')}
    for f, k in key.items():
        J = {rk: json.load(open(os.path.join(O, f, f'{rk}.json'))) for rk in RATERS if os.path.exists(os.path.join(O, f, f'{rk}.json'))}
        if not J: continue
        row = {}
        for slot in 'XY':
            b = k[slot]
            for m in M:
                v = [J[r][slot].get(m) for r in J if isinstance(J[r][slot].get(m), (int, float))]; row[f'{b}_{m}'] = v; tot[b][m] += v; per[f[:4]][b][m] += v
            row[f'{b}_flags'] = sorted({x for r in J for x in J[r][slot].get('flags', [])}); row[f'{b}_note'] = {r: J[r][slot].get('note') for r in J}
        row['better'] = {r: k.get(J[r].get('better'), 'tie') for r in J}; row['why'] = {r: J[r].get('why') for r in J}
        row['fix'] = {r: J[r].get('top_fix_for_weaker') for r in J}; row['anachronisms'] = {r: J[r].get('anachronisms_seen') for r in J}; rows[f] = row
    avg = lambda d: {b: {m: round(sum(v) / len(v), 2) for m, v in dd.items() if v} for b, dd in d.items()}
    R = {'khung': rows, 'tb': avg(tot), 'tb_theo_moc': {e: avg(d) for e, d in per.items()},
         'phieu_better': {b: sum(1 for r in rows.values() for v in r['better'].values() if v == b) for b in (*BB, 'tie')}, 'chi_phi_tong_so': round(spent(), 4)}
    json.dump(R, open(os.path.join(O, 'score.json'), 'w'), indent=1, ensure_ascii=False); print(json.dumps({k: R[k] for k in ('tb', 'phieu_better', 'chi_phi_tong_so')}, ensure_ascii=False))
if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'set': setup(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
    elif c == 'run': run(sys.argv[2])
    else: score(sys.argv[2])
