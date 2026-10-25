"""P-2610: sửa docs/BIBLE-KENH2.md theo K1177-D1…D7 (25/10/2026 11:58) và hướng phần hiện đại A+B+E (26/10/2026 00:07).
Dẫn RULES-LL 1.17.7 (LOCK 1.17.7 3a53574c…), không chép luật. Chạy một lần: /opt/cine/bin/python reports/p2610/sua_bible.py"""
P = 'docs/BIBLE-KENH2.md'
s = open(P, encoding='utf-8').read()
R = '`checks/ll/RULES-LL.md` mục 1.17.7 (LOCK 1.17.7 `3a53574c…`; Kinh thánh không chép luật)'
D1 = '(duyệt 25/10/2026 11:58, "Duyệt “K1177-D1…D7 theo khuyến nghị”"'
E = '(duyệt 26/10/2026 00:07, "Chọn hướng cho cảnh hiện đại: A+B+E (khuyến nghị)"; câu hỏi 26/10/2026 00:02 "Liệu A+B có tạo ra sản phẩm tốt hơn hẳn")'


def thay(cu, moi, n=1):
    global s
    assert s.count(cu) == n, (cu[:80], s.count(cu))
    s = s.replace(cu, moi)


def sau(moc, them):
    """chèn dòng `them` ngay sau dòng chứa `moc` (moc phải duy nhất)."""
    global s
    assert s.count(moc) == 1, (moc[:80], s.count(moc))
    i = s.index(moc); j = s.index('\n', i)
    s = s[:j + 1] + them + '\n' + s[j + 1:]


# 0. dòng đầu
thay(' (P-2510b) — 25/10/2026)\n',
     ' (P-2510b) — 25/10/2026; sửa §13 (hàng kiểm), §14.7 LOOK-T4-8, §15 (d)(f)(j), thêm §15 (k), sửa §17, §19 theo K1177-D1…D7 (duyệt 25/10/2026 11:58) và hướng phần hiện đại A+B+E (duyệt 26/10/2026 00:07) (P-2610) — 26/10/2026)\n')

# 1. luật 1.17.7 đã khoá: thay 3 chỗ "đang làm"
thay('`checks/ll/RULES-LL.md` mục 1.17.7 (đang làm — phiên K-1.17.7; tới khi LOCK 1.17.7 khoá, bộ kiểm hiện hành là 1.17.6 `513c9442…`; Kinh thánh không chép luật)',
     R + ' ' + D1 + ', D1 = A)', n=3)

# 2. §13 hàng kiểm mới từ T4
sau('- Hàng kiểm mới từ T4: MAY-19 (§19 a)',
    '- Hàng kiểm theo 1.17.7 (từ T4): **GOC-CAO** thay GOC-CAO-60 (§15 (d)); mới **TU-LIEU-THAT** (§19 (c)), **NHAN-VAT-TEN** (§15 (f)), **KIEM-2-MUC** (§15 (d) (3)); đổi K-LAI-1 (không tính M-d, theo Q2/C11), TL-1 (mục tiêu theo tập; (c) miễn ranh M-d/tư liệu), TU-LIEU-10 (trần theo tập ≤ 20 % + lớp THAT), MAY-19 (hệ toạ độ log, `diem_neo_en`, khung gần nhất), Q37 (a) (`p.lop_chong`), BE-MAT-NHA (d) (sàn Y nhấp nháy theo tập), q_thoi_dai lớp công trình mốc. Định nghĩa, trường đọc, ngưỡng và cách khai: ' + R + ' ' + D1 + ', D1 = A).')

# 3. §14.7 LOOK-T4-8 — ngoại lệ E cho góc rộng 2026
sau('- LOOK-T4-8 Toàn cảnh ở bản cuối:',
    '- LOOK-T4-8 cập nhật 26/10/2026 00:07 (P-2610): câu "không dùng vân nướng AI (D2) ở toàn cảnh" có **một ngoại lệ có điều kiện** — góc rộng năm 2026 máy cố định được dùng ảnh nền AI toàn khung theo §15 (k) (E); chỉ khi đủ điều kiện ở §15 (k); tới lúc đó và với mọi toàn cảnh khác giữ D 3D như trên ' + E + '.')

# 4. §15 (d) — K1177-D2
sau('- (d) cập nhật 25/10/2026 09:15 — gói "50 % tiết kiệm"',
    '- (d) cập nhật 25/10/2026 11:58 — luật 1.17.7 (P-2610) ' + D1 + '): (1) **5 chốt cấu trúc góc cao** ở (d) cập nhật 25/10 09:15 mục (1) là mức **Chặn G2** khi tập khai sàn 50 % (ở animatic chỉ Cảnh báo) (D2 = A) — bản dựng sửa bằng cách chèn 3D góc cao ở mở/kết chương và xen 3D trong chuỗi M-d/thấp liền nhau. (2) Kiểm 2 mức (mục (3)) đo bằng hàng KIEM-2-MUC; K-LAI-1 từ T4 không tính đoạn M-d (tính ở MINH-HOA/N2P-6, tổng AI ≤ 70 %; ai_image ngoài M-d vẫn ≤ 20 %) theo C11 (duyệt 25/10/2026 06:56). Luật kiểm: ' + R + '.')

# 5. §15 (f) — K1177-D3, D4
sau('- (f) nới hẹp từ T4 — nhân vật lịch sử có tên',
    '- (f) cập nhật 25/10/2026 11:58 (P-2610) ' + D1 + '): (1) **"không cận mặt" đo bằng máy:** mặt lớn nhất của nhân vật có tên (bộ dò YuNet) **≤ 1/8 chiều cao khung**; clip có nhân vật có tên khai chân dung tham chiếu (tệp + SHA) và dòng AUTHORSHIP chủ dự án duyệt, kiểm mức ĐỦ (hàng NHAN-VAT-TEN) (D3 = A). (2) **Lớp công trình mốc:** đoạn M-d có công trình có tên **hoặc thấy chân trời City** bắt buộc qua lớp công trình mốc của q_thoi_dai (danh sách công trình mốc theo năm); phía dựng khai `cong_trinh_moc` và khai `chan_troi_city` cho **mọi** đoạn M-d thấy chân trời City (hàng KIEM-2-MUC (d)) (D4 = A + khai chân trời City). Luật kiểm: ' + R + '.')

# 6. §15 (j) — K1177-D6 + E
sau('- (j) cập nhật sau THU-B-T4 + K-1.17.6 (P-2510)',
    '- (j) cập nhật 25/10/2026 11:58 và 26/10/2026 00:07 (P-2610): (1) sàn Y cho thước nhấp nháy BE-MAT-NHA **theo tập** (mặc định 0; **T4 khai `be_mat_nha_y_san_nhap: 0.01`**) — ' + R + ' ' + D1 + ', D6 = A). (2) Phần hiện đại T4 mở thêm **ảnh nền AI toàn khung** cho góc rộng 2026 máy cố định (AI vẽ lại cả nhà thường, không chỉ phủ bề mặt) — phạm vi, điều kiện và ngưỡng BE-MAT-NHA px/m riêng cho cảnh năm ≥ 2020 ở §15 (k); ngoài phạm vi (k), (j) giữ như các dòng trên ' + E + '.')

# 7. §15 (k) mới — phần hiện đại
sau('- (j) cập nhật 25/10/2026 11:58 và 26/10/2026 00:07 (P-2610)',
    '- (k) **Phần hiện đại T4 (≈ 1946–2026) ở bản cuối — hướng A+B+E** (P-2610) ' + E + ': (A) **thay ≈ 30–40 s cảnh 3D trung/cận hiện đại yếu bằng Omni (M-d)**; công trình có tên ở nền qua lớp công trình mốc ((f) cập nhật 25/10 11:58 mục (2)), kiểm mức ĐỦ; trần Gemini T4 giữ $55, mốc $50 ((d) cập nhật 25/10 09:15 mục (2)). (B) **ảnh thật hiện đại CC BY hoặc PD** (vd Barbican đang xây, St Paul\'s thập niên 1950, cụm tháp) — lớp THAT, theo §19 (c) cập nhật 25/10 09:15 (không share-alike, không NC/ND, bằng chứng ở `licenses/` trước khi lên hình), tính vào trần ≤ 20 %. (E) **ảnh nền AI TOÀN KHUNG cho góc rộng năm 2026, máy cố định** (CODINH): AI vẽ lại cả nhà thường; **sông, đường bờ, mái vòm St Paul\'s và toà tháp có tên ghép lại từ render 3D (lớp (a))** theo (a)–(c); ngưỡng BE-MAT-NHA px/m **nới riêng cho cảnh năm ≥ 2020** — định nghĩa và luật kiểm do phiên K-1.17.8. **Điều kiện áp E:** (1) K-1.17.8 khoá luật E (LOCK mới, Kinh thánh dẫn mục RULES-LL tương ứng, không chép luật); (2) **làm thử 2 khung trước khi dựng hết**, 2 khung thử đạt bộ kiểm đó. Thiếu một trong hai điều kiện → góc rộng 2026 giữ D 3D (LOOK-T4-8). **Đêm 2026 trượt thì giữ 3D.** Footage trả phí (C) **không làm**. **Ghi chú:** AI có thể vẽ sai vị trí nhà thường ở cảnh 2026 — **chấp nhận theo chủ dự án 25/10/2026 09:08** ("Người xem cũng không phải là người chuyên về khảo cổ hay gì để có thể nhận ra những dự khác biệt nhỏ trong những frame hình ngắn"); **lớp dữ kiện (a) vẫn chặt** (0/255, 0 vật (a) thêm/bớt/đổi, cấm đổi loại vùng).')

# 8. §17 — K1177-D5
sau('- (3) Thẻ nhân vật (chân dung PD + tên + năm, ≤ 5 s)',
    '- (4) cập nhật 25/10/2026 11:58 (P-2610) ' + D1 + ', D5 = A): mọi lớp chồng (thẻ nhân vật, bộ đếm, tư liệu) **ghi vào đặc tả shot `p.lop_chong`**; trình ghép đọc từ đặc tả (một nguồn sự thật), không tự đặt mốc ngoài đặc tả. Luật kiểm (Q37 (a)): ' + R + '.')

# 9. §19 — K1177-D7
sau('**(c) cập nhật 25/10/2026 09:15 — T4 tư liệu + ảnh/footage thật**',
    '\n**(a)/(c) cập nhật 25/10/2026 11:58 — nhịp cắt và lớp THAT** (P-2610) ' + D1 + ', D7 = A; P9): TL-1 (c) từ T4 **miễn một cắt ở mỗi ranh vào/ra đoạn M-d và tư liệu/ảnh thật** (±0,5 s); TL-1 vẫn chỉ Cảnh báo — nhịp cắt thật của phim do chủ dự án xem ở phiếu xem. Lớp THAT (mục (2)–(5) ở trên) kiểm bằng hàng TU-LIEU-THAT; trần (1) bằng TU-LIEU-10 với `tu_lieu_tran_pct: 20`. Luật kiểm: ' + R + '.')

open(P, 'w', encoding='utf-8').write(s)
print('xong')
