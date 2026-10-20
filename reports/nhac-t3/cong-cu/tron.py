"""NHẠC-T3 · trộn thử theo cue sheet (chỉ đề xuất; KHÔNG phải bản phát hành).

  tron.py <cue.json> <t0> <t1> <ra.wav> [--khong-loi] [--duck-co-dinh] [--json ra.json]

Nền nhạc (theo quy ước scripts/audio/music.py, dựng lại tối giản vì bài mới chưa có dòng RIGHTS nên music.py không nhận):
  - mỗi NHÓM cue chuẩn về −24 LUFS đo trên toàn bộ đoạn bài nhóm dùng (các cue cắt ghép cùng nhóm giữ động học nội tại);
    muc: low = −5 dB + lọc thấp 2,5 kHz · mid = 0 · high = +2,5 dB (như music.py).
  - tang: [[t0, t1, dB]] nâng nhạc trong tấm im lặng (dốc smoothstep 1 s bên trong khoảng, không chạm lời).
  - giao bài: crossfade công suất bằng nhau (cos/sin), tâm tại phim_vao / phim_ra, dài xf_vao / xf_ra giây.
Lời: stem G1 đặt lên trục phim phương án B (dat_loi.py, từ 2 MP3 xem KL42).
Hoàn thiện: GỌI NGUYÊN scripts/audio/master.py finish() (lời −17 LUFS → duck thích ứng cơ bản −12 dB → 2 lượt loudness −14 LUFS,
  trần đỉnh thật −1 dBTP kiểm sau AAC). --duck-co-dinh: sàn duck = −12 dB (đo "nhạc có tự hợp lời không" khi không hạ thêm).
SMR (A4, docs/AUDIO-THUOC-DO.md): đo trên stem lời đã xử lý vs nền đã duck, cửa sổ 3 s bước 1 s nằm trọn trong khoảng lời (gộp nghỉ < 0,55 s);
  ngoài số tổng còn ghi từng cửa sổ (giây phim) để chỉ ra đoạn nào sát ngưỡng."""
import json, os, sys, subprocess
import numpy as np
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, os.path.join(ROOT, 'scripts/audio')); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib, measure, master, dat_loi
SR = lib.SR
NGOAI = os.environ.get('NHAC_T3_NGOAI', '/tmp/claude-0/nt3/dl')
KL42 = os.environ.get('KL42', '/tmp/claude-0/kl42/reports/kl42')
MUC = dict(low=(-5.0, 2500), mid=(0.0, None), high=(2.5, None))


def tep(p): return os.path.join(NGOAI, p.split('/', 1)[1]) if p.startswith('NGOAI-GIT/') else os.path.join(ROOT, p)


def doan_bai(c, t0, t1):
    """khoảng phim cue phủ (gồm nửa crossfade) ∩ [t0,t1) → (phim_a, phim_b, bai_a)"""
    a = max(c['phim_vao'] - c['xf_vao'] / 2, t0); b = min(c['phim_ra'] + c['xf_ra'] / 2, t1)
    return a, b, c['vao_bai'] + (a - c['phim_vao'])


def ramp(t, tc, x, up):
    if x <= 0: return np.ones_like(t) if up else np.ones_like(t)
    u = np.clip((t - (tc - x / 2)) / x, 0, 1)
    return np.sin(u * np.pi / 2) if up else np.cos(u * np.pi / 2)


def nen(P, t0, t1):
    N = int(round((t1 - t0) * SR)); bed = np.zeros((N, 2), np.float32); cache = {}; log = []
    # hệ số nhóm: đo trên toàn bộ đoạn bài nhóm dùng (cả phim), không phụ thuộc cửa sổ trích → trích đoạn = cùng mức với bản cả phim
    gain = {}
    for g in sorted(set(c['nhom'] for c in P['cue'])):
        segs = []
        for c in P['cue']:
            if c['nhom'] != g: continue
            a, b, ba = doan_bai(c, 0, P['phim_s'])
            segs.append(lib.dec(tep(c['tep']), 2, ss=ba, dur=b - a, dtype=np.float32))
        L = lib.integrated(np.concatenate(segs)); gain[g] = -24.0 - L
    for c in P['cue']:
        a, b, ba = doan_bai(c, t0, t1)
        if b <= a: continue
        x = lib.dec(tep(c['tep']), 2, ss=ba, dur=b - a, dtype=np.float32)
        off, lp = MUC[c['muc']] if isinstance(c['muc'], str) else (float(c['muc']), None)
        if lp:
            r = subprocess.run(['ffmpeg', '-v', 'error', '-nostdin', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', '-af', f'lowpass=f={lp}', '-f', 'f32le', '-'],
                               input=x.tobytes(), capture_output=True, check=True); x = np.frombuffer(r.stdout, np.float32).reshape(-1, 2).copy()
        t = a + np.arange(len(x)) / SR
        env = ramp(t, c['phim_vao'], c['xf_vao'], True) * ramp(t, c['phim_ra'], c['xf_ra'], False)
        for ta, tb, db in c.get('tang', []):   # tự động hoá trong cue (tấm im lặng): dốc 1 s nằm TRONG khoảng, không chạm lời
            u = np.clip(np.minimum((t - ta) / 1.0, (tb - t) / 1.0), 0, 1); u = u * u * (3 - 2 * u); env = env * 10 ** (db * u / 20)
        x = x * (10 ** ((gain[c['nhom']] + off) / 20) * env)[:, None].astype(np.float32)
        i = int(round((a - t0) * SR)); m = min(len(x), N - i); bed[i:i + m] += x[:m]
        log.append(dict(id=c['id'], phim=[round(a, 3), round(b, 3)], bai=[round(ba, 3), round(ba + b - a, 3)], gain_db=round(gain[c['nhom']] + off, 2)))
    return bed, log


CAP = {}
_smr = measure.smr_stems
def _cap(vo, bed, speech, sr=SR):
    CAP['vo'], CAP['bed'], CAP['sp'] = vo, bed.copy(), speech; return _smr(vo, bed, speech, sr)
measure.smr_stems = _cap


def cua_so(vo, bed, speech, t0):
    kv, kb = lib.kw(vo), lib.kw(bed); W = int(3 * SR); out = []
    for t in measure.windows_in(speech, len(vo) / SR):
        i = int(t * SR); pv = (kv[i:i + W].astype(np.float64) ** 2).sum(1).mean(); pb = (kb[i:i + W].astype(np.float64) ** 2).sum(1).mean()
        out.append((round(t0 + t, 1), round(10 * np.log10(max(pv, 1e-20) / max(pb, 1e-20)), 2)))
    return out


def chay(cue, t0, t1, out, khong_loi=False, duck_co_dinh=False):
    P = json.load(open(cue)); bed, log = nen(P, t0, t1)
    if khong_loi:
        vo = np.zeros(len(bed), np.float32); sp = []
    else:
        vo, sp = dat_loi.dung(os.path.join(KL42, 'nhip-that.json'), os.path.join(KL42, 'nghe/T3-loi-G1-v42-xem-1-ch00-02.mp3'),
                              os.path.join(KL42, 'nghe/T3-loi-G1-v42-xem-2-ch03-05.mp3'), t0, t1)
        vo = vo[:len(bed)] if len(vo) >= len(bed) else np.pad(vo, (0, len(bed) - len(vo)))
    spm = lib.merge([list(x) for x in sp], 0.55) if sp else []
    kw = dict(duck_floor=-12.0) if duck_co_dinh else {}
    fi = 0.3 if t0 == 0 else 1.0
    if khong_loi:   # chỉ nhạc: không qua chuỗi lời; chuẩn −14 LUFS, trần −1,5 dBFS trên tín hiệu ×4 (như xuat.py KL42)
        return chi_nhac(bed, out, log, P, t0, t1)
    R = master.finish(dict(vo=vo[:, None], music=bed, sfx=None), speech=[tuple(x) for x in spm], out_wav=out, fade_in=fi, fade_out=1.5, **kw)
    W = cua_so(CAP['vo'], CAP['bed'], CAP['sp'], t0)
    R['cua_so_smr'] = W; R['nen'] = log; R['phuong_an'] = P['phuong_an']; R['khoang_phim'] = [t0, t1]
    R['duck_co_dinh'] = duck_co_dinh
    return R


def chi_nhac(bed, out, log, P, t0, t1):
    L = lib.integrated(bed); g = -14.0 - L; tmp = out + '.tmp.wav'; lib.write(tmp, bed * np.float32(10 ** (g / 20)), 'pcm_f32le')
    subprocess.run(['ffmpeg', '-v', 'error', '-nostdin', '-y', '-i', tmp, '-af', 'aresample=192000,alimiter=limit=0.84:attack=1:release=60:level=disabled:asc=1,aresample=48000',
                    '-c:a', 'pcm_s24le', out], check=True); os.remove(tmp)
    E = lib.ebur128(out)
    return dict(phuong_an=P['phuong_an'], khoang_phim=[t0, t1], chi_nhac=True, gain_db=round(g, 2), dau_ra=dict(I=E['I'], TP=E['TP']), nen=log)


if __name__ == '__main__':
    a = sys.argv; R = chay(a[1], float(a[2]), float(a[3]), a[4], '--khong-loi' in a, '--duck-co-dinh' in a)
    js = a[a.index('--json') + 1] if '--json' in a else a[4].rsplit('.', 1)[0] + '.json'
    json.dump(R, open(js, 'w'), ensure_ascii=False, indent=0)
    print(json.dumps({k: R.get(k) for k in ('phuong_an', 'khoang_phim', 'dau_ra', 'smr', 'dat')}, ensure_ascii=False))
    if 'duck' in R: print(json.dumps({k: v for k, v in R['duck'].items() if k != 'ds'}, ensure_ascii=False))
