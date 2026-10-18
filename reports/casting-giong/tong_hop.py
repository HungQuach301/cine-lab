#!/opt/cine/bin/python
"""CASTING-GIỌNG · gộp kết quả máy kiểm theo mã mù G (khoa-ten.json) → may-kiem.json (không có tên giọng/nguồn).
Ước phim T3: bảng shot 719,667 s dựng cho lời ≈ 668 s (2,5 từ nói/s, KHOA-LOI-41 §3); lời dài hơn 668 s thì shot phải giãn ⇒
phim ≈ 719,667 + max(0, lời − 668). Tốc độ cần để vừa bảng shot hiện tại = lời / 668 (tham số speed của ElevenLabs, 0,7–1,2)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import cg_lib as L
H = os.path.dirname(os.path.abspath(__file__)); KT = json.load(open(f'{H}/khoa-ten.json'))['G']
BANG, LOI25, TRAN = 719.667, 668.0, 721.2
def row(m):
    R = json.load(open(f'{L.OUT}/kiem-{m}.json')); A = json.load(open(f'{L.OUT}/alias-{m}.json')); loi = R['uoc_loi_T3_giay']; phim = round(BANG + max(0, loi - LOI25), 1)
    return dict(tu_dung_medium=R['tu_dung']['medium.en'], tu_dung_small=R['tu_dung']['small.en'], so_sai=R['so_thieu'], so_nghi=R['so_nghi'], ten_sai=R['ten_thieu'], ten_nghi=R['ten_nghi'],
                phat_am_dung_47=R['phat_am']['dung_47'], phat_am_sai=R['phat_am']['sai_47'], phat_am_nghi=R['phat_am']['nghi_47'], alias_thay_dung=f"{len(A['dung'])}/7", alias_thay_asr=A['nghe']['medium.en']['asr'],
                tu_giay=R['tu_giay'], tu_giay_doan=[d['tu_giay'] for d in R['doan']], uoc_loi_T3=loi, uoc_phim_T3=phim, lech_tran_pct=round((phim - TRAN) / TRAN * 100, 1),
                speed_can=round(max(1.0, loi / LOI25), 3), f0=R['f0'],
                lech_asr=[(d['doan'], c) for d in R['doan'] for c in d['nghe']['medium.en']['cho_lech']])
out = {g: dict(row(v['ma']), I=v['I'], TP=v['TP'], giay=v['giay'], mb=v['mb'], sha256=v['sha256'], tep=f'nghe-mu/{g}.mp3') for g, v in KT.items()}
loai = {'L-a': 'A3', 'L-b': 'B-nigel'}
out_loai = {k: row(m) for k, m in loai.items()}
json.dump(dict(G=out, loai=out_loai), open(f'{H}/may-kiem.json', 'w'), ensure_ascii=False, indent=1)
for g, r in list(out.items()) + list(out_loai.items()):
    print(g, r['tu_dung_medium'], r['tu_dung_small'], 'so', r['so_sai'], r['so_nghi'], 'ten', r['ten_sai'], r['ten_nghi'], 'pa', r['phat_am_dung_47'], r['phat_am_sai'], 'alias', r['alias_thay_dung'], 'wps', r['tu_giay'], r['tu_giay_doan'], 'loi', r['uoc_loi_T3'], 'phim', r['uoc_phim_T3'], r['lech_tran_pct'], 'speed', r['speed_can'], 'f0', r['f0'], r.get('I'), r.get('TP'), r.get('giay'))
