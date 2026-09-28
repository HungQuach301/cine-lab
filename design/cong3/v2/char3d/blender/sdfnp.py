# Cine Lab · Cửa mặt Ida — gói W4 ('bl'). Hàm hình khối (SDF) dạng numpy + lưới "surface nets" (mặt tứ giác) cho Blender.
# Chạy trong /opt/bpy/bin/python (bpy 5.2.2 có numpy). Không dùng tài sản ngoài.
import numpy as np


def sstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def gauss(d, w):
    return np.exp(-(d / w) ** 2)


def ell(x, y, z, c, r):
    """Ellipsoid (xấp xỉ khoảng cách tốt của IQ)."""
    px, py, pz = (x - c[0]) / r[0], (y - c[1]) / r[1], (z - c[2]) / r[2]
    k0 = np.sqrt(px * px + py * py + pz * pz)
    k1 = np.sqrt((px / r[0]) ** 2 + (py / r[1]) ** 2 + (pz / r[2]) ** 2)
    return k0 * (k0 - 1.0) / np.maximum(k1, 1e-9)


def sph(x, y, z, c, r):
    return np.sqrt((x - c[0]) ** 2 + (y - c[1]) ** 2 + (z - c[2]) ** 2) - r


def cap(x, y, z, a, b, ra, rb=None):
    rb = ra if rb is None else rb
    pa = np.stack([x - a[0], y - a[1], z - a[2]], -1)
    ba = np.array(b, float) - np.array(a, float)
    h = np.clip((pa @ ba) / (ba @ ba), 0.0, 1.0)
    q = pa - h[..., None] * ba
    return np.sqrt((q * q).sum(-1)) - (ra + (rb - ra) * h)


def smin(a, b, k):
    h = np.maximum(k - np.abs(a - b), 0.0) / k
    return np.minimum(a, b) - h * h * k * 0.25


def smax(a, b, k):
    return -smin(-a, -b, k)


def g2(ax, y, pts, w):
    """Gờ/rãnh mềm theo đường gấp khúc chiếu trước (ax, y)."""
    d = np.full(np.shape(ax), 1e9)
    for (a0, a1), (b0, b1) in zip(pts[:-1], pts[1:]):
        bx, by = b0 - a0, b1 - a1
        h = np.clip(((ax - a0) * bx + (y - a1) * by) / (bx * bx + by * by), 0.0, 1.0)
        d = np.minimum(d, np.hypot(ax - a0 - bx * h, y - a1 - by * h))
    return gauss(d, w)


def _hash(i, j, k, seed):
    n = (i * 73856093) ^ (j * 19349663) ^ (k * 83492791) ^ (seed * 2654435761)
    n = (n ^ (n >> 13)) * 1274126177
    return ((n ^ (n >> 16)) & 0xFFFFFF) / float(0xFFFFFF)


def vnoise(x, y, z, seed=1):
    """Nhiễu giá trị 3D trơn trong [0, 1]."""
    xi, yi, zi = np.floor(x).astype(np.int64), np.floor(y).astype(np.int64), np.floor(z).astype(np.int64)
    fx, fy, fz = x - xi, y - yi, z - zi
    fx, fy, fz = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy), fz * fz * (3 - 2 * fz)
    out = 0.0
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                w = (fx if dx else 1 - fx) * (fy if dy else 1 - fy) * (fz if dz else 1 - fz)
                out = out + w * _hash(xi + dx, yi + dy, zi + dz, seed)
    return out


def fbm(x, y, z, seed=1, oct=3):
    s, a, f, tot = 0.0, 1.0, 1.0, 0.0
    for o in range(oct):
        s = s + a * (vnoise(x * f, y * f, z * f, seed + o) - 0.5)
        tot += a; a *= 0.5; f *= 2.03
    return s / tot


def surface_nets(fn, lo, hi, h):
    """Lưới tứ giác từ SDF fn(x, y, z) (âm = bên trong) trên lưới đều bước h. Trả (V (n,3), Q (m,4))."""
    xs, ys, zs = [np.arange(lo[i], hi[i] + h * 0.5, h) for i in range(3)]
    X, Y, Z = np.meshgrid(xs, ys, zs, indexing='ij')
    f = fn(X, Y, Z)
    nx, ny, nz = f.shape
    ins = f < 0
    sums = np.zeros((nx - 1, ny - 1, nz - 1, 3)); cnt = np.zeros((nx - 1, ny - 1, nz - 1))
    I, J, K = np.meshgrid(np.arange(nx), np.arange(ny), np.arange(nz), indexing='ij')
    edges = []
    for ax in range(3):
        sl0 = [slice(None)] * 3; sl1 = [slice(None)] * 3; sl0[ax] = slice(0, -1); sl1[ax] = slice(1, None)
        f0, f1 = f[tuple(sl0)], f[tuple(sl1)]
        m = ins[tuple(sl0)] != ins[tuple(sl1)]
        t = np.where(m, f0 / np.where(m, f0 - f1, 1.0), 0.0)
        P = np.stack([I[tuple(sl0)], J[tuple(sl0)], K[tuple(sl0)]], -1).astype(float)
        P[..., ax] += t
        edges.append((m, ins[tuple(sl0)]))
        others = [a for a in range(3) if a != ax]
        for d1 in (0, 1):
            for d2 in (0, 1):
                sl = [slice(None)] * 3
                sl[others[0]] = slice(d1, d1 + (f.shape[others[0]] - 1))
                sl[others[1]] = slice(d2, d2 + (f.shape[others[1]] - 1))
                mm = m[tuple(sl)]
                sums += np.where(mm[..., None], P[tuple(sl)], 0.0); cnt += mm
    has = cnt > 0
    vid = -np.ones(has.shape, np.int64); vid[has] = np.arange(has.sum())
    V = sums[has] / cnt[has][:, None]
    V = np.array(lo)[None, :] + V * h
    quads = []
    for ax in range(3):
        m, inside0 = edges[ax]
        b, c = (ax + 1) % 3, (ax + 2) % 3
        idx = np.argwhere(m)
        ok = (idx[:, b] >= 1) & (idx[:, b] <= f.shape[b] - 2) & (idx[:, c] >= 1) & (idx[:, c] <= f.shape[c] - 2)
        idx = idx[ok]
        if ax < 3:
            ok2 = idx[:, ax] <= (f.shape[ax] - 2)
            idx = idx[ok2]
        def cell(db, dc):
            q = idx.copy(); q[:, b] -= db; q[:, c] -= dc
            return vid[q[:, 0], q[:, 1], q[:, 2]]
        c00, c10, c11, c01 = cell(1, 1), cell(0, 1), cell(0, 0), cell(1, 0)
        flip = inside0[idx[:, 0], idx[:, 1], idx[:, 2]]
        qd = np.stack([c00, c10, c11, c01], 1)
        qd[~flip] = qd[~flip][:, ::-1]
        quads.append(qd)
    Q = np.concatenate(quads, 0)
    Q = Q[(Q >= 0).all(1)]
    return V, Q


def grad(fn, P, e=1e-4):
    g = np.zeros_like(P)
    for a in range(3):
        d = np.zeros(3); d[a] = e
        g[:, a] = (fn(*(P + d).T) - fn(*(P - d).T)) / (2 * e)
    return g


def project(fn, P, iters=3):
    for _ in range(iters):
        f = fn(*P.T); g = grad(fn, P)
        P = P - (f / np.maximum((g * g).sum(1), 1e-9))[:, None] * g
    return P


def relax(P, E, fn, lam=0.35, iters=3):
    """Giãn đều đỉnh theo mặt tiếp tuyến (Laplace), rồi chiếu lại lên mặt SDF."""
    n = len(P)
    deg = np.bincount(E.ravel(), minlength=n).astype(float)
    for _ in range(iters):
        acc = np.zeros_like(P)
        np.add.at(acc, E[:, 0], P[E[:, 1]]); np.add.at(acc, E[:, 1], P[E[:, 0]])
        L = acc / np.maximum(deg, 1)[:, None] - P
        g = grad(fn, P); g /= np.maximum(np.linalg.norm(g, axis=1), 1e-9)[:, None]
        L -= (L * g).sum(1)[:, None] * g
        P = project(fn, P + lam * L, 2)
    return P
