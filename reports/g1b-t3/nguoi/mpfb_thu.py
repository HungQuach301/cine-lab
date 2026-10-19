"""G1b-T3 · việc 6.1 — THỬ DỰNG NGƯỜI TỪ DỮ LIỆU MPFB2 / MakeHuman (CC0) bằng BỘ NẠP CHỈ ĐỌC DỮ LIỆU (Kinh thánh §11.6): không chạy mã GPL của MPFB,
chỉ đọc tài sản CC0: base.obj (lưới gốc + UV), targets/macrodetails (giới/tuổi/cơ/cân), rigs/standard (khung xương + trọng số), da makehuman_system_assets.
Ra 1 người 1782 (lính bộ binh Anh: áo đỏ, gi-lê/quần trắng, ghệt đen, mũ tricorn) + 1 người 1943 (battledress kaki, mũ Brodie, ghệt) — ảnh tĩnh Cycles.
Quần áo = vùng vẽ trên da theo xương trội (+ vạt áo 1782 là lưới riêng) — bản THỬ, chưa phải bộ quần áo MHCLO.
  /opt/bpy/bin/python -I mpfb_thu.py <mpfb2/src/mpfb/data> <thư mục skins> <thư mục ra> [spp]"""
import sys, os, json, gzip, math, time
import bpy, bmesh
from mathutils import Vector, Matrix, Quaternion
DATA, SKINS, OUT = sys.argv[1:4]; SPP = int(sys.argv[4]) if len(sys.argv) > 4 else 64
os.makedirs(OUT, exist_ok=True)

def read_obj(p):
    V, VT, F, G = [], [], [], []; g = None
    for l in open(p):
        if l.startswith('v '): V.append([float(a) for a in l.split()[1:4]])
        elif l.startswith('vt '): VT.append([float(a) for a in l.split()[1:3]])
        elif l.startswith('g '): g = l.split()[1]
        elif l.startswith('f '):
            ix = [w.split('/') for w in l.split()[1:]]; F.append(([int(a[0]) - 1 for a in ix], [int(a[1]) - 1 if len(a) > 1 and a[1] else -1 for a in ix])); G.append(g)
    return V, VT, F, G

def target(name, V, w):
    if w <= 0: return
    for l in gzip.open(os.path.join(DATA, 'targets', name), 'rt'):
        if not l.strip() or l[0] == '#': continue
        a = l.split(); i = int(a[0]); V[i][0] += w * float(a[1]); V[i][1] += w * float(a[2]); V[i][2] += w * float(a[3])

def human(spec):
    V, VT, F, G = read_obj(os.path.join(DATA, '3dobjs', 'base.obj'))
    # macro: male, young, cân/cơ trung bình (+ chút cơ cho lính), chủng tộc châu Âu
    target('macrodetails/universal-male-young-averagemuscle-averageweight.target.gz', V, 1 - spec['muscle'])
    target('macrodetails/universal-male-young-maxmuscle-averageweight.target.gz', V, spec['muscle'])
    target('macrodetails/caucasian-male-young.target.gz', V, 1.0)
    W = [[x / 10, -z / 10, y / 10] for x, y, z in V]   # OBJ (dm, Y lên) → Blender (m, Z lên)
    groups = {}
    for (vi, _), g in zip(F, G): groups.setdefault(g, set()).update(vi)
    return W, VT, F, G, groups

def region(spec, bn, z, top, y, yc=0.0):
    if any(k in bn for k in ('head', 'jaw', 'eye', 'tongue', 'levator', 'oris', 'orbicularis', 'temporalis', 'risorius', 'special', 'neck')):
        if 'neck' in bn: return 'neck'
        if z > top - 0.07 or (z > top - 0.2 and y > yc + 0.045): return 'hair'   # đỉnh đầu + gáy
        return 'skin'
    if any(k in bn for k in ('finger', 'metacarpal', 'wrist', 'thumb')): return 'skin'
    if 'foot' in bn or 'toe' in bn: return 'shoe'
    if 'lowerleg' in bn: return spec['shin_rule'](z)
    if 'upperleg' in bn: return spec['thigh_rule'](z)
    if 'pelvis' in bn: return spec['pelvis_rule'](z)
    return 'coat'

def build(spec, x0):
    W, VT, F, G, groups = human(spec)
    zmin = min(W[i][2] for i in groups['body'])
    W = [[p[0] + x0, p[1], p[2] - zmin] for p in W]
    wts = json.load(open(os.path.join(DATA, 'rigs', 'standard', 'weights.default.json')))['weights']
    domo = {}
    for bn, L in wts.items():
        for vi, w in L:
            if w > domo.get(vi, ('', 0))[1]: domo[vi] = (bn, w)
    keep = ('body', 'helper-l-eye', 'helper-r-eye')
    body_f = [k for k, g in enumerate(G) if g in keep]
    used = sorted({i for k in body_f for i in F[k][0]}); remap = {o: n for n, o in enumerate(used)}
    # vùng theo đỉnh (xương trội + độ cao) → phồng vải theo pháp tuyến (áo dày hơn da, giày bọc ngón)
    eye = {i for k, g in enumerate(G) if g in keep[1:] for i in F[k][0]}
    top = max(W[i][2] for i in groups['body']); vreg = {}
    hv = [i for i in used if domo.get(i, ('', 0))[0] == 'head']; yc = sum(W[i][1] for i in hv) / len(hv)
    for i in used:
        vreg[i] = 'eye' if i in eye else region(spec, domo.get(i, ('spine01', 1))[0], W[i][2], top, W[i][1], yc)
    nrm = {i: Vector((0, 0, 0)) for i in used}
    for k in body_f:
        a, b, c = (Vector(W[F[k][0][j]]) for j in range(3)); n = (b - a).cross(c - a)
        for i in F[k][0]: nrm[i] += n
    INF = spec['inflate']
    P = []
    for i in used:
        d = INF.get(vreg[i], 0.0); n = nrm[i].normalized() if nrm[i].length > 0 else Vector((0, 0, 0))
        P.append([W[i][0] + n.x * d, W[i][1] + n.y * d, W[i][2] + n.z * d])
    me = bpy.data.meshes.new(spec['name']); me.from_pydata(P, [], [[remap[i] for i in F[k][0]] for k in body_f]); me.update()
    uv = me.uv_layers.new(name='UV')
    for poly, k in zip(me.polygons, body_f):
        for li, vt in zip(poly.loop_indices, F[k][1]): uv.data[li].uv = VT[vt] if vt >= 0 else (0, 0)
    ob = bpy.data.objects.new(spec['name'], me); bpy.context.scene.collection.objects.link(ob)
    for p in me.polygons: p.use_smooth = True
    # khung xương từ rig.default.json, vị trí khớp tính lại trên lưới đã biến hình
    rig = json.load(open(os.path.join(DATA, 'rigs', 'standard', 'rig.default.json')))
    def pos(d):
        s = d['strategy']
        if s == 'CUBE': ids = groups[d['cube_name']]
        elif s == 'VERTEX': ids = [d['vertex_index']]
        else: ids = d['vertex_indices']
        return Vector([sum(W[i][c] for i in ids) / len(ids) for c in range(3)])
    arm = bpy.data.armatures.new(spec['name'] + '_rig'); ao = bpy.data.objects.new(spec['name'] + '_rig', arm); bpy.context.scene.collection.objects.link(ao)
    bpy.context.view_layer.objects.active = ao; bpy.ops.object.mode_set(mode='EDIT')
    for n, b in rig.items():
        eb = arm.edit_bones.new(n); eb.head = pos(b['head']); eb.tail = pos(b['tail'])
        if (eb.tail - eb.head).length < 1e-4: eb.tail = eb.head + Vector((0, 0, 0.01))
        eb.roll = b.get('roll', 0)
    for n, b in rig.items():
        if b.get('parent'): arm.edit_bones[n].parent = arm.edit_bones[b['parent']]
    bpy.ops.object.mode_set(mode='OBJECT')
    wts = json.load(open(os.path.join(DATA, 'rigs', 'standard', 'weights.default.json')))['weights']
    dom = {}
    for bn, L in wts.items():
        vg = ob.vertex_groups.new(name=bn)
        for vi, w in L:
            if vi in remap: vg.add([remap[vi]], w, 'REPLACE');
            if vi in remap and w > dom.get(remap[vi], ('', 0))[1]: dom[remap[vi]] = (bn, w)
    md = ob.modifiers.new('rig', 'ARMATURE'); md.object = ao
    # tư thế: tay buông (cánh tay trên xoay về gần thẳng đứng, dang 7°), khuỷu chùng
    bpy.context.view_layer.objects.active = ao; bpy.ops.object.mode_set(mode='POSE')
    def aim(bn, target_dir):
        pb = ao.pose.bones[bn]; bpy.context.view_layer.update()
        cur = (pb.tail - pb.head).normalized(); q = cur.rotation_difference(target_dir.normalized())
        M = pb.matrix.copy(); t = M.to_translation(); R = q.to_matrix().to_4x4() @ Matrix(M.to_3x3()).to_4x4()
        R.translation = t; pb.matrix = R; bpy.context.view_layer.update()
    for sd, sx in (('L', 1), ('R', -1)):
        aim(f'upperarm01.{sd}', Vector((sx * math.sin(math.radians(7)), 0.02, -1)))
        aim(f'lowerarm01.{sd}', Vector((sx * 0.05, -0.18, -1)))
    bpy.ops.object.mode_set(mode='OBJECT')
    mats = {}; inv = {n: o for o, n in remap.items()}
    for p in me.polygons:
        c = {}
        for vi in p.vertices: r = vreg[inv[vi]]; c[r] = c.get(r, 0) + 1
        r = max(c, key=c.get)
        if r not in mats: mats[r] = len(mats); me.materials.append(spec['mat'][r]())
        p.material_index = mats[r]
    zs = [v.co.z for v in me.vertices]; H = max(zs) - min(zs)
    head = [me.vertices[remap[i]].co for i in used if domo.get(i, ('', 0))[0] == 'head']
    top = max(v.z for v in head); hc = Vector((sum(v.x for v in head) / len(head), sum(v.y for v in head) / len(head), top))
    return ob, ao, H, hc

# ---------- vật liệu ----------
def mat_color(name, rgb, rough=0.85, bump=0.25, scale=900.0, sheen=0.0, mix_white=None):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*rgb, 1); b.inputs['Roughness'].default_value = rough
    if 'Sheen Weight' in b.inputs: b.inputs['Sheen Weight'].default_value = sheen
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = scale; nz.inputs['Detail'].default_value = 4
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump; nt.links.new(nz.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    # loang màu nhẹ theo vải
    nz2 = nt.nodes.new('ShaderNodeTexNoise'); nz2.inputs['Scale'].default_value = 18
    mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.inputs['Factor'].default_value = 0.12
    mx.inputs['A'].default_value = (*rgb, 1); mx.inputs['B'].default_value = (rgb[0] * 0.75, rgb[1] * 0.75, rgb[2] * 0.75, 1)
    nt.links.new(nz2.outputs['Fac'], mx.inputs['Factor']); out = mx.outputs['Result']
    if mix_white:   # gi-lê trắng lộ trước ngực + dây đeo chéo (toạ độ đối tượng) — áo 1782
        tc = nt.nodes.new('ShaderNodeTexCoord'); sp = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Object'], sp.inputs['Vector'])
        mw = nt.nodes.new('ShaderNodeMath'); mw.operation = 'ABSOLUTE'
        sub = nt.nodes.new('ShaderNodeMath'); sub.operation = 'SUBTRACT'; nt.links.new(sp.outputs['X'], sub.inputs[0]); sub.inputs[1].default_value = mix_white['x0']
        nt.links.new(sub.outputs[0], mw.inputs[0])
        lt = nt.nodes.new('ShaderNodeMath'); lt.operation = 'LESS_THAN'; nt.links.new(mw.outputs[0], lt.inputs[0]); lt.inputs[1].default_value = mix_white['w']
        fr = nt.nodes.new('ShaderNodeMath'); fr.operation = 'LESS_THAN'; nt.links.new(sp.outputs['Y'], fr.inputs[0]); fr.inputs[1].default_value = -0.05
        mul = nt.nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; nt.links.new(lt.outputs[0], mul.inputs[0]); nt.links.new(fr.outputs[0], mul.inputs[1])
        zl = nt.nodes.new('ShaderNodeMath'); zl.operation = 'GREATER_THAN'; nt.links.new(sp.outputs['Z'], zl.inputs[0]); zl.inputs[1].default_value = mix_white['z0']
        mul2 = nt.nodes.new('ShaderNodeMath'); mul2.operation = 'MULTIPLY'; nt.links.new(mul.outputs[0], mul2.inputs[0]); nt.links.new(zl.outputs[0], mul2.inputs[1])
        m2 = nt.nodes.new('ShaderNodeMix'); m2.data_type = 'RGBA'; nt.links.new(mul2.outputs[0], m2.inputs['Factor']); nt.links.new(out, m2.inputs['A']); m2.inputs['B'].default_value = (0.82, 0.79, 0.71, 1); out = m2.outputs['Result']
    nt.links.new(out, b.inputs['Base Color']); return m

def mat_skin(png):
    m = bpy.data.materials.new('skin'); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    t = nt.nodes.new('ShaderNodeTexImage'); t.image = bpy.data.images.load(png); nt.links.new(t.outputs['Color'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.55
    if 'Subsurface Weight' in b.inputs: b.inputs['Subsurface Weight'].default_value = 0.15; b.inputs['Subsurface Radius'].default_value = (0.01, 0.004, 0.002)
    return m

def ring_mesh(name, rings, nseg, open_front=0.0, mat=None, thick=0.012):
    """vỏ tròn xoay: rings = [(z, cx, cy, rx, ry)…]; open_front: nửa góc mở phía trước (−Y) — vạt áo"""
    bm = bmesh.new(); prev = None
    for z, cx, cy, rx, ry in rings:
        cur = []
        for i in range(nseg + 1):
            a = -math.pi / 2 + open_front + (2 * math.pi - 2 * open_front) * i / nseg
            cur.append(bm.verts.new((cx + math.cos(a) * rx, cy + math.sin(a) * ry, z)))
        if prev:
            for i in range(nseg): bm.faces.new((prev[i], prev[i + 1], cur[i + 1], cur[i]))
        prev = cur
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    for p in me.polygons: p.use_smooth = True
    s = ob.modifiers.new('day', 'SOLIDIFY'); s.thickness = thick; ob.data.materials.append(mat); return ob

def tricorn(hc, mat, lace):
    bm = bmesh.new(); n = 36; crown = []; brim_i = []; brim_o = []
    for i in range(n):
        a = i / n * 2 * math.pi; R = 0.165 + 0.03 * math.cos(3 * a); Hh = 0.05 + 0.045 * max(0, math.cos(3 * (a - math.pi / 3)))
        brim_i.append(bm.verts.new((hc.x + math.cos(a) * 0.095, hc.y + math.sin(a) * 0.088, hc.z - 0.035)))
        brim_o.append(bm.verts.new((hc.x + math.cos(a) * R, hc.y + math.sin(a) * R * 0.95, hc.z - 0.035 + Hh)))
        crown.append(bm.verts.new((hc.x + math.cos(a) * 0.088, hc.y + math.sin(a) * 0.08, hc.z + 0.045)))
    for i in range(n):
        j = (i + 1) % n; bm.faces.new((brim_i[i], brim_o[i], brim_o[j], brim_i[j])); bm.faces.new((brim_i[i], brim_i[j], crown[j], crown[i]))
    bm.faces.new(crown)
    me = bpy.data.meshes.new('tricorn'); bm.to_mesh(me); bm.free(); ob = bpy.data.objects.new('tricorn', me); bpy.context.scene.collection.objects.link(ob)
    s = ob.modifiers.new('day', 'SOLIDIFY'); s.thickness = 0.012; ob.data.materials.append(mat)
    # mép vành viền lace: ống mảnh theo mép ngoài
    pts = [v.co.copy() for v in me.vertices][1::3]
    cu = bpy.data.curves.new('lace', 'CURVE'); cu.dimensions = '3D'; sp = cu.splines.new('POLY'); sp.points.add(len(pts));
    for k, p in enumerate(pts + [pts[0]]): sp.points[k].co = (*p, 1)
    cu.bevel_depth = 0.006; lo = bpy.data.objects.new('lace', cu); bpy.context.scene.collection.objects.link(lo); lo.data.materials.append(lace)
    for p in me.polygons: p.use_smooth = True
    return ob

def brodie(hc, mat):
    bm = bmesh.new(); n = 40; rings = []
    prof = [(0.0, 0.17), (0.012, 0.165), (0.02, 0.135), (0.03, 0.112), (0.07, 0.104), (0.105, 0.082), (0.13, 0.045), (0.14, 0.0)]
    for dz, r in prof:
        rings.append([bm.verts.new((hc.x + math.cos(i / n * 2 * math.pi) * r, hc.y + math.sin(i / n * 2 * math.pi) * r * 0.92, hc.z - 0.06 + dz)) for i in range(n)])
    for a, b in zip(rings, rings[1:]):
        for i in range(n):
            j = (i + 1) % n
            if b[i] is b[j]: continue
            try: bm.faces.new((a[i], a[j], b[j], b[i]))
            except ValueError: pass
    me = bpy.data.meshes.new('brodie'); bm.to_mesh(me); bm.free(); ob = bpy.data.objects.new('brodie', me); bpy.context.scene.collection.objects.link(ob)
    for p in me.polygons: p.use_smooth = True
    s = ob.modifiers.new('day', 'SOLIDIFY'); s.thickness = 0.006; ob.data.materials.append(mat); return ob

# ---------- cảnh ----------
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = SPP; sc.cycles.use_denoising = True
sc.render.threads_mode = 'FIXED'; sc.render.threads = 2; sc.render.resolution_x, sc.render.resolution_y = 1200, 1000; sc.render.film_transparent = False
skin = os.path.join(SKINS, 'young_caucasian_male', 'young_lightskinned_male_diffuse.png')
red = lambda: mat_color('coat_red', (0.42, 0.045, 0.035), mix_white={'x0': -0.45, 'w': 0.045, 'z0': 1.05})
S1782 = {'name': 'linh1782', 'muscle': 0.3, 'inflate': {'coat': 0.014, 'breech': 0.008, 'gaiter': 0.01, 'shoe': 0.016, 'hair': 0.012, 'neck': 0.01},
         'shin_rule': lambda z: 'gaiter', 'thigh_rule': lambda z: 'breech', 'pelvis_rule': lambda z: 'breech',
         'mat': {'skin': lambda: mat_skin(skin), 'eye': lambda: mat_color('eye', (0.03, 0.025, 0.02), rough=0.2, bump=0), 'hair': lambda: mat_color('hair_powder', (0.62, 0.6, 0.55), bump=0.6, scale=400), 'neck': lambda: mat_color('stock', (0.06, 0.05, 0.045)), 'coat': red, 'breech': lambda: mat_color('breech', (0.78, 0.74, 0.65)),
                 'gaiter': lambda: mat_color('gaiter', (0.03, 0.028, 0.025), rough=0.6), 'shoe': lambda: mat_color('shoe', (0.02, 0.018, 0.016), rough=0.35, bump=0.05)}}
khaki = (0.21, 0.18, 0.11)
S1943 = {'name': 'linh1943', 'muscle': 0.35, 'inflate': {'coat': 0.02, 'trouser': 0.016, 'anklet': 0.02, 'shoe': 0.018, 'hair': 0.006},
         'shin_rule': lambda z: 'anklet' if z < 0.2 else 'trouser', 'thigh_rule': lambda z: 'trouser', 'pelvis_rule': lambda z: 'trouser',
         'mat': {'skin': lambda: mat_skin(skin), 'eye': lambda: mat_color('eye', (0.03, 0.025, 0.02), rough=0.2, bump=0), 'hair': lambda: mat_color('hair', (0.06, 0.04, 0.025), bump=0.6, scale=400), 'neck': lambda: mat_skin(skin), 'coat': lambda: mat_color('bd_blouse', khaki, bump=0.35, scale=1200), 'trouser': lambda: mat_color('bd_trouser', (0.2, 0.17, 0.105), bump=0.35, scale=1200),
                 'anklet': lambda: mat_color('anklet', (0.36, 0.33, 0.24)), 'shoe': lambda: mat_color('boot', (0.025, 0.02, 0.016), rough=0.4, bump=0.05)}}
t0 = time.time()
o1, a1, H1, hc1 = build(S1782, -0.45)
o2, a2, H2, hc2 = build(S1943, 0.45)
print('cao (m)', round(H1, 3), round(H2, 3), 'dựng lưới', round(time.time() - t0, 1), 's')
tricorn(hc1 + Vector((0, 0, 0.0)), mat_color('felt', (0.025, 0.022, 0.02), rough=0.9), mat_color('lace', (0.85, 0.83, 0.76)))
# vạt áo 1782: vỏ từ eo xuống gối, mở phía trước, lưng xẻ — theo hông của chính lưới
hip = [v.co for v in o1.data.vertices if 0.85 < v.co.z < 1.0 and abs(v.co.x + 0.45) < 0.19]; cx1 = sum(v.x for v in hip) / len(hip); cy1 = sum(v.y for v in hip) / len(hip)
rx = max(abs(v.x - cx1) for v in hip); ry = max(abs(v.y - cy1) for v in hip)
ring_mesh('vat_ao', [(1.02, cx1, cy1, rx * 1.06, ry * 1.12), (0.75, cx1, cy1 + 0.01, rx * 1.25, ry * 1.4), (0.5, cx1, cy1 + 0.03, rx * 1.38, ry * 1.6)], 28, open_front=0.75, mat=red(), thick=0.01)
brodie(hc2 + Vector((0, 0, 0.0)), mat_color('helmet', (0.17, 0.16, 0.1), rough=0.55, bump=0.6, scale=300))
# đai (webbing) 1943 ở eo
hip2 = [v.co for v in o2.data.vertices if 0.98 < v.co.z < 1.06 and abs(v.co.x - 0.45) < 0.19]; cx2 = sum(v.x for v in hip2) / len(hip2); cy2 = sum(v.y for v in hip2) / len(hip2)
rx2 = max(abs(v.x - cx2) for v in hip2); ry2 = max(abs(v.y - cy2) for v in hip2)
ring_mesh('dai', [(1.0, cx2, cy2, rx2 * 1.04, ry2 * 1.06), (1.055, cx2, cy2, rx2 * 1.03, ry2 * 1.05)], 32, mat=mat_color('webbing', (0.33, 0.3, 0.2), bump=0.5), thick=0.008)
# nền + trời + nắng
bpy.ops.mesh.primitive_plane_add(size=30); gp = bpy.context.object; gm = mat_color('dat', (0.42, 0.36, 0.27), rough=0.95, bump=0.4, scale=60); gp.data.materials.append(gm)
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; sky = w.node_tree.nodes.new('ShaderNodeTexSky')
try: sky.sky_type = 'NISHITA'
except Exception: pass
w.node_tree.links.new(sky.outputs['Color'], w.node_tree.nodes['Background'].inputs['Color']); w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.22
sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = 4.0; sun.angle = math.radians(0.53); so = bpy.data.objects.new('sun', sun); sc.collection.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(35))
cam = bpy.data.cameras.new('cam'); cam.lens = 70; co = bpy.data.objects.new('cam', cam); sc.collection.objects.link(co); sc.camera = co
co.location = (0.9, -5.2, 1.25); co.rotation_euler = (math.radians(88), 0, math.radians(9))
sc.view_settings.view_transform = 'AgX' if 'AgX' in [i.identifier for i in sc.view_settings.bl_rna.properties['view_transform'].enum_items] else 'Filmic'
sc.render.filepath = os.path.join(OUT, 'mpfb-1782-1943.png'); t1 = time.time(); bpy.ops.render.render(write_still=True)
print('render', round(time.time() - t1, 1), 's ->', sc.render.filepath)
# góc xa (≈ 35 px/người như P4) để so với người people.js
cam.lens = 70; co.location = (0.0, -60.0, 14.0); co.rotation_euler = (math.radians(77.5), 0, 0); sc.cycles.samples = max(16, SPP // 2)
sc.render.resolution_x, sc.render.resolution_y = 1920, 1080; sc.render.filepath = os.path.join(OUT, 'mpfb-xa.png'); bpy.ops.render.render(write_still=True)
json.dump({'cao_m': [round(H1, 3), round(H2, 3)], 'giay_dung': round(t1 - t0, 1), 'giay_render': round(time.time() - t1, 1), 'spp': SPP}, open(os.path.join(OUT, 'mpfb-thu.json'), 'w'))
