#!/opt/cine/bin/python
"""K2C-T2-01 · TT3 (chủ dự án 17/10): tờ so sánh trước chấm lần 5 — khung ĐÚNG giây đã khai (g2/rague-cap.json, g2/sua-cap.json) của 12 cặp
từ master mới, đặt cạnh khung T2 lần 4 cùng cặp (kiem-mu/<ragu|ragu-sua>-l4/<cặp>/<X|Y>.jpg theo key.json) → g2/so-sanh-l5.jpg (≤ 4 MB).
  so_sanh_l5.py <master.mp4>"""
import json, os, subprocess, sys, tempfile
H = os.path.dirname(os.path.abspath(__file__)); M = sys.argv[1]; KM = f'{H}/kiem-mu'; tmp = tempfile.mkdtemp()
rows = []
for d, caps in (('ragu-l4', 'rague-cap.json'), ('ragu-sua-l4', 'sua-cap.json')):
    C = json.load(open(f'{H}/g2/{caps}')); K = json.load(open(f'{KM}/{d}/key.json'))
    for p, k in K.items():
        if not isinstance(k, dict) or 't2_s' not in k: continue
        cv = C[p]['t2'] if isinstance(C[p], dict) else C[p]; assert abs(k['t2_s'] - float(cv)) < 1e-6, (p, k['t2_s'], cv)   # giây khung = giây đã khai
        new = f'{tmp}/{p}-l5.jpg'; subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(k['t2_s']), '-i', M, '-frames:v', '1', '-vf', 'scale=800:-2', new], check=True)
        rows.append((p, k['t2_s'], f"{KM}/{d}/{p}/{k['t2']}.jpg", new))
rows.sort(key=lambda r: (r[0][0] != 'P', r[0]))
ins, fl = [], []
for i, (p, s, old, new) in enumerate(rows):
    ins += ['-i', old, '-i', new]
    fl.append(f"[{2*i}]scale=800:-2,drawtext=text='{p} L4 @{s}':x=12:y=12:fontsize=30:fontcolor=white:box=1:boxcolor=black@0.6[a{i}];[{2*i+1}]scale=800:-2,drawtext=text='{p} L5 @{s}':x=12:y=12:fontsize=30:fontcolor=yellow:box=1:boxcolor=black@0.6[b{i}];[a{i}][b{i}]hstack[r{i}]")
fl.append(''.join(f'[r{i}]' for i in range(len(rows))) + f'vstack={len(rows)}[o]')
out = f'{H}/g2/so-sanh-l5.jpg'
for q in (4, 6, 8, 10):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', ';'.join(fl), '-map', '[o]', '-q:v', str(q), out], check=True)
    if os.path.getsize(out) <= 4e6: break
print(out, round(os.path.getsize(out) / 1e6, 2), 'MB', len(rows), 'cặp')
