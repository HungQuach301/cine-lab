#!/opt/cine/bin/python
"""CASTING-GIỌNG · máy kiểm từng giọng: kiem.py <ma> [<ma> …] → $CG_OUT/kiem-<ma>.json
- ASR 2 cách nghe (medium.en beam 5, small.en beam 1; không hotwords) trên 3 đoạn + bảng phát âm.
- Tỷ lệ từ đúng (so lời KHOÁ, chuẩn hoá số), mọi số/năm (theo giá trị), mọi tên riêng (khớp mờ ≥ 0,75 với chữ viết hoặc alias).
- Phát âm 47 mục (40 ở bảng + 7 trong đoạn thử): ĐÚNG khi đạt ở CẢ HAI cách nghe.
- Nối 3 đoạn (lặng 0,8 s) → chuẩn −14 LUFS, đỉnh thật ≤ −1 dBTP (alimiter khi cần) → MP3 192 kb/s; đo lại bằng ebur128.
- Tốc độ: từ viết / thời lượng lời (từ đầu từ đầu tiên tới cuối từ cuối, theo dấu thời gian ASR); ước lời T3 = số từ viết của loi-khoa.txt (1 571, split()) / tốc độ."""
import json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import kiem_lib as K, cg_lib as L
sys.path.insert(0, str(K.R / 'scripts/audio')); import lib as AL
H = os.path.dirname(os.path.abspath(__file__))
DT = json.load(open(f'{H}/doan-thu.json'))['doan']; PA = json.load(open(f'{H}/phat-am-thu.json'))
TD = {d['viet']: d for d in json.loads((K.R / 'channel-k2/k2c-t3-01/khoa-loi/phat-am/tu-dien.json').read_text())['muc']}
TEN = {'1-moc': ['Gibraltar', 'Spain', 'Mediterranean'], '2-pin-noi': ['French', 'Spanish', 'British', 'Duc de Crillon', "d'Arçon", 'September'],
       '3-ket-so-lieu': ['Gibraltar', 'Spain', 'Britain', 'European Parliament', 'sovereignty', 'provisionally', 'October', 'December']}
LOI = (K.R / 'channel-k2/k2c-t3-01/loi-khoa.txt').read_text()
TU_T3 = sum(len(l.split()) for l in LOI.splitlines() if l.strip() and not l.startswith('['))


def item_ok(item, hyp):
    if item in TD and TD[item]['loai'] == 'năm': return K.num_ok(float(item), hyp)
    if item == '18 October 2026': return K.num_ok(2026.0, hyp) and (K.num_ok(18.0, hyp) or 'eighteenth' in hyp.lower())
    return K.name_ok(item, hyp, TD.get(item, {}).get('doc')) >= 0.75


def run(ma):
    meta = json.load(open(f'{L.OUT}/{ma}.json')); R = dict(ma=ma, voice_id=meta['voice_id'], doan=[], nghe=[n for n, _ in K.NGHE])
    words_all = 0; span_all = 0.0
    for d, f in zip(DT, meta['tep']):
        row = dict(doan=d['doan'], giay_tep=round(K.dur(f), 2), nghe={})
        for name, beam in K.NGHE:
            txt, ws = K.transcribe(f, name, beam); w = K.wer(d['khoa'], txt)
            so = sorted(A for A in __import__('asr').nums_of(d['khoa']))
            row['nghe'][name] = dict(asr=txt, tu_dung=w['tu_dung'], loi=w['loi'], so_tu=w['so_tu'], cho_lech=w['cho_lech'],
                                     so_thieu=[v for v in so if not K.num_ok(v, txt)],
                                     ten_thieu=[t for t in TEN[d['doan']] if not item_ok(t, txt)],
                                     muc_tu_dien_sai=[m for m in d['muc_tu_dien'] if not item_ok(m, txt)])
            if name == K.NGHE[0][0]: row['giay_loi'] = round(K.speech_span(ws), 2)
        row['tu_viet'] = len(d['khoa'].split()); row['tu_giay'] = round(row['tu_viet'] / row['giay_loi'], 3)
        words_all += row['tu_viet']; span_all += row['giay_loi']; R['doan'].append(row)
    pa = {}
    for name, beam in K.NGHE:
        txt, _ = K.transcribe(meta['phat_am'], name, beam); pa[name] = dict(asr=txt, sai=[m for m in PA['muc'] if not item_ok(m, txt)])
    # một mục SAI khi cả hai cách nghe đều không nhận ra (ASR tiếng Anh viết sai tên TBN/Pháp); NGHI khi chỉ một cách nghe nhận ra
    def hai(get):
        a = [set(get(n)) for n, _ in K.NGHE]; return sorted(a[0] & a[1]), sorted((a[0] | a[1]) - (a[0] & a[1]))
    sai, nghi = hai(lambda n: pa[n]['sai'] + [m for r in R['doan'] for m in r['nghe'][n]['muc_tu_dien_sai']])
    R['phat_am'] = dict(nghe=pa, sai_47=sai, nghi_47=nghi, dung_47=47 - len(sai))
    R['tu_giay'] = round(words_all / span_all, 3); R['uoc_loi_T3_giay'] = round(TU_T3 / R['tu_giay'], 1); R['tu_T3'] = TU_T3
    R['tu_dung'] = {n: round(sum(r['nghe'][n]['so_tu'] - r['nghe'][n]['loi'] for r in R['doan']) / sum(r['nghe'][n]['so_tu'] for r in R['doan']), 4) for n in R['nghe']}
    R['so_thieu'], R['so_nghi'] = hai(lambda n: [v for r in R['doan'] for v in r['nghe'][n]['so_thieu']])
    R['ten_thieu'], R['ten_nghi'] = hai(lambda n: [t for r in R['doan'] for t in r['nghe'][n]['ten_thieu']])
    # nối + loudness
    cat = f'{L.OUT}/{ma}-noi.wav'; ins = sum((['-i', f] for f in meta['tep']), [])
    fl = ''.join(f'[{i}:a]aresample=48000,aformat=channel_layouts=mono[a{i}];' for i in range(3)) + 'anullsrc=r=48000:cl=mono,atrim=0:0.8[s0];anullsrc=r=48000:cl=mono,atrim=0:0.8[s1];[a0][s0][a1][s1][a2]concat=n=5:v=0:a=1[o]'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', fl, '-map', '[o]', '-c:a', 'pcm_s24le', cat], check=True)
    x = AL.dec(cat, 1); I0 = AL.integrated(x); g = -14.0 - I0
    out = f'{L.OUT}/{ma}-14lufs.mp3'
    for lim in (None, 0.70, 0.63):
        af = f'volume={g:.3f}dB' + (f',alimiter=limit={lim}:level=false:attack=1:release=50,volume=0dB' if lim else '')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', cat, '-af', af, '-ar', '44100', '-c:a', 'libmp3lame', '-b:a', '192k', out], check=True)
        M = AL.ebur128(out)
        for _ in range(3):   # chỉnh gain theo số đo trên chính tệp MP3
            if abs(M['I'] + 14) <= 0.1: break
            g += -14 - M['I']; af = f'volume={g:.3f}dB' + (f',alimiter=limit={lim}:level=false:attack=1:release=50' if lim else '')
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', cat, '-af', af, '-ar', '44100', '-c:a', 'libmp3lame', '-b:a', '192k', out], check=True); M = AL.ebur128(out)
        if M['TP'] <= -1.0 and abs(M['I'] + 14) <= 0.3: break
    R['loudness'] = dict(LUFS_goc=round(I0, 2), I=M['I'], TP=M['TP'], limiter=lim, dat=M['TP'] <= -1.0 and -15.0 <= M['I'] <= -13.8, tep=out, sha256=AL.sha256(out), giay=round(K.dur(out), 2))
    R['f0'] = dict(zip(('trung_vi', 'p10', 'p90'), K.f0(cat)))
    json.dump(R, open(f'{L.OUT}/kiem-{ma}.json', 'w'), ensure_ascii=False, indent=1)
    print(ma, R['tu_dung'], 'số thiếu', R['so_thieu'], R['so_nghi'], 'tên thiếu', R['ten_thieu'], R['ten_nghi'], 'phát âm', R['phat_am']['dung_47'], sai, 'nghi', nghi, 'tốc độ', R['tu_giay'], 'T3', R['uoc_loi_T3_giay'], 'LUFS', R['loudness']['I'], R['loudness']['TP'], 'F0', R['f0'], flush=True)


if __name__ == '__main__':
    for m in sys.argv[1:]: run(m)
