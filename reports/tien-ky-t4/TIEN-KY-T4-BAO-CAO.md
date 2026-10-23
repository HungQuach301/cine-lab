Nhánh thật: `k2c-t4-02-tienky` (gốc `origin/main` @9852adf5; nhánh mặc định của bộ khung `ccr-a4d35b28-j7pwch` KHÔNG dùng). SHA cuối: xem §0.

# BÁO CÁO TIEN-KY-T4 — tiền kỳ tập K2C-T4-02 London (kênh 2 "Moving Parts", loạt "Contested Places") · M1 · 23/10/2026

## §0. Nhánh, SHA, phạm vi
- Nhánh `k2c-t4-02-tienky`, gốc `origin/main` @9852adf5. Các commit của phiên: cc6185ce → 4e12f513 → c0ed776d → f4964aec → 183766fe → 07a2e9f9 → 144b0ba2 → 27b8b8a2 → @@SHA_CUOI@@ (commit cuối "DỪNG chờ chủ dự án"). Đã đẩy, **không merge**.
- Chỉ sửa trong vùng được giao: `channel-k2/k2c-t4-02/**`, `design/k2v/ldn/**` (mã mới; chỉ gọi `design/cong3/shared/post.js`, không đổi T3), `scripts/k2ldn/**`, `reports/tien-ky-t4/**`. Không chạm `checks/`, `docs/`, sổ cái (AUTHORSHIP/RIGHTS/COST-LEDGER/BAI-HOC/HANG-DOI), `tools/`, `channel-k2/k2c-t3-01/**` (chỉ đọc LUT), `main`.
- Mọi commit qua preflight (`set -o pipefail`) "— ĐẠT" + `lock.py --verify` KHỚP; hook pre-commit + pre-push cài trước lần đẩy đầu. Không force-push, không amend.
- Tệp gốc lớn ngoài git ở `/var/tmp/ldn/` — tái tạo bằng lệnh trong `scripts/k2ldn/` (SHA tư liệu trong `channel-k2/k2c-t4-02/licenses/SHA256-TU-LIEU.txt`); bản thu ≤ 5 MB trong git.

## §1. Việc 1 — TREATMENT
`channel-k2/k2c-t4-02/TREATMENT.md` (1 trang): xương sống, logline, 6 phần theo tỉ lệ đã chốt (hook 6 % · cháy 27 % · dựng lại 1 22 % · 1711–1939 10 % · 1940 15 % · dựng lại 2 → nay 20 %), 8 khoảnh khắc then chốt, cách dùng tư liệu đặc biệt (bản đồ hoạt hoá, tranh khắc hoà vào 3D), âm thanh thời kỳ. **Hook có nguồn bậc 1:** Pepys 2/9/1666 xem lửa từ "a little ale-house on the Bankside, over against the Three Cranes" (Gutenberg #4167) — đúng vị trí máy xương sống Bankside CAO (T4-G3).

## §2. Việc 2 — LỜI NHÁP v1
`channel-k2/k2c-t4-02/LOI-NHAP-v1.md`: 86 câu L01–L86, **1 593 từ** (đếm bằng `scripts/k2ldn/dem_loi.py` → `reports/tien-ky-t4/do/dem-loi.json`) ≈ 11,0 phút @145 wpm + ≈ 45 s lặng + 16 s thẻ phương pháp ≈ 12:00. Mỗi câu có claim · nguồn · trang · bậc. 22 mục **[cần kiểm]** liệt kê tự động cuối tệp. Thẻ nhân vật cho tên khó; từ điển phát âm 19 mục (Farriner, Bludworth, Pepys "PEEPS", Evelyn "EEV-lin", Southwark "SUTH-uk"…). Câu chữ theo T4-G2 ("late February 1667", "fewer than ten recorded deaths", "Churchill reportedly…").
- Đã bỏ câu Bludworth "a woman might piss it out" (không có trong nhật ký Pepys — DU-KIEN-MOI N2); dùng câu Pepys thật "Lord! what can I do?".

## §3. Việc 3 — BẢNG SHOT v1
`channel-k2/k2c-t4-02/BANG-SHOT-v1.{md,json}` (sinh bằng `scripts/k2ldn/bang_shot.py`): 60 shot, 720 s, 8 điểm máy xương sống P1–P8 (P1 BANKSIDE-CAO E 532330 N 180250 h 230 m nhìn St Paul's + vùng cháy tới Pudding Lane). Tổng lớp: A 71,25 % · N2P 26,39 % (≤ 50 %) · M-d 7,22 % (≤ 20 %) · AI tổng 33,61 % (≤ 70 %) · B (Cycles) 11,81 % · MAP+MAP3D 7,64 % · TL+KHÁC+THẺ 9,72 % · góc cao 75,56 %. Mọi phép kiểm cap ĐẠT.

## §4. Việc 4 — ĐỀ XUẤT BIBLE §19
`reports/tien-ky-t4/DE-XUAT-BIBLE-19.md`: (a) bộ cú máy (đẩy vào, vòng cung, cẩu lộ, trượt sông, thiên đỉnh, khớp cắt timelapse) với thông số tốc độ (tiêu điểm ≤ 1,5 %/s khung, quay ≤ 3°/s, timelapse = máy cố định cùng chỗ); (b) bản đồ hoạt hoá (bản đồ là gia vị, không là thân — K13; cùng toạ độ EPSG:27700 map↔3D; ranh theo ngày ghi "ước lượng"); (c) tranh khắc hoà vào 3D cùng góc hoặc góc khung (không AI chạm tư liệu). Ghi xung đột §15 f M-d (6) với LUAT b34 → phiếu G1 D10.

## §5. Việc 5 — DỮ LIỆU, NGUỒN, GIẤY PHÉP
- **Tư liệu hình:** 12 mục, bằng chứng nguyên văn nơi giữ trong `channel-k2/k2c-t4-02/licenses/` (JSON API/manifest/linked-art + chụp trang khi trang không chặn). Bảng đầy đủ: `channel-k2/k2c-t4-02/RIGHTS-NHAP.md` (phiên P chép vào `RIGHTS.md` sau G1).
- **Khớp bản đồ:** Leake 1667 (TAMU) **không tải được — Cloudflare 403** cả curl lẫn trình duyệt tự động → dùng Doornick 1666 (Rijksmuseum RP-P-OB-82.345, PDM; cùng khảo sát Hollar). Khớp 13 điểm khống chế với OSM: **affine RMS 44,2 m (LOO 58,8 m)**; đa thức bậc 2 RMS 35,5 m nhưng LOO 69,4 m (quá khớp) → dùng affine để đo, TPS để đặt chồng (`channel-k2/k2c-t4-02/du-lieu/khop-doornick.json`). Ogilby & Morgan: rủi ro vừa → chưa khớp (D13). Doornick bản UMich: không cần.
- **Ranh cháy cuối** số hoá từ Doornick (mật độ mực + bờ sông vẽ tay): **161,9 ha = 399 acre** (dữ kiện đã kiểm #6 "over 400 acres" → lệch −0,25 %; con số hay dẫn 436 acre gồm cả ngoài tường → −8,5 %, hợp lý vì mặt nạ bỏ mép sông và lòng phố rộng) → `du-lieu/ranh-chay-1666-cuoi.json`.
- **Trường giờ bén lửa:** nội suy RBF từ 31 tên nơi (thời điểm bậc 2 theo LUAT a01–a17 × vị trí bậc 1); lưới 20 m. Nội suy = **bậc 5 (ước lượng)**.
- **Địa hình:** EA LiDAR Composite DTM + FZ-DSM 1 m 2022 (OGL) cho 2026; 1666 = DTM 2026 + bờ sông trước Embankment (nội suy 1864–1870 theo N13). Toà 2026: OSM 17 815 toà (7 824 cao độ từ DSM − DTM). Lô nhà 1666 theo phố OSM còn giữ + lấp lõi khối: 60 552 nhà, **14 540 nhà trong vùng cháy** (dữ kiện 13 200 → +10 %, bậc 5; hình học không phải dữ kiện).
- **Không dùng** Google 3D Tiles/Earth Studio/Cesium (T4-G4). OS Open: chưa cần trong phiên.

## §6. Việc 6 — SÁU BẢN THỬ (xem `reports/tien-ky-t4/xem/`, tờ so `reports/tien-ky-t4/TO-SO.md`)
@@BAN_THU@@

## §7. Việc 7 — ƯỚC TẬP + GHIM CÔNG CỤ
`reports/tien-ky-t4/UOC-VA-GHIM.md`. Tóm tắt: cả tập ≈ **25–30 h máy container** (≈ 2–3 phiên ≤ 12 h) và ≈ **$65–85** (GPU $5–8 theo D5(a), hoặc $21–23 nếu Cycles 1080p cho cả 85 s — số đo 1080p: ngày 45,6 s/khung, đêm 15,3 s/khung; OpenAI $21–25; Gemini ≈ $20; Claude ≈ $15). Đề xuất ghim: three.js 0.180.0 + Chromium headless 1248 + Mesa llvmpipe 25.2.8; Blender 5.2.2 LTS OptiX RTX 5090; `gpt-image-2.5-sunburst-2026-09-08` edits; `gemini-omni-1.1-flash`; pyproj 3.8.0 + OSTN15; ffmpeg 6.1.1.

## §8. Việc 8 — PHIẾU G1
`reports/tien-ky-t4/PHIEU-G1.md`: 18 quyết định D1–D18 (phương án · ưu · nhược · tác động · rủi ro · đề xuất).

## §9. Dữ kiện mới đã kiểm (nguồn + trang + ngày truy cập 23/10/2026)
Bảng đầy đủ có trích nguyên văn: `reports/tien-ky-t4/DU-KIEN-MOI.md` (N1–N25). Điểm thay đổi lời:
- N2 Bludworth "piss it out" — **không có trong Pepys** (Gutenberg #4200, tìm toàn văn) → bỏ.
- N8 "87 of the City's 109 parish churches… 51 rebuilt" (Monument CMP 03/2025).
- N9 Hooke "one of the City's surveyors, with Peter Mills" (City, Univ. of London, eprint 30766).
- N11 "about 6,000 houses finished by the end of 1670"; Toà Cháy năm đầu 374 vụ (Oxford History; Inner Temple Library).
- N12 "for more than two and a half centuries" (London Museum), không ghi "đến 1963".
- N13 Victoria Embankment 2/1864–7/1870 (British History Online, Old & New London III tr. 322–329).
- N15 "as many as five million books" (Grub Street Project, 08/2023).
- N18 tầm nhìn Richmond 15,6 km, bảo vệ "since the 1970s" (LVMF View 9), không "since 1710".
- N21 lính cứu hoả chết: nguồn lệch 12/≤14/16 → "at least twelve".
- N25 Toà Cháy ngồi lần đầu Clifford's Inn 27/2/1667 (Inner Temple Library) — lời giữ "late February 1667".
- Hook: Pepys tại Bankside (Gutenberg #4167, mục 2/9/1666).

## §10. Nguồn và giấy phép
Xem `RIGHTS-NHAP.md` §A–E. Tóm tắt rủi ro: thấp — Doornick (Rijks PDM), Met 360649/361738/395057 (CC0), YCBA 266/40597 (CC0), Rijks Luyken/Charles II/Monument, NGA Wren (CC0), LoC Wren plan ("No known restrictions"); vừa — Ogilby & Morgan (BL qua Commons), Hollar Long View, Evelyn plan (chưa dùng); bị chặn — Leake TAMU. Dữ liệu: OSM (ODbL), EA LiDAR (OGL v3), OSTN15 (câu giấy phép **[cần kiểm]**). Không dùng nguồn trong danh sách cấm (NPG, London Museum ảnh, RCT, IWM, ảnh Cảnh sát City, LCC Bomb Damage Maps, RIBA). Ảnh Crown MOI 1940: **chưa tìm được** bản ngoài sê-ri HU (Commons API 429) — D14.

## §11. Chi phí thật
| Khoản | Mốc theo dõi | Chặn an toàn | Thật | Nguồn số |
|---|---|---|---|---|
| Claude API (bộ kiểm: claude-sonnet-5-5) | $8 | > $25 | **$0,82** (T6 3 × ≈ $0,14 · T5 3 × ≈ $0,10 · q_thoi_dai 3 khung $0,10) | `cost.jsonl`, `kiem/qtd-*.json` |
| OpenAI (ảnh N2+ + gpt-6.1-sol kiểm) | $5 | > $15 | **$0,50** (ảnh 3 × $0,077 = $0,23 · kiểm $0,27) | `so-ai.jsonl`, `cost.jsonl` |
| Gemini (Omni i2v) | $5 | > $10 | **$1,02** (1 lượt 10 s 720p) | `so-ai-gemini.jsonl` |
| RunPod (RTX 5090 SECURE $1,19/h) | $8 | > $20 | **$1,90** theo số dư (23,08 → 21,18); ước theo giờ 1,62 h = $1,93; pod đã xoá (HTTP 204) | `gio-gpu.jsonl` |
| ElevenLabs / YouTube | 0 | — | 0 / 0 | — |
| Giờ máy container | 12 h | — | **≈ 5 h** (≈ 06:00 → ≈ 11:00 UTC) | CHECKPOINT |
| **Tổng tiền API/GPU** | | | **≈ $4,24** | |

Không mốc nào bị vượt; không chạm chặn. Chi phí mô hình của chính phiên Claude Code không nằm trong bảng (không có số đo trong phiên).

## §12. Sự cố
| # | Sự cố | Xử lý | Kết quả |
|---|---|---|---|
| 1 | TAMU IIIF (Leake 1667) Cloudflare 403 cả curl và Playwright | dùng Doornick 1666 (Rijks PDM) | ranh cháy đủ; Leake chờ D12 |
| 2 | Commons API 429 lặp | lùi 6 s, giảm số gọi | ảnh MOI 1940 chưa tìm được (D14) |
| 3 | Trang Met/YCBA/LoC/NGA chặn trình duyệt tự động | bằng chứng = JSON API/manifest nguyên văn | đủ bằng chứng giấy phép |
| 4 | Tải hỏng để lại tệp rỗng | chỉ ghi sau khi tải xong | — |
| 5 | Playwright route > 100 MB làm vỡ ống devtools | máy chủ http cục bộ trong render_ldn.js | ổn định |
| 6 | Màu đỉnh coi như tuyến tính; vòng nước OSM ghép sai | đổi sRGB → tuyến tính; ghép vòng relation | — |
| 7 | Mantaflow (bpy 5.2.2) lỗi `LevelsetGrid.setConst` 2/2 lần | atlas thể tích bằng numpy (curl-noise + raymarch) | **đổi cách sau 2 lỗi** (< 3) |
| 8 | Cycles hộp thể tích theo ô ≈ 177–213 s/khung | một miền thể tích theo ảnh giờ bén lửa (đóng gói ảnh) | 12,4 s/khung |
| 9 | Ảnh sinh trong Blender ra đen | `update()` + `pack()` | — |
| 10 | `pkill -f` khớp chính shell (exit 144) | dừng theo PID/PGID | — |
| 11 | T6: mặt nạ JPEG nhiễu làm trượt (i); dải "biển" giả ở chân trời làm trượt (iii) | mặt nạ PNG; giới hạn mặt nước trong hộp địa hình | (i) đạt; (iii) vẫn trượt 3/3 |
| 12 | T5 ảnh đầu đen (máy trong khối nhà, đêm) | máy 34 m trên mái, phơi sáng 6 | ảnh đầu đọc như hoàng hôn → D18 |
| 13 | T3: homography 4 điểm với máy xa làm tranh co thành thẻ nhỏ; PnP không ổn định (Hollar không đo đạc) | **v2:** giải máy 9 điểm (trục ngang + dịch ống kính bằng dựng khung cao rồi cắt), tranh giữ nguyên khung rồi uốn dần lên mặt đông | xem §6 T3 |
| 14 | Khối toà OSM sáng trong cảnh 1666 (năm bắt đầu sai) | kẹp năm toà 2026 ≥ 1667,5, sinh lại `ldn.bin` | — |
| 15 | T1 A: hạt lửa/khói trên mặt sông | bỏ hạt có nền 1666 < 1,2 m; dựng lại T1 | hết lỗi |
| 16 | Lần sửa `page.js` đầu dùng chú thích `//` giữa dòng → nuốt phần mã sau (trang lỗi cú pháp, 1 lần thử hỏng) | đổi sang `/* */`, thử lại | đạt; vòng dựng T3 đang chạy lúc đó không bị ảnh hưởng (khởi động trước) |
| 17 | Ma trận chiếu bị `post.js` (dùng chung, không sửa) đặt lại khi khử răng cưa → không dịch ống kính trực tiếp được | dựng khung cao H2 rồi cắt | tương đương dịch ống kính dọc |
| 18 | Lệnh chờ nền cũ (ghép T2) bị bộ khung dừng khi hết hạn | không cần chạy lại — T2 đã ghép xong trước đó | — |

Không có lần đẩy nhầm, không force-push, không amend. Không lỗi nào lặp ≥ 3 lần.

## §13. Chỉ số trong ±5 % quanh ngưỡng
| Chỉ số | Giá trị | Ngưỡng | Lệch | Ghi chú |
|---|---|---|---|---|
| Số từ lời nháp v1 | 1 593 | 1 650 (khung 1 650–1 800) | −3,5 % | không thêm chữ chỉ để đủ; ≈ 12:00 với lặng + thẻ |
| TL + KHÁC + THẺ trong bảng shot | 9,72 % | ≤ 10 % | −2,8 % | sửa bảng shot có thể vượt |
| Góc cao trong bảng shot | 75,56 % | ≥ 75 % | +0,7 % | |
| Diện tích vùng cháy số hoá | 399 acre | dữ kiện "over 400 acres" | −0,25 % | đo, không phải ngưỡng kiểm |
| Kiểm T6 (iii) T9b nước → đất lượt 2 | 2,42 % | ≤ 2 % | +21 % (ngoài ±5 %) | ghi để rõ: trượt thật, không sát ngưỡng |
| Quay vòng cung T4 | 10,6°/s | ≤ 3°/s (§19 đề xuất) | ngoài ±5 % | do nén bản thử 3 s |
| Quay cẩu lộ T4 | 3,74°/s | ≤ 3°/s | +25 % (ngoài ±5 %) | kéo dài đoạn khi sản xuất |
| Nhà trong vùng cháy (hình học) | 14 540 | dữ kiện ≈ 13 200 | +10 % (ngoài ±5 %) | hình học bậc 5, không lên lời |

## §14. Quyết định đề xuất
Xem `PHIEU-G1.md`. Ba đề xuất chính: **D5** lửa = cách A cho cảnh rộng + Cycles chỉ 3–4 cận đêm; **D11** N2+ phụ thuộc phiên K đổi phép (iii), nếu không thì hạ N2P ≤ 15 %; **D6** dựng lại Old St Paul's theo Hollar/Dugdale 1658.

## §15. Việc chờ chủ dự án
1. Duyệt phiếu G1 (D1–D18) — một lần cho cả M1.
2. Duyệt `RIGHTS-NHAP.md` → phiên P chép vào `RIGHTS.md`; quyết định sáng tạo được duyệt → `AUTHORSHIP.md`.
3. Chuyển cho phiên K: đề nghị đổi phép (iii) bộ kiểm N2P (D11); đưa `kiem_n2p.py` vào `checks/`.
4. (Tuỳ chọn) tải tay Leake 1667 bản TAMU bằng trình duyệt thật (D12).
5. Phiên P: merge nhánh `k2c-t4-02-tienky` sau duyệt (phiên này không merge).
