"""V5b-1 · bước 1 gói cảnh xương sống thời gian: raster nền trên lưới ENU cục bộ (m, gốc O = giao lộ đường băng × Winston Churchill Ave).
Ra $K2TL_CACHE/scene/<tên>/r_*.npy + ảnh kiểm r_*.jpg. Nguồn (giấy phép trong channel-k2/k2c-t3-01/licenses/ + v5b1-thu/licenses/):
 Copernicus GLO-30 (DSM) · Sentinel-2 L2A S2C_30STF_20260415_0 (TCI + B08; cảnh 24/09 có mây đúng trên Rock, cảnh 22/04 cụt mép dải quét — chọn theo SCL: 0,12 % mây, 0 % trống trong vùng cắt ở cảnh 22/04) · Landsat 5 TM C2 L2 201/035 26/07/1987 (USGS, công cộng).
Dùng: build_rasters.py --name gib"""
import argparse, json, os
from pathlib import Path
import numpy as np
from PIL import Image
import geo

CACHE = Path(os.environ.get("K2TL_CACHE", "/var/tmp/cine-out/k2tl-cache"))
SCENES = {"gib": dict(origin_ll=(-5.3487, 36.1513), ext=(-6500, -5500, 5500, 8500), s2="S2C_30STF_20260415_0_L2A", ls="LT05_L2SP_201035_19870726_02_T1")}   # E0, N0, E1, N1 (m quanh gốc)

def grid(ext, step):
    e0, n0, e1, n1 = ext
    xs = np.arange(e0, e1 + 1e-6, step); ys = np.arange(n1, n0 - 1e-6, -step)   # hàng 0 = bắc
    return np.meshgrid(xs, ys)

def otsu(v):
    v = v[np.isfinite(v)]; h, b = np.histogram(v, 256); c = (b[:-1] + b[1:]) / 2; w = np.cumsum(h); m = np.cumsum(h * c)
    s = (m[-1] * w / w[-1] - m) ** 2 / np.maximum(w * (w[-1] - w), 1); return c[np.argmax(s)]

def main(name):
    S = SCENES[name]; out = CACHE / "scene" / name; out.mkdir(parents=True, exist_ok=True)
    OE, ON = map(float, geo.utm(*S["origin_ll"])); ext = S["ext"]
    meta = dict(name=name, origin_ll=S["origin_ll"], origin_utm30=[OE, ON], ext=ext)
    # --- DEM (DSM) 10 m: lấy mẫu Copernicus (lat/lon) tại tâm ô ENU
    X, Y = grid(ext, 10.0); lon, lat = geo.utm_inv(X + OE, Y + ON)
    dem = geo.Raster(CACHE / "dem/cop_n36w006.tif")
    dsm = dem.sample(lon, lat, order=3).astype(np.float32)
    np.save(out / "r_dsm10.npy", dsm); meta["dsm"] = dict(step=10, shape=list(dsm.shape), min=float(dsm.min()), max=float(dsm.max()))
    # --- Sentinel-2 2026 (UTM 30N, 10 m): TCI + NIR
    for key, f in (("tci", "s2/a0415/visual.tif"), ("nir", "s2/a0415/nir.tif")):
        r = geo.Raster(CACHE / f); w = r.window_for(OE + ext[0], ON + ext[1], OE + ext[2], ON + ext[3]); r = geo.Raster(CACHE / f, window=w)
        v = r.sample(X + OE, Y + ON, order=1); np.save(out / f"r_s2{key}.npy", v.astype(np.float32))
    tci = np.load(out / "r_s2tci.npy"); nir = (np.load(out / "r_s2nir.npy") - 1000) / 10000   # L2A baseline ≥ 04.00: BOA_ADD_OFFSET −1000
    Image.fromarray(np.clip(tci, 0, 255).astype(np.uint8)).save(out / "r_s2tci.jpg", quality=92)
    red = tci[..., 0] / 255 * 0.3   # TCI ≈ phản xạ × 255/0,3 (ước, chỉ để ngưỡng NDVI)
    ndvi = (nir - red) / np.maximum(nir + red, 1e-3); np.save(out / "r_ndvi.npy", ndvi.astype(np.float32))
    t26 = otsu(nir); land26 = nir > t26
    # --- Landsat 5 1987 (UTM 30N, 30 m, PixelIsPoint)
    ls = {}
    for b in ("nir08", "red", "green", "blue"):
        r = geo.Raster(CACHE / f"ls/ls87_{b}.tif"); w = r.window_for(OE + ext[0], ON + ext[1], OE + ext[2], ON + ext[3]); r = geo.Raster(CACHE / f"ls/ls87_{b}.tif", window=w)
        ls[b] = r.sample(X + OE, Y + ON, order=1) * 2.75e-5 - 0.2
    t87 = otsu(ls["nir08"]); land87 = ls["nir08"] > t87
    rgb87 = np.clip(np.stack([ls["red"], ls["green"], ls["blue"]], -1) / 0.25, 0, 1) ** (1 / 2.2) * 255
    Image.fromarray(rgb87.astype(np.uint8)).save(out / "r_ls87.jpg", quality=92)
    ndvi87 = (ls["nir08"] - ls["red"]) / np.maximum(ls["nir08"] + ls["red"], 1e-3)
    np.save(out / "r_land26.npy", land26); np.save(out / "r_land87.npy", land87); np.save(out / "r_ndvi87.npy", ndvi87.astype(np.float32))
    np.save(out / "r_ls87rgb.npy", rgb87.astype(np.uint8))
    meta.update(s2_nir_thr=float(t26), ls87_nir_thr=float(t87), land26_pct=float(land26.mean() * 100), land87_pct=float(land87.mean() * 100))
    dbg = np.zeros(land26.shape + (3,), np.uint8); dbg[land26 & land87] = (150, 150, 150); dbg[land26 & ~land87] = (255, 60, 40); dbg[~land26 & land87] = (40, 120, 255)
    Image.fromarray(dbg).save(out / "r_landdiff.png")
    (out / "meta_rasters.json").write_text(json.dumps(meta, indent=1)); print(json.dumps(meta, indent=1))

if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("--name", default="gib"); main(a.parse_args().name)
