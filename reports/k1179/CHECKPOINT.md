# CHECKPOINT — phiên K-1.17.9 (nhánh thật `ccr-196e0bda-gcj9iw` — harness buộc; lệnh ghi `checks-1-17-9`; gốc origin/main @41de7ce3, LOCK 1.17.8 045b7bb7…)

Giờ UTC theo đồng hồ container.

## Trạng thái
| Giờ UTC | Việc | Trạng thái |
|---|---|---|
| 03:12 | verify.sh (10 PASS, 5 FAIL tuỳ chọn không dùng ở K: OpenEXR, three.js, tifffile/pyshp, k2v node_modules, Freesound); origin/main = 41de7ce3 ✓, LOCK 1.17.8 045b7bb7 ✓; đầu vào A @bc1693b5 ✓ | xong |
| 03:13 | hook pre-commit + pre-push (tools/preflight.sh) cài trước lần đẩy đầu | xong |
| 03:13 | đầu vào: `git archive bc1693b5 reports/ban-cuoi-t4-a channel-k2/k2c-t4-02 \| tar -x -C /var/tmp/k1179/in` (590 MB; tái tạo được từ git — không giữ riêng ở /var/tmp) | xong |
| 03:20 | checks-appeal.md: khiếu nại KN-1…KN-7 (nguyên văn) + KN-8 (lệnh) — TRƯỚC khi phán | xong |

## Lệnh bổ sung đã áp
- (chưa có)
| 03:22–03:40 | Lượt chuẩn 1.17.8 (worktree `/var/tmp/k1179/wt178` @41de7ce3, LOCK KHỚP): bộ đệm mô hình nhìn tái tạo từ raw.txt trong git (0 API) → 8 tấm E **trùng bảng phiên A** ở N2P-1…4, N2P-E (N2P-5: video đối chứng ngoài git → không đo, cả hai phiên bản như nhau) | xong |
| 03:25–03:40 | Số đo: YuNet H1-15b/H3-05b (`do/yunet-*.json`), KN-2 Q37 + biến cố log máy (`do/kn2-q37-log.json`), KN-8 ghép thử bo8 + bo_dat (`do/ghep_kn8.py`, T9c `do/kn8-t9c.json`) | xong |
| 03:30–03:45 | Mã 1.17.9 (chưa khoá, bản vá WIP `wip/`): q_k1179 mới; q_n2p, q_k1178, q_k1177, q_nhip, q_k2var, k2check, cap112, VERSION | đang làm |
| 03:37–03:41 | Lượt 1.17.9 (mã chưa khoá) trên 8 tấm E + 8 tấm ghép KN-8 + đặc tả v4; mô hình nhìn KN-8 lượt 1 (2 tấm bo_dat; GPT báo "sông bảo vệ đổi" vì đề bài E coi sông là phần bảo vệ) → đề bài biến thể `n2p-e-v2-nuoc` | xong |
| 03:45 | selftest_k1179 49/49 (fixture thật 2,2 MB `checks/ll/fixtures/k1179/`, nguồn+SHA `NGUON.json`) | xong |
| 03:46– | Mô hình nhìn KN-8 lượt 2 (đề bài nuoc): 2 tấm bo_dat + 2 ca âm (cầu thứ hai, thuyền thêm) · selftest toàn bộ trước khoá | đang chạy (PGID 6627, 6684) |
| 03:47–03:52 | selftest toàn bộ trước khoá 18/18 bộ ĐẠT (`do/selftest-truoc-khoa.txt`); KN-6 thước tốc độ đổi sang hệ số góc (1,5 %/s đo 1,505) + sai số 2 %; k1179 50/50 | xong |
| 03:51 | T3: master LFS `release-k2-t3-g2` SHA `5b9f0bcc…` khớp; timeline `0ff3f0da…`, log chữ `17053dff…` khớp; k2check 1.17.8 T3 (worktree) chạy nền | đang chạy |
| 03:53 | checks-appeal.md: phán quyết 1.17.9 | xong |
| 03:54 | preflight `checks/` bắt 1 email giả trong selftest (dựng lúc chạy) → ĐẠT; **lock.py (một lần) 03:54:51 → 1.17.9 `9eddaf24…`, --verify KHỚP** | xong |
| 03:55–04:05 | Sau khoá: selftest 18/18 bộ ĐẠT (`do/selftest-sau-khoa.txt`); T3 1.17.8 (worktree) **trùng hệt** bảng K-1.17.8 trừ tiêu đề | xong |
| 04:05– | cinecheck L1 selftest; rồi T3 1.17.9; chuỗi E/KN-1/KN-8/đặc tả v4 sau khoá (P ≤ 2) | đang chạy |
| 04:17–04:20 | Sau khoá: 8 tấm E 0 hàng đổi; KN-1 khai thử; ghép KN-8 (+ bộ đệm mô hình); đặc tả v4 1.17.8 (tái chạy = bảng A) ↔ 1.17.9: 5 hàng; bảng ở `do/k2/` | xong |
