"""Cine Lab · M2.0 — đo phân dải (banding) TRÊN CHÍNH DẢI JPEG.
Trong vùng mịn (độ dốc luma cục bộ ≤ 3 mã sau nhoè 9 px), đo độ dài trung bình các đoạn ngang có luma 8 bit giống hệt nhau và tỉ lệ điểm ảnh
nằm trong đoạn ≥ 24 px. Phân dải = các "bậc" phẳng dài; grain/dither đủ = đoạn ngắn. Số càng nhỏ càng ít phân dải.
/opt/cine/bin/python design/m3/thu-phong-cach/phan_dai.py <dải1.jpg> [<dải2.jpg> ...]
"""
import sys
import numpy as np
from PIL import Image, ImageFilter
for p in sys.argv[1:]:
    im = Image.open(p).convert('L'); a = np.asarray(im).astype(np.int16); s = np.asarray(im.filter(ImageFilter.BoxBlur(4))).astype(np.int16)
    smooth = (np.abs(np.diff(s, axis=1, prepend=s[:, :1])) <= 1) & (np.abs(np.diff(s, axis=0, prepend=s[:1])) <= 1) & (a > 30) & (a < 250)   # bỏ viền lưới (24) và nhãn đen của dải
    runs, longpx, tot = [], 0, 0
    for y in range(a.shape[0]):
        row, m = a[y], smooth[y]; x = 0
        while x < len(row):
            if not m[x]: x += 1; continue
            x0 = x
            while x + 1 < len(row) and m[x + 1] and row[x + 1] == row[x0]: x += 1
            L = x - x0 + 1; runs.append(L); tot += L; longpx += L if L >= 24 else 0; x += 1
    print(f'{p}: vùng mịn {smooth.mean()*100:.0f} % · đoạn luma phẳng TB {np.mean(runs):.2f} px · điểm ảnh trong đoạn ≥ 24 px {100*longpx/max(tot,1):.2f} %')
