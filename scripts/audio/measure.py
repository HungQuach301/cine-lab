#!/opt/cine/bin/python
"""ÂM THANH · đo một bản âm thanh (phiên Âm thanh, Mốc C, 15/10/2026). Số đo ra JSON để phiên K biến thành luật (docs/AUDIO-THUOC-DO.md).

  measure.py <âm thanh|video> [--speech speech.json|timeline.json] [--vo vo.flac --bed bed.flac] [--json ra.json]

Đo (mọi số là đo thật trên tệp):
  I (LUFS tích hợp), LRA (LU), TP (dBTP, ffmpeg ebur128 nâng mẫu ×4) — chuẩn EBU R128 / BS.1770-4.
  lặng: tỉ lệ thời gian loudness tức thời (400 ms) < −50 LUFS; khoảng lặng BẤT THƯỜNG = đoạn ≥ 1,0 s dưới −50 LUFS ở giữa phim (bỏ 2 s đầu/cuối).
  quãng không lời dài nhất (giây, khi biết khoảng lời).
  mẫu chạm trần: số chuỗi ≥ 3 mẫu liền |x| ≥ 0,999 (dấu hiệu cắt) trên tín hiệu đã giải mã.
  chồng lời: số cặp khoảng lời chồng nhau (hai đoạn lời phát cùng lúc) — từ timeline.
  chênh lời–nhạc (SMR, dB): khi có stem lời (--vo) và phần còn lại (--bed): trên cửa sổ 3 s bước 1 s nằm trọn trong khoảng lời,
        SMR = L_K(lời) − L_K(nền) (lọc K). Báo trung vị, p10 (10 % cửa sổ xấu nhất), % cửa sổ dưới 15 dB.
        Master không có stem: dựng lại stem bằng scripts/ll/mix.py --stems (prep offline) — đã kiểm trên T1: bản dựng lại khớp master
        tới phần dư −40 dB. Phép "chiếu" lời gốc lên master KHÔNG dùng được (lời đã qua nén phi tuyến; thử 15/10 ra SMR ≈ 3 dB, sai).
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib

SIL_LUFS, SIL_MIN, EDGE = -50.0, 1.0, 2.0
SMR_TARGET = 15.0


def arg(k, d=None):
    return sys.argv[sys.argv.index('--' + k) + 1] if '--' + k in sys.argv else d


def runs(mask, dt):
    """các đoạn liền True → [(i0, i1)] theo chỉ số"""
    m = np.concatenate([[False], mask, [False]]).astype(int); d = np.diff(m)
    return list(zip(np.where(d == 1)[0], np.where(d == -1)[0]))


def load_speech(p):
    if not p: return None, None
    J = json.load(open(p))
    if 'segments' in J:   # timeline
        raw = sorted([d['t0'] + a, d['t0'] + b] for d in J['segments'] for a, b in d.get('speech', []))
        segs = [(d['t0'] + d['vo_offset'] + (d['speech'][0][0] - d['vo_offset'] if d.get('speech') else 0), d['t0'] + d['speech'][-1][1]) for d in J['segments'] if d.get('speech')]
        ov = sum(1 for a, b in zip(segs, segs[1:]) if b[0] < a[1] - 1e-3)
        return lib.merge(raw), ov
    return J['speech'], None


def windows_in(speech, dur, win=3.0, hop=1.0):
    """tâm các cửa sổ 3 s nằm trọn trong một khoảng lời"""
    out = []
    for a, b in speech:
        t = a
        while t + win <= b + 1e-6 and t + win <= dur: out.append(t); t += hop
    return out


def smr_stems(vo, bed, speech, sr=lib.SR):
    kv, kb = lib.kw(vo), lib.kw(bed); W = int(3.0 * sr); r = []
    for t in windows_in(speech, len(vo) / sr):
        i = int(t * sr); pv = (kv[i:i + W].astype(np.float64) ** 2).sum(1).mean(); pb = (kb[i:i + W].astype(np.float64) ** 2).sum(1).mean()
        r.append(10 * np.log10(max(pv, 1e-20) / max(pb, 1e-20)))
    return r


def stats(r, target=SMR_TARGET):
    if not r: return None
    a = np.array(r); return dict(cua_so=len(a), trung_vi=round(float(np.median(a)), 2), p10=round(float(np.percentile(a, 10)), 2),
                                 min=round(float(a.min()), 2), duoi_nguong_pct=round(100 * float((a < target).mean()), 1), nguong=target)


def measure(path, speech_p=None, vo_p=None, bed_p=None):
    R = dict(tep=os.path.relpath(lib.P(path), lib.REPO) if lib.P(path).startswith(lib.REPO) else path)
    R.update(lib.ebur128(path))
    x = lib.dec(path, 2, dtype=np.float32); dur = len(x) / lib.SR; R['tong_s'] = round(dur, 2)
    t, M = lib.momentary(x); R['lang_pct'] = round(100 * float((M < SIL_LUFS).mean()), 2)
    ab = [(round(float(t[i0] - 0.2), 2), round(float(t[i1 - 1] + 0.2), 2)) for i0, i1 in runs(M < SIL_LUFS, 0.1)
          if (i1 - i0) * 0.1 >= SIL_MIN and t[i0] > EDGE and t[i1 - 1] < dur - EDGE]
    R['lang_bat_thuong'] = dict(so=len(ab), ds=ab[:30], dinh_nghia=f'≥ {SIL_MIN} s dưới {SIL_LUFS} LUFS tức thời, bỏ {EDGE} s đầu/cuối')
    clip = sum(1 for i0, i1 in runs((np.abs(x) >= 0.999).any(1), 1) if i1 - i0 >= 3); R['cham_tran'] = clip
    sp, ov = load_speech(speech_p)
    if sp:
        gaps = [b[0] - a[1] for a, b in zip(sp, sp[1:])]
        R['loi'] = dict(khoang=len(sp), ty_le_co_loi_pct=round(100 * sum(b - a for a, b in sp) / dur, 1), quang_khong_loi_dai_nhat_s=round(max(gaps), 2) if gaps else 0,
                        quang_khong_loi_gt8s=sum(1 for g in gaps if g > 8), chong_loi=ov)
        if vo_p and bed_p:
            R['smr'] = dict(cach='stem', **stats(smr_stems(lib.dec(vo_p, 2, dtype=np.float32), lib.dec(bed_p, 2, dtype=np.float32), sp)))
    R['muc_tieu'] = dict(I=[-15.0, -14.0], TP_max=-1.0, SMR_min=SMR_TARGET)
    R['dat'] = dict(I=-15.0 - 0.5 <= R['I'] <= -14.0 + 0.5, TP=R['TP'] <= -1.0, SMR=(R['smr']['p10'] >= SMR_TARGET) if 'smr' in R else None)
    return R


if __name__ == '__main__':
    if len(sys.argv) < 2: sys.exit(__doc__)
    R = measure(sys.argv[1], arg('speech'), arg('vo'), arg('bed'))
    s = json.dumps(R, ensure_ascii=False, indent=1)
    if arg('json'): open(arg('json'), 'w').write(s)
    print(s)
