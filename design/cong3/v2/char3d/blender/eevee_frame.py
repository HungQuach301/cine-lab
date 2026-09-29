# W4 · cửa mặt Ida lượt 2 — dựng lại MỘT khung PA1 trong Blender EEVEE từ dữ liệu xuất của page_l2.js ("export":1):
# cùng lưới Ida (đầu 'bl' + thân/áo/khăn/mũ của cast3d ở đúng tư thế khung), cùng máy, cùng mọi đèn của khung (L11 đã nâng, P5, cột phố, trời,
# ánh dội facelight). KHÔNG có bộ cảnh (tường, cột, thang), KHÔNG lớp vẽ Kuwahara, KHÔNG shader tóc bạc/da của three.js.
# Mục đích duy nhất: tách lỗi do HÌNH KHỐI hay do MÁY RENDER. Không thuộc pipeline.
# /opt/bpy/bin/python eevee_frame.py -- <x.timing.json> <ảnh ra.png> [--k 1.0] [--samples 32]
import sys, os, json, base64, math, tempfile
import numpy as np
import bpy, mathutils
argv = sys.argv[sys.argv.index('--') + 1:]
TJ, OUTP = argv[0], argv[1]
K = float(argv[argv.index('--k') + 1]) if '--k' in argv else 1.0
SMP = int(argv[argv.index('--samples') + 1]) if '--samples' in argv else 32
ex = json.load(open(TJ))['page_prof_ms']; X = ex['export']
bpy.ops.wm.read_factory_settings(use_empty=True); SC = bpy.context.scene
glb = os.path.join(tempfile.mkdtemp(), 'ida_frame.glb'); open(glb, 'wb').write(base64.b64decode(X['glb_b64']))
bpy.ops.import_scene.gltf(filepath=glb)
R = mathutils.Matrix(((1, 0, 0, 0), (0, 0, -1, 0), (0, 1, 0, 0), (0, 0, 0, 1)))   # three (y lên) → Blender (z lên)
to_b = lambda p: (R @ mathutils.Vector((p[0], p[1], p[2], 1.0))).xyz

def srgb2lin(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
for ob in [o for o in SC.objects if o.type == 'MESH']:
    part = ob.name.split('.')[0]; me = ob.data
    for i, m0 in enumerate(me.materials):
        if part == 'eyes':
            bs = m0.node_tree.nodes.get('Principled BSDF'); bs.inputs['Roughness'].default_value = 0.1
            if 'Coat Weight' in bs.inputs: bs.inputs['Coat Weight'].default_value = 1.0
            continue
        hx = (m0.name.split('|') + ['ffffff'])[1][:6]; fac = tuple(((int(hx[k:k + 2], 16) / 255) / 12.92 if int(hx[k:k + 2], 16) / 255 <= 0.04045 else ((int(hx[k:k + 2], 16) / 255 + 0.055) / 1.055) ** 2.4) for k in (0, 2, 4)) + (1.0,)   # màu gốc (sRGB hex trong tên vật liệu) → tuyến tính
        m = bpy.data.materials.new(part + '_ev'); m.use_nodes = True; nt = m.node_tree; bs = nt.nodes['Principled BSDF']
        rough = {'head': 0.6, 'neck': 0.6, 'hair': 0.5, 'brow': 0.55, 'earring': 0.3}.get(part, 0.85)
        bs.inputs['Roughness'].default_value = rough
        if part in ('head', 'neck') and 'Subsurface Weight' in bs.inputs:
            bs.inputs['Subsurface Weight'].default_value = 0.2; bs.inputs['Subsurface Radius'].default_value = (1.0, 0.35, 0.2); bs.inputs['Subsurface Scale'].default_value = 0.004
        if part == 'earring': bs.inputs['Metallic'].default_value = 0.85
        if me.color_attributes:
            ca = nt.nodes.new('ShaderNodeVertexColor'); ca.layer_name = me.color_attributes[0].name
            mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs['Factor'].default_value = 1.0
            mx.inputs[6].default_value = fac; nt.links.new(ca.outputs['Color'], mx.inputs[7]); nt.links.new(mx.outputs[2], bs.inputs['Base Color'])
        else: bs.inputs['Base Color'].default_value = fac
        me.materials[i] = m
    for p in me.polygons: p.use_smooth = True

cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); SC.collection.objects.link(cam); SC.camera = cam
M = mathutils.Matrix(np.array(X['cam']['matrixWorld']).reshape(4, 4).T.tolist())
cam.matrix_world = R @ M
cam.data.sensor_fit = 'VERTICAL'; cam.data.angle_y = math.radians(X['cam']['fov']); cam.data.clip_start = 0.02
W_, H_ = 1920, 1080
SC.render.resolution_x, SC.render.resolution_y = W_, H_
amb = np.zeros(3)
for L in X['lights']:
    c = L['color']; I = L['intensity'] * K
    if L['type'] == 'PointLight' or L['type'] == 'SpotLight':
        if I <= 0: continue
        ld = bpy.data.lights.new('L', 'SPOT' if L['type'] == 'SpotLight' else 'POINT'); ld.color = c; ld.energy = I * 4 * math.pi
        ld.shadow_soft_size = 0.02; ld.use_shadow = bool(L['castShadow']) or not L['face']
        if L['distance'] and L['distance'] > 0: ld.use_custom_distance = True; ld.cutoff_distance = L['distance']
        o = bpy.data.objects.new('L', ld); SC.collection.objects.link(o); o.location = to_b(L['pos'])
        if L['type'] == 'SpotLight' and L['dir']:
            d = mathutils.Vector(tuple(to_b(L['dir']) - to_b([0, 0, 0]))); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler(); ld.spot_size = 2 * L['angle']
    elif L['type'] == 'DirectionalLight':
        ld = bpy.data.lights.new('S', 'SUN'); ld.color = c; ld.energy = I; o = bpy.data.objects.new('S', ld); SC.collection.objects.link(o)
        d = mathutils.Vector(tuple(to_b(L['dir']) - to_b([0, 0, 0]))); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    elif L['type'] in ('HemisphereLight', 'AmbientLight'):
        g = L['ground'] or c; amb += I * 0.5 * (np.array(c) + np.array(g))
wd = bpy.data.worlds.new('w'); SC.world = wd; wd.use_nodes = True
bg = wd.node_tree.nodes['Background']; bg.inputs['Color'].default_value = (*[float(v) for v in np.clip(amb / max(amb.max(), 1e-6), 0, 1)], 1); bg.inputs['Strength'].default_value = float(amb.max())
SC.render.engine = 'BLENDER_EEVEE'; SC.eevee.taa_render_samples = SMP
if hasattr(SC.eevee, 'use_shadows'): SC.eevee.use_shadows = True
SC.view_settings.view_transform = 'Standard'; SC.view_settings.exposure = math.log2(max(ex['exposure'], 1e-6))
SC.render.film_transparent = False
SC.render.filepath = OUTP; bpy.ops.render.render(write_still=True)
print('EEVEE XONG', OUTP, 'đèn', len(X['lights']), 'phơi sáng three', ex['exposure'], 'K', K)
