**Nhánh thật: `claude/k1178-t4-london-rules-pdjfmz`** (harness buộc tên này; lệnh ghi `checks-1-17-8`). Gốc `origin/claude/k1177-animatic-checks-nfbsbr` @1277400a (LOCK 1.17.7 `3a53574c…`). Không merge, không đụng `main`, P-2610 hay nhánh khác.

# Phiên K-1.17.8 — luật còn thiếu trước bản cuối T4 London: LUẬT E + khiếu nại ANIMATIC-T4-V2 §8 + hiệu chuẩn BIEN-CO-V — BÁO CÁO

> Phiên K, 25/10/2026 ≈ 17:12 → ≈ 19:20 UTC (00:12 → 02:20 ngày 26/10 Asia/Saigon). Mọi số là số đo thật trong phiên; tệp số đo ở `reports/k1178/do/`.
> Căn cứ (nguyên văn, Asia/Saigon): 26/10 00:07 "Chọn hướng cho cảnh hiện đại: A+B+E (khuyến nghị)" (E = ảnh nền AI TOÀN KHUNG cho góc rộng 2026 máy cố định; AI vẽ lại cả nhà thường; sông, đường bờ, mái vòm St Paul's, toà tháp có tên ghép lại từ 3D; nới ngưỡng px/m riêng cảnh năm ≥ 2020); 25/10 09:08 "…các vấn đề khác đều có thể nới để tăng chất lượng và độ chân thực của hình ảnh / Người xem cũng không phải là người chuyên về khảo cổ…"; 25/10 21:35 "Các hình 3D hiện đại đang rất yếu so với hình từ Omni".
> Email chủ dự án không có trong tệp, commit, header, URL, payload hay User-Agent nào (UA `CineLab-research (+https://github.com/HungQuach301/cine-lab)`). Không in/ghi khoá (proxy gắn khoá).

## 0. Khối điều lệ và tóm tắt
| Trường | Lệnh | Thực tế |
|---|---|---|
| Nhánh | `checks-1-17-8` từ @1277400a | harness buộc `claude/k1178-t4-london-rules-pdjfmz` (dòng đầu); gốc đúng @1277400a |
| Vùng sửa | `checks/**`, `checks-appeal.md`, `reports/k1178/**` | đúng. Không sửa `docs/`, sổ, `scripts/`, `design/`, `channel-k2/`, main, nhánh khác (nhánh v2 chỉ ĐỌC bằng `git archive` vào `/var/tmp`) |
| Khiếu nại trước phán quyết | chép K-LAI-3 ↔ KIEM-2-MUC + §8 trước khi phán | commit `47e0ef61` 17:21 UTC (bảng §8 nguyên văn, đoạn TU-LIEU-OMNI, C7, dòng lỗi k2check, căn cứ LUẬT E); phán quyết thêm sau đo |
| Chi phí | Claude mốc $3 (chặn $10), OpenAI mốc $2 (chặn $5), Gemini 0, giờ máy 5 h | **Claude API $1,419 · OpenAI $0,855 · Gemini $0** · giờ máy ≈ 2,1 h (§11) |
| Preflight | `set -o pipefail`; commit chỉ khi "— ĐẠT"; hook trước lần đẩy đầu | hook pre-commit + pre-push cài 17:15 (trước lần đẩy đầu 17:21); mọi commit/push "PREFLIGHT ĐẠT"; mã chưa khoá cất bằng stash khi commit (`day.sh`) |
| `lock.py` không `--verify` | đúng một lần ở bước khoá cuối | **đúng một lần** (18:53:09 UTC → `045b7bb7…`); preflight quét `checks/` TRƯỚC khi khoá — bắt 1 email giả trong selftest, sửa trước khoá (bài học K-1.17.7) |
| Force/amend/dừng hỏi | không | không |
| Đẩy ≤ 30 phút + CHECKPOINT | bắt buộc | `reports/k1178/CHECKPOINT.md`; **một lần trễ ≈ 22 phút** (18:00 → 18:52: không cất `checks/` được khi selftest đang đọc tệp) — §12 |

**Tóm tắt:**
1. **LUẬT E — hàng mới N2P-E** + tấm E chạy N2P-1…5 với lớp (a)-E (sông, bờ ±8 px, toà có tên/mái vòm/cầu, thuyền, lửa) thay cho lớp (a) cũ; AI vẽ lại mọi nhà thường không cần px/m; (f) chân trời mốc; (g) đêm không chữ/biển/logo. Đáp án P9-2026 (render V2 + 3 ảnh OpenAI + 7 biến đổi tổng hợp): **máy bắt đủ mọi lỗi lớp (a)/(f)/tháp bịa, 0 báo nhầm**; mô hình nhìn (đề bài `n2p-e-v2`) **bắt tháp bịa 2/2, chữ đêm 3/3, bóng ma mái vòm; 0 báo nhầm tháp/chữ đêm** — nhưng GPT báo nhầm "bờ sông bị đổi" ở 2/5 tấm đúng (§1).
2. **K-LAI-3 ↔ KIEM-2-MUC — LỖI LUẬT, sửa:** mức nen nhận Flash + tờ khung. v2: H1-15m THIẾU → ĐẠT; **H1-06b → (b) Flash LOẠI — chờ chủ dự án duyệt ngoại lệ** (`ngoai_le_duyet`).
3. **§8 kênh:** Q34 LỖI LUẬT → **ĐẠT**; Q26b LỖI LUẬT (trùng Q26b-K2) → **KHÔNG ÁP**; Q26b-K2 giữ luật, (a) đã sạch, **(e) LỖI KHAI** (`vung`), (b) 3D 74,2 % LỖI PHIM nhẹ; SACH-1 **LỖI KHAI** + khuôn log chữ khoảng/vai §17 mới; Q37 (d) **LỖI LUẬT** (miễn thẻ PP) → sửa; TU-LIEU-OMNI: **phán góc khung kề M-d < 1 s 3D sạch = ghép liền**; đếm trùng sửa (18 → 11), còn LỖI KHAI + LỖI PHIM H2-02.
4. **BIEN-CO-V — hiệu chuẩn lại trên T4 v2 KHÔNG ĐẠT** (thị sai TRUOT/XUONG, bản xem mã hoá thấp) → T4: BIEN-CO-V chỉ Cảnh báo, Q37 không cộng biến cố đo (D4).
5. Selftest `selftest_k1178` **69/69**; cũ đạt hết trên cây đã khoá (1 ca cũ đổi cơ chế, giữ kỳ vọng — §6). **LOCK 1.17.7 `3a53574c…` → 1.17.8 `045b7bb7…`**, `--verify` KHỚP. **T3 1.17.7 ↔ 1.17.8 giống hệt** (chỉ khác tiêu đề + nhãn phiên bản hàng LOCK — §9).

## 1. LUẬT E — N2+ toàn khung hiện đại (việc 1)
### 1.1 Luật (RULES-LL §1.17.8; `checks/ll/q_k1178.py`)
| Phần | Khai (tấm `n2p.tam[]`) | Đo | Mức |
|---|---|---|---|
| (k) điều kiện | `n2p_toan_khung_hien_dai: true`, `nam_min` (mặc định 2020; < 2020 → (k), dùng 2020) | năm ≥ nam_min VÀ `cu_may` CODINH (tấm hoặc log shot); không đủ → (k) + tấm đo như N2P thường | Chặn G2 |
| (i) | `mat_na` có lớp `nha_thuong` 215 cho nhà thường, `nha` 235 cho công trình có tên/cầu/tường | (a)-E = nha ∪ nước ∪ bờ ±8 px ∪ congsu/tau/lua/co/pin/nguoi (∪ `lop_a`) = 0/255 (N2P-1 (a)); mô hình: toà có tên mất/nhân đôi, vật (a)-E thêm/bớt → N2P-1 (b); nhà thường đổi KHÔNG tính | Chặn G2 |
| (iii) | — | T9c + mô hình (N2P-3); **T9b đất→nước chỉ in ở tấm E** (kính/mái xanh AI đọc thành nước: 26,6 % trên tấm đúng) | Chặn G2 |
| (iv) (v) | `n2p.video[]` khai `n2p_toan_khung_hien_dai: true` | 0 vật chuyển động thêm (N2P-4); nhấp nháy đo ngoài (a)-E (N2P-5) | Chặn G2 |
| (f) chân trời mốc | `toa_co_ten: [{ten, ma \| mau}]` + `mat_na_ct` (PNG mã 24 bit) — thiếu → THIẾU | (f1) mỗi toà ≥ 50 điểm @1080, thuộc (a)-E, ghép = render; (f2) toà cao không tên cao hơn toà có tên gần nhất ≥ 1 % khung (máy: cụm nét dọc trên trời render chạm chân trời; mô hình: `thap_bia`) | (f1) Chặn G2 · **(f2) (w) Cảnh báo** |
| (g) đêm | `dem: true` (không khai → render trung vị V < 0,40) | 0 chữ/biển/logo AI: máy PP-OCRv4 (chữ Latin mới so render, ngoài (a)-E, đọc ≥ 0,8, độ đặc < 0,8) + mô hình `chu`; ban ngày → (w) | Chặn G2 · Cảnh báo animatic |
Px/m: tấm E không qua BE-MAT-NHA (B) — nới theo căn cứ 00:07. Đề bài mô hình riêng `PROMPT_E` (`q_n2p_vision.soi(de=…)`, khoá bộ đệm theo SHA đề bài).

### 1.2 Đáp án (`do/e/`, tiêu chí đặt trước `do/e/TIEU-CHI.md`)
Render V2 P9-2026 (@1a911a01, SHA `04cc8142…`) + mặt nạ E (`matna-e.png`; hộp 8 công trình có tên lập bằng mắt — nhãn toa_1…7, không khẳng định tên OSM) + 3 ảnh OpenAI gpt-image-2.5 toàn khung không mặt nạ (`ai/P9-2026-E-{ngay,dem,xau}-ai.jpg`, lệnh `lenh-*.txt`; "xau" = lệnh cố ý đòi tháp mới + biển quảng cáo) + biến đổi tổng hợp (`ghep_e.py --bien`). **P1-2026 không làm được:** không có render V2 P1-2026 trong git (chỉ ảnh AI + ghép JPG của animatic v1); dựng lại cần dữ liệu LDN (OSM/LiDAR) — ngoài vùng/thời gian phiên. Bản đêm là **render ngày giảm sáng** (không phải render đêm V2) — nêu rõ.

### 1.3 Kết quả máy (không API)
| Tấm | Đáp án | N2P-1 (a) | (f1) | (f2) máy | (g)/(w) chữ máy |
|---|---|---|---|---|---|
| ngay, dem | ghép đúng | 0/255 ✓ | 0 ✓ | 0 ✓ | 0 ✓ (dem: 22 hộp cửa sổ sáng — không Latin) |
| xau | tháp bịa + 6 biển | 0/255 | 0 | **bắt** (24 cụm, cao hơn mốc 16–430 px) ✓ | **7 chữ** (citi, SAMSUNG, Spotify, Coca-Cola…) ✓ |
| ngay-thap_bia | tháp bịa cao hơn ≈ 80 px | 0 | 0 | **bắt** ✓ | 0 |
| ngay-thap_thap | tháp thấp hơn mốc | 0 | 0 | 0 ✓ | 0 |
| ngay-chu / dem-chu | 3 chữ dán | 0 | 0 | 0 | 1/3 (CAFE 24; HOTEL, BANK sót) — dem-chu → (g) |
| ngay-xoa_toa / doi_toa | toà toa_3 xoá / dời 30 px | **98 / 119 /255** ✓ | **bắt** ✓ | — | — |
| ngay-thuyen | thuyền trên sông | **180/255** ✓ (+ T9c bờ lấn 70 px) | — | — | — |
Ngưỡng (f2) `THAP_GX` chọn trên chính các tấm này (1,0 / 2,0 / 3,0 đều tách đúng; chọn 2,0) — không phải kiểm độc lập (ghi ở TIEU-CHI).

### 1.4 Mô hình nhìn (gpt-6.1-sol + claude-sonnet-5-5, 6 tấm)
- **Đề bài v1: Claude chỉ mở 2–3/10 ảnh ở 6/6 tấm (cả lần gọi lại KN-3) → THIẾU.** Đối chứng đề bài N2P cũ cùng ảnh: 10/10. → v2 thêm một câu buộc mở đủ 10 tệp (sửa tuân thủ đọc; phần phát hiện giữ nguyên chữ) → Claude 10/10 ở 6/6. Một lỗi mã lộ ra cùng lúc: bộ đệm rỗng `{}` là falsy → KeyError `qtd` (có từ 1.17.0 trong `q_n2p.kiem_tam`) — sửa.
- Kết quả v2 (≥ 1 mô hình, do_tin ≥ 0,5): **tháp bịa**: xau ✓ (cả hai), thap_bia ✓ (cả hai), 0 ở ngay/dem/thap_thap ✓. **Chữ**: dem-chu 3/3 chữ cả hai ✓ → (g); xau 6 biển cả hai ✓; 0 ở dem ✓; ngay: GPT báo 2 biển nhỏ không đọc được (ban ngày → (w)). **Toà có tên**: co_mat ở mọi tấm ✓; xau: **cả hai bắt mái vòm AI thứ hai cạnh mái vòm ghép lại (bóng ma)** ✓.
- **Vật chuyển động (iv):** GPT báo xe/người ở ngay/dem/thap_*; **soi bằng mắt (`do/e/` khung cắt): ảnh AI "ngay" có thật ô tô đỗ và người nhỏ** (lệnh cấm nhưng mô hình ảnh vẫn vẽ) → đúng, đáp án bằng mắt sửa sau soi (ghi rõ).
- **Báo nhầm:** GPT báo "bờ sông bị vẽ lại / đất↔nước" ở thap_bia và xau (N2P-1 (b), N2P-3 (b)) — bờ ngoài dải 8 px là lớp AI được phép; cùng ảnh nền "ngay" GPT không báo → báo nhầm, 2/5 tấm đúng. Đây là Chặn ở G2 → người đọc tờ so phải xét (D2).
- Chi phí mô hình E: GPT $0,628 · Claude $0,705 (gồm v1 lỗi) · q_thoi_dai $0,714 (sổ `reports/k1178/so-ai.jsonl`, 60 dòng; câu trả lời thô `do/e/vision/`).

## 2. Phán quyết khiếu nại ANIMATIC-T4-V2 §8 (việc 2–3; nguyên văn ở `checks-appeal.md`)
| Mục | Tái hiện (k2check 1.17.7, bản xem nối) | Tiêu chí đặt trước | Phán | Sửa |
|---|---|---|---|---|
| K-LAI-3 ↔ KIEM-2-MUC | THIẾU H1-06b, H1-15m (không tầng 2) | mức nen = Flash + tờ khung phải là tệp kiểm hợp lệ | **LỖI LUẬT** | nen → `kiem_t1` khi `to_khung` có thật; ngoại lệ `ngoai_le_duyet`. H1-15m ĐẠT; **H1-06b (b) LOẠI — LỖI PHIM chờ duyệt** |
| Q34 | 32 shot `minh_hoa`/`tu_lieu` "ngoài danh mục" | danh mục phải chứa loại mà luật T4 định nghĩa | **LỖI LUẬT** | T4 thêm minh_hoa/tu_lieu/that → ĐẠT |
| Q26b | 1 bối cảnh, trung tính 97,9 % | đo phải có nghĩa trên đường ghép thật | **LỖI LUẬT** (trùng Q26b-K2, không đọc được bối cảnh không hero) | T4 KHÔNG ÁP |
| Q26b-K2 | (a) 1–2 loại/nửa; (b) 3D 74,2 %; (e) 0 vùng | không nới ngưỡng chủ dự án (09/10) | (a) **LỖI LUẬT** (đã sửa cùng Q34); (b) **LỖI PHIM nhẹ** (Omni 20,7 % — C1); (c)(d)(e) **LỖI KHAI** | khai `vung` từng shot (khu nội dung, như T3: 38 vùng) |
| SACH-1 | "(c) không có log chữ" | trường đã có (1.16) → khai được | **LỖI KHAI** + **LỖI LUẬT nhỏ** (vai §17 chưa nhận) | khuôn khoảng + vai §17 |
| Q37 / Q37 (1.13) / NHIP-K2 (d) | khung tĩnh 8,92 s @12:35, 6,92 s @12:44 ở thẻ PP | miễn K1173-D6 đã duyệt cho (c) | **LỖI LUẬT** | miễn (d) trong thẻ PP ≤ 10 s (từ T4) |
| TU-LIEU-OMNI | 18 ghép liền | góc khung kề M-d: người xem thấy tư liệu → AI liền nhau? | **phán: CÓ tính ghép liền khi < 1 s 3D sạch**; đếm trùng **LỖI LUẬT**; thiếu `tu_lieu_lan` **LỖI KHAI**; H2-02 0,2 s **LỖI PHIM** | chỉ clip M-d gần nhất mỗi phía (18 → 11; khai thử → 9) |

## 3. Luật đổi / mới (1.17.8)
| Hàng | Tệp | Trường đọc | Ngưỡng | Mức |
|---|---|---|---|---|
| **N2P-E** (mới) + N2P-1…5 tấm E | `q_k1178`, `q_n2p` (`do_tam bo_a`, định tuyến tấm E, sửa KeyError), `q_n2p_vision` (`de`), `q_k1175` (BMN bỏ tấm E), `cap112`, `k2check` | §1.1 | §1.1 | Chặn (k)(f)(g) G2 · Cảnh báo animatic · (w) Cảnh báo |
| K-LAI-3 (minh hoạ), KIEM-2-MUC (b) | `q_lai.klai3_mh`, `q_k1177.kiem_2_muc` | `muc_kiem`, `kiem_t1`, `to_khung`, `ngoai_le_duyet` | Flash ĐẠT hoặc duyệt | như cũ |
| Q34 | `q_types.types_tap` | `type` | + minh_hoa, tu_lieu, that (T4) | như cũ |
| Q26b-K2 / Q26b | `q_k2var.shots`, `k2check` | `type`, `vung` | như cũ; Q26b T4 KHÔNG ÁP (mã thoát không tính) | như cũ |
| SACH-1 | `q_k116.text_frames/sach1`, `q_k1178.log_chu_khoang/sach1_s17` | `log_chu` khoảng; vai §17 | §17: thẻ ≤ 5 s; bộ đếm ≤ 2 từ; chú thích ≤ 6 từ ≤ 8 s; ≤ 2 lớp | Chặn (g) |
| Q37 / NHIP-K2 / Q37 (1.13) (d) | `q_nhip.q37`, `q_k1178.mien_d` | khối thẻ PP cuối | ≤ 10 s | như cũ |
| TU-LIEU-OMNI (b) | `q_k1176.tu_lieu_omni` | `tu_lieu_lan` | clip M-d gần nhất mỗi phía; 1 s 3D sạch | như cũ |
| BIEN-CO-V | `q_bcv.HIEU_CHUAN_T4`, `hc_tap_nay` | — | T4 chưa đạt → Cảnh báo; Q37 không cộng biến cố đo | Cảnh báo (T4) |
| — | `cinecheck/__init__.py` VERSION 1.17.8, `ll/RULES-LL.md` §1.17.8, `ll/selftest_k1178.py`, `ll/selftest_k1174.py` (cơ chế 1 ca) | — | — | — |

## 4. Cách khai cho phía dựng
- **Tấm E (episode.yaml `n2p.tam[]`):** `{id, shot, render, ghep, mat_na, nam: 2026, n2p_toan_khung_hien_dai: true, nam_min: 2020, cu_may: CODINH, dem: false|true, mat_na_ct: <PNG mã công trình>, toa_co_ten: [{ten: "St Paul's Cathedral", mau: [r, g, b]}, …], noi}`. Mặt nạ lớp: nhà thường `215,215,215` (`nha_thuong`), công trình có tên/cầu/tường `235` (`nha`) — trình dựng look2.js/look3.js đã có hai màu này (look3 cờ THU-B). **Mọi toà tháp có tên/mốc trong khung phải có trong `toa_co_ten`.** Ảnh AI: không gửi mặt nạ; lệnh cấm xe/người/thuyền/chữ (đáp án: mô hình ảnh vẫn vẽ xe đỗ — kiểm N2P-4 trước khi dùng); ghép lại lớp (a)-E nở 1 px. Video: `n2p.video[]` cùng cờ. Không khai `be_mat_nha_ai` cho tấm E.
- **Đoạn M-d mức nen:** giữ `muc_kiem: nen`, `kiem_t1`, `to_khung` (có thật); Flash LOẠI mà chủ dự án duyệt dùng → `ngoai_le_duyet: {nguoi_ky: "Chủ dự án (tác giả – đạo diễn)", vai: chu_du_an, ngay: "2026-10-26", ket_luan: chap_nhan}` (không email) + dòng AUTHORSHIP.
- **Đặc tả:** `type: minh_hoa | tu_lieu | that` hợp lệ; thêm `vung: <khu nội dung>` mỗi shot (vd `bankside`, `cheapside`, `st_pauls`, `thames_pool`… như T3), không dùng `noi` thay vùng.
- **Log chữ:** episode.yaml `log_chu: log-chu.json` với `{fmt: khoang, muc: [{t0, t1, role, s, px1080?, box?}]}` (giây phim). Vai: `year` (bộ đếm năm), `the_chuong`, `the_phuong_phap`, `where` (chip nơi ≤ 3 s), `the_nhan_vat` (≤ 5 s), `bo_dem_so` (số + ≤ 2 từ), `chu_thich_tu_lieu` (≤ 6 từ, ≤ 8 s). Ghép Python ghi trực tiếp từ danh sách lớp chồng (`ghep-log.json` the/dem/khac) — mẫu chuyển: `do/khai_thu_v2.py`.
- **Tư liệu/thẻ trong shot 3D:** `tu_lieu_lan: [{t0, t1, lop}]` (giây tuyệt đối, đúng cửa sổ hiện) cho MỌI lớp TL/KHAC/THE/MAP; cửa sổ phải cách ranh clip M-d ≥ 1 s.

## 5. Hiệu chuẩn BIEN-CO-V trên animatic T4 v2 (việc 4; `do/hieu_chuan_bcv_t4.py`, `do/hieu-chuan-bcv-t4.json`, `do/quang-that.json`)
Video: nối 4 bản xem v2 (`git archive 1a911a01 reports/animatic-t4-v2/xem` + ffmpeg concat copy) → 770,897 s, 640×360, **SHA-256 `d4b5d486e9bcdb9c33b334ea0dc30c66ccc0056db6097dea3e4c8f4e2b94fbb2`**. Log máy thật: `@1a911a01 channel-k2/k2c-t4-02/animatic2/log-may/*.json` (71 tệp). Tham chiếu: 96 ranh shot, 37 beat khớp đặc tả, **TĨNH THẬT** 18,1 s (H5-05a, H5-05b, H5-06: máy đứng, năm/lửa/mặt trời không đổi ≤ 2°, ngoài lớp chồng), **CHỈ MÁY THẬT** 23,9 s (H1-03 TRUOT 1647, H2-11 XUONG 1676, H5-02s TRUOT 1976, H5-07a DAY 2026), 12 clip tổng hợp từ 6 khung bản xem. Tiêu chí = K-1.17.4 §2 + hai tập thật (đặt trước; định nghĩa tập thật sửa 1 lần trước khi đo biến cố vì bản đầu cho 0 s tĩnh).
| θ, k | R cắt đầu/sau | R beat | Δt TV | tĩnh thật /phút đầu/sau | chỉ máy thật /phút đầu/sau | tổng hợp chỉ máy | vật đổi |
|---|---|---|---|---|---|---|---|
| 6, 2 | 100 / 97,9 | 94,4 / 100 | 0,04 | 0 / 26,5 | 15,2 / 142,5 | 7 | 5/6 |
| **8, 2** (T3) | 100 / 97,9 | 94,4 / 100 | 0,04 | 0 / **9,9** | 7,6 / **127,5** | **5** | **5/6** |
| 10, 2 | 100 / 97,9 | 94,4 / 100 | 0,04 | 0 / 0 | 0 / 123,8 | 1 | 3/6 |
| 12, 3 | 100 / 97,9 | 83,3 / 100 | 0,04 | 0 / 0 | 0 / 45,0 | 0 | 3/6 |
(Bảng đủ 8 ô lưới trong JSON.) **Không ô nào đạt.** Nguyên nhân đo được: (1) thị sai mạnh — H5-02s TRUOT tầm phố (mặt nhà quét ngang khung) 23 biến cố/6 s, H2-11 XUONG 11/5 s; (2) bản xem ≈ 66 kb/s phóng 3× cho clip tổng hợp → 5 báo nhầm (T3 master: 0); (3) H5-05b 3 biến cố trong 8 s tĩnh. **Kết luận: thước chưa đạt cho T4** → `HIEU_CHUAN_T4.dat = False` → theo chính luật 1.17.4, tập từ T4 BIEN-CO-V chỉ Cảnh báo và Q37 (b)(c) không cộng biến cố đo. Cần hiệu chuẩn lại trên master/animatic đủ bitrate + tách thị sai (D4).

## 6. Selftest
- `checks/ll/selftest_k1178.py` **69/69** (không mạng/API; ảnh tổng hợp 1920×1080 dựng trong mã; mô hình nhìn giả lập): LUẬT E 34 (ghép đúng, tấm thường cùng ảnh, (k) ×4, (i)/(f1), (f) THIẾU, (f2) ×3, (g) ×6, (iii) ×2, mô hình ×7, BMN, N2P-5 ×2, áp dụng) · K-LAI-3 nen 7 · KIEM-2-MUC 3 · Q34 3 · Q26b-K2 1 · SACH-1 9 · Q37 (d) 5 · TU-LIEU-OMNI 4 · BIEN-CO-V 4. Mỗi luật đổi/mới ≥ 1 ca đạt + ≥ 1 ca trượt.
- Trước khoá (`do/selftest-truoc-khoa.txt`): 17/17 bộ `checks/ll` đạt sau khi sửa **1 ca cũ**: `selftest_k1174` "BIEN-CO-V thước đạt + G2 → Chặn" bật/tắt `HIEU_CHUAN` trên tập T4 — T4 nay dùng `HIEU_CHUAN_T4` → ca đổi sang bật/tắt hiệu chuẩn CỦA TẬP (`q_bcv.hc_tap_nay`), **kỳ vọng giữ nguyên** (91/91).
- **Sau khoá** (`do/selftest-sau-khoa.txt`, LOCK KHỚP): k112 75/75 · k1121 48/48 · k1122 37/37 · k113 64/64 · k114 126/126 · k115 105/105 · k116 144/144 · k117 130/130 · k1172 74/74 · k1173 42/42 · k1174 91/91 · k1175 52/52 · k1176 62/62 · k1177 87/87 · **k1178 69/69** · k2 129/129 · ll 317/317 — **0 SAI**. Bộ L1 `checks/selftest/run_selftest.py` (cinecheck, không đổi trừ VERSION): xem dòng cuối tệp.

## 7. LOCK
Cũ 1.17.7 `3a53574ce8c2094e4f79bc1fac88cf3e6f7bbe61993ab5a1cf695834a2067b08` → **mới 1.17.8 `045b7bb7414364d4732fe22c4b643ae04d7a0e19ae25f0e839de149379d3185a`** (DATE_UTC 2026-10-25T18:53:09Z), `--verify` KHỚP. `lock.py` không cờ gọi **đúng một lần**.

## 8. Kết quả trên animatic T4 v2 (k2check `--cap --no-asr`, cùng video `d4b5d486…`)
Bảng đủ: `do/k2/k2check-1.17.7-t4.md`, `do/k2/k2check-1.17.8-t4.md`, khai thử `do/k2/k2check-1.17.8-t4e.md` (bản sao v2 + `do/khai_thu_v2.py`: log chữ khoảng từ ghep-log + `tu_lieu_lan` thẻ). RC cả ba: 1. TRƯỢT: 1.17.7 **10** (Q26b, Q34, Q37, NHIP-K2, Q26b-K2, Q37 (1.13), K-LAI-2, K-LAI-3, SACH-1, XEM-CAM) → 1.17.8 **8** (bỏ Q26b, Q34).
| Hàng | 1.17.7 | 1.17.8 | Lý do |
|---|---|---|---|
| Q26b | TRƯỢT | KHÔNG ÁP | §2 |
| Q34 | TRƯỢT (32 shot) | **ĐẠT** | §2 |
| K-LAI-3 | TRƯỢT — THIẾU 2 | TRƯỢT — (b) **H1-06b Flash LOẠI** (H1-15m ĐẠT) | §2 |
| KIEM-2-MUC | CẢNH BÁO (b) H1-06b | như cũ (chữ chỉ thêm đường ngoại lệ) | |
| Q26b-K2 | TRƯỢT (a)(a)(b)(e) | TRƯỢT (b) 3D 74,2 %, (e) 0 vùng — (a) sạch: 3d, minh_hoa 20,7 %, anh 2,9 %, the_so 2,1 % | §2 |
| Q37 / NHIP-K2 | TRƯỢT: TB 0,53 s (biến cố đo 1 621), (c) 20,21 s, (d) 10,38 s @4:29 | TRƯỢT: **TB 6,07 s, (c) 20,17 s** (chỉ 134 biến cố khai), (d) 10,38 s | BIEN-CO-V T4 chưa hiệu chuẩn → không cộng (§5) |
| Q37 (1.13) | TRƯỢT (d) 3 + (c) | TRƯỢT (b)(c); **(d) 8,92 s + 6,92 s thẻ PP miễn** | §2 |
| BIEN-CO-V | CẢNH BÁO (Chặn được ở G2) | CẢNH BÁO — "hiệu chuẩn T4 (1.17.8): KHÔNG ĐẠT" (G2 cũng chỉ Cảnh báo) | §5 |
| SACH-1 | TRƯỢT (c) không log | TRƯỢT (c) — thông báo nêu khuôn; **khai thử: (c) hết (202 mẫu log chữ), (g) 2 chú thích tư liệu 7 từ > 6** ("Hollar: London before the Fire (pub. 1666)", "Hollar: Old St Paul's from the east") | §4 |
| TU-LIEU-OMNI | CẢNH BÁO 18 | CẢNH BÁO 11; khai thử `tu_lieu_lan` thẻ → 9 (còn H1-06 0,6 s, H1-11 0,9 s, H3-05 0,6 s, H2-02 0,2 s < 1 s; H1-09 MAP, H1-18a, H4-02 chưa khai) | §2 |
| N2P-E | — | mới — KHÔNG ÁP (v2 chưa có tấm E) | |
| 58 hàng khác | — | giống hệt | |

## 9. So k2check 1.17.7 ↔ 1.17.8 trên bản cuối T3
Đầu vào như K-1.17.7 §1 (git archive @2a49e3ca + git cục bộ, `mk_tl.py` SHA `0ff3f0da…`, `mk_log_chu.py` SHA `17053dff…`, master LFS SHA `5b9f0bcc…` khớp). 1.17.7 chạy lại: **trùng hệt** `reports/k1177/do/k2check-1.17.7-t3.md` (trừ tiêu đề). 1.17.8 (cây đã khoá): **56/56 hàng giống hệt (kết quả, giá trị, lỗi, cấp, chữ ngưỡng); `diff` hai bảng chỉ khác dòng tiêu đề và nhãn phiên bản trong tên hàng LOCK** (`do/k2/k2check-1.17.{7,8}-t3.md`). Không có hàng mới (N2P-E chỉ hiện khi tập có `n2p`/`kenh2_tu_t4`).

## 10. Chỉ số trong ±5 % quanh ngưỡng (luật cứng — nêu tên)
- T4 v2 (bản xem, 1.17.8): **TL-1 (d) H1-18a trôi 2,06 %/s so 2 (+3 %)**; **Q37 (1.13) khung tĩnh 5,96 s @11:22 và @11:28 so 6 s (−0,7 %)**; **Q26b-K2 nửa đầu đúng 3 loại (= ngưỡng)**; thẻ chương 5 × 3,0 s = trần 3 s; thẻ PP1 9,0 s / PP2 7,0 s (cận); A1 −15,2 LUFS (cận dưới −15, bản xem).
- Hiệu chuẩn BIEN-CO-V: R cắt nửa sau 97,9 % so 95 % (+3 %).
- LUẬT E: tháp bịa máy nhỏ nhất bắt được cao hơn mốc 16 px so ngưỡng 10,8 px (1 % × 1080) — ảnh "xấu" (+48 %, ngoài ±5 %); tấm đúng không có cụm nào gần ngưỡng.

## 11. Chi phí thật
| Khoản | Số |
|---|---|
| OpenAI | **$0,855** = 3 ảnh gpt-image-2.5 ($0,227) + 12 lần gpt-6.1-sol mô hình nhìn E (6 v1 + 6 v2) ($0,628) — trong mốc $2 |
| Claude API | **$1,419** = claude-sonnet-5-5 mô hình nhìn E v1+v2+đối chứng ($0,705) + q_thoi_dai O2 ($0,714) — trong mốc $3 |
| Gemini / ElevenLabs / RunPod | 0 |
| Tải | master T3 LFS 1,79 GB (SHA khớp) |
| Giờ máy | ≈ 2,1 h (17:12 → ≈ 19:20 UTC): hiệu chuẩn BCV ≈ 12 phút (P 2), k2check 7 lượt (6–12 phút, P ≤ 2), selftest toàn bộ 2 lượt |
Sổ: `reports/k1178/so-ai.jsonl` (model, lệnh/đề bài + phiên bản, SHA vào/ra, usage, giá).

## 12. Sự cố
1. **Đề bài E v1: Claude mở 2–3/10 ảnh** (6/6 tấm, cả lần gọi lại) → v2 thêm câu buộc mở đủ; $0,13 phí lượt hỏng.
2. **KeyError `qtd`** khi bộ đệm mô hình rỗng (`(cache or {})` ghi vào dict tạm) — lỗi có từ 1.17.0 ở `q_n2p.kiem_tam`, lộ ra khi mô hình lỗi; sửa cả hai chỗ.
3. Hiệu chuẩn BCV lượt 1 dừng: khung "+97 s" vượt cuối phim (690 + 97 > 770) → sửa danh sách khung.
4. `setsid … & echo $! > tệp` hai lần ghi PID thất bại (thư mục chưa tạo khi chuyển hướng) — tiến trình vẫn chạy; chờ theo PID đọc lại từ `ps`/tệp kết quả, không dùng `pgrep -f`.
5. **Ba tiến trình nặng cùng lúc ≈ 1 phút** (selftest cinecheck `checks/selftest/run_selftest.py` + 2 k2check sau khoá) — dừng selftest cinecheck theo PGID ngay (lệch "P ≤ 2"); bộ này chạy lại sau khoá (§6).
6. **Đẩy trễ ≈ 22 phút** so mốc 30 phút (18:00 → 18:52): không cất `checks/` khi selftest đang đọc tệp.
7. Bản xem T4 cho khung tĩnh dài nhất khác bản animatic đủ của phiên dựng (10,38 s @4:29 so 8,96 s @12:35) — mọi so sánh 1.17.7 ↔ 1.17.8 trong báo cáo cùng video nên không ảnh hưởng hàng đổi.

## 13. Quyết định đề xuất (chủ dự án)
| # | Đề xuất | Phương án | Ưu | Nhược | Tác động | Rủi ro | Khuyến nghị |
|---|---|---|---|---|---|---|---|
| **K1178-D1** | Duyệt luật 1.17.8 (N2P-E + sửa §8) | A: duyệt. B: giữ 1.17.7 | A: E dùng được ở bản cuối; §8 hết trượt oan | A: phía dựng khai thêm (§4) | T4 bản cuối | thấp | **A** |
| **K1178-D2** | Báo nhầm mô hình ở N2P-1 (b)/N2P-3 (b) trên tấm E ("bờ sông bị vẽ lại" khi bờ ngoài 8 px là lớp AI) | A: giữ Chặn, người đọc tờ so xác nhận và ghi `ngoai_le` (như hiện). B: tấm E: (b) của mô hình chỉ Chặn khi hộp chạm (a)-E lõi (không chạm dải bờ ngoài) | A: chặt. B: bớt chặn oan | A: thêm chạm người mỗi tấm. B: bỏ sót sửa bờ thật nhỏ | P1/P9 2026 | B: lỗi bờ thật đã do (i) 0/255 + T9c bắt | **B ở phiên K kế** (cần thêm đáp án); tạm A |
| **K1178-D3** | Mức (f2) tháp bịa | A: Cảnh báo như lệnh. B: Chặn khi CẢ máy và mô hình cùng báo | A: theo lời chủ dự án (chấp nhận sai nhỏ). B: chặn tháp kiểu "Shard" chắc chắn | B: thêm một luật Chặn | P1/P9 | thấp | **A** |
| **K1178-D4** | BIEN-CO-V cho T4 | A: như khoá — chưa đạt: Cảnh báo + Q37 không cộng biến cố đo; hiệu chuẩn lại trên master/animatic đủ bitrate + tách thị sai (log máy) trước G2. B: giữ cộng biến cố đo dù chưa đạt | A: đúng luật 1.17.4; không "đạt giả" do thị sai | A: Q37 T4 phụ thuộc beats khai (v2: TB 6,07 s → phải khai beats / thêm biến cố) | T4 G2 | A: nhịp thật bị đánh giá thấp nếu khai thiếu | **A** |
| **K1178-D5** | H1-06b (Flash LOẠI, soi mắt ĐẠT) | A: chủ dự án duyệt ngoại lệ → `ngoai_le_duyet`. B: thay clip / về 3D | A: giữ điểm nhấn | A: hoạ tiết "giống chữ P" ở khung xa | 1 clip | thấp | theo xem của chủ dự án |
| **K1178-D6** | Vùng Q26b-K2 cho T4 | A: khai `vung` khu nội dung (như T3). B: K cho `noi` làm vùng | A: một nghĩa mỗi trường | A: thêm một trường khai | T4 | B: `noi` gác minh_hoa/tu_lieu → sai vùng | **A** |

## 14. Dòng sổ đề xuất (P ghi — phiên này không sửa sổ)
- **COST-LEDGER:** `2026-10-25/26 · K-1.17.8 · OpenAI $0,855 (3 ảnh đáp án E $0,227 + mô hình nhìn $0,628) · Claude API $1,419 (mô hình nhìn E $0,705 + q_thoi_dai $0,714) · Gemini 0 · ≈ 2,1 h máy · tải LFS 1,79 GB`.
- **AUTHORSHIP:** căn cứ 26/10 00:07 "Chọn hướng cho cảnh hiện đại: A+B+E (khuyến nghị)"; ghi khi chủ dự án trả lời K1178-D1…D6.
- **RIGHTS:** ảnh đáp án `reports/k1178/do/e/ai/*.jpg` — sinh bằng OpenAI gpt-image-2.5 từ render V2 của dự án; chỉ dùng kiểm, không vào sản phẩm.
- **Kinh thánh (P):** §15 thêm (k) LUẬT E — tấm nền AI toàn khung cho góc rộng hiện đại (≥ 2020) máy cố định: nhà thường AI vẽ lại; sông, bờ, toà có tên, cầu, thuyền, lửa ghép lại từ 3D; chân trời mốc; đêm không chữ/biển (RULES-LL §1.17.8; Kinh thánh không chép luật).
- **BAI-HOC-K2 (đề xuất):** (1) đề bài mô hình nhìn mới phải chạy đối chứng "đọc đủ ảnh" trước lượt đáp án; (2) bộ đệm `{}` là falsy — không viết `(cache or {})` khi cần ghi lại; (3) mô hình ảnh vẫn vẽ xe/người dù lệnh cấm — tấm E phải qua N2P-4 trước khi dùng; (4) thước biến cố video không hiệu chuẩn được trên bản xem 66 kb/s — giữ animatic đủ bitrate trong /var/tmp tới hết phiên K kế tiếp; (5) quét preflight `checks/` trước `lock.py` (bắt email giả trong selftest — đã áp).

## 15. Việc chờ chủ dự án
1. Trả lời **K1178-D1…D6** (§13) — khuyến nghị: D1 A, D2 A (B ở phiên K kế), D3 A, D4 A, D5 theo xem, D6 A.
2. Phiên P: merge `claude/k1178-t4-london-rules-pdjfmz` khi duyệt (nhánh này **không** merge); ghi sổ theo §14.
3. Phía dựng T4 (bản cuối): khai theo §4 — tấm E (mặt nạ nhà thường/có tên, `toa_co_ten`, `mat_na_ct`, `dem`), `vung`, `log_chu` khoảng, `tu_lieu_lan` cho mọi thẻ/khắc/bản đồ trong shot 3D (cách ranh M-d ≥ 1 s), rút chú thích tư liệu ≤ 6 từ, beats khai đủ cho Q37 (biến cố đo T4 chưa tính); H1-06b theo D5.

**DỪNG chờ chủ dự án.**
