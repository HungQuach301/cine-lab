#!/usr/bin/env python3
"""P-2510: sửa docs/BIBLE-KENH2.md theo các quyết định 24/10 12:29 → 25/10 07:01 (lệnh P-2510).
Mỗi chỗ chèn neo vào một chuỗi gốc phải xuất hiện đúng 1 lần; chỉ thêm dòng, đổi duy nhất dòng tiêu đề.
Dùng: python3 -I reports/p2510/sua_bible.py docs/BIBLE-KENH2.md"""
import sys

p = sys.argv[1]
s = open(p, encoding="utf-8").read()

R = "`checks/ll/RULES-LL.md` mục 1.17.6 (LOCK 1.17.6 `513c9442…`; Kinh thánh không chép luật)"

# (neo, vị trí: "thay" | "sau-dong", văn bản)
SUA = [
    # tiêu đề
    ("theo K-1.17.5 (K1175-D1…D7) — 24/10/2026)", "thay",
     "theo K-1.17.5 (K1175-D1…D7) — 24/10/2026; sửa §3, §13.4, §14.6, §14.7 Look T4, §15 (d)(j), §19 (c) theo các quyết định 24/10/2026 12:29–17:54 và 25/10/2026 06:56–07:01 (P-2510) — 25/10/2026)"),
    # §3 thời lượng
    ("- Móc câu ≤ 45 s: tin mới → nghịch lý", "truoc-dong",
     "- T4 (K2C-T4-02 London): thời lượng bản cuối **≤ 13:00** (780 s); animatic hiện 730,1 s (duyệt 25/10/2026 07:01, \"Trả lời N1–N6: theo khuyến nghị\": N3)."),
    # §13.4 XEM CÂM T4
    ("13.4 Cổng XEM CÂM (bắt buộc từ T3)", "sau-dong",
     "\n13.4 bổ sung — T4 London: chủ dự án XEM CÂM animatic T4 (`reports/animatic-t4/PHIEU-XEM.md` mục B) **8/8** — nguyên văn \"có thể hiểu được cả 8\" (≥ 6/8: ĐẠT phần chủ dự án của cổng XEM CÂM T4); XEM CÂM AI tham khảo 7,5/8 mỗi người (duyệt 25/10/2026 06:56)."),
    # §14.6 âm thanh — N6 lời mới
    ("- Master âm thanh phát hành (giọng, nhạc, stem) PHẢI vào LFS kèm SHA.", "sau-dong",
     "- T4 London — lời mới cho các điểm nhấn (NC-T4): tối đa **10 câu**, **≤ 2 000 ký tự** gửi ElevenLabs; mỗi câu qua kiểm nguồn như lời khoá (claims, nguồn, kiểm cấp từ câu trích) trước khi thu; giọng G1 vẫn chờ quyền phát hành (Đ5) (duyệt 25/10/2026 07:01, \"Trả lời N1–N6: theo khuyến nghị\": N6)."),
    # §14.7 Look T4 — LOOK-T4-8, LOOK-T4-9 (C6)
    ("- LOOK-T4-7 Còn mở: \"đồ chơi\" chủ yếu nằm ở mái/tường nhà thường", "sau-dong",
     "- LOOK-T4-8 Toàn cảnh ở bản cuối: **D 3D** (`look3`, cờ d — nâng 3D, không AI lên lớp (a)) cho mọi toàn cảnh (khung D1 M1-rong 1666 và D2 M4-rong 2026 = D 3D); **không dùng vân nướng AI (D2) ở toàn cảnh**; nâng vật liệu 3D các toà 2026 có tên (không AI, giữ hình khối) cho khung mặt phố 2026. Chi tiết phạm vi AI ở §15 (j) cập nhật 24/10 15:25 (duyệt 24/10/2026 15:25, phiếu THU-B \"theo khuyến nghị\": D1, D2, T3 = b, T4 = a).\n"
     "- LOOK-T4-9 (C6) Bản cuối: xoay hướng nhìn P1 **≈ 4° sang trái** để mái vòm St Paul's về ≈ 30 % chiều rộng khung (đang ≈ 18 % ở fov 36°); giữ điểm đứng và fov 36° của LOOK-T4-4; dựng lại các shot P1 (≈ 9 shot); mọi lần P1 tái xuất đọc lại tham số mới (§19 (a) luật 3). Animatic giữ hướng cũ (duyệt 25/10/2026 06:56, \"đồng ý với những nhận định của bạn\": C6 = b)."),
    # §15 (d) cập nhật
    ("- (e) Công bố: bật \"AI use = Yes\" trên YouTube;", "truoc-dong",
     "- (d) cập nhật 24–25/10/2026 (P-2510): (1) **1666 ban ngày:** mở tấm nền N2+ cho cảnh 1666 ban ngày **ở bản cuối, có điều kiện**: chỉ tấm qua bộ kiểm 1.17.6 (" + R + "); tấm trượt → dùng 3D; thay câu \"Mở tấm nền cho cảnh 1666 ban ngày: chưa có quyết định\" ở dòng trên; cảnh đêm/lửa vẫn không dùng tấm nền; animatic giữ V1 (duyệt 24/10/2026 12:29, \"chon A theo khuyến nghị\"). "
     "(2) **Ngân sách Gemini T4 $55, mốc theo dõi $45** (thay $35/$30 ở dòng (d) đầu và cách khai §13.6: `ngan_sach_gemini_usd: 55`, `ngan_sach_gemini_moc_usd: 45`) (duyệt 25/10/2026 07:01, N1). "
     "(3) **Góc cao timelapse ≥ 60 % thân phim giữ nguyên** (GOC-CAO-60) (duyệt 25/10/2026 07:01, N2). "
     "(4) Chủ dự án đồng ý **nới dùng Gemini** và thêm cảnh cận, trung mô tả chân thực sự kiện, nhân vật, công trình biểu tượng (nhận xét 25/10/2026 06:56, mục 3); danh sách cảnh và mọi chỗ đụng (f) (công trình có tên làm chủ thể, nhân vật lịch sử có tên) chờ danh sách điểm nhấn NC-T4 được duyệt (N4) — tới lúc đó (f) giữ nguyên."),
    # §15 (j) cập nhật sau THU-B-T4 + K-1.17.6
    ("Vẫn **ĐANG THỬ, CHƯA ÁP** tới khi vòng thử THU-B-T4 đạt (điều kiện 2) và chủ dự án duyệt kết quả (điều kiện 3).", "sau-dong",
     "- (j) cập nhật sau THU-B-T4 + K-1.17.6 (P-2510): điều kiện (3) đã có — chủ dự án chọn theo phiếu THU-B (24/10/2026 15:25, \"theo khuyến nghị\"): B1 M1-trung 1666 = V2; B2 M4-trung 2026, B3 H3-05 P4 1938 = B chiếu; D1, D2 = D 3D. Phạm vi: **B (AI phủ bề mặt) chỉ ở nhà ≥ 4 px/m** (T2 = b; khai `be_mat_nha_px_m_min: 4` — nhà 2–4 px/m giữ render); **cách: tỉ số bóng khi máy cố định; chiếu 3D khi máy di chuyển chỉ dùng sau khi phía dựng sửa chiếu 3D (khử sáng, bóng trùng render) và tấm qua (d) khi đo lại — tới lúc đó B chỉ ở shot máy cố định** (T1; K1176-D3 = A, tạm B); mọi tấm B bắt buộc soi các hộp (w) cạnh màu mới trên tờ so (K1176-D2 = A; (w) chỉ báo); **toàn cảnh dùng D 3D** (`look3`, cờ d) + **nâng vật liệu 3D toà 2026 có tên** (T3 = b, T4 = a; §14.7 LOOK-T4-8); **không vân nướng AI ở toàn cảnh**. Điều kiện (2) giữ: chỉ tấm qua đủ cổng (c) + BE-MAT-NHA theo " + R + " được dùng; sàn Y cho thước nhấp nháy làm ở phiên K đo lại trước bản cuối (K1176-D6 = A). **Vẫn chỉ áp ở bản cuối**; animatic giữ look V2 (duyệt 24/10/2026 15:25, phiếu THU-B; 24/10/2026 17:54, \"K1176-D1…D6 theo khuyến nghị\")."),
    # §19 (c) ngoại lệ T4 + từ T4 mọi tập
    ("Tính chung trần tư liệu + tranh khắc + thẻ ≤ 10 % thời lượng.", "sau-dong",
     "\n**(c) ngoại lệ T4 và cách kết hợp tư liệu từ T4** (duyệt 24/10/2026 12:52, \"Duyệt cách kết hợp tư liệu theo khuyến nghị\"; 24/10/2026 17:54, K1176-D4 = A): (1) **T4: trần tư liệu + tranh khắc + thẻ = 15 %** thời lượng (thay 10 % cho riêng T4; khai `tu_lieu_tran_pct: 15`). (2) **Từ T4, mọi tập:** tư liệu chỉ chồng lên shot 3D; **không chồng lên và không ghép liền clip Omni (M-d)**; **mỗi lần ≤ 10 s** (khai `tu_lieu_lan`; hàng TU-LIEU-10 và TU-LIEU-OMNI — " + R + "). (3) Vị trí T4: Hollar sau cháy (met-360649-0) → H1-18; YCBA *General View of London during the Great Fire* (ycba-40597) → H1-08b; Luyken (1698) → H1-16; chân dung Charles II → H2-02, chân dung Wren trong thẻ Wren; Hollar Old St Paul's từ phía Đông (met-395057) → H2-09; Ogilby giữ D13 (không lên hình). (4) Hollar *Prospects*: met-360649-**0** là tấm SAU cháy, met-360649-**1** là tấm TRƯỚC cháy (đọc trên bản khắc); ghi công \"published 1666\", không gán 1647 (lệnh bổ sung ANIMATIC-T4, 24/10/2026 12:48).\n"
     "\n**(c) ảnh và footage thật** (nhận xét chủ dự án 25/10/2026 06:56, mục 4: \"Thêm các ảnh, footage thật (nếu có)\"; 25/10/2026 07:01, N5): footage hiện đại ưu tiên nguồn miễn phí có giấy phép thương mại rõ (không NC/ND); **mua chỉ khi chủ dự án duyệt giá**; mỗi mục vào RIGHTS + `licenses/` trước khi lên hình; tính vào trần (c) và theo (2) ở trên. Danh sách cụ thể chờ NC-T4 (N4)."),
]

for neo, kieu, van in SUA:
    n = s.count(neo)
    if n != 1:
        sys.exit(f"DỪNG: neo xuất hiện {n} lần: {neo[:70]!r}")
    i = s.index(neo)
    if kieu == "thay":
        s = s.replace(neo, van, 1)
    elif kieu == "sau-dong":
        j = s.index("\n", i)
        s = s[:j + 1] + van + "\n" + s[j + 1:]
    elif kieu == "truoc-dong":
        j = s.rfind("\n", 0, i)
        s = s[:j + 1] + van + "\n" + s[j + 1:]
open(p, "w", encoding="utf-8").write(s)
print("xong:", len(SUA), "chỗ")
