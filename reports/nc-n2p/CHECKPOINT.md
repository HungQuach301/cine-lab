# NC-N2P — CHECKPOINT (nhánh `nc-n2p` từ origin/main @bc7e96d1)

## Lượt 1 (≈ 05:00 UTC 21/10/2026)
- Bước 0 Gemini QUA: `GET /v1beta/models` 200, có `gemini-omni-1.1-flash` (bản Omni mới nhất; `gemini-omni-flash-preview` sẽ tắt 22/10/2026). OpenAI `/v1/models` 200 (gpt-image-2.5-sunburst-2026-09-08, gpt-6.1-sol).
- Nguồn T4 tải + SHA (Pepys #4167 `8a7ec38e…`, Evelyn #42081 `912a1791…` — khớp SHA NC-AI; "A True and Exact Relation … 1666" EEBO-TCP A63370 `1bf5c146…`).
  Danh mục (a) 27/27 và (b) 42/42 câu trích KHỚP nguyên văn (`ma/kiem_trich.py`).
- Worktree tạm `/var/tmp/n2p-wt` @ V7C 47a0f55a (đọc/gọi, không sửa); bộ đệm k2tl dựng lại (`ma/dung_cache.sh`, mọi SHA KHỚP).
- Mặt nạ ID V7C 1920×1080 cho 3 khung cổng A (cang f84, vay-ham f523, toan-canh f62) — khớp hình học với `reports/nc-cpu/khung/A`.
- O1 lượt 1 (có mặt nạ) 6 ảnh $0,459: gpt-image VẼ LẠI HÌNH HỌC (đất → biển ở vay-ham 32 %, núi Rock đổi dáng) → T9 trượt. Lượt 2 KHÔNG mặt nạ: giữ hình học (vay-ham T9 0,27/0,21 %).
- Đang chạy nền: dựng clip nguồn 1280×720 + mặt nạ (c1, c2, c4B, tl, c4A) ≈ 20 s/khung/làn; O1 lượt 2 (5 ảnh).
- Tệp ngoài git: /var/tmp/n2p/** (ảnh AI, khung nguồn), /var/tmp/cine-out/k2tl-cache.
