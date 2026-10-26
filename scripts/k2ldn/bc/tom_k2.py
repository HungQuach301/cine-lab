#!/opt/cine/bin/python
"""BAN-CUOI-T4-A · tóm bảng k2check.md: in hàng chọn (kết quả + 'lỗi Chặn n, Cảnh báo m' + giá trị).  tom_k2.py <k2check.md> [hàng …]"""
import re, sys
p = sys.argv[1]; chon = sys.argv[2:] or ['N2P-1', 'N2P-2', 'N2P-3', 'N2P-4', 'N2P-5', 'N2P-E', 'BE-MAT-NHA']
for l in open(p, encoding='utf-8'):
    c = [x.strip() for x in l.split('|')]
    if len(c) > 5 and c[1] in chon:
        m = re.search(r'lỗi Chặn (\d+), Cảnh báo (\d+)', c[4]); print(f"{c[1]:<12} {c[3]:<16} Chặn {m.group(1) if m else '?'} · CB {m.group(2) if m else '?'} · {c[5][:220]}")
