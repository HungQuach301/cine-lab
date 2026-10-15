#!/opt/cine/bin/python
"""NỀN TẢNG · đóng băng phiên bản theo tập (phiên Nền tảng, 14/10/2026).

Ghi lúc G1, kiểm lúc G2: luật K (checks/LOCK: VERSION + TREE_SHA256, và lock.py --verify), bộ công cụ dựng
(commit git + băm nội dung cây làm việc của từng nhóm), model Claude được ghim, giọng ElevenLabs, phiên bản công cụ máy.
Lệch giữa G1 và G2 → in từng mục lệch, mã thoát 1. Không gọi mạng, không gọi API.

  versions.py record <episode.yaml> [--gate G1] [--out <thư mục tập>/VERSIONS.yaml]
  versions.py check  <VERSIONS.yaml> [--episode <episode.yaml>] [--json <tệp>]
  versions.py show   [<episode.yaml>]           # in bản chụp hiện tại, không ghi

Băm nhóm = sha256 của chuỗi '<sha256 tệp>  <đường dẫn>\\n' sắp theo đường dẫn (cùng thuật toán checks/LOCK), trên mọi tệp
git theo dõi + tệp chưa theo dõi (không bị .gitignore) trong nhóm — nên bắt cả sửa chưa commit. Mẫu: scripts/common/VERSIONS.template.yaml."""
import glob, hashlib, json, os, re, subprocess, sys, time
import yaml

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
# nhóm bộ công cụ: tên → đường dẫn trong repo (thư mục hoặc tệp). Thêm nhóm ở đây, không ở từng tập.
GROUPS = {
    'k2v': ['design/k2v', 'scripts/k2'],            # module hình kênh 2 (relief, sticker, photo, footage) + driver
    'll-hero': ['design/ll-hero'],                   # cảnh 3D (Steel k2g01, T1 k2c106, LL ep06–08)
    'll': ['scripts/ll'],                            # nhà máy LL: render.js, lib/, mix.py (kênh 2 dùng lại mix.py)
    'shared3d': ['design/cong3/shared'],             # three.js (khoá phiên bản) + post.js, props.js, cast.js… dùng chung cho cảnh 3D
}
SKIP = re.compile(r'(^|/)(node_modules|__pycache__|\.pytest_cache)(/|$)|\.pyc$')
MODEL_RE = re.compile(r"claude-(?:opus|sonnet|haiku|fable)-\d+-\d+(?:-\d{8})?")


def sh(*a, cwd=REPO):
    r = subprocess.run(a, cwd=cwd, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def files_of(paths):
    out = set()
    for p in paths:
        ls = sh('git', 'ls-files', '-co', '--exclude-standard', '--', p) or ''
        out.update(x for x in ls.splitlines() if x and not SKIP.search(x) and os.path.isfile(os.path.join(REPO, x)))
    return sorted(out)


def tree_hash(paths):
    fs = files_of(paths)
    s = ''.join(f'{sha_file(os.path.join(REPO, f))}  {f}\n' for f in fs)
    return hashlib.sha256(s.encode()).hexdigest(), len(fs)


def checks_info():
    d = {}
    lock = os.path.join(REPO, 'checks', 'LOCK')
    if os.path.exists(lock):
        t = open(lock, encoding='utf-8').read()
        for k in ('VERSION', 'TREE_SHA256'):
            m = re.search(rf'^{k}:\s*(\S+)', t, re.M); d[k.lower()] = m.group(1) if m else None
    r = subprocess.run(['/opt/cine/bin/python', 'checks/lock.py', '--verify'], cwd=REPO, capture_output=True, text=True)
    d['lock_verify'] = 'KHỚP' if r.returncode == 0 else f'LỆCH (mã {r.returncode})'
    d['commit'] = sh('git', 'log', '-1', '--format=%H', '--', 'checks')
    return d


def tools_info():
    def v(cmd, rx=r'(\d+[\w.\-~+]*)'):
        try: out = subprocess.run(cmd, capture_output=True, text=True, timeout=30).stdout + ''
        except Exception: return None
        m = re.search(rx, out); return m.group(1) if m else None
    three = None
    lk = os.path.join(REPO, 'design/cong3/shared/package-lock.json')
    if os.path.exists(lk):
        three = json.load(open(lk)).get('packages', {}).get('node_modules/three', {}).get('version')
    pw = None
    pj = '/opt/pw/node_modules/playwright/package.json'
    if os.path.exists(pj): pw = json.load(open(pj)).get('version')
    chromium = sorted(glob.glob('/opt/pw-browsers/chromium*'))
    relief = {}
    cache = os.environ.get('K2V_CACHE', '/var/tmp/cine-out/k2v-cache')
    for m in sorted(glob.glob(os.path.join(cache, 'relief', '*', 'meta.json'))):   # nền bản đồ ngoài git: SHA từng tệp (natural/sepia/height/routes)
        try: relief[os.path.basename(os.path.dirname(m))] = hashlib.sha256(json.dumps(json.load(open(m)).get('files', {}), sort_keys=True).encode()).hexdigest()[:16]
        except Exception: pass
    return {'claude_cli': v(['claude', '--version'], r'(\d+\.\d+\.\d+)'), 'relief_cache': relief or None,
            'ffmpeg': v(['ffmpeg', '-version'], r'ffmpeg version (\S+)'), 'node': v(['node', '--version'], r'v(\S+)'),
            'python_cine': v(['/opt/cine/bin/python', '--version']), 'three': three, 'playwright': pw,
            'chromium': os.path.basename(chromium[-1]) if chromium else None}


def episode_info(ep):
    """giọng (ElevenLabs) và model Claude ghim, đọc từ đặc tả tập + các tệp .py cạnh nó (ai.py, blind_*.py)."""
    E = yaml.safe_load(open(ep, encoding='utf-8'))
    d = os.path.dirname(os.path.abspath(ep))
    voice = E.get('voice') or {}
    models = set()
    for p in glob.glob(os.path.join(d, '*.py')) + glob.glob(os.path.join(d, '*', '*.py')):
        models.update(MODEL_RE.findall(open(p, encoding='utf-8', errors='ignore').read()))
    if E.get('models'): models.update(E['models'])
    return {'id': E.get('id'), 'file': os.path.relpath(os.path.abspath(ep), REPO), 'sha256': sha_file(ep),
            'voice': {k: voice.get(k) for k in ('id', 'model', 'stability', 'similarity', 'style', 'speed') if k in voice},
            'claude_models': sorted(models)}


def served_models(ep_dir):
    """model thật đã phục vụ (trường served trong kiem-mu/cost*.jsonl) — để bắt chuyển model ngầm (fallback)."""
    s = set()
    for p in glob.glob(os.path.join(ep_dir, '**', 'cost*.jsonl'), recursive=True):
        for line in open(p, encoding='utf-8'):
            try: j = json.loads(line)
            except ValueError: continue
            for k in ('served', 'model'):
                v = j.get(k)
                if isinstance(v, str): s.update(MODEL_RE.findall(v))
                elif isinstance(v, (list, dict)): s.update(MODEL_RE.findall(json.dumps(v)))
    return sorted(s)


def snapshot(ep=None, gate=None):
    S = {'schema': 1, 'gate': gate, 'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
         'repo_head': sh('git', 'rev-parse', 'HEAD'), 'branch': sh('git', 'rev-parse', '--abbrev-ref', 'HEAD'),
         'checks': checks_info(), 'toolkit': {}, 'tools': tools_info()}
    for g, ps in GROUPS.items():
        h, n = tree_hash(ps)
        S['toolkit'][g] = {'paths': ps, 'commit': sh('git', 'log', '-1', '--format=%H', '--', *ps), 'tree_sha256': h, 'files': n}
    if ep:
        S['episode'] = episode_info(ep)
    return S


def compare(A, B):
    """A = bản ghi G1, B = hiện tại. Trả danh sách (mức, mục, cũ, mới). Mức CHẶN: luật K, bộ công cụ, model, giọng. BÁO: công cụ máy."""
    D = []
    for k in ('version', 'tree_sha256'):
        if A['checks'].get(k) != B['checks'].get(k): D.append(('CHẶN', f'checks.{k}', A['checks'].get(k), B['checks'].get(k)))
    if B['checks'].get('lock_verify') != 'KHỚP': D.append(('CHẶN', 'checks.lock_verify', A['checks'].get('lock_verify'), B['checks'].get('lock_verify')))
    for g, a in A['toolkit'].items():
        b = B['toolkit'].get(g)
        if not b: D.append(('CHẶN', f'toolkit.{g}', a['tree_sha256'], None)); continue
        if a['tree_sha256'] != b['tree_sha256']:
            D.append(('CHẶN', f'toolkit.{g}.tree_sha256', f"{a['tree_sha256'][:12]} @{(a['commit'] or '')[:8]}", f"{b['tree_sha256'][:12]} @{(b['commit'] or '')[:8]}"))
    ea, eb = A.get('episode') or {}, B.get('episode') or {}
    if ea:
        if ea.get('voice') != eb.get('voice'): D.append(('CHẶN', 'episode.voice', ea.get('voice'), eb.get('voice')))
        if ea.get('claude_models') != eb.get('claude_models'): D.append(('CHẶN', 'episode.claude_models', ea.get('claude_models'), eb.get('claude_models')))
        pinned = set(ea.get('claude_models') or [])
        extra = [m for m in eb.get('served_models', []) if pinned and m not in pinned]
        if extra: D.append(('CHẶN', 'episode.served_models (model thật khác model ghim)', sorted(pinned), extra))
    for k, a in (A.get('tools') or {}).items():
        if a != (B.get('tools') or {}).get(k): D.append(('BÁO', f'tools.{k}', a, (B.get('tools') or {}).get(k)))
    return D


def arg(k, d=None):
    return sys.argv[sys.argv.index('--' + k) + 1] if '--' + k in sys.argv else d


def main():
    if len(sys.argv) < 2: sys.exit(__doc__)
    cmd = sys.argv[1]
    if cmd == 'show':
        ep = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else None
        print(yaml.safe_dump(snapshot(ep), allow_unicode=True, sort_keys=False)); return
    if cmd == 'record':
        ep = sys.argv[2]; gate = arg('gate', 'G1')
        out = arg('out', os.path.join(os.path.dirname(os.path.abspath(ep)), 'VERSIONS.yaml'))
        S = snapshot(ep, gate)
        if S['checks']['lock_verify'] != 'KHỚP': print('CẢNH BÁO: checks/lock.py --verify không khớp lúc ghi —', S['checks']['lock_verify'])
        hdr = f"# ĐÓNG BĂNG PHIÊN BẢN tập {S['episode']['id']} — ghi lúc {gate} bởi scripts/common/versions.py. KHÔNG sửa tay; G2 chạy `versions.py check`.\n"
        open(out, 'w', encoding='utf-8').write(hdr + yaml.safe_dump(S, allow_unicode=True, sort_keys=False))
        print(f'đã ghi {os.path.relpath(out, REPO)}'); return
    if cmd == 'check':
        A = yaml.safe_load(open(sys.argv[2], encoding='utf-8'))
        ep = arg('episode') or (os.path.join(REPO, A['episode']['file']) if A.get('episode') else None)
        B = snapshot(ep, 'kiểm')
        if ep: B['episode']['served_models'] = served_models(os.path.dirname(os.path.abspath(ep)))
        D = compare(A, B)
        res = {'ghi_luc': A.get('gate'), 'utc_ghi': A.get('utc'), 'utc_kiem': B['utc'], 'lech': [dict(muc=m, cu=a, moi=b, muc_do=lv) for lv, m, a, b in D]}
        if arg('json'): json.dump(res, open(arg('json'), 'w'), ensure_ascii=False, indent=1)
        block = [d for d in D if d[0] == 'CHẶN']
        for lv, m, a, b in D: print(f'{lv:5} {m}: {a} → {b}')
        print(('LỆCH — ' + str(len(block)) + ' mục chặn (báo chủ dự án ở G2; không tự cập nhật VERSIONS.yaml)') if block else
              ('KHỚP' + (f' ({len(D)} mục BÁO công cụ máy)' if D else '')))
        sys.exit(1 if block else 0)
    sys.exit(__doc__)


if __name__ == '__main__':
    main()
