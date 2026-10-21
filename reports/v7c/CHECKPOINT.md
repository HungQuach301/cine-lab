# V7C — CHECKPOINT (nhánh thật: `claude/v7c-layout-density-qg4mng`; lệnh yêu cầu `v7c`)

## Lượt 1 (≈ 15:20 UTC 20/10)
- Nhánh từ `origin/ccr-ef2b66f0-9639kq` @317dcf51 (V7B) + `merge --no-ff` origin/main @3176ad1b + origin/claude/eloquent-dijkstra-kemr8j @4fe45ec3 (NC-GPU ⊃ NC-CPU): **0 xung đột**.
- Việc 1 (cách A = `opt.nc`): `design/k2v/tl/scenes/t3tl.js` (build → buildCore + bọc up.js khi có opt.nc), `nc/ncA.js` gọi buildCore, `nc/bake.js` nhiều lightmap theo năm (`bakes`).
  Kiểm bit: tắt → trùng byte V7B 3/3 khung (C4 f84, C3 f276, C5 f62); bật (nc {}) → trùng byte cảnh ncA NC-CPU 3/3.
- Nướng (`scripts/k2tl/v7c_nuong.sh`): b1782 → b1779 → b1781r → b2026 → b1940 đang chạy nền (≈ 30–40 phút/lightmap).
- Việc 2: đo mặt nạ ID (`design/k2v/v7c/idmask_v7c.js`, `do_bocuc.js`, `scripts/k2tl/v7c_bocuc.py`, `v7c_thu_may.py`); V7B "trước" đo xong 8 shot; đặc tả V7C `channel-k2/k2c-t3-01/v7p/mk_ep_v7c.py` (9 shot, có H2T góc thumbnail).
  Mã mới: `tl/ngua.js` (ngựa S048), `tl/duong2026.js` (cây/đèn/xe đỗ), `tl7.js camps hangLoi`, `t3tl rimPhe`.
- Ngoài git: bộ đệm `/var/tmp/cine-out/k2tl-cache` (+ `nc/tex` 54 tệp Poly Haven CC0 khớp SHA NC-CPU, `nc/bake/*`).

## CUỐI (≈ 20:30 UTC 20/10) — DỪNG chờ chủ dự án
- 5 lightmap nướng xong (8 368 s). Bản cuối cách A, 3 lượt sửa sau xem câm; master `c8bb1c02…` (ngoài git), bản xem 640×360 trong git.
- XEM CÂM P: 320 18/24 · 640 20/24. k2check 1.16.1 bản cuối: `reports/v7c/do/k2check-ban-cuoi.txt`. Chấm mù: V7C 5,17 · V7B 5,39 · A 6,39; V7C-lai 7,00 (thử).
- Báo cáo: `reports/v7c/V7C-BAO-CAO.md`.
