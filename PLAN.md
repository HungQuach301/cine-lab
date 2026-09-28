# PLAN — Bảng điều phối (phiên P duy trì)

## Mốc hiện tại: M2 — Cổng 5 (layout) · Cổng 4 ĐÃ ĐÓNG và merge vào main (5987bf3) · characters v1.3 (D2) · checks v1.4 (LOCK 289c6916…)

Quy ước nhánh: mọi nhánh làm việc tạo từ `main` (đã hợp nhất M0 + checks/v0 ngày 27/09/2026, LOCK KHỚP `57dc729b…`). Chỉ P merge vào `main`.
Video > 30 MB: đẩy lên nhánh git, không gửi qua giao diện.

## Hàng chờ chủ dự án duyệt
1. **Cổng 5 (layout) — DỪNG, chờ duyệt** (`reports/m2/CONG-5.md`): xem `screening/layout.mp4`; chọn **A** (mặt Ida), **B** (continuity C2: góc sáng tường chim), **C** (cách đóng Cổng 5). KHÔNG merge trước khi duyệt.
2. **Cổng mặt Ida KHÔNG ĐẠT** sau A1 (kiểm mù lần 4) và A3 (lần 5): cùng trượt tiêu chí "mặt nạ/búp bê/ma-nơ-canh/con rối" 3/3. Chặn Cổng 6. Chờ quyết định A.
3. Xem 3 shot C3 cờ: s08, s27, s47 (`reports/m2/cong5/c3-nguoi-xem/BANG.md`).
4. Việc nhỏ: đèn lồng cháy từ s02 hay mồi ở L4; máy mới s02, s15; lọn tóc 'temple' + câu chữ cổ áo bible v1.4; mũ nâu cam dưới đèn khí sát mặt (D2); khiếu nại P0 (chuyển K); hàng đợi render có thứ tự.

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
| M1 Cổng 4: cổng mặt Ida (biến dạng, đẩy mũ, kiểm mù) + animatic 2:30 (48 shot) + âm tạm + gói chiếu mù | P | claude/cine-lab-m1-cong4-animatic | Vòng v1 xong; xem vòng v2 | reports/m1/CONG-4.md |
| M2 Cổng 5 layout (W1, W2, W3 + P) | P + 3 subagent + 2 agent rà | claude/cine-lab-m2-cong5-layout-24o5fp | **Chờ chủ dự án duyệt — KHÔNG merge** | reports/m2/CONG-5.md |
| M1 Cổng 4 vòng v2: animatic 2:22,5 (52 shot), kịch bản nháp 3, luật thế giới v0.4, characters v1.2 (A1), C3 v1.4 (parts + views + kiểm toán) | P | claude/cine-lab-m1-cong4-animatic | **Đã merge vào main (5987bf3)** — Cổng 4 đóng | reports/m1/CONG-4-V2.md, shots/animatic/SHOTLIST.md, screening/animatic_v1_v2_diff.md |

Quy ước file lớn Cổng 4: `design/cong4/animatic/out/animatic.mp4` (v2: 45,49 MB) nằm trong nhánh; mặt nạ C3 `out/animatic.parts/` (18 MB, PNG xám) cũng trong nhánh; video nhóm và video ghép trung gian `out/v2/*.mp4`, âm trung gian `out/v2/audio/` KHÔNG commit; `screening/animatic.mp4` là bản sao y từng byte. Bản trung gian `out/video.mp4` (187 MB) và đối chứng `out/hq/` (198 MB) KHÔNG commit (vượt giới hạn GitHub; tái tạo bằng `render_film.js` / `HQ=1 package.py`). Âm lưu FLAC 24-bit.

## M2 · Cổng 5 — Layout (P điều phối, 3 gói song song)
Nhánh tích hợp: `claude/cine-lab-m2-cong5-layout-24o5fp` (tạo từ main 5987bf3). Mã layout: `design/cong5/layout/` (tách từ animatic Cổng 4).

| Gói | Agent | Phạm vi shot | File được sửa (chỉ gói đó) | Đầu ra |
|---|---|---|---|---|
| **W1** | cine-worker, worktree | Cảnh 1–3: s01 → s24c — **xong (A, C, sửa N1)** | `shots_w1.js`, `order_w1.js`, `sets.js` (bộ phố, trừ phần cuối phố) | `shots/layout/continuity/canh-1..3.md`, `shots/layout/shots_w1.json`, render ở `/var/tmp/cine-out/W1/` |
| **W2** | cine-worker, worktree | Cảnh 4–6 (kịch bản ghi cảnh 4–7): s25 → s48 — **xong (A, C, D sửa continuity); C2 chờ chủ dự án** | `shots_w2.js`, `order_w2.js`, `sets2.js`, `sets_end.js` (cuối phố: V3) | `shots/layout/continuity/canh-4..6.md`, `shots/layout/shots_w2.json`, render ở `/var/tmp/cine-out/W2/` |
| **W3** | cine-worker, worktree | Mặt Ida (A1 → A3 nếu trượt) — **A1 trượt, A3 trượt; mã A3 lưu dạng patch, layout dùng A1** | `design/cong3/v2/char3d/*` (mặt, cổ áo), `design/cong5/mat/` | ảnh thử, đề xuất đổi sheet/bible gửi P |
| P | phiên này | ghép, `common.js`, `film.js`, âm, đóng gói, luật máy, kiểm mù, báo cáo | `common.js`, `film.js`, `page.js`, `render_film.js`, `assemble.py`, `package.py`, bible/, sheet, SHA | `screening/layout.mp4`, `reports/m2/CONG-5.md` |

Luật chung:
- Subagent KHÔNG sửa `bible/`, `checks/`, không đọc mã trong `checks/`. Đề xuất đổi bible/sheet gửi P; P sửa và khoá SHA.
- Sửa lỗi: V1 (s42b/s42, W2), V2 (s31–s33, W2), V3 (cuối phố 0:52 s23 W1 dùng `sets_end.js` của W2; 1:04 s27, 1:40 s37w W2), V4 (s26, W2), D2 mũ (đã vào sheet v1.3, P).
- Thoại nguyên văn; tổng thời lượng quanh 2:22,5 (lệch > ±5 s phải báo).
- **Hàng đợi render nặng:** `scripts/render/queue.sh <gói> <nhãn> -- <lệnh>` (flock, mỗi lúc 1 render nặng). Nhật ký thời gian thật `/var/tmp/cine-queue/log.tsv`, P chép vào `reports/m2/cong5/queue-log.tsv`. Probe ≤ 3 khung/shot ở 960×540 là việc nhẹ.
- Chờ tiến trình nền bằng `while kill -0 $PID` (bài học vòng chờ). Chỉ render lại phần thay đổi.
- Thứ tự: (A) W1/W2 chốt layout + probe + continuity + manifest; W3 làm A1 bằng ảnh tĩnh → (B) P merge W3 + A vào nhánh tích hợp → (C) W1/W2 merge nhánh tích hợp, render đầy đủ qua hàng đợi → (D) P ghép, âm, kiểm mù lần 4 (ảnh 4 lấy từ s39 layout), cine-continuity rà toàn phim, luật máy, `screening/layout.mp4`.
- File lớn: render trung gian ở `/var/tmp/cine-out/` (không commit); `design/cong5/layout/out/layout.mp4` và `screening/layout.mp4` (< 50 MB) commit.
