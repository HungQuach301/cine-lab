# RUNBOOK MÔI TRƯỜNG — máy, mạng, nguồn tư liệu, giờ máy

> Phiên Nền tảng soạn ngày 15/10/2026, theo lệnh chủ dự án ngày 13/10. Mỗi dòng có nguồn: chạy thật trong phiên Nền tảng (ghi "đo 15/10") hoặc báo cáo cũ (ghi đường dẫn). Sai hoặc đổi thì sửa dòng đó và ghi ngày.
> Tài liệu liên quan: `docs/cine-lab/SETUP-MOI-TRUONG.md` (cài môi trường gốc), `docs/SESSION-CHARTER.md`, `docs/FILE-ZONES.md`.

## 1. Máy (môi trường cloud `cine-lab-av`)
| Mục | Giá trị | Nguồn |
|---|---|---|
| CPU / RAM / đĩa | 4 vCPU Xeon 2,8 GHz (AVX-512), 15 GB RAM, không swap; đĩa ghi được ≈ 17 GB đầu phiên (hạn mức của phiên, `df` không phản ánh đúng) | `scripts/env/verify.sh`, `nproc`, đo 15/10 |
| GPU | **Không có.** Không có `/dev/dri`, `/dev/nvidia*`, `nvidia-smi` | đo 15/10 |
| WebGL trong Chromium headless | `ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero)))` — dựng phần mềm trên CPU, kể cả khi bật `--enable-gpu --ignore-gpu-blocklist --use-angle=vulkan` | đo 15/10 (script dò WebGL trong báo cáo `reports/NEN-TANG-BAO-CAO.md` §1) |
| Python | chính `/opt/cine/bin/python` (3.13); Blender `/opt/bpy/bin/python`; tách nền: venv `/var/tmp/cine-out/segvenv` (tạo lại mỗi container) | CLAUDE.md, `design/k2v/README.md` |
| Container | tạm thời: mọi thứ ngoài git mất khi container bị thu hồi (cache relief, footage, trọng số, `/var/tmp/cine-out`) | — |

**Gói còn thiếu trong môi trường (phát hiện 15/10, cài tay mỗi container mới cho tới khi `scripts/env` được sửa):**
- `/opt/cine/bin/python -m pip install tifffile pyshp` — `scripts/k2/relief_build.py` cần (ghép DEM GeoTIFF, đọc shapefile Natural Earth). Thiếu thì dựng nền relief lỗi `ModuleNotFoundError`.
- `(cd design/cong3/shared && npm ci)` và `(cd design/k2v && npm ci)` — three.js 0.180 và dữ liệu bản đồ. `verify.sh` báo FAIL three.js cho tới khi chạy.

## 2. Dựng lại cache ngoài git (`K2V_CACHE`, mặc định `/var/tmp/cine-out/k2v-cache`)
| Tài sản | Lệnh | Giờ đo | Kiểm |
|---|---|---|---|
| Nền relief `erie` | `relief_build.py build --name erie --bbox -82,39,-71,46 --ppd 600 --mesh 8 --routes 'erie=Erie Canal\|Oneida River - Erie Canal;hudson=Hudson;mohawk=Mohawk'` | tải DEM 3DEP ≈ 3,2 GB ≈ 7 phút + tính 147 s (đo 15/10) | 4/4 SHA khớp `channel-k2/k2v2-mau/relief-erie-meta.json` (thiếu `mohawk` thì `routes.json` lệch) |
| Blue Marble, ảnh LoC, trang PDF | `scripts/k2/k2v_assets.py fetch all && … bm-global && … bm-crop …` | — | SHA trong `scripts/k2/k2v-assets.sha.json` |
| Ảnh hàng không NAIP | `scripts/k2/aerial.py` (venv segvenv) | — | SHA trong `channel-k2/k2v4-mau/aerial-<tên>-meta.json` |
| Trọng số tách nền | `scripts/k2/cutout.py try` tự tải (≈ 2,3 GB) vào `$K2V_CACHE/models` | ≈ 5 phút/ảnh khi thử 4 mô hình | SHA trong `design/k2v/cutouts/<id>.json`; **không commit trọng số** |

## 3. Mạng
| Đích | Trạng thái | Cách làm |
|---|---|---|
| `api.elevenlabs.io` | qua proxy, khoá được gắn sẵn | không commit khoá; mọi lệnh thử nghiệm phải chạy khi cache lời đủ (xem §5) |
| PyPI, Hugging Face, npm | được | — |
| `bls.gov` | **403** (đo 15/10) | đọc qua FRASER; hoặc liệt kê bảng/URL cho Claude Cowork, đánh dấu CHỜ XÁC MINH (BAI-HOC-LL #11, #12) |
| `web.archive.org` (Wayback) | **hết giờ** (đo 15/10) | không dựa vào Wayback |
| Freesound API | **403** (đo 15/10; `verify.sh` báo "tuỳ chọn") | dùng nguồn SFX khác có giấy phép rõ |
| GitHub LFS | đọc được qua API batch (href S3 ký sẵn, 1 giờ) | lấy **một khung** master không cần tải cả tệp: `ffmpeg -ss <giây> -i "<href>" -frames:v 1 x.png` ≈ 1,4 s/khung (đo 15/10; `scripts/common/golden.py`) |
| Máy chặn proxy để thử offline | `HTTPS_PROXY=http://127.0.0.1:9` | chặn mọi gọi mạng của một lệnh (golden.py dùng để `prep` không thể gọi ElevenLabs) |

**User-Agent:** chỉ tên dự án, **không email**: `cine-lab/1.0 (channel research)` (`aerial.py`, `stock.py`) hoặc `Mozilla/5.0 (cine-lab research; https://github.com/HungQuach301/cine-lab)` (`k2v_assets.py`). Không đưa email chủ dự án vào UA, URL hay payload.

## 4. Nguồn tư liệu — cách đọc quyền và tải
| Nguồn | Cách làm đúng | Bẫy đã gặp |
|---|---|---|
| **Library of Congress** | Quyền: `https://www.loc.gov/item/<id>/?fo=json` → trường `item.rights_advisory` (vd "No known restrictions on publication.", đo 15/10). Tải bản gốc `tile.loc.gov/storage-services/master/…u.tif`. **Giãn ≥ 30 s giữa hai lượt** JSON; dừng ngay khi 429 | G1b T1: 429 sau 7/19 ảnh khi giãn ngắn; G2 T1: 12/12 với giãn 31 s, 1 lượt, không 429 (`AUTHORSHIP`, commit `3d74d87`) |
| **Wikimedia Commons** | API: `commons.wikimedia.org/w/api.php?action=query&titles=File:<tên>&prop=imageinfo&iiprop=extmetadata&format=json` → `LicenseShortName`, `UsageTerms`, `Artist`. Kiểm **từng tệp**; ảnh LoC trên Commons thì đối chiếu bản LoC gốc | — |
| **The Met** | Trang web `metmuseum.org/art/collection/search/<id>` trả **429** cho máy (đo 15/10). Dùng **Open Access API** `collectionapi.metmuseum.org/public/collection/v1/objects/<id>` → `isPublicDomain: true`, `primaryImage` (đo 15/10: 200, 10991 true) | V4: không đối chiếu trang được → ghi "chủ dự án đối chiếu bằng mắt" (`K2V4-BAO-CAO.md` §11.6) |
| **Prelinger / archive.org** | `archive.org/metadata/<id>/metadata` → `licenseurl` (vd `http://creativecommons.org/licenses/publicdomain/`), `collection` chứa `prelinger` (đo 15/10). Lưu trang giấy phép vào `licenses/<clip>.txt` | Newsreel PD hay bị bên tổng hợp khai Content ID → rủi ro TRUNG BÌNH; bản gốc 368×480 phóng 1080p làm điểm tay nghề tụt (P6 6,0) |
| **DVIDS** | Trang `dvidshub.net/video/<id>` (301 → trang có slug) ghi "PUBLIC DOMAIN"; không dùng huy hiệu/logo đơn vị | **Chưa nằm trong danh sách nguồn cho phép của K (Q32)** — chờ chủ dự án duyệt (`K2V4-BAO-CAO.md` §11.2) |
| **NAIP** (USDA FSA qua USGS) | Dịch vụ `imagery.nationalmap.gov/arcgis/rest/services/USGSNAIPPlus/ImageServer`. Dịch vụ **trộn NAIP với ảnh HRO của bang**: gọi `identify` ở **từng tầng** để xác nhận năm/nguồn là NAIP. Ảnh xuất **≤ 3 600 px** mỗi chiều | 4 000 px trả 502; 3 600 px chạy (`K2V4-BAO-CAO.md` §10) |
| **Pexels / Pixabay** | `scripts/k2/stock.py` (cache tìm 24 giờ, tải qua CDN, SHA, dòng `SOURCES-FOOTAGE.csv`) | Không có clip kênh Erie — tìm theo nội dung câu, không lấp chỗ trống |
| **FRASER** | ưu tiên cho tài liệu BLS cũ; không đoán URL quá 1 lần | BAI-HOC-LL #12 |
| Mọi nguồn | mỗi clip/ảnh ngoài: dòng trong sổ `SOURCES-FOOTAGE.csv` + tệp `licenses/<clip_id viết thường>.txt` (trang giấy phép lưu nguyên) + SHA-256 + dòng `RIGHTS.md`. `tools/preflight.sh` chặn khi thiếu tệp giấy phép | Sổ T1 ghi quyền trong cột, không có thư mục `licenses/` → preflight `--all` báo 30 dòng (tập đã phát hành, ghi nhận, không sửa) |

## 5. Giọng ElevenLabs
- **Số viết bằng chữ trong lời gửi TTS** (vd "four thousand four hundred forty", không "4,440"): ElevenLabs đọc sai số có dấu phẩy nghìn (commit `96da659`, T1 G2; ASR small.en + medium.en xác nhận). Năm đọc bằng chữ được ASR chấp nhận (BAI-HOC-LL #19).
- Cache lời theo băm văn bản (`vo/<id>-<đoạn>.{mp3,txt,align.json}`). **Commit cả `align.json`**: Steel thiếu `align.json` trong `channel-k2/k2g-ep01/vo/`, bản duy nhất nằm ở `checks/ll/fixtures/k2g01/vo/` (phát hiện khi dựng khung vàng 15/10). Thiếu thì `prep` sẽ thu lại (tốn ký tự).
- Bộ đếm tài khoản tính ≈ 0,44–0,8 ký tự/ký tự gửi (T1: 30 360 gửi; Steel: 17 009 gửi → +13 718 bộ đếm). Ghi cả hai vào `COST-LEDGER.csv`.

## 6. Git, LFS, media
- LFS **chỉ** cho gói phát hành ở nhánh `release-*` (`tools/lfs-allow.txt`: master, Short, 3 phần xem). Mỗi tệp LFS tốn hạn mức lưu trữ và băng thông GitHub của chủ dự án.
- Media trung gian, footage, TIFF gốc, trọng số, cuộn 1080p: ngoài git, chỉ ghi SHA. Tệp commit > 5 MB phải là con trỏ LFS trong vùng cho phép (preflight chặn). Repo còn 136 tệp > 5 MB cũ ngoài LFS (`design/cong3–5`, `reports/m0–m3`, `assets/`, `screening/`) — có trước luật, ghi nhận.
- Kiểm trước khi đẩy: `bash tools/preflight.sh --range origin/main..HEAD`.

## 7. Giờ render đo được (dùng để ước G1)
| Việc | Số đo | Nguồn |
|---|---|---|
| Relief 1080p SPP2, 1 tiến trình, 24 khung liền (đoạn H cuộn K2V4) | **1,98 s/khung** | đo 15/10 |
| … cùng khung, 4 tiến trình song song | 6,37 s/khung mỗi tiến trình → **thông lượng 1,65 s/khung** (chỉ nhanh 1,2× so với 1 tiến trình) | đo 15/10 |
| … chỉ nền địa hình (bỏ vùng nổi, tuyến, vòng, nhãn) | 1,91 s/khung (nền = 96 % giờ khung) | đo 15/10 |
| … SPP1 | 1,38 s/khung (mỗi lượt lấy mẫu thêm ≈ 0,6 s) | đo 15/10 |
| Khung lẻ `--only` (4 khung rải) | 4,31 s/khung — chi phí khởi động/biên dịch shader dồn lên ít khung; đừng ước giờ tập bằng số này | đo 15/10 |
| Cuộn K2V4 1080p toàn bộ (65 s) | cảnh 1,79 / toàn bộ 2,12 s/khung, 55,2 phút | `K2V4-BAO-CAO.md` §6 |
| T1 1080p (15:41) | cảnh SPP4 11 giờ 41 phút; tổng ≈ 15,5 giờ + nháp 4,8 giờ | `TAP-K2C-T1-06-G2.md` |
| Steel 1080p (17:10) | ≈ 18 giờ tổng | `TAP-K2G-01-G2.md` |
| Khung vàng 4 ca | xem `reports/NEN-TANG-BAO-CAO.md` §3 | đo 15/10 |
- **Tất định của cảnh 3D:** `hero.js` chỉ cho cùng khung khi dựng **tuần tự từ khung 0**. Dựng lẻ `--only N` ở cảnh có người đi bộ (`k2c106/corner`) lệch vùng người tới 244 mức (đo 15/10). Khi cần đúng một khung (khung vàng, sửa lẻ), dựng 0..N.
