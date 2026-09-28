# Cine Lab · Cửa mặt Ida — gói W4 ('bl'). Shape key: 16 kênh CÙNG TÊN với facerig.js (CHANNELS) + 6 khẩu hình (VISEMES) + 4 biểu cảm (FACE_PRESETS).
# Mỗi kênh là trường dịch chuyển (đơn vị H) trên lưới Blender; áp cùng một trường cho da, mi, mày, răng → mọi phần đi cùng nhau.
# Ý nghĩa kênh giữ đúng facerig.js của W3 để Cổng 6 dùng lại rãnh khẩu hình; biên độ và mốc đặt lại theo hình khối 'bl' (ida_forms.py).
import numpy as np
from sdfnp import gauss, sstep
from ida_forms import E, ER, LID, MY, MW, MZ, JAW_HINGE, lipY

CHANNELS = ['browUp', 'browDown', 'browInnerUp', 'browKnit', 'blink', 'lidDrop', 'squint', 'cheekRaise', 'smile', 'frown',
            'jawOpen', 'press', 'pucker', 'wide', 'lowerLipIn', 'chinRaise']
VISEMES = {'A': {'jawOpen': 0.75, 'wide': 0.1}, 'E': {'jawOpen': 0.3, 'wide': 0.7}, 'O': {'jawOpen': 0.5, 'pucker': 0.9},
           'MBP': {'press': 1.0}, 'FV': {'lowerLipIn': 1.0, 'jawOpen': 0.1}, 'L': {'jawOpen': 0.4, 'wide': 0.25}}
FACE_PRESETS = {
    'neutral': {},
    'sad_smile': {'smile': 1.0, 'cheekRaise': 0.9, 'browInnerUp': 0.45, 'browKnit': 0.1, 'squint': 0.55, 'jawOpen': 0.1},
    'strained': {'press': 0.8, 'browKnit': 0.8, 'browDown': 0.3, 'chinRaise': 0.4},
    'choked': {'frown': 1.0, 'browInnerUp': 1.0, 'browKnit': 0.65, 'chinRaise': 1.0, 'press': 0.6, 'lidDrop': 0.25, 'squint': 0.2},
}


def _rotx(P, c, a, w):
    """Quay điểm quanh trục x qua c góc a·w (từng điểm)."""
    Y, Z = P[:, 1] - c[1], P[:, 2] - c[2]
    th = a * w; cs, sn = np.cos(th), np.sin(th)
    D = np.zeros_like(P)
    D[:, 1] = (Y * cs - Z * sn) - Y
    D[:, 2] = (Y * sn + Z * cs) - Z
    return D


def channel_disp(ch, P):
    x, y, z = P.T
    ax = np.sqrt(x * x + 1e-6); sx = np.where(x < 0, -1.0, 1.0)
    fm = sstep(0.05, 0.25, z)
    gp = lambda cx, cy, r: gauss(np.hypot(ax - cx, y - cy), r)
    D = np.zeros_like(P)

    def lid(th_up, th_lo):
        Y, Z = y - E[1], z - E[2]
        rr = np.sqrt((ax - E[0]) ** 2 + Y * Y + Z * Z)
        shell = gauss(rr - LID, 0.020) * gauss(ax - E[0], 0.085) * sstep(E[2] - 0.03, E[2] + 0.01, z)
        w_up = sstep(-0.012, 0.012, Y) * shell
        w_lo = sstep(0.004, -0.02, Y) * shell
        c = (0, E[1], E[2])
        return _rotx(P, c, th_up, w_up) + _rotx(P, c, th_lo, w_lo)

    if ch == 'browUp':
        k = gauss(y - 0.665, 0.05) * gauss(ax - 0.13, 0.13); D[:, 1] += 0.030 * k
        k = gauss(ax, 0.2) * gauss(y - 0.77, 0.07); D[:, 1] += 0.012 * k
    elif ch == 'browDown':
        k = gauss(y - 0.665, 0.05) * gauss(ax - 0.13, 0.13); D[:, 1] -= 0.020 * k; D[:, 2] += 0.006 * k
    elif ch == 'browInnerUp':
        k = gp(0.05, 0.665, 0.055); D[:, 1] += 0.045 * k
        k = gauss(ax, 0.1) * gauss(y - 0.76, 0.06); D[:, 1] += 0.015 * k
    elif ch == 'browKnit':
        k = gp(0.05, 0.66, 0.05); D[:, 0] -= sx * 0.014 * k * sstep(0, 0.04, ax); D[:, 1] -= 0.006 * k; D[:, 2] += 0.006 * k
    elif ch == 'blink':
        D += lid(0.80, -0.08)
    elif ch == 'lidDrop':
        D += lid(0.30, 0.0)
    elif ch == 'squint':
        D += lid(0.12, -0.32); k = gp(0.2, 0.47, 0.06); D[:, 1] += 0.006 * k
    elif ch == 'cheekRaise':
        k = gp(0.15, 0.37, 0.07); D[:, 1] += 0.018 * k; D[:, 2] += 0.012 * k; D += lid(0.0, -0.15)
    elif ch == 'smile':
        yb = lipY(x, y); lz = gauss(yb - MY, 0.026) * sstep(MW + 0.05, MW + 0.005, ax) * fm; cu = np.minimum(1, ax / MW) ** 2
        D[:, 1] += 0.03 * lz * cu; D[:, 0] += sx * 0.026 * lz * np.sqrt(cu); D[:, 2] -= 0.016 * lz * cu + 0.005 * lz
        k = gp(MW + 0.004, MY + 0.004, 0.03); D[:, 1] += 0.014 * k; D[:, 0] += sx * 0.012 * k; D[:, 2] -= 0.01 * k
        k = gp(0.13, 0.39, 0.055); D[:, 1] += 0.02 * k; D[:, 2] += 0.018 * k                 # má "táo"
        k = gp(0.105, 0.32, 0.035); D[:, 2] += 0.006 * k                                    # gờ má phồng (rãnh mũi–má sâu thêm)
        k = gauss(ax, 0.05) * gauss(y - MY + 0.02, 0.018) * fm; D[:, 2] -= 0.006 * k
    elif ch == 'frown':
        k = gp(MW, MY, 0.045); D[:, 1] -= 0.034 * k; D[:, 2] -= 0.004 * k
        k = gp(MW + 0.015, MY - 0.05, 0.035); D[:, 1] -= 0.01 * k
    elif ch == 'jawOpen':
        yb = lipY(x, y); spread = 0.004 + 0.11 * sstep(0.045, 0.22, ax)
        w = (sstep(MY + 0.002, MY - spread, yb) * sstep(-0.14, 0.04, z) * sstep(0.36, 0.26, ax)
             * (1 - sstep(0.16, 0.07, z) * sstep(0.10, -0.02, y)) * (1 - sstep(-0.02, -0.12, y)))
        D += _rotx(P, JAW_HINGE, 0.24, w)
        k = gauss(ax, 0.07) * gauss(y - MY - 0.02, 0.015) * fm; D[:, 1] += 0.008 * k
        k = sstep(0.007, 0.003, np.abs(yb - MY)) * sstep(MZ - 0.03, MZ - 0.005, z) * sstep(MW + 0.004, MW - 0.012, ax) * fm
        D[:, 2] -= 0.05 * k                                                                  # vách trong khe môi lùi → hốc miệng
    elif ch == 'press':
        k = gauss(ax, 0.06) * gauss(y - MY - 0.02, 0.016) * fm; D[:, 1] -= 0.006 * k; D[:, 2] -= 0.004 * k
        k = gauss(ax, 0.06) * gauss(y - MY + 0.022, 0.018) * fm; D[:, 1] += 0.007 * k; D[:, 2] -= 0.003 * k
    elif ch == 'pucker':
        k = gauss(ax, 0.08) * gauss(y - MY, 0.04) * fm; D[:, 2] += 0.02 * k; D[:, 0] -= sx * 0.014 * k * sstep(0, 0.06, ax)
        k = gp(MW, MY, 0.04) * fm; D[:, 0] -= sx * 0.028 * k; D[:, 2] += 0.008 * k
    elif ch == 'wide':
        k = gp(MW, MY, 0.05); D[:, 0] += sx * 0.018 * k; D[:, 2] -= 0.006 * k; D[:, 1] += 0.004 * k
    elif ch == 'lowerLipIn':
        k = gauss(ax, 0.06) * gauss(y - MY + 0.024, 0.018) * fm; D[:, 1] += 0.012 * k; D[:, 2] -= 0.014 * k
    elif ch == 'chinRaise':
        k = gp(0, 0.12, 0.05); D[:, 1] += 0.012 * k; D[:, 2] += 0.008 * k
        k = gauss(ax, 0.05) * gauss(y - MY + 0.03, 0.02); D[:, 2] += 0.006 * k
    if ch != 'jawOpen':
        D *= fm[:, None]
    return D


def mix_disp(weights, P):
    D = np.zeros_like(P)
    for ch, v in weights.items():
        if v:
            D += v * channel_disp(ch, P)
    return D
