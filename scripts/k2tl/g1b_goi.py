#!/opt/cine/bin/python
"""G1b T3 · KẾ HOẠCH RENDER SONG SONG (ngoại lệ EE2-A, Kinh thánh §12.5): từ số đo s/khung 1080p bản SẢN XUẤT theo từng cảnh (đo thật bằng g1b_probe.sh FR=two W=1920 H=1080)
+ số khung mỗi cảnh trong heroes.json (bản 1080p, không K2_DRAFT) → chia cảnh thành N gói sao cho mỗi gói ≤ TRAN giờ đồng hồ trên máy CHẬM NHẤT (hệ số an toàn K_CHAM),
ghi lệnh dựng từng gói + cách ghép + kiểm khớp màu giữa gói.
  g1b_goi.py --bench <thư mục dò 1080p> --heroes <heroes.json bản 1080p> --out <ke-hoach.json> [--tran 10] [--k-cham 1.25] [--md <ra.md>]
Cách tính giờ một cảnh = setup (đo: thời gian dò − 2 khung × s/khung) + khung × s/khung. Gói hoá: tham lam LPT (cảnh dài trước, vào gói đang nhẹ nhất), tăng N tới khi mọi gói ≤ trần."""
import argparse, json, math, os, re
from pathlib import Path

a = argparse.ArgumentParser(); a.add_argument('--bench', required=True); a.add_argument('--heroes', required=True); a.add_argument('--out', required=True)
a.add_argument('--tran', type=float, default=10.0); a.add_argument('--k-cham', type=float, default=1.25); a.add_argument('--md'); A = a.parse_args()
H = json.loads(Path(A.heroes).read_text()); B = Path(A.bench)
log = {l.split()[0]: int(re.search(r'(\d+)s', l).group(1)) for l in (B / 'probe.log').read_text().splitlines() if ' rc=0 ' in l}
rows = []
for k, h in H.items():
    n = int(round(float(h['opt'].get('dur', h['dur'])) * 24)) if h['hero'].startswith('tl/') else int(round(float(h['dur']) * 24))
    m = B / k / 'meta.json'
    if h['hero'].startswith('footage/'): spf, setup, src = 0.02, 2, 'ffmpeg (đo gần 0)'
    elif m.exists():
        spf = json.loads(m.read_text())['s_per_frame']; setup = max(5, log.get(k, 0) - 2 * spf); src = 'đo'
    else: spf, setup, src = None, None, 'THIẾU số đo'
    rows.append(dict(canh=k, hero=h['hero'], khung=n, s_khung=spf, setup_s=setup, gio=None if spf is None else round((setup + n * spf) / 3600, 3), nguon=src))
miss = [r['canh'] for r in rows if r['gio'] is None]
med = sorted(r['s_khung'] for r in rows if r['s_khung'] and r['hero'].startswith('tl/'))
fill = med[len(med) // 2] if med else 20.0
for r in rows:
    if r['gio'] is None: r['s_khung'] = fill; r['setup_s'] = 60; r['gio'] = round((60 + r['khung'] * fill) / 3600, 3); r['nguon'] = f'ước = trung vị cảnh tl {fill} s/khung (thiếu số đo)'
tong = sum(r['gio'] for r in rows); cap = A.tran / A.k_cham
big = [r for r in rows if r['gio'] > cap]
# cảnh dài hơn trần gói → tách theo dải khung (hero.js --only a-b … ; dựng tiếp --resume ghép cùng thư mục)
items = []
for r in rows:
    if r['gio'] <= cap: items.append(dict(r, dai=None)); continue
    k = math.ceil(r['gio'] / cap); step = math.ceil(r['khung'] / k)
    for i in range(k): f0, f1 = i * step, min(r['khung'], (i + 1) * step) - 1; items.append(dict(r, dai=[f0, f1], gio=round((r['setup_s'] + (f1 - f0 + 1) * r['s_khung']) / 3600, 3)))
items.sort(key=lambda x: -x['gio'])
N = max(1, math.ceil(sum(x['gio'] for x in items) / cap))
while True:
    G = [dict(gio=0.0, canh=[]) for _ in range(N)]
    for x in items: g = min(G, key=lambda g: g['gio']); g['canh'].append(x); g['gio'] += x['gio']
    if max(g['gio'] for g in G) <= cap + 1e-9: break
    N += 1
plan = dict(tran_gio=A.tran, he_so_may_cham=A.k_cham, tran_hieu_dung_gio=round(cap, 2), tong_gio_1_may=round(tong, 2), so_goi=N, thieu_so_do=miss,
            goi=[dict(id=f'G{i + 1:02d}', gio_may_do=round(g['gio'], 2), gio_may_cham=round(g['gio'] * A.k_cham, 2), canh=[dict(canh=x['canh'], dai=x['dai'], gio=x['gio']) for x in g['canh']]) for i, g in enumerate(G)],
            bang=rows)
Path(A.out).write_text(json.dumps(plan, ensure_ascii=False, indent=1) + '\n')
if A.md:
    L = [f'| Gói | Giờ (máy đo) | Giờ (máy chậm ×{A.k_cham}) | Cảnh |', '|---|---|---|---|']
    for g in plan['goi']: L.append(f"| {g['id']} | {g['gio_may_do']} | {g['gio_may_cham']} | " + ', '.join(c['canh'][4:] + (f"[{c['dai'][0]}–{c['dai'][1]}]" if c['dai'] else '') for c in g['canh']) + ' |')
    Path(A.md).write_text('\n'.join(L) + '\n')
print(f"tổng {tong:.1f} h (1 tiến trình) · trần hiệu dụng {cap:.1f} h · {N} gói · thiếu số đo: {len(miss)}")
