#!/opt/bpy/bin/python
"""LOOK-T4 · NƯỚNG ÁNH SÁNG THEO MỐC bằng Cycles (CPU, hoặc GPU nếu --gpu) — như NC-CPU cách A §2.1 mục 6 / LOOK-1 T3 (lightmap theo mốc).
  /opt/bpy/bin/python scripts/k2ldn/nuong_look.py <năm> <ra.png> [--box E0,N0,E1,N1] [--m 2.0] [--spp 16] [--gpu]
Cảnh: mọi tam giác của ldn2.bin còn sống ở <năm> (tl.x ≤ năm < tl.y; lớp 2 phế tích chỉ khi năm 1667–1675) + địa hình của năm (h66 trước 1866, h26 sau 1870) trong hộp.
Trời đều (radiance 1, không mặt trời) → nướng DIFFUSE (trực tiếp + gián tiếp, không màu) lên mặt đất UV phẳng theo (E, N): R = bức xạ trời có che khuất + nảy, so với mặt phẳng trống = 1.
Ra PNG 16 bit xám (×0,8 để chừa đầu sáng; three.js nhân lại) + <ra>.json (hộp, giây nướng, số tam giác)."""
import sys, os, json, time, math
import numpy as np
import bpy
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
YEAR = float(a[0]); OUTP = os.path.abspath(a[1])
def opt(k, d): return a[a.index(k) + 1] if k in a else d
BOX = [float(v) for v in opt('--box', '531000,179900,533900,181900').split(',')]; MPX = float(opt('--m', '2.0')); SPP = int(opt('--spp', '16')); GPU = '--gpu' in a
DATA = os.environ.get('LDN_DATA', '/var/tmp/ldn'); J = json.load(open(os.path.join(DATA, 'look/ldn2.json'))); B = open(os.path.join(DATA, 'look/ldn2.bin'), 'rb').read()
def arr(nm, dt):
    l = J['bo_cuc'][nm]; return np.frombuffer(B, dtype=dt, count=l['len'] // np.dtype(dt).itemsize, offset=l['off'])
P = arr('pos', np.float32).reshape(-1, 3); TL = arr('tl', np.float32).reshape(-1, 4); K = arr('k', np.uint8)
E0, N0 = J['goc_EN']; x0, x1 = BOX[0] - E0 - 300, BOX[2] - E0 + 300; z0, z1 = -(BOX[3] - N0) - 300, -(BOX[1] - N0) + 300
tri = P.reshape(-1, 3, 3); ttl = TL[::3]; tk = K[::3]
alive = (ttl[:, 0] <= YEAR) & (YEAR < ttl[:, 1])
if not (1666.7 < YEAR < 1676): alive &= tk != 2
cen = tri.mean(1); alive &= (cen[:, 0] > x0) & (cen[:, 0] < x1) & (cen[:, 2] > z0) & (cen[:, 2] < z1)
tri = tri[alive]; print('tam giác sống', len(tri), flush=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = SPP; sc.cycles.use_denoising = False
if GPU:
    pr = bpy.context.preferences.addons['cycles'].preferences; pr.compute_device_type = 'OPTIX'; pr.get_devices(); [setattr(d, 'use', True) for d in pr.devices]; sc.cycles.device = 'GPU'
else: sc.cycles.device = 'CPU'; sc.render.threads_mode = 'AUTO'
sc.cycles.max_bounces = 3; sc.cycles.diffuse_bounces = 2
w = bpy.data.worlds.new('troi'); w.use_nodes = True; w.node_tree.nodes['Background'].inputs[0].default_value = (1, 1, 1, 1); w.node_tree.nodes['Background'].inputs[1].default_value = 1.0; sc.world = w
def mesh(name, V, F, mat):
    me = bpy.data.meshes.new(name); me.vertices.add(len(V)); me.vertices.foreach_set('co', V.astype(np.float32).ravel())
    me.loops.add(F.size); me.loops.foreach_set('vertex_index', F.astype(np.int32).ravel()); me.polygons.add(len(F))
    me.polygons.foreach_set('loop_start', (np.arange(len(F)) * F.shape[1]).astype(np.int32)); me.polygons.foreach_set('loop_total', np.full(len(F), F.shape[1], np.int32))
    me.update(calc_edges=True); ob = bpy.data.objects.new(name, me); sc.collection.objects.link(ob); me.materials.append(mat); return ob, me
def dmat(name, g):
    m = bpy.data.materials.new(name); m.use_nodes = True; m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (g, g, g, 1); m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 1.0; return m
# toạ độ Blender: X = x (đông), Y = −z (bắc), Z = y (cao)
V = tri.reshape(-1, 3)[:, [0, 2, 1]] * np.array([1, -1, 1], np.float32); F = np.arange(len(V)).reshape(-1, 3)
mesh('nha', V, F, dmat('nha', 0.30))
# địa hình của năm trong hộp (+ đệm 300 m)
T = J['dia_hinh']; h = arr('h66' if YEAR < 1867 else 'h26', np.float32).reshape(T['nz'], T['nx'])
xs = T['x0'] + np.arange(T['nx']) * T['step']; zs = T['z0'] + np.arange(T['nz']) * T['step']
gx0, gx1, gz0, gz1 = BOX[0] - E0, BOX[2] - E0, -(BOX[3] - N0), -(BOX[1] - N0)                    # mặt đất ĐÚNG hộp (UV ∈ [0,1]; UV ngoài hộp bị ghi chồng)
ci = np.where((xs >= gx0 - 0.01) & (xs <= gx1 + 0.01))[0]; ri = np.where((zs >= gz0 - 0.01) & (zs <= gz1 + 0.01))[0]; hh = h[np.ix_(ri, ci)]
XX, ZZ = np.meshgrid(xs[ci], zs[ri]); Vt = np.stack([XX.ravel(), -ZZ.ravel(), np.maximum(hh.ravel(), 0.6)], 1)
nz_, nx_ = hh.shape; idx = np.arange(nz_ * nx_).reshape(nz_, nx_); Ft = np.stack([idx[:-1, :-1].ravel(), idx[1:, :-1].ravel(), idx[1:, 1:].ravel(), idx[:-1, 1:].ravel()], 1)   # pháp tuyến hướng LÊN (trục Y Blender = −z đảo chiều vòng)
ob, me = mesh('dat', Vt, Ft, dmat('dat', 0.25))
uv = me.uv_layers.new(name='UV'); lv = np.array([l.vertex_index for l in me.loops]); co = Vt[lv]
U_ = (co[:, 0] + E0 - BOX[0]) / (BOX[2] - BOX[0]); V_ = (co[:, 1] + N0 - BOX[1]) / (BOX[3] - BOX[1]); uv.data.foreach_set('uv', np.stack([U_, V_], 1).astype(np.float32).ravel())
W_, H_ = int(round((BOX[2] - BOX[0]) / MPX)), int(round((BOX[3] - BOX[1]) / MPX)); img = bpy.data.images.new('bake', W_, H_, float_buffer=True)
mt = me.materials[0]; nd = mt.node_tree.nodes.new('ShaderNodeTexImage'); nd.image = img; mt.node_tree.nodes.active = nd
for o in sc.objects: o.select_set(False)
ob.select_set(True); bpy.context.view_layer.objects.active = ob
bpy.context.view_layer.update()
sc.render.bake.use_pass_direct = True; sc.render.bake.use_pass_indirect = True; sc.render.bake.use_pass_color = False; sc.render.bake.margin = 2
t0 = time.time(); bpy.ops.object.bake(type='DIFFUSE'); dt = time.time() - t0
px = np.array(img.pixels[:], np.float32).reshape(H_, W_, 4)[..., 0]
print('nướng', round(dt, 1), 's', W_, 'x', H_, 'tb', float(px.mean()), flush=True)
q = np.clip(px * 0.8, 0, 1)                                         # hàng 0 = nam (Blender) → lật để hàng 0 = bắc trong PNG; three.js flipY → v = 0 ở nam
np.save(OUTP + '.npy', np.flipud(q).astype(np.float32))
import subprocess; subprocess.run(['/opt/cine/bin/python', '-I', '-c', 'import sys,numpy as n; from PIL import Image; q=n.load(sys.argv[1]); Image.fromarray((q*255+0.5).astype(n.uint8)).save(sys.argv[2])', OUTP + '.npy', OUTP], check=True)
json.dump({'nam': YEAR, 'hop_EN': BOX, 'm_px': MPX, 'spp': SPP, 'gpu': GPU, 'giay': round(dt, 1), 'tam_giac': int(len(tri)), 'co': [W_, H_], 'tb': float(px.mean()), 'he_so': 0.8}, open(OUTP + '.json', 'w'))
