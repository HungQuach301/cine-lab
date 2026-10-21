#!/usr/bin/env python3
"""P-2010 · kiểm mọi câu trích trong THUC-VAT-1782.md khớp nguyên văn tệp nguồn (chuẩn hoá khoảng trắng; mỗi đoạn tách bởi " … " / " / ")."""
import re, sys
D = '/var/tmp/cine-out/p2010/nguon/'; SRC = {'Drinkwater 1786': 'drin1786.txt', 'Spilsbury': 'spil.txt', 'Ancell 1784': 'ancell.txt'}
norm = lambda t: re.sub(r'\s+', ' ', t).strip()
txt = {k: norm(open(D + v, encoding='utf-8', errors='replace').read()) for k, v in SRC.items()}
bad = ok = 0
for l in open(sys.argv[1], encoding='utf-8'):
    m = re.match(r'\| (\d+) \| ([^|]+?) \|[^|]*\| "(.+?)" \|', l)
    if not m: continue
    src = next(k for k in SRC if m.group(2).startswith(k))
    for part in re.split(r' … | / ', m.group(3)):
        if norm(part) in txt[src]: ok += 1
        else: bad += 1; print('LỆCH', m.group(1), src, part[:70])
print(f'khớp {ok}, lệch {bad}'); sys.exit(1 if bad else 0)
