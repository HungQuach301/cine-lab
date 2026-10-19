#!/opt/cine/bin/python
"""CASTING-MỸ · gộp máy kiểm theo mã mù M (khoa-ten.json) → may-kiem.json (không có tên/nguồn giọng).
Ước thời lượng: 2 đoạn thử (móc + pin nổi) đọc CHẬM hơn trung bình cả lời (pin nổi có nhiều chỗ ngừng). Hiệu chỉnh bằng đối chứng G1, giọng duy nhất có cả
số đo 3 đoạn (casting-giong: 2,202 từ/s → lời T3 713,4 s) và số đo 2 đoạn (phiên này): hệ số = 713,4 / lời_2đoạn(G1). Áp cùng hệ số cho mọi giọng
(giả định: tỷ lệ nhịp giữa các đoạn giống nhau giữa các giọng; sai số ước ±5 %).
Phim T3 ≈ 719,667 + max(0, lời − 668) (bảng shot dựng cho lời ≈ 668 s, KHOA-LOI-41 §3); speed cần = lời / 668 (ElevenLabs 0,7–1,2)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import my_lib as M
L, H = M.L, M.H; KT = json.load(open(f'{H}/khoa-ten.json'))['G']
BANG, LOI25, TRAN, G1_3DOAN = 719.667, 668.0, 721.2, 713.4
HS = G1_3DOAN / json.load(open(f'{L.OUT}/kiem-DC-G1.json'))['uoc_loi_T3_giay']
out = {}
for g, v in KT.items():
    R = json.load(open(f'{L.OUT}/kiem-{v["ma"]}.json')); loi_tho = R['uoc_loi_T3_giay']; loi = round(loi_tho * HS, 1); phim = round(BANG + max(0, loi - LOI25), 1)
    out[g] = dict(tu_dung_medium=R['tu_dung']['medium.en'], tu_dung_small=R['tu_dung']['small.en'], so_sai=R['so_thieu'], so_nghi=R['so_nghi'],
                  ten_sai=R['ten_thieu'], ten_nghi=R['ten_nghi'], tu_giay=R['tu_giay'], tu_giay_doan=[d['tu_giay'] for d in R['doan']],
                  uoc_loi_T3_tho=loi_tho, he_so_hieu_chinh=round(HS, 4), uoc_loi_T3=loi, uoc_phim_T3=phim, lech_tran_pct=round((phim - TRAN) / TRAN * 100, 1),
                  speed_can=round(max(1.0, loi / LOI25), 3), f0=R['f0'], I=v['I'], TP=v['TP'], LRA=v['LRA'], giay=v['giay'], mb=v['mb'], sha256=v['sha256'],
                  tep=f'reports/casting-my/nghe-mu/{g}.mp3',
                  lech_asr={n: [(d['doan'], c) for d in R['doan'] for c in d['nghe'][n]['cho_lech']] for n in R['nghe']})
json.dump(dict(ghi='Theo mã mù M. Không có tên/nguồn giọng. Nghe gói mù TRƯỚC khi đọc.', G=out), open(f'{H}/may-kiem.json', 'w'), ensure_ascii=False, indent=1)
for g, r in out.items():
    print(g, r['tu_dung_medium'], r['tu_dung_small'], 'so', r['so_sai'], r['so_nghi'], 'ten', r['ten_sai'], r['ten_nghi'], 'wps', r['tu_giay'], r['tu_giay_doan'],
          'loi', r['uoc_loi_T3_tho'], r['uoc_loi_T3'], 'phim', r['uoc_phim_T3'], r['lech_tran_pct'], 'speed', r['speed_can'], 'f0', r['f0'], r['I'], r['TP'], r['LRA'], r['giay'], r['mb'])
    for n, l in r['lech_asr'].items(): print('   ', n, l)
