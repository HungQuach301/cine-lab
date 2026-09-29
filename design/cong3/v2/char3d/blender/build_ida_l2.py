# Cine Lab · Cửa mặt Ida — LƯỢT 2 (W4, quyết định chủ dự án "d — lưới người MPFB2 (CC0)").
# Chạy:  /opt/bpy/bin/python design/cong3/v2/char3d/blender/build_ida_l2.py -- <repo mpfb2> <thư mục ra> [--blend f.blend]
# Ra:    <ra>/ida_bl.glb + <ra>/ida_bl.json
# Cách dựng:
#   1. MPFB 2.0.17 (tài sản lõi CC0 — RIGHTS.md W4-MPFB-A) chạy như extension không giao diện: HumanService.create_human
#      (nữ, tuổi 74 → age 0,877, cơ 0,35, cân 0,5) + các target chi tiết (mũi dài hơi khoằm, mắt to, dái tai dài, gò má cao,
#      môi mỏng tuổi già, cằm nhỏ…) → nướng thành một hình.
#   2. Chỉ lấy ĐẦU + CỔ (+ răng helper). Đưa về hệ đầu cast3d (đơn vị H; y = 0 cằm, 1 đỉnh sọ; +z mặt) rồi CÁCH ĐIỆU:
#      sọ rộng/tròn theo sheet (0,78 × 0,92 H), cổ 0,40 H. Tai là tai của lưới MPFB (liền da, có vành, gờ, dái).
#   3. Shape key 16 kênh CÙNG TÊN facerig.js + vis_* (6 khẩu hình), dựng từ các "expression unit" CC0 của MPFB (bảng CH_UNITS) cộng
#      một phần thủ tục (browKnit). Modifier Subdivision Surface cấp 1, lấy mẫu từng shape key qua lưới đã chia.
#   4. Mắt, mày, tóc (vỏ + dải thon + sợi tơ), búi: như lượt 1 (build_ida_head.py) nhưng bám lưới mới (tia BVH), búi liền đầu.
import sys, os, json, time, math, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import bpy, addon_utils, mathutils
from mathutils.bvhtree import BVHTree
from sdfnp import sstep, gauss, fbm

argv = sys.argv[sys.argv.index('--') + 1:]
MP, OUT = argv[0], os.path.abspath(argv[1])
BLEND = argv[argv.index('--blend') + 1] if '--blend' in argv else None
os.makedirs(OUT, exist_ok=True)
T0 = time.time()
log = lambda *a: print(f'[l2 {time.time() - T0:6.1f}s]', *a, flush=True)
rng = np.random.default_rng(20260928)

bpy.ops.wm.read_factory_settings(use_empty=True)
ext = bpy.utils.user_resource('EXTENSIONS', path='user_default', create=True)
if not os.path.exists(os.path.join(ext, 'mpfb')): os.symlink(os.path.join(MP, 'src', 'mpfb'), os.path.join(ext, 'mpfb'))
addon_utils.enable('bl_ext.user_default.mpfb', default_set=True, handle_error=None)
HumanService = importlib.import_module('bl_ext.user_default.mpfb.services.humanservice').HumanService
TargetService = importlib.import_module('bl_ext.user_default.mpfb.services.targetservice').TargetService
TG = os.path.join(MP, 'src', 'mpfb', 'data', 'targets')
SC = bpy.context.scene

# ======================= 1. NGƯỜI MPFB =======================
AGE = 0.5 + (74 - 25) / (90 - 25) * 0.5          # thang tuổi MakeHuman: 0,5 = 25 tuổi, 1,0 = 90 tuổi
macro = TargetService.get_default_macro_info_dict()
macro.update({'gender': 0.0, 'age': AGE, 'muscle': 0.35, 'weight': 0.52, 'proportions': 0.5})
macro['race'] = {'asian': 0.15, 'caucasian': 0.7, 'african': 0.15}
hum = HumanService.create_human(macro_detail_dict=macro, scale=0.1, mask_helpers=False, feet_on_ground=False)
DETAIL = {   # target chi tiết (trọng số) — cách điệu tuổi 74 + nhận diện của sheet
    'nose/nose-scale-vert-incr': 0.55, 'nose/nose-hump-incr': 0.55, 'nose/nose-point-down': 0.35, 'nose/nose-volume-incr': 0.35,
    'nose/nose-point-width-incr': 0.35, 'nose/nose-scale-depth-incr': 0.25, 'nose/nose-flaring-incr': 0.2,
    'eyes/l-eye-scale-incr': 0.7, 'eyes/r-eye-scale-incr': 0.7, 'eyes/l-eye-bag-incr': 0.3, 'eyes/r-eye-bag-incr': 0.3,
    'eyes/l-eye-eyefold-down': 0.05, 'eyes/r-eye-eyefold-down': 0.05, 'eyes/l-eye-height2-incr': 0.85, 'eyes/r-eye-height2-incr': 0.85, 'eyes/l-eye-height1-incr': 0.5, 'eyes/r-eye-height1-incr': 0.5, 'eyes/l-eye-height3-incr': 0.5, 'eyes/r-eye-height3-incr': 0.5,   # L3: mí mở hơn (mắt thấy được ở góc nghiêng PA1) 'eyes/l-eye-corner2-down': 0.25, 'eyes/r-eye-corner2-down': 0.25,
    'ears/l-ear-lobe-incr': 0.7, 'ears/r-ear-lobe-incr': 0.7, 'ears/l-ear-scale-incr': 0.25, 'ears/r-ear-scale-incr': 0.25,
    'cheek/l-cheek-bones-incr': 0.35, 'cheek/r-cheek-bones-incr': 0.35, 'cheek/l-cheek-volume-incr': 0.2, 'cheek/r-cheek-volume-incr': 0.2,
    'mouth/mouth-upperlip-volume-decr': 0.25, 'mouth/mouth-angles-down': 0.12, 'mouth/mouth-scale-horiz-decr': 0.15,
    'chin/chin-width-decr': 0.3, 'chin/chin-height-decr': 0.2, 'chin/chin-prominent-incr': 0.15,
    'head/head-round': 0.45, 'head/head-age-incr': 0.75,   # L3: da/khối già hơn (lời chê 'da em bé') 'neck/neck-double-decr': 0.4,
}
for k, w in DETAIL.items():
    TargetService.load_target(hum, os.path.join(TG, k + '.target.gz'), weight=w, name='d_' + k.split('/')[-1])
dg = bpy.context.evaluated_depsgraph_get()
def co_of(ob):
    a = np.zeros(len(ob.data.vertices) * 3); ob.data.vertices.foreach_get('co', a); return a.reshape(-1, 3)
def mix_co(ob):
    kb = ob.data.shape_keys.key_blocks; base = np.zeros(len(ob.data.vertices) * 3); kb[0].data.foreach_get('co', base); base = base.reshape(-1, 3)
    out = base.copy()
    for k in kb[1:]:
        if k.value:
            a = np.zeros_like(base.ravel()); k.data.foreach_get('co', a); out += k.value * (a.reshape(-1, 3) - base)
    return out
BASE = mix_co(hum)
log(f'người MPFB: {len(BASE)} đỉnh, tuổi {AGE:.3f}')

UNITS = ['eye-left-closure', 'eye-right-closure', 'eye-left-slit', 'eye-right-slit', 'eyebrows-left-down', 'eyebrows-right-down',
         'eyebrows-left-inner-up', 'eyebrows-right-inner-up', 'eyebrows-left-up', 'eyebrows-right-up', 'mouth-compression', 'mouth-corner-puller',
         'mouth-depression', 'mouth-elevation', 'mouth-open', 'mouth-pursing', 'mouth-protusion', 'mouth-retraction', 'mouth-upward-retraction',
         'nose-compression', 'mouth-depression-retraction']
UD = {}
for u in UNITS:
    kb = TargetService.load_target(hum, os.path.join(TG, 'expression', 'units', 'caucasian', u + '.target.gz'), weight=0.0, name='u_' + u)
    a = np.zeros(len(BASE) * 3); kb.data.foreach_get('co', a)
    b = np.zeros(len(BASE) * 3); hum.data.shape_keys.key_blocks[0].data.foreach_get('co', b)
    UD[u] = (a - b).reshape(-1, 3)
FACES = [list(p.vertices) for p in hum.data.polygons]
log('đơn vị biểu cảm: ' + ', '.join(f'{u} {np.abs(d).max():.4f}' for u, d in UD.items()))

# ======================= 2. ĐẦU + CỔ, hệ đầu, cách điệu =======================
to_b = lambda P: np.stack([P[:, 0], -P[:, 2], P[:, 1]], 1)
from_b = lambda B: np.stack([B[:, 0], B[:, 2], -B[:, 1]], 1)
Pw = from_b(BASE)                                            # hệ three: y lên, +z trước (MPFB nhìn về −y Blender)
body_n = 13380
rng_ = lambda a, b: np.arange(a, b + 1)
EYE_L, EYE_R = rng_(14598, 14669), None
grp = json.load(open(os.path.join(MP, 'src/mpfb/data/mesh_metadata/basemesh_vertex_groups.json')))
gidx = lambda g: np.concatenate([rng_(a, b) for a, b in grp[g]])
eyeL, eyeR = gidx('helper-l-eye'), gidx('helper-r-eye')
teeth = np.concatenate([gidx('helper-upper-teeth'), gidx('helper-lower-teeth')])
cL, cR = Pw[eyeL].mean(0), Pw[eyeR].mean(0)
eye_y = 0.5 * (cL[1] + cR[1])
headv = np.arange(body_n)
ytop = Pw[headv, 1].max()
face_front = (np.abs(Pw[:, 0]) < 0.012) & (Pw[:, 2] > cL[2] - 0.02) & (np.arange(len(Pw)) < body_n) & (Pw[:, 1] < eye_y) & (Pw[:, 1] > eye_y - 0.2)
ychin = Pw[face_front, 1].min()
HL = ytop - ychin
log(f'đầu MPFB: dài {HL:.4f} m (cằm {ychin:.3f} → đỉnh {ytop:.3f})')
Q = (Pw - np.array([0, ychin, 0])) / HL                    # đơn vị H, y = 0 cằm
_nk = (np.abs(Q[:body_n, 1] + 0.2) < 0.03) & (np.abs(Q[:body_n, 0]) < 0.1); _zn = 0.5 * (Q[:body_n][_nk, 2].max() + Q[:body_n][_nk, 2].min())
# cổ: cắt theo TRỤ quanh trục cổ (r < 0,25 H), sâu tới y −0,46 → mép cắt là vòng tròn nằm trong cổ áo/khăn (khung EEVEE lượt 2 lộ mép răng cưa ở gáy)
keep = np.zeros(len(Q), bool); keep[:body_n] = (Q[:body_n, 1] > 0.05) | ((Q[:body_n, 1] > -0.14) & (Q[:body_n, 2] > _zn - 0.02) & (np.abs(Q[:body_n, 0]) < 0.22)) | ((Q[:body_n, 1] > -0.62) & (np.hypot(Q[:body_n, 0] / 0.24, (Q[:body_n, 2] - _zn) / 0.30) < 1.0))
keep[teeth] = True
# tâm sọ (dùng cho mũ/tóc): giữa trước–sau ở y 0,75
band = keep & (np.abs(Q[:, 1] - 0.75) < 0.02) & (np.abs(Q[:, 0]) < 0.03)
zc = 0.5 * (Q[band, 2].max() + Q[band, 2].min())
Q[:, 2] -= zc + 0.045                                        # tâm sọ ở z ≈ −0,045 (như lượt 1 / mũ cast3d)
# cách điệu theo sheet: bề ngang đầu 0,78 (gồm tóc), sâu 0,92; cổ 0,40
isb = np.arange(len(Q)) < body_n
m_w = keep & isb & (Q[:, 1] > 0.68) & (Q[:, 1] < 0.80); w_cr = 2 * np.abs(Q[m_w, 0]).max()
m_d = keep & isb & (Q[:, 1] > 0.55) & (Q[:, 1] < 0.72) & (np.abs(Q[:, 0]) < 0.08); d_cr = Q[m_d, 2].max() - Q[m_d, 2].min()
SX = np.clip(0.735 / w_cr, 1.0, 1.2); SZ = np.clip(0.88 / d_cr, 1.0, 1.15)
wy = sstep(0.05, 0.45, Q[:, 1])                              # cổ không phình theo sọ
S3 = np.stack([1 + (SX - 1) * wy, np.ones(len(Q)), 1 + (SZ - 1) * wy], 1)
m_n = keep & (np.abs(Q[:, 1] + 0.12) < 0.03) & isb
w_neck = 2 * np.percentile(np.abs(Q[m_n, 0]), 99)
SN = np.clip(0.40 / w_neck, 0.8, 1.3)
S3[:, 0] *= 1 + (SN - 1) * (1 - sstep(-0.02, 0.18, Q[:, 1]))
S3[:, 2] *= 1 + (SN - 1) * 0.6 * (1 - sstep(-0.02, 0.18, Q[:, 1]))
Qs = Q * S3
# cổ đưa ra trước (sheet: "cổ hơi đưa ra trước") cho tâm cổ trùng tâm khăn 4 vòng của cast3d (z ≈ 0) — gáy MPFB từng lòi ra sau khăn thành "vây"
_zc = Qs[:body_n][(np.abs(Qs[:body_n, 1] + 0.2) < 0.03) & (np.abs(Qs[:body_n, 0]) < 0.1) & keep[:body_n]]
ZN0 = 0.5 * (_zc[:, 2].max() + _zc[:, 2].min()); Qs[:, 2] += (0.0 - ZN0) * (1 - sstep(-0.30, -0.02, Qs[:, 1]))   # chỉ dưới đường cằm (cằm không bị kéo)
# L3: da cổ LIỀN trong khăn — dưới cằm, bán kính quanh trục cổ bị kẹp ≤ 0,205 H (mép trong khăn 4 vòng ≈ 0,21–0,25 H) → không vây/khuyết lòi qua khăn
_r = np.hypot(Qs[:, 0], Qs[:, 2]); _rc = 0.205
_w = np.maximum(1 - sstep(-0.10, 0.02, Qs[:, 1]), (1 - sstep(0.04, 0.16, Qs[:, 1])) * sstep(0.06, -0.04, Qs[:, 2]))   # gáy + hai bên cổ tới y 0,16 (vây gáy lượt 2–3)
_rn = np.where(_r > _rc, _rc + (_r - _rc) * 0.25, _r); _k = np.where(_r > 1e-6, 1 + (_rn / np.maximum(_r, 1e-6) - 1) * _w, 1.0)
Qs[:, 0] *= _k; Qs[:, 2] *= _k
log(f'tâm cổ z {ZN0:.3f} → 0'); log(f'cách điệu: sọ rộng {w_cr:.3f}→×{SX:.3f}, sâu {d_cr:.3f}→×{SZ:.3f}, cổ {w_neck:.3f}→×{SN:.3f}')
U = {u: np.stack([d[:, 0], d[:, 2], -d[:, 1]], 1) / HL * S3 for u, d in UD.items()}   # đơn vị biểu cảm → hệ H (bỏ qua đạo hàm của S3: sai < 1 %)

Qs[teeth, 2] -= 0.018   # L3: răng lùi vào trong (môi mím/cười nén từng để răng xuyên qua môi)
# ---- mốc ----
EL = Qs[eyeL]; ER_c = EL.mean(0); ER_r = float(np.linalg.norm(EL - ER_c, axis=1).mean())
EC = Qs[eyeR].mean(0)
mo = UD['mouth-open'][:body_n]; mid = keep[:body_n] & (np.abs(Qs[:body_n, 0]) < 0.015) & (Qs[:body_n, 1] > 0.15) & (Qs[:body_n, 1] < EL.mean(0)[1] - 0.12) & (Qs[:body_n, 2] > EL.mean(0)[2])
mag = np.linalg.norm(mo, axis=1)[mid]; yy_ = Qs[:body_n][mid]
lo_lip = yy_[mag > 0.5 * mag.max()]; up_lip = yy_[(mag < 0.1 * mag.max()) & (yy_[:, 1] > lo_lip[:, 1].max())]
MY_ = 0.5 * (lo_lip[:, 1].max() + up_lip[:, 1].min()); MZ_ = yy_[np.abs(yy_[:, 1] - MY_) < 0.03][:, 2].max()
MOUTH = np.array([0.0, MY_, MZ_])
jj = gidx('joint-jaw'); JAW = Qs[jj].mean(0)
log(f'mắt L {ER_c.round(3)} R {EC.round(3)} bk {ER_r:.3f}; miệng {MOUTH.round(3)}; hàm {JAW.round(3)}')

# ---- tập con + mặt ----
idx = np.nonzero(keep)[0]; remap = -np.ones(len(Q), np.int64); remap[idx] = np.arange(len(idx))
Fk = [[remap[v] for v in f] for f in FACES if all(keep[v] for v in f)]
P0 = Qs[idx]

# ======================= 3. KÊNH RIG ← đơn vị biểu cảm MPFB =======================
CH_UNITS = {
    'browUp': {'eyebrows-left-up': 1, 'eyebrows-right-up': 1},
    'browDown': {'eyebrows-left-down': 1, 'eyebrows-right-down': 1},
    'browInnerUp': {'eyebrows-left-inner-up': 2.2, 'eyebrows-right-inner-up': 2.2},   # L3: đầu mày trong nhướng rõ (buồn)
    'browKnit': {'nose-compression': 0.6, 'eyebrows-left-down': 0.25, 'eyebrows-right-down': 0.25},
    'blink': {'eye-left-closure': 1, 'eye-right-closure': 1},
    'lidDrop': {'eye-left-closure': 0.35, 'eye-right-closure': 0.35},
    'squint': {'eye-left-slit': 0.35, 'eye-right-slit': 0.35},   # Cổng 6: mí trên đã hạ sẵn (nướng eye-closure) → nheo nhẹ hơn để PA1 nghiêng không thành khe (0,6 → 0,35)   # L3: mắt không thành khe ở PA1
    'cheekRaise': {'eye-left-slit': 0.12, 'eye-right-slit': 0.12},   # Cổng 6: 0,25 → 0,12 (như squint)   # L3: + khối má nâng THỦ TỤC (ch_delta); bỏ mouth-upward-retraction (nhấc môi trên → lộ răng, cười tươi)
    'smile': {'mouth-corner-puller': 0.55, 'mouth-compression': 1.0, 'mouth-elevation': 0.35},   # L3: cười NÉN (môi khép, không lộ răng), không cười tươi
    'frown': {'mouth-depression': 1},   # L3: về 1,0; miệng gãy khi cộng press + chinRaise sửa bằng shape key sửa lỗi corr_mouth
    'jawOpen': {'mouth-open': 1},
    'press': {'mouth-compression': 1},
    'pucker': {'mouth-pursing': 1, 'mouth-protusion': 0.4},
    'wide': {'mouth-retraction': 1},
    'lowerLipIn': {'mouth-depression-retraction': 0.4, 'mouth-elevation': 0.5},
    'chinRaise': {'mouth-elevation': 1},
}
CHANNELS = list(CH_UNITS)
VISEMES = {'A': {'jawOpen': 0.75, 'wide': 0.1}, 'E': {'jawOpen': 0.3, 'wide': 0.7}, 'O': {'jawOpen': 0.5, 'pucker': 0.9},
           'MBP': {'press': 1.0}, 'FV': {'lowerLipIn': 1.0, 'jawOpen': 0.1}, 'L': {'jawOpen': 0.4, 'wide': 0.25}}
PRESETS = {'neutral': {}, 'sad_smile': {'smile': 1.0, 'cheekRaise': 0.9, 'browInnerUp': 0.45, 'browKnit': 0.1, 'squint': 0.55, 'jawOpen': 0.1},
           'strained': {'press': 0.8, 'browKnit': 0.8, 'browDown': 0.3, 'chinRaise': 0.4},
           'choked': {'frown': 1.0, 'browInnerUp': 1.0, 'browKnit': 0.65, 'chinRaise': 1.0, 'press': 0.6, 'lidDrop': 0.25, 'squint': 0.2}}
def ch_delta(ch):
    D = np.zeros_like(P0)
    if ch == 'cheekRaise':   # má "táo" nâng lên–ra trước dưới mắt, không động tới môi
        ax_ = np.abs(P0[:, 0]); k = np.exp(-((ax_ - abs(ER_c[0]) - 0.01) ** 2 + (P0[:, 1] - (ER_c[1] - 0.13)) ** 2) / 0.065 ** 2) * sstep(ER_c[2] - 0.15, ER_c[2] - 0.05, P0[:, 2])
        D[:, 1] += 0.016 * k; D[:, 2] += 0.012 * k
    for u, w in CH_UNITS[ch].items(): D += w * U[u][idx]
    return D
CHD = {c: ch_delta(c) for c in CHANNELS}
KEYD = dict(CHD)
for v, w in VISEMES.items(): KEYD['vis_' + v] = sum(wt * CHD[c] for c, wt in w.items())

# ======================= đối tượng Blender + subdivision =======================
def mk_mat(name, rgb_lin=None, rough=0.6, spec=0.3, sss=0.0, img=None, use_attr=True):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; bs = nt.nodes.get('Principled BSDF')
    bs.inputs['Roughness'].default_value = rough
    if 'Specular IOR Level' in bs.inputs: bs.inputs['Specular IOR Level'].default_value = spec
    if sss and 'Subsurface Weight' in bs.inputs:
        bs.inputs['Subsurface Weight'].default_value = sss; bs.inputs['Subsurface Radius'].default_value = (1.0, 0.35, 0.2); bs.inputs['Subsurface Scale'].default_value = 0.004
    if img is not None:
        t = nt.nodes.new('ShaderNodeTexImage'); t.image = img; nt.links.new(t.outputs['Color'], bs.inputs['Base Color'])
    elif use_attr:
        ca = nt.nodes.new('ShaderNodeVertexColor'); ca.layer_name = 'Col'
        if rgb_lin is None: nt.links.new(ca.outputs['Color'], bs.inputs['Base Color'])
        else:
            mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs['Factor'].default_value = 1.0
            mx.inputs[6].default_value = (*rgb_lin, 1); nt.links.new(ca.outputs['Color'], mx.inputs[7]); nt.links.new(mx.outputs[2], bs.inputs['Base Color'])
    else:
        bs.inputs['Base Color'].default_value = (*rgb_lin, 1)
    return m

def mk_obj(name, P, faces, cols=None, uv=None, mat=None, loc=None):
    me = bpy.data.meshes.new(name); me.from_pydata(to_b(np.asarray(P)).tolist(), [], [list(map(int, f)) for f in faces]); me.update()
    me.polygons.foreach_set('use_smooth', np.ones(len(me.polygons), bool))
    if cols is not None:
        c4 = cols if cols.shape[1] == 4 else np.concatenate([cols, np.ones((len(P), 1))], 1)
        a = me.color_attributes.new('Col', 'FLOAT_COLOR', 'POINT'); a.data.foreach_set('color', c4.astype(np.float32).ravel()); me.color_attributes.active_color = a
    if uv is not None:
        uvl = me.uv_layers.new(name='UVMap'); li = np.zeros(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', li); uvl.data.foreach_set('uv', np.asarray(uv, np.float32)[li].ravel())
    if mat is not None: me.materials.append(mat)
    ob = bpy.data.objects.new(name, me); SC.collection.objects.link(ob)
    if loc is not None: ob.location = tuple(to_b(np.array([loc]))[0])
    return ob

def verts_of(ob): a = np.zeros(len(ob.data.vertices) * 3); ob.data.vertices.foreach_get('co', a); return from_b(a.reshape(-1, 3))

head = mk_obj('ida_head', P0, Fk, cols=np.repeat(np.isin(idx, teeth)[:, None].astype(float), 3, 1))   # màu tạm = cờ răng (lan qua subdivision)
head.shape_key_add(name='Basis', from_mix=False)
for k, D in KEYD.items():
    sk = head.shape_key_add(name=k, from_mix=False); sk.data.foreach_set('co', to_b(P0 + D).astype(np.float32).ravel())
mod = head.modifiers.new('subd', 'SUBSURF'); mod.levels = 2; mod.render_levels = 2
def eval_co(ob):
    dg = bpy.context.evaluated_depsgraph_get(); ev = ob.evaluated_get(dg); me = ev.to_mesh(); a = np.zeros(len(me.vertices) * 3); me.vertices.foreach_get('co', a); ev.to_mesh_clear(); return from_b(a.reshape(-1, 3))
kbs = head.data.shape_keys.key_blocks
for k in kbs: k.value = 0.0
PS = eval_co(head)
SKD = {}
for k in list(KEYD):
    kbs[k].value = 1.0; SKD[k] = eval_co(head) - PS; kbs[k].value = 0.0
me_sub = bpy.data.meshes.new_from_object(head.evaluated_get(bpy.context.evaluated_depsgraph_get()))
_tc = np.zeros(len(me_sub.vertices) * 4, np.float32); me_sub.color_attributes['Col'].data.foreach_get('color', _tc); TFLAG = _tc.reshape(-1, 4)[:, 0] > 0.5
bpy.data.objects.remove(head)
fl = np.zeros(sum(len(p.vertices) for p in me_sub.polygons), np.int64); me_sub.polygons.foreach_get('vertices', fl)
FS = fl.reshape(-1, 4) if len(fl) == 4 * len(me_sub.polygons) else None
log(f'đầu sau subdivision: {len(PS)} đỉnh, {len(me_sub.polygons)} mặt')
# Cổng 6 (W4 gói nhân vật): MÍ — nướng eye-slit (mí dưới chạm đáy tròng) + eye-closure (mí trên che 1/4 bán kính tròng) vào trung tính
from eyelid import fix_lids
LIDS = fix_lids(PS, [list(p.vertices) for p in me_sub.polygons], SKD, [ER_c, EC], ER_r, log, slit_k=0.35)

# ---- răng: tách khỏi da (khối riêng, vật liệu ngà) ----
tsub = None
# ======================= 4. Nếp tuổi bằng khối + albedo =======================
def normals(P, F):
    tri = np.concatenate([F[:, [0, 1, 2]], F[:, [0, 2, 3]]]); n = np.cross(P[tri[:, 1]] - P[tri[:, 0]], P[tri[:, 2]] - P[tri[:, 0]])
    N = np.zeros_like(P); [np.add.at(N, tri[:, k], n) for k in range(3)]; return N / np.maximum(np.linalg.norm(N, axis=1), 1e-12)[:, None]
N = normals(PS, FS)
x, y, z = PS.T; ax = np.abs(x); E = ER_c; EX, EY = abs(E[0]), E[1]
MY, MZ = MOUTH[1], MOUTH[2]
mw_ = keep[idx]  # placeholder
fzf = sstep(E[2] - 0.12, E[2] - 0.02, z)                    # mặt trước
def g2(ax, y, pts, w):
    d = np.full(np.shape(ax), 1e9)
    for (a0, a1), (b0, b1) in zip(pts[:-1], pts[1:]):
        bx, by = b0 - a0, b1 - a1; h = np.clip(((ax - a0) * bx + (y - a1) * by) / (bx * bx + by * by), 0, 1); d = np.minimum(d, np.hypot(ax - a0 - bx * h, y - a1 - by * h))
    return gauss(d, w)
dy_e = EY - 0.575
wr = (0.0030 * (gauss(y - (EY + 0.19) - 0.12 * ax * ax, 0.011) + gauss(y - (EY + 0.23) - 0.12 * ax * ax, 0.011)) * sstep(0.26, 0.06, ax)   # 2 nếp trán
      + 0.0026 * (g2(ax, y, [(EX + 0.08, EY + 0.015), (EX + 0.13, EY + 0.035)], 0.0075) + g2(ax, y, [(EX + 0.085, EY - 0.003), (EX + 0.135, EY - 0.005)], 0.0075)
                  + g2(ax, y, [(EX + 0.078, EY - 0.022), (EX + 0.12, EY - 0.048)], 0.0075)) * sstep(E[2] - 0.2, E[2] - 0.1, z)   # chân chim
      + 0.0020 * g2(ax, y, [(0.018, EY + 0.065), (0.024, EY + 0.115)], 0.008))                                                      # nếp giữa mày
nose_w = 0.055; MWc = 0.068
wr = wr * 1.5 + 0.0034 * gauss(y - (EY + 0.27) - 0.12 * ax * ax, 0.011) * sstep(0.24, 0.06, ax)                                   # nếp trán thứ 3
wr = wr + (0.0060 * g2(ax, y, [(nose_w, 0.5 * (EY + MY) - 0.01), (MWc + 0.01, MY + 0.02), (MWc + 0.015, MY - 0.01)], 0.012)          # rãnh mũi–má sâu
           + 0.0040 * g2(ax, y, [(MWc, MY - 0.01), (MWc + 0.012, MY - 0.07), (MWc + 0.02, MY - 0.12)], 0.011)                          # rãnh khoé miệng – cằm (marionette)
           + 0.0035 * g2(ax, y, [(EX - 0.06, EY - 0.06), (EX, EY - 0.075), (EX + 0.06, EY - 0.055)], 0.010)                          # rãnh dưới bọng mắt
           + 0.0014 * sum(gauss(x - xx, 0.004) for xx in np.linspace(-0.05, 0.05, 7)) * gauss(y - (MY + 0.03), 0.012)                  # nếp dọc môi trên
           ) * 1.0
DISP = -wr * fzf
DISP -= 0.0030 * (gauss(y + 0.05 - 0.2 * ax * ax, 0.012) + gauss(y + 0.12 - 0.2 * ax * ax, 0.012)) * sstep(-0.05, 0.08, z)          # nếp ngang cổ
PS = PS + N * DISP[:, None]
N = normals(PS, FS)

def srgb2lin(c): c = np.asarray(c, float); return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
hexlin = lambda h: srgb2lin([int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)])
SKIN, HAIR = '#d8b49a', '#e2dfda'
isteeth = np.isin(idx, teeth)
# đỉnh lưới chia thuộc răng: đỉnh gốc là răng → lan qua mặt
tvert = TFLAG
HC = np.array([0.0, 0.64, -0.045])

def skin_albedo(P, N):
    x, y, z = P.T; ax = np.abs(x); fz = sstep(E[2] - 0.15, E[2] - 0.02, z)
    gp = lambda cx, cy, r: gauss(np.hypot(ax - cx, y - cy), r)
    base = hexlin(SKIN); r = np.full_like(x, 0.97); g = np.full_like(x, 1.0); b = np.full_like(x, 1.03)
    nose_y = 0.5 * (EY + MY)
    warm = (0.22 * gp(EX + 0.02, nose_y - 0.02, 0.07) + 0.28 * gp(0, nose_y + 0.01, 0.045) + 0.10 * gp(0.05, EY + 0.06, 0.05) + 0.08 * gp(0, 0.10, 0.05)) * fz
    ear = sstep(0.30, 0.36, ax) * sstep(0.62, 0.55, y) * sstep(0.28, 0.33, y)
    warm = warm + 0.25 * ear
    r += warm * 0.30; g -= warm * 0.55; b -= warm * 0.50
    cool = (0.20 * gp(EX - 0.01, EY - 0.075, 0.03) + 0.12 * gp(0.30, EY + 0.03, 0.07) + 0.08 * gp(0.12, 0.16, 0.07)) * fz
    r -= cool * 0.55; g -= cool * 0.30; b += cool * 0.12
    er = np.sqrt((ax - EX) ** 2 + (y - EY) ** 2 + (z - E[2]) ** 2)
    rim = gauss(er - ER_r * 1.08, 0.008) * fz
    r += 0.02 * rim; g -= 0.05 * rim; b -= 0.04 * rim                                         # viền mí hồng
    lash = gauss(er - ER_r * 1.04, 0.006) * sstep(EY - 0.005, EY + 0.02, y) * fz            # chân mi trên (tối) — đi theo mí khi chớp
    r -= 0.45 * lash; g -= 0.48 * lash; b -= 0.45 * lash                                       # Cổng 6: chân mi trên tối thật sự (trước đây tính mà không dùng) — mép mí có nét
    wl = gauss(er - ER_r * 1.02, 0.007) * sstep(EY - 0.2 * ER_r, EY - 0.45 * ER_r, y) * fz      # Cổng 6: VIỀN NƯỚC mí dưới (hồng, ướt: nhám thấp)
    r += 0.06 * wl; g -= 0.16 * wl; b -= 0.10 * wl
    lip = sstep(0.022, 0.0, np.hypot(ax / 1.2, (y - MY) / 0.9) - 0.05) * sstep(MZ - 0.05, MZ - 0.02, z)
    r -= 0.02 * lip; g -= 0.24 * lip; b -= 0.18 * lip
    inner = sstep(MZ - 0.02, MZ - 0.06, z) * sstep(0.06, 0.03, ax) * sstep(0.05, 0.02, np.abs(y - MY))   # lòng miệng tối
    mot = fbm(x * 9, y * 9, z * 9, 41, 3); mot2 = fbm(x * 30, y * 30, z * 30, 47, 2)
    spot = np.maximum(0, fbm(x * 16, y * 16, z * 16, 53, 2) - 0.12) * (sstep(0.55, 0.75, y) + 0.6 * gp(EX + 0.05, EY - 0.1, 0.08)) * sstep(E[2] - 0.35, E[2] - 0.15, z)
    red = (0.35 * gp(EX + 0.03, EY - 0.12, 0.06) + 0.40 * gp(0, 0.5 * (EY + MY), 0.04)) * fz                                    # L3: má, mũi ửng
    r += 0.10 * mot + 0.04 * mot2 + 0.10 * red; g -= 0.03 * mot + 0.03 * mot2 + 0.22 * red; b -= 0.07 * mot + 0.02 * mot2 + 0.18 * red
    r -= 0.55 * spot; g -= 0.70 * spot; b -= 0.85 * spot                                                                             # L3: đốm tuổi rõ hơn
    ueye = gp(EX, EY - 0.065, 0.028) * fz; r -= 0.10 * ueye; g -= 0.14 * ueye; b -= 0.04 * ueye                                     # quầng dưới mắt nâu tím
    occ = np.maximum(0.3 * sstep(-0.25, -0.8, N[:, 1]) * sstep(0.28, 0.08, y), 0.15 * sstep(0.10, -0.25, y))
    k = (1 - occ) * (1 - 0.85 * inner)
    col = np.stack([base[0] * r * k, base[1] * g * k, base[2] * b * k], 1)
    dx, dy, dz = x - HC[0], y - HC[1], z - HC[2]
    th = np.arccos(np.clip(dy / np.maximum(np.sqrt(dx * dx + dy * dy + dz * dz), 1e-9), -1, 1)); ph = np.arctan2(dx, dz)
    s = sstep(0.06, -0.06, th - theta_max(ph))
    hair = hexlin(HAIR) * 0.80
    out = np.clip(col * (1 - s[:, None]) + hair[None] * s[:, None], 0, 1)
    # nhám theo vùng → kênh alpha (three.js: roughness = mix(0.45, 0.85, a)): chữ T (trán, sống mũi) bóng nhẹ; má, cằm, cổ, tai mờ
    tz = np.maximum(gp(0, EY + 0.15, 0.08), gauss(ax, 0.03) * sstep(MY, EY, y)) * fz
    rough = np.clip(0.62 - 0.35 * tz + 0.15 * sstep(0.1, -0.1, y) + 0.15 * ear + 0.08 * mot2, 0.05, 1)
    rough = rough * (1 - 0.95 * np.clip(wl, 0, 1))                                             # viền nước: bóng ướt
    return np.concatenate([out, rough[:, None]], 1)

_TH_PH = np.array([0.00, 0.45, 0.80, 1.05, 1.22, 1.38, 1.52, 1.68, 1.90, 2.30, 2.70, np.pi])
_TH_TH = np.array([1.30, 1.50, 1.68, 1.76, 1.78, 1.72, 1.66, 1.72, 1.94, 2.30, 2.55, 2.60])   # L3: tóc phủ thái dương (nhìn chính diện dưới vành mũ thấy tóc bạc)   # chân tóc: trán dưới vành mũ; thái dương, trên tai, gáy lộ
def theta_max(ph):
    a = np.abs(ph); return np.interp(a, _TH_PH, _TH_TH) + 0.012 * np.sin(ph * 9.0) + 0.008 * np.sin(ph * 17.0 + 1.3)

# L3: SHAPE KEY SỬA LỖI 'corr_mouth' — frown + press + chinRaise đủ 1,0 cho miệng gãy như vết rách → làm trơn vùng miệng của tổ hợp đó
_Dc = SKD['frown'] + SKD['press'] + SKD['chinRaise']; _Pc = PS + _Dc
_E = np.concatenate([FS[:, [0, 1]], FS[:, [1, 2]], FS[:, [2, 3]], FS[:, [3, 0]]]); _deg = np.bincount(_E.ravel(), minlength=len(PS)).astype(float)
_mask = gauss(np.hypot(PS[:, 0] / 1.3, PS[:, 1] - MY), 0.07) * sstep(MZ - 0.10, MZ - 0.04, PS[:, 2]) * (~tvert)
_S = _Pc.copy()
for _ in range(14):
    _acc = np.zeros_like(_S); np.add.at(_acc, _E[:, 0], _S[_E[:, 1]]); np.add.at(_acc, _E[:, 1], _S[_E[:, 0]])
    _S = _S + 0.5 * _mask[:, None] * (_acc / np.maximum(_deg, 1)[:, None] - _S)
SKD['corr_mouth'] = _S - _Pc
log(f"corr_mouth: dịch tối đa {np.abs(SKD['corr_mouth']).max():.4f} H")
# L3: 'corr_smile_lip' — khi CƯỜI với hàm hé ít (sad_smile: jawOpen 0,1), môi khép lại (cười nén, không lộ khe tối/răng): bù phần môi của jawOpen ≤ 0,12
_lipm = gauss(np.hypot(PS[:, 0] / 1.6, PS[:, 1] - MY), 0.09) * sstep(MZ - 0.10, MZ - 0.04, PS[:, 2])
SKD['corr_smile_lip'] = -0.12 * SKD['jawOpen'] * _lipm[:, None]
COL = skin_albedo(PS, N)
COL[tvert, :3] = hexlin('#cfc4b2') * 0.9
head = mk_obj('ida_head', PS, FS, cols=COL, uv=np.stack([np.arctan2(PS[:, 0], PS[:, 2]) / (2 * np.pi) + 0.5, PS[:, 1]], 1),
              mat=mk_mat('bl_skin', None, rough=0.62, spec=0.22, sss=0.2))
head.shape_key_add(name='Basis', from_mix=False)
for k, D in SKD.items():
    sk = head.shape_key_add(name=k, from_mix=False); sk.data.foreach_set('co', to_b(PS + D).astype(np.float32).ravel())
log('đầu xong')

# BVH của da (tư thế trung tính) cho tóc, mày
bvh = BVHTree.FromPolygons(to_b(PS).tolist(), FS.tolist())
def skin_radius(D):
    out = np.zeros(len(D))
    o = mathutils.Vector(tuple(to_b(HC[None])[0]))
    for i, d in enumerate(to_b(D)):
        # tia từ ngoài vào tâm: điểm da xa nhất theo hướng d
        far = o + mathutils.Vector(d) * 1.2
        hit = bvh.ray_cast(far, -mathutils.Vector(d), 1.2)
        out[i] = 1.2 - hit[3] if hit[0] is not None else 0.3
    return out

# L3: lưới khoảng cách có dấu của da 'bl' (cho mép cổ áo/khăn của cast3d tính theo đầu 'bl', không theo A-α)
_lo = np.array([-0.5, -0.7, -0.6]); _hs = 0.025; _n = np.array([41, 73, 51])
_G = np.stack(np.meshgrid(*[_lo[i] + _hs * np.arange(_n[i]) for i in range(3)], indexing='ij'), -1).reshape(-1, 3)
_sd = np.zeros(len(_G), np.float32)
for i, g in enumerate(to_b(_G)):
    loc, nrm, _, dist = bvh.find_nearest(mathutils.Vector(g)); _sd[i] = dist if (mathutils.Vector(g) - loc).dot(nrm) > 0 else -dist
import base64
SDF_META = {'lo': _lo.tolist(), 'h': _hs, 'n': _n.tolist(), 'order': 'x-major (ix, iy, iz)', 'b64': base64.b64encode(_sd.tobytes()).decode()}
log('lưới SDF da cho cổ áo xong')

# ======================= MẮT =======================
def iris_image():
    S = 256; yy, xx = np.mgrid[0:S, 0:S]; X = (xx + 0.5) / S * 2 - 1; Y = (yy + 0.5) / S * 2 - 1
    r = np.hypot(X, Y); ang = np.arctan2(Y, X); RI = 0.40   # tròng ≈ 0,44 R (nhãn cầu helper MPFB lớn hơn mắt thật)
    iris_c = np.array([0x7a, 0x66, 0x52]) / 255; ring = np.array([0x5a, 0x46, 0x36]) / 255
    fib = 0.5 + 0.5 * np.sin(ang * 61 + 3 * np.sin(ang * 7)) * np.sin(ang * 23 + 1.1); t = np.clip(r / RI, 0, 1.5)
    iv = iris_c * (0.85 + 0.35 * fib[..., None] * sstep(0.35, 0.6, t)[..., None])
    iv = iv * (1 - sstep(0.7, 0.95, t))[..., None] + ring * sstep(0.7, 0.95, t)[..., None]
    iv *= (1 - 0.5 * sstep(0.9, 1.0, t))[..., None]
    pup = sstep(0.36, 0.30, t); iv = iv * (1 - pup[..., None]) + np.array([0.02, 0.02, 0.025]) * pup[..., None]
    lin = srgb2lin(iv); sc = np.array([0.62, 0.59, 0.55]) * (1 - 0.12 * sstep(0.7, 1.05, r / 1.1))[..., None]
    m = sstep(1.03, 0.97, t)[..., None]; C = lin * m + sc * (1 - m)
    img = bpy.data.images.new('ida_iris', S, S, alpha=False); img.pixels.foreach_set(np.concatenate([np.clip(C, 0, 1), np.ones((S, S, 1))], 2).astype(np.float32).ravel()); img.pack(); return img
def sphere(R, nth=32, nph=40, bulge=0.06):
    th = np.linspace(0, np.pi, nth + 1); ph = np.linspace(0, 2 * np.pi, nph + 1)[:-1]; T, Pp = np.meshgrid(th, ph, indexing='ij')
    rr = R * (1 + bulge * sstep(0.80, 0.97, np.cos(T)))
    Pm = np.stack([rr * np.sin(T) * np.cos(Pp), rr * np.sin(T) * np.sin(Pp), rr * np.cos(T)], -1).reshape(-1, 3)
    f = [[i * nph + j, (i + 1) * nph + j, (i + 1) * nph + (j + 1) % nph, i * nph + (j + 1) % nph] for i in range(nth) for j in range(nph)]
    return Pm, np.array(f)
img = iris_image(); mat_eye = mk_mat('bl_eye', rough=0.1, spec=0.5, img=img, use_attr=False)
EYES = {}
# MPFB: hốc mắt là túi da; nhãn cầu helper nằm SAU vách túi → kéo nhãn cầu ra trước tới khi giác mạc vượt vách túi 0,008 H (ngay sau mép mí)
def first_hit_z(px, py):
    o = mathutils.Vector(tuple(to_b(np.array([[px, py, 1.0]]))[0])); d = mathutils.Vector(tuple(to_b(np.array([[0, 0, -1.0]]))[0]))
    h = bvh.ray_cast(o, d, 2.0); return 1.0 - h[3] if h[0] is not None else None
EYE_R_ = ER_r * 0.97
for c in (ER_c, EC):
    zh = first_hit_z(c[0], c[1]); dz_ = (zh + 0.008) - (c[2] + EYE_R_)
    log(f'mắt {c[0]:+.3f}: vách túi z {zh:.3f}, giác mạc z {c[2] + EYE_R_:.3f} → dời {dz_:+.3f}'); c[2] += max(0.0, dz_)
for nm, c in (('ida_eye_L', ER_c), ('ida_eye_R', EC)):
    Pm, Fm = sphere(EYE_R_)
    sx = 1 if c[0] > 0 else -1; yaw = -sx * 0.035                                   # hội tụ (mắt bên +x quay về −x)
    R = np.array([[math.cos(yaw), 0, math.sin(yaw)], [0, 1, 0], [-math.sin(yaw), 0, math.cos(yaw)]])
    pitch = 0.06; Rp = np.array([[1, 0, 0], [0, math.cos(pitch), -math.sin(pitch)], [0, math.sin(pitch), math.cos(pitch)]])  # nhìn hơi xuống
    uv = np.stack([0.5 + Pm[:, 0] / (2.2 * ER_r), 0.5 + Pm[:, 1] / (2.2 * ER_r)], 1)
    Pm = Pm @ (R @ Rp).T
    tri = Pm[Fm[:, :3]]; n_ = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    if np.median((n_ * tri.mean(1)).sum(1)) < 0: Fm = Fm[:, ::-1]
    EYES[nm] = mk_obj(nm, Pm, Fm, uv=uv, mat=mat_eye, loc=c)
log('mắt xong')

# ======================= MÀY BẠC (bám da bằng tia) =======================
def on_skin_front(xy):
    out = []
    for px, py in xy:
        o = mathutils.Vector(tuple(to_b(np.array([[px, py, 1.0]]))[0])); d = mathutils.Vector(tuple(to_b(np.array([[0, 0, -1.0]]))[0]))
        h = bvh.ray_cast(o, d, 2.0); out.append(1.0 - h[3] if h[0] is not None else E[2] + 0.05)
    return np.array(out)
def strip(rows):
    n, k, _ = rows.shape; P = rows.reshape(-1, 3)
    return P, np.array([[i * k + j, i * k + j + 1, (i + 1) * k + j + 1, (i + 1) * k + j] for i in range(n - 1) for j in range(k - 1)])
def merge(parts):
    P, Fs, C, Uv, off = [], [], [], [], 0
    for p, f, c, u in parts: P.append(p); Fs.append(np.asarray(f) + off); C.append(c); Uv.append(u); off += len(p)
    return np.concatenate(P), np.concatenate(Fs), np.concatenate(C), np.concatenate(Uv)
BX = EX + np.array([-0.115, -0.06, 0.0, 0.055, 0.098]); BY = EY + np.array([0.060, 0.076, 0.080, 0.069, 0.050])
brow_parts = []
for sx in (1, -1):
    for j in range(44):
        t = (j + rng.random() * 0.8) / 44
        bx = np.interp(t, np.linspace(0, 1, 5), BX); by = np.interp(t, np.linspace(0, 1, 5), BY) + (rng.random() - 0.5) * 0.008
        ang = np.radians(55 * (1 - t) ** 2 + 6 - 16 * t + (rng.random() - 0.5) * 12); tx, ty = np.cos(ang), np.sin(ang); Lb = 0.022 + 0.012 * rng.random()
        pts = np.array([[bx + tx * Lb * tt, by + ty * Lb * tt - 0.004 * tt * tt * t] for tt in np.linspace(0, 1, 5)])
        zz = on_skin_front(pts) + 0.0012 + 0.0008 * np.sin(np.pi * np.linspace(0, 1, 5))
        rows = []
        for (px, py), pz, tt in zip(pts, zz, np.linspace(0, 1, 5)):
            hw = 0.0032 * (1 - 0.8 * tt) + 0.0004; rows.append([[sx * (px + ty * hw), py - tx * hw, pz], [sx * (px - ty * hw), py + tx * hw, pz]])
        Pb, Fb = strip(np.array(rows))
        tri = Pb[Fb[:, :3]]; n_ = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
        if np.median(n_[:, 2]) < 0: Fb = Fb[:, ::-1]
        k = 0.70 + 0.14 * rng.random()
        brow_parts.append((Pb, Fb, np.repeat(np.linspace(0.85, 1.0, 5), 2)[:, None] * k * np.ones((1, 3)), np.stack([np.tile([0, 1], 5), np.repeat(np.linspace(0, 1, 5), 2)], 1)))
Pbr, Fbr, Cbr, Ubr = merge(brow_parts)
HAIR_LIN = tuple(hexlin(HAIR))
mat_hair = mk_mat('bl_hair', HAIR_LIN, rough=0.55, spec=0.35); mat_brow = mk_mat('bl_brow', HAIR_LIN, rough=0.6, spec=0.3)
brows = mk_obj('ida_brows', Pbr, Fbr, cols=Cbr, uv=Ubr, mat=mat_brow)
# mày đi theo shape key của da: dịch bằng dịch chuyển của đỉnh da gần nhất
kd = mathutils.kdtree.KDTree(len(PS))
for i, p in enumerate(to_b(PS)): kd.insert(p, i)
kd.balance()
near = np.array([kd.find(p)[1] for p in to_b(Pbr)])
brows.shape_key_add(name='Basis', from_mix=False)
for k, D in SKD.items():
    sk = brows.shape_key_add(name=k, from_mix=False); sk.data.foreach_set('co', to_b(Pbr + D[near]).astype(np.float32).ravel())
log('mày xong')

# ======================= TÓC =======================
HAT_Y, HAT_TILT, RX0, RZ0, HCZ, HAT_FIT = float(os.environ.get('HAT_Y', 0.775)), 0.08, 0.78 * 0.52, 0.78 * 0.52 * 1.12, 0.0, False
HAT_PUSH = 0.26   # = cast3d 'bl': hatPivot.rotation.x = −0,26·hat_back (bản lề ở tâm sọ HC)
RPUSH = np.array([[1, 0, 0], [0, math.cos(HAT_PUSH), -math.sin(HAT_PUSH)], [0, math.sin(HAT_PUSH), math.cos(HAT_PUSH)]])   # hướng ở tư thế đẩy → hướng tương ứng ở tư thế nghỉ
ct, st = math.cos(-HAT_TILT), math.sin(-HAT_TILT); RXm = np.array([[1, 0, 0], [0, ct, -st], [0, st, ct]])
def sdir(th, ph): return np.stack([np.sin(th) * np.sin(ph), np.cos(th), np.sin(th) * np.cos(ph)], -1)
def band_radius(D):
    o = RXm @ (HC - np.array([0, HAT_Y, HCZ])); d = D @ RXm.T
    A = d[:, 0] ** 2 / RX0 ** 2 + d[:, 2] ** 2 / RZ0 ** 2; B = 2 * (o[0] * d[:, 0] / RX0 ** 2 + o[2] * d[:, 2] / RZ0 ** 2); C = o[0] ** 2 / RX0 ** 2 + o[2] ** 2 / RZ0 ** 2 - 1
    r = (-B + np.sqrt(np.maximum(B * B - 4 * A * C, 0))) / (2 * np.maximum(A, 1e-9)); return r, o[1] + d[:, 1] * r
_rs_cache = {}
def hair_radius(th, ph):
    th = np.asarray(th, float); ph = np.asarray(ph, float); D = sdir(th, ph).reshape(-1, 3); rs = skin_radius(D)
    tm = theta_max(ph).ravel(); thr = th.ravel(); aph = np.abs(ph).ravel()
    side = gauss(aph - 1.55, 0.55) * sstep(0.95, 1.3, thr); nape = gauss(aph - np.pi, 0.7) * sstep(1.6, 2.1, thr)
    tap = np.clip((tm - thr) / 0.045, 0, 1) ** 0.35                                   # L3: tóc dày ngay sau chân tóc
    rh = rs + (0.040 + 0.020 * side + 0.014 * nape) * tap
    rb, yh = band_radius(D); win = sstep(-0.05, 0.0, yh) * sstep(0.17, 0.12, yh) * (thr < tm)
    if HAT_FIT:
        rh = rh + (np.clip(rb - 0.010, rs + 0.006, rh + 0.012) - rh) * win     # L3: băng mũ ÉP tóc (và tóc đầy tới băng, tối đa +0,012) → mũ tỳ lên tóc
        rb2, yh2 = band_radius(D @ RPUSH.T); win2 = sstep(-0.06, 0.0, yh2) * sstep(0.17, 0.12, yh2) * (thr < tm)   # tư thế ĐẨY MŨ (s36→) : băng mũ quay quanh tâm sọ
        rh = rh + (np.maximum(np.minimum(rh, rb2 - 0.010), rs + 0.004) - rh) * win2
    # (lượt 2: bỏ 'ép tóc theo băng mũ' — tạo gờ kiểu mũ bảo hiểm khi mũ đẩy ra sau; băng mũ tỳ lên tóc tự nhiên)
    rh = np.where(thr >= tm, rs - 0.002, rh)
    return rh.reshape(th.shape), rs.reshape(th.shape)
def band_clamp(c):   # L3: dải tóc / sợi tơ nằm DƯỚI băng mũ (không thò ra thành 'viền ren' dưới băng)
    if not HAT_FIT: return c
    d_ = c - HC; r_ = np.linalg.norm(d_, axis=1); D_ = d_ / r_[:, None]; rb_, yh_ = band_radius(D_)
    win_ = sstep(-0.06, 0.0, yh_) * sstep(0.17, 0.12, yh_); r_ = r_ + (np.minimum(r_, rb_ - 0.016) - r_) * win_
    rb2, yh2 = band_radius(D_ @ RPUSH.T); w2 = sstep(-0.06, 0.0, yh2) * sstep(0.17, 0.12, yh2); r_ = r_ + (np.minimum(r_, rb2 - 0.016) - r_) * w2
    return HC + D_ * r_[:, None]
def brim_ao(P, C):   # Cổng 6: bóng tiếp xúc dưới vành/băng mũ trên tóc (che khuất thật: vành chắn ánh trời) — không phải đèn
    if not HAT_FIT or C is None: return C
    yl = ((np.asarray(P) - np.array([0, HAT_Y, HCZ])) @ RXm.T)[:, 1]
    k = 1 - 0.6 * sstep(-0.10, -0.004, yl) * sstep(0.03, 0.0, yl)
    C = np.array(C, float); C[:, :3] *= k[:, None]; return C
def hair_point(th, ph, off=0.0):
    rh, rs = hair_radius(th, ph); return HC + sdir(th, ph) * (rh + off)[..., None]
# L3: MŨ NGỒI LÊN SỌ — đo mặt cắt khối tóc ở dải băng mũ (hệ mũ nghiêng 0,08), đặt miệng mũ = elip ôm tóc × 0,985 (ép nhẹ), tâm mũ theo tâm đầu
_ph = np.linspace(-np.pi, np.pi, 181)[:-1]; _t = np.linspace(0.75, 1.75, 41); _PH, _TT = np.meshgrid(_ph, _t)
_rh, _ = hair_radius(_TT, _PH); _P = HC + sdir(_TT, _PH) * _rh[..., None]; _L = (_P.reshape(-1, 3) - np.array([0, HAT_Y, 0])) @ RXm.T
_m = (_L[:, 1] > 0.0) & (_L[:, 1] < 0.12)
_zf, _zb = _L[_m, 2].max(), _L[_m, 2].min(); HCZ = 0.5 * (_zf + _zb); _rz = 0.5 * (_zf - _zb); _rx = np.abs(_L[_m, 0]).max()
RX0 = _rx * 0.975; RZ0 = _rz * 0.975; HAT_FIT = True   # Cổng 6: miệng mũ ôm tóc theo CẢ hai trục (trước: tỷ lệ cố định 1,12 → hở một trục); ép 2,5 %
log(f'mũ: tóc ở băng rộng {2 * _rx:.3f}, sâu {2 * _rz:.3f}, tâm z {HCZ:+.3f} → miệng mũ rx {RX0:.4f} rz {RZ0:.4f} (sheet 0,4056 / 0,4543)')
log('vỏ tóc…')
NU, NV = 150, 44
phg = np.linspace(-np.pi, np.pi, NU + 1)[:-1]; tg = np.linspace(0, 1, NV + 1); PH, TT = np.meshgrid(phg, tg, indexing='xy')
TH = 0.05 + (theta_max(PH) - 0.05) * TT; RH, RS = hair_radius(TH, PH)
Psh = (HC + sdir(TH, PH) * RH[..., None]).reshape(-1, 3)
fsh = np.array([[i * NU + j, i * NU + (j + 1) % NU, (i + 1) * NU + (j + 1) % NU, (i + 1) * NU + j] for i in range(NV) for j in range(NU)])
tri = Psh[fsh[:, :3]]; n_ = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
if np.median((n_ * (tri.mean(1) - HC)).sum(1)) < 0: fsh = fsh[:, ::-1]
csh = (0.80 + 0.04 * fbm(Psh[:, 0] * 20, Psh[:, 1] * 20, Psh[:, 2] * 20, 5, 2))[:, None] * np.ones((1, 3))
shell = mk_obj('ida_hair_shell', Psh, fsh, cols=brim_ao(Psh, csh), uv=np.stack([(PH.ravel() + np.pi) / (2 * np.pi) * 8, TH.ravel() * 2], 1), mat=mat_hair)
def card(th0, ph0, th1, ph1, w0, bow, k, nrow=14, off0=0.002):
    t = np.linspace(0, 1, nrow); th = th0 + (th1 - th0) * t; ph = ph0 + (ph1 - ph0) * t
    c = band_clamp(hair_point(th, ph, off0 + bow * np.sin(np.pi * t))); rad = c - HC; rad /= np.linalg.norm(rad, axis=1)[:, None]
    tg_ = np.gradient(c, axis=0); tg_ /= np.maximum(np.linalg.norm(tg_, axis=1), 1e-9)[:, None]; bi = np.cross(tg_, rad); bi /= np.maximum(np.linalg.norm(bi, axis=1), 1e-9)[:, None]
    wv = w0 * (0.12 + 0.88 * np.sin(np.pi * np.clip(0.06 + 0.94 * t, 0, 1)) ** 0.8)
    Pc, Fc = strip(np.stack([c - bi * wv[:, None] * 0.5, c + rad * (0.18 * wv)[:, None], c + bi * wv[:, None] * 0.5], 1))
    tri = Pc[Fc[:, :3]]; n_ = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    if np.median((n_ * (tri.mean(1) - HC)).sum(1)) < 0: Fc = Fc[:, ::-1]
    sh = np.repeat(0.86 + 0.14 * np.sin(np.pi * np.clip(0.1 + 0.9 * t, 0, 1)), 3) * np.tile([0.93, 1.0, 0.93], nrow)
    return Pc, Fc, np.clip((sh * k)[:, None] * np.ones((1, 3)), 0, 1.05), np.stack([np.tile([0, 0.5, 1], nrow), np.repeat(t * 3, 3)], 1)
log('dải tóc…')
cards = []
for sx in (1, -1):
    for i in range(80):
        ph0 = sx * (0.72 + 2.05 * i / 79 + (rng.random() - 0.5) * 0.04); th0 = theta_max(ph0) - 0.012 - 0.06 * rng.random()
        ph1 = sx * (np.pi - 0.22 - 0.45 * rng.random()); th1 = 1.62 + 0.2 * rng.random()
        if abs(ph0) > 2.3: th1 = min(th1, th0 - 0.35)
        cards.append(card(th0, ph0, th1, ph1, 0.020 + 0.012 * rng.random(), 0.002 + 0.003 * rng.random(), 0.9 + 0.14 * rng.random()))
    for i in range(36):
        ph0 = sx * (0.35 + 2.2 * i / 35 + (rng.random() - 0.5) * 0.08); th0 = theta_max(ph0) - 0.14 - 0.12 * rng.random()
        cards.append(card(th0, ph0, 1.58 + 0.12 * rng.random(), sx * (np.pi - 0.3 - 0.35 * rng.random()), 0.03 + 0.01 * rng.random(), 0.004, 0.92 + 0.12 * rng.random()))
for i in range(44):
    ph0 = -0.95 + 1.9 * i / 43 + (rng.random() - 0.5) * 0.03; sg = 1 if ph0 >= 0 else -1; th0 = theta_max(ph0) - 0.01 - 0.03 * rng.random()
    cards.append(card(th0, ph0, th0 - 0.6, ph0 * 1.3 + sg * 0.25, 0.024 + 0.01 * rng.random(), 0.003, 0.92 + 0.12 * rng.random()))
Pcd, Fcd, Ccd, Ucd = merge(cards); mk_obj('ida_hair_cards', Pcd, Fcd, cols=brim_ao(Pcd, Ccd), uv=Ucd, mat=mat_hair)
fines = []
for i in range(260):
    ph = -2.55 + 5.1 * (i + rng.random() * 0.8) / 260; sg = 1 if ph >= 0 else -1; tm = theta_max(ph)
    ths, the = tm + 0.012 + 0.02 * rng.random(), tm - 0.07 - 0.06 * rng.random(); phe = ph + sg * (0.05 + 0.08 * (abs(ph) > 0.9)) + (rng.random() - 0.5) * 0.03
    t = np.linspace(0, 1, 8); th = ths + (the - ths) * t; pp = ph + (phe - ph) * t
    rh, rs = hair_radius(th, pp); r = np.maximum(rs + 0.0015, rh - 0.003) + 0.0012 * np.sin(np.pi * t)
    c = band_clamp(HC + sdir(th, pp) * r[:, None]); rad = c - HC; rad /= np.linalg.norm(rad, axis=1)[:, None]
    tg_ = np.gradient(c, axis=0); tg_ /= np.linalg.norm(tg_, axis=1)[:, None]; bi = np.cross(tg_, rad); bi /= np.linalg.norm(bi, axis=1)[:, None]
    wv = (0.0035 + 0.002 * rng.random()) * np.sin(np.pi * np.clip(0.08 + 0.9 * t, 0, 1))
    Pf, Ff = strip(np.stack([c - bi * wv[:, None] * 0.5, c + bi * wv[:, None] * 0.5], 1))
    tri = Pf[Ff[:, :3]]; n_ = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    if np.median((n_ * (tri.mean(1) - HC)).sum(1)) < 0: Ff = Ff[:, ::-1]
    fines.append((Pf, Ff, np.full((len(Pf), 3), 0.95), np.stack([np.tile([0, 1], 8), np.repeat(t, 2)], 1)))
_ylr = lambda P_: ((np.asarray(P_) - np.array([0, HAT_Y, HCZ])) @ RXm.T)[:, 1]
_nf = len(fines); fines = [f for f in fines if not (-0.11 < _ylr(f[0][:2]).mean() < 0.03)]   # Cổng 6: bỏ sợi tơ mọc ngay dưới băng mũ (thành 'viền diềm' trắng xù dưới vành)
log(f'sợi tơ: bỏ {_nf - len(fines)} / {_nf} sợi dưới băng mũ')
Pfi, Ffi, Cfi, Ufi = merge(fines); mk_obj('ida_hair_fine', Pfi, Ffi, cols=brim_ao(Pfi, Cfi), uv=Ufi, mat=mat_hair)
# ---- búi LIỀN ĐẦU: tâm búi đặt theo mặt tóc ở gáy (dưới vành mũ), lún 45 % bề dày vào khối tóc ----
av = np.array([0.0, -0.25, -1.0]); av /= np.linalg.norm(av); e1 = np.array([1.0, 0, 0]); e2 = np.cross(av, e1); e2 /= np.linalg.norm(e2)
BR = (0.262, 0.232, 0.17)
nape_pt = hair_point(np.array([1.95]), np.array([np.pi]))[0]
Cb = nape_pt + av * BR[2] * 0.55
Pm, Fm = sphere(1.0, 20, 32, 0.0)
Pcore = (Cb - av * 0.07) + Pm[:, 0:1] * BR[0] * 0.84 * e1 + Pm[:, 1:2] * BR[1] * 0.84 * e2 + Pm[:, 2:3] * BR[2] * 0.75 * av   # L3: lõi lùi vào khối tóc, nằm dưới vòng xoắn (không lộ quả cầu trơn ở góc nghiêng)
tri = Pcore[Fm[:, :3]]; n_ = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
if np.median((n_ * (tri.mean(1) - Cb)).sum(1)) < 0: Fm = Fm[:, ::-1]
bun_parts = [(Pcore, Fm, np.full((len(Pcore), 3), 0.78), np.zeros((len(Pcore), 2)))]
# L3: búi = lõi tối + 40 LỌN tóc quấn quanh lõi theo các vòng nghiêng khác nhau (như búi xoắn thật) → mọi góc đều thấy vân lọn, không còn quả cầu trơn
Pcore = Cb + Pm[:, 0:1] * BR[0] * e1 + Pm[:, 1:2] * BR[1] * e2 + Pm[:, 2:3] * BR[2] * av
bun_parts[0] = (Pcore, Fm, np.full((len(Pcore), 3), 0.5), np.zeros((len(Pcore), 2)))
NL = 40; th = np.linspace(0, 2 * np.pi, 97)
for kq in range(NL):
    phi = 2 * np.pi * kq / NL + 0.12 * rng.random(); tilt = np.radians(50 + 30 * rng.random())
    nrm = np.cos(tilt) * av + np.sin(tilt) * (np.cos(phi) * e1 + np.sin(phi) * e2)
    u = np.cross(nrm, av); u /= np.linalg.norm(u); v = np.cross(nrm, u)
    dirs = np.cos(th)[:, None] * u + np.sin(th)[:, None] * v
    rad = 1 / np.sqrt((dirs @ e1 / BR[0]) ** 2 + (dirs @ e2 / BR[1]) ** 2 + (dirs @ av / BR[2]) ** 2)
    c = Cb + dirs * (rad + 0.004 + 0.003 * rng.random() + 0.002 * np.sin(3 * th + kq))[:, None]
    tg_ = np.gradient(c, axis=0); tg_ /= np.linalg.norm(tg_, axis=1)[:, None]; up = dirs - (dirs * tg_).sum(1)[:, None] * tg_; up /= np.linalg.norm(up, axis=1)[:, None]
    bi = np.cross(tg_, up); w = (0.030 + 0.012 * rng.random()) * np.ones(len(th))
    rows = np.stack([c - bi * (w / 2)[:, None], c + up * 0.004, c + bi * (w / 2)[:, None]], 1)
    Pt, Ft = strip(rows); tri = Pt[Ft[:, :3]]; n_ = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    if np.median((n_ * np.repeat(up[:-1], 2, 0)).sum(1)) < 0: Ft = Ft[:, ::-1]
    k = 0.82 + 0.18 * rng.random() + 0.05 * np.sin(np.linspace(0, 20 + kq, len(th)))
    col = np.repeat(k, 3)[:, None] * np.tile([0.62, 1.0, 0.62], len(th))[:, None] * np.ones((1, 3))
    bun_parts.append((Pt, Ft, col, np.stack([np.tile([0, 0.5, 1], len(th)), np.repeat(th * 3, 3)], 1)))
Pbn, Fbn, Cbn, Ubn = merge(bun_parts); mk_obj('ida_bun', Pbn, Fbn, cols=Cbn, uv=Ubn, mat=mat_hair)
log('tóc xong')

# ---- hoa tai: điểm thấp nhất của dái tai mỗi bên ----
# L3: dái tai = các đỉnh mà target MPFB 'ear-lobe-incr' dịch nhiều nhất (đúng giải phẫu), hoa tai ở điểm THẤP nhất của dái, ra ngoài 0,01 H
EARRING = {}
_kbs = hum.data.shape_keys.key_blocks; _b0 = np.zeros(len(BASE) * 3); _kbs[0].data.foreach_get('co', _b0)
for lr in ('l', 'r'):
    _a = np.zeros(len(BASE) * 3); _kbs['d_' + lr + '-ear-lobe-incr'].data.foreach_get('co', _a); _d = np.linalg.norm((_a - _b0).reshape(-1, 3), axis=1)
    _top = np.argsort(_d)[-25:]; _pl = Qs[_top]; _low = _pl[np.argmin(_pl[:, 1])]
    j = np.argmin(np.linalg.norm(PS - _low, axis=1)); sx = 1.0 if PS[j, 0] > 0 else -1.0
    EARRING['L' if sx > 0 else 'R'] = (PS[j] + np.array([sx * 0.010, 0.004, 0.0])).round(4).tolist()
log(f'hoa tai (dái tai): {EARRING}')

meta = {'lids': LIDS, '_doc': "Cửa mặt Ida lượt 2 (W4, MPFB2 CC0). Hệ đầu cast3d: đơn vị H; y = 0 cằm, 1 đỉnh sọ; +z mặt. Shape key = morph target glTF; "
                "TÊN = kênh facerig.js (16) + vis_* (6 khẩu hình); preset = trọng số trên kênh. Kênh dựng từ expression unit của MPFB (CH_UNITS).",
        'mpfb': {'commit': '3edf9df0551765be43563d047888cf7877eb89b4', 'version': '2.0.17', 'age': AGE, 'macro': macro, 'detail': DETAIL},
        'stylize': {'SX': float(SX), 'SZ': float(SZ), 'SN': float(SN), 'head_len_m_mpfb': float(HL)},
        'eyes': {'L': ER_c.round(4).tolist(), 'R': EC.round(4).tolist(), 'r': round(ER_r * 0.97, 4)}, 'mouth': MOUTH.round(4).tolist(), 'jaw': JAW.round(4).tolist(),
        'hatHinge': HC.tolist(), 'hat': {'y': HAT_Y, 'rx': round(float(RX0), 4), 'rz': round(float(RZ0), 4), 'cz': round(float(HCZ), 4), 'tilt': HAT_TILT},
        'sdf': SDF_META, 'correctives': {'corr_mouth': {'mul': ['frown'], 'max': ['press', 'chinRaise']}, 'corr_smile_lip': {'mul': ['smile'], 'lim': {'jawOpen': 0.12}}}, 'earring': EARRING, 'channels': CHANNELS, 'ch_units': CH_UNITS, 'visemes': VISEMES, 'presets': PRESETS,
        'key_max_disp_H': {k: round(float(np.abs(D).max()), 4) for k, D in SKD.items()}}
bpy.data.objects.remove(hum)
meta['counts'] = {ob.name: len(ob.data.vertices) for ob in SC.objects if ob.type == 'MESH'}
json.dump(meta, open(os.path.join(OUT, os.environ.get('BL_NAME', 'ida_bl') + '.json'), 'w'), indent=1, ensure_ascii=False)
for ob in SC.objects: ob.select_set(ob.type == 'MESH')
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, os.environ.get('BL_NAME', 'ida_bl') + '.glb'), export_format='GLB', use_selection=True, export_yup=True, export_apply=False,
                          export_morph=True, export_morph_normal=False, export_vertex_color='ACTIVE', export_normals=True, export_texcoords=True,
                          export_materials='EXPORT', export_animations=False)
log(f"glb {os.path.getsize(os.path.join(OUT, os.environ.get('BL_NAME', 'ida_bl') + '.glb')) / 1e6:.1f} MB; đỉnh {meta['counts']}")
if BLEND: bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(BLEND), compress=True); log('lưu ' + BLEND)
