# Cine Lab · Cửa mặt Ida — gói W4 ('bl'): DỰNG ĐẦU IDA BẰNG BLENDER (bpy 5.2.2, chạy script, không giao diện).
# Chạy:  /opt/bpy/bin/python design/cong3/v2/char3d/blender/build_ida_head.py -- <thư mục ra> [--preview] [--blend <file.blend>]
# Ra:    <ra>/ida_bl.glb (đầu + cổ + tai + mắt + mi + mày + tóc + búi + răng; shape key 16 kênh + 6 khẩu hình)  ·  <ra>/ida_bl.json (mốc, bảng kênh)
# Cách dựng (mọi bước bằng mã, không tài sản ngoài):
#   1. Hình khối lớn + nếp tuổi = hàm khoảng cách (ida_forms.head_sdf) → lưới TỨ GIÁC "surface nets" (bước 0,011 H).
#   2. Modifier Subdivision Surface (Catmull–Clark, cấp 1) trong Blender → chiếu lại từng đỉnh lên mặt khối + giãn đều tiếp tuyến (bmesh-tương đương, numpy).
#   3. Tai: lưới riêng (vành, gờ đối, hố tai, bình tai, dái dày) dựng trong hệ tai rồi gắn vào gò gốc tai.
#   4. Tóc: vỏ tóc mỏng dần về 0 ở chân tóc (mép vỏ chui dưới da) + ~300 dải tóc thon (card không alpha) chải về búi + sợi tơ chân tóc;
#      da vùng trên chân tóc mang màu tóc → chân tóc CHUYỂN DẦN. Búi: lõi + 2 cuộn xoắn + dải tóc quấn.
#   5. Shape key: ida_rig.channel_disp (16 kênh cùng tên facerig.js) + vis_A…vis_L; áp cho da, mi, mày, răng.
import sys, os, json, time, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import bpy
from sdfnp import surface_nets, project, relax, sstep, gauss, fbm
import ida_forms as F
from ida_forms import head_sdf, ear_local_sdf, ear_frame, theta_max, sdir, skin_albedo, hexlin, E, ER, LID, MY, MW, MZ, HC
import ida_rig as RIG

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = os.path.abspath(argv[0] if argv and not argv[0].startswith('--') else 'out_bl')
PREVIEW = '--preview' in argv
BLEND = argv[argv.index('--blend') + 1] if '--blend' in argv else None
os.makedirs(OUT, exist_ok=True)
T0 = time.time()
log = lambda *a: print(f'[bl {time.time() - T0:6.1f}s]', *a, flush=True)
rng = np.random.default_rng(20260928)

bpy.ops.wm.read_factory_settings(use_empty=True)
SC = bpy.context.scene


def to_b(P):
    P = np.asarray(P, float); return np.stack([P[:, 0], -P[:, 2], P[:, 1]], 1)


def from_b(B):
    return np.stack([B[:, 0], B[:, 2], -B[:, 1]], 1)


def mk_mat(name, rgb_lin, rough=0.6, use_attr=True, spec=0.3, sss=0.0, img=None):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; bsdf = nt.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (*rgb_lin, 1)
    bsdf.inputs['Roughness'].default_value = rough
    if 'Specular IOR Level' in bsdf.inputs: bsdf.inputs['Specular IOR Level'].default_value = spec
    if sss and 'Subsurface Weight' in bsdf.inputs:
        bsdf.inputs['Subsurface Weight'].default_value = sss
        bsdf.inputs['Subsurface Radius'].default_value = (1.0, 0.35, 0.2)
        bsdf.inputs['Subsurface Scale'].default_value = 0.012
    if img is not None:
        tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = img
        nt.links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])
    elif use_attr:
        ca = nt.nodes.new('ShaderNodeVertexColor'); ca.layer_name = 'Col'
        if rgb_lin is None or tuple(rgb_lin) == (1, 1, 1):
            nt.links.new(ca.outputs['Color'], bsdf.inputs['Base Color'])
        else:
            mul = nt.nodes.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'
            mul.inputs['Factor'].default_value = 1.0
            mul.inputs[6].default_value = (*rgb_lin, 1)
            nt.links.new(ca.outputs['Color'], mul.inputs[7]); nt.links.new(mul.outputs[2], bsdf.inputs['Base Color'])
    return m


def mk_obj(name, P, faces, cols=None, uv=None, mat=None, loc=None):
    me = bpy.data.meshes.new(name)
    me.from_pydata(to_b(P).tolist(), [], [list(map(int, f)) for f in faces])
    me.update()
    me.polygons.foreach_set('use_smooth', np.ones(len(me.polygons), bool))
    if cols is not None:
        a = me.color_attributes.new('Col', 'FLOAT_COLOR', 'POINT')
        c4 = np.concatenate([np.asarray(cols, float), np.ones((len(P), 1))], 1).astype(np.float32)
        a.data.foreach_set('color', c4.ravel()); me.color_attributes.active_color = a
    if uv is not None:
        set_uv(me, uv)
    if mat is not None: me.materials.append(mat)
    ob = bpy.data.objects.new(name, me); SC.collection.objects.link(ob)
    if loc is not None: ob.location = tuple(to_b([loc])[0])
    return ob


def set_uv(me, uv, wrap_u=False):
    uvl = me.uv_layers.new(name='UVMap')
    li = np.zeros(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', li)
    L = np.asarray(uv, float)[li].copy()
    if wrap_u:
        ls = np.zeros(len(me.polygons), np.int32); lt = np.zeros(len(me.polygons), np.int32)
        me.polygons.foreach_get('loop_start', ls); me.polygons.foreach_get('loop_total', lt)
        for s, t in zip(ls, lt):
            u = L[s:s + t, 0]
            if u.max() - u.min() > 0.5: u[u < 0.5] += 1.0
    uvl.data.foreach_set('uv', L.astype(np.float32).ravel())


def verts_of(ob):
    me = ob.data; B = np.zeros(len(me.vertices) * 3); me.vertices.foreach_get('co', B); return from_b(B.reshape(-1, 3))


def set_verts(ob, P):
    ob.data.vertices.foreach_set('co', to_b(P).astype(np.float32).ravel()); ob.data.update()


def normals_of(ob):
    me = ob.data; N = np.zeros(len(me.vertices) * 3); me.vertex_normals.foreach_get('vector', N); return from_b(N.reshape(-1, 3))


def edges_of(ob):
    me = ob.data; e = np.zeros(len(me.edges) * 2, np.int64); me.edges.foreach_get('vertices', e); return e.reshape(-1, 2)


def quad_edges(Q):
    e = np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]], 0); e.sort(1); return np.unique(e, axis=0)


def strip(rows, cols_per_row=None):
    """Dải lưới: rows = mảng (n, k, 3) (n hàng dọc dải, k cột ngang). Trả (P, faces)."""
    n, k, _ = rows.shape
    P = rows.reshape(-1, 3)
    f = [[i * k + j, i * k + j + 1, (i + 1) * k + j + 1, (i + 1) * k + j] for i in range(n - 1) for j in range(k - 1)]
    return P, np.array(f)


def merge(parts):
    P, Fs, C, U, off = [], [], [], [], 0
    for p, f, c, u in parts:
        P.append(p); Fs.append(np.asarray(f) + off); C.append(c); U.append(u); off += len(p)
    return np.concatenate(P), np.concatenate(Fs), np.concatenate(C), np.concatenate(U)


# ======================= 1–2. ĐẦU + CỔ =======================
log('surface nets đầu…')
V, Q = surface_nets(head_sdf, (-0.46, -0.50, -0.60), (0.46, 1.08, 0.62), 0.011)
V = project(head_sdf, V, 2)
log(f'nets: {len(V)} đỉnh, {len(Q)} tứ giác')
mat_skin = mk_mat('bl_skin', (1, 1, 1), rough=0.62, spec=0.25, sss=0.25)
head = mk_obj('ida_head', V, Q, mat=mat_skin)
mod = head.modifiers.new('subd', 'SUBSURF'); mod.levels = 1; mod.render_levels = 1; mod.subdivision_type = 'CATMULL_CLARK'
dg = bpy.context.evaluated_depsgraph_get()
me2 = bpy.data.meshes.new_from_object(head.evaluated_get(dg))
head.modifiers.clear(); old = head.data; head.data = me2; bpy.data.meshes.remove(old); me2.name = 'ida_head'
P = verts_of(head)
log(f'subdiv: {len(P)} đỉnh; chiếu + giãn…')
P = relax(project(head_sdf, P, 2), edges_of(head), head_sdf, lam=0.3, iters=3)
set_verts(head, P)
N = normals_of(head)
col = skin_albedo(P, N)
a = head.data.color_attributes.new('Col', 'FLOAT_COLOR', 'POINT')
a.data.foreach_set('color', np.concatenate([col, np.ones((len(P), 1))], 1).astype(np.float32).ravel()); head.data.color_attributes.active_color = a
set_uv(head.data, np.stack([np.arctan2(P[:, 0], P[:, 2]) / (2 * np.pi) + 0.5, P[:, 1]], 1), wrap_u=True)
log('đầu xong')

# ======================= 3. TAI =======================
log('tai…')
ear_parts = []
EARRING = {}
for sx in (1, -1):
    M, O = ear_frame(sx)
    Vl, Ql = surface_nets(ear_local_sdf, (-0.04, -0.175, -0.115), (0.055, 0.175, 0.115), 0.0042)
    Vl = project(ear_local_sdf, Vl, 3)
    Vl = relax(Vl, quad_edges(Ql), ear_local_sdf, lam=0.3, iters=2)
    u, v, w = Vl.T
    Ph = O[None, :] + Vl @ M.T
    if sx < 0: Ql = Ql[:, ::-1]
    base = hexlin(F.SKIN)
    conch = gauss(np.hypot(v + 0.018, (w - 0.012) * 1.25), 0.034) * sstep(0.014, 0.004, u)
    rimr = sstep(0.012, 0.022, u)
    c = np.stack([base[0] * (1.02 + 0.05 * rimr), base[1] * (0.84 - 0.04 * rimr), base[2] * (0.82 - 0.04 * rimr)], 1)
    c *= (1 - 0.35 * conch)[:, None] * (1 - 0.25 * sstep(-0.004, -0.013, u))[:, None]
    ear_parts.append((Ph, Ql, np.clip(c, 0, 1), np.stack([w, v], 1)))
    EARRING['L' if sx > 0 else 'R'] = (O + M @ np.array(F.EARRING_LOCAL)).round(5).tolist()
Pe, Fe, Ce, Ue = merge(ear_parts)
ears = mk_obj('ida_ears', Pe, Fe, cols=Ce, uv=Ue, mat=mat_skin)
log(f'tai: {len(Pe)} đỉnh')

# ======================= MẮT (nhãn cầu riêng, tròng vẽ bằng thủ tục) =======================
def iris_image():
    S = 256; yy, xx = np.mgrid[0:S, 0:S]; X = (xx + 0.5) / S * 2 - 1; Y = (yy + 0.5) / S * 2 - 1
    r = np.hypot(X, Y) / 1.0; ang = np.arctan2(Y, X)
    RI = 0.56                       # bán kính tròng / R nhãn cầu (trong UV phẳng ±1,1 R)
    sclera = np.array([0.52, 0.49, 0.45])                           # lòng trắng ngà vừa (tuyến tính)
    iris_c = srgb = np.array([0x4e, 0x46, 0x40]) / 255              # nâu xám
    ring = np.array([0x5a, 0x46, 0x36]) / 255                       # vòng #5a4636 của sheet ở rìa tròng
    fib = 0.5 + 0.5 * np.sin(ang * 61 + 3 * np.sin(ang * 7)) * np.sin(ang * 23 + 1.1)
    t = np.clip(r / RI, 0, 1.5)
    irisv = iris_c[None, None, :] * (0.85 + 0.3 * fib[..., None] * sstep(0.35, 0.6, t)[..., None])
    irisv = irisv * (1 - sstep(0.7, 0.95, t))[..., None] + ring[None, None, :] * sstep(0.7, 0.95, t)[..., None]
    irisv *= (1 - 0.55 * sstep(0.88, 1.0, t))[..., None]                                  # viền tròng tối
    pup = sstep(0.40, 0.34, t)
    irisv = irisv * (1 - pup[..., None]) + np.array([0.02, 0.02, 0.025]) * pup[..., None]
    lin = F.srgb2lin(irisv)
    sc = sclera[None, None, :] * (1 - 0.18 * sstep(0.6, 1.0, r / 1.1))[..., None]            # lòng trắng tối dần về mép (bóng mí)
    sc = sc * np.array([1.0, 0.97, 0.96])
    m = sstep(1.02, 0.97, t)[..., None]
    C = lin * m + sc * (1 - m) * (1 + 0.25 * sstep(1.25, 1.0, t))[..., None] * 0.9   # quầng tròng tan vào lòng trắng
    img = bpy.data.images.new('ida_iris', S, S, alpha=False)
    rgba = np.concatenate([np.clip(C, 0, 1), np.ones((S, S, 1))], 2).astype(np.float32)
    img.pixels.foreach_set(rgba.ravel()); img.pack()
    return img


def sphere(R, nth=40, nph=48, bulge=0.07):
    th = np.linspace(0, np.pi, nth + 1); ph = np.linspace(0, 2 * np.pi, nph + 1)[:-1]
    T, Pp = np.meshgrid(th, ph, indexing='ij')
    rr = R * (1 + bulge * sstep(0.80, 0.97, np.cos(T)))                          # giác mạc nhô nhẹ (bắt điểm sáng thật)
    X = rr * np.sin(T) * np.cos(Pp); Y = rr * np.sin(T) * np.sin(Pp); Z = rr * np.cos(T)
    Pm = np.stack([X, Y, Z], -1).reshape(-1, 3)
    f = []
    for i in range(nth):
        for j in range(nph):
            a_, b_ = i * nph + j, i * nph + (j + 1) % nph
            f.append([a_, a_ + nph, b_ + nph, b_])
    return Pm, np.array(f)


img = iris_image()
mat_eye = mk_mat('bl_eye', (1, 1, 1), rough=0.12, spec=0.5, use_attr=False, img=img)
eyes = []
for sx, nm in ((1, 'ida_eye_L'), (-1, 'ida_eye_R')):
    Pm, Fm = sphere(ER)
    uv = np.stack([0.5 + Pm[:, 0] / (2.2 * ER), 0.5 + Pm[:, 1] / (2.2 * ER)], 1)
    eyes.append(mk_obj(nm, Pm, Fm, uv=uv, mat=mat_eye, loc=(sx * E[0], E[1], E[2])))
log('mắt xong')


# ======================= MI TRÊN =======================
def on_skin_z(x, y, z0=0.9):
    z = np.full_like(np.asarray(x, float), z0)
    for _ in range(80):
        z = z - 0.7 * head_sdf(x, y, z)
    return z


lash_parts = []
for sx in (1, -1):
    s = np.linspace(-1, 1, 15)
    axv = E[0] + 0.057 * s + 0.004
    ycut = E[1] + 0.021 - 0.032 * (axv - E[0])
    rz = np.sqrt(np.maximum(LID ** 2 - (axv - E[0]) ** 2 - (ycut - E[1]) ** 2, 1e-6))
    root = np.stack([sx * axv, ycut - 0.001, E[2] + rz - 0.0015], 1)
    rad = root - np.array([sx * E[0], E[1], E[2]]); rad /= np.linalg.norm(rad, axis=1)[:, None]
    dirv = rad + np.array([sx * 0.15, 0.35, 0.25]); dirv /= np.linalg.norm(dirv, axis=1)[:, None]
    L = 0.010 + 0.010 * np.sin(np.pi * (s + 1) / 2) ** 0.7 + 0.006 * (s * sx > 0)
    tang = np.gradient(root, axis=0); tang /= np.linalg.norm(tang, axis=1)[:, None]
    for i in range(len(s)):                                         # chùm mi thon
        rows = []
        for k, tt in enumerate(np.linspace(0, 1, 4)):
            c = root[i] + dirv[i] * L[i] * tt + np.array([0, 0.004, 0]) * tt * tt
            hw = 0.0038 * (1 - tt) + 0.0004
            rows.append([c - tang[i] * hw, c + tang[i] * hw])
        Pl, Fl = strip(np.array(rows))
        lash_parts.append((Pl, Fl, np.full((len(Pl), 3), 1.0), np.zeros((len(Pl), 2))))
    rows = [[root[i] - rad[i] * 0.0005, root[i] + dirv[i] * 0.0035] for i in range(len(s))]   # đường chân mi liền
    Pl, Fl = strip(np.array(rows)); lash_parts.append((Pl, Fl, np.full((len(Pl), 3), 1.0), np.zeros((len(Pl), 2))))
Pls, Fls, Cls, Uls = merge(lash_parts)
mat_lash = mk_mat('bl_lash', tuple(hexlin('#4a403c')), rough=0.7, use_attr=False)
lash = mk_obj('ida_lash', Pls, Fls, cols=Cls, mat=mat_lash)

# ======================= MÀY (bạc, chùm sợi) =======================
brow_parts = []
BX = np.array([0.035, 0.09, 0.15, 0.205, 0.248]); BY = np.array([0.668, 0.688, 0.690, 0.672, 0.645])
for sx in (1, -1):
    for j in range(24):
        t = (j + rng.random() * 0.6) / 24
        bx = np.interp(t, np.linspace(0, 1, 5), BX); by = np.interp(t, np.linspace(0, 1, 5), BY) + (rng.random() - 0.5) * 0.008
        ang = np.radians(75 * (1 - t) ** 1.5 + 8 - 12 * t)             # sợi trong dựng lên, sợi ngoài nằm ngang–chếch xuống
        tx, ty = np.cos(ang), np.sin(ang)
        Lb = 0.028 + 0.016 * rng.random()
        rows = []
        for tt in np.linspace(0, 1, 5):
            px, py = bx + tx * Lb * tt, by + ty * Lb * tt - 0.004 * tt * tt * t
            pz = on_skin_z(np.array([px]), np.array([py]))[0] + 0.0022 + 0.0012 * np.sin(np.pi * tt)
            hw = 0.0045 * (1 - 0.85 * tt) + 0.0005
            nx_, ny_ = -ty, tx
            rows.append([[sx * (px - nx_ * hw), py - ny_ * hw, pz], [sx * (px + nx_ * hw), py + ny_ * hw, pz]])
        Pb, Fb = strip(np.array(rows))
        if sx < 0: Fb = Fb[:, ::-1]
        k = 0.80 + 0.12 * rng.random()
        cb = np.repeat(np.linspace(0.85, 1.0, 5), 2)[:, None] * k * np.ones((1, 3))
        brow_parts.append((Pb, Fb, cb, np.stack([np.tile([0, 1], 5), np.repeat(np.linspace(0, 1, 5), 2)], 1)))
Pbr, Fbr, Cbr, Ubr = merge(brow_parts)
HAIR_LIN = tuple(hexlin(F.HAIR))
mat_hair = mk_mat('bl_hair', HAIR_LIN, rough=0.55, spec=0.35)
mat_brow = mk_mat('bl_brow', HAIR_LIN, rough=0.6, spec=0.3)
brows = mk_obj('ida_brows', Pbr, Fbr, cols=Cbr, uv=Ubr, mat=mat_brow)
log('mi, mày xong')

# ======================= TÓC =======================
HAT_Y, HAT_TILT, RX0, RZ0 = 0.80, 0.08, 0.78 * 0.52, 0.78 * 0.52 * 1.12
ct, st = math.cos(-HAT_TILT), math.sin(-HAT_TILT)
RXm = np.array([[1, 0, 0], [0, ct, -st], [0, st, ct]])     # đầu → hệ mũ (quay −0,08 quanh x)


def skin_radius(D):
    lo = np.full(len(D), 0.05); hi = np.full(len(D), 0.95)
    for _ in range(34):
        m = 0.5 * (lo + hi); P_ = np.array(HC)[None] + D * m[:, None]
        ins = head_sdf(*P_.T) < 0
        lo = np.where(ins, m, lo); hi = np.where(ins, hi, m)
    return 0.5 * (lo + hi)


def band_radius(D):
    o = RXm @ (np.array(HC) - np.array([0, HAT_Y, 0])); d = D @ RXm.T
    A = d[:, 0] ** 2 / RX0 ** 2 + d[:, 2] ** 2 / RZ0 ** 2; B = 2 * (o[0] * d[:, 0] / RX0 ** 2 + o[2] * d[:, 2] / RZ0 ** 2); C = o[0] ** 2 / RX0 ** 2 + o[2] ** 2 / RZ0 ** 2 - 1
    r = (-B + np.sqrt(np.maximum(B * B - 4 * A * C, 0))) / (2 * np.maximum(A, 1e-9))
    yh = o[1] + d[:, 1] * r
    return r, yh


def hair_radius(th, ph):
    th = np.asarray(th, float); ph = np.asarray(ph, float)
    D = sdir(th, ph).reshape(-1, 3)
    rs = skin_radius(D)
    tm = theta_max(ph).ravel(); thr = th.ravel(); aph = np.abs(ph).ravel()
    side = gauss(aph - 1.55, 0.55) * sstep(0.95, 1.3, thr); nape = gauss(aph - np.pi, 0.7) * sstep(1.6, 2.1, thr)
    T0_ = 0.040 + 0.020 * side + 0.016 * nape
    tap = np.clip((tm - thr) / 0.15, 0, 1) ** 0.75
    rh = rs + T0_ * tap
    rb, yh = band_radius(D)
    win = sstep(-0.09, -0.03, yh) * sstep(0.16, 0.12, yh)
    fit = np.maximum(rs + 0.012, rb - 0.004)
    rh = rh + (np.maximum(rh, fit) - rh) * win * np.clip((tm - thr) / 0.10, 0, 1) ** 0.6
    rh = np.where(thr >= tm, rs - 0.002, rh)                               # mép vỏ tóc chui dưới da
    return rh.reshape(th.shape), rs.reshape(th.shape)


def hair_point(th, ph, off=0.0):
    rh, rs = hair_radius(th, ph)
    return np.array(HC) + sdir(th, ph) * (rh + off)[..., None]


log('vỏ tóc…')
NU, NV = 180, 56
phg = np.linspace(-np.pi, np.pi, NU + 1)[:-1]
tg = np.linspace(0, 1, NV + 1)
PH, TT = np.meshgrid(phg, tg, indexing='xy')          # (NV+1, NU)
TH = 0.05 + (theta_max(PH) - 0.05) * TT
RH, RS = hair_radius(TH, PH)
Psh = (np.array(HC) + sdir(TH, PH) * RH[..., None]).reshape(-1, 3)
fsh = []
for i in range(NV):
    for j in range(NU):
        a_, b_ = i * NU + j, i * NU + (j + 1) % NU
        fsh.append([a_, b_, b_ + NU, a_ + NU])
fsh = np.array(fsh)
csh = (0.80 + 0.04 * fbm(Psh[:, 0] * 20, Psh[:, 1] * 20, Psh[:, 2] * 20, 5, 2))[:, None] * np.ones((1, 3))
ush = np.stack([(PH.ravel() + np.pi) / (2 * np.pi) * 8, TH.ravel() * 2], 1)
# kiểm hướng mặt: pháp tuyến phải hướng ra ngoài tâm sọ
tri = Psh[fsh[:, :3]]; nrm = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]); ctr = tri.mean(1) - np.array(HC)
if np.median((nrm * ctr).sum(1)) < 0: fsh = fsh[:, ::-1]
shell = mk_obj('ida_hair_shell', Psh, fsh, cols=csh, uv=ush, mat=mat_hair)
bmin = (RH - RS)[TT < 0.999]
log(f'vỏ tóc: dày {bmin.min():.3f}–{bmin.max():.3f} H')


def card(th0, ph0, th1, ph1, w0, bow, k, nrow=16, rootTaper=True, off0=0.002):
    t = np.linspace(0, 1, nrow)
    th = th0 + (th1 - th0) * t; ph = ph0 + (ph1 - ph0) * t
    ctrs = hair_point(th, ph, off0 + bow * np.sin(np.pi * t))
    radial = ctrs - np.array(HC); radial /= np.linalg.norm(radial, axis=1)[:, None]
    tang = np.gradient(ctrs, axis=0); tang /= np.maximum(np.linalg.norm(tang, axis=1), 1e-9)[:, None]
    bi = np.cross(tang, radial); bi /= np.maximum(np.linalg.norm(bi, axis=1), 1e-9)[:, None]
    prof = np.sin(np.pi * np.clip(0.06 + 0.94 * t, 0, 1)) ** 0.8 if rootTaper else np.sin(np.pi * np.clip(0.5 + 0.5 * t, 0, 1)) ** 0.8
    wv = w0 * (0.12 + 0.88 * prof)
    rows = np.stack([ctrs - bi * wv[:, None] * 0.5, ctrs + radial * (0.18 * wv)[:, None], ctrs + bi * wv[:, None] * 0.5], 1)
    Pc, Fc = strip(rows)
    tri = Pc[Fc[:, :3]]; nrm = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    if np.median((nrm * (tri.mean(1) - np.array(HC))).sum(1)) < 0: Fc = Fc[:, ::-1]
    shade = np.repeat(0.86 + 0.14 * np.sin(np.pi * np.clip(0.1 + 0.9 * t, 0, 1)), 3) * np.tile([0.93, 1.0, 0.93], nrow)
    cc = (shade * k)[:, None] * np.array([1.0, 1.0, 1.0])[None]
    uv = np.stack([np.tile([0, 0.5, 1], nrow), np.repeat(t * 3, 3)], 1)
    return Pc, Fc, np.clip(cc, 0, 1.05), uv


log('dải tóc…')
cards = []
for sx in (1, -1):
    for i in range(96):                                   # thái dương → sau tai → gáy, chải về búi
        ph0 = sx * (0.72 + 2.05 * i / 95 + (rng.random() - 0.5) * 0.04)
        th0 = theta_max(ph0) - 0.012 - 0.06 * rng.random()
        ph1 = sx * (np.pi - 0.22 - 0.45 * rng.random()); th1 = 1.60 + 0.2 * rng.random()
        if abs(ph0) > 2.3: th1 = min(th1, th0 - 0.35)
        cards.append(card(th0, ph0, th1, ph1, 0.020 + 0.012 * rng.random(), 0.002 + 0.003 * rng.random(), 0.9 + 0.14 * rng.random()))
    for i in range(46):                                   # lớp trên (phần lớn dưới mũ; lộ ở mép băng mũ)
        ph0 = sx * (0.35 + 2.2 * i / 45 + (rng.random() - 0.5) * 0.08)
        th0 = theta_max(ph0) - 0.14 - 0.12 * rng.random()
        cards.append(card(th0, ph0, 1.55 + 0.12 * rng.random(), sx * (np.pi - 0.3 - 0.35 * rng.random()), 0.03 + 0.01 * rng.random(), 0.004, 0.92 + 0.12 * rng.random()))
for i in range(34):                                       # trước trán: vén ra sau, lẩn dưới băng mũ
    ph0 = -0.85 + 1.7 * i / 33 + (rng.random() - 0.5) * 0.03; sg = 1 if ph0 >= 0 else -1
    th0 = theta_max(ph0) - 0.01 - 0.03 * rng.random()
    cards.append(card(th0, ph0, th0 - 0.6, ph0 * 1.3 + sg * 0.25, 0.024 + 0.01 * rng.random(), 0.003, 0.92 + 0.12 * rng.random()))
Pcd, Fcd, Ccd, Ucd = merge(cards)
hair_cards = mk_obj('ida_hair_cards', Pcd, Fcd, cols=Ccd, uv=Ucd, mat=mat_hair)
log(f'dải tóc: {len(cards)} dải, {len(Pcd)} đỉnh')

# sợi tơ ở chân tóc: mọc từ da (dưới mép) chui vào khối tóc theo hướng chải → mép không cắt thẳng
fines = []
for i in range(170):
    ph = -2.55 + 5.1 * (i + rng.random() * 0.8) / 170; sg = 1 if ph >= 0 else -1
    tm = theta_max(ph)
    ths, the = tm + 0.012 + 0.02 * rng.random(), tm - 0.07 - 0.06 * rng.random()
    phe = ph + sg * (0.05 + 0.08 * (abs(ph) > 0.9)) + (rng.random() - 0.5) * 0.03
    t = np.linspace(0, 1, 8); th = ths + (the - ths) * t; pp = ph + (phe - ph) * t
    rh, rs = hair_radius(th, pp)
    r = np.maximum(rs + 0.0015, rh - 0.003) + 0.0012 * np.sin(np.pi * t)
    ctrs = np.array(HC) + sdir(th, pp) * r[:, None]
    radial = ctrs - np.array(HC); radial /= np.linalg.norm(radial, axis=1)[:, None]
    tang = np.gradient(ctrs, axis=0); tang /= np.linalg.norm(tang, axis=1)[:, None]
    bi = np.cross(tang, radial); bi /= np.linalg.norm(bi, axis=1)[:, None]
    wv = (0.0035 + 0.002 * rng.random()) * np.sin(np.pi * np.clip(0.08 + 0.9 * t, 0, 1))
    rows = np.stack([ctrs - bi * wv[:, None] * 0.5, ctrs + bi * wv[:, None] * 0.5], 1)
    Pf, Ff = strip(rows)
    tri = Pf[Ff[:, :3]]; nrm = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    if np.median((nrm * (tri.mean(1) - np.array(HC))).sum(1)) < 0: Ff = Ff[:, ::-1]
    fines.append((Pf, Ff, np.full((len(Pf), 3), 0.95), np.stack([np.tile([0, 1], 8), np.repeat(t, 2)], 1)))
Pfi, Ffi, Cfi, Ufi = merge(fines)
hair_fine = mk_obj('ida_hair_fine', Pfi, Ffi, cols=Cfi, uv=Ufi, mat=mat_hair)

# búi: lõi + 2 cuộn xoắn + dải quấn
log('búi…')
Cb = np.array([0.0, 0.475, -0.585]); av = np.array([0.0, -0.25, -1.0]); av /= np.linalg.norm(av)
e1 = np.array([1.0, 0, 0]); e2 = np.cross(av, e1); e2 /= np.linalg.norm(e2)
BR = F_BUN = (0.262, 0.232, 0.17)
Pm, Fm = sphere(1.0, 24, 36, 0.0)
Pcore = Cb[None] + Pm[:, 0:1] * BR[0] * e1 + Pm[:, 1:2] * BR[1] * e2 + Pm[:, 2:3] * BR[2] * av
tri = Pcore[Fm[:, :3]]; nrm = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
if np.median((nrm * (tri.mean(1) - Cb)).sum(1)) < 0: Fm = Fm[:, ::-1]
bun_parts = [(Pcore, Fm, np.full((len(Pcore), 3), 0.78), np.zeros((len(Pcore), 2)))]


def tube(ctrs, rad_fn, nside=10, flat=0.72):
    tang = np.gradient(ctrs, axis=0); tang /= np.linalg.norm(tang, axis=1)[:, None]
    n1 = np.cross(tang, av); n1 /= np.maximum(np.linalg.norm(n1, axis=1), 1e-9)[:, None]; n2 = np.cross(tang, n1)
    rows = []
    for i, c in enumerate(ctrs):
        r = rad_fn(i / (len(ctrs) - 1))
        a_ = np.linspace(0, 2 * np.pi, nside + 1)
        rows.append(c[None] + np.cos(a_)[:, None] * n1[i] * r + np.sin(a_)[:, None] * n2[i] * r * flat)
    return strip(np.array(rows))


for phase in (0.0, np.pi):
    t = np.linspace(0, 1, 110)
    rr = 0.015 + 0.205 * t; ang = 2 * np.pi * 2.1 * t + phase
    hh = 0.15 * np.sqrt(np.clip(1 - (rr / 0.245) ** 2, 0, 1)) + 0.03
    ctrs = Cb[None] + (rr * np.cos(ang))[:, None] * e1 + (0.9 * rr * np.sin(ang))[:, None] * e2 + hh[:, None] * av
    Pt, Ft = tube(ctrs, lambda s: 0.052 * (1 - 0.5 * s) + 0.016)
    tri = Pt[Ft[:, :3]]; nrm = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    rc = tri.mean(1) - np.repeat(ctrs[:-1], 10, 0)
    if np.median((nrm * rc).sum(1)) < 0: Ft = Ft[:, ::-1]
    kk = 0.9 + 0.1 * np.sin(np.linspace(0, 40, len(Pt)))
    bun_parts.append((Pt, Ft, kk[:, None] * np.ones((1, 3)), np.stack([np.tile(np.linspace(0, 1, 11), 110), np.repeat(t * 12, 11)], 1)))
    for q in range(5):                                         # dải tóc quấn theo cuộn (vân sợi)
        aq = 2 * np.pi * q / 5
        r0 = 0.052 * (1 - 0.5 * t) + 0.016
        n1 = np.cross(np.gradient(ctrs, axis=0), av); n1 /= np.linalg.norm(n1, axis=1)[:, None]
        n2 = np.cross(np.gradient(ctrs, axis=0) / np.linalg.norm(np.gradient(ctrs, axis=0), axis=1)[:, None], n1)
        cq = ctrs + (np.cos(aq + t * 9) * (r0 + 0.003))[:, None] * n1 + (np.sin(aq + t * 9) * (r0 + 0.003) * 0.72)[:, None] * n2
        tg_ = np.gradient(cq, axis=0); tg_ /= np.linalg.norm(tg_, axis=1)[:, None]
        rad_ = cq - ctrs; rad_ /= np.linalg.norm(rad_, axis=1)[:, None]
        bi = np.cross(tg_, rad_); w = 0.02 * np.sin(np.pi * np.clip(0.03 + 0.97 * t, 0, 1)) ** 0.5
        Pq, Fq = strip(np.stack([cq - bi * w[:, None] * 0.5, cq + rad_ * 0.003, cq + bi * w[:, None] * 0.5], 1))
        tri = Pq[Fq[:, :3]]; nrm = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
        if np.median((nrm * rad_[np.arange(len(Fq)) // 2]).sum(1)) < 0: Fq = Fq[:, ::-1]
        bun_parts.append((Pq, Fq, np.full((len(Pq), 3), 0.96 + 0.06 * (q % 2)), np.stack([np.tile([0, .5, 1], 110), np.repeat(t * 12, 3)], 1)))
Pbn, Fbn, Cbn, Ubn = merge(bun_parts)
bun = mk_obj('ida_bun', Pbn, Fbn, cols=Cbn, uv=Ubn, mat=mat_hair)
log('tóc xong')

# ======================= RĂNG (chỉ lộ khi mở hàm) =======================
def arc_strip(yc, rr, zc, a, hgt):
    t = np.linspace(-a, a, 13)
    rows = [[[math.sin(q) * rr, yc - hgt / 2, zc + math.cos(q) * rr], [math.sin(q) * rr, yc + hgt / 2, zc + math.cos(q) * rr]] for q in t]
    return strip(np.array(rows))


Put, Fut = arc_strip(MY + 0.004, 0.050, MZ - 0.085, 0.75, 0.016)
Plt, Flt = arc_strip(MY - 0.022, 0.046, MZ - 0.092, 0.70, 0.014)
Pte, Fte, Cte, Ute = merge([(Put, Fut, np.ones((len(Put), 3)), np.zeros((len(Put), 2))), (Plt, Flt, np.ones((len(Plt), 3)), np.zeros((len(Plt), 2)))])
mat_teeth = mk_mat('bl_teeth', tuple(hexlin('#cfc4b2')), rough=0.4, use_attr=False)
teeth = mk_obj('ida_teeth', Pte, Fte, cols=Cte, mat=mat_teeth)

# ======================= 5. SHAPE KEY =======================
log('shape key…')
KEYS = list(RIG.CHANNELS) + ['vis_' + k for k in RIG.VISEMES]


def add_keys(ob, only_jaw=False):
    P0 = verts_of(ob)
    ob.shape_key_add(name='Basis', from_mix=False)
    stats = {}
    for kname in KEYS:
        w = {kname: 1.0} if kname in RIG.CHANNELS else RIG.VISEMES[kname[4:]]
        if only_jaw: w = {'jawOpen': w.get('jawOpen', 0.0)}
        D = RIG.mix_disp(w, P0)
        sk = ob.shape_key_add(name=kname, from_mix=False)
        sk.data.foreach_set('co', to_b(P0 + D).astype(np.float32).ravel())
        stats[kname] = float(np.abs(D).max())
    return stats


KSTAT = add_keys(head)
add_keys(lash); add_keys(brows); add_keys(teeth, only_jaw=True)
log('shape key: ' + ', '.join(f'{k} {v:.3f}' for k, v in KSTAT.items()))

# ======================= XUẤT =======================
meta = {
    '_doc': "Cửa mặt Ida — W4 'bl'. Hệ đầu cast3d (đơn vị H; y = 0 cằm, 1 đỉnh sọ; +z mặt). three.js: nhóm con của joints.head, scale = H. "
            "Shape key = morph target glTF, TÊN = kênh facerig.js (16) + vis_* (6 khẩu hình); preset = trọng số trên các kênh.",
    'E': E, 'ER': ER, 'LID': LID, 'MY': MY, 'MW': MW, 'MZ': MZ, 'jawHinge': F.JAW_HINGE, 'hatHinge': HC,
    'earring': EARRING, 'channels': RIG.CHANNELS, 'visemes': RIG.VISEMES, 'presets': RIG.FACE_PRESETS,
    'viseme_keys': {k: 'vis_' + k for k in RIG.VISEMES}, 'key_max_disp_H': KSTAT,
    'counts': {ob.name: len(ob.data.vertices) for ob in SC.objects if ob.type == 'MESH'},
}
json.dump(meta, open(os.path.join(OUT, 'ida_bl.json'), 'w'), indent=1, ensure_ascii=False)
for ob in SC.objects: ob.select_set(ob.type == 'MESH')
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, 'ida_bl.glb'), export_format='GLB', use_selection=True, export_yup=True,
                          export_apply=False, export_morph=True, export_morph_normal=False, export_vertex_color='ACTIVE',
                          export_normals=True, export_texcoords=True, export_materials='EXPORT', export_animations=False)
log(f"xuất glb: {os.path.getsize(os.path.join(OUT, 'ida_bl.glb')) / 1e6:.1f} MB; đỉnh: {meta['counts']}")
if BLEND:
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(BLEND), compress=True)
    log('lưu ' + BLEND)
