"""PT2 · lớp sống — tờ sprite NGƯỜI từ lưới gốc MakeHuman/MPFB2 (CC0: base.obj + targets macrodetails + rig/weights 'default'),
nạp bằng mã TỰ VIẾT (chỉ đọc dữ liệu, KHÔNG chạy mã addon MPFB). Trang phục do PT2 dựng: tô vùng theo xương chi phối trên lớp vỏ
'helper-tights' của chính lưới gốc (áo/quần), 'helper-skirt' (vạt áo dài 1782 / váy), mũ + súng từ khối cơ bản gắn xương.
Mỗi vai: 8 hướng × (đứng + 8 pha chu kỳ đi) — máy trực giao cùng hướng + cúi 8° như máy neo, mặt trời y hệt lượt nền,
KHÔNG mặt bắt bóng (alpha = thân người); bóng đổ dựng khi ghép: hình bóng chiếu theo hướng mặt trời của lượt, chỉ nơi lượt nắng của cảnh A sáng.
  /opt/bpy/bin/python design/pt/lai/mh_people.py -- --epoch 1782|1943 --head <độ> --roles a,b --passes d1,..,n --out DIR [--pxm 90] [--spp 12]
Nguồn trang phục (mô tả, TIEN-KY T3 / claims vây hãm): 1782 bộ binh áo đỏ đai chéo trắng mũ ba góc, pháo binh áo lam đậm; 1943 lính kaki
battledress, hải quân lam đậm/trắng, RAF xám lam; 1943 KHÔNG phụ nữ/trẻ em (dân sơ tán 1940 — S114)."""
import bpy, bmesh, math, sys, os, json, gzip, argparse, random, time
from mathutils import Vector, Matrix
ap = argparse.ArgumentParser(); ap.add_argument('--epoch', type=int, required=True); ap.add_argument('--head', type=float, required=True)
ap.add_argument('--roles', required=True); ap.add_argument('--passes', default='d1,d2,d3,d4,n'); ap.add_argument('--out', required=True)
ap.add_argument('--pxm', type=int, default=90); ap.add_argument('--spp', type=int, default=12); ap.add_argument('--mp', default='/var/tmp/pt2/mpfb2/src/mpfb/data')
ap.add_argument('--test', action='store_true')
A = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]); os.makedirs(A.out, exist_ok=True)
HERE = os.path.dirname(os.path.abspath(__file__)); EP = A.epoch; T0 = time.time()
PASSES = json.load(open(os.path.join(HERE, '..', 'scene', 'passes.json')))
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene

# ---------------------------------------------------------------- đọc lưới gốc + targets (OBJ: y lên, dm) → Blender (x, −z, y) × 0,1
def read_obj(p):
    V, F, G = [], [], {}; g = None
    for line in open(p):
        if line.startswith('v '): x, y, z = map(float, line.split()[1:4]); V.append([x, y, z])
        elif line.startswith('g '): g = line.split()[1]
        elif line.startswith('f '): F.append((g, [int(t.split('/')[0]) - 1 for t in line.split()[1:]]))
    return V, F
def read_target(rel):
    out = []
    for line in gzip.open(os.path.join(A.mp, 'targets', rel), 'rt'):
        if line[:1].isdigit(): i, dx, dy, dz = line.split(); out.append((int(i), float(dx), float(dy), float(dz)))
    return out
V, F = read_obj(os.path.join(A.mp, '3dobjs', 'base.obj'))
def body_build(gender, weight_mix, muscle_mix, height):
    """macrodetails kiểu MakeHuman: giới × tuổi 'young' (25 tuổi) × cơ × cân; chủng 'caucasian' (lính đồn trú Anh / dân Gibraltar — chỉ ảnh hưởng nhẹ hình mặt)."""
    P = [list(v) for v in V]; sx = 'male' if gender == 'm' else 'female'
    tg = []
    for wn, ww in weight_mix.items():
        for mn, mw in muscle_mix.items():
            tg.append((f'macrodetails/universal-{sx}-young-{mn}-{wn}.target.gz', ww * mw))
    tg.append((f'macrodetails/caucasian-{sx}-young.target.gz', 1.0))
    if height != 0: tg.append((f'macrodetails/height/{sx}-young-averagemuscle-averageweight-{"max" if height > 0 else "min"}height.target.gz', abs(height)))
    for rel, w in tg:
        if w <= 0: continue
        for i, dx, dy, dz in read_target(rel): P[i][0] += dx * w; P[i][1] += dy * w; P[i][2] += dz * w
    B = [Vector((x * 0.1, -z * 0.1, y * 0.1)) for x, y, z in P]
    zmin = min(B[i].z for g, f in F if g == 'body' for i in f)
    for b in B: b.z -= zmin
    return B

RIG = json.load(open(os.path.join(A.mp, 'rigs', 'standard', 'rig.default.json')))
WTS = json.load(open(os.path.join(A.mp, 'rigs', 'standard', 'weights.default.json')))['weights']
JOINT = {}
for g, f in F:
    if g and g.startswith('joint-'): JOINT.setdefault(g, set()).update(f)
def joint_pos(spec, B):
    s = spec['strategy']
    if s == 'CUBE': ids = JOINT[spec['cube_name']]; return sum((B[i] for i in ids), Vector()) / len(ids)
    if s == 'VERTEX': return B[spec['vertex_index']].copy()
    ids = spec['vertex_indices']; return sum((B[i] for i in ids), Vector()) / len(ids)

# vùng theo xương chi phối
def region_of_bone(b):
    if b.startswith(('wrist', 'finger', 'metacarpal')): return 'hand'
    if b.startswith(('foot', 'toe')): return 'foot'
    if b.startswith('lowerleg'): return 'shin'
    if b.startswith(('upperleg', 'pelvis', 'root')): return 'thigh'
    if b.startswith(('spine', 'clavicle', 'shoulder', 'breast', 'upperarm', 'lowerarm')): return 'torso_arm' if not b.startswith(('upperarm', 'lowerarm')) else 'arm'
    return 'head'
DOM = {}
for b, lst in WTS.items():
    for i, w in lst:
        if i not in DOM or w > DOM[i][1]: DOM[i] = (b, w)

# ---------------------------------------------------------------- bảng trang phục theo thời kỳ (màu tham chiếu, ghi trong báo cáo)
C = lambda *c: c
SKIN = [C(0.62, 0.43, 0.32), C(0.52, 0.36, 0.26), C(0.7, 0.5, 0.38)]
if EP == 1782:
    ROLES = {
        'linh':      dict(sex='m', coat=C(0.5, 0.05, 0.04), cuff=C(0.12, 0.16, 0.1), legs=C(0.8, 0.77, 0.68), shin=C(0.06, 0.06, 0.06), shoe=C(0.03, 0.03, 0.03), hat='tricorn', belts=C(0.88, 0.86, 0.8), tails=True, gun='musket'),
        'linh2':     dict(sex='m', coat=C(0.5, 0.05, 0.04), cuff=C(0.12, 0.16, 0.1), legs=C(0.8, 0.77, 0.68), shin=C(0.06, 0.06, 0.06), shoe=C(0.03, 0.03, 0.03), hat='tricorn', belts=C(0.88, 0.86, 0.8), tails=True, gun=None),
        'phao_binh': dict(sex='m', coat=C(0.06, 0.07, 0.16), cuff=C(0.45, 0.06, 0.05), legs=C(0.8, 0.77, 0.68), shin=C(0.06, 0.06, 0.06), shoe=C(0.03, 0.03, 0.03), hat='tricorn', belts=C(0.88, 0.86, 0.8), tails=True, gun=None),
        'dan_nam':   dict(sex='m', coat=C(0.3, 0.21, 0.13), cuff=None, legs=C(0.24, 0.2, 0.15), shin=C(0.55, 0.52, 0.46), shoe=C(0.1, 0.07, 0.05), hat='round', belts=None, tails=True, gun=None),
        'dan_nu':    dict(sex='f', coat=C(0.42, 0.36, 0.28), cuff=None, legs=C(0.2, 0.17, 0.2), shin=C(0.2, 0.17, 0.2), shoe=C(0.1, 0.07, 0.05), hat='cap_nu', belts=None, tails=False, skirt=C(0.2, 0.17, 0.2), apron=C(0.78, 0.74, 0.64), gun=None),
        'thuy_thu':  dict(sex='m', coat=C(0.1, 0.12, 0.24), cuff=None, legs=C(0.74, 0.7, 0.6), shin=C(0.74, 0.7, 0.6), shoe=C(0.05, 0.04, 0.03), hat='round', belts=None, tails=False, gun=None),
    }
else:
    ROLES = {
        'linh':      dict(sex='m', coat=C(0.33, 0.27, 0.17), cuff=None, legs=C(0.33, 0.27, 0.17), shin=C(0.42, 0.38, 0.28), shoe=C(0.04, 0.03, 0.03), hat='helmet', belts=C(0.55, 0.52, 0.4), tails=False, gun='rifle'),
        'linh2':     dict(sex='m', coat=C(0.33, 0.27, 0.17), cuff=None, legs=C(0.33, 0.27, 0.17), shin=C(0.42, 0.38, 0.28), shoe=C(0.04, 0.03, 0.03), hat='beret', belts=C(0.55, 0.52, 0.4), tails=False, gun=None),
        'thuy_thu':  dict(sex='m', coat=C(0.04, 0.05, 0.1), cuff=None, legs=C(0.04, 0.05, 0.1), shin=C(0.04, 0.05, 0.1), shoe=C(0.03, 0.03, 0.03), hat='sailor', belts=None, tails=False, gun=None, collar=C(0.15, 0.2, 0.42)),
        'thuy_thu_trang': dict(sex='m', coat=C(0.82, 0.82, 0.78), cuff=None, legs=C(0.82, 0.82, 0.78), shin=C(0.82, 0.82, 0.78), shoe=C(0.03, 0.03, 0.03), hat='sailor', belts=None, tails=False, gun=None),
        'raf':       dict(sex='m', coat=C(0.2, 0.25, 0.34), cuff=None, legs=C(0.2, 0.25, 0.34), shin=C(0.2, 0.25, 0.34), shoe=C(0.03, 0.03, 0.03), hat='sidecap', belts=None, tails=False, gun=None),
        'tho':       dict(sex='m', coat=C(0.36, 0.36, 0.34), cuff=None, legs=C(0.14, 0.16, 0.21), shin=C(0.14, 0.16, 0.21), shoe=C(0.08, 0.06, 0.04), hat='cap', belts=None, tails=False, gun=None),
    }

MATS = {}
def mat(name, col, rough=0.8, sheen=0.0):
    key = (name, tuple(round(c, 3) for c in col))
    if key in MATS: return MATS[key]
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = rough
    try: b.inputs['Sheen Weight'].default_value = sheen
    except Exception: pass
    MATS[key] = m; return m

# ---------------------------------------------------------------- dựng một người (lưới + khung xương + tư thế)
BUILD_CACHE = {}
def make_person(role, name):
    R = ROLES[role]
    key = R['sex']
    if key not in BUILD_CACHE:
        BUILD_CACHE[key] = body_build(R['sex'], {'averageweight': 1.0}, {'averagemuscle': 0.6, 'maxmuscle': 0.4} if key == 'm' else {'averagemuscle': 1.0}, 0.0)
    B = BUILD_CACHE[key]
    # khung xương
    arm = bpy.data.armatures.new(name + '_rig'); ao = bpy.data.objects.new(name + '_rig', arm); sc.collection.objects.link(ao)
    bpy.context.view_layer.objects.active = ao; bpy.ops.object.mode_set(mode='EDIT')
    eb = {}
    for bn, spec in RIG.items():
        e = arm.edit_bones.new(bn); e.head = joint_pos(spec['head'], B); e.tail = joint_pos(spec['tail'], B)
        if (e.tail - e.head).length < 1e-4: e.tail = e.head + Vector((0, 0, 0.01))
        e.roll = spec.get('roll', 0.0); eb[bn] = e
    for bn, spec in RIG.items():
        if spec.get('parent'): eb[bn].parent = eb[spec['parent']]
    bpy.ops.object.mode_set(mode='OBJECT')
    # lưới: thân (chỉ đầu, cổ, tay, bàn chân lộ ra) + vỏ tights (áo/quần) + skirt (vạt áo/váy)
    keepF = []; mats = []
    def push(f, mname, col, rough=0.8):
        keepF.append(f); m = mat(mname, col, rough)
        if m not in mats: mats.append(m)
        return mats.index(m)
    mi = []
    skin = random.Random(hash(name) & 0xffff).choice(SKIN)
    for g, f in F:
        if g == 'body':
            reg = region_of_bone(DOM[f[0]][0])
            if reg in ('head', 'hand'): mi.append(push(f, 'da', skin, 0.55))
            elif reg == 'foot': mi.append(push(f, 'giay', R['shoe'], 0.35))
        elif g == 'helper-tights':
            cs = [B[i] for i in f]; c = sum(cs, Vector()) / len(cs); reg = region_of_bone(DOM[f[0]][0])
            if reg in ('head', 'hand', 'foot'): continue
            if reg in ('torso_arm', 'arm'):
                col = R['coat']
                if R.get('belts') and EP == 1782 and reg == 'torso_arm' and c.z > 1.02:   # đai chéo trắng (hai dải chéo qua ngực/lưng)
                    if c.z > 1.06 and min(abs(c.x - (c.z - 1.24) * 0.8), abs(c.x + (c.z - 1.24) * 0.8)) < 0.026: col = R['belts']
                if R.get('belts') and EP == 1943 and reg == 'torso_arm':   # đai lưng + hai dây đeo (webbing)
                    if abs(c.z - 1.02) < 0.035 or (c.z > 1.05 and abs(abs(c.x) - 0.09) < 0.022): col = R['belts']
                if R.get('cuff') and reg == 'arm' and DOM[f[0]][0].startswith('lowerarm02'): col = R['cuff']
                if R.get('collar') and reg == 'torso_arm' and c.z > 1.33 and c.y > 0.0: col = R['collar']
                mi.append(push(f, 'ao', col))
            elif reg == 'thigh': mi.append(push(f, 'quan', R['legs'] if R['sex'] == 'm' else R['skirt']))
            elif reg == 'shin': mi.append(push(f, 'ong', R['shin'] if R['sex'] == 'm' else R['skirt']))
        elif g == 'helper-skirt' and (R.get('tails') or R['sex'] == 'f'):
            col = R['coat'] if R['sex'] == 'm' else R['skirt']
            if R['sex'] == 'm' and min(B[i].z for i in f) < 0.6: continue     # vạt áo nam dừng trên gối
            if R['sex'] == 'f' and R.get('apron'):
                cs = [B[i] for i in f]; c = sum(cs, Vector()) / len(cs)
                if c.y < -0.05 and abs(c.x) < 0.14: col = R['apron']
            mi.append(push(f, 'vat', col))
    used = sorted({i for f in keepF for i in f}); remap = {o: n for n, o in enumerate(used)}
    verts = [B[i].copy() for i in used]
    # vỏ áo/quần nở ra 6–9 mm theo pháp tuyến xấp xỉ (từ tâm trục thân) để không chạm da; vạt áo 1782 dài thêm xuống gối
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(v) for v in verts], [], [[remap[i] for i in f] for f in keepF]); me.update()
    for m in mats: me.materials.append(m)
    for p, k in zip(me.polygons, mi): p.material_index = k; p.use_smooth = True
    o = bpy.data.objects.new(name, me); sc.collection.objects.link(o); o.parent = ao
    # nhóm đỉnh + modifier khung xương
    for bn, lst in WTS.items():
        vg = None
        for i, w in lst:
            if i in remap:
                if vg is None: vg = o.vertex_groups.new(name=bn)
                vg.add([remap[i]], w, 'REPLACE')
    md = o.modifiers.new('arm', 'ARMATURE'); md.object = ao
    sub = o.modifiers.new('sub', 'SUBSURF'); sub.levels = 1; sub.render_levels = 1
    # mũ / súng (khối cơ bản, gắn xương)
    head_b = ao.data.bones['head']; htop = max(v.z for v in verts) - 0.02
    hc = Vector((0, joint_pos(RIG['head']['head'], B).y + 0.0, htop + 0.035))
    def part(kind, loc, scale, col, rot=(0, 0, 0), bone='head', rough=0.6):
        if kind == 'cyl': bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=1, depth=2, location=loc, rotation=rot)
        elif kind == 'sph': bpy.ops.mesh.primitive_uv_sphere_add(segments=18, ring_count=10, radius=1, location=loc, rotation=rot)
        elif kind == 'cone': bpy.ops.mesh.primitive_cone_add(vertices=20, radius1=1, radius2=0.6, depth=2, location=loc, rotation=rot)
        else: bpy.ops.mesh.primitive_cube_add(size=2, location=loc, rotation=rot)
        p = bpy.context.object; p.scale = scale; p.data.materials.append(mat('phu_kien', col, rough))
        for pp in p.data.polygons: pp.use_smooth = True
        bpy.context.view_layer.update(); mw = p.matrix_world.copy(); p.parent = ao; p.parent_type = 'BONE'; p.parent_bone = bone
        bpy.context.view_layer.update(); p.matrix_world = mw
        return p
    hat = R['hat']; k = (0.04, 0.04, 0.04)
    if hat == 'tricorn':   # mũ ba góc: vành dựng thành tam giác, góc nhọn ra trước
        for a in (0.0, 2.094, 4.189):
            part('cube', hc + Vector((math.sin(a) * 0.075, -math.cos(a) * 0.075, -0.015)), (0.13, 0.014, 0.035), k, rot=(0.25, 0, a))
        part('cyl', hc + Vector((0, 0, -0.005)), (0.1, 0.1, 0.04), k)
    elif hat == 'round': part('cyl', hc + Vector((0, 0, -0.03)), (0.17, 0.17, 0.008), k); part('cyl', hc + Vector((0, 0, 0.0)), (0.095, 0.095, 0.04), k)
    elif hat == 'cap_nu': part('sph', hc + Vector((0, 0.01, -0.04)), (0.115, 0.12, 0.08), C(0.86, 0.84, 0.78))
    elif hat == 'helmet':   # mũ sắt Brodie: chỏm thấp + vành rộng
        part('sph', hc + Vector((0, 0, -0.035)), (0.115, 0.125, 0.065), C(0.27, 0.27, 0.19), rough=0.7); part('cyl', hc + Vector((0, 0, -0.05)), (0.175, 0.185, 0.006), C(0.27, 0.27, 0.19), rough=0.7)
    elif hat == 'beret': part('sph', hc + Vector((0.02, 0.0, -0.025)), (0.115, 0.115, 0.04), C(0.06, 0.06, 0.07))
    elif hat == 'sailor': part('cyl', hc + Vector((0, 0, -0.02)), (0.12, 0.12, 0.03), C(0.9, 0.9, 0.88)); part('cyl', hc + Vector((0, 0, -0.045)), (0.1, 0.1, 0.015), k)
    elif hat == 'sidecap': part('cube', hc + Vector((0.01, 0, -0.03)), (0.05, 0.12, 0.035), R['coat'])
    elif hat == 'cap': part('cyl', hc + Vector((0, -0.02, -0.03)), (0.11, 0.12, 0.03), C(0.2, 0.19, 0.17)); part('cube', hc + Vector((0, -0.12, -0.05)), (0.07, 0.04, 0.006), C(0.2, 0.19, 0.17))
    if R.get('gun') == 'musket':   # súng hoả mai vác vai trái (dài ~1,5 m, có lưỡi lê)
        sh = joint_pos(RIG['shoulder01.L']['head'], B)
        part('cyl', sh + Vector((0.02, 0.12, 0.05)), (0.016, 0.016, 0.6), C(0.22, 0.13, 0.07), rot=(0.62, 0, 0), bone='spine03', rough=0.5)
    elif R.get('gun') == 'rifle':  # súng trường đeo vai phải, nòng chúc lên
        sh = joint_pos(RIG['shoulder01.R']['head'], B)
        part('cyl', sh + Vector((-0.02, 0.1, -0.15)), (0.014, 0.014, 0.55), C(0.2, 0.13, 0.08), rot=(0.12, 0, 0), bone='spine03', rough=0.5)
    return ao, o

def rot_about_head(ao, bn, axis, deg):
    pb = ao.pose.bones[bn]; h = pb.head.copy()
    M = Matrix.Translation(h) @ Matrix.Rotation(math.radians(deg), 4, axis) @ Matrix.Translation(-h)
    pb.matrix = M @ pb.matrix; bpy.context.view_layer.update()

def pose(ao, walk_phase, sex):
    """walk_phase None = đứng; 0..7 = pha chu kỳ đi (8 khung). Hướng trước của lưới gốc = −Y; quay quanh +X dương = đưa ra sau."""
    for pb in ao.pose.bones: pb.matrix_basis = Matrix()
    bpy.context.view_layer.update()
    # tay từ tư thế A (≈ 42°) xuống sát thân: chọn chiều quay làm bàn tay hạ thấp
    for s in ('L', 'R'):
        bn = f'upperarm01.{s}'; best = None
        for sg in (1, -1):
            rot_about_head(ao, bn, 'Y', 44 * sg); z = ao.pose.bones[f'wrist.{s}'].head.z
            if best is None or z < best[0]: best = (z, sg)
            rot_about_head(ao, bn, 'Y', -44 * sg)
        rot_about_head(ao, bn, 'Y', 44 * best[1])
    if walk_phase is None:
        for s in ('L', 'R'): rot_about_head(ao, f'lowerarm01.{s}', 'X', -8)
        return
    ph = 2 * math.pi * walk_phase / 8; amp = 24 if sex == 'm' else 20
    root = ao.pose.bones['root']; root.location = (0, 0, 0)
    for s, off in (('L', 0.0), ('R', math.pi)):
        p = ph + off
        hip = amp * math.sin(p)                                   # + = chân ra trước
        knee = 6 + 52 * max(0.0, math.cos(p)) ** 2                # gấp gối khi chân lướt lên
        rot_about_head(ao, f'upperleg01.{s}', 'X', -hip)
        rot_about_head(ao, f'lowerleg01.{s}', 'X', knee)
        rot_about_head(ao, f'foot.{s}', 'X', -(knee - hip) * 0.45 - 4)
        arm = -0.75 * amp * math.sin(p)                          # tay đánh ngược chân cùng bên
        rot_about_head(ao, f'upperarm01.{s}', 'X', -arm * 0.9)
        rot_about_head(ao, f'lowerarm01.{s}', 'X', -12 - 10 * max(0.0, math.sin(p + math.pi)))
    rot_about_head(ao, 'spine03', 'Z', 4 * math.sin(ph))
    # nhún thân: hạ gốc để bàn chân thấp nhất chạm đất
    bpy.context.view_layer.update()
    zf = min(ao.pose.bones['foot.L'].head.z, ao.pose.bones['foot.R'].head.z)
    return zf

# ---------------------------------------------------------------- tờ sprite: hàng = 8 hướng, cột = đứng + 8 pha đi
NA, NP = 8, 9; CELLX, ROWD = 1.7, 16.0; PITCH = math.radians(-8.0)   # không mặt bắt bóng: bóng dựng 2D theo mặt trời + lượt nắng của cảnh A
head = math.radians(A.head); fwd = Vector((math.sin(head), math.cos(head), 0)); right = Vector((math.cos(head), -math.sin(head), 0))
roles = A.roles.split(','); meta = {'epoch': EP, 'head': A.head, 'pxm': A.pxm, 'na': NA, 'np': NP, 'cellx': CELLX, 'rowd': ROWD, 'pitch_deg': -8.0, 'roles': {}}
for role in roles:
    if role not in ROLES: continue
    for o in list(sc.objects): bpy.data.objects.remove(o, do_unlink=True)
    rng = random.Random(EP * 100 + roles.index(role)); cells = []
    ankle0 = None
    for ai in range(NA):
        for pi in range(NP):
            if A.test and not (ai in (0, 2) and pi in (0, 1, 3)): continue
            ao, o = make_person(role, f'{role}_{ai}_{pi}')
            pose(ao, None if pi == 0 else pi - 1, ROLES[role]['sex'])
            # hướng mặt: k·45° ngược chiều kim đồng hồ từ "nhìn về máy"; lưới gốc nhìn −Y
            d = (-fwd); a = math.radians(45 * ai); d = Vector((d.x * math.cos(a) - d.y * math.sin(a), d.x * math.sin(a) + d.y * math.cos(a), 0))
            yaw = math.atan2(d.y, d.x) - math.atan2(-1, 0)
            u = (pi - (NP - 1) / 2) * CELLX; v = ai * ROWD
            pos = right * u + fwd * v
            bpy.context.view_layer.update()
            # bàn chân thấp nhất chạm đất (đỉnh lưới đã biến dạng)
            dg = bpy.context.evaluated_depsgraph_get(); me_ = o.evaluated_get(dg).to_mesh(); zmin = min(v_.co.z for v_ in me_.vertices); o.evaluated_get(dg).to_mesh_clear()
            ao.location = (pos.x, pos.y, -zmin); ao.rotation_euler = (0, 0, yaw)
            o.pass_index = 1
            for ch in ao.children: ch.pass_index = 1
            cells.append({'a': ai, 'p': pi, 'world': [pos.x, pos.y], 'dir': [d.x, d.y]})
    bpy.context.view_layer.update()
    cam = bpy.data.cameras.new('c'); cam.type = 'ORTHO'
    Wm = NP * CELLX; Hm = (NA - 1) * ROWD * math.sin(abs(PITCH)) + 2.7
    W, H = int(Wm * A.pxm), int(Hm * A.pxm); cam.ortho_scale = max(Wm, Hm)
    co = bpy.data.objects.new('c', cam); sc.collection.objects.link(co); sc.camera = co
    cv = (NA - 1) * ROWD / 2; mid = fwd * cv
    D = 200.0
    co.location = (mid.x - fwd.x * D * math.cos(PITCH), mid.y - fwd.y * D * math.cos(PITCH), 0.95 + D * math.sin(-PITCH))
    co.rotation_euler = (math.radians(90) + PITCH, 0, -head)
    sc.render.resolution_x, sc.render.resolution_y = W, H; sc.render.resolution_percentage = 100
    from bpy_extras.object_utils import world_to_camera_view
    bpy.context.view_layer.update()   # ma trận máy phải cập nhật trước khi chiếu toạ độ chân
    for c in cells:
        p = world_to_camera_view(sc, co, Vector((c['world'][0], c['world'][1], 0))); c['foot_px'] = [round(p.x * W, 1), round((1 - p.y) * H, 1)]
    if A.test:   # thử nhanh: chỉ dựng khung bao các ô đã đặt
        xs = [c['foot_px'][0] for c in cells]; ys = [c['foot_px'][1] for c in cells]
        sc.render.use_border = True; sc.render.use_crop_to_border = True
        sc.render.border_min_x = max(0, (min(xs) - 2.6 * A.pxm) / W); sc.render.border_max_x = min(1, (max(xs) + 2.6 * A.pxm) / W)
        sc.render.border_min_y = max(0, 1 - (max(ys) + 2.0 * A.pxm) / H); sc.render.border_max_y = min(1, 1 - (min(ys) - 2.3 * A.pxm) / H)
    sc.render.film_transparent = True
    sun = bpy.data.objects.new('sun', bpy.data.lights.new('sun', 'SUN')); sc.collection.objects.link(sun)
    world = bpy.data.worlds.new('w'); sc.world = world; world.use_nodes = True; bgn = world.node_tree.nodes['Background']
    LAT = math.radians(36.14); DECL = math.radians(4.0)
    def sun_at(hour):
        Hh = math.radians((hour - 12) * 15)
        alt = math.asin(math.sin(LAT) * math.sin(DECL) + math.cos(LAT) * math.cos(DECL) * math.cos(Hh))
        az = math.atan2(math.sin(Hh), math.cos(Hh) * math.sin(LAT) - math.tan(DECL) * math.cos(LAT)) + math.pi
        return math.degrees(alt), math.degrees(az) % 360
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = A.spp; sc.cycles.use_denoising = True; sc.render.use_persistent_data = True
    sc.view_settings.view_transform = 'AgX'
    sc.view_layers[0].use_pass_object_index = True
    try: sc.render.image_settings.media_type = 'MULTI_LAYER_IMAGE'   # Blender 5: EXR nhiều lớp (Combined + IndexOB)
    except Exception: sc.render.image_settings.file_format = 'OPEN_EXR_MULTILAYER'
    sc.render.image_settings.color_depth = '16'
    rmeta = {'W': W, 'H': H, 'cells': cells, 'passes': {}, 'render_s': {}}
    for p in A.passes.split(','):
        hr = PASSES[p]
        if hr is None:
            alt, az = 38.0, 235.0; sun.data.energy = 0.08; sun.data.color = (0.62, 0.72, 1.0); bgn.inputs[0].default_value = (0.004, 0.006, 0.012, 1); bgn.inputs[1].default_value = 1.0
        else:
            alt, az = sun_at(hr); warm = max(0.0, min(1.0, (20 - alt) / 20))
            sun.data.energy = 4.2 if alt > 12 else 2.0 + 2.2 * max(0, alt) / 12; sun.data.color = (1.0, 1.0 - 0.4 * warm, 1.0 - 0.7 * warm)
            bgn.inputs[0].default_value = (0.45, 0.55, 0.75, 1) if alt > 12 else (0.35, 0.33, 0.4, 1); bgn.inputs[1].default_value = 0.35
        sun.rotation_euler = (math.radians(90 - alt), 0, math.radians(-az + 180)); sun.data.angle = math.radians(1.5)
        t = time.time(); sc.render.filepath = os.path.join(A.out, f'{role}_{p}.exr'); bpy.ops.render.render(write_still=True)
        rmeta['passes'][p] = {'sun_alt': round(alt, 2), 'sun_az': round(az, 2)}; rmeta['render_s'][p] = round(time.time() - t, 1)
        print('SPRITE', role, p, W, H, rmeta['render_s'][p], flush=True)
    meta['roles'][role] = rmeta
json.dump(meta, open(os.path.join(A.out, f'sprites-{"-".join(roles)}.json'), 'w'), indent=1, ensure_ascii=False)
print('DONE', round(time.time() - T0, 1))
