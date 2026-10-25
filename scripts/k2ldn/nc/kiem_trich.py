"""NC-T4: kiểm mọi câu trích trong DIEM-NHAN.json khớp NGUYÊN VĂN tệp nguồn (chuẩn hoá khoảng trắng/xuống dòng). Dùng: python -I kiem_trich.py DIEM-NHAN.json"""
import json, sys, re
n = lambda s: re.sub(r'\s+', ' ', s).strip()
d = json.load(open(sys.argv[1])); ok = bad = 0
for m in d['diem_nhan']:
    for s in m['nguon']:
        f = s['tep'].split(' ')[0]
        try: t = n(open(f, encoding='utf-8').read())
        except OSError: print('BỎ QUA (không phải tệp)', m['ma'], f); continue
        for q in s['trich']:
            if n(q) in t: ok += 1
            else: bad += 1; print('LỆCH', m['ma'], f, '|', q[:80])
print(f'khớp {ok} · lệch {bad}'); sys.exit(1 if bad else 0)
