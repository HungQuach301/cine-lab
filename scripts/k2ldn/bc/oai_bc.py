#!/opt/cine/bin/python -I
"""BAN-CUOI-T4-A · OpenAI gpt-image-2.5-sunburst-2026-09-08 POST /v1/images/edits — KHÔNG mặt nạ.
image[] đầu = ảnh vào (render 3D của dự án, toàn khung) ; image[] sau = chân dung tham chiếu (chỉ trang phục/dáng; thu ≤ 1024 px).
Dùng cho (1) tấm E toàn khung (việc 1) và (2) ảnh đầu M-d dựng từ render 3D cùng năm (việc 4). Khoá do proxy gắn — mã KHÔNG đọc/in/ghi khoá; UA trung tính.
Sổ: $N2P_DIR/so-ai.jsonl (mặc định reports/ban-cuoi-t4-a) — model gửi/nhận, lệnh nguyên văn, SHA vào/ra, usage, $ (chữ vào $5/M, ảnh vào $8/M, ảnh ra $30/M + 100 token/ảnh tạm),
C2PA. Mốc OpenAI $5, chặn $10 (cộng cả cost.jsonl mô hình nhìn gpt của phiên).
  oai_bc.py --img render.png --prompt-file lenh.txt --tag P9-2026-E-ngay-l1 --out <thư mục> [--ref a.jpg …] [--size 2560x1440]"""
import argparse, base64, io, json, os, sys, time, urllib.error, urllib.request, uuid
from pathlib import Path
from PIL import Image
REPO = Path(__file__).resolve().parents[3]
os.environ.setdefault('N2P_DIR', str(REPO / 'reports/ban-cuoi-t4-a'))
sys.path.insert(0, str(REPO / 'scripts/k2ldn/ai')); import n2p_lib as L  # noqa: E402
MODEL = 'gpt-image-2.5-sunburst-2026-09-08'; MOC, CHAN = 5.0, 10.0


def tong_openai():
    c = L.N2P / 'cost.jsonl'
    g = sum(json.loads(x)['usd'] for x in c.read_text().splitlines() if x.strip() and json.loads(x)['model'].startswith('gpt')) if c.exists() else 0.0
    return L.tong_usd('openai') + g


def png_bytes(p, maxpx=None, size=None):
    im = Image.open(p).convert('RGB')
    if size: im = im.resize(size, Image.LANCZOS)
    if maxpx: im.thumbnail((maxpx, maxpx), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'PNG'); return b.getvalue(), im.size


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--img', required=True); ap.add_argument('--prompt-file', required=True); ap.add_argument('--tag', required=True)
    ap.add_argument('--out', required=True); ap.add_argument('--ref', action='append', default=[]); ap.add_argument('--size', default='2560x1440'); a = ap.parse_args()
    if tong_openai() >= CHAN: sys.exit(f'CHẶN: OpenAI phiên đã {tong_openai():.2f} ≥ {CHAN}')
    prompt = Path(a.prompt_file).read_text().strip(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    W, H = map(int, a.size.split('x'))
    params = {'model': MODEL, 'prompt': prompt, 'size': a.size, 'quality': 'high', 'n': '1', 'output_format': 'jpeg', 'output_compression': '92', 'stream': 'true', 'partial_images': '1'}
    bnd = uuid.uuid4().hex; parts = [f'--{bnd}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode() for k, v in params.items()]
    rec = {'nha': 'openai', 'tag': a.tag, 'endpoint': 'POST /v1/images/edits', 'model_req': MODEL, 'prompt': prompt, 'params': {k: v for k, v in params.items() if k != 'prompt'}, 'mask': None, 'input': []}
    b, sz = png_bytes(a.img, size=(W, H))
    parts.append(f'--{bnd}\r\nContent-Disposition: form-data; name="image[]"; filename="vao.png"\r\nContent-Type: image/png\r\n\r\n'.encode() + b + b'\r\n')
    rec['input'].append({'file': str(a.img), 'vai': 'ảnh vào (render 3D của dự án)', 'sha256_goc': L.sha_file(a.img), 'sha256_gui': L.sha(b), 'px': '%dx%d' % sz})
    for i, p in enumerate(a.ref):
        b, sz = png_bytes(p, maxpx=1024)
        parts.append(f'--{bnd}\r\nContent-Disposition: form-data; name="image[]"; filename="ref{i}.png"\r\nContent-Type: image/png\r\n\r\n'.encode() + b + b'\r\n')
        rec['input'].append({'file': p, 'vai': 'tham chiếu trang phục/dáng (chân dung thật, PD/CC0)', 'sha256_goc': L.sha_file(p), 'sha256_gui': L.sha(b), 'px': '%dx%d' % sz})
    parts.append(f'--{bnd}--\r\n'.encode())
    rq = urllib.request.Request('https://api.openai.com/v1/images/edits', data=b''.join(parts), headers={'Content-Type': f'multipart/form-data; boundary={bnd}', 'User-Agent': L.UA})
    rec['date_utc'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()); t0 = time.time(); d = None; npart = 0
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
        rec.update(http=e.code, loi=e.read().decode()[:800], usd=0.0); L.so_ai(rec); print('LỖI', e.code, rec['loi'][:400]); sys.exit(2)
    u = d.get('usage', {}); it = u.get('input_tokens_details', {}) or {}; img_in = it.get('image_tokens', 0); txt_in = it.get('text_tokens', u.get('input_tokens', 0) - img_in)
    b = base64.b64decode(d['b64_json']); fo = out / f'{a.tag}.jpg'; fo.write_bytes(b)
    rec.update(usage=u, partial_events=npart, usd=round(img_in * 8e-6 + txt_in * 5e-6 + (u.get('output_tokens', 0) + 100 * npart) * 30e-6, 4), secs=round(time.time() - t0, 1),
               model_resp=d.get('model', MODEL), output={'file': str(fo), 'sha256': L.sha(b), 'bytes': len(b), 'size': '%dx%d' % Image.open(fo).size}, c2pa=L.c2pa_of(b))
    L.so_ai(rec); tot = tong_openai()
    print(json.dumps({'tag': a.tag, 'usd': rec['usd'], 'secs': rec['secs'], 'sha': rec['output']['sha256'][:12], 'openai_phien': round(tot, 3)}))
    if tot >= MOC: print('VƯỢT MỐC THEO DÕI OpenAI $%.0f' % MOC)


if __name__ == '__main__': main()
