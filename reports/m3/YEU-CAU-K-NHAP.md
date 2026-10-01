# Yêu cầu gửi phiên K — BẢN NHÁP, CHƯA GỬI (P soạn 01/10/2026)

Căn cứ: AUTHORSHIP 01/10/2026, "P soạn sẵn yêu cầu gửi K (C3 cho nhân vật dạng bóng; profile luật Shorts 9:16), chưa gửi". Kênh Last Lamplighters, tập thử Mốc 2 (`reports/m3/KE-HOACH-TAP-THU.md` §7).
P không đọc mã `checks/`. Mọi mô tả dưới đây dựa trên `checks/RUN.md` và báo cáo luật đã chạy. Khi chủ dự án cho phép, P chuyển nguyên văn mục 1–2 vào `checks-appeal.md`.

## 1. C3 cho nhân vật dạng bóng (silhouette)
**Hiện trạng**
- C3 so tỉ lệ bộ phận (đầu, thân, cánh tay trên, cẳng tay, đùi, ống chân) với model sheet `ida.json` / `cas.json`, đo trên mặt nạ bộ phận.
- Phong cách B3 của kênh mới biến Ida (và Cas) thành **bóng đặc, chỉ một viền sáng mảnh**, không có mặt.
- Lưới, rig và diễn hoạt giữ nguyên Last Round, nên mặt nạ bộ phận vẫn xuất được. Nhưng trên hình, ranh giới giữa các bộ phận trong bóng không thấy được.

**Câu hỏi cho K**
1. Với nhân vật bóng, C3 đo trên mặt nạ hình học (vẫn xuất được) có còn đúng nghĩa không? Hay cần đổi chỉ tiêu sang **đường viền ngoài**: tỉ lệ cao/rộng của bóng, tỉ lệ đầu/thân theo đường viền, độ khớp mép bóng với mặt nạ?
2. Có cần một model sheet riêng cho dạng bóng không, ví dụ `ida-bong.json`: đường viền chuẩn ở 4 góc, tỉ lệ đầu–mũ–thân? Nếu cần, ai lập và khoá: chủ dự án duyệt, K khoá SHA?
3. Viền sáng 1–2 px có ảnh hưởng tới phép đo "độ khớp biên mặt nạ–cạnh ảnh render" (hiện trượt ở mức 0,79–1,0, ngưỡng ≥ 1,5) không?

**P đề xuất** (K quyết): giữ C3 trên mặt nạ hình học để chặn lỗi rig (kéo, lún), và thêm chỉ tiêu đường viền cho dạng bóng. Không hạ ngưỡng.

## 2. Profile luật cho Shorts 9:16
**Hiện trạng:** `run.py --profile shot|youtube|archive`. Profile `youtube` kiểm N3 khung 16:9 và SAR 1:1, M1 −14 LUFS ±1, true peak ≤ −1 dBTP.

**Nhu cầu:** Shorts 1080×1920, 24 fps, < 60 s, có chữ trên màn hình và phụ đề cháy (`KE-HOACH-TAP-THU.md` §6).

**Câu hỏi cho K**
1. Thêm profile `shorts`, với các điểm khác profile youtube:
   - N3: khung 9:16, 1080×1920, SAR 1:1; codec và bitrate theo khuyến nghị YouTube Shorts;
   - thời lượng < 60 s (luật mới hoặc thuộc N3);
   - M1: giữ −14 LUFS?
   - P0/P1/G4: vùng an toàn chữ cho giao diện Shorts (lề trên, dưới, phải bị nút che). Có cần luật vùng an toàn mới không?
2. Shorts cắt từ master 16:9: C3 và H1b chạy trên bản cắt hay chỉ trên master?

**Cách gửi khi được phép:** P ghi mục 1–2 vào `checks-appeal.md` (mục "Yêu cầu mới, 2026-10"), chờ K phán quyết và khoá bản checks mới. Trong lúc chờ, M2 chạy luật bằng profile youtube cho master.
