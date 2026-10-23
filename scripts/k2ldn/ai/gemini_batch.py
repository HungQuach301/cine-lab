#!/opt/cine/bin/python -I
"""LOOK-T4-V2 · TẤM NỀN N2+ bằng Gemini ảnh qua BATCH API (ảnh tĩnh sửa KHÔNG gửi mặt nạ — Kinh thánh §15 b).
Model: gemini-nano-banana-2.1 (Nano Banana 2.1 — bản Nano Banana mới nhất có Batch; trang model đọc 23/10/2026: "Batch API Supported", 1K/2K/4K).
Gọi: POST https://generativelanguage.googleapis.com/v1beta/models/<model>:batchGenerateContent (yêu cầu nội tuyến < 20 MB), rồi hỏi trạng thái tới khi xong.
Khoá do proxy gắn cho generativelanguage.googleapis.com — mã KHÔNG đọc/in/ghi khoá; UA trung tính. HTTP 402 → DỪNG ngay (chủ dự án tự nạp).
Giá Batch (ai.google.dev/gemini-api/docs/pricing, "Last updated 2026-10-22 UTC", đọc 23/10/2026): vào $0,75/M token; ra ảnh $15/M token (2K = 1680 token ≈ $0,0252/ảnh).
Mỗi yêu cầu → một dòng sổ AI ($N2P_DIR/so-ai.jsonl): model gửi/nhận, lệnh nguyên văn, SHA vào/ra, usage, $, thời gian chờ batch, C2PA/SynthID dò trong tệp.
  gemini_batch.py --job <tên> --muc tag:anh.jpg:lenh.txt [--muc …] --out <thư mục> [--size 2K] [--poll 20] [--model gemini-nano-banana-2.1]"""
import argparse, base64, json, os, sys, time, urllib.error, urllib.request
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import n2p_lib as L  # noqa: E402

API = 'https://generativelanguage.googleapis.com/v1beta/'
GIA_VAO, GIA_RA = 0.75e-6, 15e-6
MOC, CHAN = float(os.environ.get('GEM_MOC', 5.0)), float(os.environ.get('GEM_CHAN', 8.0))


def req(url, body=None, method=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method or ('POST' if data else 'GET'), headers={'Content-Type': 'application/json', 'User-Agent': L.UA})
    try:
        with urllib.request.urlopen(r, timeout=600) as f: return f.status, json.loads(f.read() or b'{}')
    except urllib.error.HTTPError as e:
        b = e.read().decode()[:1500]
        if e.code == 402: sys.exit(f'DỪNG: HTTP 402 từ Gemini (hết tiền) — {b[:300]}')
        return e.code, {'loi': b}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--job', required=True); ap.add_argument('--muc', action='append', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--size', default='2K'); ap.add_argument('--poll', type=float, default=20); ap.add_argument('--model', default='gemini-nano-banana-2.1'); ap.add_argument('--aspect', default='16:9')
    a = ap.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    if L.tong_usd('gemini') >= CHAN: sys.exit(f'CHẶN: Gemini đã {L.tong_usd("gemini"):.2f} ≥ {CHAN}')
    items, reqs = [], []
    for m in a.muc:
        tag, img, pf = m.split(':'); prompt = Path(pf).read_text().strip(); b = Path(img).read_bytes()
        items.append(dict(tag=tag, img=img, prompt=prompt, sha_vao=L.sha(b)))
        reqs.append({'request': {'contents': [{'role': 'user', 'parts': [{'text': prompt}, {'inline_data': {'mime_type': 'image/jpeg', 'data': base64.b64encode(b).decode()}}]}],
                                 'generation_config': {'responseModalities': ['IMAGE'], 'imageConfig': {'aspectRatio': a.aspect, 'imageSize': a.size}}},
                     'metadata': {'key': tag}})
    body = {'batch': {'display_name': a.job, 'input_config': {'requests': {'requests': reqs}}}}
    t0 = time.time(); st, r = req(API + f'models/{a.model}:batchGenerateContent', body)
    if st != 200 or 'name' not in r:
        L.so_ai({'nha': 'gemini', 'job': a.job, 'endpoint': f'POST models/{a.model}:batchGenerateContent', 'http': st, 'loi': r, 'usd': 0.0}); sys.exit(f'LỖI tạo batch {st}: {str(r)[:600]}')
    name = r['name']; print('batch', name, flush=True); json.dump({'name': name, 't0': t0, 'items': [{k: v for k, v in it.items() if k != 'prompt'} for it in items]}, open(out / f'{a.job}-batch.json', 'w'))
    state = None
    while True:
        st, r = req(API + name)
        md = r.get('metadata', r); state = md.get('state') or r.get('state')
        if r.get('done') or (state and any(s in state for s in ('SUCCEEDED', 'FAILED', 'CANCELLED', 'EXPIRED'))): break
        time.sleep(a.poll)
    cho = round(time.time() - t0, 1); print('xong', state, cho, 's', flush=True)
    json.dump(r, open(out / f'{a.job}-ketqua-raw.json', 'w'))   # nguyên văn (ảnh base64 nằm trong — tệp ngoài git)
    resp = (r.get('response') or {}); inl = (resp.get('inlinedResponses') or {}).get('inlinedResponses') or resp.get('inlinedResponses') or []
    if isinstance(inl, dict): inl = inl.get('inlinedResponses', [])
    for i, it in enumerate(items):
        x = inl[i] if i < len(inl) else {}
        key = ((x.get('metadata') or {}).get('key')) or it['tag']; it = next((t for t in items if t['tag'] == key), it)
        rr = x.get('response') or {}; um = rr.get('usageMetadata') or {}
        parts = [p for c in rr.get('candidates', []) for p in (c.get('content') or {}).get('parts', [])]
        imgp = [p for p in parts if 'inlineData' in p or 'inline_data' in p]
        rec = {'nha': 'gemini', 'tag': it['tag'], 'job': a.job, 'batch': name, 'endpoint': f'POST models/{a.model}:batchGenerateContent (Batch, nội tuyến)', 'model_req': a.model,
               'model_resp': rr.get('modelVersion'), 'prompt': it['prompt'], 'params': {'imageSize': a.size, 'aspectRatio': a.aspect, 'responseModalities': ['IMAGE']},
               'input': [{'file': it['img'], 'sha256': it['sha_vao']}], 'usage': um, 'thoi_gian_cho_batch_s': cho, 'trang_thai': state}
        if not imgp:
            rec.update(usd=round(um.get('promptTokenCount', 0) * GIA_VAO, 5), loi=json.dumps(x)[:1200]); L.so_ai(rec); print(it['tag'], 'KHÔNG CÓ ẢNH', json.dumps(x)[:400]); continue
        d = imgp[0].get('inlineData') or imgp[0].get('inline_data'); b = base64.b64decode(d['data']); ext = 'png' if 'png' in d.get('mimeType', d.get('mime_type', '')) else 'jpg'
        fo = out / f"{it['tag']}-ai.{ext}"; fo.write_bytes(b)
        ra = um.get('candidatesTokenCount', 0) or 0; vao = um.get('promptTokenCount', 0) or 0
        from PIL import Image
        rec.update(usd=round(vao * GIA_VAO + ra * GIA_RA, 5), ghi_chu_gia='Batch: vào $0,75/M, ra ảnh $15/M (trang giá 2026-10-22)', output={'file': str(fo), 'sha256': L.sha(b), 'bytes': len(b), 'size': '%dx%d' % Image.open(fo).size},
                   c2pa=L.c2pa_of(b), synthid='tài liệu: "All generated images include a SynthID watermark" (image-generation, đọc 23/10/2026)')
        L.so_ai(rec); print(it['tag'], rec['usd'], rec['output']['size'], 'C2PA', rec['c2pa'], flush=True)
    tot = L.tong_usd('gemini'); print('luỹ kế Gemini $%.3f' % tot)
    if tot >= MOC: print('VƯỢT MỐC THEO DÕI Gemini $%.0f' % MOC)


if __name__ == '__main__': main()
