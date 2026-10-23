#!/opt/cine/bin/python
"""LOOK-T4 · tờ so TRƯỚC (tiền kỳ, reports/tien-ky-t4/xem/) / SAU (look, biến thể A) — cùng điểm máy xương sống P1 khi có.
  look_so.py <trước.jpg> <sau.jpg> <ra.jpg> "<nhãn trước>" "<nhãn sau>"   (ra ≤ 2 MB, 1920 rộng)"""
import sys, os, cv2, numpy as np
a, b, out, la, lb = sys.argv[1:6]
A = cv2.resize(cv2.imread(a), (960, 540), interpolation=cv2.INTER_AREA); B = cv2.resize(cv2.imread(b), (960, 540), interpolation=cv2.INTER_AREA)
S = np.full((540 + 44, 1920, 3), 236, np.uint8); S[44:, :960] = A; S[44:, 960:] = B
for x, t in ((10, la), (970, lb)): cv2.putText(S, t, (x, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (30, 30, 30), 2, cv2.LINE_AA)
q = 92
while True:
    cv2.imwrite(out, S, [cv2.IMWRITE_JPEG_QUALITY, q])
    if os.path.getsize(out) <= 2_000_000 or q < 60: break
    q -= 4
