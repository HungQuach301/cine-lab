#!/usr/bin/env python3
# P-2610c: sửa docs/BIBLE-KENH2.md theo PHIẾU-A (D-A1…D-A9). Chỉ chèn dòng sau mốc (mỗi mốc đúng 1 lần) + sửa dòng đầu.
# Dùng: /opt/cine/bin/python -I reports/p2610c/sua_bible.py docs/BIBLE-KENH2.md
import sys

p = sys.argv[1]
L = open(p, encoding="utf-8").read().split("\n")

A = "(duyệt 26/10/2026 10:08 — giờ chủ dự án dán lệnh P-2610c sau khi trả lời \"Duyệt PHIẾU-A theo khuyến nghị điều phối\"; `reports/ban-cuoi-t4-a/PHIEU-A.md`"


def a(x):
    return A + "; " + x + ")"


CHEN = [
    ("- LOOK-T4-9 cập nhật 26/10/2026 00:12 (P-2610b)",
     "- LOOK-T4-9 cập nhật 26/10/2026 10:08 (P-2610c) " + a("D-A3, D-A8") + ": (1) **Điểm đứng P1: giữ điểm hiện tại + C6 4°; không dời, không xoay riêng M03.** Lượt thử (c) ở cập nhật 00:12 đã làm (`reports/ban-cuoi-t4-a/BAN-CUOI-T4-A-BAO-CAO.md` §2, `p1/to-p1.jpg`): dời tây 80 m chỉ đưa mái vòm lên 26,2 % (60 m: 24,2 %; hiện tại 18,2 %) mà điểm lửa M03 sát mép phải tăng 7,85 → 31,74 % — **câu \"giữ điểm đứng\" của LOOK-T4-9 có hiệu lực lại**; tham số P1 không đổi, không dựng lại 16 shot P1. (2) **Mở lạnh M00** dùng điểm **P1b** (Bankside đông 125 m, cú VONG — thấy toàn vòng lửa + cầu London có nhà; khác M03; `reports/ban-cuoi-t4-a/m00/M00-moi-a.jpg`) (Q-A3 = (a)), **kèm sửa trước khi dựng 1080p:** mặt sông đêm không được phẳng màu cát; lửa không thành cụm bông (D-A4 (iii))."),
    ("- (k) cập nhật 26/10/2026 (P-2610b):",
     "- (k) cập nhật 26/10/2026 10:08 (P-2610c) " + a("D-A1, D-A2") + ": **điều kiện (2) đã thử** — `reports/ban-cuoi-t4-a/BAN-CUOI-T4-A-BAO-CAO.md` §1 (P9-2026 ngày, P1-2026 ngày lượt 2: 0 Chặn ở mặt nạ \"đủ\"; P9-2026 đêm TRƯỢT (g)). (1) **E dùng ở H5-05a** (P9 CODINH 6 s), tấm E P9-2026 ngày, **mặt nạ \"tháp\"** (toà có tên đỉnh ≥ 75 m ODN + Guildhall, Royal Exchange, Bank of England, Mansion House, Tower of St Mary Somerset giữ 3D; toà có tên thấp coi là nhà thường) **+ ngoại lệ \"bờ\"** (mô hình báo \"bờ\" 2 Chặn — khiếu nại KN-1) — **chờ K-1.17.9 xác nhận** (KN-1, KN-5); **K bác → dùng mặt nạ \"đủ\"** (mọi toà OSM có tên giữ 3D). (2) **Tấm E-P1 chưa dùng** — chờ K xét KN-8 (nước) và KN-6 (đẩy 2D trên tấm E). (3) **H5-04 giữ D 3D + clip Omni H5-04c** (không dùng đuôi E-P1). (4) **Đêm 2026 (H5-07a) giữ 3D** theo câu \"đêm 2026 trượt thì giữ 3D\" ở trên. (5) Trước khi dựng E thật và cảnh 2026: nâng vật liệu 3D **mái vòm St Paul's + toà tháp có tên + đèn pha đêm** (Q-A4 = (a); D-A4 (iv))."),
    ("**(c) cập nhật 26/10/2026 00:12 — ảnh/footage thật T4 ở bản cuối**",
     "\n**(d) Niên đại công trình mốc T4 — luật dựng** (P-2610c) " + a("D-A4 (i)") + ":\n"
     "- **St Paul's mới (Wren):** khởi công **1675**; **vỏ vòm + đèn lồng xong 1708**; nhà thờ **hoàn tất 1711**. Trước 1675: chưa có nhà thờ mới; 1675–1708: công trường, **chưa có mái vòm hoàn chỉnh**; từ 1708: có vỏ vòm + đèn lồng.\n"
     "- **Monument:** xây **1671–1677**; thân cột **có rãnh dọc** (không trơn). Trước 1671: không có cột; 1671–1677: đang xây.\n"
     "- **Luật:** mọi shot có **năm biên** (năm đầu hoặc năm cuối của shot, kể cả ảnh đầu M-d dựng từ render 3D cùng năm) chạm giai đoạn xây của một công trình mốc ở trên **phải soi khung 3D ở chính năm biên trước khi dựng 1080p**: công trình có/không có, đúng giai đoạn, đúng hình (mái vòm, đèn lồng, rãnh cột). Ghi kết quả soi (khung + năm) vào báo cáo phiên dựng.\n"
     "- **Căn cứ:** mẫu 1080p **H2-10** (năm ≈ 1709,5) **không có mái vòm** trong khi vai shot là \"đèn lồng hoàn tất — mái vòm anh hùng\" — tự soi của phiên BAN-CUOI-T4-A không bắt (điều phối bắt); ảnh đầu M-d kế thừa lỗi niên đại của 3D (Monument 1675 trơn ở H2-06b/H2-09x). Phiên B sửa trong 3D trước khi dựng (D-A4 (i)); MAY-19 sửa máy H2-10, H5-05b (D-A4 (v)); cảnh 1960s–70s lọc năm toà OSM theo năm xây rồi thử lại H5-02b/H5-02s ≤ 2 lượt (Q-A5 = (a); D-A4 (vi))."),
]

for moc, dong in CHEN:
    idx = [i for i, s in enumerate(L) if s.startswith(moc)]
    assert len(idx) == 1, (moc, idx)
    j = idx[0] + 1
    if moc.startswith("**(c) cập nhật 26/10/2026 00:12"):
        # chèn khối (d) sau đoạn (c) 00:12, trước dòng trống + "Phạm vi…"
        assert L[j] == "" and L[j + 1].startswith("**Phạm vi và quan hệ với luật cũ"), L[j:j + 2]
    L.insert(j, dong)

cu = "(duyệt 26/10/2026 00:12) (P-2610b) — 26/10/2026)"
assert L[0].endswith(cu)
L[0] = L[0][:-1] + "; sửa §14.7 LOOK-T4-9, §15 (k), thêm §19 (d) niên đại công trình mốc T4 theo PHIẾU-A D-A1…D-A9 (duyệt 26/10/2026 10:08) (P-2610c) — 26/10/2026)"

open(p, "w", encoding="utf-8").write("\n".join(L))
print("xong", len(CHEN), "chỗ chèn + dòng đầu")
