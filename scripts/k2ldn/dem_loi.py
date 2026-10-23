#!/opt/cine/bin/python
"""Đếm từ lời nháp: chỉ các dòng **Lnn** (bỏ chú thích '>'), theo phần; ước thời lượng ở 145 từ/phút. dem_loi.py <LOI.md> <ra.json>"""
import json, re, sys
cur, parts, lines = None, {}, []
for ln in open(sys.argv[1], encoding='utf-8'):
    if ln.startswith('## ') and ('MÓC' in ln or 'HỒI' in ln): cur = ln[3:].split('(')[0].strip(); parts[cur] = 0
    m = re.match(r'\*\*(L\d+)\*\*\s+(.*)', ln)
    if m and cur:
        t = re.sub(r'⟦[^⟧]*⟧', '', m.group(2)); n = len(re.findall(r"[A-Za-z0-9’'-]+", t)); parts[cur] += n; lines.append({'id': m.group(1), 'phan': cur, 'tu': n, 'cau': t.strip()})
tot = sum(parts.values())
out = {'tong_tu': tot, 'phut_o_145': round(tot / 145, 2), 'theo_phan': parts, 'dong': lines}
json.dump(out, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1); print(tot, parts, out['phut_o_145'])
