**Nhánh thật: `ccr-3194130e-kijmlg`** (harness buộc tên này; lệnh đặt `checks-1-16`). Nhánh đặt lại về `origin/main` @ `8cedb8af` trước khi sửa. Đã đẩy, **không merge**.

# Phiên K-1.16 — bộ kiểm cho luật mới (§12.1 sửa, §13 hiểu hai đường, §13.6 timelapse), khiếu nại V6/G1b, golden V6, sổ còn treo — BÁO CÁO

> Phiên K, 19/10/2026. **Mọi luật mới CHỈ BÁO trong `k2check` (mặc định); `--cap` áp mức đề xuất. Chỉ áp cho tập kênh 2 từ T3; tập cũ giữ đúng hành vi 1.15. Không merge. DỪNG chờ chủ dự án.**
> Mọi số là số đo thật trong phiên; lệnh ghi ở từng mục. Email chủ dự án không có trong tệp, commit, header, URL hay payload nào.

## 0. Khối điều lệ (lệnh + thực tế)
| Trường | Lệnh | Thực tế |
|---|---|---|
| Loại phiên | K (kiểm định) | đúng |
| Nhánh | `checks-1-16` từ `origin/main` (8cedb8af) | **`ccr-3194130e-kijmlg`** (harness), gốc `8cedb8af`; không merge |
| LOCK gốc | 1.15.0 | **KHỚP** `f4fa0349ca53b05d64e4303554ec168e6445c82d97e662672f70ccf42df80d40` (`python3 -I checks/lock.py --verify`, đầu phiên) |
| Vùng sửa | `checks/**`, `reports/k116/**`, `AUTHORSHIP.md`, `COST-LEDGER.csv` | đúng (§11). Không sửa `docs/`, `design/`, `scripts/`, `channel-*/`, nhánh khác. Chỉ ĐỌC: `scripts/common/golden.py`, `scripts/k2/lib/k2.js` (tên vai chữ), nhánh `k2c-t3-kl42` (sổ) |
| Chi phí | Claude/OpenAI/ElevenLabs/YouTube 0 trừ trình dựng golden; giờ máy mốc 4 h | **$0 / $0 / 0 ký tự / 0 đơn vị**; giờ máy **≈ 0,8 h** thời gian thực (§10) |
| `lock.py` (không cờ) | một lần ở cuối, sau khi selftest đạt | **đúng một lần**, 10:33 UTC → 1.16.0 `dbbb6cd0…a439`; mọi lần khác chỉ `--verify` |
| Preflight | bắt buộc; che email | hook pre-commit + pre-push cài đầu phiên; mọi commit **PREFLIGHT ĐẠT** (§12) |
| Việc dở | đẩy ≤ 30 phút + `reports/k116/CHECKPOINT.md` | 3 checkpoint đẩy lúc 09:58, 10:18, 10:31 (bản vá việc dở trong `reports/k116/wip/`, đã gỡ khi commit mã) |
| Dừng | không dừng hỏi giữa chừng | đúng |

## 1. Tóm tắt (đọc 1 phút)
1. **Khiếu nại: 10 mục** (2 của V6 + 7 của G1b + câu hỏi tên trường ML1/FT1). **Chấp nhận 6, chấp nhận một phần 2, trả lời không đổi luật 1** (tên trường); 0 bác toàn bộ. Phần bác: thay K-LAI-3…6 bằng "kiểm sổ nguồn" chung (trái §11.3), và "A* KHÔNG ÁP toàn bộ" khi không lời (phần đo trên master vẫn áp, vì bản không lời §11.2 vẫn là bản phát hành). §2.
2. **Luật mới (9 hàng)**: SACH-1 (§12.1 + TL-4), CHUONG-1 (§13.3), PP-1 (D6), TL-1/TL-2/TL-3 (§13.6, đọc log shot + **thước video**), NHIP-NGHIA (§13.2), XEM-CAM (§13.4), PC-1 (thước phục chế §12.3). Ngưỡng TL ghi rõ **"hiệu chỉnh sau V7-PILOT"**. §3.
3. **Selftest**: mới **k116 129/129**; cũ đều giữ đúng kỳ vọng trên cây đã khoá: k115 105/105 · k114 126/126 · k113 64/64 · k1122 37/37 · k1121 48/48 · k112 75/75 · k2 129/129 · ll 317/317. `k2check` trên tập cũ: **T1 30/30 và T2 L5 + gib20 48/48 hàng giống hệt 1.15** (kể cả hàng LOCK). §4.
4. **T3 animatic thật (G1b) chạy 1.16**: Q26b **TRƯỢT → ĐẠT** (theo vùng: lớn nhất eo-dat 22,4 %); ML1 **0/84 → 76/84 shot gắn** khi đọc lời khoá, lộ 7 lỗi khai thật (§3.5); SACH-1 TRƯỢT (40 số/câu trích + 15 tư liệu đứng riêng — G1b dựng trước khi §12.1 sửa 19/10); PP-1 TRƯỢT (1 thẻ 5 s, 13,8 từ/s); TL-1 video **9,24 cắt/phút > 5**; XEM-CAM, NHIP-NGHIA THIẾU (chưa có tệp). §3.5.
5. **Golden**: tham chiếu mới dựng bằng trình dựng V6, khoá SHA trong LOCK. Trước: SSIM **0,9449 / 0,9307 / 0,9082** (t1 lệch cục bộ 22/144). Sau (lượt dựng độc lập thứ hai so tham chiếu mới): **1,0 / 1,0 / 1,0**, MAD 0, 0/144 ô. §5.
6. **LOCK 1.15.0 `f4fa0349…df80d40` → 1.16.0 `dbbb6cd0606cf37363738711fa8da1b24de29ada4edd1875c1e0adb25d31a439`**, `--verify` KHỚP. §6.
7. **Sổ**: AUTHORSHIP +3 (GC-C′ isthmus, giãn shot B 745,0 s, D11 = A ≈ 13:20); COST-LEDGER +3 (CASTING-GIONG, KL42, K-1.16), **61 dòng, mọi dòng 20 cột**. §7.

## 2. Khiếu nại
Căn cứ: Kinh thánh hiện hành `docs/BIBLE-KENH2.md` (§12.1 sửa 19/10 thắng câu cũ khi trái). "1.16" = chỉ tập từ T3 (`khung_sach: true` hoặc `kenh2_tu_t3: true`); tập cũ không đổi.

| Mã | Nội dung | Quyết | Lý do (Kinh thánh) | Thay đổi trong 1.16 |
|---|---|---|---|---|
| **A-V6-1** | K-LAI-3…6 áp cho vân AI HC7 (`ai_texture`) như tấm C | **Chấp nhận một phần** | §11.3 phân biệt (a) tấm C "MỘT tấm ban ngày mỗi khung neo × mốc, sửa có mặt nạ" và (b) vân "một bộ vân/toà × mốc". Các phép so khung A/tấm dùng/đêm chỉ có nghĩa với tấm C → **chấp nhận** tách nhánh. **Bác** phần "thay K-LAI-3…6 bằng kiểm sổ nguồn": §11.3 vẫn bắt "kiểm dữ kiện từng tấm/**vân** … 0 lỗi chắc mới dùng, ngoại lệ phải chủ dự án duyệt; sổ AI ghi mọi lệnh gọi (model, prompt, % mặt nạ, chi phí, C2PA)" | Chỉ vân → K-LAI-4/5/B **KHÔNG ÁP**. K-LAI-3 đọc sổ vân dạng PT3 (`tep`): có tệp dùng, có trong goi-api, 0 lỗi chắc, "dùng nếu …" phải ghi `dieu_kien_dat: true`, không chấm mù. K-LAI-6 nhận `input.mask_frac`. Hàng mới **K-LAI-3V** (Cảnh báo): tệp vân dùng còn ghi nghi vấn. **V6 thật**: K-LAI-6 ĐẠT (133 lệnh), K-LAI-4/5/B KHÔNG ÁP; **K-LAI-3 THIẾU**: 55/69 tệp "dùng nếu đạt kiểm trôi" chưa ghi kết quả; K-LAI-3V: 65 tệp còn nghi vấn |
| **A-V6-2** | A4 TRƯỢT khi đoạn không có lời | **Chấp nhận** | SMR = lời trên nhạc; không lời thì không có đại lượng để đo | Không lời → A4, A8, A9, A10, A13 KHÔNG ÁP |
| **A-G1B-1** | K-LAI-2 đòi nhãn AI suốt shot — trái §12.1 | **Chấp nhận** (chỉnh: thẻ phương pháp theo D6, không theo "4–5 s") | §12.1: "KHÔNG hiện trên hình: … nhãn Surface detail AI-assisted"; công bố chuyển sang mô tả + bình luận ghim + thẻ phương pháp; "dữ liệu … ai_image/ai_texture vẫn ghi đầy đủ trong log" | K-LAI-2 mới: (a) cờ ai_* ở mọi khung log; (b) đoạn có khung AI phải khai AI (đặc tả/log shot); (c) thẻ phương pháp nói AI; (d) mô tả có "AI use = Yes"; (e) nhãn AI **hiện trên hình là lỗi** |
| **A-G1B-2** | NC-H5 (b) nhãn nguồn ghost ≥ 38 px | **Chấp nhận** | §12.1 bỏ "dòng nguồn cho mọi cảnh 3D/bản đồ"; §10.4 dòng ghost đã ghi "(chữ trên hình: theo §12.1)" | (b) mới: ghost có nguồn (log shot `nguon` / khối `ghost`) và nguồn có trong mô tả. **Sửa luôn lỗi nhận diện** G1b nêu: bộ đếm của cảnh `tl/*` giờ được nhận ⇒ NC-H5 bật cho T3, (a) đọc `nam_khung` (chưa có → THIẾU) |
| **A-G1B-3** | BD-3 nhãn "approx. borders" + "Map: Natural Earth" | **Chấp nhận** | §11.1 ranh lịch sử + inset đều ghi "(chữ trên hình: theo §12.1)"; §12.1 liệt kê "approx. borders" vào danh sách không hiện | BD-3 mới: (a) manifest lớp có `nam` + `nguon`; (b) nguồn ranh có trong mô tả; (c) nhãn "approx. borders" **hiện trên hình là lỗi**. Không đòi nhãn trong log |
| **A-G1B-4** | Q26b đếm `tl/t3s` thành một bối cảnh | **Chấp nhận** | Q26b đo đa dạng **bối cảnh** (nơi). `tl/t3s` là một mô-đun dựng 37 vùng; Q26b-K2 (đã duyệt) đo theo `vung` | Cảnh `tl/*` có `vung` → bối cảnh = "tl/<mô-đun> · <vung>". **T3 thật: TRƯỢT → ĐẠT** (23 bối cảnh, lớn nhất eo-dat 22,4 %, liên tục dài nhất 63,5 s). Cùng một vùng suốt tập vẫn TRƯỢT (selftest) |
| **A-G1B-5** | Q37 "dài nhất ≤ 6 s" với khung neo / tấm im lặng | **Chấp nhận** (có giới hạn) | §11.2: "chỉ khung neo giữ 6–10 s"; "1–2 tấm im lặng 8–10 s" | Khoảng nằm trọn trong shot `khung_neo`/`neo`/`im_lang` ≤ 10 s được miễn ở (c); shot miễn > 10 s hoặc > 2 tấm im lặng → (c). TB (b), khung tĩnh (d) giữ nguyên. **T3 thật vẫn TRƯỢT (c) 10,0 s**: G1b chỉ khai `khung_neo` ở KA1782, KB1943; KC1910, KB2026, KC2026, KA2026 chưa khai |
| **A-G1B-6** | Thước phục chế "cạnh mới > 5 %" | **Chấp nhận** | §12.3 đòi "kiểm có đáp án"; số đo G1b cho thấy bicubic đã 3,95–6,40 % (nền nhiễu hạt phim) | K không khoá ngưỡng tuyệt đối. **PC-1**: Δ cạnh mới = công cụ − **bicubic cùng ô** ≤ 1,0 điểm % và PSNR ≥ bicubic, mức Cảnh báo tới khi hiệu chuẩn trên ≥ 10 ảnh. Trên 3 ảnh NARA thật: chỉ 000757·Swin2SR đạt (Δ −0,23), trùng kết luận của G1b |
| **A-G1B-7** (+ A-V6-2) | A1–A13 khi tập chưa có lời | **Chấp nhận một phần** | Animatic dùng nhạc tạm → chưa phải bản phát hành. Nhưng **bản không lời** (§11.2) là bản phát hành: loudness, đỉnh thật, lặng, chạm trần vẫn phải đo | `animatic: true` → mọi mục CHỈ BÁO. Không lời → chỉ mục phụ thuộc lời KHÔNG ÁP; A1–A3, A5–A7, A11, A12 vẫn áp. **Bác** "A* KHÔNG ÁP toàn bộ" |
| **ML1/FT1** | "Cần K chỉ tên trường" | **Trả lời; luật không đổi** + thêm nguồn câu cho animatic | — | **ML1** đọc `cau` = **≥ 12 ký tự đầu câu, nguyên văn**, khớp đúng một câu của lời, hoặc `claim: <id>` có trong `claims.md` **cạnh đặc tả**; đặt ở shot hoặc `p`. G1b ra 0/84 vì animatic **không có căn chữ lời** (ElevenLabs 0) và claims nằm ở `claims-vay-ham.md` một thư mục trên. 1.16 thêm `loi_khoa:` và `claims_md:`. **FT1** đọc **`ly_do_hinh`** ∈ bang_chung · con_nguoi · quy_mo · khoanh_khac — G1b khai `ly_do` nên 0/15 |

## 3. Luật mới (tập từ T3)
Mã `checks/ll/q_k116.py`; định nghĩa đầy đủ và tên trường cho phiên xưởng: `checks/ll/RULES-LL.md` mục "1.16". Hằng số ngưỡng có tên trong mã.

| Mã | Nguồn | Trường đọc | Ngưỡng | Mức đề xuất |
|---|---|---|---|---|
| **SACH-1** | §12.1 (sửa 19/10) + §13.6 TL-4 | đặc tả: `p.so`, `p.card`, `type` photo/document/record/footage, `p.phu_dia_hinh`, `p.sach`; log chữ k2.js (`--logs`) hoặc `log_chu`: `role`, `s`, `alpha` | (a) 0 tấm số/câu trích; (b) 0 tư liệu đứng riêng, phủ địa hình ≤ **3 s**; (c) 0 vai/chữ cấm hiện; (d) chip nơi ≤ **3 s**/lần; (f) mọi shot `p.sach` | Chặn (a)–(d), (f) · Cảnh báo (e) chữ bản đồ khác |
| **CHUONG-1** | §13.3 | `p.the_chuong {s, at, dur}` hoặc log vai `the_chuong` | ≤ **8**/tập · "năm — ≤ **6** từ" · ≤ **3 s** · không ở chương 0 / CH0 / `moc_s` · không captur*/liberat*/conquer*/seiz* · (f) dưới trái + mờ | Chặn (a)–(e) · Cảnh báo (f) |
| **PP-1** | §12.1 (b) + D6 | đoạn `the_phuong_phap` / id PP / part END / tiêu đề "How this film was made" | **2** thẻ × **7–9 s** (K đọc "≈ 8 s" = ±1 s) · liền, ở cuối · nói nguồn/bản đồ, ước tính, AI · (e) ≤ **3 từ/s** | Chặn (a)–(d) · Cảnh báo (e) |
| **TL-1** | §13.6 TL-1 | `log_shot`: `goc`, `tl`, `diem_may`, `moc`; video (master hoặc `--tl16-video`) | góc cao + thời gian chạy ≥ **75 %** thân phim; ≤ **5** cắt/phút (đo video); góc cao trôi ≤ **2 %** khung/s; **6–8** điểm máy, mỗi điểm ≥ 2 năm | Cảnh báo — **hiệu chỉnh sau V7-PILOT** |
| **TL-2** | §13.6 TL-2 | `goc: thap`, `vai`, `noi`, `nguoi` | ≤ **10 %**; có vai; phố hoặc khoảnh khắc người | Cảnh báo — hiệu chỉnh sau V7-PILOT |
| **TL-3** | §13.6 TL-3 | `tl`, `su_kien`, `trong_pct`, `bac` | mỗi shot 3D có thời gian chạy hoặc biến cố; "trống" = `trong_pct` > **60 %** mà không có thời gian chạy; có `bac` | Cảnh báo — hiệu chỉnh sau V7-PILOT |
| **NHIP-NGHIA** | §13.2 | `nhip_vat` (đề xuất `nhip-vat.json`): `{nhip: [{id, chinh, cau, vat: [{loai, shot}]}]}` | ≥ **90 %** nhịp chính có vật hợp lệ (loại thuộc 6 loại §13.2, shot có thật, thẻ chương có thật) | Chặn |
| **XEM-CAM** | §13.4 | `xem_cam` (đề xuất `xem-cam.json`): 8 câu, người chấm {vai ai\|chu_du_an, dung, tong}, `tat_tieng`, `video_sha256`? | đủ 8 câu · ≥ 3 AI + chủ dự án · mỗi người ≥ **6/8** · không email · SHA khớp bản xem (nếu khai). **K không tự chấm** | Chặn |
| **PC-1** | §12.3 (khiếu nại A-G1B-6) | `phuc_che {kiem, dung}` (định dạng `kiem.json` của G1b) | Δ cạnh mới so bicubic ≤ **1,0** điểm %; ΔPSNR ≥ 0 | Cảnh báo (thước tạm) |

**Trường log shot đề xuất** (tên theo lệnh): `goc` ∈ cao · thap · neo · phang; `tl` (bool); `vai`. Thêm vì luật cần: `trong_pct`, `su_kien`, `diem_may`, `nguoi`. `g1b/log-shot.json` đã có `noi`, `moc`, `bac`, `nguon`, `ai_*`.

### 3.1 Cổng 1.16
- Bật khi `khung_sach: true` (đặc tả G1b T3 đã có) hoặc `kenh2_tu_t3: true`.
- Tập không khai: một hàng "1.16 KHÔNG ÁP"; Q26b/Q37/A*/K-LAI/NC-H5/BD-3/ML1 chạy đúng đường mã 1.15 (đối chiếu §4).

### 3.2 SACH-1 — điểm cần biết
- **Vai cấm** (log k2.js): src, src_ngan, ai_label, ghost_src, inset_src, index_src, method, bien_gioi, so, trich, trich_dich. Thêm bắt theo chữ: "approx. borders", "estimated infill", "Ruins: estimated", "illustrativ…", "AI-assisted", "Source:", "Map:". `alpha` = 0 (đã tắt) không tính.
- **Vai được phép**: year, clock, calendar (bộ đếm), where (chip), the_chuong, the_phuong_phap.
- **Vai còn lại** (diem, chu_giai, inset, tag, index, card): Kinh thánh chưa nói rõ. §11.1 (chú giải ≤ 3 phe, nhãn mốc thời gian, inset 1–2 nhãn) và §10.4 NC-H4 (nhãn địa danh) vẫn đòi chữ bản đồ, nhưng §12.1 nói "CHỈ có". **K để Cảnh báo (e) và đưa chủ dự án quyết** (§9 K116-D3).
- Không có log chữ → (c), (d) THIẾU (Chặn). Animatic G1b không có log trong git, nên chỉ đo được (a), (b), (f) trên đặc tả.

### 3.3 Thước video TL-1 (hiệu chuẩn trên dữ liệu thật)
- **Cắt**: khung có [chênh lệch histogram xám 32 bin ≥ 0,20 VÀ lệch điểm ảnh TB ≥ 12/255] HOẶC [lệch ≥ 20/255 VÀ ≥ 3 × trung vị ±6 khung], cực đại cục bộ, cách cắt trước > 3 khung, bỏ 0,5 s đầu.
- **Hiệu chuẩn trên animatic T3** (270p 12 khung/s, 726 s), so với 126 mốc cắt của đặc tả:
  - khớp ±0,2 s: **103/126**; 10 phát hiện ngoài đặc tả (mở đầu, chữ thẻ cuối phim);
  - **xem khung 3 mốc bị "bỏ sót"**: 2/3 là **đổi năm cùng góc máy** (25,3 s 1943→1782; 678,4 s 1704→1735). Đặc tả khai là shot mới, nhưng thị giác là thời gian chạy — đúng thứ TL-1 muốn. 1/3 là đổi góc thật (162,1 s).
  - ⇒ số shot của đặc tả chỉ là **cận trên** số cắt (b, chỉ báo); **video quyết (c)**.
- **Chuyển động máy**:
  - Tịnh tiến: tổng phase correlation (cửa sổ Hann, bước 0,25 s), vùng y 10–68 %. Phải bỏ dải chữ tĩnh: bộ đếm, chip, phụ đề nung kéo đỉnh tương quan về 0. Thử thật: shot 0a đo 0,85 → 4,57 %/s khi bỏ dải chữ.
  - Phóng: **phase correlation log-polar (Fourier–Mellin) cho kết quả sai chiều trên video tổng hợp**, nên K đo phóng bằng phép tương tự từ dòng quang học LK (RANSAC). Lệch khỏi chữ "phase correlation" của lệnh → §9 K116-D6.
  - Selftest tổng hợp: trôi 1 %/s → **1,09**; lia 6 %/s → **6,01**; đẩy máy phóng 3 %/s → **1,61 %/s** dời góc khung (lý thuyết 1,6).

### 3.4 Khiếu nại trên dữ liệu thật V6 (đoạn thử, chỉ vân HC7; `fixtures/k116/v6/` = bản sao)
| Hàng | 1.15 | 1.16 |
|---|---|---|
| K-LAI-1 | ĐẠT | ĐẠT |
| K-LAI-2 | ĐẠT (nhãn 38 px) | **TRƯỢT (e)**: nhãn AI vẫn vẽ trên hình (đoạn thử dựng trước §12.1) |
| K-LAI-3 | TRƯỢT ("0 tấm dùng") | **THIẾU**: 69 tệp vân dùng, 0 lỗi chắc, nhưng 55 tệp "dùng nếu đạt kiểm trôi" chưa ghi kết quả kiểm trôi |
| K-LAI-4 / 5 / B | THIẾU / TRƯỢT (133 lệnh > 3) / THIẾU | **KHÔNG ÁP** (không có tấm C) |
| K-LAI-6 | TRƯỢT (thiếu % mặt nạ ×133) | **ĐẠT** (`input.mask_frac`) |
| K-LAI-3V | — | Cảnh báo: 65/69 tệp dùng còn ghi nghi vấn (vd "rong chân tường ~1–1,5 m có thể quá cao") |

### 3.5 T3 animatic thật (G1b) — 1.15 → 1.16
Lệnh: `k2check.py <episode.yaml> --tl <timeline> --master reports/g1b-t3/animatic/animatic-270p-xem.mp4 --no-asr --cap`.
- Timeline sinh lại bằng `scripts/k2/prep.py` từ đặc tả G1b (mạng chặn, không gọi API): 726,17 s, trùng G1b.
- Hai lượt chạy:
  - (1) đặc tả nguyên trạng;
  - (2) bản "khai" thêm 5 khoá trỏ tới tệp đã có trong repo: `log_shot` = `g1b/log-shot.json`, `phat_hanh.mo_ta` = `phat-hanh/nguon-mo-ta.md`, `loi_khoa`, `claims_md` = `claims-vay-ham.md`, `phuc_che.kiem`.
- Bảng đầy đủ: `reports/k116/do/k2check-1.1{5,6}-t3-animatic*.md`.

| Hàng | 1.15 | 1.16 (1) | 1.16 (2) "khai" |
|---|---|---|---|
| Q26b | TRƯỢT: tl/t3s 57,6 %, 165 s | **ĐẠT**: 23 bối cảnh, lớn nhất eo-dat 22,4 %, liên tục 63,5 s | ĐẠT |
| Q37 / NHIP-K2 / Q37 (1.13) | TRƯỢT: TB 3,95 s, dài nhất 10,0 s | TRƯỢT: miễn 2 khoảng (KA1782, KB1943); dài nhất vẫn 10,0 s (khung neo chưa khai `khung_neo`); (a) beats lệch như cũ | như (1) |
| A1–A13 | CHỈ BÁO | CHỈ BÁO; A4, A8, A9, A10, A13 KHÔNG ÁP | như (1) |
| ML1 | TRƯỢT: 0/84 gắn, trôi 72,0 % | TRƯỢT (như cũ: không có lời khoá) | TRƯỢT: **76/84 gắn, trôi 4,5 %** (≤ 15 %). 7 lỗi Chặn (c) **thật**: `cau` "May 1940:" (SM3/0, SM3/1: câu cắt ở dấu hai chấm, không phải câu của lời), 1g/0, 1h/0 không khớp lời khoá v4.1; claim S114 (4g, KB1943) và C08 (KA2026) không có trong claims-vay-ham.md |
| NC-H5 | ĐẠT ("không áp") | **TRƯỢT** (b): 3 ghost không có nguồn (không log shot) | **THIẾU** (a): chưa có `nam_khung`; (b) ĐẠT — nguồn ghost lấy từ log shot, có trong mô tả |
| K-LAI-2 | TRƯỢT | TRƯỢT (không khối `lai:` — việc của tập) | như (1) |
| SACH-1 | — | **TRƯỢT**: 40 số/câu trích (p.so, thẻ num/quote/list), 15 ảnh tư liệu đứng riêng; (c)(d) THIẾU (không log chữ) | như (1) |
| CHUONG-1 | — | ĐẠT (0 thẻ) | ĐẠT |
| PP-1 | — | **TRƯỢT**: 1 thẻ 5,0 s, 69 từ = 13,8 từ/s | như (1) |
| TL-1 | — | CẢNH BÁO: video **112 cắt = 9,24 cắt/phút** (> 5); đặc tả ≤ 10,48 (cận trên); (a) THIẾU | như (1) + 43 shot log chưa có `goc`. Tham khảo: trôi máy 50 shot 3D trung vị **2,73 %/s**, chỉ 21/50 ≤ 2 %/s |
| TL-2 / TL-3 | — | CẢNH BÁO (THIẾU log shot) | CẢNH BÁO (THIẾU `goc`) |
| NHIP-NGHIA / XEM-CAM | — | TRƯỢT (THIẾU tệp) | như (1) |
| PC-1 | — | KHÔNG ÁP | ĐẠT (0 ảnh phục chế dùng; bảng Δ ở §2) |

Đọc: T3 animatic là bản trước luật 19/10. Số trên chính là danh sách việc của V7-PILOT; không có luật nào đổi để cho T3 qua.

## 4. Selftest
| Bộ | Kết quả (cây đã khoá 1.16.0) | Thời gian |
|---|---|---|
| `selftest_k116.py` (mới) | **129/129**, 23 nhóm: cổng 3 · SACH-1 13 · CHUONG-1 10 · PP-1 7 · TL-1 10 · TL-2 5 · TL-3 6 · NHIP-NGHIA 7 · XEM-CAM 9 · PC-1 6 · K-LAI-2 6 · K-LAI-3 6 · K-LAI-4 1 · K-LAI-5 2 · K-LAI-6 3 · K-LAI-3V 3 · NC-H5 5 · BD-3 4 · Q26b 3 · Q37 6 · A* 5 · ML1 2 · cấp 6. Mọi luật có ≥ 1 ca đạt + ≥ 1 ca trượt | 9 s |
| `selftest_k115.py` | **105/105** | 11 s |
| `selftest_k114.py` | **126/126** | 14 s |
| `selftest_k113.py` | **64/64** | 7 s |
| `selftest_k1122.py` | **37/37** | 3 s |
| `selftest_k1121.py` | **48/48** | 12 s |
| `selftest_k112.py` | **75/75** | 11 s |
| `selftest_k2.py` | **129/129** | 40 s |
| `selftest_ll.py` | **317/317** | 95 s |
| `k2check` T1 (`fixtures/k2c106-g2`) 1.15 ↔ 1.16 | **30/30 hàng giống hệt** (kq, val, lỗi, sát ngưỡng; LOCK KHỚP ở cả hai) + 1 hàng mới "1.16 KHÔNG ÁP" | — |
| `k2check` T2 L5 + `--bo-tl` gib20 1.15 ↔ 1.16 | **48/48 hàng giống hệt** + 1 hàng mới KHÔNG ÁP | — |

- Bản 1.15 chạy từ worktree tạm `origin/main` @ `8cedb8af` (ngoài repo).
- Fixture 1.16 (`checks/ll/fixtures/k116/`, ≈ 1,3 MB):
  - `ep-t3/` và `vid/` tổng hợp, sinh bằng `make_fixtures.py`;
  - bản SAO dữ liệu thật: `v6/` (log khung + log chữ đoạn thử V6, sổ PT3 133 vân) và `g1b/kiem.json`.
- Không gọi mạng hay API.
- L1 (`checks/selftest/run_selftest.py`) không chạy: 1.16 không đổi `checks/cinecheck/` ngoài chuỗi `VERSION`.

## 5. Golden (P10C-5) — chụp lại theo trình dựng V6
- **Cách làm**: `scripts/common/golden.py run --only steel,ll08,t1` (bộ công cụ hiện hành = V6, llvmpipe). `moi.png` của lượt A thành tham chiếu mới `checks/golden/tham_chieu/<ca>.png`. SHA cũ/mới ghi trong `checks/golden/GOLDEN-V6.json`; tham chiếu khoá trong LOCK.
- **Lý do**:
  - Tham chiếu cũ là khung master LFS dựng trước V6.
  - Lượt A cho đúng số P-1910: steel 0,9449 KHỚP, ll08 0,9307 KHỚP, t1 0,9082 LỆCH CỤC BỘ 22/144.
  - Sheet t1 (`reports/k116/do/golden-t1-sheet-truoc.jpg`) cho thấy **ô lệch là dòng nguồn đáy**: bộ công cụ hiện hành vẽ 38 px, hai dòng; master vẽ nhỏ, một dòng. Thêm bóng đổ và tông của V6.
  - Đây là thay đổi có chủ đích (§12.5 chọn V6, Q36 nguồn ≥ 38 px), không phải hồi quy. Giữ tham chiếu cũ thì một lượt sửa nữa có thể đẩy t1 dưới 0,90 mà không có lỗi thật nào.
- **SSIM sau chụp lại**: lượt B là một lần dựng độc lập, chạy lại cả prep, hero.js, render.js. So bằng `checks/golden/so_golden.py` (bản sao độc lập thước của golden.py).

| Ca | Tham chiếu cũ (khung trích LFS) SHA-256 | Tham chiếu mới V6 SHA-256 | Trước (so cũ) | Sau (lượt B so mới) |
|---|---|---|---|---|
| steel (đoạn 01, khung 395) | `03202ae23e32bc0d21f2c786d3b35d5aa51f5c8f7ba50a257c88611750967283` (oid `28e4d1137828`) | `eb731fd47a9001c29d321d64c4281a9ce3bf983bacaeeed47eab79fc03b78a4f` | SSIM 0,9449 · MAD 2,08 · 0/144 · KHỚP | **SSIM 1,0 · MAD 0,0 · 0/144 · KHỚP** |
| ll08 (đoạn 03, khung 2102) | `d14988c7982a6f6b8b053f1051ff0e1ff756c303ca6ce7dcf896ecc36be21e41` (oid `d22d7d6e640d`) | `4eaafa5bf5da7efb56be41418f555e3854061defeb3faf834ab27d16e690f2c8` | SSIM 0,9307 · MAD 2,25 · 0/144 · KHỚP | **SSIM 1,0 · MAD 0,0 · 0/144 · KHỚP** |
| t1 (đoạn 00, khung 48) | `4861487d6fc04ff1873c1eee647444ee3e9996504c15e2191744aaea6e9d6c67` (oid `4f2d280bc649`) | `30b71b7bb8ec47f4cf75c3524a82bf79134de2817fe523c97ecdecc56fd25ecf` | SSIM 0,9082 · MAD 4,51 · **22/144 · LỆCH CỤC BỘ** | **SSIM 1,0 · MAD 0,0 · 0/144 · KHỚP** |

- Lượt B trùng lượt A **từng điểm ảnh** ⇒ trình dựng V6 trên llvmpipe tất định ở 3 khung này. Từ nay mọi đổi điểm ảnh đều hiện ra.
- `golden.py` (trong `scripts/`, ngoài vùng K) **chưa đổi**, vẫn so với master LFS. Cách dùng tham chiếu mới: sau `golden.py run --out <ra>` chạy `checks/golden/so_golden.py <ra>`. Hoặc phiên Nền tảng trỏ `golden.py` tới `checks/golden/` (§9 K116-D7).
- Số đo: `reports/k116/do/golden-a.json`, `golden-b.json`, `golden-v6-b.json`.

## 6. LOCK
- **Trước**: 1.15.0 `f4fa0349ca53b05d64e4303554ec168e6445c82d97e662672f70ccf42df80d40`.
- **Sau**: **1.16.0 `dbbb6cd0606cf37363738711fa8da1b24de29ada4edd1875c1e0adb25d31a439`** (DATE_UTC 2026-10-19T10:33:38Z). `python3 -I checks/lock.py --verify` → **KHỚP**.
- Thuật toán không đổi. `lock.py` không cờ gọi đúng một lần, sau khi selftest k116 + 8 bộ cũ đạt. Mọi selftest chạy lại trên cây đã khoá (§4).

## 7. Sổ
| Sổ | Dòng thêm |
|---|---|
| `AUTHORSHIP.md` | (1) **GC-C′** isthmus `iss-muss` → `issmus`, duyệt 19/10 16:47 (PLS `714314cf…305b` trên nhánh `k2c-t3-kl42`); (2) **giãn shot T3 phương án B 745,0 s**, duyệt 16:47 (12 shot giãn +30,3 s, 13 shot rút đuôi −6,5 s); (3) **D11 = A**, chọn ≈ 13:20 khi dán lệnh KL42-THU, bổ sung giờ cho dòng D11 của KL42 |
| `COST-LEDGER.csv` | **CASTING-GIONG**: EL 25 627 gửi, bộ đếm +12 011, Claude $0, 1,5 h (theo `reports/CASTING-GIONG-BAO-CAO.md` §5) · **KL42**: EL 12 052 gửi, bộ đếm +5 302, $0, 1,25 h, 745,0 s (theo `reports/kl42/KL42-BAO-CAO.md` trên nhánh `k2c-t3-kl42` @4cd2d941) · **K-1.16**: $0, EL 0, 0,8 h. Kiểm bằng `csv`: **61 dòng, mọi dòng đúng 20 cột**; xuống dòng LF như tệp gốc |

- Nhánh `k2c-t3-kl42` cũng thêm dòng vào cuối AUTHORSHIP. Khi P merge cả hai nhánh, chỗ nối cuối tệp sẽ xung đột. Đây là xung đột nối đuôi; giữ cả hai khối là đúng.

## 8. Chỉ số trong ±5 % quanh ngưỡng (luật cứng)
**Dữ liệu thật:**
- Golden **trước** chụp lại: t1 SSIM **0,9082** so 0,90 (+0,9 %), ll08 0,9307 (+3,4 %), steel 0,9449 (+4,99 %). Sau chụp lại: 1,0.
- T3 animatic: không chỉ số 1.16 nào nằm trong ±5 %.
  - Gần nhưng ngoài ±5 %: Q26b eo-dat 22,4 % so 25 % (−10,4 %); PC-1 000761·Swin2SR Δ +1,13 so 1,0 (+13 %).

**Ca fixture cố ý đặt đúng hoặc sát ngưỡng:**
| Ca | Giá trị | Ngưỡng |
|---|---|---|
| PP-1 thẻ | 9,0 s | cận trên 9 s |
| CHUONG-1 | 8 thẻ; 3,0 s | 8/tập; 3 s |
| XEM-CAM | 6/8 | 6/8 |
| NHIP-NGHIA | 93,3 % | 90 % (+3,7 %) |
| Video v-ok, đẩy máy phóng 3 %/s | 1,61 %/s | 2 %/s (−19,5 %, ngoài ±5 %) |

**Không thêm phần tử nào để vượt ngưỡng.** Bản "khai" T3 chỉ trỏ tới tệp đã có trong repo; không sửa đặc tả hay tệp của tập.

## 9. Quyết định đề xuất (chờ chủ dự án)
| # | Đề xuất | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|---|
| K116-D1 | **Duyệt mức 1.16** như bảng §3 (Chặn: SACH-1, CHUONG-1, PP-1, NHIP-NGHIA, XEM-CAM; Cảnh báo: TL-1/2/3 tới V7-PILOT, PC-1, K-LAI-3V) và các thay đổi khiếu nại §2 | Luật khớp Kinh thánh 19/10; T3 có thước trước khi dựng lại | V7-PILOT phải xuất thêm trường (D9) | Hàng mới vẫn CHỈ BÁO tới khi duyệt | Mức Chặn của SACH-1 (c) cần log chữ: chưa có log → THIẾU = chặn |
| K116-D2 | **XEM-CAM "đạt ≥ 6/8"**: K đọc là **mỗi người chấm ≥ 6/8** (chặt nhất). Phương án khác: trung vị 4 người ≥ 6/8, hoặc chủ dự án ≥ 6/8 + TB AI ≥ 6/8 | Không để một người hiểu sai bị che | Một AI chấm kém có thể chặn | Định nghĩa đạt | Đọc sai ý chủ dự án; cần một câu trả lời |
| K116-D3 | **Chữ bản đồ** (chú giải phe, nhãn điểm, nhãn inset, tag, index) dưới §12.1: cho phép như "nhãn bản đồ" ở shot strategic/inset, hay cấm? K đang để Cảnh báo (e) | Giữ §11.1 (chú giải ≤ 3 phe, inset 1–2 nhãn) và NC-H4 | §12.1 viết "CHỈ có" | SACH-1 (e) | Hai đoạn Kinh thánh mâu thuẫn ngầm tới khi quyết |
| K116-D4 | **Q37 ↔ TL-1**: TL-1 muốn shot ≥ 12 s, máy cố định; Q37 muốn biến cố ≤ 3,5 s TB. Đề xuất: sau V7-PILOT, K đo **biến cố thời gian chạy trên video** (đổi nội dung trong cửa sổ máy cố định) và cộng vào Q37, như I8. **Không** nhận biến cố tự khai trong log | Hết mâu thuẫn bằng số đo thật | Cần dữ liệu V7 để hiệu chuẩn | Q37 cho tập timelapse | Trước khi có thước, shot timelapse 12 s dễ trượt Q37 (c) |
| K116-D5 | **K-LAI-3V**: nghi vấn còn ghi của vân → Chặn như tấm C (K-LAI-3 (c)), hay giữ Cảnh báo | Nhất quán với tấm C | 65/69 vân V6 đang có nghi vấn → chặn ngay | Sổ PT3/V6 | — |
| K116-D6 | **Đo phóng bằng LK** thay vì phase correlation (log-polar sai chiều trên dữ liệu thử); tịnh tiến vẫn phase correlation | Đo đúng đẩy máy (1,61 so lý thuyết 1,6 %/s) | Lệch chữ của lệnh | TL-1 (d) | LK yếu trên vùng trời/nước phẳng — khi đó chỉ còn tịnh tiến |
| K116-D7 | **Nền tảng trỏ `golden.py` tới `checks/golden/tham_chieu/`** (1 dòng, ngoài vùng K) | Một lệnh như cũ | Phải sửa `scripts/` | Hồi quy so với V6 | Tham chiếu V6 sẽ phải chụp lại nếu chủ dự án đổi mức dựng |
| K116-D8 | **"≈ 8 s"** của D6 = 7–9 s; tốc độ đọc ≤ 3 từ/s (Cảnh báo) | Có số để đo | K tự đọc chữ "≈" | PP-1 | — |
| K116-D9 | **V7-PILOT xuất**: log shot có `goc`, `tl`, `vai`, `trong_pct`, `su_kien`, `diem_may`; `nhip-vat.json`; `xem-cam.json`; `nam_khung`; log chữ k2.js trong lượt kiểm; khai `khung_neo: true` cho MỌI shot khung neo, `im_lang: true`; mô tả có nguồn ghost/ranh; khối `lai:` có sổ vân + `dieu_kien_dat` | Mọi hàng 1.16 đo được, hết THIẾU | Thêm tệp xuất | Một bước xuất ở trình dựng (ngoài vùng K) | — |

## 10. Chi phí thật
| Khoản | Lệnh | Thực tế |
|---|---|---|
| Claude API / OpenAI / ElevenLabs / YouTube | 0 | **$0 / $0 / 0 ký tự / 0 đơn vị**. prep timeline T3 và golden chạy với proxy chặn hoặc không gọi dịch vụ trả phí; golden đọc khung master LFS qua HTTP (không tính phí) |
| Giờ máy | mốc theo dõi 4 h | **≈ 0,8 h** thời gian thực (09:58 → ≈ 10:40 UTC). Gồm: golden 2 lượt × 3 ca (295 s + 281 s); k2check T3 ×5 lượt (≈ 3–6 phút mỗi lượt, song song); k2check T1/T2 ×3; selftest 9 bộ ×2 lượt; prep T3; `pip` + `npm ci` để `verify.sh` đủ 15 PASS (không đổi tệp git) |
| Mạng | — | `git fetch` main, 3 nhánh release, `k2c-t3-kl42` (chỉ đọc); LFS batch API cho golden |

## 11. Tệp đã sửa (`git diff --stat 8cedb8af..HEAD`)
| Tệp | Việc |
|---|---|
| `checks/ll/q_k116.py` (mới) | SACH-1, CHUONG-1, PP-1, TL-1/2/3 + thước video, NHIP-NGHIA, XEM-CAM, PC-1; K-LAI-2, NC-H5, BD-3 bản 1.16; ML1 lời khoá; miễn Q37 |
| `checks/ll/q_lai.py` | `check116`: nhánh vân, K-LAI-3V, K-LAI-6 vân (đường `check` 1.15 không đổi) |
| `checks/ll/q_setting.py`, `q_nhip.py`, `q_k2var.py`, `q_amthanh.py` | tham số `v116` / `mien` (mặc định = hành vi 1.15) |
| `checks/ll/k2check.py`, `cap112.py` | cổng 1.16, hàng mới, mức đề xuất; `--tl16-video`, `--log-shot` |
| `checks/ll/selftest_k116.py`, `checks/ll/fixtures/k116/` (mới) | 129 ca; fixture tổng hợp + bản sao thật V6/PT3/G1b |
| `checks/golden/` (mới) | `so_golden.py`, `GOLDEN-V6.json`, `tham_chieu/{steel,ll08,t1}.png` (5,1 MB) |
| `checks/ll/RULES-LL.md` | mục 1.16 (tên trường cho phiên xưởng, gồm ML1/FT1) + tự kiểm |
| `checks/cinecheck/__init__.py`, `checks/LOCK` | 1.16.0 |
| `AUTHORSHIP.md`, `COST-LEDGER.csv` | §7 |
| `reports/k116/` | báo cáo, CHECKPOINT, `do/` (k2check T3, golden) |

## 12. Preflight, đẩy
- Hook pre-commit và pre-push (`tools/preflight.sh`) cài từ đầu phiên. Không dùng `--no-verify`.
- Checkpoint: mã `checks/` đang sửa được cất ra ngoài repo trước khi commit, nên `lock.py --verify` trong preflight vẫn KHỚP với LOCK 1.15.0.
  - Lần đầu của checkpoint 3: **preflight CHẶN** vì bản vá việc dở 8,3 MB (> 5 MB, có PNG golden và video fixture). Không có gì bị commit.
  - K bỏ phần nhị phân khỏi bản vá (510 KB) rồi commit lại: **ĐẠT**.
- Commit mã `a7162b05` (38 tệp): **PREFLIGHT ĐẠT**, LOCK **KHỚP** 1.16.0; pre-push ĐẠT.
- Commit báo cáo (chứa tệp này): preflight chạy như trên. Kết quả ghi ở thông điệp đẩy cuối; không đổi mã.

## 13. Việc chờ chủ dự án
1. **Duyệt bảng khiếu nại §2** (6 chấp nhận, 2 chấp nhận một phần, 1 trả lời tên trường) và **mức 1.16** (K116-D1).
2. **Quyết K116-D2** (cách hiểu "≥ 6/8"), **D3** (chữ bản đồ dưới §12.1), **D4** (Q37 ↔ TL-1 sau V7-PILOT), **D5** (K-LAI-3V Chặn hay Cảnh báo), **D6** (đo phóng bằng LK), **D8** ("≈ 8 s" = 7–9 s).
3. **Golden**: chấp nhận tham chiếu V6 (§5); giao Nền tảng trỏ `golden.py` sang `checks/golden/` (D7).
4. **Giao V7-PILOT/V xuất trường** ở K116-D9. Ngưỡng TL-1/2/3 hiệu chỉnh trên số đo V7-PILOT, ở một lượt K sau.
5. **V6/PT3**: ghi kết quả "kiểm trôi" cho 55 tệp vân "dùng nếu đạt kiểm trôi" (K-LAI-3 đang THIẾU).
6. **Tập T3**: sửa 7 lỗi khai ML1 thật (§3.5): "May 1940:", 1g, 1h, claim S114/C08. FT1 khai `ly_do_hinh`.
7. **Duyệt merge nhánh `ccr-3194130e-kijmlg`** (P merge; chú ý chỗ nối cuối AUTHORSHIP với nhánh `k2c-t3-kl42`, §7).

**DỪNG — chờ chủ dự án.**
