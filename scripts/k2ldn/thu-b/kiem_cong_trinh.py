#!/opt/cine/bin/python
"""THU-B-T4 · (D) kiểm hình học: mọi tam giác lớp KHÔNG phải nhà thường (công trình có tên 5, tường/kè 6, cầu 7, nhà thờ 8/9, bến 11, phế tích 2) ở look3d
TRÙNG TỪNG BIT với look2 (cùng thứ tự) → không phóng/đổi kích thước/dời công trình có tên (luật cứng). → reports/thu-b-t4/do/kiem-cong-trinh-d.json"""
import json, os, hashlib
import numpy as np
D = os.environ.get('LDN_DATA', '/var/tmp/ldn'); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
def ld(lk):
    J = json.load(open(f'{D}/{lk}/ldn2.json')); B = open(f'{D}/{lk}/ldn2.bin', 'rb').read()
    a = lambda nm, dt: np.frombuffer(B, dtype=dt, count=J['bo_cuc'][nm]['len'] // np.dtype(dt).itemsize, offset=J['bo_cuc'][nm]['off'])
    return a('pos', np.float32).reshape(-1, 9), a('k', np.uint8)[::3], a('tl', np.float32).reshape(-1, 12)[:, :4], a('mt', np.uint8)[::3], J
out = {}
P2, K2, T2, M2, J2 = ld('look2'); PD, KD, TD, MD, JD = ld('look3d')
for k in (2, 5, 6, 7, 8, 9, 11):
    a, b = P2[K2 == k], PD[KD == k]
    out[str(k)] = dict(tam_giac_v2=int(len(a)), tam_giac_d=int(len(b)), trung_tung_bit=bool(len(a) == len(b) and np.array_equal(a, b)),
                       sha_v2=hashlib.sha256(a.tobytes()).hexdigest()[:16], sha_d=hashlib.sha256(b.tobytes()).hexdigest()[:16])
out['tong'] = dict(tam_giac_v2=JD.get('thu_b', {}) and int(J2['tam_giac']), tam_giac_d=int(JD['tam_giac']), nha_thuong_k=[1, 3, 4, 10])
os.makedirs(os.path.join(REPO, 'reports/thu-b-t4/do'), exist_ok=True); json.dump(out, open(os.path.join(REPO, 'reports/thu-b-t4/do/kiem-cong-trinh-d.json'), 'w'), indent=1); print(json.dumps(out))
