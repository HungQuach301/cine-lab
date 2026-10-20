#!/opt/cine/bin/python
"""V7-PILOT · (a) TỜ SO TRƯỚC/SAU: 8 cặp khung G1b (bản xem 270p trong git, có ray lời) ↔ bản thử (bản 540p có ray, ngoài git) tại CÙNG câu lời → reports/v7p/so/to-so-8-cap.jpg
(b) CHUỖI XEM CÂM (HC-2): 1 khung/2 s từ master KHÔNG phụ đề, không tiếng → reports/v7p/xem-cam/tho-*.jpg (lưới 6 × 5, nhãn giây) cho người chấm.
Dùng: /opt/cine/bin/python -I scripts/k2tl/v7p_so.py [so] [cam]"""
import subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]; O = Path('/var/tmp/cine-out/k2c-t3-v7p'); W = ROOT / 'reports/v7p'
G1B = ROOT / 'reports/g1b-t3/animatic/animatic-270p-xem.mp4'; RAY = O / 'k2c-t3-v7p-540p-ray.mp4'; MASTER = O / 'k2c-t3-v7p-v1-master.mp4'
# (câu lời, giây G1b, giây bản thử) — chương 2 lệch 122,1 s (2a: G1b 166,6 → bản thử 44,5)
PAIRS = [('0a', 'Midnight at the Gibraltar frontier…', 3.0, 3.0), ('0d', 'Historians on both sides count fourteen sieges…', 18.5, 18.5),
         ('0f', 'In 1782, ten floating batteries came to break it.', 30.5, 30.5), ('0g', 'In 1941, a runway was laid across the only road…', 36.5, 36.5),
         ('2a', 'Half a century later… can you starve a rock?', 172.0, 49.9), ('2d', 'By January 1780, thistles, dandelions…', 204.0, 81.9),
         ('SM2', 'Britain sent three relief fleets: 1780, 1781, 1782.', 218.0, 95.9), ('2g', 'On the twelfth of April 1781… opened fire on the town.', 236.0, 113.9)]
try: F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 15)
except Exception: F = ImageFont.load_default()
def grab(src, t, out):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', str(src), '-frames:v', '1', str(out)], check=True); return Image.open(out).convert('RGB')
def so():
    tmp = Path('/var/tmp/cine-out/v7p/so'); tmp.mkdir(parents=True, exist_ok=True); w, h = 640, 360
    S = Image.new('RGB', (2 * w + 30, len(PAIRS) * (h + 30) + 40), 'white'); D = ImageDraw.Draw(S)
    D.text((10, 10), 'TRÁI: G1b animatic (bản xem 270p, 19/10) · PHẢI: V7-PILOT bản thử (540p) — cùng câu lời; cả hai có ray phụ đề tạm', fill='black', font=F)
    for i, (k, cau, tg, tp) in enumerate(PAIRS):
        a = grab(G1B, tg, tmp / f'g1b-{k}.png').resize((w, h), Image.LANCZOS); b = grab(RAY, tp, tmp / f'v7p-{k}.png').resize((w, h), Image.LANCZOS)
        y = 40 + i * (h + 30); D.text((10, y), f'{k} · "{cau}" · G1b {tg:.1f} s ↔ bản thử {tp:.1f} s', fill='black', font=F)
        S.paste(a, (10, y + 22)); S.paste(b, (20 + w, y + 22))
    (W / 'so').mkdir(parents=True, exist_ok=True); S.save(W / 'so/to-so-8-cap.jpg', quality=85); print(W / 'so/to-so-8-cap.jpg')
def cam():
    tmp = Path('/var/tmp/cine-out/v7p/cam'); tmp.mkdir(parents=True, exist_ok=True)
    for f in tmp.glob('*.png'): f.unlink()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '1.0', '-i', str(MASTER), '-vf', 'fps=0.5,scale=320:180', str(tmp / 'k%03d.png')], check=True)
    fs = sorted(tmp.glob('k*.png')); (W / 'xem-cam').mkdir(parents=True, exist_ok=True); per = 30; outs = []
    for j in range(0, len(fs), per):
        grp = fs[j:j + per]; cols = 6; rows = (len(grp) + cols - 1) // cols; S = Image.new('RGB', (cols * 330, rows * 205), 'white'); D = ImageDraw.Draw(S)
        for i, f in enumerate(grp):
            n = j + i; x, y = (i % cols) * 330, (i // cols) * 205; D.text((x + 4, y + 2), f'#{n + 1:02d} · {1 + 2 * n:d} s', fill='black', font=F); S.paste(Image.open(f), (x + 4, y + 22))
        p = W / f'xem-cam/to-{j // per + 1}.jpg'; S.save(p, quality=86); outs.append(p)
    print(len(fs), 'khung', *outs)
if __name__ == '__main__':
    a = sys.argv[1:] or ['so', 'cam']
    if 'so' in a: so()
    if 'cam' in a: cam()
