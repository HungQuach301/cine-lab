#!/opt/cine/bin/python
"""BAN-CUOI-T3 (việc 10) · TỜ KHUNG (1 khung/shot ở giữa mỗi góc máy, 320×180, nhãn mã + giây) và TỜ SO TRƯỚC/SAU các shot đổi
(TRƯỚC = tệp xem animatic v2 reports/animatic-t3-v2/xem/0x-*.mp4 640×360 — cùng mốc phim; SAU = master bản cuối 1080p thu 640×360). Mốc phim v2 ↔ bản cuối giống nhau tới 745 s.
  cuoi_to.py khung <master.mp4> <ra.jpg>
  cuoi_to.py so <master.mp4> <thư mục ra> H1,C4,N3_1,…"""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw
REPO = Path(__file__).resolve().parents[2]; EPD = REPO / 'channel-k2/k2c-t3-01/cuoi'; V2 = REPO / 'reports/animatic-t3-v2/xem'
CH = [('01-mo-dau', 0, 43.833), ('02-ch1-rock-1704', 43.833, 173.083), ('03-ch2a-vay-ham', 173.083, 262.208), ('04-ch2b-tan-cong-1782', 262.208, 382.583),
      ('05-ch3-dat-trung-lap', 382.583, 471.625), ('06-ch4-duong-bang', 471.625, 585.833), ('07-ch5a-cong', 585.833, 666.083), ('08-ch5b-ket', 666.083, 761.0)]
def khung(src, t, w=640, h=360):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', str(src), '-frames:v', '1', '-vf', f'scale={w}:{h}', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True)
    from io import BytesIO
    return Image.open(BytesIO(r.stdout)).convert('RGB') if r.stdout else Image.new('RGB', (w, h), (40, 0, 0))
def v2_tai(t):
    for n, a, b in CH:
        if a <= t < b: return V2 / f'{n}.mp4', t - a
    return None, None
B = {b['ma']: b for b in json.loads((EPD / 'bang-shot.json').read_text())}; L = {x.get('ma'): x for x in json.loads((EPD / 'log-shot.json').read_text())}
a = sys.argv
if a[1] == 'khung':
    M = a[2]; tiles = []
    for ma, b in B.items():
        cs = [0.0] + [float(c) for c in (b.get('cat') or [])] + [b['dur']]
        for x, y in zip(cs, cs[1:]): tiles.append((f"{ma} {b['t0'] + (x + y) / 2:.1f}s", b['t0'] + (x + y) / 2))
    W, H, C = 320, 180, 8; R = (len(tiles) + C - 1) // C; sh = Image.new('RGB', (W * C, (H + 16) * R), (16, 16, 16)); g = ImageDraw.Draw(sh)
    for i, (s, t) in enumerate(tiles):
        X, Y = (i % C) * W, (i // C) * (H + 16); sh.paste(khung(M, t, W, H), (X, Y + 16)); g.text((X + 3, Y + 2), s, fill=(255, 230, 120))
    sh.save(a[3], quality=80); print('to-khung', len(tiles), 'ô')
elif a[1] == 'so':
    M = a[2]; out = Path(a[3]); out.mkdir(parents=True, exist_ok=True)
    for ma in a[4].split(','):
        ma = ma.replace('_', '.') if ma not in B else ma; b = B[ma]; cs = [0.0] + [float(c) for c in (b.get('cat') or [])] + [b['dur']]
        ts = sorted({round(b['t0'] + (x + y) / 2, 2) for x, y in zip(cs, cs[1:])} | {round(b['t0'] + 0.3, 2), round(b['t1'] - 0.3, 2)})[:4]
        sh = Image.new('RGB', (640 * len(ts), 2 * 360 + 40), (16, 16, 16)); g = ImageDraw.Draw(sh)
        for j, t in enumerate(ts):
            f, tt = v2_tai(t)
            if f and f.exists(): sh.paste(khung(f, tt), (j * 640, 20))
            sh.paste(khung(M, t), (j * 640, 380)); g.text((j * 640 + 4, 4), f'TRƯỚC (v2) {ma} {t:.2f}s', fill=(255, 160, 120)); g.text((j * 640 + 4, 364), f'SAU (bản cuối) {ma} {t:.2f}s', fill=(140, 255, 160))
        sh.save(out / f"to-so-{ma.replace('.', '_')}.jpg", quality=78); print('to-so', ma, ts)
