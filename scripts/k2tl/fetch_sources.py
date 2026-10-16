"""V5b-1b · tải lại dữ liệu thô của gói cảnh Gibraltar vào $K2TL_CACHE (container mới không giữ bộ đệm) và KIỂM SHA-256 với
channel-k2/k2c-t3-01/v5b1-thu/do/sha256.txt (số của V5b-1). Nguồn và giấy phép: reports/V5B1-BAO-CAO.md §7.
Copernicus GLO-30 (AWS open data) · Sentinel-2 L2A S2C_30STF_20260415_0 (Element84 earth-search, COG) · Landsat 5 C2 L2 (Planetary Computer, ký SAS)
· Catastro INSPIRE BU 11022 · LoC 2025710366 (TIF gốc) · LUT A + B (git show origin/v5a). Dùng: fetch_sources.py [--only dem,s2,...]"""
import argparse, hashlib, json, os, subprocess, sys, urllib.parse, zipfile
from pathlib import Path

CACHE = Path(os.environ.get("K2TL_CACHE", "/var/tmp/cine-out/k2tl-cache"))
ROOT = Path(__file__).resolve().parents[2]
SHA = ROOT / "channel-k2/k2c-t3-01/v5b1-thu/do/sha256.txt"
S2 = "https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/30/S/TF/2026/4/S2C_30STF_20260415_0_L2A/"
LS = ("https://landsateuwest.blob.core.windows.net/landsat-c2/level-2/standard/tm/1987/201/035/LT05_L2SP_201035_19870726_20201014_02_T1/"
      "LT05_L2SP_201035_19870726_20201014_02_T1_SR_%s.TIF")
FILES = {
    "dem": [("dem/cop_n36w006.tif", "https://copernicus-dem-30m.s3.amazonaws.com/Copernicus_DSM_COG_10_N36_00_W006_00_DEM/Copernicus_DSM_COG_10_N36_00_W006_00_DEM.tif")],
    "s2": [("s2/a0415/visual.tif", S2 + "TCI.tif"), ("s2/a0415/nir.tif", S2 + "B08.tif")],
    "ls": [("ls/ls87_%s.tif" % b, LS % k) for b, k in (("blue", "B1"), ("green", "B2"), ("red", "B3"), ("nir08", "B4"), ("swir16", "B5"))],
    "catastro": [("catastro/bu11022.zip", "https://www.catastro.hacienda.gob.es/INSPIRE/buildings/11/11022-LA%20LINEA%20DE%20LA%20CONCEPCION/A.ES.SDGC.BU.11022.zip")],
    "loc": [("loc/1b07607u.tif", "https://tile.loc.gov/storage-services/master/pnp/pcrd/1b00000/1b07000/1b07600/1b07607u.tif")],
}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()


def curl(url, out):
    out.parent.mkdir(parents=True, exist_ok=True)
    for k in range(4):
        r = subprocess.run(["curl", "-sSL", "-m", "1200", "--retry", "2", "-o", str(out), "-w", "%{http_code}", url], capture_output=True, text=True)
        if r.stdout.strip() == "200": return
    raise SystemExit(f"LỖI tải {url}: {r.stdout} {r.stderr}")


def pc_sign(url):
    tok = json.loads(subprocess.run(["curl", "-s", "-m", "60", "https://planetarycomputer.microsoft.com/api/sas/v1/token/landsateuwest/landsat-c2"], capture_output=True, text=True).stdout)["token"]
    return url + "?" + tok


def main(only):
    want = dict(l.split()[::-1] for l in SHA.read_text().splitlines() if l.strip())
    rep = {}
    for grp, items in FILES.items():
        if only and grp not in only: continue
        for rel, url in items:
            p = CACHE / rel
            if not p.exists(): curl(pc_sign(url) if grp == "ls" else url, p)
            got = sha(p); ok = want.get(rel)
            rep[rel] = dict(sha=got, khop=(got == ok) if ok else None)
            print(rel, got[:12], "KHỚP" if got == ok else ("không có SHA gốc" if not ok else "LỆCH (nguồn đổi bản?)"), flush=True)
            if grp == "catastro":
                with zipfile.ZipFile(p) as z: z.extractall(p.parent)
    if not only or "lut" in only:
        for n in ("k2-a-thep-lanh", "k2-b-trung-tinh"):
            p = CACHE / f"lut/{n}.cube"; p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(subprocess.run(["git", "-C", str(ROOT), "show", f"origin/v5a:assets/k2/lut/{n}.cube"], capture_output=True, check=True).stdout)
            rep[f"lut/{n}.cube"] = dict(sha=sha(p), khop=(sha(p) == want.get(f"lut/{n}.cube")) if want.get(f"lut/{n}.cube") else None)
            print(f"lut/{n}.cube", rep[f"lut/{n}.cube"]["sha"][:12])
    (CACHE / "fetch_sources.json").write_text(json.dumps(rep, indent=1))
    bad = [k for k, v in rep.items() if v["khop"] is False]
    if bad: print("CẢNH BÁO SHA lệch:", bad, file=sys.stderr)


if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("--only", default="")
    main([x for x in a.parse_args().only.split(",") if x])
