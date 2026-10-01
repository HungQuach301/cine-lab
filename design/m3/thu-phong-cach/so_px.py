"""Cine Lab · M3 THỬ PHONG CÁCH — so 0 px: ảnh render bằng page.js gốc ebdacde (--page-file) và page.js nhánh này khi TẮT cờ.
/opt/cine/bin/python design/m3/thu-phong-cach/so_px.py <thư mục gốc> <thư mục cờ tắt> <tên1.png> [<tên2.png> ...]
"""
import sys
import numpy as np
from PIL import Image

a_dir, b_dir, names = sys.argv[1], sys.argv[2], sys.argv[3:]
bad = 0
for n in names:
    a = np.asarray(Image.open(f'{a_dir}/{n}')).astype(int); b = np.asarray(Image.open(f'{b_dir}/{n}')).astype(int)
    d = np.abs(a - b); k = int((d.max(2) > 0).sum()); bad += k
    print(f'{n}: {a.shape[1]}x{a.shape[0]}, điểm ảnh lệch {k}, lệch lớn nhất {int(d.max())}')
print('KẾT LUẬN:', '0 px — ĐẠT' if bad == 0 else f'LỆCH {bad} px')
