"""V6 · tờ sprite NGƯỜI khung neo — người TỰ DỰNG (nguoi6.py: SDF → marching cubes; quần áo lưới riêng có độ dày + nếp theo khớp; mũ một lưới liền).
Kế thừa bố cục tờ của mh_people4.py (PT4): hàng = 8 hướng, cột = tư thế; máy trực giao cùng hướng máy neo, cúi 8°.
Mới so với PT4 (P2 §8.1 a–e):
 (a) quần áo = lưới riêng có bề dày, mép gấu/vạt/ống lộ dày vải, nếp gợn quanh khuỷu/gối/eo/nách/háng; áo 1782 có vạt sau xẻ + bẻ lót, quần chẽn + ghệt;
     1943 battledress/khaki drill/RN/RAF;
 (b) tỉ lệ đầu/vai theo nhân trắc (đầu ≈ 1/7,5 chiều cao); TAY BUÔNG sát thân, đi bộ tay đung đưa nhỏ cạnh thân (≤ 14°), khuỷu chùng;
 (c) mũ đúng mẫu: tricorn = MỘT vành tròn bẻ lên 3 phía (lưới liền, Solidify), Brodie, calô, mũ lính thuỷ, mũ vải lưỡi trai, mũ tròn 1782, mũ vải nữ;
 (d) ÁNH SÁNG = trời Nishita + mặt trời Y HỆT lượt nền (build_scene.set_pass), tách 2 nhóm sáng (light group 'nang' / 'troi') → ghép theo bóng nhà
     của chính nền (live6.py); mặt đất ẩn với máy nhưng hắt sáng (albedo theo mốc);
 (e) 3 dáng thân + đi với ĐẦU QUAY (cột 'wl0..7': đầu quay 32° sang trái; phải = lật gương hướng đối xứng), dồn trọng tâm, vai lắc.
  /opt/bpy/bin/python design/pt/song/mh_people6.py -- --epoch 1782|1943 --head <độ> --roles a,b --out DIR [--pxm 130] [--spp 8] [--test] [--threads 2]"""
import bpy, bmesh, math, sys, os, json, argparse, random, time
from mathutils import Vector, Matrix, Quaternion
sys.path.append('/var/tmp/v6kn/pylib313')
import numpy as np
from skimage.measure import marching_cubes
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import nguoi6 as N6

ap = argparse.ArgumentParser(); ap.add_argument('--epoch', type=int, required=True); ap.add_argument('--head', type=float, required=True)
ap.add_argument('--roles', required=True); ap.add_argument('--passes', default='d1,d2,d4'); ap.add_argument('--out', required=True)
ap.add_argument('--pxm', type=int, default=130); ap.add_argument('--spp', type=int, default=8); ap.add_argument('--threads', type=int, default=2)
ap.add_argument('--test', action='store_true'); ap.add_argument('--builds', default='')    # vd 'linh:3,linh2:2'
ap.add_argument('--blend', default='')                                                      # lưu .blend người mẫu (bản tốt nhất dùng lại)
A = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]); os.makedirs(A.out, exist_ok=True)
EP = A.epoch; T0 = time.time()
PASSES = json.load(open(os.path.join(HERE, '..', 'scene', 'passes.json')))
NB = {k: int(v) for k, v in (x.split(':') for x in A.builds.split(',') if x)}

# ---------------------------------------------------------------- lưới từ SDF
def grid(lo, hi, h):
    xs = [np.arange(lo[i], hi[i] + h, h, dtype=np.float32) for i in range(3)]
    X, Y, Z = np.meshgrid(*xs, indexing='ij'); return np.stack([X, Y, Z], -1), xs
def mc(vol, xs, h):
    if not (vol < 0).any(): return None, None
    v, f, _, _ = marching_cubes(vol, 0.0, spacing=(h, h, h)); v += np.array([xs[0][0], xs[1][0], xs[2][0]], np.float32)
    return v.astype(np.float32), f
def to_mesh(name, v, f, target=None):
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(p) for p in v], [], [tuple(int(i) for i in t[::-1]) for t in f]); me.update()
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    if target and len(f) > target:
        md = o.modifiers.new('dec', 'DECIMATE'); md.ratio = target / len(f)
        bpy.context.view_layer.objects.active = o; bpy.ops.object.modifier_apply(modifier='dec')
    for p in o.data.polygons: p.use_smooth = True
    return o

# ---------------------------------------------------------------- vật liệu (màu theo thuộc tính đỉnh 'col')
MATS = {}
def mat(kind):
    if kind in MATS: return MATS[kind]
    m = bpy.data.materials.new('n6_' + kind); m.use_nodes = True; nt = m.node_tree; N = nt.nodes; L = nt.links; b = N['Principled BSDF']
    at = N.new('ShaderNodeAttribute'); at.attribute_name = 'col'; at.attribute_type = 'GEOMETRY'
    tc = N.new('ShaderNodeTexCoord'); nz = N.new('ShaderNodeTexNoise'); L.new(tc.outputs['Object'], nz.inputs['Vector'])
    sc_ = {'cloth': 7.0, 'wool': 7.0, 'leather': 25.0, 'skin': 90.0, 'hair': 70.0, 'metal': 30.0, 'wood': 12.0, 'straw': 40.0}[kind]
    nz.inputs['Scale'].default_value = sc_; nz.inputs['Detail'].default_value = 6.0
    mr = N.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value = {'skin': 0.93, 'hair': 0.75}.get(kind, 0.82); mr.inputs['To Max'].default_value = 1.08
    L.new(nz.outputs['Fac'], mr.inputs['Value'])
    mx = N.new('ShaderNodeVectorMath'); mx.operation = 'SCALE'; L.new(at.outputs['Color'], mx.inputs[0]); L.new(mr.outputs[0], mx.inputs['Scale']); L.new(mx.outputs[0], b.inputs['Base Color'])
    bp = N.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = {'cloth': 0.3, 'wool': 0.35, 'leather': 0.15, 'skin': 0.06, 'hair': 0.5, 'metal': 0.05, 'wood': 0.25, 'straw': 0.6}[kind]
    if kind in ('cloth', 'wool'):   # sợi dệt: nhiễu dài theo trục Z (sợi dọc) + nhiễu mịn
        n2 = N.new('ShaderNodeTexNoise'); n2.inputs['Scale'].default_value = 160.0; n2.inputs['Detail'].default_value = 2.0; L.new(tc.outputs['Object'], n2.inputs['Vector'])
        ad = N.new('ShaderNodeMath'); ad.operation = 'ADD'; L.new(nz.outputs['Fac'], ad.inputs[0]); L.new(n2.outputs['Fac'], ad.inputs[1]); L.new(ad.outputs[0], bp.inputs['Height'])
    else: L.new(nz.outputs['Fac'], bp.inputs['Height'])
    L.new(bp.outputs['Normal'], b.inputs['Normal'])
    b.inputs['Roughness'].default_value = {'cloth': 0.86, 'wool': 0.9, 'leather': 0.42, 'skin': 0.52, 'hair': 0.55, 'metal': 0.32, 'wood': 0.7, 'straw': 0.8}[kind]
    if kind == 'metal': b.inputs['Metallic'].default_value = 0.9
    try:
        if kind in ('wool', 'cloth'): b.inputs['Sheen Weight'].default_value = 0.35 if kind == 'wool' else 0.2; b.inputs['Sheen Roughness'].default_value = 0.6
        if kind == 'skin': b.inputs['Subsurface Weight'].default_value = 0.0; b.inputs['Coat Weight'].default_value = 0.05
        if kind == 'hair': b.inputs['Sheen Weight'].default_value = 0.4
    except Exception: pass
    MATS[kind] = m; return m

def paint(o, cols):
    """cols: mảng (n_đỉnh, 3) → thuộc tính 'col' theo đỉnh."""
    me = o.data; at = me.attributes.new('col', 'FLOAT_COLOR', 'POINT')
    flat = np.concatenate([np.asarray(cols, np.float32), np.ones((len(cols), 1), np.float32)], 1).ravel()
    at.data.foreach_set('color', flat)

def verts_of(o):
    a = np.empty(len(o.data.vertices) * 3, np.float32); o.data.vertices.foreach_get('co', a); return a.reshape(-1, 3)

# ---------------------------------------------------------------- dựng MỘT người mẫu
def build_person(role, R, bi, name):
    t0 = time.time(); bd = N6.builds(R['sex'])[bi]; rr = random.Random(hash((role, bi, EP)) & 0xffffff)
    body = N6.Body(R['sex'], **bd, seed=bi); z = body.z
    skin = N6.SKIN[(list(N6.roles(EP)).index(role) * 3 + bi) % len(N6.SKIN)]; hair = N6.HAIR[(list(N6.roles(EP)).index(role) + 2 * bi) % len(N6.HAIR)]
    if EP == 1782 and R.get('belts') is not None and 'coat' in R and bi == 0: hair = (0.52, 0.5, 0.46)    # tóc rắc bột (lính thế kỷ 18) — một dáng
    objs = []   # (obj, boneset, rootmix)
    # thân (không đầu)
    h = 0.0055; lo = (-0.3, -0.24, -0.02); hi = (0.3, 0.2, z['neck'] + 0.12)
    G, xs = grid(lo, hi, h); Dc = body.core(G)
    v, f = mc(Dc, xs, h); ob = to_mesh(name + '_than', v, f, 14000); ob.data.materials.append(mat('skin')); paint(ob, np.tile(skin, (len(ob.data.vertices), 1))); objs.append((ob, 'core', 0.0))
    band = np.abs(Dc) < 0.075
    # đầu (lưới mịn) + tóc + mắt
    hh = 0.0026; c = z['headc']; GH, xh = grid((-0.11, -0.15, c - 0.2), (0.11, 0.13, c + 0.13), hh); DH = body.head(GH)
    v, f = mc(DH, xh, hh); oh = to_mesh(name + '_dau', v, f, 9000); oh.data.materials.append(mat('skin'))
    P = verts_of(oh); col = np.tile(np.array(skin, np.float32), (len(P), 1))
    for sg in (1, -1):   # lông mày (dải cong trên hốc mắt, mặt trước), môi hồng hơn
        e = np.array([sg * 0.033, -0.09, c + 0.024]) * [body.head_k, body.head_k, 1] + [0, 0, 0]
        m_ = (np.abs(P[:, 0] - sg * 0.034 * body.head_k) < 0.022) & (np.abs(P[:, 2] - (c + 0.021 + 0.004 * (1 - ((P[:, 0] - sg * 0.034) / 0.022) ** 2))) < 0.0055) & (P[:, 1] < -0.075)
        col[m_] = np.array(hair) * 0.9 + 0.01
    lip = (np.abs(P[:, 0]) < 0.02) & (np.abs(P[:, 2] - (c - 0.064)) < 0.007) & (P[:, 1] < -0.09); col[lip] = np.array(skin) * [0.92, 0.62, 0.6]
    stub = (P[:, 2] < c - 0.05) & (P[:, 1] < -0.02) & (np.abs(P[:, 0]) < 0.06) & ~lip                     # bóng râu cạo (nam)
    if R['sex'] == 'm': col[stub] *= [0.9, 0.88, 0.88]
    paint(oh, col); objs.append((oh, 'head', 0.0))
    eyes, er = body.eyes(); er *= 0.85
    for k_, e in enumerate(eyes):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=er, location=tuple(e)); oe = bpy.context.object; oe.name = f'{name}_mat{k_}'
        oe.data.materials.append(mat('skin')); Pe = verts_of(oe) - e; ce = np.where((Pe[:, 1] < -er * 0.35)[:, None], np.array([0.025, 0.018, 0.013]), np.array([0.32, 0.29, 0.26]))
        paint(oe, ce); objs.append((oe, 'head', 0.0))
    if R.get('hair'):
        hairreg = lambda Q: (Q[..., 2] - (c - 0.018 - 0.75 * Q[..., 1])) if R['hair'] != 'bun' else (Q[..., 2] - (c - 0.03 - 0.6 * Q[..., 1]))
        tk = 0.011 if R['hair'] != 'short' else 0.006
        Dh = np.maximum(np.maximum(DH - tk - 0.003 * N6.vnoise(GH, 0.02, bi), -(DH + 0.002)), -hairreg(GH))
        if R['hair'] == 'queue':   # tóc buộc đuôi sau gáy (thế kỷ 18) + nơ đen
            Dh = np.minimum(Dh, N6.sd_cone(GH, N6.V(0, 0.085, c - 0.03), N6.V(0, 0.105, c - 0.14), 0.016, 0.01))
        if R['hair'] == 'bun': Dh = np.minimum(Dh, N6.sd_ell(GH, N6.V(0, 0.1, c - 0.01), (0.04, 0.035, 0.035)))
        v, f = mc(Dh, xh, hh)
        if v is not None:
            ohr = to_mesh(name + '_toc', v, f, 5000); ohr.data.materials.append(mat('hair')); paint(ohr, np.tile(hair, (len(ohr.data.vertices), 1))); objs.append((ohr, 'head', 0.0))
    # tay (lưới riêng, tư thế dựng giạng 30°)
    DA = {}
    for sd in 'LR':
        S, Wt = body.J['sh' + sd], body.J['hand_t' + sd]; lo_a = np.minimum(S, Wt) - 0.09; hi_a = np.maximum(S, Wt) + 0.09
        GA, xa = grid(tuple(lo_a), tuple(hi_a), 0.0045); D = body.arm(GA, sd); DA[sd] = (GA, xa, D)
        v, f = mc(D, xa, 0.0045); oa = to_mesh(f'{name}_tay{sd}', v, f, 5000); oa.data.materials.append(mat('skin')); paint(oa, np.tile(skin, (len(oa.data.vertices), 1))); objs.append((oa, 'arm' + sd, 0.0))
    # quần áo: vỏ có bề dày
    Dl = {}
    for gi, g in enumerate(N6.garments(body, R, bi)):
        base = g['base']; seed = gi * 1.7 + bi
        if base in ('skirt', 'dress', 'apron'):
            GS, xg = G, xs; D, lin = N6.skirt_shell(G, body, base, g['t_out'])
        else:
            if base.startswith('arm'): GS, xg, Db = DA[base[3:]]
            elif base in ('legs_loose', 'bells'):
                GS, xg = G, xs
                if base not in Dl: Dl[base] = N6.loose_legs(G, body, base)
                Db = Dl[base]
            else: GS, xg, Db = G, xs, Dc
            D = np.full(Db.shape, 1.0, np.float32); m_ = np.abs(Db) < 0.075; Pm = GS[m_]
            fo = N6.folds(Pm, body, g['fold'], g['amp'], seed) if (g['fold'] or g['amp']) else 0.0
            t_in = min(g['t_in'], g['t_out'] - 0.013)   # vỏ >= 13 mm (> 2 ô lưới) — tránh thủng; phần lấn vào thân bị che
            sh = np.maximum(Db[m_] - g['t_out'] - fo, -(Db[m_] - t_in))
            if g.get('clip') is not None: sh = np.maximum(sh, g['clip'](Pm))
            if g['bones'] == 'legs':   # tách hai ống quần dưới đáy quần (khe 2 cm) — không dính thành váy khi bước
                sh = np.maximum(sh, np.where(Pm[:, 2] < z['hip'] - 0.075, 0.01 - np.abs(Pm[:, 0]), -1.0))
            D[m_] = sh; lin = None
        v, f = mc(D, xg, xg[0][1] - xg[0][0])
        if v is None: print('  (bỏ, rỗng)', g['name']); continue
        og = to_mesh(f"{name}_{g['name']}", v, f, 6000 if g['name'] in ('ao', 'quan', 'vat', 'vay', 'quan_chen') else 2500)
        kind = g['kind'] if g['kind'] != 'cloth' else ('wool' if EP == 1782 or 'blouse' in R else 'cloth')
        og.data.materials.append(mat(kind)); Pg = verts_of(og); colg = np.tile(np.array(g['col'], np.float32), (len(Pg), 1))
        for fn, cc in g['regions']:
            if fn is not None: colg[fn(Pg)] = cc
        if lin is not None and g.get('lining') is not None: colg[lin(Pg)] = g['lining']
        paint(og, colg); objs.append((og, g['bones'] if g['bones'] != 'torso' else 'torso', g['rootmix']))
    print(f'  người {name}: {sum(len(o.data.polygons) for o, _, _ in objs)} mặt, {round(time.time() - t0, 1)} s', flush=True)
    return body, objs, skin, hair

# ---------------------------------------------------------------- khung xương + trọng số + mũ
def rig_person(body, objs, R, name, bi, hatless):
    arm = bpy.data.armatures.new(name + '_rig'); ao = bpy.data.objects.new(name + '_rig', arm); bpy.context.scene.collection.objects.link(ao)
    bpy.context.view_layer.objects.active = ao; bpy.ops.object.mode_set(mode='EDIT'); eb = {}
    for bn, h_, t_, par in body.bones():
        e = arm.edit_bones.new(bn); e.head = Vector(h_.tolist()); e.tail = Vector(t_.tolist()); eb[bn] = e
        if par: e.parent = eb[par]
    bpy.ops.object.mode_set(mode='OBJECT')
    for o, bs, rmx in objs:
        names = N6.BONESET[bs]; P = verts_of(o); W = N6.skin_weights(P, body, names, rootmix=rmx)
        for j, bn in enumerate(names):
            idx = np.nonzero(W[:, j] > 0.004)[0]
            if not len(idx): continue
            vg = o.vertex_groups.new(name=bn)
            for i in idx: vg.add([int(i)], float(W[i, j]), 'REPLACE')
        o.parent = ao; md = o.modifiers.new('arm', 'ARMATURE'); md.object = ao
    parts = []
    z = body.z; c = z['headc']; top = z['top']
    def hat_obj(v, f, col, thick, loc, rot=(0, 0, 0), kind='wool', face_cols=None):
        me = bpy.data.meshes.new(name + '_mu'); me.from_pydata([tuple(p) for p in v], [], f); me.update(); o = bpy.data.objects.new(name + '_mu', me)
        bpy.context.scene.collection.objects.link(o); o.data.materials.append(mat(kind))
        if face_cols is not None:   # màu theo mặt → theo đỉnh (viền ren)
            vc = np.tile(np.array(col, np.float32), (len(v), 1))
            for fi, fc in enumerate(face_cols):
                if fc is not None:
                    for vi in f[fi]: vc[vi] = fc
            paint(o, vc)
        else: paint(o, np.tile(col, (len(v), 1)))
        for p in o.data.polygons: p.use_smooth = True
        if thick: s_ = o.modifiers.new('sol', 'SOLIDIFY'); s_.thickness = thick; s_.offset = 0.0
        o.location = loc; o.rotation_euler = rot; bpy.context.view_layer.update(); mw = o.matrix_world.copy()
        o.parent = ao; o.parent_type = 'BONE'; o.parent_bone = 'head'; bpy.context.view_layer.update(); o.matrix_world = mw; parts.append(o); return o
    hat = None if hatless else R.get('hat')
    if hat == 'tricorn':
        v, f, lace = N6.hat_tricorn(lace=R.get('lace') is not None)
        fc = [R['lace'] if l else None for l in lace] if R.get('lace') else None
        hat_obj(v, f, R['hatcol'], 0.004, (0, 0.006, top - 0.052), (math.radians(-7), 0, 0), face_cols=fc)
        bpy.ops.mesh.primitive_cylinder_add(vertices=14, radius=0.022, depth=0.006, location=(0.105, -0.055, top - 0.005), rotation=(0, math.radians(70), math.radians(-30)))
        ck = bpy.context.object; ck.data.materials.append(mat('cloth')); paint(ck, np.tile((0.02, 0.02, 0.02), (len(ck.data.vertices), 1)))   # nơ (cockade) đen bên trái
        mw = ck.matrix_world.copy(); ck.parent = ao; ck.parent_type = 'BONE'; ck.parent_bone = 'head'; bpy.context.view_layer.update(); ck.matrix_world = mw; parts.append(ck)
    elif hat == 'round': v, f = N6.hat_revolve(N6.ROUND1782); hat_obj(v, f, R['hatcol'], 0.004, (0, 0.004, top - 0.045), (math.radians(-4), 0, 0))
    elif hat == 'brodie': v, f = N6.hat_revolve(N6.BRODIE, sy=1.1); hat_obj(v, f, R['hatcol'], 0.003, (0, 0.0, top - 0.055), (math.radians(-3), 0, 0), kind='metal' if False else 'leather')
    elif hat == 'sailor':
        v, f = N6.hat_revolve(N6.SAILOR); o = hat_obj(v, f, R['hatcol'], 0.003, (0, 0.006, top - 0.03), (math.radians(6), 0, 0), kind='cloth')
        vc = np.tile(np.array(R['hatcol'], np.float32), (len(v), 1)); vc[v[:, 2] < 0.03] = R['band']; paint(o, vc)
    elif hat == 'sidecap': v, f = N6.hat_sidecap(); hat_obj(v, f, R['hatcol'], 0.003, (-0.03, 0.0, top - 0.035), (0, math.radians(-14), 0), kind='wool')
    elif hat == 'flatcap':
        v, f = N6.hat_revolve(N6.FLATCAP, sy=1.12); hat_obj(v, f, R['hatcol'], 0.003, (0, -0.005, top - 0.035), (math.radians(-6), 0, 0), kind='wool')
        v, f = N6.visor(); hat_obj(v, f, R['hatcol'], 0.004, (0, -0.005, top - 0.045), (math.radians(-6), 0, 0), kind='wool')
    elif hat == 'mobcap': v, f = N6.hat_revolve(N6.MOBCAP, sy=1.12); hat_obj(v, f, R['hatcol'], 0.002, (0, 0.012, top - 0.06), (math.radians(-10), 0, 0), kind='cloth')
    return ao, parts

# ---------------------------------------------------------------- tư thế (xoay quanh đầu xương theo trục thế giới; người nhìn −Y, +X = trái)
def rot(ao, bn, axis, deg):
    pb = ao.pose.bones[bn]; hd = pb.head.copy()
    ax = {'X': Vector((1, 0, 0)), 'Y': Vector((0, 1, 0)), 'Z': Vector((0, 0, 1))}[axis] if isinstance(axis, str) else Vector(axis)
    pb.matrix = Matrix.Translation(hd) @ Matrix.Rotation(math.radians(deg), 4, ax) @ Matrix.Translation(-hd) @ pb.matrix; bpy.context.view_layer.update()
def aim(ao, bn, target, keep=1.0):
    """quay xương để hướng đầu→đuôi trùng 'target' (thế giới)."""
    pb = ao.pose.bones[bn]; cur = (pb.tail - pb.head).normalized(); q = cur.rotation_difference(Vector(target).normalized())
    if keep < 1.0: q = Quaternion().slerp(q, keep)
    hd = pb.head.copy(); pb.matrix = Matrix.Translation(hd) @ q.to_matrix().to_4x4() @ Matrix.Translation(-hd) @ pb.matrix; bpy.context.view_layer.update()
def reset(ao):
    for pb in ao.pose.bones: pb.matrix_basis = Matrix()
    bpy.context.view_layer.update()
def arms_down(ao, out=6.0, fwd=3.0):
    """tay buông: cánh tay giạng ~6° (không chạm hông), khuỷu chùng 10–14°, bàn tay hơi xoay vào đùi."""
    for sd, sg in (('L', 1), ('R', -1)):
        a = math.radians(out); aim(ao, 'uarm' + sd, (sg * math.sin(a), -math.sin(math.radians(fwd)), -math.cos(a)))
        rot(ao, 'farm' + sd, 'X', -12)
def head_turn(ao, deg, tilt=0.0):
    for bn, k in (('neck', 0.4), ('head', 0.6)): rot(ao, bn, 'Z', deg * k)
    if tilt: rot(ao, 'head', 'X', tilt)
def legs_walk(ao, ph, amp):
    """chu kỳ bước: đùi ±amp; gối gập lớn ở pha đưa chân (≈ 55°), nhỏ ở pha tiếp đất; cổ chân bù để bàn chân gần song song đất."""
    for sd, off in (('L', 0.0), ('R', math.pi)):
        p = ph + off; hip = amp * math.sin(p); knee = 6 + 50 * max(0.0, math.sin(p + 1.1)) ** 1.6
        rot(ao, 'thigh' + sd, 'X', -hip); rot(ao, 'shin' + sd, 'X', knee); rot(ao, 'foot' + sd, 'X', -(knee - hip) * 0.55 - 2)
def walk_arms(ao, ph, amp_deg=13.0, hold=()):
    for sd, off in (('L', math.pi), ('R', 0.0)):    # tay ngược pha chân cùng bên
        if sd in hold: continue
        p = ph + off; a = amp_deg * math.sin(p)
        rot(ao, 'uarm' + sd, 'X', -a); rot(ao, 'farm' + sd, 'X', -6 - 9 * max(0.0, math.sin(p)))
def pose(ao, pn, R, rr):
    reset(ao); arms_down(ao); sex = R['sex']; amp = 21 if sex == 'm' else 17
    gun = R.get('gun')
    def gun_hold():
        if gun == 'musket':   # vác súng vai trái: tay trái gập đỡ báng ngang hông
            aim(ao, 'uarmL', (0.12, 0.05, -1)); aim(ao, 'farmL', (0.15, -1.0, 0.35)); return ('L',)
        if gun == 'rifle':    # súng đeo dây vai phải: tay phải nắm dây trước ngực
            aim(ao, 'uarmR', (-0.1, -0.12, -1)); aim(ao, 'farmR', (0.3, -0.6, 0.75)); return ('R',)
        return ()
    if pn == 'st':
        rot(ao, 'shinL', 'X', 8); rot(ao, 'thighL', 'X', -4); rot(ao, 'root', 'Y', 2.5); rot(ao, 'spine', 'Y', -1.5); rot(ao, 'chest', 'Y', -1.0)
        head_turn(ao, rr.uniform(-14, 14), rr.uniform(-4, 3)); gun_hold()
    elif pn == 'talk':
        aim(ao, 'uarmR', (-0.18, -0.25, -1)); aim(ao, 'farmR', (-0.25, -1.0, 0.45)); rot(ao, 'handR', 'X', -20)
        rot(ao, 'shinR', 'X', 6); rot(ao, 'chest', 'Z', 5); head_turn(ao, 18, -4)
    elif pn == 'look':
        rot(ao, 'chest', 'Z', -10); head_turn(ao, -44, 2); rot(ao, 'shinL', 'X', 5); gun_hold()
    elif pn == 'back':   # đứng nghỉ, chắp tay sau lưng
        for sd, sg in (('L', 1), ('R', -1)):
            aim(ao, 'uarm' + sd, (sg * 0.15, 0.45, -1)); aim(ao, 'farm' + sd, (-sg * 0.9, 0.55, -0.15))
        head_turn(ao, rr.uniform(-15, 15))
    elif pn.startswith('work_'):
        w = pn[5:]
        if w == 'order':   # gác: đứng thẳng, súng dựng đất bên phải, tay phải giữ nòng
            aim(ao, 'uarmR', (-0.16, -0.06, -1)); aim(ao, 'farmR', (-0.05, -0.55, -0.8)); head_turn(ao, rr.uniform(-6, 6))
        elif w == 'tool':  # chữa tường: tay phải cầm bay đưa ngang vai, tay trái tì tường
            aim(ao, 'uarmR', (-0.15, -0.85, -0.25)); aim(ao, 'farmR', (0.0, -0.75, 0.6)); aim(ao, 'uarmL', (0.2, -0.8, -0.2)); aim(ao, 'farmL', (0.0, -0.9, 0.35))
            rot(ao, 'spine', 'X', -5); head_turn(ao, 0, -7)
        elif w == 'box':
            for sd, sg in (('L', 1), ('R', -1)): aim(ao, 'uarm' + sd, (sg * 0.08, -0.38, -1)); aim(ao, 'farm' + sd, (-sg * 0.25, -1, 0.15))
        elif w == 'sack':
            aim(ao, 'uarmR', (-0.25, -0.15, 1)); aim(ao, 'farmR', (0.5, 0.0, -0.4)); rot(ao, 'spine', 'Y', 4)
        elif w == 'basket':
            aim(ao, 'uarmL', (0.18, -0.1, -1)); aim(ao, 'farmL', (0.2, -1.0, 0.1))
        elif w == 'back':  # 1943: đứng nghỉ chắp tay sau lưng
            for sd, sg in (('L', 1), ('R', -1)):
                aim(ao, 'uarm' + sd, (sg * 0.15, 0.45, -1)); aim(ao, 'farm' + sd, (-sg * 0.9, 0.55, -0.15))
    elif pn[0] in 'wc' and pn[-1].isdigit():
        k_ = int(pn[-1]); ph = 2 * math.pi * k_ / 8; legs_walk(ao, ph, amp)
        rot(ao, 'root', 'Z', 4 * math.sin(ph)); rot(ao, 'chest', 'Z', -5 * math.sin(ph)); rot(ao, 'root', 'Y', 1.5 * math.cos(ph))
        if pn.startswith('wl'): head_turn(ao, 32, rr.uniform(-3, 2))
        if pn[0] == 'w': walk_arms(ao, ph, 13.0, hold=gun_hold())
        else:
            kind = pn[1:-1]; pose_hold(ao, kind)
            if kind in ('basket', 'sack'): walk_arms(ao, ph, 10.0, hold=('L',) if kind == 'basket' else ('R',))
def pose_hold(ao, kind):
    if kind == 'box':
        for sd, sg in (('L', 1), ('R', -1)): aim(ao, 'uarm' + sd, (sg * 0.08, -0.38, -1)); aim(ao, 'farm' + sd, (-sg * 0.25, -1, 0.15))
    elif kind == 'sack': aim(ao, 'uarmR', (-0.25, -0.15, 1)); aim(ao, 'farmR', (0.5, 0.0, -0.4))
    elif kind == 'basket': aim(ao, 'uarmL', (0.18, -0.1, -1)); aim(ao, 'farmL', (0.2, -1.0, 0.1))
    elif kind == 'barrow':
        for sd in 'LR': rot(ao, 'farm' + sd, 'X', -14)

def prim(kind, loc, scale, col, rot_=(0, 0, 0), mk='wood'):
    if kind == 'cyl': bpy.ops.mesh.primitive_cylinder_add(vertices=14, radius=1, depth=2, location=loc, rotation=rot_)
    elif kind == 'sph': bpy.ops.mesh.primitive_uv_sphere_add(segments=14, ring_count=8, radius=1, location=loc, rotation=rot_)
    else: bpy.ops.mesh.primitive_cube_add(size=2, location=loc, rotation=rot_)
    p = bpy.context.object; p.scale = scale; p.data.materials.append(mat(mk)); paint(p, np.tile(col, (len(p.data.vertices), 1)))
    for pp in p.data.polygons: pp.use_smooth = kind != 'cube'
    return p

def items(ao, R, pn):
    """vật cầm/đeo dựng theo toạ độ xương SAU khi đặt tư thế; gắn xương (đi theo nhịp bước)."""
    out = []; Pb = lambda b: ao.pose.bones[b].head.copy(); Tb = lambda b: ao.pose.bones[b].tail.copy()
    def attach(p, bone):
        bpy.context.view_layer.update(); mw = p.matrix_world.copy(); p.parent = ao; p.parent_type = 'BONE'; p.parent_bone = bone
        bpy.context.view_layer.update(); p.matrix_world = mw; out.append(p); return p
    def stick(a, b, r, col, bone, mk='wood'):
        a, b = Vector(a), Vector(b); d = b - a; L_ = d.length; q = Vector((0, 0, 1)).rotation_difference(d.normalized())
        p = prim('cyl', (a + b) / 2, (r, r, L_ / 2), col, mk=mk); p.rotation_mode = 'QUATERNION'; p.rotation_quaternion = q; return attach(p, bone)
    wood = (0.2, 0.12, 0.06); iron = (0.05, 0.05, 0.055)
    hold = pn[5:] if pn.startswith('work_') else (pn[1:-1] if pn[0] == 'c' and pn[-1].isdigit() else None)
    gun = R.get('gun')
    if gun == 'musket' and pn not in ('work_order', 'talk', 'back') and not hold:   # súng hoả mai (Brown Bess ≈ 1,58 m) tì vai trái, báng trong tay trái
        w = Pb('handL'); sh = Pb('uarmL'); top = sh + Vector((0.02, 0.17, 0.62)); bot = w + Vector((0.0, -0.02, -0.02))
        stick(bot, top, 0.016, wood, 'farmL'); stick(bot + (top - bot) * 0.3, top + (top - bot).normalized() * 0.08, 0.008, iron, 'farmL', 'metal')
    if gun == 'rifle' and pn not in ('work_order', 'back'):   # SMLE đeo dây vai phải, nòng chĩa lên sau vai
        sh = Pb('uarmR'); bot = sh + Vector((0.02, 0.12, -0.75)); top = sh + Vector((-0.02, 0.11, 0.3))
        stick(bot, top, 0.017, (0.24, 0.15, 0.08), 'chest'); stick(bot + (top - bot) * 0.6, top + (top - bot).normalized() * 0.04, 0.008, iron, 'chest', 'metal')
    if pn == 'work_order':
        w = Pb('handR'); L_ = 1.58 if gun == 'musket' else 1.13
        stick((w.x - 0.03, w.y - 0.03, 0.0), (w.x - 0.03, w.y - 0.03, L_), 0.017, wood, 'root')
    if hold == 'tool':
        w = Tb('handR'); stick(w, w + Vector((0, -0.16, 0.05)), 0.012, wood, 'handR'); p = prim('cube', w + Vector((0, -0.2, 0.06)), (0.05, 0.02, 0.035), (0.32, 0.32, 0.33), mk='metal'); attach(p, 'handR')
    elif hold == 'box':
        c = (Tb('handL') + Tb('handR')) / 2 + Vector((0, -0.02, 0.07))
        if EP == 1782: p = prim('cyl', c, (0.16, 0.16, 0.2), (0.32, 0.22, 0.13), (0, math.pi / 2, 0), 'wood')
        else: p = prim('cube', c, (0.24, 0.16, 0.13), (0.36, 0.33, 0.22), mk='wood')
        attach(p, 'spine')
    elif hold == 'sack':
        sh = Pb('uarmR'); p = prim('sph', sh + Vector((-0.03, 0.04, 0.12)), (0.16, 0.27, 0.12), (0.5, 0.44, 0.32) if EP == 1782 else (0.3, 0.33, 0.25), (0.3, 0, 0.25), 'cloth'); attach(p, 'chest')
    elif hold == 'basket':
        w = Tb('handL'); p = prim('cyl', w + Vector((0.05, -0.02, 0.06)), (0.12, 0.12, 0.085), (0.24, 0.16, 0.08), mk='straw'); attach(p, 'farmL')
    return out

# ---------------------------------------------------------------- bản sao nhẹ cho từng ô
def clone(ao, parts, objs, name):
    a2 = ao.copy(); a2.name = name + '_rig'; bpy.context.scene.collection.objects.link(a2); a2.hide_render = False
    for o, _, _ in objs:
        o2 = o.copy(); bpy.context.scene.collection.objects.link(o2); o2.parent = a2; o2.modifiers['arm'].object = a2; o2.hide_render = False
    for p in parts:
        p2 = p.copy(); bpy.context.scene.collection.objects.link(p2); p2.parent = a2; p2.parent_type = 'BONE'; p2.parent_bone = p.parent_bone
        p2.matrix_parent_inverse = p.matrix_parent_inverse.copy(); p2.hide_render = False
    return a2

# ---------------------------------------------------------------- ánh sáng Y HỆT build_scene.set_pass (lượt ngày)
LAT = math.radians(36.14); DECL = math.radians(4.0)
def sun_at(hour):
    Hh = math.radians((hour - 12) * 15)
    alt = math.asin(math.sin(LAT) * math.sin(DECL) + math.cos(LAT) * math.cos(DECL) * math.cos(Hh))
    az = math.atan2(math.sin(Hh), math.cos(Hh) * math.sin(LAT) - math.tan(DECL) * math.cos(LAT)) + math.pi
    return math.degrees(alt), math.degrees(az) % 360
def setup_light(sc):
    world = bpy.data.worlds.new('w'); sc.world = world; world.use_nodes = True; wn = world.node_tree.nodes; wl = world.node_tree.links
    bg = wn['Background']; sky = wn.new('ShaderNodeTexSky')
    try: sky.sky_type = 'NISHITA'
    except Exception: pass
    wl.new(sky.outputs[0], bg.inputs[0])
    sun = bpy.data.objects.new('sun', bpy.data.lights.new('sun', 'SUN')); sc.collection.objects.link(sun)
    vl = sc.view_layers[0]
    for g in ('nang', 'troi'):
        if g not in vl.lightgroups: vl.lightgroups.add(name=g)
    sun.lightgroup = 'nang'; world.lightgroup = 'troi'
    return sun, sky, bg
def set_pass(p, sun, sky, bg):
    hr = PASSES[p]; alt, az = sun_at(hr)
    sun.rotation_euler = (math.radians(90 - alt), 0, math.radians(-az + 180))
    sun.data.energy = 5.0 if alt > 12 else 2.8 + 2.2 * max(0, alt) / 12; sun.data.angle = math.radians(0.53)
    warm = max(0.0, min(1.0, (20 - alt) / 20)); sun.data.color = (1.0, 1.0 - 0.4 * warm, 1.0 - 0.7 * warm)
    sky.sun_elevation = math.radians(alt); sky.sun_rotation = math.radians(-az + 180 + 180)
    try: sky.sun_disc = False
    except Exception: pass
    try: sky.air_density = 1.0; sky.dust_density = 1.6 if alt < 12 else 0.5; sky.ozone_density = 1.0
    except Exception: pass
    bg.inputs[1].default_value = 0.22 if alt > 12 else 0.3
    return alt, az

# ---------------------------------------------------------------- tờ sprite
NA = 8; ROWD = 16.0; PITCH = math.radians(-8.0)
head = math.radians(A.head); fwd = Vector((math.sin(head), math.cos(head), 0)); right = Vector((math.cos(head), -math.sin(head), 0))
ROLES = N6.roles(EP)
def poses_for(R0, R):
    if R0.get('pair'): return [f'w{k}' for k in range(8)]
    ps = ['st'] + [f'w{k}' for k in range(8)] + [f'wl{k}' for k in range(8)] + ['talk', 'look', 'back', 'work_' + R['work']]
    if R.get('carry'): ps += [f'c{R["carry"]}{k}' for k in range(8)]
    return ps
roles = A.roles.split(','); meta = {'epoch': EP, 'head': A.head, 'pxm': A.pxm, 'na': NA, 'rowd': ROWD, 'pitch_deg': -8.0, 'roles': {}, 'nguon': N6.ROLE_SRC[EP],
                                    'nguoi': 'tự dựng (nguoi6.py: SDF + marching cubes) — không MPFB', 'anh_sang': 'Nishita + mặt trời như build_scene.set_pass; light group nang/troi'}
GROUND_ALB = (0.3, 0.24, 0.17) if EP == 1782 else (0.22, 0.21, 0.2)
jf = os.path.join(A.out, f'sprites-{"-".join(roles)}.json')
if os.path.exists(jf): meta['roles'].update(json.load(open(jf))['roles'])
for role in roles:
    if role not in ROLES: continue
    R0 = ROLES[role]; pair = R0.get('pair'); R = ROLES[pair] if pair else R0
    nb = 1 if pair else NB.get(role, 3)
    for bi in range(nb):
        rname = role if pair else f'{role}~{bi}'
        if rname in meta['roles'] and all(os.path.exists(os.path.join(A.out, f'{rname}_{p}.exr')) for p in A.passes.split(',')):
            print('đã có', rname); continue
        bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene; MATS.clear()
        PS = poses_for(R0, R); CELLX = 3.6 if pair else 1.5; NP = len(PS); cells = []
        if A.test: PS = ['st', 'w1', 'wl3', 'talk', 'work_' + R['work']] + ([f'c{R["carry"]}2'] if R.get('carry') else []) if not pair else ['w0', 'w2']; NP = len(PS)
        rr = random.Random(EP * 100 + roles.index(role) * 7 + bi)
        protos = []
        for j, (rl, b_) in enumerate(([(pair, 0), (pair, 1)] if pair else [(role, bi)])):
            Rj = ROLES[rl]; body, objs, skin, hair = build_person(rl, Rj, b_, f'P{j}')
            hatless = b_ in Rj.get('nohat_b', ())
            ao, parts = rig_person(body, objs, Rj, f'P{j}', b_, hatless)
            for o, _, _ in objs: o.hide_render = True
            for p in parts: p.hide_render = True
            ao.hide_render = True; protos.append((ao, parts, objs, Rj))
        CACHE = {}
        def posed(j, pn_):
            if (j, pn_) in CACHE: return CACHE[(j, pn_)]
            ao_, pa_, ob_, Rj = protos[j]; pose(ao_, pn_, Rj, rr)
            its = items(ao_, Rj, pn_) if not pair else []
            for p in its: p.hide_render = True
            dg = bpy.context.evaluated_depsgraph_get(); zmin = 9.0
            for o, _, _ in ob_:
                if 'giay' in o.name or 'than' in o.name or 'vay' in o.name:
                    me_ = o.evaluated_get(dg).to_mesh(); zmin = min(zmin, min(v_.co.z for v_ in me_.vertices)); o.evaluated_get(dg).to_mesh_clear()
            CACHE[(j, pn_)] = ({pb.name: pb.matrix_basis.copy() for pb in ao_.pose.bones}, zmin, its); return CACHE[(j, pn_)]
        for ai in range(NA):
            if A.test and ai not in (0, 1, 2, 4): continue
            for pi, pn in enumerate(PS):
                d = (-fwd); a = math.radians(45 * ai); d = Vector((d.x * math.cos(a) - d.y * math.sin(a), d.x * math.sin(a) + d.y * math.cos(a), 0))
                yaw = math.atan2(d.y, d.x) - math.atan2(-1, 0)
                u = (pi - (NP - 1) / 2) * CELLX; v = ai * ROWD; pos = right * u + fwd * v
                mem = [(0, f'cbarrow{int(pn[1:])}', 0.85), (1, f'cbarrow{(int(pn[1:]) + 4) % 8}', -0.85)] if pair else [(0, pn, 0.0)]
                for j, pn_, off in mem:
                    basis, zmin, its = posed(j, pn_)
                    ao_, pa_, ob_, _ = protos[j]; a2 = clone(ao_, pa_, ob_, f'{rname}_{ai}_{pi}_{j}')
                    for bn, mb in basis.items(): a2.pose.bones[bn].matrix_basis = mb
                    for p in its:
                        p2 = p.copy(); sc.collection.objects.link(p2); p2.parent = a2; p2.hide_render = False
                    p_ = pos + d * off; a2.location = (p_.x, p_.y, -zmin + 0.004); a2.rotation_euler = (0, 0, yaw)
                if pair:   # thùng (1782) / hòm (1943) giữa hai người, hai đòn khiêng dọc hướng đi
                    c = pos + Vector((0, 0, 0.5))
                    if R0['item'] == 'barrel': prim('cyl', c, (0.27, 0.27, 0.36), (0.32, 0.22, 0.13), (0, math.pi / 2, yaw + math.pi / 2), 'wood')
                    else: prim('cube', c, (0.4, 0.3, 0.24), (0.36, 0.33, 0.22), (0, 0, yaw), 'wood')
                    for s_ in (-1, 1):
                        side = Vector((-d.y, d.x, 0)) * 0.25 * s_; prim('cube', pos + side + Vector((0, 0, 0.66)), (0.022, 1.15, 0.022), (0.28, 0.2, 0.12), (0, 0, yaw), 'wood')
                cells.append({'a': ai, 'p': pi, 'pose': pn, 'world': [pos.x, pos.y], 'dir': [d.x, d.y]})
        # thẻ xám 18 % nằm ngang (hiệu chuẩn tỉ số bóng/nắng của sprite cho live6) — ô riêng cuối hàng 0
        u = (NP + 0.6 - (NP - 1) / 2) * CELLX; pc = right * u
        bpy.ops.mesh.primitive_plane_add(size=0.8, location=(pc.x, pc.y, 0.01)); card = bpy.context.object; card.data.materials.append(mat('cloth')); paint(card, np.tile((0.18, 0.18, 0.18), (4, 1)))
        bpy.ops.mesh.primitive_plane_add(size=600, location=(0, 0, -0.002)); gp = bpy.context.object                       # đất hắt sáng (ẩn với máy)
        gm = bpy.data.materials.new('dat'); gm.use_nodes = True; gm.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (*GROUND_ALB, 1)
        gm.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.95; gp.data.materials.append(gm); gp.visible_camera = False
        bpy.context.view_layer.update()
        cam = bpy.data.cameras.new('c'); cam.type = 'ORTHO'
        Wm = (NP + 1.4) * CELLX; Hm = (NA - 1) * ROWD * math.sin(abs(PITCH)) + 2.7
        W, H = int(Wm * A.pxm), int(Hm * A.pxm); cam.ortho_scale = max(Wm, Hm)
        co = bpy.data.objects.new('c', cam); sc.collection.objects.link(co); sc.camera = co
        mid = fwd * ((NA - 1) * ROWD / 2) + right * (0.7 * CELLX); D = 200.0
        co.location = (mid.x - fwd.x * D * math.cos(PITCH), mid.y - fwd.y * D * math.cos(PITCH), 0.95 + D * math.sin(-PITCH))
        co.rotation_euler = (math.radians(90) + PITCH, 0, -head)
        sc.render.resolution_x, sc.render.resolution_y = W, H; sc.render.resolution_percentage = 100
        from bpy_extras.object_utils import world_to_camera_view
        bpy.context.view_layer.update()
        for c_ in cells:
            p = world_to_camera_view(sc, co, Vector((c_['world'][0], c_['world'][1], 0))); c_['foot_px'] = [round(p.x * W, 1), round((1 - p.y) * H, 1)]
        pcard = world_to_camera_view(sc, co, Vector((pc.x, pc.y, 0.01))); card_px = [round(pcard.x * W, 1), round((1 - pcard.y) * H, 1)]
        if A.test:
            xs_ = [c_['foot_px'][0] for c_ in cells] + [card_px[0]]; ys_ = [c_['foot_px'][1] for c_ in cells]
            sc.render.use_border = True; sc.render.use_crop_to_border = False
            sc.render.border_min_x = max(0, (min(xs_) - CELLX * A.pxm) / W); sc.render.border_max_x = min(1, (max(xs_) + CELLX * A.pxm) / W)
            sc.render.border_min_y = max(0, 1 - (max(ys_) + 0.3 * A.pxm) / H); sc.render.border_max_y = min(1, 1 - (min(ys_) - 2.3 * A.pxm) / H)
        sc.render.film_transparent = True
        sun, sky, bgn = setup_light(sc)
        sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = A.spp; sc.cycles.use_denoising = True; sc.render.use_persistent_data = True
        sc.cycles.denoiser = 'OPENIMAGEDENOISE'; sc.cycles.max_bounces = 4; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 2
        sc.render.threads_mode = 'FIXED'; sc.render.threads = A.threads
        sc.view_settings.view_transform = 'AgX'
        try: sc.render.image_settings.media_type = 'MULTI_LAYER_IMAGE'
        except Exception: sc.render.image_settings.file_format = 'OPEN_EXR_MULTILAYER'
        sc.render.image_settings.color_depth = '16'
        try: sc.view_layers[0].cycles.denoising_store_passes = False
        except Exception: pass
        rmeta = {'W': W, 'H': H, 'cellx': CELLX, 'poses': PS, 'cells': cells, 'card_px': card_px, 'passes': {}, 'render_s': {}, 'pair': bool(pair),
                 'faces': int(sum(len(o.data.polygons) for _, _, ob_, _ in protos for o, _, _ in ob_))}
        for p in A.passes.split(','):
            alt, az = set_pass(p, sun, sky, bgn)
            t = time.time(); sc.render.filepath = os.path.join(A.out, f'{rname}_{p}.exr')
            if not os.path.exists(sc.render.filepath): bpy.ops.render.render(write_still=True)
            rmeta['passes'][p] = {'sun_alt': round(alt, 2), 'sun_az': round(az, 2)}; rmeta['render_s'][p] = round(time.time() - t, 1)
            print('SPRITE', rname, p, W, H, rmeta['render_s'][p], round(time.time() - T0), flush=True)
        meta['roles'][rname] = rmeta
        json.dump(meta, open(jf, 'w'), indent=1, ensure_ascii=False)
        if A.blend and bi == 0: bpy.ops.wm.save_as_mainfile(filepath=A.blend.replace('.blend', f'-{rname}.blend'))
json.dump(meta, open(jf, 'w'), indent=1, ensure_ascii=False)
print('DONE', round(time.time() - T0, 1))
