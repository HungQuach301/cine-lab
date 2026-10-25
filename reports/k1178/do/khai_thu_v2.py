#!/opt/cine/bin/python
"""K-1.17.8 — KHAI THỬ 1.17.8 trên bản sao animatic T4 v2 (ngoài channel-k2; chỉ để minh hoạ cách khai, không phải sản phẩm):
log_chu khuôn khoảng dựng từ ghep-log.json (thẻ nhân vật → the_nhan_vat, bộ đếm → bo_dem_so, khắc → chu_thich_tu_lieu), log shot: tu_lieu_lan cho
thẻ nhân vật (giờ từ ghep-log) ở shot 3D chưa khai.   khai_thu_v2.py <thư mục animatic2 bản sao>"""
import json, sys, yaml
d = sys.argv[1]; GL = json.load(open(f'{d}/ghep-log.json')); LS = json.load(open(f'{d}/log-shot.json')); key = 'shots' if isinstance(LS, dict) else None
L = LS['shots'] if key else LS
muc = [dict(t0=t, t1=t + du, role='the_nhan_vat', s=a + (' · ' + b if b else '')) for t, du, a, b, *_ in GL['the']]
muc += [dict(t0=t, t1=t + du, role='bo_dem_so', s=f'{a} {b}'.strip()) for t, du, a, b in GL['dem']]
t0s = {s['shot']: s['t0'] for s in L}
for sh, (rid, cap, a, du, kieu) in GL['khac'].items():
    if sh in t0s: muc.append(dict(t0=t0s[sh] + a, t1=t0s[sh] + a + du, role='chu_thich_tu_lieu', s=cap))
json.dump(dict(fmt='khoang', muc=muc), open(f'{d}/log-chu-khoang.json', 'w'), ensure_ascii=False, indent=1)
n = 0
for s in L:
    if (s.get('lop') or {}).get('THE') and not s.get('tu_lieu_lan'):
        w = [dict(t0=t, t1=t + du, lop='THE') for t, du, *_ in GL['the'] if s['t0'] - 1e-6 <= t < s['t1']]
        if w: s['tu_lieu_lan'] = w; n += 1
json.dump(LS, open(f'{d}/log-shot.json', 'w'), ensure_ascii=False, indent=1)
E = open(f'{d}/episode.yaml').read().rstrip('\n') + '\nlog_chu: log-chu-khoang.json\n'
open(f'{d}/episode.yaml', 'w').write(E); yaml.safe_load(open(f'{d}/episode.yaml'))
print(len(muc), 'mục log chữ ·', n, 'shot thêm tu_lieu_lan (THE)')
