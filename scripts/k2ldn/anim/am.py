#!/opt/cine/bin/python
"""ANIMATIC-T4 · việc 7 — ÂM THANH NHÁP: lời dựng (loi_dung.py) + SFX nháp theo hình (§16; chỉ CC0 / tài sản công Mỹ — ứng viên SFX-T3 reports/sfx-t3/ung-vien/, giấy phép trong ung-vien.json)
+ nhạc nháp theo bộ kênh (Scott Buckley, CC BY 4.0 — K2-MUS-6…13, cue-B T3) theo chương; nén nhạc/SFX dưới lời (sidechain theo đường bao lời); chuẩn −14 LUFS, đỉnh thật ≤ −1,5 dBTP.
KHÔNG phải mix cuối (lệnh). Ra: $ANIM_OUT/am-nhap.wav (48 kHz stereo) + channel-k2/k2c-t4-02/animatic/am-cue.json (cue nhạc, SFX từng shot, số đo)."""
import json, os, subprocess, zlib
from pathlib import Path
import numpy as np, soundfile as sf, pyloudnorm as pyln
REPO = Path(__file__).resolve().parents[3]; EP = REPO / 'channel-k2/k2c-t4-02'; AN = EP / 'animatic'; OUT = Path(os.environ.get('ANIM_OUT', '/var/tmp/anim/out')); SR = 48000
SFX = REPO / 'reports/sfx-t3/ung-vien'; MUS = REPO / 'assets/k2/music'
NHAC = [('MÓC', 'Katabasis_I.mp3'), ('HỒI 1', None), ('HỒI 2', 'sb_hiraeth.mp3'), ('HỒI 3', 'Echoes.mp3'), ('HỒI 4', 'sb_undertow.mp3'), ('HỒI 5', 'sb_neverdying.mp3')]
S = {  # mã shot → [(SFX, dB tương đối)]  — chọn theo hình (bậc 5, nháp)
 'M01': [('PHO-2', -6), ('GIO-3', -12)], 'M02': [('GIO-3', -8)], 'M03': [('LUAL-1', -8), ('DEM-1', -12)], 'M04': [('GIO-1', -12)],
 'H1-01a': [('LUAN-1', -2)], 'H1-01b': [('LUAN-1', -4), ('DEM-1', -10)], 'H1-02': [('LUAL-3', -2)], 'H1-03': [('GIO-3', -10), ('CHIM-1', -12)], 'H1-04': [('LUAL-1', -8), ('DONG-3', -14)],
 'H1-05a': [('DONG-2', -6), ('THUYEN-1', -6)], 'H1-05b': [('THUYEN-1', -4), ('SONG-2', -10)], 'H1-06': [('LUAL-1', -8), ('DONG-1', -14)], 'H1-07': [('LUAL-1', -8), ('GIO-2', -12)],
 'H1-08a': [('DEM-1', -8), ('SONG-2', -10), ('LUAL-1', -16)], 'H1-08b': [('LUAL-1', -8)], 'H1-10': [('NGUA-1', -4), ('DONG-2', -6)], 'H1-12': [('THUYEN-1', -4), ('LUAL-2', -6), ('SONG-2', -10)],
 'H1-11': [('LUAL-1', -6)], 'H1-13': [('LUAL-3', -4)], 'H1-14': [('LUAN-2', -4), ('LUAL-1', -10)], 'H1-15': [('LUAL-1', -8), ('NO-2', -6), ('PXA-3', -8)], 'H1-16': [('GIO-2', -10)],
 'H1-17a': [('DONG-3', -6)], 'H1-17b': [('DONG-3', -8), ('LUAN-1', -8)], 'H1-18': [('GIO-3', -10)], 'H1-19': [('GIO-3', -8), ('DAO-2', -12)], 'H2-01a': [('GIO-3', -8), ('DAO-2', -10)],
 'H2-01b': [('DAO-2', -8), ('GIO-3', -10)], 'H2-02': [('GIO-3', -14)], 'H2-03a': [('DAO-1', -6), ('DONG-3', -12)], 'H2-03b': [('GIO-3', -12)], 'H2-04a': [('DAO-1', -4)], 'H2-04b': [('NGUA-1', -6), ('DAO-1', -8)],
 'H2-05': [('DAO-1', -14), ('PHO-1', -14)], 'H2-06': [('PHO-1', -14)], 'H2-07': [('BUOC-1', -8), ('PHO-1', -10)], 'H2-08': [('CHIM-1', -14)], 'H2-09': [('PHO-1', -14)], 'H2-10': [('CHIM-1', -12)],
 'H2-11': [('GIO-3', -14)], 'H2-12': [('GIO-3', -14)], 'H2-13': [('THUYEN-1', -4), ('SONG-2', -8)], 'H2-14': [('PHO-1', -14)], 'H3-01': [('PHO-1', -14)], 'H3-02': [('SONG-2', -10), ('CHIM-1', -12)],
 'H3-03': [('GIO-3', -14)], 'H3-04a': [('PHO-1', -12)], 'H3-04b': [('BUOC-1', -6), ('PHO-2', -10)], 'H3-05': [('PHO-1', -14)], 'H3-06': [('GIO-3', -14)], 'H4-01a': [('GIO-1', -10)], 'H4-01b': [('GIO-1', -6)],
 'H4-02': [('MAYBAY-1', -6), ('NO-1', -8), ('LUAL-1', -10)], 'H4-03': [('LUAL-1', -10), ('SONG-2', -10), ('BUOC-2', -8)], 'H4-04a': [('LUAL-2', -6), ('NO-2', -10)], 'H4-04b': [('LUAL-3', -6), ('BUOC-1', -10)],
 'H4-04c': [('LUAL-2', -8), ('MAYBAY-1', -14)], 'H4-05': [('GIO-2', -10), ('LUAN-2', -14)], 'H4-06': [('GIO-2', -12)], 'H4-07': [('GIO-3', -14)], 'H4-08': [('GIO-3', -14)],
 'H5-01': [('PHO-1', -14)], 'H5-02': [('PHO-1', -12)], 'H5-03': [('GIO-3', -14)], 'H5-04': [('PHO-2', -12)], 'H5-05a': [('PHO-2', -10)], 'H5-05b': [('PHO-1', -8)], 'H5-06': [('PHO-2', -12)],
 'H5-07a': [('SONG-2', -6), ('PHO-3', -8)], 'H5-07b': [('LUAL-1', -12), ('PHO-3', -10)], 'H5-08': [('PHO-3', -12)]}


def load(p, sr=SR):
    if str(p).endswith('.mp3'):
        raw = subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-i', str(p), '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
        return np.frombuffer(raw, np.float32).astype(np.float64)
    x, s = sf.read(str(p), dtype='float64')
    if x.ndim > 1: x = x.mean(1)
    if s != sr:
        raw = subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-i', str(p), '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True, check=True).stdout; x = np.frombuffer(raw, np.float32).astype(np.float64)
    return x


def lufs_norm(x, target):
    m = pyln.Meter(SR); l = m.integrated_loudness(x) if len(x) > SR else -70
    return x * 10 ** ((target - l) / 20) if np.isfinite(l) and l > -70 else x


def env(v, a=0.1, r=0.6):
    h = int(0.05 * SR); e = np.sqrt(np.convolve(v ** 2, np.ones(h) / h, mode='same')); act = (e > 10 ** (-40 / 20)).astype(float)
    out = np.zeros_like(act); ka, kr = 1 - np.exp(-1 / (a * SR)), 1 - np.exp(-1 / (r * SR)); y = 0.0
    step = 240; idx = np.arange(0, len(act), step); vals = []
    for i in idx: x = act[i]; y += (ka * step if x > y else kr * step) * (x - y); y = min(1, max(0, y)); vals.append(y)
    return np.interp(np.arange(len(act)), idx, vals)


def main():
    B = json.loads((EP / 'BANG-SHOT-v2.json').read_text()); T = B['tong']['thoi_luong_s']; n = int(round(T * SR))
    vo, sr = sf.read('/var/tmp/anim/am/loi-dung.wav', dtype='float64'); vo = np.pad(vo, (0, max(0, n - len(vo))))[:n]
    e = env(vo)
    # nhạc theo chương
    ch_t0 = {}
    for r in B['shot']: ch_t0.setdefault(r['phan'], r['t0'])
    mus = np.zeros(n); cue = []; ks = [k for k, _ in NHAC]
    tracks = [(k, f) for k, f in NHAC if f]
    for i, (k, f) in enumerate(tracks):
        a = ch_t0[k]; b = ch_t0[tracks[i + 1][0]] if i + 1 < len(tracks) else T
        x = lufs_norm(load(MUS / f), -20.0); L = int((b - a + 3) * SR); x = np.tile(x, int(np.ceil(L / len(x))))[:L]
        fi, fo = int(2.0 * SR), int(3.0 * SR); x[:fi] *= np.linspace(0, 1, fi); x[-fo:] *= np.linspace(1, 0, fo)
        s0 = int(a * SR); s1 = min(n, s0 + len(x)); mus[s0:s1] += x[:s1 - s0]; cue.append({'chuong': k, 'tep': f, 't0': round(a, 3), 't1': round(min(T, b + 3), 3), 'giay_phep': 'CC BY 4.0 (Scott Buckley) — RIGHTS K2-MUS-6…13 / T3-MUS-DUNG'})
    pp0 = [r for r in B['shot'] if r['cu_may'] == 'PP'][0]['t0']; k = int((pp0 - 4) * SR); mus[k:] *= np.linspace(1, 0.55, n - k)
    # SFX theo shot
    sfx = np.zeros(n); dung = {}; cache = {}
    for r in B['shot']:
        for (sid, db) in S.get(r['ma'], []):
            if sid not in cache: cache[sid] = lufs_norm(load(SFX / f'{sid}.ogg'), -23.0)
            x = cache[sid]; s0 = int(r['t0'] * SR); L = int(r['dur'] * SR); off = (zlib.crc32(r['ma'].encode()) % 997) * 480 % max(1, len(x) - 1)
            y = np.tile(np.roll(x, -off), int(np.ceil(L / len(x))) + 1)[:L] * 10 ** (db / 20); f = min(int(0.3 * SR), L // 4)
            y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f); sfx[s0:s0 + L] += y[:max(0, min(L, n - s0))]; dung.setdefault(sid, 0.0); dung[sid] += r['dur']
    g_m = 10 ** ((-14 * e) / 20); g_s = 10 ** ((-8 * e) / 20)
    mix = vo + mus * g_m * 10 ** (-4 / 20) + sfx * g_s
    st = np.stack([mix, mix], 1); m = pyln.Meter(SR); li = m.integrated_loudness(st); st = (st * 10 ** ((-14.0 - li) / 20)).astype(np.float32)   # đo trên 2 kênh (BS.1770 cộng kênh)
    OUT.mkdir(parents=True, exist_ok=True); pre = OUT / 'am-truoc-gioi-han.wav'; sf.write(pre, st, SR, subtype='FLOAT')
    ra = OUT / 'am-nhap.wav'
    subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', str(pre), '-af', 'aresample=192000,alimiter=limit=0.8:level=false:attack=2:release=50,aresample=48000', '-c:a', 'pcm_s24le', str(ra)], check=True)
    o = subprocess.run(['ffmpeg', '-nostdin', '-hide_banner', '-i', str(ra), '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = float(o.split('I:')[-1].split('LUFS')[0]); TP = float(o.split('Peak:')[-1].split('dBFS')[0])
    rec = {'thoi_luong_s': T, 'I_LUFS': I, 'TP_dBTP': TP, 'nhac': cue, 'sfx_giay': {k: round(v, 2) for k, v in sorted(dung.items())}, 'sfx_shot': S,
           'nguon_sfx': 'reports/sfx-t3/ung-vien/ung-vien.json (CC0 BigSoundBank/OpenGameArt; NPS tài sản công Mỹ)', 'muc_nhac_duoi_loi_dB': -14, 'muc_sfx_duoi_loi_dB': -8, 'mix_cuoi': False}
    (AN / 'am-cue.json').write_text(json.dumps(rec, ensure_ascii=False, indent=1)); print(json.dumps({k: rec[k] for k in ('I_LUFS', 'TP_dBTP')}))


if __name__ == '__main__': main()
