**Nhánh thật: `dong-goi-t3-v2`** (đúng lệnh), tạo từ `origin/dong-goi-t3` @7b983213. Harness gán `claude/wonderful-lamport-ydmmb4`; mọi commit cũng đẩy sang nhánh đó, cùng SHA. **Không merge.**

# ĐÓNG-GÓI-T3 vòng 2 — nâng chất lượng thumbnail (V7B + AI tăng cường + ảnh thực) — BÁO CÁO (DỪNG chờ chủ dự án)

> **Phiên:** 19/10/2026, UTC ≈ 15:25 → 16:50.
>
> **Đã đọc:** `reports/dong-goi-t3/DONG-GOI-T3-BAO-CAO.md` (toàn văn), `PACKAGING-BRIEF.md`, `reports/v7b/V7B-BAO-CAO.md` (nhánh `origin/ccr-ef2b66f0-9639kq`), `reports/m3/BAI-HOC-LL.md`.
>
> **Vùng sửa:**
> - `channel-k2/k2c-t3-01/phat-hanh/`: chỉ thêm `PACKAGING-BRIEF-v2.md` và `titles-v2.txt`.
> - `reports/dong-goi-t3-v2/**`: 13 MB, không LFS.
>
> Máy dựng V7B chạy trong worktree tạm ở scratchpad. Hai bản vá tạm, **không commit**: `noRim` (tắt viền phe quanh tàu cho thumbnail) và tái dùng bộ đệm `k2tl-cache` + `buildings-v7b.json` (`v7b_mau_nha.py`).
>
> **Preflight:** ĐẠT, LOCK KHỚP. Không có email trong tệp, header, URL hay payload. UA trung tính. Khoá do proxy gắn (OpenAI) hoặc lấy từ biến tiến trình con (Claude), không in, không ghi.

## §0 Tóm tắt
| Việc | Kết quả |
|---|---|
| **1. Khung gốc V7B 4K** | Đêm 13/9/1782 23:40 từ vịnh, máy thấp (25–45 m). **10 pin nổi** thành vật thể rõ: thân gỗ, lửa, khói, cờ hải quân TBN nhỏ, phản chiếu trên nước. Phố 1782 và cờ Union trên lâu đài theo V7B. Kèm khung 2026 đêm **cùng điểm máy**, và khung 2026 đêm điểm D có **đèn đường băng** + nhà có vật liệu.<br>**Rock chiếm ≈ 28 % khung** (đường trời ở 45 % chiều cao, mặt nước ở ≈ 74 %): **chưa đạt mục tiêu ≥ 35 %** (§1). |
| **2. [F] AI tăng cường** | 4 ảnh gpt-image-2.5-sunburst-2026-09-08 (sửa ảnh từ khung gốc), C2PA 4/4, **$0,303**.<br>F1, F2, F3 dùng được, sau khi **ghép lại điểm ảnh gốc cho 3 cờ** (AI đã biến cờ Union thành đốm đèn).<br>**F4 bị loại**: AI tự thêm chi tiết kiến trúc vào nhà 2026 (§11.3). Không ảnh nào sai lịch sử kiểu pin nổi thành tàu hiện đại. |
| **3. [E] Ảnh thực** | 2 ảnh Flickr **CC BY 2.0**, giấy phép kiểm trên trang Flickr. **Cả hai chụp năm 2008, không phải 2026**, nên dải năm ghi "1782 → TODAY". Wikimedia Commons trả 429 (BAI-HOC #82); tìm qua Openverse. |
| **4. Ứng viên** | 8 ứng viên V1…V8 + 2 mốc A2/B1 vòng 1 = 10 ảnh, tên trung tính X01…X10:<br>• [F]: 4 bản (V1, V2, V3, V8) + V7 ghép [F] với dựng thuần;<br>• [E] + dựng ghép chéo: 2 bản (V4, V5);<br>• dựng thuần V7B đối chứng: V6.<br>Thử hai cỡ chữ: V1 (S, 8 %) và V8 (M, 11,5 %), cùng ảnh. |
| **5. Kiểm** | Ở 168×94, OCR đọc đúng "GIBRALTAR" và năm ở cả 10/10 ảnh. Tương phản chữ 9,8–19,0:1.<br>**Khớp phim:** pin nổi cháy có ở **26,96 s** của V7B (≤ 30 s), nhưng **góc máy thumbnail (từ vịnh) không phải góc máy trong phim** (phim nhìn từ điểm K trên sườn Rock).<br>Chấm mù cỡ nhỏ: **A2 vòng 1 8,0 muốn bấm**; V7 7,0; V5 7,0 ("trông như AI" thấp nhất 4,0); B1 vòng 1 6,67; khung đêm toàn cảnh xa 4,0–5,0. |
| **6. Tiêu đề c5** | **Hứa quá.** 12/14 cuộc vây chỉ là bước bộ đếm ≈ 0,46 s; chấm "lời hứa khớp nội dung" chỉ **4,0/10**. Đề xuất **"Gibraltar: From 14 Sieges to a Runway \| 3D Timelapse"** (khớp 6,33; trung lập 9,0) hoặc "Gibraltar, 1309–2026: 14 Sieges, Then a Runway \| 3D" (khớp 6,67, điểm top 3 cao nhất). |
| **7. Xuất cho điều phối** | `thumbnail/xuat-dieu-phoi/X01…X10-{1280x720,360x202,168x94}.png`, tờ gộp `thumbnail/to-ung-vien-X01-X10.jpg`. Khoá ở `thumbnail/khoa.json`; không mở trước khi chấm. |
| **Chi phí** | Claude **$0,486** · OpenAI **$0,303** · YouTube 0 · ElevenLabs 0 · giờ máy ≈ 0,8 h. |

## §1 Khung gốc (việc 1) — máy V7B (`tl/t3tl`, hero.js, llvmpipe, 3840×2160 SPP 3, ≈ 24–27 s/khung)

Opt lấy từ shot V7B (H1 2026 đêm; H2 1782: `fires`, `fleets` có `phe` và cờ, `co` cờ Union/Borgoña, phố 1782, `buildings-v7b.json`). Thời điểm giữ cố định. Máy riêng cho thumbnail.

| Khung | Thời điểm | Máy (E, cao, N → nhìn; fov) | Dùng ở | SHA (ngoài git `/var/tmp/cine-out/dong-goi-t3-v2/khung/`) |
|---|---|---|---|---|
| N12 | 13/9/1782 23:40 | [−2450, 45, −900] → [−750, 200, −1600]; 26° | V1, V3, V4, V6, V8 (gốc của F1) | `684d8123…` |
| N12_2026 | 18/10/2026 23:52 | như N12 (opt H1 + nhà V7B) | V3 nửa phải (gốc của F3) | `4cc8bae7…` |
| N2r | 13/9/1782 23:40 | [−1950, 25, −1150] → [−600, 180, −1600]; 46° | V2, V5, V7 (gốc của F2) | `7fe933be…` |
| D2026n | 18/10/2026 23:52 | [330, 210, 640] → [−200, 20, −350]; 44° (gần H1 V7B) | V7 nửa phải (dựng thuần) | `0c90dabf…` |

- **Soi trước ở 540p**, 13 góc máy (N1…N12, P): `noRim` tắt viền elip màu phe quanh tàu. Viền này là dấu kiểu bản đồ trong phim; ở thumbnail nó đọc thành vạch vàng trên nước.
- **Rock ≥ 35 %: CHƯA ĐẠT.**
  - Hình học không cho cả hai cùng lúc. Muốn Rock lớn phải dùng tele từ ≥ 2 km; khi đó pin nổi chỉ còn đốm.
  - N12 (fov 26) là điểm cân bằng: Rock ≈ 28 % khung (nét trời 45 %, mặt nước ≈ 74 % chiều cao).
  - N2r (cận) cho pin nổi lớn, nhưng Rock chỉ ≈ 16 %.
- **Phố 1782 ban đêm không có đèn** (đúng V7B: đèn phố chỉ từ năm ≥ 1950). Rock và phố tối, nên AI tăng cường (§2) chủ yếu làm rõ vân đá.

## §2 [F] AI tăng cường (việc 2) — `ai/goi-api.jsonl` (prompt nguyên văn), tờ so `ai/so-*.jpg`, số đo `ai/so-ai.json`

**Cách làm:**
- `POST /v1/images/edits`, `gpt-image-2.5-sunburst-2026-09-08` (cùng bản ghim với PT3). Model trả về đúng bản đó.
- Tham số: `quality high`, 2560×1440, JPEG q90, `stream` + `partial_images 1`.
- Prompt **chỉ cho tăng chi tiết bề mặt**: giữ bố cục, đường chân trời, số và vị trí vật. Cấm thêm vật, người, cờ, chữ, đèn mới.

| Ảnh | Gốc | Chi phí | C2PA | Phần AI đổi (xem cận) | Kết luận |
|---|---|---|---|---|---|
| F1 | N12 1782 | $0,076 | có | vân vách đá + cây bụi trên Rock; lửa thành ngọn lửa thật có tàn; khói dày hơn; sóng + phản chiếu lửa. Thân pin nổi và cờ TBN nhỏ giữ nguyên; **8 pin nổi trong khung ở cả hai bản** (2 chiếc ngoài mép phải, như khung gốc) | **DÙNG** (V1, V3, V8) |
| F2 | N2r 1782 | $0,076 | có | như F1, cộng tàn lửa; **3 cờ Union (tháp lâu đài, 2 pháo đài Line Wall) bị AI đổi thành đốm đèn** → **ghép lại điểm ảnh gốc** (elip 60 × 60 px @2560, mép mềm) tại vị trí chiếu từ toạ độ cảnh (`ai/co-px.json`; khớp đốm sai ±4 px). Bóng tàu đen giữa khung giữ nguyên; 7 pin nổi + 1 ở mép trái như gốc | **DÙNG** sau rào chắn (V2, V7) |
| F3 | N12 2026 | $0,076 | có | vân đá; ánh cửa sổ và phản chiếu đèn trên nước rõ hơn; vân mặt tiền nhẹ. Không thêm toà/tàu | **DÙNG** (V3 nửa phải) |
| F4 | D2026n | $0,076 | có | đèn đường băng giữ; **thêm mặt tiền cổ điển/ban công cho nhà 2026, thêm bọt sóng ở đầu đường băng**, thêm vệt phản chiếu đèn trên vịnh | **LOẠI** — §11.3: "chi tiết kiến trúc AI tự thêm = không chấp nhận". V7 dùng khung dựng thuần thay |

- **Lỗi API trước khi chạy được:** 1 × HTTP 400 (`input_fidelity` không hỗ trợ ở model này) và 2 × HTTP 502 (chế độ không stream). Sau 2 lần cùng lỗi 502, tôi **đổi cách sang stream** như PT3, không thử lần 3. Ba lệnh lỗi không tính tiền.
- **Đo chênh** |ΔL\*| > 12: dải trời 0–3 %, Rock/phố 4–8 %, nước 13–27 % (`so-ai.json`). Số đốm cam do máy đếm (16→19, 29→26) lẫn cả phản chiếu, **không dùng để đếm pin nổi**. Số pin nổi ở trên là đếm tay trên tờ cận.

## §3 [E] Ảnh thực (việc 3) — `nguon-anh.json`
| Mã | Ảnh | Tác giả | Giấy phép | Chụp | SHA | Dùng |
|---|---|---|---|---|---|---|
| a3d5740d | "Gibraltar Sunrise", flickr.com/photos/7860611@N06/2182420583 | axmiller | CC BY 2.0 | 4/1/2008 | trong json | V4 nửa phải |
| 1cc4493e | "The Rock of Gibraltar", flickr.com/photos/35042256@N00/2962358067 | BY-YOUR-⌘ | CC BY 2.0 | 11/9/2008 | trong json | V5 nửa phải |

- **Nguyên văn deed CC BY 2.0** (đọc 19/10) có trong json: "…for any purpose, even commercially… Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made…".
- **Không người nhận diện được:** người nhỏ ở mép trái ảnh 1cc4493e nằm dưới nửa dựng.
- **Lệnh xin ảnh 2026 ban đêm/hoàng hôn: không tìm được ảnh có giấy phép rõ.** Mọi kết quả Openverse đều cũ, và Commons bị chặn 429. Dùng ảnh 2008 với dải năm "TODAY" là cách trung thực nhất; Rock không đổi, nhưng phố đã đổi.
- **RIGHTS đề xuất (phiên P ghi):**
  - `DG3V2-PH1 | "Gibraltar Sunrise" (axmiller, Flickr 2182420583) | Ảnh | CC BY 2.0 | cắt + ghép thumbnail | SHA trong nguon-anh.json`
  - `DG3V2-PH2 | "The Rock of Gibraltar" (BY-YOUR-⌘, Flickr 2962358067) | Ảnh | CC BY 2.0 | …`
  - `DG3V2-AI | 3 ảnh gpt-image-2.5-sunburst-2026-09-08 (F1–F3), sửa ảnh từ khung tự dựng, C2PA; quyền đầu ra theo OpenAI Services Agreement §4.1 (như dòng PT3)`

## §4 Ứng viên (việc 4) — `thumbnail/mo-ta.json`, `thumbnail/khoa.json`
| Ứng viên | Mã | Nội dung | Chữ |
|---|---|---|---|
| V1 | X09 | [F] F1 toàn khung đêm 1782 | "1704 → 2026" · GIBRALTAR **S** (8,3 %) |
| V2 | X01 | [F] F2 cận | M (11,5 %) |
| V3 | X07 | [F] F1 ↔ F3 chéo, cùng điểm máy | "1782 → 2026" · S |
| V4 | X03 | [E] dựng N12 ↔ ảnh bình minh 2008 | "1782 → TODAY" · S |
| V5 | X05 | [E] dựng N2r ↔ ảnh La Línea 2008 | "1782 → TODAY" · M |
| V6 | X04 | **đối chứng dựng thuần V7B** N12 | S |
| V7 | X08 | [F] F2 ↔ dựng thuần D 2026 (đèn đường băng) | "1782 → 2026" · M |
| V8 | X02 | = V1 nhưng chữ M (cặp thử cỡ) | M |
| A2 vòng 1 | X06 | mốc | — |
| B1 vòng 1 | X10 | mốc | — |

- **An toàn:** không người; lửa chỉ trên pin nổi; không vũ khí; cờ nhỏ, không phải điểm nhấn; AI không vẽ chữ (chữ đặt bằng mã).

## §5 Kiểm cỡ nhỏ (việc 5)
- **OCR cục bộ (RapidOCR):**
  - Ở 168×94, đọc được "GIBRALTAR" 10/10 và năm 10/10. Mũi tên đôi khi mất ở 168, không ảnh hưởng.
  - Ở 360×202, đọc đủ.
- **Tương phản WCAG:** dải năm 9,8–10,2; "GIBRALTAR" 18,1–19,0 (`thumbnail/do-chu.json`).
- **Khớp nội dung phim:**
  - Sự kiện đêm 13→14/9/1782 với 10 pin nổi cháy có trong phim: mở đầu V7B, cháy ở **26,96 s**.
  - Nhưng **phim nhìn từ điểm K trên sườn Rock xuống vịnh**, còn thumbnail nhìn **từ vịnh về Rock**. Cùng sự kiện, cùng vật 3D, khác góc máy.
  - Nửa 2026 của V7 gần như trùng H1 (điểm D).
  - **N12_2026 (V3) không có trong phim.**
  - Ảnh thực (V4, V5) không có trong phim. Phim không dùng footage 2026.

## §6 Chấm mù cỡ nhỏ — `thumbnail/cham-mu/gop.json` (3 người chấm như vòng 1, claude-sonnet-5-5; lưới 360×202 + 168×94)
| Mã | Ứng viên | Muốn bấm | Rõ | Trung lập | Trông như AI (0–10) | Đọc ở 168 | TB 4 (không tính AI) | Điểm top 3 | Muốn bấm lượt 1* |
|---|---|---|---|---|---|---|---|---|---|
| X06 | A2 vòng 1 | **8,00** | 8,33 | 9,00 | 4,00 | 8,00 | **8,33** | **9** | 7,00 |
| X08 | **V7** [F]+dựng | 7,00 | 7,33 | 8,33 | 5,67 | 8,00 | **7,67** | 3 | 7,33 |
| X05 | **V5** [E]+dựng | 7,00 | 7,33 | 7,33 | **4,00** | 7,00 | 7,17 | 3 | 7,00 |
| X10 | B1 vòng 1 | 6,67 | 7,33 | 8,33 | 5,67 | 7,67 | 7,50 | 1 | 6,33 |
| X03 | V4 [E] | 6,33 | 6,67 | 7,33 | 4,33 | 6,33 | 6,66 | 2 | 6,33 |
| X01 | V2 [F] | 6,00 | 6,33 | 8,00 | 5,33 | 8,00 | 7,08 | 0 | 5,67 |
| X07 | V3 [F] | 5,33 | 5,67 | 8,00 | 5,33 | 6,00 | 6,25 | 0 | 5,33 |
| X02 | V8 [F] chữ M | 5,00 | 6,33 | 8,00 | 5,33 | 7,33 | 6,66 | 0 | 4,67 |
| X04 | V6 dựng thuần | 5,00 | 6,33 | 8,00 | 5,33 | 7,33 | 6,66 | 0 | 4,67 |
| X09 | V1 [F] chữ S | 4,00 | 5,33 | 8,00 | 5,33 | 6,33 | 5,91 | 0 | 3,67 |

\* Lượt 1 (`cham-mu/lan1-truoc-thay-V7/`) chấm V7 dùng F4, trước khi F4 bị loại. Cùng ảnh mà điểm chênh tới ±1,0 giữa hai lượt (A2: 7,0 → 8,0), nên **sai số người chấm ≈ ±1**.

**Đọc kết quả:**
- **Người chấm AI xem từng ảnh riêng, không trong lưới ban ngày đồng phục.** Vì vậy kết quả này **không thay** nhận xét lưới thật của điều phối, rằng ảnh đêm tách khỏi lưới rõ nhất.
- **AI tăng cường không làm ảnh "trông như AI" hơn:** F1 5,33 = dựng thuần V6 5,33.
- **Ảnh thực hạ "trông như AI"** (V5 4,0; V4 4,33).
- **Khung đêm xa** (V1/V6/V8) thua rõ, dù có AI: pin nổi quá nhỏ ở 360 px. **Khung cận (N2r)** mới đọc được.
- **Cỡ chữ:** M thắng S ở cùng ảnh (V8 5,0 so với V1 4,0; lượt 1: 4,67 so với 3,67). Kết quả này **ngược** đặc trưng "chữ khổng lồ đi cùng điểm thấp" của quét ngách. Nhưng M (11,5 %) vẫn nhỏ hơn trung vị đối thủ (17,5 %); n = 3 người chấm.
- **V7 so B1 vòng 1:** muốn bấm +0,33, rõ bằng, đọc ở 168 +0,33. Cải thiện có thật nhưng **nằm trong sai số**.

## §7 Kiểm tiêu đề c5 (việc 6) — `tieu-de/kiem-c5.json`
- **V7B mở đầu (H2):** sau 2026, bộ đếm **bước** qua 1309, 1316, 1333 (×2), 1350, 1411, 1436, 1462, 1467, 1506, 1704, 1705, 1727, 1779 → 1782.
  - Mỗi bước giữ 11 khung = **0,458 s**, kèm một nhịp khói trên phố (`sieges: true`).
  - Riêng 4/8/1704 dài 2,5 s (cờ hạ–kéo).
  - Đêm 13/9/1782 chạy liên tục.
- **Vậy phim có cho thấy cả 14 cuộc vây bằng 3D, nhưng 12/14 chỉ là chớp ≈ 0,5 s.** Chỉ 1704 và 1779–83 được kể dài.
- **Chấm mù:** 3 người chấm đọc **tóm tắt trung thực nội dung phim** (nguyên văn trong json) rồi chấm 6 biến thể.

| Tiêu đề | Ký tự | Muốn bấm | Rõ | **Hứa khớp nội dung** | Trung lập | Điểm top 3 |
|---|---|---|---|---|---|---|
| c5 Gibraltar: 14 Sieges in 3D \| Timelapse 1309–2026 | 48 | 7,33 | 8,00 | **4,00** | 9,00 | 2 |
| **Gibraltar, 1309–2026: 14 Sieges, Then a Runway \| 3D** | 51 | 6,67 | 6,67 | 6,67 | 9,00 | **7** |
| **Gibraltar: From 14 Sieges to a Runway \| 3D Timelapse** | 52 | 6,67 | 6,67 | 6,33 | 9,00 | 6 |
| Gibraltar: 700 Years Fought Over, in 3D \| 1309–2026 | 51 | 5,67 | 6,33 | **7,00** | 6,67 | 3 |
| c1 Gibraltar Under Siege: 1309 → 1783 \| 3D Timelapse | 49 | 5,67 | 7,33 | 4,00 | 8,33 | 0 |
| a2 Why Gibraltar Was Besieged 14 Times | 35 | 7,67 | 8,33 | 2,67 | 8,33 | 0 |

**Đề xuất:** CHÍNH = **"Gibraltar: From 14 Sieges to a Runway \| 3D Timelapse"**.
- Giữ mã thể loại "3D Timelapse", mà quét ngách vòng 1 cho thấy đi cùng điểm cao.
- Lời hứa nêu đủ hai nửa phim (vây hãm và đường băng).
- Dự phòng: "Gibraltar, 1309–2026: 14 Sieges, Then a Runway \| 3D" (điểm top 3 cao nhất, nhưng mất chữ "Timelapse").
- c1 và a2 cũng hứa quá. Không dùng.

## §8 Chi phí thật
| Khoản | Mốc / chặn | Thật | Ghi |
|---|---|---|---|
| Claude API | $3 / $10 | **$0,486** | 9 lệnh claude-sonnet-5-5: chấm thumbnail 2 lượt × 3, kiểm c5 × 3 → `cost.jsonl` |
| OpenAI | $6 / $10 | **$0,303** | 4 ảnh × $0,076 (gpt-image-2.5-sunburst-2026-09-08, HTTP 200, C2PA 4/4) + 3 lệnh lỗi $0 → `ai/goi-api.jsonl` |
| YouTube Data API | ≤ 200 | **0** | — |
| ElevenLabs | 0 | **0** | — |
| Giờ máy | 4 h | **≈ 0,8 h** | ≈ 26 khung 540p soi + 4 khung 4K + ghép, OCR; ước từ log, không đo đồng hồ |

**Chỉ số trong ±5 % quanh ngưỡng:** không có.
- Rock 28 % so với mục tiêu 35 % (−20 %): **trượt**, không phải sát ngưỡng.
- Cỡ PNG lớn nhất 1,48 MB so với 2 MB.

## §9 Quyết định đề xuất
| # | Đề xuất | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|---|
| Q1 | Đổi tiêu đề CHÍNH c5 → "Gibraltar: From 14 Sieges to a Runway \| 3D Timelapse" | Không hứa quá (khớp 6,3 so với 4,0); vẫn có mã thể loại | Muốn bấm −0,7 so với c5 | `titles-v2.txt`; dòng 1 mô tả giữ | Chấm AI ≠ CTR thật |
| Q2 | Bộ thumbnail thử: **V7 (X08) · V5 (X05) · A2 vòng 1 (X06)** | V7 giữ hướng đêm + lửa mà điều phối thấy nổi giữa lưới, chi tiết hơn B1; V5 trông ít AI nhất; A2 là đối chứng ngày | V7/V5 chỉ hơn B1 trong sai số người chấm; V5 dùng ảnh 2008 ("TODAY") | Thay B1 vòng 1 bằng V7 | Kết quả lưới thật của điều phối có thể đảo thứ tự. **Chọn sau lưới thật** |
| Q3 | Dùng AI tăng cường cho thumbnail **chỉ kèm rào chắn**: ghép lại điểm ảnh gốc cho cờ và vật mang dữ kiện; loại ảnh tự thêm kiến trúc | Chi tiết bề mặt tốt hơn mà "trông như AI" không tăng (5,33 = dựng thuần) | 1/4 ảnh bị loại; AI tự biến cờ thành đèn | Thêm câu khai báo thumbnail trong mô tả | Bình luận chê AI (đo §11.3, ≤ 2 %) |
| Q4 | Bỏ khung đêm xa (V1/V6/V8); khung đêm phải **cận** pin nổi | Đọc được ở điện thoại | Rock nhỏ hơn (≈ 16 %) | — | — |
| Q5 | Nếu muốn ảnh thực đúng 2026: chủ dự án tự chụp, hoặc mua ảnh có giấy phép thương mại | Đúng năm | Tốn công/tiền | — | — |
| Q6 | Cỡ chữ tên nơi: giữ **M (11,5 %)** | Thắng S ở cùng ảnh (n = 3) | Ngược tương quan quét ngách | — | Kiểm lại bằng lưới thật |

## §10 Việc chờ chủ dự án
1. **Chọn 3 thumbnail** sau khi điều phối đặt X01…X10 vào lưới tìm kiếm thật. Đề xuất: X08 (V7) · X05 (V5) · X06 (A2).
2. **Duyệt đổi tiêu đề CHÍNH** c5 → "Gibraltar: From 14 Sieges to a Runway \| 3D Timelapse" (Q1).
3. **Duyệt dùng AI trên thumbnail kèm rào chắn** (Q3), và câu khai báo thêm trong mô tả.
4. **Quyết ảnh thực 2008 với nhãn "TODAY"**, hay tìm ảnh 2026 (Q5).
5. **Phiên P ghi RIGHTS** (3 dòng đề xuất §3) và AUTHORSHIP (lựa chọn tiêu đề, thumbnail).
6. Phiên P merge nhánh khi duyệt.

**DỪNG — chờ chủ dự án.**
