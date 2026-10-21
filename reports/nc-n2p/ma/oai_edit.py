#!/opt/cine/bin/python -I
"""NC-N2P · O1 — OpenAI sửa ảnh CÓ MẶT NẠ (POST /v1/images/edits, gpt-image-2.5-sunburst-2026-09-08 — cùng bản ghim với PT3/ĐÓNG-GÓI v2).
Khoá do proxy gắn cho api.openai.com — mã KHÔNG đọc/in/ghi khoá; UA trung tính. Mặt nạ: alpha 0 = vùng ĐƯỢC sửa (lớp (c) nền), alpha 255 = giữ (lớp (a)).
Mỗi lệnh → một dòng sổ AI reports/nc-n2p/so-ai.jsonl (model gửi/nhận, ngày, lệnh nguyên văn, SHA vào/ra, % mặt nạ được sửa, usage, $ theo bảng giá
developers.openai.com/api/docs/pricing đọc 21/10/2026: chữ vào $5/M, ảnh vào $8/M, ảnh ra $30/M; C2PA đọc từ tệp ra).
Mốc theo dõi $5 (ghi lợi ích rồi làm tiếp); CHẶN an toàn $20 → từ chối gọi.
  oai_edit.py --img <ảnh 1920×1080> [--mask <mask-rgba.png>] --prompt-file <tệp> --tag <nhãn> --out <thư mục> [--size 2560x1440]"""
import argparse, base64, json, sys, time, urllib.error, urllib.request, uuid
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parent))
import n2p_lib as L  # noqa: E402

MODEL = 'gpt-image-2.5-sunburst-2026-09-08'; MOC, CHAN = 5.0, 20.0


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--img', required=True); ap.add_argument('--mask'); ap.add_argument('--prompt-file', required=True)
    ap.add_argument('--tag', required=True); ap.add_argument('--out', required=True); ap.add_argument('--size', default='2560x1440'); ap.add_argument('--quality', default='high'); ap.add_argument('--fidelity', default=None, help='input_fidelity (high|low) — giữ đặc điểm ảnh vào')
    a = ap.parse_args()
    if L.tong_usd('openai') >= CHAN: sys.exit(f'CHẶN: OpenAI đã {L.tong_usd("openai"):.2f} ≥ {CHAN}')
    prompt = Path(a.prompt_file).read_text().strip(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True); w, h = map(int, a.size.split('x'))
    inp = out / f'{a.tag}-vao.png'; Image.open(a.img).convert('RGB').resize((w, h), Image.LANCZOS).save(inp)
    files = [('image[]', inp)]; mpct = None
    if a.mask:
        mk = out / f'{a.tag}-mask.png'; m = Image.open(a.mask).convert('RGBA').resize((w, h), Image.NEAREST); m.save(mk); files.append(('mask', mk))
        import numpy as np; al = np.array(m)[:, :, 3]; mpct = round(float((al == 0).mean() * 100), 2)
    bnd = uuid.uuid4().hex; parts = []
    params = {'model': MODEL, 'prompt': prompt, 'size': a.size, 'quality': a.quality, 'n': '1', 'output_format': 'jpeg', 'output_compression': '92', 'stream': 'true', 'partial_images': '1'}
    if a.fidelity: params['input_fidelity'] = a.fidelity
    for k, v in params.items(): parts.append(f'--{bnd}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    for nm, p in files: parts.append(f'--{bnd}\r\nContent-Disposition: form-data; name="{nm}"; filename="{p.name}"\r\nContent-Type: image/png\r\n\r\n'.encode() + p.read_bytes() + b'\r\n')
    parts.append(f'--{bnd}--\r\n'.encode())
    rq = urllib.request.Request('https://api.openai.com/v1/images/edits', data=b''.join(parts), headers={'Content-Type': f'multipart/form-data; boundary={bnd}', 'User-Agent': L.UA})
    rec = {'nha': 'openai', 'tag': a.tag, 'endpoint': 'POST /v1/images/edits', 'model_req': MODEL, 'prompt': prompt, 'params': {k: v for k, v in params.items() if k != 'prompt'},
           'input': [{'file': str(p.relative_to(L.REPO)) if str(p).startswith(str(L.REPO)) else str(p), 'vai': nm, 'sha256': L.sha_file(p)} for nm, p in files], 'goc': {'file': a.img, 'sha256': L.sha_file(a.img)},
           'mask_pct_duoc_sua': mpct}
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
    u = d.get('usage', {}); it = u.get('input_tokens_details', {}) or {}; img_in = it.get('image_tokens', 0); txt_in = it.get('text_tokens', 0); img_out = u.get('output_tokens', 0)
    b = base64.b64decode(d['b64_json']); fo = out / f'{a.tag}-ai.jpg'; fo.write_bytes(b)
    rec.update(usage=u, partial_events=npart, usd=round(img_in * 8e-6 + txt_in * 5e-6 + (img_out + 100 * npart) * 30e-6, 4), ghi_chu_gia='usage sự kiện completed + 100 token ra/ảnh tạm (như PT3)',
               secs=round(time.time() - t0, 1), model_resp=d.get('model', MODEL), output={'file': str(fo.relative_to(L.REPO)) if str(fo).startswith(str(L.REPO)) else str(fo), 'sha256': L.sha(b), 'bytes': len(b),
               'size': '%dx%d' % Image.open(fo).size}, c2pa=L.c2pa_of(b), synthid=None)
    L.so_ai(rec); tot = L.tong_usd('openai')
    print(a.tag, rec['http'], rec['usd'], rec['secs'], 'C2PA', rec['c2pa'], 'luỹ kế OpenAI $%.3f' % tot)
    if tot >= MOC: print('VƯỢT MỐC THEO DÕI OpenAI $%.0f' % MOC)


if __name__ == '__main__': main()
