"""TIEN-KY-T4 · CYCLES (GPU) cho bản thử T1 (ii): phố gỗ 1666 cháy, lửa/khói THỂ TÍCH thủ tục — cùng hình học + cùng máy với cách A.
  blender -b --factory-startup --python-exit-code 1 -P cy_ldn.py -- <canh.npz> <ra_thư_mục> [--res 960x540] [--spp 64] [--frames a:b] [--dev OPTIX|CUDA|CPU] [--still f]
Đầu vào: canh.npz từ scripts/k2ldn/cy_xuat.py (tam giác + màu + tl, địa hình, ô cháy 20 m có giờ bén, shot.json).
Thời gian: thuộc tính cảnh 'gio' (giờ kể từ 2/9/1666 00:00, Julius) đặt khoá mỗi khung; vật liệu đọc qua Attribute VIEW_LAYER (cảnh).
Đèn: mặt trời theo thiên văn (NOAA, như design/k2v/tl/sun.js) + trời Nishita ban ngày; đêm: trăng yếu (Pepys b38) + đèn điểm theo cụm ô cháy (khoá năng lượng theo giờ)."""
import sys, os, json, math, time
import numpy as np
import bpy
a = sys.argv[sys.argv.index('--') + 1:]
NPZ, OUT = a[0], os.path.abspath(a[1]); opt = {}
i = 2
while i < len(a):
    if a[i].startswith('--') and i + 1 < len(a) and not a[i + 1].startswith('--'): opt[a[i]] = a[i + 1]; i += 2
    elif a[i].startswith('--'): opt[a[i]] = '1'; i += 1
    else: i += 1
RES = [int(x) for x in opt.get('--res', '960x540').split('x')]; SPP = int(opt.get('--spp', 64)); DEV = opt.get('--dev', 'OPTIX')
os.makedirs(OUT, exist_ok=True); T0 = time.time()
Z = np.load(NPZ, allow_pickle=False); S = json.loads(str(Z['shot']))
FPS = S.get('fps', 24); NF = int(round(S.get('dur', 5) * FPS))
fr = opt.get('--frames'); F0, F1 = (int(fr.split(':')[0]), int(fr.split(':')[1])) if fr else (0, NF - 1)
if '--still' in opt: F0 = F1 = int(opt['--still'])
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene

# ------------------------------------------------ thiết bị
def gpu():
    p = bpy.context.preferences.addons['cycles'].preferences
    for t in ([DEV, 'CUDA'] if DEV != 'CPU' else []):
        try:
            p.compute_device_type = t; p.refresh_devices(); n = 0
            for d in p.devices: d.use = d.type == t; n += d.use
            if n: print('CY-DEV', t, [d.name for d in p.devices if d.use], flush=True); return t
        except Exception as e: print('CY-DEV lỗi', t, repr(e))
    return 'CPU'
DT = gpu(); sc.render.engine = 'CYCLES'; sc.cycles.device = 'GPU' if DT != 'CPU' else 'CPU'
sc.cycles.samples = SPP; sc.cycles.use_denoising = True; sc.cycles.denoiser = 'OPENIMAGEDENOISE'
sc.cycles.max_bounces = 6; sc.cycles.diffuse_bounces = 3; sc.cycles.glossy_bounces = 2; sc.cycles.transparent_max_bounces = 8; sc.cycles.volume_bounces = 1
sc.cycles.volume_step_rate = float(opt.get('--vstep', 2.0)); sc.cycles.volume_max_steps = 256
sc.render.resolution_x, sc.render.resolution_y = RES; sc.render.resolution_percentage = 100; sc.render.fps = FPS
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_depth = '8'
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
sc.render.film_transparent = False

# ------------------------------------------------ thời gian + mặt trời
def hour_at(f):
    t = f / FPS; K = S['keys']
    if t <= K[0]['t']: return K[0]['hour']
    if t >= K[-1]['t']: return K[-1]['hour']
    for x, y in zip(K, K[1:]):
        if x['t'] <= t <= y['t']: u = (t - x['t']) / (y['t'] - x['t']); return x['hour'] + (y['hour'] - x['hour']) * u
def cr(p0, p1, p2, p3, t):
    t2, t3 = t * t, t * t * t
    return [0.5 * (2 * p1[i] + (-p0[i] + p2[i]) * t + (2 * p0[i] - 5 * p1[i] + 4 * p2[i] - p3[i]) * t2 + (-p0[i] + 3 * p1[i] - 3 * p2[i] + p3[i]) * t3) for i in range(3)]
def cam_at(f):
    t = f / FPS; K = S['keys']
    if t <= K[0]['t']: k = K[0]; return k['p'], k['l'], k['fov']
    if t >= K[-1]['t']: k = K[-1]; return k['p'], k['l'], k['fov']
    i = max(j for j in range(len(K) - 1) if K[j]['t'] <= t); x, y = K[i], K[i + 1]; u = (t - x['t']) / (y['t'] - x['t'])
    um = u if S.get('smooth') else u * u * (3 - 2 * u); k0, k3 = K[max(0, i - 1)], K[min(len(K) - 1, i + 2)]
    return cr(k0['p'], x['p'], y['p'], k3['p'], um), cr(k0['l'], x['l'], y['l'], k3['l'], um), x['fov'] + (y['fov'] - x['fov']) * u
RAD = math.pi / 180
def jdJulian(y, mo, d, h):
    if mo <= 2: y -= 1; mo += 12
    return math.floor(365.25 * (y + 4716)) + math.floor(30.6001 * (mo + 1)) + d - 1524.5 + h / 24
def sunpos(jd, lat=51.512, lon=-0.098):   # NOAA (bản rút gọn như sun.js)
    T = (jd - 2451545) / 36525; L0 = (280.46646 + T * (36000.76983 + 0.0003032 * T)) % 360; M = 357.52911 + T * (35999.05029 - 0.0001537 * T); e = 0.016708634 - T * 0.000042037
    C = math.sin(M * RAD) * (1.914602 - T * 0.004817) + math.sin(2 * M * RAD) * 0.019993 + math.sin(3 * M * RAD) * 0.000289
    lam = L0 + C - 0.00569 - 0.00478 * math.sin((125.04 - 1934.136 * T) * RAD); eps = 23 + (26 + (21.448 - T * 46.815) / 60) / 60 + 0.00256 * math.cos((125.04 - 1934.136 * T) * RAD)
    dec = math.asin(math.sin(eps * RAD) * math.sin(lam * RAD)); yv = math.tan(eps * RAD / 2) ** 2
    Et = 4 / RAD * (yv * math.sin(2 * L0 * RAD) - 2 * e * math.sin(M * RAD) + 4 * e * yv * math.sin(M * RAD) * math.cos(2 * L0 * RAD) - 0.5 * yv * yv * math.sin(4 * L0 * RAD) - 1.25 * e * e * math.sin(2 * M * RAD))
    tst = (((jd + 0.5) % 1) * 1440 + Et + 4 * lon + 1440) % 1440; ha = tst / 4 - 180
    cz = math.sin(lat * RAD) * math.sin(dec) + math.cos(lat * RAD) * math.cos(dec) * math.cos(ha * RAD); zen = math.acos(max(-1, min(1, cz)))
    az = math.acos(max(-1, min(1, (math.sin(lat * RAD) * math.cos(zen) - math.sin(dec)) / (math.cos(lat * RAD) * math.sin(zen))))) / RAD
    az = (az + 180) % 360 if ha > 0 else (540 - az) % 360
    return 90 - zen / RAD, az
def sun_for(h): return sunpos(jdJulian(1666, 9, 2, h + 0.098 / 15))
# ------------------------------------------------ hình học
def B(x, y, z): return (x, -z, y)    # cảnh (x, y lên, z = −N) → Blender (X đông, Y bắc, Z lên)
def mk_mesh(name, V, F, mat):
    me = bpy.data.meshes.new(name); me.from_pydata(V, [], F); me.update(); ob = bpy.data.objects.new(name, me); sc.collection.objects.link(ob); ob.data.materials.append(mat); return ob
def attr_float(me, nm, vals, dom='POINT'):
    at = me.attributes.new(nm, 'FLOAT', dom); at.data.foreach_set('value', np.asarray(vals, np.float32).ravel())
def attr_col(me, nm, vals, dom='POINT'):
    at = me.color_attributes.new(nm, 'FLOAT_COLOR', dom); at.data.foreach_set('color', np.asarray(vals, np.float32).ravel())
def nodes(mat):
    mat.use_nodes = True; nt = mat.node_tree; nt.nodes.clear(); return nt, nt.nodes, nt.links
def gio_node(N):
    at = N.new('ShaderNodeAttribute'); at.attribute_type = 'VIEW_LAYER'; at.attribute_name = 'gio'; return at.outputs['Fac']
def math_(N, Lk, op, a, b=None, val=None):
    m = N.new('ShaderNodeMath'); m.operation = op
    for idx, x in enumerate((a, b)):
        if x is None: continue
        if isinstance(x, (int, float)): m.inputs[idx].default_value = x
        else: Lk.new(x, m.inputs[idx])
    return m.outputs[0]
def smooth(N, Lk, x, e0, e1):
    m = N.new('ShaderNodeMapRange'); m.interpolation_type = 'SMOOTHSTEP'; m.inputs['From Min'].default_value = e0; m.inputs['From Max'].default_value = e1
    Lk.new(x, m.inputs['Value']); return m.outputs['Result']
def burn_expr(N, Lk, ign):
    a_ = math_(N, Lk, 'SUBTRACT', gio_node(N), ign)
    up = smooth(N, Lk, a_, 0.0, 0.7); dn = math_(N, Lk, 'SUBTRACT', 1.0, smooth(N, Lk, a_, 4.0, 9.0))
    f = math_(N, Lk, 'MULTIPLY', up, dn)
    ok = math_(N, Lk, 'GREATER_THAN', ign, -0.5)
    return math_(N, Lk, 'MULTIPLY', f, ok), a_
# nhà / công trình
tri = Z['tri']; col = Z['col'].astype(np.float32) / 255.0; tl = Z['tl']; kk = Z['k'].astype(np.float32)
n = len(tri); V = np.stack([tri[:, :, 0], -tri[:, :, 2], tri[:, :, 1]], -1).reshape(-1, 3)
F = np.arange(n * 3).reshape(-1, 3)
mb = bpy.data.materials.new('nha'); nt, N, Lk = nodes(mb)
out = N.new('ShaderNodeOutputMaterial'); bs = N.new('ShaderNodeBsdfPrincipled'); bs.inputs['Roughness'].default_value = 0.85
ca = N.new('ShaderNodeVertexColor'); ca.layer_name = 'col'
g2 = N.new('ShaderNodeGamma'); g2.inputs[1].default_value = 2.2; Lk.new(ca.outputs['Color'], g2.inputs[0]); Lk.new(g2.outputs[0], bs.inputs['Base Color'])
ia = N.new('ShaderNodeAttribute'); ia.attribute_name = 'ign'; ka = N.new('ShaderNodeAttribute'); ka.attribute_name = 'kk'
bI, aa = burn_expr(N, Lk, ia.outputs['Fac'])
isRuin = math_(N, Lk, 'COMPARE', ka.outputs['Fac'], 2.0); isRuin.node.inputs[2].default_value = 0.1
aliveH = math_(N, Lk, 'LESS_THAN', aa, 7.0); noIgn = math_(N, Lk, 'LESS_THAN', ia.outputs['Fac'], -0.5)
aliveH = math_(N, Lk, 'MAXIMUM', aliveH, noIgn)
ruinOn = math_(N, Lk, 'GREATER_THAN', aa, 5.0)
alive = math_(N, Lk, 'ADD', math_(N, Lk, 'MULTIPLY', isRuin, ruinOn), math_(N, Lk, 'MULTIPLY', math_(N, Lk, 'SUBTRACT', 1.0, isRuin), aliveH))
nz = N.new('ShaderNodeTexNoise'); nz.noise_dimensions = '4D'; nz.inputs['Scale'].default_value = 0.35; Lk.new(math_(N, Lk, 'MULTIPLY', gio_node(N), 40.0), nz.inputs['W'])
fl = smooth(N, Lk, nz.outputs['Fac'], 0.45, 0.75)
em = math_(N, Lk, 'MULTIPLY', bI, math_(N, Lk, 'ADD', 0.4, math_(N, Lk, 'MULTIPLY', fl, 2.6)))
Lk.new(math_(N, Lk, 'MULTIPLY', em, 6.0), bs.inputs['Emission Strength']); bs.inputs['Emission Color'].default_value = (1.0, 0.36, 0.08, 1)
char = math_(N, Lk, 'SUBTRACT', 1.0, math_(N, Lk, 'MULTIPLY', math_(N, Lk, 'MINIMUM', math_(N, Lk, 'MULTIPLY', bI, 1.4), 0.8), 1.0))
mc = N.new('ShaderNodeMixRGB'); mc.blend_type = 'MULTIPLY'; mc.inputs[0].default_value = 1.0; Lk.new(g2.outputs[0], mc.inputs[1]); Lk.new(char, mc.inputs[2]); Lk.new(mc.outputs[0], bs.inputs['Base Color'])
tr = N.new('ShaderNodeBsdfTransparent'); mx = N.new('ShaderNodeMixShader'); Lk.new(alive, mx.inputs[0]); Lk.new(tr.outputs[0], mx.inputs[1]); Lk.new(bs.outputs[0], mx.inputs[2]); Lk.new(mx.outputs[0], out.inputs['Surface'])
print('CY-B nha bắt đầu', round(time.time() - T0, 1), flush=True)
me0 = bpy.data.meshes.new('nha'); me0.vertices.add(len(V)); me0.vertices.foreach_set('co', V.astype(np.float32).ravel())
me0.loops.add(len(V)); me0.loops.foreach_set('vertex_index', np.arange(len(V), dtype=np.int32)); me0.polygons.add(n)
me0.polygons.foreach_set('loop_start', np.arange(0, 3 * n, 3, dtype=np.int32)); me0.polygons.foreach_set('loop_total', np.full(n, 3, np.int32)); me0.update(calc_edges=True)
ob = bpy.data.objects.new('nha', me0); sc.collection.objects.link(ob); ob.data.materials.append(mb)
print('CY-B nha xong', round(time.time() - T0, 1), flush=True)
attr_col(ob.data, 'col', np.concatenate([np.repeat(col, 3, 0), np.ones((n * 3, 1), np.float32)], 1))
attr_float(ob.data, 'ign', np.repeat(tl[:, 3], 3)); attr_float(ob.data, 'kk', np.repeat(kk, 3))
ob.data.polygons.foreach_set('use_smooth', np.zeros(n, bool))
# địa hình + nước
ter = Z['ter']; tx0, tz0, st = float(Z['ter_x0']), float(Z['ter_z0']), float(Z['ter_step']); nzr, nxr = ter.shape
XX, ZZ = np.meshgrid(tx0 + np.arange(nxr) * st, tz0 + np.arange(nzr) * st)
TV = np.stack([XX.ravel(), -ZZ.ravel(), ter.ravel()], 1); idx = np.arange(nxr * nzr).reshape(nzr, nxr)
TF = np.stack([idx[:-1, :-1].ravel(), idx[1:, :-1].ravel(), idx[1:, 1:].ravel(), idx[:-1, 1:].ravel()], 1)
mt = bpy.data.materials.new('dat'); nt, N, Lk = nodes(mt); o2 = N.new('ShaderNodeOutputMaterial'); b2 = N.new('ShaderNodeBsdfPrincipled'); b2.inputs['Roughness'].default_value = 0.95
n2 = N.new('ShaderNodeTexNoise'); n2.inputs['Scale'].default_value = 0.08; cr2 = N.new('ShaderNodeValToRGB'); cr2.color_ramp.elements[0].color = (0.16, 0.12, 0.08, 1); cr2.color_ramp.elements[1].color = (0.24, 0.19, 0.13, 1)
Lk.new(n2.outputs['Fac'], cr2.inputs[0]); Lk.new(cr2.outputs[0], b2.inputs['Base Color']); Lk.new(b2.outputs[0], o2.inputs['Surface'])
mk_mesh('dat', TV.tolist(), TF.tolist(), mt)
mw = bpy.data.materials.new('nuoc'); nt, N, Lk = nodes(mw); o3 = N.new('ShaderNodeOutputMaterial'); b3 = N.new('ShaderNodeBsdfPrincipled')
b3.inputs['Base Color'].default_value = (0.02, 0.03, 0.03, 1); b3.inputs['Roughness'].default_value = 0.06; b3.inputs['IOR'].default_value = 1.33
w3 = N.new('ShaderNodeTexWave'); w3.inputs['Scale'].default_value = 0.02; bm = N.new('ShaderNodeBump'); bm.inputs['Strength'].default_value = 0.08
Lk.new(w3.outputs['Fac'], bm.inputs['Height']); Lk.new(bm.outputs['Normal'], b3.inputs['Normal']); Lk.new(b3.outputs[0], o3.inputs['Surface'])
cx, cz = float(np.mean(XX)), float(np.mean(ZZ))
mk_mesh('nuoc', [(cx - 5000, -cz - 5000, 0.6), (cx + 5000, -cz - 5000, 0.6), (cx + 5000, -cz + 5000, 0.6), (cx - 5000, -cz + 5000, 0.6)], [(0, 1, 2, 3)], mw)
# ------------------------------------------------ lửa + khói thể tích (mỗi ô cháy một hộp; giờ bén = thuộc tính đối tượng 'ign')
cells = Z['cell']; h_all = [hour_at(f) for f in range(F0, F1 + 1)]; h0, h1 = min(h_all), max(h_all)
cells = cells[(cells[:, 3] < h1 + 0.2) & (cells[:, 3] > h0 - 40)]
if os.environ.get('CY_MAXCELL'): cells = cells[:int(os.environ['CY_MAXCELL'])]
print('CY-B thể tích', len(cells), round(time.time() - T0, 1), flush=True)
def vol_mat(kind):
    m = bpy.data.materials.new('vol-' + kind); nt, N, Lk = nodes(m); o = N.new('ShaderNodeOutputMaterial'); pv = N.new('ShaderNodeVolumePrincipled')
    ig = N.new('ShaderNodeAttribute'); ig.attribute_type = 'OBJECT'; ig.attribute_name = 'ign'
    bI, aa = burn_expr(N, Lk, ig.outputs['Fac'])
    tc = N.new('ShaderNodeTexCoord'); sep = N.new('ShaderNodeSeparateXYZ'); Lk.new(tc.outputs['Generated'], sep.inputs[0]); zc = sep.outputs['Z']
    nz = N.new('ShaderNodeTexNoise'); nz.noise_dimensions = '4D'; nz.inputs['Detail'].default_value = 6.0
    oi = N.new('ShaderNodeObjectInfo')
    w = math_(N, Lk, 'ADD', math_(N, Lk, 'MULTIPLY', gio_node(N), 60.0 if kind == 'lua' else 8.0), math_(N, Lk, 'MULTIPLY', oi.outputs['Random'], 100.0))
    Lk.new(w, nz.inputs['W'])
    vm = N.new('ShaderNodeVectorMath'); vm.operation = 'MULTIPLY'; vm.inputs[1].default_value = (3.0, 3.0, 2.0) if kind == 'lua' else (2.0, 2.0, 5.0); Lk.new(tc.outputs['Generated'], vm.inputs[0]); Lk.new(vm.outputs[0], nz.inputs['Vector'])
    # hình: lửa = chóp hẹp dần lên trên, khói = cột loe; mép hộp mềm
    gx = N.new('ShaderNodeVectorMath'); gx.operation = 'SUBTRACT'; gx.inputs[1].default_value = (0.5, 0.5, 0.0); Lk.new(tc.outputs['Generated'], gx.inputs[0])
    sp = N.new('ShaderNodeSeparateXYZ'); Lk.new(gx.outputs[0], sp.inputs[0])
    r = math_(N, Lk, 'SQRT', math_(N, Lk, 'ADD', math_(N, Lk, 'POWER', sp.outputs['X'], 2.0), math_(N, Lk, 'POWER', sp.outputs['Y'], 2.0)))
    if kind == 'lua':
        rad = math_(N, Lk, 'MULTIPLY', math_(N, Lk, 'SUBTRACT', 1.0, zc), 0.48)
        shape = math_(N, Lk, 'SUBTRACT', 1.0, smooth(N, Lk, math_(N, Lk, 'DIVIDE', r, math_(N, Lk, 'ADD', rad, 0.001)), 0.5, 1.0))
        dn = math_(N, Lk, 'MULTIPLY', smooth(N, Lk, math_(N, Lk, 'ADD', nz.outputs['Fac'], math_(N, Lk, 'MULTIPLY', zc, -0.35)), 0.38, 0.62), shape)
        dens = math_(N, Lk, 'MULTIPLY', dn, math_(N, Lk, 'MULTIPLY', bI, 3.0))
        Lk.new(math_(N, Lk, 'MULTIPLY', dens, 0.15), pv.inputs['Density']); pv.inputs['Color'].default_value = (0.2, 0.18, 0.16, 1)
        Lk.new(math_(N, Lk, 'MULTIPLY', dens, 6.0), pv.inputs['Blackbody Intensity'])
        Lk.new(math_(N, Lk, 'ADD', 950.0, math_(N, Lk, 'MULTIPLY', math_(N, Lk, 'SUBTRACT', 1.0, zc), 900.0)), pv.inputs['Temperature'])
    else:
        sb = math_(N, Lk, 'MULTIPLY', smooth(N, Lk, aa, 0.2, 1.5), math_(N, Lk, 'SUBTRACT', 1.0, smooth(N, Lk, aa, 10.0, 30.0)))
        ok = math_(N, Lk, 'GREATER_THAN', ig.outputs['Fac'], -0.5); sb = math_(N, Lk, 'MULTIPLY', sb, ok)
        shape = math_(N, Lk, 'SUBTRACT', 1.0, smooth(N, Lk, r, 0.22, 0.5))
        top = math_(N, Lk, 'SUBTRACT', 1.0, smooth(N, Lk, zc, 0.6, 1.0))
        dn = math_(N, Lk, 'MULTIPLY', math_(N, Lk, 'MULTIPLY', smooth(N, Lk, nz.outputs['Fac'], 0.42, 0.7), shape), top)
        Lk.new(math_(N, Lk, 'MULTIPLY', dn, math_(N, Lk, 'MULTIPLY', sb, 0.05)), pv.inputs['Density']); pv.inputs['Color'].default_value = (0.32, 0.30, 0.28, 1); pv.inputs['Anisotropy'].default_value = 0.35
    Lk.new(pv.outputs[0], o.inputs['Volume']); return m
mL, mS = vol_mat('lua'), vol_mat('khoi')
def box_mesh(name, w, h, lean=0.0):
    V = [(-w / 2, -w / 2, 0), (w / 2, -w / 2, 0), (w / 2, w / 2, 0), (-w / 2, w / 2, 0), (-w / 2 - lean, -w / 2, h), (w / 2 - lean, -w / 2, h), (w / 2 - lean, w / 2, h), (-w / 2 - lean, w / 2, h)]
    Fq = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    me = bpy.data.meshes.new(name); me.from_pydata(V, [], Fq); me.update(); return me
meL = box_mesh('hop-lua', 24, 30); meL.materials.append(mL); meS = box_mesh('hop-khoi', 70, 260, lean=170); meS.materials.append(mS)
nl = 0; lamps = []
for k, (x, y, z, ig) in enumerate(cells):
    for me, kind in ((meL, 'lua'), (meS, 'khoi')):
        if kind == 'khoi' and k % 2: continue
        o_ = bpy.data.objects.new(f'{kind}{k}', me); sc.collection.objects.link(o_); o_.location = B(float(x), float(y), float(z)); o_['ign'] = float(ig); nl += 1
    if k % 2 == 0:
        L_ = bpy.data.lights.new(f'den{k}', 'POINT'); L_.color = (1.0, 0.42, 0.12); L_.shadow_soft_size = 8.0; lo = bpy.data.objects.new(f'den{k}', L_); sc.collection.objects.link(lo); lo.location = B(float(x), float(y) + 12, float(z)); lamps.append((L_, float(ig)))
def burnI(ig, h):
    if h < ig: return 0.0
    a_ = h - ig; ss = lambda e0, e1, x: (lambda t: t * t * (3 - 2 * t))(min(1, max(0, (x - e0) / (e1 - e0))))
    return ss(0, 0.7, a_) * (1 - ss(4, 9, a_))
# ------------------------------------------------ máy, trời, khoá theo khung
camd = bpy.data.cameras.new('cam'); camd.sensor_fit = 'VERTICAL'; camd.clip_start = 2; camd.clip_end = 15000; cam = bpy.data.objects.new('cam', camd); sc.collection.objects.link(cam); sc.camera = cam
tgt = bpy.data.objects.new('dich', None); sc.collection.objects.link(tgt); tk_ = cam.constraints.new('TRACK_TO'); tk_.target = tgt; tk_.track_axis = 'TRACK_NEGATIVE_Z'; tk_.up_axis = 'UP_Y'
sund = bpy.data.lights.new('mattroi', 'SUN'); sund.angle = math.radians(0.6); sun = bpy.data.objects.new('mattroi', sund); sc.collection.objects.link(sun)
W = bpy.data.worlds.new('troi'); sc.world = W; nt, N, Lk = nodes(W); wo = N.new('ShaderNodeOutputWorld'); bg = N.new('ShaderNodeBackground'); sky = N.new('ShaderNodeTexSky')
sky.sky_type = 'NISHITA' if 'NISHITA' in [e.identifier for e in sky.bl_rna.properties['sky_type'].enum_items] else sky.sky_type
mxw = N.new('ShaderNodeMixRGB'); mxw.inputs[2].default_value = (0.0025, 0.003, 0.006, 1); Lk.new(sky.outputs['Color'], mxw.inputs[1]); Lk.new(mxw.outputs[0], bg.inputs['Color']); Lk.new(bg.outputs[0], wo.inputs['Surface'])
sc['gio'] = h0
for f in range(F0, F1 + 1):
    h = hour_at(f); p, l, fov = cam_at(f); sc.frame_set(f)
    sc['gio'] = h; sc.keyframe_insert('["gio"]', frame=f)
    cam.location = B(p[0] - 532000, p[2], -(p[1] - 180800)); cam.keyframe_insert('location', frame=f)
    tgt.location = B(l[0] - 532000, l[2], -(l[1] - 180800)); tgt.keyframe_insert('location', frame=f)
    camd.angle = fov * RAD; camd.keyframe_insert('lens', frame=f)
    el, az = sun_for(h); day = min(1, max(0, (el + 6) / 12))
    sun.rotation_euler = (math.radians(90 - max(el, -5)), 0, math.radians(180 - az)); sun.keyframe_insert('rotation_euler', frame=f)
    sund.energy = 3.2 * day + 0.03 * (1 - day); sund.color = (1, 0.85, 0.7) if day > 0.2 else (0.6, 0.7, 1.0); sund.keyframe_insert('energy', frame=f); sund.keyframe_insert('color', frame=f)
    try:
        sky.sun_elevation = math.radians(max(el, -2)); sky.sun_rotation = math.radians(180 - az); sky.keyframe_insert('sun_elevation', frame=f); sky.keyframe_insert('sun_rotation', frame=f)
    except Exception: pass
    mxw.inputs[0].default_value = 1 - day; mxw.inputs[0].keyframe_insert('default_value', frame=f)
    bg.inputs['Strength'].default_value = 0.35 if day > 0 else 1.0; bg.inputs['Strength'].keyframe_insert('default_value', frame=f)
    for L_, ig in lamps:
        L_.energy = 4.0e6 * burnI(ig, h); L_.keyframe_insert('energy', frame=f)
sc.frame_start, sc.frame_end = F0, F1
print('CY-CANH', json.dumps({'tam_giac': n, 'o_chay': int(len(cells)), 'vat_the_tich': nl, 'den': len(lamps), 'khung': [F0, F1], 'dung_s': round(time.time() - T0, 1), 'dev': DT}), flush=True)
sc.render.filepath = os.path.join(OUT, '#####')
tr0 = time.time(); bpy.ops.render.render(animation=True)
print('CY-XONG', json.dumps({'khung': F1 - F0 + 1, 's_khung': round((time.time() - tr0) / (F1 - F0 + 1), 2), 'res': RES, 'spp': SPP}), flush=True)
