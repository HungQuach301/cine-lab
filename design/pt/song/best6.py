"""V6 · KHUNG NEO bản TỐT NHẤT (phương án A của chủ dự án: Cycles cao nhất cho cùng hình học/máy): dựng lại CHÍNH cảnh build_scene.py
(cùng mã, cùng hạt giống) ở lượt trưa d2 với spp cao + OIDN, và đặt NGƯỜI LÀ LƯỚI 3D (nguoi6/mh_people6 — người tự dựng, cùng mẫu với sprite)
trong cảnh theo đúng kế hoạch người của khung trưa bản sản xuất (live6.py --plan). Bản sao người dùng chung lưới (linked data) + khung xương riêng.
Người mang mã lớp 9560 (BẢO VỆ khi ghép LAI). Ra: d2.png, depth.exr, cls.exr, meta.json (như build_scene).
  PT6=1 PT_CAM=k1782|pt PT_THREADS=2 /opt/bpy/bin/python best6.py -- --epoch 1943 --plan plan.json --key 1943-trua --out DIR --spp 256"""
import sys, os, json, math, random, time
HERE = os.path.dirname(os.path.abspath(__file__))
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
def arg(k, d=None): return argv[argv.index(k) + 1] if k in argv else d
EP = int(arg('--epoch')); PLAN = arg('--plan'); KEY = arg('--key'); OUT = arg('--out'); SPP = arg('--spp', '256'); T0 = time.time()
people = json.load(open(PLAN))[KEY]
STATS = {}

def add_people():
    import bpy
    from mathutils import Vector
    head = {1782: 268.7, 1943: 281.0}[EP]
    src = open(os.path.join(HERE, 'mh_people6.py')).read(); pre = src[:src.index('\nfor role in roles:')]
    old = sys.argv; sys.argv = ['mh_people6.py', '--', '--epoch', str(EP), '--head', str(head), '--roles', 'linh', '--out', os.path.join(OUT, '_tmp')]
    ns = {'__name__': 'mh6', '__file__': os.path.join(HERE, 'mh_people6.py')}; exec(compile(pre, ns['__file__'], 'exec'), ns); sys.argv = old
    sc = bpy.context.scene; ROLES = ns['ROLES']; protos = {}; t0 = time.time()
    def tag_cls(o):
        me = o.data
        if me is None or 'cls' in me.attributes: return
        a = me.attributes.new('cls', 'FLOAT', 'FACE')
        for d in a.data: d.value = float(9560 * 64 + 1)
    def proto(rl, b_):
        k = (rl, b_)
        if k not in protos:
            R = ROLES[rl]; body, objs, skin, hair = ns['build_person'](rl, R, b_, f'Q{len(protos)}')
            ao, parts = ns['rig_person'](body, objs, R, f'Q{len(protos)}', b_, b_ in R.get('nohat_b', ()))
            for o, _, _ in objs: o.hide_render = True; tag_cls(o)
            for p in parts: p.hide_render = True; tag_cls(p)
            ao.hide_render = True; protos[k] = (ao, parts, objs, R)
        return protos[k]
    rr = random.Random(EP); n = 0
    for i, P in enumerate(people):
        rk = P['rk']; d = Vector((P['dir'][0], P['dir'][1], 0)).normalized(); yaw = math.atan2(d.y, d.x) - math.atan2(-1, 0)
        if rk == 'khieng':
            R0 = ROLES['khieng']; ph = int(P['pose'][1:]) if P['pose'][1:].isdigit() else 0
            mem = [(R0['pair'], 0, f'cbarrow{ph}', 0.85), (R0['pair'], 1, f'cbarrow{(ph + 4) % 8}', -0.85)]
        else:
            role, b_ = rk.split('~'); mem = [(role, int(b_), P['pose'], 0.0)]
        for (rl, b_, pn, off) in mem:
            ao, parts, objs, R = proto(rl, b_); ns['pose'](ao, pn, R, rr); its = ns['items'](ao, R, pn) if rk != 'khieng' else []
            dg = bpy.context.evaluated_depsgraph_get(); zmin = 9.0
            for o, _, _ in objs:
                if 'giay' in o.name or 'than' in o.name or 'vay' in o.name:
                    me_ = o.evaluated_get(dg).to_mesh(); zmin = min(zmin, min(v_.co.z for v_ in me_.vertices)); o.evaluated_get(dg).to_mesh_clear()
            basis = {pb.name: pb.matrix_basis.copy() for pb in ao.pose.bones}
            a2 = ns['clone'](ao, parts, objs, f'N{i}_{rl}')
            for bn, mb in basis.items(): a2.pose.bones[bn].matrix_basis = mb
            for p in its:
                p2 = p.copy(); sc.collection.objects.link(p2); p2.parent = a2; p2.hide_render = False; tag_cls(p2)
            for p in its: bpy.data.objects.remove(p, do_unlink=True)
            pos = Vector((P['x'], P['y'], 0)) + d * off
            a2.location = (pos.x, pos.y, -zmin * P['sc'] + 0.004); a2.rotation_euler = (0, 0, yaw); a2.scale = (P['sc'],) * 3; n += 1
        if rk == 'khieng':
            c = Vector((P['x'], P['y'], 0.5)); item = ns['prim']('cyl' if EP == 1782 else 'cube', c, (0.27, 0.27, 0.36) if EP == 1782 else (0.4, 0.3, 0.24), (0.32, 0.22, 0.13),
                                                               (0, math.pi / 2, yaw + math.pi / 2) if EP == 1782 else (0, 0, yaw), 'wood'); tag_cls(item)
    bpy.context.view_layer.update()
    if os.environ.get('BEST_BORDER'):   # dựng theo dải ngang (mỗi lần ≤ 29 phút theo lệnh phiên chính) rồi ghép (best_ghep6.py)
        y0, y1 = map(float, os.environ['BEST_BORDER'].split(',')); sc.render.use_border = True; sc.render.use_crop_to_border = False
        sc.render.border_min_x, sc.render.border_max_x, sc.render.border_min_y, sc.render.border_max_y = 0.0, 1.0, y0, y1; STATS['dai'] = [y0, y1]
    STATS.update(nguoi=n, mau=len(protos), dung_s=round(time.time() - t0, 1)); print('NGUOI3D', STATS, flush=True)

src = open(os.path.join(HERE, '..', 'scene', 'build_scene.py')).read()
mark = "LOG['setup_s'] = round(time.time() - T0, 1); LOG['renders'] = []"
assert mark in src
src = src.replace(mark, "__HOOK__(); LOG['nguoi3d'] = __STATS__\n" + mark)
sys.argv = ['build_scene.py', '--', '--epoch', str(EP), '--tex', 'A', '--passes', 'd2', '--res', '1920x1080', '--spp', SPP, '--depth', '--clspass', '--out', OUT]
G = {'__name__': '__main__', '__file__': os.path.join(HERE, '..', 'scene', 'build_scene.py'), '__HOOK__': add_people, '__STATS__': STATS}
sys.path.insert(0, os.path.join(HERE, '..', 'scene'))
exec(compile(src, G['__file__'], 'exec'), G)
print('BEST DONE', round(time.time() - T0, 1))
