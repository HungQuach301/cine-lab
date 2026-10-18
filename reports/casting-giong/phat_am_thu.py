#!/opt/cine/bin/python
"""CASTING-GIỌNG · bảng phát âm: 40 mục từ điển KHÔNG có trong 3 đoạn thử (7 mục kia nằm trong đoạn thử) → đủ 47/47.
Ghi phat-am-thu.json (chữ khoá + chữ gửi sau alias + danh sách mục)."""
import json, re
from pathlib import Path
H = Path(__file__).resolve().parent; R = H.parents[1]
D = json.loads((R / 'channel-k2/k2c-t3-01/khoa-loi/phat-am/tu-dien.json').read_text())['muc']
dt = json.loads((H / 'doan-thu.json').read_text())
trong_doan = sorted({m for d in dt['doan'] for m in d['muc_tu_dien']})
nam = [d['viet'] for d in D if d['loai'] == 'năm' and d['viet'] not in trong_doan]
khoa = ("Places on the map: La Línea de la Concepción, La Línea, La Línea's harbour, San Roque, Algeciras, Cádiz, Tangier and Utrecht. "
        "People in the story: Admiral Rooke, Diego de Salinas, Prince George of Hesse-Darmstadt, General Eliott, Sergeant Ince's men, and the historian Montero. "
        "A sandy isthmus. A fait accompli. The years: " + ', '.join(nam) + '.')
def alias(t):
    for d in sorted(D, key=lambda x: -len(x['viet'])): t = re.sub(r'(?<![\w-])' + re.escape(d['viet']) + r'(?![\w])', d['doc'], t)
    return t
muc = [d['viet'] for d in D if re.search(r'(?<![\w-])' + re.escape(d['viet']) + r'(?![\w])', khoa)]
assert sorted(set(muc) | set(trong_doan)) == sorted(d['viet'] for d in D), 'chưa đủ 47 mục'
json.dump(dict(khoa=khoa, gui=alias(khoa), muc=muc, muc_trong_doan_thu=trong_doan), open(H / 'phat-am-thu.json', 'w'), ensure_ascii=False, indent=1)
print(len(muc), len(trong_doan), len(khoa), len(alias(khoa))); print(alias(khoa))
