Nhánh thật: `nc-v2v` (tiếp tục từ origin/nc-v2v @811b8ff8, không tạo nhánh mới; harness có gợi ý nhánh `ccr-c00b2de7-f4w3do` nhưng làm theo lệnh chủ dự án). Không merge. Chỉ sửa `reports/nc-v2v/**` và `design/k2v/v2v/**`. Không đụng mã k2v cũ, `scripts/**`, `checks/`, `docs/`, `channel-*/`, nhánh khác, `screening/*.mp4` (để nguyên trong cây làm việc).

# NC-V2V lượt 2 — Thử Gemini Omni Flash video→video làm "lớp bề mặt ảnh thật" trên bản dựng V7B: BÁO CÁO

> Phiên nghiên cứu, 19/10/2026 16:53–18:35 UTC. Chỉ đo và báo; không đổi đường ống sản xuất. Mọi số là số đo thật trong phiên (tệp ở `reports/nc-v2v/`), trừ chỗ ghi **(ước)**. Không chứa email hay khoá API. Khoá Gemini/OpenAI do proxy gắn; mã không đọc, in hay ghi khoá. User-Agent: `CineLab-research (+https://github.com/HungQuach301/cine-lab)`. Chỉ gửi lên Gemini clip do ta dựng (máy V7B) + bảng vật liệu CC0 + chữ lệnh; không gửi khung đối thủ.

## §0. Tóm tắt (đọc 2 phút)

**Kết luận: KHÔNG dùng Omni làm lớp bề mặt cho phim (đề xuất V2V-D1).** Omni làm ảnh trông "thật" hơn hẳn, nhưng ở cả 15 lần sửa nó đều đổi dữ kiện trên hình. Kết quả này đúng với phép thử §12.2 "bỏ AI ra mà dữ kiện đổi thì không dùng", và cùng hướng với bài học NC-AI về AI tự thêm nét.

| Việc | Kết quả đo |
|---|---|
| Bước 0 | **QUA**: `GET /v1beta/models` → HTTP 200, có `models/gemini-omni-1.1-flash`. |
| 1. Clip nguồn | Dựng lại bằng chính máy V7B (`scripts/k2/hero.js` + cảnh `tl/t3tl` @317dcf5), mỗi khung kèm một **mặt nạ ID** 10 loại. Gồm: c1 vây hãm đêm 13/9/1782 (1080p + 720p); c2 hero 2026 ban ngày; c3 lướt thấp qua đoàn Rodney 1780; c4 20 s trại 1779, cắt thành 2 × 10 s. Tổng 1 200 khung, ≈ 34 phút đồng hồ. |
| 2. Gọi Omni | **15 lượt sửa 720p** (5 đoạn × biến thể a/b/c), mỗi lượt **$1,10–1,12**. Có thêm 1 lượt thử cơ chế. Sau ≈ **$17,0** (sổ ước theo đơn giá), Google trả **HTTP 402 "prepayment credits are depleted"** cho 4 lượt cuối: 1080p, nối đa lượt, nối dài, lặp lại. **Chưa đo được 1080p và cơ chế nối của Omni.** |
| 3. Đo bằng máy | Có bản **đối chứng không AI** để biết sàn đo. Theo 6 ngưỡng ghi trước, **máy cho đạt 1/15** (c2-a). Khi P đọc khung thì c2-a có **2 cột lửa/khói bịa trên vịnh**, sân vận động có khán đài và máy bay trên sân đỗ, mà ngưỡng lửa của máy bỏ sót. ⇒ **0/15 dùng được**. Lỗi gặp nhiều: **mất cờ** (giữ 4–67 % so với đối chứng; đối chứng 93–95 %), **thêm lửa trong phố** ở cả 3 biến thể c1, **bịa đội quân/lửa trại** (c4B-a), **xoá dãy trại** (c4B-b), **bịa nhà đá, cờ, vách đá, tàu** (c4B-c), **thay hình tàu** (c3-a/c). |
| Đường nối c4 | Sửa riêng 2 đoạn 10 s. Bước nhảy màu tại giây 10 là **ΔE 19,6–27,3**, so với nền khung kề 0,4–1,0 (**gấp 28–65 lần**; nguồn tại cùng chỗ 1,07). Nối thấy rõ ở cả 3 biến thể. |
| 4. Chấm mù | 3 người chấm AI chọn bản Omni **39/45 cặp** ở cả 640×360 và 320×180. Điểm "thật như phim tài liệu" 3,29 so với 1,6; "AI-look" 2,9 so với 4,4. Nhưng **họ thưởng cho chi tiết bịa**, ví dụ "X shows troops, fires and ships; Y is empty CG" cho c4B-a, nơi quân, lửa và tàu đều là bịa. |
| 5. Ước cả tập 745 s | 1 lượt 720p cho ≈ 100 đoạn 10 s ≈ **$111** (ước). Tỉ lệ đạt đo được là 0/15, nên **số lượt làm lại không hội tụ**: cận trên 95 % của tỉ lệ đạt là ≈ 20 %, tức ≥ 5 lượt/đoạn, ≥ $555/tập, mà vẫn chưa chắc có đoạn đạt. Đầu ra có **C2PA `trainedAlgorithmicMedia` + SynthID**. Dùng Omni thì phải bỏ §12.3 "KHÔNG video AI" và trượt K-LAI-4 (Omni sửa toàn khung, không có vùng bảo vệ). |
| Chi phí thật | Gemini **$17,00** theo sổ (21 lệnh: 16 thành công, 1 lỗi 502, 4 lỗi 402). Đã **vượt mốc theo dõi $15**; lợi ích: đủ 3 biến thể cho cả đoạn có đường nối. Dưới mức chặn $40. Claude (chấm mù) **$0,262**. OpenAI (chấm mù) **$0,046**. ElevenLabs, YouTube, Runway 0. Giờ máy CPU ≈ **2,2 h** đồng hồ (mốc 8 h). |

**Xem nhanh:**
- `reports/nc-v2v/clip/so-c1.mp4`, `so-c2.mp4`, `so-c3.mp4`, `so-c4-noi.mp4`: lưới 2×2 gồm nguồn V7B, a, b, c.
- `to-so/to-so-*.png`: tờ so trước–sau; hàng cuối là bản đồ cạnh mới (đỏ) và lửa mới (vàng).
- `to-so/c2-a-khung224-lua-bia.jpg`: bằng chứng lửa bịa ở biến thể máy cho đạt.

## §1. Giới hạn thật của Omni (tài liệu đọc 19/10/2026 + đo)

**Nguồn đã đọc:**
- https://ai.google.dev/gemini-api/docs/omni ("Generate and edit videos with Gemini Omni Flash", trang ghi *Last updated 2026-09-23 UTC*), đọc 19/10/2026.
- https://ai.google.dev/gemini-api/docs/pricing (mục Gemini Omni Flash), đọc 19/10/2026.
- `GET /v1beta/models` (SHA tệp 4111db50…): `gemini-omni-1.1-flash` và `gemini-omni-flash-preview`, đều `inputTokenLimit` 131 072, phương thức `generateContent`/`countTokens`. Gọi thật qua **Interactions API** `/v1beta/interactions`.

| Mục | Tài liệu ghi | Đo trong phiên |
|---|---|---|
| Đầu vào sửa | Video tải lên để sửa hoặc nối dài **≤ 10 s**. Ref video tối đa 3 clip × 3 s. Không hỗ trợ system instruction, temperature hay negative prompt. **EEA, Thuỵ Sĩ, Anh không được sửa video tải lên.** | Gửi 10 s 1280×720 nội tuyến base64 (15–26 MB) được chấp nhận. |
| Độ phân giải ra | 360p, **720p mặc định**, **1080p và 4k là bản phóng (upscaled)**; tỉ lệ 16:9 hoặc 9:16. | 720p: **1280×720**. 1080p: **chưa đo** (402). |
| fps / thời lượng | Không ghi fps. Nối dài thêm 3–10 s mỗi lượt, tổng tối đa 40 s, dùng 10 s cuối làm ngữ cảnh và **sửa vài khung cuối của video vào** để nối mượt. | **24 fps, đúng 240 khung cho 10 s vào, 96 khung cho 4 s vào.** Có kèm âm thanh AAC do Omni sinh (ta bỏ). |
| SynthID / C2PA | Mọi video sinh ra có **SynthID** (vô hình, kiểm được bằng máy). | 16/16 tệp ra có **manifest C2PA** do "Google C2PA Media Services" ký: `c2pa.created` "Created by Google Generative AI" hoặc `c2pa.opened` + `c2pa.edited` "Added imperceptible SynthID watermark", `digitalSourceType = trainedAlgorithmicMedia`. Mã hoá lại bằng ffmpeg sẽ làm mất manifest; SynthID nằm trong điểm ảnh. |
| Cách gọi | Ví dụ trên trang là gọi đồng bộ. | Gọi đồng bộ bị cắt ở 30 s (**HTTP 502** "upstream request failed"). Chạy nền (`background: true`) rồi hỏi trạng thái thì được, 92–131 s/lượt. |
| Giá | Vào $1,50/1M token; ra video $17,50/1M; văn bản + suy nghĩ $9/1M; **5 792 token/giây 720p ≈ $0,10/s**. Không có bậc miễn phí. | Mỗi 10 s: ra 57 920 token video (đúng 5 792/s), vào 55 860 token video (5 586/s) + 88–152 token chữ (+1 100 khi có ảnh tham chiếu), suy nghĩ 340–638 → **$1,10–1,12/lượt**. Giá 1080p: trang giá không ghi, chưa đo. |

## §2. Clip nguồn (bước 1)

**Máy dựng:**
- Worktree tạm `/var/tmp/v7b-wt` @ `origin/ccr-ef2b66f0-9639kq` 317dcf5 (V7B), chạy y nguyên `scripts/k2/hero.js --hero tl/t3tl`.
- Opt shot lấy từ `channel-k2/k2c-t3-01/v7p/episode-v7b-a.yaml`. Chỉ đổi thời gian/máy ở chỗ ghi rõ: `design/k2v/v2v/clips.py` → `reports/nc-v2v/clips-opt.json`.

**Bộ đệm cảnh** dựng lại bằng `v7p_cache.sh` + `v7b_mau_nha.py` + `v7b_faden.py`, mọi SHA đều KHỚP. Phải xử lý 3 chỗ:
- Catastro trả 403 cho User-Agent mặc định của curl, tải lại được bằng UA CineLab;
- LUT phải lấy từ `origin/v5a`;
- `npm ci` cho three.js.

**Mức dựng:** `hero.js` mặc định spp 1, tức mức nháp. Đây không phải mức sản xuất V6.

| Clip | Nội dung | Khung | Tệp (ngoài git `/var/tmp/cine-out/v2v/src/`) | SHA-256 |
|---|---|---|---|---|
| c1 | H2 V7B nguyên bản, giây 11–21: 13–14/9/1782 sáng → đêm; pin nổi hiện, khai hoả, cháy; máy K (AGL 85 m, chúc 27°) | 264–503 | `c1-1080.mp4` 1920×1080 (33,8 MB) · `c1-720.mp4` (lanczos từ 1080) · `c1-1080in.mp4` (crf 21, đầu vào 1080 chưa gửi được) | `1d2c5c46…a51db` · `a1f49d12…68fe0` · `7cf07e79…eaed5` |
| c2 | H3 V7B máy D, **giữ 2026** suốt 10 s (gốc chạy 1938 → 2026), La Línea + Gibraltar ban ngày | 0–239 | `c2-720.mp4` | `243f492a…1b57b395` |
| c3 | C4 V7B (đoàn Rodney 25/1/1780 trưa), **máy mới bay thấp** AGL 16 → 10 m, 45 m/s giữa hai hàng tàu | 0–239 | `c3-720.mp4` | `6c9d9515…4ebd3` |
| c4 | C1-a V7B nguyên bản giây 0–20 (dãy trại 1779 mọc dần, máy A2), cắt A = 0–10 s, B = 10–20 s | 0–479 | `c4-20s.mp4` · `c4A-720.mp4` · `c4B-720.mp4` | `9658ffa2…181158` · `80a1272e…d56d214` · `e68a343b…631fe2` |

**Mặt nạ ID** (`design/k2v/v2v/idmask.js` + `mk_page.py` + `dung_id.js`):
- Trang dựng là bản sao `page.js` V7B tạo lúc chạy, có nối thêm đoạn mã; không sửa tệp gốc.
- Mỗi `Object3D.add` ghi tên hàm trong ngăn xếp gọi (`batteryV6`, `makeFleet`, `shipFlags`, `flags`, `lamps`, `makeCity`…). Mesh nhận loại theo luật ưu tiên: cờ > pin nổi > tàu > người > khác > nhà > vật đất.
- Mỗi khung: một lượt tất cả (uMask), một lượt mỗi loại (chỉ địa hình + loại đó), một lượt lửa (đèn/lửa ↔ địa hình trơn).
- Ra PNG 640×360, bảng màu phẳng: trời, nước, đất, nhà/công trình, tàu, cờ, pin nổi, lửa, người, khác. Dựng cho khung chẵn: 600 mặt nạ, 0,6–1,9 s/khung.
- Mẫu: `mat-na/id-c*.png`.
- Đã sửa một lần: lưới đường `roads.mesh` (thêm thẳng trong `setup`) từng bị xếp vào "khác" 11 % → nay là "đất".

## §3. Biến thể lệnh (bước 2) — nguyên văn ở `design/k2v/v2v/prompts.json`

- **(a)** Chỉ đổi vật liệu/ánh sáng sang ảnh thật, giữ nguyên mọi vật, vị trí, cỡ, số lượng, màu (kể cả tàu, cờ, nhà, lửa), máy quay và thời gian; không thêm, không bớt; một cú liền, không chữ, không lời, không nhạc.
- **(b)** Như (a), thêm khai báo nguồn/tham chiếu `[# Sources <VIDEO_0>@Video1] [# References <IMAGE_REF_0>@Image1]` và **bảng vật liệu CC0** `ref/bang-vat-lieu.jpg` (Poly Haven CC0: `marble_cliff_01`, `coast_sand_01`, `aerial_rocks_02`, mặt nước cắt từ `simons_town_harbour`; nguồn và SHA ở `ref/NGUON.md`). Lệnh dặn "chỉ tham chiếu bề mặt, không chép nội dung".
- **(c)** Đổi mạnh: "turn this 3D render into photorealistic aerial documentary footage…", chỉ giữ bố cục/số nhà–tàu–cờ và đường máy.
- **Thử cơ chế** (4 s từ `cong-hero.png` V7B, lệnh kiểu (a)): đầu ra gần như y nguyên nguồn. Ghi lại để biết rằng lệnh "giữ nguyên" có lúc chỉ cho bản chép lại.
- **Không làm được** do 402: 1080p cho biến thể tốt nhất (c1-b), nối đa lượt (`previous_interaction_id` + đoạn B), nối dài (`task: extend`), lặp lại c2-a để đo độ ổn định. Lệnh nguyên văn và tệp vào đã ghi trong sổ AI (dòng http 402).

## §4. Đo bằng máy (bước 3) — `design/k2v/v2v/do_v2v.py`, `noi.py`, `danh_gia.py`

**Cách đo** (640×360, mỗi 2 khung):
- **Căn khung:** ECC affine trên độ lớn gradient (ít nhạy với đổi sáng). Loại nghiệm phi lý, rồi chọn giữa không nắn và ECC theo NCC.
- **(i) Giữ dữ kiện:** F1 và IoU cạnh Canny (dung sai 2 px) trong vùng từng loại của mặt nạ ID.
  - Đếm vật = thành phần liên thông của tàu/cờ/pin nổi. Vật được tính là giữ khi hồi cạnh ≥ 0,5; riêng cờ thêm ΔE76 ≤ 25.
  - Cạnh mới ở vùng trống (trời/nước/đất cách vật ≥ 6 px) = cạnh ra cách mọi cạnh nguồn > 3 px.
  - Lửa mới = điểm cam sáng mới (HSV).
- **(ii) Nhấp nháy:** ảnh xám 160×90, vùng tĩnh theo nguồn.
- **(iii) Đường nối:** ΔE76 khung cuối A ↔ khung đầu B so với nền khung kề; thêm tỉ số chi tiết.
- **(iv) Bão hoà / colorfulness / chi tiết:** đúng công thức `scripts/k2tl/measure_look.py` (V5b-1b, dùng ở V6).
- **(v) Máy và thời gian:** luồng Farnebäck, độ dịch/tỉ lệ căn, lệch khung (NCC gradient, k ∈ ±12; chỉ tính khi đỉnh ≥ 0,01).

**Tự kiểm của bộ đo** (`tu-kiem/`):
- **Đồng nhất** (nguồn ↔ chính nó): F1 = 1, cạnh mới 0, lửa mới 0.
- **Nắn giả** (phóng 2 %, dịch, sáng +0,04, bão hoà ×1,15, mờ 0,8, nén lại):
  - đo ra đúng tỉ lệ 1,0203 và dịch 7,6 px như đã nắn, lệch khung 0;
  - sàn đo giữ vật: tàu 96–99 %, cờ 93–95 % (c4B: cờ trại rất nhỏ chỉ 64 %), pin nổi 90 %.
- **Vật giả** (dán khối vào trời/nước): bắt được (cạnh mới trời 0,35 %, 2,7 cụm/khung).
- Mỗi clip có một **bản đối chứng không AI** (`do/*-dc.json`). Các ngưỡng tính tương đối với bản này.

**Ngưỡng loại** (ghi trước trong `danh_gia.py`):

| Ngưỡng | Điều kiện đạt |
|---|---|
| T1 giữ tàu/cờ/pin | tỉ lệ giữ ÷ đối chứng ≥ 0,90 |
| T2 F1 cạnh | nhà ≥ 0,85, tàu ≥ 0,85 |
| T3 cạnh mới | ≤ 5 % ở mỗi vùng trời/nước/đất (luật giao việc) |
| T4 lửa mới | max ≤ max(0,05 %, 3 × đối chứng) |
| T5 nhấp nháy | ≤ 1,5 × đối chứng |
| T6 máy | dịch ≤ 12 px; tỉ lệ 0,97–1,03; lệch khung ≤ 1 khi xác định được |

**Bảng biến thể × số đo** (`danh-gia.md` / `danh-gia.json`; số thô ở `do/*.json`). "kxđ" = không xác định (cảnh gần tĩnh).

| Clip-biến thể | T1 giữ tàu / cờ / pin (÷ đối chứng) | T2 F1 nhà · tàu | T3 cạnh mới trời · nước · đất % | T4 lửa mới max % (sàn) | T5 nhấp nháy ÷ đc | T6 dịch px · tỉ lệ · lệch khung | Chi tiết nguồn → ra | Bão hoà nguồn → ra | Kết luận máy |
|---|---|---|---|---|---|---|---|---|---|
| c1-a | tàu 0,85 (0,88) · cờ 0,07 (0,07) · pin 0,82 (0,88) | 0,831 · 0,892 | nước 1,17 · đất 10,03 | 7,483 (1,002) | 2,79 | 3,93 · 1,0006 · −4 | 17,2 → 14,1 | 0,67 → 0,37 | LOẠI: T1 tàu/cờ/pin, T2 nhà, T3 đất, T4, T5, T6 thời gian |
| c1-b | tàu 0,75 (0,77) · cờ 0,31 (0,32) · pin 0,90 (0,96) | 0,879 · 0,811 | nước 1,79 · đất 12,8 | 4,799 (1,002) | 1,92 | 0,67 · 1,0004 · 0 | 17,2 → 11,5 | 0,67 → 0,36 | LOẠI: T1 tàu/cờ, T2 tàu, T3 đất, T4, T5 |
| c1-c | tàu 0,63 (0,65) · cờ 0,14 (0,15) · pin 0,45 (0,48) | 0,826 · 0,746 | nước 1,47 · đất 12,63 | 7,809 (1,002) | 3,96 | 4,37 · 1,0 · −3,5 | 17,2 → 15,1 | 0,67 → 0,35 | LOẠI: T1, T2, T3, T4, T5, T6 |
| c2-a | tàu 1,00 (1,02) | 0,958 · 0,979 | trời 0,43 · nước 0,2 · đất 2,59 | 0,032 (0,063) | 0,53 | 1,04 · 0,9947 · kxđ | 47,5 → 12,5 | 0,34 → 0,12 | **ĐẠT** (máy). **P đọc khung: LOẠI** (§4.1) |
| c2-b | tàu 1,00 (1,02) | 0,979 · 0,979 | trời 0,52 · nước 0,31 · **đất 7,58** | 0,005 (0,063) | 0,53 | 1,29 · 1,0 · kxđ | 47,5 → 19,3 | 0,34 → 0,15 | LOẠI: T3 đất |
| c2-c | tàu 0,65 (0,66) | 0,975 · 0,852 | trời 0,01 · nước 0,72 · đất 5,97 | 0,02 (0,063) | 0,76 | 5,63 · 1,0078 · kxđ | 47,5 → 18,0 | 0,34 → 0,18 | LOẠI: T1 tàu, T3 đất |
| c3-a | tàu 0,96 (0,97) · cờ 0,07 (0,08) | 0,0* · 0,833 | trời 2,58 · nước 3,25 · đất 1,15 | 0,122 (1,302) | 4,38 | 11,79 · 0,9904 · 0 | 23,4 → 10,2 | 0,35 → 0,07 | LOẠI: T1 cờ, T2, T5 |
| c3-b | tàu 0,99 (1,00) · cờ 0,61 (0,67) | 0,911 · 0,905 | trời 0,77 · nước 3,31 · đất 6,57 | 0,006 (1,302) | 1,99 | 8,33 · 0,9982 · 0 | 23,4 → 10,1 | 0,35 → 0,07 | LOẠI: T1 cờ, T3 đất, T5 |
| c3-c | tàu 0,92 (0,93) · cờ 0,06 (0,07) | 0,934 · 0,800 | trời 3,28 · nước 5,28 · đất 5,33 | 0,248 (1,302) | 4,21 | 9,76 · 0,9987 · −1 | 23,4 → 11,9 | 0,35 → 0,09 | LOẠI: T1 cờ, T2 tàu, T3 nước/đất, T5 |
| c4A-a | — | 0,989 · 0,979 | trời 0,0 · nước 2,2 · đất 13,13 | 0,064 (0,050) | 0,91 | 0,0 · 1,0 · kxđ | 20,3 → 21,4 | 0,56 → 0,41 | LOẠI: T3 đất, T4 |
| c4A-b | — | 0,895 · 1,0 | trời 0,73 · nước 1,14 · đất 9,41 | 0,0 (0,050) | 0,72 | 0,0 · 1,0 · kxđ | 20,3 → 29,7 | 0,56 → 0,27 | LOẠI: T3 đất |
| c4A-c | — | 0,916 · 0,325 | trời 0,2 · nước 6,19 · đất 14,67 | 3,063 (0,050) | 2,98 | 5,93 · 1,027 · kxđ | 20,3 → 24,4 | 0,56 → 0,29 | LOẠI: T2 tàu, T3, T4, T5 |
| c4B-a | cờ 0,04 (0,06) | 0,674 · 0,987 | trời 3,96 · nước 3,32 · đất 10,97 | 0,233 (0,050) | 1,68 | 0,17 · 0,9999 · kxđ | 19,9 → 25,9 | 0,57 → 0,40 | LOẠI: T1 cờ, T2 nhà, T3, T4, T5 |
| c4B-b | cờ 0,42 (0,65) | 0,728 · 0,782 | trời 0,27 · nước 0,53 · đất 3,66 | 0,788 (0,050) | 1,19 | 4,48 · 1,0006 · kxđ | 19,9 → 11,5 | 0,57 → 0,26 | LOẠI: T1 cờ, T2, T4 |
| c4B-c | cờ 0,27 (0,41) | 0,660 · 0,845 | trời 1,74 · nước 4,8 · đất 15,47 | 8,197 (0,050) | 2,06 | 1,17 · 0,9956 · kxđ | 19,9 → 30,3 | 0,57 → 0,40 | LOẠI: T1, T2, T3, T4, T5 |

\* c3-a T2 nhà = 0: vùng nhà trong c3 rất nhỏ (bờ xa) và Omni vẽ lại hẳn bờ.

### §4.1 P đọc khung (bổ sung cho máy, không thay máy)

**c2-a** (máy đạt), khung 224 = 9,3 s (`to-so/c2-a-khung224-lua-bia.jpg`):
- **2 cột lửa/khói trên vịnh** và gần đê. Đốm cam mới chỉ 0,03 % khung, nhỏ hơn sàn T4 0,063 % → **T4 bỏ sót**.
- Bãi cỏ thành **sân vận động có khán đài**.
- **Máy bay** đậu trên sân đỗ.
- Đường băng thành cỏ.
- ⇒ LOẠI theo §12.2. **Bài học đo:** ngưỡng lửa theo diện tích không bắt được một vụ nổ nhỏ, ngắn ở xa. Cần thêm phép đo "đốm sáng mới bền ≥ 1 s" nếu còn dùng bộ đo này.

**Các biến thể khác** (tờ so `to-so/`):

| Clip | Biến thể | Thấy trên tờ so |
|---|---|---|
| c1 | cả 3 | **Lửa cháy trong phố**; nguồn lúc đó không có lửa trong phố. |
| c1 | a | Còn phóng to cờ Union. |
| c3 | a, c | **Thay tàu cột trơn bằng tàu đủ buồm**, dời vị trí, nhân cờ. |
| c3 | b | Giữ hình tàu nhưng **đổi bờ trái thành vách đá vôi** không có trong cảnh. |
| c4B | a | **Bịa hai khối quân và lửa trại**, tàu ngoài khơi. |
| c4B | b | **Xoá dãy trại** có trong nguồn, thành bãi cát trống. |
| c4B | c | **Bịa nhà đá, cờ, vách đá, tàu buồm**. |
| c2 | c | Thêm **tàu hàng lớn** và **cờ xanh** không có trong nguồn. |

**Kết luận P:** 0/15 dùng được. Tỷ lệ làm lại thật = 15/15. Ngay biến thể giữ hình học tốt nhất (b) cũng trượt T1 cờ hoặc T3 đất ở mọi clip trừ c2. Riêng c2-b chỉ trượt T3 đất 7,58 % (vân đất thêm vào, tờ so không thấy vật mới). Đây là ca sát nhất, nhưng vẫn trượt ngưỡng giao việc.

### §4.2 Đường nối clip 4 (`do/noi-*.json`)

| Biến thể | ΔE nối | ΔE nguồn cùng chỗ | ΔE nền (trung vị) | Tỉ số nối/nền | ΔE màu 1 s mỗi bên (nguồn) | Chi tiết B/A (nguồn) |
|---|---|---|---|---|---|---|
| a | 19,62 | 1,07 | 0,55 | **35,4** | 5,80 (0,26) | 0,988 (1,014) |
| b | 27,33 | 1,07 | 0,42 | **65,1** | 4,79 (0,26) | **0,349** (1,014) |
| c | 27,34 | 1,07 | 0,97 | **28,1** | 6,15 (0,26) | 1,264 (1,014) |

- Hai đoạn sửa riêng **không cùng "look"**. Bước nhảy tại giây 10 lớn gấp 28–65 lần nền.
- Biến thể (b) còn tụt chi tiết còn 35 % ở đoạn B (đoạn B thành bãi cát trơn).
- Thử nối đa lượt và nối dài của Omni bị chặn bởi 402, **chưa có số đo**. Theo tài liệu, nối dài *sinh tiếp* nội dung từ 10 s cuối, không bám theo nguồn của ta. Vì thế về bản chất nó không giữ được hình học nguồn của đoạn B.

### §4.3 Look (iv)

- Đầu ra Omni **bão hoà thấp hơn nhiều** so với nguồn V7B: trung vị S 0,07–0,41 so với 0,34–0,67.
- **Chi tiết |Laplace| thấp hơn** ở c1–c3: 10–19 so với 17–47. Bản dựng của ta có răng cưa và vân thủ tục sắc; ảnh "thật" mềm hơn.
- Ở c4 (cỏ/cát) Omni thêm vân, chi tiết tăng lên 21–30.
- Gợi ý cho NC-CPU/NC-GPU: §6, D2.

## §5. Chấm mù (bước 4) — `reports/nc-v2v/cham-mu/`

**Giao thức:**
- 15 cặp, khung 120 (5 s) của mỗi đầu ra ↔ khung V7B cùng chỗ, X/Y xáo theo hạt 19102026 (`key.json`).
- Hai cỡ 640×360 và 320×180, cùng đề bài (`cham_mu.py`).
- Tiêu chí 1–5: thật như phim tài liệu, chi tiết, AI-look, đọc được tàu/cờ ở cỡ điện thoại; thêm câu chọn bên nào thật hơn.
- **R1** claude-sonnet-5-5 (`claude -p`, chỉ công cụ Read), **R2** gpt-6.1-sol (Responses API, stream), **R3** claude-haiku-5-5.

| Cỡ | Bên | thật | chi tiết | AI-look (5 = rõ AI) | đọc tàu/cờ | chọn Omni |
|---|---|---|---|---|---|---|
| 640×360 | V7B nguồn | 1,62 | 1,95 | 4,42 | 2,38 | — |
| 640×360 | Omni | **3,29** | **3,73** | **2,98** | **3,51** | **39/45** |
| 320×180 | V7B nguồn | 1,58 | 1,71 | 4,45 | 2,11 | — |
| 320×180 | Omni | **3,29** | **3,58** | **2,87** | **3,00** | **39/45** |

**Theo biến thể (Omni, 640 / 320):**

| Biến thể | thật | chọn Omni |
|---|---|---|
| a | 3,34 / 3,47 | 15/15 |
| b | 2,93 / 2,93 | 10/15 |
| c | 3,60 / 3,46 | 14/15 |

**Đọc kết quả:**
- Người chấm AI thấy rõ khoảng cách "giống phim thật".
- Nhưng **họ không bắt được dữ kiện bịa** và còn thưởng cho chi tiết bịa. Ví dụ c4B-a, R1: "X shows troops, fires and ships; Y is empty CG". Ở cặp đó quân, lửa và tàu đều là bịa.
- Điểm "đọc được tàu/cờ" của Omni cao hơn một phần vì Omni **vẽ thêm** cờ và tàu.
- ⇒ Chấm mù chỉ hợp để đo cảm nhận, không dùng làm bằng chứng giữ dữ kiện (khớp K-LAI-3 (e) và §12.3 "lớp kiểm là lưới lọc thứ hai").
- R3 (haiku) có vài lý do lệch nhãn X/Y, nên đáng tin kém nhất.

**So với đối thủ:** việc của phiên điều phối, làm trong chat. Phiên này **không** đưa khung đối thủ vào repo hay lên Gemini.

## §6. Ước cả tập 745 s (bước 5) — mọi số dưới đây là **(ước)** từ đơn giá thật đã đọc và số đo phiên này

| Khoản | Cách tính | Kết quả |
|---|---|---|
| Số đoạn 10 s | V7B: shot TB 14,8 s, 4,05 cắt/phút → ≈ 50 shot × 2 đoạn (giới hạn vào ≤ 10 s) | **≈ 100 đoạn, ≈ 50 đường nối trong shot** |
| Giá 1 lượt 720p | $1,11/đoạn (đo) × 100 | **≈ $111 / tập / 1 biến thể** (3 biến thể để chọn: ≈ $333) |
| Giá 1080p | Trang giá không ghi; 402 trước khi đo | **chưa biết** (tài liệu: 1080p là bản phóng) |
| Tỷ lệ làm lại | Đo 0/15 đạt (máy 1/15). Quy tắc ba: cận trên 95 % tỉ lệ đạt ≈ 3/15 = 20 % | **≥ 5 lượt/đoạn → ≥ $555/tập** ở 720p, và chưa chắc hội tụ |
| Đường nối | ΔE nối 28–65 × nền ở 3/3 biến thể | ≈ 50 đường nối thấy được. Phải hoà/cắt hoặc dùng nối dài (chưa đo) |
| Giờ máy nguồn + mặt nạ + đo | Nguồn 720p nháp 2,85 s/khung/làn (2 làn/4 lõi) → 17 880 khung ≈ **7 h**. Mặt nạ khung chẵn 8 940 × ≈ 1,3 s ≈ **3,2 h**. Đo 3 biến thể × 100 đoạn × ≈ 2,5 phút ≈ **12,5 h CPU**. Mức sản xuất V6 1080p vẫn ≈ 50 h như V7B §10 vì Omni cần nguồn của ta | **+ ≈ 16 h** ngoài giờ dựng sản xuất |
| Giờ chờ Omni | 92–131 s/lượt, chạy song song 3–6 lượt được | ≈ 1–2 h đồng hồ/lượt cả tập |

**Tác động đến luật kênh:**
- **BIBLE §12.3:** hiện ghi "KHÔNG: … video AI". Dùng Omni trên hình phải sửa luật này.
- **§12.2** (bỏ AI ra mà dữ kiện đổi thì không dùng): **trượt** ở 15/15 lần sửa.
- **K-LAI-1** (khung AI ≤ 20 % thời lượng, Chặn): tối đa ≈ 149 s/745 s.
- **K-LAI-4** (vùng bảo vệ \|LAI − A\| < 1/255 trên mặt nạ trời/cờ/tàu/mốc): Omni sửa **toàn khung**, không nhận mặt nạ. Muốn qua thì phải dán lại nguồn lên mọi vùng bảo vệ, tức là mất phần lớn lợi ích.
- **K-LAI-5** (đêm: chói ≤ 1,5×): c1 thêm lửa, chói tăng.
- **K-LAI-6:** sổ đã đủ trường (§8).

**Nhãn và công bố:**
- Đầu ra mang **C2PA `trainedAlgorithmicMedia`** và **SynthID**. Mã hoá lại thì mất C2PA nhưng SynthID còn, nên phải bật khai báo "altered or synthetic content" trên YouTube (kiểm trang chính sách lúc đăng).
- Câu mô tả §10.6 phải viết lại: hình 3D phủ bề mặt bằng AI tạo sinh, không còn là "surface detail AI-assisted on two street frames".
- **Rủi ro chính:** dữ kiện bịa (lửa, quân, cờ, nhà, tàu) trong phim lịch sử chiến tranh (§10.6) và lỗi Content ID/"inauthentic content" với hình AI. Người chấm mù không bắt được loại lỗi này.

**Kết hợp với NC-CPU/NC-GPU** (thay cho ý "Omni chỉ cho cận/cú lặn"):
- **Số đo không ủng hộ ý đó:** c3 (lướt thấp, chính là phần thấp của cú lặn) mất cờ nặng (giữ 7–67 % so với đối chứng) và **nhấp nháy cao nhất** (2,0–4,4× đối chứng). Máy cao cũng không an toàn: c1 (máy K) mất cờ 7–32 % và có lửa bịa; chỉ c2 (máy D, 2026 ban ngày, không có cờ) là ít lỗi. Không có loại máy nào cho Omni giữ được dữ kiện.
- **Đề xuất:** máy cao và cận đều **giữ bản dựng**. Omni chỉ làm **"ảnh đích" ngoài phim** cho NC-CPU/NC-GPU chỉnh look: bão hoà thấp hơn (S 0,07–0,40), sương xa, nước phản chiếu, vân đá/cát. Pixel của Omni không lên hình.

## §7. Chi phí thật

| Khoản | Mốc / chặn | Thật |
|---|---|---|
| Gemini API | $15 / $40 | **$17,00** theo sổ (đơn giá × usage trả về), 21 lệnh: 16 thành công (15 × $1,10–1,12 + thử 4 s $0,44), 1 × 502, 4 × 402 ($0). **Vượt mốc theo dõi; lợi ích: đủ 3 biến thể cho cả đoạn có đường nối thì mới đo được (iii).** Số Google thực tính chưa xem được (bảng AI Studio không truy cập từ phiên); trả trước cạn ở quanh số này. |
| Claude API (chấm mù) | $8 / $25 | **$0,262** (R1 sonnet $0,243 + R3 haiku $0,019), `cham-mu/cost.jsonl`. Token của phiên chính không đo được từ trong container. |
| OpenAI (chỉ chấm mù) | $3 | **$0,046** (R2 gpt-6.1-sol, 11 711 vào / 2 205 ra; đơn giá suy từ sổ NC-AI). |
| ElevenLabs / YouTube / Runway | 0 | 0 / 0 / 0 |
| Giờ máy CPU | 8 h | ≈ **2,2 h** đồng hồ: bộ đệm 0,25 · dựng 1 200 khung 0,6 (2 làn) · mặt nạ 600 khung 0,4 · đo 15 + 5 đối chứng + tự kiểm 0,8 · tờ so/clip 0,15. |

**Chặn an toàn và sự cố:**
- **402 bốn lần liên tiếp** (cùng lỗi ≥ 3) → dừng gọi Gemini, không thử lại.
- `pkill -f` / `pgrep -f` theo chuỗi đã **giết luôn shell của chính phiên hai lần** (BÀI HỌC #24 lặp lại). Tiến trình dựng không bị ảnh hưởng. Từ lần thứ hai chỉ dừng tiến trình theo PID. Đề nghị đưa luật "không `pkill -f`/`pgrep -f` với chuỗi có trong dòng lệnh của mình" vào BAI-HOC.

## §8. Sổ AI (K-LAI-6) — `reports/nc-v2v/so-ai.jsonl` (ghi lúc gọi) → `so-ai-klai.json` (`design/k2v/v2v/so_ai.py`)

Mỗi lệnh ghi: `model_req` + `model_resp` (`gemini-omni-1.1-flash`), `date_utc`, prompt nguyên văn, tệp vào + SHA-256, tệp ra + SHA-256 (kiểm lại khi chuẩn hoá), `usage` (token theo phương thức), `usd`, `mask.pct_duoc_sua = 100` (Omni sửa toàn khung), `c2pa` (đọc manifest thật trong tệp), `synthid`, `http`, `loi`.

Tóm tắt:

| # | Nhãn | HTTP | USD | Ra SHA-256 (đầu) | C2PA |
|---|---|---|---|---|---|
| 1 | thu-co-che (đồng bộ) | 502 | 0 | — | — |
| 2 | thu-co-che (nền, 4 s) | 200 | 0,4428 | e1b4e398… | có |
| 3–17 | c1/c2/c3/c4A/c4B × a/b/c 720p | 200 | 1,1006–1,1157 | `SHA256-ra.txt` | có (16/16 tính cả #2) |
| 18–21 | c1-b-1080p · c2-a-720p-lap2 · c4B-b-720p-daluot · c4A-b-720p-noidai | **402** | 0 | — | — |

Tệp ra Omni nằm ngoài git (`/var/tmp/cine-out/v2v/ra/`, mất theo container); SHA ở `SHA256-ra.txt`. **Bản gốc còn C2PA** có trong git: `clip/omni-goc-c2-b-720p.mp4` (4 700 717 B, SHA 7cb36003…).

## §9. Chỉ số trong ±5 % quanh ngưỡng (luật cứng)

Không chỉ số nào trong danh sách dưới làm đổi kết luận: mọi biến thể nêu tên đều trượt ngưỡng khác với khoảng cách lớn.

| Biến thể | Chỉ số | Giá trị | Lệch so ngưỡng |
|---|---|---|---|
| c1-a | T1 tàu ÷ đc · T1 pin ÷ đc | 0,881 · 0,881 | −2,1 % · −2,1 % |
| c1-a | T2 F1 nhà · T2 F1 tàu | 0,831 · 0,892 | −2,2 % · +4,9 % |
| c1-b | T2 F1 nhà · T2 F1 tàu | 0,879 · 0,811 | +3,4 % · −4,6 % |
| c1-c | T2 F1 nhà | 0,826 | −2,8 % |
| c2-c | T2 F1 tàu | 0,852 | +0,2 % |
| c3-a | T2 F1 tàu · T6 dịch | 0,833 · 11,79 px | −2,0 % · −1,8 % |
| c3-c | T1 tàu ÷ đc | 0,932 | +3,6 % |
| c4A-c | T6 tỉ lệ | 1,027 | −0,3 % so mép 1,03 |
| c4B-c | T2 F1 tàu · T3 cạnh mới nước | 0,845 · 4,8 % | −0,6 % · −4,0 % |

- Dải T6 tỉ lệ 0,97–1,03 hẹp: mọi giá trị ≈ 1,00 đều nằm trong ±5 % của cả hai mép. Không nêu riêng từng dòng (`danh-gia.json`).
- Sàn đo nằm sát ngưỡng ở hai chỗ: c4B đối chứng giữ cờ trại chỉ 64 %, và T4 bỏ sót lửa nhỏ ở c2-a (§4.1).

## §10. Quyết định đề xuất

| # | Đề xuất | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|---|
| **V2V-D1** | **Không dùng Omni (hay video→video AI) trên hình phim**; giữ §12.3 "KHÔNG video AI" | Giữ nguyên tắc dữ kiện có nguồn; tránh nhãn AI toàn phim, C2PA/SynthID; không thêm ≥ $555/tập | Mất bước nhảy "ảnh thật" mà người chấm thấy rõ (3,3 so với 1,6) | Không đổi đường ống; NC-CPU/NC-GPU tiếp tục là đường chính | Đối thủ dùng AI vẫn "thật" hơn → bù bằng D2 |
| **V2V-D2** | Dùng Omni làm **ảnh đích ngoài phim** để chỉnh look renderer (bão hoà, sương, nước, vân đá/cát): vài lượt/tập, không lên hình | Chi phí thấp (≈ $1–5/tập); đo được bằng `measure_look.py`; không vướng §12.2 vì pixel AI không lên hình | Vẫn là "AI tham gia sáng tạo" → ghi AUTHORSHIP; cần duyệt sửa câu §12.3 cho rõ "tham chiếu nội bộ" | NC-CPU/NC-GPU nhận "đích look" có số | Bắt chước cả chỗ bịa nếu không chọn khung → chỉ lấy thống kê màu/độ sương, không lấy hình |
| V2V-D3 | Nếu chủ dự án vẫn muốn thử tiếp: nạp lại tiền trả trước và chạy **4 lệnh còn dở** (1080p c1-b, nối đa lượt, nối dài, lặp c2-a), ≈ $5–8 (ước) | Đóng nốt câu hỏi 1080p và nối; đo độ ổn định lặp lại | Khó đổi kết luận D1 vì lỗi dữ kiện có ở mọi biến thể | Chỉ nghiên cứu | Tốn tiền cho câu hỏi gần như đã có đáp án |
| V2V-D4 | Đưa bộ đo (mặt nạ ID theo hàm dựng + F1 cạnh theo loại + đối chứng không AI + tờ so cạnh mới/lửa mới) thành **công cụ kiểm cho mọi bước AI sinh điểm ảnh** (K-LAI vân, phục chế ảnh) | Đo được "bịa" bằng máy, có sàn đo; chấm mù bỏ sót | Cần phiên K duyệt vì là luật mới; bổ sung phép "đốm sáng mới bền ≥ 1 s" (§4.1) | `checks/` (phiên K) | Ngưỡng theo diện tích bỏ sót vật nhỏ → luôn kèm P đọc tờ so |
| V2V-D5 | Ghi vào BAI-HOC: (a) gọi API sinh video phải chạy nền (đồng bộ bị proxy cắt 30 s); (b) không `pkill/pgrep -f` theo chuỗi; (c) người chấm AI thưởng cho chi tiết bịa | Tránh lặp lỗi | — | `reports/m3/BAI-HOC-LL.md` (phiên P) | — |

## §11. Việc chờ chủ dự án

1. **Xem** `reports/nc-v2v/clip/so-c1.mp4`, `so-c3.mp4`, `so-c4-noi.mp4` (lưới nguồn | a | b | c) và `to-so/to-so-c4B.png`, `to-so/c2-a-khung224-lua-bia.jpg`.
2. **Quyết V2V-D1…D5.** Đề xuất chính: **D1** (không dùng trên hình) + **D2** (ảnh đích ngoài phim).
3. **Billing Gemini:** tiền trả trước đã cạn (HTTP 402). Nạp lại hay không tuỳ quyết định D3. Phiên này **không** đọc được số thực tính trên AI Studio; đề nghị chủ dự án đối chiếu với sổ $17,00.
4. **Phiên P:** nếu D2 được duyệt thì ghi RIGHTS cho bảng vật liệu Poly Haven CC0 (`ref/NGUON.md`) và AUTHORSHIP. Ghi BAI-HOC theo D5. Điều phối tự so đầu ra Omni ↔ đối thủ trong chat (phiên này không đưa khung đối thủ vào repo).
5. **Phiên K:** xem đề xuất D4 (công cụ đo bịa cho mọi bước AI sinh điểm ảnh).

## Tệp

| Tệp | Nội dung |
|---|---|
| `design/k2v/v2v/` | `omni.py` (gọi + sổ + chặn chi phí $40) · `idmask.js` / `mk_page.py` / `dung_id.js` (mặt nạ ID) · `clips.py` · `prompts.json` · `do_v2v.py` · `noi.py` · `danh_gia.py` · `to_so.py` · `cham_mu.py` · `so_ai.py` |
| `reports/nc-v2v/` | `do/` (số đo + đối chứng) · `danh-gia.{json,md}` · `tu-kiem/` · `to-so/` (PNG) · `clip/` (≤ 5 MB) · `cham-mu/` (ảnh cặp, raw, khoá, kết quả, chi phí) · `mat-na/` (mẫu) · `ref/` (bảng CC0 + nguồn) · `so-ai*.json*` · `SHA256-*.txt` · `clips-opt.json` · `CHECKPOINT.md` |

---

## Phụ lục — lượt 1: 400 API_KEY_INVALID (19/10/2026 16:33–16:34 UTC, nguyên văn §1 của báo cáo lượt 1)

**§1. Bằng chứng (nguyên văn, đã che; khoá không bị đọc/in/ghi)**

Thời điểm: 2026-10-19 16:33–16:34 UTC. User-Agent: `CineLab-research (+https://github.com/HungQuach301/cine-lab)`. Không gửi email hay dữ liệu nào khác.

| # | Lệnh | Kết quả |
|---|---|---|
| 1 | `GET https://generativelanguage.googleapis.com/v1beta/models?pageSize=1000` (không tự đặt header khoá; để proxy gắn) | `400 INVALID_ARGUMENT — API key not valid. Please pass a valid API key.` |
| 2 | `GET https://generativelanguage.googleapis.com/v1/models` | như trên, `details[0].reason = API_KEY_INVALID`, `domain = googleapis.com`, `metadata.service = generativelanguage.googleapis.com` |

(Một lượt thử phụ gửi header giữ chỗ `x-goog-api-key: PROXY_INJECTED` để xem proxy có thay giá trị không — cùng lỗi 400.)

Chẩn đoán: proxy **có** gắn một khoá (nếu không có khoá, Google trả 403 "unregistered callers", không phải `API_KEY_INVALID`). Trạng thái proxy (`/__agentproxy/status`) không ghi lỗi chuyển tiếp nào. Vậy khoá đang lưu trong cấu hình môi trường bị Google coi là không hợp lệ: gõ sai/thiếu ký tự, đã xoá/thu hồi, hoặc là khoá của dịch vụ khác (vd. khoá Vertex/OAuth, không phải khoá AI Studio dạng `AIza…`).

*(Lượt 2: chủ dự án sửa khoá 19/10 23:50 theo giờ chủ dự án; bước 0 qua — §0.)*
