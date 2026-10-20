#!/opt/cine/bin/python
"""V7C (việc 2) · THỬ ĐIỂM MÁY ỨNG VIÊN cho một shot: đo mặt nạ ID (nội dung %, trống %, tiêu điểm, AGL, góc nhìn xuống) của mọi máy ứng viên trên CÙNG trạng thái khung
(năm/giờ/vật của shot), kèm khung màu 480×270 để soi. Chọn máy theo luật đo được (việc 2 a–c), không theo cảm giác.
  v7c_thu_may.py <tệp opt shot .json> <tệp ứng viên .json: [{id, p, l, fov}]> <thư mục ra> --only 0,120,240 [--td '<json>'] [--loai pho|vinh|trai]"""
import json, os, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
a = sys.argv[1:]; opt, cams, out = a[0], a[1], Path(a[2]); out.mkdir(parents=True, exist_ok=True)
only = a[a.index('--only') + 1]; td = a[a.index('--td') + 1] if '--td' in a else '[]'; loai = a[a.index('--loai') + 1] if '--loai' in a else 'pho'
ng = {'pho': 50, 'vinh': 40, 'trai': 40}[loai]
r = subprocess.run(['node', str(ROOT / 'design/k2v/v7c/do_bocuc.js'), '--opt', open(opt).read(), '--only', only, '--cams', open(cams).read(), '--td', td, '--out', str(out / 'do.json'),
                    '--jpg', str(out / 'jpg'), '--w', '480', '--h', '270', '--scale', '1'], capture_output=True, text=True, env=dict(os.environ, K2TL_CACHE=os.environ.get('K2TL_CACHE', '/var/tmp/cine-out/k2tl-cache')))
if r.returncode: print(r.stderr[-2000:]); sys.exit(1)
F = json.load(open(out / 'do.json'))['frames']; by = {}
for x in F: by.setdefault(x['ung_vien'], []).append(x)
print(f'| máy | nội dung % (ngưỡng {ng}) | trống % (≤ 33) | trời % | đá % | tiêu điểm (rộng %, đạt) | AGL | xuống ° |')
for k, L in by.items():
    av = lambda f: sum(f(x) for x in L) / len(L)
    tds = ' '.join(f"{t.get('rong_pct', '-')}{'✓' if t.get('dat') else '✗'}" for x in L for t in x['td'])
    print(f"| {k} | {av(lambda x: x['noi_dung']):.1f} ({min(x['noi_dung'] for x in L):.0f}) | {av(lambda x: x['trong']):.1f} | {av(lambda x: x['pct']['troi']):.1f} | {av(lambda x: x['pct']['da']):.1f} | {tds} | {av(lambda x: x['agl']):.0f} | {av(lambda x: x['xuong']):.1f} |")
