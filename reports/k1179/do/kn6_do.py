#!/opt/cine/bin/python
"""K-1.17.9 · KN-6 — số đo do_day_2d trên video tổng hợp từ tấm E-P9-ngay-l1-thap THẬT (fixture 640×360): đẩy cả khung 1,0 / 1,5 / 3,0 %/s;
lớp (a)-E theo tốc độ khác nền (0 / 0,8 / 0,9 so 1,0 %/s — giả lập (a)-E dựng 3D khác quỹ đạo). → do/kn6-day2d.json"""
import json, os, sys
__file__ = '/home/user/cine-lab/checks/ll/selftest_k1179.py'; sys.argv = [__file__]
src = open(__file__).read()
exec(src.split('# ====================================================================== KN-1')[0]); exec(src[src.index('def vid('):src.index('VD = lambda')])
g9, _ = ghep('p9'); out = {}
for ten, a in (('day_1.0', (1.0, None)), ('day_1.5', (1.5, None)), ('day_3.0', (3.0, None)), ('lech_1.0_vs_0', (1.0, 0.0)), ('lech_1.0_vs_0.8', (1.0, 0.8)), ('lech_1.0_vs_0.9', (1.0, 0.9))):
    R = K79.do_day_2d(vid(ten + '.avi', *a), f'{FX}/p9_matna.png', K78.LOP_A_E, {'nha_thuong': K78.NHA_THUONG})
    out[ten] = dict(toc_do_pct_s=R['toc_do_pct_s'], du_a=R['du_a'], du_ngoai=R['du_ngoai'], tran=round(max(K79.DAY_DU_SAN, K79.DAY_DU_K * R['du_ngoai']), 2)); print(ten, out[ten])
json.dump(out, open('/home/user/cine-lab/reports/k1179/do/kn6-day2d.json', 'w'), indent=1)
