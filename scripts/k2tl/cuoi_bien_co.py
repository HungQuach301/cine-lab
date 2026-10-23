#!/opt/cine/bin/python
"""BAN-CUOI-T3 (1e) · TÌM BIẾN CỐ HÌNH THẬT trong đặc tả shot: thời điểm (giây trong shot) một lớp vật XUẤT HIỆN / BIẾN MẤT / BẮT ĐẦU / DỪNG theo cửa sổ năm
(fleets.wY + path, smoke.wY|t, fires.wY, lives.wY, units.day, doiSong.wY, casks.wY) MÀ điểm vật nằm trong khung máy lúc đó (chiếu phối cảnh, máy nội suy tuyến tính).
Không thêm vật — chỉ đọc. Dùng bởi mk_ep_cuoi.py để khai su_kien (k='bien_co_tu_dac_ta')."""
import math

def _y(at, dy): return dy(at) if isinstance(at, str) else float(at)

def nam_tai(o, t, dy):
    T = o['time']
    for a, b in zip(T, T[1:]):
        if a['t'] <= t <= b['t']:
            u = (t - a['t']) / max(1e-9, b['t'] - a['t']); return _y(a['at'], dy) + (_y(b['at'], dy) - _y(a['at'], dy)) * u
    return _y(T[-1]['at'], dy) if t > T[-1]['t'] else _y(T[0]['at'], dy)

def t_cua_nam(o, Y, dy):
    """mọi t trong shot mà năm khung = Y (đoạn tăng)"""
    out = []; T = o['time']
    for a, b in zip(T, T[1:]):
        ya, yb = _y(a['at'], dy), _y(b['at'], dy)
        if ya < Y <= yb and yb > ya: out.append(a['t'] + (b['t'] - a['t']) * (Y - ya) / (yb - ya))
    return out

def cam_tai(cam, t):
    for a, b in zip(cam, cam[1:]):
        if a['t'] <= t <= b['t']:
            u = (t - a['t']) / max(1e-9, b['t'] - a['t']); f = lambda k: [a[k][i] + (b[k][i] - a[k][i]) * u for i in range(3)]; return f('p'), f('l'), a.get('fov', 40)
    k = cam[-1] if t > cam[-1]['t'] else cam[0]; return k['p'], k['l'], k.get('fov', 40)

def trong_khung(cam, t, E, N, h=5.0, bien=0.05):
    p, l, fov = cam_tai(cam, t); d = [l[0] - p[0], l[1] - p[1], l[2] - p[2]]; L = math.sqrt(sum(x * x for x in d)) or 1; f = [x / L for x in d]
    up = [0, 1, 0]; r = [f[1] * up[2] - f[2] * up[1], f[2] * up[0] - f[0] * up[2], f[0] * up[1] - f[1] * up[0]]; rl = math.sqrt(sum(x * x for x in r)) or 1; r = [x / rl for x in r]
    u = [r[1] * f[2] - r[2] * f[1], r[2] * f[0] - r[0] * f[2], r[0] * f[1] - r[1] * f[0]]
    v = [E - p[0], h - p[1], N - p[2]]; z = sum(a * b for a, b in zip(v, f))
    if z <= 1: return False
    th = math.tan(math.radians(fov) / 2); x = sum(a * b for a, b in zip(v, r)) / (z * th * 16 / 9); y = sum(a * b for a, b in zip(v, u)) / (z * th)
    return abs(x) <= 1 + bien and abs(y) <= 1 + bien

def bien_co(o, cam, D, dy):
    """[(t, mô tả)] — biến cố trong (0,2; D − 0,2)"""
    ev = []
    def them(Y, E, N, s):
        for t in t_cua_nam(o, Y, dy):
            if 0.2 < t < D - 0.2 and trong_khung(cam, t, E, N): ev.append((round(t, 2), s))
    def w(win):
        if not win: return []
        if isinstance(win, dict): return [(win.get(k), k) for k in ('on', 'full', 'off0', 'off1') if win.get(k) is not None]
        return [(win[0], 'on'), (win[1], 'off')]
    VI = {'on': 'xuất hiện', 'full': 'đủ', 'off0': 'bắt đầu rút', 'off1': 'hết', 'off': 'hết'}
    for f in o.get('fleets') or []:
        pts = [x['at'] for x in f.get('list') or []] or [f.get('center')]
        for Y, k in w(f.get('wY')):
            for E, N in pts[:3]: them(Y, E, N, f"tàu {VI[k]}")
        for q in (f.get('path') or [])[1:]:
            c = f.get('center') or pts[0]; them(q[0], c[0] + q[1], c[1] + q[2], 'tàu tới vị trí/đổi hướng')
    for s_ in o.get('smoke') or []:
        E, N = s_['at'][0], s_['at'][-1]
        if s_.get('t'):
            for t in s_['t']:
                if 0.2 < t < D - 0.2 and trong_khung(cam, t, E, N): ev.append((round(t, 2), 'khói bắt đầu/tắt'))
        for Y, k in w(s_.get('wY')): them(Y, E, N, f"khói {VI[k]}")
    for f in o.get('fires') or []:
        for Y, k in w(f.get('wY')): them(Y, f['at'][0], f['at'][1], f"lửa {VI[k]}")
    for L0 in o.get('lives') or []:
        lines = [w_.get('line') for w_ in L0.get('walkers') or []]; P = None
        for ln in lines:
            if isinstance(ln, list): P = ln[len(ln) // 2]
            elif isinstance(ln, str) and L0.get('lines', {}).get(ln): P = L0['lines'][ln][len(L0['lines'][ln]) // 2]
        if P is None and L0.get('boats'): b = L0['boats'][0]['pts']; P = b[len(b) // 2]
        if P:
            for Y, k in w(L0.get('wY')): them(Y, P[0], P[1], f"người/thuyền {VI[k]}")
    for u in o.get('units') or []:
        if u.get('day') and u.get('at'):
            for Y, k in w(u['day']): them(Y, u['at'][0], u['at'][1], f"nhóm người {VI[k]}")
    for sp in o.get('doiSong') or []:
        P = sp.get('at') or (sp.get('pts') or [None])[0]
        if P:
            for Y, k in w(sp.get('wY')): them(Y, P[0], P[1], f"{sp['kind']} {VI[k]}")
    c = o.get('casks')
    if c:
        for Y, k in w(c.get('wY')): them(Y, c['at'][0], c['at'][1], f"thùng hàng {VI[k]}")
    out, last = [], -9
    for t, s in sorted(ev):
        if t - last >= 0.5: out.append((t, s)); last = t
    return out

def khe_lon(su_kien, cat, D, tran=6.0):
    ev = sorted({0.0, D} | {float(e['t']) for e in su_kien} | {float(c) for c in cat or []}); return [(a, b) for a, b in zip(ev, ev[1:]) if b - a > tran]

def diem_dat(cam, t, hAt, xa=(180, 2600)):
    """điểm đất (hAt > 1,5 m) trên tia giữa-dưới khung (lệch xuống ~ 1/4 nửa khung) gần máy nhất trong khoảng xa"""
    p, l, fov = cam_tai(cam, t); d = [l[i] - p[i] for i in range(3)]; L = math.sqrt(sum(x * x for x in d)) or 1; f = [x / L for x in d]
    for dx in (0.0, -0.25, 0.25):
        for r in range(xa[0], xa[1], 40):
            E = p[0] + f[0] * r + dx * r * f[2]; N = p[2] + f[2] * r - dx * r * f[0]
            if hAt(E, N) > 1.5 and trong_khung(cam, t, E, N, h=hAt(E, N) + 20): return [round(E), round(N)]
    return None

def them_khoi(sh, D, hAt, dy, tran=6.0, tu=5.5):
    """1e: chia mỗi khoảng > tran giây bằng 'khói bếp / lửa đồng' (minh hoạ bậc 5) — chỉ shot trước 1950; trả số đã thêm + khoảng không đặt được"""
    o = sh['opt']
    if sh.get('khung_neo'): return 0, []
    n, kho = 0, []
    for a, b in khe_lon(sh['su_kien'], sh.get('cat'), D, tran):
        k = int(math.ceil((b - a) / tu)) - 1
        for j in range(1, k + 1):
            t = round(a + (b - a) * j / (k + 1), 2)
            if sh.get('lan') and t >= sh['lan'].get('t_may', sh['lan']['t']): kho.append(t); continue   # phần cú lặn theo đường máy riêng (t_may) — không đặt khói theo máy trước đó
            if nam_tai(o, t, dy) >= 1950: kho.append(t); continue   # khói bếp/lửa đồng chỉ trước 1950
            P = diem_dat(sh['cam'], t, hAt)
            if not P: kho.append(t); continue
            o.setdefault('smoke', []).append(dict(at=[P[0], round(hAt(*P) + 6, 1), P[1]], t=[t, round(min(D, t + 5.0), 2)], n=10, size=34, rise=55, drift=[-1.5, 0.6], period=0.32, seed=7000 + n + int(t * 10), alpha=0.65))
            sh['su_kien'].append(dict(t=t, k='khoi', s='khói bếp / lửa đồng bốc lên (minh hoạ bậc 5, ước lượng; nhịp 1e)')); n += 1
    sh['su_kien'].sort(key=lambda e: e['t']); return n, kho
