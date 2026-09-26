# CINE LAB — KHẢO SÁT CÔNG CỤ SINH VIDEO BÊN THỨ BA (26/09/2026)

Phạm vi: phục vụ câu hỏi 3(b) trong CINE-LAB-HANDOFF.md. Mọi số liệu tra ngày 26/09/2026; ưu tiên trang chính thức, nguồn tổng hợp ghi rõ "(thứ cấp)". Chưa gọi thử API nào — mọi nhận định chất lượng hình chưa được kiểm chứng.

## 1. Kết luận nhanh

- **Sora (OpenAI) bị loại:** app ngừng 26/04/2026, API ngừng 24/09/2026 (trang trợ giúp OpenAI).
- **Ứng viên chính: Google Veo 3.1 qua Vertex AI** — có bảng giá chính thức, có bồi thường bản quyền (indemnity) cho bản GA trên Vertex AI API, Gemini API mở cho Việt Nam.
- **Ứng viên phụ: Runway API** — một khoá gọi được nhiều model (Gen-4.5, Veo 3.1, Seedance 2, Wan 3); điều khoản cho phép dùng thương mại, không bắt buộc ghi công.
- **Thận trọng:** Seedance 2.0 (ByteDance) — Disney, MPA, Netflix gửi cảnh cáo pháp lý 02/2026; Kling — điều khoản chỉ đọc được qua nguồn thứ cấp.

## 2. Bảng giá (USD/giây video đầu ra)

### Veo trên Vertex AI (trang giá chính thức Google Cloud)

| Model | 720p | 1080p | 4K | Ghi chú |
|---|---|---|---|---|
| Veo 3.1 — chỉ hình | 0,20 | 0,20 | 0,40 | |
| Veo 3.1 — hình + tiếng | 0,40 | 0,40 | 0,60 | |
| Veo 3.1 Fast — chỉ hình | 0,08 | 0,10 | 0,25 | |
| Veo 3.1 Fast — hình + tiếng | 0,10 | 0,12 | 0,30 | |
| Veo 3.1 Lite — chỉ hình | 0,03 | 0,05 | — | |
| Veo 3.1 Lite — hình + tiếng | 0,05 | 0,08 | — | |

Cùng trang: Imagen 4 $0,04/ảnh, Imagen 4 Ultra $0,06/ảnh; Lyria 3 (nhạc 30 s) $0,04, Lyria 3 Pro (nguyên bài) $0,08.

### Runway API (tài liệu API chính thức; 1 credit = $0,01)

| Model | credit/giây | ≈ USD/giây |
|---|---|---|
| gen4.5 | 12 | 0,12 |
| gen4_turbo | 5 | 0,05 |
| veo3.1 (có tiếng) | 40 | 0,40 |
| veo3.1_fast (có tiếng) | 15 | 0,15 |
| seedance2 720p / 1080p | 36 / 40 | 0,36 / 0,40 |
| wan3 720p / 1080p | 10 / 20 | 0,10 / 0,20 |
| act_two (diễn xuất theo video mẫu) | 5 | 0,05 |

### Nhà khác (thứ cấp, buildmvpfast, 07/2026)

Kling 3.0 ≈ $0,10/s; Seedance 2.0 ≈ $0,092/s; Luma Ray 3 ≈ $0,21/s; Hailuo 02 ≈ $0,045/s; Wan 2.6 ≈ $0,05/s. Chưa đối chiếu trang chính thức.

## 3. Thông số kỹ thuật Veo 3.1 (tài liệu Gemini API)

- Độ dài clip 4/6/8 s; 24 fps; 720p mặc định, 1080p và 4K chỉ với clip 8 s.
- Tỷ lệ khung: chỉ 16:9 và 9:16 → 2.39:1 phải cắt từ 16:9 (mất ~26% chiều cao).
- Tối đa 3 ảnh tham chiếu (giữ nhân vật/phong cách); nội suy khung đầu–khung cuối.
- Nối dài: +7 s/lần, tối đa 20 lần (148 s) nhưng **chỉ 720p**.
- Tiếng sinh kèm luôn bật; **chỉ tiếng Anh được đánh giá đầy đủ** → lời Việt phải làm riêng.
- File lưu trên máy chủ 2 ngày → phải tải về ngay.
- Có watermark SynthID (vô hình). Độ trễ 11 s – 6 phút/clip.

## 4. Giấy phép và pháp lý

| Nhà cung cấp | Quyền sở hữu / thương mại | Bồi thường bản quyền | Rủi ro |
|---|---|---|---|
| Google Veo (Vertex AI) | Dùng thương mại được | Có — Veo bản GA qua Vertex AI API nằm trong danh mục indemnified | Chỉ áp cho Vertex AI, bản GA; cần kiểm lại khi dùng Gemini Developer API |
| Runway | "Nội dung là của bạn", không hạn chế thương mại, không bắt buộc ghi công | Không thấy cam kết | Model bên thứ ba qua Runway (Seedance…) mang rủi ro của model gốc |
| Kling (thứ cấp) | Gói trả phí mới được dùng thương mại; gói miễn phí có watermark | Không thấy | Nguồn thứ cấp nói phải hiển thị thương hiệu Kling và Kling được cấp phép vĩnh viễn dùng nội dung |
| Seedance 2.0 | — | — | Tranh chấp bản quyền với Hollywood 02/2026 |

Nền tảng phát hành (YouTube): phải bật nhãn "nội dung thay đổi/tổng hợp" khi cảnh chân thực có thể bị nhầm là thật; phim hoạt hình/huyễn tưởng rõ ràng, giọng AI cho kịch bản thì miễn. Không khai báo có thể bị gắn nhãn cưỡng chế, gỡ video hoặc đình chỉ YPP (nguồn thứ cấp tóm trang hỗ trợ YouTube).

## 5. Ước tính chi phí hình cho phim 90 giây (tỷ lệ quay 3:1 → sinh 270 s)

| Phương án | Đơn giá | Chi phí hình |
|---|---|---|
| Veo 3.1 Lite 1080p, chỉ hình | 0,05 | ≈ $14 |
| Veo 3.1 Fast 1080p, chỉ hình | 0,10 | ≈ $27 |
| Runway Gen-4.5 | 0,12 | ≈ $32 |
| Veo 3.1 1080p, chỉ hình | 0,20 | ≈ $54 |
| Veo 3.1 4K, chỉ hình | 0,40 | ≈ $108 |

Chưa gồm phí phiên Claude Code (bài B–C: $10–15 cho 2–6 phút phim dựng bằng mã). Tỷ lệ quay 3:1 là giả định; cần đo thật ở bài thử.

## 6. Việc cần để phiên cloud gọi được API

- Tạo Google Cloud project + bật Vertex AI + billing (hoặc khoá Gemini API).
- Thêm tên miền vào mạng môi trường: `aiplatform.googleapis.com`, `generativelanguage.googleapis.com`, `storage.googleapis.com` (nếu trả file qua GCS); Runway: `api.dev.runwayml.com`.
- Gắn khoá qua mục API credentials như đã làm với OpenAI.

## 7. Đo thật: phương án "chỉ Opus" dựng hình chân thực bằng Blender (26/09/2026)

- Cài `bpy` (Blender 5.0.1) bằng pip trong container cloud: thành công. Máy: 2 CPU, 7 GB RAM, không GPU.
- Cảnh thử: bầu trời vật lý, sàn phản chiếu, 7 khối, DOF f/2; Cycles CPU, 1920×1080, 64 mẫu + khử nhiễu, AgX.
- **Thời gian: 192,7 s cho một khung.** Phim 90 s × 24 fps = 2.160 khung ≈ 116 giờ render. Không khả thi trên container này.
- Ánh sáng và vật liệu đạt độ chân thực vật lý, nhưng **người chân thực thì không dựng được bằng mã** (cần mô hình, rig, da, tóc, diễn xuất).
- Kết luận: "truyện hư cấu chân thực" mà chỉ dùng Opus là không khả thi. Opus vẫn giữ vai đạo diễn/biên kịch/dựng/kiểm; điểm ảnh chân thực phải lấy từ công cụ sinh video.

## Nguồn

- OpenAI — Sora discontinuation: https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation
- Google Cloud — Vertex AI pricing: https://cloud.google.com/vertex-ai/generative-ai/pricing
- Google — Veo trên Gemini API: https://ai.google.dev/gemini-api/docs/veo
- Google — Gemini API available regions: https://ai.google.dev/gemini-api/docs/available-regions
- Google Cloud — Generative AI indemnified services: https://cloud.google.com/terms/generative-ai-indemnified-services
- Runway — API pricing: https://docs.dev.runwayml.com/guides/pricing/
- Runway — Usage rights: https://help.runwayml.com/hc/en-us/articles/18927776141715-Usage-rights
- buildmvpfast — AI video API pricing (thứ cấp): https://www.buildmvpfast.com/api-costs/ai-video
- Global GPT — Kling commercial use (thứ cấp): https://www.glbgpt.com/hub/can-i-use-kling-ai-for-commercial-use/
- CNBC — ByteDance/Seedance: https://www.cnbc.com/2026/02/16/bytedance-safegaurds-seedance-ai-copyright-disney-mpa-netflix-paramount-sony-universal.html
- Minimatters — YouTube synthetic disclosure (thứ cấp): https://minimatters.com/youtube-altered-or-synthetic-content-disclosure/
