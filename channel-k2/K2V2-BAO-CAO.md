# Kênh 2 — Bộ hình k2v nâng cấp V2: bản đồ nổi + sticker (phiên V2, 14/10/2026)

Nhánh `k2-visual2` (từ `origin/main` @ `d3beb5f`; checks 1.10.2, LOCK `c598467f…`).

**Phạm vi sửa:** `design/k2v/`, `scripts/k2/`, `channel-k2/k2v2-mau/` (mới), `channel-k2/K2V2-BAO-CAO.md`, `RIGHTS.md`, `assets/k2/archive/` (thêm 1 ảnh tài sản công).

**Không đụng tới:**
- Không sửa `checks/`, không đọc mã trong `checks/`; chỉ chạy công cụ của K.
- Không sửa tệp của tập: `design/ll-hero/k2g01.js` và `k2c106.js` chỉ được nạp qua `?rx=`.
- Không gọi công cụ tạo ảnh/video AI ngoài.

**Kinh thánh kênh 2:** tệp `claude/CINE-LAB-BIBLE-KENH2.md` nằm trong Project, phiên này không đọc được (không có trong repo, không có trên Drive). Phiên làm theo đặc tả chi tiết trong lệnh giao việc. Mục cần đối chiếu nằm ở §9.

## 0. Tóm tắt
- **Module mới `relief/map`:** bản đồ địa hình nổi thật, dựng từ DEM USGS 3DEP 1″ ghép ở ~140–185 m/px, sắc nét ở tầm vùng 300–650 km.
  - Hai bảng màu tự nhiên ↔ sepia, chuyển dần trong shot.
  - Vùng nổi theo mã màu từng phía (khối nhô có tường, viền sáng, bóng đổ).
  - Máy quay trượt liên tục (spline, không dừng ở mốc).
  - Tuyến nét liền/đứt chảy, hoặc "vệt" bám vật đang đi; vòng sáng; chồng xu/cột tỷ lệ thật có neo `col:<id>`.
- **Thư viện sticker một phong cách** (viền trắng + bóng đổ + bóng tiếp đất):
  - 16 vật: 4 vật dựng lại từ mô hình 3D của kênh (lò cao, xưởng, nhà, phố), 12 vật mới (mỏ, tàu, thuyền kênh, xu, chồng xu, văn bản, ngân hàng, cờ trung tính, xe hàng, bao, thùng, núi).
  - 8 vai nhân vật A-lite thay được đạo cụ. Phần nhân vật ≈ 6–8 % công sức, dưới trần ~10 %.
  - API đặt sticker bám toạ độ, xuất hiện theo mốc lời.
- **Bảng điểm hai phía** + biểu tượng góc (component dùng lại). Nhãn số tự né vật thể (BAI-HOC-K2 K11).
- **Cuộn shot mẫu 44 s** (5 đoạn: móc 15 s · hành trình 10 s · số liệu 8 s · chân dung 5 s · bảng điểm 6 s).
  - Đề tài trung tính: kênh Erie vs Main Line PA, 1825–1834. Mọi số có nguyên văn nguồn công khai (`claims.md`).
  - Tờ khung 540p trước, rồi 1080p SPP4.
  - **Lệch lệnh:** 1080p dựng **hai lần**, vì có một lượt sửa sau chấm mù vòng 1 (§5).
- **Chấm mù 3 người** (`claude-sonnet-5-5`, cặp mới vs khung T1 cùng loại):

  | Cặp | Vòng 1 (tay nghề T1 → mới) | Vòng 2, sau một lượt sửa |
  |---|---|---|
  | P1 bản đồ móc | 5,67 → **8,0** | 6,0 → 7,33 |
  | P2 hành trình | 7,33 → 6,0 (**T1 thắng 3/3**) | 7,0 → 7,0 (**mới thắng 3/3**) |
  | P3 số liệu | 4,67 → 7,0 | 4,33 → 6,67 |
  | P4 chân dung | 6,0 → 6,0 | 5,33 → 6,0 |
  | P5 bảng điểm | 3,67 → 7,0 | 4,0 → 7,0 |

  - Vòng 2: mới được chọn **15/15**; tay nghề trung bình mới **6,8** vs T1 5,33.
  - **Mục tiêu tay nghề ≥ 8: CHƯA ĐẠT.** Chỉ P1 đạt 8,0, ở vòng 1. Nguyên nhân còn lại và đề xuất ở §5.3.
- **Giờ render:**
  - Cảnh 3D 1080p SPP4 **3,81 s/khung đồng hồ** (3 tiến trình). T1 là 1,86 s/khung, tức chậm hơn **≈ 2,0 lần**.
  - Toàn bộ 4,19 s/khung (T1 2,47 s/khung, ≈ 1,7 lần).
  - Đề xuất giảm thời gian ở §4.
- **Luật K (1.10.2) trên cuộn:** Q33 ĐẠT; Q32 ĐẠT; Q34(c) **số neo 3D 100 %**; Q34(a)(b) trượt vì shot mẫu không có lời (như phiên V).
  - Mép 48 px: 0 vi phạm; chữ < 30 px: 0; tương phản < 4,5: 0.
  - `checks/lock.py --verify` **KHỚP** (`c598467f…`).
- **Chi phí API:** **$1,84 / trần $10**. ElevenLabs $0. YouTube API 0 lượt.

## 1. Đề tài mẫu và nguyên tắc nguồn
- **Đề tài:** kênh Erie (New York, 1825) và Main Line of Public Works (Pennsylvania, 1834).
- **Vì sao chọn:**
  - Lịch sử hạ tầng, không có phe, không có người còn sống.
  - Không nằm trong hàng đợi kênh 2. `market-k2/REPORT.md` không có video đối thủ nào về "canal"/"Erie".
  - Bản đồ nổi **tự nó cho thấy cơ chế**: khe Mohawk thấp xuyên vùng đồi, so với các dãy núi gấp nếp của Pennsylvania. Đây là câu chuyện mà hình phải kể được, không phải trang trí.
- **Nguồn số:**
  - Mọi số và câu trên hình có nguyên văn nguồn công khai trong `channel-k2/k2v2-mau/claims.md`: LOC, NPS, NPS ALPO, ECNHC (đối tác NPS), NYS Archives Partnership Trust, The Met.
  - Tác tử tra cứu đã đọc trang gốc. Số chỉ thấy qua kết quả tìm kiếm thì **không dùng**; ví dụ câu "$100 → $10" của NYSM và Britannica.
- **Học công thức, không học hình:**
  - Công thức lấy từ thể loại: bản đồ nổi, sticker viền trắng, máy trượt, vùng theo phe, bảng điểm.
  - Không mở, không tải, không dùng hình, thumbnail hay câu chữ của kênh nào.
  - Mọi tài sản đều tự dựng (three.js, vector), hoặc là tài sản công: USGS 3DEP, Natural Earth, The Met Open Access.

## 2. Module và API (chi tiết: `design/k2v/README.md` mục E)
### 2.1 `relief/map` — bản đồ địa hình nổi (`design/k2v/relief.js`, nền `scripts/k2/relief_build.py`)
- **Nền bản đồ:**
  - DEM **USGS 3DEP 1″** (tài sản công), ghép 78 ô, hạ còn 6″ (~140–185 m/px). Bản `erie`: 82°W–71°W × 39°N–46°N, 6600×4200 px, lưới độ cao 825×525. Dựng mất ≈ 2,5 phút.
  - Tô bóng nhiều hướng (315/270/360/225°, mặt trời 45°).
  - Nước, sông, ranh bang/tỉnh lấy từ Natural Earth 10m.
  - **Sắc nét ở tầm vùng:** khung 300–650 km. Khe Mohawk, Finger Lakes, dãy gấp nếp Pennsylvania, Adirondack, Catskill đều đọc được ở 540p.
- **Hai bảng màu:**
  - TỰ NHIÊN (hiện tại): màu theo độ cao × bóng, nước có dải nông.
  - SEPIA (quá khứ): giấy, mực nâu, bờ nước kẻ nét kiểu bản đồ khắc.
  - Chuyển dần trong shot bằng `sepia: [t0, t1]`. Chip năm lớn `p.year` đánh dấu mốc quá khứ.
- **Vùng nổi theo mã màu từng phía** (`regions`, ≤ 3 vùng):
  - Khối nhô `lift` km, tô bằng phép nhân để vân địa hình vẫn còn.
  - Có tường tối, viền sáng kiểu sticker, bóng đổ Đông Nam.
  - Tường được làm mượt bằng lấy mẫu mip 1,6 trong vertex shader, để khỏi răng cưa theo lưới.
- **Máy quay trượt liên tục:** spline Hermite qua các mốc `{lon, lat, dist km, tilt, head, mm}`. Máy không dừng ở mốc giữa và giữ vận tốc ở hai đầu.
- **Cung đường:**
  - Nét liền hoặc nét đứt "chảy"; vẽ dần theo `draw`, hoặc theo vật đang đi bằng `trail`.
  - Độ dày tính theo px của khung 1080p, nên giữ nguyên khi máy zoom.
  - `pts` trộn được địa danh, toạ độ và đoạn đường Natural Earth.
- **Vòng sáng:** `rings`, 3 vòng lan, cỡ tính theo px.
- **Điểm neo:**
  - Địa danh.
  - `st:<id>`: sticker đứng yên (`pins`) và sticker đi theo tuyến (`walkers`).
  - `col:<id>` (đỉnh), `colL/colR:<id>` (hộp chiếu): chồng xu/cột.
  - `rt:<id>`: đầu tuyến.
- **Tone map riêng** (`export const TONE`, đọc trong `page.js`): giữ đúng bảng màu bản đồ. ACES làm giấy sepia xỉn và đổi sắc. Các module khác vẫn dùng ACES như cũ.

### 2.2 Sticker vật — `design/k2v/stickers/` (16 vật + 8 vai), `scripts/k2/lib/sticker.js`, `design/k2v/sticker-lab.js`
- **Một phong cách cho mọi sticker** (`STK.style`): viền trắng dày ≈ 6 % cạnh và bóng đổ mềm lệch xuống phải. Trên bản đồ có thêm bóng tiếp đất dưới chân.
- **16 vật**, render toon 3 nấc ở góc 3/4 cố định:
  - Từ mô hình của kênh: `furnace` (lò cao K2G-01), `factory` (xưởng K2G-01 + ống khói mới), `house` và `town` (nhà K2C-T1-06).
  - Vật mới tự dựng: `mine`, `ship`, `boat` (thuyền kênh), `coin`, `coins`, `document`, `bank`, `flag` (cờ trung tính, không biểu tượng), `wagon`, `sack`, `barrel`, `mountain`.
- **Tái dựng và tờ rà:**
  - Dựng lại: `node scripts/k2/stickers_build.js [tên…]` (≈ 11 s cho cả thư viện).
  - SHA từng tệp: `stickers.json`.
  - Tờ rà trên cả hai bảng màu: `channel-k2/k2v2-mau/stickers-sheet.jpg`.
- **API đặt sticker** (lớp 2D, `p.stickers`):
  - Bám neo toạ độ bản đồ (`st:<id>` khai ở `opt.pins` / `opt.walkers`).
  - Xuất hiện theo mốc lời: `at`/`out` là giây hoặc `"@từ"`, qua `prep.py` như mọi mốc kênh 2.
  - Vào có bật nảy (back-out 0,42 s), ra co lại.

### 2.3 Nhân vật A-lite (phần nhân vật ≈ 6–8 % công sức phiên)
- **8 vai sticker phẳng:** worker, merchant, banker, soldier, official, engineer, farmer, sailor.
  - Vẽ vector; không mặt chi tiết, không diễn xuất, không khớp miệng.
  - Nhận ra bằng 1–2 đạo cụ thay được: mũ (`STK.HATS`, 10 loại) và vật cầm tay (`STK.HANDS`, 15 loại). Ví dụ `{role: farmer, hand: wheat}`.
- **Hoạt ảnh tối thiểu:**
  - Đi theo tuyến (`walkers`), nhún theo nhịp (`walk`), tự lật theo hướng đi.
  - Nảy nhẹ khi xuất hiện, co lại khi biến mất.
- **Chân dung tài sản công:** dùng lại `photo/print` (Ken Burns có thị sai, chú thích tên · năm · nguồn). Mẫu: DeWitt Clinton, Samuel F. B. Morse 1826, The Met Open Access.
- **Công sức:**
  - Phần nhân vật gồm `STK.char`, 8 vai, đạo cụ, lật/nhún. Tổng ≈ 100 dòng trong `sticker.js`, ≈ 6–8 % thời gian phiên, dưới trần ~10 %.
  - Không có cổng kiểm nhân vật riêng.

### 2.4 Số liệu trên bản đồ (Q34(c))
- `opt.cols: [{id, at, kind: coins|bar, n|v, unit, t, r}]`:
  - Mỗi đồng xu là một đơn vị khai rõ, nên chiều cao chồng **đúng tỷ lệ thật**. Xu rơi lần lượt.
  - Mẫu: 10 đồng (cước xe ngựa) so với 1 đồng (1/10 bằng kênh). Chú thích hình ghi "Each coin is one tenth of the wagon cost".
- **Nhãn số:**
  - Nhãn số bám `col:<id>`, có `num` và `kind: actual`.
  - Nhãn `side: 'auto'` né hộp chiếu của chính chồng xu và các sticker (BAI-HOC-K2 K11). Lỗi "nhãn đè khối" của T1 F03 đã được sửa ở mức công cụ.
- **Luật K Q34(c) 1.10.2 trên cuộn mẫu:** "số neo 3D **100 %**, chỉ card 0 % (2 số)".

### 2.5 Bảng điểm (component dùng lại)
- `p.score.corner`: biểu tượng góc gồm sticker phía, tên và điểm tăng theo mốc. Có `title` để giải thích con số (vd. "Rows won:").
- `p.score.board`: bảng tổng kết hai phía.
  - Mỗi hàng có biểu tượng sticker; ô thắng được khoanh viền màu phía thắng. Hàng không có `win` thì không khoanh (vd. "Length" không phải lợi thế rõ ràng).
  - Các hàng hiện lần lượt.
  - `align: right` + `w` để lộ bản đồ thật bên trái (nền làm tối, không làm mờ).
- **Thay cho thẻ "TO RECAP" phẳng** (BAI-HOC-K2 K11: thẻ tóm tắt phải có biểu tượng cho từng mục).

### 2.6 Sửa chung (dùng cho mọi tập kênh 2, chỉ thêm, không đổi hành vi cũ)
- **`scripts/k2/hero.js`:** gặp "Shader Error" thì **dừng có mã lỗi**, không dựng tiếp.
  - Nháp V2 từng ra khung thiếu địa hình mà không báo: chú thích `//` trong shader viết một dòng đã nuốt phần còn lại của `main()`.
  - Đã thêm phép kiểm `test_v2_shader_no_line_comment`.
- **`scripts/k2/render.js`:** nạp `lib/sticker.js` và ảnh `stk:<tên>` (PNG).
- **`scripts/k2/lib/k2.js`:** thêm `p.stickers`, `p.score`, `p.year`, `side: 'auto'` (né `LL.occ`).
  - Dòng nguồn đổi sang màu sáng hơn `#D6DDE4`. Lý do: 3/3 người chấm nêu "dòng nguồn xám, khó đọc trên điện thoại". Thay đổi này **áp cho mọi tập kênh 2 dựng sau**.
- **`scripts/k2/vshot.py`:** `--par N` dựng N cảnh 3D song song; ghi đồng hồ thật.
- **`scripts/k2/prep.py`:** `relief/*` có loại `map`; `design/k2v/relief.js` vào dấu tươi (stamp) cảnh.
- **`design/k2v/page.js`:** module có thể khai `TONE`; thêm tông `map`.
- **Kiểm thử:** `scripts/k2/test_k2v.py` **13/13 ĐẠT** (thêm 4 phép: loại relief, SHA thư viện sticker, điều kiện Q34(c) của cuộn, cấm `//` trong GLSL).

## 3. Cuộn shot mẫu (`channel-k2/k2v2-mau/K2V2-reel.yaml`, 44 s, 1080p24 SPP4)
| Đoạn | Thời lượng | Nội dung | Module |
|---|---|---|---|
| H móc | 15 s | Bản đồ hiện tại (tự nhiên) → khe Mohawk sáng lên → chuyển sepia + chip "1825" → NY (lục lam) và PA (hổ phách) nổi lên → tuyến kênh nét đứt Buffalo → Albany → Hudson; vòng sáng Buffalo/Albany | relief |
| J hành trình | 10 s | Thuyền kênh + người kéo thuyền (sticker) đi theo tuyến Buffalo → Albany → New York; vệt tuyến bám thuyền, tuyến kế hoạch nét đứt; nông dân cầm lúa mì ở Genesee Valley, thương nhân ở New York; nhãn 4 đầu mút | relief + sticker + nhân vật |
| N số liệu | 8 s | Chồng 10 xu (cước xe ngựa $90–125/tấn) và 1 xu (1/10 bằng kênh) rơi lần lượt trên bản đồ gần Buffalo; sticker xe hàng, thuyền; chú thích "Each coin is one tenth of the wagon cost" | relief cols |
| P chân dung | 5 s | DeWitt Clinton (Morse 1826, The Met Open Access), Ken Burns có thị sai; chú thích tên · năm · nguồn | photo/print |
| S bảng điểm | 6 s | "Two routes west": Opened 1825/1834 · Length 363/394 mi · Climb 568/2,102 ft · Cost $7.1M/$16.5M; huy hiệu góc "Rows won: NY 3 · PA 0"; bản đồ hai bang nổi bên trái | score + relief |

- **Video (ngoài git, không LFS, chỉ ghi SHA):**
  - Bản cuối `/var/tmp/cine-out/k2v-shots/K2V2-reel/shot.mp4`: 1920×1080, 24 fps, 44,0 s, 102,5 MB, SHA-256 `71c7c287768ae1b338d9b5e4b1a0953ee448d2fc6b698c361c41490ebb637196`.
  - Bản vòng 1, đã bị ghi đè: SHA `5f26f99f47bcdda841e9cbf92f98266f7e41c20cee17e412c72373d63c63b15d`.
  - Tệp > 30 MB nên không gửi qua giao diện. Dựng lại được bằng `vshot.py … --spp 4 --par 3`; tài sản tải lại bằng `relief_build.py` và `stickers_build.js`.
- **Tờ khung** (`channel-k2/k2v2-mau/`):
  - `to-khung-540.jpg`: nháp 540p sau lượt sửa, trước lần chỉnh máy cuối của J/S.
  - `to-khung-1080.jpg`: bản cuối.
  - `stickers-sheet.jpg`: thư viện sticker.
- **Đặc tả và số đo kèm theo:** `K2V2-reel.yaml`, `K2V2-reel.timeline.json`, `claims.md`, `measure-*.json`, `relief-erie-meta.json`.

## 4. Số đo
### 4.1 Giờ render / khung so với T1 (K2C-T1-06)
| | V2 (cuộn mẫu, 1080p SPP4, 3 tiến trình trên 4 vCPU) | T1 (bản phát hành, 1080p SPP4) |
|---|---|---|
| Cảnh 3D, đồng hồ thật / khung | **3,81 s** (4 025 s / 1 056 khung, lượt cuối; lượt 1: 3,69 s) | **1,86 s** (11 giờ 41 phút / 22 584 khung) |
| Mỗi tiến trình / khung | relief 7,2–13,0 s; photo 6,5 s | map 2,9; corner 3,5–5,9; photo 3,4–4,2 s (G1b) |
| Lớp chữ 2D / khung | 0,18–0,23 s | 0,17–0,29 s |
| Toàn bộ đồng hồ / khung | **4,19 s** (4 425 s, gồm lớp chữ + ghép) | **2,47 s** (≈ 15,5 giờ) |

- **V2 chậm hơn T1 ≈ 2 lần** ở cảnh 3D.
- **Nguyên nhân:**
  - Lưới địa hình 433 nghìn đỉnh có lấy mẫu mặt nạ trong vertex shader.
  - Hai texture màu 6600×4200 kèm mặt nạ vùng có mipmap.
  - Đoạn hành trình J có máy rộng (đến 660 km), nhiều điểm ảnh địa hình nên chậm nhất (13,0 s/khung mỗi tiến trình).
- **Ước cho tập 15 phút** nếu 50 % thời lượng dùng relief: 10 800 khung × 3,81 s ≈ **11,4 giờ** cho phần relief.
- **Đề xuất giảm thời gian** (chưa đo, cần thử ở V3):
  - Relief dùng SPP2: hình chủ yếu là texture, ít cạnh hình học, nên ít cần khử răng cưa.
  - Lưới 1/2 ở khung rộng.
  - Texture 4096 cho khung > 500 km.
- **Đã giảm trong phiên:** 5 → 1,9 s/khung ở 540p, nhờ lưới thưa hơn và thoát sớm shader khi chưa có vùng.

### 4.2 Độ dài shot trung bình (ASL)
- **Theo shot khai:**
  - Cuộn mẫu: 5 shot / 44 s = **8,8 s**.
  - T1: 103 shot khai / 941 s = **9,14 s**.
- **Theo bộ dò cắt cảnh** (ffmpeg `scene > 0,30`, ảnh 320 px), cùng một bộ dò cho cả hai:
  - T1: 72 cắt → 73 đoạn → ASL ≈ 12,9 s.
  - Cuộn mẫu: **0 cắt**, vì giữa các đoạn là mờ đen 6 khung, bộ dò không bắt được mờ/hoà tan. Số T1 cũng bỏ sót hoà tan, nên hai số dò **không so được với nhau**.
  - Kết luận: dùng ASL theo khai báo.
- **Ghi chú:** bên trong một shot relief, máy luôn chuyển động và các yếu tố (vùng, tuyến, sticker, nhãn) vào lần lượt mỗi 1–3 s, nên nhịp thị giác dày hơn số cắt.

### 4.3 Chữ và mép (lớp 2D)
- 1080p: **0** mẫu chữ < 30 px, **0** mẫu tương phản < 4,5.
  - Ở nháp lượt sửa có 10 mẫu "Rows won:" đạt 3,86 do chữ nằm trần trên bản đồ. Đã đặt vào viên nền đặc trước khi dựng 1080p.
- Mép khung (`scripts/k2/edge_check.py`, 48 px): **0 vi phạm** ở 5 đoạn; mép gần nhất 62 px.

## 5. Chấm mù (3 người chấm, model ghim)
- **Giao thức** (`channel-k2/k2v2-mau/blind_v2.py`), như `k2v-mau/blind_v.py` và `k2c-t1-06/blind_g2.py`:
  - `claude -p --model claude-sonnet-5-5`, chỉ công cụ Read, thư mục tạm trống.
  - 3 vai chấm: người xem, đạo diễn motion/3D, biên tập tài liệu.
  - Thang tuyệt đối: 5 = faceless thường.
  - Cặp và mốc giây **khai trước khi dựng 1080p**. Thứ tự X/Y trộn bằng hạt giống cố định 20261014.
  - Khung T1 trích từ master phát hành `release-k2c-t1-06-v1` (SHA `4f2d280b…`), tại giây của bộ Q27 G2.
- **Model thực chạy:** `modelUsage` mỗi lượt gồm `claude-sonnet-5-5` (sinh câu trả lời) và một lượt phụ rất nhỏ của CLI bằng `claude-haiku-5-5`.
  - Đo thử một lượt: haiku 1 174 token vào / 14 token ra, $0,0001; câu trả lời là của sonnet.
  - Phiên V/G2 không thấy lượt phụ này. Có thể do phiên bản CLI hiện tại (2.1.299).

### 5.1 Vòng 1 (1080p lần 1)
| Cặp (T1 ↔ mới) | Tay nghề T1 → mới | Đọc chữ mới | Rõ ý T1 → mới | Chọn | Cờ mới |
|---|---|---|---|---|---|
| P1 F08 bản đồ Minneapolis ↔ móc 13,0 s | 5,67 → **8,0** (8/8/8) | 8,0 | 5,0 → 9,0 | mới 3/3 | — |
| P2 F12 địa cầu Texas ↔ hành trình 21,0 s | 7,33 → 6,0 | 6,33 | 7,0 → 5,33 | **T1 3/3** | confusing |
| P3 F03 khối 13 % ↔ chồng xu 31,0 s | 4,67 → 7,0 | 8,0 | 3,33 → 8,0 | mới 3/3 | — |
| P4 F01 ảnh lưu trữ ↔ chân dung 36,0 s | 6,0 → 6,0 | 6,0 | 7,67 → 8,0 | mới 2/3, hoà 1 | flat_slide_look |
| P5 F09 TO RECAP ↔ bảng điểm 42,5 s | 3,67 → 7,0 | 7,33 | 4,67 → 8,33 | mới 3/3 | cluttered |

### 5.2 Lượt sửa (một lượt) và vòng 2
- **Sửa theo góp ý ≥ 2/3 người chấm:**
  - **J:**
    - Khung rộng thấy trọn tuyến, nhãn 4 đầu mút từ giây thứ 3.
    - Tuyến "vệt" dày 11 px bám thuyền; tuyến kế hoạch nét đứt.
    - Khối nổi NY hạ còn 2,5 km, bỏ "gai" ở bờ hồ mà người chấm gọi là vệt lỗi.
    - Sticker có bóng tiếp đất.
  - **N:**
    - Chú thích giải thích tỷ lệ xu, thay cho dòng nguồn.
    - Thuyền đặt cạnh đồng xu của nó.
    - Nhãn né hộp chiếu chồng xu.
  - **P:** máy quay đặt bản in nằm trên dải chú thích; dòng nguồn sáng hơn.
  - **S:** bảng lệch phải để lộ bản đồ; "Rows won:" giải thích điểm; nhãn hàng 32 px; hàng hiện sớm.

| Cặp | Tay nghề T1 → mới | Đọc chữ mới | Rõ ý mới | Chọn | Cờ mới |
|---|---|---|---|---|---|
| P1-v2 | 6,0 → 7,33 (8/7/7) | 8,0 | 9,0 | mới 3/3 | — |
| P2-v2 | 7,0 → 7,0 | 7,33 | **8,0** (từ 5,33) | **mới 3/3** | — |
| P3-v2 | 4,33 → 6,67 | 8,0 | 7,33 | mới 3/3 | confusing (1 người) |
| P4-v2 | 5,33 → 6,0 | 6,67 | 8,0 | mới 3/3 | empty_frame, flat_slide_look |
| P5-v2 | 4,0 → 7,0 | 7,67 | 8,0 | mới 3/3 | cluttered |

- **Nhiễu của phép đo:**
  - Cùng khung T1 nhưng điểm lệch tới ±0,67 giữa hai vòng (P1 F08: 5,67 → 6,0; P2 F12: 7,33 → 7,0).
  - P1 không đổi hình nhưng giảm 8,0 → 7,33 (1 người chấm 7). Đây là dao động của người chấm, không phải lỗi mới.
  - Chênh ≤ 0,7 điểm nằm trong nhiễu.

### 5.3 Vì sao chưa tới 8, và đề xuất (chờ chủ dự án chọn)
1. **Sticker bị đọc là "clip-art dán lên"** (2–3/3 người chấm ở P2, P3, cả hai vòng).
   - Đây chính là công thức sticker phẳng mà Kinh thánh yêu cầu. Người chấm theo thang "broadcast" phạt nó.
   - **Phương án:**
     - (a) giữ sticker, chấp nhận trần ≈ 7 cho cảnh có sticker;
     - (b) sticker vật vẫn render 3D nhưng đặt **trong cảnh** (ánh sáng chung, đổ bóng thật lên địa hình), giữ viền trắng: tốn giờ dựng;
     - (c) giữ sticker cho nhân vật, còn vật như thuyền, xe, xu dùng mô hình 3D trong cảnh.
2. **Dòng nguồn 30 px "nhỏ trên điện thoại"** (3/3, mọi cặp).
   - Người chấm xem ảnh ở 1280 px, nên chữ còn ≈ 20 px.
   - **Đề xuất** nâng dòng nguồn lên 34 px cho kênh 2 (đổi bố cục dải dưới, áp mọi tập) — cần chủ dự án duyệt.
3. **Chân dung nhỏ giữa nền nâu trống** (P4, 3/3).
   - Mâu thuẫn giữa "tranh không bị chú thích đè" và "tranh đủ lớn".
   - **Đề xuất:** bố cục chân dung lệch trái 60 % khung, chú thích đặt bên phải thay vì dải dưới. Thêm bóng đổ bản in và thị sai mạnh hơn.
4. **Nhãn ACTUAL bị coi là "nhiễu"** (P3, 2/3).
   - Nhãn này do luật nội dung kênh 2 (Q7) quy định. Đề nghị P/K xem lại việc gắn ACTUAL cho số lịch sử.
5. **P1: điểm cuối Albany chưa có nhãn ở mốc 13,0 s** (nhãn vào ở 13,4 s). Sửa dễ: đưa nhãn vào sớm hơn.

- **Không chạy lượt sửa thứ hai:** mỗi vòng 1080p ≈ 75 phút máy, và các điểm 1–4 cần chủ dự án quyết hướng.
- **Chi phí chấm hai vòng:** $1,81.

## 6. Giấy phép (chi tiết `RIGHTS.md` mục K2V2-* và dòng MET-11602)
| Mã | Tài sản | Giấy phép | Commit | SHA |
|---|---|---|---|---|
| K2V2-DEM-1 | USGS 3DEP 1″, 78 ô (gồm phần Canada USGS gộp vào lớp liền mạch) | Tác phẩm chính phủ Mỹ. Metadata ghi "Access constraints: None"; yêu cầu mô tả sửa đổi, không hàm ý USGS bảo trợ | **không** (cache 3,2 GB DEM; nền dẫn xuất ~30 MB) | từng ô: `channel-k2/k2v2-mau/relief-erie-meta.json` |
| K2V2-MAP-1 | Natural Earth 10m: hồ, đại dương, sông, đất, ranh bang/tỉnh | Tài sản công | không (zip cache) | như trên |
| K2V2-MAP-2 | `design/k2v/data/places-relief.json` (18 địa danh) | Dữ kiện | có | — |
| K2V2-STK-1 | 24 sticker (16 vật + 8 vai) | Tác phẩm tự dựng của dự án | có (1,5 MB) | `design/k2v/stickers/stickers.json` |
| MET-11602 | "De Witt Clinton", Samuel F. B. Morse 1826, The Met 09.18 | Met API `isPublicDomain: true` (Open Access CC0) | có, bản 1400×1672 (277 KB) | gốc `6883bab9…`, bản commit `73c2c15f…` |
| K2V2-LIB-1 | tifffile 2025.6.11, imagecodecs 2025.3.30 (BSD-3), pyshp 2.3.1 (MIT) | Mã công cụ | pip ghim phiên bản | — |

- **Ghi công trên hình:** "Terrain: USGS 3DEP · Map: Natural Earth"; chân dung: "Painting: Samuel F. B. Morse, 1826 · The Metropolitan Museum of Art, Open Access".
- **Mô tả YouTube khi dùng thật:** ghi thêm "elevation exaggerated, shaded and recolored" (mô tả sửa đổi, theo metadata USGS).

## 7. Chi phí
| Hạng mục | Chi phí |
|---|---|
| Claude API (chấm mù 2 vòng × 15 lượt + 1 lượt đo modelUsage) | **$1,84 / trần $10** (`kiem-mu/cost.jsonl` $1,806 + $0,037) |
| ElevenLabs | $0 (shot mẫu không lời) |
| YouTube Data API | 0 lượt |
| Tra cứu nguồn (tác tử con trong phiên, WebSearch/WebFetch) | thuộc phiên, không qua API trả phí của dự án |
| Giờ máy | Nháp 540p: 6 lượt (≈ 1,7 giờ). 1080p SPP4: 2 lượt (71,5 + 73,8 phút). Dựng nền relief 3 lượt × 2,5 phút. Tải DEM 3,2 GB |

## 8. Kiểm trước khi đẩy
- **Không có email** trong tệp commit: chỉ có `noreply@anthropic.com` ở dòng ký commit.
- **Không có media lớn:**
  - Shot mẫu **không** vào git hay LFS, chỉ ghi SHA.
  - Tệp lớn nhất được commit: ảnh `to-khung-*.jpg` ≈ 0,5 MB, `stickers-sheet.jpg` 0,26 MB, chân dung Met 0,28 MB. Sticker tổng cộng 1,5 MB; ảnh chấm mù 20 tệp × ~0,1 MB.
- **`/opt/cine/bin/python checks/lock.py --verify`: KHỚP** (`c598467f2283b141b8a14382c18dbe23b370522ef2a1afb31856399f7eb4549e`). Không có tệp nào trong `checks/` bị sửa.
- **`scripts/k2/test_k2v.py`:** 13/13 ĐẠT.
- **Tệp tập không bị sửa:** `git diff origin/main` không có `design/ll-hero/`, `channel-k2/k2c-t1-06/`, `channel-k2/k2g-ep01/`.

## 9. Việc đang chờ chủ dự án
1. **Duyệt mốc V2:** module relief, thư viện sticker + nhân vật A-lite, bảng điểm, cuộn mẫu. Sau khi duyệt, P ghi `AUTHORSHIP.md` và merge nhánh `k2-visual2` (phiên V2 không merge `main`).
2. **Quyết hướng cho mục tiêu tay nghề ≥ 8** (§5.3):
   - sticker (a/b/c);
   - cỡ dòng nguồn 34 px;
   - bố cục chân dung lệch;
   - nhãn ACTUAL cho số lịch sử (chuyển P/K).
3. **Chấp nhận lệch lệnh "1080p một lần":** đã dựng 1080p hai lần cho một lượt sửa sau chấm mù.
4. **Kinh thánh kênh 2:** phiên không đọc được `claude/CINE-LAB-BIBLE-KENH2.md`. Cần chủ dự án đối chiếu các điểm ở §1–§2 với Kinh thánh, hoặc đưa tệp vào repo để phiên sau đọc.
5. **Đề tài mẫu:** xác nhận kênh Erie/Main Line không trùng đề tài của các đối thủ ghi trong Kinh thánh. Phiên chỉ kiểm được `market-k2/REPORT.md`, không có "canal".
6. **Quyền ảnh/DEM:**
   - Mở trang The Met 11602 để đối chiếu câu Open Access (máy bị 429; đã đọc cờ `isPublicDomain: true` qua API của Met).
   - Ghi nhận phần DEM ngoài nước Mỹ (Canada) là dữ liệu USGS gộp vào lớp liền mạch 3DEP (metadata USGS: "Access constraints: None").
7. **Số liệu lệch giữa các nguồn** (`claims.md`): độ dâng kênh Erie 566/568/571 ft; chi phí $7M (dự toán) vs $7,143,789. Chọn khi làm tập thật.
8. **Tốc độ render:** relief chậm gấp ≈ 2 lần cảnh T1. Duyệt thử SPP2 / lưới nhẹ cho relief ở phiên sau (§4.1).

---

# V2b — một lượt sửa theo Kinh thánh kênh 2 §4 (phiên V2b, 14/10/2026; chủ dự án duyệt 14/10 18:08)
- **Nhánh:** `k2-visual2`, tiếp từ `0d6019a`.
- **Kinh thánh:** đã commit nguyên văn vào `docs/BIBLE-KENH2.md` (`10a035c`) và đọc trước khi sửa. Từ đây, việc "phiên không đọc được Kinh thánh" ở §0/§9 bên trên **đã được giải quyết**.
- **Không đụng tới:** không sửa `checks/`, không sửa tệp của tập, không merge `main`.

## V2b.0 Tóm tắt
| Hạng mục | V2 (vòng 2) | **V2b (vòng 3)** | Mục tiêu |
|---|---|---|---|
| Tay nghề chấm mù TB (mới) | 6,8 | **7,13** | ≥ 8 — **CHƯA ĐẠT** |
| Lượt chọn mới vs T1 | 15/15 | **15/15** | — |
| Cảnh 3D 1080p, đồng hồ thật / khung | 3,81 s (SPP4) | **2,70 s (SPP2)** | ≤ 1,86 s (T1) — **CHƯA ĐẠT** |
| Toàn bộ, đồng hồ thật / khung | 4,19 s | **3,08 s** | — |
| Nhịp thị giác: khoảng TB / dài nhất / khung tĩnh dài nhất | — | **1,16 s / 4,15 s / 4,04 s** | ≤ 3,5 s / — / ≤ 6 s — **ĐẠT** |
| Chi phí API V2b | — | **$0,90 / trần thêm $5** | — |

- **1080p dựng MỘT lần** (SPP2) sau tờ khung 540p.
- **Không chạy thêm lượt sửa nào** sau chấm mù vòng 3, đúng lệnh.

## V2b.1 Sửa gì
1. **Sticker vật dựng TRONG cảnh 3D (D2b, Kinh thánh §4)** — `design/k2v/relief.js`:
   - **Vật:** mô hình toon của `sticker-lab.js` đặt trên địa hình, cỡ theo px.
     - Nhận ánh sáng chung của cảnh. Mặt trời Tây Bắc 315°/45° được **chọn cùng hướng tô bóng địa hình**, để bóng vật và bóng núi nhất quán.
     - **Đổ bóng thật lên địa hình** bằng shadow map riêng từ máy mặt trời (2048², PCF 3×3 trong shader địa hình).
     - Đổi phối cảnh theo máy quay; vật đi theo tuyến quay theo hướng tuyến.
     - **Viền trắng bằng shader:** mặt nạ vật → quad toàn khung giãn 24 hướng, 5 px @1080p. Quad vẽ sau địa hình/tuyến và trước vật, nên chỉ viền bóng ngoài, không kẻ đường trong vật. Một phong cách, chạy trên cả hai bảng màu.
     - Chồng xu cũng đi qua cùng đường ống (bóng thật + viền), thay cho đốm bóng giả.
   - **Nhân vật A-lite:** tấm phẳng **trong cảnh**.
     - Quay trọn về máy. Lý do: máy nhìn gần thẳng xuống, nếu chỉ xoay quanh trục đứng thì nhân vật bị ép dẹt.
     - Nhận ánh sáng cảnh, nên tông đổi theo bảng màu. Đổ bóng lên địa hình. Lật theo hướng đi trên màn hình.
     - Viền trắng có sẵn trong hình (`STK.style`), đã bỏ bóng 2D.
   - **Giữ API cũ:** `scripts/k2/prep.py lift_props` tự chuyển `p.stickers` của shot `relief/*` vào `opt.props`, nên tập vẫn khai `pins/walkers/st:<id>`, `img`, `at/out` (cả `"@từ"`) như V2.
   - **Lỗi thứ tự vẽ đã sửa:** vật đục luôn vẽ trước lớp trong suốt, nên tuyến cam từng đè lên thuyền. Vật được đưa vào hàng vẽ trong suốt với `renderOrder` 9.
   - **Công sức phần nhân vật:** ≈ 20 dòng (billboard, lật, bóng), vẫn ≤ ~10 %.
2. **Chân dung (D4):**
   - Bản in lệch trái ~60 % khung, **nâng 0,12 đơn vị khỏi mặt bàn** để có bóng đổ dưới đèn bàn.
   - Máy trượt ngang 1,0 đơn vị và hạ dần, nên thị sai mạnh hơn.
   - Cột chú thích bên phải (`p.side`): tên · vai trò · năm · nguồn, có vạch nhấn hổ phách. Không còn dải chú thích dưới.
3. **Dòng nguồn 34 px (D3):** `SRCPX` trong `scripts/k2/lib/k2.js`, áp cho mọi tập 16:9 dựng sau; 9:16 giữ 46 px.
   - Chân bảng điểm có `maxW` theo bề rộng bảng.
   - Dòng nguồn H rút gọn ("LOC") để không xuống 2 dòng.
   - Kiểm lại: mép 48 px **0 vi phạm** (mép gần nhất 62 px); tương phản < 4,5: **0**; chữ < 30 px: **0**.
4. **Móc:** nhãn Albany vào ở **12,4 s**, trước mốc chấm 13,0 s (vòng 2: 13,4 s).
5. **Nhịp thị giác** (Kinh thánh §4, sửa 14/10 18:08): mục V2b.2.
6. **Nhãn né vật trong cảnh:** hộp chiếu `objL/objR` của vật/nhân vật vào `LL.occ`. Ở nháp, nhãn "Genesee Valley" từng che nhân vật nông dân; đã sửa.
7. **Thêm biến cố hình cho đoạn thưa:**
   - J: mốc máy đổi hướng 6,0 s và nhãn "Hudson River" 6,6 s.
   - N: mốc máy 5,6 s.

## V2b.2 Nhịp thị giác (`scripts/k2/rhythm.py`, kết quả `channel-k2/k2v2-mau/rhythm-v2b.json`)
- **Cách đo:**
  - Khai `segments[].beats` trong `K2V2-reel.yaml`.
  - Script đối chiếu **từng** biến cố khai với một mốc thật của đặc tả (±0,3 s): vùng, tuyến, vòng, xu, mốc máy, sticker, nhãn, chú thích, chip năm, cột chân dung, bảng điểm. Biến cố khai không khớp thì báo LỖI.
  - Trên video: khung tĩnh là chuỗi khung có sai khác trung bình < 0,6/255 (ảnh xám 160×90).

| Chỉ số | Kết quả | Ngưỡng |
|---|---|---|
| Biến cố khai / sau gộp (< 0,25 s) | 43 / 38 (0 biến cố không khớp đặc tả) | — |
| Khoảng trung bình | **1,16 s** | ≤ 3,5 s |
| Khoảng dài nhất | **4,15 s** (S 39,85 s: hàng cuối bảng điểm → hết cuộn) | — |
| Khung tĩnh dài nhất (video) | **4,04 s** (từ 39,67 s, bảng điểm đã đầy) | ≤ 6 s |
| Cắt cứng | 5 (chỉ ở 5 lần đổi cảnh) | chỉ khi đổi cảnh |

- **Theo đoạn:** H 14 biến cố / 15 s · J 10 / 10 s · N 8 / 8 s · P 4 / 5 s · S 7 / 6 s.
- **Phép kiểm:** `test_k2v.py::test_v2b_rhythm` chặn khi trượt.

## V2b.3 Tốc độ: SPP2 / LOD (`scripts/k2/lod_test.py`, `lod-test.json`, tờ so `lod-test-sheet.jpg`)
- **Cách đo:** 6 khung 1080p chọn trước, trải mọi tầm máy (H ~440 và ~520 km, J ~600 km, N ~125 km, S ~650 km, P ảnh). So với chuẩn SPP4 không LOD.
- **s/khung** là số đo 1 tiến trình, tuần tự, chỉ vài khung mỗi lần chạy, nên **chỉ dùng để so tương đối**.

| Cấu hình | SSIM TB (min) | pHash max | s/khung |
|---|---|---|---|
| A SPP4 (chuẩn) | 1 | 0 | 10,17 |
| **B SPP2** | 0,965 (0,948) | 2 | **7,61** |
| C SPP2 + lưới 1/2 (> 300 km) + texture 4096 (> 500 km) | 0,947 (0,918) | 6 | 7,48 |
| D SPP4 + LOD | 0,968 (0,948) | 4 | 8,35 |

- **Chọn B (SPP2, tắt LOD).**
  - **SPP2:** SSIM thấp hơn 1 chủ yếu do mẫu răng cưa dưới điểm ảnh đổi chỗ trên vân địa hình rất dày (đổi mẫu jitter). Phóng 2× vùng nhiều vân, A và B không phân biệt được bằng mắt. Khung N (vật + xu): SSIM 0,987; khung ảnh: 0,990.
  - **LOD:** làm vân địa hình mềm đi **thấy được** ở 1:1 (pHash tới 6; C kém B rõ ở khung H/J), mà chỉ nhanh hơn ~2 %. Vì vậy `lodMesh`/`lodTex` để **mặc định tắt** (bật bằng `opt` khi cần).
- **Giờ render cuộn 1080p** (3 tiến trình trên 4 vCPU, đồng hồ thật):

| | V2 (SPP4) | **V2b (SPP2 + D2b)** | T1 |
|---|---|---|---|
| Cảnh 3D / khung | 3,81 s | **2,70 s** (2 847,5 s / 1 056) | 1,86 s |
| Toàn bộ / khung | 4,19 s | **3,08 s** (3 248 s) | 2,47 s |
| Mỗi tiến trình | relief 7,2–13,0 s | H 5,81 · J 10,65 · N 10,20 · S 4,35 · P 3,71 s | — |

- **Phần do D2b** (đo riêng cùng khung, 1 tiến trình, SPP2, có/không vật trong cảnh; `d2b-cost.json`):
  - J: 3,25 → 4,33 s (**+33 %**); N: 2,48 → 3,75 s (**+51 %**).
  - Hai đoạn này chiếm 456/1 056 khung. Ước phần D2b trong cuộn ≈ **0,17–0,43 s/khung**, tức 6–16 % của 2,70 s, tuỳ cách quy đổi tranh chấp CPU giữa 3 tiến trình.
  - Không có D2b, cảnh 3D ≈ 2,3–2,5 s/khung, **vẫn > T1**. Phần lớn chênh lệch nằm ở bản thân bản đồ nổi (đoạn J nhìn rộng tới 660 km: 10,65 s/khung mỗi tiến trình).
- **Đề xuất để về ≤ T1** (chưa làm; mỗi mục cần đo lại bằng `lod_test.py`):
  - (a) Mặt nạ viền và shadow map dựng ở ½ độ phân giải; vòng giãn viền 24 → 12 hướng.
  - (b) Khung rộng > 500 km chuyển SPP1 + lọc khử răng cưa hậu kỳ, vì texture đã mịn.
  - (c) Dựng 4 tiến trình thay vì 3. Hiện tiến trình P xong sớm, nên đuôi chỉ còn 1–2 tiến trình chạy.
  - (d) Chia đoạn dài (J) thành 2 tiến trình theo khoảng khung.
  - Kinh thánh §9 đã dự liệu rủi ro "sticker vật trong cảnh làm tăng giờ render (bù bằng SPP2/lưới nhẹ, đo mỗi tập)". Lưới nhẹ đã đo và không đáng dùng; SPP2 đã áp dụng.

## V2b.4 Chấm mù vòng 3 (cùng giao thức `blind_v2.py`, `rejudge3`)
- Cùng cặp, cùng khung T1, cùng thứ tự X/Y, cùng đề bài. Mốc giây giữ nguyên `key.json` (13,0 / 21,0 / 31,0 / 36,0 / 42,5 s), **chốt trước khi dựng 1080p**.
- Model ghim `claude-sonnet-5-5` (kèm lượt phụ nhỏ `claude-haiku-5-5` của CLI như V2).

| Cặp | Vòng 2: T1 → mới | **Vòng 3: T1 → mới** | Đọc / Rõ ý (v3) | Chọn v3 | Cờ mới v3 |
|---|---|---|---|---|---|
| P1 bản đồ móc | 6,0 → 7,33 | 6,0 → **8,0** (8/8/8) | 8,0 / 9,0 | mới 3/3 | — |
| P2 hành trình | 7,0 → 7,0 | 7,0 → **6,67** (7/6/7) | 8,0 / 8,0 | mới 3/3 | — |
| P3 số liệu | 4,33 → 6,67 | 4,33 → **7,0** | 8,0 / 7,67 | mới 3/3 | — (v2: confusing) |
| P4 chân dung | 5,33 → 6,0 | 5,33 → **7,0** | 8,0 / 9,0 | mới 3/3 | — (v2: empty_frame, flat_slide_look) |
| P5 bảng điểm | 4,0 → 7,0 | 3,67 → **7,0** | 7,67 / 8,0 | mới 3/3 | — (v2: cluttered) |
| **TB** | 5,33 → 6,8 | 5,27 → **7,13** | | **15/15** | **0 cờ** |

- **Đã cải thiện (thấy trong ghi chú người chấm):**
  - Chân dung: "clear hierarchy… balanced".
  - Không còn cờ lỗi nào.
  - Nhãn Albany được ghi nhận ở P1.
  - Viền + bóng vật được ghi nhận "white outlines and shadows are clean" (P3, R2).
- **Còn giữ dưới 8 (≥ 2/3 người chấm):**
  1. **Vật/nhân vật vẫn bị gọi "clip-art"** (P2 2/3, P3 2/3). D2b làm vật có ánh sáng/bóng thật, nhưng hình khối toon đơn giản vẫn đọc là biểu tượng. Đây là bản chất của công thức sticker trong Kinh thánh §4.
  2. **Dòng nguồn 34 px vẫn bị nêu "small"** ở mọi cặp. Người chấm xem ảnh 1280 px, nên 34 px còn ≈ 23 px.
  3. **Nhãn ACTUAL lặp** (P3 2/3). Việc này để phiên K (D5).
  4. **Chồng 10 xu và 1 xu "khó đoán tỷ lệ bằng mắt"** (P3 1/3).
  5. **Bảng điểm che bản đồ; "Rows won" chưa rõ nghĩa** (P5 2/3).
- **Nhiễu phép đo:** khung T1 giống hệt mà điểm dao động ±0,33 giữa các vòng (F09: 4,0 → 3,67).

## V2b.5 Chi phí
| Hạng mục | Chi phí |
|---|---|
| Claude API V2b (chấm mù vòng 3, 15 lượt) | **$0,90 / trần thêm $5** (sổ `kiem-mu/cost.jsonl` luỹ kế $2,71 cho V2 + V2b) |
| ElevenLabs, YouTube API | 0 |
| Giờ máy | Nháp 540p 2 lượt (≈ 25 phút) · `lod_test.py` 20 lần dựng (≈ 30 phút) · 1080p SPP2 **một lần** 54,1 phút · đo D2b 4 lần dựng (≈ 10 phút) |

## V2b.6 Kiểm trước khi đẩy
- `scripts/k2/test_k2v.py`: **16/16 ĐẠT**. Thêm `test_v2b_lift_props`, `test_v2b_outline_shader`, `test_v2b_rhythm`.
- `checks/lock.py --verify`: **KHỚP** (`c598467f…`). Không sửa `checks/`.
- **Luật K 1.10.2:**
  - Q33 ĐẠT; Q32 ĐẠT (tư liệu 11,4 %); Q34(c) số neo 3D **100 %**.
  - Q34(a)(b) trượt vì cuộn mẫu không có lời (như V2).
- **Không có email; không có media lớn ngoài git.**
  - Cuộn 1080p không vào git hay LFS. SHA-256 `0f7273714dc3885c59570da6e3dfccc6e3663f1d80e17501310fa1fa97f19981`, 114,2 MB, `/var/tmp/cine-out/k2v-shots/K2V2-reel/shot.mp4`.
  - Ảnh commit lớn nhất: tờ khung ≈ 0,5 MB.
- **Tệp mới/sửa:**
  - `docs/BIBLE-KENH2.md`.
  - `design/k2v/{relief,photo,sticker-lab}.js`, `design/k2v/data/places-relief.json`, `design/k2v/README.md` (mục V2b).
  - `scripts/k2/{hero.js,prep.py,vshot.py,rhythm.py,lod_test.py,test_k2v.py}`, `scripts/k2/lib/k2.js`.
  - `channel-k2/k2v2-mau/{K2V2-reel.yaml, to-khung-540.jpg, to-khung-1080.jpg, rhythm-v2b.json, lod-test.json, lod-test-sheet.jpg, d2b-cost.json, measure-1080-spp2-v2b.json, blind_v2.py, kiem-mu/…-v3}`.

## V2b.7 Việc đang chờ chủ dự án
1. **Duyệt V2b:** sticker vật trong cảnh, chân dung lệch, dòng nguồn 34 px, nhịp thị giác, SPP2. Sau đó P ghi `AUTHORSHIP.md` và merge `k2-visual2`.
2. **Tay nghề 7,13 < 8.** Chọn hướng cho phiên sau, vì lệnh cấm sửa thêm sau vòng 3:
   - (a) vật thư viện chi tiết hơn: vật liệu PBR thay toon, bevel, vân gỗ/kim loại, giữ viền;
   - (b) dòng nguồn 38–40 px, hoặc chuyển nguồn đầy đủ xuống mô tả, trên hình chỉ giữ tên nguồn ngắn;
   - (c) chồng xu có vạch thước "×10" cạnh chồng;
   - (d) bảng điểm thu nhỏ còn ~40 % khung, "Rows won" đổi thành "Advantages".
3. **Giờ render 2,70 > 1,86 s/khung (T1).** Duyệt thử các đề xuất (a)–(d) ở V2b.3 trong phiên kế, mỗi mục đo bằng `lod_test.py`.
4. **Nhãn ACTUAL cho số lịch sử (D5):** chuyển phiên K.
5. **Các việc còn treo từ V2 (§9 bên trên):** đối chiếu trang The Met; chọn số lệch nguồn (568/571 ft; $7,1M).
