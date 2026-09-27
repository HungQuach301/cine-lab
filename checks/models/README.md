# Mô hình ghim cho luật P0 (máy dò chữ độc lập)

| File | Nguồn | Giấy phép | SHA-256 |
|---|---|---|---|
| `ch_PP-OCRv4_det_infer.onnx` | PaddleOCR PP-OCRv4 det (DB), bản ONNX đóng gói trong `rapidocr_onnxruntime==1.4.4` (PyPI) | Apache-2.0 | `d2a7720d45a54257208b1e13e36a8479894cb74155a5efe29462512d42f49da9` |
| `ch_PP-OCRv4_rec_infer.onnx` | PaddleOCR PP-OCRv4 rec, cùng gói; bảng ký tự nằm trong metadata `character` của file | Apache-2.0 | `48fc40f24f6d2a207a2b1091d3437eb3cc3eb6b676dc3ef9c37384005483683b` |

- Chạy bằng `onnxruntime` (CPU) có sẵn trong `/opt/cine`. Không cần mạng khi chạy.
- Đây là công cụ kiểm, không phải tài sản của phim; không đưa vào sản phẩm phát hành.
- Đổi mô hình = đổi luật: chỉ phiên K, chạy lại selftest, khoá lại SHA.
