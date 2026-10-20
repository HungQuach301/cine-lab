"""NC-CPU · CẢNH BLENDER từ bản xuất k2v (design/pt/cpu/nc_export.js) — dùng chung cho 3 việc:
  nuong  (cách A): nướng ánh sáng Cycles CPU vào ảnh phủ hộp [E0,N0,E1,N1] (UV phẳng của địa hình) → bake.png + meta.json cho design/k2v/tl/nc/bake.js
  cycles (cách B): dựng thẳng bằng Cycles CPU (mẫu thấp + OIDN) — mức 'nhanh' / 'dep'
  eevee  (cách C): dựng bằng Eevee (OpenGL phần mềm llvmpipe trong container)
Vật liệu ĐỨNG RIÊNG (không ghép albedo màn hình của k2v): nền = ảnh albedo nhìn thẳng xuống của chính cảnh k2v (nc_topo.js, có vân CC0 theo lớp phủ + đường/vườn);
nhà = màu đỉnh k2v × vữa CC0 + cửa sổ thủ tục theo toạ độ thế giới + ngói CC0 trên mái dốc; công sự = màu đỉnh × đá CC0; bụi/cây = màu bản sao; nước = Principled
(Fresnel, sóng bump động); trời = Sky Texture vật lý theo hướng nắng (ngày) / trời đêm + trăng; sương khí quyển e^(−σd) trong MỌI vật liệu (Camera Data) — cùng σ và màu với cách A.
  /opt/bpy/bin/python design/pt/cpu/nc_blend.py -- <thư mục xuất> <việc> <ra> [--topo <thư mục topo>[,<thư mục topo 2>]] [--tex <thư mục vân>] [--spp N] [--res WxH]
      [--threads N] [--box E0,N0,E1,N1 --bres m] [--fires <json>] [--night 0..1] [--anim <json đường máy>] [--frames a:b] [--persist]"""
import sys, os, json, math, time
import numpy as np
import bpy, mathutils

a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
D, JOB, OUT = a[0], a[1], a[2]
opt = {}
i = 3
while i < len(a):
    if a[i].startswith('--'):
        if i + 1 < len(a) and not a[i + 1].startswith('--'): opt[a[i]] = a[i + 1]; i += 2
        else: opt[a[i]] = '1'; i += 1
    else: i += 1
T0 = time.time()
TEX = opt.get('--tex', '/var/tmp/cine-out/nc/tex'); TH = int(opt.get('--threads', 4)); NIGHT = float(opt.get('--night', 0))
HAZE_S, HAZE_C = float(opt.get('--haze', 1 / 16000)), (0.66, 0.74, 0.84)
M = json.load(open(os.path.join(D, 'manifest.json')))
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
S = mathutils.Matrix(((1, 0, 0, 0), (0, 0, -1, 0), (0, 1, 0, 0), (0, 0, 0, 1)))   # three (x E, y cao, z −N) → Blender (x E, y N, z cao)
def load(i):
    meta = M['bufs'][i]; dt = {'Float32Array': np.float32, 'Uint32Array': np.uint32, 'Uint16Array': np.uint16}[meta['type']]
    return np.fromfile(os.path.join(D, f'b{i}.bin'), dtype=dt)
def img(p, color=True):
    im = bpy.data.images.load(p, check_existing=True)
    if not color: im.colorspace_settings.name = 'Non-Color'
    return im

# ---------------------------------------------------------------- nút dùng chung
def N(nt, t, **kw):
    n = nt.nodes.new(t)
    for k, v in kw.items(): setattr(n, k, v)
    return n
def haze_wrap(m, emit_k=1.0):
    """bọc đầu ra vật liệu: mix(bề mặt, phát xạ màu sương, 1 − e^(−σ·d)); d = khoảng cách tới máy (Camera Data). Đêm: màu sương tối theo NIGHT."""
    nt = m.node_tree; out = [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'][0]; src = out.inputs['Surface'].links[0].from_socket
    cd = N(nt, 'ShaderNodeCameraData'); mu = N(nt, 'ShaderNodeMath', operation='MULTIPLY'); mu.inputs[1].default_value = -HAZE_S
    ex = N(nt, 'ShaderNodeMath', operation='EXPONENT'); sub = N(nt, 'ShaderNodeMath', operation='SUBTRACT'); sub.inputs[0].default_value = 1.0
    em = N(nt, 'ShaderNodeEmission'); k = 1 - NIGHT; em.inputs['Color'].default_value = (*[c * k + cn * NIGHT for c, cn in zip(HAZE_C, (0.035, 0.05, 0.09))], 1); em.inputs['Strength'].default_value = SKY_K * emit_k
    mx = N(nt, 'ShaderNodeMixShader'); L = nt.links
    L.new(cd.outputs['View Distance'], mu.inputs[0]); L.new(mu.outputs[0], ex.inputs[0]); L.new(ex.outputs[0], sub.inputs[1]); L.new(sub.outputs[0], mx.inputs['Fac'])
    L.new(src, mx.inputs[1]); L.new(em.outputs[0], mx.inputs[2]); L.new(mx.outputs[0], out.inputs['Surface'])
def box_tex(nt, path, scale, color=True, blend=0.25):
    tc = N(nt, 'ShaderNodeTexCoord'); mp = N(nt, 'ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1 / scale,) * 3
    t = N(nt, 'ShaderNodeTexImage', projection='BOX', projection_blend=blend); t.image = img(path, color)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], t.inputs['Vector']); return t
def attr(nt, name, kind='GEOMETRY'):
    n = N(nt, 'ShaderNodeAttribute'); n.attribute_name = name; n.attribute_type = kind; return n
def principled(m):
    b = m.node_tree.nodes['Principled BSDF']
    for k in ('Specular IOR Level',):
        if k in b.inputs: b.inputs[k].default_value = 0.2
    return b

TOPO = []   # [(ảnh, hộp E0, N0, E1, N1)] ưu tiên ảnh đầu (mịn)
def topo_image(d):
    T = json.load(open(os.path.join(d, 'topo.json'))); W = int(round((T['box'][2] - T['box'][0]) / T['res'])); H = int(round((T['box'][3] - T['box'][1]) / T['res']))
    cache = os.path.join(d, 'topo_full.png')
    if not os.path.exists(cache):
        import imageio.v3 as iio
        A = np.zeros((H, W, 4), np.uint8)
        for t in T['tiles']:
            p = iio.imread(os.path.join(d, t['file'])); x0 = t['i'] * T['TILE']; y0 = t['j'] * T['TILE']; A[y0:y0 + p.shape[0], x0:x0 + p.shape[1]] = p[:, :, :4] if p.shape[2] == 4 else np.dstack([p, np.full(p.shape[:2], 255, np.uint8)])
        iio.imwrite(cache, A)
    return img(cache), T['box']

def mat_ground():
    m = bpy.data.materials.new('m_dia_hinh'); m.use_nodes = True; nt = m.node_tree; b = principled(m); b.inputs['Roughness'].default_value = 0.95; L = nt.links
    tc = N(nt, 'ShaderNodeTexCoord'); col = None; alpha_prev = None
    for k, (im, bx) in enumerate(TOPO):
        mp = N(nt, 'ShaderNodeMapping'); mp.inputs['Location'].default_value = (-bx[0] / (bx[2] - bx[0]), -bx[1] / (bx[3] - bx[1]), 0); mp.inputs['Scale'].default_value = (1 / (bx[2] - bx[0]), 1 / (bx[3] - bx[1]), 1)
        mp.vector_type = 'TEXTURE'   # (P − E0)/(E1 − E0) theo trục — dùng kiểu POINT với vị trí/thu phóng tách rời
        mp.vector_type = 'POINT'; mp.inputs['Scale'].default_value = (1 / (bx[2] - bx[0]), 1 / (bx[3] - bx[1]), 1); mp.inputs['Location'].default_value = (-bx[0] / (bx[2] - bx[0]), -bx[1] / (bx[3] - bx[1]), 0)
        t = N(nt, 'ShaderNodeTexImage', extension='CLIP', interpolation='Cubic'); t.image = im; L.new(tc.outputs['Object'], mp.inputs['Vector']); L.new(mp.outputs['Vector'], t.inputs['Vector'])
        if col is None: col, alpha_prev = t.outputs['Color'], t.outputs['Alpha']
        else:   # ảnh mịn (trước) phủ lên ảnh thô (sau) theo alpha của ảnh mịn
            mx = N(nt, 'ShaderNodeMix', data_type='RGBA'); L.new(alpha_prev, mx.inputs['Factor']); L.new(t.outputs['Color'], mx.inputs[6]); L.new(col, mx.inputs[7]); col = mx.outputs[2]
            mxa = N(nt, 'ShaderNodeMath', operation='MAXIMUM'); L.new(alpha_prev, mxa.inputs[0]); L.new(t.outputs['Alpha'], mxa.inputs[1]); alpha_prev = mxa.outputs[0]
    if col is None: b.inputs['Base Color'].default_value = (0.32, 0.30, 0.22, 1)
    else:
        L.new(col, b.inputs['Base Color'])
        # gồ ghề vi mô từ độ sáng albedo (cùng nguồn với màu → khớp vân)
        bm = N(nt, 'ShaderNodeBump'); bm.inputs['Strength'].default_value = 0.35; bm.inputs['Distance'].default_value = 0.4; L.new(col, bm.inputs['Height']); L.new(bm.outputs['Normal'], b.inputs['Normal'])
    m['kind'] = 'dia_hinh'; return m

def mat_city():
    """tường: màu đỉnh k2v × vữa CC0; cửa sổ thủ tục (tầng 3 m, gian 3 m, ô 1,1 × 1,5 m) theo toạ độ dọc tường = dot(P.xy, tiếp tuyến), chỉ mặt đứng;
    mái dốc (pháp tuyến z 0,25–0,97): ngói CC0; mái bằng: màu đỉnh."""
    m = bpy.data.materials.new('m_nha'); m.use_nodes = True; nt = m.node_tree; b = principled(m); b.inputs['Roughness'].default_value = 0.88; L = nt.links
    vc = attr(nt, 'col'); geo = N(nt, 'ShaderNodeNewGeometry')
    pl = box_tex(nt, os.path.join(TEX, 'white_plaster_rough_01_diff_1k.jpg'), 1.6); tl = box_tex(nt, os.path.join(TEX, 'clay_roof_tiles_02_diff_1k.jpg'), 2.5)
    # độ sáng vữa (÷ ~0,55) nhân màu đỉnh
    bw = N(nt, 'ShaderNodeRGBToBW'); L.new(pl.outputs['Color'], bw.inputs[0]); kpl = N(nt, 'ShaderNodeMath', operation='MULTIPLY'); kpl.inputs[1].default_value = 1 / 0.55; L.new(bw.outputs[0], kpl.inputs[0])
    mpl = N(nt, 'ShaderNodeMix', data_type='RGBA', blend_type='MULTIPLY'); mpl.inputs['Factor'].default_value = 0.6; L.new(vc.outputs['Color'], mpl.inputs[6]); L.new(kpl.outputs[0], mpl.inputs[7])
    # tiếp tuyến ngang t = (−Ny, Nx); u = P·t ; v = P.z
    sep = N(nt, 'ShaderNodeSeparateXYZ'); L.new(geo.outputs['Normal'], sep.inputs[0]); sp = N(nt, 'ShaderNodeSeparateXYZ'); L.new(geo.outputs['Position'], sp.inputs[0])
    m1 = N(nt, 'ShaderNodeMath', operation='MULTIPLY'); L.new(sp.outputs['X'], m1.inputs[0]); L.new(sep.outputs['Y'], m1.inputs[1])
    m2 = N(nt, 'ShaderNodeMath', operation='MULTIPLY'); L.new(sp.outputs['Y'], m2.inputs[0]); L.new(sep.outputs['X'], m2.inputs[1])
    u = N(nt, 'ShaderNodeMath', operation='SUBTRACT'); L.new(m2.outputs[0], u.inputs[0]); L.new(m1.outputs[0], u.inputs[1])
    def frac_band(src, period, lo, hi):   # 1 trong khoảng [lo, hi] của chu kỳ
        d = N(nt, 'ShaderNodeMath', operation='DIVIDE'); d.inputs[1].default_value = period; L.new(src, d.inputs[0]); f = N(nt, 'ShaderNodeMath', operation='FRACT'); L.new(d.outputs[0], f.inputs[0])
        g1 = N(nt, 'ShaderNodeMath', operation='GREATER_THAN'); g1.inputs[1].default_value = lo; L.new(f.outputs[0], g1.inputs[0]); g2 = N(nt, 'ShaderNodeMath', operation='LESS_THAN'); g2.inputs[1].default_value = hi; L.new(f.outputs[0], g2.inputs[0])
        mm = N(nt, 'ShaderNodeMath', operation='MULTIPLY'); L.new(g1.outputs[0], mm.inputs[0]); L.new(g2.outputs[0], mm.inputs[1]); return mm.outputs[0]
    wu = frac_band(u.outputs[0], 3.0, 0.32, 0.68); wv = frac_band(sp.outputs['Z'], 3.0, 0.30, 0.80)
    wall = N(nt, 'ShaderNodeMath', operation='LESS_THAN'); wall.inputs[1].default_value = 0.25; az = N(nt, 'ShaderNodeMath', operation='ABSOLUTE'); L.new(sep.outputs['Z'], az.inputs[0]); L.new(az.outputs[0], wall.inputs[0])
    win = N(nt, 'ShaderNodeMath', operation='MULTIPLY'); L.new(wu, win.inputs[0]); L.new(wv, win.inputs[1]); win2 = N(nt, 'ShaderNodeMath', operation='MULTIPLY'); L.new(win.outputs[0], win2.inputs[0]); L.new(wall.outputs[0], win2.inputs[1])
    # mái dốc → ngói
    rf1 = N(nt, 'ShaderNodeMath', operation='GREATER_THAN'); rf1.inputs[1].default_value = 0.25; L.new(sep.outputs['Z'], rf1.inputs[0]); rf2 = N(nt, 'ShaderNodeMath', operation='LESS_THAN'); rf2.inputs[1].default_value = 0.97; L.new(sep.outputs['Z'], rf2.inputs[0])
    rf = N(nt, 'ShaderNodeMath', operation='MULTIPLY'); L.new(rf1.outputs[0], rf.inputs[0]); L.new(rf2.outputs[0], rf.inputs[1])
    tcol = N(nt, 'ShaderNodeMix', data_type='RGBA', blend_type='MULTIPLY'); tcol.inputs['Factor'].default_value = 0.85; L.new(vc.outputs['Color'], tcol.inputs[6]); L.new(tl.outputs['Color'], tcol.inputs[7])
    kt = N(nt, 'ShaderNodeMix', data_type='RGBA'); kt.inputs[7].default_value = (1.7, 1.7, 1.7, 1)
    roofc = N(nt, 'ShaderNodeMix', data_type='RGBA'); L.new(rf.outputs[0], roofc.inputs['Factor']); L.new(mpl.outputs[2], roofc.inputs[6]); L.new(tcol.outputs[2], roofc.inputs[7])
    glass = N(nt, 'ShaderNodeMix', data_type='RGBA'); L.new(win2.outputs[0], glass.inputs['Factor']); L.new(roofc.outputs[2], glass.inputs[6]); glass.inputs[7].default_value = (0.035, 0.04, 0.05, 1)
    L.new(glass.outputs[2], b.inputs['Base Color'])
    rg = N(nt, 'ShaderNodeMapRange'); L.new(win2.outputs[0], rg.inputs['Value']); rg.inputs['To Min'].default_value = 0.88; rg.inputs['To Max'].default_value = 0.12; L.new(rg.outputs['Result'], b.inputs['Roughness'])
    if NIGHT > 0 and 'Emission Color' in b.inputs:   # cửa sổ sáng đêm: chỉ ≥ 1950 (cảnh đêm 1782: tắt) — để 0
        pass
    m['kind'] = 'nha'; return m

def mat_vc(kind, tex=None, scale=1.7, rough=0.9, k=0.5, base=(0.5, 0.5, 0.5)):
    m = bpy.data.materials.new('m_' + kind); m.use_nodes = True; nt = m.node_tree; b = principled(m); b.inputs['Roughness'].default_value = rough; L = nt.links
    vc = attr(nt, 'col'); has = N(nt, 'ShaderNodeMix', data_type='RGBA'); has.inputs[6].default_value = (*base, 1); L.new(vc.outputs['Color'], has.inputs[7]); L.new(vc.outputs['Alpha'], has.inputs['Factor'])
    c = has.outputs[2]
    if tex:
        t = box_tex(nt, os.path.join(TEX, tex), scale); bw = N(nt, 'ShaderNodeRGBToBW'); L.new(t.outputs['Color'], bw.inputs[0]); kk = N(nt, 'ShaderNodeMath', operation='MULTIPLY'); kk.inputs[1].default_value = 1 / 0.5; L.new(bw.outputs[0], kk.inputs[0])
        mm = N(nt, 'ShaderNodeMix', data_type='RGBA', blend_type='MULTIPLY'); mm.inputs['Factor'].default_value = k; L.new(c, mm.inputs[6]); L.new(kk.outputs[0], mm.inputs[7]); c = mm.outputs[2]
        bm = N(nt, 'ShaderNodeBump'); bm.inputs['Strength'].default_value = 0.5; L.new(bw.outputs[0], bm.inputs['Height']); L.new(bm.outputs['Normal'], b.inputs['Normal'])
    L.new(c, b.inputs['Base Color'])
    if kind == 'co':
        tlu = N(nt, 'ShaderNodeBsdfTranslucent'); L.new(c, tlu.inputs['Color']); mx = N(nt, 'ShaderNodeMixShader'); mx.inputs['Fac'].default_value = 0.4
        o = [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'][0]; L.new(b.outputs[0], mx.inputs[1]); L.new(tlu.outputs[0], mx.inputs[2]); L.new(mx.outputs[0], o.inputs['Surface'])
    m['kind'] = kind; return m

def mat_inst(kind, base=(0.12, 0.16, 0.07)):   # bụi/cây: màu bản sao (thuộc tính 'icol' trên điểm → miền instance)
    m = bpy.data.materials.new('m_' + kind); m.use_nodes = True; nt = m.node_tree; b = principled(m); b.inputs['Roughness'].default_value = 0.85; L = nt.links
    ic = attr(nt, 'icol', 'INSTANCER'); mx = N(nt, 'ShaderNodeMix', data_type='RGBA'); mx.inputs[6].default_value = (*base, 1); L.new(ic.outputs['Color'], mx.inputs[7]); L.new(ic.outputs['Alpha'], mx.inputs['Factor'])
    nz = N(nt, 'ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.4; mm = N(nt, 'ShaderNodeMix', data_type='RGBA', blend_type='MULTIPLY'); mm.inputs['Factor'].default_value = 0.35
    L.new(mx.outputs[2], mm.inputs[6]); L.new(nz.outputs['Color'], mm.inputs[7]); L.new(mm.outputs[2], b.inputs['Base Color'])
    bm = N(nt, 'ShaderNodeBump'); bm.inputs['Strength'].default_value = 0.6; L.new(nz.outputs['Fac'], bm.inputs['Height']); L.new(bm.outputs['Normal'], b.inputs['Normal'])
    m['kind'] = kind; return m

MATS = {}
def mat(kind, inst=False, hasC=True):
    key = kind + ('_i' if inst else '') + ('' if hasC else '_0')
    if key in MATS: return MATS[key]
    if kind == 'dia_hinh': m = mat_ground()
    elif kind == 'nha': m = mat_city()
    elif inst and kind in ('cay', 'bui'): m = mat_inst(kind, (0.10, 0.15, 0.06) if kind == 'cay' else (0.15, 0.18, 0.09))
    elif kind in ('cong_su', 'do_nat'): m = mat_vc(kind, 'seaworn_sandstone_brick_diff_1k.jpg', 1.69, 0.9, 0.55, (0.62, 0.55, 0.42))
    elif kind == 'nguoi': m = mat_vc(kind, None, rough=0.8, base=(0.4, 0.3, 0.25))
    elif kind == 'co': m = mat_vc(kind, None, rough=0.7, base=(0.6, 0.6, 0.6))
    else: m = mat_vc(kind + ('_i' if inst else ''), None, rough=0.8, base=(0.45, 0.42, 0.38))
    if not hasC:   # không có màu đỉnh: bỏ nút thuộc tính 'col' (Cycles trả alpha 1, màu 0 → đen)
        for n in list(m.node_tree.nodes):
            if n.type == 'ATTRIBUTE' and n.attribute_name == 'col':
                for l in list(n.outputs['Alpha'].links): l.to_socket.node.inputs['Factor'].default_value = 0.0 if 'Factor' in l.to_socket.node.inputs else 0
                for l in list(n.outputs['Alpha'].links) + list(n.outputs['Color'].links): m.node_tree.links.remove(l)
                m.node_tree.nodes.remove(n)
        m.name = m.name + '_0'
    MATS[key] = m; return m

# ---------------------------------------------------------------- hình học (cùng phép đổi trục với scripts/k2tl/cy6.py)
def mesh_from(P, I, name, C=None, smooth=False):
    me = bpy.data.meshes.new(name); n = len(P) // 3
    V = P.reshape(-1, 3)[:, [0, 2, 1]] * np.array([1, -1, 1], np.float32)
    if I is None: I = np.arange(n, dtype=np.uint32)
    I = I.reshape(-1, 3)
    me.vertices.add(n); me.vertices.foreach_set('co', V.ravel())
    nl = len(I); me.loops.add(nl * 3); me.loops.foreach_set('vertex_index', I.ravel().astype(np.int32))
    me.polygons.add(nl); me.polygons.foreach_set('loop_start', np.arange(0, nl * 3, 3, dtype=np.int32)); me.polygons.foreach_set('loop_total', np.full(nl, 3, np.int32))
    me.update(calc_edges=False); me.validate(clean_customdata=False)
    me.polygons.foreach_set('use_smooth', np.full(nl, smooth, bool))
    if C is not None and len(C) == n * 3:
        ca = me.color_attributes.new('col', 'FLOAT_COLOR', 'POINT'); ca.data.foreach_set('color', np.hstack([C.reshape(-1, 3), np.ones((n, 1), np.float32)]).ravel())
    return me
col = bpy.data.collections.new('k2v'); sc.collection.children.link(col); base_col = bpy.data.collections.new('k2v_goc'); sc.collection.children.link(base_col)
stat = {'vat': 0, 'tam_giac': 0, 'ban_sao': 0, 'loai': {}}
if '--topo' in opt:
    for d in opt['--topo'].split(','): TOPO.append(topo_image(d))
TERR = []
SKY_K = 1.0
for k, o in enumerate(M['objs']):
    kind = o['kind']
    if kind == 'khac' and o['name'] and 'Sprite' in o['name']: continue
    P = load(o['buf']['P']); I = load(o['buf']['I']) if 'I' in o['buf'] else None; C = load(o['buf']['C']) if 'C' in o['buf'] else None
    me = mesh_from(P, I, f"o{k}_{kind}", C, smooth=kind in ('dia_hinh', 'cay', 'bui'))
    inst = 'M' in o['buf']; me.materials.append(mat(kind, inst, C is not None or kind == 'dia_hinh' or (inst and kind in ('cay', 'bui'))))
    if inst:
        base = bpy.data.objects.new(f"goc{k}", me); base_col.objects.link(base)
        Mx = load(o['buf']['M']).reshape(-1, 16); IC = load(o['buf']['IC']).reshape(-1, 3) if 'IC' in o['buf'] else None
        pts, rot, scl, keep = [], [], [], []
        for q, e in enumerate(Mx):
            m3 = mathutils.Matrix([e[0:4], e[4:8], e[8:12], e[12:16]]).transposed(); mb = S @ m3 @ S.inverted(); lo, ro, sc_ = mb.decompose()
            if sc_.length < 1e-6: continue
            pts.append(lo); rot.append(ro.to_euler()); scl.append(sc_); keep.append(q)
        if not pts: continue
        pm = bpy.data.meshes.new(f"pts{k}"); pm.vertices.add(len(pts)); pm.vertices.foreach_set('co', np.array(pts, np.float32).ravel())
        ra = pm.attributes.new('rot', 'FLOAT_VECTOR', 'POINT'); ra.data.foreach_set('vector', np.array([tuple(r) for r in rot], np.float32).ravel())
        sa = pm.attributes.new('scl', 'FLOAT_VECTOR', 'POINT'); sa.data.foreach_set('vector', np.array([tuple(s) for s in scl], np.float32).ravel())
        if IC is not None:
            ia = pm.color_attributes.new('icol', 'FLOAT_COLOR', 'POINT'); ia.data.foreach_set('color', np.hstack([IC[keep], np.ones((len(keep), 1), np.float32)]).ravel())
        ob = bpy.data.objects.new(f"inst{k}_{kind}", pm); col.objects.link(ob)
        gm = ob.modifiers.new('ban_sao', 'NODES'); ng = bpy.data.node_groups.new(f'gn{k}', 'GeometryNodeTree'); gm.node_group = ng
        ng.interface.new_socket('Geometry', in_out='INPUT', socket_type='NodeSocketGeometry'); ng.interface.new_socket('Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
        gi = ng.nodes.new('NodeGroupInput'); go = ng.nodes.new('NodeGroupOutput'); mtp = ng.nodes.new('GeometryNodeMeshToPoints'); iop = ng.nodes.new('GeometryNodeInstanceOnPoints'); oi = ng.nodes.new('GeometryNodeObjectInfo'); oi.inputs['Object'].default_value = base
        rr = ng.nodes.new('GeometryNodeInputNamedAttribute'); rr.data_type = 'FLOAT_VECTOR'; rr.inputs['Name'].default_value = 'rot'
        ss = ng.nodes.new('GeometryNodeInputNamedAttribute'); ss.data_type = 'FLOAT_VECTOR'; ss.inputs['Name'].default_value = 'scl'
        L = ng.links; L.new(gi.outputs[0], mtp.inputs['Mesh']); L.new(mtp.outputs['Points'], iop.inputs['Points']); L.new(oi.outputs['Geometry'], iop.inputs['Instance'])
        L.new(rr.outputs['Attribute'], iop.inputs['Rotation']); L.new(ss.outputs['Attribute'], iop.inputs['Scale']); L.new(iop.outputs['Instances'], go.inputs[0])
        stat['ban_sao'] += len(pts)
    else:
        ob = bpy.data.objects.new(f"o{k}_{kind}", me); col.objects.link(ob)
        if kind == 'dia_hinh': TERR.append(ob)
    stat['vat'] += 1; stat['tam_giac'] += o['nt'] * (o.get('inst') or 1); stat['loai'][kind] = stat['loai'].get(kind, 0) + 1
base_col.hide_render = True
T_LOAD = time.time() - T0

# ---------------------------------------------------------------- nước, trời, nắng, máy
C = M['cam']; Su = M['sun']; sd = (S @ mathutils.Vector((*Su['dir'], 0)).to_4d()).to_3d().normalized()
sun_el = math.degrees(math.asin(max(-1, min(1, sd.z))))
def water():
    bpy.ops.mesh.primitive_plane_add(size=60000, location=(0, 0, 0)); wp = bpy.context.active_object; wp.name = 'nuoc'
    m = bpy.data.materials.new('m_nuoc'); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']; L = nt.links
    b.inputs['Base Color'].default_value = (0.010, 0.045, 0.070, 1); b.inputs['Roughness'].default_value = 0.035; b.inputs['IOR'].default_value = 1.333
    if 'Specular IOR Level' in b.inputs: b.inputs['Specular IOR Level'].default_value = 0.5
    tc = N(nt, 'ShaderNodeTexCoord'); w1 = N(nt, 'ShaderNodeTexWave'); w1.inputs['Scale'].default_value = 0.035; w1.inputs['Distortion'].default_value = 6; w1.inputs['Detail'].default_value = 4
    w2 = N(nt, 'ShaderNodeTexNoise'); w2.inputs['Scale'].default_value = 0.12; w2.inputs['Detail'].default_value = 6
    w3 = N(nt, 'ShaderNodeTexNoise'); w3.inputs['Scale'].default_value = 0.9; w3.inputs['Detail'].default_value = 3
    for w in (w1, w2, w3): L.new(tc.outputs['Object'], w.inputs['Vector'])
    if hasattr(w2, 'noise_dimensions'): w2.noise_dimensions = '4D'; w3.noise_dimensions = '4D'
    ad = N(nt, 'ShaderNodeMath', operation='ADD'); L.new(w1.outputs['Fac'], ad.inputs[0]); L.new(w2.outputs['Fac'], ad.inputs[1]); ad2 = N(nt, 'ShaderNodeMath', operation='MULTIPLY_ADD'); ad2.inputs[1].default_value = 0.3
    L.new(w3.outputs['Fac'], ad2.inputs[0]); L.new(ad.outputs[0], ad2.inputs[2])
    bm = N(nt, 'ShaderNodeBump'); bm.inputs['Strength'].default_value = 0.22; bm.inputs['Distance'].default_value = 0.6; L.new(ad2.outputs[0], bm.inputs['Height']); L.new(bm.outputs['Normal'], b.inputs['Normal'])
    wp.data.materials.append(m); m['kind'] = 'nuoc'; return wp, (w2, w3)
WATER, WN = water()
cam = bpy.data.cameras.new('cam'); cob = bpy.data.objects.new('cam', cam); sc.collection.objects.link(cob); sc.camera = cob
q = C['quat']; m3 = mathutils.Quaternion((q[3], q[0], q[1], q[2])).to_matrix().to_4x4(); m3.translation = mathutils.Vector(C['pos']); cob.matrix_world = S @ m3
cam.sensor_fit = 'VERTICAL'; cam.angle_y = math.radians(C['fov']); cam.clip_start = max(1.0, C['near']); cam.clip_end = 90000
RES = opt.get('--res'); W, H = (C['W'], C['H']) if not RES else map(int, RES.split('x')); sc.render.resolution_x, sc.render.resolution_y = W, H; sc.render.resolution_percentage = 100
sl = bpy.data.lights.new('sun', 'SUN'); sl.angle = math.radians(0.53)
so = bpy.data.objects.new('sun', sl); sc.collection.objects.link(so); so.rotation_euler = sd.to_track_quat('Z', 'Y').to_euler()
wld = bpy.data.worlds.new('w'); sc.world = wld; wld.use_nodes = True; wnt = wld.node_tree; wnt.nodes.clear()
bg = wnt.nodes.new('ShaderNodeBackground'); wo = wnt.nodes.new('ShaderNodeOutputWorld'); wnt.links.new(bg.outputs[0], wo.inputs[0])
SKYNODE = None
def sky_day():
    """trời gradient như k2v (water.js skyCol: chân trời sáng ngả xám-lam → thiên đỉnh lam) — tia máy/tia bóng thấy trời SÁNG (như k2v vẽ trời),
    tia khuếch tán nhận trời DỊU khớp ánh trời bán cầu k2v (bức xạ mặt phẳng ≈ hemiI × màu trời) → cùng tỉ lệ nắng/trời với cách A."""
    L = wnt.links; tc = wnt.nodes.new('ShaderNodeTexCoord'); sx = wnt.nodes.new('ShaderNodeSeparateXYZ'); L.new(tc.outputs['Generated'], sx.inputs[0])
    cl = wnt.nodes.new('ShaderNodeClamp'); L.new(sx.outputs['Z'], cl.inputs['Value']); pw = wnt.nodes.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 0.5; L.new(cl.outputs[0], pw.inputs[0])
    vis = wnt.nodes.new('ShaderNodeMix'); vis.data_type = 'RGBA'; L.new(pw.outputs[0], vis.inputs['Factor']); vis.inputs[6].default_value = (*HAZE_C, 1); vis.inputs[7].default_value = (0.20, 0.40, 0.78, 1)
    hm = M['hemi']; k = hm['intensity'] * 1.15
    dif = wnt.nodes.new('ShaderNodeMix'); dif.data_type = 'RGBA'; L.new(cl.outputs[0], dif.inputs['Factor'])
    dif.inputs[6].default_value = (*[c * k for c in hm['sky']], 1); dif.inputs[7].default_value = (*[c * k * 0.85 for c in hm['sky']], 1)
    lp = wnt.nodes.new('ShaderNodeLightPath'); mx = wnt.nodes.new('ShaderNodeMath'); mx.operation = 'MAXIMUM'; L.new(lp.outputs['Is Camera Ray'], mx.inputs[0]); L.new(lp.outputs['Is Glossy Ray'], mx.inputs[1])
    sel = wnt.nodes.new('ShaderNodeMix'); sel.data_type = 'RGBA'; L.new(mx.outputs[0], sel.inputs['Factor']); L.new(dif.outputs[2], sel.inputs[6]); L.new(vis.outputs[2], sel.inputs[7])
    L.new(sel.outputs[2], bg.inputs['Color']); bg.inputs['Strength'].default_value = 1.0
def sky_night():
    """trời đêm như k2v (water.js skyCol, uNight = 1): thiên đỉnh (0,018; 0,030; 0,070), chân trời + (0,06; 0,075; 0,11)·(1 − h)⁴ — tia máy/bóng thấy trời này;
    tia khuếch tán: ánh trời đêm bán cầu k2v (hemiI × màu trời đêm)."""
    L = wnt.links; tc = wnt.nodes.new('ShaderNodeTexCoord'); sx = wnt.nodes.new('ShaderNodeSeparateXYZ'); L.new(tc.outputs['Generated'], sx.inputs[0])
    cl = wnt.nodes.new('ShaderNodeClamp'); L.new(sx.outputs['Z'], cl.inputs['Value']); om = wnt.nodes.new('ShaderNodeMath'); om.operation = 'SUBTRACT'; om.inputs[0].default_value = 1.0; L.new(cl.outputs[0], om.inputs[1])
    p4 = wnt.nodes.new('ShaderNodeMath'); p4.operation = 'POWER'; p4.inputs[1].default_value = 4.0; L.new(om.outputs[0], p4.inputs[0])
    vis = wnt.nodes.new('ShaderNodeMix'); vis.data_type = 'RGBA'; L.new(p4.outputs[0], vis.inputs['Factor']); vis.inputs[6].default_value = (0.018, 0.030, 0.070, 1); vis.inputs[7].default_value = (0.078, 0.105, 0.180, 1)
    hm = M['hemi']; k = hm['intensity']; dif = wnt.nodes.new('ShaderNodeRGB'); dif.outputs[0].default_value = (*[c * k for c in hm['sky']], 1)
    lp = wnt.nodes.new('ShaderNodeLightPath'); mx = wnt.nodes.new('ShaderNodeMath'); mx.operation = 'MAXIMUM'; L.new(lp.outputs['Is Camera Ray'], mx.inputs[0]); L.new(lp.outputs['Is Glossy Ray'], mx.inputs[1])
    sel = wnt.nodes.new('ShaderNodeMix'); sel.data_type = 'RGBA'; L.new(mx.outputs[0], sel.inputs['Factor']); L.new(dif.outputs[0], sel.inputs[6]); L.new(vis.outputs[2], sel.inputs[7])
    L.new(sel.outputs[2], bg.inputs['Color']); bg.inputs['Strength'].default_value = 1.0
if NIGHT < 0.5:
    sky_day(); sl.energy = Su['intensity']; sl.color = Su['color'][:3]
else:
    sky_night(); sl.energy = Su['intensity']; sl.color = Su['color'][:3]
for m in list(bpy.data.materials):
    if m.get('kind') and m.use_nodes: haze_wrap(m)

# ---------------------------------------------------------------- lửa (pin nổi cháy) : đèn điểm + ngọn lửa phát xạ
FIRES = json.loads(opt['--fires']) if '--fires' in opt else []
FIRE_OBJ = []
def add_fires():
    fm = bpy.data.materials.new('m_lua'); fm.use_nodes = True; nt = fm.node_tree; nt.nodes.clear(); out = N(nt, 'ShaderNodeOutputMaterial'); em = N(nt, 'ShaderNodeEmission')
    nz = N(nt, 'ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 0.35; cr = N(nt, 'ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = (1.0, 0.25, 0.03, 1); cr.color_ramp.elements[1].color = (1.0, 0.75, 0.30, 1)
    nt.links.new(nz.outputs['Fac'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], em.inputs['Color']); em.inputs['Strength'].default_value = 60.0; nt.links.new(em.outputs[0], out.inputs['Surface'])
    for f in FIRES:
        e, n = f['at']; z = f.get('z', 3.0); s = f.get('size', 30) / 30.0
        for j, (dx, dy, k) in enumerate(((0, 0, 1.0), (-11, 3, 0.7), (10, -4, 0.75))):   # 3 ngọn lửa trên boong pin nổi (dài ≈ 45 m)
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1, location=(e + dx * s, n + dy * s, z + 4 * s * k)); fo = bpy.context.active_object; fo.scale = (5 * s * k, 3 * s * k, 7 * s * k); fo.data.materials.append(fm); fo.name = 'lua'
            if j: FIRE_OBJ.append((fo, None, f))
        li = bpy.data.lights.new('lua', 'POINT'); li.energy = f.get('W', 2.5e6) * s; li.color = (1.0, 0.45, 0.14); li.shadow_soft_size = 8 * s
        lo = bpy.data.objects.new('lua', li); lo.location = (e, n, z + 12 * s); sc.collection.objects.link(lo); FIRE_OBJ.append((fo, lo, f))
if FIRES: add_fires()
SMOKE = []
def add_smoke():
    """cột khói THỂ TÍCH (Principled Volume, mật độ nhiễu 4D theo thời gian, nghiêng theo gió) trên mỗi đám cháy — thử chi phí thể tích ở Cycles CPU."""
    vm = bpy.data.materials.new('m_khoi'); vm.use_nodes = True; nt = vm.node_tree; nt.nodes.clear(); out = N(nt, 'ShaderNodeOutputMaterial'); pv = N(nt, 'ShaderNodeVolumePrincipled'); L = nt.links
    tc = N(nt, 'ShaderNodeTexCoord'); nz = N(nt, 'ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 2.2; nz.inputs['Detail'].default_value = 4
    if hasattr(nz, 'noise_dimensions'): nz.noise_dimensions = '4D'
    L.new(tc.outputs['Generated'], nz.inputs['Vector']); cr = N(nt, 'ShaderNodeMapRange'); cr.inputs['From Min'].default_value = 0.45; cr.inputs['From Max'].default_value = 0.75; L.new(nz.outputs['Fac'], cr.inputs['Value'])
    sx = N(nt, 'ShaderNodeSeparateXYZ'); L.new(tc.outputs['Generated'], sx.inputs[0]); fall = N(nt, 'ShaderNodeMapRange'); fall.inputs['From Min'].default_value = 0.0; fall.inputs['From Max'].default_value = 1.0; fall.inputs['To Min'].default_value = 1.0; fall.inputs['To Max'].default_value = 0.15; L.new(sx.outputs['Z'], fall.inputs['Value'])
    # mép: hình trụ mềm theo khoảng cách tới trục (x, y quanh 0,5)
    vx = N(nt, 'ShaderNodeVectorMath', operation='SUBTRACT'); vx.inputs[1].default_value = (0.5, 0.5, 0); L.new(tc.outputs['Generated'], vx.inputs[0]); m2 = N(nt, 'ShaderNodeVectorMath', operation='MULTIPLY'); m2.inputs[1].default_value = (1, 1, 0); L.new(vx.outputs[0], m2.inputs[0])
    ln = N(nt, 'ShaderNodeVectorMath', operation='LENGTH'); L.new(m2.outputs[0], ln.inputs[0]); edge = N(nt, 'ShaderNodeMapRange'); edge.inputs['From Min'].default_value = 0.5; edge.inputs['From Max'].default_value = 0.25; L.new(ln.outputs['Value'], edge.inputs['Value'])
    d1 = N(nt, 'ShaderNodeMath', operation='MULTIPLY'); L.new(cr.outputs['Result'], d1.inputs[0]); L.new(fall.outputs['Result'], d1.inputs[1]); d2 = N(nt, 'ShaderNodeMath', operation='MULTIPLY'); L.new(d1.outputs[0], d2.inputs[0]); L.new(edge.outputs['Result'], d2.inputs[1])
    d3 = N(nt, 'ShaderNodeMath', operation='MULTIPLY'); d3.inputs[1].default_value = float(opt.get('--smoked', 0.04)); L.new(d2.outputs[0], d3.inputs[0]); L.new(d3.outputs[0], pv.inputs['Density'])
    pv.inputs['Color'].default_value = (0.035, 0.032, 0.03, 1); pv.inputs['Anisotropy'].default_value = 0.3; L.new(pv.outputs[0], out.inputs['Volume']); SMOKE.append(nz)
    for f in FIRES:
        e, n = f['at']; s_ = f.get('size', 30) / 30.0
        bpy.ops.mesh.primitive_cube_add(size=1, location=(e - 40 * s_, n + 10 * s_, 110 * s_)); so_ = bpy.context.active_object; so_.scale = (110 * s_, 110 * s_, 240 * s_); so_.rotation_euler = (0, math.radians(-14), 0)
        so_.data.materials.append(vm); so_.name = 'khoi'
if '--smoke' in opt and FIRES: add_smoke()

def cycles(spp, denoise=True, bounces=(4, 3, 2)):
    sc.render.engine = 'CYCLES'; cy = sc.cycles; cy.device = 'CPU'; cy.samples = spp; cy.use_denoising = denoise; cy.denoiser = 'OPENIMAGEDENOISE'
    cy.max_bounces, cy.diffuse_bounces, cy.glossy_bounces = bounces[0], bounces[1], bounces[2]; cy.transmission_bounces = 2; cy.transparent_max_bounces = 4; cy.volume_bounces = 0
    if hasattr(cy, 'volume_step_rate'): cy.volume_step_rate = float(opt.get('--vstep', 4.0))
    cy.use_adaptive_sampling = True; cy.adaptive_threshold = 0.02; sc.render.threads_mode = 'FIXED'; sc.render.threads = TH
    if hasattr(cy, 'denoising_input_passes'): cy.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
    sc.render.use_persistent_data = '--persist' in opt
    sc.view_settings.view_transform = 'Standard'

info = dict(stat, nap_s=round(T_LOAD, 1), sun_el=round(sun_el, 2), blender=bpy.app.version_string, night=NIGHT)

# ================================================================= VIỆC
if JOB in ('cycles', 'eevee'):
    if JOB == 'cycles': cycles(int(opt.get('--spp', 16)), bounces=tuple(int(x) for x in opt.get('--bounces', '4,3,2').split(',')))
    else:
        sc.render.engine = 'BLENDER_EEVEE'; ee = sc.eevee
        for nm, v in (('taa_render_samples', int(opt.get('--spp', 32))), ('use_shadows', True), ('use_raytracing', True), ('shadow_ray_count', 1), ('shadow_step_count', 6), ('use_volumetric_shadows', False)):
            if hasattr(ee, nm): setattr(ee, nm, v)
        if hasattr(ee, 'ray_tracing_options'):
            ro = ee.ray_tracing_options
            for nm, v in (('resolution_scale', '2'), ('use_denoise', True)):
                if hasattr(ro, nm):
                    try: setattr(ro, nm, v)
                    except Exception: pass
        sc.view_settings.view_transform = 'Standard'
    sc.render.image_settings.file_format = 'OPEN_EXR'; sc.render.image_settings.color_depth = '32'; sc.render.film_transparent = False
    frames = [None]
    if '--anim' in opt:   # đường máy: [{f, p:[E,cao,N], l:[E,cao,N], fov}] (toạ độ ENU như k2v) — một EXR mỗi khung
        A = json.load(open(opt['--anim'])); fr = opt.get('--frames'); lo, hi = (map(int, fr.split(':')) if fr else (0, len(A['keys']) - 1))
        frames = [k for k in A['keys'] if lo <= k['f'] <= hi]
    times = []
    for k in frames:
        if k is not None:
            p = mathutils.Vector((k['p'][0], k['p'][2], k['p'][1])); l = mathutils.Vector((k['l'][0], k['l'][2], k['l'][1]))
            cob.location = p; cob.rotation_euler = (l - p).to_track_quat('-Z', 'Y').to_euler(); cam.angle_y = math.radians(k.get('fov', 40))
            t = k['f'] / 24.0
            for w in list(WN) + SMOKE:
                if 'W' in w.inputs: w.inputs['W'].default_value = t * 0.15
            for fo, lo_, f in FIRE_OBJ:   # nhấp nháy lửa tất định
                if lo_ is None: continue
                ff = 0.8 + 0.2 * math.sin(t * 7.1 + f['at'][0] * 0.01) * math.sin(t * 3.3 + f['at'][1] * 0.013); lo_.data.energy = f.get('W', 2.5e6) * (f.get('size', 30) / 30) * ff
            sc.render.filepath = os.path.join(OUT, f"{k['f']:05d}.exr")
        else: sc.render.filepath = OUT
        t1 = time.time(); bpy.ops.render.render(write_still=True); times.append(round(time.time() - t1, 2))
        print('NC-RENDER', JOB, k['f'] if k else '-', times[-1], flush=True)
    info.update(job=JOB, spp=int(opt.get('--spp', 16 if JOB == 'cycles' else 32)), res=[W, H], render_s=times, threads=TH)
    json.dump(info, open((OUT if not frames[0] else os.path.join(OUT, 'nc')) + '.json', 'w'), ensure_ascii=False)
    print('NC-BLEND', json.dumps(info, ensure_ascii=False))

elif JOB == 'nuong':
    """nướng: R trời, G nảy nắng, (B lửa) vào ảnh phẳng hộp box; mỗi lượt một ảnh float rồi gộp."""
    box = [float(x) for x in opt['--box'].split(',')]; br = float(opt.get('--bres', 2.0)); BW = int(round((box[2] - box[0]) / br)); BH = int(round((box[3] - box[1]) / br))
    spp = int(opt.get('--spp', 64)); cycles(spp, denoise=False, bounces=(3, 3, 0))
    # bỏ phần VÁY chồng mép của mỗi ô 1 km (terrain.js chunk(): mở rộng ±1 bước) — không thì mép ô bị ô kề che → đường xám lưới 1 km trong ảnh nướng
    import bmesh
    for ob in TERR:
        co = np.zeros(len(ob.data.vertices) * 3, np.float32); ob.data.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
        ex = co[:, 0].max() - co[:, 0].min()
        if ex > 1100: continue   # lưới ngoài/toàn vùng: giữ
        cx, cy = co[:, 0].mean(), co[:, 1].mean(); e0 = -3000 + math.floor((cx + 3000) / 1000) * 1000; n0 = -5500 + math.floor((cy + 5500) / 1000) * 1000
        bm = bmesh.new(); bm.from_mesh(ob.data); dl = [f for f in bm.faces if not (e0 <= f.calc_center_median().x <= e0 + 1000 and n0 <= f.calc_center_median().y <= n0 + 1000)]
        bmesh.ops.delete(bm, geom=dl, context='FACES'); bm.to_mesh(ob.data); bm.free()
    # UV phẳng cho mọi ô địa hình
    for ob in TERR:
        me = ob.data; uv = me.uv_layers.new(name='bake'); co = np.zeros(len(me.vertices) * 3, np.float32); me.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
        li = np.zeros(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', li); U = (co[li, 0] - box[0]) / (box[2] - box[0]); V = (co[li, 1] - box[1]) / (box[3] - box[1])
        uv.data.foreach_set('uv', np.stack([U, V], 1).ravel().astype(np.float32)); me.uv_layers.active = uv
    # chỉ giữ ô địa hình có phần trong hộp
    tgt = []
    for ob in TERR:
        co = np.zeros(len(ob.data.vertices) * 3, np.float32); ob.data.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
        if ((co[:, 0] > box[0]) & (co[:, 0] < box[2]) & (co[:, 1] > box[1]) & (co[:, 1] < box[3])).any(): tgt.append(ob)
    gm = MATS['dia_hinh']; nt = gm.node_tree; bi = N(nt, 'ShaderNodeTexImage'); nt.nodes.active = bi
    WATER.hide_render = True   # nước không tham gia nảy (k2v: nước vẽ riêng)
    res = {}
    def bake(name, filt):
        im = bpy.data.images.new('bk_' + name, BW, BH, float_buffer=True, alpha=False); bi.image = im
        bpy.ops.object.select_all(action='DESELECT')
        for ob in tgt: ob.select_set(True)
        bpy.context.view_layer.objects.active = tgt[0]
        t1 = time.time(); bpy.ops.object.bake(type='DIFFUSE', pass_filter=filt, margin=4, use_clear=True, target='IMAGE_TEXTURES')
        a = np.array(im.pixels[:], np.float32).reshape(BH, BW, 4)[::-1, :, :3].mean(2); res[name] = (a, round(time.time() - t1, 1)); print('NC-BAKE', name, res[name][1], 's', flush=True)
    # (1) TRỜI: vòm trên trắng đều L = 1/π (bức xạ mặt phẳng trống = 1), dưới chân trời đen; không nắng
    for n_ in list(wnt.nodes): wnt.nodes.remove(n_)
    tc = wnt.nodes.new('ShaderNodeTexCoord'); sx = wnt.nodes.new('ShaderNodeSeparateXYZ'); gt = wnt.nodes.new('ShaderNodeMath'); gt.operation = 'GREATER_THAN'; gt.inputs[1].default_value = 0.0
    mu = wnt.nodes.new('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = 1 / math.pi
    bg2 = wnt.nodes.new('ShaderNodeBackground'); wo2 = wnt.nodes.new('ShaderNodeOutputWorld'); L = wnt.links
    L.new(tc.outputs['Generated'], sx.inputs[0]); L.new(sx.outputs['Z'], gt.inputs[0]); L.new(gt.outputs[0], mu.inputs[0]); L.new(mu.outputs[0], bg2.inputs['Strength']); L.new(bg2.outputs[0], wo2.inputs[0]); bg2.inputs['Color'].default_value = (1, 1, 1, 1)
    sl.energy = 0
    for fo, lo_, f in FIRE_OBJ:
        fo.hide_render = True
        if lo_: lo_.hide_render = True
    bake('sky', {'DIRECT', 'INDIRECT'})
    # (2) NẮNG: chỉ nảy (gián tiếp) + trực tiếp làm mốc chuẩn hoá; trời đen
    bg2.inputs['Color'].default_value = (0, 0, 0, 1); sl.energy = 1.0; sl.color = (1, 1, 1)
    bake('sun_ind', {'INDIRECT'}); bake('sun_dir', {'DIRECT'})
    # (3) LỬA (nếu có): đèn điểm lửa, không nắng/trời
    if FIRE_OBJ:
        sl.energy = 0
        for fo, lo_, f in FIRE_OBJ:
            if lo_: lo_.hide_render = False
        bake('fire', {'DIRECT', 'INDIRECT'})
    sky = res['sky'][0]; kS = float(np.percentile(sky, 99.5)) or 1.0
    dirf = res['sun_dir'][0]; kD = float(np.percentile(dirf, 99.5)) or 1.0   # mặt phẳng trống: I·cos(zenith)·c
    cz = max(0.05, sd.z); G = res['sun_ind'][0] / kD * cz   # nảy ÷ bức xạ nắng pháp tuyến
    Rch = np.clip(sky / kS, 0, 1); Gch = np.clip(G * 4.0, 0, 1)
    Bch = np.zeros_like(Rch); fpk = 0.0
    if 'fire' in res: fa = res['fire'][0]; fpk = float(np.percentile(fa, 99.9)) or 1.0; Bch = np.clip(fa / fpk, 0, 1)
    # A: cao độ mặt đất (pack terrain.f32 nội suy theo ô ảnh) ÷ 600
    pk = json.load(open(os.path.join(opt['--pack'], 'meta.json'))); Hh = np.fromfile(os.path.join(opt['--pack'], 'terrain.f32'), np.float32).reshape(pk['terrain_shape'])
    e0, n0, e1, n1 = pk['ext']; stp = pk['step_terrain']; ee = box[0] + (np.arange(BW) + 0.5) * br; nn = box[3] - (np.arange(BH) + 0.5) * br
    fc = np.clip((ee - e0) / stp, 0, Hh.shape[1] - 1.001); fr = np.clip((n1 - nn) / stp, 0, Hh.shape[0] - 1.001); c0 = fc.astype(int); r0 = fr.astype(int); ax = fc - c0; ay = fr - r0
    hh = (Hh[r0][:, c0] * (1 - ax) + Hh[r0][:, c0 + 1] * ax) * (1 - ay)[:, None] + (Hh[r0 + 1][:, c0] * (1 - ax) + Hh[r0 + 1][:, c0 + 1] * ax) * ay[:, None]
    Ach = np.clip(hh / 600.0, 0, 1)
    import imageio.v3 as iio
    os.makedirs(OUT, exist_ok=True); rgba = (np.dstack([Rch, Gch, Bch, Ach]) * 255 + 0.5).astype(np.uint8); iio.imwrite(os.path.join(OUT, 'bake.png'), rgba)
    for nm, (arr, s_) in res.items(): np.save(os.path.join(OUT, f'raw_{nm}.npy'), arr.astype(np.float16))
    meta = dict(box=box, res_m=br, px=[BW, BH], spp=spp, sun_dir=[float(x) for x in (S.inverted() @ sd.to_4d()).to_3d()], sun_el=round(sun_el, 2), g_scale=0.25, fire_peak=fpk, norm=dict(sky_p995=kS, dir_p995=kD),
                bake_s={k: v[1] for k, v in res.items()}, tong_s=round(time.time() - T0, 1), nap_s=round(T_LOAD, 1), o_dia_hinh=len(tgt), threads=TH, blender=bpy.app.version_string,
                kenh='R trời/mặt phẳng trống · G nảy nắng ×4 · B lửa/đỉnh · A cao/600 m', stat=stat)
    json.dump(meta, open(os.path.join(OUT, 'meta.json'), 'w'), ensure_ascii=False); print('NC-BAKE-XONG', json.dumps({k: meta[k] for k in ('bake_s', 'tong_s', 'px')}))
