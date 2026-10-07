# M2.2b — ANIMATIC V3 CẢ TẬP "The Last Lamplighters" · 01/10/2026

Kênh Last Lamplighters, Mốc 2. Chủ dự án duyệt lát cắt M2.2a làm chuẩn kênh và mở animatic v3 cả tập (AUTHORSHIP 01/10/2026).
- Kịch bản v3.1. Giọng Bill thu thật. Áp đủ `CHUAN-KENH-LL.md`, gồm cả §6 "Đĩa và bàn giao".
- P: thu giọng, dòng thời gian, nhạc, mix, ghép, đo, sửa sau xưởng.
- Bốn gói xưởng: STORY, STORY-2, HISTORY, TODAY. Báo cáo từng xưởng ở `reports/m3/m2-2b/BAO-CAO-XUONG-*.md`.
- **Mọi số dưới đây là số đo thật trên tệp**, P đo lại sau xưởng.

## 1. Sản phẩm
| Tệp | Nội dung | Thông số | Dung lượng | SHA-256 |
|---|---|---|---|---|
| `screening/ll-ep01-animatic-v3-p1.mp4` | đoạn 01–07 (0:00–3:20,25) | 1280×720, 24 fps, H.264 2 lượt hình 2,8 Mb/s, AAC 128 kb/s | 72,8 MB | 5e78fda4…94c06 |
| `screening/ll-ep01-animatic-v3-p2.mp4` | đoạn 08–14 (3:20,25–7:11,92) | như trên | **84,8 MB** | c3df2b75…193bb |
| `screening/ll-ep01-animatic-v3-p3.mp4` | đoạn 15–19 (7:11,92–9:56,58) | như trên | 60,8 MB | 9e119483…c42fb |
| Master (ngoài git) | `/var/tmp/cine-out/ep01/out/ll-ep01-animatic-v3-master.mp4`, 1920×1080, 24 fps, H.264 crf 16, AAC 256 kb/s | | 840,7 MB | `3891882d6444ce2156ea160cc3ca1a6753a9651beb7ed5e285c92f28d694ec06` |

- **Thời lượng thật: 9:56,58** (14 318 khung), dưới trần 11:00.
- Bản xem không có phụ đề cháy vào hình.

## 2. Tỷ lệ thật
Bảng tính 7 s cầu nối đầu khối 10–13 về STORY.

| Phần | Giây | Tỷ lệ thật | Đích | Lệch |
|---|---|---|---|---|
| STORY | 103,7 | **17,4 %** | 20 % | −2,6 điểm |
| HISTORY | 218,2 | **36,6 %** | 35 % | +1,6 điểm |
| TODAY | 274,7 | **46,0 %** | 45 % | +1,0 điểm |

- Cả ba phần nằm trong ±5 điểm % so với đích.
- STORY thấp hơn đích. Lý do: Bill đọc chậm hơn công thức 141,2 từ/phút ở phần số liệu, nên HISTORY và TODAY dài ra.
- Theo chỉ thị, không rút thời lượng STORY.

## 3. Số đo
| Chỉ số | Chuẩn | Kết quả | Đo trên |
|---|---|---|---|
| **Judder** (đứng hình 2–12 khung) | 0 | **0** ở cả 16 đoạn | trung gian H.264 crf 10 yuv444p (số chuẩn, §6.4) |
| Judder, đối chiếu | 0 | **0** | master; p1, p2, p3 (không lệch đoạn nào) |
| Giữ 13–23 khung / giữ ≥ 1 s / giây < 12 khung mới | — | 0 / 0 / 0 | trung gian, master, 3 phần |
| **Loudness tích hợp** | −14 LUFS | **−14,0** | master có tiếng |
| **True peak** | ≤ −1 dBTP | **−1,6** | master |
| LRA | — | 3,5 LU | master |
| Loudness 3 phần (đối chiếu) | — | p1 −14,2 / p2 −14,0 / p3 −14,0 LUFS; TP −1,4 / −1,5 / −1,5 | 3 phần bản xem |
| Nhạc hạ khi có lời | 10–14 dB | **12,0 dB** | đường bao, đo trên cùng mẫu |
| Tương phản chữ thấp nhất | ≥ 4,5:1 | **4,79:1** ("1820s", đoạn 02); các đoạn khác ≥ 4,86:1 | clip trung gian (xưởng đo; P xem lại khung) |
| Số khung từng đoạn | đúng timeline | **16/16 khớp** | trung gian |
| Kiểm mù màu | phân biệt được nhóm | **đạt** ở protanopia, deuteranopia, tritanopia trên 8 khung số (08, 09, 10–13 ×2, 14, 15, 16, 17). Thực tế/dự báo phân biệt bằng đặc và gạch chéo, kèm nhãn chữ | `scripts/p/mu_mau.py`; ảnh ở `reports/m3/m2-2b/mu-mau/` |
| Giọng | khớp văn bản, không cụt | whisper khớp 15/15 đoạn mới, chỉ lệch chính tả hoặc đồng âm | các take Bill |

- **ElevenLabs:**
  - gửi 5 696 ký tự cho đoạn 01–09 và 14–19; đoạn 10–13 dùng lại take của lát cắt;
  - bộ đếm **3 649 → 5 707**; gói Creator, hạn 144 034.

### Chỉ số trong ±5 % quanh ngưỡng (nêu tên theo luật)
- **Loudness −14,0 LUFS:** đúng đích.
- **Phần p2 dung lượng 84,8 MB / 90 MB:** dưới trần 5,8 %, sát vùng ±5 %.
- **True peak phần p1 −1,4 dBTP:** cách ngưỡng −1 dBTP 0,4 dB, do mã hoá lại AAC. Master đạt −1,6.
- **Tương phản 4,79:1** (đoạn 02) và **4,86:1** (đoạn 06): cao hơn ngưỡng 4,5:1 lần lượt 6,4 % và 8 %. Đây là chữ nâu ở góc tối.

## 4. Sửa theo yêu cầu (lát cắt → animatic v3)
| Mục | Cách xử lý | Ở đâu |
|---|---|---|
| **L1** · hai quãng trống | 13,4–24,4 s: bìa báo cáo BLS cắt giấy, năm dòng trống chờ tên nghề, dải 2025 → 2035, mỗi phần tử hiện đúng từ lời. 45,7–58,6 s: dải 2023 → 2033, thẻ trích MLR chữ lớn hiện từng cụm theo lời. Dời tiêu đề và thẻ PROJECTION vốn hiện trước lời ở lát cắt | khối 10–13 |
| Luật **≤ 3 s trống** | rà theo mốc sự kiện. Thêm hình cho câu "one task, repeated…" (10–13) và chữ "London:" (07) | cả tập |
| **L2** · chuỗi thang máy | ngắt đường ở chỗ đổi phân loại. Mảnh 1900–1950 (97k, phân loại 1950), mảnh 94k → 77k (phân loại 1960), mảnh 77k → 37k (phân loại 1970); mỗi mảnh một kiểu điểm, có ghi chú. Đoạn 14 dùng cùng gốc: −18 % = 94 → 77, −52 % = 77 → 37 | 08, 10–13 (G1), 14 |
| **L3** · end / change / new | đặt ở dải trống riêng, có mũi tên ngắn; không đè ô thu nhỏ hay mép biểu đồ. Đoạn 18 xếp thành ba cột đèn | 10–13, 18 |
| **L4** · ghép hai đợt dự báo | vạch ngăn nét đứt suốt bề ngang; nhãn đợt riêng; hai dòng nguồn có tiền tố "2023–33:" và "2025–35:" | 10–13 |
| Khối văn phòng cảnh mở | ba khối ở ba độ sâu; cửa sổ sáng không đều (mật độ theo tầng, ≈ 7 % ô ấm); ≈ 4,5 % ô bật/tắt chậm; sương theo độ sâu ≈ 4 / 26 / 53 / 81 % | tấm nền br10 (10–13), đoạn 19 |
| Bóng s03/s05 | viền sáng 2,75 px quanh toàn bộ bóng, sáng gấp đôi nền (1 stop) | đoạn 03 (người thắp đèn vô danh) |
| Kiểm mù màu toàn tập | công cụ mới `scripts/p/mu_mau.py` (mô phỏng Machado 2009 + ΔE cặp màu) | mục 3 |
| Nhạc | thay bản preview M2-MUS-1 bằng bản tải đầy đủ CC BY 4.0: Kevin MacLeod **"Immersed"** (nền) và **"Reawakening"** (cảnh kết đoạn 19) — RIGHTS M3-MUS-1/2. **Bắt buộc ghi công** trong mô tả YouTube và credit phim | toàn tập |

## 5. Shot đã thay (giới hạn chủ dự án: giữ e01b, e01c, e19a)
| Shot gốc → shot thay | Khung | Lý do | Giờ máy tiết kiệm |
|---|---|---|---|
| e01e (bọc s05) → e01n2 (cận trung ngọn đèn vừa thắp) | 168 | Khung gốc tối, tường đen chiếm tiền cảnh; đèn vừa thắp hợp câu "But her job was real…" | −206 s (tốn hơn) |
| e01f (bọc s24, Cas ở xa) → e01n3 (hàng đèn khí cạnh cột điện chưa bật) | 120 | s24 là cảnh đêm có sao, lệch với chạng vạng của đoạn 01; trùng với e19b | +939 s |
| e01g (bọc s43, thành phố trắng điện) → e01n4 (phố chưa thắp) | 128 | Trái với chạng vạng đầu tập; trùng ảnh kết e19d | −256 s |

- **Ròng: +477 s ≈ 8 phút máy.** Lý do chính của các lần thay là liền mạch hình, không phải giờ máy: khung có nhân vật đo thật chỉ 6–7 s, không phải ≈ 14 s như đã ước. Chủ dự án có thể chọn trả lại shot gốc.
- Ba shot bắt buộc render đủ, có nhân vật:
  - e01b (Ida vác thang, lần xuất hiện đầu);
  - e01c (sào mồi chạm, đèn số một bừng);
  - e19a (Ida thắp ngọn thứ hai).
- Thời lượng STORY không đổi.

## 6. Lỗi P phát hiện sau xưởng và đã sửa
1. **Máy quay trôi cộng dồn (STORY-2):** với shot dùng máy gốc tĩnh, độ "trôi" cộng thêm sau mỗi khung.
   - e01b (đoạn 01, 7,7–9,9 s): máy xuyên vào khối nhà.
   - e04c (đoạn 04): đồng hồ quảng trường trôi khỏi khung 3,5 s, chỉ còn trời trống.
   - e04d: máy xuyên tường. e04b: lệch dần.
   - **Judder không bắt được** lỗi này vì khung vẫn thay đổi liên tục; P chỉ thấy khi xem khung.
   - **Sửa:** trôi máy tính từ vị trí gốc mỗi khung (commit `bada6bc`); render lại 4 shot (378 khung) và ghép lại đoạn 01, 04. Đoạn 19 không dính lỗi.
   - **Đề xuất:** thêm luật đo "máy xuyên hình học" (ví dụ tỷ lệ điểm ảnh gần mặt phẳng gần) vào yêu cầu gửi K.
2. **Tiến trình render treo** (TODAY) từ lúc đĩa đầy, chạy 1 giờ 25 phút chiếm CPU, không ghi tệp: P dừng.
3. **Thoại Ida thu nóng:** đỉnh +7 dBTP trước limiter. P chuẩn riêng về −18 LUFS và nén nhẹ; trước limiter còn −2,6 dBTP.

## 7. Đĩa và bàn giao (CHUAN-KENH §6)
- **Sự cố 12:38:** đĩa phiên đầy (5 worktree + FFV1 lát cắt). P dọn được 12 GB; đổi trung gian sang H.264 crf 10 yuv444p. Hai render đầu của TODAY và HISTORY hỏng và đã chạy lại.
- **Hạn mức đĩa** ≈ 40 GB. Ngưỡng dừng render mới là < 6 GB; sau sự cố chưa lúc nào chạm ngưỡng.

**Mức đĩa trống thấp nhất theo khối:**

| Khối | Trống thấp nhất |
|---|---|
| STORY tấm nền | 9,8 GB |
| STORY-2 04 / 19 / 01 | 9,7 / 12 / 14 GB |
| HISTORY 06 / 07 | 9,8 / 9,4 GB |
| TODAY | 9,2 GB |
| Toàn đợt sau sự cố | **8,6 GB** (14:01) |
| Lúc ghép | 15–16 GB |

**Dung lượng đo thật:**
- trung gian đồ hoạ ≈ 147–160 MB/phút;
- trung gian cảnh truyện ≈ 520–600 MB/phút;
- tổng trung gian 16 đoạn ≈ 2,6 GB;
- master crf 16 **840,7 MB**, cao hơn ước 0,63 GB: hạt giấy và nhiễu khó nén. Đã cập nhật tham chiếu ≈ 85 MB/phút.

**Worktree và tệp tạm:**
- tối đa 3 worktree cùng lúc; đã gỡ cả 4 worktree xưởng sau khi lưu bản vá;
- tấm nền br10 và s03 đã xoá;
- **trung gian `sec/` (≈ 2,6 GB) và clip shot STORY (≈ 1,1 GB) đang GIỮ** để sửa lẻ shot. Xoá khi chủ dự án duyệt master.

**Bản vá mã:** các nhánh xưởng chỉ có ở máy cục bộ; bản vá đã lưu vào repo:
- `reports/m3/m2-2b/ma/ma-story-bada6bc.patch`
- `reports/m3/m2-2b/ma/ma-history-a8b0ae8.patch`
- `reports/m3/m2-2b/ma/ma-today-82cdc61.patch`
- Áp từng bản bằng `git apply --binary` lên `lat-cat-m22a`.

**Bàn giao:** không dùng GitHub Release. Ba phần bản xem nằm trong git; master ở ngoài git, có SHA-256 ở mục 1.

## 8. Giờ máy và token
| Khối | Khung | Giờ máy (đo) |
|---|---|---|
| Cảnh truyện: tấm nền br10 + s03 | 468 | ≈ 1,6 h |
| Cảnh truyện: 01, 04, 19 (+ khung thử) | 2 320 | ≈ 4,2 h (có nhân vật: TB 9,3 s/khung; không nhân vật: 3,5 s/khung) |
| P render lại 4 shot | 378 | ≈ 0,5 h |
| Đồ hoạ HISTORY | 5 238 | ≈ 1,3 h (TB 0,90 s/khung) |
| Đồ hoạ TODAY | 6 760 | ≈ 1,5 h (TB 0,61–0,86 s/khung) |
| Mã hoá master + 3 phần (2 lượt) | 14 318 | 0,44 + 0,61 h |
| Mix, judder, đo | — | ≈ 0,2 h |
| **Tổng** | | **≈ 10,3 giờ máy.** Chạy song song trên 4 vCPU dùng chung, đồng hồ thực ≈ 5–6 giờ cho phần render |

- **Tiêu chí 3** (một tập trong một chu kỳ tuần): **đạt** về giờ máy.

**Token (bộ đếm harness):**

| Gói | Token | Hạn | Lệch |
|---|---|---|---|
| STORY | 170,6 nghìn | 180 nghìn | trong hạn |
| STORY-2 | 196,8 nghìn | 180 nghìn | +9 % |
| HISTORY | 328,2 nghìn | 200 nghìn | **+64 %** |
| TODAY | 249,3 nghìn | 180 nghìn | **+38 %** |
| **Cộng xưởng** | **≈ 945 nghìn** | | |
| P | ≈ 150–200 nghìn (ước, không đo được chính xác) | | |
| **Animatic v3** | **≈ 1,1 triệu** | ước đầu việc 0,7 triệu | **vượt ≈ 57 %** |

- Lý do vượt: sự cố đĩa (render lại, đổi luồng ghi); rà khung kỹ cho luật ≤ 3 s; gói STORY phải tách hai.
- Tính theo phút phim: 1,1 triệu / 9,94 phút ≈ **0,11 triệu/phút**. Cộng kịch bản v3 (0,18 triệu) và lát cắt (≈ 0,23 triệu) → ≈ 0,15 triệu/phút. **Tiêu chí 2 (≤ 0,3 triệu/phút): đạt.** Số đầu tiên đo trên cả tập.

## 9. Điểm yếu P thấy, chưa sửa (đề xuất làm ở M2.2)
1. **Bản đồ London (02) và Paris/Opéra (05)** còn trừu tượng: lưới đường gấp khúc, khó đọc ra thành phố.
2. **Cuối đoạn 09:** hai bảng thu còn 60 % nên chữ trên bảng rất nhỏ. Tương phản được đo lúc bảng còn đủ cỡ.
3. **e04b:** cuối shot, đồng hồ bỏ túi bị cắt một nửa ở mép khung (theo chuyển động của tay trong shot nguồn).
4. **e19a (shot bắt buộc c):** Ida thắp ngọn thứ hai ở cỡ xa, hình người nhỏ trên khung.
5. **"Pall Mall"** Bill đọc theo kiểu Mỹ ("Paul Mall"). Nếu muốn cách đọc Anh ("pal-mal"), cần thu lại câu này với phiên âm hoặc thẻ phát âm.
6. **Shorts 9:16** (S1–S4) chưa dựng.
7. Chưa kiểm mù với người xem.

## 10. Chờ chủ dự án
1. **Duyệt animatic v3:** xem `screening/ll-ep01-animatic-v3-p1/p2/p3.mp4`.
2. **Chữ trên hình mới** do xưởng đặt (đoạn 02–18), danh sách trong `BAO-CAO-XUONG-HISTORY.md` và `BAO-CAO-XUONG-TODAY.md`.
3. **Quyết định sáng tạo của xưởng:**
   - cột Telephone operators ở 14;
   - bàn tay gạch sửa ở 16;
   - ba chi tiết thêm ở 18;
   - thanh expected nét đứt ở 17;
   - hai màu ở 15;
   - thiết kế văn phòng mới;
   - dáng người thắp đèn vô danh và viền 2,75 px;
   - chạng vạng muộn ở 19;
   - hai đốm hổ phách ở e19d (quầng tắt depthTest);
   - tư thế Cas giữ thang;
   - thẻ kết DejaVu Serif Bold 80 px.
4. **Ba shot thay ở đoạn 01** (mục 5): giữ hay trả lại shot gốc.
5. **Nhạc:** Kevin MacLeod CC BY 4.0, bắt buộc ghi công.
6. **Yêu cầu gửi K** (giữ nháp tới M2.3): luật judder, cộng đề xuất luật "máy xuyên hình học" (mục 6).
7. Sau duyệt: xoá trung gian (≈ 3,7 GB) và mở M2.2/M2.3.
