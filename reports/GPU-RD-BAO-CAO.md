# GPU-RD — Nghiên cứu GPU cho dựng hình kênh 2 (chỉ tài liệu + đo trên CPU) — BÁO CÁO

> Phiên GPU-RD, 16/10/2026, theo lệnh chủ dự án duyệt 16/10. Nhánh `gpu-rd` tạo từ `origin/main` @ `7255aa4` (đẩy cùng commit lên nhánh harness `claude/gpu-research-channel-2-a8ckci`). **Không thuê, không đăng ký tài khoản, không nhập thẻ. Không merge. DỪNG chờ chủ dự án.**
> Mọi số là số đo thật trong phiên (tệp ở `research/gpu/do/`) hoặc tra nguồn có URL (ngày đọc 16/10/2026). Số ước ghi **(ước)**. Email người dùng không xuất hiện trong repo/báo cáo.

## 0. Khối điều lệ (lệnh + thực tế)
| Trường | Lệnh | Thực tế |
|---|---|---|
| Loại phiên | nghiên cứu (chỉ tài liệu + đo CPU) | đúng; không thuê/đăng ký/nhập thẻ |
| Nhánh | `gpu-rd` từ `origin/main` | `gpu-rd` @ `7255aa4` + commit phiên; cùng commit đẩy lên nhánh harness. Mã v5b1b đọc qua `git worktree` ở thư mục tạm (không đổi nhánh nào) |
| Tệp được sửa | CHỈ `research/gpu/**`, `reports/GPU-RD-BAO-CAO.md` | đúng (§11). Không sửa `scripts/k2tl`, `design/k2v/tl` (đổi cờ GL bằng nạp trước `-r`, không chạm mã phiên V). Không đọc mã `checks/` |
| Trần | Claude API ≤ $1 (ghim model) · YouTube 0 · ElevenLabs 0 · giờ máy ≤ 1 h | **$0** (không gọi API; không có `cost.jsonl`) · **0** · **0** · **≈ 0,55 giờ máy** (§10) |
| Preflight | BẮT BUỘC | §11 |
| Điều kiện dừng | xong việc → đẩy → dừng | (1) xong việc |

## 1. Tóm tắt (đọc 1 phút)
1. **Hồ sơ đường dựng (SwiftShader, 3 khung 470/175/300, SPP2, 1080p): 5,90 s/khung, trong đó 97,4 % (5,75 s) là thực thi lệnh GL trong tiến trình GPU (SwiftShader).** JS + gửi lệnh 7 ms; ghép lớp chữ 2D 57 ms; đọc lại khung 27 ms; mã hoá JPEG 52 ms (mã hoá CPU thuần 37 ms); chuyển base64 về Node + ghi 26 ms. Sàn không-GL ≈ **0,15 s/khung**. CPU: tiến trình GPU ăn 22,4 CPU-giây/khung (≈ 3,8/4 nhân), trình kết xuất 0,13 s. ⇒ GPU thật tăng tốc được gần như toàn bộ; trần lý thuyết (Amdahl) ≈ 39×.
2. **Phát hiện chính (việc 6): Mesa llvmpipe — vẫn CPU, đã có sẵn trong container — nhanh gấp ≈ 5,4× SwiftShader.** Cờ `--use-gl=angle --use-angle=gl-egl` (không cần X). Trọn đoạn gib20 480 khung 1080p SPP thích ứng: **1,177 s/khung (9,4 phút)** so với 6,41 s (V5b-1b, cùng loại máy). Tất định bit-exact khi dựng lại; test trình duyệt của mô-đun ĐẠT. Ước tập 10 phút kịch bản 3: **5,4 h máy nhanh / 7,7 h máy chậm (ước) — ĐẠT ≤ 12 h không cần GPU**.
3. **Khớp hình llvmpipe ↔ SwiftShader (15 khung 1080p): KHÔNG ĐẠT tiêu chí chặt của lệnh** (PSNR 34,0–38,1 dB < 40; lệch > 10/255 ở 0,4–3,1 % điểm ảnh). Lệch nằm ở **tần cao** (hạt/nhiễu thủ tục, cạnh dưới điểm ảnh): dịch màu trung bình −0,0…−0,45 mức/kênh, lệch tần thấp TB 0,47 mức; PSNR ở ¼ kích thước 40,7–44,8 dB; SSIM 0,90–0,94; mắt không thấy khác (ảnh so §2.3). GPU thật gần như chắc cũng lệch kiểu này → **cần chủ dự án/K quyết tiêu chí khớp** (đề xuất §6.3).
4. **GPU thuê (ước):** 0,21–0,71 s/khung 3D → tập kịch bản 3 **0,8–2,4 h dựng + ≈ 0,5 h môi trường**, **≈ $0,4–2,2/tập** với 7 mức giá (T4/L4, $0,29–0,76/h). Không có benchmark công khai SwiftShader↔GPU cho three.js; khoảng tăng tốc phải đo thật (kế hoạch thử ≤ $5, script viết sẵn §6, chưa chạy).
5. **Khuyến nghị: phương án D — llvmpipe trên CPU hiện có** (không tiền thuê, không tài khoản/thẻ/khoá, không đổi môi trường), sau khi chủ dự án duyệt mắt bản 540p llvmpipe và K chốt tiêu chí khớp; **GPU giữ hoãn** (NT K6), mở lại khi cần SPP cao/4K hoặc tập > 4 h máy. Chi tiết §8.

## 2. Hồ sơ đường dựng (việc 1)
### 2.1 Cách đo
- Mã v5b1b @ `e8092a1` (worktree tạm). Dữ liệu thô tải lại bằng `scripts/k2tl/fetch_sources.py`: **10/10 tệp nguồn KHỚP SHA-256 của V5b-1** (DEM, Sentinel-2 ×2, Landsat ×5, Catastro, LoC; 2 LUT lấy từ `origin/v5a`); OSM 19 ô 70 MB; gói cảnh dựng lại 58 s, **trùng thống kê V5b-1b** (28 538 toà, 82 533 cây, ghost 1880 = 1 252). Thiếu so với V5b-1b: 11 toà mốc 1913 (`--plan1913` cần ảnh Baedeker, không ảnh hưởng 3 khung đo) và ảnh cắt `ng_crop.jpg` (V5b-1 không ghi cách cắt — tôi thu nhỏ cả TIF; chỉ hiện ở khung 196–263).
- `research/gpu/profile.js`: driver riêng, **không sửa mã dựng**. Gắn đo bằng `addInitScript`: đếm lệnh vẽ; trước `drawImage(canvas WebGL → 2D)` đọc 1 điểm ảnh GL để buộc chờ dựng xong (**`gl.finish()` trong Chrome không chặn — đo 0 ms**); trước `toDataURL` tách xả lớp 2D / đọc lại đủ khung / mã hoá; đo riêng mã hoá JPEG trên canvas phần mềm. CPU-giây từng loại tiến trình Chromium đọc từ `/proc`. Chrome tracing 1 khung (`trace_sum.py`).
- Bench chuẩn như V5b-1b §7: khung 470, 175, 300, SPP2, dựng 2 lần, lấy lần 2. Máy phiên này ≈ máy C của V5b-1b (SwiftShader 5,90–6,00 s ↔ 5,81 s).

### 2.2 Kết quả (trung bình 3 khung, lượt 2; `do/profile-swiftshader.json`)
| Bước | ms/khung | % | GPU thật tăng tốc? |
|---|---|---|---|
| JS + cập nhật cảnh + gửi lệnh GL (625 lệnh vẽ/khung) | 7 | 0,1 | không cần |
| **Thực thi GL: bóng 4096 + 2 lượt cảnh (SPP2) + tích luỹ + hậu kỳ (SwiftShader)** | **5 746** | **97,4** | **CÓ** — phần duy nhất đáng kể |
| Ghép lớp chữ 2D + xả canvas 2D | 57 | 1,0 | có một phần (canvas 2D cũng chạy qua tiến trình GPU) |
| Đọc lại khung 1080p về CPU (`getImageData`) | 27 | 0,5 | ít (băng thông PCIe; vẫn ≈ 5–20 ms **(ước)**) |
| Mã hoá JPEG q0,95 (`toDataURL`) | 52 (CPU thuần 37) | 0,9 | **không** (CPU) |
| Chuyển base64 về Node + ghi tệp | 26 | 0,4 | **không** |
| **Tổng tường** | **5 899** | 100 | sàn không-GL ≈ **153 ms** |

- CPU-giây mỗi khung: **tiến trình GPU 22,4 s** (SwiftShader đa luồng, ≈ 3,8 nhân trong 5,9 s), trình kết xuất 0,13 s, trình duyệt 0,01 s.
- Chrome tracing khung 470 (`do/trace-swiftshader-f470.json`): 4 893 ms trên `CrGpuMain` nằm trong `RasterDecoderImpl::DoReadbackARGBImagePixelsINTERNAL` — **lệnh GL bị hoãn, chỉ thực thi khi có lệnh đọc lại** → nhìn trace dễ nhầm "đọc lại chậm"; tách bằng điểm đồng bộ ở trên mới thấy đó là dựng hình. (Trùng nhận xét V5b-1 §5.2 "thời gian thật nằm ở bước đồng bộ GPU→canvas".)
- 1080p → 540p (¼ điểm ảnh): 5,90 → **2,38 s** (÷2,5) — phần lớn chi phí tỉ lệ với số điểm ảnh tô (fill), phần còn lại theo đỉnh/bóng. GPU mạnh nhất đúng ở loại tải này.
- **Kết luận việc 1:** GPU thật thay được ≈ 97 % thời gian khung. Không cần tối ưu mã hoá/đọc lại trước khi có GPU; sau khi có GPU, sàn 0,15 s (JPEG + IPC + 2D) sẽ chiếm phần lớn → khi đó mới đáng chuyển sang đọc RGB thô (`post.js` `finalize` đã có) + mã hoá song song ngoài trình duyệt.

### 2.3 Ảnh so (llvmpipe, §7)
`do/so-hinh-ss-llvmpipe-00470.jpg`, `do/so-hinh-ss-llvmpipe-00175.jpg`: trái SwiftShader · giữa llvmpipe · phải |lệch|×4; hàng dưới cắt 1:1 ô lệch nhất. Lệch dạng hạt rải đều + đường bờ biển/cạnh mảnh.

## 3. Ước tăng tốc GPU (việc 2)
### 3.1 Nguồn công khai (đọc 16/10/2026 qua tác tử con; mục "chưa xác nhận" ghi rõ)
| So sánh | Số | Nguồn |
|---|---|---|
| SwiftShader ↔ Mesa llvmpipe (CPU 8 nhân, Chrome 150, cảnh 3D nặng) | ≈ 24 s → ≈ 6 s (4×) khi chạy riêng; 2× dưới tải thật | https://microlink.io/blog/webgl-without-a-gpu · https://microlink.io/blog/faster-webgl-screenshots |
| **Đo trong phiên này** (cảnh gib20, 4 vCPU) | SwiftShader → llvmpipe **5,3–5,4×** | `do/cpu-*.json`, `do/llvmpipe-gib20-480khung.json` |
| WebGL2 demo nặng: GPU ↔ SwiftShader | 60 fps (khoá vsync) ↔ "một chữ số" fps → ≥ 6× (giai thoại, không đối chứng) | https://demo.dev.squidler.io/gpu_stress.html |
| Chrome team, T4 Colab, headless | chỉ định tính ("vài giây"/epoch trên SwiftShader, nhanh hơn nhiều trên T4); cờ `--use-angle=vulkan --enable-features=Vulkan --disable-vulkan-surface` | https://developer.chrome.com/blog/supercharge-web-ai-testing |
| Remotion / Hackernoon (EC2 g4dn T4, Chrome headless) | "significantly faster", không có số; đường `--use-angle=gl-egl` hoặc vulkan, driver 535 | https://www.remotion.dev/docs/miscellaneous/cloud-gpu · https://hackernoon.com/unlocking-gpu-accelerated-server-side-rendering-in-remotion-with-chrome-chromium-and-puppeteer |
| Blender Cycles GPU ↔ CPU (không phải WebGL, chỉ tham khảo) | > 10× | https://modal.com/docs/examples/blender_video |
| Phoronix llvmpipe ↔ GPU | trang 403, chỉ đoạn trích tìm kiếm (2011–14) — **chưa xác nhận** | https://www.phoronix.com/review/ubuntu_1404_llvmpipe |
**Không có benchmark công khai SwiftShader ↔ GPU thật cho three.js headless có số.**

### 3.2 Khoảng tăng tốc cho cảnh của mình (ước)
Mô hình: s/khung GPU = sàn 0,153 s (đo) + phần GL SwiftShader × 0,974 ÷ k. Cảnh 3D trộn SPP như V5b-1 kịch bản 2 (SwiftShader 5,74 s/khung).
| Mức | k (GL GPU ÷ GL SwiftShader) **(ước)** | Lý do | s/khung 3D **(ước)** | Tăng tốc cả khung **(ước)** |
|---|---|---|---|---|
| thấp | 10× | GPU lớp T4 + đường ANGLE/EGL headless kém tối ưu, đồng bộ mỗi khung; chỉ gấp ~2× llvmpipe đo được | 0,71 | 8× |
| giữa | 30× | L4/A10 lớp trung; tải fill + bóng 4096 hợp GPU | 0,34 | 17× |
| cao | 100× | GPU tốt, đường Vulkan; sàn 0,15 s chiếm phần lớn | 0,21 | 27× |
Ràng buộc: headless Chromium dùng GPU qua ANGLE (Vulkan hoặc EGL) cần driver đồ hoạ (container phải có `NVIDIA_DRIVER_CAPABILITIES` chứa `graphics`, https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/docker-specialized.html); lỗi hay gặp: `nvidia-smi` chạy nhưng Vulkan không thấy GPU (https://github.com/NVIDIA/nvidia-container-toolkit/issues/191); `--disable-gpu` âm thầm rơi về SwiftShader; cờ sai vẫn hiện GPU trong chrome://gpu nhưng không dùng (Chrome team) → **phải kiểm `UNMASKED_RENDERER` thật** (`research/gpu/webgl_probe.js`, thoát 5 nếu vẫn là phần mềm).

## 4. Nhà cung cấp GPU thuê theo giờ (việc 3)
Giá đọc 16/10/2026 (tác tử con đọc trang; dòng "chưa xác nhận" là từ đoạn trích tìm kiếm). Lớp GPU đồ hoạ đủ cho WebGL: T4, L4, A10/A10G, A4000/A5000, RTX 4000/6000 Ada, 3090/4090, A40 — không cần A100/H100.
| Nhà cung cấp | GPU hợp · $/giờ | Tính phí | Chromium headless có GPU (Vulkan/EGL)? | Hạn chế (KYC, thẻ, vùng) | Dữ liệu vào/ra (gói ≈ 30–60 MB thực đo, video ≈ 100 MB) |
|---|---|---|---|---|---|
| **AWS EC2** | g4dn.xlarge T4: $0,526 / spot $0,287 · g5.xlarge A10G: $1,006 / spot $0,414 · g6.xlarge L4: $0,805 / spot $0,502 (doit.com, bên thứ ba: https://www.doit.com/compute/spot/us-east-1/g4dn.xlarge , …/g5.xlarge , …/g6.xlarge) | theo giây, tối thiểu 60 s (https://aws.amazon.com/ec2/pricing/on-demand/) | **CÓ, tài liệu tốt nhất**: driver Tesla/GRID/gaming đều hỗ trợ OpenGL/Vulkan trên g4dn/g5/g6 (https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/install-nvidia-driver.html); Remotion + Hackernoon chạy Chrome trên g4dn | thẻ; **hạn mức "G and VT instances" mặc định thấp, phải xin tăng**; spot có thể bị thu hồi | 100 GB/tháng ra Internet miễn phí; vào miễn phí; scp/S3 |
| **Google Cloud** | g2-standard-4 (1× L4, 4 vCPU): $0,7068 / spot $0,4028, us-central1 (https://gcloud-compute.com/g2-standard-4.html, dữ liệu 11/10) · T4 $0,35/h GPU riêng (**chưa xác nhận**) | theo giây, tối thiểu 1 phút (**chưa xác nhận**) | máy ảo đủ quyền; có biến thể vWS cho đồ hoạ (`nvidia-l4-vws`) (https://docs.cloud.google.com/compute/docs/gpus) | thẻ; hạn mức GPU tài khoản mới thường = 0, phải xin (**chưa xác nhận**); T4 "sắp hết hỗ trợ" | phí ra Internet (chưa đọc mức); gcloud/gsutil |
| **RunPod** | L4 $0,59 (secure) / $0,44 (community) · A5000 $0,27 / $0,16 (cần kiểm lại) · 3090 $0,50 / $0,22 · 4090 $0,89 / $0,34 · A40 $0,59 / $0,35 (https://www.runpod.io/pricing) | theo giây (https://docs.runpod.io/pods/pricing) | **chưa xác nhận** (không có tài liệu `NVIDIA_DRIVER_CAPABILITIES`/Vulkan; pod là container) | trả trước ≥ 1 giờ; hết tiền pod dừng, mất dữ liệu nếu không có volume | **không phí vào/ra**; volume $0,07–0,10/GB-tháng |
| **Vast.ai** | chợ giá động — không đọc được bảng giá; interruptible "rẻ hơn 50 %+" (https://vast.ai/pricing) | theo giây; băng thông tính theo byte, giá tuỳ máy chủ (https://docs.vast.ai/guides/reference/billing.md) | **chưa xác nhận**; chỉ cho `-e`/`-p`, đặt được `NVIDIA_DRIVER_CAPABILITIES` nhưng máy chủ có mở Vulkan không thì tuỳ | trả trước (≈ $5 tối thiểu — **chưa xác nhận**); máy chủ cá nhân, độ tin cậy/driver không đều → **rủi ro bảo mật cao nhất** cho dữ liệu | phí băng thông theo máy |
| **Lambda** | Quadro RTX 6000 $0,69 · A6000 $1,09 · A10 $1,29 (https://lambda.ai/pricing) | theo phút, hoá đơn tuần (https://docs.lambda.ai/public-cloud/billing/) | máy ảo đủ quyền, tự cài Vulkan (chưa nêu hỗ trợ đồ hoạ) | thẻ (**chưa xác nhận**) | filesystem không phí vào/ra |
| **DigitalOcean GPU Droplet** (kế thừa Paperspace) | RTX 4000 Ada $0,76 · RTX 6000 Ada $1,57 · L40S $1,57 (https://www.digitalocean.com/pricing/gpu-droplets) | theo giây, tối thiểu 5 phút; droplet tắt vẫn tính | máy ảo đủ quyền (ước: được) | giữ thẻ ≈ $1 | 10 000 GiB truyền miễn phí |
| **Modal** | T4 $0,59 · L4 $0,80 · A10 $1,10 + CPU/RAM (https://modal.com/pricing) | theo giây | **chưa xác nhận** (tài liệu chỉ có Blender CUDA) | gói Starter $30/tháng tín dụng miễn phí; chỉ serverless | ra $0,04/GiB sau 1 TiB/tháng miễn phí |
| TensorDock | 4090 từ $0,35 (https://tensordock.com/) | trừ liên tục | máy ảo (**chưa xác nhận**) | nạp từ $5; hết tiền xoá máy | không phí vào/ra |
Thời gian khởi động máy: không nguồn nào có số → ước 5–15 phút (máy ảo + cài driver/Chromium) **(ước)**.
**Thực đo về dữ liệu:** gói cảnh Gibraltar đã dựng chỉ **12 MB** (dữ liệu thô 1,1 GB không cần mang lên máy GPU); gói thử (mã + gói cảnh + 24 khung tham chiếu) ≈ 30–60 MB **(ước)**. Video 1080p 20 s ≈ 100 MB ra.

## 5. Chi phí mỗi tập & so phương án (việc 4)
### 5.1 Giờ máy tập 10 phút (14 400 khung) — `research/gpu/uoc_tap.py` → `do/uoc-tap.json`
| Phương án | 100 % 3D (kịch bản 2) | 70 % 3D + 30 % relief (kịch bản 3) | Nguồn số |
|---|---|---|---|
| A. CPU SwiftShader, 1 phiên (hiện hành) | 23,0 h / 32,4 h chậm | **18,5 h / 26,0 h** | V5B1B §7 (đo) |
| B. CPU SwiftShader, 2–3 phiên song song | giờ máy như A; **thời gian thực ÷2–3: 6,2–13 h** | | (ước từ A) |
| C. GPU thuê toàn bộ | 0,8–2,9 h | **0,8–2,4 h** + ≈ 0,5 h môi trường | **(ước)** §3.2 |
| C'. Lai: GPU cho cảnh 3D, relief giữ CPU | — | 3D 0,6–2,0 h GPU + relief 2,4 h CPU (song song được) | **(ước)** |
| **D. CPU llvmpipe, 1 tiến trình** | **4,4 h / 6,2 h chậm (ước)** | **5,4 h / 7,7 h chậm (ước)** (relief vẫn SwiftShader 1,98 s) | 3D: **đo** trọn gib20; hệ số máy chậm ×1,41 áp cho llvmpipe là (ước) |
| D'. llvmpipe 2 tiến trình/container | 3,7 h | 4,5 h | đo ×1,2 thông lượng (§7) |

### 5.2 Chi phí tiền
| Phương án | Tiền/tập | Ghi chú |
|---|---|---|
| A, B, D, D' | **$0 tiền thuê** | dùng container cloud hiện có (hạn mức phiên của gói Claude của chủ dự án — không có số $/giờ trong repo) |
| C (kịch bản 3, 1,3–2,9 h thuê gồm 0,5 h môi trường) | **$0,37–2,21** — rẻ nhất AWS g4dn spot $0,37–0,84; L4 GCP spot $0,52–1,17; RunPod L4 $0,57–1,72; DO RTX 4000 Ada $0,98–2,21 | **(ước)**; thêm lần đầu ≈ 1 h làm ảnh máy (AMI/template) |
| Lượt thử GPU (§6) | ≤ $5 (trần), ước $0,5–1,5 | 1 phiên ≤ 2 h |

### 5.3 Ưu / nhược / tác động / rủi ro
| | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|
| **A** SwiftShader 1 phiên | đã kiểm, khung vàng hiện hành dựng trên nó | 18,5–26 h/tập > trần 12 h; 2 tập/tuần ≈ 37–52 h máy | nhịp 2 tập/tuần không giữ được ở chuẩn hình mới | máy chậm (×1,41) làm trễ không báo trước |
| **B** SwiftShader 2–3 phiên | không đổi hình; không tiền thuê | giờ máy không giảm; P phải chia khúc + ghép; mỗi phiên ≈ 1–2 phút nạp cảnh | đạt thời gian thực ≤ 12 h | **tất định:** cảnh có người đi bộ chỉ đúng khi dựng tuần tự từ khung 0 (RUNBOOK §7) → chia khúc phải bắt đầu ở mốc cảnh; mất phiên giữa chừng = dựng lại khúc |
| **C** GPU thuê | nhanh nhất (ước 8–27×); mở đường SPP4 toàn tập / 4K | tài khoản + thẻ + hạn mức GPU; dựng môi trường driver/Vulkan (lỗi đã biết); chưa có số đo thật | ≈ $1–2/tập; ≤ 3 h/tập | **bảo mật:** máy thuê không được có khoá (Claude/ElevenLabs/GitHub token) — script §6 không cần khoá; chép kết quả bằng scp, không đẩy git từ máy thuê. **Mất máy** (spot thu hồi) → dựng lại khúc. **Khác hình CPU↔GPU** (§7 cho thấy khác trình dựng = lệch tần cao, PSNR 34–38) → bắt buộc kiểm khớp khung + khung vàng mới. Chi phí ngầm: quên xoá máy |
| **C'** Lai | GPU chỉ cho phần nặng; relief giữ nguyên | hai đường dựng, hai bộ khung vàng | — | ghép cảnh hai trình dựng → màu nối cảnh phải kiểm |
| **D** llvmpipe | **5,4× SwiftShader, $0, không tài khoản/thẻ/khoá, cùng container**; tất định bit-exact; đạt ≤ 12 h cả máy chậm (ước) | hình KHÔNG trùng byte với SwiftShader (lệch tần cao); cần đổi cờ trong `scripts/k2tl/render.js` (vùng phiên V); relief/hero (`scripts/k2`, `scripts/ll`) chưa đo | đạt trần 12 h ngay | Mesa là gói hệ thống (25.2.8, LLVM 20) → nâng cấp image có thể đổi hình → **ghim phiên bản trong `VERSIONS.yaml`/`verify.sh`**; khung vàng/ngưỡng K tính trên SwiftShader phải dựng lại |

## 6. Kế hoạch thử GPU nhỏ nhất (việc 5) — script viết sẵn, CHƯA chạy
### 6.1 Điều kiện
1 phiên máy GPU ≤ **$5** (ước $0,5–1,5): **AWS g4dn.xlarge (T4) hoặc GCP g2-standard-4 (L4)** — máy ảo đủ quyền, đường Chrome-headless-GPU có tài liệu; tránh Vast.ai (máy chủ cá nhân). Chủ dự án tự tạo tài khoản/nhập thẻ/xin hạn mức (phiên không làm). Không đặt khoá nào lên máy thuê.
### 6.2 Script (`research/gpu/thu-gpu/`, đọc `README.md`)
| Tệp | Việc |
|---|---|
| `0_chuan_bi_cpu.sh` | trên container CPU: dựng 24 khung tham chiếu SwiftShader (rải 10..470, bước 20, `--only`), đóng gói mã v5b1b + gói cảnh + LUT + khung → `gpu-thu.tar.zst` |
| `1_cai_dat_gpu.sh` | trên máy GPU: `nvidia-smi`, `vulkaninfo`, Node 22, **Playwright 1.64.0 (Chrome for Testing 156.0.8078.4, cùng bản container)**, three.js `npm ci`, venv so hình |
| `2_chay_thu.sh` | thử cờ vulkan → egl, headless-shell → Chromium đầy đủ; **dừng (mã 5) nếu `webgl_probe` vẫn ra SwiftShader/llvmpipe**; hồ sơ 3 khung (`profile.js`, cùng phép đo §2); 24 khung → `compare.py`; trọn 480 khung (s/khung thật); bản xem 540p; ghi `ket-qua/` |
| `../gl_flags.js` | nạp trước (`node -r` / `NODE_OPTIONS`) đổi cờ GL của `render.js` **không sửa mã phiên V** (đã dùng thật cho llvmpipe trong phiên này) |
### 6.3 Tiêu chí
| Tiêu chí | Ngưỡng |
|---|---|
| Khớp hình (theo lệnh) | mỗi khung: PSNR ≥ 40 dB **hoặc** lệch > 10/255 ở ≤ 1 % điểm ảnh (`compare.py`, cột `dat`) |
| Khớp cấu trúc (**đề xuất, đặt SAU khi thấy số llvmpipe — chờ chủ dự án/K duyệt**) | lệch tần thấp (Gauss σ 8) > 3 mức ở ≤ 3 % điểm ảnh · dịch màu TB ≤ 1 mức/kênh · PSNR ở ¼ kích thước ≥ 40 dB · SSIM ≥ 0,90 · + xem mù bản 540p (cột `dat_cau_truc`) |
| Tốc độ | trọn gib20 480 khung ≤ **0,8 s/khung** (≥ 8×, mức "thấp" §3.2) để đáng thuê; nếu ≤ 1,2 s/khung (ngang llvmpipe) → **không thuê**, dùng D |
| Ổn định | 0 lỗi trang/shader; RSS < bộ nhớ máy; dựng lại 3 khung trùng byte |
Lưu ý: lệnh yêu cầu tiêu chí khớp chặt; **dữ liệu llvmpipe cho thấy một trình dựng khác SwiftShader sẽ trượt tiêu chí chặt dù mắt không thấy khác** (lệch nằm ở hạt/nhiễu, §7). Nếu giữ tiêu chí chặt, cả D và C đều không qua → hệ quả: GPU/llvmpipe chỉ dùng được cho tập MỚI với khung vàng dựng lại trên chính trình dựng đó (không trộn khung SwiftShader và khung GPU trong một cảnh).

## 7. Tối ưu CPU chưa thử (việc 6) — số đo thật (3 khung 470/175/300, SPP2, 1080p, lượt 2; `do/cpu-*.json`)
| # | Thử | s/khung | so SwiftShader 6,00 | Hình so SwiftShader | Kết luận |
|---|---|---|---|---|---|
| 1 | **Mesa llvmpipe** (`--use-gl=angle --use-angle=gl-egl`, không X) | **1,16** (lặp lại 1,10) | **÷5,2–5,4** | PSNR 34,9–37,6 dB; ¼ kích thước 43–44,7; SSIM 0,91–0,94; dịch màu ≤ 0,45 mức; tần thấp > 3 mức ≤ 0,33 % | **ĐÁNG ÁP** (chờ duyệt hình) |
| 1b | llvmpipe trọn gib20 480 khung, SPP thích ứng | **1,177** (SPP1 0,764 · SPP2 1,110 · SPP4 1,829) | ÷5,45 (6,41 V5b-1b) | 12 khung rải 1080p (`--only`, cả hai trình dựng): PSNR 34,0–38,1, ¼ 40,7–44,8, SSIM 0,901–0,942, tần thấp > 3 mức ≤ 2,41 %; **12/12 đạt tiêu chí cấu trúc, 2/12 đạt tiêu chí chặt**. Cả đoạn so bản xem 540p SwiftShader: bằng sàn nén H.264 ở khung kiểm (31,7 ↔ 31,5 dB khung 175) | bản xem `do/gib20_llvmpipe_540p.mp4` (4,5 MB, âm chép từ bản xem V5b-1b; khung 196–263 ảnh LoC cắt khác — do tôi cắt lại, không do trình dựng) |
| 1c | llvmpipe tất định | lặp lại trùng byte 3/3 | — | — | dùng làm khung vàng mới được |
| 1d | test trình duyệt mô-đun (`scripts/k2tl/tests/test_browser.js`) dưới llvmpipe (`NODE_OPTIONS=-r gl_flags.js`) | 34–59 s | — | ĐẠT: chữ ≤ 15,63 %, tương phản min 9,63, năm mốc đinh 1941 (renderer trong log = llvmpipe) | — |
| 2 | 2 tiến trình SwiftShader song song (4 vCPU) | 11,6 mỗi tiến trình → thông lượng 5,8 | ×1,03 | — | **không lợi** (SwiftShader đã dùng ≈ 3,8 nhân) — khớp NT 15/10 (relief 1,2×) |
| 3 | 2 tiến trình llvmpipe song song | 1,84 mỗi tiến trình → thông lượng **0,92** | ×1,2 so 1 tiến trình llvmpipe | — | lợi nhỏ; RAM 2 × ≈ 2 GB ổn |
| 4 | Bóng 2048 thay 4096 (giảm bóng theo khoảng cách — giới hạn trên của lợi) | 5,99 | ≈ 0 | khung 470: lệch > 10/255 ở 5,3 % điểm ảnh (bóng mềm/nhoè khác) | **không lợi**, bỏ (khớp V5b-1 "+4 %") |
| 5 | 540p (¼ điểm ảnh) — chỉ để biết loại tải | 2,38 | ÷2,5 | — | tải phần lớn theo fill → GPU hợp |
| 6 | Impostor phố xa | **không đo thêm**: V5b-1 đã ẩn toà "rất xa" và dùng nền vệ tinh làm impostor; V5b-1b đo bỏ hết nhà chỉ −12 % → lợi của impostor ≤ 12 % (giới hạn trên), nhỏ hơn nhiều llvmpipe | — | — | ưu tiên thấp |
Bản xem mp4 V5b-1b không làm chuẩn so chặt được: khung 470 SwiftShader dựng lại bằng mã hiện tại so với bản xem cũng chỉ 29,6 dB (sàn nén); khung 479 của bản xem có góc máy khác khung dựng lại → so chuẩn chỉ bằng khung dựng cùng mã, cùng cách (`--only`).

## 8. Khuyến nghị
1. **Chọn D (llvmpipe) làm đường dựng chính cho mô-đun xương sống thời gian**, sau 3 bước: (a) chủ dự án xem mù `research/gpu/do/gib20_llvmpipe_540p.mp4` cạnh `channel-k2/k2c-t3-01/v5b1-thu/v5b1b/gib20_540p.mp4` (nhánh `v5b1b`); (b) K chốt tiêu chí khớp (chặt hay cấu trúc §6.3) và dựng lại khung vàng trên llvmpipe; (c) phiên V thêm biến môi trường chọn cờ GL vào `scripts/k2tl/render.js:16` (mặc định giữ SwiftShader tới khi duyệt), ghim Mesa 25.2.8 trong `scripts/env/verify.sh`/`VERSIONS.yaml`. Ước tập kịch bản 3: **5,4 h** (máy nhanh) / **7,7 h** (máy chậm, ước); với 2 tiến trình 4,5 h. Lý do: ĐẠT trần 12 h, $0, không mở tài khoản/thẻ/khoá, cùng môi trường; rủi ro chính là hình khác SwiftShader ở tần cao — đã đo, đã có ảnh so.
2. **Đo tiếp llvmpipe cho relief/hero** (`scripts/k2/hero.js:38`, `scripts/ll/hero.js:13` — vùng phiên V) trước khi áp toàn kênh: nếu cũng ≈ 5×, kịch bản 3 xuống ≈ 3,5 h **(ước)**.
3. **GPU (C/C') giữ hoãn** (NT K6). Mở lại khi: tập cần SPP4 toàn bộ, 4K, hoặc > 4 h máy/tập với llvmpipe. Khi mở: chạy lượt thử §6 (≤ $5) trên AWS g4dn.xlarge spot hoặc GCP L4 spot; chỉ thuê dài khi ≤ 0,8 s/khung.
4. **B (song song nhiều phiên SwiftShader)** chỉ là dự phòng nếu chủ dự án không chấp nhận hình llvmpipe: giữ hình byte-trùng, nhưng giờ máy 18,5–26 h/tập và phải chia khúc theo mốc cảnh (tất định).

## 9. Chỉ số trong ±5 % quanh ngưỡng (luật cứng)
| Chỉ số | Đo | Ngưỡng | Lệch |
|---|---|---|---|
| SSIM llvmpipe↔SwiftShader khung 280 (min 12 khung) | 0,9009 | ≥ 0,90 (đề xuất §6.3; cũng là ngưỡng tạm khung vàng NT K7) | +0,1 % |
| SSIM khung 190 | 0,9023 | ≥ 0,90 | +0,3 % |
| PSNR ¼ kích thước khung 10 | 40,7 dB | ≥ 40 (đề xuất) | +1,8 % |
| PSNR ¼ kích thước khung 470 bóng 2048 | 39,46 dB | ≥ 40 | −1,4 % (phương án đã bỏ) |
Tiêu chí cấu trúc đặt sau khi thấy số → chủ dự án/K cần duyệt trước khi dùng.

## 10. Chi phí phiên
| Mục | Thực tế |
|---|---|
| Claude API (gọi từ script) | **$0** — không gọi; không có `cost.jsonl` |
| YouTube / ElevenLabs | 0 / 0 |
| Giờ máy (render + dựng) | ≈ **0,55 h**: tải nguồn ≈ 4 phút, dựng gói cảnh 1 phút, hồ sơ + bench ≈ 14 phút, trọn gib20 llvmpipe 9,4 phút, 12 khung × 2 trình dựng 2,2 phút, test trình duyệt × 3 ≈ 2,2 phút, phụ ≈ 2 phút |
| Mạng | ≈ 1,2 GB tải (dữ liệu thô V5b-1, 10/10 KHỚP SHA) |
| Token phiên | 1 tác tử con tra giá/benchmark (≈ 115 nghìn token) + phiên chính |
Dòng `COST-LEDGER.csv` **không ghi** (ngoài vùng tệp được sửa) — đề xuất dòng cho P: `GPU-RD-01, 16/10/2026, GPU-RD, Claude API $0, ElevenLabs 0, YouTube 0, giờ máy 0,55 h, nghiên cứu GPU + đo llvmpipe`.

## 11. Tệp, preflight, ghép thử
- Tệp mới (chỉ 2 vùng được phép): `research/gpu/{profile.js, gl_flags.js, webgl_probe.js, compare.py, so_mp4.py, trace_sum.py, cpu_bench.sh, uoc_tap.py}`, `research/gpu/thu-gpu/{README.md, 0_chuan_bi_cpu.sh, 1_cai_dat_gpu.sh, 2_chay_thu.sh}`, `research/gpu/do/*` (số đo JSON, 2 ảnh so, bản xem 540p 4,5 MB), `reports/GPU-RD-BAO-CAO.md`.
- Preflight: hook pre-commit/pre-push cài đầu lúc commit; `bash tools/preflight.sh --range origin/main..HEAD` → **36 tệp ĐẠT, `lock.py --verify` KHỚP, PREFLIGHT ĐẠT** (commit `0a2a2ef`; chạy lại trước khi đẩy commit cuối). Không dùng `--no-verify`.
- Ghép thử với `main`: nhánh chỉ thêm tệp mới trong `research/gpu/` và một báo cáo → không xung đột với `main`, `v5b1b`.
- Bài học mới (đề xuất cho `reports/m3/BAI-HOC-LL.md`, P ghi): (1) `gl.finish()` trong Chrome không chặn — đo bước dựng phải đồng bộ bằng `readPixels` 1 điểm ảnh; trace Chrome dồn thời gian dựng vào "Readback". (2) Chú thích `//` chèn giữa dòng lại nuốt mã (lần 3, BAI-HOC-LL #42) — `node --check` bắt được. (3) Vòng chờ `until ! pgrep -f "<mẫu>"` khớp chính lệnh của nó → chạy tới hết giờ (lần 3, #24/#41). (4) Preload `node -r` không truyền sang tiến trình con `execFileSync` → dùng `NODE_OPTIONS`.

## 12. Việc chờ chủ dự án
1. **Xem mù** `research/gpu/do/gib20_llvmpipe_540p.mp4` (nhánh `gpu-rd`) cạnh bản SwiftShader `v5b1b/gib20_540p.mp4`, và 2 ảnh so `research/gpu/do/so-hinh-ss-llvmpipe-*.jpg` → quyết có chấp nhận hình llvmpipe (phương án D).
2. **Tiêu chí khớp hình:** giữ tiêu chí chặt của lệnh (PSNR ≥ 40 / ≤ 1 % lệch > 10) hay duyệt tiêu chí cấu trúc §6.3 (giao K). Quyết định này áp cho cả llvmpipe lẫn GPU sau này.
3. Nếu duyệt D: giao phiên V đổi cờ GL theo biến môi trường trong `scripts/k2tl/render.js` (+ đo relief/hero), giao K dựng lại khung vàng trên llvmpipe, ghim Mesa trong môi trường.
4. GPU: giữ hoãn (khuyến nghị) hay duyệt lượt thử §6 (≤ $5; chủ dự án tự tạo tài khoản AWS/GCP, xin hạn mức GPU, nhập thẻ — phiên không làm).
5. P ghi dòng COST-LEDGER `GPU-RD-01` (§10) và 4 bài học (§11).
