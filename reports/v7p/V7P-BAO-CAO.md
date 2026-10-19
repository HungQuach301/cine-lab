Nhánh thật: `ccr-f96ee5b5-2ec2i5` (harness buộc tên này). Lệnh yêu cầu `v7-pilot` — mọi commit cũng đã đẩy sang `origin/v7-pilot` (cùng SHA). Gốc: `origin/ccr-6189ede9-lpjwe0` @b9cff40e (G1b). Không merge. Không sửa `loi-khoa.txt` (SHA 0fdc72ce… kiểm lại khớp), `checks/`, `docs/`, `main`.

# V7-PILOT T3 Gibraltar — BÁO CÁO: bản thử ≈ 2 phút theo ngữ pháp "timelapse làm xương sống"

## §0 Tóm tắt

| Việc | Kết quả |
|---|---|
| 1. Điểm máy | **8 điểm** A–H (`design/k2v/tl/data/diem-may-v7.json`), bảng **74 shot cũ → 42 shot mới** cả tập (`reports/v7p/diem-may.md`). Dự kiến cả tập: timelapse góc cao **93,5 %**, khung neo 5,9 %, lướt thấp 0 %, **3,47 cắt/phút**, shot TB **17,3 s**. |
| 2. Bộ máy timelapse | `design/k2v/tl/tl7.js` + cảnh `scenes/t3tl.js`: thời gian **liên tục** theo đường cong (tua ngược được), vật có ngày (mọc/cháy/sập/rút), ngày–đêm thật, **đêm có đèn** (đèn đường, đèn đường băng, cửa sổ sáng), khói theo sự kiện, **đường băng mọc qua đường rồi lấn vịnh**, phố 1781 **sập dần** thành "RUINS". Một shot = (điểm máy, đường cong thời gian). |
| 3. Eo đất có nguồn | Trại vây hãm 1779–83 **số hoá từ Faden 1783**, đối chiếu Drinkwater 1786 ("CAMP of the ALLIES"); công sự tiền phương (ghost SH); Línea 1730–35 mọc tây → đông; 14 mốc vây hãm; cờ Borgoña → Union 1704; hàng rào 1909. Nguồn + bậc ghi trong `eo-dat-v7.json` và log. |
| 4. Bản thử | **8 shot, 119,1 s**, 540p. Bản xem trong git `reports/v7p/ban-thu/v7p-xem.mp4` (640×360, 2,74 MB). Bản 540p có ray lời ngoài git (SHA §4). |
| 5. Tự đo | Góc cao có thời gian chạy **100 %** · lướt thấp **0 %** · khung neo **0 %** · **4,03 cắt/phút**, shot TB **14,9 s** · khung "trống" **0/60** (đất trống lớn nhất 46,2 %) · tấm chữ **3,0 s** (chỉ thẻ chương) · 1080p **4,9–12,5 s/khung**. |
| 6. Xem câm | 3 người chấm AI: **11/24** (P đọc lại; chấm từ khoá cho 17/24). Q2 "1779 bắt đầu gì" 6/6, Q1 "ai giữ Rock" **0/6**. Độ rõ 2,0/5. |
| 7. Tờ so | `reports/v7p/so/to-so-8-cap.jpg` (8 cặp G1b ↔ bản thử cùng câu lời). |
| Chi phí | Claude API **$0,230** · OpenAI **$0** · ElevenLabs 0 · YouTube 0 · giờ máy ≈ **4,3 h** đồng hồ bận máy. |

**Xem nhanh:** bản xem `reports/v7p/ban-thu/v7p-xem.mp4` · tờ so `reports/v7p/so/to-so-8-cap.jpg` · 6 khung cổng `reports/v7p/khung/cong-*.png` · chuỗi xem câm `reports/v7p/xem-cam/to-1.jpg`, `to-2.jpg` · bản xem lượt 1 để so `reports/v7p/ban-thu/v7p-xem-luot1.mp4`.

## §1 Điểm máy (việc 1)

| Điểm | Chỗ đứng | Dùng ở bản thử | Năm quay lại (cả tập) |
|---|---|---|---|
| **A** | Bắc, đồi Campamento (cao 205 m) nhìn nam qua dãy trại tới eo đất + Rock | C1 | 1704 · 1730 · 1779 · 1783 · 1810 |
| **B** | Vịnh, tây-bắc phố (cao 250–300 m) nhìn phố + Old Mole + Line Wall | H2, C4 | 1704 · 1780 · 1782 · 1943 · bookend 2026 |
| **C** | Sườn tây trên Grand Parade / King's Bastion (cao 300 m) | C3, C5 | 1704 · 1780 · 1781 · 1782 |
| **D** | Mép nam La Línea, nhìn nam qua cổng + đường băng (cao 320 m) | H1, H3 | 2026 đêm · 1934 · 1939–43 · 1969 · 2026 |
| **E** | Phía Algeciras, trên vịnh, tele | C2 | 1779 |
| F, G, H | Catalan Bay / đỉnh Rock nhìn bắc / phố La Línea | — | ch.1, 3, 4, 5 |

- Toạ độ, hướng, FOV (tiêu cự tương đương 25–45 mm) và bảng đầy đủ 74 → 42 ở `reports/v7p/diem-may.md`.
- **Rủi ro nêu tên:** điểm D chiếm 193,5 s = 26,6 % cả tập (luật BAI-HOC #96: một bối cảnh ≤ 25 %). Đề xuất chuyển N5.2 sang H → 24,8 %.
- Điểm A và E phải đặt trong hộp địa hình chi tiết của gói (N ≤ 4 400, E ≥ −6 500). Ngoài hộp, máy thấy mép khối DTM (hộp nâu ở C2 lượt đầu) hoặc cây nổi.

## §2 Bộ máy timelapse (việc 2)

**Thời gian.** `tl7.timeline(keys)`:
- Mốc = (giây cảnh, ngày giờ hoặc năm thập phân, kiểu mặt trời, kiểu nhãn).
- Nội suy JD bằng Hermite đơn điệu (Fritsch–Carlson): không vượt mốc; đảo chiều mượt khi tua ngược; mốc `hold` dừng êm.
- Đoạn chạy nhanh khai giờ mặt trời cố định → không nhấp nháy ngày–đêm. Đoạn chậm dùng mặt trời thiên văn thật (`sun.js`).
- Bộ đếm tự đổi dạng theo đoạn: năm / tháng / ngày / ngày-giờ.

**Vật có ngày.** `win(Y, {on, full, off0, off1})` → mọc 0..1 rồi rút. Áp cho:
- Línea (mọc từng đoạn tây → đông).
- Công sự tiền phương (rãnh + ụ đất mọc dọc tuyến).
- Trại: lều hiện dần; 35 % số lều theo cửa sổ 1779, phần còn lại theo cửa sổ 1782. Dải đất giẫm dưới trại.
- Hàng rào 1909 (cọc + lưới mọc dọc ranh).
- Cờ, tàu/hạm đội (đường đi theo năm), đám người theo cửa sổ năm.
- Khói: khi đường cong đi qua năm sự kiện, khói phát theo **giây cảnh**. Lượt 1 có lỗi khói pin nổi bật lúc đang tua ngược; đã sửa bằng cách tính mọi khoảng giây mà năm nằm trong cửa sổ.

**Phố theo năm.**
- Gói OSM/Catastro mọc theo năm xây (shader `aYear` sẵn có), cùng ghost 1704 và c.1880/1900.
- Cửa sổ 1779–1783,6 thay bằng phố Drinkwater 1786.
- Vùng "THE RUINS" còn nguyên tới 12/4/1781, rồi sập theo 8 nhóm tới giữa 6/1781 (ngày từng nhóm là **ước tính**).
- 5 nhà gần Spanish Church cháy đêm 13→14/4/1781 rồi sập (S063: 4–5 nhà; vị trí ước tính).

**Đường băng.** Cờ `uRecl` trong `terrain.js`/`heroes.js` (mặc định tắt → cảnh cũ không đổi):
- Mặt cứng mọc từ đầu đông (cuối 1939, S091) qua đường (1941).
- Đất lấn vịnh + đường băng kéo ra tây tới 7/1943 (S092).

**Đêm** (`page.js`, `water.js`, `city.js`; đều tắt mặc định):
- Ánh trăng/ánh trời đêm từ hướng cố định; trời và nước tối dần.
- Đèn đường dọc đường OSM (cách 30–38 m), đèn mép đường băng ICAO (≤ 60 m), đèn ngưỡng.
- Cửa sổ sáng ≈ 45 % (chỉ khi năm ≥ 1950). Quầng lửa cho pin nổi và nhà cháy.
- Không sinh ảnh đêm bằng AI.

**Máy.** Điểm cố định, trôi tuyến tính p0 → p1. Đo bằng `driftPct`: **0,06–0,38 % khung/s** (trần TL-1: 2 %).

**Công cụ.**
- `v7p/mk_ep_v7p.py`: đặc tả.
- `scripts/k2tl/v7p_dung.sh`: một lệnh dựng.
- `v7p_probe.py`: soi khung.
- `v7p_do.py`: tự đo.
- `v7p_so.py`: tờ so + chuỗi câm.
- `v7p_cam.py`: xem câm.
- `v7p_diem_may.py`: kế hoạch điểm máy.
- `v7p_eo_dat.py`: dữ liệu eo đất.
- `v7p_cache.sh`: bộ đệm.
- Thẻ chương: `p.chuong` trong `scripts/k2/lib/k2.js` (góc dưới trái, trên bộ đếm, ≤ 3 s).

## §3 Nội dung eo đất 1730–1783 + nguồn/bậc (việc 3)

| Vật | Hình học | Ngày | Nguồn | Bậc / sai số |
|---|---|---|---|---|
| **Trại TBN 1779–83** (7 dãy) + **trại Pháp 1782** (1 dãy) | Dải trại số hoá tay trên **Faden 1783** (Yale 2046612, PD), lưới 10 px. Phép đồng dạng 3 điểm khống chế của SH (RMS 12,5 m trong vùng). Sâu ≈ 100 m (14 hàng lều × 7 m), ≈ 9 000 lều đủ trại | lập 13/7 → đủ 10/1779 (S041, S048); thêm 1782 (S049, S065); rút 3/1783 (S045–47) | Faden 1783; đối chiếu **Drinkwater 1786 Chart of the Bay** ("CAMP of the ALLIES", "E The Old Camp", cùng chỗ: giữa Point Mala và Buena Vista) | vị trí bậc 1, **sai số ≤ 250 m** (ngoài vùng khống chế; Point Mala lệch ≈ 250 m so bờ DEM). Số lều bậc 2 (≈ 14 000 / 40 000 quân) + bậc 5 (≈ 6 người/lều). Hình lều bậc 4. Ngày đầu/cuối: ước tính |
| **Công sự tiền phương** | lines1782_tp + fort1782_tp (ghost SH) | đang đào 12/9/1779 (S043) → đủ 12/4/1781 (S062) → rút 2–3/1783 | Drinkwater 1786 Plan of the Batteries, đối chiếu Faden 1783 | bậc 1, do_tin **thấp**, sai số ≥ 160 m; ngày nội suy (ước tính) |
| **Línea de Contravalación** | ghost SH T1782-01 (do_tin cao) | 1730 → 1735; phá 14/2/1810 | Drinkwater 1786; TIEN-KY T3; lời ch.3 | bậc 1 (4–23 m) |
| **14 cuộc vây** (nhịp khói) | lâu đài Moor + phố + Line Wall | năm giữa mỗi cuộc (claims `dem_so_lan_vay`) | Sayer 1862 · Stephens 1870 · GNM · García Sanz 2022 | thời điểm bậc 2; **vị trí khói minh hoạ** |
| **Cờ** | Tower of Homage | Borgoña 1506 → Union từ 4/8/1704; trước 1506 **không cờ** (chưa có nguồn mẫu cờ Castile/Nasrid) | props.js (RIGHTS-V6) | mẫu bậc 3–4; cột minh hoạ. Ở 2 km cờ chỉ còn vài điểm ảnh → xem §6 |
| **Hàng rào 1909** | ranh OSM 2026 | 1909 | lời ch.3 | vị trí ước tính (chưa có bản đồ 1909) |
| **Đám đông / quân** | khối quân V6 trước trại (≈ 1 000 người hiện), lính trên Grand Parade, người hái rau dại trên sườn, dân chạy về nam | theo cửa sổ năm | S048 (quy mô), S052 (hái rau dại, bậc 2), S062 (dân chạy nam) | vị trí khối/lối: minh hoạ (bậc 5) |
| **Danh sách 9/1782** | chỉ mục `dung_duoc` + `correct` (62 mục) | 9/1782 | `reports/nc-ai/aib/danh-sach-9-1782.json` | **Chưa áp vào hình bản thử.** Mọi mục đều thuộc 1–9/9/1782, ngoài dải năm bản thử (21/6/1779 → 14/4/1781) — dùng lệch ngày là trái §12.3. Kế hoạch áp: N2.7 / N2.9 (đội gác Lines 130 lính, King's/Prince's/Queen's Lines 50/50/30) |

Tàu, hạm đội và thuyền (Rooke 1704, Barceló 1779, Rodney 1780, tàu chanh Đan Mạch 1780, Darby 1781, liên quân 1782, 10 pin nổi): ngày theo S054/S055/S062/S065/S066/S074. **Vị trí neo là minh hoạ**, ghi trong `log-shot.json` từng shot.

## §4 Bản thử (việc 4)

| Shot | Điểm | Lời | Giây | Thời gian chạy trong shot |
|---|---|---|---|---|
| H1 | D | 0a + 0b | 12,0 | 18/10/2026 23:52 → 19/10 08:20 (đêm có đèn → bình minh) |
| H2 | B | 0c + 0d + 0e + 0f | 21,0 | 2026 → **tua ngược** 1309 → 14 nhịp vây → 1704 (phố, cờ) → 1779 → 13/9/1782 → **pin nổi cháy đêm** (thấy từ 29,3 s) |
| H3 | D | 0g + 0h | 11,5 | 1938 → đường băng qua đường 1941 → lấn vịnh 1943 → 2026 |
| C1 | A | 2a + 2b | 22,5 | 20/6 → 28/10/1779 (cổng đóng; trại dựng); thẻ chương |
| C2 | E | 2c | 12,0 | 12/7 → 20/12/1779 (hải đội ra hàng chặn; thuyền châu Phi quay lại) |
| C3 | C | 2d + 2e | 14,1 | 14 → 15/1/1780 (một đêm) |
| C4 | B | SM2 + 2f | 13,5 | 1/1780 (đoàn Rodney) → 10/1780 (tàu chanh) |
| C5 | C | 2g | 12,5 | 12/4 09:20 → 14/4/1781 (thả neo 10:45, pháo kích, dân chạy nam, cháy đêm) |

- Lời không đổi. Nhịp 2,5 từ/s và độ trễ đầu câu như G1b. Phụ đề tạm là đường ray (chỉ trên bản xem).
- Không tấm số, không tấm tư liệu, không câu trích trên hình (TL-4). Các trích Montero ở 2b/2c của G1b đã bỏ khỏi hình.
- Dựng 3 lượt:
  - Lượt 1: toàn bản, 57 phút.
  - Lượt 2: toàn bản. Lửa đêm đọc được; nhịp vây lớn hơn; điểm A gần trại; ≈ 60 phút.
  - Lượt 3: riêng C1, máy nhìn thẳng dãy trại; ≈ 25 phút.

| Tệp | Nơi | Cỡ | SHA-256 |
|---|---|---|---|
| Master 960×540 (nhạc tạm, không phụ đề) | ngoài git `/var/tmp/cine-out/k2c-t3-v7p/k2c-t3-v7p-v1-master.mp4` | 121 408 624 B | `3d24da9663ad94cddd0bce0bab6f28d298581301338cb4eabf8816dd9fc87743` |
| **Bản 540p có ray lời** | ngoài git `/var/tmp/cine-out/k2c-t3-v7p/k2c-t3-v7p-540p-ray.mp4` | 35 903 877 B | `980a5fe50fb3963f012cc63d05f6bb6d07e965e097317d66a658954f54d631f0` |
| Bản xem 640×360 có ray | **trong git** `reports/v7p/ban-thu/v7p-xem.mp4` | 2 738 179 B | `2748af61eae2ecf328d3177d96f56379558b3853364b6e14475515ee9683b0df` |
| Bản xem lượt 1 (để so) | trong git `reports/v7p/ban-thu/v7p-xem-luot1.mp4` | 2 683 270 B | `233cc4f7…ed7dd7` |

Tái tạo: `bash scripts/k2tl/v7p_cache.sh` (bộ đệm) → `bash scripts/k2tl/v7p_dung.sh`.

**1080p (đo thật, máy rảnh, 1 tiến trình; `reports/v7p/do/`):**

| Shot | H1 | H2 | H3 | C1 | C2 | C3 | C4 | C5 |
|---|---|---|---|---|---|---|---|---|
| s/khung 1080p | 10,1 | 7,3 | 12,5 | 11,9 | 4,9 | 7,8 | 6,1 | 7,0 |

Cảnh có phố 2026 dày (điểm D) nặng nhất. Ở 540p: 2,0–3,3 s/khung.

## §5 Số đo việc 5 (ghi số, không tự chấm đạt) — `reports/v7p/do/do-v7p.json`

| Chỉ số | Bản thử | Mục tiêu TL | G1b cùng đoạn |
|---|---|---|---|
| Góc cao/toàn cảnh có thời gian chạy | **100 %** (8/8 shot) | ≥ 75 % | — |
| Lướt thấp | **0 %** | ≤ 10 % | — |
| Khung neo | 0 % | — | — |
| Cắt/phút | **4,03** | ≤ 5 | 11,9 (cả tập) |
| Shot TB | **14,9 s** | ≥ 12 s | — |
| Khung "trống" (đất tự nhiên phẳng không vật thể > 60 %, mặt nạ, 1 khung/2 s) | **0/60** | — | — |
| Đất trống trung bình theo shot | H3 30,2 % (max 46,2 %), C1 25,0 % (max 26,4 %), còn lại ≤ 6,3 % | — | — |
| Giây có tấm chữ | **3,0 s** (thẻ chương). Tấm số / tư liệu / trích = 0 | — | — |
| Trôi máy | 0,06–0,38 % khung/s | ≤ 2 % | — |
| Năm/s lớn nhất | H2 **538**, H3 41, còn lại ≤ 0,4 | §10.3: ≤ 20 (crane) | — |

- **Mặt nạ đếm cây/bụi là "không trống"**, nên C1 đo 25 % dù mắt vẫn thấy "đồng cỏ" (xem §6).
- Tỷ lệ lửa đỏ trong khung đêm H2 (luật §10.6 ≤ 15 %) **chưa đo**.

**6 khung cổng PNG sạch 1920×1080** (`reports/v7p/khung/`; chuyển từ JPG q2 của hero.js, không chữ):
- `cong-vay-ham` (C1 cuối)
- `cong-cang` (C4, đoàn Rodney)
- `cong-pho-day` (C3, phố 1780)
- `cong-hero` (H3, Rock + đường băng 2026)
- `cong-toan-canh` (C5, phố + đoàn Darby)
- `cong-bo-chien-su` (H2, pin nổi bắn 13/9/1782)

Chờ điều phối chấm so đối thủ.

## §6 Xem câm HC-2 — `reports/v7p/xem-cam/ket-qua.json`

- **Cách làm:** 3 vai (người xem YouTube tắt tiếng, giáo viên sử, dựng phim), `claude -p` ghim claude-sonnet-5-5, chỉ Read. Mỗi người xem 59 khung (1 khung/2 s, không phụ đề), 2 tờ lưới.
- **Phục vụ thật:** sonnet-5-5 + haiku-5-5 (CLI tự gọi haiku phụ).

| Câu | R1 | R2 | R3 | Tổng (P đọc lại) |
|---|---|---|---|---|
| Q1 Ai giữ Rock | 0 | 0 | 0 | **0/6** |
| Q2 1779 bắt đầu gì | 2 | 2 | 2 | **6/6** |
| Q3 Vì sao đói | 1 | 1 | 1 | **3/6** |
| Q4 Cái gì đến cứu | 0 | 1 | 1 | **2/6** |
| **Tổng** | | | | **11/24**; độ rõ 2,0/5 |

**Lý do cả 3 nêu:**
1. Không thấy cờ/quân phục nên không biết ai giữ Rock. Cờ trên lâu đài ở 2 km chỉ còn vài điểm ảnh.
2. Không phân biệt được tàu cứu viện với tàu địch.
3. Đói không có hình (không người, không kho rỗng).
4. Đoạn tua ngược + 1939–2026 ở mở đầu khó theo khi tắt tiếng. Đoạn này dựa vào lời, đúng thiết kế móc.
5. C1 "~10 khung đồng cỏ, Rock ở xa, chỉ có ngày đổi" (2/3 người nêu).

## §7 Tờ so trước/sau

`reports/v7p/so/to-so-8-cap.jpg`: 8 cặp G1b (bản xem 270p) ↔ bản thử, cùng câu lời 0a, 0d, 0f, 0g, 2a, 2d, SM2, 2g.

| Câu | G1b | Bản thử |
|---|---|---|
| 0d | thẻ "14" | nhịp khói vây hãm trên phố |
| 0f | bản khắc trong khung giấy | 10 pin nổi cháy đêm |
| 2d | thẻ danh sách | phố tháng 1/1780 |
| SM2 | bản đồ chiến lược | đoàn Rodney trong vịnh |

Lệch: cặp 2g lấy ở 113,9 s rơi vào 21:31 (đêm). Câu "opened fire on the town" nói lúc ban ngày (10:45–13:00), nên khoảnh khắc pháo kích trong C5 ngắn (≈ 2,4 s) so với câu lời.

## §8 Giờ máy 1080p ước cả tập theo ngữ pháp mới

- **Cách tính:** s/khung đo ở §4 gán theo điểm máy: D 11,3; A 11,9; B 6,7; C 7,4; E 4,9. G, H tạm như D (nhìn phố dày); F như B.
- Nhân với thời lượng mỗi điểm trong `diem-may.json`:
  - 3D timelapse ≈ **43,8 h**
  - khung neo (6 × ≈ 7 s × 6 s/khung) ≈ 1,7 h
  - lớp 2D + ghép ≈ 2,4 h
  - **Tổng ≈ 48 h một tiến trình** (G1b đo 29,6 h). Lý do tăng: shot dài nhìn phố 2026/1782 dày + đêm có đèn + nhiều tàu.
- **Chia gói:** ≈ **6 gói × ≤ 8 h máy đo** (≤ 10 h máy chậm ×1,25), hoặc 5 gói nếu chấp nhận ≈ 12 h/gói.
- **Chưa đo trực tiếp** G, H, F → sai số ước ±20 %.

## §9 Chi phí thật

| Khoản | Mốc / chặn | Thật | Ghi |
|---|---|---|---|
| Claude API | $8 / $25 | **$0,230** | 3 lượt xem câm (`reports/v7p/xem-cam/cost.jsonl`) |
| OpenAI | $5 / $50 | **$0** | không sinh ảnh |
| ElevenLabs / YouTube | 0 | 0 / 0 | — |
| Giờ máy | 10 h | ≈ **4,3 h** đồng hồ bận máy | bộ đệm 0,1 · soi 0,8 · 3 lượt dựng 2,4 · đo 1080p + mặt nạ 0,9 · xem câm 0,1 |

Chặn an toàn: lỗi cùng loại "C1 nhìn như đồng cỏ" đã đổi máy 3 lần (gần trại, sát trại, nhìn thẳng dãy trại). Theo luật, tôi dừng chỉnh máy và đề xuất đổi cách (§11 D3).

## §10 Chỉ số trong ±5 % quanh ngưỡng (luật cứng)

- **Điểm D = 26,6 % thời lượng cả tập (kế hoạch)** so trần 25 % (BAI-HOC #96). Cao hơn 6,4 % tương đối, sát vùng ±5 %; nêu tên, đề xuất D1.
- Ngoài vùng ±5 % (ghi để rõ, không phải "sát ngưỡng"):
  - cắt/phút 4,03 (trần 5)
  - shot TB 14,9 s (sàn 12)
  - trôi ≤ 0,38 % (trần 2 %)
  - khung trống max 46,2 % (ngưỡng 60 %)
- **Trái luật cũ (không phải sát ngưỡng):** tốc độ năm của H2 (538 năm/s) vượt xa §10.3 (≤ 20 năm/s crane/reveal; ≤ 10 năm/s bay thấp). TL-5 yêu cầu "timelapse nhanh" nhưng chỉ thắng §12.1, không thắng §10.3 → cần chủ dự án quyết (D2).

## §11 Quyết định đề xuất

| # | Đề xuất | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|---|
| D1 | Chuyển N5.2 (13 s) từ D sang H | D về 24,8 % (≤ 25 %) | thêm 1 điểm máy cho ch.5 | ch.5 | — |
| D2 | Cho TL-5 miễn §10.3 cho đoạn tua ngược ≤ 3 s ở mở đầu (và bookend 5j) | giữ "fourteen sieges" thành timelapse | nhấp nháy năm khó đọc khi tắt tiếng | H2, N5.5 | người xem câm thấy "năm nhảy lung tung" (§6) |
| D3 | **C1 (1779) đổi cách kể:** (a) máy thấp hơn, trôi dọc dãy trại ở 200–400 m (dùng hạn mức lướt thấp TL-2 ≤ 10 %, vai "khoảnh khắc người"); hoặc (b) bản đồ Faden 1783 phủ khớp lên địa hình ≤ 3 s khi lời nói "facing the Rock" rồi tan vào trại (TL-4 cho phép) | trại và quân đọc được; giải lỗi "đồng cỏ" (2/3 người xem câm) | (a) dùng 22,5 s × hạn mức lướt thấp; (b) cần thử `phaseMaps` | C1 + N1.4/N2.11/N3.1 cùng điểm A | (a) lều 3 m vẫn nhỏ nếu máy > 400 m |
| D4 | **Đọc phe trên hình:** cờ lớn đúng tỷ lệ ở 3 điểm (Line Wall, lâu đài, tàu soái hạm), viền màu phe (§11.1) cho khối quân/tàu khi máy > 1 km; tàu cứu viện mang cờ Anh, hải đội mang cờ TBN | Q1/Q4 xem câm (0/6, 2/6) | cờ là vật mang dữ kiện → cần nguồn mẫu cờ hải quân 1779–82 | mọi shot vây hãm | cờ phóng to = sai tỷ lệ → chỉ phóng ≤ 1,5× và ghi |
| D5 | **Đói có hình:** C3 thêm cảnh gần (khung neo/lướt thấp ≤ 4 s) hàng người hái rau dại hoặc chợ vắng (S052) | Q3 xem câm | thêm 1 cắt | C3 | — |
| D6 | Áp danh sách 9/1782 (bậc 2) vào N2.7–N2.9: đội gác Lines 130, King's/Prince's/Queen's 50/50/30, Main Guard 37 | mật độ đúng nguồn | chỉ hợp ngày 1–9/9/1782 | ch.2 sau bản thử | — |
| D7 | Render cả tập theo **6 gói ≤ 8 h** (§8) | trong 10 h/gói | ≈ 48 h máy (+62 % so G1b) | lịch dựng | ước G/H/F chưa đo |
| D8 | Giữ 3 công cụ mới làm chuẩn: đường cong thời gian, đêm có đèn, phố sập dần | dùng lại cho T4 London 1666 (cháy) và T5 Boston | thêm mã đêm cần kiểm "đêm ≤ 1,5× A" khi có tấm C | kênh | — |

## §12 Việc chờ chủ dự án

1. **Xem bản thử** `reports/v7p/ban-thu/v7p-xem.mp4` (và bản 540p có ray ngoài git, SHA §4). Duyệt hay không duyệt ngữ pháp mới để áp cả tập.
2. **Quyết D1–D8**, nhất là:
   - D2 (miễn §10.3 cho tua ngược);
   - D3 (cách cứu C1);
   - D4 (cờ/viền phe để người xem câm biết ai giữ Rock).
3. **Hiệu chỉnh số TL-1** theo bản thử: 4,03 cắt/phút và shot TB 14,9 s đạt dễ. Có muốn hạ trần xuống ≤ 3,5 cắt/phút cho cả tập (kế hoạch 3,47) không?
4. **Điều phối chấm 6 khung cổng** `reports/v7p/khung/cong-*.png` so đối thủ.
5. **Ghi AUTHORSHIP/RIGHTS (phiên P):**
   - quyết định điểm máy + ngữ pháp TL;
   - Faden 1783 (Yale 2046612) dùng để số hoá trại (đã có trong tai-san-vay-ham);
   - nhạc tạm Tyrant.mp3 (K2-MUS).
6. Phiên P merge nhánh này khi duyệt.

**DỪNG — chờ chủ dự án.**
