# Tài liệu ElevenLabs đọc lại hôm nay — eleven_v4: thanh tốc độ, giá (GIỌNG-CHỐT)

Ngày truy cập mọi URL: **2026-10-19 (UTC ≈ 00:00)**. Tải bản Markdown/HTML công khai, UA `CineLab-research (+https://github.com/HungQuach301/cine-lab)`; không gửi email, không gửi khoá. Trích nguyên văn.

## 1. Speed / Style của v4
URL: https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4.md
> Both variants use two voice settings: Stability and Similarity.

> Style and Speed sliders are not available in Eleven v4, and SSML is not supported.

> We're still experimenting with Eleven v4 to understand how best to use it.

API `GET /v1/models` (cùng ngày, số đo thật): `eleven_v4` → `can_use_style: false`, `can_use_speaker_boost: false`, `requires_alpha_access: false`, `maximum_text_length_per_request: 10000`.
⇒ Phiên này thu v4 **không gửi `speed`** (chỉ stability 0,5, similarity 0,75); v2 cùng cảnh: speed 1,0.

URL: https://elevenlabs.io/docs/api-reference/text-to-speech/convert.md
> `speed` (double, optional, nullable, default: 1) — Adjusts the speed of the voice. A value of 1.0 is the default speed, while values less than 1.0 slow down the speech, and values greater than 1.0 speed it up.

> `seed` (integer, optional, nullable) — If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed.

## 2. Giá / hệ số tính phí v4 so với v2
URL: https://elevenlabs.io/pricing/api (trích văn bản trang)
> v4 New Text to Speech $0.08 Price per 1K characters

> v4 Turbo New Text to Speech $0.04 Price per 1K characters

> v2 Multilingual Text to Speech $0.08 Price per 1K characters

> Creator $11 [...] 275k characters of TTS (v4) included

API `GET /v1/models`: `eleven_v4` `model_rates` = `{"character_cost_multiplier": 1.0, "cost_discount_multiplier": 1.0}`, `token_cost_factor` 1.0 — **giống hệt** `eleven_multilingual_v2`; `eleven_v4_turbo` 0,5.
⇒ Giá $0,08 của v4 trên trang Subscription là giá **bằng** v2 (không phải gấp đôi); chỉ v4 Turbo rẻ một nửa.

**Đo thật:** lượt pin 2k–2n bằng `eleven_v4` (807 ký tự gửi, gửi riêng, chờ 90 s): bộ đếm 134 845 → 135 200 = **+355 (0,440/ký tự)**; đọc lại trước lượt kế vẫn 135 200 (không trễ). Lượt v2 cùng chữ: gộp với móc, +862 cho 1 962 ký tự = 0,439. ⇒ **v4 và v2 tốn bộ đếm như nhau.**

## 3. Ghi chú
- URL `https://elevenlabs.io/docs/overview/models.md`: `eleven_v4` 10 000 ký tự/lệnh (≈ 10 phút).
- "API generations are discounted" (giay-phep.md §5) khớp tỷ lệ 0,44 bộ đếm/ký tự gửi đo được qua API.
