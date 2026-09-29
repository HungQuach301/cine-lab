# Cine Lab · Cổng 6 (W4, gói nhân vật) — BÀN TAY MPFB2 cho Ida và Cas (tài sản lõi CC0: RIGHTS.md W4-MPFB-A3).
# Chạy:  /opt/bpy/bin/python design/cong3/v2/char3d/blender/build_hands_bl.py -- <repo mpfb2> <thư mục ra>
# Ra:    <ra>/hands_bl.json  (mỗi nhân vật: lưới bàn tay TRÁI + PHẢI đã chia 1 cấp, trọng số 16 xương, dữ liệu xương nghỉ)
# Cách dựng:
#   1. MPFB 2.0.17 chạy không giao diện: người như đầu 'bl' (Ida: nữ 74 tuổi; Cas: nam 10 tuổi) + target tay; khung xương 'default'
#      (rigs/standard/rig.default.json) + trọng số (weights.default.json) — đều CC0.
#   2. Lấy đỉnh có trọng số wrist + finger*-* ≥ 0,5 (thêm một đoạn cổ tay nằm trong măng sét/tay áo), chia Catmull-Clark 1 cấp.
#   3. Đưa về HỆ BÀN TAY của cast3d: gốc = đầu xương wrist; ngón theo −y; ngón cái phía +z; lòng bàn tay −x (trái) / +x (phải).
#      Co giãn đều để cổ tay → đầu ngón giữa = (palm_length + finger_length) × H_m của sheet (cast3d phóng thêm HAND_SCALE như cũ).
#   4. Màu đỉnh (hệ số nhân với màu da): khớp đốt ửng, lòng tay sáng, móng. three.js làm da trên CPU (blender/hands_bl.js).
import sys, os, math, json, time, importlib, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import bpy, addon_utils, mathutils
from sdfnp import sstep, gauss, fbm

argv = sys.argv[sys.argv.index('--') + 1:]
MP, OUT = argv[0], os.path.abspath(argv[1])
os.makedirs(OUT, exist_ok=True)
T0 = time.time()
log = lambda *a: print(f'[tay {time.time() - T0:6.1f}s]', *a, flush=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
ext = bpy.utils.user_resource('EXTENSIONS', path='user_default', create=True)
if not os.path.exists(os.path.join(ext, 'mpfb')): os.symlink(os.path.join(MP, 'src', 'mpfb'), os.path.join(ext, 'mpfb'))
addon_utils.enable('bl_ext.user_default.mpfb', default_set=True, handle_error=None)
HumanService = importlib.import_module('bl_ext.user_default.mpfb.services.humanservice').HumanService
TargetService = importlib.import_module('bl_ext.user_default.mpfb.services.targetservice').TargetService
TG = os.path.join(MP, 'src', 'mpfb', 'data', 'targets')
SHEETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'model-sheet')

BONES = ['wrist'] + [f'finger{f}-{k}' for f in range(1, 6) for k in range(1, 4)]
CHARS = {
    'ida': dict(macro={'gender': 0.0, 'age': 0.5 + (74 - 25) / (90 - 25) * 0.5, 'muscle': 0.35, 'weight': 0.52, 'proportions': 0.5},
                detail={'hands/l-hand-fingers-diameter-decr': 0.25, 'hands/r-hand-fingers-diameter-decr': 0.25}),
    'cas': dict(macro={'gender': 1.0, 'age': 0.1875 * (10 - 1) / (11 - 1), 'muscle': 0.5, 'weight': 0.45, 'proportions': 0.5},
                detail={}),
}

def b64(a, dt): return base64.b64encode(np.ascontiguousarray(a, dtype=dt).tobytes()).decode()

def build(who):
    cfg = CHARS[who]; sheet = json.load(open(os.path.join(SHEETS, who + '.json'))); hp = sheet['parts']['hand']; Hm = sheet['H_m']
    for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
    macro = TargetService.get_default_macro_info_dict(); macro.update(cfg['macro']); macro['race'] = {'asian': 0.15, 'caucasian': 0.7, 'african': 0.15}
    hum = HumanService.create_human(macro_detail_dict=macro, scale=0.1, mask_helpers=False, feet_on_ground=False)
    for k, w in cfg['detail'].items(): TargetService.load_target(hum, os.path.join(TG, k + '.target.gz'), weight=w, name='d_' + k.split('/')[-1])
    rig = HumanService.add_builtin_rig(hum, 'default', import_weights=True)
    bpy.context.view_layer.update()
    # lưới đã trộn shape key, KHÔNG qua armature (tư thế nghỉ)
    for m in list(hum.modifiers): m.show_viewport = False
    dg = bpy.context.evaluated_depsgraph_get(); ev = hum.evaluated_get(dg); me = ev.to_mesh()
    nV = len(me.vertices); P = np.zeros(nV * 3); me.vertices.foreach_get('co', P); P = P.reshape(-1, 3)
    P = (np.array(hum.matrix_world) @ np.c_[P, np.ones(nV)].T).T[:, :3]
    faces = [tuple(p.vertices) for p in me.polygons]
    gname = {g.index: g.name for g in hum.vertex_groups}
    Wt = {}
    for v in hum.data.vertices:
        for g in v.groups:
            n = gname[g.group]
            if g.weight > 1e-4: Wt.setdefault(v.index, {})[n] = g.weight
    ev.to_mesh_clear()
    A = rig.matrix_world
    bone = lambda n: (np.array(A @ rig.data.bones[n].head_local), np.array(A @ rig.data.bones[n].tail_local))
    out = {}
    for s, sx in (('L', 1), ('R', -1)):
        names = [b + '.' + s for b in BONES]
        hand_w = np.array([sum(Wt.get(i, {}).get(n, 0) for n in names) for i in range(nV)])
        w0, _ = bone('wrist.' + s); f3, _ = bone('finger3-1.' + s); f2, _ = bone('finger2-1.' + s); f5, _ = bone('finger5-1.' + s)
        d = f3 - w0; d /= np.linalg.norm(d)
        ez = f2 - f5; ez -= d * (ez @ d); ez /= np.linalg.norm(ez)
        ey = -d; ex = np.cross(ey, ez)
        Rm = np.stack([ex, ey, ez], 1)                                         # cột = trục cục bộ (thế giới MPFB)
        # đoạn cổ tay: đỉnh cẳng tay trong 0,05 m sau khớp cổ tay (nằm trong măng sét) đi cứng theo xương wrist
        along = (P - w0) @ d
        near = (hand_w < 0.5) & (along > -0.05) & (along < 0.01) & (np.linalg.norm((P - w0) - np.outer(along, d), axis=1) < 0.06)
        # W4T (sửa "mảng đen lởm chởm ở cổ tay"): cắt cổ tay bằng MẶT PHẲNG vuông trục cẳng tay (3 cm sau khớp), không theo ngưỡng
        # trọng số (mép răng cưa); rồi BỊT miệng ống bằng nắp da lõm nhẹ → không còn lỗ tối nhìn xuyên vào trong bàn tay
        rad_ = np.linalg.norm((P - w0) - np.outer(along, d), axis=1)
        keep = (along >= -0.03) & (rad_ < 0.07) & (sx * P[:, 0] > 0.15)
        F = [f for f in faces if all(keep[list(f)])]
        used = np.unique(np.array([i for f in F for i in f])); keep[:] = False; keep[used] = True
        idx = np.nonzero(keep)[0]; remap = -np.ones(nV, int); remap[idx] = np.arange(len(idx))
        Fl = [tuple(remap[list(f)]) for f in F]
        eg = {}
        for f in Fl:
            for k in range(len(f)): e = tuple(sorted((f[k], f[(k + 1) % len(f)]))); eg[e] = eg.get(e, 0) + 1
        bde = {}   # cạnh biên có hướng (giữ chiều mặt) → nắp quay đúng pháp tuyến ra ngoài
        for f in Fl:
            for k in range(len(f)):
                a_, b_ = f[k], f[(k + 1) % len(f)]
                if eg[tuple(sorted((a_, b_)))] == 1: bde[a_] = b_
        Pk = P[idx]; ring = [v for v in bde if (Pk[v] - w0) @ d < -0.02]
        if ring:
            cidx = len(Pk); cen = Pk[ring].mean(0) + d * 0.004
            Pk = np.r_[Pk, cen[None]]; Fl += [(bde[v], v, cidx) for v in ring if bde[v] in ring]
            idx = np.r_[idx, -1]
        # đối tượng tạm để chia Catmull-Clark (trọng số nội suy theo)
        mesh = bpy.data.meshes.new('h'); mesh.from_pydata(Pk.tolist(), [], Fl); mesh.update()
        ob = bpy.data.objects.new('h_' + who + s, mesh); bpy.context.scene.collection.objects.link(ob)
        vg = {n: ob.vertex_groups.new(name=n) for n in names}
        for j, i in enumerate(idx):
            ws = {n: Wt.get(int(i), {}).get(n, 0) for n in names} if i >= 0 else {}; t = sum(ws.values())
            if t < 1e-6: ws = {'wrist.' + s: 1.0}; t = 1.0
            for n, w in ws.items():
                if w > 1e-4: vg[n].add([j], w / t, 'REPLACE')
        mod = ob.modifiers.new('sub', 'SUBSURF'); mod.levels = 1; mod.render_levels = 1
        dg = bpy.context.evaluated_depsgraph_get(); oe = ob.evaluated_get(dg); m2 = oe.to_mesh()
        n2 = len(m2.vertices); Q = np.zeros(n2 * 3); m2.vertices.foreach_get('co', Q); Q = Q.reshape(-1, 3)
        tris = []
        m2.calc_loop_triangles()
        T = np.zeros(len(m2.loop_triangles) * 3, int); m2.loop_triangles.foreach_get('vertices', T); T = T.reshape(-1, 3)
        gi = {g.index: g.name for g in ob.vertex_groups}
        Wv = np.zeros((n2, len(BONES)), np.float32)
        for v in m2.vertices:
            for g in v.groups:
                Wv[v.index, names.index(gi[g.group])] = g.weight
        Wv /= np.maximum(1e-6, Wv.sum(1, keepdims=True))
        oe.to_mesh_clear()
        # về hệ bàn tay (m, chưa co giãn)
        L = (Q - w0) @ Rm
        heads = np.array([(bone(n)[0] - w0) @ Rm for n in names]); tails = np.array([(bone(n)[1] - w0) @ Rm for n in names])
        # co giãn: cổ tay → đầu ngón giữa = (palm + finger) × H_m
        tip = L[np.argmax(Wv[:, BONES.index('finger3-3')] * (-L[:, 1]))]
        k = (hp['palm_length'] + hp['finger_length']) * Hm / (-tip[1])
        L *= k; heads *= k; tails *= k
        # hướng tam giác: pháp tuyến ra ngoài
        c = L.mean(0); tri = L[T]; nrm = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
        if np.sum((nrm * (tri.mean(1) - c)).sum(1) > 0) < len(T) / 2: T = T[:, ::-1]
        # màu (hệ số nhân với màu da): lòng tay sáng, mu tay hơi đỏ ở đốt, móng
        dors = L[:, 0] * sx                                                      # > 0: mu tay
        col = np.ones((len(L), 3))
        fin = Wv[:, 1:].sum(1)
        knuck = np.zeros(len(L))
        for f in range(2, 6):
            for kk in (1, 2, 3):
                hj = heads[BONES.index(f'finger{f}-{kk}')]
                knuck += (1.0 if kk == 1 else 0.7) * gauss(np.linalg.norm(L - hj, axis=1), 0.009 if kk == 1 else 0.006) * sstep(0.0, 0.004, dors - hj[0] * sx)
        knuck = np.clip(knuck, 0, 1)
        col[:, 0] += 0.04 * knuck; col[:, 1] -= 0.10 * knuck; col[:, 2] -= 0.08 * knuck
        palm = sstep(0.0, -0.006, dors) * (1 - fin * 0.5)
        col += np.outer(palm, [0.04, 0.02, 0.0])
        nail = np.zeros(len(L))
        for f in range(1, 6):
            bi = BONES.index(f'finger{f}-3'); h3, t3 = heads[bi], tails[bi]; ax_ = t3 - h3; ln = np.linalg.norm(ax_); ax_ /= ln
            u = (L - h3) @ ax_; r = L - h3 - np.outer(u, ax_)
            dorsal_dir = np.array([sx, 0, 0.0]) if f > 1 else np.cross(ax_, np.array([0, 1.0, 0])) * 0 + np.array([sx * 0.7, 0, -0.7])
            dorsal_dir -= ax_ * (dorsal_dir @ ax_); dorsal_dir /= np.linalg.norm(dorsal_dir)
            cosd = (r @ dorsal_dir) / np.maximum(1e-6, np.linalg.norm(r, axis=1))
            nail = np.maximum(nail, Wv[:, bi] * sstep(0.35, 0.6, u / ln) * sstep(0.55, 0.8, cosd))
        nailc = np.array([1.08, 0.97, 0.95]) if who == 'ida' else np.array([1.1, 0.98, 0.97])
        col = col * (1 - nail[:, None]) + nailc * nail[:, None]
        mot = 1 + 0.03 * fbm(L[:, 0] * 90, L[:, 1] * 90, L[:, 2] * 90, 5, 3)
        col *= mot[:, None]
        # bán kính ngón theo xương (cho va chạm lúc nắm)
        rad = []
        for bi, n in enumerate(BONES):
            h, t = heads[bi], tails[bi]; ax_ = t - h; ln = np.linalg.norm(ax_) or 1; ax_ = ax_ / ln
            sel = Wv[:, bi] > 0.6
            if bi == 0 or sel.sum() < 4: rad.append(0.0); continue
            u = (L[sel] - h) @ ax_; r = np.linalg.norm(L[sel] - h - np.outer(u, ax_), axis=1); rad.append(float(np.median(r)))
        pc = heads[[BONES.index(f'finger{f}-1') for f in range(2, 6)]].mean(0) * 0.55   # tâm lòng bàn tay (giữa cổ tay và gốc ngón)
        palmN = np.array([-sx, 0, 0.0])
        out[s] = {'n': int(len(L)), 'pos': b64(L, np.float32), 'idx': b64(T.ravel(), np.uint32), 'col': b64(np.clip(col, 0, 1.5), np.float32),
                  'w': b64(Wv, np.float32), 'bones': BONES, 'heads': np.round(heads, 6).tolist(), 'tails': np.round(tails, 6).tolist(), 'rad': np.round(rad, 5).tolist(),
                  'palm': np.round(pc, 5).tolist(), 'palmN': palmN.tolist(), 'scale_k': float(k)}
        log(f'{who} {s}: {len(L)} đỉnh, {len(T)} tam giác, k {k:.3f}, bán kính ngón giữa {rad[BONES.index("finger3-2")]:.4f} m')
    return out

res = {'_doc': 'Bàn tay MPFB2 (CC0; RIGHTS W4-MPFB-A3). Hệ bàn tay cast3d: gốc = khớp cổ tay, ngón −y, ngón cái +z, lòng −x (L) / +x (R); đơn vị m (trước HAND_SCALE). '
              'pos/col/w: Float32 base64 (w: n × 16 theo "bones"); idx: Uint32 base64. heads/tails: xương nghỉ.',
       'mpfb': {'commit': '3edf9df0551765be43563d047888cf7877eb89b4', 'rig': 'default', 'macro': {k: v['macro'] for k, v in CHARS.items()}, 'detail': {k: v['detail'] for k, v in CHARS.items()}}}
for who in ('ida', 'cas'): res[who] = build(who)
json.dump(res, open(os.path.join(OUT, 'hands_bl.json'), 'w'))
log('xong', os.path.join(OUT, 'hands_bl.json'), os.path.getsize(os.path.join(OUT, 'hands_bl.json')) // 1024, 'KB')
