"""J1b — lời rõ trên nhạc, đo từ stem thoại và stem nền (M&E) do bản mix xuất ra.

Thư mục <video>.stems/: dialogue.wav|flac (thoại) và ≥ 1 file âm khác (me.wav, hoặc music.wav +
sfx.wav ...) — mọi file âm không phải dialogue.* được cộng lại thành nền. Máy:
  1) kiểm tổng các stem khớp mix cuối trong file video (hồi quy 2 hệ số, lệch thời gian ±100 ms);
  2) tách câu từ stem thoại (khoảng lặng ≥ 350 ms), tính SII rút gọn theo từng câu và cửa sổ 0,5 s.
"""
import subprocess
from pathlib import Path

import numpy as np

from scipy.optimize import nnls

from .common import FAIL, metric, probe, read_audio, result, stream

SR = 48000
AUDIO_EXT = {".wav", ".flac", ".aif", ".aiff", ".w64"}
MAX_LAG = int(0.1 * SR)
ENV_MAX_DB = 3.0         # P95 sai lệch bao năng lượng tổng stem so với mix (nội bộ)
GAIN_DIFF_MAX_DB = 1.0   # chênh hệ số khớp thoại/nền (nội bộ)
ENV_BANDS = [125, 250, 500, 1000, 2000, 4000, 8000]
SII_SENT_MIN = 0.75      # ANSI S3.5: SII > 0,75 được coi là giao tiếp tốt (dùng cho SII rút gọn, nội bộ)
SII_WIN_MIN = 0.45       # ANSI S3.5: SII < 0,45 được coi là kém (nội bộ)
# ANSI S3.5-1997, thủ tục dải octave: tầm quan trọng dải cho lời nói trung bình
BANDS = [(250, 0.0617), (500, 0.1671), (1000, 0.2373), (2000, 0.2648), (4000, 0.2142), (8000, 0.0549)]
HOP = 480                # 10 ms
NFFT = 2048
GAP = 35                 # khoảng lặng ≥ 350 ms tách câu
MIN_SENT = 30            # câu ≥ 300 ms
WIN = 50                 # cửa sổ 0,5 s


def decode(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:a:0", "-ac", "2", "-ar", str(SR),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)


def load_stems(stem_dir):
    d = Path(stem_dir)
    files = sorted(p for p in d.iterdir() if p.suffix.lower() in AUDIO_EXT)
    dia = [p for p in files if p.stem.lower() == "dialogue"]
    bg = [p for p in files if p.stem.lower() != "dialogue"]
    if not dia or not bg:
        raise FileNotFoundError(f"{d}: cần dialogue.wav|flac và ≥ 1 stem nền; thấy {[p.name for p in files]}")
    D = decode(dia[0])
    Bs = [decode(p) for p in bg]
    n = max([len(D)] + [len(b) for b in Bs])
    pad = lambda x: np.pad(x, ((0, n - len(x)), (0, 0)))
    return pad(D), sum(pad(b) for b in Bs), [dia[0].name] + [p.name for p in bg]


def best_lag(ref, x):
    """Lệch (mẫu) sao cho x[t + lag] ≈ ref[t], tìm trong ±MAX_LAG trên 30 s đầu (tương quan FFT)."""
    n = min(len(ref), len(x), 30 * SR)
    a, b = ref[:n], x[:n]
    m = 1 << int(np.ceil(np.log2(2 * n)))
    c = np.fft.irfft(np.fft.rfft(b, m) * np.conj(np.fft.rfft(a, m)), m)
    c = np.concatenate([c[-MAX_LAG:], c[:MAX_LAG + 1]])
    return int(np.argmax(c)) - MAX_LAG


def shift(x, lag, n):
    out = np.zeros((n, x.shape[1]))
    if lag >= 0:
        seg = x[lag:lag + n]
    else:
        seg = np.concatenate([np.zeros((-lag, x.shape[1])), x[:n + lag]])
    out[:len(seg)] = seg
    return out


def band_power(x):
    """x mono → (số khung 10 ms, số dải) công suất octave, cửa sổ Hann 2048."""
    n = 1 + max(0, (len(x) - NFFT) // HOP)
    idx = np.arange(NFFT)[None, :] + HOP * np.arange(n)[:, None]
    xp = np.pad(x, (0, max(0, idx.max() + 1 - len(x))))
    S = np.abs(np.fft.rfft(xp[idx] * np.hanning(NFFT), axis=1)) ** 2
    f = np.fft.rfftfreq(NFFT, 1 / SR)
    return np.stack([S[:, (f >= fc / np.sqrt(2)) & (f < fc * np.sqrt(2))].sum(1) for fc, _ in BANDS], 1)


def env(x):
    """Năng lượng (khung 100 ms, dải octave ENV_BANDS), dàn phẳng."""
    n = 1 + max(0, (len(x) - NFFT) // HOP)
    idx = np.arange(NFFT)[None, :] + HOP * np.arange(n)[:, None]
    xp = np.pad(x, (0, max(0, idx.max() + 1 - len(x))))
    S = np.abs(np.fft.rfft(xp[idx] * np.hanning(NFFT), axis=1)) ** 2
    f = np.fft.rfftfreq(NFFT, 1 / SR)
    E = np.stack([S[:, (f >= fc / np.sqrt(2)) & (f < fc * np.sqrt(2))].sum(1) for fc in ENV_BANDS], 1)
    k = len(E) // 10
    return E[:k * 10].reshape(k, 10, -1).sum(1).ravel()


def sii(ps, pn):
    snr = 10 * np.log10(np.maximum(ps, 1e-20) / np.maximum(pn, 1e-20))
    a = np.clip((snr + 15) / 30, 0, 1)
    return float(np.sum([w for _, w in BANDS] * a)), snr


def sentences(d_mono):
    fr = len(d_mono) // HOP
    e = 10 * np.log10(np.mean(d_mono[:fr * HOP].reshape(fr, HOP) ** 2, 1) + 1e-20)
    if fr == 0 or e.max() < -60:
        return [], e
    act = e > max(e.max() - 35, -60)
    segs, i = [], 0
    while i < fr:
        if not act[i]:
            i += 1
            continue
        j = i
        while j < fr:
            if act[j]:
                j += 1
                continue
            k = j
            while k < fr and not act[k]:
                k += 1
            if k - j >= GAP or k == fr:
                break
            j = k
        if j - i >= MIN_SENT:
            segs.append((i, j))
        i = j + 1
    return segs, act


def check_j1b(video, profile, stem_dir=None):
    if stream(probe(video), "audio") is None:
        return result("J1b", FAIL, notes=["File không có luồng âm."])
    mix = read_audio(video, SR, 2).astype(np.float64)
    D, B, names = load_stems(stem_dir)
    if abs(len(mix) - len(D)) > SR:
        return result("J1b", FAIL, notes=[f"Độ dài stem ({len(D) / SR:.2f} s) lệch mix ({len(mix) / SR:.2f} s) quá 1 s."])
    lag = best_lag((D + B).mean(1), mix.mean(1))
    m = shift(mix, lag, len(D))  # căn: m[t] = mix[t + lag] ≈ stem[t]
    Ds, Bs = D, B
    # Khớp theo bao năng lượng (khung 100 ms × dải octave 125 Hz–8 kHz): bền với mã hoá AAC và limiter nhẹ.
    Em, Ed, Eb = (env(x.mean(1)) for x in (m, Ds, Bs))
    act = Em > Em.max() * 10 ** (-60 / 10)
    A = np.stack([Ed[act] / Em[act], Eb[act] / Em[act]], 1)
    (al, be), _ = nnls(A, np.ones(int(act.sum())))
    pred = al * Ed + be * Eb
    err = np.abs(10 * np.log10(np.maximum(pred[act], 1e-20) / Em[act]))
    env_p95 = float(np.percentile(err, 95)) if err.size else float("inf")
    gd, gb = float(np.sqrt(al)), float(np.sqrt(be))
    gdiff = 20 * np.log10(gd / gb) if gd > 0 and gb > 0 else float("inf")
    fit = np.stack([Ds.ravel(), Bs.ravel()], 1) @ np.array([gd, gb])
    resid_db = 10 * np.log10(np.sum((m.ravel() - fit) ** 2) / max(np.sum(m ** 2), 1e-20))
    dm, bm = gd * Ds.mean(1), gb * Bs.mean(1)
    segs, _ = sentences(dm)
    PS, PN = band_power(dm), band_power(bm)
    rows, worst_win = [], (1.0, None)
    for a, b in segs:
        b = min(b, len(PS))
        s_val, snr = sii(PS[a:b].mean(0), PN[a:b].mean(0))
        wmin = s_val
        wat = a
        for w0 in range(a, max(a + 1, b - WIN + 1), 5):
            v, _ = sii(PS[w0:w0 + WIN].mean(0), PN[w0:w0 + WIN].mean(0))
            if v < wmin:
                wmin, wat = v, w0
        rows.append(dict(tu_giay=round(a * HOP / SR, 2), den_giay=round(b * HOP / SR, 2), sii=round(s_val, 3),
                         sii_cua_so_min=round(wmin, 3), cua_so_te_giay=round(wat * HOP / SR, 2),
                         snr_dai_db=[round(float(x), 1) for x in snr]))
        if wmin < worst_win[0]:
            worst_win = (wmin, round(wat * HOP / SR, 2))
    notes = [f"Stem: {', '.join(names)}. Lệch thời gian mix–stem: {lag / SR * 1000:.1f} ms. "
             f"Hệ số khớp: thoại {gd:.3f}, nền {gb:.3f}."]
    notes.append(f"Phần dư dạng sóng sau khớp (tham khảo, chịu ảnh hưởng mã hoá AAC): {resid_db:.1f} dB.")
    ms = [metric("sai lệch bao năng lượng tổng stem so với mix (P95)", env_p95, "<=", ENV_MAX_DB, "dB"),
          metric("chênh hệ số khớp thoại/nền", abs(float(gdiff)), "<=", GAIN_DIFF_MAX_DB, "dB")]
    if not segs:
        notes.append("Stem thoại không có câu nào (im lặng): đoạn không có lời.")
    else:
        ms += [metric("SII rút gọn thấp nhất theo câu", min(r["sii"] for r in rows), ">=", SII_SENT_MIN),
               metric("SII rút gọn thấp nhất cửa sổ 0,5 s trong câu", worst_win[0], ">=", SII_WIN_MIN)]
    return result("J1b", None, ms, notes,
                  evidence=dict(so_cau=len(rows), cau=rows[:200], lech_ms=round(lag / SR * 1000, 2),
                                he_so=dict(thoai=round(float(gd), 4), nen=round(float(gb), 4))))
