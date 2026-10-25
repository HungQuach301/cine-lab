# CHECKPOINT — phiên K-1.17.7 (nhánh thật `claude/k1177-animatic-checks-nfbsbr` — harness buộc; lệnh ghi `checks-1-17-7`; gốc origin/main @2a49e3ca, LOCK 1.17.6 513c9442…)

## Trạng thái
| Giờ UTC | Việc | Trạng thái |
|---|---|---|
| 02:20 | verify.sh (10 PASS, 5 FAIL tuỳ chọn: OpenEXR, three.js, tifffile/pyshp, k2v node_modules, Freesound); đọc CLAUDE.md, BAI-HOC-LL, K1176-BAO-CAO, ANIMATIC-T4-BAO-CAO §9, PHIEU-XEM C11/C13/C14 | xong |
| 02:34 | hook pre-commit + pre-push (tools/preflight.sh) cài trước lần đẩy đầu; `lock.py --verify` KHỚP 513c9442 | xong |
| 02:35 | checks-appeal.md: A1–A5 + C11 + C13 + ghi chú C14 chép nguyên văn — TRƯỚC khi phán (commit 839d4b52) | xong |
| 02:36–02:50 | Đọc mã k2check, q_k1174 (MAY-19, GOC-CAO-60), q_k1176 (TU-LIEU), q_k116 (TL-1), q_lai (K-LAI-1), q_nhip (Q37 a), q_n2p (tam), q_thoi_dai; tái hiện A2: diem_neo khai [E,N,h] bị đọc như toạ độ cảnh + (c) chỉ so khung CUỐI shot tham chiếu → H5-07b 51 704 px (neo đổi đúng: khung đầu M03 0 px, khung cuối 36 px); H2-12 0,08 px "đạt giả" (neo đúng: 51,9 px với đầu/cuối H1-03, 0,128 px với khung 202 giữa shot) | xong (số đo) |
| 02:45 | A4: Q37 (a) so beats khai với mốc ĐẶC TẢ (spec_times), không với biến cố đo — 12 lớp chồng không có trong đặc tả (p.*) → khuôn `p.lop_chong`; A5: n2p.tam khai ở log shot thay vì episode.yaml | xong (chẩn đoán) |
| 02:48 | Mô hình dò mặt YuNet 2023mar (HF opencv/face_detection_yunet, MIT, SHA 8f2383e4…) tải về /var/tmp/k1177/dl | xong |
| 02:50–02:58 | q_thoi_dai lớp công trình mốc (đề bài o2-v3-moc, chỉ khi bật); hiệu chuẩn 9 lần gọi claude-sonnet-5-5 ($0,30): H2-13 v1 k25/k55/k90 **bắt 3/3** (tin 0,8), 3 khung đúng (1935, 1940, 1666 sau cháy) **0/3 báo**; lớp chung không danh sách: H2-13 bắt (0,6), 2 khung đúng 0 báo | xong |
| 03:00 | WIP `reports/k1177/wip/checks-wip.patch` + kết quả `do/moc/`; đẩy | xong |

## Lệnh bổ sung đã áp
- (chưa có)
