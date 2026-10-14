#!/opt/cine/bin/python
"""Tờ liên hợp thư viện sticker K2V2 (nền bản đồ sepia + tự nhiên để rà viền/bóng trên cả hai bảng màu) → channel-k2/k2v2-mau/stickers-sheet.jpg"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont
REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'); D = os.path.join(REPO, 'design/k2v/stickers')
CACHE = os.environ.get('K2V_CACHE', '/var/tmp/cine-out/k2v-cache')
man = json.load(open(os.path.join(D, 'stickers.json'))); names = [k for k in man if not k.startswith('_')]
cols, cw, chh = 8, 240, 270; rows = (len(names) + cols - 1) // cols; W, H = cols * cw, rows * chh
bgs = []
for n in ('natural', 'sepia'):
    p = os.path.join(CACHE, 'relief/erie', n + '.jpg')
    bgs.append(Image.open(p).crop((1800, 1200, 1800 + W, 1200 + H)) if os.path.exists(p) else Image.new('RGB', (W, H), (200, 190, 160)))
out = Image.new('RGB', (W * 2, H)); F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
for b, bg in enumerate(bgs):
    out.paste(bg, (b * W, 0)); d = ImageDraw.Draw(out)
    for i, n in enumerate(names):
        im = Image.open(os.path.join(D, n + '.png')).convert('RGBA'); s = min((cw - 20) / im.width, (chh - 50) / im.height); im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        x, y = b * W + (i % cols) * cw, (i // cols) * chh; out.paste(im, (x + (cw - im.width) // 2, y + 8 + (chh - 50 - im.height) // 2), im); d.text((x + 10, y + chh - 32), n, fill=(20, 20, 20), font=F)
out.save(sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'channel-k2/k2v2-mau/stickers-sheet.jpg'), quality=82); print('ok', out.size)
