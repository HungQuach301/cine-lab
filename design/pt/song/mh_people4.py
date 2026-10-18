"""PT4 · tờ sprite NGƯỜI "có sự sống" — lưới gốc MakeHuman/MPFB2 (CC0: base.obj + targets macrodetails + rig/weights 'default'),
nạp bằng mã TỰ VIẾT (chỉ đọc dữ liệu, KHÔNG chạy mã addon MPFB) — kế thừa design/pt/lai/mh_people.py (PT2), thêm:
- 2 DÁNG THÂN mỗi vai (b0 trung bình · b1 gầy cao / chắc thấp), da, tóc, có/không mũ theo vai;
- MẶT/TÓC/BÀN TAY tầm xa: nhãn cầu tối + lòng trắng, lông mày, môi, tóc (lớp vỏ 'helper-hair' của lưới gốc), da bán trong (SSS nhẹ), vải có nếp (bump nhiễu);
- TƯ THẾ: đi 8 pha · đứng thả lỏng (dồn trọng tâm) · nói (tay ra hiệu, quay đầu) · nhìn quanh (quay đầu + vai) · chắp tay sau lưng ·
  việc theo vai (chữa tường có dụng cụ, gác súng dựng, ôm thùng, vác bao, giỏ) · đi tay mang vật (8 pha);
- CẶP KHIÊNG: hai người cùng khiêng một thùng/hòm (một sprite, đi 8 pha).
Máy trực giao cùng hướng + cúi 8° như máy neo; mặt trời y hệt lượt nền; bóng đổ dựng khi ghép (live4.py).
  /opt/bpy/bin/python design/pt/song/mh_people4.py -- --epoch 1782|1943 --head <độ> --roles a,b --out DIR [--pxm 130] [--spp 12] [--test]
Trang phục như PT2 (TIEN-KY T3/claims): 1782 bộ binh áo đỏ đai chéo trắng mũ ba góc, pháo binh áo lam đậm; 1943 battledress kaki, hải quân, RAF;
1943 KHÔNG phụ nữ/trẻ em (S114)."""
import bpy, math, sys, os, json, gzip, argparse, random, time
from mathutils import Vector, Matrix
ap = argparse.ArgumentParser(); ap.add_argument('--epoch', type=int, required=True); ap.add_argument('--head', type=float, required=True)
ap.add_argument('--roles', required=True); ap.add_argument('--passes', default='d1,d2,d4'); ap.add_argument('--out', required=True)   # lượt: d3 → dùng d4, n → d2 tối + lam (live4.py)
ap.add_argument('--pxm', type=int, default=110); ap.add_argument('--spp', type=int, default=8); ap.add_argument('--mp', default='/var/tmp/pt4/mpfb2/src/mpfb/data')
ap.add_argument('--test', action='store_true')
A = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]); os.makedirs(A.out, exist_ok=True)
HERE = os.path.dirname(os.path.abspath(__file__)); EP = A.epoch; T0 = time.time()
PASSES = json.load(open(os.path.join(HERE, '..', 'scene', 'passes.json')))
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene

# ---------------------------------------------------------------- lưới gốc + targets (OBJ: y lên, dm) → Blender (x, −z, y) × 0,1
def read_obj(p):
    V, F = [], []; g = None
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
def body_build(sex, weight_mix, muscle_mix, height):
    P = [list(v) for v in V]; sx = 'male' if sex == 'm' else 'female'; tg = []
    for wn, ww in weight_mix.items():
        for mn, mw in muscle_mix.items(): tg.append((f'macrodetails/universal-{sx}-young-{mn}-{wn}.target.gz', ww * mw))
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
GROUP_V = {}
for g, f in F: GROUP_V.setdefault(g, set()).update(f)

# ---------------------------------------------------------------- vai, dáng thân, việc (màu tham chiếu như PT2)
C = lambda *c: c
SKIN = [C(0.6, 0.42, 0.31), C(0.5, 0.35, 0.25), C(0.68, 0.49, 0.37), C(0.44, 0.3, 0.21)]
HAIR = [C(0.05, 0.035, 0.025), C(0.12, 0.08, 0.05), C(0.02, 0.02, 0.02), C(0.28, 0.2, 0.12), C(0.35, 0.33, 0.3)]
if EP == 1782:
    ROLES = {
        'linh':      dict(sex='m', coat=C(0.5, 0.05, 0.04), cuff=C(0.12, 0.16, 0.1), legs=C(0.8, 0.77, 0.68), shin=C(0.06, 0.06, 0.06), shoe=C(0.03, 0.03, 0.03), hat='tricorn', belts=C(0.88, 0.86, 0.8), tails=True, gun='musket', work='order', carry=None),
        'linh2':     dict(sex='m', coat=C(0.5, 0.05, 0.04), cuff=C(0.12, 0.16, 0.1), legs=C(0.8, 0.77, 0.68), shin=C(0.06, 0.06, 0.06), shoe=C(0.03, 0.03, 0.03), hat='tricorn', belts=C(0.88, 0.86, 0.8), tails=True, gun=None, work='tool', carry='box'),
        'phao_binh': dict(sex='m', coat=C(0.06, 0.07, 0.16), cuff=C(0.45, 0.06, 0.05), legs=C(0.8, 0.77, 0.68), shin=C(0.06, 0.06, 0.06), shoe=C(0.03, 0.03, 0.03), hat='tricorn', belts=C(0.88, 0.86, 0.8), tails=True, gun=None, work='tool', carry='box'),
        'dan_nam':   dict(sex='m', coat=C(0.3, 0.21, 0.13), cuff=None, legs=C(0.24, 0.2, 0.15), shin=C(0.55, 0.52, 0.46), shoe=C(0.1, 0.07, 0.05), hat='round', belts=None, tails=True, gun=None, work='sack', carry='sack', nohat_b1=True),
        'dan_nu':    dict(sex='f', coat=C(0.42, 0.36, 0.28), cuff=None, legs=C(0.2, 0.17, 0.2), shin=C(0.2, 0.17, 0.2), shoe=C(0.1, 0.07, 0.05), hat='cap_nu', belts=None, tails=False, skirt=C(0.2, 0.17, 0.2), apron=C(0.78, 0.74, 0.64), gun=None, work='basket', carry='basket'),
        'thuy_thu':  dict(sex='m', coat=C(0.1, 0.12, 0.24), cuff=None, legs=C(0.74, 0.7, 0.6), shin=C(0.74, 0.7, 0.6), shoe=C(0.05, 0.04, 0.03), hat='round', belts=None, tails=False, gun=None, work='sack', carry='sack', nohat_b1=True),
        'khieng':    dict(pair='linh2', item='barrel'),
    }
else:
    ROLES = {
        'linh':      dict(sex='m', coat=C(0.33, 0.27, 0.17), cuff=None, legs=C(0.33, 0.27, 0.17), shin=C(0.42, 0.38, 0.28), shoe=C(0.04, 0.03, 0.03), hat='helmet', belts=C(0.55, 0.52, 0.4), tails=False, gun='rifle', work='order', carry=None),
        'linh2':     dict(sex='m', coat=C(0.33, 0.27, 0.17), cuff=None, legs=C(0.33, 0.27, 0.17), shin=C(0.42, 0.38, 0.28), shoe=C(0.04, 0.03, 0.03), hat='beret', belts=C(0.55, 0.52, 0.4), tails=False, gun=None, work='back', carry='box'),
        'thuy_thu':  dict(sex='m', coat=C(0.04, 0.05, 0.1), cuff=None, legs=C(0.04, 0.05, 0.1), shin=C(0.04, 0.05, 0.1), shoe=C(0.03, 0.03, 0.03), hat='sailor', belts=None, tails=False, gun=None, collar=C(0.15, 0.2, 0.42), work='sack', carry='sack'),
        'thuy_thu_trang': dict(sex='m', coat=C(0.82, 0.82, 0.78), cuff=None, legs=C(0.82, 0.82, 0.78), shin=C(0.82, 0.82, 0.78), shoe=C(0.03, 0.03, 0.03), hat='sailor', belts=None, tails=False, gun=None, work='back', carry='sack'),
        'raf':       dict(sex='m', coat=C(0.2, 0.25, 0.34), cuff=None, legs=C(0.2, 0.25, 0.34), shin=C(0.2, 0.25, 0.34), shoe=C(0.03, 0.03, 0.03), hat='sidecap', belts=None, tails=False, gun=None, work='back', carry=None),
        'tho':       dict(sex='m', coat=C(0.36, 0.36, 0.34), cuff=None, legs=C(0.14, 0.16, 0.21), shin=C(0.14, 0.16, 0.21), shoe=C(0.08, 0.06, 0.04), hat='cap', belts=None, tails=False, gun=None, work='tool', carry='box', nohat_b1=True),
        'khieng':    dict(pair='tho', item='crate'),
    }
# dáng thân: b0 trung bình; b1 nam gầy cao hoặc chắc thấp (luân phiên theo vai), nữ đầy đặn hơn
def builds(role, R):
    if R['sex'] == 'm':
        alt = list(ROLES).index(role) % 2
        return [dict(w={'averageweight': 1.0}, mu={'averagemuscle': 0.6, 'maxmuscle': 0.4}, h=0.0),
                dict(w={'minweight': 0.55, 'averageweight': 0.45}, mu={'averagemuscle': 1.0}, h=0.45) if alt == 0 else
                dict(w={'maxweight': 0.45, 'averageweight': 0.55}, mu={'averagemuscle': 0.5, 'maxmuscle': 0.5}, h=-0.4)]
    return [dict(w={'averageweight': 1.0}, mu={'averagemuscle': 1.0}, h=0.0), dict(w={'maxweight': 0.4, 'averageweight': 0.6}, mu={'averagemuscle': 1.0}, h=-0.3)]

MATS = {}
def mat(name, col, rough=0.8, kind='plain'):
    key = (name, kind, tuple(round(c, 3) for c in col))
    if key in MATS: return MATS[key]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; N = nt.nodes; L = nt.links; b = N['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = rough
    if kind in ('cloth', 'hair', 'skin'):   # nếp vải / sợi tóc / lỗ chân lông: bump nhiễu thủ tục (toạ độ vật)
        tc = N.new('ShaderNodeTexCoord'); nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = {'cloth': 9.0, 'hair': 60.0, 'skin': 120.0}[kind]
        nz.inputs['Detail'].default_value = 4.0; L.new(tc.outputs['Object'], nz.inputs['Vector'])
        if kind == 'hair':
            mp = N.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1, 1, 6); L.new(tc.outputs['Object'], mp.inputs[0]); L.new(mp.outputs[0], nz.inputs['Vector'])
        bp = N.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = {'cloth': 0.35, 'hair': 0.6, 'skin': 0.08}[kind]; L.new(nz.outputs['Fac'], bp.inputs['Height']); L.new(bp.outputs['Normal'], b.inputs['Normal'])
        if kind == 'cloth':   # vải nhuộm thời kỳ: loang màu nhẹ (không đều như nhựa)
            mr = N.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value = 0.82; mr.inputs['To Max'].default_value = 1.08; L.new(nz.outputs['Fac'], mr.inputs['Value'])
            mx = N.new('ShaderNodeVectorMath'); mx.operation = 'SCALE'; mx.inputs[0].default_value = col; L.new(mr.outputs[0], mx.inputs['Scale']); L.new(mx.outputs[0], b.inputs['Base Color'])
        if kind == 'skin':
            pass   # (SSS thử ở lượt đầu: chậm ×3 khi dựng, không thấy được ở ≥ 10 m → bỏ)
        if kind == 'hair':
            try: b.inputs['Sheen Weight'].default_value = 0.3
            except Exception: pass
    MATS[key] = m; return m

# ---------------------------------------------------------------- dựng MỘT người mẫu (lưới + khung xương + mũ), sau đó sao chép cho mọi ô
BUILD_CACHE = {}
def make_person(role, bi, name):
    R = ROLES[role]; bd = builds(role, R)[bi]; key = (R['sex'], bi, list(ROLES).index(role) % 2)
    if key not in BUILD_CACHE: BUILD_CACHE[key] = body_build(R['sex'], bd['w'], bd['mu'], bd['h'])
    B = BUILD_CACHE[key]; rr = random.Random(hash((role, bi, EP)) & 0xffff)
    arm = bpy.data.armatures.new(name + '_rig'); ao = bpy.data.objects.new(name + '_rig', arm); sc.collection.objects.link(ao)
    bpy.context.view_layer.objects.active = ao; bpy.ops.object.mode_set(mode='EDIT'); eb = {}
    for bn, spec in RIG.items():
        e = arm.edit_bones.new(bn); e.head = joint_pos(spec['head'], B); e.tail = joint_pos(spec['tail'], B)
        if (e.tail - e.head).length < 1e-4: e.tail = e.head + Vector((0, 0, 0.01))
        e.roll = spec.get('roll', 0.0); eb[bn] = e
    for bn, spec in RIG.items():
        if spec.get('parent'): eb[bn].parent = eb[spec['parent']]
    bpy.ops.object.mode_set(mode='OBJECT')
    skin = SKIN[(list(ROLES).index(role) * 2 + bi) % len(SKIN)]; hair = HAIR[(list(ROLES).index(role) + 3 * bi) % len(HAIR)]
    if EP == 1782 and R.get('belts') and bi == 0: hair = C(0.55, 0.52, 0.48)   # tóc rắc bột (bộ binh thế kỷ 18) — một dáng
    # mắt, lông mày, môi: vị trí từ nhãn cầu + răng của lưới gốc
    eyeL = sum((B[i] for i in GROUP_V['helper-l-eye']), Vector()) / len(GROUP_V['helper-l-eye']); eyeR = sum((B[i] for i in GROUP_V['helper-r-eye']), Vector()) / len(GROUP_V['helper-r-eye'])
    teeth = sum((B[i] for i in GROUP_V['helper-upper-teeth']), Vector()) / len(GROUP_V['helper-upper-teeth'])
    def face_mark(c):
        for e in (eyeL, eyeR):   # lông mày: dải cong ngay trên hốc mắt, mặt trước
            dx, dz = c.x - e.x, c.z - e.z
            if 0.012 < dz - 0.25 * (dx / 0.02) ** 2 * 0.004 < 0.024 and abs(dx) < 0.028 and c.y < e.y + 0.004: return 'brow'
        dx, dz = c.x - teeth.x, c.z - teeth.z
        if abs(dx) < 0.024 and -0.016 < dz < 0.004 and c.y < teeth.y - 0.004: return 'lip'
        return None
    hatless = bi == 1 and R.get('nohat_b1')
    keepF = []; mats = []; mi = []
    def push(f, m):
        keepF.append(f)
        if m not in mats: mats.append(m)
        mi.append(mats.index(m))
    for g, f in F:
        if g == 'body':
            reg = region_of_bone(DOM[f[0]][0])
            if reg in ('head', 'hand'):
                c = sum((B[i] for i in f), Vector()) / len(f); fm = face_mark(c) if reg == 'head' else None
                if fm == 'brow': push(f, mat('may', tuple(x * 1.0 for x in hair), 0.7, 'hair'))
                elif fm == 'lip': push(f, mat('moi', (skin[0] * 0.85, skin[1] * 0.6, skin[2] * 0.58), 0.45, 'skin'))
                else: push(f, mat('da', skin, 0.5, 'skin'))
            elif reg == 'foot': push(f, mat('giay', R['shoe'], 0.35))
        elif g in ('helper-l-eye', 'helper-r-eye'):
            c = sum((B[i] for i in f), Vector()) / len(f); e = eyeL if g == 'helper-l-eye' else eyeR
            front = (e.y - c.y) > 0.008                        # nửa trước nhãn cầu: tròng đen; quanh: lòng trắng
            push(f, mat('trong_mat' if front else 'long_trang', C(0.03, 0.025, 0.02) if front else C(0.62, 0.58, 0.54), 0.15))
        elif g == 'helper-hair':   # vỏ tóc của lưới gốc dài tới vai → chỉ giữ phần sọ: trên tai và không phủ mặt (tóc ngắn / tóc buộc gọn)
            c = sum((B[i] for i in f), Vector()) / len(f); ez = (eyeL.z + eyeR.z) / 2; ey = (eyeL.y + eyeR.y) / 2
            if c.z > ez + 0.025 or (c.z > ez - 0.05 and c.y > ey + 0.07): push(f, mat('toc', hair, 0.55, 'hair'))
        elif g == 'helper-tights':
            cs = [B[i] for i in f]; c = sum(cs, Vector()) / len(cs); reg = region_of_bone(DOM[f[0]][0])
            if reg in ('head', 'hand', 'foot'): continue
            if reg in ('torso_arm', 'arm'):
                col = R['coat']
                if R.get('belts') and EP == 1782 and reg == 'torso_arm' and c.z > 1.02:
                    if c.z > 1.06 and min(abs(c.x - (c.z - 1.24) * 0.8), abs(c.x + (c.z - 1.24) * 0.8)) < 0.026: col = R['belts']
                if R.get('belts') and EP == 1943 and reg == 'torso_arm':
                    if abs(c.z - 1.02) < 0.035 or (c.z > 1.05 and abs(abs(c.x) - 0.09) < 0.022): col = R['belts']
                if R.get('cuff') and reg == 'arm' and DOM[f[0]][0].startswith('lowerarm02'): col = R['cuff']
                if R.get('collar') and reg == 'torso_arm' and c.z > 1.33 and c.y > 0.0: col = R['collar']
                if bi == 1 and col == R['coat']: col = tuple(min(1, x * 1.07) for x in col)    # áo dáng 2 bạc màu hơn
                push(f, mat('ao', col, 0.85, 'cloth'))
            elif reg == 'thigh': push(f, mat('quan', R['legs'] if R['sex'] == 'm' else R['skirt'], 0.85, 'cloth'))
            elif reg == 'shin': push(f, mat('ong', R['shin'] if R['sex'] == 'm' else R['skirt'], 0.85, 'cloth'))
        elif g == 'helper-skirt' and (R.get('tails') or R['sex'] == 'f'):
            col = R['coat'] if R['sex'] == 'm' else R['skirt']
            if R['sex'] == 'm' and min(B[i].z for i in f) < 0.6: continue
            if R['sex'] == 'f' and R.get('apron'):
                cs = [B[i] for i in f]; c = sum(cs, Vector()) / len(cs)
                if c.y < -0.05 and abs(c.x) < 0.14: col = R['apron']
            push(f, mat('vat', col, 0.85, 'cloth'))
    used = sorted({i for f in keepF for i in f}); remap = {o: n for n, o in enumerate(used)}
    verts = [B[i].copy() for i in used]
    # tóc: vỏ helper-hair nở 4 mm ra ngoài theo hướng từ tâm đầu (không xuyên da)
    hcen = (eyeL + eyeR) / 2 + Vector((0, 0.06, 0.02))
    for o_, n_ in remap.items():
        if o_ in GROUP_V['helper-hair']: v = verts[n_]; d = (v - hcen).normalized(); verts[n_] = v + d * 0.004
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(v) for v in verts], [], [[remap[i] for i in f] for f in keepF]); me.update()
    for m in mats: me.materials.append(m)
    for p, k in zip(me.polygons, mi): p.material_index = k; p.use_smooth = True
    o = bpy.data.objects.new(name, me); sc.collection.objects.link(o); o.parent = ao
    for bn, lst in WTS.items():
        vg = None
        for i, w in lst:
            if i in remap:
                if vg is None: vg = o.vertex_groups.new(name=bn)
                vg.add([remap[i]], w, 'REPLACE')
    md = o.modifiers.new('arm', 'ARMATURE'); md.object = ao
    # (không SUBSURF: 168 người/tờ × chia lưới làm tràn RAM 15 GB; ở 110 px/m lưới gốc đủ mịn)
    parts = []
    htop = max(v.z for v in verts) - 0.02; hc = Vector((0, joint_pos(RIG['head']['head'], B).y, htop + 0.035)); k = (0.04, 0.04, 0.04)
    def part(kind, loc, scale, col, rot=(0, 0, 0), bone='head', rough=0.6):
        p = prim(kind, loc, scale, col, rot, rough); bpy.context.view_layer.update(); mw = p.matrix_world.copy()
        p.parent = ao; p.parent_type = 'BONE'; p.parent_bone = bone; bpy.context.view_layer.update(); p.matrix_world = mw; parts.append(p); return p
    hat = None if hatless else R['hat']
    if hat == 'tricorn':
        for a in (0.0, 2.094, 4.189): part('cube', hc + Vector((math.sin(a) * 0.075, -math.cos(a) * 0.075, -0.015)), (0.13, 0.014, 0.035), k, rot=(0.25, 0, a))
        part('cyl', hc + Vector((0, 0, -0.005)), (0.1, 0.1, 0.04), k)
    elif hat == 'round': part('cyl', hc + Vector((0, 0, -0.03)), (0.17, 0.17, 0.008), k); part('cyl', hc + Vector((0, 0, 0.0)), (0.095, 0.095, 0.04), k)
    elif hat == 'cap_nu': part('sph', hc + Vector((0, 0.01, -0.04)), (0.115, 0.12, 0.08), C(0.86, 0.84, 0.78))
    elif hat == 'helmet':
        part('sph', hc + Vector((0, 0, -0.035)), (0.115, 0.125, 0.065), C(0.27, 0.27, 0.19), rough=0.7); part('cyl', hc + Vector((0, 0, -0.05)), (0.175, 0.185, 0.006), C(0.27, 0.27, 0.19), rough=0.7)
    elif hat == 'beret': part('sph', hc + Vector((0.02, 0.0, -0.025)), (0.115, 0.115, 0.04), C(0.06, 0.06, 0.07))
    elif hat == 'sailor': part('cyl', hc + Vector((0, 0, -0.02)), (0.12, 0.12, 0.03), C(0.9, 0.9, 0.88)); part('cyl', hc + Vector((0, 0, -0.045)), (0.1, 0.1, 0.015), k)
    elif hat == 'sidecap': part('cube', hc + Vector((0.01, 0, -0.03)), (0.05, 0.12, 0.035), R['coat'])
    elif hat == 'cap': part('cyl', hc + Vector((0, -0.02, -0.03)), (0.11, 0.12, 0.03), C(0.2, 0.19, 0.17)); part('cube', hc + Vector((0, -0.12, -0.05)), (0.07, 0.04, 0.006), C(0.2, 0.19, 0.17))
    return ao, o, parts

def prim(kind, loc, scale, col, rot=(0, 0, 0), rough=0.6, mkind='plain'):
    if kind == 'cyl': bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=1, depth=2, location=loc, rotation=rot)
    elif kind == 'sph': bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=9, radius=1, location=loc, rotation=rot)
    else: bpy.ops.mesh.primitive_cube_add(size=2, location=loc, rotation=rot)
    p = bpy.context.object; p.scale = scale; p.data.materials.append(mat('vat_' + kind, col, rough, mkind))
    for pp in p.data.polygons: pp.use_smooth = kind != 'cube'
    return p

def clone(ao, o, parts, name):
    """bản sao dùng chung lưới + dữ liệu xương (chỉ tư thế riêng) — nhanh hơn dựng lại từng người."""
    a2 = ao.copy(); a2.name = name + '_rig'; sc.collection.objects.link(a2); a2.hide_render = False
    o2 = o.copy(); o2.name = name; sc.collection.objects.link(o2); o2.parent = a2; o2.modifiers['arm'].object = a2; o2.hide_render = False
    for p in parts:
        p2 = p.copy(); sc.collection.objects.link(p2); p2.parent = a2; p2.parent_type = 'BONE'; p2.parent_bone = p.parent_bone; p2.matrix_parent_inverse = p.matrix_parent_inverse.copy(); p2.hide_render = False
    return a2, o2

# ---------------------------------------------------------------- tư thế (xoay quanh đầu xương, trục thế giới; lưới nhìn −Y, +X = tay TRÁI)
def rot(ao, bn, axis, deg):
    pb = ao.pose.bones[bn]; h = pb.head.copy()
    pb.matrix = Matrix.Translation(h) @ Matrix.Rotation(math.radians(deg), 4, axis) @ Matrix.Translation(-h) @ pb.matrix; bpy.context.view_layer.update()
def arms_down(ao):
    for pb in ao.pose.bones: pb.matrix_basis = Matrix()
    bpy.context.view_layer.update()
    for s in ('L', 'R'):
        bn = f'upperarm01.{s}'; best = None
        for sg in (1, -1):
            rot(ao, bn, 'Y', 44 * sg); z = ao.pose.bones[f'wrist.{s}'].head.z
            if best is None or z < best[0]: best = (z, sg)
            rot(ao, bn, 'Y', -44 * sg)
        rot(ao, bn, 'Y', 44 * best[1])
def head_turn(ao, deg, tilt=0.0):
    for bn, k in (('neck01', 0.3), ('neck02', 0.3), ('head', 0.4)): rot(ao, bn, 'Z', deg * k)
    if tilt: rot(ao, 'head', 'X', tilt)
def legs_walk(ao, ph, amp):
    for s, off in (('L', 0.0), ('R', math.pi)):
        p = ph + off; hip = amp * math.sin(p); knee = 6 + 52 * max(0.0, math.cos(p)) ** 2
        rot(ao, f'upperleg01.{s}', 'X', -hip); rot(ao, f'lowerleg01.{s}', 'X', knee); rot(ao, f'foot.{s}', 'X', -(knee - hip) * 0.45 - 4)
def arms_hold(ao, kind):
    """tay mang vật: box = hai tay ôm trước bụng; sack = tay phải giữ bao trên vai; basket = tay trái đỡ giỏ bên hông; barrow = hai tay buông nắm càng."""
    if kind == 'box':
        for s in ('L', 'R'): rot(ao, f'upperarm01.{s}', 'X', -28); rot(ao, f'lowerarm01.{s}', 'X', -62)
    elif kind == 'sack':
        rot(ao, 'upperarm01.R', 'X', -95); rot(ao, 'upperarm01.R', 'Y', 25); rot(ao, 'lowerarm01.R', 'X', 120)
    elif kind == 'basket':
        rot(ao, 'upperarm01.L', 'X', -12); rot(ao, 'lowerarm01.L', 'X', -85)
    elif kind == 'barrow':
        for s in ('L', 'R'): rot(ao, f'upperarm01.{s}', 'X', -8); rot(ao, f'lowerarm01.{s}', 'X', -22)
def pose(ao, name, sex, rr):
    """name: st · w0..w7 · talk · look · back · work_<kind> · c<kind>0..7 (đi tay mang vật)."""
    arms_down(ao); amp = 24 if sex == 'm' else 20
    if name == 'st':   # đứng thả lỏng: dồn trọng tâm một chân, khuỷu hơi cong
        rot(ao, 'lowerleg01.L', 'X', 9); rot(ao, 'upperleg01.L', 'X', -4); rot(ao, 'spine01', 'Y', 2.5); rot(ao, 'spine03', 'Y', -2)
        for s in ('L', 'R'): rot(ao, f'lowerarm01.{s}', 'X', -10)
        head_turn(ao, rr.uniform(-12, 12))
    elif name == 'talk':   # nói chuyện: tay phải ra hiệu, quay đầu
        rot(ao, 'upperarm01.R', 'X', -18); rot(ao, 'upperarm01.R', 'Y', -10); rot(ao, 'lowerarm01.R', 'X', -48); rot(ao, 'lowerarm01.L', 'X', -15)
        rot(ao, 'lowerleg01.R', 'X', 7); head_turn(ao, 22, -5); rot(ao, 'spine03', 'Z', 6)
    elif name == 'look':   # nhìn quanh: quay đầu + vai
        rot(ao, 'spine03', 'Z', -12); head_turn(ao, -48, 3)
        for s in ('L', 'R'): rot(ao, f'lowerarm01.{s}', 'X', -14)
    elif name == 'back':   # chắp tay sau lưng (đứng nghỉ)
        for s, sg in (('L', -1), ('R', 1)): rot(ao, f'upperarm01.{s}', 'X', 22); rot(ao, f'lowerarm01.{s}', 'Z', 75 * sg)
        head_turn(ao, rr.uniform(-15, 15))
    elif name == 'work_tool':   # chữa tường: tay phải cầm bay/búa đưa lên, tay trái tì tường
        rot(ao, 'upperarm01.R', 'X', -105); rot(ao, 'lowerarm01.R', 'X', -35); rot(ao, 'upperarm01.L', 'X', -70); rot(ao, 'lowerarm01.L', 'X', -25)
        rot(ao, 'spine02', 'X', -6); head_turn(ao, 0, -8)
    elif name == 'work_order':   # gác: đứng thẳng, súng dựng bên phải
        rot(ao, 'upperarm01.R', 'Y', 6); rot(ao, 'lowerarm01.R', 'X', -18)
    elif name.startswith('work_'):
        arms_hold(ao, name[5:]); rot(ao, 'lowerleg01.L', 'X', 6)
    elif name[0] in 'wc' and name[-1].isdigit():
        ph = 2 * math.pi * int(name[-1]) / 8; legs_walk(ao, ph, amp)
        if name[0] == 'w':
            for s, off in (('L', 0.0), ('R', math.pi)):
                p = ph + off; a_ = -0.55 * amp * math.sin(p)
                rot(ao, f'upperarm01.{s}', 'X', -a_ * 0.9); rot(ao, f'lowerarm01.{s}', 'X', -12 - 10 * max(0.0, math.sin(p + math.pi)))
        else:
            arms_hold(ao, name[1:-1])
        rot(ao, 'spine03', 'Z', 4 * math.sin(ph))

def items(ao, role, pname, R):
    """vật cầm theo tư thế, dựng ở toạ độ xương SAU khi đặt tư thế; gắn xương để đi theo nhịp bước."""
    out = []; P = lambda b: ao.pose.bones[b].head.copy()
    def add(kind, loc, scale, col, bone, rot_=(0, 0, 0), rough=0.6, mk='plain'):
        p = prim(kind, loc, scale, col, rot_, rough, mk); p.parent = ao; out.append(p)   # mẫu ở gốc toạ độ → không cần nghịch đảo cha
    wood = C(0.22, 0.13, 0.07)
    if R.get('gun') == 'musket' and pname != 'work_order':
        sh = P('shoulder01.L'); add('cyl', sh + Vector((0.02, 0.12, 0.05)), (0.016, 0.016, 0.6), wood, 'spine03', (0.62, 0, 0), 0.5)
    if R.get('gun') == 'rifle' and pname != 'work_order':
        sh = P('shoulder01.R'); add('cyl', sh + Vector((-0.02, 0.1, -0.15)), (0.014, 0.014, 0.55), C(0.2, 0.13, 0.08), 'spine03', (0.12, 0, 0), 0.5)
    if pname == 'work_order':   # súng dựng đất bên phải, tay phải giữ nòng
        w = P('wrist.R'); L_ = 0.75 if R.get('gun') == 'musket' else 0.56
        add('cyl', Vector((w.x - 0.04, w.y - 0.02, L_)), (0.016, 0.016, L_), wood, 'root', (0, 0, 0), 0.5)
    hold = pname[5:] if pname.startswith('work_') else (pname[1:-1] if pname[0] == 'c' and pname[-1].isdigit() else None)
    if hold == 'tool':
        w = P('wrist.R'); add('cube', w + Vector((0, -0.08, 0.02)), (0.012, 0.09, 0.012), wood, 'lowerarm01.R'); add('cube', w + Vector((0, -0.16, 0.02)), (0.05, 0.02, 0.03), C(0.3, 0.3, 0.32), 'lowerarm01.R', rough=0.4)
    elif hold == 'box':
        c = (P('wrist.L') + P('wrist.R')) / 2 + Vector((0, -0.08, 0.06))
        if EP == 1782: add('cyl', c, (0.17, 0.17, 0.2), C(0.36, 0.25, 0.15), 'spine02', (0, math.pi / 2, 0), 0.7, 'cloth')   # thùng nhỏ nằm ngang
        else: add('cube', c, (0.24, 0.17, 0.14), C(0.42, 0.36, 0.24), 'spine02', rough=0.75, mk='cloth')                     # hòm gỗ
    elif hold == 'sack':
        sh = P('shoulder01.R'); add('sph', sh + Vector((-0.02, 0.04, 0.12)), (0.17, 0.26, 0.13), C(0.55, 0.48, 0.36) if EP == 1782 else C(0.32, 0.36, 0.28), 'spine03', (0.3, 0, 0.2), 0.9, 'cloth')
    elif hold == 'basket':
        w = P('wrist.L'); add('cyl', w + Vector((0.04, -0.05, 0.08)), (0.16, 0.16, 0.1), C(0.5, 0.38, 0.22), 'lowerarm01.L', rough=0.9, mk='cloth')
    return out

# ---------------------------------------------------------------- tờ sprite: hàng = 8 hướng, cột = tư thế
NA = 8; ROWD = 16.0; PITCH = math.radians(-8.0)
head = math.radians(A.head); fwd = Vector((math.sin(head), math.cos(head), 0)); right = Vector((math.cos(head), -math.sin(head), 0))
def poses_for(R):
    if R.get('pair'): return [f'w{k}' for k in range(8)]
    ps = ['st'] + [f'w{k}' for k in range(8)] + ['talk', 'look', 'back', 'work_' + R['work']]
    if R.get('carry'): ps += [f'c{R["carry"]}{k}' for k in range(8)]
    return ps
roles = A.roles.split(','); meta = {'epoch': EP, 'head': A.head, 'pxm': A.pxm, 'na': NA, 'rowd': ROWD, 'pitch_deg': -8.0, 'roles': {}}
LAT = math.radians(36.14); DECL = math.radians(4.0)
def sun_at(hour):
    Hh = math.radians((hour - 12) * 15)
    alt = math.asin(math.sin(LAT) * math.sin(DECL) + math.cos(LAT) * math.cos(DECL) * math.cos(Hh))
    az = math.atan2(math.sin(Hh), math.cos(Hh) * math.sin(LAT) - math.tan(DECL) * math.cos(LAT)) + math.pi
    return math.degrees(alt), math.degrees(az) % 360
for role in roles:
    if role not in ROLES: continue
    R0 = ROLES[role]; pair = R0.get('pair'); R = ROLES[pair] if pair else R0
    nb = 1 if pair else 2
    for bi in range(nb):
        rname = role if pair else f'{role}~{bi}'
        for o in list(sc.objects): bpy.data.objects.remove(o, do_unlink=True)
        PS = poses_for(R0); CELLX = 3.6 if pair else 1.7; NP = len(PS); cells = []
        rr = random.Random(EP * 100 + roles.index(role) * 7 + bi)
        if pair: protos = [make_person(pair, 0, 'P0'), make_person(pair, 1, 'P1')]
        else: protos = [make_person(role, bi, 'P')]
        for ao_, o_, pa_ in protos: ao_.hide_render = True; o_.hide_render = True; [setattr(p, 'hide_render', True) for p in pa_]
        CACHE = {}
        def posed(j, pn_):
            """đặt tư thế MỘT lần trên người mẫu (ẩn), ghi matrix_basis từng xương + zmin + vật cầm → sao cho mọi ô (tránh cập nhật cả cảnh mỗi lần xoay)."""
            if (j, pn_) in CACHE: return CACHE[(j, pn_)]
            ao_, o_, pa_ = protos[j]; pose(ao_, pn_, 'm' if pair else R['sex'], rr)
            its = items(ao_, role, pn_, R) if not pair else []
            for p in its: p.hide_render = True
            dg = bpy.context.evaluated_depsgraph_get(); me_ = o_.evaluated_get(dg).to_mesh(); zmin = min(v_.co.z for v_ in me_.vertices); o_.evaluated_get(dg).to_mesh_clear()
            CACHE[(j, pn_)] = ({pb.name: pb.matrix_basis.copy() for pb in ao_.pose.bones}, zmin, its); return CACHE[(j, pn_)]
        for ai in range(NA):
            for pi, pn in enumerate(PS):
                if A.test and ai not in (0, 2): continue
                d = (-fwd); a = math.radians(45 * ai); d = Vector((d.x * math.cos(a) - d.y * math.sin(a), d.x * math.sin(a) + d.y * math.cos(a), 0))
                yaw = math.atan2(d.y, d.x) - math.atan2(-1, 0)
                u = (pi - (NP - 1) / 2) * CELLX; v = ai * ROWD; pos = right * u + fwd * v
                mem = [(0, f'cbarrow{int(pn[1:])}', 0.85), (1, f'cbarrow{(int(pn[1:]) + 4) % 8}', -0.85)] if pair else [(0, pn, 0.0)]
                for j, pn_, off in mem:
                    basis, zmin, its = posed(j, pn_)
                    a2, o2 = clone(*protos[j], f'{rname}_{ai}_{pi}_{j}')
                    for bn, mb in basis.items(): a2.pose.bones[bn].matrix_basis = mb
                    for p in its:
                        p2 = p.copy(); sc.collection.objects.link(p2); p2.parent = a2; p2.hide_render = False
                    p_ = pos + d * off; a2.location = (p_.x, p_.y, -zmin); a2.rotation_euler = (0, 0, yaw)
                if pair:   # thùng (1782) / hòm (1943) giữa hai người ở tầm tay buông, hai đòn khiêng dọc hướng đi
                    c = pos + Vector((0, 0, 0.55))
                    if R0['item'] == 'barrel': prim('cyl', c, (0.28, 0.28, 0.36), C(0.36, 0.25, 0.15), (0, math.pi / 2, yaw + math.pi / 2), 0.7, 'cloth')
                    else: prim('cube', c, (0.4, 0.3, 0.25), C(0.42, 0.36, 0.24), (0, 0, yaw), 0.75, 'cloth')
                    for s_ in (-1, 1):
                        side = Vector((-d.y, d.x, 0)) * 0.24 * s_; prim('cube', pos + side + Vector((0, 0, 0.66)), (0.02, 1.15, 0.02), C(0.3, 0.22, 0.14), (0, 0, yaw), 0.7)
                cells.append({'a': ai, 'p': pi, 'pose': pn, 'world': [pos.x, pos.y], 'dir': [d.x, d.y]})
        bpy.context.view_layer.update()
        cam = bpy.data.cameras.new('c'); cam.type = 'ORTHO'
        Wm = NP * CELLX; Hm = (NA - 1) * ROWD * math.sin(abs(PITCH)) + 2.7
        W, H = int(Wm * A.pxm), int(Hm * A.pxm); cam.ortho_scale = max(Wm, Hm)
        co = bpy.data.objects.new('c', cam); sc.collection.objects.link(co); sc.camera = co
        mid = fwd * ((NA - 1) * ROWD / 2); D = 200.0
        co.location = (mid.x - fwd.x * D * math.cos(PITCH), mid.y - fwd.y * D * math.cos(PITCH), 0.95 + D * math.sin(-PITCH))
        co.rotation_euler = (math.radians(90) + PITCH, 0, -head)
        sc.render.resolution_x, sc.render.resolution_y = W, H; sc.render.resolution_percentage = 100
        from bpy_extras.object_utils import world_to_camera_view
        bpy.context.view_layer.update()
        for c in cells:
            p = world_to_camera_view(sc, co, Vector((c['world'][0], c['world'][1], 0))); c['foot_px'] = [round(p.x * W, 1), round((1 - p.y) * H, 1)]
        if A.test:
            xs = [c['foot_px'][0] for c in cells]; ys = [c['foot_px'][1] for c in cells]
            sc.render.use_border = True; sc.render.use_crop_to_border = True
            sc.render.border_min_x = max(0, (min(xs) - CELLX * A.pxm) / W); sc.render.border_max_x = min(1, (max(xs) + CELLX * A.pxm) / W)
            sc.render.border_min_y = max(0, 1 - (max(ys) + 2.0 * A.pxm) / H); sc.render.border_max_y = min(1, 1 - (min(ys) - 2.3 * A.pxm) / H)
        sc.render.film_transparent = True
        sun = bpy.data.objects.new('sun', bpy.data.lights.new('sun', 'SUN')); sc.collection.objects.link(sun)
        world = bpy.data.worlds.new('w'); sc.world = world; world.use_nodes = True; bgn = world.node_tree.nodes['Background']
        sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = A.spp; sc.cycles.use_denoising = True; sc.render.use_persistent_data = True
        sc.view_settings.view_transform = 'AgX'
        try: sc.render.image_settings.media_type = 'MULTI_LAYER_IMAGE'
        except Exception: sc.render.image_settings.file_format = 'OPEN_EXR_MULTILAYER'
        sc.render.image_settings.color_depth = '16'
        rmeta = {'W': W, 'H': H, 'cellx': CELLX, 'poses': PS, 'cells': cells, 'passes': {}, 'render_s': {}, 'pair': bool(pair)}
        for p in A.passes.split(','):
            hr = PASSES[p]
            if hr is None:
                alt, az = 38.0, 235.0; sun.data.energy = 0.08; sun.data.color = (0.62, 0.72, 1.0); bgn.inputs[0].default_value = (0.004, 0.006, 0.012, 1); bgn.inputs[1].default_value = 1.0
            else:
                alt, az = sun_at(hr); warm = max(0.0, min(1.0, (20 - alt) / 20))
                sun.data.energy = 4.2 if alt > 12 else 2.0 + 2.2 * max(0, alt) / 12; sun.data.color = (1.0, 1.0 - 0.4 * warm, 1.0 - 0.7 * warm)
                bgn.inputs[0].default_value = (0.45, 0.55, 0.75, 1) if alt > 12 else (0.35, 0.33, 0.4, 1); bgn.inputs[1].default_value = 0.35
            sun.rotation_euler = (math.radians(90 - alt), 0, math.radians(-az + 180)); sun.data.angle = math.radians(1.5)
            t = time.time(); sc.render.filepath = os.path.join(A.out, f'{rname}_{p}.exr')
            if not os.path.exists(sc.render.filepath): bpy.ops.render.render(write_still=True)   # tiếp tục sau khi bị cắt: giữ EXR đã dựng (cùng hạt giống ⇒ cùng ô)
            rmeta['passes'][p] = {'sun_alt': round(alt, 2), 'sun_az': round(az, 2)}; rmeta['render_s'][p] = round(time.time() - t, 1)
            print('SPRITE', rname, p, W, H, rmeta['render_s'][p], round(time.time() - T0), flush=True)
        meta['roles'][rname] = rmeta
        json.dump(meta, open(os.path.join(A.out, f'sprites-{"-".join(roles)}.json'), 'w'), indent=1, ensure_ascii=False)   # ghi sau mỗi dáng
json.dump(meta, open(os.path.join(A.out, f'sprites-{"-".join(roles)}.json'), 'w'), indent=1, ensure_ascii=False)
print('DONE', round(time.time() - T0, 1))
