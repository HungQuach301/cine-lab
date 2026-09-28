# Cine Lab · Cửa mặt Ida lượt 2 (W4) — phép thử khả thi MPFB2 không giao diện.
# /opt/bpy/bin/python mpfb_try.py -- <thư mục mpfb2 (repo clone)> <ảnh ra.png>
# Tạo người nữ ~70 tuổi bằng HumanService.create_human (tài sản lõi CC0), render EEVEE chính diện.
import sys, os, math, time
argv = sys.argv[sys.argv.index('--') + 1:]
MP, OUTP = argv[0], argv[1]
import bpy, addon_utils, importlib
t0 = time.time()
bpy.ops.wm.read_factory_settings(use_empty=True)
# cài như extension ở kho người dùng (symlink tới repo clone) rồi bật — cách MPFB chạy chuẩn trong Blender 4.2+
ext = bpy.utils.user_resource('EXTENSIONS', path='user_default', create=True)
dst = os.path.join(ext, 'mpfb')
if not os.path.exists(dst): os.symlink(os.path.join(MP, 'src', 'mpfb'), dst)
bpy.ops.extensions.repo_refresh_all() if hasattr(bpy.ops.extensions, 'repo_refresh_all') else None
addon_utils.enable('bl_ext.user_default.mpfb', default_set=True, handle_error=None)
HumanService = importlib.import_module('bl_ext.user_default.mpfb.services.humanservice').HumanService
TargetService = importlib.import_module('bl_ext.user_default.mpfb.services.targetservice').TargetService
macro = TargetService.get_default_macro_info_dict()
print('MACRO mặc định', macro)
macro.update({'gender': 0.0, 'age': 0.94, 'muscle': 0.35, 'weight': 0.5})
h = HumanService.create_human(macro_detail_dict=macro, scale=0.1)
print('HUMAN', h.name, len(h.data.vertices), 'đỉnh; shape keys', [k.name for k in h.data.shape_keys.key_blocks] if h.data.shape_keys else None, f'{time.time() - t0:.1f}s')
SC = bpy.context.scene
SC.render.engine = 'BLENDER_EEVEE'; SC.render.resolution_x = 540; SC.render.resolution_y = 720
wd = bpy.data.worlds.new('w'); wd.use_nodes = True; wd.node_tree.nodes['Background'].inputs['Color'].default_value = (0.08, 0.08, 0.09, 1); SC.world = wd
import mathutils
bb = [h.matrix_world @ mathutils.Vector(c) for c in h.bound_box]; top = max(v.z for v in bb)
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); SC.collection.objects.link(cam); SC.camera = cam
cam.data.lens = 85; cam.location = (0, -1.6, top - 0.12); cam.rotation_euler = (math.radians(90), 0, 0)
for nm, loc, e in [('key', (0.8, -1.2, top + 0.3), 120), ('fill', (-1.0, -0.8, top - 0.1), 30)]:
    L = bpy.data.objects.new(nm, bpy.data.lights.new(nm, 'POINT')); L.data.energy = e; L.location = loc; SC.collection.objects.link(L)
SC.render.filepath = OUTP; bpy.ops.render.render(write_still=True)
print('XONG', f'{time.time() - t0:.1f}s', 'đỉnh cao', top)
