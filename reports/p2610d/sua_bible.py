#!/usr/bin/env python3
# P-2610d: sửa docs/BIBLE-KENH2.md theo K1179-D1…D7. Chỉ chèn dòng sau mốc (mỗi mốc đúng 1 lần) + sửa dòng đầu.
# Dùng: /opt/cine/bin/python -I reports/p2610d/sua_bible.py docs/BIBLE-KENH2.md
import sys

p = sys.argv[1]
L = open(p, encoding="utf-8").read().split("\n")

A = "(duyệt 26/10/2026 13:02 — giờ chủ dự án dán lệnh P-2610d sau khi trả lời \"Duyệt K1179-D1…D7 theo khuyến nghị điều phối\"; `reports/k1179/K1179-BAO-CAO.md` §12"
R = "`checks/ll/RULES-LL.md` mục 1.17.9 (LOCK 1.17.9 `9eddaf24…`; Kinh thánh không chép luật)"


def a(x):
    return A + "; " + x + ")"


CHEN = [
    # §13.6 — nhịp T4 (D3)
    ("- Cập nhật 26/10/2026 (P-2610b): hiệu chuẩn lại BIEN-CO-V",
     "- Cập nhật 26/10/2026 13:02 (P-2610d) — nhịp T4 " + a("K1179-D3") + ": từ 1.17.9 Q37 (b)(c) cộng thêm biến cố **đo từ log máy** (mặt trời qua 0°/−6°, pha máy đứng↔chạy); beats `bien_co_tl` tự khai vẫn không được nhận; biến cố `fire` ±10 % và mỗi lần năm nhảy **không** nhận. Đo trên đặc tả v4: TB 5,75 → 5,04 s, dài nhất 20,17 s, **39 khoảng > 6 s** (M00 17,0 s, M01 17,9 s, H2-03b 20,2 s, H5-07b 15,3 s, H1-06 14,9 s, H5-08 14,0 s, H3-05 12,7 s…) → đây là **nhịp thật của phim**, khớp nhận xét chủ dự án 25/10 06:56. (1) **Q37 giữ Chặn ở G2** — không nới (c), không thêm phần tử chỉ để vượt ngưỡng. (2) **Nhịp sửa ở khâu dựng, SAU khi chủ dự án xem bản xem 1080p:** ở shot chủ dự án chỉ ra, rút ngắn hoặc cắt xen shot dài **bằng khung đã dựng (không dựng lại)**, hoặc thêm biến cố **CÓ NGHĨA** theo §13.2 (vật mang nghĩa). (3) **Miễn có duyệt cho ≤ 3 shot \"đứng có chủ ý\"** do chủ dự án chọn khi xem; mỗi shot miễn ghi một dòng AUTHORSHIP (ngày, giờ, mã shot). (4) K hiệu chuẩn BIEN-CO-V T4 trên master 1080p sau phiên B (K1178-D4 giữ); tới lúc đó dòng cập nhật P-2610b ở trên giữ nguyên (BIEN-CO-V T4 chỉ Cảnh báo). Luật kiểm: " + R + "."),
    # §13.6 — hàng kiểm 1.17.9 + LOCK hiện hành (D1)
    ("- Hàng kiểm theo 1.17.8 (từ T4): mới **N2P-E**",
     "- Hàng kiểm theo 1.17.9 (từ T4) — **LOCK hiện hành 1.17.9 `9eddaf24e8c5276b6017af172e7c8185ba21831a7b6e842cc17094fd5c66fc34`** (thay 1.17.8 `045b7bb7…`; T3 không đổi kết quả): N2P-1 (b)/N2P-3 (b) nhận **`ngoai_le` có `duyet_chu_du_an`** trên tấm E (§15 (k)); N2P-E (k) **toà có tên** theo `loai`; N2P-E (h) **đẩy/trượt 2D**; N2P-E (u) **nước AI** (`nuoc_ai`); Q37/NHIP-K2/Q37 (1.13) cộng biến cố đo từ log máy (§13.6 cập nhật 13:02); NHAN-VAT-TEN đọc **`cat_clip`** và **miễn (k) khi không có chân dung** (§15 (f)). Định nghĩa, trường đọc, ngưỡng: " + R + "; phán quyết và số đo: `reports/k1179/K1179-BAO-CAO.md` §2–§3 " + a("K1179-D1 = A") + "."),
    ("- Cách khai thêm từ 1.17.8 (theo `reports/k1178/K1178-BAO-CAO.md` §4;",
     "- Cách khai thêm từ 1.17.9 (theo `reports/k1179/K1179-BAO-CAO.md` §4; " + R + "): tấm E ngoại lệ `ngoai_le` (khuôn §4, mẫu `reports/k1179/do/k2/e/KN1-khai-thu-episode.yaml`; không email); `toa_co_ten[].loai` + `dinh_odn_m` hoặc `nguon_lich_su`; `n2p.video[].day_2d {kieu, toc_do_pct_s}`; tấm `nuoc_ai: true` + `duyet_chu_du_an`, ghép bờ phía đất (`reports/k1179/do/ghep_kn8.py <khung> <lượt> thap bo_dat`); `cat_clip` đúng khung bản dựng dùng; NHAN-VAT-TEN `chan_dung: khong_co` + `chan_dung_nguon_da_tra.noi` + `duyet_chu_du_an` \"YYYY-MM-DD HH:MM\" trỏ dòng AUTHORSHIP cùng ngày-giờ-mã shot " + a("K1179-D1 = A") + "."),
    # §15 (f) — D7
    ("- (f) cập nhật 26/10/2026 00:12 (P-2610b) — A1 phiếu xem v2",
     "- (f) cập nhật 26/10/2026 13:02 (P-2610d) — NHAN-VAT-TEN (k) khi không có chân dung " + a("K1179-D7; luật 1.17.9 KN-7") + ": clip nhân vật có tên **không có chân dung tham chiếu** được **miễn (k)** khi đủ ba điều kiện 1.17.9: (1) khai `chan_dung: khong_co` + `chan_dung_nguon_da_tra.noi` (≥ 1 nơi đã tra); (2) YuNet đo trên clip (trong `cat_clip` nếu có): mọi hộp mặt điểm **≥ 0,60** (không chỉ ≥ 0,75) **≤ 1/8** chiều cao khung; (3) `duyet_chu_du_an` \"YYYY-MM-DD HH:MM\" trỏ dòng AUTHORSHIP cùng ngày, giờ, mã shot. Miễn (k) không miễn (a). **H3-05b (Godfrey Allen) giữ** — đủ điều kiện: YuNet ≤ 0,070, 4 nơi đã tra, AUTHORSHIP 2026-10-26 00:12. **Trước gói phát hành tra thêm** NPG, St Paul's (lưu trữ nhà thờ), Wikimedia Commons, Historic England; tìm thấy chân dung thì xét lại (k). **H3-05c (3D) chỉ là dự phòng.** **H1-15b** giữ `cat_clip` [0, 110] (YuNet trong cửa sổ 0,062 — hết (a)/(w), lỗi mã KN-4 đã sửa)."),
    # §15 (k) — D1, D2, D4, D5, D6
    ("- (k) cập nhật 26/10/2026 10:08 (P-2610c)",
     "- (k) cập nhật 26/10/2026 13:02 (P-2610d) " + a("K1179-D1, D2, D4, D5, D6") + ": LUẬT E theo 1.17.9 (" + R + "). (1) **Toà có tên (D4)** cho LUẬT E = **tháp đỉnh ≥ 75 m ODN** (`loai: thap`, `dinh_odn_m`) **+ công trình lịch sử có `nguon_lich_su`** (NHLE/Historic England…; `loai: lich_su`) **+ St Paul's** (`loai: mai_vom`) — đây là mặt nạ \"tháp\"; toà OSM có tên khác coi là nhà thường. **\"Guildhall Art Gallery\" không tính là lịch sử nếu không có nguồn** (toà mới; danh sách lịch sử khớp theo tiền tố của phiên A nhận nhầm). Trường `nguon` của toa.json (nguồn mặt nạ) không thay `nguon_lich_su`. Đo: (a)-E P9 13,88 → 5,74 %, P1 38,11 → 28,36 %. (2) **Ngoại lệ \"bờ\" (D2) DUYỆT** cho tấm **E-P9-ngay-l1**, mặt nạ \"tháp\", shot **H5-05a**: hộp **[0.0, 0.96, 0.09, 1.0]** (góc dưới trái — mép kè/nước ngoài dải bờ 8 px; máy 0/255, T9c 0), hàng N2P-1 (b), N2P-3 (b); khai đúng khuôn `reports/k1179/K1179-BAO-CAO.md` §4 (`ngoai_le: [{hang: [\"N2P-1 (b)\", \"N2P-3 (b)\"], hop: [0.0, 0.96, 0.09, 1.0], ly_do: …, duyet_chu_du_an: {nguoi_ky: \"Chủ dự án (tác giả – đạo diễn)\", vai: chu_du_an, ngay: \"2026-10-26\", ket_luan: chap_nhan}}]`); dòng AUTHORSHIP K1179-D2. Ngoại lệ chỉ hạ báo MÔ HÌNH xuống (w) khi máy sạch; máy không được miễn; tấm/hộp khác cần duyệt riêng. → câu \"K bác → dùng mặt nạ đủ\" ở cập nhật 10:08 hết hiệu lực; **H5-05a dùng mặt nạ \"tháp\" + ngoại lệ \"bờ\"**. (3) **Đẩy/trượt 2D trên tấm E (D5) cho phép**: **MỘT phép 2D cho cả khung ghép** (dựng SAU ghép), **≤ 1,5 %/s**, **máy 3D giữ CODINH** (MAY-19 (b) đo log như cũ); khai `n2p.video[].day_2d`; dùng **theo tờ so**, chủ dự án duyệt ở phiếu bản cuối (dự kiến M01/H5-05a — liên quan nhịp §13.6). (4) **Nước AI trên tấm E (D6) cho phép**: tấm khai `nuoc_ai: true`, ghép **giữ bờ PHÍA ĐẤT** (không dải ±8 px hai phía — viền xanh), **duyệt từng tấm qua tờ so** (`duyet_chu_du_an`); **trước khi dùng phải sửa:** thuyền render **elip đen** (lớp tàu P1) và **bóng cầu AI lệch** (che hoặc ghép lại vệt tối cạnh cầu); T9c trên nước AI chỉ in, không làm thước. → mục (2) \"Tấm E-P1 chưa dùng — chờ KN-8, KN-6\" ở cập nhật 10:08: điều kiện luật đã có; dùng E-P1 khi qua (4) và tờ so được duyệt."),
]

for moc, dong in CHEN:
    idx = [i for i, s in enumerate(L) if s.startswith(moc)]
    assert len(idx) == 1, (moc, idx)
    L.insert(idx[0] + 1, dong)

cu = "(duyệt 26/10/2026 10:08) (P-2610c) — 26/10/2026)"
assert L[0].endswith(cu)
L[0] = L[0][:-1] + "; sửa §13.6 (nhịp T4, hàng kiểm và cách khai 1.17.9, LOCK hiện hành 1.17.9), §15 (f)(k) theo K1179-D1…D7 (duyệt 26/10/2026 13:02) (P-2610d) — 26/10/2026)"

open(p, "w", encoding="utf-8").write("\n".join(L))
print("xong", len(CHEN), "chỗ chèn + dòng đầu")
