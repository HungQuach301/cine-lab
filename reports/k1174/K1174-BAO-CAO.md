**Nhánh thật: `checks-1-17-4`** (đúng lệnh; harness gợi ý `ccr-db327794-xgq2sr` nhưng đẩy `checks-1-17-4`, như K-1.17.3). Gốc `origin/main` @ `c6a4772b` (LOCK 1.17.3 `d99af8f2…`). Không merge, không đụng `main` hay nhánh khác.

# Phiên K-1.17.4 — bộ kiểm cho T4 London trước animatic (D11, K117-D8, K1173-D6, Q2, §19) — BÁO CÁO

> Phiên K, 23/10/2026 ≈ 15:40–@@GIO_KET@@ UTC, chạy song song LOOK-T4 (không ghi vào `channel-k2/k2c-t4-02`, `design/k2v/ldn`, `scripts/k2ldn`, `reports/look-t4`; chỉ ĐỌC, và CHẠY bản sao trong thư mục tạm). Mọi số là số đo thật trong phiên; tệp số đo ở `reports/k1174/do/`.
> Email chủ dự án không có trong tệp, commit, header, URL, payload hay User-Agent nào (tải master bằng UA `CineLab-research (+https://github.com/HungQuach301/cine-lab)`). Không in/ghi khoá.

## 0. Khối điều lệ và tóm tắt
| Trường | Lệnh | Thực tế |
|---|---|---|
| Loại phiên | K-1.17.4 | đúng |
| Nhánh | `checks-1-17-4` từ `origin/main` @c6a4772b | đúng |
| Vùng sửa | `checks/**`, `reports/k1174/**`, `checks-appeal.md` (chỉ thêm mục phán quyết) | đúng. Không sửa `docs/`, sổ, `design/`, `scripts/`, `channel-k2/`, `main`. `BANG-SHOT-v1.json` (không có trong git) được sinh lại bằng BẢN SAO `bang_shot.py` trong thư mục tạm (bản `.md` sinh ra trùng bản trong git) |
| Chi phí | Claude API mốc $3 (chặn $10), OpenAI $1, Gemini $0, giờ máy 5 h; không `--o2-api` | **Claude API $0 · OpenAI $0 · Gemini $0** · giờ máy @@GIO_MAY@@ (§11) · không `--o2-api`, `--ml2-api`, `--n2p-vision` |
| Preflight | `set -o pipefail`, commit chỉ khi "— ĐẠT" | hook pre-commit + pre-push cài 15:50 trước lần đẩy đầu; mọi commit/push: `preflight: … — ĐẠT` + `lock.py --verify: KHỚP` + `PREFLIGHT ĐẠT` |
| `lock.py` không `--verify` | chỉ ở bước khoá cuối | **đúng một lần** (§10) |
| Đẩy ≤ 30 phút + CHECKPOINT | bắt buộc | 15:50, 15:56, 16:05, 16:18, 16:25, 16:38, 17:00, 17:16, … (mã chưa khoá đi dạng bản vá `reports/k1174/wip/`, `checks/` cất bằng stash khi commit — như K-1.17.3); `reports/k1174/CHECKPOINT.md` |
| Force / amend / dừng hỏi | không | không |

**Tóm tắt:**
@@TOM_TAT@@

## 1. D11 — phép (iii) N2P-3 trên T6 tiền kỳ T4: **LỖI ẢNH, giữ luật và ngưỡng 2 %**
Tái hiện: ghép lại 3 lượt từ đầu vào gốc trong git (`channel-k2/k2c-t4-02/ai/goc/T6-*`, SHA trong `do/d11-t6-iii.json`) bằng `scripts/k2ldn/t6_ghep.py` nguyên bản (thư mục tạm) → SHA ảnh ghép **trùng từng bit** sổ kiểm tiền kỳ (l1b `cb59edc0…`, l2 `5cc3a4b6…`, l3 `d5de5127…`); đo bằng `q_n2p.do_tam` 1.17.3 → **đúng số tiền kỳ**.

| Lượt | T9b nước→đất (luật) | Bỏ dải chân trời (vùng hợp lệ — cách sửa khiếu nại đề nghị) | Render thô | Dải "biển" chân trời góp vào tử số | Sát bờ ≤ 40 px | Giữa nước | Lý do mất "màu nước" | Đất→nước |
|---|---|---|---|---|---|---|---|---|
| l1 | 42,24 % | 43,32 % | 43,01 % | 4 403 / 258 471 điểm (1,7 %) | 38,08 % | 4,16 % | 86 % nhạt (S < 40) — cả sông thành xám | 0,00 % |
| **l2** | **2,42 %** | **2,67 %** | **2,67 %** | **0 điểm** | **1,49 %** | **0,93 %** | 85 % nhạt, 15 % lệch sắc | 0,01 % |
| l3 | 15,02 % | 15,02 % | 15,05 % | (render l3 không còn dải) | 11,01 % | 4,00 % | 83 % nhạt | **20,63 %** (2 mô hình cùng báo) |

- **Giả thuyết khiếu nại bị số đo bác:** dải "biển" ngoài hộp địa hình góp **0 điểm** vào lỗi lượt 2 — nó chỉ nằm ở mẫu số; đo đúng cách khiếu nại đề nghị (chỉ vùng hợp lệ, mặt nạ PNG) thì lượt 2 **tăng lên 2,67 %**. Mặt nạ JPEG chỉ ảnh hưởng (i): (iii) lượt 1 JPEG ↔ 1b PNG trùng 42,24 %; mặt nạ lượt 2 vốn là PNG.
- **Ảnh sai ở đâu (lượt 2, `do/d11-t6-l2-nuoc-thanh-dat.jpg`):** (1) **bờ bắc**: AI vẽ bãi/bến lấn ra sông 8–40 px so đường bờ của mặt nạ (1,49 % điểm nước; cụm lớn: x 157–233 y 717–780, x 529–624 y 722–769, x 666–715 y 694–735 bến nhô). Đường bờ là lớp dữ kiện hình học (§15 (a)) — lỗi thật, không phụ thuộc cách đo màu. (2) **giữa sông**: vệt phản chiếu nhà dọc và loé nhạt dưới ngưỡng loé (0,93 %).
- **Không nới, không sửa mã đo.** Phần (2) có thể là báo nhầm của thước màu với phản chiếu đúng vật lý (mặt nước thuộc lớp nền), nhưng chưa có khung đáp án phân biệt "phản chiếu" ↔ "bãi lấn"; không có căn cứ đo để miễn → đề xuất **K1174-D1** (§9). Phán quyết ghi `checks-appeal.md` "Phán quyết K — checks 1.17.4 · D11".
- **Hệ quả cho T4:** giữ "N2P ≤ 15 % thời lượng tới khi phép (iii) đạt" (Kinh thánh §15 (d) dòng D11) — tấm N2+ phải qua (iii) như luật hiện hành; cách sửa phía dựng: ghép lại dải bờ từ render (± 40 px quanh đường bờ, như lớp (a)), lệnh không xin "reflections", kiểm từng tấm trước khi dùng.

## 2. K117-D8 — thước BIẾN CỐ ĐO TRÊN VIDEO (`checks/ll/q_bcv.py`, hàng BIEN-CO-V)
@@THUOC@@

## 3. K1173-D6 — Q37 (c) miễn thẻ phương pháp
`q_k116.q37_mien` thêm khối thẻ PP liền nhau **kết ở cuối phim (± 0,5 s)** vào danh sách miễn (c) như khung neo/tấm im lặng (1.16); trần ≤ 10 s/thẻ (đã có — `MIEN_MAX`) và **≤ 2 thẻ/tập** (`q_nhip.PP_MIEN_N`; thừa → (c)). (b) TB và (d) khung tĩnh không đổi. Áp từ T3 (Q37, NHIP-K2, Q37 (1.13), BIEN-CO-V dùng chung danh sách miễn). Selftest: 2 thẻ × 9 s cuối phim → miễn; cùng tập không miễn → (c) 9 s (tái hiện lỗi cũ); thẻ 11 s, thẻ đầu phim, 3 thẻ → không miễn. Trên T3: @@T3_D6@@

## 4. Luật đổi / mới (1.17.4)
| Hàng | Tệp | Trường đọc | Ngưỡng | Mức | Căn cứ |
|---|---|---|---|---|---|
| N2P-3 (iii) | `q_n2p.py` (không đổi) | — | T9b ≤ 2 % mỗi chiều + 0 báo mô hình | như cũ (Chặn G2 / Cảnh báo animatic) | D11: LỖI ẢNH (§1) |
| **BIEN-CO-V** (mới) | `q_bcv.py`, `k2check.py`, `cap112.py` | master/animatic (`--master`); timeline (ranh shot); miễn `q37_mien` | (b) TB khoảng biến cố đo ≤ 3,5 s · (c) dài nhất ≤ 6 s (miễn khung neo/im lặng/thẻ PP ≤ 10 s) · (h) bắt ≥ 95 % ranh shot | Cảnh báo ở animatic; Chặn (b)(c)(h) ở G2 khi `HIEU_CHUAN` đạt @@HC_DAT@@ | Kinh thánh §4, §13.6 TL-1/TL-3; K116-D4; K117-D8 = A (23/10 17:42); Q7 (21:45) |
| Q37 / NHIP-K2 / Q37 (1.13) (b)(c) | `q_nhip.q37(bcv=)`, `q_k2var.nhip_k2`, `q_bcv.cho_q37` | biến cố đo | cộng biến cố đo khi tập từ T4 VÀ thước đạt hiệu chuẩn; không bao giờ nhận `su_kien` tự khai | như cũ (Chặn) | K117-D8 = A |
| Q37 / NHIP-K2 / Q37 (1.13) (c) | `q_k116.q37_mien`, `q_nhip.PP_MIEN_N` | đoạn thẻ PP (`the_phuong_phap`, id PP, part END, tiêu đề "How this film was made") | miễn khi khối thẻ kết ở cuối phim; ≤ 10 s/thẻ; ≤ 2 thẻ | như cũ | K1173-D6 = A (23/10 17:42); Q7 |
| MINH-HOA (a) | `q_k117.minh_hoa` | log shot `minh_hoa` | từ T4: **không trần cứng** (chỉ ghi %); T3 giữ ≤ 20 % | như cũ | Q2 (21:45) |
| N2P-6 (b) | `q_n2p.n2p6` | `minh_hoa` | **bỏ** (chỉ ghi %); (a) ≤ 50 %, (c) tổng AI ≤ 70 %, (d) không chồng: giữ | như cũ | Q2 (ii) giữ 70 % |
| **GEMINI-NGAN-SACH** (mới) | `q_k1174.gemini_ngan_sach` | episode.yaml `ngan_sach_gemini_usd`, `ngan_sach_gemini_moc_usd`, `so_ai_gemini` (hoặc `so_ai` lọc Gemini) — trường `usd` từng dòng | tổng ≤ ngân sách | (a) vượt, (u) thiếu `usd`: Chặn ở G2 · (k) thiếu khai, (m) vượt mốc: Cảnh báo · animatic: Cảnh báo | Q2 (i), Q1 ($25/$30) |
| **GOC-CAO-60** (mới) | `q_k1174.goc_cao_60` | log shot `goc: cao` + `tl: true` (TL-1); `log_may` → V7B-D1 theo khung | ≥ 60 % thân phim (trừ thẻ PP) | Chặn G2 / Cảnh báo animatic | Q2 (iii); §13.6 TL-1; V7B-D1 |
| **MAY-19** (mới) | `q_k1174.may19` | log shot `cu_may`, `log_may` (log.json `render_ldn.js`), `tieu_diem(_en)`, `khop_voi`, `diem_neo`, `hoa_s`, `lo_ra`, `chuong`, `ai_nen` | §19 (a) từng cú máy (bảng RULES-LL 1.17.4); (b) N2+ ⇒ CODINH ≤ 2 %/s; (c) KHOP ≤ 0,5 px, cùng FOV, hoà ≤ 1 s; (d) ≥ 4 loại/chương; (e) ≤ 2 liền; (f) THAP ≤ 12 %; (g) thiếu log → THIẾU | Chặn (a)–(g) G2 / Cảnh báo animatic; (w) luôn Cảnh báo | Kinh thánh §19 (a), §13.6 dòng "Từ T4"; D9 (≤ 3°/s) |
| **BAN-DO-12** (mới) | `q_k1174.ban_do_12` | `lop.MAP`, `lop.MAP3D` (hoặc `ban_do_s`) | MAP + MAP3D ≤ 12 %; mỗi lần bản đồ cổ ≤ 10 s | Chặn G2 / Cảnh báo animatic | §19 (b) |
| **TU-LIEU-10** (mới) | `q_k1174.tu_lieu_10` | `lop.TL`, `lop.KHAC`, `lop.THE` | ≤ 10 % | Chặn G2 / Cảnh báo animatic | §19 (c) |
| **AI-TU-LIEU** (mới) | `q_k1174.ai_tu_lieu` | `lop.MAP/KHAC/TL` × `minh_hoa/ai_image/ai_texture/ai_nen`; `sha_tu_lieu` × đầu vào sổ AI | (a) 0 shot tư liệu có AI (ai_nen phải khai `tu_lieu_chong_sau_ai`); (b) 0 dòng sổ AI có SHA tư liệu | Chặn G2 / Cảnh báo animatic | §19 (b)(c) "không AI lên tư liệu" |
| — | `cinecheck/__init__.py`, `RULES-LL.md`, `cap112.py` | — | VERSION 1.17.4; mục RULES-LL 1.17.4; cấp 7 hàng mới (tập `CONG`) | — | — |

**Cách đọc §19 (a) mà K đã chọn (cần chủ dự án xác nhận ở K1174-D3):** tốc độ = trung bình trượt 1 s, lấy lớn nhất trong shot; "tiêu điểm phóng ≤ 1,5 %/s chiều rộng" (DAY) đọc là **tiêu điểm dịch ≤ 1,5 % bề ngang/s** (cùng cách đo của bản thử T4 và `t4_do.py`) **và** tiến ≤ 1,5 % khoảng cách/s; tốc độ phóng ảnh tại tiêu điểm chỉ Cảnh báo. Khoảng "2–6 m/s" (CAU) và "150–300 m": chỉ cận trên 6 m/s Chặn; cận dưới và dải cao Cảnh báo. "Tiêu điểm giữ trong vùng 1/3" (VONG): Cảnh báo khi ra ngoài 1/6–5/6 khung. "0 px" (KHOP): ≤ 0,5 px trên 7 điểm (neo ± 25 % khoảng cách ngang/dọc/sâu — điểm nhìn luôn ở giữa khung nên một điểm không đủ). Luật (3) "điểm máy xương sống tái xuất mỗi hồi với khung y hệt" chưa thành chỉ số riêng (lệnh không giao; KHOP đo một phần).

## 5. Cách khai cho T4 (tên trường)
- **episode.yaml:** `kenh2_tu_t4: true` · `animatic: true` ở animatic · `ngan_sach_gemini_usd: 30` · `ngan_sach_gemini_moc_usd: 25` (Q1) · `so_ai_gemini: <so-ai-gemini.jsonl>` (mỗi dòng có `usd` = giá thật, `nha: gemini`, `model_req`, `input[].sha256`) · `so_ai` / `so_ai_openai` · `sha_tu_lieu: licenses/SHA256-TU-LIEU.txt` · `goc_toa_do: [532000, 180800]` (gốc toạ độ cảnh của `render_ldn.js`, như `t4_do.py`) · `mat_dat_m` (tuỳ chọn) · `log_shot`.
- **log shot (mỗi shot):** `shot`, `t0`, `t1`/`dur`, `chuong`, `goc` (`cao`/`thap`/…), `tl`, `cu_may` ∈ {CODINH, DAY, KEO, CAU, VONG, TRUOT, NGHIENG, THAP, XUONG, LAN, KHOP} hoặc MD/PP/THE, **`log_may`: log.json của `render_ldn.js` cho đúng shot (giữ lại — không xoá cùng `/var/tmp`)**, `tieu_diem_en: [E, N, h]` (hoặc `tieu_diem` toạ độ cảnh; mặc định điểm nhìn khung đầu), KHOP: `khop_voi`, `diem_neo`, `hoa_s`; KEO: `lo_ra`; `lop: {MAP, MAP3D, KHAC, TL, THE, N2P, MD: giây}` (như BANG-SHOT); `ai_nen`, `minh_hoa`, `ai_image`, `ai_texture`; `tu_lieu_chong_sau_ai` khi tư liệu chồng lên tấm N2+.
- **video:** BIEN-CO-V đo trên master/animatic được đưa vào `--master` (không cần khai gì thêm); ranh shot lấy từ timeline.
- **Bảng shot tiền kỳ** (`BANG-SHOT-v*.json` của `bang_shot.py`) đọc trực tiếp được làm `log_shot` để thử trước dựng (`q_k1174.chuan_ls`).

### 5.1 Thử trên đầu vào tiền kỳ T4 (`do/thu-t4-bang-shot.txt`; BANG-SHOT-v1 + sổ Gemini tiền kỳ + ngân sách Q1)
| Hàng | animatic | G2 | Giá trị |
|---|---|---|---|
| MAY-19 | CẢNH BÁO (50 THIẾU log khung + 2 (w) KEO thiếu `lo_ra`) | **TRƯỢT** (THIẾU log khung — đúng: chưa dựng) | 52 shot cú máy; loại/chương MÓC 4 · H1 6 · H2 9 · H3 5 · H4 7 · H5 7 (≥ 4 đạt); không chuỗi > 2; THAP 9,2 % |
| MAY-19 trên `t4-may.json` (bảng tóm tắt bản thử, `selftest_k1174`) | — | — | DAY 1,06 %/s **đạt**; VONG 12,64°/s **trượt** (> 3°/s); CAU 130,9 m/s, 4,77°/s **trượt**; KHOP 0,0 px **đạt** — khớp kết luận tiền kỳ (vượt do nén đoạn 3 s) |
| BAN-DO-12 | ĐẠT | ĐẠT | 55 s / 720 s = 7,64 %; bản đồ cổ mỗi lần ≤ 10 s (H1-09 9 s) |
| TU-LIEU-10 | ĐẠT | ĐẠT | 70 s = **9,72 %** (TL 14 · KHAC 13 · THE 43 s) — **sát ngưỡng (−2,8 %)** |
| AI-TU-LIEU | ĐẠT (khi khai `sha_tu_lieu`: 13 SHA × 4 dòng sổ AI → 0 trùng) | ĐẠT | không khai `sha_tu_lieu` → THIẾU (Chặn ở G2) |
| GEMINI-NGAN-SACH | ĐẠT | ĐẠT | 1 lệnh, $1,02 / $30 (mốc $25) |
| GOC-CAO-60 | ĐẠT | ĐẠT | 544 / 704 s thân phim = 77,3 % (bảng shot tự tính 75,56 % trên 720 s — khác mẫu số: K trừ thẻ PP như TL-1) |

## 6. Selftest
@@SELFTEST@@

## 7. So k2check 1.17.3 ↔ 1.17.4 trên bản cuối T3
@@SO_T3@@

## 8. LOCK
@@LOCK@@

## 9. Quyết định đề xuất (chủ dự án)
@@QD@@

## 10. Chỉ số trong ±5 % quanh ngưỡng (luật cứng — nêu tên)
@@SAT@@

## 11. Chi phí thật
@@CHIPHI@@

## 12. Dòng sổ đề xuất (phiên P sau ghi — phiên này không sửa sổ)
@@SO@@

## 13. Việc chờ chủ dự án
@@CHO@@
