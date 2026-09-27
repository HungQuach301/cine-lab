# Cổng 3 — Thiết kế (ĐÃ KHOÁ, 27/09/2026)

Chủ dự án khoá thiết kế sau đợt vá A2+ (AUTHORSHIP.md mục "Cổng 3 đợt vá A2+").

## Style frame chuẩn
**`design/cong3/v2/out/a2p/`** là style frame chuẩn của phim:
- khung tĩnh: `a_close_ida`, `b_cas_bird`, `c_s5_wide`, `c_s5_medium`, `d_s6_alley`, `e_ending` (png + mp4 1 s);
- clip đi bộ: `walk`, `walk_cas` (png + mp4 2 s);
- thử biểu cảm: `face/`.

Mọi shot sản xuất so màu, ánh sáng, chất liệu với thư mục này.

Mọi ảnh cũ **giữ làm tư liệu, không dùng làm chuẩn**:
- vòng 1: `dir-A|B|C/out*`, `KHUNG-MAU-3-HUONG.png`;
- vòng 2: `v2/out/v2/`, `v2/out/v2-dev/`;
- vòng 3: các file trực tiếp trong `v2/out/`.

## Tài liệu khoá (SHA-256 trong `LOCK-THIET-KE.sha256`)
- `bible/characters.md` v1.1 (tỷ lệ B1 cho C3)
- `bible/world-rules.md` (có dòng đá lát)
- `bible/props/gas-lamp.md` và ảnh `bible/props/img/gas-lamp.png`
- style frame `v2/out/a2p/*.png`, `*.mp4`

Kiểm lại: `sha256sum -c design/cong3/LOCK-THIET-KE.sha256` (chạy từ gốc repo).

## Mã dựng (tham khảo cho Cổng 4)
| File | Nội dung |
|---|---|
| `v2/page.js` | trang render |
| `v2/shots.js` | các shot a, b, walk, face, prop, turn |
| `v2/s5.js`, `v2/s6.js`, `v2/s1.js` | cảnh 5, cảnh 6 và kết, mở đầu |
| `v2/street.js` | bộ phố |
| `v2/char3d/` | nhân vật C′ |
| `shared/props.js` | đèn khí |
| `shared/dof.js` | DOF hậu kỳ |
| `shared/export_sidecars.js` | file đi kèm cho checks |

Mã hoá chuẩn: `v2/run_a2p.sh` (CRF 12, no-fast-pskip, deadzone 0).
