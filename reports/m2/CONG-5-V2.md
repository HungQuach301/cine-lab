# CỔNG 5 · VÒNG v2 — LAYOUT "Last Round" (theo quyết định chủ dự án sau Cổng 5)

Phiên P · nhánh `claude/cine-lab-m2-cong5-layout-24o5fp` (@44a469a) · 28/09/2026 04:30–08:45 UTC · **KHÔNG merge Cổng 5.** DỪNG, chờ chủ dự án.

## 0. Tóm tắt
- **Ghi công đã sửa** trong `AUTHORSHIP.md` (lỗi do Claude rà độc lập bên ngoài phát hiện; chủ dự án duyệt và giao sửa) + mục "Cổng 5 — quyết định".
- **B1 + a–d đã vào phim**; rà continuity v2 tìm 1 chặn + 6 nên sửa → đã sửa hết mục hình, render lại. Layout v2: **52 shot, 2:20,5** (3 372 khung; −2,0 s so với v1, trong ±5 s). `screening/layout.mp4` **44,84 MB**, phụ đề cháy, âm tạm dựng lại theo mốc mới; sao y từng byte `design/cong5/layout/out/layout.mp4` (SHA `78e662d1…`).
- **Hiệu chuẩn phép kiểm mặt:** 0/4 khung "Sprite Fright" bị gọi mặt nạ/búp bê → **giữ tiêu chí cũ**.
- **Cổng mặt Ida (A-α): KHÔNG ĐẠT.** Tuổi/giới 4/4, cảm xúc 4/4 (tốt nhất từ trước tới nay), nhưng **4/4 ảnh vẫn có "búp bê/mặt nạ/ma-nơ-canh/con rối"**. A-α vẫn vào phim (tóc trắng hơn là yêu cầu cho mọi shot; giới/tuổi đọc tốt hơn A1). characters **v1.4**, khoá SHA.
- **Luật v1.4 (bản cuối): TRƯỢT** — trượt P0 (báo nhầm lần 2: hai người trong hốc đọc "MA"), G3b, H1b, C3. Kiểm toán C3 **TRƯỢT** ở s35: lệch 3,21 % điểm ảnh biên (ngưỡng 2 %) — P tìm ra nguyên nhân thật: **s35 phụ thuộc thứ tự render** (mục 5).

## 1. B1 và a–d: trước / sau (số đo thật)
| Mục | Trước (layout v1) | Sau (layout v2) | Bằng chứng |
|---|---|---|---|
| **B1** cột điện phố chính | cột (13,5; −4,2) cách L11 ~5,6 m → tường chim trắng từ 1:04 nhưng góc L11 tối ở cảnh 5 (mâu thuẫn C2) | cột vào sân trước hông nhà kho **(17,0; −5,9)**, tầm 8,5 m (điểm (15,4; −6,2) P đề xuất rơi vào nhà đầu dãy bắc → dời dãy bắc sang x = 18,5); Cas (14,3; −7,15), cách L11 7,1 m. Đầu đèn cách tường chim 5,2 m (trong vũng), cách L11 9,5 m (ngoài). Rà v2: một cột duy nhất, tắt tới khung 1546 (1:04,42) rồi bật; góc L11 đúng ở s27, s35, s37w; P5 bật khung 2381 (1:39,2). s33 (C5) ngoài vòm nay tối: tường (48, 46, 52)/(91, 69, 61), trước (217, 217, 221) | `reports/m2/cong5/w2/v2_B1_*.jpg`, `v3_C5-N3_s33.jpg`, `reports/m2/cong5/w1/v2_B1_s23-s24c.jpg` |
| **(a)** 1:20–1:28 người/bóng | s33 rộng tĩnh 7 s; lưng tối, áo Ida chìm đen; AI mù "3–4 khối tối", "đứa trẻ thứ hai" | s33 **5,0 s**, dolly 0,9 m + dịch ngang 0,4 m (thị sai); phơi sáng 1,0 → 1,5: lưng Ida/Cas bắt ánh vàng đèn lồng; đèn x 0,2, Cas 0,9 → bóng Ida lệch trái 0,77 m (vành mũ bóng tách khỏi thân); bóng bà ×1,94, cậu ×1,36 | `v2_a_s33-s34.jpg`, `v3_C5-N3_s33.jpg`. Chưa kiểm mù lại đoạn này |
| **(b)** ~1:52 đèn đã tắt | AI mù "the lamp still looks lit" | kính L11 tối đục (#16181f, độ đục 0,85) ở s40w, s41, s42a; độ sáng vùng lồng đèn s40w **73,5 → 54,7** (/255); không lửa, không quầng. Rà v2: L11 tắt khung 2621 | `v2_b_s40-s40w-s41.jpg` |
| **(c)** tỷ lệ đá lát | đá "to như cuội" (0:42, 1:44), nền cận đồng hồ "chấm bi" (0:18, 0:28, 2:12) | trải 2,4 m/tile: viên **0,088–0,136 m, TB 0,112 m ≈ 1/14,8 chiều cao Ida (1,66 m)**; đá phiến vỉa hè 0,45–0,95 → 0,34–0,71 m (s14). s46: đổi máy, nền là tường ngõ. s06, s09w: nền nhoè (giả lấy nét ở khâu dựng, không đổi texture khoá; lấy nét thật ở Cổng 7) | `reports/m2/cong5/w1/v2_c_da-lat.jpg`, `w2/v2_c_s46.jpg` |
| **(d)** tóc trắng hơn | #b9b3aa; dưới lửa s05 hue 30°, S 0,58 → đọc "tóc vàng" | #e2dfda + cách điệu "tóc bạc" (ánh sáng tới tóc kéo 70 % về trung tính): s05 **S 0,58 → 0,31**, s26 **S 0,31 → 0,10**; s05 bản render **S 0,36, đọc bạc**. Kiểm mù lần 6: 4/4 "tóc bạc trắng" | `reports/m2/cong5/w3/BAO-CAO-W3.md` mục A-α |

Việc nhỏ đã làm: (1) đèn lồng thắt lưng TẮT s02 → bắt lửa khung 283 (s04), nhịp tay mồi ghi `shots_w1.json` cho Cổng 6; (2) máy s02, s15 giữ; (6) hàng đợi có **làn nhanh** (`LAN=nhanh`, việc < 60 s): 26 việc chờ 0 s (v1: ảnh 20 s có lúc chờ 1 956 s); (5) khiếu nại P0 đã ghi (thêm lần 2).

## 2. Hiệu chuẩn phép kiểm mặt (nguyên văn: `reports/m2/cong5/hieu-chuan/HIEU-CHUAN.md`)
4 khung "Sprite Fright" (© Blender Foundation, CC BY 4.0; chỉ hiệu chuẩn nội bộ, không đưa vào phim, khung không commit — `RIGHTS.md` REF-SF-HC), cỡ cảnh gần khung Ida, 2 cảnh đêm. Mỗi khung một subagent mới, cùng câu hỏi.

| Khung | Đọc ra | Cảm xúc | "mặt nạ/búp bê/con rối/ma-nơ-canh"? |
|---|---|---|---|
| b7 Ellie 1:44,5 | bé gái 10–12 | lo lắng, bối rối | Không |
| f2 Ellie 4:16 (đêm) | bé gái 10–13 | lo lắng, ngại | Không ("da… như đất sét hay tượng") |
| n4 Victoria 5:32 (đêm) | nữ 40–50 | đau khổ, hoảng sợ | Không |
| u8 Rex 1:43,5 | nam 25–35 | tự mãn | Không |

**0/4 → giữ tiêu chí cũ** (quy tắc: ≥ 2/3 mới đổi sang tiêu chí so sánh). Phép kiểm phân biệt được: người xem vẫn chê chi tiết ở phim chuyên nghiệp (khuyên "dán vào má", cổ mảnh) nhưng không gọi là búp bê.

## 3. Cổng mặt Ida — A-α (nguyên văn: `kiem-mu-mat/aa-tung-buoc.md`, `lan6.md`)
Kiểm từng bước (1 ảnh/bước, định hướng): **bước 1** (cổ lộ 0,46 H, cổ áo bẻ thấp, mũ hạ) — "hơi giống đàn ông… cổ ma-nơ-canh… tượng sáp hoặc mặt nạ"; **bước 2** (mặt tròn–mềm, khối tóc bạc, da sắc độ, cổ 0,40 H) — giới "Nữ" chắc chắn, tóc "bạc trắng", còn "con rối hoặc tượng sáp"; **bước 3 = bộ cuối**.

| Tiêu chí (sau hiệu chuẩn) | Lần 6 — A-α | (lần 4 A1 · lần 5 A3) |
|---|---|---|
| 4/4 phụ nữ lớn tuổi | **4/4** chắc chắn (65–80) | 3/3 · 3/3 nhưng 2/3 do dự |
| ≥ 3/4 cảm xúc đúng | **4/4** | 3/3 · 3/3 |
| Không ảnh nào mặt nạ/búp bê/con rối/ma-nơ-canh | **TRƯỢT 4/4** | trượt 3/3 · trượt 3/3 |

Câu then chốt: x4 "đầu búp bê hay ma-nơ-canh"; j7 "mặt nạ gắn vào đầu… búp bê lắc đầu"; e2 "tượng hoặc mặt nạ… búp bê hay tượng sáp"; ảnh 4 (s39 khung 2531, layout) "đầu trông như gắn lên cổ, giống con rối… giống búp bê", thêm lỗi mới "mắt đỏ… ma quái" dưới ánh điện.
Lời chê còn lại gom 4 nhóm: (1) hình đầu–mặt "trứng/bóng đèn", mép mặt–tóc sắc như mặt nạ; (2) tóc là "vỏ khắc sọc"; (3) cổ mảnh như trụ, mũ lơ lửng; (4) da nhẵn sáp, mắt thuỷ tinh.

Sheet: `ida.json` cổ 0,30 → 0,40 H; tóc #e2dfda + `silver_shader` 0,7; cổ áo bẻ thấp; khăn thấp; mũ `seat_H` 0,80, `fit` 0,52; **B1 8 góc đo lại → `c3_views`** (0° thân 2,682, tay trên 1,571, cẳng tay 0,976; 135°/180° thân +7…+10 %, ±90° −4…−5 % so với v1.3). characters **v1.4**, `LOCK-THIET-KE.sha256` 26/26, `LIBRARY.json` CHR-ida-sheet-v1.4.
Phơi sáng cận mặt (điểm ảnh mặt cháy): s05 23,8 % → **0,5 %** (facelight 'gas'); s31 21,1 % → **0,07 %**; s36 16,1 % → **0,52 %**; s37 20,3 % → **0,61 %**; s39 3,7 % → **0,15 %**. s36/s37/s39 bật bóng L11 (bóng vành mũ thật); s37 máy +10° bỏ cột thang cháy sáng.

## 4. Continuity
**Rà v2** (agent cine-continuity, 52 shot; `reports/m2/cong5/continuity-v2.md`): 1 chặn, 6 nên sửa, 10 ghi nhận. Lỗi cũ: C1, C3, C4, N1, N4 đã sửa; C2 phần lớn (còn s33 → C5).
| Mã | Lỗi | Xử lý |
|---|---|---|
| C5 (chặn) | s33 ngoài vòm trắng trước khi P5 bật (trái B1) | **Đã sửa** (W2): ngoài vòm tối, chỉ hổ phách L11 |
| N2 | s42a ôm đèn → s42b chìa/xách | **Đã sửa**: ôm trước ngực suốt s41–s42b |
| N3 | s33 Ida chồng bóng | **Đã sửa**: bóng lệch 0,77 m |
| N6 | đèn lồng thắt lưng cảnh 4 (sheet mâu thuẫn) | **P chốt**: sáng liên tục tới khi tháo ở s30; s30 vũng sáng tăng dần 0,8–1,85 s (hết bật cóc) |
| N7 | s42b đứng → s42 ngồi xổm (mất nhịp) | **Đã sửa**: cuối s42b quay ra vòm, ngồi xổm, đặt đèn |
| N8 | s43 không đọc được "một ô cửa hổ phách" | **Đã sửa một phần**: mọi ô khác kính lạnh, còn một ô hổ phách — nhưng chỉ ~6–8 px ở 960 px (xem quyết định C) |
| N9 | sheet còn số cũ | **Đã sửa** (W1 canh-3, LAYOUT-W1; W2 canh-4/5/6, LAYOUT-W2, shots_w2.json) |
Sau sửa: P tự xem ảnh trước/sau C5, N8; **chưa chạy lại rà toàn phim lần 3**.

## 5. Luật máy (checks v1.4; không sửa, không đọc mã `checks/`)
**Video ghép bản cuối** (`checks/run.py design/cong5/layout/out/layout.mp4 --profile shot` → `reports/checks/layout-cong5/`):
```
[   PASS] N1 24 fps CFR; không rơi hay lặp khung theo PTS
[   PASS] N2 BT.709 đủ 3 trường; dải limited — đo cả nhãn lẫn giá trị điểm ảnh
[    N/A] N3 Codec và bitrate đúng loại master; khung 16:9, SAR 1:1
[   FAIL] P0 Máy dò chữ độc lập: mọi chữ trong hình phải có matte
[   PASS] P1 Không chữ đè chữ, tính theo điểm ảnh nét chữ
[   PASS] G4 Chữ tương phản ≥ 4,5:1 (WCAG AA), đo điểm ảnh
[   PASS] G3 Không banding trên gradient
[   FAIL] G3b Grain cố định: có grain, ổn định theo thời gian và giữa các shot, chuyển động theo khung
[    N/A] M1 Master YouTube: −14 LUFS ±1; true peak ≤ −1 dBTP
[   PASS] M3 Tương quan pha và tương thích mono
[   PASS] J1 Mọi từ trong kịch bản nghe rõ trên bản mix cuối
[   PASS] J1b Lời rõ trên nhạc theo từng câu, đo từ stem thoại và stem nền
[   PASS] H1 Không chuyển động tuyến tính ở bộ phận nhân vật
[   FAIL] H1b Chuyển động khai báo khớp hình render (luồng quang học ở vùng nhân vật)
[   FAIL] C3 Đúng model: tỷ lệ bộ phận so với model sheet, có tính nhiễu đo
[   PASS] O3 Mọi tài sản lấy từ thư viện có SHA
VERDICT: TRƯỢT
```
- **P0:** báo nhầm lần 2 — khung 1980 (s33), hộp bao **hai nhân vật đứng trong hốc** đọc "MA", độ tin 0,86 (ngưỡng 0,8). Không có chữ trong hình. Đã ghi `checks-appeal.md` (cùng gốc khiếu nại lần 1). Không sửa hình để lách.
- **C3:** 51 mẫu trượt chắc chắn, 47 không chứng minh được, biên trên lớn nhất 36,35 %, khớp biên thấp nhất 0,81 (≥ 1,5 ✗), **20 đoạn CẦN NGƯỜI XEM**. **Kiểm toán TRƯỢT**: hạt giống `9476883171053887317`, khung 1332 (khớp 0) và **2148 (s35): thân lệch 3,21 % điểm ảnh biên** (ngưỡng ≤ 2 %). P kiểm: render thẳng khung 2148 khác render nối tiếp từ 2136 đúng 19 điểm ảnh; render nối tiếp trùng khít bản nộp → **mã s35 giữ trạng thái giữa các khung** (lỗi thật, sẽ làm lệch khi chia render ở Cổng 6). Chưa sửa (đề xuất ở mục 7). Yêu cầu kiểm toán trước đó huỷ vì video đổi: lưu `reports/m2/cong5/c3-kiem-toan/`.
- **3 shot bị cờ ở v2:** s08 và s47 — CẦN NGƯỜI XEM (không mẫu đo được); **s27 thân −8,34 %** "trượt chắc chắn" (6 mẫu; layout v1 −5,7 %, animatic v2 −12,3 %) — góc máy s27 đổi theo B1.
- **G3b:** σ nhỏ nhất 0,716 (≥ 0,8 ✗), σ lớn/nhỏ 2,94 (≤ 1,3 ✗), tương quan khung kề 0,841 (≤ 0,5 ✗) — layout chưa có khâu grain (cùng gốc Cổng 4). **H1b:** track tệ nhất 25 % (≥ 90 ✗), 5 track toàn null.
- **Chỉ số trong ±5 % quanh ngưỡng:** C3 hệ số mặt nạ 4,0 (ngưỡng 4,0); C3 hệ số khi đầu < 100 px 4,0 (ngưỡng 3,98). Ngoài ra (tự nêu): s23 mặt vôi 18,5 % (mức ~20 %).
- Lệnh kiểm trên video nhóm của W2 (s30…s43): chỉ trượt G3b (σ lớn/nhỏ 1,713; tương quan 0,603 s34, 0,541 s41, 0,538 s42a).

## 6. Số liệu thời gian và token
**Hàng đợi vòng v2** (04:49 → 08:39; `reports/m2/cong5/queue-log.tsv`): 39 việc, **chạy 9 032 s (2 giờ 31 phút máy)**, chờ 2 200 s.
| Gói | Việc | Chờ | Chạy | Làm lại |
|---|---|---|---|---|
| W1 | 3 | 1 061 s | 1 632 s | 0 shot (1 lượt cảnh 3 mất khi phiên bị hệ thống dừng, chạy lại, không mất khung) |
| W2 | 5 | 1 139 s | 3 399 s | 7 shot (sửa continuity v2) |
| W3 | 19 (làn nhanh) | 0 s | 797 s | ảnh nộp 8 lần qua 3 bước; ~75 lần thử nhanh |
| P | 12 | 0 s | 3 204 s | xuất mặt nạ C3 + luật 2 lần (bản v2 trước và sau sửa continuity) |
Render đầy đủ vòng này: W1 1 176 khung / 1 632 s (1,33 s/khung); W2 1 956 khung / 2 812 s (1,44 s/khung) + 444 khung / 569 s sửa; tổng khung render ≈ 3 576 cho phim 3 372 (×1,06).

**Thời gian đồng hồ từng gói (vòng v2):** W1 ≈ 1 giờ 5 phút (A2 32 phút, C2 ~33 phút có gián đoạn, N9 2 phút); W2 ≈ 2 giờ 20 phút (A2 19 phút, s46 ~12 phút, C2 ~70 phút gồm render, sửa v2 ~33 phút); W3 ≈ 60 phút (bước 1 ~14, bước 2 ~18, bước 3 ~26); P kiểm mù 12 subagent (~30 s mỗi cái) + hiệu chuẩn 4.

**Token** (số công cụ báo khi agent kết thúc lượt; là kích thước ngữ cảnh tích luỹ của agent, không phải tiền tệ tiêu thụ; mỗi lượt đọc lại ngữ cảnh nên tổng tiêu thụ lớn hơn):
| Agent | Lượt gần nhất | Các lượt vòng v2 |
|---|---|---|
| W1 | 633 600 | 566 777 (A2) → 619 458 (C2 tiếp) → 633 600 (N9) |
| W2 | 226 069 (sau nén ngữ cảnh) | 725 063 (A2) → 734 766 (s46) → 769 975 (C2) → 226 069 (sửa v2) |
| W3 | 736 843 | 591 241 (bước 1) → 666 367 (bước 2) → 736 843 (bước 3) |
| cine-continuity v2 | 220 781 | 1 lượt |
| 12 subagent kiểm mù/hiệu chuẩn | ~48 000–50 600 mỗi cái | 4 hiệu chuẩn + 2 bước + 4 cuối + … |
**Hạn mức gói Claude (ảnh chủ dự án gửi):** 8:44 (giờ máy chủ dự án) phiên hiện tại 16 %, tuần 12 % → 11:45 tuần **16 %** (phiên mới 1 %) — tức vòng Cổng 5 v1 (phần lớn) dùng ~4 % hạn mức tuần. P không đo được % của riêng vòng v2 (cần ảnh usage mới).

## 7. Quyết định cần chủ dự án
### A. Cổng mặt Ida sau 3 phương án (A1, A3, A-α) đều trượt tiêu chí "búp bê"
| | **A-i — Đổi hướng dựng mặt: mặt điêu khắc hình khối + rig biểu cảm (A-β cũ), làm như một vòng thiết kế riêng có kiểm mù từng bước (khuyến nghị)** | A-ii — Tiếp tục A-α thêm 1 vòng nhắm 4 nhóm lời chê còn lại | A-iii — Chấp nhận A-α cho Cổng 6, ghi nhận trượt; sửa mặt ở vòng hoàn thiện nhân vật |
|---|---|---|---|
| Ưu | Lời chê lặp lại qua 6 lần kiểm đều chỉ vào gốc C′ (mặt vẽ trên đầu nhẵn → "mặt nạ", "da sáp", "nếp vẽ"); A-α đã tối đa hoá tuổi/giới/cảm xúc (4/4) nên phần còn lại là hình khối; có sẵn rig miệng cho khẩu hình Cổng 6 | Rẻ; giữ đường ống; còn vài lỗi cụ thể (mép mặt–tóc, tóc khắc sọc, mắt đỏ dưới điện) | Không chặn lịch; tuổi/giới/cảm xúc đã đạt |
| Nhược | Đảo quyết định C′ (Cổng 3); lâu nhất; phải khoá lại sheet, đo lại B1 | 3 vòng vừa rồi cho thấy lời chê "búp bê" không giảm khi sửa chi tiết | Trái tiêu chí chủ dự án đặt ("phải đạt trước Cổng 6"); rủi ro phim bị xem là "búp bê" |
| Tác động | Lùi Cổng 6; render lại mọi shot có Ida (~1 giờ máy) | 1 vòng (~2 giờ agent + ~1 giờ render) | 0 |
| Rủi ro | Thấp về kết quả, cao về lịch | Cao (có thể trượt lần 4) | Cao về chất lượng |

### B. Lỗi phụ thuộc thứ tự render (s35) làm trượt kiểm toán C3
| | **B-i — W2 sửa s35 thành hàm thuần của thời gian, render lại s35, xuất mặt nạ + kiểm toán lại (khuyến nghị)** | B-ii — Rà mọi shot tìm trạng thái ẩn (chạy render thẳng vs nối tiếp cho khung mẫu từng shot) rồi sửa hết | B-iii — Để Cổng 6 |
|---|---|---|---|
| Ưu | Nhanh (~30 phút); kiểm toán có thể đạt | Chặn lỗi cùng loại ở shot khác trước Cổng 6 (chia render) | 0 |
| Nhược | Có thể còn shot khác cùng lỗi | ~1 giờ máy | Kiểm toán C3 trượt treo |
| Rủi ro | Thấp | Thấp | Trung bình |

### C. s43 "một ô cửa hổ phách" chỉ ~6–8 px ở 960 px (12–16 px ở 1080p)
| | **C-i — Máy s43 đẩy vào chậm để ô cửa lớn dần (đúng "dolly vào rất chậm" của animatic) (khuyến nghị)** | C-ii — Thêm quầng ấm có thật quanh ô (ánh đèn lồng hắt ra mái đối diện) | C-iii — Giữ |
|---|---|---|---|
| Ưu | Đọc được mà không thêm gì giả | Giữ khung | 0 |
| Nhược | Đổi khung toàn cảnh (lặp khung mở đầu) | Phải chứng minh quang học | Khán giả có thể không thấy |
| Tác động | Render lại s43 (~2 phút) | Render lại s43 | 0 |
| Rủi ro | Thấp | Trung bình | Trung bình |

### D. Đóng Cổng 5
| | D-i — Đóng Cổng 5 (layout đạt về máy, dàn dựng, bối cảnh, continuity), mang A/B/C sang gói trước Cổng 6 | **D-ii — Làm B-i + C-i + rà continuity lần 3 + AI mù ngoài trên `screening/layout.mp4`, rồi đóng (khuyến nghị)** | D-iii — Chưa đóng tới khi A đạt |
|---|---|---|---|
| Ưu | Nhanh | Đóng với 0 lỗi continuity chặn đã biết, kiểm toán C3 có thể đạt | Chặt |
| Nhược | Mang lỗi kiểm toán sang | ~1 giờ | Chặn toàn bộ tiến độ vì một hạng mục |
| Rủi ro | Trung bình | Thấp | Cao về lịch |

## 8. Việc đang chờ chủ dự án
1. Xem `screening/layout.mp4` (2:20,5; 44,84 MB) và cho Claude bên ngoài chạy AI mù (nhất là 1:20–1:25 người/bóng, 1:49–1:52 đèn tắt, 2:02–2:06 ô cửa hổ phách).
2. Chọn **A** (hướng mặt Ida), **B** (lỗi s35), **C** (ô cửa s43), **D** (cách đóng Cổng 5).
3. Xác nhận kết quả hiệu chuẩn (giữ tiêu chí cũ).
4. Duyệt characters v1.4 (A-α: cổ lộ, cổ áo bẻ thấp, khăn thấp, mũ ngồi thấp, tóc bạc + cách điệu shader) — đã khoá SHA theo chỉ đạo, chờ ghi nhận.
5. Duyệt cách tạm cho nền s06, s09w (nhoè ở khâu dựng thay cho lấy nét thật, tới Cổng 7).
6. Khiếu nại P0 (2 lần báo nhầm: mắt, hai dáng người) chờ K.
Cổng 5 **chưa merge**. Nhánh đã push.
