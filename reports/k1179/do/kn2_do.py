#!/opt/cine/bin/python
"""K-1.17.9 · KN-2 — số đo: Q37 (b)(c) của đặc tả v4 khi cộng thêm biến cố ĐO TỪ LOG MÁY (không khai) theo từng loại neo.
Đầu vào CHỈ ĐỌC @bc1693b5 (dac-ta-v4: episode.yaml, timeline.json, log-shot.json; animatic2/log-may/*.json — log máy thật của animatic v3, cùng máy với bảng v4).
Loại neo (mỗi loại = một biến cố tại khung đầu của thay đổi, trong khung shot):
  (n1) mặt trời qua chân trời / hoàng hôn dân sự: sun_el đổi dấu qua 0° hoặc qua −6°
  (n2) pha máy: tốc độ máy (|Δ vị trí| + góc nhìn quy về px khung) chuyển giữa ĐỨNG (< 10 % đỉnh của shot) và CHẠY
  (n3) lửa: trường `fire` của log đổi ≥ 10 % so với lần biến cố trước trong shot (đơn vị log — chỉ để tham khảo, chưa hiệu chuẩn thấy được)
  (n4) năm qua số nguyên (bộ đếm năm nhảy) — CẬN TRÊN, không phải biến cố hình (đồng hồ chạy không tính từ 1.15)
In: TB, dài nhất, số shot > 6 s không biến cố — trước/sau mỗi loại. Không API.   kn2_do.py <ra.json>
"""
import json, math, os, sys
sys.path.insert(0, os.environ.get('K_REPO', '/home/user/cine-lab'))
import yaml
from checks.ll import q_nhip as QN
D = '/var/tmp/k1179/in/channel-k2/k2c-t4-02/ban-cuoi/dac-ta-v4'
E = yaml.safe_load(open(f'{D}/episode.yaml')); TL = json.load(open(f'{D}/timeline.json')); LS = json.load(open(f'{D}/log-shot.json'))


def ev_shot(s):
    p = s.get('log_may')
    if not p: return {}
    L = json.load(open(os.path.normpath(os.path.join(D, p)))); F = L['frames']; fps = (L.get('shot') or {}).get('fps', 24)
    dur = float(s['dur']); n = min(len(F), int(round(dur * fps))); F = F[:n]; t0 = float(s['t0']); out = {k: [] for k in ('n1', 'n2', 'n3', 'n4')}
    for a, b in zip(F, F[1:]):
        t = t0 + b['f'] / fps
        for z in (0.0, -6.0):
            if a.get('sun_el') is not None and (a['sun_el'] - z) * (b['sun_el'] - z) < 0: out['n1'].append((t, f'sun_el qua {z:g}°'))
        if a.get('year') is not None and math.floor(a['year']) != math.floor(b['year']): out['n4'].append((t, f"năm {math.floor(b['year'])}"))
    # pha máy
    sp = []
    for a, b in zip(F, F[1:]):
        pa, pb = a['cam']['p'], b['cam']['p']; la, lb = a['cam']['l'], b['cam']['l']
        dist = max(1.0, math.dist(pa, la)); v = math.dist(pa, pb) / dist + math.acos(max(-1, min(1, sum((x - y) * (u - w) for x, y, u, w in zip(la, pa, lb, pb)) / (math.dist(la, pa) * math.dist(lb, pb) + 1e-9))))
        sp.append(v)
    if sp and max(sp) > 0:
        th = 0.1 * max(sp); st = [x >= th for x in sp]
        for i in range(1, len(st)):
            if st[i] != st[i - 1]: out['n2'].append((t0 + (i + 1) / fps, 'máy chạy' if st[i] else 'máy dừng'))
    lf = None
    for b in F:
        fv = b.get('fire')
        if fv is None: continue
        if lf is None: lf = fv; continue
        if abs(fv - lf) >= 0.10 * max(abs(lf), 1e-6) and abs(fv - lf) > 0: out['n3'].append((t0 + b['f'] / fps, f'fire {lf:.3g}→{fv:.3g}')); lf = fv
    return out


ALL = {k: [] for k in ('n1', 'n2', 'n3', 'n4')}
for s in LS:
    for k, v in ev_shot(s).items(): ALL[k] += [(t, s['shot'], f'log:{k}', m) for t, m in v]
R = dict(so_bien_co_log={k: len(v) for k, v in ALL.items()})
goc = QN.q37(E, TL)
R['goc'] = dict(val=goc['val'], bien_co=goc['bien_co'])
for ten, ks in (('n1', ['n1']), ('n2', ['n2']), ('n3', ['n3']), ('n1+n2', ['n1', 'n2']), ('n1+n2+n3', ['n1', 'n2', 'n3']), ('n4 (cận trên)', ['n4']), ('n1+n2+n3+n4', ['n1', 'n2', 'n3', 'n4'])):
    x = QN.q37(E, TL, bcv=sum((ALL[k] for k in ks), []))
    R[ten] = dict(tb=(x['bien_co'] or {}).get('tb'), dai_nhat=(x['bien_co'] or {}).get('dai_nhat'), tu=(x['bien_co'] or {}).get('dai_nhat_tu'), gop=(x['bien_co'] or {}).get('gop'),
                  loi=[l for l in x['loi'] if l.startswith('(b)') or l.startswith('(c)')])
json.dump(R, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1)[:4000])
