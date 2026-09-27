# PLAN — Bảng điều phối (phiên P duy trì)

## Mốc hiện tại: M1 — Tiền kỳ "Last Round" · Cổng 1 đã chọn (P3) · đang DỪNG ở Cổng 2 (Kịch bản, nháp 1)

Quy ước nhánh: mọi nhánh làm việc tạo từ `main` (đã hợp nhất M0 + checks/v0 ngày 27/09/2026, LOCK KHỚP `57dc729b…`). Chỉ P merge vào `main`.
Video > 30 MB: đẩy lên nhánh git, không gửi qua giao diện.

## Hàng chờ chủ dự án duyệt
1. **Cổng 2:** chọn A/B/C cho 6 điểm (hình mở, hình kết, câu L5, đồng hồ, cao trào, thời lượng) — `reports/m1/CONG-2.md`, chat 27/09.
2. Nghe table read `reports/m1/cong2/tableread/last-round-tableread.mp3`, xác nhận bằng tai 5 câu đủ từ (J1 máy trượt vì ASR — khiếu nại đã ghi).
3. **Cổng 1 tiêu chí L3:** đọc logline P3 cho 3 người, ≥ 2 kể lại đúng và muốn xem.
4. Duyệt `bible/world-rules.md` (luật hai loại ánh sáng, chim bóng).
5. Phiên K: phán quyết 3 khiếu nại J1 trong `checks-appeal.md`.

## Bảng gói việc
| Gói | Phiên/agent | Nhánh | Trạng thái | Báo cáo |
|---|---|---|---|---|
| M0 Cổng 0 | P | claude/jolly-edison-a4hq3n | Đã merge vào main | reports/m0/BAO-CAO-M0.md |
| checks v0 | K | checks/v0 | Đã merge vào main | checks/RULES.md, reports/checks-selftest/ |
| M1 hợp nhất + giọng + banding + Cổng 1 | P | claude/cine-lab-m1-last-round-f1667s | Cổng 1 đã chọn P3 | reports/m1/CONG-1.md, reports/m1/banding/BANDING.md |
| M1 Cổng 2 kịch bản nháp 1 + table read | P | claude/cine-lab-m1-last-round-f1667s | Chờ duyệt Cổng 2 | reports/m1/CONG-2.md, scripts/last-round.fountain |
