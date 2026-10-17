"""PT nhánh B (H-B) — sinh vân vật liệu LÁT ĐƯỢC bằng OpenAI Images API. CHỈ 9 khe vân của phim trường (vữa, đá vôi, gạch, đá hộc,
ngói, gỗ, đất lát 1782, đá lát 1943, vải buồm/mái che). Không sinh nhà, mặt tiền, người, cờ, biển hiệu, chữ, tàu, cảnh.
Khoá API do proxy gắn cho api.openai.com — mã này KHÔNG đọc, KHÔNG in, KHÔNG ghi khoá.
  /opt/cine/bin/python -I gen_tex_b.py <out_dir> <log.jsonl> [slot ...]
Mỗi lệnh gọi ghi một dòng: model, prompt nguyên văn, thông số, ngày, usage, chi phí tính theo bảng giá đã chép (reports/pt/giay-phep/openai.md),
SHA-256 ảnh, có/không chunk C2PA (caBX / JUMBF) trong PNG."""
import sys, os, json, base64, hashlib, datetime, urllib.request, ssl, time, struct
OUT, LOG = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
MODEL = 'gpt-image-2.5-flare'; SIZE = '1024x1024'; QUALITY = 'high'
# bảng giá đọc 17/10/2026 (developers.openai.com/api/docs/pricing, Standard): image output $30/1M, text input $5/1M, image input $8/1M
PRICE = {'text_in': 5.0, 'img_in': 8.0, 'img_out': 30.0}
COMMON = ("Seamless tileable texture, orthographic flat top-down/straight-on view of a material surface only, evenly and softly lit "
          "with no shadows from objects, no perspective, no vignette, no borders, no objects, no text, no letters, no logos, no people, "
          "no buildings, no sky. The pattern must wrap perfectly on all four edges for repeating. Photographic realism, natural fine detail. Material: ")
SLOTS = {
    'vua': "old hand-applied lime plaster render on a Mediterranean house wall, off-white, subtle trowel marks, hairline cracks, slight stains, about 2 m across",
    'da_voi': "dressed pale Gibraltar limestone ashlar masonry blocks with thin lime mortar joints, weathered, about 2 m across, regular courses",
    'gach': "damaged lime plaster partly fallen away exposing old handmade red-brown bricks and rubble beneath, war-worn wall surface, about 2 m across",
    'da_hoc': "irregular rubble stone wall of grey-beige limestone with lime mortar, eighteenth-century fortification style, about 2.5 m across",
    'ngoi': "weathered terracotta Roman/curved clay roof tiles (Mediterranean barrel tiles) in regular overlapping rows, seen straight on, about 1.5 m across",
    'go': "weathered old wooden planks, sun-bleached grey-brown timber boards with grain, nail holes and worn edges, vertical boards, about 1.2 m across",
    'lat1782': "packed earth street surface with scattered small stones, dust and pebbles, eighteenth-century unpaved town street, about 3 m across",
    'lat1943': "old granite setts / cobblestone street paving in regular rows, worn and slightly dusty, early twentieth century, about 2 m across",
    'vai': "coarse natural linen sailcloth canvas, unbleached cream fabric with visible weave, slightly worn, close-up about 1 m across",
}

def c2pa_chunks(png):
    found = []; i = 8
    while i + 8 <= len(png):
        n, t = struct.unpack('>I4s', png[i:i + 8]); t = t.decode('latin1')
        if t in ('caBX', 'jumb', 'jumd') or (t in ('iTXt', 'tEXt', 'zTXt') and b'c2pa' in png[i + 8:i + 8 + n].lower()): found.append(t)
        i += 12 + n
        if t == 'IEND': break
    return found

ctx = ssl.create_default_context(cafile='/root/.ccr/ca-bundle.crt')
for slot in (sys.argv[3:] or list(SLOTS)):
    prompt = COMMON + SLOTS[slot]
    body = {'model': MODEL, 'prompt': prompt, 'size': SIZE, 'quality': QUALITY, 'n': 1, 'output_format': 'png'}
    req = urllib.request.Request('https://api.openai.com/v1/images/generations', data=json.dumps(body).encode(), method='POST',
                                 headers={'Content-Type': 'application/json'})
    t0 = time.time(); rec = {'slot': slot, 'model_req': MODEL, 'prompt': prompt, 'params': {k: v for k, v in body.items() if k != 'prompt'},
                             'seed': 'API không có tham số seed (không tái tạo được từng điểm ảnh)', 'date_utc': datetime.datetime.now(datetime.UTC).isoformat(timespec='seconds')}
    try:
        r = urllib.request.urlopen(req, timeout=300, context=ctx); code = r.status; d = json.loads(r.read())
    except urllib.error.HTTPError as e:
        code = e.code; d = {'error': e.read().decode('utf8', 'replace')[:500]}
    rec['http'] = code; rec['secs'] = round(time.time() - t0, 1)
    if code == 200:
        u = d.get('usage', {}); rec['usage'] = u
        det = u.get('input_tokens_details', {}) or {}
        ti = det.get('text_tokens', u.get('input_tokens', 0)); ii = det.get('image_tokens', 0); oo = u.get('output_tokens', 0)
        rec['usd'] = round((ti * PRICE['text_in'] + ii * PRICE['img_in'] + oo * PRICE['img_out']) / 1e6, 5)
        rec['model_resp'] = d.get('model', MODEL)
        b = base64.b64decode(d['data'][0]['b64_json']); fn = os.path.join(OUT, f'{slot}.png'); open(fn, 'wb').write(b)
        rec['file'] = os.path.basename(fn); rec['sha256'] = hashlib.sha256(b).hexdigest(); rec['bytes'] = len(b)
        rec['c2pa_chunks'] = c2pa_chunks(b); rec['c2pa'] = bool(rec['c2pa_chunks'])
        rec['revised_prompt'] = d['data'][0].get('revised_prompt')
    else:
        rec['error'] = d.get('error'); rec['usd'] = 0.0
    with open(LOG, 'a') as f: f.write(json.dumps(rec, ensure_ascii=False) + '\n')
    print(slot, code, rec.get('usd'), rec.get('c2pa'), rec.get('secs'), flush=True)
    if code in (401, 403): print('NHÁNH B CHƯA CHẠY: thiếu khoá / bị từ chối'); break
