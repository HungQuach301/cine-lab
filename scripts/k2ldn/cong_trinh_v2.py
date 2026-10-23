#!/opt/cine/bin/python
"""LOOK-T4-V2 · CÔNG TRÌNH BIỂU TƯỢNG chi tiết cao (lớp dữ kiện — dựng 3D theo kích thước có nguồn, KHÔNG AI). Dùng bởi hinh_hoc_v2.py
(thay st_pauls_wren / monument / tower_of_london của hinh_hoc_look.py; phần còn lại của thành phố giữ nguyên từng tam giác).
Nguồn + bậc (§12.2) — trích nguyên văn trong reports/look-t4-v2/NGUON-CONG-TRINH.md:
- St Paul's (Wren): Gilbertson, Official Guide qua 'Views of St. Paul's Cathedral' (Gutenberg #48491, PD) — dài ngoài 515 ft, ngang cánh 250 ft, mặt tây 180 ft,
  trống dưới vòm Ø 112 ft, vòm Ø 102 ft, tháp tây 221 ft, tới thập giá 365 ft (bậc 3); Wikipedia: tường tới lan can ≈ 110 ft, thân + gian bên 121 ft (bậc 3);
  tỉ lệ tầng trống/gác/đèn lồng, số cột hàng cột 32, tầng tháp tây — bậc 4–5 (ước theo hình chiếu đứng công khai; ghi rõ trong NGUON-CONG-TRINH.md).
- Monument: 'London and Its Environs Described' 1761 (Gutenberg #60008, PD) — cột Ø 15 ft, cao 120 ft, bệ 40 ft, chóp + bầu 42 ft, ban công sắt quanh nón 32 ft,
  bầu lửa đồng mạ vàng (bậc 3); vị trí: OSM relation 3374550 (bậc 1); bề ngang bệ 21,5 ft (Strype 1720, qua lookup.london — bậc 3 thứ cấp, chưa đọc bản gốc).
- White Tower: Wikipedia 'White Tower' — 36 × 32 m không kể tháp góc, 27 m tới lan can phía nam, tháp vuông ở hai góc tây, tháp tròn góc đông bắc, khối bán nguyệt
  góc đông nam (apse nhà nguyện) (bậc 3); mũ chì 4 tháp góc theo Hollar (Met CC0, bậc 4); vị trí + hướng: OSM way 369135772 (bậc 1)."""
import math
import numpy as np
import hinh_hoc_look as HL
from hinh_hoc_look import L, Hg, axis_of, frame_of, PORTLAND, LEAD, STONE

RV = np.random.default_rng(20261023)                 # bộ sinh riêng: không làm lệch chuỗi ngẫu nhiên của phần thành phố còn lại
def jv(c, a=4): return HL.jit(c, a, RV)
GOLD = (214, 176, 84); IRON = (40, 40, 42); DARK = (34, 32, 34); WHITE = (214, 208, 192)
FT = 0.3048


def st_pauls_wren(m):
    """St Paul's (Wren 1675–1711). Trục u tây → đông (giao điểm u = 0), v bắc–nam. Toàn chiều dài 157 m (515 ft) từ mặt portico tây (u −90) tới apse (u +67)."""
    c, ax, _ = axis_of("St Paul's Cathedral"); ax = ax if ax[0] > 0 else -ax; ang, P = frame_of(c, ax); g = Hg(*c)
    pc = PORTLAND; t = (1675.5, 9999.0, g, -1.0); tD = (1697.0, 9999.0, g, -1.0); tT = (1707.0, 9999.0, g, -1.0); tL = (1708.8, 9999.0, g, -1.0)
    def B(u, v, w, d, y0, y1, roof='flat', pitch=0, tl=t, col=pc, colr=None, mt=6, mtr=9, fl=8):
        x, z = P(u, v); return m.box(x, z, w, d, ang, g + y0, g + y1, jv(col, 3), jv(colr or LEAD, 3), tl, 5, mt, mtr, fl, roof, pitch, ybase=g)
    def C(u, v, r0, r1, y0, y1, tl=t, col=pc, mt=6, seg=12, cap=True):
        x, z = P(u, v); m.cyl(x, z, r0, r1, g + y0, g + y1, jv(col, 3), tl, 5, mt, seg, cap=cap, yb=g)
    def win(u, v, w, h, y, side, tl=t):                 # ô cửa tối áp mặt tường (side ±1 = mặt bắc/nam, mặt hướng ±v)
        x0, z0 = P(u - w / 2, v + side * 0.12); x1, z1 = P(u + w / 2, v + side * 0.12)
        a, b = ((x0, z0), (x1, z1)) if side > 0 else ((x1, z1), (x0, z0)); m.wall(a, b, g + y, g + y + h, g, DARK, tl, 5, 13, 0)
    def winE(u, v, w, h, y, side, tl=t):                # ô cửa trên mặt hướng ±u (đông/tây)
        x0, z0 = P(u + side * 0.12, v - w / 2); x1, z1 = P(u + side * 0.12, v + w / 2)
        a, b = ((x1, z1), (x0, z0)) if side > 0 else ((x0, z0), (x1, z1)); m.wall(a, b, g + y, g + y + h, g, DARK, tl, 5, 13, 0)
    # --- thân: tường màn 2 tầng tới lan can 33,5 m (≈ 110 ft); thân + gian bên 37 m (121 ft); cánh ngang 66 m tường + portico bán nguyệt tới ±38 m (250 ft cửa–cửa)
    B(-45.5, 0, 57, 37, 0, 33.5); B(-45.5, 0, 57, 15, 33.5, 36.5, 'side', 22)                 # thân tây (u −74…−17) + mái chì gian giữa (ló trên tường màn)
    B(36.5, 0, 39, 37, 0, 33.5); B(36.5, 0, 39, 15, 33.5, 36.5, 'side', 22)                   # hợp xướng (u 17…56)
    B(0, 0, 34, 66, 0, 33.5); B(0, 0, 15, 62, 33.5, 36.5, 'side', 22)                         # cánh ngang + giao điểm
    C(56, 0, 9.5, 9.5, 0, 26, seg=20); x, z = P(56, 0); m.dome(x, z, 9.5, g + 26, 6, LEAD, t, 5, 9, 20, 4)   # apse (→ u +65,5)
    for s_ in (-1, 1):                                                                          # gờ lan can (balustrade) sáng hơn + đường gờ giữa hai tầng
        for (u0, u1) in ((-74, -17), (17, 56)):
            B((u0 + u1) / 2, s_ * 18.75, u1 - u0, 0.5, 31.6, 33.5, col=(232, 228, 216)); B((u0 + u1) / 2, s_ * 18.8, u1 - u0, 0.6, 16.0, 17.2, col=(228, 224, 212))
            for k in range(int((u1 - u0) / 7.6)):                                               # mỗi khoang: cửa sổ vòm tầng dưới + ô hốc tầng trên + trụ áp
                u = u0 + 3.8 + k * 7.6; win(u, s_ * 18.5, 2.4, 6.2, 6.0, s_); win(u, s_ * 18.5, 2.2, 5.2, 21.0, s_)
                B(u + 3.8, s_ * 18.75, 1.1, 0.5, 0, 31.6, col=(226, 222, 210))
        for k in range(-3, 4):                                                                  # mặt hồi cánh ngang
            win(k * 4.2, s_ * 33.0, 2.0, 6.0, 6.0, s_); win(k * 4.2, s_ * 33.0, 1.9, 5.0, 21.0, s_)
        C(0, s_ * 34.5, 6.0, 6.0, 0, 15.5, seg=16); x, z = P(0, s_ * 34.5); m.dome(x, z, 6.0, g + 15.5, 2.6, LEAD, t, 5, 9, 16, 3)   # portico bán nguyệt
        for i in range(7):                                                                      # cột portico bán nguyệt
            a = math.pi * i / 6; C(5.8 * math.cos(a), s_ * (34.5 + 5.8 * math.sin(a)), 0.55, 0.5, 0, 14.5, seg=8, cap=False)
        B(0, s_ * 33.6, 18, 1.0, 33.5, 39.5, 'front', 28, col=(230, 226, 214))                   # trán tam giác hồi cánh ngang
    # --- mặt tây 180 ft (54,9 m): hai tháp tây 221 ft (67,4 m) + portico hai tầng cột ghép đôi + trán tam giác
    for s_ in (-1, 1):
        v = s_ * 21.9
        B(-79, v, 11, 11, 0, 33.5, tl=tT)
        for k in (0, 1): winE(-84.5, v, 2.6, 6.0, 6.0 + 15.0 * k, -1, tT); win(-79, v + s_ * 5.5, 2.4, 6.0, 6.0 + 15.0 * k, s_, tT)
        B(-79, v, 9.4, 9.4, 33.5, 35.0, tl=tT, col=(232, 228, 216))
        B(-79, v, 5.8, 5.8, 35.0, 46.0, tl=tT, col=(170, 166, 158))                               # lõi tầng chuông (trong bóng cột)
        for a_, b_ in ((-1, -1), (1, -1), (1, 1), (-1, 1)):                                     # cột góc ghép đôi tầng chuông (mở)
            for e in (-0.9, 0.9):
                C(-79 + a_ * 3.9 + (e if a_ * b_ > 0 else 0), v + b_ * 3.9 + (0 if a_ * b_ > 0 else e), 0.42, 0.38, 35.0, 46.0, tl=tT, seg=6, cap=False)
        B(-79, v, 9.6, 9.6, 46.0, 48.0, tl=tT, col=(232, 228, 216))
        C(-79, v, 3.4, 3.4, 48.0, 54.5, tl=tT, seg=8); C(-79, v, 3.9, 3.9, 54.5, 55.6, tl=tT, seg=8)
        x, z = P(-79, v)
        m.lathe(x, z, [(3.6, g + 55.6), (2.0, g + 58.0), (2.6, g + 60.0), (1.2, g + 62.5), (0.6, g + 63.5)], jv(LEAD, 3), tT, 5, 9, 12)   # mũ chì cong
        m.lathe(x, z, [(0.6, g + 63.5), (1.0, g + 64.6), (0.8, g + 66.0), (0.05, g + 67.4)], GOLD, tT, 5, 9, 10)                    # quả dứa mạ vàng
    B(-81, 0, 14, 32, 0, 33.5, tl=tT)                                                           # khối giữa sau portico
    B(-87.0, 0, 6.0, 30, 0, 1.6, col=(196, 192, 182)); B(-86.0, 0, 3.0, 26, 1.6, 15.0, col=(150, 146, 138))   # bậc + tường lùi (trong bóng)
    for i in range(6):                                                                          # 12 cột ghép đôi tầng dưới
        vv = -12.5 + i * 5.0
        for e in (-0.75, 0.75): C(-88.6, vv + e, 0.62, 0.55, 1.6, 15.0, seg=8, cap=False)
    B(-88.2, 0, 3.6, 30, 15.0, 17.2, col=(232, 228, 216)); B(-86.0, 0, 3.0, 22, 17.2, 28.0, col=(150, 146, 138))
    for i in range(4):                                                                          # 8 cột ghép đôi tầng trên
        vv = -7.5 + i * 5.0
        for e in (-0.7, 0.7): C(-87.8, vv + e, 0.55, 0.5, 17.2, 28.0, seg=8, cap=False)
    B(-87.6, 0, 3.6, 22, 28.0, 29.6, col=(232, 228, 216)); B(-87.4, 0, 3.0, 22, 29.6, 29.6 + 0.01, 'front', 24, col=(232, 228, 216))
    x0, z0 = P(-89.2, -11.0); x1, z1 = P(-89.2, 11.0); xm, zm = P(-89.2, 0)                  # trán tam giác tây (mặt đứng) cao ≈ 5 m
    m.tri((x0, g + 29.6, z0), (x1, g + 29.6, z1), (xm, g + 34.6, zm), jv((230, 226, 214), 2), t, 5, 6, 8)
    m.tri((x1, g + 29.6, z1), (x0, g + 29.6, z0), (xm, g + 34.6, zm), jv((230, 226, 214), 2), t, 5, 6, 8)
    # --- trống + vòm (Ø trống 112 ft = 34,1 m; Ø vòm 102 ft = 31,1 m; tới thập giá 365 ft = 111,3 m)
    x, z = P(0, 0); R0 = 112 * FT / 2; RD = 102 * FT / 2
    m.cyl(x, z, R0 + 0.5, R0 + 0.5, g + 33.5, g + 37.0, pc, tD, 5, 6, 48)                          # bệ trống
    m.cyl(x, z, R0 - 3.2, R0 - 3.2, g + 37.0, g + 50.5, (150, 146, 138), tD, 5, 6, 48, cap=False)   # tường trống sau hàng cột (trong bóng)
    for i in range(32):                                                                           # hàng 32 cột (peristyle) — bậc 4
        a = 2 * math.pi * i / 32; m.cyl(x + (R0 - 0.8) * math.cos(a), z + (R0 - 0.8) * math.sin(a), 0.78, 0.72, g + 37.0, g + 50.5, jv(pc, 2), tD, 5, 6, 8, cap=False)
    for i in range(8):                                                                            # 8 khối đặc (buttress) giữa hàng cột — giữ trống đọc khối ở xa
        a = 2 * math.pi * (i + 0.5) / 8; m.box(x + (R0 - 1.6) * math.cos(a), z + (R0 - 1.6) * math.sin(a), 2.6, 2.6, -a, g + 37.0, g + 50.5, jv(pc, 2), jv(pc, 2), tD, 5, 6, 6, 8)
    m.cyl(x, z, R0 + 0.2, R0 + 0.2, g + 50.5, g + 52.4, (234, 230, 218), tD, 5, 6, 48)              # đầu cột + gờ
    m.cyl(x, z, R0 - 0.2, R0 - 0.2, g + 52.4, g + 53.5, (226, 222, 210), tD, 5, 6, 48, cap=False)   # lan can Stone Gallery
    m.cyl(x, z, RD + 0.6, RD + 0.6, g + 52.4, g + 61.0, pc, tD, 5, 6, 48, cap=False, fl=8)          # tầng gác (attic)
    for i in range(24):                                                                           # cửa sổ tầng gác
        a = 2 * math.pi * (i + 0.5) / 24; ca, sa = math.cos(a), math.sin(a); rr = RD + 0.66; w2 = 0.8
        p0 = (x + rr * ca - w2 * sa, z + rr * sa + w2 * ca); p1 = (x + rr * ca + w2 * sa, z + rr * sa - w2 * ca)
        m.wall(p0, p1, g + 55.0, g + 58.6, g, DARK, tD, 5, 13, 0)
    m.cyl(x, z, RD + 1.0, RD + 1.0, g + 61.0, g + 61.8, (232, 228, 216), tD, 5, 6, 48)              # gờ chân vòm
    prof = [(RD + 0.15, 61.8), (RD + 0.05, 64.5), (RD - 0.6, 68.5), (RD - 2.0, 72.5), (RD - 4.2, 76.5), (RD - 7.2, 80.5), (RD - 10.2, 83.6), (4.4, 85.6)]
    m.lathe(x, z, [(r, g + y) for r, y in prof], (78, 79, 77), (1708.5, 9999.0, g, -1.0), 5, 9, 64)   # mã 1708,5 = vỏ vòm (đo bề ngang)                      # vòm chì phong hoá xám sẫm (gân: shader theo góc)
    m.cyl(x, z, 4.6, 4.6, g + 85.6, g + 86.4, (230, 226, 214), tL, 5, 6, 24)                       # Golden Gallery
    m.cyl(x, z, 4.5, 4.5, g + 86.4, g + 87.4, IRON, tL, 5, 9, 24, cap=False)                       # lan can sắt Golden Gallery
    m.cyl(x, z, 3.4, 3.3, g + 86.4, g + 97.5, pc, tL, 5, 6, 16, fl=8)                              # đèn lồng (lantern) đá Portland
    for i in range(4):                                                                            # 4 cánh trụ (portico nhỏ) của đèn lồng — đọc thành hình chữ thập khi nhìn xa
        a = math.pi / 4 + i * math.pi / 2; m.box(x + 3.3 * math.cos(a), z + 3.3 * math.sin(a), 2.2, 1.6, -a, g + 86.4, g + 95.0, jv(pc, 2), jv(pc, 2), tL, 5, 6, 6, 8)
    for i in range(8):
        a = 2 * math.pi * (i + 0.5) / 8; ca, sa = math.cos(a), math.sin(a); rr = 3.42; w2 = 0.55
        m.wall((x + rr * ca - w2 * sa, z + rr * sa + w2 * ca), (x + rr * ca + w2 * sa, z + rr * sa - w2 * ca), g + 89.0, g + 93.8, g, DARK, tL, 5, 13, 0)
    m.cyl(x, z, 3.7, 3.7, g + 97.5, g + 98.4, (232, 228, 216), tL, 5, 6, 16)
    m.lathe(x, z, [(3.0, g + 98.4), (2.4, g + 100.6), (1.4, g + 102.8), (0.7, g + 104.6), (0.45, g + 106.4)], jv(LEAD, 2), tL, 5, 9, 16)   # mũ đèn lồng
    m.lathe(x, z, [(0.01, g + 106.4), (0.95, g + 106.9), (1.0, g + 107.5), (0.95, g + 108.1), (0.01, g + 108.6)], GOLD, tL, 5, 9, 12)      # quả cầu vàng
    m.box(x, z, 0.45, 0.45, ang, g + 108.6, g + 111.3, GOLD, GOLD, tL, 5, 9, 9); m.box(x, z, 1.9, 0.4, ang, g + 110.1, g + 110.6, GOLD, GOLD, tL, 5, 9, 9)   # thập giá
    return c


def monument(m):
    """Monument (Wren & Hooke 1671–1677) tại vị trí OSM. Bệ 40 ft (12,19 m) trên đế 27 ft vuông; thân cột Doric có rãnh Ø 15 ft (4,57 m), cột cao 120 ft (36,58 m);
    chóp (cippus) + bầu 42 ft (12,80 m): ban công sắt quanh nón 32 ft, trên là bầu lửa đồng mạ vàng — tổng 202 ft (61,57 m)."""
    c = np.array([532923.0, 180761.0]); g = Hg(*c); x, z = L(*c)
    tA = (1671.5, 9999.0, g, -1.0); tB = (1672.5, 9999.0, g, -1.0); tC = (1676.5, 9999.0, g, -1.0); tU = (1676.9, 9999.0, g, -1.0)
    H1 = 40 * FT; H2 = H1 + 120 * FT; H3 = H2 + 42 * FT
    m.box(x, z, 27 * FT, 27 * FT, 0, g, g + 1.1, jv(PORTLAND, 3), jv(PORTLAND, 3), tA, 5, 6, 6, 8)                       # đế + bậc
    m.box(x, z, 21.5 * FT, 21.5 * FT, 0, g + 1.1, g + H1 - 1.4, jv(PORTLAND, 3), jv(PORTLAND, 3), tA, 5, 6, 6, 8)       # bệ (mặt có phù điêu/bia — không vẽ chữ)
    m.box(x, z, 23.6 * FT, 23.6 * FT, 0, g + H1 - 1.4, g + H1, jv((232, 228, 216), 2), jv((232, 228, 216), 2), tA, 5, 6, 6, 8)   # gờ đầu bệ
    for a_, b_ in ((-1, -1), (1, -1), (1, 1), (-1, 1)):                                       # bốn con rồng ở góc đầu bệ (khối ước)
        m.box(x + a_ * 3.25, z + b_ * 3.25, 1.2, 1.2, 0.785, g + H1, g + H1 + 1.6, jv((190, 186, 176), 3), jv((190, 186, 176), 3), tA, 5, 6, 6)
    m.cyl(x, z, 2.75, 2.6, g + H1, g + H1 + 1.1, jv(PORTLAND, 2), tB, 5, 6, 24)                  # chân cột (torus)
    r0, r1 = 15 * FT / 2, 15 * FT / 2 * 0.86; y0, y1 = g + H1 + 1.1, g + H2 - 2.3; n = 40      # thân có 20 rãnh (40 đoạn so le bán kính)
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n; k0 = 1.0 if i % 2 == 0 else 0.955; k1 = 0.955 if i % 2 == 0 else 1.0
        p00 = (x + r0 * k0 * math.cos(a0), y0, z + r0 * k0 * math.sin(a0)); p01 = (x + r0 * k1 * math.cos(a1), y0, z + r0 * k1 * math.sin(a1))
        p10 = (x + r1 * k0 * math.cos(a0), y1, z + r1 * k0 * math.sin(a0)); p11 = (x + r1 * k1 * math.cos(a1), y1, z + r1 * k1 * math.sin(a1))
        u0, u1 = 2 * math.pi * r0 * i / n, 2 * math.pi * r0 * (i + 1) / n
        m.quad(p00, p10, p11, p01, jv(PORTLAND, 2), tB, 5, 6, 8, ((u0, y0 - g), (u0, y1 - g), (u1, y1 - g), (u1, y0 - g)))
    m.lathe(x, z, [(r1, y1), (r1 * 1.05, y1 + 0.5), (2.65, y1 + 1.3)], jv(PORTLAND, 2), tC, 5, 6, 24)   # đầu cột Doric (echinus)
    m.box(x, z, 5.7, 5.7, 0, y1 + 1.3, g + H2, jv((232, 228, 216), 2), jv((232, 228, 216), 2), tC, 5, 6, 6, 8)   # abacus = sàn ban công
    for s_ in (-1, 1):                                                                         # lan can sắt ban công (tối, mảnh)
        m.box(x + s_ * 2.8, z, 0.1, 5.6, 0, g + H2, g + H2 + 1.15, IRON, IRON, tC, 5, 9, 9); m.box(x, z + s_ * 2.8, 5.6, 0.1, 0, g + H2, g + H2 + 1.15, IRON, IRON, tC, 5, 9, 9)
    m.lathe(x, z, [(1.55, g + H2), (1.45, g + H2 + 3.0), (1.25, g + H2 + 6.5), (1.05, g + H2 + 9.0), (1.3, g + H2 + 9.4), (0.7, g + H2 + 9.75)], jv(PORTLAND, 2), tC, 5, 6, 16)   # nón (cippus) 32 ft
    yu = g + H2 + 9.75                                                                         # bầu lửa mạ vàng ≈ 3 m (42 − 32 ft)
    m.lathe(x, z, [(0.55, yu), (0.95, yu + 0.35), (1.15, yu + 0.9), (1.0, yu + 1.35), (0.75, yu + 1.6)], GOLD, tU, 5, 9, 16)
    for i in range(9):                                                                         # lưỡi lửa đồng mạ vàng (chóp nhọn tỏa ra)
        a = 2 * math.pi * i / 9; rr = 0.42 if i % 3 else 0.0; h = 1.5 if i % 3 else 1.6
        m.cyl(x + rr * math.cos(a), z + rr * math.sin(a), 0.32, 0.02, yu + 1.55, yu + 1.55 + h, GOLD, tU, 5, 9, 5)
    return c


def tower_of_london(m):
    """Tháp Trắng (White Tower) theo hướng + tâm OSM; 36 × 32 m (không kể tháp góc), 27 m tới lan can; tháp vuông hai góc tây, tháp tròn đông bắc,
    khối bán nguyệt (apse) đông nam; bốn mũ chì cong trên tháp góc (Hollar, bậc 4); tường quét vôi trắng (tên 'White Tower' từ lần quét vôi thế kỷ 13 — Wikipedia, bậc 3).
    Tường thành trong/ngoài + tháp tròn góc giữ như look v1 (bậc 5)."""
    c, ax, r = axis_of('White Tower'); g = Hg(*c); tl = (1100.0, 9999.0, g, -1.0); tw = (1100.5, 9999.0, g, -1.0)
    # trục dài của đa giác OSM (gồm cả tháp góc) ≈ đông–tây; đặt u theo trục đó, hướng u về phía ĐÔNG
    ax = ax if ax[0] > 0 else -ax; ang, P = frame_of(c, ax); W, D, H = 36.0, 32.0, 27.0
    col = WHITE
    def B(u, v, w, d, y0, y1, cl=col, mt=5, tl_=tl, roof='flat'):
        x, z = P(u, v); m.box(x, z, w, d, ang, g + y0, g + y1, jv(cl, 4), jv((96, 98, 100), 3), tl_, 5, mt, 9, 8, roof, 0, ybase=g)
    def win(u, v, w, h, y, face):                    # face: 'n','s' (±v) · 'e','w' (±u)
        if face in 'ns':
            s = 1 if face == 'n' else -1; x0, z0 = P(u - w / 2, v + s * 0.12); x1, z1 = P(u + w / 2, v + s * 0.12); a, b = ((x0, z0), (x1, z1)) if s > 0 else ((x1, z1), (x0, z0))
        else:
            s = 1 if face == 'e' else -1; x0, z0 = P(u + s * 0.12, v - w / 2); x1, z1 = P(u + s * 0.12, v + w / 2); a, b = ((x1, z1), (x0, z0)) if s > 0 else ((x0, z0), (x1, z1))
        m.wall(a, b, g + y, g + y + h, g, DARK, tl, 5, 13, 0)
    B(0, 0, W, D, 0, H)
    for i in range(int(W / 1.8)):                                                              # răng cưa lan can (merlon)
        uu = -W / 2 + 0.9 + i * 1.8
        for s in (-1, 1): B(uu, s * (D / 2 - 0.4), 0.9, 0.8, H, H + 1.3)
    for i in range(int(D / 1.8)):
        vv = -D / 2 + 0.9 + i * 1.8
        for s in (-1, 1): B(s * (W / 2 - 0.4), vv, 0.8, 0.9, H, H + 1.3)
    for k in (-2, -1, 0, 1, 2):                                                                # trụ áp (pilaster buttress) + cửa sổ 3 tầng
        for s in (-1, 1):
            B(k * W / 5.0, s * (D / 2 + 0.25), 1.6, 0.5, 0, H); B(s * (W / 2 + 0.25), k * D / 5.0, 0.5, 1.6, 0, H)
    for k in range(5):
        for y in (8.0, 14.5, 21.0):
            uu = -W / 2 + W / 10 + k * W / 5; vv = -D / 2 + D / 10 + k * D / 5
            win(uu, D / 2, 1.3, 2.6, y, 'n'); win(uu, -D / 2, 1.3, 2.6, y, 's'); win(W / 2, vv, 1.3, 2.6, y, 'e'); win(-W / 2, vv, 1.3, 2.6, y, 'w')
    # tháp góc: vuông ở tây bắc + tây nam, tròn ở đông bắc, apse bán nguyệt đông nam; cao hơn lan can ≈ 5 m, mũ chì cong + chong chóng
    HT = H + 5.5; corners = [(-W / 2, D / 2, 'sq'), (-W / 2, -D / 2, 'sq'), (W / 2, D / 2, 'rd'), (W / 2, -D / 2, 'sq2')]
    for (u, v, kind) in corners:
        x, z = P(u, v)
        if kind == 'rd': m.cyl(x, z, 4.0, 4.0, g, g + HT, jv(col, 3), tw, 5, 5, 16, fl=8)
        else: B(u, v, 6.6, 6.6, 0, HT, tl_=tw)
        m.lathe(x, z, [(3.3, g + HT), (3.6, g + HT + 0.6), (2.0, g + HT + 2.6), (2.5, g + HT + 3.8), (0.9, g + HT + 5.2), (0.15, g + HT + 6.0)], jv((90, 92, 96), 3), tw, 5, 9, 16)
        m.box(x, z, 0.18, 0.18, ang, g + HT + 6.0, g + HT + 7.6, GOLD, GOLD, tw, 5, 9, 9)
    x, z = P(W / 2, -D / 2 + 8.0); m.cyl(x, z, 8.0, 8.0, g, g + H - 2.0, jv(col, 3), tl, 5, 5, 20, fl=8)   # apse nhà nguyện St John (đông nam)
    # tường thành trong / ngoài (như look v1, bậc 5) — tâm cũ để không đổi bố cục tường
    cx_, cz_ = L(533612.0, 180555.0); g0 = Hg(533612.0, 180555.0)
    for half, hh in ((118, 11), (92, 15)):
        pts = [(cx_ - half, cz_ - half), (cx_ + half, cz_ - half), (cx_ + half, cz_ + half), (cx_ - half, cz_ + half)]
        for i in range(4):
            (ax_, az), (bx, bz) = pts[i], pts[(i + 1) % 4]; L_ = math.hypot(bx - ax_, bz - az)
            m.box((ax_ + bx) / 2, (az + bz) / 2, L_, 3.5, math.atan2(bz - az, bx - ax_), g0, g0 + hh, jv(STONE, 6), jv(STONE, 6), (1100.0, 9999.0, g0, -1.0), 6, 5, 5)
            m.cyl(ax_, az, 6, 6, g0, g0 + hh + 4, jv(STONE, 6), (1100.0, 9999.0, g0, -1.0), 6, 5, 12)
            for j in range(1, 4):                                                              # tháp giữa tường (13 tháp tường trong — ước vị trí, bậc 5)
                f = j / 4.0; m.cyl(ax_ + (bx - ax_) * f, az + (bz - az) * f, 4.2, 4.2, g0, g0 + hh + 3.0, jv(STONE, 6), (1100.0, 9999.0, g0, -1.0), 6, 5, 10)
    return c
