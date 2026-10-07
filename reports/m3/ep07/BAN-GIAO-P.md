# Bàn giao phiên P → phiên P mới (tập 7) · 07/10/2026

## Trạng thái
- **Tập 6 v2:** Claude kiểm bản sửa: ĐẠT. Gói phát hành ở `release-ll-ep06-v2` @ `ac607c9` (tải ngược 11/11 SHA OK). Hướng dẫn đăng: `reports/m3/HUONG-DAN-DANG-TAP6.md`. **Chờ chủ dự án làm G3.** Bản v1 không phát hành (`release-ll-ep06-v1` chỉ để đối chiếu).
- **Checks LL v3 1.7.1** (LOCK `e3fcd2e6…`) đã merge vào nhánh lô và `main`; `checks/lock.py --verify` KHỚP. P không sửa `checks/`.
- **Tập 7** ("When Computers Were People"): kịch bản v1 đã duyệt ở G1, nhưng đặc tả **chưa** sửa theo G1 và chưa dựng. **Tập 8** ("The Translator's Desk"): tương tự, làm sau tập 7.
- **Hạ tầng sẵn dùng** (xem `scripts/ll/README.md`, mục "Bổ sung tập 6 v2"):
  - cảnh đinh 3D `design/ll-hero/`, mẫu v3;
  - nhạc theo hồi (`mix.py`), âm thanh nghề, `pause`/`speed`, bản đồ `map:`;
  - `diversity.py`, `cont.py`, `blind_set.py`.

## Quyết định đã có cho tập 7–8 (AUTHORSHIP)
- **Tiêu đề:** phương án A cho cả hai tập.
- **Số BLS đợt 2025–35** ("đã xác minh (Claude)", 06/10):
  - software developers 1 717 800 → 1 892 600 (+10,2 %);
  - interpreters & translators 73 900 → 75 400 (+2,0 %);
  - toàn nền +3,5 %;
  - đợt 2024–34 / 2023–33 chỉ ở khung riêng.
- **Lời dẫn** không nói về việc phim làm bằng AI (CHUAN-KENH §10). Altered content = No.
- **Tập 7:** được dùng ảnh NASA (do NASA tạo, không logo, không hàm ý bảo trợ, có dòng RIGHTS; ưu tiên tổ "computer" Langley).
- **Tập 8:** thẻ kết "More from Last Lamplighters".
- **NGUYÊN TẮC TỐI CAO:** chất lượng và liền mạch trên hết; trần token mềm. Theo CHUAN-KENH §11:
  - 4–6 cảnh đinh 3D mới mỗi tập;
  - ≥ 3 bối cảnh/đạo cụ mới và ≥ 3 âm thanh nghề;
  - bàn làm việc ≤ 3 lần;
  - nhạc hiệu kênh + 3 cue theo hồi;
  - tư liệu ≤ 20 %.
- **Từ tập 7 áp đủ checks v3** (Q1–Q31 + LOCK):
  - Q27 chấm bộ 60 ảnh (30 tập mới + 30 tập 1);
  - Q31: vòng 1 chặn mọi điểm ≥ 2/3; từ vòng 2 chỉ chặn điểm 3/3, điểm 2/3 phải có giải trình;
  - **không xoá `<out>/blind/q31-lich-su/`**;
  - G2 ghi mọi lần chấm mù (kể cả lần trượt) và token thật.
- **Rút từ tập 6 (Q27/Q31):**
  - tựa phim chồng lên cảnh đinh (v3 đã cho phép), thay thẻ tựa giấy;
  - thay bàn làm việc 2D bằng cảnh 3D nội thất;
  - không đặt khung đôi ngay trước chuyển hồi;
  - nhân vật trong cảnh đêm phải có nguồn sáng riêng.

## Bài học #70–#79 phải nhớ (chi tiết: BAI-HOC-LL.md)
- **#70, #76:** không chèn chú thích vào giữa dòng nhiều lệnh. `tests/comment_guard.py` + `node --check` chạy đầu mỗi build. Sửa mã cảnh đinh thì xem trước `hero.js --only` vài khung.
- **#70:** `build.sh` dựng cảnh đinh vào `<dir>.new`, chỉ thay khi thành công.
- **#79:** **không viết khoá `off:` / `on:` / `yes:` / `no:` trong YAML.** Dùng `frame0`; `ll.py` chặn khoá boolean. Mọi tham số mới: kiểm giá trị trong `timeline.json` trước khi dựng.
- **#71, #72:** "cùng bố cục" đo dễ sai với cảnh tối và với fade. Thước khoá của K nay là chuẩn.
- **#73:** bộ xem mù có thể tự tạo lỗi giả. Luôn đối chiếu điểm mù trên khung thật trước khi sửa.
- **#74, #75:** trích dẫn ngắn đặt thành chú thích trên cảnh vật chất. Chữ trên vùng sáng của cảnh 3D cần dải tối.
- **#77:** bóng người tối trên nền tối thì biến mất.
- **#78:** bàn làm việc 2D là cảnh yếu nhất.
- **Khác:** dải che phải vẽ trước ghi công (Q5); `pkill -f` có thể khớp chính shell, nên dừng theo PID; vòng chờ dùng `kill -0 <PID>`.

## Phiên sau đọc (≤ 8 tệp)
1. `reports/m3/BAI-HOC-LL.md`
2. `reports/m3/CHUAN-KENH-LL.md` (§10–11)
3. `reports/m3/ep07/BAN-GIAO-P.md` (tệp này)
4. `reports/m3/ep07/episode.yaml`
5. `reports/m3/ep07/NGUON-TAP7.md`
6. `checks/ll/RULES-LL.md` (chỉ định nghĩa Q26–Q31; không đọc mã `checks/`)
7. `scripts/ll/README.md` (mục "Bổ sung tập 6 v2")
8. `reports/m3/ep06/episode.yaml` (mẫu đặc tả đủ `map:`, `heroes:`, `pause`, `sfx`, `frame0`)

## Đang chờ chủ dự án
- G3 tập 6 v2 (đăng theo HUONG-DAN-DANG-TAP6).
- Lệnh mở phiên P mới cho tập 7.
