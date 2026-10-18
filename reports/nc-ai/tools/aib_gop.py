"""NC-AI · gộp lượt 1 (gpt-6.1-sol) + kiểm máy + lượt 2 (claude sonnet, kiểm từng mục) + phân xử P → danh sách cuối tháng 9/1782.
Bậc AI-A: mục chữ = bậc 2 (văn bản). Vị trí trên phố KHÔNG lấy từ chữ → cột 'can_bac_1' ghi nơi phải neo bằng bản đồ (Drinkwater 1786 plan, đã nắn ở SH).
Dùng: python3 -I aib_gop.py"""
import json, re
A = json.load(open('aib/luot1-gpt61sol.json'))['items']; K = json.load(open('aib/kiem-trich-luot1.json'))['muc']
B = {b['id']: b for b in json.load(open('aib/luot2B-sonnet-kiem-luot1.json'))}
SHA = {k: v['sha256'] for k, v in json.load(open('aib/bang-trang.json'))['nguon'].items()}
P_DA_XEM = {17, 18, 19, 62, 9, 25}  # P đọc lại trang, đồng ý với lượt 2 ở cả 6
NOI = ['Line Wall', 'Mole', "Willis", 'Europa', 'Landport', 'Waterport', 'Ragged', 'Princes', 'Grand Battery', 'Rosia', 'Red Sands', 'Windmill', 'Lines', 'King', 'Montagu', 'Orange', 'Rock gun', 'rock gun', 'Camp']
rows = []
for i, (a, k) in enumerate(zip(A, K)):
    b = B.get(i, {}); v = b.get('verdict', '?')
    noi = sorted({n for n in NOI if n.lower() in (a['quote'] + a['description_en']).lower()})
    rows.append({'id': i, 'loai': a['category'], 'mo_ta_en': a['description_en'], 'trich_nguyen_van': a['quote'], 'nguon': a['page'].split('-p')[0],
                 'trang': int(a['page'].split('-p')[1]), 'sha256': SHA[a['page'].split('-p')[0]], 'ngay': a['date'], 'kiem_may': k['ket_qua'],
                 'luot2': v, 'luot2_ghi_chu': b.get('note', ''), 'p_doc_lai': i in P_DA_XEM,
                 'dung_duoc': v == 'correct' or v == 'wrong_category', 'bac_AI_A': 2, 'can_bac_1': noi})
json.dump(rows, open('aib/danh-sach-9-1782.json', 'w'), ensure_ascii=False, indent=1)
from collections import Counter
print(Counter(r['luot2'] for r in rows), Counter(r['loai'] for r in rows if r['dung_duoc']), sum(bool(r['can_bac_1']) for r in rows))
L = ['# AI-B (a) — danh sách tháng 9/1782 (Gibraltar, trong thành) — máy sinh từ `danh-sach-9-1782.json`', '',
     'Cột: id · loại · ngày · nguồn tr. · kiểm máy · lượt 2 · trích nguyên văn (OCR giữ nguyên, ≤ 140 ký tự) · nơi cần neo bản đồ (bậc 1). Mọi mục chữ = **bậc 2**. SHA-256 tệp: xem `bang-trang.json`.', '',
     '| id | loại | ngày | nguồn tr. | máy | lượt 2 | trích | neo bậc 1 |', '|---|---|---|---|---|---|---|---|']
for r in rows:
    q = r['trich_nguyen_van'].replace('|', '/')[:140]
    L.append(f"| {r['id']} | {r['loai']} | {r['ngay'] or '—'} | {r['nguon']} {r['trang']} | {r['kiem_may']} | {r['luot2']} | {q} | {', '.join(r['can_bac_1']) or '—'} |")
open('aib/DANH-SACH-9-1782.md', 'w').write('\n'.join(L) + '\n')
