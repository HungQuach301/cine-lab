# CỔNG 5 · VÒNG v3 — CHỐT LAYOUT "Last Round" (theo quyết định chủ dự án sau Cổng 5 v2)

Nhánh: `claude/cine-lab-m2-cong5-layout-24o5fp`. **Chưa merge.** Claude bên ngoài chạy AI mù rồi chủ dự án duyệt merge.
Bản chốt:
- `design/cong5/layout/out/layout.mp4` và `screening/layout.mp4`: trùng từng byte, **44,84 MB**, SHA-256 `34f058a78a857989996330a8cbd17a702e1b66db082d3b7bcd370fc9e5e721dd`.
- 52 shot, **2:20,5 (3 372 khung)**, 960×540, 24 fps, phụ đề cháy.

## 0. Tóm tắt
- **Làm xong cả 7 việc chủ dự án giao (a–g).**
- **B-i:** kiểm toán C3 đạt. P kiểm riêng s35 khung 2148: render thẳng = render nối tiếp = bản nộp, 0 điểm ảnh lệch (v2 lệch 19 px).
- **Rà trạng thái ẩn cả 52 shot:** tìm thêm 2 lỗi cùng loại và đã sửa. Một là phơi sáng s05; hai là đèn lồng thắt lưng theo hướng của lần đặt trước, gặp ở s02, s07, s08, s15, s23, s26, s35.
- **Continuity lần 3: 0 lỗi chặn.** 3 lỗi nên sửa (N10–N12) đã sửa ngay trong vòng; phụ đề vắt qua cắt (G14) đã sửa.
- **Luật máy v1.4:**
  - Đạt 12/15 luật áp dụng, **P0 nay ĐẠT**.
  - Còn trượt 3 luật như v2, gốc đã biết: G3b grain, H1b track, C3 tỷ lệ mô hình. C3 có kiểm toán lại **đạt**.
- **Cổng 5 sẵn sàng đóng.**

## 1. Bảy việc: trước / sau (số đo thật)
| Việc | Trước (v2) | Sau (v3 chốt) | Người làm |
|---|---|---|---|
| a) B-i s35 thuần theo thời gian + rà trạng thái ẩn | Kiểm toán C3 **trượt**: s35 khung 2148 thân lệch 3,21 % điểm ảnh biên. Render thẳng khác nối tiếp 19 px | **Đạt**: kiểm toán khung 960 lệch 0. P đo riêng s35 f2148 thẳng / nối tiếp / bản nộp: 0 / 0 / 0 px ở cả 6 bộ phận. Rà 52 shot bằng so ảnh RGB (> 2/255) thẳng và nối tiếp: **0 px ở mọi shot sau sửa** | W1 (s01–s24c), W2 (s25–s48) |
| — nguồn 1: phơi sáng s05 khoá ở khung render đầu tiên | 25 919 px lệch | 0. Bản đầy đủ cũ trùng từng byte, nên không render lại | W1 |
| — nguồn 2: `util.makeChar().place` gọi `setPose` trước khi đặt gốc, đèn lồng theo hướng lần đặt trước | Lệch khung đầu: s02 28 px, s07 4, s08 307, s23 257, s26 299, s35 198 | 0. Sửa cục bộ `mkChar` trong shots_w1/shots_w2 (util.js không đổi). Render lại s02, s07, s08, s15, s23, s26, s35 | W1, W2 |
| b) C-i s43 máy đẩy chậm | Ô hổ phách lõi khoảng 5×9 px, máy gần như đứng | Trong 4 s: dolly 12 m + 28 → 45 mm. **Một** điểm vàng duy nhất lớn dần tới khoảng 8×20 px (continuity đo), gần giữa khung. Không thêm nguồn sáng | W2 |
| c) Câu "Just… keep a little dark for the ones who need it." bắt đầu trên Ida | Câu bắt đầu trên hình Cas (s38 1:41,6) | Thứ tự **s37w → s39 (Ida 1:41,6–1:46,0) → s38 (Cas 1:46,0–1:47,4) → s40**. Lời "Just…" bắt đầu 102,33 s, tức 0,74 s sau khi vào Ida. Phụ đề hiện từ f2453, trên hình Ida. Cắt sang Cas sau "for the ones", đúng ranh "ones / who". Tổng thời lượng và mốc thoại không đổi | W2 |
| d) Đồng hồ chỉ tiến | Cảnh 6: s45c 10:00 → s46 9:53, giờ lùi | Thứ tự **s45 → s46 (vặn 9:53 → 10:00) → s45c (10:00:00 → 10:00:01)**. Kim giờ ăn khớp kim phút (1/12). Mốc giờ ghi vào continuity (xem dưới) | W1, W2 |
| e) Người và bóng ở hốc vòm | — | Không sửa layout. Ghi vào PLAN.md cho Cổng 7: X = 2,0 | P |
| f) Continuity lần 3 + luật v1.4 + screening | — | Mục 3, 4 | P + agent rà |
| g) Báo cáo này, push | — | commit trên nhánh | P |

**Mốc giờ đồng hồ, đọc trên hình từng khung** (W1 đọc góc kim thật bằng móc chỉ đọc; W2 và agent rà đọc trên hình):

| Shot | Đồng hồ | Giờ | Số lần kim lùi |
|---|---|---|---|
| s06 | bỏ túi | 7:31:00 → 7:31:03 | 0 |
| s09 | quảng trường | 8:00:00 → 8:00:02 | 0 |
| s09w | bỏ túi | 7:53:00 → 7:53:02 | 0 |
| s45 | bỏ túi | chỉ thấy vỏ, sau sửa N12 | — |
| s46 | bỏ túi | 9:53 → khoảng 9:57 → 10:00 | 0 |
| s45c | quảng trường | 10:00 | 0 |

## 2. Sửa thêm sau continuity lần 3 (trong vòng)
| # | Lỗi | Sửa | Kiểm |
|---|---|---|---|
| N12 | Đồng hồ bỏ túi đổi hình qua cắt s45 → s46: vỏ vàng, khoen, mặt kem thành viền nâu dày | s45 đặt đồng hồ cùng vị trí và hướng như insert s46. Mô hình vốn đã chung; chỗ khác là cách đặt và ánh sáng | Ảnh trước/sau `reports/m2/cong5/w2/v5_N10-N12_s44-s45-s46-s45c.jpg` |
| N10 | s45: miệng ngõ sau lưng Ida nhưng bà ngẩng về máy, nên s45c không đọc ra POV | Trong 1,0–1,8 s bà quay đầu 50° và vai 20° về miệng ngõ, phía quảng trường. Máy lùi 1,75 → 2,0 m, đứng yên, cùng phía máy s44, không vượt trục | So ảnh thẳng/nối tiếp s45: 0 px. **Kiểm mù** 1 subagent, 4 khung s44 → s45 → s46 → s45c: đọc ra câu chuyện, giờ 10:00 → 10:00. POV "nghiêng về… góc nhìn của bà" nhưng "không chắc hẳn" (`reports/m2/cong5/kiem-mu-pov/POV-canh6.md`) |
| N11 | Sheet s37/s39/s45 lệch hình | Sửa `canh-5.md`, `canh-6.md` | — |
| G14 | Phụ đề vắt qua cắt: sub02 thừa 5 khung sang s23, sub07 thừa 4 khung sang s40 | `package.py`: nếu có cắt rơi trong 0,5 s cuối thẻ thì thẻ kết thúc đúng tại cắt. sub02 52,7 → 52,5 s, sub07 107,6 → 107,4 s; cả hai vẫn phủ hết lời (52,39 s; 107,05 s) | Đo trên layout.mp4: f1259 và f2577 có thẻ; f1260 và f2578 không có |

## 3. Continuity lần 3 (nguyên bản: `reports/m2/cong5/continuity-v3.md`)
Agent rà giải mã đủ 3 372 khung và so cả 51 chỗ cắt.
- **Lỗi lần 2:**
  - Đã đóng: C5 (lỗi chặn duy nhất), N2, N6, N7, N9.
  - N8: đóng phần chính; còn "điểm vàng chưa ra hình ô cửa", chuyển thành G16 → Cổng 7.
  - N3: đã cải thiện; phần còn lại chuyển thành G17 → Cổng 7 theo quyết định (e).
- **Mới:** N10, N11, N12 nên sửa và **đã sửa** (mục 2). G14 đã sửa.
- **Còn lại: chặn 0 · nên sửa 0 · ghi nhận 13.** Các mục G1, G2, G5/G6, G7–G13, G16, G17 thuộc Cổng 6 hoặc 7 và đã ghi vào PLAN.md.
- Agent rà chạy trên bản trung gian v4. Bản chốt v5 chỉ khác ở s45 (N10, N12, đã xem ảnh trước/sau và kiểm mù POV) và thời điểm tắt 2 thẻ phụ đề.

## 4. Luật máy (checks v1.4; không sửa, không đọc mã `checks/`)
`checks/run.py design/cong5/layout/out/layout.mp4 --profile shot` → `reports/checks/layout-cong5/`
```
[   PASS] N1  [   PASS] N2  [    N/A] N3  [   PASS] P0  [   PASS] P1  [   PASS] G4  [   PASS] G3
[   FAIL] G3b [    N/A] M1  [   PASS] M3  [   PASS] J1  [   PASS] J1b [   PASS] H1  [   FAIL] H1b
[   FAIL] C3  [   PASS] O3                                                     VERDICT: TRƯỢT
```
- **P0 ĐẠT:** 0 vùng chữ không có matte. v2 trượt vì báo nhầm "MA" ở khung 1980. Khiếu nại P0 vẫn để trong `checks-appeal.md` chờ K.
- **C3:**
  - Kiểm toán **đạt**: hạt giống `13835408031386974546`, khung 960; lệch điểm ảnh 0, views lệch 0°.
  - Phần tỷ lệ **không đổi so với v2**: 51 mẫu trượt chắc chắn, 47 không chứng minh được, biên trên lớn nhất 36,35 %, khớp biên thấp nhất 0,749 (≥ 1,5 ✗), 22 shot CẦN NGƯỜI XEM. Gốc vẫn như Cổng 4/5: tư thế và góc layout so với 8 góc sheet, ví dụ s02 thân +7 đến +15 % ở góc −45° (khung 96–168).
  - Yêu cầu kiểm toán cũ huỷ vì video đổi; lưu trong `reports/m2/cong5/c3-kiem-toan/` (`request_v2-cuoi.json` trượt s35; `request_v3-trung-gian.json` khung 252, 756, đạt).
- **G3b:** σ nhỏ nhất 0,718 (≥ 0,8 ✗), σ lớn/nhỏ 3,0 (≤ 1,3 ✗), tương quan khung kề 0,83 (≤ 0,5 ✗). Layout chưa có khâu grain; việc của Cổng 7.
- **H1b:** track tệ nhất 25 % (≥ 90 ✗), 5 track toàn null. Như v2; chuyển động layout còn thô, việc của Cổng 6.
- **Chỉ số trong ±5 % quanh ngưỡng:**
  - C3 hệ số mặt nạ 4,0 (ngưỡng ≤ 4,0).
  - C3 hệ số khi đầu < 100 px 4,0 (ngưỡng ≥ 3,98).
  - P tự nêu thêm: s23 mặt vôi 18,5 % (mức khoảng 20 %), không đổi.

## 5. Số liệu thời gian và token (vòng v3, 09:21 → 13:05 UTC, khoảng 3 giờ 45 phút đồng hồ)
**Hàng đợi** (`reports/m2/cong5/queue-log.tsv`, từ 09:20, không tính W3):

| Gói | Việc | Chờ | Chạy | Nội dung |
|---|---|---|---|---|
| W1 | 3 | 0 s | 1 376 s | render lại 5 shot (360 khung, 964 s, 2,59 s/khung do máy dùng chung), 2 lượt mặt nạ thẳng/nối tiếp |
| W2 | 41 | 1 926 s | 5 099 s | 32 lô so mặt nạ (làn nhanh), 3 lượt so RGB, render 7 shot (488 khung, 932 s) + s45 (48 khung, 73 s) |
| P | 12 | 1 436 s | 3 764 s | trộn âm, 2 lượt ghép + đóng gói + mặt nạ C3 (857 s mỗi lượt) + kiểm toán + luật (482–486 s) |

Chờ của P chủ yếu do W3 giữ làn nặng lúc render clip (572 s và 796 s). 12 việc bị gắn QUA-60S trong toàn bộ log (W2/W3 làn nhanh khi máy dùng chung).

**Token** (số công cụ báo khi agent kết thúc lượt, là kích thước ngữ cảnh tích luỹ, không phải số tiêu thụ):

| Agent | Token | Thời gian | Lượt |
|---|---|---|---|
| W1 v3 | 688 878 | 56 phút | 1 |
| W2 v3/v4 (a–d + util) | 393 061 | 2 giờ 1 phút | 1 |
| W2 v5 (N10–N12) | 419 122 | 10 phút | 1 |
| cine-continuity lần 3 | 222 328 | 18 phút | 1 |
| Kiểm mù POV cảnh 6 | 49 075 | 40 s | 1 |

(Gói cửa mặt A-i báo riêng trong `reports/m2/MAT-IDA-AI.md`.) **Hạn mức gói Claude:** P không đo được; cần ảnh usage mới của chủ dự án.

## 6. Quyết định cần chủ dự án
### A. Đóng Cổng 5
| | A1 — Đóng như bản này (khuyến nghị) | A2 — Làm thêm một vòng trước khi đóng |
|---|---|---|
| Ưu | Đủ 7 việc; 0 lỗi continuity chặn; kiểm toán C3 đạt; P0 đạt. Các trượt còn lại (G3b, H1b, C3 tỷ lệ) có gốc đã biết, thuộc Cổng 6/7 | Có thể xử lý sớm các mục ghi nhận (G7 màu mũ, G16 ô cửa) |
| Nhược | 13 mục ghi nhận chuyển sang Cổng 6/7 | Tốn thêm 1 vòng; các mục này phụ thuộc hoạt hoạ và ánh sáng cuối, làm ở layout dễ phải làm lại |
| Tác động | Claude bên ngoài chạy AI mù; chủ dự án duyệt merge vào main | Dời mốc |
| Rủi ro | Thấp. Cổng 6 vẫn khoá cho tới khi có lời giải mặt Ida (MAT-IDA-AI) | Làm lại |

### B. POV cảnh 6 (s45 → s46 → s45c)
Kiểm mù đọc ra "nghiêng về góc nhìn của bà" nhưng "không chắc hẳn", vì thiếu cảnh phản ứng sau POV và nền s45 sáng trắng trong khi s45c trời đen.
- **B1 (khuyến nghị):** giữ layout; ở Cổng 6 cho bà nhìn rõ hướng (mắt và đầu) và làm đồng hồ trong tay đọc rõ. Tổng thời lượng không đổi.
- **B2:** thêm 0,5–1 s cảnh phản ứng của Ida sau s45c. Rõ POV hơn, nhưng đổi tổng thời lượng và mốc nhạc, phải trộn và kiểm lại.
- **B3:** chấp nhận s45c là cảnh chèn.

## 7. Việc đang chờ chủ dự án
1. Chọn A (đóng Cổng 5) và B (POV cảnh 6); cho Claude bên ngoài chạy AI mù trên `screening/layout.mp4`, rồi duyệt merge.
2. Quyết định cửa mặt Ida (báo cáo riêng `reports/m2/MAT-IDA-AI.md`). Cổng 6 chỉ mở khi có lời giải.
3. Khiếu nại P0 chờ K (không còn chặn, vì P0 đã đạt ở bản này).
4. Ảnh usage gói Claude, nếu muốn đo hạn mức vòng này.
