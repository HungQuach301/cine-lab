"""V6 · xem nhanh tờ sprite (EXR nhiều lớp, light group nang/troi) → PNG trên nền xám, qua AgX như nền A.
  /opt/cine/bin/python -I xem_sprite6.py <tờ.exr> <ra.png> [--bong 0.0..1] [--cat x0,y0,x1,y1] [--kenh]"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, OpenEXR, cv2
import agx6
def load(p):
    f = OpenEXR.File(p); ch = {}
    for part in f.parts:
        for k, v in part.channels.items(): ch[k] = v.pixels
    return ch
def layers(ch):
    """trả (nang RGB, troi RGB, alpha) — tên kênh theo Blender 5.x (ViewLayer.Combined_<nhóm>)."""
    def get(prefix):
        for k, v in ch.items():
            if k.endswith(prefix) or k == prefix: return v
        return None
    al = None; ng = tr = comb = None
    for k, v in ch.items():
        kl = k.lower()
        if 'combined_nang' in kl: ng = v
        elif 'combined_troi' in kl: tr = v
        elif kl.endswith('combined') or kl.endswith('combined.rgba') or kl == 'viewlayer.combined': comb = v
    return ng, tr, comb
if __name__ == '__main__':
    ch = load(sys.argv[1])
    if '--kenh' in sys.argv:
        for k, v in ch.items(): print(k, v.shape, v.dtype)
        sys.exit()
    ng, tr, comb = layers(ch)
    bong = float(sys.argv[sys.argv.index('--bong') + 1]) if '--bong' in sys.argv else 1.0
    a = comb[..., 3:4].astype(np.float32)
    C = comb[..., :3].astype(np.float32)
    if ng is not None:   # light group không khử nhiễu → chỉ dùng TỈ SỐ nắng/(nắng+trời) đã làm mờ nhẹ, nhân với Combined đã khử nhiễu
        n_ = cv2.GaussianBlur(ng[..., :3].astype(np.float32), (0, 0), 1.2); t_ = cv2.GaussianBlur(tr[..., :3].astype(np.float32), (0, 0), 1.2)
        fr = n_ / np.maximum(n_ + t_, 1e-5); rgb = C * (fr * bong + (1 - fr))
    else: rgb = C
    un = rgb / np.maximum(a, 1e-3)
    disp = agx6.agx(un)
    bgc = np.full_like(disp, 0.45)
    out = disp * a + bgc * (1 - a)
    if '--cat' in sys.argv:
        x0, y0, x1, y1 = map(int, sys.argv[sys.argv.index('--cat') + 1].split(',')); out = out[y0:y1, x0:x1]
    cv2.imwrite(sys.argv[2], (np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8)[..., ::-1])
    print('ok', out.shape)
