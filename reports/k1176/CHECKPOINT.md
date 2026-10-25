# CHECKPOINT — phiên K-1.17.6 (nhánh `checks-1-17-6`, gốc origin/main @df317915, LOCK 1.17.5 c7630b4a…)

Nhánh harness gợi ý: `claude/beautiful-turing-rqkp8c` — không dùng để đẩy công việc. Nhánh thật theo lệnh: `checks-1-17-6`.

## Trạng thái
| Giờ UTC | Việc | Trạng thái |
|---|---|---|
| 08:20 | Đọc CLAUDE.md, BAI-HOC-LL (đầu), K1175-BAO-CAO, khieu-nai-K.md (THU-B @353d0f0c), mã q_n2p.py / q_k1175.py | xong |
| 08:30 | `git archive` THU-B (thu-b/, reports/thu-b-t4/) → /var/tmp/k1176/thub (207 MB, không sửa) | xong |
| 08:34 | Nhánh `checks-1-17-6` từ origin/main @df317915; hook pre-commit + pre-push (tools/preflight.sh) cài trước lần đẩy đầu; `lock.py --verify` KHỚP | xong |
| 08:40 | checks-appeal.md: KN-1…KN-6 chép nguyên văn (sha256 nguồn 7a76f249…) + yêu cầu kèm theo — TRƯỚC khi phán | xong |
| 08:42–08:52 | Dữ liệu nền LOOK dựng lại trong bản sao tạm `/var/tmp/k1176/src` (git archive THU-B: design/k2v, design/cong3/shared, scripts, channel-k2/k2c-t4-02, LUT T3) để tái tạo video kiểm không mất (video-sha.json); lượt 1 thiếu pyproj → cài pyproj/tifffile/pyshp, chạy lại → DUNG-LAI-XONG 08:51; `ldn2.bin` bd776509… TRÙNG phiên THU-B | xong |
| 08:44–08:50 | Mã: `q_k1176.py` (mới), q_k1175 (T9c đủ khoá; (d) theo điểm ảnh; (e) độ phân giải video; px/m theo tập; KN-3), q_n2p (KN-1, KN-2), q_n2p_vision (KN-3) — bản vá WIP `reports/k1176/wip/checks-wip.patch` | đang làm |
| 08:50 | KN-1 tái hiện bằng 1.17.5 trên kiem/M4-l12, B3-l2: KeyError 'so_doan_lan' (B3: nước 213 px < 0,2 % khung → T9c trả sớm thiếu khoá). Bản sửa: 3 hàng N2P chạy, T9c KHÔNG ÁP. KN-2: M1/B3/M4 (a) sau trừ vùng BMN 0/255 (trước: 218/224/183) | xong (số đo) |
| 08:52–(chạy) | Tái tạo video kiểm không mất (`/var/tmp/k1176/tai/tai_video.sh`, mã THU-B nguyên bản): look3b (SHA ldn2 trùng), nướng 1938.7 (55da7758…), tl-B3 V2 540 s; đang: chiếu 3D B3, rồi M4, M1 | đang chạy |
| 08:55–09:10 | KN-4: đáp án lập bằng mắt TRƯỚC khi đo (`do/kn4-dap-an.json`: B3 l1 20 ống khói + 2 đầu hồi; l2 0); 4 thước thử (khối màu theo mặt phẳng; phần dư affine; cạnh mới; cạnh mới có hướng) — tối đa 17/20, không điểm nào 100 % ở báo nhầm thấp → CHỈ BÁO (w), không đề xuất Chặn | xong (số đo) |
| 09:04 | Master T3 LFS `release-k2-t3-g2` tải về (UA CineLab-research), SHA 5b9f0bcc… khớp | xong |
| 09:12–09:14 | KN-3 gọi thật 2 tấm (M4 l1, B3 l1): 2/2 đọc đủ 10/10 lần 1; THU-B 4/14 lần thiếu → đường gọi lại kiểm bằng selftest; sổ AI `so-ai.jsonl` 4 dòng $0,1997 | xong |
| 09:15 | Video kiểm B3 l2 tái tạo: render, ảnh tĩnh, tỉ số bóng TRÙNG SHA video-sha.json; chiếu 3D khác SHA (PSNR so bản xem 34,73 dB ≈ nền mã hoá 35,23 dB; 1.17.5 cho đúng số THU-B 15,0 % · 4,6/12,6) | xong |
| 09:20 | selftest_k1176 57/57 (sau 3 lần sửa CẢNH tổng hợp của chính bài: bão hoà 8 bit, mã sRGB tuyến tính, pass bóng phẳng — không sửa luật) | xong |
| 09:25 | KN-5/6 B3 thật: tỉ số bóng 7,2 % → ĐẠT (d)(e); chiếu 3D (e) ĐẠT ở 640×360, (d) 15,0 → 9,4 % (tường sáng hơn render ~20 % khi nắng đổi — lệch ánh sáng thật của bản dựng); ảnh tĩnh TRƯỢT 85,5 % | xong |
| 09:28– | k2check 1.17.5 trên T3 (cây origin/main, master LFS) chạy nền; tái tạo M4, M1 chạy nền | đang chạy |
| 09:58 | Tái tạo M4 (khác SHA, 1.17.5 cho đúng số THU-B) + M1 (trùng SHA 3/4); T3 1.17.5 chạy lại có git cục bộ → TRÙNG HỆT bảng K-1.17.5 | xong |
| 10:00–10:15 | KN-5 M1: tỉ số bóng 5,8 % do lượng tử 8 bit khung gần đen (không do khói) → sàn Y ≥ 0,01 (chọn trên M1, ghi rõ) → 1,6 %; ảnh tĩnh vẫn trượt; selftest +2 ca sàn | xong |
| 10:15–10:25 | Thử k2check B3 trước khoá: N2P-1 (b) mô hình báo khung cửa sổ trong vùng BMN → (c) người đọc (cùng nguyên tắc KN-2), selftest +3 ca qua kiem_tam; selftest cũ trước khoá đạt hết | xong |
| 10:26:29 | `lock.py` (MỘT lần) → 1.17.6 `513c9442…`; `--verify` KHỚP; commit 7a35dd86 | xong |
| 10:30 | khởi chạy selftest sau khoá; k2check 1.17.6 T3 (cây tạm có git); k2check THU-B (gốc + px4) | xong (dòng dưới) |
| 10:30–10:50 | selftest sau khoá: tất cả đạt (k1176 62/62; 0 SAI); T3 1.17.6 = 1.17.5 ngoài nhãn LOCK; k2check THU-B 6 lượt (gốc + khai 4 px/m): tỉ số bóng B3/M4/M1 qua đủ Chặn ở ngưỡng 2; khai 4 → (b) trượt (tấm ghép cả nhà 2–4 px/m) | xong |
| 10:55 | M1 nhấp nháy tỉ số bóng 0,0119 / 0,0133 (4 px/m): không do khói, do khung gần đen — thước nhấp nháy chưa có sàn Y → K1176-D6 (mã đã khoá một lần, không sửa) | xong |
| 11:00 | Báo cáo `K1176-BAO-CAO.md` (§0–§14), phán quyết trong `checks-appeal.md`, K1176-D1…D6 | xong — **DỪNG chờ chủ dự án** |

## Lệnh bổ sung đã áp
- 08:35: `git worktree add` toàn nhánh THU-B làm đầy đĩa (≈ 6 GB, còn 9,5 GB) → dừng theo PGID, xoá; thay bằng `git archive` chỉ thư mục cần (≈ 280 MB).
- 08:40: vòng chờ `until ! pgrep -f "git reset …"` khớp chính dòng lệnh của nó (lặp bài học K-1.17.5 (1)) → dừng theo PGID; từ đây chờ bằng PID cụ thể (`kill -0 <pid>`), không `pgrep -f` với chuỗi có trong lệnh chờ.
- 08:58: `open(…,'w')` trước khi đọc làm rỗng `checks/cinecheck/__init__.py` (lỗi thao tác) → khôi phục `git checkout --`, sửa VERSION bằng sed; không ảnh hưởng gì khác.
- 10:00: hai lượt nặng chạy song song (tái tạo M1 + k2check T3) — P ≤ 2 giữ; RAM ≥ 5 GB giữ (dung.py chờ RAM).
- 10:55: sau khoá phát hiện khiếm khuyết nhấp nháy (thiếu sàn Y) — không khoá lại (lệnh: lock.py đúng một lần) → ghi K1176-D6.
