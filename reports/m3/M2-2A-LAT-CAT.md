# M2.2a — LÁT CẮT HOÀN CHỈNH "The Last Lamplighters" (đoạn 10–13 kịch bản v3.1) · 01/10/2026

Kênh Last Lamplighters, Mốc 2. Chủ dự án giao lát cắt hoàn chỉnh trước khi sản xuất cả tập (AUTHORSHIP 01/10/2026).
- **P (LL-P, nhánh `ccr-a27221d7-0iwsne`):** thu giọng Bill, giao xưởng, kiểm lại trên chính tệp, sửa 3 lỗi hình, ghép, báo cáo.
- **Xưởng:** nhánh cục bộ `lat-cat-m22a` (từ `thu-phong-cach` @49df834), không push. Bản vá: `reports/m3/m2-2a/ma-lat-cat.patch` (`git apply --binary` lên 49df834).
- Mọi số dưới đây **đo trên chính tệp cuối**, P đo lại sau xưởng.

## 1. Sản phẩm
| Tệp | Thông số | Dung lượng | SHA-256 |
|---|---|---|---|
| `screening/ll-ep01-lat-cat.mp4` (bản xem 1080p, trong git) | 1920×1080, 24/1 CFR, H.264 High crf 18 (maxrate 7 Mb/s), bt709; AAC 48 kHz 256 kb/s; **93,75 s** | 62,9 MB | 87e55761…4cb4b2 |
| `screening/ll-ep01-lat-cat-720p.mp4` | 1280×720, crf 19, maxrate 2,8 Mb/s | **25,7 MB** (giới hạn 40 MB) | 099b8117…7f9940 |
| Master 1080p crf 16 (ngoài git) | `/var/tmp/cine-out/m22a/ll-ep01-lat-cat.mp4` trên container | 98,2 MB | c026812b…7d84d4 |
| Phụ đề `reports/m3/m2-2a/ll-ep01-lat-cat.en.srt` | 25 cue từ mốc ký tự ElevenLabs; không cháy vào hình | | |
| Khung đại diện `reports/m3/m2-2a/khung/*.jpg` | 0,5 · 6,6 (chuyển G0→G1) · 11,7 (G1) · 35 (G3, −34 %) · 60 (G4) · 80 (G5) · 92,2 (G6) s | | |

Master > 30 MB nên không gửi qua giao diện. Bản xem 1080p trong git dùng crf 18 để dưới trần 90 MB của repo.

## 2. Nội dung và cách dựng
**Lời dẫn:** đúng §9.2 kịch bản v3, 1 149 ký tự, một lượt Bill liền mạch. Hai câu sửa ở v3.1 nằm ở đoạn 14, ngoài lát cắt.

| Mã | Thời điểm | Nội dung |
|---|---|---|
| G0 · STORY | 0–7 s | Shot mới `br10` (three.js, cờ b3v3, render đủ 180 khung). Đèn khí đầu tiên của Ida ở tiền cảnh; máy nâng chậm (smootherstep); sau phố hiện khối văn phòng cửa sổ trắng lạnh. Không có người, không cận mặt. **3 lớp parallax** (cột đèn 8 m · mặt tiền 6–26 m · văn phòng 70 m), sương theo độ sâu, quầng rung ±3 %, ≈ 420 hạt bụi trong vùng sáng |
| Chuyển G0→G1 | 6,0–7,55 s | Quầng đèn co thành chấm hổ phách, bay theo đường cong thành điểm 1950 của đường thang máy; motion blur khung con |
| G1 · HISTORY | 7–13 s | Người vận hành thang máy 97k → 77k → 37k. Nét liền, nhãn "ACTUAL · U.S. Census · persons", trục từ 0, chú thích "occupation definitions revised in 1960 and 1970" |
| G2–G3 · TODAY | 13–38 s | G1 rời khung, lật giấy sang khung mới. 5 cột dự báo BLS 2025–35 (gạch chéo, viền nét đứt, "PROJECTION 2025–35 · BLS · jobs"), trục 0 → −40 %. **−34 % đứng ≈ 18 s** |
| G3b | 38–45 s | "Not the same technology. The same pattern…": biểu tượng cửa thang nối tới hàng typists, chữ "same pattern" |
| G4 | 45–68 s | G3 thu nhỏ góc trái; khung "BLS projections that name AI", nhãn kỳ khác màu "PROJECTION 2023–33", cùng thang 0 → −40 % |
| G5 | 68–88 s | Trục biến hình liền sang −40 → +45 %; hai nhóm kỳ (2023–33 và 2025–35) tách bằng khe và nhãn |
| G6 | 88–93,75 s | "end · change · new" đặt trên ba nhóm; ánh rọi lướt qua; mờ về đen |

**Kỹ thuật:**
- **Đồ hoạ:** canvas2D trong Chromium, vẽ lại mỗi khung, t = khung/24, toạ độ điểm ảnh con, easing, motion blur khung con (4 mẫu) ở 4 cửa sổ chuyển cảnh nhanh.
- **Chất giấy B3:** giấy ngà có vân, mép xé, bóng đổ theo ánh rọi; ánh rọi ấm lướt chậm; giấy lay ±1,6 px / ±0,12°; bụi.
- **Âm thanh:**
  - lời Bill nguyên bản, chỉ highpass 70 Hz và nén 3:1;
  - nhạc M2-MUS-1 hạ 12 dB khi có lời;
  - 3 SFX CC0 (M2-SFX-1…3), fade 8 ms;
  - master về −14 LUFS rồi limiter nâng mẫu ×4.

## 3. Số đo (đo thật trên tệp cuối)
| Chỉ số | Chuẩn | Bản xem 1080p | 720p | Master |
|---|---|---|---|---|
| **Judder** (`scripts/p/judder.py`, framemd5): đoạn đứng 2–12 khung | 0 | **0** | **0** | **0** |
| Đoạn giữ 13–23 khung / ≥ 1 s / giây < 12 khung mới | — | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| Loudness tích hợp | −14 LUFS | **−14,1** | −14,1 | −14,1 |
| True peak | ≤ −1 dBTP | **−1,6** | −1,6 | −1,6 |
| LRA | — | 1,7 LU | 1,7 | 1,7 |
| Nhạc hạ khi có lời | 10–14 dB | **12,0 dB** (đường bao); RMS đo 12,2 dB | | |
| Im số tuyệt đối (−90 dB, ≥ 50 ms) | 0 | — | — | 0 |
| Tương phản chữ thông tin thấp nhất | ≥ 4,5:1 | **5,95:1** ("37k", G1) | 5,34:1 (dòng nguồn 2, G5) | 5,96:1 |

- **Mốc so judder:** animatic M2.1 có 799 đoạn, chiếm 16,96 % thời lượng.
- **Giọng:** whisper (small.en) so với văn bản: khớp 100 %, chỉ khác cách ghi số ("thirty-four percent" ↔ "34"). Không cụt chữ.
- **ElevenLabs:** một lượt, gửi 1 149 ký tự. Bộ đếm **3 143 → 3 649 (+506)**; đọc lại sau ≈ 1 giờ vẫn là 3 649. Bộ đếm tăng ít hơn số ký tự gửi, giống hiện tượng đã ghi ở PLAN-HANDOFF §6. Gói Creator, hạn 144 034. Dùng **≤ 3 000 ký tự** theo hạn.

### Giây render/khung (tách riêng)
| Loại | Mean | Max | Ghi chú |
|---|---|---|---|
| **Cảnh truyện** `br10` 1080p (three.js b3v3) | **1,74 s** | 10,24 s (khung đầu, khởi động; bỏ khung đầu: 1,69 / 2,35 s) | 180 khung, 313 s. Không nhân vật, một đèn đổ bóng. **Tham chiếu có nhân vật: s22 b3v3 13,1 s/khung** |
| **Đồ hoạ dữ liệu** 1080p (canvas2D, mỗi luồng) | **0,42–0,57 s** theo đoạn | 1,52 s (đoạn có khung con motion blur) | 2 250 khung; 3 luồng song song: wall ≈ 7,5 phút cho 93,75 s |
| Mã hoá | master 240 s · bản xem 229 s · 720p 141 s | | cho 93,75 s phim |

## 4. Ước cả tập (theo tỷ lệ 20/35/45, kịch bản v3.1)
**Thời lượng ước ≈ 10:30 (630 s).** Bill đọc đoạn nhiều số chậm ≈ 124 từ/phút, so với 141,2 từ/phút đo trên văn xuôi; trần mới là 11:00. Số thật đo ở animatic v3.

| Phần | Giây | Khung | Giờ máy |
|---|---|---|---|
| STORY 20 % | 126 | 3 024 | 1,5 h (kiểu br10) … **11,0 h** (kiểu s22, có nhân vật); một tiến trình |
| HISTORY 35 % + TODAY 45 % (đồ hoạ, bản đồ) | 504 | 12 096 | ≈ 1,7 h CPU-luồng, ≈ 0,6 h wall (3 luồng) |
| Mã hoá 3 bản + đo | 630 | — | ≈ 1,2 h |
| **Tổng** | | | **≈ 3–13 h máy** |

- **Tiêu chí 3** (một tập trong một chu kỳ tuần): giờ máy **đạt** với dư lớn. Giới hạn thật là token và vòng duyệt của chủ dự án.
- **Tiêu chí 2** (≤ 0,3 triệu token/phút):
  - **Lát cắt:**
    - xưởng **184,0 nghìn** (bộ đếm harness);
    - P ≈ 35–45 nghìn (ước, không đo được chính xác);
    - tổng ≈ **220–230 nghìn cho 1,56 phút ≈ 0,14–0,15 triệu/phút** → đạt.
  - **Ước cả tập:** ≈ 0,10–0,15 triệu/phút. Phần dựng bộ máy đồ hoạ là chi phí một lần; mỗi đồ hoạ mới vẫn cần mã riêng. Kịch bản v3 (176,7 nghìn) chia cho 10,5 phút ≈ 17 nghìn/phút. **Đây là ước tính, chưa đo**; số thật có ở animatic v3.

## 5. P kiểm và sửa sau xưởng
Xem khung 1080p, P phát hiện và tự sửa 3 lỗi (commit `3f69e79` trên `lat-cat-m22a`; render lại 2/3 đoạn đồ hoạ):
1. **Luật so sánh điểm 5 (ngụ ý sai):** ở G5, tiêu đề "BLS projections that name AI", câu trích MLR và nhãn "PROJECTION 2023–33 · earlier round" vẫn nằm trên khung khi các nghề tăng kỳ 2025–35 hiện ra. Người xem dễ đọc thành "BLS gắn nurse practitioners/solar/data scientists với AI".
   - **Sửa:** ba phần tử này mờ đi khi trục biến hình; tiêu đề mới "Projected change in selected U.S. jobs".
2. **Tương phản:** chữ trong bản thu nhỏ G3 (mờ 40 %) chỉ đạt 2,05:1.
   - **Sửa:** bản thu nhỏ chỉ giữ hình cột và biểu tượng, không còn chữ. Đây cũng là câu hỏi Q1 của xưởng, nay không cần chủ dự án quyết.
3. **Chồng lấn:** nhãn "PROJECTION 2025–35 · newest" đè chữ "Nurse practitioners"; hộp "new" đè nhãn đó.
   - **Sửa:** dời cả hai.

Judder, loudness và tương phản ở mục 3 đo **sau** khi sửa.

## 6. Chỉ số trong ±5 % quanh ngưỡng (nêu tên theo luật)
- **Thời lượng 93,75 s:** vượt trần cũ 90 s 4,2 %; trong mức "tới ~95 s" chủ dự án cho phép (cách 95 s là 1,3 %).
- **Loudness −14,1 LUFS:** lệch đích −14 là 0,7 %, tức là đạt đúng đích.
- **Token gói kịch bản v3:** 176,7 / 180 nghìn (98,2 %).
- **Token lát cắt vượt hạn:**
  - xưởng 184,0 nghìn so với hạn P giao 150 nghìn (+23 %);
  - cả lát cắt ≈ 220–230 nghìn so với hạn 200 nghìn (**vượt ≈ 10–15 %**).
  - Lý do chính: dựng bộ máy đồ hoạ động từ đầu, và P sửa sau xưởng.

Các chỉ số khác nằm ngoài vùng ±5 %:
- TP −1,6 dBTP;
- tương phản thấp nhất 5,34:1 (cách ngưỡng 4,5:1 là 19 %);
- 720p 25,7 MB (64 % của 40 MB);
- bản xem 1080p 62,9 MB.

## 7. Điểm yếu P thấy, chưa sửa (đề xuất làm ở animatic v3 / M2.2)
1. **Khối văn phòng G0** là lưới cửa sổ đều, sáng phẳng, phủ gần kín trời. Đọc giống "phông nền" hơn là toà nhà xa. Sương theo độ sâu chưa ăn vào khối này.
   - **Đề xuất:** cửa sổ sáng không đều (tắt/bật ngẫu nhiên, vài ô ấm); thấp hơn và xa hơn; sương phủ dày hơn ở 70 m.
   - Chi phí: chỉ render lại G0 (≈ 5 phút máy).
2. **Chữ "end · change · new" (G6)** đặt hộp nổi giữa khoảng trống, chưa bám chặt vào nhóm cột. Có thể gắn nhãn sát mép nhóm.
3. **Bóng s03/s05** (viền 2,5–3 px) chưa áp, vì lát cắt không chứa shot người thắp đèn trên tường. Làm khi dựng các shot này ở animatic v3.
4. **Nhạc M2-MUS-1** là bản preview HQ mp3. Nhạc chốt cần bản gốc hoặc nhạc khác (CC0/CC BY do người làm).
5. Chưa kiểm mù lát cắt (ngoài phạm vi). Đề xuất kiểm mù 1 dải (lát cắt + đối chứng) nếu chủ dự án muốn có số khách quan trước khi sản xuất.

## 8. Câu hỏi cho chủ dự án
- **Q2 (xưởng nêu):** duyệt các chữ do xưởng hoặc P đặt trên hình, kịch bản chưa ghi sẵn:
  - "Elevator operators, United States";
  - "Fastest-shrinking U.S. jobs";
  - "BLS projections that name AI" + câu trích MLR nguyên văn "expected to primarily affect occupations whose core tasks can be most easily replicated by GenAI";
  - "word processors and typists, 2025–35";
  - "PROJECTION 2025–35 · newest";
  - "Projected change in selected U.S. jobs" (P đặt).
- **Q3 (xưởng nêu):** ngọn đèn tiền cảnh là L10 của bộ phố Last Round; khối văn phòng là hình mới, thủ tục. P không thấy luật world-rules nào cấm văn phòng hiện đại ở hậu cảnh trong kênh mới, nhưng **cần chủ dự án xác nhận** đây đúng là hình ảnh "the office lights" mong muốn.
- **Duyệt lát cắt** → mở animatic v3 (giọng Bill thật cả tập, đo thời lượng thật, ≤ 11:00).

## 9. RIGHTS
- Thêm M2-VO-1 (lời Bill lát cắt), M2-SFX-1 (#320149 OwlStorm), M2-SFX-2 (#159386 clairinski), M2-SFX-3 (#470189 Atrius1), M2-GFX-1 (đồ hoạ tự tạo).
- Ba SFX: xưởng và P đều kiểm trên trang Freesound là "Creative Commons 0".
- Nhạc: M2-MUS-1 (đã có).

## 10. Dựng lại
1. `git apply --binary reports/m3/m2-2a/ma-lat-cat.patch` lên `thu-phong-cach` @49df834.
2. Liên kết `node_modules`.
3. `design/m3/lat-cat/run_story.sh` → `run_dohoa.sh` → `am_thanh.py` → `ghep.sh` → `do.sh`.
- Lời dẫn: `reports/m3/m2-2a/vo/bill-lat-cat-take1.mp3` + `.align.json`.
- Mix: `reports/m3/m2-2a/mix.json`.
