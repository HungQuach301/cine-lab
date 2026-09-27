# CỔNG 3 — THIẾT KẾ · vòng 1 · "Last Round"

Phiên P, 27/09/2026. Nhánh `claude/cine-lab-m1-cong3-design`, tạo từ `main` sau khi hợp nhất kịch bản chốt và `checks/v1.1`. `lock.py --verify` trên main: **KHỚP** `d97f9b01…5c3f`.
Mọi số dưới đây là đo thật. Đây là bản **đề xuất của Claude, chưa duyệt**; hướng mỹ thuật, model sheet và color script chờ chủ dự án chọn bằng mắt.

## 0. Tóm tắt
- **Ba hướng mỹ thuật**, mỗi hướng 2 khung 1920×1080 (s1 mở phim lúc chạng vạng; s5 hai cái bóng trong hốc cửa). Bảng tổng: `design/cong3/KHUNG-MAU-3-HUONG.png`.
- **Chưa hướng nào đạt ngân sách render 2,5 s/khung** ở thiết lập sản xuất (8 mẫu). Hướng gần nhất là C, vượt 1,3–1,7 lần.
- **Luật:** N1, N2, G3 đạt ở cả 3 hướng. **G3b chỉ C đạt**; A trượt sát ngưỡng, B trượt rõ (xem mục 3).
- **Khuyến nghị: hướng C "Painted Glow"**, có điều kiện (mục 5).
- Nói thẳng: **cả 3 hướng đều còn lộ "CG" ở nhân vật**. Bộ dựng nhân vật chung ghép từ khối nguyên thuỷ nên đọc như búp bê gỗ ở cận cảnh. Ở khung rộng, C và B giấu được tốt hơn A.

## 1. Nền chung (P làm, mọi hướng bắt buộc dùng)
| Thành phần | File | Ghi chú |
|---|---|---|
| Bộ dựng nhân vật | `design/cong3/shared/cast.js` | Khung xương đo giữa hai tâm khớp (bài học C3 ở M0); áo Ida 4 vạt (xẻ tà, vạt trước theo đùi); bàn tay 5 ngón (chim bóng) |
| Đường ống xuất hình | `design/cong3/shared/post.js` | Float32 + jitter R2 + ACES + **grain cố định** (σ 1,5 mã, hạt 1,6 px) + dither: như M1, đã qua G3/N2 |
| Driver | `design/cong3/shared/render_still.js` | Render khung tĩnh; 48 khung grain động để ghép video kiểm luật |
| Model sheet dữ liệu | `design/cong3/model-sheet/ida.json`, `cas.json` | Tỷ lệ (luật C3), quy ước đo, trang phục, đạo cụ, màu gốc, 9 tư thế then chốt |

Lỗi của chính P phát hiện trong vòng này (đã sửa):
1. Một lần sửa bằng `sed` làm dòng gắn lông mày nằm sau `//`, nên lông mày không được gắn. Hướng C phát hiện.
2. **Gáy Ida bị đọc nhầm thành khuôn mặt**: nửa sau sọ để trần, giữa có búi tóc tròn sáng. Hướng B và C phát hiện; P đã nhầm nhận xét rằng B để nhân vật quay mặt về máy, rồi kiểm lại bằng ảnh đối chứng thì thấy B đúng. Đã sửa gốc: thêm tóc phủ nửa sau sọ trong `cast.js`. Các khung mẫu vòng 1 render trước bản sửa; hướng B và C đã tự vá tạm.
3. Quả bông mũ Cas bị nứt, trông như nét vẽ nguệch ngoạc (nhiễu đỉnh theo chỉ số), sửa thành nhiễu theo vị trí.

## 2. Model sheet và silhouette (C2)
- `design/cong3/model-sheet/MS-ida.png`, `MS-cas.png`: xoay 4 góc; 4 tư thế Ida và 5 tư thế Cas theo kịch bản; bảng tỷ lệ; màu gốc. Tỷ lệ lưu trong JSON cho luật C3.
- `C2-silhouettes.png`: tô đen đặc 9 tư thế. Số đo máy trong `c2-silhouette-metrics.json`:
  - IoU giữa hai tư thế của cùng nhân vật: tối đa 0,49 (Ida) và 0,61 (Cas: `shadow_bird`~`look_lantern`);
  - IoU Ida–Cas khi đứng: 0,31.
- **Đánh giá bằng mắt của P (thẳng thắn):**
  - Đọc rõ 4/9: P1 đi vác thang, P3 quỳ cầm đèn, C3 giữ thang, C4 ngồi hơ tay.
  - Đọc được nhưng nhỏ 1/9: C1 chim bóng, chỉ rõ khi nhìn từ phía nguồn sáng.
  - Yếu 4/9: P2 hơ tay (không có đèn thì trông như đang chìa tay), P4 đứng nhìn, C2 hạ tay nhìn đèn, C5 tay nửa giơ.
  - Ước khoảng 55% tư thế đọc được qua silhouette, **dưới xa mức ≥ 90% của C2**. Tư thế "nhìn" cần đạo cụ hoặc bố cục (hướng đầu, vai, khoảng cách) mới đọc được; phải sửa ở Cổng 5 và 6. Máy không thay được kiểm C2 bằng khán giả.

## 3. Ba hướng mỹ thuật
### Số đo (đo lại **tuần tự trên máy rỗi**, 1920×1080, SwiftShader CPU 4 vCPU; thô: `reports/m1/cong3/timing/`)
| Hướng | s1 · 8 mẫu | s5 · 8 mẫu | s1 · 32 mẫu | s5 · 32 mẫu | Vượt ngân sách 2,5 s (8 mẫu) |
|---|---|---|---|---|---|
| A Tin & Felt | 57,2 s | 20,7 s | 190,3 s | 53,9 s | **8–23×** |
| B Ink & Lamplight | 7,5 s | 5,5 s | 21,8 s | 13,3 s | **2,2–3,0×** |
| C Painted Glow | 4,2 s | 3,3 s | 12,9 s | 9,0 s | **1,3–1,7×** |

Mốc so sánh: cảnh mẫu M1 (1 đèn, 8 mẫu) là 1,9 s/khung. Thời gian dựng cảnh (không tính mỗi khung): A khoảng 32 s, B 0,8 s, C 6 s.

### Luật máy (profile `shot`, 2 shot × 48 khung mỗi hướng, x264 30 Mbps tune grain; báo cáo: `design/cong3/dir-X/check/report/`, `design/cong3/check-all/report/`)
| | N1 | N2 luma ngoài dải | G3 banding lớn nhất | G3b |
|---|---|---|---|---|
| A | ĐẠT | ĐẠT 0,0423% | ĐẠT 0% | **TRƯỢT**: σ 1,132; CV 0,078; max/min 1,006; tương quan khung kề **0,514** (ngưỡng ≤ 0,5; **nằm trong vùng ±5%**) |
| B | ĐẠT | ĐẠT 0,0003% | ĐẠT 0% | **TRƯỢT**: σ 1,835; CV 0,067; max/min 1,022; tương quan **0,853** |
| C | ĐẠT | ĐẠT 0,0001% | ĐẠT 0% | **ĐẠT**: σ 1,221; CV 0,112; max/min 1,223; tương quan 0,438 |
| Cả 6 shot | ĐẠT | ĐẠT 0,0144% | ĐẠT 0% | TRƯỢT: σ max/min **1,684** giữa các hướng. Chỉ có nghĩa nếu trộn nhiều hướng; phim sẽ dùng một hướng |

P0 (dò chữ) đạt ở cả 3 hướng: không có chữ trong hình. Các luật thiếu dữ liệu (J1, H1, C3, O3…) không áp cho khung tĩnh.

Vì sao G3b trượt: grain chung vẫn đổi theo từng khung, nhưng **kết cấu tĩnh** nằm trong phần dư mà máy đo coi là grain.
- **B:** vân giấy và halftone gắn cố định vào màn hình. Đây là **lỗi thật**: khi máy quay chạy, nó thành "lưới dính kính" (B tự báo). Muốn sửa phải gắn kết cấu vào vật.
- **A:** vân dạ và đá gắn vào vật. Trên khung tĩnh, máy không phân biệt được kết cấu vật với grain, nên đây một phần là giới hạn của phép đo trên khung tĩnh. Kết quả nằm sát ngưỡng.
- **C:** vân canvas và nét cọ tính theo màn hình nhưng mảnh hơn nên vẫn đạt. Rủi ro thật của C nằm ở chuyển động ("kính tắm", mục 4).

### Tỷ lệ key : tràn tại vách trong hốc (do từng hướng tự đo, luật thế giới 3.1 cần ≥ 4 : 1)
A 5,6–8,3 : 1 · B ≈ 34 : 1 · C 14,5–36 : 1. Không số nào nằm trong ±5% quanh ngưỡng.

### Cả ba hướng lệch brief ở máy quay s5
Brief đặt máy 1,5 m sau đèn lồng. Với vòm rộng 3,2 m, ở vị trí đó mép khung nằm trọn trong hốc, **không thể thấy phố trắng ngoài vòm**. P tính sai hình học khi viết brief. Các hướng lùi máy: A 4,3 m, B 6,2 m, C 7,5 m (khung "tranh trong tranh"). C nộp thêm bản đặt máy đúng brief để so. Chủ dự án chọn ở mục 6.

## 4. Tự chấm theo `checks/RUBRIC.md` (P tự chấm; **không thay** người chấm L2 độc lập ≥ 3 người)
Chấm trên 2 khung tĩnh mỗi hướng, nên bằng chứng hẹp hơn chấm cả phim. Mã chưa có ví dụ mức 5 giữ trần 4.

| Mã | A Tin & Felt | B Ink & Lamplight | C Painted Glow |
|---|---|---|---|
| **D2** Ngôn ngữ hình thống nhất | **2**: s5, nhân vật trơn như nhựa đặt giữa dàn cảnh đá, gạch, vữa chi tiết cao; thấy ngay hai mức chi tiết khác nhau | **3**: viền mực, mảng phẳng, giấy in thống nhất ở cả s1, s5 và nhân vật; nhân vật tô phẳng vẫn đọc như búp bê gỗ | **3**: lớp vẽ phủ đều cả thế giới và nhân vật; cận cảnh (bản đặt máy theo brief) lộ khối nguyên thuỷ |
| **D3** Theo color script | **2**: s5 không thấy phố trắng ở mép khung, mất đối lập ấm–lạnh của ô 5 | **3**: s1 khớp ô 1 (tím, hồng, tâm hổ phách); s5 khớp ô 5 (hốc ấm, tường trắng) | **3**: như B; s5 đối lập ấm–lạnh rõ nhất |
| **G1** Ánh sáng có nguồn | **3**: nguồn đúng vật lý; vũng sáng sát chân đèn cháy gần trắng, đèn chưa đọc là thiếc | **3**: nguồn đúng, bóng đúng hình học 1,5×; vòng sáng đèn khí s1 đồng tâm như sơ đồ | **4**: s5 vùng tương phản cao nhất rơi đúng hai cái bóng (chủ thể kể chuyện); s1 dải phố sáng dẫn mắt. Chưa đủ 5 vì chưa có thay đổi ánh sáng trong cảnh |
| **C1** Chiều sâu nhân vật | Chưa chấm được: C1 cần xem phim và hồ sơ nhân vật (mong muốn, nhu cầu, điểm yếu, thay đổi), mà **hồ sơ này chưa có** | như A | như A |
| **C2** Silhouette | Chung cho mọi hướng (dùng chung tư thế): **khoảng 55% tư thế đọc được, trượt mức 90%** (mục 2) | | |

### "Trông như CG rẻ tiền" ở đâu (nói thẳng)
- **A:** nhân vật như búp bê nhựa đặt trong một dàn cảnh chi tiết; thành phố s1 là lưới nhà na ná nhau (đã xoay lưới 19° cho bớt); ở 8 mẫu DOF lộ các bản chồng rời và bóng mềm có vân bậc thang. **Đắt nhất**, 8–23 lần ngân sách.
- **B:** vòng sáng đồng tâm quanh đèn khí như sơ đồ; rìa bóng s5 như viền dán hơn là vùng bán dạ; nhân vật tô phẳng đọc như búp bê gỗ; vân giấy và halftone dính màn hình (trượt G3b).
- **C:** ít "CG" nhất ở khung rộng vì lớp vẽ giấu khối. Nhưng cận cảnh lộ nhân vật khối nguyên thuỷ; thành phố s1 có lưới cửa sổ đều; s5 tường trắng chiếm khoảng 60% khung, còn trống; có một vòng tròn lạ trên tường phải (vật thừa). Rủi ro lớn nhất: **lớp vẽ tính theo màn hình, chưa thử trên chuyển động**.
- **Chung cả 3:** s1 đồng hồ quảng trường và Ida quá nhỏ để đọc (khoảng 15–30 px). Việc này sửa ở layout (Cổng 5): toàn cảnh mở phim không mang được chi tiết đó.

## 5. So sánh và khuyến nghị
| | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|
| **A Tin & Felt** | Chất liệu sờ được, DOF thật, cảm giác "phim quay thật" | Nhân vật lệch mức chi tiết với dàn cảnh; mất đối lập ấm–lạnh ở s5 | Muốn đạt phải điêu khắc lại nhân vật và làm vật liệu dạ thật | **Không khả thi về render** trên hạ tầng hiện tại (8–23×); dễ bị so với phim stop-motion |
| **B Ink & Lamplight** | Bản sắc đồ hoạ mạnh nhất; silhouette và bóng đọc rõ; màu hẹp có chủ đích | Kết cấu dính màn hình; vòng sáng như sơ đồ; nhân vật tô phẳng lộ khối | Cần gắn kết cấu vào vật; viết lại cách tô vùng bán dạ | Vượt 2–3×; rung viền mực khi chuyển động |
| **C Painted Glow** ★ | Không khí và ánh sáng mạnh nhất; khung rộng ít "CG" nhất; nhanh nhất; đạt G3b | Lớp vẽ theo màn hình; nhân vật cận cảnh lộ khối | Cần ổn định lớp vẽ theo thời gian (gắn vào vật hoặc dùng luồng quang học) | "Kính tắm" hoặc nhấp nháy khi chuyển động: **phải thử bằng shot chuyển động ngay đầu vòng 2**; vượt 1,3–1,7× |

**Khuyến nghị C**, với 3 điều kiện ở vòng 2:
1. Thử một shot chuyển động 3–5 s (máy quay lia + Ida đi) để kiểm độ ổn định của lớp vẽ theo thời gian. Nếu nhấp nháy mà không sửa được trong ngân sách thì lùi về B.
2. Hạ về ≤ 2,5 s/khung: 4 mẫu (8 và 32 mẫu gần như không phân biệt được vì lớp vẽ che răng cưa); Kuwahara 28 → 16 mẫu; nướng sẵn vũng sáng đèn khí xa.
3. Nâng chất nhân vật trong `cast.js`, chung cho mọi hướng: mặt, tay, nếp vải.

## 6. Color script
`design/cong3/color-script/COLOR-SCRIPT.png`: 6 ô theo luật thế giới mục 5, kèm màu chủ đạo (hex) và cảm xúc từng cảnh. Là thumbnail màu giản lược; sau khi chọn hướng sẽ vẽ lại bằng chính hướng đó.
