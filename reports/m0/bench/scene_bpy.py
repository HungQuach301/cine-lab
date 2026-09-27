# Cảnh mẫu M0 — phong cách (c) Blender bpy (Workbench / EEVEE), không dùng Cycles, không GPU.
# /opt/bpy/bin/python scene_bpy.py --engine EEVEE|WORKBENCH --start 0 --end 240 --mb 1|8 --outdir DIR [--json t.json] [--res 100]
import bpy, json, math, os, sys, time
import numpy as np

A = sys.argv
arg = lambda k, d: A[A.index('--' + k) + 1] if '--' + k in A else d
ENGINE, START, END = arg('engine', 'EEVEE'), int(arg('start', 0)), int(arg('end', 240))
MB, OUT, JSON, RES = int(arg('mb', 1)), arg('outdir', 'frames/bpy'), arg('json', None), int(arg('res', 100))
ROOT = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(ROOT, 'scene.json')))
M = json.load(open(os.path.join(ROOT, '../consistency/model-sheet.json')))
U = 0.32
os.makedirs(OUT, exist_ok=True)
T0 = time.time()

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = S['width'], S['height'], RES
sc.render.fps = S['fps']
sc.frame_start, sc.frame_end = 1, 240

def hexc(h, a=1.0):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return [x ** 2.2 for x in c] + [a]

_mats = {}
def mat(h, emit=0.0):
    k = (h, emit)
    if k in _mats: return _mats[k]
    m = bpy.data.materials.new(h + str(emit)); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = hexc(h); b.inputs['Roughness'].default_value = 0.85
    if emit:
        b.inputs['Emission Color'].default_value = hexc(h); b.inputs['Emission Strength'].default_value = emit
    m.diffuse_color = hexc(h)  # màu cho Workbench
    _mats[k] = m; return m

def add(obj, color, emit=0.0, parent=None):
    obj.data.materials.append(mat(color, emit))
    if parent: obj.parent = parent
    return obj

def box(size, loc, color, emit=0.0, parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = size
    return add(o, color, emit, parent)

def empty(loc, parent=None):
    o = bpy.data.objects.new('j', None); sc.collection.objects.link(o); o.location = loc
    if parent: o.parent = parent
    return o

def limb(parent, part, color):
    L, w = M[part]['length'] * U, M[part]['width'] * U
    bpy.ops.mesh.primitive_cylinder_add(radius=w / 2, depth=L, vertices=16, location=(0, 0, -L / 2))
    o = add(bpy.context.object, color, parent=parent)
    bpy.ops.object.shade_smooth()
    return o

# --- Nền 3 lớp ---
rnd = np.random.default_rng(7)
bpy.ops.mesh.primitive_plane_add(size=1, location=(4, 0, 0)); g = bpy.context.object; g.scale = (200, 30, 1); add(g, '#2b2128')
for x in np.arange(-60, 120, 3.5):  # lớp xa
    h, w = 6 + rnd.random() * 10, 2 + rnd.random() * 4
    box((w, 0.2, h), (x, 45, h / 2), S['layers'][0]['color'], emit=0.4)
x = -12.0
while x < 40:  # lớp giữa
    w, h = 2.6 + rnd.random() * 1.2, 3.5 + rnd.random() * 2.5
    box((w, 3, h), (x, 4.5, h / 2), S['layers'][1]['color'])
    wy = 0.9
    while wy < h - 0.6:
        wx = -w / 2 + 0.5
        while wx < w / 2 - 0.3:
            on = rnd.random() < 0.45
            box((0.3, 0.02, 0.45), (x + wx, 4.5 - 1.51, wy), '#e89a4a' if on else '#1a1520', emit=3.0 if on else 0)
            wx += 0.8
        wy += 0.9
    x += 3.2 + rnd.random() * 1.5
for x in np.arange(-8, 60, 7.0):  # lớp gần
    box((0.3, 0.3, 8), (x, -3.2, 4), S['layers'][2]['color'])
# Cột đèn + nguồn sáng ấm duy nhất.
lx = S['light']['world_x'] / 100 - 9.6 + 3
box((0.12, 0.12, 3.4), (lx, 1.2, 1.7), '#15111a')
box((0.28, 0.28, 0.4), (lx, 1.2, 3.55), '#ffd08a', emit=25)
ld = bpy.data.lights.new('lamp', 'POINT'); ld.energy = 2500; ld.color = hexc(S['light']['color'])[:3]; ld.shadow_soft_size = 0.2
lo = bpy.data.objects.new('lamp', ld); sc.collection.objects.link(lo); lo.location = (lx, 1.0, 3.5)
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
w.node_tree.nodes['Background'].inputs['Color'].default_value = hexc('#3a2540'); w.node_tree.nodes['Background'].inputs['Strength'].default_value = 1.2

# --- Nhân vật từ model sheet (trục: +x phía trước, +z lên) ---
T = M['torso']; tl = T['length'] * U
legLen = (M['thigh']['length'] + M['shin']['length'] + M['foot']['width']) * U
root = empty((0, 0, legLen * 0.97))
bpy.ops.mesh.primitive_cone_add(vertices=20, radius1=T['bottom_width'] * U / 2, radius2=T['top_width'] * U / 2, depth=tl, location=(0, 0, tl / 2))
torso = add(bpy.context.object, T['color'], parent=root); torso.scale.y = 0.6
hcz = tl + M['neck']['length'] * U + M['head']['length'] * U / 2
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, hcz)); hd = add(bpy.context.object, M['head']['color'], parent=root)
hd.scale = (M['head']['width'] * U, M['head']['width'] * U, M['head']['length'] * U); bpy.ops.object.shade_smooth()
bpy.ops.mesh.primitive_cylinder_add(radius=M['hat']['width'] * U / 2, depth=0.03, location=(0, 0, hcz + M['head']['length'] * U * 0.3)); add(bpy.context.object, M['hat']['color'], parent=root)
bpy.ops.mesh.primitive_cylinder_add(radius=0.4 * U, depth=M['hat']['length'] * U, location=(0, 0, hcz + M['head']['length'] * U * 0.3 + M['hat']['length'] * U / 2)); add(bpy.context.object, M['hat']['color'], parent=root)
def chain(z, y, p1, p2, dark):
    j1 = empty((0, y, z), root); limb(j1, p1, '#3b2219' if dark else M[p1]['color'])
    j2 = empty((0, 0, -M[p1]['length'] * U), j1); limb(j2, p2, '#3b2219' if dark else M[p2]['color'])
    return j1, j2
legF, legB = chain(0, -0.1, 'thigh', 'shin', False), chain(0, 0.1, 'thigh', 'shin', True)
sz = tl - M['joints']['shoulder_from_torso_top'] * U
armF, armB = chain(sz, -0.2, 'upper_arm', 'forearm', False), chain(sz, 0.2, 'upper_arm', 'forearm', True)

cam_d = bpy.data.cameras.new('cam'); cam_d.lens = 35; cam_d.sensor_width = 36
cam = bpy.data.objects.new('cam', cam_d); sc.collection.objects.link(cam); sc.camera = cam
cam.rotation_euler = (math.radians(86), 0, 0)

# Hoạt hình: khoá khung mỗi khung hình (cùng công thức với 2D/3D).
def pose(t):
    C = S['character']; ph = t * C['step_hz'] * 2 * math.pi; s = math.sin(ph)
    root.location = (-10.5 + 28 * t / S['duration_s'], 0, legLen * 0.97 - abs(math.cos(ph)) * 0.02)
    legF[0].rotation_euler.y = -0.42 * s; legF[1].rotation_euler.y = max(0, 0.7 * math.sin(ph + 1.2))
    legB[0].rotation_euler.y = 0.42 * s; legB[1].rotation_euler.y = max(0, -0.7 * math.sin(ph + 1.2))
    armF[0].rotation_euler.y = -(0.12 - 0.05 * s); armF[1].rotation_euler.y = -0.9
    armB[0].rotation_euler.y = -0.35 * s; armB[1].rotation_euler.y = -0.35
    cam.location = (3 + t * 0.6, -16, 2.2)
for f in range(1, 241):
    pose((f - 1) / S['fps'])
    for o in (root, legF[0], legF[1], legB[0], legB[1], armF[0], armF[1], armB[0], armB[1]):
        o.keyframe_insert('location' if o is root else 'rotation_euler', frame=f)
    cam.keyframe_insert('location', frame=f)

sc.render.image_settings.file_format = 'PNG'
sc.render.film_transparent = False
sc.view_settings.view_transform = 'AgX' if ENGINE == 'EEVEE' else 'Standard'
if ENGINE == 'EEVEE':
    sc.render.engine = 'BLENDER_EEVEE'
    ee = sc.eevee; ee.taa_render_samples = int(arg('samples', 16))
    for k in ('use_shadows', 'use_raytracing'):
        if hasattr(ee, k): setattr(ee, k, k == 'use_shadows')
    sc.render.use_motion_blur = MB > 1
    if MB > 1:
        sc.render.motion_blur_shutter = S['motion_blur']['shutter']
        ee.motion_blur_steps = MB
else:
    sc.render.engine = 'BLENDER_WORKBENCH'
    sc.display.shading.light = 'STUDIO'; sc.display.shading.color_type = 'MATERIAL'
    sc.display.shading.show_shadows = True; sc.display.render_aa = '8'

setup_s = time.time() - T0
per = []
for f in range(START, END):
    a = time.time(); fp = os.path.join(OUT, f'f{f:04d}.png')
    if ENGINE == 'EEVEE' or MB == 1:
        sc.frame_set(f + 1); sc.render.filepath = fp; bpy.ops.render.render(write_still=True)
    else:  # Workbench không có motion blur: siêu lấy mẫu thời gian thủ công rồi lấy trung bình.
        accum = None; sh = S['motion_blur']['shutter']
        for s in range(MB):
            off = sh * ((s + 0.5) / MB - 0.5)
            fi = math.floor(f + 1 + off); sc.frame_set(fi, subframe=(f + 1 + off) - fi)
            sc.render.filepath = fp; bpy.ops.render.render(write_still=True)
            im = bpy.data.images.load(fp, check_existing=False); px = np.array(im.pixels[:], dtype=np.float32); bpy.data.images.remove(im)
            accum = px if accum is None else accum + px
        im = bpy.data.images.new('acc', sc.render.resolution_x * RES // 100, sc.render.resolution_y * RES // 100, alpha=True)
        im.pixels = (accum / MB).tolist(); im.filepath_raw = fp; im.file_format = 'PNG'; im.save(); bpy.data.images.remove(im)
    per.append(time.time() - a)
    print(f'frame {f} {per[-1]:.2f}s', flush=True)
res = {'engine': ENGINE, 'mb_samples': MB, 'frames': END - START, 'setup_s': setup_s, 'render_s': sum(per),
       'mean_s_per_frame': sum(per) / len(per), 'max_s_per_frame': max(per), 'wall_s': time.time() - T0,
       'res_percent': RES}
res['render_s_per_film_s'] = res['wall_s'] / ((END - START) / S['fps'])
print(json.dumps(res))
if JSON: json.dump(res, open(JSON, 'w'), indent=1)
