# V7-PILOT — CHECKPOINT (nhánh thật: `ccr-f96ee5b5-2ec2i5` — harness buộc; lệnh yêu cầu `v7-pilot`; gốc origin/ccr-6189ede9-lpjwe0 @b9cff40e)

## Xong
- Bộ đệm cảnh tl dựng lại trong container mới (`/var/tmp/cine-out/k2tl-cache`, 1,1 GB, fetch KHỚP SHA V5b-1) — `/var/tmp/cine-out/v7p/cache.sh`.
- Bộ máy timelapse `design/k2v/tl/tl7.js` + cảnh `scenes/t3tl.js`; đêm (page/water/city), đất lấn vịnh + đường băng mọc dần (terrain/heroes, cờ uRecl).
- Nội dung eo đất có nguồn: `scripts/k2tl/v7p_eo_dat.py` → `design/k2v/tl/data/eo-dat-v7.json` (trại Faden 1783 ↔ Drinkwater 1786, công sự, Línea, 14 vây, cờ, hàng rào).
- Điểm máy `design/k2v/tl/data/diem-may-v7.json`; đặc tả bản thử `channel-k2/k2c-t3-01/v7p/mk_ep_v7p.py` (8 shot, 119,1 s).

## Đang dở
- Dựng bản thử: `bash scripts/k2tl/v7p_dung.sh` (log `/var/tmp/cine-out/v7p/dung.log`).

## Tệp ngoài git
| Đường dẫn | Tái tạo |
|---|---|
| /var/tmp/cine-out/k2tl-cache | `/var/tmp/cine-out/v7p/cache.sh` (= bảng G1b CHECKPOINT; cần `git fetch origin v5a main`) |
| /var/tmp/cine-out/k2c-t3-v7p, /var/tmp/cine-out/hero/k2c-t3-v7p-* | `bash scripts/k2tl/v7p_dung.sh` |
