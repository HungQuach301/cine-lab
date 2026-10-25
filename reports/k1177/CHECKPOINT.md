# CHECKPOINT — phiên K-1.17.7 (nhánh thật `claude/k1177-animatic-checks-nfbsbr` — harness buộc; lệnh ghi `checks-1-17-7`; gốc origin/main @2a49e3ca, LOCK 1.17.6 513c9442…)

Giờ UTC theo đồng hồ container (giờ commit git); dòng 02:36–03:00 của bản checkpoint trước ghi giờ ước sai — nay sửa theo giờ tệp/commit.

## Trạng thái
| Giờ UTC | Việc | Trạng thái |
|---|---|---|
| ≈ 02:25 | verify.sh (10 PASS, 5 FAIL tuỳ chọn: OpenEXR, three.js, tifffile/pyshp, k2v node_modules, Freesound); đọc CLAUDE.md, BAI-HOC-LL, K1176-BAO-CAO, ANIMATIC-T4-BAO-CAO §9, PHIEU-XEM C11/C13/C14 | xong |
| 02:34 | hook pre-commit + pre-push (tools/preflight.sh) cài trước lần đẩy đầu; `lock.py --verify` KHỚP 513c9442 | xong |
| 02:34:36 | checks-appeal.md: A1–A5 + C11 + C13 + ghi chú C14 chép nguyên văn — TRƯỚC khi phán (commit 839d4b52), đẩy 02:35 | xong |
| 02:36–02:42 | Đọc mã k2check, q_k1174, q_k1176, q_k116, q_lai, q_nhip, q_n2p, q_thoi_dai; tái hiện A2 (H5-07b 51 704 px với neo [E, N, h] đọc như hệ cảnh; neo đúng: khung đầu M03 0 px, khung cuối 36 px; H2-12 "đạt giả" 0,08 px → neo đúng 51,9 px đầu/cuối H1-03, 0,128 px khung 202); A4 (Q37 (a) so beats với mốc ĐẶC TẢ — 12 lớp chồng không có trong đặc tả); A5 (n2p.tam ở log shot) | xong |
| 02:42 | YuNet 2023mar tải (HF opencv/face_detection_yunet, MIT, SHA 8f2383e4…) | xong |
| 02:43–02:45 | q_thoi_dai lớp công trình mốc; hiệu chuẩn 9 lần gọi claude-sonnet-5-5 ($0,30): H2-13 v1 bắt 3/3, khung đúng 0/3; lớp chung: H2-13 bắt, 2 khung đúng 0 | xong; commit 3c3d50a2 02:45 (đẩy) |
| 02:46–02:52 | Hiệu chuẩn YuNet trên 23 clip M-d (347 hộp ≥ 4 % khung; đáp án bằng mắt → ngưỡng 0,75; bắt 8/18 mặt thấy được ≥ 3,5 %) | xong (`do/mat/DAP-AN.md`) |
| 02:47–02:58 | Mã 1.17.7: q_k1177 (mới), q_k1174 (A1/A2/THAT), q_k1176 (trần 20, THAT), q_k116 (TL-1), q_nhip (lop_chong), q_n2p (A5), q_k1175 + q_k1176 (sàn Y nhấp nháy), cap112, k2check, VERSION 1.17.7, RULES-LL §1.17.7; selftest_k1177 **85/85** (sau 2 lần sửa chính bài thử); selftest_k1176: ca (k) "khai 20" đổi thành "khai 25" (trần duyệt 15 → 20) | xong |
| 02:54–03:00 | k2check thử 1.17.7 trên animatic T4 (không video): chạy được; GOC-CAO 67,2 %, K-LAI-1 ĐẠT (M-d 20,4 % không tính), MAY-19 (c) 0 | xong |
| 03:03 | Cất `checks/` sửa dở (stash + tgz `/var/tmp/k1177/wip`) → cây 1.17.6 KHỚP; master T3 LFS tải (SHA 5b9f0bcc… khớp); đầu vào T3 tái tạo (git archive + mk_tl + mk_log_chu); chạy đối chứng 1.17.6 trên T4 (video nối 3 bản xem, SHA 4263d29d…) và T3 song song (P = 2) | đang chạy |

## Lệnh bổ sung đã áp
- (không có lệnh bổ sung từ chủ dự án trong phiên)
- Ghi chú vận hành: mã `checks/` chưa khoá không commit được (preflight `lock.py --verify`) → bản vá WIP ở `reports/k1177/wip/checks-wip.patch`; đẩy bằng `reports/k1177/day.sh` (cất checks/ khi đẩy).
