Nhánh thật: `ccr-3194130e-kijmlg` (harness buộc tên này; lệnh đặt `checks-1-16`). Gốc `origin/main` @ `8cedb8af`.

# K-1.16 — CHECKPOINT (việc dở)

| Giờ UTC | Trạng thái |
|---|---|
| 09:58 | Bắt đầu. LOCK gốc 1.15.0 `f4fa0349…df80d40` **KHỚP**. Hook preflight pre-commit + pre-push đã cài. Đã đọc Kinh thánh §10–§13, hai tệp khiếu nại, G1B §1.7/§2, P-1910, K-1.15. |
| 10:55 | Golden lượt A (trình dựng hiện hành, trước chụp lại) trùng P-1910: steel 0,9449 KHỚP · ll08 0,9307 KHỚP · t1 0,9082 LỆCH CỤC BỘ 22/144 (ô lệch = dòng nguồn đáy 38 px hai dòng + bóng V6). Timeline T3 sinh lại từ đặc tả G1b (prep, mạng chặn): 726,17 s. Mã 1.16 đang viết: `q_k116.py` (SACH-1, CHUONG-1, PP-1, TL-1/2/3, NHIP-NGHIA, XEM-CAM, PC-1, K-LAI-2/NC-H5/BD-3 1.16), cờ v116 ở Q26b/Q37/A*/K-LAI; thước cắt video hiệu chuẩn trên animatic T3. Bản vá: `reports/k116/wip/checks-wip.patch`. Chưa selftest. |

Quy ước checkpoint: mã `checks/` đang sửa được cất tạm (bản sao ngoài repo) khi commit checkpoint để `lock.py --verify` trong preflight vẫn KHỚP; bản vá việc dở nằm ở `reports/k116/wip/`. LOCK chỉ nâng một lần ở cuối.
