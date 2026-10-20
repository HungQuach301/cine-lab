#!/opt/cine/bin/python -I
"""NC-V2V · 4 clip nguồn dựng bằng CHÍNH máy V7B (opt shot lấy từ channel-k2/k2c-t3-01/v7p/episode-v7b-a.yaml @317dcf5, chỉ đổi thời gian/máy khi ghi rõ).
   clips.py <worktree V7B> <ra.json>"""
import copy, json, sys, yaml
from pathlib import Path
E = yaml.safe_load(open(Path(sys.argv[1]) / 'channel-k2/k2c-t3-01/v7p/episode-v7b-a.yaml'))['heroes']
H = lambda k: copy.deepcopy(E[k]['opt'])
C = {}
# (1) vây hãm đêm 13/9/1782, pin nổi hiện → khai hoả → cháy; máy K cao (AGL 85 m, chúc 27°) — GIỮ NGUYÊN shot H2, lấy giây 11–21 (khung 264–503)
o = H('v7b_H2'); C['c1'] = dict(opt=o, dur=E['v7b_H2']['dur'], f0=264, n=240, mo_ta='H2 V7B nguyên bản, giây 11–21: đêm 13–14/9/1782, pin nổi + lửa, máy K')
# (2) hero La Línea + Gibraltar 2026 ban ngày — máy D của H3 (trôi như H3), thời gian GIỮ 2026 suốt 10 s (H3 gốc chạy 1938 → 2026; ở đây chỉ phần 2026)
o = H('v7b_H3'); o['time'] = [{'t': 0, 'at': 2026.79, 'sun': 10.5, 'lab': 'y'}, {'t': 10.0, 'at': 2026.792, 'sun': 10.9, 'lab': 'y'}]
o['cam'] = [{'t': 0, 'p': [380, 250, 760], 'l': [-150, 0, -250], 'fov': 44}, {'t': 10.0, 'p': [363, 246, 729], 'l': [-150, 0, -250], 'fov': 44}]; o['dur'] = 10.0
C['c2'] = dict(opt=o, dur=10.0, f0=0, n=240, mo_ta='H3 V7B máy D, 2026 ngày (đổi: thời gian giữ 2026)')
# (3) lướt thấp trên mặt nước qua đoàn Rodney thả neo (1/1780) — cảnh C4 V7B, thời gian giữ 25/1/1780 trưa, máy MỚI bay thấp (AGL ≈ 14 → 9 m) giữa hai hàng tàu
o = H('v7b_C4'); o['time'] = [{'t': 0, 'at': '1780-01-25 12:00', 'sun': 13.0, 'lab': 'd'}, {'t': 10.0, 'at': '1780-01-25 12:20', 'sun': 13.3, 'lab': 'd'}]
o['cam'] = CAM3 = [{'t': 0, 'p': [-1560, 16, -560], 'l': [-1640, 6, -1500], 'fov': 50}, {'t': 10.0, 'p': [-1585, 10, -1010], 'l': [-1660, 4, -1900], 'fov': 50}]; o['dur'] = 10.0
C['c3'] = dict(opt=o, dur=10.0, f0=0, n=240, mo_ta='C4 V7B (đoàn Rodney), máy mới lướt thấp trên nước 45 m/s')
# (4) 20 s liên tục cắt làm 2 đoạn 10 s (đường nối ở giây 10) — C1-a V7B nguyên bản (trại vây hãm 1779, máy A2), giây 0–20
o = H('v7b_C1a'); C['c4'] = dict(opt=o, dur=E['v7b_C1a']['dur'], f0=0, n=480, mo_ta='C1-a V7B nguyên bản giây 0–20 (2 đoạn 10 s)')
json.dump(C, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1); print({k: (v['f0'], v['n']) for k, v in C.items()})
