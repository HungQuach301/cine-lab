# Cine Lab · Cửa mặt Ida — gói W4 ('bl'). HÌNH KHỐI đầu Ida (hệ đầu của cast3d: đơn vị H, y = 0 cằm, 1 đỉnh sọ, +z mặt, x ngang).
# Mọi số đo ở đây là thiết kế riêng của gói này (không lấy từ nhân vật có sẵn). Tuân model sheet v1.4: tuổi 74, mũi dài 0,26 H hơi khoằm,
# cổ 0,40 H, tóc bạc #e2dfda, búi 0,546 H, hoa tai ở dái tai; cách điệu kiểu phim hoạt hình (khối lớn rõ, nếp tuổi là KHỐI rộng, không nét).
import numpy as np
from sdfnp import ell, sph, cap, smin, smax, gauss, sstep, g2, fbm

# ---- mốc (landmark) — dùng chung cho hình khối, rig, tóc, three.js (ghi ra ida_bl.json) ----
E = (0.150, 0.575, 0.290)     # tâm nhãn cầu (x > 0 bên trái nhân vật)
ER = 0.062                    # bán kính nhãn cầu
LID = ER + 0.011              # bán kính vỏ mí
MY, MW, MZ = 0.285, 0.060, 0.392   # khe môi: độ cao, nửa bề rộng, độ sâu tâm môi
JAW_HINGE = (0.0, 0.40, -0.04)
HC = (0.0, 0.60, -0.05)       # tâm sọ (tâm tia cho tóc, bản lề mũ)
EAR_C = (0.352, 0.505, -0.035)   # tâm tai (gốc bám vào đầu)
EAR_YAW, EAR_TILT = -0.30, -0.24  # vểnh sau (rad), ngả đỉnh tai ra sau


def lipY(x, y):
    return y + 0.55 * x * x      # khoé miệng cụp nhẹ (tuổi)


def head_sdf(x, y, z):
    ax = np.sqrt(x * x + 1e-5)
    fr = lambda z0: sstep(z0, z0 + 0.1, z)
    yb = lipY(x, y)
    # ---- khối lớn ----
    d = ell(x, y, z, (0, 0.635, -0.045), (0.372, 0.385, 0.455))                      # sọ: rộng ở vòng mũ (mũ ôm đầu), đỉnh ≈ 1,02
    d = smin(d, ell(x, y, z, (0, 0.715, 0.10), (0.305, 0.245, 0.285)), 0.10)          # trán tròn cao
    d = smin(d, ell(x, y, z, (0, 0.44, 0.10), (0.285, 0.27, 0.29)), 0.12)             # khối giữa mặt
    d = smin(d, ell(ax, y, z, (0.215, 0.49, 0.225), (0.085, 0.052, 0.08)), 0.09)      # gò má cao
    d = smin(d, ell(ax, y, z, (0.145, 0.355, 0.245), (0.078, 0.085, 0.08)), 0.10)     # đệm má (tuổi: hơi trễ)
    d = smin(d, cap(ax, y, z, (0.238, 0.30, -0.035), (0.078, 0.095, 0.245), 0.034, 0.028), 0.055)   # XƯƠNG HÀM: góc hàm dưới tai → cằm (đường hàm rõ)
    d = smin(d, ell(x, y, z, (0, 0.235, 0.225), (0.14, 0.13, 0.165)), 0.075)          # khối miệng–hàm dưới
    d = smin(d, sph(x, y, z, (0, 0.092, 0.285), 0.052), 0.045)                        # cằm tròn nhỏ (đáy ≈ 0,04)
    d = smin(d, ell(ax, y, z, (0.148, 0.175, 0.185), (0.048, 0.042, 0.048)), 0.05)    # má chùng nhẹ trên đường hàm (tuổi, nhỏ — không quả lê)
    # ---- cổ liền hàm ----
    neck = ell(x, y, z, (0, -0.16, -0.035), (0.198, 0.46, 0.188))
    neck = smin(neck, cap(ax, y, z, (0.185, 0.31, -0.11), (0.045, -0.42, 0.125), 0.027, 0.03), 0.05)  # cơ ức–đòn–chũm
    neck = smin(neck, ell(x, y, z, (0, 0.045, 0.115), (0.115, 0.055, 0.105)), 0.06)                 # da chùng dưới cằm (nhẹ)
    d = smin(d, neck, 0.045)
    d = smax(d, -(y + 0.46), 0.02)                                                     # đáy cổ kín (nằm trong khăn/cổ áo)
    d += 0.0025 * (gauss(y - 0.0 - 0.35 * ax * ax, 0.011) + gauss(y + 0.075 - 0.35 * ax * ax, 0.011)) * sstep(0.02, 0.12, z)   # 2 nếp da cổ
    d = smin(d, ell(ax, y, z, (0.335, 0.50, -0.02), (0.035, 0.085, 0.05)), 0.04)      # gò gốc tai
    # ---- mắt ----
    d = smin(d, cap(ax, y, z, (0.025, 0.668, 0.372), (0.225, 0.650, 0.300), 0.036, 0.027), 0.05)   # gờ mày
    d = smax(d, -ell(ax, y, z, (E[0], E[1] + 0.008, 0.358), (0.098, 0.071, 0.074)), 0.035)          # hốc mắt
    lid = sph(ax, y, z, E, LID)
    d = smin(d, smax(lid, -(y - (E[1] + 0.021 - 0.032 * (ax - E[0]))), 0.010), 0.018)             # mí trên nặng, đuôi cụp
    d = smin(d, smax(lid, y - (E[1] - 0.035), 0.010), 0.012)                                         # mí dưới
    d = smin(d, cap(ax, y, z, (0.085, 0.626, 0.342), (0.218, 0.600, 0.298), 0.018, 0.016), 0.03)     # da chùng trên mí
    # ---- mũi dài 0,26 H, hơi khoằm ----
    d = smin(d, cap(x, y, z, (0, 0.648, 0.368), (0, 0.475, 0.462), 0.024, 0.030), 0.04)             # sống mũi
    d = smin(d, sph(x, y, z, (0, 0.548, 0.432), 0.027), 0.035)                                        # gồ nhẹ (khoằm)
    d = smin(d, sph(x, y, z, (0, 0.438, 0.488), 0.040), 0.035)                                        # đầu mũi tròn
    d = smin(d, sph(x, y, z, (0, 0.412, 0.470), 0.029), 0.03)                                         # đầu mũi trễ xuống
    d = smin(d, sph(ax, y, z, (0.047, 0.418, 0.425), 0.029), 0.026)                                   # cánh mũi
    d = smax(d, -ell(ax, y, z, (0.022, 0.400, 0.452), (0.012, 0.0065, 0.015)), 0.006)                 # lỗ mũi (nông)
    # ---- môi ----
    lips = smin(ell(x, yb, z, (0, MY + 0.013, MZ - 0.004), (0.064, 0.0135, 0.024)),
                ell(x, yb, z, (0, MY - 0.017, MZ - 0.012), (0.056, 0.0165, 0.026)), 0.004)
    d = smin(d, lips, 0.04)
    d += 0.0065 * gauss(yb - MY, 0.0032) * sstep(MW + 0.006, MW - 0.016, ax) * fr(0.3)              # khe môi (rãnh hình học)
    d += 0.0035 * gauss(ax, 0.011) * gauss(y - 0.345, 0.018) * fr(0.33)                              # nhân trung
    d += 0.004 * gauss(y - 0.225, 0.015) * gauss(ax, 0.055) * fr(0.2)                                 # hõm môi–cằm
    # ---- nếp tuổi bằng KHỐI (rộng ≥ 0,01 H) ----
    d += (0.0065 * g2(ax, y, [(0.058, 0.425), (0.085, 0.36), (0.098, 0.315), (0.100, 0.290)], 0.016)
          - 0.003 * g2(ax, y, [(0.084, 0.415), (0.110, 0.355), (0.122, 0.315)], 0.022)) * fr(0.22)     # rãnh mũi–má + gờ má
    d += 0.0035 * g2(ax, y, [(0.072, 0.272), (0.086, 0.215), (0.100, 0.175)], 0.013) * fr(0.2)        # rãnh khoé miệng xuống cằm
    d += (0.0026 * g2(ax, y, [(0.075, 0.497), (0.13, 0.478), (0.19, 0.492)], 0.012)
          - 0.0028 * g2(ax, y, [(0.09, 0.517), (0.145, 0.506), (0.195, 0.516)], 0.014)) * fr(0.24)     # bọng + rãnh dưới mắt
    d += 0.003 * (g2(ax, y, [(0.230, 0.592), (0.280, 0.612)], 0.0075) + g2(ax, y, [(0.234, 0.572), (0.286, 0.570)], 0.0075)
                  + g2(ax, y, [(0.228, 0.552), (0.272, 0.528)], 0.0075)) * sstep(0.05, 0.15, z)          # chân chim
    d += 0.0034 * (gauss(y - 0.752 - 0.12 * ax * ax, 0.011) + gauss(y - 0.792 - 0.12 * ax * ax, 0.011)) * sstep(0.26, 0.06, ax) * fr(0.25)  # nếp trán
    d += 0.0024 * g2(ax, y, [(0.018, 0.64), (0.024, 0.69)], 0.008) * fr(0.3)                           # nếp giữa mày
    d += 0.006 * gauss(np.hypot(ax - 0.30, y - 0.62), 0.06) * sstep(-0.05, 0.1, z)                     # thái dương hõm nhẹ
    d += 0.004 * gauss(np.hypot(ax - 0.215, y - 0.395), 0.05) * fr(0.15)                              # hõm nhẹ dưới gò má
    d += 0.0012 * fbm(x * 30, y * 30, z * 30, 7, 2)                                                   # da không phẳng tuyệt đối
    return d


# ---------------- TAI (lưới riêng, hệ tai: u ra ngoài, v lên, w ra trước) ----------------
def ear_local_sdf(u, v, w):
    rw = 0.080 * (1 - 0.34 * sstep(0.0, -0.125, v))              # dái nhỏ dần
    rv = 0.142
    q = np.sqrt((v / rv) ** 2 + ((w + 0.004) / rw) ** 2)
    d2 = (q - 1.0) * np.minimum(rw, 0.1)
    lobe = sstep(-0.065, -0.105, v)
    rimm = (1 - lobe) * (1 - gauss(np.hypot(v + 0.035, w - 0.075), 0.035))                      # vành (helix) — mở ở khe trước dái tai
    h = 0.010 + 0.015 * gauss(d2 + 0.011, 0.0085) * rimm                                          # vành cuộn
    h += 0.0085 * gauss(d2 + 0.036, 0.0085) * sstep(-0.06, -0.01, v) * sstep(0.05, -0.01, w)     # gờ đối (antihelix)
    h -= 0.017 * gauss(np.hypot(v + 0.018, (w - 0.012) * 1.25), 0.036) * (1 - lobe)              # hố tai (concha)
    h += 0.010 * gauss(np.hypot(v + 0.028, w - 0.070), 0.016)                                     # bình tai (tragus)
    h += 0.008 * lobe                                                                             # dái dày, mềm (đỡ hoa tai)
    return smax(smax(u - h, -0.013 - u, 0.007), d2, 0.010)


def ear_frame(sx):
    """Ma trận 3×3 (cột = trục u, v, w trong hệ đầu) và gốc, cho tai bên sx (+1: x > 0)."""
    cy, sy = np.cos(EAR_YAW * sx), np.sin(EAR_YAW * sx)
    ct, st = np.cos(EAR_TILT), np.sin(EAR_TILT)
    Rx = np.array([[1, 0, 0], [0, ct, -st], [0, st, ct]])
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    M = Ry @ Rx
    M[:, 0] *= sx                                                                                   # u hướng ra ngoài
    return M, np.array([sx * EAR_C[0], EAR_C[1], EAR_C[2]])


EARRING_LOCAL = (0.020, -0.122, -0.004)   # nụ hoa tai: mặt ngoài dái tai


# ---------------- TÓC: đường chân tóc θmax(|φ|) quanh tâm sọ HC ----------------
_TH_PH = np.array([0.00, 0.45, 0.80, 1.05, 1.22, 1.38, 1.52, 1.68, 1.90, 2.30, 2.70, np.pi])
_TH_TH = np.array([1.20, 1.22, 1.27, 1.42, 1.53, 1.47, 1.38, 1.42, 1.60, 2.02, 2.33, 2.43])


def theta_max(ph):
    a = np.abs(ph)
    base = np.interp(a, _TH_PH, _TH_TH)
    return base + 0.012 * np.sin(ph * 9.0) + 0.008 * np.sin(ph * 17.0 + 1.3)     # mép tóc gợn nhẹ, không thẳng


def sdir(th, ph):
    return np.stack([np.sin(th) * np.sin(ph), np.cos(th), np.sin(th) * np.cos(ph)], -1)


# ---------------- sắc độ da (albedo tuyến tính) ----------------
def srgb2lin(c):
    c = np.asarray(c, float)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def hexlin(h):
    return srgb2lin([int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)])


SKIN = '#d8b49a'
HAIR = '#e2dfda'


def skin_albedo(P, N):
    x, y, z = P.T
    ax = np.abs(x); fz = sstep(0.1, 0.3, z)
    gp = lambda cx, cy, r: gauss(np.hypot(ax - cx, y - cy), r)
    base = hexlin(SKIN)
    r = np.full_like(x, 1.0); g = np.full_like(x, 1.0); b = np.full_like(x, 1.0)
    r *= 0.97; g *= 1.0; b *= 1.03                                                         # nền da bớt bão hoà
    warm = (0.22 * gp(0.165, 0.37, 0.07) + 0.28 * gp(0, 0.445, 0.045) + 0.10 * gp(0.05, 0.64, 0.05) + 0.08 * gp(0, 0.12, 0.05)) * fz
    r += warm * 0.30; g -= warm * 0.55; b -= warm * 0.50                                    # ẤM: má, mũi, giữa mày, cằm
    cool = (0.20 * gp(0.14, 0.497, 0.03) + 0.12 * gp(0.30, 0.60, 0.07) + 0.08 * gp(0.12, 0.17, 0.07)) * sstep(0.0, 0.2, z)
    r -= cool * 0.55; g -= cool * 0.30; b += cool * 0.12                                    # MÁT: dưới mắt, thái dương, hàm
    lidrim = gauss(np.sqrt((ax - E[0]) ** 2 + (y - E[1]) ** 2 + (z - E[2]) ** 2) - LID, 0.006) * fz
    r += 0.05 * lidrim; g -= 0.10 * lidrim; b -= 0.08 * lidrim                              # viền mí hồng
    yb = lipY(x, y)
    lip = sstep(0.02, 0.0, np.hypot(ax / 1.15, (yb - MY) / 0.8) - 0.052) * fz
    r -= 0.02 * lip; g -= 0.26 * lip; b -= 0.20 * lip                                       # môi hồng xỉn
    inner = sstep(0.006, 0.0025, np.abs(yb - MY)) * sstep(MZ + 0.012, MZ - 0.004, z) * sstep(MW + 0.006, MW - 0.006, ax)
    nost = sstep(0.02, 0.006, np.hypot((ax - 0.022) / 1.4, y - 0.401)) * sstep(-0.2, -0.6, N[:, 1]) * sstep(0.40, 0.43, z)
    mot = fbm(x * 9, y * 9, z * 9, 41, 3) * fz
    spot = np.maximum(0, fbm(x * 24, y * 24, z * 24, 53, 2) - 0.2) * sstep(0.5, 0.75, y) * sstep(0.0, 0.2, z)
    r += 0.05 * mot; g -= 0.02 * mot; b -= 0.04 * mot
    r -= 0.35 * spot; g -= 0.45 * spot; b -= 0.55 * spot                                   # vài đốm tuổi mờ (trán, thái dương)
    occ = np.maximum.reduce([0.35 * sstep(-0.25, -0.8, N[:, 1]) * sstep(0.30, 0.10, y) * sstep(0.34, 0.22, z),  # dưới hàm
                             0.18 * sstep(0.12, -0.20, y)])                                                          # cổ xuống thấp
    k = (1 - occ) * (1 - 0.85 * inner) * (1 - 0.8 * nost)
    col = np.stack([base[0] * r * k, base[1] * g * k * (1 - 0.45 * inner), base[2] * b * k * (1 - 0.40 * inner)], 1)
    # chân tóc CHUYỂN DẦN: da vùng trên đường chân tóc mang màu tóc (da đầu dưới tóc thưa), hoà trong dải ~0,05 rad
    dx, dy, dz = x - HC[0], y - HC[1], z - HC[2]
    th = np.arccos(np.clip(dy / np.maximum(np.sqrt(dx * dx + dy * dy + dz * dz), 1e-9), -1, 1)); ph = np.arctan2(dx, dz)
    s = sstep(0.035, -0.05, th - theta_max(ph)) * sstep(0.0, 0.1, y + 0.1)
    hair = hexlin(HAIR) * 0.80
    col = col * (1 - s[:, None]) + hair[None, :] * s[:, None] * np.clip(k, 0.6, 1)[:, None]
    return np.clip(col, 0, 1)
