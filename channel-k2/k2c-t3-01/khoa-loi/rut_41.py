"""Khoá lời v4.1 · tổng phim ≤ 720 s (lệnh: vượt thì rút tấm im lặng hoặc thẻ, KHÔNG cắt lời). Chạy SAU fit_khoa.py (LOI=script-v4.1-KHOA.md).
Thứ tự rút, dừng khi ≤ 720 s: tấm im lặng KB1943, KA2026 9 → 8 s (sàn Kinh thánh §11.2); thẻ số còn dư so lời (cần = từ nói/2,5 + vào trễ + 0,4 s) rút tới đúng lời + 0,4 s, bậc 1 khung hình (1/24 s, 24 fps).
Giữ dur trước rút ở trường dur_truoc_rut. Ghi khoa-loi/rut-41.json. Dùng: /opt/cine/bin/python -I channel-k2/k2c-t3-01/khoa-loi/rut_41.py"""
import json, math, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent; EP = HERE.parent; TP = EP / 'vay-ham/treatment.json'; PY = sys.executable; CAP = 720.0
tr = json.loads(TP.read_text()); S = tr['shots']; K = {r['id']: r for r in json.loads((EP / 'g1/kiem-chu.json').read_text())['shots']}
tong = lambda: round(sum(s['dur'] for s in S), 3); rut = []
def set_dur(s, d):
    s.setdefault('dur_truoc_rut', s['dur']); rut.append([s['id'], s['dur'], d]); s['dur'] = d
for s in S:
    if tong() <= CAP: break
    if s.get('im_lang') and s['dur'] > 8.0: set_dur(s, 8.0)
for s in S:
    if tong() <= CAP: break
    if s['loai'] == 'thẻ số':
        k = K[s['id']]; need = round(math.ceil((k['uoc_s'] + k['bat_dau_tre_s'] + 0.4) * 24 - 1e-6) / 24, 4)   # bậc 1 khung hình (24 fps)
        if need < s['dur']: set_dur(s, need)
TP.write_text(json.dumps(tr, ensure_ascii=False, indent=1) + '\n')
(HERE / 'rut-41.json').write_text(json.dumps({'note': __doc__.splitlines()[1], 'rut': rut, 'tong': tong()}, ensure_ascii=False, indent=1) + '\n')
print('rút', rut, 'tổng', tong())
r = subprocess.run([PY, '-I', str(EP / 'g1/kiem_loi.py'), str(EP / 'script-v4.1-KHOA.md'), str(TP)], capture_output=True, text=True); print('\n'.join(l for l in r.stdout.splitlines() if l.startswith(('{', 'LỖI', 'CẢNH'))))
r2 = subprocess.run([PY, '-I', str(EP / 'vay-ham/tu_kiem.py')], capture_output=True, text=True); print([l for l in (r2.stdout + r2.stderr).splitlines() if 'TU KIEM' in l])
sys.exit(1 if tong() > CAP else (r.returncode or r2.returncode))
