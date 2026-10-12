#!/opt/cine/bin/python
"""KÊNH 2 · chấm MÙ 4 shot mẫu k2v so với 4 khung Steel tương ứng (phiên V, 12/10/2026).
Cách làm giống channel-k2/k2g-ep01/blind_k2.py: `claude -p` ghim model claude-sonnet-5-5, không subagent, chỉ công cụ Read, thư mục tạm trống;
khoá ANTHROPIC_API_KEY lấy từ $CONSOLE_API_KEY trong môi trường tiến trình con (không in, không ghi). Trần API $15 (dừng ở $14). Chi phí: kiem-mu/cost.jsonl.
Mỗi cặp: 1 khung Steel 1080p (bản phát hành) + 1 khung shot mẫu 1080p ở mốc khai trước (không chọn tay sau khi xem), đặt tên X/Y theo thứ tự trộn
bằng hạt giống cố định; người chấm không biết khung nào cũ/mới, không thấy repo, chỉ đọc 2 ảnh. Thang tuyệt đối như Q27 G2 Steel (5 = video faceless thường).
  blind_v.py set      dựng bộ ảnh (kiem-mu/blind/P1..P4/{X,Y}.jpg + key.json)
  blind_v.py run      3 người chấm × 4 cặp (12 lần gọi)
  blind_v.py rejudge P2   vòng 2 cho một cặp sau một lượt sửa
  blind_v.py score    bảng trước/sau"""
import json, os, random, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'kiem-mu'); B = os.path.join(OUT, 'blind'); LOG = os.path.join(OUT, 'cost.jsonl')
CAP, STOP, MODEL = 15.0, 14.0, 'claude-sonnet-5-5'
STEEL = os.path.join(HERE, '..', 'k2g-ep01', 'kiem-mu', 'blind', 'q27')   # khung Steel đã trích từ master 1080p bản phát hành (1280 px, key.json = giây)
SH = '/var/tmp/cine-out/k2v-shots'
# (cặp, nhãn, khung Steel: tệp F## của bộ Q27 Steel (giây ở q27/key.json), khung mẫu: thư mục + giây — khai trước khi chấm)
PAIRS = [('P1', 'a map showing where steel and trade policy happen', 'F02', 'A-map-washington-brussels', 11.2),       # Steel F02 bản đồ tuyến Ngũ Đại Hồ  ↔ A bản đồ thật, khung Brussels + cột 50 %
         ('P2', 'a data graphic with steel numbers', 'F04', 'B-chart3d-steel-1950-2025', 8.6),       # Steel F04 thẻ cột trên nền mờ      ↔ B cột 3D tỷ lệ thật
         ('P3', 'a historical/official record: a person, a document or a timeline', 'F09', 'C-photo-carnegie-proclamation', 3.6), # Steel F09 thẻ mốc thời gian (hồ sơ) ↔ C chân dung LoC trong khung
         ('P4', 'a 3D scene of the steel industry', 'F12', 'D-cams-furnace-variants', 4.6)]         # Steel F12 cảnh port                 ↔ D cảnh furnace, preset mới
RATERS = {
  'R1': "You are a general YouTube viewer who watches documentary explainers (economics, history) on a phone and a TV.",
  'R2': "You are a senior motion-graphics and 3D animation director who reviews explainer videos for broadcast quality.",
  'R3': "You are a documentary editor who checks whether on-screen text, numbers and images are clear, honest and readable on a small screen.",
}
PROMPT = """{persona}

In the current folder there are two still frames, X.jpg and Y.jpg (open both with the Read tool). Both come from faceless documentary explainers about the steel industry and trade policy; they show the same kind of content ({kind}). Judge only what you see. Be honest and specific; do not be polite.

For EACH frame score 1–10:
- craft: composition, lighting, materials, overall visual quality (10 = top-tier broadcast explainer, 5 = typical faceless YouTube explainer, 1 = broken)
- readability: can every word/number be read on a phone screen? (0 if there is no text)
- clarity: how quickly a viewer understands what is shown (place, quantity, document or person)
- flags: any of "broken_render", "text_overlap", "text_cut_off", "illegible_text", "cluttered", "empty_frame", "flat_slide_look", "confusing", or [].

Return ONLY JSON:
{{"X": {{"craft": <int>, "readability": <int>, "clarity": <int>, "flags": [..], "note": "<short>"}},
 "Y": {{"craft": <int>, "readability": <int>, "clarity": <int>, "flags": [..], "note": "<short>"}},
 "better": "X|Y|tie", "why": "<one sentence>", "top_fix_for_weaker": "<concrete>"}}"""


def spent():
    return sum(json.loads(l)['usd'] for l in open(LOG)) if os.path.exists(LOG) else 0.0


def grab(v, t, out):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', v, '-frames:v', '1', '-vf', 'scale=1280:-2', '-q:v', '3', out], check=True)


def setup():
    R = random.Random(20261012); key = {}
    for pid, kind, ts, sd, tn in PAIRS:
        d = os.path.join(B, pid); os.makedirs(d, exist_ok=True); new = os.path.join(SH, sd, 'shot.mp4')
        old_is_x = R.random() < 0.5
        shutil.copy(os.path.join(STEEL, ts + '.jpg'), os.path.join(d, 'X.jpg' if old_is_x else 'Y.jpg')); grab(new, tn, os.path.join(d, 'Y.jpg' if old_is_x else 'X.jpg'))
        key[pid] = dict(kind=kind, steel='X' if old_is_x else 'Y', moi='Y' if old_is_x else 'X', steel_t=ts, moi_shot=sd, moi_t=tn)
    json.dump(key, open(os.path.join(B, 'key.json'), 'w'), indent=1); print(json.dumps(key, indent=1))


def call(pid, rk):
    if spent() > STOP: raise SystemExit(f'dừng: đã tiêu ${spent():.2f} (dừng ở ${STOP}, trần ${CAP})')
    key = json.load(open(os.path.join(B, 'key.json'))); prompt = PROMPT.format(persona=RATERS[rk], kind=key[pid]['kind'])
    env = dict(os.environ, ANTHROPIC_API_KEY=os.environ['CONSOLE_API_KEY'])
    with tempfile.TemporaryDirectory() as cwd:
        for f in ('X.jpg', 'Y.jpg'): shutil.copy(os.path.join(B, pid, f), cwd)
        for _ in range(2):
            r = subprocess.run(['claude', '-p', '--model', MODEL, '--output-format', 'json', '--allowedTools', 'Read'], input=prompt, capture_output=True, text=True, env=env, cwd=cwd, timeout=900)
            try: d = json.loads(r.stdout)
            except Exception: continue
            with open(LOG, 'a') as f: f.write(json.dumps({'tag': f'{pid}-{rk}', 'model': MODEL, 'served': sorted(d.get('modelUsage', {})), 'usd': d.get('total_cost_usd', 0)}) + '\n')
            open(os.path.join(B, pid, f'{rk}.raw.txt'), 'w').write(d.get('result', ''))
            m = re.search(r'\{.*\}', d.get('result', ''), re.S)
            if m:
                try: j = json.loads(m.group(0)); json.dump(j, open(os.path.join(B, pid, f'{rk}.json'), 'w'), indent=1); return True
                except Exception: pass
    return False


def run():
    jobs = [(p[0], rk) for p in PAIRS for rk in RATERS if not os.path.exists(os.path.join(B, p[0], f'{rk}.json'))]
    with ThreadPoolExecutor(3) as ex: res = list(ex.map(lambda a: call(*a), jobs))
    print(dict(zip([f'{a}-{b}' for a, b in jobs], res)), f'chi phí lũy kế ${spent():.2f}')


def rejudge(pid):
    """vòng 2 cho một cặp sau một lượt sửa: thư mục <pid>-v2, cùng thứ tự X/Y, cùng mốc, cùng đề bài"""
    key = json.load(open(os.path.join(B, 'key.json'))); k = dict(key[pid]); nid = pid + '-v2'; d = os.path.join(B, nid); os.makedirs(d, exist_ok=True)
    shutil.copy(os.path.join(B, pid, k['steel'] + '.jpg'), os.path.join(d, k['steel'] + '.jpg')); grab(os.path.join(SH, k['moi_shot'], 'shot.mp4'), k['moi_t'], os.path.join(d, k['moi'] + '.jpg'))
    key[nid] = k; json.dump(key, open(os.path.join(B, 'key.json'), 'w'), indent=1)
    with ThreadPoolExecutor(3) as ex: res = list(ex.map(lambda rk: call(nid, rk), RATERS))
    print(nid, res, f'chi phí lũy kế ${spent():.2f}')


def score():
    key = json.load(open(os.path.join(B, 'key.json'))); rows = []
    for pid in key:
        k = key[pid]; kind = k['kind']
        if not os.path.isdir(os.path.join(B, pid)): continue
        k = key[pid]; S = {'steel': [], 'moi': []}; better = []; notes = []
        for rk in RATERS:
            f = os.path.join(B, pid, f'{rk}.json')
            if not os.path.exists(f): continue
            j = json.load(open(f))
            for side in ('steel', 'moi'): S[side].append(j[k[side]])
            better.append('mới' if j['better'] == k['moi'] else 'Steel' if j['better'] == k['steel'] else 'hoà'); notes.append(f"{rk}: {j.get('why', '')}")
        av = lambda L, c: round(sum(x[c] for x in L) / max(1, len(L)), 2)
        rows.append(dict(cap=pid, loai=kind, n=len(S['moi']), craft_steel=av(S['steel'], 'craft'), craft_moi=av(S['moi'], 'craft'), read_steel=av(S['steel'], 'readability'), read_moi=av(S['moi'], 'readability'),
                         clar_steel=av(S['steel'], 'clarity'), clar_moi=av(S['moi'], 'clarity'), hon=better, co_steel=sorted({x for s in S['steel'] for x in s['flags']}), co_moi=sorted({x for s in S['moi'] for x in s['flags']}), ly_do=notes))
    json.dump(rows, open(os.path.join(OUT, 'blind-score.json'), 'w'), indent=1, ensure_ascii=False)
    for r in rows: print(json.dumps(r, ensure_ascii=False))
    print(f'chi phí ${spent():.2f} / trần ${CAP}')


if __name__ == '__main__':
    if sys.argv[1] == 'rejudge': rejudge(sys.argv[2])
    else: {'set': setup, 'run': run, 'score': score}[sys.argv[1]]()
