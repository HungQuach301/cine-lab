"""NC-GPU · chạy NGUYÊN VĂN design/pt/cpu/nc_blend.py (cảnh B của NC-CPU) trên GPU để đo hệ số GPU/CPU trên CÙNG tệp, CÙNG cài đặt (16 spp + OIDN, adaptive 0,02, nảy 4/3/2).
Chỉ đổi 2 chỗ khi nạp (không sửa tệp gốc): (1) sau read_factory_settings bật thiết bị Cycles (OPTIX, dự phòng CUDA); (2) cy.device = 'GPU'. Mọi thứ khác giữ nguyên.
  blender -b --factory-startup --python-exit-code 1 -P nc_gpu_compat.py -- <như nc_blend.py> [--ncsrc <đường nc_blend.py>] [--gpudev OPTIX|CUDA|CPU]"""
import sys, os, bpy
a = sys.argv[sys.argv.index('--') + 1:]
src = a[a.index('--ncsrc') + 1] if '--ncsrc' in a else os.path.join(os.path.dirname(os.path.abspath(__file__)), '../cpu/nc_blend.py')
DEV = a[a.index('--gpudev') + 1] if '--gpudev' in a else 'OPTIX'
def _gpu_prefs():
    p = bpy.context.preferences.addons['cycles'].preferences
    for t in ([DEV, 'CUDA'] if DEV != 'CPU' else []):
        try:
            p.compute_device_type = t; p.refresh_devices(); n = 0
            for d in p.devices: d.use = d.type == t; n += d.use
            if n: print('NC-GPU-DEV', t, [d.name for d in p.devices if d.use], flush=True); return t
        except Exception as e: print('NC-GPU-DEV lỗi', t, repr(e), flush=True)
    return 'CPU'
code = open(src, encoding='utf-8').read()
A = "bpy.ops.wm.read_factory_settings(use_empty=True)"; B = "cy.device = 'CPU'"
assert A in code and B in code, 'nc_blend.py đổi — không vá được'
code = code.replace(A, A + "\n_DEV = _gpu_prefs()").replace(B, "cy.device = 'GPU' if _DEV != 'CPU' else 'CPU'")
g = {'__name__': '__main__', '__file__': src, '_gpu_prefs': _gpu_prefs}
exec(compile(code, src, 'exec'), g)
