# ƯỚC TẬP + ĐỀ XUẤT GHIM CÔNG CỤ — K2C-T4-02 London (TIEN-KY-T4, 23/10/2026)

> Ước từ **số đo bản thử của phiên này** (§6 báo cáo) + **số thật T3** (BAN-CUOI-T3: cách A 1080p 3,3–5,1 s/khung/tiến trình ở P = 2; Cycles RTX 5090 ngày 27–28 s/khung, đêm 64 spp 100–117 s/khung; $1,19/h). Cập nhật 10:05 UTC sau khi pod T1 xong: số Cycles đêm + 1080p là số đo và bảng shot v1 (720 s). Mọi số là **(ước)** trừ chỗ ghi "đo".

## 1. Số đo dùng để ước (đo trong phiên)
| Lớp | Cấu hình | Số đo | Ghi chú |
|---|---|---|---|
| Cách A (London, 1,72 triệu tam giác, lửa/khói atlas) | 1280×720, spp 3–4, llvmpipe, 1 tiến trình (chạy chồng 1 Blender CPU) | **4,3–6,4 s/khung** (T2 4,3; T4 ≈ 5; T1 ngày 6,44 / đêm 5,32) | 1080p một khung: 8,0 s (ngày); T3 Gibraltar nhẹ hơn (3,3–5,1 s ở P = 2) |
| Cách A mặt nạ ID | 1920×1080, một lượt không post | 5,6–7,5 s/khung | lượt riêng cho shot N2+ |
| Cycles GPU (miền thể tích duy nhất) | RTX 5090 OptiX, 960×540, 32 spp + OIDN, ngày | **12,36 s/khung (đo 48 khung, 601 s đồng hồ gồm dựng cảnh)** | cách cũ (hộp theo ô, 318 khối): ≈ 177–213 s/khung → bỏ |
| Cycles GPU đêm | 960×540, 48 spp | **6,38 s/khung (đo 120 khung)** | ngày phần còn lại 16,1 s/khung (72 khung) |
| Cycles GPU 1080p (một khung) | 1920×1080, ngày 32 spp / đêm 48 spp | **45,6 s / 15,3 s (đo)** | gồm dựng cảnh ≈ 2 s |
| OpenAI tấm N2+ | `gpt-image-2.5-sunburst-2026-09-08` edits 2560×1440 high | $0,077/lượt + kiểm 2 mô hình ≈ $0,20 → **≈ $0,28/lượt**; 0/3 lượt đạt máy (§6 T6) | |
| Gemini Omni M-d | `gemini-omni-1.1-flash` i2v 10 s 720p | **$1,02/lượt**; 1/1 đạt máy (T5) + kiểm ≈ $0,25 | T3: 11 lượt cho 5 đoạn (2,2 lượt/đoạn) |

## 2. Ước cả tập (720 s = 17 280 khung)
| Khoản | Cách tính | Giờ máy | Tiền |
|---|---|---|---|
| Cách A 1080p | lớp A 513 s (12 312 khung) × 8 s/khung ÷ 2 tiến trình (P = 2) | **≈ 14 h** đồng hồ | 0 |
| Mặt nạ ID shot N2+ | 190 s (4 560 khung) × 6,5 s | ≈ 8 h (≈ 4 h ở P = 2) | 0 |
| Nướng ánh sáng (nếu đưa lightmap kiểu T3 vào London) | 6–8 mốc × ≈ 40 phút | ≈ 5 h | 0 |
| Cycles GPU (lớp B 85 s = 2 040 khung) | 1080p đo: ngày 45,6 s, đêm 15,3 s → nửa ngày/nửa đêm ≈ 17 h GPU + cài/kéo ≈ 1 h | (pod, không tốn giờ máy container) | **≈ $21–23** (> chặn RunPod $20 một phiên → chia 2 phiên); theo D5(a) chỉ 30–40 s cận đêm → **≈ $5–8** |
| Tấm nền N2+ | 15 shot cố định × ≈ 1,3 tấm × ≈ 3 lượt × $0,28 | — | **≈ $16–20** OpenAI |
| M-d Omni | 7 đoạn × ≈ 2,2 lượt × ($1,02 + $0,25) | — | **≈ $20** Gemini |
| Kiểm/chấm (Claude CLI + gpt) | ≈ 120 lượt soi × $0,2 | — | ≈ $15 Claude + ≈ $5 OpenAI |
| Giọng (ElevenLabs) | ≈ 9 800 ký tự lời v1 × (G1 + sửa 30 %) | — | trong gói thuê bao |
| **Tổng** | | **≈ 25–30 h máy container** (≈ 2–3 phiên ≤ 12 h) | **≈ $65–85** (GPU $5–23 · OpenAI $21–25 · Gemini $20 · Claude $15; thêm ≈ $5 nếu D18(a)) |

## 3. Bộ công cụ đề xuất GHIM cho cả T4
| Lớp | Công cụ · phiên bản | Giới hạn / luật kèm |
|---|---|---|
| Dữ liệu 2026 | OSM (api 0.6 /map, ODbL) + LiDAR EA Composite DTM/FZ-DSM 1 m 2022 (WCS, OGL) + pyproj 3.8.0 + OSTN15 | T4-G4; không Google 3D/Earth Studio/Cesium; cao độ thiếu → DSM − DTM trung vị 9 điểm |
| Dữ liệu 1666 | Doornick 1666 (Rijks PDM) — khớp 13 điểm OSM, affine RMS 44,2 m (LOO 58,8 m), TPS để đặt chồng; ranh cháy cuối số hoá (399 acre) | Leake (TAMU) bị chặn — chờ chủ dự án; Ogilby & Morgan rủi ro vừa |
| Hình học | `scripts/k2ldn/hinh_hoc.py` (numpy, tất định seed 1666) → `ldn.bin` dùng chung A/Cycles | lô nhà theo phố OSM còn giữ + lấp lõi khối; 14 540 nhà trong vùng cháy (+10 % so 13 200) — bậc 5 |
| Cách A | three.js 0.180.0 + `design/cong3/shared/post.js`; Chromium headless shell 1248 (Playwright) + Mesa llvmpipe 25.2.8 (LLVM 20); `design/k2v/ldn/page.js` | P = 2 khi có Blender; chờ RAM ≥ 5 GB; một vòng dựng một lúc |
| Lửa/khói A | atlas thể tích nướng sẵn (`nuong_flipbook.py`, numpy curl-noise; 64 khung 96×192) + bản đồ ánh lửa 20 m | Mantaflow trong bpy 5.2.2 lỗi (`LevelsetGrid.setConst`) → không dùng |
| Cycles | Blender 5.2.2 LTS, OptiX, RTX 5090 SECURE RunPod $1,19/h; `cy_ldn.py` miền thể tích duy nhất; step rate 12, max 64 bước; OIDN | không ghép A↔B trong một cú máy (K28); kéo PNG → JPG ngay (K29); pod báo xong thiếu khung > 2 lượt → tắt (K26) |
| Tấm nền N2+ | OpenAI `gpt-image-2.5-sunburst-2026-09-08` `/v1/images/edits` KHÔNG mặt nạ + ghép lớp (a) theo mặt nạ ID (PNG) + khớp màu render vào tông tấm (Reinhard Lab k 0,7) | ≤ 3 lượt/tấm; bộ kiểm `scripts/k2ldn/ai/kiem_n2p.py` (bản chép NC-N2P) — chờ phiên K đưa vào `checks/` |
| M-d | Gemini `gemini-omni-1.1-flash` image-to-video 720p (ảnh đầu = render) | ≤ 3 lượt; bộ kiểm `kiem_minh_hoa.py` (gpt-6.1-sol + claude-sonnet-5-5 + `checks/ll/q_thoi_dai.py` của K, chỉ chạy) |
| Màu | LUT kênh `k2c-t3-kenh-v030.cube` (bản thử áp ở bước xuất) | chỉnh màu toàn phim ở bản cuối (§16) |
| Mã hoá | ffmpeg 6.1.1; numpy 2.5.4, scipy 1.18.1, OpenCV 5.0.0, Pillow 13.0.0 | |

## 4. Rủi ro chính
| Rủi ro | Mức | Giảm thiểu |
|---|---|---|
| Chi phí Cycles 1080p cho 85 s ≈ $21–23 sát/vượt chặn RunPod $20 | vừa | dựng 1280×720 + phóng Lanczos/unsharp như Omni T3; hoặc giảm lớp B xuống ≈ 60 s; hoặc nâng chất lửa cách A (atlas mô phỏng lớn hơn, nhiều hạt) để B chỉ còn 3–4 cận đêm |
| Tấm N2+ không qua (iii) (màu nước/đổi vùng) | cao | sửa cảnh (đã bỏ dải "biển" chân trời); đề nghị K đổi phép (iii) sang mặt nạ vùng thay vì sắc độ; giảm % N2+ nếu không hội tụ |
| Mô hình Old St Paul's lệch tranh Hollar (đỉnh tháp lệch 299 px khi khớp mặt đông) | vừa | dựng lại theo bản khắc đo vẽ Hollar trong Dugdale *History of St Paul's* (1658, PD) — bậc 3–4 |
| Ranh cháy theo ngày là nội suy (bậc 5) giữa tên nơi bậc 2 | vừa | ghi "ước lượng" trong log + thẻ phương pháp; chủ dự án duyệt cách vẽ |
| Leake 1667 không tải được (Cloudflare) | thấp | Doornick đủ cho ranh; Leake chỉ để chính xác lô |
| Mạng phố 1666 = phố OSM còn giữ (danh sách phố mới sau 1666 là ước lượng) | vừa | kiểm danh sách với Ogilby & Morgan 1676 khi xác nhận PD |
