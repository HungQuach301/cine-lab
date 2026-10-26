#!/opt/cine/bin/python
"""BAN-CUOI-T4-A · chi phí thật theo nhà từ sổ (không gõ tay): reports/ban-cuoi-t4-a/{so-ai.jsonl (OpenAI ảnh), so-ai-gemini.jsonl (Omni + Flash), cost.jsonl (gpt-6.1-sol tầng 2)};
q_thoi_dai (claude-sonnet-5-5 qua `claude -p`) = 'chi phí $x' trong mọi tệp kiểm q_thoi_dai (omni/kiem2/qtd-moc-*.json, *-kiem.json khung[].q_thoi_dai) + k2check (n2p-cost.jsonl, qtd/);
k2check mô hình nhìn (gpt + claude) = /var/tmp/bc/k2c/*/n2p-cost.jsonl (chép vào git: ban-cuoi/*/kiem/*/vision/). Ghi sổ Claude từng lệnh: reports/ban-cuoi-t4-a/so-ai-claude.jsonl.
  chi_phi.py → reports/ban-cuoi-t4-a/do/chi-phi.json"""
import glob, json, os, re, shutil
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))); R = f'{REPO}/reports/ban-cuoi-t4-a'; BC = f'{REPO}/channel-k2/k2c-t4-02/ban-cuoi'
rows = lambda p: [json.loads(l) for l in open(p) if l.strip()] if os.path.exists(p) else []
oai_anh = sum(float(r.get('usd') or 0) for r in rows(f'{R}/so-ai.jsonl') if r.get('nha') == 'openai')
oai_t2 = sum(float(r.get('usd') or 0) for r in rows(f'{R}/cost.jsonl') if str(r.get('model', '')).startswith('gpt'))
gem = rows(f'{R}/so-ai-gemini.jsonl'); omni = sum(float(r.get('usd') or 0) for r in gem if 'omni' in str(r.get('model_req'))); flash = sum(float(r.get('usd') or 0) for r in gem if 'flash' in str(r.get('model_req')) and 'omni' not in str(r.get('model_req')))
omni_s = [r for r in gem if 'omni' in str(r.get('model_req')) and r.get('http') == 200 and r.get('output')]
CL = []; seen = set()
def qtd(p, nguon):
    try: d = json.load(open(p))
    except Exception: return
    def walk(o, tag):
        if isinstance(o, dict):
            v = o.get('val')
            if isinstance(v, str) and 'chi phí $' in v and (p, tag) not in seen:
                m = re.search(r'chi phí \$([0-9.]+)', v); seen.add((p, tag))
                CL.append(dict(nha='anthropic', model='claude-sonnet-5-5', cong_cu='checks/ll/q_thoi_dai.py (claude -p)', tep=os.path.relpath(p, REPO) if p.startswith(REPO) else p, tag=tag, usd=float(m.group(1)), nguon=nguon, val=v[:160]))
            for k, x in o.items(): walk(x, tag + '/' + k if k == 'q_thoi_dai' else tag)
        elif isinstance(o, list):
            for i, x in enumerate(o): walk(x, f'{tag}[{i}]')
    walk(d, os.path.basename(p))
for p in glob.glob(f'{BC}/omni/kiem2/*.json'): qtd(p, 'M-d tầng 2 / lớp mốc')
k2 = {'gpt': 0.0, 'claude': 0.0}
for d in glob.glob('/var/tmp/bc/k2c/*/'):
    n = os.path.basename(d.rstrip('/')); dst = None
    for cand in (f'{BC}/e/kiem/{n}', f'{BC}/b/kiem/{n}'):
        if os.path.isdir(cand): dst = f'{cand}/vision'
    for r in rows(f'{d}/n2p-cost.jsonl'):
        if 'gpt' in str(r.get('model')): k2['gpt'] += float(r.get('usd') or 0)
        elif 'claude' in str(r.get('model')):
            k2['claude'] += float(r.get('usd') or 0); CL.append(dict(nha='anthropic', model=r['model'], cong_cu='k2check --n2p-vision', tep=f'{n}/n2p-cost.jsonl', tag=r.get('tag'), usd=float(r.get('usd') or 0), nguon='k2check tấm E/B'))
    for p in glob.glob(f'{d}/qtd/*.json') + glob.glob(f'{d}/**/qtd*.json', recursive=True): qtd(p, 'k2check N2P-2 q_thoi_dai')
    if dst:
        os.makedirs(dst, exist_ok=True)
        for f in glob.glob(f'{d}/*.raw.txt') + glob.glob(f'{d}/n2p-cost.jsonl'): shutil.copy(f, dst)
with open(f'{R}/so-ai-claude.jsonl', 'w') as f:
    for c in CL: f.write(json.dumps(c, ensure_ascii=False) + '\n')
claude = round(sum(c['usd'] for c in CL), 3)
import sys; sys.path.insert(0, f'{REPO}/scripts/k2ldn/anim'); os.environ.update(GEM_DIR='reports/ban-cuoi-t4-a', GEM_TRUOC_THEM='reports/animatic-t4/so-ai-gemini.jsonl,reports/animatic-t4-v2/so-ai-gemini.jsonl')
import gem_lib as G
out = dict(openai=dict(anh=round(oai_anh, 3), tang2_gpt=round(oai_t2, 3), k2check_gpt=round(k2['gpt'], 3), tong=round(oai_anh + oai_t2 + k2['gpt'], 3)),
           gemini=dict(omni=round(omni, 3), flash=round(flash, 3), tong_phien=round(omni + flash, 3), t4_tong=G.tong_t4(), omni_giay=round(sum(float(r.get('giay') or 0) for r in omni_s), 1), omni_lenh=len([r for r in gem if 'omni' in str(r.get('model_req'))])),
           claude_api=dict(tong=claude, q_thoi_dai=round(sum(c['usd'] for c in CL if 'q_thoi_dai' in c['cong_cu']), 3), k2check_vision=round(k2['claude'], 3), so_dong=len(CL)),
           elevenlabs=0, runpod=0)
json.dump(out, open(f'{R}/do/chi-phi.json', 'w'), ensure_ascii=False, indent=1); print(json.dumps(out, ensure_ascii=False, indent=1))
