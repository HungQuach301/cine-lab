#!/opt/cine/bin/python
"""KÊNH 2 · chấm MÙ cuộn mẫu K2V2 so với khung T1 (K2C-T1-06 bản phát hành) cùng loại (phiên V2, 14/10/2026).
Giao thức như k2v-mau/blind_v.py (phiên V) và k2c-t1-06/blind_g2.py: `claude -p` GHIM model claude-sonnet-5-5, không subagent, chỉ công cụ Read,
thư mục tạm trống; khoá ANTHROPIC_API_KEY lấy từ $CONSOLE_API_KEY trong môi trường tiến trình con (không in, không ghi).
Trần API phiên V2 $10 (dừng ở $9). Chi phí: kiem-mu/cost.jsonl (model yêu cầu + model thực chạy theo modelUsage).
Cặp + mốc KHAI TRƯỚC khi dựng 1080p (không chọn tay sau khi xem):
  khung T1 = master 1080p release-k2c-t1-06-v1 (SHA 4f2d280b…) ở giây của bộ Q27 G2 (k2c-t1-06/kiem-mu/blind-g2/q27/key.json);
  khung mới = shot.mp4 1080p của cuộn K2V2 ở giây khai dưới đây. Tên X/Y trộn bằng hạt giống cố định. Thang tuyệt đối (5 = video faceless thường).
  blind_v2.py set <master_t1.mp4>   ·   blind_v2.py run   ·   blind_v2.py score
  blind_v2.py rejudge3 [P1 …]  vòng 3 (V2b), thư mục <cặp>-v3
  blind_v2.py rejudge4 [P1 …]  vòng 4 (V3, 14/10): cùng giao thức/cặp/khung T1/X-Y/mốc giây, thư mục <cặp>-v4; trần V3 $4 tính từ mức đã tiêu trước V3 ($2,708), dừng ở $3,6
  blind_v2.py rejudge [P1 …]   vòng 2 sau MỘT lượt sửa: thư mục <cặp>-v2, cùng khung T1, cùng thứ tự X/Y, cùng mốc giây, cùng đề bài (khung mới trích từ shot.mp4 mới)"""
import json, os, random, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'kiem-mu'); B = os.path.join(OUT, 'blind'); LOG = os.path.join(OUT, 'cost.jsonl')
CAP, STOP, MODEL = 10.0, 9.0, 'claude-sonnet-5-5'
V3_BASE = 2.708   # chi phí lũy kế khi bắt đầu V3
NEW = '/var/tmp/cine-out/k2v-shots/K2V2-reel/shot.mp4'
T1KEY = os.path.join(HERE, '..', 'k2c-t1-06', 'kiem-mu', 'blind-g2', 'q27', 'key.json')
# (cặp, loại nội dung chung, khung T1 (F## bộ Q27 G2), giây khung mới trong cuộn — đoạn H 0–15, J 15–25, N 25–33, P 33–38, S 38–44)
PAIRS = [('P1', 'a terrain map that sets up the story (where it happens)', 'F08', 13.0),        # T1 F08 bản đồ địa hình + callout Minneapolis ↔ hook: sepia, vùng nổi, tuyến, vòng sáng
         ('P2', 'a map showing a route or movement across a region', 'F12', 21.0),         # T1 F12 địa cầu + callout Texas ↔ hành trình sticker theo tuyến
         ('P3', 'numbers shown as 3D objects in a scene', 'F03', 31.0),                   # T1 F03 khối 13 % ↔ chồng xu tỷ lệ thật trên bản đồ
         ('P4', 'a historical portrait or archival image with a caption', 'F01', 36.0),   # T1 F01 ảnh lưu trữ trên bàn ↔ chân dung Ken Burns
         ('P5', 'a summary / comparison screen', 'F09', 42.5)]                            # T1 F09 thẻ TO RECAP ↔ bảng điểm hai phía
RATERS = {
  'R1': "You are a general YouTube viewer who watches documentary explainers (economics, history) on a phone and a TV.",
  'R2': "You are a senior motion-graphics and 3D animation director who reviews explainer videos for broadcast quality.",
  'R3': "You are a documentary editor who checks whether on-screen text, numbers and images are clear, honest and readable on a small screen.",
}
PROMPT = """{persona}

In the current folder there are two still frames, X.jpg and Y.jpg (open both with the Read tool). Both come from faceless documentary explainers about economics and history (the two videos are about different topics); they show the same kind of content ({kind}). Judge only what you see. Be honest and specific; do not be polite.

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


def setup(master):
    R = random.Random(20261014); key = {}; K1 = json.load(open(T1KEY))
    for pid, kind, f, tn in PAIRS:
        d = os.path.join(B, pid); os.makedirs(d, exist_ok=True); old_is_x = R.random() < 0.5
        grab(master, K1[f], os.path.join(d, 'X.jpg' if old_is_x else 'Y.jpg')); grab(NEW, tn, os.path.join(d, 'Y.jpg' if old_is_x else 'X.jpg'))
        key[pid] = dict(kind=kind, t1='X' if old_is_x else 'Y', moi='Y' if old_is_x else 'X', t1_frame=f, t1_s=K1[f], moi_s=tn)
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


def run(only=None):
    jobs = [(p[0], rk) for p in PAIRS for rk in RATERS if (not only or p[0] in only) and not os.path.exists(os.path.join(B, p[0], f'{rk}.json'))]
    with ThreadPoolExecutor(3) as ex: res = list(ex.map(lambda a: call(*a), jobs))
    print(dict(zip([f'{a}-{b}' for a, b in jobs], res)), f'chi phí lũy kế ${spent():.2f} / trần ${CAP}')


def rejudge(only=None, suf='v2'):
    key = json.load(open(os.path.join(B, 'key.json')))
    for pid in [p[0] for p in PAIRS if not only or p[0] in only]:
        k = dict(key[pid]); nid = f'{pid}-{suf}'; d = os.path.join(B, nid); os.makedirs(d, exist_ok=True)
        shutil.copy(os.path.join(B, pid, k['t1'] + '.jpg'), os.path.join(d, k['t1'] + '.jpg')); grab(NEW, k['moi_s'], os.path.join(d, k['moi'] + '.jpg')); key[nid] = k
    json.dump(key, open(os.path.join(B, 'key.json'), 'w'), indent=1)
    jobs = [(n, rk) for n in key if n.endswith('-' + suf) and (not only or n.rsplit('-', 1)[0] in only) for rk in RATERS if not os.path.exists(os.path.join(B, n, f'{rk}.json'))]
    with ThreadPoolExecutor(3) as ex: res = list(ex.map(lambda a: call(*a), jobs))
    print(dict(zip([f'{a}-{b}' for a, b in jobs], res)), f'chi phí lũy kế ${spent():.2f} / trần ${CAP}')


def score():
    key = json.load(open(os.path.join(B, 'key.json'))); rows = []
    for pid, k in key.items():
        S = {'t1': [], 'moi': []}; better = []; notes = []; fixes = []
        for rk in RATERS:
            f = os.path.join(B, pid, f'{rk}.json')
            if not os.path.exists(f): continue
            j = json.load(open(f))
            for side in ('t1', 'moi'): S[side].append(j[k[side]])
            better.append('mới' if j['better'] == k['moi'] else 'T1' if j['better'] == k['t1'] else 'hoà'); notes.append(f"{rk}: {j.get('why', '')}")
            if j['better'] != k['moi']: fixes.append(f"{rk} (mới yếu hơn): {j.get('top_fix_for_weaker', '')}")
            else: fixes.append(f"{rk} (ghi chú mới): {j[k['moi']].get('note', '')}")
        av = lambda L, c: round(sum(x[c] for x in L) / max(1, len(L)), 2)
        rows.append(dict(cap=pid, loai=k['kind'], t1=k['t1_frame'], moi_s=k['moi_s'], n=len(S['moi']), craft_t1=av(S['t1'], 'craft'), craft_moi=av(S['moi'], 'craft'), read_t1=av(S['t1'], 'readability'), read_moi=av(S['moi'], 'readability'),
                         clar_t1=av(S['t1'], 'clarity'), clar_moi=av(S['moi'], 'clarity'), hon=better, co_t1=sorted({x for s in S['t1'] for x in s['flags']}), co_moi=sorted({x for s in S['moi'] for x in s['flags']}),
                         craft_moi_tung_nguoi=[x['craft'] for x in S['moi']], ly_do=notes, goi_y=fixes))
    json.dump(rows, open(os.path.join(OUT, 'blind-score.json'), 'w'), indent=1, ensure_ascii=False)
    for r in rows: print(json.dumps({k: v for k, v in r.items() if k not in ('ly_do', 'goi_y')}, ensure_ascii=False))
    print(f'chi phí ${spent():.2f} / trần ${CAP}')


if __name__ == '__main__':
    a = sys.argv[1]
    if a == 'set': setup(sys.argv[2])
    elif a == 'run': run(sys.argv[2:] or None)
    elif a == 'rejudge': rejudge(sys.argv[2:] or None)
    elif a == 'rejudge4':   # V3: vòng 4 — trần riêng $4 trên mức lũy kế trước V3
        STOP = min(STOP, V3_BASE + 3.6); rejudge(sys.argv[2:] or None, 'v4')
    elif a == 'rejudge3': rejudge(sys.argv[2:] or None, 'v3')   # V2b: vòng 3 (cùng cặp, cùng khung T1, cùng X/Y, cùng mốc giây — khai trước 1080p)
    else: score()
