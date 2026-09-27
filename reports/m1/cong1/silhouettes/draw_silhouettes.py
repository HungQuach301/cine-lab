"""Cổng 1 — phác thảo silhouette cho 3 phương án (bà lão thắp đèn + đứa trẻ).
Chỉ là phác thảo đọc-dáng (luật C2: tô đen đặc vẫn nhận ra ai, đang làm gì), không phải model sheet.
Vẽ bằng hình cơ bản (elip, khối, nét bo tròn) ở 4× rồi thu nhỏ để khử răng cưa. Tỷ lệ chung: 1 đơn vị = 1 px ở bản 1×,
bà lão cao ~520–600, trẻ 8–10 tuổi ~330–380 (đứng cùng một đường đất để so dáng).
Chạy: /opt/cine/bin/python reports/m1/cong1/silhouettes/draw_silhouettes.py
Ghi: P{1,2,3}-{lamplighter,child}.png (mỗi nhân vật một file) và CONG1-silhouettes.png (bảng tổng hợp)."""
import math, os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SS = 4                     # hệ số siêu lấy mẫu
PAPER = (239, 230, 214)
INK = (18, 14, 20)
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'


class Pen:
    """Vẽ theo toạ độ nhân vật: gốc (0,0) ở giữa hai bàn chân trên mặt đất, y dương hướng LÊN."""
    def __init__(self, d, ox, gy):
        self.d, self.ox, self.gy = d, ox, gy

    def p(self, x, y):
        return ((self.ox + x) * SS, (self.gy - y) * SS)

    def poly(self, pts):
        self.d.polygon([self.p(x, y) for x, y in pts], fill=INK)

    def ell(self, cx, cy, rx, ry, rot=0.0, n=48):
        pts = []
        for i in range(n):
            a = 2 * math.pi * i / n
            x, y = rx * math.cos(a), ry * math.sin(a)
            c, s = math.cos(rot), math.sin(rot)
            pts.append((cx + x * c - y * s, cy + x * s + y * c))
        self.poly(pts)

    def line(self, pts, w):
        """Nét bo tròn hai đầu và các khớp (chi, sào, dây)."""
        q = [self.p(x, y) for x, y in pts]
        self.d.line(q, fill=INK, width=int(w * SS), joint='curve')
        r = w * SS / 2
        for x, y in (q[0], q[-1]):
            self.d.ellipse((x - r, y - r, x + r, y + r), fill=INK)

    def rect(self, x0, y0, x1, y1, rot=0.0, cx=None, cy=None):
        cx = (x0 + x1) / 2 if cx is None else cx
        cy = (y0 + y1) / 2 if cy is None else cy
        c, s = math.cos(rot), math.sin(rot)
        pts = []
        for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)):
            dx, dy = x - cx, y - cy
            pts.append((cx + dx * c - dy * s, cy + dx * s + dy * c))
        self.poly(pts)

    def ring(self, cx, cy, r, w):
        x, y = self.p(cx, cy)
        self.d.ellipse((x - r * SS, y - r * SS, x + r * SS, y + r * SS), outline=INK, width=int(w * SS))


# ---------------- Phương án 1 — "Two Knocks" ----------------
def hester(P):
    """Hester Pell, 71: thấp, đậm, lưng còng; áo khoác dài chạm mắt cá xoè như chuông; mũ len có vạt che tai;
    tay phải dựng sào có móc cao hơn người, đang gõ hai lần vào cột; tay trái xách đèn lồng thiếc bên hông."""
    # chân + giày
    P.line([(-26, 70), (-30, 6)], 20); P.line([(22, 70), (26, 6)], 20)
    P.ell(-36, 8, 24, 10); P.ell(32, 8, 24, 10)
    # áo khoác chuông
    P.poly([(-70, 28), (78, 28), (60, 200), (48, 330), (10, 372), (-40, 360), (-58, 300), (-66, 160)])
    # lưng còng + vai
    P.ell(-8, 350, 62, 46, 0.25)
    # khăn quàng dày
    P.ell(22, 382, 38, 22, 0.2)
    # đầu cúi ra trước, mũ len vạt tai
    P.ell(46, 420, 34, 38, 0.15)
    P.ell(40, 446, 40, 26, 0.1)                          # chỏm mũ
    P.poly([(8, 430), (18, 430), (22, 390), (12, 384)])  # vạt tai sau
    P.ell(42, 474, 10, 10)                               # quả len trên đỉnh
    P.ell(80, 412, 7, 9)                                 # mũi
    # tay phải -> sào (nghiêng nhẹ, đầu móc gõ vào cột bên phải)
    P.line([(46, 330), (92, 270), (118, 300)], 22)
    P.line([(96, 40), (150, 640)], 9)                    # sào
    P.line([(150, 640), (158, 668), (174, 672), (182, 656)], 7)  # móc
    # cột đèn (một phần) để thấy hành động "gõ"
    P.rect(186, 0, 206, 690)
    P.line([(160, 668), (178, 660)], 3)                  # vạch gõ
    P.line([(160, 690), (178, 690)], 3)
    # tay trái -> đèn lồng thiếc có miếng hàn
    P.line([(-52, 320), (-78, 230), (-84, 172)], 22)
    P.line([(-84, 172), (-84, 150)], 4)
    P.poly([(-106, 150), (-62, 150), (-58, 90), (-110, 90)])
    P.poly([(-114, 92), (-54, 92), (-64, 76), (-104, 76)])
    P.ell(-84, 160, 12, 8)


def tobin(P):
    """Tobin, 9: mũ trùm của một chiếc áo quá khổ (vai rộng, tay áo dài quá tay), đôi găng nối bằng một sợi dây
    vòng qua cổ áo lủng lẳng; hai tay nắm vào nhau trước ngực — dáng co lại."""
    P.line([(-14, 110), (-16, 6)], 14); P.line([(14, 110), (18, 6)], 14)
    P.ell(-22, 7, 17, 8); P.ell(24, 7, 17, 8)
    # áo quá khổ tới gối
    P.poly([(-52, 100), (54, 100), (48, 180), (44, 250), (24, 272), (-26, 272), (-46, 250), (-50, 180)])
    # mũ trùm to
    P.ell(0, 300, 40, 44)
    P.poly([(-38, 300), (38, 300), (30, 262), (-30, 262)])
    # mặt nhìn ra (lỗ trong mũ trùm: vẽ nền giấy)
    x0, y0 = P.p(-4, 318); x1, y1 = P.p(26, 280)
    P.d.ellipse((x0, y0, x1, y1), fill=PAPER)
    P.ell(12, 300, 12, 15)                               # khuôn mặt nhìn nghiêng trong mũ trùm
    # hai tay áo dài chụm trước ngực, găng lủng lẳng trên dây
    P.line([(-40, 244), (-30, 196), (-2, 188)], 18)
    P.line([(40, 244), (32, 198), (6, 190)], 18)
    P.ell(2, 190, 14, 12)
    P.line([(-34, 258), (-44, 170), (-40, 120)], 2.5)    # dây găng
    P.line([(34, 258), (46, 176), (44, 132)], 2.5)
    P.ell(-40, 112, 10, 13); P.ell(44, 124, 10, 13)       # hai chiếc găng


# ---------------- Phương án 2 — "The Lamp Ledger" ----------------
def maud(P):
    """Maud Kettering, 78: cao, gầy, hơi khom; váy dài hẹp; mũ rộng vành mềm; khăn quàng dài bay một đầu ra sau;
    kẹp cuốn sổ đèn dày dưới nách trái, tay phải chống sào như chống gậy."""
    P.line([(-10, 120), (-12, 6)], 14); P.line([(14, 120), (16, 6)], 14)
    P.ell(-18, 7, 20, 7); P.ell(24, 7, 20, 7)
    # váy dài hẹp + thân áo
    P.poly([(-38, 24), (42, 24), (36, 200), (30, 380), (-26, 380), (-32, 200)])
    P.ell(0, 400, 36, 40, -0.12)                         # vai hơi khom
    # cổ dài + đầu hơi đưa ra trước
    P.line([(8, 420), (20, 470)], 18)
    P.ell(26, 498, 24, 30, -0.1)
    # mũ rộng vành mềm
    P.ell(22, 520, 62, 12, -0.08)
    P.ell(20, 536, 30, 20)
    # khăn quàng dài bay ra sau
    P.poly([(-10, 452), (24, 456), (10, 432), (-40, 420), (-110, 380), (-150, 356), (-160, 368), (-118, 398), (-40, 440)])
    # tay trái kẹp sổ dày dưới nách
    P.line([(-22, 400), (-40, 330), (-10, 296)], 16)
    P.rect(-66, 296, -8, 372, rot=-0.18)                 # cuốn sổ
    P.rect(-70, 330, -60, 338, rot=-0.18)                # dây buộc chì thò ra
    P.line([(-66, 334), (-84, 312)], 3)
    # tay phải chống sào như gậy (sào cao)
    P.line([(24, 400), (52, 330), (66, 280)], 16)
    P.line([(76, 0), (58, 640)], 8)
    P.line([(58, 640), (54, 668), (40, 672), (34, 658)], 6)


def wren(P):
    """Wren, 8: bím tóc duy nhất vểnh ngang; áo khoác ngắn; ủng to; hai tay nâng một hũ mứt rỗng (nắp đục lỗ) ngang
    ngực; người nghiêng như vừa ló ra sau một bức tường."""
    P.line([(-12, 100), (-14, 30)], 14); P.line([(14, 100), (16, 30)], 14)
    P.poly([(-30, 36), (0, 36), (-2, 0), (-36, 0)])      # ủng to
    P.poly([(4, 36), (34, 36), (38, 0), (4, 0)])
    # áo khoác ngắn
    P.poly([(-40, 94), (40, 94), (34, 200), (22, 236), (-22, 236), (-34, 200)])
    # đầu nghiêng + bím tóc vểnh
    P.ell(6, 272, 32, 34, 0.18)
    P.line([(-22, 282), (-54, 290), (-72, 280)], 11)
    P.ell(-78, 278, 8, 7)
    P.poly([(-24, 290), (30, 304), (30, 296), (-20, 280)])  # tóc mái / mái ngố
    # hai tay nâng hũ
    P.line([(-30, 220), (-26, 176), (-8, 164)], 14)
    P.line([(30, 220), (30, 176), (18, 164)], 14)
    P.rect(-14, 150, 26, 206)                            # hũ
    P.rect(-17, 206, 29, 216)                            # nắp
    for i in range(4):                                   # lỗ trên nắp (nền giấy)
        x, y = P.p(-10 + i * 11, 213)
        P.d.ellipse((x - 2 * SS, y - 2 * SS, x + 2 * SS, y + 2 * SS), fill=PAPER)
    x0, y0 = P.p(-6, 198); x1, y1 = P.p(18, 158)         # thân hũ trong suốt: nền giấy ở giữa
    P.d.rounded_rectangle((x0, y0, x1, y1), radius=4 * SS, fill=PAPER)


# ---------------- Phương án 3 — "Keep a Little Dark" ----------------
def ida(P):
    """Ida Marrow, 74: cao trung bình, thẳng lưng; áo khoác dài xẻ tà; mũ phớt mềm vành hẹp; vác một chiếc thang gỗ
    ngắn chéo qua vai phải (dáng nhận ra từ xa); tay trái xoè ra hơ trước ngọn lửa tưởng tượng (thói quen đếm ba)."""
    P.line([(-18, 150), (-26, 6)], 16); P.line([(20, 150), (30, 6)], 16)
    P.ell(-32, 7, 21, 8); P.ell(36, 7, 21, 8)
    # áo dài xẻ tà
    P.poly([(-52, 90), (-4, 90), (0, 130), (6, 90), (56, 90), (44, 300), (36, 420), (-32, 420), (-42, 300)])
    P.ell(2, 424, 44, 26)
    # cổ + đầu thẳng
    P.line([(4, 440), (6, 468)], 18)
    P.ell(6, 494, 26, 31)
    # mũ phớt vành hẹp
    P.ell(6, 516, 44, 9)
    P.poly([(-22, 518), (34, 518), (28, 552), (-16, 552)])
    # thang chéo qua vai phải
    for off in (-9, 9):
        P.line([(-150 + off, 300 + off * 2), (170 + off, 560 + off * 2)], 7)
    for i in range(1, 8):
        t = i / 8
        x, y = -150 + 320 * t, 300 + 260 * t
        P.line([(x - 7, y + 11), (x + 7, y - 11)], 5)
    # tay phải giữ thang
    P.line([(26, 420), (50, 380), (60, 430)], 16)
    # tay trái hơ ra trước, bàn tay mở
    P.line([(-26, 410), (-70, 360), (-110, 350)], 16)
    for a in (-0.5, -0.2, 0.1, 0.4):
        P.line([(-112, 350), (-112 - 24 * math.cos(a), 350 + 24 * math.sin(a))], 5)


def cas(P):
    """Cas (Casimir), 10: gầy, chân tay dài; mũ len có quả bông; tai vểnh; áo len ngắn; hai tay giơ cao đan ngón cái
    vào nhau, xoè ngón thành đôi cánh — đang làm chim bóng."""
    P.line([(-14, 150), (-18, 6)], 13); P.line([(14, 150), (20, 6)], 13)
    P.ell(-24, 7, 16, 7); P.ell(26, 7, 16, 7)
    P.poly([(-26, 140), (26, 140), (30, 180), (32, 270), (-30, 270), (-30, 180)])
    # đầu + mũ len quả bông + tai vểnh
    P.ell(0, 300, 26, 30)
    P.poly([(-26, 306), (26, 306), (18, 342), (-18, 342)])
    P.ell(0, 350, 12, 12)
    P.ell(-27, 296, 7, 10, 0.3); P.ell(27, 296, 7, 10, -0.3)
    # hai tay giơ lên trước mặt, đan ngón cái -> chim bóng
    P.line([(-24, 262), (-50, 330), (-14, 404)], 12)
    P.line([(24, 262), (50, 330), (14, 404)], 12)
    P.ell(0, 410, 16, 10)
    for side in (-1, 1):
        for k, a in enumerate((0.35, 0.6, 0.85, 1.1)):
            ang = math.pi / 2 - side * a
            L = 34 - k * 3
            P.line([(side * 8, 414), (side * 8 + L * math.cos(ang) * 1.3, 414 + L * math.sin(ang) * 0.9)], 5)
    P.line([(0, 418), (0, 436)], 6)                      # ngón cái đan = đầu chim


OPTIONS = [
    ('P1', 'Two Knocks', ('Hester Pell, 71', hester, 560), ('Tobin, 9', tobin, 360)),
    ('P2', 'The Lamp Ledger', ('Maud Kettering, 78', maud, 600), ('Wren, 8', wren, 330)),
    ('P3', 'Keep a Little Dark', ('Ida Marrow, 74', ida, 580), ('Cas, 10', cas, 400)),
]
ROLE_FILE = ('lamplighter', 'child')


def canvas(w, h):
    im = Image.new('RGB', (w * SS, h * SS), PAPER)
    return im, ImageDraw.Draw(im)


def ground(d, x0, x1, gy):
    d.line([(x0 * SS, gy * SS), (x1 * SS, gy * SS)], fill=(120, 108, 96), width=2 * SS)


def label(im, text, xy, size, bold=False):
    f = ImageFont.truetype(FONT_B if bold else FONT, size)
    ImageDraw.Draw(im).text(xy, text, font=f, fill=(60, 52, 48))


def single(tag, role, name, fn):
    W, H, GY = 640, 900, 830
    im, d = canvas(W, H)
    ground(d, 20, W - 20, GY)
    fn(Pen(d, W // 2 - 20, GY))
    im = im.resize((W, H), Image.LANCZOS)
    label(im, f'{tag} · {name}', (20, 16), 22, True)
    label(im, 'silhouette sketch — Cổng 1 (chưa duyệt)', (20, 46), 15)
    out = os.path.join(HERE, f'{tag}-{role}.png'); im.save(out, optimize=True)
    return out


def sheet():
    CW, RH, GY0 = 700, 900, 830
    W, H = CW * 3, RH
    im, d = canvas(W, H)
    for i, (tag, title, adult, child) in enumerate(OPTIONS):
        x0 = i * CW
        ground(d, x0 + 30, x0 + CW - 30, GY0)
        adult[1](Pen(d, x0 + 250, GY0))
        child[1](Pen(d, x0 + 520, GY0))
    im = im.resize((W, H), Image.LANCZOS)
    for i, (tag, title, adult, child) in enumerate(OPTIONS):
        x0 = i * CW
        label(im, f'{tag} — "{title}"', (x0 + 30, 18), 26, True)
        label(im, adult[0], (x0 + 150, GY0 + 14), 19)
        label(im, child[0], (x0 + 470, GY0 + 14), 19)
    out = os.path.join(HERE, 'CONG1-silhouettes.png'); im.save(out, optimize=True)
    return out


if __name__ == '__main__':
    outs = []
    for tag, title, adult, child in OPTIONS:
        for role, (name, fn, _h) in zip(ROLE_FILE, (adult, child)):
            outs.append(single(tag, role, name, fn))
    outs.append(sheet())
    print('\n'.join(outs))
