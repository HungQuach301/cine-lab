"""Tự kiểm measure_parts.py: vẽ đầu hình elip, bộ phận khác hình chữ nhật đúng tỷ lệ model sheet (khử răng cưa, toạ độ dưới điểm ảnh)
ở nhiều cỡ đầu (px) và góc xoay khác nhau; sai lệch đo được = sàn nhiễu của phép đo, không phải lỗi dựng.
Chạy: /opt/cine/bin/python reports/m0/consistency/selftest_measure.py"""
import json, os, subprocess, sys, tempfile
import cv2, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sh = json.load(open(os.path.join(HERE, 'model-sheet.json')))
def make(d, u, ang):
    os.makedirs(os.path.join(d, 'masks'), exist_ok=True)
    for i, p in enumerate(sh['measured_parts']):
        m = np.zeros((1080, 1920), np.uint8)
        if p == 'head':  # đầu là elip (trường hợp đã làm lộ lỗi minAreaRect)
            cv2.ellipse(m, ((960.3, 540.7), (sh[p]['width'] * u, sh[p]['length'] * u), ang), 255, -1, cv2.LINE_AA)
        else:
            box = cv2.boxPoints(((960.3, 540.7), (sh[p]['width'] * u, sh[p]['length'] * u), ang + 7 * i))
            cv2.fillPoly(m, [np.round(box * 16).astype(np.int32)], 255, lineType=cv2.LINE_AA, shift=4)
        cv2.imwrite(os.path.join(d, 'masks', f'{p}.png'), m)
out = []
for ua, ub in ((57.1, 146.4), (100, 146.4), (146.4, 146.4)):
    with tempfile.TemporaryDirectory() as t:
        a, b = os.path.join(t, 'A'), os.path.join(t, 'B'); make(a, ua, 20); make(b, ub, -65)
        r = subprocess.run([sys.executable, os.path.join(HERE, 'measure_parts.py'), a, b], capture_output=True, text=True)
        rows = json.loads(r.stdout)
        out.append({'head_px_a': ua, 'head_px_b': ub, 'max_dev_a_vs_b': max(x['dev_a_vs_b'] for x in rows),
                    'max_dev_vs_sheet': max(max(abs(x['dev_a_vs_sheet']), abs(x['dev_b_vs_sheet'])) for x in rows)})
        print(json.dumps(out[-1]))
json.dump(out, open(os.path.join(HERE, '..', 'raw', 'consistency-selftest.json'), 'w'), indent=1)
