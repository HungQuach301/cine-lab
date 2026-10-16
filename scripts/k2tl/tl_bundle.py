"""V5b-2a (K-1.12 §7.1) · gom SỐ LIỆU một lượt dựng thành "bộ timelapse" commit được (≤ 5 MB, nén gzip) cho bộ kiểm checks 1.12 (q_tl.py, q_hinh.py bc1):
campath.json.gz (grammarLog mỗi khung + renderer) · text-budget.json.gz (ngân sách chữ + vai chữ + đường dẫn MỌI khung) · noi-dung-mask.json.gz (mặt nạ MỌI khung + hero_pct)
· log-chu.json (log chữ MỌI khung có thẻ/ảnh/nhãn neo, có role index_src) · anchor-dev.json (lệch đường dẫn ↔ điểm chiếu, anchor_dev.py) · nhan-sang.json (TL-Q1c)
· goi-canh-meta.json · bo-tl.json (trỏ các tệp trên; trường theo định nghĩa đầu q_tl.py).
Dùng: tl_bundle.py --run <thư mục lượt dựng: do/ + f1080/log.json> --out <thư mục đo trong repo> --scene-cues '<json cues>' [--sang <thư mục khung không chữ mốc đinh> --maskpng <thư mục>]"""
import argparse, gzip, json, os, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[1]
CACHE = Path(os.environ.get("K2TL_CACHE", "/var/tmp/cine-out/k2tl-cache"))


def gz(src, dst):
    with open(src, "rb") as f, gzip.open(dst, "wb", compresslevel=9, mtime=0) as g: g.write(f.read())


def sang(frames_dir, mask_dir, hero_b=2):
    """TL-Q1c: sáng TB (Y Rec.709 trên sRGB) trong mặt nạ hero / phần còn lại — khung KHÔNG chữ của quãng mốc đinh, mặt nạ cùng khung (thu về cỡ mặt nạ)."""
    out = []
    for m in sorted(Path(mask_dir).glob("*.png")):
        fp = Path(frames_dir) / (m.stem + ".jpg")
        if not fp.exists(): continue
        M = np.asarray(Image.open(m).convert("RGB")); hero = (M[..., 0] > 128) & (M[..., 1] < 90) & (np.abs(M[..., 2].astype(int) - hero_b) < 1)
        im = np.asarray(Image.open(fp).convert("RGB").resize((M.shape[1], M.shape[0]), Image.BOX), np.float64)
        Y = 0.2126 * im[..., 0] + 0.7152 * im[..., 1] + 0.0722 * im[..., 2]
        if hero.sum() < 50: continue
        out.append(dict(f=int(m.stem), hero_px=int(hero.sum()), y_hero=round(float(Y[hero].mean()), 2), y_con_lai=round(float(Y[~hero].mean()), 2), ti_le=round(float(Y[hero].mean() / max(1e-6, Y[~hero].mean())), 3)))
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--run", required=True); ap.add_argument("--out", required=True); ap.add_argument("--cues", required=True)
    ap.add_argument("--sang"); ap.add_argument("--maskpng"); ap.add_argument("--rights", default=str(ROOT / "RIGHTS.md")); a = ap.parse_args()
    R, O = Path(a.run), Path(a.out); O.mkdir(parents=True, exist_ok=True); cues = json.loads(a.cues)
    for n in ("campath.json", "text-budget.json", "noi-dung-mask.json"): gz(R / "do" / n, O / (n + ".gz"))
    log = json.load(open(R / "f1080" / "log.json"))
    lc = dict(nguon=f"render.js log.json — MỌI khung có thẻ/ảnh/nhãn neo + khung đo (mỗi 24)", renderer=log["renderer"], gl=log.get("gl"),
              frames=[dict(f=r["f"], year=r["year"], text=r["text"]) for r in log["frames"] if r.get("text")])
    json.dump(lc, open(O / "log-chu.json", "w"), ensure_ascii=False, separators=(",", ":"))
    ad = subprocess.run([sys.executable, str(HERE / "anchor_dev.py"), str(R / "do" / "campath.json"), str(R / "do" / "text-budget.json"), "--out", str(O / "anchor-dev.json")], capture_output=True, text=True, check=True)
    AD = json.load(open(O / "anchor-dev.json"))
    meta = json.load(open(CACHE / "scene/gib/pack/meta.json")); json.dump({k: meta[k] for k in ("stat", "n_buildings", "landY_counts", "plan1913", "origin_ll") if k in meta}, open(O / "goi-canh-meta.json", "w"), ensure_ascii=False, indent=1)
    rel = lambda p: os.path.relpath(p, O)
    bo = {"ten": f"gib20 V5b-2a (cú liên hoàn; {log['renderer']})", "ghi_chu": "Bộ timelapse do V5b-2a xuất (scripts/k2tl/tl_bundle.py): campath = grammarLog mỗi khung; mặt nạ + ngân sách chữ MỌI khung.",
          "campath": "campath.json.gz", "mat_bang": "xz", "fps": 24, "ngan_sach": "text-budget.json.gz", "log_chu": "log-chu.json",
          "tuyen": [{"t": cues["line"], "dung_dev_m": True, "nguon": "OSM Winston Churchill Avenue (tim tuyến gộp hai chiều, gib20.js)", "dich": [320, 15, 1650]}],
          "reveal": [{"t": [3.2, 7.4], "truong": "d_tower", "kieu": "zoom_in"}, {"t": cues["reveal"], "truong": "d_crossing", "kieu": "keo_lui"}],
          "anh": [{"id": "2025710366", "rights": rel(a.rights), "neo": True, "neo_px_loi": [x["dev_px"] for x in AD["leaders"] if x["role"] == "photo"]}],
          "ket": cues["end"],
          "nam_toa": {"nam_hien_tai": 2026, "moc": {"1941": "HM Government of Gibraltar 199/2018, 177/2023 (đường băng lấn vịnh 1941–1943)", "1987": "Landsat 5 TM 1987 (USGS)", "2026": "Copernicus Sentinel-2, 15/04/2026"},
                      "lop": {"Gibraltar (khối OSM, tầng chuẩn)": {"loai": "tang_chuan", "nguon": "goi-canh-meta.json stat gib_1987 + gib_2026", "nam": {"1987": meta["stat"]["gib_1987"], "2026": meta["stat"]["gib_2026"]}},
                              "đất theo năm (landY)": {"loai": "tang_chuan", "nguon": "goi-canh-meta.json landY_counts (0 = luôn là đất)", "nam": {k: v for k, v in meta["landY_counts"].items() if k != "0"}}}}}
    if a.sang and a.maskpng:
        S = sang(a.sang, a.maskpng); json.dump(S, open(O / "nhan-sang.json", "w"), indent=1)
        if S: bo["nhan_sang"] = [{"t": cues["pin"], "ti_le": round(float(np.median([x["ti_le"] for x in S])), 3)}]
    json.dump(bo, open(O / "bo-tl.json", "w"), ensure_ascii=False, indent=1)
    tot = sum(p.stat().st_size for p in O.iterdir() if p.is_file()); print(json.dumps(dict(out=str(O), bytes=tot, anchor=AD["summary"], nhan_sang=bo.get("nhan_sang")), ensure_ascii=False))


if __name__ == "__main__":
    main()
