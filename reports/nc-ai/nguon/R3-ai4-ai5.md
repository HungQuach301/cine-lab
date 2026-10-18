# R3 — AI4/AI5: SFX/ambience AI, giọng đọc ElevenLabs, image-to-video, chính sách YouTube

Ngày đọc: **2026-10-18** (mọi URL dưới đây đọc ngày này, trừ khi ghi khác). Không gọi API trả phí nào.

**Lưu ý phương pháp (quan trọng):** công cụ WebFetch trả về bản trích do một mô hình nhỏ đọc trang, không phải HTML thô. Các câu trong ngoặc kép là trích dẫn mà công cụ báo là nguyên văn; với điều khoản pháp lý then chốt (quyền sở hữu, giấy phép, ngưỡng doanh thu), trước khi ghi vào `RIGHTS.md` cần một người mở trang gốc và đối chiếu từng chữ. Mục nào chỉ có nguồn thứ cấp (blog, bên bán lại) được đánh dấu **[thứ cấp]**; mục bị chặn được đánh dấu **[BỊ CHẶN]**.

---

## A. Sinh hiệu ứng âm thanh / không khí (ambience) bằng AI

### A1. ElevenLabs Sound Effects
- Tài liệu endpoint: https://elevenlabs.io/docs/api-reference/text-to-sound-effects/convert
  - `POST https://api.elevenlabs.io/v1/sound-generation`
  - Body: `text` (bắt buộc), `model_id` mặc định và duy nhất `eleven_text_to_sound_v2`, `duration_seconds` "Must be at least 0.5 and at most 30.", `loop` (boolean, chỉ v2; tạo âm lặp liền mạch, hữu ích cho nền gió/biển), `prompt_influence` mặc định 0.3.
  - Query `output_format`: "MP3 with 192kbps bitrate requires you to be subscribed to Creator tier or above"; PCM 44.1 kHz cần Pro trở lên.
  - Trang tài liệu không ghi giá.
- Giá (https://elevenlabs.io/pricing/api): Sound Effects "$0.12" mỗi phút; FAQ lại ghi "Music and Sound Effects are billed per generation". Hai câu này mâu thuẫn, nên **đơn vị tính tiền chưa rõ**; cần kiểm bằng một lần tạo thật trên tài khoản (xem số credit bị trừ).
- Điều khoản (https://elevenlabs.io/terms-of-use, "Last Updated: 09 October 2026"):
  - Quyền sở hữu, mục 4(c)(ii): "Except as expressly set forth herein, as between you and ElevenLabs, you retain all rights in and to your Output."
  - Gói miễn phí, mục 1(c)(i): chỉ dùng phi thương mại. Câu nguyên văn kèm theo: "If using the Services for non-commercial purposes, a personal e-mail address must be used."
  - Gói trả phí được dùng thương mại, tuân theo Prohibited Use Policy (mục 1(c)(ii)).
  - Trang điều khoản không có điều khoản về C2PA hay watermark.
- **Kết luận:** muốn dùng thương mại phải có gói trả phí (Starter $6/tháng trở lên). Âm ra thuộc về người dùng.

### A2. Stability AI: Stable Audio Open 1.0 / Stable Audio 2.5
- Stable Audio Open 1.0 (https://huggingface.co/stabilityai/stable-audio-open-1.0):
  - Giấy phép "Stability AI Community License"; "For commercial use, please refer to https://stability.ai/license".
  - Dữ liệu huấn luyện: "486492 audio recordings, where 472618 are from Freesound and 13874 are from the Free Music Archive (FMA)." "All audio files are licensed under CC0, CC BY, or CC Sampling+."
  - Giới hạn: "The model is better at generating sound effects and field recordings than music."
  - Lưu ý: tập huấn luyện có cả Sampling+, là giấy phép mà ta loại khi chọn tài sản. Đây không phải vi phạm pháp lý trực tiếp, nhưng nên ghi vào `RIGHTS.md` như một rủi ro về nguồn gốc dữ liệu.
- Community License (https://stability.ai/community-license-agreement, "July 5, 2024"):
  - Ngưỡng doanh thu: giấy phép chấm dứt nếu You/Affiliates "generate more than USD $1,000,000 in annual revenue (or the equivalent thereof in Your local currency)".
  - Đầu ra: "As between You and Stability AI, You own any outputs generated from the Models or Derivative Works to the extent permitted by applicable law."
- Stable Audio 2.5 (chỉ có qua API, không có trọng số mở): trang https://platform.stability.ai/pricing **[BỊ CHẶN: trang JS, không có nội dung]**. Nguồn thứ cấp nói 1 credit = $0.01 và khoảng 20 credit mỗi lần tạo text-to-audio, nhưng chưa xác minh được **[thứ cấp]**.

### A3. Meta AudioCraft / AudioGen
- https://github.com/facebookresearch/audiocraft/blob/main/LICENSE_weights: "Creative Commons Attribution-NonCommercial 4.0 International Public License" (CC-BY-NC 4.0). **Đã xác nhận NC, nên loại** vì phim có kiếm tiền.

### A4. Các mô hình khác
| Mô hình | Giấy phép (nguyên văn) | URL | Kết luận |
|---|---|---|---|
| AudioLDM 2 | "License: cc-by-nc-sa-4.0" | https://huggingface.co/cvssp/audioldm2 | Loại (NC) |
| Tango 2 | "License: cc-by-nc-sa-4.0" | https://huggingface.co/declare-lab/tango2 | Loại (NC) |
| Mirelo SFX (video→âm) | Chưa tìm thấy điều khoản chính thức | fal.ai: v1.5 $0.01/giây **[thứ cấp]**; SFX 2.0 ra ngày 14/10/2026 theo một blog | Chưa đủ căn cứ; cần đọc ToS của Mirelo |
| Adobe Firefly Sound Effects | helpx.adobe.com **[BỊ CHẶN: 403]** | Tubefilter (02/10/2026) dẫn blog Adobe gọi bộ âm thanh là "commercially safe" **[thứ cấp]**; trang Firefly nói có cả "partner models from Google, OpenAI, ElevenLabs, Luma AI, Runway, and others" | Phải biết mỗi lần tạo dùng mô hình Adobe hay mô hình đối tác; cần đọc Adobe Generative AI Product Specific Terms |
| Google (Lyria / âm của Veo) | Không đọc riêng trong đợt này | Âm đi kèm Veo 3.1 có trong giá "with audio" | Xem mục C |

### A5. Freesound (đối chứng)
- FAQ (https://freesound.org/help/faq/):
  - CC0: "for the "zero" license you can do pretty much what you want with the sound." "You could even sell the sound, ... but you can't claim you are the author!"
  - BY-NC: "works like attribution, but you can't earn any money with the piece of work you create!"
  - Sampling+: "you can do pretty much what you could do with the attribution noncommercial license", không được dùng cho quảng cáo thương mại; Creative Commons đã rút giấy phép này. **Loại cả NC và Sampling+.**
- API:
  - Xác thực (https://freesound.org/docs/api/authentication.html): dùng token cho các tài nguyên chỉ đọc; OAuth2 "enables non “read-only” resources...".
  - Tải file gốc (https://freesound.org/docs/api/resources_apiv2.html): "Download Sound (OAuth2 required)". Bản xem trước HQ MP3 có trường `previews`, nhưng tài liệu không nói có cần OAuth2 hay không.
  - Điều khoản API (https://freesound.org/help/tos_api/): "Terms for commercial use of the API will be negotiated on a case by case basis with UPF"; "You will be provided with one Access Key per Application."
  - **Hệ quả:** tải thủ công từ website rồi lưu bằng chứng giấy phép CC0 thì an toàn. Dùng API tự động cho dự án thương mại thì về chữ nghĩa cần thương lượng với UPF. Dù đi đường nào cũng cần tài khoản và key.

---

## B. ElevenLabs: giọng đọc trích dẫn lịch sử

| Mô hình TTS (tên trên trang giá) | USD / 1K ký tự |
|---|---|
| "v4" | $0.08 |
| "v4 Turbo" | $0.04 |
| "v3" | $0.08 |
| "v3 Conversational" | $0.04 |
| "v2 Multilingual" | $0.08 |
| "Flash / Turbo" | $0.04 |

- Nguồn giá: https://elevenlabs.io/pricing/api. Các gói: Free/PAYG, Starter $6, Creator $22, Pro $99, Scale $299, Business $990/tháng.
- Mã `model_id` cụ thể cho "v4" chưa đọc trên trang models; cần kiểm trước khi viết mã.
- Ước tính: một phim 15 phút có khoảng 3.000 ký tự trích dẫn, tức khoảng $0.24 ở mức $0.08/1K, chưa tính các lần tạo lại.
- Thương mại: chỉ gói trả phí (Terms 1(c), xem A1).
- Prohibited Use Policy (https://elevenlabs.io/use-policy, cập nhật 09/10/2026):
  - "Cloning, synthesizing, or impersonating the voice, identity, or likeness of any living individual"
  - "or of any deceased individual in a manner that is reasonably likely to cause harm"
  - "a person's voice or likeness without authorization"
  - "You must clearly disclose when people are interacting with AI where required by law"
- **Diễn giải:** dùng một giọng tổng hợp chung (voice library hoặc voice design) để *đọc* lời nhân chứng thì **không phải** nhân bản giọng thật của người đã mất. Cấm là nhân bản hay giả giọng một cá nhân cụ thể. Không được dựng "giọng thật" của nhân vật lịch sử (cũng không có bản ghi nào để làm vậy). Nên ghi rõ trên màn hình hoặc trong mô tả, ví dụ "Voiced by a synthetic narrator; words from [source, year]", để tránh khán giả tưởng đó là giọng thật.
- Watermark / C2PA:
  - https://elevenlabs.io/docs/eleven-creative/audio-tools/audio-detector: "Uses watermarking technology to detect imperceptible watermarks embedded in ElevenLabs-generated audio."; "Content generated by third-party models available through ElevenLabs is generally not watermarked."
  - Theo kết quả tìm kiếm (help.elevenlabs.io), SynthID hiện được gắn vào mọi lần TTS của người dùng miễn phí và "select paid features", và đang mở rộng dần **[thứ cấp; trang help 403, blog /synthid 404]**.
  - Báo chí nói ElevenLabs áp dụng C2PA, nhưng chưa có tài liệu chính thức **[thứ cấp, chưa xác minh]**.

---

## C. Image-to-video (chỉ cho cảnh phi sự thật: biển, trời, khói xa)

Giá 5 giây được tính từ đơn giá chính thức, trừ chỗ ghi khác. "API generic server" nghĩa là gọi được bằng REST với key từ một máy chủ bất kỳ.

| Nhà cung cấp / mô hình | Còn hoạt động? | Giá ~5 s | Thời lượng tối đa mỗi lần | Quyền đầu ra (nguyên văn) | Watermark / C2PA | API từ server |
|---|---|---|---|---|---|---|
| **Google Veo 3.1** (`veo-3.1-generate-preview`, `-fast-`, `-lite-`) | Có (preview); Veo 3.0 "Deprecated" | Đơn giá/giây: Std 720p/1080p $0.40, 4K $0.60; Fast $0.10/$0.12/$0.30; Lite $0.05/$0.08. Không có lựa chọn 5 s: Lite 720p 4 s = $0.20, 6 s = $0.30; 1080p bắt buộc 8 s (Lite $0.64, Fast $0.96, Std $3.20) | 4/6/8 s; "8 seconds only if 1080p or 4k" | Gemini API Terms (cập nhật 2026-04-28): "Google won't claim ownership over that content." | "Videos created by Veo are watermarked using" SynthID; trang không nói về C2PA | Có. Lưu ý: ở EEA/CH/UK chỉ được dùng Paid Services; I2V chỉ "allow_adult"; video lưu trên server 2 ngày |
| **Runway** `gen4.5`, `gen4_turbo` | Có | $0.01/credit. gen4.5 12 cr/s → **$0.60**; gen4_turbo 5 cr/s → **$0.25**; còn có veo3.1 qua Runway (40 cr/s có audio) | Chưa đọc được (trang API bị cắt) | Terms (cập nhật 15/09/2026): "The Company does not claim ownership of any of your Inputs or Outputs." "...does not restrict your commercial use of your Outputs." Runway có quyền dùng Input/Output để huấn luyện | Footer có link "Verify Content Credentials"; ToS không nói | Có |
| **Luma Ray3.2** (`ray-3.2`) | Có | I2V 5 s: 720p **$0.30**, 1080p **$1.20** (SDR; HDR gấp 2) | Có bảng giá 10 s | ToS (14/05/2026) mục 4.9.1: Customer "owns and retains all right, title, and interest in and to the Output"; thương mại chỉ khi Output "were produced during an active Subscription Term" thuộc gói cho phép; API có API Terms riêng (chưa đọc) | Luma có thể nhúng "watermarks, content credentials, provenance metadata" và người dùng không được gỡ; Output giống người thật phải ghi là AI | Có |
| **Kling 3.0** | Có (theo bên thứ ba) | **[thứ cấp]** 720p không audio $0.084/s → ~$0.42; 1080p $0.112/s → ~$0.56 | — | Trang chính thức **[BỊ CHẶN: JS]**; theo nguồn thứ cấp gói trả phí được dùng thương mại và Kuaishou có licence rộng trên nội dung | Gói free có watermark hiện **[thứ cấp]** | Có, mua theo gói tài nguyên |
| **MiniMax** (H3; Hailuo 2.3/02 là "Legacy") | Có | H3 768P $0.08/s → ~$0.40; Hailuo-2.3 1080P 6 s $0.49; 2.3-Fast 1080P 6 s $0.33 | Hailuo: 6/10 s | Chưa đọc ToS | Trang giá không nói | Có |
| **Pika 2.2 / 2.5** | Pika 2.2 còn trên fal.ai; Pika không có API riêng rõ ràng | **[thứ cấp]** fal: 5 s 720p $0.20, 1080p $0.45 | 5–10 s | Chưa đọc | — | Qua fal.ai |
| **ByteDance Seedance 2.0** (BytePlus ModelArk) | Có | **[thứ cấp, dẫn trang giá BytePlus]** 5 s 16:9: 720p ~$0.76, 1080p ~$1.87; Fast 720p ~$0.60 | — | Chưa đọc | — | Có (ModelArk) |
| **Alibaba Wan 2.2** (mở) | Trọng số Wan 2.2 có thật; Wan 2.6/2.7/3.0 không có trọng số mở được xác nhận **[thứ cấp]** | Tự chạy (chi phí GPU) | ~5 s | "The models in this repository are licensed under the Apache 2.0 License."; "We claim no rights over the your generated contents" (https://huggingface.co/Wan-AI/Wan2.2-I2V-A14B) | Không có | Tự host |
| **LTX-2** (Lightricks, mở) | Có | Tự chạy | — | "ltx-2-community-license-agreement": doanh nghiệp có "annual revenues of at least $10,000,000" phải "obtain a paid commercial use license"; "Licensor claims no rights in the Output you generate using LTX-2" | Không | Tự host |
| **HunyuanVideo-I2V** (Tencent, mở) | Có | Tự chạy | — | Territory: "the worldwide territory, excluding the territory of the European Union, United Kingdom and South Korea."; trên 100 triệu MAU phải xin giấy phép | Không | Tự host. **Rủi ro** nếu bán phim ở EU/UK/Hàn: nên loại |
| **Stable Video Diffusion** | Trọng số còn trên HF | Tự chạy | ~2–4 s (25 khung) | "License: stable-video-diffusion-community"; theo Community License (ngưỡng $1M doanh thu/năm) | Không | Tự host; chất lượng thấp hơn hẳn các mô hình 2026 |
| **OpenAI Sora / Videos API** | **ĐÃ TẮT** | — | — | https://developers.openai.com/api/docs/deprecations: "On March 24th, 2026, we notified developers using the Videos API and Sora 2 video generation model aliases and snapshots" "of their deprecation and removal from the API on September 24, 2026." Áp dụng cho `sora-2`, `sora-2-pro` và các snapshot; trang không nêu mô hình thay thế | — | Không |

---

## D. YouTube

### D1. Disclosing altered or synthetic content
Nguồn: https://support.google.com/youtube/answer/14328491

- **Phải khai báo:**
  - "Alters footage of a real event or place."
  - "AI generated extra footage of a real place, like a video of a surfer in Maui for a promotional travel video"
  - "Showing a realistic depiction of a tornado or other weather events moving toward a real city"
  - "Makes a real person appear to say or do something they didn't do."
- **Không cần khai báo:**
  - "Creators don't need to disclose non-realistic content that's made with AI"
  - "AI generating or extending a backdrop to simulate a moving car"
  - "Special effects filters, like adding background blur or vintage effects"
  - "Cloning one's own voice to create voice overs or dubs"
- Trang **không có** ví dụ nào về sky/sea hay sự kiện lịch sử.
- Cách nhãn hiển thị: với "non-photorealistic or animated content" thì "Labels may appear in the expanded description"; với nội dung photorealistic thì "a label in the video player may also appear".
- **Diễn giải cho Cine Lab:** phim hoạt hình phong cách hoá, không photoreal, thuộc nhóm "non-realistic", nên phần hình nói chung không bắt buộc khai báo. Tuy vậy, nếu cảnh I2V trông thật và tả một địa điểm hay sự kiện có thật (cảng, trận đánh, khói ở một thành phố cụ thể), nó gần với ví dụ "extra footage of a real place" và "alters footage of a real event". Giọng tổng hợp đọc lời nhân chứng có thật cũng gần với "real person appear to say". **Khuyến nghị: bật khai báo** để an toàn; với hoạt hình, nhãn chỉ nằm trong mô tả.

### D2. Kiếm tiền: "inauthentic content"
Nguồn: https://support.google.com/youtube/answer/1311392

- Đổi tên ngày 15/07/2025: "We are also renaming this policy from "repetitious content" to "inauthentic content.""
- Yêu cầu chung: "the substance of each video should be materially varied and deliver creative, educational, or other value."
- Không được:
  - "AI-generated content made with generic or unoriginal templates giving the impression of mass production"
  - "Image slideshows, templated storylines, or scrolling text with minimal or no narrative, commentary, or educational value"
- Được, ví dụ: "like using AI to edit your video scripts or generate a unique background visual"
- Về giọng/đọc văn bản, mục Reused Content không cho phép: "Content that exclusively features readings of other materials you did not originally create," "like text from websites or news feeds".
- Trang **không có** chính sách riêng về TTS/giọng AI.
- **Hệ quả:** phim chỉ ghép trích dẫn nhân chứng đọc bằng TTS là rủi ro. Cần có lời bình, cấu trúc và phân tích gốc của tác giả bao quanh trích dẫn. Kiểu phim tài liệu kể chuyện có kịch bản riêng phù hợp với điều này.

---

## Khuyến nghị ngắn

1. **SFX / ambience:**
   - Lớp chính: Freesound **CC0** (tải thủ công, lưu ảnh chụp trang giấy phép và ID vào `RIGHTS.md`) cộng ElevenLabs SFX v2 trên **gói trả phí** (≤30 s, `loop=true` cho nền gió/biển).
   - Stable Audio Open dùng được khi doanh thu dưới $1M/năm, nhưng phải ghi rủi ro dữ liệu Sampling+.
   - Loại AudioGen, AudioLDM 2 và Tango 2 (NC).
   - Adobe Firefly và Mirelo chỉ xét sau khi đọc được ToS gốc.
2. **Giọng:**
   - Dùng ElevenLabs gói trả phí (Creator $22 để có MP3 192 kbps; Pro nếu cần PCM 44.1 kHz), mô hình "v3"/"v4" ở $0.08/1K ký tự, với giọng tổng hợp, **không** nhân bản giọng người thật.
   - Ghi rõ "synthetic voice" trong mô tả và credits, đồng thời bật khai báo AI trên YouTube.
3. **I2V (chỉ cảnh phi sự thật):**
   - Ưu tiên **Veo 3.1 Fast/Lite** (rẻ, có SynthID; điều khoản "won't claim ownership") hoặc **Runway gen4.5** (điều khoản sở hữu và thương mại rõ nhất).
   - **Luma Ray3.2** chỉ khi duy trì gói thuê bao có quyền thương mại.
   - Nếu tự host: **Wan 2.2 (Apache 2.0)** là sạch nhất về giấy phép; LTX-2 dùng được khi doanh thu dưới $10M.
   - Loại HunyuanVideo (không có quyền ở EU/UK/KR) và Sora (đã tắt từ 24/09/2026).
   - Mọi cảnh I2V phải qua cổng chất lượng về liền mạch phong cách với khung hình render gốc.
4. **Việc cần chủ dự án hoặc người kiểm tay:**
   - Đối chiếu nguyên văn các điều khoản then chốt.
   - Mở các trang bị chặn: Kling, BytePlus pricing, Adobe, Stability pricing.
   - Xác nhận đơn vị tính tiền SFX của ElevenLabs bằng một lần tạo thử có giám sát.

---

## Nguồn

### URL đã đọc trực tiếp (WebFetch có nội dung): 31
1. https://elevenlabs.io/docs/api-reference/text-to-sound-effects/convert
2. https://elevenlabs.io/pricing/api
3. https://elevenlabs.io/terms-of-use
4. https://elevenlabs.io/use-policy
5. https://elevenlabs.io/docs/eleven-creative/audio-tools/audio-detector
6. https://stability.ai/community-license-agreement
7. https://huggingface.co/stabilityai/stable-audio-open-1.0
8. https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt
9. https://github.com/facebookresearch/audiocraft/blob/main/LICENSE_weights
10. https://huggingface.co/cvssp/audioldm2
11. https://huggingface.co/declare-lab/tango2
12. https://freesound.org/help/faq/
13. https://freesound.org/docs/api/authentication.html
14. https://freesound.org/docs/api/resources_apiv2.html
15. https://freesound.org/help/tos_api/
16. https://ai.google.dev/gemini-api/docs/pricing
17. https://ai.google.dev/gemini-api/docs/video
18. https://ai.google.dev/gemini-api/docs/veo
19. https://ai.google.dev/gemini-api/terms
20. https://docs.dev.runwayml.com/guides/pricing/
21. https://docs.dev.runwayml.com/guides/models/
22. https://runway.com/terms-of-use
23. https://lumalabs.ai/api/pricing
24. https://lumalabs.ai/legal/tos
25. https://platform.minimax.io/docs/guides/pricing
26. https://developers.openai.com/api/docs/deprecations
27. https://huggingface.co/Lightricks/LTX-2
28. https://huggingface.co/Lightricks/LTX-2/blob/main/LICENSE
29. https://huggingface.co/tencent/HunyuanVideo-I2V/blob/main/LICENSE
30. https://huggingface.co/Wan-AI/Wan2.2-I2V-A14B
31. https://support.google.com/youtube/answer/14328491 và https://support.google.com/youtube/answer/1311392

### Bị chặn hoặc trống: 7
- https://platform.stability.ai/pricing (JS, trống)
- helpx.adobe.com (Firefly sound effects, 403)
- https://kling.ai/document-api/productBilling/billingMethod (JS, trống)
- https://docs.dev.runwayml.com/api/ (bị cắt)
- https://docs.byteplus.com/en/docs/ModelArk/1544106 (không có bảng giá)
- https://elevenlabs.io/blog/synthid (404)
- help.elevenlabs.io (403)

### Tìm kiếm web: 9 truy vấn
Gồm Stable Audio 2.5, Adobe Firefly, Mirelo, Kling ToS, Kling giá, Seedance giá, Pika, ElevenLabs C2PA và Wan. Các số liệu lấy từ tìm kiếm được đánh dấu **[thứ cấp]**.
