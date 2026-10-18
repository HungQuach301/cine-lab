"""PT2 · tấm nền C (HC1) — MỘT tấm cho mỗi khung neo × mốc, CHỈ khung BAN NGÀY (lượt d2 của nền A).
POST /v1/images/edits (gpt-image-2.5-sunburst — model sửa ảnh hiện hành, tài liệu đọc lại phiên PT2) + MẶT NẠ dựng từ lượt mã lớp của Blender:
chỉ cho sửa bề mặt tường/mái/mặt đất/đồ vật nền (alpha 0); mọi vật mang dữ kiện + trời + biển + đồi + Line Wall + cửa/kính/cửa chớp/ban công/biển hiệu
= alpha 255 (giữ). Tài liệu OpenAI: "Masking with GPT Image is entirely prompt-based… may not follow its exact shape" → sau đó BẮT BUỘC ghép lại
điểm ảnh A cho vùng bảo vệ (compose_c2.py, HC2). Khoá API do proxy gắn — mã KHÔNG đọc/in/ghi khoá.
  /opt/cine/bin/python -I gen_c2.py <nền A dir> <ra dir> <log.jsonl> <khung neo: 1782|1943> [--lan 2|3]
Trần OpenAI phiên PT2 ≤ $5 → dừng trước lệnh gọi nếu sổ PT2 đã ≥ $4,8."""
import sys, os, json, base64, hashlib, datetime, urllib.request, ssl, time, struct, io, uuid
import numpy as np, cv2
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lai_common as LC
BG, OUT, LOG, EP = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]); LAN = int(sys.argv[sys.argv.index('--lan') + 1]) if '--lan' in sys.argv else 1
os.makedirs(OUT, exist_ok=True)
MODEL, SIZE, QUALITY = 'gpt-image-2.5-sunburst', '2048x1152', 'high'
PRICE = {'text_in': 5.0, 'img_in': 8.0, 'img_out': 30.0}      # $/1M token, bảng giá đọc lại phiên PT2
GUARD = 4.8

KEEP = ("Only the TRANSPARENT areas of the mask may change: plain wall surfaces, roof surfaces, the ground, and the few existing barrels, carts, "
        "rubble heaps and timber on the ground. Everything else must stay exactly as it is. KEEP EXACTLY UNCHANGED: camera position and angle, "
        "framing, lens perspective, horizon, the shape, height, roofline and position of every building, every window, door, shutter, balcony and "
        "plain signboard, the sea wall, the sea, the distant hills, the sky, the flagpole, the cannon, the lamp, the sun direction, the shadows and "
        "the time-of-day lighting. ")
FORBID = ("DO NOT ADD: people, figures, animals, flags, banners, pennants, emblems, insignia, text, letters, numbers, signs, posters, ships or boats, "
          "vehicles, lamps, lanterns, candles, fires, lit windows or any new light source, plants, modern objects. Photorealistic, natural daylight.")
EPOCH = {
    1782: ("Edit this photograph-like image: a narrow lane of lime-washed two- and three-storey houses in the town of Gibraltar in September 1782, "
           "during the Great Siege, after months of bombardment. It is a clear day. ",
           "In the editable areas ADD ONLY surface and small-scale detail: weathered, stained and patched lime-wash; cracks and places where plaster has "
           "fallen away showing rough rubble stone or brick; soot streaks above damaged openings; worn, uneven clay roof tiles; a packed-earth and "
           "rough stone lane surface with ruts, dust and small scattered debris; you may add a few period background objects lying along the foot of "
           "the walls: wooden barrels, heaps of broken masonry and charred loose timber. Add nothing else. "),
    1943: ("Edit this photograph-like image: a street of painted rendered houses with green louvred shutters and iron balconies at Commercial "
           "Square, Gibraltar, in September 1943, during the Second World War, when most civilians had been evacuated. It is a clear day. ",
           "In the editable areas ADD ONLY surface and small-scale detail: weathered painted lime render in ochre, pink and cream with peeling patches, "
           "grime and water stains; worn granite setts and stone paving with dust and small cracks. Do not add any objects at all: surface "
           "detail only. "),
}
def prompt_for(ep, lan):
    s = EPOCH[ep][0] + KEEP + EPOCH[ep][1] + FORBID
    if lan > 1: s = ("STRICT: change nothing outside the transparent mask areas; add no new objects except the listed background objects. "
                     "Keep every cast shadow exactly where it is: the shadow of the buildings across the lane must stay the same shape and darkness; "
                     "do not brighten or relight the scene. Roofless ruined houses must stay roofless ruins; do not rebuild, re-roof or repair them. " + s)
    return s

def spent():
    return sum(json.loads(l).get('usd', 0) for l in open(LOG)) if os.path.exists(LOG) else 0.0
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
    for k, v in fields.items(): out.write(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    for k, (fn, data, ct) in files.items():
        out.write(f'--{b}\r\nContent-Disposition: form-data; name="{k}"; filename="{fn}"\r\nContent-Type: {ct}\r\n\r\n'.encode()); out.write(data); out.write(b'\r\n')
    out.write(f'--{b}--\r\n'.encode()); return out.getvalue(), f'multipart/form-data; boundary={b}'

if spent() >= GUARD: sys.exit(f'DỪNG: sổ OpenAI PT2 đã {spent():.4f}')
d = os.path.join(BG, f'{EP}A')
plate = cv2.imread(os.path.join(d, 'd2.png'), cv2.IMREAD_UNCHANGED)[..., :3][..., ::-1]
plate8 = (plate.astype(np.float32) / 257.0 + 0.5).astype(np.uint8)             # 16 bit → 8 bit (cùng ảnh hiển thị AgX)
prot = LC.protected_mask(d)                                                      # True = vùng bảo vệ (đã nở 3 px)
im = Image.fromarray(plate8).resize((2048, 1152), Image.LANCZOS)
mk = Image.fromarray(((prot) * 255).astype(np.uint8)).resize((2048, 1152), Image.NEAREST)
mrgba = Image.new('RGBA', (2048, 1152), (0, 0, 0, 0)); mrgba.putalpha(mk)        # alpha 0 = được sửa, 255 = giữ
tag = f'{EP}-d2' + (f'-lan{LAN}' if LAN > 1 else '')
im.save(os.path.join(OUT, f'{tag}-vao.png')); mrgba.save(os.path.join(OUT, f'{tag}-matna.png'))
bi = io.BytesIO(); im.save(bi, 'PNG'); bm = io.BytesIO(); mrgba.save(bm, 'PNG')
pr = prompt_for(EP, LAN)
fields = {'model': MODEL, 'prompt': pr, 'size': SIZE, 'quality': QUALITY, 'n': '1', 'output_format': 'png', 'stream': 'true', 'partial_images': '1'}
body, ct = multipart(fields, {'image[]': (f'{tag}.png', bi.getvalue(), 'image/png'), 'mask': ('mask.png', bm.getvalue(), 'image/png')})
rec = {'anh': tag, 'khung_neo': EP, 'lan_thu': LAN, 'ai_image': True, 'endpoint': 'POST /v1/images/edits', 'model_req': MODEL, 'prompt': pr,
       'params': {k: v for k, v in fields.items() if k != 'prompt'}, 'mask': {'pct_duoc_sua': round(float((~prot).mean() * 100), 2), 'quy_uoc': 'alpha 0 = được sửa'},
       'input': {'pass': 'd2', 'sha256_png_gui': hashlib.sha256(bi.getvalue()).hexdigest()}, 'seed': 'API không có tham số seed',
       'date_utc': datetime.datetime.now(datetime.UTC).isoformat(timespec='seconds')}
ctx = ssl.create_default_context(cafile='/root/.ccr/ca-bundle.crt')
req = urllib.request.Request('https://api.openai.com/v1/images/edits', data=body, method='POST', headers={'Content-Type': ct})
t0 = time.time()
try:
    r = urllib.request.urlopen(req, timeout=900, context=ctx); code = r.status; dd = {}
    for line in r:
        line = line.decode('utf8', 'replace').strip()
        if not line.startswith('data:'): continue
        ev = json.loads(line[5:].strip())
        if ev.get('type', '').endswith('.completed'): dd = {'b64': ev['b64_json'], 'usage': ev.get('usage', {}), 'size': ev.get('size'), 'quality': ev.get('quality'), 'model': ev.get('model')}
        elif ev.get('type', '').endswith('partial_image'): rec['partial_events'] = rec.get('partial_events', 0) + 1
        elif 'error' in ev: dd = {'error': ev['error']}
    if 'b64' not in dd: code = 599; dd.setdefault('error', 'stream kết thúc không có ảnh')
except urllib.error.HTTPError as e:
    code = e.code; dd = {'error': e.read().decode('utf8', 'replace')[:600]}
rec['http'] = code; rec['secs'] = round(time.time() - t0, 1)
if code == 200:
    u = dd.get('usage', {}); rec['usage'] = u; det = u.get('input_tokens_details', {}) or {}
    ti = det.get('text_tokens', 0); ii = det.get('image_tokens', 0); oo = u.get('output_tokens', 0)
    usd = (ti * PRICE['text_in'] + ii * PRICE['img_in'] + oo * PRICE['img_out']) / 1e6 + rec.get('partial_events', 0) * 100 * PRICE['img_out'] / 1e6
    rec['usd'] = round(usd, 5); rec['model_resp'] = dd.get('model') or MODEL
    rec['ghi_chu_gia'] = 'usage của sự kiện completed + 100 token ra/ảnh tạm (partial) theo tài liệu'
    b = base64.b64decode(dd['b64']); fn = os.path.join(OUT, f'{tag}.png'); open(fn, 'wb').write(b)
    rec.update(file=os.path.basename(fn), sha256=hashlib.sha256(b).hexdigest(), bytes=len(b), c2pa_chunks=c2pa_chunks(b))
    rec['c2pa'] = bool(rec['c2pa_chunks'])
else:
    rec['error'] = dd.get('error'); rec['usd'] = 0.0
with open(LOG, 'a') as f: f.write(json.dumps(rec, ensure_ascii=False) + '\n')
print(tag, code, rec.get('usd'), rec.get('c2pa'), rec.get('secs'), 'tong PT2', round(spent(), 4), flush=True)
