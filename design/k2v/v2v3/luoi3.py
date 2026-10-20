#!/opt/cine/bin/python -I
"""NC-V2V3 · clip xem ≤ 5 MB: lưới 3 × 2 ô 480×270, 81 khung 24 fps: nguồn V7B | A | B / B2 | ô 5 | Omni-a (NC-V2V, CÙNG khung — CÓ vật bịa, chỉ để so 'độ thật').
Ô 5 = B2 khử nhiễu 0,5 (c2) hoặc mặt nạ vùng AI được vẽ (trắng) chồng lên nguồn. Nhãn ASCII (Hershey). Omni-a lấy ô trên–phải của reports/nc-v2v/clip/so-*.mp4 (nguồn|a / b|c).
  luoi3.py <clip c2|c4B|c1> <ra.mp4>"""
import subprocess, sys, os
import cv2, numpy as np
B = '/var/tmp/cine-out/v2v3'; R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..'))
c, out = sys.argv[1], sys.argv[2]; cw, ch = 480, 270
OM = {'c2': ('so-c2.mp4', 80), 'c4B': ('so-c4-noi.mp4', 320), 'c1': ('so-c1.mp4', 80)}


def vid(p):
    cap = cv2.VideoCapture(p); fs = []
    while True:
        ok, f = cap.read()
        if not ok: break
        fs.append(f)
    return fs


om_f, om0 = OM[c]; OMV = vid(os.path.join(R, 'reports/nc-v2v/clip', om_f))
cells = [('nguon V7B', lambda i: cv2.imread(f'{B}/ctrl/{c}/src/{i:05d}.png')), ('A: do sau + canh', lambda i: cv2.imread(f'{B}/vid/{c}-A/khung/{i:05d}.png')),
         ('B: + mat na', lambda i: cv2.imread(f'{B}/vid/{c}-B/khung/{i:05d}.png')), ('B2: + khoi tu nguon 0.6', lambda i: cv2.imread(f'{B}/vid/{c}-B2/khung/{i:05d}.png'))]
if c == 'c2': cells.append(('B2 khu nhieu 0.5', lambda i: cv2.imread(f'{B}/vid/c2-B2d50/khung/{i:05d}.png')))
else:
    def mk(i):
        s = cv2.imread(f'{B}/ctrl/{c}/src/{i:05d}.png') // 2; m = cv2.imread(f'{B}/ctrl/{c}/mask/{i:05d}.png', cv2.IMREAD_GRAYSCALE) > 127; s[m] = (s[m] * 0.4 + 150).astype(np.uint8); return s
    cells.append(('vung AI duoc ve (sang)', mk))
cells.append(('Omni-a (NC-V2V, CO vat bia)', lambda i: OMV[om0 + i][0:270, 480:960] if om0 + i < len(OMV) else np.zeros((270, 480, 3), np.uint8)))
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{3 * cw}x{2 * ch}', '-r', '24', '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '21', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
for i in range(81):
    ims = []
    for name, f in cells:
        im = cv2.resize(f(i), (cw, ch), interpolation=cv2.INTER_AREA); cv2.rectangle(im, (0, 0), (cw, 22), (20, 20, 20), -1)
        cv2.putText(im, name, (6, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (240, 240, 240), 1, cv2.LINE_AA); ims.append(im)
    p.stdin.write(np.vstack([np.hstack(ims[:3]), np.hstack(ims[3:])]).tobytes())
p.stdin.close(); p.wait(); print(out, os.path.getsize(out))
