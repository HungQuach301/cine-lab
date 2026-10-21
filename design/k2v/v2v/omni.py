#!/opt/cine/bin/python -I
"""NC-V2V · gọi Gemini Omni Flash (Interactions API) để sửa video do ta dựng — MÃ THỬ, không thuộc đường ống sản xuất.

Khoá: proxy gắn header cho host generativelanguage.googleapis.com — mã này KHÔNG đọc/đặt khoá.
Mỗi lần gọi ghi một dòng sổ AI (K-LAI-6): model, date_utc, prompt nguyên văn, input (tệp + sha256), output (tệp + sha256), usage, usd, c2pa, synthid.
Chặn chi phí: tổng usd trong sổ ≥ CHAN (40) → từ chối gọi.

  omni.py edit --video in.mp4 [--image ref.jpg …] --prompt "…" --res 720p --out ra.mp4 --tag c1a [--prev ID] [--task edit|extend]
"""
import argparse, base64, datetime, hashlib, json, os, sys, time, urllib.request, urllib.error

API = 'https://generativelanguage.googleapis.com/v1beta'
UA = 'CineLab-research (+https://github.com/HungQuach301/cine-lab)'
MODEL = 'gemini-omni-1.1-flash'
SO = os.environ.get('V2V_SO', '/home/user/cine-lab/reports/nc-v2v/so-ai.jsonl')
GIA_IN, GIA_OUT_VID, GIA_OUT_TXT = 1.50e-6, 17.50e-6, 9.00e-6   # USD/token — ai.google.dev/gemini-api/docs/pricing (đọc 19/10/2026)
MOC, CHAN = 15.0, 40.0


def sha(b): return hashlib.sha256(b).hexdigest()


def tong_usd():
    if not os.path.exists(SO): return 0.0
    return sum(float(json.loads(l).get('usd') or 0) for l in open(SO) if l.strip())


def req(method, url, body=None, timeout=1800):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method, headers={'User-Agent': UA, 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(r, timeout=timeout) as f: return f.status, f.read()
    except urllib.error.HTTPError as e: return e.code, e.read()


def get_bytes(url):
    r = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(r, timeout=600) as f: return f.read()


def usd_of(u):
    if not u: return None
    tin = u.get('total_input_tokens') or u.get('input_tokens') or 0
    out = u.get('total_output_tokens') or u.get('output_tokens') or 0
    th = u.get('total_thought_tokens') or u.get('total_reasoning_tokens') or 0
    # tách token video ra nếu có theo phương thức
    vid = None
    for k in ('output_tokens_by_modality', 'total_output_tokens_by_modality'):
        for m in u.get(k) or []:
            if str(m.get('modality', '')).lower() == 'video': vid = m.get('tokens')
    if vid is None: vid = out
    txt = max(0, out - vid) + th
    return round(tin * GIA_IN + vid * GIA_OUT_VID + txt * GIA_OUT_TXT, 4)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('cmd'); ap.add_argument('--video'); ap.add_argument('--image', action='append', default=[])
    ap.add_argument('--prompt', required=True); ap.add_argument('--res', default='720p'); ap.add_argument('--out', required=True); ap.add_argument('--tag', required=True)
    ap.add_argument('--prev'); ap.add_argument('--task'); ap.add_argument('--model', default=MODEL)
    a = ap.parse_args()
    t0u = tong_usd()
    if t0u >= CHAN: sys.exit(f'CHẶN chi phí: sổ đã {t0u:.2f} USD ≥ {CHAN}')
    content, inp = [], []
    if a.video:
        b = open(a.video, 'rb').read(); content.append({'type': 'video', 'mime_type': 'video/mp4', 'data': base64.b64encode(b).decode()}); inp.append({'file': a.video, 'sha256': sha(b), 'bytes': len(b)})
    for im in a.image:
        b = open(im, 'rb').read(); mt = 'image/png' if im.endswith('.png') else 'image/jpeg'
        content.append({'type': 'image', 'mime_type': mt, 'data': base64.b64encode(b).decode()}); inp.append({'file': im, 'sha256': sha(b), 'bytes': len(b)})
    content.append({'type': 'text', 'text': a.prompt})
    body = {'model': a.model, 'input': [{'type': 'user_input', 'content': content}], 'response_format': {'type': 'video', 'resolution': a.res, 'aspect_ratio': '16:9', 'delivery': 'uri'}}
    if a.prev: body['previous_interaction_id'] = a.prev
    if a.task: body['generation_config'] = {'video_config': {'task': a.task}}
    body['background'] = True   # gọi đồng bộ bị cắt ở 30 s (HTTP 502 'upstream request failed', 19/10) → chạy nền + hỏi trạng thái
    t0 = time.time(); st, raw = req('POST', f'{API}/interactions', body)
    if st == 200:
        J0 = json.loads(raw)
        while J0.get('status') in ('in_progress', 'queued', 'pending', 'running', None) and J0.get('id') and time.time() - t0 < 3600:
            time.sleep(10); s2, r2 = req('GET', f"{API}/interactions/{J0['id']}", timeout=300)
            if s2 == 200: J0 = json.loads(r2); raw = r2
            elif s2 >= 500: continue
            else: st, raw = s2, r2; break
    wall = time.time() - t0
    rec = {'tag': a.tag, 'model_req': a.model, 'date_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'), 'prompt': a.prompt, 'res': a.res,
           'prev': a.prev, 'task': a.task, 'input': inp, 'http': st, 'wall_s': round(wall, 1), 'c2pa': None, 'synthid': True}
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    try: J = json.loads(raw)
    except Exception: J = {'raw': raw[:2000].decode('utf8', 'replace')}
    open(a.out + '.resp.json', 'w').write(json.dumps(strip(J), ensure_ascii=False, indent=1))
    if st != 200:
        rec.update(loi=strip(J), usd=0.0); log(rec); print(json.dumps(rec, ensure_ascii=False)[:3000]); sys.exit(2)
    rec['model_resp'] = J.get('model'); rec['id'] = J.get('id'); rec['status'] = J.get('status'); rec['usage'] = J.get('usage')
    vid = None
    for s in J.get('steps') or []:
        for c in s.get('content') or []:
            if c.get('type') == 'video': vid = c
    if vid is None and J.get('output_video'): vid = J['output_video']
    if not vid: rec.update(loi='không có video trong trả lời', usd=usd_of(J.get('usage')) or 0.0); log(rec); print(json.dumps(rec, ensure_ascii=False)[:3000]); sys.exit(3)
    if vid.get('data'): b = base64.b64decode(vid['data'])
    else:
        uri = vid['uri']; fid = uri.split('files/')[1].split(':')[0].split('?')[0]
        for _ in range(240):
            s2, r2 = req('GET', f'{API}/files/{fid}', timeout=120); stt = json.loads(r2).get('state') if s2 == 200 else None
            if stt == 'ACTIVE': break
            if stt == 'FAILED': rec.update(loi='file FAILED', usd=usd_of(J.get('usage')) or 0.0); log(rec); sys.exit(4)
            time.sleep(5)
        b = get_bytes(f'{API}/files/{fid}:download?alt=media')
    open(a.out, 'wb').write(b)
    rec['output'] = {'file': a.out, 'sha256': sha(b), 'bytes': len(b)}; rec['usd'] = usd_of(J.get('usage'))
    if rec['usd'] is None: rec['usd'] = 0.0; rec['usd_ghi_chu'] = 'không có usage trong trả lời'
    log(rec); tot = tong_usd()
    print(json.dumps({k: rec[k] for k in ('tag', 'id', 'model_resp', 'usage', 'usd', 'output', 'wall_s')}, ensure_ascii=False))
    if tot >= MOC: print(f'MỐC THEO DÕI: tổng Gemini {tot:.2f} USD ≥ {MOC}', file=sys.stderr)


def strip(J):
    """bỏ dữ liệu base64 lớn khỏi bản lưu trả lời"""
    if isinstance(J, dict): return {k: ('<b64 %d>' % len(v) if k == 'data' and isinstance(v, str) and len(v) > 200 else strip(v)) for k, v in J.items()}
    if isinstance(J, list): return [strip(x) for x in J]
    return J


def log(rec):
    os.makedirs(os.path.dirname(SO), exist_ok=True)
    with open(SO, 'a') as f: f.write(json.dumps(rec, ensure_ascii=False) + '\n')


if __name__ == '__main__': main()
