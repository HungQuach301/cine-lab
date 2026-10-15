# PHIÊN NỀN TẢNG — vận hành nhà máy (chủ dự án duyệt 13/10, nhấn GPU 15/10) · báo cáo 15/10/2026

- **Nhánh:** `nen-tang`. Lúc mở phiên `origin/main` (650f05b) **chưa** chứa b9a1368 nên nhánh được tạo từ `origin/k2-visual4` (b9a1368). Trong phiên, main được fast-forward lên `f5ea772` (V4 duyệt), nên nhánh đã **rebase lên `origin/main` f5ea772**. `nen-tang` hiện là fast-forward của main.
- **Phạm vi đã sửa:** `scripts/common/` (mới), `tools/` (mới), `docs/` (trừ `BIBLE-KENH2.md`), `reports/m3/CHUAN-KENH-LL.md` §13–14, `COST-LEDGER.csv` (mới, gốc repo), `reports/nen-tang/` + tệp này. **Không sửa** `checks/`, `scripts/k2/`, `design/`, `channel-k2/k2c-t2-*`. Không đọc mã trong `checks/`. Chỉ đọc dữ liệu `checks/ll/fixtures/k2g01/vo/*.align.json` (xem §3.3).
- **Chi phí:** Claude API **$0 / trần $3** (phiên không gọi `claude -p`). ElevenLabs **0 ký tự**: mọi lệnh `prep` chạy sau proxy chặn, và một lần proxy đã chặn đúng một lệnh gọi TTS (§3.3). Giờ máy ≈ 0,9 giờ, gồm dựng lại nền relief ≈ 10 phút, đo relief ≈ 7 phút, khung vàng 24,5 phút + 3 lượt thử ≈ 6 phút. Token phiên: máy không đọc được trường `usage`, chủ dự án xem trên trang Usage và điền `COST-LEDGER.csv` dòng NT.

## 0. Tóm tắt
| # | Việc | Kết quả |
|---|---|---|
| 1 | GPU / tốc độ | **Không có GPU.** WebGL = SwiftShader (CPU). Relief đoạn H 1080p SPP2: **1,98 s/khung** với 1 tiến trình; **4 tiến trình chỉ nhanh 1,2×** (thông lượng 1,65 s/khung). Nền địa hình chiếm **96 %** giờ khung. Ước tập 10 phút, 50 % relief: **≈ 7,7–9,8 giờ máy** với cấu hình hiện hành. Đề xuất: **thử GPU trước (a)** |
| 2 | Đóng băng phiên bản | `scripts/common/versions.py record/check/show` + `VERSIONS.template.yaml`. Đã thử: đổi một tệp chưa commit trong `design/ll-hero` → CHẶN, mã 1 |
| 3 | Hồi quy khung vàng | `scripts/common/golden.py`: 4 ca, **24,5 phút**. Steel, LL ep08, K2V4: **KHỚP**. T1: **LỆCH CỤC BỘ**, do dòng nguồn (luật V3 38 px) xuống 2 dòng. Thêm 2 phát hiện hạ tầng (§3.3) |
| 4 | Điều lệ phiên | `docs/SESSION-CHARTER.md` (khối điều lệ, "không dừng hỏi lại giữa chừng") + `docs/FILE-ZONES.md` (bảng vùng 6 loại phiên; tệp dùng chung chỉ ghi thêm, mã `<tiền tố>-<số>`) |
| 5 | Preflight | `tools/preflight.sh` + `scripts/common/preflight_scan.py` + `tools/lfs-allow.txt`, có hướng dẫn cài hook. Nhánh này: **ĐẠT**. Quét toàn repo `--all` tìm ra nợ cũ (§5) |
| 6 | RUNBOOK | `docs/RUNBOOK-MOI-TRUONG.md`. Từng nguồn đều chạy thử thật ngày 15/10 (Met API 200 / trang 429; LoC `?fo=json` 200; bls.gov 403; Wayback hết giờ…) |
| 7 | Sổ chi phí | `COST-LEDGER.csv` (11 dòng mốc gốc Steel, T1, V1–V4, kèm tệp:dòng nguồn) + `docs/COST-LEDGER-HUONG-DAN.md` |
| 8 | CHUẨN KÊNH | `docs/CHUAN-KENH-K2.md` (mới: 1 Short, PACKAGING-BRIEF, chủ dự án làm thumbnail, mô tả ≤ 5 000, nguồn ở bình luận ghim, dẫn chiếu Kinh thánh). `CHUAN-KENH-LL.md` §13 và §14 bước 5 sửa theo cùng nguyên tắc |
| — | Ghép thử | main: fast-forward. `k2c-t2` (4977016) và `ccr-bef6f172` (nhánh WIP của T2): **sạch, 0 xung đột** |

**Chỉ số trong ±5 % quanh ngưỡng (luật cứng):**
- Khung vàng K2V4: SSIM **0,9498**, cách ngưỡng tạm 0,90 là 5,5 %, ngoài dải 5 % nhưng sát. Tham chiếu là JPEG 1280×720 của lượt chấm mù nên nhiễu nén cao hơn tham chiếu master.
- Khung vàng T1: SSIM **0,9549** (cách 6,1 %).
- Mô tả gói Steel **5 502** ký tự, **vượt** trần 5 000.
- Mô tả gói T1 **4 585** ký tự (cách trần 8,3 %).

## 1. GPU và tốc độ (ưu tiên)
### 1.1 Kiểm phần cứng (lệnh và kết quả)
| Lệnh | Kết quả |
|---|---|
| `nproc; free -g; grep 'model name' /proc/cpuinfo` | 4 · 15 GB · Intel Xeon @ 2.80GHz (avx2, avx512f, fma) |
| `ls /dev/dri /dev/nvidia*; nvidia-smi; lspci` | không có thiết bị · `nvidia-smi: command not found` · `lspci: command not found` |
| `node scripts/common/webgl_probe.js` (4 bộ cờ Chromium, gồm `--enable-gpu --ignore-gpu-blocklist --use-angle=vulkan` và `--use-gl=egl`) | cả 4: `WebGL 2.0`, renderer **`ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero)), SwiftShader driver)`**, MAX_TEXTURE_SIZE 8192 |
| Môi trường Claude Code của tài khoản (`list_environments`) | 4 môi trường, đều `anthropic_cloud`; không có pool tự host |

**Kết luận:** máy hiện tại không có GPU. Mọi cảnh 3D dựng phần mềm bằng SwiftShader trên 4 vCPU. Ngoài ra `scripts/k2/hero.js:38` và `scripts/ll/hero.js:13` **ghim cứng** `--use-angle=swiftshader`, nên kể cả trên máy có GPU, mã hiện hành vẫn dựng bằng CPU. Muốn dùng GPU phải sửa một dòng trong vùng của phiên V; phiên Nền tảng không sửa.

### 1.2 Đo relief một khung chuẩn
Khung đo: cuộn K2V4, đoạn H (hero `h_hook`, `relief/map`), 1080p, SPP2 + bóng 1024 + viền 12 hướng như V4. Nền `erie` dựng lại trong phiên, **4/4 SHA khớp** `k2v2-mau/relief-erie-meta.json`. Gọi `hero.js --only`, không đổi mã. Số đo đầy đủ: `reports/nen-tang/do-relief.json`.

| Cấu hình | s/khung | Ghi chú |
|---|---|---|
| **1 tiến trình, 24 khung liền** | **1,98** | trạng thái ổn định |
| **4 tiến trình song song, 24 khung liền mỗi tiến trình** | 6,37 mỗi tiến trình → **thông lượng 1,65** | chỉ nhanh **1,2×**: một tiến trình SwiftShader đã dùng gần hết 4 lõi |
| Chỉ nền địa hình (bỏ vùng nổi, tuyến, vòng, nhãn) | 1,91 | nền = **96 %** giờ khung; lớp phủ chỉ 4 % |
| SPP1 | 1,38 | mỗi lượt lấy mẫu ≈ 0,6 s; SPP1 đã bị bác ở V3 vì răng cưa |
| 960×540 SPP2 / 1080p SPP1 (khung rải) | 2,36 / 2,80 | so với 4,31 của 1080p SPP2 khung rải: ≈ 30 % giờ khung không phụ thuộc số điểm ảnh |
| Khung rải 24/120/240/340 (cách đo của V4) | 4,31 | chi phí khởi động và biên dịch shader dồn lên ít khung. V4 ghi 4,15 với cùng cách đo. **Không dùng số này để ước giờ tập** |
| Đối chiếu: V4 dựng trọn 1080p, H, 4 tiến trình | 7,13 mỗi tiến trình → thông lượng 1,78 | `K2V4-BAO-CAO.md` §6 |

### 1.3 Ước giờ máy cho tập 10 phút, 50 % relief (14 400 khung, 7 200 khung relief)
| Phần | Cấu hình hiện hành (4 vCPU, SwiftShader) | Cơ sở |
|---|---|---|
| Cảnh relief 1080p | 7 200 × 1,65–1,78 s = **3,3–3,6 giờ** | đo 15/10 + V4 |
| Cảnh khác (ảnh tách nền, footage, cảnh 3D khác) | 7 200 × 0,3–0,8 s = 0,6–1,6 giờ | V4: footage 0,04–0,07, chân dung ≈ 0,77 s/khung thông lượng. **Ước** theo tỉ lệ cảnh, chưa đo trên tập thật |
| Lớp chữ 2D + ghép | 14 400 × 0,33 s = 1,3 giờ | V4: (3 313 − 2 797,8) s / 1 560 khung |
| **Một lượt 1080p** | **≈ 5,2–6,5 giờ** | — |
| Lượt nháp 540p (tờ khung, G1b) | ≈ 2,5–3,3 giờ | relief 540p ≈ 55 % giờ 1080p (đo khung rải) |
| **Tổng một tập (chưa tính lượt sửa)** | **≈ 7,7–9,8 giờ** | Đối chiếu: T1 (15:41) thật 20,3 giờ, quy về 10 phút ≈ 13 giờ, ở SPP4 với cảnh PBR nặng |

### 1.4 Ba phương án
| | (a) Máy render có GPU | (b) Nhiều vCPU hơn | (c) Cache nền địa hình khi máy đứng yên |
|---|---|---|---|
| Cách làm | Máy Linux có GPU NVIDIA (máy của chủ dự án hoặc VM thuê). Cài repo + `npm ci` + cache (DEM 3,2 GB). Chạy **`claude remote-control`** trong thư mục repo trên máy đó, phiên hiện ra trong ứng dụng Claude Code và điều khiển máy đó. Phiên cloud hiện tại **không** gắn được GPU: môi trường của tài khoản đều là `anthropic_cloud`, 4 vCPU. **Phải sửa** cờ Chromium trong `hero.js` (k2 + ll), ví dụ biến `K2_GL=gpu` → `--use-angle=vulkan`/`--use-gl=egl`. Đây là việc của phiên V | (b1) **Chia việc cho N phiên cloud song song** (mỗi phiên 4 vCPU), mỗi phiên dựng một nhóm đoạn. (b2) Máy/VM 16–32 vCPU qua Remote Control | Trong `relief.js`: khi máy quay đứng yên, giữ ảnh nền địa hình + độ sâu, chỉ vẽ lại lớp phủ và vật trong cảnh |
| Số liệu | **Ước, chưa đo:** phần lấy mẫu/raster (≈ 70 % giờ khung) và đỉnh lưới chạy trên GPU; còn phần CPU (JS, đọc ảnh, mã hoá JPEG) ≈ 0,2–0,5 s/khung → relief ≈ 0,4–1,0 giờ thay cho 3,3–3,6. Lượt 1080p ≈ 2,3–3,9 giờ; tổng tập ≈ 3,5–5,5 giờ | (b1) N = 4: **giờ đồng hồ** relief ≈ 0,9 giờ, **giờ máy không giảm** (≈ 3,4 giờ). (b2) chưa đo SwiftShader trên > 4 lõi; ước 2,5–3,5× trên 16 lõi → relief ≈ 1,0–1,4 giờ | Nền = 96 % giờ khung relief (đo). Nhưng ngữ pháp hình là "máy trượt liên tục" (Kinh thánh §4): cuộn K2V4 có **0 quãng máy đứng yên** giữa các mốc `cam`. Lợi = 0,96 × tỉ lệ khung đứng yên. Ví dụ 10 % khung đứng yên → tiết kiệm ≈ 0,3 giờ/tập |
| Chi phí ước | VM GPU loại T4/L4 khoảng $0,5–1,5/giờ (**giá thị trường ước, chưa kiểm báo giá**) → ≈ $2–8/tập + 0,3 giờ dựng cache mỗi máy mới. Máy của chủ dự án: $0, nhưng chiếm máy | (b1) không tốn thêm tiền máy, nhưng tốn hạn mức phiên. Phải chuyển khung: 0,61 MB/khung → ≈ 4,4 GB/tập chỉ riêng relief, cần kho ngoài (rclone + khoá trong secrets môi trường). Git/LFS không phù hợp. (b2) VM 16 vCPU ≈ $0,5–0,8/giờ (ước) | chỉ công sức mã (phiên V) |
| Chất lượng / rủi ro | GPU raster **không giống bit** SwiftShader (khử răng cưa, độ chính xác) → phải chuẩn lại khung vàng và so SSIM/pHash với SwiftShader trên cuộn K2V4 trước khi dùng cho tập. Rủi ro driver headless, sẵn có GPU, an toàn dữ liệu nếu dùng máy cá nhân | Không đổi hình (cùng SwiftShader, tất định). (b1) rủi ro lệch phiên bản giữa các phiên → bắt bằng `VERSIONS.yaml` | Mã phức tạp: vật dựng trong cảnh đổ bóng thật lên địa hình (D2b) nên phải tách lớp + độ sâu. Dễ lệch bóng và viền. Lợi gần 0 với ngữ pháp hiện hành |
| **Khuyến nghị** | **Thử trước:** 1 buổi, dựng đoạn H + Z của cuộn K2V4 trên GPU. Đo s/khung, chạy `webgl_probe.js` (phải hiện tên GPU) và so với khung SwiftShader bằng `golden.py`. Nếu lệch hình ≤ ngưỡng và relief ≤ 0,5 s/khung → dùng cho T3 | (b1) dùng khi cần **rút giờ lịch** trước một cổng, sau khi có kho ngoài | **Chưa làm.** Xem lại nếu T2/T3 có nhiều quãng giữ máy |

## 2. Đóng băng phiên bản theo tập
- **Công cụ:** `scripts/common/versions.py`
  - `record <episode.yaml> --gate G1` → `<tập>/VERSIONS.yaml`
  - `check <VERSIONS.yaml> [--json …]` lúc G2
  - `show`
- **Mẫu:** `scripts/common/VERSIONS.template.yaml`.
- **Nội dung ghi:**
  - `checks/LOCK` VERSION + TREE_SHA256 và kết quả `lock.py --verify`.
  - 4 nhóm bộ công cụ (`k2v` = design/k2v + scripts/k2, `ll-hero`, `ll`, `shared3d` = design/cong3/shared), mỗi nhóm commit cuối + băm nội dung cây làm việc theo thuật toán LOCK. Băm này bắt cả sửa chưa commit và tệp chưa theo dõi.
  - Giọng ElevenLabs của tập; model Claude ghim, tìm trong `ai.py`/`blind_*.py` của tập.
  - Công cụ máy: Claude Code CLI, ffmpeg, node, Python, three.js, Playwright, Chromium, SHA nền relief trong cache.
- **Lúc G2:**
  - So mọi mục trên. Thêm phép kiểm **model thật đã phục vụ** (trường `served` trong `kiem-mu/cost*.jsonl`) khác model ghim → CHẶN, để bắt chuyển model ngầm.
  - Công cụ máy lệch chỉ BÁO, không chặn.
- **Thử:** ghi T1 → kiểm KHỚP. Thêm một tệp vào `design/ll-hero` → `CHẶN toolkit.ll-hero.tree_sha256`, mã 1. Gỡ tệp → KHỚP.
- **Với T2:** T2 đã ghim tay `channel-k2/k2c-t2-01/VERSIONS.md` lúc G1. Đề xuất: ở G2, T2 chạy `versions.py record` trên commit G1 (worktree) rồi `check` trên HEAD để có phép so bằng máy. Không bắt buộc, vì T2 đang chạy.

## 3. Hồi quy khung vàng
### 3.1 Cách làm (`scripts/common/golden.py run`)
- Mỗi ca dựng lại một khung cố định bằng bộ công cụ **hiện hành**:
  1. `prep` offline;
  2. dựng **tuần tự** cảnh 3D từ khung 0 tới khung cần;
  3. `render.js --only` (lớp chữ 2D).
- So với khung tham chiếu:
  - Steel, T1, LL ep08: khung **master trong LFS**, đọc thẳng qua API batch + `ffmpeg -ss` (≈ 1,4 s, không tải cả tệp 0,9–1,6 GB);
  - K2V4 (master ngoài git): khung chấm mù vòng 5 đã commit.
- Số đo: pHash 64 bit, SSIM, MAD, tỉ lệ điểm ảnh lệch > 24 mức, ô lệch trên lưới 16×9.
- Kết luận theo 3 mức: KHỚP / LỆCH CỤC BỘ / LỆCH.
- Ảnh so (tham chiếu | mới | diff ×4): `reports/nen-tang/golden/*-sheet.jpg`. Số đo: `reports/nen-tang/golden/golden.json`.

### 3.2 Kết quả (15/10, HEAD b9a1368 = bộ công cụ của main f5ea772)
| Ca | Khung | Tham chiếu | pHash | SSIM | MAD | > 24 mức | Ô lệch | Kết luận | Giờ |
|---|---|---|---|---|---|---|---|---|---|
| Steel k2g01 | đoạn 01 khung 48 (v_open) | LFS `release-k2g-ep01-v1` master | 0/64 | 0,978 | 1,76 | 0,04 % | 0 | **KHỚP** | 179 s |
| T1 k2c-t1-06 | đoạn 00 khung 48 (c_wide) | LFS `release-k2c-t1-06-v1` master | 0/64 | 0,9549 | 3,85 | 1,24 % | **22** (2 hàng đáy) | **LỆCH CỤC BỘ** | 181 s |
| LL ep08 | đoạn 03 khung 48 (booth_room) | LFS `release-ll-ep08-v1` master | 0/64 | 0,9686 | 1,74 | 0,0 % | 0 | **KHỚP** | 456 s |
| Cuộn K2V4 | H khung 312 (= 23,0 s) | `kiem-mu/blind/P1` (khung mới) | 0/64 | 0,9498 | 2,55 | 0,03 % | 0 | **KHỚP** | 647 s |
| **Tổng** | | | | | | | | | **1 470 s = 24,5 phút** (≤ 30 phút) |

**Khác biệt T1:**
- Phạm vi: chỉ dòng nguồn ở đáy khung.
- Ở master (luật lúc đó) dòng nguồn nhỏ, một dòng. Bộ công cụ hiện hành dựng cỡ ≥ 38 px (V3, chủ dự án duyệt 14/10 20:45) nên dòng nguồn dài của T1 **xuống 2 dòng**.
- Nghĩa là dựng lại một tập cũ bằng bộ công cụ mới sẽ đổi chữ trên hình. Từ V3, luật mới yêu cầu "chỉ tên nguồn ngắn, không xuống 2 dòng", nhưng đặc tả cũ không theo luật này.
- Cảnh 3D và người đi bộ khớp sau khi dựng tuần tự (§3.3).
- Tập đã phát hành nên không cần sửa. Ghi để không ai "dựng lại T1" mà không biết.

### 3.3 Phát hiện hạ tầng trong lúc dựng khung vàng
1. **`hero.js --only N` không tất định ở cảnh có người đi bộ.**
   - Lượt đầu dựng lẻ khung 48 của `k2c106/corner`: người đi bộ lệch vị trí và tư thế so với master.
   - Dựng tuần tự 0..49 rồi so khung 48: lệch tới 244 mức trong vùng người (x 624–1278, y 693–780). Cảnh tích luỹ trạng thái theo khung.
   - `golden.py` đã chuyển sang dựng tuần tự từ khung 0; sau đó người đi bộ khớp master.
   - Luật cho mọi phiên (đã ghi RUNBOOK §7): sửa lẻ một khung cảnh có nhân vật phải dựng từ đầu shot.
2. **Steel: không thể `prep` lại bằng bộ công cụ hiện hành.**
   - (a) Luật lặp góc máy (chủ dự án 12/10) ra đời sau Steel nên chặn `prep`. `golden.py` bỏ qua đúng phép kiểm đó và ghi chú trong `golden.json`.
   - (b) `align.json` của Steel **chưa từng được commit** cạnh `channel-k2/k2g-ep01/vo/`. Bản duy nhất nằm ở bộ dữ liệu kiểm của K `checks/ll/fixtures/k2g01/vo/`. `golden.py` chỉ đọc bản này.
   - Nếu không có bộ dữ liệu đó, `prep` sẽ thu lại giọng: tốn ký tự, và giọng mới có nhịp khác giọng đã phát hành.
   - **Đề xuất:** phiên P/K chép `align.json` Steel vào `channel-k2/k2g-ep01/vo/`. Phiên này không làm vì ngoài vùng.
3. **LL ep08:** `ll.py prep` mặc định `vo_dir` = thư mục của đặc tả. Lượt đầu (bản sao đặc tả ở `/var/tmp`) đã cố gọi ElevenLabs, và **proxy chặn đúng lệnh đó, 0 ký tự**. `golden.py` luôn đặt `vo_dir` về thư mục gốc của tập và chạy `prep` sau proxy chặn.
4. **Bisect lượt đầu** (worktree ở commit cuối T1 `edc3d61` và `de55653`): khác biệt T1 khi dựng lẻ đã có ngay ở bộ công cụ của chính T1, nên đó là do dựng lẻ, không do V2–V4 phá. Các commit trên nhánh V không có tệp tập nên không bisect sâu hơn được; không cần nữa sau khi dựng tuần tự.
5. **Steel lượt đầu ở khung 96** (dựng lẻ) lệch cục bộ đúng dòng miễn trừ ("An explainer…"): bản mới sáng hơn, như thể đã hiện hết trong khi master còn đang hoà. Lệch này **có cả ở bộ công cụ `edc3d61`**, nên không do V2–V4. Nghi do align.json của bộ dữ liệu K lệch nhịp nhỏ so với lời gốc. **Chưa xác minh.** Khung vàng đặt ở khung 48 (KHỚP).

## 4. Điều lệ phiên và vùng tệp
- `docs/SESSION-CHARTER.md`:
  - khối điều lệ để P dán vào đầu lệnh: nhánh, tệp được sửa, tệp không được sửa, tệp dùng chung, trần chi phí, đầu vào, đầu ra, điều kiện dừng, merge;
  - nguyên văn **"KHÔNG dừng hỏi lại giữa chừng"**, kèm 4 điều kiện dừng;
  - mặc định khi lệnh không ghi;
  - 10 luật chạy phiên (preflight, COST-LEDGER, VERSIONS, tiến trình nền theo PID…).
- `docs/FILE-ZONES.md`:
  - bảng 17 nhóm đường dẫn × 6 loại phiên (P, K, tập, V, M, NT) với các mức S / + / R / ✗;
  - tệp dùng chung `AUTHORSHIP.md`, `RIGHTS.md`, `BAI-HOC-*`, `COST-LEDGER.csv`, `checks-appeal.md` **chỉ ghi thêm**, mã dòng `<tiền tố>-<số>` (NT, T2, V5, LL09, P, K, M, C);
  - luật "một tệp — một chủ ở một thời điểm".

## 5. Preflight
- `tools/preflight.sh`:
  - chạy tay: `--staged` (mặc định), `--range origin/main..HEAD`, `--all`;
  - làm hook: `ln -sf ../../tools/preflight.sh .git/hooks/pre-commit` / `pre-push`. Hook tự nhận vai theo tên tệp.
- Các mục kiểm:
  - P1 email (cả tác giả commit);
  - P2 khoá bí mật (Anthropic, AWS, GitHub, HF, ElevenLabs, khoá riêng, biến `*_API_KEY=`; bỏ qua khoá giả `SELFTEST`/`KHOA-GIA`);
  - P3 tệp > 5 MB không qua LFS, và con trỏ LFS ngoài `tools/lfs-allow.txt` (chỉ master/Short/3 phần xem của gói phát hành);
  - `lock.py --verify`;
  - P4 dấu xung đột merge;
  - P5 mỗi dòng `SOURCES-FOOTAGE.csv`/`SOURCES-NGOAI-SO.csv` phải có `licenses/<clip>.txt`;
  - P6 (chỉ báo) ảnh tư liệu mới chưa thấy trong RIGHTS/SOURCES/licenses.
- Ở `--staged`/`--range`, P1/P2/P4 chỉ **chặn dòng thêm mới**; nội dung có sẵn chỉ BÁO, để tệp dùng chung không chặn nhầm phiên khác.
- **Nhánh này `--range origin/main..HEAD`:** ĐẠT, `lock.py` KHỚP.
- **Nợ cũ tìm ra bằng `--all`** (ghi nhận, không sửa vì ngoài vùng):
  1. **`RIGHTS.md` dòng 26 (REF-SF) chứa một email bên thứ ba**: email liên hệ người tải lên archive.org, có từ commit `4bbdc73`. Đề xuất P thay bằng "liên hệ người tải lên (xem trang archive.org)" sau khi chủ dự án duyệt.
  2. **136 tệp > 5 MB commit thẳng ngoài LFS** (`design/cong5` 34, `design/cong3` 26, `reports/m3` 7, `design/cong4` 6, `assets/ll` 6, `assets/k2` 5, `screening/` …). Có trước luật; muốn gỡ phải viết lại lịch sử, không đề xuất.
  3. **30 dòng sổ T1** (`k2c-t1-06/SOURCES-FOOTAGE.csv`) ghi quyền trong cột, không có thư mục `licenses/`. Quy ước tệp giấy phép ra đời ở V4.

## 6. RUNBOOK môi trường
`docs/RUNBOOK-MOI-TRUONG.md`:
- **Máy:** không GPU; thiếu gói **`tifffile`, `pyshp`** (dựng relief lỗi; đã cài tay trong phiên, đề xuất thêm vào `scripts/env`); three.js cần `npm ci`.
- **Dựng lại cache:** lệnh relief đúng gồm `mohawk` (thiếu thì `routes.json` lệch SHA); tải ≈ 7 phút + 147 s.
- **Mạng (đo 15/10):** ElevenLabs qua proxy; bls.gov 403; Wayback hết giờ; Freesound 403; đọc khung LFS bằng HTTP; chặn proxy để chạy offline.
- **User-Agent không chứa email.**
- **Từng nguồn:**
  - LoC: `?fo=json` → `rights_advisory`, giãn ≥ 30 s, dừng khi 429;
  - Commons: API `extmetadata`;
  - Met: trang 429, dùng API → `isPublicDomain`;
  - Prelinger: `archive.org/metadata` → `licenseurl`;
  - DVIDS: "PUBLIC DOMAIN", **chưa trong danh sách Q32**;
  - NAIP: `USGSNAIPPlus`, `identify` từng tầng, ≤ 3 600 px;
  - Pexels/Pixabay;
  - FRASER.
- **rembg / trọng số:** ngoài git.
- **TTS:** số viết bằng chữ; commit cả `align.json`.
- **LFS / media.**
- **Giờ render đo được**, và luật tất định của `hero.js`.

## 7. Sổ chi phí
- `COST-LEDGER.csv`: 18 cột. Gồm % hạn mức, token sinh/ghi cache/đọc cache, Claude API $ + trần + model, ký tự ElevenLabs (gửi + bộ đếm), giờ render, giờ lịch giữa cổng, số lần chủ dự án chạm, thời lượng, % relief, nguồn tệp:dòng.
- 11 dòng mốc gốc: Steel G1/G2/G3, T1 G1a/G1b/G2, V1, V2, V2b, V3, V4.
- **Không báo cáo nào có % hạn mức.** Token chỉ có ở Steel và T1 G1a. Ô trống = chưa đo, không đoán.
- Giờ lịch giữa cổng chỉ tính được ở V2b → V3 (2,6 giờ). Các cổng khác có ngày nhưng thiếu giờ duyệt.
- Hướng dẫn: `docs/COST-LEDGER-HUONG-DAN.md`.

## 8. CHUẨN KÊNH
- **Kênh 2 (`docs/CHUAN-KENH-K2.md`, mới; trước đây kênh 2 chưa có tệp chuẩn kênh):**
  - Kinh thánh đứng trên; tệp này chỉ cụ thể hoá phần gói phát hành;
  - **1 Short**; `.srt`;
  - **mô tả ≤ 5 000 ký tự Unicode**; **nguồn đầy đủ ở bình luận ghim** (≤ 10 000);
  - 3 tiêu đề; **PACKAGING-BRIEF + 2–3 ảnh nền không chữ**; **chủ dự án tự làm thumbnail**; không liên kết chéo sang LL;
  - lệnh đếm ký tự; ghi nhận mô tả Steel 5 502 ký tự.
- **LL (`reports/m3/CHUAN-KENH-LL.md` §13, thêm khối "Sửa 15/10"; §14 bước 5 đánh dấu):**
  - 1 Short thay 2 Short; gói giống kênh 2; mô tả ≤ 5 000 + bình luận ghim;
  - dẫn chiếu `docs/BIBLE-KENH2.md`. Cách làm hình mới của Kinh thánh chỉ áp cho LL khi chủ dự án duyệt riêng (lộ trình Kinh thánh §7 bước 5).

## 9. Ghép thử
| Nhánh | Kết quả |
|---|---|
| `origin/main` (f5ea772) | `nen-tang` là fast-forward, không xung đột |
| `origin/k2c-t2` (4977016, T2 đang chạy) | merge thử **sạch**, 0 xung đột. T2 đổi `scripts/k2/hero.js`, `relief_build.py`, `lib/k2.js`, `design/k2v/*`, `docs/BIBLE-KENH2.md`; phiên này không chạm các tệp đó |
| `origin/ccr-bef6f172-fcqat9` (nhánh WIP của T2, cùng HEAD) | sạch |
- **Lưu ý ngữ nghĩa:** sau khi T2 merge (đổi `hero.js`, `relief.js`, `lib/k2.js`), nên chạy lại `golden.py run` ở main mới để xem T2 có làm lệch khung vàng của Steel, T1, LL, K2V4 không. Đúng việc này là mục đích của công cụ.

## 10. Việc đang chờ chủ dự án
1. **Duyệt merge `nen-tang`** vào main. Theo lệnh, chỉ merge giữa hai tập: sau khi T2 xong, không merge khi T2 đang dựng. P merge, phiên này không merge.
2. **Phương án tốc độ:** duyệt **thử GPU (a)**:
   - chọn máy: máy của chủ dự án có GPU NVIDIA, hoặc thuê VM GPU (báo giá cần chủ dự án kiểm);
   - giao phiên V sửa cờ Chromium của `hero.js` (k2 + ll) theo biến môi trường;
   - buổi thử: đo cuộn K2V4 đoạn H + Z, so khung bằng `golden.py`.
   (b1) chia nhiều phiên cần kho ngoài cho ≈ 4,4 GB khung/tập. (c) không khuyến nghị lúc này.
3. **Duyệt** `SESSION-CHARTER.md`, `FILE-ZONES.md`, `CHUAN-KENH-K2.md` và phần sửa `CHUAN-KENH-LL.md` §13 (1 Short, mô tả ≤ 5 000, nguồn ở bình luận ghim). Sau duyệt, P ghi `AUTHORSHIP.md`.
4. **RIGHTS.md dòng 26 có email bên thứ ba:** cho phép P thay bằng lời dẫn tới trang nguồn?
5. **Steel:** cho phép P/K chép `align.json` từ bộ dữ liệu K vào `channel-k2/k2g-ep01/vo/`, để tập dựng lại được mà không thu lại giọng.
6. **Môi trường:** thêm `tifffile`, `pyshp` và `npm ci` (k2v + cong3/shared) vào `scripts/env`. Phiên nào được giao?
7. **Điền % hạn mức và token** của phiên Nền tảng (đọc trên trang Usage) vào dòng NT của `COST-LEDGER.csv`.
8. **Ngưỡng khung vàng** (pHash ≤ 6, SSIM ≥ 0,90, 0 ô lệch) là tạm; đề xuất chốt sau 3 lần chạy. Cài hook preflight là tự nguyện cho tới khi chủ dự án biến thành luật trong điều lệ.
