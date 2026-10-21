"""NHẠC-T3 · bảng số đo từ JSON của tron.py: SMR theo đoạn (p10/min/trung vị), độ duck, cửa sổ < 15 dB, mức nhạc ở tấm im lặng.
  bang_so.py <thư mục mix> > so-do.json"""
import json, sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../scripts/audio'))
import lib
D = sys.argv[1]
SEC = [('móc 0a–0h', 0, 43.83), ('ch1 ROCK', 43.83, 173.08), ('ch2 2a–2i', 173.08, 262.17), ('ch2 KA1782–2p', 262.17, 288.54), ('ch2 2j–2n', 288.54, 354.96),
       ('ch2 2q–2r', 354.96, 382.58), ('ch3 NEUTRAL', 382.58, 471.62), ('ch4 4a–SM3', 471.62, 549.8), ('ch4 4h–4i', 558.62, 585.83), ('ch5 5a–5i', 585.83, 697.54), ('ch5 5j–5k', 697.54, 761)]
IM = [('KB1943', 549.8, 558.62), ('KA2026', 716.57, 725.0)]
def st(v):
    a = np.array(v); return dict(n=len(a), p10=round(float(np.percentile(a, 10)), 2), min=round(float(a.min()), 2), trung_vi=round(float(np.median(a)), 2)) if len(a) else None
out = {}
for P in 'AB':
    for kieu, f in (('thich_ung', f'full-{P}.json'), ('co_dinh_-12', f'fix-{P}.json')):
        R = json.load(open(os.path.join(D, f))); W = R['cua_so_smr']; Dk = R['duck']['ds']
        rec = dict(tong=R['smr'], dau_ra=R['dau_ra'], duck=dict(trung_vi=R['duck']['trung_vi_db'], sau_nhat=R['duck']['sau_nhat_db'], vuot_co_ban=R['duck']['khoang_vuot_co_ban'], so_khoang=R['duck']['so_khoang']), doan={})
        for n, a, b in SEC:
            rec['doan'][n] = dict(smr=st([v for t, v in W if a <= t < b]), duck_trung_vi=float(np.median([d['duck_db'] for d in Dk if a <= d['t0'] < b] or [0])), duck_sau=min([d['duck_db'] for d in Dk if a <= d['t0'] < b] or [0]))
        rec['duoi_15'] = [(t, v) for t, v in W if v < 15]
        if kieu == 'thich_ung':
            x = lib.dec(os.path.join(D, f'full-{P}.wav'), 2, dtype=np.float32); rec['im_lang'] = {}
            for n, a, b in IM:
                seg = x[int(a * lib.SR):int(b * lib.SR)]; pre = x[int((a - 12) * lib.SR):int((a - 1) * lib.SR)]
                rec['im_lang'][n] = dict(LUFS=round(float(lib.integrated(seg)), 1), LUFS_11s_truoc_co_loi=round(float(lib.integrated(pre)), 1))
            del x
        out[f'{P}_{kieu}'] = rec
json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
