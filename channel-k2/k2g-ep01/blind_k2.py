#!/opt/cine/bin/python
"""K2G-01 G2 · chấm hình mù (Q27) và xem liền mạch mù (Q31) MỘT LẦN trên bản 1080p (chủ dự án 11/10). `claude -p` ghim model, không subagent
(qua ai.py: khoá lấy từ $CONSOLE_API_KEY trong tiến trình con, không in; chi phí ghi kiem-mu/$K2_COST, trần $K2_CAP).
Khác giao thức LL (K: subagent so với tập 1): kênh 2 chưa có tập tham chiếu → chấm tuyệt đối theo thang mô tả + cờ lỗi; ghi rõ ở báo cáo.
  blind_k2.py q27 <master.mp4> [--n 12] [--seed 11]      12 khung ngẫu nhiên (tránh 1 s đầu/cuối), 1280×720, tên ẩn F01…
  blind_k2.py q31 <master.mp4> <timeline.json>            mỗi điểm nối đoạn: dải 6 khung (−2,5…+2,5 s) + lời quanh điểm nối; thêm 4 tấm tổng quan 1 khung/8 s
Người chấm chỉ nhận ảnh + lời (Q31), không nhận đặc tả, mã, hay kịch bản."""
import json, os, random, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ai  # noqa: E402

OUT = os.path.join(ai.OUT, 'blind'); os.makedirs(OUT, exist_ok=True)
dur = lambda v: float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', v], capture_output=True, text=True).stdout)
def grab(v, t, out, w=1280): subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', v, '-frames:v', '1', '-vf', f'scale={w}:-2', '-q:v', '3', out], check=True)

RATERS = {
  'R1': "You are a general YouTube viewer who watches documentary explainers (economics, history) on a phone and a TV.",
  'R2': "You are a senior motion-graphics and 3D animation director who reviews explainer videos for broadcast quality.",
  'R3': "You are a documentary editor who checks whether on-screen text, numbers and images are clear, honest and readable on a small screen.",
}
Q27 = """{persona}

You will see {n} still frames (files F01.jpg … F{n:02d}.jpg in the current folder; open each with the Read tool) taken at random from a ~17-minute faceless documentary explainer about the steel industry, rendered as stylised 3D scenes with data graphics. Judge only what you see. Be honest and specific; do not be polite.

For EACH frame score 1–10:
- craft: composition, lighting, materials, overall visual quality (10 = top-tier broadcast explainer, 5 = typical faceless YouTube explainer, 1 = broken)
- readability: can every word/number be read on a phone screen? (10 = effortless; mark 0 if there is no text)
- flags: list any of "broken_render", "missing_image", "text_overlap", "text_cut_off", "illegible_text", "cluttered", "empty_frame", "confusing", or [] if none.

Return ONLY JSON:
{{"frames": {{"F01": {{"craft": <int>, "readability": <int>, "flags": [..], "note": "<short>"}}, ...}},
 "overall_craft_1to10": <int>, "compared_to_typical_faceless_explainers": "below|similar|above|far_above",
 "best_frame": "Fxx", "worst_frame": "Fxx", "top3_visual_fixes": ["<concrete>", "<concrete>", "<concrete>"]}}"""
Q31 = """{persona}

You will check CONTINUITY of a ~17-minute documentary explainer about steel without watching it. Files in the current folder (open each with the Read tool):
- J01.jpg … J{nj:02d}.jpg: one strip per join between sections; each strip has 6 frames left→right at −2.5, −1.5, −0.5, +0.5, +1.5, +2.5 s around the join. The narration around each join is in the list below.
- O1.jpg … O{no}.jpg: overview contact sheets, one frame every 8 seconds of the whole film, in order (left→right, top→bottom).

Narration around each join:
{words}

For each join decide: is it smooth / acceptable / a break (jarring change of look, picture that contradicts the words, text that jumps or disappears mid-sentence, visual style that suddenly changes)? Then judge the whole film from the overview sheets: does the look stay consistent? Is any single setting overused? Does the picture match a documentary about steel, tariffs and carbon?

Return ONLY JSON:
{{"joins": {{"J01": {{"verdict": "smooth|acceptable|break", "why": "<short>"}}, ...}},
 "consistency_1to10": <int>, "variety_1to10": <int>, "picture_matches_words_1to10": <int>,
 "breaks": ["Jxx: <why>"], "overused_setting": "<name or empty>", "top3_fixes": ["<concrete>", "<concrete>", "<concrete>"]}}"""


def run(prompt, tag, files):
    with ThreadPoolExecutor(3) as ex:
        res = dict(zip(RATERS, ex.map(lambda k: ai.ai(prompt.format(persona=RATERS[k], **FMT), f'{tag}-{k}', 'claude-sonnet-5-5', files), RATERS)))
    print(json.dumps({k: bool(v) for k, v in res.items()}), f'chi phí lũy kế ${ai.spent():.2f}')


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
    elif mode == 'q31':
        TL = json.load(open(sys.argv[3])); D = os.path.join(OUT, 'q31'); os.makedirs(D, exist_ok=True); segs = TL['segments']; lines = []
        sys.path.insert(0, os.path.join(ai.HERE.parent.parent, 'scripts', 'll')); import ll
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
