#!/opt/cine/bin/python
"""ANIMATIC-T4-V2 · việc 6 — ÂM THANH NHÁP v3 (như am.py của ANIMATIC-T4: không phải mix cuối): lời dựng v3 (loi_v3.py, −14 LUFS) + SFX nháp theo shot v3
(CC0 BigSoundBank/OpenGameArt + NPS từ reports/sfx-t3/ung-vien; MỚI: chuông nhà thờ + còi báo động CC0 BigSoundBank — reports/animatic-t4-v2/sfx/sfx.json)
+ nhạc nháp Scott Buckley CC BY 4.0 theo chương (MÓC bắt đầu ở M00). Nén nhạc/SFX dưới lời; chuẩn −14 LUFS, giới hạn đỉnh. Ra: $ANIM_OUT/am-nhap.wav + animatic2/am-cue.json."""
import json, os, subprocess, zlib
from pathlib import Path
import numpy as np, soundfile as sf, pyloudnorm as pyln
import am as A0
REPO = A0.REPO; EP = A0.EP; AN2 = EP / 'animatic2'; SR = A0.SR; OUT = Path(os.environ.get('ANIM_OUT', '/var/tmp/anim/out3'))
SFX3 = REPO / 'reports/animatic-t4-v2/sfx'
S = dict(A0.S)
S.update({'M00': [('LUAL-1', -8), ('DEM-1', -14), ('SONG-2', -14)], 'H1-01h': [('DEM-1', -10), ('LUAN-1', -14)], 'H1-02h': [('LUAN-1', -8), ('GIO-3', -14)],
 'H1-03b': [('GIO-3', -10), ('CHIM-1', -12)], 'H1-04b': [('DONG-2', -6), ('GIO-1', -10), ('LUAL-1', -16)], 'H1-05h': [('LUAL-1', -10), ('CHUONG-1', -14), ('SONG-2', -12)],
 'H1-06x': [('THUYEN-1', -4), ('SONG-2', -8), ('LUAL-1', -14)], 'H1-06b': [('THUYEN-2', -6), ('DAO-2', -6), ('DONG-2', -10)], 'H1-07b': [('LUAL-1', -6), ('SONG-1', -12)],
 'H1-11b': [('LUAL-3', -4), ('DAO-2', -10)], 'H1-12x': [('CHIM-1', -10), ('GIO-3', -12), ('CHUONG-1', -16)], 'H1-13a': [('LUAL-3', -6)], 'H1-13c': [('LUAL-3', -4), ('DAO-2', -12)],
 'H1-15m': [('NO-2', -4), ('DAO-2', -8)], 'H1-15b': [('DAO-1', -6), ('DEM-1', -12), ('LUAL-1', -18)], 'H1-15h': [('LUAL-1', -8), ('GIO-2', -12)], 'H1-15x': [('DONG-2', -6), ('NGUA-1', -10), ('LUAL-1', -12)],
 'H1-18a': [('GIO-3', -10)], 'H1-18t': [('GIO-3', -12)], 'H1-18b': [('GIO-3', -10), ('DAO-2', -14)], 'H2-00': [('GIO-3', -8), ('DAO-2', -14)], 'H2-02b': [('PHO-1', -18)],
 'H2-04h': [('DAO-1', -12), ('PHO-1', -14)], 'H2-05s': [('NGUA-1', -6), ('PHO-1', -10), ('DAO-1', -12)], 'H3-02t': [('SONG-2', -12)], 'H3-03t': [('SONG-2', -12), ('PHO-1', -14)],
 'H3-05b': [('GIO-1', -10), ('PHO-1', -14)], 'H4-01a': [('GIO-1', -10), ('COI-40', -10)], 'H4-02b': [('LUAL-2', -6), ('NO-2', -12), ('COI-40', -18)], 'H4-04d': [('LUAL-2', -4), ('NUOC-1', -10)],
 'H4-06t': [('GIO-2', -14)], 'H5-01b': [('PHO-1', -14)], 'H5-02s': [('PHO-1', -6), ('PHO-2', -10)], 'H5-05c': [('PHO-2', -12), ('CHIM-1', -14)], 'H5-07a': [('SONG-2', -6), ('PHO-3', -8)],
 'H2-14': [('PHO-1', -14), ('CHUONG-1', -12)], 'H3-01': [('PHO-1', -14), ('CHUONG-1', -14)], 'H5-08': [('PHO-3', -12), ('CHUONG-1', -18)]})


def sfx_path(sid):
    p = SFX3 / f'{sid}.ogg'
    return p if p.exists() else A0.SFX / f'{sid}.ogg'


def main():
    B = json.loads((EP / 'BANG-SHOT-v3.json').read_text()); T = B['tong']['thoi_luong_s']; n = int(round(T * SR))
    vo, sr = sf.read('/var/tmp/anim/am/loi-dung-v3.wav', dtype='float64'); assert sr == SR; vo = np.pad(vo, (0, max(0, n - len(vo))))[:n]
    e = A0.env(vo); ch_t0 = {}
    for r in B['shot']: ch_t0.setdefault(r['phan'], r['t0'])
    mus = np.zeros(n); cue = []; tracks = [(k, f) for k, f in A0.NHAC if f]
    for i, (k, f) in enumerate(tracks):
        a = ch_t0[k]; b = ch_t0[tracks[i + 1][0]] if i + 1 < len(tracks) else T
        x = A0.lufs_norm(A0.load(A0.MUS / f), -20.0); L = int((b - a + 3) * SR); x = np.tile(x, int(np.ceil(L / len(x))))[:L]
        fi, fo = int(2.0 * SR), int(3.0 * SR); x[:fi] *= np.linspace(0, 1, fi); x[-fo:] *= np.linspace(1, 0, fo)
        s0 = int(a * SR); s1 = min(n, s0 + len(x)); mus[s0:s1] += x[:s1 - s0]; cue.append({'chuong': k, 'tep': f, 't0': round(a, 3), 't1': round(min(T, b + 3), 3), 'giay_phep': 'CC BY 4.0 (Scott Buckley) — RIGHTS K2-MUS-6…13 / T3-MUS-DUNG'})
    pp0 = [r for r in B['shot'] if r['cu_may'] == 'PP'][0]['t0']; k = int((pp0 - 4) * SR); mus[k:] *= np.linspace(1, 0.55, n - k)
    sfx = np.zeros(n); dung = {}; cache = {}; thieu = []
    for r in B['shot']:
        for (sid, db) in S.get(r['ma'], []):
            p = sfx_path(sid)
            if not p.exists(): thieu.append(sid); continue
            if sid not in cache: cache[sid] = A0.lufs_norm(A0.load(p), -23.0)
            x = cache[sid]; s0 = int(r['t0'] * SR); L = int(r['dur'] * SR); off = (zlib.crc32(r['ma'].encode()) % 997) * 480 % max(1, len(x) - 1)
            y = np.tile(np.roll(x, -off), int(np.ceil(L / len(x))) + 1)[:L] * 10 ** (db / 20); f = min(int(0.3 * SR), L // 4)
            y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f); sfx[s0:s0 + L] += y[:max(0, min(L, n - s0))]; dung[sid] = dung.get(sid, 0.0) + r['dur']
    g_m = 10 ** ((-14 * e) / 20); g_s = 10 ** ((-8 * e) / 20)
    mix = vo + mus * g_m * 10 ** (-4 / 20) + sfx * g_s
    st = np.stack([mix, mix], 1); li = pyln.Meter(SR).integrated_loudness(st); st = (st * 10 ** ((-14.0 - li) / 20)).astype(np.float32)
    OUT.mkdir(parents=True, exist_ok=True); pre = OUT / 'am-truoc-gioi-han.wav'; sf.write(pre, st, SR, subtype='FLOAT'); ra = OUT / 'am-nhap.wav'
    subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', str(pre), '-af', 'aresample=192000,alimiter=limit=0.8:level=false:attack=2:release=50,aresample=48000', '-c:a', 'pcm_s24le', str(ra)], check=True)
    o = subprocess.run(['ffmpeg', '-nostdin', '-hide_banner', '-i', str(ra), '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = float(o.split('I:')[-1].split('LUFS')[0]); TP = float(o.split('Peak:')[-1].split('dBFS')[0])
    rec = {'thoi_luong_s': T, 'I_LUFS': I, 'TP_dBTP': TP, 'nhac': cue, 'sfx_giay': {k: round(v, 2) for k, v in sorted(dung.items())}, 'sfx_shot': {k: v for k, v in S.items() if any(r['ma'] == k for r in B['shot'])},
           'nguon_sfx': 'reports/sfx-t3/ung-vien/ung-vien.json (CC0 BigSoundBank/OpenGameArt; NPS tài sản công Mỹ) + reports/animatic-t4-v2/sfx/sfx.json (CC0 BigSoundBank: chuông, còi)',
           'sfx_thieu': sorted(set(thieu)), 'muc_nhac_duoi_loi_dB': -14, 'muc_sfx_duoi_loi_dB': -8, 'mix_cuoi': False}
    AN2.mkdir(parents=True, exist_ok=True); (AN2 / 'am-cue.json').write_text(json.dumps(rec, ensure_ascii=False, indent=1)); print(json.dumps({k: rec[k] for k in ('I_LUFS', 'TP_dBTP', 'sfx_thieu')}))


if __name__ == '__main__': main()
