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
