#!/opt/cine/bin/python
"""THU-B-T4 · chi phí thật: sổ AI ảnh (reports/thu-b-t4/so-ai.jsonl) + mô hình nhìn/O2 của k2check (channel-k2/k2c-t4-02/thu-b/kiem/*/vision: n2p-cost.jsonl, qtd/*/run.jsonl
total_cost_usd) — khử trùng lặp theo (tag, date_utc) vì thư mục vision chép lũy kế qua các lần chạy cùng tên. → reports/thu-b-t4/do/chi-phi.json"""
import glob, json, os, re
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
so = [json.loads(l) for l in open(os.path.join(REPO, 'reports/thu-b-t4/so-ai.jsonl'))]
anh = sum(float(x.get('usd') or 0) for x in so); n_anh = sum(1 for x in so if x.get('http') == 200)
seen = set(); gpt = cl = 0.0; n_g = n_c = 0
for f in glob.glob(os.path.join(REPO, 'channel-k2/k2c-t4-02/thu-b/kiem/*/vision/n2p-cost.jsonl')):
    for l in open(f):
        d = json.loads(l); key = (d.get('tag'), d.get('date_utc'))
        if key in seen: continue
        seen.add(key)
        if 'gpt' in d.get('model', ''): gpt += float(d.get('usd') or 0); n_g += 1
        else: cl += float(d.get('usd') or 0); n_c += 1
o2 = 0.0; n_o2 = 0; seen2 = set()
for f in glob.glob(os.path.join(REPO, 'channel-k2/k2c-t4-02/thu-b/kiem/*/vision/qtd/*/run.jsonl')):
    for l in open(f):
        if '"total_cost_usd"' not in l: continue
        d = json.loads(l); key = (d.get('session_id'), d.get('total_cost_usd'))
        if key in seen2: continue
        seen2.add(key); o2 += float(d['total_cost_usd']); n_o2 += 1
out = dict(openai=dict(anh_usd=round(anh, 4), so_anh=n_anh, nhin_gpt_usd=round(gpt, 4), lan_nhin=n_g, tong=round(anh + gpt, 4), moc=4, chan=10),
           claude_api=dict(nhin_claude_usd=round(cl, 4), lan_nhin=n_c, q_thoi_dai_o2_usd=round(o2, 4), lan_o2=n_o2, tong=round(cl + o2, 4), moc=4, chan=12),
           gemini=0, elevenlabs=0, runpod=0, youtube=0)
os.makedirs(os.path.join(REPO, 'reports/thu-b-t4/do'), exist_ok=True); json.dump(out, open(os.path.join(REPO, 'reports/thu-b-t4/do/chi-phi.json'), 'w'), indent=1); print(json.dumps(out))
