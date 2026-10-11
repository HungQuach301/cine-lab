# P-G1-LO — mở một lô tập đến G1 (dán một dòng: "Chạy playbook/prompts/P-G1-LO.md cho lô <tập>: <cặp nghề…>")

1. Khởi động: `bash scripts/env/verify.sh` (thiếu node_modules → `npm ci`, ghi kết quả, không dừng). Đọc `reports/m3/BAI-HOC-LL.md`, `CHUAN-KENH-LL.md` §3, §7–8.
2. Nguồn: P **tự tải và lọc** (`curl` + `pdftotext` + `grep`) trước; chỉ giao subagent Sonnet đoạn trích đã cắt (~10 nghìn token/nguồn). Không Wikipedia, không đoán URL quá 1 lần. Số bls.gov → liệt kê bảng/URL cho Claude (Cowork), đánh dấu CHỜ XÁC MINH.
2b. **Dữ liệu (CHUAN-KENH §14, không thêm cổng):** Việc 0 `market.py own` + `market.py topic <slug>` (quota cho phép; không đủ thì chờ ngày quota, hồ sơ bắt buộc trước G1). Lời trả lời ≥ 3/5 câu hỏi khán giả (bảng câu → đoạn), một nhịp xử lý điểm yếu đối thủ (không tên kênh), độ dài trong dải thắng hoặc ghi lý do; kiểm mù: một người đọc nhập vai người hỏi.
3. Mỗi tập: `reports/m3/epNN/episode.yaml` (`ll.py check` ĐẠT, `ll.py est` ước thời lượng/tỷ lệ), `NGUON-TAPN.md`, bảng 6 điểm, 3 tiêu đề (số khớp nguồn; không "your job is next"), tóm tắt 5 dòng; dòng DỰ ĐOÁN (`market.py predict <slug> --ep epNN`) + dòng hồ sơ cầu (khoảng trống, 3 video vượt trội, dải thắng); tiêu đề theo một khuôn thắng của hồ sơ, không hứa vượt claim.
4. Thẻ so sánh: ưu tiên **cùng nguồn, cùng kỳ** (BLS 2025–35); vế lịch sử chỉ làm bối cảnh nếu khác cơ chế/kỳ (BAI-HOC #17).
5. Báo cáo `reports/m3/LO-…-G1.md`; mỗi quyết định có phương án + khuyến nghị; nêu chỉ số trong ±5 % ngưỡng. Ghi token thật. **DỪNG ở G1.**
