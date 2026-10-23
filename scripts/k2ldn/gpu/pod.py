#!/opt/cine/bin/python
# TIEN-KY-T4: bản sao scripts/k2tl/cuoi_gpu/pod.py — chỉ đổi đường sổ giờ + trạng thái (reports/tien-ky-t4/gio-gpu.jsonl, /var/tmp/ldn/gpu/pod.json).
"""NC-GPU · điều khiển pod RunPod từ container (khoá do proxy gắn cho rest.runpod.io / api.runpod.io — mã này KHÔNG đọc, in hay ghi khoá).
Sổ giờ GPU (bật/tắt, giá, số dư trước/sau): reports/nc-gpu/gio-gpu.jsonl. Trạng thái pod đang chạy (có mã TOK một lần): $NCG_STATE (ngoài git).
  pod.py gia [id…]                      giá + tình trạng kho từng loại GPU (GraphQL gpuTypes)
  pod.py len <gpuTypeId> <SECURE|COMMUNITY> <nhãn> [đĩa GB]   tạo pod (python:3.13-slim + pod_srv.py) → chờ /ping
  pod.py put <tệp/thư mục cục bộ> <đường trên pod>   tải lên theo khúc 64 MB (thư mục: từng tệp), kiểm SHA-256
  pod.py get <đường trên pod> <tệp cục bộ>           tải về theo khúc, kiểm SHA-256
  pod.py run '<lệnh bash>' [--cho]      chạy nền trên pod; --cho: chờ xong, in đuôi log
  pod.py log <id> [n]  ·  pod.py ls <thư mục>  ·  pod.py tat          xoá pod, ghi giờ tắt + tiền
UA: "CineLab-research (+https://github.com/HungQuach301/cine-lab)" — không email trong header/URL/payload."""
import sys, os, json, time, base64, secrets, hashlib, urllib.request, urllib.error, datetime
UA = 'CineLab-research (+https://github.com/HungQuach301/cine-lab)'
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '../../..'))   # scripts/k2ldn/gpu → gốc repo
LEDGER = os.path.join(REPO, 'reports/tien-ky-t4/gio-gpu.jsonl')
STATE = os.environ.get('NCG_STATE', '/var/tmp/ldn/gpu/pod.json')
CH = 64 << 20

def now(): return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def req(url, data=None, method=None, headers=None, timeout=300):
    h = {'User-Agent': UA}; h.update(headers or {})
    r = urllib.request.Request(url, data=data, method=method, headers=h)
    for k in range(5):
        try:
            with urllib.request.urlopen(r, timeout=timeout) as f: return f.status, f.read()
        except urllib.error.HTTPError as e:
            b = e.read()
            if e.code in (502, 503, 504, 524) and k < 4: time.sleep(2 ** (k + 1)); continue
            return e.code, b
        except Exception:
            if k < 4: time.sleep(2 ** (k + 1)); continue
            raise
def gql(q):
    s, b = req('https://api.runpod.io/graphql', json.dumps({'query': q}).encode(), 'POST', {'Content-Type': 'application/json'})
    return json.loads(b)
def balance(): return gql('{ myself { clientBalance currentSpendPerHr } }')['data']['myself']
def ledger(rec):
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True); open(LEDGER, 'a').write(json.dumps(rec, ensure_ascii=False) + '\n')
def st(): return json.load(open(STATE))
def base(): s = st(); return f"https://{s['id']}-8888.proxy.runpod.net", {'X-Tok': s['tok']}

def gia(ids):
    out = []
    for i in ids:
        d = gql('{ gpuTypes(input:{id:"%s"}) { id displayName memoryInGb securePrice communityPrice secureSpotPrice lowestPrice(input:{gpuCount:1, secureCloud:true}) { uninterruptablePrice stockStatus maxUnreservedGpuCount availableGpuCounts } } }' % i)
        g = d['data']['gpuTypes'][0]; dc = gql('{ gpuTypes(input:{id:"%s"}) { lowestPrice(input:{gpuCount:1, secureCloud:false}) { uninterruptablePrice stockStatus } } }' % i)['data']['gpuTypes'][0]
        g['community'] = dc['lowestPrice']; out.append(g); print(json.dumps(g, ensure_ascii=False))
    return out

def len_(gpu, cloud, lab, disk=60):
    tok = secrets.token_hex(24); srv = base64.b64encode(open(os.path.join(HERE, 'pod_srv.py'), 'rb').read()).decode()
    body = {'name': f'cinelab-t4-{lab}', 'imageName': 'python:3.13-slim-bookworm', 'gpuTypeIds': [gpu], 'gpuCount': 1, 'cloudType': cloud,
            'containerDiskInGb': int(disk), 'volumeInGb': 0, 'ports': ['8888/http'], 'interruptible': False,
            'env': {'TOK': tok, 'SRV': srv, 'NVIDIA_DRIVER_CAPABILITIES': 'all'},
            'dockerStartCmd': ['python3', '-c', "import os,base64;exec(base64.b64decode(os.environ['SRV']))"]}
    b0 = balance(); t0 = now(); s, b = req('https://rest.runpod.io/v1/pods', json.dumps(body).encode(), 'POST', {'Content-Type': 'application/json'})
    if s >= 300:
        msg = b.decode('utf-8', 'replace')[:800]; ledger({'su_kien': 'tao_loi', 'gpu': gpu, 'cloud': cloud, 'luc': t0, 'http': s, 'nguyen_van': msg}); print('LỖI', s, msg); sys.exit(2)
    P = json.loads(b); os.makedirs(os.path.dirname(STATE), exist_ok=True)
    json.dump({'id': P['id'], 'tok': tok, 'gpu': gpu, 'cloud': cloud, 'lab': lab, 'bat': t0, 'gia_h': P.get('costPerHr'), 'du_truoc': b0['clientBalance']}, open(STATE, 'w'))
    ledger({'su_kien': 'bat', 'pod': P['id'], 'gpu': gpu, 'cloud': cloud, 'nhan': lab, 'luc': t0, 'gia_h': P.get('costPerHr'), 'so_du_truoc': b0['clientBalance'], 'machine': P.get('machine', {}).get('gpuDisplayName') if isinstance(P.get('machine'), dict) else None})
    print('POD', P['id'], 'gia/h', P.get('costPerHr')); u, h = base(); t1 = time.time()
    while time.time() - t1 < 900:
        try:
            s, b = req(u + '/ping', timeout=20)
            if s == 200: print('SAN SANG sau', round(time.time() - t1), 's'); ledger({'su_kien': 'san_sang', 'pod': P['id'], 'luc': now(), 'cho_s': round(time.time() - t1)}); return
        except Exception: pass
        time.sleep(10)
    print('KHÔNG LÊN sau 15 phút — tắt'); tat()

def tat():
    s = st(); t = now(); code, b = req(f"https://rest.runpod.io/v1/pods/{s['id']}", method='DELETE')
    time.sleep(3); b1 = balance(); h = (datetime.datetime.fromisoformat(t.replace('Z', '+00:00')) - datetime.datetime.fromisoformat(s['bat'].replace('Z', '+00:00'))).total_seconds() / 3600
    rec = {'su_kien': 'tat', 'pod': s['id'], 'gpu': s['gpu'], 'cloud': s['cloud'], 'nhan': s['lab'], 'bat': s['bat'], 'tat': t, 'gio': round(h, 4), 'gia_h': s.get('gia_h'),
           'tien_uoc': round(h * (s.get('gia_h') or 0), 3), 'so_du_truoc': s.get('du_truoc'), 'so_du_sau': b1['clientBalance'], 'http_xoa': code}
    ledger(rec); print(json.dumps(rec, ensure_ascii=False)); os.rename(STATE, STATE + '.' + s['id'])

def sha_local(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 22), b''): h.update(c)
    return h.hexdigest()
def put1(lp, rp):
    u, h = base(); n = os.path.getsize(lp); off = 0
    with open(lp, 'rb') as f:
        while True:
            b = f.read(CH)
            if not b and off > 0: break
            s, r = req(f"{u}/f/{rp}?off={off}", b, 'PUT', dict(h, **{'Content-Type': 'application/octet-stream'}))
            if s != 200: raise SystemExit(f'PUT {rp} {s} {r[:200]}')
            off += len(b)
            if not b: break
    s, r = req(f"{u}/sha/{rp}", headers=h); rs = json.loads(r)
    if rs['sha'] != sha_local(lp): raise SystemExit(f'SHA lệch {rp}')
    return n
def put(lp, rp):
    t = time.time(); tot = 0
    if os.path.isdir(lp):
        for r, _, fs in os.walk(lp):
            for x in sorted(fs): fp = os.path.join(r, x); tot += put1(fp, rp.rstrip('/') + '/' + os.path.relpath(fp, lp))
    else: tot = put1(lp, rp)
    dt = time.time() - t; print(json.dumps({'len_MB': round(tot / 1e6, 1), 's': round(dt, 1), 'MB_s': round(tot / 1e6 / max(dt, 1e-3), 1)})); return tot, dt
def get(rp, lp):
    u, h = base(); s, r = req(f"{u}/sha/{rp}", headers=h); rs = json.loads(r); n = rs['n']; off = 0; t = time.time()
    os.makedirs(os.path.dirname(os.path.abspath(lp)), exist_ok=True)
    with open(lp, 'wb') as f:
        while off < n:
            s, b = req(f"{u}/f/{rp}?off={off}&n={min(CH, n - off)}", headers=h)
            if s != 200: raise SystemExit(f'GET {rp} {s}')
            f.write(b); off += len(b)
    if sha_local(lp) != rs['sha']: raise SystemExit(f'SHA lệch {rp}')
    return n, time.time() - t
def run(cmd, wait=False):
    u, h = base(); s, r = req(u + '/run', cmd.encode(), 'POST', h); jid = json.loads(r)['id']; print('VIEC', jid)
    if wait:
        while True:
            time.sleep(10); s, r = req(f'{u}/log/{jid}?tail=3000', headers=h); j = json.loads(r)
            if j['xong']: print(j['log']); print('MA', j['ma']); return j
    return jid

if __name__ == '__main__':
    a = sys.argv[1:]; c = a[0]
    if c == 'gia': gia(a[1:])
    elif c == 'len': len_(a[1], a[2], a[3], *(a[4:5]))
    elif c == 'tat': tat()
    elif c == 'put': put(a[1], a[2])
    elif c == 'get': n, dt = get(a[1], a[2]); print(json.dumps({'MB': round(n / 1e6, 1), 's': round(dt, 1)}))
    elif c == 'run': run(a[1], '--cho' in a)
    elif c == 'log': u, h = base(); s, r = req(f'{u}/log/{a[1]}?tail={a[2] if len(a) > 2 else 3000}', headers=h); j = json.loads(r); print(j['log']); print('XONG', j['xong'], 'MA', j['ma'])
    elif c == 'ls': u, h = base(); s, r = req(f'{u}/ls/{a[1]}', headers=h); print(r.decode())   # KHÔNG cắt: cắt 4000 ký tự làm hỏng JSON khi > ~147 tệp → dk_pod.sh không kéo được khung nào (sự cố 22/10 16:23–18:20)
    elif c == 'du': print(json.dumps(balance()))
