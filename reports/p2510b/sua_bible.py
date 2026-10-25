#!/usr/bin/env python3
"""P-2510b: sửa docs/BIBLE-KENH2.md theo gói "50 % tiết kiệm" + phiếu NC-T4 P1–P10 (chủ dự án 25/10/2026 08:15–09:15).
Mỗi chỗ chèn neo vào một chuỗi gốc phải xuất hiện đúng 1 lần; chỉ thêm dòng, đổi duy nhất dòng tiêu đề.
Dùng: python3 -I reports/p2510b/sua_bible.py docs/BIBLE-KENH2.md"""
import sys

p = sys.argv[1]
s = open(p, encoding="utf-8").read()

R7 = "`checks/ll/RULES-LL.md` mục 1.17.7 (đang làm — phiên K-1.17.7; tới khi LOCK 1.17.7 khoá, bộ kiểm hiện hành là 1.17.6 `513c9442…`; Kinh thánh không chép luật)"
DUYET = "(duyệt 25/10/2026 09:15, \"Duyệt gói 50 % tiết kiệm + P1–P10 theo khuyến nghị\"; căn cứ 08:15, 08:21, 09:08)"

SUA = [
    # tiêu đề
    ("25/10/2026 06:56–07:01 (P-2510) — 25/10/2026)", "thay",
     "25/10/2026 06:56–07:01 (P-2510) — 25/10/2026; sửa §15 (d)(f), §19 (c) theo gói \"50 % tiết kiệm\" + phiếu NC-T4 P1–P10 (duyệt 25/10/2026 09:15) (P-2510b) — 25/10/2026)"),
    # §15 (d) — gói 50 %
    ("animatic giữ V1 (duyệt 24/10/2026 12:29, \"chon A theo khuyến nghị\"). (2) **Ngân sách Gemini T4 $55", "dong-sau-chua",
     "- (d) cập nhật 25/10/2026 09:15 — gói \"50 % tiết kiệm\" (P-2510b) " + DUYET + ": "
     "(1) **Góc cao timelapse T4 ≥ 50 % thân phim** (thay ≥ 60 % ở (d) đầu và (d) cập nhật 24–25/10 mục (3)), kèm **5 chốt cấu trúc**: "
     "(i) mỗi chương mở và kết bằng một shot góc cao; (ii) điểm máy xương sống P1 tái xuất mỗi hồi (§19 (a) luật 3); "
     "(iii) ≤ 2 shot liền nhau thuộc nhóm thấp/cận/M-d/ảnh thật; (iv) mỗi chương ≥ 40 % góc cao; "
     "(v) TL-1 (§19 (a) luật 4): tỉ lệ góc cao **mục tiêu 60 %** cho T4 (đích hướng tới, không phải sàn; sàn luật là 50 % ở (1)). "
     "Phần ≈ 80 s giải phóng (so với sàn 60 %) phân bổ ≈ 25 s ảnh/tư liệu thật + ≈ 15 s 3D tầm phố + ≈ 40 s Omni (M-d). "
     "Lý do của chủ dự án: chi phí là mối lo chính, các mặt khác được nới để tăng chất lượng và độ chân thực; người xem không phải chuyên gia để nhận ra khác biệt nhỏ trong khung ngắn (09:08). "
     "(2) **Ngân sách Gemini T4: trần $55, mốc theo dõi $50** (thay mốc $45 ở (d) cập nhật 24–25/10 mục (2); khai `ngan_sach_gemini_usd: 55`, `ngan_sach_gemini_moc_usd: 50`). "
     "(3) **Kiểm clip M-d 2 mức:** mức ĐỦ cho clip có công trình có tên, nhân vật có tên, chân trời hoặc dữ kiện lớp (a) — bộ kiểm (c) đủ, ≤ 3 lượt sinh/clip; "
     "mức NỀN cho các clip còn lại — kiểm bằng mô hình Flash + soi khung, ≤ 2 lượt sinh/clip, được bỏ qua lỗi nhỏ ở hậu cảnh (lớp chi tiết minh hoạ/lớp nền), "
     "**KHÔNG bỏ qua lỗi lớp dữ kiện (a)** ở bất kỳ mức nào. "
     "(4) **720p:** chỉ sinh lại ở 720p các lệnh đã đạt ở 360p; không dự trữ lượt (bỏ hệ số làm lại 30 % của ước NC-T4). "
     "(5) Một clip M-d được dùng cho tối đa 2 shot (cắt đoạn khác nhau hoặc khung khác nhau). "
     "Định nghĩa, cách đo và tên hàng kiểm (thay GOC-CAO-60, mức kiểm, 2 shot/clip): " + R7 + "."),
    # §15 (f) — nới hẹp P2 (b)
    ("- (g) Lối mòn/đường đất:", "truoc-dong",
     "- (f) nới hẹp từ T4 — nhân vật lịch sử có tên (phiếu NC-T4 P2 = (b)) " + DUYET + ": câu \"không dựng nhân vật lịch sử có tên\" ở (f) trên được nới **hẹp** như sau: "
     "được dựng nhân vật lịch sử có tên trong M-d **chỉ ở khung trung hoặc xa, không cận mặt**; trang phục, tóc giả và dáng theo **chân dung thật làm tham chiếu** "
     "(chân dung có giấy phép trong RIGHTS — mục NC-T4; chỉ lấy trang phục/dáng, không đưa mặt vào lệnh, không làm \"giống mặt\"); "
     "**chủ dự án duyệt từng clip** trước khi clip vào bản dựng; người không có chân dung xác thực (Robert Hooke) **chỉ thẻ chữ**, không dựng trong M-d; "
     "người chưa có chân dung sạch quyền (Bludworth, Barbon, Godfrey Allen, Holden, Holford, Matthews) cũng chỉ thẻ chữ. "
     "Phần còn lại của (f) giữ nguyên (máy tầm người, kẹp giữa hai shot 3D cùng thời điểm, khớp lớp (a), qua bộ kiểm (c) mức ĐỦ — (d) cập nhật 25/10 09:15 mục (3)). "
     "Không cận mặt nhân vật có tên ở mọi trường hợp (phương án (c) không duyệt). Phép kiểm do phiên K thêm: " + R7 + "."),
    # §19 (c) — 20 %
    ("Danh sách cụ thể chờ NC-T4 (N4).", "dong-sau-chua",
     "\n**(c) cập nhật 25/10/2026 09:15 — T4 tư liệu + ảnh/footage thật** (phiếu NC-T4 P6, P7, P8 = (a) sửa 20 %; gói \"50 % tiết kiệm\") " + DUYET + ": "
     "(1) **T4: trần tư liệu + tranh khắc + thẻ + ảnh/footage thật ≤ 20 %** thời lượng (thay 15 % ở (c) ngoại lệ T4 mục (1); khai `tu_lieu_tran_pct: 20`). "
     "(2) Ảnh/footage thật là **lớp THAT**: không tính vào tổng khung có AI, không tính vào góc cao. "
     "(3) **Ảnh thật toàn khung có chuyển động máy** (đẩy/trượt theo giới hạn (c)) là **shot hợp lệ** (không bị coi là khung đứng); ảnh chồng góc khung (≤ 1/3) giữ góc của shot nền. "
     "(4) Lớp THAT **không ghép liền clip Omni (M-d)**, như (c) ngoại lệ T4 mục (2). "
     "(5) **Footage hiện đại chỉ dùng giấy phép không share-alike** (không CC BY-SA, không NC/ND) và **có bằng chứng giấy phép lưu ở `licenses/`** trước khi lên hình; T4 chỉ 1 clip footage đêm (H5-07a, ≈ 6 s; P7); phần còn lại footage chỉ làm tham chiếu bố cục/ánh sáng. "
     "(6) Tư liệu 1940: dùng ảnh MoI Crown đã hết bản quyền, chú thích đúng năm chụp (1941–1944); **LOẠI \"St Paul's Survives\" (Herbert Mason)** và không dựng lại bố cục đó bằng AI; **không dùng phim 1940** (*London Can Take It!*) trong T4 (P6). "
     "Luật kiểm ở " + R7 + "."),
]

for neo, cach, van in SUA:
    n = s.count(neo)
    if n != 1:
        sys.exit(f"NEO KHÔNG DUY NHẤT ({n}): {neo[:70]}")
    i = s.index(neo)
    if cach == "thay":
        s = s.replace(neo, van, 1)
    elif cach == "truoc-dong":
        d = s.rindex("\n", 0, i) + 1
        s = s[:d] + van + "\n" + s[d:]
    elif cach == "dong-sau-chua":
        e = s.index("\n", i)
        s = s[:e + 1] + van + "\n" + s[e + 1:]
open(p, "w", encoding="utf-8").write(s)
print("ĐÃ SỬA", len(SUA), "chỗ")
