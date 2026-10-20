"""NC-CPU · EXR (Cycles/Eevee, tuyến tính) → .f32 (RGBA float32, hàng từ dưới lên) cho nc_grade.js.  /opt/cine/bin/python nc_exr.py <exr…> --out <thư mục> [--k <hệ số phơi sáng>]"""
import sys, os, numpy as np, OpenEXR
a = sys.argv[1:]; out = a[a.index('--out') + 1]; k = float(a[a.index('--k') + 1]) if '--k' in a else 1.0; fs = [x for x in a if x.endswith('.exr')]
os.makedirs(out, exist_ok=True)
for p in fs:
    ch = OpenEXR.File(p).channels(); key = [c for c in ch if c.endswith('RGBA') or c.endswith('RGB')]
    px = np.asarray(ch[key[0]].pixels, np.float32) if key else np.dstack([np.asarray(ch[c].pixels, np.float32) for c in ('R', 'G', 'B')])
    rgb = px[..., :3] * k; rgba = np.dstack([rgb, np.ones(rgb.shape[:2], np.float32)])[::-1]
    np.ascontiguousarray(rgba).astype(np.float32).tofile(os.path.join(out, os.path.basename(p)[:-4] + '.f32'))
print(len(fs))
