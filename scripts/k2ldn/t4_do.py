#!/opt/cine/bin/python
"""TIEN-KY-T4 · BẢN THỬ T4 — đo cú máy từ log.json của render_ldn.js (đề xuất §19 (a)): mỗi đoạn → tốc độ tiêu điểm (% chiều rộng khung/giây, chiếu điểm neo
qua ma trận máy), tốc độ máy (m/s), quay hướng nhìn (°/s), năm/giây; đoạn KHOP: sai khác điểm neo giữa khung đầu và khung cuối (px).
  t4_do.py <ra.json> <thư mục đoạn 1> [<thư mục đoạn 2> …]   (điểm neo mặc định: mái vòm St Paul's 532100, 181140, 60 m)"""
import json, os, sys
import numpy as np
NEO = np.array([532100.0 - 532000, 60.0, -(181140.0 - 180800)])
def proj(fr, W, H, X):
    V = np.array(fr['view']).reshape(4, 4).T; P = np.array(fr['proj']).reshape(4, 4).T; q = P @ V @ np.append(X, 1.0); q = q[:3] / q[3]
    return np.array([(q[0] + 1) / 2 * W, (1 - q[1]) / 2 * H])
out = {'neo': 'mái vòm St Paul\'s (E 532100, N 181140, 60 m)', 'doan': []}
for d in sys.argv[2:]:
    L = json.load(open(os.path.join(d, 'log.json'))); W, H = L['W'], L['H']; fps = L['shot'].get('fps', 24); F = sorted(L['frames'], key=lambda r: r['f'])
    s = np.array([proj(r, W, H, NEO) for r in F]); p = np.array([r['cam']['p'] for r in F], float); l = np.array([r['cam']['l'] for r in F], float)
    dirs = (l - p) / np.linalg.norm(l - p, axis=1, keepdims=True); yr = np.array([r['year'] for r in F])
    v_tieu = np.linalg.norm(np.diff(s, axis=0), axis=1) * fps / W * 100; v_may = np.linalg.norm(np.diff(p, axis=0), axis=1) * fps
    ang = np.degrees(np.arccos(np.clip((dirs[1:] * dirs[:-1]).sum(1), -1, 1))) * fps
    rec = {'doan': os.path.basename(d.rstrip('/')), 'khung': len(F), 'giay': len(F) / fps, 'tieu_diem_pct_khung_s': {'tb': round(float(v_tieu.mean()), 2), 'max': round(float(v_tieu.max()), 2)},
           'may_m_s': {'tb': round(float(v_may.mean()), 1), 'max': round(float(v_may.max()), 1)}, 'quay_do_s': {'tb': round(float(ang.mean()), 2), 'max': round(float(ang.max()), 2)},
           'nam_s': round(float((yr[-1] - yr[0]) / (len(F) / fps)), 1), 'nam': [round(float(yr[0]), 2), round(float(yr[-1]), 2)],
           'neo_px_dau_cuoi': [s[0].round(1).tolist(), s[-1].round(1).tolist()]}
    if 'khop' in d: rec['khop_lech_neo_px'] = round(float(np.linalg.norm(s[-1] - s[0])), 2)
    out['doan'].append(rec); print(json.dumps(rec, ensure_ascii=False))
json.dump(out, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
