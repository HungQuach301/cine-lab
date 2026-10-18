"""V6 · biến đổi hiển thị Y HỆT nền A: AgX + look "AgX - Medium High Contrast" + phơi sáng 0,35 (build_scene.py) — OpenColorIO đọc
config.ocio của chính Blender 5.2 (/opt/bpy/.../datafiles/colormanagement). Dùng để đưa sprite tuyến tính (EXR, light group) về cùng không gian
hiển thị với nền PNG trước khi ghép. OpenColorIO cài ngoài git ở /var/tmp/v6kn/pylib313 (pip, BSD-3)."""
import sys, os
sys.path.append('/var/tmp/v6kn/pylib313')
import numpy as np
import PyOpenColorIO as OCIO
CFG = '/opt/bpy/lib/python3.13/site-packages/bpy/5.2/datafiles/colormanagement/config.ocio'
_P = {}
def proc(look='AgX - Medium High Contrast'):
    if look not in _P:
        cfg = OCIO.Config.CreateFromFile(CFG)
        t = OCIO.DisplayViewTransform(src='Linear Rec.709', display='sRGB', view='AgX')
        lt = OCIO.LookTransform(src='Linear Rec.709', dst='Linear Rec.709', looks=look) if look else None
        grp = OCIO.GroupTransform([lt, t] if lt else [t])
        _P[look] = cfg.getProcessor(grp).getDefaultCPUProcessor()
    return _P[look]
def agx(rgb, exposure=0.35, look='AgX - Medium High Contrast'):
    """rgb tuyến tính (H, W, 3) → sRGB hiển thị 0–1 (như PNG của Blender)."""
    a = np.ascontiguousarray(np.asarray(rgb, np.float32) * (2.0 ** exposure)).copy()
    sh = a.shape; flat = a.reshape(-1, 3).copy()
    proc(look).applyRGB(flat)
    return np.clip(flat.reshape(sh), 0, 1)
def srgb2lin(a): return np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
