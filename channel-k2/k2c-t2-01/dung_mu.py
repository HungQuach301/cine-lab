#!/opt/cine/bin/python
"""K2C-T2-01 · Dựng (Mốc B, G2) — NGƯỜI CHẤM MÙ XEM NHÁP 540p, đánh dấu chỗ muốn bỏ + chữ thừa (lệnh chủ dự án 15/10, M2: mục tiêu ≤ ~45 dòng chú thích).
Giao thức như k2v2-mau/blind_v2.py: `claude -p` GHIM claude-sonnet-5-5, chỉ công cụ Read, thư mục tạm trống chỉ chứa tờ khung, 3 vai, không subagent.
Mỗi người chấm nhận: 7 tờ khung (mỗi chương một tờ, 1 khung / 4 s, ghi giây), lời theo giây (từ căn chữ thật), danh sách dòng chú thích có mã (Cnn) và giây hiện.
Hỏi: (1) đoạn muốn bỏ/rút (giây đầu–cuối, lý do); (2) dòng chú thích thừa (mã, lý do: lặp lời / thừa chữ / che hình); (3) mối nối gãy; (4) chỗ hình trống hoặc rối.
Kết quả: kiem-mu/dung/<R>.json + bảng gộp (≥ 2/3 cùng nêu → sửa một lượt). Sổ chi phí kiem-mu/cost.jsonl (tag "dung:…"), trần tập $11, dừng $10.
  dung_mu.py set <nhap.mp4> <timeline.json>   → kiem-mu/dung/ (tờ khung, lời, chú thích)
  dung_mu.py run                              → 3 vai song song
  dung_mu.py score                            → kiem-mu/dung/gop.json"""
import json, os, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
HERE = Path(__file__).resolve().parent; OUT = HERE / 'kiem-mu'; D = OUT / 'dung'; LOG = OUT / 'cost.jsonl'
MODEL, CAP, STOP = 'claude-sonnet-5-5', 11.0, 10.0
RATERS = {
    'R1': "You are a general YouTube viewer (30s) who watches documentary explainers on a phone and leaves when a video drags or feels like homework.",
    'R2': "You are a senior documentary film editor who cuts 10-15 minute explainers for YouTube and is ruthless about pacing, redundancy and on-screen text.",
    'R3': "You are a motion-graphics director who checks whether on-screen text is necessary, readable on a phone, and never fights the picture or repeats the narration word for word.",
}
PROMPT = """{persona}

In the current folder are 7 contact sheets, ch00.jpg … ch06.jpg (open ALL of them with the Read tool). Each is one chapter of a 10:45 documentary explainer draft (540p, every 4 seconds; each thumbnail shows its time in seconds from the start of the video at top-left). Below are the exact narration with timestamps, and the list of on-screen caption lines (bottom-third text strips) with ids and times. Number tags and place labels on the map are NOT in the caption list.

The producer wants FEWER caption lines: at most about 45 in total (now {ncap}). Mark the ones that are redundant (repeat the narration nearly word for word, add nothing, or clutter the picture). Keep lines that carry a source/attribution, a date or "as of" fact, a "Our read" label, or a "LORE" label unless they truly add nothing. Also mark any stretch you would cut or shorten, transitions that feel broken, and moments where the picture is empty or cluttered. Be specific and honest; do not be polite.

Return ONLY JSON:
{{"cut_or_shorten": [{{"t0": <sec>, "t1": <sec>, "why": "<short>"}}],
 "redundant_captions": [{{"id": "Cnn", "why": "repeats_narration|adds_nothing|clutters_picture|too_long"}}],
 "broken_transitions": [{{"t": <sec>, "why": "<short>"}}],
 "empty_or_cluttered": [{{"t": <sec>, "kind": "empty|cluttered|text_overlap|hard_to_read", "why": "<short>"}}],
 "pace_1to10": <int>, "visual_variety_1to10": <int>, "overall_1to10": <int>, "top3_fixes": ["<concrete>", "<concrete>", "<concrete>"]}}

=== NARRATION (seconds from video start) ===
{narr}

=== CAPTION LINES ===
{caps}"""


def spent():
    return sum(json.loads(l)['usd'] for l in open(LOG)) if LOG.exists() else 0.0


def setup(mp4, tlp):
    D.mkdir(parents=True, exist_ok=True); TL = json.load(open(tlp)); caps = []; narr = []
    for sg in TL['segments']:
        t0, t1 = sg['t0'], sg['t1']; n = int((t1 - t0) // 4) + 1; cols = 6; rows = -(-n // cols)
        with tempfile.TemporaryDirectory() as td:
            for k in range(n):
                t = t0 + 2 + 4 * k
                if t >= t1: t = t1 - 0.2
                f = os.path.join(td, f'{k:03d}.jpg')
                subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.2f}', '-i', mp4, '-frames:v', '1', '-vf', f"scale=320:-2,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='{t:.0f}s':x=6:y=6:fontsize=20:fontcolor=white:borderw=2", '-q:v', '4', f], check=True)
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', '1', '-i', os.path.join(td, '%03d.jpg'), '-vf', f'tile={cols}x{rows}:padding=4:color=black', '-frames:v', '1', '-q:v', '4', str(D / f"ch{sg['id']}.jpg")], check=True)
        al = json.load(open(HERE.parent.parent / sg['vo_file'].replace('.mp3', '.align.json'))) if sg.get('vo_file') else None
        if al:
            sys.path.insert(0, str(HERE.parent.parent / 'scripts/ll')); import ll
            W = ll.words(al); line, ls = [], None
            for w in W:
                if ls is None: ls = t0 + sg['vo_offset'] + w[1]
                line.append(w[3])
                if re.search(r'[.?!]$', w[3]): narr.append(f'[{ls:6.1f}] ' + ' '.join(line)); line, ls = [], None
            if line: narr.append(f'[{ls:6.1f}] ' + ' '.join(line))
        for sh in sg['shots']:
            for c in sh['p'].get('cap') or []:
                if c.get('s') and not any(x['s'] == c['s'] and abs(x['t'] - (t0 + c['at'])) < 12 for x in caps):
                    caps.append(dict(id=f'C{len(caps) + 1:02d}', t=round(t0 + c['at'], 1), s=c['s'], seg=sg['id']))
    json.dump(dict(caps=caps, narr=narr), open(D / 'input.json', 'w'), indent=1, ensure_ascii=False); print(len(caps), 'dòng chú thích;', len(narr), 'câu lời')


def call(rk):
    I = json.load(open(D / 'input.json'))
    prompt = PROMPT.format(persona=RATERS[rk], ncap=len(I['caps']), narr='\n'.join(I['narr']), caps='\n'.join(f"{c['id']} [{c['t']:6.1f}] {c['s']}" for c in I['caps']))
    if spent() > STOP: raise SystemExit(f'dừng: đã tiêu ${spent():.2f}')
    env = dict(os.environ, ANTHROPIC_API_KEY=os.environ['CONSOLE_API_KEY'])
    with tempfile.TemporaryDirectory() as cwd:
        for f in sorted(D.glob('ch*.jpg')): shutil.copy(f, cwd)
        for _ in range(3):
            r = subprocess.run(['claude', '-p', '--model', MODEL, '--output-format', 'json', '--allowedTools', 'Read'], input=prompt, capture_output=True, text=True, env=env, cwd=cwd, timeout=1800)
            try: d = json.loads(r.stdout)
            except Exception: continue
            u = d.get('usage', {})
            with open(LOG, 'a') as f: f.write(json.dumps({'tag': f'dung:nhap-{rk}', 'model': MODEL, 'served': sorted(d.get('modelUsage', {})), 'usd': d.get('total_cost_usd', 0),
                                                         'in': u.get('input_tokens', 0) + u.get('cache_creation_input_tokens', 0) + u.get('cache_read_input_tokens', 0), 'out': u.get('output_tokens', 0)}) + '\n')
            (D / f'{rk}.raw.txt').write_text(d.get('result', ''))
            m = re.search(r'\{.*\}', d.get('result', ''), re.S)
            if m:
                try: j = json.loads(m.group(0)); (D / f'{rk}.json').write_text(json.dumps(j, indent=1, ensure_ascii=False)); return rk, True
                except Exception: pass
    return rk, False


def score():
    I = json.load(open(D / 'input.json')); R = {rk: json.load(open(D / f'{rk}.json')) for rk in RATERS if (D / f'{rk}.json').exists()}
    cnt = {}
    for rk, j in R.items():
        for c in j.get('redundant_captions', []): cnt.setdefault(c['id'], []).append((rk, c.get('why')))
    capmap = {c['id']: c for c in I['caps']}
    red = [dict(id=k, s=capmap.get(k, {}).get('s'), t=capmap.get(k, {}).get('t'), n=len(v), why=[w for _, w in v]) for k, v in sorted(cnt.items(), key=lambda x: (-len(x[1]), x[0]))]
    G = dict(n_caps=len(I['caps']), caps_2of3=[x for x in red if x['n'] >= 2], caps_1of3=[x for x in red if x['n'] == 1],
             cut=[dict(rk=rk, **c) for rk, j in R.items() for c in j.get('cut_or_shorten', [])], transitions=[dict(rk=rk, **c) for rk, j in R.items() for c in j.get('broken_transitions', [])],
             empty=[dict(rk=rk, **c) for rk, j in R.items() for c in j.get('empty_or_cluttered', [])],
             scores={rk: {k: j.get(k) for k in ('pace_1to10', 'visual_variety_1to10', 'overall_1to10')} for rk, j in R.items()}, fixes={rk: j.get('top3_fixes') for rk, j in R.items()})
    json.dump(G, open(D / 'gop.json', 'w'), indent=1, ensure_ascii=False)
    print(json.dumps({k: G[k] for k in ('n_caps', 'scores')}, ensure_ascii=False), '\n≥2/3 chữ thừa:', [(x['id'], x['n']) for x in G['caps_2of3']])


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'set': setup(sys.argv[2], sys.argv[3])
    elif cmd == 'run':
        with ThreadPoolExecutor(3) as ex: print(list(ex.map(call, [rk for rk in RATERS if not (D / f'{rk}.json').exists()]))); print(f'chi phí luỹ kế ${spent():.2f} / trần ${CAP}')
    elif cmd == 'score': score()
