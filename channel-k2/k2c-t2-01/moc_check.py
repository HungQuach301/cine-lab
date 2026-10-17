#!/opt/cine/bin/python
"""K2C-T2-01 · v3.4: so MỌI mốc "@từ" của các đoạn bị sửa (02, 03, 04, 06) giữa căn chữ v3.3 (vo/v3.3) và v3.4.
Đúng khi: mốc trước điểm nối giữ nguyên giây; mốc sau điểm nối dời đúng bằng phần âm cắt (−) / chèn (+). Khác → trỏ nhầm hoặc gãy → in ra để sửa đặc tả.
  moc_check.py"""
import json, os, re, sys, yaml
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', '..', 'scripts/ll')); import ll  # noqa
J = json.load(open(f'{H}/vo/sua-v3.4.json'))
SH = {'03': [(J['03'][0]['noi_s'], -J['03'][0]['cat'])], '04': [(J['04'][0]['noi_s'], -J['04'][0]['cat'])], '02': [(J['02'][0]['noi_s'], -J['02'][0]['cat'])],
      '06': [(J['06'][0]['noi_s'], -J['06'][0]['cat'] - J['06'][1]['cat']), (J['06'][2]['noi_s'][0], J['06'][2]['chen'])]}
Ssrc = yaml.safe_load(open(f'{H}/ep-src-segs.yaml')); HZ = yaml.safe_load(open(f'{H}/ep-src-heroes.yaml'))['heroes']
def strs(x):
    if isinstance(x, str) and re.match(r'^@', x): yield x
    elif isinstance(x, dict):
        for v in x.values(): yield from strs(v)
    elif isinstance(x, list):
        for v in x: yield from strs(v)
bad = 0
for sg in Ssrc['segments']:
    sid = sg['id']
    if sid not in SH: continue
    W0 = ll.words(json.load(open(f'{H}/vo/v3.3/k2c-t2-01-{sid}.align.json'))); W1 = ll.words(json.load(open(f'{H}/vo/k2c-t2-01-{sid}.align.json')))
    A = set()
    for sh in sg['shots']:
        A |= set(strs(sh)); h = sh.get('p', {}).get('hero')
        if h: A |= set(strs(HZ.get(h, {})))
    for a in sorted(A):
        try: t0 = ll.anchor(a, W0, 0, '')
        except SystemExit: t0 = None
        try: t1 = ll.anchor(a, W1, 0, '')
        except SystemExit: t1 = None
        if t0 is None: continue
        # SH lưu điểm nối theo giờ v3.3 cho cắt; với 06 (cắt rồi chèn) giờ chèn tính sau khi cắt → quy về v3.3 cộng phần đã cắt
        exp = t0; cum = 0.0
        for k, (p, d) in enumerate(SH[sid]):
            pv = p if k == 0 else p - SH[sid][0][1]   # điểm chèn (giờ sau cắt) → giờ v3.3
            if t0 > pv: exp += d
        ok = t1 is not None and abs(t1 - exp) < 0.02
        if not ok: bad += 1; print(f'{sid} {a:28s} v3.3 {t0:7.2f}  v3.4 {t1 if t1 is None else round(t1, 2)}  (cần ≈ {exp:.2f})')
print('mốc lệch:', bad)
