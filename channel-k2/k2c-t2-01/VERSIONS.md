# K2C-T2-01 · VERSIONS (ghim ở G1, 15/10/2026)
| Thành phần | Ghim | Kiểm |
|---|---|---|
| Luật kiểm (phiên K) | `checks/` **1.10.2**, LOCK TREE_SHA256 `c598467f2283b141b8a14382c18dbe23b370522ef2a1afb31856399f7eb4549e` | `checks/lock.py --verify` → **KHỚP** (15/10); phiên T2 không sửa, không đọc mã `checks/` |
| Bộ công cụ k2v (sau Bước 0c) | `design/k2v/`, `scripts/k2/` tại commit G1 của nhánh `k2c-t2` (xem `git log -1 -- design/k2v scripts/k2` tại thẻ G1); thay đổi trong T2: hàng xu dày + cạnh khía + gờ (`relief.js`), hộp né mép trước hàng xu, footage khung trong khung (`hero.js`), DEM SRTM ngoài Mỹ + đệm ô 3DEP lệch cỡ (`relief_build.py`), nhãn ESTIMATE (`lib/k2.js`), đạo cụ `freighter`/`crane`/`order` (`sticker-lab.js`, `stickers/`) | `scripts/k2/test_k2v.py` (kết quả ở G1-BAO-CAO §8) |
| Model viết/điều phối | phiên Claude Code này (`claude-opus-5-5` theo cấu hình phiên); tác tử tra nguồn: Sonnet (`model: sonnet` của Agent) | — |
| Model kiểm (`claude -p`, ghim) | người đọc mù + chấm "xem tiếp": `claude-sonnet-5-5`; REVIEWER lời + tiêu đề: `claude-opus-5-5`; gắn nhãn bình luận: `claude-haiku-5-5` | mỗi lượt ghi model yêu cầu + model chạy thật (`served`) ở `kiem-mu/cost.jsonl` |
| Claude Code CLI | 2.1.300 | `claude --version` |
| Giọng | như T1: ElevenLabs voice `cjVigY5qzO86Huf0OWal` (Eric), `eleven_multilingual_v2`, stability 0,5, similarity 0,75 (`k2c-t1-06/episode.yaml`) | chưa thu (sau G1) |
| three.js | 0.180.0 (`design/cong3/shared` package-lock, `npm ci` 15/10) | — |
| Nền bản đồ (cache ngoài git) | `erie` (3DEP), `sfbay` (3DEP, ppd 900), `korea` (SRTM skadi, ppd 600) — SHA từng tệp trong `$K2V_CACHE/relief/<tên>/meta.json` | dựng lại được bằng `relief_build.py` |
