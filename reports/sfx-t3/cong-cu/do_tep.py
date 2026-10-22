"""SFX-T3 · đo kỹ thuật một tệp tiếng (gốc hoặc đoạn cắt): độ dài, tần số mẫu, kênh, I/LRA/TP (ebur128), đỉnh mẫu,
sàn nhiễu (p5 RMS 400 ms, dBFS), độ động (p95 − p5), băng thông (tần số dưới đó có 99 % năng lượng), DC, ù thấp (tỉ số đỉnh hẹp 40–200 Hz / nền).
  do_tep.py <ra.json> <tệp...>"""
import json, os, sys, subprocess, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../scripts/audio'))
import lib
SR = 48000
def probe(p):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=sample_rate,channels,codec_name,bits_per_raw_sample:format=duration', '-of', 'json', p], capture_output=True, text=True)
    j = json.loads(r.stdout); s = j['streams'][0]
    return dict(sr_goc=int(s['sample_rate']), kenh=int(s['channels']), codec=s['codec_name'], bit=s.get('bits_per_raw_sample'), dai_s=round(float(j['format']['duration']), 2))
def do(p):
    R = probe(p); x = lib.dec(p, 2, dtype=np.float64); m = x.mean(1)
    E = lib.ebur128(p) if R['dai_s'] >= 0.4 else dict(I=None, LRA=None, TP=None)
    w = int(0.4 * SR); n = len(m) // w
    rms = 20 * np.log10(np.sqrt((m[:n * w].reshape(n, w) ** 2).mean(1)) + 1e-12) if n else np.array([-120.0])
    F = np.abs(np.fft.rfft(m[:min(len(m), SR * 60)] * np.hanning(min(len(m), SR * 60)))) ** 2; f = np.fft.rfftfreq(min(len(m), SR * 60), 1 / SR)
    c = np.cumsum(F) / F.sum(); bw = float(f[np.searchsorted(c, 0.99)])
    lo = (f >= 40) & (f <= 200); band = F[lo]; hum = float(10 * np.log10(band.max() / np.median(band))) if band.size else 0
    R.update(I=E.get('I'), LRA=E.get('LRA'), TP=E.get('TP'), dinh_mau_dbfs=round(float(20 * np.log10(np.abs(x).max() + 1e-12)), 2),
             san_nhieu_dbfs=round(float(np.percentile(rms, 5)), 1), dong_db=round(float(np.percentile(rms, 95) - np.percentile(rms, 5)), 1),
             bang_thong_99_hz=round(bw), dc=round(float(m.mean()), 5), u_thap_db=round(hum, 1), sha256=lib.sha256(p))
    return R
if __name__ == '__main__':
    out = json.load(open(sys.argv[1])) if os.path.exists(sys.argv[1]) else {}
    for p in sys.argv[2:]:
        k = os.path.basename(p)
        if k in out: continue
        out[k] = do(p); print(k, {a: out[k][a] for a in ('dai_s', 'sr_goc', 'kenh', 'I', 'TP', 'san_nhieu_dbfs', 'bang_thong_99_hz')}, flush=True)
        json.dump(out, open(sys.argv[1], 'w'), ensure_ascii=False, indent=0)
