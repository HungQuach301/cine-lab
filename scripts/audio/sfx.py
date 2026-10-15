#!/opt/cine/bin/python
"""ÂM THANH · SFX gắn biến cố hình (phiên Âm thanh, Mốc C, 15/10/2026).

Thư viện nhỏ assets/audio/sfx/ (LIBRARY.yaml: id, loại, tệp, nguồn, giấy phép, SHA-256):
  coin_drop     xu rơi/chồng xu        — Kenney "Impact Sounds" impactMetal_light + "RPG Audio" handleCoins (CC0)
  paper_drop    phiếu/giấy rơi xuống   — Kenney "Casino Audio" card-place (CC0)
  camera_move   máy lặn/trượt mạnh     — whoosh tự tổng hợp (mã scripts/audio/sfx.py synth, thuộc dự án)
  palette_shift chuyển bảng màu        — "shimmer" tự tổng hợp (hợp âm sin + nhiễu khí, thuộc dự án)
Mỗi loại có ≥ 3 biến thể; chọn xoay vòng theo băm (loại, thời điểm) để không lặp một mẫu liền nhau.

API — khai trong đặc tả tập (khoá `sfx_events`), mốc theo LỜI:
  sfx_events:
  - {seg: '03', at: '@coins+0.05', kind: coin_drop, n: 4, gain_db: 0}   # "@từ[#n][±giây]" như ll.py, hoặc giây trong đoạn
  - {at_abs: 512.3, kind: paper_drop}                                   # giây tuyệt đối
  - {seg: '05', at: 2.0, file: assets/k2/sfx/typewriter.mp3, dur: 1.2}  # tệp bất kỳ đã có dòng RIGHTS
Tự suy từ cảnh 3D (auto, tắt bằng `sfx_auto: false`), đổi giây-trong-cảnh → giây phim qua shot đang hiện (speed, off):
  relief cols kind 'coins' t:[t0,t1]  → coin_drop rải trong [t0, t1] (≤ 6 tiếng, nhanh dần)
  relief/k2v sepia|natural: [t0, t1]  → palette_shift tại t0
  cam: mốc liền nhau đổi độ cao/khoảng cách ≥ 2,5× trong ≤ 3 s (hoặc ≥ 4× trong ≤ 6 s) → camera_move, tâm ở giữa đoạn đổi
Biến cố cách nhau < 0,25 s cùng loại thì gộp. Mức mặc định đặt dưới lời (master.py còn hạ nền theo lời, SFX hạ ½).

  sfx.py lib                         → dựng lại thư viện (cần các gói Kenney đã tải ở /var/tmp/cine-out/am-thanh/dl)
  sfx.py build <timeline.json> <episode.yaml|-> <ra.flac>   → stem SFX + nhật ký JSON
"""
import hashlib, json, math, os, re, sys
import numpy as np
import yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'll'))
import lib

SR = lib.SR
LIBD = os.path.join(lib.REPO, 'assets/audio/sfx')
GAIN = dict(coin_drop=-10.0, paper_drop=-9.0, camera_move=-16.0, palette_shift=-18.0)   # dB so với mẫu đã chuẩn −20 LUFS đỉnh ngắn


# ---------- tổng hợp (tài sản thuộc dự án) ----------
def _pink(n, rng):
    w = rng.standard_normal(n); f = np.fft.rfft(w); k = np.arange(len(f)); k[0] = 1; return np.fft.irfft(f / np.sqrt(k), n)


def whoosh(dur, seed, f0=250, f1=2600, f2=500):
    """nhiễu hồng qua lọc dải có tâm quét lên rồi xuống, bao hình chuông lệch, quét trái→phải"""
    from scipy.signal import butter, sosfilt
    rng = np.random.default_rng(seed); n = int(dur * SR); x = _pink(n + SR, rng)[:n]; out = np.zeros(n); B = 512
    u = np.linspace(0, 1, n); peak = 0.55
    fc = np.where(u < peak, f0 * (f1 / f0) ** (u / peak), f1 * (f2 / f1) ** ((u - peak) / (1 - peak)))
    for i in range(0, n, B):   # lọc theo khối, tâm đổi dần (chồng 50 % để mượt)
        c = float(fc[min(n - 1, i + B // 2)]); sos = butter(2, [c / 1.6, min(c * 1.6, SR / 2 - 100)], 'band', fs=SR, output='sos')
        seg = x[max(0, i - B):i + B]; y = sosfilt(sos, seg)[-min(B, n - i):]; out[i:i + len(y)] = y
    env = np.where(u < peak, (u / peak) ** 2.2, ((1 - u) / (1 - peak)) ** 1.6); y = out * env
    pan = np.clip(0.2 + 0.6 * u, 0, 1); st = np.stack([y * np.cos(pan * np.pi / 2), y * np.sin(pan * np.pi / 2)], 1)
    return st / (np.abs(st).max() + 1e-9) * 0.7


def shimmer(dur, seed, root=440.0):
    """hợp âm sin (1, 5/4, 3/2, 2, 9/4 × gốc) tách nhẹ L/R, vào chậm ra dài + nhiễu khí trên 4 kHz"""
    from scipy.signal import butter, sosfilt
    rng = np.random.default_rng(seed); n = int(dur * SR); t = np.arange(n) / SR; y = np.zeros((n, 2))
    for k, r in enumerate((1, 1.25, 1.5, 2, 2.25)):
        for ch, det in ((0, -0.7), (1, 0.7)):
            ph = rng.uniform(0, 2 * np.pi); y[:, ch] += np.sin(2 * np.pi * (root * r + det * (k + 1) * 0.3) * t + ph) / (k + 1.5)
    air = sosfilt(butter(2, 4000, 'high', fs=SR, output='sos'), rng.standard_normal(n)) * 0.08; y += air[:, None]
    a = 0.35 * dur; env = np.where(t < a, (t / a) ** 1.5, np.exp(-(t - a) / (0.33 * dur))); y *= env[:, None]
    fo = int(0.05 * SR); y[-fo:] *= np.linspace(1, 0, fo)[:, None]
    return y / (np.abs(y).max() + 1e-9) * 0.6


DL = '/var/tmp/cine-out/am-thanh/dl'
PICK = {   # (loại, id, nguồn trong gói, gói)
    'coin_drop': [('coin-1', 'kenney-impact-sounds/Audio/impactMetal_light_000.ogg', 'impact-sounds'), ('coin-2', 'kenney-impact-sounds/Audio/impactMetal_light_001.ogg', 'impact-sounds'),
                  ('coin-3', 'kenney-impact-sounds/Audio/impactMetal_light_002.ogg', 'impact-sounds'), ('coin-4', 'kenney-rpg/Audio/handleCoins2.ogg', 'rpg-audio')],
    'paper_drop': [('paper-1', 'kenney-casino-audio/Audio/card-place-1.ogg', 'casino-audio'), ('paper-2', 'kenney-casino-audio/Audio/card-place-2.ogg', 'casino-audio'),
                   ('paper-3', 'kenney-casino-audio/Audio/card-place-3.ogg', 'casino-audio'), ('paper-4', 'kenney-casino-audio/Audio/card-place-4.ogg', 'casino-audio')],
}
PACK = {'impact-sounds': ('Impact Sounds', 'https://kenney.nl/assets/impact-sounds', '029d734af1582474edf3a694d1b0cebc97c1c152f2f39fa34d4c2bafc5de77f8'),
        'rpg-audio': ('RPG Audio', 'https://kenney.nl/assets/rpg-audio', '6dbeaf8544da958d8f2adcb4a4a4b76c1ade34a05f8ab9edccd327da7375f38b'),
        'casino-audio': ('Casino Audio', 'https://kenney.nl/assets/casino-audio', 'f36250766ac5bc378c13708ddf12a23a8e54a3251f8d482c7536e51b5dbafa18')}


def build_lib():
    os.makedirs(LIBD, exist_ok=True); rows = []
    for kind, L in PICK.items():
        for sid, src, pk in L:
            out = os.path.join(LIBD, sid + '.ogg')
            lib.write(out, lib.dec(os.path.join(DL, src), 2), 'libvorbis', extra=('-q:a', '6'))
            name, url, zsha = PACK[pk]
            rows.append(dict(id=sid, loai=kind, tep=os.path.relpath(out, lib.REPO), sha256=lib.sha256(out), nguon=f'Kenney "{name}" ({url}), tệp gốc {os.path.basename(src)} trong zip SHA-256 {zsha}',
                             giay_phep='CC0 1.0 (License.txt trong gói; assets/audio/licenses/kenney-cc0.txt)', tac_gia='Kenney Vleugels (kenney.nl)'))
    for kind, fn, specs in (('camera_move', whoosh, [('whoosh-1', 0.9, 11), ('whoosh-2', 1.4, 12), ('whoosh-3', 2.0, 13)]),
                            ('palette_shift', shimmer, [('shimmer-1', 2.4, 21), ('shimmer-2', 3.0, 22), ('shimmer-3', 2.4, 23)])):
        for sid, d, seed in specs:
            x = fn(d, seed) if kind == 'camera_move' else fn(d, seed, root={21: 440.0, 22: 392.0, 23: 493.88}[seed])
            out = os.path.join(LIBD, sid + '.ogg'); lib.write(out, x, 'libvorbis', extra=('-q:a', '6'))
            rows.append(dict(id=sid, loai=kind, tep=os.path.relpath(out, lib.REPO), sha256=lib.sha256(out), nguon=f'tự tổng hợp: scripts/audio/sfx.py {fn.__name__}(dur={d}, seed={seed})',
                             giay_phep='thuộc dự án (mã của dự án tạo ra, không dùng mẫu ngoài)', tac_gia='CINE LAB'))
    yaml.safe_dump(dict(version=1, ghi_chu='Thư viện SFX gắn hình — phiên Âm thanh 15/10/2026; dòng RIGHTS: AM-01…', mau=rows), open(os.path.join(LIBD, 'LIBRARY.yaml'), 'w'),
                   allow_unicode=True, sort_keys=False)
    return rows


def library():
    return yaml.safe_load(open(os.path.join(LIBD, 'LIBRARY.yaml')))['mau']


# ---------- biến cố ----------
def scene_to_film(TL):
    """{hero_key: [(t_phim_đầu, t_phim_cuối, t0_shot_phim, speed, off_s)]}"""
    M = {}
    for s in TL['segments']:
        for sh in s['shots']:
            p = sh.get('p') or {}
            if sh.get('tpl') == 'plate' and p.get('hero'):
                M.setdefault(p['hero'], []).append((s['t0'] + sh['t0'], s['t0'] + sh['t1'], s['t0'] + sh['t0'], p.get('speed', 1) or 1, (p.get('off') or 0) / 24))
    return M


def to_film(M, key, s_scene):
    out = []
    for a, b, t0, sp, off in M.get(key, []):
        t = t0 + (s_scene - off) / sp
        if a - 1e-3 <= t <= b + 1e-3: out.append(t)
    return out


def auto_events(TL):
    H = TL.get('heroes') or {}; M = scene_to_film(TL); ev = []
    for k, h in H.items():
        o = h.get('opt') or {}; dur = float(h.get('dur', 0))
        for c in o.get('cols', []) or []:
            if c.get('kind') == 'coins' and isinstance(c.get('t'), list):
                t0, t1 = c['t']; n = int(min(6, max(2, c.get('n', 4)))); fr = [((i / (n - 1)) ** 0.7) for i in range(n)]
                for f in fr:
                    for t in to_film(M, k, t0 + f * (t1 - t0)): ev.append(dict(t=t, kind='coin_drop', why=f'{k}: cols {c.get("id")}'))
        for key in ('sepia', 'natural'):
            if isinstance(o.get(key), list):
                for t in to_film(M, k, o[key][0]): ev.append(dict(t=t, kind='palette_shift', why=f'{k}: {key} {o[key]}'))
        cam = o.get('cam')
        if isinstance(cam, list) and len(cam) > 1 and all(isinstance(q, dict) for q in cam):
            tt = [q.get('t', q.get('u', 0) * dur if 'u' in q else None) for q in cam]
            ht = [q.get('alt', q.get('dist')) for q in cam]
            for i in range(len(cam) - 1):
                if None in (tt[i], tt[i + 1], ht[i], ht[i + 1]) or not ht[i] or not ht[i + 1]: continue
                dt = tt[i + 1] - tt[i]; r = max(ht[i], ht[i + 1]) / min(ht[i], ht[i + 1])
                if (r >= 2.5 and 0 < dt <= 3.0) or (r >= 4.0 and 0 < dt <= 6.0):
                    for t in to_film(M, k, (tt[i] + tt[i + 1]) / 2): ev.append(dict(t=t, kind='camera_move', why=f'{k}: cam {i}→{i + 1} ×{r:.1f} trong {dt:.1f} s', span=dt))
    return ev


def manual_events(TL, E):
    import ll
    seg = {s['id']: s for s in TL['segments']}; ev = []
    for i, e in enumerate((E or {}).get('sfx_events', []) or []):
        if 'at_abs' in e: t = float(e['at_abs'])
        else:
            s = seg.get(str(e['seg']))
            if not s: raise SystemExit(f'sfx_events[{i}]: không có đoạn {e.get("seg")}')
            if isinstance(e['at'], str):
                W = ll.words(json.load(open(lib.P(s['vo_file'][:-4] + '.align.json')))); t = ll.anchor(e['at'], W, s['vo_offset'], f'sfx_events[{i}]') + s['t0']
            else: t = s['t0'] + float(e['at'])
        for j in range(int(e.get('n', 1))):
            ev.append(dict(t=t + j * float(e.get('step', 0.09)), kind=e.get('kind'), file=e.get('file'), dur=e.get('dur'), src_ss=e.get('src_ss', 0),
                           gain_db=e.get('gain_db', 0), why=f'sfx_events[{i}] {e.get("at", e.get("at_abs"))}'))
    return ev


def build(TL, E=None, total=None):
    total = total or TL['tong_s']; N = int(round(total * SR)); out = np.zeros((N, 2)); L = library(); log = []
    ev = (auto_events(TL) if (E or {}).get('sfx_auto', True) else []) + manual_events(TL, E)
    ev.sort(key=lambda e: e['t']); keep = []
    for e in ev:   # gộp biến cố cùng loại cách < 0,25 s
        if keep and keep[-1]['kind'] == e['kind'] and e.get('file') is None and e['t'] - keep[-1]['t'] < 0.25: continue
        keep.append(e)
    cache = {}
    for e in keep:
        if e.get('file'):
            x = lib.dec(e['file'], 2, ss=e.get('src_ss', 0), dur=e.get('dur')); src = e['file']; g = float(e.get('gain_db', 0)) - 12
        else:
            V = [r for r in L if r['loai'] == e['kind']]
            if not V: raise SystemExit(f'sfx: không có mẫu loại {e["kind"]}')
            if e['kind'] == 'camera_move':   # biến thể có độ dài gần đoạn máy lặn nhất
                r = min(V, key=lambda r: abs(float(r['nguon'].split('dur=')[1].split(',')[0]) - e.get('span', 1.4)) if 'dur=' in r['nguon'] else 9)
            else:
                r = V[int(hashlib.sha1(f"{e['kind']}{e['t']:.2f}".encode()).hexdigest(), 16) % len(V)]
            if r['tep'] not in cache:
                y = lib.dec(r['tep'], 2); cache[r['tep']] = y / (np.abs(y).max() + 1e-9) * 0.5
            x = cache[r['tep']]; src = r['tep']; g = GAIN[e['kind']] + float(e.get('gain_db', 0))
        lead = len(x) * 0.5 / SR if e['kind'] == 'camera_move' else (0.35 * len(x) / SR if e['kind'] == 'palette_shift' else 0.0)   # tâm whoosh/đỉnh shimmer trùng biến cố
        k0 = int(round((e['t'] - lead) * SR)); x2 = x * 10 ** (g / 20)
        if k0 < 0: x2 = x2[-k0:]; k0 = 0
        m = min(len(x2), N - k0)
        if m > 0: out[k0:k0 + m] += x2[:m]
        log.append(dict(t=round(e['t'], 3), loai=e['kind'], tep=src, gain_db=round(g, 1), ly_do=e.get('why')))
    return out, log


if __name__ == '__main__':
    if len(sys.argv) < 2: sys.exit(__doc__)
    if sys.argv[1] == 'lib':
        for r in build_lib(): print(r['id'], r['loai'], r['sha256'][:12], r['tep'])
    elif sys.argv[1] == 'build':
        TL = json.load(open(sys.argv[2])); E = yaml.safe_load(open(sys.argv[3])) if sys.argv[3] != '-' else None
        x, log = build(TL, E); lib.write(sys.argv[4], x, 'flac', extra=('-sample_fmt', 's32')); print(json.dumps(log, ensure_ascii=False, indent=1))
