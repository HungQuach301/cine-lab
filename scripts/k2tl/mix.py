"""V5b-1 · âm cho đoạn thử xương sống thời gian (port lab/timelapse/mix30.py): nhạc + SFX gắn biến cố hình, không lời (ElevenLabs 0).
Tài sản chỉ đọc, đã có dòng RIGHTS.md: K2-MUS-1 "Half Mystery" (Kevin MacLeod, CC BY 4.0) · K2-SFX-9 ship-siren · K2-SFX-26 camera-shutter ·
K2-SFX-24 building-site · K2-SFX-16 city-traffic (Work With Sounds, CC BY 4.0). Tiếng "tích" khi thẻ hiện + nhịp trầm mốc đinh: tự tổng hợp.
Master −14 LUFS tích hợp, true peak ≤ −1,5 dBTP (đo ebur128). Dùng: mix.py --cues <cues.json> --dur 20 --out <ra.wav>"""
import argparse, json, subprocess
from pathlib import Path
import numpy as np
import pyloudnorm as pyln
from scipy.ndimage import minimum_filter1d, uniform_filter1d
import soundfile as sf

SR = 48000
REPO = Path(__file__).resolve().parents[2]

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
    if m > 0: dst[k:k + m] += src[:m] * 10 ** (gain_db / 20)

def main(cues, dur, out, music="assets/k2/music/Half-Mystery.mp3", music_ss=0.0):
    N = int(SR * dur); t = np.arange(N) / SR; meter = pyln.Meter(SR); mix = np.zeros((N, 2))
    mus = dec(music, ss=music_ss, dur=dur); mus = mus * env(len(mus), 0.6, 1.6)
    put(mix, mus / 10 ** (meter.integrated_loudness(mus) / 20) * 10 ** (-17 / 20), 0, 0)
    for c in cues["sfx"]:
        x = dec(c["file"], c.get("ss", 0), c["dur"]); x = x * env(len(x), c.get("fi", 0.2), c.get("fo", 0.6))
        L = meter.integrated_loudness(x) if len(x) > SR * 0.4 else -20
        put(mix, x / 10 ** (L / 20) * 10 ** (-17 / 20), c["at"], c["db"])
    tick = (np.sin(2 * np.pi * 1760 * t[:int(0.09 * SR)]) * np.exp(-t[:int(0.09 * SR)] * 55))[:, None] * [1, 1]
    for at in cues.get("ticks", []): put(mix, tick, at, -24)
    for at in cues.get("booms", []):
        boom = (np.sin(2 * np.pi * 62 * t[:int(1.4 * SR)]) * np.exp(-t[:int(1.4 * SR)] * 2.8))[:, None] * [1, 1]; put(mix, boom, at, -11)
    mix *= 10 ** ((-14 - meter.integrated_loudness(mix)) / 20)
    lim = 10 ** (-1.8 / 20)
    for _ in range(6):
        if np.max(np.abs(np.repeat(mix, 4, axis=0))) <= lim: break
        g = np.minimum(1, lim / np.maximum(np.abs(mix).max(axis=1), 1e-9)); g = uniform_filter1d(minimum_filter1d(g, 480), 480)[:, None]; mix *= g
        mix *= 10 ** ((-14 - meter.integrated_loudness(mix)) / 20)
    sf.write(out, mix.astype(np.float32), SR, subtype="PCM_24")
    r = subprocess.run(["ffmpeg", "-nostdin", "-i", out, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    I = float(r.split("I:")[-1].split("LUFS")[0]); TP = float(r.split("Peak:")[-1].split("dBFS")[0])
    res = dict(lufs_I=I, true_peak_dbtp=TP, music=music, cues=cues); json.dump(res, open(out + ".json", "w"), ensure_ascii=False, indent=1); print(I, TP)

if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("--cues", required=True); a.add_argument("--dur", type=float, default=20); a.add_argument("--out", required=True)
    o = a.parse_args(); main(json.load(open(o.cues)), o.dur, o.out)
