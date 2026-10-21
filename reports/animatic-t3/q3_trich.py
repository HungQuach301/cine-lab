#!/opt/cine/bin/python
"""ANIMATIC-T3 việc 6 · Q3 "vì sao đói": trích NGUYÊN VĂN (OCR giữ chính tả) từ 3 nguồn đã đăng ký SHA (claims-vay-ham.json / reports/p2010/THUC-VAT-1782.md),
kiểm bằng máy: SHA-256 tệp = đăng ký, mỗi đoạn trích = nối các dòng OCR [a, b] (chuẩn hoá khoảng trắng) và có trong tệp. Ra q3-trich.json.
  q3_trich.py <thư mục chứa *_djvu.txt tải lại (tên = id archive.org + .txt)>"""
import hashlib, json, re, sys, os
D = sys.argv[1]
SRC = {'drinkwater1786': ('historyoflatesie00driniala', '7576bb8fb645db341cbf981383d7d41efae91fce1c9991737e21be4d04565212'),
       'spilsbury': ('ajournalsiegegi00spilgoog', 'f6c2f3a940cde7ac88eb6745421b458f1f8c764c4a8affef42a784c54699dc1f'),
       'ancell1784': ('acircumstantial00ancegoog', '67d61d0aced585978cd08b34717ca985699b3dc7e32d01014f974d1fe488b526')}
T = [  # nguồn, dòng OCR đầu–cuối, trang (theo đầu trang chạy OCR), ngày, ý
 ('drinkwater1786', 5200, 5208, 'tr. 107', '1/1780', 'bánh mì hạn mức, có lính gác nơi phát; người yếu nhiều ngày không có bánh'),
 ('drinkwater1786', 5220, 5233, 'tr. 108', '1/1780', 'ăn cây kế, bồ công anh, tỏi dại; ít hàng từ Barbary, không thấy cứu viện → nạn đói'),
 ('drinkwater1786', 5235, 5251, 'tr. 108', '1/1780', 'giá thịt, gà, vịt, củi, sữa, bắp cải'),
 ('drinkwater1786', 5254, 5255, 'tr. 109', '1/1780', 'trứng sáu xu một quả'),
 ('ancell1784', 2758, 2772, 'trang OCR không đọc được (dấu "( H )"), thư 9/9/1780', '9/1780', 'không nhận con bò nào từ Barbary từ 12/6 → mọi thứ giá cắt cổ'),
 ('ancell1784', 2741, 2753, 'trang OCR không đọc được (dấu "( H )"), thư 9/9/1780', '9/1780', 'phong toả cảng chặt hơn bao giờ hết'),
 ('spilsbury', 884, 887, 'trang không xác định trong OCR (bản 1908), mục ngày 27, sau mục "22nd October" (dòng 866)', '27/10/1779', 'gạo gấp năm lần giá thường; ít thịt tươi'),
 ('spilsbury', 7429, 7430, 'tr. 121 (bảng phụ lục)', 'phụ lục', 'bảng khẩu phần một người lính 7–28 ngày'),
]
out = dict(ghi=__doc__.splitlines()[0], nguon={}, trich=[])
txt = {}
for k, (fid, sha) in SRC.items():
    p = os.path.join(D, fid + '.txt'); b = open(p, 'rb').read(); h = hashlib.sha256(b).hexdigest()
    out['nguon'][k] = dict(archive_id=fid, url=f'https://archive.org/download/{fid}/{fid}_djvu.txt', sha256=h, khop_dang_ky=h == sha); txt[k] = b.decode('utf-8', 'replace').splitlines()
ok = 0
for k, a, b, tr, ngay, y in T:
    s = re.sub(r'\s+', ' ', ' '.join(txt[k][a - 1:b])).strip(); full = re.sub(r'\s+', ' ', ' '.join(txt[k]))
    khop = s in full and out['nguon'][k]['khop_dang_ky']; ok += khop
    out['trich'].append(dict(nguon=k, dong=[a, b], trang=tr, ngay=ngay, y=y, trich=s, khop=khop))
out['kiem'] = f'{ok}/{len(T)} đoạn khớp nguyên văn tệp có SHA đăng ký'
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'q3-trich.json'), 'w'), ensure_ascii=False, indent=1); print(out['kiem'])
for t in out['trich']: print(t['nguon'], t['dong'], t['trang'], '|', t['trich'][:160])
