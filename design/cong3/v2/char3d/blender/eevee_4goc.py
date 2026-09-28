# W4 · cửa mặt Ida lượt 2 — ảnh EEVEE 4 góc (0°, 35°, 90°, 150° quanh hướng mặt) của Ida 'bl' ĐÚNG như trong phim: đầu glb + thân/khăn 4 vòng/
# mũ phớt D2 (#262a33, hình của cast3d, không phải mũ giả lập) — lưới lấy từ dữ liệu xuất của page_l2.js ("export":1). Đèn studio trung tính.
# /opt/bpy/bin/python eevee_4goc.py -- <x.timing.json> <ảnh ra (tiền tố .png)>
import sys, os, json, base64, math, tempfile
import numpy as np
import bpy, mathutils
argv = sys.argv[sys.argv.index('--') + 1:]
X = json.load(open(argv[0]))['page_prof_ms']['export']; OUTP = argv[1]
bpy.ops.wm.read_factory_settings(use_empty=True); SC = bpy.context.scene
glb = os.path.join(tempfile.mkdtemp(), 'ida.glb'); open(glb, 'wb').write(base64.b64decode(X['glb_b64'])); bpy.ops.import_scene.gltf(filepath=glb)
R = mathutils.Matrix(((1, 0, 0, 0), (0, 0, -1, 0), (0, 1, 0, 0), (0, 0, 0, 1)))
for ob in [o for o in SC.objects if o.type == 'MESH']:
    part = ob.name.split('.')[0]; me = ob.data
    for i, m0 in enumerate(me.materials):
        if part == 'eyes': continue
        hx = (m0.name.split('|') + ['ffffff'])[1][:6]; fac = tuple(((int(hx[k:k + 2], 16) / 255) / 12.92 if int(hx[k:k + 2], 16) / 255 <= 0.04045 else ((int(hx[k:k + 2], 16) / 255 + 0.055) / 1.055) ** 2.4) for k in (0, 2, 4)) + (1.0,)   # màu gốc (sRGB hex trong tên vật liệu) → tuyến tính
        m = bpy.data.materials.new(part); m.use_nodes = True; nt = m.node_tree; bs = nt.nodes['Principled BSDF']
        bs.inputs['Roughness'].default_value = {'head': 0.6, 'neck': 0.6, 'hair': 0.5, 'brow': 0.55, 'earring': 0.3}.get(part, 0.85)
        if part in ('head', 'neck'): bs.inputs['Subsurface Weight'].default_value = 0.2; bs.inputs['Subsurface Radius'].default_value = (1.0, 0.35, 0.2); bs.inputs['Subsurface Scale'].default_value = 0.004
        if part == 'earring': bs.inputs['Metallic'].default_value = 0.85
        if me.color_attributes:
            ca = nt.nodes.new('ShaderNodeVertexColor'); ca.layer_name = me.color_attributes[0].name
            mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs['Factor'].default_value = 1.0
            mx.inputs[6].default_value = fac; nt.links.new(ca.outputs['Color'], mx.inputs[7]); nt.links.new(mx.outputs[2], bs.inputs['Base Color'])
        else: bs.inputs['Base Color'].default_value = fac
        me.materials[i] = m
Hm = R @ mathutils.Matrix(np.array(X['head']['matrixWorld']).reshape(4, 4).T.tolist()); H = X['head']['H']
ctr = Hm @ mathutils.Vector((0, 0.55 * H, 0.05 * H)); fw = (Hm.to_3x3() @ mathutils.Vector((0, 0, 1))); fw.z = 0; fw.normalize()
up = mathutils.Vector((0, 0, 1)); side = fw.cross(up)
wd = bpy.data.worlds.new('w'); SC.world = wd; wd.use_nodes = True; wd.node_tree.nodes['Background'].inputs['Color'].default_value = (0.05, 0.05, 0.06, 1)
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); SC.collection.objects.link(cam); SC.camera = cam; cam.data.lens = 85
SC.render.engine = 'BLENDER_EEVEE'; SC.eevee.taa_render_samples = 32; SC.render.resolution_x = SC.render.resolution_y = 640
SC.view_settings.view_transform = 'Standard'
tiles = []
for i, deg in enumerate((0, 35, 90, 150)):
    a = math.radians(deg); d = fw * math.cos(a) + side * math.sin(a)
    for o in [o for o in SC.objects if o.type == 'LIGHT']: bpy.data.objects.remove(o)
    for nm, (az, el, e, col) in {'key': (35, 30, 30, (1, 0.95, 0.88)), 'fill': (-50, 5, 8, (0.85, 0.9, 1)), 'rim': (160, 35, 20, (0.9, 0.92, 1))}.items():
        aa = a + math.radians(az); v = (fw * math.cos(aa) + side * math.sin(aa)) * math.cos(math.radians(el)) + up * math.sin(math.radians(el))
        ld = bpy.data.lights.new(nm, 'POINT'); ld.energy = e; ld.color = col; ld.shadow_soft_size = 0.15; o = bpy.data.objects.new(nm, ld); SC.collection.objects.link(o); o.location = ctr + v * 1.2
    cam.location = ctr + d * 1.35 * H / 0.258 + up * 0.05; cam.rotation_euler = (ctr - cam.location).to_track_quat('-Z', 'Y').to_euler()
    f = OUTP.replace('.png', f'_{i}.png'); SC.render.filepath = f; bpy.ops.render.render(write_still=True); tiles.append(f)
print('TILES', ' '.join(tiles))
