#!/opt/cine/bin/python
"""ANIMATIC-T3-V2 · TỜ SO TRƯỚC | SAU từng shot sửa (khung đầu / giữa / cuối) + tờ M1–M5 (ảnh đầu render | khung Omni).
TRƯỚC = tệp xem ANIMATIC-T3 trong git (reports/animatic-t3/xem/*.mp4, 640×360 — master v1 960×540 đã mất theo container), mốc shot theo bang-shot.json @41e0c8fd.
SAU = master v2 (960×540) theo bang-shot.json hiện tại.
  v2_to_so.py shot <master v2.mp4> <thư mục ra> A,B,…        → to-so-<mã>.jpg
  v2_to_so.py mh <thư mục ra>                                  → to-so-minh-hoa.jpg (dau/<M>.jpg | omni/chon/<M>.mp4 25 % · 55 % · 90 %)"""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw
REPO = Path(__file__).resolve().parents[2]
XEM = [('01-mo-dau', 0.0), ('02-ch1-rock-1704', 43.833), ('03-ch2a-vay-ham', 173.083), ('04-ch2b-tan-cong-1782', 262.167), ('05-ch3-dat-trung-lap', 382.583),
       ('06-ch4-duong-bang', 471.625), ('07-ch5a-cong', 585.833), ('08-ch5b-ket', 666.083)]
W, H = 480, 270


def khung(src, t, out):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{max(0, t):.3f}', '-i', str(src), '-frames:v', '1', '-vf', f'scale={W}:{H}', str(out)], check=True); return Image.open(out).convert('RGB')


def v1_src(t):
    f, t0 = [x for x in XEM if x[1] <= t + 1e-6][-1]; return REPO / f'reports/animatic-t3/xem/{f}.mp4', t - t0


def shot(master, out, ids):
    B1 = {b['ma']: b for b in json.loads(subprocess.run(['git', '-C', str(REPO), 'show', '41e0c8fd:channel-k2/k2c-t3-01/animatic/bang-shot.json'], capture_output=True, text=True).stdout)}
    B2 = {b['ma']: b for b in json.loads((REPO / 'channel-k2/k2c-t3-01/animatic/bang-shot.json').read_text())}
    out.mkdir(parents=True, exist_ok=True); tmp = out / '_t.png'
    for sid in ids:
        a, b = B1[sid], B2[sid]; sh = Image.new('RGB', (W * 3, (H + 22) * 2), (18, 18, 18)); g = ImageDraw.Draw(sh)
        for r, (lab, bb, src_of) in enumerate([('TRƯỚC (ANIMATIC-T3, 640×360)', a, lambda t: v1_src(t)), ('SAU (v2)', b, lambda t: (master, t))]):
            ts = [bb['t0'] + 0.3, (bb['t0'] + bb['t1']) / 2, bb['t1'] - 0.3]
            for j, t in enumerate(ts):
                s, tt = src_of(t); sh.paste(khung(s, tt, tmp), (j * W, r * (H + 22) + 22)); g.text((j * W + 4, r * (H + 22) + 4), f'{sid} {lab} · phim {t:.1f} s', fill=(255, 230, 120))
        sh.save(out / f"to-so-{sid.replace('.', '_')}.jpg", quality=82); print('xong', sid)
    tmp.unlink(missing_ok=True)


def mh(out):
    out.mkdir(parents=True, exist_ok=True); D = REPO / 'reports/animatic-t3-v2/omni'; Ms = ['M1', 'M2', 'M3', 'M4', 'M5']
    sh = Image.new('RGB', (W * 4, (H + 22) * len(Ms)), (18, 18, 18)); g = ImageDraw.Draw(sh); tmp = out / '_t.png'
    for i, m in enumerate(Ms):
        y = i * (H + 22) + 22; p = D / 'dau' / f'{m}.jpg'
        if p.exists(): sh.paste(Image.open(p).convert('RGB').resize((W, H)), (0, y))
        g.text((4, y - 18), f'{m} ảnh đầu (render của ta)', fill=(255, 230, 120)); c = D / 'chon' / f'{m}.mp4'
        if c.exists():
            d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(c)], capture_output=True, text=True).stdout)
            for j, u in enumerate((0.25, 0.55, 0.9)): sh.paste(khung(c, u * d, tmp), ((j + 1) * W, y)); g.text(((j + 1) * W + 4, y - 18), f'{m} Omni {int(u * 100)} %', fill=(255, 230, 120))
        else: g.text((W + 10, y + 100), f'{m}: không có clip đạt — giữ bản 3D', fill=(255, 120, 120))
    sh.save(out / 'to-so-minh-hoa.jpg', quality=82); tmp.unlink(missing_ok=True); print('xong minh hoạ')


if __name__ == '__main__':
    if sys.argv[1] == 'shot': shot(Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4].split(','))
    else: mh(Path(sys.argv[2]))
