# Bàn giao phiên P (tập 8) → phiên P mới (tập 9) · 10/10/2026

## Trạng thái
- **Tập 8** "From Headphones to Machine Drafts: How Translators' Work Changed": **G2 DUYỆT có điều kiện (10/10)** — điều kiện đã làm (sửa T01 đoạn 00, Q31 vòng 3, chỉ một Short S2). Chi tiết: `reports/m3/TAP8-G2.md` mục 9.
  - Gói phát hành: `release-ll-ep08-v1` @ `67bfc2e`, tải ngược kiểm 9/9 SHA OK (master `d22d7d6e…`).
  - Hướng dẫn đăng: `reports/m3/HUONG-DAN-DANG-TAP8.md` (Short S2 đăng N − 1; tập chính ngày N; T1 chính, T2 A/B).
  - **Chờ chủ dự án làm G3.** Nhánh làm việc `ccr-a261f349-6rkunc` chưa merge vào `main`.
- **Khiếu nại chờ phiên K** (sau CN 20:00): Q28f ASR đọc số (09/10) và Q27 chấm lại theo SHA master mới (10/10), `checks-appeal.md`.
- **Đề tài tập 9:** chưa làm; `reports/m3/ep09/PLAN.md` có mục "## Cải thiện hình".

## Luật mới của chủ dự án (10/10/2026) — áp từ tập 9
1. **Mỗi tập 2 Shorts** (không phải 3). Đặc tả `shorts:` chỉ 2 mục; QC Q10/Q22 áp cho 2 Short đó. (CHUAN-KENH §13)
2. **Bỏ thumbnail khỏi gói phát hành.** `make_thumb.py` không còn là bước bắt buộc. (CHUAN-KENH §13)
3. **Chỉ số sát ngưỡng (±5 %)**: chấp nhận, chỉ liệt kê trong báo cáo, không coi là lỗi.
4. Ngân sách credits theo tập (tập 8: $100); sau QC + Q27/Q31 chỉ sửa lỗi nghiêm trọng, tối đa một lượt, chỉ dựng lại đoạn bị ảnh hưởng; lỗi nhỏ ghi "Lỗi nhỏ chấp nhận" + BAI-HOC.
5. Không chạy subagent ngoài Q27 chính thức (một lần, 1080p) và Q31 bản cuối.

## Bài học mới (chi tiết BAI-HOC-LL.md #99–#107)
- **#101, #105:** lời nói về A trên hình B ở điểm chuyển chủ đề, và câu hỏi móc cắt cứng sang khung truyện → 3/3 đứt mạch. Câu hỏi nói xong và phụ đề tắt trước điểm cắt; hoà sang cảnh mới; J-cut âm.
- **#106:** soát mọi chuyển cảnh trước Q31 bằng danh sách kiểm (lời A/hình B, câu hỏi cắt giữa, phụ đề vắt qua cắt) để lượt sửa duy nhất gom đủ.
- **#107:** sửa sau Q27 làm đổi SHA master → `qc.sh` tính lại Q27 sai; giữ số chấm trên đúng bản, ghi SHA đã chấm.
- **#102:** job nền bị dừng ở 30 phút/2 giờ → chạy tách rời `setsid nohup`.
- **#103:** ElevenLabs tính ≈ 0,44 × ký tự gửi; vẫn kiểm bộ đếm trước/sau mỗi build.
- **#104:** `asr.py --check` trước khi để ASR tự thu lại.
- **#108:** `render.js` chỉ nạp khung cảnh đinh tới `t1 + 0,6 s`; hoà dài hơn làm hiện chữ "missing plate" trên cảnh cũ. Đã nới thành 1,5 s (tập 8, sửa T01). Hoà > 1,4 s phải nới tiếp. Đổi độ dài một đoạn làm đổi `t0` các đoạn sau → băm đoạn đổi; đoạn không đổi nội dung dựng lại cho khung trùng hệt (đã kiểm `framemd5` đoạn 02).

## Công cụ mới của tập 8
- `scripts/ll/heroes_par.sh`: dựng cảnh đinh song song (khoá pid, `--resume`), chạy tách rời.
- `scripts/ll/asr.py`: bộ phân tích số sửa (thứ tự sau tên tháng, "and a half", không ghép số sau năm).

## Phiên sau đọc (≤ 8 tệp)
1. `reports/m3/BAI-HOC-LL.md`
2. `reports/m3/CHUAN-KENH-LL.md` (§2, §10–13)
3. `reports/m3/ep08/BAN-GIAO-P.md` (tệp này)
4. `reports/m3/ep09/PLAN.md`
5. `reports/m3/ep08/episode.yaml` (mẫu đặc tả: `heroes` có `opt`, J-cut, chú thích trên cảnh đinh)
6. `checks/ll/RULES-LL.md` (không đọc mã `checks/`)
7. `design/ll-hero/ep08.js` (mẫu cảnh đinh)
8. `reports/m3/TAP8-G2.md` (chi phí, giờ máy)

## Đang chờ chủ dự án
- G3 tập 8: đăng theo `HUONG-DAN-DANG-TAP8.md`.
- Chọn đề tài tập 9 và lệnh mở phiên P tập 9.
- Merge nhánh tập 8 vào `main` (phiên P giữ quyền merge).
