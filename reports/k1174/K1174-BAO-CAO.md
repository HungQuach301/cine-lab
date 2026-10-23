**Nhánh thật: `checks-1-17-4`** (đúng lệnh; harness gợi ý `ccr-db327794-xgq2sr` nhưng đẩy `checks-1-17-4`, như K-1.17.3). Gốc `origin/main` @ `c6a4772b` (LOCK 1.17.3 `d99af8f2…`). Không merge, không đụng `main` hay nhánh khác.

# Phiên K-1.17.4 — bộ kiểm cho T4 London trước animatic (D11, K117-D8, K1173-D6, Q2, §19) — BÁO CÁO

> Phiên K, 23/10/2026 ≈ 15:40–18:05 UTC, chạy song song LOOK-T4 (không ghi vào `channel-k2/k2c-t4-02`, `design/k2v/ldn`, `scripts/k2ldn`, `reports/look-t4`; chỉ ĐỌC, và CHẠY bản sao trong thư mục tạm). Mọi số là số đo thật trong phiên; tệp số đo ở `reports/k1174/do/`.
> Email chủ dự án không có trong tệp, commit, header, URL, payload hay User-Agent nào (tải master bằng UA `CineLab-research (+https://github.com/HungQuach301/cine-lab)`). Không in/ghi khoá.

## 0. Khối điều lệ và tóm tắt
| Trường | Lệnh | Thực tế |
|---|---|---|
| Loại phiên | K-1.17.4 | đúng |
| Nhánh | `checks-1-17-4` từ `origin/main` @c6a4772b | đúng |
| Vùng sửa | `checks/**`, `reports/k1174/**`, `checks-appeal.md` (chỉ thêm mục phán quyết) | đúng. Không sửa `docs/`, sổ, `design/`, `scripts/`, `channel-k2/`, `main`. `BANG-SHOT-v1.json` (không có trong git) được sinh lại bằng BẢN SAO `bang_shot.py` trong thư mục tạm (bản `.md` sinh ra trùng bản trong git) |
| Chi phí | Claude API mốc $3 (chặn $10), OpenAI $1, Gemini $0, giờ máy 5 h; không `--o2-api` | **Claude API $0 · OpenAI $0 · Gemini $0** · giờ máy ≈ 2,5 h đồng hồ container (§11) · không `--o2-api`, `--ml2-api`, `--n2p-vision` |
| Preflight | `set -o pipefail`, commit chỉ khi "— ĐẠT" | hook pre-commit + pre-push cài 15:50 trước lần đẩy đầu; mọi commit/push: `preflight: … — ĐẠT` + `lock.py --verify: KHỚP` + `PREFLIGHT ĐẠT` |
| `lock.py` không `--verify` | chỉ ở bước khoá cuối | **đúng một lần**, 17:49:12 UTC (§8) |
| Đẩy ≤ 30 phút + CHECKPOINT | bắt buộc | 15:50, 15:56, 16:05, 16:18, 16:25, 16:38, 17:00, 17:16, 17:36, 17:50 (mã khoá), commit cuối (mã chưa khoá đi dạng bản vá `reports/k1174/wip/`, `checks/` cất bằng stash khi commit — như K-1.17.3); `reports/k1174/CHECKPOINT.md` |
| Force / amend / dừng hỏi | không | không |

**Tóm tắt:**
1. **D11 = LỖI ẢNH, giữ luật và ngưỡng 2 %.** Tái hiện khớp từng bit; giả thuyết "dải biển giả ngoài hộp + mặt nạ JPEG" bị số đo bác: dải góp **0 điểm** vào lỗi lượt 2, đo đúng cách khiếu nại đề nghị (vùng hợp lệ, PNG) → **2,67 %** (vẫn vượt). Lỗi thật: bờ bắc dịch vào sông 8–40 px (1,49 %) + phản chiếu/nhạt màu giữa sông (0,93 %). Câu hỏi "phản chiếu có phải báo nhầm" → K1174-D1.
2. **K117-D8: thước biến cố đo trên video `q_bcv.py` (hàng BIEN-CO-V) — hiệu chuẩn trên master T3 ĐẠT** (θ 8/255, k 2, lưới 8×6, neo ≤ 3 s): R cắt 100 %, R beat 90,8 % / 98,2 % (nửa chỉnh / nửa kiểm), sai số giờ trung vị 0,04–0,05 s, 0 báo nhầm (quãng tĩnh theo ô + clip chỉ máy đi), bắt 6/6 vật đổi tổng hợp. Giới hạn: vật < ≈ 1–2 % khung không thành biến cố (10/153 beat sót đều là khói bếp/tàu xa). Mức: Cảnh báo ở animatic, Chặn ở G2; từ T4 biến cố đo cộng vào Q37 (b)(c).
3. **K1173-D6:** Q37 (c) miễn khối thẻ PP cuối phim (≤ 2 × ≤ 10 s). **Q2 vào luật:** từ T4 bỏ trần 20 % M-d (MINH-HOA (a), N2P-6 (b)); mới **GEMINI-NGAN-SACH** và **GOC-CAO-60**; T3 không hồi tố. **§19 thành chỉ số:** **MAY-19** (tốc độ từng cú máy từ log khung `render_ldn.js`, N2+ ⇒ CODINH, KHOP ≤ 0,5 px, ≥ 4 loại/chương, ≤ 2 liền, THAP ≤ 12 %), **BAN-DO-12**, **TU-LIEU-10**, **AI-TU-LIEU**.
4. **Selftest:** `selftest_k1174.py` **91/91**; cũ k112 75 · k1121 48 · k1122 37 · k113 64 · k114 126 · k115 105 · k116 144 · k117 130 · k1172 74 · k1173 42 · k2 129 · ll 317 — đạt hết trên cây đã khoá; **một kỳ vọng cũ đổi có căn cứ** (selftest_k117: N2P-6 minh hoạ 21 % — Q2).
5. **T3 1.17.3 ↔ 1.17.4:** 51/54 hàng giống hệt; đổi đúng phạm vi: Q37/NHIP-K2/Q37 (1.13) (c) "9,0 s từ PP1" hết (miễn thẻ PP) → lộ (c) 8,03 s ở N5_5 (vẫn TRƯỢT như trước, số lỗi 71/71/78 không đổi); + BIEN-CO-V (T3: (c) 19,62 s từ 1:02,6) + "1.17.4 (T4) KHÔNG ÁP". Lượt 1.17.3 tái lập **trùng hệt** bảng của K-1.17.3.
6. **LOCK 1.17.3 `d99af8f2…` → 1.17.4 `08486eb2…`**, `--verify` KHỚP. Chi phí API $0.

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
**Định nghĩa "biến cố thấy được" (đo trên video, không nhận số tự khai):** video → xám 256×144, mờ σ 2. Mỗi cặp khung liền: chuyển động máy toàn cục = homography (điểm góc Shi–Tomasi + Lucas–Kanade + RANSAC 2 px); không khớp được (< 12 điểm hoặc < 30 % điểm theo) hoặc phần dư sau bù > 18/255 → **cắt** (cũng là biến cố). Lưới **8 × 6 ô**; mỗi ô giữ một khung neo (tuổi ≤ **3 s**); mỗi 0,25 s so khung hiện tại với khung neo của ô đã bù máy (homography gộp) và bù sáng toàn khung (g·x + o); phần dư làm mờ σ 1,5, lấy TB trong ô. Ô **đổi** khi phần dư ≥ **θ = 8/255** VÀ ≥ **k = 2 ×** trung vị các ô (đổi CỤC BỘ, không phải trôi/thị sai toàn khung) → biến cố; neo lại ô đó + 8 ô kề (một vật = một biến cố). Ô ra khỏi khung do máy đi, hoặc neo quá 3 s → neo lại, KHÔNG là biến cố. Khung trống (độ lệch chuẩn < 3) không theo. Gộp biến cố cách < 0,25 s (như Q37). Nghĩa: **"một vùng cỡ ô (≈ 1/48 khung, 240 × 180 px ở 1080p) đổi ≥ 8/255 trung bình trong ≤ 3 s, sau khi trừ chuyển động máy"**; lửa lan/nhà mọc liên tục cho biến cố lặp theo tốc độ đổi.

**Hiệu chuẩn trên master T3 bản cuối** (SHA `5b9f0bcc…`; `reports/k1174/do/hieu_chuan_bcv.py`, kết quả `do/hieu-chuan-bcv.json`). Tham chiếu không tự khai: **72 cắt** (ranh shot timeline từ đặc tả + ranh góc máy `goc_may` + beat `cut` khớp đặc tả), **153 beat đã khớp mốc đặc tả** 1.17.3 (phần Q37 (a) nhận), 516 mốc đặc tả (chỉ báo độ chính xác), **2 quãng tĩnh theo ô** (610,0 s 9,08 s; 717,0 s 8,0 s — mọi ô lệch < 3/255), **12 clip tổng hợp** từ 6 khung T3 (10 s, máy 2D trượt 2 %/s + phóng 1,5 %/s + quay 0,5°/s; 6 clip có thêm một ô 96 px đổi ở 5,0 s). Tiêu chí đặt trước lượt đo đầy đủ: R cắt ≥ 95 %, R beat ≥ 70 %, Δt trung vị ≤ 0,25 s, báo nhầm ≤ 1/phút ở quãng tĩnh và 0 trên clip chỉ máy đi, bắt 6/6 vật đổi. Chọn (θ, k) trên nửa đầu phim, kiểm trên nửa sau.

| θ | k | Nửa đầu: R cắt · R beat · Δt TV · báo nhầm tĩnh | Nửa sau: R cắt · R beat · Δt TV · báo nhầm tĩnh (16,1 s) | Clip: báo nhầm chỉ máy · bắt vật đổi | Đạt (đầu/sau) |
|---|---|---|---|---|---|
| 6 | 2 | 100 · 90,8 · 0,042 · 0 | 100 · 98,2 · 0,053 · 0 | 3 · 6/6 | không/không |
| 6 | 3 | 100 · 89,8 · 0,057 · 0 | 100 · 94,5 · 0,083 · 0 | 3 · 6/6 | không/không |
| **8** | **2** | **100 · 90,8 · 0,050 · 0** | **100 · 98,2 · 0,042 · 0** | **0 · 6/6** | **ĐẠT/ĐẠT — chọn** |
| 8 | 3 | 100 · 87,8 · 0,080 · 0 | 100 · 94,5 · 0,041 · 0 | 0 · 6/6 | đạt/đạt |
| 10 | 2 | 100 · 85,7 · 0,042 · 0 | 100 · 96,4 · 0,067 · 0 | 0 · 5/6 | không/không |
| 10 | 3 | 100 · 85,7 · 0,065 · 0 | 100 · 92,7 · 0,042 · 0 | 0 · 5/6 | không/không |
| 12 | 2 | 100 · 83,7 · 0,042 · 0 | 100 · 94,5 · 0,071 · 0 | 0 · 4/6 | không/không |
| 12 | 3 | 100 · 83,7 · 0,058 · 0 | 100 · 92,7 · 0,042 · 0 | 0 · 4/6 | không/không |

**Sai số (θ 8, k 2):** giờ biến cố so cắt/beat: trung vị **0,04–0,05 s** (≈ 1 khung; bước đo 0,25 s là cận trên); R cắt 100 % (72/72); R beat 90,8 % (nửa đầu, 98 beat) / 98,2 % (nửa sau, 55 beat) — **10/153 beat sót**, đều là vật nhỏ ở tầm cao: khói bếp ×5 (N1_1, N1_2 ×3, N4_3), tàu tới vị trí ×2 (N1_1, N2_8), bụi đào hầm (N2_10), khói bắt đầu (N2_10), pin nổi khai hoả (H2). Độ chính xác so mốc đặc tả 40,3 % / 33,9 % so mức ngẫu nhiên 37,9 % / 31,6 % — **không dùng được làm tiêu chí** (biến cố đo dày ≈ 2,2/s trên T3 vì thời gian chạy liên tục giữa các mốc; mốc không phủ đổi liên tục) — chỉ báo.
**Những gì đã đổi giữa các lượt (minh bạch):** lượt 1 (mờ khung σ 1) KHÔNG đạt: clip chỉ máy đi báo nhầm 14–201 biến cố/60 s (răng cưa chi tiết khi máy phóng/quay). Sửa trong lượt 2–3: (a) clip tổng hợp cắt giữa khung lớn (bản đầu dùng biên phản chiếu — lỗi của clip thử); (b) chuẩn "tĩnh" = tĩnh THEO Ô (23/25 quãng tĩnh Q37 1.13 có ô đổi tới 52/255 — đổi cục bộ thật mà TB toàn khung không thấy); (c) mờ khung σ 2; (d) neo lại 8 ô kề (selftest lộ đếm trùng 1 vật ở ô kề). Tiêu chí ĐẠT không đổi giữa các lượt; lưới (θ, k) thu về {6, 8, 10, 12} × {2, 3} sau lượt 1 (θ 4 và k 1,5 báo nhầm nhiều nhất ở lượt 1).
**Giới hạn đã biết:** (1) vật nhỏ hơn ≈ 1–2 % khung (tàu xa vài px, khói mảnh, chữ số bộ đếm) không thành biến cố — thử lưới mịn 16 × 9 (384×216): ở mọi θ không báo nhầm, đoạn N1_2 1:02,6–1:22,2 vẫn 0 biến cố (`thu` trong CHECKPOINT); (2) clip tổng hợp dùng chung hai nửa (chỉ quãng tĩnh và cắt/beat chia nửa); quãng tĩnh theo ô chỉ ở nửa sau (16,1 s); (3) thị sai mạnh (cẩu thấp sát nhà) chưa có tham chiếu riêng — điều kiện "cục bộ ≥ 2 × trung vị" chặn phần lớn; (4) chi phí đo ≈ 3–4 phút/phim 12 phút (CPU container).
**Mức:** BIEN-CO-V Cảnh báo ở animatic; **Chặn (b)(c)(h) ở G2** vì `HIEU_CHUAN` đạt — với điều kiện thêm (h) trên chính tập (bắt ≥ 95 % ranh shot), không đạt (h) thì tự hạ Cảnh báo. Q37/NHIP-K2/Q37 (1.13) **từ T4** cộng biến cố đo vào (b)(c). T3: BIEN-CO-V là hàng mới chỉ để ghi (T3 đã phát hành; G2 T3 không chạy lại).

## 3. K1173-D6 — Q37 (c) miễn thẻ phương pháp
`q_k116.q37_mien` thêm khối thẻ PP liền nhau **kết ở cuối phim (± 0,5 s)** vào danh sách miễn (c) như khung neo/tấm im lặng (1.16); trần ≤ 10 s/thẻ (đã có — `MIEN_MAX`) và **≤ 2 thẻ/tập** (`q_nhip.PP_MIEN_N`; thừa → (c)). (b) TB và (d) khung tĩnh không đổi. Áp từ T3 (Q37, NHIP-K2, Q37 (1.13), BIEN-CO-V dùng chung danh sách miễn). Selftest: 2 thẻ × 9 s cuối phim → miễn; cùng tập không miễn → (c) 9 s (tái hiện lỗi cũ); thẻ 11 s, thẻ đầu phim, 3 thẻ → không miễn. Trên T3: Q37, NHIP-K2, Q37 (1.13): (c) "9,0 s từ PP1 745,00 s" **hết**; khoảng dài nhất còn lại **8,03 s từ N5_5 698,04 s** (trước bị che vì luật chỉ in khoảng dài nhất) → các hàng vẫn TRƯỢT, số lỗi không đổi (71 · 71 · 78).

## 4. Luật đổi / mới (1.17.4)
| Hàng | Tệp | Trường đọc | Ngưỡng | Mức | Căn cứ |
|---|---|---|---|---|---|
| N2P-3 (iii) | `q_n2p.py` (không đổi) | — | T9b ≤ 2 % mỗi chiều + 0 báo mô hình | như cũ (Chặn G2 / Cảnh báo animatic) | D11: LỖI ẢNH (§1) |
| **BIEN-CO-V** (mới) | `q_bcv.py`, `k2check.py`, `cap112.py` | master/animatic (`--master`); timeline (ranh shot); miễn `q37_mien` | (b) TB khoảng biến cố đo ≤ 3,5 s · (c) dài nhất ≤ 6 s (miễn khung neo/im lặng/thẻ PP ≤ 10 s) · (h) bắt ≥ 95 % ranh shot | Cảnh báo ở animatic; Chặn (b)(c)(h) ở G2 khi `HIEU_CHUAN` đạt (**đạt** — §2) | Kinh thánh §4, §13.6 TL-1/TL-3; K116-D4; K117-D8 = A (23/10 17:42); Q7 (21:45) |
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
`checks/ll/selftest_k1174.py` — **91/91** (`do/selftest-k1174-chi-tiet.txt`; ≈ 25 s; không mạng/API; video thử dựng tại chỗ từ vân tổng hợp): BIEN-CO-V 10 (tĩnh → 0; chỉ máy đi trượt + phóng + quay → 0; vật đổi ở 5,0 s → bắt ±0,25 s, không thừa; cắt; 6 vật mỗi 2 s → 6/6; (b)(c) đạt/trượt; miễn thẻ PP; (h) đạt/trượt) · cấp 5 (BIEN-CO-V chưa/đã hiệu chuẩn, animatic; MAY-19 animatic/G2) · Q37 11 (bcv tập T4 + thước đạt → cộng; T3 / chưa đạt → không; `su_kien` tự khai không nhận; K1173-D6 miễn 2 thẻ × 9 s; trước 1.17.4 → (c) 9 s; 11 s / đầu phim / 3 thẻ → không miễn) · MINH-HOA 2 · N2P-6 2 · MAY-19 39 (9 cú máy × đạt + trượt trên log khung tổng hợp định dạng render_ldn.js; N2+; KHOP 0 px / lệch 2 m / FOV khác; chương 4/3 loại; 2/3 liền, MD ngắt chuỗi; THAP 12 %/13 %; thiếu log, thiếu cu_may; (w) KEO; **bảng tóm tắt tiền kỳ T4 thật `t4-may.json`**: DAY đạt, VONG 12,64°/s trượt, CAU trượt, KHOP 0,0 px đạt, đủ ở animatic / THIẾU ở G2) · BAN-DO-12 3 · TU-LIEU-10 2 · AI-TU-LIEU 5 · GEMINI-NGAN-SACH 7 · GOC-CAO-60 4 · áp dụng 1. Mỗi luật đổi/mới ≥ 1 ca đạt + ≥ 1 ca trượt.
Selftest cũ trên cây đã khoá (`do/selftest-sau-khoa.txt`): k112 75/75 · k1121 48/48 · k1122 37/37 · k113 64/64 · k114 126/126 · k115 105/105 · k116 144/144 · k117 130/130 · k1172 74/74 · k1173 42/42 · k2 129/129 · ll 317/317 — mã thoát 0 hết. Kỳ vọng đổi: **một** (selftest_k117 "minh hoạ 21 % → (b)" → "không (b)" vì Q2; ghi ngay trong ca).

## 7. So k2check 1.17.3 ↔ 1.17.4 trên bản cuối T3
Đầu vào như K-1.17.3: `git archive origin/main channel-k2/k2c-t3-01 reports/animatic-t3-v2 AUTHORSHIP.md RIGHTS.md` (thư mục tạm), timeline tổng hợp từ đặc tả (`reports/k1172/do/mk_tl.py`, SHA `0ff3f0da…`, 761,9998 s), log chữ tổng hợp (`reports/k1173/do/mk_log_chu.py`), master thật LFS `release-k2-t3-g2` (SHA-256 `5b9f0bcc…` khớp). Lệnh: `k2check.py <tạm>/…/cuoi/episode.yaml --tl timeline.json --master <tuyệt đối>/k2-t3-v1-master.mp4 --cap --no-asr`. 1.17.3 chạy từ worktree thưa `origin/main` (LOCK 1.17.3 KHỚP) — **trùng hệt bảng K-1.17.3** (`reports/k1173/do/k2check-1.17.3-t3.md`) ở mọi hàng và giá trị. Bảng đủ: `do/k2check-1.17.3-t3.md`, `do/k2check-1.17.4-t3.md`, `do/so-1173-1174.md`.

| Hàng | 1.17.3 | 1.17.4 | Lý do |
|---|---|---|---|
| Q37 | TRƯỢT 71 — (c) 9,0 s từ PP1 · (d) 9,46 s | TRƯỢT 71 — **(c) 8,03 s từ N5_5 698,04 s** · (d) 9,46 s; miễn 8 khoảng (6 khung neo + 2 thẻ PP) | K1173-D6 |
| NHIP-K2 | TRƯỢT 71 (như Q37) | TRƯỢT 71 (như Q37) | K1173-D6 |
| Q37 (1.13) | TRƯỢT 78 — (c) 9,0 s PP1 · (d) ×8 | TRƯỢT 78 — (c) 8,03 s N5_5 · (d) ×8 | K1173-D6 |
| **BIEN-CO-V** (mới) | — | **TRƯỢT** (Chặn ở G2): 1 987 biến cố đo (gộp 1 690; TB 0,45 s), ranh shot 44/44, **(c) 19,62 s không biến cố đo từ 1:02,6** (N1_2: khói bếp mảnh, tàu xa, bộ đếm 1→2 Aug) | K117-D8 (T3 đã phát hành — chỉ ghi) |
| 1.17.4 (T4) (mới) | — | KHÔNG ÁP (tập trước T4 — Q2 không hồi tố) | Q2 |
| LOCK | ĐẠT (1.17.3) | ĐẠT (1.17.4 KHỚP) | — |
| 51 hàng còn lại (Q26b … N2P-1…6, MINH-HOA, EO-DAT-R1…R4, A1–A13) | — | **giống hệt** (kết quả + giá trị) | — |
Mã thoát cả hai: 1 (TRƯỢT — còn Q37 (a)(c)(d), EO-DAT-R3 (a), XEM-CAM, K-LAI-2 (d); thêm BIEN-CO-V ở 1.17.4). Không hàng nào chuyển ĐẠT → TRƯỢT ngoài hàng mới BIEN-CO-V. Thời gian: 11 m 49 s (1.17.3) · 10 m 12 s (1.17.4 cuối, có đo thước video).

## 8. LOCK
- **Cũ:** 1.17.3 `d99af8f22d5e7c0ba3469c4b95bcc01296f72f64d9e72d21ed3fb897549ba10b` (2026-10-23T06:58:54Z).
- **Mới:** **1.17.4 `08486eb21dc55749115849e9691a4321458ecf8411e0562b141506f77227dd6d`** (DATE_UTC 2026-10-23T17:49:12Z). `python3 -I checks/lock.py` không cờ gọi **đúng một lần** (17:49, sau selftest_k1174 91/91); `--verify` → **KHỚP** (ngay sau khoá; mọi commit/push; hàng LOCK k2check 1.17.4 cuối "KHỚP"; sau selftest đủ).
- Tệp đổi trong `checks/`: `LOCK`, `cinecheck/__init__.py`, `ll/RULES-LL.md` (mục 1.17.4), `ll/cap112.py`, `ll/k2check.py`, `ll/q_k116.py`, `ll/q_k117.py`, `ll/q_k2var.py`, `ll/q_n2p.py`, `ll/q_nhip.py`, `ll/selftest_k117.py` (1 kỳ vọng); mới `ll/q_bcv.py`, `ll/q_k1174.py`, `ll/selftest_k1174.py`.
- Ngoài `checks/`: `checks-appeal.md` (mục "Phán quyết K — checks 1.17.4 · D11"), `reports/k1174/**`.

## 9. Quyết định đề xuất (chủ dự án)
| # | Đề xuất | Phương án | Ưu | Nhược | Tác động | Rủi ro | Khuyến nghị |
|---|---|---|---|---|---|---|---|
| **K1174-D1** | N2P-3 (iii) với phản chiếu thật trên mặt nước | A: phiên K riêng dựng khung đáp án (bãi/bờ lấn chèn + phản chiếu thật từ tấm AI đạt mắt) rồi mới quyết miễn phản chiếu; tới lúc đó luật giữ. B: giữ luật vĩnh viễn; phía dựng tránh phản chiếu. C: miễn ngay vùng "giữa nước" | A: quyết bằng số đo; không nới bừa. B: đơn giản. C: tấm T6 lượt 2 qua ngay | A: thêm một phiên K (≈ 1–2 h, ≈ $1–2 OpenAI). B: mặt nước kém thật. C: **trái lệnh** (phần đo hợp lệ vẫn 2,67 %), bãi lấn giữa nước lọt | T4 N2+ (đang ≤ 15 %) | A: đáp án chưa phủ đủ kiểu lỗi. C: lỗi đổi vùng lọt G2 | **A** |
| **K1174-D2** | Duyệt định nghĩa + mức BIEN-CO-V (θ 8/255, k 2, ô 1/48 khung, đổi trong ≤ 3 s; Chặn ở G2 từ T4) | A: duyệt như hiệu chuẩn (vật < 1–2 % khung không là biến cố). B: duyệt, nhưng (c) Chặn chỉ khi > 10 s, 6–10 s Cảnh báo cho tới khi hiệu chuẩn lại trên animatic T4. C: chỉ báo mọi cổng | A: số đo thật thay số tự khai; khớp "thấy được" trên điện thoại. B: an toàn với shot chỉ có đổi nhỏ (khói mảnh, tàu xa). C: không chặn oan | A: shot timelapse chỉ có vật nhỏ đổi sẽ trượt (c) (T3 N1_2 19,6 s). B: nới phần 6–10 s. C: Q37 (b)(c) T4 lại phụ thuộc beat khai | Q37/BIEN-CO-V mọi tập từ T4 | A: chặn oan nhịp tinh tế. B/C: nhịp thưa lọt | **A**, kèm hiệu chuẩn lại trên animatic T4 (log máy thật) trước G2 |
| **K1174-D3** | Cách đọc §19 (a) (§4 cuối bảng): DAY "tiêu điểm phóng ≤ 1,5 %/s" = tiêu điểm dịch ≤ 1,5 % bề ngang/s + tiến ≤ 1,5 % khoảng cách/s; CAU chỉ cận trên 6 m/s Chặn; VONG "vùng 1/3" Cảnh báo; KHOP "0 px" = ≤ 0,5 px trên 7 điểm | A: duyệt. B: chủ dự án đọc khác (vd DAY = phóng ảnh ≤ 1,5 %/s) | A: khớp cách đo bản thử T4 (`t4_do.py`). B: sát chữ hơn nếu ý là "phóng" | A: một chỗ K tự diễn giải | MAY-19 T4 | thấp | **A** |
| **K1174-D4** | G2 đòi log máy MỖI KHUNG (`log_may` = log.json `render_ldn.js`); bảng tóm tắt `t4_do.py` chỉ đủ ở animatic | A: duyệt. B: nhận bảng tóm tắt cả ở G2 | A: số đo từ trình dựng, không từ bảng phụ. B: nhẹ việc lưu trữ | A: phải giữ log.json từng shot (không xoá cùng `/var/tmp`) | phía dựng T4 | A: quên lưu → THIẾU = Chặn ở G2 | **A** |
| **K1174-D5** | AI-TU-LIEU (b) đòi khai `sha_tu_lieu` (thiếu → THIẾU, Chặn ở G2) | A: duyệt. B: chỉ (a) theo log shot | A: kiểm thật "không AI lên tư liệu" bằng SHA. B: không cần khai | A: một trường khai | T4 | thấp (tệp đã có: `licenses/SHA256-TU-LIEU.txt`, 13 SHA; thử: 0 trùng) | **A** |
| **K1174-D6** | GOC-CAO-60: mẫu số = thân phim (trừ thẻ PP, như TL-1); shot có log máy chỉ tính khung đạt V7B-D1 (AGL ≥ 120 m hoặc chúc ≥ 15° với ≥ 50 m) | A: duyệt. B: mẫu số = cả phim; chỉ dùng `goc` khai | A: đo, không tự khai; cùng định nghĩa TL-1. B: khớp số bảng shot (75,56 %) | A: V7B-D1 mới là đề xuất V7B — cần xác nhận còn hiện hành | T4 | thấp (T4 dự kiến 77 %) | **A** |
| (nhắc) | Q37 (c) T3 lộ 8,03 s ở N5_5 sau khi miễn thẻ PP; BIEN-CO-V T3 (c) 19,6 s ở N1_2 | ghi hồ sơ; T3 đã phát hành — không sửa | — | — | — | — | không cần quyết |

## 10. Chỉ số trong ±5 % quanh ngưỡng (luật cứng — nêu tên)
Trên luật đổi/mới và các lượt đo của phiên:
- **TU-LIEU-10 trên bảng shot T4 v1: 9,72 % (ngưỡng 10 %, −2,8 %)** — sửa bảng shot (thêm thẻ/tranh khắc) dễ vượt.
- D11 lượt 2: T9b 2,42 % (+21 %) và 2,67 % vùng hợp lệ (+33,5 %) — ngoài ±5 %, ghi để rõ: trượt thật.
- Hiệu chuẩn BIEN-CO-V: không chỉ số nào trong ±5 % quanh tiêu chí (R cắt 100 % ≫ 95 %; R beat 90,8 % ≫ 70 %; Δt 0,05 ≪ 0,25 s); θ 10 (sát lựa chọn) bắt 5/6 → trượt tiêu chí 6/6 — tức θ 8 nằm cách biên hỏng một nấc lưới.
- GOC-CAO-60 trên bảng shot T4: 77,3 % (ngưỡng 60 %) — xa ngưỡng; theo bảng shot tự tính 75,56 % so mục tiêu TL-1 75 % (+0,7 %, do phiên tiền kỳ nêu).
- T3 (không đổi so K-1.17.3, nhắc lại): EO-DAT-R3 N5_1 6,00 s (= 6 s), N5_4 5,87 s (−2,2 %); Q37 (1.13) khung tĩnh 5,92 s (−1,3 %); CHUONG-1 5 thẻ 3,00 s; PP-1 thẻ 9,0 s (cận trên); A1 −14,0 LUFS.
Selftest có ca đúng ngưỡng (bản đồ 12 %, tư liệu 10 %, góc cao 60 %, THAP 12 %) — dữ liệu tổng hợp, không phải số phim. Không phần tử nào được thêm để vượt ngưỡng; phiên này không sửa phim.

## 11. Chi phí thật
| Khoản | Số |
|---|---|
| Claude API (judge, O2, ML2, nhìn) | **$0** — không gọi (không `--o2-api`, `--ml2-api`, `--n2p-vision`, `selftest_k117 --api`) |
| OpenAI | **$0** |
| Gemini / ElevenLabs / RunPod / YouTube | 0 / 0 / 0 / 0 |
| Giờ máy (container) | **≈ 2,5 h đồng hồ** (15:40 → 18:05): k2check trên T3 4 lượt (8 m 38 s lỗi đường master + 11 m 49 s 1.17.3 + 12 m 6 s 1.17.4 trước khoá + 10 m 12 s cuối) ≈ 43 phút; hiệu chuẩn 3 lượt (lượt 1 ≈ 45 phút, lượt 2 dừng sau ≈ 15 phút, lượt 3 18 m 28 s) + thử tham số (≈ 8 phút); selftest đủ 2 lượt (≈ 12 phút); D11 tái hiện ≈ 3 phút. Song song tối đa 4 luồng (4 CPU) |
| Băng thông | tải master 1,79 GB (LFS `release-k2-t3-g2`) một lần |
| Token phiên chính | không đo được từ container (như K-1.17, K-1.17.3) |

## 12. Dòng sổ đề xuất (phiên P sau ghi — phiên này không sửa sổ)
- **COST-LEDGER:** 23/10 K-1.17.4 — Claude API $0, OpenAI $0, Gemini $0, giờ máy ≈ 2,5 h (container), tải LFS 1,79 GB.
- **AUTHORSHIP:** ghi khi chủ dự án trả lời K1174-D1…D6 (nguyên văn + giờ). Quyết định 23/10 21:45 "Duyệt Q1–Q7" (P ghi theo lệnh).
- **RIGHTS:** không tài sản mới (master T3 và đầu vào T6 đều đã có trong repo/LFS).
- **BAI-HOC-K2 (đề xuất):** (1) "`pkill -f`/`grep` theo chuỗi có trong chính lệnh shell giết shell" — lặp 2 lần trong phiên này (LL #24/#41): lấy PID bằng lệnh riêng; (2) "đẩy WIP bằng stash `checks/` làm hỏng lượt k2check đang chạy (import lười) — chạy k2check từ bản sao/worktree"; (3) "giả thuyết nguyên nhân lỗi đo phải kiểm bằng tách điểm lỗi theo vùng trước khi xin đổi luật (D11: dải giả góp 0 %)"; (4) "log.json máy của `render_ldn.js` phải lưu cùng shot — G2 cần cho MAY-19".

## 13. Việc chờ chủ dự án
1. **Trả lời K1174-D1…D6** (§9) — khuyến nghị: "Duyệt theo khuyến nghị" (D1 A, D2 A + hiệu chuẩn lại trên animatic T4, D3 A, D4 A, D5 A, D6 A).
2. Phiên P: merge `checks-1-17-4` khi duyệt (nhánh này **không** merge); ghi sổ theo §12; Kinh thánh §15 (d) sửa theo Q2 (bỏ "minh hoạ M-d ≤ 20 %" cho T4, thêm ngân sách Gemini/tập và góc cao ≥ 60 %) — K đã viết luật theo quyết định 21:45, chữ Kinh thánh do P ghi.
3. Phía dựng T4 (LOOK-T4 / sản xuất): khai trường theo §5; giữ log.json máy mỗi shot; tấm N2+ phải qua (iii) như cũ (sửa ảnh theo §1, hoặc chờ D1).
4. Nếu duyệt D1 A: một phiên K ngắn dựng khung đáp án phản chiếu ↔ bãi lấn cho N2P-3. Nếu duyệt D2 A: hiệu chuẩn lại BIEN-CO-V trên animatic T4 (log máy thật) trước G2 T4.
5. (Nhắc, không phải quyết định K) Cổng XEM CÂM §13.4 của T3 vẫn "chủ dự án chưa chấm"; bảng `reports/k1173/QUYET-DINH-TREO.md` còn các dòng ngoài K117-D8/K1173-D1/D6 nếu chưa ghi sổ.
