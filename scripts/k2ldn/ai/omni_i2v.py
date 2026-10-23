#!/opt/cine/bin/python -I
"""ANIMATIC-T3-V2 · MINH HOẠ N2 bằng Gemini Omni Flash — sinh video TỪ ẢNH ĐẦU (image-to-video) = khung render của chính shot (giữ bố cục, ánh sáng, mùa).
Dựa trên design/k2v/v2v/omni.py (NC-V2V) + bài học NC-N2P §4.3: chỉ nhận video ở bước đầu ra của mô hình, dừng chờ sau 10 phút.
Tài liệu đọc 21/10/2026: https://ai.google.dev/gemini-api/docs/omni (Last updated 2026-09-23 UTC: image-to-video qua `generation_config.video_config.task = "image_to_video"`,
  360p/720p, 1080p/4K là phóng; SynthID trong mọi video) · https://ai.google.dev/gemini-api/docs/pricing (Last updated 2026-10-19 UTC: vào $1,50/1M; ra video $17,50/1M,
  5 792 token/s 720p ≈ $0,10/s).
Khoá: proxy gắn header cho generativelanguage.googleapis.com — mã này KHÔNG đọc/đặt/in khoá. UA nghiên cứu, không email.
Sổ AI (K-LAI): reports/tien-ky-t4/so-ai-gemini.jsonl (TIEN-KY-T4) — model, ngày, lệnh nguyên văn, SHA vào/ra, usage, giá, C2PA/SynthID.
Chặn: mốc theo dõi $15; CHẶN AN TOÀN $20 (tổng sổ + $1,2 dự phòng một lượt > 20 → từ chối); HTTP 402/hết hạn mức → ghi DUNG-GEMINI, từ chối mọi lệnh sau;
cùng lỗi ≥ 3 lần liên tiếp → dừng.
  omni_i2v.py --image dau.png --prompt-file lenh.txt --out ra.mp4 --tag M1-l1 [--res 720p]"""
import argparse, base64, datetime, hashlib, json, sys, time, urllib.error, urllib.request
from pathlib import Path
REPO = Path(__file__).resolve().parents[3]; D = REPO / 'reports/tien-ky-t4'; SO = D / 'so-ai-gemini.jsonl'; STOP = D / 'DUNG-GEMINI'
API = 'https://generativelanguage.googleapis.com/v1beta'; UA = 'CineLab-research (+https://github.com/HungQuach301/cine-lab)'; MODEL = 'gemini-omni-1.1-flash'
GIA_IN, GIA_VID, GIA_TXT = 1.50e-6, 17.50e-6, 9.00e-6
MOC, CHAN, LUOT = 5.0, 10.0, 1.2   # TIEN-KY-T4: mốc $5, chặn $10 (lệnh 23/10)


def sha(b): return hashlib.sha256(b).hexdigest()
def rows(): return [json.loads(l) for l in SO.read_text().splitlines() if l.strip()] if SO.exists() else []
def tong(): return sum(float(r.get('usd') or 0) for r in rows())


def req(method, url, body=None, timeout=600):
    r = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None, method=method, headers={'User-Agent': UA, 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(r, timeout=timeout) as f: return f.status, f.read()
    except urllib.error.HTTPError as e: return e.code, e.read()
    except Exception as e: return 599, json.dumps({'loi_mang': str(e)[:300]}).encode()


def usd_of(u):
    if not u: return None
    tin = u.get('total_input_tokens') or u.get('input_tokens') or 0; out = u.get('total_output_tokens') or u.get('output_tokens') or 0
    th = u.get('total_thought_tokens') or u.get('total_reasoning_tokens') or 0; vid = None
    for k in ('output_tokens_by_modality', 'total_output_tokens_by_modality'):
        for m in u.get(k) or []:
            if str(m.get('modality', '')).lower() == 'video': vid = m.get('tokens')
    if vid is None: vid = out
    return round(tin * GIA_IN + vid * GIA_VID + (max(0, out - vid) + th) * GIA_TXT, 4)


def strip(J):
    if isinstance(J, dict): return {k: ('<b64 %d>' % len(v) if k == 'data' and isinstance(v, str) and len(v) > 200 else strip(v)) for k, v in J.items()}
    if isinstance(J, list): return [strip(x) for x in J]
    return J


def log(rec):
    D.mkdir(parents=True, exist_ok=True)
    with open(SO, 'a') as f: f.write(json.dumps(rec, ensure_ascii=False) + '\n')


def c2pa_of(b):
    dst = next((k.decode() for k in (b'trainedAlgorithmicMedia', b'compositeWithTrainedAlgorithmicMedia', b'algorithmicMedia') if k in b), None)
    return {'co_manifest': b'c2pa' in b, 'digitalSourceType': dst, 'synthid_trong_manifest': b'SynthID' in b or b'synthid' in b}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--image', required=True); ap.add_argument('--prompt-file', required=True); ap.add_argument('--out', required=True); ap.add_argument('--tag', required=True)
    ap.add_argument('--res', default='720p'); a = ap.parse_args()
    if STOP.exists(): sys.exit('DỪNG Gemini: ' + STOP.read_text())
    if tong() + LUOT > CHAN: sys.exit(f'CHẶN AN TOÀN: sổ Gemini {tong():.2f} + {LUOT} > {CHAN}')
    R = rows(); n, last = 0, None
    for r in reversed(R):
        if r.get('http') == 200 and r.get('output'): break
        k = (r.get('http'), json.dumps(r.get('loi'))[:120])
        if last is None or k == last: n, last = n + 1, k
        else: break
    if n >= 3: sys.exit(f'DỪNG: cùng lỗi {n} lần liên tiếp {last}')
    prompt = Path(a.prompt_file).read_text().strip(); img = Path(a.image).read_bytes(); mt = 'image/png' if a.image.endswith('.png') else 'image/jpeg'
    body = {'model': MODEL, 'input': [{'type': 'user_input', 'content': [{'type': 'image', 'mime_type': mt, 'data': base64.b64encode(img).decode()}, {'type': 'text', 'text': prompt}]}],
            'response_format': {'type': 'video', 'resolution': a.res, 'aspect_ratio': '16:9', 'delivery': 'uri'}, 'generation_config': {'video_config': {'task': 'image_to_video'}}, 'background': True}
    t0 = time.time(); st, raw = req('POST', f'{API}/interactions', body); J = {}
    if st == 200:
        J = json.loads(raw)
        while J.get('status') in ('in_progress', 'queued', 'pending', 'running', None) and J.get('id') and time.time() - t0 < 900:
            time.sleep(10); s2, r2 = req('GET', f"{API}/interactions/{J['id']}", timeout=120)
            if s2 == 200: J = json.loads(r2); raw = r2
            elif s2 >= 500: continue
            else: st, raw = s2, r2; break
    rec = {'tag': a.tag, 'model_req': MODEL, 'date_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'), 'nha': 'gemini', 'task': 'image_to_video', 'prompt': prompt, 'res': a.res,
           'input': [{'file': str(Path(a.image).resolve().relative_to(REPO)) if str(Path(a.image).resolve()).startswith(str(REPO)) else a.image, 'sha256': sha(img), 'bytes': len(img)}], 'http': st, 'wall_s': round(time.time() - t0, 1)}
    try: J = json.loads(raw)
    except Exception: J = {'raw': raw[:2000].decode('utf8', 'replace')}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True); Path(a.out + '.resp.json').write_text(json.dumps(strip(J), ensure_ascii=False, indent=1))
    if st != 200 or J.get('status') in ('failed', 'cancelled'):
        rec.update(loi=strip(J.get('error') or J)[:1] if isinstance(J, list) else strip(J.get('error') or J), usd=0.0); log(rec)
        if st in (402,) or 'prepay' in json.dumps(J).lower() or 'quota' in json.dumps(J).lower(): STOP.write_text(f'HTTP {st} ở {a.tag}: {json.dumps(strip(J))[:400]}\n')
        sys.exit(f'LỖI {st} {json.dumps(strip(J))[:600]}')
    if J.get('status') != 'completed':
        rec.update(loi=f"quá 15 phút, trạng thái {J.get('status')}", id=J.get('id'), usd=0.0); log(rec); sys.exit('QUÁ GIỜ ' + str(J.get('status')))
    rec.update(model_resp=J.get('model'), id=J.get('id'), status=J.get('status'), usage=J.get('usage'))
    vid = None
    for s in J.get('steps') or []:   # chỉ nhận video ở bước đầu ra của mô hình (NC-N2P §4.3)
        if s.get('type') in ('model_output', 'output', None) or s.get('role') == 'model':
            for c in s.get('content') or []:
                if c.get('type') == 'video': vid = c
    if vid is None and J.get('output_video'): vid = J['output_video']
    if not vid: rec.update(loi='không có video ở bước đầu ra', usd=usd_of(J.get('usage')) or 0.0); log(rec); sys.exit('KHÔNG CÓ VIDEO')
    if vid.get('data'): b = base64.b64decode(vid['data'])
    else:
        fid = vid['uri'].split('files/')[1].split(':')[0].split('?')[0]
        for _ in range(120):
            s2, r2 = req('GET', f'{API}/files/{fid}', timeout=120); stt = json.loads(r2).get('state') if s2 == 200 else None
            if stt == 'ACTIVE': break
            if stt == 'FAILED': rec.update(loi='file FAILED', usd=usd_of(J.get('usage')) or 0.0); log(rec); sys.exit('FILE FAILED')
            time.sleep(5)
        s2, b = req('GET', f'{API}/files/{fid}:download?alt=media', timeout=600)
        if s2 != 200: rec.update(loi=f'tải tệp HTTP {s2}', usd=usd_of(J.get('usage')) or 0.0); log(rec); sys.exit('TẢI LỖI')
    if sha(b) == sha(img): rec.update(loi='đầu ra trùng ảnh vào', usd=0.0); log(rec); sys.exit('TRÙNG ĐẦU VÀO')
    Path(a.out).write_bytes(b)
    rec.update(output={'file': str(Path(a.out).resolve().relative_to(REPO)) if str(Path(a.out).resolve()).startswith(str(REPO)) else a.out, 'sha256': sha(b), 'bytes': len(b)}, usd=usd_of(J.get('usage')), c2pa=c2pa_of(b), synthid='theo tài liệu: SynthID trong mọi video Omni')
    if rec['usd'] is None: rec['usd'] = 0.0; rec['usd_ghi_chu'] = 'không có usage trong trả lời'
    log(rec); t = tong()
    print(json.dumps({k: rec.get(k) for k in ('tag', 'id', 'model_resp', 'usd', 'output', 'wall_s', 'c2pa')}, ensure_ascii=False))
    print(f'Gemini luỹ kế ${t:.2f}' + (f' — VƯỢT MỐC THEO DÕI ${MOC:.0f}' if t >= MOC else ''), file=sys.stderr)


if __name__ == '__main__': main()
