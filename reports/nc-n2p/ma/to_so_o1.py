#!/opt/cine/bin/python -I
"""NC-N2P · TỜ SO O1 (PNG): mỗi khung cổng một tờ 3 × 3 ô 480×270 —
hàng 1–2: render (cách A) | AI lượt cuối (vừa / mạnh; lượt 3 nếu lượt 2 trượt) | AI + ghép lớp (a) (khớp màu, mã ghép cuối); hàng 3: lượt 1 (gửi mặt nạ) AI vừa | ghép vừa | ghép mạnh.
  to_so_o1.py <thư mục kiểm cuối> <thư mục ra>"""
import sys
from pathlib import Path
import cv2, numpy as np
K, OUT = Path(sys.argv[1]), Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
AI = Path('/var/tmp/n2p/o1/ai'); REPO = Path(__file__).resolve().parents[3]
W, H = 480, 270


def cell(p, txt):
    im = cv2.resize(cv2.imread(str(p)), (W, H), interpolation=cv2.INTER_AREA)
    cv2.rectangle(im, (0, 0), (W, 22), (0, 0, 0), -1); cv2.putText(im, txt, (6, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    return im


for k in ('cang', 'vay-ham', 'toan-canh'):
    R = REPO / f'reports/nc-cpu/khung/A/cong-{k}.jpg'; rows = []
    for lv in ('vua', 'manh'):
        l = 'l3' if (AI / f'{k}-{lv}-l3-ai.jpg').exists() else 'l2'
        rows.append(np.hstack([cell(R, f'{k} render (A)'), cell(AI / f'{k}-{lv}-{l}-ai.jpg', f'AI {l} - {lv}'), cell(K / f'{k}-{lv}-{l}-ghep.png', f'AI + ghep lop (a) - {lv} {l}')]))
    rows.append(np.hstack([cell(AI / f'{k}-vua-ai.jpg', 'luot 1 (gui mat na) AI vua'), cell(K / f'{k}-vua-l1-ghep.png', 'luot 1 ghep vua'), cell(K / f'{k}-manh-l1-ghep.png', 'luot 1 ghep manh')]))
    cv2.imwrite(str(OUT / f'to-so-o1-{k}.png'), np.vstack(rows), [cv2.IMWRITE_PNG_COMPRESSION, 9]); print(k)
