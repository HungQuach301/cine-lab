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

def gauss_(d, w): return math.exp(-(d / w) ** 2)
def sst(e0, e1, x): t = min(1, max(0, (x - e0) / (e1 - e0))); return t * t * (3 - 2 * t)
if '--nohat' not in argv:   # mũ phớt D2 (#262a33) theo hình của cast3d A-α: chóp thon 16 %, rãnh giữa + 2 vết bóp trước, vành trước cụp, băng mũ
    RX0, RZ0, CH, BR = 0.4056, 0.4543, 0.48, 0.68
    n = 72; A = np.linspace(-np.pi, np.pi, n + 1)[:-1]
    def crown_r(a, y): f = 1 - 0.16 * sst(0, CH, y); return np.hypot(math.sin(a) * RX0, math.cos(a) * RZ0) * f
    def top_y(x, z): return CH - 0.075 * gauss_(x, 0.07) * sst(-RZ0 * 0.9, -RZ0 * 0.2, z) * (1 - 0.3 * sst(0.2, 0.5, z)) - 0.05 * gauss_(math.hypot(abs(x) - 0.2, z - 0.30), 0.09)
    rings = []
    for fr_ in (1.36 / 2 / RX0, 0.8 * 1.36 / 2 / RX0 + 0.2, 1.0):   # vành: ngoài → miệng mũ
        ring = []
        for a in A:
            r = np.hypot(math.sin(a) * RX0, math.cos(a) * RZ0) * fr_; x, z = math.sin(a) * r, math.cos(a) * r
            rr = math.hypot(x, z / 1.12); ff = max(0, (rr - RX0 * 0.98) / (BR - RX0 * 0.98)); frt = 0.5 + 0.5 * z / max(math.hypot(x, z), 1e-6)
            ring.append((x, -ff * ff * (0.03 + 0.05 * frt * frt), z))
        rings.append(ring)
    for y in np.linspace(0.0, CH * 0.97, 9):
        rings.append([(math.sin(a) * crown_r(a, y), y, math.cos(a) * crown_r(a, y)) for a in A])
    for k in np.linspace(0.85, 0.0, 6):   # nắp chóp có rãnh
        ring = []
        for a in A:
            r = crown_r(a, CH) * k; x, z = math.sin(a) * r, math.cos(a) * r; ring.append((x, min(top_y(x, z), CH * 0.97 + 0.02 * k), z))
        rings.append(ring)
    V = np.array([p for r in rings for p in r])
    Fs = [[i * n + j, i * n + (j + 1) % n, (i + 1) * n + (j + 1) % n, (i + 1) * n + j] for i in range(len(rings) - 1) for j in range(n)]
    ct, st = math.cos(0.08), math.sin(0.08)
    def place(V): return np.stack([V[:, 0], 0.80 + V[:, 1] * ct - V[:, 2] * st, V[:, 1] * st + V[:, 2] * ct], 1)
    for nm, VV, FF, col in [('hat', V, Fs, (0.018, 0.022, 0.032, 1))]:
        me = bpy.data.meshes.new(nm); me.from_pydata([to_b(p) for p in place(VV)], [], FF); me.update()
        for pg in me.polygons: pg.use_smooth = True
        m = bpy.data.materials.new(nm); m.use_nodes = True; bs = m.node_tree.nodes['Principled BSDF']; bs.inputs['Base Color'].default_value = col; bs.inputs['Roughness'].default_value = 0.85
        me.materials.append(m); ob = bpy.data.objects.new(nm, me); SC.collection.objects.link(ob)
    bandV = np.array([(math.sin(a) * np.hypot(math.sin(a) * RX0, math.cos(a) * RZ0) * 1.02, y, math.cos(a) * np.hypot(math.sin(a) * RX0, math.cos(a) * RZ0) * 1.02) for y in (0.0, 0.12) for a in A])
    me = bpy.data.meshes.new('band'); me.from_pydata([to_b(p) for p in place(bandV)], [], [[j, (j + 1) % n, n + (j + 1) % n, n + j] for j in range(n)]); me.update()
    m = bpy.data.materials.new('band'); m.use_nodes = True; m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.022, 0.016, 0.014, 1)
    me.materials.append(m); ob = bpy.data.objects.new('band', me); SC.collection.objects.link(ob)

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
tgt = np.array([float(v) for v in opt('--tgt', '0,0.55,0').split(',')])
tiles = []
views = [(0, 0.0), (35, 0.03), (90, 0.0), (150, 0.05)] if '--views' not in argv else [(int(v), 0.0) for v in opt('--views').split(',')]
for i, (deg, up) in enumerate(views):
    a = math.radians(deg); d = float(opt('--dist', '3.4'))
    p = tgt + np.array([math.sin(a) * d, up * d + float(opt('--camy', '0.35')), math.cos(a) * d])
    cam.location = to_b(p)
    dvec = np.array(to_b(tgt)) - np.array(to_b(p))
    import mathutils
    cam.rotation_euler = mathutils.Vector(dvec).to_track_quat('-Z', 'Y').to_euler()
    f = OUTP.replace('.png', f'_{i}.png'); SC.render.filepath = f
    bpy.ops.render.render(write_still=True); tiles.append(f)
print('TILES', ' '.join(tiles))
