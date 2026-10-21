#!/opt/cine/bin/python
"""K-1.17 · so hai lượt k2check (--json) theo hàng: kq, val, loi, sat, cap, chan, canh_bao. so_k2check.py <cũ.json> <mới.json> <nhãn>"""
import json, sys
A = {r['q']: r for r in json.load(open(sys.argv[1]))['rows']}; B = {r['q']: r for r in json.load(open(sys.argv[2]))['rows']}
K = ('kq', 'val', 'loi', 'sat', 'cap', 'chan', 'canh_bao')
same = [q for q in A if q in B and all(A[q].get(k) == B[q].get(k) for k in K)]
diff = [q for q in A if q in B and q not in same]
print(f"{sys.argv[3]}: {len(A)} hàng cũ / {len(B)} hàng mới · giống hệt {len(same)} · khác {diff} · chỉ ở mới {[q for q in B if q not in A]} · chỉ ở cũ {[q for q in A if q not in B]}"
      + ''.join(f" · {q}: {A[q]['kq']} {A[q]['ten']!r} → {B[q]['kq']} {B[q]['ten']!r}" for q in diff))
