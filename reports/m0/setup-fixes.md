# M0 — Sửa môi trường trong phiên (26/09/2026)

Máy: Ubuntu 24.04.4, 4 vCPU Intel Xeon 2,10 GHz, 15 GB RAM (16 095 MB), không swap, không GPU. Đĩa trống đầu phiên 28 GB (sau khi cài ACE-Step + trọng số còn ~11 GB).

## 1. Blender bpy — FAIL → PASS

**Lỗi gốc** (`/var/log/cine-setup.log`, lặp 3 lần rồi `FAIL`):
```
Traceback (most recent call last):
  File "/usr/bin/add-apt-repository", line 3, in <module>
    import apt_pkg
ModuleNotFoundError: No module named 'apt_pkg'
FAIL: add-apt-repository -y ppa:deadsnakes/ppa
== RESULT apt=1 py=0 playwright=0 bpy=1 (0 = OK)
```
**Nguyên nhân (đã kiểm):** `/usr/bin/python3` → `/etc/alternatives/python3` → `/usr/bin/python3.11`. `add-apt-repository` có shebang `#!/usr/bin/python3` nhưng `apt_pkg` chỉ có bản cho Python 3.12 (`apt_pkg.cpython-312-x86_64-linux-gnu.so`). Không phải lỗi mạng hay PPA.
Ảnh VM **đã có sẵn** nguồn `deadsnakes-ubuntu-ppa-noble.sources` và gói `python3.13 3.13.12-1+noble1`, `python3.13-venv`. Nhánh bpy trong setup cũ bị bỏ qua chỉ vì `[ $R1 -eq 0 ]` (apt báo lỗi ở bước PPA).

**Lệnh chạy được trong phiên** (28 s):
```bash
python3.13 -m venv /opt/bpy && /opt/bpy/bin/pip install -q bpy
/opt/bpy/bin/python -c "import bpy; print(bpy.app.version_string)"   # 5.2.2 LTS
```
Không cần PPA. Nếu một ảnh VM sau này thiếu python3.13, lệnh thêm PPA đúng là:
```bash
/usr/bin/python3.12 /usr/bin/add-apt-repository -y ppa:deadsnakes/ppa   # đã thử: chạy được (--help), có apt_pkg
```
Không cần thử `uv python install 3.13` hay bản Blender Linux chính thức vì cách trên đã chạy.

**Render không GPU:** Workbench và EEVEE đều render được qua EGL phần mềm (Mesa). Log in 3 dòng `EGL Error (0x3009): EGL_BAD_MATCH` mỗi lần khởi động nhưng ảnh ra đúng (đã kiểm giá trị điểm ảnh). Cảnh mặc định 640×360: EEVEE 37,7 s (gồm biên dịch shader), Workbench 0,74 s.

## 2. Playwright / Chromium — PASS, không cần cài lại

| Gói | Phiên bản | Chromium cần | Có trong /opt/pw-browsers |
|---|---|---|---|
| `/opt/pw/node_modules/playwright` (setup cài) | 1.63.0 | chromium-1243 (153.0.8010.12) | có |
| `playwright` toàn cục của VM | 1.56.1 | chromium-1194 | có |

Đã chạy thử: Chromium 153.0.8010.12 khởi động; WebGL2 chạy trên `ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero)))` với cờ `--use-angle=swiftshader --enable-unsafe-swiftshader`. Không lệch phiên bản nên **không** chạy `npx playwright install`.
Quy ước: script luôn `require('/opt/pw/node_modules/playwright')` để không lẫn với bản toàn cục.

## 3. Thay đổi trong `scripts/env/setup.sh`
1. Bỏ gọi `add-apt-repository` vô điều kiện. Chỉ cài python3.13 khi thiếu; chỉ thêm PPA khi thiếu nguồn deadsnakes, và gọi qua `/usr/bin/python3.12`.
2. Nhánh bpy chạy khi có `python3.13`, không phụ thuộc mã thoát của cả khối apt.
3. Thêm `psutil` vào `/opt/cine` (dùng cho `reports/m0/peakmem.py` đo RAM đỉnh).

Đã chạy lại **toàn bộ** setup.sh mới trong phiên: `RESULT apt=0 py=0 playwright=0 bpy=0`, 6 s (các gói đã có sẵn nên đây chỉ chứng minh logic và cú pháp, không đo thời gian cài mới). Log: `reports/m0/setup-rerun.log`.
`verify.sh` trước: 9 PASS / 1 FAIL (bpy). Sau: **10 PASS / 0 FAIL** (`reports/m0/verify-before.txt`, `verify-after.txt`).

## 4. ACE-Step (cài trong phiên, KHÔNG đưa vào setup)
```bash
git clone --depth 1 https://github.com/ace-step/ACE-Step-1.5 /opt/acestep-src/ACE-Step-1.5   # commit ca1e85f, 29/08/2026
uv venv -p /usr/bin/python3.12 /opt/acestep                                                     # repo yêu cầu Python 3.11–3.12
VIRTUAL_ENV=/opt/acestep uv pip install "transformers>=4.51.0,<4.58.0" "diffusers>=0.37.0" matplotlib scipy soundfile loguru \
  einops "accelerate>=1.12.0" diskcache "numba>=0.63.1" "vector-quantize-pytorch>=1.27.15" "torchao>=0.16.0,<0.17.0" toml modelscope \
  "peft>=0.18.0" "safetensors==0.7.0" xxhash typer-slim pytorch-wavelets pywavelets huggingface_hub psutil fastapi uvicorn \
  python-multipart "gradio==6.2.0" "torchcodec>=0.9.1"
VIRTUAL_ENV=/opt/acestep uv pip install "torch==2.14.0" torchaudio
VIRTUAL_ENV=/opt/acestep uv pip install --no-deps -e /opt/acestep-src/ACE-Step-1.5
/opt/acestep/bin/python -c "from huggingface_hub import snapshot_download; snapshot_download('ACE-Step/Ace-Step1.5', local_dir='/opt/acestep-src/ACE-Step-1.5/checkpoints', max_workers=8)"   # 10,1 GB, 60 s
```
**Lỗi nguyên văn khi cài torch bản CPU:**
```
error: Failed to fetch: `https://download.pytorch.org/whl/cpu/torch/`
  Caused by: tunnel error: unsuccessful
[agent-proxy] download.pytorch.org:443 — connect_rejected
```
`download.pytorch.org` không nằm trong allowlist, nên torch được kéo từ PyPI: **2.14.0+cu130 (bản CUDA, venv 6,0 GB)**, chạy CPU được nhưng tốn đĩa gấp nhiều lần bản CPU; torchaudio PyPI chỉ có 2.11.0 cho cặp này. Repo ghim torch 2.10.0 → đang chạy lệch phiên bản (xem kết quả bước 4 trong báo cáo).
Đề xuất (chủ dự án quyết): thêm `download.pytorch.org` vào allowlist nếu chọn ACE-Step.
