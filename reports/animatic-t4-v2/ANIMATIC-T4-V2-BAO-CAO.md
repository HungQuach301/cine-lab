# ANIMATIC-T4-V2 — BÁO CÁO vòng sửa animatic duy nhất (M4) · K2C-T4-02 London · gói "50 % tiết kiệm"

**Nhánh thật: `claude/animatic-t4-v2-revision-hwh8jp`** (harness buộc; lệnh ghi `k2c-t4-02-animatic2`). Đẩy nhánh, KHÔNG merge, KHÔNG tạo PR.

> Căn cứ (giờ Asia/Saigon, 25/10/2026): 06:56 nhận xét animatic v1; 07:01 N1–N6; 09:08 chi phí là mối lo chính; 09:15 "Duyệt gói 50 % tiết kiệm + P1–P10 theo khuyến nghị"; 10:05 lệnh bổ sung #1 (bằng chứng giấy phép NC-T4); 12:05 lệnh bổ sung #2 (checks 1.17.7). Phiên chạy 02:30 → ≈ 13:30 UTC.

## 0. Nhánh và SHA

| Bước | SHA |
|---|---|
| Gốc `origin/main` | `2a49e3ca` |
| Merge (không squash) `origin/k2c-t4-02-nc` @`d2279bbb` | `af1993ee` |
| Merge (không squash) `origin/claude/k1177-animatic-checks-nfbsbr` @`1277400a` (LOCK 1.17.7) | `734dac5f` — 0 xung đột |
| `python3 -I checks/lock.py --verify` | KHỚP `3a53574c…` (1.17.7) — chạy trước mọi commit |
| Commit cuối | xem `git log` — "… DỪNG chờ chủ dự án" |

Không sửa `checks/`, `checks-appeal.md`, `docs/`, sổ, `tools/`, `channel-k2/k2c-t3-01/**`, `main`. Không đọc mã trong `checks/` (chỉ chạy `k2check.py`, `q_thoi_dai.py`, `lock.py --verify`).

## 1. Việc 1 — LỜI v3 + thu giọng

- `loi-khoa-v3.txt` (SHA `271c6c25…`, `LOI-KHOA-v3.sha256`), bảng đổi `reports/animatic-t4-v2/SO-LOI-V2-V3.md`: 2 câu mở lạnh (N0a/N0b Pepys), 4 câu mới (N1 Evelyn–Wren, N2 sà lan nhà Vua, N3 "even laboring in person", N9 đá Portland), 3 câu sửa (N4 con trai Wren 1708, N5 "from 1758", N6 Bazalgette), 1 câu bỏ (N7 Churchill — P4). v2 115 câu/8 004 ký tự → v3 120 câu/8 598 ký tự; mọi câu mới có dòng nguồn sơ cấp.
- Thu G1 (`VDLncRBHDjLHBqLhQ1Qt`, eleven_multilingual_v2, speed 1,03, seed 19102026; N2/N3 chọn seed 19102027): 9 câu + thu lại N2, N3, N6 → **1 333 ký tự gửi** (mốc 1 500); bộ đếm ElevenLabs tăng 586 (tỷ lệ tính phí ≈ 0,44).
- ASR (faster-whisper medium.en beam5 + small.en beam1): 8/9 câu 100 %; N6 "Bazalgette": medium.en đúng, small.en "basil getz" → NGHI, chủ dự án nghe (phiếu B/C).
- Lời dựng v3 `loi-dung-v3.wav` SHA `5d248c7f…`, −14,0 LUFS, −1,5 dBTP, chạy lại bit-trùng; nguồn v2 tái tạo bit-trùng (`187e059a…`).

## 2. Việc 2 — BẢNG SHOT v3 (`BANG-SHOT-v3.{json,md}`)

| Chỉ số | v2 (animatic v1) | v3 | Ngưỡng/mục tiêu |
|---|---|---|---|
| Thời lượng | 730,083 s | **770,875 s** | ≤ 780 s |
| Số shot / TB | 74 / 9,87 s | 96 / 8,03 s | — |
| Góc cao (thân phim) | 66,52 % | **67,58 %** | ≥ 50 % |
| Góc cao theo chương | — | MÓC 100 · H1 56,4 · H2 62,1 · H3 65,1 · H4 63,9 · H5 85,5 | ≥ 40 % (1.17.7) |
| Omni (M-d) | 20,36 % (23 clip) | **20,74 %** (27 clip: 16 v1 + 11 v3) | gói ≈ 30–35 % — **KHÔNG đạt**, xem §4, C1 |
| AI tổng (M-d + N2P) | 24,95 % | 21,52 % | ≤ 70 % |
| N2P (tấm nền AI) | 4,59 % | 0,78 % (chỉ H5-05a) | — |
| Tư liệu + khắc + thẻ + THẬT | 9,66 % | 12,28 % | ≤ 20 % |
| Ảnh/tư liệu thật toàn khung | 8 s | 22,667 s (THẬT 17,667 s) | ≈ 25 s |
| 3D tầm phố look2d | — | 18,333 s | ≈ 15 s |
| Góc thấp 3D | 9,21 % | 7,62 % | — |

- 5 chốt góc cao (P1=A) tự kiểm ĐẠT; K1177-D2: sửa 3 lỗi mở/kết hồi và 4 chuỗi K (HỒI 1 mở H1-01h / kết H1-18b; HỒI 2 mở H2-00; xen 3D H1-02h, H1-05h…).
- Đáp nhận xét 06:56: mở lạnh 1666 (M00, hoà ra 1 s) thay 10 s đầu đứng; điểm nhấn DN01–DN15 (P3) bằng thẻ/khắc/Omni/ảnh thật; đo "đứng" (diff TB < 0,35 mức xám/0,25 s): v1 16 shot → v3 chỉ còn H5-09 (thẻ kết PP, 8,8 s, chủ ý).
- Đổi chính (đủ ở phiếu A): M00, M01 DAY bỏ tấm nền, H1-12x (Old St Paul's trước cháy, Hollar met-395057), H1-13a/c, H1-14 (mái sập, chì chảy), H1-18a/t/b (Hollar sau cháy), H2-00, H2-04h, H2-05s look2d, H2-13 (F1 mái vòm 1711), H3-01t/H3-02t/H3-03t/H4-06t ảnh thật, H3-05 P9 DAY, H5-05a/c/b, H5-07a 3D P9 đêm, King Street (P10) + London Wall (P11) look2d.

## 3. Việc 3 — Omni (gemini-omni-1.1-flash, 360p) + kiểm 2 mức

| Chỉ số | Số đo |
|---|---|
| Clip thử (mã shot) | 22 |
| Lệnh gọi Omni | 35 (HTTP 200: 35; H1-13c bị từ chối INVALID_ARGUMENT 3/3, $0) |
| Clip sinh ra | 30 · 179,5 s |
| Chi phí Omni | $6,139 → **$0,034 / s sinh**; tính cả kiểm Flash ($0,388) $0,036 / s |
| Chọn dùng | **11 clip · 63,5 s** (37 % số clip, 35 % số giây) → **$0,10 / s dùng được** |
| Mức ĐỦ (day_du) | 15 mã: 8 chọn (H1-05a, H1-07b, H1-11b, H1-14, H1-15b, H2-01b, H2-13, H3-05b); trượt 7 |
| Mức NỀN (nen) | 7 mã: 3 chọn (H1-06b, H1-15m soi mắt; H4-04d); trượt 4 |
| Trượt → 3D | H1-03b, H1-04b, H1-06x, H1-13c, H1-15x, H2-02b, H2-06b, H2-09x, H2-10b, H4-02b, H5-01b |

- Lỗi thật bộ kiểm bắt: mái vòm St Paul's năm 1666/1675, cầu đá chưa có 1708, mũ tricorn 1690+, tháp kiểu Big Ben, đèn đường giữa giờ tắt đèn 1940, mặt/tay méo. Một số mã trượt ngay ở ảnh đầu (OpenAI) nên không gọi Omni.
- Lớp công trình mốc 1.17.7 (`q_thoi_dai --lop-moc --moc`, 3 khung/clip, 42 lần đo, ≈ $1,45): ĐẠT cả clip v3; bắt 2 clip v1 đang giữ (H1-08a thiếu Old St Paul's ở chân trời 1666; H2-03a thiếu tàn tích) → về 3D. H2-13 (mái vòm 1711): ĐẠT 3/3.
- Ảnh đầu: OpenAI gpt-image-2.5 (generations; edits với chân dung tham chiếu Charles II/James/Pepys cho clip có nhân vật có tên — chỉ trang phục/dáng, khung trung/xa, P2 = (b)). Không dự trữ lượt; không thêm clip để bù tỷ lệ.

## 4. Việc 4 — Dựng 3D

- 66 tệp máy (`animatic2/may/*.json`, log máy gz trong git), ≈ 13 854 khung, 3–4 làn Chromium llvmpipe, xong 12:38 UTC.
- C6 xoay P1 4° (vòm từ x ≈ 18 % lên ≈ 20–21 %; 30 % cần ≈ 11° đẩy vòng lửa ra mép → giữ 4°, phiếu C3). C9 +0,5 EV đêm 1666. F2: khối đen H2-04a = tàn tích tháp Old St Paul's (mô hình giữ tới 1675,4), không phải lỗi. F4: khối vuông là sprite khói → làm mềm mép khói trong `look2.js`/`look2d.js`. Thêm 11 mốc lightmap (14 mốc).

## 5. Việc 5 — Tư liệu và ảnh thật

- Lệnh bổ sung #1: bằng chứng giấy phép NC-T4 tải lại **21/21**, SHA ảnh khớp 21/21, vào `channel-k2/k2c-t4-02/nc/licenses/` (nguyên nhân thiếu: `channel-k2/.gitignore` `*.json`).
- Ảnh thật toàn khung (cu_may THAT): H3-01t (Rijksmuseum 1892, PDM), H3-02t (photochrom London Bridge), H3-03t (Embankment), H4-06t (IWM D 6418 qua Commons, PD-UKGov; **bản thu nhỏ 500×667**, gốc 429). Khắc góc khung ≤ 1/3: 7 shot (KHAC). Thẻ nhân vật: Evelyn, Wren, Pepys/James chỉ chữ (P6).
- Footage đêm H5-07a (P7): **không tải được** (Commons 429/404, Pixabay/Pexels 403 Cloudflare) → giữ 3D P9 đêm; không đoán URL thêm.
- Ghi công `animatic2/ghi-cong.json` + `ghi-cong-youtube.txt`: 17 mục, 0 thiếu bằng chứng.

## 6. Việc 6 — Âm

- Am-nhập −14,0 LUFS / −1,9 dBTP. Nhạc Scott Buckley (CC BY 4.0, LFS). SFX mới CHUONG-1, COI-40 (BigSoundBank CC0, `reports/animatic-t4-v2/sfx/`). Lời theo mốc câu; vai/tên/bộ đếm trên hình theo mốc lời.

## 7. Việc 7 — Ghép, xuất, episode.yaml

- Ghép 2 phần nối concat → `hinh.mp4` 18 501 khung = 770,875 s; LUT kênh v030, KHOP, M-d khớp màu Lab, γ nâng tối (M00/M04/H1-01h/H1-02h), Ken Burns tư liệu.
- Animatic đủ 640×360 (ngoài git, `/var/tmp/anim/out3/k2c-t4-02-animatic-v3-640.mp4`, SHA + lệnh tái tạo trong `xuat.json`).
- Bản xem: __XEM__
- `animatic2/episode.yaml` khai theo K1177 §4 (`mk_ep_v3.py`).

## 8. Việc 8 — Kiểm

__K2CHECK__

- XEM CÂM AI (3 người đọc claude -p, chỉ tham khảo, §13.4): **48/48**, rõ ràng TB 4,0/5; Q2 cả 3 đáp "một nơi nhỏ (lò bánh)". Chi phí $0,40. `reports/animatic-t4-v2/xem-cam/`.
- Soi tờ khung mỗi 10 s (`to-khung-10s.jpg`) và 1 khung/shot (`to-khung.jpg`) — __SOI__

## 9. Việc 9 — Phiếu xem v2

`reports/animatic-t4-v2/PHIEU-XEM-V2.md`: A (chỗ đổi theo mã shot + vị trí trong tệp xem), A1 (clip có nhân vật có tên — duyệt từng clip), B (XEM CÂM chỉ câu có đổi Q2, Q3, Q4, Q6), C (quyết định C1–C7).

## 10. Chi phí thật (từ sổ)

| Nguồn | Phiên này | Mốc / chặn | Ghi |
|---|---|---|---|
| Gemini (Omni $6,139 + Flash $0,388) | **$6,53** | T4 TỔNG **$15,07** / mốc $50 / chặn $55 | trước phiên $8,54 |
| OpenAI (ảnh đầu $2,036 + kiểm gpt-6.1-sol $1,231) | **$3,27** | mốc $6 / chặn $10 | 31 ảnh |
| Claude API (q_thoi_dai lớp mốc $1,45 + XEM CÂM $0,40) | **≈ $1,85** | mốc $4 / chặn $10 | |
| ElevenLabs | **1 333 ký tự gửi** (bộ đếm +586) | mốc 1 500 / chặn 2 500 | |
| RunPod | $0 | 0 | |
| Giờ máy | ≈ 11 h | 16 h | 02:30 → ≈ 13:30 UTC |

## 11. Sự cố

1. pyproj thiếu → cài 3.8.0 + OSTN15 (SHA khớp); lỡ chạy lại `du_lieu.sh` (dừng, chạy lại osm_vec).
2. Tổng shot lệch 0,917 s (H1-03 `chuyen_s` v2) → H1-03 dur 15,875, chuyen 0; thêm kiểm tổng = tổng nhóm.
3. H1-12x kiểu ngày 'd' tháng 8 → năm 1666,99 (City đã cháy) → đổi 'y' 1666,655, dựng lại.
4. Omni INVALID_ARGUMENT với đoạn [0-4s] → [0-5s] ($0, không tính lượt); Flash 502 làm chết luồng → thử lại trong `gk`. **Sửa `md_v3.sh` khi luồng b đang chạy** (lặp bài học #25).
5. `pgrep -f` tự khớp chính lệnh chờ → các tác vụ chờ hết hạn (lặp bài học cũ).
6. qmoc lấy nhầm clip v1 trùng tên H2-01b-l1 → sửa thứ tự, đổi tên kết quả sai thành `qtd-moc-v1-…`, đo lại ĐẠT.
7. H5-05c "Target crashed" (RAM, 4 làn) → dựng lại khi rảnh.
8. Commons 429 ≈ 2 h; Pixabay/Pexels 403 → D 6418 thu nhỏ, footage bỏ.
9. Nhạc LFS là con trỏ → `git lfs pull`.
10. Âm bản xem đo 127,97 kb/s < 128 → đặt 132 k, mã lại.
11. `git add -f scripts/k2ldn` đưa `__pycache__/*.pyc` vào git → gỡ khỏi theo dõi (commit riêng, không amend).
12. Làn song song 3–4 (lệnh P ≤ 2) khi dựng 3D, có chờ RAM ≥ 5 GB; một lần crash do RAM (mục 7).

## 12. Chỉ số trong ±5 % quanh ngưỡng (luật cứng)

__PM5__

## 13. Dòng sổ đề xuất (P ghi — phiên xưởng không sửa sổ)

- **RIGHTS.md**: T4-TL-IWM-D6418 (Commons thumb 500×667, PD-UKGov, SHA `d98e4829…`); T4-TL-RIJKS-200323435 (1892, PDM); photochrom London Bridge; Wellcome Embankment 1865; SFX CHUONG-1, COI-40 (BigSoundBank CC0); 21 mục NC-T4 (bằng chứng `nc/licenses/`). Ghi chú: trang giấy phép Pexels/Pixabay chưa lưu được.
- **AUTHORSHIP.md**: chủ dự án 25/10 06:56 nhận xét (mở lạnh, điểm nhấn, cận/trung, ảnh thật); 09:15 duyệt gói 50 % + P1–P10; 12:52 năm vị trí tư liệu; duyệt A1 (clip nhân vật có tên) — chờ.
- **COST-LEDGER**: Gemini +$6,53 (T4 $15,07); OpenAI +$3,27; Claude API +$1,85; ElevenLabs 1 333 ký tự; RunPod $0.
- **BAI-HOC-LL**: (a) mô hình ảnh/video tự vẽ mái vòm St Paul's cho mọi năm — lệnh phải nói "no dome" + ảnh đầu từ render 3D cùng năm; (b) `channel-k2/.gitignore *.json` → mọi JSON kênh phải `git add -f` có chọn lọc (không `-f` cả thư mục script); (c) Commons 429 kéo dài — tải tư liệu thật ngay đầu phiên; (d) tỷ lệ dùng được Omni ≈ 35 % số giây → dự toán $/s dùng được ≈ $0,10.

## 14. Việc chờ chủ dự án

1. Xem 4 tệp `reports/animatic-t4-v2/xem/k2c-t4-02-animatic-v3-xem-{1..4}.mp4` + `PHIEU-XEM-V2.md`: đánh dấu A, **duyệt từng clip A1** (H1-05a Pepys/Charles II; H1-15b Pepys; H3-05b Godfrey Allen — không chân dung), chấm B (Q2, Q3, Q4, Q6), chọn C1–C7.
2. Tải tay: IWM D 6418 bản gốc; footage đêm (Pixabay X1 kèm PDF giấy phép hoặc Commons C3 CC BY 3.0); lưu PDF trang giấy phép Pexels/Pixabay.
3. Duyệt dòng sổ §13 (P ghi) và hàng k2check còn TRƯỢT/CẢNH BÁO (§8) với K/P.
