#!/opt/cine/bin/python
"""V5b-2c · CHẤM MÙ BẢN ĐỒ CHIẾN LƯỢC (giao thức blind_g2/blind_v5b2b): `claude -p` GHIM claude-sonnet-5-5, chỉ công cụ Read, thư mục tạm trống chỉ chứa ảnh,
3 vai RATERS nạp nguyên văn từ channel-k2/k2v2-mau/blind_v2.py, thang craft tuyệt đối như blind_v2 (5 = video faceless thường).
Bản đồ là CHUYỂN ĐỘNG 7 s → mỗi phiên bản = 4 khung theo thứ tự thời gian (X1..X4 / Y1..Y4, 1280 px), không phải 1 khung.
  SM2 (cặp, ẩn nhãn phiên bản): M13-lite (đoạn a 0–6,5 s) ↔ DỰ PHÒNG NC-BD §2.4 (đoạn b), cùng nội dung, cùng máy; X/Y theo hạt giống 20261018.
  SM3 (đơn, chỉ ĐỘ RÕ — lệnh E-SM3 "chấm mù độ rõ riêng"): 4 khung của bản 7 s.
Độ rõ = trả lời 4 câu "đến từ đâu · qua đường nào · khi nào · ở đâu trên bản đồ" CHỈ từ ảnh; chấm đúng/sai bằng ĐÁP ÁN KHAI TRƯỚC (KEYS dưới đây, theo routes.geojson
gói TUYẾN) — so khớp từ khoá, ghi nguyên câu trả lời để chủ dự án đọc lại. Sổ chi phí reports/v5b2c/kiem-mu/cost.jsonl; trần $3, dừng $2,7.
  blind_v5b2c.py set <master.mp4> <sm3.mp4> · blind_v5b2c.py run · blind_v5b2c.py score"""
import importlib.util, json, os, random, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
OUT = os.path.join(HERE, 'kiem-mu'); LOG = os.path.join(OUT, 'cost.jsonl')
spec = importlib.util.spec_from_file_location('bv2', os.path.join(REPO, 'channel-k2', 'k2v2-mau', 'blind_v2.py')); BV2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(BV2)
RATERS, MODEL = BV2.RATERS, BV2.MODEL
assert MODEL == 'claude-sonnet-5-5'
CAP, STOP = 3.0, 2.7
# khai TRƯỚC khi chấm (giây trong master v5b2c-t / video SM3)
T_A = [1.6, 3.6, 5.3, 6.3]; T_B = [24.5 + t for t in T_A]; T_SM3 = [0.8, 2.0, 4.0, 6.2]
# mô tả TRUNG TÍNH: không lộ đáp án câu độ rõ (ai/đâu/khi nào)
KIND = {'SM2': 'an animated historical strategic map from a documentary', 'SM3': 'an animated historical strategic map from a documentary'}
# đáp án khai trước: mỗi câu đúng khi câu trả lời chứa ÍT NHẤT một từ khoá của mỗi nhóm (nhóm = list)
KEYS = {'SM2': dict(from_=[['england', 'britain', 'british isles', 'uk', 'spithead', 'portsmouth', 'english channel', 'north']],
                    route=[['atlantic', 'portugal', 'iberia', 'west coast', 'cape st', 'along the coast', 'south']],
                    when=[['1780', '1781', '1782']],
                    where=[['gibraltar']]),
        'SM3': dict(from_=[['gibraltar']],
                    route=[['casablanca', 'morocco', 'london', 'madeira', 'jamaica', 'oran', 'algiers', 'north africa']],
                    when=[['1940'], ['1942']],
                    where=[['gibraltar', 'strait', 'southern tip', 'south of spain', 'iberia']])}
PROMPT_PAIR = """{persona}

In the current folder there are eight still frames from two versions of the same short animated map ({kind}): X1.jpg–X4.jpg are version X and Y1.jpg–Y4.jpg are version Y, each in time order over about 7 seconds. Open all eight with the Read tool. Judge only what you see. Be honest and specific; do not be polite.

For EACH version score 1–10:
- craft: composition, cartography, lighting, overall visual quality (10 = top-tier broadcast explainer, 5 = typical faceless YouTube explainer, 1 = broken)
- readability: can every word/number be read on a phone screen?
- clarity: how quickly a viewer understands who moves, from where, by which route, when, and where the destination is on the map
- flags: any of "broken_render", "text_overlap", "text_cut_off", "illegible_text", "cluttered", "empty_frame", "flat_slide_look", "confusing", or [].
Then, using ONLY what version X shows, answer in a few words: where do the moving forces come FROM, which ROUTE do they take, WHEN does it happen, and WHERE on the map is the destination. Do the same for version Y. Write "unclear" if the frames do not tell you.

Return ONLY JSON:
{{"X": {{"craft": <int>, "readability": <int>, "clarity": <int>, "flags": [..], "from": "<..>", "route": "<..>", "when": "<..>", "where": "<..>", "note": "<short>"}},
 "Y": {{"craft": <int>, "readability": <int>, "clarity": <int>, "flags": [..], "from": "<..>", "route": "<..>", "when": "<..>", "where": "<..>", "note": "<short>"}},
 "better": "X|Y|tie", "why": "<one sentence>", "top_fix_for_weaker": "<concrete>"}}"""
PROMPT_ONE = """{persona}

In the current folder there are four still frames from one short animated map ({kind}): X1.jpg–X4.jpg, in time order over about 7 seconds. Open all four with the Read tool. Judge only what you see. Be honest and specific; do not be polite.

Score 1–10:
- craft: composition, cartography, lighting, overall visual quality (10 = top-tier broadcast explainer, 5 = typical faceless YouTube explainer, 1 = broken)
- readability: can every word/number be read on a phone screen?
- clarity: how quickly a viewer understands who moves, from where, by which route, when, and where things are on the map
- flags: any of "broken_render", "text_overlap", "text_cut_off", "illegible_text", "cluttered", "empty_frame", "flat_slide_look", "confusing", "too_many_things_at_once", or [].
Then, using ONLY what the frames show, answer in a few words: where do the moving people/forces come FROM, which ROUTES/destinations, WHEN (all dates you can read), and WHERE on the map the starting place is.
Finally say whether the two periods shown would be clearer as two separate shots ("split": true/false) and why.

Return ONLY JSON:
{{"X": {{"craft": <int>, "readability": <int>, "clarity": <int>, "flags": [..], "from": "<..>", "route": "<..>", "when": "<..>", "where": "<..>", "note": "<short>"}},
 "split": <bool>, "why_split": "<one sentence>", "top_fix": "<concrete>"}}"""


def spent():
    return sum(json.loads(l)['usd'] for l in open(LOG)) if os.path.exists(LOG) else 0.0


def grab(v, t, out):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', v, '-frames:v', '1', '-vf', 'scale=1280:-2', '-q:v', '3', out], check=True)


def setup(master, sm3):
    os.makedirs(OUT, exist_ok=True); R = random.Random(20261018); key = {}
    m13_is_x = R.random() < 0.5; d = os.path.join(OUT, 'SM2'); os.makedirs(d, exist_ok=True)
    for i, (ta, tb) in enumerate(zip(T_A, T_B), 1):
        grab(master, ta, os.path.join(d, f"{'X' if m13_is_x else 'Y'}{i}.jpg")); grab(master, tb, os.path.join(d, f"{'Y' if m13_is_x else 'X'}{i}.jpg"))
    key['SM2'] = dict(kind=KIND['SM2'], m13='X' if m13_is_x else 'Y', du_phong='Y' if m13_is_x else 'X', t_m13=T_A, t_du_phong=T_B)
    d = os.path.join(OUT, 'SM3'); os.makedirs(d, exist_ok=True)
    for i, t in enumerate(T_SM3, 1): grab(sm3, t, os.path.join(d, f'X{i}.jpg'))
    key['SM3'] = dict(kind=KIND['SM3'], t=T_SM3)
    json.dump(key, open(os.path.join(OUT, 'key.json'), 'w'), indent=1); print(json.dumps(key, indent=1))


def call(pid, rk):
    if spent() > STOP: raise SystemExit(f'dừng: đã tiêu ${spent():.2f}')
    key = json.load(open(os.path.join(OUT, 'key.json'))); P = PROMPT_PAIR if pid == 'SM2' else PROMPT_ONE
    prompt = P.format(persona=RATERS[rk], kind=key[pid]['kind'])
    env = dict(os.environ, ANTHROPIC_API_KEY=os.environ['CONSOLE_API_KEY'])
    with tempfile.TemporaryDirectory() as cwd:
        for f in sorted(os.listdir(os.path.join(OUT, pid))):
            if re.fullmatch(r'[XY]\d\.jpg', f): shutil.copy(os.path.join(OUT, pid, f), cwd)
        for _ in range(2):
            r = subprocess.run(['claude', '-p', '--model', MODEL, '--output-format', 'json', '--allowedTools', 'Read'], input=prompt, capture_output=True, text=True, env=env, cwd=cwd, timeout=900)
            try: d = json.loads(r.stdout)
            except Exception: continue
            with open(LOG, 'a') as f: f.write(json.dumps({'tag': f'v5b2c:{pid}-{rk}', 'model': MODEL, 'served': sorted(d.get('modelUsage', {})), 'usd_by_model': {m: round(u.get('costUSD', 0), 5) for m, u in d.get('modelUsage', {}).items()}, 'usd': d.get('total_cost_usd', 0)}) + '\n')
            open(os.path.join(OUT, pid, f'{rk}.raw.txt'), 'w').write(d.get('result', ''))
            m = re.search(r'\{.*\}', d.get('result', ''), re.S)
            if m:
                try: j = json.loads(m.group(0)); json.dump(j, open(os.path.join(OUT, pid, f'{rk}.json'), 'w'), indent=1); return True
                except Exception: pass
    return False


def run():
    key = json.load(open(os.path.join(OUT, 'key.json')))
    jobs = [(p, rk) for p in key for rk in RATERS if not os.path.exists(os.path.join(OUT, p, f'{rk}.json'))]
    with ThreadPoolExecutor(3) as ex: res = list(ex.map(lambda a: call(*a), jobs))
    print(dict(zip([f'{a}-{b}' for a, b in jobs], res)), f'chi phí ${spent():.2f} / trần ${CAP}')


def right(pid, v):
    """số câu đúng /4 theo đáp án khai trước"""
    ok = {}
    for q, groups in KEYS[pid].items():
        s = str(v.get(q.rstrip('_'), '')).lower(); ok[q.rstrip('_')] = all(any(k in s for k in g) for g in groups)
    return ok


def score():
    key = json.load(open(os.path.join(OUT, 'key.json'))); R = {}
    J = {rk: json.load(open(os.path.join(OUT, 'SM2', f'{rk}.json'))) for rk in RATERS if os.path.exists(os.path.join(OUT, 'SM2', f'{rk}.json'))}
    k = key['SM2']; row = dict(nguoi=len(J))
    for lab, v in (('m13', k['m13']), ('du_phong', k['du_phong'])):
        row[lab] = dict(craft=[J[r][v]['craft'] for r in J], readability=[J[r][v]['readability'] for r in J], clarity=[J[r][v]['clarity'] for r in J],
                        dung=[right('SM2', J[r][v]) for r in J], tra_loi=[{q: J[r][v].get(q) for q in ('from', 'route', 'when', 'where')} for r in J],
                        flags=sorted({f for r in J for f in J[r][v].get('flags', [])}))
        for m in ('craft', 'readability', 'clarity'): row[lab]['tb_' + m] = round(sum(row[lab][m]) / max(1, len(J)), 2)
        row[lab]['dung_tong'] = f"{sum(sum(d.values()) for d in row[lab]['dung'])}/{4 * len(J)}"
    row['chon_m13'] = f"{sum(1 for r in J if J[r].get('better') == k['m13'])}/{len(J)}"; row['why'] = [J[r].get('why') for r in J]; row['sua_yeu_hon'] = [J[r].get('top_fix_for_weaker') for r in J]
    R['SM2'] = row
    J = {rk: json.load(open(os.path.join(OUT, 'SM3', f'{rk}.json'))) for rk in RATERS if os.path.exists(os.path.join(OUT, 'SM3', f'{rk}.json'))}
    R['SM3'] = dict(nguoi=len(J), craft=[J[r]['X']['craft'] for r in J], clarity=[J[r]['X']['clarity'] for r in J], readability=[J[r]['X']['readability'] for r in J],
                    dung=[right('SM3', J[r]['X']) for r in J], tra_loi=[{q: J[r]['X'].get(q) for q in ('from', 'route', 'when', 'where')} for r in J],
                    flags=sorted({f for r in J for f in J[r]['X'].get('flags', [])}), tach=[J[r].get('split') for r in J], why_split=[J[r].get('why_split') for r in J], top_fix=[J[r].get('top_fix') for r in J])
    R['chi_phi'] = round(spent(), 3)
    json.dump(R, open(os.path.join(OUT, 'score.json'), 'w'), indent=1, ensure_ascii=False); print(json.dumps(R, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    a = sys.argv[1]
    if a == 'set': setup(sys.argv[2], sys.argv[3])
    elif a == 'run': run()
    elif a == 'score': score()
