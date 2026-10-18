"""T3 khoá lời · đặt lại thời lượng shot theo LỜI KHOÁ (script-v4-KHOA.md), cùng luật g1/fit_dur.py, gốc = bảng shot G1 đã duyệt (702 s):
cần = từ nói/2,5 + 0,4 s; dur = max(sàn, ⌈cần⌉₀,₅) trong trần; sàn = dur G1 cho mốc đinh/cú liên hoàn/khung neo, 3 s cho móc, còn lại min(dur G1, cần + 0,5 s) ≥ 4 s; theo loại (thẻ số 8 · ảnh/tranh/bản đồ lịch sử 12 · strategic 8 · khung neo 10 · 3D không trần);
cố định 4b 15 s, 0c 3 s (NC-H2), 4g 5,5 s (SM3 chảy sang). Ghi khoa-loi/dur-khoa.json + vay-ham/treatment.json (dur_g1 = giá trị G1), rồi chạy kiem_loi + tu_kiem.
Dùng: /opt/cine/bin/python -I channel-k2/k2c-t3-01/khoa-loi/fit_khoa.py"""
import json, math, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent; EP = HERE.parent; TP = EP / 'vay-ham/treatment.json'; PY = sys.executable
CAP = {'thẻ số': 8, 'ảnh': 12, 'tranh Ken Burns': 12, 'bản đồ chiến lược': 8, 'bản đồ lịch sử': 12}
FIX = {'4b': 15.0, '0c': 3.0, '4g': 5.5}
subprocess.run([PY, '-I', str(EP / 'g1/kiem_loi.py'), str(EP / 'script-v4-KHOA.md'), str(TP)], capture_output=True)
K = {r['id']: r for r in json.loads((EP / 'g1/kiem-chu.json').read_text())['shots']}
tr = json.loads(TP.read_text()); doi, chan = {}, []
for s in tr['shots']:
    old = s.get('dur_g1', s['dur']); need = K[s['id']]['uoc_s'] + 0.4
    cap = 10 if s.get('neo') else CAP.get(s['loai'], 99)
    keep = s.get('neo') or s.get('moc_dinh') or s.get('cu')
    floor = old if keep else (3.0 if s['ch'] == 0 else max(4.0, min(old, math.ceil((need + 0.5) * 2) / 2)))
    new = FIX.get(s['id'], max(floor, min(math.ceil(need * 2) / 2, max(cap, old))))
    if new + 1e-9 < need: chan.append([s['id'], new, round(need, 1)])
    if abs(new - old) > 1e-9: s['dur_g1'] = old; doi[s['id']] = [old, new]
    s['dur'] = new
if 'khoá lời' not in tr['note']: tr['note'] += ' | Khoá lời 18/10: thời lượng theo lời khoá (khoa-loi/dur-khoa.json; dur_g1 = giá trị G1).'
TP.write_text(json.dumps(tr, ensure_ascii=False, indent=1) + '\n')
tong = round(sum(s['dur'] for s in tr['shots']), 1)
(HERE / 'dur-khoa.json').write_text(json.dumps({'note': __doc__.splitlines()[1], 'doi': doi, 'tran_chan': chan, 'tong_g1': round(sum(s.get('dur_g1', s['dur']) for s in tr['shots']), 1), 'tong': tong}, ensure_ascii=False, indent=1) + '\n')
print(len(doi), 'shot đổi', doi, '\nchặn trần:', chan, '\ntổng', tong)
r = subprocess.run([PY, '-I', str(EP / 'g1/kiem_loi.py'), str(EP / 'script-v4-KHOA.md'), str(TP)], capture_output=True, text=True); print('\n'.join(l for l in r.stdout.splitlines() if l.startswith(('{', 'LỖI', 'CẢNH'))))
r2 = subprocess.run([PY, '-I', str(EP / 'vay-ham/tu_kiem.py')], capture_output=True, text=True); print([l for l in (r2.stdout + r2.stderr).splitlines() if 'TU KIEM' in l], 'mã', r2.returncode)
sys.exit(r.returncode or r2.returncode)
