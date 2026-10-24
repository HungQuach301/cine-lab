#!/opt/cine/bin/python -I
"""K-1.17.5 · A5 — ảnh AI THẬT cho khung đáp án BE-MAT-NHA: OpenAI POST /v1/images/edits (gpt-image-2.5-sunburst-2026-09-08, như LOOK-T4-V2), KHÔNG mặt nạ,
lệnh chỉ phủ bề mặt nhà thường. Khoá do proxy gắn cho api.openai.com — mã không đọc/in/ghi khoá; UA "CineLab-research (+https://github.com/HungQuach301/cine-lab)".
Mỗi lệnh → một dòng sổ AI reports/k1175/so-ai.jsonl (model gửi/nhận, lệnh nguyên văn, SHA vào/ra, usage, $ theo bảng giá như oai_edit.py: chữ vào $5/M, ảnh vào $8/M,
ảnh ra $30/M). Trần phiên: ≤ 6 ảnh, chặn $5.
  oai_bmn.py --img <render 1920×1080> --tag <nhãn> --out <thư mục>"""
import argparse, base64, hashlib, json, os, sys, time, urllib.error, urllib.request, uuid, io
from PIL import Image
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')); SO = os.path.join(ROOT, 'reports/k1175/so-ai.jsonl')
MODEL = 'gpt-image-2.5-sunburst-2026-09-08'; UA = 'CineLab-research (+https://github.com/HungQuach301/cine-lab)'
PROMPT = ("This is a frame from our own 3D reconstruction of a riverside town in the year 1666, seen from high above. Repaint ONLY the SURFACES of the ordinary houses so "
          "they look like a real photograph: weathered lime-plastered timber-framed walls, dark oak beams, small leaded windows, old clay-tile and grey slate roofs with "
          "moss and soot. Keep every building exactly where it is, with exactly the same outline, height, roof shape and the same number of buildings: do not add, remove, "
          "merge, split or move any building, and do not change any roof shape. Do not change the church and its tower, the bridge, the long wall, the boats, the river, "
          "the river banks, the sky or the open ground. Same camera, same framing, same perspective, same lighting direction. No people, no text, nothing modern.")
sha = lambda b: hashlib.sha256(b).hexdigest()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--img', required=True); ap.add_argument('--tag', required=True); ap.add_argument('--out', required=True); a = ap.parse_args()
    done = [json.loads(x) for x in open(SO)] if os.path.exists(SO) else []
    if len(done) >= 6 or sum(float(x.get('usd') or 0) for x in done) >= 5: sys.exit('CHẶN: trần 6 ảnh / $5 của phiên')
    os.makedirs(a.out, exist_ok=True); buf = io.BytesIO(); Image.open(a.img).convert('RGB').resize((2560, 1440), Image.LANCZOS).save(buf, 'PNG'); inp = buf.getvalue()
    params = {'model': MODEL, 'prompt': PROMPT, 'size': '2560x1440', 'quality': 'high', 'n': '1', 'output_format': 'jpeg', 'output_compression': '92', 'stream': 'true', 'partial_images': '1'}
    bnd = uuid.uuid4().hex; parts = [f'--{bnd}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode() for k, v in params.items()]
    parts.append(f'--{bnd}\r\nContent-Disposition: form-data; name="image[]"; filename="vao.png"\r\nContent-Type: image/png\r\n\r\n'.encode() + inp + b'\r\n'); parts.append(f'--{bnd}--\r\n'.encode())
    rq = urllib.request.Request('https://api.openai.com/v1/images/edits', data=b''.join(parts), headers={'Content-Type': f'multipart/form-data; boundary={bnd}', 'User-Agent': UA})
    rec = dict(nha='openai', tag=a.tag, endpoint='POST /v1/images/edits', model_req=MODEL, prompt=PROMPT, params={k: v for k, v in params.items() if k != 'prompt'},
               input=[dict(file=os.path.relpath(a.img, ROOT) if a.img.startswith(ROOT) else os.path.basename(a.img), vai='image[] (2560×1440 PNG Lanczos)', sha256_goc=sha(open(a.img, 'rb').read()), sha256_gui=sha(inp))],
               mask_pct_duoc_sua=None, date_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
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
    c2 = b'c2pa' in b or b'C2PA' in b
    rec.update(http=200, usage=u, partial_events=npart, usd=round(it.get('image_tokens', 0) * 8e-6 + it.get('text_tokens', 0) * 5e-6 + (u.get('output_tokens', 0) + 100 * npart) * 30e-6, 4),
               secs=round(time.time() - t0, 1), model_resp=d.get('model', MODEL), output=dict(file=os.path.relpath(fo, ROOT), sha256=sha(b), bytes=len(b), size='%dx%d' % Image.open(fo).size), c2pa_co_chuoi=c2)
    open(SO, 'a').write(json.dumps(rec, ensure_ascii=False) + '\n'); print(a.tag, rec['usd'], rec['secs'], rec['output'])


if __name__ == '__main__': main()
