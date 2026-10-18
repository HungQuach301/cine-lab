"""PT3 · đọc EXR một lớp (RGBA float32) do build_pt3.py ghi — /opt/cine/bin/python (OpenEXR 3)."""
import numpy as np, OpenEXR

def read(path, chans='RGBA'):
    with OpenEXR.File(path, separate_channels=True) as f:
        ch = f.channels(); return np.stack([ch[c].pixels.astype(np.float32) for c in chans if c in ch], -1)

def lin2srgb(x):
    x = np.clip(x, 0, 1); return np.where(x <= 0.0031308, 12.92 * x, 1.055 * np.power(x, 1 / 2.4) - 0.055)

def srgb2lin(x):
    x = np.clip(x, 0, 1); return np.where(x <= 0.04045, x / 12.92, np.power((x + 0.055) / 1.055, 2.4))
