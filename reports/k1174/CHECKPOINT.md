# CHECKPOINT — phiên K-1.17.4 (nhánh `checks-1-17-4`, gốc origin/main @c6a4772b, LOCK 1.17.3 d99af8f2…)

## Trạng thái
| Giờ UTC | Việc | Trạng thái |
|---|---|---|
| 15:40 | Đọc Kinh thánh §13.6, §14.2, §15, §17, §19; K1173 báo cáo + QUYET-DINH-TREO; K117 §2, §6, §10 (D8); K116-D4; TIEN-KY-T4 §6, TO-SO T6, PHIEU-G1 D11, DE-XUAT-BIBLE-19; `reports/tien-ky-t4/kiem/**` | xong |
| 15:50 | Nhánh `checks-1-17-4` từ origin/main @c6a4772b; hook pre-commit + pre-push (tools/preflight.sh) cài trước lần đẩy đầu | xong |
| 15:56 | D11 tái hiện: ghép lại T6 l1/l2/l3 từ đầu vào gốc trong git bằng `t6_ghep.py` (không sửa) → **SHA ghép trùng sổ kiểm** (l1b, l2, l3); T9b nước→đất l2 = **2,42 %** (trùng). Dải 'biển' chân trời: **0 điểm** ở tử số l2; bỏ dải (vùng hợp lệ) → **2,67 %**; render thô → 2,67 %. Nguồn: bờ bắc 1,49 % + giữa nước 0,93 % (phản chiếu/nhạt màu). Nghiêng **LỖI ẢNH** — `do/d11-t6-iii.json`, `do/d11_tai_hien.py` | xong (số đo) |
| 16:05 | Master T3 tải (UA CineLab-research; SHA 5b9f0bcc… khớp). k2check 1.17.3 trên T3 chạy từ worktree thưa origin/main (LOCK KHỚP). `checks/ll/q_bcv.py` (thước biến cố video, chưa khoá) + `do/hieu_chuan_bcv.py`; thử 60 s đầu: bắt cắt góc 4,5/9,58 s, ranh shot, bước năm H2 trùng beat | xong |
| 16:24 | k2check 1.17.3 trên T3 (worktree thưa origin/main, master đường tuyệt đối) **trùng hệt** bảng K-1.17.3 (11 m 49 s) → `do/k2check-1.17.3-t3.md`. Mã 1.17.4 (chưa khoá, bản vá WIP): q_bcv (thước sửa: neo ≤ 3 s, mờ σ 1,5), q_k1174 (MAY-19, BAN-DO-12, TU-LIEU-10, AI-TU-LIEU, GEMINI-NGAN-SACH, GOC-CAO-60), D6 (q37_mien thẻ PP), Q2 (MINH-HOA/N2P-6), k2check + cap112, RULES-LL 1.17.4, VERSION 1.17.4; `checks-appeal.md` phán quyết D11 = LỖI ẢNH. Selftest cũ k112…k2 đạt (k117: 1 kỳ vọng đổi có căn cứ Q2); selftest_k1174 89/91 (2 ca thước tổng hợp chờ ngưỡng hiệu chuẩn). Thử T4 (BANG-SHOT-v1 + sổ Gemini) → `do/thu-t4-bang-shot.txt` | xong |
| 16:51 | Hiệu chuẩn lượt 1 (σ khung 1): mọi cấu hình R cắt 100 %, R beat 87–98 %, Δt TV 0,04–0,07 s, 0 báo nhầm ở quãng tĩnh theo ô — nhưng clip chỉ máy đi báo nhầm 14–201/60 s → KHÔNG đạt. Sửa: (1) clip tổng hợp cắt giữa (bỏ biên phản chiếu), (2) quãng tĩnh = tĩnh theo ô (23/25 quãng tĩnh Q37 1.13 có ô đổi tới 52/255), (3) mờ khung σ 2 (răng cưa khi phóng/quay) | xong |
| 17:00 | Hiệu chuẩn lượt 2 (σ khung 2, neo 3 s) — dừng giữa chừng (theo PID): selftest tổng hợp cho thấy đếm trùng ở ô kề | bỏ |
| 17:16 | Thước: ô đổi → neo lại cả 8 ô kề (một vật = một biến cố); selftest_k1174 91/91 (θ 8 và 10). Hiệu chuẩn lượt 3 (thuật toán cuối) | xong |
| 17:35 | Hiệu chuẩn lượt 3 **ĐẠT**: θ 8, k 2 (chọn nửa đầu, kiểm nửa sau đạt) — R cắt 100/100 %, R beat 90,8/98,2 %, Δt TV 0,05/0,04 s, 0 báo nhầm (tĩnh theo ô + chỉ máy đi), bắt 6/6 → `do/hieu-chuan-bcv.json`; `q_bcv.HIEU_CHUAN` ghi hằng số; selftest_k1174 91/91 | xong |
| 17:48 | k2check 1.17.4 (chưa khoá) trên T3 (12 m 6 s): chỉ đổi Q37/NHIP-K2/Q37 (1.13) (c) 9,0 s PP1 → miễn (lộ 8,03 s N5_5), + BIEN-CO-V (TRƯỢT (c) 19,62 s từ 1:02,6), + hàng 1.17.4 (T4) KHÔNG ÁP → `do/k2check-1.17.4-t3-truoc-khoa.md`. Thử lưới mịn 16×9: không cứu vật nhỏ ở mọi θ không báo nhầm → giữ 8×6 | xong |
| 17:49 | `lock.py` (không `--verify`, MỘT lần) → **1.17.4 `08486eb2…`**; `--verify` KHỚP; selftest_k1174 91/91 | xong |
| 18:00 | Trên cây đã khoá: selftest k112…k1174, k2, ll đạt hết (k1174 91/91); k2check 1.17.4 cuối trên T3 (10 m 12 s) trùng lượt trước khoá, LOCK 1.17.4 KHỚP; 51/54 hàng như 1.17.3 → `do/so-1173-1174.md` | xong |
| 18:05 | Báo cáo `K1174-BAO-CAO.md` (§0–§13), quyết định K1174-D1…D6 | xong — **DỪNG chờ chủ dự án** |

## Lệnh bổ sung đã áp
- 17:37: lần 2 lệnh dừng theo chuỗi (`grep "[k]2check-1174-truoc"`) khớp chính shell (exit 144) — chỉ lượt k2check vừa khởi động bị dừng; từ đây lấy PID bằng lệnh riêng.
- `pkill -f hieu_chuan_bcv.py` khớp chính lệnh shell (bài học LL #24/#41, lặp lại) → shell thoát 144; sửa bị bỏ đã chạy lại; từ đó dừng tiến trình theo PID.
- Mã `checks/` chưa khoá được đẩy dạng bản vá `reports/k1174/wip/checks-1174-wip.patch` (checks/ cất bằng stash khi commit vì hook kiểm LOCK), như K-1.17.3.
- Môi trường: `/opt/cine` thiếu gói (verify.sh 7 FAIL) → cài lại gói Python của setup.sh bước 2 vào `/opt/cine` (không sửa repo).
- Harness gợi ý nhánh `ccr-db327794-xgq2sr`; đẩy theo lệnh lên `checks-1-17-4` (như K-1.17.3).
