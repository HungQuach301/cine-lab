#!/opt/cine/bin/python
"""ANIMATIC-T3 · tải lại 18 vân Poly Haven CC0 của cách A (danh sách + SHA trong reports/nc-cpu/RIGHTS-NC.md) vào $K2TL_CACHE/nc/tex/
(bộ đệm ngoài git của V7C/NC-CPU đã mất theo container). Đặt tên như up.js đọc: <id>_diff_<r>.jpg, <id>_nor_<r>.jpg (nor = nor_gl hoặc nor_dx — chọn bản
khớp SHA ghi ở RIGHTS-NC; không khớp bản nào → dừng). User-Agent không email.
  anim_tex.py"""
import hashlib, json, os, re, sys, urllib.request
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(os.environ.get('K2TL_CACHE', '/var/tmp/cine-out/k2tl-cache'), 'nc', 'tex'); os.makedirs(OUT, exist_ok=True)
UA = 'CineLab-research (+https://github.com/HungQuach301/cine-lab)'
def get(u): return urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA}), timeout=120).read()
R = open(os.path.join(REPO, 'reports/nc-cpu/RIGHTS-NC.md')).read()
SHA = dict(re.findall(r'`([a-z0-9_]+_(?:diff|nor)_[12]k\.jpg)` ([0-9a-f]{12})', R))
n = 0
for f, h in sorted(SHA.items()):
    p = os.path.join(OUT, f)
    if os.path.exists(p) and hashlib.sha256(open(p, 'rb').read()).hexdigest()[:12] == h: n += 1; continue
    m = re.match(r'(.+)_(diff|nor)_([12]k)\.jpg', f); aid, kind, r = m.groups(); F = json.loads(get(f'https://api.polyhaven.com/files/{aid}'))
    for key in (['Diffuse'] if kind == 'diff' else ['nor_gl', 'nor_dx']):
        b = get(F[key][r]['jpg']['url'])
        if hashlib.sha256(b).hexdigest()[:12] == h: open(p, 'wb').write(b); n += 1; print(f, key, 'KHỚP', flush=True); break
    else: sys.exit(f'LỖI: {f} không khớp SHA {h}')
print(f'VAN-XONG {n}/{len(SHA)}')
