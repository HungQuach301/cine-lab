# PLAN — Bảng điều phối (phiên P duy trì)

## Mốc hiện tại: M1 — Tiền kỳ "Last Round" · kịch bản CHỐT · checks v1.1 · đang DỪNG ở Cổng 3 vòng 2 (nhân vật)

Quy ước nhánh: mọi nhánh làm việc tạo từ `main` (đã hợp nhất M0 + checks/v0 ngày 27/09/2026, LOCK KHỚP `57dc729b…`). Chỉ P merge vào `main`.
Video > 30 MB: đẩy lên nhánh git, không gửi qua giao diện.

## Hàng chờ chủ dự án duyệt
1. **Cổng 3 vòng 2:** chọn cách làm nhân vật, duyệt phóng to tay và chi tiết thứ cấp, chim bóng, cảnh 5, ngân sách (A/B/C trong chat; `reports/m1/CONG-3-VONG-2.md`).
2. Duyệt hồ sơ nhân vật `bible/characters.md` (C1).

## Bảng gói việc
| Gói | Phiên/agent | Nhánh | Trạng thái | Báo cáo |
|---|---|---|---|---|
| M0 Cổng 0 | P | claude/jolly-edison-a4hq3n | Đã merge vào main | reports/m0/BAO-CAO-M0.md |
| checks v0 | K | checks/v0 | Đã merge vào main | checks/RULES.md, reports/checks-selftest/ |
| M1 hợp nhất + giọng + banding + Cổng 1 | P | claude/cine-lab-m1-last-round-f1667s | Cổng 1 đã chọn P3 | reports/m1/CONG-1.md, reports/m1/banding/BANDING.md |
| M1 Cổng 2 kịch bản nháp 1 → nháp 2 + table read | P | claude/cine-lab-m1-last-round-f1667s | Chờ duyệt Cổng 2 (nháp 2) | reports/m1/CONG-2.md, scripts/last-round.fountain |
| M1 Cổng 3 vòng 1: nền chung, model sheet, 3 hướng (3 subagent song song), color script | P + 3 subagent | claude/cine-lab-m1-cong3-design | Chờ chủ dự án chọn | reports/m1/CONG-3-VONG-1.md |
| M1 Cổng 3 vòng 2: hạ tầng 4 shot, 2 cách nhân vật (2 subagent), C2 mù, nhấp nháy | P + 2 subagent | claude/cine-lab-m1-cong3-v2 | Chờ chủ dự án chọn | reports/m1/CONG-3-VONG-2.md |
