#!/opt/cine/bin/python
"""GIỌNG-CHỐT · máy kiểm G1 (dùng lại casting-giong/kiem_lib): ASR 2 cách nghe (medium.en beam 5, small.en beam 1; không hotwords) trên mọi bản thu
(bang, moc-1.00/1.03/1.06, pin-v2, pin-v4) → $CG_OUT/kiem.json + may-kiem.json (bản gọn, vào git).
- Từ đúng so lời KHOÁ (chuẩn hoá số); số/năm theo giá trị; tên khớp mờ ≥ 0,75 với chữ viết hoặc alias (như casting).
- 47 mục = 41 ở `bang` (40 mục + câu 5i có "18 October 2026") + 3 ở móc (1309, 1783, 2026; bản speed 1,00) + 3 ở pin (1782, Duc de Crillon, d'Arçon; bản v2).
  ĐÚNG khi đạt ở CẢ HAI cách nghe; NGHI khi chỉ một cách nghe nhận ra; SAI khi cả hai đều không.
- Tốc độ: từ viết / thời lượng lời (đầu từ đầu → cuối từ cuối, dấu thời gian ASR medium)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import gc_lib as G
K, L = G.K, G.L
import asr as A
D = json.load(open(f'{G.H}/doan.json')); IDX = json.load(open(f'{L.OUT}/thu.json'))
TD = {d['viet']: d for d in json.loads((K.R / 'channel-k2/k2c-t3-01/khoa-loi/phat-am/tu-dien.json').read_text())['muc']}
TEN = {'moc': ['Gibraltar', 'Spain', 'Mediterranean'], 'pin': ['French', 'Spanish', 'British', 'Duc de Crillon', "d'Arçon", 'September'], 'bang': []}


def item_ok(item, hyp):
    if item in TD and TD[item]['loai'] == 'năm': return K.num_ok(float(item), hyp)
    if item == '18 October 2026': return K.num_ok(2026.0, hyp) and (K.num_ok(18.0, hyp) or 'eighteenth' in hyp.lower())
    return K.name_ok(item, hyp, TD.get(item, {}).get('doc')) >= 0.75


def diem(item, hyp): return 1.0 if item_ok(item, hyp) else (K.name_ok(item, hyp, TD.get(item, {}).get('doc')) if TD.get(item, {}).get('loai') != 'năm' else 0.0)


R = {}
for tag, meta in IDX.items():
    doan = tag.split('-')[0].replace('mocb', 'moc'); d = D[doan]; f = meta['tep']; row = dict(tag=tag, model=meta['model'], settings=meta['settings'], giay_tep=round(K.dur(f), 2), nghe={})
    for name, beam in K.NGHE:
        txt, ws = K.transcribe(f, name, beam); w = K.wer(d['khoa'], txt)
        row['nghe'][name] = dict(asr=txt, tu_dung=w['tu_dung'], loi=w['loi'], so_tu=w['so_tu'], cho_lech=w['cho_lech'],
                                 so_thieu=[v for v in sorted(A.nums_of(d['khoa'])) if not K.num_ok(v, txt)] if doan != 'bang' else [],
                                 ten_thieu=[t for t in TEN[doan] if not item_ok(t, txt)],
                                 muc_sai=[m for m in d['muc'] if not item_ok(m, txt)], diem={m: diem(m, txt) for m in d['muc']})
        if name == K.NGHE[0][0]: row['giay_loi'] = round(K.speech_span(ws), 2)
    row['tu_viet'] = len(d['khoa'].split()); row['tu_giay'] = round(row['tu_viet'] / row['giay_loi'], 3)
    row['f0'] = dict(zip(('trung_vi', 'p10', 'p90'), K.f0(f)))
    R[tag] = row; print(tag, row['giay_loi'], row['tu_giay'], {n: (v['tu_dung'], v['so_thieu'], v['ten_thieu'], v['muc_sai']) for n, v in row['nghe'].items()}, flush=True)


def hai(tags):
    s = [set(m for t in tags for m in R[t]['nghe'][n]['muc_sai']) for n, _ in K.NGHE]
    return sorted(s[0] & s[1]), sorted((s[0] | s[1]) - (s[0] & s[1]))


sai, nghi = hai(['bang', 'moc-1.00', 'pin-v2'])
P47 = dict(sai=sai, nghi=nghi, dung_ca_hai=47 - len(sai) - len(nghi), dat_it_nhat_mot=47 - len(sai))
sai4, nghi4 = hai(['pin-v4']); P47['pin_v4'] = dict(sai=sai4, nghi=nghi4, muc=D['pin']['muc'])
OUT = dict(ghi='G1 · GIỌNG-CHỐT · ASR M=medium.en beam5, S=small.en beam1, không hotwords', ban=R, phat_am_47=P47)
json.dump(OUT, open(f'{L.OUT}/kiem.json', 'w'), ensure_ascii=False, indent=1)
gon = {t: dict(model=r['model'], settings=r['settings'], giay_tep=r['giay_tep'], giay_loi=r['giay_loi'], tu_viet=r['tu_viet'], tu_giay=r['tu_giay'], f0=r['f0'],
               nghe={n: dict(asr=v['asr'], tu_dung=v['tu_dung'], cho_lech=v['cho_lech'], so_thieu=v['so_thieu'], ten_thieu=v['ten_thieu'], muc_sai=v['muc_sai'], diem=v['diem'])
                     for n, v in r['nghe'].items()}) for t, r in R.items()}
json.dump(dict(ghi=OUT['ghi'], ban=gon, phat_am_47=P47), open(f'{G.H}/may-kiem.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(P47, ensure_ascii=False))
