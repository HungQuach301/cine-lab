#!/opt/cine/bin/python
"""CASTING-MỸ · đoạn thử: CHỈ 2 đoạn của lời khoá (móc 0a–0e, pin nổi 2k–2n), lấy nguyên từ casting-giong/doan-thu.json
(đã kiểm nguyên văn với loi-khoa.txt SHA 0fdc72ce…), áp alias đã sửa theo Đ3 casting (chữ thường). Trong 2 đoạn này chỉ d'Arçon có mặt
(dar-SOHN → dar-sohn); Elliot / fet ah-kom-plee / la lee-nay-ah / mon-tair-oh không xuất hiện. Ghi doan-thu.json."""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
G = json.load(open(os.path.join(os.path.dirname(H), 'casting-giong/doan-thu.json')))['doan'][:2]
D3 = [('Eliott', 'Elliot'), ('fait accompli', 'fet ah-kom-plee'), ('La Línea', 'la lee-nay-ah'), ('Montero', 'mon-tair-oh'), ("d'Arçon", 'dar-sohn')]
CU = {"d'Arçon": 'dar-SOHN'}   # alias cũ trong chữ gửi casting-giong
out = []
for d in G:
    gui = d['gui']; ap = []
    for viet, moi in D3:
        if viet in d['khoa']:
            assert CU[viet] in gui; gui = gui.replace(CU[viet], moi); ap.append(f'{viet} → {moi}')
    out.append(dict(d, gui=gui, alias_D3=ap))
json.dump(dict(nguon='casting-giong/doan-thu.json đoạn 1–2 (lời khoá SHA 0fdc72ce…) + alias Đ3', doan=out,
               ky_tu_khoa=sum(len(o['khoa']) for o in out), ky_tu_gui=sum(len(o['gui']) for o in out)), open(f'{H}/doan-thu.json', 'w'), ensure_ascii=False, indent=1)
for o in out: print(o['doan'], len(o['gui']), o['alias_D3'])
