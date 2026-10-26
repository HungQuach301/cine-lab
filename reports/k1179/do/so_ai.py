#!/opt/cine/bin/python
"""K-1.17.9 · sổ AI: gộp mọi lệnh gọi mô hình của phiên (k2check --n2p-vision: n2p-cost.jsonl; q_thoi_dai O2: qtd/*/run.jsonl) → reports/k1179/so-ai.jsonl
(model, công cụ + lệnh nguyên văn, đề bài/phiên bản, SHA vào (render, ghép), SHA ra (raw.txt), usage, usd). Không chứa khoá/email."""
import glob, hashlib, json, os
K2V = '/var/tmp/k1179/k2v'; O = '/home/user/cine-lab/reports/k1179/so-ai.jsonl'
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest() if p and os.path.exists(p) else None
L = []
for d in sorted(glob.glob(f'{K2V}/*/')):
    tid = os.path.basename(d.rstrip('/')); import yaml
    E = yaml.safe_load(open(f'{d}/episode.yaml')); t = E['n2p']['tam'][0]
    lenh = f"VISION=1 /opt/cine/bin/python reports/k1179/do/e_k2.py 1.17.9-vision /var/tmp/k1179/k2v {os.path.dirname(t['ghep'])}/episode.yaml → checks/ll/k2check.py {d}episode.yaml --tl … --no-asr --cap --n2p-vision"
    for l in open(f'{d}/n2p-cost.jsonl'):
        r = json.loads(l)
        if 'usd' not in r: continue
        mh = 'gpt' if 'gpt' in r['tag'] else 'claude'
        L.append(dict(nha='openai' if mh == 'gpt' else 'anthropic', model=r['model'], served=r.get('served'), cong_cu='k2check N2P mô hình nhìn (q_n2p_vision)',
                      de_bai='n2p-e-v2-nuoc (K-1.17.9)' if r['date_utc'] >= '2026-10-26T03:43' else 'n2p-e-v2 (K-1.17.8) — lượt 1, đề bài chưa sửa',
                      lenh=lenh, tag=r['tag'], sha_vao=dict(render=sha(t['render']), ghep=sha(t['ghep'])), sha_ra=sha(f"{d}/{r['tag']}.raw.txt"),
                      usage=dict(vao=r.get('vao'), ra=r.get('ra'), so_anh_doc=r.get('so_anh_doc')), usd=float(r['usd'] or 0), date_utc=r['date_utc']))
    for f in sorted(glob.glob(f'{d}/qtd/*/run.jsonl')):
        for l in open(f):
            try: r = json.loads(l)
            except ValueError: continue
            if r.get('type') != 'result': continue
            L.append(dict(nha='anthropic', model=','.join(sorted(r.get('modelUsage') or {})), cong_cu='q_thoi_dai O2 (k2check N2P-2 (b))', de_bai='o2 (checks/ll/q_thoi_dai.py)',
                          lenh=lenh, tag=os.path.basename(os.path.dirname(f)), sha_vao=dict(anh=sha(os.path.join(os.path.dirname(f), 'full.jpg'))), sha_ra=hashlib.sha256((r.get('result') or '').encode()).hexdigest(),
                          usage=r.get('usage'), usd=float(r.get('total_cost_usd') or 0), date_utc=None))
with open(O, 'w') as w:
    for x in L: w.write(json.dumps(x, ensure_ascii=False) + '\n')
tong = {}
for x in L: tong[x['nha']] = round(tong.get(x['nha'], 0) + x['usd'], 4)
print(len(L), 'dòng', tong)
