#!/opt/cine/bin/python
"""So hai bảng k2check (--json): hàng giống hệt / khác (kết quả, giá trị, lỗi) / chỉ có ở một bên. Dùng: so_k2check.py cu.json moi.json [nhãn_cũ nhãn_mới]"""
import json, sys
a, b = json.load(open(sys.argv[1])), json.load(open(sys.argv[2])); la, lb = (sys.argv[3:5] + ['cũ', 'mới'])[:2] if len(sys.argv) > 3 else ('cũ', 'mới')
A = {r['q']: r for r in a['rows']}; B = {r['q']: r for r in b['rows']}
gi, kh = [], []
for q in list(A) + [q for q in B if q not in A]:
    x, y = A.get(q), B.get(q)
    if x is None or y is None: kh.append((q, x and x['kq'], y and y['kq'], 'chỉ có ở ' + (lb if x is None else la))); continue
    d = [k for k in ('kq', 'val', 'loi', 'sat', 'nguong', 'cap', 'chan', 'canh_bao') if x.get(k) != y.get(k)]
    if not d: gi.append(q)
    else: kh.append((q, x['kq'], y['kq'], ', '.join(d)))
print(f'giống hệt {len(gi)} hàng; khác {len(kh)} hàng')
print(f'| Hàng | {la} | {lb} | Trường khác |\n|---|---|---|---|')
for q, x, y, d in kh: print(f'| {q} | {x} | {y} | {d} |')
print('\nGiống hệt: ' + ', '.join(gi))
