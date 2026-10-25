#!/opt/cine/bin/python
"""Cấp Chặn / Cảnh báo của luật 1.12 + 1.12.1 + 1.12.2 (biến thể kênh 2, đề xuất) + 1.13 (NC-H1…H5, hàng đợi khiếu nại T2; đề xuất) + 1.14 (BD-1…BD-8, K-R1…K-R9) + 1.15 (K-LAI-1…6, K-LAI-B, O2, BC2–BC4) + 1.16 (SACH-1…PC-1, K-LAI-3V; chỉ tập từ T3; chủ dự án duyệt K116-D1…D9 19/10 18:48 → 1.16.1) + 1.17 (MINH-HOA, EO-DAT-R1…R3 từ T3; N2P-1…6 từ T4) + 1.17.1 (EO-DAT ngưỡng §14.7, EO-DAT-R4) + 1.17.2 (EO-DAT-R1 chỉ báo mọi cổng — V2-D2; CONG-BO-1 Chặn ở gói phát hành) + 1.17.3 (khiếu nại BAN-CUOI-T3 A1–A6: không đổi cấp hàng nào) + 1.17.4 (BIEN-CO-V; từ T4: MAY-19, BAN-DO-12, TU-LIEU-10, AI-TU-LIEU, GEMINI-NGAN-SACH, GOC-CAO-60) + 1.17.5 (từ T4: BE-MAT-NHA; N2P-1 (d)(e), N2P-3 T9c) + 1.17.6 (từ T4: TU-LIEU-OMNI; TU-LIEU-10 (b)(k); khiếu nại THU-B KN-1…KN-6 không đổi cấp) + 1.17.7 (từ T4: GOC-CAO thay GOC-CAO-60, TU-LIEU-THAT, NHAN-VAT-TEN, KIEM-2-MUC; không đổi cấp hàng cũ) (phiên K, 17–23/10/2026). Cấp = cột "Cấp đề xuất" của reports/K-1.12-BAO-CAO.md §2 (chủ dự án duyệt
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
    # 1.16 (CHỈ tập từ T3) — chủ dự án DUYỆT K116-D1 19/10/2026 18:48 (mức như bảng §3 reports/k116/K116-BAO-CAO.md) + D2/D3/D5 (1.16.1)
    'SACH-1': ('Chặn (a)–(f) (K116-D1; (e) chữ bản đồ Chặn theo K116-D3: ≤ 2 nhãn địa danh ≤ 3 s, không chú giải chữ)', set('abcdefg'), set()),   # 1.17.8: (g) vai §17 (từ T4) — mô tả cấp giữ nguyên chữ (T3 giống hệt)
    'CHUONG-1': ('Chặn (a)–(e) · Cảnh báo (f) vị trí/mờ (K116-D1)', set('abcde'), set('f')),
    'PP-1': ('Chặn (a)–(d) · Cảnh báo (e) tốc độ đọc ≤ 3 từ/s (K116-D1, D8: ≈ 8 s = 7–9 s)', set('abcd'), set('e')),
    'TL-1': ('Cảnh báo (K116-D1; mục tiêu §13.6, hiệu chỉnh sau V7-PILOT)', set(), {'*'}),
    'TL-2': ('Cảnh báo (K116-D1; hiệu chỉnh sau V7-PILOT)', set(), {'*'}),
    'TL-3': ('Cảnh báo (K116-D1; hiệu chỉnh sau V7-PILOT)', set(), {'*'}),
    'NHIP-NGHIA': ('Chặn (K116-D1; §13.2)', {'*'}, set()),
    'XEM-CAM': ('Chặn (K116-D1, D2; §13.4 bắt buộc từ T3)', {'*'}, set()),
    'PC-1': ('Cảnh báo (K116-D1; thước tạm, hiệu chuẩn trên ≥ 10 ảnh)', set(), {'*'}),
    'K-LAI-3V': ('Chặn ở cổng G2 (bản phát hành) · Cảnh báo ở animatic (K116-D5)', {'*'}, set()),
    # 1.17 (phiên K-1.17, 21/10/2026; mức theo lệnh K-1.17: MINH HOẠ + EO-DAT "Chặn ở G2, Cảnh báo ở animatic"; N2P cùng sơ đồ cổng — K đề xuất, chờ duyệt)
    'MINH-HOA': ('Chặn ở G2 · Cảnh báo ở animatic (lệnh K-1.17; §14.1 (c) N2 / §15 M-d)', {'*'}, set()),
    'EO-DAT-R1': ('Chỉ báo ở mọi cổng — chủ dự án chấm bằng mắt (1.17.2, V2-D2 duyệt 22/10 11:09); in pixel thô + vùng nở 1,5 % bề ngang (§14.7 R1 "≥ 15–20 %")', set(), {'*'}),
    'EO-DAT-R2': ('Chặn ở G2 · Cảnh báo ở animatic (§14.7 R2: trống > 50 % ≤ 6 s liên tục, ≤ 10 % thời lượng chương)', {'*'}, set()),
    'EO-DAT-R3': ('Chặn ở G2 · Cảnh báo ở animatic (lệnh K-1.17; §14.7 R3)', {'*'}, set()),
    'EO-DAT-R4': ('Chặn ở G2 · Cảnh báo ở animatic (§14.7 R4 + TL-4; lệnh K-1.17.1)', {'*'}, set()),
    'N2P-1': ('Chặn (a), (b), (d) vòng khớp màu cục bộ, (e) lớp sống ở G2 · Cảnh báo ở animatic · (c) cụm dải 20 px luôn Cảnh báo (người đọc tờ so) — §15 (c)(i); (d)(e) 1.17.5', set('abde'), set('c')),
    'N2P-2': ('Chặn ở G2 · Cảnh báo ở animatic — §15 (c)(ii), K đề xuất', {'*'}, set()),
    'N2P-3': ('Chặn ở G2 · Cảnh báo ở animatic — §15 (c)(iii); 1.17.5: nước→đất = T9c (c) bờ lấn, (d) giữa nước (đối chứng render)', {'*'}, set()),
    'N2P-4': ('Chặn ở G2 · Cảnh báo ở animatic — §15 (c)(iv), K đề xuất', {'*'}, set()),
    'N2P-5': ('Chặn ở G2 · Cảnh báo ở animatic — §15 (b), (c)(v), K đề xuất', {'*'}, set()),
    'N2P-6': ('Chặn ở G2 · Cảnh báo ở animatic — §15 (d) trần, K đề xuất', {'*'}, set()),
    # 1.17.2 (phiên K-1.17.2, 22/10/2026; quyết định chủ dự án 22/10 11:09)
    'CONG-BO-1': ('Chặn ở gói phát hành (`cong: phat_hanh` | `phat_hanh.goi: true`) · chỉ báo (Cảnh báo) ở mọi cổng trước — §14.1 (f), YouTube "AI use"', {'*'}, set()),
    # 1.17.4 (phiên K-1.17.4, 23/10/2026; chủ dự án duyệt Q1–Q7 23/10 21:45; lệnh: "mức Cảnh báo ở animatic, Chặn ở G2 trừ khi ghi khác")
    'BIEN-CO-V': ('Chặn (b), (c), (h) ở G2 khi thước đạt hiệu chuẩn (q_bcv.HIEU_CHUAN + (h) trên tập) · Cảnh báo ở animatic hoặc khi chưa hiệu chuẩn — K117-D8', set('bch'), set()),
    'MAY-19': ('Chặn (a)–(g) ở G2 · Cảnh báo ở animatic · (w) luôn Cảnh báo — §19 (a)', set('abcdefg'), {'w'}),
    'BAN-DO-12': ('Chặn ở G2 · Cảnh báo ở animatic — §19 (b)', {'*'}, set()),
    'TU-LIEU-10': ('Chặn (a) trần theo tập `tu_lieu_tran_pct` (mặc định 10 %, ≤ 15 %), (b) mỗi lần ≤ 10 s, (k) khai sai trần ở G2 · Cảnh báo ở animatic — §19 (c); 1.17.6 (chủ dự án 24/10 12:52)', {'*'}, set()),
    'TU-LIEU-OMNI': ('Chặn (a) tư liệu trùng clip M-d, (b) ghép liền clip M-d (< 1 shot / < 1 s 3D) ở G2 · Cảnh báo ở animatic — 1.17.6 (chủ dự án 24/10 12:52)', {'*'}, set()),
    'AI-TU-LIEU': ('Chặn ở G2 · Cảnh báo ở animatic — §19 (b)(c)', {'*'}, set()),
    'GEMINI-NGAN-SACH': ('Chặn (a) vượt ngân sách, (u) thiếu giá thật ở G2 · Cảnh báo (k) thiếu khai, (m) vượt mốc theo dõi · Cảnh báo ở animatic — Q2 (i)', set('au'), set('km')),
    'GOC-CAO-60': ('Chặn ở G2 · Cảnh báo ở animatic — Q2 (iii)', {'*'}, set()),
    # 1.17.5 (phiên K-1.17.5, 24/10/2026; phương án B, chủ dự án 24/10 06:21; lệnh: "Chặn ở G2, Cảnh báo ở animatic")
    'BE-MAT-NHA': ('Chặn (a)–(e) ở G2 · Cảnh báo ở animatic · (w) mô hình nhìn không năm/hình khối luôn Cảnh báo — phương án B (AI phủ bề mặt nhà thường)', set('abcde'), {'w'}),
    # 1.17.7 (phiên K-1.17.7, 25/10/2026; chủ dự án 25/10 09:15 gói "50 % tiết kiệm" + P1–P10; 06:56 C11, C13; lệnh: "Chặn G2 / Cảnh báo animatic")
    'GOC-CAO': ('Chặn (p) tỉ lệ ≥ goc_cao_min_pct, (a)–(d) 5 chốt cấu trúc, (k) khai sai ở G2 · Cảnh báo ở animatic · (w) luôn Cảnh báo — Q2 (iii) + gói tiết kiệm', set('pabcdk'), {'w'}),
    'TU-LIEU-THAT': ('Chặn (a) THAT có AI, (g) footage hiện đại thiếu giấy phép (tệp + SHA) ở G2 · Cảnh báo ở animatic · (w) luôn Cảnh báo — §19 (c) + gói tiết kiệm', set('ag'), {'w'}),
    'NHAN-VAT-TEN': ('Chặn (a) cận mặt > 1/8 khung, (k) chân dung tham chiếu, (u) thiếu duyệt chủ dự án, (m) không đo được ở G2 · Cảnh báo ở animatic · (w) luôn Cảnh báo — P2 b', set('akum'), {'w'}),
    'KIEM-2-MUC': ('Chặn ở G2 · Cảnh báo ở animatic — kiểm 2 mức day_du / nen (gói tiết kiệm)', {'*'}, set()),
    # 1.17.8 (chủ dự án 26/10 00:07 "A+B+E"): LUẬT E — tấm nền AI toàn khung hiện đại
    'N2P-E': ('Chặn (k) điều kiện, (f) toà có tên có mặt, (g) đêm không chữ/biển/logo AI ở G2 · Cảnh báo ở animatic · (w) toà bịa cao hơn mốc gần / chữ ban ngày luôn Cảnh báo — 1.17.8', set('kfg'), {'w'}),
}
CONG = {'K-LAI-3V', 'MINH-HOA', 'EO-DAT-R2', 'EO-DAT-R3', 'EO-DAT-R4', 'N2P-1', 'N2P-2', 'N2P-3', 'N2P-4', 'N2P-5', 'N2P-6',
        'BIEN-CO-V', 'MAY-19', 'BAN-DO-12', 'TU-LIEU-10', 'AI-TU-LIEU', 'GEMINI-NGAN-SACH', 'GOC-CAO-60', 'BE-MAT-NHA', 'TU-LIEU-OMNI',
        'GOC-CAO', 'TU-LIEU-THAT', 'NHAN-VAT-TEN', 'KIEM-2-MUC', 'N2P-E'}   # cấp theo cổng (r['cong']); 1.17.4 thêm 7 hàng; 1.17.5 +1; 1.17.6 +1; 1.17.7 +4; 1.17.8 +1
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
    if ma in CONG and r.get('cong') == 'animatic': return mo, [], loi + th   # K116-D5 (+ 1.17): animatic (`animatic: true`) chỉ Cảnh báo
    if ma == 'BIEN-CO-V' and not r.get('dat_hieu_chuan'): return mo, [], loi + th   # 1.17.4: thước chưa đạt hiệu chuẩn → chỉ Cảnh báo
    if ma == 'CONG-BO-1' and r.get('cong') != 'phat_hanh': return mo, [], loi + th   # 1.17.2: Chặn chỉ ở gói phát hành
    if '*' in CH: return mo, loi + th, []
    if '*' in CB: return mo, [], loi + th
    ch = [x for x in loi + th if _muc(x, M) in CH]
    cb = [x for x in loi + th if x not in ch]
    return mo, ch, cb
