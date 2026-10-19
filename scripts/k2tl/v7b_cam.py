#!/opt/cine/bin/python
"""V7B · XEM CÂM lại (cùng 3 vai, cùng 4 câu, cùng giao thức V7P — reports/v7p/xem-cam): chuỗi khung KHÔNG phụ đề, không lời của bản thử V7B (biến thể C1 = đối số).
Bản gốc V7-PILOT · XEM CÂM (HC-2): 3 người chấm AI xem chuỗi khung 1 khung/2 s của bản thử (master KHÔNG phụ đề, không tiếng — reports/v7p/xem-cam/to-*.jpg),
trả lời 4 câu hiểu cốt truyện. Giao thức như reports/g1b-t3/nguoi/blind_toy.py: `claude -p` ghim claude-sonnet-5-5, chỉ công cụ Read, thư mục tạm chỉ chứa tờ khung.
Chấm: đáp án khoá (KEY) — 2 = đúng ý chính, 1 = đúng một phần, 0 = sai/không biết; chấm bằng từ khoá + P đọc lại nguyên văn (ghi 'p_doc').
  v7b_cam.py a|b run · score"""
import json, os, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]; V = next((a for a in sys.argv[1:] if a in ('a', 'b')), 'a'); D = ROOT / f'reports/v7b/xem-cam/{V}'; LOG = ROOT / 'reports/v7b/xem-cam/cost.jsonl'; MODEL = 'claude-sonnet-5-5'
RATERS = {
 'R1': 'You are a regular YouTube viewer who often watches short history videos on your phone WITH THE SOUND OFF (e.g. on a train).',
 'R2': 'You are a secondary-school history teacher who has never studied Gibraltar in detail.',
 'R3': 'You are a documentary film editor who judges whether pictures alone tell a story.',
}
Q = ['Q1 Who holds the Rock (the fortified town on the big rock) during the main part of this video?',
     'Q2 What begins in 1779?',
     'Q3 Why are people in the town hungry?',
     'Q4 What comes to help/rescue the town?']
PROMPT = """{persona}

The current folder holds {n} contact sheets ({names}) of a ~2-minute 3D-animated history video, sampled ONE FRAME EVERY 2 SECONDS in order (numbers + seconds are printed above each frame).
You watch it MUTED and WITHOUT subtitles: you only have the pictures (and any text that appears on screen). Open every sheet with the Read tool and look carefully, in order.
Then answer, from the pictures only (say "not sure" if the pictures do not tell you; do not guess from outside knowledge you cannot see evidence for):
{qs}
Also give: clarity (1–5, how clearly the pictures alone tell a story), and the frame numbers where you got lost (if any) with one short reason each.
Return ONLY JSON: {{"Q1": "...", "Q2": "...", "Q3": "...", "Q4": "...", "clarity": <int>, "lost": [{{"frame": <int>, "why": "..."}}]}}"""
KEY = {'Q1': (['brit', 'english', 'england', 'union', 'redcoat', 'red coat'], []),
       'Q2': (['siege', 'blockade', 'besieg'], ['spanish', 'spain', 'camp', 'army', 'fleet', 'ships', 'navy']),
       'Q3': (['blockade', 'cut off', 'siege', 'surround', 'no supplies', 'supplies', 'ships block', 'blocked'], ['food', 'sea', 'supply']),
       'Q4': (['fleet', 'convoy', 'ships', 'relief', 'navy'], ['brit', 'supply', 'relief', 'convoy'])}

def spent(): return sum(json.loads(l)['usd'] for l in open(LOG)) if LOG.exists() else 0.0
def call(rk):
    if spent() > 6.0: raise SystemExit(f'dừng: ${spent():.2f}')
    sheets = sorted(D.glob('to-*.jpg')); out = D / f'phieu-{rk}.json'
    prompt = PROMPT.format(persona=RATERS[rk], n=len(sheets), names=', '.join(s.name for s in sheets), qs='\n'.join(Q))
    with tempfile.TemporaryDirectory() as cwd:
        for s in sheets: shutil.copy(s, cwd)
        for _ in range(2):
            r = subprocess.run(['claude', '-p', '--model', MODEL, '--output-format', 'json', '--allowedTools', 'Read'], input=prompt, capture_output=True, text=True, cwd=cwd, timeout=900)
            try: d = json.loads(r.stdout)
            except Exception: continue
            with open(LOG, 'a') as f: f.write(json.dumps({'tag': f'v7b-xem-cam-{V}:{rk}', 'model': MODEL, 'served': sorted(d.get('modelUsage', {})), 'usd': d.get('total_cost_usd', 0)}) + '\n')
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
    return 2 if hit and ex else 1 if hit or (extra and ex and q in ('Q3', 'Q4')) else 0
def score():
    R = {}
    for rk in RATERS:
        p = D / f'phieu-{rk}.json'
        if not p.exists(): continue
        j = json.loads(p.read_text()); R[rk] = dict(diem={q: grade(q, j.get(q)) for q in KEY}, clarity=j.get('clarity'), tra_loi={q: j.get(q) for q in KEY}, lac=j.get('lost', []))
    tot = {q: sum(R[r]['diem'][q] for r in R) for q in KEY}; out = dict(may='claude-sonnet-5-5 (claude -p, chỉ Read)', thang='0/1/2 mỗi câu × 3 người = tối đa 6', theo_cau=tot,
               tong=sum(tot.values()), toi_da=6 * len(KEY), clarity_tb=round(sum(R[r]['clarity'] or 0 for r in R) / max(1, len(R)), 2), nguoi=R, chi_phi_usd=round(spent(), 4))
    (D / 'ket-qua.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n'); print(json.dumps({k: out[k] for k in ('theo_cau', 'tong', 'toi_da', 'clarity_tb', 'chi_phi_usd')}, ensure_ascii=False))
if __name__ == '__main__':
    if 'run' in sys.argv:
        with ThreadPoolExecutor(3) as ex: print(dict(zip(RATERS, ex.map(call, RATERS))), f'${spent():.3f}')
    if 'score' in sys.argv: score()
