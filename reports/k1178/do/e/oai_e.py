#!/opt/cine/bin/python -I
"""K-1.17.8 · LUẬT E — ảnh AI đáp án (OpenAI POST /v1/images/edits, gpt-image-2.5-sunburst-2026-09-08 — bản ghim tấm nền T4, Kinh thánh §15 (d)).
Khoá do proxy gắn cho api.openai.com — mã KHÔNG đọc/in/ghi khoá; UA trung tính (không email). KHÔNG mặt nạ (toàn khung — phương án E).
Mỗi lệnh → một dòng sổ reports/k1178/so-ai.jsonl (model gửi/nhận, lệnh nguyên văn, SHA vào/ra, usage, $ theo bảng giá dùng ở oai_edit.py
(chữ vào $5/M, ảnh vào $8/M, ảnh ra $30/M + 100 token/ảnh tạm), C2PA không đọc). Chặn: luỹ kế OpenAI của phiên ≥ $5 → từ chối.
  oai_e.py --img <png> --prompt-file <txt> --tag <nhãn> --out <thư mục>"""
import argparse, base64, hashlib, json, os, sys, time, urllib.error, urllib.request, uuid
from pathlib import Path
from PIL import Image

MODEL = 'gpt-image-2.5-sunburst-2026-09-08'; UA = 'CineLab-research (+https://github.com/HungQuach301/cine-lab)'
SO = Path(__file__).resolve().parents[2] / 'so-ai.jsonl'; CHAN = 5.0


def tong():
    if not SO.exists(): return 0.0
    return sum(float(json.loads(l).get('usd') or 0) for l in SO.read_text().splitlines() if l.strip() and json.loads(l).get('nha') == 'openai')


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--img', required=True); ap.add_argument('--prompt-file', required=True); ap.add_argument('--tag', required=True); ap.add_argument('--out', required=True)
    a = ap.parse_args()
    if tong() >= CHAN: sys.exit(f'CHẶN: OpenAI phiên đã ${tong():.2f} ≥ ${CHAN}')
    prompt = Path(a.prompt_file).read_text().strip(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    inp = out / f'{a.tag}-vao.png'; Image.open(a.img).convert('RGB').resize((2560, 1440), Image.LANCZOS).save(inp)
    bnd = uuid.uuid4().hex; parts = []
    params = {'model': MODEL, 'prompt': prompt, 'size': '2560x1440', 'quality': 'high', 'n': '1', 'output_format': 'jpeg', 'output_compression': '92', 'stream': 'true', 'partial_images': '1'}
    for k, v in params.items(): parts.append(f'--{bnd}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    parts.append(f'--{bnd}\r\nContent-Disposition: form-data; name="image[]"; filename="{inp.name}"\r\nContent-Type: image/png\r\n\r\n'.encode() + inp.read_bytes() + b'\r\n')
    parts.append(f'--{bnd}--\r\n'.encode())
    sha = lambda b: hashlib.sha256(b).hexdigest()
    rec = dict(nha='openai', tag=a.tag, endpoint='POST /v1/images/edits', model_req=MODEL, prompt=prompt, params={k: v for k, v in params.items() if k != 'prompt'},
               input=[dict(file=str(inp), vai='image[]', sha256=sha(inp.read_bytes()))], goc=dict(file=a.img, sha256=sha(open(a.img, 'rb').read())), mask=None,
               date_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
    rq = urllib.request.Request('https://api.openai.com/v1/images/edits', data=b''.join(parts), headers={'Content-Type': f'multipart/form-data; boundary={bnd}', 'User-Agent': UA})
    t0 = time.time(); d = None; npart = 0
    try:
        with urllib.request.urlopen(rq, timeout=900) as r:
            for line in r:
                line = line.decode().strip()
                if not line.startswith('data:'): continue
                ev = json.loads(line[5:].strip())
                if ev.get('type', '').endswith('partial_image'): npart += 1
                if ev.get('type', '').endswith('completed'): d = ev
        rec['http'] = 200
        if d is None: raise RuntimeError('không có sự kiện completed')
    except urllib.error.HTTPError as e:
        rec.update(http=e.code, loi=e.read().decode()[:800], usd=0.0); open(SO, 'a').write(json.dumps(rec, ensure_ascii=False) + '\n'); print('LỖI', e.code, rec['loi'][:300]); sys.exit(2)
    u = d.get('usage', {}); it = u.get('input_tokens_details', {}) or {}
    b = base64.b64decode(d['b64_json']); fo = out / f'{a.tag}-ai.jpg'; fo.write_bytes(b)
    rec.update(usage=u, partial_events=npart, usd=round(it.get('image_tokens', 0) * 8e-6 + it.get('text_tokens', 0) * 5e-6 + (u.get('output_tokens', 0) + 100 * npart) * 30e-6, 4),
               secs=round(time.time() - t0, 1), model_resp=d.get('model', MODEL), output=dict(file=str(fo), sha256=sha(b), bytes=len(b), size='%dx%d' % Image.open(fo).size))
    open(SO, 'a').write(json.dumps(rec, ensure_ascii=False) + '\n'); print(a.tag, rec['http'], rec['usd'], rec['secs'], 'luỹ kế OpenAI $%.3f' % tong())


if __name__ == '__main__':
    main()
