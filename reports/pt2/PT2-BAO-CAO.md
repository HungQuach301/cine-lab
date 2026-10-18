Nhánh thật: `pt2-lai` (đúng lệnh) — tạo từ `origin/claude/pt-khung-neo-ab-test-njr9wp` @ `7adb88fa`. Harness của phiên chỉ định nhánh làm việc `ccr-ab204b7f-mmf94u`; phiên đẩy `pt2-lai` theo lệnh chủ dự án (xem §0, §12).

# PT2 — Khung neo LAI "A + C có kiểm soát" (H-C có rào chắn dữ kiện) + nâng lớp sống — BÁO CÁO

> Phiên R&D PT2, 18/10/2026, theo lệnh chủ dự án (duyệt J1, J3–J6, HC1–HC6 ngày 18/10). **Không merge. DỪNG chờ chủ dự án.**
> Mọi số là số đo thật trong phiên (tệp ở `reports/pt2/`) hoặc ghi rõ **(ước)**. Không có email, không có khoá API trong repo/báo cáo.

## 0. Khối điều lệ (lệnh + thực tế)
| Trường | Lệnh | Thực tế |
|---|---|---|
| Loại phiên | R&D PT2 | đúng |
| Nhánh | `pt2-lai` từ `origin/claude/pt-khung-neo-ab-test-njr9wp` (@7adb88f) | `pt2-lai` từ `7adb88fa`; ghi ở dòng đầu |
| Tệp được sửa | CHỈ `design/pt/**` + `reports/pt2/**` | chỉ hai vùng này: mới `design/pt/lai/**` (9 tệp), sửa `design/pt/scene/pt_site.py` + `build_scene.py` (tương thích ngược: mặc định = PT), mới `reports/pt2/**`. `scripts/`, `checks/`, `docs/`, `channel-*/` chỉ **đọc/chạy** (`tools/preflight.sh`, `checks/lock.py --verify` chạy, không đọc mã `checks/`). Ghost SH đọc bằng `git show` nhánh `claude/sh-ghost-gibraltar-t3-1gkftx` ra `/var/tmp/pt/ghost/` |
| Trần | Claude API ≤ $3 · OpenAI ≤ $5 · YouTube 0 · ElevenLabs 0 · giờ máy ≤ 5 h | **$1,417** (24 lượt chấm mù) · **$0,188** (3 lệnh sửa ảnh) · **0** · **0** · **≈ 3,6 h tiến trình** (≈ 1,9 h đồng hồ, chạy song song) — §8 |
| Preflight | bắt buộc; che email; không in/ghi khoá | `tools/preflight.sh` (129 tệp staged) **ĐẠT**; `checks/lock.py --verify` **KHỚP**. Khoá OpenAI do proxy gắn — mã không đọc biến khoá; khoá Claude chỉ truyền qua biến môi trường cho `claude -p` như PT |
| Video / ảnh | 540p ≤ 15 MB, không LFS; ảnh ≤ 30 MB | 2 video 540p **3,3 + 2,6 MB**; ảnh **27,6 MB** (tệp lớn nhất 4,7 MB < 5 MB — 3 ảnh C gốc bắt buộc lưu) |
| Dừng | không dừng hỏi giữa chừng | xong việc; câu hỏi không chặn tự quyết, liệt kê §12 |

## 1. Tóm tắt (đọc 2 phút)
1. **Hai khung neo phố hẹp, mỗi mốc 9 s ngày→đêm, làm đủ hai bản LAI và A-thuần nâng cấp** (cùng người, đám đông, đồ phố, chỉnh màu; khác duy nhất: bề mặt tường/mái/đất/đồ nền từ tấm C): **1782 hẻm mới** giữa khối Drinkwater K09/K10, nhìn tây ra Line Wall (trời **16,1 %**, đất trống **12,4 %**, cờ Union mẫu **1707**); **1943 Commercial Square** (máy PT; trời 13,5 %, đất 12,4 %, cờ 1801). Video 20 s: 1782 9 s · hoà 2 s · 1943 9 s.
2. **HC1–HC2 đạt bằng số đo:** một tấm C/khung neo × mốc, chỉ lượt ngày d2, sửa bằng `gpt-image-2.5-sunburst` `/v1/images/edits` với **mặt nạ từ lượt mã lớp Blender** (được sửa 62–66 % khung). Tài liệu OpenAI: mặt nạ "entirely prompt-based… may not follow its exact shape" — và thật vậy AI vẫn vẽ lại vùng bảo vệ → **ghép lại điểm ảnh A**: vùng bảo vệ LAI vs A **sai khác 0,000/255 ở 5/5 lượt nền 16 bit và 0,0/255, 0 % điểm ảnh khác ở 8/8 khung cuối** (sau lớp sống + chỉnh màu).
3. **HC4 kiểm dữ kiện:** 1 **lỗi chắc** (lần 1 tấm 1782: AI **dựng lại mái/tường cho các lô ĐỔ NÁT** Drinkwater ghi RUINS, và bỏ bóng hẻm) → sinh lại 1 lần; 1 nghi vấn (1943: AI đổi mép mái thành gờ đá chạm trổ) → xoá; **0 người/cờ/chữ/tàu/nguồn sáng mới**. Cuối: **0 lỗi chắc**, 1 sót nhẹ (≈ 0,05 % khung), **1 ngoại lệ chờ duyệt** (công-xon dưới ban công 1943). Rà bằng mắt 200 %/400 %, **không dùng chấm mù**.
4. **Lớp sống mới (HC3):** người **MakeHuman/MPFB (CC0)** dựng lại bằng bộ nạp tự viết — 6 vai/mốc × 8 hướng × (đứng + **chu kỳ đi 8 khung**), trang phục thời kỳ (áo đỏ đai chéo trắng mũ ba góc / pháo binh áo lam / battledress kaki, hải quân, RAF), **1943 không phụ nữ/trẻ em (S114)**; **33–57 người/khung ban ngày ở 10–60 m**, 5–16 ban đêm; vệt mờ phơi sáng; **bóng người theo mặt trời từng lượt, chỉ trên đất có nắng ở lượt nắng của cảnh A**.
5. **Ngày→đêm không sinh C đêm:** LAI_p = C × tỉ số đổ bóng A_p/A_d2 (lọc hình thái bỏ vệt gờ mảnh); đêm 1943 phong toả: **trần độ sáng 1,5× A**, không cửa sổ sáng, không đèn pha (PT có đèn pha 2D — không nguồn → bỏ).
6. **Chấm mù (3 người, ẩn nhãn, cùng khung): LAI thắng 22/24 phiếu** — craft **6,12 vs 4,75**, chi tiết **6,71 vs 3,58**, đúng thời kỳ 5,96 vs 5,29, **ai_look 3,79 vs 3,67 (gần như không tăng)**, toy_like 5,83 vs 6,67. A thắng 2/3 phiếu duy nhất ở 1943 chiều. Người chấm lại **gán nhầm "cờ 1801"** cho khung 1782 (cờ do mã vẽ đúng mẫu 1707) → xác nhận HC4d.
7. **Đo theo cách điều phối** (640×360, y 60–300): FIND_EDGES LAI **33–35 ngày** (A 13–24); bão hoà LAI 0,28–0,55, colorfulness 27–79 (§4).
8. **Đề xuất (§9):** chấp nhận LAI cho **khung neo phố hẹp có tường gần** với đủ 6 luật K đề xuất; việc phải làm trước khi lên phim: người (toy_like vẫn 5,8–6,0), tàu/hầm/đổ nát của A (vùng bảo vệ lộ chất lượng thấp hơn quanh nó), nguồn đồ phố 1943.

## 2. Việc đã làm (quy trình HC1–HC6 thực tế)
### 2.1 Nền A trước (HC1 bước 1) — `design/pt/scene/build_scene.py`, `pt_site.py`
- **Máy neo theo preset** `PT_CAM` (mặc định `pt` = PT không đổi). Góc mới `k1782`: UTM E 288 237,2 N 4 002 030,7 (đã tính SHIFT 1782 +6 m Đông của PT), cao **3,4 m**, hướng **268,7°** (trục hẻm), ngẩng 1°, 30 mm. Hẻm rộng 7–8 m theo bản nắn Drinkwater (RMS nắn 21 m — ghi rõ: vị trí hẻm có sai số cỡ chiều rộng hẻm). Kiểm trước khi dựng: **trời 16,1 % ≤ 25 %, đất trống 12,4 % ≤ 33 %** (lượt độ sâu + mã lớp, 640×360).
- **Đồ phố 1782 hẻm** (đặt tay, kiểm trống; đếm từ meta): 5 thùng, 5 đống gạch vụn nhỏ, 5 dầm gỗ chống tường, 2 đống đạn pháo, 1 đèn dầu, 1 pháo (**2 xe kéo không đặt được** — kiểm trống trượt trong hẻm 7–8 m) + **cột cờ trên Line Wall cuối hẻm (vị trí dựng — không có nguồn vị trí; mẫu cờ có nguồn)**. Lô đổ nát: 8 lô; PT2 đổi lòng nhà cháy thành **đá hộc ám khói** (bản PT: vữa nhạt → trông như hộp vữa xanh dưới ánh trời) → dựng lại 5 lượt.
- **Sửa dữ kiện của chính A:** (a) 1943 đêm: PT để cửa sổ sáng (gain 0,6) → **0** (phong toả); (b) 1943 **bỏ bao cát cửa** (PT đặt, **không có nguồn TIEN-KY**; cờ `PT2_NO_SANDBAG`, giữ chuỗi ngẫu nhiên → mọi hình học khác trùng; 143 146 → 133 618 mặt).
- **Lượt mới cho HC:** `--clspass` (EXR float32: `mã vùng × 64 + mã vật liệu`, 1 mẫu/điểm ảnh, lọc 0,01 — không pha mép); bộ đệm tách riêng **má cửa** (`vua_mo`), **phần đổ nát** (`*_do`), **gờ** (`vua_go`), **biển hiệu trơn** (`bien_hieu`) — cùng vật liệu, không đổi ảnh; `--sunvis` (chỉ mặt trời, vật liệu trắng, 960×540) cho bóng người.
- Cycles CPU 1080p @40 spp, 5 lượt + độ sâu + mã + nắng: **1943 v2 586 s** (chạy riêng), 1782 887 s / v2 987 s (chạy song song với sprite).

### 2.2 Tấm nền C (HC1 bước 2) — `design/pt/lai/gen_c2.py`, sổ `reports/pt2/ai-c/goi-api.jsonl`
- Model: `GET /v1/models` (200) + hướng dẫn đọc lại 18/10: `gpt-image-2.5-sunburst` ("editing precision matters most"). `POST /v1/images/edits`, 2048×1152, `quality: high`, PNG + mặt nạ PNG RGBA cùng cỡ (alpha 0 = được sửa), `stream` + 1 ảnh tạm (như PT §15.2). **API không có seed.**
- **Mặt nạ được sửa** = tường/mái/bao cát của toà (vữa, gạch, đá, ngói) + mặt đất + đồ nền (thùng, xe kéo, gạch vụn, dầm gỗ). **Giữ**: trời, đồi/chân trời, biển, tàu, Line Wall, cột cờ, pháo, đạn pháo, đèn, hầm, + trên toà: kính, lòng cửa, má cửa, cửa chớp, cửa, ban công, biển hiệu trơn, phần đổ nát.
- Prompt (nguyên văn trong sổ): giữ máy/khối/cửa/bóng; chỉ thêm chi tiết bề mặt; vật nền chỉ trong danh sách có nguồn (1782: thùng, gạch vụn, dầm gỗ cháy; **1943: không vật nào** vì TIEN-KY không có nguồn đồ phố 1943); **cấm người, cờ, chữ/biển hiệu, tàu, xe, đèn, cửa sổ sáng, nguồn sáng mới, cây, vật hiện đại**.
- 3 lệnh: 1782 lần 1 (**loại**, §5), 1782 lần 2 (dùng; prompt thêm "giữ bóng, không lợp lại nhà đổ nát"), 1943 lần 1 (dùng). Mỗi ảnh C đều có **C2PA `caBX`** khi tải về.

### 2.3 Lớp dữ kiện được bảo vệ (HC2) — `compose_c2.py`
- Vùng bảo vệ = mã lớp; vật ngoài toà nở 3 px, phần gắn trên toà nở 1 px (bản 3 px để lộ viền vữa A xám lam quanh mọi ô cửa — thấy ở rà 200 %, đã sửa). Giá trị 16 bit của A **chép thẳng** vào vùng bảo vệ (không qua phép tính) → **sai khác 0,000/255 ở d1, d2, d3, d4, n** cả hai khung (ghi trong `log/nen-*L-meta.json`).
- Vật loại ở HC4 → `--xoa-lop` ghép lại A: 1782 `9510` (thùng A), 1943 `vua_go,ngoi` (gờ + mép mái).
- Má cửa: mặt nạ GỬI AI giữ, nhưng khi ghép lấy điểm ảnh C (má cửa vữa phẳng của A lạc tông với tường C); nội dung má cửa được rà ở HC4 (0 người/vật trong ô cửa).

### 2.4 Ngày→đêm (HC3 phần nền) — không sinh C đêm
- **LAI_p = C × (A_p + ε)/(A_d2 + ε)** (tuyến tính): vân A triệt tiêu trong tỉ số → chỉ còn đổ bóng của hình học A; lượt d2 = đúng C. Log tỉ số lọc **mở + đóng hình thái 21 px** (bỏ vệt bóng gờ mảnh mà AI đã xoá — bản đầu để lại vệt tối như **dây điện** trên tường 1782); vùng C lệch bóng lớn so với A (0,33 % / 0,93 % khung) dùng tỉ số nội suy từ lân cận.
- Đêm: **trần LAI ≤ 1,5 × A cùng lượt** (bản 2,5× để lại mảng đất ấm như có đèn ở 1943 → trái phong toả). Đèn duy nhất = đèn của nền A (1782: 1 đèn dầu + cửa sổ 16 %; 1943: không cửa sổ sáng, đèn phố che chụp rất mờ).
- Đã thử và **bỏ** (ghi để không lặp lại): chuyển chi tiết tách vùng nắng/bóng σ40/σ150 (dải mờ ở gờ), kẹp độ sáng vùng lệch (mảng tròn phẳng), ghép A vùng lệch (mảng xám), vá ảnh + bóng A (mảng tròn).

### 2.5 Lớp sống (HC3) — `mh_people.py`, `live2.py`
- **Người:** MakeHuman/MPFB2 (CC0, cùng commit RIGHTS W4-MPFB). Chạy mã addon MPFB **bị bộ phân loại an toàn của phiên chặn** ("code from external") → phiên **tự viết bộ nạp chỉ đọc dữ liệu**: `base.obj` + targets macrodetails (nam/nữ trẻ, cơ, caucasian) + khung xương `rig.default` + trọng số. Trang phục: tô vùng theo xương chi phối trên lớp vỏ `helper-tights` của lưới gốc, `helper-skirt` cho vạt áo 1782 (dừng trên gối) / váy; đai chéo 1782, đai + dây đeo 1943, cổ áo hải quân; mũ ba góc / mũ tròn / mũ sắt Brodie / beret / mũ thuỷ thủ / mũ ca lô / mũ vải; súng hoả mai vác vai (1782 lính), súng trường (1943 lính).
- **Tờ sprite:** máy trực giao cùng hướng máy neo, cúi 8°, 110 px/m, 12 spp; 6 vai × 8 hướng × 9 ô × 5 lượt mỗi mốc (1 614 s + 1 530 s, chạy song song). Lỗi phát hiện: toạ độ chân tính trước khi cập nhật ma trận máy → sửa mã + tính lại từ tham số máy (không dựng lại).
- **Vai và tỉ lệ:** 1782: lính 56 %, pháo binh 16 %, thuỷ thủ 12 %, dân nam 12 %, dân nữ 4 % (phố sau pháo kích 4/1781, dân chạy về nam — S062); 1943: lính 50 %, hải quân 25 %, RAF 12 %, thợ 13 %, **0 phụ nữ/trẻ em** (S114).
- **Đám đông:** 140 tuyến đi/mốc giữa hai điểm đất nhìn thấy **10–60 m** (điểm giữa ≤ 62 m), tốc độ đám đông ×3 (1 chu kỳ bước = **8 khung** @24 fps), vệt phơi sáng 5 dấu lùi (1 / 0,24 / 0,12 / 0,06 / 0,03), mờ vào/ra 0,25 s; nhóm đứng hiện/tắt theo giờ ảo; đêm còn ~15 %. **Đếm thật:** ngày **33–57** người/khung (TB 44,7 / 41,4), đêm 5–16.
- **Bóng người:** hình người (alpha) biến đổi phối cảnh theo hướng + cot(độ cao) mặt trời của từng lượt (sun_alt/az của nền A), nhân lượt nắng của cảnh A → chỉ đổ trên đất có nắng; người đứng trong bóng nhà tắt phần nắng. Ví dụ hoàng hôn 1782: bóng dài đổ về máy.
- **Cờ** vẽ 2D theo mã: 1782 bản 1707–1801 (không chéo đỏ St Patrick), 1943 bản 1801 — không qua AI. Khói ống khói/tàu, hải âu, sao như PT; **bỏ đèn pha phòng không** (không nguồn).

### 2.6 Nhãn + công bố (HC5)
- Khung LAI: dòng **"Surface detail AI-assisted · layout, landmarks & flags from sources"** Inter Medium **38 px @1080p**, góc dưới trái, nền tối, **480/480 khung** (cả 48 khung hoà chuyển), dưới dòng nguồn bố cục; A-thuần giữ nhãn PT. Log mỗi khung `ai_image: true` (LAI 480/480) / `false` (A 480/480) — `reports/pt2/log/log-*-960x540.jsonl`.
- **C2PA:** 3/3 ảnh C gốc có chunk `caBX`; **tấm cuối sau ghép (PNG nền LAI, khung PNG/JPEG, MP4) KHÔNG còn C2PA** (phiên ghi tệp mới; kiểm chunk PNG + chuỗi `c2pa`/`jumb` trong MP4: không có). SynthID trong điểm ảnh: OpenAI nói "may survive some transformations" — **phiên không kiểm** (chưa gọi công cụ kiểm nguồn gốc). ⇒ YouTube không tự gắn nhãn qua C2PA, nhưng **nghĩa vụ công bố vẫn còn** (cảnh tả thực nơi có thật có chi tiết AI — chính sách đã chép ở `reports/pt/giay-phep/youtube-disclosing-genai.txt`).

## 3. Giấy phép (`reports/pt2/giay-phep/README.md`, nguyên văn)
| Tài sản | Nguồn | Giấy phép | Dùng |
|---|---|---|---|
| Vân nền A (9) | Poly Haven, tải lại 18/10, SHA 27/27 khớp PT | CC0 | như PT |
| Lưới người, targets, rig, trọng số | MPFB2 commit `3edf9df0…` (SHA base.obj/rig/weights khớp RIGHTS W4-MPFB) | CC0 1.0 (LICENSE.md mục C); đầu ra không mang logic chương trình (mục D) | người đám đông khung neo — **cần dòng RIGHTS mở rộng phạm vi (W4-MPFB-A5)** |
| Ảnh C (3) | OpenAI `gpt-image-2.5-sunburst` | Services Agreement §4.1/§4.4 như PT | **chỉ nghiên cứu** đến khi chủ dự án duyệt |
| Font Inter | có sẵn | SIL OFL 1.1 (RIGHTS K2-F1) | nhãn |
| Ghost SH 1782/1943 | nhánh SH (git show) | như SH | khối nhà |

## 4. Số đo (`reports/pt2/do/do-khung.json`) — cách điều phối: toàn khung → 640×360 INTER_AREA, cắt y 60–300
| Khung (giờ ảo khai trước) | LAI bão hoà / colorfulness / FIND_EDGES | A-thuần | Vùng bảo vệ LAI vs A (TB /255 · % điểm ảnh khác) |
|---|---|---|---|
| 1782 sáng 10,0 | 0,282 / 43,4 / **35,0** | 0,200 / 42,5 / 13,0 | 0,0 · 0 % |
| 1782 trưa 12,8 (= giờ tấm C) | 0,298 / 41,3 / **35,0** | 0,251 / 38,4 / 13,9 | 0,0 · 0 % |
| 1782 chiều 17,55 | 0,294 / 27,2 / 20,4 | 0,620 / 39,4 / 9,8 | 0,0 · 0 % |
| 1782 đêm 21,8 | 0,573 / 37,2 / 5,3 | 0,561 / 36,7 / 3,3 | 0,0 · 0 % |
| 1943 sáng | 0,486 / **79,4** / 33,5 | 0,235 / 32,9 / 24,1 | 0,0 · 0 % |
| 1943 trưa | 0,478 / 71,3 / 33,4 | 0,216 / 24,9 / 23,8 | 0,0 · 0 % |
| 1943 chiều | 0,545 / 73,4 / 28,6 | 0,278 / 30,2 / 23,3 | 0,0 · 0 % |
| 1943 đêm | 0,667 / 24,6 / 2,6 | 0,667 / 24,5 / 2,7 | 0,0 · 0 % |
- Nền: **% trời 16,07 (1782) / 13,51 (1943)**; **% mặt đất 12,39 / 12,36**. Người: ngày 33–57, đêm 5–16 (từ log, mọi khung). Vật nền (meta): 1782 A 5 thùng · 5 đống gạch vụn (+ gạch vụn trong 8 lô đổ nát) · 5 dầm gỗ · 2 đống đạn pháo · 1 đèn · 1 pháo · 1 cột cờ · 6 tàu buồm + 5 thuyền nhỏ; LAI thêm 3 thùng + gạch vụn chân tường + ≈ 6 dầm gỗ (HC4); 1943 A 3 đèn · 1 xe kéo · 3 thùng · 1 cột cờ · hầm (bao cát hầm) · 102 chậu cây · 40 mái che · 5 tàu máy + 1 thuyền buồm; LAI không thêm vật.
- **Đọc:** C nâng chi tiết FIND_EDGES ×2,5 (1782) / ×1,4 (1943). Bão hoà/colorfulness 1943 LAI **cao hơn mốc đối thủ** điều phối từng cấp (Timelapse Studio Rome 0,28/26/26) vì AI đổi màu sơn + chỉnh màu chung ×1,85 của PT áp lên tấm đã giàu màu → **tông vàng–cam đậm** (1943 chiều 0,545/73,4). Đề xuất hạ hệ số bão hoà riêng cho LAI nếu chọn LAI (chưa làm — giữ chỉnh màu chung để so công bằng). 1782 chiều A bão hoà 0,62 là trời lam đậm + tường xanh lam trong bóng của A.
- Chi phí OpenAI thật: **$0,06254 + $0,06291 + $0,06234 = $0,18779** (1 508 token ảnh vào + 323–438 token chữ + 1 522 token ra + 100 token ảnh tạm mỗi lệnh; 30–33 s).

## 5. Kiểm dữ kiện (HC4) — `reports/pt2/kiem-du-kien.json`, bằng chứng `reports/pt2/kiem/bang-chung-400.jpg`
Cách: so A↔LAI theo vùng (bản đồ khác biệt cấu trúc + màu bão hoà, `kiem_c.py`) trên **kết quả ghép thật**; rà tay 16 ô 200 % mỗi khung × 3 vòng; phóng 400 % từng vật nghi ngờ; đối chiếu danh sách vật nền cho phép có nguồn (1782: thùng — S051; gạch vụn, vết bong vữa, muội, mảnh pháo — S062/S063 + ghost RUINS; dầm gỗ cháy — S063; 1943: **chỉ bề mặt**). **Không dùng chấm mù.**

| # | Khung | Phát hiện | Loại | Xử lý |
|---|---|---|---|---|
| — | 1782 lần 1 | AI **lợp mái + xây liền tường** các lô ĐỔ NÁT; bỏ bóng nhà trên lòng hẻm | **LỖI CHẮC** (đổi dữ kiện) + trái HC1 | **sinh lại lần 2** + bảo vệ phần đổ nát (`*_do`) |
| — | 1782 lần 2 | AI vẫn vẽ lại lô đổ nát (tường có gờ) **trong vùng bảo vệ** | vi phạm mặt nạ | HC2 đã thay bằng A — không còn trong kết quả |
| V1–V5 | 1782 | 3 thùng gỗ; gạch vụn chân tường; ≈ 6 dầm gỗ cháy; bong vữa/muội/vết mảnh pháo; đất nện có vệt bánh xe | trong danh sách, có nguồn | giữ |
| V6 | 1782 | AI thay 2 thùng A bằng gạch vụn → bóng thùng A in lên gạch vụn khi chiếu sáng | lỗi **ghép** | ghép lại thùng A. *Sửa sổ:* lần rà đầu ghi "thùng kim loại đục lỗ" — đó là sản phẩm bước ghép bản đầu của phiên, không phải AI (phát hiện ở 400 % lần 2) |
| V7 | 1782 | AI xoá gờ tầng/gờ mái thủ tục của A | không phải vật thêm (gờ A không nguồn) | giữ C, lọc vệt bóng gờ |
| W1 | 1943 | AI **đổi màu sơn**: toà trái hồng → vàng đất, toà phải kem → hồng loang | không lỗi dữ kiện (màu A là bảng màu thủ tục) | giữ — **chờ chủ dự án** |
| W2 | 1943 | vữa bong, loang ẩm, đá lát mòn | bề mặt | giữ |
| W3 | 1943 | AI đổi mép mái/gờ mái thành **gờ đá chạm trổ + công-xon** | **nghi vấn** (kiến trúc ngoài danh sách) | xoá: ghép lại gờ + ngói A (vòng 1 chỉ gỡ lớp gờ — chạm trổ nằm trên lớp ngói, thấy ở 400 % vòng 2); **sót** vài vệt nhỏ trên tường ngay dưới mái trái ≈ 0,05 % khung |
| W4 | 1943 | bao cát (PT đặt) — AI xoá → bóng ma | vật **không nguồn trong chính A** | bỏ khỏi A 1943 ở cả hai bản |
| W5 | 1943 | công-xon dưới 3 ban công AI vẽ trên tường (không bóng), 0,33 % khung | **ngoại lệ** — chi tiết phụ của ban công (vật bảo vệ), không mang dữ kiện thời kỳ | giữ C (ghép A / vá ảnh để lại mảng tròn thấy rõ ở 400 %) — **chờ duyệt**; nếu không chấp nhận: sinh lại 1943 lần 2 |
- **Vật cấm trong kết quả: 0 người, 0 cờ mới, 0 chữ/biển hiệu, 0 tàu mới, 0 nguồn sáng mới, 0 vật hiện đại** (cả hai khung).
- **Tổng:** trước xử lý 1 lỗi chắc + 1 nghi vấn (+ 2 lỗi ghép của phiên); **cuối 0 lỗi chắc, 0 nghi vấn nặng, 1 sót nhẹ, 1 ngoại lệ chờ duyệt** → hai tấm được dùng cho thử nghiệm này. So PT nhánh C (không rào chắn): 4 lỗi chắc + 3 nghi vấn / 6 khung, trong đó cờ 1707 → 1801 ×3 — với HC2 lỗi cờ **không thể xảy ra** (cờ không qua AI).
- **Giờ người rà thật:** ≈ 1 h cho 2 tấm (gồm 3 vòng rà sau mỗi lần sửa ghép và làm bảng chứng); ổn định ước **20–30 phút/tấm** (ước).

## 6. Chấm mù (`design/pt/lai/blind_lai.py`, `reports/pt2/kiem-mu/`: key, X/Y, phiếu thô, `score.json`)
Giao thức như PT: `claude -p` ghim **claude-sonnet-5-5** (sổ ghi phục vụ `sonnet-5-5` + `haiku-5-5` phụ trợ của CLI), chỉ Read, thư mục tạm chỉ X/Y, 3 vai nguyên văn `blind_v2.py`, ẩn nhãn, hạt giống 20261018; 8 cặp (2 khung neo × 4 giờ khai trước) × 3 = 24 phiếu, **không chữ**. Thang PT + **toy_like 0–10**. Không khung đối thủ (điều phối tự so trong chat — gợi ý `reports/pt2/to-khung-LAI-A.jpg`).

| | craft | chi tiết | đúng thời kỳ | ai_look | toy_like |
|---|---|---|---|---|---|
| **LAI (8 khung)** | **6,12** | **6,71** | **5,96** | 3,79 | **5,83** |
| A-thuần | 4,75 | 3,58 | 5,29 | 3,67 | 6,67 |
| 1782 LAI / A | 6,42 / 4,42 | 7,25 / 3,08 | 5,83 / 4,67 | 3,58 / 3,83 | 5,67 / 6,75 |
| 1943 LAI / A | 5,83 / 5,08 | 6,17 / 4,08 | 6,08 / 5,92 | 4,00 / 3,50 | 6,00 / 6,58 |
- "Tốt hơn": **LAI 22, A 2** (cả 2 ở 1943 chiều: A craft 6,33 vs LAI 6,0 — LAI vàng cam đậm). Cờ lặp: `toy_like` ở **mọi khung cả hai bản** (người "mannequin", "generic uniforms"), `cluttered` ở LAI, `flat_slide_look` + `empty_frame` ở A.
- **Người chấm sai dữ kiện:** 1782 cả 3 người ghi "Union Jack post-1801 / St Patrick's cross" ở ≥ 3 khung — **sai** (cờ do mã vẽ, không chéo đỏ); R2 lại cho là "plausibly the 1606 Union flag". ⇒ như PT: chấm bằng mô hình không thay được kiểm dữ kiện.
- **Lưu ý tính nhất quán:** phiếu chấm trên lượt sản xuất thứ 2 (trước khi nâng mật độ ban ngày và gỡ gờ mái chạm trổ 1943). Nền, vùng bảo vệ, chỉnh màu giống bản cuối; khác: số người đi (bản chấm có khung 26–29 người) và mép mái 1943. Ảnh đã chấm lưu ở `reports/pt2/kiem-mu/*/X.jpg|Y.jpg`. Không chấm lại để giữ trần Claude ($1,417 + 24 lượt nữa ≈ $2,83 sát trần dừng $2,7).

## 7. Giờ máy, chi phí, dung lượng (`reports/pt2/log/gio-dung.txt`)
| Khoản | Trần | Thực tế |
|---|---|---|
| Claude API | $3 | **$1,417** (24 lượt; `reports/pt2/kiem-mu/cost.jsonl`) |
| OpenAI API | $5 | **$0,188** (3 lệnh `/v1/images/edits`) |
| YouTube / ElevenLabs | 0 / 0 | 0 / 0 |
| Giờ máy | ≤ 5 h | **≈ 3,6 h tiến trình** (≈ 1,9 h đồng hồ do chạy song song): nền A 887 + ≈ 1 800 (lần 1943 bị cắt ở giới hạn 30 phút của trình chạy nền sau d4) + 242 + 987 + 586 s · lượt mã dựng lại ≈ 90 s · sprite 1 614 + 1 530 s + thử ≈ 750 s · ghép HC2 ≈ 420 s · rà ≈ 100 s · thử lớp sống ≈ 200 s · 5 lượt sản xuất (2 bản) ≈ 1 200 s |
| Dung lượng | video ≤ 15 MB; ảnh ≤ 30 MB | video **5,8 MB**; ảnh **27,6 MB** (3 ảnh C gốc 13,7 MB bắt buộc lưu) |
- **Dòng COST-LEDGER đề xuất (P ghi):** `PT2-01,khung neo LAI A+C có rào chắn + lớp sống MPFB,R&D,2026-10-18,,,,,1.42,3,claude-sonnet-5-5,0,0,≈ 3,6,,0,20,OpenAI $0.19 (gpt-image-2.5-sunburst ×3),reports/pt2/PT2-BAO-CAO.md,YouTube 0; không merge`

### 7.1 Ước cho một tập 10–15 phút (ước, máy này 4 lõi CPU, 1080p)
| Hạng mục | Mỗi khung neo × mốc | 6 khung neo × 2 mốc = 12 |
|---|---|---|
| Nền A 5 lượt + độ sâu + mã + nắng | 0,16–0,25 h | 2–3 h |
| Sprite người (theo hướng máy; dùng chung nếu hướng gần nhau ±20°) | 0,3–0,45 h (song song) | 0,9–5,4 h |
| Tấm C (1 + ≤ 0,5 lần sinh lại TB) | $0,06–0,13 · 1 phút | **$0,75–1,5** |
| Ghép HC2 + chiếu sáng 5 lượt | 0,01 h | 0,1 h |
| Lớp sống 1080p 216 khung (≈ 1,2 s/khung) | 0,07 h | 0,9 h |
| **Người rà dữ kiện (HC4)** | 20–30 phút | **4–6 giờ người** |
| **Tổng máy** | | **≈ 4–9 h** (GPU giảm mạnh phần Cycles) |
- Thời lượng `ai_image` nếu mọi khung neo là LAI: 12 × 9 s = 108 s ≈ **12–18 % thời lượng tập**.

## 8. Việc cần chuyển vào V6
1. **Người (vẫn `toy_like` 5,8–6,0):** mặt/tóc/bàn tay, nếp vải (giãn vỏ áo theo pháp tuyến thật), 2–3 dáng người/vai, tư thế đứng nói chuyện/làm việc, súng cầm tay; kiểm toy_like ≤ 4.
2. **Vật bảo vệ của A lộ chất lượng thấp** cạnh tường C chi tiết: tàu 1943 (khối hộp), hầm trú ẩn, lòng nhà đổ nát 1782, cột cờ/đèn. Vì không qua AI, phải dựng tốt hơn bằng A.
3. **Nguồn đồ phố 1943** (TIEN-KY T3 chưa có): ảnh PD đường phố Gibraltar thời chiến → danh sách vật nền 1943 (bao cát, hòm, xe…). Không có nguồn thì 1943 chỉ có bề mặt.
4. **Màu sơn mặt tiền:** chủ dự án quyết nguồn màu (ảnh màu/tranh thời kỳ) — C đổi màu tự do khi A không có nguồn.
5. **Chỉnh màu riêng cho LAI** (tấm C đã giàu màu; ×1,85 làm 1943 vàng cam đậm — lý do A thắng 1943 chiều).
6. Công cụ: `mh_people.py` (bộ nạp MPFB tự viết, đã sửa lỗi toạ độ chân); `compose_c2.py` (ghép + tỉ số đổ bóng); `kiem_c.py`/`bang_chung.py` (rà); lượt mã lớp/nắng trong `build_scene.py`. Trình chạy nền: tách lệnh dài > 30 phút (lần dựng 1943 đầu bị cắt).
7. `OpenEXR` vào `/opt/cine` (lại phải cài trong phiên — PT §10.8 đã đề xuất thêm vào `verify.sh`).

## 9. Quyết định đề xuất
### Q-PT2-1 — Dùng LAI (A + C có rào chắn) cho khung neo của kênh?
| Phương án | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|
| **A. LAI cho khung neo phố hẹp, kèm 6 luật K dưới — đề xuất có điều kiện** | thắng 22/24 phiếu; craft +1,37, chi tiết +3,13, thời kỳ +0,67; **ai_look gần như không tăng (+0,12)**; dữ kiện mang thông tin (cờ, tàu, mốc, ô cửa, đổ nát, đèn) trùng A **0/255**; lỗi kiểu "cờ 1801" bị loại theo cấu trúc; rẻ ($0,06/tấm) | 4–6 giờ người rà/tập; AI vẫn đổi thứ không bị bảo vệ (màu sơn, gờ, công-xon); cần sinh lại khi AI đổi dữ kiện (1/3 lần); vùng bảo vệ của A lộ chất lượng thấp | phải bỏ "No AI imagery" cho khung LAI; dòng phương pháp 38 px; sổ `kiem-du-kien` mỗi tấm | công bố AI theo YouTube (cảnh tả thực, nơi có thật) — dù C2PA đã mất sau ghép, SynthID có thể còn; quyền đầu ra "to the extent permitted by law" |
| B. A-thuần nâng cấp (người MPFB, bóng theo nắng, sửa dữ kiện A) | "No AI imagery" giữ nguyên; không rà AI; mọi điểm ảnh có nguồn hoặc thủ tục | thua rõ (craft 4,75, chi tiết 3,58, `flat_slide_look`) | tiếp tục V6 mục 1–2 | khoảng cách chất lượng với kênh dùng AI |
| C. LAI chỉ cho mốc có danh sách vật nền có nguồn (hiện: 1782), A cho mốc chưa có (1943) | giảm phạm vi AI | hai phong cách trong một tập | như A nhưng hẹp | như A |

### Q-PT2-2 — Luật K đề xuất (phiên K viết; không sửa `checks/`)
1. **K-LAI-1 thời lượng:** tổng giây khung `ai_image: true` ≤ **20 %** thời lượng tập (đề xuất trần; chủ dự án quyết số).
2. **K-LAI-2 nhãn:** mọi khung `ai_image: true` có dòng phương pháp ≥ 38 px @1080p góc dưới trái **suốt shot** (log `nhan_phuong_phap: true` + kiểm vùng chữ).
3. **K-LAI-3 kiểm dữ kiện:** mỗi tấm C có mục trong `kiem-du-kien.json` với `loi_chac_cuoi = 0`, `nghi_van` đã xử lý, ngoại lệ có duyệt của chủ dự án; không dùng chấm mù làm bằng chứng.
4. **K-LAI-4 vùng bảo vệ:** khung LAI vs A-thuần cùng khung, không chữ, PNG: sai khác TB **< 1/255** trên `bao_ve.png`; trời/cờ/tàu/mốc/ô cửa/đèn luôn trong vùng bảo vệ.
5. **K-LAI-5 một tấm, ban ngày:** ≤ 1 tấm C/khung neo × mốc, chỉ lượt ngày; ≤ 2 lần sinh lại; không sinh C đêm; đêm không sáng hơn 1,5× A.
6. **K-LAI-6 sổ AI:** `goi-api.jsonl` mỗi lệnh: model, prompt nguyên văn, % mặt nạ được sửa, usage, $ , C2PA, giờ.

## 10. Chỉ số trong ±5 % quanh ngưỡng
- **Nhãn phương pháp 38 px** = đúng ngưỡng ≥ 38 px (0 %).
- **Chu kỳ đi 8 khung** = đúng ngưỡng ≥ 8 (0 %).
- **Khoảng cách người tối thiểu 10,0 m** = đúng ngưỡng (luật cứng trong mã: lấy mẫu bỏ < 10 m).
- Không chỉ số nào khác trong ±5 %: người/khung ngày 33–57 (ngưỡng 30–80: +10 %); trời 16,1 / 13,5 % (ngưỡng 25 %); đất 12,4 % (33 %); vùng bảo vệ 0/255 (ngưỡng 1/255); ảnh 27,6/30 MB (−7,9 %); video 5,8/15 MB; Claude $1,417/$3; OpenAI $0,19/$5; giờ máy 3,6/5 h (−28 %).

## 11. Tệp
- **Mã mới** `design/pt/lai/`: `mh_people.py`, `gen_c2.py`, `lai_common.py`, `compose_c2.py`, `kiem_c.py`, `bang_chung.py`, `live2.py`, `measure2.py`, `blind_lai.py`, `sheet_lai.py`, `README.md`. **Sửa** `design/pt/scene/pt_site.py` (preset máy), `build_scene.py` (preset đồ phố k1782, lượt mã lớp + nắng, tách bộ đệm má cửa/đổ nát/gờ/biển hiệu, lòng nhà đổ nát, 1943 đêm không cửa sổ sáng, cờ `PT2_NO_SANDBAG`) — mặc định vẫn ra cảnh PT (trừ hai sửa dữ kiện 1943 đêm).
- **Báo cáo** `reports/pt2/`: `pt2-LAI-540p.mp4`, `pt2-A-540p.mp4`, `to-khung-LAI-A.jpg`, `to-chuoi-HC.jpg` (A → mặt nạ → C thô → LAI), `khung/` (16 khung không chữ + 4 khung có chữ), `ai-c/` (3 ảnh C gốc gồm lần 1 bị loại, 3 mặt nạ, sổ gọi API), `kiem-du-kien.json`, `kiem/bang-chung-400.jpg`, `do/do-khung.json`, `kiem-mu/`, `log/` (log khung, meta nền A/LAI, sprite, giờ dựng), `giay-phep/README.md`.
- **Đề xuất ngoài vùng (chưa ghi):** RIGHTS: dòng W4-MPFB-A5 (mở rộng phạm vi sang người đám đông khung neo), 3 dòng ảnh C "chỉ nghiên cứu" (đến khi Q-PT2-1 duyệt); AUTHORSHIP: Q-PT2-1/2, chọn góc hẻm K09/K10, bỏ bao cát 1943; COST-LEDGER dòng PT2-01; `verify.sh` kiểm `OpenEXR`.

## 12. Việc chờ chủ dự án
1. **Q-PT2-1** (LAI / A-thuần / LAI một phần) và **Q-PT2-2** (6 luật K, gồm con số trần thời lượng `ai_image`).
2. **W5** công-xon dưới ban công 1943 (ngoại lệ HC4): chấp nhận hay sinh lại 1943 lần 2.
3. **W1** màu sơn 1943 do AI đổi (A cũng không có nguồn màu): chấp nhận, hay cần nguồn màu trước.
4. **Nhánh:** harness chỉ định `ccr-ab204b7f-mmf94u`; phiên đẩy `pt2-lai` theo lệnh. Nếu cần nhánh `claude/...` thì P tạo từ commit cuối của `pt2-lai`.
5. Nguồn đồ phố 1943 cho danh sách vật nền (V6 mục 3); cột cờ cuối hẻm 1782 có vị trí dựng (không nguồn vị trí).
6. Ghi các đề xuất ngoài vùng §11 (RIGHTS, AUTHORSHIP, COST-LEDGER, verify.sh).
7. Chấm lại mù trên bản cuối nếu chủ dự án muốn số khớp tuyệt đối (§6, ≈ $1,4).
8. So với Timelapse Studio trong chat (điều phối) — tờ `reports/pt2/to-khung-LAI-A.jpg` và hai video.
