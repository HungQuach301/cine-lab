"""Âm cho đoạn thử 30 s — biến thể A: chỉ nhạc + SFX gắn biến cố (ElevenLabs 0 trong phiên R&D; biến thể B có lời chỉ đặc tả).
Tài sản chỉ đọc, đã có quyền trong RIGHTS.md: K2-MUS-2 "Beauty Flow" (Kevin MacLeod, CC BY 4.0), K2-SFX-9 ship-siren, K2-SFX-24 building-site,
K2-SFX-16 city-traffic (Work With Sounds, CC BY 4.0). Tiếng "tích" khi thẻ hiện: tự tổng hợp.
Master: −14 LUFS tích hợp, true peak ≤ −1 dBTP. Dùng: mix30.py <ra.wav>"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
import pyloudnorm as pyln

SR, DUR = 48000, 30.0
REPO = Path(__file__).resolve().parents[2]
N = int(SR * DUR); t = np.arange(N) / SR

def dec(p, ss=0, dur=None):
    cmd = ["ffmpeg", "-v", "error", "-nostdin", "-ss", str(ss)] + (["-t", str(dur)] if dur else []) + ["-i", str(REPO / p), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).reshape(-1, 2).astype(np.float64)

def env(n, fi, fo):
    e = np.ones(n); a, b = int(fi * SR), int(fo * SR)
    if a: e[:a] = np.linspace(0, 1, a)
    if b: e[-b:] = np.minimum(e[-b:], np.linspace(1, 0, b))
    return e[:, None]

def put(dst, src, at, gain_db):
    k = int(at * SR); m = min(len(src), len(dst) - k)
    dst[k:k + m] += src[:m] * 10 ** (gain_db / 20)

meter = pyln.Meter(SR)
mix = np.zeros((N, 2))
mus = dec("assets/k2/music/Beauty-Flow.mp3", ss=0, dur=DUR); mus = mus * env(len(mus), 1.0, 2.5)
put(mix, mus / 10 ** (meter.integrated_loudness(mus) / 20) * 10 ** (-17 / 20), 0, 0)   # nhạc ≈ −17 LUFS trước master
CUES = [  # (giây, tệp, ss, dài, fade vào, fade ra, dB so với nhạc) — gắn biến cố trên hình (dòng thời gian v2, 4 yếu tố)
    (8.5, "assets/k2/sfx/ship-siren.mp3", 0.5, 3.0, 0.2, 1.2, -6),       # E2 bay dọc Damrak + nhịp "why here": tàu biển gặp thuyền sông
    (20.4, "assets/k2/sfx/building-site.mp3", 2.0, 4.6, 1.2, 1.4, -9),   # E3 reveal kéo lùi: 1900–1945 bùng nổ
    (27.9, "assets/k2/sfx/city-traffic.mp3", 1.0, 2.6, 1.0, 0.8, -10),   # E4b hoà sang "now"
]
for at, f, ss, d, fi, fo, db in CUES:
    x = dec(f, ss, d); x = x * env(len(x), fi, fo)
    x = x / 10 ** (meter.integrated_loudness(x) / 20) * 10 ** (-17 / 20)
    put(mix, x, at, db)
tick = (np.sin(2 * np.pi * 1760 * t[:int(0.09 * SR)]) * np.exp(-t[:int(0.09 * SR)] * 55))[:, None] * [1, 1]
for at in (0.4, 4.2, 8.6, 17.6, 27.0):   # thẻ hiện
    put(mix, tick, at, -24)
# E1 mốc đinh 13,0 s: nhịp trầm tự tổng hợp (65 Hz, tắt dần 1,2 s) khi năm dừng
boom = (np.sin(2 * np.pi * 65 * t[:int(1.2 * SR)]) * np.exp(-t[:int(1.2 * SR)] * 3.2))[:, None] * [1, 1]
put(mix, boom, 13.0, -12)
L = meter.integrated_loudness(mix); mix *= 10 ** ((-14 - L) / 20)
lim = 10 ** (-1.8 / 20)
for _ in range(4):
    up = np.repeat(mix, 4, axis=0); pk = np.max(np.abs(up))
    if pk <= lim: break
    g = np.minimum(1, lim / np.maximum(np.abs(mix).max(axis=1), 1e-9))
    from scipy.ndimage import minimum_filter1d, uniform_filter1d
    g = uniform_filter1d(minimum_filter1d(g, 480), 480)[:, None]; mix *= g
    mix *= 10 ** ((-14 - meter.integrated_loudness(mix)) / 20)
out = sys.argv[1]
import soundfile as sf
sf.write(out, mix.astype(np.float32), SR, subtype="PCM_24")
r = subprocess.run(["ffmpeg", "-nostdin", "-i", out, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
I = float(r.split("I:")[-1].split("LUFS")[0]); TP = float(r.split("Peak:")[-1].split("dBFS")[0])
json.dump(dict(lufs_I=I, true_peak_dbtp=TP, cues=[c[:2] for c in CUES]), open(out + ".json", "w"))
print(I, TP)
