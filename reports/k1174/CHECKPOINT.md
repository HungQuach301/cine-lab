# CHECKPOINT — phiên K-1.17.4 (nhánh `checks-1-17-4`, gốc origin/main @c6a4772b, LOCK 1.17.3 d99af8f2…)

## Trạng thái
| Giờ UTC | Việc | Trạng thái |
|---|---|---|
| 15:40 | Đọc Kinh thánh §13.6, §14.2, §15, §17, §19; K1173 báo cáo + QUYET-DINH-TREO; K117 §2, §6, §10 (D8); K116-D4; TIEN-KY-T4 §6, TO-SO T6, PHIEU-G1 D11, DE-XUAT-BIBLE-19; `reports/tien-ky-t4/kiem/**` | xong |
| 15:50 | Nhánh `checks-1-17-4` từ origin/main @c6a4772b; hook pre-commit + pre-push (tools/preflight.sh) cài trước lần đẩy đầu | xong |
| — | D11 tái hiện phép (iii) trên đầu vào gốc T6 (`channel-k2/k2c-t4-02/ai/goc/`) | đang làm |

## Lệnh bổ sung đã áp
- Môi trường: `/opt/cine` thiếu gói (verify.sh 7 FAIL) → cài lại gói Python của setup.sh bước 2 vào `/opt/cine` (không sửa repo).
- Harness gợi ý nhánh `ccr-db327794-xgq2sr`; đẩy theo lệnh lên `checks-1-17-4` (như K-1.17.3).
