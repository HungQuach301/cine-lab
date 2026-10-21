#!/opt/cine/bin/python
"""ANIMATIC-T3 việc 8 · XEM CÂM 3 người AI — CHỈ THAM KHẢO (chủ dự án là người chấm cuối, §13.4). Giao thức V7B/V7C (scripts/k2tl/v7b_cam.py): `claude -p` ghim
claude-sonnet-5-5, chỉ công cụ Read, thư mục tạm chỉ chứa tờ khung; 3 vai nguyên văn V7B; chuỗi khung KHÔNG phụ đề, không tiếng, 1 khung / 4 s (cả tập 761 s) ở 320×180.
8 câu hiểu cốt truyện cả tập (§13.4). Chấm từ khoá (0/1/2) + P đọc lại nguyên văn (điền 'p_doc' trong ket-qua.json bằng tay).
  anim_cam.py to <master.mp4> · run · score"""
import json, os, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from PIL import Image, ImageDraw
ROOT = Path(__file__).resolve().parents[2]; D = ROOT / 'reports/animatic-t3/xem-cam'; D.mkdir(parents=True, exist_ok=True); LOG = D / 'cost.jsonl'; MODEL = 'claude-sonnet-5-5'; STEP = 4
RATERS = {
 'R1': 'You are a regular YouTube viewer who often watches short history videos on your phone WITH THE SOUND OFF (e.g. on a train).',
 'R2': 'You are a secondary-school history teacher who has never studied Gibraltar in detail.',
 'R3': 'You are a documentary film editor who judges whether pictures alone tell a story.',
}
Q = ['Q1 Who holds the fortified town on the big rock after 1704 (whose flag)?',
     'Q2 What begins in 1779?',
     'Q3 Why are people in the town hungry around 1780?',
     'Q4 What comes to help/rescue the town?',
     'Q5 What happens at sea in September 1782?',
     'Q6 What gets built, over the centuries, on the flat sandy land north of the rock?',
     'Q7 What happens at the border gate in 1969, and later?',
     'Q8 What connects the two towns on either side of the border today?']
KEY = {'Q1': (['brit', 'english', 'england', 'union', 'redcoat', 'red coat'], []),
       'Q2': (['siege', 'blockade', 'besieg'], ['spanish', 'spain', 'camp', 'army', 'fleet', 'ships', 'tents']),
       'Q3': (['blockade', 'cut off', 'siege', 'surround', 'no supplies', 'blocked', 'turned back', 'turned away'], ['food', 'sea', 'supply', 'ships', 'boats']),
       'Q4': (['fleet', 'convoy', 'ships', 'relief', 'navy'], ['brit', 'supply', 'relief', 'convoy', 'barrels', 'cargo']),
       'Q5': (['floating batter', 'batteries', 'burn', 'fire', 'attack'], ['fail', 'destroy', 'burn', 'sink', 'explod', 'lost']),
       'Q6': (['runway', 'airfield', 'airstrip', 'fence', 'wall', 'line', 'fortif'], ['runway', 'airfield', 'airstrip', 'fence']),
       'Q7': (['close', 'shut', 'stop'], ['reopen', 'open again', 'resume', 'later']),
       'Q8': (['people cross', 'workers', 'commut', 'pedestrian', 'walk', 'crowd', 'crossing'], ['daily', 'work', 'gate', 'border', 'runway'])}
PROMPT = """{persona}

The current folder holds {n} contact sheets ({names}) of a ~12-minute 3D-animated history video, sampled ONE FRAME EVERY {step} SECONDS in order (frame number + seconds are printed above each frame).
You watch it MUTED and WITHOUT subtitles: you only have the pictures (and any text that appears on screen, such as a date counter or a short chapter title). Open every sheet with the Read tool and look carefully, in order.
Then answer, from the pictures only (say "not sure" if the pictures do not tell you; do not guess from outside knowledge you cannot see evidence for):
{qs}
Also give: clarity (1–5, how clearly the pictures alone tell a story), and the frame numbers where you got lost (if any) with one short reason each.
Return ONLY JSON: {{"Q1": "...", "Q2": "...", "Q3": "...", "Q4": "...", "Q5": "...", "Q6": "...", "Q7": "...", "Q8": "...", "clarity": <int>, "lost": [{{"frame": <int>, "why": "..."}}]}}"""

def spent(): return sum(json.loads(l)['usd'] for l in open(LOG)) if LOG.exists() else 0.0
def to(master):
    tmp = Path('/var/tmp/cine-out/k2c-t3-anim/cam'); shutil.rmtree(tmp, ignore_errors=True); tmp.mkdir(parents=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', master, '-vf', f'fps=1/{STEP},scale=320:180:flags=area', str(tmp / '%04d.jpg')], check=True)
    fs = sorted(tmp.glob('*.jpg')); per, cols = 24, 4
    for p in D.glob('to-*.jpg'): p.unlink()
    for b in range(0, len(fs), per):
        F = fs[b:b + per]; rows = (len(F) + cols - 1) // cols; S = Image.new('RGB', (320 * cols, 196 * rows), (12, 12, 12)); g = ImageDraw.Draw(S)
        for i, f in enumerate(F):
            k = b + i; x, y = (i % cols) * 320, (i // cols) * 196; S.paste(Image.open(f), (x, y + 16)); g.text((x + 4, y + 2), f'#{k}  {k * STEP} s', fill=(255, 230, 120))
        S.save(D / f'to-{b // per + 1:02d}.jpg', quality=80)
    print(len(fs), 'khung')
def call(rk):
    if spent() > 8.0: raise SystemExit(f'dừng: ${spent():.2f}')
    sheets = sorted(D.glob('to-*.jpg')); out = D / f'phieu-{rk}.json'
    prompt = PROMPT.format(persona=RATERS[rk], n=len(sheets), names=', '.join(s.name for s in sheets), step=STEP, qs='\n'.join(Q))
    with tempfile.TemporaryDirectory() as cwd:
        for s in sheets: shutil.copy(s, cwd)
        for _ in range(2):
            r = subprocess.run(['claude', '-p', '--model', MODEL, '--output-format', 'json', '--allowedTools', 'Read'], input=prompt, capture_output=True, text=True, cwd=cwd, timeout=1500)
            try: d = json.loads(r.stdout)
            except Exception: continue
            with open(LOG, 'a') as f: f.write(json.dumps({'tag': f'anim-xem-cam:{rk}', 'model': MODEL, 'served': sorted(d.get('modelUsage', {})), 'usd': d.get('total_cost_usd', 0)}) + '\n')
            (D / f'raw-{rk}.txt').write_text(d.get('result', ''))
            m = re.search(r'\{.*\}', d.get('result', ''), re.S)
            if m:
                try: out.write_text(json.dumps(json.loads(m.group(0)), ensure_ascii=False, indent=1)); return True
                except Exception: pass
    return False
def grade(q, a):
    a = (a or '').lower(); must, extra = KEY[q]
    if 'not sure' in a and not any(k in a for k in must): return 0
    hit = any(k in a for k in must); ex = any(k in a for k in extra) if extra else True
    return 2 if hit and ex else 1 if hit else 0
def score():
    R = {}
    for rk in RATERS:
        p = D / f'phieu-{rk}.json'
        if not p.exists(): continue
        j = json.loads(p.read_text()); R[rk] = dict(diem={q: grade(q, j.get(q)) for q in KEY}, clarity=j.get('clarity'), tra_loi={q: j.get(q) for q in KEY}, lac=j.get('lost', []))
    tot = {q: sum(R[r]['diem'][q] for r in R) for q in KEY}
    out = dict(ghi='THAM KHẢO — không phải chấm đạt; chủ dự án chấm cuối (§13.4)', may=f'{MODEL} (claude -p, chỉ Read)', thang='0/1/2 mỗi câu × 3 người = tối đa 6/câu', theo_cau=tot,
               tong=sum(tot.values()), toi_da=6 * len(KEY), clarity_tb=round(sum(R[r]['clarity'] or 0 for r in R) / max(1, len(R)), 2), nguoi=R, chi_phi_usd=round(spent(), 4))
    (D / 'ket-qua.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n'); print(json.dumps({k: out[k] for k in ('theo_cau', 'tong', 'toi_da', 'clarity_tb', 'chi_phi_usd')}, ensure_ascii=False))
if __name__ == '__main__':
    if sys.argv[1] == 'to': to(sys.argv[2])
    if 'run' in sys.argv:
        with ThreadPoolExecutor(3) as ex: print(dict(zip(RATERS, ex.map(call, RATERS))), f'${spent():.3f}')
    if 'score' in sys.argv: score()
