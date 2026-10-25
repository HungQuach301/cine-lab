#!/opt/cine/bin/python
"""ANIMATIC-T4 · L3 (chủ dự án 23/10/2026 23:27, "người/xe/thuyền nhỏ thêm ở sản xuất cho khung trung ≤ 60 m"): đoạn phố cho lớp người/xe của look2.js.
Lấy tim đường OSM 2026 (highway chính + phụ, bỏ đường sắt/lối trong nhà) trong bán kính 900 m quanh các máy thấp (P4 Fleet Street, P4b Ludgate Hill, P6 sông) → $LDN_DATA/look2/dan.json
[{x0, z0, x1, z1, w (bề rộng làn ước), ten}] (toạ độ cảnh). Bậc 5 (minh hoạ đời sống chung: số lượng/vị trí ước lượng, không mang dữ kiện); kiểu người/xe theo năm do look2.js chọn."""
import json, math, os
D = os.environ.get('LDN_DATA', '/var/tmp/ldn'); R = json.load(open(os.path.join(D, 'vec/osm2026.json')))
TAM = [(531300, 181160), (531640, 181150), (533250, 180480)]; RMAX = 900
OK = {'primary': 7, 'secondary': 6, 'tertiary': 5, 'unclassified': 4, 'residential': 4, 'service': 3, 'pedestrian': 4, 'living_street': 4, 'trunk': 8, 'footway': 2}
out = []
for w in R['duong']:
    hw = w.get('hw'); 
    if hw not in OK or w.get('bridge') == 'viaduct': continue
    for (a, b) in zip(w['l'], w['l'][1:]):
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        if min(math.hypot(mx - x, my - y) for x, y in TAM) > RMAX: continue
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if L < 4: continue
        out.append({'x0': round(a[0] - 532000, 1), 'z0': round(-(a[1] - 180800), 1), 'x1': round(b[0] - 532000, 1), 'z1': round(-(b[1] - 180800), 1), 'w': OK[hw], 'ten': w.get('name', '')})
json.dump(out, open(os.path.join(D, 'look2/dan.json'), 'w'))
print('đoạn phố', len(out), 'tổng m', round(sum(math.hypot(s['x1'] - s['x0'], s['z1'] - s['z0']) for s in out)))
