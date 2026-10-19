# V7B — CHECKPOINT (nhánh thật: `ccr-ef2b66f0-9639kq`; lệnh yêu cầu `v7b`)

## Lượt 1 (≈ 11:40 UTC 19/10)
- Đã merge `origin/k2c-t3-kl42` (không xung đột; lời v4.2 SHA 51d1c773… khớp).
- Mã mới/sửa: `design/k2v/tl/phe.js` (cờ tàu + viền phe), `props.js` (mẫu cờ Red Ensign 1707, cờ hải quân TBN 1701–85, cờ trắng Pháp; hạ–kéo), `city.js` (màu/kiểu có nguồn, LOD gần chỉnh được),
  `page.js` (bfile, cityOpt, classMask), `people.js`/`layers.js` (người cúi), `scenes/t3tl.js` (cờ, viền, Faden phủ, thùng hàng, phố trước 1704, lớp đo khối), `scripts/k2tl/render.js` (--classmask),
  `scripts/k2tl/v7b_mau_nha.py`, `v7b_faden.py`, `v7b_dung.sh`, `channel-k2/k2c-t3-01/v7p/mk_ep_v7b.py` + đặc tả sinh ra.
- Đang dựng: biến thể C1-a (`bash scripts/k2tl/v7b_dung.sh a render ghep xem`). Sau đó: C1-b (chỉ C1 dựng lại), đo, xem câm, báo cáo.
- Ngoài git: bộ đệm `/var/tmp/cine-out/k2tl-cache` (tái tạo: `bash scripts/k2tl/v7p_cache.sh` → `v7b_mau_nha.py` → `v7b_faden.py`).
