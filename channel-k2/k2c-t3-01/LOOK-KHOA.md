# LOOK KHOÁ — K2C-T3-01 Gibraltar (phiên ANIMATIC-T3, 21/10/2026)

> Tệp này chép **nguyên văn** quyết định look của chủ dự án (21/10/2026 07:05) và ghi thông số để tái lập. Phiên P sau ghi vào Kinh thánh §14.7.
> Nhánh tạo tệp: `ccr-d189108f-6mcz9k` (harness buộc; lệnh gọi tên `k2c-t3-animatic`), gốc V7C `47a0f55a` + merge `origin/main` `bc7e96d1`.

## 1. Quyết định của chủ dự án (nguyên văn, 21/10/2026 07:05)

QUYẾT ĐỊNH LOOK (chủ dự án 21/10 07:05 — chép NGUYÊN VĂN vào LOOK-KHOA.md, phiên P sau sẽ ghi Kinh thánh §14.7):
- LOOK-1 Bề mặt, ánh sáng, màu: cách A (`opt.nc` + lightmap Cycles nướng theo mốc + vân CC0 + bụi + nước + sương) cho mọi cảnh; mức tham chiếu = reports/nc-cpu/khung/A/cong-*.jpg. Không dựng cả tập bằng Cycles, không Eevee. Bão hoà trung vị ≥ 0,40 (§14.4).
- LOOK-2 Bố cục toàn cảnh, cảng, phố, vây hãm = "khung lai" (tham chiếu reports/v7c/khung/lai/cong-*.png): có dải trời + sương 8–20 % khung, nhìn xuống 12–25°, MỘT tiêu điểm rõ ở vùng 1/3; Rock/biển/hạm đội là sân khấu. Bỏ ngưỡng "nội dung ≥ 50 %": % nội dung dưới chân trời chỉ ghi để theo dõi. Khung chặt nhìn gần chỉ cho cận phố/người/cờ có vai truyện.
- LOOK-3 Chiến sự đêm có lửa (13/9/1782): theo reports/v7c/khung/cong-bo-chien-su.png (H2T, góc thumbnail).
- LOOK-4 Lỗi KHÔNG được mang theo: lều trắng xếp ô như bàn cờ; viền xanh nhạt quanh bờ nước; mảng bọt trắng hình chữ nhật gần bờ; Rock bị cắt mép khung; khung nhìn thẳng xuống như bàn cờ (V7C giây 60 và 100); khung chỉ còn mặt nước (V7C giây 68–76); cảnh 2026 mở đầu mất Rock (V7C giây 4).
- LOOK-5 Thứ tự ưu tiên khi xung đột: người xem hiểu được (kể cả tắt tiếng) > đẹp như phim > chỉ số đo.
- Tham chiếu ngữ pháp máy đã kiểm: toàn cảnh có Rock + hạm đội theo V7B biến thể a (giây 68–76: hạm đội phong toả đọc rõ, Rock giữa khung); mở đầu theo V7C (pin nổi cháy + Rock rõ trước giây 30); giữ shot H2T góc thumbnail.

## 2. Khung tham chiếu (SHA-256)

| Vai | Tệp | SHA-256 |
|---|---|---|
| LOOK-1 mức bề mặt/ánh sáng/màu | `reports/nc-cpu/khung/A/cong-vay-ham.jpg` | `10041633972713dcd4c16cd6cd8ac91d2f55c8d87a366609fa57b07413a46dd0` |
| LOOK-1 | `reports/nc-cpu/khung/A/cong-cang.jpg` | `bf84359616cfde1a072c4265f47edad852e65f99fcccf2ff7f72c70696616c3f` |
| LOOK-1 | `reports/nc-cpu/khung/A/cong-pho-day.jpg` | `02fce3689ad617aea7dcabcff6a8dce94297a398ad9ef073710371135e05e889` |
| LOOK-1 | `reports/nc-cpu/khung/A/cong-hero.jpg` | `f2fe32571b7674a11cfb54df599ecc4dfd671ac9055c7075d96c586363960792` |
| LOOK-1 | `reports/nc-cpu/khung/A/cong-toan-canh.jpg` | `32a726645a57a5e04ed8c393e68f1ddb74539c1cf834d6dc8ebdbee3577fbf49` |
| LOOK-1 | `reports/nc-cpu/khung/A/cong-bo-chien-su.jpg` | `0d6782e49092ab9a167679dc82a6b9b0afde2c2c0066f81b03edb00b25d58935` |
| LOOK-2 khung lai | `reports/v7c/khung/lai/cong-vay-ham.png` | `bf866b659d2cf550d9066b0104147900e841a44ca568542fc42bfd2911896665` |
| LOOK-2 khung lai | `reports/v7c/khung/lai/cong-cang.png` | `99a55c580c00525f4d4b88e8886e6f73ef9399cb0d1399b836b8d144961bbff2` |
| LOOK-2 khung lai | `reports/v7c/khung/lai/cong-pho-day.png` | `d513a1c55faf87f46827a1c64e00873fbf7fa514e614e2a99693c55667ec7fdb` |
| LOOK-3 đêm lửa (H2T, góc thumbnail) | `reports/v7c/khung/cong-bo-chien-su.png` | `2ebf2636246ee81efacb84e6dbf67b7f0860fb5332c49bd9699b713d520925e2` |

Lưu ý khi dùng tham chiếu (đọc từ chính các khung, không phải quyết định mới):
- `lai/cong-vay-ham.png` là mẫu **bố cục** (chân trời, sương, góc xiên). Chính khung đó có lều trắng xếp ô như bàn cờ và không thấy Rock — hai điều LOOK-4/LOOK-2 cấm. Animatic lấy bố cục, không lấy hai lỗi này.
- `nc-cpu/khung/A/cong-toan-canh.jpg` có viền đỏ quanh tàu (đã bỏ từ V7C, `rimPhe: ['es']`) và dải nước nông sáng bám bờ phía nam. Animatic lấy mức bề mặt/ánh sáng, không lấy viền tàu Anh.

## 3. Thông số tái lập

### 3.1 Cách A (LOOK-1) — `design/k2v/tl/scenes/t3tl.js` `build()` khi có `opt.nc`
- Bọc: `nc/up.js` `preBuild → buildCore → postBuild` (như `nc/ncA.js` của NC-CPU). Không khai `opt.nc` → đường V7B (không dùng ở T3).
- `opt.nc` mặc định T3 (mọi shot animatic):
  - `bakes: [{dir, wY: [năm đầu, năm cuối], fire?}]` theo §3.2. Ngoài mọi cửa sổ → lightmap gần nhất (`nc/bake.js`).
  - `bushes`: bật (mặc định). Mật độ trước 1900 = 0,45 × hiện nay (bậc 5 tạm, §14.4). Ẩn trong dải trại và nền đô thị theo năm.
  - `water`: bật (sóng 5 hướng, dải nông/bọt theo bờ của NĂM; `tCoast` 1940 / 2026 đổi ở 1942,5).
  - `haze`: `{ s: 1/16000, c: [0.66, 0.74, 0.84] }` (sương e^(−σd), σ = 1/16 km).
  - `tex`: bật; `nk` 0,55 (độ mạnh pháp tuyến vân).
- Vân CC0: 18 tấm Poly Haven (danh sách + SHA-12: `reports/nc-cpu/RIGHTS-NC.md`); tải lại bằng `scripts/k2tl/anim_tex.py` vào `$K2TL_CACHE/nc/tex/`, kiểm SHA từng tệp.

### 3.2 Lightmap nướng theo mốc (Cycles CPU một lần/mốc; `scripts/k2tl/anim_nuong.sh`, kế thừa `v7c_nuong.sh`)
Hộp E −3000…1000, N −3000…3500; 3 m/texel; 24 spp; albedo nền 4 m cả hộp + 1 m phố. Kênh R = trời có che khuất + nảy; G = nảy nắng; B = lửa; A = cao độ.

| Lightmap | Mốc nướng | Cửa sổ năm dùng (`wY`) | Trạng thái |
|---|---|---|---|
| b1704 | 3/8/1704 12:00 | 1300 → 1779,0 | phố 1704 (lớp tái dựng 1705) |
| b1779 | 15/1/1780 12:00 | 1779,0 → 1781,278 | phố 1779–81 nguyên, trại + công sự |
| b1781r | 1/7/1781 12:00 | 1781,278 → 1782,5 | vùng THE RUINS đã sập |
| b1782 | 13/9/1782 15:30 + lửa 10 pin nổi | 1782,5 → 1783,6 | trạng thái NC-CPU |
| b1900 | 1/6/1910 12:00 | 1783,6 → 1938 | đất trung lập, hàng rào 1909, La Línea theo năm xây |
| b1940 | 1/6/1940 11:00 | 1938 → 1946 | ghost 1943 + đường băng |
| b2026 | 19/10/2026 12:00 | 1946 → 2030 | nhà 2026 có vật liệu |

Giây nướng thật từng lightmap ghi ở `reports/animatic-t3/ANIMATIC-BAO-CAO.md` và `reports/animatic-t3/do/nuong-*.json`.

### 3.3 Chỉnh màu (giữ nguyên đường ống V7B/V7C/NC-CPU)
- Tích luỹ SPP có jitter → tone ACES → LUT `k2-a-thep-lanh.cube` (`lutMode` 1, `lutK` 1,0) → V6 grade `[1.0, 0.35, 0.6]` → vibrance 0,78 (`GRADE.vib` của t3tl) → vignette 0,16 → hạt cố định. Exposure 1,0.
- Ánh sáng V6: `sunK` 1,1, `hemiK` 1,2; `LOOK` t3tl: `hemiI` 0,74, trời `#a9c0e2`, đất `#b0845a`, chân trời `[0.30, 0.52, 0.90]`.
- Mục tiêu: bão hoà trung vị ≥ 0,40 (đo 640×360, cắt y 60–300, như V7C).

### 3.4 Khung lai (LOOK-2) — thông số mẫu
- Máy xiên có chân trời: **nhìn xuống 12–25°** (đo tại tâm khung); **dải trời + sương 8–20 % chiều cao khung**; AGL 150–450 m (cảng/phố 150–300 m, toàn cảnh 250–450 m); FOV dọc 34–46° (≈ 27–37 mm FF).
- MỘT tiêu điểm (vật hero có vai truyện) ở 1/3 trái/phải hoặc giao điểm 1/3; Rock + biển + hạm đội là nền sân khấu, Rock không bị cắt mép khung.
- Khung V7C-lai không ghi máy trong git (chỉ có ảnh). Thông số máy thật của từng shot animatic ghi trong `channel-k2/k2c-t3-01/animatic/bang-shot.md` và log shot (góc nhìn xuống, AGL, FOV, % trời đo trên khung).
- Khung chặt (cận) chỉ khi có vai truyện: cận phố, người, cờ.

### 3.5 Đêm lửa (LOOK-3)
- Điểm máy N2r (= X01/X08): `[-1950, 25, -1150] → [-600, 180, -1600]`, FOV 46°; lửa pin nổi theo `design/pt/cpu/fires-1782.json` (kênh B của b1782, `wY` 1782,70046–1782,703082, k 1,5); 13/9/1782 17:55 → 14/9 02:30.

### 3.6 LOOK-4 — cách kiểm
Soi 1 khung/2 s toàn tập (640×360); mỗi lỗi ghi shot + giây + cách sửa trong `reports/animatic-t3/ANIMATIC-BAO-CAO.md` §LOOK-4.
