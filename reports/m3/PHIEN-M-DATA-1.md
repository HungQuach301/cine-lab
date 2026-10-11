# Phiên M "Nhà máy dữ liệu" — báo cáo mốc 1–5 · 11/10/2026

Nhánh `claude/phase-m-data-factory-1mygkc` (nhánh được giao cho phiên; lệnh gọi là `data-m1`), từ `origin/main`, rebase lên `origin/main` mới nhất trước khi đẩy. Không sửa `checks/`, không sửa `scripts/ll` (qc/LL giữ nguyên hành vi), không thêm cổng.
Mọi nhãn/chỉ số tính ra: **tự tính, không phải chỉ số YouTube**.

## Kết quả
| Mốc | Làm được | Tệp |
|---|---|---|
| 1 Lõi dùng chung | Hợp nhất `channel-k2` collect/current/final thành mô-đun theo **gói kênh** (ngách, đề tài + câu hỏi mẫu, model ghim theo vai, trần chi, ngưỡng); purge 30 ngày; sổ chi AI; fail closed; **bộ điều phối quota** (ước trước khi chạy, thứ tự ưu tiên phiên, phần giữ cho phiên khác, dừng khi < dự phòng 500). **27 test** bằng dữ liệu giả, không mạng, không AI: ĐẠT | `toolkit/market/`, `toolkit/tests/test_market.py`, `fixtures/market/` |
| 2 Hồ sơ cầu | Mẫu hồ sơ (cầu hiện hành + bền, khoảng trống, 3 video vượt trội, 5 câu hỏi khán giả, điểm yếu đối thủ, dải thời lượng thắng, mẫu tiêu đề, giờ đăng); lệnh `market.py topic <slug>` (≈ 630 đơn vị/đề tài; **chưa chạy thật** — search.list dành k2 tới hết 12/10); khối cột Cầu/Khoảng trống/Câu hỏi trong `topics/queue.md` (T3, T4, T5 "chưa đo") | `reports/m3/topics/_MAU.md`, `topics/queue.md` |
| 3 Cài vào quy trình | CHUAN-KENH-LL **§14** (7 bước trong việc sẵn có: Việc 0, G1 dòng DỰ ĐOÁN, viết lời ≥ 3/5 câu hỏi + 1 nhịp điểm yếu + dải thắng, kiểm mù vai người hỏi, đóng gói theo khuôn thắng/Shorts móc câu hỏi, G3 giờ đăng, đối chiếu số; bảng số đo giữ/bỏ sau 3 tập); sửa PLAN-TAP-MAU, P-G1-LO, P-SAN-XUAT, P-G3, BAN-GIAO-P tập 8, PLAN tập 9, HUONG-DAN-DANG-TAP8 §7; AUTHORSHIP | `reports/m3/CHUAN-KENH-LL.md` §14 |
| 4 Đối chiếu lượt xem thật | `market.py own` (mốc 48 giờ/7 ngày/28 ngày: đúng mốc · nội suy · chờ · lỡ mốc), `predict` (dải TẠM), luật hiệu chỉnh mỗi 3 tập (Spearman nhãn cầu ↔ lượt xem 7 ngày). **Chạy thật: 2 đơn vị** (channels.list + videos.list). Phương án YouTube Analytics API (OAuth, CTR/giữ chân) ghi trong báo cáo, chưa làm | `reports/m3/KHAN-GIA-SO.md`, `reports/m3/khan-gia/snapshots.jsonl` |
| 5 Kênh 2 | `packs/k2.json` (12 đề tài × 6 câu, ngách A/D/J từ `final.py`); cách dùng ở README mục "Mốc 5" | `toolkit/market/README.md` |

## Số đo thật
- **Kênh LL lúc đọc (11/10 13:25 UTC):** 9 video công khai (kể cả Shorts). Có `video_id`: tập 1, 6, 7, 8 (từ `channel-k2/calib.py`). Tập 7 có số đúng mốc 48 giờ; tập 1, 6 lỡ mốc 48 giờ (đọc ở ngày 5 và 4). Tập 2–5 chưa có `video_id` (tối nay không được dò danh sách tải lên). Bảng: `KHAN-GIA-SO.md`.
- **Phát hiện:** tiêu đề trên YouTube đã đổi khác gói phát hành, sang dạng câu hỏi tìm kiếm (vd tập 6 "Will AI Replace Graphic Designers? History Has a Clue"). Công cụ ghi cả hai.
- **Hiệu chỉnh:** chưa đủ mẫu (0/3). Nhãn hồi tố 8 tập chờ `channel-k2/calib.py` (k2, 12/10).
- **Quota:** 2 đơn vị (trần 50, chỉ videos/channels); 0 search.list.
- **AI:** $1,05 / trần $5 — chỉ REVIEWER Opus 2 lượt (`claude-opus-5-5`, served opus + Haiku phụ của CLI). Không subagent.
- **Sát ngưỡng ±5 %:** không có chỉ số nào (chưa đo cầu).

## REVIEWER Opus (luật dữ liệu · không đổi checks/qc · không thêm cổng · fail closed · lỗi mã · nguyên tắc)
- **Lượt 1 ($0,81):** R2 checks/qc PASS, R6 nguyên tắc PASS. Đã sửa: nhãn "tự tính" ở dòng DỰ ĐOÁN; chặn câu AI chép nguyên văn ≥ 8 từ; 403 bình luận chỉ coi "tắt" khi `commentsDisabled`; ghi ảnh chụp + báo cáo một lần sau khi tính xong; lượt AI hỏng ghi chi ước dư; ép model thực chạy = model ghim; chia lô videos.list; thay bộ lọc số thô dễ báo nhầm bằng đối chiếu chính xác số thô đã thu; sửa chữ để không hiểu thành cổng/duyệt mới; tập mới phải vào `own.episodes`. Không nhận: "thiếu fixtures" (do tôi cắt khỏi diff gửi duyệt).
- **Lượt 2 ($0,24):** R2, R3, R6 PASS. Đã sửa: chặn cả số like bình luận; `modelUsage` rỗng hoặc có model lạ → dừng; thêm test `commentsDisabled`. Ghi thành giới hạn (README): không bắt số làm tròn ("4,8 triệu") hay < 1 000, bình luận < 8 từ; `--session` tự khai; ghi hai tệp của `own` không nguyên tử chung. Không chạy lượt 3.

## Ưu, nhược, tác động, rủi ro
- **Ưu:** một lõi cho hai kênh; quota được ước và phân theo phiên trước khi tốn; lỗi dừng hẳn; repo không nhận số thô kênh khác; quy trình không thêm cổng.
- **Nhược:** hồ sơ cầu chưa có bản thật nào; dự đoán G1 là công thức TẠM trên lịch sử rất ngắn (kênh mới, vài chục lượt xem/tập).
- **Tác động:** từ tập 9, G1 cần hồ sơ cầu → Việc 0 phụ thuộc ngày có quota (≈ 630 đơn vị/đề tài).
- **Rủi ro:** câu hỏi khán giả kéo lời lệch trục biến đổi §12 (đã chặn bằng câu "phục vụ mạch biến đổi, không thay trục"); phiên khai sai `--session` vượt phần giữ quota.

## Đang chờ chủ dự án
1. Duyệt bản viết CHUAN-KENH-LL §14 (7 bước + bảng giữ/bỏ sau 3 tập).
2. Trọng số nhãn cầu: giữ TẠM tới `channel-k2/CALIBRATION.md` (12/10).
3. Phiên P merge nhánh này vào `main`; tập 9: chọn đề tài, thêm vào `packs/ll.json`, chạy hồ sơ cầu từ 13/10.
4. Tuỳ chọn: YouTube Analytics API (OAuth) — chỉ làm khi chủ dự án yêu cầu.
