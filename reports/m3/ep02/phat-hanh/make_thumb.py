#!/opt/cine/bin/python
"""Thumbnail tập 2 (1280×720) từ khung trung gian + chữ lớn. python make_thumb.py <out_dir> <thư mục ra>"""
import subprocess, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
O, D = sys.argv[1], sys.argv[2]; os.makedirs(D, exist_ok=True)
SB, SR = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def frame(seg, t):
    p = f'{D}/_f.png'; subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', f'{O}/sec/{seg}.mkv', '-frames:v', '1', '-vf', 'scale=1280:720', p], check=True)
    return Image.open(p).convert('RGB')
def card(im, lines, pos='left'):
    d = ImageDraw.Draw(im, 'RGBA'); y = 70
    for s, px, col, f in lines:
        F = ImageFont.truetype(f, px); w = d.textlength(s, font=F); x = 60 if pos == 'left' else (1280 - w) / 2
        d.rectangle([x - 18, y - 10, x + w + 18, y + px + 14], fill=(20, 26, 46, 215)); d.text((x, y), s, font=F, fill=col); y += px + 34
    return im
CREAM, AMB = (236, 223, 190), (232, 160, 80)
# T1: phòng tổng đài + câu hỏi
im = frame('00', 4.0); card(im, [('AUTOMATION HURT THE OPERATORS.', 56, CREAM, SB), ('NOT THE NEXT GENERATION.', 56, CREAM, SB), ('WHAT ABOUT US?', 72, AMB, SB)]).save(f'{D}/ll-ep02-thumb-T1.jpg', quality=90)
# T2: thẻ so sánh −16,1 % / −5,3 %
im = frame('11', 40.0); card(im, [('THEN −16%  ·  NEXT −5%?', 66, CREAM, SB)], 'center').save(f'{D}/ll-ep02-thumb-T2.jpg', quality=90)
os.remove(f'{D}/_f.png'); print('ok')
