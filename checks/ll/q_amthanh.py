#!/opt/cine/bin/python
"""Âm thanh A1–A13 — luật khoá bản 1.11.0 (phiên K, 15/10/2026; chủ dự án duyệt L6 15/10/2026). Kênh 2 (từ K2 tập 3).
Căn cứ: docs/AUDIO-THUOC-DO.md (phiên Âm thanh, 15/10/2026, nhánh am-thanh) — K viết lại phép đo, KHÔNG gọi scripts/audio/
(bản sao độc lập: đổi công cụ của xưởng không đổi nghĩa luật). Định nghĩa: checks/ll/RULES-LL.md (mục A1–A13).

  q_amthanh.py <episode.yaml> [--tl timeline.json] [--master master.mp4] [--mix mix.json] [--vo vo.flac --bed bed.flac]
               [--no-asr] [--json ra.json]

ÁP DỤNG: tập dựng bằng chuỗi âm thanh mới (MIX=audio: mix.json có `cong_cu: scripts/audio/master.py`) → các mục CHẶN quyết kết quả.
Tập cũ (mix.json của scripts/ll/mix.py, hoặc không có mix.json): mọi mục CHỈ BÁO (đo được gì báo nấy), kết quả "CHỈ BÁO".

Đo trên bản PHÁT HÀNH (master mp4, luồng âm AAC giải mã lại), trừ A4/A9 (stem / tệp lời) và A8/A10 (timeline):
  A1  CHẶN  loudness tích hợp (ffmpeg ebur128, BS.1770-4) −15,0 ≤ I ≤ −13,8 LUFS (mục tiêu −14,0; mép trên đã gồm dung sai đo +0,2)
  A2  CHẶN  đỉnh thật (ebur128 peak=true, nâng mẫu ×4) trên luồng đã giải mã SAU AAC ≤ −1,0 dBTP
  A3  báo   biên độ loudness LRA: báo khi < 2,0 hoặc > 8,0 LU
  A4  CHẶN  lời trên nhạc (SMR, lọc K): p10 ≥ 15 dB và min ≥ 12 dB trên cửa sổ 3 s bước 1 s nằm trọn trong khoảng lời. Nguồn số:
            stem lời + stem nền đã xử lý (--vo/--bed) khi có — K tự tính; không có stem thì đọc `smr` trong mix.json (master.py đo trên stem
            đã xử lý). Thiếu cả hai → TRƯỢT.
  A5  CHẶN  0 khoảng lặng bất thường: loudness tức thời 400 ms < −50 LUFS kéo dài ≥ 1,0 s, bỏ 2 s đầu/cuối
  A6  báo   tỉ lệ thời gian loudness tức thời < −50 LUFS
  A7  CHẶN  0 chạm trần: chuỗi ≥ 3 mẫu liền |x| ≥ 0,999 (kênh bất kỳ) trên tín hiệu giải mã
  A8  CHẶN  0 chồng lời: hai đoạn lời phát cùng lúc (khoảng [lời đầu, lời cuối] của các đoạn liền nhau giao nhau), đọc timeline
  A9  CHẶN  ASR đọc đúng 100 % đoạn THEO HAI CÁCH NGHE: faster-whisper small.en (1) beam 5 và (2) tham lam beam 1 (nhiệt 0, không VAD,
            không hotword); mọi số (so theo GIÁ TRỊ, bộ đọc số Q28f) và tên riêng (giống ≥ 0,75) của lời khoá phải có trong CẢ HAI bản nghe.
            Bản nghe được thêm dạng tách gạch nối giữa hai chữ ("Minneapolis-fed" → "Minneapolis fed"; đo T1 15/10: báo nhầm "Fed").
            Miễn: câu khai ở đoạn đặc tả `asr_mo_ho: [{cau: "<nguyên văn câu trong lời>", ly_do: "<≥ 20 ký tự>"}]` — chấm bằng tai (G2),
            liệt kê trong báo cáo; câu khai không có trong lời hoặc lý do ngắn → TRƯỢT.
  A10 báo   quãng không lời > 8 s (gộp nghỉ < 0,55 s) mà đoạn không khai `khoanh_khac_nhac: [[t0, t1], …]` (giây trong đoạn) phủ quãng đó
  A11 CHẶN  giao nhạc (mix.json `nhac[]`): |lệch điểm giao − ranh giới chương| ≤ 1 ô nhịp (4 phách theo bpm của bài ĐANG chạy);
            không lặp: cue không đọc quá cuối bài, không cue lặp vòng, cùng bài dùng lại ≤ 60 s nguồn (Q28a)
  A12 CHẶN  loudnorm tuyến tính: mix.json `loudness[-1].loudnorm.normalization_type == linear`
  A13 báo   đồng bộ tiếng: trễ luồng âm master so với stem lời (tương quan chéo trên ≤ 120 s có lời) — chỉ khi có --vo; báo khi > 5 ms
Trong ±5 % quanh ngưỡng (A1, A2, A4): nêu tên (sát ngưỡng).
"""
import hashlib, json, os, re, subprocess, sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from checks.ll import base  # noqa: E402

SR = 48000
I_MIN, I_MAX, I_TARGET = -15.0, -13.8, -14.0
TP_MAX = -1.0
LRA_LO, LRA_HI = 2.0, 8.0
SMR_P10, SMR_MIN, SMR_WIN, SMR_HOP = 15.0, 12.0, 3.0, 1.0
SIL_LUFS, SIL_MIN, EDGE = -50.0, 1.0, 2.0
CLIP_LVL, CLIP_RUN = 0.999, 3
GAP_MERGE, GAP_MAX = 0.55, 8.0
MUSIC_REPEAT_MAX = 60.0
SYNC_MAX_MS = 5.0
LY_DO_MIN = 20
ASR_MODEL = 'small.en'
NEW_CHAIN = 'scripts/audio/master.py'
# BS.1770-4, lọc K ở 48 kHz (hai tầng): tiền lọc kệ cao + RLB thông cao
_KB1, _KA1 = [1.53512485958697, -2.69169618940638, 1.19839281085285], [1.0, -1.69065929318241, 0.73248077421585]
_KB2, _KA2 = [1.0, -2.0, 1.0], [1.0, -1.99004745483398, 0.99007225036621]


def P(p): return p if os.path.isabs(p) else os.path.join(base.REPO, p)


def mmss(t): return f'{int(t // 60)}:{t % 60:04.1f}'


# ---------------------------------------------------------------- đo
def ebur128(path):
    """(I LUFS, LRA LU, TP dBTP) — ffmpeg ebur128 trên luồng âm đầu tiên (giải mã AAC nếu là mp4)"""
    r = subprocess.run(['ffmpeg', '-nostats', '-nostdin', '-i', P(path), '-map', '0:a:0', '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                       capture_output=True, text=True).stderr
    s = r[r.rfind('Summary:'):]; g = lambda k: float(s.split(k)[1].split()[0])
    return g('I:'), g('LRA:'), g('Peak:')


def decode(path, ch=2):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-nostdin', '-i', P(path), '-map', '0:a:0', '-ac', str(ch), '-ar', str(SR), '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, ch)


def kblocks(x, blk=0.1):
    """công suất lọc K (tổng kênh) từng khối 100 ms"""
    from scipy.signal import lfilter
    n = int(blk * SR); nb = len(x) // n; e = np.zeros(nb)
    for c in range(x.shape[1]):
        y = lfilter(_KB2, _KA2, lfilter(_KB1, _KA1, x[:, c].astype(np.float64)))
        e += (y[:nb * n] ** 2).reshape(nb, n).mean(1); del y
    return e


def momentary(x):
    """loudness tức thời 400 ms, bước 100 ms → (t tâm, LUFS); cùng định nghĩa docs/AUDIO-THUOC-DO.md A5/A6"""
    e = kblocks(x); k = 4
    if len(e) < k: return np.array([len(x) / SR / 2]), np.array([-70.0])
    c = np.concatenate([[0.0], np.cumsum(e)]); p = (c[k:] - c[:-k]) / k
    return np.arange(len(p)) * 0.1 + 0.2, -0.691 + 10 * np.log10(np.maximum(p, 1e-20))


def runs(mask):
    m = np.concatenate([[False], np.asarray(mask, bool), [False]]).astype(np.int8); d = np.diff(m)
    return list(zip(np.where(d == 1)[0], np.where(d == -1)[0]))


def silences(t, M, dur):
    return [(round(float(t[i0] - 0.2), 2), round(float(t[i1 - 1] + 0.2), 2)) for i0, i1 in runs(M < SIL_LUFS)
            if (i1 - i0) * 0.1 >= SIL_MIN - 1e-9 and t[i0] > EDGE and t[i1 - 1] < dur - EDGE]


def clips(x):
    return sum(1 for i0, i1 in runs((np.abs(x) >= CLIP_LVL).any(1)) if i1 - i0 >= CLIP_RUN)


def merge(iv, gap=0.0):
    out = []
    for a, b in sorted(iv):
        if out and a - out[-1][1] <= gap: out[-1][1] = max(out[-1][1], b)
        else: out.append([a, b])
    return out


def speech(TL):
    """khoảng lời tuyệt đối (phim chính) — segments[].speech là giây trong đoạn"""
    return merge([[s['t0'] + a, s['t0'] + b] for s in TL['segments'] for a, b in s.get('speech') or []])


def overlaps(TL):
    """A8: [lời đầu, lời cuối] của từng đoạn có lời; đoạn sau bắt đầu trước khi đoạn trước dứt → chồng"""
    seg = [(s['id'], s['t0'] + s['speech'][0][0], s['t0'] + s['speech'][-1][1]) for s in TL['segments'] if s.get('speech')]
    return [f'{a[0]}↔{b[0]} {mmss(b[1])} ({a[2] - b[1]:.2f} s)' for a, b in zip(seg, seg[1:]) if b[1] < a[2] - 1e-3]


def smr_stems(vo, bed, sp):
    """A4 từ stem: SMR = L_K(lời) − L_K(nền) trên cửa sổ 3 s bước 1 s nằm trọn trong một khoảng lời"""
    from scipy.signal import lfilter
    kv = lambda z: sum(lfilter(_KB2, _KA2, lfilter(_KB1, _KA1, z[:, c].astype(np.float64))) ** 2 for c in range(z.shape[1]))
    ev, eb = kv(vo), kv(bed); W = int(SMR_WIN * SR); dur = min(len(ev), len(eb)) / SR; cv = np.concatenate([[0.0], np.cumsum(ev)]); cb = np.concatenate([[0.0], np.cumsum(eb)])
    r = []
    for a, b in sp:
        t = a
        while t + SMR_WIN <= b + 1e-6 and t + SMR_WIN <= dur:
            i = int(t * SR); pv = (cv[i + W] - cv[i]) / W; pb = (cb[i + W] - cb[i]) / W
            r.append(10 * np.log10(max(pv, 1e-20) / max(pb, 1e-20))); t += SMR_HOP
    return r


def smr_stats(r):
    if not r: return None
    a = np.array(r); return dict(cua_so=len(a), trung_vi=round(float(np.median(a)), 2), p10=round(float(np.percentile(a, 10)), 2), min=round(float(a.min()), 2))


def sync_ms(master_x, vo_x, sp):
    """A13: trễ (ms) của luồng master so với stem lời, tương quan chéo đường bao năng lượng 1 ms trên ≤ 120 s đầu có lời; ±50 ms"""
    if not sp: return None
    a0 = sp[0][0]; a1 = min(len(master_x), len(vo_x)) / SR; a1 = min(a1, a0 + 120.0)
    if a1 - a0 < 5: return None
    i0, i1 = int(a0 * SR), int(a1 * SR); m = master_x[i0:i1].mean(1); v = vo_x[i0:i1].mean(1)
    # tương quan chéo trực tiếp trên tín hiệu (lệch nguyên mẫu), tìm trong ±50 ms
    L = int(0.05 * SR); best, lag = -1e30, 0
    v = v - v.mean(); m = m - m.mean(); n = len(v)
    for d in range(-L, L + 1, 4):
        a = m[max(0, d):n + min(0, d)]; b = v[max(0, -d):n - max(0, d)]; c = float(np.dot(a, b))
        if c > best: best, lag = c, d
    for d in range(lag - 4, lag + 5):
        a = m[max(0, d):n + min(0, d)]; b = v[max(0, -d):n - max(0, d)]; c = float(np.dot(a, b))
        if c > best: best, lag = c, d
    return round(1000 * lag / SR, 2)


# ---------------------------------------------------------------- A9 ASR
def _cache_dir(): return os.environ.get('K_ASR_CACHE', '/var/tmp/cine-out/k-asr-cache')


def _sha(p):
    h = hashlib.sha256()
    with open(P(p), 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def transcribe(vo_file, beam, model=None):
    """bản nghe tất định (nhiệt 0, không VAD, không hotword, không nối ngữ cảnh). Cache theo SHA tệp + cách nghe."""
    key = f'{_sha(vo_file)}-{ASR_MODEL}-b{beam}'; cp = os.path.join(_cache_dir(), key + '.txt')
    if os.path.exists(cp): return open(cp, encoding='utf-8').read(), model
    from checks.ll import q_av
    if model is None:
        from faster_whisper import WhisperModel
        model = WhisperModel(ASR_MODEL, device='cpu', compute_type='int8', cpu_threads=4)
    segs, _ = model.transcribe(q_av.pcm(vo_file), language='en', beam_size=beam, best_of=1, vad_filter=False, temperature=0.0,
                               condition_on_previous_text=False)
    txt = ' '.join(z.text.strip() for z in segs)
    os.makedirs(_cache_dir(), exist_ok=True); open(cp, 'w', encoding='utf-8').write(txt)
    return txt, model


def _sq(s): return re.sub(r'\s+', ' ', str(s or '')).strip()


def asr_exempt(spec_seg):
    """→ (lời đã bỏ câu miễn, [câu miễn hợp lệ], [lỗi khai])"""
    vo = _sq(spec_seg.get('vo')); ok, bad = [], []
    for x in spec_seg.get('asr_mo_ho') or []:
        cau = _sq((x or {}).get('cau') if isinstance(x, dict) else x); ly = _sq((x or {}).get('ly_do') if isinstance(x, dict) else '')
        if not cau or cau not in vo: bad.append(f'{spec_seg.get("id")}: câu miễn "{cau[:60]}" không có nguyên văn trong lời'); continue
        if len(ly) < LY_DO_MIN: bad.append(f'{spec_seg.get("id")}: câu miễn "{cau[:40]}…" thiếu lý do (≥ {LY_DO_MIN} ký tự)'); continue
        ok.append(dict(doan=spec_seg.get('id'), cau=cau, ly_do=ly)); vo = vo.replace(cau, ' ')
    return vo, ok, bad


def heard(txt):
    """bản nghe + bản tách gạch nối giữa hai chữ ("Minneapolis-fed" → thêm "Minneapolis fed"): ASR hay nối tên riêng với từ sau bằng gạch;
    chỉ THÊM dạng tách (không bỏ dạng gốc), số không đổi (gạch giữa hai chữ số giữ nguyên: "1.7-2 million" vẫn sai như BAI-HOC-LL #86)"""
    return txt + ' ' + re.sub(r'(?<=[A-Za-z])[-‐](?=[A-Za-z])', ' ', txt)


def asr_a9(E, TL, transcripts=None):
    """→ (lỗi, câu miễn, {cách nghe: số đoạn đạt}, số đoạn). transcripts: {đoạn: {5: txt, 1: txt}} (selftest) hoặc None (chạy ASR thật)"""
    from checks.ll import q_av
    spec = {s['id']: s for s in E.get('segments') or []}; bad, exempt, okc, n, model = [], [], {5: 0, 1: 0}, 0, None
    for s in TL['segments']:
        if not s.get('vo_file'): continue
        sp = spec.get(s['id']) or {}; n += 1
        vo, ex, eb = asr_exempt(dict(sp, id=s['id'])); exempt += ex; bad += eb
        for beam in (5, 1):
            if transcripts is not None: txt = (transcripts.get(s['id']) or {}).get(beam, '')
            else: txt, model = transcribe(s['vo_file'], beam, model)
            miss = q_av.asr_miss(vo, heard(txt))
            if miss: bad.append(f"{s['id']} ({'beam 5' if beam == 5 else 'tham lam'}): thiếu {', '.join(miss)}")
            else: okc[beam] += 1
    return bad, exempt, okc, n


# ---------------------------------------------------------------- A11
def music_a11(MX, fdur=None):
    from checks.ll import q_av
    fdur = fdur or (lambda f: q_av.fdur(f))
    L = MX.get('nhac') or []; bad, rows = [], []
    if not L: return ['mix.json không có nhac[] (nhật ký giao nhạc của chuỗi mới)'], rows
    for i, c in enumerate(L):
        nm = os.path.basename(c.get('file', '?'))
        if c.get('loop'): bad.append(f'{nm}: cue lặp vòng')
        try: d = fdur(c['file'])
        except (OSError, ValueError, KeyError, subprocess.SubprocessError): d = None
        if d is None: bad.append(f'{nm}: không đọc được độ dài bài')
        elif c.get('src_to', 0) > d + 0.05: bad.append(f"{nm}: đọc tới {c['src_to']:.1f} s, bài dài {d:.1f} s (lặp/kéo dài nhạc)")
        if i == 0: continue
        prev = L[i - 1]; bpm = float(prev.get('bpm') or 0)
        if bpm <= 0: bad.append(f'{nm}: cue trước không có bpm, không đo được ô nhịp'); continue
        bar = 240.0 / bpm; lech = float(c.get('lech_ranh_gioi_s', (c.get('diem_giao', 0) - c.get('ranh_gioi', 0))))
        rows.append(dict(cue=i, bai=nm, lech_s=round(lech, 3), o_nhip_s=round(bar, 3)))
        if abs(lech) > bar + 1e-3: bad.append(f'cue {i} {nm}: giao lệch ranh giới chương {lech:+.2f} s > 1 ô nhịp ({bar:.2f} s ở {bpm:g} bpm)')
    # cùng bài dùng lại > 60 s nguồn (bỏ cue `tiep_bai`: cùng vị trí trong bài, chỉ đổi cường độ)
    src = [(c['file'], c.get('ss_doc', 0.0), c.get('src_to', 0.0)) for c in L if not c.get('tiep_bai')]
    for i in range(len(src)):
        for j in range(i + 1, len(src)):
            if src[i][0] == src[j][0]:
                o = max(0.0, min(src[i][2], src[j][2]) - max(src[i][1], src[j][1]))
                if o > MUSIC_REPEAT_MAX: bad.append(f'{os.path.basename(src[i][0])} dùng lại {o:.0f} s nguồn (> {MUSIC_REPEAT_MAX:g} s)')
    return bad, rows


# ---------------------------------------------------------------- tổng
def chain(MX):
    return bool(MX) and str(MX.get('cong_cu') or '') == NEW_CHAIN


def near(v, thr): return v is not None and abs(v - thr) <= 0.05 * abs(thr)


LOI_MUC = ('A4', 'A8', 'A9', 'A10', 'A13')   # 1.16: mục phụ thuộc lời — KHÔNG ÁP khi tập/đoạn không có lời


def check(E, TL, master=None, MX=None, vo=None, bed=None, asr=True, transcripts=None, fdur=None, v116=False):
    """v116 (1.16, CHỈ tập từ T3 — khiếu nại A-V6-2, A-G1B-7): (1) đặc tả `animatic: true` → mọi mục CHỈ BÁO (bản xem nội bộ, nhạc tạm);
    (2) không có lời (timeline không có `speech`, không có stem --vo) → A4, A8, A9, A10, A13 KHÔNG ÁP; A1–A3, A5–A7, A11, A12 (đo trên master)
    vẫn áp như cũ (bản không lời §11.2 vẫn là bản phát hành)."""
    ap = chain(MX) and not (v116 and E.get('animatic')); rows = []; sat = []
    sp = speech(TL); khong_loi = bool(v116 and not sp and not (vo and os.path.exists(P(vo))))
    def row(ma, ten, ok, gia, nguong, chan=True):
        if khong_loi and ma in LOI_MUC: ok, gia, chan = None, 'KHÔNG ÁP (không có lời — 1.16)', False
        rows.append(dict(ma=ma, ten=ten, ok=ok, gia_tri=gia, nguong=nguong, chan=chan and ap))
    # A1–A3, A5–A7 trên master
    if master and os.path.exists(P(master)):
        I, LRA, TP = ebur128(master)
        row('A1', 'Loudness tích hợp (master sau AAC)', I_MIN <= I <= I_MAX, f'{I:.1f} LUFS', f'{I_MIN:.1f} … {I_MAX:.1f}')
        row('A2', 'Đỉnh thật sau AAC', TP <= TP_MAX, f'{TP:.1f} dBTP', f'≤ {TP_MAX:.1f}')
        row('A3', 'Biên độ loudness LRA', LRA_LO <= LRA <= LRA_HI, f'{LRA:.1f} LU', f'{LRA_LO:g}–{LRA_HI:g} (báo)', chan=False)
        if near(I, I_MIN) or near(I, I_MAX): sat.append(f'A1 I = {I:.1f} LUFS (ngưỡng {I_MIN:g} / {I_MAX:g})')
        if near(TP, TP_MAX): sat.append(f'A2 TP = {TP:.1f} dBTP (ngưỡng {TP_MAX:g})')
        x = decode(master); dur = len(x) / SR; t, M = momentary(x); ab = silences(t, M, dur)
        row('A5', 'Lặng bất thường ≥ 1 s (< −50 LUFS tức thời)', not ab, f'{len(ab)} đoạn' + (f' ({", ".join(f"{mmss(a)}–{mmss(b)}" for a, b in ab[:5])})' if ab else ''), '0')
        row('A6', 'Tỉ lệ lặng', True, f'{100 * float((M < SIL_LUFS).mean()):.2f} %', 'báo', chan=False)
        cl = clips(x); row('A7', 'Chạm trần (≥ 3 mẫu |x| ≥ 0,999)', cl == 0, str(cl), '0')
        if vo and os.path.exists(P(vo)):
            ms = sync_ms(x, decode(vo), sp); row('A13', 'Đồng bộ tiếng (trễ master so với stem lời)', ms is not None and abs(ms) <= SYNC_MAX_MS, f'{ms} ms', f'≤ {SYNC_MAX_MS:g} ms (báo)', chan=False)
        else: row('A13', 'Đồng bộ tiếng', None, 'không đo (không có stem lời --vo)', f'≤ {SYNC_MAX_MS:g} ms (báo)', chan=False)
        del x
    else:
        for ma, ten in (('A1', 'Loudness tích hợp'), ('A2', 'Đỉnh thật sau AAC'), ('A5', 'Lặng bất thường'), ('A7', 'Chạm trần')):
            row(ma, ten, False, 'không có master', '')
        row('A3', 'LRA', None, 'không có master', 'báo', chan=False); row('A6', 'Tỉ lệ lặng', None, 'không có master', 'báo', chan=False)
        row('A13', 'Đồng bộ tiếng', None, 'không có master', 'báo', chan=False)
    # A4
    st, src = None, None
    if vo and bed and os.path.exists(P(vo)) and os.path.exists(P(bed)):
        st = smr_stats(smr_stems(decode(vo), decode(bed), sp)); src = 'stem (K tính)'
    elif MX and isinstance(MX.get('smr'), dict) and MX['smr'].get('p10') is not None:
        st = MX['smr']; src = 'mix.json'
    if st:
        ok4 = st['p10'] >= SMR_P10 and st['min'] >= SMR_MIN
        row('A4', 'Lời trên nhạc (SMR)', ok4, f"p10 {st['p10']:.1f} · min {st['min']:.1f} dB · {st.get('cua_so')} cửa sổ · {src}", f'p10 ≥ {SMR_P10:g} · min ≥ {SMR_MIN:g}')
        if near(st['p10'], SMR_P10): sat.append(f"A4 p10 = {st['p10']:.1f} dB (ngưỡng {SMR_P10:g})")
        if near(st['min'], SMR_MIN): sat.append(f"A4 min = {st['min']:.1f} dB (ngưỡng {SMR_MIN:g})")
    else: row('A4', 'Lời trên nhạc (SMR)', False, 'không có stem (--vo/--bed) và mix.json không có smr', f'p10 ≥ {SMR_P10:g} · min ≥ {SMR_MIN:g}')
    # A8, A10
    ov = overlaps(TL); row('A8', 'Chồng lời', not ov, f'{len(ov)}' + (f' ({"; ".join(ov[:4])})' if ov else ''), '0')
    spec = {s['id']: s for s in E.get('segments') or []}; mm = []
    for s in TL['segments']:
        for a, b in (spec.get(s['id']) or {}).get('khoanh_khac_nhac') or []: mm.append((s['t0'] + float(a), s['t0'] + float(b)))
    G = merge(sp, GAP_MERGE); long_ = [(a[1], b[0]) for a, b in zip(G, G[1:]) if b[0] - a[1] > GAP_MAX and not any(x <= a[1] + 0.5 and y >= b[0] - 0.5 for x, y in mm)]
    gmax = max([b[0] - a[1] for a, b in zip(G, G[1:])] or [0.0])
    row('A10', 'Quãng không lời > 8 s không khai khoảnh khắc nhạc', not long_, f'dài nhất {gmax:.1f} s · {len(long_)} quãng' + (f' ({", ".join(mmss(a) for a, b in long_[:4])})' if long_ else ''), '> 8 s (báo)', chan=False)
    # A9
    if khong_loi: ex = []; row('A9', 'ASR hai cách nghe', None, '', '100 % đoạn')
    elif asr:
        b9, ex, okc, n = asr_a9(E, TL, transcripts)
        row('A9', 'ASR hai cách nghe (beam 5 + tham lam): số + tên riêng', not b9,
            f'beam 5 {okc[5]}/{n} · tham lam {okc[1]}/{n} đoạn · miễn {len(ex)} câu' + (f' · {"; ".join(b9[:4])}' if b9 else ''), '100 % đoạn, cả hai cách')
    else:
        ex = []; row('A9', 'ASR hai cách nghe', False, 'không chạy (--no-asr)', '100 % đoạn')
    # A11, A12
    if MX and ap:
        b11, r11 = music_a11(MX, fdur); mx = max([abs(r['lech_s']) for r in r11] or [0.0])
        row('A11', 'Giao nhạc ≤ 1 ô nhịp, không lặp', not b11, f'{len(MX.get("nhac") or [])} cue · lệch lớn nhất {mx:.2f} s' + (f' · {"; ".join(b11[:3])}' if b11 else ''), '≤ 1 ô nhịp · không lặp')
        nt = (((MX.get('loudness') or [{}])[-1].get('loudnorm') or {}).get('normalization_type'))
        row('A12', 'Loudnorm tuyến tính', nt == 'linear', str(nt), 'linear')
    else:
        row('A11', 'Giao nhạc', None, 'không đo (mix.json không phải chuỗi mới)', '≤ 1 ô nhịp · không lặp')
        row('A12', 'Loudnorm tuyến tính', None, 'không đo (mix.json không phải chuỗi mới)', 'linear')
    loi = [f"{r['ma']} {r['ten']}: {r['gia_tri']}" for r in rows if r['chan'] and r['ok'] is not True]
    bao = [f"{r['ma']} {r['ten']}: {r['gia_tri']}" for r in rows if not r['chan'] and r['ok'] is False]
    kq = ('ĐẠT' if not loi else 'TRƯỢT') if ap else 'CHỈ BÁO'
    return dict(ok=not loi, ket_qua=kq, ap_dung=ap, khong_loi=khong_loi, rows=rows, loi=loi, bao=bao, sat_nguong=sat, mien_asr=ex, note='; '.join(loi[:6]),
                val=f"{kq} · " + ' · '.join(f"{r['ma']} {r['gia_tri'].split(' · ')[0]}" for r in rows if r['ma'] in ('A1', 'A2', 'A4', 'A5', 'A7', 'A8')))


def table(r):
    md = ['| Mục | Kiểm | Loại | Kết quả | Giá trị | Ngưỡng |', '|---|---|---|---|---|---|']
    for x in sorted(r['rows'], key=lambda z: int(z['ma'][1:])):
        kq = '—' if x['ok'] is None else 'ĐẠT' if x['ok'] else 'TRƯỢT' if x['chan'] else 'BÁO'
        md.append(f"| {x['ma']} | {x['ten']} | {'chặn' if x['ma'] not in ('A3', 'A6', 'A10', 'A13') else 'báo'} | {kq} | {x['gia_tri'].replace('|', '/')} | {x['nguong']} |")
    return '\n'.join(md)


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    g = lambda k: a[a.index('--' + k) + 1] if '--' + k in a else None
    E = base.load(a[0]); TL = json.load(open(g('tl') or os.path.join(E['out'], 'timeline.json')))
    mp = g('mix') or os.path.join(E['out'], 'mix.json'); MX = json.load(open(mp)) if os.path.exists(mp) else None
    r = check(E, TL, master=g('master'), MX=MX, vo=g('vo'), bed=g('bed'), asr='--no-asr' not in a)
    print(f"Âm thanh A1–A13 {r['ket_qua']} (áp dụng: {'MIX=audio' if r['ap_dung'] else 'tập cũ — chỉ báo'})\n" + table(r)
          + (f"\nsát ngưỡng (±5 %): {'; '.join(r['sat_nguong'])}" if r['sat_nguong'] else '')
          + (''.join(f"\nmiễn ASR (chấm tai): {x['doan']} \"{x['cau'][:70]}\" — {x['ly_do']}" for x in r['mien_asr'])))
    if g('json'): json.dump(r, open(g('json'), 'w'), ensure_ascii=False, indent=1)
    sys.exit(0 if r['ok'] else 1)
