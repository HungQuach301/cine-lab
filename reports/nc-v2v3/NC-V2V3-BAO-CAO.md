Nhánh thật: `nc-v2v3` (tạo mới từ `origin/nc-v2v` @2c1d1e12 theo lệnh; harness gợi ý nhánh `ccr-1fd6ea6d-2o3dj8` nhưng làm theo lệnh chủ dự án). Không merge. Chỉ sửa `reports/nc-v2v3/**` và `design/k2v/v2v3/**`; GỌI (không sửa) `design/k2v/v2v/**` và `design/pt/gpu/pod.py`, `pod_srv.py` (đọc từ `origin/claude/eloquent-dijkstra-kemr8j` ra thư mục tạm). Không đụng `scripts/**`, `checks/`, `docs/`, `channel-*/`, nhánh khác. Không đọc mã `checks/` (chỉ đọc `checks/ll/RULES-LL.md` theo lệnh).

# NC-V2V3 — Thử AI video→video BÁM CẤU TRÚC (Wan2.2-VACE-Fun, GPU thuê) điều khiển bằng độ sâu + cạnh + mặt nạ của chính cảnh ta: BÁO CÁO

> Phiên nghiên cứu, 20/10/2026 ≈ 10:00–15:50 UTC. CHỈ đo và báo; không đổi đường ống. Mọi số là số đo thật trong phiên (tệp ở `reports/nc-v2v3/`), trừ chỗ ghi **(ước)**. Không chứa email hay khoá. Khoá RunPod do proxy gắn; mã không đọc/in/ghi khoá; không khoá nào lên pod (trọng số tải ẩn danh từ Hugging Face). User-Agent mọi lệnh của ta: `CineLab-research (+https://github.com/HungQuach301/cine-lab)`. KHÔNG gọi Omni/Gemini.

## §0. Tóm tắt (đọc 2 phút)

**Trả lời câu hỏi chính: KHÔNG.** AI video→video bám cấu trúc (Wan2.2-VACE-Fun-A14B, mô hình mở Apache-2.0, điều khiển bằng bản đồ độ sâu *từ chính renderer* + cạnh + mặt nạ ID) **không giữ được dữ kiện ở 10/10 lượt** (P đọc), và **không đẹp gần Omni**: ở chấm mù nó còn **kém cả bản V7B gốc** (độ thật 3,1 so với 5,0 ở cổng; 3,1 so với 3,4 ở clip; Omni 7,7). Đề xuất **V2V3-D1: không dùng video→video AI trên hình** (giữ §12.3 "KHÔNG video AI"), khép hướng V2V; tiếp tục đường A/Cycles (NC-CPU/NC-GPU).

| Việc | Kết quả đo |
|---|---|
| 0. Mô hình | **Chính: Wan2.2-VACE-Fun-A14B** (alibaba-pai, Apache-2.0), bản fp8 đóng gói của Comfy-Org (Apache-2.0), ComfyUI v0.42.1 trên **1 × RTX 5090 32 GB** (RunPod SECURE $1,19/h). 4 tệp trọng số 41,7 GB, SHA-256 khớp LFS 4/4, tải 68 s. **Loại**: LoRA "Ditto sim2real" cho VACE (CC BY-NC-SA 4.0 — cấm thương mại). **Phụ LTX-2.x: không chạy** (chủ dự án 22:30 chuyển sang Cosmos; giấy phép LTX ghi ở §1). **Cosmos-Transfer2.5-2B: thử 2 lần, không cài được, bỏ, 0 phút pod** (§1b). Giấy phép cho dùng thương mại, nhưng: (1) trọng số gated, tải ẩn danh trả `GatedRepoError: 401`; (2) bản sao cộng đồng int4 không có giấy phép; (3) tài liệu ghi cần 65,4 GB VRAM, lớn hơn 32 GB. Cosmos 3 Nano/Super là ứng viên vòng sau (chỉ đọc tài liệu). |
| 1. Nguồn + điều khiển (CPU) | Máy V7B @317dcf5 (cùng `clips.py` NC-V2V, opt khớp 100 %): 3 cửa sổ **81 khung 1280×720 24 fps (3,4 s)** quanh khung 120 của c2 / c4B / c1 + 3 cửa sổ 17 khung tại 3 điểm cổng NC-CPU/NC-GPU + c4 đủ 481 khung (20 s) cho chế độ C. Mỗi khung: màu (đúng vòng `hero.js`), **độ sâu từ bộ đệm z của renderer** (log 16 bit), mặt nạ ID (idmask.js NC-V2V nguyên văn), lượt "mái phố" riêng. Giữ **24 fps 1:1 với nguồn** (mô hình học 16 fps → chuyển động tự sinh như sóng/khói nhanh ×1,5); **độ dài hạ còn 81 khung/lượt** (giới hạn huấn luyện Wan). |
| 2. Gọi mô hình | **10 lượt 81 khung + 8 lượt cổng 17 khung + 2/7 cửa sổ chế độ C.** A (độ sâu + cạnh toàn khung), B (A + mặt nạ inpaint, ghép lại điểm ảnh nguồn viền ≤ 3 px), **B2 (thêm sau khi B biến đất thành biển: B + khởi từ khung nguồn, khử nhiễu 0,6)**, B2d50 (khử nhiễu 0,5). GPU thuần: A/B **19,7 s/khung**, B2 **12,0 s/khung**, B2d50 10,0 s/khung (720p, 20 bước, hạt 20102026). |
| Kiểu lỗi đổi loại vùng (§4b) | A/B trượt T9 6/6; B2 qua T9 2/3 nhưng xoá vật trong lớp đất 3/3. Wan không có kênh phân vùng — đúng nhận định 19:45. |
| 3. Đo (bộ đo NC-V2V T1–T6 y nguyên + đối chứng không AI + T7 đốm sáng bền ≥ 1 s + T8 vật mới bền + T9 đổi loại vùng) | **Máy cho qua 1/10** (c2-B2d50). **P đọc: 0/10 đạt.** A và B **đổi loại vùng** ở 6/6 lượt (biển → cát ở c2/c1, eo đất → biển ở c4B-B, xoá trại ở c4B-A, ngày → đêm ở c1-A). B2 giữ bố cục nhưng **xoá vật mang dữ kiện nằm trong lớp "đất"**: dải đê lấn biển (c2-B2; c2-B2d50 cắt rời đê khỏi bờ), cụm cây thành vòng rỗng + xoá lối mòn (c4B-B2), xoá bãi cạn trên vịnh (c1-B2). **T3 "cạnh mới" ≈ 0 ở mọi lượt** dù AI bịa/xoá cả vùng → phép đo cũ không bắt được lỗi kiểu này; T9 mới bắt được. |
| (C) Nối c4A + c4B 20 s | **Dừng theo lệnh chủ dự án sau 2/7 cửa sổ** (6,4 s, B2 nối tiếp 9 khung ngữ cảnh): đường nối **3,55 × nền** (thấy được; Omni 28–65 ×). §5. |
| 4. Chấm mù (3 vai Sonnet 5.5, giao thức NC-GPU, 640 + 320) | **Cổng:** Cycles GPU hạng nhất 6/9, A (NC-CPU) 3/9, V7B 0/9, **V2V3-B2 0/9, hạng TB 4,0/4 (cuối ở mọi cổng, mọi cỡ)**; độ thật GPU 5,89 · A 5,55 · V7B 5,00 · **V2V3-B2 3,11**. **Clip:** Omni-a (có vật bịa) hạng nhất 9/9, độ thật 7,67; V7B 3,44; **V2V3-B2 3,11**; V2V3-A 3,56. Lời phê: "washed out", "flat colour field", "game-like". |
| 5. Ước cả tập 745 s | ≈ 300 cửa sổ × 973 s ≈ **81 h GPU ≈ $97 (720p, 1 lượt, ước)**; tỉ lệ đạt đo được **0/10** → cận trên 95 % ≈ 30 % → **≥ 3,3 lượt/cửa sổ ≈ ≥ $320 và không chắc hội tụ**; + ≈ 30 h CPU dựng nguồn/điều khiển; + ≈ 10 h P đọc tờ so. Trượt §12.2 (10/10), §12.3, K-LAI-5 (đêm c1-B2: 1,7 % điểm > 1,5 × A + 2/255, ngưỡng 0,5 %). |
| GPU bật/tắt + tiền | 2 pod RTX 5090 SECURE, **5,01 h**, RunPod **$6,05 thật** (số dư $14,02 → $7,97). Mọi pod đã xoá, `GET /pods` = `[]`. §7. |
| Chi phí khác | Claude chấm mù **$2,046** (mốc $8). OpenAI $0 · Gemini $0 · ElevenLabs $0. CPU ≈ **2,6 h** đồng hồ (mốc 8 h). |

**Xem nhanh:** `clip/luoi-c2.mp4`, `luoi-c4B.mp4`, `luoi-c1.mp4` (lưới 3 × 2: nguồn | A | B / B2 | B2 khử nhiễu 0,5 hoặc vùng AI vẽ | Omni-a cùng khung) · `to-so/to-so-c4B-B.png` (eo đất thành biển) · `to-so/to-so-c2-B2.png` (xoá đê) · `to-so/zoom-*.jpg`.

## §1. Mô hình + giấy phép (đọc 20/10/2026)

**Chọn:** Wan VACE theo lệnh. Đọc thẻ mô hình qua API Hugging Face (`/api/models/<repo>?blobs=true`, 20/10/2026 ≈ 10:05 UTC) và mã ComfyUI (`comfy_extras/nodes_wan.py` @ v0.42.1: nút `WanVaceToVideo` gắn `vace_frames/vace_mask/vace_strength` với `append=True` → **nhiều lớp điều khiển nối tiếp được**: độ sâu + cạnh).

| Repo | Bản (commit) | Tệp dùng (SHA-256 = LFS oid, khớp sau tải) | Giấy phép nguyên văn | URL |
|---|---|---|---|---|
| Comfy-Org/Wan_2.2_ComfyUI_Repackaged | `ee6f4a40737a995bf5818954cfce6d59443b0f04` | `wan2.2_fun_vace_high_noise_14B_fp8_scaled.safetensors` 17,35 GB `23130f30…1fb54c` · `…low_noise…` 17,35 GB `ca55a5cc…dbcb69` · `umt5_xxl_fp8_e4m3fn_scaled.safetensors` 6,74 GB `c3355d30…204f68` · `wan_2.1_vae.safetensors` 0,25 GB `2fc39d31…48976b` | thẻ: `license: apache-2.0` (`giay-phep/Comfy-Org_…_README-dau.md`) | https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged |
| alibaba-pai/Wan2.2-VACE-Fun-A14B (gốc của tệp trên) | `4438caabbfdd7437bbb0283d86cb200d1b7223ba` | — | thẻ: `license: apache-2.0`; README: "本项目采用 [Apache License (Version 2.0)](https://github.com/modelscope/modelscope/blob/master/LICENSE)." (`giay-phep/alibaba-pai_…_README-trich.md`) | https://huggingface.co/alibaba-pai/Wan2.2-VACE-Fun-A14B |
| Wan-AI/Wan2.1-VACE-14B (họ VACE, văn bản giấy phép đầy đủ) | `539c162b1387eac9dc4c20bd3f74671309e76a4c` | — | "The models in this repository are licensed under the Apache 2.0 License. We claim no rights over the your generated contents, granting you the freedom to use them while ensuring that your usage complies with the provisions of this license. …" + `LICENSE.txt` Apache 2.0 đầy đủ (`giay-phep/Wan-AI_…`) | https://huggingface.co/Wan-AI/Wan2.1-VACE-14B |
| QingyanBai/Ditto_models (LoRA "sim2real" cho VACE 14B) | — | **KHÔNG dùng** | thẻ: `license: cc-by-nc-sa-4.0` → cấm thương mại (kênh kiếm tiền) | https://huggingface.co/QingyanBai/Ditto_models |
| Lightricks/LTX-2.3 (phụ, không chạy) | `3c6a4e66e5d0a684231950b9c74dd4ded7b6fadc` | — | "LTX-2 Community License Agreement": "Entities with annual revenues of at least $10,000,000 (the "Commercial Entities") are required to obtain a paid commercial license …" (`giay-phep/Lightricks_LTX-2.3_LICENSE.txt`, dòng 80–91) → **ngưỡng doanh thu $10 triệu/năm**, kênh dưới ngưỡng thì dùng được; IC-LoRA hiện có: `LTX-2.3-22b-IC-LoRA-Union-Control`, `LTX-2-19b-IC-LoRA-Depth/Canny-Control`, `LTX-2.5-22b-IC-LoRA-Layout-To-Render` | https://huggingface.co/Lightricks/LTX-2.3 |

Kết luận giấy phép: Wan2.2-VACE-Fun (Apache-2.0) **cho phép dùng thương mại** trên kênh YouTube kiếm tiền và phim bán; đầu ra không mang C2PA/SynthID (khác Omni) → nếu dùng phải tự khai. Trọng số là **công cụ**, không phải tài sản trên hình → ghi vào RIGHTS phần "công cụ" (việc phiên P).

**Môi trường pod:** ảnh `python:3.12-bookworm` + venv torch **2.14.1+cu130** (PyPI/download.pytorch.org) + ComfyUI **v0.42.1** (`63be2f9b82ad0dac88a7ceaa28a9cf3154125a18`, 18/10/2026) + nút đọc/ghi PNG riêng (`design/k2v/v2v3/comfy_node/`). RTX 5090 32 607 MiB, driver 595.91.07, RAM 503 GB. Cài + tải trọng số **184–191 s/pod**. Máy chủ tệp `pod_srv.py` của NC-GPU (mã ngẫu nhiên một lần, không khoá dịch vụ).

## §1b. NVIDIA Cosmos-Transfer2.5-2B (bổ sung 17:20 / 19:45 / 22:10 / 22:30) — KHÔNG cài được, bỏ, 0 phút pod

- **Mô hình:** https://huggingface.co/nvidia/Cosmos-Transfer2.5-2B (commit `ce8440327c632d8313c3bde69db13b627ba5cae1`, đọc 20/10/2026). Mã: https://github.com/nvidia-cosmos/cosmos-transfer2.5 @`2ff49d0717af02057ae79bc75c00fbff9da1b4e7` (07/06/2026). Đây là multi-controlnet có điều khiển depth / **seg** / edge / blur, trọng số từng điều khiển và mặt nạ không gian, đúng việc "CG → ảnh thật" mà lệnh mô tả.
- **Giấy phép** (đọc nguyên văn 20/10/2026, https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license, "Last Modified: October 24, 2025"; bản chữ `giay-phep/NVIDIA-Open-Model-License.txt`): "Models are commercially usable. You are free to create and distribute Derivative Models. NVIDIA does not claim ownership to any outputs generated using the Models or Derivative Models." → **cho phép dùng thương mại**. Điều kiện đáng chú ý: "If You bypass, disable, reduce the efficacy of, or circumvent any technical limitation, safety guardrail … your rights under this Agreement will automatically terminate." Bảng thời gian chạy của NVIDIA đo khi "disabled guardrails", nhưng theo giấy phép thì tắt bộ lọc có thể làm mất quyền dùng. Cần luật sư hoặc chủ dự án đọc lại nếu dùng.
- **Lần thử 1** (container, ẩn danh, 20/10 ≈ 15:55 UTC): `hf_hub_download('nvidia/Cosmos-Transfer2.5-2B', 'general/depth/…_ema_bf16.pt')` → nguyên văn: `GatedRepoError: 401 Client Error. … Cannot access gated repo for url https://huggingface.co/nvidia/Cosmos-Transfer2.5-2B/resolve/main/general/depth/0f214f66-ae98-43cf-ab25-d65d09a7e68f_ema_bf16.pt. Access to model nvidia/Cosmos-Transfer2.5-2B is restricted. You must have access to it and be authenticated to access it. Please log in.` Hướng dẫn chính thức (`docs/setup.md`) yêu cầu "Get a Hugging Face Access Token … `hf auth login` … Accept the NVIDIA Open Model License Agreement". Bộ lọc an toàn `meta-llama/Llama-Guard-3-8B` cũng trả 401.
- **Lần thử 2:** bản sao cộng đồng không khoá `circulus/Cosmos-Transfer2.5-2B-bnb-int4` (@`6c16e548…`). **Không có trường giấy phép, không có README ("Entry not found"), không rõ nguồn gốc**, và là bản lượng tử int4 không đối chiếu được SHA với bản chính thức → không đủ điều kiện "nguồn công khai + giấy phép nguyên văn". Bỏ.
- **Thêm một chặn nữa dù có tải được:** tài liệu `docs/inference.md` ghi "Cosmos-Transfer2.5-2B | Required GPU VRAM 65.4 GB" > 32 GB của RTX 5090. Máy rẻ nhất đủ VRAM trên RunPod là RTX PRO 6000 96 GB ($2,49/h SECURE) hoặc H100.
- Không bật pod cho Cosmos; tốn $0. Lỗi nguyên văn đầy đủ ở `cosmos/LOI-NGUYEN-VAN.txt`. Muốn chạy được thì chủ dự án phải (a) chấp nhận giấy phép trên tài khoản HF, (b) cho phép một token HF chỉ-đọc trên pod (hiện trái luật phiên), (c) thuê GPU ≥ 80 GB.
- **Cosmos 3 (ứng viên vòng sau — chỉ đọc tài liệu, không chạy):** `nvidia/Cosmos3-Nano` (@`e59a53c2…`, 35,0 GB trọng số) và `nvidia/Cosmos3-Super` (@`f543c562…`, 132,7 GB). Cả hai tạo ngày **10/03/2026** trên HF (lệnh ghi "ra 06/2026"; tôi ghi theo API), **không gated**, giấy phép `openmdw1.1-license` (chưa đọc nguyên văn, vòng sau phải đọc). Thẻ mô hình liệt kê nhiệm vụ "video transfer"; "Test Hardware: GB200 and H100"; Super khuyến nghị 8×H100/H200. Khớp nhận định cần RTX PRO 6000/H100 trở lên.

## §2. Nguồn + điều khiển (bước 1, CPU)

**Máy dựng:** worktree đọc-chỉ `/var/tmp/v7b-wt` @ `origin/ccr-ef2b66f0-9639kq` 317dcf5 (V7B), bộ đệm k2tl dựng lại bằng `v7p_cache.sh` (+ `v7b_mau_nha.py`, `v7b_faden.py`; LUT từ `origin/v5a`, mọi SHA nguồn KHỚP). Opt shot = `design/k2v/v2v/clips.py` (NC-V2V) → `clips-opt.json` **khớp từng byte JSON** với `reports/nc-v2v/clips-opt.json`. Mức dựng = mặc định `hero.js` (spp 1, nháp), như NC-V2V.

**Driver một lần dựng** `design/k2v/v2v3/dung3.js` trên trang tạm `page-v2v3.js` (bản sao `page.js` V7B + `../v2v/idmask.js` nguyên văn + `depth.js`, tạo bởi `mk_page3.py`, không sửa tệp gốc). Mỗi khung:
1. **Màu**: đúng vòng `scripts/k2/hero.js` (`renderFrame` → `finalize` → ffmpeg vflip JPEG q2).
2. **Độ sâu từ chính renderer** (`depth.js`): dựng lại cảnh vào đích có `DepthTexture` float → mọi shader tự dời đỉnh (địa hình, nước, cờ bay) ghi độ sâu thật; đổi z bộ đệm → khoảng cách mắt tuyến tính (m); mã hoá log 16 bit (1 m – 60 km). **Không ước độ sâu bằng AI** (§12.3).
3. **Mặt nạ ID** 10 loại (idmask.js NC-V2V, toàn 1280×720).
4. **Mái phố**: lượt riêng chỉ địa hình + mesh `makeCity` (không gồm công sự, trại, phế tích, mốc, nhà hero, pin nổi, tàu, cờ, đèn).
- Tốc độ: ≈ 11–15 s/khung/làn (màu 5,9 · độ sâu 1,5 · ID 3,4 · mái ≈ 0,5), 2 làn trên 4 vCPU.
- **Lỗi đã gặp và sửa:** lượt mái đọc trạng thái nước/trời SAU khi ẩn → từ khung thứ 2 mất trời/nước trong khung màu; phát hiện bằng so khung 120 ↔ 121, sửa, dựng lại toàn bộ.

**Điều khiển** (`ctrl3.py`, mỗi cửa sổ):
- `depth/`: nghịch đảo khoảng cách, chuẩn hoá MỘT LẦN cho cả cửa sổ (phân vị 1–99 %), gần sáng – xa tối, trời 0. Chế độ C: chuẩn hoá cố định cho cả 20 s.
- `canny/`: Canny trên khung màu nguồn (Gauss σ 1,5, ngưỡng 60/150).
- `mask/` (chế độ B/B2): trắng = AI được vẽ = trời ∪ nước ∪ đất/thực vật ∪ **mái phố** (lớp nhà ∩ mesh phố ∩ pháp tuyến thế giới lên ≥ 0,8, tính từ chính bản đồ độ sâu + ma trận máy). Vùng giữ (tàu, cờ, pin nổi, lửa, người, khác, công trình không phải mái phố) nới 2 px. Phần trăm vùng AI vẽ: c2 **76,5 %** (mái 7,5 %), c4B **79,4 %**, c1 **67,8 %**.
- `bdepth/`, `bcanny/`: điểm ảnh nguồn ở vùng giữ + độ sâu/cạnh ở vùng vẽ (quy ước `WanVaceToVideo`: inactive = ctrl·(1−m), reactive = ctrl·m).
- `alpha/`: hệ số ghép sau cùng, **0 trên mọi vùng giữ** (đúng điểm ảnh nguồn), tăng tuyến tính tới 1 trong 3 px phía vùng vẽ.

| Cửa sổ | Khung (tuyệt đối) | Nội dung | Ngoài git `/var/tmp/cine-out/v2v3/` |
|---|---|---|---|
| c2 | 80–160 của c2 (H3 máy D, 2026 ngày) | La Línea + Gibraltar 2026 | `src/c2/`, `ctrl/c2/`, `vid/c2-nguon.mp4` |
| c4B | 320–400 của c4 (C1-a, trại 1779) = khung 80–160 của c4B NC-V2V | đoạn Omni bịa nặng nhất | `src/c4B/`, `ctrl/c4B/` |
| c1 | 344–424 của H2 (khung 80–160 của c1 NC-V2V) | vây hãm 1782, **chiều → đêm**, pin nổi cháy | `src/c1/`, `ctrl/c1/` |
| g-hero · g-vay-ham · g-bo-chien-su | 242–258 (H3) · 515–531 (C1a) · 311–327 (H2), khung giữa = cổng NC-CPU | 3 cổng có A + Cycles GPU cùng chỗ | `src/g-*/`, `ctrl/g-*/` (`gates3.py`) |
| c4full (chế độ C) | 0–480 của c4 | 20 s c4A + c4B | `src/c4full/` (hợp nhất 5 lượt dựng) |

SHA-256 video nguồn cửa sổ, tar điều khiển, và chuỗi PNG độ sâu/cạnh/mặt nạ từng cửa sổ: `SHA256-nguon-dieu-khien.txt`. Mẫu: `to-so/` (cột nguồn), `clip/luoi-*.mp4` (ô "vùng AI được vẽ").

## §3. Gọi mô hình (bước 2)

Đồ thị ComfyUI dựng bằng mã (`wf_vace.py`): UNETLoader × 2 (chuyên gia nhiễu cao/thấp) → ModelSamplingSD3 shift 8 → `WanVaceToVideo` × 2 nối tiếp (lớp 1 độ sâu, lớp 2 cạnh, cường độ 1,0 / 1,0) → KSamplerAdvanced nhiễu cao bước 0–10 → nhiễu thấp 10–20 → VAEDecode → PNG. euler/simple, cfg 3,5, **20 bước**, **hạt 20102026** mọi lượt, 1280×720, 81 khung. Lệnh nguyên văn: `design/k2v/v2v3/prompts3.json` (phần chung "Photorealistic aerial documentary footage… nothing added, nothing removed" + mô tả clip CHỈ kể vật có trong nguồn + âm bản liệt kê vật hay bị bịa ở NC-V2V: lửa, khói, tàu, máy bay, sân vận động, quân, cờ).

| Chế độ | Khác biệt | Ghép sau cùng |
|---|---|---|
| A | điều khiển độ sâu + cạnh toàn khung, khởi từ nhiễu | không (toàn khung AI) |
| B | như A, mỗi lớp mang điểm ảnh nguồn ở vùng giữ + mặt nạ | dán lại nguồn trên vùng giữ, viền ≤ 3 px (K-LAI-4 trên PNG: \|ra − nguồn\| = **0,000** ở mọi lượt B/B2) |
| **B2** (thêm trong phiên) | như B + **khởi từ khung nguồn** (VAE mã hoá) và chỉ khử nhiễu 0,6 (bước 8–20) | như B |
| B2d50 | như B2, khử nhiễu 0,5 (bước 10–20, tách chuyên gia ở 11) | như B |

Lý do thêm B2: sau c4B-B (AI biến cả eo đất thành biển) và c1-B (biến vịnh thành cát) — **cùng một lỗi ≥ 2 lần ở B và 3/3 ở A** → đổi cách theo luật "cùng lỗi ≥ 3 lần → đổi cách". Độ sâu không phân biệt được đất phẳng với nước phẳng; chỉ có màu nguồn mang ngữ nghĩa vùng.

**Sửa lệnh trong phiên:** c1 lúc đầu ghi "Night, 1782" trong khi cửa sổ đi từ chiều sang đêm → c1-A ra đêm từ khung 0 (lỗi lệnh của phiên). Sửa thành "Late afternoon light fading into night…" cho c1-B2 (bản cũ giữ trong `prompts3.json` khoá `c1_v1_da_dung_cho_c1A_c1B`).

| Lượt | GPU thuần (ComfyUI "Prompt executed") | s/khung GPU |
|---|---|---|
| c2-A, c4B-B, c1-B, c2-B, c4B-A, c1-A (81 khung, 20 bước) | 1 572–1 603 s | **19,4–19,8** |
| c2-B2, c4B-B2, c1-B2 (81 khung, 12 bước thật) | 965–973 s | **11,9–12,0** |
| c2-B2d50 | 812 s | 10,0 |
| cổng × A/B (17 khung) | 157–161 s | 9,2–9,5 |
| cổng × B2 (17 khung) | 99–100 s | 5,8–5,9 |
| bước khử nhiễu 81 khung 720p | 76–78 s/bước (2 lớp VACE) | — |
| thử 17 khung (pod 1) | 7,3 s/bước | — |

## §4. Đo (bước 3) — `do_v2v.py` (NC-V2V, không sửa) + `do_them3.py` + `danh_gia3.py`

**Đối chứng không AI** mỗi cửa sổ (cách NC-V2V: phóng 2 %, dịch 5/3 px, sáng +0,04, bão hoà ×1,15, mờ σ 0,8, nén crf 23): `do/*-dc*.json`. Sàn đáng chú ý: c4B đối chứng giữ cờ trại chỉ **53,7 %** (cờ trại rất nhỏ); c1 đối chứng "lửa mới" max 0,482 % và đất→nước 7,4 % (đất đêm ngả lam).

**Ngưỡng:** T1–T6 Y NGUYÊN `design/k2v/v2v/danh_gia.py`. Thêm, ghi trong `danh_gia3.py` **trước khi đọc kết quả B2**:
- **T7** đốm sáng mới bền ≥ 1 s (bài học NC-V2V §4.1): điểm sáng cục bộ mới (V ≥ 0,63, V − trung vị 15×15 ≥ 40/255, cách mọi điểm sáng/lửa/pin nổi nguồn > 6 px), nối vệt qua khung, vệt ≥ 24 khung; đạt khi ≤ max(1, đối chứng) và 0 vệt màu lửa.
- **T8** vật mới bền ≥ 1 s trong vùng trống: thành phần liên thông cạnh mới ≥ 40 px nối qua khung; đạt khi 0.
- **T9** đổi loại vùng (thêm sau c4B-B, ghi trước khi có B2/c1): % điểm lớp đất có màu nước ở đầu ra mà nguồn không (đất→nước) và chiều ngược lại; đạt khi mỗi chiều ≤ max(2 %, đối chứng + 2 điểm).
- **ĐẠT = qua T1–T9 VÀ P đọc tờ so không thấy vật bịa/dữ kiện đổi** (`p_doc.json`).

**Bảng biến thể × số đo** (`danh-gia.md` / `danh-gia.json`; số thô `do/*.json`):

| Clip-chế độ | T1 giữ tàu / cờ / pin (÷ đc) | T2 F1 nhà · tàu | T3 cạnh mới trời · nước · đất % | T4 lửa mới max % (sàn) | T5 nhấp nháy ÷ đc | T6 dịch px · tỉ lệ · lệch khung | T7 đốm sáng bền (lửa) · đc | T8 vật mới bền | T9 đất→nước · nước→đất % | Chi tiết nguồn → ra | Bão hoà nguồn → ra | Máy | P đọc | Kết luận |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| c2-A | tau 0.20 (0.20) | 0.86 · 0.424 | troi 0.0 · nuoc 0.0 · dat 0.0 | 9.352 (0.050) | 0.81 | 1.26 · 1.0043 · kxđ | 0 (0) · 1 | 0 | 0.45 · 43.72 | 47.4 → 8.7 | 0.34 → 0.36 | LOẠI: T1 tau, T2 tàu, T4 lửa, T9 đổi loại vùng | LOẠI: đường bờ dời: vịnh nước giữa–phải khung thành bãi cát, biển lùi sang phải; đê chắn sóng/cầu tàu bên phải biến mất; mọi toà nhà mất màu có nguồn (S2/OSM) thành khối cát như phế tích; bãi cỏ/sân xanh thành cát; thêm mảng đỏ (sân/mái đỏ) ở dưới–giữa và phải không có trong nguồn; tàu xa gần như mất (máy: giữ 20 %) | LOẠI |
| c2-B | tau 1.00 (1.00) | 0.996 · 0.989 | troi 0.0 · nuoc 0.04 · dat 0.16 | 0.278 (0.050) | 1.04 | 0.0 · 1.0 · kxđ | 6 (0) · 1 | 1 | 1.03 · 19.35 | 47.4 → 37.3 | 0.34 → 0.33 | LOẠI: T4 lửa, T7 đốm sáng bền, T8 vật mới bền, T9 đổi loại vùng | LOẠI: vịnh giữa khung (giữa đê chắn sóng và phố) bị vẽ thành bãi cát, đường bờ dời sang phải (máy: nước→đất 19,4 %); đê/cầu tàu bên phải mất; bãi cỏ và sân xanh thành cát; Rock mất thảm thực vật xanh thành đá nâu tím; viền lam sáng quanh tàu và mép nhà (ghép vùng giữ); mái phố được vẽ lại nhưng giữ khối | LOẠI |
| c2-B2 | tau 1.00 (1.00) | 0.996 · 0.998 | troi 0.0 · nuoc 0.0 · dat 0.0 | 0.016 (0.050) | 1.51 | 0.11 · 1.0004 · kxđ | 2 (1) · 1 | 0 | 1.5 · 1.91 | 47.4 → 34.3 | 0.34 → 0.33 | LOẠI: T5 nhấp nháy, T7 đốm sáng bền | LOẠI: giữ đúng đường bờ, vịnh, Rock, bãi cỏ, phố và tàu; NHƯNG XOÁ dải đê/đường băng lấn biển màu xám chạy từ đầu đường băng ra giữa vịnh (lớp ID 'đất', nằm trong vùng AI được vẽ) — dữ kiện công trình đổi; xoá vệt sáng phản chiếu trên vịnh xa; mép vùng giữ quanh tàu còn viền lam nhẹ | LOẠI |
| c2-B2d50 | tau 1.00 (1.00) | 0.996 · 1.0 | troi 0.0 · nuoc 0.0 · dat 0.0 | 0.014 (0.050) | 1.47 | 0.17 · 1.0003 · kxđ | 0 (0) · 1 | 0 | 1.09 · 1.7 | 47.4 → 34.4 | 0.34 → 0.33 | qua | LOẠI: khử nhiễu 0,5: giữ bờ, vịnh, Rock, bãi cỏ, phố, tàu và PHẦN LỚN dải đê lấn biển; nhưng đoạn gốc đê nối với bờ (≈ 1/4 chiều dài) bị XOÁ → đê thành dải nổi rời khỏi bờ (dữ kiện công trình đổi); vệt phản chiếu xa trên vịnh bị xoá; mặt nước/đá ít 'thật' hơn B2 0,6 | LOẠI |
| c4B-A | co 0.00 (0.00) | 0.559 · 0.0 | troi 0.0 · nuoc 1.14 · dat 0.06 | 47.061 (0.050) | 1.27 | 0.0 · 1.0 · kxđ | 9 (8) · 0 | 2 | 0.0 · 99.57 | 20.3 → 15.4 | 0.57 → 0.65 | LOẠI: T1 co, T2 nhà, T2 tàu, T4 lửa, T7 đốm sáng bền, T8 vật mới bền, T9 đổi loại vùng | LOẠI: XOÁ hai dãy trại (lều chỉ còn vệt mờ), xoá tàu ngoài khơi, xoá cây và mảng cỏ xanh → sa mạc nâu cam đồng màu; THÊM một đống đá/phế tích ở giữa–phải không có trong nguồn; biển xám mất màu (máy: nước→đất 99,6 % theo màu); toàn khung 'lửa mới' theo màu cam (dương tính giả T4 do màu cát, nhưng vẫn là đổi màu dữ kiện) | LOẠI |
| c4B-B | co 1.00 (1.86) | 0.939 · 0.992 | troi 0.0 · nuoc 0.99 · dat 0.04 | 0.058 (0.050) | 1.28 | 0.0 · 1.0 · kxđ | 6 (1) · 0 | 2 | 26.35 · 15.2 | 20.3 → 13.1 | 0.57 → 0.51 | LOẠI: T4 lửa, T7 đốm sáng bền, T8 vật mới bền, T9 đổi loại vùng | LOẠI: eo đất cát giữa khung bị vẽ thành BIỂN/đầm nước xanh (dữ kiện địa lý đổi), chỉ còn hai dải trại (vùng giữ) như đảo; viền 'hộp' sáng quanh tàu xa và cờ trại (ghép vùng giữ lộ nền biển nguồn); thêm cồn cát/bãi rời trên mặt nước | LOẠI |
| c4B-B2 | co 1.00 (1.86) | 0.984 · 1.0 | troi 0.0 · nuoc 0.0 · dat 0.01 | 0.063 (0.050) | 1.43 | 0.02 · 0.9999 · kxđ | 1 (0) · 0 | 0 | 0.07 · 3.12 | 20.3 → 15.0 | 0.57 → 0.59 | LOẠI: T4 lửa, T9 đổi loại vùng | LOẠI: giữ đúng bờ biển, eo đất, Rock, hai dãy trại và tàu xa (không đổi loại vùng); NHƯNG cụm cây (lớp đất/thực vật, vùng AI vẽ) biến thành các VÒNG RỖNG như bóng ma, lối mòn trắng uốn cong bị XOÁ, mảng cỏ xanh nhạt hẳn; vệt xanh sáng chạy dọc mép vùng giữ của dãy trại (đường ghép); cả khung mờ sương, chi tiết 20,3 → thấp hơn | LOẠI |
| c1-A | tau 0.60 (0.60) · co 0.04 (0.04) · pin 1.00 (1.00) | 0.074 · 0.901 | nuoc 0.04 · dat 0.0 | 0.008 (1.446) | 0.83 | 0.25 · 1.0002 · 1.5 | 3 (0) · 0 | 0 | 2.4 · 49.25 | 27.1 → 1.8 | 0.75 → 0.40 | LOẠI: T1 tau, T1 co, T2 nhà, T6 thời gian, T7 đốm sáng bền, T9 đổi loại vùng | LOẠI: ĐỔI THỜI ĐIỂM: khung đầu cửa sổ là ban ngày (nắng chiều) nhưng đầu ra tối đen như đêm từ khung 0 (lệnh 'Night, 1782' — lỗi lệnh của phiên, đã sửa cho c1-B2); phố mất mái ngói đỏ thành khối xám; cờ Union bên phải thành một ĐỐM LỬA sáng (bịa lửa, mất cờ); khói pin nổi đen thành khói trắng nhạt; công sự gần như mất trong bóng tối | LOẠI |
| c1-B | tau 1.00 (1.00) · co 0.99 (1.03) · pin 1.00 (1.00) | 0.99 · 0.997 | nuoc 0.0 · dat 0.02 | 15.749 (1.446) | 2.74 | 0.19 · 1.0001 · -3.0 | 1 (1) · 0 | 0 | 0.22 · 96.88 | 27.1 → 9.5 | 0.75 → 0.47 | LOẠI: T4 lửa, T5 nhấp nháy, T6 thời gian, T7 đốm sáng bền, T9 đổi loại vùng | LOẠI: cả mặt vịnh (vùng nước) bị vẽ thành bãi cát/sa mạc vàng ở khung ngày, nâu sẫm khi chiều (máy: nước→đất 96,9 %); viền lam sáng quanh mọi tàu/pin nổi và mép công sự (ghép vùng giữ lộ nước nguồn); đồng cỏ xanh trong thành thành cát; ở khung đêm lửa pin nổi giữ (vùng giữ) nhưng mặt nước không còn phản chiếu | LOẠI |
| c1-B2 | tau 1.00 (1.00) · co 1.00 (1.04) · pin 1.00 (1.00) | 0.994 · 0.998 | nuoc 0.06 · dat 0.01 | 2.095 (1.446) | 1.05 | 0.08 · 0.9998 · -1.0 | 1 (1) · 0 | 0 | 0.48 · 1.09 | 27.1 → 18.6 | 0.75 → 0.65 | LOẠI: T4 lửa, T7 đốm sáng bền | LOẠI: lệnh đã sửa ('chiều → đêm'): giữ đúng chuyển ngày → đêm, pin nổi + lửa + khói (vùng giữ), phố, công sự, cầu tàu; NHƯNG XOÁ bãi cạn/đảo cát nhỏ trên mặt vịnh bên phải cầu tàu (lớp đất, vùng AI vẽ) và mép bãi phía phải; thêm bóng tối hình nêm cạnh cầu tàu; viền lam sáng bao quanh cầu tàu (đường ghép); sóng nước mất vân, mặt nước phẳng như kính | LOẠI |

**P đọc tờ so** (`to-so/to-so-<clip>-<chế độ>.png`: 3 hàng thời điểm + hàng cạnh mới đỏ / lửa mới vàng; phóng to `to-so/zoom-*.jpg`) — mọi vật bịa/dữ kiện đổi thấy được:

| Lượt | P đọc (mọi vật bịa / dữ kiện đổi thấy được) | P |
|---|---|---|
| c2-A | đường bờ dời: vịnh nước giữa–phải khung thành bãi cát, biển lùi sang phải; đê chắn sóng/cầu tàu bên phải biến mất; mọi toà nhà mất màu có nguồn (S2/OSM) thành khối cát như phế tích; bãi cỏ/sân xanh thành cát; thêm mảng đỏ (sân/mái đỏ) ở dưới–giữa và phải không có trong nguồn; tàu xa gần như mất (máy: giữ 20 %) | LOẠI |
| c4B-B | eo đất cát giữa khung bị vẽ thành BIỂN/đầm nước xanh (dữ kiện địa lý đổi), chỉ còn hai dải trại (vùng giữ) như đảo; viền 'hộp' sáng quanh tàu xa và cờ trại (ghép vùng giữ lộ nền biển nguồn); thêm cồn cát/bãi rời trên mặt nước | LOẠI |
| c1-B | cả mặt vịnh (vùng nước) bị vẽ thành bãi cát/sa mạc vàng ở khung ngày, nâu sẫm khi chiều (máy: nước→đất 96,9 %); viền lam sáng quanh mọi tàu/pin nổi và mép công sự (ghép vùng giữ lộ nước nguồn); đồng cỏ xanh trong thành thành cát; ở khung đêm lửa pin nổi giữ (vùng giữ) nhưng mặt nước không còn phản chiếu | LOẠI |
| c2-B | vịnh giữa khung (giữa đê chắn sóng và phố) bị vẽ thành bãi cát, đường bờ dời sang phải (máy: nước→đất 19,4 %); đê/cầu tàu bên phải mất; bãi cỏ và sân xanh thành cát; Rock mất thảm thực vật xanh thành đá nâu tím; viền lam sáng quanh tàu và mép nhà (ghép vùng giữ); mái phố được vẽ lại nhưng giữ khối | LOẠI |
| c4B-A | XOÁ hai dãy trại (lều chỉ còn vệt mờ), xoá tàu ngoài khơi, xoá cây và mảng cỏ xanh → sa mạc nâu cam đồng màu; THÊM một đống đá/phế tích ở giữa–phải không có trong nguồn; biển xám mất màu (máy: nước→đất 99,6 % theo màu); toàn khung 'lửa mới' theo màu cam (dương tính giả T4 do màu cát, nhưng vẫn là đổi màu dữ kiện) | LOẠI |
| c2-B2 | giữ đúng đường bờ, vịnh, Rock, bãi cỏ, phố và tàu; NHƯNG XOÁ dải đê/đường băng lấn biển màu xám chạy từ đầu đường băng ra giữa vịnh (lớp ID 'đất', nằm trong vùng AI được vẽ) — dữ kiện công trình đổi; xoá vệt sáng phản chiếu trên vịnh xa; mép vùng giữ quanh tàu còn viền lam nhẹ | LOẠI |
| c1-A | ĐỔI THỜI ĐIỂM: khung đầu cửa sổ là ban ngày (nắng chiều) nhưng đầu ra tối đen như đêm từ khung 0 (lệnh 'Night, 1782' — lỗi lệnh của phiên, đã sửa cho c1-B2); phố mất mái ngói đỏ thành khối xám; cờ Union bên phải thành một ĐỐM LỬA sáng (bịa lửa, mất cờ); khói pin nổi đen thành khói trắng nhạt; công sự gần như mất trong bóng tối | LOẠI |
| c4B-B2 | giữ đúng bờ biển, eo đất, Rock, hai dãy trại và tàu xa (không đổi loại vùng); NHƯNG cụm cây (lớp đất/thực vật, vùng AI vẽ) biến thành các VÒNG RỖNG như bóng ma, lối mòn trắng uốn cong bị XOÁ, mảng cỏ xanh nhạt hẳn; vệt xanh sáng chạy dọc mép vùng giữ của dãy trại (đường ghép); cả khung mờ sương, chi tiết 20,3 → thấp hơn | LOẠI |
| c2-B2d50 | khử nhiễu 0,5: giữ bờ, vịnh, Rock, bãi cỏ, phố, tàu và PHẦN LỚN dải đê lấn biển; nhưng đoạn gốc đê nối với bờ (≈ 1/4 chiều dài) bị XOÁ → đê thành dải nổi rời khỏi bờ (dữ kiện công trình đổi); vệt phản chiếu xa trên vịnh bị xoá; mặt nước/đá ít 'thật' hơn B2 0,6 | LOẠI |
| c1-B2 | lệnh đã sửa ('chiều → đêm'): giữ đúng chuyển ngày → đêm, pin nổi + lửa + khói (vùng giữ), phố, công sự, cầu tàu; NHƯNG XOÁ bãi cạn/đảo cát nhỏ trên mặt vịnh bên phải cầu tàu (lớp đất, vùng AI vẽ) và mép bãi phía phải; thêm bóng tối hình nêm cạnh cầu tàu; viền lam sáng bao quanh cầu tàu (đường ghép); sóng nước mất vân, mặt nước phẳng như kính | LOẠI |

**Đọc kết quả:**
1. **A (toàn khung) và B (mặt nạ, khởi từ nhiễu) đổi ngữ nghĩa vùng ở 6/6 lượt.** Độ sâu + cạnh chỉ giữ *hình*; mặt đất phẳng và mặt nước phẳng có cùng độ sâu, cùng "không cạnh" → mô hình tự chọn cát hay nước theo lệnh và thói quen ảnh. T9: c4B-B đất→nước **26,4 %**, c1-B nước→đất **96,9 %**, c4B-A **99,6 %**.
2. **B2 giữ ngữ nghĩa vùng** (T9 0,1–3,1 %) và giữ trọn vùng bảo vệ (T1 1,00, T2 ≥ 0,98), nhưng **xoá/biến dạng vật mang dữ kiện nằm trong lớp "đất"** của mặt nạ: dải đê lấn biển (c2), cụm cây + lối mòn (c4B), bãi cạn (c1). Mặt nạ theo lớp renderer không đủ: "đất" chứa cả công trình đất (đê, đường, đường băng lấn biển) và vật nền (cây). Muốn chặn phải bảo vệ thêm các lớp này → vùng AI còn lại chỉ là nước/trời/đồng trống, tức lợi ích "ảnh thật" gần như không còn.
3. **Máy cho qua 1/10 (c2-B2d50) nhưng P loại** (đê bị cắt rời khỏi bờ) — lặp lại bài học NC-V2V c2-a: ngưỡng diện tích/cạnh bỏ sót một vật bị xoá. **T3 "cạnh mới" = 0,0–0,16 % ở mọi lượt** kể cả khi cả eo đất thành biển (mặt nước phẳng không sinh cạnh) → T3 chỉ bắt vật *thêm có cạnh*, không bắt *xoá* hay *đổi loại vùng*.
4. **Nhấp nháy (T5):** B2 1,43–1,51 × đối chứng (sát ngưỡng 1,5); B c1 2,74. Vùng ghép quanh vật giữ có **viền lam sáng** ở B (và nhẹ ở B2) — nền nguồn trong 2 px nới lộ ra cạnh nền AI tối hơn.
5. **Look:** chi tiết |Laplace| giảm ở mọi lượt (c2 47,4 → 8,7 A / 34,3 B2; c1 27,1 → 1,8 A / 18,6 B2); colorfulness giảm (c2 71 → 47 A / 63 B2). Không có "vân ảnh thật" như Omni.
6. **K-LAI-5 (d) đêm c1** (20 khung cuối): chói TB LAI/A 0,51 (B) · **0,72 (B2)** · 0,10 (A) — đều ≤ 1,5; nhưng % điểm > 1,5 × A + 2/255: B 0,14 % · **B2 1,70 %** (ngưỡng 0,5 % → **trượt**) · A 0,13 %. Ánh lửa B2 loang ra mặt nước.

## §4b. Kiểu lỗi "đổi loại vùng" (chỉ đạo 19:45 / 22:10) + T9 cho mọi biến thể

**Cơ chế:** độ sâu và cạnh chỉ mang *hình*. Một mặt đất phẳng và một mặt nước phẳng ở cùng khoảng cách cho ra cùng bản đồ độ sâu, và cả hai đều gần như không có cạnh. Khi vùng đó được giao cho AI vẽ (A: toàn khung; B: mọi vùng đất/nước/trời), mô hình tự chọn "cát" hay "nước" theo lệnh chữ và thói quen ảnh của nó. Đường bờ vì thế dời đi, eo đất ngập, vịnh thành sa mạc. Phép đo cũ T3 "cạnh mới" không thấy lỗi này: mặt nước phẳng mới không sinh cạnh nào (T3 = 0,0 % ở c4B-B dù đất→nước 26 %). T9 đo màu theo lớp của mặt nạ ID nên bắt được.

| Lượt | Đất→nước % | Nước→đất % | Giới hạn T9 (max(2, đc + 2)) đất→nước · nước→đất | T9 | P đọc: đổi loại vùng / xoá vật trong lớp đất |
|---|---|---|---|---|---|
| c2 đối chứng không AI | 0.66 | 1.06 | — | — | — |
| c4B đối chứng không AI | 0.01 | 0.52 | — | — | — |
| c1 đối chứng không AI | 7.41 | 0.38 | — | — | — |
| c2-A | 0.45 | 43.72 | 2.66 · 3.06 | **trượt** | đường bờ dời: vịnh nước giữa–phải khung thành bãi cát, biển lùi sang phải |
| c2-B | 1.03 | 19.35 | 2.66 · 3.06 | **trượt** | vịnh giữa khung (giữa đê chắn sóng và phố) bị vẽ thành bãi cát, đường bờ dời sang phải (máy: nước→đất 19,4 %) |
| c2-B2 | 1.5 | 1.91 | 2.66 · 3.06 | qua | giữ đúng đường bờ, vịnh, Rock, bãi cỏ, phố và tàu; **NHƯNG XOÁ dải đê/đường băng lấn biển màu xám chạy từ đầu đường băng ra giữa vịnh (lớp ID 'đất', nằm trong vùng AI được vẽ) — dữ kiện công trình đổi; xoá vệt sáng phản chiếu trên vịnh xa; mép vùng giữ quanh tàu còn viền lam nhẹ** |
| c2-B2d50 | 1.09 | 1.7 | 2.66 · 3.06 | qua | khử nhiễu 0,5: giữ bờ, vịnh, Rock, bãi cỏ, phố, tàu và PHẦN LỚN dải đê lấn biển; **nhưng đoạn gốc đê nối với bờ (≈ 1/4 chiều dài) bị XOÁ → đê thành dải nổi rời khỏi bờ (dữ kiện công trình đổi); vệt phản chiếu xa trên vịnh bị xoá; mặt nước/đá ít 'thật' hơn B2 0,6** |
| c4B-A | 0.0 | 99.57 | 2.01 · 2.52 | **trượt** | XOÁ hai dãy trại (lều chỉ còn vệt mờ), xoá tàu ngoài khơi, xoá cây và mảng cỏ xanh → sa mạc nâu cam đồng màu |
| c4B-B | 26.35 | 15.2 | 2.01 · 2.52 | **trượt** | eo đất cát giữa khung bị vẽ thành BIỂN/đầm nước xanh (dữ kiện địa lý đổi), chỉ còn hai dải trại (vùng giữ) như đảo |
| c4B-B2 | 0.07 | 3.12 | 2.01 · 2.52 | **trượt** | giữ đúng bờ biển, eo đất, Rock, hai dãy trại và tàu xa (không đổi loại vùng); **NHƯNG cụm cây (lớp đất/thực vật, vùng AI vẽ) biến thành các VÒNG RỖNG như bóng ma, lối mòn trắng uốn cong bị XOÁ, mảng cỏ xanh nhạt hẳn; vệt xanh sáng chạy dọc mép vùng giữ của dãy trại (đường ghép); cả khung mờ sương, chi tiết 20,3 → thấp hơn** |
| c1-A | 2.4 | 49.25 | 9.41 · 2.38 | **trượt** | ĐỔI THỜI ĐIỂM: khung đầu cửa sổ là ban ngày (nắng chiều) nhưng đầu ra tối đen như đêm từ khung 0 (lệnh 'Night, 1782' — lỗi lệnh của phiên, đã sửa cho c1-B2) |
| c1-B | 0.22 | 96.88 | 9.41 · 2.38 | **trượt** | cả mặt vịnh (vùng nước) bị vẽ thành bãi cát/sa mạc vàng ở khung ngày, nâu sẫm khi chiều (máy: nước→đất 96,9 %) |
| c1-B2 | 0.48 | 1.09 | 9.41 · 2.38 | qua | lệnh đã sửa ('chiều → đêm'): giữ đúng chuyển ngày → đêm, pin nổi + lửa + khói (vùng giữ), phố, công sự, cầu tàu; **NHƯNG XOÁ bãi cạn/đảo cát nhỏ trên mặt vịnh bên phải cầu tàu (lớp đất, vùng AI vẽ) và mép bãi phía phải; thêm bóng tối hình nêm cạnh cầu tàu; viền lam sáng bao quanh cầu tàu (đường ghép); sóng nước mất vân, mặt nước phẳng như kính** |

**Đọc:** A và B trượt T9 ở 6/6 lượt; B2 qua T9 ở c2 và c1. Khởi từ khung nguồn (B2) chặn được đổi loại vùng ở 2/3 cửa sổ (c4B-B2 vẫn trượt T9: nước→đất 3,1 %, sát giới hạn 2,5). Nhưng B2 sinh ra kiểu lỗi thứ hai: **xoá vật mang dữ kiện nằm trong lớp "đất"** (đê, cây, lối mòn, bãi cạn), mà T9 lẫn T3 đều không bắt được. Đúng như chỉ đạo 19:45 dự báo, mô hình cần một kênh **phân vùng** ("đây là nước"). Wan VACE không có kênh đó, nên tôi thay bằng màu nguồn (B2). Cosmos-Transfer2.5 có kênh phân vùng thật nhưng không tải được (§1b).

## §5. Chế độ C — nối c4A + c4B thành 20 s (`noi_c3.py`, `noi3.py`)

**DỪNG theo lệnh chủ dự án 20/10 22:30 (giờ chủ dự án) sau 2/7 cửa sổ** — không chờ hết 20 s. Đã có: khung 0–152 (6,4 s) của c4 = cửa sổ w0 (0–80) + w1 (72–152, 9 khung đầu là NGỮ CẢNH = khung đã ra của w0, mặt nạ 0, cũng là khung khởi), chuẩn hoá độ sâu cố định cho cả 20 s, chế độ B2. Hai cửa sổ ra đủ 81/81 khung, đã kéo về trước khi dừng pod. 5 cửa sổ còn lại và cổng `g-bo-chien-su-A` bị huỷ khỏi hàng đợi (không chạy).

| Số đo (`do/noi-c4C-B2.json`, 640×360, ΔE76) | Giá trị |
|---|---|
| ΔE tại biên khung 80 → 81 (đầu phần mới của w1) | **3,21** |
| ΔE nguồn cùng chỗ | 1,20 |
| Nền: trung vị ΔE khung kề trong cửa sổ · p95 | 0,905 · 1,33 |
| **Tỉ số nối ÷ nền** | **3,55** (> 3 → nối thấy được theo quy ước NC-V2V; Omni NC-V2V 28–65) |
| Bước nhảy chi tiết sau/trước | 0,975 |
| Ngữ cảnh 9 khung bị vẽ lại? | 0,000 (ghép giữ nguyên ngữ cảnh) |

- Nối tiếp bằng ngữ cảnh giảm bước nhảy ≈ 10–18 lần so với Omni sửa riêng từng đoạn, nhưng **vẫn thấy được** (3,55 × nền, ≈ 2,7 × khi trừ phần chuyển động nguồn 1,20/0,905). Một đường nối mỗi 3 s (cửa sổ 81 khung) ⇒ ≈ 250 đường nối/tập.
- Clip xem: `clip/c4C-B2-0-152-noi81.mp4` (960×540, 0,8 MB; nối ở giây 3,4).
- Không có số đo cho đường nối giây 10 (c4A ↔ c4B) vì dừng trước cửa sổ w3.

## §6. Chấm mù (bước 4) — `cham3.py`, `cham-mu/`

**Giao thức NC-GPU nguyên văn** (PROMPT + 3 vai RATERS của `channel-k2/k2v2-mau/blind_v2.py`, `claude -p` ghim **claude-sonnet-5-5**, chỉ công cụ Read, thư mục tạm chỉ chứa ảnh, nhãn hoán vị hạt 20102026), mỗi bộ chấm ở **640×360 và 320×180**.
- **Bộ cổng** (cùng điểm máy NC-CPU/NC-GPU): V7B · A (NC-CPU) · Cycles GPU 256 spp (NC-GPU) · **V2V3-B2** (khung giữa của cửa sổ 17 khung). Không có "bản đạt" (0/10) → dùng B2, chế độ giữ dữ kiện tốt nhất.
- **Bộ clip** (khung 120 của clip NC-V2V = khung 40 của cửa sổ): V7B · V2V3-A · V2V3-B2 · **Omni-a** (NC-V2V, cùng khung — **có vật bịa: quân, lửa trại, tàu ở c4B; lửa phố ở c1; không phải ứng viên**, chỉ để đo khoảng cách "độ thật").

| Cỡ | Bộ | Bản | craft | độ thật | ai_look | toy_like | hạng 1 | hạng TB |
|---|---|---|---|---|---|---|---|---|
| 640 | cổng (3 cảnh × 3 vai) | Cycles GPU | **6,56** | **5,89** | 3,67 | 4,56 | **6/9** | **1,67** |
| 640 | cổng | A (NC-CPU) | 6,33 | 5,55 | 3,67 | 4,78 | 3/9 | 1,78 |
| 640 | cổng | V7B | 6,00 | 5,00 | 3,89 | 5,44 | 0/9 | 2,56 |
| 640 | cổng | **V2V3-B2** | 4,00 | **3,11** | 4,89 | 6,33 | **0/9** | **4,00** |
| 640 | clip (3 cảnh × 3 vai) | Omni-a (có vật bịa) | 7,67 | **7,67** | 5,22 | 2,22 | 9/9 | 1,00 |
| 640 | clip | V7B | 5,00 | 3,44 | 3,89 | 6,11 | 0/9 | 2,22 |
| 640 | clip | **V2V3-B2** | 4,22 | **3,11** | 3,78 | 6,22 | 0/9 | 3,11 |
| 640 | clip | V2V3-A | 3,33 | 3,56 | 4,45 | 3,44 | 0/9 | 3,67 |
| 320 | cổng | Cycles GPU | 5,44 | 4,89 | 4,44 | 4,45 | 4/9 | 2,11 |
| 320 | cổng | A (NC-CPU) | 6,00 | 5,33 | 4,11 | 4,11 | 3/9 | 1,67 |
| 320 | cổng | V7B | 5,67 | 5,00 | 4,22 | 4,55 | 2/9 | 2,22 |
| 320 | cổng | **V2V3-B2** | 4,00 | 3,22 | 4,78 | 5,67 | 0/9 | **4,00** |
| 320 | clip | Omni-a (có vật bịa) | 7,11 | 6,78 | 4,44 | 3,11 | 9/9 | 1,00 |
| 320 | clip | V7B | 4,78 | 3,89 | 4,78 | 5,22 | 0/9 | 2,11 |
| 320 | clip | **V2V3-B2** | 4,22 | 3,44 | 4,78 | 5,67 | 0/9 | 3,33 |
| 320 | clip | V2V3-A | 3,22 | 3,22 | 4,22 | 3,22 | 0/9 | 3,56 |

- V2V3-B2 **cuối ở cả 3 cổng × 2 cỡ** (hạng TB 4,0/4). Cờ người chấm: `washed_out`, `flat_slide_look`, `toy_look` ("The ground is a beige or tan colour field with no texture", "monotone yellow-olive blanket that looks like felt").
- Khoảng cách "độ thật" tới Omni: **−4,6 điểm** (3,11 so với 7,67 @640) — **lớn hơn** khoảng cách V7B ↔ Omni (−4,2). Tức AI bám cấu trúc **không thu hẹp** mà nới rộng khoảng cách.
- Chấm mù không thay kiểm dữ kiện (K-LAI-3 e); ở đây hai phép đo cùng chiều: V2V3 vừa đổi dữ kiện vừa không đẹp hơn.

## §7. Giờ GPU bật/tắt + tiền thật (`gio-gpu.jsonl`)

Sổ nguyên văn `gio-gpu.jsonl` (UTC). Giá đọc qua API (GraphQL `gpuTypes`) 20/10 ≈ 10:20: RTX 5090 SECURE $1,19 (kho Low), COMMUNITY $0,69 (hết kho); RTX PRO 4500 32 GB $0,72 (Medium); L40S $1,09; A40 $0,59 (Ampere, không fp8). Chọn 5090 vì nhanh nhất trên 32 GB.

| Nhãn | Pod | Bật → tắt | Giờ | Giá × giờ | Số dư trước → sau | Việc |
|---|---|---|---|---|---|---|
| v1 | `ezts7n6h2htm8y` | 10:23:26 → 10:37:26 | 0,233 h | $0,278 | 14,016 → 13,788 | cài (184 s), thử 17 khung (7,3 s/bước); tắt để khỏi chờ nguồn CPU |
| v2 | `zktbumbgeuej8t` | 10:49:02 → 15:35:40 | 4,777 h | $5,685 | 13,733 → 7,966 | 10 lượt 81 khung, 8 lượt cổng 17 khung, chế độ C 2 cửa sổ |
| **Tổng** | 2 pod RTX 5090 SECURE, một pod tại một thời điểm | | **5,01 h** | **$5,96** | **14,016 → 7,966 = $6,05 thật** | |

- Mọi pod đã XOÁ (HTTP 204); `GET rest.runpod.io/v1/pods` → `[]`, `currentSpendPerHr` 0 (15:36 UTC).
- Trạng thái pod ghi đĩa (`/var/tmp/cine-out/v2v3/pod.json`), kiểm đủ khung (`keo3.py`, SHA từng tệp) trước khi tắt (NG-D6).
- Sau khi tắt, số dư đọc lại 15:37 UTC = **$22,966** = 7,966 + 15,000 → **có khoản nạp $15 vào tài khoản** (không do phiên này; đề nghị chủ dự án xác nhận).
- Lãng phí do vận hành: pod v2 chờ nguồn CPU ≈ 10 phút đầu và các job xếp hàng song song làm thứ tự ưu tiên xen kẽ (không tốn thêm giờ GPU).

## §8. Ước cả tập 745 s (bước 5) — mọi số **(ước)** từ số đo phiên này

| Khoản | Cách tính | Kết quả |
|---|---|---|
| Số cửa sổ | 745 s × 24 = 17 880 khung; cửa sổ 81 khung, bước 72 (9 khung ngữ cảnh) → 249; + ≈ 50 shot mỗi shot một chuỗi riêng (cửa sổ đầu không có ngữ cảnh, cửa sổ cuối chồng thừa) | **≈ 300 cửa sổ** |
| Giờ GPU 1 lượt (B2, 720p) | 300 × 973 s (đo) | **≈ 81 h ≈ $97** ở $1,19/h (RTX 5090) |
| 1080p | token × 2,25, chú ý ≈ bậc 2 → ≈ × 2,5–3 (chưa đo) | **≈ 200–240 h ≈ $240–290** |
| Tỉ lệ làm lại thật | P đọc 0/10 đạt (máy 1/10). Quy tắc ba: cận trên 95 % tỉ lệ đạt ≈ 3/10 = 30 % | **≥ 3,3 lượt/cửa sổ ⇒ ≥ 270 h, ≥ $320 (720p)**, và vì lỗi mang tính cơ chế (vùng AI vẽ được = vùng có thể xoá dữ kiện) **không có cơ sở để tin sẽ hội tụ** |
| Đường nối | xem §5 | nối tiếp có ngữ cảnh: **3,55 × nền mỗi 3,4 s** (đo 1 biên) ⇒ ≈ 250 đường nối thấy được/tập; phải hoà/che hoặc cửa sổ dài hơn (chưa đo) |
| CPU nguồn + điều khiển | dung3.js ≈ 12 s/khung/làn × 17 880 / 2 làn | **≈ 30 h CPU** (mức nháp spp 1; nguồn sản xuất V6 vẫn phải dựng vì AI cần nguồn của ta) |
| Người đọc tờ so | 300 cửa sổ × ≈ 2 phút | **≈ 10 h P/tập** (máy không đủ — §4 điểm 3) |
| Công sức đưa vào G0 (sau A/Cycles) | đã có: độ sâu từ renderer, mặt nạ ID + mái, điều khiển, ComfyUI/pod, ghép K-LAI-4, cửa sổ nối, bộ đo T7–T9. Còn: gắn vào `episode.yaml` theo shot, lớp bảo vệ "đất công trình" (đê/đường/cây), xử lý viền ghép, lưu cảnh trên Network Volume | **≈ 2–3 phiên** + 10 h P/tập lặp lại |

**Tác động luật kênh:**
- **BIBLE §12.3** "KHÔNG: … video AI" → phải sửa luật. **§12.2** (bỏ AI ra mà dữ kiện đổi thì không dùng): **trượt 10/10**.
- **K-LAI-1** (≤ 20 % thời lượng): tối đa ≈ 149 s/745 s. **K-LAI-4** (vùng bảo vệ \|LAI − A\| < 1/255): B/B2 đạt **0,000** trên PNG trước nén (ghép lại nguồn); A trượt (toàn khung). **K-LAI-5**: đêm c1-B2 trượt (d) 1,70 % > 0,5 %. **K-LAI-B** (bão hoà ≤ 0,40, cảnh báo): c4B-B2 0,59, c1-B2 0,65 → cảnh báo. **K-LAI-6**: sổ đủ trường (job JSON + SHA tệp vào/ra).
- **Nhãn:** đầu ra Wan **không** có C2PA/SynthID → kênh phải tự khai "altered or synthetic content" trên YouTube (kiểm trang chính sách lúc đăng) và sửa thẻ "How this film was made"; có thể tự gắn C2PA (chưa thử).
- **Rủi ro chính:** xoá/bịa dữ kiện địa lý và công trình trong phim lịch sử, mà phép đo máy hiện có bỏ sót (T3 = 0 khi cả eo đất thành biển).

## §9. Chi phí

| Khoản | Mốc / chặn | Thật |
|---|---|---|
| RunPod GPU | chặn cứng $12 (sàn số dư $2,5) | **$6,05 thật** (số dư 14,016 → 7,966; 5,01 h; giá × giờ $5,96) — dưới chặn $12; không chạm sàn $2,5 |
| Claude (chấm mù 36 lượt `claude -p` Sonnet 5.5) | mốc $8 · chặn > $25 | **$2,046** (`cham-mu/cost.jsonl`). Token phiên chính không đo được từ trong container. |
| OpenAI | $2 | **$0** (chấm mù theo giao thức NC-GPU, chỉ Claude) |
| Gemini / ElevenLabs / YouTube | 0 | 0 / 0 / 0 |
| Giờ máy CPU (4 vCPU) | 8 h | **≈ 2,6 h** đồng hồ: bộ đệm 0,2 · dựng 3 cửa sổ + 3 cổng 0,7 · c4 đủ 20 s 0,75 · đo/tờ so/lưới 0,4 · chế độ C ghép 0,3 · gỡ lỗi 0,2 |
| Đĩa ngoài git | — | `/var/tmp/cine-out/v2v3/` ≈ 4 GB (nguồn, điều khiển, đầu ra PNG, video đo) |

## §10. Chỉ số trong ±5 % quanh ngưỡng (luật cứng)

| Lượt | Chỉ số | Giá trị | Lệch so ngưỡng |
|---|---|---|---|
| c2-B2 | T5 nhấp nháy ÷ đối chứng | 1,51 | +0,7 % trên 1,5 (trượt sát) |
| c2-B2d50 | T5 | 1,47 | −2,0 % (qua sát) |
| c4B-B2 | T5 | 1,43 | −4,7 % (qua sát) |
| c2-A | T2 F1 nhà | 0,860 | +1,2 % trên 0,85 |
| c1-B2 | T6 lệch khung | −1,0 | đúng mép \|k\| ≤ 1 |
| RunPod | tiền thật so chặn $12 | $6,05 / $12 (−50 %) | — |

- Dải T6 tỉ lệ 0,97–1,03 hẹp: mọi giá trị ≈ 1,00 đều trong ±5 % của cả hai mép (như NC-V2V); không nêu từng dòng.
- Không chỉ số nào ở trên làm đổi kết luận: mọi lượt nêu tên đều bị P loại vì dữ kiện đổi.
- Không thêm phần tử nào để vượt ngưỡng.

## §11. Quyết định đề xuất

| # | Đề xuất | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|---|
| **V2V3-D1** | **Không dùng video→video AI trên hình** (cả loại bám cấu trúc, mô hình mở); giữ §12.3; **đóng hướng V2V** (NC-V2V + NC-V2V3) | Giữ §12.2; không $100–320+/tập; không 10 h đọc tờ so/tập; không nhãn AI toàn phim | Mất hy vọng "ảnh thật kiểu Omni" bằng AI | Đường chính vẫn là A + Cycles GPU (NG-D1/G0) | Đối thủ dùng AI vẫn "thật" hơn → bù bằng NG-D5 (khói/lửa thể tích, nướng GPU, vân) |
| V2V3-D2 | Đưa **T9 "đổi loại vùng"** + **phép "vật bị xoá"** (hồi cạnh nguồn trong lớp đất/công trình đất) vào bộ đo cho mọi bước AI sinh điểm ảnh (bổ sung V2V-D4) | Bắt được lỗi mà T3 bỏ sót (eo đất → biển, T3 = 0) | Phiên K phải duyệt luật mới | `checks/` (phiên K) | Vẫn cần P đọc tờ so |
| V2V3-D3 | Giữ `depth.js` (độ sâu từ chính renderer) + lượt mái phố làm **công cụ nội bộ** (tạo bản đồ độ sâu đúng cho sương khí quyển/DOF hậu kỳ của A, so look) | Có sẵn, đúng vật lý, không AI | Thêm ≈ 1,5 s/khung | A/Cycles hậu kỳ | — |
| V2V3-D4 | Nếu chủ dự án vẫn muốn thử mô hình khác: **Cosmos-Transfer2.5-2B** cần chủ dự án tự chấp nhận NVIDIA Open Model License trên tài khoản HF và cấp token đọc *riêng cho pod* (phải đổi luật "không khoá lên pod") — hoặc **LTX-2.x IC-LoRA** (không gated); ngân sách ≥ $8, cùng bộ đo T1–T9 + P đọc | Đóng nốt câu hỏi "mô hình khác" | Cơ chế lỗi (vùng AI vẽ được = vùng có thể xoá dữ kiện) không phụ thuộc mô hình → khó đổi kết luận | Chỉ nghiên cứu | Tốn tiền cho câu hỏi gần như đã có đáp án |
| V2V3-D5 | Ghi BAI-HOC (phiên P): (a) độ sâu không mang ngữ nghĩa vùng — inpaint theo độ sâu biến đất ↔ nước; (b) máy qua mà P loại lần thứ 2 (NC-V2V c2-a, NC-V2V3 c2-B2d50) → không bao giờ nhận AI chỉ bằng máy; (c) khi lượt phụ ẩn/hiện vật: đọc trạng thái TRƯỚC khi ẩn; (d) `pgrep/pkill`/`grep` trên danh sách tiến trình khớp cả lệnh của chính mình (gặp lại 2 lần, BÀI HỌC #24); (e) tải lên pod theo tar (16 MB/s) thay vì từng PNG (0,2–0,7 MB/s) | Tránh lặp lỗi | — | `reports/m3/BAI-HOC-LL.md` | — |

## §12. Việc chờ chủ dự án

1. **Xem** `reports/nc-v2v3/clip/luoi-c4B.mp4`, `luoi-c2.mp4`, `luoi-c1.mp4` và `to-so/to-so-c4B-B.png`, `to-so/to-so-c2-B2.png`, `to-so/zoom-c2-B2-de.jpg`.
2. **Quyết V2V3-D1…D5.** Đề xuất chính: **D1** (không dùng, đóng hướng V2V) + D2 (bộ đo) + D5 (bài học).
3. **Cosmos-Transfer2.5-2B:** không cài được vì trọng số gated (401) — nếu muốn thử, quyết D4 (chấp nhận giấy phép NVIDIA trên HF + cho phép token đọc trên pod). **RunPod:** số dư còn $22,97 (gồm khoản nạp $15 lúc ≈ 15:37 UTC); mọi pod đã XOÁ. Nạp thêm chỉ khi duyệt G0 (NG-D1) hoặc D4.
4. **Phiên P:** ghi RIGHTS phần công cụ (Wan2.2-VACE-Fun Apache-2.0, ComfyUI GPL-3.0 công cụ, không lên hình vì D1), BAI-HOC theo D5, AUTHORSHIP: không có quyết định sáng tạo mới lên hình. **Phiên K:** xem D2.

## Tệp

| Tệp | Nội dung |
|---|---|
| `design/k2v/v2v3/` | `depth.js` (độ sâu từ renderer + lượt mái phố) · `mk_page3.py` · `dung3.js` (một lần dựng: màu + sâu + ID + mái) · `clips` dùng `../v2v/clips.py` · `gates3.py` · `ctrl3.py` (điều khiển, mặt nạ, alpha) · `comfy_node/` (nút PNG) · `wf_vace.py` (đồ thị ComfyUI) · `mk_job3.py` · `prompts3.json` · `pod3.py` (gọi pod.py NC-GPU, chặn tiền) · `pod_setup3.sh` · `pod_batch.sh` · `models.json` (repo/bản/SHA) · `keo3.py` (kéo + kiểm đủ khung) · `ghep3.py` (ghép vùng giữ, đối chứng) · `do3.sh`, `do_them3.py` (T7–T9), `danh_gia3.py` · `noi_c3.py`, `noi3.py` (chế độ C) · `cham3.py`, `cham-cfg.json` · `luoi3.py` · `chay_*.sh` (lệnh đã chạy) |
| `reports/nc-v2v3/` | `NC-V2V3-BAO-CAO.md` · `danh-gia.{md,json}` · `p_doc.json` · `do/` · `to-so/` (PNG + zoom) · `clip/` (≤ 5 MB) · `cham-mu/` · `giay-phep/` · `gio-gpu.jsonl` · `SHA256-*.txt` · `CHECKPOINT.md` |
