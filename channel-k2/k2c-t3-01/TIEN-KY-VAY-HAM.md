# TIỀN KỲ T3b — Gibraltar khung "vây hãm": vì sao ai cũng tranh giành Rock (K2C-T3-01)

> Phiên tiền kỳ T3b, 17/10/2026, theo lệnh chủ dự án (duyệt NC-LS 17/10). Nhánh `k2c-t3-tienky-b` từ `origin/k2c-t3-tienky` @ `d8e83cc`. **Chỉ tài liệu + tải tư liệu có quyền. Không merge. DỪNG chờ chủ dự án.**
> Đọc kèm: `claims-vay-ham.md` (123 claim mới), `tienky/claims.json` (C01–C35 của TIEN-KY, giữ nguyên), `vay-ham/` (bảng shot máy đọc, bộ tự kiểm, bảng tài sản, ảnh xem trước).
> Mọi câu trích là nguyên văn từ tệp tải bằng curl (tệp thô ngoài git, `/var/tmp/cine-out/t3b/`, SHA-256 trong repo). Lượt xem YouTube không dùng trong báo cáo này. Số giờ người là **(ước)**.

## Khối điều lệ (lệnh + thực tế)
| Trường | Lệnh | Thực tế |
|---|---|---|
| Loại phiên | Tiền kỳ T3b (chỉ tài liệu + tư liệu có quyền) | đúng |
| Nhánh | `k2c-t3-tienky-b` từ `origin/k2c-t3-tienky` | đúng (`d8e83cc`); đẩy, không merge |
| Tệp được sửa | CHỈ `channel-k2/k2c-t3-01/**` | chỉ thêm: `TIEN-KY-VAY-HAM.md`, `claims-vay-ham.md`, `licenses/` (+42 tệp: 39 tư liệu + OSM + Catastro + chép 0 tệp trùng), `vay-ham/` (JSON, 4 script nhỏ, 39 ảnh xem trước 14 MB ≤ 20 MB). **Không** sửa `TIEN-KY.md`, `tienky/*`, main, `checks/`, `scripts/`, `design/`, `docs/`, nhánh khác. Không ghi RIGHTS/AUTHORSHIP/COST-LEDGER (đề xuất §9) |
| Trần | Claude API ≤ $1 (ghim) · YouTube ≤ 500 đv · ElevenLabs 0 · giờ máy ≤ 1 h | **$0** (không gọi API trả tiền) · **200 đv** · **0** · **≈ 0,15 h** (§9) |
| Preflight | bắt buộc; che email | hook pre-commit/pre-push cài đầu phiên; mọi commit **PREFLIGHT ĐẠT**, `lock.py --verify` **KHỚP**; 0 email trong tệp ghi (giấy phép đã che) |
| Nội dung kênh khác | không đưa video/khung/lời kênh khác vào repo | đúng: 2 lượt `search.list` chỉ để tránh trùng tiêu đề; tiêu đề đối thủ để ngoài git, báo cáo chỉ nêu mẫu cần tránh |
| Điều kiện dừng | xong → đẩy → dừng; không dừng hỏi giữa chừng | (1) xong việc. Câu hỏi không chặn đã tự quyết (§10) |

---

## 0. Tóm tắt (đọc 2 phút)
1. **"14 sieges" ĐỨNG VỮNG — cả hai phía cùng cách đếm.** Sayer 1862 ("Fourteen Sieges"), Stephens 1870, Bảo tàng Quốc gia Gibraltar (1704–05 là cuộc thứ 12, 1727 thứ 13, Great Siege "the last") và sử học Tây Ban Nha hiện đại (García Sanz 2022: 1704 là "undécimo asedio") đều đếm **14 cuộc, 1309–1783** (1333 tính hai lần; 1704 và 1704–05 là hai cuộc; không tính cướp biển 1540). Con số 15 (cộng đóng cổng 1969–85) chỉ có ở nguồn bách khoa → không dùng. Câu đề xuất: *"Historians count fourteen sieges of Gibraltar between 1309 and 1783."* (S001–S008).
2. **Claims vây hãm: 123 claim mới** (99 XÁC MINH · 21 MÂU THUẪN có ghi cách nói hai phía · 3 CHƯA XÁC MINH), trích từ 46 nguồn (65 tệp đã tải) (Drinkwater 1785/86/1905, nhật ký Spilsbury, Ancell; Montero 1860; bản biện hộ phía Pháp 1785; Jenkinson 1785 + Chalmers 1790 cho Điều X Utrecht; Elcano ARI 19/2013 bản Tây Ban Nha; Marquina Barrio 1981; Almoraima/IECG; Hansard; HMGoG; UK Mil AIP…). **Phiên P kiểm lại độc lập mọi câu trích với tệp có đúng SHA: 116/123 khớp nguyên khối, 7 khớp theo mảnh** (lệch một mảnh do OCR/ngắt dòng → đối chiếu ảnh trang trước khi lên hình).
   - **Điều X Utrecht (13/7/1713): đủ toàn văn Anh + Tây Ban Nha.** Bản chép của Gibraltar Heritage Trust có lỗi đổi nghĩa ("having the sale" thay "the same") → **không dùng bản này trên hình**.
   - **Số hai phía (Great Siege):** quân Pháp–TBN 33 000 (Montero) – gần 40 000 (Drinkwater); 10 pin nổi 138–142 pháo, 5 190–5 260 người; tổn thất ngày 13–14/9/1782 "hơn 2 000" theo cả hai sử Anh/TBN, nhưng bản biện hộ Pháp chỉ nhận 185 do pháo; đồn Anh cả cuộc vây 333 chết trận/vì thương + 536 chết bệnh (Drinkwater) ↔ "gần 2 000" (Montero); Pháp–TBN "gần 6 000" (Montero). Giờ khai hoả 13/9/1782: 09:30 vào vị trí → 09:45 Anh bắn → 10:25 toàn tuyến (ba nguồn) — đủ cho bộ đếm giờ + mặt trời (M6).
   - **Hậu cần (khán giả hỏi nhiều):** đói 1/1780 (cây kế, bồ công anh, tỏi dại; giá trứng), scorbut chữa bằng chanh từ một tàu Đan Mạch đi Malaga (không phải tàu Hà Lan), ba đoàn tiếp tế (1/1780, 4/1781, 10/1782), đạn: đồn bắn 205 328 phát, đối phương 258 387 (từ 12/4/1781), ~8 000 thùng thuốc súng.
   - **Đường hầm 1782:** đào từ 25/5/1782; 13 người, ~82 ft trong 5 tuần (Spilsbury 4/7); 140 ft ngày 5/8; ~600 ft tháng 5/1783 (MÂU THUẪN với các số phổ biến). **"Henry Ince đề xuất" chỉ có nguồn bách khoa → CHƯA XÁC MINH**; nói "Sergeant Ince's gallery" (Spilsbury) là an toàn.
   - **1941:** dải cỏ 1934–36 (£573); đường băng cứng từ cuối 1939; cuối 11/1941 quyết định nối ra biển tới 1 550 yd (≈ 1 417 m), dùng được 7/1943; 1955 tới 6 000 ft; nay **1 798 × 45 m** (UK Mil AIP). Đá lấp từ vách bắc + đá đào hầm (HMGoG 199/2018). Lấn vịnh "500 m" chỉ có một nguồn Tây Ban Nha → chưa đối chứng. **Hầm: ~55 km tổng** (HMGoG 310/2017, Nature Reserve; Hansard "34 miles") — **~30 km đào trong WWII** chỉ một nguồn (hướng dẫn viên bảo tàng).
3. **Tư liệu có quyền: 39 tài sản mới**, tất cả PD/CC0/"no known restrictions" (đã kiểm lại SHA 39/39). Đủ cho mọi mốc **trừ 1830–60 (yếu)**: bình đồ 1705 (Rijksmuseum CC0, Visscher 1706 LoC), Homann 1733, Faden 1781/1783 (công sự TBN tới 19/10/1782), Drinkwater 1786 (plan cuộc xuất kích, plan các khẩu đội 13/9/1782), Sayer 1865, **AMS M981 1943 1:10 000 Gibraltar + La Línea** (từng nhà, có lưới toạ độ → RMS ước ~12 m), plan hầm ONI 1954 (NARA), bản khắc Sharp theo Copley (LoC), "Destruction of the Floating Batteries" (Rijks), ảnh 1860 "neutral ground" (Rijks CC0), màu nước 1844 (YCBA CC0), ảnh NARA 2/10/1943 (C-47 ở North Front). **Không có ảnh PD đúng năm 1941** (thi công đường băng, đào hầm, sơ tán) ngoài IWM (đã loại).
4. **Thành phố có nhà (NC-H1, lỗi T2):** mọi shot 3D nói về phố đều có nguồn nhà đúng mốc: 2026 = OSM (706 toà trong phố cổ 1,07 km²; 1 419 toà lõi 3,7 km²; **chỉ 8 toà có số tầng** → chiều cao phải ước), La Línea = Catastro (tầng ĐẦY ĐỦ), 1943 = AMS (từng nhà), 1782 = Drinkwater 1786 + Faden 1783 (khối phố), 1727 = Homann 1733 (khối phố), 1704 = Exact Plan 1705 + Visscher 1706 (khối phố, RMS ước 100–120 m). **Công số hoá ≈ 37–47 giờ người (ước)** cho 3 mốc ghost bắt buộc (1704, 1782, 1943) ở lõi ≈ 1 km² (§3). Mốc 1830–60 và 1810 **không dựng nhà** → bản đồ lịch sử phẳng có nhãn / 3D vùng không nói phố.
5. **Treatment (§4): Móc + 5 chương, 65 shot, 9:23,5** (Kinh thánh §3: 9–11 phút), 6 mốc đinh, **2 cú liên hoàn** (#1 gib20 1941 đã dựng; #2 mới: bay thấp mặt vịnh → orbit King's Bastion, dừng 13/9/1782 09:45 → reveal 10 pin nổi). **Tự kiểm ĐẠT mọi luật:** Q26b-K2 (6 loại mỗi nửa; lớn nhất 42,2 % / 39,1 %), NC-H2 (1 lần, 2,5 s), NC-H3 (99,2 % ≤ 60 km; 87,5 % ≤ 3 km), NC-H1, lặp vùng+góc tối đa 1, footage 0,9 %. **Vượt:** hồ sơ thật 20,7 % > 10–15 % (đề xuất ngoại lệ cho thể loại lịch sử, D4).
6. **Máy dựng (§5):** V5b-2b nhận **P0** = tích hợp 9 điểm V5b-2a §8 + M9 (nạp footprint + mái theo 3 thời kỳ) + M12 (bản đồ pha/ghost theo mốc) + M6 (ngày/giờ + mặt trời) + M3/M4 rút gọn (pin nổi, chiến tuyến, hạm đội) + đo AGL vào meta; **P1** = M1, M7, M8, M11; **P2** = M5 đầy đủ. Hero: Rock + vách bắc, King's Bastion (OSM 1 294 m² + khu 4 231 m²), Línea de Contravalación + 2 pháo đài, 10 pin nổi, Great Siege Tunnels, đường băng 1934→1943→nay, cổng biên giới.
7. **Đóng gói (§7):** tiêu đề đề xuất **"Why Gibraltar Was Besieged 14 Times"** (35 ký tự) + 2 phương án; tránh mẫu "Why everyone wants…" (đã có video dùng). Thumbnail A (bản đồ 3D, chiến tuyến 1782 + đường băng, hộp "14 SIEGES", không cờ/không vũ khí chĩa người) và B (chia đôi 1782 sepia ↔ 2026, không chữ).
8. **Lộ trình (§8):** T3b → duyệt D → (V5b-2b P0 ∥ số hoá ghost 1782) → đoạn thử phố Gibraltar qua cổng chuẩn hình → G1b → render → G2 → đăng **trước 14/12/2026**. G1 (lời) song song. Có 3 điểm cắt giảm không hạ chất lượng (đổi loại cảnh, chạy lại tự kiểm).
9. **Chi phí thật:** Claude API **$0** · YouTube **200/500 đv** · ElevenLabs **0** · giờ máy **≈ 0,15 h** · mạng ≈ 1,1 GB (ngoài git). Token: 4 tác tử Claude Code ≈ 1,04 triệu token (trần mềm; không qua API trả tiền).

### Bảng quyết định đề xuất (chờ chủ dự án)
| # | Đề xuất | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|---|
| D1 | **Nói "14 sieges"** đúng câu "Historians count fourteen sieges … between 1309 and 1783"; tiêu đề T-A dùng số 14 | 4 nguồn hai phía khớp; số tròn mạnh cho tiêu đề/thumbnail | nguồn chính là sử thế kỷ 19 + bảo tàng; danh sách hiện đại (Fa & Finlayson) chưa đọc bản gốc | lời ch.0, ch.1, ch.5; thumbnail A | khán giả cãi "15 (tính 1969)" → ghim nguồn + cách đếm |
| D2 | **Mạch Móc + 5 chương, 9:23** (Great Siege 2:48 là trục; cú lật kinh tế dồn vào ch.5 ≈ 1:40) | đúng mạch NC-LS §4.2; vây hãm là khung, kinh tế là kết | phần kinh tế ngắn hơn TIEN-KY (11:30) | lời G1; Short | khán giả kinh tế cũ thấy ít "Moving Parts" → giữ cú lật làm câu chốt |
| D3 | **Cú liên hoàn #2 (vịnh 13/9/1782)** + tái dùng #1 (gib20 1941) | hai bước ngoặt lớn nhất có cú máy riêng; #1 đã dựng | #2 cần M3/M6/M7 + ghost 1782 | thêm ≈ 0,4 h máy (ước) | nếu M7 trễ → khói tối giản, không bỏ cú |
| D4 | **Ngoại lệ "hồ sơ thật" 20,7 %** (Kinh thánh 10–15 %) cho tập lịch sử | tranh/bản đồ/văn bản đúng thời kỳ là bằng chứng "every date sourced" (lời hứa L1) | lệch Kinh thánh | ghi ngoại lệ ở AUTHORSHIP; hoặc giảm 3 shot ảnh → 3D | bị chê "slideshow" → mọi tranh/bản đồ có máy trượt + nhãn neo |
| D5 | **Phạm vi số hoá ghost: 3 mốc bắt buộc (1704, 1782, 1943) ở lõi ≈ 1 km², mức khối phố (1943 từng nhà)** ≈ 37–47 h người | đúng NC-H1; dữ liệu có quyền đã đủ | công người lớn; người làm chưa định | phiên tiền kỳ số hoá song song V5b-2b | trễ → shot 1d/1e/2g đổi sang bản đồ phẳng (đã có) |
| D6 | **Ưu tiên máy dựng P0/P1/P2** như §5 | khớp đúng bảng shot; không làm M2 (đội hình bộ binh) | V5b-2b dài hơn | ≈ 1,5–2 h máy thử (ước NC-LS) | P0 trễ chặn G1b |
| D7 | **Luật hình chiến sự** CS1–CS10 + crop tranh (§6) | giữ đủ quảng cáo; kể hai phía | mất tranh "đẹp" (Emes, nửa trái Copley) | REVIEWER kiểm ở G1 | — |
| D8 | **AMS 1943 bản Princeton = ĐIỀU KIỆN**: lên hình dùng bản Yale 15487373; Princeton chỉ để nắn | tránh câu "non-commercial" của Princeton | phải tải thêm bản Yale | +1 tải | thấp (tác phẩm gốc PD-USGov) |
| D9 | **Ảnh 1941**: đặt LoC Duplication Services quét lô LoC 2005677710 (16 ảnh 1942, "No known restrictions", có đào hầm) | lấp lỗ "không ảnh 1941" | phí + thời gian chờ (chưa rõ) | shot 4a/4d có ảnh thật | nếu không kịp → giữ NARA 1943 + AMS |
| D10 | **Tiêu đề + thumbnail** §7 (T-A + thumbnail A/B Test & Compare) | số 14 có nguồn; không cờ | — | gói G1 | — |


**Chỉ số trong ±5 % quanh ngưỡng (nêu tên):**
- **Móc 43,5 s** so trần 45 s (Kinh thánh §3): −3,3 %. Lời G1 phải giữ móc ≤ 45 s; nếu dài hơn thì cắt shot 0g (5 s) trước.
- **Đường băng 1955 "6 000 ft" = 1 828,8 m** so AIP 1 798 m: lệch +1,7 % (hai nguồn chính thức; MÂU THUẪN S093) — hero dựng theo AIP, lời không nói số 1955.
- Bộ tự kiểm bảng shot: không chỉ số nào trong ±5 % (§4.3).
- Ước georef (của gói tư liệu, chưa chạy GCP thật) không có ngưỡng → không xét.

**Việc chờ chủ dự án:** §11.

---

## 1. Claims vây hãm (chi tiết: `claims-vay-ham.md`, máy đọc `vay-ham/claims-vay-ham.json`)

### 1.1 Cách làm và kiểm
- 3 gói tra nguồn chạy song song (1704/Utrecht/eo đất · Great Siege · 1941/hầm). Mỗi câu trích chép từ tệp tải bằng curl (djvu.txt archive.org, PDF, HTML), ghi URL, SHA-256, trang, ngày đọc.
- **Phiên P kiểm độc lập** (`vay-ham/verify_quotes.py`, đọc tệp thô ngoài git): tách chữ lại từ tệp có đúng SHA, so toàn câu sau khi bỏ dấu câu/khoảng trắng (ſ/f gộp). **116/123 khớp nguyên khối; 7 khớp theo mảnh** (S008, S010, S011, S018, S024, S027, S034: một mảnh lệch do OCR hoặc PDF hai cột) → ghi "đối chiếu ảnh trang trước khi lên hình" ở từng claim.
- Ưu tiên nguồn: sơ cấp (Drinkwater, Spilsbury, Ancell, Jenkinson 1785, Chalmers 1790, AIP), học thuật (Montero 1860, García Sanz 2022, Elcano, Marquina Barrio 1981, Almoraima/IECG), bảo tàng (Gibraltar National Museum), chính thức (HMGoG, Hansard, MAEUEC). Bách khoa chỉ để tìm nguồn; claim nào chỉ có bách khoa → CHƯA XÁC MINH.

### 1.2 Bảng mục bắt buộc của lệnh
| Mục lệnh | Kết luận | Claim | Cách nói an toàn |
|---|---|---|---|
| Số lần bị vây ("14" chưa kiểm) | **14, 1309–1783** — 4 nguồn hai phía, cùng cách đếm (1333 ×2; 1704 và 1704–05 tách; không tính 1540). Lệch nhỏ: bảo tàng ghi cuộc thứ 2 năm 1316 (sách cũ 1315); mục lục Sayer ghi cướp biển 1540 nhưng thân sách gọi 1506 là thứ 10. "15" (cộng 1969–85) chỉ bách khoa | S001–S008 | "Historians count fourteen sieges of Gibraltar between 1309 and 1783"; thời Anh: "four sieges between 1704 and 1783" |
| 1704: ngày | Anh (lịch cũ) 21, 23, 24/7 — TBN (lịch mới) 1, 3, 4/8; hai sử thế kỷ 19 tự giải thích lệch lịch | S012, S013 | "early August 1704" hoặc nói rõ hai lịch; TIEN-KY từng bỏ ngày 4/8 vì "mâu thuẫn" → nay **giải được** |
| 1704: ai | Rooke (hạm đội) + Hesse-Darmstadt (bộ binh), **nhân danh ứng viên Habsburg "Charles III"**; chủ quyền nghi lễ của ứng viên Áo kéo dài tới 1709 (García Sanz) | S012, S017, S020 | không kể chuyện "Rooke kéo cờ Anh nhân danh Nữ hoàng Anne" như sự thật |
| 1704: quân giữ | Montero "cien hombres" ↔ Sayer ≤ 150 chính quy, tổng ≤ 500 | S014, S015 | "a few hundred men" |
| 1704: hệ quả | điều khoản đầu hàng (đi với vũ khí, hành lý); dân chọn rời sang San Roque | S018, S019 | hai phía có nguồn |
| Utrecht 1713 Điều X (trích nguyên văn) | **toàn văn Anh** (Jenkinson 1785 "by the Queen's special Command", đối chiếu Chalmers 1790) + **bản TBN được chấp nhận chung** (Elcano ARI 19/2013; văn bản có giá trị pháp lý là tiếng Latinh). Ngày 13/7/1713: HMGoG và MAEUEC cùng ghi | S022–S029 | trích trên hình từ bản 1785 (PD); **không dùng bản chép GHT** (lỗi "having the sale") |
| Great Siege: bắt đầu/kết thúc | ba mốc bắt đầu: 21/6/1779 đóng giao thông · 16/7/1779 phong toả biển · 12/9/1779 đồn bắn phát đầu; kết thúc: 2/2/1783 tin hoà ước sơ bộ · 5/2/1783 phát súng cuối · 10/3/1783 công văn chính thức; hoà ước sơ bộ 20/1 (Drinkwater) ↔ 30/1 (Montero); Versailles 3/9/1783 | S037–S047 | "from June 1779 to February 1783" |
| Lò nung đạn đỏ | thử 23 và 25/9/1779; dùng hàng loạt 8/9/1782 (theo đề xuất của Boyd); 13/9 lò di động không đủ → nung bằng lửa củi; sau 13/9 xây lò kiểu lò vôi nung > 100 viên/1,25 h | S058–S061 | cơ chế, không cảnh trúng người |
| Pin nổi 13/9/1782 | 10 pin nổi (d'Arçon), 142 pháo dùng + 70 dự bị / 5 260 người (Drinkwater) ↔ 138 pháo / 5 190 người (Montero); cả 10 bị phá sáng 14/9; 357 người được quân Anh cứu; nguồn Pháp: d'Arçon đã xin thử với đạn đỏ trước | S065–S075, S050 | số hai phía; "all ten were lost" |
| Đường hầm 1782 | đào từ 25/5/1782 trên Farringdon's battery; 13 người ~82 ft/5 tuần; lỗ thông gió 15/7 → đặt pháo; 140 ft (5/8/1782); ~600 ft (5/1783, MÂU THUẪN); **người đề xuất = Ince: CHƯA XÁC MINH** (chỉ bách khoa); bệ pháo hạ nòng Koehler thử 15/2/1782 | S080–S087 | "Sergeant Ince's gallery" (Spilsbury); không nói "Ince proposed" |
| Số quân/thương vong hai phía | bảng `claims-vay-ham.md` §0b (9 chỉ số) | S069–S079 | luôn "by the British count / Spanish records" |
| Eo đất trung lập: từ khi nào, rào | Línea de Contravalación: Philip V ra lệnh 1730, khởi công 11/1730, xong 1735 (Verboom) — **"1730–31" trong lệnh chưa chính xác**; 1810 Anh phá các pháo đài **với sự đồng ý của TBN** (Montero ghi 1811); La Línea tách khỏi San Roque 17/1/1870 (lập 7/1870); 8/1908 Anh báo TBN "as an act of courtesy" → rào dựng 1909; TBN không công nhận rào là biên giới; Anh (Lidington 2015) "Gibraltar as including the isthmus" | S030–S036 | hai lập trường trích nguyên văn |
| 1941 đường băng | §0.2 trên; lấn vịnh 500 m chỉ một nguồn TBN | S089–S102 | "pushed out into the bay" (không nói số mét) |
| Đường hầm WWII | ~55 km tổng (HMGoG/Nature Reserve; Hansard 34 dặm); ~30 km đào trong WWII (một nguồn); Great North Road ~1 dặm; phòng bệnh viện 200 × 35 × 12 ft; sức chứa 16 000 (MÂU THUẪN về thời gian: 1 năm / 16 tháng / ~2 năm) | S106–S113 | "about 55 kilometres — more than the Rock's roads" |
| Hậu cần vây | đói 1/1780, scorbut + chanh, 3 đoàn tiếp tế, đạn 205 328 ↔ 258 387, ~8 000 thùng thuốc súng | S051–S057 | trả lời trực tiếp câu hỏi bình luận (NC-LS §1.5) |
| Thêm (không bắt buộc) | sơ tán 1940 (13 000–16 000 tuỳ nguồn, MÂU THUẪN), Torch (Eisenhower trong hầm; 650 máy bay đêm 7/8/11/1942), Felix (đặt tên 11/1940, đình chỉ sau 12/1940), TBN phản đối sân bay 1939 ("porción usurpada"), "fait accompli" (Beigbeder) | S103–S123 | Felix = nhạy cảm CAO: chỉ nêu tên kế hoạch + ngày, không biểu tượng |

### 1.3 Không dùng / cần đối chiếu trước G1
- "Henry Ince proposed the tunnels" (S085) · "fifteenth siege" (S007) · câu của Burnet qua trích Sayer (S011) · "Gibraltar changed hands only five times" (chưa đọc Hills 1974) · lấn vịnh "500 m" (S095, một nguồn) · diện tích lấn (không tìm được) · số người Canada đào hầm (234/324, MÂU THUẪN) · bảng Gaceta de Madrid "719" (chưa tải được).
- García Sanz 2022 (sách còn bản quyền, bản archive.org do người dùng tải lên): chỉ để kiểm chứng; trích lên hình phải đối chiếu bản in.
- Bài "Goodbye Frontier" (Gibraltar Chronicle) đã loại (số sai).
- Bị chặn (thử lại ở G1): RAF AHB "Flying from the Rock" (403), visitgibraltar.gi, ministryforheritage.gi (403), publications.parliament.uk (403), web.archive.org (chặn qua proxy), Bộ Quốc phòng TBN (ngắt).

## 2. Tư liệu có quyền (bảng đầy đủ: `vay-ham/tai-san-vay-ham.json`; giấy phép: `licenses/<id>.txt`; ảnh xem trước ≤ 1600 px: `vay-ham/ref/`)
- 39 tài sản mới; **tệp gốc ngoài git** `/var/tmp/cine-out/t3b/a4/raw/` (764 MB), phiên P kiểm lại SHA-256 gốc + xem trước: **39/39 khớp**. Mỗi tệp giấy phép chép **nguyên câu quyền** từ trang gốc đã tải, ngày đọc, dòng ghi công; email đã che.
- Cột "Georef" là **ước tính của gói tư liệu trên ảnh xem trước** (chưa chạy điểm khống chế thật). Luật hình §6.2 gắn vào cột cuối.
- Loại 8 nhóm: Leventhal/Harvard/Mount Vernon (CC BY-NC-SA), bản 1705 trên archive.org gốc Gallica (thu phí thương mại), các bản David Rumsey trên IA (NC), UIC ("copyright not evaluated"), Trumbull của YUAG (chỉ 480 px).
- Tài sản đã có từ TIEN-KY/V5b giữ nguyên: Copernicus DEM, Sentinel-2, PNOA, Rooke (Rijks/YCBA CC0), Met 12828 Trumbull, Met 18113 Eliott, LoC 2016646782, 2025710366, 2020680546, Baedeker 1913. Mới trong phiên này: `licenses/osm-odbl-attribution.txt` (OSMF Attribution Guideline 2021, mục "TV, film, or video productions"), `licenses/catastro-inspire-bu.txt` (chép từ V5b-1).



### 2.1 Độ phủ theo nhu cầu của lệnh
| Nhu cầu | Chính | Dự phòng | Lỗ hổng |
|---|---|---|---|
| Sơ đồ chiến tuyến TBN trên eo đất | **Faden 1783** (Yale 2046612, công sự đến 19/10/1782, ~1:24 700, 14 điểm khống chế); **Drinkwater 1786 plan cuộc xuất kích** (~1:4–5 000, chi tiết eo đất, RMS ước ~35 m) | Faden 1781 (BPL, "trước vây"), Sayer & Bennett 1782 (Yale), Drinkwater 1905, màu nước "Spanish Lines" 1844 (YCBA CC0) | bình đồ quân sự TBN gốc (CGE/AGS) và "Plan of the Spanish Established Lines" 1782 của TNA: chưa số hoá |
| Phố/thành luỹ 1704 | Exact Plan 1704/5 (Rijks CC0); Visscher 1706 (LoC TIFF 238 MB) | Kaart 1704 (Rijks, không nắn được), Marchand 1705 (LoC) | bán phối cảnh → RMS 100–120 m, chỉ khối phố |
| ~1727 | Homann 1733 (Rijks CC0) | Homann 1733 (Yale, phân giải cao hơn); Tirion 1759 | — |
| ~1779–83 | Drinkwater 1786 plan các khẩu đội 13/9/1782 (khối phố, RMS ước ~40 m) | Drinkwater 1905 (1782 + 1905) | — |
| ~1830–60 | Sayer 1865 (~1:30 000, bản quét 2 343 px) | hải đồ New Mole 1873 (1:1 240, từng nhà nhưng chỉ khu cảng nam); ảnh Rijks c.1860 (neutral ground, Landport, Rock từ Fort San Felipe — CC0) | **MỐC YẾU NHẤT**: bình đồ kỹ sư 1:2 500 (Edinburgh/TNA) chưa số hoá → không dựng nhà mốc này |
| ~1900 | Drinkwater 1905 plan (~1:25 000, có rìa "Town of Linea") | Baedeker 1913 (đã nắn, RMS 65 m) | — |
| 1941 | **AMS M981 1943 Gibraltar + La Línea 1:10 000** (từng nhà, lưới toạ độ, RMS ước ~12 m) | plan hầm ONI 1954 (NARA, PD) | bản Princeton có câu "non-commercial" → D8 |
| Tranh PD/CC0 | bản khắc Sharp theo Copley (LoC, TIFF 204 MB) — **chỉ nửa phải**; "Destruction of the Floating Batteries" (Rijks CC0) — crop | phác thảo Copley (Cleveland CC0, Met ×3), quạt vẽ 1782 (Met), Drinkwater views, chân dung Eliott 1784 (Rijks) | sơn dầu Copley (Guildhall) không có ảnh mở; Trumbull bản Cincinnati/Boston không mở |
| Bản khắc pin nổi | Rijks RP-P-OB-19.249; Drinkwater 1786 "view of the grand attack" | Emes 1784 (Rijks) — **không dùng làm Ken Burns** (tiêu điểm người chết đuối) | — |
| Ảnh 1941 | NARA 342-FH 2/10/1943 (C-47 ở North Front ×2, đường biên giới) | — | **không có ảnh PD năm 1941** (thi công, đào hầm, sơ tán) ngoài IWM; LoC 2005677710 (16 ảnh 1942) chưa số hoá → D9 |

### 2.2 Bảng tài sản (39 mục mới)

| ID | Loại · mốc | Tài sản | Nơi giữ · giấy phép (trích ngắn) | px | SHA-256 (gốc, 16 ký tự) | Dùng cho | Georef | Ưu tiên · ghi chú |
|---|---|---|---|---|---|---|---|---|
| yale-2046612-faden-1783 | ban-do · 1779-83 | Plan of the bay, rock and town of Gibraltar ... with the works, batteries, and i (1783-01-26) | Yale University Library, Beinecke (1982 Folio 10) · Public domain work; Yale Open Access Policy — "may be used by anyone f · `licenses/yale-2046612-faden-1783.txt` | 10313×6960 | `598915ea012c9db6` | tuyến vây / bản đồ lịch sử phẳng (toàn vịnh: phòng tuyến TBN, trại San Roque, pháo đài San | có · ~1:24 700 · 14 điểm · RMS ước 90 m · không · 3 h | chính;  |
| bpl-faden-1781 | ban-do · 1779-83 | Plan of the bay, rock and town of Gibraltar, from an actual survey by an officer (1781-01-01) | Boston Public Library, Norman B. Leventhal Map & Education Center · No known copyright restrictions. / No known restrictions on use. · `licenses/bpl-faden-1781.txt` | 9088×6636 | `5d652965da00d699` | tuyến vây / bản đồ lịch sử phẳng (trạng thái đầu vây, chưa có công sự 1782) | có · ~1:24 600 · 13 điểm · RMS ước 90 m · không · 3 h | dự phòng;  |
| ia-drinkwater1786-plan-sortie | ban-do · 1779-83 | A Plan shewing the Attack and Distribution of the Detachment ... which sallied . (1786) | Internet Archive (University of Pittsburgh Library System copy) · Public domain (1786 publication); IA item without use conditions · `licenses/ia-drinkwater1786-plan-sortie.txt` | 3562×2665 | `c747dbc882541f60` | tuyến vây (eo đất chi tiết: Spanish Lines, Fort San Felipe/Santa Bárbara, neutral ground,  | có · ~1:4 000–1:5 000 · 9 điểm · RMS ước 35 m · khối phố · 6 h | chính;  |
| ia-drinkwater1786-plan-batteries | ban-do · 1782-09-13 | A Plan of the Batteries erected before Gibraltar ... with the attack by the batt (1786) | Internet Archive (University of Pittsburgh Library System copy) · Public domain (1786 publication) · `licenses/ia-drinkwater1786-plan-batteries.txt` | 3995×2837 | `476cb89bb9288ce6` | tuyến vây + vị trí 10 tàu-pháo 13/9/1782 / ghost phố (thị trấn có khối phố) | có · ~1:5 000–1:6 000 · 11 điểm · RMS ước 40 m · khối phố · 8 h | chính;  |
| ia-drinkwater1905-plans | ban-do · 1782-09-13 + 1900 | Plan of the Spanish Batteries before Gibraltar 13th September 1782 / Plan of Gib (1905) | Internet Archive (University of California Libraries copy) · Public domain (1905 publication, anonymous map; US pre-1931; UK anonym · `licenses/ia-drinkwater1905-plans.txt` | 2817×2215 | `577bf795a90fea49` | sơ đồ phẳng dễ đọc cho tuyến vây 1782 (đặt tên rõ) + bản đồ 1905 (British Lines, Neutral G | có · 1782: ~1:8 000; 1905: ~1:25 000 · 12 điểm · RMS ước 45 m · khối phố · 4 h | dự phòng;  |
| yale-15487367-sayer-bennett-lines | ban-do · 1779-83 | A plan of the town and fortifications of Gibraltar : with the Spanish lines &c. ("27 Novr." (Yale ghi 1796; nhiều khả năng ấn bản 1781–82)) | Yale University Library, Beinecke (399 1706) · Public domain work; Yale Open Access Policy · `licenses/yale-15487367-sayer-bennett-lines.txt` | 6591×4687 | `36e93b25d13db7a4` | tuyến vây + thị trấn (danh mục 22 khẩu đội A–V) / bản đồ lịch sử phẳng | có · ~1:14 300 · 11 điểm · RMS ước 60 m · khối phố · 6 h | dự phòng;  |
| ia-drinkwater1786-plan-bay | ban-do · 1779-83 | A Plan of the Bay of Gibraltar ... with the encampments (Drinkwater plate) (1786) | Internet Archive (University of Pittsburgh Library System copy) · Public domain (1786 publication) · `licenses/ia-drinkwater1786-plan-bay.txt` | 3336×2423 | `ed1ce3ce48b2559d` | bản đồ lịch sử phẳng (toàn vịnh, trại TBN) | hạn chế · ~1:50 000 · 8 điểm · RMS ước 150 m · không · 1 h | dự phòng;  |
| loc-2008621715-visscher-1706 | ban-do · 1704 | Plan de la ville de Gibraltar / Platte grond der stercke stad Gibralter (with pl (1706) | Library of Congress, Geography and Map Division (G1793 .B4 1709) · LoC G&M: free to use and reuse (no Rights Advisory) · `licenses/loc-2008621715-visscher-1706.txt` | 9619×8244 | `42241a7b055917cf` | bản đồ lịch sử phẳng 1704–05 (tường thành, công sự vây 1704–05 trên eo đất) / ghost phố mứ | hạn chế · ~1:8 000 (thước "Cent Toises"; hình học méo, núi vẽ phối cảnh) · 7 điểm · RMS ước 120 m · khối phố · 8 h | chính;  |
| rijks-rp-p-ob-83400-exact-plan-1705 | ban-do · 1704 | An Exact Plan of the Town, Castle, Moles and Bay of Gibraltar, and the Eenemies  (1705) | Rijksmuseum (RP-P-OB-83.400) · CC0 1.0 (Rijksmuseum) · `licenses/rijks-rp-p-ob-83400-exact-plan-1705.txt` | 5240×3292 | `d7a903a616adb6bd` | bản đồ lịch sử phẳng 1704–05 (công sự tiếp cận của địch, legend A–Z) / ghost phố mức khối | hạn chế · ~1:6 000–1:8 000 (bán phối cảnh) · 7 điểm · RMS ước 100 m · khối phố · 8 h | chính;  |
| rijks-rp-p-ob-83395-kaart-1704 | ban-do · 1704 | De Haven en Straat van Gibraltar (Kaart van Gibraltar, 1704) (1704) | Rijksmuseum (RP-P-OB-83.395) · CC0 1.0 (Rijksmuseum) · `licenses/rijks-rp-p-ob-83395-kaart-1704.txt` | 5452×4508 | `980238cfff811f7d` | bản đồ lịch sử phẳng (hạm đội Anh–Hà Lan trong vịnh 08/1704) | không · vịnh, không thước tin cậy · 0 điểm · RMS ước None m · không · 0 h | dự phòng;  |
| rijks-rp-p-2018-1131-homann-1733 | ban-do · 1727 | Neuester und exacter Plan und Prospect von der Stadt, Vestung, Bay und Fortifica (1733) | Rijksmuseum (RP-P-2018-1131) · CC0 1.0 (Rijksmuseum) · `licenses/rijks-rp-p-2018-1131-homann-1733.txt` | 5460×4576 | `795d4c738849544f` | bản đồ lịch sử phẳng cuộc vây 1727 (đường tiếp cận TBN, plan A thị trấn + plan B toàn bán  | hạn chế · ~1:12 000 (plan B) / lớn hơn (plan A, bán phối cảnh) · 8 điểm · RMS ước 90 m · khối phố · 6 h | chính;  |
| yale-15487374-homann-1733 | ban-do · 1727 | Neuester und exacter Plan und Prospect von der Stadt, Vestung, Bay und Fortifica (1733) | Yale University Library, Beinecke (399AM 1733) · Public domain work; Yale Open Access Policy · `licenses/yale-15487374-homann-1733.txt` | 8539×6523 | `2ff94c35aabc9158` | như Rijks RP-P-2018-1131, bản phân giải cao hơn (8539×6523) | hạn chế · ~1:12 000 · 8 điểm · RMS ước 90 m · khối phố · 6 h | dự phòng;  |
| rijks-rp-p-2018-1774-tirion-1759 | ban-do · 1759 | Nieuwe Aftekening der Stad en Berg van Gibraltar (1759) | Rijksmuseum (RP-P-2018-1774) · CC0 1.0 (Rijksmuseum) · `licenses/rijks-rp-p-2018-1774-tirion-1759.txt` | 4872×2798 | `d955cb4f8228ed1c` | bản đồ lịch sử phẳng giữa hai cuộc vây (trước King's Bastion 1773) | hạn chế · ~1:20 000 (bán phối cảnh) · 6 điểm · RMS ước 120 m · khối phố · 3 h | dự phòng;  |
| ia-sayer1865-plan | ban-do · 1830-60 | Plan of the Rock, Town and Territory of Gibraltar (folding plate in F. Sayer, Th (1865 (ed. 2; ed. 1 1862)) | Internet Archive (University of California Libraries copy) · Public domain (1865 publication); IA possible-copyright-status NOT_IN_ · `licenses/ia-sayer1865-plan.txt` | 2343×1186 | `9e702057500f4521` | bản đồ lịch sử phẳng ~1860 (neutral ground có Gardens/Burying Ground, khối phố thị trấn) | có · ~1:30 000 (thước 5000 ft) · 10 điểm · RMS ước 70 m · khối phố · 4 h | chính;  |
| bpl-ushydro-newmole-1873 | ban-do · 1873 | Mediterranean, New Mole Harbor, Gibraltar (surveyed by HMS Challenger 1873; repu (1873) | Boston Public Library, Leventhal Map & Education Center · No known copyright restrictions. / No known restrictions on use. · `licenses/bpl-ushydro-newmole-1873.txt` | 5201×6502 | `9a7ca0e9d5dfe822` | ghost phố khu New Mole–Rosia (tỷ lệ rất lớn) / mặt nước cảng thế kỷ 19 | có · ~1:1 240 · 6 điểm · RMS ước 10 m · từng nhà · 5 h | dự phòng;  |
| pu-ams-m981-gibraltar-1943 | ban-do · 1941 | Spain 1:10,000. Gibraltar city plan. A.M.S. M981, First Edition (1943) | Princeton University Library (G6671.C1 1943 .A7M3); bản sao Yale 15487373 · No Known Copyright (rightsstatements.org NKC); US federal work (AMS) · `licenses/pu-ams-m981-gibraltar-1943.txt` | 6813×11091 | `252ca705afca56c6` | ghost phố 1941 / đường băng North Front (đường băng 1943 đã kéo ra vịnh) / bản đồ phẳng | có · 1:10 000, có lưới Lambert Iberian zone + kinh vĩ độ · 20 điểm · RMS ước 12 m · từng nhà · 20 h | chính; Princeton ghi "non-commercial … fair-use academic" cho bản quét dù "claims no copyright or license"; tác phẩm gốc PD-USGov → ĐIỀU KIỆN: lên hình dùng bản Yale 15487373 (Yale Open Access "any purpose") — chủ dự án duyệt; bản Princeton dùng làm bằng chứng/nắn. |
| pu-ams-m981-lalinea-1943 | ban-do · 1941 | Spain 1:10,000. La Linea city plan. A.M.S. M981, First Edition (1943) | Princeton University Library (G6564.L22 1943 .A7M3); bản sao Yale 15487290 · No Known Copyright (rightsstatements.org NKC); US federal work (AMS) · `licenses/pu-ams-m981-lalinea-1943.txt` | 6563×6551 | `f4bdb5dfed2797f3` | A3: La Línea + neutral ground 1940s (từng nhà) / ghost phố | có · 1:10 000, lưới quân sự · 14 điểm · RMS ước 12 m · từng nhà · 15 h | chính; Như AMS Gibraltar: ĐIỀU KIỆN — tìm bản Yale/khác trước khi lên hình; dùng làm bằng chứng/nắn. |
| nara-353129601-oni-underground-1954 | ban-do · 1941 | Berthing Diagram, Underground Installation and Base Development Plan - Gibraltar (1954-06) | U.S. National Archives (RG 263, NAID 353129601) · Unrestricted; US federal work (public domain) · `licenses/nara-353129601-oni-underground-1954.txt` | 6537×3880 | `a924bf6219ae5232` | sơ đồ mạng đường hầm (phần lớn đào 1940–44) / North, South, Detached Moles | có · ~1:12 000 (thước feet) · 10 điểm · RMS ước 30 m · không · 2 h | dự phòng;  |
| rijks-rp-f-2001-7-257-16-neutral-ground-1860 | anh · 1830-60 | The neutral ground, from the Rock (album "A history of Gibraltar and its sieges" (c.1860–70) | Rijksmuseum (RP-F-2001-7-257-16) · CC0 1.0 (Rijksmuseum) · `licenses/rijks-rp-f-2001-7-257-16-neutral-ground-1860.txt` | 6546×4138 | `960d1fb7b2b6cc95` | A3 tham chiếu: neutral ground + La Línea sơ khai nhìn từ Rock / tranh Ken Burns | — | chính;  |
| rijks-rp-f-2001-7-257-1-rock-from-san-felipe-1860 | anh · 1830-60 | The rock, from fort San Felipe (c.1860–70) | Rijksmuseum (RP-F-2001-7-257-1) · CC0 1.0 (Rijksmuseum) · `licenses/rijks-rp-f-2001-7-257-1-rock-from-san-felipe-1860.txt` | 6188×4202 | `bb6f4f2cb0d4727a` | A3 tham chiếu: tàn tích Fort San Felipe + Rock / Ken Burns | — | dự phòng;  |
| rijks-rp-f-2001-7-257-14-landport-1860 | anh · 1830-60 | The Landport (c.1860–70) | Rijksmuseum (RP-F-2001-7-257-14) · CC0 1.0 (Rijksmuseum) · `licenses/rijks-rp-f-2001-7-257-14-landport-1860.txt` | 6798×4228 | `f047eb0129bc101b` | tham chiếu kiến trúc cổng Landport cho dựng 3D | — | dự phòng;  |
| ycba-b1975-4-491-hall-spanish-lines-1844 | tranh · 1830-60 | Part of the Bay of Gibraltar, the Spanish Lines (1844) | Yale Center for British Art, Paul Mellon Collection (B1975.4.491) · CC0 / Yale Open Access (public domain) · `licenses/ycba-b1975-4-491-hall-spanish-lines-1844.txt` | 5441×3411 | `fe1ca0994a1916b0` | A3/1830-60: phòng tuyến TBN và vịnh năm 1844 / tranh Ken Burns | — | chính;  |
| ycba-b1975-4-490-hall-kings-bastion-1844 | tranh · 1830-60 | The King's Bastion, the Club House Hotel, Gibraltar (1844) | Yale Center for British Art, Paul Mellon Collection (B1975.4.490) · CC0 / Yale Open Access (public domain) · `licenses/ycba-b1975-4-490-hall-kings-bastion-1844.txt` | 5456×3397 | `327c636b857b5dc0` | tham chiếu King's Bastion giữa thế kỷ 19 / Ken Burns | — | dự phòng;  |
| loc-96510788-sharp-copley-siege | ban-khac · 1782-09-13 | The siege and relief of Gibraltar (c.1810 (plate pub. 1810)) | Library of Congress, Prints & Photographs (PGA - Sharp, W. (D size); LC-DIG-pga-02739) · No known restrictions on publication. · `licenses/loc-96510788-sharp-copley-siege.txt` | 9338×7290 | `d266392ed584c646` | tranh Ken Burns: Copley "The Siege of Gibraltar" (bản khắc toàn cảnh, TIFF 204 MB) | — | chính; LUẬT HÌNH §6.2: góc trái-dưới có người chết đuối → CHỈ crop nửa phải (Eliott, sĩ quan, thành luỹ); bỏ dải chữ đề tặng. |
| cma-1950-215-copley-study | tranh · 1782-09-13 | Study for The Siege of Gibraltar (c.1785–86) | Cleveland Museum of Art (1950.215) · CC0 (Cleveland Museum of Art Open Access) · `licenses/cma-1950-215-copley-study.txt` | 3996×6202 | `fc07ea2295971120` | tranh Ken Burns (phác thảo Copley) | — | dự phòng; Kiểm từng khung Ken Burns: phác thảo nhóm người — chỉ dùng nếu không có cảnh người chết. |
| met-10549 | tranh · 1782-09-13 | Study for "The Siege of Gibraltar": Figures Scaling Floating Battery; Cannon (1785–86) | The Metropolitan Museum of Art (60.44.18) · Public Domain / CC0 (Met Open Access, isPublicDomain=true) · `licenses/met-10549.txt` | 1626×2522 | `bf3edb071bd5bf41` | chèn chi tiết Ken Burns (phác thảo người trên tàu-pháo) | — | dự phòng; Kiểm khung: phác thảo Copley — tránh vùng người ngã/chết đuối. |
| met-10547 | tranh · 1782-09-13 | Study for "The Siege of Gibraltar": The Wrecked Longboat (1785–86) | The Metropolitan Museum of Art (60.44.12 recto) · Public Domain / CC0 (Met Open Access, isPublicDomain=true) · `licenses/met-10547.txt` | 2276×1860 | `c95dad96dd12fbcb` | chèn chi tiết Ken Burns (phác thảo người trên tàu-pháo) | — | dự phòng; Kiểm khung: phác thảo Copley. |
| met-10538 | tranh · 1782-09-13 | Study for "The Siege of Gibraltar": Three Officers, Two Standing and One Kneelin (1785–86) | The Metropolitan Museum of Art (60.44.17 recto) · Public Domain / CC0 (Met Open Access, isPublicDomain=true) · `licenses/met-10538.txt` | 2194×1515 | `cd171143f7f76966` | chèn chi tiết Ken Burns (phác thảo người trên tàu-pháo) | — | dự phòng; Kiểm khung: phác thảo Copley. |
| met-209515-fan-1782 | ban-khac · 1779-83 | Fan with depiction of the siege of Gibraltar by the Spanish (1779–1783) (ca. 1782) | The Metropolitan Museum of Art (24.80.3) · Public Domain / CC0 (Met Open Access) · `licenses/met-209515-fan-1782.txt` | 4000×2771 | `b562381d00624475` | chèn văn hoá đại chúng thời vây (quạt in cảnh vây) / Ken Burns | — | dự phòng;  |
| rijks-rp-p-ob-19249-destruction-floating-batteries | ban-khac · 1782-09-13 | The Destruction of the Floating Batteries before Gibraltar, September the 14th 1 (1783) | Rijksmuseum (RP-P-OB-19.249) · CC0 1.0 / Public Domain Mark (Rijksmuseum) · `licenses/rijks-rp-p-ob-19249-destruction-floating-batteries.txt` | 6344×5002 | `3fb24fc6210b9c80` | tranh Ken Burns: tàu-pháo cháy 13–14/9/1782 | — | chính; LUẬT HÌNH §6.2: crop phần pin nổi cháy + thành luỹ, bỏ xuồng có người cận cảnh và dải chữ "Glorious Transaction" (giọng tôn vinh). |
| rijks-rp-p-ob-70560-emes-scene-14sep1782 | ban-khac · 1782-09-13 | The Scene before Gibraltar on the morning of the 14th of September 1782 (1786–89) | Rijksmuseum (RP-P-OB-70.560) · CC0 1.0 (Rijksmuseum) · `licenses/rijks-rp-p-ob-70560-emes-scene-14sep1782.txt` | 7480×5648 | `8ecb5063e01d75b1` | tranh Ken Burns: sáng 14/9, xác tàu-pháo, cứu người (Curtis) | — | chính; LUẬT HÌNH §6.2: tiêu điểm là người chết đuối/được vớt → KHÔNG dùng làm Ken Burns; chỉ tham chiếu dáng pin nổi cho dựng 3D. |
| rijks-rp-p-1960-424-beleg-1779-82 | ban-khac · 1779-83 | Beleg van Gibraltar, 1779-1782 (c.1780–83) | Rijksmuseum (RP-P-1960-424) · CC0 1.0 / Public Domain Mark (Rijksmuseum) · `licenses/rijks-rp-p-1960-424-beleg-1779-82.txt` | 4322×3784 | `d71e6514955e76d7` | tranh Ken Burns (pháo kích từ tàu) | — | dự phòng;  |
| ia-drinkwater1786-view-grand-attack | ban-khac · 1782-09-13 | A View of the Grand Attack upon Gibraltar September 13th 1782 (Drinkwater plate) (1786) | Internet Archive (University of Pittsburgh Library System copy) · Public domain (1786 publication) · `licenses/ia-drinkwater1786-view-grand-attack.txt` | 4125×2096 | `1873cf0838088e31` | tranh Ken Burns toàn cảnh (nhìn từ Rock xuống vịnh, tàu-pháo trước King's Bastion) | — | dự phòng;  |
| ia-drinkwater1786-view-spanish-batteries | ban-khac · 1779-83 | A View from Gibraltar of the Spanish Batteries erected in the late Siege before  (1786) | Internet Archive (University of Pittsburgh Library System copy) · Public domain (1786 publication) · `licenses/ia-drinkwater1786-view-spanish-batteries.txt` | 4000×2007 | `bb057d4f780f512c` | tham chiếu dựng 3D phòng tuyến TBN nhìn từ Rock / Ken Burns | — | dự phòng;  |
| loc-2016646790-marchand-1705 | ban-khac · 1704 | Das im vorig- und jetzigem Jahr ... gewaltig bestürmte ... Gibraltar 1705 d. 2 A (1705) | Library of Congress, Prints & Photographs (LOT 14117, no. 182; LC-USZ62-67236) · No known restrictions on publication. · `licenses/loc-2016646790-marchand-1705.txt` | 1536×1179 | `6745670357f06026` | minh hoạ cuộc vây 1704–05 (chỉ minh hoạ) | không · phối cảnh · 0 điểm · RMS ước None m · không · 0 h | dự phòng;  |
| nara-204918833 | anh · 1941 | A Douglas C-47 transport plane is unloaded at Gibraltar Airfield. Note the Rock  (1943-10-02) | U.S. National Archives (342-FH, NAID 204918833) · Unrestricted; US federal work (public domain) · `licenses/nara-204918833.txt` | 4532×3532 | `c3b81b1904a4fbbf` | ảnh lưu trữ 1941–43: sân bay North Front + Rock (C-47) — gần nhất với đường băng thời chiế | — | chính;  |
| nara-204918836 | anh · 1941 | With the Rock of Gibraltar as a background, a Douglas C-47, "Superman" transport (1943-10-02) | U.S. National Archives (342-FH, NAID 204918836) · Unrestricted; US federal work (public domain) · `licenses/nara-204918836.txt` | 4512×3516 | `f5812d275dd70f5f` | ảnh lưu trữ 1941–43: sân bay North Front + Rock | — | dự phòng;  |
| nara-204918839 | anh · 1941 | View of the international boundary line between Gibraltar and Spain. 2 October 1 (1943-10-02) | U.S. National Archives (342-FH, NAID 204918839) · Unrestricted; US federal work (public domain) · `licenses/nara-204918839.txt` | 4504×3502 | `cc2ab128a513301c` | ảnh lưu trữ 1941–43: biên giới/neutral ground 1943 (hàng rào, cổng) | — | chính;  |
| rijks-rp-p-ob-53323-eliott-1784 | ban-khac · 1779-83 | Portret van generaal George Eliott met Zeeslag bij Gibraltar (1784) | Rijksmuseum (RP-P-OB-53.323) · CC0 1.0 / Public Domain Mark (Rijksmuseum) · `licenses/rijks-rp-p-ob-53323-eliott-1784.txt` | 2820×3634 | `28d85492a11e771e` | chân dung Eliott (bổ sung cho Met 18113) | — | dự phòng;  |


## 3. Dữ liệu "thành phố có nhà" theo mốc (VV2 / NC-H1 — sửa lỗi T2)

### 3.1 Đo OSM hôm nay (API `/map`, 4 ô, đọc 17/10/2026; tệp thô ngoài git, SHA trong `vay-ham/osm-do.json`)
| Vùng | Diện tích | Số toà | Phủ mái | Có `building:levels` | Có `height` | Có `start_date` | Diện tích mái trung vị |
|---|---|---|---|---|---|---|---|
| Phố cổ trong tường (−5,356…−5,347; 36,1335…36,1455) | 1,07 km² | 706 | 26,2 % | **8** | 0 | 6 | 173 m² |
| Lõi mở rộng (−5,360…−5,345; 36,125…36,150) | 3,73 km² | 1 419 | 17,7 % | 74 | 2 | 9 | 206 m² |
- **Hệ quả:** OSM cho **mặt bằng** đủ (khớp số V5b-1: 2 451 toà toàn Gibraltar), **không cho chiều cao** (≤ 5 % có tầng) và **không có năm xây**. Chiều cao: ước từ DSM như V5b-1 (thô) hoặc từ số tầng đếm trên ảnh LoC/Rijks + AMS 1943 cho dãy mặt tiền nhìn thấy trong khung. Không có năm xây → Gibraltar ở **tầng CHUẨN theo mốc** (không nội suy), như V5b-1.
- **Giấy phép + ghi công** (`licenses/osm-odbl-attribution.txt`, OSMF Attribution Guideline 2021): phim là "Produced Work" → không phải phát hành theo ODbL; OSM là thành phần chính của hình → ghi **ở góc khung** đủ lâu để đọc khi cảnh OSM xuất hiện lần đầu **và** ở màn kết/mô tả kèm `https://www.openstreetmap.org/copyright`. Chữ: "Map data from OpenStreetMap (ODbL)" ≥ 38 px. Dữ liệu dẫn xuất (OSM + ghost) không phát hành.
- **La Línea:** Catastro INSPIRE BU 11022 — tầng ĐẦY ĐỦ (11 141 toà / 26 087 phần toà, năm 1849–2025, số tầng) đã nạp ở gib20; ghi "Source: Dirección General del Catastro". Toà đã phá trước nay không có trong Catastro → mốc 1943 lấy thêm từ AMS La Línea (tuỳ chọn).

### 3.2 Bảng theo mốc
| Mốc | Phía Gibraltar: nguồn dựng nhà + phố | Mức | Điểm khống chế / RMS (ước) | Phía La Línea | Shot 3D phố dùng | Không có dữ liệu → đổi sang |
|---|---|---|---|---|---|---|
| 2026 | OSM footprint + đường; chiều cao ước | từng nhà | — (toạ độ thật) | Catastro (đầy đủ) | 0a, 0e (pha 2026), 5c, 5h, 5k | — |
| 1969–85 | OSM trừ đất lấn sau 1987 (Landsat) — chưa có năm xây | khối (tầng chuẩn) | — | Catastro lọc năm ≤ mốc | 5a | — |
| 1941–43 | **AMS M981 1943 1:10 000** (từng nhà, lưới km + kinh vĩ độ) | từng nhà | ≥ 20 điểm (≥ 12 giao điểm lưới) / **~12 m** | AMS La Línea 1943 + Catastro ≤ 1943 | 0e (pha 1943), 4b (gib20), 4c, 4i | — |
| ~1900–13 | Drinkwater 1905 plan + Baedeker 1913 (đã nắn, RMS 65 m) + ảnh LoC | khối (khu) | 12 / ~45 m; Baedeker 8 / 65 m | Catastro ≤ 1910 + lõi c.1900 (gib20) | 3f | — |
| ~1830–60 | Sayer 1865 (~1:30 000) | khu (không đủ nhà) | 10 / ~70 m | Catastro ≤ 1860 (ít) | **không** | **3c = bản đồ lịch sử phẳng có nhãn**; 3d nhìn phía La Línea (Catastro) |
| 1810 | không có bình đồ riêng | — | — | — | **không** (3b là 3D vùng, không nói phố; phố Gibraltar ở xa dùng ghost 1782) | — |
| 1779–83 | **Drinkwater 1786 plan các khẩu đội 13/9/1782** + Faden 1783; plan cuộc xuất kích cho eo đất | khối phố | 11 / ~40 m; sortie 9 / ~35 m | (chưa có La Línea) chiến tuyến từ Faden/Drinkwater | 0e (pha 1782), 2g, 2j, 2m | nếu số hoá trễ: 2g → Drinkwater 1786 phẳng |
| ~1727–35 | Homann 1733 | khối phố | 8 / ~90 m | Línea de Contravalación (Homann, Faden) | không (1j, 1k là 3D vùng) | — |
| 1704 | Exact Plan 1705 + Visscher 1706 (bán phối cảnh) | khối phố | 7 / ~100–120 m | — | 0e (pha 1704), 1d, 1e | nếu không đạt RMS ≤ 120 m sau nắn: 1d → bản đồ lịch sử phẳng (Exact Plan) |

### 3.3 Ước công số hoá (giờ người, lõi ≤ 1–2 km²)
| Việc | Mốc | Giờ (ước) | Ghi chú |
|---|---|---|---|
| Nắn + kiểm điểm khống chế (mỗi bản) | 1704, 1782 (×2 bản), 1943 | 4 × 1–1,5 = **4–6 h** | ghi sổ điểm, RMS thật thay số ước |
| Vẽ khối phố 1704 (≈ 120–150 khối trong tường) | 1704 | **8 h** | khối ghost ≤ 12 m, nhãn "reconstructed from Exact Plan 1705" |
| Vẽ khối phố 1782 + chiến tuyến TBN | 1782 | **8 h + 6 h** | phố từ plan các khẩu đội; chiến tuyến/pháo đài từ plan cuộc xuất kích |
| Vẽ từng nhà 1943 (phố cổ ≈ 700 toà) | 1943 | **~20 h** (hoặc **~10 h** mức khối) | dùng OSM làm nền, chỉ sửa toà khác 1943 (đối chiếu chồng) → có thể nhanh hơn |
| **Tổng 3 mốc bắt buộc** | | **≈ 37–47 h** | NC-LS §5.2 M10 ước 20–40 h/tập → sát/vượt trần trên nếu làm 1943 từng nhà; đề xuất 1943 mức khối + sửa theo OSM (D5) |
| Tuỳ chọn: 1727 (Homann), 1900 (Drinkwater 1905) | | +6 h, +4 h | chỉ khi thêm shot 3D phố mốc này |

### 3.4 Shot KHÔNG có dữ liệu nhà → đã đổi sang bản đồ lịch sử phẳng có nhãn
- **3c** (eo đất 1830–60): Sayer 1865 phẳng, nhãn "Neutral Ground".
- **1c** (1705), **2b** (Faden 1783), **2k** (13/9/1782), **4f** (AMS 1943): bản đồ phẳng là hồ sơ thật, đặt trước/sau shot 3D cùng mốc.
- Shot 3D ở mốc **1727 (1j), 1730–35 (1k), 1810 (3b)** là **3D vùng** nhìn eo đất/chiến tuyến, lời không nói về phố → NC-H1 không áp; phố Gibraltar ở xa dùng ghost mốc gần nhất có nguồn, nhãn ghi mốc nguồn.

## 4. Treatment theo shot (KHÔNG viết lời) — `vay-ham/treatment.json` (máy đọc), `vay-ham/treatment-rows.txt` (nguồn), `vay-ham/tu_kiem.py`

### 4.1 Quy ước
- **Loại cảnh:** 3D phố (máy ≤ 3 km, nơi có tên) · 3D vùng (eo đất/vịnh/eo biển) · bản đồ lịch sử (phẳng, có nhãn) · tranh Ken Burns · ảnh (ảnh/văn bản lưu trữ, ≤ 8 s/lần) · footage · thẻ số.
- **AGL ước** = độ cao máy đại diện (max trong ngoặc). **Vai** máy theo ngữ pháp V5b-2a: co-che / buoc-ngoat / he-qua. Thời lượng là **ước theo treatment**; chốt ở G1 theo lời thật (shot 3D/bản đồ/tranh đã giãn ×1,25 so nhịp hình để vừa 9–11 phút; thẻ/ảnh giữ ≤ 8 s).
- Mỗi chương: **câu hỏi → trở ngại → bước ngoặt → hệ quả** (dòng in nghiêng). Claim S… ở `claims-vay-ham.md`; C… ở `tienky/claims.json`.
- Nhân vật (Kinh thánh §3): Rooke + Hesse-Darmstadt (ch.1), Eliott ↔ Álvarez de Sotomayor/Crillon + d'Arçon (ch.2), "người đào hầm của Ince" (nhóm, ch.2), kỹ sư/đội đào hầm 1940 (nhóm, ch.4), người lao động qua biên giới (nhóm A-lite, ch.5) — giữ từ TIEN-KY §4.3.

### 4.2 Bảng shot

#### Móc — Midnight at the Gate — 43.5 s

| Shot | t0 (s) | Dài (s) | Loại cảnh | Vùng · góc | Mốc | AGL ước (km) | Vai | Máy / nội dung hình | Dữ liệu nhà | Claim | Máy dựng |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0a | 0.0 | 5.5 | 3D phố | cong-bien-gioi · mat-dat-nhin-nam | 2026 | 0.003 (max 0.03) | co-che | follow A-lite đi bộ băng qua đường băng, máy cao 3 m — Nửa đêm 2026: người đi bộ băng qua đường băng về phía Rock; chip nơi "Gibraltar–La Línea frontier" | OSM 2026 + Catastro (La Línea) | C33, C02, C26 | M9 |
| 0b | 5.5 | 6.0 | 3D vùng | eo-dat · crane-len-tu-nam | 2026 | 0.6 (max 2.5) | co-che | crane up từ cổng → eo đất, đường băng, vách bắc — Một đường băng nằm ngang giữa hai thành phố; vách bắc Rock đứng sau | OSM + Catastro | C20, C33, S094 | — |
| 0c | 11.5 | 3.0 | 3D vùng | eo-bien · dinh-vi-cao | 2026 | 90.0 (max 95.0) | co-che | zoom nhiều tầng: chạm 90 km 2,5 s rồi lặn lại (lần DUY NHẤT > 50 km) — Định vị: cửa Địa Trung Hải, hai lục địa — "the key of the Mediterranean" theo cả nguồn Anh lẫn TBN | — | S009, S010 | M12 |
| 0d | 14.5 | 5.0 | thẻ số | the · the | 1309–1783 | 0.0 (max 0.0) | co-che | thẻ số trên nền mờ Rock — "14 sieges, 1309–1783" — "historians count"; nguồn ngắn: Sayer 1862 · Gibraltar National Museum | — | S001, S004, S006 | — |
| 0e | 19.5 | 8.0 | 3D phố | pho-co · push-in-tu-vinh | 2026→1704 | 0.35 (max 0.6) | co-che | push-in từ vịnh vào phố; cắt nhảy năm 2026 / 1943 / 1782 / 1704, mỗi mốc ≥ 1,5 s có nhãn năm + nhãn nguồn ghost — "Tua ngược": phố đổi qua 4 mốc có nguồn | OSM 2026 → ghost 1943 (AMS M981) → ghost 1782 (bình đồ c.1779–83) → ghost 1704 | S012, S062, S092 | M9,M12 |
| 0f | 27.5 | 4.0 | tranh Ken Burns | tranh-1782 · kb | 1782 | 0.0 (max 0.0) | buoc-ngoat | Ken Burns bản khắc Sharp theo Copley (LoC 96510788) — CHỈ crop nửa phải (thành luỹ, khói), §6.2 — Nháy hứa: pin nổi trước thành luỹ | — | S065, S074 | M8 |
| 0g | 31.5 | 5.0 | 3D phố | giao-lo-1941 · orbit | 1941 | 0.04 (max 0.1) | buoc-ngoat | orbit ngắn quanh giao lộ (hero gib20) — Nháy hứa 1941: đường băng cắt ngang con đường sang Tây Ban Nha | OSM + Catastro + Baedeker 1913 | C33, S091 | — |
| 0h | 36.5 | 7.0 | 3D vùng | vach-bac · nhin-tu-bac-thap | 2026 | 0.25 (max 0.4) | co-che | push-in giữ hơi lên vách bắc lúc bình minh — Câu hỏi trùng tiêu đề; hứa cú lật: "the last siege of the Rock is being fought with paperwork — and payrolls" | — | S001, S009, C20 | M6 |

#### Ch.1 — 1704: A Rock Changes Hands — 101.5 s

*Hỏi: vì sao một hạm đội muốn một tảng đá? → Trở ngại: tường + vách, vài trăm người giữ → Bước ngoặt: đầu hàng 4/8/1704 (N.S.) → Hệ quả: dân rời sang San Roque; Utrecht 1713 "không giao thông đường bộ"; TBN thử lại 1704–05, 1727, rồi dựng chiến tuyến 1730–35*

| Shot | t0 (s) | Dài (s) | Loại cảnh | Vùng · góc | Mốc | AGL ước (km) | Vai | Máy / nội dung hình | Dữ liệu nhà | Claim | Máy dựng |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1a | 43.5 | 11.0 | 3D vùng | vinh · tu-tay-cao | 1704 | 12.0 (max 25.0) | co-che | lateral theo hạm đội Anh–Hà Lan vào vịnh (M3); bộ đếm ngày hai lịch — Câu hỏi chương: vì sao một hạm đội muốn một tảng đá? Bộ đếm "21 July (O.S.) / 1 Aug (N.S.) 1704" | — | S012, S013 | M3,M6 |
| 1b | 54.5 | 6.0 | tranh Ken Burns | chan-dung · kb | 1704 | 0.0 (max 0.0) | co-che | chân dung cắt nền Rooke (Rijksmuseum CC0) — Nhân vật: Rooke + Hesse-Darmstadt — nhân danh ứng viên Habsburg (hai nguồn) | — | S012, S017 | M8 |
| 1c | 60.5 | 9.0 | bản đồ lịch sử | bd-1705 · phang | 1705 | 0.0 (max 0.0) | co-che | "Exact Plan 1704/5" (Rijksmuseum RP-P-OB-83.400, CC0) phẳng có nhãn; dự phòng Visscher 1706 (LoC 2008621715) — Trở ngại: tường + vách; phố trong tường theo bản in 1705 | — | S012, S014 | M12 |
| 1d | 69.5 | 12.5 | 3D phố | pho-co · tu-vinh-thap | 1704 | 0.3 (max 0.5) | co-che | push-in giữ hơi từ vịnh vào Old Mole — Phố 1704 ghost có nhãn nguồn; "a few hundred defenders" (hai nguồn) | ghost 1704 — khối phố từ Exact Plan 1705 + Visscher 1706 (nắn hạn chế, RMS ước 100–120 m → chỉ mức khối phố); dự phòng ghost gib20 356 khối | S014, S015, S016 | M9,M12 |
| 1e | 82.0 | 9.0 | 3D phố | old-mole · orbit | 1704 | 0.15 (max 0.3) | buoc-ngoat | orbit Old Mole; khói 2D xa (không người); MỐC ĐINH ngày đầu hàng **MỐC ĐINH** — MỐC ĐINH 4/8/1704 (N.S.) = 24/7 (O.S.): đầu hàng — nhãn phụ giải thích hai lịch | ghost 1704 | S013, S016 | M7,M6 |
| 1f | 91.0 | 6.0 | thẻ số | the · the | 1704 | 0.0 (max 0.0) | co-che | thẻ hai cột: phòng thủ (Sayer ≤ 500 / Montero ~100 lính) — chấm trung tính — Số hai phía, ghi "British account" / "Spanish account" | — | S014, S015 | — |
| 1g | 97.0 | 10.0 | 3D vùng | eo-dat · top-down-rise | 1704 | 1.2 (max 2.0) | he-qua | top-down; mũi tên trắng nét đứt phố → San Roque (M1) — Hệ quả: gần hết dân rời lên bắc, lập San Roque | ghost 1704 | S018, S019 | M1 |
| 1h | 107.0 | 8.0 | ảnh | van-ban-utrecht · ho-so | 1713 | 0.0 (max 0.0) | he-qua | trang Điều X (Jenkinson 1785, archive.org, PD) tô dòng — 2 nửa ≤ 4,5 s mỗi nửa — Hồ sơ thật: "without any territorial jurisdiction…without any open communication by land" | — | S022, S023, S025 | — |
| 1i | 115.0 | 10.0 | 3D vùng | eo-dat · tu-dong-bac | 1713 | 0.8 (max 1.5) | he-qua | boundary trace dọc tường bắc — không vẽ biên giới trên eo đất — Hai cách hiểu cùng một câu: TBN (S030) ↔ Anh (S031) | ghost 1704–1713 | S023, S030, S031 | M12 |
| 1j | 125.0 | 11.0 | 3D vùng | eo-dat · lateral-tay | 1704→1727 | 1.5 (max 3.0) | he-qua | lateral; năm nhảy 1704–05 → 1727; hai tuyến tấn công dạng dải — Tây Ban Nha thử lại hai lần (1704–05, 1727) — cuộc vây thứ 12 và 13 theo bảo tàng | ghost 1727 — Homann 1733 (Rijks CC0, RMS ước ~60–90 m, khối phố) | S021, S004 | M4,M6 |
| 1k | 136.0 | 9.0 | 3D vùng | eo-dat · tu-bac-cao | 1730→1735 | 2.0 (max 3.0) | he-qua | crane chậm; Línea de Contravalación mọc 1730→1735 (M4) — Hệ quả: TBN dựng một chiến tuyến cố định ngoài tầm pháo — tên "La Línea" bắt đầu từ đây | — | S032 | M4,M6 |

#### Ch.2 — The Great Siege (1779–83) — 168.5 s

*Hỏi: làm sao bỏ đói một tảng đá? → Trở ngại: phong toả bộ + biển, đói, scorbut → Bước ngoặt: phố cháy 12/4/1781; đạn đỏ + 13/9/1782; đường hầm 1782 → Hệ quả: 10 pin nổi mất, vây kết thúc 2/1783, hiệp ước 1783 giữ nguyên hiện trạng*

| Shot | t0 (s) | Dài (s) | Loại cảnh | Vùng · góc | Mốc | AGL ước (km) | Vai | Máy / nội dung hình | Dữ liệu nhà | Claim | Máy dựng |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2a | 145.0 | 11.0 | 3D vùng | eo-dat · tu-bac-thap-2 | 1779 | 0.8 (max 1.5) | co-che | lateral chậm dọc chiến tuyến TBN 6/1779; bộ đếm ngày (M6) — Câu hỏi chương: làm sao bỏ đói một tảng đá? Cổng đóng 21/6/1779 | ghost 1782 (Drinkwater 1786 + Faden 1783) | S040, S042, S044 | M4,M6 |
| 2b | 156.0 | 9.0 | bản đồ lịch sử | bd-faden-1781 · phang | 1769–75/1781 | 0.0 (max 0.0) | co-che | Faden 1783 (Yale 2046612: công sự TBN đến 19/10/1782) phẳng có nhãn Fort St Philip/St Barbara, San Roque; dự phòng Faden 1781 (BPL) — Hồ sơ thật: vịnh, chiến tuyến, hai thành phố đối diện | — | S040, S042 | M12 |
| 2c | 165.0 | 10.0 | 3D vùng | vinh · tu-nam-cao | 1779–80 | 8.0 (max 15.0) | co-che | hạm đội phong toả (M3 rút gọn) quanh vịnh — Phong toả biển từ 16/7/1779; quân bộ ~14 000 (10/1779) | — | S042, S048 | M3 |
| 2d | 175.0 | 7.0 | thẻ số | the · the | 1/1780 | 0.0 (max 0.0) | co-che | thẻ hậu cần: giá trứng/thực phẩm 1/1780 + 5 382 người trong đồn — Trở ngại: đói — "thistles, dandelion and wild leeks" | — | S052, S078 | — |
| 2e | 182.0 | 6.0 | tranh Ken Burns | chan-dung · kb2 | 1779 | 0.0 (max 0.0) | co-che | chân dung Eliott (The Met 18113, CC0) cắt nền — Nhân vật: thống đốc giữ thành | — | S040 | M8 |
| 2f | 188.0 | 11.0 | 3D vùng | eo-bien · tu-tay-rat-cao | 1780–82 | 30.0 (max 45.0) | co-che | mũi tên đoàn tiếp tế (M1) từ tây: 1/1780, 4/1781, 10/1782; chanh Malaga (tàu Đan Mạch) — Ba đoàn tiếp tế; scorbut được chữa bằng chanh — hậu cần khán giả hỏi | — | S054, S055, S056, S053 | M1,M3,M6 |
| 2g | 199.0 | 12.5 | 3D phố | pho-co · tu-tay-thap | 1781 | 0.25 (max 0.4) | buoc-ngoat | push-in; phố đổi vật liệu "cháy → ghost tro" (M7), không người; mũi tên dân về nam **MỐC ĐINH** — MỐC ĐINH 12/4/1781 10:45: đoàn Darby thả neo, pháo TBN bắn vào phố | ghost 1782 — khối phố từ Drinkwater 1786 plan of batteries (RMS ước ~40 m) + Faden 1783 | S062, S063 | M7,M9,M6 |
| 2h | 211.5 | 6.0 | ảnh | ban-khac-pho · ho-so | 1781–82 | 0.0 (max 0.0) | he-qua | bản khắc Drinkwater 1786 "view of the Spanish batteries" / Rijks RP-P-1960-424 (CC0) — không cảnh người — Hồ sơ thật: phố sau bắn phá (không cảnh cướp bóc có người) | — | S062, S064 | — |
| 2i | 217.5 | 7.0 | thẻ số | the · the | 1779–83 | 0.0 (max 0.0) | co-che | thẻ: 205 328 vs 258 387 phát; ~8 000 thùng thuốc súng — Hậu cần đạn dược hai phía (Drinkwater ↔ Montero) | — | S051 | — |
| 2j | 224.5 | 11.0 | 3D phố | king-bastion · orbit | 1782 | 0.08 (max 0.15) | co-che | orbit King's Bastion; lò nung đạn đỏ (sticker vật 3D, ánh đỏ ấm) — Cơ chế: đạn nung đỏ (thử 9/1779; dùng hàng loạt 8/9/1782) | ghost 1779–83 + OSM footprint bastion | S058, S059, S061 | M5(rút gọn),M6 |
| 2k | 235.5 | 10.0 | bản đồ lịch sử | bd-13-9-1782 · phang | 1782 | 0.0 (max 0.0) | co-che | Drinkwater 1786 "plan of the batteries 13 Sept 1782" (archive.org, PD) phẳng có nhãn 10 pin nổi — Hồ sơ thật: thế trận — 47 tàu chiến tuyến, 33 000–40 000 quân (hai nguồn) | — | S065, S068 | M12 |
| 2l | 245.5 | 7.5 | tranh Ken Burns | tranh-1782 · kb3 | 1782 | 0.0 (max 0.0) | co-che | Rijks RP-P-OB-19.249 "Destruction of the Floating Batteries" (CC0) — crop pin nổi + thành luỹ, bỏ xuồng người cận và dải chữ — d'Arçon và pin nổi; ông đã xin thử với đạn đỏ trước (nguồn Pháp) | — | S050, S073 | M8 |
| 2m | 253.0 | 20.0 | 3D vùng | vinh · lien-hoan-1782 | 1782-09-13 | 0.1 (max 1.4) | buoc-ngoat | CÚ LIÊN HOÀN #2: bay thấp 100 m dọc mặt vịnh từ Algeciras → ramp → orbit King's Bastion, NĂM/GIỜ DỪNG 13/9/1782 09:45 → crane → reveal hàng 10 pin nổi + khói (M7), mặt trời đúng giờ (M6); không người **MỐC ĐINH** **[lien-hoan-2-vinh-1782]** — MỐC ĐINH 13/9/1782: 09:30 vào vị trí → 09:45 Anh khai hoả → 10:25 toàn tuyến Pháp–TBN (ba nguồn) | ghost 1782 (Drinkwater 1786 + Faden 1783) | S066, S067, S075 | M3,M6,M7 |
| 2n | 273.0 | 7.0 | thẻ số | the · the | 1782 | 0.0 (max 0.0) | he-qua | thẻ: 10 → 0 pin nổi; thương vong hai phía bằng số + chấm trung tính; 357 được cứu — Hệ quả bằng số, ghi rõ ai đếm | — | S069, S070, S071, S074 | — |
| 2o | 280.0 | 12.5 | 3D phố | vach-bac · mat-cat | 1782 | 0.12 (max 0.2) | buoc-ngoat | mặt cắt vách bắc (M11): đường hầm đào theo ngày từ 25/5/1782, lỗ châu mai 15/7 — Cơ chế mới: 13 người, 82 ft trong 5 tuần; 140 ft (5/8/1782) | — | S080, S081, S082, S083 | M11,M6 |
| 2p | 292.5 | 5.0 | footage | ham-hom-nay · footage | 2026 | 0.0 (max 0.0) | he-qua | footage trong đường hầm hôm nay (CHỈ khi có clip giấy phép rõ; nếu không → ảnh/3D) — Then/now: lỗ châu mai vẫn còn | — | S084 | — |
| 2q | 297.5 | 10.0 | 3D vùng | eo-dat · tu-nam-cao | 1783 | 2.5 (max 4.0) | he-qua | reveal kéo lùi; tuyến vây mờ dần theo ngày 2/1783 — Kết vây: phát súng cuối 5/2/1783 | ghost 1783 | S045, S046, S037 | M4,M6 |
| 2r | 307.5 | 6.0 | ảnh | van-ban-1783 · ho-so | 1783 | 0.0 (max 0.0) | he-qua | văn bản/ấn bản hiệp ước 1783 (PD) tô dòng + thẻ tổn thất cả cuộc vây hai phía — Hiệp ước 1783: TBN lấy Minorca + Florida, Gibraltar giữ nguyên | — | S038, S076, S077 | — |

#### Ch.3 — The Neutral Ground (1730–1938) — 70.5 s

*Hỏi: Rock kết thúc ở đâu? → Trở ngại: hiệp ước không nói về eo đất → Bước ngoặt: 1810 chiến tuyến bị phá; 1909 hàng rào → Hệ quả: La Línea mọc; khoảng giữa thành trại, vườn, trường đua, dải cỏ 1934–36*

| Shot | t0 (s) | Dài (s) | Loại cảnh | Vùng · góc | Mốc | AGL ước (km) | Vai | Máy / nội dung hình | Dữ liệu nhà | Claim | Máy dựng |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3a | 313.5 | 10.0 | 3D vùng | eo-dat · tu-tay-thap | 1783–1810 | 0.6 (max 1.0) | co-che | lateral dọc chiến tuyến; dải giữa tô trung tính "neutral ground (as maps call it)" — Câu hỏi: Rock kết thúc ở đâu? | ghost (bình đồ 1779–83 + 1830–60) | S032, S035 | M4 |
| 3b | 323.5 | 9.0 | 3D vùng | eo-dat · orbit-cao | 1810 | 0.9 (max 1.5) | buoc-ngoat | orbit; hai pháo đài bốc khói (M7) — MỐC ĐINH 1810 **MỐC ĐINH** — MỐC ĐINH 1810: Anh phá chiến tuyến, TBN đồng ý (Montero ghi 1811) | ghost 1810 | S034 | M7,M6 |
| 3c | 332.5 | 9.0 | bản đồ lịch sử | bd-eo-dat-tk19 · phang | 1830–73 | 0.0 (max 0.0) | co-che | Sayer 1865 plan (archive.org, PD) phẳng có nhãn "Neutral Ground"; ảnh Rijks 1860 làm chèn — Hồ sơ thật: "Neutral Ground" trên bản đồ đương thời | — | S035 | M12 |
| 3d | 341.5 | 12.5 | 3D phố | la-linea · lateral | 1849→1910 | 0.11 (max 0.2) | he-qua | lateral parallax trước La Línea: toà Catastro mọc đúng năm — La Línea mọc sau chiến tuyến; tách khỏi San Roque 1870 | Catastro BU 11022 (tầng ĐẦY ĐỦ) | S033 | M9 |
| 3e | 354.0 | 5.0 | ảnh | anh-neutral-ground · ho-so | 1900–10 | 0.0 (max 0.0) | he-qua | ảnh Rijks RP-F-2001-7-257-16 "neutral ground" c.1860 (CC0) neo điểm 3D; dự phòng LoC 2025710366 (1900–10) — Hồ sơ thật: khoảng giữa c.1900 | — | S035, S088 | — |
| 3f | 359.0 | 11.0 | 3D phố | north-front · tu-bac-thap | 1900→1910 | 0.1 (max 0.2) | buoc-ngoat | push-in giữ hơi; hàng rào 1909 mọc (MỐC ĐINH) **MỐC ĐINH** — MỐC ĐINH 1909: hàng rào Anh (báo TBN 8/1908) — TBN không công nhận là biên giới | Baedeker 1913 (đã nắn) + OSM + Catastro | S036, S030 | M12,M6 |
| 3g | 370.0 | 5.0 | ảnh | anh-north-town · ho-so | 1905 | 0.0 (max 0.0) | he-qua | ảnh LoC 2020680546 North Town (≤ 8 s) — Hồ sơ thật: phố bắc đầu thế kỷ 20 | — | S088 | — |
| 3h | 375.0 | 9.0 | 3D vùng | eo-dat · top-down | 1909→1938 | 1.5 (max 2.0) | he-qua | top-down: trại lính, vườn, trường đua, dải cỏ 1934–36 hiện theo năm — Eo đất trước chiến tranh: trường đua thành dải cỏ hạ cánh (£573) | Baedeker 1913 + AMS 1943 | S088, S089, S090 | M12,M6 |

#### Ch.4 — A Runway on the Isthmus (1939–45) — 79.0 s

*Hỏi: vì sao xây sân bay trên đất tranh chấp? → Trở ngại: Rock không có đất bằng; TBN phản đối 1939 → Bước ngoặt: 1941 nối đường băng ra biển bằng đá đào hầm → Hệ quả: căn cứ Torch, dân sơ tán, đường băng cắt đường sang TBN tới nay*

| Shot | t0 (s) | Dài (s) | Loại cảnh | Vùng · góc | Mốc | AGL ước (km) | Vai | Máy / nội dung hình | Dữ liệu nhà | Claim | Máy dựng |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 4a | 384.0 | 5.0 | ảnh | anh-1941 · ho-so | 1941 | 0.0 (max 0.0) | co-che | ảnh NARA 342-FH 204918833 (2/10/1943, C-47 ở North Front, PD) — nhãn đúng năm 1943 — Câu hỏi: vì sao xây sân bay trên đất tranh chấp? | — | S091 | — |
| 4b | 389.0 | 15.0 | 3D phố | giao-lo-1941 · lien-hoan | 1896→2026 | 0.1 (max 3.3) | buoc-ngoat | CÚ LIÊN HOÀN #1 gib20: bay WCA 100 m → ramp → orbit giao lộ (năm dừng 1941) → crane → reveal ×12 **MỐC ĐINH** **[lien-hoan-1-gib20-1941]** — MỐC ĐINH 1941 (đã dựng ở gib20) | OSM + Catastro + Baedeker 1913 | C33, S091, S092 | — |
| 4c | 404.0 | 10.0 | 3D vùng | vinh-tay · top-down-rise | 1941→1943 | 1.0 (max 1.8) | he-qua | top-down rise; đường băng lấn vịnh theo tháng (M12) tới 1 550 yd — Đường băng mọc ra biển; đá từ hầm + vách bắc | AMS 1943 + OSM | S092, S102 | M12,M6 |
| 4d | 414.0 | 12.5 | 3D phố | ham-wwii · mat-cat | 1940–44 | 0.2 (max 0.4) | co-che | mặt cắt khối Rock (M11) theo plan hầm ONI 1954 (NARA 353129601, PD); mạng hầm sáng dần; mũi tên đá thải → đường băng — "Thành phố ngầm": Great North Road ~1 dặm, bệnh viện, nhà máy điện | — | S110, S112, S113 | M11,M1 |
| 4e | 426.5 | 5.0 | thẻ số | the · the | 1940s | 0.0 (max 0.0) | co-che | thẻ: ~55 km hầm (≈ 34 dặm) — dài hơn đường bộ trên mặt — Một con số quy tầm người; ~30 km đào trong WWII (một nguồn) | — | S106, S108, S109 | — |
| 4f | 431.5 | 9.0 | bản đồ lịch sử | bd-ams-1943 · phang | 1943 | 0.0 (max 0.0) | he-qua | AMS M981 1943 phẳng có nhãn (lên hình: bản Yale 15487373 — ĐIỀU KIỆN; Princeton chỉ bằng chứng) — Hồ sơ thật: bình đồ quân sự 1943 | — | S092 | M12 |
| 4g | 440.5 | 9.0 | 3D vùng | vinh · tu-nam-cao-2 | 1940 | 5.0 (max 8.0) | he-qua | mũi tên trung tính: dân sơ tán (M1) → Casablanca, London, Madeira, Jamaica — Hệ quả: hầu hết dân thường rời Rock 1940 (13 000–16 000 tuỳ nguồn) | ghost 1943 | S114, S117, S118, S120 | M1,M3 |
| 4h | 449.5 | 6.0 | ảnh | van-ban-tbn · ho-so | 1939/2026 | 0.0 (max 0.0) | he-qua | văn bản phản đối 1939 / lập trường MAEUEC hôm nay — trích nguyên văn — Hai phía: "porción usurpada" (TBN 1939), "ilegal" (MAEUEC) ↔ Anh (Hansard 1991) | — | S096, S098, S100, S101 | — |
| 4i | 455.5 | 7.5 | 3D vùng | eo-dat · lateral-dong | 1942 | 0.4 (max 0.8) | he-qua | lateral dọc đường băng đêm 7/8/11/1942: hàng máy bay (khối A-lite) hai bên — Hệ quả: đường băng thành bàn đạp Torch — 650 máy bay | AMS 1943 + OSM | S122, S123 | M6 |

#### Ch.5 — The Gate, 1969 → 2026 (cú lật kinh tế + điều cần theo dõi) — 100.5 s

*Hỏi: khi cổng đóng, ai mất gì? → Trở ngại: 1969–85 đóng cổng; Brexit → Bước ngoặt: con số "giàu" tính trên dân cư trú, không có người làm từ La Línea (cú lật) → Hệ quả: hiệp ước 2026 áp dụng tạm thời, EP biểu quyết dự kiến 14/12/2026*

| Shot | t0 (s) | Dài (s) | Loại cảnh | Vùng · góc | Mốc | AGL ước (km) | Vai | Máy / nội dung hình | Dữ liệu nhà | Claim | Máy dựng |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 5a | 463.0 | 9.0 | 3D phố | cong-bien-gioi · mat-dat-nhin-bac | 1969 | 0.03 (max 0.05) | co-che | cổng biên giới đóng (sepia), chắn hạ; không người — Câu hỏi: khi cổng đóng, ai mất gì? 6/1969 | OSM + Catastro (≤ 1969) | C19 | M6 |
| 5b | 472.0 | 6.0 | thẻ số | the · the | 1969/2025 | 0.0 (max 0.0) | co-che | thẻ: ~4 600 lao động ngày 1969 → 14 112 việc làm 2025 — "4 in 10 jobs" | — | C19, C08 | — |
| 5c | 478.0 | 11.0 | 3D phố | duong-bang-2026 · follow | 1985→2026 | 0.013 (max 0.03) | co-che | follow-object: người lao động A-lite đi bộ băng qua đường băng 2026 — Mở lại 1985; sáng 2026 dòng người qua đường băng | OSM + Catastro | C19b, C33, C08 | — |
| 5d | 489.0 | 11.0 | 3D phố | la-linea · lateral-cao | 2026 | 0.15 (max 0.25) | buoc-ngoat | lateral dọc phố La Línea (Catastro); 28,6 % neo trên phố — Thất nghiệp cao nhất 113 đô thị INE đo | Catastro BU 11022 | C14, C15 | M9 |
| 5e | 500.0 | 8.0 | thẻ số | the · the | 2024/25 | 0.0 (max 0.0) | buoc-ngoat | thẻ mẫu số: GDP/người theo dân cư trú vs người làm qua biên giới — CÚ LẬT (giữ từ TIEN-KY) | — | C11, C12, C13 | — |
| 5f | 508.0 | 11.0 | 3D vùng | eo-dat · boundary-trace | 1960→2026 | 0.095 (max 0.2) | he-qua | boundary trace preset gib20: hai dải màu theo số toà hai bên — Hai thành phố cùng một cổng — tô theo số, không vẽ lại biên giới | OSM + Catastro | C20, C29, C30 | — |
| 5g | 519.0 | 6.0 | ảnh | van-ban-2026 · ho-so | 2026 | 0.0 (max 0.0) | he-qua | văn bản hiệp ước 2026 Điều 2 tô dòng — Điều khoản chủ quyền | — | C07, C05 | — |
| 5h | 525.0 | 10.0 | 3D phố | cong-bien-gioi · orbit | 2026 | 0.04 (max 0.08) | he-qua | orbit cổng 2026: hàng rào cũ gỡ từng đoạn, hàng rào mới phía sau — Đúng C03: không phải "hàng rào đã đổ" | OSM + Catastro | C03, C02 | — |
| 5i | 535.0 | 6.0 | thẻ số | the · the | 2026-12-14 | 0.0 (max 0.0) | he-qua | thẻ "as of": áp dụng tạm thời từ 15/7; EP dự kiến biểu quyết 14/12/2026 — Điều cần theo dõi — có ngày | — | C26, C27 | — |
| 5j | 541.0 | 15.0 | 3D vùng | eo-dat · reveal-tong | 1704→2026 | 1.5 (max 3.0) | he-qua | reveal kéo lùi; chồng các tuyến lịch sử dạng ghost sepia (1704 tường, 1730 Línea, 1779–83, 1909 rào, 1941 đường băng) — Bảng điểm tổng kết bằng địa hình | tất cả lớp mốc | S001, C29, C30 | M4,M12 |
| 5k | 556.0 | 7.5 | 3D phố | cong-bien-gioi · mat-dat-nhin-nam-2 | 2026 | 0.003 (max 0.02) | he-qua | quay về hình mở đầu (nửa đêm) — góc ngược 0a — Câu chốt nghịch lý; dẫn sang tập kế | OSM + Catastro | C33 | — |



### 4.3 Tự kiểm trên bảng shot (`python3 -I vay-ham/tu_kiem.py` → `vay-ham/tu-kiem.json`)
Đo trên **bảng shot** (thời lượng ước, AGL ước) — không phải trên hình dựng; K đo lại trên `campath.json` / mặt nạ ở G1b. Luật NC-H1…H3 là **đề xuất NC-LS chưa khoá** (chờ K chạy thử).


| Luật | Ngưỡng | Đo trên bảng shot | Kết quả |
|---|---|---|---|
| Q26b-K2 nửa 1 | ≥ 3 loại; một loại ≤ 70 % | 6 loại; lớn nhất 3D vùng 42.2 % | ĐẠT |
| Q26b-K2 nửa 2 | ≥ 3 loại; một loại ≤ 70 % | 6 loại; lớn nhất 3D phố 39.1 % | ĐẠT |
| NC-H2 địa cầu | AGL > 50 km ≤ 1 lần, ≤ 3 s | 1 lần (0c), [2.5] s | ĐẠT |
| NC-H3 ≤ 60 km | ≥ 70 % thời lượng 3D | 99.2 % (3D = 385.0 s = 68.3 % phim) | ĐẠT |
| NC-H3 ≤ 3 km | ≥ 40 % thời lượng 3D | 87.5 % | ĐẠT |
| NC-H1 phố có nhà | mọi shot 3D nói về phố có nguồn nhà đúng mốc | 17 shot nói về phố, 13 là 3D — đều có nguồn; lỗi 0 | ĐẠT |
| Lặp vùng + góc | ≤ 2 | lớn nhất 1 | ĐẠT |
| Footage | ≤ 20 % | 0.9 % | ĐẠT |
| Shot có claim | 100 % | thiếu: 0 | ĐẠT |
| Hồ sơ thật (tranh + ảnh + bản đồ lịch sử) — Kinh thánh §4 | 10–15 % (chỉ báo) | 20.7 % | VƯỢT (đề xuất ngoại lệ D4) |
| Thời lượng — Kinh thánh §3 | 9–11 phút; móc ≤ 45 s | 563.5 s (9:23.5); móc 43.5 s | ĐẠT |
| Mốc đinh | ≥ 1/chương bước ngoặt | 6: 1e @ 82.0 s; 2g @ 199.0 s; 2m @ 253.0 s; 3b @ 323.5 s; 3f @ 359.0 s; 4b @ 389.0 s | ĐẠT |
| Cú liên hoàn | 1–2 | 2: lien-hoan-1-gib20-1941, lien-hoan-2-vinh-1782 | ĐẠT |

**Tỷ lệ loại cảnh cả phim:** 3D vùng 37.2 % · 3D phố 31.1 % · thẻ số 10.1 % · ảnh 8.3 % · bản đồ lịch sử 8.2 % · tranh Ken Burns 4.2 % · footage 0.9 %
**Chỉ số trong ±5 % quanh ngưỡng:** không có


## 5. Máy dựng cho T3 (để kịp 14/12) — việc cho V5b-2b
Đánh số M theo NC-LS §5.2. **P0** = thiếu thì không dựng được shot trong bảng; **P1** = có phương án dự phòng làm giảm hình (vẫn đúng); **P2** = làm nếu còn thời gian.

| Ưu tiên | Việc | Shot dùng | Cách làm (từ mã đã có) | Dữ liệu vào | Dự phòng nếu trễ |
|---|---|---|---|---|---|
| **P0** | Tích hợp 9 điểm V5b-2a §8 (hero.js llvmpipe + kiểm renderer, trang `tl/` trong `scripts/k2`, SPP theo pha, LUT A, env_check vào verify/VERSIONS) | mọi shot 3D | đã chỉ đúng dòng mã ở V5b-2a §8 | — | không có (chặn) |
| **P0** | **Ghi AGL mỗi khung vào `meta.json`** (NC-H2/H3 đo được trên `scripts/k2`) | mọi shot 3D | `campath.js grammarLog` đã có AGL → xuất ra meta | — | đo tay từ campath (chậm) |
| **P0** | **M9 nạp footprint chung + mái theo thời kỳ (bản rút gọn 3 bộ)**: (a) 1704–1782: mái ngói thấp + sân thượng phẳng; (b) 1900–1943: mái ngói + mái bằng, ban công; (c) 2026 (có sẵn) | 0e, 1d, 1e, 2g, 2j, 2m, 3f, 4b–4c, 5a–5k | tổng quát bộ nạp Catastro → nạp GeoJSON bất kỳ (OSM, ghost) | OSM, Catastro, GeoJSON ghost (§3.3) | khối ghost không mái (đúng nhưng thô) |
| **P0** | **M12 bản đồ pha theo mốc** (raster đã nắn crossfade làm vân mặt đất + lớp ghost theo mốc) | 0e, 1d, 1i, 2g, 3f, 4c, 5j | tầng CHUẨN đã có khái niệm mốc → thêm raster/vector theo mốc | 5 bản đã nắn (§3.3) | chỉ ghost không vân |
| **P0** | **M6 ngày/giờ + mặt trời**: bộ đếm "13 Sep 1782 · 09:45"; hai lịch "24 Jul (O.S.) / 4 Aug (N.S.) 1704"; mặt trời theo thiên văn tại 36,14° B | 1a, 1e, 2a, 2g, 2m, 2o, 2q, 3b, 3f, 4c, 4i | biến thể bộ đếm `text.js` + vị trí mặt trời | `lich_su_kien` (28 mốc, `claims-vay-ham.json`) | bộ đếm năm (mất giờ) |
| **P0** | **M3 rút gọn**: hạm đội theo đội hình + đường đi theo giờ (1704, phong toả 1779, 3 đoàn tiếp tế, 10 pin nổi 13/9/1782) | 1a, 2c, 2f, 2m, 4g | `ships.js` (đã có tàu buồm) + đường đi | vị trí từ Drinkwater 1786 plan các khẩu đội (đã nắn) | tàu tĩnh + mũi tên |
| **P0** | **M4 rút gọn**: chiến tuyến/hào mọc theo ngày (dải hạ thấp + gờ đất trên DTM), dải màu phe | 1j, 1k, 2a, 2q, 3a, 5j | mở rộng `overlay3d.js` (dải bám ranh) | tuyến từ Faden 1783 + plan xuất kích (đã nắn) | dải màu phẳng không gờ |
| P1 | **M1 mũi tên** (ruy băng bám địa hình, mọc theo giờ, màu trung tính cho dân thường) | 1g, 2f, 4d, 4g | `overlay3d.js` | tuyến GeoJSON + mốc giờ | mũi tên 2D lớp chữ |
| P1 | **M7 khói/lửa sprite 2D** + đổi vật liệu "cháy → ghost tro"; **không người trong vùng khói**; lửa đỏ ≤ 15 % khung | 1e, 2g, 2m, 3b | billboard + tích luỹ SPP | vùng cháy theo nguồn (S062–S063) | chỉ đổi vật liệu (không khói) |
| P1 | **M8 Ken Burns tranh trong trang tl** (crop theo luật §6.2; thẻ neo) | 0f, 1b, 2e, 2l | tích hợp cắt nền + Ken Burns k2v | tranh CC0/PD (§2) | dùng plate k2v ngoài tl (cắt cảnh) |
| P1 | **M11 mặt cắt đường hầm**: (a) 1782 vách bắc — gallery theo ngày (82 ft → 140 ft → ~600 ft); (b) WWII — mạng hầm theo plan ONI 1954 | 2o, 4d | khối đá DEM cắt mặt phẳng + ống hầm | S080–S084; NARA 353129601 | bản đồ hầm phẳng có nhãn |
| P2 | **M5 thành luỹ tham số** (King's Bastion đầy đủ: mặt bằng góc, tường chắn mái, ụ pháo) | 2j, 2m | `heroes.js` tham số | OSM + plan 1782 | đùn footprint OSM + gờ (P0 M9 đủ dùng) |
| — | M2 đội hình bộ binh | không shot nào | **không làm cho T3** (V6) | — | — |

**Hero cần dựng (kích thước + nguồn):**
| Hero | Kích thước / dữ liệu | Nguồn |
|---|---|---|
| Rock + vách bắc | DEM GLO-30 (30 m) đã nạp gib20; lưới mịn 20 m; vách bắc đã sửa lỗi xuyên lưới (V5b-2a §4.3) | Copernicus DEM (TIEN-KY §6) |
| King's Bastion (xây 1773, theo plan 1782) | toà OSM 952588383 **1 294 m²** (bbox 35 × 89 m); cả khu bastion nay (Leisure Centre 256821558) **4 231 m²** (58 × 111 m) | OSM (`vay-ham/osm-do.json`); hình dạng 1782 từ Drinkwater 1786 |
| Line Wall Curtain + Charles V Wall | Line Wall ≈ 3,4 km (6 đoạn OSM); Charles V Wall 292 + 354 m, `start_date` 1540 | OSM |
| Línea de Contravalación + Fort San Felipe (tây) + Fort Santa Bárbara (đông) | tuyến ngang eo đất (khởi công 11/1730, xong 1735; phá 1810) — kích thước từ Faden 1783 + plan cuộc xuất kích sau nắn | S032, S034; Yale 2046612, Drinkwater 1786 |
| 10 pin nổi (13/9/1782) | 138–142 pháo / 5 190–5 260 người cho 10 chiếc; vị trí neo ~900 yd (tàu chỉ huy, MÂU THUẪN) — **kích thước thân tàu chưa có nguồn** → dựng theo bản khắc (Rijks 19.249, Drinkwater view), nhãn "illustrative" | S066, S068; d'Arçon (mémoire gốc chưa tải) |
| Great Siege Tunnels (1782) | gallery cao 8 ft (S081); 82 ft (4/7/1782) → 140 ft (5/8/1782) → ~600 ft (5/1783); lối vào trên Farringdon's battery (OSM 672708050, 525 m²) | S080–S084 |
| Hầm WWII | tổng ~55 km; Great North Road ~1 dặm; phòng bệnh viện 61 × 10,7 × 3,7 m | S106–S113; NARA ONI 1954 |
| Đường băng | 1934–36 dải cỏ (không có chiều dài) → mục tiêu 1 550 yd (1 417 m) dùng được 7/1943 → nay **1 798 × 45 m**, 087,5°/267,5°, toạ độ ngưỡng AIP | S090–S094; UK Mil AIP; OSM 157316482 |
| Cổng biên giới | OSM node 5029266974 (`barrier=border_control`) — đã dựng ở gib20 (1941) | V5b-1b |

**Ước giờ máy thêm cho T3 (ước, máy D):** nền NC-LS §5.3 ≈ 6,7 h (dải 5,5–7) cho tập 10 phút; bảng shot T3 có 3D = 68,3 % (≈ 6:25) → ≈ **5,5–6,5 h** dựng + mặt nạ, cộng cú #2 (SPP4 orbit) ≈ +0,1 h; dưới trần 12 h. Phải đo lại trên đoạn thử V5b-2b-T (phố ghost dày) trước khi khoá.


## 6. Nhạy cảm: luật câu chữ chiến sự, luật hình chiến tranh, lọc bình luận

Mức: **VÀNG đầy đủ** (giữ TIEN-KY §7, cả 6 điều kiện VÀNG của QUAN-TRI-RUI-RO §1). Khung vây hãm **thêm** một lớp rủi ro: chiến tranh (bạo lực, thương vong) và tự hào dân tộc hai phía (Great Siege là biểu tượng ở Anh/Gibraltar; Tây Ban Nha nhìn là mất đất). Luật dưới đây **mở rộng** TIEN-KY §7, không thay.

### 6.1 Luật câu chữ — phần chiến sự (lời, tiêu đề, thumbnail, mô tả, bình luận ghim)
| # | Tránh (lời của kênh) | Dùng thay | Lý do / claim |
|---|---|---|---|
| CS1 | "occupied", "stole", "colony", "usurped", "reconquered" | "captured in 1704" (S012, S017: nhân danh ứng viên Habsburg); "held" / "kept"; khi cần chữ của một phía thì **trích nguyên văn + nói rõ ai nói** ("Spain's foreign ministry calls it…") | TIEN-KY §7 mở rộng sang 1704–1783 |
| CS2 | "heroic defence", "glorious victory", "the Spanish were crushed", "humiliating defeat" | động từ cơ chế: "the batteries failed / burned / were abandoned"; "the siege was lifted"; "neither side could…" | không tôn vinh bạo lực (NC-LS §7.5.3); giọng giáo dục trung tính (AFG "Educational … expresses an opinion in a neutral way") |
| CS3 | "the British", "the Spanish" như một khối đạo đức ("the Spanish wanted revenge") | chủ thể cụ thể: "the Spanish crown", "the garrison", "the Franco-Spanish fleet", "Gibraltar's civilians" | không gán động cơ cho cả dân tộc |
| CS4 | số thương vong một phía, hoặc số không nói ai đếm | **luôn "by the British count / by Spanish records"**, có số hai phía khi lệch (bảng `so_hai_phia` trong claims) | luật lệnh mục 1 |
| CS5 | "15 sieges" (tính cả 1969–85) hoặc số thứ tự từng cuộc vây | "Historians count fourteen sieges between 1309 and 1783" (D1) | S001–S008 |
| CS6 | "the Spanish lines were an occupation of British land" / "Britain's illegal advance onto Spanish soil" | mô tả vật lý + hai lập trường trích nguyên văn (C29 ↔ C30); eo đất = "the isthmus", "the neutral ground (as maps of the time call it)" | chủ quyền eo đất là trục tranh chấp hiện nay |
| CS7 | "Franco closed the border to punish…" (suy động cơ); "a fifteenth siege" (S007) | "In June 1969 Spain closed the land frontier" (C19) + trích lý do chính thức của TBN nếu có nguồn | không suy động cơ người thật |
| CS8 | gọi 1941 đường băng là "a land grab" hoặc "perfectly legal" | "built across the isthmus in 1941 (C33); Spain says… (S096, S100) ; the UK says… (S031, S101)" | hai phía |
| CS9 | "unbreakable fortress", "impregnable" | "none of the three sieges after 1704 took it" (S001 danh sách: 1704–05, 1727, 1779–83) | không hứa vượt claim (QUAN-TRI-RUI-RO §2) |
| CS10 | cảnh/chữ chế giễu phe thua (pin nổi "useless", "ridiculous") | "the design rested on one assumption that failed: …" (cơ chế) | — |

### 6.2 Luật hình chiến tranh (áp NC-LS §7.5 cho từng loại cảnh của bảng shot)
| Loại cảnh | Được | Không |
|---|---|---|
| 3D phố/vùng | khói 2D (M7) ở công trình, tàu, pháo đài; đổi vật liệu "cháy → ghost tro"; mũi tên/tuyến theo phe | người A-lite trong vùng khói/lửa; người ngã; máu; xác; tàu chìm có người; ánh lửa đỏ phủ khung > 15 % (giảm cảm giác đồ hoạ) |
| Tranh Ken Burns | crop phần tàu, thành luỹ, cảnh quan, chân dung | vùng tranh có người chết/hấp hối/chết đuối làm tiêu điểm (vd. nhân vật hấp hối ở giữa tranh "Sortie" của Trumbull; người chết đuối ở cảnh pin nổi) → **crop bỏ hoặc không dùng**; kiểm từng khung Ken Burns trước khi khoá |
| Ảnh 1940s | sân bay, công trường, tàu, sơ tán (người đi bộ, hành lý) | ảnh có thương vong, tù binh, biểu tượng cực đoan |
| Thẻ số | thương vong = số + chấm/cột trung tính (một chấm = N người), màu trung tính, **không** màu phe đỏ máu | đầu lâu, thập tự, hình người ngã, "body count" |
| Footage | then/now đường hầm, đường băng (Pexels/Pixabay đã kiểm từng clip) | footage chiến tranh có người bị thương/chết; footage IWM/Pathé |
| Thumbnail | Rock + chiến tuyến + đường băng; tàu ở xa; khói trên pháo đài không người | vũ khí chĩa vào người; lửa có người; cờ làm điểm nhấn; biểu tượng cực đoan; tranh có người chết |

Bối cảnh giáo dục **trong hình và tiếng** (YouTube EDSA): câu mở nói rõ đây là giải thích lịch sử; dòng nguồn ngắn ≥ 38 px khi có số.

### 6.3 Lọc bình luận (bật từ phút đăng)
- Từ khoá chặn/giữ để duyệt (EN/ES): các từ miệt thị dân tộc hai phía (danh sách đầy đủ để ngoài git, P giữ), "invade", "take it back by force", "nuke", "war now", "Ceuta" + "Melilla" + "Morocco" (giữ để duyệt, không chặn), "colony" (giữ để duyệt).
- Không trả lời bình luận chủ quyền; ghim một bình luận nguồn + "as of" (C26) và cam kết cập nhật sau 14/12.
- Sửa sai có trọng số ≥ 20 like: đối chiếu claims trong 48 h, sửa mô tả/bình luận ghim nếu đúng (NC-LS §8 chỉ số "độ đúng").


## 7. Đóng gói

### 7.1 Ba tiêu đề (mở bằng "Why", có tên nơi, ≤ 60 ký tự)
| # | Tiêu đề | Ký tự | Claim | Ghi chú |
|---|---|---|---|---|
| **T-A (đề xuất)** | **Why Gibraltar Was Besieged 14 Times** | 35 | S001–S008 | số có nguồn hai phía; khớp thumbnail A |
| T-B | Why Gibraltar Was Fought Over for 474 Years | 43 | S001 (1309 → 1783) | "fought over" trung tính; số tự tính từ hai năm có nguồn |
| T-C | Why Gibraltar's Road to Spain Crosses a Runway | 46 | C33, S092 | móc 1941 → nay; dùng cho Short hoặc Test & Compare |
- Tránh: mẫu "Why everyone wants …" (đã có video dùng, kiểm 17/10 bằng `search.list`, 200 đv); "occupied/stole/colony"; "impregnable"; "still at war".

### 7.2 Thumbnail (Kinh thánh §2: bản đồ thật, vùng tô nổi, một số/1–2 từ trong hộp, ≤ 2 biểu tượng; biến thể không chữ quá khứ–hiện tại)
```
THUMBNAIL BRIEF — K2C-T3-01 (khung vây hãm)
[A] BẢN ĐỒ VÂY HÃM
- Nền: render 3D của mình (Copernicus GLO-30 + Sentinel-2), Rock nhìn từ tây-bắc, thấp, thấy vách bắc + eo đất + vịnh; rõ ở 168×94.
- Vùng tô: dải chiến tuyến TBN 1782 (sepia, đúng vị trí Faden 1783) + đường băng nay (xám nhựa) cắt ngang eo đất.
- Hộp chữ (nền tối, 1 hộp): "14 SIEGES" (S001). Phương án A2: "1309–1783".
- Biểu tượng (≤ 2): sticker pin nổi (thân tàu, không lửa, không người) ở vịnh; sticker chìa khoá (mô-típ "key of the Mediterranean" — cả nguồn Anh lẫn TBN, S010).
[B] HAI THỜI (không chữ)
- Cùng góc máy, chia dọc: trái 13/9/1782 (sepia; pin nổi ở xa, khói trên pháo đài, KHÔNG người, không lửa phủ khung); phải 2026 (tự nhiên; đường băng, người đi bộ A-lite băng qua).
Chung: không cờ làm điểm nhấn; không vũ khí chĩa vào người; không tranh có người chết; mọi số có trong video; lề 5 %; tránh góc dưới-phải.
Test & Compare: A, A2, B.
```

### 7.3 Câu "as of" (hiệp ước, hạn 14/12) — dùng trong lời, trên hình (thẻ 5i) và mô tả
- Lời/hình: *"As of [ngày khoá lời], the UK–EU treaty on Gibraltar has been applied provisionally since 15 July 2026. The European Parliament's consent vote is indicatively scheduled for 14 December 2026."* (C02, C26 — nguồn: EP Legislative Train 2026/0058(NLE), EM CP 1645 §5.6).
- Mô tả: thêm *"Facts as of [ngày đăng]. We will update the pinned comment after the European Parliament vote."*
- Phải đọc lại hai nguồn **ngay trước khi khoá lời (G1) và ngay trước khi đăng**; nếu ngày biểu quyết đổi → sửa thẻ 5i, mô tả, bình luận ghim.


## 8. Lộ trình ngược từ 14/12/2026 (theo MỐC)

Đích: video dài + Short **đăng trước phiên biểu quyết dự kiến của Nghị viện châu Âu 14/12/2026** (C26), để "điều cần theo dõi" còn mở; bình luận ghim cập nhật sau biểu quyết. Còn **58 ngày** kể từ 17/10 (chỉ để biết độ dài cửa sổ; kế hoạch dưới đây theo mốc).

| Mốc | Việc | Đầu vào bắt buộc (chặn bởi) | Đầu ra | Chặn việc nào |
|---|---|---|---|---|
| **T3b** (phiên này) | claims vây hãm, tài sản có quyền, dữ liệu nhà theo mốc, treatment theo shot, danh sách máy dựng | — | `TIEN-KY-VAY-HAM.md`, `claims-vay-ham.md`, `vay-ham/*` | mọi mốc sau |
| **D** chủ dự án duyệt | D1–D10 ở §0 (cách đếm số lần vây, tiêu đề, mạch, ưu tiên máy dựng, ngoại lệ hồ sơ thật, tài sản điều kiện) | T3b | AUTHORSHIP (P ghi) | V5b-2b, số hoá, G1 |
| **SH** số hoá ghost (phiên tiền kỳ số hoá, song song V5b-2b) | nắn + vẽ khối phố cho các mốc có nguồn (§3.3) | D (chọn mốc), tư liệu §2 | GeoJSON ghost theo mốc + sổ điểm khống chế + RMS (ngoài git; SHA trong repo) | cảnh **3D phố** các mốc 1704/1779–83/1941 (không có → đổi sang bản đồ lịch sử phẳng) |
| **V5b-2b** máy dựng | tích hợp 9 điểm V5b-2a §8 + P0 (§5) | D (ưu tiên P0/P1) | mã `design/k2v/tl`, `scripts/k2*`; test ĐẠT | G1b, render |
| **V5b-2b-T** đoạn thử phố Gibraltar 20–30 s | một cảnh 3D phố 1782 (ghost từ SH) + một cảnh vịnh 13/9/1782 (M3/M6/M7) qua **cổng chuẩn hình** (MAU1, BC1, NC-H1/H2/H3 bản K chạy thử) | V5b-2b P0, SH mốc 1782 (tối thiểu) | 540p + tờ khung + số đo | G1b (nếu trượt: vòng sửa trước khi viết shot G1b) |
| **K** chạy thử NC-H1…H5 trên gib20 + T2 + đoạn thử | khoá ngưỡng (25 %/15 %, 50 km/3 s, 60 km/3 km) | V5b-2b-T | `checks/` (chỉ K) | G1b chấm chính thức |
| **G1** | lời (EN) + claims chốt (REVIEWER Opus độc lập — điều kiện VÀNG 3) + treatment theo câu + 3 tiêu đề + PACKAGING-BRIEF + trần ElevenLabs | D, claims §1 (mục CHƯA XÁC MINH phải xong hoặc bỏ) | G1 duyệt (chạm 1) | thu giọng, G1b |
| **G1b** | animatic 540p / tờ khung toàn tập theo bảng shot thật | G1, V5b-2b, đoạn thử ĐẠT | 540p + tờ khung (chạm 2 nếu cần) | render |
| **Giọng** | ElevenLabs (trần ghi ở G1), ASR kiểm tên riêng (Rooke, Eliott, d'Arçon, Crillon, La Línea, Santa Bárbara) | G1 | VO + align | render lớp chữ |
| **Render** | 3D llvmpipe ≈ 6–7 h máy D (NC-LS §5.3 ước, chưa tính M7) + mặt nạ + lớp chữ + ghép | G1b, giọng | master 1080p + Short | G2 |
| **G2** | QC nhà máy + k2check + chấm mù (giao thức T2) + kiểm footage/tranh từng khung (luật hình §6.2) | render | G2 duyệt (chạm 3) | đăng |
| **Đăng** | trước 14/12; bình luận ghim nguồn + "as of"; lọc bình luận bật; theo dõi 48 h (QUAN-TRI-RUI-RO §5) | G2 | — | cập nhật sau 14/12 |

**Đường găng:** D → (V5b-2b P0 ∥ SH 1782) → đoạn thử qua cổng → G1b → render → G2 → đăng. G1 (lời) chạy **song song** với V5b-2b/SH; không chặn máy dựng.
**Điểm cắt giảm có sẵn (nếu đường găng trễ, không giảm chất lượng hình đã làm):** (i) bỏ ghost 1704 → bản đồ LoC 1705 phẳng (shot 1d → bản đồ lịch sử); (ii) M11 mặt cắt → bản đồ hầm phẳng có nhãn; (iii) M7 khói → chỉ đổi vật liệu. Mỗi điểm cắt đổi loại cảnh trong bảng shot → chạy lại `tu_kiem.py` (Q26b-K2, NC-H3).


## 9. Chi phí thật, tệp, preflight, đề xuất ngoài vùng
| Hạng mục | Trần | Thực tế |
|---|---|---|
| Claude API | $1 (ghim) | **$0** — không gọi API trả tiền; không có `cost.jsonl` |
| YouTube Data API | 500 đv | **200 đv** (`search.list` × 2, kiểm trùng tiêu đề; kết quả thô ngoài git) |
| ElevenLabs | 0 | **0** ký tự |
| Giờ máy | 1 h | **≈ 0,15 h (ước)** — tải, tách chữ PDF/HTML, kiểm SHA + câu trích, script bảng; không dựng hình |
| Mạng | — | ≈ 1,1 GB, 207 tệp ngoài git `/var/tmp/cine-out/t3b/` (tư liệu gốc 764 MB) |
| Token (trần mềm) | — | 4 tác tử Claude Code ≈ **1,04 triệu token** (290 k / 252 k / 204 k / 297 k) + phiên P; cao hơn mức "~10 nghìn/nguồn" của BAI-HOC #14 vì tác tử tự tìm và đọc 65 nguồn sơ cấp — đổi lại 123 claim có trích + 39 tài sản đã kiểm quyền. Ghi ở `vay-ham/cost.json` |

**Tệp trong nhánh (chỉ thêm, trong `channel-k2/k2c-t3-01/`):**
- `TIEN-KY-VAY-HAM.md` (tệp này) · `claims-vay-ham.md`
- `licenses/`: 39 tệp tư liệu mới + `osm-odbl-attribution.txt` + `catastro-inspire-bu.txt` (không trùng tên tệp cũ)
- `vay-ham/`: `claims-vay-ham.json`, `idmap.json` (mã gói → S…), `tai-san-vay-ham.json`, `treatment.json`, `treatment-rows.txt`, `tu-kiem.json`, `osm-do.json`, `cost.json`; script `gop_claims.py`, `mk_treatment.py`, `tu_kiem.py`, `bang_md.py`, `osm_stat.py`, `verify_quotes.py` (chỉ đọc dữ liệu ngoài git); `ref/` 39 ảnh xem trước ≤ 1600 px (14 MB, mỗi tệp < 1 MB); `bang_md.py` sinh bảng §2.2/§4.2/§4.3 ra tệp tạm `_*.md` (không commit).
- JSON thêm bằng `git add -f` (`channel-k2/.gitignore` chặn `*.json`), như TIEN-KY.

**Preflight:** hook pre-commit/pre-push cài đầu phiên; mọi commit **PREFLIGHT ĐẠT**, `lock.py --verify` **KHỚP**; không dùng `--no-verify`. Lưu ý: chạy tay `tools/preflight.sh --range origin/main..HEAD` trong lúc có tệp chưa commit báo các mục P3/P5 **của tệp có sẵn trên main** (nhạc `assets/k2/music/*.mp3`, giấy phép k2c-t1-06) — không thuộc khoảng commit của phiên; hook pre-push (đúng khoảng của nhánh) ĐẠT.

**Ghép thử:** nhánh chỉ thêm tệp mới trong `channel-k2/k2c-t3-01/`, không sửa tệp có sẵn → không xung đột với `main`, `k2c-t3-tienky`, `v5b2a`, `nc-lich-su`, `k2c-t2`.

**Đề xuất cho P (ngoài vùng, chưa ghi):**
1. `COST-LEDGER.csv`: `T3b-01, 2026-10-17, k2c-t3-tienky-b, tiền kỳ, claude_api_usd=0, youtube_units=200, elevenlabs_chars=0, render_h=0.15`.
2. `RIGHTS.md`: một dòng cho mỗi tài sản **khi được dùng thật ở G1** (nguồn: `vay-ham/tai-san-vay-ham.json` + `licenses/`); dòng OSM ODbL (cách ghi công §3.1).
3. `channel-k2/.gitignore`: `!k2c-t3-01/vay-ham/*.json`.
4. `docs/BIBLE-KENH2.md` (nếu D4 duyệt): ngoại lệ "hồ sơ thật" cho tập lịch sử; luật câu chữ chiến sự CS1–CS10 + luật hình §6.2 vào `LUAT-NOI-DUNG-G.md`.
5. `BAI-HOC-K2.md`: (a) bản chép "sạch" của tổ chức uy tín vẫn có lỗi đổi nghĩa (GHT "having the sale") → trích từ bản in gốc; (b) Princeton ghi "non-commercial" cho bản quét tác phẩm PD → luôn có bản sao thứ hai; (c) preflight `--range` khi working tree bẩn báo lỗi tệp có sẵn.

## 10. Tự quyết của phiên (không dừng hỏi), cần chủ dự án biết
1. **Mạch giữ đúng NC-LS §4.2 (Móc + 5 chương)**, không chia Great Siege thành 2 chương; Great Siege dài nhất (2:48) vì là trục và có câu hỏi hậu cần.
2. **Thời lượng shot 3D/bản đồ/tranh giãn ×1,25** so nhịp hình để đạt 9–11 phút (Kinh thánh §3); không thêm shot chỉ để đủ phút. Lời G1 sẽ quyết thời lượng thật.
3. **Shot 0c (địa cầu) giữ 1 lần 2,5 s** để định vị eo biển — đúng giới hạn NC-H2; có thể bỏ nếu chủ dự án muốn 0 lần.
4. **AMS 1943 bản Princeton → "điều kiện"** (D8), dù gói tư liệu đánh "commercial_ok".
5. **Emes 1784 không dùng làm Ken Burns; Sharp/Copley chỉ nửa phải; Trumbull "Sortie" (Met 12828, đã có ở TIEN-KY) không dùng nhân vật hấp hối làm tiêu điểm** — luật hình §6.2.
6. **"Ince proposed" không dùng** dù phổ biến (chỉ nguồn bách khoa).
7. Thử 2 lượt `search.list` (200 đv) để tránh tiêu đề trùng — không chép tiêu đề kênh khác vào repo.
8. Kiểm câu trích **độc lập** thay vì tin báo cáo tác tử (BAI-HOC "số đo thật thắng số tự khai").

## 11. Việc đang chờ chủ dự án
1. **Duyệt D1–D10** (§0): cách nói "14 sieges"; mạch 9:23; cú liên hoàn #2; ngoại lệ hồ sơ thật 20,7 %; phạm vi số hoá 3 mốc (≈ 37–47 h người — **cần chỉ định ai/phiên nào số hoá**); ưu tiên P0/P1/P2 cho V5b-2b; luật chiến sự CS1–CS10 + crop tranh; AMS 1943 bản Yale; đặt quét LoC 2005677710; tiêu đề T-A + thumbnail A/B.
2. **Mở phiên V5b-2b** với danh sách §5 (P0 trước) và **đoạn thử phố Gibraltar 1782** qua cổng chuẩn hình; mở **phiên số hoá ghost** song song (mốc 1782 trước, rồi 1704, 1943).
3. **Giao K** chạy thử NC-H1…H5 trên gib20 + T2 + đoạn thử để khoá ngưỡng (25 %/15 %, 50 km/3 s, 60 km/3 km).
4. **P ghi** COST-LEDGER, `.gitignore`, (khi dùng) RIGHTS, AUTHORSHIP theo §9.
5. **Nguồn còn mở trước G1:** mémoire gốc của d'Arçon (kích thước pin nổi); Gaceta de Madrid (thương vong TBN); Hills/Fa & Finlayson (danh sách 14 cuộc bản hiện đại); nguồn Anh cho lý do dựng rào 1909; RAF AHB "Flying from the Rock" (403); ảnh 1941.
6. **Lịch:** xác nhận vẫn đăng **trước 14/12/2026**; ngày khoá lời G1 dùng làm mốc "as of".
