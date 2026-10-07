# P-SAN-XUAT — sản xuất một tập đến G2 (dán: "Chạy playbook/prompts/P-SAN-XUAT.md cho tập NN")

1. Đọc `reports/m3/epNN/PLAN.md` và các tệp "Phiên sau đọc" (≤ 8). Ngân sách đĩa: ghi mức cần/mức trống vào PLAN tập (≥ 1,5 ×).
2. **Kiểm mù trước khi thu giọng:** trích lời ra một tệp; 1 subagent Sonnet đọc với 3 vai độc lập (chỉ đưa lời, không đưa repo), trần ~50 nghìn. Sửa điểm ≥ 2/3 vai cùng nêu; tóm tắt vào báo cáo G2.
3. `bash scripts/ll/tests/run.sh` (test thư viện) → `bash scripts/ll/build.sh reports/m3/epNN/episode.yaml` (ASR → prep → render → mix → ghép → Shorts → KHAN-GIA) → `bash scripts/ll/qc.sh …`.
4. Chỉ mở vòng sửa khi qc TRƯỢT hoặc sai nội dung (CHUAN-KENH §8). Gom sửa `lib/` vào một lượt (đổi lib = render lại mọi đoạn).
5. Phát hành: `phat-hanh/make_thumb.py`, `make_desc.py`, text Shorts; qc Q12/Q13 ĐẠT; khung tổng quan `khung-g2.jpg`; bản xem `screening/…-p1/p2/p3.mp4`; master + Shorts lên nhánh `release-ll-epNN-v1` (LFS), tải ngược kiểm SHA.
6. Báo cáo `reports/m3/TAPN-G2.md` (bàn giao, qc, tỷ lệ, kiểm mù, token/ElevenLabs/giờ máy/đĩa, hàng chờ, chờ chủ dự án). AUTHORSHIP. Thêm bài học vào `BAI-HOC-LL.md`. **DỪNG ở G2.**
