# Cine Lab · Cổng 6 (W4) — NGHIÊN CỨU KHẢ THI thân MPFB cho Cas (CHỈ BÁO CÁO, không vào phim). Tài sản lõi CC0 (RIGHTS W4-MPFB-A3).
# /opt/bpy/bin/python study_cas_body.py -- <repo mpfb2> <x.timing.json của page_l2 (export Cas hiện tại)> <ảnh ra .png> <json số liệu ra>
# Trái: thân Cas hiện tại (cast3d, xuất từ khung layout). Phải: người MPFB (nam 10 tuổi, như đầu 'bl') + khung xương 'default',
# ÁO LEN và QUẦN do W4 dựng bằng vỏ lệch theo pháp tuyến từ chính lưới thân CC0 (repo MPFB lõi KHÔNG có quần áo).
import sys, os, json, math, base64, tempfile, time, importlib
import numpy as np
import bpy, addon_utils, mathutils
argv = sys.argv[sys.argv.index('--') + 1:]
MP, XJ, OUTP, OUTJ = argv[0], argv[1], argv[2], argv[3]
T0 = time.time()
bpy.ops.wm.read_factory_settings(use_empty=True); SC = bpy.context.scene
ext = bpy.utils.user_resource('EXTENSIONS', path='user_default', create=True)
if not os.path.exists(os.path.join(ext, 'mpfb')): os.symlink(os.path.join(MP, 'src', 'mpfb'), os.path.join(ext, 'mpfb'))
addon_utils.enable('bl_ext.user_default.mpfb', default_set=True, handle_error=None)
HumanService = importlib.import_module('bl_ext.user_default.mpfb.services.humanservice').HumanService
TargetService = importlib.import_module('bl_ext.user_default.mpfb.services.targetservice').TargetService
sheet = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'model-sheet', 'cas.json')))
LC = sheet['local_colors']
def hexlin(h): h = h.lstrip('#'); v = np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)]) / 255; return np.where(v <= 0.04045, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)
def mat(name, hexc, rough=0.8):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']; c = hexlin(hexc)
    b.inputs['Base Color'].default_value = (*c, 1); b.inputs['Roughness'].default_value = rough; return m
# ---- người MPFB ----
macro = TargetService.get_default_macro_info_dict(); macro.update({'gender': 1.0, 'age': 0.1875 * 0.9, 'muscle': 0.5, 'weight': 0.45, 'proportions': 0.5})
macro['race'] = {'asian': 0.15, 'caucasian': 0.7, 'african': 0.15}
hum = HumanService.create_human(macro_detail_dict=macro, scale=0.1, mask_helpers=False, feet_on_ground=True)
rig = HumanService.add_builtin_rig(hum, 'default', import_weights=True)
for m in list(hum.modifiers): m.show_viewport = False
bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get(); ev = hum.evaluated_get(dg); me = ev.to_mesh()
BODY_N = 13380
nV = len(me.vertices); P = np.zeros(nV * 3); me.vertices.foreach_get('co', P); P = (np.array(hum.matrix_world) @ np.c_[P.reshape(-1, 3), np.ones(nV)].T).T[:, :3]
Nn = np.zeros(nV * 3); me.vertices.foreach_get('normal', Nn); Nn = Nn.reshape(-1, 3) @ np.array(hum.matrix_world)[:3, :3].T; Nn /= np.maximum(1e-9, np.linalg.norm(Nn, axis=1))[:, None]
F = [tuple(p.vertices) for p in me.polygons if max(p.vertices) < BODY_N]
ev.to_mesh_clear()
gname = {g.index: g.name for g in hum.vertex_groups}
BN = set(b.name for b in rig.data.bones)
cls = np.zeros((nV, 4))   # thân, tay, chân, (khác)
for v in hum.data.vertices:
    for g in v.groups:
        if gname[g.group] not in BN: continue
        n = gname[g.group].lower()
        k = 0 if any(t in n for t in ('spine', 'breast', 'clavicle', 'pelvis', 'root')) else 1 if any(t in n for t in ('upperarm', 'lowerarm', 'shoulder')) else 2 if any(t in n for t in ('thigh', 'calf', 'upperleg', 'lowerleg', 'foot')) else 3
        cls[v.index, k] += g.weight
bones = len(rig.data.bones)
H = P[:BODY_N, 2].max() - P[:BODY_N, 2].min()
hum.hide_render = True; rig.hide_render = True
def obj(name, V, Fs, m):
    mesh = bpy.data.meshes.new(name); mesh.from_pydata(V.tolist(), [], Fs); mesh.update()
    for p in mesh.polygons: p.use_smooth = True
    o = bpy.data.objects.new(name, mesh); SC.collection.objects.link(o); o.data.materials.append(m); return o
# da (toàn thân) + áo len (vỏ +12 mm, gấu/ cổ tay/ cổ lật cao) + quần (vỏ +8 mm)
skin = obj('mpfb_body', P[:BODY_N], F, mat('skin', LC.get('skin', '#e2bfa2'), 0.6))
w = cls[:BODY_N]; lab = np.argmax(w, 1)
def shell(sel_v, off, name, m):
    keepF = [f for f in F if all(sel_v[list(f)])]
    idx = np.unique(np.array([i for f in keepF for i in f])); remap = -np.ones(BODY_N, int); remap[idx] = np.arange(len(idx))
    V = P[idx] + Nn[idx] * off
    return obj(name, V, [tuple(remap[list(f)]) for f in keepF], m)
z = P[:BODY_N, 2]; neck_top = np.percentile(z[lab == 0], 99.5)
sw = ((lab == 0) | (lab == 1)) & (z < neck_top + 0.02) & (z > np.percentile(z[lab == 0], 12))
shell(sw, 0.012, 'ao_len', mat('sweater', LC.get('sweater', '#8f3a2e'), 0.9))
tr = ((lab == 2) | ((lab == 0) & (z < np.percentile(z[lab == 0], 30)))) & (z > P[:BODY_N, 2].min() + 0.12 * H)
shell(tr, 0.008, 'quan', mat('trousers', LC.get('trousers', '#2c3346'), 0.8))
mp_objs = [o for o in SC.objects if o.type == 'MESH' and o.name in ('mpfb_body', 'ao_len', 'quan')]
# ---- thân Cas hiện tại (cast3d) ----
X = json.load(open(XJ))['page_prof_ms']['export']
glb = os.path.join(tempfile.mkdtemp(), 'cas.glb'); open(glb, 'wb').write(base64.b64decode(X['glb_b64'])); before = set(SC.objects)
bpy.ops.import_scene.gltf(filepath=glb); cur = [o for o in SC.objects if o not in before and o.type == 'MESH']
for o in cur:
    for m in o.data.materials:
        if m and m.use_nodes and 'Principled BSDF' in m.node_tree.nodes: m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.8
bpy.context.view_layer.update()
def bbox(objs):
    pts = np.array([o.matrix_world @ mathutils.Vector(c) for o in objs for c in o.bound_box]); return pts.min(0), pts.max(0)
Mh = X['head']['matrixWorld']; fb = np.array([Mh[8], -Mh[10], Mh[9]]); ang = math.atan2(fb[0], -fb[1]) + math.pi   # hướng mặt (three Y-lên → Blender Z-lên) → quay về máy (−y)
piv = sum((o.matrix_world.translation for o in cur), mathutils.Vector()) / len(cur); Rz = mathutils.Matrix.Translation(piv) @ mathutils.Matrix.Rotation(ang, 4, 'Z') @ mathutils.Matrix.Translation(-piv)
for o in cur: o.matrix_world = Rz @ o.matrix_world
bpy.context.view_layer.update()
lo, hi = bbox(cur); ctr = (lo + hi) / 2; h_cur = hi[2] - lo[2]
for o in cur: o.location -= mathutils.Vector((ctr[0] + 0.55, ctr[1], lo[2]))
bpy.context.view_layer.update(); lo2, hi2 = bbox(mp_objs); s = h_cur / (hi2[2] - lo2[2]); c2 = (lo2 + hi2) / 2
for o in mp_objs: o.scale = (s, s, s); o.location = mathutils.Vector((0.55 - c2[0] * s, -c2[1] * s, -lo2[2] * s))
# ---- máy + đèn studio ----
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); SC.collection.objects.link(cam); SC.camera = cam
cam.data.type = 'ORTHO'; cam.data.ortho_scale = max(2.4, h_cur * 1.25); cam.location = (0, -6, h_cur * 0.5); cam.rotation_euler = (math.pi / 2, 0, 0)
for loc, e in (((-3, -4, 3), 800), ((4, -2, 2), 300), ((0, 4, 3), 400)):
    L = bpy.data.objects.new('L', bpy.data.lights.new('L', 'AREA')); L.data.energy = e; L.data.size = 3; L.location = loc; SC.collection.objects.link(L)
    L.rotation_euler = (mathutils.Vector((0, 0, h_cur * 0.5)) - mathutils.Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
SC.world = bpy.data.worlds.new('w'); SC.world.use_nodes = True; SC.world.node_tree.nodes['Background'].inputs[0].default_value = (0.18, 0.18, 0.2, 1)
SC.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE'
SC.render.resolution_x, SC.render.resolution_y = 1600, 1000; SC.render.filepath = OUTP; SC.eevee.taa_render_samples = 16
bpy.ops.render.render(write_still=True)
stats = {'mpfb_body_verts': BODY_N, 'mpfb_faces': len(F), 'bones_default_rig': bones, 'mpfb_height_m': round(float(H), 3), 'scale_to_cas': round(float(s), 3),
         'cas_current_mesh_objs': len(cur), 'cas_current_verts': int(sum(len(o.data.vertices) for o in cur)), 'render_s': round(time.time() - T0, 1)}
json.dump(stats, open(OUTJ, 'w'), indent=1); print('STUDY', stats, flush=True)
