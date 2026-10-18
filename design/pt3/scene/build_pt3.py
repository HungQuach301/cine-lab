"""PT3 · VÂN NƯỚNG (HC7) + TẤM CHIẾU (HC8) — dựng cảnh Blender cho MÁY CHUYỂN ĐỘNG (bay dọc phố 1943 / orbit King's Bastion 1782).
Bản sao có sửa từ design/pt/scene/build_scene.py @7adb88f (PT, 17/10) — KHÔNG sửa design/pt (phiên PT2 đang sửa). Khác PT:
  · dựng theo VÙNG quanh đường bay (mọi mặt hở được chi tiết hoá, không chỉ mặt quay về một máy cố định);
  · mỗi mặt mang mã toà 'bid' + mã nhóm chiếu 'grp' (một mặt phẳng tường của một toà = một nhóm 'elev'; mặt ngang = nhóm 'top');
  · --tex A: 9 khe vân CC0 Poly Haven như PT nhánh A (không điểm ảnh AI) · --tex HC7: mặt đủ điều kiện lấy albedo từ ATLAS của chính toà
    (vân AI nướng một lần cho mỗi toà × mốc, gắn cố định theo UV lên hình học → mọi khung dùng cùng một vân); mặt khác giữ A;
  · --mode probe: lượt mã nhóm ở các khung mẫu (chọn nhóm cần vân) · elev/top: dựng trực giao albedo + mặt nạ cho từng nhóm (đầu vào sửa ảnh)
    · anim: dựng cú máy (khung PNG đã chỉnh màu AgX + EXR: Position, Normal, DiffCol, AOV bid/ai) · cproj: dựng tấm C cho HC8 (góc máy chính).
Hình học, hạt giống, vật liệu nhánh A giống hệt giữa A và HC7 (cùng mã). Không mô hình AI nào chạy trong tệp này.
  /opt/bpy/bin/python build_pt3.py --site street|kb --tex A|HC7 --mode probe|elev|top|anim|cproj --out DIR [--frames 0-191] [--res 960x540] [--spp 32]"""
import bpy, bmesh, math, random, json, os, sys, time, argparse
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import pt_site as S
import cams as CM

ap = argparse.ArgumentParser()
ap.add_argument('--site', required=True, choices=['street', 'kb']); ap.add_argument('--tex', default='A', choices=['A', 'HC7'])
ap.add_argument('--mode', default='anim'); ap.add_argument('--out', required=True); ap.add_argument('--frames', default='')
ap.add_argument('--step', type=int, default=1); ap.add_argument('--res', default='960x540'); ap.add_argument('--spp', type=int, default=32)
ap.add_argument('--atlas', default=os.environ.get('PT3_ATLAS', '/var/tmp/pt3/atlas')); ap.add_argument('--groups', default='')
ap.add_argument('--blend', default=''); ap.add_argument('--hour', type=float, default=16.2)
A = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])
EP = 1943 if A.site == 'street' else 1782; os.makedirs(A.out, exist_ok=True)
T0 = time.time()
TEXDIR = os.environ.get('PT3_TEXA', '/var/tmp/pt3/texA')
SLOTS = {'vua': 'painted_plaster_wall', 'da_voi': 'white_sandstone_blocks_02', 'gach': 'red_brick_plaster_patch_02', 'da_hoc': 'old_stone_wall',
         'ngoi': 'clay_roof_tiles_02', 'go': 'weathered_planks', 'lat1782': 'stony_dirt_path', 'lat1943': 'cobblestone_pavement', 'vai': 'hessian_230'}
TILE_M = {'vua': 2.0, 'da_voi': 2.2, 'gach': 2.0, 'da_hoc': 2.5, 'ngoi': 1.6, 'go': 1.2, 'lat1782': 3.0, 'lat1943': 2.2, 'vai': 1.0}
ELIG = ('vua', 'da_voi', 'gach', 'da_hoc', 'ngoi', 'lat')   # khe được nhận vân AI (bề mặt: vữa, đá, gạch, ngói, nền) — KHÔNG gỗ cửa/chớp, kính, sắt, vải
SITE = CM.SITE[A.site]   # vùng dựng chi tiết + đường bay (cams.py)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
R = random.Random(EP * 7 + 3)

# ---------------------------------------------------------------- vật liệu
def tex_files(slot):
    b = SLOTS[slot]; return {k: os.path.join(TEXDIR, f'{b}_{k}_2k.jpg') for k in ('diff', 'nor', 'rough')}

def img(path, color=True):
    im = bpy.data.images.load(path, check_existing=True)
    if not color: im.colorspace_settings.name = 'Non-Color'
    return im

MATS = {}
def m_textured(name, slot, tint_attr=True, rough_mul=1.0, bump=0.35):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; N = nt.nodes; L = nt.links
    b = N['Principled BSDF']
    tc = N.new('ShaderNodeTexCoord'); mp = N.new('ShaderNodeMapping'); s = 1.0 / TILE_M[slot]
    mp.inputs['Scale'].default_value = (s, s, s); L.new(tc.outputs['Object'], mp.inputs['Vector'])
    f = tex_files(slot)
    def T(path, color=True):
        t = N.new('ShaderNodeTexImage'); t.image = img(path, color); t.projection = 'BOX'; t.projection_blend = 0.25
        L.new(mp.outputs['Vector'], t.inputs['Vector']); return t
    d = T(f['diff'])
    col = d.outputs['Color']
    if tint_attr:
        at = N.new('ShaderNodeAttribute'); at.attribute_name = 'tint'; at.attribute_type = 'GEOMETRY'
        mul = N.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'; mul.inputs['Factor'].default_value = 1.0
        L.new(col, mul.inputs['A']); L.new(at.outputs['Color'], mul.inputs['B']); col = mul.outputs['Result']
    L.new(col, b.inputs['Base Color'])
    if 'rough' in f:
        r = T(f['rough'], False); mr = N.new('ShaderNodeMath'); mr.operation = 'MULTIPLY'; mr.inputs[1].default_value = rough_mul
        L.new(r.outputs['Color'], mr.inputs[0]); L.new(mr.outputs[0], b.inputs['Roughness'])
        n = T(f['nor'], False); nm = N.new('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value = 1.0
        L.new(n.outputs['Color'], nm.inputs['Color']); L.new(nm.outputs['Normal'], b.inputs['Normal'])
    else:   # nhánh B: độ nhám + bump suy từ độ sáng của chính ảnh vân (phép toán, không AI)
        bw = N.new('ShaderNodeRGBToBW'); L.new(d.outputs['Color'], bw.inputs[0])
        mr = N.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value = 0.95 * rough_mul; mr.inputs['To Max'].default_value = 0.6 * rough_mul
        L.new(bw.outputs[0], mr.inputs['Value']); L.new(mr.outputs[0], b.inputs['Roughness'])
        bp = N.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump; bp.inputs['Distance'].default_value = 0.02
        L.new(bw.outputs[0], bp.inputs['Height']); L.new(bp.outputs['Normal'], b.inputs['Normal'])
    m['slot'] = slot; return m

def m_plain(name, col, rough=0.6, metal=0.0, emit=None, estr=0.0, tint_attr=False):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    if tint_attr:
        N = m.node_tree.nodes; at = N.new('ShaderNodeAttribute'); at.attribute_name = 'tint'
        m.node_tree.links.new(at.outputs['Color'], b.inputs['Base Color'])
    if emit:
        b.inputs['Emission Color'].default_value = (*emit, 1); b.inputs['Emission Strength'].default_value = estr
    return m

def m_louvre(name):   # cửa chớp lá sách: vân gỗ + sọc ngang thủ tục (bump theo Z thế giới, bước 4,5 cm)
    m = m_textured(name, 'go', rough_mul=1.0); nt = m.node_tree; N = nt.nodes; L = nt.links; b = N['Principled BSDF']
    tc = N.new('ShaderNodeTexCoord'); sep = N.new('ShaderNodeSeparateXYZ'); L.new(tc.outputs['Object'], sep.inputs[0])
    w = N.new('ShaderNodeMath'); w.operation = 'MULTIPLY'; w.inputs[1].default_value = 2 * math.pi / 0.045; L.new(sep.outputs['Z'], w.inputs[0])
    sn = N.new('ShaderNodeMath'); sn.operation = 'SINE'; L.new(w.outputs[0], sn.inputs[0])
    bp = N.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.9; bp.inputs['Distance'].default_value = 0.01; L.new(sn.outputs[0], bp.inputs['Height'])
    old = [l for l in L if l.to_socket == b.inputs['Normal']]
    if old: L.new(old[0].from_socket, bp.inputs['Normal'])
    L.new(bp.outputs['Normal'], b.inputs['Normal'])
    return m

def m_glass():
    m = bpy.data.materials.new('kinh'); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (0.03, 0.035, 0.04, 1); b.inputs['Roughness'].default_value = 0.08
    b.inputs['Specular IOR Level'].default_value = 0.8
    N = m.node_tree.nodes; at = N.new('ShaderNodeAttribute'); at.attribute_name = 'lit'
    mul = N.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = 0.0; mul.name = 'litgain'
    m.node_tree.links.new(at.outputs['Fac'], mul.inputs[0]); m.node_tree.links.new(mul.outputs[0], b.inputs['Emission Strength'])
    b.inputs['Emission Color'].default_value = (1.0, 0.62, 0.3, 1)
    return m

def m_interior():
    m = bpy.data.materials.new('trong_nha'); m.use_nodes = True; N = m.node_tree.nodes; b = N['Principled BSDF']
    b.inputs['Base Color'].default_value = (0.025, 0.02, 0.016, 1); b.inputs['Roughness'].default_value = 0.9
    at = N.new('ShaderNodeAttribute'); at.attribute_name = 'lit'
    mul = N.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = 0.0; mul.name = 'litgain'
    m.node_tree.links.new(at.outputs['Fac'], mul.inputs[0]); m.node_tree.links.new(mul.outputs[0], b.inputs['Emission Strength'])
    b.inputs['Emission Color'].default_value = (1.0, 0.55, 0.25, 1)
    return m

def m_sea():
    m = bpy.data.materials.new('bien'); m.use_nodes = True; N = m.node_tree.nodes; L = m.node_tree.links; b = N['Principled BSDF']
    b.inputs['Base Color'].default_value = (0.012, 0.05, 0.06, 1); b.inputs['Roughness'].default_value = 0.16
    tc = N.new('ShaderNodeTexCoord'); n = N.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = 0.35; n.inputs['Detail'].default_value = 8
    mp = N.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1, 2.2, 1); L.new(tc.outputs['Object'], mp.inputs[0]); L.new(mp.outputs[0], n.inputs['Vector'])
    bp = N.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.45; L.new(n.outputs['Fac'], bp.inputs['Height']); L.new(bp.outputs['Normal'], b.inputs['Normal'])
    return m

def m_hills():
    m = bpy.data.materials.new('doi'); m.use_nodes = True; N = m.node_tree.nodes; L = m.node_tree.links; b = N['Principled BSDF']
    tc = N.new('ShaderNodeTexCoord'); n = N.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = 0.004; n.inputs['Detail'].default_value = 10
    L.new(tc.outputs['Object'], n.inputs['Vector']); cr = N.new('ShaderNodeValToRGB')
    cr.color_ramp.elements[0].color = (0.16, 0.15, 0.09, 1); cr.color_ramp.elements[1].color = (0.32, 0.3, 0.2, 1)
    L.new(n.outputs['Fac'], cr.inputs[0]); L.new(cr.outputs[0], b.inputs['Base Color']); b.inputs['Roughness'].default_value = 0.95
    return m

M = {}
for s in ('vua', 'da_voi', 'gach', 'da_hoc', 'ngoi', 'go', 'vai'): M[s] = m_textured('m_' + s, s)
M['lat'] = m_textured('m_lat', 'lat1782' if EP == 1782 else 'lat1943', tint_attr=False)
def ground_grime(m):
    nt = m.node_tree; N = nt.nodes; L = nt.links; b = N['Principled BSDF']; src = b.inputs['Base Color'].links[0].from_socket
    tc = N.new('ShaderNodeTexCoord'); n = N.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = 0.08; n.inputs['Detail'].default_value = 6
    L.new(tc.outputs['Object'], n.inputs['Vector']); cr = N.new('ShaderNodeMapRange'); cr.inputs['From Min'].default_value = 0.35; cr.inputs['From Max'].default_value = 0.65
    cr.inputs['To Min'].default_value = 0.62; cr.inputs['To Max'].default_value = 1.08; L.new(n.outputs['Fac'], cr.inputs['Value'])
    mul = N.new('ShaderNodeVectorMath'); mul.operation = 'SCALE'; L.new(src, mul.inputs[0]); L.new(cr.outputs[0], mul.inputs['Scale']); L.new(mul.outputs[0], b.inputs['Base Color'])
ground_grime(M['lat'])
def wall_grime(m, k=1.0):   # vệt ẩm chân tường + loang bẩn theo độ cao (thủ tục; như nhau ở nhánh A và B)
    nt = m.node_tree; N = nt.nodes; L = nt.links; b = N['Principled BSDF']; src = b.inputs['Base Color'].links[0].from_socket
    tc = N.new('ShaderNodeTexCoord'); sep = N.new('ShaderNodeSeparateXYZ'); L.new(tc.outputs['Object'], sep.inputs[0])
    n = N.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = 0.6; n.inputs['Detail'].default_value = 8
    mp = N.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1, 1, 0.25); L.new(tc.outputs['Object'], mp.inputs[0]); L.new(mp.outputs[0], n.inputs['Vector'])
    h = N.new('ShaderNodeMapRange'); h.inputs['From Min'].default_value = 0.0; h.inputs['From Max'].default_value = 1.6; h.inputs['To Min'].default_value = 0.55; h.inputs['To Max'].default_value = 1.0
    L.new(sep.outputs['Z'], h.inputs['Value'])
    g = N.new('ShaderNodeMapRange'); g.inputs['From Min'].default_value = 0.4; g.inputs['From Max'].default_value = 0.7; g.inputs['To Min'].default_value = 1.0 - 0.3 * k; g.inputs['To Max'].default_value = 1.0
    L.new(n.outputs['Fac'], g.inputs['Value'])
    m1 = N.new('ShaderNodeMath'); m1.operation = 'MULTIPLY'; L.new(h.outputs[0], m1.inputs[0]); L.new(g.outputs[0], m1.inputs[1])
    mul = N.new('ShaderNodeVectorMath'); mul.operation = 'SCALE'; L.new(src, mul.inputs[0]); L.new(m1.outputs[0], mul.inputs['Scale']); L.new(mul.outputs[0], b.inputs['Base Color'])
wall_grime(M['vua'], 1.0 if EP == 1782 else 0.7)
M['laso'] = m_louvre('m_laso'); M['kinh'] = m_glass(); M['trong'] = m_interior()
M['sat'] = m_plain('sat', (0.025, 0.025, 0.027), 0.45, 0.85); M['dong'] = m_plain('dong_den', (0.05, 0.045, 0.04), 0.5, 0.7)
M['son'] = m_plain('son', (1, 1, 1), 0.55, tint_attr=True)   # sơn trơn (thân tàu, xe, cột cờ) — màu theo 'tint'
M['bien'] = m_sea(); M['doi'] = m_hills()
M['den'] = m_plain('den_dau', (1, 0.8, 0.5), 0.5, emit=(1.0, 0.6, 0.28), estr=0.0)
M['cat'] = m_textured('m_bao_cat', 'vai')   # bao cát (vải bố) — tô màu kaki qua tint

# ---------------------------------------------------------------- bộ đệm lưới theo vật liệu (mỗi mặt có 'tint', 'lit')
CUR = [0]   # mã lớp (bid) của mặt đang dựng: 1..N toà · 8000 bastion · 9000 Line Wall · 9500 đồ phố · 9600 đồi · 9700 biển · 9800 mặt đất · 9900 tàu
CURG = [0]  # mã nhóm chiếu (grp) của mặt đang dựng: 0 = không nhóm; ≥ 1 = nhóm 'elev' (mặt phẳng tường) trong GRP
GRP = [None]   # GRP[g] = {'kind': 'elev', 'bid', 'p0', 'u', 'w', 'L', 'z0', 'z1', 'order'}
def new_group(bid, p0, p1, z0, z1, order):
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]; L = math.hypot(dx, dy); u = (dx / L, dy / L)
    GRP.append({'kind': 'elev', 'bid': bid, 'p0': list(p0), 'u': list(u), 'w': [u[1], -u[0]], 'L': L, 'z0': z0, 'z1': z1, 'order': order}); return len(GRP) - 1
class Buf:
    def __init__(s): s.v = []; s.f = []; s.tint = []; s.lit = []; s.bid = []; s.grp = []
    def face(s, pts, tint=(1, 1, 1), lit=0.0):
        i = len(s.v); s.v.extend(pts); s.f.append(tuple(range(i, i + len(pts)))); s.tint.append(tint); s.lit.append(lit); s.bid.append(CUR[0]); s.grp.append(CURG[0])
B = {k: Buf() for k in M}

def box(mat, c, size, yaw=0.0, tint=(1, 1, 1), lit=0.0, faces='all', pitch=0.0):
    """hộp tâm c, cỡ (sx, sy, sz) trong hệ (u dọc, w ra, v lên) quay quanh Z một góc yaw; pitch quay quanh trục u."""
    sx, sy, sz = [x / 2 for x in size]; cy, sy_ = math.cos(yaw), math.sin(yaw); cp, sp = math.cos(pitch), math.sin(pitch)
    def P(x, y, z):
        y, z = y * cp - z * sp, y * sp + z * cp
        return (c[0] + x * cy - y * sy_, c[1] + x * sy_ + y * cy, c[2] + z)
    v = [P(x, y, z) for x in (-sx, sx) for y in (-sy, sy) for z in (-sz, sz)]
    F = {'-x': (0, 1, 3, 2), '+x': (4, 6, 7, 5), '-y': (0, 4, 5, 1), '+y': (2, 3, 7, 6), '-z': (0, 2, 6, 4), '+z': (1, 5, 7, 3)}
    for k, q in F.items():
        if faces == 'all' or k in faces: B[mat].face([v[i] for i in q], tint, lit)

class Frame:
    """hệ toạ độ mặt tiền: gốc p0 (mặt đường), u dọc cạnh p0→p1, w pháp tuyến ra ngoài, v lên."""
    def __init__(s, p0, p1, z0=0.0):
        s.p0 = p0; dx, dy = p1[0] - p0[0], p1[1] - p0[1]; s.L = math.hypot(dx, dy); s.u = (dx / s.L, dy / s.L); s.w = (s.u[1], -s.u[0]); s.z0 = z0
        s.yaw = math.atan2(s.u[1], s.u[0])
    def P(s, u, v, w=0.0):
        return (s.p0[0] + s.u[0] * u + s.w[0] * w, s.p0[1] + s.u[1] * u + s.w[1] * w, s.z0 + v)
    def quad(s, mat, u0, u1, v0, v1, w=0.0, tint=(1, 1, 1), lit=0.0, flip=False):
        q = [s.P(u0, v0, w), s.P(u1, v0, w), s.P(u1, v1, w), s.P(u0, v1, w)]
        B[mat].face(q[::-1] if flip else q, tint, lit)
    def box(s, mat, u0, u1, v0, v1, w0, w1, tint=(1, 1, 1), lit=0.0, faces='all'):
        c = s.P((u0 + u1) / 2, (v0 + v1) / 2, (w0 + w1) / 2); box(mat, c, (u1 - u0, w1 - w0, v1 - v0), s.yaw, tint, lit, faces)

# ---------------------------------------------------------------- bảng màu thời kỳ (màu sơn/vôi — đặt tay theo tranh khắc/ảnh tham chiếu, ghi trong báo cáo)
if EP == 1782:
    WALLC = [(0.93, 0.89, 0.78), (0.96, 0.93, 0.86), (0.9, 0.8, 0.62), (0.86, 0.78, 0.66), (0.97, 0.95, 0.9), (0.84, 0.72, 0.56), (0.8, 0.74, 0.64)]
    SHUT = [(0.32, 0.22, 0.14), (0.4, 0.3, 0.2), (0.25, 0.28, 0.2), (0.45, 0.38, 0.3)]
else:
    WALLC = [(0.95, 0.78, 0.5), (0.92, 0.64, 0.5), (0.97, 0.9, 0.72), (0.84, 0.76, 0.62), (0.95, 0.72, 0.45), (0.86, 0.56, 0.44), (0.94, 0.92, 0.84), (0.7, 0.78, 0.7), (0.98, 0.85, 0.62)]
    SHUT = [(0.12, 0.3, 0.16), (0.1, 0.26, 0.15), (0.16, 0.34, 0.2), (0.3, 0.2, 0.12), (0.1, 0.22, 0.14)]

LOG = {'epoch': EP, 'site': A.site, 'mode': A.mode, 'tex': A.tex, 'ai_texture': A.tex == 'HC7', 'houses': 0, 'windows': 0, 'balconies': 0, 'ruins': 0, 'props': {}}
def note(k, n=1): LOG['props'][k] = LOG['props'].get(k, 0) + n

# ---------------------------------------------------------------- mặt tiền thủ tục
def facade(fr, H, storeys, spec, rng):
    """một mặt tiền dài fr.L, cao H, các tầng storeys=[(v0, v1)], spec: dict kiểu nhà."""
    L = fr.L; wc = spec['wall']; ep = EP
    bay = spec['bay']; nb = max(1, int((L - 0.6) / bay)); bw = (L - 0.0) / nb
    ruin_top = spec.get('ruin')    # danh sách cao độ đỉnh tường theo nhịp (nhà đổ nát) hoặc None
    def top_at(i): return ruin_top[i] if ruin_top else H
    # dải tường giữa các ô cửa (tường đặc + ô trống) theo từng tầng
    for i in range(nb):
        u0, u1 = i * bw, (i + 1) * bw; uc = (u0 + u1) / 2; tH = top_at(i)
        for si, (v0, v1) in enumerate(storeys):
            if v0 >= tH - 0.3: break
            v1c = min(v1, tH)
            ground = si == 0
            kind = spec['gf'][i] if ground else ('win' if rng.random() > spec.get('blank', 0.08) else 'blank')
            if kind == 'blank' or v1c - v0 < 1.6:
                fr.quad('vua', u0, u1, v0, v1c, tint=wc); continue
            if ground:
                ow = min(bw - 0.5, spec['door_w'] if kind == 'door' else spec['shop_w']); oh = min(v1c - v0 - 0.5, spec['door_h'] if kind == 'door' else spec['shop_h']); s0 = 0.0
            else:
                ow = min(bw - 0.55, spec['win_w']); oh = min(v1c - v0 - 0.9, spec['win_h']); s0 = spec['sill']
            a0, a1 = uc - ow / 2, uc + ow / 2; b0 = v0 + s0; b1 = b0 + oh
            if b1 > v1c - 0.15: b1 = v1c - 0.15
            # tường quanh ô
            fr.quad('vua', u0, a0, v0, v1c, tint=wc); fr.quad('vua', a1, u1, v0, v1c, tint=wc)
            if b0 > v0: fr.quad('vua', a0, a1, v0, b0, tint=wc)
            fr.quad('vua', a0, a1, b1, v1c, tint=wc)
            d = spec['reveal']
            # má cửa (reveal)
            fr_rev(fr, a0, a1, b0, b1, d, wc)
            broken = ruin_top is not None and rng.random() < 0.55
            lit = 1.0 if (not broken and rng.random() < spec['lit_p']) else 0.0
            if ground:
                gf_fill(fr, kind, a0, a1, b0, b1, d, spec, rng, broken)
            else:
                LOG['windows'] += 1
                win_fill(fr, a0, a1, b0, b1, d, spec, rng, broken, lit)
                if spec['balc_p'] > rng.random() and not broken and si >= 1:
                    balcony(fr, a0 - 0.35, a1 + 0.35, b0, spec, rng)
            # khung đá/vữa quanh cửa sổ (1943: gờ chỉ; 1782: viền vôi)
            if spec['surround'] and not ground and not broken:
                t = 0.11; fr.box('vua', a0 - t, a0, b0, b1 + t, 0, 0.04, tint=spec['trim']); fr.box('vua', a1, a1 + t, b0, b1 + t, 0, 0.04, tint=spec['trim'])
                fr.box('vua', a0 - t, a1 + t, b1, b1 + t + 0.06, 0, 0.06, tint=spec['trim'])
            if not ground and spec['sill_stone']:
                fr.box('da_voi', a0 - 0.08, a1 + 0.08, b0 - 0.07, b0, 0, 0.09)
    # đầu tường đổ nát: mặt trên tường hở (dày 0,45 m) + thanh dầm cháy chìa ra
    if ruin_top:   # lô đổ nát: tường ngăn phía sau (sâu 5,5 m) + sàn cháy + đống gạch → không lộ lòng khối rỗng
        P = fr.P; bt = tuple(c * 0.9 for c in wc)
        B['vua'].face([P(0, 0, -5.5), P(L, 0, -5.5), P(L, H + 0.8, -5.5), P(0, H + 0.8, -5.5)], bt)
        B['gach'].face([P(0, storeys[0][1] - 0.2, -0.3), P(L, storeys[0][1] - 0.2, -0.3), P(L, storeys[0][1] - 0.2, -5.5), P(0, storeys[0][1] - 0.2, -5.5)][::-1])
        for uu in (0.0, L): B['vua'].face([P(uu, 0, 0), P(uu, 0, -5.5), P(uu, H, -5.5), P(uu, H * 0.7, 0)], bt)
        for k in range(int(L / 1.5)):
            c = P(rng.uniform(0.3, L - 0.3), storeys[0][1] - 0.1, -rng.uniform(1, 5)); sz = rng.uniform(0.3, 0.9)
            box('da_hoc' if k % 2 else 'gach', c, (sz, sz, sz * 0.5), fr.yaw + rng.uniform(0, 3))
        for i in range(nb):
            u0, u1 = i * bw, (i + 1) * bw; tH = top_at(i)
            fr.box('gach', u0, u1, tH - 0.25, tH, -0.45, 0.0)
            if rng.random() < 0.5:
                fr.box('go', u0 + 0.3, u0 + 0.5, tH - 0.9 - rng.random(), tH - 0.7, -1.6, 0.25 + rng.random() * 0.4, tint=(0.18, 0.15, 0.12))
    else:
        # gờ tầng + gờ mái
        for si, (v0, v1) in enumerate(storeys[1:], 1):
            fr.box('vua' if EP == 1782 else 'da_voi', -0.02, L + 0.02, v0 - 0.12, v0 + 0.06, 0, spec['band'], tint=spec['trim'])
        c = spec['cornice']
        fr.box('vua', -0.05, L + 0.05, H - 0.32, H - 0.1, 0, c * 0.6, tint=spec['trim'])
        fr.box('vua', -0.1, L + 0.1, H - 0.1, H + 0.06, 0, c, tint=spec['trim'])
        if spec['roof'] == 'hip' and EP == 1782:   # mái ngói một dốc theo lô (nhìn thấy từ đường), không phủ cả khối phố
            rise = math.tan(math.radians(spec['pitch'])) * 5.5; P = fr.P
            B['ngoi'].face([P(-0.1, H + 0.04, 0.5), P(L + 0.1, H + 0.04, 0.5), P(L + 0.1, H + rise, -5.0), P(-0.1, H + rise, -5.0)])
            B['ngoi'].face([P(-0.1, H - 0.06, 0.5), P(L + 0.1, H - 0.06, 0.5), P(L + 0.1, H + 0.04, 0.5), P(-0.1, H + 0.04, 0.5)])
            for uu in (-0.1, L + 0.1): B['vua'].face([P(uu, H, 0), P(uu, H, -5.0), P(uu, H + rise, -5.0)], wc)
        if spec['roof'] == 'flat':   # tường chắn mái
            fr.box('vua', 0, L, H + 0.06, H + spec['parapet'], -0.25, 0.0, tint=wc)
            fr.box('da_voi', -0.03, L + 0.03, H + spec['parapet'], H + spec['parapet'] + 0.08, -0.3, 0.04)
    # chân tường đá
    fr.box('da_voi', -0.02, L + 0.02, 0, spec['plinth'], 0, 0.05)
    if spec['quoins']:
        for v in range(int(H / 0.5)):
            wq = 0.55 if v % 2 else 0.35
            for uu in (0.0, L - wq): fr.box('da_voi', uu, uu + wq, v * 0.5 + 0.02, v * 0.5 + 0.48, 0, 0.035)

def fr_rev(fr, a0, a1, b0, b1, d, wc):
    fr.quad('vua', a0, a0, b0, b1, tint=wc)  # placeholder (không diện tích)
    B['vua'].f.pop(); B['vua'].tint.pop(); B['vua'].lit.pop(); B['vua'].bid.pop(); B['vua'].grp.pop(); [B['vua'].v.pop() for _ in range(4)]
    P = fr.P
    B['vua'].face([P(a0, b0, 0), P(a0, b1, 0), P(a0, b1, -d), P(a0, b0, -d)], wc)
    B['vua'].face([P(a1, b0, -d), P(a1, b1, -d), P(a1, b1, 0), P(a1, b0, 0)], wc)
    B['vua'].face([P(a0, b1, 0), P(a1, b1, 0), P(a1, b1, -d), P(a0, b1, -d)], wc)
    B['vua'].face([P(a0, b0, -d), P(a1, b0, -d), P(a1, b0, 0), P(a0, b0, 0)], wc)

def win_fill(fr, a0, a1, b0, b1, d, spec, rng, broken, lit):
    sh = spec['shut']; st = rng.random()
    if broken:   # cửa vỡ: lỗ tối, khung gãy, muội
        fr.quad('trong', a0, a1, b0, b1, -d - 0.6)
        fr.quad('vua', a0 - 0.25, a1 + 0.25, b1, b1 + 0.6, 0.005, tint=(0.25, 0.22, 0.2))
        if rng.random() < 0.5: fr.box('go', a0, a1, b0 + 0.4, b0 + 0.5, -d, -d + 0.05, tint=(0.2, 0.16, 0.12))
        return
    fr.quad('trong', a0, a1, b0, b1, -d - 0.5, lit=lit)
    # khung + kính (mạng ô kính)
    gl_w = -d + 0.04
    fr.quad('kinh', a0, a1, b0, b1, gl_w, lit=lit)
    nx = 2 if spec['win_w'] < 1.0 else 2; ny = 3 if EP == 1782 else 3
    for k in range(1, nx): x = a0 + (a1 - a0) * k / nx; fr.box('go', x - 0.025, x + 0.025, b0, b1, gl_w, gl_w + 0.04, tint=spec['frame'])
    for k in range(1, ny): y = b0 + (b1 - b0) * k / ny; fr.box('go', a0, a1, y - 0.02, y + 0.02, gl_w, gl_w + 0.04, tint=spec['frame'])
    fr.box('go', a0, a1, b0, b0 + 0.06, gl_w, gl_w + 0.06, tint=spec['frame']); fr.box('go', a0, a1, b1 - 0.06, b1, gl_w, gl_w + 0.06, tint=spec['frame'])
    # cửa chớp: mở áp tường / khép / hé
    half = (a1 - a0) / 2
    if st < spec['shut_open']:
        for s_, (x0, x1) in ((-1, (a0 - half - 0.02, a0 - 0.02)), (1, (a1 + 0.02, a1 + half + 0.02))):
            fr.box(spec['shut_mat'], x0, x1, b0, b1, 0.01, 0.05, tint=sh)
    elif st < spec['shut_open'] + spec['shut_closed']:
        fr.box(spec['shut_mat'], a0, a0 + half - 0.01, b0, b1, -0.06, -0.02, tint=sh); fr.box(spec['shut_mat'], a0 + half + 0.01, a1, b0, b1, -0.06, -0.02, tint=sh)
    else:   # hé: một cánh mở góc
        ang = 0.9; P = fr.P
        x0 = a0
        c = P(x0 - math.cos(ang) * half / 2, (b0 + b1) / 2, math.sin(ang) * half / 2)
        box(spec['shut_mat'], c, (half, 0.04, b1 - b0), fr.yaw - ang, tint=sh)
        fr.box(spec['shut_mat'], a0 + half + 0.01, a1, b0, b1, -0.06, -0.02, tint=sh)

def gf_fill(fr, kind, a0, a1, b0, b1, d, spec, rng, broken):
    if broken:
        fr.quad('trong', a0, a1, b0, b1, -d - 1.0)
        if rng.random() < 0.6: fr.box('go', a0 + 0.1, a1 - 0.1, b0, b0 + (b1 - b0) * rng.uniform(0.3, 0.7), -d + 0.02, -d + 0.07, tint=(0.25, 0.2, 0.15))  # ván bít
        return
    if kind == 'door':
        fr.box('go', a0, a1, b0, b1, -d, -d + 0.06, tint=spec['door'])
        for k in range(1, 4): x = a0 + (a1 - a0) * k / 4; fr.box('go', x - 0.015, x + 0.015, b0, b1, -d + 0.06, -d + 0.075, tint=spec['door'])
        fr.box('sat', (a0 + a1) / 2 + 0.15, (a0 + a1) / 2 + 0.22, b0 + 1.0, b0 + 1.08, -d + 0.06, -d + 0.1)
    else:   # cửa hàng: khung gỗ, kính ô, quầy; hoặc cánh gỗ khép
        if rng.random() < spec['shop_closed']:
            fr.box('go', a0, a1, b0, b1, -d, -d + 0.05, tint=spec['door'])
            for k in range(1, 6): x = a0 + (a1 - a0) * k / 6; fr.box('go', x - 0.012, x + 0.012, b0, b1, -d + 0.05, -d + 0.065, tint=spec['door'])
        else:
            fr.quad('trong', a0, a1, b0, b1, -d - 2.0, lit=0.0)
            for k in range(0, 4):
                x = a0 + (a1 - a0) * k / 3; fr.box('go', x - 0.04, x + 0.04, b0, b1, -d, -d + 0.08, tint=spec['frame'])
            fr.box('go', a0, a1, b0, b0 + 0.75, -d, -d + 0.1, tint=spec['door']); fr.quad('kinh', a0, a1, b0 + 0.75, b1, -d + 0.03)
            fr.box('go', a0, a1, b1 - 0.35, b1, -d, -d + 0.08, tint=spec['door'])   # dải biển hiệu trơn (KHÔNG chữ)
        if spec['awning_p'] > rng.random():
            awning(fr, a0 - 0.2, a1 + 0.2, b1 + 0.15, spec, rng)
    if EP == 1943 and spec.get('sandbag') and rng.random() < spec['sandbag']:
        sandbags(fr, a0 - 0.3, a1 + 0.3, rng)

def balcony(fr, a0, a1, v, spec, rng):
    LOG['balconies'] += 1
    dep = spec['balc_d']; iron = EP == 1943
    fr.box('da_voi' if iron else 'go', a0, a1, v - 0.14, v, 0, dep, tint=(0.4, 0.3, 0.2) if not iron else (1, 1, 1))
    mat = 'sat' if iron else 'go'; tn = (0.3, 0.22, 0.15)
    hgt = 1.0; bar = 0.022 if iron else 0.05; step = 0.12 if iron else 0.16
    fr.box(mat, a0, a1, v + hgt - 0.04, v + hgt, dep - 0.05, dep, tint=tn)
    fr.box(mat, a0, a1, v + 0.05, v + 0.09, dep - 0.05, dep, tint=tn)
    n = int((a1 - a0) / step)
    for k in range(n + 1):
        x = a0 + (a1 - a0) * k / max(1, n); fr.box(mat, x - bar / 2, x + bar / 2, v, v + hgt, dep - 0.04, dep - 0.04 + bar, tint=tn)
    for side in (a0, a1):
        for k in range(4):
            w = dep * k / 4; fr.box(mat, side - bar / 2, side + bar / 2, v, v + hgt, w, w + bar, tint=tn)
    if iron and rng.random() < 0.35:   # chậu cây
        fr.box('vua', a0 + 0.2, a0 + 0.45, v, v + 0.25, dep - 0.35, dep - 0.1, tint=(0.55, 0.3, 0.2)); note('chau_cay')

def awning(fr, a0, a1, v, spec, rng):
    note('mai_che')
    proj = 1.3 + rng.random() * 0.5; drop = 0.6; P = fr.P
    tint = rng.choice([(0.85, 0.82, 0.72), (0.55, 0.25, 0.2), (0.35, 0.4, 0.3), (0.8, 0.7, 0.5)])
    B['vai'].face([P(a0, v + 0.3, 0.02), P(a1, v + 0.3, 0.02), P(a1, v + 0.3 - drop, proj), P(a0, v + 0.3 - drop, proj)][::-1], tint)
    B['vai'].face([P(a0, v + 0.3 - drop, proj), P(a1, v + 0.3 - drop, proj), P(a1, v + 0.3 - drop - 0.25, proj + 0.02), P(a0, v + 0.3 - drop - 0.25, proj + 0.02)][::-1], tint)
    for x in (a0 + 0.05, a1 - 0.05): fr.box('sat', x - 0.012, x + 0.012, v + 0.3 - drop - 0.02, v + 0.3, proj - 0.03, proj, faces='all')

def sandbags(fr, a0, a1, rng):
    note('bao_cat')
    for row in range(5):
        x = a0 - (0.2 if row % 2 else 0)
        while x < a1:
            w = 0.55; fr.box('cat', x, x + w - 0.03, row * 0.2, row * 0.2 + 0.19, 0.3, 0.75, tint=(0.62, 0.55, 0.4)); x += w

# ---------------------------------------------------------------- khối nhà
def roof_flat(poly, H, spec):
    bm = bmesh.new(); vs = [bm.verts.new((x, y, H + 0.05)) for x, y in poly]
    try: bm.faces.new(vs)
    except ValueError: pass
    for f in bm.faces: B['vua'].face([tuple(v.co) for v in f.verts], spec['wall'])
    bm.free()

def roof_hip(poly, H, spec):
    """mái ngói bốn mái trên hình chữ nhật bao (định hướng theo cạnh dài nhất), độ dốc 26° (1943) / 18° (1782)."""
    n = len(poly); best = max(range(n), key=lambda i: math.dist(poly[i], poly[(i + 1) % n]))
    p0, p1 = poly[best], poly[(best + 1) % n]; ux, uy = (p1[0] - p0[0]), (p1[1] - p0[1]); l = math.hypot(ux, uy); ux, uy = ux / l, uy / l; vx, vy = -uy, ux
    us = [(x - p0[0]) * ux + (y - p0[1]) * uy for x, y in poly]; vs_ = [(x - p0[0]) * vx + (y - p0[1]) * vy for x, y in poly]
    u0, u1, v0, v1 = min(us) - 0.3, max(us) + 0.3, min(vs_) - 0.3, max(vs_) + 0.3
    if (u1 - u0) * (v1 - v0) > 2.2 * abs(S.area(poly)) + 30: return roof_flat(poly, H, spec) or 'flat'
    W = v1 - v0; rise = math.tan(math.radians(spec['pitch'])) * W / 2; hu = W / 2
    P = lambda u, v, z: (p0[0] + ux * u + vx * v, p0[1] + uy * u + vy * v, H + z)
    a, b, c, d = P(u0, v0, 0), P(u1, v0, 0), P(u1, v1, 0), P(u0, v1, 0)
    r0, r1 = P(min(u0 + hu, (u0 + u1) / 2), (v0 + v1) / 2, rise), P(max(u1 - hu, (u0 + u1) / 2), (v0 + v1) / 2, rise)
    for f in ([a, b, r1, r0], [b, c, r1], [c, d, r0, r1], [d, a, r0]): B['ngoi'].face(f)
    # mép ngói dày
    for q in ((a, b), (b, c), (c, d), (d, a)):
        e0, e1 = q; B['ngoi'].face([e0, e1, (e1[0], e1[1], e1[2] - 0.08), (e0[0], e0[1], e0[2] - 0.08)][::-1])
    return 'hip'

def chimney(x, y, H, rng):
    note('ong_khoi'); w = 0.5 + rng.random() * 0.3; h = 1.0 + rng.random() * 0.9
    box('vua', (x, y, H + h / 2), (w, w * 0.8, h), tint=(0.85, 0.82, 0.75)); box('gach', (x, y, H + h + 0.06), (w + 0.1, w * 0.8 + 0.1, 0.12))
    CHIM.append((x, y, H + h + 0.12))
CHIM = []

def open_side(px, py, polys, me):
    for j, q in enumerate(polys):
        if j != me and S.inside(px, py, q): return False
    return True

def house_spec(rng, ruin=False):
    if EP == 1782:
        return dict(wall=rng.choice(WALLC), trim=(0.97, 0.96, 0.93), shut=rng.choice(SHUT), frame=(0.35, 0.28, 0.2), door=(0.3, 0.22, 0.15),
                    bay=rng.uniform(2.6, 3.4), win_w=0.85, win_h=1.35, sill=0.9, door_w=1.15, door_h=2.3, shop_w=1.6, shop_h=2.4, reveal=0.32,
                    balc_p=0.12, balc_d=0.55, shut_open=0.35, shut_closed=0.45, shut_mat='go', surround=rng.random() < 0.5, sill_stone=False,
                    band=0.05, cornice=0.18, parapet=0.7, plinth=0.45, quoins=False, roof=rng.choice(['flat', 'hip', 'hip']), pitch=20,
                    lit_p=0.16, awning_p=0.08, shop_closed=0.7, blank=0.12, ruin=None, sandbag=0)
    return dict(wall=rng.choice(WALLC), trim=(0.95, 0.93, 0.88), shut=rng.choice(SHUT), frame=(0.92, 0.9, 0.85), door=rng.choice([(0.12, 0.2, 0.14), (0.3, 0.18, 0.1), (0.15, 0.15, 0.17)]),
                bay=rng.uniform(2.2, 2.8), win_w=1.0, win_h=1.95, sill=0.75, door_w=1.3, door_h=2.9, shop_w=2.0, shop_h=3.0, reveal=0.26,
                balc_p=0.45, balc_d=0.65, shut_open=0.45, shut_closed=0.3, shut_mat='laso', surround=True, sill_stone=True,
                band=0.1, cornice=0.42, parapet=0.95, plinth=0.6, quoins=rng.random() < 0.3, roof=rng.choice(['flat', 'flat', 'hip']), pitch=26,
                lit_p=0.02, awning_p=0.35, shop_closed=0.45, blank=0.04, ruin=None, sandbag=0.25)

def building(poly, polys, me, storeys_n, rng, ruin_p=0.0):
    """PT3: mọi mặt hở (không áp toà khác) trong vùng chi tiết của đường bay được dựng mặt tiền đầy đủ; mỗi cạnh = một nhóm chiếu 'elev'."""
    CUR[0] = me + 1
    if S.area(poly) < 0: poly = poly[::-1]
    spec = house_spec(rng); LOG['houses'] += 1
    gfh = 3.9 if EP == 1943 else 3.4; uh = 3.4 if EP == 1943 else 3.1
    st = [(0.0, gfh)] + [(gfh + uh * i, gfh + uh * (i + 1)) for i in range(storeys_n - 1)]
    H = st[-1][1]; ruin = rng.random() < ruin_p
    if ruin: LOG['ruins'] += 1
    n = len(poly); front_any = False
    top = H + (spec['parapet'] + 0.1 if spec['roof'] == 'flat' else spec['cornice'] + 0.2)
    for i in range(n):
        p0, p1 = poly[i], poly[(i + 1) % n]
        L = math.dist(p0, p1)
        if L < 0.8: continue
        CURG[0] = new_group(me + 1, p0, p1, 0.0, top, i)
        fr = Frame(p0, p1); mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        visible = open_side(mx + fr.w[0] * 1.5, my + fr.w[1] * 1.5, polys, me)
        near = CM.dist_path(SITE, mx, my) < SITE['detail_d']
        if visible and near and L > 2.0:
            front_any = True
            nl = max(1, int(L / rng.uniform(7.0, 11.0))); lw = L / nl
            for k in range(nl):
                q0 = (p0[0] + fr.u[0] * lw * k, p0[1] + fr.u[1] * lw * k); q1 = (p0[0] + fr.u[0] * lw * (k + 1), p0[1] + fr.u[1] * lw * (k + 1))
                sp = house_spec(rng) if k else dict(spec); sp['roof'] = spec['roof']; sp['ruin'] = None
                fk = Frame(q0, q1); nb = max(1, int((lw - 0.6) / sp['bay']))
                kinds = []
                for b_ in range(nb):
                    kinds.append('door' if (b_ == nb // 2 and nb % 2) or rng.random() < 0.3 else ('shop' if rng.random() < (0.7 if EP == 1943 else 0.35) else 'door'))
                sp['gf'] = kinds
                lot_ruin = ruin or (rng.random() < ruin_p * 0.5)
                if lot_ruin:
                    sp['ruin'] = [max(gfh + 0.6, H - rng.uniform(0.5, uh * 1.4)) for _ in range(nb)]
                    sp['wall'] = tuple(c * 0.82 for c in sp['wall'])
                facade(fk, H, st, sp, rng)
        else:
            # mặt khuất/xa: tường trơn (vẫn có vân vữa)
            B['vua'].face([(p0[0], p0[1], 0), (p1[0], p1[1], 0), (p1[0], p1[1], H), (p0[0], p0[1], H)], spec['wall'])
    CURG[0] = 0
    if ruin:   # nhà đổ nát: không mái, sàn cháy, tường trong lộ
        roof_flat(poly, gfh - 0.2, {'wall': (0.42, 0.36, 0.3)})
        cx = sum(p[0] for p in poly) / n; cy = sum(p[1] for p in poly) / n
        for k in range(6): box('go', (cx + rng.uniform(-3, 3), cy + rng.uniform(-3, 3), gfh + rng.uniform(0, 2)), (rng.uniform(2, 4), 0.2, 0.22), rng.uniform(0, 3), tint=(0.12, 0.1, 0.08), pitch=rng.uniform(-0.5, 0.5))
        rubble(cx, cy, rng, 8)
    else:
        kind = spec['roof'] if (storeys_n <= 4 and EP == 1943) else 'flat'
        if kind == 'hip': kind = roof_hip(poly, H, spec) or 'flat'
        if kind == 'flat': roof_flat(poly, H, spec)
        cx = sum(p[0] for p in poly) / n; cy = sum(p[1] for p in poly) / n
        for k in range(rng.randint(1, 3)):
            chimney(cx + rng.uniform(-2, 2), cy + rng.uniform(-2, 2), H + (1.2 if kind == 'hip' else 0), rng)
    return front_any

def rubble(cx, cy, rng, n):
    note('dong_gach_vun', n)
    for k in range(n):
        s = rng.uniform(0.3, 1.1); box('da_hoc' if k % 3 else 'gach', (cx + rng.uniform(-2.5, 2.5), cy + rng.uniform(-2.5, 2.5), s * 0.25), (s, s * 0.8, s * 0.5), rng.uniform(0, 3), pitch=rng.uniform(-0.4, 0.4))

# ---------------------------------------------------------------- đặt khối nhà theo mốc
blocks = S.load(EP, kinds=['nha', 'khoi_pho', 'phao_dai', 'cong_su'], R=900)
polys = [b['pts'] for b in blocks if not b['line']]
meta_bl = []
def cen(pts): return sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)
if EP == 1943:
    for j, b in enumerate(blocks):
        if b['line'] or b['loai'] != 'nha': continue
        n = (b['tang'] or 3) + (R.random() < 0.35)
        if CM.dist_path(SITE, *cen(b['pts'])) > SITE['keep_d']: continue
        building(b['pts'], polys, j, n, R, 0.0)
        meta_bl.append(b['id'])
else:
    # 1782: khối phố (22 khối, Drinkwater) → chia lô dọc mép khối hở; công sự (gồm King's Bastion theo plan) KHÔNG dựng ở đây — bastion lấy OSM (bastion() dưới)
    for j, b in enumerate(blocks):
        if b['line']: continue
        if CM.dist_path(SITE, *cen(b['pts'])) > SITE['keep_d']: continue
        if b['loai'] in ('cong_su', 'phao_dai'): continue
        n = b['tang'] or 2
        building(b['pts'], polys, j, n + (R.random() < 0.25), R, ruin_p=0.42)
        meta_bl.append(b['id'])
LOG['ghost_ids'] = meta_bl

CUR[0] = 9000
# ---------------------------------------------------------------- mặt đất, Line Wall, biển, đồi bên kia vịnh
KB_POLYS = []
if A.site == 'kb':   # King's Bastion: footprint OSM (way 952588383 = bastion; 256821558 = phần sau, nay Leisure Centre) — như V5b-2b (vinh1782.js)
    _osm = json.load(open(os.path.join(HERE, '..', 'data', 'osm-kings-bastion.json')))
    for _w in ('952588383', '256821558'):
        _pts = [S.local(lo, la) for lo, la in _osm['ways'][_w]['lonlat']]
        if _pts[0] == _pts[-1]: _pts = _pts[:-1]
        if S.area(_pts) < 0: _pts = _pts[::-1]
        if KB_POLYS:   # gộp đỉnh của phần sau vào đỉnh bastion gần nhất (≤ 1,5 m; OSM hai way lệch 0,5–0,8 m) → cạnh chung khít, không khe
            _pts = [min(KB_POLYS[0], key=lambda q: math.dist(q, p)) if min(math.dist(q, p) for q in KB_POLYS[0]) <= 1.5 else p for p in _pts]
        KB_POLYS.append(_pts)
GX0, GY0, GX1, GY1 = SITE['ground']
WALLX = None
for b in S.load(1782, kinds=['chien_tuyen'], R=900):
    xs = [p for p in b['pts'] if GY0 - 10 < p[1] < GY1 + 10]
    if xs and abs(sum(p[0] for p in xs) / len(xs) + 110) < 60: WALLX = xs; break
if not WALLX: WALLX = [(-112, GY0), (-110, GY1)]
if A.site == 'kb':
    _lw = {b['id']: b['pts'] for b in S.load(1782, kinds=['cong_su'], R=900) if b['line']}
    _r = KB_POLYS[1]; _e = sorted([p for p in _r if p[0] > -122], key=lambda p: p[1])          # cạnh đông phần sau bastion (x ≈ −120 … −114)
    WALLX = [p for p in _lw.get('C1782-06', []) if p[1] < _e[0][1] - 1] + _e + [p for p in _lw.get('C1782-07', []) if p[1] > _e[-1][1] + 1]
WALLX = sorted(WALLX, key=lambda p: p[1])
def wx(y):   # x của Line Wall tại y (nội suy tuyến tính giữa các điểm ghost; PT dùng điểm gần nhất)
    if y <= WALLX[0][1]: return WALLX[0][0]
    for (xa, ya), (xb, yb) in zip(WALLX[:-1], WALLX[1:]):
        if ya <= y <= yb: return xa + (xb - xa) * (y - ya) / max(1e-6, yb - ya)
    return WALLX[-1][0]
gx0 = -125 if EP == 1943 else max(p[0] for p in WALLX) + 0.5   # kb: biển phủ tới Line Wall; mặt đất cắt theo wx(y) từng hàng ô
CUR[0] = 9800   # mặt đất chia ô 8 m (để mỗi ô ánh xạ được vào bản ghép vân 'top' của HC7)
_gxa = gx0 if EP == 1943 else min(p[0] for p in WALLX)
_xs = [_gxa] + list(range(int(math.ceil(_gxa / 8.0)) * 8, int(GX1), 8)) + [GX1]; _ys = [GY0] + list(range(int(math.ceil(GY0 / 8.0)) * 8, int(GY1), 8)) + [GY1]
for _i in range(len(_xs) - 1):
    for _j in range(len(_ys) - 1):
        _xa = _xs[_i] if EP == 1943 else max(_xs[_i], wx((_ys[_j] + _ys[_j + 1]) / 2))
        if _xs[_i + 1] - _xa > 0.01 and _ys[_j + 1] - _ys[_j] > 0.01:
            B['lat'].face([(_xa, _ys[_j], 0), (_xs[_i + 1], _ys[_j], 0), (_xs[_i + 1], _ys[_j + 1], 0), (_xa, _ys[_j + 1], 0)])
CUR[0] = 9700; B['bien'].face([(-16000, -16000, -5.5), (gx0, -16000, -5.5), (gx0, 16000, -5.5), (-16000, 16000, -5.5)])
# Line Wall: mặt tường đá dốc ra biển + tường chắn có lỗ châu mai (1782) / lan can (1943)
CUR[0] = 9000
ys = list(range(int(GY0), int(GY1) + 1, 6))
for k in range(len(ys) - 1):
    y0, y1 = ys[k], ys[k + 1]; x0, x1 = wx(y0), wx(y1)
    B['da_voi'].face([(x0 - 1.2, y0, -5.6), (x1 - 1.2, y1, -5.6), (x1, y1, 0.0), (x0, y0, 0.0)])
    B['lat'].face([(x0, y0, 0.0), (x1, y1, 0.0), (gx0 + 30 if False else x1 + 0.01, y1, 0.0), (x0 + 0.01, y0, 0.0)])
    if any(S.inside((x0 + x1) / 2 - 0.6, (y0 + y1) / 2, q) for q in KB_POLYS): continue
    if EP == 1782:
        if k % 2 == 0: box('da_voi', ((x0 + x1) / 2 + 0.6, (y0 + y1) / 2, 0.8), (1.6, (y1 - y0) * 0.62, 1.6), math.pi / 2)
    else:
        box('da_voi', ((x0 + x1) / 2 + 0.4, (y0 + y1) / 2, 0.55), (0.7, y1 - y0, 1.1), math.pi / 2)
gnd_w = wx(0)
if EP == 1943: B['lat'].face([(gnd_w, GY0, 0), (gx0, GY0, 0), (gx0, GY1, 0), (gnd_w, GY1, 0)][::-1])

def newell(pts):
    nx = ny = nz = 0.0
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        nx += (a[1] - b[1]) * (a[2] + b[2]); ny += (a[2] - b[2]) * (a[0] + b[0]); nz += (a[0] - b[0]) * (a[1] + b[1])
    n = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
    return nx / n, ny / n, nz / n
# ---------------------------------------------------------------- King's Bastion (1782): công sự đá theo footprint OSM — hình học từ nguồn, KHÔNG AI
KB_Z0, KB_TOP, KB_PAR = -5.5, 1.2, 3.2     # chân tường (mặt biển), mặt sàn pháo (terreplein), đỉnh tường chắn — cao tổng ≈ 8,7 m (V5b-2b ước 9 m)
KB_LOG = {'canh_ngoai': 0, 'lo_chau_mai': 0, 'phao': 0}; UNION = []
def earclip(poly):
    """tam giác hoá đa giác đơn (cắt tai, O(n³) — đủ cho ≤ 100 đỉnh); trả tam giác ngược chiều kim đồng hồ."""
    P = list(poly)
    if S.area(P) < 0: P = P[::-1]
    def cross(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    def inside_t(p, a, b, c): return cross(a, b, p) >= 0 and cross(b, c, p) >= 0 and cross(c, a, p) >= 0
    idx = list(range(len(P))); out = []; guard = 0
    while len(idx) > 3 and guard < 10000:
        guard += 1; done = False
        for k in range(len(idx)):
            i0, i1, i2 = idx[k - 1], idx[k], idx[(k + 1) % len(idx)]; a, b, c = P[i0], P[i1], P[i2]
            if cross(a, b, c) <= 1e-9: continue
            if any(inside_t(P[j], a, b, c) for j in idx if j not in (i0, i1, i2)): continue
            out.append((a, b, c)); idx.pop(k); done = True; break
        if not done: break
    if len(idx) == 3: out.append(tuple(P[i] for i in idx))
    return out

def bastion():
    """tường đá (scarp) từ mặt biển tới sàn pháo + gờ đá; tường chắn dày 2,4 m dạng VÀNH LIỀN (góc vát theo phân giác — không hở góc),
    lỗ châu mai mỗi ~7 m; cạnh chung hai footprint: không tường, thêm dải sàn 2,5 m lấp khe giữa hai polygon OSM."""
    CUR[0] = 8000; rng = random.Random(1773); T = 2.4
    for pi_, poly in enumerate(KB_POLYS):
        n = len(poly); other = [q for q in KB_POLYS if q is not poly]
        CURG[0] = 0
        # phân loại cạnh
        kind = []
        for i in range(n):
            p0, p1 = poly[i], poly[(i + 1) % n]; L = math.dist(p0, p1)
            if L < 0.05: kind.append('skip'); continue
            fr = Frame(p0, p1); mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2; ox, oy = mx + fr.w[0] * 1.0, my + fr.w[1] * 1.0
            if any(S.inside(ox, oy, q) for q in other) or any(S.inside(mx + fr.w[0] * 2.5, my + fr.w[1] * 2.5, q) for q in other): kind.append('chung')
            elif ox < wx(oy) - 0.5: kind.append('bien')
            else: kind.append('dat')
        # đỉnh trong của vành (vát theo phân giác) cho cạnh có tường chắn
        def inner(i):
            a_, b_, c_ = poly[i - 1], poly[i], poly[(i + 1) % n]
            def nrm(p, q):
                dx, dy = q[0] - p[0], q[1] - p[1]; L = math.hypot(dx, dy) or 1; return (-dy / L, dx / L)   # pháp tuyến TRONG (polygon ngược chiều kim đồng hồ)
            n1, n2 = nrm(a_, b_), nrm(b_, c_); bx, by = n1[0] + n2[0], n1[1] + n2[1]; bl = math.hypot(bx, by)
            if bl < 1e-6: return (b_[0] + n2[0] * T, b_[1] + n2[1] * T)
            cs = (bx * n2[0] + by * n2[1]) / bl; d = T / max(cs, 0.35)
            return (b_[0] + bx / bl * d, b_[1] + by / bl * d)
        UNION.extend((poly[i], poly[(i + 1) % n]) for i in range(n) if kind[i] not in ('chung', 'skip'))
        def perp(i, at_end):
            p0_, p1_ = poly[i], poly[(i + 1) % n]; dx, dy = p1_[0] - p0_[0], p1_[1] - p0_[1]; L_ = math.hypot(dx, dy) or 1; nx_, ny_ = -dy / L_, dx / L_
            b_ = p1_ if at_end else p0_; return (b_[0] + nx_ * T, b_[1] + ny_ * T)
        QS = [inner(i) if kind[i - 1] == 'bien' else perp(i, False) for i in range(n)]          # đầu cạnh i
        QE = [inner((i + 1) % n) if kind[(i + 1) % n] == 'bien' else perp(i, True) for i in range(n)]   # cuối cạnh i
        for i in range(n):
            k = kind[i]
            if k in ('skip',): continue
            p0, p1 = poly[i], poly[(i + 1) % n]; L = math.dist(p0, p1); fr = Frame(p0, p1)
            if k == 'chung': continue   # cạnh chung (đỉnh đã gộp) — không tường
            sea = k == 'bien'; z0 = KB_Z0 if sea else 0.0
            CURG[0] = new_group(8000, p0, p1, z0, KB_PAR, i + 1000 * pi_); KB_LOG['canh_ngoai'] += 1
            B['da_voi'].face([fr.P(0, z0), fr.P(L, z0), fr.P(L, KB_TOP - 0.25), fr.P(0, KB_TOP - 0.25)])
            fr.box('da_voi', -0.05, L + 0.05, KB_TOP - 0.25, KB_TOP + 0.05, 0.0, 0.28)
            if not sea:
                B['da_voi'].face([fr.P(0, KB_TOP - 0.25), fr.P(L, KB_TOP - 0.25), fr.P(L, KB_TOP + 1.0), fr.P(0, KB_TOP + 1.0)])
                CURG[0] = 0; B['da_voi'].face([(*p1, KB_TOP + 1.0), (*p0, KB_TOP + 1.0), (*perp(i, False), KB_TOP + 1.0), (*perp(i, True), KB_TOP + 1.0)][::-1]); continue
            q0, q1 = QS[i], QE[i]
            def O(u, z): return (p0[0] + (p1[0] - p0[0]) * u / L, p0[1] + (p1[1] - p0[1]) * u / L, z)
            def I(u, z): return (q0[0] + (q1[0] - q0[0]) * u / L, q0[1] + (q1[1] - q0[1]) * u / L, z)
            ne = max(1, int(L / 7.0)) if L > 4.0 else 0; emb = [L * (k_ + 0.5) / ne for k_ in range(ne)]
            pieces = []; u = 0.0
            for e in emb: pieces.append((u, e - 0.5, KB_PAR)); pieces.append((e - 0.5, e + 0.5, KB_TOP + 0.95)); u = e + 0.5
            pieces.append((u, L, KB_PAR)); KB_LOG['lo_chau_mai'] += len(emb)
            for (a0, a1, zt) in pieces:
                if a1 - a0 < 0.02: continue
                CURG[0] = GRP.__len__() - 1
                B['da_voi'].face([O(a0, KB_TOP + 0.05), O(a1, KB_TOP + 0.05), O(a1, zt), O(a0, zt)])          # mặt ngoài (nhóm elev của cạnh)
                CURG[0] = 0
                B['da_voi'].face([O(a0, zt), O(a1, zt), I(a1, zt), I(a0, zt)])                             # mặt trên (pháp tuyến lên → 'top')
                B['da_voi'].face([I(a1, KB_TOP), I(a0, KB_TOP), I(a0, zt), I(a1, zt)])                     # mặt trong
            for (a0, a1, zt), (b0, b1, zb) in zip(pieces[:-1], pieces[1:]):   # má lỗ châu mai (giữa phần cao và phần thấp)
                lo, hi = min(zt, zb), max(zt, zb); u = a1
                B['da_voi'].face([O(u, lo), I(u, lo), I(u, hi), O(u, hi)][::(1 if zt > zb else -1)])
            for e in emb:
                if rng.random() < 0.7:   # pháo trên bệ gỗ, nòng qua lỗ châu mai (đồ vật A, không nhận vân AI)
                    KB_LOG['phao'] += 1; CUR[0] = 8100; c = fr.P(e, 0, -T - 1.6)
                    box('go', (c[0], c[1], KB_TOP + 0.35), (0.9, 1.6, 0.45), fr.yaw, tint=(0.3, 0.22, 0.15))
                    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.2, depth=2.8, location=(*fr.P(e, 0, -T - 0.4)[:2], KB_TOP + 0.85), rotation=(math.pi / 2, 0, fr.yaw))
                    o = bpy.context.object; o.data.materials.append(M['dong']); EXTRA.append(o); CUR[0] = 8000
            # đầu vành khi cạnh kề không có tường chắn
            for j, (pp, qq) in ((i - 1, (p0, q0)), ((i + 1) % n, (p1, q1))):
                if kind[j] != 'bien': B['da_voi'].face([(*pp, KB_TOP), (*qq, KB_TOP), (*qq, KB_PAR), (*pp, KB_PAR)])
    # sàn pháo: MỘT mặt theo đường bao hợp của hai footprint (tránh hai mặt trùng phẳng chồng nhau → vệt đen)
    CURG[0] = 0; CUR[0] = 8000
    left = list(UNION[1:]); loop = [UNION[0][0], UNION[0][1]]; KB_LOG['noi_hop_m'] = []
    while left:   # nối cạnh kế tiếp: đỉnh đầu trùng đỉnh cuối hiện tại; nếu không có, cạnh có đỉnh đầu gần nhất (≤ 3 m — chỗ hai way OSM chạm lệch)
        j = min(range(len(left)), key=lambda k_: math.dist(left[k_][0], loop[-1])); d_ = math.dist(left[j][0], loop[-1])
        if d_ > 3.0: break
        if d_ > 1e-6: KB_LOG['noi_hop_m'].append(round(d_, 2))
        a_, b_ = left.pop(j)
        if d_ > 1e-6: loop.append(a_)
        loop.append(b_)
    if math.dist(loop[-1], loop[0]) < 1e-6: loop.pop()
    ch = True
    while ch and len(loop) > 3:   # bỏ đỉnh "gai" (đường bao quay ngược ≥ 150° ở chỗ nối lệch) — tránh đa giác tự cắt
        ch = False
        for k_ in range(len(loop)):
            a_, b_, c_ = loop[k_ - 1], loop[k_], loop[(k_ + 1) % len(loop)]
            u_ = (b_[0] - a_[0], b_[1] - a_[1]); v_ = (c_[0] - b_[0], c_[1] - b_[1]); nu, nv = math.hypot(*u_), math.hypot(*v_)
            if nu < 1e-6 or nv < 1e-6 or (u_[0] * v_[0] + u_[1] * v_[1]) / (nu * nv) < -0.866: loop.pop(k_); KB_LOG['bo_gai'] = KB_LOG.get('bo_gai', 0) + 1; ch = True; break
    KB_LOG['bao_hop_dinh'] = len(loop); KB_LOG['bao_hop_kin'] = not left; KB_LOG['bao_hop'] = [[round(x, 1), round(y, 1)] for x, y in loop]
    rings_ = [loop] if not left else KB_POLYS
    for r_ in rings_:
        for tri in earclip(r_): B['lat'].face([(x, y, KB_TOP) for x, y in tri])
    CURG[0] = 0; LOG['bastion'] = KB_LOG

def hills():
    CUR[0] = 9600; rng = random.Random(11); pts = []
    for k in range(121):
        az = math.radians(170 + k * 1.2)      # cung tây nam → tây bắc (bờ vịnh Algeciras / Sierra)
        dist = 9000 + 2500 * math.sin(k * 0.13)
        h = 120 + 160 * (0.5 + 0.5 * math.sin(k * 0.17 + 1)) + 60 * math.sin(k * 0.53) ** 2 + (330 if 30 < k < 70 else 0) * math.sin((k - 30) / 40 * math.pi) ** 2
        pts.append((math.sin(az) * dist, math.cos(az) * dist, h))
    for k in range(len(pts) - 1):
        a, b = pts[k], pts[k + 1]
        B['doi'].face([(a[0], a[1], -6), (b[0], b[1], -6), (b[0], b[1], b[2]), (a[0], a[1], a[2])])
hills()

# ---------------------------------------------------------------- tàu hậu cảnh (thủ tục; buồm = khe 'vai')
def ship_sail(x, y, yaw, L, rng, set_sails):
    note('tau_buom'); h = L * 0.11
    box('son', (x, y, -5.5 + h / 2), (L, L * 0.27, h), yaw, tint=(0.18, 0.13, 0.09)); box('son', (x, y, -5.5 + h * 0.98), (L * 0.98, L * 0.25, 0.25), yaw, tint=(0.75, 0.62, 0.3))
    box('son', (x - math.cos(yaw) * L * 0.42, y - math.sin(yaw) * L * 0.42, -5.5 + h * 1.25), (L * 0.16, L * 0.25, h * 0.5), yaw, tint=(0.2, 0.15, 0.1))
    for k, f in enumerate((-0.28, 0.02, 0.3)):
        mx, my = x + math.cos(yaw) * L * f, y + math.sin(yaw) * L * f; mh = L * (0.85 if k == 1 else 0.72)
        box('go', (mx, my, -5.5 + h + mh / 2), (0.5, 0.5, mh), yaw, tint=(0.3, 0.22, 0.15))
        for j, yy in enumerate((0.35, 0.6, 0.82)):
            yl = L * (0.42 - 0.1 * j) * (0.9 if k != 1 else 1)
            box('go', (mx, my, -5.5 + h + mh * yy), (0.3, yl, 0.3), yaw, tint=(0.3, 0.22, 0.15))
            if set_sails:
                box('vai', (mx + math.cos(yaw) * 0.6, my + math.sin(yaw) * 0.6, -5.5 + h + mh * (yy - 0.11)), (0.25, yl * 0.92, mh * 0.21), yaw, tint=(0.9, 0.86, 0.76))
            else:
                box('vai', (mx, my, -5.5 + h + mh * yy - 0.35), (0.6, yl * 0.85, 0.5), yaw, tint=(0.85, 0.8, 0.7))
    box('go', (x + math.cos(yaw) * L * 0.62, y + math.sin(yaw) * L * 0.62, -5.5 + h * 1.5), (L * 0.3, 0.35, 0.35), yaw, tint=(0.3, 0.22, 0.15), pitch=0.0)

def ship_steam(x, y, yaw, L, rng, kind):
    note('tau_may_' + kind); h = L * 0.09; grey = (0.42, 0.44, 0.46) if kind == 'chien' else (0.2, 0.18, 0.17)
    box('son', (x, y, -5.5 + h / 2), (L, L * 0.12, h), yaw, tint=grey)
    box('son', (x + math.cos(yaw) * L * 0.43, y + math.sin(yaw) * L * 0.43, -5.5 + h / 2), (L * 0.14, L * 0.07, h), yaw, tint=grey)
    box('son', (x - math.cos(yaw) * L * 0.05, y - math.sin(yaw) * L * 0.05, -5.5 + h * 1.6), (L * 0.28, L * 0.1, h * 1.2), yaw, tint=(0.5, 0.5, 0.5) if kind == 'chien' else (0.85, 0.83, 0.78))
    fx, fy = x - math.cos(yaw) * L * 0.12, y - math.sin(yaw) * L * 0.12
    box('son', (fx, fy, -5.5 + h * 2.6), (L * 0.06, L * 0.06, h * 1.4), yaw, tint=(0.12, 0.12, 0.12) if kind == 'chien' else (0.6, 0.25, 0.12))
    CHIM.append((fx, fy, -5.5 + h * 3.3))
    for f in (0.3, -0.3): box('sat', (x + math.cos(yaw) * L * f, y + math.sin(yaw) * L * f, -5.5 + h * 3.2), (0.3, 0.3, h * 3), yaw)
    if kind == 'chien':
        for f in (0.28, -0.32): box('son', (x + math.cos(yaw) * L * f, y + math.sin(yaw) * L * f, -5.5 + h * 1.25), (L * 0.06, L * 0.05, h * 0.5), yaw, tint=grey)

rs = random.Random(5)
CUR[0] = 9900
if EP == 1782:
    for (dx, dy, L, ss) in ((-650, -220, 48, False), (-1100, 130, 52, False), (-1900, -600, 55, True), (-2600, 420, 50, False), (-3400, -150, 45, True), (-4200, -900, 40, False)):
        ship_sail(dx, dy, rs.uniform(0, math.pi), L, rs, ss)
    for k in range(5): box('son', (-300 - k * 140, -60 + k * 70, -5.3), (6, 2.2, 0.8), rs.uniform(0, 3), tint=(0.25, 0.18, 0.12)); note('thuyen_nho')
else:
    for (dx, dy, L, kd) in ((-700, -160, 110, 'chien'), (-1250, 220, 140, 'hang'), (-2100, -450, 160, 'hang'), (-2900, 260, 120, 'chien'), (-3800, -800, 150, 'hang')):
        ship_steam(dx, dy, rs.uniform(0, math.pi), L, rs, kd)
    ship_sail(-520, 90, 0.4, 14, rs, True)     # thuyền buồm đánh cá nhỏ trong cảng (còn thấy ở vịnh thập niên 1940)

# ---------------------------------------------------------------- đồ phố theo thời kỳ (đặt trong vùng trống trước máy)
def free(x, y, r=1.5):
    if x < wx(y) + 2: return False
    return all(not S.inside(x + dx, y + dy, q) for q in polys for dx, dy in ((0, 0), (r, 0), (-r, 0), (0, r), (0, -r)))

def barrel(x, y, rng, tint=(0.35, 0.25, 0.15)):
    note('thung')
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.33, depth=0.85, location=(x, y, 0.425)); o = bpy.context.object
    o.data.materials.append(M['go']); EXTRA.append(o)
    for z in (0.15, 0.7):
        bpy.ops.mesh.primitive_torus_add(major_radius=0.34, minor_radius=0.02, location=(x, y, z)); t = bpy.context.object; t.data.materials.append(M['sat']); EXTRA.append(t)

def cart(x, y, yaw, rng, two_wheel=True):
    note('xe_keo'); tn = (0.38, 0.28, 0.18)
    box('go', (x, y, 0.75), (2.2, 1.3, 0.08), yaw, tint=tn)
    for s in (-1, 1): box('go', (x - math.sin(yaw) * 0.62 * s, y + math.cos(yaw) * 0.62 * s, 0.95), (2.2, 0.06, 0.35), yaw, tint=tn)
    box('go', (x + math.cos(yaw) * 1.8, y + math.sin(yaw) * 1.8, 0.6), (1.6, 0.09, 0.09), yaw, tint=tn, pitch=0.0)
    for s in (-1, 1):
        bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=0.62, depth=0.09, location=(x - math.sin(yaw) * 0.72 * s, y + math.cos(yaw) * 0.72 * s, 0.62),
                                            rotation=(math.pi / 2, 0, yaw)); o = bpy.context.object; o.data.materials.append(M['go']); EXTRA.append(o)

def lamp_post(x, y, rng):
    note('den_duong'); box('sat', (x, y, 1.7), (0.12, 0.12, 3.4)); box('sat', (x, y, 0.3), (0.3, 0.3, 0.6))
    box('sat', (x, y, 3.55), (0.32, 0.32, 0.04)); box('den', (x, y, 3.75), (0.24, 0.24, 0.36)); box('sat', (x, y, 4.0), (0.36, 0.36, 0.1))
    LAMPS.append((x, y, 3.75))

def shot_pile(x, y, rng):   # đống đạn pháo xếp tháp (1782)
    note('dong_dan_phao')
    for lv in range(4):
        n = 4 - lv
        for i in range(n):
            for j in range(n):
                bpy.ops.mesh.primitive_uv_sphere_add(segments=10, ring_count=6, radius=0.12, location=(x + (i - (n - 1) / 2) * 0.24, y + (j - (n - 1) / 2) * 0.24, 0.12 + lv * 0.17))
                o = bpy.context.object; o.data.materials.append(M['sat']); EXTRA.append(o)

def cannon(x, y, yaw):
    note('phao'); box('go', (x, y, 0.35), (1.6, 0.9, 0.45), yaw, tint=(0.3, 0.22, 0.15))
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.2, depth=2.8, location=(x + math.cos(yaw) * 0.4, y + math.sin(yaw) * 0.4, 0.85), rotation=(0, math.pi / 2, yaw))
    o = bpy.context.object; o.data.materials.append(M['dong']); EXTRA.append(o)

def stall(x, y, yaw, rng):
    note('quay_hang'); tn = (0.4, 0.3, 0.2)
    box('go', (x, y, 0.9), (2.2, 1.0, 0.06), yaw, tint=tn)
    for sx in (-1, 1):
        for sy in (-1, 1):
            box('go', (x + math.cos(yaw) * sx * 1.0 - math.sin(yaw) * sy * 0.45, y + math.sin(yaw) * sx * 1.0 + math.cos(yaw) * sy * 0.45, 1.1), (0.06, 0.06, 2.2), yaw, tint=tn)
    box('vai', (x, y, 2.25), (2.5, 1.5, 0.04), yaw, tint=rng.choice([(0.85, 0.8, 0.7), (0.7, 0.4, 0.3)]), pitch=0.12)
    for k in range(5): box('go' if k % 2 else 'vai', (x + math.cos(yaw) * (k - 2) * 0.4, y + math.sin(yaw) * (k - 2) * 0.4, 1.05), (0.32, 0.32, 0.24), yaw, tint=rng.choice([(0.6, 0.45, 0.25), (0.8, 0.7, 0.4), (0.5, 0.6, 0.3)]))

def truck(x, y, yaw):
    note('xe_tai_quan_su'); ol = (0.3, 0.32, 0.22)
    box('son', (x, y, 1.0), (5.8, 2.2, 0.5), yaw, tint=(0.15, 0.15, 0.13))
    box('son', (x + math.cos(yaw) * 2.0, y + math.sin(yaw) * 2.0, 1.75), (1.6, 2.1, 1.4), yaw, tint=ol)
    box('vai', (x - math.cos(yaw) * 0.9, y - math.sin(yaw) * 0.9, 2.1), (3.8, 2.25, 1.9), yaw, tint=(0.38, 0.36, 0.26))
    box('kinh', (x + math.cos(yaw) * 2.81, y + math.sin(yaw) * 2.81, 2.0), (0.02, 1.8, 0.6), yaw)
    for f in (1.9, -1.3, -2.3):
        for s in (-1, 1):
            bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=0.48, depth=0.3, location=(x + math.cos(yaw) * f - math.sin(yaw) * 1.0 * s, y + math.sin(yaw) * f + math.cos(yaw) * 1.0 * s, 0.48), rotation=(math.pi / 2, 0, yaw))
            o = bpy.context.object; o.data.materials.append(M['sat']); EXTRA.append(o)

def flagpole(x, y, h):
    note('cot_co'); box('son', (x, y, h / 2), (0.12, 0.12, h), tint=(0.92, 0.92, 0.9)); box('son', (x, y, h + 0.08), (0.2, 0.2, 0.16), tint=(0.7, 0.6, 0.3))
    FLAGS.append((x, y, h - 0.05))

def sentry_box(x, y, yaw):
    note('chot_gac'); box('go', (x, y, 1.2), (1.1, 1.1, 2.4), yaw, tint=(0.75, 0.68, 0.55)); box('go', (x, y, 2.55), (1.3, 1.3, 0.3), yaw, tint=(0.3, 0.22, 0.15))
    box('trong', (x + math.cos(yaw) * 0.56, y + math.sin(yaw) * 0.56, 1.1), (0.02, 0.7, 1.9), yaw)

def shelter():   # lối xuống hầm trú ẩn dưới Commercial Square (xây 1939 — ảnh Commons, chỉ tham chiếu)
    note('ham_tru_an'); x, y = -40, 12
    box('vua', (x, y, 1.1), (5.0, 3.2, 2.2), 0.1, tint=(0.62, 0.6, 0.55)); box('vua', (x, y, 2.3), (5.4, 3.6, 0.2), 0.1, tint=(0.55, 0.53, 0.5))
    box('trong', (x + 2.51, y + 0.25, 0.9), (0.02, 1.4, 1.8), 0.1); sandbags(Frame((x + 2.6, y - 1.8), (x + 2.6, y + 1.8)), 0.0, 1.2, rng=R)

EXTRA = []; LAMPS = []; FLAGS = []; CUR[0] = 9500
if EP == 1782:
    for (x, y) in ((-30, -8), (-36, -2), (-55, 14)):
        if free(x, y): shot_pile(x, y, R)
    for (x, y, yw) in ((-20, -18, 0.4), (-62, 4, 2.0)):
        if free(x, y, 2.5): cart(x, y, yw, R)
    for (x, y) in ((-14, -12), (-15, -10.8), (-13.6, -11), (-45, 18), (-46, 19.1), (-70, -10)):
        if free(x, y, 0.5): barrel(x, y, R)
    cannon(wx(-30) + 2.2, -30, math.pi); cannon(wx(-6) + 2.2, -6, math.pi); cannon(wx(20) + 2.2, 20, math.pi); cannon(wx(44) + 2.2, 44, math.pi)
    sentry_box(-8, 18, -math.pi / 2); lamp_post(-6.5, 16.5, R)
    flagpole(wx(8) + 4, 8, 12.0)
    for (x, y) in ((-25, 22), (-60, -14), (-14, 8), (-40, -22), (-8, -18)):
        if free(x, y, 2): rubble(x, y, R, 9)
    for (x, y) in ((-18, -4), (-48, 6), (-33, -14), (-12, -26)):
        if free(x, y): shot_pile(x, y, R)
    for (x, y, yw) in ((-28, 4, 1.2), (-52, -20, 2.6)):
        if free(x, y, 2.5): cart(x, y, yw, R)
    for k in range(7):   # đống gỗ xẻ / dầm (sửa chữa sau pháo kích)
        x, y = -22 + R.uniform(-2, 2), -10 + R.uniform(-1.5, 1.5)
        if free(x, y, 1): box('go', (x, y, 0.12 + 0.22 * (k % 3)), (4.0, 0.22, 0.2), 0.3 + R.uniform(-0.05, 0.05), tint=(0.42, 0.32, 0.22)); note('dong_go')
    for (x, y) in ((-10, -6), (-10.8, -6.6), (-36, 10), (-36.7, 10.6), (-37.4, 10.1)):
        if free(x, y, 0.5): barrel(x, y, R)
else:
    shelter()
    for (x, y) in ((-6, -10), (-28, 26), (-52, -6), (-75, 22), (-95, 0)):
        if free(x, y, 0.6): lamp_post(x, y, R)
    for (x, y, yw) in ((-58, 26, 0.3),):
        if free(x, y, 3.5): truck(x, y, yw)
    for (x, y, yw) in ((-16, -16, 1.2), (-70, -16, 0.2)):
        if free(x, y, 2.5): cart(x, y, yw, R)
    for (x, y, yw) in ((-24, -20, 0.1), (-31, -21, 0.05)):
        if free(x, y, 1.5): stall(x, y, yw, R)
    for (x, y) in ((-12, -14), (-12.8, -13.2), (-48, 20), (-49, 21)):
        if free(x, y, 0.5): barrel(x, y, R)
    flagpole(wx(8) + 4, 8, 12.0)
if A.site == 'kb': bastion()
LOG['lamps'] = LAMPS; LOG['flags'] = FLAGS; LOG['chimneys'] = CHIM

# ---------------------------------------------------------------- PT3: gán nhóm chiếu cho từng mặt + UV vào atlas (HC7)
TOPR = CM.SITE[A.site].get('top_rect')            # (x0, y0, x1, y1): vùng bản ghép 'top' (mái, sàn pháo, mặt đường)
TOP_BIDS = CM.SITE[A.site].get('top_bids')        # None = mọi toà + mặt đất 9800; hoặc danh sách bid
MAN = None
if A.tex == 'HC7':
    MAN = json.load(open(os.path.join(A.atlas, 'manifest.json')))   # {'elev': {bid: {file, W, H, groups: {g: {x0, zmin, zmax, ppm}}}}, 'top': {file, rect, W, H}}
def assign(k, pts, bid, g):
    """→ ('elev', g) · ('top', 0) · None. Điều kiện hình học, không phụ thuộc atlas có hay chưa (probe/elev dùng để biết mặt nào CÓ THỂ nhận vân)."""
    if k not in ELIG: return None
    n = newell(pts); c = [sum(p[i] for p in pts) / len(pts) for i in range(3)]
    if g > 0:
        G = GRP[g]; wdot = n[0] * G['w'][0] + n[1] * G['w'][1]
        off = (c[0] - G['p0'][0]) * G['w'][0] + (c[1] - G['p0'][1]) * G['w'][1]
        if wdot > 0.7 and -1.0 < off < 3.0: return ('elev', g, abs(off) < 0.03 and (EP == 1782 or k == 'vua'))   # cờ 'phẳng': mặt tường vữa nằm trên mặt phẳng tường (phần nhô giữ A)
    if n[2] > 0.7 and TOPR and TOPR[0] <= c[0] <= TOPR[2] and TOPR[1] <= c[1] <= TOPR[3]:
        if TOP_BIDS is None and bid < 9000 or bid == 9800 or (TOP_BIDS and bid in TOP_BIDS): return ('top', 0, True)
    return None

def m_atlas(name, path, bump=0.25):
    """albedo = ảnh atlas (vân AI đã nướng + đều sáng); độ nhám + bump suy từ độ sáng của chính atlas (phép toán, như PT §6)."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; N = nt.nodes; L = nt.links; b = N['Principled BSDF']
    uv = N.new('ShaderNodeUVMap'); uv.uv_map = 'ai_uv'; t = N.new('ShaderNodeTexImage'); t.image = img(path); t.interpolation = 'Cubic'; t.extension = 'EXTEND'
    L.new(uv.outputs['UV'], t.inputs['Vector']); L.new(t.outputs['Color'], b.inputs['Base Color'])
    bw = N.new('ShaderNodeRGBToBW'); L.new(t.outputs['Color'], bw.inputs[0])
    mr = N.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value = 0.95; mr.inputs['To Max'].default_value = 0.6
    L.new(bw.outputs[0], mr.inputs['Value']); L.new(mr.outputs[0], b.inputs['Roughness'])
    bp = N.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump; bp.inputs['Distance'].default_value = 0.02
    L.new(bw.outputs[0], bp.inputs['Height']); L.new(bp.outputs['Normal'], b.inputs['Normal'])
    ao = N.new('ShaderNodeOutputAOV'); ao.aov_name = 'ai'; ao.inputs['Value'].default_value = 1.0   # AOV 'ai' = 1 trên mặt có vân AI
    return m
ATLAS_M = {}
def atlas_mat(key, path):
    if key not in ATLAS_M: ATLAS_M[key] = m_atlas('hc7_' + key, path)
    return ATLAS_M[key]

# ---------------------------------------------------------------- tạo đối tượng từ bộ đệm: một đối tượng mỗi (khe vật liệu, toà) — pass_index = bid
OBJ = {}; STAT = {'faces': 0, 'elig_faces': 0, 'elev_faces': 0, 'top_faces': 0, 'ai_faces': 0, 'ai_area_m2': 0.0, 'elig_area_m2': 0.0}
def farea(pts):
    n = [0.0, 0.0, 0.0]
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        n[0] += a[1] * b[2] - a[2] * b[1]; n[1] += a[2] * b[0] - a[0] * b[2]; n[2] += a[0] * b[1] - a[1] * b[0]
    return 0.5 * math.sqrt(sum(c * c for c in n))
def flush(k, buf):
    if not buf.f: return
    by = {}
    for i, b in enumerate(buf.bid): by.setdefault(b, []).append(i)
    for bid, idx in by.items():
        vs = []; fs = []; uvs = []; mi = []; grp = []; flat = []; mats = [M[k]]
        for i in idx:
            pts = [buf.v[j] for j in buf.f[i]]; j0 = len(vs); vs.extend(pts); fs.append(tuple(range(j0, j0 + len(pts))))
            a = assign(k, pts, bid, buf.grp[i]); STAT['faces'] += 1; ar = farea(pts)
            if k in ELIG: STAT['elig_faces'] += 1; STAT['elig_area_m2'] += ar
            if a: STAT[a[0] + '_faces'] += 1
            grp.append(a[1] if a and a[0] == 'elev' else (-1 if a else 0)); flat.append(1.0 if a and a[2] else 0.0)
            uv = [(0.0, 0.0)] * len(pts); slot = 0
            if MAN and a:
                if a[0] == 'elev' and str(bid) in MAN['elev'] and str(a[1]) in MAN['elev'][str(bid)]['groups']:
                    E = MAN['elev'][str(bid)]; Gm = E['groups'][str(a[1])]; G = GRP[a[1]]
                    uv = [((Gm['x0'] + ((p[0] - G['p0'][0]) * G['u'][0] + (p[1] - G['p0'][1]) * G['u'][1]) * E['ppm']) / E['W'],
                           1.0 - (E['H'] - (p[2] - E['zmin']) * E['ppm']) / E['H']) for p in pts]
                    mat = atlas_mat(f'b{bid}', os.path.join(A.atlas, E['file']))
                elif a[0] == 'top' and MAN.get('top'):
                    T = MAN['top']; x0, y0, x1, y1 = T['rect']
                    uv = [((p[0] - x0) / (x1 - x0), (p[1] - y0) / (y1 - y0)) for p in pts]; mat = atlas_mat('top', os.path.join(A.atlas, T['file']))
                else: mat = None
                if mat is not None:
                    if mat not in mats: mats.append(mat)
                    slot = mats.index(mat); STAT['ai_faces'] += 1; STAT['ai_area_m2'] += ar
            mi.append(slot); uvs.extend(uv)
        name = f'{k}|{bid}'; me = bpy.data.meshes.new(name); me.from_pydata(vs, [], fs); me.update()
        at = me.attributes.new('tint', 'FLOAT_COLOR', 'FACE'); lt = me.attributes.new('lit', 'FLOAT', 'FACE'); gt = me.attributes.new('grp', 'FLOAT', 'FACE'); it = me.attributes.new('ai', 'FLOAT', 'FACE'); ft = me.attributes.new('flat', 'FLOAT', 'FACE')
        for n_, i in enumerate(idx): at.data[n_].color = (*buf.tint[i], 1.0); lt.data[n_].value = buf.lit[i]; gt.data[n_].value = float(grp[n_]); it.data[n_].value = 1.0 if mi[n_] > 0 else 0.0; ft.data[n_].value = flat[n_]
        ul = me.uv_layers.new(name='ai_uv')
        for li, lp in enumerate(me.loops): ul.data[li].uv = uvs[lp.vertex_index]
        for n_, p in enumerate(me.polygons): p.material_index = mi[n_]; p.use_smooth = False
        o = bpy.data.objects.new(name, me)
        for m_ in mats: o.data.materials.append(m_)
        o.pass_index = int(bid); o['k'] = k; o['bid'] = int(bid); sc.collection.objects.link(o); OBJ[name] = o
for k, buf in B.items(): flush(k, buf)
if os.environ.get('PT3_DEBUG'):   # gỡ lỗi: in các mặt có tâm trong hộp x0,y0,x1,y1
    bx = [float(v) for v in os.environ['PT3_DEBUG'].split(',')]
    for k, buf in B.items():
        for i, f in enumerate(buf.f):
            pts = [buf.v[j] for j in f]; c = [sum(p[q] for p in pts) / len(pts) for q in range(3)]
            if bx[0] <= c[0] <= bx[2] and bx[1] <= c[1] <= bx[3]: print('DBG', k, buf.bid[i], buf.grp[i], [tuple(round(x, 1) for x in p) for p in pts], [round(x, 2) for x in newell(pts)])
for o in EXTRA: o['k'] = 'extra'; o['bid'] = -1
LOG['faces'] = STAT['faces']; LOG['stat'] = {k: (round(v, 1) if isinstance(v, float) else v) for k, v in STAT.items()}
LOG['groups'] = [None] + [{k: (round(v, 3) if isinstance(v, float) else ([round(x, 3) for x in v] if isinstance(v, list) else v)) for k, v in G.items()} for G in GRP[1:]]
print('DỰNG', LOG['stat'], 'nhóm', len(GRP) - 1, 'đối tượng', len(OBJ), round(time.time() - T0, 1), 's', flush=True)

# ---------------------------------------------------------------- ánh sáng: mặt trời theo thiên văn (ngày 12/9, vĩ độ 36,14° B), bầu trời Nishita
LAT = math.radians(36.14); DECL = math.radians(4.0)
def sun_at(hour):   # giờ mặt trời biểu kiến
    Hh = math.radians((hour - 12) * 15)
    alt = math.asin(math.sin(LAT) * math.sin(DECL) + math.cos(LAT) * math.cos(DECL) * math.cos(Hh))
    az = math.atan2(math.sin(Hh), math.cos(Hh) * math.sin(LAT) - math.tan(DECL) * math.cos(LAT)) + math.pi
    return math.degrees(alt), math.degrees(az) % 360
world = bpy.data.worlds.new('w'); sc.world = world; world.use_nodes = True; wn = world.node_tree.nodes; wl = world.node_tree.links
bg = wn['Background']; sky = wn.new('ShaderNodeTexSky')
try: sky.sky_type = 'NISHITA'
except Exception: pass
wl.new(sky.outputs[0], bg.inputs[0])
sun = bpy.data.objects.new('sun', bpy.data.lights.new('sun', 'SUN')); sc.collection.objects.link(sun)
alt, az = sun_at(A.hour)
sun.rotation_euler = (math.radians(90 - alt), 0, math.radians(-az + 180))
sun.data.energy = 5.0 if alt > 12 else 2.8 + 2.2 * max(0, alt) / 12; sun.data.angle = math.radians(0.53)
warm = max(0.0, min(1.0, (20 - alt) / 20)); sun.data.color = (1.0, 1.0 - 0.4 * warm, 1.0 - 0.7 * warm)
sky.sun_elevation = math.radians(alt); sky.sun_rotation = math.radians(-az + 180 + 180)
try: sky.sun_disc = False
except Exception: pass
try: sky.air_density = 1.0; sky.dust_density = 1.6 if alt < 12 else 0.5; sky.ozone_density = 1.0
except Exception: pass
bg.inputs[1].default_value = 0.22 if alt > 12 else 0.3
LOG['sun'] = {'gio_mt': A.hour, 'alt': round(alt, 2), 'az': round(az, 2), 'ngay': '12/9 (như PT passes.json)'}

# ---------------------------------------------------------------- máy quay + dựng
cam = bpy.data.cameras.new('cam'); cam.sensor_width = S.SENSOR; cam.sensor_fit = 'HORIZONTAL'; cam.clip_start = 0.5; cam.clip_end = 40000
co = bpy.data.objects.new('cam', cam); sc.collection.objects.link(co); sc.camera = co
W, H = map(int, A.res.split('x')); sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = W, H, 100
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = A.spp; sc.cycles.use_denoising = True
sc.cycles.denoiser = 'OPENIMAGEDENOISE'; sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.02
sc.cycles.max_bounces = 4; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 2; sc.cycles.transmission_bounces = 2; sc.cycles.transparent_max_bounces = 4
sc.cycles.caustics_reflective = False; sc.cycles.caustics_refractive = False; sc.render.use_persistent_data = True
sc.cycles.seed = 20261018; sc.cycles.use_animated_seed = False
sc.view_settings.view_transform = 'AgX'
for lk in ('AgX - Medium High Contrast', 'Medium High Contrast', 'None'):
    try: sc.view_settings.look = lk; break
    except Exception: pass
sc.view_settings.exposure = 0.35; LOG['look'] = sc.view_settings.look
VL = sc.view_layers[0]
def set_cam(pos, look, mm):
    co.location = pos; co.rotation_euler = CM.blender_rot(pos, look); cam.type = 'PERSP'; cam.lens = mm
def render_exr(path, half=False):   # dựng + ghi EXR đa lớp (mọi lượt bật trong view layer)
    s_ = sc.render.image_settings; s_.media_type = 'MULTI_LAYER_IMAGE'; s_.file_format = 'OPEN_EXR_MULTILAYER'; s_.color_depth = '16' if half else '32'; s_.exr_codec = 'ZIP'
    sc.render.filepath = path; bpy.ops.render.render(write_still=True)
def png_out(path):
    s_ = sc.render.image_settings; s_.media_type = 'IMAGE'; s_.file_format = 'PNG'; s_.color_depth = '8'; s_.color_mode = 'RGB'
    bpy.data.images['Render Result'].save_render(path, scene=sc)
def frames():
    st = CM.SITE[A.site]; N = st['N']
    if A.frames:
        a, b = (int(x) for x in A.frames.split('-')); return list(range(a, b + 1, A.step))
    return list(range(0, N, A.step))
def show_only(pred):
    for o in list(OBJ.values()) + EXTRA: o.hide_render = not pred(o)
LOG['renders'] = []
# ---- chế độ albedo: mọi vật liệu có nhánh phát sáng = màu nền (Base Color) — bật bằng thuộc tính view layer 'alb' (không ánh sáng, không bóng)
VL['alb'] = 0.0
def add_albedo(m):
    nt = m.node_tree; N = nt.nodes; L = nt.links; b = N.get('Principled BSDF'); out = N.get('Material Output')
    if b is None or out is None or not out.inputs['Surface'].links: return
    src = out.inputs['Surface'].links[0].from_socket
    em = N.new('ShaderNodeEmission'); em.inputs['Strength'].default_value = 1.0
    if b.inputs['Base Color'].links: L.new(b.inputs['Base Color'].links[0].from_socket, em.inputs['Color'])
    else: em.inputs['Color'].default_value = b.inputs['Base Color'].default_value
    at = N.new('ShaderNodeAttribute'); at.attribute_type = 'VIEW_LAYER'; at.attribute_name = 'alb'
    mx = N.new('ShaderNodeMixShader'); L.new(at.outputs['Fac'], mx.inputs[0]); L.new(src, mx.inputs[1]); L.new(em.outputs[0], mx.inputs[2]); L.new(mx.outputs[0], out.inputs['Surface'])
for m in list(bpy.data.materials): add_albedo(m)
# ---- vật liệu phủ (override) cho lượt phụ: 'pos' = vị trí thế giới (m) · 'aux' = (mã toà pass_index, cờ ai, khoảng cách tới máy) · 'grp' = mã nhóm + 2 · 'gmask' = 1 nếu mặt thuộc nhóm VL['g']
def ovr(kind):
    m = bpy.data.materials.new('ovr_' + kind); m.use_nodes = True; N = m.node_tree.nodes; L = m.node_tree.links
    for n in list(N): N.remove(n)
    em = N.new('ShaderNodeEmission'); out = N.new('ShaderNodeOutputMaterial'); L.new(em.outputs[0], out.inputs[0]); em.inputs['Strength'].default_value = 1.0
    if kind == 'pos':
        g = N.new('ShaderNodeNewGeometry'); L.new(g.outputs['Position'], em.inputs['Color'])
    elif kind == 'aux':
        oi = N.new('ShaderNodeObjectInfo'); at = N.new('ShaderNodeAttribute'); at.attribute_name = 'ai'; cd = N.new('ShaderNodeCameraData')
        cm = N.new('ShaderNodeCombineXYZ'); L.new(oi.outputs['Object Index'], cm.inputs[0]); L.new(at.outputs['Fac'], cm.inputs[1]); L.new(cd.outputs['View Distance'], cm.inputs[2])
        L.new(cm.outputs[0], em.inputs['Color'])
    elif kind == 'grp':
        at = N.new('ShaderNodeAttribute'); at.attribute_name = 'grp'; ad = N.new('ShaderNodeMath'); ad.operation = 'ADD'; ad.inputs[1].default_value = 2.0
        L.new(at.outputs['Fac'], ad.inputs[0]); L.new(ad.outputs[0], em.inputs['Strength']); em.inputs['Color'].default_value = (1, 1, 1, 1)
    elif kind == 'gmask':
        at = N.new('ShaderNodeAttribute'); at.attribute_name = 'grp'; vg = N.new('ShaderNodeAttribute'); vg.attribute_type = 'VIEW_LAYER'; vg.attribute_name = 'g'
        sb = N.new('ShaderNodeMath'); sb.operation = 'SUBTRACT'; L.new(at.outputs['Fac'], sb.inputs[0]); L.new(vg.outputs['Fac'], sb.inputs[1])
        ab = N.new('ShaderNodeMath'); ab.operation = 'ABSOLUTE'; L.new(sb.outputs[0], ab.inputs[0])
        lt = N.new('ShaderNodeMath'); lt.operation = 'LESS_THAN'; lt.inputs[1].default_value = 0.5; L.new(ab.outputs[0], lt.inputs[0])
        fa = N.new('ShaderNodeAttribute'); fa.attribute_name = 'flat'; mu = N.new('ShaderNodeMath'); mu.operation = 'MULTIPLY'
        L.new(lt.outputs[0], mu.inputs[0]); L.new(fa.outputs['Fac'], mu.inputs[1]); L.new(mu.outputs[0], em.inputs['Strength']); em.inputs['Color'].default_value = (1, 1, 1, 1)
    return m
OVR = {k: ovr(k) for k in ('pos', 'aux', 'grp', 'gmask')}
def setup(kind):
    """beauty: Cycles A.spp, AgX · alb: albedo phát sáng · pos/aux/grp/gmask: 1 mẫu, không lọc, Standard."""
    VL.material_override = OVR.get(kind); VL['alb'] = 1.0 if kind == 'alb' else 0.0
    data = kind != 'beauty'
    sun.hide_render = data
    if data:
        if bg.inputs[0].links: wl.remove(bg.inputs[0].links[0])
        bg.inputs[0].default_value = (0, 0, 0, 1); bg.inputs[1].default_value = 0.0
        sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'; sc.view_settings.exposure = 0.0
        sc.cycles.samples = 6 if kind == 'alb' else 1; sc.cycles.use_denoising = False; sc.cycles.use_adaptive_sampling = False; sc.cycles.max_bounces = 0
        sc.cycles.filter_width = 1.0 if kind == 'alb' else 0.01
    else:
        if not bg.inputs[0].links: wl.new(sky.outputs[0], bg.inputs[0])
        bg.inputs[1].default_value = 0.22 if alt > 12 else 0.3
        sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = LOG['look']; sc.view_settings.exposure = 0.35
        sc.cycles.samples = A.spp; sc.cycles.use_denoising = True; sc.cycles.use_adaptive_sampling = True; sc.cycles.max_bounces = 4; sc.cycles.filter_width = 1.5
def render_exr(path):   # EXR một lớp RGBA float32
    s_ = sc.render.image_settings; s_.media_type = 'IMAGE'; s_.file_format = 'OPEN_EXR'; s_.color_depth = '32'; s_.exr_codec = 'ZIP'; s_.color_mode = 'RGBA'
    sc.render.filepath = path; bpy.ops.render.render(write_still=True)
def render_png(path):
    s_ = sc.render.image_settings; s_.media_type = 'IMAGE'; s_.file_format = 'PNG'; s_.color_depth = '8'; s_.color_mode = 'RGB'
    sc.render.filepath = path; bpy.ops.render.render(write_still=True)

if A.mode in ('anim', 'proj'):
    if A.blend: bpy.ops.wm.save_as_mainfile(filepath=A.blend)
    jobs = [(f'{f:04d}', *CM.cam_at(A.site, f)) for f in frames()] if A.mode == 'anim' else [(f'proj{int(az):03d}', *CM.orbit_cam(CM.SITE['kb'], az), CM.SITE['kb']['mm']) for az in CM.SITE['kb']['proj_az']]
    kinds = [k for k in os.environ.get('PT3_KINDS', 'beauty,pos,aux,alb').split(',') if k]
    for kind in kinds:
        setup(kind); tk = time.time()
        for (tag, pos, look, mm) in jobs:
            set_cam(pos, look, mm); t = time.time()
            if kind == 'beauty': render_png(os.path.join(A.out, tag + '.png'))
            else: render_exr(os.path.join(A.out, f'{tag}_{kind}.exr'))
            info = {'tag': tag, 'kind': kind, 'pos': [round(x, 3) for x in pos], 'look': [round(x, 3) for x in look], 'mm': mm, 's': round(time.time() - t, 2)}
            LOG['renders'].append(info); print('KHUNG', json.dumps(info), flush=True)
        LOG.setdefault('kind_s', {})[kind] = round(time.time() - tk, 1)
        json.dump(LOG, open(os.path.join(A.out, 'meta.json'), 'w'), ensure_ascii=False)

elif A.mode == 'probe':   # khung mẫu: mã nhóm (grp + 2: ≥ 3 elev · 1 top · 2 khác · 0 nền trời) + vị trí
    jobs = [(f, *CM.cam_at(A.site, f)) for f in frames()]
    if A.site == 'kb': jobs += [(1000 + int(az), *CM.orbit_cam(CM.SITE['kb'], az), CM.SITE['kb']['mm']) for az in CM.SITE['kb']['proj_az']]
    for kind in ('grp', 'pos'):
        setup(kind)
        for (f, pos, look, mm) in jobs: set_cam(pos, look, mm); render_exr(os.path.join(A.out, f'probe{f:04d}_{kind}.exr'))
    print('PROBE', len(jobs))

elif A.mode in ('elev', 'top'):   # trực giao: albedo (RGBA, alpha = phủ) + mặt nạ nhóm (1 = mặt thuộc nhóm này)
    sc.render.film_transparent = True; cam.type = 'ORTHO'
    req = json.load(open(A.groups))
    def shoot(tag):
        setup('alb'); t = time.time(); render_exr(os.path.join(A.out, tag + '_alb.exr')); setup('gmask'); render_exr(os.path.join(A.out, tag + '_mask.exr')); return round(time.time() - t, 2)
    if A.mode == 'elev':
        ppm = req['ppm']
        for bid, gl in req['elev'].items():
            show_only(lambda o: o['k'] in ELIG and o['bid'] == int(bid))
            for g in gl:
                G = GRP[g]; L_ = G['L']; Hh = G['z1'] - G['z0']; Wpx = max(16, int(round(L_ * ppm))); Hpx = max(16, int(round(Hh * ppm)))
                sc.render.resolution_x, sc.render.resolution_y = Wpx, Hpx; cam.ortho_scale = max(L_, Hh); cam.sensor_fit = 'AUTO'
                D = 60.0; mx = G['p0'][0] + G['u'][0] * L_ / 2; my = G['p0'][1] + G['u'][1] * L_ / 2
                pos = (mx + G['w'][0] * D, my + G['w'][1] * D, (G['z0'] + G['z1']) / 2)
                co.location = pos; co.rotation_euler = CM.blender_rot(pos, (mx, my, pos[2])); cam.clip_start = D - 3.2; cam.clip_end = D + 0.6
                VL['g'] = float(g); s_ = shoot(f'elev_b{bid}_g{g}')
                LOG['renders'].append({'bid': int(bid), 'g': g, 'W': Wpx, 'H': Hpx, 's': s_})
    else:
        T = req['top']; x0, y0, x1, y1 = T['rect']; ppm = T['ppm']
        show_only(lambda o: o['k'] in ELIG and (TOP_BIDS is None and 0 <= o['bid'] < 9000 or o['bid'] == 9800 or (TOP_BIDS and o['bid'] in TOP_BIDS)))
        Wpx, Hpx = int(round((x1 - x0) * ppm)), int(round((y1 - y0) * ppm)); sc.render.resolution_x, sc.render.resolution_y = Wpx, Hpx
        cam.ortho_scale = max(x1 - x0, y1 - y0); cam.sensor_fit = 'AUTO'; cam.clip_start = 1.0; cam.clip_end = 400.0
        co.location = ((x0 + x1) / 2, (y0 + y1) / 2, 200.0); co.rotation_euler = (0.0, 0.0, 0.0)
        VL['g'] = -1.0; s_ = shoot('top'); LOG['renders'].append({'top': T, 'W': Wpx, 'H': Hpx, 's': s_})

LOG['total_s'] = round(time.time() - T0, 1)
json.dump(LOG, open(os.path.join(A.out, 'meta.json'), 'w'), ensure_ascii=False)
print('DONE', LOG['total_s'], 's')
