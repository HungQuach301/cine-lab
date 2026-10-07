#!/opt/cine/bin/python
"""Thumbnail tập 6 (1280×720) từ khung trung gian, dựng bằng scripts/ll/thumb.py (lề an toàn 5 %).
python make_thumb.py <thư mục ra> <khung T1> <khung T2>   (v2: T1 = cảnh đinh shop_hook khung 280 — ô cửa người vẽ, cùng khung móc câu 0:00; T2 = wall_push khung 420 — tường bản nháp)"""
import sys
sys.path.insert(0, __file__.rsplit('/reports/', 1)[0] + '/scripts/ll')
from PIL import Image
import thumb
D, f1, f2 = sys.argv[1:4]
CREAM, AMB = (236, 223, 190), (232, 160, 80)
thumb.make(Image.open(f1), [('THE COMPUTER REPLACED THE TYPESETTER', 52, CREAM, 'serif'), ('AND MADE THE DESIGNER.', 52, CREAM, 'serif'), ('NOW AI CAN DRAW', 64, AMB, 'serif')], f'{D}/ll-ep06-thumb-T1.jpg')
thumb.make(Image.open(f2), [('GRAPHIC DESIGNERS: −1.7% PROJECTED, 2025–35', 50, CREAM, 'serif'), ('BLS: AI "REDUCE THE NEED"', 40, AMB, 'sans')], f'{D}/ll-ep06-thumb-T2.jpg', align='center')
print('ok')
