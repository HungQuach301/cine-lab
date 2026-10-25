#!/opt/cine/bin/python
"""N2+ — HAI MÔ HÌNH NHÌN KHÁC NHAU liệt kê vật THÊM / BỚT / ĐỔI giữa render (TRƯỚC) và khung AI đã ghép (SAU) — bản 1.17.0 (phiên K-1.17,
21/10/2026). Chuyển từ reports/nc-n2p/ma/vision_kiem.py (NC-N2P, kiểm có đáp án 6/6 mỗi mô hình, đối chứng 0 báo). Mô hình CHỈ liệt kê;
q_n2p.py (máy) kết luận theo loại + vị trí.

  - OpenAI GPT (Responses API, stream, reasoning medium) — khoá do proxy gắn cho api.openai.com; mã KHÔNG đọc/in/ghi khoá.
  - Claude GHIM judge.MODEL qua judge.call (`claude -p --bare --restricted`, chỉ công cụ Read, HOME tạm, khoá CONSOLE_API_KEY qua môi trường
    tiến trình con; trần --max-budget-usd CAP_CLAUDE mỗi khung).
  Cả hai nhận CÙNG đề bài (PROMPT_VER) + cùng 10 ảnh: TRƯỚC và SAU, mỗi ảnh toàn khung 1568×882 + 4 ô phần tư phóng 1,5× (1440×810), danh sách
  CẤM data/cam_thoi_dai.json ('chung' chỉ khi năm < 1850; 'ai_da_bia' luôn; 't4_1666' khi --t4).
  User-Agent cố định UA (không email); payload chỉ gồm đề bài + ảnh khung của ta.

MẶC ĐỊNH TẮT: chỉ gọi mạng khi q_n2p/k2check chạy với `--vision` (api=True). Không cờ → chỉ đọc bộ đệm (khoá = sha256 TRƯỚC + SAU + năm + nơi + t4
+ PROMPT_VER + hai mô hình); khung chưa có → THIẾU, không gọi mạng.
Chi phí đo ở NC-N2P (21/10/2026, một khung 1920×1080): GPT ≈ $0,04–0,07 (giá $2/M vào, $10/M ra — developers.openai.com), Claude ≈ $0,13–0,15
(total_cost_usd) → ≈ $0,17–0,22/khung cho cả hai; đo lại K-1.17 21/10: $0,097–0,117/khung (GPT $0,033–0,045 + Claude $0,064–0,072).
Ghi từng lần gọi vào <out>/n2p-cost.jsonl.
"""
import base64, hashlib, json, os, re, shutil, sys, tempfile, time, urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from checks.ll import judge  # noqa: E402

PROMPT_VER = 'n2p-v1 (NC-N2P vision_kiem 21/10/2026 → K-1.17)'
GPT = 'gpt-6.1-sol'
CLAUDE = judge.MODEL
GPT_USD_IN, GPT_USD_OUT = 2e-6, 10e-6
CAP_CLAUDE = 0.40
UA = 'CineLab-research (+https://github.com/HungQuach301/cine-lab)'
CAM = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'cam_thoi_dai.json')
LOAI = {
    'co': 'flag, banner or ensign', 'cong_trinh': 'building, house, tower, steeple, church, hut, wall, gate, pier, mole, quay, bridge, road or paved street',
    'cong_su': 'fortification, bastion, battery, trench, cannon or gun', 'tau_lon': 'ship (sea-going sailing vessel, any ship larger than a rowing boat)',
    'chu': 'text, letters, numbers, sign, logo, watermark', 'den': 'lamp or artificial light source', 'lua_lon': 'large fire or burning building',
    'leu': 'tent, awning or temporary shelter', 'do_dac': 'goods, barrels, crates, sacks, furniture, heaps, timber or stone piles',
    'xe_dung': 'cart or carriage standing without animals or people', 'rom': 'haystack or hay rick', 'vuon': 'garden plot, field, terrace, hedge',
    'cay': 'tree, bush, scrub, grass', 'da_dat': 'rocks, sand, soil, cliff texture', 'nguoi': 'person or people', 'dong_vat': 'animal (horse, cattle, dog …)',
    'chim': 'bird', 'thuyen_nho': 'small boat, rowing boat, barge or lighter', 'xe_chay': 'cart, carriage or vehicle with animals or in motion',
    'khoi': 'smoke, steam or dust plume', 'lua_trai': 'campfire, cooking fire or small flame', 'phoi': 'laundry or cloth hung to dry', 'may_bay': 'aircraft',
    'xe_may': 'motor vehicle', 'khac': 'anything else'}
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
GPT_LEAD = 'Read ALL the image files below with the Read tool before answering (paths are absolute):'


def cam_list(nam, t4=False):
    C = json.load(open(CAM))
    return (C['chung'] if float(nam) < 1850 else []) + C['ai_da_bia'] + (C['t4_1666'] if t4 else [])


def tiles(img, d, pre):
    import cv2
    im = cv2.imread(str(img), cv2.IMREAD_COLOR)
    if im is None: raise FileNotFoundError(img)
    im = cv2.resize(im, (1920, 1080), interpolation=cv2.INTER_AREA if im.shape[1] > 1920 else cv2.INTER_CUBIC); q = [cv2.IMWRITE_JPEG_QUALITY, 92]; out = []
    p = os.path.join(d, f'{pre}_full.jpg'); cv2.imwrite(p, cv2.resize(im, (1568, 882), interpolation=cv2.INTER_AREA), q); out.append(p)
    for i, (ox, oy) in enumerate(((0, 0), (960, 0), (0, 540), (960, 540))):
        p = os.path.join(d, f'{pre}_q{i + 1}.jpg'); cv2.imwrite(p, cv2.resize(im[oy:oy + 540, ox:ox + 960], (1440, 810), interpolation=cv2.INTER_CUBIC), q); out.append(p)
    return out


def sha_file(p):
    with open(p, 'rb') as f: return hashlib.sha256(f.read()).hexdigest()


def khoa(truoc, sau, nam, noi, t4, mo_hinh):
    return hashlib.sha256(f'{sha_file(truoc)}|{sha_file(sau)}|{int(float(nam))}|{noi}|{bool(t4)}|{PROMPT_VER}|{",".join(mo_hinh)}|{GPT}|{CLAUDE}'.encode()).hexdigest()[:32]


def parse(txt):
    x = judge.parse_json(txt)
    if x is not None: return x
    m = re.search(r'\{.*\}', txt or '', re.S)
    try: return json.loads(m.group(0)) if m else None
    except ValueError: return None


def _log(out, rec):
    if not out: return
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, 'n2p-cost.jsonl'), 'a') as f: f.write(json.dumps(rec, ensure_ascii=False) + '\n')


def call_gpt(prompt, imgs, tag, out=None):
    content = [{'type': 'input_text', 'text': prompt}] + [{'type': 'input_image', 'detail': 'high', 'image_url': 'data:image/jpeg;base64,' + base64.b64encode(open(p, 'rb').read()).decode()}
                                                            for p in imgs]
    body = {'model': GPT, 'input': [{'role': 'user', 'content': content}], 'stream': True, 'reasoning': {'effort': 'medium'}}
    rq = urllib.request.Request('https://api.openai.com/v1/responses', data=json.dumps(body).encode(), headers={'Content-Type': 'application/json', 'User-Agent': UA})
    err = None
    for _ in range(2):
        txt, usage, model = '', {}, None
        try:
            with urllib.request.urlopen(rq, timeout=900) as r:
                for line in r:
                    line = line.decode().strip()
                    if not line.startswith('data:'): continue
                    try: ev = json.loads(line[5:].strip())
                    except ValueError: continue
                    ty = ev.get('type', '')
                    if ty == 'response.output_text.delta': txt += ev.get('delta', '')
                    elif ty == 'response.completed': usage = ev['response'].get('usage') or {}; model = ev['response'].get('model')
            break
        except Exception as e:   # noqa: BLE001 — lỗi mạng/API → thử lại 1 lần rồi THIẾU
            err = f'{type(e).__name__}: {str(e)[:200]}'; time.sleep(5)
    else: return None, dict(loi=err)
    usd = round(usage.get('input_tokens', 0) * GPT_USD_IN + usage.get('output_tokens', 0) * GPT_USD_OUT, 4)
    _log(out, dict(tag=tag, model=GPT, served=model, usd=usd, vao=usage.get('input_tokens', 0), ra=usage.get('output_tokens', 0), date_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())))
    loi = None if (model or '').startswith(GPT) else f'mô hình trả về {model!r} ≠ {GPT}'
    return txt, dict(model=model, usd=usd, usage=usage, loi=loi)


def call_claude(prompt, cwd, tag, out=None):
    x = judge.call(prompt, cwd, CAP_CLAUDE)
    e = ([f"lỗi API: {x['error']}"] if x['is_error'] else []) + judge.model_errors(x['model_usage'])
    _log(out, dict(tag=tag, model=CLAUDE, served=sorted(x.get('model_usage') or {}), usd=x.get('cost_usd'), so_anh_doc=len(x.get('reads') or []),
                   date_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())))
    return x.get('result'), dict(model=sorted(x.get('model_usage') or {}), usd=x.get('cost_usd'), reads=x.get('reads') or [], loi='; '.join(e) or None)


def khoa_de(truoc, sau, nam, de, mo_hinh):
    """1.17.8: khoá bộ đệm cho đề bài riêng (LUẬT E) — SHA ảnh + năm + phiên bản + SHA đề bài đã điền (danh sách mốc) + hai mô hình"""
    return hashlib.sha256(f"{sha_file(truoc)}|{sha_file(sau)}|{int(float(nam))}|{de['ver']}|{hashlib.sha256(de['prompt'].encode()).hexdigest()}|{','.join(mo_hinh)}|{GPT}|{CLAUDE}".encode()).hexdigest()[:32]


def soi(truoc, sau, nam, noi='', t4=False, out=None, tag='khung', api=False, cache=None, mo_hinh=('gpt', 'claude'), de=None):
    """→ dict(ket_qua={mh: {json, meta}}, khoa, tu_bo_dem, loi). Không api và không có trong bộ đệm → loi='chưa soi'.
    de (1.17.8, LUẬT E): dict(prompt=<đề bài đã điền trừ {truoc}/{sau}>, ver=<phiên bản>) thay PROMPT n2p-v1."""
    k = khoa_de(truoc, sau, nam, de, mo_hinh) if de else khoa(truoc, sau, nam, noi, t4, mo_hinh)
    if cache is not None and k in cache: return dict(cache[k], khoa=k, tu_bo_dem=True)
    if not api: return dict(khoa=k, ket_qua={}, loi='chưa soi: không có trong bộ đệm và không chạy --vision (mô hình nhìn có chi phí ≈ $0,2/khung)')
    td = tempfile.mkdtemp(prefix='n2pv-')
    try:
        T = tiles(truoc, td, 'before'); S = tiles(sau, td, 'after')
        if de: pr = de['prompt'].replace('{truoc}', '\n'.join(f'- {p}' for p in T)).replace('{sau}', '\n'.join(f'- {p}' for p in S))
        else: pr = PROMPT.format(noi=noi or 'the place', nam=int(float(nam)), truoc='\n'.join(f'- {p}' for p in T), sau='\n'.join(f'- {p}' for p in S),
                                 cam='\n'.join(f'- {x}' for x in cam_list(nam, t4)), loai=', '.join(f'"{a}" ({b})' for a, b in LOAI.items()))
        res, loi = {}, []
        for mh in mo_hinh:
            t0 = time.time()
            if mh == 'gpt': txt, meta = call_gpt(pr.replace(GPT_LEAD, 'The images are attached in this order:'), T + S, f'{tag}-gpt', out)
            else:
                from checks.ll import q_k1176 as K76   # 1.17.6 (KN-3): không đọc đủ ảnh → gọi lại MỘT lần; cả hai lần vào n2p-cost.jsonl
                txt, meta = K76.goi_claude_du(sys.modules[__name__], pr, td, T + S, f'{tag}-claude', out)
            j = parse(txt) if not meta.get('loi') else None
            if not meta.get('loi') and j is None: meta['loi'] = 'trả lời không đọc được (không phải JSON)'
            if meta.get('loi'): loi.append(f"{mh}: {meta['loi']}")
            if out:
                os.makedirs(out, exist_ok=True); open(os.path.join(out, f'{tag}-{mh}.raw.txt'), 'w').write(txt or '')
            res[mh] = dict(meta=meta, secs=round(time.time() - t0, 1), json=j)
    finally: shutil.rmtree(td, ignore_errors=True)
    R = dict(khoa=k, ket_qua=res, prompt_ver=de['ver'] if de else PROMPT_VER, loi='; '.join(loi) or None, chi_phi_usd=round(sum(float(v['meta'].get('usd') or 0) for v in res.values()), 4))
    if cache is not None and not R['loi']: cache[k] = {a: b for a, b in R.items() if a != 'khoa'}
    return R
