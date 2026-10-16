#!/opt/cine/bin/python
"""Cấp Chặn / Cảnh báo của luật 1.12 + 1.12.1 (phiên K, 17/10/2026). Cấp = cột "Cấp đề xuất" của reports/K-1.12-BAO-CAO.md §2 (chủ dự án duyệt
HH1) và các luật 1.12.1 (chủ dự án duyệt 16–17/10: HH2, HH3, MM1–MM4, JJ1–JJ2, KK1). Mặc định `k2check.py` vẫn CHỈ BÁO (ghi cấp cạnh kết quả);
`--cap` áp cấp vào mã thoát: hàng có lỗi thuộc phần Chặn → TRƯỢT, chỉ có lỗi phần Cảnh báo → CẢNH BÁO (không tính vào mã thoát).

cap(ma, r) → (chuỗi cấp, [lỗi Chặn], [lỗi Cảnh báo]); THIẾU ở phần Chặn tính là Chặn (không đo được thì không ĐẠT).
"""
import re

# mã → (mô tả cấp, mục Chặn, mục Cảnh báo). Mục = chữ (a)…(f) đầu dòng lỗi hoặc khoá `muc`; '*' = cả luật.
CAP = {
    'ML1': ('Chặn (b), (c) · Cảnh báo (a) ở T3 (Chặn từ T4)', set('bc'), set('a')),
    'ML2': ('Chặn có giải trình (người quyết; không vào mã thoát tự động)', set(), {'*'}),
    'ML3': ('Chặn', {'*'}, set()),
    'FT1': ('Cảnh báo (20 % footage đã Chặn ở Q32 b2)', set(), {'*'}),
    'BC1': ('Cảnh báo', set(), {'*'}),
    'MAU1': ('Chặn bão hoà/colorfulness/cháy · Cảnh báo chi tiết', {'mau'}, {'chi_tiet'}),
    'KHOP1': ('Chặn (a), (b), (d) · (c) Chặn khi đổi trình dựng giữa tập', set('abd') | {'c_doi'}, {'c'}),
    'TL-Q1': ('Chặn (a), (e) · Cảnh báo (b), (c), (d)', set('ae'), set('bcd')),
    'TL-Q2': ('Cảnh báo (1.12.1: AGL theo loại tuyến, HH2)', set(), {'*'}),
    'TL-Q3': ('Chặn', {'*'}, set()),
    'TL-Q4': ('Chặn (a), (c) · Cảnh báo (b)', set('ac'), set('b')),
    'TL-Q5': ('Chặn (a), (b), (f) · Cảnh báo (c), (d), (e)', set('abf'), set('cde')),
    'TL-Q6': ('Chặn', {'*'}, set()),
    'Q35-TL': ('Chặn (như Q35)', {'*'}, set()),
    'TL-Q7': ('Chặn (MM2)', {'*'}, set()),
    'TL-Q8': ('Cảnh báo (MM1)', set(), {'*'}),
    'TL-Q9': ('Cảnh báo (a)–(d) · Chặn (e) tốc độ góc (JJ1/KK1)', {'e'}, set('abcd')),
}
_M = re.compile(r'^\((\w)\)')


def _muc(x, M=None):
    m = _M.match(x)
    if m: return m.group(1)
    for k, v in (M or {}).items():
        if x in (v or []): return k
    return None


def cap(ma, r):
    ma = ma.split(' [')[0]   # 'TL-Q1 [bộ]' khi tập có nhiều bộ timelapse
    mo, CH, CB = CAP.get(ma, ('—', {'*'}, set()))
    loi = list(r.get('loi') or []); th = list(r.get('thieu') or []); M = r.get('muc') or {}
    if ma == 'MAU1':
        ch, cb = [], []
        for x in loi: (cb if all('chi tiết' in y for y in x.split(': ', 1)[-1].split('; ')) else ch).append(x)
        return mo, ch + th, cb
    if ma == 'KHOP1':
        ch = [x for x in loi + th if (_muc(x) or '*') in 'abd*' or (_muc(x) == 'c' and r.get('doi_trinh_dung'))]
        return mo, ch, [x for x in loi if x not in ch]
    if '*' in CH: return mo, loi + th, []
    if '*' in CB: return mo, [], loi + th
    ch = [x for x in loi + th if _muc(x, M) in CH]
    cb = [x for x in loi + th if x not in ch]
    return mo, ch, cb
