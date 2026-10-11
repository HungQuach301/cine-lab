# P-G3 — chuẩn bị phát hành sau G2 (dán: "Chạy playbook/prompts/P-G3.md cho tập NN")

1. Áp sửa nhỏ G2 (nếu có): chỉ render lại đoạn đổi (`ONLY="…"`), ghép lại, qc lại, cập nhật nhánh `release-ll-epNN-v1` + `SHA256SUMS.txt`, tải ngược kiểm SHA.
2. `reports/m3/HUONG-DAN-DANG-TAPN.md` theo khung tập 2 (tiêu đề chủ dự án chọn trong 3 phương án, mô tả, **thumbnail: chủ dự án tạo 2–3 bản theo PACKAGING-BRIEF và bật Test & Compare khi đăng; nếu chủ dự án gửi ảnh cho P thì P đọc kiểm claim + vùng an toàn và ghi vào hướng dẫn (không chặn, không chờ); CTR bản thắng vào `epNN/KHAN-GIA.md`**, **giờ đăng: mặc định kênh + gợi ý hồ sơ cầu** (§14 bước 6), lịch đọc số 48 giờ/7 ngày/28 ngày, chương, Shorts, phụ đề, **Altered content = No**, giấy phép nhạc).
3. Xoá trung gian (`/var/tmp/cine-out/ll-epNN`, giữ master/Shorts đối chiếu nếu cần). Ghi AUTHORSHIP.
4. Chủ dự án tự đăng theo hướng dẫn; P không dừng chờ, sang tập kế. Sau 48 giờ/7 ngày: điền `KHAN-GIA.md` từ ảnh YouTube Studio; `market.py own --pack ll --session ll` cập nhật `reports/m3/KHAN-GIA-SO.md` (dự đoán G1 vs thật; Việc 0 tập kế cũng tự chạy).
