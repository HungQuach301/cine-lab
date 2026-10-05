#!/opt/cine/bin/python
"""Thumbnail tập 2 (1280×720) từ khung trung gian, dựng bằng scripts/ll/thumb.py (lề an toàn 5 %).
python make_thumb.py <thư mục ra> <khung T1 .png> <khung T2 .png>   (khung lấy từ trung gian trước khi xoá: 00 @4,0 s; 11 @40,0 s)"""
import sys
sys.path.insert(0, __file__.rsplit('/reports/', 1)[0] + '/scripts/ll')
from PIL import Image
import thumb
D, f1, f2 = sys.argv[1:4]
CREAM, AMB = (236, 223, 190), (232, 160, 80)
thumb.make(Image.open(f1), [('AUTOMATION HURT THE OPERATORS.', 56, CREAM, 'serif'), ('NOT THE NEXT GENERATION.', 56, CREAM, 'serif'), ('WHAT ABOUT US?', 72, AMB, 'serif')], f'{D}/ll-ep02-thumb-T1.jpg')
thumb.make(Image.open(f2), [('THEN −16%  ·  NEXT −5%?', 66, CREAM, 'serif')], f'{D}/ll-ep02-thumb-T2.jpg', align='center')
print('ok')
