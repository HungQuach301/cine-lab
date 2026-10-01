"""Cine Lab · M3 THỬ PHONG CÁCH — dải kiểm mù thứ 4: đoạn 20 s (bước 2,0 s → 10 khung) + khung dữ liệu làm ô cuối, cùng lưới 4 cột.
Cùng cách dựng với `scripts/p/kiem_mu.py dai` (ô rộng 480, lề 6, nhãn mốc tương đối góc trên-trái); ô khung dữ liệu không ghi mốc.
/opt/cine/bin/python design/m3/thu-phong-cach/dai4.py <video 20 s> <khung dữ liệu.png> <ra.jpg>
"""
import io, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

def main(video, data, out, buoc=2.0, rong=480):
    ts = [round(i * buoc, 3) for i in range(10)]
    ims = []
    for t in ts:
        r = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-ss', f'{t:.3f}', '-i', video, '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True, check=True)
        im = Image.open(io.BytesIO(r.stdout)).convert('RGB'); ims.append(im.resize((rong, round(rong * im.height / im.width))))
    dd = Image.open(data).convert('RGB'); ims.append(dd.resize((rong, round(rong * dd.height / dd.width)), Image.LANCZOS))
    C = 4; R = (len(ims) + C - 1) // C; w, h = ims[0].size; pad = 6
    sheet = Image.new('RGB', (C * w + (C + 1) * pad, R * h + (R + 1) * pad), (24, 24, 24)); d = ImageDraw.Draw(sheet)
    try: f = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf', 18)
    except Exception: f = ImageFont.load_default()
    for i, im in enumerate(ims):
        x = pad + (i % C) * (w + pad); y = pad + (i // C) * (h + pad); sheet.paste(im, (x, y))
        if i < len(ts):
            lab = f"{ts[i]:.1f} s".replace('.', ','); d.rectangle([x, y, x + 64, y + 24], fill=(0, 0, 0)); d.text((x + 5, y + 2), lab, fill=(255, 255, 255), font=f)
    sheet.save(out, quality=90); print(out, len(ims), 'ô', sheet.size)

if __name__ == '__main__':
    main(*sys.argv[1:4])
