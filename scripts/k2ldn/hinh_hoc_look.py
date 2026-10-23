#!/opt/cine/bin/python
"""LOOK-T4 · HÌNH HỌC LONDON v2 (chất lượng look, dùng chung cho mọi mốc) — nâng từ hinh_hoc.py (TIEN-KY-T4; dùng lại đầu vào, mặt nạ, trường giờ bén lửa).
  hinh_hoc_look.py   → $LDN_DATA/look/ldn2.bin + ldn2.json + cls66.png/cls26.png (lớp mặt đất) + cay.f32 (cây) + thuyen.json + khoi_bep.f32
Đỉnh: pos(3 f32) · col(3 u8, sRGB albedo) · tl(4 f32 = năm sinh, năm mất, y đáy, giờ bén lửa 1666 | −1) · k(u8 lớp) · uv(2 f32, MÉT trên mặt: u ngang, v cao trên chân)
      · mt(u8 vật liệu) · fl(u8 cờ: 1 = mặt tiền ra phố, 2 = tầng trệt cửa hàng, 4 = mái, 8 = có cửa sổ, 16 = tầng nhô (jetty)).
Lớp k: 1 nhà 1666 · 2 phế tích 1666 · 3 nhà xây lại 1667+ (4 hạng Rebuilding Act) · 4 toà 2026 · 5 công trình có tên · 6 tường thành/kè · 7 cầu
       · 8 nhà thờ giáo xứ 1666 · 9 nhà thờ Wren · 10 khối Victoria–Edward (1840–1940, ước lượng bậc 5) · 11 cầu tàu/bến gỗ.
Vật liệu mt: 0 trát + khung gỗ · 1 gỗ · 2 gạch đỏ 1667 · 3 ngói đất nung · 4 đá phiến · 5 đá thô Trung cổ · 6 đá Portland · 7 kính tường rèm · 8 đá/bê tông văn phòng
       · 9 chì/kim loại · 10 cháy sém · 11 gạch Victoria · 12 mái bằng · 13 kính cửa (ô tối) · 14 gạch ống khói.
Bậc căn cứ (§12.2) ghi trong ldn2.json → 'bac'."""
import json, math, os, sys, hashlib, zlib
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hinh_hoc as H0                        # nạp OSM/LiDAR/Doornick, mặt nạ BUILT/WAT66/WAT26/BURN, t_chay, pho_1666 (không chạy main)
from hinh_hoc import R, BB, E0, N0, G, GW, GH, to_g, poly_mask, at, t_chay, lidar, DTM, DSM, WAT26, WAT66, BURN, BUILT
OUT = os.path.join(H0.DATA, 'look'); os.makedirs(OUT, exist_ok=True)
# bờ bắc 1666 (Fleet → Tower): mặt nạ cháy Doornick bỏ mép sông và nét khắc ven sông thưa → dải ≤ 150 m từ mép nước là kho/bến/nhà dày đặc (Thames Street, Hollar Long View) — bậc 4
_gE = BB[0] + (np.arange(GW) + 0.5) * G; _gN = BB[3] - (np.arange(GH) + 0.5) * G
_dw = cv2.distanceTransform((WAT66 == 0).astype(np.uint8), cv2.DIST_L2, 5) * G
RIV = ((_dw > 3) & (_dw < 150) & (_gE[None, :] > 531650) & (_gE[None, :] < 533450) & (_gN[:, None] > 180550) & (WAT66 == 0)).astype(np.uint8)
BUILT[RIV == 1] = 1
REPO = H0.REPO
RNG = np.random.default_rng(16661)
def L(E, N): return (E - E0, -(N - N0))
def Hg(E, N): return float(np.clip(lidar(DTM, E, N), 0.5, 40.0))

# ------------------------------------------------------------------ bộ dựng lưới có UV mét + vật liệu
class M:
    def __init__(s): s.P, s.C, s.T, s.K, s.UV, s.MT, s.FL = [], [], [], [], [], [], []
    def tri(s, a, b, c, col, tl, k, mt, fl=0, uv=((0, 0), (0, 0), (0, 0))):
        s.P += [a, b, c]; s.C += [col] * 3; s.T += [tl] * 3; s.K += [k] * 3; s.UV += list(uv); s.MT += [mt] * 3; s.FL += [fl] * 3
    def quad(s, a, b, c, d, col, tl, k, mt, fl=0, uv=((0, 0), (1, 0), (1, 1), (0, 1))):
        s.tri(a, b, c, col, tl, k, mt, fl, (uv[0], uv[1], uv[2])); s.tri(a, c, d, col, tl, k, mt, fl, (uv[0], uv[2], uv[3]))
    def wall(s, p0, p1, y0, y1, ybase, col, tl, k, mt, fl=0, u0=0.0):
        """tường thẳng đứng từ p0=(x,z) tới p1 (ngoài nhìn bên PHẢI khi đi p0→p1 theo vòng ngược kim đồng hồ); uv: u mét dọc tường, v mét trên chân ybase."""
        ln = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        s.quad((p0[0], y0, p0[1]), (p1[0], y0, p1[1]), (p1[0], y1, p1[1]), (p0[0], y1, p0[1]), col, tl, k, mt, fl,
               ((u0, y0 - ybase), (u0 + ln, y0 - ybase), (u0 + ln, y1 - ybase), (u0, y1 - ybase)))
    def flat(s, ring, y, col, tl, k, mt, fl=4):
        for i in range(1, len(ring) - 1):
            a, b, c = ring[0], ring[i], ring[i + 1]
            s.tri((a[0], y, a[1]), (b[0], y, b[1]), (c[0], y, c[1]), col, tl, k, mt, fl, ((a[0], a[1]), (b[0], b[1]), (c[0], c[1])))
    def prism(s, ring, y0, y1, ybase, colw, colr, tl, k, mtw, mtr, flw=8, roof_h=None):
        n = len(ring); u = 0.0
        for i in range(n):
            p0, p1 = ring[i], ring[(i + 1) % n]; ln = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
            if roof_h is None: s.wall(p0, p1, y0, y1, ybase, colw, tl, k, mtw, flw, u)
            else:
                h0, h1 = roof_h(p0), roof_h(p1)
                s.quad((p0[0], y0, p0[1]), (p1[0], y0, p1[1]), (p1[0], h1, p1[1]), (p0[0], h0, p0[1]), colw, tl, k, mtw, flw, ((u, y0 - ybase), (u + ln, y0 - ybase), (u + ln, h1 - ybase), (u, h0 - ybase)))
            u += ln
        if roof_h is None: s.flat(ring, y1, colr, tl, k, mtr)
        else:
            for i in range(1, n - 1):
                a, b, c = ring[0], ring[i], ring[i + 1]
                s.tri((a[0], roof_h(a), a[1]), (b[0], roof_h(b), b[1]), (c[0], roof_h(c), c[1]), colr, tl, k, mtr, 4, ((a[0], a[1]), (b[0], b[1]), (c[0], c[1])))
    def house(s, c, u, v, w, d, y0, y1, colw, colr, tl, k, mtw, mtr, roof='front', pitch=50.0, jetty=0.0, fl_front=1, ybase=None):
        """nhà hộp trên lô: c tâm (x,z), u = hướng dọc phố (đơn vị), v = hướng vào lô (từ phố vào trong), w mặt tiền, d sâu.
        roof 'front' = đầu hồi ra phố (nóc vuông góc phố) · 'side' = nóc song song phố · 'hip' = mái bốn dốc · 'flat'.
        jetty > 0: tầng trên nhô ra phố (khối trên lùi về sau không, khối dưới lùi vào jetty m)."""
        yb = y0 if ybase is None else ybase
        cx, cz = c; ux, uz = u; vx, vz = v
        P = lambda a, b: (cx + ux * a + vx * b, cz + uz * a + vz * b)   # a dọc phố [-w/2, w/2], b vào lô [-d/2 (mặt tiền), d/2]
        def body(ya, yb_, front_off, flg):
            ring = [P(-w / 2, -d / 2 + front_off), P(w / 2, -d / 2 + front_off), P(w / 2, d / 2), P(-w / 2, d / 2)]
            names = [fl_front | flg, 0, 0, 0]          # cạnh 0 = mặt tiền ra phố
            uu = 0.0
            for i in range(4):
                p0, p1 = ring[(i + 1) % 4], ring[i]          # đảo chiều để mặt ngoài nhìn ra ngoài (vòng nhìn từ trên)
                s.wall(p0, p1, ya, yb_, yb, colw, tl, k, mtw, 8 | names[i] | (16 if (i == 0 and front_off == 0 and jetty > 0 and ya > y0) else 0), uu); uu += w if i % 2 == 0 else d
            return ring
        if jetty > 0 and y1 - y0 > 4.0:
            gh = min(2.9, (y1 - y0) * 0.45)
            body(y0, y0 + gh, jetty, 2 if fl_front else 0)
            # mặt dưới của phần nhô
            s.quad((*P(-w / 2, -d / 2)[:1], y0 + gh, P(-w / 2, -d / 2)[1]), (P(w / 2, -d / 2)[0], y0 + gh, P(w / 2, -d / 2)[1]),
                   (P(w / 2, -d / 2 + jetty)[0], y0 + gh, P(w / 2, -d / 2 + jetty)[1]), (P(-w / 2, -d / 2 + jetty)[0], y0 + gh, P(-w / 2, -d / 2 + jetty)[1]), colw, tl, k, 1, 0)
            ring = body(y0 + gh, y1, 0.0, 0)
        else:
            ring = body(y0, y1, 0.0, 2 if (fl_front and k in (1, 10)) else 0)
        A, B, C_, D = ring                                   # A,B mặt tiền; C_,D sau
        if roof == 'flat':
            s.flat([A, D, C_, B], y1, colr, tl, k, mtr); return y1
        if roof == 'front':                                  # nóc vuông góc phố: hồi tam giác ở mặt tiền và mặt sau
            rh = (w / 2) * math.tan(math.radians(pitch)); m0 = P(0, -d / 2); m1 = P(0, d / 2)
            Rf, Rb = (m0[0], y1 + rh, m0[1]), (m1[0], y1 + rh, m1[1])
            sl = math.hypot(w / 2, rh)
            s.quad((A[0], y1, A[1]), Rf, Rb, (D[0], y1, D[1]), colr, tl, k, mtr, 4, ((0, 0), (0, sl), (d, sl), (d, 0)))
            s.quad((C_[0], y1, C_[1]), Rb, Rf, (B[0], y1, B[1]), colr, tl, k, mtr, 4, ((0, 0), (0, sl), (d, sl), (d, 0)))
            s.tri((B[0], y1, B[1]), Rf, (A[0], y1, A[1]), colw, tl, k, mtw, 8 | fl_front, ((w, y1 - yb), (w / 2, y1 + rh - yb), (0, y1 - yb)))
            s.tri((D[0], y1, D[1]), Rb, (C_[0], y1, C_[1]), colw, tl, k, mtw, 0, ((0, y1 - yb), (w / 2, y1 + rh - yb), (w, y1 - yb)))
            return y1 + rh
        if roof == 'side':                                   # nóc song song phố
            rh = (d / 2) * math.tan(math.radians(pitch)); m0 = P(-w / 2, 0); m1 = P(w / 2, 0)
            Rl, Rr = (m0[0], y1 + rh, m0[1]), (m1[0], y1 + rh, m1[1]); sl = math.hypot(d / 2, rh)
            s.quad((A[0], y1, A[1]), (B[0], y1, B[1]), Rr, Rl, colr, tl, k, mtr, 4, ((0, 0), (w, 0), (w, sl), (0, sl)))
            s.quad((C_[0], y1, C_[1]), (D[0], y1, D[1]), Rl, Rr, colr, tl, k, mtr, 4, ((0, 0), (w, 0), (w, sl), (0, sl)))
            s.tri((D[0], y1, D[1]), (A[0], y1, A[1]), Rl, colw, tl, k, mtw, 0, ((0, y1 - yb), (d, y1 - yb), (d / 2, y1 + rh - yb)))
            s.tri((B[0], y1, B[1]), (C_[0], y1, C_[1]), Rr, colw, tl, k, mtw, 0, ((0, y1 - yb), (d, y1 - yb), (d / 2, y1 + rh - yb)))
            return y1 + rh
        # hip
        rh = min(w, d) / 2 * math.tan(math.radians(pitch)); cxz = P(0, 0)
        ins = max(0.0, (max(w, d) - min(w, d)) / 2)
        if w >= d: r0, r1 = P(-ins, 0), P(ins, 0)
        else: r0, r1 = P(0, -ins), P(0, ins)
        R0, R1 = (r0[0], y1 + rh, r0[1]), (r1[0], y1 + rh, r1[1])
        if w >= d:
            s.quad((A[0], y1, A[1]), (B[0], y1, B[1]), R1, R0, colr, tl, k, mtr, 4, ((0, 0), (w, 0), (w - ins, 3), (ins, 3)))
            s.quad((C_[0], y1, C_[1]), (D[0], y1, D[1]), R0, R1, colr, tl, k, mtr, 4, ((0, 0), (w, 0), (w - ins, 3), (ins, 3)))
            s.tri((D[0], y1, D[1]), (A[0], y1, A[1]), R0, colr, tl, k, mtr, 4, ((0, 0), (d, 0), (d / 2, 3))); s.tri((B[0], y1, B[1]), (C_[0], y1, C_[1]), R1, colr, tl, k, mtr, 4, ((0, 0), (d, 0), (d / 2, 3)))
        else:
            s.quad((B[0], y1, B[1]), (C_[0], y1, C_[1]), R1, R0, colr, tl, k, mtr, 4, ((0, 0), (d, 0), (d - ins, 3), (ins, 3)))
            s.quad((D[0], y1, D[1]), (A[0], y1, A[1]), R0, R1, colr, tl, k, mtr, 4, ((0, 0), (d, 0), (d - ins, 3), (ins, 3)))
            s.tri((A[0], y1, A[1]), (B[0], y1, B[1]), R0, colr, tl, k, mtr, 4, ((0, 0), (w, 0), (w / 2, 3))); s.tri((C_[0], y1, C_[1]), (D[0], y1, D[1]), R1, colr, tl, k, mtr, 4, ((0, 0), (w, 0), (w / 2, 3)))
        return y1 + rh
    def box(s, cx, cz, w, d, ang, y0, y1, colw, colr, tl, k, mtw, mtr, flw=0, roof='flat', pitch=45.0, ybase=None):
        c, sn = math.cos(ang), math.sin(ang)
        return s.house((cx, cz), (c, sn), (-sn, c), w, d, y0, y1, colw, colr, tl, k, mtw, mtr, roof, pitch, 0.0, flw, ybase)
    def cyl(s, cx, cz, r0, r1, y0, y1, col, tl, k, mt, seg=16, cap=True, fl=0, yb=None):
        yb = y0 if yb is None else yb; circ = 2 * math.pi * max(r0, r1)
        for i in range(seg):
            a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg
            p00 = (cx + r0 * math.cos(a0), y0, cz + r0 * math.sin(a0)); p01 = (cx + r0 * math.cos(a1), y0, cz + r0 * math.sin(a1))
            p10 = (cx + r1 * math.cos(a0), y1, cz + r1 * math.sin(a0)); p11 = (cx + r1 * math.cos(a1), y1, cz + r1 * math.sin(a1))
            u0, u1 = circ * i / seg, circ * (i + 1) / seg
            s.quad(p00, p10, p11, p01, col, tl, k, mt, fl, ((u0, y0 - yb), (u0, y1 - yb), (u1, y1 - yb), (u1, y0 - yb)))
            if cap and r1 > 0: s.tri((cx, y1, cz), p11, p10, col, tl, k, mt, 4, ((cx, cz), (p11[0], p11[2]), (p10[0], p10[2])))
    def lathe(s, cx, cz, prof, col, tl, k, mt, seg=24, fl=0):
        """prof: [(r, y)] từ dưới lên; mặt tròn xoay."""
        for j in range(len(prof) - 1):
            (ra, ya), (rb, yb) = prof[j], prof[j + 1]; s.cyl(cx, cz, ra, rb, ya, yb, col, tl, k, mt, seg, cap=False, fl=fl, yb=prof[0][1])
    def dome(s, cx, cz, r, y0, h, col, tl, k, mt, seg=32, rings=10):
        prof = [(r * math.cos(j / rings * math.pi / 2), y0 + h * math.sin(j / rings * math.pi / 2)) for j in range(rings + 1)]
        s.lathe(cx, cz, prof, col, tl, k, mt, seg)
    def arr(s):
        return (np.array(s.P, np.float32).reshape(-1, 3), np.array(s.C, np.uint8).reshape(-1, 3), np.array(s.T, np.float32).reshape(-1, 4),
                np.array(s.K, np.uint8), np.array(s.UV, np.float32).reshape(-1, 2), np.array(s.MT, np.uint8), np.array(s.FL, np.uint8))

def jit(c, a=10, rng=RNG):
    k = rng.integers(-a, a + 1); return tuple(int(np.clip(v + k + rng.integers(-a // 4, a // 4 + 1), 0, 255)) for v in c)
# bảng albedo (sRGB) — nhân với vân ảnh trong shader (vân mang cấu trúc + một phần sắc độ)
PLASTER = [(214, 204, 182), (206, 192, 160), (196, 186, 168), (222, 214, 196), (190, 170, 138), (200, 178, 150), (176, 168, 156)]   # vôi trắng, vàng đất, xám bẩn
TIMBER = (84, 64, 48); BRICK67 = [(150, 82, 58), (138, 74, 54), (160, 96, 70), (128, 78, 60)]; TILE = [(124, 80, 64), (110, 74, 62), (134, 90, 70), (98, 72, 64), (118, 94, 80), (142, 98, 74), (100, 94, 90)]   # ngói đất nung phong hoá + ám khói than (Evelyn, Fumifugium 1661); 1/7 xám (chì/đá phiến)
STONE = (150, 140, 124); PORTLAND = (222, 216, 202); LEAD = (112, 118, 124); VICT = [(150, 110, 84), (176, 150, 116), (128, 92, 74), (196, 186, 166)]   # STONE: đá Kent (ragstone) + đá Caen ám khói
SLATE = (92, 96, 104)

# ------------------------------------------------------------------ nhà 1666 + nhà xây lại 1667 (4 hạng) theo lô
def lots(streets):
    """sinh lô dọc phố (mặt tiền + chiều sâu) cho nhà 1666; trả danh sách dict lô. Chiếm chỗ trên lưới 2 m để không chồng."""
    occ = np.zeros((GH, GW), np.uint8); occ |= WAT66; out = []
    for l, hw, nm in streets: cv2.polylines(occ, [np.round(to_g(l)).astype(np.int32)], False, 1, thickness=max(1, int(round(2 * hw / G))))   # lòng phố không bị lô của phố khác lấn
    for l, hw, nm in streets:
        seg = np.diff(l, axis=0); ln = np.linalg.norm(seg, axis=1)
        for i in range(len(seg)):
            if ln[i] < 3: continue
            u = seg[i] / ln[i]; v = np.array([-u[1], u[0]]); s = 0.0
            while s < ln[i]:
                r = RNG.random()
                w = float(RNG.uniform(3.4, 4.6) if r < 0.45 else RNG.uniform(4.6, 6.4) if r < 0.88 else RNG.uniform(7.0, 11.0))   # mặt tiền: đa số 1 khoang, ít nhà giàu/quán trọ 2–3 khoang
                for side in (1, -1):
                    for row in (0, 1):
                        if row == 1 and hw < 3: continue
                        d = float(RNG.uniform(8.0, 14.0) if hw >= 4 else RNG.uniform(7.0, 11.0)) if row == 0 else float(RNG.uniform(6.0, 9.0))
                        off = hw + 0.4 + d / 2 if row == 0 else hw + 0.4 + 13.5 + 1.0 + d / 2
                        c = l[i] + u * (s + w / 2) + v * side * off
                        if not (BB[0] + 50 < c[0] < BB[2] - 50 and BB[1] + 50 < c[1] < BB[3] - 50): continue
                        if at(BUILT, c) == 0: continue
                        cs = [c + u * a * w / 2 + v * b * d / 2 for a in (-0.8, 0, 0.8) for b in (-0.8, 0, 0.8)]
                        if sum(at(occ, q) for q in cs) > 1: continue
                        poly = np.array([c + u * (-w / 2) + v * (-d / 2), c + u * (w / 2) + v * (-d / 2), c + u * (w / 2) + v * (d / 2), c + u * (-w / 2) + v * (d / 2)])
                        cv2.fillPoly(occ, [np.round(to_g(poly)).astype(np.int32)], 1)
                        out.append({'c': c, 'u': u, 'v': v * side, 'w': w, 'd': d, 'hw': hw, 'front': row == 0, 'pho': nm})
                s += w
    # lõi khối (sân sau, ngõ không còn trên OSM): nhà nhỏ quay về phố gần nhất; chừa vườn > 45 m từ phố (bậc 5)
    st = np.zeros((GH, GW), np.uint8)
    for l, hw, nm in streets: cv2.polylines(st, [np.round(to_g(l)).astype(np.int32)], False, 1, thickness=max(1, int(2 * hw / G)))
    dt = cv2.distanceTransform(1 - st, cv2.DIST_L2, 5); gy, gx = np.gradient(dt.astype(np.float32))
    for N in np.arange(BB[3] - 60, BB[1] + 60, -7.0):
        for E in np.arange(BB[0] + 60, BB[2] - 60, 7.0):
            c = np.array([E + RNG.uniform(-1.5, 1.5), N + RNG.uniform(-1.5, 1.5)])
            if at(BUILT, c) == 0 or at(occ, c) == 1: continue
            gc = to_g(c); r_, c_ = int(gc[1]), int(gc[0])
            if dt[r_, c_] * G > (110 if RIV[r_, c_] else 45) or RNG.random() < (0.08 if RIV[r_, c_] else 0.2): continue   # ven sông: kho/sân bến dày, không vườn
            nx_, ny_ = gx[r_, c_], -gy[r_, c_]; nn = math.hypot(nx_, ny_) or 1.0; vdir = np.array([-nx_ / nn, -ny_ / nn])   # về phía phố
            udir = np.array([vdir[1], -vdir[0]]); w = float(RNG.uniform(4.0, 6.5)); d = float(RNG.uniform(6.0, 9.0))
            cs = [c + udir * a * w / 2 + vdir * b * d / 2 for a in (-0.8, 0, 0.8) for b in (-0.8, 0, 0.8)]
            if sum(at(occ, q) for q in cs) > 1: continue
            poly = np.array([c - udir * w / 2 - vdir * d / 2, c + udir * w / 2 - vdir * d / 2, c + udir * w / 2 + vdir * d / 2, c - udir * w / 2 + vdir * d / 2])
            cv2.fillPoly(occ, [np.round(to_g(poly)).astype(np.int32)], 1)
            out.append({'c': c, 'u': udir, 'v': -vdir, 'w': w, 'd': d, 'hw': 1.5, 'front': False, 'pho': ''})
    return out, occ

def kho_ven_song(occ):
    """kho/bến/nhà ven sông bờ bắc 1666 (Fleet → Tower) và bờ nam (Bankside): dãy nhà sát kè, đầu hồi ra sông (Hollar Long View 1647; Doornick vẽ dãy nhà sát nước) — bậc 4 hình, bậc 5 lô."""
    out = []; sm = cv2.GaussianBlur((WAT66 > 0).astype(np.float32), (0, 0), 3.0)
    cs, _ = cv2.findContours((sm > 0.5).astype(np.uint8), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    for cnt in cs:
        if len(cnt) < 200: continue
        P = cnt[:, 0, :].astype(float)[::2]; EN = np.stack([BB[0] + (P[:, 0] + 0.5) * G, BB[3] - (P[:, 1] + 0.5) * G], 1)
        acc = 0.0; nxt = 0.0
        for i in range(len(EN) - 1):
            p0, p1 = EN[i], EN[i + 1]; sg = float(np.linalg.norm(p1 - p0)); acc += sg
            if acc < nxt or sg < 0.5: continue
            E, N = p0
            north = 531650 < E < 533450 and N > 180560; south = 531300 < E < 533700 and N < 180560
            if not (north or south): continue
            u = (p1 - p0) / sg; v = np.array([-u[1], u[0]])
            if at(WAT66, p0 + v * 6) == 1: v = -v                                 # v hướng vào đất
            w = float(RNG.uniform(6.0, 12.0)); d = float(RNG.uniform(9.0, 15.0)); c = p0 + u * w / 2 + v * (d / 2 + 2.5)
            nxt = acc + w + float(RNG.uniform(0.0, 1.5))
            cs_ = [c + u * a * w / 2 + v * b * d / 2 for a in (-0.8, 0, 0.8) for b in (-0.8, 0, 0.8)]
            if sum(at(occ, q) for q in cs_) > 1 or at(WAT66, c) == 1: continue
            poly = np.array([c - u * w / 2 - v * d / 2, c + u * w / 2 - v * d / 2, c + u * w / 2 + v * d / 2, c - u * w / 2 + v * d / 2])
            cv2.fillPoly(occ, [np.round(to_g(poly)).astype(np.int32)], 1)
            out.append({'c': c, 'u': u, 'v': v, 'w': w, 'd': d, 'hw': 4.5, 'front': True, 'pho': 'ven sông'})
    return out

def nha(m, LOTS, chim):
    n = {'1666': 0, 'xay_lai': 0, 'phe_tich': 0, 'hang': {1: 0, 2: 0, 3: 0, 4: 0}}
    for lo in LOTS:
        c, w, d, hw = lo['c'], lo['w'], lo['d'], lo['hw']
        x, z = L(*c); g = Hg(*c); burn = float(t_chay(c)[0])
        if burn < 0 and at(RIV, c) == 1: burn = float(np.clip(H0.TFIT(np.atleast_2d(c)), 1.0, 90.0)[0])   # dải ven sông bờ bắc (Thames Street) CHÁY (Pepys/Relation: lửa men theo bờ sông) — mặt nạ Doornick bỏ mép sông
        u = (lo['u'][0], -lo['u'][1]); v = (lo['v'][0], -lo['v'][1])            # (E,N) → (x,z)
        main = hw >= 4.0; mid = hw >= 3.0
        st = int(RNG.choice([2, 3, 3, 4, 4, 5], p=[0.08, 0.27, 0.2, 0.25, 0.12, 0.08])) if main else int(RNG.choice([2, 3, 3, 4], p=[0.25, 0.4, 0.2, 0.15])) if mid else int(RNG.choice([2, 2, 3], p=[0.45, 0.3, 0.25]))
        if not lo['front']: st = min(st, 3)
        y1 = g + st * float(RNG.uniform(2.6, 3.0))
        die = 1666.0 + (245 + burn / 24) / 365.0 if burn >= 0 else 1790.0 + float(RNG.uniform(0, 70))
        r = RNG.random(); mtw = 0 if r < 0.78 else (1 if r < 0.88 else 2)
        colw = jit(PLASTER[RNG.integers(len(PLASTER))], 10) if mtw == 0 else jit(TIMBER, 10) if mtw == 1 else jit(BRICK67[RNG.integers(4)], 8)
        roof = 'front' if (w < 7.0 and RNG.random() < 0.72) else 'side'
        pitch = float(RNG.uniform(46, 56)) if roof == 'front' else float(RNG.uniform(40, 50))
        tl = (1500.0, die, g, burn)
        top = m.house((x, z), u, v, w * 0.985, d, g, y1, colw, jit(TILE[RNG.integers(len(TILE))], 8), tl, 1, mtw, 3, roof, pitch,
                      jetty=float(RNG.uniform(0.35, 0.6)) if (lo['front'] and st >= 3 and mtw != 2) else 0.0, fl_front=1 if lo['front'] else 0)
        n['1666'] += 1
        if RNG.random() < 0.85:                                                   # ống khói gạch trên tường bên/sau
            a = float(RNG.uniform(-0.35, 0.35)) * w; b = d * float(RNG.uniform(0.15, 0.4))
            cx_, cz_ = x + u[0] * a + v[0] * b, z + u[1] * a + v[1] * b; ch = top + float(RNG.uniform(0.8, 1.8))
            m.box(cx_, cz_, 0.9, 1.5, math.atan2(u[1], u[0]), y1 - 1.0, ch, jit((126, 70, 52), 10), jit((60, 50, 46), 6), tl, 1, 14, 14)
            if burn < 0 and RNG.random() < 0.05: chim.append((cx_, ch, cz_, 1500.0, die))
            elif burn >= 0 and RNG.random() < 0.05: chim.append((cx_, ch, cz_, 1500.0, die))
        prev_die = die
        if burn >= 0:
            reb = min(1667.25 + float(RNG.exponential(1.1)), 1672.0)
            # phế tích: tường gạch/đá thấp + ống khói đứng (Evelyn: "nothing but stones…chimneys")
            m.house((x, z), u, v, w * 0.9, d * 0.9, g, g + float(RNG.uniform(0.8, 3.2)), jit((112, 102, 92), 12), jit((70, 62, 56), 8), (die, reb, g, burn), 2, 10, 10, 'flat')
            if RNG.random() < 0.55:
                m.box(x + u[0] * w * 0.3, z + u[1] * w * 0.3, 1.0, 1.5, math.atan2(u[1], u[0]), g, g + float(RNG.uniform(4, 9)), jit((96, 70, 58), 8), jit((60, 50, 46), 6), (die, reb, g, burn), 2, 14, 14)
            n['phe_tich'] += 1
            # Rebuilding Act 1667: 1 = by-lane 2 tầng; 2 = phố/ngõ đáng kể 3 tầng; 3 = phố lớn 4 tầng; 4 = dinh thự (không ra phố) ≤ 4 tầng. Tường gạch, mặt tiền phẳng, nóc song song phố.
            hang = 3 if hw >= 4.5 else 2 if hw >= 3.0 else 1
            if not lo['front'] and w * d > 70: hang = 4
            st2 = {1: 2, 2: 3, 3: 4, 4: 4}[hang]; n['hang'][hang] += 1
            y2 = g + st2 * 3.0 + 1.2                                              # + gác mái thấp + móng cao (hầm)
            die2 = 1830.0 + float(RNG.uniform(0, 75))
            tl2 = (reb, die2, g, -1.0)
            top2 = m.house((x, z), u, v, w * 0.99, d, g, y2, jit(BRICK67[RNG.integers(4)], 8), jit(TILE[RNG.integers(len(TILE))] if RNG.random() < 0.8 else SLATE, 8), tl2, 3, 2, 3, 'side', float(RNG.uniform(36, 44)), 0.0, 1 if lo['front'] else 0)
            m.box(x - u[0] * w * 0.45, z - u[1] * w * 0.45, 0.6, d * 0.5, math.atan2(u[1], u[0]), y2 - 0.5, top2 + 1.2, jit((126, 70, 52), 8), jit((60, 50, 46), 6), tl2, 3, 14, 14)
            if RNG.random() < 0.04: chim.append((x - u[0] * w * 0.45, top2 + 1.2, z - u[1] * w * 0.45, reb, die2))
            n['xay_lai'] += 1; prev_die = die2
        if 530900 < c[0] < 534000 and 179900 < c[1] < 182000:
            s26 = float(at(START_R, c)); vdie = 1940.995 if at(BLITZ_M, c) else (s26 if s26 < 9000 else 1950.0 + float(RNG.uniform(0, 45)))
            if vdie > prev_die + 2:
                stv = int(RNG.choice([3, 4, 4, 5, 5, 6])) if lo['hw'] >= 3 else int(RNG.choice([3, 3, 4, 4, 5])); yv = g + stv * 3.6 + 0.8
                vic = RNG.random() < 0.72
                m.house((x, z), u, v, w * 0.995, d, g, yv, jit(VICT[RNG.integers(4)], 10) if vic else jit(PORTLAND, 6), jit(SLATE, 6), (prev_die, vdie, g, -1.0), 10, 11 if vic else 6, 4 if RNG.random() < 0.7 else 12,
                        'side' if RNG.random() < 0.6 else 'flat', float(RNG.uniform(28, 38)), 0.0, 1 if lo['front'] else 0)
                n['vict'] = n.get('vict', 0) + 1
    return n

# ------------------------------------------------------------------ vùng bom 29/12/1940 (D15: mô tả văn bản → ranh vẽ tay, ƯỚC LƯỢNG bậc 5)
# Văn bản đã xác minh (DU-KIEN-MOI, TIEN-KY-T4): Paternoster Row + quanh St Paul's, Cripplegate/Aldersgate/Barbican, Moorgate; không dùng LCC Bomb Damage Maps.
BLITZ = [(531980, 181120), (531900, 181250), (531960, 181420), (532080, 181560), (532200, 181760), (532420, 181800), (532640, 181720), (532760, 181560),
         (532720, 181400), (532560, 181300), (532380, 181220), (532230, 181150), (532120, 181100)]
BLITZ_M = poly_mask([BLITZ])

# ------------------------------------------------------------------ toà 2026 + khối Victoria tiền nhiệm
START = {}; START_R = None
def toa_start():
    """năm dựng mỗi toà OSM 2026 (start_date nếu có; thiếu → 1950–2020 trong vùng bom 1940, 1955–2020 nơi khác; > 120 m → ≥ 1995) + raster 2 m (năm dựng nhỏ nhất phủ ô)."""
    global START_R
    rs = np.random.default_rng(2026); START_R = np.full((GH, GW), 9999.0, np.float32)
    for b in R['toa']:
        r = np.array(b['r'], float)
        if len(r) < 3: continue
        c = r.mean(0); st = None
        try: st = float(int(str(b.get('start') or '')[:4]))
        except Exception: pass
        if st is None: st = (1950.0 + rs.uniform(0, 70)) if at(BLITZ_M, c) else (1955.0 + rs.uniform(0, 65))
        if (b['h'] or 0) > 120: st = max(st, 1995.0 + rs.uniform(0, 25))
        st = max(st, 1667.5); START[b['id']] = st
    for b in sorted([b for b in R['toa'] if not b['part'] and b['id'] in START], key=lambda b: -START[b['id']]):   # vẽ từ muộn → sớm: ô giữ năm NHỎ nhất
        cv2.fillPoly(START_R, [np.round(to_g(np.array(b['r'], float)) * 4).astype(np.int32)], float(START[b['id']]), shift=2)
def special(name, c):
    if name == 'The Leadenhall Building' or np.hypot(c[0] - 533166, c[1] - 181190) < 35: return 'leadenhall'
    if name == '30 St Mary Axe' or np.hypot(c[0] - 533301, c[1] - 181252) < 25: return 'gherkin'
    return None
def toa(m):
    """toà OSM: bỏ mọi đường bao/phần nằm trong St Paul's (dựng tham số riêng) và trong Tower of London (dựng riêng); nhà thờ/nhà nguyện OSM = đá, có từ trước (không thành khối văn phòng)."""
    n = {'2026': 0, 'vict': 0, 'lidar': 0, 'bo_trung_cong_trinh': 0, 'nha_tho_osm': 0}
    RT = np.random.default_rng(2027); jitT = lambda c, a=10: jit(c, a, RT)                                       # bộ sinh riêng: thứ tự toà không làm lệch phần hình học khác
    spC = next(np.array(b["r"], float) for b in R["toa"] if b["name"] == "St Paul's Cathedral").astype(np.float32).reshape(-1, 1, 2)
    parts = [b for b in R['toa'] if b['part']]
    pc = np.array([np.mean(np.array(b['r'], float), 0) for b in parts]) if parts else np.zeros((0, 2))
    for b in R['toa']:
        r = np.array(b['r'], float)
        if len(r) > 3 and np.allclose(r[0], r[-1]): r = r[:-1]
        if len(r) < 3: continue
        c = r.mean(0)
        if not (BB[0] + 30 < c[0] < BB[2] - 30 and BB[1] + 30 < c[1] < BB[3] - 30): continue
        if b['name'] in ("St Paul's Cathedral",) or cv2.pointPolygonTest(spC, (float(c[0]), float(c[1])), True) > -6 or np.hypot(c[0] - 533612, c[1] - 180555) < 60:
            n['bo_trung_cong_trinh'] += 1; continue
        area = 0.5 * abs(np.dot(r[:, 0], np.roll(r[:, 1], 1)) - np.dot(r[:, 1], np.roll(r[:, 0], 1)))
        if area < 12: continue
        if not b['part'] and len(pc):                                             # đường bao có building:part bên trong → chỉ dựng phần (luật OSM 3D)
            inside = cv2.pointPolygonTest(r.astype(np.float32).reshape(-1, 1, 2), (0, 0), False) if False else None
            near = pc[np.hypot(pc[:, 0] - c[0], pc[:, 1] - c[1]) < np.sqrt(area)]
            if len(near) and any(cv2.pointPolygonTest(r.astype(np.float32).reshape(-1, 1, 2), (float(p[0]), float(p[1])), False) >= 0 for p in near): continue
        sp = special(b['name'], c)
        if sp == 'gherkin' and not b['part']: continue
        g = Hg(*c); h = b['h']
        if not h:
            qs = np.array([c] + [c * 0.4 + p * 0.6 for p in r[:: max(1, len(r) // 8)]])
            hh = lidar(DSM, qs[:, 0], qs[:, 1]) - lidar(DTM, qs[:, 0], qs[:, 1]); h = float(np.clip(np.median(hh), 3.0, 320.0)); n['lidar'] += 1
        y0 = g + (b['minh'] or 0.0) if b['part'] else g
        ring = [L(*p) for p in r]
        sa = sum(ring[i][0] * ring[(i + 1) % len(ring)][1] - ring[(i + 1) % len(ring)][0] * ring[i][1] for i in range(len(ring)))
        if sa < 0: ring = ring[::-1]
        start = START[b['id']]
        hs = (zlib.crc32(str(b['id']).encode()) % 1000) / 1000.0
        if b['b'] in ('church', 'cathedral', 'chapel') and not b['part']:
            burnt = at(BURN, c) == 1                                             # trong vùng cháy: nhà thờ OSM là bản dựng lại sau 1666 (Wren) — không có trong cảnh 1666
            st0 = start if start < 1900 else ((1677.0 + RT.uniform(0, 25)) if burnt else 1200.0)
            m.prism(ring[::-1], y0, g + min(h, 30.0), y0, jitT(PORTLAND if burnt else STONE, 8), jitT(LEAD, 6), (st0, 9999.0, y0, -1.0), 9 if burnt else 8, 6 if burnt else 5, 9, 0); n['nha_tho_osm'] += 1; continue
        tall = h > 60
        if tall: mtw, colw = (7, jitT((120, 138, 150), 8)) if hs < 0.8 else (8, jitT((196, 192, 182), 8))
        elif start < 1914: mtw, colw = (6, jitT(PORTLAND, 6)) if hs < 0.45 else (11, jitT(VICT[int(hs * 40) % 4], 8))
        else:
            mtw = 8 if hs < 0.40 else 7 if hs < 0.62 else 11 if hs < 0.80 else 6
            colw = jitT([(190, 186, 176), (130, 146, 156), (150, 108, 84), PORTLAND][[8, 7, 11, 6].index(mtw)], 8)
        tl = (start, 9999.0, y0, -1.0)
        if sp == 'gherkin':
            cx, cz = L(*c); prof = [(24.5, g), (27.0, g + 40), (28.5, g + 70), (27.5, g + 100), (24.0, g + 130), (18.0, g + 155), (10.0, g + 172), (3.0, g + 179), (0.1, g + 180)]
            m.lathe(cx, cz, prof, jitT((90, 110, 124), 6), (2003.0, 9999.0, g, -1.0), 4, 7, 32, fl=8); n['2026'] += 1; continue
        if sp == 'leadenhall':
            Nmax = r[:, 1].max(); topH = g + h
            rh = lambda p: max(y0 + 6.0, min(topH, topH - (Nmax - (-(p[1]) + N0)) * 4.2))
            m.prism(ring[::-1], y0, topH, y0, colw, jitT((80, 86, 92), 6), tl, 4, 7, 7, 8, roof_h=rh); n['2026'] += 1; continue
        m.prism(ring[::-1], y0, g + h, y0, colw, jitT((112, 112, 110), 8), tl, 4, mtw, 12, 8)
        n['2026'] += 1
        # tiền nhiệm Victoria–Edward (1840–1940) trên cùng nền nếu toà 2026 dựng sau 1940 — thành phố 1940 dày đặc (bậc 5)
        if False:
            hv = float(RT.uniform(14, 24)); vstart = 1845.0 + float(RT.uniform(0, 60))
            vdie = 1940.995 if at(BLITZ_M, c) else start
            m.prism(ring[::-1], g, g + hv, g, jitT(VICT[int(hs * 97) % 4], 10), jitT(SLATE, 6), (vstart, max(vdie, vstart + 1), g, -1.0), 10, 11 if hs < 0.6 else 6, 4, 8)
            n['vict'] += 1
    return n

# ------------------------------------------------------------------ công trình có tên
def axis_of(name):
    for b in R['toa']:
        if b['name'] == name:
            r = np.array(b['r'], float); c = r.mean(0); X = r - c; w, V = np.linalg.eigh(X.T @ X); return c, V[:, 1], r
def frame_of(c, ax):
    ang = math.atan2(-ax[1], ax[0]); cxz = L(*c)
    P = lambda u, v: (cxz[0] + math.cos(ang) * u - math.sin(ang) * v, cxz[1] + math.sin(ang) * u + math.cos(ang) * v)
    return ang, P
def st_pauls_wren(m):
    """St Paul's (Wren, 1675–1711). Số đo: dài 158 m (518 ft) / 175 m gồm bậc portico; ngang cánh 75 m (246 ft); thân + gian bên 37 m (121 ft); tường ≈ 33,5 m (110 ft) tới lan can;
    giao điểm–tây 68 m + bát giác ≈ 34 m + hợp xướng 51 m; tới thập giá 111 m (365 ft) (Fletcher 1962 qua Wikipedia) — bậc 3. Tháp tây ≈ 65 m (212 ft), trống 32 cột — bậc 4."""
    c, ax, _ = axis_of("St Paul's Cathedral"); ax = ax if ax[0] > 0 else -ax; ang, P = frame_of(c, ax); g = Hg(*c)
    pc = PORTLAND; t = (1675.5, 9999.0, g, -1.0); t2 = (1697.0, 9999.0, g, -1.0); t3 = (1708.8, 9999.0, g, -1.0)
    def B(u, v, w, d, y0, y1, roof='flat', pitch=0, tl=t, col=pc, colr=None, mt=6, mtr=9):
        x, z = P(u, v); return m.box(x, z, w, d, ang, g + y0, g + y1, jit(col, 3), jit(colr or LEAD, 3), tl, 5, mt, mtr, 8, roof, pitch, ybase=g)
    B(-51, 0, 68, 37, 0, 27.5); B(-51, 0, 64, 15, 27.5, 33.5, 'side', 22)          # thân tây: tường màn 2 tầng tới lan can; mái chì trên gian giữa
    B(42, 0, 51, 37, 0, 27.5); B(42, 0, 51, 15, 27.5, 33.5, 'side', 22)            # hợp xướng
    x, z = P(70, 0); m.cyl(x, z, 9.0, 9.0, g, g + 24, pc, t, 5, 6, 16, fl=8); m.dome(x, z, 9.0, g + 24, 6, LEAD, t, 5, 9, 16, 4)   # apse
    B(0, 0, 34, 75, 0, 27.5); B(0, 0, 15, 70, 27.5, 33.5, 'side', 22)              # cánh ngang + giao điểm
    for s_ in (-1, 1):
        x, z = P(0, s_ * 39.0); m.cyl(x, z, 6.5, 6.5, g, g + 14, pc, t, 5, 6, 16, fl=8); m.dome(x, z, 6.5, g + 14, 3, LEAD, t, 5, 9, 16, 3)   # portico bán nguyệt
        B(-86, s_ * 13.5, 12, 12, 0, 33.5, tl=t2); xx, zz = P(-86, s_ * 13.5)                                       # tháp tây
        m.cyl(xx, zz, 5.5, 5.5, g + 33.5, g + 48, pc, t2, 5, 6, 12, fl=8); m.cyl(xx, zz, 4.2, 4.2, g + 48, g + 55, pc, t2, 5, 6, 12)
        m.dome(xx, zz, 4.2, g + 55, 4.0, LEAD, t2, 5, 9, 12, 3); m.cyl(xx, zz, 1.2, 0.2, g + 59, g + 65, (200, 170, 90), t2, 5, 9, 8)
    B(-86, 0, 12, 15, 0, 33.5, tl=t2); B(-95.5, 0, 7, 30, 0, 20.5); B(-95.5, 0, 7, 22, 20.5, 33.0); B(-95.5, 0, 7, 22, 33.0, 39.0, 'side', 18)   # portico 2 tầng + trán
    x, z = P(-101, 0); m.box(x, z, 8, 34, ang, g, g + 1.6, (190, 186, 176), (190, 186, 176), t, 5, 6, 6)   # bậc
    x, z = P(0, 0)
    m.cyl(x, z, 21.5, 21.5, g + 33.5, g + 36.0, pc, t2, 5, 6, 48)                               # chân trống
    for i in range(32):                                                                           # hàng 32 cột (peristyle)
        a = 2 * math.pi * i / 32; m.cyl(x + 21.0 * math.cos(a), z + 21.0 * math.sin(a), 0.9, 0.9, g + 36.0, g + 49.5, pc, t2, 5, 6, 6, cap=False)
    m.cyl(x, z, 17.5, 17.5, g + 36.0, g + 49.5, (150, 146, 138), t2, 5, 6, 48, cap=False, fl=0)   # tường trống sau hàng cột (trong bóng hàng cột)
    m.cyl(x, z, 21.8, 21.8, g + 49.5, g + 51.5, pc, t2, 5, 6, 48)                                # gờ + lan can
    m.cyl(x, z, 16.8, 16.8, g + 51.5, g + 60.0, pc, t2, 5, 6, 48, cap=False, fl=8)               # tầng gác (attic)
    m.lathe(x, z, [(16.8, g + 60.0), (16.6, g + 64.0), (15.6, g + 70.0), (13.4, g + 76.0), (10.0, g + 81.5), (5.6, g + 85.5), (3.4, g + 86.6)], (78, 79, 77), t3, 5, 9, 48)   # chì phong hoá xám sẫm (không ngả lam)
    m.cyl(x, z, 3.6, 3.6, g + 86.6, g + 97.0, pc, t3, 5, 6, 16, fl=8)                            # đèn lồng
    m.lathe(x, z, [(3.6, g + 97.0), (2.6, g + 100.0), (1.2, g + 103.0), (0.5, g + 106.0)], jit(LEAD, 2), t3, 5, 9, 16)
    m.lathe(x, z, [(0.01, g + 106.0), (1.0, g + 106.6), (1.0, g + 107.4), (0.01, g + 108.0)], (214, 176, 84), t3, 5, 9, 12)   # quả cầu mạ vàng
    m.box(x, z, 0.4, 0.4, ang, g + 108.0, g + 111.0, (214, 176, 84), (214, 176, 84), t3, 5, 9, 9); m.box(x, z, 1.8, 0.35, ang, g + 109.6, g + 110.1, (214, 176, 84), (214, 176, 84), t3, 5, 9, 9)
    return c
def st_pauls_old(m):
    """Old St Paul's theo Hollar/Dugdale 1658 (Met 336039 mặt nam, 395057 mặt đông): dài 586 ft ≈ 179 m (không kể portico Inigo Jones), thân 100 ft ≈ 30 m,
    ngang cánh 290 ft ≈ 88 m (Clifton-Taylor tr. 275, qua Wikipedia — bậc 3); tháp giao điểm 204 ft ≈ 62 m (Hooke 1664, Jardine 2001 — bậc 2/3), không chóp từ 1561.
    Tỉ lệ tầng (gian bên 18 m, lan can cửa sổ cao 30 m, nóc 40 m), số khoang (thân 12, hợp xướng 12), cửa sổ tròn thân tây (Inigo Jones bọc lại), portico tây 10 cột — đo trên bản khắc (bậc 4)."""
    c, ax, _ = axis_of("St Paul's Cathedral"); ax = ax if ax[0] > 0 else -ax; c = c + ax * 18.0; ang, P = frame_of(c, ax); g = Hg(*c)
    burn = float(t_chay(c)[0]); die = 1666.0 + (245 + burn / 24) / 365.0
    st = STONE; t = (1300.0, die, g, burn); tr = (die, 1675.4, g, burn)
    def B(u, v, w, d, y0, y1, roof='flat', pitch=0, tl=t, col=st, colr=LEAD, mt=5, mtr=9, fl=8):
        x, z = P(u, v); return m.box(x, z, w, d, ang, g + y0, g + y1, jit(col, 4), jit(colr, 4), tl, 5, mt, mtr, fl, roof, pitch, ybase=g)
    def W(u, v, w, h, y, side):                                    # cửa sổ: tấm tối áp sát mặt tường (side ±1 = phía bắc/nam)
        x0, z0 = P(u - w / 2, v + side * 0.08); x1, z1 = P(u + w / 2, v + side * 0.08)
        a, b = ((x0, z0), (x1, z1)) if side > 0 else ((x1, z1), (x0, z0))
        m.wall(a, b, g + y, g + y + h, g, (34, 32, 34), t, 5, 13, 0)
    # thân tây (Romanesque, bọc lại cổ điển): u −93…−12; hợp xướng Gothic: u 12…86; cánh ngang u −12…12, v ±44
    B(-52.5, 0, 81, 13, 0, 30, 'side', 52); B(-52.5, -11.0, 81, 9, 0, 18, 'side', 18); B(-52.5, 11.0, 81, 9, 0, 18, 'side', 18)
    B(49.0, 0, 74, 13, 0, 31, 'side', 52); B(49.0, -11.0, 74, 9, 0, 19, 'side', 18); B(49.0, 11.0, 74, 9, 0, 19, 'side', 18)
    B(0, 0, 24, 88, 0, 30, 'front', 52)
    for side in (-1, 1):
        for i in range(12):                                         # thân tây: cửa sổ tròn gian bên + cửa sổ vòm cao
            u = -90 + i * 6.6; W(u, side * 15.5, 1.8, 1.8, 10.5, side); W(u, side * 6.5, 2.0, 4.0, 22.5, side)
            if i % 2 == 0: B(u + 3.3, side * 16.0, 1.2, 1.2, 0, 19.5)                                       # trụ áp
        for i in range(12):                                         # hợp xướng Gothic: cửa sổ nhọn 2 tầng + trụ bay có chóp
            u = 15 + i * 6.0; W(u, side * 15.5, 2.6, 7.5, 6.5, side); W(u, side * 6.5, 3.0, 8.0, 20.5, side)
            B(u + 3.0, side * 16.6, 1.6, 2.2, 0, 21); x, z = P(u + 3.0, side * 16.6); m.cyl(x, z, 0.8, 0.05, g + 21, g + 25.5, jit(st, 4), t, 5, 5, 6)
            B(u + 3.0, side * 11.0, 0.5, 9.0, 23, 24.6)                                                       # cầu trụ bay (thanh nghiêng ước)
        W(0, side * 44.1, 7.0, 7.0, 13.0, side); W(0, side * 44.1, 3.2, 6.0, 4.0, side)                       # hồi cánh ngang: cửa sổ tròn + cửa
        for uu in (-12.6, 12.6):
            B(uu, side * 43.0, 2.4, 2.4, 0, 33); x, z = P(uu, side * 43.0); m.cyl(x, z, 1.1, 0.05, g + 33, g + 41, jit(st, 4), t, 5, 5, 8)
    # mặt đông: cửa sổ hoa hồng + 7 cửa sổ nhọn (Hollar 2010.529), tháp nhọn góc
    x0, z0 = P(86.1, -5.5); x1, z1 = P(86.1, 5.5)
    m.wall((x0, z0), (x1, z1), g + 4.0, g + 17.0, g, (34, 32, 34), t, 5, 13, 0)
    xr, zr = P(86.12, 0); m.cyl(xr, zr, 4.6, 4.6, g + 20.0, g + 20.3, (30, 28, 32), t, 5, 13, 24)
    for vv in (-15.5, -6.5, 6.5, 15.5):
        B(86.0, vv, 2.4, 2.4, 0, 36 if abs(vv) < 10 else 22); x, z = P(86.0, vv); m.cyl(x, z, 1.1, 0.05, g + (36 if abs(vv) < 10 else 22), g + (45 if abs(vv) < 10 else 28), jit(st, 4), t, 5, 5, 8)
    # tháp giao điểm: thân 20 m vuông tới 58 m, lan can + 4 chóp góc tới 62–66 m; hai tầng cửa sổ nhọn mỗi mặt
    B(0, 0, 20, 20, 30, 58.5); B(0, 0, 21, 21, 58.5, 60.0)
    for a_, b_ in ((-9.8, -9.8), (9.8, -9.8), (9.8, 9.8), (-9.8, 9.8)):
        B(a_, b_, 2.6, 2.6, 30, 60.5); x, z = P(a_, b_); m.cyl(x, z, 1.3, 0.1, g + 60.5, g + 66.0, jit(st, 4), t, 5, 5, 8)
    for side in (-1, 1):
        for k_ in (-4.5, 0, 4.5):
            W(k_, side * 10.1, 2.2, 9.0, 33.0, side); W(k_, side * 10.1, 2.2, 10.0, 45.0, side)
        for k_ in (-4.5, 0, 4.5):
            xa, za = P(side * 10.1, k_ - 1.1); xb, zb = P(side * 10.1, k_ + 1.1)
            a, b = ((xa, za), (xb, zb)) if side < 0 else ((xb, zb), (xa, za))
            m.wall(a, b, g + 33.0, g + 42.0, g, (34, 32, 34), t, 5, 13, 0); m.wall(a, b, g + 45.0, g + 55.0, g, (34, 32, 34), t, 5, 13, 0)
    # portico Inigo Jones (thập niên 1630): 10 cột Corinth cao ≈ 17 m, rộng ≈ 50 m; mặt tây + 2 tháp nhỏ
    B(-95.0, 0, 6.0, 30, 0, 30, 'front', 45); B(-101.5, 0, 9.0, 50, 15.5, 18.5)
    for i in range(10):
        x, z = P(-104.8, -22.5 + i * 5.0); m.cyl(x, z, 0.85, 0.75, g, g + 15.5, PORTLAND, t, 5, 6, 10, cap=False)
    for vv in (-14.0, 14.0):
        B(-92.0, vv, 4.5, 4.5, 0, 27); x, z = P(-92.0, vv); m.cyl(x, z, 2.2, 0.1, g + 27, g + 36, jit(LEAD, 4), t, 5, 9, 8)
    # nhà thờ St Gregory áp góc tây nam (Hollar 336039): thân + tháp vuông chóp
    B(-84.0, -24.0, 16, 9, 0, 9, 'side', 30, col=(190, 182, 166)); B(-92.0, -24.0, 6, 6, 0, 17, col=(190, 182, 166)); x, z = P(-92.0, -24.0); m.cyl(x, z, 3.2, 0.2, g + 17, g + 23, jit(LEAD, 4), t, 5, 9, 8)
    # phế tích sau 4–7/9/1666 (mái sập, tường đứng; Relation a19): vỏ tường + tháp cụt, cháy sém
    for (u, w_, h_) in ((-52.5, 81, 18), (49.0, 74, 19)):
        for vv in (-15.4, 15.4): B(u, vv, w_, 1.2, 0, h_, tl=tr, col=(120, 108, 96), mt=10, colr=(80, 72, 66), mtr=10)
    B(0, 0, 20, 20, 0, 44, tl=tr, col=(116, 104, 94), mt=10, colr=(80, 72, 66), mtr=10)
    for vv in (-44, 44): B(0, vv, 24, 1.2, 0, 26, tl=tr, col=(120, 108, 96), mt=10, colr=(80, 72, 66), mtr=10)
    return c
def tower_of_london(m):
    c = np.array([533612.0, 180555.0]); g = Hg(*c); x, z = L(*c); tl = (1100.0, 9999.0, g, -1.0)
    m.box(x, z, 36, 32, math.radians(-10), g, g + 27, jit(STONE, 6), jit(LEAD, 4), tl, 5, 5, 9, 8)
    for a, b in ((-17, -15), (17, -15), (17, 15)):
        m.cyl(x + a, z + b, 3.0, 3.0, g + 27, g + 33, jit(STONE, 4), tl, 5, 5, 10); m.cyl(x + a, z + b, 3.2, 0.5, g + 33, g + 36.5, jit(LEAD, 4), tl, 5, 9, 10)
    m.cyl(x - 17, z + 15, 4.5, 4.5, g + 27, g + 33, jit(STONE, 4), tl, 5, 5, 12); m.dome(x - 17, z + 15, 4.6, g + 33, 3.0, LEAD, tl, 5, 9, 12, 3)
    for half, hh in ((118, 11), (92, 15)):
        pts = [(x - half, z - half), (x + half, z - half), (x + half, z + half), (x - half, z + half)]
        for i in range(4):
            (ax_, az), (bx, bz) = pts[i], pts[(i + 1) % 4]; L_ = math.hypot(bx - ax_, bz - az)
            m.box((ax_ + bx) / 2, (az + bz) / 2, L_, 3.5, math.atan2(bz - az, bx - ax_), g, g + hh, jit(STONE, 6), jit(STONE, 6), tl, 6, 5, 5)
            m.cyl(ax_, az, 6, 6, g, g + hh + 4, jit(STONE, 6), tl, 6, 5, 12)
def monument(m):
    c = np.array([532990.0, 180750.0]); g = Hg(*c); x, z = L(*c)
    m.box(x, z, 8.5, 8.5, 0, g, g + 12, PORTLAND, PORTLAND, (1671.5, 9999.0, g, -1.0), 5, 6, 6)
    m.cyl(x, z, 2.4, 2.2, g + 12, g + 52, PORTLAND, (1672.5, 9999.0, g, -1.0), 5, 6, 20)
    m.box(x, z, 5.0, 5.0, 0, g + 52, g + 55, PORTLAND, PORTLAND, (1676.5, 9999.0, g, -1.0), 5, 6, 6)
    m.lathe(x, z, [(1.4, g + 55), (1.0, g + 57), (1.3, g + 59), (0.5, g + 61), (0.05, g + 61.5)], (214, 170, 70), (1676.9, 9999.0, g, -1.0), 5, 9, 12)
def london_bridge_old(m):
    """Cầu London Trung cổ (1209–1831): 19 vòm trên trụ có 'starling' (đảo đá nhọn), dãy nhà 4–6 tầng nhô hai bên lòng cầu ≈ 4 m; Nonsuch House (gỗ, 1579) ở đoạn giữa-nam;
    khoảng trống phía bắc do cháy 13/2/1633 (Relation a23) — theo Hollar Long View / Prospects (Met 17.50.100, CC0) bậc 4; vị trí khoảng trống trong đoạn bậc 5."""
    a = np.array([532905.0, 180640.0]); b = np.array([532840.0, 180370.0]); g = 6.5
    u = (b - a) / np.linalg.norm(b - a); v = np.array([-u[1], u[0]]); Ln = float(np.linalg.norm(b - a))
    uxz = (u[0], -u[1]); vxz = (v[0], -v[1]); ang = math.atan2(uxz[1], uxz[0]); tl = (1209.0, 1831.5, 0.0, -1.0)
    x, z = L(*((a + b) / 2)); m.box(x, z, Ln, 13, ang, 3.0, g, jit(STONE, 5), jit((120, 110, 98), 6), tl, 7, 5, 5)
    for i in range(20):                                             # trụ + starling (nhọn hai đầu theo dòng chảy)
        p = a + u * (6 + i * (Ln - 12) / 19); x, z = L(*p)
        m.box(x, z, 7.5, 13.5, ang, -2.5, 3.2, jit(STONE, 6), jit(STONE, 6), tl, 7, 5, 5)
        m.box(x, z, 10.0, 22.0, ang, -2.5, 0.9, jit((112, 104, 92), 6), jit((112, 104, 92), 6), tl, 7, 5, 5, roof='hip', pitch=20)
    s = 4.0; hs = {}
    while s < Ln - 6:
        w = float(RNG.uniform(5, 8))
        gap = 22 < s < 95                                           # khoảng trống 1633 (đoạn bắc)
        if not gap:
            for side in (1, -1):
                p = a + u * (s + w / 2) + v * side * 4.6; x, z = L(*p)
                st = int(RNG.integers(4, 7)); y1 = g + st * 2.7
                m.house((x, z), uxz, (vxz[0] * side, vxz[1] * side), w * 0.97, 6.0, g, y1, jit(PLASTER[RNG.integers(len(PLASTER))], 10), jit(TILE[RNG.integers(len(TILE))], 8), tl, 7, 0, 3,
                        'front', 50, 0.0, 1)
                # nhô ra sông trên chân gỗ (mặt sau nhà vượt mép cầu)
                pq = a + u * (s + w / 2) + v * side * 8.6; xq, zq = L(*pq)
                m.box(xq, zq, w * 0.95, 2.4, ang, g - 1.6, y1 - 1.0, jit((96, 76, 58), 8), jit(TILE[0], 8), tl, 7, 1, 3)
        s += w
    # Nonsuch House (gỗ sơn, 4 tháp hành củ hành) ≈ 1/3 từ nam
    p = a + u * (Ln * 0.66); x, z = L(*p); m.box(x, z, 24, 13, ang, g, g + 17, (220, 210, 188), jit(LEAD, 4), tl, 7, 0, 9, 8)
    for da, db in ((-11, -6), (11, -6), (11, 6), (-11, 6)):
        q = p + u * da + v * db; xq, zq = L(*q); m.cyl(xq, zq, 2.0, 2.0, g + 17, g + 20, (220, 210, 188), tl, 7, 0, 10); m.dome(xq, zq, 2.0, g + 20, 3.0, LEAD, tl, 7, 9, 10, 3)
def quays(m, WAT, year0, year1, kind):
    """bờ sông theo đường mép nước (mịn): 1666–1864 kè/bến gỗ + cầu thang nước (water stairs); 1870+ tường Embankment granite."""
    sm = cv2.GaussianBlur((WAT > 0).astype(np.float32), (0, 0), 3.0)
    cs, _ = cv2.findContours((sm > 0.5).astype(np.uint8), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    n = 0
    for cnt in cs:
        if len(cnt) < 200: continue
        P = cnt[:, 0, :].astype(float); P = cv2.GaussianBlur(P.reshape(-1, 1, 2), (1, 0), 4.0).reshape(-1, 2) if len(P) > 30 else P
        P = P[::3]
        EN = np.stack([BB[0] + (P[:, 0] + 0.5) * G, BB[3] - (P[:, 1] + 0.5) * G], 1)
        keep = (EN[:, 0] > 530200) & (EN[:, 0] < 534800) & (EN[:, 1] > 179900) & (EN[:, 1] < 181200)
        acc = 0.0
        for i in range(len(EN) - 1):
            if not (keep[i] and keep[i + 1]): continue
            p0, p1 = EN[i], EN[i + 1]; seg = np.linalg.norm(p1 - p0)
            if seg < 0.5 or seg > 20: continue
            a, b = L(*p0), L(*p1)
            if kind == 'go':
                m.wall(a, b, -2.0, 2.4, -2.0, jit((92, 74, 56), 8), (year0, year1, -2.0, -1.0), 11, 1, 0, acc)
            else:
                m.wall(a, b, -2.0, 4.4, -2.0, jit((176, 172, 162), 5), (year0, year1, -2.0, -1.0), 6, 5, 0, acc)
            acc += seg; n += 1
            if kind == 'go' and RNG.random() < 0.018:              # cầu thang nước / cầu tàu gỗ nhô ra sông
                d = np.array([p1[1] - p0[1], -(p1[0] - p0[0])]) / seg
                if at(WAT, p0 + d * 8) == 0: d = -d
                q = p0 + d * float(RNG.uniform(6, 14)); x, z = L(*q); ang = math.atan2(-d[1], d[0])
                m.box(x, z, float(np.linalg.norm(q - p0)) * 2, 3.0, ang, -1.5, 1.6, jit((96, 78, 60), 8), jit((112, 92, 70), 8), (year0, year1, -1.5, -1.0), 11, 1, 1)
    return n
def tuong_thanh(m):
    pts = [(533560, 180700), (533590, 180950), (533540, 181160), (533380, 181330), (533196, 181431), (532900, 181530), (532697, 181548), (532450, 181610), (532300, 181620), (532170, 181520),
           (532145, 181465), (531900, 181430), (531796, 181409), (531780, 181280), (531760, 181158), (531700, 181000), (531660, 180830)]
    tl = (1200.0, 1766.0, 0.0, -1.0)
    for i in range(len(pts) - 1):
        a, b = np.array(pts[i], float), np.array(pts[i + 1], float); c = (a + b) / 2; g = Hg(*c); x, z = L(*c)
        m.box(x, z, float(np.linalg.norm(b - a)), 2.6, math.atan2(-(b - a)[1], (b - a)[0]), g, g + 7, jit(STONE, 8), jit(STONE, 8), tl, 6, 5, 5)
    for nm, E, N in [('Aldgate', 533540, 181160), ('Bishopsgate', 533196, 181431), ('Moorgate', 532697, 181548), ('Cripplegate', 532330, 181620), ('Aldersgate', 532145, 181465), ('Newgate', 531796, 181409), ('Ludgate', 531760, 181158)]:
        g = Hg(E, N); x, z = L(E, N); m.box(x, z, 14, 10, 0, g, g + 13, jit(STONE, 8), jit(LEAD, 6), tl, 6, 5, 9, 0, 'side', 30)

def nha_tho(m, sites):
    """nhà thờ giáo xứ: 1666 = thân đá + tháp vuông (lan can răng cưa hoặc chóp chì nhỏ); trong vùng cháy → phế tích → nhà thờ Wren (tháp/chóp Portland, 1670–1700).
    sites: [(tên, E, N, nguồn)] — vị trí từ Doornick 1666 (số nhà thờ trên bản đồ, TPS → EN) khi có, ngoài vùng cháy từ OSM (bậc ghi trong ldn2.json)."""
    n = 0
    for nm, E, N, src, rebuilt in sites:
        g = Hg(E, N); x, z = L(E, N); burn = float(t_chay([E, N])[0]); die = 1666.0 + (245 + burn / 24) / 365.0 if burn >= 0 else 1950.0 + float(RNG.uniform(0, 60))
        ang = float(RNG.uniform(-0.12, 0.12)); tl = (1300.0, die, g, burn)
        nl, nw = float(RNG.uniform(22, 34)), float(RNG.uniform(10, 15))
        m.box(x + 0.0, z, nl, nw, ang, g, g + float(RNG.uniform(9, 12)), jit(STONE, 10), jit(LEAD, 6), tl, 8, 5, 9, 8, 'side', 25)
        tx, tz = x - math.cos(ang) * (nl / 2 + 2.5), z - math.sin(ang) * (nl / 2 + 2.5); th = float(RNG.uniform(20, 32))
        m.box(tx, tz, 6.5, 6.5, ang, g, g + th, jit(STONE, 10), jit(LEAD, 6), tl, 8, 5, 9, 8)
        if RNG.random() < 0.45: m.cyl(tx, tz, 2.6, 0.2, g + th, g + th + float(RNG.uniform(5, 14)), jit(LEAD, 6), tl, 8, 9, 8)
        else:
            for a_, b_ in ((-3, -3), (3, -3), (3, 3), (-3, 3)): m.cyl(tx + a_ * math.cos(ang) - b_ * math.sin(ang), tz + a_ * math.sin(ang) + b_ * math.cos(ang), 0.5, 0.05, g + th, g + th + 2.5, jit(STONE, 6), tl, 8, 5, 6)
        if burn >= 0:
            m.box(x, z, nl, nw, ang, g, g + 6, jit((118, 106, 96), 8), jit((80, 70, 64), 6), (die, 1672.0, g, burn), 2, 10, 10)
            m.box(tx, tz, 6.5, 6.5, ang, g, g + th * 0.7, jit((118, 106, 96), 8), jit((80, 70, 64), 6), (die, 1675.0, g, burn), 2, 10, 10)
            if rebuilt:                                                          # dựng lại theo danh sách (51/87 — N8); nhà thờ không dựng lại: Reynolds 1922
                t0 = 1670.0 + float(RNG.uniform(0, 28)); tw = (t0, 9999.0 if RNG.random() < 0.75 else 1940.995, g, -1.0)
                m.box(x, z, nl * 0.9, nw, ang, g, g + 11, jit(PORTLAND, 5), jit(LEAD, 5), tw, 9, 6, 9, 8, 'side', 22)
                m.box(tx, tz, 6.0, 6.0, ang, g, g + th, jit(PORTLAND, 5), jit(LEAD, 5), tw, 9, 6, 9, 8)
                sty = RNG.random()
                if sty < 0.45: m.lathe(tx, tz, [(2.9, g + th), (2.4, g + th + 5), (1.6, g + th + 10), (0.9, g + th + 15), (0.05, g + th + float(RNG.uniform(20, 30)))], jit(PORTLAND, 5) if RNG.random() < 0.6 else LEAD, tw, 9, 6, 8)
                elif sty < 0.75: m.cyl(tx, tz, 2.6, 2.6, g + th, g + th + 5, jit(PORTLAND, 5), tw, 9, 6, 8); m.dome(tx, tz, 2.6, g + th + 5, 2.5, LEAD, tw, 9, 9, 8, 3); m.cyl(tx, tz, 0.5, 0.05, g + th + 7.5, g + th + 12, LEAD, tw, 9, 9, 6)
                else:
                    for a_, b_ in ((-2.8, -2.8), (2.8, -2.8), (2.8, 2.8), (-2.8, 2.8)): m.cyl(tx + a_ * math.cos(ang) - b_ * math.sin(ang), tz + a_ * math.sin(ang) + b_ * math.cos(ang), 0.45, 0.05, g + th, g + th + 3.5, jit(PORTLAND, 5), tw, 9, 6, 6)
        n += 1
    return n
def cau_2026(m):
    """cầu hiện đại: MỘT mặt cầu cho mỗi cầu (OSM có nhiều đường song song — làn xe, lối bộ, đường ray — trước đây vẽ chồng thành tấm rộng), bề rộng + năm theo cầu; trụ mỗi ≈ 50 m (bậc 5 hình trụ)."""
    W_ = {'London Bridge': (32, 1973.0, (172, 170, 164)), 'Southwark Bridge': (17, 1921.0, (118, 128, 104)), 'Blackfriars Bridge': (32, 1869.0, (150, 60, 52)),
          'Millennium Bridge': (4, 2000.0, (186, 188, 190)), 'Cannon Street Railway Bridge': (30, 1866.0, (90, 92, 96)), 'Tower Bridge': (18, 1894.0, (130, 150, 170))}
    best = {}
    for d in R['duong']:
        if d.get('bridge') != 'yes': continue
        nm = d['name'] if d['name'] in W_ else ('Cannon Street Railway Bridge' if d['hw'] == 'rail' else None)
        if not nm: continue
        l = np.array(d['l'], float)
        if not at(WAT26, l.mean(0)): continue
        ln = float(np.linalg.norm(np.diff(l, axis=0), axis=1).sum())
        if nm not in best or ln > best[nm][0]: best[nm] = (ln, l)
    for nm, (ln, l) in best.items():
        wd, t0, col = W_[nm]
        for i in range(len(l) - 1):
            a, b = l[i], l[i + 1]; c = (a + b) / 2; x, z = L(*c); sl = float(np.linalg.norm(b - a))
            m.box(x, z, sl + 0.5, wd, math.atan2(-(b - a)[1], (b - a)[0]), 6.0, 8.2, jit(col, 4), (104, 104, 102), (t0, 9999.0, 6.0, -1.0), 7, 8, 12)
        tot = np.r_[0, np.cumsum(np.linalg.norm(np.diff(l, axis=0), axis=1))]
        for sdist in np.arange(25, tot[-1] - 20, 50.0):
            i = int(np.searchsorted(tot, sdist)) - 1; i = max(0, min(i, len(l) - 2)); f = (sdist - tot[i]) / max(tot[i + 1] - tot[i], 1e-3); p = l[i] + (l[i + 1] - l[i]) * f
            if not at(WAT26, p): continue
            x, z = L(*p); m.box(x, z, 6, wd * 0.8, math.atan2(-(l[i + 1] - l[i])[1], (l[i + 1] - l[i])[0]), -3.0, 6.0, (150, 146, 138), (150, 146, 138), (t0, 9999.0, -3.0, -1.0), 7, 5, 5)
    return len(best)

# ------------------------------------------------------------------ mặt đất: lớp phủ 2 m (1666 / 2026) → PNG (R = lớp)
def lop_dat(streets):
    """lớp: 0 sân/đất trống · 1 phố lát (1666 sỏi; 2026 nhựa) · 2 vỉa hè (2026) · 3 cỏ/vườn · 4 bãi bùn sông · 5 sân nhà thờ."""
    c66 = np.zeros((GH, GW), np.uint8); c26 = np.zeros((GH, GW), np.uint8)
    for l, hw, nm in streets: cv2.polylines(c66, [np.round(to_g(l)).astype(np.int32)], False, 1, thickness=max(1, int(2 * hw / G)))
    for d in R['duong']:
        if d['hw'] in ('rail', 'proposed', 'platform', 'corridor') or d.get('tunnel') == 'yes': continue
        hw = {'trunk': 7.0, 'primary': 6.0, 'secondary': 5.0, 'tertiary': 4.5, 'unclassified': 3.5, 'residential': 3.5, 'service': 2.5}.get(d['hw'], 0)
        if hw: cv2.polylines(c26, [np.round(to_g(d['l'])).astype(np.int32)], False, 1, thickness=max(1, int(2 * hw / G)))
        elif d['hw'] in ('footway', 'pedestrian', 'path'): cv2.polylines(c26, [np.round(to_g(d['l'])).astype(np.int32)], False, 2, thickness=2)
    c26[(c26 == 0)] = 2                                                     # thành phố 2026: còn lại là vỉa hè/sân lát
    gm = poly_mask([d['r'] for d in R['dat']]); c26[gm == 1] = 3
    # 1666: vườn sâu trong khối (Doornick vẽ vườn) — xa phố > 45 m trong vùng có nhà; ngoài vùng có nhà = đồng cỏ
    st = (c66 == 1).astype(np.uint8); dt = cv2.distanceTransform(1 - st, cv2.DIST_L2, 5) * G
    c66[(dt > 45) & (BUILT == 1) & (RIV == 0)] = 3; c66[(BUILT == 0) & (c66 == 0)] = 3; c66[(RIV == 1) & (c66 == 0)] = 5
    for c_, W, wharf in ((c66, WAT66, 5), (c26, WAT26, 2)):
        dd = cv2.distanceTransform((W == 0).astype(np.uint8), cv2.DIST_L2, 5) * G
        c_[(W == 0) & (dd < 22)] = wharf                                 # 1666: bến/kè gỗ + sân bến (lát sỏi, ván) dọc bờ — không cỏ; 2026: lối đi ven sông lát đá
        c_[W == 1] = 6                                                   # mặt nước
    return c66, c26

# ------------------------------------------------------------------ cây + thuyền
def cay(c66, c26):
    out = []
    for yr0, yr1, cl, dens in ((1500.0, 1850.0, c66, 0.0016), (1850.0, 9999.0, c26, 0.0022)):
        ys, xs = np.where(cl == 3)
        if yr0 < 1700: ok = BUILT[ys, xs] == 1; ys, xs = ys[ok], xs[ok]                 # 1666: chỉ vườn trong khối nhà (Doornick vẽ vườn), không rải đồng ngoài hộp
        idx = RNG.choice(len(ys), size=min(len(ys), int(len(ys) * G * G * dens)), replace=False) if len(ys) else []
        for i in idx:
            E = BB[0] + (xs[i] + RNG.random()) * G; N = BB[3] - (ys[i] + RNG.random()) * G
            if not (530300 < E < 534800 and 179700 < N < 182300): continue
            if yr0 < 1700 and at(BURN, [E, N]): y1_ = 1666.0 + (245 + float(t_chay([E, N])[0]) / 24) / 365.0
            else: y1_ = yr1
            x, z = L(E, N); out += [x, Hg(E, N), z, float(RNG.uniform(3.0, 6.5)), yr0, y1_, float(RNG.random())]
    return np.array(out, np.float32)
CAMS = [(532330, 180250), (532690, 180290), (533250, 180480), (531300, 181160), (532990, 180750), (533800, 180600)]   # P1, P2, P6, P4, P3, P8 (BANG-SHOT-v1)
def thuyen():
    """thuyền theo mốc (thưa, đúng thời kỳ — bậc 4–5): 1666 đò wherry (6 m), sà lan lighter (14 m), tàu buồm 2–3 cột dưới cầu (Pool of London);
    1940 sà lan + tàu kéo; 2026 tàu khách + sà lan. Vị trí rải trên mặt nước của năm, lệch về dòng chính."""
    out = []; RB = np.random.default_rng(1667)                                # bộ sinh riêng: thuyền không đổi khi hình học đổi
    ws = {66: WAT66, 26: WAT26}
    for (y0, y1, key, kinds) in ((1500, 1830, 66, [('wherry', 70), ('lighter', 22), ('ship', 14)]), (1900, 1950, 26, [('barge', 26), ('tug', 6)]), (1990, 9999, 26, [('cruise', 9), ('barge', 6)])):
        W = ws[key]; ys, xs = np.where(W == 1)
        for kind, nn in kinds:
            k = 0
            while k < nn:
                i = RB.integers(len(ys)); E = BB[0] + xs[i] * G; N = BB[3] - ys[i] * G
                if not (531200 < E < 534200 and 180150 < N < 180950): continue
                dd = cv2.distanceTransform((W == 1).astype(np.uint8), cv2.DIST_L2, 5)[ys[i], xs[i]] * G if False else None
                if kind == 'ship' and E < 532950: continue                 # tàu lớn không qua cầu: dưới cầu
                if min(np.hypot(E - ce, N - cn) for ce, cn in CAMS) < 260: continue   # không đặt thuyền sát điểm máy (che khung)
                if at(W, [E + 12, N]) == 0 or at(W, [E - 12, N]) == 0 or at(W, [E, N + 12]) == 0 or at(W, [E, N - 12]) == 0: continue
                x, z = L(E, N); out.append({'k': kind, 'x': round(x, 1), 'z': round(z, 1), 'a': round(float(RB.uniform(-0.4, 0.4)) + (math.pi if RB.random() < 0.5 else 0), 3), 'y0': y0, 'y1': y1, 's': round(float(RB.random()), 3)})
                k += 1
    return out

# ------------------------------------------------------------------ vị trí nhà thờ (Doornick khi có → mo-hinh/nha-tho-doornick.json; ngoài vùng cháy → OSM)
def sites_nha_tho():
    out = []; f = os.path.join(REPO, 'channel-k2/k2c-t4-02/mo-hinh/nha-tho-1666.json')
    for d in json.load(open(f))['nha_tho']: out.append((d['ten'], d['EN'][0], d['EN'][1], 'wiki', d['dung_lai_wren']))
    have = np.array([[o[1], o[2]] for o in out]) if out else np.zeros((0, 2))
    seen = set()
    for d in R['diem']:
        if d['k'] != 'place_of_worship' or d['name'] in seen: continue
        E, N = d['p']
        if not (531100 < E < 533800 and 180500 < N < 181800): continue
        if "Paul" in d['name'] and 'Cathedral' in d['name']: continue
        if len(have) and np.min(np.hypot(have[:, 0] - E, have[:, 1] - N)) < 40: continue
        seen.add(d['name']); out.append((d['name'], E, N, 'osm', True))
    return out

def dia_hinh(step=4.0):
    """địa hình hai cao độ (1666 / 2026) với mép nước MỊN: mặt nạ nước làm trơn Gauss (σ 6 m) rồi hoà cao độ đất ↔ lòng sông (−3 m) theo smoothstep
    → đường mép (mặt nước y 0,6) là đường đồng mức của trường trơn, không răng cưa theo ô (LOOK-4 T3: không bờ bậc thang)."""
    es = np.arange(BB[0], BB[2] + 0.1, step); ns = np.arange(BB[3], BB[1] - 0.1, -step)
    EE, NN = np.meshgrid(es, ns); h = np.clip(cv2.resize(DTM, (len(es), len(ns)), interpolation=cv2.INTER_AREA), 0.5, 45.0)
    def smooth(W): return cv2.GaussianBlur(W.astype(np.float32), (0, 0), 3.0)
    s26, s66 = smooth(WAT26), smooth(WAT66)
    g = to_g(np.stack([EE, NN], -1)); ci = np.clip(g[..., 0], 0, GW - 1).astype(np.float32); ri = np.clip(g[..., 1], 0, GH - 1).astype(np.float32)
    w26 = cv2.remap(s26, ci, ri, cv2.INTER_LINEAR); w66 = cv2.remap(s66, ci, ri, cv2.INTER_LINEAR)
    ss = lambda x: np.clip((x - 0.30) / 0.40, 0, 1) ** 2 * (3 - 2 * np.clip((x - 0.30) / 0.40, 0, 1))
    land26 = h; land66 = np.where(w26 > 0.5, 2.6, h)                    # đất 1666 nơi nay là nước (bờ trước Embankment) = bãi thấp 2,6 m
    h26 = land26 * (1 - ss(w26)) + (-3.0) * ss(w26); h66 = land66 * (1 - ss(w66)) + (-3.0) * ss(w66)
    gm = poly_mask([d['r'] for d in R['dat']]); green = at(gm, np.stack([EE, NN], -1))
    return {'nx': len(es), 'nz': len(ns), 'x0': es[0] - E0, 'z0': -(ns[0] - N0), 'step': step, 'h26': h26.astype(np.float32), 'h66': h66.astype(np.float32), 'xanh': green.astype(np.uint8)}

def main():
    meta = {'goc_EN': [E0, N0], 'bbox': BB, 'bac': {}, 'phien_ban': 'look-v2'}
    T = dia_hinh(step=4.0); meta['dia_hinh'] = {k: T[k] for k in ('nx', 'nz', 'x0', 'z0', 'step')}
    m = M(); streets = H0.pho_1666(); meta['pho_1666'] = len(streets); chim = []
    LOTS, occ = lots(streets); KHO = kho_ven_song(occ); LOTS = LOTS + KHO; meta['lo'] = len(LOTS); meta['kho_ven_song'] = len(KHO); toa_start()
    meta['nha'] = nha(m, LOTS, chim); meta['bac']['nha_1666'] = '5 (lô theo phố OSM còn giữ + mặt nạ Doornick bậc 1; kiểu nhà khung gỗ trát, tầng nhô, đầu hồi ra phố — bậc 4 theo Hollar)'
    meta['bac']['nha_1667'] = '4–5 (4 hạng Rebuilding Act 1667: 2/3/4/4 tầng theo hạng phố; tường gạch)'
    meta['toa'] = toa(m); meta['bac']['toa_2026'] = '1 (OSM ODbL + LiDAR EA OGL); vật liệu theo loại/độ cao — bậc 5'; meta['bac']['vict'] = '5 (khối 1840–1940 trên nền toà sau 1941)'
    c_new = st_pauls_wren(m); c_old = st_pauls_old(m); tower_of_london(m); monument(m); london_bridge_old(m); tuong_thanh(m)
    meta['bac']['old_st_pauls'] = '3 (kích thước Clifton-Taylor/Hooke) + 4 (tỉ lệ, khoang theo Hollar/Dugdale 1658)'; meta['bac']['wren'] = '3 (Fletcher 1962) + 4 (tháp tây, trống)'
    meta['ke'] = {'go_1666': quays(m, WAT66, 1500.0, 1866.0, 'go'), 'embankment': quays(m, WAT26, 1868.0, 9999.0, 'da')}
    S = sites_nha_tho(); meta['nha_tho'] = nha_tho(m, S); meta['nha_tho_nguon'] = {k: sum(1 for s in S if s[3] == k) for k in ('wiki', 'osm')}
    meta['cau_2026'] = cau_2026(m)
    meta['st_pauls_EN'] = c_new.tolist(); meta['old_st_pauls_EN'] = c_old.tolist(); _c, _ax, _ = axis_of("St Paul's Cathedral"); meta['old_st_pauls_truc'] = (_ax if _ax[0] > 0 else -_ax).tolist(); meta['blitz_1940'] = BLITZ
    P, C, TL, Kk, UV, MT, FL = m.arr(); meta['dinh'] = len(P); meta['tam_giac'] = len(P) // 3
    c66, c26 = lop_dat(streets); cv2.imwrite(os.path.join(OUT, 'cls66.png'), c66); cv2.imwrite(os.path.join(OUT, 'cls26.png'), c26)
    meta['lop_dat'] = {'w': GW, 'h': GH, 'buoc': G, 'E0': BB[0], 'N1': BB[3]}
    tr = cay(c66, c26); tr.tofile(os.path.join(OUT, 'cay.f32')); meta['cay'] = len(tr) // 7
    json.dump(thuyen(), open(os.path.join(OUT, 'thuyen.json'), 'w'));
    np.array(chim, np.float32).tofile(os.path.join(OUT, 'khoi_bep.f32')); meta['khoi_bep'] = len(chim)
    with open(os.path.join(OUT, 'ldn2.bin'), 'wb') as f:
        off = 0; lay = {}
        for nm, a in (('pos', P), ('col', C), ('tl', TL), ('k', Kk), ('uv', UV), ('mt', MT), ('fl', FL), ('h26', T['h26']), ('h66', T['h66']), ('xanh', T['xanh'])):
            b = np.ascontiguousarray(a).tobytes(); lay[nm] = {'off': off, 'len': len(b), 'dtype': str(a.dtype), 'shape': list(a.shape)}; f.write(b); off += len(b)
            pad = (-off) % 4; f.write(b'\0' * pad); off += pad
    meta['bo_cuc'] = lay; meta['sha256_bin'] = hashlib.sha256(open(os.path.join(OUT, 'ldn2.bin'), 'rb').read()).hexdigest()
    es = np.arange(531000, 533800, 20.0); ns = np.arange(181800, 180500, -20.0); EE, NN = np.meshgrid(es, ns)
    tg = t_chay(np.stack([EE.ravel(), NN.ravel()], 1)).reshape(EE.shape)
    meta['luoi_chay'] = {'E0': 531000, 'N0': 181800, 'buoc': 20, 'nx': len(es), 'nz': len(ns)}
    tg.astype('<f4').tofile(os.path.join(OUT, 'luoi_chay.f32'))
    # lưới lửa 1940 (giờ kể từ 29/12/1940 18:00): ô ngẫu nhiên trong vùng bom ƯỚC LƯỢNG, bén 18:15–21:30 (bậc 5)
    b40 = at(BLITZ_M, np.stack([EE, NN], -1)) == 1; cl = cv2.GaussianBlur(RNG.random(EE.shape).astype(np.float32), (0, 0), 1.2)   # cụm cháy rời (nhiễu làm mịn), ≈ 20 % ô
    t40 = np.where(b40 & (cl > np.quantile(cl[b40], 0.80)), RNG.uniform(0.25, 3.5, EE.shape), -1.0)
    t40.astype('<f4').tofile(os.path.join(OUT, 'luoi_1940.f32'))
    json.dump(meta, open(os.path.join(OUT, 'ldn2.json'), 'w'), ensure_ascii=False, indent=1)
    print(json.dumps({k: meta[k] for k in ('pho_1666', 'lo', 'kho_ven_song', 'nha', 'toa', 'nha_tho', 'nha_tho_nguon', 'ke', 'cay', 'khoi_bep', 'dinh', 'tam_giac')}, ensure_ascii=False))
if __name__ == '__main__': main()
