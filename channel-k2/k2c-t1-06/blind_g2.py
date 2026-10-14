#!/opt/cine/bin/python
"""K2C-T1-06 G2 · chấm hình mù (Q27) và xem liền mạch mù (Q31) MỘT LẦN trên bản 1080p — chép giao thức k2g-ep01/blind_k2.py (cùng 3 vai, cùng thang,
cùng cờ lỗi, cùng cách lấy khung), chỉ đổi mô tả đề tài/thời lượng. `claude -p` ghim claude-sonnet-5-5, chỉ công cụ Read, thư mục tạm trống chỉ chứa ảnh;
khoá ANTHROPIC_API_KEY lấy từ $CONSOLE_API_KEY trong môi trường tiến trình con (không in, không ghi). Chi phí: kiem-mu/cost.jsonl (sổ chung của tập, trần $40, dừng $36).
Kênh 2 chưa có tập tham chiếu → chấm tuyệt đối theo thang mô tả + cờ lỗi (như K2G-01).
  blind_g2.py q27 <master.mp4> [--n 12] [--seed 11]
  blind_g2.py q31 <master.mp4> <timeline.json>
Người chấm chỉ nhận ảnh + lời (Q31), không nhận đặc tả, mã, hay kịch bản."""
import json, os, random, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__)); KM = os.path.join(HERE, 'kiem-mu'); OUT = os.path.join(KM, 'blind-g2'); os.makedirs(OUT, exist_ok=True)
LOG = os.path.join(KM, 'cost.jsonl'); CAP, STOP, MODEL = 40.0, 36.0, 'claude-sonnet-5-5'
dur = lambda v: float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', v], capture_output=True, text=True).stdout)
def grab(v, t, out, w=1280): subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', v, '-frames:v', '1', '-vf', f'scale={w}:-2', '-q:v', '3', out], check=True)
def spent(): return sum(json.loads(l)['usd'] for l in open(LOG)) if os.path.exists(LOG) else 0.0


def aicall(prompt, tag, files):
    if spent() > STOP: raise SystemExit(f'dừng: đã tiêu ${spent():.2f} (dừng ở ${STOP}, trần ${CAP})')
    env = dict(os.environ, ANTHROPIC_API_KEY=os.environ['CONSOLE_API_KEY'])
    with tempfile.TemporaryDirectory() as cwd:
        for f in files: shutil.copy(f, cwd)
        for _ in range(2):
            r = subprocess.run(['claude', '-p', '--model', MODEL, '--output-format', 'json', '--allowedTools', 'Read'], input=prompt, capture_output=True, text=True, env=env, cwd=cwd, timeout=1800)
            try: d = json.loads(r.stdout)
            except Exception: continue
            with open(LOG, 'a') as fh: fh.write(json.dumps({'tag': f'g2-{tag}', 'model': MODEL, 'served': sorted(d.get('modelUsage', {})), 'usd': d.get('total_cost_usd', 0)}) + '\n')
            open(os.path.join(OUT, f'{tag}.raw.txt'), 'w').write(d.get('result', ''))
            m = re.search(r'\{.*\}', d.get('result', ''), re.S)
            if m:
                try: j = json.loads(m.group(0)); json.dump(j, open(os.path.join(OUT, f'{tag}.json'), 'w'), indent=1); return j
                except Exception: pass
    return None

RATERS = {
  'R1': "You are a general YouTube viewer who watches documentary explainers (economics, history) on a phone and a TV.",
  'R2': "You are a senior motion-graphics and 3D animation director who reviews explainer videos for broadcast quality.",
  'R3': "You are a documentary editor who checks whether on-screen text, numbers and images are clear, honest and readable on a small screen.",
}
Q27 = """{persona}

You will see {n} still frames (files F01.jpg … F{n:02d}.jpg in the current folder; open each with the Read tool) taken at random from a ~16-minute faceless documentary explainer about why America almost stopped building small apartment buildings (zoning maps, building-code stair rules, lending rules), rendered as stylised 3D scenes with data graphics. Judge only what you see. Be honest and specific; do not be polite.

For EACH frame score 1–10:
- craft: composition, lighting, materials, overall visual quality (10 = top-tier broadcast explainer, 5 = typical faceless YouTube explainer, 1 = broken)
- readability: can every word/number be read on a phone screen? (10 = effortless; mark 0 if there is no text)
- flags: list any of "broken_render", "missing_image", "text_overlap", "text_cut_off", "illegible_text", "cluttered", "empty_frame", "confusing", or [] if none.

Return ONLY JSON:
{{"frames": {{"F01": {{"craft": <int>, "readability": <int>, "flags": [..], "note": "<short>"}}, ...}},
 "overall_craft_1to10": <int>, "compared_to_typical_faceless_explainers": "below|similar|above|far_above",
 "best_frame": "Fxx", "worst_frame": "Fxx", "top3_visual_fixes": ["<concrete>", "<concrete>", "<concrete>"]}}"""
Q31 = """{persona}

You will check CONTINUITY of a ~16-minute documentary explainer about small apartment buildings and the rules that shape them without watching it. Files in the current folder (open each with the Read tool):
- J01.jpg … J{nj:02d}.jpg: one strip per join between sections; each strip has 6 frames left→right at −2.5, −1.5, −0.5, +0.5, +1.5, +2.5 s around the join. The narration around each join is in the list below.
- O1.jpg … O{no}.jpg: overview contact sheets, one frame every 8 seconds of the whole film, in order (left→right, top→bottom).

Narration around each join:
{words}

For each join decide: is it smooth / acceptable / a break (jarring change of look, picture that contradicts the words, text that jumps or disappears mid-sentence, visual style that suddenly changes)? Then judge the whole film from the overview sheets: does the look stay consistent? Is any single setting overused? Does the picture match a documentary about small apartment buildings, zoning, stairs and lending rules?

Return ONLY JSON:
{{"joins": {{"J01": {{"verdict": "smooth|acceptable|break", "why": "<short>"}}, ...}},
 "consistency_1to10": <int>, "variety_1to10": <int>, "picture_matches_words_1to10": <int>,
 "breaks": ["Jxx: <why>"], "overused_setting": "<name or empty>", "top3_fixes": ["<concrete>", "<concrete>", "<concrete>"]}}"""


Q31J = """{persona}

You will check CONTINUITY at ONE join between two sections of a ~16-minute documentary explainer about small apartment buildings and the rules that shape them, without watching it.
File in the current folder (open it with the Read tool): {jn}.jpg — one strip of 6 frames left→right at −2.5, −1.5, −0.5, +0.5, +1.5, +2.5 s around the join.
Narration around the join:
{words}

Decide: is this join smooth / acceptable / a break (jarring change of look, picture that contradicts the words, text that jumps or disappears mid-sentence, an empty card while the narration is already speaking)?

Return ONLY JSON:
{{"joins": {{"{jn}": {{"verdict": "smooth|acceptable|break", "why": "<short>"}}}}, "fix_if_any": "<concrete or empty>"}}"""


def run(prompt, tag, files):
    with ThreadPoolExecutor(3) as ex:
        res = dict(zip(RATERS, ex.map(lambda k: aicall(prompt.format(persona=RATERS[k], **FMT), f'{tag}-{k}', files), RATERS)))
    print(json.dumps({k: bool(v) for k, v in res.items()}), f'chi phí lũy kế tập ${spent():.2f} / trần ${CAP}')


FMT = {}
if __name__ == '__main__':
    mode, video = sys.argv[1], sys.argv[2]
    if mode == 'q27':
        n = int(sys.argv[sys.argv.index('--n') + 1]) if '--n' in sys.argv else 12; seed = int(sys.argv[sys.argv.index('--seed') + 1]) if '--seed' in sys.argv else 11
        D = os.path.join(OUT, 'q27'); os.makedirs(D, exist_ok=True); R = random.Random(seed); T = dur(video)
        ts = sorted(R.uniform(1, T - 1) for _ in range(n)); key = {}
        for i, t in enumerate(ts, 1): f = os.path.join(D, f'F{i:02d}.jpg'); grab(video, t, f); key[f'F{i:02d}'] = round(t, 2)
        json.dump(key, open(os.path.join(D, 'key.json'), 'w'), indent=1); FMT.update(n=n)
        run(Q27, 'q27', [os.path.join(D, f'F{i:02d}.jpg') for i in range(1, n + 1)])
    elif mode == 'q31j':   # chấm lại MỘT điểm nối (chủ dự án 12/10, D2): cùng vai, cùng dải 6 khung, cùng lời quanh điểm nối
        TL = json.load(open(sys.argv[3])); j = int(sys.argv[sys.argv.index('--join') + 1]); D = os.path.join(OUT, f'q31j{j:02d}'); os.makedirs(D, exist_ok=True); segs = TL['segments']
        sys.path.insert(0, os.path.join(HERE, '..', '..', 'scripts', 'll')); import ll
        def words(sg): return ll.words(json.load(open(os.path.join(ll.REPO, sg['vo_file'][:-4] + '.align.json')))) if sg.get('vo_file') else []
        a, b = segs[j - 1], segs[j]; c = b['t0']; tmp = tempfile.mkdtemp(); jn = f'J{j:02d}'
        for k, dt in enumerate([-2.5, -1.5, -0.5, 0.5, 1.5, 2.5]): grab(video, c + dt, f'{tmp}/{k}.jpg', 480)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{tmp}/%d.jpg', '-vf', 'tile=6x1:padding=6:color=white', '-frames:v', '1', '-q:v', '3', os.path.join(D, f'{jn}.jpg')], check=True)
        wa = ' '.join(w[3] for w in words(a) if a['vo_offset'] + w[1] > a['t1'] - a['t0'] - 6); wb = ' '.join(w[3] for w in words(b) if b['vo_offset'] + w[1] < 6)
        FMT.update(jn=jn, words=f'{jn}: …{wa} || {wb}…'); run(Q31J, f'q31j{j:02d}', [os.path.join(D, f'{jn}.jpg')])
    elif mode == 'q31':
        TL = json.load(open(sys.argv[3])); D = os.path.join(OUT, 'q31'); os.makedirs(D, exist_ok=True); segs = TL['segments']; lines = []
        sys.path.insert(0, os.path.join(HERE, '..', '..', 'scripts', 'll')); import ll
        def words(sg): return ll.words(json.load(open(os.path.join(ll.REPO, sg['vo_file'][:-4] + '.align.json')))) if sg.get('vo_file') else []
        for j, (a, b) in enumerate(zip(segs, segs[1:]), 1):
            c = b['t0']; tmp = tempfile.mkdtemp()
            for k, dt in enumerate([-2.5, -1.5, -0.5, 0.5, 1.5, 2.5]): grab(video, c + dt, f'{tmp}/{k}.jpg', 480)
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{tmp}/%d.jpg', '-vf', 'tile=6x1:padding=6:color=white', '-frames:v', '1', '-q:v', '3', os.path.join(D, f'J{j:02d}.jpg')], check=True)
            wa = ' '.join(w[3] for w in words(a) if a['vo_offset'] + w[1] > a['t1'] - a['t0'] - 6); wb = ' '.join(w[3] for w in words(b) if b['vo_offset'] + w[1] < 6)
            lines.append(f'J{j:02d}: …{wa} || {wb}…')
        T = dur(video); no = 0; per = 32
        for s in range(0, int(T // 8) + 1, per):
            no += 1; tmp = tempfile.mkdtemp()
            for k in range(per):
                t = (s + k) * 8 + 4
                if t < T - 1: grab(video, t, f'{tmp}/{k:03d}.jpg', 320)
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-pattern_type', 'glob', '-i', f'{tmp}/*.jpg', '-vf', 'tile=8x4:padding=4:color=white', '-frames:v', '1', '-q:v', '3', os.path.join(D, f'O{no}.jpg')], check=True)
        FMT.update(nj=len(segs) - 1, no=no, words='\n'.join(lines))
        run(Q31, 'q31', [os.path.join(D, f) for f in sorted(os.listdir(D)) if f.endswith('.jpg')])
