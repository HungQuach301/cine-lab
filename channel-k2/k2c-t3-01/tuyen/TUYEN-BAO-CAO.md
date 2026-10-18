**Nhánh thật: `tuyen-t3`** (từ `origin/main` @ `82a17aef`; harness không buộc nhánh `claude/...`). Không merge.

# TUYẾN T3 — claim tuyến đường + bản vá bảng shot (SM1–SM3, 4 inset) cho Gibraltar: BÁO CÁO

> Phiên TUYẾN, 17/10/2026, theo lệnh chủ dự án (duyệt B1–B8 của NC-BD ngày 17/10). **Chỉ tạo tệp trong `channel-k2/k2c-t3-01/tuyen/`** (≈ 0,7 MB ≤ 20 MB). Không sửa `treatment.json`, `claims-vay-ham.*`, `ghost/`, `scripts/`, `design/`, `checks/`, `docs/`, nhánh khác.
> Đọc trước đã đọc: NC-BD §2.1–§2.4, §3.3 (nhánh `nc-ban-do`, chỉ đọc; thêm tên thực thể trong 6 mẫu GeoJSON để ghi đúng tên — chỉ đọc), `TIEN-KY-VAY-HAM.md` §1, §4, `claims-vay-ham.md`, `vay-ham/claims-vay-ham.json` (schema), `vay-ham/treatment.json`, `vay-ham/tu_kiem.py`, `docs/BIBLE-KENH2.md`, `reports/m3/BAI-HOC-LL.md`.
> Mọi câu trích là nguyên văn từ tệp tải bằng curl (ngoài git: `/var/tmp/cine-out/tuyen/`), SHA-256 trong `claims-tuyen.json`. Số giờ/khối lượng ghi **(ước)** khi chưa đo.

## Khối điều lệ (lệnh + thực tế)
| Trường | Lệnh | Thực tế |
|---|---|---|
| Nhánh | `tuyen-t3` từ `origin/main` | đúng; đẩy, không merge |
| Tệp được sửa | CHỈ `channel-k2/k2c-t3-01/tuyen/**` (≤ 20 MB) | 21 tệp + 3 ảnh xem nhanh, ≈ 0,7 MB. Thêm `tuyen/.gitignore` (`!*.json`) vì `channel-k2/.gitignore` chặn `*.json` và phiên không được sửa tệp đó (§9) |
| Trần | Claude API ≤ $2 (ghim) · YouTube 0 · ElevenLabs 0 · giờ máy ≤ 1 h | **$0** · **0** · **0** · **≈ 0,05 h** (§8) |
| Subagent | Sonnet được, chỉ giao đoạn trích đã lọc | **không dùng** — tra nguồn bằng `grep` trên tệp đã tải (rẻ hơn ≈ 45 nghìn token nền/subagent, BAI-HOC #15) |
| Preflight | bắt buộc; che email | hook `pre-commit`/`pre-push` cài đầu phiên (`tools/preflight.sh`); kết quả ở §9 |
| Dừng | không dừng hỏi giữa chừng; xong → đẩy → dừng | đúng; câu hỏi không chặn đã tự quyết (§10) |

---

## 0. Tóm tắt (đọc 2 phút)
1. **26 claim mới T001–T026** (lệnh ≈ 10–14; tăng vì tách riêng các điểm MÂU THUẪN thay vì gộp): **20 XÁC MINH · 4 MÂU THUẪN · 2 CHƯA XÁC MINH**. Mỗi claim XÁC MINH có ≥ 2 nguồn độc lập; **83/83 câu trích khớp nguyên khối** với tệp có đúng SHA (`verify_quotes_tuyen.py`). Nguồn hai phía khi có: Sayer 1862, Drinkwater 1905, Montero 1860, Ancell 1784, Stephens 1870 (đã có ở tiền kỳ, **SHA tải lại khớp 10/10**) + mới: Beatson 1804, Clowes 1898 (t. II, III), Schomberg 1802, Mahon 1836, **Fernández Duro 1900–01 (Armada española t. VI, VII — phía Tây Ban Nha)**, FRUS 1940–41, Hansard 1940–42, Howe 1957 (US Army CMH), HMGoG.
2. **Phát hiện đổi bản đồ/lời (đều có số đo):**
   - **Minorca đầu hàng ngày 5/2/1782** (cờ trắng 4/2) — Fernández Duro + Schomberg (+ Clowes "February 1782"). **OHM 1782‑01‑05 sai một tháng; Cliopatria 1781 sai** → đổi màu đúng 1782‑02‑05.
   - **Trận "ánh trăng" 16/1/1780:** Anh gọi theo mũi St Vincent (Beatson: thấy địch khi mũi ở phía bắc 4 league), Tây Ban Nha + nhật ký Ancell đặt hạm đội Lángara ở mũi Santa María (~100 km phía đông) → **MÂU THUẪN, vẽ VÙNG không vẽ điểm**.
   - **Trận 20/10/1782 ("Cape Spartel"):** Fernández Duro "á la vista de Cabo Espartel" ↔ Montero/báo cáo của Córdoba "junto á Cádiz" → **vùng**.
   - **Darby rời cảng:** 13/3/1781 (3 nguồn Anh) ↔ ~28/3/1781 (Fernández Duro) → **MÂU THUẪN**, bộ đếm chỉ ghi "Mar 1781".
   - **Rodney:** ngày đi 27/12/1779 khớp Anh + Tây Ban Nha, nhưng **không nguồn nào nêu thẳng cảng đi** → tuyến **vào từ mép, nhãn "from England"** (đúng luật lệnh). Vị trí bắt đoàn tàu Caracas 8/1/1780 MÂU THUẪN (ngoài khơi Bồ Đào Nha ↔ "100 league ĐĐB Finisterre") → không vẽ điểm.
   - **Torch: đoàn tàu KHÔNG xuất phát từ Gibraltar** (Howe 1957: từ Hampton Roads và sông Clyde; một nguồn → CHƯA XÁC MINH). Gibraltar là **chỉ huy sở (Eisenhower trong lòng Rock, 5–6/11/1942) + sân bay** (Spitfire bay sang Tafaraoui 8/11). → **Bỏ mũi tên biển "Gibraltar → Bắc Phi" của NC-BD §2.2**, thay bằng mũi tên KHÔNG Gibraltar → Tafaraoui + ba mũi tên biển vào từ mép, không ghi nơi đi (đề xuất E2).
   - **Ngày hạm đội liên hợp rời Cádiz 9/1782: không tìm được** (6 nguồn) → CHƯA; chỉ vẽ đoạn "từ cửa tây eo biển → Algeciras" sáng–chiều 12/9/1782 (hai phía).
3. **`routes.geojson`: 15 tuyến + 3 vùng.** Kiểm "tuyến biển không cắt đất" (Natural Earth 1:10m land + minor islands, đệm 5 km quanh cảng): **14/14 tuyến biển cắt đất 0,000 km; 0 điểm biển nằm trên đất** (lượt đầu bắt 9 tuyến cắt đất 3,5–44,9 km → đã sửa điểm điều khiển + spline hướng tâm). Gần bờ nhất 0,23 km (luồng Tagus/St Helens Roads — luồng cảng, nêu tên §2).
4. **`ranh-gioi.json`:** 3 mốc theo B1; chỉnh tay đủ 5 mục lệnh; **đồng minh = cùng màu phe dẫn đầu pha 85 % + gạch 45°** (đo: ΔE với xám trung tính 23,1 dưới mô phỏng mù màu đỏ–lục; mức 55 % ban đầu chỉ đạt 6,8 → loại).
5. **`treatment-patch.json`: SM1 6 s (từ 1a), SM2 7 s (từ 2f), SM3 7 s (từ 4g) + 4 inset (1d, 2a, 3d, 5d) góc TRÊN TRÁI, 9,84 % khung, 3,0 s, mờ 0,3 s.** Tự kiểm trên BẢN SAO: tổng **563,5 s không đổi**; strategic **20 s = 3,55 %**, dài nhất 7 s, 1 lần/chương, không liền nhau; Q26b 7 loại mỗi nửa; NC-H2 giữ 1 lần 2,5 s; NC-H3 ≤ 3 km 87,5 % → **92,3 %**; mốc đinh không xê dịch. `tu_kiem.py` gốc **dừng ở assert** với loại mới → chạy bản vá tối thiểu (diff kèm theo).
6. **Lời SM1–SM3** (tiếng Anh, CHỜ G1): 15 / 13 (19 từ nói) / 21 từ — §5.
7. **Chi phí thật:** Claude API **$0** · YouTube **0** · ElevenLabs **0** · giờ máy **≈ 0,05 h** · mạng ≈ 51 MB (ngoài git).

### Bảng quyết định đề xuất (chờ chủ dự án)
| # | Đề xuất | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|---|
| E1 | **Dùng 26 claim T001–T026**; 4 MÂU THUẪN vẽ VÙNG/không điểm; 2 CHƯA không vẽ | mọi điểm mốc có ≥ 2 nguồn, có phía Tây Ban Nha; không bịa toạ độ | nhiều claim hơn lệnh (26 ↔ 10–14) | REVIEWER G1 đọc thêm ≈ 26 dòng | nguồn thế kỷ 19 OCR lỗi → đối chiếu ảnh trang trước khi lên hình chữ trích |
| E2 | **Torch: không vẽ tàu "từ Gibraltar"**; vẽ đường KHÔNG Gibraltar → Tafaraoui (T024) + 3 mũi tên biển vào từ mép tây (không nhãn nơi đi, T025 CHƯA) + điểm Gibraltar "Allied HQ" | đúng sử liệu; tránh lỗi khán giả hay chỉ ra | khác NC-BD §2.2 ("mũi tên Gibraltar → bờ Bắc Phi") | SM3 nhịp 5,0–6,5 s | nếu muốn ghi "from Britain / from the USA" cần thêm 1 nguồn (công văn Cunningham, London Gazette 38204) |
| E3 | **SM2 chỉ vẽ phong toả + 3 đoàn tiếp tế + Minorca đổi màu**; KHÔNG vẽ hạm đội liên hợp 12/9/1782, trận 16/1/1780, trận 20/10/1782 | không lộ cao trào 2m (13/9/1782); mọi thứ trên hình có lời tương ứng (BAI-HOC #1) | ba tuyến/vùng có claim nhưng chưa dùng | dữ liệu sẵn trong `routes.geojson` cho shot khác nếu cần | — |
| E4 | **Đồng minh = màu phe dẫn đầu pha 85 % + gạch 45°**; đồng minh có màu series riêng (Pháp ↔ Tây Ban Nha) giữ màu riêng | chú giải ≤ 3 mục; một thực thể một màu; gạch đọc được khi mù màu | cần kiểu tô pattern trong M13-lite | V5b-2c thêm pattern fill | gạch moiré khi nén → gạch ≥ 6 px, kiểm ở G1b |
| E5 | **Tây Ban Nha 1941 giữ màu vàng đất + nhãn "Spain (non-belligerent)"**, không đổi sang xám | khán giả nhận ra cùng một nước suốt tập (NC-BD §3.3.7) | lệch chữ "không tham chiến #a89f8a" của B6 nếu đọc B6 theo trạng thái | AUTHORSHIP ghi cách đọc B6 | khán giả hiểu nhầm "đồng minh Trục" → nhãn chữ bắt buộc |
| E6 | **Inset khu ≈ 120 km với bờ Natural Earth**; khu 20–30 km chỉ khi đổi sang bờ OSM + nhãn "Map: © OpenStreetMap contributors" | NE đo: đỉnh cách nhau TB 2,7 km → ở 120 km ≈ 13 px/đoạn (mịn); ở ≤ 30 km > 50 px/đoạn (gãy khúc) | hộp đỏ dấu chân khung máy chỉ 2–11 px → cần vòng định vị 16 px | M14 | dấu chân quá nhỏ → khán giả không thấy hộp; giữ vòng định vị |
| E7 | **Ngày đổi chủ Minorca = 1782‑02‑05** cho mọi bản đồ series | hai phía khớp | phải sửa tay cả OHM lẫn Cliopatria | 1 dòng chỉnh trong dữ liệu ranh | — |
| E8 | **K viết luật strategic thật** (B3) dựa trên `tu_kiem_strategic.diff` (thêm loại, loại khỏi NC-H2, khối luật ≤ 15 %/≤ 8 s/≤ 2 mỗi chương/không liền nhau) | đo được ngay trên bảng shot | phiên này không sửa `checks/` (đúng vai) | chờ phiên K | nếu K xếp strategic vào "hồ sơ thật" thì tỷ lệ hồ sơ thật 20,7 % → 24,2 % (ngoại lệ D4 xa hơn) |
| E9 | **Schema claim mở rộng `nguon_doi_chieu` + `muc_lenh`** (giữ nguyên mọi trường cũ) | một claim chứa đủ ≥ 2 nguồn, kiểm tự động được | lệch schema T3b một chút | `gop_claims.py`/`bang_md.py` cũ bỏ qua trường mới (không vỡ) | — |

**Chỉ số trong ±5 % quanh ngưỡng (nêu tên):**
- **Lời SM3 ước 9,2 s so cửa sổ 9,0 s (SM3 7 s + 4g 2 s): +2,2 %.** Dự phòng: SM3 → 8 s (đúng trần B3, khi đó "SM3 8 s so trần 8 s" = 0 %, cũng phải nêu), 4g → 1 s; không cắt chữ.
- **Lời SM1 ước 6,0 s so cửa sổ 6,0 s: 0 %** (vừa khít; lời 1a bắt đầu ngay sau).
- Ngoài ±5 % (đã xét): strategic 3,55 % so 15 %; shot 7 s so 8 s (−12,5 %); inset 9,84 % so 12 % (−18 %); ΔE đồng minh–trung tính (deuteranopia) 23,1 so 20 (+15,5 %); NC-H3 ≤ 60 km 99,2 % so 70 %; ≤ 3 km 92,3 % so 40 %.

**Việc chờ chủ dự án:** §11.

---

## 1. Claim tuyến đường (`claims-tuyen.json`, bảng đọc `claims-tuyen.md`)

### 1.1 Cách làm và kiểm
- Tải lại 10 tệp nguồn tiền kỳ (archive.org djvu.txt) → **SHA khớp 10/10** với `vay-ham/claims-vay-ham.json`. Tải mới: Beatson 1804 t. V, Clowes 1898 t. II–III, Schomberg 1802 t. II, Mahon 1836, Fernández Duro t. VI–VII, Burchett 1720 (không dùng), FRUS (history.state.gov), Hansard API, HyperWar (Howe 1957), HMGoG 838/2022. Beatson t. VI (Howe 1782) trả **503** bốn lần → thay bằng Clowes t. III + Schomberg.
- Lọc bằng `grep` trên tệp, đọc đoạn quanh dòng khớp; không giao subagent.
- `tim.py` chuẩn hoá (chữ thường, ſ→s, bỏ ký tự không phải chữ/số) và định vị **dòng tệp + số trang in theo đầu trang OCR gần nhất** — số trang trong `vi_tri` là do máy đọc đầu trang, **không ghi tay** (lượt đầu tôi ghi số trang tay, đối chiếu máy thấy nhiều số lệch 3–14 trang so đầu trang OCR → đã bỏ hết số ghi tay). Đầu trang OCR méo giữ nguyên (Montero "868", "870" = tr. 368, 370).
- `verify_quotes_tuyen.py`: **83/83 câu trích (26 nguồn chính + 57 đối chiếu) khớp** tệp có đúng SHA.

### 1.2 Bảng claim (đếm: XÁC MINH 20 · MÂU THUẪN 4 · CHƯA XÁC MINH 2)
| ID | Mục | Trạng thái | Nội dung (tóm tắt) | Nguồn (phía) |
|---|---|---|---|---|
| T001 | a | XÁC MINH | Hạm đội Anh–Hà Lan chở "Charles III": St Helens 12/2/1704 (O.S.) → Lisbon 25/2 (O.S.); TBN: cửa Tagus 6/3 (N.S.) | Sayer · Clowes II (Anh) · Fernández Duro VI (TBN) |
| T002 | a | XÁC MINH | 6/1704: Shovell nhập hạm đội ngoài khơi Lagos/Algarve (16/6 O.S.) | Clowes II · Fernández Duro VI |
| T003 | a | XÁC MINH | 17/7/1704 (O.S.) họp chiến sự ngoài khơi Tetuan → đánh Gibraltar | Sayer · Clowes II · Montero · Fernández Duro VI |
| T004 | b | XÁC MINH | Đại Liên minh (Anh, Hoàng đế/Áo, Hà Lan) ↔ Pháp + Tây Ban Nha của Philip V | Sayer · Mahon · Fernández Duro VI |
| T005 | b | XÁC MINH | Bồ Đào Nha vào Đại Liên minh 5/1703 (ngày/nơi lệch: Lisbon 6/5 ↔ London 10/5 → chỉ nói "May 1703") | Mahon · Fernández Duro VI |
| T006 | c | XÁC MINH | Căn cứ phong toả: neo Algeciras (Barceló), cắt tiếp tế từ bờ châu Phi | Drinkwater ×2 · Montero · Beatson |
| T007 | c | XÁC MINH | Trạm canh/xuồng pháo ở Cabrita Point (Punta Carnero) | Drinkwater · Montero · Fernández Duro VII |
| T008 | c | XÁC MINH | 1/1780: hải đội Lángara tuần eo biển ↔ mũi St Vincent | Montero · Beatson |
| T009 | d | XÁC MINH | Rodney ra khơi 27/12/1779 (cảng đi KHÔNG có nguồn → vào từ mép) | Beatson · Fernández Duro VII · Drinkwater |
| T010 | d | MÂU THUẪN | Bắt đoàn Caracas 8/1/1780: "off Portugal" ↔ "100 leagues ENE of Finisterre" | Drinkwater · Fernández Duro VII ↔ Beatson |
| T011 | d | XÁC MINH | 16/1/1780 Rodney vượt mũi St Vincent | Beatson · Fernández Duro VII |
| T012 | e | MÂU THUẪN | Trận ánh trăng: phía nam mũi St Vincent (Anh) ↔ ngoài Santa María (TBN, Ancell) → VÙNG | Beatson · Stephens ↔ Fernández Duro VII · Montero · Ancell |
| T013 | d | MÂU THUẪN | Darby rời St Helens/Spithead 13/3/1781 (Anh) ↔ ~28/3 (TBN) | Beatson · Clowes III · Schomberg ↔ Fernández Duro VII |
| T014 | d | XÁC MINH | Darby: Cork (tàu lương thực) → … → ngoài Cap Spartel tối 11/4 → vịnh 12/4/1781 | Beatson ×2 · Clowes III ×2 · Drinkwater |
| T015 | d | XÁC MINH | Howe rời Spithead 11/9/1782 | Clowes III · Schomberg |
| T016 | d | XÁC MINH | Howe: St Vincent 8/10 → vào eo 11/10 → trôi vào Địa Trung Hải (ngoài Fuengirola/Marbella 13/10) → về vịnh 18/10/1782 | Clowes III · Schomberg · Montero · Fernández Duro VII |
| T017 | f | MÂU THUẪN | Trận 20/10/1782: ngày khớp; vị trí "trước Cap Spartel" ↔ "gần Cádiz" → VÙNG | Fernández Duro VII · Clowes III ↔ Montero (×2) |
| T018 | g | XÁC MINH | Hạm đội liên hợp vào eo từ phía tây sáng 12/9/1782, chiều neo giữa Orange Grove và Algeciras | Drinkwater ×2 · Fernández Duro VII |
| T019 | g | CHƯA XÁC MINH | Ngày hạm đội liên hợp rời Cádiz đi Algeciras 9/1782 — không tìm được | (Clowes III chỉ có chuyến Cádiz → eo Manche 6/1782) |
| T020 | h | XÁC MINH | Minorca: cờ trắng 4/2, đầu hàng 5/2/1782 | Fernández Duro VII · Schomberg · Clowes III |
| T021 | i | XÁC MINH | Sắc lệnh "non-belligerency" El Pardo 12/6/1940 (BOE 13/6) | FRUS 1940 (dịch sắc lệnh TBN) · Hansard 20/8/1940 · FRUS 12/6 |
| T022 | j | XÁC MINH | 14/6/1940 quân Khalifa do TBN chỉ huy chiếm vùng Tangier ("tạm thời"); 3/11/1940 viên chỉ huy TBN nắm hành chính | Hansard 19/6/1940 · FRUS 1940 (dịch công hàm TBN) · Hansard 13/11/1940 |
| T023 | k | XÁC MINH | 8/11/1942 đổ bộ Casablanca, Oran, Alger | Hansard Lords 11/11/1942 · Howe 1957 |
| T024 | k | XÁC MINH | Gibraltar = chỉ huy sở (Eisenhower 5–6/11) + Spitfire bay Gibraltar → Tafaraoui 8/11/1942 | Howe 1957 · HMGoG 838/2022 (= S122) |
| T025 | k | CHƯA XÁC MINH | Đoàn tàu Torch từ Hampton Roads và sông Clyde (không từ Gibraltar) — một nguồn | Howe 1957 |
| T026 | (ranh 1941) | XÁC MINH | 1941: Pháp chia bởi "line of demarcation" — vùng Đức chiếm ↔ vùng do Vichy quản | Hansard 14/5/1941 (Eden) · FRUS 1941 (công hàm Đại sứ Pháp; lời Pétain) |

### 1.3 Không dùng / cần làm trước G1
- Montero tr. 352–353 **lẫn sự kiện 1756** (Byng, Blakeney) vào Minorca 1781–82 → không dùng Montero cho Minorca.
- Văn bản BOE gốc 13/6/1940: bộ tìm Gazeta của BOE không nhận tham số qua curl (thử 2 lần, dừng theo BAI-HOC #12); FRUS đã dịch nguyên văn → đủ cho claim; nếu muốn trích tiếng Tây Ban Nha trên hình cần bản BOE.
- Beatson t. VI (archive.org 503) — thử lại nếu muốn nguồn Anh thứ ba cho Howe/Spartel.
- Ảnh trang: câu trích từ OCR thế kỷ 18–19 phải đối chiếu ảnh trang trước khi lên hình (như T3b).

---

## 2. Tuyến (`routes.geojson`, điểm mốc `gazetteer.json`, số đo `kiem-dat.json`)

### 2.1 Cách dựng
- **Điểm mốc** mang claim id; toạ độ từ OSM Nominatim (38 truy vấn, tệp thô + SHA ngoài git) cộng **độ dời ra khơi ghi rõ** ("ngoài khơi Lagos: dời 8,3 km về nam"…). Không toạ độ nào lấy từ trí nhớ.
- **Điểm điều khiển** (`dieu_khien`, 35 điểm) KHÔNG phải sự kiện: chỉ giữ nét spline trên biển. Đoạn giữa hai điểm có claim luôn `approx: true`.
- Spline **Catmull–Rom hướng tâm** (α = 0,5; không vọt ở chỗ quay đầu như ở Cork, Fuengirola); lấy mẫu ~4 km; tính trong LAEA châu Âu (EPSG:3035).
- **Kiểm đất:** Natural Earth 1:10m land + minor islands (v5.1.1, SHA zip trong `mk_routes.py`); phần tuyến ngoài đệm 5 km quanh điểm cảng ∩ đất = độ dài cắt đất.
- Lượt 1: **9/14 tuyến biển cắt đất** (đảo Wight, cửa Tagus, Tarifa, Ceuta, Punta Carnero, Cork, North Foreland, Madeira, mũi tây Alger: 3,5–44,9 km) → thêm điểm điều khiển, đổi spline → lượt 3: **0/14**. Lượt rà ảnh (`xem-truoc/SM3.png`) bắt thêm lỗi: điểm "vào từ mép" của Torch nằm **trong** khung (−12°) → dời ra −19°, thêm kiểm tự động "điểm mép phải ngoài bbox shot".

### 2.2 Bảng tuyến
| Tuyến | Shot | Mode | Phe | Ngày | Điểm mốc (claim) | Vào/ra mép | Dài km | Cắt đất km | Gần bờ nhất km |
|---|---|---|---|---|---|---|---|---|---|
| R1704-LIS | SM1 (phụ) | biển | Đại Liên minh | 12–25/2/1704 O.S. | St Helens (T001) → Lisbon (T001) | — | 1 697,5 | 0,000 | 0,23 ¹ |
| R1704-GIB | SM1 | biển | Đại Liên minh | 16/6 → 21/7 O.S. (1/8 N.S.) | ngoài Lagos (T002) → ngoài Tetuan (T003) → vịnh (S012) | — | 443,7 | 0,000 | 2,21 |
| R1780-PATROL | (chưa gán) | biển | Tây Ban Nha | 1/1780 | cửa tây eo (T008) ↔ St Vincent (T008) | — | 328,4 | 0,000 | 5,52 |
| R1780-RODNEY | SM2 | biển | Anh | 27/12/1779 → 18/1/1780 | mép (T009, T010) → St Vincent (T011) → vịnh (S054) | **vào từ mép, "from England"** | 967,8 | 0,000 | 1,92 |
| R1781-DARBY | SM2 | biển | Anh | 3/1781 → 12/4/1781 | St Helens (T013) → ngoài Cork (T014) → ngoài Spartel (T014) → vịnh (S055, S062) | cảng đi ngoài khung SM2 | 2 825,6 | 0,000 | 1,23 |
| R1782-HOWE | SM2 | biển | Anh | 11/9 → 20/10/1782 | Spithead (T015) → St Vincent (T016) → eo (T016, S056) → ngoài Fuengirola (T016) → vịnh (S056) → ngoài Spartel (T017) | cảng đi ngoài khung SM2 | 2 489,1 | 0,000 | 1,61 |
| R1782-ALLIED | (chưa gán, E3) | biển | Pháp–TBN | 12/9/1782 | cửa tây eo (T018) → neo Algeciras (T018, S065) | — | 50,5 | 0,000 | 3,44 |
| R1940-EV-CASA | SM3 | biển | dân thường | 22/5–24/6/1940 | Gibraltar (S114, S115) → Casablanca (S115) | — | 365,4 | 0,000 | 2,69 |
| R1940-EV-LON | SM3 | biển | dân thường | 7–8/1940 | Gibraltar (S114, S117) → cửa Thames "London" (S114, S116) | — | 2 488,7 | 0,000 | 3,03 |
| R1940-EV-MAD | SM3 | biển | dân thường | 7–8/1940 | Gibraltar → Funchal (S117, S120) | — | 1 150,2 | 0,000 | 3,03 |
| R1940-EV-JAM | SM3 | biển | dân thường | 9 & 31/10/1940 | Gibraltar (S118) → mép tây "to Jamaica" | **ra mép** | 1 396,2 | 0,000 | 3,03 |
| R1942-AIR-ORAN | SM3 | **không** | Đồng minh | 8/11/1942 | Gibraltar (T024, S122, S123) → Tafaraoui (T024) | — | 444,7 | không áp | — |
| R1942-SEA-WEST | SM3 | biển | Đồng minh | 8/11/1942 | mép (T025) → Fedala/Mohammédia (T023) | **vào từ mép, không nhãn nơi đi** | 1 095,9 | 0,000 | 1,19 ¹ |
| R1942-SEA-ORAN | SM3 | biển | Đồng minh | 8/11/1942 | mép (T025) → Oran (T023) | **vào từ mép** | 1 691,0 | 0,000 | 3,10 |
| R1942-SEA-ALG | SM3 | biển | Đồng minh | 8/11/1942 | mép (T025) → Alger (T023) | **vào từ mép** | 2 040,1 | 0,000 | 4,02 |

¹ Ba chỗ sát bờ < 1,5 km ngoài đệm cảng: luồng ra St Helens Roads (0,3 km dài), luồng Tagus vào Lisbon (cửa sông hẹp ≈ 2 km), luồng vào Fedala (0,3 km) — đều là luồng cảng; ở khung 2 500 km (≈ 1,3 km/px) chúng chạm nét bờ. Không có ngưỡng → nêu để V5b-2c quyết độ dày nét.

**Vùng (không vẽ điểm):** Z1780-MOONLIGHT (T012, elip bán kính 22 km quanh đoạn St Vincent-4-league ↔ ngoài Santa María) · Z1782-SPARTEL (T017, Spartel ↔ ngoài Cádiz) · Z1779-BLOCKADE (T006, T007, S042: Algeciras · Cabrita · Ceuta, nét đứt).

**Ảnh xem nhanh** (không phải hình phim): `xem-truoc/SM1.png`, `SM2.png`, `SM3.png`. Ghi nhận khi rà: ở SM2 ba đoàn tiếp tế đi gần như **cùng một hành lang** → hoạt hình phải vẽ lần lượt và **mờ tuyến trước còn 30 %** khi tuyến sau bắt đầu (ghi trong `nhip` của SM2), nếu không ba tuyến chồng thành một.

---

## 3. Ranh giới (`ranh-gioi.json`)
| Mốc | Nguồn chính / đối chiếu (B1) | Chỉnh tay | Chú giải (≤ 3) |
|---|---|---|---|
| **1704** (SM1) | OHM (Spain từ 1704‑08‑04) / Cliopatria 1702–1705 | **Bỏ "Pro-Habsburg Spain"** (gộp vào "Spain (Philip V)"); Gibraltar = ĐIỂM, đổi màu đúng 1/8/1704 N.S. + nhãn "taken in the name of 'Charles III'"; Bồ Đào Nha tô màu đồng minh theo T005 (nguồn ranh không mang liên minh) | Grand Alliance (England & allies) · France · Spain (Philip V) |
| **1780–82** (SM2) | Cliopatria / OHM | **Minorca = Anh trước 1782‑02‑05, TBN từ 1782‑02‑05** (T020; cả hai nguồn ranh sai); Menorca đo 49,1 × 23,3 km ≈ 38 × 18 px → polygon; Gibraltar = ĐIỂM | Britain · Spain · France |
| **1941** (SM3) | Cliopatria (có vùng chiếm đóng) / OHM (chỉ đối chiếu TBN, Bồ Đào Nha) | **Tangier → "Spanish-occupied since June 1940"** (T022, gạch vàng; không ghi năm kết thúc); "**German-occupied France**" (gạch xám-nâu, không màu/biểu tượng chế độ) / "**Vichy France**" (xanh, T026); "**Spain (non-belligerent)**" (T021); đổi tên Cliopatria: Francoist Spain → Spain, Estado Novo → Portugal; Bắc Phi: "French Morocco", "Algeria" (không có claim cho chữ "Vichy" ở châu Phi) | Britain & Allies · Spain (non-belligerent) · France: Vichy / German-occupied |

**Màu B6:** Anh `#b03a2e`, Tây Ban Nha `#c9a227`, Pháp `#2e5c8a`, không tham chiến `#a89f8a`, dân thường kem (B6 không ghi mã → đề xuất `#efe6cf`).

**Đồng minh (lệnh yêu cầu đề xuất + lý do):** chọn **cùng màu phe dẫn đầu, pha 85 % với nền giấy + gạch 45°**; đồng minh có màu series riêng giữ màu riêng (Pháp ↔ Tây Ban Nha 1779–83). Lý do: chú giải ≤ 3 mục; một thực thể một màu; gạch không phụ thuộc sắc độ. Số đo ΔE76 (CIELAB D65; mù màu đỏ–lục mô phỏng Machado 2009, mức 1,0):

| Cặp | ΔE thường | ΔE deuteranopia |
|---|---|---|
| Anh ↔ Tây Ban Nha | 59,8 | 34,4 |
| Anh ↔ Pháp | 79,8 | 71,0 |
| Tây Ban Nha ↔ Pháp | 98,9 | 100,5 |
| Anh ↔ không tham chiến | 57,4 | 32,8 |
| Tây Ban Nha ↔ không tham chiến | 51,9 | 50,3 |
| đồng minh Anh (pha 85 %) ↔ không tham chiến | 45,9 | **23,1** |
| đồng minh Anh (pha 85 %) ↔ Tây Ban Nha | 56,0 | 36,5 |
| đồng minh Anh (pha 85 %) ↔ Anh | 12,3 | 9,6 (cùng phe; phân biệt bằng gạch) |
| không tham chiến ↔ dân thường | 25,7 | 25,7 |

Lượt đầu tôi đặt pha 55 %: đồng minh ↔ không tham chiến dưới deuteranopia chỉ **6,8** (gần như trùng màu) → thử 40/55/70/80/90 % → không mức nào cách cả xám lẫn đỏ ≥ 20; chọn 85 % (cách xám 23,1) và để gạch tách khỏi Anh.

---

## 4. Bản vá bảng shot (`treatment-patch.json`) và tự kiểm (`tu-kiem-truoc-sau.json`)

### 4.1 Shot mới (`type: strategic`, loại "bản đồ chiến lược")
| Shot | Chèn | Dài | Tuyến | Ranh / nhãn | Bộ đếm | Không vẽ (lý do) |
|---|---|---|---|---|---|---|
| **SM1** | trước 1a (1a 11 → 5 s) | 6 s | R1704-GIB (+ R1704-LIS mờ, 1 s) | 1704 · "approx. borders c. 1704 — OpenHistoricalMap, IGN" | Feb 1704 → Jun 1704 → "21 July (O.S.) / 1 Aug (N.S.) 1704" (nối sang 1a) | — |
| **SM2** | trước 2f (2f 11 → 4 s) | 7 s | Rodney → Darby → Howe (lần lượt, mờ tuyến trước) + vòng phong toả | 1780–82 · "approx. borders c. 1782 — Cliopatria (Seshat)"; Minorca đổi màu lúc bộ đếm qua 5 Feb 1782 | Jan 1780 → Apr 1781 → 5 Feb 1782 → Oct 1782 (dừng 18 Oct) | tuần tra Lángara, vùng trận 1780, hạm đội liên hợp, vùng trận 20/10/1782 (E3) |
| **SM3** | trước 4g (4g 9 → 2 s) | 7 s | 4 cung sơ tán (kem) + KHÔNG Gibraltar → Tafaraoui + 3 mũi tên biển vào từ mép | 1941 · "approx. borders c. 1941 — Cliopatria (Seshat)"; "Spain (non-belligerent)" hiện 12/6; Tangier đổi 14/6 | May 1940 → 12–14 Jun 1940 → Jul–Oct 1940 → 8 Nov 1942 | tàu "từ Gibraltar" (E2) |

Mỗi SM khai: `tuyen` (id trong `routes.geojson`), `ranh` (mốc trong `ranh-gioi.json`), `nhan_ranh`, `bo_dem`, `nhip` (biến cố hình ≤ 3,5 s/lần — Kinh thánh §4), `chu_giai`, `claims`, `bbox`, `khung_rong_km`, máy (lặn liên tục vào shot 3D kế tiếp).

### 4.2 Inset (B4 theo lệnh: góc TRÊN TRÁI, chip nơi chuyển TRÊN PHẢI)
| Shot | Vào/dài/mờ | Khu | Nhãn (≤ 2) | Hộp đỏ dấu chân (ước) |
|---|---|---|---|---|
| 1d | 0,6 s / 3,0 s / 0,3 s | eo biển ~120 km | Gibraltar · Strait of Gibraltar | ≈ 0,8 km ≈ 4 px → đúng tỉ lệ + vòng định vị 16 px |
| 2a | như trên | như trên | Gibraltar · Spain | ≈ 2,2 km ≈ 11 px |
| 3d | như trên | như trên | La Línea · Gibraltar | ≈ 0,3 km → vòng định vị |
| 5d | như trên | như trên | La Línea · Gibraltar | ≈ 0,4 km → vòng định vị |

Khung inset 600 × 340 px = **9,84 %** (trần 12 %; NC-BD khuyên nhắm ≤ 11 %), x/y = 96/54 px (lề an toàn 5 %), chỉ bờ biển + hộp đỏ + nhãn, không ranh giới, "Map: Natural Earth". Dấu chân thật lấy từ `campath.json` khi dựng (ước ở bảng = 2,7 × AGL đại diện). Độ mịn bờ NE: E6.

### 4.3 Tự kiểm trước/sau (đo trên BẢN SAO; `vay-ham/treatment.json` SHA `b7f455d0…` không đổi — script kiểm lại SHA sau khi chạy)
| Luật | Ngưỡng | TRƯỚC | SAU (strategic) | Ghi chú |
|---|---|---|---|---|
| Tổng thời lượng | 9–11 phút; giữ 9:23,5 | 563,5 s, 65 shot | **563,5 s**, 68 shot | không đổi |
| Q26b-K2 nửa 1 | ≥ 3 loại; một loại ≤ 70 % | 6 loại; 42,2 % | **7 loại; 37,6 %** | 3D vùng giảm |
| Q26b-K2 nửa 2 | như trên | 6 loại; 39,1 % | **7 loại; 39,1 %** | |
| NC-H2 địa cầu | > 50 km ≤ 1 lần, ≤ 3 s | 1 lần (0c), 2,5 s | **1 lần, 2,5 s** | strategic không tính (B3) |
| NC-H3 ≤ 60 km | ≥ 70 % thời lượng 3D | 99,2 % | **99,2 %** | |
| NC-H3 ≤ 3 km | ≥ 40 % | 87,5 % | **92,3 %** | bỏ 20 s 3D ở 5–45 km |
| 3D / phim | — | 68,3 % | 64,8 % | |
| NC-H1 | 0 lỗi | 0 | 0 | |
| Lặp vùng + góc | ≤ 2 | 1 | 1 | |
| Footage | ≤ 20 % | 0,9 % | 0,9 % | |
| Shot thiếu claim | 0 | 0 | 0 | |
| Mốc đinh | ≥ 1/chương bước ngoặt | 6 (1e 82,0 · 2g 199,0 · 2m 253,0 · 3b 323,5 · 3f 359,0 · 4b 389,0 s) | **6, cùng thời điểm** | |
| **Strategic tỷ trọng** | ≤ 15 % | — | **3,55 % (20 s)** | |
| **Strategic mỗi lần** | ≤ 8 s | — | **dài nhất 7 s** | |
| **Strategic mỗi chương** | ≤ 2 | — | **ch.1: 1 · ch.2: 1 · ch.4: 1** | |
| **Strategic liền nhau** | không | — | **không** | |
| Hồ sơ thật (chỉ báo) | 10–15 % | 20,7 % | 20,7 % | nếu xếp strategic vào "bản đồ lịch sử": 24,2 % |

- `tu_kiem.py` gốc trên bản vá: **dừng ở `AssertionError: SM1`** (loại mới chưa có) → ghi trong `tu-kiem-truoc-sau.json`.
- Chạy thêm "SM coi như bản đồ lịch sử" (để thấy tác động lên luật cũ): mọi luật ĐẠT; hồ sơ thật 24,2 %.
- Bản vá tối thiểu (3 chỗ, `tu_kiem_strategic.diff`): thêm loại, loại khỏi NC-H2, thêm khối luật B3. Bản gốc trong `vay-ham/` **không sửa**; đây là đề xuất cho K (E8).

---

## 5. Lời SM1–SM3 (tiếng Anh — **CHỜ DUYỆT Ở G1**; không viết lại lời chỗ khác)
Ước 2,5 từ/s (Kinh thánh §3: ~150 từ/phút); năm đọc thành chữ tính theo từ nói.

| Shot | Câu | Từ | Ước | Cửa sổ | Claim |
|---|---|---|---|---|---|
| SM1 | *England, the Dutch and Portugal backed a rival for Spain's crown; France backed Madrid's king.* | 15 | 6,0 s | 6,0 s | T004, T005 |
| SM2 | *To break the blockade, Britain sent three relief fleets: 1780, 1781, 1782.* | 13 (19 nói) | 7,6 s | 11,0 s (SM2 + 2f) | T006, T009, T013, T015, S054–S056 |
| SM3 | *June 1940: Spain turns 'non-belligerent' and occupies Tangier. Gibraltar sends its women and children away. By 1942, it launches an invasion.* | 21 (23 nói) | 9,2 s | 9,0 s (SM3 + 4g) | T021, T022, S114, T023, T024, S122 |

- SM1 hai phía trung tính: không gọi Philip V là "claimant"; "Madrid's king" đúng vị thế năm 1704. Phương án: *"1704. Europe is at war over Spain's crown — and an Anglo-Dutch fleet is heading south."* (16 từ).
- SM2 tuỳ chọn (nếu lời 2f còn chỗ): *"Between the second and the third, Spain took back Minorca."* (T020). Không nói số tàu (nguồn lệch 20–22 / 28 / 34).
- SM3: "women and children" theo S114; "it launches an invasion" = Gibraltar là chỉ huy sở + sân bay (T024) — **không** nói đoàn tàu xuất phát từ Gibraltar (T025).

---

## 6. Ghi chú kỹ thuật cho V5b-2c (M13-lite, M14)
- `routes.geojson`: `LineString` WGS84 đã lấy mẫu ~4 km; mỗi feature có `waypoints` (claim, nhãn ngày), `doan` (approx), `diem_dieu_khien`, `vao_tu_mep`/`ra_mep`, `kiem_dat`. Ba vùng là `Polygon`.
- Mọi thay đổi điểm điều khiển phải chạy lại `mk_routes.py` (mã thoát 1 nếu cắt đất) — **K nên khoá luật này** (NC-BD §3.4).
- `xem_truoc.py` có kiểm "điểm vào/ra mép nằm ngoài bbox shot" (assert).

## 7. Hạn chế
- Hải trình giữa các điểm có claim là **biểu trưng** (approx); không có nhật ký hải trình theo ngày.
- Vị trí "ngoài khơi X" là toạ độ gazetteer + độ dời tôi chọn (ghi trong `gazetteer.json`), không phải toạ độ trong nguồn (trừ điểm Beatson "4 leagues" cho vùng T012).
- Nguồn ranh (Cliopatria/OHM) chưa tải trong phiên này; `ranh-gioi.json` là **đặc tả chỉnh tay**, chưa phải polygon đã sửa (việc của V5b-2c/phiên chuẩn hoá ranh, NC-BD §2.1 ước 1,5–2 h).
- Đường phân giới Pháp 1941: claim T026 kiểm sự tồn tại hai vùng, **không** kiểm hình dạng đường → giữ nhãn "approx.".
- Gazetteer dùng dữ liệu OSM (ODbL): chỉ 38 toạ độ điểm (trích không đáng kể) + ghi công trong mô tả; đề xuất dòng RIGHTS (§11).

## 8. Chi phí thật (`cost.json`)
| Mục | Trần | Thật |
|---|---|---|
| Claude API | ≤ $2 | **$0** (không gọi API trả tiền; không subagent) |
| YouTube | 0 | **0** |
| ElevenLabs | 0 | **0** |
| Giờ máy | ≤ 1 h | **≈ 0,05 h** (mỗi script < 2 s; còn lại là tải/đọc nguồn) |
| Mạng | — | ≈ 51 MB ngoài git: 21 tệp archive.org, 51 tệp web (FRUS, Hansard, HyperWar, HMGoG, Marquina), 39 tệp Nominatim, 3 zip Natural Earth; WebSearch 0 |

Dòng đề xuất cho `COST-LEDGER` (P ghi, phiên này không sửa): `TUYEN-T3-01 | 17/10/2026 | API $0 | YT 0 | EL 0 | máy ≈ 0,05 h | nhánh tuyen-t3`.

## 9. Tệp và preflight
| Tệp | Nội dung |
|---|---|
| `TUYEN-BAO-CAO.md` | báo cáo này |
| `claims-tuyen.json` / `claims-tuyen.md` | 26 claim + nguồn đã tải (SHA) / bảng đọc |
| `routes.geojson` · `gazetteer.json` · `kiem-dat.json` | 15 tuyến + 3 vùng · toạ độ điểm mốc + độ dời · số đo cắt đất |
| `ranh-gioi.json` | 3 mốc ranh, chỉnh tay, màu B6, đề xuất đồng minh, ΔE |
| `treatment-patch.json` · `tu-kiem-truoc-sau.json` · `tu_kiem_strategic.diff` | bản vá SM1–SM3 + 4 inset + lời · tự kiểm trước/sau · vá tối thiểu tu_kiem |
| `xem-truoc/SM1.png`, `SM2.png`, `SM3.png` | ảnh xem nhanh (không phải hình phim) |
| `mk_claims.py`, `tim.py`, `verify_quotes_tuyen.py`, `mk_claims_md.py`, `mk_routes.py`, `mk_ranh.py`, `mk_patch.py`, `ap_patch.py`, `xem_truoc.py` | dựng lại mọi tệp trên từ tệp thô (`/opt/cine/bin/python -I …`) |
| `cost.json` · `.gitignore` | chi phí · mở lại `*.json` cho riêng `tuyen/` |

- Môi trường: `verify.sh` đầu phiên 9 PASS / 4 FAIL (three.js, tifffile/pyshp, k2v node_modules, Freesound — không dùng trong phiên). Cài thêm vào `/opt/cine`: `shapely 2.2.0`, `pyshp 3.1.6`, `pyproj 3.8.0` (ngoài repo).
- Preflight: hook `pre-commit` + `pre-push` (`tools/preflight.sh`): **pre-commit "24 tệp (staged) — ĐẠT", `lock.py --verify` KHỚP, PREFLIGHT ĐẠT**; email: 0 trong tệp ghi (tác giả commit `noreply@anthropic.com`).

## 10. Tự quyết của phiên (không dừng hỏi), cần chủ dự án biết
1. Tăng số claim lên 26 (tách MÂU THUẪN; thêm T026 cho nhãn 1941 mà lệnh yêu cầu).
2. Mở rộng schema (`nguon_doi_chieu`, `muc_lenh`) thay vì tách mỗi nguồn thành một claim như T3b.
3. Bỏ mũi tên biển "Gibraltar → Bắc Phi" (E2); không đưa hạm đội liên hợp/hai trận vào SM2 (E3) — dữ liệu vẫn có trong `routes.geojson`.
4. Đồng minh pha 85 % (không phải 55 %) sau khi đo ΔE.
5. Inset khu ≈ 120 km (không phải tầm phố) vì độ thô bờ NE đo được.
6. Không dùng subagent (việc tra nguồn vừa đủ cho một phiên; rẻ hơn).
7. Đọc (chỉ đọc) tên thực thể trong 6 mẫu GeoJSON của nhánh `nc-ban-do` để ghi đúng tên trong `ranh-gioi.json`.

## 11. Việc đang chờ chủ dự án
1. Duyệt **E1–E9** (§0).
2. Duyệt **lời SM1–SM3** ở G1 (§5), kể cả câu tuỳ chọn Minorca.
3. Ghi **AUTHORSHIP** nếu duyệt: E2 (Torch), E3 (phạm vi SM2), E4–E5 (màu), E6 (inset).
4. **RIGHTS.md** (P ghi): Natural Earth (PD, bờ biển + kiểm đất); OSM Nominatim (ODbL, 38 toạ độ điểm — "© OpenStreetMap contributors"); Cliopatria/OHM như NC-BD; FRUS/Hansard (công vụ Mỹ — PD; Hansard — Open Parliament Licence) nếu trích lên hình.
5. Giao **K**: luật strategic (E8) + khoá luật "tuyến biển không cắt đất" (`mk_routes.py` làm mẫu đo).
6. Giao **V5b-2c**: M13-lite đọc `routes.geojson` + `ranh-gioi.json` (pattern fill, mờ tuyến trước, bộ đếm hai lịch 1704), M14 theo §4.2.
7. Tuỳ chọn trước G1: tìm nguồn thứ hai cho T025 (London Gazette 38204) và ngày rời Cádiz T019 (Gaceta de Madrid 9/1782); thử lại Beatson t. VI.

**DỪNG chờ chủ dự án.**
