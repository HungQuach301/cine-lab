"""M0 bước 6 — đo tỷ lệ bộ phận nhân vật từ mặt nạ đã render (không dùng số tự khai của agent).
Mỗi shot có thư mục masks/ với <part>.png (bộ phận vẽ riêng, trắng trên đen, cùng phép biến đổi như khung hình).
Độ dài bộ phận = cạnh dài của hình chữ nhật bao nhỏ nhất (cv2.minAreaRect) của mặt nạ.
ratio = length(part) / length(head). So với model sheet và giữa 2 shot; ngưỡng C3 = 3% (nội bộ).
Chạy: /opt/cine/bin/python reports/m0/consistency/measure_parts.py SHOT_A_DIR SHOT_B_DIR"""
import json, os, sys
import cv2, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sheet = json.load(open(os.path.join(HERE, 'model-sheet.json')))
PARTS = sheet['measured_parts']
TOL = 0.03

def measure(shot):
    out = {}
    for p in PARTS:
        fn = os.path.join(shot, 'masks', f'{p}.png')
        if not os.path.exists(fn):
            out[p] = None; continue
        m = cv2.imread(fn, cv2.IMREAD_GRAYSCALE)
        pts = cv2.findNonZero((m > 127).astype(np.uint8))
        if pts is None:
            out[p] = None; continue
        (cx, cy), (w, h), ang = cv2.minAreaRect(pts)
        out[p] = {'length_px': round(max(w, h), 2), 'width_px': round(min(w, h), 2), 'area_px': int(len(pts))}
    return out

def ratios(meas):
    hl = meas['head']['length_px']
    return {p: (round(meas[p]['length_px'] / hl, 4) if meas.get(p) else None) for p in PARTS}

shots = sys.argv[1:3]
M = {s: measure(s) for s in shots}
R = {s: ratios(M[s]) for s in shots}
sheet_r = {p: sheet[p]['length'] / sheet['head']['length'] for p in PARTS}
rows = []
for p in PARTS:
    a, b = R[shots[0]][p], R[shots[1]][p]
    row = {'part': p, 'sheet': round(sheet_r[p], 4), 'shot_a': a, 'shot_b': b}
    if a and b:
        row['dev_a_vs_sheet'] = round(a / sheet_r[p] - 1, 4)
        row['dev_b_vs_sheet'] = round(b / sheet_r[p] - 1, 4)
        row['dev_a_vs_b'] = round(abs(a / b - 1), 4)
        row['pass_C3_between_shots'] = row['dev_a_vs_b'] <= TOL
        row['within_5pct_of_threshold'] = abs(row['dev_a_vs_b'] - TOL) <= 0.05 * TOL
    rows.append(row)
res = {'shots': shots, 'tolerance': TOL, 'head_px': {s: M[s]['head']['length_px'] for s in shots},
       'measurements': M, 'rows': rows}
print(json.dumps(rows, indent=1))
json.dump(res, open(os.path.join(HERE, '..', 'raw', 'consistency-measure.json'), 'w'), indent=1)
