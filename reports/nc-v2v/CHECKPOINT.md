# CHECKPOINT NC-V2V lượt 2 — 2026-10-19 17:35 UTC
- Bước 0: QUA (HTTP 200, có `gemini-omni-1.1-flash`).
- Thử cơ chế 1 lần (clip 4 s dựng từ khung `cong-hero.png` V7B): gọi đồng bộ bị cắt 30 s (HTTP 502) → chạy nền (`background: true`) + hỏi trạng thái: được 1280×720, 24 fps, 4,0 s, $0,4428 (sổ `so-ai.jsonl`).
- Bộ đệm cảnh V7B dựng lại xong (`/var/tmp/cine-out/k2tl-cache`, 1,1 GB; Catastro cần User-Agent; LUT từ origin/v5a).
- Đang dựng: c1 1080p, c2, c3, c4 (720p) bằng `scripts/k2/hero.js` của V7B (worktree tạm). Mặt nạ ID: `design/k2v/v2v/idmask.js` (đã thử đúng trên c1, c3).
- Mã thử: `design/k2v/v2v/{omni.py, idmask.js, mk_page.py, dung_id.js, clips.py, do_v2v.py, noi.py}`.
- Chi phí đến giờ: Gemini $0,44 · OpenAI $0.
