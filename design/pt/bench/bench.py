"""PT việc 1 — đo Cycles CPU / EEVEE headless trên máy phiên (không giả định).
Cảnh hộp đơn giản (giống mô tả cảnh đo của điều phối): sàn + 40 hộp + mặt trời + bầu trời Nishita, vật liệu Principled có nhiễu thủ tục.
  /opt/bpy/bin/python design/pt/bench/bench.py <engine> <W> <H> <spp> <denoise 0|1> <out.png>
engine: CYCLES | EEVEE ; in một dòng JSON: thời gian dựng (gồm/không gồm khởi tạo), số luồng."""
import bpy, sys, time, json, math, random, os
eng, W, H, spp, den, out = sys.argv[-6:]; W, H, spp, den = int(W), int(H), int(spp), den == '1'
t0 = time.time()
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
random.seed(1)
def mat(name, col, rough=0.7):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    n = nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = 12
    mix = nt.nodes.new('ShaderNodeMixRGB'); mix.blend_type = 'MULTIPLY'; mix.inputs[0].default_value = 0.5
    mix.inputs[1].default_value = (*col, 1); nt.links.new(n.outputs['Color'], mix.inputs[2])
    nt.links.new(mix.outputs[0], b.inputs['Base Color']); b.inputs['Roughness'].default_value = rough
    return m
bpy.ops.mesh.primitive_plane_add(size=200); bpy.context.object.data.materials.append(mat('g', (0.5, 0.45, 0.4)))
ms = [mat('m%d' % i, (random.uniform(.4, .9), random.uniform(.35, .8), random.uniform(.3, .7))) for i in range(6)]
for i in range(40):
    x = (i % 2) * 18 - 9; y = (i // 2) * 7 + 5
    bpy.ops.mesh.primitive_cube_add(location=(x, y, 0)); o = bpy.context.object
    h = random.uniform(6, 14); o.scale = (3, 3.2, h / 2); o.location.z = h / 2; o.data.materials.append(random.choice(ms))
bpy.ops.object.light_add(type='SUN', rotation=(math.radians(50), 0, math.radians(30))); bpy.context.object.data.energy = 4
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
sky = w.node_tree.nodes.new('ShaderNodeTexSky')
try: sky.sky_type = 'NISHITA'
except Exception: pass
w.node_tree.links.new(sky.outputs[0], w.node_tree.nodes['Background'].inputs[0])
bpy.ops.object.camera_add(location=(0, -2, 1.7), rotation=(math.radians(88), 0, 0)); sc.camera = bpy.context.object
sc.camera.data.lens = 28
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = W, H, 100
sc.render.filepath = out; sc.render.image_settings.file_format = 'PNG'
if eng == 'CYCLES':
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = spp
    sc.cycles.use_adaptive_sampling = False; sc.cycles.use_denoising = den
    if den: sc.cycles.denoiser = 'OPENIMAGEDENOISE'
    sc.render.threads_mode = 'AUTO'
else:
    sc.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE'
    sc.eevee.taa_render_samples = spp
t1 = time.time()
bpy.ops.render.render(write_still=True)
t2 = time.time()
print('BENCH', json.dumps({'engine': sc.render.engine, 'W': W, 'H': H, 'spp': spp, 'denoise': den, 'threads': sc.render.threads,
      'setup_s': round(t1 - t0, 2), 'render_s': round(t2 - t1, 2), 'total_s': round(t2 - t0, 2)}))
