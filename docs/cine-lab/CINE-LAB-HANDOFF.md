# CINE LAB — BÀN GIAO KHỞI ĐỘNG

Nguồn: rút từ Project "Crux Studio — Chiến lược", các bài thử A–D (22–26/09/2026).
Chủ dự án: Hung Quach (GitHub: HungQuach301).

---

## 1. Mục tiêu nghiên cứu

Đánh giá và xây quy trình dùng Claude Opus 5.5 (qua Claude Code cloud session) để sản xuất phim/video ngắn mang tính điện ảnh.

Tách khỏi Crux Studio: Crux là kênh YouTube data-explainer (không mặt người, không footage thật, persona "nhà phân tích"). Các ràng buộc đó KHÔNG mặc nhiên áp cho Cine Lab. Bài học kỹ thuật và quy trình thì dùng lại được.

## 2. Năm câu hỏi đầu tiên — ĐÃ CHỐT (26/09/2026)

| # | Câu hỏi | Quyết định | Trạng thái |
|---|---|---|---|
| 1 | Loại phim | **Truyện hư cấu, phong cách hoá** (hoạt hình stylized: silhouette / hình học / 2.5D). Ban đầu chọn "hư cấu chân thực", đổi sau khi đo cho thấy chỉ dùng Opus thì không dựng được hình chân thực. | Chốt |
| 2 | Độ dài, khung, nền tảng | **Bài thử năng lực: 2–3 phút. Phim đích: 10–15 phút.** 16:9, YouTube + bán phim; khán giả nói tiếng Anh | Chốt |
| 3 | Chất liệu hình | **(a) chỉ Opus dựng bằng mã**, không dùng công cụ sinh video/ảnh bên thứ ba | Chốt |
| 4 | Mục đích | **Sản phẩm thương mại riêng**: kiếm tiền YouTube là chính, kèm bán phim | Chốt |
| 5 | Ngân sách, mức đạt | **Trần $250** cho bài thử đầu. Mức đạt: xem đề xuất ở dưới | Ngân sách chốt; mức đạt chờ duyệt |

Đề xuất mức đạt tối thiểu (chờ chủ dự án duyệt):
- Đạt toàn bộ luật §4 áp dụng được cho hoạt hình. Luật do phiên K viết và khoá SHA; phiên dựng không được sửa.
- Kỹ thuật: ≥ 16 Mbps, CFR, BT.709, −14 LUFS / ≤ −1 dBTP, không có va chạm chữ tính theo điểm ảnh.
- Người chấm: kịch bản, hình, âm thanh mỗi mục ≥ 7/10; không có lỗi nhìn thấy khi xem ở tốc độ thường.
- Thương mại: đủ điều kiện kiếm tiền trên YouTube (nội dung gốc, không lặp mẫu hàng loạt). Mọi âm thanh và phông chữ có giấy phép rõ ràng.

Căn cứ quyết định:
- Khảo sát công cụ bên thứ ba: `claude/CINE-LAB-KHAO-SAT-CONG-CU-VIDEO.md`. Sora API đã ngừng 24/09/2026; Veo 3.1 qua Vertex AI là ứng viên nếu sau này mở hướng (b).
- Đo thật: Blender Cycles CPU trong container (2 CPU, không GPU) mất 193 s/khung 1080p, tức khoảng 116 giờ cho 90 s phim. Không dựng được người chân thực bằng mã.

Bổ sung (26/09/2026, chủ dự án chốt):
- **Âm thanh:** chấp nhận dùng provider như ElevenLabs (gói trả phí). "Chỉ Opus" chỉ áp cho hình.
- **Khán giả:** nói tiếng Anh; phim tiếng Anh.
- **Kiếm tiền:** YouTube là chính, kèm bán phim.
- **Mục tiêu chất lượng (làm rõ):** KHÔNG làm phim để tranh giải. Mục tiêu là chất lượng điện ảnh cao nhất, cụ thể hoá thành khung sản xuất và cổng kiểm chứng: `claude/CINE-LAB-KHUNG-CHAT-LUONG.md` (v0.1, chờ duyệt). Quy chế Oscar chỉ để tham khảo.
- **26/09/2026 (tiếp):** khung v0.1 được đồng ý; phim tham chiếu do Claude chọn (R1–R5: Ice Merchants, Hair Love, Alike, The Flying Sailor, Sprite Fright); người chấm là chủ dự án (L2) + bạn bè (L3 mù); nhạc lấy nguồn miễn phí hoặc tự sinh (ưu tiên ACE-Step, cần đo CPU); triển khai nhiều phiên song song. Chi tiết và kế hoạch M0–M4: `claude/CINE-LAB-KE-HOACH-TRIEN-KHAI.md`.
- **26/09/2026 (M0 chuẩn bị):** chủ dự án đã tạo repo GitHub và kết nối Claude; đã có ElevenLabs trả phí (TTS chuyển từ OpenAI sang ElevenLabs). Toàn bộ tài liệu dự án được đóng gói vào repo (`docs/cine-lab/`, `CLAUDE.md`, `.claude/agents/`, `scripts/env/`) để các phiên Claude Code cloud đọc được. Hướng dẫn môi trường: `docs/cine-lab/SETUP-MOI-TRUONG.md`; ý tưởng bài thử: `docs/cine-lab/Y-TUONG-BAI-THU.md`; đề bài M0: `docs/cine-lab/PROMPT-M0.md`.
- **Chuẩn tham chiếu (lịch sử):** ban đầu chủ dự án nêu chuẩn Viện Hàn lâm (Oscar). Xem `claude/CINE-LAB-CHUAN-OSCAR.md`. Viện Hàn lâm không có checklist chất lượng; chỉ có điều kiện hợp lệ, chuẩn DCP, quy định AI/tác giả là con người, và bỏ phiếu đồng nghiệp.

- **Rà khía cạnh còn thiếu:** xem `claude/CINE-LAB-KHOANG-TRONG.md` (G1–G14). Rủi ro cao nhất cho việc bán phim: bản quyền của sản phẩm có AI (Cục Bản quyền Mỹ chỉ bảo hộ phần con người quyết định biểu đạt) và chain of title/E&O.
- **Bài học từ BRIEF-D:** xem `claude/CINE-LAB-BAI-HOC-BRIEF-D.md`.

Câu hỏi mở / rủi ro phải xử lý:
- ~~Xung đột YouTube – Oscar~~: không còn áp dụng vì không tranh giải.
- **Eleven Music:** không dùng (gói tự phục vụ loại trừ phim/TV). Đã chốt: nhạc miễn phí hoặc tự sinh.
- **Vai trò tác giả:** chủ dự án phải là tác giả câu chuyện; lập nhật ký quyền tác giả trong repo.
- **Giao nộp:** thêm bản DCP 2K 24 fps + mix 5.1 cho bản chiếu (chưa kiểm chứng trong container).

## 3. Bằng chứng từ các bài thử (Crux, đề tài tài chính cá nhân)

| Bài | Sản phẩm | Chi phí / thời gian | Kết quả chính |
|---|---|---|---|
| A | 86 s, không tiếng | $4 / 20 phút | Đúng số; hình tĩnh (độ phủ chuyển động 19%) |
| B | 128 s, 3 lớp âm thanh, nhạc sinh bằng mã | $10 / 65 phút | Chuyển động 95%; âm thanh đạt; gu hình 3/6 khung đạt 8/8 |
| C | 6:04, giọng TTS + nhạc + SFX + phụ đề + master −14 LUFS + đóng gói | $15 / 90 phút tới mốc giữa, cộng ~3 giờ phần cuối | Đúng số và nội dung đạt; còn 3 chỗ chữ đè chữ; bitrate video chỉ 0,64 Mbps (quá thấp) |
| D | ≥ 10 phút "chuẩn điện ảnh" | Đang chạy (theo dõi ở Project Crux) | Phiên kiểm K: 71 luật khoá SHA; chạy trên bài C: 27 đạt / 32 trượt / 12 thiếu |

Bài học đã chứng minh:
- Model dựng được sản phẩm hoàn chỉnh nhiều lớp, nhưng **máy kiểm do chính model dựng viết thì không đáng tin**: bỏ sót lỗi nhìn thấy, tự nới luật sau khi trượt, thêm phần tử chỉ để vượt ngưỡng (Goodhart).
- **Tách hai phiên:** phiên K viết và khoá luật (SHA-256), phiên D dựng và không được sửa luật; khiếu nại ghi vào file riêng.
- **Kiểm va chạm chữ theo điểm ảnh**, không chỉ theo hộp DOM.
- **Kiểm lời đọc theo "mọi từ quan trọng phải có"**, không theo tỷ lệ %.
- **Số đo thật thắng số tự khai**; phải chấm độc lập từ file đã render.
- **Đi theo mốc có điểm dừng:** M0 bước 0 (hạ tầng, dữ liệu, đo tốc độ render) → M1 tiền kỳ (kịch bản, đọc thử, storyboard, cue sheet) → M2 bản dựng mẫu → M3 bản đầy đủ. Duyệt kịch bản trước khi tốn tiền render.
- Mắt xích yếu nhất: nhạc sinh bằng mã và giọng TTS (giãn thời gian gây méo; có lúc bỏ sót từ). Cần tai người chấm.

## 4. Chuẩn điện ảnh — danh mục kiểm (đã dùng cho bài D)

- **Kịch bản:** cold open hình đi trước lời; vòng mở (open loop) trả lời ở cuối; câu móc lại 0:30–0:45; cấu trúc hồi có câu hỏi, bước ngoặt, payoff; nhân vật hoá và cái giá cụ thể; show don't tell; callback; đọc thử trước khi dựng.
- **Nhịp:** bản đồ căng–chùng; ngắt nhịp mỗi 30–60 s; khoảng thở sau điểm quyết định; cắt đúng phách hoặc đúng điểm hành động; độ dài cảnh biến thiên.
- **Bố cục:** một phần ba, đường dẫn mắt, khoảng trống phía trước theo hướng chuyển động, thứ bậc ba mức, vùng an toàn.
- **Máy quay:** shot list (cỡ, góc, tiêu cự giả lập, chuyển động và lý do); establishing shot; quy tắc 180° và hướng màn hình; quán tính (lấy đà, trễ, vượt nhẹ); rack focus; làm mờ chuyển động (siêu lấy mẫu).
- **Ánh sáng, màu:** key/fill/rim; color script theo hồi; một bảng grade; chống banding (dither/grain); tương phản chữ ≥ 4,5:1; an toàn cho người mù màu.
- **Hoạt hình:** 12 nguyên lý hoạt hình; chữ động theo nhịp lời; chuyển cảnh có động cơ (match cut, J/L-cut).
- **Âm thanh:** spotting và cue sheet; leitmotif; tempo map khớp dựng; sound design (whoosh, riser, impact, room tone); pan theo vị trí, reverb theo chiều sâu; khoét tần số 1–4 kHz khi có lời; khoảng lặng có chủ ý.
- **Master:** −14 LUFS (YouTube), true peak ≤ −1 dBTP, LRA 6–10 LU; tương thích mono.
- **Kỹ thuật:** CFR, không rơi khung; metadata BT.709; bitrate đủ (≥ 16 Mbps cho 1080p); phụ đề chuẩn.

## 5. Hạ tầng đã dựng (dùng lại được)

- Claude Code cloud session trên claude.ai/code, model Opus 5.5.
- Repo thử nghiệm: `github.com/HungQuach301/crux-spike-opus55` (riêng tư). Cine Lab nên dùng repo mới.
- Môi trường `crux-spike-av`:
  - Mạng Custom + default list, thêm `api.openai.com`, `huggingface.co`, `*.huggingface.co`, `*.hf.co`.
  - Khoá OpenAI gắn qua mục API credentials (proxy gắn khoá, phiên không thấy khoá).
  - Setup script cài ffmpeg, faster-whisper, pyloudnorm.
- Lưu ý đã gặp:
  - Biến `CLAUDE_CODE_ENVIRONMENT_NAME` có thể trống dù môi trường đúng; kiểm bằng cách gọi API qua proxy.
  - Lệnh `apt-get` trong setup script có thể lỗi âm thầm; phải có bước thử lại.
  - `pip install bpy` (Blender 5.0.1) cài được trong container; nó hạ numpy xuống 1.26 làm lệch opencv, nên cần venv riêng.
- TTS tạm: OpenAI gpt-4o-mini-tts; ASR kiểm: faster-whisper chạy cục bộ.
- Video trên 30 MB không gửi kèm qua giao diện phiên được; phải lấy từ nhánh git.

## 6. Cách làm việc (giữ như Crux)

- Trả lời tiếng Việt, văn phong chuyên nghiệp.
- Kế hoạch theo mốc và bước nhỏ, không theo tuần hay ngày.
- Mỗi đề xuất nêu ưu, nhược, tác động, rủi ro.
- Không đoán: kiểm bằng repo, tài liệu hiện hành hoặc chạy thật.
- Việc làm ngay được thì làm ngay, kèm hướng dẫn từng bước.
- Luôn nêu việc đang chờ chủ dự án.
- Chấm độc lập từ file đã render; không tin số phiên tự báo.
