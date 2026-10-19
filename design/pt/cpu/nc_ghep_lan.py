"""NC-CPU · GHÉP CÚ LẶN 20 s (480 khung 24 fps): A (three.js + nướng) cho đoạn cao, B (Cycles CPU, chỉnh màu k2v) cho đoạn lướt thấp đêm,
hoà chéo theo trọng số smoothstep ở hai mối nối. Ra PNG chuỗi → ffmpeg (ngoài tệp này).
  /opt/cine/bin/python nc_ghep_lan.py <thư mục A0 (khung 0–228)> <thư mục A336> <thư mục B png> <ra> --x1 216,228 --x2 336,348"""
import sys, os, cv2, numpy as np
A0, A1, B, OUT = sys.argv[1:5]; a = sys.argv[5:]
x1 = [int(v) for v in a[a.index('--x1') + 1].split(',')]; x2 = [int(v) for v in a[a.index('--x2') + 1].split(',')]
os.makedirs(OUT, exist_ok=True); src = {}
def A(f): p = os.path.join(A0 if f <= 228 else A1, f'{f:05d}.jpg'); return cv2.imread(p)
def Bf(f): return cv2.imread(os.path.join(B, f'{f:05d}.png'))
ss = lambda u: u * u * (3 - 2 * u)
for f in range(480):
    if f < x1[0] or f > x2[1]: im = A(f); src[f] = 'A'
    elif f <= x1[1]: w = ss((f - x1[0]) / (x1[1] - x1[0])); im = cv2.addWeighted(A(f).astype(np.float32), 1 - w, Bf(f).astype(np.float32), w, 0).astype(np.uint8); src[f] = f'A→B {w:.2f}'
    elif f < x2[0]: im = Bf(f); src[f] = 'B'
    else: w = ss((f - x2[0]) / (x2[1] - x2[0])); im = cv2.addWeighted(Bf(f).astype(np.float32), 1 - w, A(f).astype(np.float32), w, 0).astype(np.uint8); src[f] = f'B→A {w:.2f}'
    cv2.imwrite(os.path.join(OUT, f'{f:05d}.png'), im)
import json; json.dump(src, open(os.path.join(OUT, 'nguon.json'), 'w')); print({k: sum(1 for v in src.values() if v.startswith(k)) for k in ('A', 'B')})
