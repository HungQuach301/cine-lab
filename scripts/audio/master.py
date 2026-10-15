#!/opt/cine/bin/python
"""ÂM THANH · chuỗi hoàn thiện âm thanh dùng lại (phiên Âm thanh, Mốc C, 15/10/2026).

  master.py <ra.wav> --vo vo.flac --music music.flac [--sfx sfx.flac] --speech speech.json|timeline.json
            [--smr 15] [--duck -12] [--I -14] [--tp -1] [--fade-in 1.5] [--fade-out 3] [--aac 256k] [--json ra.json]

Đầu vào là STEM chưa trộn, đặt sẵn trên trục thời gian (scripts/audio/compose.py, hoặc scripts/ll/mix.py --stems: raw-vo, raw-music, raw-sfx).
Chuỗi (mọi tham số chỉnh được; mặc định là đề xuất cho luật K, docs/AUDIO-THUOC-DO.md):
  1. Lời: lọc thấp 70 Hz → khử xì nhẹ (deesser) → nén nhẹ 2,5:1 (ngưỡng −24 dBFS, attack 5 ms, release 120 ms, knee 6) → chuẩn −17 LUFS trên vùng có lời.
  2. Ducking nhạc theo lời, THÍCH ỨNG (duck cơ bản −12 dB = mức của mix.py mà T1/Steel đã duyệt; chỉ hạ thêm khi cần): mỗi khoảng lời (gộp quãng nghỉ < 0,8 s) hạ nền (nhạc + ½ mức cho SFX) một mức HẰNG trong khoảng:
        mức = min(duck_cơ_bản, L_lời(khoảng) − SMR_đích − 1 dB − L_nền_ngắn_hạn_lớn_nhất(khoảng)), sàn −30 dB;
     vào 250 ms trước lời, ra 450 ms sau lời (đường cong smoothstep) — không "bơm" giữa các từ.
  3. Fade: nền vào fade_in giây, ra fade_out giây cuối; cả bản thêm dốc ra bắt đầu không sớm hơn 0,3 s sau từ cuối (không cắt lời).
  4. Loudness 2 lượt (ffmpeg loudnorm): lượt 1 đo → nhân hệ số + giới hạn đỉnh thật (alimiter trên tín hiệu nâng mẫu ×4, trần = TP − 0,5 dB)
     → lượt 2 loudnorm linear=true với số đo lượt 2 (chỉ khuếch đại tuyến tính; báo normalization_type).
  5. Kiểm sau mã hoá AAC (như master thật): đỉnh thật sau AAC > TP → hạ trần limiter đúng phần vượt; I đo lại bằng ebur128 lệch > 0,1 LU → bù tuyến tính; làm lại (≤ 4 vòng). BAI-HOC-LL #69.
  6. Báo JSON: số đo đầu vào/từng lượt/đầu ra, SMR (stem lời đã xử lý vs nền đã duck), mức duck từng khoảng, lặng, chạm trần, tham số.
"""
import json, os, subprocess, sys, tempfile
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib, measure

SR = lib.SR
DEF = dict(smr=15.0, duck=-12.0, duck_floor=-30.0, merge_gap=0.8, attack=0.25, release=0.45, sfx_duck_ratio=0.5, vo_lufs=-17.0,
           I=-14.0, tp=-1.0, tp_margin=0.5, fade_in=1.5, fade_out=3.0, aac='256k',
           vo_chain='highpass=f=70,deesser=i=0.35:m=0.5:f=0.5:s=o,acompressor=threshold=-24dB:ratio=2.5:attack=5:release=120:knee=6')


def vo_process(vo, chain):
    with tempfile.TemporaryDirectory() as d:
        a = os.path.join(d, 'a.wav'); lib.write(a, vo, 'pcm_f32le'); return lib.dec(a, vo.shape[1], af=chain)


def smooth_env(N, iv, levels, attack, release):
    """đường hạ (dB, ≤ 0) theo khoảng lời: mỗi khoảng một mức hằng, dốc smoothstep"""
    env = np.zeros(N); t = lambda i0, i1: np.arange(i0, i1) / SR
    for (a, b), L in zip(iv, levels):
        i0, i1 = max(0, int((a - attack) * SR)), min(N, int((b + release) * SR)); tt = t(i0, i1)
        u = np.clip(np.minimum((tt - (a - attack)) / attack, ((b + release) - tt) / release), 0, 1); u = u * u * (3 - 2 * u)
        env[i0:i1] = np.minimum(env[i0:i1], L * u)
    return env


def st_loud(x, win=3.0, hop=0.1):
    """loudness ngắn hạn (lọc K) cửa sổ 3 s, bước 100 ms → (t_đầu_cửa_sổ, LUFS)"""
    p = lib.power(x, win, hop); return np.arange(len(p)) * hop, lib.lu(p)


def ducking(vo, bed, speech, C):
    """mức duck (dB) cho từng khoảng lời + lý do"""
    iv = lib.merge(speech, C['merge_gap']); tb, Lb = st_loud(bed, 3.0); kv = lib.kw(vo).astype(np.float64); out = []
    for a, b in iv:
        i0, i1 = int(a * SR), int(b * SR); pv = (kv[i0:i1] ** 2).sum(1); Lv = float(lib.lu(pv.mean())) if i1 > i0 else -70
        sel = (tb >= a - 0.5) & (tb + 3.0 <= b + 0.5)
        if not sel.any(): sel = (tb <= a) & (tb + 3.0 >= a)
        Lbmax = float(Lb[sel].max()) if sel.any() else -70
        need = Lv - C['smr'] - 1.0 - Lbmax   # cần hạ thêm bao nhiêu để nền ≤ lời − SMR − 1 dB
        lvl = max(C['duck_floor'], min(C['duck'], need))
        out.append(dict(t0=round(a, 2), t1=round(b, 2), L_loi=round(Lv, 1), L_nen_max=round(Lbmax, 1), duck_db=round(lvl, 1)))
    return iv, out


def ffm(args, **kw):
    return subprocess.run(['ffmpeg', '-v', 'error', '-nostdin', '-y'] + args, check=True, **kw)


def loudness_2pass(mix, C, work, ceiling_db, extra_db=0.0):
    """lượt 1 đo → gain + limiter ×4 → lượt 2 loudnorm linear. Trả (đường dẫn wav 24 bit, nhật ký)"""
    raw = os.path.join(work, 'sum.wav')
    if not os.path.exists(raw): lib.write(raw, mix, 'pcm_f32le')
    m1 = lib.loudnorm_measure(raw, C['I'], C['tp']); g = C['I'] - float(m1['input_i']) + extra_db
    lim = os.path.join(work, 'lim.wav')
    ffm(['-i', raw, '-af', f'volume={g:.3f}dB,aresample=192000,alimiter=limit={10 ** (ceiling_db / 20):.5f}:attack=1:release=60:level=disabled:asc=1,aresample=48000',
         '-c:a', 'pcm_f32le', lim])
    m2 = lib.loudnorm_measure(lim, C['I'] + extra_db, C['tp'])   # đích loudnorm dời theo phần bù (loudnorm tự đo lệch ebur128 trên clip ngắn)
    out = os.path.join(work, 'out.wav'); lra = max(11.0, float(m2['input_lra']) + 1)
    r = subprocess.run(['ffmpeg', '-v', 'info', '-nostdin', '-y', '-i', lim, '-af',
                        f"loudnorm=I={C['I'] + extra_db:.2f}:TP={C['tp']}:LRA={lra}:measured_I={m2['input_i']}:measured_TP={m2['input_tp']}:measured_LRA={m2['input_lra']}:"
                        f"measured_thresh={m2['input_thresh']}:offset={m2['target_offset']}:linear=true:print_format=json,aresample=48000",
                        '-c:a', 'pcm_s24le', '-ar', '48000', out], capture_output=True, text=True)
    if r.returncode: raise SystemExit('loudnorm lượt 2 lỗi: ' + r.stderr[-500:])
    j = json.loads(r.stderr[r.stderr.rfind('{'):r.stderr.rfind('}') + 1])
    return out, dict(luot1=dict(I=float(m1['input_i']), TP=float(m1['input_tp']), LRA=float(m1['input_lra'])), gain_db=round(g, 2), bu_db=round(extra_db, 2), tran_limiter_dbtp=round(ceiling_db, 2),
                     luot2=dict(I=float(m2['input_i']), TP=float(m2['input_tp']), LRA=float(m2['input_lra'])), loudnorm=dict(normalization_type=j.get('normalization_type'),
                     output_i=float(j['output_i']), output_tp=float(j['output_tp']), target_offset=float(j.get('target_offset', 0))))


def aac_tp(wav, rate, work):
    p = os.path.join(work, 'x.m4a'); ffm(['-i', wav, '-c:a', 'aac', '-b:a', rate, '-ar', '48000', p]); return lib.ebur128(p)


def finish(vo, music=None, sfx=None, speech=None, out_wav=None, **kw):
    """vo (N,1|2), music (N,2), sfx (N,2)|None — mảng sẽ bị chuyển float32 và GIẢI PHÓNG trong hàm (tiết kiệm bộ nhớ: phim 17 phút ≈ 50 triệu mẫu)"""
    if isinstance(vo, dict): S = vo; vo, music, sfx = S.pop('vo'), S.pop('music'), S.pop('sfx')   # gọi bằng dict: hàm giữ tham chiếu duy nhất → giải phóng được
    C = dict(DEF, **{k: v for k, v in kw.items() if v is not None}); N = max(len(vo), len(music), len(sfx) if sfx is not None else 0); dur = N / SR
    f32 = lambda x, ch: np.zeros((N, ch), np.float32) if x is None else (x if x.dtype == np.float32 and len(x) == N else np.pad(np.asarray(x, np.float32), ((0, N - len(x)), (0, 0))))
    vo1 = f32(vo[:, :1], 1); del vo; music = f32(music, 2); sfx = f32(sfx, 2)
    # 1. lời (mono; nhân đôi kênh khi trộn)
    vp = vo_process(vo1, C['vo_chain'])[:, 0].astype(np.float32); del vo1
    vp = vp[:N] if len(vp) >= N else np.pad(vp, (0, N - len(vp)))
    mask = np.zeros(N, bool)
    for a, b in speech: mask[int(a * SR):int(b * SR)] = True
    Lvo = lib.integrated(np.stack([vp[mask], vp[mask]], 1)) if mask.any() else -70; del mask; vp *= np.float32(10 ** ((C['vo_lufs'] - Lvo) / 20))
    # 2. ducking thích ứng
    bed0 = music + sfx; iv, D = ducking(vp[:, None], bed0, speech, C); del bed0
    env = smooth_env(N, iv, [d['duck_db'] for d in D], C['attack'], C['release'])
    # 3. fade
    # nền: vào fade_in, ra fade_out giây cuối (như mix.py); cả bản: dốc ngắn sau từ cuối (không cắt lời)
    t = np.arange(N) / SR; last = max((b for a, b in speech), default=0.0)
    fo0 = max(last + 0.3, dur - C['fade_out']); fade_out = np.clip((dur - t) / max(dur - fo0, 0.05), 0, 1).astype(np.float32)
    fin = (np.clip(t / C['fade_in'], 0, 1) if C['fade_in'] > 0 else np.ones(N)) * np.clip((dur - t) / C['fade_out'], 0, 1); fin = fin.astype(np.float32); del t
    gm = (10 ** (env / 20)).astype(np.float32) * fin; gs = (10 ** (env * C['sfx_duck_ratio'] / 20)).astype(np.float32) * fin; del env, fin
    bed = (music * gm[:, None] + sfx * gs[:, None]) * fade_out[:, None]; del music, sfx, gm, gs
    vp *= fade_out; del fade_out
    # SMR trên stem đã xử lý (hệ số master chung cho cả hai nên tỉ số không đổi) — đo trước khi trộn để giải phóng stem
    smr = measure.stats(measure.smr_stems(np.stack([vp, vp], 1), bed, speech), C['smr'])
    bed += vp[:, None]; mix = bed; del vp
    # 4–5. loudness 2 lượt + kiểm sau AAC
    log = []; ceiling = C['tp'] - C['tp_margin']
    with tempfile.TemporaryDirectory(dir=os.path.dirname(os.path.abspath(out_wav))) as work:
        extra = 0.0
        for k in range(4):   # ≤ 4 vòng: hạ trần khi đỉnh sau AAC vượt; bù tuyến tính khi I (ebur128) lệch > 0,1 LU (loudnorm đo lệch trên clip ngắn)
            o, L = loudness_2pass(mix, C, work, ceiling, extra); A = aac_tp(o, C['aac'], work); E = lib.ebur128(o)
            L['aac'] = dict(I=A['I'], TP=A['TP']); L['ebur128'] = dict(I=E['I'], TP=E['TP']); log.append(L)
            tp_ok = A['TP'] <= C['tp']; dI = C['I'] - E['I']
            if tp_ok and abs(dI) <= 0.1: break
            if not tp_ok: ceiling -= (A['TP'] - C['tp']) + 0.1
            if abs(dI) > 0.1: extra += dI
        os.replace(o, out_wav)
    # 6. báo cáo
    del mix; M = measure.measure(out_wav, None)
    R = dict(cong_cu='scripts/audio/master.py', tham_so={k: C[k] for k in C}, tong_s=round(dur, 3), loi_LUFS_truoc_chuan=round(float(Lvo), 2),
             duck=dict(so_khoang=len(D), trung_vi_db=float(np.median([d['duck_db'] for d in D])) if D else 0, sau_nhat_db=min((d['duck_db'] for d in D), default=0),
                       khoang_vuot_co_ban=sum(1 for d in D if d['duck_db'] < C['duck'] - 0.05), ds=D),
             fade=dict(nen_vao_s=C['fade_in'], nen_ra_s=C['fade_out'], ca_ban_ra_bat_dau_s=round(fo0, 2), ca_ban_ra_s=round(dur - fo0, 2)), loudness=log,
             dau_ra=dict(I=M['I'], LRA=M['LRA'], TP=M['TP'], TP_sau_aac=log[-1]['aac']['TP'], lang_pct=M['lang_pct'], lang_bat_thuong=M['lang_bat_thuong']['so'], cham_tran=M['cham_tran']),
             smr=smr)
    R['dat'] = dict(I=abs(M['I'] - C['I']) <= 0.2, TP=M['TP'] <= C['tp'], TP_sau_aac=log[-1]['aac']['TP'] <= C['tp'], SMR_p10=bool(smr and smr['p10'] >= C['smr']),
                    loudnorm_tuyen_tinh=log[-1]['loudnorm']['normalization_type'] == 'linear')
    return R


def arg(k, d=None, f=str):
    return f(sys.argv[sys.argv.index('--' + k) + 1]) if '--' + k in sys.argv else d


if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1].startswith('--'): sys.exit(__doc__)
    sp, _ = measure.load_speech(arg('speech'))
    R = finish(dict(vo=lib.dec(arg('vo'), 1, dtype=np.float32), music=lib.dec(arg('music'), 2, dtype=np.float32), sfx=lib.dec(arg('sfx'), 2, dtype=np.float32) if arg('sfx') else None), speech=sp, out_wav=sys.argv[1],
               smr=arg('smr', None, float), duck=arg('duck', None, float), I=arg('I', None, float), tp=arg('tp', None, float),
               fade_in=arg('fade-in', None, float), fade_out=arg('fade-out', None, float), aac=arg('aac'))
    js = arg('json', sys.argv[1].rsplit('.', 1)[0] + '.json'); json.dump(R, open(js, 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(dict(dau_ra=R['dau_ra'], smr=R['smr'], dat=R['dat'], duck={k: v for k, v in R['duck'].items() if k != 'ds'}), ensure_ascii=False))
