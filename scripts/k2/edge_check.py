#!/opt/cine/bin/python
"""KÊNH 2 · kiểm máy vùng an toàn chữ (lệnh chủ dự án 13/10/2026): mọi hộp chữ (log render.js, `text[].items[].box`, toạ độ 1920×1080)
phải cách mọi mép khung ≥ MARGIN px (mặc định 48). In số khung vi phạm + mẫu; mã thoát 1 nếu có vi phạm.
  edge_check.py <seg.mkv.log.json> [...] [--margin 48]"""
import json, sys
a = sys.argv[1:]; M = int(a[a.index('--margin') + 1]) if '--margin' in a else 48; files = [x for x in a if x.endswith('.json')]
bad_all = 0
for fn in files:
    L = json.load(open(fn)); W, H = (1080, 1920) if L.get('fmt') == '9x16' else (1920, 1080); n = 0; bad = []; mn = 1e9
    for e in L.get('text', []):
        for it in e['items']:
            x0, y0, x1, y1 = it['box']; d = min(x0, y0, W - x1, H - y1); n += 1; mn = min(mn, d)
            if d < M: bad.append((e['f'], it['s'], d))
    frames = len(set(b[0] for b in bad)); bad_all += len(bad)
    print(f'{fn}: {n} hộp chữ, mép gần nhất {mn:.0f} px, vi phạm < {M} px: {len(bad)} hộp / {frames} khung' + ('' if not bad else ' · mẫu: ' + '; '.join(f'f{f} "{s}" {d:.0f}px' for f, s, d in bad[:5])))
sys.exit(1 if bad_all else 0)
