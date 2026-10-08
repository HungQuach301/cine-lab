#!/opt/cine/bin/python
"""Thumbnail tập 7 (1280×720) từ khung cảnh đinh 1080p, dựng bằng scripts/ll/thumb.py (lề an toàn 5 %). Không dùng ảnh người thật của NASA.
python make_thumb.py <thư mục ra> <khung T1> <khung T2>   (T1 = air_light sau khi đèn bàn sau kính bừng — dải cửa sổ phòng tính toán; T2 = tower_code sau khi dòng mã được đánh dấu)"""
import sys
sys.path.insert(0, __file__.rsplit('/reports/', 1)[0] + '/scripts/ll')
from PIL import Image
import thumb
D, f1, f2 = sys.argv[1:4]
CREAM, AMB = (236, 223, 190), (232, 160, 80)
thumb.make(Image.open(f1), [('WHEN COMPUTERS', 66, CREAM, 'serif'), ('WERE PEOPLE', 66, CREAM, 'serif'), ('ONE WORD, THREE JOBS', 46, AMB, 'serif')], f'{D}/ll-ep07-thumb-T1.jpg')
thumb.make(Image.open(f2), [('SOFTWARE DEVELOPERS: +10.2% PROJECTED, 2025–35', 46, CREAM, 'serif'), ('PROGRAMMERS: PROJECTED TO SHRINK', 42, AMB, 'sans')], f'{D}/ll-ep07-thumb-T2.jpg', align='center')
print('ok')
