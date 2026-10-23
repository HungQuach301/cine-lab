"""NC-GPU · CẢNH CYCLES GPU "chất lượng điện ảnh" — dựng từ cảnh B của NC-CPU (design/pt/cpu/nc_blend.py, bản sao + sửa; tệp gốc không đổi) và bản xuất
design/pt/gpu/gpu_export.js (có màu vật liệu, cờ có ảnh lá cờ, khói/lửa k2v ở fx.json). Sửa các lỗi NC-CPU §3:
  (1) nhạt/bão hoà thấp → sương khí quyển theo màu trời, mật độ theo cảnh (--haze, --hazek) + tách ánh trời/khuếch tán; đo lại sau chỉnh màu k2v;
  (2) nền mờ → albedo 0,5 m quanh điểm máy (nc_topo.js, hộp near_box.py) phủ trên 1 m / 4 m + vân CC0 4k theo lớp phủ cls.png gần máy (≤ 700 m);
  (3) mái bằng đen → vật không có màu đỉnh lấy màu vật liệu k2v (rec.mc) thay vì Attribute 'col' rỗng; (4) lều có màu vải (rec.mc);
  (5) khói/lửa ban ngày → mỗi cụm khói/lửa smokeV6 đang hiện = một khối THỂ TÍCH (cầu nhiễu) + lửa phát xạ + đèn điểm.
Thêm thứ GPU làm được: GI toàn khung (nảy 8/6/6, thể tích 2), khói/lửa thể tích, motion blur (khung hoá máy theo đường máy), DOF nhẹ (lấy nét tâm khung),
bụi cây dày gấp k (bản sao lệch ≤ 4 m quanh MỖI bụi có nguồn lớp phủ — không thêm bụi ở chỗ k2v không có), nước phản chiếu thật (Principled, nhám 0,02–0,06 theo gió).
KHÔNG thêm vật không có nguồn: mọi vật từ k2v (V7B/NC-CPU).
  blender -b --factory-startup --python-exit-code 1 -P gpu_blend.py -- <thư mục xuất> cycles <ra> [--topo d1,d2,…] [--tex <vân>] [--spp N] [--res WxH]
      [--gpudev OPTIX|CUDA|CPU] [--fx] [--mb] [--dof] [--bushx k] [--d4k] [--night 0..1] [--fires json] [--smoke] [--anim json --frames a:b] [--persist] [--cls <cls.png>] [--year Y]"""
import sys, os, json, math, time
import numpy as np
import bpy, mathutils

a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
D, JOB, OUT = a[0], a[1], a[2]
opt = {}
i = 3
while i < len(a):
    if a[i].startswith('--'):
        if i + 1 < len(a) and not a[i + 1].startswith('--'): opt[a[i]] = a[i + 1]; i += 2
        else: opt[a[i]] = '1'; i += 1
    else: i += 1
T0 = time.time()
TEX = opt.get('--tex', '/w/tex'); DEV = opt.get('--gpudev', 'OPTIX'); YEAR = float(opt.get('--year', 1782)); TH = int(opt.get('--threads', 4)); NIGHT = float(opt.get('--night', 0))
HAZE_S, HAZE_C = float(opt.get('--haze', 1 / 16000)), tuple(float(x) for x in opt.get('--hazec', '0.66,0.74,0.84').split(',')); HAZE_K = float(opt.get('--hazek', 1.0))
# ánh trời khuếch tán: three.js (V7B) irradiance = hemi·I; Cycles: irradiance mặt phẳng = π·L → L = hemi·I/π khớp k2v (SKYDIF = 1/1,15π ≈ 0,277). NC-CPU dùng 1,0 (trời mạnh ≈ 3,6×)
SKYDIF = float(opt.get('--skydif', 0.277))
M = json.load(open(os.path.join(D, 'manifest.json')))
bpy.ops.wm.read_factory_settings(use_empty=True)
def _gpu_prefs():
    p = bpy.context.preferences.addons['cycles'].preferences
    for t in ([DEV, 'CUDA'] if DEV != 'CPU' else []):
        try:
            p.compute_device_type = t; p.refresh_devices(); n = 0
            for d in p.devices: d.use = d.type == t; n += d.use
            if n: print('NC-GPU-DEV', t, [d.name for d in p.devices if d.use], flush=True); return t
        except Exception as e: print('NC-GPU-DEV lỗi', t, repr(e), flush=True)
    return 'CPU'
_DEV = _gpu_prefs()
if '--needgpu' in sys.argv and _DEV == 'CPU': print('NC-GPU-DEV KHÔNG CÓ GPU — dừng (không dựng âm thầm bằng CPU)', flush=True); sys.exit(9)   # lượt 1: pod 3 sau hết VRAM rơi về CPU, 24 khung × 220 s
sc = bpy.context.scene
S = mathutils.Matrix(((1, 0, 0, 0), (0, 0, -1, 0), (0, 1, 0, 0), (0, 0, 0, 1)))   # three (x E, y cao, z −N) → Blender (x E, y N, z cao)
def load(i):
    meta = M['bufs'][i]; dt = {'Float32Array': np.float32, 'Uint32Array': np.uint32, 'Uint16Array': np.uint16}[meta['type']]
    return np.fromfile(os.path.join(D, f'b{i}.bin'), dtype=dt)
def img(p, color=True):
    im = bpy.data.images.load(p, check_existing=True)
    if not color: im.colorspace_settings.name = 'Non-Color'
    return im

# ---------------------------------------------------------------- nút dùng chung
def N(nt, t, **kw):
    n = nt.nodes.new(t)
    for k, v in kw.items(): setattr(n, k, v)
    return n
def haze_wrap(m, emit_k=1.0):
    """bọc đầu ra vật liệu: mix(bề mặt, phát xạ màu sương, 1 − e^(−σ·d)); d = khoảng cách tới máy (Camera Data). Đêm: màu sương tối theo NIGHT."""
    nt = m.node_tree; out = [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'][0]; src = out.inputs['Surface'].links[0].from_socket
    cd = N(nt, 'ShaderNodeCameraData'); mu = N(nt, 'ShaderNodeMath', operation='MULTIPLY'); mu.inputs[1].default_value = -HAZE_S
    ex = N(nt, 'ShaderNodeMath', operation='EXPONENT'); sub = N(nt, 'ShaderNodeMath', operation='SUBTRACT'); sub.inputs[0].default_value = 1.0
    em = N(nt, 'ShaderNodeEmission'); k = 1 - NIGHT; em.inputs['Color'].default_value = (*[c * k + cn * NIGHT for c, cn in zip(HAZE_C, (0.035, 0.05, 0.09))], 1); em.inputs['Strength'].default_value = SKY_K * emit_k * HAZE_K
    mx = N(nt, 'ShaderNodeMixShader'); L = nt.links; HAZE_EM.append(em)
    L.new(cd.outputs['View Distance'], mu.inputs[0]); L.new(mu.outputs[0], ex.inputs[0]); L.new(ex.outputs[0], sub.inputs[1])
    # NC-GPU: sương CHỈ trên tia máy/tia bóng (phối cảnh khí quyển dọc tia nhìn). NC-CPU áp cho mọi tia → mặt xa phát xạ xám-lam làm nguồn sáng phụ cho tia nảy (một nguyên nhân "nhạt")
    lp = N(nt, 'ShaderNodeLightPath'); cg = N(nt, 'ShaderNodeMath', operation='MAXIMUM'); L.new(lp.outputs['Is Camera Ray'], cg.inputs[0]); L.new(lp.outputs['Is Glossy Ray'], cg.inputs[1])
    fz = N(nt, 'ShaderNodeMath', operation='MULTIPLY'); L.new(sub.outputs[0], fz.inputs[0]); L.new(cg.outputs[0], fz.inputs[1]); L.new(fz.outputs[0], mx.inputs['Fac'])
    L.new(src, mx.inputs[1]); L.new(em.outputs[0], mx.inputs[2]); L.new(mx.outputs[0], out.inputs['Surface'])
def box_tex(nt, path, scale, color=True, blend=0.25):
    tc = N(nt, 'ShaderNodeTexCoord'); mp = N(nt, 'ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1 / scale,) * 3
    t = N(nt, 'ShaderNodeTexImage', projection='BOX', projection_blend=blend); t.image = img(path, color)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], t.inputs['Vector']); return t
def attr(nt, name, kind='GEOMETRY'):
    n = N(nt, 'ShaderNodeAttribute'); n.attribute_name = name; n.attribute_type = kind; return n
def principled(m):
    b = m.node_tree.nodes['Principled BSDF']
    for k in ('Specular IOR Level',):
        if k in b.inputs: b.inputs[k].default_value = 0.2
    return b

TOPO = []   # [(ảnh, hộp E0, N0, E1, N1)] ưu tiên ảnh đầu (mịn)
def topo_image(d):
    T = json.load(open(os.path.join(d, 'topo.json'))); W = int(round((T['box'][2] - T['box'][0]) / T['res'])); H = int(round((T['box'][3] - T['box'][1]) / T['res']))
    cache = os.path.join(d, 'topo_full.png')
    if not os.path.exists(cache):
        import imageio.v3 as iio
        A = np.zeros((H, W, 4), np.uint8)
        for t in T['tiles']:
            p = iio.imread(os.path.join(d, t['file'])); x0 = t['i'] * T['TILE']; y0 = t['j'] * T['TILE']; A[y0:y0 + p.shape[0], x0:x0 + p.shape[1]] = p[:, :, :4] if p.shape[2] == 4 else np.dstack([p, np.full(p.shape[:2], 255, np.uint8)])
        iio.imwrite(cache, A)
    return img(cache), T['box']

def mat_ground():
    m = bpy.data.materials.new('m_dia_hinh'); m.use_nodes = True; nt = m.node_tree; b = principled(m); b.inputs['Roughness'].default_value = 0.95; L = nt.links
    tc = N(nt, 'ShaderNodeTexCoord'); col = None; alpha_prev = None
    for k, (im, bx) in enumerate(TOPO):
        mp = N(nt, 'ShaderNodeMapping'); mp.inputs['Location'].default_value = (-bx[0] / (bx[2] - bx[0]), -bx[1] / (bx[3] - bx[1]), 0); mp.inputs['Scale'].default_value = (1 / (bx[2] - bx[0]), 1 / (bx[3] - bx[1]), 1)
        mp.vector_type = 'TEXTURE'   # (P − E0)/(E1 − E0) theo trục — dùng kiểu POINT với vị trí/thu phóng tách rời
        mp.vector_type = 'POINT'; mp.inputs['Scale'].default_value = (1 / (bx[2] - bx[0]), 1 / (bx[3] - bx[1]), 1); mp.inputs['Location'].default_value = (-bx[0] / (bx[2] - bx[0]), -bx[1] / (bx[3] - bx[1]), 0)
        t = N(nt, 'ShaderNodeTexImage', extension='CLIP', interpolation='Cubic'); t.image = im; L.new(tc.outputs['Object'], mp.inputs['Vector']); L.new(mp.outputs['Vector'], t.inputs['Vector'])
        if col is None: col, alpha_prev = t.outputs['Color'], t.outputs['Alpha']
        else:   # ảnh mịn (trước) phủ lên ảnh thô (sau) theo alpha của ảnh mịn
            mx = N(nt, 'ShaderNodeMix', data_type='RGBA'); L.new(alpha_prev, mx.inputs['Factor']); L.new(t.outputs['Color'], mx.inputs[6]); L.new(col, mx.inputs[7]); col = mx.outputs[2]
            mxa = N(nt, 'ShaderNodeMath', operation='MAXIMUM'); L.new(alpha_prev, mxa.inputs[0]); L.new(t.outputs['Alpha'], mxa.inputs[1]); alpha_prev = mxa.outputs[0]
    if col is None: b.inputs['Base Color'].default_value = (0.32, 0.30, 0.22, 1)
    else:
        L.new(col, b.inputs['Base Color'])
        # gồ ghề vi mô từ độ sáng albedo (cùng nguồn với màu → khớp vân)
        bm = N(nt, 'ShaderNodeBump'); bm.inputs['Strength'].default_value = 0.35; bm.inputs['Distance'].default_value = 0.4; L.new(col, bm.inputs['Height'])
        if '--d4k' in opt: col, nrm = ground_detail(nt, col, tc); L.new(col, b.inputs['Base Color']); L.new(nrm, bm.inputs['Normal'])
        L.new(bm.outputs['Normal'], b.inputs['Normal'])
    m['kind'] = 'dia_hinh'; return m

D4K = [   # nhóm lớp phủ (cls.png, R = tự nhiên, G = đô thị) → vân CC0 4k (Poly Haven), cỡ thật (m) — cùng họ vân với cách A (up.js G_GROUND)
    ('aerial_beach_01', 30.0, (1,)), ('dry_ground_rocks', 4.0, (2, 5, 11)), ('aerial_grass_rock', 15.0, (3, 13)), ('aerial_rocks_02', 50.0, (4,))]
def ground_detail(nt, col, tc):
    """vân 4k CC0 theo lớp phủ, CHỈ gần máy (≤ 150 m đủ, tắt dần tới 700 m): màu × tỉ lệ vân/trung bình (25 % sắc độ như cách A) + pháp tuyến 4k."""
    L = nt.links; means = json.load(open(os.path.join(TEX, 'mean4k.json'))); pk = json.load(open(opt['--packmeta'])); e0, n0, e1, n1 = pk['ext']
    sx = N(nt, 'ShaderNodeSeparateXYZ'); L.new(tc.outputs['Object'], sx.inputs[0])
    cu = N(nt, 'ShaderNodeMath', operation='MULTIPLY_ADD'); cu.inputs[1].default_value = 1 / (e1 - e0); cu.inputs[2].default_value = -e0 / (e1 - e0); L.new(sx.outputs['X'], cu.inputs[0])
    cv = N(nt, 'ShaderNodeMath', operation='MULTIPLY_ADD'); cv.inputs[1].default_value = 1 / (n1 - n0); cv.inputs[2].default_value = -n0 / (n1 - n0); L.new(sx.outputs['Y'], cv.inputs[0])
    cc = N(nt, 'ShaderNodeCombineXYZ'); L.new(cu.outputs[0], cc.inputs['X']); L.new(cv.outputs[0], cc.inputs['Y'])
    ct = N(nt, 'ShaderNodeTexImage', interpolation='Closest', extension='EXTEND'); ct.image = img(opt['--cls'], False); L.new(cc.outputs[0], ct.inputs['Vector'])
    sc_ = N(nt, 'ShaderNodeSeparateColor'); L.new(ct.outputs['Color'], sc_.inputs['Color'])
    cl = N(nt, 'ShaderNodeMath', operation='MULTIPLY'); cl.inputs[1].default_value = 255.0; L.new(sc_.outputs['Green' if YEAR >= 1900 else 'Red'], cl.inputs[0])
    acc_c = None; acc_n = None; acc_w = None
    for tid, size, vals in D4K:
        w = None
        for v in vals:
            cp = N(nt, 'ShaderNodeMath', operation='COMPARE'); cp.inputs[1].default_value = v; cp.inputs[2].default_value = 0.5; L.new(cl.outputs[0], cp.inputs[0])
            if w is None: w = cp.outputs[0]
            else: ad = N(nt, 'ShaderNodeMath', operation='ADD'); L.new(w, ad.inputs[0]); L.new(cp.outputs[0], ad.inputs[1]); w = ad.outputs[0]
        mp = N(nt, 'ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1 / size,) * 3; L.new(tc.outputs['Object'], mp.inputs['Vector'])
        td = N(nt, 'ShaderNodeTexImage'); td.image = img(os.path.join(TEX, f'{tid}_diff_4k.jpg')); L.new(mp.outputs['Vector'], td.inputs['Vector'])
        tn = N(nt, 'ShaderNodeTexImage'); tn.image = img(os.path.join(TEX, f'{tid}_nor_4k.jpg'), False); L.new(mp.outputs['Vector'], tn.inputs['Vector'])
        mu = means[f'{tid}_diff_4k.jpg']; dv = N(nt, 'ShaderNodeVectorMath', operation='DIVIDE'); dv.inputs[1].default_value = tuple(max(0.02, x) for x in mu); L.new(td.outputs['Color'], dv.inputs[0])
        wc = N(nt, 'ShaderNodeVectorMath', operation='SCALE'); L.new(dv.outputs[0], wc.inputs[0]); L.new(w, wc.inputs['Scale'])
        wn = N(nt, 'ShaderNodeVectorMath', operation='SCALE'); L.new(tn.outputs['Color'], wn.inputs[0]); L.new(w, wn.inputs['Scale'])
        if acc_c is None: acc_c, acc_n, acc_w = wc.outputs[0], wn.outputs[0], w
        else:
            a1 = N(nt, 'ShaderNodeVectorMath', operation='ADD'); L.new(acc_c, a1.inputs[0]); L.new(wc.outputs[0], a1.inputs[1]); acc_c = a1.outputs[0]
            a2 = N(nt, 'ShaderNodeVectorMath', operation='ADD'); L.new(acc_n, a2.inputs[0]); L.new(wn.outputs[0], a2.inputs[1]); acc_n = a2.outputs[0]
            a3 = N(nt, 'ShaderNodeMath', operation='ADD'); L.new(acc_w, a3.inputs[0]); L.new(w, a3.inputs[1]); acc_w = a3.outputs[0]
    # phần không thuộc nhóm nào (đô thị, nước): tỉ lệ 1, pháp tuyến phẳng
    rest = N(nt, 'ShaderNodeMath', operation='SUBTRACT'); rest.inputs[0].default_value = 1.0; L.new(acc_w, rest.inputs[1])
    r1 = N(nt, 'ShaderNodeVectorMath', operation='SCALE'); r1.inputs[0].default_value = (1, 1, 1); L.new(rest.outputs[0], r1.inputs['Scale'])
    r2 = N(nt, 'ShaderNodeVectorMath', operation='SCALE'); r2.inputs[0].default_value = (0.5, 0.5, 1.0); L.new(rest.outputs[0], r2.inputs['Scale'])
    tc_ = N(nt, 'ShaderNodeVectorMath', operation='ADD'); L.new(acc_c, tc_.inputs[0]); L.new(r1.outputs[0], tc_.inputs[1])
    tn_ = N(nt, 'ShaderNodeVectorMath', operation='ADD'); L.new(acc_n, tn_.inputs[0]); L.new(r2.outputs[0], tn_.inputs[1])
    lt = N(nt, 'ShaderNodeRGBToBW'); L.new(tc_.outputs[0], lt.inputs[0]); kc = N(nt, 'ShaderNodeMix', data_type='RGBA'); kc.inputs['Factor'].default_value = 0.25
    L.new(lt.outputs[0], kc.inputs[6]); L.new(tc_.outputs[0], kc.inputs[7]); cl2 = N(nt, 'ShaderNodeClamp'); 
    # gần máy: hệ số tắt dần theo khoảng cách nhìn
    cd = N(nt, 'ShaderNodeCameraData'); fd = N(nt, 'ShaderNodeMapRange'); fd.inputs['From Min'].default_value = 150; fd.inputs['From Max'].default_value = 700; fd.inputs['To Min'].default_value = 0.7; fd.inputs['To Max'].default_value = 0.0
    L.new(cd.outputs['View Distance'], fd.inputs['Value'])
    mm = N(nt, 'ShaderNodeMix', data_type='RGBA', blend_type='MULTIPLY'); L.new(fd.outputs['Result'], mm.inputs['Factor']); L.new(col, mm.inputs[6]); L.new(kc.outputs[2], mm.inputs[7])
    nm = N(nt, 'ShaderNodeNormalMap'); L.new(tn_.outputs[0], nm.inputs['Color']); L.new(fd.outputs['Result'], nm.inputs['Strength'])
    return mm.outputs[2], nm.outputs['Normal']

def mat_city():
    """tường: màu đỉnh k2v × vữa CC0; cửa sổ thủ tục (tầng 3 m, gian 3 m, ô 1,1 × 1,5 m) theo toạ độ dọc tường = dot(P.xy, tiếp tuyến), chỉ mặt đứng;
    mái dốc (pháp tuyến z 0,25–0,97): ngói CC0; mái bằng: màu đỉnh."""
    m = bpy.data.materials.new('m_nha'); m.use_nodes = True; nt = m.node_tree; b = principled(m); b.inputs['Roughness'].default_value = 0.88; L = nt.links
    vc = attr(nt, 'col'); geo = N(nt, 'ShaderNodeNewGeometry')
    pl = box_tex(nt, os.path.join(TEX, 'white_plaster_rough_01_diff_1k.jpg'), 1.6); tl = box_tex(nt, os.path.join(TEX, 'clay_roof_tiles_02_diff_1k.jpg'), 2.5)
    # độ sáng vữa (÷ ~0,55) nhân màu đỉnh
    bw = N(nt, 'ShaderNodeRGBToBW'); L.new(pl.outputs['Color'], bw.inputs[0]); kpl = N(nt, 'ShaderNodeMath', operation='MULTIPLY'); kpl.inputs[1].default_value = 1 / 0.55; L.new(bw.outputs[0], kpl.inputs[0])
    mpl = N(nt, 'ShaderNodeMix', data_type='RGBA', blend_type='MULTIPLY'); mpl.inputs['Factor'].default_value = 0.6; L.new(vc.outputs['Color'], mpl.inputs[6]); L.new(kpl.outputs[0], mpl.inputs[7])
    # tiếp tuyến ngang t = (−Ny, Nx); u = P·t ; v = P.z
    sep = N(nt, 'ShaderNodeSeparateXYZ'); L.new(geo.outputs['Normal'], sep.inputs[0]); sp = N(nt, 'ShaderNodeSeparateXYZ'); L.new(geo.outputs['Position'], sp.inputs[0])
    m1 = N(nt, 'ShaderNodeMath', operation='MULTIPLY'); L.new(sp.outputs['X'], m1.inputs[0]); L.new(sep.outputs['Y'], m1.inputs[1])
    m2 = N(nt, 'ShaderNodeMath', operation='MULTIPLY'); L.new(sp.outputs['Y'], m2.inputs[0]); L.new(sep.outputs['X'], m2.inputs[1])
    u = N(nt, 'ShaderNodeMath', operation='SUBTRACT'); L.new(m2.outputs[0], u.inputs[0]); L.new(m1.outputs[0], u.inputs[1])
    def frac_band(src, period, lo, hi):   # 1 trong khoảng [lo, hi] của chu kỳ
        d = N(nt, 'ShaderNodeMath', operation='DIVIDE'); d.inputs[1].default_value = period; L.new(src, d.inputs[0]); f = N(nt, 'ShaderNodeMath', operation='FRACT'); L.new(d.outputs[0], f.inputs[0])
        g1 = N(nt, 'ShaderNodeMath', operation='GREATER_THAN'); g1.inputs[1].default_value = lo; L.new(f.outputs[0], g1.inputs[0]); g2 = N(nt, 'ShaderNodeMath', operation='LESS_THAN'); g2.inputs[1].default_value = hi; L.new(f.outputs[0], g2.inputs[0])
        mm = N(nt, 'ShaderNodeMath', operation='MULTIPLY'); L.new(g1.outputs[0], mm.inputs[0]); L.new(g2.outputs[0], mm.inputs[1]); return mm.outputs[0]
    wu = frac_band(u.outputs[0], 3.0, 0.32, 0.68); wv = frac_band(sp.outputs['Z'], 3.0, 0.30, 0.80)
    wall = N(nt, 'ShaderNodeMath', operation='LESS_THAN'); wall.inputs[1].default_value = 0.25; az = N(nt, 'ShaderNodeMath', operation='ABSOLUTE'); L.new(sep.outputs['Z'], az.inputs[0]); L.new(az.outputs[0], wall.inputs[0])
    win = N(nt, 'ShaderNodeMath', operation='MULTIPLY'); L.new(wu, win.inputs[0]); L.new(wv, win.inputs[1]); win2 = N(nt, 'ShaderNodeMath', operation='MULTIPLY'); L.new(win.outputs[0], win2.inputs[0]); L.new(wall.outputs[0], win2.inputs[1])
    # mái dốc → ngói
    rf1 = N(nt, 'ShaderNodeMath', operation='GREATER_THAN'); rf1.inputs[1].default_value = 0.25; L.new(sep.outputs['Z'], rf1.inputs[0]); rf2 = N(nt, 'ShaderNodeMath', operation='LESS_THAN'); rf2.inputs[1].default_value = 0.97; L.new(sep.outputs['Z'], rf2.inputs[0])
    rf = N(nt, 'ShaderNodeMath', operation='MULTIPLY'); L.new(rf1.outputs[0], rf.inputs[0]); L.new(rf2.outputs[0], rf.inputs[1])
    tcol = N(nt, 'ShaderNodeMix', data_type='RGBA', blend_type='MULTIPLY'); tcol.inputs['Factor'].default_value = 0.85; L.new(vc.outputs['Color'], tcol.inputs[6]); L.new(tl.outputs['Color'], tcol.inputs[7])
    kt = N(nt, 'ShaderNodeMix', data_type='RGBA'); kt.inputs[7].default_value = (1.7, 1.7, 1.7, 1)
    roofc = N(nt, 'ShaderNodeMix', data_type='RGBA'); L.new(rf.outputs[0], roofc.inputs['Factor']); L.new(mpl.outputs[2], roofc.inputs[6]); L.new(tcol.outputs[2], roofc.inputs[7])
    glass = N(nt, 'ShaderNodeMix', data_type='RGBA'); L.new(win2.outputs[0], glass.inputs['Factor']); L.new(roofc.outputs[2], glass.inputs[6]); glass.inputs[7].default_value = (0.035, 0.04, 0.05, 1)
    L.new(glass.outputs[2], b.inputs['Base Color'])
    rg = N(nt, 'ShaderNodeMapRange'); L.new(win2.outputs[0], rg.inputs['Value']); rg.inputs['To Min'].default_value = 0.88; rg.inputs['To Max'].default_value = 0.12; L.new(rg.outputs['Result'], b.inputs['Roughness'])
    if NIGHT > 0 and 'Emission Color' in b.inputs:   # cửa sổ sáng đêm: chỉ ≥ 1950 (cảnh đêm 1782: tắt) — để 0
        pass
    m['kind'] = 'nha'; return m

def mat_vc(kind, tex=None, scale=1.7, rough=0.9, k=0.5, base=(0.5, 0.5, 0.5)):
    m = bpy.data.materials.new('m_' + kind); m.use_nodes = True; nt = m.node_tree; b = principled(m); b.inputs['Roughness'].default_value = rough; L = nt.links
    vc = attr(nt, 'col'); has = N(nt, 'ShaderNodeMix', data_type='RGBA'); has.inputs[6].default_value = (*base, 1); L.new(vc.outputs['Color'], has.inputs[7]); L.new(vc.outputs['Alpha'], has.inputs['Factor'])
    c = has.outputs[2]
    if tex:
        t = box_tex(nt, os.path.join(TEX, tex), scale); bw = N(nt, 'ShaderNodeRGBToBW'); L.new(t.outputs['Color'], bw.inputs[0]); kk = N(nt, 'ShaderNodeMath', operation='MULTIPLY'); kk.inputs[1].default_value = 1 / 0.5; L.new(bw.outputs[0], kk.inputs[0])
        mm = N(nt, 'ShaderNodeMix', data_type='RGBA', blend_type='MULTIPLY'); mm.inputs['Factor'].default_value = k; L.new(c, mm.inputs[6]); L.new(kk.outputs[0], mm.inputs[7]); c = mm.outputs[2]
        bm = N(nt, 'ShaderNodeBump'); bm.inputs['Strength'].default_value = 0.5; L.new(bw.outputs[0], bm.inputs['Height']); L.new(bm.outputs['Normal'], b.inputs['Normal'])
    L.new(c, b.inputs['Base Color'])
    if kind == 'co':
        tlu = N(nt, 'ShaderNodeBsdfTranslucent'); L.new(c, tlu.inputs['Color']); mx = N(nt, 'ShaderNodeMixShader'); mx.inputs['Fac'].default_value = 0.4
        o = [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'][0]; L.new(b.outputs[0], mx.inputs[1]); L.new(tlu.outputs[0], mx.inputs[2]); L.new(mx.outputs[0], o.inputs['Surface'])
    m['kind'] = kind; return m

def mat_inst(kind, base=(0.12, 0.16, 0.07)):   # bụi/cây: màu bản sao (thuộc tính 'icol' trên điểm → miền instance)
    m = bpy.data.materials.new('m_' + kind); m.use_nodes = True; nt = m.node_tree; b = principled(m); b.inputs['Roughness'].default_value = 0.85; L = nt.links
    ic = attr(nt, 'icol', 'INSTANCER'); mx = N(nt, 'ShaderNodeMix', data_type='RGBA'); mx.inputs[6].default_value = (*base, 1); L.new(ic.outputs['Color'], mx.inputs[7]); L.new(ic.outputs['Alpha'], mx.inputs['Factor'])
    nz = N(nt, 'ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.4; mm = N(nt, 'ShaderNodeMix', data_type='RGBA', blend_type='MULTIPLY'); mm.inputs['Factor'].default_value = 0.35
    L.new(mx.outputs[2], mm.inputs[6]); L.new(nz.outputs['Color'], mm.inputs[7]); L.new(mm.outputs[2], b.inputs['Base Color'])
    bm = N(nt, 'ShaderNodeBump'); bm.inputs['Strength'].default_value = 0.6; L.new(nz.outputs['Fac'], bm.inputs['Height']); L.new(bm.outputs['Normal'], b.inputs['Normal'])
    m['kind'] = kind; return m

def mat_const(kind, mc, mo=1.0):
    """vật KHÔNG có màu đỉnh: màu vật liệu k2v (rec.mc, tuyến tính) — lều vải, thân tàu, mái/sàn bằng, cột cờ… (NC-CPU: xám 0,45 hoặc đen do Attribute 'col' rỗng)"""
    key = f"c_{kind}_{mc[0]:.2f}_{mc[1]:.2f}_{mc[2]:.2f}"
    if key in MATS: return MATS[key]
    m = bpy.data.materials.new('m_' + key); m.use_nodes = True; nt = m.node_tree; b = principled(m); L = nt.links
    b.inputs['Base Color'].default_value = (*mc[:3], 1); b.inputs['Roughness'].default_value = 0.85 if kind != 'nha' else 0.9
    if kind in ('cong_su', 'do_nat'):
        t = box_tex(nt, os.path.join(TEX, 'seaworn_sandstone_brick_diff_1k.jpg'), 1.69); bw = N(nt, 'ShaderNodeRGBToBW'); L.new(t.outputs['Color'], bw.inputs[0])
        kk = N(nt, 'ShaderNodeMath', operation='MULTIPLY'); kk.inputs[1].default_value = 2.0; L.new(bw.outputs[0], kk.inputs[0])
        mm = N(nt, 'ShaderNodeMix', data_type='RGBA', blend_type='MULTIPLY'); mm.inputs['Factor'].default_value = 0.55; mm.inputs[6].default_value = (*mc[:3], 1); L.new(kk.outputs[0], mm.inputs[7]); L.new(mm.outputs[2], b.inputs['Base Color'])
    elif max(mc[:3]) > 0.3:   # vải/vữa sáng: vân nhỏ để không phẳng lì
        nz = N(nt, 'ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 3.0; mm = N(nt, 'ShaderNodeMix', data_type='RGBA', blend_type='MULTIPLY'); mm.inputs['Factor'].default_value = 0.18
        mm.inputs[6].default_value = (*mc[:3], 1); L.new(nz.outputs['Color'], mm.inputs[7]); L.new(mm.outputs[2], b.inputs['Base Color'])
    if mo < 0.99: b.inputs['Alpha'].default_value = mo
    m['kind'] = kind; MATS[key] = m; return m
def mat_flag(kind, png_dataurl, k):
    """cờ: ảnh lá cờ k2v (flagTex — vật mang dữ kiện, giữ đúng mẫu) theo UV, hai mặt, vải xuyên sáng một phần"""
    import base64, tempfile
    fn = os.path.join(tempfile.gettempdir(), f'ncg_co_{k}.png'); open(fn, 'wb').write(base64.b64decode(png_dataurl.split(',', 1)[1]))
    m = bpy.data.materials.new(f'm_co_{k}'); m.use_nodes = True; nt = m.node_tree; b = principled(m); L = nt.links; b.inputs['Roughness'].default_value = 0.8
    t = N(nt, 'ShaderNodeTexImage'); t.image = img(fn); uvn = N(nt, 'ShaderNodeUVMap'); uvn.uv_map = 'uv'; L.new(uvn.outputs['UV'], t.inputs['Vector']); L.new(t.outputs['Color'], b.inputs['Base Color'])
    tlu = N(nt, 'ShaderNodeBsdfTranslucent'); L.new(t.outputs['Color'], tlu.inputs['Color']); mx = N(nt, 'ShaderNodeMixShader'); mx.inputs['Fac'].default_value = 0.35
    o = [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'][0]; L.new(b.outputs[0], mx.inputs[1]); L.new(tlu.outputs[0], mx.inputs[2]); L.new(mx.outputs[0], o.inputs['Surface'])
    m['kind'] = kind; return m
MATS = {}
def mat(kind, inst=False, hasC=True):
    key = kind + ('_i' if inst else '') + ('' if hasC else '_0')
    if key in MATS: return MATS[key]
    if kind == 'dia_hinh': m = mat_ground()
    elif kind == 'nha': m = mat_city()
    elif inst and kind in ('cay', 'bui'): m = mat_inst(kind, (0.10, 0.15, 0.06) if kind == 'cay' else (0.15, 0.18, 0.09))
    elif kind in ('cong_su', 'do_nat'): m = mat_vc(kind, 'seaworn_sandstone_brick_diff_1k.jpg', 1.69, 0.9, 0.55, (0.62, 0.55, 0.42))
    elif kind == 'nguoi': m = mat_vc(kind, None, rough=0.8, base=(0.4, 0.3, 0.25))
    elif kind == 'co': m = mat_vc(kind, None, rough=0.7, base=(0.6, 0.6, 0.6))
    else: m = mat_vc(kind + ('_i' if inst else ''), None, rough=0.8, base=(0.45, 0.42, 0.38))
    if not hasC:   # không có màu đỉnh: bỏ nút thuộc tính 'col' (Cycles trả alpha 1, màu 0 → đen)
        for n in list(m.node_tree.nodes):
            if n.type == 'ATTRIBUTE' and n.attribute_name == 'col':
                for l in list(n.outputs['Alpha'].links): l.to_socket.node.inputs['Factor'].default_value = 0.0 if 'Factor' in l.to_socket.node.inputs else 0
                for l in list(n.outputs['Alpha'].links) + list(n.outputs['Color'].links): m.node_tree.links.remove(l)
                m.node_tree.nodes.remove(n)
        m.name = m.name + '_0'
    MATS[key] = m; return m

# ---------------------------------------------------------------- hình học (cùng phép đổi trục với scripts/k2tl/cy6.py)
def mesh_from(P, I, name, C=None, smooth=False, UV=None):
    me = bpy.data.meshes.new(name); n = len(P) // 3
    V = P.reshape(-1, 3)[:, [0, 2, 1]] * np.array([1, -1, 1], np.float32)
    if I is None: I = np.arange(n, dtype=np.uint32)
    I = I.reshape(-1, 3)
    me.vertices.add(n); me.vertices.foreach_set('co', V.ravel())
    nl = len(I); me.loops.add(nl * 3); me.loops.foreach_set('vertex_index', I.ravel().astype(np.int32))
    me.polygons.add(nl); me.polygons.foreach_set('loop_start', np.arange(0, nl * 3, 3, dtype=np.int32)); me.polygons.foreach_set('loop_total', np.full(nl, 3, np.int32))
    me.update(calc_edges=False); me.validate(clean_customdata=False)
    me.polygons.foreach_set('use_smooth', np.full(nl, smooth, bool))
    if C is not None and len(C) == n * 3:
        ca = me.color_attributes.new('col', 'FLOAT_COLOR', 'POINT'); ca.data.foreach_set('color', np.hstack([C.reshape(-1, 3), np.ones((n, 1), np.float32)]).ravel())
    if UV is not None and len(UV) == n * 2:
        uv = me.uv_layers.new(name='uv'); li = np.zeros(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', li); uv.data.foreach_set('uv', UV.reshape(-1, 2)[li].ravel())
    return me
col = bpy.data.collections.new('k2v'); sc.collection.children.link(col); base_col = bpy.data.collections.new('k2v_goc'); sc.collection.children.link(base_col)
stat = {'vat': 0, 'tam_giac': 0, 'ban_sao': 0, 'loai': {}}
if '--topo' in opt:
    for d in opt['--topo'].split(','): TOPO.append(topo_image(d))
TERR = []
SKY_K = 1.0
for k, o in enumerate(M['objs']):
    kind = o['kind']
    if kind == 'khac' and o['name'] and 'Sprite' in o['name']: continue
    P = load(o['buf']['P']); I = load(o['buf']['I']) if 'I' in o['buf'] else None; C = load(o['buf']['C']) if 'C' in o['buf'] else None
    UV = load(o['buf']['UV']) if 'UV' in o['buf'] else None
    me = mesh_from(P, I, f"o{k}_{kind}", C, smooth=kind in ('dia_hinh', 'cay', 'bui'), UV=UV)
    inst = 'M' in o['buf']; mc = o.get('mc')
    if o.get('map') and UV is not None: me.materials.append(mat_flag(kind, o['map'], k)); stat['co_anh'] = stat.get('co_anh', 0) + 1
    elif C is None and mc and min(mc[:3]) < 0.97 and kind != 'dia_hinh' and not (inst and kind in ('cay', 'bui')):   # mc trắng = màu nằm trong shader k2v → giữ vật liệu NC-CPU
        me.materials.append(mat_const(kind, mc, o.get('mo', 1.0))); stat['mau_vl'] = stat.get('mau_vl', 0) + 1
    else: me.materials.append(mat(kind, inst, C is not None or kind == 'dia_hinh' or (inst and kind in ('cay', 'bui'))))
    if inst:
        base = bpy.data.objects.new(f"goc{k}", me); base_col.objects.link(base)
        Mx = load(o['buf']['M']).reshape(-1, 16); IC = load(o['buf']['IC']).reshape(-1, 3) if 'IC' in o['buf'] else None
        pts, rot, scl, keep = [], [], [], []
        for q, e in enumerate(Mx):
            m3 = mathutils.Matrix([e[0:4], e[4:8], e[8:12], e[12:16]]).transposed(); mb = S @ m3 @ S.inverted(); lo, ro, sc_ = mb.decompose()
            if sc_.length < 1e-6: continue
            pts.append(lo); rot.append(ro.to_euler()); scl.append(sc_); keep.append(q)
        if not pts: continue
        pm = bpy.data.meshes.new(f"pts{k}"); pm.vertices.add(len(pts)); pm.vertices.foreach_set('co', np.array(pts, np.float32).ravel())
        ra = pm.attributes.new('rot', 'FLOAT_VECTOR', 'POINT'); ra.data.foreach_set('vector', np.array([tuple(r) for r in rot], np.float32).ravel())
        sa = pm.attributes.new('scl', 'FLOAT_VECTOR', 'POINT'); sa.data.foreach_set('vector', np.array([tuple(s) for s in scl], np.float32).ravel())
        if IC is not None:
            ia = pm.color_attributes.new('icol', 'FLOAT_COLOR', 'POINT'); ia.data.foreach_set('color', np.hstack([IC[keep], np.ones((len(keep), 1), np.float32)]).ravel())
        ob = bpy.data.objects.new(f"inst{k}_{kind}", pm); col.objects.link(ob)
        gm = ob.modifiers.new('ban_sao', 'NODES'); ng = bpy.data.node_groups.new(f'gn{k}', 'GeometryNodeTree'); gm.node_group = ng
        ng.interface.new_socket('Geometry', in_out='INPUT', socket_type='NodeSocketGeometry'); ng.interface.new_socket('Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
        gi = ng.nodes.new('NodeGroupInput'); go = ng.nodes.new('NodeGroupOutput'); mtp = ng.nodes.new('GeometryNodeMeshToPoints'); iop = ng.nodes.new('GeometryNodeInstanceOnPoints'); oi = ng.nodes.new('GeometryNodeObjectInfo'); oi.inputs['Object'].default_value = base
        rr = ng.nodes.new('GeometryNodeInputNamedAttribute'); rr.data_type = 'FLOAT_VECTOR'; rr.inputs['Name'].default_value = 'rot'
        ss = ng.nodes.new('GeometryNodeInputNamedAttribute'); ss.data_type = 'FLOAT_VECTOR'; ss.inputs['Name'].default_value = 'scl'
        L = ng.links; L.new(gi.outputs[0], mtp.inputs['Mesh']); L.new(mtp.outputs['Points'], iop.inputs['Points']); L.new(oi.outputs['Geometry'], iop.inputs['Instance'])
        L.new(rr.outputs['Attribute'], iop.inputs['Rotation']); L.new(ss.outputs['Attribute'], iop.inputs['Scale'])
        BX = int(opt.get('--bushx', 1))
        if kind == 'bui' and BX > 1:   # bụi DÀY: (BX − 1) bản sao nhỏ lệch ≤ 4 m quanh MỖI bụi k2v (đã ẩn theo năm/trại/đô thị) — không rải bụi ở chỗ k2v không có
            dup = ng.nodes.new('GeometryNodeDuplicateElements'); dup.domain = 'POINT'; dup.inputs['Amount'].default_value = BX - 1; L.new(mtp.outputs['Points'], dup.inputs['Geometry'])
            rv = ng.nodes.new('FunctionNodeRandomValue'); rv.data_type = 'FLOAT_VECTOR'; rv.inputs['Min'].default_value = (-4.0, -4.0, -0.45); rv.inputs['Max'].default_value = (4.0, 4.0, -0.15); rv.inputs['Seed'].default_value = 11
            sp_ = ng.nodes.new('GeometryNodeSetPosition'); L.new(dup.outputs['Geometry'], sp_.inputs['Geometry']); L.new(rv.outputs['Value'], sp_.inputs['Offset'])
            rf = ng.nodes.new('FunctionNodeRandomValue'); rf.data_type = 'FLOAT'; rf.inputs['Min'].default_value = 0.4; rf.inputs['Max'].default_value = 0.8; rf.inputs['Seed'].default_value = 5
            sm = ng.nodes.new('ShaderNodeVectorMath'); sm.operation = 'SCALE'; L.new(ss.outputs['Attribute'], sm.inputs[0]); L.new(rf.outputs['Value'], sm.inputs['Scale'])
            rz = ng.nodes.new('FunctionNodeRandomValue'); rz.data_type = 'FLOAT_VECTOR'; rz.inputs['Min'].default_value = (0, 0, 0); rz.inputs['Max'].default_value = (0, 0, 6.283); rz.inputs['Seed'].default_value = 7
            ra_ = ng.nodes.new('ShaderNodeVectorMath'); ra_.operation = 'ADD'; L.new(rr.outputs['Attribute'], ra_.inputs[0]); L.new(rz.outputs['Value'], ra_.inputs[1])
            iop2 = ng.nodes.new('GeometryNodeInstanceOnPoints'); L.new(sp_.outputs['Geometry'], iop2.inputs['Points']); L.new(oi.outputs['Geometry'], iop2.inputs['Instance'])
            L.new(ra_.outputs[0], iop2.inputs['Rotation']); L.new(sm.outputs[0], iop2.inputs['Scale'])
            jg = ng.nodes.new('GeometryNodeJoinGeometry'); L.new(iop.outputs['Instances'], jg.inputs[0]); L.new(iop2.outputs['Instances'], jg.inputs[0]); L.new(jg.outputs[0], go.inputs[0])
            stat['bui_them'] = stat.get('bui_them', 0) + len(pts) * (BX - 1)
        else: L.new(iop.outputs['Instances'], go.inputs[0])
        stat['ban_sao'] += len(pts)
    else:
        ob = bpy.data.objects.new(f"o{k}_{kind}", me); col.objects.link(ob)
        if kind == 'dia_hinh': TERR.append(ob)
    stat['vat'] += 1; stat['tam_giac'] += o['nt'] * (o.get('inst') or 1); stat['loai'][kind] = stat['loai'].get(kind, 0) + 1
base_col.hide_render = True
T_LOAD = time.time() - T0

# ---------------------------------------------------------------- nước, trời, nắng, máy
C = M['cam']; Su = M['sun']; sd = (S @ mathutils.Vector((*Su['dir'], 0)).to_4d()).to_3d().normalized()
sun_el = math.degrees(math.asin(max(-1, min(1, sd.z))))
def water():
    bpy.ops.mesh.primitive_plane_add(size=60000, location=(0, 0, 0)); wp = bpy.context.active_object; wp.name = 'nuoc'
    m = bpy.data.materials.new('m_nuoc'); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']; L = nt.links
    b.inputs['Base Color'].default_value = (0.010, 0.045, 0.070, 1); b.inputs['Roughness'].default_value = 0.035; b.inputs['IOR'].default_value = 1.333
    if 'Specular IOR Level' in b.inputs: b.inputs['Specular IOR Level'].default_value = 0.5
    tc = N(nt, 'ShaderNodeTexCoord'); w1 = N(nt, 'ShaderNodeTexWave'); w1.inputs['Scale'].default_value = 0.035; w1.inputs['Distortion'].default_value = 6; w1.inputs['Detail'].default_value = 4
    w2 = N(nt, 'ShaderNodeTexNoise'); w2.inputs['Scale'].default_value = 0.12; w2.inputs['Detail'].default_value = 6
    w3 = N(nt, 'ShaderNodeTexNoise'); w3.inputs['Scale'].default_value = 0.9; w3.inputs['Detail'].default_value = 3
    for w in (w1, w2, w3): L.new(tc.outputs['Object'], w.inputs['Vector'])
    if hasattr(w2, 'noise_dimensions'): w2.noise_dimensions = '4D'; w3.noise_dimensions = '4D'
    ad = N(nt, 'ShaderNodeMath', operation='ADD'); L.new(w1.outputs['Fac'], ad.inputs[0]); L.new(w2.outputs['Fac'], ad.inputs[1]); ad2 = N(nt, 'ShaderNodeMath', operation='MULTIPLY_ADD'); ad2.inputs[1].default_value = 0.3
    L.new(w3.outputs['Fac'], ad2.inputs[0]); L.new(ad.outputs[0], ad2.inputs[2])
    bm = N(nt, 'ShaderNodeBump'); bm.inputs['Strength'].default_value = 0.22; bm.inputs['Distance'].default_value = 0.6; L.new(ad2.outputs[0], bm.inputs['Height']); L.new(bm.outputs['Normal'], b.inputs['Normal'])
    wp.data.materials.append(m); m['kind'] = 'nuoc'; return wp, (w2, w3)
WATER, WN = water()
cam = bpy.data.cameras.new('cam'); cob = bpy.data.objects.new('cam', cam); sc.collection.objects.link(cob); sc.camera = cob
q = C['quat']; m3 = mathutils.Quaternion((q[3], q[0], q[1], q[2])).to_matrix().to_4x4(); m3.translation = mathutils.Vector(C['pos']); cob.matrix_world = S @ m3
cam.sensor_fit = 'VERTICAL'; cam.angle_y = math.radians(C['fov']); cam.clip_start = max(1.0, C['near']); cam.clip_end = 90000
RES = opt.get('--res'); W, H = (C['W'], C['H']) if not RES else map(int, RES.split('x')); sc.render.resolution_x, sc.render.resolution_y = W, H; sc.render.resolution_percentage = 100
DOF_L = [None]   # cú lặn: điểm nhìn của đường máy (k['l']) → lấy nét đúng chủ thể, không vào mặt nước sát máy
def set_dof():
    """DOF nhẹ: lấy nét vào điểm tia giữa khung chạm cảnh; f/--fstop (mặc định 4) trên cảm biến 36 mm — rõ ở cận cảnh/lướt thấp, gần như không thấy ở góc cao"""
    if '--dof' not in opt: return None
    if DOF_L[0] is not None:
        dist = (DOF_L[0] - cob.matrix_world.translation).length; cam.dof.use_dof = True; cam.dof.focus_distance = dist; cam.dof.aperture_fstop = float(opt.get('--fstop', 5.6)); cam.sensor_width = 36.0; return dist
    for ob in FX: ob.hide_viewport = True
    bpy.context.view_layer.update(); mw = cob.matrix_world; o_ = mw.translation; d_ = (mw.to_3x3() @ mathutils.Vector((0, 0, -1))).normalized()
    hit, loc, *_ = sc.ray_cast(bpy.context.view_layer.depsgraph, o_, d_, distance=20000)
    dist = (loc - o_).length if hit else 2000.0
    for ob in FX: ob.hide_viewport = False
    cam.dof.use_dof = True; cam.dof.focus_distance = dist; cam.dof.aperture_fstop = float(opt.get('--fstop', 4.0)); cam.sensor_width = 36.0; return dist
sl = bpy.data.lights.new('sun', 'SUN'); sl.angle = math.radians(0.53)
so = bpy.data.objects.new('sun', sl); sc.collection.objects.link(so); so.rotation_euler = sd.to_track_quat('Z', 'Y').to_euler()
wld = bpy.data.worlds.new('w'); sc.world = wld; wld.use_nodes = True; wnt = wld.node_tree; wnt.nodes.clear()
bg = wnt.nodes.new('ShaderNodeBackground'); wo = wnt.nodes.new('ShaderNodeOutputWorld'); wnt.links.new(bg.outputs[0], wo.inputs[0])
SKYNODE = None
def sky_day():
    """trời gradient như k2v (water.js skyCol: chân trời sáng ngả xám-lam → thiên đỉnh lam) — tia máy/tia bóng thấy trời SÁNG (như k2v vẽ trời),
    tia khuếch tán nhận trời DỊU khớp ánh trời bán cầu k2v (bức xạ mặt phẳng ≈ hemiI × màu trời) → cùng tỉ lệ nắng/trời với cách A."""
    L = wnt.links; tc = wnt.nodes.new('ShaderNodeTexCoord'); sx = wnt.nodes.new('ShaderNodeSeparateXYZ'); L.new(tc.outputs['Generated'], sx.inputs[0])
    cl = wnt.nodes.new('ShaderNodeClamp'); L.new(sx.outputs['Z'], cl.inputs['Value']); pw = wnt.nodes.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 0.5; L.new(cl.outputs[0], pw.inputs[0])
    vis = wnt.nodes.new('ShaderNodeMix'); vis.data_type = 'RGBA'; L.new(pw.outputs[0], vis.inputs['Factor']); vis.inputs[6].default_value = (*HAZE_C, 1); vis.inputs[7].default_value = (0.20, 0.40, 0.78, 1)
    hm = M['hemi']; k = hm['intensity'] * 1.15 * SKYDIF
    dif = wnt.nodes.new('ShaderNodeMix'); dif.data_type = 'RGBA'; L.new(cl.outputs[0], dif.inputs['Factor'])
    dif.inputs[6].default_value = (*[c * k for c in hm['sky']], 1); dif.inputs[7].default_value = (*[c * k * 0.85 for c in hm['sky']], 1)
    lp = wnt.nodes.new('ShaderNodeLightPath'); mx = wnt.nodes.new('ShaderNodeMath'); mx.operation = 'MAXIMUM'; L.new(lp.outputs['Is Camera Ray'], mx.inputs[0]); L.new(lp.outputs['Is Glossy Ray'], mx.inputs[1])
    sel = wnt.nodes.new('ShaderNodeMix'); sel.data_type = 'RGBA'; L.new(mx.outputs[0], sel.inputs['Factor']); L.new(dif.outputs[2], sel.inputs[6]); L.new(vis.outputs[2], sel.inputs[7])
    return sel.outputs[2], dif
def sky_night():
    """trời đêm như k2v (water.js skyCol, uNight = 1): thiên đỉnh (0,018; 0,030; 0,070), chân trời + (0,06; 0,075; 0,11)·(1 − h)⁴ — tia máy/bóng thấy trời này;
    tia khuếch tán: ánh trời đêm bán cầu k2v (hemiI × màu trời đêm)."""
    L = wnt.links; tc = wnt.nodes.new('ShaderNodeTexCoord'); sx = wnt.nodes.new('ShaderNodeSeparateXYZ'); L.new(tc.outputs['Generated'], sx.inputs[0])
    cl = wnt.nodes.new('ShaderNodeClamp'); L.new(sx.outputs['Z'], cl.inputs['Value']); om = wnt.nodes.new('ShaderNodeMath'); om.operation = 'SUBTRACT'; om.inputs[0].default_value = 1.0; L.new(cl.outputs[0], om.inputs[1])
    p4 = wnt.nodes.new('ShaderNodeMath'); p4.operation = 'POWER'; p4.inputs[1].default_value = 4.0; L.new(om.outputs[0], p4.inputs[0])
    vis = wnt.nodes.new('ShaderNodeMix'); vis.data_type = 'RGBA'; L.new(p4.outputs[0], vis.inputs['Factor']); vis.inputs[6].default_value = (0.018, 0.030, 0.070, 1); vis.inputs[7].default_value = (0.078, 0.105, 0.180, 1)
    hm = M['hemi']; k = hm['intensity'] * SKYDIF; dif = wnt.nodes.new('ShaderNodeRGB'); dif.outputs[0].default_value = (*[c * k for c in hm['sky']], 1)
    lp = wnt.nodes.new('ShaderNodeLightPath'); mx = wnt.nodes.new('ShaderNodeMath'); mx.operation = 'MAXIMUM'; L.new(lp.outputs['Is Camera Ray'], mx.inputs[0]); L.new(lp.outputs['Is Glossy Ray'], mx.inputs[1])
    sel = wnt.nodes.new('ShaderNodeMix'); sel.data_type = 'RGBA'; L.new(mx.outputs[0], sel.inputs['Factor']); L.new(dif.outputs[0], sel.inputs[6]); L.new(vis.outputs[2], sel.inputs[7])
    return sel.outputs[2], dif
# trời NGÀY và ĐÊM cùng dựng, trộn theo NK (= uNight của k2v; khung cổng: 0/1 cố định; cú lặn: cập nhật từng khung bằng set_light)
_cd, DIF_D = sky_day(); _cn, DIF_N = sky_night()
NKN = wnt.nodes.new('ShaderNodeValue'); NKN.outputs[0].default_value = 1.0 if NIGHT >= 0.5 else 0.0
_mw = wnt.nodes.new('ShaderNodeMix'); _mw.data_type = 'RGBA'; wnt.links.new(NKN.outputs[0], _mw.inputs['Factor']); wnt.links.new(_cd, _mw.inputs[6]); wnt.links.new(_cn, _mw.inputs[7])
wnt.links.new(_mw.outputs[2], bg.inputs['Color']); bg.inputs['Strength'].default_value = 1.0
sl.energy = Su['intensity']; sl.color = Su['color'][:3]
HAZE_EM = []
for m in list(bpy.data.materials):
    if m.get('kind') and m.use_nodes: haze_wrap(m)
def set_light(st):
    """ánh sáng của MỘT khung k2v (gpu_export.js --lightfx): nắng/trăng (hướng, màu, cường độ), ánh trời bán cầu, uNight → trời + màu sương"""
    d = (S @ mathutils.Vector((*st['sun']['dir'], 0)).to_4d()).to_3d().normalized(); so.rotation_euler = d.to_track_quat('Z', 'Y').to_euler()
    sl.energy = st['sun']['intensity']; sl.color = st['sun']['color'][:3]; hm = st['hemi']; k = hm['intensity'] * 1.15 * SKYDIF
    DIF_D.inputs[6].default_value = (*[c * k for c in hm['sky']], 1); DIF_D.inputs[7].default_value = (*[c * k * 0.85 for c in hm['sky']], 1)
    DIF_N.outputs[0].default_value = (*[c * hm['intensity'] * SKYDIF for c in hm['sky']], 1)
    nk = float(st.get('night') or 0); NKN.outputs[0].default_value = nk; NK_NOW[0] = nk
    for em in HAZE_EM: em.inputs['Color'].default_value = (*[c * (1 - nk) + cn * nk for c, cn in zip(HAZE_C, (0.035, 0.05, 0.09))], 1)

# ---------------------------------------------------------------- lửa (pin nổi cháy) : đèn điểm + ngọn lửa phát xạ
FIRES = json.loads(opt['--fires']) if '--fires' in opt else []
FIRE_OBJ = []
def add_fires():
    fm = bpy.data.materials.new('m_lua'); fm.use_nodes = True; nt = fm.node_tree; nt.nodes.clear(); out = N(nt, 'ShaderNodeOutputMaterial'); em = N(nt, 'ShaderNodeEmission')
    nz = N(nt, 'ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 0.35; cr = N(nt, 'ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = (1.0, 0.25, 0.03, 1); cr.color_ramp.elements[1].color = (1.0, 0.75, 0.30, 1)
    nt.links.new(nz.outputs['Fac'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], em.inputs['Color']); em.inputs['Strength'].default_value = 60.0; nt.links.new(em.outputs[0], out.inputs['Surface'])
    for f in FIRES:
        e, n = f['at']; z = f.get('z', 3.0); s = f.get('size', 30) / 30.0
        for j, (dx, dy, k) in enumerate(((0, 0, 1.0), (-11, 3, 0.7), (10, -4, 0.75))):   # 3 ngọn lửa trên boong pin nổi (dài ≈ 45 m)
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1, location=(e + dx * s, n + dy * s, z + 4 * s * k)); fo = bpy.context.active_object; fo.scale = (5 * s * k, 3 * s * k, 7 * s * k); fo.data.materials.append(fm); fo.name = 'lua'
            if j: FIRE_OBJ.append((fo, None, f))
        li = bpy.data.lights.new('lua', 'POINT'); li.energy = f.get('W', 2.5e6) * s; li.color = (1.0, 0.45, 0.14); li.shadow_soft_size = 8 * s
        lo = bpy.data.objects.new('lua', li); lo.location = (e, n, z + 12 * s); sc.collection.objects.link(lo); FIRE_OBJ.append((fo, lo, f))
if FIRES: add_fires()
SMOKE = []
def add_smoke():
    """cột khói THỂ TÍCH (Principled Volume, mật độ nhiễu 4D theo thời gian, nghiêng theo gió) trên mỗi đám cháy — thử chi phí thể tích ở Cycles CPU."""
    vm = bpy.data.materials.new('m_khoi'); vm.use_nodes = True; nt = vm.node_tree; nt.nodes.clear(); out = N(nt, 'ShaderNodeOutputMaterial'); pv = N(nt, 'ShaderNodeVolumePrincipled'); L = nt.links
    tc = N(nt, 'ShaderNodeTexCoord'); nz = N(nt, 'ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 2.2; nz.inputs['Detail'].default_value = 4
    if hasattr(nz, 'noise_dimensions'): nz.noise_dimensions = '4D'
    L.new(tc.outputs['Generated'], nz.inputs['Vector']); cr = N(nt, 'ShaderNodeMapRange'); cr.inputs['From Min'].default_value = 0.45; cr.inputs['From Max'].default_value = 0.75; L.new(nz.outputs['Fac'], cr.inputs['Value'])
    sx = N(nt, 'ShaderNodeSeparateXYZ'); L.new(tc.outputs['Generated'], sx.inputs[0]); fall = N(nt, 'ShaderNodeMapRange'); fall.inputs['From Min'].default_value = 0.0; fall.inputs['From Max'].default_value = 1.0; fall.inputs['To Min'].default_value = 1.0; fall.inputs['To Max'].default_value = 0.15; L.new(sx.outputs['Z'], fall.inputs['Value'])
    # mép: hình trụ mềm theo khoảng cách tới trục (x, y quanh 0,5)
    vx = N(nt, 'ShaderNodeVectorMath', operation='SUBTRACT'); vx.inputs[1].default_value = (0.5, 0.5, 0); L.new(tc.outputs['Generated'], vx.inputs[0]); m2 = N(nt, 'ShaderNodeVectorMath', operation='MULTIPLY'); m2.inputs[1].default_value = (1, 1, 0); L.new(vx.outputs[0], m2.inputs[0])
    ln = N(nt, 'ShaderNodeVectorMath', operation='LENGTH'); L.new(m2.outputs[0], ln.inputs[0]); edge = N(nt, 'ShaderNodeMapRange'); edge.inputs['From Min'].default_value = 0.5; edge.inputs['From Max'].default_value = 0.25; L.new(ln.outputs['Value'], edge.inputs['Value'])
    d1 = N(nt, 'ShaderNodeMath', operation='MULTIPLY'); L.new(cr.outputs['Result'], d1.inputs[0]); L.new(fall.outputs['Result'], d1.inputs[1]); d2 = N(nt, 'ShaderNodeMath', operation='MULTIPLY'); L.new(d1.outputs[0], d2.inputs[0]); L.new(edge.outputs['Result'], d2.inputs[1])
    d3 = N(nt, 'ShaderNodeMath', operation='MULTIPLY'); d3.inputs[1].default_value = float(opt.get('--smoked', 0.04)); L.new(d2.outputs[0], d3.inputs[0]); L.new(d3.outputs[0], pv.inputs['Density'])
    pv.inputs['Color'].default_value = (0.035, 0.032, 0.03, 1); pv.inputs['Anisotropy'].default_value = 0.3; L.new(pv.outputs[0], out.inputs['Volume']); SMOKE.append(nz)
    for f in FIRES:
        e, n = f['at']; s_ = f.get('size', 30) / 30.0
        bpy.ops.mesh.primitive_cube_add(size=1, location=(e - 40 * s_, n + 10 * s_, 110 * s_)); so_ = bpy.context.active_object; so_.scale = (110 * s_, 110 * s_, 240 * s_); so_.rotation_euler = (0, math.radians(-14), 0)
        so_.data.materials.append(vm); so_.name = 'khoi'
if '--smoke' in opt and FIRES: add_smoke()

FX = []
NK_NOW = [1.0 if NIGHT >= 0.5 else 0.0]
FXMAT = {}
def add_fx(fp=None):
    """khói/lửa của k2v ở khung này (fx.json, smokeV6: [E, cao, N, cỡ, alpha, tuổi, loại, hạt]) → mỗi cụm một cầu THỂ TÍCH:
    khói (loại 0: xám sáng thuốc súng/khói gỗ; loại 2: nâu-đen tàu cháy) mật độ = −ln(1 − 0,9·α)/cỡ × nhiễu 3D × tắt mép; lửa (loại 1) = thể tích phát xạ cam-vàng + đèn điểm.
    Cỡ/vị trí/alpha theo đúng k2v (cùng thời điểm) — không thêm cụm nào."""
    fp = fp or os.path.join(D, 'fx.json')
    if not os.path.exists(fp): return
    puffs = json.load(open(fp))['puffs']
    def vmat(name, fire, absorb=False):
        # absorb: khói đen muội (loại 2, albedo ≈ 0,08) = thể tích CHỈ HẤP THỤ — tán xạ gần như không thấy mà giá tán xạ (lấy mẫu đèn từng bước) rất cao (cú lặn đêm: > 10 phút/khung)
        vm = bpy.data.materials.new(name); vm.use_nodes = True; nt = vm.node_tree; nt.nodes.clear(); out = N(nt, 'ShaderNodeOutputMaterial'); L = nt.links
        pv = N(nt, 'ShaderNodeVolumeAbsorption' if absorb else 'ShaderNodeVolumePrincipled')
        tc = N(nt, 'ShaderNodeTexCoord'); nz = N(nt, 'ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.5; nz.inputs['Detail'].default_value = 3; nz.inputs['Roughness'].default_value = 0.5
        sd = attr(nt, 'sd', 'OBJECT'); off = N(nt, 'ShaderNodeVectorMath', operation='ADD'); L.new(tc.outputs['Object'], off.inputs[0]); L.new(sd.outputs['Fac'], off.inputs[1]); L.new(off.outputs[0], nz.inputs['Vector'])
        r = N(nt, 'ShaderNodeVectorMath', operation='LENGTH'); L.new(tc.outputs['Object'], r.inputs[0])
        fall = N(nt, 'ShaderNodeMapRange'); fall.inputs['From Min'].default_value = 1.0; fall.inputs['From Max'].default_value = 0.35; L.new(r.outputs['Value'], fall.inputs['Value'])
        sh = N(nt, 'ShaderNodeMapRange'); sh.inputs['From Min'].default_value = 0.30; sh.inputs['From Max'].default_value = 0.62; L.new(nz.outputs['Fac'], sh.inputs['Value'])
        d1 = N(nt, 'ShaderNodeMath', operation='MULTIPLY'); L.new(fall.outputs['Result'], d1.inputs[0]); L.new(sh.outputs['Result'], d1.inputs[1])
        dk = attr(nt, 'dk', 'OBJECT'); d2 = N(nt, 'ShaderNodeMath', operation='MULTIPLY'); L.new(d1.outputs[0], d2.inputs[0]); L.new(dk.outputs['Fac'], d2.inputs[1]); L.new(d2.outputs[0], pv.inputs['Density'])
        cc = attr(nt, 'cc', 'OBJECT')
        if absorb: iv = N(nt, 'ShaderNodeInvert'); L.new(cc.outputs['Color'], iv.inputs['Color']); L.new(iv.outputs['Color'], pv.inputs['Color'])   # hấp thụ màu (1 − albedo) → muội nâu-đen
        else: L.new(cc.outputs['Color'], pv.inputs['Color']); pv.inputs['Anisotropy'].default_value = 0.35
        if fire:
            # phát xạ theo CHIỀU DÀI: cường độ/m = fe = FIREEM/cỡ → độ chói qua cả cụm ≈ FIREEM (k2v lõi lửa HDR 1,2–3,4)
            pv.inputs['Emission Color'].default_value = (1.0, 0.42, 0.08, 1); fe = attr(nt, 'fe', 'OBJECT'); em = N(nt, 'ShaderNodeMath', operation='MULTIPLY')
            sz_ = N(nt, 'ShaderNodeSeparateXYZ'); L.new(tc.outputs['Object'], sz_.inputs[0]); vg = N(nt, 'ShaderNodeMapRange'); vg.inputs['From Min'].default_value = -1.0; vg.inputs['From Max'].default_value = 1.0
            vg.inputs['To Min'].default_value = 1.4; vg.inputs['To Max'].default_value = 0.1; L.new(sz_.outputs['Z'], vg.inputs['Value'])   # chân ngọn sáng, đỉnh tắt dần
            e0 = N(nt, 'ShaderNodeMath', operation='MULTIPLY'); L.new(d1.outputs[0], e0.inputs[0]); L.new(vg.outputs['Result'], e0.inputs[1])
            L.new(e0.outputs[0], em.inputs[0]); L.new(fe.outputs['Fac'], em.inputs[1]); L.new(em.outputs[0], pv.inputs['Emission Strength'])
            rp = N(nt, 'ShaderNodeValToRGB'); rp.color_ramp.elements[0].color = (0.9, 0.18, 0.02, 1); rp.color_ramp.elements[1].color = (1.0, 0.75, 0.32, 1); L.new(e0.outputs[0], rp.inputs['Fac']); L.new(rp.outputs['Color'], pv.inputs['Emission Color'])
        L.new(pv.outputs[0], out.inputs['Volume']); return vm
    if not FXMAT:
        FXMAT['s'], FXMAT['f'], FXMAT['d'] = vmat('m_fx_khoi', False), vmat('m_fx_lua', True), vmat('m_fx_muoi', False, absorb=True)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=1, location=(0, 0, -9999)); base_s = bpy.context.active_object; FXMAT['me'] = base_s.data; bpy.data.objects.remove(base_s)
    ms, mf, base_me = FXMAT['s'], FXMAT['f'], FXMAT['me']
    nf = 0
    for i, (x, y, z_n, sz, a, age, kd, sdv) in enumerate(puffs):
        if a < 0.01: continue
        kd = int(round(kd)); fire = kd == 1; ob = bpy.data.objects.new(f'fx{i}', base_me.copy()); col.objects.link(ob)
        ob.location = (x, z_n, y); r = sz * 0.5; ob.scale = (r * 0.6, r * 0.6, r * 1.35) if fire else (r, r, r * 0.9);   # lửa: ngọn đứng (k2v: lõi + lưỡi lửa)
        ob.data.materials.append(mf if fire else (FXMAT['d'] if (kd == 2 and '--soot-absorb' in opt) else ms))
        ob['sd'] = sdv * 13.7; ob['fe'] = float(opt.get('--fireem', 2.5)) / max(1.0, sz); ob['dk'] = -math.log(1 - min(0.95, 0.9 * a)) / max(1.0, sz) * (1.8 if fire else 1.3)
        ob['cc'] = (0.9, 0.55, 0.3) if fire else ((0.13, 0.11, 0.095) if kd == 2 else (0.80 + 0.1 * (1 - age), 0.79 + 0.1 * (1 - age), 0.77 + 0.1 * (1 - age)))
        ob.visible_shadow = True; FX.append(ob)
        if fire:
            li = bpy.data.lights.new(f'lua_fx{i}', 'POINT'); li.energy = (float(opt['--firew']) if '--firew' in opt else 20.0 + 380.0 * NK_NOW[0]) * sz * sz * a;   # ngày 20 → đêm 400 theo uNight TỪNG khung (lượt 1 chọn theo đầu đoạn → lửa bật sáng ở khung 168)   # ≈ 4π·E·(1,5·cỡ)²: E ≈ 1,5 (≈ 40 % nắng) ở 1,5 cỡ ban ngày; đêm ×10
            li.color = (1.0, 0.48, 0.16); li.shadow_soft_size = sz * 0.3
            lo = bpy.data.objects.new(f'lua_fx{i}', li); lo.location = (x, z_n, y); sc.collection.objects.link(lo); nf += 1; FX.append(lo)
    stat['fx_cum'] = len(FX); stat['fx_lua'] = nf
if '--fx' in opt: add_fx()

def cycles(spp, denoise=True, bounces=(4, 3, 2)):
    sc.render.engine = 'CYCLES'; cy = sc.cycles; cy.device = 'GPU' if _DEV != 'CPU' else 'CPU'; cy.samples = spp; cy.use_denoising = denoise; cy.denoiser = 'OPENIMAGEDENOISE'
    if hasattr(cy, 'denoising_use_gpu'): cy.denoising_use_gpu = _DEV != 'CPU'
    cy.max_bounces, cy.diffuse_bounces, cy.glossy_bounces = bounces[0], bounces[1], bounces[2]; cy.transmission_bounces = 4; cy.transparent_max_bounces = 8; cy.volume_bounces = int(opt.get('--vbounce', 2))
    cy.sample_clamp_indirect = float(opt.get('--clampi', 10.0)); cy.caustics_reflective = False; cy.caustics_refractive = False
    if hasattr(cy, 'volume_step_rate'): cy.volume_step_rate = float(opt.get('--vstep', 4.0))
    if '--vbiased' in opt and hasattr(cy, 'volume_biased'): cy.volume_biased = True; cy.volume_max_steps = int(opt.get('--vmax', 256))   # ray-marching cũ (nhanh, chệch nhẹ) thay null-scattering mặc định 5.x
    cy.use_adaptive_sampling = True; cy.adaptive_threshold = 0.02; sc.render.threads_mode = 'FIXED'; sc.render.threads = TH
    if hasattr(cy, 'denoising_input_passes'): cy.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
    sc.render.use_persistent_data = '--persist' in opt
    sc.view_settings.view_transform = 'Standard'

info = dict(stat, nap_s=round(T_LOAD, 1), sun_el=round(sun_el, 2), blender=bpy.app.version_string, night=NIGHT)

# ================================================================= VIỆC
if JOB in ('cycles', 'eevee'):
    if JOB == 'cycles': cycles(int(opt.get('--spp', 16)), bounces=tuple(int(x) for x in opt.get('--bounces', '8,6,6').split(',')))
    else:
        sc.render.engine = 'BLENDER_EEVEE'; ee = sc.eevee
        for nm, v in (('taa_render_samples', int(opt.get('--spp', 32))), ('use_shadows', True), ('use_raytracing', True), ('shadow_ray_count', 1), ('shadow_step_count', 6), ('use_volumetric_shadows', False)):
            if hasattr(ee, nm): setattr(ee, nm, v)
        if hasattr(ee, 'ray_tracing_options'):
            ro = ee.ray_tracing_options
            for nm, v in (('resolution_scale', '2'), ('use_denoise', True)):
                if hasattr(ro, nm):
                    try: setattr(ro, nm, v)
                    except Exception: pass
        sc.view_settings.view_transform = 'Standard'
    sc.render.image_settings.file_format = 'OPEN_EXR'; sc.render.image_settings.color_depth = '16' if '--half' in opt else '32'; sc.render.film_transparent = False
    frames = [None]
    if '--anim' in opt:   # đường máy: [{f, p:[E,cao,N], l:[E,cao,N], fov}] (toạ độ ENU như k2v) — một EXR mỗi khung
        A = json.load(open(opt['--anim'])); fr = opt.get('--frames'); lo, hi = (map(int, fr.split(':')) if fr else (0, len(A['keys']) - 1))
        frames = [k for k in A['keys'] if lo <= k['f'] <= hi]
        # MOTION BLUR: khung hoá máy ở MỌI khung lân cận (lo − 1 … hi + 1) để Cycles nội suy chuyển động trong màn trập 180°
        KD = {k['f']: k for k in A['keys']}
        for f in range(lo - 1, hi + 2):
            k = KD.get(f)
            if not k: continue
            p = mathutils.Vector((k['p'][0], k['p'][2], k['p'][1])); l = mathutils.Vector((k['l'][0], k['l'][2], k['l'][1]))
            cob.location = p; cob.rotation_euler = (l - p).to_track_quat('-Z', 'Y').to_euler(); cam.angle_y = math.radians(k.get('fov', 40))
            cob.keyframe_insert('location', frame=f); cob.keyframe_insert('rotation_euler', frame=f); cam.keyframe_insert('lens', frame=f)
        if cob.animation_data and cob.animation_data.action:
            for fc in getattr(cob.animation_data.action, 'fcurves', []): 
                for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
    if '--mb' in opt: sc.render.use_motion_blur = True; sc.render.motion_blur_shutter = float(opt.get('--shutter', 0.5)); sc.render.motion_blur_position = 'CENTER' if hasattr(sc.render, 'motion_blur_position') else None
    FXDIR = opt.get('--fxdir')
    times = []
    for k in frames:
        if k is not None:
            sc.frame_set(k['f']); DOF_L[0] = mathutils.Vector((k['l'][0], k['l'][2], k['l'][1]))
            if FXDIR and os.path.exists(os.path.join(FXDIR, f"{k['f']:05d}.json")):   # khói/lửa + ánh sáng k2v của ĐÚNG khung này
                fj = os.path.join(FXDIR, f"{k['f']:05d}.json"); set_light(json.load(open(fj)))
                for ob in FX:   # xoá cả dữ liệu (lưới sao chép, đèn) — lượt 1 chỉ xoá vật → rò bộ nhớ, hết VRAM 32 GB ở khung 442 (--persist)
                    d_ = ob.data; bpy.data.objects.remove(ob)
                    if d_ is not None and d_.users == 0: (bpy.data.meshes if isinstance(d_, bpy.types.Mesh) else bpy.data.lights).remove(d_)
                FX.clear()
                if '--fx' in opt: add_fx(fj)
            t = k['f'] / 24.0
            for w in list(WN) + SMOKE:
                if 'W' in w.inputs: w.inputs['W'].default_value = t * 0.15
            for fo, lo_, f in FIRE_OBJ:   # nhấp nháy lửa tất định
                if lo_ is None: continue
                ff = 0.8 + 0.2 * math.sin(t * 7.1 + f['at'][0] * 0.01) * math.sin(t * 3.3 + f['at'][1] * 0.013); lo_.data.energy = f.get('W', 2.5e6) * (f.get('size', 30) / 30) * ff
            sc.render.filepath = os.path.join(OUT, f"{k['f']:05d}.exr")
        else: sc.render.filepath = OUT
        fd = set_dof()
        t1 = time.time(); bpy.ops.render.render(write_still=True); times.append(round(time.time() - t1, 2))
        if fd: info['dof_m'] = round(fd, 1)
        print('NC-RENDER', JOB, k['f'] if k else '-', times[-1], flush=True)
    info.update(job=JOB, spp=int(opt.get('--spp', 16 if JOB == 'cycles' else 32)), res=[W, H], render_s=times, threads=TH)
    json.dump(info, open((OUT if not frames[0] else os.path.join(OUT, f"nc-{frames[0]['f']:05d}")) + '.json', 'w'), ensure_ascii=False)
    print('NC-BLEND', json.dumps(info, ensure_ascii=False))

elif JOB == 'nuong':
    """nướng: R trời, G nảy nắng, (B lửa) vào ảnh phẳng hộp box; mỗi lượt một ảnh float rồi gộp."""
    box = [float(x) for x in opt['--box'].split(',')]; br = float(opt.get('--bres', 2.0)); BW = int(round((box[2] - box[0]) / br)); BH = int(round((box[3] - box[1]) / br))
    spp = int(opt.get('--spp', 64)); cycles(spp, denoise=False, bounces=(3, 3, 0))
    # bỏ phần VÁY chồng mép của mỗi ô 1 km (terrain.js chunk(): mở rộng ±1 bước) — không thì mép ô bị ô kề che → đường xám lưới 1 km trong ảnh nướng
    import bmesh
    for ob in TERR:
        co = np.zeros(len(ob.data.vertices) * 3, np.float32); ob.data.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
        ex = co[:, 0].max() - co[:, 0].min()
        if ex > 1100: continue   # lưới ngoài/toàn vùng: giữ
        cx, cy = co[:, 0].mean(), co[:, 1].mean(); e0 = -3000 + math.floor((cx + 3000) / 1000) * 1000; n0 = -5500 + math.floor((cy + 5500) / 1000) * 1000
        bm = bmesh.new(); bm.from_mesh(ob.data); dl = [f for f in bm.faces if not (e0 <= f.calc_center_median().x <= e0 + 1000 and n0 <= f.calc_center_median().y <= n0 + 1000)]
        bmesh.ops.delete(bm, geom=dl, context='FACES'); bm.to_mesh(ob.data); bm.free()
    # UV phẳng cho mọi ô địa hình
    for ob in TERR:
        me = ob.data; uv = me.uv_layers.new(name='bake'); co = np.zeros(len(me.vertices) * 3, np.float32); me.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
        li = np.zeros(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', li); U = (co[li, 0] - box[0]) / (box[2] - box[0]); V = (co[li, 1] - box[1]) / (box[3] - box[1])
        uv.data.foreach_set('uv', np.stack([U, V], 1).ravel().astype(np.float32)); me.uv_layers.active = uv
    # chỉ giữ ô địa hình có phần trong hộp
    tgt = []
    for ob in TERR:
        co = np.zeros(len(ob.data.vertices) * 3, np.float32); ob.data.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
        if ((co[:, 0] > box[0]) & (co[:, 0] < box[2]) & (co[:, 1] > box[1]) & (co[:, 1] < box[3])).any(): tgt.append(ob)
    gm = MATS['dia_hinh']; nt = gm.node_tree; bi = N(nt, 'ShaderNodeTexImage'); nt.nodes.active = bi
    WATER.hide_render = True   # nước không tham gia nảy (k2v: nước vẽ riêng)
    res = {}
    def bake(name, filt):
        im = bpy.data.images.new('bk_' + name, BW, BH, float_buffer=True, alpha=False); bi.image = im
        bpy.ops.object.select_all(action='DESELECT')
        for ob in tgt: ob.select_set(True)
        bpy.context.view_layer.objects.active = tgt[0]
        t1 = time.time(); bpy.ops.object.bake(type='DIFFUSE', pass_filter=filt, margin=4, use_clear=True, target='IMAGE_TEXTURES')
        a = np.array(im.pixels[:], np.float32).reshape(BH, BW, 4)[::-1, :, :3].mean(2); res[name] = (a, round(time.time() - t1, 1)); print('NC-BAKE', name, res[name][1], 's', flush=True)
    # (1) TRỜI: vòm trên trắng đều L = 1/π (bức xạ mặt phẳng trống = 1), dưới chân trời đen; không nắng
    for n_ in list(wnt.nodes): wnt.nodes.remove(n_)
    tc = wnt.nodes.new('ShaderNodeTexCoord'); sx = wnt.nodes.new('ShaderNodeSeparateXYZ'); gt = wnt.nodes.new('ShaderNodeMath'); gt.operation = 'GREATER_THAN'; gt.inputs[1].default_value = 0.0
    mu = wnt.nodes.new('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = 1 / math.pi
    bg2 = wnt.nodes.new('ShaderNodeBackground'); wo2 = wnt.nodes.new('ShaderNodeOutputWorld'); L = wnt.links
    L.new(tc.outputs['Generated'], sx.inputs[0]); L.new(sx.outputs['Z'], gt.inputs[0]); L.new(gt.outputs[0], mu.inputs[0]); L.new(mu.outputs[0], bg2.inputs['Strength']); L.new(bg2.outputs[0], wo2.inputs[0]); bg2.inputs['Color'].default_value = (1, 1, 1, 1)
    sl.energy = 0
    for fo, lo_, f in FIRE_OBJ:
        fo.hide_render = True
        if lo_: lo_.hide_render = True
    bake('sky', {'DIRECT', 'INDIRECT'})
    # (2) NẮNG: chỉ nảy (gián tiếp) + trực tiếp làm mốc chuẩn hoá; trời đen
    bg2.inputs['Color'].default_value = (0, 0, 0, 1); sl.energy = 1.0; sl.color = (1, 1, 1)
    bake('sun_ind', {'INDIRECT'}); bake('sun_dir', {'DIRECT'})
    # (3) LỬA (nếu có): đèn điểm lửa, không nắng/trời
    if FIRE_OBJ:
        sl.energy = 0
        for fo, lo_, f in FIRE_OBJ:
            if lo_: lo_.hide_render = False
        bake('fire', {'DIRECT', 'INDIRECT'})
    sky = res['sky'][0]; kS = float(np.percentile(sky, 99.5)) or 1.0
    dirf = res['sun_dir'][0]; kD = float(np.percentile(dirf, 99.5)) or 1.0   # mặt phẳng trống: I·cos(zenith)·c
    cz = max(0.05, sd.z); G = res['sun_ind'][0] / kD * cz   # nảy ÷ bức xạ nắng pháp tuyến
    Rch = np.clip(sky / kS, 0, 1); Gch = np.clip(G * 4.0, 0, 1)
    Bch = np.zeros_like(Rch); fpk = 0.0
    if 'fire' in res: fa = res['fire'][0]; fpk = float(np.percentile(fa, 99.9)) or 1.0; Bch = np.clip(fa / fpk, 0, 1)
    # A: cao độ mặt đất (pack terrain.f32 nội suy theo ô ảnh) ÷ 600
    pk = json.load(open(os.path.join(opt['--pack'], 'meta.json'))); Hh = np.fromfile(os.path.join(opt['--pack'], 'terrain.f32'), np.float32).reshape(pk['terrain_shape'])
    e0, n0, e1, n1 = pk['ext']; stp = pk['step_terrain']; ee = box[0] + (np.arange(BW) + 0.5) * br; nn = box[3] - (np.arange(BH) + 0.5) * br
    fc = np.clip((ee - e0) / stp, 0, Hh.shape[1] - 1.001); fr = np.clip((n1 - nn) / stp, 0, Hh.shape[0] - 1.001); c0 = fc.astype(int); r0 = fr.astype(int); ax = fc - c0; ay = fr - r0
    hh = (Hh[r0][:, c0] * (1 - ax) + Hh[r0][:, c0 + 1] * ax) * (1 - ay)[:, None] + (Hh[r0 + 1][:, c0] * (1 - ax) + Hh[r0 + 1][:, c0 + 1] * ax) * ay[:, None]
    Ach = np.clip(hh / 600.0, 0, 1)
    import imageio.v3 as iio
    os.makedirs(OUT, exist_ok=True); rgba = (np.dstack([Rch, Gch, Bch, Ach]) * 255 + 0.5).astype(np.uint8); iio.imwrite(os.path.join(OUT, 'bake.png'), rgba)
    for nm, (arr, s_) in res.items(): np.save(os.path.join(OUT, f'raw_{nm}.npy'), arr.astype(np.float16))
    meta = dict(box=box, res_m=br, px=[BW, BH], spp=spp, sun_dir=[float(x) for x in (S.inverted() @ sd.to_4d()).to_3d()], sun_el=round(sun_el, 2), g_scale=0.25, fire_peak=fpk, norm=dict(sky_p995=kS, dir_p995=kD),
                bake_s={k: v[1] for k, v in res.items()}, tong_s=round(time.time() - T0, 1), nap_s=round(T_LOAD, 1), o_dia_hinh=len(tgt), threads=TH, blender=bpy.app.version_string,
                kenh='R trời/mặt phẳng trống · G nảy nắng ×4 · B lửa/đỉnh · A cao/600 m', stat=stat)
    json.dump(meta, open(os.path.join(OUT, 'meta.json'), 'w'), ensure_ascii=False); print('NC-BAKE-XONG', json.dumps({k: meta[k] for k in ('bake_s', 'tong_s', 'px')}))
