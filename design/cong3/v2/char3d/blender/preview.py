# Cine Lab · Cửa mặt Ida — W4. Ảnh XEM NHANH của đầu 'bl' trong Blender (không phải khung nộp).
# /opt/bpy/bin/python preview.py -- <file.blend> <ảnh ra.png> [--engine EEVEE|WORKBENCH] [--expr choked] [--nohat] [--size 520]
# Có mũ giả lập (cùng số của cast3d A-α: gốc 0,80 H, nghiêng 0,08, miệng 0,4056 × 0,4543, vành 0,68) để kiểm tóc–băng mũ.
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import bpy
import ida_rig as RIG

argv = sys.argv[sys.argv.index('--') + 1:]
BL, OUTP = argv[0], argv[1]
opt = lambda k, d=None: argv[argv.index(k) + 1] if k in argv else d
ENG = opt('--engine', 'EEVEE'); EXPR = opt('--expr', 'neutral'); SZ = int(opt('--size', '520'))
bpy.ops.wm.open_mainfile(filepath=BL)
SC = bpy.context.scene
to_b = lambda p: (p[0], -p[2], p[1])

w = RIG.FACE_PRESETS.get(EXPR, {})
for ob in SC.objects:
    if ob.type == 'MESH' and ob.data.shape_keys:
        for kb in ob.data.shape_keys.key_blocks[1:]:
            kb.value = w.get(kb.name, 0.0) if kb.name in RIG.CHANNELS else 0.0

if '--nohat' not in argv:   # mũ giả lập
    RX0, RZ0, CH, BRM = 0.4056, 0.4543, 0.48, 0.68
    rings = []
    for yy, f in [(-0.005, 1.0), (0.0, 1.0), (0.12, 1.0), (0.3, 0.93), (0.44, 0.86), (0.48, 0.0)]:
        a = np.linspace(-np.pi, np.pi, 65)[:-1]
        r = np.hypot(np.sin(a) * RX0, np.cos(a) * RZ0) * f * (1.018 if 0 <= yy <= 0.12 else 1.0)
        rings.append(np.stack([np.sin(a) * r, np.full_like(a, yy), np.cos(a) * r], 1))
    a = np.linspace(-np.pi, np.pi, 65)[:-1]
    for fr_ in (1.0, BRM / RX0 * 0.62, BRM / RX0):
        x = np.sin(a) * RX0 * fr_ * 0.98; z = np.cos(a) * RX0 * fr_ * 0.98 * 1.12
        rr = np.hypot(x, z / 1.12); ff = np.clip((rr - RX0 * 0.98) / (BRM - RX0 * 0.98), 0, 1); frt = 0.5 + 0.5 * z / np.maximum(np.hypot(x, z), 1e-6)
        rings.insert(0, np.stack([x, -ff * ff * (0.03 + 0.05 * frt * frt), z], 1))
    V = np.concatenate(rings); n = 64
    Fs = [[i * n + j, i * n + (j + 1) % n, (i + 1) * n + (j + 1) % n, (i + 1) * n + j] for i in range(len(rings) - 1) for j in range(n)]
    ct, st = math.cos(0.08), math.sin(0.08)
    Vh = np.stack([V[:, 0], 0.80 + V[:, 1] * ct - V[:, 2] * st, V[:, 1] * st + V[:, 2] * ct], 1)
    me = bpy.data.meshes.new('hat'); me.from_pydata([to_b(p) for p in Vh], [], Fs); me.update()
    m = bpy.data.materials.new('hat'); m.use_nodes = True; m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.018, 0.022, 0.03, 1)
    me.materials.append(m); ob = bpy.data.objects.new('hat', me); SC.collection.objects.link(ob)

SC.render.engine = 'BLENDER_EEVEE' if ENG == 'EEVEE' else 'BLENDER_WORKBENCH'
SC.render.resolution_x = SZ; SC.render.resolution_y = SZ
SC.render.film_transparent = False
wd = bpy.data.worlds.new('w'); wd.use_nodes = True; wd.node_tree.nodes['Background'].inputs['Color'].default_value = (0.06, 0.06, 0.07, 1); SC.world = wd
if ENG == 'WORKBENCH':
    SC.display.shading.light = 'STUDIO'; SC.display.shading.color_type = 'TEXTURE'
else:
    for nm, loc, e, c in [('key', (1.6, 2.2, 1.6), 260, (1, 0.93, 0.85)), ('fill', (-2.0, 0.8, 0.6), 60, (0.8, 0.85, 1)), ('rim', (-0.8, -2.0, 1.4), 160, (0.9, 0.9, 1))]:
        L = bpy.data.objects.new(nm, bpy.data.lights.new(nm, 'POINT')); L.data.energy = e; L.data.color = c; L.data.shadow_soft_size = 0.2
        L.location = to_b(loc); SC.collection.objects.link(L)
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); SC.collection.objects.link(cam); SC.camera = cam
cam.data.lens = 85; cam.data.sensor_width = 36
tgt = np.array([0.0, 0.52, 0.0])
tiles = []
views = [(0, 0.0), (35, 0.03), (90, 0.0), (150, 0.05)] if '--views' not in argv else [(int(v), 0.0) for v in opt('--views').split(',')]
for i, (deg, up) in enumerate(views):
    a = math.radians(deg); d = 3.4
    p = tgt + np.array([math.sin(a) * d, up * d + 0.05, math.cos(a) * d])
    cam.location = to_b(p)
    dvec = np.array(to_b(tgt)) - np.array(to_b(p))
    import mathutils
    cam.rotation_euler = mathutils.Vector(dvec).to_track_quat('-Z', 'Y').to_euler()
    f = OUTP.replace('.png', f'_{i}.png'); SC.render.filepath = f
    bpy.ops.render.render(write_still=True); tiles.append(f)
print('TILES', ' '.join(tiles))
