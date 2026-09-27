# BÁO CÁO M0 — Cổng 0: năng lực và hạ tầng

Phiên P (điều phối), 26/09/2026. Nhánh `claude/jolly-edison-a4hq3n`.
Mọi số dưới đây là **đo thật** trong phiên này. Script đo và kết quả thô nằm trong `reports/m0/` (bảng tra ở mục 9).
Không sửa `checks/`. Không có chỉ số nào nằm trong vùng ±5% quanh ngưỡng (render 57–63 s/s, C3 2,85–3,15%, WER 4,75–5,25%).

## 0. Tóm tắt

| Tiêu chí Cổng 0 | Kết quả | Trạng thái |
|---|---|---|
| Render ≤ 60 s/giây phim | 2D Canvas 42,1 · three.js 45,3 (có motion blur 8 mẫu); Blender Workbench 42,9 (không blur); EEVEE 384–408 | **Đạt** với (a), (b), Workbench không blur. EEVEE **trượt** |
| Cảnh cảm xúc khó "tin được" với ≥ 3/5 người nghe mù | 12 take đã sinh, đủ từ 12/12 | **Chờ chủ dự án + người nghe** |
| Nhân vật ở 2 phiên lệch tỷ lệ ≤ 3% (C3) | Lệch lớn nhất 1,30% (thân) | **Đạt** |
| Công cụ kiểm L1 chạy được | Việc của phiên K; nhánh này chưa có `checks/` | **Chờ phiên K** |

## 1. Môi trường (bước 0–1)

| Hạng mục | Số đo |
|---|---|
| CPU | **4 vCPU** Intel Xeon 2,10 GHz, không GPU |
| RAM | **15 GB** (16 095 MB), không swap |
| Đĩa trống | **28 GB** đầu phiên → ~11 GB sau khi cài ACE-Step (6,0 GB venv + 10,1 GB trọng số) |
| verify.sh trước sửa | 9 PASS / 1 FAIL (bpy) |
| verify.sh sau sửa | **10 PASS / 0 FAIL** (Blender bpy 5.2.2 LTS) |

Nguyên nhân lỗi bpy: `python3` của VM trỏ tới 3.11 không có `apt_pkg`, làm `add-apt-repository` hỏng; python3.13 thực ra đã có sẵn. Chi tiết, lệnh và lỗi nguyên văn: `setup-fixes.md`. Playwright 1.63 khớp Chromium 1243 sẵn có, không cần cài lại.

## 2. Tốc độ render (bước 2)

Cảnh mẫu chung (`bench/scene.json`): 10 s, 24 fps, 1920×1080, 1 nhân vật đi qua khung, nền 3 lớp chiều sâu (xa/giữa/gần, parallax), một đèn khí ấm; motion blur = trung bình 8 khung con trong màn trập 180°. Mỗi phép đo chạy tuần tự, máy rỗi. Thời gian tính cả khởi động, đọc điểm ảnh và mã hoá H.264.

| Phong cách | Không blur (s/giây phim) | Blur 8 mẫu (s/giây phim) | RAM đỉnh | Ghi chú |
|---|---|---|---|---|
| (a) 2D Canvas trong Chromium | **8,95** (240 khung) | **42,08** (240 khung) | 1,39 GB | Đèn và quầng sáng phải vẽ giả bằng gradient |
| (b) 2.5D three.js (WebGL, SwiftShader CPU) | **8,06** (240 khung) | **45,31** (240 khung) | 1,45 GB | Đèn điểm có bóng đổ thật, sương mù, ACES |
| (c1) Blender Workbench | **42,91** (240 khung) | 483,6 (24 khung, ngoại suy) | 0,89 GB (1,23 GB có blur) | **Không dùng được đèn thật**: Workbench bỏ qua nguồn sáng |
| (c2) Blender EEVEE, 16 mẫu | 407,9 (24 khung, ngoại suy) | 384,3 (6 khung, ngoại suy) | 2,02 GB | Trượt ngưỡng ~6,8 lần. Đo được: bật blur 8 bước không chậm hơn (giả thuyết: mẫu chia theo bước; chưa kiểm mã) |

Quy ra phim 15 phút trên **một** máy: (a) ~10,5 giờ, (b) ~11,3 giờ, Workbench không blur ~10,7 giờ, EEVEE ~102 giờ.

Phát hiện phụ:
- Ở (a) và (b), thời gian vẽ gần như bằng 0. Gần hết chi phí nằm ở bước đọc điểm ảnh và mã hoá PNG trong trang (`toDataURL`, một luồng): 73,6 / 89,5 s. Đổi PNG sang JPEG giảm từ 8,95 xuống **6,59 s/s** (−26%). Còn dư địa tối ưu (đọc điểm ảnh thô, blur thích ứng chỉ ở shot chuyển động nhanh).
- Lần đo mb8 đầu tiên bị nhiễu do tải ACE-Step và subagent chạy chen (46,96 và 46,80). Số trong bảng là lần chạy lại sạch; cả hai lần đều giữ trong `raw/`.
- Biên an toàn còn 25–30% so với ngưỡng 60. Cảnh thật có nhiều nhân vật, nhiều đèn hơn cảnh mẫu, nên cần đo lại ở M1 với shot thật.

Xem: `media/SO-SANH-PHONG-CACH.mp4` (4 ô cạnh nhau), từng bản ở `media/`.

## 3. ElevenLabs — cảnh cảm xúc khó (bước 3)

Câu (bà lão thắp đèn chào con phố lần cuối): *"That's the last one, then. Goodnight, old street. Forty years, every single night. You'll be brighter now. Just don't forget how warm we were."* Câu gửi đi có thẻ diễn xuất của eleven_v3: `[softly] [sighs] [voice breaking] [whispers]`.

| Giọng | Nguồn | Take | Dài (s) | ASR đủ từ | WER |
|---|---|---|---|---|---|
| V1 Maria Moody (bà cụ Mỹ, "octogenarian") | Thư viện chia sẻ | 3 (ổn định 0,5 / 0 / 0) | 15,8–18,1 | 3/3 | 0 |
| V2 Beatrice (nữ lớn tuổi Anh) | Thư viện chia sẻ | 3 | 15,0–16,6 | 3/3 | 0 |
| V3 Giọng thiết kế (Voice Design, mô tả bà cụ Anh ~78 tuổi, khàn, sắp khóc) | text-to-voice/design, **chưa lưu giọng** | 3 preview | 17,7–20,0 | 3/3 | 0 |
| C1 Austin ("timid orphan boy", người lớn đóng giọng trẻ) — câu: *"Please, could you light the old one? The new ones hurt my eyes."* | Thư viện chia sẻ | 3 | 5,3–8,5 | 3/3 | 0 |

- ASR: faster-whisper `small.en`, int8, CPU; 12 file mất 40 s, RAM 1,0 GB. Không có thẻ nào bị đọc thành lời.
- **Bộ kiểm lần đầu báo sai.** Nó báo thiếu "goodnight"/"forty" vì ASR viết "Good night"/"40". Đã sửa chuẩn hoá (số → chữ, "good night" = "goodnight"), không nới ngưỡng. Luật J1 chính thức vẫn là việc của phiên K.
- ASR chỉ chứng minh đủ từ, **không** chứng minh "tin được". Tiêu chí đó cần tai người.
- Chi phí: **1 031 ký tự** (24 723 → 25 754 / 55 779, gói Starter). Độ trễ 2,4–10,7 s mỗi take.
- **Tác dụng phụ:** gọi TTS bằng giọng thư viện làm ElevenLabs **tự thêm** 3 giọng (Maria Moody, Beatrice, Austin) vào "My Voices" của tài khoản. `voice_slots_used` hiện là 1/10.
- Giọng trẻ em: thư viện không có giọng trẻ thật, chỉ có người lớn đóng giọng trẻ (đa số giọng Ấn hoặc giọng "cartoon" phỏng theo nhân vật nổi tiếng; loại vì rủi ro IP). Voice Design cho giọng trẻ em chưa thử.
- Quyền: API trả `notice_period: 730` ngày cho cả 3 giọng thư viện. Chưa trích nguyên văn điều khoản dùng giọng thư viện cho phim bán; đã ghi vào `RIGHTS.md` với trạng thái "chỉ thử M0".

Nghe chấm mù: `NGHE-CHAM-M0.html` (mã A1–A9, B1–B3, M1–M2; khoá mã ở cuối trang và trong `voice/blind-key.json`).

## 4. ACE-Step trên CPU (bước 4)

ACE-Step 1.5, bản `acestep-v15-turbo`, 8 bước, chỉ DiT (không bật LM "thinking"), 60 s, 4 luồng.
Mô tả gửi vào: *"Quiet cinematic theme… solo felt piano, soft sustained strings, distant celesta. Sad, still and tender, slowly opening into a small, warm feeling of hope. Slow tempo, sparse… no drums, no vocals."* Tham số ép thêm: 66 BPM, D minor.

| Lần chạy | Kết quả | Thời gian | RAM đỉnh |
|---|---|---|---|
| 1. Mặc định (VAE chunk 256) | **Bị kernel giết (OOM)** ở bước giải mã VAE, exit −9. Nguyên văn: `Memory cgroup out of memory: Killed process 7354 (python) total-vm:18126852kB, anon-rss:13951028kB` | 127,7 s tới lúc chết | 13,57 GB |
| 2. `ACESTEP_VAE_DECODE_CHUNK_SIZE=64` | **Thành công**, `music/theme-dit-1.flac` | **261 s tổng** = nạp 23 s + sinh 231 s (mã hoá chữ 3,8 s, khuếch tán 78 s ≈ 9,8 s/bước, giải mã VAE ~150 s) | **13,54 GB** |
| 3. Thêm lượng tử int8 cho DiT | Thành công, `music/theme-dit-int8-1.flac` | 267 s | 13,47 GB (không giảm) |

- Tỷ lệ: **~4,4 phút CPU cho 60 s nhạc**; 10 phút nhạc cho phim đích ≈ 45 phút mỗi lượt sinh. Chấp nhận được.
- RAM đỉnh 13,5 / 15 GB. ACE-Step phải chạy **một mình trên một máy**; không chạy chung với render. Bật LM 1,7B chưa thử vì RAM không đủ chỗ (ước thêm ~7 GB ở fp32).
- Đo được từ file (bản 2): 60,0 s, 48 kHz stereo, −22,2 LUFS, LRA 14 LU, tempo phát hiện 64,6 BPM, sắc âm trội A-D-F-E (khớp D thứ), 0,6 nốt khởi/giây (thưa), âm lượng dâng ở giữa và tắt dần 10 s cuối. Chất lượng thẩm mỹ **chờ tai chủ dự án**.
- Lệch phiên bản: `download.pytorch.org` bị proxy chặn nên torch lấy từ PyPI: 2.14.0+cu130 (bản CUDA, nặng), torchaudio 2.11.0. Repo ghim torch 2.10.0. Có cảnh báo DCW rơi về no-op (`pytorch_wavelets`).
- Giấy phép: mã MIT (file LICENSE), thẻ model HF `license: mit`. Dữ liệu huấn luyện chưa rà.

## 5. Song song 2 subagent (bước 5)

Cấu hình: (a) 2D, blur 8 mẫu, 240 khung chia đôi 0–119 / 120–239; 2 subagent `cine-worker` có `isolation: worktree`, chạy cùng lúc.

| Chỉ số | Giá trị |
|---|---|
| Chạy một mình, 240 khung | **420,8 s** |
| Mỗi nửa khi chạy song song | 360,8 s và 360,1 s |
| Tổng song song (từ lúc render đầu bắt đầu tới lúc cái sau xong) | **365,9 s → tăng tốc 1,15×** |
| Tính cả chi phí khởi động agent (15,9 s) | 381,8 s → **1,10×** |
| Ghép 2 nửa so với bản chạy một mình | 240 khung; PSNR trung bình 56,8 dB, thấp nhất 53,6 dB. Khung nguồn giống nhau; chênh lệch chỉ do x264 mã hoá 2 đoạn riêng. **Render xác định.** |

Kết luận: **subagent trong cùng một phiên dùng chung 4 vCPU của một máy**, và một tiến trình Chromium đã dùng gần hết (load ~4). Chạy song song trong một phiên gần như không nhanh hơn. Muốn nhanh phải dùng **nhiều phiên cloud riêng** (mỗi phiên một máy); điều này **chưa đo** ở M0.

Xung đột và sự cố (nguyên văn trong `raw/parallel-summary.json`):
1. Không có xung đột git; merge sạch.
2. **Worktree tạo từ `main`, không phải nhánh đang làm.** Ở bước 6, model sheet chưa có trong worktree. Cả hai agent phải đọc file từ checkout chính bằng đường dẫn tuyệt đối, tức là **thủng cách ly**. Ở bước 5 đã vá bằng lệnh `git checkout <commit> -- <paths>`.
3. Bộ lọc cách ly chặn nhầm `git add reports/m0/parallel`, vì hiểu chữ "parallel" là lệnh `parallel/xargs`. Agent phải vòng qua bằng `git -C`.

## 6. Nhất quán nhân vật (bước 6)

Model sheet dữ liệu: `consistency/model-sheet.json` (đơn vị H = chiều cao đầu, 6 bộ phận đo).
- Hai subagent **tự viết bộ dựng riêng** từ JSON. Cả hai tự chọn Python + Pillow. Cấm đọc mã của nhau và mã cảnh mẫu.
- Shot A: toàn cảnh, đi sang phải, 1 H = 57,1 px. Shot B: trung cảnh, đứng giơ sào sang trái, 1 H = 146,4 px.
- P đo từ **mặt nạ đã render** (`consistency/measure_parts.py`), không dùng số tự khai.

| Bộ phận | Sheet (÷ đầu) | Shot A | Shot B | A so sheet | B so sheet | **A so B** |
|---|---|---|---|---|---|---|
| torso | 1,90 | 1,879 | 1,904 | −1,09% | +0,22% | **1,30%** |
| upper_arm | 0,95 | 0,952 | 0,958 | +0,18% | +0,84% | 0,66% |
| forearm | 0,85 | 0,852 | 0,856 | +0,20% | +0,71% | 0,50% |
| thigh | 1,20 | 1,199 | 1,208 | −0,07% | +0,66% | 0,73% |
| shin | 1,15 | 1,146 | 1,157 | −0,33% | +0,62% | 0,94% |

- **Đạt C3 (≤ 3%)**, lệch lớn nhất 1,30%.
- **Sàn nhiễu của phép đo** (self-test với hình chuẩn, `raw/consistency-selftest.json`): 1,27% khi đầu cao 57 px, 0,31% khi đầu cao 146 px. Ở toàn cảnh, riêng nhiễu đo đã ăn ~40% biên 3%. Luật C3 nên đo ở khung hình có đầu ≥ 100 px, hoặc render mặt nạ ở độ phân giải cao hơn.
- **Công cụ đo của P lần đầu sai.** `minAreaRect` đo đầu elip 57×49 px thành hình vuông 52×52 xoay 45°, sinh ra lệch giả ~8% ở mọi bộ phận. Đã phát hiện khi đối chiếu, thay bằng đo theo trục chính (PCA), và thêm elip vào self-test. Đây đúng là bài học "máy kiểm do người dựng tự viết thì không đáng tin".
- Tỷ lệ khớp, nhưng **chi tiết model sheet không quy định thì trôi**: dáng mũ và dải mũ, mắt/tai, vị trí bàn tay, cách cầm sào, gót chân, bề rộng thân khi nhìn nghiêng (B tự ghi là cần duyệt). Cả hai agent tình cờ chọn cùng quy ước "đầu mút bo tròn nằm trong độ dài". Nếu chọn khác nhau, mỗi chi sẽ lệch khoảng một bề rộng (15–30%).
- Hệ quả cho bible: model sheet phải có quy ước đo (đầu mút, khớp), turnaround, mũ/mặt, và bề rộng theo góc nhìn. Với 2.5D, nên dùng **một rig 3D duy nhất** cho mọi shot để tỷ lệ đúng theo cấu tạo.

Ảnh: `consistency/shots-A-B.jpg`; mã và mặt nạ: `shots/m0-consistency/shot-A|B/`.

## 7. Khuyến nghị phong cách hình

| | (a) 2D vector Canvas | **(b) 2.5D three.js — khuyến nghị** | (c) Blender bpy |
|---|---|---|---|
| Tốc độ | 42 s/s (blur) | 45 s/s (blur) | Workbench 43 s/s không blur; EEVEE 408 s/s |
| Ưu | Hợp thẩm mỹ 2D bảng màu hẹp (R1 Ice Merchants); nhẹ RAM; toàn quyền nét vẽ | Ánh sáng và bóng đổ thật: vàng gas đối lập trắng điện, đúng lõi Ý tưởng A "ánh sáng là nhân vật". Máy quay và parallax thật. Một rig dùng cho mọi shot nên C3 gần như tự đúng | Công cụ chuẩn ngành, Grease Pencil |
| Nhược | Mọi hiệu ứng sáng phải vẽ giả từng shot; nhân vật vẽ lại mỗi shot nên dễ trôi chi tiết (thấy ở bước 6) | Dễ ra "CG rẻ tiền" nếu không làm shader phong cách hoá (toon/NPR, grain, dither); WebGL chạy CPU qua SwiftShader | Workbench không có đèn thật; EEVEE trượt ngưỡng 6,8 lần |
| Tác động | Công thiết kế ánh sáng tăng theo số shot | Thêm một bước M1: làm shader phong cách và bảng style frame | Loại khỏi đường chính |
| Rủi ro | Trần chất lượng ánh sáng | Chi phí tăng theo số đèn có bóng (mỗi đèn điểm = 6 lượt render bóng); Ý tưởng A có nhiều đèn. **Phải đo 8–12 đèn ở đầu M1**; vượt 60 s/s thì bớt đèn có bóng hoặc lùi về (a) | — |

Có thể kết hợp: (b) cho dàn cảnh, ánh sáng và nhân vật; lớp 2D (a) cho hiệu ứng, chữ, grain. Cả hai chạy trong cùng Chromium.

## 8. Khuyến nghị số phiên song song

- **Bài thử (M1–M2): P + K + 2 phiên xưởng**, mỗi xưởng là **một phiên cloud riêng**, không phải subagent. Căn cứ:
  - Một render đã chiếm hết 4 vCPU; song song trong cùng máy chỉ nhanh 1,10–1,15×.
  - ACE-Step cần 13,5 GB RAM nên phải có máy riêng.
- Subagent chỉ dùng cho việc nhẹ, không render: viết mã, soạn manifest, kiểm liên tục.
- Việc cần làm trước khi tăng số phiên:
  - Đo 2 phiên cloud thật chạy cùng lúc (tốc độ, hạn mức dùng chung) ở bước đầu M1.
  - P commit bible và mã chung lên `main` trước khi giao việc, vì worktree tạo từ `main`.
- Phim đích (M4): tăng lên 3–4 phiên xưởng theo số đo M1–M2.

## 9. Bảng tra file

| Mục | File |
|---|---|
| Kiểm môi trường | `verify-before.txt`, `verify-after.txt`, `setup-fixes.md`, `setup-rerun.log` |
| Render | `bench/` (cảnh, driver, `run_bench.sh`, `run_rerun.sh`), `raw/bench-*.json`, `raw/*.mem.json`, `media/*.mp4` |
| Giọng | `voice/el_takes.py`, `voice/asr_check.py`, `voice/takes/*.mp3`, `raw/voice-takes.json`, `raw/voice-asr.json`, `NGHE-CHAM-M0.html` |
| Nhạc | `music/acestep_gen.py`, `music/theme-dit-1.{flac,mp3}`, `music/theme-dit-int8-1.{flac,mp3}`, `raw/music-*.json`, `raw/music-*.log` |
| Song song | `parallel/w1.*`, `parallel/w2.*`, `raw/parallel-summary.json`, `raw/parallel-psnr.log` |
| Nhất quán | `consistency/model-sheet.json`, `consistency/measure_parts.py`, `consistency/selftest_measure.py`, `raw/consistency-*.json`, `consistency/shots-A-B.jpg`, `shots/m0-consistency/` |
| Đo RAM | `peakmem.py` |

## 10. Việc đang chờ chủ dự án
1. Nghe chấm mù `NGHE-CHAM-M0.html` (và gửi cho ≥ 3–5 người nghe mù) → tiêu chí giọng Cổng 0.
2. Chọn phong cách hình, nguồn nhạc, giọng, số phiên song song, allowlist mạng (phương án ở câu trả lời chat và PLAN.md).
3. Dán `scripts/env/setup.sh` mới vào môi trường `cine-lab-av`.
4. Phiên K: công cụ kiểm L1 (tiêu chí thứ 4 của Cổng 0).
5. Duyệt model sheet chỉ là bản thử của Claude. Thiết kế nhân vật thật là quyết định sáng tạo của chủ dự án, ghi vào `AUTHORSHIP.md` ở M1.
