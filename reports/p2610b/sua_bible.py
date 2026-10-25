#!/usr/bin/env python3
# P-2610b: sửa docs/BIBLE-KENH2.md theo K1178-D1…D6 và phiếu xem v2. Chỉ chèn dòng sau mốc (mỗi mốc đúng 1 lần) + sửa dòng đầu.
# Dùng: /opt/cine/bin/python -I reports/p2610b/sua_bible.py docs/BIBLE-KENH2.md
import sys

p = sys.argv[1]
L = open(p, encoding="utf-8").read().split("\n")

R = "`checks/ll/RULES-LL.md` mục 1.17.8 (LOCK 1.17.8 `045b7bb7…`; Kinh thánh không chép luật)"
Q = "(duyệt 26/10/2026 00:12, \"Duyệt phiếu xem v2 theo khuyến nghị\")"
D = "(duyệt 26/10/2026 06:28 — giờ chủ dự án dán lệnh P-2610b sau khi trả lời điều phối \"K1178-D1…D6 theo khuyến nghị\""


def d(x):
    return D + "; " + x + ")"


CHEN = [
    ("- Chủ dự án chạm ≤ 3 lần/tập.",
     "- Bản xem gửi chủ dự án (từ bản cuối T4): chia **5–6 phần**, mỗi phần ≤ 5 MB, âm AAC ≥ 128 kb/s như F5 (phiếu xem v2 C5 = (b)) " + Q + "."),
    ("13.4 bổ sung — T4 London:",
     "\n13.4 bổ sung 26/10/2026 (P-2610b) — T4: các câu XEM CÂM có hình đổi ở animatic v3 (**Q2, Q3, Q4, Q6**, phiếu xem v2 mục B) chưa chấm; **chủ dự án chấm trên bản cuối** — cổng XEM-CAM ở G2; các câu còn lại giữ điểm v1 " + Q + "."),
    ("- Từ T4, nhịp đo trên video:",
     "- Cập nhật 26/10/2026 (P-2610b): hiệu chuẩn lại BIEN-CO-V trên animatic T4 v2 **không đạt** (`reports/k1178/K1178-BAO-CAO.md` §5) → với T4, BIEN-CO-V **chỉ Cảnh báo** (cả ở G2) và Q37 (b)(c) **không cộng biến cố đo**; phía dựng **khai beats đủ** cho Q37; hiệu chuẩn lại trên master/animatic đủ bitrate + tách thị sai trước G2 (K1178 §13). Luật kiểm: " + R + " " + d("D4 = A") + "."),
    ("- Hàng kiểm theo 1.17.7 (từ T4):",
     "- Hàng kiểm theo 1.17.8 (từ T4): mới **N2P-E** (tấm nền AI toàn khung hiện đại — §15 (k) (E)); đổi **K-LAI-3** (đoạn M-d mức nen nhận Flash + tờ khung; ngoại lệ có chủ dự án duyệt), **Q34** (T4 nhận loại `minh_hoa`/`tu_lieu`/`that`), **Q26b T4 KHÔNG ÁP** (Q26b-K2 đo thay), **SACH-1** (log chữ khuôn khoảng + vai §17 (5)), **Q37 (d)** miễn khối thẻ PP, **TU-LIEU-OMNI** (góc khung kề M-d với < 1 s 3D sạch tính là ghép liền; chỉ đếm clip M-d gần nhất mỗi phía), **BIEN-CO-V T4 chỉ Cảnh báo** (dòng cập nhật 26/10 ở trên) — trả lời C7 của phiếu xem v2. Định nghĩa, trường đọc, ngưỡng: " + R + "; cách khai theo `reports/k1178/K1178-BAO-CAO.md` §4 " + d("D1 = A") + "."),
    ("- Cách khai thêm từ 1.17.5 (theo",
     "- Cách khai thêm từ 1.17.8 (theo `reports/k1178/K1178-BAO-CAO.md` §4; " + R + "): **`vung` cho từng shot** = khu nội dung (vd `bankside`, `cheapside`, `st_pauls`, `thames_pool`, như T3), không dùng `noi` thay vùng (D6 = A); `log_chu` khuôn khoảng theo vai §17 (5); `tu_lieu_lan` cho mọi lớp tư liệu/khắc/thẻ/bản đồ trong shot 3D; đoạn M-d mức nen giữ `muc_kiem: nen`, `kiem_t1`, `to_khung`, thêm `ngoai_le_duyet` (không email) khi chủ dự án duyệt dùng clip Flash LOẠI; tấm E khai theo K1178 §4 " + d("D1 = A, D6 = A") + "."),
    ("- LOOK-T4-9 (C6) Bản cuối:",
     "- LOOK-T4-9 cập nhật 26/10/2026 00:12 (P-2610b) " + Q + ": (1) **C3:** đo trên khung animatic v3, xoay 4° chỉ đưa mái vòm St Paul's lên ≈ 20–21 % chiều rộng khung (chưa tới ≈ 30 %); animatic giữ 4° ((a)); **bản cuối thử (c): dời điểm đứng P1 sang tây 60–80 m** (thay câu \"giữ điểm đứng\" ở LOOK-T4-9 cho lượt thử này), vòng cung lửa giữ trong khung; tham số P1 mới lưu một lần, mọi lần P1 tái xuất đọc lại (§19 (a) luật 3). (2) **C9b:** cảnh đêm 1666 **M04 +0,5 EV** nữa ở bản cuối ((b)). (3) **Mở lạnh** dùng **góc lửa khác shot M03** (không lặp khung M03)."),
    ("- (d) cập nhật 25/10/2026 11:58 — luật 1.17.7",
     "- (d) cập nhật 26/10/2026 (P-2610b): (1) **M-d điểm nhấn ở bản cuối** (phiếu xem v2 C1 = (b)) " + Q + ": thử lại 6 clip điểm nhấn đã trượt (H1-06x, H1-15x, H2-02b, H2-06b, H2-09x, H2-10b), **≤ 2 lượt/clip**, lệnh sửa theo lỗi bộ kiểm đã đo, **ảnh đầu dựng từ render 3D cùng năm**; gộp vào lượt 720p của phiên bản cuối; không nới luật kiểm (C1 (c) không chọn). (2) **H1-06b** (mức nen; Flash LOẠI vì hoạ tiết tròn giống chữ, do_tin 0,55–0,58): **ngoại lệ ở animatic** (`ngoai_le_duyet`); bản cuối 720p kiểm lại, còn đọc ra chữ thì sinh lại ≤ 2 lượt hoặc về 3D. Luật kiểm (K-LAI-3 mức nen): " + R + " " + d("D5 = A") + "."),
    ("- (f) cập nhật 25/10/2026 11:58 (P-2610)",
     "- (f) cập nhật 26/10/2026 00:12 (P-2610b) — A1 phiếu xem v2, chủ dự án duyệt từng clip nhân vật có tên " + Q + ": **H1-05a** (Samuel Pepys, Charles II) duyệt; **H1-15b** (Samuel Pepys) duyệt, **bản cuối cắt khung để mặt ≤ 1/8 chiều cao khung** (animatic có khung mặt > 1/8); **H3-05b** (Godfrey Allen, khung xa) duyệt — người này thuộc danh sách \"chỉ thẻ chữ\" ở (f) nới hẹp và clip không có chân dung tham chiếu; duyệt theo từng clip (P2 = (b)), câu \"chỉ thẻ chữ\" giữ cho mọi trường hợp khác. Dòng duyệt: AUTHORSHIP.md (26/10/2026 00:12)."),
    ("- (k) **Phần hiện đại T4",
     "- (k) cập nhật 26/10/2026 (P-2610b): **điều kiện (1) đã có** — LUẬT E khoá ở 1.17.8, hàng **N2P-E**: " + R + " " + d("D1 = A") + "; **còn điều kiện (2): thử 2 khung** E đạt bộ kiểm trước khi dựng hết (đáp án K-1.17.8 chỉ có P9-2026; P1-2026 chưa có render V2 trong git — K1178 §1.2). Mô hình nhìn báo nhầm \"bờ sông bị vẽ lại\" trên tấm E (N2P-1 (b)/N2P-3 (b)) **giữ Chặn**; ngoại lệ đưa vào phiếu cho chủ dự án duyệt cùng khung E; báo nhầm lặp lại thì phương án B để phiên K sau (D2 = A). Tháp bịa (f2) mức **Cảnh báo** (D3 = A). **Tấm nền P1-2026 mới** (H5-04, theo hướng máy P1 mới ở LOOK-T4-9 cập nhật 26/10) làm ở bản cuối, qua bộ kiểm đúng loại tấm (phiếu xem v2 C4 = (b)) " + Q + "."),
    ("- (4) cập nhật 25/10/2026 11:58 (P-2610)",
     "- (5) cập nhật 26/10/2026 (P-2610b): log chữ của lớp chồng khai theo **vai** — `year` (bộ đếm năm), `the_chuong`, `the_phuong_phap`, `where` (chip nơi), `the_nhan_vat`, `bo_dem_so`, `chu_thich_tu_lieu`; trần mỗi vai theo (1)–(3) ở trên và §13.3; khuôn khoảng và cách đo SACH-1: " + R + " " + d("D1 = A") + ". **Thẻ Pepys/James chỉ chữ** (không chân dung; phiếu xem v2 C6 = (a)) " + Q + "."),
    ("**(a)/(c) cập nhật 25/10/2026 11:58 — nhịp cắt",
     "\n**(c) cập nhật 26/10/2026 00:12 — ảnh/footage thật T4 ở bản cuối** (P-2610b) (phiếu xem v2 C2) " + Q + ": phiên bản cuối **tự tải lại ảnh gốc IWM D 6418** — bản gốc trên Commons (600×800; không tải từ trang IWM vì điều khoản phi thương mại), thay bản thu 500×667; SHA + bằng chứng ở `licenses/`, RIGHTS; **BỎ footage đêm 2026 ở T4** — câu \"T4 chỉ 1 clip footage đêm (H5-07a, ≈ 6 s; P7)\" ở (c) cập nhật 25/10 09:15 mục (5) không dùng, H5-07a giữ 3D; vì vậy không cần PDF trang giấy phép Pexels/Pixabay."),
]

for moc, dong in CHEN:
    idx = [i for i, s in enumerate(L) if s.startswith(moc)]
    assert len(idx) == 1, (moc, idx)
    L.insert(idx[0] + 1, dong)

cu = "(duyệt 26/10/2026 00:07) (P-2610) — 26/10/2026)"
assert L[0].endswith(cu)
L[0] = L[0][:-1] + "; sửa §6, §13.4, §13.6, §14.7 LOOK-T4-9, §15 (d)(f)(k), §17, §19 (c) theo K1178-D1…D6 (duyệt 26/10/2026 06:28) và phiếu xem v2 (duyệt 26/10/2026 00:12) (P-2610b) — 26/10/2026)"

open(p, "w", encoding="utf-8").write("\n".join(L))
print("xong", len(CHEN), "chỗ chèn + dòng đầu")
