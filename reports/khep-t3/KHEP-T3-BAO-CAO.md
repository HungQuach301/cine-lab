Nhánh thật: `k2c-t3-khep` (từ origin/main @9852adf5) + `release-k2-t3-g2` (@0c7ec0d8 → @6bf8d88b). Nhánh mặc định của bộ khung `ccr-e05d9102-klug8w` không dùng.

# BÁO CÁO KHEP-T3 — 1 Short T3 Gibraltar + sổ quyết định 23/10 (23/10/2026) — DỪNG chờ chủ dự án

> Lệnh chủ dự án 23/10 12:49 ("Chỉ cần 1 short"). Chạy song song với TIEN-KY-T4 và K-1.17.3; không đụng `checks/`, `docs/`, `tools/`, `channel-k2/k2c-t3-01/cuoi/**`, `channel-k2/k2c-t4-02/**`. Mọi số dưới đây là số đo thật trên tệp.

## 0. Tóm tắt, nhánh, lệnh bổ sung
| Mục | Giá trị |
|---|---|
| Short | `k2-t3-short-S1.mp4` · SHA-256 `e1632f934b494cccf9531c900e14e58a1a7b3264a71be064b1c7fa71bdc3a4c8` · 118 650 672 B · ở gốc nhánh `release-k2-t3-g2` @**6bf8d88b** (LFS, mẫu `*-short-*.mp4`). Tải công khai lại qua media.githubusercontent.com: SHA **KHỚP** |
| Gói chữ | `k2-t3-short-S1-title.txt`, `-description.txt`, `-dang-tai.md` (cùng gốc nhánh release; bản sao `reports/khep-t3/goi/`) |
| Nhánh release | chỉ THÊM 4 tệp ở gốc (0 tệp cũ bị sửa): `git diff --name-status 0c7ec0d8 6bf8d88b` = 4 dòng `A` |
| Nhánh làm việc | `k2c-t3-khep` → ff `main` (mục 6) |
| LOCK | 1.17.2 `aca05e60…6d60` — `lock.py --verify` KHỚP ở mọi commit |
| Lệnh bổ sung trong phiên | **không có** lệnh bổ sung nào gửi tới phiên này (mục "Lệnh bổ sung đã áp" trong `CHECKPOINT.md` ghi rõ) |
| Lệnh bổ sung cũ còn treo | 23/10 10:57 cho PHAT-HANH-T3 (dòng "Who's who" trong mô tả YouTube T3) **không được áp** — kiểm `k2-t3-v1-youtube-description.txt` @0c7ec0d8: 0 lần "Who's who". Ghi BAI-HOC-K2 K32; phiên này không sửa mô tả phim chính (ngoài phạm vi "chỉ thêm tệp Short") → chờ chủ dự án (mục 9) |

## 1. Short S1 — "Gibraltar, 1704 → 2026"
### 1.1 Cách dựng
- **Hình 3D cách A dựng lại khung dọc** (không cắt từ 16:9): cảnh `tl/t3tl`, opt cảnh đinh bản cuối (`anim_H1`, `anim_H2`, `anim_N5_6` — cờ, vây, hạm đội, đời sống, đèn đêm…) chỉ đổi máy/thời gian/độ dài/danh sách lightmap; mã cảnh `design/k2v/tl/**` và `scripts/k2/**` **không sửa**. 1080×1920, SPP 4, llvmpipe.
- **Lightmap** nướng lại đúng `scripts/k2tl/anim_nuong.sh` (b2026 1 646 s, b1704 2 127 s, b1940 1 855 s, b1900 1 401 s). Meta so bản cuối (`reports/ban-cuoi-t3/do/nuong-*.json`): p99,5 lệch ≤ **1,8e-5** cả 4 → cùng lightmap. LUT kênh `k2c-t3-kenh-v030.cube` (`1fc6aa38…`) áp lên khung 3D như bước ghép bản cuối.
- **Cycles pin nổi cháy 13–14/9/1782**: cắt từ master `5b9f0bcc…` (N2.9, 347,0–351,3 s = 4,3 s), vùng **608×1080 tại x = 760** của khung gốc **1920×1080**, phóng **1,778×** lên 1080×1920 (lanczos + unsharp 5:5:0,45 như Omni 1080p); master đã mang LUT nên không áp lại. **Không** dùng 4 đoạn minh hoạ AI.
- **Giọng**: 10 câu cắt nguyên mốc câu (`T3-loi-moc.json`) từ master `T3-loi-G1-v42-14LUFS.wav`; không tạo giọng mới. Cả 10 câu có nguyên văn trong `loi-khoa.txt` (10/10); ASR faster-whisper small.en khớp chữ khoá 10/10.
- **Nhạc**: Scott Buckley "Intervention (No Melody Alt Mix)" 0–48,5 s (bài + đoạn của cue B1 mở đầu T3; RIGHTS K2-MUS-6, CC BY 4.0). **SFX** gói T3: 14 sự kiện / 13 mã (GIO-1/2, PHO-1/3, MAYBAY-1, SONG-1, CHIM-1, PXA-1/3, LUAL-1, NO-1, CO-2, DEM-1). Trộn bằng đúng chuỗi `cuoi_mix.finish_stem` (≈ `scripts/audio/master.py finish`).
- **Chữ trên hình**: chỉ bộ đếm năm (kiểu `tlLayer` của `k2.js` ở 9:16: Inter Display 700, 104 px, nảy 0,4 s khi đổi năm; góc trên trái y 202–366) + phụ đề lời cháy cứng (Inter Bold 66 px, ≤ 2 dòng/thẻ, đáy thẻ y = 1 560). Không chữ AI, không nhãn.

### 1.2 Kịch bản hình–lời (ngày → đêm)
| Giây | Điểm máy | Bộ đếm | Lời |
|---|---|---|---|
| 0,0–4,2 | **D7** (eo đất + đường băng, Rock từ bắc), 2026 15:00 → 15:40 | 2026 | To walk in from Spain, you cross an airport runway. |
| 4,2–16,0 | **Vịnh** từ tây bắc (phố trong tường, hạm đội 1704, khói vây 1705) | 1704 → 1705 → 1727 | The Rock sits at the western gate of the Mediterranean. / Historians on both sides count fourteen sieges of it, between 1309 and 1783. |
| 16,0–20,3 | **Cycles N2.9** pin nổi cháy | 1782 | In 1782, ten floating batteries came to break it. |
| 20,3–26,3 | **Línea** (Spanish Lines 1730 tiền cảnh) | 1783 | The last siege ended in 1783. / The argument didn't. |
| 26,3–35,0 | góc 2 gần ranh giới (hàng rào 1909, đường băng 1941) | 1909 → 1941 | A fence in 1909. / A runway in 1941. |
| 35,0–48,5 | **D7** (cùng điểm máy 0,0 s), 19:30 → 23:52, đèn bật | 2026 | Since July 2026, this gate has had no routine checks. / Midnight at the Gibraltar frontier. |

### 1.3 Số đo tự đo (`reports/khep-t3/do/short-S1-do.json`, `mix.json`, `chu.json` → tóm tắt)
| Chỉ số | Yêu cầu | Đo |
|---|---|---|
| Độ phân giải / fps / mã | 1080×1920, 24, H.264 | **1080×1920**, 24/1, h264 **High**, yuv420p bt709; AAC 48 kHz 299 kb/s |
| Thời lượng | 45–58 s | **48,500 s** (1 164 khung) |
| Loudness | −14 LUFS | **−14,0 LUFS** (ebur128 trên tệp cuối), LRA 3,8 LU |
| Đỉnh thật | ≤ −1 dBTP | **−1,4 dBTP** (ebur128 trên AAC cuối) |
| Lời/nền (SMR p10) | ≥ 15 dB | 19,3 dB |
| Vùng an toàn Shorts | tránh 15 % dưới, 10 % phải | 1 910 hộp chữ (mọi khung): **0 vi phạm**; đáy chữ lớn nhất y = **1 560** (≤ 1 632); mép phải lớn nhất x = **969,3** (≤ 972) |
| Tỉ lệ nguồn hình | — | 3D cách A 44,2 s (4 cảnh, 5 góc; 1 062 khung dựng) · Cycles cắt 4,3 s · AI **0 s** |

### 1.4 Tờ khung 9 ô
`reports/khep-t3/do/short-S1-do-to-khung-9.jpg` (giây 1,8 · 6,0 · 10,5 · 14,5 · 18,0 · 23,0 · 28,0 · 32,5 · 44,0).

### 1.5 Soát và sửa trong phiên (lượt 1 → lượt 2)
- Lượt 1 (SHA `4cfa5e25…`): đọc tờ khung thấy (1) cảnh Línea lúc "A fence in 1909" / "A runway in 1941" **không thấy** hàng rào, đường băng (xa 1,5–2 km) — lặp K24; (2) phụ đề nháy mờ 0,04 s giữa 2 thẻ cùng câu. Sửa: D chia 2 góc (cắt 6,0 s sang góc gần ranh giới, thử 6 góc không lightmap G1–G6), góc 1 còn 6,0 s; thẻ liền nhau đổi chữ tại chỗ. Dựng lại 353 khung D (1 372 s). Lượt 2 = bản phát hành.

### 1.6 Chỉ số trong ±5 % ngưỡng và điểm còn lại (nêu tên)
- **Mép phải phụ đề 969,3 px** so ngưỡng 972 (99,7 %) — trong vùng an toàn nhưng sát ngưỡng.
- **Góc 1 Línea (1783) cỏ trống ≈ 50 % khung trong 6,0 s** — đúng trần R2 "≤ 6 s liên tục" (không đo mặt nạ ID; ước bằng mắt trên tờ khung).
- **Góc 2 D (26,3–35,0 s): Rock chạm mép trái khung** (sườn tây bắc). Ở khoảng cách đủ gần để thấy hàng rào 1909 (≈ 1,4 km tới Rock), khung dọc ngang 33° không chứa trọn Rock (≈ 46°) — LOOK-4 coi "Rock cắt mép" là lỗi; tôi chọn ưu tiên vật lời nhắc tới (LOOK-5: người xem hiểu > đẹp). Chờ chủ dự án (mục 9).
- Cảnh vịnh (4,2–16,0 s): Rock nhìn chéo, đất eo/sườn bắc chạm mép trái; tàu 1704 nhỏ (xa ≈ 3 km).
- Dữ liệu OSM tải lại 23/10 khác bản cuối 22/10: thẻ màu nhà OSM 47 → 54 trên 14 440 toà (0,05 %), các số đếm khác giống hệt (`v7b_mau_nha.py`). Ảnh hưởng chỉ màu tường của ≤ 7 toà 2026.

## 2. Gói chữ Short (gốc nhánh release)
- `k2-t3-short-S1-title.txt`: `Gibraltar, 1704 → 2026 | 3D Timelapse` (**37 ký tự**). Mọi năm có trong lời + bộ đếm.
- `k2-t3-short-S1-description.txt` (1 298 ký tự): dòng 1 = các mốc đúng lời khoá (sieges, ten floating batteries in 1782, fence 1909, runway 1941, no routine checks since July 2026); "Full film: [link video chính — chủ dự án điền]"; câu công bố "Narration: synthetic voice (ElevenLabs)…", "No AI-generated scenes in this Short", "AI use = Yes (synthetic voice)"; ghi công nhạc đúng mẫu dòng Scott Buckley của mô tả T3 + link CC BY 4.0; SFX (Sardin, thimras, NPS + câu NPS); OSM/Catastro/Copernicus/Poly Haven/ambientCG như phim chính.
- `k2-t3-short-S1-dang-tai.md`: hướng dẫn tiếng Việt — tải tệp + SHA, tiêu đề/mô tả, **AI use = Yes** vì giọng tổng hợp, **Related video** tới phim chính sau khi cả hai đã đăng, thứ tự đăng, bảng nội dung đối chiếu.

## 3. Sổ (nhánh k2c-t3-khep)
| Tệp | Dòng thêm |
|---|---|
| `AUTHORSHIP.md` | +3: 23/10 10:57 "Xem câm đạt 7/8 , tên người giữ rock tôi hơi khó nghe" → **XEM CÂM ĐẠT** §13.4; 12:49 "Đồng ý với lộ trình khuyến nghị" + "Chỉ cần 1 short"; 13:06 duyệt nâng cấp chất lượng T4 + 3 điểm bổ sung (bản đồ lịch sử hoạt hoá; hình vẽ/bản vẽ công trình và nhân vật biểu tượng; đa dạng cú máy điện ảnh vẫn giữ timelapse cùng nơi) |
| `RIGHTS.md` | +1 mục, dòng **T3-SHORT-S1** (nguồn hình 3D/Cycles, giọng, nhạc K2-MUS-6, 13 mã SFX, SHA); dòng **T3-THUMB** đổi cột nguồn thành "**chờ chủ dự án: công cụ AI, ngày tạo, khung gốc**" |
| `COST-LEDGER.csv` | +1 dòng `KHEP-T3` |
| `channel-k2/BAI-HOC-K2.md` | K32 (lệnh bổ sung phải vào CHECKPOINT + báo cáo §0; "Who's who" không được áp), K33 (hook preflight thay hook LFS → GH008), K34 (9:16 làm mất vật lời nhắc tới) |
| `scripts/k2tl/khep_short.py` | mã Short (mới; chỉ thêm) |
| `reports/khep-t3/**` | báo cáo, CHECKPOINT, số đo, `heroes.json` (opt + dấu cảnh từng cảnh), `loi.json`, `phu-de.json`, `mix.json`, meta 4 lightmap, gói chữ |

## 4. Kiểm
| Kiểm | Kết quả |
|---|---|
| LOI-KHOA (`sha256sum -c LOI-KHOA.sha256`) | **3/3 OK** |
| `checks/lock.py --verify` | **KHỚP** 1.17.2 `aca05e60…` (mọi commit; không gọi lock.py thiếu --verify) |
| `tools/preflight.sh` (hook pre-commit/pre-push, `set -o pipefail`, chỉ commit khi "— ĐẠT") | ĐẠT mọi commit; `--range origin/main..HEAD` ở mục 6 |
| Email | 0 email trong diff phiên (preflight + grep mục 6); UA tải: "CineLab-research (+https://github.com/HungQuach301/cine-lab)" |
| Tự đo Short | mục 1.3 |
| Không force-push, không amend | đúng |

## 5. Chi phí thật
| Dịch vụ | Chi | Mốc |
|---|---|---|
| Claude API | **$0** (0 subagent; ASR chạy máy) | $3 |
| RunPod | **$0** (không thuê GPU) | $0 |
| ElevenLabs / Gemini / OpenAI / YouTube | 0 ký tự / $0 / $0 / 0 | 0 |
| Giờ máy | **≈ 3,6 h** (06:19 → ≈ 09:55 UTC; nướng 7 029 s chồng dựng 1 062 + 353 khung) | 6 h |
| LFS | +119 MB | — |

## 6. Merge main
Mục này được điền sau khi chạy (xem commit cuối).

## 7. Sự cố
1. `cuoi_cache.sh` lần 1 dừng: thiếu ref `origin/v5a` (LUT A) → `git fetch origin v5a`, chạy lại (≈ 3 phút).
2. Nướng lần 1 hỏng cả b2026, b1704: Blender python thiếu `imageio` (`ModuleNotFoundError`, ≈ 5 phút vô ích) → `/opt/bpy/bin/python -m pip install imageio` (nên thêm vào `scripts/env/setup.sh` — đề xuất cho phiên Nền tảng).
3. Chromium sập (Target crashed) khi chạy 3 trình duyệt thử góc + Blender → giữ P ≤ 2 từ đó.
4. Hàng chờ dựng lấy PID bằng `pgrep -f` khớp nhầm (cùng PID cho 2 luồng) → dừng theo PGID, đặt lại bằng PID từ `ps`.
5. Ghép lượt đầu: cỡ chữ 0 tại khoảnh khắc đổi năm (backOut = 0 ở u = 0) → kẹp tỉ lệ ≥ 0,05.
6. Lượt 1 thiếu vật lời ở D (mục 1.5) → dựng lại 353 khung.
7. Đẩy release bị GH008 (đối tượng LFS chưa lên) vì hook pre-push là preflight → `git lfs push origin release-k2-t3-g2` rồi đẩy lại; tải công khai kiểm SHA KHỚP (K33).
8. `cuoi_cache.sh` ghi đè `reports/v7b/do/mau-nha.json` (ngoài vùng) → `git checkout` trả lại, không commit.

## 8. Tệp ngoài git (tái tạo)
| Tệp | Tái tạo |
|---|---|
| bộ đệm cảnh `/var/tmp/cine-out/k2tl-cache/` | `git fetch origin v5a && bash scripts/k2tl/cuoi_cache.sh` |
| lightmap | `NUONG_META=reports/khep-t3/do bash scripts/k2tl/anim_nuong.sh b2026 b1704 b1940 b1900` (cần `imageio` cho Blender) |
| khung cảnh dọc (≈ 680 MB) | `KHEP_OUT=/var/tmp/cine-out/khep python scripts/k2tl/khep_short.py heroes` rồi `dung short_A|B|D|E` (dấu cảnh trong `reports/khep-t3/do/heroes.json`) |
| Short | `khep_short.py tron && khep_short.py ghep` (cần master T3 `5b9f0bcc…` ở `$KHEP_OUT`) — bản phát hành ở release (LFS) |

## 9. Việc chờ chủ dự án
1. **Duyệt Short S1**: xem `k2-t3-short-S1.mp4` (nhánh release) + tờ khung 9 ô.
2. Quyết **Rock chạm mép trái** ở góc 2 cảnh D (26,3–35,0 s) — giữ (ưu tiên thấy hàng rào/đường băng) hay đổi sang góc xa (Rock trọn, hàng rào khó thấy).
3. Sau khi đăng: điền link phim chính vào mô tả Short, gắn **Related video**; gửi link + ngày giờ đăng cho phiên P.
4. **T3-THUMB**: gửi công cụ AI, ngày tạo, khung gốc của thumbnail T3 (RIGHTS).
5. **Dòng "Who's who"** trong mô tả T3 (lệnh 10:57 chưa áp): sửa trực tiếp trên YouTube hoặc giao một phiên đóng gói sửa `k2-t3-v1-youtube-description.txt`.
6. Đề xuất cho phiên Nền tảng/K (không thuộc phiên xưởng): `tools/preflight.sh` ở chế độ pre-push gọi thêm `git lfs pre-push "$@"`; `scripts/env/setup.sh` cài `imageio` cho Blender python.
