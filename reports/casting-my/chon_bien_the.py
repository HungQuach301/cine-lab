#!/opt/cine/bin/python
"""CASTING-MỸ · chọn 1 biến thể/mô tả bằng máy, chỉ trong biến thể 1–2 (lệnh): (1) tỷ lệ từ đúng cao nhất (thấp hơn của 2 cách nghe);
(2) bằng nhau → F0 trung vị thấp nhất (mục tiêu "trầm"). Ghi thêm từ/giây để tham khảo. Ghi vào thiet-ke.json."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import my_lib as M
K = M.K; P = f'{M.H}/thiet-ke.json'; S = json.load(open(P))
for k, v in S.items():
    for b in v['bien_the']:
        acc = []
        for name, beam in K.NGHE:
            txt, ws = K.transcribe(b['tep'], name, beam); acc.append(K.wer(v['chu_thu'], txt)['tu_dung'])
        b['tu_dung'] = acc; b['f0'] = K.f0(b['tep']); b['tu_giay'] = round(len(v['chu_thu'].split()) / K.speech_span(ws), 3)
        print(k, b['bien_the'], b['xet'], acc, b['f0'], b['tu_giay'], flush=True)
    best = sorted([b for b in v['bien_the'] if b['xet']], key=lambda b: (-min(b['tu_dung']), b['f0'][0]))[0]
    v['chon'] = best['bien_the']; v['ly_do_chon'] = f"từ đúng {min(best['tu_dung'])} (thấp hơn của 2 cách nghe), F0 trung vị {best['f0'][0]} Hz"
json.dump(S, open(P, 'w'), ensure_ascii=False, indent=1)
print({k: v['chon'] for k, v in S.items()})
