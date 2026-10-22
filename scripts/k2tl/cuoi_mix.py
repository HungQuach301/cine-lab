#!/opt/cine/bin/python
"""BAN-CUOI-T3 (việc 6) · TRỘN TIẾNG BẢN CUỐI 762 s + STEM (giọng / nhạc / SFX).
  · Giọng = master LFS channel-k2/k2c-t3-01/am-thanh/master/T3-loi-G1-v42-14LUFS.wav (SHA ba50fba7…), KHÔNG đổi chữ, không tạo giọng mới; đặt theo
    channel-k2/k2c-t3-01/cuoi/anim-loi.json — 3 câu đầu cắt ĐÚNG mốc câu (T3-loi-moc.json) và đảo thứ tự (việc 1c), còn lại như animatic (nhịp B).
  · Nhạc = phương án B (cue-B.json) + KA2026 = A8 (§14.6) — đúng cue_sheet() của scripts/k2tl/anim_mix.py; thời lượng phim 762 s (PP1 9 s) → cue cuối kéo thêm 1 s.
  · SFX = gói bản cuối (scripts/k2tl/cuoi_sfx.py → su-kien-cuoi.json), mức "tối giản dưới lời", dựng bằng sfx_stem() của reports/sfx-t3/cong-cu/tron_thu.py (import, không sửa).
  · Hoàn thiện = BẢN SAO TỪNG BƯỚC của scripts/audio/master.py finish() (lời −17 LUFS → duck thích ứng §4, SFX hạ ½ mức duck của nhạc → loudness 2 lượt −14 LUFS,
    trần −1 dBTP kiểm sau AAC) — chép để giữ được 3 stem đã xử lý; mọi hàm con gọi từ master.py (vo_process, ducking, smooth_env, loudness_2pass, aac_tp).
  · Stem: thành phần đã duck/fade × hệ số tuyến tính bình phương tối thiểu (bản master ↔ tổng trước loudness); tổng 3 stem ≈ master trừ phần bộ giới hạn đỉnh (ghi sai khác).
  · Ghi mix.json có nhac[] (log cue nhạc, F3), sfx[], giong{}.
  cuoi_mix.py <anim-loi.json> <su-kien-cuoi.json> <thư mục ra> [--tong 762.0]"""
import copy, json, os, sys, tempfile
import numpy as np
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.environ.setdefault('NHAC_T3_NGOAI', os.path.join(REPO, 'assets/k2/music'))
for p in ('reports/nhac-t3/cong-cu', 'scripts/audio', 'reports/sfx-t3/cong-cu', 'scripts/k2tl'): sys.path.insert(0, os.path.join(REPO, p))
import tron, lib, master, measure, tron_thu, anim_mix
SR = lib.SR; MASTER = anim_mix.MASTER

def giong(L, N, pad=0.12):
    a = lib.dec(MASTER, 1, dtype=np.float32)[:, 0]; vo = np.zeros(N, np.float32); sp = []; r = int(0.01 * SR)
    for d in L['dong']:
        p = 0.05 if d.get('cau') else pad   # câu cắt lẻ (1c): đệm ngắn, không lấn câu kề trong stem gốc
        s0, s1 = max(0.0, d['bd_stem'] - p), d['kt_stem'] + p; x = a[int(s0 * SR):int(s1 * SR)].copy(); x[:r] *= np.linspace(0, 1, r); x[-r:] *= np.linspace(1, 0, r)
        i = int(round((d['bd_phim'] - (d['bd_stem'] - s0)) * SR)); m = min(len(x), N - i); vo[i:i + m] += x[:m]
        sp.append((round(d['bd_phim'], 3), round(d['bd_phim'] + d['kt_stem'] - d['bd_stem'], 3)))
    return vo, sorted(sp)

def finish_stem(vo, music, sfx, speech, out_wav, C):
    N = len(music); dur = N / SR
    vp = master.vo_process(vo[:, None].astype(np.float32), C['vo_chain'])[:, 0].astype(np.float32); vp = vp[:N] if len(vp) >= N else np.pad(vp, (0, N - len(vp)))
    mask = np.zeros(N, bool)
    for a, b in speech: mask[int(a * SR):int(b * SR)] = True
    Lvo = lib.integrated(np.stack([vp[mask], vp[mask]], 1)); vp *= np.float32(10 ** ((C['vo_lufs'] - Lvo) / 20))
    iv, D = master.ducking(vp[:, None], music + sfx, speech, C); env = master.smooth_env(N, iv, [d['duck_db'] for d in D], C['attack'], C['release'])
    t = np.arange(N) / SR; last = max((b for a, b in speech), default=0.0); fo0 = max(last + 0.3, dur - C['fade_out'])
    fade_out = np.clip((dur - t) / max(dur - fo0, 0.05), 0, 1).astype(np.float32); fin = (np.clip(t / C['fade_in'], 0, 1) * np.clip((dur - t) / C['fade_out'], 0, 1)).astype(np.float32)
    gm = (10 ** (env / 20)).astype(np.float32) * fin; gs = (10 ** (env * C['sfx_duck_ratio'] / 20)).astype(np.float32) * fin
    Mu = music * (gm * fade_out)[:, None]; Sx = sfx * (gs * fade_out)[:, None]; Vo = np.stack([vp * fade_out, vp * fade_out], 1)
    smr = measure.stats(measure.smr_stems(Vo, Mu + Sx, speech), C['smr']); mix = Vo + Mu + Sx
    log = []; ceiling = C['tp'] - C['tp_margin']
    with tempfile.TemporaryDirectory(dir=os.path.dirname(os.path.abspath(out_wav))) as work:
        extra = 0.0
        for k in range(4):
            o, L = master.loudness_2pass(mix, C, work, ceiling, extra); A = master.aac_tp(o, C['aac'], work); E = lib.ebur128(o)
            L['aac'] = dict(I=A['I'], TP=A['TP']); L['ebur128'] = dict(I=E['I'], TP=E['TP']); log.append(L)
            tp_ok = A['TP'] <= C['tp']; dI = C['I'] - E['I']
            if tp_ok and abs(dI) <= 0.1: break
            if not tp_ok: ceiling -= (A['TP'] - C['tp']) + 0.1
            if abs(dI) > 0.1: extra += dI
        os.replace(o, out_wav)
    out = lib.dec(out_wav, 2, dtype=np.float32)[:N]
    a, b = out[SR * 30:SR * 60, 0], mix[SR * 30:SR * 60, 0]; lag, best = 0, -2.0   # trễ của chuỗi loudness (bộ giới hạn nhìn trước) — dò ±400 mẫu
    for k in range(-400, 401):
        x, y = (a[k:], b[:len(b) - k]) if k >= 0 else (a[:k], b[-k:]); r = float(np.dot(x, y) / np.sqrt(np.dot(x, x) * np.dot(y, y) + 1e-20))
        if r > best: lag, best = k, r
    sh = lambda x: np.concatenate([np.zeros((lag, x.shape[1]), np.float32), x[:len(x) - lag]]) if lag > 0 else (np.concatenate([x[-lag:], np.zeros((-lag, x.shape[1]), np.float32)]) if lag < 0 else x)
    Vo, Mu, Sx, mix = sh(Vo), sh(Mu), sh(Sx), sh(mix)
    g = float(np.sum(out * mix[:len(out)]) / max(1e-12, np.sum(mix[:len(out)] ** 2)))   # hệ số tuyến tính master/tổng (sau khi khử trễ)
    resid = out - g * mix[:len(out)]; rel = float(20 * np.log10(max(1e-9, np.sqrt(np.mean(resid ** 2))) / max(1e-9, np.sqrt(np.mean(out ** 2)))))
    M = measure.measure(out_wav, None)
    R = dict(cong_cu='scripts/k2tl/cuoi_mix.py (bước như scripts/audio/master.py finish)', tham_so={k: C[k] for k in C if k != 'vo_chain'}, tong_s=round(dur, 3), loi_LUFS_truoc_chuan=round(float(Lvo), 2),
             duck=dict(so_khoang=len(D), trung_vi_db=float(np.median([d['duck_db'] for d in D])) if D else 0, sau_nhat_db=min((d['duck_db'] for d in D), default=0)), loudness=log,
             dau_ra=dict(I=M['I'], LRA=M['LRA'], TP=M['TP'], TP_sau_aac=log[-1]['aac']['TP'], lang_pct=M['lang_pct'], lang_bat_thuong=M['lang_bat_thuong']['so'], cham_tran=M['cham_tran']), smr=smr,
             stem=dict(he_so=round(g, 5), tre_mau=lag, tuong_quan=round(best, 5), sai_khac_tong_stem_vs_master_dB=round(rel, 1)))
    R['dat'] = dict(I=abs(M['I'] - C['I']) <= 0.2, TP=M['TP'] <= C['tp'], TP_sau_aac=log[-1]['aac']['TP'] <= C['tp'], SMR_p10=bool(smr and smr['p10'] >= C['smr']))
    return R, dict(giong=Vo * g, nhac=Mu * g, sfx=Sx * g)

if __name__ == '__main__':
    L = json.load(open(sys.argv[1])); SK = json.load(open(sys.argv[2])); OD = sys.argv[3]; os.makedirs(OD, exist_ok=True)
    T = float(sys.argv[sys.argv.index('--tong') + 1]) if '--tong' in sys.argv else 762.0
    P = anim_mix.cue_sheet(); P['phim_s'] = T
    for c in P['cue']:
        if abs(c['phim_ra'] - 761.0) < 0.01: c['phim_ra'] = T
    json.dump(P, open(os.path.join(OD, 'mix-cue.json'), 'w'), ensure_ascii=False, indent=1)
    bed, nlog = tron.nen(P, 0.0, T); N = len(bed)
    vo, sp = giong(L, N); fx, flog = tron_thu.sfx_stem(SK['su_kien'], 0.0, T); fx = fx[:N] if len(fx) >= N else np.pad(fx, ((0, N - len(fx)), (0, 0)))
    spm = [tuple(x) for x in lib.merge([list(x) for x in sp], 0.55)]
    C = dict(master.DEF, fade_in=0.3, fade_out=2.0)
    R, ST = finish_stem(vo, bed, fx, spm, os.path.join(OD, 'mix.wav'), C)
    for k, x in ST.items(): lib.write(os.path.join(OD, f'stem-{k}.wav'), x) if hasattr(lib, 'write') else __import__('soundfile').write(os.path.join(OD, f'stem-{k}.wav'), x, SR, subtype='PCM_24')
    R['nhac'] = nlog; R['sfx'] = flog; R['giong'] = dict(tep=MASTER, sha256='ba50fba75aa956731226f7269adbffb6728853d6d2a7fc95b4eefba8e13b586d', dong=len(L['dong']), dao_3_cau_dau=[d for d in L['dong'] if d.get('cau')])
    R['cue'] = 'cue-B + A8 ở KA2026 (§14.6)'; R['khoang_loi'] = spm
    json.dump(R, open(os.path.join(OD, 'mix.json'), 'w'), ensure_ascii=False, indent=0)
    print(json.dumps({k: R.get(k) for k in ('dau_ra', 'smr', 'dat', 'stem')}, ensure_ascii=False))
