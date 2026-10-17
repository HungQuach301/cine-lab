"""PT nhánh C (H-C) — CHỈ NGHIÊN CỨU, KHÔNG lên kênh. Sửa ảnh (image edit) khung đã render của nhánh A bằng model ảnh hiện hành của OpenAI
(POST /v1/images/edits, gpt-image-2.5-sunburst — tài liệu: "Choose Sunburst for workflows where editing precision matters most").
Prompt chỉ mô tả vật liệu/đồ vật/trang phục đúng thời kỳ (TIEN-KY), yêu cầu GIỮ NGUYÊN hình khối, vị trí nhà, phố, chân trời, góc máy, ánh sáng;
không tên người thật, không thêm cờ/biểu tượng (khung A có MỘT cờ Union — giữ nguyên, không thêm), không chữ/biển hiệu, không cận mặt.
Khoá API do proxy gắn cho api.openai.com — mã KHÔNG đọc/in/ghi khoá.
  /opt/cine/bin/python -I gen_c.py <thư mục khung A> <out_dir> <log.jsonl> <tên khung…> [--try2]
Trần: tổng OpenAI (B + C, đọc cả hai sổ) ≤ $15 → dừng trước lệnh gọi nếu tổng đã ≥ $14,5 (dự phòng một lệnh)."""
import sys, os, json, base64, hashlib, datetime, urllib.request, ssl, time, struct, io, uuid
from PIL import Image
SRC, OUT, LOG = sys.argv[1], sys.argv[2], sys.argv[3]; TRY2 = '--try2' in sys.argv
NAMES = [a for a in sys.argv[4:] if not a.startswith('--')]; os.makedirs(OUT, exist_ok=True)
MODEL, SIZE, QUALITY = 'gpt-image-2.5-sunburst', '2048x1152', 'high'
PRICE = {'text_in': 5.0, 'img_in': 8.0, 'img_out': 30.0}       # $/1M, bảng giá đọc lại 18/10 (không đổi so với 17/10)
CAP, GUARD = 15.0, 14.5
LOG_B = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'reports', 'pt', 'ai', 'goi-api.jsonl')

KEEP = ("KEEP EXACTLY UNCHANGED: the camera position and angle, framing, lens perspective, horizon line, the shape, position, height, roofline "
        "and window positions of every building, the layout of the street and square, the sea wall, the sea, the distant hills, the position of "
        "every ship, the single existing flag and its pole, the sun direction, the shadows and the time-of-day lighting and colour grading. "
        "Do not add, remove, move, resize or reshape any building, wall, roof, window or ship. ")
RULES = ("No text, no letters, no numbers, no signs or signboards, no posters, no new flags, no emblems or insignia. No modern objects. "
         "People only small and far away (at least 10 metres from the camera), no close-up faces, nobody lying on the ground. Photorealistic.")
EPOCH = {
    1782: ("This is a fixed eye-level camera view of the Grand Parade beside Main Street, Gibraltar, in September 1782, during the Great Siege; "
           "part of the town is damaged by bombardment. ",
           "ADD ONLY surface and small-scale detail: weathered lime-washed plaster with stains, patches and soot near broken openings; "
           "plain eighteenth-century timber doors and board shutters; worn limestone; packed-earth ground with cart ruts, footprints and scattered rubble; "
           "period objects such as wooden barrels, piles of iron cannonballs, two-wheeled wooden carts and stacked timber; and a few small distant figures "
           "wearing 1780s British infantry red coats with white cross-belts and black tricorne hats, artillerymen in dark blue coats, "
           "or plain eighteenth-century civilian clothing. "),
    1943: ("This is a fixed eye-level camera view of Commercial Square beside Main Street, Gibraltar, in September 1943, during the Second World War "
           "(most civilians had been evacuated; the town is full of servicemen). ",
           "ADD ONLY surface and small-scale detail: weathered painted lime render in ochre, pink and cream with peeling patches and grime; "
           "green louvred wooden shutters; wrought-iron balconies; worn granite setts; sandbags stacked at doorways; period objects such as wooden handcarts, "
           "crates, barrels and a few bicycles; and a few small distant figures wearing 1940s British Army khaki battledress, Royal Navy dark blue or white "
           "uniforms, or plain 1940s civilian clothes. "),
}
TIME = {'dau': "It is morning. ", 'giua': "It is afternoon. ", 'cuoi': "It is night under a blackout: keep it dark, keep the same few light sources, do not add lit windows or street lights. "}
TIME1782N = "It is night: keep it dark, keep the same few light sources (one oil lantern), do not add lit windows. "

def prompt_for(name, strict=False):
    ep, t = name.split('-'); ep = int(ep)
    tm = TIME1782N if (ep == 1782 and t == 'cuoi') else TIME[t]
    s = "Edit this image. " + EPOCH[ep][0] + tm + KEEP + EPOCH[ep][1] + RULES
    if strict: s = ("STRICT GEOMETRY PRESERVATION: the output must overlay the input pixel-for-pixel in structure; change only fine texture and add only "
                    "tiny props and distant figures on the ground. " + s)
    return s

def spent_all():
    t = 0.0
    for p in (LOG_B, LOG):
        if os.path.exists(p): t += sum(json.loads(l).get('usd', 0) for l in open(p))
    return t

def c2pa_chunks(png):
    found = []; i = 8
    while i + 8 <= len(png):
        n, t = struct.unpack('>I4s', png[i:i + 8]); t = t.decode('latin1')
        if t in ('caBX', 'jumb', 'jumd'): found.append(t)
        i += 12 + n
        if t == 'IEND': break
    return found

def multipart(fields, files):
    b = uuid.uuid4().hex; out = io.BytesIO()
    for k, v in fields.items():
        out.write(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    for k, (fn, data, ct) in files.items():
        out.write(f'--{b}\r\nContent-Disposition: form-data; name="{k}"; filename="{fn}"\r\nContent-Type: {ct}\r\n\r\n'.encode()); out.write(data); out.write(b'\r\n')
    out.write(f'--{b}--\r\n'.encode()); return out.getvalue(), f'multipart/form-data; boundary={b}'

ctx = ssl.create_default_context(cafile='/root/.ccr/ca-bundle.crt')
for name in NAMES:
    tag = name + ('-thu2' if TRY2 else '')
    if spent_all() >= GUARD: print('DỪNG: tổng OpenAI B+C đã', round(spent_all(), 4)); break
    src = os.path.join(SRC, f'{name}-A-notext.jpg'); im = Image.open(src).convert('RGB').resize((2048, 1152), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, 'JPEG', quality=95); data = buf.getvalue()   # JPEG q95 (~1 MB): lệnh PNG 5 MB đầu tiên bị 502
    pr = prompt_for(name, strict=TRY2)
    fields = {'model': MODEL, 'prompt': pr, 'size': SIZE, 'quality': QUALITY, 'n': '1', 'output_format': 'png', 'stream': 'true', 'partial_images': '1'}
    # stream + 1 ảnh tạm: lệnh không stream bị 502 đúng 30,4 s (đường truyền cắt khi chờ > 30 s); ảnh tạm tính thêm 100 token ra
    body, ct = multipart(fields, {'image[]': (f'{name}-A.jpg', data, 'image/jpeg')})
    req = urllib.request.Request('https://api.openai.com/v1/images/edits', data=body, method='POST', headers={'Content-Type': ct})
    rec = {'anh': tag, 'nhanh': 'C', 'ai_image': True, 'chi_nghien_cuu': True, 'endpoint': 'POST /v1/images/edits', 'model_req': MODEL, 'prompt': pr,
           'params': {k: v for k, v in fields.items() if k != 'prompt'}, 'input': {'file': os.path.basename(src), 'sha256': hashlib.sha256(open(src, 'rb').read()).hexdigest(),
           'gui_len': 'JPEG q95 2048x1152 (LANCZOS từ 1920x1080)'}, 'seed': 'API không có tham số seed', 'date_utc': datetime.datetime.now(datetime.UTC).isoformat(timespec='seconds')}
    t0 = time.time()
    try:
        r = urllib.request.urlopen(req, timeout=900, context=ctx); code = r.status; d = {}
        for line in r:
            line = line.decode('utf8', 'replace').strip()
            if not line.startswith('data:'): continue
            ev = json.loads(line[5:].strip())
            if ev.get('type', '').endswith('.completed'): d = {'data': [{'b64_json': ev['b64_json']}], 'usage': ev.get('usage', {}), 'size': ev.get('size'), 'quality': ev.get('quality'), 'model': ev.get('model')}
            elif ev.get('type', '').endswith('partial_image'): rec['partial_events'] = rec.get('partial_events', 0) + 1
            elif 'error' in ev: d = {'error': ev['error']}
        if 'data' not in d: code = 599; d.setdefault('error', 'stream kết thúc không có ảnh')
    except urllib.error.HTTPError as e:
        code = e.code; d = {'error': e.read().decode('utf8', 'replace')[:600]}
    rec['http'] = code; rec['secs'] = round(time.time() - t0, 1)
    if code == 200:
        u = d.get('usage', {}); rec['usage'] = u; det = u.get('input_tokens_details', {}) or {}
        ti = det.get('text_tokens', 0); ii = det.get('image_tokens', 0); oo = u.get('output_tokens', 0)
        rec['usd'] = round((ti * PRICE['text_in'] + ii * PRICE['img_in'] + oo * PRICE['img_out']) / 1e6, 5); rec['model_resp'] = d.get('model') or MODEL
        rec['ghi_chu_gia'] = 'usage của sự kiện completed; ảnh tạm (partial) tính thêm 100 token ra/ảnh theo tài liệu — đã cộng' ; rec['usd'] = round(rec['usd'] + rec.get('partial_events', 0) * 100 * PRICE['img_out'] / 1e6, 5)
        b = base64.b64decode(d['data'][0]['b64_json']); fn = os.path.join(OUT, f'{tag}.png'); open(fn, 'wb').write(b)
        rec.update(file=os.path.basename(fn), sha256=hashlib.sha256(b).hexdigest(), bytes=len(b), c2pa_chunks=c2pa_chunks(b))
        rec['c2pa'] = bool(rec['c2pa_chunks']); rec['size_resp'] = d.get('size'); rec['quality_resp'] = d.get('quality')
    else:
        rec['error'] = d.get('error'); rec['usd'] = 0.0
    with open(LOG, 'a') as f: f.write(json.dumps(rec, ensure_ascii=False) + '\n')
    print(tag, code, rec.get('usd'), rec.get('c2pa'), rec.get('secs'), 'tong B+C', round(spent_all(), 4), flush=True)
    if code in (401, 403): print('NHÁNH C CHƯA CHẠY: thiếu khoá / bị từ chối'); break
