"""NHẠC-T3 · đo đặc tính cue (chỉ đọc tệp nhạc; không sửa assets/).
Mỗi bản: thời lượng, loudness tích hợp (BS.1770, pyloudnorm), LRA xấp xỉ, tempo, giọng (chroma), và hồ sơ theo cửa sổ 5 s:
  L  = loudness ngắn hạn (LUFS, cửa sổ 5 s)       · rel = L − I (âm = chỗ lặng, hợp nằm dưới lời)
  sb = tỉ lệ năng lượng dải lời 300–3 400 Hz (%)  · cao = dễ đè lời (cần duck sâu hơn)
  on = số onset/giây (độ dày nhịp)                · c = trọng tâm phổ (Hz)
Dùng: python do_cue.py ra.json tệp1.mp3 [tệp2 …]"""
import sys, json, numpy as np, librosa, pyloudnorm as pyln
KEYS = 'C C# D D# E F F# G G# A A# B'.split()
MAJ = np.array([6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88]); MIN = np.array([6.33,2.68,3.52,5.38,2.60,3.53,2.54,4.75,3.98,2.69,3.34,3.17])
def key_of(y, sr):
    ch = librosa.feature.chroma_cqt(y=y, sr=sr).mean(1); best = None
    for i in range(12):
        for nm, prof in (('maj', MAJ), ('min', MIN)):
            r = np.corrcoef(ch, np.roll(prof, i))[0, 1]
            if best is None or r > best[0]: best = (r, f'{KEYS[i]} {nm}')
    return best[1]
def one(p, win=5.0):
    y2, sr = librosa.load(p, sr=44100, mono=False); y2 = np.atleast_2d(y2)
    meter = pyln.Meter(sr); I = meter.integrated_loudness(y2.T)
    y = librosa.to_mono(y2); y22 = librosa.resample(y, orig_sr=sr, target_sr=22050); s22 = 22050
    tempo = float(np.atleast_1d(librosa.beat.beat_track(y=y22, sr=s22)[0])[0])
    S = np.abs(librosa.stft(y22, n_fft=2048, hop_length=512)) ** 2; f = librosa.fft_frequencies(sr=s22, n_fft=2048)
    band = (f >= 300) & (f <= 3400); fr_t = librosa.frames_to_time(np.arange(S.shape[1]), sr=s22, hop_length=512)
    on_t = librosa.onset.onset_detect(y=y22, sr=s22, units='time'); cen = librosa.feature.spectral_centroid(S=np.sqrt(S), sr=s22)[0]
    prof = []; n = int(len(y) / sr // win)
    for k in range(n):
        a, b = k * win, (k + 1) * win; seg = y2[:, int(a * sr):int(b * sr)].T
        try: L = meter.integrated_loudness(seg) if seg.shape[0] > sr * 0.5 else -70
        except Exception: L = -70
        m = (fr_t >= a) & (fr_t < b); E = S[:, m].sum()
        prof.append(dict(t=a, L=round(float(max(L, -70)), 1), rel=round(float(max(L, -70) - I), 1), sb=round(float(100 * S[band][:, m].sum() / (E + 1e-12)), 0),
                         on=round(float(((on_t >= a) & (on_t < b)).sum() / win), 2), c=int(np.median(cen[m])) if m.any() else 0))
    Ls = np.array([q['L'] for q in prof if q['L'] > -60])
    return dict(tep=p.split('/')[-1], giay=round(len(y) / sr, 2), I=round(float(I), 1), LRA_xap_xi=round(float(np.percentile(Ls, 95) - np.percentile(Ls, 10)), 1) if len(Ls) else None,
                tempo=round(tempo, 1), giong=key_of(y22, s22), ho_so=prof)
if __name__ == '__main__':
    R = [one(p) for p in sys.argv[2:]]; json.dump(R, open(sys.argv[1], 'w'), ensure_ascii=False, indent=0)
    for r in R:
        print(f"\n## {r['tep']}  {r['giay']} s  I {r['I']}  LRA≈{r['LRA_xap_xi']}  {r['tempo']} bpm  {r['giong']}")
        print(' '.join(f"{int(q['t'])}:{q['rel']:+.0f}/{int(q['sb'])}/{q['on']:.1f}" for q in r['ho_so']))
