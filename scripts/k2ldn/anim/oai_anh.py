#!/opt/cine/bin/python -I
"""ANIMATIC-T4 · việc 6 — ẢNH ĐẦU HOÀN THIỆN (Q3 điểm 2) cho minh hoạ M-d: OpenAI gpt-image-2.5-sunburst-2026-09-08, POST /v1/images/generations (chữ → ảnh, 2560×1440 high).
Lý do không dùng render 3D tầm người: mô hình thành phố look2 dựng cho máy ≥ 60 m; ở 2–3 m máy nằm trong khối tường (đo: H1-02, H4-04b, H1-12 → ảnh tường phẳng/khối, 24/10/2026).
Ảnh đầu qua kiểm tầng 1 (gem_kiem.py) trước khi gửi Omni. Không chạm tư liệu. Sổ: reports/animatic-t4/so-ai.jsonl (n2p_lib, N2P_DIR); mốc OpenAI $5, chặn $10 (lệnh).
Khoá do proxy gắn — mã KHÔNG đọc/in/ghi khoá. Giá như oai_edit.py (developers.openai.com 21/10/2026: chữ vào $5/M, ảnh ra $30/M).
  oai_anh.py --prompt-file lenh.txt --tag H1-02-a1 --out <thư mục> [--size 2560x1440]"""
import argparse, base64, json, os, sys, time, urllib.error, urllib.request
from pathlib import Path
from PIL import Image
os.environ.setdefault('N2P_DIR', str(Path(__file__).resolve().parents[3] / 'reports/animatic-t4'))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'ai')); import n2p_lib as L  # noqa: E402
MODEL = 'gpt-image-2.5-sunburst-2026-09-08'; MOC, CHAN = 5.0, 10.0


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prompt-file', required=True); ap.add_argument('--tag', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--size', default='2560x1440'); ap.add_argument('--quality', default='high'); a = ap.parse_args()
    if L.tong_usd('openai') >= CHAN: sys.exit(f'CHẶN: OpenAI đã {L.tong_usd("openai"):.2f} ≥ {CHAN}')
    prompt = Path(a.prompt_file).read_text().strip(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    params = {'model': MODEL, 'prompt': prompt, 'size': a.size, 'quality': a.quality, 'n': 1, 'output_format': 'jpeg', 'output_compression': 92, 'stream': True, 'partial_images': 1}
    rq = urllib.request.Request('https://api.openai.com/v1/images/generations', data=json.dumps(params).encode(), headers={'Content-Type': 'application/json', 'User-Agent': L.UA})
    rec = {'nha': 'openai', 'tag': a.tag, 'endpoint': 'POST /v1/images/generations', 'model_req': MODEL, 'prompt': prompt, 'params': {k: v for k, v in params.items() if k != 'prompt'}, 'input': []}
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
    u = d.get('usage', {}); it = u.get('input_tokens_details', {}) or {}; txt_in = it.get('text_tokens', u.get('input_tokens', 0)); img_out = u.get('output_tokens', 0)
    b = base64.b64decode(d['b64_json']); fo = out / f'{a.tag}.jpg'; fo.write_bytes(b)
    rec.update(usage=u, partial_events=npart, usd=round(txt_in * 5e-6 + (img_out + 100 * npart) * 30e-6, 4), ghi_chu_gia='usage sự kiện completed + 100 token ra/ảnh tạm (như PT3)',
               secs=round(time.time() - t0, 1), model_resp=d.get('model', MODEL), output={'file': str(fo), 'sha256': L.sha(b), 'bytes': len(b), 'size': '%dx%d' % Image.open(fo).size}, c2pa=L.c2pa_of(b))
    L.so_ai(rec); tot = L.tong_usd('openai')
    print(json.dumps({'tag': a.tag, 'usd': rec['usd'], 'secs': rec['secs'], 'sha': rec['output']['sha256'][:12], 'openai_luy_ke': round(tot, 3)}))
    if tot >= MOC: print('VƯỢT MỐC THEO DÕI OpenAI $%.0f' % MOC)


if __name__ == '__main__': main()
