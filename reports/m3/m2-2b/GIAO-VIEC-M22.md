# Giao việc M2.2 · hoàn thiện trên nền animatic v3 (P, 04/10/2026)

Chủ dự án đã duyệt animatic v3 (71b68e2). M2.2 **chỉ render lại shot hoặc đoạn bị sửa**. Mọi luật của `reports/m3/CHUAN-KENH-LL.md` vẫn áp, gồm §6 (đĩa) và §7 (nguồn số không dùng Wikipedia làm nguồn chính).

## Chung
- **Timeline mới:** `reports/m3/m2-2b/timeline-v4.json`. Đoạn móc 00 dài 6 s (144 khung) chèn trước đoạn 01, nên **mọi t0 tuyệt đối +6 s**. Số khung từng đoạn không đổi.
- **Đầu ra:** `/var/tmp/cine-out/ep01/sec-m22/<NN>.mkv`.
  - H.264 `-c:v libx264 -preset medium -crf 10 -pix_fmt yuv444p -g 48`, 1920×1080, 24 fps, không tiếng, đúng số khung.
  - **Không ghi đè** `/var/tmp/cine-out/ep01/sec/` (bản đã duyệt).
- **Cue SFX mới:** `/var/tmp/cine-out/ep01/sfx4/<NN>.json`, `at_abs` theo **timeline v4**. Các cue cũ ở đó đã cộng sẵn +6 s.
- **Judder:** tự chạy `python3 scripts/p/judder.py` trên trung gian, mục tiêu `loi == 0` và `giu_co_y_ge_1s == 0`. **Xem khung** (lưới khung thu nhỏ) để bắt lỗi máy trôi hoặc xuyên hình. Judder không bắt được các lỗi này.
- **Tương phản chữ ≥ 4,5:1**, đo trên clip. Cỡ chữ thông tin tối thiểu ở bản 720p: chữ hoa cao ≥ 12 px ở 720p, tức ≥ 18 px ở 1080p. Chữ nguồn tối thiểu cũng theo mức này.
- **Đĩa:** kiểm `df -h /` trước mỗi render dài; dừng khi trống < 6 GB. Xoá PNG hoặc tệp tạm sau khi xong.
- **Ảnh khung trước/sau:** ghi vào `/var/tmp/cine-out/ep01/m22/truoc-sau/<mục>-truoc.jpg` và `-sau.jpg`, 1280×720, cùng thời điểm.
- **Mã:** commit cục bộ trên nhánh được giao, không push. Cuối gói xuất bản vá ra `/var/tmp/cine-out/ep01/m22/ma-<gói>.patch` bằng `git diff lat-cat-m22a HEAD --binary`.
- **Báo cáo:** trả trong lời trả về, gồm:
  - từng mục: cách làm, khung, judder, tương phản, s/khung;
  - chữ trên hình mới;
  - chỉ số nằm trong ±5 % quanh ngưỡng;
  - token tự ước.

## Gói HISTORY-M22 (nhánh `ep01-history`)
1. **3.1 · Bản đồ** London (02), Paris/Opéra (05), New York 1907 (06): người xem phải nhận ra thành phố trong 2 s.
   - Vẽ đường bờ sông đúng dáng: Thames uốn qua Westminster–City, mũi Isle of Dogs; Seine với Île de la Cité. Vẽ đường bờ Manhattan (đảo dài, mũi nam Battery, sông Hudson/East River).
   - Thêm 2–3 nhãn địa danh mỗi bản đồ (ví dụ "Thames", "Westminster", "Pall Mall"; "Seine", "Opéra", "Louvre"; "Manhattan", "Hudson River", "Broadway").
   - Giữ phong cách cắt giấy.
   - Dữ liệu đường bờ: tự vẽ giản lược theo hiểu biết địa lý công khai. Nếu tải dữ liệu thì chỉ dùng Natural Earth (public domain) và ghi lại để P vào RIGHTS. **Không** dùng tile bản đồ hay ảnh có bản quyền.
2. **3.5 · Đoạn 02 dựng lại theo lời dẫn mới** (thu lại, `reports/m3/m2-2b/vo/bill-02-m22.mp3` cùng `.align.json`; thời lượng đoạn giữ 32,04 s = 769 khung, vo_offset 4,0 s). Câu 2 mới: "The idea spread fast. Within a few years, gas lamps ran along street after street across London." (lời cũ có "1820s… forty thousand… 215 miles").
   - **Bỏ hẳn** khỏi hình: nhãn "1820s · 40,000+ lamps · 215 miles" và chữ "1820s" trong ô tựa.
   - Mạng phố sáng dần như rễ cây theo câu mới. Mốc theo align mới.
   - Dòng nguồn: bỏ Wikipedia, chỉ còn "Sources: London Remembers · English Heritage" cho mốc Pall Mall 1807.
   - Cue SFX đoạn 02 làm lại theo mốc mới, ghi vào `sfx4/02.json`.
3. **3.2 · Cuối đoạn 09:** khi hai bảng thu nhỏ, mọi chữ còn hiện phải ≥ cỡ tối thiểu. Nếu không đủ chỗ thì **chỉ giữ con số nổi bật** (421k; 3.92M) và tên ngắn, mờ phần chữ nhỏ trước khi thu. Đo lại tương phản ở trạng thái thu nhỏ.
4. Render lại các đoạn 02, 05, 06, 09 (đúng 769 / 589 / 659 / 664 khung).

## Gói STORY-M22 (nhánh `ep01-story`)
1. **3.3 · e04b** (đồng hồ bỏ túi, đoạn 04 5–8 s, 72 khung): chỉnh khung (tiêu cự, vị trí, nhìn) để mặt đồng hồ **không bị cắt ở mép** suốt shot, vẫn chỉ 7:53.
2. **3.4 · e19a** (Ida thắp ngọn thứ hai, đoạn 19 0–7,5 s, 180 khung; shot bắt buộc giữ người thật): đổi sang **cỡ trung hoặc cận trung** để đọc được động tác (sào mồi chạm, đèn bừng ở ≈ 5,08 s của đoạn). Không cận mặt. Giữ chạng vạng muộn (`dusk`), giữ hướng nhìn nối với e19b.
3. Render lại đúng 2 shot, ghép lại đoạn 04 (378 khung) và 19 (950 khung) từ clip shot ở `/var/tmp/cine-out/ep01/story/clip/{04,19}`. Thay riêng clip shot bị sửa bằng bản mới, giữ các clip khác. `ghep_doan.py` đang ghi ra `sec/`; hãy cho nó ghi ra `sec-m22/`.
4. Lỗi trôi máy cộng dồn đã được P sửa ở commit `bada6bc`. Sau khi render, xem khung kiểm lại.
