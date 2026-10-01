"""Cine Lab · M3 THỬ PHONG CÁCH — khung dữ liệu và tấm giấy số liệu, sinh THỦ TỤC (không tài sản ngoài).

Font: CHỈ DejaVu Sans Regular (RIGHTS.md C4-F1). Kết cấu giấy, mép xé, mảng sáng bậc thang: sinh bằng numpy (hạt giống cố định).
Số liệu MINH HOẠ, không phải số liệu lịch sử; mọi tấm đều ghi "Illustrative data".

/opt/cine/bin/python design/m3/thu-phong-cach/data_frame.py panels            → design/m3/thu-phong-cach/data/panel_{map,chart}.png
/opt/cine/bin/python design/m3/thu-phong-cach/data_frame.py b3 <ra.png>       → khung dữ liệu 1920×1080 ngôn ngữ B3 (cắt giấy)
/opt/cine/bin/python design/m3/thu-phong-cach/data_frame.py b1 <ra.png>       → khung dữ liệu 1920×1080 ngôn ngữ B1 (toon + viền nét)
/opt/cine/bin/python design/m3/thu-phong-cach/data_frame.py contrast <ra.png> → in tỉ lệ tương phản WCAG các cặp màu chữ/nền đã dùng
"""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'   # RIGHTS.md C4-F1
HERE = os.path.dirname(os.path.abspath(__file__))

# số liệu minh hoạ
STREETS = [('Ostler Street', 11), ('Mill Lane', 9), ("Tanner's Walk", 8), ('Chapel Row', 7), ('Clock Square', 6), ('River Steps', 5)]
YEARS = [(1890, 14), (1900, 12), (1905, 9), (1910, 7), (1915, 4), (1920, 1)]

INK = (33, 26, 23); CREAM = (236, 223, 190); AMBER = (196, 112, 38); NAVY = (20, 26, 46); LAMP = (255, 196, 110); RIVER = (122, 138, 150)

def font(px): return ImageFont.truetype(FONT, int(px))

def noise(h, w, seed, scales=((2, .4), (6, .3), (20, .2), (60, .1))):
    r = np.random.default_rng(seed); acc = np.zeros((h, w), np.float32)
    for s, a in scales:
        small = r.random((max(2, h // s + 2), max(2, w // s + 2))).astype(np.float32)
        im = Image.fromarray((small * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        acc += a * (np.asarray(im, np.float32) / 255.0)
    return acc  # ~0..1

def fibres(h, w, seed):
    r = np.random.default_rng(seed); im = Image.new('L', (w, h), 0); d = ImageDraw.Draw(im)
    for _ in range(int(w * h / 900)):
        x, y = r.random() * w, r.random() * h; a = r.normal(0.15, 0.5); L = r.uniform(6, 26)
        d.line([x, y, x + L * math.cos(a), y + L * math.sin(a)], fill=int(r.uniform(40, 120)), width=1)
    return np.asarray(im.filter(ImageFilter.GaussianBlur(0.6)), np.float32) / 255.0

def paperize(img, seed, k=0.07, fib=0.05):
    a = np.asarray(img.convert('RGB'), np.float32); h, w = a.shape[:2]
    n = noise(h, w, seed) - 0.5; f = fibres(h, w, seed + 1)
    a = a * (1 + k * 2 * n[..., None]) * (1 + fib * f[..., None])
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def deckle(w, h, seed, amp=7):
    """mặt nạ alpha mép giấy xé tay"""
    r = np.random.default_rng(seed); m = Image.new('L', (w, h), 0); d = ImageDraw.Draw(m)
    def edge(n): v = np.cumsum(r.normal(0, 1, n)); v -= np.linspace(v[0], v[-1], n); v = v / (np.abs(v).max() + 1e-6); return amp * (0.6 * v + 0.4 * r.uniform(-1, 1, n) * 0.3)
    N = 60; pts = []
    e = edge(N); pts += [(amp + i * (w - 2 * amp) / (N - 1), amp + e[i]) for i in range(N)]
    e = edge(N); pts += [(w - amp + e[i], amp + i * (h - 2 * amp) / (N - 1)) for i in range(N)]
    e = edge(N); pts += [(w - amp - i * (w - 2 * amp) / (N - 1), h - amp + e[i]) for i in range(N)]
    e = edge(N); pts += [(amp + e[i], h - amp - i * (h - 2 * amp) / (N - 1)) for i in range(N)]
    d.polygon(pts, fill=255); return m.filter(ImageFilter.GaussianBlur(0.8))

def text(d, xy, s, px, fill, anchor='la'):
    d.text(xy, s, font=font(px), fill=fill, anchor=anchor)

# ---------------------------------------------------------------- tấm bản đồ
def panel_map(W_=1200, H_=780, seed=11, style='b3'):
    W, H = 1200, 780; K = 2; w, h = W * K, H * K
    im = Image.new('RGB', (w, h), CREAM); d = ImageDraw.Draw(im)
    lw = 3 * K
    text(d, (40 * K, 34 * K), 'OLD TOWN', 46 * K, INK)
    text(d, (40 * K, 92 * K), 'Gas lamps per street, 1905', 28 * K, INK)
    # sông
    river = [(0, 650 * K), (220 * K, 610 * K), (460 * K, 670 * K), (700 * K, 620 * K), (900 * K, 655 * K)]
    d.line(river, fill=RIVER, width=40 * K, joint='curve')
    # phố: dải giấy mực (vùng bản đồ x 40–780; cột chú giải x 820–1160)
    S = {'Ostler Street': [(70 * K, 300 * K), (640 * K, 300 * K)], 'Mill Lane': [(170 * K, 300 * K), (250 * K, 590 * K)],
         "Tanner's Walk": [(400 * K, 300 * K), (470 * K, 600 * K)], 'Chapel Row': [(70 * K, 440 * K), (400 * K, 440 * K)],
         'River Steps': [(560 * K, 300 * K), (600 * K, 600 * K)]}
    for k, ln in S.items(): d.line(ln, fill=INK, width=16 * K)
    for k, ln in S.items(): d.line(ln, fill=(214, 198, 160), width=8 * K)
    d.rectangle([640 * K, 240 * K, 770 * K, 370 * K], outline=INK, width=lw * 2, fill=(214, 198, 160))
    def dot(x, y): r = 7 * K; d.ellipse([x - r, y - r, x + r, y + r], fill=AMBER, outline=INK, width=2 * K)
    def lamps(a, b, n):
        for i in range(n): u = (i + 0.5) / n; dot(a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)
    for (k, n) in STREETS:
        if k in S: lamps(*S[k], n)
    for i in range(6):
        a = 2 * math.pi * i / 6; dot(705 * K + 42 * K * math.cos(a), 305 * K + 42 * K * math.sin(a))
    # thẻ chữ cái trên bản đồ + chú giải bên phải (tên phố, số đèn)
    tags = {'Ostler Street': (40 * K, 300 * K), 'Mill Lane': (262 * K, 612 * K), "Tanner's Walk": (482 * K, 622 * K), 'Chapel Row': (40 * K, 440 * K),
            'River Steps': (612 * K, 622 * K), 'Clock Square': (705 * K, 215 * K)}
    for i, (k, n) in enumerate(STREETS):
        x, y = tags[k]; L_ = 'ABCDEF'[i]; r = 17 * K
        d.ellipse([x - r, y - r, x + r, y + r], fill=CREAM, outline=INK, width=3 * K); text(d, (x, y), L_, 22 * K, INK, 'mm')
        yy = 250 * K + i * 62 * K
        d.ellipse([830 * K - r, yy - r, 830 * K + r, yy + r], fill=CREAM, outline=INK, width=3 * K); text(d, (830 * K, yy), L_, 22 * K, INK, 'mm')
        text(d, (862 * K, yy), k, 26 * K, INK, 'lm'); text(d, (1160 * K, yy), str(n), 30 * K, INK, 'rm')
    tot = sum(n for _, n in STREETS)
    text(d, (1160 * K, 34 * K), f'{tot}', 110 * K, INK, 'ra')
    text(d, (1160 * K, 160 * K), 'gas lamps', 28 * K, INK, 'ra')
    text(d, (1160 * K, 740 * K), 'Illustrative data', 24 * K, INK, 'rs')
    im = im.resize((W_, H_), Image.LANCZOS)
    if style == 'b1': return im   # B1: mảng phẳng, không hạt giấy, mép thẳng
    im = paperize(im, seed)
    im.putalpha(deckle(W_, H_, seed + 5)); return im

# ---------------------------------------------------------------- tấm biểu đồ
def panel_chart(W_=1080, H_=780, seed=23, style='b3'):
    W, H = 1080, 780; K = 2; w, h = W * K, H * K
    im = Image.new('RGB', (w, h), CREAM); d = ImageDraw.Draw(im)
    text(d, (40 * K, 34 * K), 'LAMPLIGHTERS', 46 * K, INK)
    text(d, (40 * K, 92 * K), 'on the Old Town payroll', 28 * K, INK)
    x0, y0, bw, gap, top = 90 * K, 640 * K, 110 * K, 56 * K, 190 * K
    vmax = max(v for _, v in YEARS); hmax = y0 - top - 40 * K
    d.line([(60 * K, y0), (W * K - 50 * K, y0)], fill=INK, width=4 * K)
    for i, (yr, v) in enumerate(YEARS):
        x = x0 + i * (bw + gap); hh = hmax * v / vmax
        d.rectangle([x, y0 - hh, x + bw, y0], fill=AMBER, outline=INK, width=4 * K)
        text(d, (x + bw / 2, y0 - hh - 12 * K), str(v), 40 * K, INK, 'ms')
        text(d, (x + bw / 2, y0 + 16 * K), str(yr), 28 * K, INK, 'mt')
    text(d, (W * K - 40 * K, 34 * K), '14 → 1', 84 * K, INK, 'ra')
    text(d, (W * K - 40 * K, 740 * K), 'Illustrative data', 24 * K, INK, 'rs')
    im = im.resize((W_, H_), Image.LANCZOS)
    if style == 'b1': return im   # B1: mảng phẳng, không hạt giấy, mép thẳng
    im = paperize(im, seed)
    im.putalpha(deckle(W_, H_, seed + 5)); return im


def panels():
    os.makedirs(f'{HERE}/data', exist_ok=True)
    panel_map().save(f'{HERE}/data/panel_map.png'); panel_chart().save(f'{HERE}/data/panel_chart.png')
    print('ghi', f'{HERE}/data/panel_map.png', f'{HERE}/data/panel_chart.png')

# ---------------------------------------------------------------- khung 1920×1080
def stair(v, n):  # bậc thang (posterize) giá trị 0..1
    return np.floor(v * n + 0.5) / n

def frame_b3(out, cy=300, fall=1.6):
    W, H = 1920, 1080; K = 2; w, h = W * K, H * K
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # trời + vũng sáng ấm bậc thang quanh ngọn đèn (giữa-trên)
    sky = np.zeros((H, W, 3), np.float32) + np.array(NAVY, np.float32)
    cx = 1012; r = np.hypot((xx - cx) / 1.15, (yy - cy)) / 820
    pool = stair(np.clip(1 - r, 0, 1) ** fall if fall != 1.0 else 1.0 / (1.0 + (r * 4.2) ** 2), 5)
    warm = np.array([150, 92, 46], np.float32)
    bg = sky + pool[..., None] * (warm - sky * 0.4) * 0.85
    img = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8))
    img = paperize(img, 101, k=0.06, fib=0.04).convert('RGBA')
    # lớp mái nhà cắt giấy (3 lớp), mỗi lớp đổ bóng mềm xuống-phải
    rng = np.random.default_rng(7)
    def roofline(base, amp, seed, col):
        r = np.random.default_rng(seed); pts = [(0, H)]; x = -20
        while x < W + 40:
            wdt = r.uniform(110, 230); hh = base - r.uniform(0, amp)
            pts += [(x, hh), (x + wdt * 0.5, hh - r.uniform(30, 70)) if r.random() < 0.55 else (x + wdt * 0.5, hh), (x + wdt, hh)]
            if r.random() < 0.4: cxp = x + wdt * r.uniform(0.2, 0.8); pts += [(cxp, hh - 10), (cxp, hh - 46), (cxp + 18, hh - 46), (cxp + 18, hh - 10)]
            x += wdt
        pts += [(W, H)]; return pts, col
    layers = [roofline(560, 90, 3, (58, 64, 98)), roofline(700, 70, 5, (38, 42, 68)), roofline(880, 60, 9, (17, 19, 30))]
    for i, (pts, col) in enumerate(layers):
        sh = Image.new('L', (W, H), 0); ImageDraw.Draw(sh).polygon([(x + 9, y + 9) for x, y in pts], fill=150)
        sh = sh.filter(ImageFilter.GaussianBlur(6)); dark = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dark.putalpha(sh)
        img = Image.alpha_composite(img, dark)
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).polygon(pts, fill=col + (255,))
        # cửa sổ vàng thưa trên lớp giữa
        if i == 1:
            dl = ImageDraw.Draw(lay)
            for _ in range(14):
                x = rng.uniform(60, W - 60); y = rng.uniform(760, 880); dl.rectangle([x, y, x + 16, y + 24], fill=(214, 150, 70, 255))
        tex = paperize(lay.convert('RGB'), 200 + i, k=0.08, fib=0.05).convert('RGBA'); tex.putalpha(lay.getchannel('A'))
        img = Image.alpha_composite(img, tex)
    # cột đèn khí + ngọn đèn sáng (bóng cắt giấy)
    post = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dp = ImageDraw.Draw(post)
    px = 1012; dp.rectangle([px - 9, 330, px + 9, 1080], fill=(12, 12, 18, 255)); dp.polygon([(px - 40, 330), (px + 40, 330), (px + 26, 250), (px - 26, 250)], fill=(12, 12, 18, 255))
    dp.polygon([(px - 30, 322), (px + 30, 322), (px + 22, 262), (px - 22, 262)], fill=LAMP + (255,)); dp.polygon([(px - 48, 250), (px + 48, 250), (px, 214)], fill=(12, 12, 18, 255))
    img = Image.alpha_composite(img, post)
    # hai tấm giấy dán, đổ bóng
    def stick(p, x, y, ang):
        p = p.rotate(ang, resample=Image.BICUBIC, expand=True)
        a = p.getchannel('A'); sh = Image.new('RGBA', p.size, (0, 0, 0, 0)); sh.putalpha(a.point(lambda v: int(v * 0.6)))
        sh = sh.filter(ImageFilter.GaussianBlur(10))
        base = Image.new('RGBA', (W, H), (0, 0, 0, 0)); base.alpha_composite(sh, (x + 14, y + 16)); base.alpha_composite(p, (x, y)); return base
    img = Image.alpha_composite(img, stick(panel_map(860, 560, 11), 70, 300, 1.2))
    img = Image.alpha_composite(img, stick(panel_chart(760, 560, 23), 1090, 320, -0.9))
    d = ImageDraw.Draw(img)
    # kênh "Last Lamplighters" (chủ dự án chọn 01/10/2026) — khẩu hiệu gợi ý của P
    text(d, (74, 52), 'LAST LAMPLIGHTERS', 28, LAMP)
    text(d, (72, 96), 'Old Town, 1890\u20131920', 64, (241, 228, 198))
    text(d, (74, 182), 'Every era has its last lamplighters', 32, (241, 228, 198))
    d.rectangle([60, 960, 1010, 1052], fill=(20, 22, 34))
    text(d, (74, 1006), 'Then: 14 lamplighters became 1.  Now: which jobs are next?', 30, (241, 228, 198), 'lm')
    d.rectangle([1500, 1000, 1860, 1052], fill=(20, 22, 34))
    text(d, (1846, 1042), 'Illustrative data', 30, (241, 228, 198), 'rs')
    img.convert('RGB').save(out); print('ghi', out)


# ---------------------------------------------------------------- B3 v2: tấm trong cảnh, chữ LỚN (đọc được ở 720p trong đoạn 20 s)
def panel_map_v2(seed=11):
    W, H, K = 1200, 780, 2; im = Image.new('RGB', (W * K, H * K), CREAM); d = ImageDraw.Draw(im)
    text(d, (44 * K, 30 * K), 'OLD TOWN, 1905', 64 * K, INK)
    S = [[(60, 330), (700, 330)], [(170, 330), (250, 640)], [(400, 330), (470, 640)], [(60, 480), (400, 480)], [(560, 330), (600, 640)]]
    d.line([(0, 690 * K), (300 * K, 650 * K), (700 * K, 700 * K), (1200 * K, 660 * K)], fill=RIVER, width=50 * K, joint='curve')
    for ln in S: d.line([(x * K, y * K) for x, y in ln], fill=INK, width=22 * K)
    for ln in S: d.line([(x * K, y * K) for x, y in ln], fill=(214, 198, 160), width=10 * K)
    for (a, b), n in zip(S, [11, 9, 8, 7, 5]):
        for i in range(n):
            u = (i + 0.5) / n; x, y = (a[0] + (b[0] - a[0]) * u) * K, (a[1] + (b[1] - a[1]) * u) * K; r = 10 * K
            d.ellipse([x - r, y - r, x + r, y + r], fill=AMBER, outline=INK, width=3 * K)
    text(d, (1160 * K, 150 * K), '46', 230 * K, INK, 'ra')
    text(d, (1160 * K, 400 * K), 'gas lamps', 64 * K, INK, 'ra')
    text(d, (46 * K, 110 * K), 'Illustrative data', 44 * K, INK)
    im = im.resize((W, H), Image.LANCZOS); im = paperize(im, seed, k=0.05, fib=0.03); im.putalpha(deckle(W, H, seed + 5)); return im

def panel_chart_v2(seed=23):
    W, H, K = 1080, 780, 2; im = Image.new('RGB', (W * K, H * K), CREAM); d = ImageDraw.Draw(im)
    text(d, (40 * K, 30 * K), 'LAMPLIGHTERS', 64 * K, INK)
    text(d, (W * K - 40 * K, 20 * K), '14\u21921', 120 * K, INK, 'ra')
    YR = [(1890, 14), (1905, 9), (1920, 1)]; x0, y0, bw, gap, top = 90 * K, 600 * K, 230 * K, 90 * K, 230 * K
    d.line([(60 * K, y0), (W * K - 50 * K, y0)], fill=INK, width=6 * K)
    for i, (yr, v) in enumerate(YR):
        x = x0 + i * (bw + gap); hh = (y0 - top - 70 * K) * v / 14
        d.rectangle([x, y0 - hh, x + bw, y0], fill=AMBER, outline=INK, width=6 * K)
        text(d, (x + bw / 2, y0 - hh - 14 * K), str(v), 80 * K, INK, 'ms'); text(d, (x + bw / 2, y0 + 14 * K), str(yr), 60 * K, INK, 'mt')
    text(d, (W * K - 40 * K, 760 * K), 'Illustrative data', 48 * K, INK, 'rs')
    im = im.resize((W, H), Image.LANCZOS); im = paperize(im, seed, k=0.05, fib=0.03); im.putalpha(deckle(W, H, seed + 5)); return im

def panels_v2():
    panel_map_v2().save(f'{HERE}/data/panel_map_v2.png'); panel_chart_v2().save(f'{HERE}/data/panel_chart_v2.png'); print('ghi tấm v2')

def frame_b3v2(out):
    """Khung dữ liệu B3 v2: quầng đèn GIẢM DẦN liên tục từ ngọn đèn trong khung (không vành bậc), dither chống phân dải."""
    global stair
    s0 = stair; stair = lambda v, n: v + (np.random.default_rng(3).random(v.shape).astype(np.float32) - 0.5) / 255.0   # bỏ bậc, thêm dither
    try: frame_b3(out, cy=286, fall=1.0)
    finally: stair = s0

def frame_b1(out):
    """B1: mảng phẳng toon + viền nét đậm (không kết cấu giấy, không mép xé)."""
    W, H = 1920, 1080; K = 2; w, h = W * K, H * K
    img = Image.new('RGB', (w, h), (24, 30, 52)); d = ImageDraw.Draw(img)
    for i, (r, c) in enumerate([(900, (58, 48, 52)), (680, (96, 66, 44)), (470, (150, 98, 50))]):
        d.ellipse([960 * K - r * K * 1.15, 470 * K - r * K, 960 * K + r * K * 1.15, 470 * K + r * K], fill=c, outline=(10, 10, 14), width=6 * K)
    rng = np.random.default_rng(5)
    for base, col in ((720, (34, 40, 66)), (880, (20, 22, 36))):
        x = 0; pts = [(0, h)]
        while x < W:
            wd = rng.uniform(140, 240); hh = base - rng.uniform(0, 60); pts += [(x * K, hh * K), ((x + wd / 2) * K, (hh - 50) * K), ((x + wd) * K, hh * K)]; x += wd
        pts += [(w, h)]; d.polygon(pts, fill=col, outline=(8, 8, 12), width=8 * K)
    def box(p, x, y):
        q = p.convert('RGB'); bw, bh = q.size; img.paste(q.resize((bw * K, bh * K)), (x * K, y * K)); d.rectangle([x * K, y * K, (x + bw) * K, (y + bh) * K], outline=(10, 10, 14), width=8 * K)
    def flat(fn, W_, H_, seed):
        return fn(W_, H_, seed, 'b1')
    box(flat(panel_map, 860, 560, 11), 70, 300); box(flat(panel_chart, 760, 560, 23), 1090, 320)
    d.rectangle([56 * K, 36 * K, 800 * K, 236 * K], fill=(24, 30, 52), outline=(8, 8, 12), width=6 * K)   # ô chữ toon
    text(d, (74 * K, 52 * K), 'LAST LAMPLIGHTERS', 28 * K, LAMP)
    text(d, (72 * K, 96 * K), 'Old Town, 1890\u20131920', 64 * K, (241, 228, 198))
    text(d, (74 * K, 182 * K), 'Every era has its last lamplighters', 32 * K, (241, 228, 198))
    d.rectangle([60 * K, 960 * K, 1010 * K, 1052 * K], fill=(20, 22, 34), outline=(8, 8, 12), width=6 * K)
    text(d, (74 * K, 1006 * K), 'Then: 14 lamplighters became 1.  Now: which jobs are next?', 30 * K, (241, 228, 198), 'lm')
    d.rectangle([1500 * K, 1000 * K, 1860 * K, 1052 * K], fill=(20, 22, 34))
    text(d, (1846 * K, 1042 * K), 'Illustrative data', 30 * K, (241, 228, 198), 'rs')
    img.resize((W, H), Image.LANCZOS).save(out); print('ghi', out)

def lin(c): c = c / 255.0; return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def L(rgb): return 0.2126 * lin(rgb[0]) + 0.7152 * lin(rgb[1]) + 0.0722 * lin(rgb[2])
def ratio(a, b): la, lb = sorted([L(a), L(b)], reverse=True); return (la + 0.05) / (lb + 0.05)

def contrast(png):
    """đo tương phản THẬT trên ảnh: lấy màu nền quanh từng nhóm chữ (trung vị ô nền) so với màu chữ."""
    im = np.asarray(Image.open(png).convert('RGB'))
    def med(x0, y0, x1, y1): return tuple(int(v) for v in np.median(im[y0:y1, x0:x1].reshape(-1, 3), axis=0))
    def dark(x0, y0, x1, y1): a = im[y0:y1, x0:x1].reshape(-1, 3).astype(int); i = np.argsort(a.sum(1))[: max(1, len(a) // 200)]; return tuple(int(v) for v in np.median(a[i], axis=0))
    def light(x0, y0, x1, y1): a = im[y0:y1, x0:x1].reshape(-1, 3).astype(int); i = np.argsort(-a.sum(1))[: max(1, len(a) // 200)]; return tuple(int(v) for v in np.median(a[i], axis=0))
    rows = []
    for name, box in [('Tiêu đề (chữ sáng / nền trời)', (60, 40, 760, 220)), ('Dòng Then/Now (chữ sáng / nền mực)', (60, 960, 1010, 1052)), ('Nhãn "Illustrative data" (khung dưới phải)', (1500, 1000, 1860, 1052)),
                      ('Chữ bản đồ (mực / giấy)', (100, 330, 900, 820)), ('Chữ biểu đồ (mực / giấy)', (1110, 340, 1830, 860))]:
        x0, y0, x1, y1 = box; bgm = med(*box)
        fg = light(*box) if L(bgm) < 0.18 else dark(*box)
        rows.append((name, fg, bgm, ratio(fg, bgm)))
    for n, a, b, r in rows: print(f'{n}: chữ {a} nền {b} → {r:.1f}:1')
    print('cặp màu thiết kế: mực/giấy', f'{ratio(INK, CREAM):.1f}:1', '· kem/navy', f'{ratio((241, 228, 198), NAVY):.1f}:1')

if __name__ == '__main__':
    c = sys.argv[1] if len(sys.argv) > 1 else ''
    if c == 'panels': panels()
    elif c == 'b3': frame_b3(sys.argv[2])
    elif c == 'b1': frame_b1(sys.argv[2])
    elif c == 'panels_v2': panels_v2()
    elif c == 'b3v2': frame_b3v2(sys.argv[2])
    elif c == 'contrast': contrast(sys.argv[2])
    else: print(__doc__)
