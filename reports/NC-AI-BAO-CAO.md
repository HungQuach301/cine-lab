Nhánh thật: `ccr-fcb0e150-g16lfi`. Harness của phiên chỉ định nhánh này; lệnh xin `nc-ai`. Nhánh tạo lại từ `origin/main` @ `6c16e548`.

# NC-AI — Dùng AI rộng hơn để tăng chất lượng và độ chân thực kênh 2, không bịa dữ kiện — BÁO CÁO

> Phiên nghiên cứu NC-AI, 18/10/2026, theo lệnh chủ dự án (đã duyệt AI-A, AI-B lúc 20:14). Phiên chỉ viết tài liệu và chạy thử nhỏ để kiểm, không dựng phim. **Không merge. DỪNG chờ chủ dự án.**
> Mọi số trong báo cáo là số đo thật trong phiên (tệp ở `reports/nc-ai/`), trừ chỗ ghi rõ **(ước)**. Báo cáo không chứa email hay khoá API.
> Nguyên tắc kiểm cho mọi mục: bỏ AI ra mà dữ kiện trên hình đổi thì không được dùng.

## Khối điều lệ (lệnh và thực tế)
| Trường | Lệnh | Thực tế |
|---|---|---|
| Loại phiên | Nghiên cứu: tài liệu + thử nhỏ | Đúng lệnh. Không dựng phim, không render |
| Nhánh | `nc-ai` từ `origin/main` | `ccr-fcb0e150-g16lfi` từ `origin/main` @ `6c16e548` (harness buộc; ghi ở dòng đầu) |
| Tệp được sửa | CHỈ `reports/NC-AI-BAO-CAO.md` + `reports/nc-ai/**`, tổng ≤ 10 MB | Chỉ hai vùng này, ≈ 1,1 MB. Không sửa `scripts/`, `design/`, `checks/`, `docs/`, `channel-*/` hay nhánh khác. Chỉ **đọc** tệp `channel-k2/k2c-t3-01/**` và đọc nhánh PT bằng `git show` |
| Chi phí | Không trần cứng. Mốc theo dõi: Claude $3, OpenAI $3. Dừng an toàn: Claude > $15, OpenAI > $20 | OpenAI **$0,1607**. Claude: **≈ 0,57 triệu token** ở 5 subagent (đo), cộng phiên chính; xem §8, có dòng lợi ích. YouTube **0**, ElevenLabs **0** |
| Preflight | Bắt buộc; che email; không in hay ghi khoá | `tools/preflight.sh` chạy trước commit cuối (§10). Khoá OpenAI do proxy gắn, mã không đọc biến khoá. Đã che email trong mọi tệp nguồn đưa vào repo |
| Đẩy việc dở | Sau mỗi phần hoặc tối đa 30 phút | 3 lần đẩy (`931bf617`, `fea841f0`, commit cuối) |
| Môi trường | `verify.sh` | 9 PASS, 5 FAIL không liên quan: OpenEXR, three.js, tifffile/pyshp, k2v node_modules, Freesound 403. Cài thêm cho thử nghiệm: venv riêng trong scratchpad (torch CPU 2.14.1, transformers 5.20.1, mediapipe 1.1.1) và apt `tesseract-ocr` 5.3.4, `libgles2`. Không đụng `/opt/cine` |

---

## §0. Tóm tắt (đọc 2 phút) + bảng quyết định đề xuất

**Kết luận chung.** AI giúp nhiều nhất ở **khâu đọc và số hoá**: đọc nguồn, trích nguyên văn, chép trang, vẽ bao khối nhà khi người click chỉ định. Ở các khâu đó, mọi kết quả đều kiểm lại được bằng máy, đối chiếu với tệp có SHA. AI rủi ro nhất ở **khâu sinh điểm ảnh**: phóng to ảnh khắc, sinh video. Ở các khâu này AI tự thêm nét, và người chấm (kể cả mô hình chấm) không bắt được.

Số đo chính trong phiên:

1. **AI-B (a) Gibraltar 9/1782.** Đọc 9 trang (Drinkwater 1786 tr. 351–353, Spilsbury 1908 tr. 73–75, Ancell 1784 tr. 253–255). Cả 3 tệp tải lại đều **khớp SHA** của TIEN-KY.
   - Lượt 1: `gpt-6.1-sol` trích **82 mục**, chi phí $0,0915, chạy 132 s.
   - Kiểm máy câu trích: **80/82 khớp nguyên khối**, 2 gần khớp (gạch nối cuối dòng, dòng bảng).
   - Lượt 2: Claude Sonnet, lượt riêng. Bước A đọc độc lập khi chưa thấy lượt 1, được 15 mục, cả 15 đều có trong lượt 1. Bước B kiểm từng mục của lượt 1: **62 đúng · 16 sai loại · 3 sai ngày · 1 hiểu quá · 0 bịa · 0 sai trang**. Phiên P đọc lại 6/20 mục bất đồng và đồng ý với lượt 2 ở cả 6.
   - ⇒ **0 % mục bịa, 1,2 % hiểu quá, 3,7 % sai ngày, 19,5 % sai loại**. Không có mục **trang phục** nào: 9 trang này không tả quần áo. Vì vậy trang phục phải lấy từ bậc 3–4, không lấy được từ nhật ký.
2. **AI-B (b) London 1666.** Nguồn: Pepys (Gutenberg #4167) và Evelyn (#42081), các mục 2–7/9/1666, có SHA.
   - Được **20 mục**, **20/20 khớp nguyên khối**, $0,0448.
   - Kiểm lượt 2 bằng Opus (phiên P): 17 đúng, 2 sai loại, 1 đúng nhưng dễ dựng sai. "night-gowne" của Pepys là áo choàng mặc nhà thế kỷ 17, không phải váy ngủ hiện đại.
   - 0 bịa. Mô hình **không điền ngày** cho mục nào (0/20); ngày lấy được từ mục nhật ký.
3. **AI-1 vector hoá khối phố** trên Drinkwater 1786, ô phố đã dùng ở SH, so với 22 khối SH dò tay:
   - Hai cách **tự động hoàn toàn** (không học máy) đều **trượt**: IoU hợp ≤ 0,40, **0/22** khối đạt IoU ≥ 0,5. Lý do: chữ khắc đè và nét viền đứt.
   - **SAM ViT-B (Apache-2.0), người click 1 điểm mỗi khối:** IoU trung vị **0,754**, **19/22 ≥ 0,5**, 16/22 ≥ 0,7, 5/22 ≥ 0,85. Mỗi click 0,08 s trên CPU. 3 khối hỏng: hai khối bị chữ "Lt Governor" và "GIBRALTAR" đè, một khối có điểm click rơi vào ô nhà đậm.
   - ⇒ Dùng được làm **bán tự động** (người chọn khối, máy vẽ bao, người sửa khoảng 15 % số khối). Không dùng được để phát hiện tự động.
4. **AI-1 OCR** (trang Ancell 254, 103 từ, đáp án do P chép tay từ ảnh trang):

   | Cách đọc | WER (nới) |
   |---|---|
   | OCR sẵn của IA | 0,175 |
   | Tesseract 5.3.4 `eng` | 0,379 (vỡ do lề ngày tháng) |
   | `gpt-6.1-sol` nhìn ảnh | **0,000**, giữ ſ, $0,024 |

   Mô hình nhìn còn **sửa được đáp án của P**: bản in ghi "aſſidiouſly", P chép nhầm "aſſiduouſly".
5. **AI-2 (a) ước tư thế** bằng MediaPipe Pose Landmarker (Apache-2.0, CPU 0,04 s/khung) trên phim NARA 37058 (CC0, bản IA 320×240):
   - Chỉ **7,5 %** khung mẫu (558 khung, mỗi 3 s một khung) phát hiện được người.
   - Đoạn liên tục 8 s: 0 % khung mất dấu, nhưng rung p95 = 0,24 chiều cao người/khung².
   - Đoạn "nhiều người nhất" mà máy chọn lại là **footage màu thập niên 1980** chèn trong phim 1981. ⇒ Phải gắn thời kỳ cho từng đoạn footage **trước** khi lấy chuyển động.
6. **AI-3 phục chế bản khắc** (Drinkwater 1786 leaf 427, có đáp án: thu nhỏ ×4 rồi phóng lại):
   - Swin2SR ×4 (Apache-2.0) có PSNR **16,10 < bicubic 16,38**, SSIM 0,348 > 0,289.
   - Nhìn bằng mắt: Swin2SR **biến nét gạch khắc thành vệt loang và thêm mảng tối trên mặt người lính** (bịa nét).
   - Độ sâu Depth Anything V2 Small (Apache-2.0, 8,5 s): thứ tự trời/xa/gần hợp lý (disparity trên 0,07, dưới 0,91), 2,6 % điểm ảnh ở bước nhảy độ sâu. Lề giấy bị coi là "gần".
7. **Tài liệu hiện hành** (4 gói tra cứu, ≈ 230 URL đọc ngày 18/10, nguồn ở `reports/nc-ai/nguon/`):
   - OpenAI Videos/Sora **đã tắt 24/9/2026**.
   - Video AI qua API còn sống: Veo 3.1, Runway gen4.5, Luma Ray3.2, MiniMax H3. Giá ≈ $0,20–1,20 cho mỗi 4–6 s.
   - Bị loại vì NC/SA/vùng lãnh thổ: CodeFormer, SUPIR, GFPGAN (phần StyleGAN2 NC), Depth Pro, DA2 Base/Large, SMPL (kéo theo 4DHumans/WHAM/TRAM), OpenPose, YOLO-pose (AGPL), AMASS, LaFAN1, Bandai Namco, AudioGen, Tango, HunyuanVideo (loại trừ EU/UK).

### Bảng quyết định đề xuất (xếp theo lợi ích/rủi ro, cao → thấp)
| # | Mục | Đề xuất | Ưu | Nhược | Tác động | Rủi ro dữ kiện → cách kiểm bằng máy |
|---|---|---|---|---|---|---|
| 1 | **AI-B + AI-1 đọc nguồn** (trích vật/hoạt động/mật độ người, chép trang, dịch hai phía) | **DÙNG NGAY** ở mọi tiền kỳ (T4 London, T5) | 0 bịa / 102 mục; 100 % câu trích có thật; ≈ $0,01/trang; chép trang WER 0 trên trang sạch | Sai loại 19 %, sai ngày 4 %; không điền ngày khi ngày nằm ở đề mục; không cho trang phục | Rút việc đọc khoảng 9 trang/giờ người xuống vài phút máy + 1 lượt rà (ước) | Mọi mục phải qua `aib_kiem_trich.py` (khớp nguyên văn trong tệp SHA). Lượt 2 bằng mô hình khác. Mục lệch ngày/loại không lên hình khi chưa có người duyệt |
| 2 | **Lớp kiểm** (kiểm chéo nhiều mô hình, soi lỗi thời đại, đo bình luận) | **DÙNG**, nhưng chỉ làm lưới lọc thứ hai | Bắt được 20 lỗi nhỏ ở lượt 1; rẻ | Mô hình nhìn soi lỗi thời đại chỉ đạt 58,7 % (TAB-VLM 2026, §6) | Thêm cổng tự động cho claim | Không thay kiểm nguồn (bài học PT §15.5); đo được bằng tỷ lệ bất đồng giữa hai lượt |
| 3 | **AI-1 vector hoá bán tự động** (SAM 1 click/khối) | **DÙNG** cho ghost T4 London | IoU trung vị 0,754; 0,08 s/click; Apache-2.0 | Chữ khắc đè làm hỏng khoảng 15 % số khối | Rút công dò tay (ước 2–3 phút/khối → khoảng 0,5 phút/khối) | Người click thì khối do người chọn; IoU với bản dò tay trên ô mẫu ≥ 0,7 mới nhận lô; vẽ chồng lên bản đồ để rà |
| 4 | **AI-A 5 bậc tái dựng có căn cứ** (quy tắc, không phải công cụ) | **ĐƯA VÀO KINH THÁNH** (§9) | Biến "không bịa" thành sổ kiểm được (mỗi phần tử có bậc + nguồn) | Thêm cột vào bảng shot | Đề tài thời kỳ xa chỉ vào hàng đợi khi đủ bậc 1–3 | Phép thử "bỏ AI ra" kiểm được bằng cột bậc |
| 5 | **AI-4 âm thanh**: Freesound CC0 là chính; ElevenLabs SFX (gói trả phí) cho tiếng khó tìm | **THỬ CÓ ĐIỀU KIỆN** (chấm mù tai) | Không vướng NC; đầu ra thuộc người dùng (ToS ElevenLabs) | Đơn vị tính tiền SFX trên trang giá ElevenLabs mâu thuẫn; Freesound API dùng thương mại phải "negotiated" → tải tay | Không khí thời kỳ dày hơn | SFX AI có thể lẫn âm hiện đại (động cơ, máy) → soi lỗi thời đại bằng tai + phổ; mỗi SFX ghi RIGHTS |
| 6 | **AI-2 sự sống**: mocap mở (CMU, 100STYLE CC BY, Quaternius CC0) + động tác theo điều lệnh PD | **DÙNG** dữ liệu mở; **CHƯA** dùng ước tư thế từ footage | Dáng đi/khiêng thật hơn búp bê (điểm yếu số 1 ở PT4) | Mocap hiện đại ≠ dáng người thế kỷ 18 → chỉ dùng cho đi/đứng/khiêng; động tác quân sự theo bản khắc điều lệnh | Giảm toy_like (PT4 vẫn 6,67) | Không có dữ kiện trong dáng đi; động tác súng phải khớp bản khắc tư thế (1764 / Ordenanzas 1762) — so tay |
| 7 | **AI-3 phục chế ảnh/tranh lưu trữ** (khử nhiễu, làm nét ×2) | **CHỈ** cho ảnh chụp thế kỷ 20 có nhãn; **KHÔNG** cho bản khắc | YouTube xếp "upscaling or repair" vào nhóm không cần công khai | Bản khắc bị thêm nét giả (đo được); bản quét của ta đã 3 000–9 000 px nên không cần phóng | Nhỏ | Kiểm có đáp án (thu nhỏ → phóng → so gốc); cạnh mới > 5 % → loại |
| 8 | **2,5D parallax ảnh lưu trữ** | **GIỮ CẤM** trong Kinh thánh; mở phiên thử riêng nếu chủ dự án muốn | DA2-Small chạy CPU 8,5 s, thứ tự độ sâu hợp lý | Tách người khỏi nền tạo rìa giả; YouTube không có ví dụ cho trường hợp này; "Alters footage of a real event or place" có thể áp | Thêm chuyển động cho ảnh tĩnh | Độ sâu do AI suy ra là dữ kiện không có nguồn (cái gì đứng trước cái gì); bậc 5 |
| 9 | **AI-5 video image-to-video** (biển, trời, khói xa) | **CHƯA DÙNG**; chỉ giữ tài liệu | Rẻ (Veo 3.1 Lite $0,05–0,08/s) | Phải công khai AI; C2PA/SynthID gắn nhãn tự động không gỡ được; không có khoá trong môi trường; OpenAI đã tắt | Ít, vì cảnh biển/trời dựng được bằng Blender | Thước đo trôi/nhấp nháy §5; chỉ dùng khi chủ dự án duyệt nhà cung cấp |

---

## §1. AI-1 Nghiên cứu + số hoá

### 1.1 Công cụ hiện hành (chi tiết, giấy phép nguyên văn: `reports/nc-ai/nguon/R1-ai1-ai3.md`)
| Việc | Chọn | Giấy phép (nguyên văn rút gọn) | Chạy trong phiên cloud | Loại |
|---|---|---|---|---|
| OCR sách in thế kỷ 17–18 | **kraken 7.1.1** + mô hình CATMuS-Print (Zenodo 10592716, "CC-BY-4.0", giữ ſ); **Tesseract 5.3.4** (apt; `enm`, `deu_latf` có ſ, còn `eng` không có) | Apache-2.0 | Có (đã cài và chạy Tesseract) | Surya: trọng số "AI PUBS OPEN RAIL-M LICENSE (MODIFIED)", ngưỡng doanh thu 5 triệu USD + share-alike lên Output → **không dùng** |
| Chép trang bằng mô hình nhìn | `gpt-6.1-sol` (API, khoá do proxy gắn); mở: Qwen3-VL 2B/4B (Apache-2.0), Florence-2 (MIT) | — | Có (API); mô hình mở chưa đo trên CPU | Qwen2.5-VL-3B "Qwen RESEARCH LICENSE" (NC) |
| Vector hoá bản đồ | **SAM / SAM 2** (Apache-2.0 cho cả mã lẫn checkpoint) + QGIS/GDAL | Apache-2.0 / GPL-2 (đầu ra không bị ràng buộc) / MIT | Có (đã chạy SAM ViT-B) | SAM 3: "SAM License", checkpoint gated (HF trả 401) |

Các nguồn đọc ngày 18/10/2026:
- `raw.githubusercontent.com/mittagessen/kraken/main/LICENSE`
- `zenodo.org/api/records/10592716`
- `raw.githubusercontent.com/facebookresearch/sam2/main/LICENSE`
- `huggingface.co/Qwen/Qwen3-VL-*`
- `arxiv.org/html/2510.27547v1`: MapSAM2. IoU 10-shot trên Building Block ICDAR 2021: "MapSAM2 75.8, U-Net 60.0, PerSAM 16.0" → SAM không tinh chỉnh mà để tự động thì không đủ, khớp với số đo của phiên.

### 1.2 Thử vector hoá (`tools/ai1_vector.py`, `tools/ai1_sam.py`, `ai1/`)
Ảnh thử: Drinkwater 1786 "Plan of the Batteries", IA `historyoflatesie00drin/page/leaf373.jpg`. **SHA `476cb89b…555117` khớp** `tai-san-vay-ham.json`.

Ô so sánh: hộp bao các khối và nhà vùng `pho` của SH, cộng lề 60 px (px 270–1378 × 1215–1615). Chuẩn so là 22 khối phố trong `so-hoa-1782-px.json`.

| Cách | Khối máy | IoU hợp | Khối tay đạt IoU ≥ 0,5 / ≥ 0,7 | IoU từng khối (trung vị) | Khối thừa | Ghi chú |
|---|---|---|---|---|---|---|
| Mật độ chấm, ngưỡng 0,06 / 0,10 / 0,14 | 11 | 0,401 / 0,308 / 0,103 | 0 / 0 · 1 / 0 · 0 / 0 | 0,061 / 0,094 / 0,018 | 7 / 6 / 5 | Khối dính nhau qua phố; vườn, sườn đồi cũng chấm → thừa |
| Vùng kín bởi nét viền, ngưỡng 0,03–0,09 | 1–3 | ≤ 0,047 | 0 / 0 | 0 | — | Nét viền khắc đứt, chữ lớn cắt vùng |
| **SAM ViT-B, 1 click/khối** | 22 | **0,669** | **19 / 16** | **0,754** (TB 0,692; 5 khối ≥ 0,85) | — (người chọn khối) | Nạp mô hình 8,1 s, mã hoá ảnh 10,8 s, **0,08 s/click**. Hỏng: K1782-07 (0,08, chữ "Lt Governor"), K1782-15 (0,07), K1782-01 (0,21, click rơi vào ô nhà đậm) |

- Ảnh kiểm: `ai1/sam-1click.jpg` (đỏ = SH dò tay, xanh lá = SAM, chấm lam = điểm click) và `ai1/so-sanh-matdo-T0.06.jpg`.
- **Lưu ý về chuẩn so.** Khối SH là khối dò tay có `do_tin` cao, vừa hoặc thấp; nó không phải "sự thật". IoU ở đây đo **độ khớp với cách người dựng đọc bản đồ**.

### 1.3 Thử OCR có đáp án (`ai1/ocr/`, `tools/ai1_wer.py`)
- **Trang:** Ancell 1784, tr. 254 = IA `acircumstantial00ancegoog/page/n267.jpg`. SHA ảnh `d3960f33…982256`, đọc 18/10. Phiên dò trang bằng cách cho Tesseract đọc số trang các lá n258–n270.
- **Đáp án:** P chép tay 103 từ nửa trên trang. Đã sửa 1 từ P chép sai sau khi đối chiếu ảnh: "aſſidiouſly".

| Cách đọc | WER nới (ſ/f→s) | WER chặt | Chi phí |
|---|---|---|---|
| OCR djvu sẵn của IA (tệp SHA `67d61d0a…`) | 0,175 | 0,243 | $0 |
| Tesseract 5.3.4 `eng`, cả trang | 0,379 | 0,427 | $0, vài giây |
| **`gpt-6.1-sol` nhìn ảnh, chép theo dạng in gốc** | **0,000** | **0,000** | $0,0244, 14,5 s |

**Đọc kết quả.** Một trang in sạch thì chưa đủ để kết luận về chữ viết tay hay trang mờ.

**Rủi ro.** Mô hình nhìn có thể "chuẩn hoá" chữ (ſ→s, hiện đại hoá chính tả) hoặc điền chữ ở vùng mờ. Lần này nó không làm vậy; nó còn bắt được lỗi của người.

**Luật đề xuất.**
- Chép bằng mô hình nhìn chỉ là **tệp làm việc**, ghi SHA của **ảnh trang**.
- Câu trích lên hình phải đối chiếu ảnh trang (như luật 7 claim "khớp theo mảnh" của TIEN-KY).
- Chạy lượt chép thứ hai bằng mô hình khác; chữ lệch giữa hai lượt thì người đọc ảnh.

### 1.4 Tìm mâu thuẫn số liệu
Phiên không chạy thử riêng. Cơ chế đã có sẵn trong TIEN-KY: 21 claim MÂU THUẪN, ghi hai phía. Lượt AI-B có thể gắn cờ tự động khi hai nguồn cho số khác nhau cho cùng một vật/ngày. Ví dụ đã thấy trong 9 trang: Ancell ghi trại TBN "56,000 men", còn TIEN-KY ghi Drinkwater "gần 40 000" và Montero 33 000. Đề xuất: lượt AI-B xuất thêm cột `so` và `don_vi`; script so cùng `vat + ngay` giữa các nguồn.

### 1.5 Ước giờ người tiết kiệm cho T4 London 1666 (ước)
| Việc | Không AI (ước) | Có AI (ước) | Căn cứ |
|---|---|---|---|
| Đọc nhật ký/văn bản lấy vật, hoạt động, mật độ người (≈ 60 trang Pepys + Evelyn + Vincent + Rege Sincera) | ≈ 15 phút/trang → ≈ 15 h | Máy ≈ 1–2 phút/9 trang + kiểm máy + rà 20 % mẫu ≈ 3–4 h | AI-B: 9 trang → 82 mục trong 132 s; lượt 2 ≈ 2 phút |
| Chép trang khó đọc (Gazette 85, Vincent 1667 bản quét) | ≈ 20–30 phút/trang | ≈ 3–5 phút/trang (2 lượt mô hình + so lệch) | §1.3 |
| Ghost khối phố trong vùng cháy (Hollar 1666 / Ogilby & Morgan 1676) | ≈ 2–3 phút/khối dò tay | ≈ 0,5 phút/khối (click + sửa khoảng 15 %) | §1.2; số khối London chưa đếm |

**Tổng (ước): tiết kiệm khoảng 60–70 % giờ đọc và số hoá cho T4.** Phần còn lại là việc của người: chọn khối, rà mẫu, đối chiếu ảnh trang.

---

## §2. AI-2 Sự sống có căn cứ (`reports/nc-ai/nguon/R2-ai2.md`)

### 2.1 (a) Ước tư thế từ footage tư liệu thập niên 1940
**Công cụ duy nhất sạch giấy phép + CPU + không SMPL:** MediaPipe Pose Landmarker. Model card ghi "LICENSED UNDER Apache License, Version 2.0"; mô hình cho 33 điểm 3D, z tương đối.

Các công cụ bị loại:
- OpenPose (NC).
- Ultralytics YOLO-pose (AGPL, cả trọng số).
- SMPL/SMPL-X: "production of other artefacts for commercial purposes" bị cấm. Vì vậy 4DHumans/WHAM/TRAM (mã MIT nhưng cần SMPL) cũng bị loại.
- GVHMR (NC).
- MotionBERT: trọng số học trên Human3.6M "academic use only".

Chưa rõ: giấy phép trọng số RTMPose/ViTPose (mã Apache-2.0).

**Thử** (`tools/ai2_pose.py`, `ai2/ket-qua.json`). Footage: NARA ARC 37058 "The story of Hoover Dam", IA `gov.archives.arc.37058_512kb.mp4`, licenseurl CC0, đã có giấy phép trong `k2c-t4-01/licenses/`; SHA `d7096f84…55cc2a`. Thông số: 320×240, 29,97 fps, 27,6 phút.

| Đo | Kết quả |
|---|---|
| Khung mẫu 1/3 s có ≥ 1 người | **7,5 %** (42/558); trung bình 1,05 người khi có |
| Tốc độ | 0,04 s/khung (CPU) |
| Đoạn 8 s nhiều người nhất (máy chọn, 1207,6 s) | 0 % mất dấu; rung (gia tốc khớp hông/gối/cổ chân ÷ chiều cao người) trung vị 0,024, **p95 0,239** |
| Nội dung đoạn đó | **footage màu thập niên 1980** (phim làm năm 1981) — không phải 1930s |

**Kết luận.**
- Bản IA 512kb quá nhỏ cho người ở cảnh xa. Bản MPEG2 gốc 1,35 GB chưa thử.
- Rung p95 lớn ⇒ cần lọc mượt trước khi chuyển sang rig MPFB.
- Rủi ro dữ kiện lớn nhất **không nằm ở mô hình** mà ở **chọn sai đoạn footage khác thời kỳ**.
- ⇒ Nếu dùng: chỉ lấy **nhịp và dáng** (tốc độ đi, khiêng) từ đoạn đã gắn năm bằng tay. Không lấy động tác cụ thể làm dữ kiện.

### 2.2 (b) Thời kỳ không có footage
**Mocap mở dùng được:**
- CMU Graphics Lab: "You may include this data in commercially-sold products, but you may not resell this data directly".
- 100STYLE: CC BY 4.0.
- Quaternius Universal Animation Library: CC0.

Mixamo và Rokoko mới có nguồn thứ cấp (trang FAQ Mixamo 403) → chờ đọc gốc.

**Mocap bị loại:** Bandai Namco (CC BY-NC), LaFAN1 (BY-NC-ND), AMASS, HumanML3D, SFU, Motorica (NC); KIT chưa rõ.

**Điều lệnh PD** (URL archive.org trong R2):

| Nước, thế kỷ | Nguồn |
|---|---|
| Anh thế kỷ 18 | *The Manual Exercise as ordered by His Majesty in 1764* (bản gắn CC0); Bland *Treatise of Military Discipline* 1727–1746; Muller *Treatise of Artillery* 1768/1780 |
| Tây Ban Nha thế kỷ 18 | *Ordenanzas* 1762 tomo II (archive.org `A303417`, Public Domain Mark, "XVI h. de grab. pleg." = 16 tờ khắc thao tác súng); *Ordenanzas* 1768 (PDM). Ảnh BNE/BDH: CC BY 4.0 |
| Anh thế kỷ 17 | Hexham 1637; Barriffe 1635–1661; Elton 1650/1659/1668 |

- Văn bản EEBO-TCP Phase I là CC0, nhưng: "This waiver does not extend to any page images" → hình tư thế lấy từ bản quét archive.org.
- Dundas 1792 muộn hơn Gibraltar 1779–83 → **không dùng** làm chuẩn.

**Vân trang phục:**

| Mức | Nguồn |
|---|---|
| Dùng được | Rijksmuseum (CC0/PD); The Met (CC0 theo từng mục); Smithsonian (chỉ mục gắn CC0); Anne S.K. Brown (Brown Univ., "No Copyright - United States"); ảnh tranh 2D theo PD-Art (Commons dẫn án THJ v Sheridan 2023 cho Anh) |
| Hạn chế | Royal Collection Trust; National Army Museum (CC BY-NC-ND); V&A (thu phí thương mại); London Museum ("© London Museum", cấm cả dùng cho AI) |
| Chưa rõ | Museo del Ejército; Europeana (theo từng mục) |

**Rủi ro dữ kiện.**
- Mocap hiện đại có dáng người hiện đại → chỉ dùng cho người nền ở xa ≥ 10 m.
- Động tác quân sự phải khớp bản khắc điều lệnh đúng nước, đúng năm. Kiểm bằng máy: đo góc khớp của rig so với góc trên bản khắc (đã nắn) ở 3–5 tư thế khoá; lệch > 15° → sửa (đề xuất, chưa thử).

---

## §3. AI-3 Hồ sơ thật (`tools/ai3_phuc_che.py`, `ai3/`)

### 3.1 Công cụ và giấy phép (R1 §C)
| Mức | Công cụ |
|---|---|
| Dùng được | Real-ESRGAN (BSD-3); SwinIR, HAT, Swin2SR (Apache-2.0); NAFNet, Restormer, waifu2x, BOPBTL, DeOldify (MIT); MiDaS, ZoeDepth (MIT); Depth Anything V2 **Small** và DA3 Small/Base/Mono-Large (Apache-2.0) |
| Loại | CodeFormer ("S-Lab License 1.0", NC); SUPIR (NC); GFPGAN (StyleGAN2 kèm NVIDIA "non-commercially"); Depth Pro ("exclusively for Research Purposes"); DA2 Base/Large/Giant và DA3 Large/Giant (CC BY-NC 4.0) |

YouTube (support.google.com/youtube/answer/14328491, đọc 18/10, tiêu đề "Disclosing use of GenAI content") xếp vào nhóm KHÔNG cần công khai: "Video sharpening, upscaling or repair and voice or audio repair", "Color adjustment or lighting filters". Nhóm PHẢI công khai: "Alters footage of a real event or place", "Generates a realistic scene that didn't actually occur".

### 3.2 Thử phục chế có đáp án
**Ảnh:** Drinkwater 1786 "A View from Gibraltar of the Spanish Batteries", IA leaf427. **SHA `bb057d4f…` khớp TIEN-KY.**

**Cách làm:** cắt 6 ô 256×256 (hạt giống 20261018); thu nhỏ ×4 rồi phóng lại ×4.

| | PSNR | SSIM | Cạnh máy có cạnh gốc trong 2 px |
|---|---|---|---|
| bicubic | 16,38 | 0,289 | 1,000 |
| Swin2SR ×4 (Apache-2.0) | **16,10** | 0,348 | 0,996 |

Nhìn bằng mắt (`ai3/phuc-che-goc-bicubic-swin2sr.jpg`, cột gốc / bicubic / Swin2SR):
- Swin2SR **biến nét gạch song song thành vệt loang**.
- Swin2SR **vẽ thêm mảng tối trên mặt và áo người lính** mà bản khắc không có. Đây là bịa nét ở mức chi tiết, đúng kiểu lỗi PT §15.4.
- Bicubic mờ nhưng không thêm gì.

Thử ×4 từ 64 px là ca khó cố ý. Bản quét của ta đã 3 000–9 000 px, nên thực tế **không cần phóng to bản khắc**. Chỉ ảnh chụp thế kỷ 20 độ phân giải thấp mới cần.

**Tô màu:** giữ luật §11.5 (chỉ khi có nguồn màu + nhãn "colourised"). DeOldify (MIT) chạy được nhưng màu là suy đoán → bậc 5.

### 3.3 2,5D parallax cho ảnh/tranh lưu trữ — đánh giá nới luật
**Thử:** Depth Anything V2 Small (`ai3/do-sau-da2s.jpg`), 8,5 s/ảnh trên CPU.
- Trời xa (disparity trung vị 1/5 trên 0,068), tiền cảnh gần (0,911).
- Bờ và đồi xếp lớp hợp lý.
- 2,61 % điểm ảnh ở bước nhảy độ sâu > 0,02: chỗ đó rách hoặc giãn khi trượt máy.
- **Lề giấy và dải chữ bị coi là "gần"**, phải cắt trước.

**Rủi ro.**
1. Độ sâu là **dữ kiện suy ra không có nguồn**: ai đứng trước ai, bờ cách bao xa. Bản khắc vốn đã có phối cảnh lý tưởng hoá.
2. Tách lớp người khỏi nền làm lộ vùng nền "sau lưng người" → phải vẽ bù bằng AI (bịa).
3. YouTube: parallax ảnh thật có thể rơi vào "Alters footage of a real event or place". Trang không có ví dụ nào về trường hợp này.

**Đề xuất:** **GIỮ CẤM** ước độ sâu bằng AI trên hình phát hành. Thay bằng máy trượt 2D + nhãn neo (đã có §10.8). Nếu chủ dự án muốn thử: một phiên riêng với các rào sau:
- chỉ tranh/bản khắc có ≥ 3 lớp tách bằng tay (người dựng vẽ mặt nạ lớp, AI chỉ ước độ sâu **trong** từng lớp);
- biên độ trượt ≤ 1,5 % bề ngang;
- không vẽ bù vùng bị lộ (giữ biên độ đủ nhỏ để không lộ);
- nhãn "Archival image · depth effect" cùng dòng nguồn;
- chấm mù có câu "trông AI".

---

## §4. AI-4 Âm thanh thời kỳ (`reports/nc-ai/nguon/R3-ai4-ai5.md`)

| Nguồn | Giấy phép / điều khoản (nguyên văn rút gọn, đọc 18/10) | Giá | Kết luận |
|---|---|---|---|
| **Freesound CC0** | CC0 1.0; cấm nhận là tác giả. Dùng thương mại qua API: "negotiated on a case by case basis with UPF" | $0 | **Chính.** Tải tay từng tệp CC0, ghi RIGHTS (verify.sh: Freesound 403 từ phiên cloud) |
| ElevenLabs Sound Effects (`POST /v1/sound-generation`, `eleven_text_to_sound_v2`, 0,5–30 s, có loop) | ToS 09/10/2026: "you retain all rights in and to your Output"; gói miễn phí chỉ phi thương mại | Trang giá "$0.12"/phút ↔ FAQ "per generation" — **mâu thuẫn**, cần đo 1 lần | **Thử có điều kiện** cho tiếng khó tìm (pháo xa, đám đông 1666) |
| Stable Audio Open | Stability Community License, ngưỡng "USD $1,000,000 in annual revenue"; dữ liệu học có CC Sampling+ | tự chạy | Dự phòng; rủi ro gốc dữ liệu |
| AudioGen, AudioLDM 2, Tango 2 | CC-BY-NC / cc-by-nc-sa-4.0 | — | **Loại** |
| Giọng đọc trích nhân chứng: ElevenLabs TTS | "v4"/"v3"/"v2 Multilingual" $0,08/1K ký tự; "Flash/Turbo" $0,04. Cấm nhân bản giọng "of any living individual" và người đã mất "in a manner that is reasonably likely to cause harm"; có SynthID | ≈ $0,08 cho 1 000 ký tự trích | **Dùng giọng tổng hợp chung** (không mô phỏng giọng Pepys/Drinkwater). Lời đọc = trích nguyên văn có nguồn + nhãn "read by synthetic voice" |

**Rủi ro dữ kiện của âm thanh AI:** lẫn âm hiện đại (động cơ, còi, máy) và nhạc cụ sai thời. Cách kiểm:
1. Soi phổ: tìm vạch ổn định 50/60 Hz và hài của động cơ.
2. Nghe mù có câu "âm nào không thuộc năm X".
3. Mỗi SFX AI vào sổ AI (model, prompt, chi phí).

Chất lượng AI so CC0: **chưa đo**; §11.5 đã ghi "đo trước". Đề xuất: chấm mù tai 5 cặp, mỗi cặp một SFX AI và một CC0, trong phiên âm thanh G1b T3.

---

## §5. AI-5 Video AI có rào — CHỈ TÀI LIỆU (không gọi API video)

| Nhà cung cấp | Còn sống (18/10) | Giá ≈ 5 s | Quyền đầu ra (nguyên văn) | Watermark/C2PA |
|---|---|---|---|---|
| Google Veo 3.1 (`veo-3.1-generate-preview`/`-fast-`/`-lite-`) | Có (preview); Veo 3.0 "Deprecated" | Lite 720p 4 s $0,20; Fast $0,10–0,12/s; Std $0,40/s; 1080p chỉ 8 s | "won't claim ownership" | SynthID |
| Runway gen4.5 / gen4_turbo | Có | $0,60 / $0,25 | "does not claim ownership", "does not restrict your commercial use" | chưa đọc được |
| Luma Ray3.2 | Có | 720p $0,30; 1080p $1,20 | Customer "owns and retains all right, title, and interest in and to the Output"; thương mại chỉ khi đang thuê bao | — |
| MiniMax H3 | Có | $0,08/s ≈ $0,40 | chưa đọc | — |
| Kling 3.0, Seedance 2.0, Pika | Có (thứ cấp) | $0,42–1,87 (thứ cấp) | chưa đọc gốc | — |
| Wan 2.2 (mở) | trọng số có | GPU tự chạy | "licensed under the Apache 2.0 License" | — |
| LTX-2 (mở) | có | — | doanh thu ≥ $10 000 000/năm phải mua giấy phép | — |
| HunyuanVideo-I2V | có | — | "excluding … European Union, United Kingdom and South Korea" → **loại** | — |
| **OpenAI Sora / Videos API** | **ĐÃ TẮT 24/9/2026** (trang deprecations) | — | — | — |

**Phạm vi nếu được duyệt:**
- Chỉ cảnh không mang dữ kiện: biển, trời, khói ở xa ≥ 2 km, không tàu, không bờ có công trình.
- Khung đầu là render của mình.
- ≤ 4 s mỗi lần.
- Tính vào trần AI ≤ 20 % (§11.3).
- Bật công khai AI trên YouTube.

**Thước đo bằng máy** (kế thừa PT §15.3 và PT3):
1. Ghép lại điểm ảnh A cho mọi vùng bảo vệ (đường chân trời có đồi, bờ, công trình); sai khác < 1/255.
2. Trôi hình: IoU cạnh Canny thô trong vùng không-trời giữa khung 0 và khung 2/4/6/8 s ≥ 0,85; đường chân trời lệch ≤ 2 px.
3. Nhấp nháy: chiếu ngược t→t+1 theo luồng quang học trên vùng AI; |Δ| trung bình ≤ 1,1× nền A; tỷ lệ điểm chớp (|Δ| > 12) ≤ 2 % (PT3: A 0,90–2,05 %).
4. Kiểm C2PA đầu ra bằng `c2patool` ("MIT OR Apache-2.0") và ghi vào sổ AI.
5. Rà mắt 100 % khung có xuất hiện vật mới (tàu, chim, cờ) → loại.

**Đề xuất:** **CHƯA DÙNG**, vì biển/trời/khói xa dựng được bằng Blender mà không phải công khai AI hay chịu nhãn C2PA. Mở lại khi chủ dự án duyệt nhà cung cấp và có khoá trong môi trường.

---

## §6. Lớp kiểm (`reports/nc-ai/nguon/R4-london-kiem.md` phần 2)

1. **Kiểm dữ kiện chéo nhiều mô hình.** Phiên này thử đúng cơ chế đó ở AI-B: GPT trích, máy khớp nguyên văn, Claude kiểm từng mục và đọc độc lập, P phân xử mẫu.
   - Số đo: lượt 2 bắt 20/82 vấn đề (sai loại, sai ngày, hiểu quá), 0 bịa.
   - Tài liệu: Wu et al. 2025 (Nature Communications) cho thấy "between 50% and 90%" câu trả lời y khoa có trích dẫn không được nguồn ủng hộ đầy đủ; bộ kiểm tự động đạt "88.7% agreement" với bác sĩ. Magesh et al. 2024: công cụ AI pháp lý "hallucinate between 17% and 33% of the time".
   - ⇒ **Khớp nguyên văn bằng máy là cổng bắt buộc**; mô hình thứ hai chỉ là lớp nghĩa.
2. **Soi lỗi thời đại mở rộng** (âm thanh, chữ).
   - TAB-VLM (ACL Findings 2026): mô hình tốt nhất (GPT-5.2) chỉ "58.7% overall accuracy" khi phát hiện lỗi thời đại trên ảnh. ⇒ Lưới lọc thứ hai, không là cổng.
   - Chữ: soi chính tả theo thời kỳ (ví dụ ſ, "shew") trên mọi chữ lên hình bằng danh sách cho từng mốc.
   - Âm thanh: §4.
3. **Đo bình luận chê AI.** YouTube Data API `commentThreads.list` "has a quota cost of 1 unit", tối đa 100 bình luận/lượt, quota mặc định 10 000/ngày ⇒ mẫu 100 bình luận/tập tốn 1–2 đơn vị. Phân loại "chê AI / chê giọng / khác" bằng mô hình rẻ + P đọc 20 % mẫu. Ngưỡng ≤ 2 % theo §10.1/§11.3.
4. **C2PA / SynthID.** `c2patool file.jpg` (thêm `-d` để xem chi tiết) kiểm được tệp của mình trước khi đăng. SynthID: chỉ kiểm được trong ứng dụng Gemini (blog Google); cổng detector mở thì chưa có trang chính thức.

---

## §7. AI-B — Thử thời kỳ xa (bắt buộc)

### 7.1 (a) Gibraltar tháng 9/1782 — `reports/nc-ai/aib/`
**Nguồn** (tải lại 18/10; SHA-256 khớp `claims-vay-ham.json/nguon_da_tai`; ranh trang dò bằng mắt vì OCR làm hỏng số trang: "3S3", "*54", "25«", Spilsbury "78" cho 73):

| nguon_id | Tệp | SHA-256 | Trang |
|---|---|---|---|
| drinkwater1786 | IA `historyoflatesie00driniala_djvu.txt` (Dublin 1786) | `7576bb8f…65212` | 351–353 |
| spilsbury1908 | IA `ajournalsiegegi00spilgoog_djvu.txt` (lần tải đầu HTTP 500, lần hai 200) | `f6c2f3a9…dc1f` | 73–75 (gồm bảng "DETAILS OF THE GUARDS, GIBRALTAR, 7TH SEPTEMBER, 1782") |
| ancell1784 | IA `acircumstantial00ancegoog_djvu.txt` | `67d61d0a…488b526` | 253–255 |

**Quy trình:**
1. Lượt 1: `gpt-6.1-sol`, Responses API, JSON schema chặt, stream (lệnh không stream bị 502 ở ~30 s như PT §15.2).
2. Kiểm máy câu trích (`aib_kiem_trich.py`).
3. Lượt 2: Claude Sonnet. Bước A đọc độc lập trước khi mở lượt 1; bước B chấm từng mục.
4. P phân xử 6 mục.
5. Gộp kết quả (`aib_gop.py`).

| Đo | Kết quả |
|---|---|
| Mục lượt 1 | 82 (crowd_density 44, activity 27, object 11, **clothing 0**); Spilsbury 62, Ancell 13, Drinkwater 7 |
| Câu trích khớp nguyên khối trong trang ghi (máy) | **80/82 = 97,6 %**; 2 gần đúng (0,94; 0,93); lượt 2 xác nhận **82/82 có trên trang** |
| Lượt 2 chấm | **correct 62 (75,6 %) · wrong_category 16 (19,5 %) · wrong_date 3 (3,7 %) · overreach 1 (1,2 %) · fabricated 0 · not_garrison 0** |
| P phân xử (6 mục: 9, 17, 18, 19, 25, 62) | 6/6 đồng ý lượt 2. Ví dụ: mục 17–19 (kỹ sư, than cho lò nung đạn) thuộc đoạn sau "the night of the 31st", trước "on the 2d" → không phải ngày 1/9; mục 62 đọc "4 privates" từ dòng bảng OCR nát |
| Lượt 2 bước A (độc lập) | 15 mục, 0 mục mới ngoài lượt 1 ⇒ lượt 1 bao trùm, nhưng chi tiết hơn tới mức thừa (≈ 20 dòng bảng gác bị chấm "doubtful") |
| Dùng được (correct hoặc chỉ sai loại) | **78/82**; mục có tên nơi cần neo bản đồ (bậc 1): 36 |
| Chi phí / thời gian | $0,0915, 132 s (lượt 1) + lượt 2 Claude ≈ 82 nghìn token, 119 s |

- Danh sách đầy đủ (mỗi mục: trích nguyên văn, nguồn, trang, SHA, ngày, kết quả kiểm máy, lượt 2, bậc): `aib/danh-sach-9-1782.json`, bảng đọc nhanh `aib/DANH-SACH-9-1782.md`.
- **Mật độ người trên phố:** bảng gác 7/9/1782 (Spilsbury tr. 74–75) cho số người theo từng điểm gác (Landport, Waterport, Ragged Staff, Europa, New Mole…). Đây là căn cứ bậc 2 cho mật độ lính ở khung neo. OCR bảng nát → **phải đọc ảnh trang** trước khi dùng số (mục 62).
- **Hoạt động có căn cứ (ví dụ):**
  - "All the inhabitants are seeking places of safety" (Spilsbury);
  - "the inhabitants … were wonderfully active in securing themselves and their property" (Drinkwater tr. 351);
  - "coals were distributed to the grates and furnaces for heating shot" (Drinkwater tr. 352; ngày ≈ 31/8–2/9, không ghi);
  - "Every one that is able to fire a musquet, or carry a shot, must take post upon any alarm" (Ancell tr. 254).

### 7.2 (b) London 1666 — danh sách mẫu ≤ 20 mục (`aib/london-*.json`)
**Nguồn** (PD tại Mỹ, Gutenberg; tải 18/10):

| Nguồn | URL | SHA-256 | Mục ngày |
|---|---|---|---|
| Pepys (Wheatley) | `gutenberg.org/cache/epub/4167/pg4167.txt` | `8a7ec38e…3f918` | 2–4/9/1666 |
| Evelyn vol. 2 (Bray) | `…/42081/pg42081.txt` | `912a1791…d51cb` | 2–7/9/1666 |

Không có số trang in → vị trí = mục ngày + dòng (`bang-trang-london.json`). Nguồn còn lại đã có URL tải được, chưa chạy: Vincent 1667 và Rege Sincera (EEBO-TCP, CC0), London Gazette số 85 (OGL v3.0).

| Đo | Kết quả |
|---|---|
| Mục | 20 (object 7, activity 7, crowd_density 3, clothing 3), $0,0448, 49 s |
| Khớp nguyên khối (máy) | **20/20** |
| Lượt 2 (P, Opus — khác mô hình lượt 1) | correct 17 · wrong_category 2 (mục 0 là sự kiện lan cháy; mục 4 "without a rag" không phải trang phục) · **correct_rui_ro_dung 1** (mục 16 "night-gowne": áo choàng mặc nhà thế kỷ 17) · bịa 0 |
| Ngày | mô hình để `null` cả 20 → điền từ mục ngày |
| Số cần nguồn thứ hai | "200,000 people … dispersed" (Evelyn 7/9) là ước lượng của một người → chưa lên hình |

### 7.3 (c) Xếp bậc AI-A
| Bậc | Gibraltar 9/1782 | London 9/1666 |
|---|---|---|
| 1 Bản đồ đo đạc | Drinkwater 1786 Plan of the Batteries (đã nắn ở SH, RMS 21,2 / LOO 33,3 m) → vị trí khối phố, điểm gác | Hollar 1666 (vùng cháy; Commons PDM nhưng chỉ 2369×1879 px); Ogilby & Morgan 1676 (BHO "Public Domain", sau cháy). Leake 1667 trên BHO "All rights reserved" → loại. Lớp MoEML/Agas CC BY-SA → loại. Faithorne & Newcourt 1658: chưa kiểm |
| 2 Văn bản | 82 mục (Drinkwater, Spilsbury, Ancell) + 123 claim TIEN-KY | 20 mục (Pepys, Evelyn) + Vincent, Rege Sincera, Gazette 85 |
| 3 Hiện vật / công trình mở dữ liệu | Thiếu cho trang phục 1782 trong tệp đã có → cần bản vẽ quân phục (Anne S.K. Brown, Rijks CC0) | Yếu: London Museum hạn chế; Met CC0 có ít trang phục Anh đúng 1666 (5 mục gần nhất, doublet ≈ 1645 có rủi ro sai niên đại) |
| 4 Tranh / bản khắc thời đó | Sharp theo Copley (LoC), Drinkwater views, Rijks "Destruction of the Floating Batteries" | Hollar "Prospects of London Before and After the Great Fire" (Met 360649, CC0); Rijks RP-P-OB-76.977, 82.020, 82.017, 82.342 ("Public domain") |
| 5 Tương đồng ("illustrative") | Đồ phố/vật nền (PT4: chưa có nguồn → không thêm) | Đồ nhà mang đi (virginals có nguồn bậc 2 — Pepys; các đồ khác bậc 5) |

**Mọi mục chữ của AI-B là bậc 2.** Không mục nào tự cho vị trí; 36/82 mục Gibraltar nêu tên nơi → vị trí lấy bậc 1. Trang phục: **0** mục bậc 2 ở Gibraltar; London có 2 mục bậc 2 nhưng chỉ mô tả cá nhân (khăn quàng cổ của Lord Mayor, áo choàng mặc nhà của Pepys). Vì vậy trang phục đám đông của cả hai mốc phải từ bậc 3–4.

### 7.4 (d) Trọng số "mức tư liệu" cho thước chấm đề tài /25
Thước NC-LS hiện có 5 trục × 5 điểm: cầu · khoảng trống · dữ liệu timelapse · bản đồ/tranh có quyền · hero.

**Đề xuất thay trục "dữ liệu timelapse" bằng "mức tư liệu"** cho đề tài trước khoảng 1850, giữ thang /25:

| Thành phần | Điểm |
|---|---|
| Bậc 1: bản đồ đo đạc thời đó nắn được RMS ≤ 50 m ở lõi phố (≤ 120 m nếu chỉ dùng tầm vùng) | 2 |
| Bậc 2: ≥ 2 văn bản sơ cấp độc lập đã số hoá, tải được, có SHA; lượt AI-B đạt khớp nguyên văn ≥ 95 % và bịa 0 | 1 |
| Bậc 3: hiện vật/công trình/bản vẽ mở dữ liệu (CC0/PD) cho trang phục + vật liệu của ≥ 2 nhóm người chính | 1 |
| Bậc 4: ≥ 2 tranh/bản khắc thời đó, đối chiếu chéo được | 1 |

- **Cổng (CHẶN):** thiếu bất kỳ bậc 1, 2 hay 3 → **không vào hàng đợi**, dù /25 ≥ 20. Bậc 5 không cộng điểm.
- **Chấm thử:** Gibraltar 1782 = 2 + 1 + 0,5 (trang phục chưa tải bản vẽ) + 1 = **4,5/5**. London 1666 = 1 (Hollar 1666 độ phân giải thấp; Ogilby 1676 sau cháy) + 1 + 0,5 + 1 = **3,5/5**.
- **Cổng bậc 3 của London đang "yếu"** → tiền kỳ T4 phải chốt nguồn trang phục 1660s (Met CC0, Rijks) trước G0.

---

## §8. Chi phí thật

| Mục | Số đo |
|---|---|
| OpenAI (`aib/cost.jsonl`) | Lượt 1 Gibraltar $0,09152 (6 136 vào / 7 925 ra) · London $0,04484 · chép trang Ancell $0,02440 · 1 lệnh không stream 502 ở ≈ 30 s ($0, không kết quả) ⇒ **$0,1608** (đơn giá `gpt-6.1-sol` $2/$10 mỗi MTok, developers.openai.com/api/docs/models, đọc 18/10) |
| Claude — subagent (token đo từ thông báo hoàn tất) | R1 126 014 · R2 144 376 · R3 96 298 · R4 121 517 (bốn gói tra cứu, mô hình phiên) · lượt 2 AI-B 82 430 (Sonnet) ⇒ **570 635 token** |
| Claude — phiên chính | Không có đồng hồ $ trong phiên (không có `CONSOLE_API_KEY`, không gọi `claude -p`). Theo token: **vượt mốc theo dõi $3 (ước)**, dưới chặn an toàn $15 (ước) |
| Dòng lợi ích (mốc $3) | Bốn gói tra cứu đọc ≈ 230 URL giấy phép/giá hiện hành, thay cho trí nhớ. Đó là căn cứ để loại 15+ công cụ NC/SA trước khi phiên xưởng nào dùng chúng |
| YouTube / ElevenLabs | 0 / 0 |
| Giờ máy | ≈ 0,3 h tính toán (SAM 20 s, Swin2SR + DA2 ≈ 1 phút, pose ≈ 1 phút + tải video 120 MB, cài torch); phiên ≈ 1,5 h đồng hồ |
| Dung lượng thêm vào repo | ≈ 1,1 MB (`reports/nc-ai/`), không tệp nào > 1 MB, không LFS |

**Đơn giá đo lại cho ước chi phí/tập (theo đơn giá đo được, ước):**

| Việc | Đơn giá |
|---|---|
| Đọc nguồn AI-B | ≈ $0,010/trang (lượt 1 GPT) + lượt 2 Claude |
| Chép trang bằng mô hình nhìn | ≈ $0,024/nửa trang |
| Ảnh AI (PT) | ≈ $0,065/tấm |
| Chấm mù | ≈ $0,06/phiếu |

Một tập lịch sử với 60 trang nguồn, 40 trang chép, 6 tấm C và 24 phiếu ≈ **$0,6 + $1,0 + $0,4 + $1,4 ≈ $3,4/tập** (ước), chưa tính lượt 2 Claude.

---

## §9. Đề xuất nguyên văn đổi Kinh thánh §11 (chờ duyệt)

**Thêm §11.7 "Tái dựng có căn cứ — 5 bậc (AI-A)":**
> - Mọi phần tử nhìn thấy trong cảnh dựng (công trình, phố, vật, người, trang phục, động tác, mật độ người) mang một **bậc căn cứ** trong bảng shot: (1) bản đồ/sơ đồ đo đạc thời đó → bố cục, vị trí; (2) văn bản thời đó (nhật ký, sổ quân, điều lệnh) → hoạt động, mật độ người, động tác; (3) công trình/hiện vật còn lại, bảo tàng mở dữ liệu (CC0/PD) → hình khối, vật liệu, trang phục; (4) tranh/bản khắc thời đó → không khí, màu, chỉ sau đối chiếu chéo ≥ 2 tác phẩm vì có thể lý tưởng hoá; (5) tương đồng cùng vùng + thời kỳ → chỉ vật nền phụ, nhãn "illustrative". Không có căn cứ → không dựng, kể bằng bản đồ/tài liệu/lời.
> - Vị trí chỉ lấy từ bậc 1; văn bản (bậc 2) không tự cho vị trí. Trang phục đám đông lấy từ bậc 3–4.
> - AI được TÌM, ĐỌC, ĐỐI CHIẾU, PHỤC CHẾ, LÀM SỐNG cái đã có nguồn; không sinh dữ kiện (vị trí, công trình, cờ, quân phục, ngày, số). Phép thử: bỏ AI ra mà dữ kiện trên hình đổi → không được dùng.
> - AI đọc nguồn: mọi mục AI trích phải khớp **nguyên văn** trong tệp có SHA-256 (kiểm bằng máy), kèm trang hoặc mục ngày; lượt đọc thứ hai bằng mô hình khác; mục lệch ngày, lệch loại hoặc "hiểu quá" không lên hình khi người chưa duyệt. Chép trang bằng mô hình nhìn chỉ là tệp làm việc; câu lên hình đối chiếu ảnh trang.
> - Số hoá bản đồ: AI vẽ đường bao khi người chỉ định khối (bán tự động); không nhận khối do máy tự phát hiện. Lô khối nhận khi IoU với mẫu dò tay ≥ 0,7 trên ô kiểm.
> - Thước đề tài: đề tài trước ~1850 dùng trục "mức tư liệu" (/5) thay "dữ liệu timelapse"; thiếu bậc 1, 2 hoặc 3 → không vào hàng đợi.

**Sửa §11.3, dòng "KHÔNG":** giữ "ước độ sâu bằng AI". Thêm:
> phóng to/làm nét bằng AI trên bản khắc và tranh (thêm nét giả — NC-AI §3.2); tô màu không có nguồn màu; lấy chuyển động từ footage khi chưa gắn năm cho đoạn đó.

**Sửa §11.5, dòng "phục chế ảnh lưu trữ":**
> phục chế (khử nhiễu, làm nét ≤ ×2) chỉ cho ảnh chụp; kiểm có đáp án (thu nhỏ → phục chế → so gốc) trước khi dùng một công cụ mới; công cụ phải có giấy phép trọng số cho phép thương mại (loại CodeFormer, SUPIR, GFPGAN, Depth Pro, DA2 Base/Large).

**2,5D lưu trữ:** **không đề xuất nới** (§3.3). Nếu chủ dự án muốn thử thì mở phiên riêng với các rào ở §3.3.

---

## §10. Gắn việc vào phiên
| Phiên | Việc từ NC-AI |
|---|---|
| **Tiền kỳ T4 London 1666** | Chạy AI-B (`tools/aib_doc.py london1666` + `aib_kiem_trich.py` + lượt 2) trên toàn bộ 2–7/9 của Pepys, Evelyn, Vincent, Rege Sincera, Gazette 85. Chấm "mức tư liệu" (§7.4) trước G0; chốt bậc 3 trang phục 1660s. Ghost: Hollar 1666 + Ogilby & Morgan 1676 bằng SAM 1 click/khối (kiểm IoU trên ô mẫu dò tay). Đọc lại điều khoản gốc Mixamo/Smithsonian/RCT/Europeana (bị chặn trong phiên) |
| **V7 (máy dựng)** | Thêm cột `bac` + `nguon` cho mỗi phần tử vào bảng shot; người nền dùng mocap CMU/100STYLE/Quaternius (đi, đứng, khiêng) qua bộ nạp MPFB; động tác súng theo *Manual Exercise* 1764 / *Ordenanzas* 1762 |
| **G1b T3** | Mật độ lính khung neo 1782 theo bảng gác 7/9/1782 (đọc ảnh trang Spilsbury tr. 74–75, không đọc OCR); hoạt động phố theo `aib/danh-sach-9-1782.json` (mục `correct`); chấm mù tai SFX AI vs CC0 (5 cặp) |
| **Phiên K** | Nếu chủ dự án duyệt §9: luật kiểm cột `bac` (phần tử bậc 5 phải có nhãn "illustrative"; không phần tử nào thiếu bậc) |

## §11. Thước đo chân thực đề xuất (mỗi tập)
| Chỉ số | Ngưỡng | Đo bằng |
|---|---|---|
| Lỗi dữ kiện / khung (khung có AI) | 0 lỗi chắc (PT2/PT4 đạt 0 sau quy trình) | Rà 200–400 % + đối chiếu nguồn từng khung |
| Claim có ≥ 2 nguồn | 100 % claim số trên hình; claim chỉ 1 nguồn → nói "according to …" | `claims.json` |
| Câu trích AI khớp nguyên văn | 100 % (máy) | `aib_kiem_trich.py` |
| Phần tử dựng có bậc 1–4 | ≥ 90 % diện tích phần tử trong khung; bậc 5 có nhãn | cột `bac` |
| Chấm mù "đúng thời kỳ" | ≥ 7/10 (PT C đạt 7,44 nhưng có lỗi cờ người chấm không bắt được → không thay kiểm) | chấm mù |
| Chấm mù "trông AI" | ≤ 3/10 (A/B 2,56; C 3,89; LAI PT4 4,72) | chấm mù |
| Bình luận chê AI | ≤ 2 % (mẫu 100) | `commentThreads.list` |
| Thời lượng AI | ≤ 20 % | sổ AI |

## §12. Chỉ số trong ±5 % quanh ngưỡng
- Lượt 1 Gibraltar khớp nguyên khối **97,6 %** so ngưỡng đề xuất 95 % (+2,7 %) — **trong ±5 %**.
- SAM, ngưỡng 0,7 (`ai1/sam-1click.json`): **K1782-08 0,690 · K1782-19 0,694 · K1782-09 0,715 · K1782-16 0,725** nằm trong ±5 %. Vì vậy số "16/22 ≥ 0,7" có thể đổi trong khoảng 14–18 nếu ngưỡng lệch nhẹ. Ở ngưỡng 0,85, có 7 khối nằm trong ±5 % (0,823–0,881). Ở ngưỡng 0,5, không có khối nào.
- Gần đúng câu trích: 0,93 và 0,94 so ngưỡng 0,90 (+3–4 %) — trong ±5 %.
- Rung tư thế, PSNR: không có ngưỡng đã duyệt.

## §13. Sự cố cần chủ dự án biết
- Một subagent tra cứu (gói R4, London 1666) **đã lỡ đặt email chủ dự án vào header User-Agent** khi gọi API Wikimedia Commons. Các yêu cầu đó đều bị trả 429 và không được lặp lại. Email **không** có trong repo; mọi tệp nguồn đưa vào repo đã được lọc email (2 email công khai của bên thứ ba trong R2 cũng đã che).
- Proxy chặn: GitHub API/releases (403), si.edu, rct.uk, Europeana, Mixamo FAQ, Adobe helpx (403), Freesound (403). Trang JS (Kling, Stability pricing) trả về rỗng. Dữ kiện từ các nguồn này ghi "[thứ cấp]" hoặc "chưa đọc".

## §14. Tệp
| Đường dẫn | Nội dung |
|---|---|
| `reports/NC-AI-BAO-CAO.md` | báo cáo này |
| `reports/nc-ai/nguon/R1…R4-*.md` | 4 gói tra cứu: URL, ngày đọc, giấy phép nguyên văn |
| `reports/nc-ai/tools/` | `tach_trang.py`, `aib_doc.py`, `aib_kiem_trich.py`, `aib_gop.py`, `ai1_vector.py`, `ai1_sam.py`, `ai1_ocr_vlm.py`, `ai1_wer.py`, `ai2_pose.py`, `ai3_phuc_che.py` |
| `reports/nc-ai/aib/` | bảng trang + SHA, lượt 1, kiểm máy, lượt 2 A/B, danh sách cuối Gibraltar + London, `cost.jsonl` |
| `reports/nc-ai/ai1/` | kết quả vector hoá (JSON + ảnh so sánh), SAM 1 click, `ocr/` (đáp án, 3 bản chép, WER) |
| `reports/nc-ai/ai2/`, `ai3/` | kết quả pose, phục chế, độ sâu |

Tệp thô (sách djvu.txt, bản đồ, ảnh trang, video) để ngoài git (scratchpad); mọi SHA đã ghi ở trên.

## §15. Việc chờ chủ dự án
1. **Duyệt bảng quyết định §0.** Đề xuất: DÙNG mục 1–4 · THỬ CÓ ĐIỀU KIỆN mục 5 · DÙNG dữ liệu mở mục 6 · mục 7 chỉ cho ảnh chụp · GIỮ CẤM mục 8 · CHƯA DÙNG mục 9.
2. **Duyệt văn bản đổi Kinh thánh §9:** thêm §11.7 (5 bậc), sửa dòng "KHÔNG" của §11.3, sửa §11.5. Ghi vào AUTHORSHIP.
3. **Duyệt trục "mức tư liệu" /5 và cổng bậc 1–3** cho thước đề tài (§7.4). Lưu ý London 1666 chấm 3,5/5 và **cổng bậc 3 đang yếu**.
4. **Quyết định 2,5D lưu trữ:** giữ cấm (đề xuất) hay mở một phiên thử riêng có rào §3.3.
5. **Quyết định nhà cung cấp video AI:** chưa dùng (đề xuất); nếu muốn thử, chọn nhà cung cấp và cấp khoá vào môi trường.
6. **RIGHTS:**
   - Nếu dùng CATMuS (CC-BY-4.0), 100STYLE (CC BY 4.0), CMU mocap thì cần dòng ghi công.
   - Chủ dự án hoặc phiên tiền kỳ mở tay và lưu điều khoản gốc của Mixamo, Smithsonian, RCT, Europeana, Freesound API (bị chặn trong phiên).
   - Duyệt có hỏi OpenMMLab về giấy phép trọng số RTMPose hay không.
7. **Ghi nhận sự cố email ở User-Agent** (§13).
8. **Gắn việc §10** vào lệnh tiền kỳ T4, V7, G1b T3.
