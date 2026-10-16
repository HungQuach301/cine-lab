"""GPU-RD · so cả đoạn: khung 1080p JPG (đường GL mới) thu về 960×540 với bản xem 540p của SwiftShader (mp4 đã commit ở v5b1b).
Nén H.264 của bản xem làm sàn lệch → hiệu chuẩn bằng các khung SwiftShader 1080p có sẵn (--ref-ss): so (SS 1080p→540p) với mp4 cho cùng khung.
Dùng: /opt/cine/bin/python research/gpu/so_mp4.py <mp4> <thư mục khung mới> [--ref-ss <thư mục khung SS 1080p>] [--out kq.json]"""
import argparse, json, subprocess, tempfile
from pathlib import Path
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser(); ap.add_argument("mp4"); ap.add_argument("new"); ap.add_argument("--ref-ss"); ap.add_argument("--out"); a = ap.parse_args()
T = Path(tempfile.mkdtemp()); subprocess.run(["ffmpeg", "-loglevel", "error", "-i", a.mp4, "-start_number", "0", str(T / "%05d.png")], check=True)


def psnr(x, y):
    m = float(((x.astype(np.float64) - y) ** 2).mean()); return 99.0 if m == 0 else 10 * np.log10(255 ** 2 / m)


def cmp(dirpath, names):
    r = {}
    for n in names:
        v = T / (n[:-4] + ".png"); s = Path(dirpath) / n
        if not v.exists() or not s.exists(): continue
        A = np.asarray(Image.open(v).convert("RGB")); B = np.asarray(Image.open(s).convert("RGB").resize((A.shape[1], A.shape[0]), Image.BOX))
        d = np.abs(A.astype(np.int16) - B).max(2); r[n] = dict(psnr540=round(psnr(A, B), 2), pct_gt10=round(float((d > 10).mean() * 100), 3))
    return r


names = sorted(p.name for p in Path(a.new).glob("*.jpg"))
new = cmp(a.new, names); ps = [v["psnr540"] for v in new.values()]
out = dict(frames=len(new), psnr540_min=min(ps), psnr540_p10=float(np.percentile(ps, 10)), psnr540_median=float(np.median(ps)),
           pct_gt10_median=float(np.median([v["pct_gt10"] for v in new.values()])), worst=sorted(new.items(), key=lambda kv: kv[1]["psnr540"])[:8])
if a.ref_ss:
    rs = cmp(a.ref_ss, sorted(p.name for p in Path(a.ref_ss).glob("*.jpg"))); out["san_nen_ss"] = rs
    out["cung_khung_moi"] = {k: new[k] for k in rs if k in new}
print(json.dumps(out, ensure_ascii=False, indent=1))
if a.out: Path(a.out).write_text(json.dumps(dict(summary=out, frames=new), ensure_ascii=False, indent=1))
