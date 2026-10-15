#!/opt/cine/bin/python
"""ÂM THANH · nhạc theo chương (phiên Âm thanh, Mốc C, 15/10/2026).

API (khai trong đặc tả tập, khoá `music`, tương thích ngược với scripts/ll/mix.py):
  music:
  - file: assets/k2/music/Half-Mystery.mp3   # chỉ tài sản có dòng RIGHTS.md
    from: '00'            # id đoạn (chương) bắt đầu cue — hoặc at: <giây tuyệt đối>
    ss: 0                 # giây vào trong bài (được nắn tới phách/ô nhịp gần nhất phía sau)
    gain_db: -1           # cộng sau chuẩn −24 LUFS của cue
    intensity: mid        # low (−5 dB, lọc thấp 2,5 kHz) | mid (0) | high (+2,5 dB) | số dB
    xfade: 3              # giây giao bài (làm tròn về số ô nhịp nguyên của bài đang chạy)
    align: bar            # bar | beat | none — điểm giao rơi đúng vạch ô nhịp (hoặc phách) của bài cũ, phách mạnh bài mới trùng điểm đó
    continue: false       # true = vẫn bài trước, chỉ đổi cường độ ở vạch ô nhịp (dốc 1 ô nhịp, cùng vị trí trong bài nên liền mạch)
    bpm: 72               # gợi ý tempo cho bộ dò phách (tuỳ chọn; lấy từ RIGHTS.md)
  KHÔNG lặp nhạc (Q28): bài ngắn hơn khoảng cần → lỗi.

  music.py grid <bài.mp3> [--bpm 72]                → in tempo, phách, vạch ô nhịp (cache /var/tmp/cine-out/am-thanh/beats)
  music.py build <timeline.json> <ra.flac> [--json] → dựng nền nhạc theo timeline (TL['music'] hoặc --cues cues.yaml)

Giao bài: crossfade công suất bằng nhau (cos/sin) dài X = n ô nhịp, tâm tại Tc = vạch ô nhịp của bài cũ gần ranh giới chương nhất
(trong ±1 ô nhịp); bài mới đặt sao cho phách mạnh đầu tiên sau `ss` rơi đúng Tc. Ô nhịp = 4 phách, pha chọn theo năng lượng dải trầm
tại phách (librosa không cho phách mạnh — đây là ước, ghi trong báo cáo). Đổi cường độ trong cùng bài: dốc tuyến tính 1 ô nhịp (tín hiệu tương quan).
"""
import hashlib, json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib

SR = lib.SR
CACHE = os.environ.get('AUDIO_CACHE', '/var/tmp/cine-out/am-thanh/beats')
INT = {'low': (-5.0, 2500), 'mid': (0.0, None), 'high': (2.5, None)}
META = __import__('yaml').safe_load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'music-meta.yaml'))) or {}   # bpm/align theo RIGHTS.md


def meta(f):
    return META.get(os.path.relpath(lib.P(f), lib.REPO), {})


def grid(path, bpm=None):
    key = hashlib.sha1((lib.sha256(path) + str(bpm)).encode()).hexdigest()[:16]; cp = os.path.join(CACHE, key + '.json')
    if os.path.exists(cp): return json.load(open(cp))
    import librosa
    y = lib.dec(path, 1, sr=22050)[:, 0].astype(np.float32)
    tempo, beats = librosa.beat.beat_track(y=y, sr=22050, units='time', start_bpm=float(bpm or 120), tightness=200 if bpm else 100)
    tempo = float(np.atleast_1d(tempo)[0]); beats = np.asarray(beats, float)
    # pha ô nhịp: phách có năng lượng dải trầm (< 200 Hz) lớn nhất theo chu kỳ 4
    import scipy.signal as ss
    lo = ss.sosfilt(ss.butter(4, 200, 'low', fs=22050, output='sos'), y); e = np.array([np.abs(lo[int(b * 22050):int(b * 22050) + 2205]).mean() for b in beats])
    ph = int(np.argmax([e[k::4].mean() if len(e[k::4]) else 0 for k in range(4)])) if len(e) >= 8 else 0
    G = dict(file=os.path.relpath(lib.P(path), lib.REPO), bpm=round(tempo, 2), beats=[round(b, 4) for b in beats], bars=[round(b, 4) for b in beats[ph::4]],
             dur=round(len(y) / 22050, 3), pha=ph, bpm_goi_y=bpm)
    os.makedirs(CACHE, exist_ok=True); json.dump(G, open(cp, 'w')); return G


def nearest(arr, x, lo=None, hi=None):
    a = np.asarray(arr); m = np.ones(len(a), bool)
    if lo is not None: m &= a >= lo
    if hi is not None: m &= a <= hi
    if not m.any(): return None
    i = np.argmin(np.abs(a[m] - x)); return float(a[m][i])


def first_after(arr, x):
    a = np.asarray(arr); a = a[a >= x - 1e-6]; return float(a[0]) if len(a) else None


def cue_level(c):
    it = c.get('intensity', 'mid'); g, lp = INT[it] if isinstance(it, str) else (float(it), None)
    return g + float(c.get('gain_db', 0)), c.get('lpf', lp)


def build(TL, cues=None, total=None):
    """→ (nền nhạc (N, 2), nhật ký cue). Mốc theo TL['segments'][i]['t0']."""
    M = cues if cues is not None else (TL.get('music') or []); total = total or TL['tong_s']; N = int(round(total * SR)); bed = np.zeros((N, 2)); log = []
    if not M: return bed, log
    seg0 = {s['id']: s['t0'] for s in TL['segments']}
    T = []
    for c in M:
        if 'at' in c: T.append(float(c['at']))
        elif str(c.get('from')) in seg0: T.append(seg0[str(c.get('from'))])
        else: raise SystemExit(f"music: cue trỏ tới đoạn không có: {c.get('from')}")
    # pha 1: điểm giao Tc, độ dài giao X và vị trí đọc của từng cue
    P = []
    for i, c in enumerate(M):
        G = grid(c['file'], c.get('bpm') or meta(c['file']).get('bpm')); align = c.get('align') or meta(c['file']).get('align', 'bar')
        if i > 0 and align != 'none' and (meta(P[-1]['c']['file']).get('align') == 'none'): align = 'none'   # bài cũ không có phách tin được
        if i == 0:
            ss0 = float(c.get('ss', 0)); P.append(dict(c=c, G=G, a0=T[0], ss=ss0, tc=T[0], X=0.0, align=align)); continue
        A = P[-1]; GA = A['G']; Ag = GA['bars'] if align == 'bar' else GA['beats']
        tl = [A['a0'] + (b - A['ss']) for b in Ag]   # lưới của bài cũ trên trục phim
        barA = 4 * 60.0 / GA['bpm']
        tc = nearest(tl, T[i], lo=max(T[i] - barA, A['tc'] + barA), hi=T[i] + barA) if align != 'none' else None
        tc = T[i] if tc is None else tc
        if c.get('continue'):
            if c['file'] != A['c']['file']: raise SystemExit(f"music: cue {i} continue nhưng khác bài ({c['file']})")
            P.append(dict(c=c, G=GA, a0=A['a0'], ss=A['ss'], tc=tc, X=barA, cont=True, align=align)); continue
        xf = float(c.get('xfade', 3)); nb = max(1, int(round(xf / barA))); X = min(nb * barA, 2 * xf + barA) if align != 'none' else xf
        Bg = G['bars'] if align == 'bar' else G['beats']; want = float(c.get('ss', 0))
        bB = first_after(Bg, want + X / 2) if align != 'none' else want + X / 2
        if bB is None: raise SystemExit(f"music: {c['file']} không còn phách sau {want} s")
        P.append(dict(c=c, G=G, a0=tc - X / 2, ss=bB - X / 2, tc=tc, X=X, beatB=bB, align=align))
    # pha 2: dựng
    for i, p in enumerate(P):
        c = p['c']; g, lp = cue_level(c); nxt = P[i + 1] if i + 1 < len(P) else None
        start = p['tc'] if p.get('cont') else p['a0']; end = (nxt['tc'] + nxt['X'] / 2) if nxt else total
        if nxt and nxt.get('cont'): end = nxt['tc'] + nxt['X']
        need = end - start; rd = p['ss'] + (start - p['a0'])
        if rd < 0: raise SystemExit(f"music: cue {i} đọc trước đầu bài ({rd:.2f} s)")
        src = lib.dec(c['file'], 2, af=(f'lowpass=f={lp}' if lp else None), ss=rd, dur=need + 0.1)
        if len(src) < int(need * SR) - 1:
            raise SystemExit(f"music: {c['file']} từ {rd:.1f} s chỉ còn {len(src) / SR:.1f} s, cần {need:.1f} s (Q28: không lặp nhạc)")
        x = src[:int(need * SR)].copy(); n = len(x)
        # chuẩn −24 LUFS đo trên ≤ 240 s đầu của đoạn dùng (cue continue dùng chung hệ số của cue gốc)
        ref = P[i - 1]['_ref'] if p.get('cont') else lib.integrated(lib.dec(c['file'], 2, ss=p['ss'], dur=min(240, need + 1)))
        p['_ref'] = ref   # đo trên bản CHƯA lọc: cường độ low nhỏ hơn đúng phần lọc cắt + gain
        x *= 10 ** ((-24.0 + g - ref) / 20)
        u = lambda k: np.linspace(0, 1, k)[:, None]
        if i > 0:
            k = min(n, int(p['X'] * SR))
            x[:k] *= u(k) if p.get('cont') else np.sin(np.pi / 2 * u(k))
        if nxt:
            k = min(n, int(nxt['X'] * SR))
            x[-k:] *= (1 - u(k)) if nxt.get('cont') else np.cos(np.pi / 2 * u(k))
        k0 = int(round(start * SR)); m = min(n, N - k0); bed[k0:k0 + m] += x[:m]
        log.append(dict(file=c['file'], intensity=c.get('intensity', 'mid'), gain_db=round(g, 2), lpf=lp, t0=round(start, 3), t1=round(end, 3), ranh_gioi=round(T[i], 3),
                        diem_giao=round(p['tc'], 3), lech_ranh_gioi_s=round(p['tc'] - T[i], 3), giao_s=round(p['X'], 3), ss_doc=round(rd, 3), src_to=round(rd + need, 2),
                        bpm=p['G']['bpm'], tiep_bai=bool(p.get('cont')), align=p.get('align')))
    fi = min(N, int(1.5 * SR)); bed[:fi] *= np.linspace(0, 1, fi)[:, None]
    return bed, log


if __name__ == '__main__':
    if len(sys.argv) < 3: sys.exit(__doc__)
    if sys.argv[1] == 'grid':
        b = float(sys.argv[sys.argv.index('--bpm') + 1]) if '--bpm' in sys.argv else None; G = grid(sys.argv[2], b)
        print(json.dumps(dict(file=G['file'], bpm=G['bpm'], so_phach=len(G['beats']), so_o=len(G['bars']), o_dau=G['bars'][:6], dur=G['dur']), ensure_ascii=False))
    elif sys.argv[1] == 'build':
        import yaml
        TL = json.load(open(sys.argv[2])); cues = yaml.safe_load(open(sys.argv[sys.argv.index('--cues') + 1])) if '--cues' in sys.argv else None
        bed, log = build(TL, cues); lib.write(sys.argv[3], bed, 'flac', extra=('-sample_fmt', 's32'))
        print(json.dumps(log, ensure_ascii=False, indent=1))
