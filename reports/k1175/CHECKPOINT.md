# CHECKPOINT — phiên K-1.17.5 (nhánh `checks-1-17-5`, gốc origin/checks-1-17-4 @f4a3d9ca, LOCK 1.17.4 08486eb2…)

Nhánh harness gợi ý: `ccr-be60bd61-3pu9td` (đã fast-forward tới cùng gốc). Nhánh thật theo lệnh: `checks-1-17-5`.

## Trạng thái
| Giờ UTC | Việc | Trạng thái |
|---|---|---|
| 23:40 | Đọc CLAUDE.md, K1174-BAO-CAO §1/§9, BAI-HOC-LL (đầu), LOOK-T4-V2 §3/§11, PHIEU-LOOK-V2 (V3, V4), tam_nen_v2.py, Kinh thánh §14.1, §15; mã q_n2p.py, q_k1174.py, k2check, cap112 | xong |
| 23:48 | Nhánh `checks-1-17-5` từ origin/checks-1-17-4 @f4a3d9ca; hook pre-commit + pre-push (tools/preflight.sh) cài trước lần đẩy đầu; `lock.py --verify` KHỚP | xong |
| 23:55 | D11 tái hiện lại trên T6 (d11_tai_hien.py của K-1.17.4): SHA ghép l1/l2/l3 trùng từng bit; T9b như cũ (42,24 / 2,42 / 15,02 %) | xong |
| 00:00 | Mặt nạ ID look2 KHÔNG có trong git (ở /var/tmp phiên LOOK) → khung đáp án dùng T6 (mặt nạ trong git) + cảnh tổng hợp Blender `do/canh_tong_hop.py` (mặt nạ lớp + mã nhà + mã mặt phẳng chính xác từng bit, phản chiếu nước vật lý Cycles, biến đổi hình học có kiểm soát) | xong |
| 00:05–00:25 | A1/A2 lượt 1–3: thước đường bờ T9c với mẫu nước của chính tấm + phép thử gương (trục gương, vật cao, α, phần dư) — phân biệt phản chiếu AI ↔ bờ lấn KHÔNG đạt (dải chồng lấn; luật 0 lọt chỉ miễn ≈ 48 % dải phản chiếu 2D, 0 % phản chiếu vật lý Blender: phần dư màu 0,6–0,9) | bỏ hướng |
| 00:25–00:48 | A1/A2 lượt 4: ĐỐI CHỨNG RENDER — tấm ≈ T(render), T affine Lab khớp bền trên vùng nước → phản chiếu có trong render 3D giữ tự động, AI đổi sắc nước hấp thụ. Blender: 11/11 ca âm (phản chiếu vật lý, nhám, xám/ô-liu/nâu) ĐẠT; bờ lấn ≥ 8 px 29/32 → sửa mép bờ (kè/bóng ≤ 2 dải) + bờ dốc | đang làm |
| 00:00–00:48 | Render Blender: A1 20 cảnh xong; A5 (2 gốc + 34 biến thể + 2 pass bóng + 24 khung timelapse 960×540) đang chạy nền, ≤ 2 tiến trình nặng | đang chạy |
| 00:30–00:45 | A3 (lớp sống cộng hiệu) trên T6 + khói tổng hợp: phép (i-s) G = clip(nền + (R − N)) — đúng: lệch 0; dán nguyên kiểu T6: 72; lệch 6 px: 50; nửa cường độ: 22 | xong (số đo) |
| 00:30–00:45 | A4 (vòng bảo vệ): (i) của K chỉ đo trong mặt nạ (a), KHÔNG đo vòng nở — ràng buộc vòng = render là chữ Kinh thánh §15 (a); khớp màu cục bộ (một độ lệch/vật) giữ (i) 0/255, phần dư vòng ≤ 1; T6 không tái hiện được quầng của M1-rong (cần mặt nạ look2) | xong (số đo) |
| 00:50–01:25 | A5: 34 biến thể Blender + pass bóng + 24 khung timelapse; 2 ảnh AI thật (OpenAI edits, sổ AI); (d)(e) đạt cả hai nửa; (a) KHÔNG đạt 100 % ở 1,4–4,8 px/m — Chặn chỉ phần thô (đỡ < 0,20: 0/4 248 báo nhầm, xoá 3/3) | xong |
| 01:30–01:40 | (c) thật: lời nhắc BMN v2 (năm bắt buộc) 5/5 vật hiện đại + q_thoi_dai; 0 báo trên 2 ảnh AI sạch ($0,45 nhìn + $0,24 O2) | xong |
| 01:15 / 01:45 | checks-appeal.md: khiếu nại A1–A5 (trước) → phán quyết (sau) | xong |
| 01:52:26 | `lock.py` (không `--verify`, MỘT lần) → **1.17.5 `c7630b4a…`**; `--verify` KHỚP; selftest sau khoá đạt hết (k1175 52/52) | xong |
| 02:05–02:30 | k2check 1.17.5 trên T3 (719 s); 1.17.4 chạy lại từ worktree mở rộng (643 s; lượt đầu hỏng: worktree thưa thiếu RIGHTS.md — lỗi của phiên): 55/55 hàng chung giống hệt, + hàng 1.17.5 (T4) KHÔNG ÁP; 1.17.4 trùng hệt bảng K-1.17.4 | xong |
| 02:35 | Báo cáo `K1175-BAO-CAO.md` (§0–§14), quyết định K1175-D1…D7 | xong — **DỪNG chờ chủ dự án** |

## Lệnh bổ sung đã áp
- 00:37: `pkill -f cho2.sh` khớp chính shell (exit 144) — lặp bài học LL #24/#41 (đã nêu ở K-1.17.4); không mất dữ liệu; từ đây dừng tiến trình theo PGID (`kill -TERM -<PGID>`).
- 00:35: hàng đợi Blender A1 chạy hai bản song song vài phút (tôi xoá thư mục B-mau-nau khi tiến trình gốc còn sống) — dừng bản thứ hai theo PGID 5177; P nặng ≤ 2 giữ.
- 01:45: cất `checks/` bằng stash để commit khi selftest cũ đang chạy nền — lặp bài học K-1.17.4 (2); selftest đó vẫn đạt; mọi selftest chạy lại sau khoá đạt.
- 02:00: worktree thưa 1.17.4 thiếu tệp gốc (RIGHTS.md) → lượt k2check 1.17.4 đầu lỗi; mở rộng worktree (mọi tệp gốc, bỏ channel-k2/design/reports/assets) và chạy lại.
- Lỗi của chính phiên đã sửa: canh_tong_hop.py chiếu px/m khi ma trận máy chưa cập nhật (px/m 229–327 sai) → thêm view_layer.update(), sinh lại cấu hình A5; kè đứng gán 'congsu' (vật cao) thay 'suon'.
