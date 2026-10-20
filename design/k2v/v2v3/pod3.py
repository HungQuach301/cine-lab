"""NC-V2V3 · điều khiển pod RunPod: GỌI NGUYÊN design/pt/gpu/pod.py của NC-GPU (đọc từ nhánh claude/eloquent-dijkstra-kemr8j, không sửa)
và chỉ đổi: sổ giờ → reports/nc-v2v3/gio-gpu.jsonl, trạng thái → /var/tmp/cine-out/v2v3/pod.json, ảnh pod python:3.12-bookworm (có git/curl), chặn tiền.
Khoá RunPod do proxy gắn cho api.runpod.io / rest.runpod.io — mã KHÔNG đọc, in hay ghi khoá. UA CineLab-research; không email.
  pod3.py du                                  số dư + $/h đang tiêu
  pod3.py len <gpuTypeId> <SECURE|COMMUNITY> <nhãn> [đĩa GB]   CHẶN: số dư < $2,5 hoặc đã tiêu ≥ $12 kể từ đầu phiên → không bật
  pod3.py tat · put · get · run · log · ls    như pod.py
Biến: NCG_POD_PY = đường dẫn pod.py (mặc định /var/tmp/ncg-src/design/pt/gpu/pod.py)."""
import base64, importlib.util, json, os, secrets, sys, time

SRC = os.environ.get('NCG_POD_PY', '/var/tmp/ncg-src/design/pt/gpu/pod.py')
sp = importlib.util.spec_from_file_location('pod', SRC); pod = importlib.util.module_from_spec(sp); sp.loader.exec_module(pod)
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
pod.LEDGER = os.path.join(REPO, 'reports/nc-v2v3/gio-gpu.jsonl'); pod.STATE = '/var/tmp/cine-out/v2v3/pod.json'
SO_DU_DAU = 14.0158906504   # đọc 20/10/2026 10:0x UTC trước mọi pod của phiên
CHAN_TIEU, SAN_SO_DU = 12.0, 2.5


def len3(gpu, cloud, lab, disk=120):
    b = pod.balance()['clientBalance']
    if b < SAN_SO_DU or SO_DU_DAU - b >= CHAN_TIEU:
        pod.ledger({'su_kien': 'chan_tien', 'luc': pod.now(), 'so_du': b}); raise SystemExit(f'CHẶN TIỀN: số dư {b:.2f}')
    if os.path.exists(pod.STATE): raise SystemExit('đang có pod (một pod tại một thời điểm): ' + open(pod.STATE).read()[:200])
    tok = secrets.token_hex(24); srv = base64.b64encode(open(SRC.replace('pod.py', 'pod_srv.py'), 'rb').read()).decode()
    body = {'name': f'cinelab-v2v3-{lab}', 'imageName': 'python:3.12-bookworm', 'gpuTypeIds': [gpu], 'gpuCount': 1, 'cloudType': cloud,
            'containerDiskInGb': int(disk), 'volumeInGb': 0, 'ports': ['8888/http'], 'interruptible': False,
            'env': {'TOK': tok, 'SRV': srv, 'NVIDIA_DRIVER_CAPABILITIES': 'all'},
            'dockerStartCmd': ['python3', '-c', "import os,base64;exec(base64.b64decode(os.environ['SRV']))"]}
    t0 = pod.now(); s, r = pod.req('https://rest.runpod.io/v1/pods', json.dumps(body).encode(), 'POST', {'Content-Type': 'application/json'})
    if s >= 300:
        msg = r.decode('utf-8', 'replace')[:800]; pod.ledger({'su_kien': 'tao_loi', 'gpu': gpu, 'cloud': cloud, 'luc': t0, 'http': s, 'nguyen_van': msg}); print('LỖI', s, msg); sys.exit(2)
    P = json.loads(r); os.makedirs(os.path.dirname(pod.STATE), exist_ok=True)
    json.dump({'id': P['id'], 'tok': tok, 'gpu': gpu, 'cloud': cloud, 'lab': lab, 'bat': t0, 'gia_h': P.get('costPerHr'), 'du_truoc': b}, open(pod.STATE, 'w'))
    pod.ledger({'su_kien': 'bat', 'pod': P['id'], 'gpu': gpu, 'cloud': cloud, 'nhan': lab, 'luc': t0, 'gia_h': P.get('costPerHr'), 'so_du_truoc': b, 'anh': body['imageName']})
    print('POD', P['id'], 'gia/h', P.get('costPerHr')); u, h = pod.base(); t1 = time.time()
    while time.time() - t1 < 900:
        try:
            s, _ = pod.req(u + '/ping', timeout=20)
            if s == 200: print('SAN SANG sau', round(time.time() - t1), 's'); pod.ledger({'su_kien': 'san_sang', 'pod': P['id'], 'luc': pod.now(), 'cho_s': round(time.time() - t1)}); return
        except Exception: pass
        time.sleep(10)
    print('KHÔNG LÊN sau 15 phút — tắt'); pod.tat()


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'len': len3(a[1], a[2], a[3], *(a[4:5]))
    elif a[0] == 'du': print(json.dumps(pod.balance()))
    else:
        sys.argv = [SRC] + a; exec(compile(open(SRC).read().split("if __name__ == '__main__':")[1].replace('\n    ', '\n'), SRC, 'exec'), vars(pod))
