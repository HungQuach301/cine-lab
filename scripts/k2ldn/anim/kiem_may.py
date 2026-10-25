#!/opt/cine/bin/python
"""ANIMATIC-T4 · tự đo cú máy §19 (a) TRƯỚC và SAU dựng (tham khảo; chấm chính thức là MAY-19 của k2check 1.17.4).
Đọc tệp máy (khoá) hoặc log.json của render_look.js (cam mỗi khung) → tốc độ TB trượt 1 s, lấy lớn nhất trong shot:
tiêu điểm dịch (% bề ngang/s, chiếu qua máy pinhole cùng fov), tiến/lùi (% khoảng cách tới tiêu điểm/s), dọc (m/s), góc chúc (°/s), vòng quanh tiêu điểm (°/s), tổng vòng (°), độ cao + góc chúc.
  kiem_may.py <tệp máy hoặc log.json> … → bảng + JSON (--json ra.json)"""
import json, math, sys
import numpy as np
W, H, FPS = 640, 360, 24
GH = {'CODINH': [('td', 2.0)], 'DAY': [('td', 1.5), ('tien', 1.5)], 'KEO': [('lui', 2.0)], 'CAU': [('doc', 6.0), ('chuc', 1.5)], 'VONG': [('vong', 3.0), ('vong_tong', 45)],
      'TRUOT': [('td', 3.0)], 'NGHIENG': [('chuc', 2.0)], 'THAP': [], 'XUONG': [], 'KHOP': [('td', 0.5)], 'LAN': []}


def frames_from(j):
    if 'frames' in j:   # log.json
        return [(f['cam']['p'], f['cam']['l'], f['cam']['fov']) for f in j['frames']], j['shot']
    K = j['keys']; n = max(1, round(j['dur'] * FPS)); out = []
    ts = [k['t'] for k in K]
    for i in range(n):
        t = i / FPS; p = [float(np.interp(t, ts, [k['p'][a] for k in K])) for a in range(3)]; l = [float(np.interp(t, ts, [k['l'][a] for k in K])) for a in range(3)]
        out.append((p, l, float(np.interp(t, ts, [k['fov'] for k in K]))))
    return out, j


def proj(p, l, fov, x):
    p, l, x = map(lambda v: np.array(v, float), (p, l, x)); f = l - p; f /= np.linalg.norm(f); r = np.cross(f, [0, 0, 1.0]); r /= np.linalg.norm(r); u = np.cross(r, f)
    d = x - p; z = d @ f; fy = 1 / math.tan(math.radians(fov) / 2); fx = fy * H / W
    return np.array([0.5 + 0.5 * (d @ r) / z * fx, 0.5 - 0.5 * (d @ u) / z * fy]) if z > 1 else np.array([np.nan, np.nan])


def do(path):
    j = json.load(open(path)); F, S = frames_from(j); cu = S.get('cu_may', '?'); td = S.get('tieu_diem_en') or F[0][1]
    td = np.array(td, float); P = np.array([f[0] for f in F]); L = np.array([f[1] for f in F])
    pr = np.array([proj(*f, td) for f in F]); dist = np.linalg.norm(td - P, axis=1)
    v = L - P; chuc = np.degrees(np.arctan2(v[:, 2], np.hypot(v[:, 0], v[:, 1])))
    az = np.degrees(np.arctan2(P[:, 1] - td[1], P[:, 0] - td[0]))
    def rate(x, scale=1.0):
        if len(x) < 2: return 0.0
        d = np.abs(np.diff(x, axis=0)) * FPS * scale
        if d.ndim > 1: d = np.linalg.norm(d, axis=1)
        k = min(FPS, len(d)); c = np.convolve(np.nan_to_num(d), np.ones(k) / k, mode='valid'); return float(np.max(c)) if len(c) else 0.0
    rel = np.diff(dist) / dist[:-1] * 100 * FPS if len(dist) > 1 else np.array([0.0])
    k = min(FPS, max(1, len(rel))); mv = np.convolve(rel, np.ones(k) / k, mode='valid') if len(rel) else np.array([0.0])
    R = {'shot': S.get('shot', path), 'cu_may': cu, 'khung': len(F), 'td': round(rate(pr[:, 0:1], 100), 3), 'tien': round(float(max(0, -mv.min())), 3), 'lui': round(float(max(0, mv.max())), 3),
         'doc': round(rate(P[:, 2]), 3), 'chuc': round(rate(chuc), 3), 'vong': round(rate(np.unwrap(np.radians(az)), 180 / math.pi), 3) if cu == 'VONG' else 0.0,
         'vong_tong': round(float(np.ptp(np.degrees(np.unwrap(np.radians(az))))), 2) if cu == 'VONG' else 0.0, 'h_min': round(float(P[:, 2].min()), 1), 'h_max': round(float(P[:, 2].max()), 1),
         'chuc_dau': round(float(chuc[0]), 1), 'chuc_cuoi': round(float(chuc[-1]), 1), 'td_ra_ngoai_1_6': bool(np.nanmax(np.abs(pr[:, 0] - 0.5)) > 1 / 3)}
    loi = [f'{k} {R[k]} > {lim}' for k, lim in GH.get(cu, []) if R[k] > lim]
    if cu == 'THAP' and not (5 <= R['chuc_dau'] <= 15): loi.append(f"ngửa {R['chuc_dau']}° ngoài 5–15°")
    if cu == 'XUONG' and not (R['chuc_dau'] <= -85 and -35 <= R['chuc_cuoi'] <= -20): loi.append(f"chúc {R['chuc_dau']} → {R['chuc_cuoi']}")
    if cu == 'CAU' and not (150 <= R['h_min'] and R['h_max'] <= 300): R['canh_bao'] = 'cao ngoài 150–300 m'
    R['loi'] = loi; R['dat'] = not loi; return R


if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]; outj = sys.argv[sys.argv.index('--json') + 1] if '--json' in sys.argv else None
    if outj: a = [x for x in a if x != outj]
    rs = [do(p) for p in a]
    for r in rs: print(f"{r['shot']:10s} {r['cu_may']:8s} td {r['td']:6.2f}%/s tiến {r['tien']:5.2f} lùi {r['lui']:5.2f} dọc {r['doc']:5.2f} chúc {r['chuc']:5.2f} vòng {r['vong']:5.2f}/{r['vong_tong']:5.1f}° h {r['h_min']:.0f}–{r['h_max']:.0f} góc {r['chuc_dau']}→{r['chuc_cuoi']} {'ĐẠT' if r['dat'] else 'TRƯỢT ' + '; '.join(r['loi'])} {r.get('canh_bao', '')}")
    if outj: json.dump(rs, open(outj, 'w'), ensure_ascii=False, indent=1)
