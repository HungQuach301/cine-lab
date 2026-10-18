#!/opt/cine/bin/python
"""Cấp Chặn / Cảnh báo của luật 1.12 + 1.12.1 + 1.12.2 (biến thể kênh 2, đề xuất) + 1.13 (NC-H1…H5, hàng đợi khiếu nại T2; đề xuất) + 1.14 (BD-1…BD-8, K-R1…K-R9) + 1.15 (K-LAI-1…6, K-LAI-B, O2, BC2–BC4) (phiên K, 17–18/10/2026). Cấp = cột "Cấp đề xuất" của reports/K-1.12-BAO-CAO.md §2 (chủ dự án duyệt
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
    # 1.12.2 (đề xuất, chờ chủ dự án duyệt — reports/K-1.12.2-BAO-CAO.md §2)
    'NHIP-K2': ('Chặn (như Q37)', {'*'}, set()),
    'Q26b-K2': ('Chặn (c), (d), (e) (như Q26b) · Cảnh báo (a), (b)', set('cde'), set('ab')),
    'Q33-K2': ('Chặn (như Q33)', {'*'}, set()),
    'Q32b-K2': ('Chặn (như Q32b)', {'*'}, set()),
    # 1.13 (đề xuất, chờ chủ dự án duyệt — reports/K-1.13-BAO-CAO.md §2)
    'NC-H1': ('Chặn (a), (b) (đúng lỗi chủ dự án nêu ở T2)', set('ab'), set()),
    'NC-H2': ('Chặn (a), (b)', set('ab'), set()),
    'NC-H3': ('Cảnh báo', set(), {'*'}),
    'NC-H4': ('Chặn', {'*'}, set()),
    'NC-H5': ('Chặn (a) · Cảnh báo (b)', set('a'), set('b')),
    'Q7/Q8-K2': ('Chặn (thay Q7/Q8 cho kênh 2, như Q35)', {'*'}, set()),
    'Q33 (1.13)': ('Chặn (thay Q33 cho kênh 2)', {'*'}, set()),
    'Q36 (1.13)': ('Chặn (thay Q36 cho kênh 2)', {'*'}, set()),
    'Q37 (1.13)': ('Chặn (thay Q37 cho kênh 2)', {'*'}, set()),
    # 1.14 (chủ dự án duyệt B1–B8 + YY5 17/10; mức theo lệnh phiên K-1.14; đề xuất mức cuối: reports/K-1.14-BAO-CAO.md §5)
    'BD-1': ('Chặn', {'*'}, set()),
    'BD-2': ('Cảnh báo (tới khi hiệu chuẩn trên V5b-2c)', set(), {'*'}),
    'BD-3': ('Chặn (a) · Cảnh báo (c) năm nhãn ≠ năm lớp (K thêm, chờ duyệt)', set('a'), set('c')),
    'BD-4': ('Chặn', {'*'}, set()),
    'BD-5': ('Chặn', {'*'}, set()),
    'BD-6': ('Chặn', {'*'}, set()),
    'BD-7': ('Cảnh báo (tới khi hiệu chuẩn trên V5b-2c)', set(), {'*'}),
    'BD-8': ('Cảnh báo (tới khi hiệu chuẩn trên V5b-2c)', set(), {'*'}),
    'K-R1': ('Chặn (đề xuất; ĐỎ-K)', {'*'}, set()), 'K-R2': ('Chặn (đề xuất; ĐỎ-K)', {'*'}, set()), 'K-R3': ('Chặn (đề xuất; ĐỎ-K)', {'*'}, set()),
    'K-R4': ('Chặn (đề xuất; ĐỎ-K)', {'*'}, set()), 'K-R5': ('Chặn (đề xuất; ĐỎ-K)', {'*'}, set()), 'K-R6': ('Chặn (đề xuất; ĐỎ-K)', {'*'}, set()),
    'K-R7': ('Chặn (đề xuất; ĐỎ-K)', {'*'}, set()), 'K-R8': ('Chặn (đề xuất; ĐỎ-K)', {'*'}, set()), 'K-R9': ('Chặn (đề xuất; ĐỎ-K)', {'*'}, set()),
    # 1.15 (chủ dự án duyệt P2-2 [K-LAI-1…6 Chặn], P2-3 [bão hoà Cảnh báo], O2 [Cảnh báo], I3 [Cảnh báo tới V5b-2c], I8 ngày 18/10)
    'K-LAI-1': ('Chặn (P2-2)', {'*'}, set()), 'K-LAI-2': ('Chặn (P2-2)', {'*'}, set()), 'K-LAI-3': ('Chặn (P2-2)', {'*'}, set()),
    'K-LAI-4': ('Chặn (P2-2)', {'*'}, set()), 'K-LAI-5': ('Chặn (P2-2)', {'*'}, set()), 'K-LAI-6': ('Chặn (P2-2)', {'*'}, set()),
    'K-LAI-B': ('Cảnh báo (P2-3)', set(), {'*'}),
    'O2': ('Cảnh báo (lưới lọc thứ hai — không thay kiểm nguồn)', set(), {'*'}),
    'BC2': ('Cảnh báo (tới khi hiệu chuẩn trên V5b-2c)', set(), {'*'}), 'BC3': ('Cảnh báo (tới khi hiệu chuẩn trên V5b-2c)', set(), {'*'}),
    'BC4': ('Cảnh báo (chỉ báo; tới khi hiệu chuẩn trên V5b-2c)', set(), {'*'}),
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
