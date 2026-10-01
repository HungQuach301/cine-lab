# BÀN GIAO → phiên mới "LL-P · Last Lamplighters" (01/10/2026)

Phiên P cũ (nhánh `ccr-af7a498d-ss3snk`) dừng nhận việc theo chỉ thị chủ dự án 01/10/2026. Tài liệu này đủ để phiên mới tiếp tục mà không cần đọc lịch sử chat.
Đọc kèm: `CLAUDE.md`, `PLAN.md` (mục "Hàng chờ" 5–10), `AUTHORSHIP.md` (các dòng 01/10/2026), `RIGHTS.md` (mục M2-*, M3-*).

## 1. Trạng thái
| Mốc | Trạng thái | Tài liệu |
|---|---|---|
| Cổng 6 (Last Round) | ĐÓNG 01/10; main có merge `8c392fd` | `reports/m2/CONG-6-DONG.md` |
| Chuyển hướng kênh | quyết 01/10 | AUTHORSHIP "Định hướng" |
| Mốc 1: thử phong cách B3/B1 → chọn B3 | XONG | `reports/m3/THU-PHONG-CACH.md`, `THU-PHONG-CACH-V2.md` |
| Kịch bản v1, v2; series 6 tập | XONG | `reports/m3/KICH-BAN-TAP-THU.md` (v1 để đối chiếu), `KICH-BAN-TAP-THU-V2.md`, `SERIES-LAST-LAMPLIGHTERS.md` |
| Kế hoạch tập thử | XONG | `reports/m3/KE-HOACH-TAP-THU.md` |
| M2.0 chuẩn bị (B3 v3, bộ mẫu dữ liệu, giọng, đo 1080p, bảng shot) | XONG, chủ dự án duyệt | `reports/m3/M2-0-CHUAN-BI.md`, `BANG-SHOT-M2.md` |
| M2.1 animatic nhịp | XONG (9:37,5) | `reports/m3/M2-1-ANIMATIC.md`, `screening/ll-ep01-animatic.mp4` |
| **Tiếp theo** | **kịch bản v3 + lát cắt M2.2a** (lệnh sẽ dán ở phiên mới) | — |

## 2. Nhánh và commit cuối
| Nhánh | Commit cuối | Vai trò |
|---|---|---|
| `ccr-af7a498d-ss3snk` | **xem dòng cuối của mục 10** (commit bàn giao) | nhánh P: mọi báo cáo, AUTHORSHIP, PLAN, RIGHTS, screening, bản vá mã. Chỉ có tài liệu và tài sản, KHÔNG có mã m3 chạy được |
| `thu-phong-cach` | `49df834` | **mã chạy được** của B3/B3v2/b3v3, bộ mẫu dữ liệu, animatic (`design/m3/**`, móc trong `design/cong5/layout/page.js`). Đã push, không merge |
| `thu-mat` | `5db04fe` | THỬ MẶT V1 (vật liệu da three.js, cờ `thuMat`); hướng mặt bán tả thực đã bỏ. Đã push |
| `thu-mat-2` | `1b47939` (CHỈ cục bộ, không push) | THỬ MẶT 2 dừng giữa chừng; bản vá ở `reports/m2/cong7/thu-mat-2/ma-dung-do.patch`. Không cần cho LL |
| `main` | `ebdacde` | Cổng 6 + tài liệu tới lúc chuyển hướng. Nhánh P đi trước main (chỉ tài liệu); **P chỉ merge main khi chủ dự án cho phép** |

Bản vá mã phong cách (dựng lại nếu mất nhánh): `reports/m3/thu-phong-cach/ma-thu-phong-cach.patch` (`git apply --binary` lên `ebdacde`).

## 3. Mã: vị trí và cách chạy (trên nhánh `thu-phong-cach`)
Chuẩn bị worktree: `git worktree add <dir> thu-phong-cach`, rồi `ln -s /home/user/cine-lab/node_modules <dir>/node_modules` (hoặc `npm ci`; xem `scripts/env/setup.sh` bước 5). Render nặng đi qua hàng đợi: `bash scripts/render/queue.sh <PHIÊN> <nhãn> -- <lệnh>` (làn nặng mặc định; `LAN=nhanh` cho việc < 60 s).

| Việc | Tệp | Cách chạy |
|---|---|---|
| Cờ phong cách | `design/m3/thu-phong-cach/style.js` (B3 v1, B1), `style_v2.js` (b3v2 và **b3v3**: `o.style === 'b3v3'`), `lamp_shot.js` (đoạn 20 s `lp20`); móc 3 chỗ trong `design/cong5/layout/page.js` | bật bằng `dbg.style = 'b3' \| 'b1' \| 'b3v2' \| 'b3v3'`; tắt cờ thì 0 px với ebdacde |
| Driver render theo shot | `design/m3/thu-phong-cach/frames.js` | `node design/m3/thu-phong-cach/frames.js --shot s22 --out <dir> --dbg '{"style":"b3v3"}' [--all] [--frames 1440,1452] [--w 1920 --h 1080] [--tag x]` |
| Kiểm 0 px khi tắt cờ | `so_px.py` | so ảnh render bằng page.js gốc (`--page-file`) và page.js nhánh |
| Bộ mẫu dữ liệu B3 (5 khung D-MAP, D-BAR, D-TL, D-NUM, D-COL) | `bo_mau.py` (+ `data_frame.py`, `data/panel_*_v3.png`) | `/opt/cine/bin/python design/m3/thu-phong-cach/bo_mau.py <dir>` |
| Đo tương phản chữ trong clip | `tuong_phan_clip.py` | `/opt/cine/bin/python … tuong_phan_clip.py <clip.mp4>` |
| Đo phân dải trên dải JPEG | `phan_dai.py` | `/opt/cine/bin/python … phan_dai.py <dải.jpg> …` |
| Ảnh trước/sau | `truoc_sau.py`, `truoc_sau_v2.py` | |
| Dải kiểm mù thứ 4 (dữ liệu + 20 s) | `dai4.py` | |
| Animatic: nhịp flite → Bill 141,2 wpm | `design/m3/animatic/nhip.py` | `python3 design/m3/animatic/nhip.py <dir>` → `nhip.json` + wav từng câu |
| Animatic: thẻ dữ liệu / placeholder | `the.py` | `/opt/cine/bin/python design/m3/animatic/the.py <dir>` |
| Animatic: khung tĩnh b3v3 | `frames.js --mid` (mỗi shot nguồn) | |
| Animatic: dựng | `dung.py` | `/opt/cine/bin/python design/m3/animatic/dung.py <nhip.json> <dir wav> <dir still> <dir thẻ> <dir làm việc> screening/ll-ep01-animatic.mp4 1.00 1` (mức tốc độ; `1` = cắt đoạn 07) |
| Animatic: đo tương phản phụ đề | `do_phu_de.py` | trên chính mp4 |
| Đóng gói / đo da (thử mặt, đã bỏ) | `design/cong7/thu-mat/dong_goi.py`, `do_mat.py`, `frames.js` (nhánh `thu-mat`) | chỉ tham khảo |
| Kiểm mù | `scripts/p/kiem_mu.py` (nhánh P) | `dai <video> <t0> <t1> <ra.jpg> [bước]` · `doi-chung-dai <dir>` (Sprite Fright, KHÔNG commit) · `chuan-bi-dai <dir> nhãn=ảnh …` · `nguyen-van <dir> <ra.md> <tasks_dir> <agentId>=<tên mù> …` · `dem <NGUYEN-VAN.md>`. Chạy bằng `/opt/cine/bin/python` (cần PIL). Mỗi dải một subagent MỚI, câu hỏi nguyên văn (xem `reports/m3/THU-PHONG-CACH.md` §9; thêm câu chấm 1–10 và câu nhớ số liệu) |
| Luật máy (Last Round) | `scripts/p/layout_full.sh`, `checks/run.py` (P chỉ CHẠY, không đọc mã `checks/`) | profile `shot` / `youtube` |
| Đo judder | **chưa có công cụ trong repo** | cần viết ở M2.2 (xem mục 6) |

**Tài sản đã có trong git (nhánh P):**
- bộ mẫu dữ liệu `reports/m3/thu-phong-cach/bo-mau-du-lieu/*.png`;
- khung B3 v3 `reports/m3/thu-phong-cach/M2-0/`;
- giọng mẫu `reports/m3/m2-0/giong-mau/*.mp3`, `reports/m3/m2-1/bill-*.mp3`;
- animatic + `nhip.json`, `thuc-te.json`, `ll-ep01-animatic.en.srt`;
- bảng shot JSON trong `BANG-SHOT-M2.md`.
- Nhạc tạm nằm trên nhánh `thu-phong-cach`: `design/m3/animatic/audio/freesound-496757-erokia-ambient-wave-48.mp3`.

**Không đưa vào git (tạo lại bằng lệnh trên):**
- khung tĩnh và wav làm việc của animatic (`/var/tmp/cine-out/…` của xưởng);
- render 1080p thô;
- master tập (≈ 2 GB; theo quyết định: thử GitHub Release, không được thì giữ trên container + bản xem ≤ 90 MB trong repo).

## 4. Môi trường
- Cloud `cine-lab-av`. Đầu phiên chạy `bash scripts/env/verify.sh` (11 PASS). Python `/opt/cine/bin/python`, Blender `/opt/bpy/bin/python`, Chromium `/opt/pw-browsers`.
- **node_modules:** repo chính có sẵn. Worktree mới KHÔNG có: liên kết `ln -s /home/user/cine-lab/node_modules node_modules`, hoặc `npm ci` (khoá three.js theo package-lock; `verify.sh` kiểm phiên bản).
- **ElevenLabs:** proxy tự gắn khoá cho `api.elevenlabs.io`. Không commit khoá, không cần biến môi trường.
  - Giọng kể: **Bill**, premade "Bill – Wise, Mature, Balanced", voice_id **`pqHfZKP75CvOlQylNhV4`**.
  - Model `eleven_multilingual_v2`; stability 0,5, similarity_boost 0,75, style 0, speaker boost bật; **tốc độ 1,00**. Tham số `speed` 1,05 đo được không tác dụng.
  - Đo thật: 141,2 từ/phút.
  - Giọng Ida: "CINE-LastRound-Lamplighter-V3" `59pjz3MTZdh9U1AETKfW` (eleven_v3); animatic dùng lại take C4-D1 L1, L2.
  - **Gói:** chủ dự án đã nâng Creator (121 000 credits/tháng, dùng chung với Crux). Lúc bàn giao, API `/v1/user/subscription` vẫn báo `starter`, đã dùng 84 839 / 105 779 (đọc 01/10). Kiểm lại trước khi thu.
  - Quy tắc: ghi số dư trước và sau mỗi lượt đọc.
- **Nhạc tạm:** Freesound #496757 "Ambient Wave 48 (Tribute)", tác giả Erokia, **CC0**, do người làm (RIGHTS M2-MUS-1). Không dùng nhạc AI, không YouTube Audio Library.
- **Mạng:** Full (chủ dự án mở 01/10). Riêng `bls.gov` chặn truy cập tự động (Akamai 403), không phải proxy.

## 5. Quyết định còn hiệu lực (AUTHORSHIP, các dòng 01/10/2026)
| Quyết định | Dòng AUTHORSHIP |
|---|---|
| Trục kênh: nghề xưa ↔ nghề hôm nay dưới AI và công nghệ; truyện có thật, không cận mặt người, 2.5D, tập 8–12 phút | "Định hướng" (chuyển hướng; tên kênh) |
| Tên kênh **Last Lamplighters**; khẩu hiệu gợi ý "Every era has its last lamplighters" | "Định hướng" (chọn tên) |
| Tiêu chí đi tiếp: chủ dự án chấm ≥ 8/10; ≤ 0,3 triệu token/phút; một tập trong một chu kỳ tuần; người xem nhớ ≥ 2 số liệu | "Định hướng" (tiêu chí) |
| **B3** cho phần truyện (chủ dự án chấm ≥ 8/10); đổi cỡ cảnh s03/s05/s22; đèn lồng rọi thành vũng sáng | "Last Lamplighters (Mốc 1)" |
| 4 số neo (40 000 · 5 · 1 trong 270 · −34 %); ghi cả 1 500 (2015) và 1 100 (2023); bỏ Düsseldorf/Berlin; 6 tập theo thứ tự 1, 2, 3, 6, 4, 5; "Ida thắp một ngọn đèn cho mỗi nghề"; **KHÔNG trích Anthropic Economic Index** | "Last Lamplighters (Mốc 1)" (duyệt cả gói) |
| Giọng kể **Bill**, tốc độ 1,00 | "Last Lamplighters (Mốc 2)" (chọn Bill) |
| **Cắt đoạn 07** nếu > 10:00; animatic đã cắt, 9:37,5 | "Mốc 2" (gói kế hoạch) |
| **s22 dùng góc máy v3** (thấy cột điện mé đối diện ở rìa khung); BANG-SHOT §1 còn ghi "không có cột điện trong khung" (B3 v2), **cần sửa theo v3** | "Mốc 2" (duyệt M2.0; s22 đạt) + chỉ thị bàn giao |
| **3 Shorts**: S1 London (đoạn 08), S2 nghề hôm nay (đoạn 12), S3 "One job in 270" (đoạn 11) | chỉ thị bàn giao; chi tiết `M2-1-ANIMATIC.md` §5 |
| **Tỷ lệ 20/35/45** | chỉ thị bàn giao 01/10; **chưa ghi rõ trong repo đây là tỷ lệ gì** (ví dụ STORY/DATA/…?). Phiên mới XÁC NHẬN với chủ dự án và ghi vào AUTHORSHIP |
| Nâng ElevenLabs **Creator** (dùng chung Crux) | "Mốc 2" (nâng Creator) |
| Thẻ Bessen: "Only 1 of ~270 occupations was eliminated mainly by automation" (đã áp trong animatic) | "Mốc 2" (sửa nhỏ b) |
| s03/s05 bóng quá tối → viền sáng 2,5–3 px hoặc nền sau bóng sáng hơn một bậc, làm trong M2.2 | "Mốc 2" (sửa nhỏ a) |
| Nhạc CC0/CC BY do người làm; master ngoài git; P soạn sẵn yêu cầu gửi K, chưa gửi | "Mốc 2" (gói kế hoạch) |

## 6. Chuẩn đã đặt và bẫy đã gặp
- **Kiểm mù:** mỗi dải một subagent MỚI; câu hỏi nguyên văn + chấm 1–10 + (dải dữ liệu) nhớ số liệu; 2 đối chứng Sprite Fright (Ellie 104,5 s; Victoria 332 s) dùng chung, KHÔNG commit (RIGHTS REF-SF-HC). Mốc đã đo: B3 4,75; B3 v2 4,50; đối chứng 6,5. Mỗi dải ≈ 44–46 nghìn token. Một người chấm mỗi dải nên ±1 điểm là nhiễu.
- **Judder** (chủ dự án nêu): khung tĩnh pan/zoom và chuyển động máy trong animatic có thể giật ở 24 fps. **Chưa có công cụ đo trong repo.** Đề xuất ở M2.2: đo dịch chuyển giữa khung (optical flow trên vùng tĩnh) và đặt chuẩn trước khi dựng thật.
- **flite kéo giãn:** nháp flite đọc nhanh nên `nhip.py` dùng atempo 0,683–1,039 để quy về 141,2 từ/phút; giọng nghe kéo dài và méo ở hệ số thấp. Chỉ dùng để đo nhịp, không để duyệt cảm xúc.
- **Bóng ma** (B3 v2): khối thân mờ + quầng 10 px → đọc "nửa trong suốt". Đã bỏ ở b3v3.
- **Bóng chìm** (b3v3 s03/s05): bóng đặc quá tối, chìm vào tường → sửa ở M2.2 (viền 2,5–3 px hoặc nền sáng hơn một bậc).
- **Nguồn sáng ngoài khung đọc là vô lý:** người xem không thấy nguồn thì chê "đèn pha không rõ từ đâu". Luôn cho thấy mép nguồn (s22 v3).
- **Khoá ElevenLabs của proxy thiếu quyền:** `/v1/history` trả 401 (thiếu `speech_history_read`), nên không quy được phần tiêu thụ của dự án khác. Chủ dự án ghi nhận thiếu cả `user_read`; trong phiên này `/v1/user/subscription` vẫn trả 200. Phiên mới kiểm lại; nếu không đọc được số dư thì ghi "không đọc được", không đoán.
- **Bộ đếm ký tự** tăng ít hơn số ký tự gửi (300 cho ≈ 1 125; 150 cho 375), và tăng khi phiên không gọi (dùng chung Crux). Luôn đọc trước và sau.
- **bls.gov chặn tự động** (Akamai 403 với curl và WebFetch). Đối chiếu qua Wayback hoặc FRASER; chủ dự án ghi các số BLS chính "đã đọc toàn văn (Claude)".
- **Worktree cần node_modules** (liên kết hoặc `npm ci`); thiếu thì render lỗi ngay.
- **Container khởi động lại** (≥ 6 lần ở Cổng 6): mất lệnh nền và render dở, đĩa còn. Chạy việc dài bằng `setsid nohup … & disown`, chờ bằng `tail --pid`, commit sau mỗi bước, nối lại subagent bằng SendMessage.
- **Subagent không ghi được tệp .md** trong một số cấu hình: P lưu nội dung từ lời trả về (đã gặp ở M2.1).
- **Hạn token subagent hay vượt** (kịch bản V2 +35 %, series +31 %, kế hoạch +37 % theo bộ đếm harness): ghi cả số tự báo và số harness.
- **Vân giấy B3 neo theo khung đầu shot** (đã sửa ở v3). Render khung lẻ phải trùng render nối tiếp.

## 7. Việc tồn
1. **Tra nhãn hiệu** "Last Lamplighters" (USPTO, EUIPO, UKIPO) trước khi mở kênh. Đọc chính sách YouTube hiện hành về nội dung AI và nhãn "altered or synthetic content".
2. **Yêu cầu gửi K** (C3 cho nhân vật dạng bóng; profile luật Shorts 9:16): bản nháp `reports/m3/YEU-CAU-K-NHAP.md`, **chưa gửi**; chờ chủ dự án cho phép rồi chuyển vào `checks-appeal.md`.
3. **Lỗi thẻ "+30 %"** (13-02): thẻ ghi "+30% or more" vì kịch bản không có số riêng cho từng nghề tăng. Cần số có nguồn (BLS 2025–35: nurse practitioners +41,0 %, solar PV installers +36,5 %, data scientists +34,6 %, wind turbine techs +29,5 % — xem V2 D30) hoặc bỏ thẻ. Xử lý ở kịch bản v3.
4. **Thẻ kết tràn** (chủ dự án nêu): thẻ kết kênh (14-04) bị tràn chữ hoặc khung. Sửa trong `the.py` / bộ mẫu ở M2.2a.
5. Thẻ −34 % ở 12-01 chỉ đứng 2,3 s → giữ làm lớp trên 12-02 để đứng ≥ 5 s.
6. 11 thẻ PLACEHOLDER, 6 bản đồ dùng khung chung, 13 khung TEMP (danh sách: `M2-1-ANIMATIC.md` §3).
7. Sửa BANG-SHOT §1 cho s22 theo góc máy v3.
8. Thu trọn lời dẫn bằng Bill khi API báo Creator (≈ 7 400 ký tự; đoạn 07 đã cắt).
9. Tồn đọng Cổng 6 (nếu dùng lại shot Last Round): continuity K1, K3 s06; K4/L7 s24c; K6; K7 (xem `CONG-6-DONG.md` §4).

## 8. Token đã dùng ở m3 (bộ đếm harness, để ước ngân sách)
| Gói | Token |
|---|---|
| Thử phong cách B3 + B1 | ≈ 272 nghìn |
| Kiểm mù Mốc 1 (10 dải) | ≈ 450 nghìn |
| Kịch bản v1 / v2 / series | ≈ 118 / 203 / 131 nghìn |
| Kế hoạch tập thử + bảng shot | ≈ 164 + 22 nghìn |
| B3 v2 + kiểm mù 4 dải | ≈ 84 + 180 nghìn |
| M2.0 xưởng | ≈ 75 nghìn |
| M2.1 xưởng | ≈ 94 nghìn |

## 9. Các worktree còn trên đĩa (cục bộ, có thể dọn)
`.claude/worktrees/agent-a76cbe2e4cde117cc` (thu-phong-cach, sạch), `agent-ae1abc4c7355404b0` (thu-mat), `agent-ada79b0ee6f3b75ac` (thu-mat-2), `agent-a0a21a7b7afaa669a` (cong6-w1-v3), `agent-ac1ac7e44143e484b` (cong6-b34). Không có thay đổi chưa commit trên các nhánh cần cho LL.

## 10. Commit bàn giao
Nhánh `ccr-af7a498d-ss3snk`: commit chứa tệp này (xem `git log -1 -- reports/m3/PLAN-HANDOFF-LL.md`).
