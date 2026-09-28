# CỔNG 5 — LAYOUT "Last Round" (M2)

Phiên P · nhánh `claude/cine-lab-m2-cong5-layout-24o5fp` · 28/09/2026 · **KHÔNG merge Cổng 5.** Đang DỪNG, chờ chủ dự án duyệt.

## 0. Tóm tắt
- **Layout xong:** 52 shot, **2:22,5** (3 420 khung, không lệch so với animatic v2), 960×540, 24 fps, bối cảnh và máy bản cuối. `screening/layout.mp4` **45,48 MB**, phụ đề tiếng Anh cháy vào hình, âm tạm; sao y từng byte `design/cong5/layout/out/layout.mp4` (SHA `25d67d1d…`).
- **V1–V4 đã sửa** (mục 2). D2 mũ #262a33 đã vào sheet v1.3 và vào hình.
- **Cổng mặt Ida: CHƯA ĐẠT.** A1 trượt (kiểm mù lần 4), A3 trượt (lần 5) cùng một tiêu chí "mặt nạ/búp bê/ma-nơ-canh/con rối", 3/3 ảnh mỗi lần. Theo chỉ đạo: dừng, không hạ tiêu chí, báo kết quả (mục 3). Layout dùng mặt A1.
- **Continuity:** rà toàn phim tìm 4 lỗi chặn + 5 nên sửa; đã sửa 3 chặn + 5 nên sửa, render lại 8 shot. **Còn 1 lỗi chặn (C2) cần chủ dự án chọn** (mục 4).
- **Luật v1.4 trên video ghép (lần 3, bản cuối):** TRƯỢT — đạt 11, trượt G3b, H1b, C3; 2 N/A. Kiểm toán C3 ĐẠT (lệch 0 điểm ảnh). P0 lần 1 trượt vì máy dò đọc mắt Cas thành "56" → đã khiếu nại K; P tự tìm và sửa một lỗi bộ xuất mặt nạ C3 của chính P (s27 rỗng) (mục 5).
- **Quyết định sớm của chủ dự án** (cuối phố nhà kho chữ L, kéo mũ lại khi rời đi, không quầng chân trời) đã vào phim, AUTHORSHIP và world-rules v0.5.

## 1. Tổ chức và số liệu thời gian (số đo thật)
3 gói, 3 subagent cine-worker, mỗi gói một worktree; P giữ phần chung và là người duy nhất ghép. File chia theo gói (`design/cong5/layout/`): W1 `shots_w1.js`, `order_w1.js`, `sets.js`; W2 `shots_w2.js`, `order_w2.js`, `sets2.js`, `sets_end.js`; W3 `design/cong3/v2/char3d/*`, `facelight.js`; P `common.js`, `film.js`, `page.js`, `render_film.js`, `assemble.py`, `package.py`. Không có xung đột merge nào.

**Hàng đợi render nặng** `scripts/render/queue.sh` (flock, mỗi lúc 1 việc nặng; nhật ký `reports/m2/cong5/queue-log.tsv`, 54 việc):

| Gói | Việc nặng | Chờ hàng đợi | Chạy thật |
|---|---|---|---|
| W1 | 5 | 2 232 s | 2 037 s |
| W2 | 4 | 1 562 s | 3 361 s |
| W3 | 29 | 3 900 s | 1 609 s |
| P | 16 | 0 s | 3 941 s |
| **Tổng** | 54 | 7 694 s | **10 949 s (3 giờ 02 phút máy)** |

- Render đầy đủ lần đầu: 3 420 khung trong 4 654 s chạy (**1,36 s/khung**, 1 tiến trình; animatic v2 là 2,1 s/khung/tiến trình khi chạy 3 tiến trình song song).
- Render lại: 636 khung / 744 s (s08, s23, 7 shot sửa continuity) → hệ số làm lại khung **×1,19** (animatic v2: ×1,33).
- Ghép 145–150 s; đóng gói 2 pass 225–228 s; mặt nạ C3 4× (285 khung) 652–694 s (3 lần); luật máy 374–402 s mỗi lần (3 lần).
- Hàng đợi không chia lượt theo thứ tự đến (W3 báo): ảnh tĩnh 20 s của W3 có lúc chờ 1 956 s sau render cả cảnh. Lần sau nên dùng hàng đợi có thứ tự (ticket) hoặc làn riêng cho việc < 60 s.

**Thời gian từng gói** (thời gian agent làm việc, theo đồng hồ):

| Gói | Giai đoạn | Thời gian | Làm lại |
|---|---|---|---|
| W1 | A layout + probe (68 lượt shot, 204 khung) | 40 phút | — |
| W1 | C render đầy đủ + đối chiếu cột điện + đo mặt vôi s23 | 88 phút | 1 (s08: ô cửa lơ lửng) |
| W1 | D sửa N1 (Cas ở s23) | 4 phút | 1 |
| W2 | A layout + V1–V4 (17 lần probe, 135 lượt shot) | 81 phút | — |
| W2 | C render đầy đủ + cử chỉ kéo mũ | 75 phút | 0 |
| W2 | D sửa continuity C1, C3, C4, N2–N5 | 16 phút | 7 shot |
| W3 | A1 (cổ áo, nếp mũi–má, facelight) | 59 phút | ảnh nộp render 3 lần; 9 vòng cổ áo, 4 vòng facelight |
| W3 | A3 (nửa dưới mặt) | 98 phút | ảnh nộp render 2 lần; 6 vòng đầu, 4 vòng cổ áo |

Đồng hồ toàn cổng: giao việc 23:54 → báo cáo 04:35 (≈ 4 giờ 40 phút).

## 2. V1–V4 trước / sau
| Lỗi | Nguyên nhân tìm được | Sửa | Sau (bằng chứng) |
|---|---|---|---|
| **V1** 2:00 (s42b/s42) Cas mất mũ len, tay to, ngồi xổm méo | Mũ KHÔNG rơi. Máy chính diện thấp 0,72 m, đèn lồng giữa máy và Cas; mặt và mũ ngoài nón sáng (nắp chắn tia > 49°) nên mũ kem chỉ nhận ánh dội, quả bông khuất sau đỉnh đầu → đọc "tóc vàng". Lòng bàn tay gần máy hơn đầu 0,4–0,5 m → tay to | Cas quay mặt ra vòm; máy sau lưng lệch phải, lùi 2,3 m, 40 mm. Ida trái, Cas phải. Không đổi tỷ lệ tay 1,30× | Mũ len và quả bông in trên nền phố trắng; tay đúng cỡ (`reports/m2/cong5/w2/V1_s42b-s42_truoc-tren_sau-duoi.jpg`). Rà continuity: đạt phần chính; còn thân dưới dáng xổm thành một khối tối, chỉ thấy một tay hơ |
| **V2** 1:28 (s33–s34) người và bóng lẫn nhau | Cas sát vách 0,45 m: bóng ×1,18 lệch 0,06 m (gần như sau lưng) | Chỉ quang học: đèn lồng (−0,05; 3,0 m từ vách); Ida cách vách 1,45 m → bóng ×1,94 (≈ 3,2 m), vành mũ của bóng hiện, lệch trái 0,53 m; Cas 0,8 m → ×1,36 (≈ 1,8 m), lệch phải. **Bóng bà cao gấp 1,77 bóng cậu.** Bóng mềm (nguồn ~12 cm). s34 26 mm thấy nền: bóng nối chân mỗi người | `D_N3-N4_s33-s34.jpg`. Còn rủi ro: s33 Ida chồng 0,15 m lên mép bóng; cần AI mù xác nhận hết "hai cậu bé" |
| **V3** cuối phố tường trống (0:52 s23, 1:04 s27, 1:40 s37w) | Cuối phố là một mặt phẳng vôi 24 × 11 m | Nhà kho chữ L có mái, máng, chòi thông gió, cửa kéo, cửa sổ cao; tường chim là hông nhà kho có hốc vòm; phố rẽ trái, dốc 5 %; nhiều lớp mái xa, sương. Phố chính (W1): lớp nhà sau dâng theo dốc 3,5 %, quảng trường có nhà bao, 5 dãy nhà xa | Mặt vôi s23: **29,4 % → 15,5 %** khung (đo bằng mặt nạ). `V3_s27-s35-s37w_…jpg`. Chủ dự án đã duyệt (v0.5) |
| **V4** 1:02 (s26) mặt Ida tối, mắt ánh cam | L11 sau-bên bà 1,9 m, ngẩng 40° → vành mũ che hết mặt; đèn lồng thắt lưng chỉ bắt vào tròng mắt | Ida dời tới cách L11 3,5 m, L11 gần chính trước mặt (ngẩng 25°); máy 3/4; `facelight.js` 'gas'; phơi sáng 3,4 | Mặt đọc là bà cụ đội mũ, hết mắt tự sáng (`V4_s26_…jpg`) |
| **D2** mũ #262a33 | — | Sheet v1.3, khoá SHA | s40 cùng khung: dưới lửa **#5a3f39** (nâu xám), sau khi tắt **#1b1e2c** (đen xanh). Ngoại lệ: s36, s05 đèn khí cách 0,5 m vẫn nâu cam (#471d0d, #57260e) — ghi cho Cổng 7 |

Sửa thêm khi layout (không ai yêu cầu, phát hiện trên probe): s28 chim còn xám trái luật 3.3; s30–s32 vỏ đèn lồng tự che ngọn lửa; s38 tay Cas lơ lửng; s45 không thấy đồng hồ; s47 đèn lồng còn ở hông sau khi đã trao; s48 chim lẫn vào bóng người; s15 hai cái thang; s22 nhịp xoè tay vô lý; s05 máy trôi theo đầu.

Quyết định sớm của chủ dự án đã vào hình: **kéo mũ lại khi rời đi** ở cuối s42 (1,9–2,2 s tay lên vành; 2,2–2,8 s `hat_back` 0,35 → 0; quay người đi) — góc mũ liền mạch s36 (đẩy) → s37…s42 (0,35) → cảnh 6 (0), continuity cảnh 5–6 có bảng `hat_back` đầu/cuối từng shot; rà continuity xác nhận đạt. **Không quầng chân trời:** độ sáng trời sát chân trời s10 23,4 · s12 42,9 · s19 31,1 · s23 35,4 (luma 0–255); s43 sửa từ trời xám lilac RGB (85, 98, 137) → (13, 25, 68) có sao.

## 3. Cổng mặt Ida — KHÔNG ĐẠT sau A1 và A3
Mỗi ảnh gửi một subagent MỚI không ngữ cảnh, chỉ mở một file, câu hỏi: "Người này bao nhiêu tuổi, giới tính gì, đang cảm thấy gì? Nêu thêm điều gì người xem có thể thấy lạ trong ảnh (nếu có)." Nguyên văn đầy đủ: `reports/m2/cong5/kiem-mu-mat/lan4.md` (A1), `lan5.md` (A3).

| Tiêu chí (chủ dự án) | Lần 4 — A1 | Lần 5 — A3 |
|---|---|---|
| Cả 4 ảnh đọc ra phụ nữ lớn tuổi | 3/3 "bà cụ" 65–80, chắc chắn | 3/3 nói nữ nhưng 2/3 do dự ("che bông tai thì hơi giống đàn ông"; "không có hoa tai có thể đoán là ông cụ") |
| ≥ 3/4 cảm xúc đúng | đạt ở 3 ảnh | đạt ở 3 ảnh |
| KHÔNG ảnh nào "mặt nạ/búp bê/con rối/ma-nơ-canh" | **TRƯỢT 3/3** | **TRƯỢT 3/3** |
| Ảnh 4 (khung chính diện câu thoại cuối, s39) | không gửi — không thể đổi kết luận | không gửi — như trên |

Câu then chốt (nguyên văn):
- A1 h5: "Mặt giống một cái trứng hay chiếc mặt nạ nhẵn thuôn nhọn xuống cằm… trông giống ma-nơ-canh hay búp bê hơn là mặt người."
- A1 r2: "khuôn mặt như một chiếc mặt nạ phát sáng, cộng với chỗ nối giữa mặt, cổ và cổ áo trông không tự nhiên."
- A1 t8: "khuôn mặt tự phát sáng, không có cổ và đầu hình trứng dễ gây cảm giác 'búp bê hoặc mặt nạ'."
- A3 p3: "Đầu như cắm lên một cái cổ áo tròn cứng, trông giống búp bê hoặc ma-nơ-canh hơn người thật."
- A3 k9: "tỷ lệ đầu với cổ, vùng cằm và cách gắn tóc và hoa tai khiến nhân vật trông giống búp bê hay mặt nạ."
- A3 d6: "Không có cổ. Đầu to, cằm chạm thẳng vào cổ áo xanh, trông như đầu đặt lên cổ áo, giống con rối."

Đọc kết quả:
- A3 sửa được ánh sáng (điểm cháy mặt 2 % → 0 %; mặt/khung 26× → 2×; "tự phát sáng" còn 1/3) nhưng nửa dưới mặt mới bị chê "to, xệ, lệch, tan chảy" (3/3) và làm **giới tính yếu đi**. Vì vậy layout giữ **A1**; mã A3 lưu ở `reports/m2/cong5/w3/a3-ma-nguon.patch`.
- Lời chê lặp lại qua cả lần 3, 4, 5: **đầu cắm lên cổ áo, không thấy cổ** và **nếp nhăn vẽ nét trên da nhẵn như sáp**. Hai điều này nằm ở gốc cách dựng C′ (mặt vẽ tay trên texture phủ đầu 3D; cổ 0,30 H; cổ áo dựng cao che cổ), không nằm ở một chi tiết nào sửa được trong phạm vi A1/A3. Đây là nhận định của P, chưa kiểm bằng thử nghiệm.
- Chưa khoá: `IDA_WISPS='temple'` làm tỷ lệ 0° đo được giảm 3,0 % so với `c3_views` (chưa cập nhật sheet — chờ quyết định mặt; C3 có thể cờ oan ở góc chính diện vì lý do này). Cổ áo A1 cần câu chữ bible v1.4 nếu giữ.

## 4. Continuity (agent cine-continuity, 156 khung + phóng to; `reports/m2/cong5/continuity.md`)
| Mã | Mức | Lỗi | Xử lý |
|---|---|---|---|
| C1 | chặn | s27: thang biến mất khỏi L11 | **Đã sửa** (W2): thang tựa phía bắc L11 như bộ phố |
| C2 | chặn | Góc tường chim trắng từ 1:04,4 (cột phố chính bật), nhưng s35–s37w cùng góc lại tối, có bóng dài. Cột (13,5; −4,2) chỉ cách L11 ~5,6 m, trái luật v0.4 "ngoài tầm vũng sáng ~20 m" | **Chờ chủ dự án** (quyết định B) |
| C3 | chặn | s41, s42a nhảy trục 180° (Cas trái, Ida phải) | **Đã sửa**: Ida trái, Cas phải như s40w, s42 |
| C4 | chặn | s43 trời xám lilac sáng, không sao | **Đã sửa**: trời đêm có sao, không quầng |
| N1 | nên sửa | s23 thiếu Cas ở chân tường (s24 có) | **Đã sửa** (W1): s23 không hề dựng Cas → thêm |
| N2 | nên sửa | s42a ôm đèn, s42b chìa xa | **Đã sửa**: ôm sát ngực bằng hai tay s41–s42b |
| N3 | nên sửa | V2 chưa trọn (s33 chồng, s34 bóng Cas quá sắc) | **Đã sửa** (mục 2) |
| N4 | nên sửa | s33 cột gang lạ cạnh vòm (bộ khoá Cổng 3) | **Đã sửa**: ẩn trong lớp bọc |
| N5 | nên sửa | continuity sheet ghi khác hình (5 chỗ) | **Đã sửa** canh-4, canh-5, LAYOUT-W2 |

Chỗ nối W1 ↔ W2 (s24 → s24c → s25 → s26): **khớp** (Cas ở chân tường, nhìn trái; Ida xuống thang ngoài hình; đèn lồng hông trái; cột phố chính tắt đúng lịch). Chưa chạy lại toàn bộ rà sau khi sửa; P đã tự xem 8 khung sau sửa (s23, s26, s27, s34, s41, s42, s43, s39).

## 5. Luật máy (checks v1.4, không sửa `checks/`, không đọc mã `checks/`)
Chạy 3 lần trên `design/cong5/layout/out/layout.mp4` (`/opt/cine/bin/python checks/run.py … --profile shot` → `reports/checks/layout-cong5/`):
- Lần 1 (trước sửa continuity): P0 TRƯỢT (báo nhầm, dưới đây).
- Lần 2 (sau sửa continuity, video mới SHA `25d67d1d…`).
- **Lần 3 (bản cuối, cùng video)** sau khi P sửa lỗi bộ xuất mặt nạ C3 (mục 5.1):
```
[   PASS] N1 24 fps CFR; không rơi hay lặp khung theo PTS
[   PASS] N2 BT.709 đủ 3 trường; dải limited — đo cả nhãn lẫn giá trị điểm ảnh
[    N/A] N3 Codec và bitrate đúng loại master; khung 16:9, SAR 1:1
[   PASS] P0 Máy dò chữ độc lập: mọi chữ trong hình phải có matte
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
- **P0:** lần 1 vùng duy nhất là **mắt + lông mày Cas** ở s42a (khung 2775) đọc "56", độ tin 0,84 (ngưỡng 0,8 — sát ngưỡng). Không có chữ nào trong hình. Khiếu nại đã ghi `checks-appeal.md` (ảnh `reports/m2/cong5/khieu-nai/P0_khung2775_s42a.jpg`). Lần 2–3 ĐẠT vì khung s42a đổi khi sửa trục 180° (lý do dàn dựng, không phải để lách).
- **G3b:** σ nhỏ nhất 0,733 (≥ 0,8 ✗), CV lớn nhất 0,242 (≤ 0,2 ✗), σ lớn/nhỏ 2,868 (≤ 1,3 ✗), tương quan khung kề 0,828 (≤ 0,5 ✗). Cùng gốc Cổng 4: lớp vẽ giữ cấu trúc giữa các khung; chưa xử lý ở layout.
- **H1b:** track tệ nhất khớp 33,3 % (≥ 90 ✗); 2 track toàn null. Cùng gốc Cổng 4 (tư thế previs).
- **C3:** kiểm toán lần 3 **ĐẠT** (hạt giống `2226881257325565179`, khung 2964, 3276; lệch điểm ảnh 0; views lệch 0°/0). Hai lần trước bị huỷ trước khi đối chiếu, hạt giống lưu `reports/m2/cong5/c3-kiem-toan/`: lần 1 `5864998127796708074` (video đổi sau sửa continuity), lần 2 `12016497369048562390` (P sửa bộ xuất mặt nạ). Đo: 44 mẫu trượt chắc chắn, 76 không chứng minh được, biên trên |lệch| + U lớn nhất 38,27 %, độ khớp biên thấp nhất 0,65 (≥ 1,5 ✗), **20 đoạn CẦN NGƯỜI XEM** (19 shot). Mẫu trượt tập trung ở shot đi/vác thang (s02, s07, s19), Cas–Ida gần (s32, s42, s42a).
- **Chỉ số trong ±5 % quanh ngưỡng:** C3 hệ số mặt nạ 4,0 (ngưỡng tối đa 4,0); C3 hệ số khi đầu < 100 px 4,0 (ngưỡng 3,98); lần 1: P0 độ tin 0,84 (ngưỡng 0,8), G3b CV 0,205 (ngưỡng 0,2); shot mẫu s42: G3b tương quan 0,521 (ngưỡng 0,5).

**Từng shot mẫu** (clip cắt từ video ghép, không file đi kèm → các luật cần file đi kèm báo THIẾU; `reports/checks/layout-cong5-mau/`): s05 (cận mặt), s33 (hốc cửa): N1, N2, P0, G3, **G3b ĐẠT**. s42 (V1): N1, N2, P0, G3 đạt; **G3b TRƯỢT** — tương quan khung kề **0,521** (ngưỡng ≤ 0,5, sát ngưỡng), CV 0,184.

### 5.1 C3 — tờ so sánh cho người xem (Q-C3r B) và 3 shot bị cờ ở v2
Agent cine-continuity lập `reports/m2/cong5/c3-nguoi-xem/BANG.md` (21 ảnh so sánh + 4 ảnh phủ mặt nạ). **Chủ dự án chỉ cần xem 3 shot CỜ:**

| Shot | Cổng 4 v2 | Layout Cổng 5 | Còn cờ? |
|---|---|---|---|
| **s08** | cẳng tay +19,1 % | +21,5 / +17,5 / +19,3 % ở 3 khung hợp lệ (+14…+18 % sau hiệu chỉnh đầu). Hình gần như y hệt Cổng 4; bằng mắt vẫn đúng dáng | **Còn cờ** |
| **s27** | thân −12,3 % | Lúc đầu mặt nạ rỗng dù Ida cao ~130 px → **lỗi bộ xuất của P** (vật che tô đen hai mặt; máy đặt sau một mặt phẳng một mặt). Đã sửa. Sau sửa: thân −5,7 %, tay trên −5,1 %, cẳng tay −6,0 % ("không chứng minh được"); 1 mẫu cẳng tay −11,1 % ở khung 1536 | **Cờ nhẹ** (lệch giảm một nửa) |
| **s47** | thân +16,2 %, cẳng tay +17,5 % | Chỉ khung 3252 (thân +16,7 %, cẳng tay +16,4 %; đầu nhìn từ sau chỉ còn dải 29×15 px); 3 khung sau trong ±4,1 % | **Cờ nhẹ** — agent khuyến nghị chấp nhận nếu ảnh đúng dáng |

- **Không cờ: 19/20 đoạn** (thân cắt mép, bộ phận che/gập, đầu co ngắn, góc lệch > 30°). Mũ, khăn, hoa tai, cổ áo, váy khớp bible v1.3. s34 số thô thân +36 % nhưng đầu chỉ là vệt 89 px cạnh bàn tay che mặt → không dùng làm chuẩn được, không cờ.
- **So với Cổng 4:** hết cờ 6 shot (s03, s04, s05, s36, s37, s39 — cả nhóm màu mũ, nhờ D2). Không cờ mới. Để biết: ở s05, s36, s40 mũ dưới đèn khí sát mặt đọc **nâu cam**, sáng hơn áo — vượt mô tả "nâu xám" của D2 (xử lý ở Cổng 7 bằng ánh sáng, hoặc chủ dự án xác nhận).
- Giới hạn: danh sách lý do loại của máy bị cắt ở 300 mục (tới khung 2196); lý do cho 8 đoạn sau đó agent suy từ `views`.

## 6. Quyết định cần chủ dự án

### A. Cổng mặt Ida chưa đạt sau A1 và A3 (chặn Cổng 6)
| | **A-α — Vòng thiết kế lại vùng mặt–cổ theo hướng cách điệu (khuyến nghị)** | A-β — Bỏ C′ cho mặt: mặt điêu khắc hình khối đầy đủ + rig biểu cảm | A-γ — Đổi cách kiểm |
|---|---|---|---|
| Làm gì | Giữ C′ (mặt vẽ trên đầu 3D) nhưng: lộ một đoạn cổ thật (cổ áo thấp, mở; khăn quàng thấp), đổi tỷ lệ cổ trong sheet; bớt tả thực trên mặt (ít nét nhăn vẽ, khối má–hàm đơn giản, chất da có sắc độ thay vì nhẵn sáp); mỗi bước kiểm mù 1 ảnh để lái | Khắc nếp nhăn, khe môi, cằm, cổ vào hình học; biểu cảm bằng biến dạng lưới; cần rig miệng (cũng cần cho khẩu hình Cổng 6) | Kiểm trên clip chuyển động trong phim và/hoặc người xem thật thay cho ảnh tĩnh subagent |
| Ưu | Đánh đúng hai lời chê lặp lại qua lần 3–5 ("đầu cắm lên cổ áo", "nét vẽ trên da sáp"); giữ đường ống hiện có | Giải quyết gốc "nét vẽ trên sáp"; có sẵn khẩu hình cho Cổng 6 | Nhanh |
| Nhược | Đổi thiết kế đã khoá (trang phục cổ, tỷ lệ cổ) → characters v1.4, đo lại B1; vẫn có thể trượt | Đảo quyết định C′ của chủ dự án ở Cổng 3; lâu nhất | Là **nới tiêu chí** — chỉ chủ dự án được quyết; có thể che lỗi thật |
| Tác động | 1 vòng thiết kế + kiểm mù 4 ảnh; render lại ~20 shot có mặt Ida cỡ MS trở lên (~30 phút máy, số đo 1,36 s/khung) | Lùi Cổng 6; phải khoá lại sheet và model sheet ảnh | Không render thêm |
| Rủi ro | Trung bình | Thấp về kết quả, cao về lịch | Cao về chất lượng phim |

### B. Lỗi continuity C2 còn chặn: góc tường chim sáng từ 1:04 nhưng cùng góc tối ở cảnh 5
Gốc: cột phố chính (bật 1:04,4) chỉ cách L11 ~5,6 m trong địa lý chốt, trái luật v0.4 "góc ngọn 11 ngoài tầm vũng sáng (~20 m)". Phương án (W2 soạn, thời gian theo s/khung đo thật, chưa kể chờ):

| | **B1 — Cột vào sân trước hông nhà kho, tầm sáng ngắn (~6 m); dời chỗ Cas sang đông 4 m (khuyến nghị)** | B2 — Chấp nhận góc sáng từ 1:04 (luật v0.6) | B3 — Dời tường chim + Cas sang tây hốc cửa |
|---|---|---|---|
| Ưu | Giữ luật v0.4 và nhịp "…brighter now" (góc chuyển tối → trắng đúng câu thoại — chỉ đạo của chủ dự án ở Cổng 4) | Rẻ nhất | Góc L11 xa cột > 10 m |
| Nhược | Cas cách L11 6,4 m (mức W1 đặt ≤ 5 m), mặt Cas ở s24c tối hơn | Mất tương phản hổ phách trong lời từ biệt; đụng chỉ đạo 1:50 của chủ dự án | Hỏng s24c; đổi bố cục khung chuẩn b_cas_bird |
| Tác động | Render lại s24, s24c, s25–s32, s35–s42a (~1 470 khung ≈ 40 phút máy) + rà continuity lại | s35–s37w (350 khung ≈ 8 phút) + sửa luật | s23–s24c, toàn cảnh 4, s33–s35 (≈ 45–50 phút); rủi ro nối lớn nhất |
| Rủi ro | Thấp | Trung bình (kể chuyện) | Cao |

### C. Đóng Cổng 5
| | C1 — Duyệt layout ngay, C2 sửa theo B trong Cổng 6 | **C2 — Chọn B, P render lại + rà lại continuity + chạy AI mù ngoài trên `screening/layout.mp4` mới, rồi đóng (khuyến nghị)** | C3 — Làm lại layout một phần theo góp ý khi xem |
|---|---|---|---|
| Ưu | Nhanh | Đóng với 0 lỗi continuity chặn; AI mù xác nhận V2 ("hai cậu bé") trên bản cuối | Chủ dự án chỉnh bố cục trước khi khoá |
| Nhược | Mang lỗi chặn sang Cổng 6 | Thêm ~1 giờ | Lâu hơn |
| Tác động | — | ~40 phút máy + rà | Tuỳ góp ý |
| Rủi ro | Trung bình | Thấp | Thấp |

Việc nhỏ cần duyệt (ghi PLAN.md):
1. Đèn lồng cháy sẵn từ s02 (như v2) hay mồi ở L4 như kịch bản (0:12)? (W1) — P khuyến nghị theo kịch bản: mồi ở L4, thêm một nhịp tay ở s03/s04 ở Cổng 6.
2. Duyệt máy mới s02 (nhìn chéo lên phố) và s15 (nhìn xuôi dốc; hết lỗi hai cái thang). (W1)
3. Lọn tóc thái dương 'temple' (đang dùng; làm tỷ lệ 0° đo được giảm 3,0 % so với `c3_views`) và câu chữ cổ áo A1 cho bible v1.4 — nên quyết cùng A.
4. Mũ nâu cam dưới đèn khí sát mặt (s05, s36, s40) có nằm trong ý D2 không, hay để Cổng 7 hạ.
5. Khiếu nại P0 (máy dò đọc mắt nhân vật thành chữ) — chuyển K.
6. Quy trình: hàng đợi render nên có thứ tự/làn nhanh cho việc < 60 s (ảnh tĩnh W3 có lúc chờ 1 956 s).

## 7. Việc đang chờ chủ dự án
1. **Xem `screening/layout.mp4`** (2:22,5; 45,48 MB; trên nhánh `claude/cine-lab-m2-cong5-layout-24o5fp`) và cho Claude bên ngoài chạy AI mù.
2. **Chọn A** (mặt Ida), **B** (C2 góc sáng), **C** (cách đóng Cổng 5).
3. Xem 3 shot C3 cờ: **s08, s27, s47** (ảnh trong `reports/m2/cong5/c3-nguoi-xem/`).
4. Duyệt 6 việc nhỏ ở mục 6.
5. Phán quyết khiếu nại P0.
Cổng 5 **chưa merge**. Nhánh đã push.
