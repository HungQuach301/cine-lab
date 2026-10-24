#!/opt/cine/bin/python -I
"""THU-B-T4 · (B) AI phủ BỀ MẶT nhà thường — OpenAI POST /v1/images/edits (gpt-image-2.5-sunburst-2026-09-08), KHÔNG mặt nạ (Kinh thánh §15 b; K-1.17.5 A5),
lời nhắc BMN v2 (năm BẮT BUỘC; chỉ bề mặt mái/tường; cấm thêm/bớt/gộp/tách/dời nhà, cấm đổi mái; cấm vật lớp (a); "không vẽ phản chiếu").
Chép khuôn reports/k1175/do/ma/oai_bmn.py (K) — đổi: lời nhắc theo khung + năm, sổ AI reports/thu-b-t4/so-ai.jsonl, trần ≤ 3 lượt/khung, mốc/chặn OpenAI của phiên.
Khoá do proxy gắn cho api.openai.com — mã không đọc/in/ghi khoá; UA "CineLab-research (+https://github.com/HungQuach301/cine-lab)".
Giá (như oai_edit.py/K): chữ vào $5/M, ảnh vào $8/M, ảnh ra $30/M (+100 token ảnh ra mỗi sự kiện ảnh từng phần).
  oai_bmn_thub.py --img <ảnh vào 1920×1080> --khung <M1-trung|M4-trung|B3-p4-1938|fac-*> --tag <nhãn> --out <thư mục> [--luot n] [--prompt-file f]"""
import argparse, base64, hashlib, json, os, sys, time, urllib.error, urllib.request, uuid, io
from PIL import Image
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')); SO = os.path.join(ROOT, 'reports/thu-b-t4/so-ai.jsonl')
MODEL = 'gpt-image-2.5-sunburst-2026-09-08'; UA = 'CineLab-research (+https://github.com/HungQuach301/cine-lab)'
MOC, CHAN = 4.0, 10.0
CAM = ("Keep every building exactly where it is, with exactly the same outline, height, roof shape and the same number of buildings: do not add, remove, merge, "
       "split or move any building, and do not add or change any roof, chimney, dormer, storey, cornice or balcony. ")
KHONG = ("Do not add anything: no people, animals, vehicles, boats, carts, smoke, fire, flags, signs, lettering, lamps, street furniture, scaffolding, trees or plants. "
         "Do not paint any reflections on water or glass. ")
KHUNG = {
 'M1-trung': dict(nam=1666, p=("This is a frame from our own 3D reconstruction of a riverside city in the year 1666, seen from a church tower about 70 m high. "
   "Repaint ONLY the SURFACES of the roofs and walls of the ordinary houses so they look like a real photograph of the year 1666: weathered lime-plastered "
   "timber-framed walls, dark oak beams, small leaded windows, old clay-tile roofs with moss and coal soot, a few grey slate and lead roofs, each house a little different. "
   + CAM + "Do not change the bridge with houses on it, the churches and their towers, the city wall, the wharves, the river, the river banks, the sky or the open ground. "
   + KHONG + "Nothing from after 1666. Same camera, same framing, same perspective, same time of day, same lighting direction and shadows.")),
 'M4-trung': dict(nam=2026, p=("This is a frame from our own 3D reconstruction of a city street in the year 2026, seen from about 19 m above the street, looking along the street "
   "towards a domed cathedral. Repaint ONLY the SURFACES of the walls and roofs of the ordinary buildings so they look like a real photograph of the year 2026: "
   "real Portland stone, red and brown brick, painted render and modern stone cladding, metal window frames with real glass, rain streaks and subtle grime, "
   "each building a little different in tone and age. " + CAM +
   "Do not change the domed cathedral, the tall towers, the street, the pavements, the trees or the sky. " + KHONG +
   "Nothing from after 2026. Same camera, same framing, same perspective, same time of day, same lighting direction and shadows.")),
 'B3-p4-1938': dict(nam=1938, p=("This is a frame from our own 3D reconstruction of a city street in the year 1938, seen from about 40 m above the street, looking along the street "
   "towards a domed cathedral. Repaint ONLY the SURFACES of the walls and roofs of the ordinary Victorian and Edwardian buildings so they look like a real photograph "
   "of the year 1938: soot-darkened Portland stone, red and yellow London stock brick, grey slate roofs, painted timber sash windows, coal grime, "
   "each building a little different in tone and age. " + CAM +
   "Do not change the domed cathedral, the churches and their towers, the street or the sky. " + KHONG +
   "Nothing from after 1938. Same camera, same framing, same perspective, same time of day, same lighting direction and shadows.")),
}
sha = lambda b: hashlib.sha256(b).hexdigest()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--img', required=True); ap.add_argument('--khung', required=True); ap.add_argument('--tag', required=True)
    ap.add_argument('--out', required=True); ap.add_argument('--luot', type=int, default=1); ap.add_argument('--prompt-file'); ap.add_argument('--size', default='2560x1440'); a = ap.parse_args()
    done = [json.loads(x) for x in open(SO)] if os.path.exists(SO) else []
    usd = sum(float(x.get('usd') or 0) for x in done if x.get('nha') == 'openai')
    if usd >= CHAN: sys.exit(f'CHẶN: OpenAI ${usd:.3f} ≥ chặn ${CHAN}')
    if usd >= MOC: print(f'CẢNH BÁO: OpenAI ${usd:.3f} ≥ mốc theo dõi ${MOC}', file=sys.stderr)
    if not a.khung.startswith('fac') and sum(1 for x in done if x.get('khung') == a.khung and x.get('http') == 200) >= 3: sys.exit('CHẶN: đã 3 lượt cho khung này (≤ 3 lượt/khung/cách)')
    if a.prompt_file: prompt = open(a.prompt_file).read().strip(); nam = None
    else: prompt = KHUNG[a.khung]['p']; nam = KHUNG[a.khung]['nam']
    W, H = map(int, a.size.split('x'))
    os.makedirs(a.out, exist_ok=True); buf = io.BytesIO(); Image.open(a.img).convert('RGB').resize((W, H), Image.LANCZOS).save(buf, 'PNG'); inp = buf.getvalue()
    params = {'model': MODEL, 'prompt': prompt, 'size': a.size, 'quality': 'high', 'n': '1', 'output_format': 'jpeg', 'output_compression': '92', 'stream': 'true', 'partial_images': '1'}
    bnd = uuid.uuid4().hex; parts = [f'--{bnd}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode() for k, v in params.items()]
    parts.append(f'--{bnd}\r\nContent-Disposition: form-data; name="image[]"; filename="vao.png"\r\nContent-Type: image/png\r\n\r\n'.encode() + inp + b'\r\n'); parts.append(f'--{bnd}--\r\n'.encode())
    rq = urllib.request.Request('https://api.openai.com/v1/images/edits', data=b''.join(parts), headers={'Content-Type': f'multipart/form-data; boundary={bnd}', 'User-Agent': UA})
    rec = dict(nha='openai', khung=a.khung, tag=a.tag, luot=a.luot, nam=nam, loi_nhac='bmn-v2-thub' if not a.prompt_file else os.path.basename(a.prompt_file), endpoint='POST /v1/images/edits',
               model_req=MODEL, prompt=prompt, params={k: v for k, v in params.items() if k != 'prompt'}, mask=None,
               input=[dict(file=os.path.relpath(a.img, ROOT) if a.img.startswith(ROOT) else a.img, vai=f'image[] ({W}×{H} PNG Lanczos)', sha256_goc=sha(open(a.img, 'rb').read()), sha256_gui=sha(inp))],
               date_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
    t0 = time.time(); d = None; npart = 0
    try:
        with urllib.request.urlopen(rq, timeout=900) as r:
            for line in r:
                line = line.decode().strip()
                if not line.startswith('data:'): continue
                ev = json.loads(line[5:].strip())
                if ev.get('type', '').endswith('partial_image'): npart += 1
                if ev.get('type', '').endswith('completed'): d = ev
        if d is None: raise RuntimeError('không có sự kiện completed')
    except urllib.error.HTTPError as e:
        rec.update(http=e.code, loi=e.read().decode()[:600], usd=0.0); open(SO, 'a').write(json.dumps(rec, ensure_ascii=False) + '\n'); sys.exit(f'LỖI {e.code}')
    u = d.get('usage', {}); it = u.get('input_tokens_details', {}) or {}
    b = base64.b64decode(d['b64_json']); fo = os.path.join(a.out, f'{a.tag}-ai.jpg'); open(fo, 'wb').write(b)
    rec.update(http=200, usage=u, partial_events=npart, usd=round(it.get('image_tokens', 0) * 8e-6 + it.get('text_tokens', 0) * 5e-6 + (u.get('output_tokens', 0) + 100 * npart) * 30e-6, 4),
               secs=round(time.time() - t0, 1), model_resp=d.get('model', MODEL), output=dict(file=os.path.relpath(fo, ROOT) if fo.startswith(ROOT) else fo, sha256=sha(b), bytes=len(b),
               size='%dx%d' % Image.open(fo).size), c2pa_co_chuoi=(b'c2pa' in b or b'C2PA' in b))
    open(SO, 'a').write(json.dumps(rec, ensure_ascii=False) + '\n'); print(a.tag, rec['usd'], rec['secs'], rec['output'])


if __name__ == '__main__': main()
