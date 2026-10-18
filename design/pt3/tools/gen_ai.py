"""PT3 · HC7/HC8 — gọi sửa ảnh OpenAI (POST /v1/images/edits) cho từng khúc vân (mặt nạ CHỈ vùng tường/mái/sàn) hoặc tấm chiếu C (HC8).
Model: gpt-image-2.5-sunburst-2026-09-08 (bản chụp ghim của model sửa ảnh hiện hành; tài liệu: "Choose Sunburst for workflows where editing
precision matters most"). Không có seed trong API. Mặt nạ với GPT Image "entirely prompt-based" → sau đó GHÉP CỨNG theo mặt nạ (bake_hc7.py).
Ảnh ra JPEG q82 (giữ nguyên tệp gốc từ API kèm C2PA — dung lượng repo), lưu reports/pt3/ai/<tên>.jpg; sổ: reports/pt3/ai/goi-api.jsonl.
Khoá do proxy gắn cho api.openai.com — mã KHÔNG đọc/in/ghi khoá. Trần OpenAI phiên PT3 $15 → dừng trước lệnh gọi khi tổng ≥ $14,5.
  /opt/cine/bin/python -I gen_ai.py <chunks.json> <tên khúc,...|all> [--ref <ảnh mẫu>] [--try2]"""
import sys, os, json, base64, hashlib, datetime, urllib.request, urllib.error, ssl, time, io, uuid
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
OUT = os.path.join(REPO, 'reports', 'pt3', 'ai'); LOG = os.path.join(OUT, 'goi-api.jsonl'); os.makedirs(OUT, exist_ok=True)
CJ = sys.argv[1]; NAMES = sys.argv[2]; REF = sys.argv[sys.argv.index('--ref') + 1] if '--ref' in sys.argv else None; TRY2 = '--try2' in sys.argv
MODEL, QUALITY = 'gpt-image-2.5-sunburst-2026-09-08', 'high'
PRICE = {'text_in': 5.0, 'img_in': 8.0, 'img_out': 30.0}   # $/1M token (bảng giá đọc 18/10, giay-phep/openai.md)
CAP, GUARD = 15.0, 14.5
D = os.path.dirname(os.path.abspath(CJ)); man = json.load(open(CJ)); site = man['site']

RULES = ("Strict texture rules: this is a flat albedo texture map — no cast shadows, no sunlight, no shading gradients, no perspective, no depth, "
         "no vignetting. Do not draw or add any window, door, opening, shutter, balcony, arch, column, sign, letter, number, poster, flag, emblem, "
         "coat of arms, person, animal, plant pot, pipe, cable, lamp, vehicle or any other object, and do not add, remove, move or reshape any architectural element. "
         "Keep the exact same framing and scale: the surface must cover exactly the same pixels as in the input, from edge to edge — do not shrink, shift, "
         "crop or reframe it, do not add black borders or empty areas, and do not invent bands, cornices, parapets, crenellations, notches or block patterns "
         "that are not visible in the input. Every boundary and every black area stays exactly where it is. The result must look like a high-resolution photographic texture of the SAME surfaces.")
STYLE = (" The second image is only a small material swatch from a neighbouring wall of the same set: match its material character, grain and degree of "
         "weathering, but NOT its layout, size or colours, and do not copy anything else from it.")
PROMPT = {
    ('street', 'elev'): ("Edit only the transparent (masked) area of the first image. The masked area is a flat, orthographic, evenly lit ALBEDO texture of "
        "lime render (stucco) on a masonry wall in Gibraltar's old town in 1943. It is ONLY a wall surface: it contains no windows, doors or openings except the "
        "black areas already present, which must stay black, unchanged and the only openings. Many of these walls are completely blank side walls — keep them blank. "
        "Re-texture the masked surface as realistic weathered painted lime render keeping the SAME base colour as the input at every point: fine hairline cracks, "
        "patched and re-rendered areas, slightly flaking paint, faint vertical rain and water stains, light grime, darker damp staining near the bottom edge. "),
    ('street', 'top'): ("Edit only the transparent (masked) areas of the first image. It is a flat, top-down orthographic ALBEDO texture (no lighting) of roofs and "
        "streets of Gibraltar's old town in 1943, seen straight from above: flat roof terraces finished in lime plaster, clay tile roofs, and streets paved with "
        "stone setts. Re-texture every surface as realistic weathered material of the SAME type and the SAME colour as the input at every point: stained, patched "
        "lime-plastered terraces with faint cracks and grime along the edges; weathered terracotta tiles with colour variation; worn, uneven stone setts with dirt "
        "in the joints. Do not draw chimneys, water tanks, laundry, furniture, carts, vehicles, people or markings. "),
    ('kb', 'elev'): ("Edit only the transparent (masked) wall areas of the first image. It is a flat, orthographic, evenly lit ALBEDO texture of the outer stone wall "
        "of King's Bastion, Gibraltar (an 18th-century artillery bastion built in 1773, as it stood in 1782). The whole image is one continuous stone wall "
        "surface; its bottom edge is at sea level. Black areas are openings or background and must stay black and "
        "unchanged. Re-texture the stone as realistic weathered limestone ashlar masonry keeping the SAME base colour as the input at every point: coursed blocks with "
        "thin mortar joints at the same scale as the input courses, slight colour variation between blocks, small chips and spalls, salt and water staining, darker damp and some dark green-brown algae in "
        "the lowest band near sea level. "),
    ('kb', 'top'): ("Edit only the transparent (masked) areas of the first image. It is a flat, top-down orthographic ALBEDO texture (no lighting) of King's Bastion, "
        "Gibraltar, in 1782, seen straight from above: the large gun platform (terreplein) and the tops of the stone parapet walls around it. Re-texture keeping the "
        "SAME colour as the input at every point: the platform as compacted earth and gravel with worn stone patches and wheel wear, the wall tops as worn limestone "
        "coping. Do not draw cannons, gun carriages, cannonballs, shot piles, barrels, carts, tents, people or markings. "),
}

def spent():
    return sum(json.loads(l).get('usd', 0) for l in open(LOG)) if os.path.exists(LOG) else 0.0

def c2pa_jpeg(b):
    """tìm đoạn APP11 (0xFFEB) chứa JUMBF/C2PA trong JPEG."""
    found = []; i = 2
    while i + 4 <= len(b) and b[i] == 0xFF:
        m = b[i + 1]; n = int.from_bytes(b[i + 2:i + 4], 'big')
        if m == 0xEB:
            seg = b[i + 4:i + 2 + n]; found.append('APP11' + ('+jumb' if b'jumb' in seg else '') + ('+c2pa' if b'c2pa' in seg else ''))
        if m == 0xDA: break
        i += 2 + n
    return found

def multipart(fields, files):
    bnd = uuid.uuid4().hex; out = io.BytesIO()
    for k, v in fields.items(): out.write(f'--{bnd}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    for k, fn, data, ct in files:
        out.write(f'--{bnd}\r\nContent-Disposition: form-data; name="{k}"; filename="{fn}"\r\nContent-Type: {ct}\r\n\r\n'.encode()); out.write(data); out.write(b'\r\n')
    out.write(f'--{bnd}--\r\n'.encode()); return out.getvalue(), f'multipart/form-data; boundary={bnd}'

ctx = ssl.create_default_context(cafile='/root/.ccr/ca-bundle.crt')
todo = [c for c in man['chunks'] if 'bo_qua' not in c and (NAMES == 'all' or c['name'] in NAMES.split(','))]
for c in todo:
    tag = c['name'] + ('-thu2' if TRY2 else '')
    if os.path.exists(os.path.join(OUT, tag + '.jpg')): print('đã có', tag); continue
    if spent() >= GUARD: print('DỪNG: tổng OpenAI PT3 đã', round(spent(), 4)); break
    kind = c.get('kind'); pr = c.get('prompt') or (PROMPT[(site, kind)] + RULES + (STYLE if REF else ''))
    img = open(os.path.join(D, c['name'] + '.png'), 'rb').read(); files = [('image[]', c['name'] + '.png', img, 'image/png')]
    if REF: files.append(('image[]', 'style_ref.png', open(REF, 'rb').read(), 'image/png'))
    mk = os.path.join(D, c['name'] + '_mask.png')
    if os.path.exists(mk): files.append(('mask', c['name'] + '_mask.png', open(mk, 'rb').read(), 'image/png'))
    size = f"{c['W_api']}x{c['H_api']}"
    fields = {'model': MODEL, 'prompt': pr, 'size': size, 'quality': QUALITY, 'n': '1', 'output_format': 'jpeg', 'output_compression': '82',
              'stream': 'true', 'partial_images': '1'}
    body, ct = multipart(fields, files)
    req = urllib.request.Request('https://api.openai.com/v1/images/edits', data=body, method='POST', headers={'Content-Type': ct})
    rec = {'anh': tag, 'pt3': site, 'loai': kind, 'ai_texture': True, 'endpoint': 'POST /v1/images/edits', 'model_req': MODEL, 'prompt': pr,
           'params': {k: v for k, v in fields.items() if k != 'prompt'}, 'input': {'file': c['name'] + '.png', 'sha256': hashlib.sha256(img).hexdigest(),
           'mask': os.path.basename(mk) if os.path.exists(mk) else None, 'mask_frac': c.get('mask_frac'), 'style_ref': os.path.basename(REF) if REF else None},
           'seed': 'API không có tham số seed', 'date_utc': datetime.datetime.now(datetime.UTC).isoformat(timespec='seconds')}
    t0 = time.time()
    for attempt in range(2):   # lỗi đường truyền (5xx, đứt luồng) thử lại 1 lần — không tính là "lần thử" của model
        try:
            r = urllib.request.urlopen(req, timeout=900, context=ctx); code = r.status; d = {}
            for line in r:
                line = line.decode('utf8', 'replace').strip()
                if not line.startswith('data:'): continue
                ev = json.loads(line[5:].strip())
                if ev.get('type', '').endswith('.completed'): d = {'b64': ev['b64_json'], 'usage': ev.get('usage', {}), 'size': ev.get('size'), 'quality': ev.get('quality'), 'model': ev.get('model')}
                elif ev.get('type', '').endswith('partial_image'): rec['partial_events'] = rec.get('partial_events', 0) + 1
                elif 'error' in ev: d = {'error': ev['error']}
            if 'b64' not in d: code = 599; d.setdefault('error', 'luồng kết thúc không có ảnh')
        except urllib.error.HTTPError as e:
            code = e.code; d = {'error': e.read().decode('utf8', 'replace')[:600]}
        except Exception as e:
            code = 598; d = {'error': repr(e)[:300]}
        if code == 200 or code < 500: break
        rec.setdefault('loi_duong_truyen', []).append({'http': code, 'error': str(d.get('error'))[:200]}); time.sleep(5)
    rec['http'] = code; rec['secs'] = round(time.time() - t0, 1)
    if code == 200:
        u = d.get('usage', {}); rec['usage'] = u; det = u.get('input_tokens_details', {}) or {}
        ti, ii, oo = det.get('text_tokens', 0), det.get('image_tokens', 0), u.get('output_tokens', 0)
        rec['usd'] = round((ti * PRICE['text_in'] + ii * PRICE['img_in'] + oo * PRICE['img_out']) / 1e6 + rec.get('partial_events', 0) * 100 * PRICE['img_out'] / 1e6, 5)
        rec['ghi_chu_gia'] = 'usage của sự kiện completed + 100 token ra/ảnh tạm (partial) theo tài liệu'
        b = base64.b64decode(d['b64']); fn = os.path.join(OUT, tag + '.jpg'); open(fn, 'wb').write(b)
        rec.update(model_resp=d.get('model') or MODEL, file=os.path.basename(fn), sha256=hashlib.sha256(b).hexdigest(), bytes=len(b), c2pa_segments=c2pa_jpeg(b),
                   size_resp=d.get('size'), quality_resp=d.get('quality'))
        rec['c2pa'] = any('c2pa' in x or 'jumb' in x for x in rec['c2pa_segments'])
    else:
        rec['error'] = d.get('error'); rec['usd'] = 0.0
    with open(LOG, 'a') as f: f.write(json.dumps(rec, ensure_ascii=False) + '\n')
    print(tag, code, rec.get('usd'), 'C2PA', rec.get('c2pa'), rec.get('secs'), 's · tổng PT3', round(spent(), 4), flush=True)
    if code in (401, 403): print('DỪNG: bị từ chối'); break
