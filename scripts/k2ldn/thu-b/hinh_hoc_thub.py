#!/opt/cine/bin/python
"""THU-B-T4 · hình học London cho vòng thử chống "đồ chơi" (K2C-T4-02) — bản SAO đọc lại hinh_hoc_v2.py (LOOK-T4-V2), KHÔNG sửa tệp của LOOK/ANIMATIC.
  hinh_hoc_thub.py b   → $LDN_DATA/look3b/  hình học V2 TỪNG TAM GIÁC (SHA ldn2.bin phải trùng look2/) + mã nhà/mặt phẳng cho phép kiểm BE-MAT-NHA (K-1.17.5 §7)
  hinh_hoc_thub.py d   → $LDN_DATA/look3d/  biến thể (D) NÂNG 3D: đa dạng khối/mái theo lô, gãy mái, mái hắt (eave) có độ vươn, cửa mái, ống khói có chụp,
                                            màu theo nhà; toà 2026 thường: lan can mái + thiết bị/phòng máy + lam; KHÔNG đổi công trình có tên (lớp 5, 8, 9, cầu, tường, toà OSM có tên).
Tệp thêm (cạnh ldn2.bin, cùng thứ tự đỉnh): hid.f32 (mã nhà THƯỜNG cho mỗi đỉnh; 0 = không phải nhà thường), pid.f32 (mã mặt phẳng trong nhà thường; 0 = khác),
  nha.json ({id: {k, lo, E, N, y0, y1, ten?}}) — "lo" = chỉ số lô 1666 (lots/kho_ven_song) hoặc 'osm:<id>' cho toà 2026.
Nhà thường = lớp k 1 (nhà 1666), 3 (nhà xây lại 1667+), 10 (khối Victoria–Edward), 4 (toà 2026 KHÔNG có tên OSM, không phải 30 St Mary Axe/Leadenhall).
Bộ sinh ngẫu nhiên chung của thành phố KHÔNG bị tiêu thụ thêm: biến thể D chỉ dùng băm theo vị trí nhà (zlib.crc32) → lô, vị trí, số nhà giữ nguyên."""
import os, sys, json, math, zlib, hashlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
MODE = (sys.argv[1] if len(sys.argv) > 1 else 'b').lower()
import hinh_hoc_v2 as V2                      # noqa: E402  (vá 3 công trình như LOOK-T4-V2; main không chạy khi import)
HL = V2.HL
HL.OUT = os.path.join(HL.H0.DATA, 'look3' + MODE); os.makedirs(HL.OUT, exist_ok=True)
M = HL.M
CUR = [0]; NEXT = [1]; INFO = {}
NHA_K = (1, 3, 10)

# ---------------------------------------------------------------- ghi mã nhà theo từng tam giác (không đổi hình học, không tiêu thụ RNG)
_init, _tri, _house, _prism = M.__init__, M.tri, M.house, M.prism
def init2(s): _init(s); s.H = []
def tri2(s, a, b, c, col, tl, k, mt, fl=0, uv=((0, 0), (0, 0), (0, 0))):
    _tri(s, a, b, c, col, tl, k, mt, fl, uv); s.H += [CUR[0]] * 3
M.__init__ = init2; M.tri = tri2


def hrand(x, z, salt):
    """số giả ngẫu nhiên [0,1) theo vị trí nhà (tất định, không đụng RNG chung)"""
    return (zlib.crc32(f'{round(x, 1)}|{round(z, 1)}|{salt}'.encode()) % 100000) / 100000.0


def house_d(s, c, u, v, w, d, y0, y1, colw, colr, tl, k, mtw, mtr, roof='front', pitch=50.0, jetty=0.0, fl_front=1, ybase=None, eave=0.35):
    """bản sao M.house (hinh_hoc_look.py) + MÁI HẮT: mặt mái vươn ra ngoài tường `eave` m (theo cả hai trục, hạ theo độ dốc) + diềm mái (fascia) mỏng
    — tạo bóng đổ dưới mái và phá mép sắc hộp; tường giữ nguyên."""
    if roof == 'flat' or eave <= 0: return _house(s, c, u, v, w, d, y0, y1, colw, colr, tl, k, mtw, mtr, roof, pitch, jetty, fl_front, ybase)
    yb = y0 if ybase is None else ybase
    cx, cz = c; ux, uz = u; vx, vz = v
    P = lambda a, b: (cx + ux * a + vx * b, cz + uz * a + vz * b)
    # tường + đầu hồi: gọi bản gốc với roof='flat' rồi BỎ mặt phẳng mái bằng (2 tam giác cuối) — chỉ giữ tường
    n0 = len(s.P); _house(s, c, u, v, w, d, y0, y1, colw, colr, tl, k, mtw, mtr, 'flat', pitch, jetty, fl_front, ybase)
    for L_ in (s.P, s.C, s.T, s.K, s.UV, s.MT, s.FL, s.H): del L_[len(L_) - 6:]
    e = eave; tp = math.tan(math.radians(pitch))
    A, B, C_, D = P(-w / 2, -d / 2), P(w / 2, -d / 2), P(w / 2, d / 2), P(-w / 2, d / 2)
    if roof == 'front':
        rh = (w / 2) * tp; ye = y1 - e * tp
        m0, m1 = P(0, -d / 2 - e), P(0, d / 2 + e)
        Ae, De = P(-w / 2 - e, -d / 2 - e), P(-w / 2 - e, d / 2 + e); Be, Ce = P(w / 2 + e, -d / 2 - e), P(w / 2 + e, d / 2 + e)
        Rf, Rb = (m0[0], y1 + rh, m0[1]), (m1[0], y1 + rh, m1[1]); sl = math.hypot(w / 2 + e, rh + e * tp); dd = d + 2 * e
        s.quad((Ae[0], ye, Ae[1]), Rf, Rb, (De[0], ye, De[1]), colr, tl, k, mtr, 4, ((0, 0), (0, sl), (dd, sl), (dd, 0)))
        s.quad((Ce[0], ye, Ce[1]), Rb, Rf, (Be[0], ye, Be[1]), colr, tl, k, mtr, 4, ((0, 0), (0, sl), (dd, sl), (dd, 0)))
        s.tri((B[0], y1, B[1]), (P(0, -d / 2)[0], y1 + rh, P(0, -d / 2)[1]), (A[0], y1, A[1]), colw, tl, k, mtw, 8 | fl_front, ((w, y1 - yb), (w / 2, y1 + rh - yb), (0, y1 - yb)))
        s.tri((D[0], y1, D[1]), (P(0, d / 2)[0], y1 + rh, P(0, d / 2)[1]), (C_[0], y1, C_[1]), colw, tl, k, mtw, 0, ((0, y1 - yb), (w / 2, y1 + rh - yb), (w, y1 - yb)))
        top = y1 + rh; eaves = [(Ae, De), (Ce, Be)]
    elif roof == 'side':
        rh = (d / 2) * tp; ye = y1 - e * tp
        m0, m1 = P(-w / 2 - e, 0), P(w / 2 + e, 0)
        Ae, Be = P(-w / 2 - e, -d / 2 - e), P(w / 2 + e, -d / 2 - e); Ce, De = P(w / 2 + e, d / 2 + e), P(-w / 2 - e, d / 2 + e)
        Rl, Rr = (m0[0], y1 + rh, m0[1]), (m1[0], y1 + rh, m1[1]); sl = math.hypot(d / 2 + e, rh + e * tp); ww = w + 2 * e
        s.quad((Ae[0], ye, Ae[1]), (Be[0], ye, Be[1]), Rr, Rl, colr, tl, k, mtr, 4, ((0, 0), (ww, 0), (ww, sl), (0, sl)))
        s.quad((Ce[0], ye, Ce[1]), (De[0], ye, De[1]), Rl, Rr, colr, tl, k, mtr, 4, ((0, 0), (ww, 0), (ww, sl), (0, sl)))
        s.tri((D[0], y1, D[1]), (A[0], y1, A[1]), (P(-w / 2, 0)[0], y1 + rh, P(-w / 2, 0)[1]), colw, tl, k, mtw, 0, ((0, y1 - yb), (d, y1 - yb), (d / 2, y1 + rh - yb)))
        s.tri((B[0], y1, B[1]), (C_[0], y1, C_[1]), (P(w / 2, 0)[0], y1 + rh, P(w / 2, 0)[1]), colw, tl, k, mtw, 0, ((0, y1 - yb), (d, y1 - yb), (d / 2, y1 + rh - yb)))
        top = y1 + rh; eaves = [(Ae, Be), (Ce, De)]
    else:
        return _house(s, c, u, v, w, d, y0, y1, colw, colr, tl, k, mtw, mtr, roof, pitch, jetty, fl_front, ybase)
    # diềm mái (fascia) 0,22 m dưới mép mái hắt — gỗ tối (1666) / đá phiến (khác)
    fc = (58, 44, 34) if k == 1 else tuple(int(v * 0.7) for v in colr)
    for p0, p1 in eaves:
        s.quad((p0[0], ye - 0.22, p0[1]), (p1[0], ye - 0.22, p1[1]), (p1[0], ye, p1[1]), (p0[0], ye, p0[1]), fc, tl, k, 1, 0)
        s.quad((p1[0], ye - 0.22, p1[1]), (p0[0], ye - 0.22, p0[1]), (p0[0], ye, p0[1]), (p1[0], ye, p1[1]), fc, tl, k, 1, 0)
    return top


def house2(s, c, u, v, w, d, y0, y1, colw, colr, tl, k, mtw, mtr, roof='front', pitch=50.0, jetty=0.0, fl_front=1, ybase=None):
    chim = (mtw == 14 and mtr == 14)
    if not chim: CUR[0] = NEXT[0]; NEXT[0] += 1
    hid = CUR[0]
    if hid not in INFO: INFO[hid] = dict(k=int(k), x=float(c[0]), z=float(c[1]), y0=float(y0), y1=float(y1), w=float(w), d=float(d))
    if MODE != 'd' or k not in NHA_K:
        return _house(s, c, u, v, w, d, y0, y1, colw, colr, tl, k, mtw, mtr, roof, pitch, jetty, fl_front, ybase)
    x, z = c
    if chim:                                                             # ống khói: cao/thấp khác nhau + chụp ống (chimney pot) đất nung
        a = hrand(x, z, 'ch'); y1b = y1 + (a - 0.3) * 1.2
        top = _house(s, c, u, v, w, d, y0, y1b, colw, colr, tl, k, mtw, mtr, roof, pitch, jetty, fl_front, ybase)
        n = 1 + int(hrand(x, z, 'pot') * 3)
        for i in range(n):
            a_ = (i - (n - 1) / 2) * min(w, d) * 0.32
            _house(s, (x + u[0] * a_, z + u[1] * a_), u, v, 0.22, 0.22, y1b, y1b + 0.45 + 0.25 * hrand(x, z, f'p{i}'), (150, 84, 58), (40, 36, 34), tl, k, 14, 14, 'flat')
        return top
    # (1) cao theo lô: ±0–0,8 tầng (không đổi chân/lô); (2) hướng hồi đổi ở 22 % lô hẹp; (3) độ dốc rộng hơn; (4) gãy mái: lô rộng chia 2 khối khác cao/khác mái
    r1, r2, r3, r4 = (hrand(x, z, t) for t in ('h', 'r', 'p', 'g'))
    st_h = 2.8 if k == 1 else (3.0 if k == 3 else 3.6)
    y1n = y1 + (r1 - 0.45) * 0.9 * st_h * (0.6 if k == 10 else 1.0)
    y1n = max(y0 + 2.6, y1n)
    if roof in ('front', 'side') and r2 < 0.22 and w < 8: roof = 'side' if roof == 'front' else 'front'
    if roof in ('front', 'side'): pitch = float(np.clip(pitch + (r3 - 0.5) * (16 if k == 1 else 10), 28, 60))
    eave = 0.40 if k == 1 else 0.28 if k == 3 else 0.22
    if k == 10 and roof == 'flat' and r2 < 0.4: roof, pitch = 'side', 32.0 + 8 * r3        # khối Victoria: một phần mái bằng → mái dốc đá phiến
    if w >= 6.4 and r4 < 0.55 and k in (1, 3):
        a = 0.42 + 0.16 * hrand(x, z, 'ga'); wa, wb = w * a, w * (1 - a)
        ca = (x + u[0] * (-w / 2 + wa / 2), z + u[1] * (-w / 2 + wa / 2)); cb = (x + u[0] * (w / 2 - wb / 2), z + u[1] * (w / 2 - wb / 2))
        dy = (0.6 + 0.8 * hrand(x, z, 'gd')) * (1 if hrand(x, z, 'gs') < 0.5 else -1)
        rb = roof if hrand(x, z, 'gr') < 0.5 else ('front' if wb < 6.0 else 'side')
        t1 = house_d(s, ca, u, v, wa, d, y0, y1n, colw, colr, tl, k, mtw, mtr, roof, pitch, jetty, fl_front, ybase, eave)
        colw2 = tuple(int(np.clip(cc * (0.92 + 0.16 * hrand(x, z, 'gc')), 0, 255)) for cc in colw)
        t2 = house_d(s, cb, u, v, wb, d * (0.93 + 0.07 * hrand(x, z, 'gdd')), y0, max(y0 + 2.6, y1n + dy), colw2, colr, tl, k, mtw, mtr, rb, pitch + (hrand(x, z, 'gp') - 0.5) * 8, jetty, fl_front, ybase, eave)
        top = max(t1, t2)
    else:
        top = house_d(s, c, u, v, w, d, y0, y1n, colw, colr, tl, k, mtw, mtr, roof, pitch, jetty, fl_front, ybase, eave)
    # cửa mái (dormer) trên mái nhà 1666/1667 ≥ 3 tầng, mặt trước, 35 %
    if k in (1, 3) and roof in ('front', 'side') and (y1n - y0) > 7.5 and hrand(x, z, 'dm') < 0.35:
        tp = math.tan(math.radians(pitch)); half = (w / 2) if roof == 'front' else (d / 2)
        if roof == 'side':
            b_ = -d / 2 + 0.45 * half; yb_ = y1n + (half - abs(b_)) * tp * 0.25
            for a_ in ((-w * 0.22, w * 0.22) if w > 6 else (0.0,)):
                cc = (x + u[0] * a_ + v[0] * b_, z + u[1] * a_ + v[1] * b_)
                _house(s, cc, u, v, 1.5, 1.6, yb_, yb_ + 1.5, colw, colr, tl, k, mtw, mtr, 'front', 50.0, 0.0, fl_front, yb_)
    return top


def prism2(s, ring, y0, y1, ybase, colw, colr, tl, k, mtw, mtr, flw=8, roof_h=None):
    CUR[0] = NEXT[0]; NEXT[0] += 1; hid = CUR[0]
    xs = [p[0] for p in ring]; zs = [p[1] for p in ring]
    INFO[hid] = dict(k=int(k), x=float(np.mean(xs)), z=float(np.mean(zs)), y0=float(y0), y1=float(y1), ring=[[round(p[0], 2), round(p[1], 2)] for p in ring])
    out = _prism(s, ring, y0, y1, ybase, colw, colr, tl, k, mtw, mtr, flw, roof_h)
    if MODE == 'd' and k == 4 and roof_h is None and mtw in (6, 8, 11, 7):
        x, z = float(np.mean(xs)), float(np.mean(zs)); h = y1 - y0
        # lan can mái 1,1 m (mặt tường cao thêm, mặt trong tối) + 1–4 khối phòng máy/thiết bị + dải lam (kính) theo băm toà
        pc = tuple(int(v * 0.86) for v in colw)
        n = len(ring); par = 1.1 if h < 60 else 1.6
        for i in range(n):
            p0, p1 = ring[i], ring[(i + 1) % n]
            s.wall(p0, p1, y1, y1 + par, ybase, pc, tl, k, mtw, 0, 0.0)
            s.wall(p1, p0, y1, y1 + par, ybase, tuple(int(v * 0.6) for v in pc), tl, k, 12, 0, 0.0)
        A = 0.5 * abs(sum(ring[i][0] * ring[(i + 1) % n][1] - ring[(i + 1) % n][0] * ring[i][1] for i in range(n)))
        if A > 120:
            m_ = 1 + int(hrand(x, z, 'pm') * min(4, A / 250))
            P_ = np.array(ring); cx_, cz_ = P_.mean(0)
            for j in range(m_):
                a = hrand(x, z, f'e{j}') - 0.5; b = hrand(x, z, f'f{j}') - 0.5; sc = math.sqrt(A) * 0.35
                ex, ez = cx_ + a * sc, cz_ + b * sc; ew = 2.5 + hrand(x, z, f'w{j}') * min(10, sc); ed = 2.0 + hrand(x, z, f'd{j}') * min(8, sc)
                eh = 1.6 + hrand(x, z, f'h{j}') * (3.5 if h > 30 else 1.8)
                ang = math.atan2(ring[1][1] - ring[0][1], ring[1][0] - ring[0][0])
                gc = (150, 152, 150) if hrand(x, z, f'g{j}') < 0.6 else (96, 100, 104)
                _house(s, (ex, ez), (math.cos(ang), math.sin(ang)), (-math.sin(ang), math.cos(ang)), ew, ed, y1, y1 + eh, gc, tuple(int(v * 0.8) for v in gc), tl, k, 8, 12, 'flat', 0, 0.0, 0, y1)
                if hrand(x, z, f'l{j}') < 0.5:          # lam (louvre) ốp quanh phòng máy: mt 9 (kim loại) — sọc do shader kim loại
                    _house(s, (ex, ez), (math.cos(ang), math.sin(ang)), (-math.sin(ang), math.cos(ang)), ew + 0.3, ed + 0.3, y1 + 0.3, y1 + eh * 0.85, (120, 124, 128), (90, 94, 98), tl, k, 9, 9, 'flat', 0, 0.0, 0, y1)
    return out


M.house = house2; M.prism = prism2

# ---------------------------------------------------------------- lô (để khai trường "lo" của mỗi nhà)
LOTS_ALL = []
_lots, _kho = HL.lots, HL.kho_ven_song
def lots2(streets):
    out, occ = _lots(streets); LOTS_ALL.extend(out); return out, occ
def kho2(occ):
    out = _kho(occ); LOTS_ALL.extend(out); return out
HL.lots = lots2; HL.kho_ven_song = kho2

ARR = {}
_arr = M.arr
def arr3(s):
    r = _arr(s); ARR['H'] = np.array(s.H, np.int64); ARR['K'] = r[3]; ARR['P'] = r[0]; ARR['MT'] = r[5]; return r
M.arr = arr3


def ten_toa():
    """tâm (x, z) toà OSM có tên → tên (toà có tên = lớp (a), không phải nhà thường)"""
    out = []
    for b in HL.R['toa']:
        if not b.get('name'): continue
        r = np.array(b['r'], float)
        if len(r) < 3: continue
        c = r.mean(0); out.append((c[0] - HL.E0, -(c[1] - HL.N0), b['name'], b['id']))
    return out


def sau_main():
    H = ARR['H']; K = ARR['K']; P = ARR['P']; MT = ARR['MT']
    nt = len(H) // 3; Ht = H[::3]; Kt = K[::3]
    named = ten_toa(); nm_xy = np.array([[a, b] for a, b, _, _ in named]) if named else np.zeros((0, 2))
    thuong = {}
    lots_xy = np.array([[lo['c'][0] - HL.E0, -(lo['c'][1] - HL.N0)] for lo in LOTS_ALL]) if LOTS_ALL else np.zeros((0, 2))
    osm = [(np.array(b['r'], float).mean(0), b['id']) for b in HL.R['toa'] if len(b['r']) >= 3]
    osm_xy = np.array([[c[0] - HL.E0, -(c[1] - HL.N0)] for c, _ in osm])
    special = (MT[::3] == 15) | (MT[::3] == 16)
    sp_h = set(Ht[special].tolist())
    for hid, inf in INFO.items():
        k = inf['k']
        if k not in (1, 3, 4, 10): continue
        if hid in sp_h: continue
        if k == 4:
            if len(nm_xy) and 'ring' in inf:
                rr = np.array(inf['ring'], np.float32).reshape(-1, 1, 2)
                import cv2
                if any(cv2.pointPolygonTest(rr, (float(a), float(b)), False) >= 0 for a, b in nm_xy): continue
            j = int(np.argmin(np.hypot(osm_xy[:, 0] - inf['x'], osm_xy[:, 1] - inf['z']))); lo = f"osm:{osm[j][1]}"
        else:
            if not len(lots_xy): lo = None
            else:
                j = int(np.argmin(np.hypot(lots_xy[:, 0] - inf['x'], lots_xy[:, 1] - inf['z']))); lo = j
        thuong[hid] = dict(k=k, lo=lo, E=round(inf['x'] + HL.E0, 2), N=round(-inf['z'] + HL.N0, 2), y0=round(inf['y0'], 2), y1=round(inf['y1'], 2))
    keep = np.isin(Ht, np.array(sorted(thuong), np.int64))
    hid_t = np.where(keep, Ht, 0).astype(np.float64)
    # mã mặt phẳng: (nhà, pháp tuyến lượng tử 0,05, độ lệch mặt phẳng 0,25 m) → số thứ tự 1…; 0 = không phải nhà thường
    T = P.reshape(-1, 3, 3).astype(np.float64); nrm = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0]); ln = np.linalg.norm(nrm, axis=1); ok = ln > 1e-9
    nrm[ok] /= ln[ok, None]; dd = (nrm * T[:, 0]).sum(1)
    key = np.stack([Ht, np.round(nrm[:, 0] * 20), np.round(nrm[:, 1] * 20), np.round(nrm[:, 2] * 20), np.round(dd / 0.25)], 1).astype(np.int64)
    pid_t = np.zeros(nt, np.float64)
    idx = np.nonzero(keep & ok)[0]
    if len(idx):
        _, inv = np.unique(key[idx], axis=0, return_inverse=True); pid_t[idx] = inv.ravel() + 1
    assert hid_t.max() < 2 ** 24 and pid_t.max() < 2 ** 24
    np.repeat(hid_t, 3).astype(np.float32).tofile(os.path.join(HL.OUT, 'hid.f32'))
    np.repeat(pid_t, 3).astype(np.float32).tofile(os.path.join(HL.OUT, 'pid.f32'))
    json.dump({str(k): v for k, v in thuong.items()}, open(os.path.join(HL.OUT, 'nha.json'), 'w'), ensure_ascii=False)
    st = dict(che_do=MODE, nha_thuong=len(thuong), theo_lop={str(k): sum(1 for v in thuong.values() if v['k'] == k) for k in (1, 3, 4, 10)},
              mat_phang=int(pid_t.max()), toa_co_ten_bo=len(named), tam_giac=int(nt),
              sha_hid=hashlib.sha256(open(os.path.join(HL.OUT, 'hid.f32'), 'rb').read()).hexdigest(), sha_pid=hashlib.sha256(open(os.path.join(HL.OUT, 'pid.f32'), 'rb').read()).hexdigest())
    J = os.path.join(HL.OUT, 'ldn2.json'); meta = json.load(open(J)); meta['thu_b'] = st
    if MODE == 'd':
        meta['phien_ban'] = 'look-v2 + cong-trinh-v2 + THU-B (D) nâng 3D nhà thường'
    json.dump(meta, open(J, 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(st, ensure_ascii=False))


if __name__ == '__main__':
    HL.main()
    J = os.path.join(HL.OUT, 'ldn2.json'); meta = json.load(open(J)); meta['phien_ban'] = 'look-v2 + cong-trinh-v2 (LOOK-T4-V2) — bản THU-B ' + MODE
    json.dump(meta, open(J, 'w'), ensure_ascii=False, indent=1)
    sau_main()
