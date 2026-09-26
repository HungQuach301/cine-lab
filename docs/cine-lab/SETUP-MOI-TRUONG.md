# CINE LAB — HƯỚNG DẪN DỰNG MÔI TRƯỜNG CLOUD `cine-lab-av` (26/09/2026)

Căn cứ: tài liệu Claude Code "Configure cloud environments" (code.claude.com/docs/en/cloud-environments), tài liệu xác thực ElevenLabs, và một lần chạy thử setup script trong máy Ubuntu 24.04 (xem mục 5).

## 1. Tạo môi trường

1. Vào **claude.ai/code** → ô chọn môi trường → **Add cloud environment**.
2. **Name:** `cine-lab-av`.
3. **Network access:** chọn **Custom**, **tích** ô *"Also include default list of common package managers"* (giữ PyPI, npm, Ubuntu apt, GitHub, Docker…).
4. **Allowed domains** — dán đúng khối dưới (mỗi dòng một tên miền):

```
huggingface.co
*.huggingface.co
*.hf.co
cdn.playwright.dev
playwright.download.prss.microsoft.com
api.launchpad.net
ppa.launchpadcontent.net
freesound.org
*.freesound.org
api.elevenlabs.io
```

| Tên miền | Dùng cho | Bắt buộc? |
|---|---|---|
| `huggingface.co`, `*.huggingface.co`, `*.hf.co` | Tải model faster-whisper (kiểm lời đọc) và ACE-Step (nhạc) | Có |
| `cdn.playwright.dev`, `playwright.download.prss.microsoft.com` | Tải Chromium để render hình 2D/HTML và chụp khung | Có (đã chạy thử: thiếu thì bị chặn 403) |
| `api.launchpad.net`, `ppa.launchpadcontent.net` | Thêm Python 3.13 (PPA deadsnakes) cho Blender `bpy` — bpy không có bản cho Python 3.12 mặc định | Có nếu dùng Blender |
| `freesound.org`, `*.freesound.org` | Tải SFX CC0/CC BY | Tuỳ chọn |
| `api.elevenlabs.io` | Giọng, SFX của ElevenLabs | Có (thực tế host có API credential đi được cả khi không liệt kê; ghi để rõ ràng) |

Không cần thêm: PyPI, npm, `archive.ubuntu.com`, GitHub (đã trong danh sách mặc định; GitHub đi proxy riêng).

5. **Environment variables:** để trống. **Không** dán khoá API vào đây (ai dùng môi trường cũng đọc được).
6. **Setup script:** dán toàn bộ nội dung `scripts/env/setup.sh`.
7. **Create environment.**

## 2. Gắn khoá ElevenLabs (API credential)

API credential chỉ thêm được **sau khi** môi trường đã tạo, và chỉ có ở gói Pro/Max.

1. Rê chuột lên `cine-lab-av` → biểu tượng cài đặt → **Update cloud environment** → mục **API credentials** → **Add credential**.
2. **Credential type:** Bearer (mặc định).
3. **Name:** `ElevenLabs`.
4. **Allowed websites:** `api.elevenlabs.io`.
5. **Custom headers:** đổi tên header từ `Authorization` thành **`xi-api-key`**, **xoá Prefix** (`Bearer`), dán khoá ElevenLabs vào **Value**.
6. **Connect.** Khoá sẽ không xem lại được; muốn đổi thì xoá và thêm lại.

Lưu ý:
- Proxy **không** gắn khoá cho request trong setup script. Vì vậy mọi lệnh gọi ElevenLabs phải chạy trong phiên, không chạy trong setup.
- Khoá OpenAI không cần cho Cine Lab. TTS đã chuyển sang ElevenLabs.

## 3. Phần mềm được cài (setup script)

| Nhóm | Gói | Vai trò |
|---|---|---|
| Hệ thống (apt) | ffmpeg, sox, mediainfo, fonts-noto-core, fonts-liberation2, thư viện đồ hoạ cho Blender | Dựng, mã hoá, đo âm lượng (ebur128), font |
| Python chính `/opt/cine` | faster-whisper, pyloudnorm, numpy, scipy, soundfile, librosa, opencv-python-headless, pillow, scenedetect, elevenlabs, requests, jsonschema | Kiểm lời đọc, LUFS, phân tích hình, phát hiện cú cắt, gọi ElevenLabs |
| Blender `/opt/bpy` (Python 3.13) | bpy | Dựng 3D/2.5D, Grease Pencil |
| Node `/opt/pw` | playwright + Chromium | Render 2D/HTML/Canvas theo khung |
| Có sẵn trong VM | Python 3.x, Node 22, git, gh, Docker, GCC… | — |
| **Không** cài trong setup | model faster-whisper, ACE-Step | Tải trong phiên (setup phải xong trong ~5 phút) |

Setup chạy song song các nhóm, tự thử lại 3 lần mỗi lệnh, luôn thoát 0 để môi trường được lưu cache. Kết quả ghi ở `/var/log/cine-setup.log`, dòng `RESULT`.

## 4. Kiểm tra sau khi tạo

1. Mở phiên mới trên repo, chọn môi trường `cine-lab-av`.
2. Bảo Claude: *"Chạy `bash scripts/env/verify.sh` và báo kết quả"*.
3. Kỳ vọng: toàn bộ **PASS**, gồm "ElevenLabs API (khoá được proxy gắn)" và số vCPU/RAM thật của máy.
4. Có dòng FAIL: gửi nguyên văn cho Claude trong Project Cine Lab để xử lý.

Setup script chạy lại khi: đổi nội dung script, đổi danh sách tên miền, hoặc cache hết hạn (~7 ngày).

## 5. Đã chạy thử (26/09/2026, máy thử Ubuntu 24.04, 2 CPU)

- Cú pháp 2 script: đạt.
- Nhóm Python chính: **đạt**; toàn bộ setup chạy **44 giây**.
- Chromium: **bị chặn 403 tại `cdn.playwright.dev`** vì máy thử không có tên miền này. Đây là bằng chứng phải thêm tên miền ở mục 1.
- PPA deadsnakes: bị chặn tại `api.launchpad.net`, `ppa.launchpadcontent.net` ở máy thử, cùng lý do.
- Chưa chạy được trong môi trường `cine-lab-av` thật → verify.sh là bước xác nhận cuối.

## 6. Rủi ro

| Rủi ro | Xử lý |
|---|---|
| PPA hoặc bpy lỗi | Blender là tuỳ chọn; quyết định phong cách ở Cổng 0 có thể không cần Blender |
| Playwright đổi CDN ở phiên bản sau | verify.sh báo FAIL Chromium → xem log, thêm tên miền mới |
| Setup vượt 5 phút | Tách bpy hoặc Chromium sang SessionStart hook |
