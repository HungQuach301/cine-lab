#!/opt/cine/bin/python
"""BAN-CUOI-T4-A · tờ so tấm E cho chủ dự án: một hàng render | AI | ghép (mỗi ô 1280×720) + hàng 3 ô cắt phóng ×2 (mái vòm/toà có tên; ranh 3D↔AI; phố/nhà thường)
— JPG ≤ 2 MB vào reports/ban-cuoi-t4-a/e/so-<khung>-<tag>.jpg.   to_so_e.py <khung> <tag> [nhãn]"""
import json, os, sys
import cv2, numpy as np
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
T = os.path.join(REPO, 'channel-k2/k2c-t4-02/ban-cuoi/e/tam'); O = os.path.join(REPO, 'reports/ban-cuoi-t4-a/e'); os.makedirs(O, exist_ok=True)
k, tag = sys.argv[1], sys.argv[2]; nhan = sys.argv[3] if len(sys.argv) > 3 else ''
R = cv2.imread(f'{T}/{k}/render.png'); A = cv2.imread(f'{T}/{k}/{tag}/ai-1080.png'); G = cv2.imread(f'{T}/{k}/{tag}/ghep.png')
toa = json.load(open(f'{T}/{k}/toa.json')); sp = next(t for t in toa if t['ten'].startswith("St Paul"))
x0, y0, x1, y1 = sp['hop']; cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
def cat(im, cx, cy, w=480, h=270):
    x = int(np.clip(cx - w // 2, 0, im.shape[1] - w)); y = int(np.clip(cy - h // 2, 0, im.shape[0] - h)); return cv2.resize(im[y:y + h, x:x + w], (w * 2, h * 2), interpolation=cv2.INTER_NEAREST), (x, y)
c1, p1 = cat(G, cx, cy); c2, p2 = cat(G, int(G.shape[1] * 0.7), int(G.shape[0] * 0.55)); c3, p3 = cat(G, int(G.shape[1] * 0.3), int(G.shape[0] * 0.85))
s = lambda x: cv2.resize(x, (1280, 720), interpolation=cv2.INTER_AREA)
top = np.hstack([s(R), s(A), s(G)]); bot = np.hstack([cv2.resize(c, (1280, 720)) for c in (c1, c2, c3)])
for i, t in enumerate(('RENDER 3D (look3 d)', 'AI toan khung (gpt-image-2.5)', 'GHEP (lop (a)-E = render)')):
    cv2.putText(top, t, (20 + 1280 * i, 46), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 5, cv2.LINE_AA); cv2.putText(top, t, (20 + 1280 * i, 46), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
for i, (t, p) in enumerate((('mai vom', p1), ('ranh 3D/AI', p2), ('pho', p3))):
    lb = f'{t} x2 @({p[0]},{p[1]})'; cv2.putText(bot, lb, (20 + 1280 * i, 46), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 5, cv2.LINE_AA); cv2.putText(bot, lb, (20 + 1280 * i, 46), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
out = np.vstack([top, bot]); q = 88
cv2.putText(out, f'{k} {tag} {nhan}', (20, out.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3, cv2.LINE_AA)
while True:
    p = f'{O}/so-{k}-{tag}.jpg'; cv2.imwrite(p, out, [cv2.IMWRITE_JPEG_QUALITY, q])
    if os.path.getsize(p) <= 2_000_000 or q < 40: break
    q -= 6
print(p, os.path.getsize(p), q)
