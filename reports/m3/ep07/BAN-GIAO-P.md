# Bàn giao phiên P (tập 7) → phiên P mới (tập 8) · 09/10/2026

## Trạng thái main
- `main` gồm hai merge, đều không squash:
  1. nhánh tập 7 `claude/eager-babbage-6cc4l6`, commit merge `907cdd3`;
  2. nhánh K `claude/checks-ll-v3-tap-7-b3kbii` @ `06524c1`, commit merge `f115e8b`.
- **Tập 7** "When Computers Were People: One Word, Three Jobs": **G2 DUYỆT nguyên trạng 09/10.**
  - Gói phát hành: `release-ll-ep07-v1` @ `6adb15c`, tải ngược kiểm 14/14 SHA OK.
  - Hướng dẫn đăng: `reports/m3/HUONG-DAN-DANG-TAP7.md` (S1 đăng N − 1, tập chính ngày N, T1 chính, T2 A/B).
  - **Chờ chủ dự án làm G3.**
  - Báo cáo: `reports/m3/TAP7-G2.md`; chấm mù: `reports/m3/ep07/Q27-Q31.md`.
- **Tập 6 v2:** G3 do chủ dự án tự đăng (`release-ll-ep06-v2`).
- **Tập 8** "The Translator's Desk":
  - Lời v1 duyệt ở G1 lô 6–8, ngày 06/10, **trước** khi có trục kể biến đổi (CHUAN-KENH §12, áp từ tập 7).
  - Rất có thể phải viết lại như tập 7 (G1 rút gọn: lời v2 → 3 kiểm mù → dừng G1). **Hỏi chủ dự án trước khi làm.**
  - Luật mới đã ghi ở `reports/m3/ep08/PLAN.md` (mục "Luật mới từ G2 tập 7" và "## Cải thiện hình").

## Checks LL v3 1.8.1 (chủ dự án duyệt 09/10)
- Kiểm trên `main`:
  - LOCK `208121b48826b80a2170d5fab2e8cb9d092b37cf011de8f0da956e7d0dd98af7`, `checks/lock.py --verify` KHỚP;
  - `checks/ll/selftest_ll.py` 160/160;
  - `scripts/ll/tests/run.sh` ĐẠT.
- **Mới: Q26b quãng liên tục.**
  - Không bối cảnh nào > 25 % thời lượng hay > 90 s liên tục.
  - Cảnh "trung tính" không làm dứt quãng; quãng dứt khi bối cảnh khác cộng dồn ≥ 8 s.
  - Đo tập 7 (ghi nhận, không áp): tower 139,1 s, pool 104,3 s, TRƯỢT. Tập 6 v2: 27,1 s, ĐẠT.
  - Chi tiết: `reports/checks-ll-v3/BAO-CAO.md` mục 14.
- Q27 (60 ảnh), Q31 (sổ vòng theo tập; từ vòng 2, điểm 2/3 phải có `giai-trinh.json`) giữ như 1.7.1.
- Chủ dự án đã chấp nhận cách đếm vòng Q31 theo tập cho tập 7; K sẽ chốt luật.
- P không sửa và không đọc mã `checks/`; chỉ đọc `checks/ll/RULES-LL.md` và chạy `q_blind.py`.

## Bài học mới phải nhớ (chi tiết: BAI-HOC-LL.md #89–#98)
- **#96:** không bối cảnh 3D nào > 25 % thời lượng hay > 90 s liên tục; nửa sau phim ≥ 3 bối cảnh khác nhau (ban ngày / cận cảnh / nơi người mới học nghề). Kiểm ở đặc tả, trước khi dựng nháp (Q26b).
- **#97:** nội thất chi tiết hơn, sáng hơn, ít khối thô và tối: vân vật liệu, đồ vật, ánh sáng có nguồn, tương phản, chiều sâu. Làm từ cảnh đầu tiên. Thay thẻ giấy dựng dở bằng cảnh hoàn chỉnh.
- **#98:** ElevenLabs lệch 1 814 ký tự không giải thích được. **Kiểm bộ đếm trước và sau mỗi build** (`ll.chars_used()`); lệch so với `el_sent` thì dừng và báo.
- **#95:** `asr.py` đã sửa để truyền `speed`. Prep bản cuối (có ASR) chạy riêng một lần, kiểm `el_sent` = 0 trước khi dựng cảnh đinh.
- **#94:** `hero.js --resume` và `pending` stamp: job nền bị ngắt ở mốc 2 giờ thì chạy lại lệnh build, sẽ dựng tiếp phần dở.
- **#89–#93:**
  - Q27 dao động ±0,36; Q27 trên nháp chỉ để chẩn đoán.
  - Người chấm trả thiếu hoặc thừa mục: lưu nguyên văn, chạy lại riêng người đó.
  - Đổi nơi chốn thì cần cảnh riêng có dấu hiệu nơi chốn và phụ đề nơi chốn.
  - Diptych cần nhãn (`p.labels`).
  - Cắt ảnh lưu trữ ↔ 3D luôn bị 2/3 nêu: giữ, hoà hình, giải trình.

## Quy trình tiết kiệm token (rút từ tập 7)
Tập 7 tốn khoảng 8,5 triệu token (đầu vào mới + sinh ra), gấp khoảng 5,7 lần trần 1,5 triệu; phần lớn ở giai đoạn nháp. Làm thế này để giảm mà không giảm chất lượng:
1. **Đặc tả đúng ngay từ đầu.**
   - Kiểm Q26b (quãng bối cảnh), tỷ lệ trục kể §2 và nội thất chi tiết bằng `ll.py check` và xem trước `hero.js --only` vài khung.
   - Rồi mới dựng nháp.
   - Gom mọi sửa mã cảnh đinh vào một lượt, vì băm cảnh đinh tính trên cả thư mục (#83).
2. **Nháp 960×540 SPP1 tối đa 2 bản:**
   - bản 1: QC + Q27 (chẩn đoán) + Q31;
   - bản 2: sau một lượt sửa.
   - **Không lặp chấm Q27 trên nháp.** Q27 chính thức chạy một lần trên 1080p.
3. **Q31:**
   - Từ vòng 2, điểm 2/3 là chuyển cảnh có chủ ý của kịch bản khoá (cầu người thắp đèn, match cut, ảnh lưu trữ) thì viết giải trình. Không dựng lại.
   - Chỉ sửa điểm đứt mạch thật (lời–hình lệch, nơi chốn không rõ).
4. **Chấm mù:**
   - Giao 6 subagent cùng lúc (Q27 R1–R3, Q31 R1–R3), đề bài chép nguyên `PROMPT-Rk.txt`.
   - Lưu câu trả lời bằng heredoc từ tin nhắn trả về.
   - **Không đọc tệp `.output` của subagent** (bản ghi đầy đủ, rất dài).
5. **Đọc tệp lớn bằng `grep` hoặc `sed -n` theo dòng**, không đọc cả `episode.yaml` và `ep07.js` nhiều lần.
6. **Render 1080p:**
   - Khoảng 11 giờ máy cho cảnh đinh (≈ 3,5 s/khung) + 1 giờ ghép.
   - Chạy nền theo lượt ≤ 2 giờ, mỗi lượt gọi lại `build.sh … prep render`.
   - Không dựng chờ bằng `sleep`; dùng vòng `until` chạy nền.
   - Không `pkill -f <mẫu>` trong cùng lệnh với mẫu đó, vì khớp chính shell (exit 144). Dừng theo PID.
7. **Mỗi bước dài** (render, chấm mù): báo ngắn một dòng, không dán log dài vào hội thoại.

## Phiên sau đọc (≤ 8 tệp)
1. `reports/m3/BAI-HOC-LL.md`
2. `reports/m3/CHUAN-KENH-LL.md` (§2, §10–12)
3. `reports/m3/ep07/BAN-GIAO-P.md` (tệp này)
4. `reports/m3/ep08/PLAN.md` (luật mới, "## Cải thiện hình")
5. `reports/m3/ep08/episode.yaml`
6. `checks/ll/RULES-LL.md` (Q26b, Q27, Q31; không đọc mã `checks/`)
7. `reports/m3/ep07/episode.yaml` (mẫu đặc tả v2 đủ `map:`, `heroes:` có `opt`, `pause`, `speed`, `labels` cho diptych, `frame0`)
8. `design/ll-hero/ep07.js` (mẫu cảnh đinh: nội thất chi tiết, cảnh ban ngày `jpl`)

## Đang chờ chủ dự án
- G3 tập 7: đăng theo `HUONG-DAN-DANG-TAP7.md`.
- Lệnh mở phiên P cho tập 8, kèm quyết định có viết lại lời tập 8 theo trục kể biến đổi hay không.
