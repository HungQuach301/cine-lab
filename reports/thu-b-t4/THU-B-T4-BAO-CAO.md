**Nhánh thật: `ccr-ce664665-996oyl`** (harness buộc; lệnh gọi `k2c-t4-02-thu-b`). Gốc origin/main @`2414d1d31a766973ab70cc50ffb463581a28e100`; merge (không squash) origin/checks-1-17-5 @`1dc8be60d4ed0e36e0b127b2b6a594929154a43e` → commit merge **`ea15a120b52bfe6c905682aac3a670418e34a6b7`** (merge sạch, LOCK 1.17.5 `c7630b4a…` KHỚP ở mọi commit). Không merge vào `main`, không đụng nhánh khác.

# THU-B-T4 — vòng thử chống "đồ chơi" T4 London (K2C-T4-02): (B) AI phủ bề mặt nhà thường · (D) nâng 3D toàn cảnh — BÁO CÁO

> 24/10/2026 04:35 → ≈ 08:10 UTC. Căn cứ: chủ dự án 24/10 06:21 "1. Chọn phương án A+B theo khuyến nghị"; 24/10 "Duyệt K1175-D1…D7 theo khuyến nghị…" (D5 = A + D; D6; D7); nhận xét gốc 23/10 23:41. Kinh thánh §15 (j) **ĐANG THỬ, CHƯA ÁP** — vòng này KHÔNG đưa gì vào phim.
> Mọi số là số đo thật trong phiên. Email chủ dự án không có trong tệp/commit/header/URL/payload/UA (UA "CineLab-research (+https://github.com/HungQuach301/cine-lab)"); khoá do proxy gắn, không in/ghi. Không chạy `lock.py` thiếu `--verify`. Không đọc mã `checks/` (chỉ CHẠY `k2check.py`; một traceback in ra khi chạy được trích ở khiếu nại KN-1).

## 0. Khối điều lệ, SHA, tóm tắt
| Trường | Lệnh | Thực tế |
|---|---|---|
| Vùng sửa | `design/k2v/ldn/thu-b/**`, `scripts/k2ldn/thu-b/**`, `channel-k2/k2c-t4-02/thu-b/**`, `reports/thu-b-t4/**` | đúng. Không sửa `checks/`, `docs/`, sổ, `tools/`, tệp của ANIMATIC-T4/P-2410b. `look2.js`, `render_look.js` chỉ ĐỌC/CHÉP: `look3.js` sinh từ `look2.js` bằng `tao_look3.py` (thay chuỗi có kiểm), `render_thub.js` = bản sao `render_look.js` + `--fac`. Thêm `channel-k2/k2c-t4-02/thu-b/.gitignore` (`!*.json`) để JSON máy/kiểm vào git (BAI-HOC-K2 K39) |
| Preflight | `set -o pipefail`, chỉ commit khi "— ĐẠT"; hook trước lần đẩy đầu | hook pre-commit + pre-push cài 04:50 (trước lần đẩy đầu 04:52); mọi commit qua `scripts/k2ldn/thu-b/cam.sh` (pipefail + kiểm "PREFLIGHT ĐẠT"). 1 lần preflight CHẶN (video kiểm 11 MB lọt vào thư mục git) → gỡ, không commit (sự cố 8) |
| Force/amend/dừng hỏi | không | không |
| Đẩy ≤ 30 phút + CHECKPOINT | bắt buộc | 17 lần đẩy; `reports/thu-b-t4/CHECKPOINT.md` |
| Tiến trình nền | PGID, một vòng nặng một lúc, P ≤ 2, RAM ≥ 5 GB | hàng đợi `dung.py` (chờ RAM ≥ 5 GB, P ≤ 2); dừng theo PGID 2 lần (sự cố 9, 12). Một lần dựng hình học D (đơn luồng, `nice 10`) chạy cạnh 2 tiến trình dựng (sự cố 6) |
| D6 lưu | mặt nạ ID, tấm ghép, ảnh AI, JSON kiểm vào git ≤ 10 phút | ảnh AI vào git 3–8 phút sau khi về (`channel-k2/k2c-t4-02/thu-b/ai/`); tấm/mặt nạ/bóng/albedo/JSON: `thu-b/tam/<khung>/`; khai + k2check + nguyên văn mô hình nhìn: `thu-b/kiem/`; video kiểm không mất (crf 0, 6–12 MB) NGOÀI git, SHA trong `video-sha.json` + lệnh tái tạo |

**Tóm tắt (đọc trước):**
1. **B làm thật được trên 3 khung, khoá dữ kiện giữ đúng:** BE-MAT-NHA (b) **0/255** ở mọi tấm; lớp (a) trừ `nha_thuong` **0/255** (đo của phiên); (a) hình khối **0 Chặn** ở cả 3 khung; (c) **0 lỗi thời đại** (gpt-6.1-sol + claude-sonnet-5-5 + O2). Ảnh AI đẹp hơn rõ ở nhà gần (≥ 4 px/m: mái ngói, vữa, gạch, cửa kính thật) — xem tờ so.
2. **Nhưng ảnh TĨNH (i) không dùng được cho timelapse nắng đổi:** (d) 57–100 % nhà lệch quỹ đạo sáng, nhấp nháy 0,046–0,088 (trần 0,012) ở cả 3 khung. Chỉ dùng được cho khung tĩnh thật sự (không đổi giờ).
3. **Chiếu 3D (ii) dựng lại ánh sáng ĐÚNG hướng nhưng chưa qua (d) ở 2 h nắng đổi:** (ii-a) chiếu trong trình dựng: (d) 7,1 % (M4) · 15,0 % (B3) · 39,3 % (M1) nhà lệch (trần 2 %); (ii-b) tỉ số bóng (tương đương chiếu camera khi máy cố định): 7,1 % · 7,2 % · 32,1 %; với **30 phút** nắng đổi (M1): **3,2 %**, nhấp nháy **0,0121** (trần 0,012, +0,8 %). Phiên tách nguyên nhân: nhà lệch là nhà có đường bóng quét qua + AI phân bố lại độ sáng bề mặt → khiếu nại KN-5 (thước (d) phạt cả dựng sáng đúng). (e) khung 0: **ĐẠT khi so ở độ phân giải video**, trượt 4,6–4,9 / 12,6–14,7 khi so tấm 1080p với video 640×360 (KN-6).
4. **Rủi ro dữ kiện còn lại của B:** AI vẽ THÊM ống khói/đầu hồi/gờ TRONG bóng nhà — thước (a) không bắt (B3 lượt 1: gpt báo 10 (w), (a) 0 cờ); lời nhắc bmn-v2b (lượt 2) giảm rõ nhưng không bằng 0; ở 2–3 px/m AI ra "vữa nhoè" và đổi bản sắc vật liệu (nhà gạch đỏ → khung gỗ). Hai lỗi phía K: N2P-* KeyError khi khung không nước (KN-1), N2P-1 (a) đếm vùng BMN là lớp (a) (KN-2).
5. **D (nâng 3D, không AI lên lớp (a)):** hình học 2 275 896 → **4 601 432 tam giác (×2,02)**; công trình có tên + mọi lớp không phải nhà thường **trùng từng bit**; số lô giữ 42 947. Đa dạng khối/mái, gãy mái, mái hắt + diềm, cửa mái, chụp ống khói, phong hoá theo nhà, nền phố tối + bóng tiếp xúc, lan can/phòng máy/lam trên toà 2026 KHÔNG tên, kính phản chiếu dải phố. Tự soi: đỡ "đồ chơi" ở toàn cảnh 2026 (mái hết phẳng trơn) và nền phố 1666; **toàn cảnh 1666 ở P1 vẫn đọc là mô hình thu nhỏ** (nhịp nhà đồng cỡ, mép sắc ở 10–20 px/nhà). D2 (vân nướng AI) gần như không thấy ở P1 (nhà 10–20 px), làm xám mái 1666 (bão hoà 0,137 → 0,122).
6. **Ước tác động (BANG-SHOT-v1):** B áp được **9/60 shot, 108 s (15,0 %)**; nhân diện tích khung có nhà đo được → **≈ 26 s-khung (3,6 %)**. Giá thật **$0,0757–0,0765/ảnh**, kiểm ≈ $0,14/tấm/lượt. D: thời gian dựng xem §4.
7. **Chi phí:** OpenAI **$1,33** (mốc $4) · Claude API **$0,82** (mốc $4) · Gemini $0 (không gọi) · ElevenLabs/RunPod/YouTube $0 · giờ máy ≈ 3,6 h.

## 1. Việc 1 — khung thử (cùng máy/giờ V2 — CHON-V2.json)
| Khung | Vai | Máy (E, N, h) → nhìn, FOV | Giờ | Nguồn máy |
|---|---|---|---|---|
| B1 M1-trung | 1666, tháp St Saviour | [532690, 180290, 70] → [532786, 180554, 0], 50° | 11/9/1666 (Greg.) 16:00 LMT | `look/may-v2/M1-trung.json` (đọc lại nguyên) |
| B2 M4-trung | 2026 mặt phố Fleet St ("hộp trắng") | [531560, 181176, 19,1] → [532102, 181122, 87], 22° | 2/9/2026 16:30 BST | `look/may-v2/M4-trung.json` |
| B3 B3-p4-1938 | H3-05 (BANG-SHOT-v1): P4 Fleet St/Ludgate 40 m | [531300, 181160, 40] → [532100, 181140, 60], 35° | 2/9/1938 15:00 BST | bảng shot P4 + look A V2 của M4 |
| D1 M1-rong-hep | P1 toàn cảnh 1666 | P1, **fov 36°** (LOOK-T4-4) | 11/9/1666 15:30 | `look/may-v2/M1-rong-hep.json` |
| D2 M4-rong-hep | P1 toàn cảnh 2026 | P1, fov 36° | 2/9/2026 15:00 | `look/may-v2/M4-rong-hep.json` |
**Lý do chọn B3:** trong BANG-SHOT-v1 chỉ P4 (40 m) và P6 (35 m) ở ≤ 60 m; shot ban ngày của P4/P6 ở 1666 hoặc ≈ 1940 không có nhà mọc/mất trong shot: **H3-05 (1937–1938, THAP, lớp A)** — duy nhất. H2-04 (P4 1667–1668) loại vì nhà đang xây lại (mọc dần) trong shot; H4-03 (P6 1940) là đêm bom. Mốc 1938 dùng hình học "1940" (khối Victoria–Edward ước lượng, bậc 5). Không có khung V2 đã chọn cho B3 → cột "V2" là look V2 dựng lại cùng máy/giờ.
**Lưu ý dựng lại:** container mới, `/var/tmp` trống → dữ liệu nền dựng lại bằng đúng lệnh LOOK (`dung_lai_du_lieu.sh`). OSM sống đổi (lô 42 951 → 42 947) → `ldn2.bin` `bd776509…` ≠ LOOK-T4-V2 `73e68223…`; cột "V2 đã chọn" trên tờ so là V2 **dựng lại** cùng máy/giờ, cùng `look2.js` (`look3.js` ≡ `look2.js` **sai khác 0** điểm ảnh — kiểm M4-trung 640×360).
**Timelapse:** 3 s, 640×360, spp 4, máy CODINH, khung 0 = giờ khung V2, chạy tới **+2 h** (bóng quét rõ); thêm M1 +30 phút (đo (d) khi nắng đổi chậm).

## 2. Việc 2 — (B) AI phủ bề mặt nhà thường
### 2.1 Cách làm
- **Mặt nạ (K-1.17.5 §7):** hình học `look3b` = V2 từng tam giác (SHA trùng) + `hid.f32`/`pid.f32` (`hinh_hoc_thub.py b`): mã nhà thường (lớp 1, 3, 10, 4 không tên OSM, không phải 30 St Mary Axe/Leadenhall — 95 548 nhà), mã mặt phẳng (nhà, pháp tuyến lượng tử 0,05, mặt phẳng 0,25 m — 997 396). `look3.js`: mặt nạ 1 tô `nha_thuong` (215,215,215), 3 = mã nhà 24 bit, 4 = mã mặt phẳng, 6 = albedo; pass bóng (albedo xám 0,6). `nha.json` [{id, lo, px_m}] (px_m = 1 m ngang chiếu ở tâm nhà, quy 1080p).
- **Nhà ĐO ĐƯỢC** (cùng định nghĩa K: ≥ 2 px/m, ≥ 100 px, ≥ 40 điểm cạnh hình học thấy ở render và bóng) — số của phiên **trùng k2check** (153/1 248, 14/34, 557/8 510).
- **AI:** OpenAI `gpt-image-2.5-sunburst-2026-09-08` `/v1/images/edits`, KHÔNG mặt nạ, 2560×1440 high. Lời nhắc **bmn-v2** (năm bắt buộc, chỉ bề mặt mái/tường, cấm thêm/bớt/gộp/tách/dời nhà, cấm đổi mái/ống khói/cửa mái, liệt kê lớp (a) không được đổi, cấm người/xe/thuyền/khói/lửa/cờ/chữ/đèn/cây, "Do not paint any reflections on water or glass", "Nothing from after <năm>") — lượt 1; **bmn-v2b** (lượt 2, sau k2check lượt 1: cấm rõ ống khói/chụp ống/đầu hồi/gờ/đá góc/cửa mới — Kinh thánh §11.3). Nguyên văn trong sổ `reports/thu-b-t4/so-ai.jsonl` và `scripts/k2ldn/thu-b/oai_bmn_thub.py`. Ảnh vào 1666 = render KHÔNG khói bếp (K42). **2 lượt/khung** (trần 3).
- **Ghép (i) ảnh tĩnh:** AI chỉ trong nhà đo được, nở 1 px CHỈ vào lớp nền (trời/đất/cây — không lấn lớp (a), không lấn nước); khớp tông AI VÀO tông render đã duyệt (Lab, k 0,7 — ngược chiều tấm nền vì ở đây render là nền); viền mềm 2 px phía TRONG vùng AI; ngoài vùng = render đúng từng bit; 1666: khói bếp cộng hiệu render có/không (khai `song`). Phóng AI về 1080p bằng Lanczos.
- **(ii-a) chiếu 3D trong trình dựng:** albedo đã khử sáng = albedo render × (tấm/render) (sRGB tuyến tính), chiếu lên mặt nhà thường bằng ma trận VP của máy khung (shader `uProj`), dựng lại ánh sáng theo giờ từng khung; hiệu chỉnh lặp (albedo × tấm/khung-0-đã-dựng): 1080p 3–5 vòng, rồi 3 vòng ở 640×360 (độ phân giải video). **(ii-b) tỉ số bóng:** trong nhà đo được C(t) = tấm × R(t)/R(0) từng điểm ảnh — đúng bằng chiếu albedo AI rồi nhân bóng(t) khi máy cố định (không lấy mẫu lại kết cấu); khai `cach: chieu_3d`.
- **k2check:** `channel-k2/k2c-t4-02/thu-b/kiem/<tên>/` (episode.yaml tối thiểu `channel: k2`, `khung_sach`, `kenh2_tu_t4`, timeline tổng hợp 3 s/tấm theo khuôn `reports/k1172/do/mk_tl.py`, log shot tối thiểu) — `k2check.py episode.yaml --tl timeline.json --no-asr --cap [--n2p-vision]`. Video kiểm **không mất** (crf 0 yuv444p); bản crf 10 yuv420p làm nhấp nháy (d) tăng do nhiễu mã hoá (B3 (ii-b) 0,0216 → ĐẠT khi không mất).

### 2.2 Nhà đo được theo khung
| Khung | Nhà thường thấy | Đo được | % số nhà | % diện tích nhà thường | % khung là AI | px/m TV (nhà đo được) | lý do không đo được (px/m < 2 · px < 100 · cạnh < 40) |
|---|---|---|---|---|---|---|---|
| B1 M1-trung | 8 510 | 557 | 6,5 | 79,3 | 27,7 | 2,77 | 7 250 · 7 715 · 7 821 |
| B2 M4-trung | 34 | 14 | 41,2 | 92,0 | 29,4 | 16,67 | 17 · 3 · 12 |
| B3 1938 | 1 248 | 153 | 12,3 | 91,7 | 41,0 | 4,18 | 631 · 944 · 1 072 |

### 2.3 Kết quả k2check 1.17.5 từng tấm (lượt chọn = 2; bảng đủ trong `kiem/*/k2check.md`)
| Tấm | BE-MAT-NHA (a) | (b) | (c) | (d) quỹ đạo · nhấp nháy | (e) khung 0 | N2P-1 | N2P-3 |
|---|---|---|---|---|---|---|---|
| B1 M1-trung l1 | 0 Chặn · 1 (w) | 0/255 | 0 lỗi | — | — | TRƯỢT 192/255 (KN-2) | ĐẠT (T9b 0,09 %, T9c 0) |
| B1 M1-trung l2 · (i) | 0 Chặn · 2 (w) | 0/255 | 0 lỗi (lần 2; lần 1 THIẾU — KN-3) | **100 % · 0,088** | — | TRƯỢT 218/255 (KN-2) | ĐẠT |
| B1 · (ii-a) chiếu 3D | như trên | 0/255 | 0 | **39,3 % · 0,0199** | 4,9/12,9 (tấm 1080p) · **ĐẠT** (tấm 640) | — | — |
| B1 · (ii-b) tỉ số bóng | như trên | 0/255 | 0 | **32,1 % · 0,0143** | ĐẠT | — | — |
| B1 · (ii-b) 30 phút | như trên | 0/255 | — | **3,2 % · 0,0121** | ĐẠT | — | — |
| B1 · (i) 30 phút | như trên | 0/255 | — | 86,9 % · 0,0774 | — | — | — |
| B2 M4-trung l1 | 0 Chặn · 0 (w) | 0/255 | THIẾU (claude không đọc đủ ảnh) | — | — | không chạy được (KN-1) | không chạy được |
| B2 M4-trung l2 · (i) | 0 Chặn · 0 (w) | 0/255 | 0 lỗi | **57,1 % · 0,0455** | — | không chạy được (KN-1) | không chạy được |
| B2 · (ii-a) | 0 · 0 | 0/255 | 0 | **7,1 % (1/14) · 0,0138** | 4,8/14,7 · **ĐẠT** (640) | — | — |
| B2 · (ii-b) | 0 · 0 | 0/255 | 0 | **7,1 % (1/14) · ĐẠT** | ĐẠT | — | — |
| B3 l1 | 0 Chặn · 0 (w) máy; gpt **10 (w)** "thêm ống khói/đổi đầu hồi" | 0/255 | THIẾU (claude) | — | — | không chạy được | không chạy được |
| B3 l2 · (i) | 0 Chặn · 1 (w) | 0/255 | 0 lỗi | **88,2 % · 0,0469** | — | không chạy được | không chạy được |
| B3 · (ii-a) | 0 · 1 (w) | 0/255 | 0 | **15,0 % · ĐẠT** | 4,6/12,6 · **ĐẠT** (640) | — | — |
| B3 · (ii-b) | 0 · 1 (w) | 0/255 | 0 | **7,2 % (11/153) · ĐẠT** | ĐẠT | — | — |
Ghi: "—" = không khai/không áp. Hàng BE-MAT-NHA tổng của mỗi lần chạy là TRƯỢT vì (d) (và (e) khi so tấm 1080p). Khung 0 chiếu 3D ở 1080p (PNG, so tấm): B1 2,43/8,09 · B2 2,90/9,52 · B3 2,36/9,77; ở 640×360: 2,44/6,60 · 2,47/8,38 · 2,19/6,48.

### 2.4 Đọc từng cờ (w) bằng mắt (ô phóng ×3 render | ghép: `thu-b/tam/<khung>/l*/soi-a.jpg` ngoài git → JSON `soi-a.json` trong git; ảnh tờ so)
| Tấm | Nhà | Cờ | Đọc bằng mắt |
|---|---|---|---|
| B3 l2 | 34226 (26,4 px/m) | nghi dời 3,6 m (IoU 0,02; đỡ 0,68 → 1,00) | mái đá phiến cùng chỗ, cùng mép; AI chỉ sắc hơn + thêm vân — **báo nhầm** (dịch tối ưu bắt vào hàng ngói lặp) |
| B1 l1 | 87390 (3,2 px/m) | nghi dời 2,2 m | nhà xa, mép giữ; mái AI "nhoè" — báo nhầm về hình khối, nhưng **chất lượng kém** (vữa nhoè) |
| B1 l2 | 24449 (2,27 px/m), 24555 (2,39 px/m) | nghi dời 4,0 / 4,9 m (đỡ 0,47 / 0,65) | cụm nhà xa ở ngưỡng đo: AI thành mảng màu nhoè, mất bóng đổ giữa các mái → không "dời" mà **mất cấu trúc**; đây đúng là vùng không nên dùng B |
| B3 l1 (mô hình nhìn) | 10 vùng | thêm ống khói/chụp ống, đổi đầu hồi | ô phóng xác nhận **ống khói AI vẽ thêm** trong bóng nhà (34014, 34242) — thước (a) không bắt (KN-4); lượt 2 bmn-v2b hết ở ô thấp nhất |
| Tự soi thêm (không cờ) | B1 88339; B3 30956 | — | AI đổi bản sắc vật liệu (gạch đỏ → khung gỗ xám; mặt tiền trơn → gạch trang trí); ghép "bóng ma" khi nhà AI lệch 1–3 px so khối (B3 33355, 82337) |

### 2.5 Tự soi chỗ còn "đồ chơi" (thẳng)
- B làm biến mất "đồ chơi" ở **nhà gần** (B2 cả khung trừ toà có tên; B3 lớp nhà trước) — đây là cải thiện lớn nhất của vòng.
- **"Hộp trắng" giữa-phải M4-trung là toà CÓ TÊN OSM** (lớp (a)) → B không được chạm; vẫn "hộp trắng". Muốn hết phải nâng 3D vật liệu toà đó (hướng D) hoặc quyết luật cho toà 2026 có tên không phải công trình mốc.
- M1-trung: nhà xa (≈ 79 % số nhà, 21 % diện tích nhà) giữ render → **ranh AI/render thấy được**: nửa trước "ảnh chụp", nửa sau "mô hình". Ở 2–3 px/m AI ra nhoè.
- Timelapse: (i) ảnh tĩnh "chết" khi nắng đổi (bóng in sẵn); (ii) bóng đi đúng nhưng ô cửa AI phản chiếu cố định.

## 3. Việc 3 — (D) nâng 3D toàn cảnh (không AI lên lớp (a))
**Hình học `look3d`** (`hinh_hoc_thub.py d`; RNG chung KHÔNG tiêu thụ thêm — biến thể theo băm vị trí nhà): cao ±0–0,8 tầng theo lô; đổi hướng hồi 22 % lô hẹp; dốc ±8°; **gãy mái** (lô ≥ 6,4 m chia 2 khối khác cao/khác mái, 55 %); **mái hắt** 0,22–0,40 m + diềm mái (phá mép hộp, tạo bóng dưới mái); cửa mái 35 % nhà ≥ 3 tầng; ống khói cao thấp + 1–3 chụp ống; khối Victoria mái bằng → mái dốc (40 %); toà 2026 KHÔNG tên: lan can 1,1–1,6 m + 1–4 phòng máy/thiết bị + lam. **Kiểm luật cứng:** mọi tam giác lớp 2, 5, 6, 7, 8, 9, 11 trùng từng bit với V2 (`reports/thu-b-t4/do/kiem-cong-trinh-d.json`); toà OSM có tên không thêm gì (sửa giữa phiên — sự cố 6). 4 601 432 tam giác (×2,02).
**Shader `look3.js` (cờ `d`):** mỗi nhà một độ sáng/ngả màu/độ bẩn; vệt chảy dọc; chân tường tối (tiếp đất 2,4 m); rêu/ám khói loang + mép mái tối; đá nhà thờ giáo xứ/tường thành ám khói (chỉ bề mặt); nền phố tối + loang; che khuất trời mạnh hơn trong ngõ (bóng tiếp xúc nhà–phố từ lightmap nướng); kính 2026 phản chiếu dải phố dưới chân trời + trời, ô kính lệch nhẹ. Nướng lại 1666.6/2026.7 trên `look3d`.
**D2 (vân nướng AI, §11.3 (b)):** 4 ảnh OpenAI edits ($0,303) sửa từ BẢN VẼ lưới cửa của chính shader (tầng 2,8/3,0/3,6/3,8 m, khoang 2,4/2,3/2,6/3,0 m): 8 mặt tiền 12 × 13,5 m cho mỗi thời kỳ (1666 khung gỗ; gạch Georgian/Victoria; văn phòng 2026) + 3 mái (ngói đất nung, đá phiến, mái bằng). Gán theo băm mã nhà, albedo chuẩn hoá theo trung bình hàng atlas × độ sáng albedo gốc của nhà. **Khác "vân vật liệu AI kiểu B" (PT/H-B, thua chấm mù):** kiểu B = 9 mẫu vật liệu LÁT LẶP sinh tự do, albedo không hiệu chuẩn, lộ nối, không giữ lưới cửa; D2 = mặt tiền trọn (tầng, cửa, cửa hàng, bẩn theo tầng) theo lưới cửa của cảnh 3D, hiệu chuẩn albedo, gán theo nhà. **Chưa đạt "một bộ vân/toà × mốc" của §11.3 (b)**: 8 biến thể/thời kỳ dùng chung theo băm (lặp thấy được ở khung gần — chưa thử ở khung gần). Nhà 1666 gạch và khối Victoria giữ thủ tục; gạch 2026 giữ thủ tục (sửa giữa phiên — sự cố 7).
**Số đo** (`reports/thu-b-t4/do/d-*.json`, thước `look_do.py`):
| Khung | Biến thể | Tam giác | Bão hoà TV (640×360) | Trời + sương | 
|---|---|---|---|---|
| D1 M1-rong-hep | V2 · D · D2 | 2 275 896 · 4 601 432 · 4 601 432 | 0,137 · 0,137 · 0,122 | 7,0 % · 7,0 % · 7,0 % (≤ 20 %) |
| D2 M4-rong-hep | V2 · D · D2 | như trên | 0,114 · 0,114 · 0,141 | 7,0 % |
(Bão hoà trung vị lượng tử theo 1/255 → V2 và D trùng số dù ảnh khác TB 8,0/8,7 mức xám.) **Tốc độ:** §4.
**Tự soi D (thẳng):** 2026: mái hết là tấm phẳng trơn, nền phố bớt "sân trắng" — đỡ rõ "đồ chơi"; nhưng mặt tiền văn phòng vẫn là lưới cửa thủ tục đều. 1666 ở P1: nhà ≈ 10–20 px, nhịp đồng cỡ + mép sắc vẫn đọc như mô hình thu nhỏ; D làm mái đa dạng hơn và bớt cam đồng đều, nhưng **không đổi được cảm giác tỉ lệ**. D2 ở P1 gần như vô hình, làm mái 1666 xám. Lớp (a) (nhà thờ giáo xứ khối hộp sáng, tường thành) vẫn là khối thô lớn nhất trong toàn cảnh 1666 — nằm ngoài phạm vi B và ngoài phần D của vòng này (chỉ phong hoá bề mặt).

## 4. Việc 4 — tờ so, ô 1080p, clip
- Tờ so: `reports/thu-b-t4/to-so-thu-b.jpg` (2944 × 5120, nhãn rõ, KHÔNG mù): B1–B3 cột **V2 đã chọn · B ảnh tĩnh · B chiếu 3D (khung 0)** + dải "+2 h" (V2 · (i) · (ii-a) · (ii-b)); D1–D2 cột **V2 · D 3D · D + vân nướng** (+ dải "+2 h" D1). Dòng kết quả kiểm dưới mỗi ô. Cấu hình: `reports/thu-b-t4/do/to-so-cau-hinh.json`.
- Ô 1080p JPG ≤ 2 MB: `reports/thu-b-t4/khung/<khung>-{v2,B-anh-tinh,B-chieu-3d,D,D2}.jpg` (15 ô).
- Clip 3 s 640×360 (≤ 0,5–1 MB): `reports/thu-b-t4/clip/<khung>-B-{anh_tinh,chieu_3d,chieu_tiso}.mp4`, `<khung>-V2-render.mp4`; D: `M1-rong-D-{v2,d,d2}.mp4`.
- **Tốc độ dựng** (đo KHÔNG chạy chồng, `scripts/k2ldn/thu-b/bench.sh`, s/khung sau nạp cảnh): một tiến trình, sau nạp cảnh (nạp: V2 ≈ 8 s, D ≈ 15–16 s):
| Khung | Biến thể | 1080p spp 24 (s/khung) | 640×360 spp 4 (s/khung, 12 khung timelapse) | × V2 |
|---|---|---|---|---|
| D1 M1-rong-hep | V2 · D · D2 | 48,4 · 75,5 · 72,6 | 8,49 · 13,08 · 13,01 | D ×1,56 / ×1,54 |
| D2 M4-rong-hep | V2 · D · D2 | 49,1 · 79,4 · 78,2 | 8,75 · 14,68 · 14,53 | D ×1,62 / ×1,68 |
Số đo khi chạy chồng (P = 2, ghi trên tờ so ở lượt đầu) cao hơn 15–40 % — không dùng để ước. Tốc độ bị giới hạn bởi số đỉnh (llvmpipe), D2 không chậm thêm.

## 5. Việc 5 — ước tác động cả tập (BANG-SHOT-v1; ANIMATIC-T4 chưa đẩy bảng v2 — `git ls-remote` 06:00 không có nhánh animatic T4)
**% nhà đo được theo điểm máy** (đo thật, mặt nạ + bóng, `channel-k2/k2c-t4-02/thu-b/uoc/`):
| Điểm máy | Mốc | Nhà thấy | % số nhà đo được | % diện tích nhà | % khung | px/m TV nhà đo được |
|---|---|---|---|---|---|---|
| P1 (fov 36°) | 1666 · 2026 | 11 953 · 1 128 | 9,4 · 8,4 | 49,1 · 58,5 | 19,7 · 23,1 | 2,56 · 2,50 |
| P2 (M1-trung, fov 50°) | 1666 | 8 510 | 6,5 | 79,3 | 27,3 | 2,77 |
| P3 | 1666 | 10 732 | 4,2 | 54,9 | 22,3 | 4,13 |
| P4 (B3) / P4b (M4-trung) | 1938 / 2026 | 1 248 / 34 | 12,3 / 41,2 | 91,7 / 92,0 | 41,0 / 29,3 | 4,18 / 16,67 |
| P5 | 1666 · 2026 | 11 616 · 2 059 | 6,2 · 3,9 | 33,2 · 53,8 | 14,3 · 23,1 | 2,58 · 2,85 |
| P6 | 1666 | 4 184 | 5,3 | 79,9 | 9,5 | 4,58 |
| P8 | 1666 | 17 201 | 1,3 | 25,6 | 7,3 | 3,09 |
| P7 (2 200 m) | — | — | 0 (px/m ≤ 0,7, tính hình học) | 0 | 0 | — |
**Shot áp được** (luật đặt trước khi đếm: shot 3D lớp A; ban ngày suốt shot; không trong cháy 1666/đêm bom 1940; không có nhà mọc/mất trong shot — `do/uoc-tac-dong.json`, bảng đủ `do/uoc-tac-dong.md`): **9/60 shot, 108 s = 15,0 % thời lượng** (H1-03, H2-07, H2-12, H2-13, H3-05, H3-06, H4-08, H5-05, H5-06); có nhà đo được trong khung ≈ **26 s-khung (3,6 %)**. Ngược với giả định K1175-D5 "P1 gần như không được phủ": ở P1 fov 36° vẫn có ≈ 20 % khung là nhà đo được (Bankside + bờ bắc gần), nhưng px/m TV 2,5 — **đúng vùng AI nhoè** (§2.4).
**$/tấm thật:** ảnh $0,0757–0,0765 (sổ AI); kiểm/tấm/lượt: gpt-6.1-sol $0,045–0,068 + claude-sonnet-5-5 $0,040–0,065 + O2 ≈ $0,011 × 2 → ≈ $0,14. **Cả tập** (≈ 11 tấm: 9 shot, 2 shot KHOP hai mốc) × 2 lượt × ($0,076 + $0,14) ≈ **$4,8**; + video kiểm (máy). Giờ máy B: (ii-b) chỉ cần thêm render KHÔNG khói bếp (1666) + 5 mặt nạ/bóng/albedo ≈ 2–4 phút/shot; (ii-a) dựng lại cả shot (+100 % giờ dựng shot đó) + 6 khung hiệu chỉnh.
**Giờ dựng thêm của D cả tập:** lớp A cả tập 12 312 khung (ước LOOK-T4-V2 §5); D chậm hơn V2 ×1,54–1,68 (đo ở trên) → **+≈ 6,5–8 h giờ máy ở P = 2** (V2 ≈ 12,1 h → D ≈ 19–20 h); thêm nướng lightmap D 3 mốc ≈ 3 phút. Bộ nhớ: hình học D 590 MB (V2 297 MB) — P = 2 vẫn còn ≥ 5 GB RAM trong phiên.
**Rủi ro dữ kiện còn lại:** (1) chi tiết kiến trúc AI tự thêm trong bóng nhà (ống khói, đầu hồi, gờ) — chỉ mô hình nhìn (w) + người đọc bắt; (2) AI đổi bản sắc vật liệu (gạch ↔ khung gỗ; màu sơn — §11.3 "màu sơn do AI đổi chỉ tạm chấp nhận"); (3) ranh nhà đo được/không đo được thấy được trong khung (chất lượng, không phải dữ kiện); (4) N2P-* không chạy trên khung không nước và N2P-1 trượt mọi tấm BMN tới khi K sửa (KN-1, KN-2) → **chưa có tấm nào qua đủ cổng (c)**; (5) (d) trượt ở nắng đổi 2 h với mọi cách — áp B cho timelapse cần K quyết KN-5 hoặc giới hạn tốc độ nắng đổi.

## 6. Việc 6 — phiếu
`reports/thu-b-t4/PHIEU-THU-B.md` (chọn cột mỗi khung; quyết B: cách nào, ở đâu; quyết D: bản nào). Phiên không chấm mù bằng AI, không chọn hộ.

## 7. Chi phí thật (`reports/thu-b-t4/do/chi-phi.json`, sổ `reports/thu-b-t4/so-ai.jsonl`)
| Khoản | Mốc | Chặn | Thật | Ghi |
|---|---|---|---|---|
| OpenAI | $4 | $10 | **$1,33** | ảnh 10 × gpt-image-2.5 edits = $0,761 (D2 4 = $0,303; B 6 = $0,458) + mô hình nhìn gpt-6.1-sol 14 lần $0,565 |
| Claude API | $4 | $12 | **$0,82** | mô hình nhìn claude-sonnet-5-5 14 lần $0,684 + q_thoi_dai (O2) ≈ 11 lần $0,139 |
| Gemini | 0 | — | **$0** | không gọi (ngân sách T4 dành animatic) |
| ElevenLabs / RunPod / YouTube | 0 | — | 0 | |
| Giờ máy | 8 h | — | ≈ 3,6 h đồng hồ container (04:35 → ≈ 08:10) | dựng lại dữ liệu nền 11 phút; ≈ 100 lượt dựng llvmpipe |
| Token phiên chính | — | — | không đo được từ container | |
C2PA: 10/10 ảnh AI có chuỗi C2PA (`c2pa_co_chuoi` trong sổ).

## 8. Sự cố
| # | Sự cố | Xử lý | Kết quả |
|---|---|---|---|
| 1 | Container mới: `/var/tmp` trống; `verify.sh` FAIL OpenEXR, three.js, tifffile/pyshp, k2v node_modules; `osm_vec.py` thiếu `pyproj` | cài theo gợi ý verify + `pyproj`; dựng lại dữ liệu bằng lệnh LOOK | 11 phút; SHA trong CHECKPOINT; `tai_tu_lieu.py`/`tai_van.py` ghi đè tệp git → khôi phục bằng `git checkout` (không sửa tệp ngoài vùng) |
| 2 | OSM sống đổi → `ldn2.bin` khác LOOK-T4-V2 | cột V2 dựng lại cùng máy/giờ | ghi |
| 3 | Mã nhà 24 bit lệch −1 ở mã bội 256 (nội suy varying lệch ε) | làm tròn trong shader; dựng lại mặt nạ 3/4 B1, B2 | còn 3 điểm ảnh mã lạ ở B1 → 0 (ghi `ma_la_px`) |
| 4 | k2check cần timeline + `channel: k2` + `khung_sach` mới ra hàng N2P/BE-MAT-NHA | episode/timeline/log shot tối thiểu | chạy được |
| 5 | N2P KeyError (không nước), N2P-1 đếm vùng BMN, claude không đọc đủ ảnh 4/14 lần | khiếu nại `khieu-nai-K.md` KN-1…KN-3; chạy lại mô hình nhìn | (c) đủ ở lượt chọn cả 3 khung |
| 6 | D thêm lan can/thiết bị cả cho toà OSM CÓ TÊN (luật cứng) | lọc toà có tên, dựng lại `look3d` (`nice 10`, cạnh 2 tiến trình dựng — vượt "một vòng nặng" trong ≈ 7 phút) | chỉ khung 2026 bị ảnh hưởng; đã dựng lại; không khung sai nào vào tờ so |
| 7 | D2 phủ mặt tiền văn phòng lên toà gạch 2026; nhà 1666 gạch nhận mặt tiền 1900 | loại khỏi D2 (giữ thủ tục) | dựng lại M4-rong-hep D2 |
| 8 | Video kiểm crf 10 → nhiễu mã hoá làm (d) nhấp nháy trượt; video không mất 11 MB lọt vào thư mục git → preflight CHẶN | video kiểm không mất NGOÀI git (SHA), bản xem crf 20 trong git | không có tệp > 5 MB nào được commit |
| 9 | Chiếu M4 sau 3 vòng ΔE 4,62/14,06 | dừng chuỗi theo PGID, thêm 2 vòng | 2,90/9,52 |
| 10 | (e) trượt vì so video 640×360 với tấm 1080p | hiệu chỉnh ở 640×360 + khiếu nại KN-6 | ĐẠT khi so cùng độ phân giải |
| 11 | Thông điệp commit `9bea2b19` ghi "CHECKPOINT 06:35" (đúng 06:05) | không amend; ghi ở đây | — |
| 12 | Dừng chuỗi ước (uoc) theo PGID để ưu tiên chiếu B | chạy lại, bỏ qua việc đã xong | không mất dữ liệu |
| 13 | Lỗi mã của phiên: biến `TP` thiếu ở `tiso`; khai 30 phút thiếu bước `luu` | sửa, chạy lại | — |
| 14 | `design/k2v/ldn/thu-b/look3.js` không nằm trong lệnh `git add` từ commit 3 → bản trong git cũ hơn bản đã dùng tới commit cuối | phát hiện khi kiểm `git status` sau commit cuối; commit `89ceec70` đưa đúng bản đã dùng (sinh lại bằng `tao_look3.py` khớp từng byte, sha256 `5b726c5a…`) | mọi số đo trong báo cáo là của bản này |
Không lỗi nào lặp ≥ 3 lần cùng cách. Không `pkill -f`.

## 9. Chỉ số trong ±5 % quanh ngưỡng (luật cứng — nêu tên)
| Chỉ số | Giá trị | Ngưỡng | Lệch |
|---|---|---|---|
| (d) nhấp nháy B1 (ii-b) nắng đổi 30 phút | 0,0121 | ≤ 0,012 | **+0,8 %** (TRƯỢT sát) |
| (e) p95 B3 (ii-a) so tấm 1080p | 12,6 | ≤ 12 | **+5,0 %** |
| (a) đỡ cạnh nhà 24449 (B1 l2) | 0,47 | Cảnh báo < 0,45 | +4,4 % (cờ do "dời") |
| Ngoài ±5 % (ghi để rõ): (d) nhấp nháy B2 (ii-a) 0,0138 (+15 %); (e) p95 B1 12,9 (+7,5 %), B2 14,7 (+22,5 %); (d) % nhà B2 7,1 % = 1/14 nhà (cỡ mẫu nhỏ); trời + sương P1 7,0 % (≤ 20 %, xa) | | | |

## 10. Dòng sổ đề xuất (P ghi — phiên này không sửa sổ)
- **COST-LEDGER:** 24/10 THU-B-T4 — OpenAI $1,33 (ảnh $0,761 + nhìn $0,565), Claude API $0,82 (nhìn $0,684 + O2 $0,139), Gemini $0, giờ máy ≈ 3,6 h.
- **RIGHTS:** 10 ảnh AI OpenAI (`channel-k2/k2c-t4-02/thu-b/ai/`) — đầu vào là render của chính dự án / bản vẽ lưới cửa của phiên; chỉ dùng thử, CHƯA dùng trong phim (§15 (j)). Không nhạc/SFX/giọng/font/tư liệu mới. Dữ liệu nền tải lại theo giấy phép cũ (OSM ODbL, EA LiDAR OGL, Poly Haven CC0, Rijks Doornick).
- **AUTHORSHIP:** ghi khi chủ dự án trả lời phiếu THU-B (nguyên văn + giờ).
- **BAI-HOC-K2 (đề xuất):** (1) mã ID qua varying phải làm tròn trước khi mã hoá (lệch ở bội 256); (2) video kiểm cho thước nhấp nháy phải không mất — crf 10 yuv420p đủ làm trượt; (3) (e)/(d) so ở cùng độ phân giải; (4) biến thể hình học "nhà thường" phải lọc toà OSM có tên NGAY ở bộ sinh (luật cứng), kèm kiểm trùng từng bit các lớp khác; (5) AI phủ bề mặt chỉ đáng dùng ≥ ≈ 4 px/m — ở 2–3 px/m ra nhoè dù qua thước (a).

## 11. Việc chờ chủ dự án
1. Trả lời phiếu `reports/thu-b-t4/PHIEU-THU-B.md` (chọn cột 5 khung; T1 cách B; T2 phạm vi B; T3 bản D; T4 hướng xử lý "hộp trắng" toà có tên).
2. Phiên P: chuyển `reports/thu-b-t4/khieu-nai-K.md` (KN-1…KN-6) vào `checks-appeal.md`; ghi sổ §10; merge nhánh khi duyệt (phiên này không merge).
3. Phiên K (nếu chủ dự án muốn áp B cho timelapse): sửa KN-1, KN-2 (để có tấm qua đủ cổng (c)); quyết KN-5 (thước (d)), KN-6 (độ phân giải (e)).
