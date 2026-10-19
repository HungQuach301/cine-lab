import sys, numpy as np, OpenEXR, cv2
def read(p):
    f = OpenEXR.File(p); ch = f.channels()
    k = [c for c in ch if c.endswith('RGBA') or c.endswith('RGB')]
    if k: a = ch[k[0]].pixels
    else:
        names = sorted(ch); a = np.dstack([ch[n].pixels for n in ('R','G','B') if n in ch])
    return np.asarray(a, np.float32)[..., :3]
if __name__ == '__main__':
    a = read(sys.argv[1]); ex = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    x = a * ex; x = (x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14)   # ACES (Narkowicz) xem nhanh
    y = np.clip(x, 0, 1) ** (1 / 2.2); cv2.imwrite(sys.argv[2], (y[..., ::-1] * 255 + 0.5).astype(np.uint8)); print(a.shape, float(a.mean()), float(np.percentile(a, 99)))
