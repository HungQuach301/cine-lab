#!/opt/cine/bin/python
"""CASTING-MỸ · máy kiểm từng giọng (như casting-giong/kiem.py, rút còn 2 đoạn, không có bảng phát âm 40 mục): kiem.py <ma> … → $CG_OUT/kiem-<ma>.json
- ASR 2 cách nghe (medium.en beam 5, small.en beam 1; không hotwords). Tỷ lệ từ đúng so lời KHOÁ; mọi số/năm theo giá trị; tên trong đoạn khớp mờ ≥ 0,75
  với chữ viết hoặc alias. SAI = cả hai cách nghe trượt; NGHI = một cách nghe trượt.
- Từ/giây = từ viết / thời lượng lời (từ đầu tiên → từ cuối, dấu thời gian ASR medium). Ước lời T3 = 1 571 từ viết của loi-khoa.txt / từ/giây.
- Nối 2 đoạn (lặng 0,8 s, mono 48 kHz WAV) cho F0 (pyin) và gói nghe (nghe_mu.py)."""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import my_lib as M
K, L = M.K, M.L
DT = json.load(open(f'{M.H}/doan-thu.json'))['doan']
TD = {d['viet']: d for d in json.loads((K.R / 'channel-k2/k2c-t3-01/khoa-loi/phat-am/tu-dien.json').read_text())['muc']}
TD["d'Arçon"] = dict(TD["d'Arçon"], doc='dar-sohn')   # alias Đ3
TEN = {'1-moc': ['Gibraltar', 'Spain', 'Mediterranean'], '2-pin-noi': ['French', 'Spanish', 'British', 'Duc de Crillon', "d'Arçon", 'September']}
LOI = (K.R / 'channel-k2/k2c-t3-01/loi-khoa.txt').read_text()
TU_T3 = sum(len(l.split()) for l in LOI.splitlines() if l.strip() and not l.startswith('['))
import asr as A   # noqa: E402  (scripts/ll, nạp qua kiem_lib)


def item_ok(item, hyp):
    if item in TD and TD[item]['loai'] == 'năm': return K.num_ok(float(item), hyp)
    return K.name_ok(item, hyp, TD.get(item, {}).get('doc')) >= 0.75


def run(ma):
    meta = json.load(open(f'{L.OUT}/{ma}.json')); R = dict(ma=ma, voice_id=meta['voice_id'], doan=[], nghe=[n for n, _ in K.NGHE])
    words_all = 0; span_all = 0.0
    for d, f in zip(DT, meta['tep']):
        row = dict(doan=d['doan'], giay_tep=round(K.dur(f), 2), nghe={})
        for name, beam in K.NGHE:
            txt, ws = K.transcribe(f, name, beam); w = K.wer(d['khoa'], txt); so = sorted(A.nums_of(d['khoa']))
            row['nghe'][name] = dict(asr=txt, tu_dung=w['tu_dung'], loi=w['loi'], so_tu=w['so_tu'], cho_lech=w['cho_lech'],
                                     so_thieu=[v for v in so if not K.num_ok(v, txt)], ten_thieu=[t for t in TEN[d['doan']] if not item_ok(t, txt)],
                                     muc_tu_dien_sai=[m for m in d['muc_tu_dien'] if not item_ok(m, txt)])
            if name == K.NGHE[0][0]: row['giay_loi'] = round(K.speech_span(ws), 2)
        row['tu_viet'] = len(d['khoa'].split()); row['tu_giay'] = round(row['tu_viet'] / row['giay_loi'], 3)
        words_all += row['tu_viet']; span_all += row['giay_loi']; R['doan'].append(row)

    def hai(get):
        a = [set(get(n)) for n, _ in K.NGHE]; return sorted(a[0] & a[1]), sorted((a[0] | a[1]) - (a[0] & a[1]))
    R['so_thieu'], R['so_nghi'] = hai(lambda n: [v for r in R['doan'] for v in r['nghe'][n]['so_thieu']])
    R['ten_thieu'], R['ten_nghi'] = hai(lambda n: [t for r in R['doan'] for t in r['nghe'][n]['ten_thieu'] + r['nghe'][n]['muc_tu_dien_sai']])
    R['tu_giay'] = round(words_all / span_all, 3); R['uoc_loi_T3_giay'] = round(TU_T3 / R['tu_giay'], 1); R['tu_T3'] = TU_T3
    R['tu_dung'] = {n: round(sum(r['nghe'][n]['so_tu'] - r['nghe'][n]['loi'] for r in R['doan']) / sum(r['nghe'][n]['so_tu'] for r in R['doan']), 4) for n in R['nghe']}
    cat = f'{L.OUT}/{ma}-noi.wav'; ins = sum((['-i', f] for f in meta['tep']), [])
    fl = ''.join(f'[{i}:a]aresample=48000,aformat=channel_layouts=mono[a{i}];' for i in range(2)) + 'anullsrc=r=48000:cl=mono,atrim=0:0.8[s0];[a0][s0][a1]concat=n=3:v=0:a=1[o]'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', fl, '-map', '[o]', '-c:a', 'pcm_s24le', cat], check=True)
    R['f0'] = dict(zip(('trung_vi', 'p10', 'p90'), K.f0(cat)))
    json.dump(R, open(f'{L.OUT}/kiem-{ma}.json', 'w'), ensure_ascii=False, indent=1)
    print(ma, R['tu_dung'], 'số', R['so_thieu'], R['so_nghi'], 'tên', R['ten_thieu'], R['ten_nghi'], 'tốc độ', R['tu_giay'], [r['tu_giay'] for r in R['doan']],
          'T3', R['uoc_loi_T3_giay'], 'F0', R['f0'], flush=True)


if __name__ == '__main__':
    for m in sys.argv[1:]: run(m)
