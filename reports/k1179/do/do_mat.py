#!/opt/cine/bin/python
"""K-1.17.9 · KN-4/KN-7: đo YuNet bằng CHÍNH hàm của checks (q_k1177.do_mat/mat_khung, mỗi 2 khung, độ phân giải gốc) trên clip thật → JSON.
Ghi thêm mọi hộp điểm ≥ 0,60 (mức (w)) và phần hộp nằm trên/ngoài cửa sổ cat_clip. Không API.   do_mat.py <clip.mp4> [<ra.json>]"""
import json, sys, cv2, hashlib
sys.path.insert(0, '/home/user/cine-lab')
from checks.ll import q_k1177 as K
p = sys.argv[1]; cap = cv2.VideoCapture(p); i = 0; F = []
while True:
    ok, f = cap.read()
    if not ok: break
    if i % 2 == 0: F.append(dict(f=i, hop=[dict(ty=round(ty, 4), diem=round(sc, 3), hop=b) for ty, sc, b in K.mat_khung(f)]))
    i += 1
R = dict(clip=p, sha256=hashlib.sha256(open(p, 'rb').read()).hexdigest(), khung=i, do=F,
         max_075=max([h['ty'] for x in F for h in x['hop'] if h['diem'] >= 0.75] or [0]),
         max_060=max([h['ty'] for x in F for h in x['hop'] if h['diem'] >= 0.60] or [0]),
         tren_1_8=[(x['f'], h['ty'], h['diem'], h['hop']) for x in F for h in x['hop'] if h['ty'] > 0.125])
if len(sys.argv) > 2: json.dump(R, open(sys.argv[2], 'w'), indent=0)
print(p.split('/')[-1], 'khung', i, 'max≥0.75', R['max_075'], 'max≥0.60', R['max_060'], '>1/8:', R['tren_1_8'][:12], len(R['tren_1_8']))
