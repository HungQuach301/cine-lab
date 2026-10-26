#!/opt/cine/bin/python
"""K-1.17.9 · so hai bảng k2check (.md) → hàng đổi (kết quả hoặc 'lỗi Chặn n, Cảnh báo m' hoặc giá trị).  so_bang.py <cũ.md> <mới.md> [--gia-tri]"""
import re, sys


def doc(p):
    R = {}
    for l in open(p):
        if not l.startswith('| ') or l.startswith('| Mục') or l.startswith('|---'): continue
        c = [x.strip() for x in l.strip().strip('|').split('|')]
        if len(c) < 5: continue
        q = re.sub(r'\b1\.17\.[89]\b', '1.17.x', c[0]); m = re.search(r'lỗi Chặn (\d+), Cảnh báo (\d+)', c[3])
        R[q] = dict(kq=c[2].strip('*'), cb=(m.group(1), m.group(2)) if m else None, val=c[4])
    return R


A, B = doc(sys.argv[1]), doc(sys.argv[2]); gv = '--gia-tri' in sys.argv; n = 0
for q in list(A) + [x for x in B if x not in A]:
    a, b = A.get(q), B.get(q)
    if a is None or b is None: print(f'| {q} | {a and a["kq"]} | {b and b["kq"]} | hàng {"mới" if a is None else "bỏ"} |'); n += 1; continue
    if a['kq'] != b['kq'] or a['cb'] != b['cb'] or (gv and a['val'] != b['val']):
        print(f"| {q} | {a['kq']} {a['cb'] or ''} | {b['kq']} {b['cb'] or ''} | {b['val'][:160] if a['val'] != b['val'] else '(giá trị như cũ)'} |"); n += 1
print(f'<!-- {n} hàng đổi / {len(B)} hàng -->')
