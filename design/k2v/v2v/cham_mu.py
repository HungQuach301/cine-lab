#!/opt/cine/bin/python -I
"""NC-V2V · CHẤM MÙ: cặp khung cùng chỗ (đầu ra Omni ↔ khung V7B nguồn), thứ tự X/Y xáo theo hạt cố định, ở 640×360 và 320×180.
3 người chấm AI, mỗi người một lượt cho mọi cặp, không biết bên nào là AI:
  R1 claude-sonnet-5-5 (`claude -p`, chỉ công cụ Read, thư mục tạm chỉ chứa ảnh cặp) · R2 gpt-6.1-sol (OpenAI Responses API, stream — không stream bị cắt 502 ở ~30 s; khoá do proxy gắn) · R3 claude-haiku-5-5 (`claude -p` như R1).
  cham_mu.py tao <cặp.json> <thư mục>   — cặp.json: [{"id": "...", "src": nguồn.mp4, "out": ra.mp4, "f": khung}]
  cham_mu.py chay <thư mục>              — gọi 3 người chấm, ghi raw + phiếu + sổ chi phí
  cham_mu.py diem <thư mục>              — giải mã X/Y → điểm theo bên (nguồn/Omni)"""
import base64, json, os, random, subprocess, sys, time, urllib.request
from pathlib import Path
UA = 'CineLab-research (+https://github.com/HungQuach301/cine-lab)'
ASK = """You are a blind rater for a history documentary channel. Each numbered pair shows two frames, X and Y, of the SAME shot (same place, same moment); one is from version 1 and one from version 2, in random order. Rate EACH frame from 1 to 5:
- real: looks like real documentary footage filmed with a real camera (5 = indistinguishable from real footage)
- detail: fine, believable detail
- ailook: looks AI-generated or synthetic (5 = obviously AI/synthetic)
- read: at this size (as on a phone), you can make out ships and flags and tell them apart (5 = clearly; use 3 if the shot has no ships/flags)
Then pick which frame of the pair looks more like real documentary footage ("prefer": "X" or "Y") and give a reason of at most 15 words.
Answer ONLY with JSON: {"pairs": [{"pair": "<id>", "size": "<size>", "X": {"real":n,"detail":n,"ailook":n,"read":n}, "Y": {...}, "prefer": "X|Y", "why": "..."} , ...]}"""


def frame(mp4, f, w, h, out):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', mp4, '-vf', f'select=eq(n\\,{f}),scale={w}:{h}:flags=area', '-frames:v', '1', '-q:v', '2', out], check=True)


def tao(cfg, d):
    d = Path(d); (d / 'anh').mkdir(parents=True, exist_ok=True); P = json.load(open(cfg)); R = random.Random(19102026); key = {}
    for p in P:
        swap = R.random() < 0.5; key[p['id']] = 'X=omni' if swap else 'X=nguon'
        for (w, h, s) in ((640, 360, '640'), (320, 180, '320')):
            a, b = (p['out'], p['src']) if swap else (p['src'], p['out'])
            frame(a, p['f'], w, h, str(d / 'anh' / f"{p['id']}-{s}-X.jpg")); frame(b, p['f'], w, h, str(d / 'anh' / f"{p['id']}-{s}-Y.jpg"))
    json.dump(key, open(d / 'key.json', 'w'), indent=1); json.dump(P, open(d / 'cap.json', 'w'), indent=1, ensure_ascii=False); print(len(P), 'cặp')


def imgs(d): return sorted((Path(d) / 'anh').glob('*.jpg'))


def openai(model, d, tag):
    content = [{'type': 'input_text', 'text': ASK}]
    for im in imgs(d):
        pid, s, xy = im.stem.rsplit('-', 2)
        content.append({'type': 'input_text', 'text': f'pair {pid} size {s} frame {xy}:'})
        content.append({'type': 'input_image', 'image_url': 'data:image/jpeg;base64,' + base64.b64encode(im.read_bytes()).decode()})
    body = {'model': model, 'input': [{'role': 'user', 'content': content}], 'stream': True}
    r = urllib.request.Request('https://api.openai.com/v1/responses', data=json.dumps(body).encode(), headers={'Content-Type': 'application/json', 'User-Agent': UA})
    txt, J = '', {}
    with urllib.request.urlopen(r, timeout=1800) as f:
        for line in f:
            line = line.decode('utf8', 'replace').strip()
            if not line.startswith('data:'): continue
            ev = json.loads(line[5:])
            if ev.get('type') == 'response.output_text.delta': txt += ev.get('delta', '')
            if ev.get('type') == 'response.completed': J = ev.get('response', {})
    return txt, J.get('usage', {}), J.get('model')


PRICE = {'gpt-6.1-sol': (2e-6, 10e-6)}   # USD/token in/out — suy từ sổ chi phí thật NC-AI (reports/nc-ai/aib/cost.jsonl: 3 dòng khớp đúng $2/M vào, $10/M ra)


def chay(d):
    d = Path(d); cost = d / 'cost.jsonl'
    names = ' '.join(f'anh/{im.name}' for im in imgs(d))
    p1 = ASK + f'\n\nThe frames are image files in the current directory: {names}. File name = <pair>-<size>-<X|Y>.jpg. Read every file with the Read tool before answering.'
    for rk, m in (('R1', 'claude-sonnet-5-5'), ('R3', 'claude-haiku-5-5')):
        t0 = time.time(); r = subprocess.run(['claude', '-p', '--model', m, '--output-format', 'json', '--allowedTools', 'Read'], input=p1, capture_output=True, text=True, cwd=d, timeout=1800)
        J = json.loads(r.stdout); (d / f'raw-{rk}.txt').write_text(J.get('result', ''))
        with open(cost, 'a') as f: f.write(json.dumps({'nguoi': rk, 'model': m, 'served': sorted(J.get('modelUsage', {})), 'usd': J.get('total_cost_usd', 0), 'wall_s': round(time.time() - t0, 1)}) + '\n')
    for rk, m in (('R2', 'gpt-6.1-sol'),):
        t0 = time.time(); txt, u, served = openai(m, d, rk); (d / f'raw-{rk}.txt').write_text(txt)
        pi, po = PRICE[m]; usd = round(u.get('input_tokens', 0) * pi + u.get('output_tokens', 0) * po, 4)
        with open(cost, 'a') as f: f.write(json.dumps({'nguoi': rk, 'model': m, 'served': served, 'usage': u, 'usd_uoc': usd, 'wall_s': round(time.time() - t0, 1)}) + '\n')


def parse(t):
    t = t[t.find('{'): t.rfind('}') + 1]; return json.loads(t)['pairs']


def diem(d):
    d = Path(d); key = json.load(open(d / 'key.json')); P = {p['id']: p for p in json.load(open(d / 'cap.json'))}; out = {}
    for rk in ('R1', 'R2', 'R3'):
        f = d / f'raw-{rk}.txt'
        if not f.exists(): continue
        for x in parse(f.read_text()):
            pid, s = str(x['pair']), str(x['size']); om = 'X' if key.get(pid) == 'X=omni' else 'Y'; ng = 'Y' if om == 'X' else 'X'
            out.setdefault(pid, {}).setdefault(s, {})[rk] = {'omni': x[om], 'nguon': x[ng], 'chon_omni': x['prefer'] == om, 'why': x.get('why')}
    tong = {}
    for pid, by in out.items():
        for s, rr in by.items():
            for side in ('omni', 'nguon'):
                for k in ('real', 'detail', 'ailook', 'read'):
                    v = [r[side][k] for r in rr.values()]; tong.setdefault(pid, {}).setdefault(s, {}).setdefault(side, {})[k] = round(sum(v) / len(v), 2)
            tong[pid][s]['chon_omni'] = f"{sum(r['chon_omni'] for r in rr.values())}/{len(rr)}"
    json.dump({'phieu': out, 'tb': tong}, open(d / 'ket-qua.json', 'w'), indent=1, ensure_ascii=False); print(json.dumps(tong, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'tao': tao(sys.argv[2], sys.argv[3])
    elif c == 'chay': chay(sys.argv[2])
    elif c == 'diem': diem(sys.argv[2])
