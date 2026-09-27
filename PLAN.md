# PLAN — Bảng điều phối (phiên P duy trì)

## Mốc hiện tại: M1 — Tiền kỳ "Last Round" · Cổng 1 đã chọn (P3) · đang DỪNG ở Cổng 2 (Kịch bản, nháp 2)

Quy ước nhánh: mọi nhánh làm việc tạo từ `main` (đã hợp nhất M0 + checks/v0 ngày 27/09/2026, LOCK KHỚP `57dc729b…`). Chỉ P merge vào `main`.
Video > 30 MB: đẩy lên nhánh git, không gửi qua giao diện.

## Hàng chờ chủ dự án duyệt
1. **Cổng 2 nháp 2:** chọn A/B/C cho điểm 7 (tường khuất điện cảnh 5), 8 (nhịp đồng hồ cảnh 3), 9 (chỉnh giờ cảnh 6), 10 (bóng lúc chạng vạng cảnh 1), 11 (thời lượng) — `reports/m1/CONG-2.md` mục "NHÁP 2", chat 27/09.
2. Nghe table read nháp 2 `reports/m1/cong2/tableread-d2/last-round-tableread-d2.mp3`.
3. Duyệt các mục **[P]** trong `bible/world-rules.md` v0.2.
4. **Cổng 1 tiêu chí L3:** đọc logline P3 cho 3 người.
5. **Phiên K:** sửa J1 theo 3 khiếu nại đã được chấp nhận; P chạy lại J1 trên table read nháp 2.

## Bảng gói việc
| Gói | Phiên/agent | Nhánh | Trạng thái | Báo cáo |
|---|---|---|---|---|
| M0 Cổng 0 | P | claude/jolly-edison-a4hq3n | Đã merge vào main | reports/m0/BAO-CAO-M0.md |
| checks v0 | K | checks/v0 | Đã merge vào main | checks/RULES.md, reports/checks-selftest/ |
| M1 hợp nhất + giọng + banding + Cổng 1 | P | claude/cine-lab-m1-last-round-f1667s | Cổng 1 đã chọn P3 | reports/m1/CONG-1.md, reports/m1/banding/BANDING.md |
| M1 Cổng 2 kịch bản nháp 1 → nháp 2 + table read | P | claude/cine-lab-m1-last-round-f1667s | Chờ duyệt Cổng 2 (nháp 2) | reports/m1/CONG-2.md, scripts/last-round.fountain |
