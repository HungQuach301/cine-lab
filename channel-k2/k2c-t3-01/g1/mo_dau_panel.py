#!/opt/cine/bin/python
"""G1 T3 · O7 — bảng người xem mô phỏng chấm 3 mở đầu (Kinh thánh §11.5).
Giao thức (theo k2c-t2-01/dung_mu.py): `claude -p` GHIM claude-sonnet-5-5, KHÔNG công cụ, thư mục tạm trống; 5 vai khán giả YouTube khác nhau;
ẩn tác giả (không nói ai làm, không nói kênh, không nói AI; ba bản gọi X/Y/Z, thứ tự xáo khác nhau cho từng vai để khử thiên vị vị trí).
Câu hỏi chính: sau 30 giây có xem tiếp không (yes/no) + xác suất 0–10 + lý do + chỗ muốn bỏ đi; rồi xếp hạng 3 bản.
Sổ chi phí g1/kiem-mu/cost.jsonl (tag "mo-dau:<vai>"), trần lệnh $3 cho cả phiên, dừng ở $2,5.
  mo_dau_panel.py run     → g1/kiem-mu/mo-dau/<vai>.json (song song)
  mo_dau_panel.py score   → g1/kiem-mu/mo-dau/gop.json"""
import json, os, random, re, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent; OUT = HERE / 'kiem-mu' / 'mo-dau'; LOG = HERE / 'kiem-mu' / 'cost.jsonl'
MODEL, STOP = 'claude-sonnet-5-5', 2.5
VERS = os.environ.get('VERS', 'ABC').split(',') if ',' in os.environ.get('VERS', '') else list(os.environ.get('VERS', 'ABC'))
OUT = OUT if os.environ.get('VERS', 'ABC') == 'ABC' else HERE / 'kiem-mu' / ('mo-dau-' + os.environ['VERS'])
TITLE = 'Why Gibraltar Was Besieged 14 Times'
RATERS = {
    'V1-luot-dien-thoai': "You are 23, you scroll YouTube on your phone on the bus, mostly short history and geography videos; you leave in seconds if an opening feels slow, vague or like a lecture.",
    'V2-me-su': "You are 54, a history enthusiast who watches long military-history and siege documentaries; you have read about Gibraltar and you leave when a video oversimplifies, gets a date wrong or sounds like clickbait.",
    'V3-nguoi-andalucia': "You are 38 and live in Cádiz province, Spain; you watch English-language history videos and you are quick to leave when a video about Gibraltar takes the British side or treats Spain as the villain.",
    'V4-nguoi-anh': "You are 61, British, your father served in the Gibraltar garrison; you enjoy history videos but you leave when one sneers at Britain or turns Gibraltar's story into a modern political rant.",
    'V5-kinh-te-dia-ly': "You are 31 and watch economics and geography explainer videos about why places get rich or poor; you came for the mechanism behind a place, and you leave if a video is only battles and dates.",
}
PROMPT = """{persona}

You just clicked a YouTube video titled "{title}". Below are three different versions of its first ~30 seconds (X, Y and Z). Each line gives the picture on screen in [brackets] and then the narration. After these 30 seconds, all three versions continue identically.

{versions}

For EACH version, answer honestly as yourself: after these 30 seconds, would you keep watching? Then rank the three. Do not be polite; you have no stake in who made it.
Reply with ONLY this JSON (no other text):
{{"X": {{"keep_watching": true|false, "chance_0to10": n, "why": "...", "moment_you_would_leave_or_doubt": "..."}},
 "Y": {{...}}, "Z": {{...}},
 "ranking_best_first": ["?", "?", "?"], "one_change_to_the_best_version": "..."}}"""


def versions():
    md = (HERE / 'mo-dau.md').read_text(); V = {}
    for key, body in re.findall(r'^## ([A-E]) —.*?\n(.*?)(?=^## )', md, re.S | re.M):
        rows = [r for r in body.splitlines() if re.match(r'^\| 0[a-e] ', r)]
        V[key] = [(c[2].strip(), re.sub(r'\s*\{[^}]*\}', '', c[3]).strip()) for c in (r.split('|') for r in rows)]
    assert set(V) >= {'A', 'B', 'C'}, V.keys()
    return {k: V[k] for k in VERS}


def spent():
    return sum(json.loads(l)['usd'] for l in LOG.read_text().splitlines()) if LOG.exists() else 0.0


def call(rk, seed, suf=''):
    V = versions(); keys = list(VERS); random.Random(seed).shuffle(keys)
    lab = dict(zip('XYZ', keys))
    txt = '\n\n'.join(f'--- Version {x} ---\n' + '\n'.join(f'[{h}] {l}' for h, l in V[k]) for x, k in lab.items())
    prompt = PROMPT.format(persona=RATERS[rk], title=TITLE, versions=txt)
    if spent() > STOP: raise SystemExit(f'dừng: đã tiêu ${spent():.2f}')
    env = dict(os.environ, ANTHROPIC_API_KEY=os.environ['CONSOLE_API_KEY'])
    with tempfile.TemporaryDirectory() as cwd:
        for _ in range(3):
            r = subprocess.run(['claude', '-p', '--model', MODEL, '--output-format', 'json', '--allowedTools', ''], input=prompt, capture_output=True, text=True, env=env, cwd=cwd, timeout=900)
            try: d = json.loads(r.stdout)
            except Exception: continue
            u = d.get('usage', {})
            with open(LOG, 'a') as f: f.write(json.dumps({'tag': f'mo-dau:{rk}{suf}', 'model': MODEL, 'served': sorted(d.get('modelUsage', {})), 'usd': d.get('total_cost_usd', 0),
                                                         'in': u.get('input_tokens', 0) + u.get('cache_creation_input_tokens', 0) + u.get('cache_read_input_tokens', 0), 'out': u.get('output_tokens', 0)}) + '\n')
            (OUT / f'{rk}{suf}.raw.txt').write_text(d.get('result', ''))
            m = re.search(r'\{.*\}', d.get('result', ''), re.S)
            if m:
                try:
                    j = json.loads(m.group(0)); j['_nhan'] = lab; j['_prompt'] = prompt
                    (OUT / f'{rk}{suf}.json').write_text(json.dumps(j, indent=1, ensure_ascii=False)); return rk + suf, True
                except Exception: pass
    return rk + suf, False


def score():
    R = {p.stem: json.loads(p.read_text()) for p in sorted(OUT.glob('V*.json'))}
    G = {k: dict(xem_tiep=0, diem=[], hang=[], ly_do=[], cho_bo=[]) for k in VERS}
    for rk, j in R.items():
        inv = j['_nhan']
        for x, k in inv.items():
            a = j[x]; g = G[k]; g['xem_tiep'] += bool(a['keep_watching']); g['diem'].append(a['chance_0to10'])
            g['ly_do'].append(f"{rk}: {a['why']}"); g['cho_bo'].append(f"{rk}: {a['moment_you_would_leave_or_doubt']}")
        for pos, x in enumerate(j['ranking_best_first']): G[inv[x]]['hang'].append(pos + 1)
    for k, g in G.items():
        g['diem_tb'] = round(sum(g['diem']) / len(g['diem']), 2); g['hang_tb'] = round(sum(g['hang']) / len(g['hang']), 2); g['so_vai'] = len(g['diem'])
    order = sorted(VERS, key=lambda k: (-G[k]['xem_tiep'], G[k]['hang_tb'], -G[k]['diem_tb']))
    out = dict(xep_hang=order, ban=G, sua_ban_tot_nhat={rk: j.get('one_change_to_the_best_version') for rk, j in R.items()}, chi_phi_usd=round(spent(), 4))
    (OUT / 'gop.json').write_text(json.dumps(out, indent=1, ensure_ascii=False))
    for k in order: print(k, 'xem tiếp', G[k]['xem_tiep'], '/', G[k]['so_vai'], '· điểm TB', G[k]['diem_tb'], '· hạng TB', G[k]['hang_tb'])
    print('$', out['chi_phi_usd'])


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    if sys.argv[1] == 'run':
        with ThreadPoolExecutor(5) as ex:
            jobs = [(rk, i + 7, '') for i, rk in enumerate(RATERS)] + [(rk, i + 101, '-b') for i, rk in enumerate(RATERS)]   # 2 lượt, thứ tự X/Y/Z xáo khác nhau
            for rk, ok in ex.map(lambda a: call(*a), jobs): print(rk, ok)
    else: score()
