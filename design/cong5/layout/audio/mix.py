"""Cổng 4 — ÂM TẠM cho animatic "Last Round" (v2: 142,5 s, 48 kHz stereo). Mọi mốc lấy từ film.js (render_film.js --events), không gõ tay.
Chạy: /opt/cine/bin/python design/cong5/layout/audio/mix.py <thư mục ra>
Ghi: mix.flac (tổng), stems/dialogue.flac (CHỈ thoại), stems/amb.flac, stems/sfx.flac, stems/music.flac (FLAC 24-bit) — mix = tổng các stem đúng từng mẫu
(cùng một hệ số chuẩn hoá, không limiter), để J1b đối chiếu. cues.json: mốc thoại, SFX, đoạn nhạc.

Nguồn:
- Thoại: take L1–L4 của table read nháp 2 (reports/m1/cong2/tableread-d2/lines, giọng voice_id 59pjz3MTZdh9U1AETKfW, eleven_v3, seed 101)
  — bản chủ dự án đã nghe và duyệt ở Cổng 2. Đặt ở đầu shot s05 / s22 / s31 / s37 (EVENTS.DIALOGUE).
- Room tone, rè điện, "phụp", tách rơ-le, chuông, gõ kính, núm đồng hồ, van, bước chân: TỔNG HỢP BẰNG MÃ trong file này (không mẫu ngoài).
- Nhạc: ACE-Step 1.5 bản thử M0 (reports/m0/music/theme-dit-1.flac) — NHẠC TẠM, chỉ dùng cho animatic, không phát hành.
"""
import json, os, sys
import numpy as np, soundfile as sf, librosa, pyloudnorm as pyln
from scipy.signal import butter, sosfilt

import subprocess
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
EV = json.loads(subprocess.run(['node', os.path.join(REPO, 'design/cong5/layout/render_film.js'), '--events', '--out', '/tmp'], capture_output=True, text=True, check=True).stdout)
T0, T1 = EV['T0'], EV['T1']
SR, DUR = 48000, EV['FILM_S']
N = int(SR * DUR)
rng = np.random.default_rng(20260927)
t_all = np.arange(N) / SR
db = lambda x: 10 ** (x / 20)

def bp(x, lo=None, hi=None, order=4):
    if lo and hi: sos = butter(order, [lo, hi], 'bandpass', fs=SR, output='sos')
    elif lo: sos = butter(order, lo, 'highpass', fs=SR, output='sos')
    else: sos = butter(order, hi, 'lowpass', fs=SR, output='sos')
    return sosfilt(sos, x)
def place(buf, x, t, pan=0.0, gain=1.0):
    i = int(t * SR); j = min(N, i + len(x));
    if j <= i: return
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    buf[i:j, 0] += x[: j - i] * gain * l * 1.41421; buf[i:j, 1] += x[: j - i] * gain * r * 1.41421
def env(n, a, d):  # attack a (s), decay hằng số d (s)
    tt = np.arange(n) / SR; return np.minimum(1, tt / max(a, 1e-4)) * np.exp(-tt / d)
def noise(n): return rng.standard_normal(n)
def limit(x, thr_db, look=0.002, rel=0.04):   # hạn đỉnh có nhìn trước (xử lý thoại/nhạc thông thường); x: (n,) hoặc (n, c)
    a = np.abs(x) if x.ndim == 1 else np.abs(x).max(1); w = int(look * SR) * 2 + 1
    from scipy.ndimage import maximum_filter1d, uniform_filter1d
    e = maximum_filter1d(a, w); g = np.minimum(1.0, db(thr_db) / np.maximum(e, 1e-9)); g = np.minimum(g, uniform_filter1d(g, int(rel * SR)))
    return x * (g if x.ndim == 1 else g[:, None])
def brown(n):
    w = rng.standard_normal(n); b = np.cumsum(w); b = b - np.convolve(b, np.ones(4801) / 4801, 'same'); return b / (np.abs(b).max() + 1e-9)

# ---------------- SFX tổng hợp ----------------
def sfx_phup():   # mồi đèn khí: bùm trầm + xì bắt lửa
    n = int(0.9 * SR); tt = np.arange(n) / SR
    thump = np.sin(2 * np.pi * (70 + 40 * np.exp(-tt / 0.03)) * tt) * env(n, 0.004, 0.09)
    burst = bp(noise(n), hi=500) * env(n, 0.002, 0.07) * 1.2
    whoosh = bp(noise(n), 1800, 6000) * env(n, 0.03, 0.35) * 0.25
    return (thump * 0.8 + burst + whoosh) * 0.5
def sfx_click(bright=True):
    n = int(0.08 * SR); tt = np.arange(n) / SR
    x = bp(noise(n), 900, 5000) * env(n, 0.0005, 0.004) + np.sin(2 * np.pi * 2900 * tt) * env(n, 0.0005, 0.018) * 0.4
    return x if bright else bp(x, hi=1500)
def sfx_ding():
    n = int(3.2 * SR); tt = np.arange(n) / SR; x = np.zeros(n)
    for f, d, a in [(880, 2.6, 1.0), (1334, 1.7, 0.55), (2212, 0.9, 0.35), (3130, 0.5, 0.2), (440, 2.0, 0.25)]:
        x += a * np.sin(2 * np.pi * f * tt) * env(n, 0.002, d)
    return x * 0.28
def sfx_tick(): n = int(0.02 * SR); return bp(noise(n), 2500, 8000) * env(n, 0.0003, 0.002)
def sfx_tap():
    n = int(0.06 * SR); tt = np.arange(n) / SR
    return (bp(noise(n), 1500, 7000) * env(n, 0.0004, 0.003) + np.sin(2 * np.pi * 4200 * tt) * env(n, 0.0004, 0.012) * 0.5) * 0.9
def sfx_step():
    n = int(0.12 * SR); tt = np.arange(n) / SR
    return (bp(noise(n), 120, 1800) * env(n, 0.002, 0.025) + np.sin(2 * np.pi * 85 * tt) * env(n, 0.003, 0.03) * 0.6) * 0.35
def sfx_valve():
    n = int(0.9 * SR); tt = np.arange(n) / SR
    f = 1150 - 300 * tt / 0.9 + 25 * np.sin(2 * np.pi * 9 * tt)
    sq = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, tt / 0.05) * np.exp(-np.maximum(0, tt - 0.35) / 0.1) * 0.12
    hiss = bp(noise(n), 2500, 9000) * np.exp(-np.maximum(0, tt - 0.3) / 0.25) * np.minimum(1, tt / 0.1) * 0.08
    return sq + hiss
def sfx_snap(): n = int(0.1 * SR); tt = np.arange(n) / SR; return bp(noise(n), 800, 6000) * env(n, 0.0005, 0.006) + np.sin(2 * np.pi * 180 * tt) * env(n, 0.001, 0.02) * 0.4

# ---------------- ambience: room tone + rè điện theo cảnh ----------------
def amb_track():
    out = np.zeros((N, 2))
    c, w1, w2 = bp(brown(N), hi=900), bp(brown(N), hi=900), bp(brown(N), hi=900)
    tone = np.stack([c + 0.35 * w1, c + 0.35 * w2], 1) / 1.06   # M3: phần chung ở giữa + độ rộng nhẹ (bản trước: hai kênh độc lập → tương quan âm, mono kém)
    wind = bp(noise(N), 180, 700) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.07 * t_all + 1.0))
    # mức room tone theo cảnh (dB): cảnh 1 ngoài phố chạng vạng (có gió), cảnh 2–4 phố đêm, hốc cửa/ngõ kín hơn, phòng Cas rất kín
    BAY = ['s33', 's34', 's42b', 's42']; ALLEY = ['s44', 's45', 's46', 's47']
    rt = np.full(N, -36.0); rt[:int(T0['s09'] * SR)] = -34
    for sid in BAY + ALLEY: rt[int(T0[sid] * SR):int(T1[sid] * SR)] = -42
    rt[int(T0['s48'] * SR):] = -48
    out += tone * db(rt)[:, None] * 0.9
    wmask = t_all < T0['s09']; out[:, 0] += wind * db(-44) * wmask; out[:, 1] += wind * db(-44) * wmask
    # rè điện 50 Hz + hài: mức theo độ gần nguồn điện trong từng shot (0…1), nhảy bậc ở các lần bật (theo EVENTS)
    hum = sum(np.sin(2 * np.pi * 50 * k * t_all + k) / k for k in range(1, 7)) * (1 + 0.05 * np.sin(2 * np.pi * 0.3 * t_all))
    hum = hum + 0.15 * bp(noise(N), 3000, 6000)
    LV = {'s09': 0.15, 's09w': 0.1, 's10e': 0.2, 's10': 0.45, 's11': 0.4, 's12': 0.5, 's13': 0.7, 's14': 1.0, 's15': 1.0, 's19': 0.6, 's21': 1.0, 's22': 0.8,
          's23': 0.35, 's24': 0.25, 's24c': 0.25, 's25': 0.25, 's26': 0.25, 's27': 0.25, 's28': 1.0, 's29': 0.9, 's30': 0.9, 's31': 0.8, 's32': 0.8, 's33': 0.3, 's34': 0.3,
          's35': 0.35, 's36': 0.3, 's37': 0.3, 's37w': 0.35, 's38': 0.9, 's39': 0.9, 's40': 0.9, 's40w': 1.0, 's41': 0.9, 's42a': 1.0, 's42b': 0.6, 's42': 0.3,
          's43': 0.6, 's44': 0.2, 's45': 0.2, 's45c': 0.5, 's46': 0.2, 's47': 0.5, 's48': 0.03}
    lv = np.zeros(N)
    for sid, v in LV.items(): lv[int(T0[sid] * SR):int(T1[sid] * SR)] = v
    # bậc tăng khi nguồn điện trong/gần khung bật: (mốc, shot, mức sau khi bật)
    SW = [(EV['SQUARE_ON'], 's10e', 0.75), (EV['POST_ON'][2], 's12', 0.75), (EV['REACH_IDA'], 's13', 1.0), (EV['POST_ON'][3], 's19', 1.0),
          (EV['WALL_POST_ON'], 's27', 1.0), (EV['POST_ON'][5], 's37w', 1.0)]
    for t0, sid, v in SW: lv[int(t0 * SR):int(T1[sid] * SR)] = v
    lv[int(T1['s47'] * SR) - int(1.2 * SR):int(T1['s47'] * SR)] = np.linspace(0.5, 0.8, int(1.2 * SR))
    lv = np.convolve(lv, np.ones(960) / 960, 'same')
    # tắt tiếng theo bậc "nhấp 2 lần rồi đứng" ở các lần bật
    for t0 in [EV['CLOCK_ON'], EV['SQUARE_ON'], EV['POST_ON'][2], EV['REACH_IDA'], EV['POST_ON'][3], EV['WALL_POST_ON'], EV['POST_ON'][5]]:
        for a, b in [(0.08, 0.16), (0.26, 0.34)]: lv[int((t0 + a) * SR):int((t0 + b) * SR)] *= 0.3
    MUF = BAY + ALLEY
    muff = np.zeros(N, bool)
    for sid in MUF: muff[int(T0[sid] * SR):int(T1[sid] * SR)] = True
    h2 = np.where(muff, bp(hum, hi=400), hum) * lv * db(-30)
    out[:, 0] += h2; out[:, 1] += h2 * 0.95
    return out

def main(outdir):
    os.makedirs(os.path.join(outdir, 'stems'), exist_ok=True)
    dia, sfx, amb, mus = np.zeros((N, 2)), np.zeros((N, 2)), amb_track(), np.zeros((N, 2))
    cues = {'dialogue': [], 'sfx': [], 'music': []}
    # ---- thoại (take đã duyệt ở Cổng 2) ----
    LD = os.path.join(REPO, 'reports/m1/cong2/tableread-d2/lines')
    TEXT = {'L1': "Evening, old street.", 'L2': "Not yet... not yet.", 'L3': "Go on, then.",
            'L4': "That's the last one, then. Goodnight, old street. You'll be brighter now. Just... keep a little dark for the ones who need it."}
    meter = pyln.Meter(SR)
    D = EV['DIALOGUE']
    for code, t0 in [('L1', D['L1']), ('L2', D['L2']), ('L3', D['L3']), ('L4', D['L4'])]:
        y, _ = librosa.load(os.path.join(LD, f'{code}.mp3'), sr=SR, mono=True)
        idx = np.nonzero(np.abs(y) > db(-45))[0]; y = y[max(0, idx[0] - int(0.05 * SR)): idx[-1] + int(0.15 * SR)]
        L = meter.integrated_loudness(np.stack([y, y], 1)); y = limit(y * db(-20 - L), -7.0)       # mỗi câu về −20 LUFS, hạn đỉnh −7 dBFS (trước chuẩn hoá tổng)
        place(dia, y, t0, pan=0.0, gain=1 / 1.41421)
        cues['dialogue'].append({'code': code, 'start_s': t0, 'dur_s': round(len(y) / SR, 2), 'text': TEXT[code]})
    # ---- SFX ----
    def add(name, x, t, pan=0.0, g=0.0): place(sfx, x, t, pan, db(g)); cues['sfx'].append({'sfx': name, 't': round(t, 2), 'gain_db': g})
    G = EV['GAS_ON']
    for i, g in [(4, -6), (8, -8), (10, -7), (11, -8)]: add('phup', sfx_phup(), G[str(i)], -0.2, g)   # L10 bắt lửa SAU câu "Not yet… not yet." (kịch bản)
    add('phup_far', sfx_phup(), G['9'], -0.4, -20)
    add('relay_far', sfx_click(False), EV['RELAY_1'], 0.4, -26)
    add('clock_on', sfx_click(True), EV['CLOCK_ON'] - 0.05, 0.0, -18); add('ding', sfx_ding(), EV['DING'], 0.0, -8)
    add('relay_square', sfx_click(True), EV['SQUARE_ON'] - 0.05, 0.1, -12); add('relay_square_2', sfx_click(True), EV['SQUARE_ON'] + 0.2, 0.1, -16)
    for n in range(3): add('relay_city', sfx_click(False), T0['s10'] + 0.85 + n * 0.8, 0.3, -24 - 2 * n)
    P = EV['POST_ON']
    for t0, g in [(P[2], -16), (EV['REACH_IDA'], -14), (P[3], -15), (P[4], -22), (EV['WALL_POST_ON'], -12), (P[5], -9)]:
        add('relay', sfx_click(True), t0 - 0.05, 0.3, g); add('relay_flicker', sfx_click(True), t0 + 0.2, 0.3, g - 4)
    for b in [0.8, 1.2]: add('tap_glass', sfx_tap(), T0['s06'] + b, 0.1, -14)
    for a, b in [(T0['s06'], T1['s06']), (T0['s09w'], T1['s09w']), (T0['s45'], T1['s46'])]:
        for tt in np.arange(a, b, 0.2): place(sfx, sfx_tick(), tt, 0.0, db(-40))
        cues['sfx'].append({'sfx': 'watch_tick', 't': round(a, 2), 'to': round(b, 2), 'gain_db': -40})
    for tt in np.arange(T0['s46'] + 0.3, T0['s46'] + 2.2, 0.07): place(sfx, sfx_tick() * 1.6, tt, 0.05, db(-30))
    cues['sfx'].append({'sfx': 'crown_ratchet', 't': round(T0['s46'] + 0.3, 2), 'to': round(T0['s46'] + 2.2, 2), 'gain_db': -30}); add('watch_snap', sfx_snap(), T0['s46'] + 2.6, 0.05, -16)
    add('valve_off', sfx_valve(), EV['VALVE'], -0.1, -6)
    add('flame_out', sfx_snap() * 0.5, EV['L11_OFF'] - 0.02, -0.1, -18)
    for a, b, per, g in [(T0['s02'], T1['s02'], 0.625, -22), (T0['s07'], T1['s07'], 0.625, -22), (T0['s08'], T1['s08'], 0.625, -32), (T0['s15'] + 0.8, T1['s15'], 0.5, -22),
                         (T0['s23'], T0['s23'] + 1.1, 0.45, -20), (T0['s33'] + 1.2, T0['s33'] + 4.0, 0.62, -24), (T0['s35'], T0['s35'] + 2.4, 0.62, -22),
                         (T0['s42b'], T0['s42b'] + 1.7, 0.42, -24), (T0['s47'], T1['s47'], 0.6, -24)]:
        for tt in np.arange(a, b, per): place(sfx, sfx_step() * (0.8 + 0.4 * rng.random()), tt, rng.uniform(-0.2, 0.2), db(g))
        cues['sfx'].append({'sfx': 'footsteps', 't': round(a, 2), 'to': round(b, 2), 'gain_db': g})
    # ---- nhạc tạm (ACE-Step M0) ----
    m, msr = sf.read(os.path.join(REPO, 'reports/m0/music/theme-dit-1.flac'), always_2d=True)
    if msr != SR: m = np.stack([librosa.resample(m[:, c], orig_sr=msr, target_sr=SR) for c in range(m.shape[1])], 1)
    if m.shape[1] == 1: m = np.repeat(m, 2, 1)
    Mm, Sm = (m[:, 0] + m[:, 1]) / 2, (m[:, 0] - m[:, 1]) / 2; m = np.stack([Mm + 0.35 * Sm, Mm - 0.35 * Sm], 1)   # M3: bản ACE-Step có đoạn ngược pha (tương quan tới −0,74) → thu hẹp độ rộng còn 35 %
    Lm = meter.integrated_loudness(m); m = limit(m * db(-30 - Lm), -9.0)                                  # nền nhạc ~ −30 LUFS (dưới thoại ~10 dB)
    mlen = len(m) / SR; e3 = min(mlen, 37.0 + DUR - T0['s42a'])
    for src0, src1, film0, fi, fo in [(0.0, 24.0, 0.0, 2.0, 3.0), (24.0, 24.0 + T0['s37'] - T0['s32'], T0['s32'], 2.0, 2.0), (37.0, e3, T0['s42a'], 2.0, 3.5)]:
        seg = m[int(src0 * SR): int(src1 * SR)].copy(); n = len(seg); tt = np.arange(n) / SR
        g = np.minimum(1, tt / fi) * np.minimum(1, (n / SR - tt) / fo)
        i = int(film0 * SR); j = min(N, i + n); mus[i:j] += seg[: j - i] * g[: j - i, None]
        cues['music'].append({'src': 'reports/m0/music/theme-dit-1.flac', 'src_s': [src0, src1], 'film_s': [film0, round(film0 + (j - i) / SR, 2)], 'status': 'NHẠC TẠM'})
    # hạ nhạc 8 dB dưới L1
    duck = np.ones(N); a, b = int((D['L1'] - 0.6) * SR), int((D['L1'] + 2.8) * SR); duck[a:b] = db(-8); duck = np.convolve(duck, np.ones(4800) / 4800, 'same'); mus *= duck[:, None]
    # ---- ưu tiên lời: hạ nền (room tone, rè điện, SFX, nhạc) 8 dB khi có thoại (±0,25 s, vào/ra 0,15 s) ----
    act = np.abs(dia).max(1) > db(-45); from scipy.ndimage import maximum_filter1d, uniform_filter1d
    act = maximum_filter1d(act.astype(float), int(0.5 * SR)); dk = 1 - (1 - db(-8)) * uniform_filter1d(act, int(0.15 * SR))
    for x in (amb, sfx, mus): x *= dk[:, None]
    cues['ducking'] = {'db': -8, 'pad_s': 0.25, 'ramp_s': 0.15, 'stems': ['amb', 'sfx', 'music']}
    # ---- chuẩn hoá chung (một hệ số cho mọi stem) ----
    mix = dia + sfx + amb + mus
    # Neo theo THOẠI (không theo tích phân cả phim): mỗi câu −20 LUFS → +6 dB = −14 LUFS; nền giữ tương quan. Bus SFX hạn đỉnh −10 dBFS.
    sfx[:] = limit(sfx, -10.0); mix = dia + sfx + amb + mus
    gain = db(6.0)
    peak = np.abs(librosa.resample((mix * gain).T, orig_sr=SR, target_sr=SR * 4)).max()
    if peak > db(-1.5): gain *= db(-1.5) / peak
    for name, x in [('dialogue', dia), ('sfx', sfx), ('amb', amb), ('music', mus)]: sf.write(os.path.join(outdir, 'stems', f'{name}.flac'), (x * gain).astype(np.float32), SR, subtype='PCM_24')
    sf.write(os.path.join(outdir, 'mix.flac'), (mix * gain).astype(np.float32), SR, subtype='PCM_24')
    rep = {'sr': SR, 'dur_s': DUR, 'integrated_lufs': round(meter.integrated_loudness(mix * gain), 2), 'gain_db': round(20 * np.log10(gain), 2),
           'true_peak_dbfs_4x': round(20 * np.log10(np.abs(librosa.resample((mix * gain).T, orig_sr=SR, target_sr=SR * 4)).max()), 2), **cues}
    json.dump(rep, open(os.path.join(outdir, 'cues.json'), 'w'), ensure_ascii=False, indent=1)
    print(json.dumps({k: rep[k] for k in ['integrated_lufs', 'gain_db', 'true_peak_dbfs_4x']}))

if __name__ == '__main__':
    main(sys.argv[1])
