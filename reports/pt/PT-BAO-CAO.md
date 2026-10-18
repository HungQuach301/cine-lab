Nhánh thật: `claude/pt-khung-neo-ab-test-njr9wp` (harness buộc nhánh `claude/...`; lệnh ghi `pt-khung-neo`) — tạo từ `origin/v5b2b` @ `4bce864e` (fast-forward, main nằm trong v5b2b).

# PT — Phim trường khung neo + thử A/B "không AI" (H-A) vs "AI chỉ cho vân vật liệu" (H-B) — BÁO CÁO

> Phiên R&D PT, 17/10/2026, theo lệnh chủ dự án (duyệt F1–F8, G1–G5; yêu cầu thử H-A/H-B 17/10). **Không merge. DỪNG chờ chủ dự án.**
> **Bổ sung 18/10: nhánh C (sửa ảnh AI, chỉ nghiên cứu) ở §15.** Mọi số là số đo thật trong phiên (tệp ở `reports/pt/`) hoặc ghi rõ **(ước)**. Không có email, không có khoá API trong repo/báo cáo.

## 0. Khối điều lệ (lệnh + thực tế)
| Trường | Lệnh | Thực tế |
|---|---|---|
| Loại phiên | R&D PT | đúng |
| Nhánh | `pt-khung-neo` từ `origin/v5b2b` | `claude/pt-khung-neo-ab-test-njr9wp` (harness) từ `origin/v5b2b` @ `4bce864e`; ghi ở dòng đầu |
| Tệp được sửa | CHỈ `design/pt/**` + `reports/pt/**` | chỉ hai vùng này. `scripts/` chỉ **đọc/chạy** (`scripts/k2tl/measure_look.py` được nhập để đo; `scripts/env/verify.sh`); `checks/` không đọc mã; ghost SH đọc bằng `git show` ra `/var/tmp/pt/ghost/` |
| Trần | Claude API ≤ $3 (chỉ chấm mù) · OpenAI ≤ $5 (chỉ nhánh B; **18/10 nâng ≤ $15 cho B + C**) · YouTube 0 · ElevenLabs 0 · giờ máy ≤ 4 h | **$2,641** (24 lượt A\|B + 18 lượt A\|B\|C, ghim `claude-sonnet-5-5`) · **$0,863** (B $0,480 + C $0,383) · **0** · **0** · **≈ 1,9 h** (§9, §15.6) |
| Preflight | bắt buộc; che email; không in/ghi khoá | hook pre-commit/pre-push cài đầu phiên; kết quả §12. Khoá OpenAI do proxy gắn — mã không đọc biến khoá; khoá Claude chỉ truyền qua biến môi trường cho `claude -p` như giao thức V5b-2b |
| Video thử | không LFS; 540p ≤ 15 MB + ảnh tĩnh ≤ 30 MB | 2 video 540p **1,7 + 1,6 MB**; khung/tờ khung **3,4 MB**; ảnh AI gốc (bắt buộc lưu) **25 MB** ở `reports/pt/ai/` — §9 |
| Dừng | không dừng hỏi giữa chừng | xong việc; câu hỏi không chặn đã tự quyết, liệt kê ở §13 |

## 1. Tóm tắt (đọc 2 phút)
1. **Công cụ (đo thật, 4 lõi Xeon 2,8 GHz, không GPU):** Cycles CPU 1080p **223 s/khung @64 spp + OIDN**, **444 s @128 spp**, 215 s @64 spp không khử nhiễu; 720p 64 spp 107 s. **EEVEE chạy headless được** (EGL báo lỗi nhưng rơi về dựng phần mềm) **126 s/khung 1080p** — không nhanh hơn nhiều. Cảnh thật PT: **215–230 s/lượt (1943, 143 k mặt) và ≈ 100 s/lượt (1782) @40 spp 1080p**. Dựng hiện có three.js/llvmpipe: 1,5–1,6 s/khung (V5b-2b). ⇒ Cycles **chỉ khả thi theo cách phim trường**: nền tĩnh dựng 5 lượt chiếu sáng MỘT lần, lớp sống ghép 2D **1,05 s/khung 1080p** (0,26 s ở 540p).
2. **Khung neo đã dựng:** Grand Parade / Commercial Square (nay John Mackintosh Sq.), mép Main Street, máy cố định cao **4,6 m**, 32 mm, nhìn W-WNW ra Line Wall + vịnh. Hai mốc **1782** (ghost SH Drinkwater, 24 lô nhà, 12 lô đổ nát sau pháo kích, đạn pháo, pháo, xe kéo, tàu buồm) và **1943** (ghost SH OSM+AMS, 117 toà, 688 cửa sổ, 300 ban công, bao cát, hầm trú ẩn, tàu chiến/tàu hàng, đèn pha đêm phong toả). Mỗi mốc **9 s ngày→đêm có người**, nối bằng hoà 2 s (bộ đếm năm chạy 1782→1943), bộ đếm năm dưới-phải, nhãn phương pháp dưới-trái.
3. **Nhánh B đã chạy** (khoá có, `GET /v1/models` 200): 9 vân lát được bằng **`gpt-image-2.5-flare`** (model hiện hành theo tài liệu OpenAI đọc 17/10), 1024², **$0,0533/vân**, cả 9 có **chunk C2PA `caBX`**; tài liệu OpenAI nêu thêm **SynthID nhúng trong điểm ảnh**. 2/9 lộ đường nối (ngói 2,36; gỗ 1,56) → làm liền bằng phép toán. Render lại **cùng máy/ánh sáng/khung/mã/hạt giống** (số mặt, cửa sổ trùng từng số).
4. **Chấm mù (3 người, ẩn nhãn, thứ tự ngẫu nhiên): A thắng B ở CẢ HAI mốc, 6/6 phiếu.** Craft A–B: **1782 +0,67** (4,67 vs 4,00), **1943 +1,00** (7,00 vs 6,00); chi tiết +1,0 cả hai mốc; đúng thời kỳ +0,33/+1,0; "trông như ảnh AI" **B 3,33/3,67 vs A 3,33/3,00** (B nhỉnh "AI" hơn ở 1943). Lý do 3/3 người nêu: vân AI **sạch/phẳng kiểu CG**, đất 1782 AI đọc thành "cát trơn"; vân ảnh chụp A **cũ, thô, có thời chiến**.
5. **So với khung kênh cùng nơi (gib20 ×2, V5b-2b-T):** khung **1782** PT **thua 5/6 cặp** (craft 3,7–4,0 vs 5–6; "empty_frame / toy_like / flat_slide_look"); một cặp (vs gib20 1884) A thắng 2/3. Khung **1943-A** đạt craft **7,0** — cao nhất phiên. ⇒ phương pháp khung neo đạt khi khung **đầy mặt tiền gần** (1943), trượt khi khung **trống** (1782: 40 % trời + bãi tập rộng) và **người thủ tục "búp bê gỗ"** (cờ `toy_like` ở 24/24 phiếu).
6. **Số đo khung tĩnh (§7):** 1943 chi tiết M1 **19,5–20,2** (≥ cận dưới cổng 16; dưới đối thủ 26–31), colorfulness 23–35, bão hoà 0,14–0,25; 1782 chi tiết **6,9–8,9**, bão hoà **0,06–0,09** — xa dưới mọi mốc.
7. **Đề xuất (§11):** giữ **H-A (không AI)** cho vân — B không thắng chất lượng mà thêm rủi ro công bố; đưa **phim trường khung neo + Cycles nền 5 lượt + ghép lớp sống** vào V5b-2c/V6 cho **khung phố gần** (kiểu 1943), **không** dùng cho khung bãi rộng; việc cần trước khi lên phim: người (thay hình thủ tục), lấp khung 1782, chiếu ảnh PD có nguồn.

## 2. Việc 1 — công cụ (đo, không giả định)
Máy phiên: 4 lõi Intel Xeon @ 2,80 GHz (1 luồng/lõi), 15 GB RAM, **không GPU, không /dev/dri**. Blender `bpy` **5.2.2 LTS** (`/opt/bpy`), Cycles CPU (CUDA/OptiX vắng — `CUEW initialization failed`).

| Bài đo (`design/pt/bench/bench.py`, cảnh hộp 40 khối + sàn + mặt trời + trời Nishita, vật liệu nhiễu thủ tục) | Dựng (s) | Tổng tiến trình (s) |
|---|---|---|
| Cycles 1280×720 · 16 spp · OIDN (lượt khởi động) | 37,4 | 39,5 |
| Cycles 1280×720 · **64 spp · OIDN** | **106,5** | 108,0 |
| Cycles 1920×1080 · **64 spp · OIDN** | **223,1** | 225,0 |
| Cycles 1920×1080 · **128 spp · OIDN** | **443,6** | 445,3 |
| Cycles 1920×1080 · 64 spp · không khử nhiễu | 214,8 | 216,4 |
| **EEVEE** 1920×1080 · 64 mẫu TAA (headless; `EGL_BAD_MATCH` ×3 rồi dựng phần mềm, ảnh đúng: TB 210/255) | **126,2** | 127,7 |

- Mốc điều phối (2 lõi, 720p 64 spp, cảnh hộp, gồm biên dịch): 141 s. Máy này 4 lõi: **107 s** (≈ 1,3×, không phải 2× — OIDN + dựng BVH không song song hết).
- OIDN chỉ thêm ~4 % (223 vs 215 s) → luôn bật.
- **Cảnh thật PT @40 spp 1080p, adaptive 0,02, nảy tối đa 4:** 1943 (143 146 mặt, 117 toà) **214,6–231,8 s/lượt**, 5 lượt + độ sâu **1 124 s (A) / 1 174 s (B)**; 1782 (33 393 mặt) **≈ 100 s/lượt**, **531 s / 498 s**. Persistent data giữ BVH giữa các lượt.
- **So với three.js/llvmpipe hiện có:** 1,50–1,62 s/khung 1080p (V5b-2b, cảnh tl 3D, 2 tiến trình) — nhanh hơn Cycles ~140× mỗi khung, nhưng không có GI/bóng mềm/vật liệu PBR quét. Cycles mỗi khung 24 fps = **≈ 1,5 giờ máy cho 1 giây phim** → **không dùng Cycles từng khung**; chỉ dùng cho nền tĩnh (§4).

## 3. Việc 2 — tài sản không-AI: tải được + giấy phép nguyên văn
| Nguồn | Phiên tới được? | Tải thử | Giấy phép (nguyên văn trong `reports/pt/giay-phep/`) | Dùng trong PT |
|---|---|---|---|---|
| **Poly Haven** | **được** (polyhaven.com 200, api 200, dl.polyhaven.org 521 nhưng URL tệp qua API tải được) | 14 bộ vân 2K (màu + pháp tuyến + nhám), SHA trong `polyhaven-files.json` | **CC0** — "Our assets are all licensed as CC0…" (`polyhaven-license.txt`); API: "free for everyone - including commercial use" (`polyhaven-api.txt`) | **9 vân nhánh A** (bảng `giay-phep/README.md`) |
| **ambientCG** | **được** | `PavingStones036_1K-JPG.zip` 200, 9,35 MB, 11 tệp | **CC0 1.0** (`ambientcg-license.txt`); phương pháp tạo (photogrammetry/procedural/approximated…) có trang riêng — không có hạng "AI" (`ambientcg-creation-methods.txt`) | không (đủ ở Poly Haven) |
| **Quaternius** | trang **được** (200) | tệp qua Google Drive/itch.io — không tải tự động | FAQ: "All models are under the CC0 License." (`quaternius-faq.txt`) | không — phong cách low-poly hoạt hình, không hợp tả thực |
| **Kenney** | **được** | `kenney_city-kit-commercial_2.1.zip` 200, 4,10 MB | `License.txt` trong gói: "License: (Creative Commons Zero, CC0)" (`kenney-city-kit-commercial-License.txt`) | không — phong cách hoạt hình |
| **Smithsonian Open Access 3D** | **không**: 3d.si.edu **403**, si.edu/termsofuse **403**, api.si.edu (DEMO_KEY) **429** | — | không đọc được (ghi 403 trong `smithsonian-*.txt`) | — |
| **GitHub (bộ CC0)** | **một phần**: github.com 400, api.github.com **403**, codeload **403**; **raw.githubusercontent.com 200**, **`git ls-remote`/clone qua proxy được** | `git ls-remote KhronosGroup/glTF-Sample-Assets` OK | theo từng repo | không |
| **Commons** | API được nhưng **429** sau vài lệnh (như BAI-HOC #82) | — | — | ứng viên ảnh PD §4.3 |
| **LoC** | trang item JSON từng được (15/10); **tìm kiếm 403 Cloudflare** hôm nay | — | — | — |
| Font Inter | có sẵn (`fonts-inter`) | — | SIL OFL 1.1 — đã có dòng RIGHTS **K2-F1** | chữ trên hình |

- Phương án khi bị chặn đã dùng: **mặt tiền thủ tục + vân ảnh chụp CC0** (Poly Haven); không cần 3D tải về.
- 5 vân Poly Haven đã tải rồi **bỏ** sau khi xem tờ vân (`reports/pt/to-van-AB.jpg`): vữa `white_plaster_rough_01` ngả rêu xanh, `rough_linen` là vải màu lam… (ghi trong `giay-phep/README.md`).
- **Rủi ro còn lại (dữ kiện):** Poly Haven và ambientCG tự khai nguồn gốc (ảnh chụp/quét/thủ tục); phiên không kiểm độc lập được từng bước xử lý của họ. 3/9 vân dùng được đăng 2025–2026.

## 4. Việc 3–4 — mặt tiền có nguồn + lớp sống
### 4.1 Chọn góc + lý do
- **Grand Parade / Commercial Square, mép Main Street** (UTM 30N E 288 244,6 · N 4 002 145,8): (a) có trong **cả hai ghost SH** — 1782 có 2 điểm khống chế ngay quảng trường (sai khớp 20,3 / 9,9 m), 1943 dày toà OSM đã đối chiếu AMS; (b) là **bãi tập của đồn trú 1782** (Grand Parade) → người hợp thời kỳ (lính áo đỏ, đội hình) có lý do có mặt; (c) nhìn ra **Line Wall + vịnh + bờ Tây Ban Nha** → nhiều lớp chiều sâu, hoàng hôn trong khung, tàu hậu cảnh; (d) mặt tiền phía bắc quay nam → **có nắng cả ngày**.
- Main Street thuần (nhìn dọc phố) đã cân nhắc: chi tiết/khung cao hơn nhưng không có biển/tàu và khối 1782 dọc phố lệch tây 20–35 m (SH §4) → chọn quảng trường.
- **Hình học máy:** cao 4,6 m (tầm ban công tầng một, trong dải 2–10 m), hướng 281°, ngẩng 2°, 32 mm (HFOV 58°). Kiểm tự động "máy không nằm trong toà" (lần đặt đầu nằm TRONG toà w257446846 — bắt được trên ảnh xem trước, đã dời).
- **1782 dời +6 m Đông** để tim Main Street hai mốc trùng: khối Drinkwater nắn affine RMS 21,2 m (LOO 33,3) — dời nằm trong sai số nắn; ghi trong `design/pt/scene/pt_site.py` (`SHIFT`).

### 4.2 Bộ sinh mặt tiền (`design/pt/scene/build_scene.py`)
- **Khối:** ghost SH (chỉ đọc). 1943: mỗi toà `nha` một khối, số tầng `so_tang_uoc` (+1 tầng ngẫu nhiên 35 %), tầng trệt 3,9 m, tầng trên 3,4 m. 1782: 22 `khoi_pho` → **chia lô 7–11 m dọc mép nhìn thấy**, mỗi lô một nhà (màu vôi, nhịp, cửa chớp riêng), 2–3 tầng (trệt 3,4 / trên 3,1 m).
- **Mặt tiền** (chỉ mặt quay về máy, < 170 m, kiểm "mặt hở" bằng điểm thử 1,5 m ngoài tường): tường có lỗ cửa thật (má cửa sâu 0,26–0,32 m), kính chia ô + khung, **cửa chớp lá sách** (1943: sọc 4,5 cm bằng bump thủ tục; 1782: ván), mở/khép/hé; **ban công** (1943 sắt, thanh 12 cm; 1782 gỗ, hiếm), gờ tầng, gờ mái 3 bậc, tường chắn mái, chân tường đá, đá góc (30 % nhà 1943), bậu đá, cửa hàng (khung gỗ, kính, **dải biển hiệu trơn — không chữ**), mái che vải, chậu cây, bao cát cửa (1943, 25 %).
- **Mái:** 1943 bằng/tường chắn hoặc bốn mái ngói; 1782 mái ngói một dốc theo lô. Ống khói (226 ở 1943 / 21 ở 1782).
- **Đổ nát 1782** (bản đồ Drinkwater ghi "RUINS", sau đợt pháo 4/1781): 12/24 lô — đỉnh tường gãy theo nhịp, không mái, dầm cháy chìa, tường ngăn sau + sàn cháy + gạch vụn (không lộ lòng khối rỗng).
- **Đồ phố đúng thời kỳ:** 1782: 7 đống đạn pháo xếp tháp, 4 pháo trên Line Wall, 4 xe kéo hai bánh, 10 thùng, đống gỗ xẻ, chốt gác + đèn dầu, cột cờ **Union flag bản 1707–1801** (không chéo đỏ St Patrick), 6 tàu buồm (2 căng buồm) + 5 thuyền nhỏ. 1943: lối hầm trú ẩn dưới quảng trường (xây 1939), 3 đèn phố, cột cờ Union flag 1801, 2 tàu chiến + 3 tàu hàng (khói ống), 1 thuyền buồm cá. **Xe tải quân sự và 2 quầy hàng không đặt được** (kiểm vị trí trống trượt) — ghi là thiếu.
- **Biển, Line Wall, đồi Algeciras/Sierra** (đường đồi thủ tục 9–11 km — **không phải DEM**: phiên không có DEM tại máy; ghi là xấp xỉ).
- **9 khe vân lát được** (đúng danh sách H-B): vữa, đá vôi, gạch, đá hộc, ngói, gỗ, đất lát 1782, đá lát 1943, vải bố (mái che, buồm, bao cát). Chiếu hộp theo toạ độ vật (không UV). Màu sơn/vôi = vân × màu từng mặt (`tint`). Loang bẩn mặt đất + vệt ẩm chân tường = nhiễu thủ tục **giống hệt ở hai nhánh**.

### 4.3 Texture chiếu từ ảnh PD đúng phố — **CHƯA LÀM (không có nguồn đạt)**
- Cần: ảnh/bản khắc PD nhìn ngang tầm đúng Commercial Square/Main Street, ≥ 1 000 px, nguồn rõ.
- Tìm được: LoC (tìm kiếm **403 Cloudflare**), Commons (**429**; một subagent thử tiếp có lùi thời gian). Ứng viên duy nhất trong danh mục Commons "John Mackintosh Square": "Commercial Square shelter construction 3" — **604×442 px, tác giả không rõ, nguồn "Facebook"** → **không đạt** (độ phân giải, nguồn gốc). Drinkwater 1786 views nhìn từ Rock xuống vịnh — không đúng góc.
- ⇒ Không có RMS chiếu nào để báo. Bộ sinh đã sẵn khe vân theo mặt tiền; khi có ảnh, bước chiếu = khớp ≥ 6 điểm góc cửa/gờ ↔ toạ độ mặt tiền đã biết, giải máy (PnP), ghi RMS px. Đưa vào V5b-2c (§10).

### 4.4 Lớp sống (`design/pt/scene/people.py` + `live.py`)
- **Người:** không có bộ người CC0 tả thực hợp thời kỳ (Quaternius/Kenney: hoạt hình) → **hình người thủ tục** từ khối cơ bản, 6 vai mỗi mốc × 4 hướng × đứng/bước. Trang phục: 1782 lính áo đỏ + đai chéo trắng + mũ ba góc (có/không súng), pháo binh áo lam đậm, dân nam/nữ (váy dài, khăn), thuỷ thủ; 1943 lính kaki (mũ sắt/beret), hải quân lam đậm + trắng, RAF xám lam, thợ. **1943 phần lớn quân nhân** (dân thường Gibraltar sơ tán 1940).
- **Ánh sáng người = ánh sáng nền:** mỗi lượt dựng một tờ sprite bằng máy trực giao cùng hướng/cúi 8°, **cùng mặt trời**, mặt phẳng bắt bóng → bóng thật trong alpha. Đặt theo **phép chiếu phối cảnh của máy neo**, **che khuất bằng lượt khoảng cách của chính cảnh** (không mô hình độ sâu AI). Vị trí lấy mẫu theo điểm ảnh mặt đất nhìn thấy, **khoảng cách ≥ 10,0 m** (luật §10.6 của lệnh: không cận mặt, không người ngã).
- **Vệt phơi sáng dài:** mỗi khung = 3,6 phút "giờ ảo"; người đi = vệt liền (một dấu mỗi ~2 px, độ phủ 38 %). Bản đầu in 9–22 dấu rời → **chuỗi "bóng ma"** (thấy trên tờ khung) → đã sửa. Người đứng (nhóm, gác, **đội hình 32 lính 1782 lúc 9:00–10:36**) hiện/tắt theo giờ ảo.
- **Khói** ống khói (đỉnh nấu ăn sáng/chiều, gió Levante đẩy tây) + khói ống tàu đậm; **hải âu**; **cờ** gợn theo khung; **đêm**: 1782 quầng đèn dầu tại vị trí đèn thật + cửa sổ ấm; **1943 phong toả ánh sáng** (blackout) + 3 đèn pha phòng không quét trời (2D, có chủ đích minh hoạ) + sao.
- **Ngày→đêm:** 5 lượt nền (giờ mặt trời biểu kiến 9:30 · 12:48 · 16:12 · 17:33 · đêm; mặt trời theo thiên văn 12/9, vĩ độ 36,14°: 42,9°/124° → 7,8°/269°) hoà theo giờ ảo 8:36→22:24; giờ xanh = tối + ngả lam trước lượt đêm.
- **Chuyển F1** (diễn giải của phiên — F1 chưa có văn bản trong repo): hoà chéo 2 s đêm 1782 → sáng 1943, bộ đếm năm chạy 1782→1943 (dịu đầu/cuối). **F2**: bộ đếm năm dưới-phải (Inter SemiBold 78 px @1080p). Nhãn phương pháp dưới-trái **38 px**, kiểu SH §5: "Reconstructed from J. Drinkwater, Plan of the Batteries, 1782 · Facades: procedural, period style · not a photograph" / "Buildings: OpenStreetMap, checked against U.S. Army Map Service plan, 1943 · Map data from OpenStreetMap (ODbL) · facades procedural".
- **Chỉnh màu hậu kỳ chung** (bão hoà ×1,85 theo độ sáng, cong S 0,42, ấm 4 %) áp **mọi khung, cả hai nhánh** — sau khi đo bản đầu bạc màu (colorfulness 11–14). Không thêm phần tử nào để đạt chỉ số.

## 5. Việc 5 — khung thử
| Tệp | Nội dung |
|---|---|
| `reports/pt/pt-A-540p.mp4` (1,68 MB) · `pt-B-540p.mp4` (1,61 MB) | 20,0 s, 24 fps: 1782 ngày→đêm 9 s · hoà 2 s · 1943 ngày→đêm 9 s; có chữ |
| `reports/pt/to-khung-AB.jpg` | **tờ khung A\|B cạnh nhau**, 6 thời điểm (trưa/chiều/đêm × 2 mốc), không chữ |
| `reports/pt/khung/*.jpg` | khung 1080p không chữ (5 thời điểm × A/B) + 2 mẫu có chữ + dải khung video A |
| `reports/pt/log/log-{A,B}-540p.jsonl` | 480 dòng/nhánh: khung, giờ ảo, năm, trọng số lượt nền, số người đứng/vệt, **`ai_texture: true` ở 480/480 khung B**, `false` ở 480/480 khung A |
| `reports/pt/log/nen-*-meta.json`, `sprites-*.json` | thống kê cảnh (toà, cửa sổ, ban công, đồ phố), máy, mặt trời mỗi lượt, giây dựng |
- Khung tĩnh **khai trước** trong `live.py` (trưa = giờ ảo 12,8 = lượt d2; chiều = 17,55; đêm = 21,8), không chọn sau khi xem.

## 6. Việc 6 — nhánh B (H-B)
- **Credential:** proxy gắn khoá cho `api.openai.com`; `GET /v1/models` **HTTP 200** (133 model). Mã không đọc/in biến khoá.
- **Model + giá (nguyên văn trong `giay-phep/openai.md`):** hướng dẫn sinh ảnh hiện hành: "…using gpt-image-2.5-sunburst and gpt-image-2.5-flare… Flare for fast, high-quality everyday image generation". Giá GPT Image 2.5: "$8 per million image input tokens… $30 per million image output tokens, $5 per million text input tokens". Điều khoản đầu ra (OpenAI Services Agreement, PDF cdn.openai.com, SHA `b93f17c5…`): §4.1 "…Customer: (a) retains all ownership rights in Input; and (b) owns all Output. OpenAI hereby assigns to Customer all OpenAI's right, title, and interest, if any, in and to Output."; §4.4 "Output may not be unique, and other users may receive similar content". Trang HTML điều khoản trả **403** cho phiên.
- **Sinh:** 9 lệnh, `gpt-image-2.5-flare`, 1024×1024, `quality: high`, PNG; prompt nguyên văn + usage + SHA + C2PA từng lệnh trong `reports/pt/ai/goi-api.jsonl`. **Không có tham số seed** trong API (không tái tạo được từng điểm ảnh) — ghi trong log.
- **Chi phí thật:** mỗi lệnh 125 token chữ vào + 1 756 token ảnh ra ≈ **$0,0533**; **tổng $0,4795** (15 804 token ra).
- **C2PA:** 9/9 PNG có chunk **`caBX`** (Content Credentials). Tài liệu OpenAI "Content provenance": ảnh còn **SynthID** "embedded directly in supported media… may survive some transformations" (nguyên văn trong `openai.md`).
- **Kiểm lát** (tỉ số chênh qua đường nối / chênh bên trong; ≈ 1 = liền, > 1,5 = lộ; `design/pt/tools/seam.py`, `reports/pt/ai/kiem-lat.jsonl`): B 7/9 đạt (1,0–1,40); **ngói 2,36 và gỗ 1,56 lộ** → làm liền bằng hoà chéo bản dịch nửa ô (tất định) → 1,01 / 1,10; ảnh gốc AI + bản làm liền đều lưu. Nhánh A Poly Haven: 0,81–1,37.
- **Thay đúng 9 khe**: `build_scene.py --tex B` chỉ đổi đường dẫn vân; độ nhám + bump nhánh B suy từ độ sáng chính ảnh AI (phép toán) vì AI chỉ cho ảnh màu. Hình học trùng từng số (1943: 143 146 mặt, 688 cửa sổ ở cả A và B).
- **Khác biệt nhìn thấy:** vân AI **sáng và sạch hơn** (vữa gần trắng, đất 1782 vàng cát, gỗ xám bạc) → tường B sáng hơn, ít "thời gian"; gạch AI có hoạ tiết lặp xương cá. Albedo vân AI không hiệu chuẩn (khác với vân quét PBR).

## 7. Việc 7 — đo + chấm
### 7.1 Số đo khung tĩnh 1080p không chữ (`reports/pt/do/do-khung.json`)
M1 = cách cổng điều phối (`scripts/k2tl/measure_look.py`: thu 640×360, vùng giữa 15–85 %, chi tiết = |Laplace|). M2 = cắt đúng vùng giữa 640×360 của khung 1080p, chi tiết = **FIND_EDGES** (PIL). Mốc đối thủ điều phối cấp (bão hoà/colorfulness/chi tiết): Timelapse Studio Rome 0,28/26/26 · CITYTONS Rome 0,41/34/31 · Barcelona 0,60/70/31 — **không rõ cách đo nào sinh ra mốc này, nên báo cả hai**.

| Khung | A · M1 | B · M1 | A · M2 (FIND_EDGES) | B · M2 |
|---|---|---|---|---|
| 1782 trưa | 0,055 / 15,6 / 8,9 | 0,063 / 19,8 / 6,9 | 0,043 / 20,3 / 7,5 | 0,051 / 16,4 / 6,4 |
| 1782 chiều | 0,094 / 25,6 / 7,6 | 0,090 / 24,9 / 6,9 | 0,102 / 25,0 / 6,1 | 0,094 / 22,5 / 6,1 |
| 1782 đêm | 0,894 / 56,7 / 1,8 | 0,894 / 56,9 / 2,1 | 0,894 / 57,0 / 1,8 | 0,894 / 56,9 / 2,2 |
| 1943 trưa | 0,169 / 23,6 / 19,5 | 0,141 / 29,3 / 19,8 | 0,059 / 20,0 / 14,7 | 0,059 / 19,6 / 13,7 |
| 1943 chiều | 0,251 / 30,1 / 19,9 | 0,224 / **35,1** / 20,2 | 0,133 / 25,0 / 16,3 | 0,122 / 23,4 / 15,1 |
| 1943 đêm | 0,502 / 33,3 / 2,9 | 0,667 / 33,0 / 4,0 | 0,922 / 37,1 / 2,2 | 0,902 / 36,8 / 2,7 |
| *Khung kênh cùng nơi* | V5b-2b-T 21 s: 0,318 / 50,4 / 23,9 | gib20 1752: 0,424 / 52,5 / 27,1 | gib20 1884: 0,447 / 46,0 / 20,5 | |

- Trước chỉnh màu (A): 1782 trưa 0,055/10,9/7,7; 1943 chiều 0,102/13,8/18,0 → chỉnh màu chủ yếu nâng colorfulness.
- Đêm: bão hoà 0,89–0,92 là **trời lam đậm** chiếm khung, không phải màu nội dung — không dùng để so.
- **B vs A:** chi tiết gần như nhau (±1,5); B colorfulness M1 cao hơn ở 1943 (+5) vì vân AI sáng/tươi; không khác biệt có ý nghĩa ở 1782.

### 7.2 Chấm mù (`design/pt/tools/blind_pt.py`; `reports/pt/kiem-mu/`: key, X/Y, phiếu thô, `score.json`)
Giao thức như V5b-2b: `claude -p` ghim **claude-sonnet-5-5**, chỉ công cụ Read, thư mục tạm chỉ có X.jpg/Y.jpg, 3 vai nguyên văn `blind_v2.py` (R1 người xem, R2 đạo diễn 3D/motion, R3 biên tập tài liệu), thứ tự X/Y hạt giống 20261017, **không có nhãn nhánh**; mỗi khung khai năm định thể hiện. Thang: craft/detail/period 1–10, **ai_look 0–10** ("có trông như ảnh AI không?").

| Cặp | Khung | craft (R1, R2, R3 → TB) | chi tiết | đúng thời kỳ | ai_look | Chọn |
|---|---|---|---|---|---|---|
| **A vs B 1782** | A | 5, 4, 5 → **4,67** | 4,00 | 4,33 | 3,33 | **A 3/3** |
| | B | 4, 4, 4 → **4,00** | 3,00 | 4,00 | 3,33 | |
| **A vs B 1943** | A | 7, 7, 7 → **7,00** | 5,67 | 5,67 | **3,00** | **A 3/3** |
| | B | 6, 6, 6 → **6,00** | 4,67 | 4,67 | **3,67** | |
| A-1782 vs gib20 1752 | A / g | 4,00 / 6,00 | 3,0 / 6,0 | 4,0 / 4,33 | 3,0 / 3,0 | gib20 3/3 |
| A-1782 vs gib20 1884 | A / g | **6,00** / 5,00 | 3,33 / 4,67 | 4,33 / 3,33 | 3,0 / 2,67 | **A 2/3** |
| A-1782 vs V5b-2b-T | A / v | 3,67 / 6,00 | 3,0 / 5,67 | 4,0 / 5,67 | 3,0 / 3,0 | V5b-2b 3/3 |
| B-1782 vs gib20 1752 | B / g | 4,00 / 6,00 | 3,0 / 7,0 | 4,0 / 4,33 | 3,33 / 2,67 | gib20 3/3 |
| B-1782 vs gib20 1884 | B / g | 4,00 / 5,00 | 3,0 / 4,67 | 4,33 / 4,33 | 3,33 / 2,33 | gib20 3/3 |
| B-1782 vs V5b-2b-T | B / v | 3,67 / 6,00 | 2,67 / 5,67 | 4,0 / 6,0 | 3,33 / 2,33 | V5b-2b 3/3 |

- **Chênh A–B:** craft +0,67 (1782), +1,00 (1943); chi tiết +1,00/+1,00; thời kỳ +0,33/+1,00; ai_look 0/−0,67 (B "AI" hơn ở 1943). Trung bình craft A **5,83** vs B **5,00** trên hai cặp A/B.
- **Lý do (nguyên văn rút gọn):** B 1943 "materials look flat and CG-smooth"; A "weathered plaster, stone edging and darker shutters that look aged… feels more wartime". B 1782: "smooth sandy ground with no texture… flat beach".
- **Cờ lặp:** `toy_like` 24/24 phiếu khung PT ("peg-doll soldiers"), `empty_frame` mọi khung PT, `flat_slide_look` mọi khung 1782. R3 gắn `anachronism` cho A-1782 ở 1 cặp (không nêu cụ thể).
- **Độ ổn định người chấm:** cùng ảnh A-1782 được craft 3,67–6,00 tuỳ ảnh đối chứng (thang tương đối theo cặp) — đọc số theo cặp, không so tuyệt đối giữa cặp.
- **Cặp đối thủ:** không có khung đối thủ trong repo hay API; điều phối tự chấm trong chat (gợi ý dùng `reports/pt/khung/1943-trua-A.jpg` và `1782-trua-A.jpg`).

## 8. Rủi ro công bố AI (chỉ dữ kiện, không kết luận luật)
- Ảnh nhánh B mang **C2PA Content Credentials** (chunk `caBX`, 9/9) khi tải về; tài liệu OpenAI nói C2PA "Editing, converting, or sharing a file can remove its metadata" và **SynthID** là watermark trong điểm ảnh "may survive some transformations". Vân bị chiếu hộp, thu nhỏ, đổ bóng, mã hoá H.264 trong khung cuối — phiên **không kiểm** SynthID có còn dò được trên khung phim hay không (công cụ `POST /v1/content_provenance_checks` có, chưa gọi để giữ chi phí và phạm vi).
- Điều khoản OpenAI §4.1 giao quyền đầu ra cho khách "to the extent permitted by applicable law"; §4.4 đầu ra "may not be unique".
- Kênh đã có luật trên hình "No AI imagery" ở khung gib20 (thấy trên khung đối chứng) và CHUAN-KENH §10 (lời không nói trực diện về AI, không khẳng định sai cách làm phim). Dùng nhánh B thì dòng "No AI imagery" **không còn đúng** cho khung có vân B.
- YouTube/nền tảng bán phim có chính sách công bố nội dung tổng hợp — phiên không đọc trang chính sách (ngoài phạm vi), đưa vào việc chờ.

## 9. Giờ máy, chi phí, dung lượng
| Khoản | Trần | Thực tế |
|---|---|---|
| Claude API | $3 | **$1,467** (24 lượt chấm mù; `reports/pt/kiem-mu/cost.jsonl`, phục vụ `claude-sonnet-5-5` 24/24) |
| OpenAI API | $5 | **$0,4795** (9 lệnh; `reports/pt/ai/goi-api.jsonl`) |
| YouTube / ElevenLabs | 0 / 0 | 0 / 0 |
| Giờ máy | ≤ 4 h | **≈ 1,8 h**: bộ đo 1 121 s · xem trước ≈ 300 s · sprite 2 mốc × 5 lượt ≈ 510 s · nền 1080p A+B 3 327 s · ghép lớp sống (thử, 4 lượt khung, 4 video) ≈ 1 100 s |
| Dung lượng repo | video ≤ 15 MB, ảnh ≤ 30 MB | video 3,3 MB; khung + tờ khung 3,4 MB; **ảnh AI gốc 25 MB** (lệnh bắt lưu ở `reports/pt/ai/`; tệp lớn nhất 3,4 MB < 5 MB, không LFS) |

- **Đề xuất dòng COST-LEDGER (P ghi):** `PT-01,phim trường khung neo + A/B vân AI,R&D,2026-10-17,,,,,1.47,3,claude-sonnet-5-5,0,0,≈ 1,8,,0,20,OpenAI $0.48 (gpt-image-2.5-flare ×9),reports/pt/PT-BAO-CAO.md,YouTube 0; không merge`
- **Ước giờ máy/tập cho 4–6 khung neo (ước, máy này, 1080p):** mỗi khung neo × mỗi mốc = nền 5 lượt + độ sâu (1943-loại 0,31 h · 1782-loại 0,15 h @40 spp) + sprite 0,07 h + ghép 216 khung × 1,05 s = 0,06 h → **0,3–0,45 h**. 4–6 khung neo × 2 mốc ⇒ **2,4–5,4 h**; nâng 64 spp ⇒ **3,4–7,6 h**. Chưa gồm vòng sửa. Nhánh B **không thêm** giờ máy (chỉ thay vân) nhưng thêm $0,05/vân.

## 10. Việc cần đưa vào V5b-2c / V6
1. **Người:** thay hình thủ tục "búp bê gỗ" (24/24 phiếu `toy_like`) — người có tỉ lệ đúng, áo nếp, dáng đi (rig MPFB/Blender đã dùng ở M-tập 1) dựng sprite như PT; giữ ≥ 10 m.
2. **Bố cục khung neo:** khung phải **đầy mặt tiền gần ở 1/3 trái hoặc phải**, trời ≤ 25 %; khung bãi rộng (1782 hiện tại) → hạ ngẩng, 40–50 mm, hoặc chọn góc khác (Main Street nhìn bắc). Luật tự kiểm: % trời + % mặt đất trống trước khi render nền.
3. **1782:** mặt tiền 1782 chi tiết hơn (cửa sổ bé song sắt, mái đua gỗ, giàn phơi, tường vôi loang), đổ nát tự nhiên hơn (vỡ theo khối, không bậc thang), đất có vết bánh xe/vũng.
4. **Chiếu ảnh PD có nguồn** (§4.3): cần chủ dự án/Cowork lấy ảnh đúng góc (LoC photochrom "Commercial Square"/"Main Street" c.1890–1900 nếu có; Gibraltar National Archives cần kiểm quyền) → PnP + RMS.
5. **Đồ phố còn thiếu:** xe tải/xe jeep 1943 + quầy hàng (đặt vị trí tay, kiểm trống), biển hiệu (chữ thời kỳ đúng nguồn, không chữ bịa).
6. **DEM thật cho đồi bên kia vịnh** (Copernicus GLO-30 đã có giấy phép trong repo) thay đường đồi thủ tục.
7. **Lượt chiếu sáng:** 5 lượt đủ cho 9 s; khung dài hơn → 7–8 lượt để bóng không "nhảy" khi hoà; thử lượt "giờ xanh" thật thay vì tint.
8. **Công cụ:** `live.py` cần đọc EXR qua `OpenEXR` (OpenCV của môi trường không đọc EXR — đã cài `OpenEXR` vào `/opt/cine` trong phiên; đề xuất thêm vào `verify.sh`).

## 11. Quyết định đề xuất
### Q-PT1 — Vân vật liệu: H-A hay H-B?
| Phương án | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|
| **A. Giữ H-A (không AI) — đề xuất** | thắng chấm mù 6/6 phiếu, craft +0,67/+1,0; vân quét PBR (pháp tuyến, nhám thật); giữ được nhãn "No AI imagery"; $0 | thư viện CC0 hữu hạn, đôi khi phải chọn lại (5/14 vân bỏ) | không đổi quy trình | Poly Haven/ambientCG tự khai nguồn gốc |
| B. Dùng H-B cho vân | rẻ ($0,05/vân), đúng mô tả từng vật liệu, tạo nhanh | thua chấm mù; "CG-smooth", albedo không hiệu chuẩn; 2/9 lộ nối; không seed (không tái tạo); C2PA + SynthID | phải bỏ nhãn "No AI imagery"; thêm sổ AI + cờ `ai_texture` mọi khung | công bố AI trên nền tảng/bán phim (§8); quyền đầu ra "to the extent permitted by law" |
| C. Lai: H-A mặc định, H-B chỉ khi CC0 không có vật liệu cần | lấp lỗ thư viện | vẫn kéo theo toàn bộ nghĩa vụ công bố cho khung đó | như B nhưng hẹp | như B |

### Q-PT2 — Phương pháp phim trường khung neo (Cycles nền 5 lượt + ghép lớp sống)
| Phương án | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|
| **A. Đưa vào V5b-2c/V6 cho khung phố gần — đề xuất** | khung 1943 craft 7,0 (cao nhất phiên, > khung kênh 5–6); nhà/đồ vật **cố định giữa mốc trong cùng thời kỳ** (khác đối thủ AI); mọi chi tiết có nguồn (ghost SH) hoặc ghi "procedural"; 0,3–0,45 h máy/khung neo-mốc | người thủ tục yếu; 1782 khung rộng trượt; chiếu ảnh PD chưa làm | 4–6 khung neo/tập ⇒ 2,4–5,4 h máy (ước) | cần GPU nếu muốn 64–128 spp + nhiều lượt |
| B. Chỉ dùng three.js/llvmpipe như hiện tại | nhanh 1,5 s/khung, đã có dây chuyền | không GI/PBR; chi tiết tầm mắt thấp | giữ nguyên | khung tầm mắt kém đối thủ |
| C. Cycles từng khung | chuyển động thật mọi lớp | ≈ 1,5 h máy / 1 s phim | không khả thi trên CPU | — |

## 12. Chỉ số trong ±5 % quanh ngưỡng · preflight · tệp
- **±5 %:** colorfulness M1 khung **1943 chiều B = 35,1** vs mục tiêu cổng 35 (+0,3 %). Không chỉ số nào khác trong ±5 %: kiểm lát gần nhất B `da_hoc` 1,40 vs 1,5 (−6,7 %); chi tiết 1943 M1 19,5–20,2 vs 16 (+22–26 %); trần Claude $1,467/$3 (49 %), OpenAI $0,48/$5, giờ máy 1,8/4 h, video 3,3/15 MB. Khoảng cách người ≥ 10,0 m là **luật cứng trong mã** (lấy mẫu bỏ < 10 m), không phải chỉ số đo.
- **Preflight:** ĐẠT (§14).
- **Tệp mới:** `design/pt/{bench/bench.py, scene/{pt_site.py, build_scene.py, people.py, live.py, passes.json}, tools/{page_text.py, ghost_map.py, gen_tex_b.py, seam.py, measure.py, sheet_ab.py, blind_pt.py}}`, `reports/pt/**`. Không sửa tệp nào khác. Ghép thử với `main`: chỉ thêm thư mục mới `design/pt/`, `reports/pt/` → không xung đột (nhánh chứa thêm các commit V5b-2b chưa merge của `origin/v5b2b`).
- **Đề xuất ngoài vùng (chưa ghi):** RIGHTS.md 9 dòng vân Poly Haven CC0 (bảng `giay-phep/README.md`) + 9 dòng vân AI nếu chọn H-B; AUTHORSHIP.md quyết định Q-PT1/Q-PT2 + chọn góc Grand Parade + dời 1782 +6 m; COST-LEDGER dòng PT-01; `scripts/env/verify.sh` kiểm `OpenEXR`.

## 13. Việc chờ chủ dự án
1. **Q-PT1** (H-A / H-B / lai) và **Q-PT2** (đưa phim trường khung neo vào V5b-2c/V6, phạm vi khung phố gần).
2. **F1 / F2:** văn bản F1–F8, G1–G5 (17/10) chưa có trong repo — phiên diễn giải F1 = hoà chéo + bộ đếm năm chạy nhanh, F2 = bộ đếm năm dưới-phải. Kênh hiện đặt năm dưới-**trái** (khung gib20/V5b-2b) → xác nhận vị trí.
3. **§10.6 Kinh thánh:** `docs/BIBLE-KENH2.md` trong repo chỉ có §1–9 — luật "người ≥ 10 m, không người ngã/chết" áp theo lệnh; đề nghị P ghi §10 vào Kinh thánh.
4. **Ảnh PD đúng phố** cho chiếu texture (§4.3) — cần Cowork/chủ dự án lấy (LoC bị Cloudflare chặn phiên).
5. **Nhánh:** cần tên `pt-khung-neo` thì P tạo từ commit cuối của nhánh này.
6. Ghi các đề xuất ngoài vùng §12 (RIGHTS, AUTHORSHIP, COST-LEDGER, verify.sh).
8. **Preflight `origin/main..HEAD` của nhánh `v5b2b` TRƯỢT 35 mục** (§14) — P xử lý trước khi merge v5b2b (và nhánh này, vì dựng trên v5b2b).
7. Nếu chọn H-B: chủ dự án quyết cách công bố AI (dòng chữ trên hình/mô tả) và có kiểm SynthID trên khung phim hay không (§8).

## 14. Preflight
- `bash tools/preflight.sh` (137 tệp staged) **ĐẠT**, `checks/lock.py --verify` **KHỚP**. Lần chạy đầu **TRƯỢT 1 mục**: email liên hệ của tác giả Quaternius nằm trong văn bản FAQ chép nguyên văn → đã che trong `giay-phep/quaternius-faq.txt` (ghi chú ngay chỗ che), chạy lại ĐẠT. Hook pre-commit/pre-push chạy lại khi commit/đẩy; không dùng `--no-verify`.
- `--range origin/main..HEAD` **TRƯỢT 35 mục** — cả 35 nằm trong nội dung `origin/v5b2b` (đã có trên remote; `--range origin/main..origin/v5b2b` cho đúng 35 mục: 5 tệp 13–16,5 MB ngoài LFS + 30 dòng thiếu tệp giấy phép ở `channel-k2/k2c-t1-06/SOURCES-*.csv`), **không phải tệp của PT**. Phần mới của phiên `--range origin/v5b2b..HEAD` (137 tệp) **ĐẠT**; hook pre-push cục bộ của phiên chạy đúng phạm vi này. Việc 35 mục của v5b2b → chờ P/V5b-2b (§13).

---

## 15. Nhánh C (H-C) — CHỈ NGHIÊN CỨU, KHÔNG dùng lên kênh (lệnh bổ sung 18/10)
> Làm sau khi xong A và B. Vùng tệp: `design/pt/**` + `reports/pt/ai-c/**` (+ `reports/pt/kiem-mu-abc/`, `reports/pt/to-khung-ABC.jpg`, bổ sung `giay-phep/openai.md`, `giay-phep/youtube-*.txt`). Trần OpenAI B + C ≤ $15.

### 15.1 Tóm tắt
1. **Ảnh tĩnh C: 6/6 xong** (1782 và 1943 × đầu/giữa/cuối của khung neo), `gpt-image-2.5-sunburst` qua **`POST /v1/images/edits`**, 2048×1152, `quality: high`, **$0,0624–0,0626/ảnh**; cả 6 có **C2PA `caBX`**. Mọi khung C gắn `ai_image: true` (`reports/pt/ai-c/goi-api.jsonl`).
2. **VIDEO C CHƯA CHẠY**: `sora-2`/`sora-2-pro` vẫn có trong `/v1/models`, nhưng tài liệu hiện hành ghi "The Sora 2 models and Videos API were shut down on September 24, 2026 and are no longer available. No one-to-one replacement API is available"; kiểm thật `GET /v1/videos` và `POST /v1/videos` đều **HTTP 404** (không tính phí). Không tìm đường khác (đúng lệnh).
3. **Trôi hình học (đo bằng máy, khung ngày):** C **giữ hình khối**: recall cạnh khối thô 0,87–0,93, chân trời lệch TB **0,1–1,7 px**, **0 toà biến mất, 0 đổi hình, 0 vùng xuất hiện** trên 4 khung ngày. Nhưng **độ chính xác cạnh tinh chỉ 0,20–0,55** → AI thêm/thay rất nhiều chi tiết nhỏ, và **hai tấm C cùng mốc kém nhất quán hơn hai tấm A** (IoU cạnh vùng nhà 0,50 vs 0,66; 0,48 vs 0,59) — đúng điểm yếu "đồ vật đổi giữa hai tấm" của đối thủ, ở mức đồ vật/người chứ không ở mức nhà.
4. **Lỗi dữ kiện: 4 lỗi chắc + 3 nghi vấn / 6 khung (≈ 0,67 lỗi chắc/khung).** Nặng nhất: **AI đổi cờ Union đúng mẫu 1707 của khung A thành mẫu 1801 ở cả 3 khung 1782** (prompt đã yêu cầu giữ nguyên cờ); thêm đèn sáng vào đêm phong toả 1943.
5. **Chấm mù ba nhánh (cùng khung, ẩn nhãn): C thắng 18/18 phiếu "đẹp nhất"**, craft **C 7,78** vs B 3,56 vs A 3,44; chi tiết C 8,44; đúng thời kỳ C 7,44 (dù có lỗi cờ); **"trông như ảnh AI": C 3,89 vs A/B 2,56** (1943: C 4,67). Cả 3 người **không bắt được** lỗi cờ ở C mà **gán nhầm** lỗi cờ cho cả A và B.
6. **Chi phí thật C: $0,383** (6 ảnh + 1 lệnh thử nhỏ + 2 lệnh lỗi 502 $0). **Tổng OpenAI B + C: $0,862 / $15.** Claude cả phiên **$2,641 / $3**.

### 15.2 Tài liệu + cách gọi (nguyên văn ở `giay-phep/openai.md` §5)
- Hướng dẫn: "Choose Sunburst for workflows where editing precision matters most" → chọn `gpt-image-2.5-sunburst` (cũng là mặc định của `/v1/images/edits`). `input_fidelity` "Supports high and low on gpt-image-1 and gpt-image-1.5… For gpt-image-2, omit" → **không có tham số giữ chi tiết cho dòng 2.5**; giữ bố cục chỉ bằng prompt (khối "KEEP EXACTLY UNCHANGED…", `design/pt/tools/gen_c.py`). Không dùng mask (mask = sửa vùng; lệnh cần thêm chi tiết khắp khung).
- Kích thước: 2048×1152 (bội 16, 16:9, dưới ngưỡng "experimental" 2560×1440); khung A 1920×1080 phóng LANCZOS, gửi JPEG q95; ảnh C thu về 1920×1080 để đo.
- **Đường truyền:** hai lệnh không stream đầu tiên bị **502 "upstream request failed" đúng 30,4 s** (không ảnh, $0); lệnh nhỏ 1088×608 `low` xong trong 14 s ($0,0082) → kết luận đường truyền cắt khi chờ > 30 s; chuyển sang `stream: true` + `partial_images: 1` (thêm 100 token ra/ảnh tạm, đã cộng vào chi phí) → 6/6 thành công (28,8–33,4 s).
- **"Tối đa 2 lần thử/ảnh":** mỗi ảnh C đúng **1 lần sinh**; riêng `1943-giua` có thêm 2 lệnh 502 không sinh ảnh — tính là lỗi đường truyền, không phải lần thử của model (ghi đủ trong sổ). Không dùng lần thử 2 vì không ảnh nào trượt ngưỡng trôi.
- Prompt nguyên văn từng ảnh (vật liệu/đồ vật/trang phục theo TIEN-KY; không tên người thật; giữ đúng MỘT cờ có sẵn; cấm chữ/biển hiệu/cờ mới/phù hiệu; người ≥ 10 m, không cận mặt, không người nằm) trong `goi-api.jsonl`. **API không có seed.**

### 15.3 Độ trôi hình học A → C (`design/pt/tools/drift_c.py`, `reports/pt/ai-c/do-troi.json`)
Thước: Canny tinh (60/150, dung sai 2 px) và thô (480×270, làm mờ, dung sai 1 px); SSIM bản đồ cạnh thô; mặt nạ "không phải trời" (A: lượt độ sâu; C: loang trời từ mép trên — **cùng bộ phân vùng chạy trên A để kiểm độ tin**, chỉ tính cột mà phân vùng A khớp độ sâu ≤ 3 px); từng toà theo **lượt mã toà** dựng lại từ cùng cảnh (hình học trùng từng mặt với nền A: 33 393 / 143 146 mặt).

| Khung | Canny tinh IoU / recall / precision | Canny thô IoU / recall | SSIM cạnh thô | SSIM xám thô | IoU không-trời (độ tin phân vùng A) | Chân trời lệch TB / p95 px (cột tin được) | Toà giữ / đổi hình / biến mất | Vùng xuất hiện |
|---|---|---|---|---|---|---|---|---|
| 1782 đầu | 0,278 / 0,884 / 0,307 | 0,294 / 0,871 | 0,624 | 0,756 | 0,998 (0,997) | 1,71 / 2,0 (96 %) | 3 / 0 / 0 | 0 |
| 1782 giữa | 0,190 / 0,920 / 0,198 | 0,252 / 0,901 | 0,605 | 0,721 | 0,999 (0,997) | 0,50 / 2,0 (97 %) | 3 / 0 / 0 | 0 |
| 1782 cuối (đêm) | 0,005 / 0,689 / 0,006 | 0,197 / 0,734 | 0,748 | 0,778 | 0,998 (0,995) | 30,1 / 292 (61 %) | 3 / 0 / 0 | 0 |
| 1943 đầu | 0,404 / 0,929 / 0,457 | 0,475 / 0,931 | 0,537 | 0,742 | 0,852 (0,847) | 0,14 / 1,0 (50 %) | 4 / 0 / 0 | 0 |
| 1943 giữa | 0,466 / 0,890 / 0,551 | 0,520 / 0,888 | 0,562 | 0,749 | 0,902 (0,854) | 0,08 / 0,0 (51 %) | 4 / 0 / 0 | 0 |
| 1943 cuối (đêm) | 0,030 / 0,888 / 0,034 | 0,151 / 0,748 | 0,642 | 0,488 | 0,517 (0,246) | 1,09 / 3,0 (9 %) | 3 / 1 / 0 | 0 |

- **Đọc:** recall cao + precision thấp = hình khối A còn nguyên, AI phủ thêm rất nhiều cạnh mới (vết bong vữa, gạch vụn, thùng, người). Khung **đêm không tin cậy** (A gần như không có cạnh; phân vùng trời chỉ tin 9–61 % cột) — "1 toà đổi hình" ở 1943 đêm (toà mã 7, recall 0,48 — ngay dưới ngưỡng 0,5) nằm trong nhóm không tin cậy; ghi, không kết luận.
- **Nhất quán giữa các tấm C cùng mốc** (IoU cạnh thô trong vùng nhà; đối chứng A–A cùng hình học, khác ánh sáng): 1782 đầu~giữa **C 0,501 vs A 0,655**; 1943 đầu~giữa **C 0,481 vs A 0,592**. Cặp có đêm: C cao hơn A (0,27–0,41 vs 0,11–0,31) vì C làm sáng đêm. ⇒ giữa hai tấm ngày, C **đổi đồ vật/người/vết bẩn** (thấy bằng mắt: số xe kéo, thùng, đống gạch, người khác nhau) dù nhà giữ nguyên.
- **Cùng một toà ở 1782 và 1943:** không có — hai mốc dựng từ hai nguồn khác nhau (Drinkwater vs OSM+AMS), không toà nào chung mã. Vật chung duy nhất là Line Wall + đường đồi bên kia vịnh; phân vùng trời **không tách được đồi mờ khỏi trời** (0 cột tin được) → **không đo được**, ghi là chưa đo.
- **Video:** không có (§15.1 mục 2) → không có số trôi theo thời gian 0/2/4/6/8 s.

### 15.4 Kiểm dữ kiện từng khung C (`reports/pt/ai-c/kiem-du-kien.json`)
| Khung | Lỗi chắc (sai thời kỳ / trái lệnh) | Nghi vấn | Đổi vật (không phải lỗi thời kỳ) |
|---|---|---|---|
| 1782 đầu | cờ Union mẫu **1801** (khung A: mẫu 1707, phóng to xác nhận) | — | pháo tiền cảnh → xe kéo chở thùng; tàu buồm xa đổi hình |
| 1782 giữa | cờ mẫu 1801 | — | thêm pháo dọc Line Wall |
| 1782 cuối | cờ mẫu 1801 | lính áo đỏ sáng rõ dưới trăng | — |
| 1943 đầu | — | tàu khách thân trắng ống khói cam (sơn thời bình; tàu thời chiến sơn xám) | tàu chiến đổi hình/vị trí |
| 1943 giữa | — | như trên | thêm xe tải mui bạt (hợp thời kỳ, không phù hiệu); xoá 2 người ~10–12 m |
| 1943 cuối | **đèn tường sáng** ở toà cuối phố — trái blackout và trái prompt | — | đêm sáng hơn A |
- **Tổng: 4 lỗi chắc + 3 nghi vấn / 6 khung.** Chữ giả: 0. Vật hiện đại rõ ràng: 0. Cách kiểm: rà tay 100–400 %, đối chiếu khung A cùng máy và mô tả nguồn TIEN-KY (Drinkwater 1786, Copley/Sharp, NARA 342-FH 1943). Phiên không có ảnh gốc của các nguồn đó trên máy (ngoài git, máy khác) → đối chiếu theo mô tả + khung A.
- **Bài học chính:** AI **kéo chi tiết về mẫu quen thuộc hiện đại** (cờ 1801), kể cả khi khung vào đã đúng và prompt cấm đổi; lỗi này nhỏ trên khung (≈ 30×25 px) nên **người chấm mù không bắt được** — mà còn gán nhầm cho A/B.

### 15.5 Chấm mù ba nhánh (`design/pt/tools/blind_abc.py`, `reports/pt/kiem-mu-abc/`)
Giao thức như §7.2: ghim `claude-sonnet-5-5`, chỉ Read, ba ảnh X/Y/Z hoán vị ngẫu nhiên (hạt giống 20261018), nhãn nhánh ẩn, 3 vai nguyên văn; 6 khung × 3 người = 18 phiếu.

| Mốc | Nhánh | craft | chi tiết | đúng thời kỳ | ai_look |
|---|---|---|---|---|---|
| 1782 (3 khung) | A | 2,67 | 2,11 | 3,78 | 2,44 |
| | B | 3,00 | 2,00 | 4,11 | 2,44 |
| | **C** | **7,67** | **8,33** | **7,22** | **3,11** |
| 1943 (3 khung) | A | 4,22 | 3,22 | 4,78 | 2,67 |
| | B | 4,11 | 3,00 | 4,78 | 2,67 |
| | **C** | **7,89** | **8,56** | **7,67** | **4,67** |
| **Cả 6 khung** | A / B / C | 3,44 / 3,56 / **7,78** | 2,67 / 2,50 / **8,44** | 4,28 / 4,44 / **7,44** | 2,56 / 2,56 / **3,89** |
- "Đẹp nhất": **C 18/18**. "Kém nhất": A 10/18, B 8/18.
- **Thang tương đối:** cùng khung A 1943 được craft **7,0** khi đặt cạnh B (§7.2) nhưng **4,2** khi đặt cạnh C — đọc theo bộ khung, không so tuyệt đối giữa các vòng.
- **"Trông như ảnh AI" tăng ở C** (+1,33 TB; 1943 +2,0, một khung 1943 giữa: 5/6/6). A và B bằng nhau.
- **Lỗi người chấm:** 1782 cả 3 người ghi "Union Jack with the St Patrick's cross (post-1801 design) in all three frames" — sai với A/B (đã phóng to), đúng với C; R3 còn ghi ngược "The Union flag with St Patrick's saltire is correct for 1782". ⇒ chấm mù bằng mô hình **không thay được kiểm dữ kiện**.
- Cặp đối thủ: không có khung đối thủ trong repo/API; điều phối tự so A/B/C với đối thủ trong chat (gợi ý dùng `reports/pt/to-khung-ABC.jpg`).

### 15.6 Chi phí thật từng lệnh gọi (OpenAI, nhánh C — `reports/pt/ai-c/goi-api.jsonl`)
| # | Ảnh | HTTP | Token vào (ảnh+chữ) | Token ra | $ | C2PA | Giây |
|---|---|---|---|---|---|---|---|
| 1 | 1943-giua (không stream, PNG) | 502 | — | — | 0 | — | 30,4 |
| 2 | 1943-giua (không stream, JPEG) | 502 | — | — | 0 | — | 30,4 |
| 3 | thử nhỏ 1088×608 `low` (không phải ảnh C) | 200 | 682 | 96 | 0,00823 | JPEG, không kiểm | 14 |
| 4 | 1943-giua | 200 | 1 850 | 1 522 | 0,06243 | có | 30,8 |
| 5 | 1782-dau | 200 | 1 856 | 1 522 | 0,06246 | có | 33,4 |
| 6 | 1782-giua | 200 | 1 856 | 1 522 | 0,06246 | có | 28,8 |
| 7 | 1782-cuoi | 200 | 1 877 | 1 522 | 0,06257 | có | 30,8 |
| 8 | 1943-dau | 200 | 1 850 | 1 522 | 0,06243 | có | 32,0 |
| 9 | 1943-cuoi | 200 | 1 873 | 1 522 | 0,06255 | có | 31,9 |
| | **Tổng C** | | | | **0,38313** | | |
- Tổng OpenAI phiên: B $0,47953 + C $0,38313 = **$0,86266 / $15**. Claude phiên: $1,467 (A|B) + $1,174 (A|B|C) = **$2,641 / $3**. Giờ máy thêm cho C ≈ 0,1 h (lượt mã toà 2 × ~10 s, khung A/B mới 2 × ~40 s, đo trôi ~1 phút) → **cả phiên ≈ 1,9 h / 4 h**.
- Dung lượng thêm: 6 PNG C gốc **20 MB** (mỗi tệp 2,7–4,1 MB < 5 MB, không LFS) + tờ khung A|B|C 0,65 MB.

### 15.7 Giờ người rà nếu dùng C (ước)
- Rà một ảnh C để bắt lỗi kiểu cờ 1801 cần phóng 400 % từng vật (cờ, tàu, đèn, trang phục): **≈ 4–6 phút/ảnh** (phiên này: 6 ảnh ≈ 30 phút có đối chiếu khung A); ≈ 0,67 lỗi chắc/ảnh → sửa lại (≤ 2 lần thử) thêm ≈ 3 phút/ảnh.
- C **không dùng được cho video liên tục** (đồ vật/người đổi giữa hai tấm, §15.3; không có API video). Chỉ dùng được như **ảnh tĩnh Ken Burns**: 1 phút phim ≈ 15–30 ảnh (2–4 s/ảnh) ⇒ **≈ 1,5–4,5 giờ người/phút phim** (ước), chưa gồm kiểm nguồn cho từng chi tiết AI thêm (không có nguồn nào cho các thùng/xe/người do AI đặt).

### 15.8 Rủi ro công bố AI — chính sách YouTube hiện hành (nguyên văn trong `giay-phep/youtube-disclosing-genai.txt`, đọc 18/10; chỉ dữ kiện)
- "We require creators to disclose AI-generated or altered content that seems realistic… Creators must disclose GenAI content that… Generates a realistic scene that didn't actually occur."
- Ví dụ phải công bố có: "AI generated extra footage of a real place, like a video of a surfer in Maui for a promotional travel video". Ví dụ không cần: "Color adjustment or lighting filters", "Video sharpening, upscaling or repair", "AI generating or extending a backdrop to simulate a moving car".
- "YouTube may automatically apply an AI label… for: Content made using YouTube's GenAI tools · Content that contains C2PA metadata · Content that our internal systems detect is AI generated or altered… content containing C2PA metadata… can not be adjusted."
- "Creators who consistently choose not to disclose this information may be subject to manual application of a label, or penalties from YouTube, including removal of content or suspension from the YouTube Partner Program." · "Disclosing AI content alone won't limit a video's audience or impact its eligibility to earn money."
- Chính sách kiếm tiền (`giay-phep/youtube-monetization-policies.txt`): nội dung phải "Not be mass-produced, generic, repetitive, or manipulative" (cập nhật 15/7/2025: "repetitious content" đổi tên "inauthentic content").
- Dữ kiện liên quan PT: 6/6 ảnh C và 9/9 vân B có C2PA khi tải về; OpenAI nói ảnh có SynthID trong điểm ảnh; khung C là cảnh tả thực về nơi có thật, năm có thật, với chi tiết do AI đặt.

### 15.9 Đề xuất A / B / C
| Phương án | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|
| **A (không AI) — đề xuất cho kênh** | mọi chi tiết có nguồn hoặc ghi "procedural"; cờ/đồ vật đúng mẫu do người đặt; hình nhất quán tuyệt đối giữa tấm; giữ "No AI imagery"; $0 API | chấm cạnh C thua xa (craft 3,4 vs 7,8); người thủ tục "búp bê"; khung trống | tiếp tục §10 (người, bố cục, 1782) | khoảng cách chất lượng thấy được với kênh dùng AI |
| B (vân AI) | rẻ | không hơn A (3,56 vs 3,44 cạnh C; thua A ở vòng A\|B); C2PA | như §11 | như §8 |
| C (sửa ảnh AI) — **chỉ nghiên cứu** | chi tiết/craft cao nhất (7,8; 18/18 đẹp nhất); giữ hình khối (recall 0,87–0,93, chân trời ≤ 1,7 px, 0 nhà mất); rẻ ($0,06/ảnh) | **0,67 lỗi chắc/khung**, gồm sửa SAI cái A đã đúng (cờ 1801), người chấm không bắt được; đồ vật đổi giữa tấm; không seed; không video (API ngừng); đêm bị làm sáng | nếu dùng: thêm 1,5–4,5 giờ người rà/phút (ước), dán nhãn AI | công bố AI bắt buộc theo YouTube (cảnh tả thực, nơi có thật); nhãn tự động do C2PA không gỡ được; nghĩa vụ kiểm nguồn cho chi tiết AI tự thêm |
| Hướng lai để nghiên cứu tiếp (không lên kênh khi chưa duyệt) | dùng C làm **bảng tham chiếu** cho người dựng A (vết bong vữa, mật độ đồ vật, cách bày) rồi dựng lại bằng A | thêm giờ dựng | học "mật độ chi tiết" mà không có điểm ảnh AI lên hình | thấp (C không lên hình) |

### 15.10 Chỉ số trong ±5 % quanh ngưỡng (bổ sung)
- Toà mã 7 ở **1943 đêm**: recall cạnh thô **0,481** vs ngưỡng "đổi hình" 0,5 (−3,8 %) — trong ±5 %, nằm ở khung đêm không tin cậy.
- Claude phiên **$2,641 / $3** (88 %); không chỉ số nào khác trong ±5 %.

### 15.11 Việc chờ chủ dự án (bổ sung)
9. Quyết định A/B/C (§15.9) — đề xuất: kênh giữ **A**; C chỉ là bảng tham chiếu nội bộ, không lên hình.
10. Nếu muốn video C: OpenAI đã ngừng Videos API (24/9/2026) — cần chủ dự án quyết có xét nhà cung cấp khác hay không (lệnh cấm phiên tự tìm đường khác).
11. RIGHTS/AUTHORSHIP: ghi rằng 6 ảnh C + 9 vân B là ảnh AI **chỉ nghiên cứu**, không vào gói phát hành.
