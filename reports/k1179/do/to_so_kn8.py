#!/opt/cine/bin/python
"""K-1.17.9 · KN-8 — tờ so trước/sau (JPG ≤ 2 MB): hàng 1 = ghép cũ (1.17.8: nước render) | ghép đề xuất KN-8 (dải bờ ±8 px cả hai phía) | ghép K (bờ phía đất,
nước toàn phần AI); hàng 2 = ô phóng ×2 cùng một chỗ (bờ + cầu/tàu). to_so_kn8.py <khung> <lượt> <mn> <x> <y> <ra.jpg>"""
import sys, cv2, numpy as np
k, luot, mn, x, y, ra = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
d = f'/var/tmp/k1179/kn8/{k}-{luot}-{mn}'
I = [cv2.imread(f'{d}/ghep-cu.png'), cv2.imread(f'{d}/ghep.png'), cv2.imread(f'{d}-bo_dat/ghep.png')]
NH = ['1.17.8: nuoc = render', 'KN-8 de xuat: bo +-8 px ca hai phia', 'K-1.17.9: bo phia dat, nuoc AI']
W = 960; top = [cv2.resize(a, (W, 540), interpolation=cv2.INTER_AREA) for a in I]
bot = [cv2.resize(a[y:y + 270, x:x + 480], (W, 540), interpolation=cv2.INTER_CUBIC) for a in I]
for i, a in enumerate(top):
    cv2.rectangle(a, (x // 2, y // 2), ((x + 480) // 2, (y + 270) // 2), (0, 255, 255), 2); cv2.putText(a, NH[i], (12, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
for a in bot: cv2.putText(a, f'x2 @({x},{y})', (12, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
S = np.vstack([np.hstack(top), np.hstack(bot)]); q = 88
while True:
    cv2.imwrite(ra, S, [cv2.IMWRITE_JPEG_QUALITY, q])
    import os
    if os.path.getsize(ra) <= 2_000_000 or q <= 60: break
    q -= 6
print(ra, os.path.getsize(ra), 'q', q)
