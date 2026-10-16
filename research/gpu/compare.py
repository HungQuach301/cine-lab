"""GPU-RD · so khung GPU với khung CPU (SwiftShader) cùng số khung — tiêu chí khớp hình của lượt thử GPU.
Dùng: /opt/cine/bin/python research/gpu/compare.py <thư mục CPU> <thư mục GPU> [--out kq.json] [--psnr 40] [--diff 10] [--pct 1.0]
ĐẠT một khung khi PSNR ≥ 40 dB HOẶC tỉ lệ điểm ảnh lệch > 10/255 (kênh lớn nhất) ≤ 1 %. Báo thêm PSNR ở 1/4 kích thước (psnr_q4, tham khảo), SSIM (xám) và vùng lệch lớn nhất (ô 64×64).
Tiêu chí CẤU TRÚC (đề xuất, tham khảo): dat_cau_truc. Khung so: mọi tệp %05d.jpg có ở cả hai thư mục."""
import argparse, json, sys
from pathlib import Path
import numpy as np
from PIL import Image


def ssim_gray(a, b):
    import cv2
    a = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY).astype(np.float64); b = cv2.cvtColor(b, cv2.COLOR_RGB2GRAY).astype(np.float64)
    C1, C2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    mu1, mu2 = cv2.GaussianBlur(a, (11, 11), 1.5), cv2.GaussianBlur(b, (11, 11), 1.5)
    s1 = cv2.GaussianBlur(a * a, (11, 11), 1.5) - mu1 ** 2; s2 = cv2.GaussianBlur(b * b, (11, 11), 1.5) - mu2 ** 2; s12 = cv2.GaussianBlur(a * b, (11, 11), 1.5) - mu1 * mu2
    return float((((2 * mu1 * mu2 + C1) * (2 * s12 + C2)) / ((mu1 ** 2 + mu2 ** 2 + C1) * (s1 + s2 + C2))).mean())


def one(pa, pb, thr):
    a = np.asarray(Image.open(pa).convert("RGB")); b = np.asarray(Image.open(pb).convert("RGB"))
    if a.shape != b.shape: return dict(error=f"kích thước khác {a.shape} {b.shape}")
    d = np.abs(a.astype(np.int16) - b.astype(np.int16)); mse = float((d.astype(np.float64) ** 2).mean())
    psnr = 99.0 if mse == 0 else 10 * np.log10(255 ** 2 / mse)
    big = d.max(axis=2) > thr; pct = float(big.mean() * 100)
    H, W = big.shape; T = 64; worst = (0, 0, 0.0)
    for y in range(0, H - T + 1, T):
        for x in range(0, W - T + 1, T):
            v = float(big[y:y + T, x:x + T].mean())
            if v > worst[2]: worst = (x, y, v)
    q = lambda x: np.asarray(Image.fromarray(x).resize((x.shape[1] // 4, x.shape[0] // 4), Image.BOX), np.float64)
    m4 = float(((q(a) - q(b)) ** 2).mean()); psnr4 = 99.0 if m4 == 0 else 10 * np.log10(255 ** 2 / m4)   # PSNR ở 1/4 kích thước (bỏ nhiễu tần cao: grain/nhiễu thủ tục lệch số thực) — chỉ để tham khảo
    import cv2
    sd = b.astype(np.float64) - a; lo = cv2.GaussianBlur(sd, (0, 0), 8)   # lệch tần thấp (màu/sáng vùng), bỏ grain + cạnh dưới điểm ảnh
    lo_pct = float((np.abs(lo).max(axis=2) > 3).mean() * 100); shift = [round(float(x), 2) for x in sd.mean(axis=(0, 1))]
    return dict(psnr=round(psnr, 2), psnr_q4=round(psnr4, 2), lo_pct_gt3=round(lo_pct, 3), shift_rgb=shift, pct_diff_gt=round(pct, 3), ssim=round(ssim_gray(a, b), 4), mean_abs=round(float(d.mean()), 3), max_abs=int(d.max()), worst_tile=dict(x=worst[0], y=worst[1], pct=round(worst[2] * 100, 1)))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("cpu"); ap.add_argument("gpu"); ap.add_argument("--out"); ap.add_argument("--psnr", type=float, default=40.0)
    ap.add_argument("--diff", type=int, default=10); ap.add_argument("--pct", type=float, default=1.0); a = ap.parse_args()
    A, B = Path(a.cpu), Path(a.gpu); names = sorted(p.name for p in A.glob("*.jpg") if (B / p.name).exists())
    if not names: sys.exit("không có khung chung")
    rows = {}
    for n in names:
        r = one(A / n, B / n, a.diff); r["dat"] = bool(r.get("psnr", 0) >= a.psnr or r.get("pct_diff_gt", 100) <= a.pct)
        # tiêu chí CẤU TRÚC (đề xuất GPU-RD §5.3, chờ chủ dự án/K): tần thấp lệch > 3 mức ≤ 3 % · dịch màu TB ≤ 1 mức/kênh · PSNR 1/4 ≥ 40 · SSIM ≥ 0,90
        r["dat_cau_truc"] = bool("psnr" in r and r["lo_pct_gt3"] <= 3.0 and max(abs(x) for x in r["shift_rgb"]) <= 1.0 and r["psnr_q4"] >= 40 and r["ssim"] >= 0.90); rows[n] = r
        print(n, json.dumps(r), flush=True)
    ok = sum(r["dat"] for r in rows.values()); ps = [r["psnr"] for r in rows.values() if "psnr" in r]
    summ = dict(frames=len(rows), dat=ok, ty_le_dat=round(ok / len(rows), 4), psnr_min=min(ps), psnr_trung_vi=float(np.median(ps)),
                dat_cau_truc=sum(r.get("dat_cau_truc", False) for r in rows.values()), lo_pct_max=max(r.get("lo_pct_gt3", 0) for r in rows.values()),
                ssim_min=min(r.get("ssim", 0) for r in rows.values()), psnr_q4_min=min(r.get("psnr_q4", 0) for r in rows.values()), pct_diff_max=max(r["pct_diff_gt"] for r in rows.values() if "pct_diff_gt" in r), tieu_chi=dict(psnr=a.psnr, diff=a.diff, pct=a.pct))
    print("TỔNG", json.dumps(summ, ensure_ascii=False))
    if a.out: Path(a.out).write_text(json.dumps(dict(summary=summ, frames=rows), ensure_ascii=False, indent=1))
    sys.exit(0 if ok == len(rows) else 4)


if __name__ == "__main__":
    main()
