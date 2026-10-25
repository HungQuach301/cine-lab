#!/opt/cine/bin/python -I
"""ANIMATIC-T4 · việc 6 — minh hoạ M-d bằng Gemini Omni Flash, image-to-video TỪ ẢNH ĐẦU (+ ảnh cuối nếu có: chế độ đầu + cuối, Q3).
Gọi như scripts/k2ldn/ai/omni_i2v.py (ANIMATIC-T3-V2) nhưng: sổ AI + ngân sách T4 qua gem_lib (chặn $35 tổng T4, mốc $30; 402 → dừng ngay);
độ phân giải mặc định 360p (Q3: nháp độ phân giải thấp nhất có được); prompt có khung thời gian [0-Ns] để clip đúng độ dài (Q3).
Tài liệu đọc 24/10/2026: https://ai.google.dev/gemini-api/docs/omni (bản .md.txt SHA a7a2002c…): interactions API; `response_format.resolution` 360p/720p (1080p/4k là phóng);
hai ảnh = khung đầu + khung cuối; `generation_config.video_config.task`; "All generated videos include SynthID watermarking".
  omni.py --dau dau.jpg [--cuoi cuoi.jpg] --prompt-file lenh.txt --out ra.mp4 --tag H1-02-l1 [--res 360p]"""
import argparse, base64, json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent)); import gem_lib as G  # noqa: E402
MODEL = 'gemini-omni-1.1-flash'


def strip(J):
    if isinstance(J, dict): return {k: ('<b64 %d>' % len(v) if k == 'data' and isinstance(v, str) and len(v) > 200 else strip(v)) for k, v in J.items()}
    if isinstance(J, list): return [strip(x) for x in J]
    return J


def c2pa_of(b):
    dst = next((k.decode() for k in (b'trainedAlgorithmicMedia', b'compositeWithTrainedAlgorithmicMedia', b'algorithmicMedia') if k in b), None)
    return {'co_manifest': b'c2pa' in b, 'digitalSourceType': dst}


def rel(p):
    p = Path(p).resolve(); return str(p.relative_to(G.REPO)) if str(p).startswith(str(G.REPO)) else str(p)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--dau', required=True); ap.add_argument('--cuoi'); ap.add_argument('--prompt-file', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--tag', required=True); ap.add_argument('--res', default='360p'); a = ap.parse_args()
    G.kiem_truoc(1.2 if a.res == '720p' else 0.5)
    prompt = Path(a.prompt_file).read_text().strip(); imgs = [Path(a.dau)] + ([Path(a.cuoi)] if a.cuoi else [])
    content = [{'type': 'image', 'mime_type': 'image/png' if str(p).endswith('.png') else 'image/jpeg', 'data': base64.b64encode(p.read_bytes()).decode()} for p in imgs] + [{'type': 'text', 'text': prompt}]
    body = {'model': MODEL, 'input': [{'type': 'user_input', 'content': content}], 'response_format': {'type': 'video', 'resolution': a.res, 'aspect_ratio': '16:9', 'delivery': 'uri'},
            'generation_config': {'video_config': {'task': 'image_to_video'}}, 'background': True}
    t0 = time.time(); st, raw = G.req('POST', f'{G.API}/interactions', body); J = {}
    if st == 200:
        J = json.loads(raw)
        while J.get('status') in ('in_progress', 'queued', 'pending', 'running', None) and J.get('id') and time.time() - t0 < 900:
            time.sleep(10); s2, r2 = G.req('GET', f"{G.API}/interactions/{J['id']}", timeout=120)
            if s2 == 200: J = json.loads(r2); raw = r2
            elif s2 >= 500: continue
            else: st, raw = s2, r2; break
    rec = {'tag': a.tag, 'nha': 'gemini', 'model_req': MODEL, 'task': 'image_to_video' + ('+cuoi' if a.cuoi else ''), 'prompt': prompt, 'res': a.res,
           'input': [{'file': rel(p), 'sha256': G.sha(p.read_bytes()), 'bytes': p.stat().st_size} for p in imgs], 'http': st, 'wall_s': round(time.time() - t0, 1)}
    try: J = json.loads(raw)
    except Exception: J = {'raw': raw[:2000].decode('utf8', 'replace')}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True); Path(a.out + '.resp.json').write_text(json.dumps(strip(J), ensure_ascii=False, indent=1))
    if st != 200 or J.get('status') in ('failed', 'cancelled'):
        rec.update(loi=strip(J.get('error') or J) if isinstance(J, dict) else str(J)[:500], usd=0.0); G.log(rec); G.dung_neu_402(st, J, a.tag); sys.exit(f'LỖI {st} {json.dumps(strip(J))[:600]}')
    if J.get('status') != 'completed': rec.update(loi=f"quá 15 phút, trạng thái {J.get('status')}", id=J.get('id'), usd=0.0); G.log(rec); sys.exit('QUÁ GIỜ')
    rec.update(model_resp=J.get('model'), id=J.get('id'), status=J.get('status'), usage=J.get('usage'))
    vid = None
    for s in J.get('steps') or []:
        if s.get('type') in ('model_output', 'output', None) or s.get('role') == 'model':
            for c in s.get('content') or []:
                if c.get('type') == 'video': vid = c
    if not vid: rec.update(loi='không có video ở bước đầu ra', usd=G.usd_of(MODEL, J.get('usage')) or 0.0); G.log(rec); sys.exit('KHÔNG CÓ VIDEO')
    if vid.get('data'): b = base64.b64decode(vid['data'])
    else:
        fid = vid['uri'].split('files/')[1].split(':')[0].split('?')[0]
        for _ in range(120):
            s2, r2 = G.req('GET', f'{G.API}/files/{fid}', timeout=120); stt = json.loads(r2).get('state') if s2 == 200 else None
            if stt == 'ACTIVE': break
            if stt == 'FAILED': rec.update(loi='file FAILED', usd=G.usd_of(MODEL, J.get('usage')) or 0.0); G.log(rec); sys.exit('FILE FAILED')
            time.sleep(5)
        s2, b = G.req('GET', f'{G.API}/files/{fid}:download?alt=media', timeout=600)
        if s2 != 200: rec.update(loi=f'tải tệp HTTP {s2}', usd=G.usd_of(MODEL, J.get('usage')) or 0.0); G.log(rec); sys.exit('TẢI LỖI')
    Path(a.out).write_bytes(b)
    rec.update(output={'file': rel(a.out), 'sha256': G.sha(b), 'bytes': len(b)}, usd=G.usd_of(MODEL, J.get('usage')), c2pa=c2pa_of(b), synthid='theo tài liệu: SynthID trong mọi video Omni')
    if rec['usd'] is None: rec['usd'] = 0.0; rec['usd_ghi_chu'] = 'không có usage trong trả lời'
    G.log(rec)
    print(json.dumps({k: rec.get(k) for k in ('tag', 'usd', 'output', 'wall_s', 'c2pa')}, ensure_ascii=False)); print(f'Gemini T4 luỹ kế ${G.tong_t4():.2f}', file=sys.stderr)


if __name__ == '__main__': main()
