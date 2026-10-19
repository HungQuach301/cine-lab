Nhánh thật: `nc-v2v` (tách từ origin/main 3176ad1b). Không bị harness buộc nhánh khác.

# NC-V2V — Báo cáo: DỪNG ở bước 0 (khoá Gemini không hợp lệ)

## §0. Kết luận
- Bước 0 (lệnh nhẹ: liệt kê model) **thất bại**: Google trả `HTTP 400 INVALID_ARGUMENT`, `reason: API_KEY_INVALID`.
- Theo luật giao việc ("401/403/402/không có `gemini-omni-1.1-flash` → DỪNG"): mã 400 không nằm trong danh sách, nhưng ý nghĩa tương đương (khoá bị từ chối) và **không thể xác nhận có `gemini-omni-1.1-flash`** → DỪNG.
- **Chưa làm** bước 1–5 (clip nguồn, gọi Omni, đo, chấm mù, ước cả tập). Không tạo số đo giả, không thay bằng kết quả mô phỏng.
- Chi phí thật: Gemini $0 (2 lượt gọi đều bị từ chối trước khi tính tiền); OpenAI $0; ElevenLabs/YouTube/Runway 0; giờ máy CPU ≈ 0.

## §1. Bằng chứng (nguyên văn, đã che; khoá không bị đọc/in/ghi)
Thời điểm: 2026-10-19 16:33–16:34 UTC. User-Agent: `CineLab-research (+https://github.com/HungQuach301/cine-lab)`. Không gửi email hay dữ liệu nào khác.

| # | Lệnh | Kết quả |
|---|---|---|
| 1 | `GET https://generativelanguage.googleapis.com/v1beta/models?pageSize=1000` (không tự đặt header khoá; để proxy gắn) | `400 INVALID_ARGUMENT — API key not valid. Please pass a valid API key.` |
| 2 | `GET https://generativelanguage.googleapis.com/v1/models` | như trên, `details[0].reason = API_KEY_INVALID`, `domain = googleapis.com`, `metadata.service = generativelanguage.googleapis.com` |

(Một lượt thử phụ gửi header giữ chỗ `x-goog-api-key: PROXY_INJECTED` để xem proxy có thay giá trị không — cùng lỗi 400.)

Chẩn đoán: proxy **có** gắn một khoá (nếu không có khoá, Google trả 403 "unregistered callers", không phải `API_KEY_INVALID`). Trạng thái proxy (`/__agentproxy/status`) không ghi lỗi chuyển tiếp nào. Vậy khoá đang lưu trong cấu hình môi trường bị Google coi là không hợp lệ: gõ sai/thiếu ký tự, đã xoá/thu hồi, hoặc là khoá của dịch vụ khác (vd. khoá Vertex/OAuth, không phải khoá AI Studio dạng `AIza…`).

## §2. Việc chờ chủ dự án
1. Tạo/kiểm lại khoá Gemini API (AI Studio) có quyền gọi `gemini-omni-1.1-flash` và đã bật billing; cập nhật trong cài đặt môi trường `cine-lab-av` (menu môi trường trên thanh tiêu đề phiên → Edit → Network secrets / API credentials, host `generativelanguage.googleapis.com`). **Không dán khoá vào chat.** Phiên mới mới nhận khoá.
2. Mở phiên NC-V2V mới (cùng giao việc). Phiên đó chạy lại bước 0; nếu qua thì làm trọn bước 1–5. Nhánh `nc-v2v` đã có báo cáo này để nối tiếp.
3. (Tuỳ chọn) Nếu muốn, cho phép phiên làm trước phần **không cần Gemini** (dựng lại 4 clip nguồn + mặt nạ ID bằng máy V7B, bộ đo IoU/Canny/nhấp nháy/đường nối/luồng quang học chạy thử trên chính nguồn) trong khi chờ khoá. Phiên này không làm vì giao việc ghi rõ DỪNG ở bước 0.

## §3. Chỉ số ±5 % quanh ngưỡng
Không có (chưa đo gì).

## §4. Sổ AI (K-LAI)
| Model | Ngày | Đầu vào | Đầu ra | Giá |
|---|---|---|---|---|
| (liệt kê model, generativelanguage v1beta/v1) | 2026-10-19 | không tệp | lỗi 400, không có đầu ra | $0 |
