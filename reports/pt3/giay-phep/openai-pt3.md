# OpenAI — tài liệu đọc lại cho PT3 (18/10/2026)

Khoá do proxy gắn cho api.openai.com; phiên không đọc/in/ghi khoá. Giá + điều khoản quyền đầu ra + C2PA/SynthID: xem `reports/pt/giay-phep/openai.md` (PT, đọc 17–18/10, không đổi).

## 1. `GET /v1/models` (18/10, HTTP 200) — model ảnh có trong danh sách
`chatgpt-image-latest, gpt-image-1, gpt-image-1-mini, gpt-image-1.5, gpt-image-2, gpt-image-2-2026-04-21, gpt-image-2.5-flare, gpt-image-2.5-flare-2026-09-08, gpt-image-2.5-sunburst, gpt-image-2.5-sunburst-2026-09-08`
→ PT3 ghim bản chụp **`gpt-image-2.5-sunburst-2026-09-08`** (model sửa ảnh hiện hành theo hướng dẫn: "Choose Sunburst for workflows where editing precision matters most").

## 2. Tham chiếu `POST /v1/images/edits` — https://developers.openai.com/api/reference/resources/images/methods/edit
SHA-256 HTML gốc: 55bb53b4621c726c5068ac809283ab1791a3e1ab0f3862354377c04f012d7d59
```text






```
Hướng dẫn (đã chép ở PT §5.2): "Masking with GPT Image is entirely prompt-based." → PT3 GHÉP CỨNG theo mặt nạ sau khi nhận ảnh.
