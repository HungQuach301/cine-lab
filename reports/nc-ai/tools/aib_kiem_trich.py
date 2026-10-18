"""NC-AI · kiểm máy câu trích AI-B: câu trích có nằm NGUYÊN VĂN trong trang được ghi không (trang cắt từ tệp có đúng SHA).
Chuẩn hoá hai phía như verify_quotes.py của TIEN-KY: gộp khoảng trắng, nối gạch nối cuối dòng; KHÔNG sửa lỗi OCR.
Kết quả: nguyen_khoi (khớp nguyên) | sai_trang (có ở trang khác) | gan_dung (≥ 0,90 theo SequenceMatcher trên cửa sổ trượt) | khong_thay.
Dùng: python3 -I aib_kiem_trich.py <luot.json> <thu_muc_trang> <ra.json>"""
import sys, os, re, json, glob, difflib
lj, pdir, out = sys.argv[1:4]
def norm(s): s = re.sub(r'-\s*\n\s*', '', s); return re.sub(r'\s+', ' ', s).strip()
P = {os.path.basename(p)[:-4]: norm(open(p).read()) for p in glob.glob(os.path.join(pdir, '*.txt'))}
def best(q, t):
    n = len(q); b = 0.0
    for i in range(0, max(1, len(t) - n + 1), max(1, n // 8)):
        r = difflib.SequenceMatcher(None, q, t[i:i + n + n // 10], autojunk=False).ratio(); b = max(b, r)
    return b
items = json.load(open(lj))['items']; res = []
for k, it in enumerate(items):
    q = norm(it['quote']); pg = it['page']
    if pg in P and q in P[pg]: v, sc = 'nguyen_khoi', 1.0
    elif any(q in t for t in P.values()): v, sc = 'sai_trang', 1.0
    else:
        sc = best(q, P.get(pg, '')); v = 'gan_dung' if sc >= 0.90 else 'khong_thay'
    res.append({'i': k, 'page': pg, 'ket_qua': v, 'diem': round(sc, 3), 'quote': it['quote'][:160]})
from collections import Counter
c = Counter(r['ket_qua'] for r in res)
json.dump({'tong': len(res), 'dem': c, 'muc': res}, open(out, 'w'), ensure_ascii=False, indent=1)
print(dict(c)); [print(r) for r in res if r['ket_qua'] != 'nguyen_khoi']
