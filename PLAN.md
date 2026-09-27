# PLAN — Bảng điều phối (phiên P duy trì)

## Mốc hiện tại: M1 — Tiền kỳ "Last Round" · kịch bản CHỐT · thiết kế KHOÁ (Cổng 3, main c21e5df) · checks v1.3 (K đang làm v1.4) · đang DỪNG ở Cổng 4 (animatic)

Quy ước nhánh: mọi nhánh làm việc tạo từ `main` (đã hợp nhất M0 + checks/v0 ngày 27/09/2026, LOCK KHỚP `57dc729b…`). Chỉ P merge vào `main`.
Video > 30 MB: đẩy lên nhánh git, không gửi qua giao diện.

## Hàng chờ chủ dự án duyệt
1. **Cổng 4:**
   - xem animatic `screening/animatic.mp4`;
   - quyết định A/B/C trong `reports/m1/CONG-4.md`, gồm: cổng mặt Ida (giới tính còn đọc do dự), mốc câu hỏi 0:40 hay 0:48, và bước chiếu mù.
2. **Chiếu mù:** 3–5 người xem thật, dùng `screening/questions.json` (chủ dự án tổ chức).
3. **Cổng mặt Ida** vẫn mở. Không được sang Cổng 6 khi cổng này chưa đóng.
4. **Chờ K v1.4:**
   - khiếu nại C3 (tư thế/góc);
   - gộp hai khiếu nại vòng 3 đã chấp nhận.

## Bảng gói việc
| Gói | Phiên/agent | Nhánh | Trạng thái | Báo cáo |
|---|---|---|---|---|
| M0 Cổng 0 | P | claude/jolly-edison-a4hq3n | Đã merge vào main | reports/m0/BAO-CAO-M0.md |
| checks v0 | K | checks/v0 | Đã merge vào main | checks/RULES.md, reports/checks-selftest/ |
| M1 hợp nhất + giọng + banding + Cổng 1 | P | claude/cine-lab-m1-last-round-f1667s | Cổng 1 đã chọn P3 | reports/m1/CONG-1.md, reports/m1/banding/BANDING.md |
| M1 Cổng 2 kịch bản nháp 1 → nháp 2 + table read | P | claude/cine-lab-m1-last-round-f1667s | Chờ duyệt Cổng 2 (nháp 2) | reports/m1/CONG-2.md, scripts/last-round.fountain |
| M1 Cổng 3 vòng 1: nền chung, model sheet, 3 hướng (3 subagent song song), color script | P + 3 subagent | claude/cine-lab-m1-cong3-design | Chờ chủ dự án chọn | reports/m1/CONG-3-VONG-1.md |
| M1 Cổng 3 vòng 2: hạ tầng 4 shot, 2 cách nhân vật (2 subagent), C2 mù, nhấp nháy | P + 2 subagent | claude/cine-lab-m1-cong3-v2 | Chờ chủ dự án chọn | reports/m1/CONG-3-VONG-2.md |
| M1 Cổng 3 vòng 3 + đợt vá A2+ + khoá thiết kế | P | claude/cine-lab-m1-cong3-v3 | **Đã merge vào main (c21e5df)**; SHA khoá `design/cong3/LOCK-THIET-KE.sha256` | reports/m1/CONG-3-VONG-3.md, reports/m1/CONG-3-VA-A2PLUS.md |
| M1 Cổng 4: cổng mặt Ida (biến dạng, đẩy mũ, kiểm mù) + animatic 2:30 (48 shot) + âm tạm + gói chiếu mù | P | claude/cine-lab-m1-cong4-animatic | Chờ chủ dự án duyệt — **KHÔNG merge** | reports/m1/CONG-4.md, shots/animatic/SHOTLIST.md |

Quy ước file lớn Cổng 4: `design/cong4/animatic/out/animatic.mp4` (47,85 MB) nằm trong nhánh; `screening/animatic.mp4` là bản sao y từng byte. Bản trung gian `out/video.mp4` (187 MB) và đối chứng `out/hq/` (198 MB) KHÔNG commit (vượt giới hạn GitHub; tái tạo bằng `render_film.js` / `HQ=1 package.py`). Âm lưu FLAC 24-bit.
