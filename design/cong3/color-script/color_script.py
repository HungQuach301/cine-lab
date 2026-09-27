"""Color script "Last Round" — dải 6 ô cho 6 cảnh, theo bible/world-rules.md v0.2 mục 5.
Vẽ 2D bằng numpy ở không gian tuyến tính, dither TPDF trước khi lượng tử 8 bit (không banding).
Mỗi ô là bố cục giản lược (thumbnail màu), không phải khung phim. Dưới mỗi ô: tên cảnh, thời lượng, màu chủ đạo, cảm xúc.
Chạy: /opt/cine/bin/python design/cong3/color-script/color_script.py"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 640, 360
rng = np.random.default_rng(7)
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def lin(hexc):
    c = np.array([int(hexc[i:i + 2], 16) for i in (1, 3, 5)]) / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)

def to_srgb8(img):
    c = np.clip(img, 0, 1); s = np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055)
    s = s * 255 + (rng.random(s.shape[:2])[..., None] - rng.random(s.shape[:2])[..., None])  # dither TPDF ±1 LSB
    return np.clip(np.round(s), 0, 255).astype(np.uint8)

yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)

def vgrad(stops):
    """stops: [(t, hex)] theo chiều dọc 0 (trên) → 1 (dưới)."""
    t = yy / (H - 1); out = np.zeros((H, W, 3), np.float32)
    ts = [s[0] for s in stops]; cs = [lin(s[1]) for s in stops]
    for k in range(3): out[..., k] = np.interp(t, ts, [c[k] for c in cs])
    return out

def glow(img, cx, cy, r, hexc, gain=1.0):
    d2 = ((xx - cx) ** 2 + (yy - cy) ** 2) / (r * r)
    img += (np.exp(-d2 * 2.2) * gain)[..., None] * lin(hexc)

def rect(img, x0, y0, x1, y1, hexc, a=1.0):
    img[int(y0):int(y1), int(x0):int(x1)] = img[int(y0):int(y1), int(x0):int(x1)] * (1 - a) + lin(hexc) * a

def roofline(img, base, hexc, seed, hmin=30, hmax=90, wmin=40, wmax=90):
    r = np.random.default_rng(seed); x = -20
    while x < W:
        w = r.integers(wmin, wmax); h = r.integers(hmin, hmax)
        rect(img, x, base - h, x + w, H, hexc)
        peak = np.clip((w / 2 - np.abs(xx - (x + w / 2))) * 0.7, 0, None)
        m = (yy > base - h - peak) & (yy <= base - h) & (xx >= x) & (xx < x + w); img[m] = lin(hexc)
        if r.random() < 0.6: rect(img, x + w * 0.7, base - h - peak.max() * 0.6 - 18, x + w * 0.7 + 8, base - h, hexc)
        x += w + r.integers(0, 10)

def figure(img, x, y, s, hexc):
    """Hình người giản lược (đầu + thân + mũ) cao s px, chân tại (x, y)."""
    rect(img, x - s * 0.12, y - s * 0.78, x + s * 0.12, y, hexc)
    d2 = ((xx - x) ** 2 + (yy - (y - s * 0.87)) ** 2); img[d2 < (s * 0.09) ** 2] = lin(hexc)

def panel1():  # The Round — trời xanh cuối chạng vạng, tâm hổ phách, nhịp sáng–tối
    img = vgrad([(0, '#3a3a6e'), (0.45, '#6d4c7d'), (0.7, '#c77a86'), (1, '#e3a28a')])
    roofline(img, 200, '#2a2238', 1, 20, 60)
    rect(img, 0, 200, W, H, '#231c2c')
    for k, (x, y) in enumerate([(90, 330), (190, 300), (280, 276), (360, 256), (430, 240), (490, 228), (540, 219)]):
        if k < 4: glow(img, x, y, 70 - k * 8, '#ffae55', 0.9); glow(img, x, y - 20, 10, '#fff0c0', 1.5)
        else: rect(img, x - 2, y - 30, x + 2, y, '#141018')
    figure(img, 215, 305, 40, '#15111a')
    return img

def panel2():  # Switch-on — sóng trắng lạnh lấn từ nền về tiền cảnh; đồng hồ sáng trước
    img = vgrad([(0, '#2c2c52'), (0.5, '#4d3f66'), (1, '#6b5470')])
    roofline(img, 190, '#262035', 2, 20, 60)
    rect(img, 0, 190, W, H, '#241d2c')
    wave = np.clip((330 - yy) / 140 - (xx - 300) / 900, 0, 1) ** 1.5
    img += (wave * 0.75)[..., None] * lin('#dde7f0') * ((yy > 150)[..., None])
    glow(img, 520, 120, 26, '#f2f6ff', 1.6); d2 = ((xx - 520) ** 2 + (yy - 120) ** 2); img[d2 < 14 ** 2] = lin('#f4f8ff')
    for x, y in [(100, 330), (200, 300)]: glow(img, x, y, 60, '#ffae55', 0.7)
    figure(img, 150, 318, 44, '#15111a')
    return img

def panel3():  # The Race — xen kẽ hổ phách vừa thắp → trắng phủ; nhịp nhanh
    img = vgrad([(0, '#2b2b4f'), (1, '#4a3e5c')])
    roofline(img, 170, '#241e32', 3, 20, 50)
    rect(img, 0, 170, W, H, '#cfd8e0', 1.0)
    for k, x in enumerate(range(40, W, 110)):
        warm = k % 2 == 1
        if warm: glow(img, x, 280, 70, '#ffa24a', 0.8)
        rect(img, x - 2, 200, x + 2, 300, '#2a2630')
    rect(img, 0, 170, W, H, '#b9c6d2', 0.25)
    figure(img, 380, 300, 50, '#1c1822')
    return img

def panel4():  # The Wall — tường trắng phẳng; một quầng hổ phách nhỏ quanh đèn lồng; chim bóng
    img = vgrad([(0, '#dfe6ec'), (1, '#c9d2da')])
    rect(img, 0, 250, W, H, '#b7c0c8')
    glow(img, 300, 250, 110, '#ffb160', 1.0); glow(img, 300, 262, 12, '#fff2c6', 2.0)
    bird = ((np.abs(xx - 330) < 70) & (np.abs(yy - 150 + 0.45 * np.abs(xx - 330)) < 9)) | (((xx - 330) ** 2 + (yy - 140) ** 2) < 12 ** 2)
    img[bird] = img[bird] * 0.35 + lin('#8a6a58') * 0.2
    figure(img, 360, 330, 90, '#3a2e30'); figure(img, 250, 335, 70, '#2f3438')
    return img

def panel5():  # The Last Lamp — hốc cửa tối ấm, hai bóng người trên vách vôi; ngoài vòm phố trắng
    img = np.zeros((H, W, 3), np.float32) + lin('#dfe7ee') * 0.9
    rect(img, 120, 20, 520, H, '#3a261c')
    glow(img, 320, 330, 260, '#ffb46a', 0.9)
    for (x, s) in [(260, 240), (380, 170)]:  # hai bóng vươn cao trên vách
        m = (np.abs(xx - x) < s * 0.16) & (yy > 330 - s) & (yy < 330)
        img[m] *= 0.45
        d2 = (xx - x) ** 2 + (yy - (330 - s - s * 0.1)) ** 2; img[d2 < (s * 0.11) ** 2] *= 0.45
    figure(img, 270, 345, 120, '#1a1214'); figure(img, 370, 345, 90, '#1a1214')
    glow(img, 320, 352, 14, '#fff0c0', 2.5)
    arch = ((xx - 320) ** 2 / 200 ** 2 + (yy - 20) ** 2 / 60 ** 2 < 1) & (yy < 20)
    img[arch] = lin('#3a261c')
    return img

def panel6():  # The Window — thành phố trắng, một ô vàng | phòng: hổ phách trọn khung, chim bóng lớn
    img = np.zeros((H, W, 3), np.float32) + lin('#d9e2ea')
    for gx in range(0, 380, 38):
        for gy in range(20, H, 34): rect(img, gx + 4, gy, gx + 30, gy + 24, '#c3ced8')
    rect(img, 194, 157, 216, 177, '#ffb04c'); glow(img, 205, 167, 30, '#ffaa50', 0.7)
    room = np.zeros((H, 260, 3), np.float32)
    ry, rx = np.mgrid[0:H, 0:260]
    room += lin('#6a3a22') + (np.exp(-(((rx - 40) ** 2 + (ry - 250) ** 2) / 160 ** 2) * 1.5))[..., None] * lin('#ffb870')
    bird = (np.abs(ry - 140 + 0.5 * np.abs(rx - 150)) < 14) & (np.abs(rx - 150) < 95) | (((rx - 150) ** 2 + (ry - 128) ** 2) < 17 ** 2)
    room[bird] *= 0.4
    img[:, 380:] = room
    rect(img, 378, 0, 382, H, '#1a1214')
    return img

PANELS = [
    ('1 · The Round', '0:00–0:26', 'Tím chạng vạng + hổ phách; nhịp sáng–tối', 'Êm, trìu mến', panel1, ['#3a3a6e', '#c77a86', '#ffae55', '#231c2c']),
    ('2 · Switch-on', '0:26–0:44', 'Trắng lạnh lấn dần nền → tiền cảnh', 'Hụt hẫng', panel2, ['#2c2c52', '#dde7f0', '#f4f8ff', '#ffae55']),
    ('3 · The Race', '0:44–1:08', 'Xen kẽ hổ phách vừa thắp → trắng phủ', 'Căng, thương', panel3, ['#cfd8e0', '#ffa24a', '#2b2b4f', '#1c1822']),
    ('4 · The Wall', '1:08–1:34', 'Trắng phẳng; một quầng hổ phách nhỏ', 'Đau nhói → ấm', panel4, ['#dfe6ec', '#ffb160', '#3a2e30', '#b7c0c8']),
    ('5 · The Last Lamp', '1:34–2:10', 'Hốc tối ấm, hai bóng trên vách; ngoài vòm trắng', 'Nghẹn → an', panel5, ['#3a261c', '#ffb46a', '#dfe7ee', '#1a1214']),
    ('6 · The Window', '2:10–2:30', 'Toàn trắng, một ô vàng; phòng hổ phách', 'Ấm, hy vọng', panel6, ['#d9e2ea', '#ffb04c', '#6a3a22', '#ffb870']),
]

def main():
    pad, lab = 16, 150
    sheet = Image.new('RGB', (pad + len(PANELS) * (W + pad), 70 + H + lab), (238, 233, 225)); d = ImageDraw.Draw(sheet)
    d.text((pad, 16), 'COLOR SCRIPT — "Last Round" · 6 cảnh · theo luật thế giới v0.2 mục 5 · Cổng 3 vòng 1 (đề xuất, chưa duyệt)', font=ImageFont.truetype(FB, 28), fill=(40, 36, 34))
    for k, (name, t, dom, emo, fn, sw) in enumerate(PANELS):
        x = pad + k * (W + pad); tile = Image.fromarray(to_srgb8(fn())); sheet.paste(tile, (x, 70))
        tile.save(os.path.join(HERE, f'cs-{k + 1}.png'))
        y = 70 + H + 10
        d.text((x, y), f'{name}  ({t})', font=ImageFont.truetype(FB, 22), fill=(40, 36, 34))
        d.text((x, y + 32), dom, font=ImageFont.truetype(F, 17), fill=(60, 55, 52))
        d.text((x, y + 56), 'Cảm xúc: ' + emo, font=ImageFont.truetype(F, 17), fill=(60, 55, 52))
        for j, c in enumerate(sw):
            d.rectangle((x + j * 110, y + 88, x + j * 110 + 40, y + 118), fill=c, outline=(80, 80, 80)); d.text((x + j * 110 + 46, y + 96), c, font=ImageFont.truetype(F, 14), fill=(70, 70, 70))
    sheet.save(os.path.join(HERE, 'COLOR-SCRIPT.png'), optimize=True)

if __name__ == '__main__':
    main()
