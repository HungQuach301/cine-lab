#!/opt/cine/bin/python
"""KL42 · bước 2: kiểm 47 mục từ điển (alias Đ3 + GC-C) với G1, v2, speed 1,03, seed 19102026, TRƯỚC khi thu cả tập.
Chữ: bảng 41 mục của GIỌNG-CHỐT (doan.json 'bang' — 40 mục casting + câu 5i "18 October 2026") + 1 câu bổ sung chứa 6 mục GIỌNG-CHỐT kiểm trong móc/pin
(1309, 1782, 1783, 2026, Duc de Crillon, d'Arçon). Hai cách nghe như GIỌNG-CHỐT: M = medium.en beam 5, S = small.en beam 1, không hotwords.
ĐÚNG = đạt cả hai; NGHI = một cách; SAI = cả hai trượt. → kiem47.json; bản nghe $KL_OUT/kiem47.mp3 (+ bản xem trong git phat-am/G1-47-muc-s1.03.mp3)."""
import json, sys
import kl_lib as K
sys.path.insert(0, str(K.R / 'reports/casting-giong')); import kiem_lib as KL   # noqa: E402
B = json.loads((K.R / 'reports/giong-chot/doan.json').read_text())['bang']
BS = "Also in the story: 1309, 1782, 1783 and 2026; the Duc de Crillon; and the French engineer d'Arçon."
khoa = B['khoa'] + ' ' + BS; gui = K.alias(khoa)
MUC = B['muc'] + ['1309', '1782', '1783', '2026', 'Duc de Crillon', "d'Arçon"]
TDM = {d['viet']: d for d in K.TD}
assert set(MUC) == set(TDM) and len(MUC) == 47, sorted(set(TDM) ^ set(MUC))


def ok(item, hyp):
    if TDM[item]['loai'] == 'năm': return KL.num_ok(float(item), hyp)
    if item == '18 October 2026': return KL.num_ok(2026.0, hyp) and (KL.num_ok(18.0, hyp) or 'eighteenth' in hyp.lower())
    return KL.name_ok(item, hyp, TDM[item]['doc']) >= 0.75


if __name__ == '__main__':
    c0 = K.counter(); mp3, al, n = K.tts(gui, 'kiem47'); c1 = K.counter(90 if n else 0)
    if n: print(K.ghi_bodem('kiem47', n, c0, c1))
    out = dict(chu_khoa=khoa, chu_gui=gui, ky_tu=len(gui), tep=mp3, giay=round(K.dur(mp3), 2), nghe={})
    for name, beam in KL.NGHE:
        txt, ws = KL.transcribe(mp3, name, beam)
        out['nghe'][name] = dict(asr=txt, sai=[m for m in MUC if not ok(m, txt)],
                                 diem={m: (1.0 if ok(m, txt) else KL.name_ok(m, txt, TDM[m]['doc'])) for m in MUC if TDM[m]['loai'] != 'năm'})
    s = [set(v['sai']) for v in out['nghe'].values()]
    out['ket_qua'] = dict(sai=sorted(s[0] & s[1]), nghi=sorted((s[0] | s[1]) - (s[0] & s[1])), dung_ca_hai=47 - len(s[0] | s[1]), dat_it_nhat_mot=47 - len(s[0] & s[1]))
    json.dump(out, open(K.H / 'kiem47.json', 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(out['ket_qua'], ensure_ascii=False)); [print(k, v['asr']) for k, v in out['nghe'].items()]
