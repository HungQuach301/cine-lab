"""Cine Lab · M2.0 (c) — BỘ MẪU DỮ LIỆU B3: 5 khung mẫu 1920×1080 (D-MAP, D-BAR, D-TL, D-NUM, D-COL 3 cột), sinh THỦ TỤC.
Ngôn ngữ hình B3: nền đêm có vân giấy, tờ giấy ngà mép xé + bóng đổ giấy, hổ phách = đèn khí, trắng lạnh = đèn điện.
Bảng màu + cỡ chữ theo reports/m3/KE-HOACH-TAP-THU.md §2 (nhánh P). Font: DejaVu Sans / Sans Bold / Serif Bold (RIGHTS C4-F1, M2-F2..F4).
Số thật có nguồn ghi dòng nguồn; hình không đúng tỉ lệ ghi "Illustrative" (+ "Not to scale" cho bản đồ).
Đo tương phản: mỗi chữ ghi hộp bao; trên ảnh cuối, chữ = trung vị 5 % điểm gần màu chữ nhất, nền = trung vị 50 % điểm xa nhất (WCAG).
/opt/cine/bin/python design/m3/thu-phong-cach/bo_mau.py <thư mục ra>
"""
import json, os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_frame import paperize, deckle, ratio

FD = '/usr/share/fonts/truetype/dejavu/'
F = {'sans': FD + 'DejaVuSans.ttf', 'sansb': FD + 'DejaVuSans-Bold.ttf', 'serifb': FD + 'DejaVuSerif-Bold.ttf'}
NIGHT, PAPER, AMBER, COLD, GREY, INK, AMBER_D, BLUE = (0x14, 0x1B, 0x2D), (0xEF, 0xE6, 0xD2), (0xF0, 0xA9, 0x4A), (0xDC, 0xE6, 0xF0), (0xA7, 0xB1, 0xC2), (0x2E, 0x22, 0x19), (0x8A, 0x4F, 0x0E), (0x2B, 0x4A, 0x6F)
W, H, K = 1920, 1080, 2
MINUS = '−'

class Frame:
    def __init__(self, seed):
        bg = Image.new('RGB', (W, H), NIGHT)
        self.im = paperize(bg, seed, k=0.10, fib=0.06).resize((W * K, H * K), Image.BICUBIC).convert('RGBA')   # vân giấy nền: dither tự nhiên, không dải chuyển màu mịn
        self.d = ImageDraw.Draw(self.im); self.texts = []
    def text(self, xy, s, px, fill, font='sans', anchor='la'):
        f = ImageFont.truetype(F[font], int(px * K)); x, y = xy[0] * K, xy[1] * K
        self.d.text((x, y), s, font=f, fill=fill, anchor=anchor); bb = self.d.textbbox((x, y), s, font=f, anchor=anchor)
        self.texts.append({'s': s, 'px': px, 'fill': fill, 'box': [int(v / K) for v in bb]})
    def sheet(self, x, y, w, h, seed, ang=0.0):
        """tờ giấy ngà mép xé + bóng đổ giấy; trả ImageDraw vẽ trực tiếp lên tờ (toạ độ ảnh cuối)"""
        p = paperize(Image.new('RGB', (w, h), PAPER), seed, k=0.05, fib=0.04); p.putalpha(deckle(w, h, seed + 1, amp=8))
        p = p.resize((w * K, h * K), Image.BICUBIC)
        sh = Image.new('RGBA', p.size, (0, 0, 0, 0)); sh.putalpha(p.getchannel('A').point(lambda v: int(v * 0.55))); sh = sh.filter(ImageFilter.GaussianBlur(14))
        self.im.alpha_composite(sh, (x * K + 16, y * K + 20)); self.im.alpha_composite(p, (x * K, y * K))
    def line(self, pts, fill, w): self.d.line([(a * K, b * K) for a, b in pts], fill=fill, width=int(w * K), joint='curve')
    def rect(self, b, fill, outline=None, w=0): self.d.rectangle([v * K for v in b], fill=fill, outline=outline, width=int(w * K))
    def dot(self, x, y, r, fill, outline=None): self.d.ellipse([(x - r) * K, (y - r) * K, (x + r) * K, (y + r) * K], fill=fill, outline=outline, width=2 * K)
    def save(self, path):
        out = self.im.convert('RGB').resize((W, H), Image.LANCZOS); out.save(path)
        a = np.asarray(out).astype(int); res = []
        for t in self.texts:
            x0, y0, x1, y1 = t['box']; x0, y0 = max(0, x0 - 2), max(0, y0 - 2); px = a[y0:y1 + 2, x0:x1 + 2].reshape(-1, 3)
            dist = np.abs(px - np.array(t['fill'][:3])).sum(1); o = np.argsort(dist)
            fg = tuple(int(v) for v in np.median(px[o[: max(1, len(o) // 20)]], axis=0)); bg = tuple(int(v) for v in np.median(px[o[len(o) // 2:]], axis=0))
            res.append({'text': t['s'], 'px': t['px'], 'fg': fg, 'bg': bg, 'ratio': round(ratio(fg, bg), 2)})
        return res

def src(f, s): f.text((96, H - 54), s, 30, GREY, anchor='ls')

def d_map(out):
    f = Frame(301); f.sheet(96, 150, 1040, 830, 11, 0)
    # sông Thames (lam mực), phố (mực nâu), chấm đèn hổ phách — HÌNH MINH HOẠ, không đúng tỉ lệ
    f.line([(110, 760), (330, 700), (560, 780), (800, 720), (1120, 790)], BLUE, 46)
    rng = np.random.default_rng(4)
    streets = [[(150, 330), (1080, 330)], [(150, 470), (900, 470)], [(260, 230), (360, 690)], [(520, 230), (600, 690)], [(800, 260), (860, 690)], [(150, 600), (1000, 620)]]
    for s in streets: f.line(s, INK, 9)
    for s in streets:
        n = 14
        for i in range(n): u = (i + 0.5) / n; f.dot(s[0][0] + (s[1][0] - s[0][0]) * u, s[0][1] + (s[1][1] - s[0][1]) * u, 7, AMBER, INK)
    f.line([(560, 400), (900, 400)], AMBER_D, 14)   # Pall Mall
    f.text((620, 420), 'Pall Mall · 1807', 34, AMBER_D, 'sansb', 'la')
    f.text((140, 200), 'LONDON', 64, INK, 'serifb')
    f.text((1096, 950), 'Thames', 32, BLUE, 'sans', 'rs')
    f.text((1190, 330), '40,000+', 140, AMBER, 'serifb')
    f.text((1214, 560), 'gas lamps by the 1820s', 40, PAPER)
    f.text((1214, 620), 'some 215 miles of streets', 40, PAPER)
    f.text((W - 96, 54 + 30), 'Illustrative · Not to scale', 30, GREY, 'sans', 'rs')
    src(f, 'Source: English Heritage'); return f.save(out)

def d_bar(out):
    f = Frame(302); f.text((96, 70), "London's gas lamps", 64, PAPER, 'serifb')
    f.text((96, 160), 'Same scale, starting at zero', 34, GREY)
    data = [('1820s', 40000, '40,000+'), ('2015', 1500, '~1,500'), ('2023', 1100, '~1,100')]
    base, top, x0, bw, gap = 900, 300, 260, 150, 330
    f.line([(180, base), (1500, base)], PAPER, 4)
    for i, (yr, v, lab) in enumerate(data):
        x = x0 + i * (bw + gap); h = (base - top) * v / 40000
        # cột = cột đèn cắt giấy: thân + thanh ngang + đầu đèn hổ phách
        f.rect([x + bw * 0.38, base - h, x + bw * 0.62, base], AMBER)
        f.rect([x + bw * 0.15, base - h, x + bw * 0.85, base - h + 10], AMBER)
        f.text((x + bw / 2, base - h - 24), lab, 64, AMBER if i == 0 else PAPER, 'serifb', 'ms')
        f.text((x + bw / 2, base + 24), yr, 40, PAPER, 'sans', 'mt')
    f.text((1420, 520), '5 lamplighters', 48, PAPER, 'sansb')
    f.text((1420, 585), 'still tend them', 40, PAPER)
    f.text((1420, 640), '(British Gas, 2023)', 34, GREY)
    src(f, 'Sources: English Heritage; NPR (2015); British Gas (2023)'); return f.save(out)

def d_tl(out):
    f = Frame(303); f.text((96, 70), 'From gas to electric', 64, PAPER, 'serifb')
    ev = [('1807', 'Pall Mall lit by gas', AMBER), ('1812', 'Gas company gets royal charter', AMBER), ('1820s', '40,000+ gas lamps in London', AMBER),
          ('1878', 'Electric arc lamps, Paris', COLD), ('1907', 'New York lamplighters strike', COLD), ('2023', '5 lamplighters left in London', AMBER)]
    y, x0, x1 = 560, 150, 1770
    f.line([(x0, y), (x1, y)], PAPER, 5)
    for i, (yr, s, c) in enumerate(ev):
        x = x0 + (x1 - x0) * (i + 0.5) / len(ev); f.dot(x, y, 16, c, NIGHT)
        up = i % 2 == 0
        f.text((x, y - 50 if up else y + 50), yr, 54, c, 'serifb', 'ms' if up else 'mt')
        words = s.split(' '); half = (len(words) + 1) // 2
        for k, ln in enumerate([' '.join(words[:half]), ' '.join(words[half:])]):
            f.text((x, (y - 130 - (1 - k) * 44) if up else (y + 130 + k * 44)), ln, 32, PAPER, 'sans', 'ms' if up else 'mt')
    f.text((W - 96, 1080 - 54 - 50), 'amber = gas · cold white = electric', 30, GREY, 'sans', 'rs')
    src(f, 'Sources: English Heritage; Gas Light & Coke Co. charter; NPR; British Gas'); return f.save(out)

def d_num(out):
    f = Frame(304); f.sheet(1080, 170, 740, 760, 41)
    # lưới 270 ô (27 × 10) trên tờ giấy: 269 ô mực lam, 1 ô tắt (khung rỗng) — biểu tượng hoá, đúng số 270
    cx, cy, s = 1130, 250, 24
    for k in range(270):
        i, j = k % 27, k // 27; x, y = cx + i * s, cy + j * s * 1.4
        if k == 200: f.rect([x, y, x + s - 6, y + s * 1.4 - 8], None, INK, 2)
        else: f.rect([x, y, x + s - 6, y + s * 1.4 - 8], BLUE)
    f.text((1130, 760), 'Elevator operator', 40, INK, 'sansb')
    f.text((1130, 815), 'the one job automated away', 32, INK)
    f.text((96, 300), '1 of ~270', 150, AMBER, 'serifb')   # M2.1 (e): câu chủ dự án duyệt
    f.text((100, 560), 'Only 1 of ~270 occupations was', 40, PAPER)
    f.text((100, 615), 'eliminated mainly by automation', 40, PAPER)
    src(f, 'Source: J. Bessen (2016), NBER · 271 occupations listed'); return f.save(out)

def d_col(out):
    f = Frame(305); f.text((96, 70), 'Then · Today · Next', 64, PAPER, 'serifb')
    cols = [('THEN', '40,000+', ['gas lamps,', 'London 1820s'], AMBER, 'English Heritage'),
            ('TODAY', '5', ['lamplighters,', '~1,100 lamps (2023)'], AMBER, 'British Gas'),
            ('NEXT', MINUS + '34%', ['word processors', 'and typists', 'U.S. projection 2025–35'], COLD, 'U.S. BLS')]
    for i, (h, n, lines, c, s) in enumerate(cols):
        x = 96 + i * 590; f.sheet(x, 200, 540, 720, 51 + i)
        f.text((x + 40, 260), h, 40, INK, 'sansb')
        f.text((x + 40, 330), n, 100 if len(n) > 4 else 140, AMBER_D if c == AMBER else BLUE, 'serifb')
        for k, ln in enumerate(lines): f.text((x + 40, 540 + k * 52), ln, 38, INK)
        f.text((x + 40, 860), s, 30, BLUE)
    src(f, 'Sources: English Heritage; British Gas (2023); U.S. BLS Employment Projections 2025–35'); return f.save(out)

if __name__ == '__main__':
    o = sys.argv[1]; os.makedirs(o, exist_ok=True); rep = {}
    for n, fn in [('d-map', d_map), ('d-bar', d_bar), ('d-tl', d_tl), ('d-num', d_num), ('d-col', d_col)]:
        r = fn(f'{o}/mau-{n}.png'); rep[n] = r; m = min(r, key=lambda t: t['ratio'])
        print(f"{n}: {len(r)} chữ · tương phản nhỏ nhất {m['ratio']}:1 ('{m['text']}', {m['px']} px) · cỡ nhỏ nhất {min(t['px'] for t in r)} px")
    json.dump(rep, open(f'{o}/tuong-phan.json', 'w'), ensure_ascii=False, indent=1)
