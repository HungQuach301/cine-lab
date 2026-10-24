"""K-1.17.5 · CẢNH TỔNG HỢP có đáp án (Blender, không AI) cho A1 (phản chiếu thật ↔ bờ lấn) và A5 (BE-MAT-NHA: nhà thường đổi hình khối).
Một thành phố ven sông kiểu 1666 dựng THEO HẠT (tất định): dãy nhà khung theo lô/phố, mái hồi/mái hông/mái bằng, một nhà thờ có tháp + cầu + tường
(lớp (a) 'nha'), thuyền ('tau'), dải bãi ('suon'), mặt nước bóng (phản chiếu VẬT LÝ của Cycles, sóng gợn bump). Biến thể = cùng hạt + danh sách
biến đổi (dời / xoá / thêm / gộp nhà, đổi mái, thêm tầng, đổi vật liệu, bờ lấn d m, nước đổi sắc).
Ra: rgb.png (Cycles), cls.png (lớp, bảng màu q_n2p.PAL + 'nha_thuong' 215,215,215), iid.png (mã nhà thường 24 bit: R<<16|G<<8|B, 0 = không),
    nha.json (mỗi nhà: id, lo, tam [x,y,z], px_m (điểm ảnh / mét ngang ở tâm nhà), kieu_mai, bien_doi), may.json (máy).
  /opt/bpy/bin/python canh_tong_hop.py <cfg.json> <thư mục ra>
cfg: {seed, may: 'P1'|'TRUNG', W, H, spp, mat_seed (vật liệu; mặc định = seed), nuoc: {mau: [r,g,b], nham: 0.03, song: 0.15},
      mat_troi: [độ cao°, phương vị°], bien_doi: [{loai: doi|xoa|them|gop|mai|tang|lan, ...}], chi: 'rgb'|'mask'|'ca'}"""
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

cfg = json.load(open(sys.argv[-2])); OUT = sys.argv[-1]; os.makedirs(OUT, exist_ok=True)
SEED = int(cfg.get('seed', 1)); W, H = int(cfg.get('W', 1920)), int(cfg.get('H', 1080)); CHI = cfg.get('chi', 'ca')
BD = cfg.get('bien_doi', [])
PAL = {'troi': (40, 80, 200), 'nuoc': (0, 170, 190), 'bang': (200, 170, 90), 'suon': (150, 120, 70), 'nha': (235, 235, 235), 'tau': (255, 0, 0),
       'congsu': (170, 150, 120), 'nha_thuong': (215, 215, 215), 'cay': (60, 140, 60), 'pho': (255, 200, 220)}
SHORE = 222.0; Z_BANK = 2.5; Z_W = 0.3

# ------------------------------------------------------------------ bố cục nhà (tất định theo SEED)
rng = np.random.default_rng(SEED)
houses = []   # dict(id, lo, x0, y0, x1, y1 (chân), h (mái hiên), kieu: hoi_doc|hoi_ngang|hong|bang, mat (0..), z0)
def add_house(lo, x0, y0, x1, y1, h, kieu, nid=None):
    houses.append(dict(id=nid or len(houses) + 1, lo=lo, x0=x0, y0=y0, x1=x1, y1=y1, h=h, kieu=kieu, z0=Z_BANK, bd=[]))
KIEU = ['hoi_doc', 'hoi_ngang', 'hong', 'bang']; KP = [0.62, 0.23, 0.08, 0.07]
lo = 0
# dãy ven sông bờ bắc: nhà sát mép nước ở các đoạn, bãi 'suon' ở đoạn khác
bai = [(-560, -420), (-150, -30), (180, 260), (430, 560)]
def tren_bai(x): return any(a <= x <= b for a, b in bai)
for bx in np.arange(-700, 700, 70.0):
    lo += 1; x = bx + 2
    while x < bx + 66:
        w = float(rng.uniform(5, 9)); d = float(rng.uniform(9, 13)); h = float(rng.uniform(7, 12)); k = str(rng.choice(KIEU, p=KP))
        x1 = min(x + w, bx + 68)
        if not tren_bai((x + x1) / 2): add_house(lo, x, SHORE + 0.5, x1, SHORE + 0.5 + d, h, k)
        else: rng.uniform();
        x = x1
# các khối phố bờ bắc: phố song song sông mỗi 44 m, phố cắt mỗi 70 m; nhà theo hai mặt phố của khối
for by in np.arange(SHORE + 22, 1300, 44.0):
    for bx in np.arange(-700, 700, 70.0):
        lo += 1
        for mat, (ya, yb) in enumerate(((by + 1, None), (by + 39, None))):
            x = bx + 3
            while x < bx + 64:
                w = float(rng.uniform(5, 9)); d = float(rng.uniform(9, 14)); h = float(rng.uniform(7, 13)); k = str(rng.choice(KIEU, p=KP))
                x1 = min(x + w, bx + 66)
                if rng.uniform() > 0.06:   # khoảng trống (sân/vườn) 6 %
                    if mat == 0: add_house(lo, x, ya, x1, ya + d, h, k)
                    else: add_house(lo, x, ya - d, x1, ya, h, k)
                x = x1
# bờ nam (tiền cảnh) một dải nhà
for bx in np.arange(-600, 600, 70.0):
    lo += 1; x = bx + 2
    while x < bx + 66:
        w = float(rng.uniform(5, 9)); d = float(rng.uniform(9, 13)); h = float(rng.uniform(7, 11)); k = str(rng.choice(KIEU, p=KP))
        x1 = min(x + w, bx + 68); add_house(lo, x, -14 - d, x1, -14, h, k); x = x1
NHA_THO = dict(x0=-260, y0=420, x1=-200, y1=446, h=24, thap=(-275, 425, -263, 437, 62))

# ------------------------------------------------------------------ biến đổi (đáp án)
by_id = {hh['id']: hh for hh in houses}
mat_seed = int(cfg.get('mat_seed', SEED))
for b in BD:
    t = b['loai']
    if t == 'doi':
        hh = by_id[b['id']]; dx, dy = float(b.get('dx', 0)), float(b.get('dy', 0))
        for k_, v in (('x0', dx), ('x1', dx), ('y0', dy), ('y1', dy)): hh[k_] += v
        hh['bd'].append(dict(b))
    elif t == 'xoa': by_id[b['id']]['xoa'] = True; by_id[b['id']]['bd'].append(dict(b))
    elif t == 'mai': hh = by_id[b['id']]; hh['bd'].append(dict(b, cu=hh['kieu'])); hh['kieu'] = b['kieu']
    elif t == 'tang': hh = by_id[b['id']]; hh['h'] += float(b.get('dh', 3.0)); hh['bd'].append(dict(b))
    elif t == 'gop':
        a, c = by_id[b['ids'][0]], by_id[b['ids'][1]]
        a['bd'].append(dict(b)); c['bd'].append(dict(b)); c['xoa'] = True
        a['x0'], a['x1'] = min(a['x0'], c['x0']), max(a['x1'], c['x1']); a['y0'], a['y1'] = min(a['y0'], c['y0']), max(a['y1'], c['y1'])
        a['h'] = max(a['h'], c['h']); a['kieu'] = 'hoi_doc'; a['gop'] = c['id']
    elif t == 'them':
        nid = 900000 + len([x for x in houses if x['id'] >= 900000]) + 1
        add_house(-1, float(b['x0']), float(b['y0']), float(b['x0']) + float(b.get('w', 7)), float(b['y0']) + float(b.get('d', 11)), float(b.get('h', 10)),
                  b.get('kieu', 'hoi_doc'), nid=nid); houses[-1]['bd'].append(dict(b)); houses[-1]['them'] = True

# ------------------------------------------------------------------ màu vật liệu (đổi theo mat_seed = biến thể "bề mặt mới")
mr = np.random.default_rng(mat_seed * 7919 + 13)
TUONG = [(0.78, 0.74, 0.64), (0.85, 0.82, 0.74), (0.55, 0.42, 0.30), (0.62, 0.36, 0.26), (0.70, 0.64, 0.52), (0.45, 0.33, 0.24)]
MAI = [(0.42, 0.20, 0.13), (0.50, 0.27, 0.17), (0.33, 0.30, 0.30), (0.38, 0.24, 0.17), (0.28, 0.25, 0.24), (0.55, 0.33, 0.22)]
if cfg.get('bang_mau') == 'khac':   # bề mặt "AI" khác hẳn: tông lạnh/ấm khác, cùng hình khối
    TUONG = [(0.60, 0.58, 0.55), (0.72, 0.66, 0.50), (0.40, 0.35, 0.32), (0.66, 0.50, 0.40), (0.82, 0.78, 0.70)]
    MAI = [(0.22, 0.22, 0.24), (0.36, 0.18, 0.12), (0.30, 0.28, 0.22), (0.48, 0.40, 0.30)]
for hh in houses:
    hh['c_tuong'] = TUONG[int(mr.integers(len(TUONG)))]; hh['c_mai'] = MAI[int(mr.integers(len(MAI)))]
    hh['van'] = float(mr.uniform(0.2, 1.0))

# ------------------------------------------------------------------ lưới
V, F, FC, FK, FI, FT = [], [], [], [], [], []   # đỉnh, mặt, màu albedo, lớp, mã nhà, vân
def poly(pts, col, cls, iid=0, van=0.0):
    i0 = len(V); V.extend(pts); F.append(tuple(range(i0, i0 + len(pts)))); FC.append(col); FK.append(cls); FI.append(iid); FT.append(van)
def box(x0, y0, x1, y1, z0, z1, col, cls, iid=0, van=0.0, top=True):
    p = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    q = lambda *ix: [p[i] for i in ix]
    poly(q(0, 1, 5, 4), col, cls, iid, van); poly(q(1, 2, 6, 5), col, cls, iid, van); poly(q(2, 3, 7, 6), col, cls, iid, van); poly(q(3, 0, 4, 7), col, cls, iid, van)
    if top: poly(q(4, 5, 6, 7), col, cls, iid, van)
def house_mesh(hh):
    x0, y0, x1, y1, z0, h = hh['x0'], hh['y0'], hh['x1'], hh['y1'], hh['z0'], hh['h']; zt = z0 + h; ct, cm, iid, van = hh['c_tuong'], hh['c_mai'], hh['id'], hh['van']
    cls = 'nha_thuong'
    k = hh['kieu']
    if k == 'bang':
        box(x0, y0, x1, y1, z0, zt, ct, cls, iid, van, top=False); poly([(x0, y0, zt), (x1, y0, zt), (x1, y1, zt), (x0, y1, zt)], cm, cls, iid, van); return
    box(x0, y0, x1, y1, z0, zt, ct, cls, iid, van, top=False)
    if k == 'hoi_doc':      # nóc song song trục x (mặt phố)
        r = 0.5 * (y1 - y0) * 0.9; ym = 0.5 * (y0 + y1)
        poly([(x0, y0, zt), (x1, y0, zt), (x1, ym, zt + r), (x0, ym, zt + r)], cm, cls, iid, van); poly([(x1, y1, zt), (x0, y1, zt), (x0, ym, zt + r), (x1, ym, zt + r)], cm, cls, iid, van)
        poly([(x0, y0, zt), (x0, ym, zt + r), (x0, y1, zt)], ct, cls, iid, van); poly([(x1, y1, zt), (x1, ym, zt + r), (x1, y0, zt)], ct, cls, iid, van)
    elif k == 'hoi_ngang':  # nóc song song trục y (đầu hồi ra phố)
        r = 0.5 * (x1 - x0) * 1.0; xm = 0.5 * (x0 + x1)
        poly([(x1, y0, zt), (x1, y1, zt), (xm, y1, zt + r), (xm, y0, zt + r)], cm, cls, iid, van); poly([(x0, y1, zt), (x0, y0, zt), (xm, y0, zt + r), (xm, y1, zt + r)], cm, cls, iid, van)
        poly([(x0, y0, zt), (x1, y0, zt), (xm, y0, zt + r)], ct, cls, iid, van); poly([(x1, y1, zt), (x0, y1, zt), (xm, y1, zt + r)], ct, cls, iid, van)
    else:                   # mái hông (4 mặt dốc)
        s = min(x1 - x0, y1 - y0); r = 0.45 * s; ym = 0.5 * (y0 + y1); i = 0.5 * s
        a, b = (x0 + i, ym, zt + r), (x1 - i, ym, zt + r)
        if a[0] > b[0]: a = b = (0.5 * (x0 + x1), ym, zt + r)
        poly([(x0, y0, zt), (x1, y0, zt), b, a], cm, cls, iid, van); poly([(x1, y1, zt), (x0, y1, zt), a, b], cm, cls, iid, van)
        poly([(x0, y1, zt), (x0, y0, zt), a], cm, cls, iid, van); poly([(x1, y0, zt), (x1, y1, zt), b], cm, cls, iid, van)
for hh in houses:
    if not hh.get('xoa'): house_mesh(hh)
# đất, bãi, phố
poly([(-2500, SHORE + 0.0, Z_BANK), (2500, SHORE, Z_BANK), (2500, 3000, Z_BANK), (-2500, 3000, Z_BANK)], (0.48, 0.42, 0.33), 'bang')
for a, b in bai: poly([(a, SHORE - 0.4, Z_BANK + 0.01), (b, SHORE - 0.4, Z_BANK + 0.01), (b, SHORE + 13, Z_BANK + 0.01), (a, SHORE + 13, Z_BANK + 0.01)], (0.62, 0.55, 0.42), 'suon')
poly([(-2500, -3000, Z_BANK), (2500, -3000, Z_BANK), (2500, -6, Z_BANK), (-2500, -6, Z_BANK)], (0.46, 0.41, 0.32), 'bang')
# bờ dốc (kè) hai bờ: dải đứng từ nước lên mặt đất
poly([(-2500, SHORE - 0.4, Z_W - 0.5), (2500, SHORE - 0.4, Z_W - 0.5), (2500, SHORE - 0.4, Z_BANK), (-2500, SHORE - 0.4, Z_BANK)], (0.35, 0.31, 0.25), 'suon')
poly([(2500, -6, Z_W - 0.5), (-2500, -6, Z_W - 0.5), (-2500, -6, Z_BANK), (2500, -6, Z_BANK)], (0.35, 0.31, 0.25), 'suon')
# lớp (a): nhà thờ + tháp, cầu, tường thành, thuyền
nt = NHA_THO; box(nt['x0'], nt['y0'], nt['x1'], nt['y1'], Z_BANK, Z_BANK + nt['h'], (0.80, 0.78, 0.72), 'nha'); tx = nt['thap']
box(tx[0], tx[1], tx[2], tx[3], Z_BANK, Z_BANK + tx[4], (0.78, 0.76, 0.70), 'nha')
box(300, -6, 312, SHORE, 7.5, 9.0, (0.60, 0.55, 0.48), 'nha')
for py in np.arange(10, SHORE, 30.0): box(301, py, 311, py + 5, Z_W - 0.5, 7.5, (0.55, 0.50, 0.44), 'nha')
box(-700, 1180, 700, 1186, Z_BANK, Z_BANK + 9, (0.58, 0.55, 0.50), 'nha')
for i, (bx_, by_) in enumerate([(-80, 120), (60, 60), (150, 170), (-350, 90), (500, 140)]):
    box(bx_, by_, bx_ + 9, by_ + 3, Z_W - 0.2, Z_W + 1.4, (0.30, 0.22, 0.16), 'tau')
# bờ lấn (đáp án A1): khối bãi/bến đất lấn vào nước, mép răng cưa
for b in BD:
    if b['loai'] != 'lan': continue
    x0, x1, d = float(b['x0']), float(b['x1']), float(b['sau_m']); col = tuple(b.get('mau', (0.62, 0.55, 0.42)))
    n = max(2, int((x1 - x0) / 3)); lr = np.random.default_rng(int(x0 * 10) % 9973)
    xs = np.linspace(x0, x1, n + 1); ds = d * (1 + 0.15 * lr.uniform(-1, 1, n + 1)); ds[0] = ds[-1] = 0.3 * d
    pts = [(xs[0], SHORE + 0.2, Z_W + 0.5)] + [(xs[i], SHORE - ds[i], Z_W + 0.5) for i in range(n + 1)] + [(xs[-1], SHORE + 0.2, Z_W + 0.5)]
    poly(pts, col, 'suon')
# nước
poly([(-3000, -6.5, Z_W), (3000, -6.5, Z_W), (3000, SHORE + 0.5, Z_W), (-3000, SHORE + 0.5, Z_W)], tuple(cfg.get('nuoc', {}).get('mau', (0.10, 0.20, 0.24))), 'nuoc')

me = bpy.data.meshes.new('canh'); me.from_pydata(V, [], F); me.update()
nl = np.array([len(f) for f in F]); fi = np.repeat(np.arange(len(F)), nl)
def cattr(name, vals, typ='FLOAT_COLOR'):
    a = me.color_attributes.new(name, typ, 'CORNER'); arr = np.asarray(vals, np.float32)[fi]
    a.data.foreach_set('color_srgb' if typ == 'BYTE_COLOR' else 'color', np.concatenate([arr, np.ones((len(arr), 1), np.float32)], 1).ravel()); return a
cattr('alb', FC)
cattr('cls', [tuple(c / 255 for c in PAL[k]) for k in FK], 'BYTE_COLOR')
cattr('iid', [((i >> 16) / 255, ((i >> 8) & 255) / 255, (i & 255) / 255) for i in FI], 'BYTE_COLOR')
PI = [(j + 1 if FK[j] == 'nha_thuong' else 0) for j in range(len(F))]   # mã MẶT PHẲNG (mỗi mặt lưới nhà thường một mã) — biên mặt phẳng = sống/hông/mép mái, góc tường
cattr('pid', [((i >> 16) / 255, ((i >> 8) & 255) / 255, (i & 255) / 255) for i in PI], 'BYTE_COLOR')
va = me.attributes.new('van', 'FLOAT', 'CORNER'); va.data.foreach_set('value', np.asarray(FT, np.float32)[fi])
isw = me.attributes.new('nuoc', 'FLOAT', 'CORNER'); isw.data.foreach_set('value', (np.array([k == 'nuoc' for k in FK], np.float32))[fi])
for o in list(bpy.data.objects): bpy.data.objects.remove(o)
ob = bpy.data.objects.new('canh', me)
sc = bpy.context.scene; sc.collection.objects.link(ob)

# ------------------------------------------------------------------ vật liệu Cycles: albedo theo thuộc tính + vân nhiễu; nước bóng có gợn
nuoc = cfg.get('nuoc', {})
m = bpy.data.materials.new('m'); m.use_nodes = True; nt_ = m.node_tree; N = nt_.nodes; Lk = nt_.links
bs = N['Principled BSDF']; at = N.new('ShaderNodeAttribute'); at.attribute_name = 'alb'
aw = N.new('ShaderNodeAttribute'); aw.attribute_name = 'nuoc'; av = N.new('ShaderNodeAttribute'); av.attribute_name = 'van'
nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 0.9; nz.inputs['Detail'].default_value = 6.0
mix = N.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.blend_type = 'MULTIPLY'
mul = N.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = 0.55
Lk.new(av.outputs['Fac'], mul.inputs[0]); Lk.new(mul.outputs[0], mix.inputs['Factor'])
Lk.new(at.outputs['Color'], mix.inputs['A']); Lk.new(nz.outputs['Color'], mix.inputs['B'])
rough = N.new('ShaderNodeMix'); rough.data_type = 'FLOAT'; rough.inputs['A'].default_value = 0.85; rough.inputs['B'].default_value = float(nuoc.get('nham', 0.035))
Lk.new(aw.outputs['Fac'], rough.inputs['Factor']); Lk.new(rough.outputs['Result'], bs.inputs['Roughness'])
Lk.new(mix.outputs['Result'], bs.inputs['Base Color'])
wn = N.new('ShaderNodeTexWave'); wn.inputs['Scale'].default_value = 0.08; wn.inputs['Distortion'].default_value = 6.0
bp = N.new('ShaderNodeBump'); bs2 = N.new('ShaderNodeMath'); bs2.operation = 'MULTIPLY'; bs2.inputs[1].default_value = float(nuoc.get('song', 0.12))
Lk.new(aw.outputs['Fac'], bs2.inputs[0]); Lk.new(bs2.outputs[0], bp.inputs['Strength']); Lk.new(wn.outputs['Color'], bp.inputs['Height']); Lk.new(bp.outputs['Normal'], bs.inputs['Normal'])
ob.data.materials.append(m)

# ------------------------------------------------------------------ trời, nắng, máy
MAY = {'P1': dict(p=(0, -700, 230), l=(0, 520, 0), fov=50.0), 'TRUNG': dict(p=(-60, -160, 105), l=(-40, 430, 0), fov=50.0)}[cfg.get('may', 'P1')]
cam_d = bpy.data.cameras.new('cam'); cam_d.lens_unit = 'FOV'; cam_d.sensor_fit = 'HORIZONTAL'; cam_d.angle = math.radians(MAY['fov']); cam_d.clip_end = 8000
cam = bpy.data.objects.new('cam', cam_d); sc.collection.objects.link(cam); sc.camera = cam
cam.location = MAY['p']; d = Vector(MAY['l']) - Vector(MAY['p']); cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
el, az = cfg.get('mat_troi', [32.0, 215.0])
sun_d = bpy.data.lights.new('sun', 'SUN'); sun_d.energy = 4.0; sun_d.angle = math.radians(1.0); sun = bpy.data.objects.new('sun', sun_d); sc.collection.objects.link(sun)
sun.rotation_euler = (math.radians(90 - el), 0, math.radians(az))
wd = bpy.data.worlds.new('w'); sc.world = wd; wd.use_nodes = True
bg = wd.node_tree.nodes['Background']; tc = wd.node_tree.nodes.new('ShaderNodeTexCoord'); sep = wd.node_tree.nodes.new('ShaderNodeSeparateXYZ')
cr = wd.node_tree.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = (0.75, 0.80, 0.86, 1); cr.color_ramp.elements[1].color = (0.30, 0.45, 0.72, 1)
wd.node_tree.links.new(tc.outputs['Generated'], sep.inputs[0]); wd.node_tree.links.new(sep.outputs['Z'], cr.inputs[0]); wd.node_tree.links.new(cr.outputs['Color'], bg.inputs['Color'])
bg.inputs['Strength'].default_value = 1.0
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = W, H, 100
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGB'

# ------------------------------------------------------------------ nhà: tâm, px/m, vùng thấy (tính ở bước đo)
def px(pw):
    v = world_to_camera_view(sc, cam, Vector(pw)); return (v.x * W, (1 - v.y) * H, v.z)
right = (cam.matrix_world.to_3x3() @ Vector((1, 0, 0))).normalized()
rec = []
for hh in houses:
    if hh.get('xoa') and not hh['bd']: continue
    c = (0.5 * (hh['x0'] + hh['x1']), 0.5 * (hh['y0'] + hh['y1']), hh['z0'] + 0.5 * hh['h'])
    a, b = px(c), px(tuple(Vector(c) + right))
    rec.append(dict(id=hh['id'], lo=hh['lo'], tam=[round(v, 2) for v in c], tam_px=[round(a[0], 1), round(a[1], 1)], sau_m=round(a[2], 1),
                    px_m=round(math.hypot(b[0] - a[0], b[1] - a[1]), 3), kieu_mai=hh['kieu'], rong=round(hh['x1'] - hh['x0'], 2), sau=round(hh['y1'] - hh['y0'], 2),
                    cao=round(hh['h'], 2), xoa=bool(hh.get('xoa')), them=bool(hh.get('them')), gop=hh.get('gop'), bien_doi=hh['bd']))
json.dump(dict(cfg=cfg, nha=rec, may=MAY, W=W, H=H), open(os.path.join(OUT, 'nha.json'), 'w'), ensure_ascii=False)

# ------------------------------------------------------------------ dựng
if CHI in ('ca', 'mask'):
    sc.render.engine = 'BLENDER_WORKBENCH'; sh = sc.display.shading; sh.light = 'FLAT'; sh.color_type = 'VERTEX'
    sc.display.render_aa = 'OFF'; sc.render.dither_intensity = 0.0; sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'
    sc.view_settings.exposure = 0; sc.view_settings.gamma = 1
    sh.background_type = 'VIEWPORT'; sh.background_color = tuple(c / 255 for c in PAL['troi'])
    for nm in ('cls', 'iid', 'pid'):
        me.color_attributes.active_color = me.color_attributes[nm]; me.color_attributes.render_color_index = me.color_attributes.find(nm)
        sc.render.filepath = os.path.join(OUT, f'{nm}.png'); bpy.ops.render.render(write_still=True)
if CHI in ('ca', 'rgb'):
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = int(cfg.get('spp', 32)); sc.cycles.use_denoising = True
    sc.cycles.max_bounces = 4; sc.view_settings.view_transform = 'AgX' if 'AgX' in [x.identifier for x in sc.view_settings.bl_rna.properties['view_transform'].enum_items] else 'Filmic'
    sc.render.film_transparent = False; sc.render.filepath = os.path.join(OUT, 'rgb.png'); bpy.ops.render.render(write_still=True)
print('XONG', OUT, len(F), 'mặt', len(rec), 'nhà')
