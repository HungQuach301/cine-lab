"""Cine Lab · M2.1 — đo tương phản phụ đề cháy vào hình (WCAG) trên chính mp4: lấy khung ở giữa mỗi câu phụ đề (tối đa 40 câu, rải đều),
vùng phụ đề = hộp bao các điểm gần trắng ở dải dưới khung; chữ = trung vị 2 % điểm sáng nhất, nền = trung vị điểm < 160 trong hộp (thân hộp đen).
/opt/cine/bin/python design/m3/animatic/do_phu_de.py <video.mp4> <sub.srt>
"""
import io, re, subprocess, sys
import numpy as np
from PIL import Image
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__file__), '../thu-phong-cach')); from data_frame import ratio
v, srt = sys.argv[1:3]
tt = [sum(float(x) * m for x, m in zip(re.split('[:,]', a)[:3] + [re.split('[:,]', a)[3]], (3600, 60, 1, 0.001))) for a in re.findall(r'(\d\d:\d\d:\d\d,\d\d\d) -->', open(srt).read())]
en = [sum(float(x) * m for x, m in zip(re.split('[:,]', a), (3600, 60, 1, 0.001))) for a in re.findall(r'--> (\d\d:\d\d:\d\d,\d\d\d)', open(srt).read())]
idx = np.linspace(0, len(tt) - 1, min(40, len(tt))).astype(int); res = []
for i in idx:
    t = (tt[i] + en[i]) / 2
    r = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-ss', f'{t:.2f}', '-i', v, '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True, check=True)
    a = np.asarray(Image.open(io.BytesIO(r.stdout)).convert('RGB')).astype(int)[380:]; L = a.mean(2)
    ys, xs = np.where(L > 235)
    if len(ys) < 20: continue
    box = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1].reshape(-1, 3); Lb = box.mean(1)
    fg = tuple(int(x) for x in np.median(box[Lb >= np.percentile(Lb, 98)], axis=0)); bg = tuple(int(x) for x in np.median(box[Lb < 160], axis=0))
    res.append((round(ratio(fg, bg), 2), round(t, 1), fg, bg))
res.sort(); print(f'{len(res)} khung đo · tương phản nhỏ nhất {res[0]} · trung vị {res[len(res) // 2][0]}:1')
