"""NC-GPU · ghép ô albedo nc_topo.js thành topo_full.png (đúng cách nc_blend.topo_image) TRƯỚC khi gửi lên pod (Python của Blender trên pod không có imageio)."""
import sys, os, json, numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
for d in sys.argv[1:]:
    T = json.load(open(os.path.join(d, 'topo.json'))); W = int(round((T['box'][2] - T['box'][0]) / T['res'])); H = int(round((T['box'][3] - T['box'][1]) / T['res']))
    A = np.zeros((H, W, 4), np.uint8)
    for t in T['tiles']:
        p = np.asarray(Image.open(os.path.join(d, t['file'])).convert('RGBA')); x0 = t['i'] * T['TILE']; y0 = t['j'] * T['TILE']; A[y0:y0 + p.shape[0], x0:x0 + p.shape[1]] = p
    Image.fromarray(A).save(os.path.join(d, 'topo_full.png'), compress_level=3); print(d, A.shape)
