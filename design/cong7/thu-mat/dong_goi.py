"""Cổng 7 THỬ MẶT — cháy phụ đề vào mp4 từng shot (y hệt thẻ của package.py: DejaVuSans 30, hộp tối, viền 2 px) rồi lập dải kiểm mù.
Chạy: /opt/cine/bin/python design/cong7/thu-mat/dong_goi.py <thư mục render (s03.mp4…)> <thư mục báo cáo reports/m2/cong7/thu-mat/V1>
Mốc thẻ theo layout-v21.text/elements.json (khung phim): L1 288–349, L2 1188–1259. Mốc shot trong phim: s03 8,5–10,5; s05 12,0–16,0; s22 49,5–52,5.
"""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H = 960, 540
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; FILL = (244, 241, 234)
SHOTS = {'s03': (8.5, 10.5, None), 's05': (12.0, 16.0, (288, 349, 'Evening, old street.')), 's22': (49.5, 52.5, (1188, 1259, 'Not yet... not yet.'))}


def card(txt, out):
    font = ImageFont.truetype(FONT, 30); full = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(full)
    tw = d.textlength(txt, font=font); x, y = (W - tw) / 2, H - 46 - 30
    l, t, r, bt = d.textbbox((x, y), txt, font=font); d.rounded_rectangle((l - 14, t - 9, r + 14, bt + 10), radius=6, fill=(12, 12, 14, 228))
    d.text((x, y), txt, font=font, fill=FILL + (255,), stroke_width=2, stroke_fill=(10, 10, 12, 255)); full.save(out)


def main(rd, od):
    os.makedirs(od, exist_ok=True)
    for s, (t0, t1, sub) in SHOTS.items():
        src = os.path.join(rd, f'{s}.mp4'); dst = os.path.join(od, f'{s}.mp4')
        if sub:
            f0, f1, txt = sub; png = os.path.join(rd, f'{s}_card.png'); card(txt, png); a, b = f0 - round(t0 * 24), f1 - round(t0 * 24)
            vf = f"[0:v][1:v]overlay=0:0:enable='between(n,{a},{b})':shortest=0:eof_action=pass,format=yuv420p[v]"
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-loop', '1', '-framerate', '24', '-i', png, '-filter_complex', vf, '-map', '[v]', '-frames:v', str(round((t1 - t0) * 24)),
                            '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-color_range', 'tv', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-r', '24', dst], check=True)
        else:
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', dst], check=True)
        subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), '../../../scripts/p/kiem_mu.py'), 'dai', dst, '0', f'{t1 - t0:.2f}', os.path.join(od, f'dai_{s}.jpg')], check=True)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
