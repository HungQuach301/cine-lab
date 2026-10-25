# CHECKPOINT — phiên K-1.17.8 (nhánh thật `claude/k1178-t4-london-rules-pdjfmz` — harness buộc; lệnh ghi `checks-1-17-8`; gốc origin/claude/k1177-animatic-checks-nfbsbr @1277400a, LOCK 1.17.7 3a53574c…)

Giờ UTC theo đồng hồ container.

## Trạng thái
| Giờ UTC | Việc | Trạng thái |
|---|---|---|
| 17:12–17:15 | verify.sh (10 PASS, 5 FAIL tuỳ chọn: OpenEXR, three.js, tifffile/pyshp, k2v node_modules, Freesound); đọc CLAUDE.md, BAI-HOC-LL, K1177-BAO-CAO, ANIMATIC-T4-V2-BAO-CAO §8 (@1a911a01), PHIEU-XEM-V2 C7; nhánh đặt về @1277400a | xong |
| 17:15 | hook pre-commit + pre-push (tools/preflight.sh) cài trước lần đẩy đầu; `lock.py --verify` KHỚP 3a53574c | xong |
| 17:20 | checks-appeal.md: khiếu nại ANIMATIC-T4-V2 §8 + C7 + dòng lỗi k2check + căn cứ LUẬT E chép nguyên văn — TRƯỚC khi phán (commit, đẩy 17:21) | xong |
| 17:20 | Video kiểm = nối 4 bản xem v2 (ffmpeg concat copy) → `/var/tmp/k1178/anim-v2-xem-noi.mp4` 770,897 s, 640×360, 18 501 khung, **SHA-256 `d4b5d486e9bcdb9c33b334ea0dc30c66ccc0056db6097dea3e4c8f4e2b94fbb2`** (tái tạo: `git archive 1a911a01 reports/animatic-t4-v2/xem` + concat 4 tệp theo thứ tự 1..4) | xong |
| 17:22–17:30 | Hiệu chuẩn BIEN-CO-V T4: tiêu chí đặt trước (docstring `do/hieu_chuan_bcv_t4.py`); định nghĩa tập thật (log máy) sửa 1 lần TRƯỚC khi đo biến cố (bản đầu 0 s tĩnh); lượt 1 lỗi khung +97 s vượt cuối phim → FR_T sửa, chạy lại 17:34 (PID 8014, P = 2) | đang chạy |
| 17:28–17:32 | Đáp án LUẬT E: mặt nạ E P9-2026 (render V2 @1a911a01) + 3 ảnh OpenAI gpt-image-2.5 (ngày / đêm / "xấu" có tháp bịa + biển quảng cáo) **$0,227**, vào git `do/e/ai/` | xong |
| 17:35–17:45 | Mã 1.17.8: q_k1178 (mới), q_n2p (E, bo_a, N2P-E), q_n2p_vision (đề bài riêng), q_k1175 (BMN bỏ tấm E), q_lai + q_k1177 (mức nen), q_types, q_k2var, k2check, cap112, q_k116 (SACH-1), q_nhip (Q37 d), q_k1176 (OMNI) | đang làm |
| 17:40–17:49 | Mô hình nhìn đề bài E v1 trên 6 tấm: Claude chỉ đọc 2–3/10 ảnh ở 6/6 tấm (cả lần gọi lại KN-3) → THIẾU; lỗi KeyError "qtd" khi bộ đệm rỗng (q_n2p + q_k1178, sửa); ≈ $0,56 | xong — sự cố |
| 17:50 | Đối chứng: đề bài N2P cũ, Claude đọc 10/10 → đề bài E v2 thêm câu buộc mở đủ 10 tệp (sửa tuân thủ đọc, không sửa phần phát hiện) | xong |
| 17:52– | Mô hình nhìn đề bài E v2 trên 6 tấm (Claude đọc 10/10) | đang chạy |
| 17:45–18:00 | Hiệu chuẩn BIEN-CO-V T4 xong: KHÔNG (θ, k) nào đạt (θ 8 k 2: tĩnh thật 9,9/phút nửa sau, chỉ máy thật 127,5/phút — thị sai TRUOT/XUONG, tổng hợp 5, vật đổi 5/6) → HIEU_CHUAN_T4 dat False; selftest_k1178 69/69 (chưa khoá) | xong |

## Lệnh bổ sung đã áp
- (không có lệnh bổ sung từ chủ dự án trong phiên)
- Ghi chú vận hành: mã `checks/` chưa khoá không commit được (preflight `lock.py --verify`) → bản vá WIP `reports/k1178/wip/checks-wip.patch` + tệp mới `wip/checks-moi.tgz`; đẩy bằng `reports/k1178/day.sh` (cất checks/ khi commit/đẩy).
- Chờ tiến trình nền theo PID ghi lúc khởi chạy (`setsid … & echo $!`), không `pgrep -f`.
