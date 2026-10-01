"""Cine Lab · M3 B3 v2 — đo tương phản chữ TRONG VÙNG SÁNG của đoạn 20 s (720p): khung lấy từ mp4, ô bao quanh nhóm chữ/số;
màu chữ = trung vị 3 % điểm tối nhất, nền = trung vị 40 % điểm sáng nhất trong ô (tỉ lệ WCAG).
/opt/cine/bin/python design/m3/thu-phong-cach/tuong_phan_clip.py <clip.mp4>
"""
import io, subprocess, sys
import numpy as np
from PIL import Image
sys.path.insert(0, __import__('os').path.dirname(__file__)); from data_frame import ratio
v = sys.argv[1]
BOX = [(10.0, "số \"46\" + \"gas lamps\" (tấm bản đồ)", (465, 300, 575, 375)), (10.0, "chữ \"OLD TOWN, 1905\"", (200, 268, 400, 300)),
       (15.0, 'số trên cột "14", "9" + năm (tấm biểu đồ)', (660, 300, 980, 470)), (15.0, 'số "14→1"', (880, 265, 990, 305)), (15.0, 'chữ "LAMPLIGHTERS"', (690, 268, 880, 300))]
for t, name, b in BOX:
    r = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-ss', f'{t}', '-i', v, '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True, check=True)
    a = np.asarray(Image.open(io.BytesIO(r.stdout)).convert('RGB').crop(b)).reshape(-1, 3).astype(int); s = a.sum(1); o = np.argsort(s)
    fg = tuple(int(x) for x in np.median(a[o[: max(1, len(o) * 3 // 100)]], axis=0)); bg = tuple(int(x) for x in np.median(a[o[-len(o) * 40 // 100:]], axis=0))
    print(f'{t:4.1f} s · {name}: chữ {fg} / nền {bg} → {ratio(fg, bg):.1f}:1')
