# CỔNG 4 · VÒNG SỬA v2 — Animatic "Last Round"

Phiên P · nhánh `claude/cine-lab-m1-cong4-animatic` · 27/09/2026 · **KHÔNG merge Cổng 4.** Đang DỪNG, chờ chủ dự án duyệt.

## 0. Tóm tắt
- **Animatic v2:** 52 shot, **2:22,5** (142,5 s; v1: 2:30, 48 shot). Có phụ đề tiếng Anh cháy vào hình. `screening/animatic.mp4` nặng **45,49 MB** (< 50 MB), sao y từng byte bản chạy luật (`design/cong4/animatic/out/animatic.mp4`, SHA `43d64a2b…`). Lời thoại giữ nguyên văn.
- **Kịch bản nháp 3, luật thế giới v0.4, characters v1.2** đã ghi. Ba chỉ đạo của chủ dự án đã vào phim (mục 3).
- **Luật máy trên bản chạy luật:** TRƯỢT. Đạt 11 luật; trượt G3b, H1b, C3; 2 luật N/A.
  - C3 lần đầu có đủ dữ liệu (mặt nạ 4× + `views` + kiểm toán). Kiểm toán ĐẠT: lệch 0 điểm ảnh, views khớp. Nhưng 68 mẫu trượt chắc chắn, 63/196 khung khớp biên dưới 1,5, và 21 shot CẦN NGƯỜI XEM.
- **Cổng mặt lần 3:** đạt tuổi, giới và cảm xúc ở 3 ảnh biểu cảm. **TRƯỢT** tiêu chí "không mặt nạ/búp bê": 3/4 ảnh bị gọi "giống mặt nạ" hoặc "cổ ma-nơ-canh… búp bê". Ảnh thứ 4 (khung animatic) còn do dự về giới.
- **AI mù v2:** hiểu truyện đúng (đêm, đèn điện thay đèn khí, bà tắt ngọn cuối, trao đèn lồng, cậu bé vào góc tối). Còn chê: mặt không nhất quán, vài cảnh "sáng phẳng như ban ngày", cảnh hốc cửa khó phân biệt người và bóng, nhịp dồn ở 0:20–0:40.

## 1. Bảng 7 mục (trước / sau, số đo thật)
| # | Mục | v1 (trước) | v2 (sau) | Đo / bằng chứng | Kết luận |
|---|---|---|---|---|---|
| 1 | **Tiền đề đêm, đèn điện thấy được** | Phố trắng đọc thành ban ngày (0:34–0:58); 0:30 "điện hay bình minh?" | Trời đêm xanh đen có sao sau khi bật; bỏ chân trời hồng. Đầu đèn điện nhấp 2 lần rồi đứng, loá lạnh, ở 5 shot: s10e, s12, s19, s27, s37w | Độ sáng trung bình 1/4 trên khung (luma 0–255): 0:34–0:58 **132,6 → 86,7**; toàn cảnh thành phố lúc bật **155,9 → 21,7**. AI mù (e): "buổi tối… trời có sao… ánh sáng trắng là đèn điện kiểu mới, lạnh và loá" | **Đạt phần chính.** Còn 4 chỗ AI thấy "sáng phẳng gần như ban ngày" (0:44, 1:12, 1:42, 1:52–1:56) |
| 2 | **Ngọn cuối (2:04 v1)** | "Thắp hay tắt?" | s40 (1:49,4): tay trên van, lửa co lại, ngả xanh, tắt, giữ im 0,8 s. s40w (1:52): toàn cảnh, không gì đổi | Van 1:49,7; lửa co và xanh 1:50,3–1:51,2; tắt 1:51,2. AI mù (h): "bà tắt ngọn đèn đi… khá chắc nhưng không hoàn toàn, vì không thấy khoảnh khắc tắt" | **Đạt** (khung mẫu 2 s rơi đúng hai bên khoảnh khắc tắt) |
| 3 | **Đồng hồ 3 nhịp, giờ tiến** | 0:16, 0:48, 2:20 gần như cùng giờ | Nhịp 1 (0:16) 7:31 · nhịp 2 = lúc bật điện (0:25–0:30): đồng hồ quảng trường 8:00, đồng hồ bỏ túi 7:53 · nhịp 3 (2:09–2:15): 9:53 → 10:00 | AI mù (g) đọc được: 7:30 · 8:00 · 7:55 · 9:55 · 10:00 | **Đạt.** AI chưa hiểu ý "chậm 7 phút" |
| 4 | **Bóng cảnh 5** | 1:42 "ba cái bóng"; bóng Cas to hơn bóng Ida | Quang học thật: đèn lồng cách vách 3,0 m. Ida đứng cách vách 1,4 m → bóng ×1,88 (≈ 2,8 m); Cas sát vách 0,45 m → bóng ×1,18 (≈ 1,5 m), ngay cạnh cậu. s34 máy nghiêng từ phải: Cas cạnh bóng nhỏ của mình | AI mù (i): "1:28 rõ nhất, có 2 bóng: bóng phụ nữ cao… và bóng cậu bé có quả bông". Nhưng ở 1:22–1:26 "không phân biệt được hình nào là người thật, hình nào là bóng"; "bóng bà không có mũ" | **Đạt một phần.** Kích thước đúng; khung rộng s33 còn lẫn người với bóng |
| 5 | **Mặt Ida nhất quán** | Mắt xanh + má hồng (1:00) đọc thành ông già; mắt phát sáng (1:14); mũ nâu/đen/nâu | A1 (lọn tóc + hoa tai) ✔. Mắt nâu #5a4636 theo sheet ✔ (sửa luôn một lỗi: dải màu tròng cũ bị chú thích "nuốt"). Mắt phát sáng s26: tìm ra là **đèn khí L11 ngay trên đầu** (vành mũ che trán, cổ áo che cằm, còn dải mắt sáng); dời Ida 1,3 m ra xa đèn ✔. Mũ: albedo một màu #2b2a2a, không chỉnh theo shot ✔ | Đầu/cổ đo trên lưới: đầu rộng 0,77 H (sheet 0,78), cổ 0,30 H (sheet 0,30). Màu mũ thấy được ở s40: dưới lửa **sắc 17°, bão hoà 0,49** (nâu) → sau khi tắt **252°, 0,17** (đen xám), cùng một albedo. Cổng mặt lần 3: xem mục 4 | **Chưa đạt.** Albedo đúng; màu thấy vẫn đổi theo màu nguồn sáng (vật lý đúng). Mặt vẫn bị đọc "mặt nạ/búp bê" |
| 6 | **Siết nhịp** | 2:30; hụt chú ý 0:34–0:58, 1:08–1:22, 2:14–2:24 | 2:22,5. Đoạn đua: 24 s → 15,5 s. Cảnh 4: 26 s → 21 s. Bỏ s16–s18, s20 | Hụt chú ý theo AI mù v2: 0:20–0:40 (cắt dồn đồng hồ/đèn), 0:50–1:00 (góc tối quá tối), 1:00–1:10, 1:20–1:30, 1:40–1:50 (cận mặt dài), 2:00–2:10 | **Đạt về thời lượng.** Chỗ hụt đổi vị trí: đoạn v1 chậm nay ổn, còn đoạn mới quá dồn |
| 7 | **Cas đọc được (1:04 v1)** | Chỉ là một chấm | s24c (0:57,5–0:59): cận trung Cas, mặt ấm vì ngọn L11 | AI mù (j): "chấm đỏ nhỏ ở 0:56, rõ mặt lần đầu ở 0:58" | **Đạt** |

## 2. Việc làm theo từng nhiệm vụ

### 2.1 Tiền đề đêm (nhiệm vụ 1)
- `nightSky()` được thêm vào phố, tường nhà kho và thành phố: trời xanh đen, sao nhỏ. Bản đầu sao to như bông tuyết ở tiêu cự dài; đã thu nhỏ.
- `elecGlare()`: quầng + vệt loá ngang trên đầu đèn điện. Đèn bật theo nhịp "tối–sáng–tắt–sáng–đứng" (kịch bản dòng 48).
- **Lỗi tôi gây ra rồi sửa.** Tôi hạ trắng tràn ban đêm (0,9 → 0,32) để phố bớt "ban ngày". Kết quả: ở 0:40–0:42 bóng dài của đèn khí vẫn còn, trái kịch bản. AI mù lần A đọc 0:40 là "ấm áp… vừa thắp đèn". Đã trả về 0,9 và render lại 21 shot. Dấu hiệu đêm giờ do trời sao và sương tối, không do giảm trắng.
- Cần biết: `bible/world-rules.md` mục 2 ghi đèn điện "không lõi, không rìa". Quầng loá là loá ống kính, có lõi sáng. Tôi giữ vì chủ dự án yêu cầu "đèn trắng lạnh chói". Nếu muốn đúng luật tuyệt đối thì bỏ vệt loá ngang.

### 2.2 Ngọn cuối (nhiệm vụ 2)
- s40 bản v1 đặt máy **trong** lồng kính, không đọc được. Bản v2 đặt máy ngoài lồng, 50 mm.
- Bàn tay được đặt lên cần van bằng cách dịch gốc nhân vật (≤ vài chục cm; insert không thấy chân thang). Cần van quay −0,5 → 0,7 rad.
- Lửa co lại còn 20%, ngả xanh (#6f8cff), tắt ở +1,8 s. Tiếng: van, lửa xì nhỏ, "phụt" tắt.
- s40w: toàn cảnh góc, trắng đứng yên 2 s.

### 2.3 Đồng hồ (nhiệm vụ 3)
Lý do từng nhịp nằm ở cột "Lý do chọn" của SHOTLIST (s06, s09, s09w, s45, s45c, s46).

| Nhịp | Mốc | Đồng hồ quảng trường | Đồng hồ bỏ túi |
|---|---|---|---|
| 1 | 0:16 | — | 7:31 (gõ kính) |
| 2 | 0:25–0:30, **trùng lúc bật điện** | sáng đúng 8:00 + chuông | 7:53 |
| 3 | 2:09–2:15 | 10:00 | 9:53 → vặn lên 10:00, gập lại, không gõ |

### 2.4 Bóng cảnh 5 (nhiệm vụ 4)
- Không dùng bóng giả. Chỉ đổi chỗ đứng: bóng phóng đại = 3,0 / (3,0 − khoảng cách người–vách).
- s33 khung rộng giữ bố cục style frame c_s5_wide. s34 đổi máy từ qua vai sang nghiêng từ phải.

### 2.5 Mặt Ida (nhiệm vụ 5)
- A1 đã dựng (`cast3d.js`). Sheet v1.2, SHA khoá lại (mục 5).
- **Đầu/cổ ở góc gần chính diện.** Số đo khớp sheet: đầu rộng 0,77 H (sheet 0,78), cổ 0,30 H (sheet 0,30). Bản v1 trông "đầu quả trứng" vì cổ trần dài lộ ra; v2 dựng cổ áo đứng cao tới cằm, đúng hình model sheet.
  - Nhưng cổ áo hình trụ trơn lại bị người xem gọi là "cổ ma-nơ-canh" và "mặt ghép lên thân" (mục 4).
- **Mắt phát sáng.** Hai lần sửa:
  - Lần 1: hạ đèn lồng thắt lưng 0,06 → 0,012. Không hết.
  - Lần 2 (chẩn đoán bằng tắt từng lớp): nguyên nhân là **đèn khí gần như ngay trên đầu**. Dời Ida ra xa đèn, hết.
  - Ở bộ cảnh hốc cửa và ngõ (dựng từ Cổng 3), glint mắt mặc định 5,0 hợp phơi sáng 0,12. Ở phơi sáng animatic ~1 mắt Cas sáng trắng, nên đã hạ về 0,12 như mọi shot khác.
- **Mũ.** Chỉ có một nguồn màu (`local_colors.hat` = #2b2a2a, trung tính). Không shot nào ghi đè. AI mù vẫn liệt kê mũ "nâu" dưới đèn khí và "đen" dưới điện. Xem quyết định D.

### 2.6 Nhịp (nhiệm vụ 6)
Toàn bộ mốc lấy từ một bảng `ORDER` trong `film.js`. Âm (`mix.py`), phụ đề (`package.py`), SHOTLIST và câu hỏi chiếu mù đều đọc từ đó (`render_film.js --events`), không gõ tay.

| Cảnh | v1 | v2 |
|---|---|---|
| 1 Vòng đèn | 0:00–0:26 | 0:00–0:25 |
| 2 Bật điện | 0:26–0:44 | 0:25–0:43,5 |
| 3 Chạy đua | 0:44–1:08 | 0:43,5–0:59 |
| 4 Bức tường | 1:08–1:34 | 0:59–1:20 |
| 5 Ngọn cuối | 1:34–2:10 | 1:20–2:02,5 |
| 6 Ô cửa | 2:10–2:30 | 2:02,5–2:22,5 |

### 2.7 Kịch bản, SHOTLIST, gói chiếu
- `scripts/last-round.fountain` → **nháp 3**: mốc mới, cấu trúc mới; thoại nguyên văn.
- `shots/animatic/SHOTLIST.md` sinh lại: có cột "Nguồn khung", mục "Ba nhịp đồng hồ" và "Nguồn sáng điện thấy được và góc tối".
- `screening/animatic_v1_v2_diff.md`: shot bỏ, mới, sửa, kèm lý do.
- `screening/questions.json`:
  - c1 giữ 0:40;
  - c2 1:50 → 1:41;
  - c3 2:07 → 2:00;
  - đoạn (b) theo 2:22.

## 3. Ba chỉ đạo của chủ dự án sau khi xem animatic v1
| Chỉ đạo (nguyên văn, AUTHORSHIP) | Đã làm | Shot | Mốc v2 |
|---|---|---|---|
| 0:40 — "có thể hiểu được phố chuyển sang đèn điện trắng" | Giữ ý. Trước 0:40 có đủ dấu hiệu:<br>• trời đêm có sao;<br>• đồng hồ 8:00 + chuông (s09);<br>• đồng hồ bỏ túi 7:53 (s09w);<br>• bóng đèn điện quảng trường nhấp hai lần, đứng trắng (s10e);<br>• sóng trắng lan (s10);<br>• bóng đèn x=85 bật (s12).<br>Ở 0:40 trắng tràn tới Ida (s13); 0:41,5 bà giơ tay, không bóng dài (s14). Khối cuối cạnh nhà kho không bật trong sóng (đoạn cáp cuối) | s09–s14 | 0:25–0:43,5 |
| 1:50 — "góc phố cuối cùng từ tối sang bị chiếu sáng bởi ánh đèn điện, phù hợp với câu thoại" | **Luật thế giới v0.4 "đoạn cáp cuối":** góc ngọn 11 đóng điện sau cùng.<br>• Góc tối, chỉ có hổ phách và bóng dài từ khi Ida thắp ngọn cuối, qua lúc đẩy mũ và vế đầu câu L4.<br>• Đúng quanh "You'll be brighter now", cột góc nhấp hai lần rồi đứng trắng; bóng dài và bóng tối biến mất.<br>• Ở cảnh 4, cột **phố chính** cạnh góc nhà kho bật và phủ tường chim (1:04). Góc ngọn 11 lùi sau góc nhà, ngoài tầm vũng sáng ~20 m | s23, s24, s24c, s35, s36, s37 (tối) → **s37w** (bật) → s38, s39 (trắng) | tối 0:52,5–1:40,8; **bật 1:41,2**; lời "You'll be brighter now" bắt đầu 1:41,55 |
| 2:07 — "Cas nên chọn 1 góc tối để huơ tay" | Cas nhận đèn lồng, nhìn quanh phố trắng. Cậu mang đèn vào **vòm hốc cửa tối** (nơi có hai cái bóng ở cảnh 5), ngồi xổm, hơ tay một–hai–ba. Máy đặt trong hốc nhìn ra vòm: sau lưng cậu là phố trắng, Ida đứng ở miệng vòm nhìn vào, không nói. **Không thêm chim bóng** trong hốc; giữ kết phòng Cas (s48), xem quyết định B | s42a, s42b, s42 | 1:55,5–2:02,5 (đếm ba ở 2:00,1 / 2:00,7 / 2:01,3) |

Luật thế giới v0.4 (`bible/world-rules.md` mục 1) chọn lý do **đoạn cáp cuối bật sau**. Không chọn "bị nhà che", vì cột góc đứng ngay trong khung s37w và phải bật được trên hình.

Đồng hồ nhịp 3 đặt ở 2:09–2:15, sau khi Cas vào góc tối.

## 4. Cổng mặt — kiểm mù lần 3 (nguyên văn trong `reports/m1/cong4/kiem-mu-mat/lan3.md`)
Mỗi ảnh gửi cho **một subagent mới**, câu hỏi đúng nguyên văn: "Người này bao nhiêu tuổi, giới tính gì, đang cảm thấy gì?".
- k2 = trung tính, m7 = cười buồn, w4 = nghẹn.
- q9 = khung gần chính diện của animatic (s37, 1:37,5, tương ứng 1:50 v1).

| Tiêu chí | Kết quả |
|---|---|
| 3/3 đọc là bà cụ, không "không chắc" | **ĐẠT.** k2, m7, w4: "nữ, bà cụ", 65–80 tuổi |
| ≥ 2/3 cảm xúc đúng | **ĐẠT.** m7 ✔, w4 ✔, k2 ~ ("trầm ngâm… gần như vô cảm") |
| Không "mặt nạ/búp bê/con rối" | **TRƯỢT.** k2 "giống mặt nạ"; w4 "hơi giống mặt nạ ghép lên thân"; q9 "cổ ma-nơ-canh… búp bê" |
| Ảnh 4 (animatic) | **TRƯỢT.** "Có lẽ là nữ… nét mặt không cho thấy rõ" |

Nguyên nhân chung người xem nêu:
- ranh giới cằm/cổ cứng (cổ áo trụ trơn);
- ở q9, nét nếp mũi–má chạy tới cằm đọc thành "vết nứt";
- q9 còn cháy sáng vì nguồn khí ở rất gần.

## 5. C3 và luật máy
### 5.1 Sheet (Q-C3v A, Q-C3w A)
- Đo B1 thêm góc −45°, ±135°, 180° cho Ida và Cas, ghi vào `c3_views` 8 góc. Ida đo lại toàn bộ sau A1 và cổ áo cao.
  - Ida ở 0°: cổ áo che cằm nên tỷ lệ tăng ~3%. Thân 2,584 → **2,667**; cánh tay trên 1,55 → 1,60; cẳng tay 0,963 → 0,994.
  - Cas: lưới không đổi, số cũ giữ nguyên. Cẳng tay ở 90° ghi null (0,05 là mẩu cổ tay ló ra).
- **Q-C3w (đùi Cas):** đo ở −60/−75/−80/−85/−88/−90° được 1,19 / **1,211** / 1,068 / 1,074 / 1,075 / 1,076.
  - Bậc −13% nằm giữa −75° và −80°. Mặt nạ so sánh cho thấy **cánh tay buông che mép trước đùi**, không phải gấu áo len.
  - Số −90° đúng cho tư thế turnaround. Lệch +9–11% ở walk_cas đến từ chuyện tay vung khỏi đùi khi đi.
  - Đã ghi vào sheet và `characters.md` làm giới hạn đã biết; không đổi số.
- `bible/characters.md` v1.2. `design/cong3/LOCK-THIET-KE.sha256`: 26/26 OK, thêm `ida.json` và `cas.json` vào khoá.
- `assets/LIBRARY.json`: cập nhật SHA sheet v1.2. Luật O3 đã bắt đúng chỗ này.

### 5.2 Bộ xuất `views` và kiểm toán
- `design/cong4/animatic/export_c3.js` + `window.exportC3` (page.js) tính theo công cụ tham chiếu `k_views.js` của K:
  - mặt nạ 4× (3840×2160);
  - `views` cho 285 khung (0, 12, …, 3408), trong đó 236 khung có Ida;
  - khung không có Ida: mặt nạ rỗng, mọi bộ phận hidden = 1.
- **Kiểm toán: phát 5 lần, 4 lần đầu HUỶ trước khi đối chiếu.** Hạt giống lưu ở `reports/m1/cong4/c3-kiem-toan/request_huy_*.json`.

  | Lần | Hạt giống | Khung | Lý do huỷ |
  |---|---|---|---|
  | 1 | 204756444951447011 | 1656, 2976 | Render lại 21 shot sau lỗi trắng tràn → video đổi |
  | 2 | 10878265309862672119 | 900, 1116 | `views` thiếu mục cho khung không có Ida (luật báo sai định dạng) |
  | 3 | 15511226453768317070 | 1116, 2976 | Bộ phận nằm sau mặt phẳng máy (insert s09w, s46) có depth âm |
  | 4 | 1215417136224124268 | 2952 | Bỏ bộ phận đó khỏi `views` nhưng còn trong `frames` |
  | **5 (hiệu lực)** | **1089546929179889476** | **708, 2616** | — |

  - Khung do máy chọn ngẫu nhiên từ hệ điều hành; tôi không chọn khung.
  - Lần 5: render lại khớp **0,0%** điểm ảnh biên, views khớp (lệch 0° / 0).
  - Ghi chú trung thực: P tự render lại (không có phiên xưởng riêng).

### 5.3 Kết quả luật máy (nguyên văn)
**Lệnh được giao:** `/opt/cine/bin/python checks/run.py screening/animatic.mp4 --profile shot`. Báo cáo: `reports/checks/animatic-screening-v2/`.
```
[   PASS] N1 24 fps CFR; không rơi hay lặp khung theo PTS
[   PASS] N2 BT.709 đủ 3 trường; dải limited — đo cả nhãn lẫn giá trị điểm ảnh
[    N/A] N3 Codec và bitrate đúng loại master; khung 16:9, SAR 1:1
[   FAIL] P0 Máy dò chữ độc lập: mọi chữ trong hình phải có matte
[MISSING] P1 Không chữ đè chữ, tính theo điểm ảnh nét chữ
[MISSING] G4 Chữ tương phản ≥ 4,5:1 (WCAG AA), đo điểm ảnh
[   PASS] G3 Không banding trên gradient
[   FAIL] G3b Grain cố định: có grain, ổn định theo thời gian và giữa các shot, chuyển động theo khung
[    N/A] M1 Master YouTube: −14 LUFS ±1; true peak ≤ −1 dBTP
[   PASS] M3 Tương quan pha và tương thích mono
[MISSING] J1 Mọi từ trong kịch bản nghe rõ trên bản mix cuối
[MISSING] J1b Lời rõ trên nhạc theo từng câu, đo từ stem thoại và stem nền
[MISSING] H1 Không chuyển động tuyến tính ở bộ phận nhân vật
[MISSING] H1b Chuyển động khai báo khớp hình render (luồng quang học ở vùng nhân vật)
[MISSING] C3 Đúng model: tỷ lệ bộ phận so với model sheet, có tính nhiễu đo
[MISSING] O3 Mọi tài sản lấy từ thư viện có SHA
VERDICT: TRƯỢT
```
`screening/` cố ý chỉ chứa video và câu hỏi (gói chiếu mù), nên mọi luật cần file đi kèm đều báo THIẾU. P0 trượt vì phụ đề không có matte cạnh file này.

**Cùng video, byte giống hệt, có đủ file đi kèm:** `checks/run.py design/cong4/animatic/out/animatic.mp4 --profile shot`. Báo cáo: `reports/checks/animatic-v2/`.
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

**Chỉ số trong ±5% quanh ngưỡng** (máy liệt kê):
- C3, hệ số mặt nạ 4,0 (ngưỡng tối đa 4,0);
- C3, hệ số khi đầu < 100 px 4,0 (ngưỡng 3,98).

**Chi tiết C3:**
- Mẫu đo được: 125/588 (21,3%). Kết quả: **68 trượt chắc chắn, 56 không chứng minh được, 1 đạt**.
- Trượt tập trung ở:
  - thân ở −90° khi vác thang (+6–8%);
  - cẳng tay ở −45° (−16…−20%, tay cầm đèn ở sheet so với tay buông trong phim);
  - cánh tay trên ở 45° (−8…−34%).
- Độ khớp biên < 1,5 ở 63/196 khung (lớp vẽ Kuwahara làm mềm cạnh).
- **CẦN NGƯỜI XEM:** 21 đoạn theo cách tách shot của máy, ứng với 19 shot phim: s03, s04, s05, s08, s12, s14, s21, s22, s27, s31, s34, s36, s37, s38, s39, s40, s42a, s44, s47.

**G3b:** vẫn trượt như v1. Tương quan grain giữa khung kề > 0,5 ở vài shot vì lớp vẽ giữ cấu trúc. Trung vị σ không đều giữa shot.

**H1b:** vẫn trượt. Các track tay ở shot đi bộ (s02, s07) khớp 43–63%.

### 5.4 Q-C3r B — bảng so sánh cho người xem
- Agent cine-continuity làm 21 ảnh so sánh: khung phim đặt cạnh hình model sheet ở góc gần nhất, kèm độ lệch từng bộ phận và lý do máy loại. Bảng: `reports/m1/cong4/c3-nguoi-xem/BANG.md`.
- Giới hạn agent tự nêu: `MS-ida.png` còn là bản Cổng 3 vòng 1 (chưa có khăn, hoa tai, cổ áo cao), nên trang phục được so với bible v1.2.

### 5.5 Shot bị cờ — chủ dự án chỉ cần xem 9 ảnh (8 shot phim)
- **Nhóm màu, 6 ảnh.** Dưới đèn khí, mũ đọc nâu vàng và áo đọc xanh lá sáng, đảo quan hệ "mũ tối nhất" của sheet. Albedo không đổi; đây là ánh sáng và grade, cùng gốc với quyết định D.
  - s03 (khung 228)
  - s04 (khung 276)
  - s05 (khung 360)
  - s36 (khung 2268)
  - s37 (khung 2412)
  - s39 (khung 2520)
- **Nhóm số đo, 3 ảnh.** Lệch > 10% ở bộ phận không che, không gập. Bằng mắt, agent vẫn đọc đúng là Ida.
  - s08 (khung 588): cẳng tay +19,1%.
  - s27 (khung 1536): thân −12,3%, còn khoảng −8,7% nếu trừ phối cảnh.
  - s47 (khung 3252): thân +16,2%, cẳng tay +17,5%; đầu đọc nhỏ so với thân ở góc sau lưng; thang dựng gần đứng.
- **Không cờ: 12 ảnh.** Thân bị cắt ở mép khung, bộ phận bị che hoặc gập, hoặc không có đầu trong hình. Mặt, hoa tai, khăn, tóc khớp bible v1.2.
- **Gần ngưỡng góc 30°:** s34 cách hình "Sau lưng" 31°; s12 lệch 30,6°.

## 6. Thời gian và số lần làm lại
Máy: 4 lõi CPU, Chromium/SwiftShader, 960×540, 1 mẫu.

| Việc | Thời gian máy | Làm lại |
|---|---|---|
| Probe (3 khung/shot), 5 vòng + chẩn đoán | ≈ 10 phút | — |
| Render đợt 1: 49 shot mới, 3 tiến trình song song + nhóm D | 4 bản ghi 1 915 + 2 041 + 1 454 + 725 s (≈ 45 phút đồng hồ) | — |
| Render đợt 2: 24 shot (sửa trắng tràn + dời Ida ở cảnh 4) | 1 058 + 890 + 951 + 687 s (≈ 25 phút đồng hồ) | 1 |
| Tổng khung render | 4 560 khung cho phim 3 420 khung (trung bình 2,1 s/khung/tiến trình) | ×1,33 |
| Ghép hình (`assemble.py`) | 4,8 phút × 2 | 1 |
| Đóng gói 2 pass (`package.py`) | 4,0 phút × 2 | 1 |
| Âm (`mix.py`) | 56 s | 0 |
| Mặt nạ C3 4× + views, 285 khung | ≈ 15 phút × 2 | 1 (video đổi) |
| Kiểm toán C3 | 5 lần phát, 4 huỷ | 4 |
| Luật máy | ≈ 20 phút/lần; 5 lần | 4 (sửa định dạng) |
| Cổng mặt (3 ảnh 1920×1080, 3 mẫu) | 28 + 31 + 31 s | — |
| AI mù (71 khung) | 131 s (lần A) + 141 s (lần B) | 1 (sau sửa 0:40) |

Số lần làm lại theo nhiệm vụ:

| # | Nhiệm vụ | Làm lại | Chi tiết |
|---|---|---|---|
| 1 | Đêm | 3 | s10e máy 2 lần (mái nhà lơ lửng); s27 máy 1 lần (lộ mép bộ → nối tường 40 m); trắng tràn 0,32 → 0,9 và render lại 21 shot |
| 2 | Ngọn cuối | 1 | s40 máy trong lồng → ngoài lồng |
| 3 | Đồng hồ | 0 | |
| 4 | Bóng | 0 | |
| 5 | Mặt | 4 | Lỗi dải màu tròng; mắt phát sáng 2 lần; phơi sáng cận mặt 1 lần. Cổng mặt: 1 lần kiểm, trượt |
| 6 | Nhịp | 0 | s25 chuyển từ tái dùng v1 sang render lại |
| 7 | Cas | 1 | s24c: Cas quá tối, xa → dời gần, máy gần |

## 7. Quyết định cần chủ dự án
**A. Cổng mặt trượt tiêu chí "mặt nạ/búp bê".**

| | A1 — Sửa vùng cằm–cổ, kiểm mù lần 4 (đề xuất) | A2 — Chấp nhận cho animatic, sửa ở Cổng 6 | A3 — Làm lại mặt |
|---|---|---|---|
| Làm gì | Cổ áo đứng có nếp và mép cong ôm cằm (bỏ trụ trơn); làm mềm nét nếp mũi–má ở góc chính diện; key phụ dịu hơn cho cận mặt dưới đèn khí. Không đổi tỷ lệ sheet | Ghi nhận trượt; animatic chỉ để duyệt truyện | Dựng lại nửa dưới mặt (má, cằm) và cổ |
| Ưu | Nhắm đúng lời chê của cả 3 người xem; giữ A1 và B1 | Không tốn thêm | Có thể giải quyết gốc |
| Nhược | Cổ áo đổi → đo lại B1 ở 0° | Rủi ro dời sang sau | Lâu nhất; phải khoá lại sheet |
| Tác động | Characters v1.3; 1 vòng kiểm 4 ảnh | Cổng mặt để mở | Lùi Cổng 5 |
| Rủi ro | Trung bình | Cao | Thấp về kết quả, cao về lịch |

**B. Kết (2:07 v1): chim bóng trong hốc hay giữ phòng Cas.** Hiện làm theo B1.

| | B1 — Không chim trong hốc; giữ kết phòng Cas (hiện tại) | B2 — Chim bóng trong hốc, bỏ phòng Cas |
|---|---|---|
| Ưu | Hai nhịp không trùng: hốc = trả mô-típ đếm ba; phòng = chim trở lại, lớn và bay | Kết ngắn hơn ~5 s; khép vòng ngay tại chỗ |
| Nhược | Phim dài hơn một cảnh | Mất hình kết đã khoá (e_ending); chim hai lần gần nhau |
| Tác động | Không đổi | Sửa s42, bỏ s48, sửa kịch bản |
| Rủi ro | Thấp | Trung bình |

**C. Đọc "sáng phẳng như ban ngày" còn sót (0:44, 1:12, 1:42, 1:52–1:56).**

| | C1 — Giữ; trắng phẳng là ý đồ, trời sao đủ báo đêm (đề xuất) | C2 — Giảm trắng tràn ở khung có trời (mặt tiền tối dần lên cao) |
|---|---|---|
| Ưu | Đúng luật thế giới: điện phẳng, không bóng | Đọc "đêm" chắc hơn |
| Nhược | Một số người xem vẫn thấy "ngày" | Dễ làm lộ lại bóng dài (lỗi 0:40 lần A) |
| Tác động | 0 | Render lại ~15 shot |
| Rủi ro | Thấp | Trung bình |

**D. Màu mũ đổi theo ánh sáng** (albedo đã cố định).

| | D1 — Giữ albedo trung tính #2b2a2a (đề xuất) | D2 — Đổi mũ sang xanh đen #262a33 | D3 — Grade khử bão hoà vùng tối dưới đèn khí |
|---|---|---|---|
| Ưu | Đúng vật lý | Dưới lửa ra nâu xám, dưới điện ra đen xanh: bớt nhảy "nâu ↔ đen" | Không đổi thiết kế |
| Nhược | Người xem vẫn thấy nâu dưới lửa | Đổi màu đã khoá (sheet v1.3) | Đụng color script đã khoá |
| Tác động | 0 | Sửa sheet, khoá lại | Sửa grade mọi shot |
| Rủi ro | Thấp | Thấp | Trung bình |

## 8. Việc đang chờ chủ dự án
1. **Xem `screening/animatic.mp4` (2:22,5)** và duyệt ba chỉ đạo đã vào phim (mục 3).
2. Chọn A (cổng mặt), B (kết), C (đọc đêm), D (mũ).
3. Duyệt **luật thế giới v0.4** ("đoạn cáp cuối"), **kịch bản nháp 3**, **characters v1.2**; các file này đã khoá lại SHA.
4. Xem 9 ảnh C3 bị cờ ở mục 5.5 (Q-C3r B) và xác nhận đúng model. Cân nhắc cho làm lại `MS-ida.png` theo v1.2 để các vòng sau có hình chuẩn.
5. Quyết cách chấm L3 (chủ dự án chấm một mình, đã ghi): lịch chiếu gói chiếu mù v2 cho người thật.
6. Ghi chú: 4 lần phát kiểm toán bị huỷ (mục 5.2). Nếu chủ dự án hoặc K thấy cần, K có thể phát lại lần 6 trên bản này.
