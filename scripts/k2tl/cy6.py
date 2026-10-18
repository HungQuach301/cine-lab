"""V6 bước 7 (phương án A) · BẢN TỐT NHẤT: dựng khung k2v bằng Blender Cycles trên CÙNG hình học + CÙNG máy + CÙNG mặt trời/trời (xuất bằng scripts/k2tl/export6.js).
  /opt/bpy/bin/python scripts/k2tl/cy6.py <thư mục xuất> <ra.exr> [--spp 192] [--threads 3] [--res 1920x1080] [--cc0 <thư mục vân CC0>]
Cycles tính ÁNH SÁNG THẬT (mặt trời mềm 0,53°, trời bán cầu khớp ánh trời k2v, GI 4 nảy, AO thật, bóng mềm) trên vật liệu khuếch tán xám theo loại vật
(albedo GI hợp lý); màu bề mặt cuối = albedo k2v (lượt albedo không chiếu sáng — gồm vân thủ tục, cửa sổ, vân HC7) × ánh sáng Cycles (ghép ở cy6_ghep.py).
Vân CC0 (Poly Haven, nếu có --cc0): bản đồ pháp tuyến/độ gồ cho mái ngói, tường vữa, đá công sự, đất → vi chi tiết bóng đổ trong lượt ánh sáng.
Nước: mặt phẳng z = 0 kiểu HOLDOUT (che phần ngập, trong suốt) — nước/trời/khói lấy từ k2v. Ra: EXR Combined (khử nhiễu OIDN, alpha) + <ra>-aux.exr (R = albedo GI, G = độ sâu Z/1000; xem lượt phụ)."""
import sys, os, json, math, time
import numpy as np
import bpy, mathutils

a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
D, OUT = a[0], a[1]
opt = {k: v for k, v in zip(a[2::2], a[3::2])}
SPP = int(opt.get('--spp', 192)); TH = int(opt.get('--threads', 3)); RES = opt.get('--res'); CC0 = opt.get('--cc0'); AUX = opt.get('--aux', '0')   # --aux only: chỉ dựng lượt phụ
t0 = time.time()
M = json.load(open(os.path.join(D, 'manifest.json')))
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
S = mathutils.Matrix(((1, 0, 0, 0), (0, 0, -1, 0), (0, 1, 0, 0), (0, 0, 0, 1)))   # three (x E, y cao, z −N) → Blender (x E, y N, z cao)
def load(i):
    meta = M['bufs'][i]; dt = {'Float32Array': np.float32, 'Uint32Array': np.uint32, 'Uint16Array': np.uint16}[meta['type']]
    return np.fromfile(os.path.join(D, f'b{i}.bin'), dtype=dt)
# ---------- vật liệu theo loại (albedo GI) ----------
ALB = {'dia_hinh': 0.32, 'nha': 0.58, 'cong_su': 0.55, 'nguoi': 0.42, 'cay': 0.18, 'khac': 0.45, 'tau': 0.22, 'do_nat': 0.52}
def mat(kind):
    name = 'm_' + kind
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    v = ALB.get(kind, 0.45); b.inputs['Base Color'].default_value = (v, v, v, 1); b.inputs['Roughness'].default_value = 0.92
    for k in ('Specular IOR Level', 'Specular'):
        if k in b.inputs: b.inputs[k].default_value = 0.08
    if CC0 and kind in ('nha', 'cong_su', 'dia_hinh', 'do_nat'):   # vi chi tiết CC0 (pháp tuyến), toạ độ tam phẳng theo thế giới
        f = {'nha': 'plaster', 'cong_su': 'stone', 'dia_hinh': 'ground', 'do_nat': 'stone'}[kind]; p = os.path.join(CC0, f + '_nor.jpg')
        if os.path.exists(p):
            im = nt.nodes.new('ShaderNodeTexImage'); im.image = bpy.data.images.load(p); im.image.colorspace_settings.name = 'Non-Color'; im.projection = 'BOX'; im.projection_blend = 0.3
            mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (0.35, 0.35, 0.35); nm = nt.nodes.new('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value = 0.8
            tco = nt.nodes.new('ShaderNodeNewGeometry'); nt.links.new(tco.outputs['Position'], mp.inputs['Vector'])
            nt.links.new(mp.outputs['Vector'], im.inputs['Vector']); nt.links.new(im.outputs['Color'], nm.inputs['Color']); nt.links.new(nm.outputs['Normal'], b.inputs['Normal'])
    return m
def mesh_from(P, I, name):
    me = bpy.data.meshes.new(name); n = len(P) // 3
    V = P.reshape(-1, 3)[:, [0, 2, 1]] * np.array([1, -1, 1], np.float32)   # (x, y, z)three → (x, −z, y)
    if I is None: I = np.arange(n, dtype=np.uint32)
    I = I.reshape(-1, 3)
    me.vertices.add(n); me.vertices.foreach_set('co', V.ravel())
    nl = len(I); me.loops.add(nl * 3); me.loops.foreach_set('vertex_index', I.ravel().astype(np.int32))
    me.polygons.add(nl); me.polygons.foreach_set('loop_start', np.arange(0, nl * 3, 3, dtype=np.int32)); me.polygons.foreach_set('loop_total', np.full(nl, 3, np.int32))
    me.update(calc_edges=False); me.validate(clean_customdata=False)
    me.polygons.foreach_set('use_smooth', np.zeros(nl, bool)); return me
col = bpy.data.collections.new('k2v'); sc.collection.children.link(col); base_col = bpy.data.collections.new('k2v_goc'); sc.collection.children.link(base_col)
stat = {'vat': 0, 'tam_giac': 0, 'ban_sao': 0}
for k, o in enumerate(M['objs']):
    P = load(o['buf']['P']); I = load(o['buf']['I']) if 'I' in o['buf'] else None
    me = mesh_from(P, I, f"o{k}_{o['kind']}"); me.materials.append(mat(o['kind']))
    if 'M' in o['buf']:   # bản sao: lưới gốc (ẩn) + đám điểm có rot/scale → Geometry Nodes Instance on Points
        base = bpy.data.objects.new(f"goc{k}", me); base_col.objects.link(base)
        Mx = load(o['buf']['M']).reshape(-1, 16); pts, rot, scl = [], [], []
        for e in Mx:
            m3 = mathutils.Matrix([e[0:4], e[4:8], e[8:12], e[12:16]]).transposed(); mb = S @ m3 @ S.inverted(); lo, ro, sc_ = mb.decompose()
            pts.append(lo); rot.append(ro.to_euler()); scl.append(sc_)
        pm = bpy.data.meshes.new(f"pts{k}"); pm.vertices.add(len(pts)); pm.vertices.foreach_set('co', np.array(pts, np.float32).ravel())
        ra = pm.attributes.new('rot', 'FLOAT_VECTOR', 'POINT'); ra.data.foreach_set('vector', np.array([tuple(r) for r in rot], np.float32).ravel())
        sa = pm.attributes.new('scl', 'FLOAT_VECTOR', 'POINT'); sa.data.foreach_set('vector', np.array([tuple(s) for s in scl], np.float32).ravel())
        ob = bpy.data.objects.new(f"inst{k}_{o['kind']}", pm); col.objects.link(ob)
        gm = ob.modifiers.new('ban_sao', 'NODES'); ng = bpy.data.node_groups.new(f'gn{k}', 'GeometryNodeTree'); gm.node_group = ng
        ng.interface.new_socket('Geometry', in_out='INPUT', socket_type='NodeSocketGeometry'); ng.interface.new_socket('Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
        gi = ng.nodes.new('NodeGroupInput'); go = ng.nodes.new('NodeGroupOutput'); mtp = ng.nodes.new('GeometryNodeMeshToPoints'); iop = ng.nodes.new('GeometryNodeInstanceOnPoints'); oi = ng.nodes.new('GeometryNodeObjectInfo'); oi.inputs['Object'].default_value = base
        rr = ng.nodes.new('GeometryNodeInputNamedAttribute'); rr.data_type = 'FLOAT_VECTOR'; rr.inputs['Name'].default_value = 'rot'
        ss = ng.nodes.new('GeometryNodeInputNamedAttribute'); ss.data_type = 'FLOAT_VECTOR'; ss.inputs['Name'].default_value = 'scl'
        L = ng.links; L.new(gi.outputs[0], mtp.inputs['Mesh']); L.new(mtp.outputs['Points'], iop.inputs['Points']); L.new(oi.outputs['Geometry'], iop.inputs['Instance'])
        L.new(rr.outputs['Attribute'], iop.inputs['Rotation']); L.new(ss.outputs['Attribute'], iop.inputs['Scale']); L.new(iop.outputs['Instances'], go.inputs[0])
        stat['ban_sao'] += len(pts)
    else:
        ob = bpy.data.objects.new(f"o{k}_{o['kind']}", me); col.objects.link(ob)
    stat['vat'] += 1; stat['tam_giac'] += o['nt'] * (o.get('inst') or 1)
base_col.hide_render = True
# nước: mặt phẳng holdout z = 0 (che phần ngập dưới mực nước như k2v; điểm ảnh nước lấy từ k2v)
bpy.ops.mesh.primitive_plane_add(size=60000, location=(0, 0, 0)); wp = bpy.context.active_object; wm = bpy.data.materials.new('holdout'); wm.use_nodes = True
wm.node_tree.nodes.clear(); ho = wm.node_tree.nodes.new('ShaderNodeHoldout'); out = wm.node_tree.nodes.new('ShaderNodeOutputMaterial'); wm.node_tree.links.new(ho.outputs[0], out.inputs['Surface']); wp.data.materials.append(wm)
# máy
C = M['cam']; cam = bpy.data.cameras.new('cam'); cob = bpy.data.objects.new('cam', cam); sc.collection.objects.link(cob); sc.camera = cob
q = C['quat']; m3 = mathutils.Quaternion((q[3], q[0], q[1], q[2])).to_matrix().to_4x4(); m3.translation = mathutils.Vector(C['pos']); cob.matrix_world = S @ m3
cam.sensor_fit = 'VERTICAL'; cam.angle_y = math.radians(C['fov']); cam.clip_start = C['near']; cam.clip_end = C['far']
W, H = (C['W'], C['H']) if not RES else map(int, RES.split('x')); sc.render.resolution_x, sc.render.resolution_y = W, H; sc.render.resolution_percentage = 100
# mặt trời: hướng TỚI mặt trời (three) → đèn chiếu ngược lại; cường độ = intensity (cùng công thức Lambert I·cosθ/π)
Su = M['sun']; sd = (S @ mathutils.Vector((*Su['dir'], 0)).to_4d()).to_3d().normalized(); sl = bpy.data.lights.new('sun', 'SUN'); sl.energy = Su['intensity']; sl.color = Su['color'][:3]; sl.angle = math.radians(0.53)
so = bpy.data.objects.new('sun', sl); sc.collection.objects.link(so); so.rotation_euler = sd.to_track_quat('Z', 'Y').to_euler()
# trời bán cầu: radiance L = hemiI·màu/π (khớp ánh trời Lambert của k2v), trộn theo z hướng nhìn
Hm = M['hemi']; w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; nt = w.node_tree; nt.nodes.clear()
tc = nt.nodes.new('ShaderNodeTexCoord'); sx = nt.nodes.new('ShaderNodeSeparateXYZ'); mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = -1; mr.inputs['From Max'].default_value = 1
mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; bg = nt.nodes.new('ShaderNodeBackground'); wo = nt.nodes.new('ShaderNodeOutputWorld')
k = Hm['intensity'] / math.pi; mx.inputs[6].default_value = (*[c * k for c in Hm['ground']], 1); mx.inputs[7].default_value = (*[c * k for c in Hm['sky']], 1)
L = nt.links; L.new(tc.outputs['Generated'], sx.inputs[0]); L.new(sx.outputs['Z'], mr.inputs['Value']); L.new(mr.outputs['Result'], mx.inputs['Factor']); L.new(mx.outputs[2], bg.inputs['Color']); L.new(bg.outputs[0], wo.inputs[0])
# Cycles
sc.render.engine = 'CYCLES'; cy = sc.cycles; cy.device = 'CPU'; cy.samples = SPP; cy.use_denoising = True; cy.denoiser = 'OPENIMAGEDENOISE'; cy.max_bounces = 4; cy.diffuse_bounces = 4; cy.glossy_bounces = 1; cy.transparent_max_bounces = 4
cy.use_adaptive_sampling = True; cy.adaptive_threshold = 0.01; sc.render.film_transparent = True; sc.render.threads_mode = 'FIXED'; sc.render.threads = TH
sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'
vl = sc.view_layers[0]; vl.use_pass_diffuse_color = True; vl.use_pass_z = True; vl.use_pass_combined = True
(setattr(sc.render.image_settings, 'media_type', 'MULTI_LAYER_IMAGE') if hasattr(sc.render.image_settings, 'media_type') else None); sc.render.image_settings.file_format = 'OPEN_EXR_MULTILAYER'; sc.render.image_settings.color_depth = '32'; sc.render.filepath = OUT
t1 = time.time()
if AUX != 'only': bpy.ops.render.render(write_still=True)
t2 = time.time()
# LƯỢT PHỤ (Blender 5.2 bpy KHÔNG ghi DiffCol/Depth vào EXR đa lớp — đã thử write_still, save_render, nút File Output): dựng lại 4 spp, vật liệu PHÁT XẠ
#  R = albedo GI của loại vật (= DiffCol), G = độ sâu nhìn Z/1000 (cùng định nghĩa sương FogExp2 của three), không nảy, không khử nhiễu → <ra>-aux.exr (Combined, nhân alpha)
for m in [m for m in bpy.data.materials if m.name.startswith('m_')]:
    nt = m.node_tree; v = ALB.get(m.name[2:], 0.45); cd = nt.nodes.new('ShaderNodeCameraData'); mt = nt.nodes.new('ShaderNodeMath'); mt.operation = 'MULTIPLY'; mt.inputs[1].default_value = 1e-3
    cc = nt.nodes.new('ShaderNodeCombineColor'); cc.inputs[0].default_value = v; em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Strength'].default_value = 1
    nt.links.new(cd.outputs['View Z Depth'], mt.inputs[0]); nt.links.new(mt.outputs[0], cc.inputs[1]); nt.links.new(cc.outputs[0], em.inputs['Color'])
    nt.links.new(em.outputs[0], [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'][0].inputs['Surface'])
bg.inputs['Strength'].default_value = 0; sl.energy = 0
cy.samples = 4; cy.use_denoising = False; cy.use_adaptive_sampling = False; cy.max_bounces = 0
sc.render.filepath = OUT[:-4] + '-aux.exr'; bpy.ops.render.render(write_still=True); t3 = time.time()
json.dump(dict(stat, spp=SPP, threads=TH, res=[W, H], nap_s=round(t1 - t0, 1), dung_s=round(t2 - t1, 1), phu_s=round(t3 - t2, 1), blender=bpy.app.version_string), open(OUT + ('.aux.json' if AUX == 'only' else '.json'), 'w'), ensure_ascii=False)
print('CY6', json.dumps(dict(stat, nap_s=round(t1 - t0, 1), dung_s=round(t2 - t1, 1), phu_s=round(t3 - t2, 1))))
