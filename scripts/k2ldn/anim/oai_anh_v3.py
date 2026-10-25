#!/opt/cine/bin/python -I
"""ANIMATIC-T4-V2 · ẢNH ĐẦU M-d v3 — OpenAI gpt-image-2.5-sunburst-2026-09-08 (bản ghim như v1).
Không tham chiếu: POST /v1/images/generations (như oai_anh.py). Có tham chiếu (nhân vật có tên, P2 = (b)): POST /v1/images/edits, image[] = chân dung thật đã duyệt
(NC-T4 NHAN-VAT-ANH.md; thu ≤ 1024 px) — lệnh nói rõ chỉ lấy trang phục/dáng, không vẽ mặt lớn. Sổ: $N2P_DIR/so-ai.jsonl (n2p_lib); mốc OpenAI $6, chặn $10 (lệnh phiên).
Khoá do proxy gắn — mã KHÔNG đọc/in/ghi khoá. Giá (developers.openai.com 21/10/2026): chữ vào $5/M, ảnh vào $8/M, ảnh ra $30/M.
  oai_anh_v3.py --prompt-file lenh.txt --tag H1-05a-a1 --out <thư mục> [--ref a.jpg --ref b.jpg] [--size 2560x1440]"""
import argparse, base64, io, json, os, sys, time, urllib.error, urllib.request, uuid
from pathlib import Path
from PIL import Image
os.environ.setdefault('N2P_DIR', str(Path(__file__).resolve().parents[3] / 'reports/animatic-t4-v2'))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'ai')); import n2p_lib as L  # noqa: E402
MODEL = 'gpt-image-2.5-sunburst-2026-09-08'; MOC, CHAN = 6.0, 10.0


def tong_openai():   # ảnh (so-ai.jsonl) + kiểm gpt-6.1-sol (cost.jsonl của vision_kiem) — cùng phiên
    c = L.N2P / 'cost.jsonl'; g = sum(json.loads(x)['usd'] for x in c.read_text().splitlines() if x.strip() and json.loads(x)['model'].startswith('gpt')) if c.exists() else 0.0
    return L.tong_usd('openai') + g


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prompt-file', required=True); ap.add_argument('--tag', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--ref', action='append', default=[]); ap.add_argument('--size', default='2560x1440'); ap.add_argument('--quality', default='high'); a = ap.parse_args()
    if tong_openai() >= CHAN: sys.exit(f'CHẶN: OpenAI phiên đã {tong_openai():.2f} ≥ {CHAN}')
    prompt = Path(a.prompt_file).read_text().strip(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    params = {'model': MODEL, 'prompt': prompt, 'size': a.size, 'quality': a.quality, 'n': 1, 'output_format': 'jpeg', 'output_compression': 92, 'stream': True, 'partial_images': 1}
    rec = {'nha': 'openai', 'tag': a.tag, 'model_req': MODEL, 'prompt': prompt, 'params': {k: v for k, v in params.items() if k != 'prompt'}, 'input': []}
    if a.ref:
        bnd = uuid.uuid4().hex; parts = []
        for k, v in params.items(): parts.append(f'--{bnd}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{str(v).lower() if isinstance(v, bool) else v}\r\n'.encode())
        for i, p in enumerate(a.ref):
            im = Image.open(p).convert('RGB'); im.thumbnail((1024, 1024), Image.LANCZOS); bio = io.BytesIO(); im.save(bio, 'PNG'); b = bio.getvalue()
            parts.append(f'--{bnd}\r\nContent-Disposition: form-data; name="image[]"; filename="ref{i}.png"\r\nContent-Type: image/png\r\n\r\n'.encode() + b + b'\r\n')
            rec['input'].append({'file': p, 'vai': 'tham chiếu trang phục/dáng (chân dung thật, PD/CC0)', 'sha256_goc': L.sha_file(p), 'sha256_gui': L.sha(b), 'px': '%dx%d' % im.size})
        parts.append(f'--{bnd}--\r\n'.encode())
        rq = urllib.request.Request('https://api.openai.com/v1/images/edits', data=b''.join(parts), headers={'Content-Type': f'multipart/form-data; boundary={bnd}', 'User-Agent': L.UA}); rec['endpoint'] = 'POST /v1/images/edits'
    else:
        rq = urllib.request.Request('https://api.openai.com/v1/images/generations', data=json.dumps(params).encode(), headers={'Content-Type': 'application/json', 'User-Agent': L.UA}); rec['endpoint'] = 'POST /v1/images/generations'
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
        rec.update(http=e.code, loi=e.read().decode()[:800], usd=0.0); L.so_ai(rec); print('LỖI', e.code, rec['loi'][:400]); sys.exit(2)
    u = d.get('usage', {}); it = u.get('input_tokens_details', {}) or {}; img_in = it.get('image_tokens', 0); txt_in = it.get('text_tokens', u.get('input_tokens', 0) - img_in); img_out = u.get('output_tokens', 0)
    b = base64.b64decode(d['b64_json']); fo = out / f'{a.tag}.jpg'; fo.write_bytes(b)
    rec.update(usage=u, partial_events=npart, usd=round(img_in * 8e-6 + txt_in * 5e-6 + (img_out + 100 * npart) * 30e-6, 4), ghi_chu_gia='usage sự kiện completed + 100 token ra/ảnh tạm (như PT3)',
               secs=round(time.time() - t0, 1), model_resp=d.get('model', MODEL), output={'file': str(fo), 'sha256': L.sha(b), 'bytes': len(b), 'size': '%dx%d' % Image.open(fo).size}, c2pa=L.c2pa_of(b))
    L.so_ai(rec); tot = tong_openai()
    print(json.dumps({'tag': a.tag, 'usd': rec['usd'], 'secs': rec['secs'], 'sha': rec['output']['sha256'][:12], 'openai_phien': round(tot, 3)}))
    if tot >= MOC: print('VƯỢT MỐC THEO DÕI OpenAI $%.0f' % MOC)


if __name__ == '__main__': main()
