#!/opt/cine/bin/python
"""ÂM THANH · dựng tiếng cả tập bằng chuỗi mới (phiên Âm thanh, Mốc C, 15/10/2026) — thay cho scripts/ll/mix.py khi bật MIX=audio.

  compose.py <timeline.json> <ra.wav> [--episode episode.yaml] [--stems thư_mục] [--short ID] [master.py: --smr 15 --duck -8 --I -14 --tp -1]

  lời   : vo_file của từng đoạn đặt đúng t0 + vo_offset (nguyên bản ElevenLabs; xử lý ở master.py)
  nhạc  : scripts/audio/music.py — nhạc theo chương, giao bài đúng ô nhịp, đổi cường độ (TL['music'], tương thích khoá cũ)
  SFX   : cue sẵn có trong timeline (ll.py: lật/trượt giấy, đèn khí, cue khai ở shot) như mix.py (−6 dB, fade_ms)
          + scripts/audio/sfx.py — biến cố hình tự suy (xu, bảng màu, máy lặn) + `sfx_events` theo mốc lời (cần --episode)
  master: scripts/audio/master.py — nén nhẹ lời, ducking thích ứng (SMR ≥ 15 dB), fade, loudness 2 lượt, đỉnh thật sau AAC
Ghi <ra>.json: báo cáo master + nhật ký nhạc + nhật ký SFX (để phiên K biến thành luật, docs/AUDIO-THUOC-DO.md).
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib, master, music, sfx

SR = lib.SR


def arg(k, d=None, f=str):
    return f(sys.argv[sys.argv.index('--' + k) + 1]) if '--' + k in sys.argv else d


def timeline_cues(segs, N):
    out = np.zeros((N, 2)); log = []
    for d in segs:
        for c in d.get('sfx', []):
            s = lib.dec(c['file'], 2, ss=c.get('src_ss', 0), dur=c.get('dur')); n = len(s)
            if not n: continue
            fl = max(1, min(n // 2, int(c.get('fade_ms', 8) / 1000 * SR))); w = np.ones(n); w[:fl] = np.linspace(0, 1, fl); w[-fl:] = np.linspace(1, 0, fl)
            k = int(round(c['at_abs'] * SR)); m = min(n, N - k)
            if m > 0 and k >= 0: out[k:k + m] += (s * w[:, None] * 10 ** ((c.get('gain_db', 0) - 6) / 20))[:m]
            log.append(dict(t=c['at_abs'], tep=c['file'], dur=c.get('dur'), nguon='timeline'))
    return out, log


def main():
    if len(sys.argv) < 3: sys.exit(__doc__)
    import yaml
    TL = json.load(open(sys.argv[1])); out = sys.argv[2]; short = arg('short'); E = yaml.safe_load(open(arg('episode'))) if arg('episode') else None
    segs = [s for s in TL['shorts'] if s['id'] == short] if short else TL['segments']; dur = segs[0]['t1'] if short else TL['tong_s']; N = int(round(dur * SR))
    vo = np.zeros((N, 1), np.float32)
    for d in segs:
        if d.get('vo_file'):
            x = lib.dec(d['vo_file'], 1); k = int(round((d['t0'] + d['vo_offset']) * SR)); m = min(len(x), N - k); vo[k:k + m] += x[:m]
    sp = lib.speech_from_timeline(TL, short)
    if short:   # Short: cue đầu (nhạc hiệu), không giao bài
        M = (TL.get('music') or [])[:1]; mus, mlog = music.build(dict(TL, segments=[dict(id=M[0].get('from') if M else None, t0=0.0)], tong_s=dur), M, dur) if M else (np.zeros((N, 2)), [])
        fx, slog = timeline_cues(segs, N)
    else:
        mus, mlog = music.build(TL); fx, slog = timeline_cues(segs, N)
        ev, elog = sfx.build(TL, E); fx = fx + ev; slog += elog
    if arg('stems'):
        os.makedirs(arg('stems'), exist_ok=True)
        for n, x in (('raw-vo', vo), ('raw-music', mus), ('raw-sfx', fx)): lib.write(os.path.join(arg('stems'), n + '.flac'), x, 'flac', extra=('-sample_fmt', 's32'))
        json.dump(dict(tong_s=dur, speech=sp), open(os.path.join(arg('stems'), 'speech.json'), 'w'))
    S = dict(vo=vo, music=mus.astype(np.float32), sfx=fx.astype(np.float32)); del vo, mus, fx
    R = master.finish(S, speech=sp, out_wav=out, smr=arg('smr', None, float), duck=arg('duck', None, float), I=arg('I', None, float), tp=arg('tp', None, float),
                      fade_in=arg('fade-in', 0.0 if not short else None, float), fade_out=arg('fade-out', 1.2 if short else None, float),
                      aac=arg('aac', '192k' if short else None))
    R['nhac'] = mlog; R['sfx'] = slog
    json.dump(R, open(out.rsplit('.', 1)[0] + '.json', 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(dict(dau_ra=R['dau_ra'], smr=R['smr'], dat=R['dat'], so_cue_nhac=len(mlog), so_sfx=len(slog)), ensure_ascii=False))


if __name__ == '__main__':
    main()
