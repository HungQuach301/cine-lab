#!/opt/cine/bin/python
"""Thumbnail tập 5 (1280×720) từ khung trung gian, dựng bằng scripts/ll/thumb.py (lề an toàn 5 %).
python make_thumb.py <thư mục ra> <khung T1 .png> <khung T2 .png>   (khung lấy từ trung gian trước khi xoá: 11 cảnh quầy; 12 thẻ so sánh)"""
import sys
sys.path.insert(0, __file__.rsplit('/reports/', 1)[0] + '/scripts/ll')
from PIL import Image
import thumb
D, f1, f2 = sys.argv[1:4]
CREAM, AMB = (236, 223, 190), (232, 160, 80)
thumb.make(Image.open(f1), [('IN 1966, COMPUTERS COULDN\'T', 56, CREAM, 'serif'), ('JUDGE AN INSURANCE CLAIM.', 56, CREAM, 'serif'), ('NOW SOFTWARE PRICES THE WRECK', 60, AMB, 'serif')], f'{D}/ll-ep05-thumb-T1.jpg')
thumb.make(Image.open(f2), [('AUTO DAMAGE APPRAISERS −9% BY 2035', 56, CREAM, 'serif'), ('BLS PROJECTION', 40, AMB, 'sans')], f'{D}/ll-ep05-thumb-T2.jpg', align='center')
print('ok')
