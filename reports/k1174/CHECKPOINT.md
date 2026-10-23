# CHECKPOINT — phiên K-1.17.4 (nhánh `checks-1-17-4`, gốc origin/main @c6a4772b, LOCK 1.17.3 d99af8f2…)

## Trạng thái
| Giờ UTC | Việc | Trạng thái |
|---|---|---|
| 15:40 | Đọc Kinh thánh §13.6, §14.2, §15, §17, §19; K1173 báo cáo + QUYET-DINH-TREO; K117 §2, §6, §10 (D8); K116-D4; TIEN-KY-T4 §6, TO-SO T6, PHIEU-G1 D11, DE-XUAT-BIBLE-19; `reports/tien-ky-t4/kiem/**` | xong |
| 15:50 | Nhánh `checks-1-17-4` từ origin/main @c6a4772b; hook pre-commit + pre-push (tools/preflight.sh) cài trước lần đẩy đầu | xong |
| 15:56 | D11 tái hiện: ghép lại T6 l1/l2/l3 từ đầu vào gốc trong git bằng `t6_ghep.py` (không sửa) → **SHA ghép trùng sổ kiểm** (l1b, l2, l3); T9b nước→đất l2 = **2,42 %** (trùng). Dải 'biển' chân trời: **0 điểm** ở tử số l2; bỏ dải (vùng hợp lệ) → **2,67 %**; render thô → 2,67 %. Nguồn: bờ bắc 1,49 % + giữa nước 0,93 % (phản chiếu/nhạt màu). Nghiêng **LỖI ẢNH** — `do/d11-t6-iii.json`, `do/d11_tai_hien.py` | xong (số đo) |
| — | K117-D8 thước biến cố trên video; K1173-D6; Q2; §19 | đang làm |

## Lệnh bổ sung đã áp
- Môi trường: `/opt/cine` thiếu gói (verify.sh 7 FAIL) → cài lại gói Python của setup.sh bước 2 vào `/opt/cine` (không sửa repo).
- Harness gợi ý nhánh `ccr-db327794-xgq2sr`; đẩy theo lệnh lên `checks-1-17-4` (như K-1.17.3).
