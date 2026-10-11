# toolkit/market — nhà máy dữ liệu thị trường (dùng chung mọi kênh)

Phiên M "Nhà máy dữ liệu", 11/10/2026. Hợp nhất `channel-k2/collect.py` · `current.py` · `final.py` (nhánh `channel-k2`) thành một
mô-đun cấu hình theo **gói kênh**; học cách cài vào quy trình từ Crux (`crux-lab`: `market/`, `CALIBRATION.md`,
`playbook/episode.md` §1b/§3.11/§5c/§10). Cài vào quy trình LL: `reports/m3/CHUAN-KENH-LL.md` §14 (không thêm cổng).

> Dữ liệu **chọn và định hướng**; KHÔNG quyết định nội dung hay hình. Nguyên tắc tối cao (chất lượng) đứng trên.

## Lệnh (Python chính: `/opt/cine/bin/python`)
| Lệnh | Việc | Đơn vị quota (ước) |
|---|---|---|
| `market.py purge` | xoá số liệu thô > 30 ngày (mọi lệnh cũng tự chạy trước) | 0 |
| `market.py quota --session S [--plan topic SLUG\|own\|niche KEY]` | phần còn được dùng hôm nay + ước của lệnh, CHẠY ĐƯỢC/KHÔNG | 0 |
| `market.py topic SLUG --pack ll --session ll` | hồ sơ cầu → `reports/m3/topics/SLUG.md` + `labels.json` | ≈ 100 × (số câu 90 ngày + số câu toàn thời gian) + ~30 (3+3 câu → ≈ 630) |
| `market.py queue --pack ll` | cột Cầu / Khoảng trống / Câu hỏi vào `topics/queue.md` (khối máy sinh) | 0 |
| `market.py own --pack ll --session ll` | lượt xem công khai video LL → `reports/m3/KHAN-GIA-SO.md` | 2–3 |
| `market.py predict SLUG --ep epNN --pack ll` | dòng DỰ ĐOÁN cho G1 (ghi `reports/m3/khan-gia/predictions.json`) | 0 |
| `market.py niche KEY --pack k2 --session k2` | thước "kênh mới bật được không" (port `final.py`) | ≈ 100 × số câu + ~200 |

Cờ chung: `--cap N` (trần đơn vị của lượt chạy), `--used-elsewhere N` (phiên khác đã dùng hôm nay), `--dry` (chỉ ước).
Test: `/opt/cine/bin/python -m unittest toolkit/tests/test_market.py -v` (dữ liệu giả `toolkit/tests/fixtures/market/`, không mạng, không AI).

## Tệp
| Tệp | Nội dung |
|---|---|
| `core.py` | gói kênh (kiểm trường, model phải ghim đủ tên), thư mục số liệu ngoài git, purge 30 ngày, gọi API có cache, `MarketError` |
| `quota.py` + `quota-policy.json` | bộ điều phối quota: ước trước khi chạy, thứ tự ưu tiên phiên, phần giữ cho phiên khác, dừng khi < dự phòng |
| `ai.py` | `claude -p --model <ghim>`, `ANTHROPIC_API_KEY="$CONSOLE_API_KEY"`, `--tools ""` (không subagent/công cụ), sổ chi, trần |
| `demand.py` | hồ sơ cầu: cầu hiện hành, cầu bền, khoảng trống, vượt trội, dải thời lượng, câu hỏi/hoàn cảnh/điểm yếu, mẫu tiêu đề |
| `render.py` | markdown hồ sơ + khối hàng đợi; `assert_repo_safe` chặn số thô kênh khác trước khi ghi repo |
| `own.py` | ảnh chụp lượt xem kênh mình ở mốc 48 giờ / 7 ngày / 28 ngày, dự đoán G1, luật hiệu chỉnh |
| `niche.py` | thước kênh mới bật được (port `channel-k2/final.py`, bỏ phần riêng ngách G) |
| `packs/ll.json`, `packs/k2.json` | gói kênh |

## Luật dữ liệu (fail closed)
- **Số thô kênh khác** (lượt xem, like, người đăng ký, bình luận nguyên văn, mô tả): chỉ ở `$MARKET_DATA` (mặc định
  `~/.cache/cine-market/<gói>/`), **ngoài git** — mã dừng nếu thư mục nằm trong một cây git. Mỗi lệnh tự xoá tệp > 30 ngày
  (YouTube API Developer Policies III.E.4); sổ chi AI giữ lại để trần không bị đặt lại. Không có lịch xoá khi mã không chạy
  (như channel-k2); container phiên mất thì dữ liệu mất theo.
- **Repo chỉ nhận:** định danh kênh/video, nhãn (Mạnh/Yếu/Không, Có/Không, ≥ 3×/≥ 5×), bậc lượt xem (≥ 500 nghìn …), dải,
  câu diễn đạt lại (không tên người, không trích nguyên văn). `render.assert_repo_safe` dừng nếu văn bản có số thô nào (lượt xem/like/bình luận/người đăng ký, like+phản hồi bình luận, ≥ 1 000) đã thu ở lượt chạy, viết đủ chữ số (12345 · 12,345 · 12.345 · 12 345). Giới hạn: không bắt dạng làm tròn ("4,8 triệu") và số < 1 000; lớp chặn chính là AI tổng hợp **không được nhìn thấy số đếm** (chỉ nhận tiêu đề và ý bình luận đã diễn đạt lại) và hồ sơ chỉ in bậc; `render.verbatim` dừng nếu câu AI chép nguyên ≥ 8 từ liền của bình luận hoặc tiêu đề (bình luận ngắn hơn 8 từ không bắt được; ý bình luận luôn qua bước diễn đạt lại của `classify`).
- Mọi nhãn/chỉ số tính ra ghi **"tự tính, không phải chỉ số YouTube"**.
- **Kênh mình (LL):** viewCount/like/bình luận công khai của video LL commit dạng tổng hợp theo video
  (`reports/m3/khan-gia/snapshots.jsonl`, `KHAN-GIA-SO.md`).
- **Fail closed:** lỗi HTTP, hết quota, phương thức bị giữ, model không ghim, thiếu khoá, AI không ra JSON, phủ nhãn < ngưỡng,
  vượt trần chi → `DỪNG:` + mã 2, không ghi đầu ra dở (ghi một lần ở cuối, `write_atomic`).
- AI: không subagent, không công cụ; model theo vai trong gói (`classify` Haiku 5.5, `judge` Sonnet 5.5, `reviewer` Opus 5.5);
  sổ ghi model ghim + model thực chạy (`served`); model ghim không có trong `served`, hoặc có model khác ngoài model ghim + Haiku phụ nội bộ của CLI → dừng. Lượt CLI hỏng/quá giờ ghi chi bằng trần lượt (ước dư). Trần gói `ai_cap_usd` ($5), dừng ở 90 %.
- 403 của `commentThreads` chỉ coi là "tắt bình luận" khi lý do là `commentsDisabled`; 403 khác (hết quota, khoá) dừng.

## Bộ điều phối quota
- Một project/khoá YouTube cho cả môi trường: 10 000 đơn vị/ngày, đặt lại 0:00 giờ Thái Bình Dương; `search.list` = 100.
- `quota-policy.json`: `priority` (k2 → ll → m), `reservations` (đơn vị giữ cho phiên đứng trước), `holds`
  (phương thức giữ riêng cho một phiên; giới hạn phương thức/đơn vị của một phiên), `reserve_floor` 500.
- Sổ đơn vị `$MARKET_DATA/quota/<ngày PT>.jsonl` chỉ thấy container này; phần phiên khác khai bằng `--used-elsewhere`.
  Không biết thì phần `reservations` là lớp bảo vệ. Hai phiên chạy song song phải khai cho nhau qua PLAN/BAN-GIAO.
- **Giới hạn:** `--session` do phiên tự khai, mã không xác minh được; luật giữ phương thức chỉ có hiệu lực khi phiên khai đúng tên. Mỗi phiên dùng đúng tên của mình (P LL = `ll`, k2 = `k2`, phiên dữ liệu = `m`).
- Hiện hành (chủ dự án 11/10): `search` chỉ phiên k2 tới hết 12/10; phiên M ≤ 50 đơn vị, chỉ `videos`/`channels`.

## Trọng số nhãn cầu — TẠM
Nhãn cầu là một cột tham khảo trong hàng đợi; chưa có trọng số chính thức trong chọn đề tài. Chốt sau `channel-k2/CALIBRATION.md`
(phiên k2, 12/10) và sau 3 tập LL có dự đoán G1 (`KHAN-GIA-SO.md`, luật hiệu chỉnh ở `own.calibrate`).

## Mốc 5 — kênh 2 dùng cùng toolkit
1. **Gói kênh** `packs/k2.json` (đã chuyển từ `channel-k2/current.py` Q/TITLE và `final.py` NICHE A/D/J): ngách, 12 đề tài × 6
   câu, model ghim, trần $5, đầu ra `channel-k2/de-tai/` + `channel-k2/HANG-DOI.md`. Đề tài mới: thêm `title` + 2–6 câu hỏi.
2. **Phiên** `k2` trong `quota-policy.json` (đứng đầu ưu tiên tới hết 12/10). Lệnh như LL, đổi `--pack k2 --session k2`.
3. **Khác LL:** ngưỡng có thể khác (`thresholds`), `long_min_s` giữ 480 s; thước kênh mới (`niche`) chỉ dùng cho định vị kênh;
   ngách B (tập kênh 72 câu) và phần nhãn riêng ngách G (khung âm mưu, tầng) **chưa port** — vẫn chạy bằng `channel-k2/final.py`.
4. **Khi kênh 2 có video:** thêm khối `own` (handle, `episodes`, đường dẫn snapshots/predictions/report) vào `packs/k2.json`;
   `market own --pack k2` sinh `KHAN-GIA-SO` riêng; luật hiệu chỉnh giống LL.
5. **Quy trình:** cài theo cùng 7 bước CHUAN-KENH-LL §14 vào tài liệu kênh 2 (hiến chương/luật chọn đề tài), không thêm cổng.
   `LUAT-CHON-DE-TAI.md` điều kiện 1 (có cầu) và 2 (khoảng trống) đọc thẳng nhãn `labels.json` của gói.
6. Dữ liệu cũ của channel-k2 ở `$K2C_DATA` không tự chuyển; `market topic` thu lại (cache riêng `$MARKET_DATA/k2/`).

## Khác channel-k2 (cố ý)
- Lỗi AI/HTTP dừng hẳn thay vì trả `{}` rồi đi tiếp; 429 không chờ 4 giờ (dừng, chạy lại sau khi quota đặt lại).
- Khoảng trống chạy `judge` (Sonnet) như luật 11/10, không Haiku.
- Cầu bền chỉ đếm video **đúng đề tài** (có chấm liên quan), channel-k2 vòng 1 đếm mọi video dài top 5.
- Hồ sơ trong repo không ghi lượt xem thô kênh khác (channel-k2 `de-tai/*.md` có ghi) — dùng bậc + nhãn vượt trội như Crux.
