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

## Lượt 2 (≈ 05:20 UTC)
- Kiểm có đáp án (khung thử = render cổng 'cang' + 6 vật chèn bằng gpt-image, chỉ dán trong hộp, ngoài lớp (a)): gpt-6.1-sol 6/6, claude-sonnet-5-5 6/6, q_thoi_dai.py 3/3 lỗi thời đại; đối chứng (render ↔ render) 0 báo ở cả hai.
- O1 lượt 2 (không mặt nạ) 6 ảnh + 2 tấm timelapse; khớp màu Reinhard làm lệch viền nền↔vật giảm ≈ 21 → 5–7 ΔE. Sửa ghép: bảo vệ (a) nở 1 px, vật nhỏ nở 3 px (cờ trại bị báo "mất" khi chưa nở).
- Lượt 2 đọc nguồn (gpt-6.1-sol) + P phân xử → sửa mô tả mục (a)/(b). Luật nháp `LUAT-N2P-T4.md` §1–4, §6.
- Đang chạy: kiểm cuối O1 (máy + 2 mô hình + q_thoi_dai); dựng clip c1 (≈ 70 %), c4B; sau đó Omni c1.

## Lượt 3 (≈ 06:45 UTC)
- O1 lượt 3 (làm lại ảnh trượt lượt 2: bỏ chữ "terraces/plots" đã gợi AI vẽ tường đá); bộ kiểm (ii) sửa: cờ "thời đại sai" không kèm năm → nghi vấn; (iii) thêm T9b (bỏ loé nắng + dải 8 px bờ).
- Omni: c1, c4B, c2 (vừa/mạnh) đã gọi; Omni đổi máy/địa lý (c4B mạnh dựng hẳn góc máy mới), bịa lửa + nhà ở c1 → ghép lớp (a) không cứu được. Làm lại 1 lượt (lệnh "RESTYLE ONLY") cho c1, c4B đang chạy.
- Timelapse 12 s máy cố định (2 tấm AI 1/7 và 18/9/1779) đã ghép; đo hoà mờ vs cắt cứng.
