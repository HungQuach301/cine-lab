"""Nhóm M — M1 (loudness, true peak theo BS.1770) và M3 (tương quan pha, tương thích mono)."""
import re
import subprocess

import numpy as np
import pyloudnorm

from .common import FAIL, NA, metric, not_applicable, probe, read_audio, result, stream

SR = 48000


def ebur128(path):
    """Đo integrated loudness và true peak bằng bộ lọc ebur128 của ffmpeg."""
    cmd = ["ffmpeg", "-nostats", "-hide_banner", "-i", str(path), "-map", "0:a:0",
           "-filter:a", "ebur128=peak=true", "-f", "null", "-"]
    err = subprocess.run(cmd, capture_output=True, text=True).stderr
    summary = err[err.rfind("Summary:"):]
    i = re.search(r"I:\s+(-?[\d.]+|-inf)\s+LUFS", summary)
    lra = re.search(r"LRA:\s+(-?[\d.]+)\s+LU", summary)
    tp = re.search(r"True peak:\s+Peak:\s+(-?[\d.]+|-inf)\s+dBFS", summary)
    f = lambda m: float(m.group(1)) if m and m.group(1) != "-inf" else float("-inf")
    return f(i), f(tp), (f(lra) if lra else None)


def check_m1(path, profile):
    if profile != "youtube":
        return not_applicable("M1", "M1 chỉ áp cho master YouTube (--profile youtube). "
                                    "Master lưu trữ theo M2 (Chính), chưa thuộc v0.")
    if stream(probe(path), "audio") is None:
        return result("M1", FAIL, notes=["Không có luồng âm."])
    i, tp, lra = ebur128(path)
    ms = [metric("integrated loudness", i, "in", (-15.0, -13.0), "LUFS"),
          metric("true peak", tp, "<=", -1.0, "dBTP")]
    return result("M1", None, ms, notes=[f"LRA = {lra} LU (tham khảo)."] if lra is not None else [])


def _db(x):
    return 10 * np.log10(np.maximum(x, 1e-20))


def check_m3(path, profile):
    info = probe(path)
    a = stream(info, "audio")
    if a is None:
        return not_applicable("M3", "File không có luồng âm.")
    ch = int(a.get("channels", 0))
    if ch == 1:
        return result("M3", None, [metric("số kênh", 1, "==", 1)],
                      notes=["Âm mono: tương thích mono hiển nhiên. Master phải là stereo (N3)."])
    if ch != 2:
        return result("M3", FAIL, notes=[f"{ch} kênh: v0 chỉ đo stereo; bản 5.1 cần luật riêng."])
    x = read_audio(path, SR, 2).astype(np.float64)
    L, R = x[:, 0], x[:, 1]
    win = int(0.4 * SR)
    n = len(L) // win
    Lw, Rw = L[: n * win].reshape(n, win), R[: n * win].reshape(n, win)
    pl, pr = np.mean(Lw ** 2, 1), np.mean(Rw ** 2, 1)
    active = _db(np.maximum(pl, pr)) >= -50.0
    if not np.any(active):
        return result("M3", FAIL, notes=["Không có cửa sổ âm hoạt động (≥ −50 dBFS)."])
    corr = np.sum(Lw * Rw, 1) / np.sqrt(np.maximum(pl * pr, 1e-30)) / win
    ca = corr[active]
    neg_pct = 100.0 * np.mean(ca < -0.3)
    # Mất mát mono tích phân theo BS.1770: (L+R)/2 phát cả hai kênh so với stereo.
    meter = pyloudnorm.Meter(SR)
    m = (L + R) / 2
    st = meter.integrated_loudness(np.stack([L, R], 1))
    mo = meter.integrated_loudness(np.stack([m, m], 1))
    loss = mo - st if np.isfinite(st) and np.isfinite(mo) else float("-inf")
    # Cửa sổ 3 s (hop 400 ms), chỉ xét cửa sổ đủ hoạt động.
    pm = np.mean(((Lw + Rw) / 2) ** 2, 1)
    k = int(round(3.0 / 0.4))
    worst = 0.0
    worst_t = None
    for s in range(0, max(1, n - k + 1)):
        sl = slice(s, s + k)
        if np.mean(active[sl]) < 0.5:
            continue
        v = _db(2 * np.sum(pm[sl])) - _db(np.sum(pl[sl]) + np.sum(pr[sl]))
        if v < worst:
            worst, worst_t = float(v), round(s * 0.4, 1)
    ms = [
        metric("cửa sổ tương quan < −0,3", float(neg_pct), "<=", 1.0, "%"),
        metric("mất mát mono tích phân (BS.1770)", float(loss), ">=", -3.0, "dB"),
        metric("mất mát mono cửa sổ 3 s tệ nhất", worst, ">=", -6.0, "dB"),
    ]
    ev = {"tuong_quan_trung_vi": round(float(np.median(ca)), 3),
          "tuong_quan_nho_nhat": round(float(np.min(ca)), 3), "cua_so_te_nhat_giay": worst_t}
    return result("M3", None, ms, evidence=ev)
