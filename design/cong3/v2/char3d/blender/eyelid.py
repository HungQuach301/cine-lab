# Cine Lab · Cổng 6 (W4, gói nhân vật) — MÍ MẮT: bớt "mắt búp bê" (lòng trắng lộ trên/dưới tròng) cho đầu 'bl' Ida và Cas.
# Đo mép mí bằng tia (lưới da sau chia, hệ đầu H) rồi NƯỚNG vào tư thế trung tính:
#   • mí dưới: nâng bằng đơn vị MPFB eye-slit (CC0) tới khi mép mí dưới chạm đáy tròng (không lộ lòng trắng dưới tròng);
#   • mí trên: hạ bằng đơn vị eye-closure (CC0) tới khi mép mí trên che ~1/4 bán kính tròng phía trên.
# Kênh 'blink' được co lại (1 − c0) để chớp kín vẫn đúng 1,0 = nhắm hẳn. Các kênh khác giữ định nghĩa.
import numpy as np
import mathutils
from mathutils.bvhtree import BVHTree


def _margin(bvh, cx, cy, R, sgn, wall):
    """Khoảng (theo y, đơn vị H) từ tâm mắt tới mép mí (sgn +1: mí trên, −1: mí dưới). Tia bắn từ trước mặt theo −z."""
    for k in range(0, 91):
        y = cy + sgn * k * 0.01 * R
        h = bvh.ray_cast(mathutils.Vector((cx, y, 3.0)), mathutils.Vector((0, 0, -1.0)), 5.0)
        if h[0] is not None and h[0].z > wall + 0.30 * R: return k * 0.01 * R
    return 0.9 * R


def measure(P, polys, centers, R):
    bvh = BVHTree.FromPolygons(P.tolist(), polys)
    out = []
    for c in centers:
        h = bvh.ray_cast(mathutils.Vector((c[0], c[1], 3.0)), mathutils.Vector((0, 0, -1.0)), 5.0)
        wall = h[0].z if h[0] is not None else c[2]
        out.append((_margin(bvh, c[0], c[1], R, +1, wall), _margin(bvh, c[0], c[1], R, -1, wall)))
    return np.array(out).mean(0)   # (mí trên, mí dưới) — khoảng cách tới tâm mắt


def fix_lids(PS, polys, SKD, centers, R, log, iris_r=0.44, pitch=0.06, cover_up=0.25, cover_lo=0.05, slit_key='squint', slit_k=0.6, max_slit=0.6, max_close=0.6):
    yc_iris = -np.sin(pitch) * R                                 # mắt nhìn hơi xuống: tâm tròng thấp hơn tâm nhãn cầu
    up_t = yc_iris + iris_r * R * (1 - cover_up)                  # mép mí trên mong muốn (trên tâm mắt)
    lo_t = -(yc_iris - iris_r * R * (1 - cover_lo))               # mép mí dưới mong muốn (dưới tâm mắt, dương)
    m0 = measure(PS, polys, centers, R)
    log(f'mí trước: trên {m0[0] / R:.2f} R, dưới {m0[1] / R:.2f} R; đích trên {up_t / R:.2f} R, dưới {lo_t / R:.2f} R; tròng {iris_r:.2f} R')
    Dsl = SKD[slit_key] / slit_k; Dcl = SKD['blink']
    s0 = 0.0
    if m0[1] > lo_t + 0.02 * R:
        lo, hi = 0.0, max_slit
        for _ in range(7):
            mid = 0.5 * (lo + hi); m = measure(PS + mid * Dsl, polys, centers, R)
            lo, hi = (mid, hi) if m[1] > lo_t else (lo, mid)
        s0 = 0.5 * (lo + hi)
    P1 = PS + s0 * Dsl; m1 = measure(P1, polys, centers, R); c0 = 0.0
    if m1[0] > up_t + 0.02 * R:
        lo, hi = 0.0, max_close
        for _ in range(7):
            mid = 0.5 * (lo + hi); m = measure(P1 + mid * Dcl, polys, centers, R)
            lo, hi = (mid, hi) if m[0] > up_t else (lo, mid)
        c0 = 0.5 * (lo + hi)
    PS += s0 * Dsl + c0 * Dcl
    SKD['blink'] = SKD['blink'] * (1 - c0)
    m2 = measure(PS, polys, centers, R)
    log(f'mí sau: trên {m2[0] / R:.2f} R, dưới {m2[1] / R:.2f} R (nướng eye-slit {s0:.3f}, eye-closure {c0:.3f}; blink ×{1 - c0:.3f})')
    return {'slit': round(float(s0), 4), 'closure': round(float(c0), 4), 'before_R': [round(float(v / R), 3) for v in m0], 'after_R': [round(float(v / R), 3) for v in m2],
            'target_R': [round(float(up_t / R), 3), round(float(lo_t / R), 3)], 'iris_R': iris_r}
