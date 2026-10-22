#!/opt/cine/bin/python
"""BAN-CUOI-T3 · KIỂM KHUNG cảnh đinh sau sự cố hết đĩa (22/10 19:23): giải mã ĐẦY ĐỦ mọi jpg ghi sau mốc (PIL load) trong /var/tmp/cine-out/hero/k2c-t3-cuoi-*;
khung hỏng/cụt → in ra và (--xoa) xoá để `hero.js --resume` dựng lại (resume giữ mọi khung size > 0, nên khung cụt sẽ lọt nếu không xoá).
  cuoi_kiem_khung.py [--tu '2026-10-22 18:30'] [--xoa]"""
import datetime as dt, glob, os, sys
from PIL import Image
a = sys.argv; tu = a[a.index('--tu') + 1] if '--tu' in a else '2026-10-22 18:30'
t0 = dt.datetime.strptime(tu, '%Y-%m-%d %H:%M').replace(tzinfo=dt.timezone.utc).timestamp(); hong = {}; n = 0
for d in sorted(glob.glob('/var/tmp/cine-out/hero/k2c-t3-cuoi-*')):
    for f in sorted(glob.glob(d + '/*.jpg')):
        if os.path.getmtime(f) < t0: continue
        n += 1
        try:
            with Image.open(f) as im: im.load(); assert im.size == (1920, 1080)
        except Exception as e: hong.setdefault(d, []).append(os.path.basename(f))
for d, fs in hong.items():
    print(os.path.basename(d), len(fs), fs[:4], fs[-2:])
    if '--xoa' in a: [os.remove(os.path.join(d, f)) for f in fs]
print(f'kiểm {n} khung sau {tu} UTC · hỏng {sum(map(len, hong.values()))}' + (' · ĐÃ XOÁ' if '--xoa' in a else ''))
