"""PT · lớp sống — hình người THỦ TỤC tầm xa (≥ 10 m; không mặt chi tiết, không người ngã), trang phục theo bảng màu thời kỳ.
Không có bộ người CC0 kiểu tả thực hợp thời kỳ (Quaternius/Kenney: phong cách hoạt hình) → dựng từ khối cơ bản trong Blender.
Mỗi lượt chiếu sáng dựng MỘT tờ sprite (máy trực giao cùng hướng + cùng góc cúi với máy neo, mặt trời y hệt lượt nền,
mặt phẳng bắt bóng → bóng đổ thật trong kênh alpha).
  /opt/bpy/bin/python design/pt/scene/people.py --epoch 1782 --passes d1,d2,d3,d4,n --out DIR"""
import bpy, math, sys, os, json, argparse, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import pt_site as S
ap = argparse.ArgumentParser(); ap.add_argument('--epoch', type=int, required=True); ap.add_argument('--passes', default='d2'); ap.add_argument('--out', required=True)
ap.add_argument('--spp', type=int, default=24)
A = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]); os.makedirs(A.out, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene; EP = A.epoch

def mat(name, col, rough=0.75):
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = rough; return m

def prim(kind, loc, scale, col, rot=(0, 0, 0), parent=None, name='p'):
    if kind == 'cyl': bpy.ops.mesh.primitive_cylinder_add(vertices=14, radius=1, depth=2, location=loc, rotation=rot)
    elif kind == 'sph': bpy.ops.mesh.primitive_uv_sphere_add(segments=14, ring_count=8, radius=1, location=loc, rotation=rot)
    elif kind == 'cone': bpy.ops.mesh.primitive_cone_add(vertices=14, radius1=1, radius2=0.7, depth=2, location=loc, rotation=rot)
    else: bpy.ops.mesh.primitive_cube_add(size=2, location=loc, rotation=rot)
    o = bpy.context.object; o.scale = scale; o.data.materials.append(mat(col[0], col[1])); o.parent = parent
    for p in o.data.polygons: p.use_smooth = True
    return o

SKIN = [('da1', (0.72, 0.52, 0.4)), ('da2', (0.58, 0.4, 0.3)), ('da3', (0.8, 0.62, 0.5))]
# bảng trang phục thời kỳ (màu tham chiếu: quân phục bộ binh Anh 1780s áo đỏ + đai chéo trắng, mũ ba góc; 1943: kaki, hải quân xanh đậm/trắng, RAF xám xanh)
if EP == 1782:
    ROLES = {
        'linh':   dict(coat=('ao_do', (0.55, 0.06, 0.05)), legs=('quan_trang', (0.82, 0.8, 0.72)), gait=('xa_cap', (0.05, 0.05, 0.05)), hat='tricorn', belts=True, musket=True, tails=True),
        'linh2':  dict(coat=('ao_do', (0.55, 0.06, 0.05)), legs=('quan_trang', (0.82, 0.8, 0.72)), gait=('xa_cap', (0.05, 0.05, 0.05)), hat='tricorn', belts=True, musket=False, tails=True),
        'phao_binh': dict(coat=('ao_xanh_dam', (0.08, 0.1, 0.2)), legs=('quan_trang', (0.82, 0.8, 0.72)), gait=('xa_cap', (0.05, 0.05, 0.05)), hat='tricorn', belts=True, musket=False, tails=True),
        'dan_nam': dict(coat=('ao_nau', (0.32, 0.22, 0.14)), legs=('quan_nau', (0.25, 0.2, 0.15)), gait=('giay', (0.12, 0.08, 0.05)), hat='cap', belts=False, musket=False, tails=False),
        'dan_nu':  dict(coat=('ao_nu', (0.45, 0.38, 0.3)), legs=('vay', (0.2, 0.18, 0.22)), gait=('giay', (0.12, 0.08, 0.05)), hat='scarf', skirt=True, belts=False, musket=False, tails=False),
        'thuy_thu': dict(coat=('ao_xanh', (0.12, 0.15, 0.3)), legs=('quan_trang2', (0.75, 0.72, 0.62)), gait=('giay', (0.1, 0.08, 0.05)), hat='round', belts=False, musket=False, tails=False),
    }
else:
    ROLES = {
        'linh':   dict(coat=('kaki', (0.36, 0.3, 0.19)), legs=('kaki', (0.36, 0.3, 0.19)), gait=('giay_den', (0.05, 0.05, 0.05)), hat='helmet', belts=True, musket=True, tails=False),
        'linh2':  dict(coat=('kaki', (0.36, 0.3, 0.19)), legs=('kaki', (0.36, 0.3, 0.19)), gait=('giay_den', (0.05, 0.05, 0.05)), hat='beret', belts=False, musket=False, tails=False),
        'thuy_thu': dict(coat=('hq_xanh', (0.05, 0.06, 0.12)), legs=('hq_xanh', (0.05, 0.06, 0.12)), gait=('giay_den', (0.05, 0.05, 0.05)), hat='sailor', belts=False, musket=False, tails=False),
        'thuy_thu_trang': dict(coat=('hq_trang', (0.85, 0.85, 0.82)), legs=('hq_trang', (0.85, 0.85, 0.82)), gait=('giay_den', (0.05, 0.05, 0.05)), hat='sailor', belts=False, musket=False, tails=False),
        'raf':    dict(coat=('raf', (0.24, 0.29, 0.38)), legs=('raf', (0.24, 0.29, 0.38)), gait=('giay_den', (0.05, 0.05, 0.05)), hat='sidecap', belts=False, musket=False, tails=False),
        'tho':    dict(coat=('ao_xam', (0.4, 0.4, 0.38)), legs=('quan_xanh', (0.15, 0.17, 0.22)), gait=('giay', (0.1, 0.08, 0.05)), hat='cap', belts=False, musket=False, tails=False),
    }

def figure(role, x, y, face, walk, rng):
    """người cao ~1,72 m, chân tại (x, y, 0); face = góc quay (rad) quanh Z (0 = nhìn +Y)."""
    R = ROLES[role]; root = bpy.data.objects.new('root', None); sc.collection.objects.link(root); root.location = (x, y, 0); root.rotation_euler = (0, 0, face)
    sk = rng.choice(SKIN); h = rng.uniform(0.95, 1.04)
    st = 0.18 if walk else 0.0
    if R.get('skirt'):
        prim('cone', (0, 0, 0.45 * h), (0.27, 0.27, 0.45 * h), R['legs'], parent=root)
    else:
        for s in (-1, 1):
            prim('cyl', (0.1 * s, st * s, 0.44 * h), (0.07, 0.07, 0.44 * h), R['legs'], rot=(st * s * 1.2, 0, 0), parent=root)
            prim('cyl', (0.1 * s, st * s * 1.6, 0.13), (0.075, 0.075, 0.13), R['gait'], rot=(st * s * 1.2, 0, 0), parent=root)
    prim('cyl', (0, 0, 1.15 * h), (0.19, 0.13, 0.3 * h), R['coat'], parent=root)
    if R.get('tails'): prim('cube', (0, -0.08, 0.78 * h), (0.16, 0.04, 0.16), R['coat'], rot=(0.15, 0, 0), parent=root)
    if R.get('belts'):
        for s in (-1, 1): prim('cube', (0, 0.13, 1.15 * h), (0.025, 0.012, 0.3), ('trang', (0.9, 0.88, 0.82)), rot=(0, 0.55 * s, 0), parent=root)
    for s in (-1, 1):
        prim('cyl', (0.25 * s, -st * s * 0.8, 1.13 * h), (0.055, 0.055, 0.29 * h), R['coat'], rot=(-st * s, 0.08 * s, 0), parent=root)
        prim('sph', (0.27 * s, -st * s * 1.4, 0.84 * h), (0.045, 0.045, 0.05), sk, parent=root)
    prim('cyl', (0, 0, 1.47 * h), (0.05, 0.05, 0.05), sk, parent=root)
    prim('sph', (0, 0, 1.6 * h), (0.095, 0.105, 0.115), sk, parent=root)
    hat = R['hat']; hz = 1.71 * h
    if hat == 'tricorn':
        for k in range(3): prim('cube', (0, 0, hz), (0.17, 0.05, 0.035), ('mu_den', (0.04, 0.04, 0.04)), rot=(0, 0, k * 2.094), parent=root)
        prim('cyl', (0, 0, hz + 0.03), (0.1, 0.1, 0.04), ('mu_den', (0.04, 0.04, 0.04)), parent=root)
    elif hat == 'helmet':
        prim('cyl', (0, 0, hz - 0.02), (0.17, 0.17, 0.012), ('mu_kaki', (0.3, 0.3, 0.2)), parent=root); prim('sph', (0, 0, hz), (0.11, 0.11, 0.06), ('mu_kaki', (0.3, 0.3, 0.2)), parent=root)
    elif hat == 'beret':
        prim('sph', (0.02, 0, hz - 0.02), (0.11, 0.11, 0.035), ('mu_beret', (0.08, 0.08, 0.08)), parent=root)
    elif hat == 'sailor':
        prim('cyl', (0, 0, hz - 0.02), (0.11, 0.11, 0.035), ('mu_trang', (0.92, 0.92, 0.9)), parent=root)
    elif hat == 'sidecap':
        prim('cube', (0, 0, hz - 0.03), (0.05, 0.11, 0.035), R['coat'], parent=root)
    elif hat == 'cap':
        prim('cyl', (0, 0.02, hz - 0.03), (0.105, 0.11, 0.03), ('mu_vai', (0.2, 0.18, 0.16)), parent=root)
    elif hat == 'scarf':
        prim('sph', (0, -0.01, 1.62 * h), (0.11, 0.12, 0.12), ('khan', (0.6, 0.55, 0.45)), parent=root)
    elif hat == 'round':
        prim('cyl', (0, 0, hz - 0.01), (0.15, 0.15, 0.012), ('mu_den', (0.04, 0.04, 0.04)), parent=root); prim('cyl', (0, 0, hz + 0.04), (0.09, 0.09, 0.05), ('mu_den', (0.04, 0.04, 0.04)), parent=root)
    if R.get('musket'):
        prim('cyl', (0.22, 0.05, 1.3 * h), (0.018, 0.018, 0.75), ('sung', (0.15, 0.1, 0.06)), rot=(0.12, 0, 0), parent=root)
    return root

# tờ sprite: lưới vai × hướng (mặt về máy, sang trái, sang phải, lưng) × (đứng, bước)
roles = list(ROLES); faces = [('mat', 0.0), ('trai', math.pi / 2), ('phai', -math.pi / 2), ('lung', math.pi)]
CELL = 2.2; rng = random.Random(EP)
cells = []
for i, r in enumerate(roles):
    for j, (fn, fa) in enumerate(faces):
        for k, walk in enumerate((False, True)):
            x = (j * 2 + k) * CELL; y = 0; zrow = -i * 2.6
            # máy trực giao nhìn theo hướng máy neo → quay cả lưới theo hướng đó; "mặt về máy" = quay 180° so với hướng nhìn
            cells.append({'role': r, 'face': fn, 'walk': walk, 'gx': j * 2 + k, 'gy': i})
cols, rows = 8, len(roles); ROWD = 19.0   # khoảng sâu giữa hai hàng (máy cúi 8° → cách nhau ~2,6 m trên ảnh)
head = math.radians(S.CAM_HEAD); pitch = math.radians(-8.0)
fx, fy = math.sin(head), math.cos(head); rx, ry = math.cos(head), -math.sin(head)   # hướng nhìn, phải
for c in cells:
    u = (c['gx'] - (cols - 1) / 2) * CELL; v = (c['gy']) * ROWD
    px, py = rx * u + fx * v, ry * u + fy * v
    face = {'mat': math.pi, 'trai': math.pi / 2, 'phai': -math.pi / 2, 'lung': 0.0}[c['face']] - head
    c['root'] = figure(c['role'], px, py, face, c['walk'], rng).name
# máy trực giao
cam = bpy.data.cameras.new('c'); cam.type = 'ORTHO'; PXM = 60   # điểm ảnh / m
W = int(cols * CELL * PXM); H = int((rows * ROWD * math.sin(abs(pitch)) + 2.6 * math.cos(pitch)) * PXM) + 40
cam.ortho_scale = max(W, H) / PXM
co = bpy.data.objects.new('c', cam); sc.collection.objects.link(co); sc.camera = co
cv = (rows - 1) * ROWD / 2
co.location = (fx * (cv - 60 * math.cos(pitch)), fy * (cv - 60 * math.cos(pitch)), 0.9 + 60 * math.sin(-pitch))
co.rotation_euler = (math.radians(90) + pitch, 0, -head)
sc.render.resolution_x, sc.render.resolution_y = W, H
bpy.ops.mesh.primitive_plane_add(size=400, location=(0, 0, 0)); gp = bpy.context.object; gp.is_shadow_catcher = True
sc.render.film_transparent = True
sun = bpy.data.objects.new('sun', bpy.data.lights.new('sun', 'SUN')); sc.collection.objects.link(sun)
world = bpy.data.worlds.new('w'); sc.world = world; world.use_nodes = True; bgn = world.node_tree.nodes['Background']
LAT = math.radians(36.14); DECL = math.radians(4.0)
def sun_at(hour):
    Hh = math.radians((hour - 12) * 15)
    alt = math.asin(math.sin(LAT) * math.sin(DECL) + math.cos(LAT) * math.cos(DECL) * math.cos(Hh))
    az = math.atan2(math.sin(Hh), math.cos(Hh) * math.sin(LAT) - math.tan(DECL) * math.cos(LAT)) + math.pi
    return math.degrees(alt), math.degrees(az) % 360
PASSES = json.load(open(os.path.join(HERE, 'passes.json')))
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = A.spp; sc.cycles.use_denoising = True
sc.view_settings.view_transform = 'AgX'; sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
meta = {'epoch': EP, 'cells': [{k: v for k, v in c.items() if k != 'root'} for c in cells], 'cols': cols, 'rows': rows, 'W': W, 'H': H, 'pxm': PXM,
        'pitch_deg': -8.0, 'passes': {}}
# toạ độ điểm ảnh chân mỗi ô (chiếu điểm gốc) — tính bằng world_to_camera_view
from bpy_extras.object_utils import world_to_camera_view
bpy.context.view_layer.update()
for c, cm in zip(cells, meta['cells']):
    o = bpy.data.objects[c['root']]; p = world_to_camera_view(sc, co, o.matrix_world.translation)
    cm['foot_px'] = [round(p.x * W, 1), round((1 - p.y) * H, 1)]
for p in A.passes.split(','):
    hr = PASSES[p]
    if hr is None:
        alt, az = 38.0, 235.0; sun.data.energy = 0.08; sun.data.color = (0.62, 0.72, 1.0); bgn.inputs[0].default_value = (0.004, 0.006, 0.012, 1)
    else:
        alt, az = sun_at(hr); warm = max(0.0, min(1.0, (20 - alt) / 20))
        sun.data.energy = 4.2 if alt > 12 else 2.0 + 2.2 * max(0, alt) / 12; sun.data.color = (1.0, 1.0 - 0.4 * warm, 1.0 - 0.7 * warm)
        bgn.inputs[0].default_value = (0.45, 0.55, 0.75, 1) if alt > 12 else (0.35, 0.33, 0.4, 1); bgn.inputs[1].default_value = 0.35
    sun.rotation_euler = (math.radians(90 - alt), 0, math.radians(-az + 180)); sun.data.angle = math.radians(1.5)
    sc.render.filepath = os.path.join(A.out, f'sprites_{p}.png'); bpy.ops.render.render(write_still=True)
    meta['passes'][p] = {'sun_alt': round(alt, 2), 'sun_az': round(az, 2)}
json.dump(meta, open(os.path.join(A.out, 'sprites.json'), 'w'), indent=1, ensure_ascii=False)
print('DONE sprites', W, H)
