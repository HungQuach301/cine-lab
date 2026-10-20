#!/opt/cine/bin/python -I
"""NC-V2V3 · kéo một thư mục kết quả từ pod về (mỗi tệp kiểm SHA-256 bằng pod.get), rồi KIỂM ĐỦ số khung trước khi cho phép tắt pod (bài học NG-D6 a).
  keo3.py <thư mục trên pod, vd ra/c2-A> <thư mục cục bộ> <số khung cần>  → mã 0 nếu đủ"""
import importlib.util, json, os, sys
sp = importlib.util.spec_from_file_location('p3', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pod3.py')); p3 = importlib.util.module_from_spec(sp); sys.argv_bak = sys.argv; sp.loader.exec_module(p3)
pod = p3.pod; rd, ld, need = sys.argv[1], sys.argv[2], int(sys.argv[3])
u, h = pod.base(); s, r = pod.req(f'{u}/ls/{rd}', headers=h); fs = json.loads(r) if s == 200 else []
os.makedirs(ld, exist_ok=True); n = 0
for name, size in sorted(fs):
    lp = os.path.join(ld, name)
    if os.path.exists(lp) and os.path.getsize(lp) == size: n += 1; continue
    pod.get(rd.rstrip('/') + '/' + name, lp); n += 1
have = len([x for x in os.listdir(ld) if x.endswith('.png')]); print(json.dumps({'dir': rd, 'tren_pod': len(fs), 'cuc_bo_png': have, 'can': need, 'du': have >= need}))
sys.exit(0 if have >= need else 3)
