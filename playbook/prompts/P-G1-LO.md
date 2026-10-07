# P-G1-LO — mở một lô tập đến G1 (dán một dòng: "Chạy playbook/prompts/P-G1-LO.md cho lô <tập>: <cặp nghề…>")

1. Khởi động: `bash scripts/env/verify.sh` (thiếu node_modules → `npm ci`, ghi kết quả, không dừng). Đọc `reports/m3/BAI-HOC-LL.md`, `CHUAN-KENH-LL.md` §3, §7–8.
2. Nguồn: P **tự tải và lọc** (`curl` + `pdftotext` + `grep`) trước; chỉ giao subagent Sonnet đoạn trích đã cắt (~10 nghìn token/nguồn). Không Wikipedia, không đoán URL quá 1 lần. Số bls.gov → liệt kê bảng/URL cho Claude (Cowork), đánh dấu CHỜ XÁC MINH.
3. Mỗi tập: `reports/m3/epNN/episode.yaml` (`ll.py check` ĐẠT, `ll.py est` ước thời lượng/tỷ lệ), `NGUON-TAPN.md`, bảng 6 điểm, 3 tiêu đề (số khớp nguồn; không "your job is next"), tóm tắt 5 dòng.
4. Thẻ so sánh: ưu tiên **cùng nguồn, cùng kỳ** (BLS 2025–35); vế lịch sử chỉ làm bối cảnh nếu khác cơ chế/kỳ (BAI-HOC #17).
5. Báo cáo `reports/m3/LO-…-G1.md`; mỗi quyết định có phương án + khuyến nghị; nêu chỉ số trong ±5 % ngưỡng. Ghi token thật. **DỪNG ở G1.**
