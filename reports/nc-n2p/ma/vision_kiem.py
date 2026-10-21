#!/opt/cine/bin/python -I
"""NC-N2P · bộ kiểm (ii)+(iv)+(i-b) bằng HAI MÔ HÌNH NHÌN KHÁC NHAU: OpenAI gpt-6.1-sol (Responses API, stream) và Claude claude-sonnet-5-5 (`claude -p`, chỉ công cụ Read,
thư mục tạm, khoá CONSOLE_API_KEY qua biến môi trường của tiến trình con — không in/ghi). Cả hai nhận CÙNG đề bài + cùng ảnh: TRƯỚC (render của ta) và SAU (khung AI đã ghép
lớp (a)), mỗi ảnh toàn khung 1568×882 + 4 ô phần tư phóng 1,5×. Đề bài hỏi danh mục VẬT THÊM / BỚT / ĐỔI có hộp toạ độ, loại theo danh sách cố định, cờ lỗi thời đại
theo danh sách CẤM (cam_thoi_dai.json) và năm khung. Máy (kiem_n2p.py) mới là bên kết luận (luật theo loại + vị trí); mô hình chỉ liệt kê.
Chi phí: OpenAI theo usage × giá developers.openai.com (21/10/2026: gpt-6.1-sol $2/M vào, $10/M ra); Claude theo total_cost_usd → reports/nc-n2p/cost.jsonl.
Chặn an toàn: OpenAI tổng sổ ≥ $20, Claude ≥ $25 → từ chối.
  vision_kiem.py --truoc <render.jpg> --sau <ghep.jpg> --nam 1780 --noi "Gibraltar" --tag <nhãn> --out <thư mục> [--mo-hinh gpt,claude] [--anh-tinh 1]"""
import argparse, base64, json, os, re, shutil, subprocess, sys, tempfile, time, urllib.request
from pathlib import Path
import cv2
sys.path.insert(0, str(Path(__file__).resolve().parent))
import n2p_lib as L  # noqa: E402

COST = L.N2P / 'cost.jsonl'
GPT = 'gpt-6.1-sol'; CLAUDE = 'claude-sonnet-5-5'
LOAI = {
 'co': 'flag, banner or ensign', 'cong_trinh': 'building, house, tower, steeple, church, hut, wall, gate, pier, mole, quay, bridge, road or paved street',
 'cong_su': 'fortification, bastion, battery, trench, cannon or gun', 'tau_lon': 'ship (sea-going sailing vessel, any ship larger than a rowing boat)', 'chu': 'text, letters, numbers, sign, logo, watermark',
 'den': 'lamp or artificial light source', 'lua_lon': 'large fire or burning building', 'leu': 'tent, awning or temporary shelter', 'do_dac': 'goods, barrels, crates, sacks, furniture, heaps, timber or stone piles',
 'xe_dung': 'cart or carriage standing without animals or people', 'rom': 'haystack or hay rick', 'vuon': 'garden plot, field, terrace, hedge', 'cay': 'tree, bush, scrub, grass', 'da_dat': 'rocks, sand, soil, cliff texture',
 'nguoi': 'person or people', 'dong_vat': 'animal (horse, cattle, dog …)', 'chim': 'bird', 'thuyen_nho': 'small boat, rowing boat, barge or lighter', 'xe_chay': 'cart, carriage or vehicle with animals or in motion',
 'khoi': 'smoke, steam or dust plume', 'lua_trai': 'campfire, cooking fire or small flame', 'phoi': 'laundry or cloth hung to dry', 'may_bay': 'aircraft', 'xe_may': 'motor vehicle', 'khac': 'anything else'}
PROMPT = """You are a strict inspector for a historical documentary that uses AI image editing under the rule "N2+". The scene depicts {noi} in the year {nam}.
Read ALL the image files below with the Read tool before answering (paths are absolute):
BEFORE = our own 3D render (the ground truth of what exists):
{truoc}
AFTER = the AI-edited version of the same frame (same camera):
{sau}
The quarter images are 1.5x enlargements: q1 top-left, q2 top-right, q3 bottom-left, q4 bottom-right of the full frame.

Task 1 — list EVERY visible object or feature that is ADDED in AFTER (not present in BEFORE), and every object that is REMOVED, MOVED or CHANGED IN KIND between BEFORE and AFTER \
(for example a ship changed into a different ship, a flag changed, a building given a new tower). Ignore pure changes of texture, colour grading, haze, cloud shapes and water ripples. \
Small objects matter: look at the enlarged quarters.
Task 2 — for each listed item decide whether it is an ANACHRONISM for the year {nam}, using this list of forbidden things (and your own knowledge):
{cam}
Task 3 — report any place where LAND became WATER or WATER became LAND (coastline moved, sea turned to sand, field turned to lake).

Use ONLY these category keys for "loai": {loai}
Give each item's bounding box in FULL-frame normalized coordinates [x0, y0, x1, y1] (0-1, origin top-left); convert from quarter images (full = quarter offset + 0.5 x quarter coordinate).
Answer with ONLY one JSON object, no other text:
{{"them": [{{"loai": "<key>", "mo_ta": "<what>", "toa_do": [x0, y0, x1, y1], "thoi_dai_sai": true|false, "ly_do_thoi_dai": "<why or empty>", "nam_xuat_hien": <year or null>, "do_tin": <0-1>}}],
 "bot_doi": [{{"loai": "<key>", "mo_ta": "<what was removed/moved/changed>", "toa_do": [x0, y0, x1, y1], "do_tin": <0-1>}}],
 "doi_loai_vung": [{{"mo_ta": "<land->water or water->land, where>", "toa_do": [x0, y0, x1, y1], "do_tin": <0-1>}}]}}"""


def spent(model_prefix):
    if not COST.exists(): return 0.0
    return sum(json.loads(l)['usd'] for l in COST.read_text().splitlines() if l.strip() and json.loads(l)['model'].startswith(model_prefix))


def log_cost(rec):
    COST.parent.mkdir(parents=True, exist_ok=True)
    with open(COST, 'a') as f: f.write(json.dumps(rec, ensure_ascii=False) + '\n')


def tiles(img, d, pre):
    im = cv2.imread(str(img)); im = cv2.resize(im, (1920, 1080), interpolation=cv2.INTER_AREA); q = [cv2.IMWRITE_JPEG_QUALITY, 92]; out = []
    p = d / f'{pre}_full.jpg'; cv2.imwrite(str(p), cv2.resize(im, (1568, 882), interpolation=cv2.INTER_AREA), q); out.append(p)
    for i, (ox, oy) in enumerate(((0, 0), (960, 0), (0, 540), (960, 540))):
        p = d / f'{pre}_q{i + 1}.jpg'; cv2.imwrite(str(p), cv2.resize(im[oy:oy + 540, ox:ox + 960], (1440, 810), interpolation=cv2.INTER_CUBIC), q); out.append(p)
    return out


def parse(txt):
    m = re.search(r'\{.*\}', txt or '', re.S)
    if not m: return None
    try: return json.loads(m.group(0))
    except Exception: return None


def call_gpt(prompt, imgs, tag):
    if spent('gpt') + L.tong_usd('openai') >= 20: raise SystemExit('CHẶN OpenAI $20')
    content = [{'type': 'input_text', 'text': prompt}]
    for p in imgs: content.append({'type': 'input_image', 'image_url': 'data:image/jpeg;base64,' + base64.b64encode(Path(p).read_bytes()).decode(), 'detail': 'high'})
    body = {'model': GPT, 'input': [{'role': 'user', 'content': content}], 'stream': True, 'reasoning': {'effort': 'medium'}}
    rq = urllib.request.Request('https://api.openai.com/v1/responses', data=json.dumps(body).encode(), headers={'Content-Type': 'application/json', 'User-Agent': L.UA})
    txt, usage, model = '', {}, None
    for att in range(3):
        try:
            with urllib.request.urlopen(rq, timeout=900) as r:
                for line in r:
                    line = line.decode().strip()
                    if not line.startswith('data:'): continue
                    ev = json.loads(line[5:].strip()); ty = ev.get('type', '')
                    if ty == 'response.output_text.delta': txt += ev.get('delta', '')
                    if ty == 'response.completed': usage = ev['response'].get('usage', {}); model = ev['response'].get('model')
            break
        except Exception as e:
            err = str(e); time.sleep(5)
    else: return None, {'loi': err}
    usd = round(usage.get('input_tokens', 0) * 2e-6 + usage.get('output_tokens', 0) * 10e-6, 4)
    log_cost({'tag': tag, 'model': GPT, 'served': model, 'usd': usd, 'in': usage.get('input_tokens', 0), 'out': usage.get('output_tokens', 0), 'date_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())})
    return txt, {'model': model, 'usd': usd, 'usage': usage}


def call_claude(prompt, imgs, tag):
    if spent('claude') >= 25: raise SystemExit('CHẶN Claude $25')
    env = dict(os.environ, ANTHROPIC_API_KEY=os.environ['CONSOLE_API_KEY'])
    with tempfile.TemporaryDirectory() as cwd:
        mp = {}
        for p in imgs: q = Path(cwd) / Path(p).name; shutil.copy(p, q); mp[str(p)] = str(q)
        pr = prompt
        for k, v in mp.items(): pr = pr.replace(k, v)
        cmd = ['claude', '-p', '--model', CLAUDE, '--output-format', 'json', '--allowedTools', 'Read']
        for _ in range(3):
            r = subprocess.run(cmd, input=pr, capture_output=True, text=True, env=env, cwd=cwd, timeout=1800)
            try: d = json.loads(r.stdout)
            except Exception: continue
            u = d.get('usage', {}); usd = d.get('total_cost_usd', 0)
            log_cost({'tag': tag, 'model': CLAUDE, 'served': sorted(d.get('modelUsage', {})), 'usd': usd, 'in': u.get('input_tokens', 0) + u.get('cache_creation_input_tokens', 0) + u.get('cache_read_input_tokens', 0),
                      'out': u.get('output_tokens', 0), 'date_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())})
            return d.get('result', ''), {'model': sorted(d.get('modelUsage', {})), 'usd': usd}
    return None, {'loi': 'claude -p không trả JSON'}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--truoc', required=True); ap.add_argument('--sau', required=True); ap.add_argument('--nam', required=True); ap.add_argument('--noi', default='Gibraltar')
    ap.add_argument('--tag', required=True); ap.add_argument('--out', required=True); ap.add_argument('--mo-hinh', default='gpt,claude'); ap.add_argument('--t4', action='store_true')
    a = ap.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    C = json.load(open(Path(__file__).parent / 'cam_thoi_dai.json')); cam = (C['chung'] if float(a.nam) < 1850 else []) + C['ai_da_bia'] + (C['t4_1666'] if a.t4 else [])   # danh sách 'chung' chỉ cho cảnh trước 1850 (sửa sau c2 2026: mô hình coi ô tô 2026 là lỗi thời đại)
    with tempfile.TemporaryDirectory() as td:
        d = Path(td); T = tiles(a.truoc, d, 'before'); S = tiles(a.sau, d, 'after')
        prompt = PROMPT.format(noi=a.noi, nam=a.nam, truoc='\n'.join(f'- {p}' for p in T), sau='\n'.join(f'- {p}' for p in S), cam='\n'.join(f'- {x}' for x in cam),
                               loai=', '.join(f'"{k}" ({v})' for k, v in LOAI.items()))
        res = {}
        for mh in a.mo_hinh.split(','):
            t0 = time.time()
            if mh == 'gpt': txt, meta = call_gpt(prompt.replace('Read ALL the image files below with the Read tool before answering (paths are absolute):', 'The images are attached in this order:'), T + S, a.tag + '-gpt')
            else: txt, meta = call_claude(prompt, T + S, a.tag + '-claude')
            (out / f'{a.tag}-{mh}.raw.txt').write_text(txt or '')
            res[mh] = dict(meta=meta, secs=round(time.time() - t0, 1), json=parse(txt))
    json.dump(dict(tag=a.tag, truoc=a.truoc, sau=a.sau, nam=a.nam, prompt_sha=L.sha(PROMPT.encode()), ket_qua=res), open(out / f'{a.tag}-vision.json', 'w'), ensure_ascii=False, indent=1)
    for mh, r in res.items(): j = r['json'] or {}; print(a.tag, mh, 'them', len(j.get('them', [])), 'bot_doi', len(j.get('bot_doi', [])), 'vung', len(j.get('doi_loai_vung', [])), r['meta'].get('usd'), r['secs'], 's')


if __name__ == '__main__': main()
