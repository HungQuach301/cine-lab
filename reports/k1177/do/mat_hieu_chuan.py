#!/opt/cine/bin/python
"""K-1.17.7 việc 5: hiệu chuẩn bộ dò mặt YuNet (checks/models/face_detection_yunet_2023mar.onnx) trên 23 clip M-d animatic T4 (omni/chon).
Ra: /var/tmp/k1177/mat/do.json (mỗi clip: khung mẫu k25/k55/k90 + mọi khung bước 2: hộp mặt, điểm) + tờ soi có vẽ hộp (để lập đáp án bằng mắt)."""
import cv2, glob, json, os, sys, numpy as np
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')); A = os.path.join(R, 'channel-k2/k2c-t4-02/animatic/omni')
M = sys.argv[1] if len(sys.argv) > 1 else '/var/tmp/k1177/dl/yunet.onnx'; OUT = '/var/tmp/k1177/mat'; os.makedirs(OUT, exist_ok=True)
def doc(mp4):
    cap = cv2.VideoCapture(mp4); F = []
    while True:
        ok, f = cap.read()
        if not ok: break
        F.append(f)
    return F
def do(det, f, thr):
    h, w = f.shape[:2]; det.setInputSize((w, h)); det.setScoreThreshold(thr); _, fa = det.detect(f)
    return [] if fa is None else [dict(x=float(z[0]), y=float(z[1]), w=float(z[2]), h=float(z[3]), s=round(float(z[14]), 3)) for z in fa]
det = cv2.FaceDetectorYN.create(M, '', (320, 320), 0.5, 0.3, 5000)
KQ = {}; sheets = []
for c in sorted(glob.glob(os.path.join(A, 'chon', '*.txt'))):
    tag = open(c).read().split()[0]; mp4 = os.path.join(A, 'clip', tag + '.mp4')
    F = doc(mp4); n = len(F); H = F[0].shape[0]
    per = [do(det, F[i], 0.5) for i in range(0, n, 2)]
    mx = [max([b['h'] for b in p if b['s'] >= 0.6] or [0]) / H for p in per]
    mau = {}
    for u in (0.25, 0.55, 0.90):
        i = min(n - 1, int(round(u * (n - 1)))); b = do(det, F[i], 0.5); im = F[i].copy()
        for z in b:
            col = (0, 255, 0) if z['s'] >= 0.6 else (0, 160, 255)
            cv2.rectangle(im, (int(z['x']), int(z['y'])), (int(z['x'] + z['w']), int(z['y'] + z['h'])), col, 1)
            cv2.putText(im, f"{z['s']:.2f}/{z['h'] / H:.3f}", (int(z['x']), max(10, int(z['y']) - 2)), 0, 0.35, col, 1)
        cv2.line(im, (0, int(H / 8)), (12, int(H / 8)), (0, 0, 255), 2)   # vạch 1/8 chiều cao khung
        cv2.putText(im, f'{tag} k{int(u * 100)}', (4, H - 6), 0, 0.45, (0, 255, 255), 1)
        mau[f'k{int(u * 100)}'] = dict(i=i, hop=b); sheets.append(im)
    KQ[tag] = dict(n=n, H=H, mau=mau, mat_lon_nhat_ty=round(max(mx), 4), khung_tren_1_8=sum(v > 1 / 8 for v in mx), khung_do=len(per))
    print(tag, n, 'mặt lớn nhất/H', round(max(mx), 3), 'khung >1/8', KQ[tag]['khung_tren_1_8'], '/', len(per), flush=True)
json.dump(KQ, open(os.path.join(OUT, 'do.json'), 'w'), indent=1)
for k in range(0, len(sheets), 12):
    S = sheets[k:k + 12]
    while len(S) < 12: S.append(np.zeros_like(sheets[0]))
    cv2.imwrite(os.path.join(OUT, f'to-{k // 12:02d}.jpg'), np.vstack([np.hstack(S[j:j + 3]) for j in range(0, 12, 3)]), [cv2.IMWRITE_JPEG_QUALITY, 88])
