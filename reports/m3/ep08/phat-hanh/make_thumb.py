#!/opt/cine/bin/python
"""Thumbnail tập 8 (1280×720) từ khung cảnh đinh 1080p, dựng bằng scripts/ll/thumb.py (lề an toàn 5 %).
python make_thumb.py <thư mục ra> <khung T1> <khung T2>   (T1 = booth_in: buồng phiên dịch, tai nghe, đèn cảnh báo; T2 = st_screen: màn hình duyệt bản nháp máy)"""
import sys
sys.path.insert(0, __file__.rsplit('/reports/', 1)[0] + '/scripts/ll')
from PIL import Image
import thumb
D, f1, f2 = sys.argv[1:4]
CREAM, AMB = (236, 223, 190), (232, 160, 80)
thumb.make(Image.open(f1), [('FROM HEADPHONES', 66, CREAM, 'serif'), ('TO MACHINE DRAFTS', 66, CREAM, 'serif'), ("HOW TRANSLATORS' WORK CHANGED", 42, AMB, 'serif')], f'{D}/ll-ep08-thumb-T1.jpg')
thumb.make(Image.open(f2), [('1954: "A FEW YEARS"', 58, CREAM, 'serif'), ('IT TOOK MORE THAN FIFTY', 46, AMB, 'sans')], f'{D}/ll-ep08-thumb-T2.jpg', align='center')
print('ok')
