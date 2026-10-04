"""3 phương án thumbnail ep01 (1280×720, cùng hệ nhận diện: giấy ngà/chàm đêm, hổ phách, DejaVu Serif Bold).
python thumb_ep01.py <thư mục khung nguồn> <thư mục ra>"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
S, O = sys.argv[1], sys.argv[2]
SER = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'; SAN = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
AMB = (242, 178, 76); IVO = (246, 236, 214); INK = (12, 14, 28)
def base(f, crop=None, dark=0.0):
    im = Image.open(f).convert('RGB')
    if crop: im = im.crop(crop)
    im = im.resize((1280, 720), Image.LANCZOS)
    if dark:
        g = Image.new('L', (1280, 720)); d = ImageDraw.Draw(g)
        for x in range(1280): d.line([(x, 0), (x, 720)], fill=int(255 * dark * max(0, 1 - x / 760)))
        im = Image.composite(Image.new('RGB', im.size, INK), im, g)
    return im
def txt(im, xy, s, size, fill, font=SER, shadow=True, anchor='la'):
    d = ImageDraw.Draw(im); f = ImageFont.truetype(font, size)
    if shadow:
        sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((xy[0] + 3, xy[1] + 4), s, font=f, fill=(0, 0, 0, 200), anchor=anchor)
        im.paste(sh.filter(ImageFilter.GaussianBlur(5)), (0, 0), sh.filter(ImageFilter.GaussianBlur(5)))
    d.text(xy, s, font=f, fill=fill, anchor=anchor)
def mark(im):   # dấu kênh góc dưới trái: cột đèn nhỏ + tên kênh
    d = ImageDraw.Draw(im); x, y = 44, 662
    d.rectangle([x, y - 34, x + 3, y], fill=AMB); d.rectangle([x - 6, y - 44, x + 9, y - 34], fill=AMB)
    d.text((x + 22, y - 30), 'LAST LAMPLIGHTERS', font=ImageFont.truetype(SAN, 22), fill=IVO)
# T1: ngọn đèn bừng (đoạn 01, e01c) + câu hỏi kênh
a = base(f'{S}/src-01.png', crop=(240, 0, 1920, 945), dark=0.85)
txt(a, (60, 150), 'THE LAST', 92, IVO); txt(a, (60, 250), 'LAMPLIGHTERS', 92, AMB)
txt(a, (64, 380), 'Which jobs are next?', 52, IVO); mark(a); a.save(f'{O}/T1-den-bung.jpg', quality=90)
# T2: lưới cửa sổ văn phòng trên phố đèn khí (10–13) + −34%
b = base(f'{S}/src-10-13.png', crop=(160, 60, 1760, 960)); b = ImageEnhance.Brightness(b).enhance(1.12)
pan = Image.new('RGBA', b.size, (0, 0, 0, 0)); ImageDraw.Draw(pan).rounded_rectangle([40, 70, 600, 470], 18, fill=(10, 12, 26, 210)); b.paste(pan, (0, 0), pan)
txt(b, (70, 100), '−34%', 170, AMB, shadow=False); txt(b, (76, 300), 'word processors', 40, IVO, shadow=False); txt(b, (76, 345), '& typists, 2025–35', 40, IVO, shadow=False)
txt(b, (76, 405), 'U.S. BLS projection', 28, (200, 196, 186), font=SAN, shadow=False); mark(b); b.save(f'{O}/T2-tru-34.jpg', quality=90)
# T3: London hôm nay (đoạn 07) + "5"
c = base(f'{S}/src-07.png', crop=(480, 0, 1920, 810), dark=0.7)
txt(c, (60, 120), '5', 260, AMB); txt(c, (230, 175), 'lamplighters', 70, IVO); txt(c, (232, 260), 'in London, 2023', 46, IVO)
txt(c, (64, 420), 'Who are the last', 58, IVO); txt(c, (64, 490), 'of our time?', 58, AMB); mark(c); c.save(f'{O}/T3-con-5.jpg', quality=90)
