# Cine Lab · Cổng 6 (gói W4T, thân Cas "cách A") — THÂN + ÁO LEN + QUẦN + DA ỐNG CHÂN của Cas dựng từ lưới thân MPFB2 (CC0; RIGHTS W4-MPFB-A4).
# Chạy:  /opt/bpy/bin/python design/cong3/v2/char3d/blender/build_cas_body_bl.py -- <repo mpfb2> <thư mục ra>
# Ra:    <ra>/cas_body_bl.json — lưới đã chia 1 cấp, toạ độ HỆ ROOT cast3d ở TƯ THẾ BIND (khai trong tệp), trọng số theo 16 khớp cast3d.
# Cách A (không đổi rig, không đổi tư thế layout):
#   1. Người MPFB như đầu 'bl' và tay MPFB (nam 10 tuổi) + rig 'default' CHỈ để lấy trọng số (không dùng rig MPFB khi diễn).
#   2. UỐN HÌNH về khung cast3d theo sheet Cas (giữ hệ tỷ lệ v1.6): mỗi đoạn (thân, cánh tay trên, cẳng tay, đùi, cẳng chân) có phép
#      biến đổi riêng: gốc đoạn MPFB → khớp cast3d, dài theo sheet, ngang theo hệ số vòng; trộn theo trọng số MPFB (mượt qua khớp).
#   3. Trọng số cast3d = gộp trọng số MPFB theo bảng 163 → 16 khớp (đòn → thân; vai MPFB chia thân/vai).
#   4. Áo len, quần: VỎ tự dựng từ lưới thân đã uốn (lệch theo pháp tuyến, làm mượt bỏ chi tiết cơ thể, nếp vải thủ tục);
#      da ống chân lấy thẳng từ lưới thân. Không dùng quần áo/da/texture MPFB.
#   5. Tư thế BIND = vai dạng BIND_SH độ, khuỷu gập BIND_EL độ (gần tư thế hay dùng; ít biến dạng LBS nhất). three.js ghi bind ở tư thế này.
import sys, os, json, time, importlib, base64, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import bpy, addon_utils
from sdfnp import sstep, gauss

argv = sys.argv[sys.argv.index('--') + 1:]
MP, OUT = argv[0], os.path.abspath(argv[1]); os.makedirs(OUT, exist_ok=True)
T0 = time.time(); log = lambda *a: print(f'[than {time.time() - T0:6.1f}s]', *a, flush=True)
PRM = dict(BIND_SH=24.0, BIND_EL=20.0, LIFT=0.5, G_ARM=1.0, G_LEG=0.82, SW=0.016, SW_BELLY=0.012, SL=0.012, TR=0.010, SMOOTH=110,
           # W4T lượt 2 (chủ dự án 29/09/2026): tay theo tỷ lệ MPFB (độ dài NHÌN THẤY, H; đo trên người MPFB nam 10 tuổi, quy về chiều cao sheet),
           # gấu áo theo sheet v1.6 (2,17 H; HEM_DROP chỉ để thử) buông (phủ qua cạp quần), quần ống thẳng rộng (bán kính TR_R m), đũng mượt; áo nới, ngực mượt.
           UA_V=-1, FA_V=-1, HEM_DROP=0.0, HEM_FLARE=0.005, HIP2PELVIS=0.6, TR_R=0.051, TR_RZ=0.92, TR_SMOOTH=40, CROTCH_SMOOTH=40, CHEST_SMOOTH=120, SEAT_SMOOTH=150)
for a in argv[2:]:
    k, v = a.split('='); PRM[k] = float(v)

bpy.ops.wm.read_factory_settings(use_empty=True)
ext = bpy.utils.user_resource('EXTENSIONS', path='user_default', create=True)
if not os.path.exists(os.path.join(ext, 'mpfb')): os.symlink(os.path.join(MP, 'src', 'mpfb'), os.path.join(ext, 'mpfb'))
addon_utils.enable('bl_ext.user_default.mpfb', default_set=True, handle_error=None)
HS_ = importlib.import_module('bl_ext.user_default.mpfb.services.humanservice').HumanService
TS_ = importlib.import_module('bl_ext.user_default.mpfb.services.targetservice').TargetService
SHEET = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'model-sheet', 'cas.json')))
H = SHEET['H_m']; PT = SHEET['parts']; JD = SHEET['joints_default']

# ---------------- 1. người MPFB (như build_cas_bl.py / build_hands_bl.py) ----------------
macro = TS_.get_default_macro_info_dict()
macro.update({'gender': 1.0, 'age': 0.1875 * (10 - 1) / (11 - 1), 'muscle': 0.5, 'weight': 0.45, 'proportions': 0.5})
macro['race'] = {'asian': 0.15, 'caucasian': 0.7, 'african': 0.15}
hum = HS_.create_human(macro_detail_dict=macro, scale=0.1, mask_helpers=False, feet_on_ground=True)
rig = HS_.add_builtin_rig(hum, 'default', import_weights=True)
for m in list(hum.modifiers): m.show_viewport = False
bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get(); ev = hum.evaluated_get(dg); me = ev.to_mesh()
BODY_N = 13380
MW = np.array(hum.matrix_world)
Pm = np.zeros(len(me.vertices) * 3); me.vertices.foreach_get('co', Pm); Pm = (MW @ np.c_[Pm.reshape(-1, 3), np.ones(len(me.vertices))].T).T[:BODY_N, :3]
FACES = [tuple(p.vertices) for p in me.polygons if max(p.vertices) < BODY_N]
ev.to_mesh_clear()
cv = lambda p: np.stack([p[..., 0], p[..., 2], -p[..., 1]], -1)        # MPFB (z lên, −y trước) → cast3d (y lên, +z trước)
P0 = cv(Pm)
RW = np.array(rig.matrix_world)
BH = {b.name: cv((RW @ np.r_[b.head_local, 1])[:3]) for b in rig.data.bones}
BONES = [b.name for b in rig.data.bones]; BI = {n: i for i, n in enumerate(BONES)}
gname = {g.index: g.name for g in hum.vertex_groups}
WM = np.zeros((BODY_N, len(BONES)), np.float32)
for v in hum.data.vertices[:BODY_N]:
    for g in v.groups:
        n = gname[g.group]
        if n in BI: WM[v.index, BI[n]] += g.weight
WM /= np.maximum(1e-9, WM.sum(1, keepdims=True))
log('MPFB', BODY_N, 'đỉnh', len(FACES), 'mặt', len(BONES), 'xương; cao', round(P0[:, 1].max() - P0[:, 1].min(), 3))

# ---------------- 2. khung cast3d (sheet) ở tư thế bind ----------------
JN = ['pelvis', 'spine', 'neck', 'head', 'shoulder_L', 'elbow_L', 'wrist_L', 'shoulder_R', 'elbow_R', 'wrist_R', 'hip_L', 'knee_L', 'ankle_L', 'hip_R', 'knee_R', 'ankle_R']
JI = {n: i for i, n in enumerate(JN)}
tL, nL = PT['torso']['length'], PT['neck']['length']; ua, fa, th, sh = PT['upper_arm']['length'], PT['forearm']['length'], PT['thigh']['length'], PT['shin']['length']
hipY = (0.10 + sh + th) * H; shX, shY, hipX = JD['shoulder_spacing_H'] / 2, tL - JD['shoulder_offset_from_torso_top_H'], JD['hip_joint_spacing_H'] / 2
PAR = {'pelvis': None, 'spine': 'pelvis', 'neck': 'spine', 'head': 'neck'}
OFF = {'pelvis': [0, hipY, 0], 'spine': [0, 0, 0], 'neck': [0, tL * H, 0], 'head': [0, nL * H, 0]}
for s, sx in (('L', 1), ('R', -1)):
    PAR.update({f'shoulder_{s}': 'spine', f'elbow_{s}': f'shoulder_{s}', f'wrist_{s}': f'elbow_{s}', f'hip_{s}': 'pelvis', f'knee_{s}': f'hip_{s}', f'ankle_{s}': f'knee_{s}'})
    OFF.update({f'shoulder_{s}': [sx * shX * H, shY * H, 0], f'elbow_{s}': [0, -ua * H, 0], f'wrist_{s}': [0, -fa * H, 0],
                f'hip_{s}': [sx * hipX * H, 0, 0], f'knee_{s}': [0, -th * H, 0], f'ankle_{s}': [0, -sh * H, 0]})
def Rx(a): c, s = math.cos(a), math.sin(a); return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
def Rz(a): c, s = math.cos(a), math.sin(a); return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
D2R = math.pi / 180
BIND = {'shoulder_L': [0, 0, PRM['BIND_SH']], 'shoulder_R': [0, 0, -PRM['BIND_SH']], 'elbow_L': [-PRM['BIND_EL'], 0, 0], 'elbow_R': [-PRM['BIND_EL'], 0, 0]}   # độ, Euler XYZ như applyPose
def build_joints():
    JW = {}; JR = {}
    for n in JN:
        e = BIND.get(n, [0, 0, 0]); Rl = Rx(e[0] * D2R) @ Rz(e[2] * D2R)
        if PAR[n] is None: JW[n] = np.array(OFF[n], float); JR[n] = Rl
        else: JW[n] = JW[PAR[n]] + JR[PAR[n]] @ np.array(OFF[n], float); JR[n] = JR[PAR[n]] @ Rl
    return JW, JR
JW, JR = build_joints()

# ---------------- 3. uốn hình MPFB → cast3d ----------------
def rot_between(a, b):
    a = a / np.linalg.norm(a); b = b / np.linalg.norm(b); v = np.cross(a, b); c = float(a @ b)
    if np.linalg.norm(v) < 1e-9: return np.eye(3)
    K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]]); return np.eye(3) + K + K @ K / (1 + c)
p_m = (BH['upperleg01.L'] + BH['upperleg01.R']) / 2; n_m = BH['neck01']
SY = (tL * H) / (n_m[1] - p_m[1]); SX = shX * H / BH['upperarm01.L'][0]; SZ = 0.92
TORSO_C = JW['pelvis']
def torso_tf(V):
    d = V - p_m; out = TORSO_C + d * np.array([SX, SY, SZ])
    # NÂNG VAI: đưa khớp vai giải phẫu MPFB lên gần tâm quay vai cast3d (LIFT = tỷ lệ bù), chỉ phần bên (|x| lớn), không kéo cổ
    gap = JW['shoulder_L'][1] - (TORSO_C[1] + (BH['upperarm01.L'][1] - p_m[1]) * SY)
    lat = sstep(0.035, 0.085, np.abs(out[:, 0])); vert = sstep(JW['spine'][1] + 0.12, JW['shoulder_L'][1] - 0.02, out[:, 1])
    out[:, 1] += PRM['LIFT'] * gap * lat * vert
    return out
GAP_SH = JW['shoulder_L'][1] - (TORSO_C[1] + (BH['upperarm01.L'][1] - p_m[1]) * SY)
# W4T lượt 2: TAY THEO TỶ LỆ MPFB. Độ dài nhìn thấy = độ dài xương MPFB × (chiều cao sheet / chiều cao MPFB); khớp vai cast3d cao hơn gốc cánh tay
# (khớp vai giải phẫu, sau khi nâng vai) (1 − LIFT)·GAP_SH, nên độ dài KHỚP tay trên = nhìn thấy + phần đó. Không đổi khớp vai, thân, chân.
k_h = SHEET['total_height_H'] * H / (P0[:, 1].max() - P0[:, 1].min())
ua_m = np.linalg.norm(BH['lowerarm01.L'] - BH['upperarm01.L']) * k_h; fa_m = np.linalg.norm(BH['wrist.L'] - BH['lowerarm01.L']) * k_h
if PRM['UA_V'] < 0: PRM['UA_V'] = round(float(ua_m / H), 4)   # −1 = lấy từ MPFB; 0 = giữ sheet v1.4
if PRM['FA_V'] < 0: PRM['FA_V'] = round(float(fa_m / H), 4)
if PRM['UA_V'] > 0: ua = PRM['UA_V'] + (1 - PRM['LIFT']) * GAP_SH / H
if PRM['FA_V'] > 0: fa = PRM['FA_V']
for s in 'LR': OFF[f'elbow_{s}'] = [0, -ua * H, 0]; OFF[f'wrist_{s}'] = [0, -fa * H, 0]
JW, JR = build_joints()
ARM = {'upper_arm': round(float(ua), 4), 'forearm': round(float(fa), 4), 'upper_arm_visible': PRM['UA_V'], 'forearm_visible': PRM['FA_V'],
       'mpfb_m': {'upper_arm': round(float(ua_m), 4), 'forearm': round(float(fa_m), 4), 'k_height': round(float(k_h), 4)}, 'sheet': {'upper_arm': PT['upper_arm']['length'], 'forearm': PT['forearm']['length']}, 'v1_4': {'upper_arm': 0.92, 'forearm': 0.82}}
log('tay MPFB: xương (m, quy chiều cao)', ARM['mpfb_m'], '→ khớp cast3d (H)', ARM['upper_arm'], ARM['forearm'])
def seg_tf(a, b, A, B, g):
    dm = b - a; Lm = np.linalg.norm(dm); dm = dm / Lm; Lc = np.linalg.norm(B - A); R = rot_between(dm, B - A)
    def f(V):
        w = V - a; t = w @ dm; p = w - t[:, None] * dm
        return A + (R @ ((Lc / Lm) * t[:, None] * dm + g * p).T).T
    return f
TF = {'torso': torso_tf}
for s in 'LR':
    anc = JW[f'shoulder_{s}'] - np.array([0, (1 - PRM['LIFT']) * GAP_SH, 0])   # gốc cánh tay: nơi thân (đã nâng) đặt khớp vai MPFB
    TF[f'ua_{s}'] = seg_tf(BH[f'upperarm01.{s}'], BH[f'lowerarm01.{s}'], anc, JW[f'elbow_{s}'], PRM['G_ARM'])
    TF[f'fa_{s}'] = seg_tf(BH[f'lowerarm01.{s}'], BH[f'wrist.{s}'], JW[f'elbow_{s}'], JW[f'wrist_{s}'], PRM['G_ARM'])
    TF[f'th_{s}'] = seg_tf(BH[f'upperleg01.{s}'], BH[f'lowerleg01.{s}'], JW[f'hip_{s}'], JW[f'knee_{s}'], PRM['G_LEG'])
    TF[f'sh_{s}'] = seg_tf(BH[f'lowerleg01.{s}'], BH[f'foot.{s}'], JW[f'knee_{s}'], JW[f'ankle_{s}'], PRM['G_LEG'])
def side(n): return 'L' if n.endswith('.L') or n.endswith('_L') else 'R' if n.endswith('.R') or n.endswith('_R') else None
def seg_of(n):   # xương MPFB → [(đoạn uốn, hệ số)]
    s = side(n)
    if n.startswith('shoulder01'): return [('torso', 0.5), (f'ua_{s}', 0.5)]
    if n.startswith('upperarm'): return [(f'ua_{s}', 1)]
    if n.startswith(('lowerarm', 'wrist', 'finger', 'metacarpal')): return [(f'fa_{s}', 1)]
    if n.startswith('upperleg'): return [(f'th_{s}', 1)]
    if n.startswith(('lowerleg', 'foot', 'toe')): return [(f'sh_{s}', 1)]
    return [('torso', 1)]
def joint_of(n):   # xương MPFB → [(khớp cast3d, hệ số)]
    s = side(n)
    if n in ('root',) or n.startswith('pelvis'): return [('pelvis', 1)]
    if n == 'spine05': return [('pelvis', 0.6), ('spine', 0.4)]
    if n == 'spine04': return [('pelvis', 0.2), ('spine', 0.8)]
    if n.startswith(('spine', 'breast', 'clavicle')): return [('spine', 1)]
    if n.startswith('shoulder01'): return [('spine', 0.35), (f'shoulder_{s}', 0.65)]
    if n.startswith('upperarm'): return [(f'shoulder_{s}', 1)]
    if n.startswith('lowerarm'): return [(f'elbow_{s}', 1)]
    if n.startswith(('wrist', 'finger', 'metacarpal')): return [(f'wrist_{s}', 1)]
    if n.startswith('neck'): return [('neck', 1)]
    if n.startswith('upperleg'): return [(f'hip_{s}', 1)]
    if n.startswith('lowerleg'): return [(f'knee_{s}', 1)]
    if n.startswith(('foot', 'toe')): return [(f'ankle_{s}', 1)]
    return [('head', 1)]
SEGS = list(TF); SW_ = np.zeros((len(BONES), len(SEGS))); JWm = np.zeros((len(BONES), len(JN)))
for i, n in enumerate(BONES):
    for sg, k in seg_of(n): SW_[i, SEGS.index(sg)] += k
    for j, k in joint_of(n): JWm[i, JI[j]] += k
WS = WM @ SW_; WJ = WM @ JWm
V = np.zeros_like(P0)
for k, sg in enumerate(SEGS):
    sel = WS[:, k] > 1e-5
    if sel.any(): V[sel] += WS[sel, k][:, None] * TF[sg](P0[sel])
V /= np.maximum(1e-9, WS.sum(1))[:, None]
log('uốn xong; khe vai', round(GAP_SH, 4), 'SX SY SZ', round(SX, 3), round(SY, 3), SZ)

# ---------------- 4. vỏ áo len / quần / da ống chân ----------------
F = np.array([f for f in FACES if len(f) == 4]); F3 = [f for f in FACES if len(f) == 3]
def vnormals(Vx, Fq):
    n = np.zeros_like(Vx)
    for a, b, c in ((0, 1, 2), (0, 2, 3)):
        fn = np.cross(Vx[Fq[:, b]] - Vx[Fq[:, a]], Vx[Fq[:, c]] - Vx[Fq[:, a]])
        for k in (a, b, c): np.add.at(n, Fq[:, k], fn)
    return n / np.maximum(1e-12, np.linalg.norm(n, axis=1))[:, None]
NB = vnormals(V, F)
dom = np.argmax(WJ, 1); dn = np.array(JN)[dom]
cen = (np.abs(V[:, 0]) < 0.006) & (V[:, 1] > 0.3) & np.isin(dn, ['pelvis', 'spine']); crotchY = float(V[cen, 1].min())   # đáy đũng: điểm thấp nhất đường giữa thuộc chậu (đùi trong chạm nhau thuộc hông, không tính)
hemY = max((SHEET['costume']['sweater']['hem_height_H'] - PRM['HEM_DROP']) * H, crotchY + 0.02)   # W4T lượt 2: gấu áo hạ, phủ qua cạp quần
log('đáy đũng y', round(crotchY, 4), '→ gấu áo y', round(hemY, 4), f"({hemY / H:.3f} H; sheet {SHEET['costume']['sweater']['hem_height_H']} H)")
trHemY = (0.10 + SHEET['costume']['trousers']['hem_above_ankle_H']) * H
neckY = JW['neck'][1]
def along(s, Vx, j0, j1):   # tham số dọc đoạn (m) từ khớp j0 về phía j1
    d = JW[j1] - JW[j0]; return (Vx - JW[j0]) @ (d / np.linalg.norm(d))
arm = np.isin(dn, ['shoulder_L', 'elbow_L', 'wrist_L', 'shoulder_R', 'elbow_R', 'wrist_R'])
legs = np.isin(dn, ['hip_L', 'knee_L', 'ankle_L', 'hip_R', 'knee_R', 'ankle_R'])
cut_w = np.zeros(BODY_N, bool)
for s in 'LR':
    t = along(s, V, f'elbow_{s}', f'wrist_{s}'); m = np.isin(dn, [f'elbow_{s}', f'wrist_{s}'])
    cut_w |= m & (t > fa * H - 0.004)
sw_v = (V[:, 1] >= hemY) & (V[:, 1] <= neckY + 0.012) & ~np.isin(dn, ['head', 'neck']) & ~cut_w
sw_v |= np.isin(dn, ['neck']) & (V[:, 1] <= neckY + 0.012) & ~cut_w
tr_v = (V[:, 1] <= hemY + 0.05) & (V[:, 1] >= trHemY) & (legs | np.isin(dn, ['pelvis', 'spine']))
sk_v = legs & (V[:, 1] <= trHemY + 0.03) & np.isin(dn, ['knee_L', 'knee_R', 'ankle_L', 'ankle_R']) & (V[:, 1] >= JW['ankle_L'][1] - 0.01)

def sub(sel):
    fk = F[np.all(sel[F], 1)]; idx = np.unique(fk); rm = -np.ones(BODY_N, int); rm[idx] = np.arange(len(idx)); return idx, rm[fk]
def adjacency(n, Fq):
    e = np.concatenate([Fq[:, [0, 1]], Fq[:, [1, 2]], Fq[:, [2, 3]], Fq[:, [3, 0]]]); e = np.concatenate([e, e[:, ::-1]])
    return e
def boundary(n, Fq):
    e = np.sort(np.concatenate([Fq[:, [0, 1]], Fq[:, [1, 2]], Fq[:, [2, 3]], Fq[:, [3, 0]]]), 1)
    u, c = np.unique(e, axis=0, return_counts=True); b = np.zeros(n, bool); b[u[c == 1].ravel()] = True; return b
def smooth(Vx, Fq, it, lam=0.5, mu=-0.53, fix=None):
    e = adjacency(len(Vx), Fq); deg = np.bincount(e[:, 0], minlength=len(Vx)).astype(float)
    for k in range(int(it)):
        for f in (lam, mu):
            s = np.zeros_like(Vx); np.add.at(s, e[:, 0], Vx[e[:, 1]]); L = s / np.maximum(1, deg)[:, None] - Vx
            if fix is not None: L[fix] = 0
            Vx = Vx + f * L
    return Vx

def edge_proj(Vs, W, bd):
    # mép vải: gấu áo phẳng ở hemY, ống tay cắt vuông ở cổ tay, gấu quần ở trHemY, cổ áo ở neckY (không răng cưa theo mặt lưới)
    out = Vs.copy()
    for v in np.nonzero(bd)[0]:
        y = Vs[v, 1]; j = JN[int(np.argmax(W[v]))]
        if j.startswith(('elbow', 'wrist')):
            s = j[-1]; d = JW[f'wrist_{s}'] - JW[f'elbow_{s}']; d /= np.linalg.norm(d); t = (Vs[v] - JW[f'elbow_{s}']) @ d
            if t > fa * H - 0.04: out[v] += d * (fa * H - 0.002 - t)
        elif abs(y - hemY) < 0.05 and j in ('pelvis', 'spine', 'hip_L', 'hip_R'): out[v, 1] = hemY
        elif abs(y - trHemY) < 0.035: out[v, 1] = trHemY
        elif abs(y - (neckY + 0.012)) < 0.03: out[v, 1] = min(y, neckY + 0.012)
    return out
def shell(sel, thick_fn, fold_fn, it, Wm=None, shape_fn=None, post_fn=None):
    idx, fq = sub(sel); Vs = V[idx].copy(); Ns = NB[idx]; W = (WJ if Wm is None else Wm)[idx]
    Vs = Vs + Ns * thick_fn(Vs, W)[:, None]
    bd = boundary(len(Vs), fq)
    Vs = edge_proj(Vs, W, bd)
    if shape_fn is not None: Vs = shape_fn(Vs, W, fq, bd)
    Vs = smooth(Vs, fq, it, fix=bd)                                   # bỏ chi tiết cơ thể (vải phủ qua); mép giữ nguyên (không co)
    Ns = vnormals(Vs, fq); fd = fold_fn(Vs, W); fd[bd] *= 0.3; Vs = Vs + Ns * fd[:, None]
    if post_fn is not None: Vs = post_fn(Vs, W, fq, bd)                # sau nếp: vải căng bắc cầu (không để làm mượt/nếp tạo rãnh ở đường giữa)
    return dict(idx=idx, F=fq, V=Vs, W=W, fold=fd, bd=bd)

rng = np.random.default_rng(7)
def sw_thick(Vs, W):
    y = (Vs[:, 1] - JW['pelvis'][1]) / H                              # hệ H từ khớp hông
    t = PRM['SW'] + PRM['SW_BELLY'] * sstep(1.0, 0.25, y) * sstep(-0.1, 0.25, y)   # chùng dần xuống bụng (len rủ), gấu ôm lại
    yh = (Vs[:, 1] - hemY) / H
    t = t + PRM['HEM_FLARE'] * sstep(0.35, 0.0, yh)                   # W4T lượt 2: gấu buông, loe nhẹ (bỏ bo gấu ôm hông của lượt 1)
    armw = W[:, [JI[k] for k in ('shoulder_L', 'elbow_L', 'wrist_L', 'shoulder_R', 'elbow_R', 'wrist_R')]].sum(1)
    return t * (1 - armw) + PRM['SL'] * armw
def sw_fold(Vs, W):
    f = np.zeros(len(Vs)); y = (Vs[:, 1] - JW['pelvis'][1]) / H; ph = np.arctan2(Vs[:, 0], Vs[:, 2])
    tor = W[:, [JI['spine'], JI['pelvis']]].sum(1)
    ctr = 1 - 0.85 * (gauss(np.abs(ph) - np.pi, 0.45) + gauss(ph, 0.45))   # W4T lượt 2: không đặt rãnh nếp ở giữa lưng/giữa ngực (lượt 1: rãnh giữa lưng dưới đọc thành khe mông)
    f += tor * 0.0035 * ctr * np.sin(ph * 7 + 1.3 * np.sin(y * 5)) * sstep(0.9, 0.2, y) * sstep(-0.05, 0.15, y)   # rủ dọc nhẹ trên gấu
    f += tor * 0.0025 * np.sin(y * 34 + 2 * np.sin(ph * 3)) * sstep(0.55, 0.15, y)                          # chùng ngang trên bo gấu
    for s in 'LR':
        e = JW[f'elbow_{s}']; d = np.linalg.norm(Vs - e, axis=1)
        a = W[:, [JI[f'shoulder_{s}'], JI[f'elbow_{s}'], JI[f'wrist_{s}']]].sum(1)
        tU = along(s, Vs, f'shoulder_{s}', f'elbow_{s}'); tF = along(s, Vs, f'elbow_{s}', f'wrist_{s}')
        f += a * 0.004 * np.sin(tU * 95 + np.sin(ph * 2) * 2) * gauss(d, 0.06)                            # nếp nén quanh khuỷu
        f += a * 0.003 * np.sin(tF * 120 + ph) * sstep(fa * H - 0.07, fa * H, tF)                          # len chùng ở cổ tay
        f += a * 0.002 * np.sin(ph * 3 + tU * 30) * sstep(0.02, 0.12, tU) * sstep(ua * H, ua * H - 0.08, tU)   # nếp xoắn dọc tay áo (nhẹ)
    return f
for s_ in 'LR':   # tay áo là vải: không xoắn theo cổ tay → trọng số wrist dồn về khuỷu (măng sét gắn khuỷu ở cast3d)
    WJ[sw_v, JI[f'elbow_{s_}']] += WJ[sw_v, JI[f'wrist_{s_}']]; WJ[sw_v, JI[f'wrist_{s_}']] = 0
WS_ = WJ.copy()   # áo: gấu treo theo chậu (hông → chậu HIP2PELVIS), không kéo theo đùi — không đổi trọng số của quần
for s_ in 'LR':
    mv = WS_[sw_v, JI[f'hip_{s_}']] * PRM['HIP2PELVIS']; WS_[sw_v, JI['pelvis']] += mv; WS_[sw_v, JI[f'hip_{s_}']] -= mv
BR_N = [0, 0.0]
def bridge(Vs, sel, sgn, step=0.008):
    # vải căng BẮC CẦU qua chỗ lõm giữa hai khối (khe mông sau lưng, rãnh giữa hai cơ ngực): mỗi lát ngang, nối hai đỉnh nhô nhất
    # (mỗi bên x) bằng đường thẳng; đỉnh nằm giữa mà lõm hơn đường nối thì đẩy ra tới đường nối. sgn = −1: phía sau (z âm), +1: phía trước.
    out = Vs.copy(); ys = Vs[sel, 1]
    if not sel.any(): return out
    for y0 in np.arange(ys.min(), ys.max() + step, step):
        m = sel & (np.abs(Vs[:, 1] - y0) < step * 0.75)
        L = m & (Vs[:, 0] > 0.01); R = m & (Vs[:, 0] < -0.01)
        if L.sum() < 3 or R.sum() < 3: continue
        iL = np.nonzero(L)[0][np.argmax(sgn * Vs[L, 2])]; iR = np.nonzero(R)[0][np.argmax(sgn * Vs[R, 2])]
        xL, zL, xR, zR = Vs[iL, 0], Vs[iL, 2], Vs[iR, 0], Vs[iR, 2]
        mid = m & (Vs[:, 0] < xL) & (Vs[:, 0] > xR)
        zl = zR + (Vs[mid, 0] - xR) / max(1e-6, xL - xR) * (zL - zR)
        idx = np.nonzero(mid)[0]; push = sgn * (zl - Vs[idx, 2]) > 0
        out[idx[push], 2] = zl[push]; BR_N[0] += int(push.sum()); BR_N[1] = max(BR_N[1], float((sgn * (zl - Vs[idx, 2]))[push].max()) if push.any() else 0)
    return out
def sw_shape(Vs, W, fq, bd):
    # W4T lượt 2: ngực/lưng trên — len phủ qua, không in cơ ngực: làm mượt thêm vùng ngực–bả vai (giữ nách, vai, tay áo)
    armw = W[:, [JI[k] for k in ('shoulder_L', 'elbow_L', 'wrist_L', 'shoulder_R', 'elbow_R', 'wrist_R')]].sum(1)
    reg = (Vs[:, 1] > JW['spine'][1] + 0.08) & (Vs[:, 1] < JW['shoulder_L'][1] - 0.01) & (armw < 0.2) & (np.abs(Vs[:, 0]) < shX * H * 0.85)
    Vs = smooth(Vs, fq, PRM['CHEST_SMOOTH'], fix=bd | ~reg)
    # gấu áo buông qua hông/mông: không in khe mông, không ôm mông — làm mượt mạnh vùng dưới eo (giữ mép gấu)
    reg2 = (Vs[:, 1] < JW['pelvis'][1] + 0.09) & (armw < 0.2)
    Vs = bridge(Vs, reg2 & (Vs[:, 2] < 0.0), -1.0)                                           # khe mông
    Vs = bridge(Vs, reg & (Vs[:, 2] > 0.0), 1.0)                                             # rãnh giữa ngực
    return smooth(Vs, fq, PRM['SEAT_SMOOTH'], fix=bd | ~reg2)
def sw_post(Vs, W, fq, bd):
    # Làm mượt nhiều vòng (umbrella) trên lưới MPFB mật độ không đều làm đỉnh trượt tiếp tuyến → rãnh 1 cm ở giữa lưng dưới/xương cùng
    # (đọc thành khe mông/ rãnh sống lưng). Bắc cầu lại SAU khi làm mượt: cả lưng (dưới vai) và rãnh giữa ngực; rồi mượt nhẹ vùng đó.
    armw = W[:, [JI[k] for k in ('shoulder_L', 'elbow_L', 'wrist_L', 'shoulder_R', 'elbow_R', 'wrist_R')]].sum(1)
    body = (armw < 0.2) & (Vs[:, 1] < JW['shoulder_L'][1] - 0.02) & (np.abs(Vs[:, 0]) < shX * H * 0.85)
    Vs = bridge(Vs, body & (Vs[:, 2] < 0.0), -1.0, step=0.006)
    Vs = bridge(Vs, body & (Vs[:, 2] > 0.0) & (Vs[:, 1] > JW['spine'][1] + 0.08), 1.0, step=0.006)
    return smooth(Vs, fq, 12, fix=bd | ~body)
sw = shell(sw_v, sw_thick, sw_fold, PRM['SMOOTH'], Wm=WS_, shape_fn=sw_shape, post_fn=sw_post)
log('bắc cầu: đỉnh đẩy', BR_N[0], 'đẩy max (m)', round(BR_N[1], 4))
def tr_shape(Vs, W, fq, bd):
    # W4T lượt 2: ỐNG QUẦN THẲNG, RỘNG — mỗi ống: bán kính (elip, sâu TR_RZ) tối thiểu TR_R quanh trục chân (x = ±hipX·H, z = 0 ở tư thế bind);
    # vải không bám bắp chân/đầu gối. Trên đáy đũng giữ dáng mông/hông. Rồi làm mượt riêng vùng đũng (không lộ hình háng).
    out = Vs.copy(); sx = np.where(Vs[:, 0] >= 0, 1.0, -1.0); ax = sx * hipX * H
    dx = Vs[:, 0] - ax; dz = Vs[:, 2]; r = np.hypot(dx, dz / PRM['TR_RZ']); ph = np.arctan2(dz / PRM['TR_RZ'], dx)
    k = sstep(crotchY + 0.035, crotchY - 0.02, Vs[:, 1])                  # 0 trên đũng → 1 dưới đũng
    rn = np.maximum(r, PRM['TR_R'])
    rn = r + k * (rn - r)
    out[:, 0] = ax + rn * np.cos(ph); out[:, 2] = rn * np.sin(ph) * PRM['TR_RZ']
    reg = (np.abs(Vs[:, 0]) < hipX * H * 1.1) & (Vs[:, 1] > crotchY - 0.05) & (Vs[:, 1] < crotchY + 0.07)
    fixm = bd | ~reg
    out = smooth(out, fq, PRM['CROTCH_SMOOTH'], fix=fixm)
    return out
def tr_fold(Vs, W):
    kn = JW['knee_L'][1]; ph = np.arctan2(Vs[:, 2], Vs[:, 0] - np.sign(Vs[:, 0]) * hipX * H)
    f = 0.003 * np.sin(Vs[:, 1] * 120 + 2 * ph) * sstep(kn + 0.08, kn - 0.02, Vs[:, 1]) * sstep(kn - 0.12, kn - 0.02, Vs[:, 1])   # nếp gối
    f += 0.0022 * np.sin(ph * 5 + 3 * Vs[:, 1]) * sstep(crotchY - 0.02, kn, Vs[:, 1])                                               # rủ dọc ống
    f += 0.003 * np.sin((Vs[:, 1] - trHemY) * 160 + ph) * sstep(trHemY + 0.07, trHemY + 0.01, Vs[:, 1])                          # nếp chùng trên gấu
    return f
tr = shell(tr_v, lambda Vs, W: np.full(len(Vs), PRM['TR']), tr_fold, PRM['TR_SMOOTH'], shape_fn=tr_shape)
sk_idx, sk_F = sub(sk_v); sk = dict(idx=sk_idx, F=sk_F, V=V[sk_idx], W=WJ[sk_idx], fold=np.zeros(len(sk_idx)), bd=boundary(len(sk_idx), sk_F))
log('vỏ: áo', len(sw['V']), 'quần', len(tr['V']), 'da ống chân', len(sk['V']))

# ---------------- 5. chia 1 cấp trong Blender (nội suy trọng số), tam giác hoá, xuất ----------------
def subdivide(D, name):
    mesh = bpy.data.meshes.new(name); mesh.from_pydata(D['V'].tolist(), [], D['F'].tolist()); mesh.update()
    o = bpy.data.objects.new(name, mesh); bpy.context.scene.collection.objects.link(o)
    for j, n in enumerate(JN):
        vs = np.nonzero(D['W'][:, j] > 1e-4)[0]
        if len(vs) == 0: continue
        g = o.vertex_groups.new(name=n)
        for v in vs: g.add([int(v)], float(D['W'][v, j]), 'REPLACE')
    fg = o.vertex_groups.new(name='_fold')
    for v in range(len(D['V'])): fg.add([v], float(np.clip(0.5 + D['fold'][v] / 0.02, 0, 1)), 'REPLACE')
    md = o.modifiers.new('sub', 'SUBSURF'); md.levels = 1; md.render_levels = 1; md.boundary_smooth = 'PRESERVE_CORNERS'
    tri = o.modifiers.new('tri', 'TRIANGULATE')
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    bpy.ops.object.modifier_apply(modifier='sub'); bpy.ops.object.modifier_apply(modifier='tri')
    m = o.data; n = len(m.vertices); Vx = np.zeros(n * 3); m.vertices.foreach_get('co', Vx); Vx = Vx.reshape(-1, 3)
    idx = np.zeros(len(m.polygons) * 3, np.int64); m.polygons.foreach_get('vertices', idx)
    gn = {g.index: g.name for g in o.vertex_groups}; Wx = np.zeros((n, len(JN)), np.float32); fold = np.zeros(n, np.float32)
    for v in m.vertices:
        for g in v.groups:
            nm = gn[g.group]
            if nm == '_fold': fold[v.index] = (g.weight - 0.5) * 0.02
            else: Wx[v.index, JI[nm]] = g.weight
    Wx /= np.maximum(1e-9, Wx.sum(1, keepdims=True))
    return Vx, idx.reshape(-1, 3), Wx, fold
def b64(a, dt): return base64.b64encode(np.ascontiguousarray(a, dtype=dt).tobytes()).decode()
def tri_normals(Vx, T):
    n = np.zeros_like(Vx); fn = np.cross(Vx[T[:, 1]] - Vx[T[:, 0]], Vx[T[:, 2]] - Vx[T[:, 0]])
    for k in range(3): np.add.at(n, T[:, k], fn)
    return n / np.maximum(1e-12, np.linalg.norm(n, axis=1))[:, None]
PARTOF = {'sweater': {'pelvis': 'torso', 'spine': 'torso', 'hip': 'torso', 'neck': 'torso', 'head': 'torso', 'shoulder': 'upper_arm', 'elbow': 'forearm', 'wrist': 'forearm'},
          'trousers': {'pelvis': 'trouser_seat', 'spine': 'trouser_seat', 'hip': 'thigh', 'knee': 'shin_trouser', 'ankle': 'shin_trouser'},
          'skin': {'knee': 'shin', 'ankle': 'shin', 'hip': 'shin'}}
cuff = {}
for s in 'LR':
    d = JW[f'wrist_{s}'] - JW[f'elbow_{s}']; d /= np.linalg.norm(d); bdv = np.nonzero(sw['bd'])[0]
    t = (sw['V'][bdv] - JW[f'elbow_{s}']) @ d; m = (t > fa * H - 0.01) & ((sw['V'][bdv, 0] > 0) == (s == 'L'))
    q = sw['V'][bdv][m] - JW[f'elbow_{s}'] - t[m][:, None] * d; r = np.linalg.norm(q, axis=1)
    # hệ khớp khuỷu ở BIND: trục −y của khớp = d; bán kính trung bình + tâm lệch (m)
    cuff[s] = {'r': float(r.mean()), 'rmax': float(r.max())}
log('miệng tay áo', cuff)
out = {'version': 'w4t-2', 'H': H, 'joints': JN, 'bind': BIND, 'prm': PRM, 'arm': ARM, 'meta': {'cuff': cuff, 'hemY': hemY, 'crotchY': crotchY}, 'meshes': []}
for role, D in (('sweater', sw), ('trousers', tr), ('skin', sk)):
    Vx, T, Wx, fold = subdivide(D, role)
    if role == 'sweater':   # bắc cầu lần cuối trên lưới đã chia (Catmull-Clark lưới thô lại tạo rãnh ~5 mm ở xương cùng)
        aw = Wx[:, [JI[k] for k in ('shoulder_L', 'elbow_L', 'wrist_L', 'shoulder_R', 'elbow_R', 'wrist_R')]].sum(1)
        bm = (aw < 0.2) & (Vx[:, 1] < JW['shoulder_L'][1] - 0.02) & (np.abs(Vx[:, 0]) < shX * H * 0.85)
        Vx = bridge(Vx, bm & (Vx[:, 2] < 0.0), -1.0, step=0.004)
        # còn rãnh hẹp (≤ 1 cm) đúng đường giữa: lấp cục bộ — mỗi đỉnh dải |x| < 2 cm lấy z sau nhất trong bán kính 6 mm (mặt phẳng x–y)
        cz = np.nonzero(bm & (Vx[:, 2] < -0.03) & (np.abs(Vx[:, 0]) < 0.02))[0]; nb = np.nonzero(bm & (Vx[:, 2] < -0.03) & (np.abs(Vx[:, 0]) < 0.03))[0]
        zc = Vx[cz, 2].copy()
        for k, v in enumerate(cz):
            d = np.hypot(Vx[nb, 0] - Vx[v, 0], Vx[nb, 1] - Vx[v, 1]); zc[k] = min(zc[k], Vx[nb[d < 0.006], 2].min())
        log('lấp rãnh giữa lưng: đỉnh', int((zc < Vx[cz, 2] - 1e-5).sum()), 'sâu nhất (mm)', round(float(1000 * (Vx[cz, 2] - zc).max()), 1))
        Vx[cz, 2] = zc
        # NGỰC: len phủ trơn, không in cơ ngực/núm — khớp MỘT mặt đa thức trơn z(x, y) (bậc 4 theo x, 3 theo y; bình phương tối thiểu)
        # cho mặt trước vùng ngực, thay z bằng mặt khớp với trọng số giảm dần ra mép vùng (không tạo bậc).
        y_lo, y_hi, xw = JW['spine'][1] + 0.06, JW['shoulder_L'][1] - 0.005, shX * H * 0.75
        fr = np.nonzero(bm & (Vx[:, 2] > 0.02) & (Vx[:, 1] > y_lo - 0.04) & (Vx[:, 1] < y_hi + 0.02) & (np.abs(Vx[:, 0]) < xw + 0.02))[0]
        xs_, ys_ = Vx[fr, 0] / 0.1, (Vx[fr, 1] - (y_lo + y_hi) / 2) / 0.1
        A = np.stack([xs_ ** i * ys_ ** j for i in range(5) for j in range(4)], 1); cf = np.linalg.lstsq(A, Vx[fr, 2], rcond=None)[0]
        wt = sstep(xw + 0.01, xw - 0.03, np.abs(Vx[fr, 0])) * sstep(y_lo - 0.03, y_lo, Vx[fr, 1]) * sstep(y_hi + 0.01, y_hi - 0.02, Vx[fr, 1])
        dz = wt * (A @ cf - Vx[fr, 2]); log('ngực trơn: đỉnh', len(fr), 'đổi max (mm)', round(float(1000 * np.abs(dz).max()), 1))
        Vx[fr, 2] += dz
    Nx = tri_normals(Vx, T)
    # AO thủ tục: thung lũng nếp tối (fold âm), khe dưới nách, gấu
    ao = 1 - 9 * np.clip(-fold, 0, None)
    if role == 'sweater':
        for s in 'LR':
            ax = JW[f'shoulder_{s}'] - np.array([0, 0.06, 0]); ao -= 0.25 * gauss(np.linalg.norm(Vx - ax, axis=1), 0.035) * (np.sign(Vx[:, 0]) == (1 if s == 'L' else -1))
    col = np.clip(np.stack([ao, ao, ao * 0.96 + 0.04], 1), 0.35, 1.05)
    # tách theo bộ phận C3 (mỗi tam giác theo khớp trội trung bình) — pháp tuyến dùng chung nên không lộ đường nối
    fj = np.argmax(Wx[T].mean(1), 1); fam = np.array([JN[j].split('_')[0] for j in fj])
    pmap = PARTOF[role]; fpart = np.array([pmap.get(a, role) for a in fam])
    # mỗi bên một lưới (mặt nạ C3 chọn bộ phận theo bên L/R bằng tâm hộp bao của lưới)
    fside = np.where(Vx[T].mean(1)[:, 0] >= 0, 'L', 'R'); fkey = np.array([p_ if p_ in ('torso', 'trouser_seat') else p_ + '|' + s_ for p_, s_ in zip(fpart, fside)])
    for key in np.unique(fkey):
        part = key.split('|')[0]; Tp = T[fkey == key]; iv = np.unique(Tp); rm = -np.ones(len(Vx), int); rm[iv] = np.arange(len(iv)); Tl = rm[Tp]
        Vp, Np, Cp, Wp = Vx[iv], Nx[iv], col[iv], Wx[iv]
        # UV (m × UVK): thân/quần/da — quanh trục dọc (đường nối sau lưng/ trong đùi); tay áo — quanh trục tay (đường nối mặt dưới)
        UVK = 14.0
        if part in ('upper_arm', 'forearm'):
            s = np.where(Vp[:, 0] >= 0, 'L', 'R'); U = np.zeros(len(Vp)); Vv = np.zeros(len(Vp)); per = np.zeros(len(Vp))
            for sd in 'LR':
                m = s == sd; j0, j1 = (f'shoulder_{sd}', f'elbow_{sd}') if part == 'upper_arm' else (f'elbow_{sd}', f'wrist_{sd}')
                ax = (JW[j1] - JW[j0]) / np.linalg.norm(JW[j1] - JW[j0]); ref = np.cross(ax, [0, 0, 1.0]); ref /= np.linalg.norm(ref); ref2 = np.cross(ax, ref)
                w = Vp[m] - JW[j0]; t = w @ ax; q = w - t[:, None] * ax; r = np.linalg.norm(q, axis=1).mean()
                U[m] = np.arctan2(q @ ref2, q @ ref) * r * UVK; Vv[m] = t * UVK; per[m] = 2 * np.pi * r * UVK
        else:
            cx = np.where(np.abs(Vp[:, 0]) > 0.03, np.sign(Vp[:, 0]) * hipX * H, 0) if role != 'sweater' else np.zeros(len(Vp))
            r = np.maximum(0.03, np.hypot(Vp[:, 0] - cx, Vp[:, 2]).mean()); ph = np.arctan2(Vp[:, 0] - cx, Vp[:, 2])
            U = ph * r * UVK; Vv = Vp[:, 1] * UVK; per = np.full(len(Vp), 2 * np.pi * r * UVK)
        UV = np.stack([U, Vv], 1)
        # tam giác vắt qua đường nối: nhân đôi đỉnh phía thấp với u + chu kỳ (không kéo giãn texture)
        bad = np.nonzero(UV[Tl, 0].max(1) - UV[Tl, 0].min(1) > per[Tl].max(1) / 2)[0]
        add = {}; extra = []
        for f in bad:
            for k in range(3):
                v = Tl[f, k]
                if UV[v, 0] < 0:
                    if v not in add: add[v] = len(iv) + len(extra); extra.append(v)
                    Tl[f, k] = add[v]
        if extra:
            ex = np.array(extra); Vp = np.r_[Vp, Vp[ex]]; Np = np.r_[Np, Np[ex]]; Cp = np.r_[Cp, Cp[ex]]; Wp = np.r_[Wp, Wp[ex]]
            UV = np.r_[UV, UV[ex] + np.stack([per[ex], np.zeros(len(ex))], 1)]
        top = np.argsort(-Wp, 1)[:, :4]; tw = np.take_along_axis(Wp, top, 1); tw /= np.maximum(1e-9, tw.sum(1, keepdims=True))
        out['meshes'].append({'role': role, 'part': str(part), 'n': int(len(Vp)), 'pos': b64(Vp, np.float32), 'nrm': b64(Np, np.float32), 'uv': b64(UV, np.float32),
                              'col': b64(Cp, np.float32), 'idx': b64(Tl, np.uint32), 'wj': b64(top, np.uint8), 'ww': b64(tw, np.float32)})
        log(role, part, len(Vp), 'đỉnh', len(Tl), 'tam giác;', len(extra), 'đỉnh nhân đôi ở đường nối UV')
json.dump(out, open(os.path.join(OUT, 'cas_body_bl.json'), 'w'))
log('ghi', os.path.join(OUT, 'cas_body_bl.json'), round(os.path.getsize(os.path.join(OUT, 'cas_body_bl.json')) / 1e6, 2), 'MB')
