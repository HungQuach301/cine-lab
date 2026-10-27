#!/usr/bin/env python3
# P-2710: sửa docs/BIBLE-KENH2.md theo D-B1 + B1-Q1…Q5. Chỉ chèn dòng sau mốc (mỗi mốc đúng 1 lần) + sửa dòng đầu.
# Dùng: /opt/cine/bin/python -I reports/p2710/sua_bible.py docs/BIBLE-KENH2.md
import sys

p = sys.argv[1]
L = open(p, encoding="utf-8").read().split("\n")

Q = ("(duyệt 27/10/2026 07:24 — giờ chủ dự án dán lệnh P-2710 sau khi trả lời \"Duyệt B1-Q1…Q5 theo khuyến nghị điều phối\"; "
     "`reports/ban-cuoi-t4-b1/BAN-CUOI-T4-B1-BAO-CAO.md` §9 + lệnh P-2710")
DB1 = ("(duyệt 26/10/2026 10:42 — giờ chủ dự án dán lệnh BAN-CUOI-T4-B1 (03:41:56Z), nguyên văn \"Đã Duyệt D-B1 bằng cách dán lệnh BAN-CUOI-T4-B1 vào một phiên mới.\"; D-B1)")
B1 = "`reports/ban-cuoi-t4-b1/BAN-CUOI-T4-B1-BAO-CAO.md`"


def q(x):
    return Q + "; " + x + ")"


CHEN = [
    # §14.7 Look T4 — trang dựng hiện hành + LFS D-B1
    ("- LOOK-T4-9 cập nhật 26/10/2026 10:08 (P-2610c)",
     "- LOOK-T4 bản cuối cập nhật 27/10/2026 07:24 (P-2710) — **trang dựng hiện hành và LFS bản dựng trung gian** " + q("ghi kết quả B1 §1–§2") + ": "
     "(1) **Trang dựng hiện hành: `design/k2v/ldn/bc/look3-b1.js`** (cờ d, spp 4, 1920 × 1080, 24 fps) — sinh bằng `scripts/k2ldn/bc/tao_look3_b1.py` = bản sao `thu-b/look3.js` (không sửa) + các chỗ sửa D-A4 (i)–(iv) (lịch xây công trình mốc §19 (d), thuyền/sà lan có boong, nước đêm + lửa M00, quầng lửa giảm khi cách máy < 320 m, đá Portland + mái chì St Paul's, kính rèm từng toà, đèn pha + cửa sổ đêm từ 1951); hình học `scripts/k2ldn/bc/hinh_hoc_b1.py` (= THU-B d + niên đại toà §19 (d)). Mọi shot 1080p còn lại của bản cuối T4 (B2a, B2b, B3) dựng bằng trang + hình học này; `look3` (THU-B) chỉ còn làm đối chứng \"trước\". "
     "(2) **LFS bản dựng trung gian (D-B1)** " + DB1 + ": bản dựng 1080p từng shot (H.264 High, CRF 16, yuv420p, không âm, **chưa LUT, chưa lớp chồng**) vào LFS theo mẫu **`channel-k2/k2c-t4-02/ban-cuoi/dung/*-1080p.mp4`** (`.gitattributes` + `tools/lfs-allow.txt`, đúng 1 mẫu); SHA256 + số khung ở `ban-cuoi/dung/SHA256SUMS`, log máy `ban-cuoi/dung/log-may/`; `git lfs push` trước `git push` sau MỖI shot, kiểm `git lfs ls-files` trước khi báo xong. Đây là ngoại lệ có duyệt cho câu \"chỉ master phát hành vào LFS\" (§11.6, §12.5) — chỉ cho mẫu trên. B1: 27 tệp, 4 818 khung (+ 317 khung dựng lại H1-13a/c), ≈ 1,03 GB."),
    # §14.7 — B1-Q1, Q2, Q4, Q5 (ngay sau dòng vừa chèn: chèn sau mốc riêng ở bước 2)
    ("- LOOK-T4 bản cuối cập nhật 27/10/2026 07:24 (P-2710) — **trang dựng hiện hành",
     "- LOOK-T4 bản cuối cập nhật 27/10/2026 07:24 (P-2710) — **B1-Q1, Q2, Q4, Q5** " + q("B1-Q1, B1-Q2, B1-Q4, B1-Q5") + ": "
     "(1) **B1-Q1 (GOC-CAO):** nâng máy **mở chương M00 (P1b)** và **H1-01h** lên **≈ 160 m** để GOC-CAO nhận là góc cao (log máy B1: H1-01h 120 m, M00 125 → 112 m → GOC-CAO (a) 2; bản sao thử 160 m: ĐẠT, 0 cảnh báo). **H1-01h dựng lại 72 khung ở B2a; M00 dựng ở B2a với máy nâng**, giữ hướng nhìn, cú VONG và giờ của khung P1b đã duyệt (D-A8; LOOK-T4-9 cập nhật 10:08 (2)). "
     "(2) **B1-Q2 (chia phiên):** phần dựng còn lại chia **B2a** = MÓC + H2-00…H2-05; **B2b** = H2-05s…H2-14 + HỒI 4 + sửa H3-03 (mục (3)); **B3** = HỒI 5 + tấm E H5-05a + B + Omni 720p + âm + ghép + xuất + G2; **mỗi phiên ≤ 12 h máy** (ước bằng thông lượng đo 11,6 s/khung, P = 2 — B1 §4; shot đêm/lửa nặng hơn TB). "
     "(3) **B1-Q4 (H3-03, 1860–1871, nhìn xuống):** ≈ 1/2 khung là nền đường xám không nhà ở Southwark/Westminster (thiếu khối thời kỳ ngoài lõi City, có từ hình học look2) → **B2b lấp khối nhà thời kỳ cho vùng ngoài City trong khung** (từ nền OSM; chiều cao/màu nhà Victoria; **không công trình có tên mới**; ghi \"ước lượng\" như LOOK-T4-6) rồi **dựng lại H3-03 (227 khung)**; không đạt → chuyển H3-03 thành **lớp MAP3D cả shot** (kiểu bản đồ có chủ ý; tính vào trần bản đồ §19 (b)). "
     "(4) **B1-Q5 (độ sáng/tông):** H1-01h/H1-02h (đêm 1666, độ sáng TB ≈ 15/255) và H1-13a/H1-13c (lửa ngày tầm phố, quầng sáng mạnh) **chấp nhận ở bản dựng**; chỉnh ở khâu màu/ghép B3 (`nang_toi`, tông lửa) — **không dựng lại vì lý do này**; chủ dự án chấm lại khi xem bản xem 1080p (cùng vòng nhịp K1179-D3, §13.6 cập nhật 26/10 13:02)."),
    # §15 (k) — B1-Q3
    ("- (k) cập nhật 26/10/2026 13:02 (P-2610d)",
     "- (k) cập nhật 27/10/2026 07:24 (P-2710) — **H5-02b, H5-02s (B1-Q3)** " + q("B1-Q3") + ": thử lại Omni sau sửa niên đại toà (D-A4 (vi), Q-A5 = (a); ≤ 2 lượt): H5-02b 2 lượt TRƯỢT Flash clip (tháp \"hiện đại\" chân trời; xe khí động học hiện đại), H5-02s lượt 1 ảnh đầu LOẠI, lượt 2 **tầng 2 LOẠI** (" + B1 + " §1 (vi)). → **Cả hai giữ 3D** (niên đại toà đã sửa §19 (d), tháp Barbican đúng năm) **+ ảnh thật H5-02t**; **không thêm lượt Omni**. Bảng shot không đổi (không có BANG-SHOT-v5); phần (A) Omni của hướng A+B+E không gồm hai shot này."),
    # §19 (d) — lịch xây từng phần + niên đại toà hiện đại
    ("- **Căn cứ:** mẫu 1080p **H2-10** (năm ≈ 1709,5) **không có mái vòm**",
     "- **(d) cập nhật 27/10/2026 07:24 (P-2710) — lịch xây từng phần đã dùng ở bản cuối** " + q("ghi kết quả D-A4 (i) đã duyệt 26/10/2026 10:08; " + B1 + " §1 (i)") + ": "
     "**Quy tắc dựng: phần công trình mốc đang xây \"mọc\" bằng MẶT CẮT DÂNG DẦN theo lịch riêng từng phần — không bóp dẹt cả khối từ mặt đất** (lỗi cũ của look3: mọi phần lớp 5 mọc 1,5 năm bằng bóp dẹt → vỏ vòm mã 1708,5 mới 74 % ở 1709,5, nằm trong trống; bầu Monument xong 1678,4); mã `tl.x` giữ làm mã mặt nạ 2. "
     "**Lịch (trang `bc/look3-b1.js`):** St Paul's thân/hợp xướng/cánh ngang 1675,5 → 1697; trống + hàng cột + gác 1697 → 1705; mặt tây + 2 tháp tây 1702 → 1708; **vỏ vòm chì 1707,3 → 1708,0** (lần đầu đặt 1705 → 1708 thì H2-09 1707,86 vẫn đọc \"vòm hoàn chỉnh\" → dời); **đèn lồng + quả cầu + thập giá 1707,95 → 1708,0**. Monument: bệ 1671 → 1672,5; **thân 1672,5 → 1675,5, 20 rãnh dọc đọc được** (sọc sáng/tối theo góc quanh tâm cột); đầu cột + chóp 1675,5 → 1676,5; **bầu lửa 1676,5 → 1677,0**. "
     "**Soi năm biên** (luật (d) ở trên): danh sách lấy từ bảng shot (shot 3D có St Paul's mới/Monument trong 1666–1711), mỗi shot soi khung 1080p ở năm đầu/cuối + các năm mốc 1675 / 1708,0 / 1709,5 / 1711; đo mặt nạ 2 + **q_thoi_dai lớp công trình mốc** (`--lop-moc`, sổ có `usd` từng dòng); \"gần xong\" phải đọc thành \"đang xây\". B1: 24 khung, **20 ĐẠT, 4 ghi** (H2-05s 1670 phế tích tháp nhà thờ hình khối trơn; H2-06 1671,0 Monument mới móng; H2-06 1676,99 thân St Paul's thấp ≈ 2,9 m theo lịch tuyến tính; H3-01 1798 Monument ngoài khung) — phiên dựng sau xét chi tiết phế tích và lịch thân St Paul's nhanh hơn ở đầu khi dựng các shot đó."),
    ("- **(d) cập nhật 27/10/2026 07:24 (P-2710) — lịch xây từng phần",
     "- **(d) cập nhật 27/10/2026 07:24 (P-2710) — niên đại toà hiện đại** " + q("ghi kết quả D-A4 (vi), Q-A5 = (a) đã duyệt 26/10/2026 10:08; " + B1 + " §1 (vi)") + ": "
     "toà OSM **xuất hiện ở năm = năm hoàn thành − 2,5** (lớp 4 mọc 2,5 năm); bảng năm hoàn thành có nguồn trong `scripts/k2ldn/bc/hinh_hoc_b1.py` (Cromwell Tower 1973, Lauderdale Tower 1974, Shakespeare Tower 1976, City Point/Britannic House 1967, London Wall Place 2017, 5 Aldermanbury Square 2007, 20 Ropemaker Street 2021, 6 hội quán phường hội); **Barbican: ba tháp 1973–1976** (toà Barbican Estate thiếu năm: 1965–1976); hành lang London Wall thiếu năm: dựng lại 1985–2020; vùng bom 1940 thiếu năm có năm dựng > 1962 → khối tiền nhiệm hậu chiến 1953–1961 rồi tới năm dựng. **Bỏ luật cũ** ép mọi toà > 120 m về năm ≥ 1995 và năm ngẫu nhiên 1950–2020 cho toà thiếu `start_date`. **Công trình lịch sử có tên (nhà thờ, hội quán phường hội, tên riêng lịch sử) loại trừ khỏi mọi quy tắc gán năm theo vùng** (B1 lần đầu gán nhầm St Giles, St Alban, St Botolph và hội quán). B1: 323 toà đổi năm (`reports/ban-cuoi-t4-b1/sua/nam-toa-b1.json`; tờ `sua/vi-ban-do-nam-toa.jpg`); HỒI 1/HỒI 3 (≤ 1938) không bị ảnh hưởng."),
]

for moc, dong in CHEN:
    idx = [i for i, s in enumerate(L) if s.startswith(moc)]
    assert len(idx) == 1, (moc, idx)
    L.insert(idx[0] + 1, dong)

cu = "(duyệt 26/10/2026 13:02) (P-2610d) — 26/10/2026)"
assert L[0].endswith(cu)
L[0] = L[0][:-1] + "; sửa §14.7 Look T4 (trang dựng hiện hành `bc/look3-b1.js`, LFS bản dựng trung gian D-B1, B1-Q1/Q2/Q4/Q5), §15 (k) (B1-Q3), §19 (d) (lịch xây từng phần, niên đại toà hiện đại) theo D-B1 (duyệt 26/10/2026 10:42) và B1-Q1…Q5 (duyệt 27/10/2026 07:24) (P-2710) — 27/10/2026)"

open(p, "w", encoding="utf-8").write("\n".join(L))
print("xong", len(CHEN), "chỗ chèn + dòng đầu")
