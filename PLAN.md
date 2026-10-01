# PLAN — Bảng điều phối (phiên P duy trì)

## Mốc hiện tại: **Cổng 6 ĐÃ ĐÓNG 01/10/2026** (main, layout-v22 = `screening/layout.mp4`, `reports/m2/CONG-6-DONG.md`) · **CHUYỂN HƯỚNG (01/10/2026): kênh lai **Last Lamplighters** (chủ dự án chọn tên 01/10/2026; trục nghề xưa ↔ nghề hôm nay dưới AI)** — Mốc 1 BÀI THỬ PHONG CÁCH (B1 toon + viền nét; B3 2.5D cắt giấy; nhánh `thu-phong-cach` từ main, bật bằng cờ, `reports/m3/THU-PHONG-CACH.md`) + GÓI KỊCH BẢN TẬP THỬ "The Last Lamplighters" (`reports/m3/KICH-BAN-TAP-THU.md`) chạy song song · THỬ MẶT 2 DỪNG (bỏ hướng A) · Cổng 7 không mở · chưa mở kênh · checks v1.5 (LOCK 8d55b6ad…)

Quy ước nhánh: mọi nhánh làm việc tạo từ `main` (đã hợp nhất M0 + checks/v0 ngày 27/09/2026, LOCK KHỚP `57dc729b…`). Chỉ P merge vào `main`.
Video > 30 MB: đẩy lên nhánh git, không gửi qua giao diện.

## Hàng chờ chủ dự án duyệt
0. **Cổng 6 — diễn hoạt: W2 ĐÓNG (30/09/2026, chủ dự án duyệt sau khi xem clip v19). W1 MỞ 30/09/2026 (+ B2 s23, B3 hướng ánh cảnh 4, B4 mục treo W2); v1 kiểm mù TRƯỢT → **W1-v2 phương án A đang chạy** (dàn dựng mặt cận, L3/L4 chặn, Đ1–Đ3) — AUTHORSHIP "Cổng 6 — diễn hoạt"** — chỉ thị và quyết định: AUTHORSHIP "Cổng 6 — diễn hoạt". Nhịp: khôi phục môi trường (npm ci, dò lệch 0 px) → sửa bộ xuất C3 cho cả Cas (`export_c3.js --who`, `scripts/p/c3_hai_nv.sh`; khiếu nại "C3 một nhân vật" chờ K trong checks-appeal.md) → **W2** (hạn ~1,5 triệu token, tối đa 2 vòng) → P: luật v1.5 (C3 Ida + Cas), kiểm mù 10 dải + 2 đối chứng, cine-continuity cảnh 4–6 → báo cáo `reports/m2/CONG-6-W2.md` → **DỪNG**. **Vòng 1 xong (layout-v17): luật như v16, kiểm mù TRƯỢT, continuity 1 chặn. Vòng 2 (cuối) đang chạy; Đ3 duyệt, Đ4 = (b), Đ5 không làm, Đ6 +x (AUTHORSHIP 30/09). Vòng 2 trượt thì KHÔNG làm vòng 3.**
1. **Cổng 6 — MỞ (29/09/2026), kế hoạch duyệt** (CONG-6-MO.md mục 4). Nhịp: **gói W4 nhân vật (XONG) → DỪNG (đang chờ duyệt CONG-6-W4.md) → W1 + W2 → kiểm.** W1/W2 CHƯA mở, chưa diễn hoạt. Báo cáo gói W4: reports/m2/CONG-6-W4.md.
2. **checks v1.5 ĐÃ DUYỆT và merge vào main (08c07dd, LOCK 8d55b6ad…).** Q-P0c: "phần lớn trong mặt nạ" = phản chứng + mặt nạ chạm hộp + khớp biên cục bộ. **Q-C3h: Ida giữ `c3_head_axis` 'pca'; Cas v1.6 khai 'doc' và đo c3_views theo 'doc'.** Khâu render xuất `silhouettes` (RUN.md 3.6.3) cho mọi khung P0 lấy mẫu. **Theo dõi s33:** độ khớp biên cục bộ P0 1,61 (ngưỡng 1,5) — render lại mà dưới 1,5 thì báo, không sửa hình để lách.
3. **Cổng 6 nhân vật XONG (29/09/2026):** khoá v1.5.1 + v1.6 (2f05a4b; LOCK-THIẾT-KẾ 34/34), layout-v16 + luật v1.5 (P0 ĐẠT; C3/H1b/G3b trượt như v15), **merge main 3c40f03**. Báo cáo reports/m2/CONG-6-KHOA.md. **Kế hoạch W1/W2** (reports/m2/cong6/KE-HOACH-W1-W2.md) **CHỜ chủ dự án quyết mở**. Kiểm mù: **10 khung** mỗi lần (chủ dự án chốt khi bàn giao). Việc chờ quyết: C3 cho Cas (hiện luật chỉ đo Ida). **Bàn giao phiên P: PLAN-HANDOFF-P.md.**
   - **Quyết định 29/09/2026:** lượt 3 = sửa tham số (gấu áo nâng một phần, ống quần nới, tay nắm quai đèn lồng s41/s42a), **không kiểm mù**; chủ dự án xem ảnh (reports/m2/CONG-6-THAN-3.md) rồi duyệt khoá. Khi duyệt: khoá v1.5.1 + v1.6 một lần (sai lệch chấp nhận: chân/tay có thể còn bị chê ở khung tĩnh, kiểm lại trên clip W1/W2), mặc định Cas 'bl' + thân + tay mới, layout-v16 kèm silhouettes, luật v1.5, merge main (tài sản phải có trên main cho worktree W1/W2).
   - **Cách chấm kiểm mù từ W1/W2:** **10 khung mỗi lần, được phép 1 khung trúng** (AUTHORSHIP "Cổng 6 — bàn giao P" và "Cổng 6 — diễn hoạt"), cộng 2 đối chứng chạy mỗi lần; ĐẠT khi ≤ 1/10 khung (cột HÌNH; ở W2 cả cột TƯ THẾ) có từ khoá và không lời chê cùng chỗ lặp ≥ 2 khung. Nhiễu nền đối chứng hiện 2/20.
4. ~~Khiếu nại P0 (2 lần báo nhầm) chờ K~~ — **đã phán quyết và sửa ở checks v1.5** (checks-appeal.md). **Khiếu nại mới (29/09/2026): C3 chỉ đọc một nhân vật mỗi thư mục parts — chờ K/chủ dự án.**
5. **Cổng 7 THỬ MẶT (30/09/2026; nhánh cục bộ `thu-mat` @5db04fe, KHÔNG merge; bản vá `reports/m2/cong7/thu-mat/ma-v1.patch`):** V1 (three.js: da tán xạ giả, phơi sáng theo shot, ánh dội môi trường, mắt ướt, vi chuyển động) xong; V2 EEVEE dừng trước khi dựng (hạn token). **Kiểm mù V1 TRƯỢT 3/3** (s03 "mặt nạ" do đỏ cam, s05 "búp bê/đất nặn", s22 "sáp/búp bê" kèm "hói", tai to). `reports/m2/cong7/THU-MAT.md` §10. **Chờ chủ dự án quyết:** (A) giữ V1 làm nền vật liệu Cổng 7, có sửa (trần bão hoà da, phơi sáng s05, tai); (B) mở cửa thiết kế mặt/tóc Ida (nếp nhăn tuổi bằng normal map, chân tóc thái dương, cỡ tai; mở khoá v1.5.1); (C) dàn dựng tránh MCU tĩnh s22.
6. **Tồn đọng kênh Last Lamplighters:** chưa tra nhãn hiệu USPTO (và EUIPO/UKIPO) cho tên kênh "Last Lamplighters" — làm trước khi mở kênh.
7. **Last Lamplighters — Mốc 1 + kịch bản + series XONG (01/10/2026), DỪNG chờ chủ dự án:** `reports/m3/THU-PHONG-CACH.md` (B3 + B1; kiểm mù: 0 từ khoá chê, điểm TB 4,75 cả hai vs đối chứng 6,5; nhớ số liệu đủ; P đề xuất B3 + lượt sửa nhỏ ánh sáng/viền ngược sáng), `reports/m3/KICH-BAN-TAP-THU-V2.md` (~9:31, 4 số neo, 20/31 nguồn đọc toàn văn + BLS đọc toàn văn bởi Claude), `reports/m3/SERIES-LAST-LAMPLIGHTERS.md` (6 tập). Mã thử phong cách ở nhánh cục bộ `thu-phong-cach` @383d051 + `reports/m3/thu-phong-cach/ma-thu-phong-cach.patch`.
8. **B3 v2 + kế hoạch tập thử XONG (01/10/2026), DỪNG chờ chủ dự án:** `reports/m3/THU-PHONG-CACH-V2.md` (kiểm mù 4 dải: 0 từ khoá chê — đạt; điểm TB 4,50 < 4,75 — chưa đạt; lỗi mới "bóng ma" do khối thân mờ; P đề xuất lượt sửa ngắn A), `reports/m3/KE-HOACH-TAP-THU.md` (78 shot 9:31; ~0,2 triệu token/phút; ElevenLabs qua proxy, còn ~29 400 ký tự tới 23/10). Nhánh `thu-phong-cach` @02e6872 đã push. Chưa render tập thử, chưa mở kênh.
9. **Mốc 2 mở 01/10/2026 — M2.0 XONG, DỪNG chờ duyệt:** `reports/m3/M2-0-CHUAN-BI.md` (B3 v3 sửa "bóng ma" + s22 thấy nguồn điện; bộ mẫu dữ liệu 5 khung; 1080p 2,64 s/khung → tập ≈ 17 h máy; giọng kể **Bill** 141,2 từ/phút → ≈ 10:03–10:05; ElevenLabs còn 25 308 ký tự tới 23/10), `reports/m3/BANG-SHOT-M2.md` (78 shot), `reports/m3/YEU-CAU-K-NHAP.md` (chưa gửi). Sau duyệt → M2.1 animatic nhịp (flite, thử Bill 1,05, quyết đoạn 07).
10. **M2.1 XONG (01/10/2026), DỪNG chờ duyệt nhịp + giọng:** `screening/ll-ep01-animatic.mp4` (9:37,5; Bill 1,00 + cắt đoạn 07; flite), `reports/m3/M2-1-ANIMATIC.md`. Chờ chốt: máy s22 (05-08) b3v3 vs BANG-SHOT; thẻ −34 % đứng ≥ 5 s; nhạc tạm M2-MUS-1; 3 Shorts. ElevenLabs API vẫn báo Starter (còn ≈ 20 940) → chưa thu trọn lời dẫn.
11. **BÀN GIAO 01/10/2026 → phiên mới "LL-P · Last Lamplighters":** `reports/m3/PLAN-HANDOFF-LL.md`. Việc tiếp: kịch bản v3 + lát cắt M2.2a (lệnh dán ở phiên mới). Phiên P cũ dừng nhận việc.
12. **LL-P (nhánh `ccr-a27221d7-0iwsne`, 01/10/2026) — M2.2a XONG, DỪNG chờ chủ dự án duyệt lát cắt:** `reports/m3/M2-2A-LAT-CAT.md`, `screening/ll-ep01-lat-cat.mp4` (93,75 s, judder 0, −14,1 LUFS / −1,6 dBTP, tương phản ≥ 5,34:1) + 720p 25,7 MB. Kịch bản **v3.1 đã duyệt** (trần tập 11:00). Mã lát cắt: nhánh cục bộ `lat-cat-m22a` (bản vá `reports/m3/m2-2a/ma-lat-cat.patch`). Chờ: Q2 chữ trên hình, Q3 khối văn phòng G0, duyệt lát cắt → mở animatic v3 (Bill thật cả tập, ≤ 11:00). Yêu cầu K (mục 3 luật judder) chưa gửi, gửi ở M2.3.
13. **ANIMATIC V3 CẢ TẬP — MỞ 01/10/2026 (chủ dự án duyệt lát cắt M2.2a làm chuẩn kênh).** Kịch bản v3.1; giọng Bill thật đã thu đủ (đoạn 01–09, 14–19 mới; 10–13 dùng lại M2-VO-1); dòng thời gian thật `reports/m3/m2-2b/timeline-v3.json` = **9:56,6** (trần 11:00). Gói: xưởng STORY (01, 04, 19, G0 đoạn 10 sửa văn phòng, tấm bóng đoạn 03 sửa s03/s05), xưởng HISTORY (02–09), xưởng TODAY (10–13 từ lát cắt + L1–L4, 14–18); P: nhạc có giấy phép, mix, ghép, judder, loudness, kiểm mù màu, báo cáo `reports/m3/M2-2B-ANIMATIC-V3.md`. **DỪNG sau báo cáo.**
    - **Ước ngân sách (ghi đầu việc, không chờ duyệt):** token ≈ STORY 180k + HISTORY 200k + TODAY 180k + P 150k ≈ **0,7 triệu** (≈ 0,07 triệu/phút; cộng kịch bản v3 0,18 triệu → ≈ 0,09 triệu/phút; tiêu chí ≤ 0,3). Giờ máy: cảnh truyện ≈ 2 700 khung × 1,7–13 s ≈ 1,5–10 h; đồ hoạ ≈ 11 600 khung × 0,5 s ≈ 1,6 h luồng; ghép + mã hoá + đo ≈ 1 h → **≈ 4–13 h** (4 vCPU dùng chung). ElevenLabs: 5 696 ký tự gửi (bộ đếm 3 649 → 5 707).
    - **Ngân sách đĩa (CHUAN-KENH §6, ghi 01/10/2026 ≈ 13:25, sau sự cố đĩa đầy 12:38):** hạn mức phiên ≈ 40 GB (29 dùng + 11 trống) → ngưỡng dừng render mới: trống < 6 GB (15 %) hoặc < 3 GB. Mức trống thực tế (df): **11 GB**. Mức cần còn lại ≈ trung gian còn lại 1,2 GB (đồ hoạ ≈ 160 MB/phút đo thật trên 7 đoạn; truyện ước ≈ 400 MB/phút) + master crf 16 0,63 GB + bản xem 720p 3 phần 0,23 GB (×2: /var/tmp và repo) + âm thanh làm việc 0,4 GB + tấm nền PNG tăng thêm ≈ 0,5 GB ≈ **3,2 GB** → 1,5 × 3,2 = 4,8 GB ≤ 11 GB: **ĐẠT, không cần chia khối nhỏ hơn**. Worktree: 3 (story, history, today) = trần 3. Đã dọn: FFV1 lát cắt 6,2 GB, worktree `tpc` và worktree lát cắt.
Hạn mức: chủ dự án chọn **giữ tốc độ**; vẫn ghi token từng gói.

## Việc cho Cổng 6 — theo quyết định "Cửa mặt Ida (đóng)" 29/09/2026 (chỉ ghi, chưa làm)
**a. Nhịp cười buồn đo trên CLIP CHUYỂN ĐỘNG CÓ TIẾNG** (s37: "That's the last one, then.", "Goodnight, old street."):
- chủ dự án tự xem và chấm;
- AI mù đọc bảng khung theo thời gian (mỗi 0,5 s trong nhịp, kèm phụ đề).
- **Tiêu chí:** AI mù kể ra cả "cười" lẫn "buồn/tiếc".

**b. Danh sách sửa:**
- (1) Mắt khung chính diện: bớt bóng kiểu mắt búp bê, mí che bớt tròng, có viền nước.
- (2) Mũ ôm đầu, không lơ lửng.
- (3) Mắt đọc được khi quay nghiêng (máy PA1).
- (4) Tay Ida dùng tay MPFB, cầm nắm cột và van đúng.

**c′. Quyết định cố định (29/09/2026):** **s22 (W1)**: xoay Ida sang 3/4 (> 30°), giữ MCU. **s40 (W2)**: mặt Ida chìm vào bóng tối đúng lúc L11 tắt (1:49,2) — quyết định cố định. Đã ghi vào shots_w1.json / shots_w2.json (trường `cong6`).

**c. Shot có Ida quay chính diện / gần chính diện (≤ 30°):** bảng ở reports/m2/CONG-6-MO.md mục 3. **Phải đổi cỡ nếu chưa sửa mắt: s22 (MCU), s36 (MCU), s37 (CU), s39 (CU), s40 (CU insert)**; s36–s39 đã thuộc dàn dựng lại PA1. **Chưa sửa xong mắt (b1) thì các shot này không dùng cận mặt**; bảng đó ghi shot nào phải đổi cỡ cảnh.

**e. Gói W4 nhân vật — XONG (reports/m2/CONG-6-W4.md), chờ duyệt Q1–Q4:** mắt Ida + Cas; mũ ôm đầu (mũ phớt Ida, mũ len Cas, tóc gáy Cas); tay MPFB Ida + Cas (Ida nắm cột và van, Cas cầm đèn lồng); **Cas cổ áo len lật cao** (P soạn số cổ vào nháp v1.6); nghiên cứu khả thi thân MPFB (chỉ báo cáo). Sau đó kiểm mù 6 subagent.

**d. Gói đầu Cổng 6:** Cas đi quy trình MPFB (W4) — XONG; chủ dự án chọn **A+** (nhận Cas 'bl' làm nền, cổ áo lật cao), kiểm mù nhẹ TRƯỢT (Cas "búp bê" 2/2, lệch phong cách 1/2); nháp v1.6 chờ duyệt; mặc định Cas v1.4.

## Việc cho Cổng 6 (từ Cổng 5 — B1 và continuity lần 3)
- **B1 cảnh 6:** làm rõ hướng mặt, hướng đầu của Ida ở s45 và đồng hồ trong tay (s45 → s46 → s45c giữ nguyên).
- Ghi nhận continuity lần 3 thuộc Cổng 6: **G2** mũ đội thẳng s40 (nhảy mũ s39 → s40); **G5/G6** tay s44 ("tay đặt ngực") và s45 (tay trái tách đồng hồ); **G10** Ida xuống thang trong s40w; **G11** s32 → s33 Ida quỳ → đứng (cho 0–0,6 s đứng dậy); **G13** thang trong ngõ ở s44 trước khi bà vác ở s47.
- Khác: khẩu hình s39 câu cuối L4 (phụ thuộc lời giải mặt Ida); nhịp "gập đồng hồ" trong `bible/characters.md` — layout chưa có nắp: Cổng 6 dựng nắp hoặc P đề xuất sửa bible (chủ dự án duyệt); s45 tay che nửa mặt 0–1,0 s.

## Việc cho Cổng 9 (danh sách sửa)
- **Mô-típ đồng hồ:** Claude (AI mù bên ngoài) chê "the times don't add up" 3 lần liền. Kiểm lại giờ của hai loại đồng hồ (quảng trường và bỏ túi) đặt liền nhau (mốc hiện tại: s06 bỏ túi 7:31, s09 quảng trường 8:00, s09w bỏ túi 7:53, s46 bỏ túi 9:53 → 10:00, s45c quảng trường 10:00); soạn phương án **"chỉ giữ một loại đồng hồ"** để chủ dự án chọn ở Cổng 9.

## Việc cho Cổng 8 (âm thanh)
- **Tiếng tách gập nắp đồng hồ** (ngoài hình, sau nhịp giữ 10:00 ở cảnh 6) — chủ dự án chọn Đ4 (b), 30/09/2026.

## Việc dời sang Cổng 7 (chủ dự án quyết, 28/09/2026)
- **Người và bóng ở hốc vòm (1:18–1:26, s32–s34):** tiêu chí đo được — **mỗi người sáng hơn bóng của chính mình trên vách ít nhất X = 2,0 lần**, đo bằng trung vị luma hiển thị (Rec.709, mã 8 bit, sau grade) trên mặt nạ người (phần nhìn thấy) so với mặt nạ bóng của chính người đó trên vách, ở mọi khung mẫu (mỗi 12 khung). Căn cứ: luật thế giới 3.1 đòi key : tràn ≥ 4 : 1 tại mặt nhận bóng để bóng hiện; mặt người quay về đèn lồng nhận key trực tiếp, vùng bóng chỉ nhận tràn → tỷ lệ tuyến tính ≥ 4; qua đường cong hiển thị (gamma ~2,2) 4× tuyến tính ≈ 1,9× luma hiển thị, nên chọn **2,0** (≈ 4,6× tuyến tính) — đủ để mắt tách người khỏi bóng mà không phải thêm đèn giả. Bóng mặc định đo ở phần thân bóng (không tính đầu bóng mờ nhạt ở vùng vách tối dần, luật 4).
- Ghi nhận continuity lần 3 thuộc Cổng 7: **G1** kính đèn P5/cột sân trước tắt vẫn đọc đĩa xám sáng (s23); **G7** màu mũ nhảy theo nguồn sáng (s11–s13, s39 #311615, s42); **G8** kim/vạch đồng hồ quảng trường nhạt hoặc hồng nâu khi mặt loá (s09, s45c); **G9** quầng loá P5 phủ trời (s37w, s40w); **G12** tóc xám tối dưới vành mũ s45; **G16** s43 điểm vàng chưa đọc ra ô cửa; **G17** người/bóng s33 (tiêu chí X = 2,0 ở trên). Thêm: ánh nền s45 trắng / s45c trời đen (kiểm mù POV cảnh 6).
- Hạ phơi sáng s11 (1,5–1,7); màu mũ nâu cam dưới đèn khí sát mặt (s05, s36, s40); lấy nét thật thay cho nền nhoè s06, s09w; ánh cửa sổ ấm có thật ở nhà đầu dãy bắc cho mặt Cas s24c.
- **s42b: mặt nghiêng + tay Ida đen đặc như bóng cắt** (continuity W1 L5, sau khi sửa trục M1) — chủ dự án chuyển Cổng 7, 30/09/2026.
- **s27 (1:04–1:07):** tường trắng đều như ban ngày, quầng L11 mất hẳn — mức sáng và độ giảm dần theo hướng nguồn (nguồn trắng mé đối diện, ngoài khung). **Nền s45 cháy trắng.** (Chủ dự án chuyển, 30/09/2026.)
- **s40 (1:49,2): khi L11 tắt cảnh không tối đi; bà quay gáy thành "cục len trắng"** — ánh sáng thật: L11 là nguồn chính trên mặt, ánh sáng nền thấp (chủ dự án chuyển từ Cổng 6, 30/09/2026).
- **Đèn lồng của Cas chưa chiếu sáng ra xung quanh** (mặt đường, tường, người bên cạnh), kiểm mù W4T 3/3 khung nhắc (Claude rà độc lập bên ngoài phát hiện; chủ dự án duyệt và giao, 29/09/2026).

## Bảng gói việc
| Gói | Phiên/agent | Nhánh | Trạng thái | Báo cáo |
|---|---|---|---|---|
| M0 Cổng 0 | P | claude/jolly-edison-a4hq3n | Đã merge vào main | reports/m0/BAO-CAO-M0.md |
| checks v0 | K | checks/v0 | Đã merge vào main | checks/RULES.md, reports/checks-selftest/ |
| M1 hợp nhất + giọng + banding + Cổng 1 | P | claude/cine-lab-m1-last-round-f1667s | Cổng 1 đã chọn P3 | reports/m1/CONG-1.md, reports/m1/banding/BANDING.md |
| M1 Cổng 2 kịch bản nháp 1 → nháp 2 + table read | P | claude/cine-lab-m1-last-round-f1667s | Chờ duyệt Cổng 2 (nháp 2) | reports/m1/CONG-2.md, scripts/last-round.fountain |
| M1 Cổng 3 vòng 1: nền chung, model sheet, 3 hướng (3 subagent song song), color script | P + 3 subagent | claude/cine-lab-m1-cong3-design | Chờ chủ dự án chọn | reports/m1/CONG-3-VONG-1.md |
| M1 Cổng 3 vòng 2: hạ tầng 4 shot, 2 cách nhân vật (2 subagent), C2 mù, nhấp nháy | P + 2 subagent | claude/cine-lab-m1-cong3-v2 | Chờ chủ dự án chọn | reports/m1/CONG-3-VONG-2.md |
| M1 Cổng 3 vòng 3 + đợt vá A2+ + khoá thiết kế | P | claude/cine-lab-m1-cong3-v3 | **Đã merge vào main (c21e5df)**; SHA khoá `design/cong3/LOCK-THIET-KE.sha256` | reports/m1/CONG-3-VONG-3.md, reports/m1/CONG-3-VA-A2PLUS.md |
| M1 Cổng 4: cổng mặt Ida (biến dạng, đẩy mũ, kiểm mù) + animatic 2:30 (48 shot) + âm tạm + gói chiếu mù | P | claude/cine-lab-m1-cong4-animatic | Vòng v1 xong; xem vòng v2 | reports/m1/CONG-4.md |
| M2 Cổng 5 layout (W1, W2, W3 + P) | P + 3 subagent + 2 agent rà | claude/cine-lab-m2-cong5-layout-24o5fp | Vòng v1 xong; xem vòng v2 | reports/m2/CONG-5.md |
| M2 Cổng 5 vòng v2 (A-α, hiệu chuẩn, B1, a–d, continuity v2) | P + W1, W2, W3 + agent rà + 16 subagent kiểm mù | claude/cine-lab-m2-cong5-layout-24o5fp | Xong; chủ dự án đã quyết (AUTHORSHIP "Cổng 5 v2 — quyết định") | reports/m2/CONG-5-V2.md |
| M2 Cổng 5 vòng v3 (chốt layout) | P + W1, W2 + agent rà + 1 subagent kiểm mù | claude/cine-lab-m2-cong5-layout-24o5fp | **Cổng 5 ĐÃ ĐÓNG (A1) — merge vào main** | reports/m2/CONG-5-V3.md |
| M2 Cửa mặt Ida A-i | W3 + 37 subagent kiểm mù | claude/cine-lab-m2-cong5-layout-24o5fp (merge e2394c5, IDA_STYLE 'aa') | 2 vòng TRƯỢT; chủ dự án chọn **C chỉnh** | reports/m2/MAT-IDA-AI.md |
| M2 Cửa mặt Ida — Blender (C chỉnh) | W4 (worker mới) + P kiểm mù | claude/cine-lab-m2-cong5-layout-24o5fp | L1 dừng; L2 trượt; L3 (A′) trượt tiêu chí cảm xúc 2/4 (búp bê 0/4) — chờ chủ dự án chọn A/B/C | reports/m2/MAT-IDA-BLENDER.md, -L2.md, -L3.md |
| M1 Cổng 4 vòng v2: animatic 2:22,5 (52 shot), kịch bản nháp 3, luật thế giới v0.4, characters v1.2 (A1), C3 v1.4 (parts + views + kiểm toán) | P | claude/cine-lab-m1-cong4-animatic | **Đã merge vào main (5987bf3)** — Cổng 4 đóng | reports/m1/CONG-4-V2.md, shots/animatic/SHOTLIST.md, screening/animatic_v1_v2_diff.md |

Quy ước file lớn Cổng 4: `design/cong4/animatic/out/animatic.mp4` (v2: 45,49 MB) nằm trong nhánh; mặt nạ C3 `out/animatic.parts/` (18 MB, PNG xám) cũng trong nhánh; video nhóm và video ghép trung gian `out/v2/*.mp4`, âm trung gian `out/v2/audio/` KHÔNG commit; `screening/animatic.mp4` là bản sao y từng byte. Bản trung gian `out/video.mp4` (187 MB) và đối chứng `out/hq/` (198 MB) KHÔNG commit (vượt giới hạn GitHub; tái tạo bằng `render_film.js` / `HQ=1 package.py`). Âm lưu FLAC 24-bit.

## M2 · Cổng 5 — Layout (P điều phối, 3 gói song song)
Nhánh tích hợp: `claude/cine-lab-m2-cong5-layout-24o5fp` (tạo từ main 5987bf3). Mã layout: `design/cong5/layout/` (tách từ animatic Cổng 4).

| Gói | Agent | Phạm vi shot | File được sửa (chỉ gói đó) | Đầu ra |
|---|---|---|---|---|
| **W1** | cine-worker, worktree | Cảnh 1–3: s01 → s24c — **xong (A, C, sửa N1)** | `shots_w1.js`, `order_w1.js`, `sets.js` (bộ phố, trừ phần cuối phố) | `shots/layout/continuity/canh-1..3.md`, `shots/layout/shots_w1.json`, render ở `/var/tmp/cine-out/W1/` |
| **W2** | cine-worker, worktree | Cảnh 4–6 (kịch bản ghi cảnh 4–7): s25 → s48 — **xong (A, C, D sửa continuity); C2 chờ chủ dự án** | `shots_w2.js`, `order_w2.js`, `sets2.js`, `sets_end.js` (cuối phố: V3) | `shots/layout/continuity/canh-4..6.md`, `shots/layout/shots_w2.json`, render ở `/var/tmp/cine-out/W2/` |
| **W3** | cine-worker, worktree | Mặt Ida (A1 → A3 nếu trượt) — **A1 trượt, A3 trượt; mã A3 lưu dạng patch, layout dùng A1** | `design/cong3/v2/char3d/*` (mặt, cổ áo), `design/cong5/mat/` | ảnh thử, đề xuất đổi sheet/bible gửi P |
| P | phiên này | ghép, `common.js`, `film.js`, âm, đóng gói, luật máy, kiểm mù, báo cáo | `common.js`, `film.js`, `page.js`, `render_film.js`, `assemble.py`, `package.py`, bible/, sheet, SHA | `screening/layout.mp4`, `reports/m2/CONG-5.md` |

Luật chung:
- Subagent KHÔNG sửa `bible/`, `checks/`, không đọc mã trong `checks/`. Đề xuất đổi bible/sheet gửi P; P sửa và khoá SHA.
- Sửa lỗi: V1 (s42b/s42, W2), V2 (s31–s33, W2), V3 (cuối phố 0:52 s23 W1 dùng `sets_end.js` của W2; 1:04 s27, 1:40 s37w W2), V4 (s26, W2), D2 mũ (đã vào sheet v1.3, P).
- Thoại nguyên văn; tổng thời lượng quanh 2:22,5 (lệch > ±5 s phải báo).
- **Hàng đợi render nặng:** `scripts/render/queue.sh <gói> <nhãn> -- <lệnh>` (flock, mỗi lúc 1 render nặng). Nhật ký thời gian thật `/var/tmp/cine-queue/log.tsv`, P chép vào `reports/m2/cong5/queue-log.tsv`. Probe ≤ 3 khung/shot ở 960×540 là việc nhẹ.
- Chờ tiến trình nền bằng `while kill -0 $PID` (bài học vòng chờ). Chỉ render lại phần thay đổi.
- Thứ tự: (A) W1/W2 chốt layout + probe + continuity + manifest; W3 làm A1 bằng ảnh tĩnh → (B) P merge W3 + A vào nhánh tích hợp → (C) W1/W2 merge nhánh tích hợp, render đầy đủ qua hàng đợi → (D) P ghép, âm, kiểm mù lần 4 (ảnh 4 lấy từ s39 layout), cine-continuity rà toàn phim, luật máy, `screening/layout.mp4`.
- File lớn: render trung gian ở `/var/tmp/cine-out/` (không commit); `design/cong5/layout/out/layout.mp4` và `screening/layout.mp4` (< 50 MB) commit.
