**Nhánh thật: `checks-1-17-5`** (đúng lệnh; gốc `origin/checks-1-17-4` @f4a3d9ca, LOCK 1.17.4 `08486eb2…`). Harness gợi ý `ccr-be60bd61-3pu9td` — không dùng để đẩy công việc. Không merge, không đụng `main` hay nhánh khác.

# Phiên K-1.17.5 — tấm nền N2+ T4 (A1–A4) + phép kiểm mới BE-MAT-NHA (A5, phương án B) — BÁO CÁO

> Phiên K, 23/10/2026 23:40 → 24/10/2026 ≈ 02:30 UTC, song song P-2410 và GIONG-T4 (không ghi vào vùng của họ). Mọi số là số đo thật trong phiên; tệp số đo ở `reports/k1175/do/`. Đọc (không sửa) `origin/k2c-t4-02-look2` @c4079595 bằng `git archive` vào thư mục tạm; mã dựng chỉ CHẠY bản sao trong thư mục tạm.
> Email chủ dự án không có trong tệp, commit, header, URL, payload hay User-Agent nào (UA `CineLab-research (+https://github.com/HungQuach301/cine-lab)`). Không in/ghi khoá (proxy gắn khoá).

## 0. Khối điều lệ và tóm tắt
| Trường | Lệnh | Thực tế |
|---|---|---|
| Nhánh | `checks-1-17-5` từ origin/checks-1-17-4 @f4a3d9ca | đúng |
| Vùng sửa | `checks/**`, `checks-appeal.md` (khiếu nại + phán quyết), `reports/k1175/**` | đúng. Không sửa `docs/`, sổ, `scripts/`, `design/`, `channel-k2/`, `main` |
| Chi phí | Claude API mốc $3 (chặn $10), OpenAI $2 (chặn $5), Gemini 0, giờ máy 5 h | **Claude API $0,50 · OpenAI $0,34 · Gemini $0** · giờ máy ≈ 2,9 h đồng hồ container (§11) |
| Preflight | `set -o pipefail`; commit chỉ khi "— ĐẠT"; hook trước lần đẩy đầu | hook pre-commit + pre-push cài 23:48 (trước lần đẩy đầu); mọi commit/push "PREFLIGHT ĐẠT" + `lock.py --verify: KHỚP` (mã chưa khoá: cất `checks/` bằng stash khi commit/push — như K-1.17.3/4) |
| `lock.py` không `--verify` | đúng một lần ở bước khoá cuối | **đúng một lần**, 2026-10-24 01:52:26 UTC (§8) |
| Force/amend/dừng hỏi | không | không |
| Đẩy ≤ 30 phút + CHECKPOINT | bắt buộc | `reports/k1175/CHECKPOINT.md` (mục Trạng thái + Lệnh bổ sung đã áp) |

**Tóm tắt:**
1. **A2 = LỖI LUẬT, sửa.** N2P-3 chiều nước→đất đổi từ T9b ("màu nước" HSV tuyệt đối) sang **T9c — đường bờ đo, đối chứng render** (tấm ≈ T(render), T affine Lab khớp bền; độ sâu "khác nước" đo từ đường bờ). Nước đổi xám/ô-liu/nâu/nhạt giữ bờ: đạt (luật cũ: T9b 91,1 %). Bờ lấn ≥ 8 px: **bắt 100 %** ở cả nửa chỉnh lẫn nửa kiểm (2D 30/30, Blender 32/32). T6 lượt 1/2/3 thật vẫn TRƯỢT (l2 bờ bắc lấn sâu 22 px — đúng D11).
2. **A1 = MỘT PHẦN.** Phản chiếu VẬT LÝ có trong render 3D được giữ tự động (Blender Cycles: 12/12 ca âm đạt). Phản chiếu do AI tự vẽ thêm **không được miễn**: thử 3 thước phân biệt (trục gương + vật cao + pha màu + tương quan) — luật 0 lọt bờ lấn chỉ miễn ≈ 48 % dải phản chiếu tổng hợp, 0 % phản chiếu vật lý. Muốn có phản chiếu: dựng trong 3D.
3. **A3 = LỖI LUẬT, sửa.** Thêm N2P-1 (e) lớp sống cộng hiệu (ghép == clip(nền + (render có − không)) ≤ 1/255) và (iv) soi tấm nền.
4. **A4 = không phải lỗi mã K** ((i) chỉ đo trong mặt nạ (a)); vòng bảo vệ = render là chữ Kinh thánh §15 (a). K thêm phép kiểm (d) cho khớp màu cục bộ — chỉ áp khi chủ dự án duyệt K1175-D3.
5. **A5 BE-MAT-NHA = luật mới, đạt một phần.** (b) khoá 0/255, (c) thời đại (5/5 vật hiện đại, 0 báo nhầm trên 2 ảnh AI thật), (d) quỹ đạo sáng + nhấp nháy, (e) khung 0 chiếu 3D: đạt tiêu chí cả hai nửa. **(a) hình khối KHÔNG đạt "bắt 100 % nhà dời ≥ 2 m hoặc đổi mái"** ở 1,4–4,8 px/m: chỉ Chặn phần thô (xoá nhà 3/3, 0 báo nhầm), còn lại Cảnh báo người đọc → quyết định **K1175-D5**.
6. Selftest `selftest_k1175.py` **52/52**; cũ k112 75 · k1121 48 · k1122 37 · k113 64 · k114 126 · k115 105 · k116 144 · k117 130 · k1172 74 · k1173 42 · k1174 91 · k2 129 · ll 317 — đạt hết trên cây đã khoá; **0 kỳ vọng cũ đổi**.
7. **LOCK 1.17.4 `08486eb2…` → 1.17.5 `c7630b4a…`**, `--verify` KHỚP. T3: xem §7.

## 1. Dữ liệu và khung đáp án (tiêu chí đặt TRƯỚC khi đo)
- **Ảnh có sẵn:** T6 tiền kỳ T4 (render + mặt nạ ID + 3 ảnh AI trong git; ghép lại bằng `t6_ghep.py` nguyên bản qua `reports/k1174/do/d11_tai_hien.py` → SHA ghép trùng từng bit sổ kiểm tiền kỳ, T9b 42,24 / 2,42 / 15,02 % như K-1.17.4). look2: 24 ảnh AI thô + khung render JPG trong git; **mặt nạ ID và tấm ghép KHÔNG có trong git** (ở `/var/tmp/ldn/v2/tn/` của phiên LOOK) → không tái hiện được số `tam-nen.json`; chỉ đo chỉ báo bằng mặt nạ nước suy từ render (thuyền/cầu lớp (a) chưa ghép nên số không dùng để phán).
- **Cảnh tổng hợp có đáp án** (`do/canh_tong_hop.py`, Blender 5.2 Cycles, tất định theo hạt): thành phố ven sông kiểu 1666 (6 886 nhà ở hạt 3; dãy nhà theo lô, mái hồi dọc/ngang/hông/bằng), nhà thờ + tháp, cầu, tường, kè đứng, thuyền (lớp (a)), bãi; mặt nước **bóng có gợn — phản chiếu vật lý**; mặt nạ lớp + mã nhà 24 bit + mã mặt phẳng + **pass bóng** (albedo xám đều) xuất bằng Workbench không khử răng cưa — chính xác từng bit. Máy P1 (230 m, cách bờ ≈ 920 m, fov 50° → 1,4–2,1 px/m) và TRUNG (105 m, ≈ 390 m → 2,3–4,8 px/m). Cấu hình mọi cảnh: `do/cau-hinh/`.
- **Chia nửa:** A1/A2 — nửa A (chỉnh) = T6 render lượt 1/2 + Blender P1 hạt 1; nửa B (kiểm) = T6 render lượt 3 + Blender TRUNG hạt 2. A5 — nửa A = Blender P1 hạt 3, nửa B = Blender TRUNG hạt 4 (+ 2 ảnh AI thật).
- **Tiêu chí A1/A2 (đặt trước):** (1) bắt 100 % đoạn bờ lấn ≥ 8 px @1080 (đáp án 4–40 px); (2) 0 báo nhầm ở nước đổi sắc giữ bờ và phản chiếu vật lý có trong render; (3) T6 lượt 2 thật vẫn trượt; (4) ghi tỷ lệ bắt 4–6 px (không bắt buộc). **A5 (đặt trước, theo lệnh):** (a) bắt 100 % nhà dời ≥ 2 m (độ dời chiếu ≥ 3 px) hoặc mái đổi dạng, 0 nhà không đổi bị báo; (b) bắt mọi điểm đổi ngoài vùng cho phép; (c) bắt vật hiện đại có trên ảnh, 0 báo trên ảnh sạch; (d) dán tĩnh khi nắng đổi + nhiễu mỗi khung trượt, dựng lại ánh sáng đúng đạt; (e) chồng sáng trượt.

## 2. A1/A2 — N2P-3 (iii): **A2 LỖI LUẬT (sửa) · A1 MỘT PHẦN**
**Đi tới T9c (minh bạch các lượt):** lượt 1–3 giữ ý "mẫu nước của chính tấm" + phép thử gương (trục gương ở mặt nước dưới chân vật, chỉ vật cao mới có ảnh phản chiếu nhìn từ máy cao, pha màu α, phần dư, tương quan gradient). Kết quả (dải 4 hàng × cửa sổ 24 cột, `do/band-feat.json`): luật miễn phản chiếu có 0 dải bờ lấn lọt (tf ≥ 0,6, α ∈ [0,05; 0,8], phần dư ≤ 0,4) chỉ miễn **48,5 % / 47,0 %** dải phản chiếu tổng hợp (nửa A / B); trên phản chiếu vật lý Blender phần dư màu **0,6–0,9** → miễn 0 %. Kết luận: không tách được phản chiếu AI khỏi bờ lấn ở độ nhạy 100 % → **bỏ hướng miễn phản chiếu AI**. Lượt 4: **đối chứng render** — thứ render 3D có (phản chiếu vật lý, bóng) không phải thay đổi của AI.

**T9c (mã `checks/ll/q_k1175.py::t9c`, gọi trong `q_n2p.do_tam`):** mỗi thành phần nước (≥ 0,2 % khung): tấm ≈ T(render), T = affine Lab 3×3 + hằng + hệ số hàng y, khớp IRLS Huber (4 vòng) — hấp thụ đổi sắc/độ sáng; ΔE76 (mờ σ 1,5) tới T(render) > τ = max(τ0, 3 σ lõi) → "khác nước"; bỏ loé. Bờ trên: cửa sổ 24 cột (bước 8), dải 4 hàng, bỏ 2 px mép mềm, ≤ 2 dải đầu được giống nước (kè/bóng); độ sâu = các dải liền ≥ 50 % khác nước. **(c)** đoạn sâu ≥ 6 px @1080, dài ≥ 12 px; bờ khác: cụm bám bờ sâu ≥ 6 px; **(d)** khác nước giữa nước ≤ 2 %. T9b đất→nước (a) giữ; T9b nước→đất chỉ in.

**Chọn τ0 ở nửa A, kiểm ở nửa B** (`do/grid.out`, `do/a1-*.json`):
| τ0 | Nửa A: bắt ≥ 8 px (2D · Blender) | Nửa A: ca âm đạt (2D không phản chiếu AI · Blender) | Nửa B: bắt ≥ 8 px | Nửa B: ca âm đạt | Ghi |
|---|---|---|---|---|---|
| 5 | 15/15 · 18/18 | 4/4 · **4/6** | 15/15 · 14/14 | 4/4 · 6/6 | hỏng ca âm Blender (ô-liu, nâu) |
| **6** | **15/15 · 18/18** | **4/4 · 6/6** | **15/15 · 14/14** | **4/4 · 6/6** | **chọn** |
| 7 | 15/15 · 17/18 | 4/4 · 6/6 | 15/15 · 14/14 | 4/4 · 6/6 | sót bến gỗ tối 8 px |
| 8 | 15/15 · 16/18 → 17/18 sau sửa mép kè | 4/4 · 6/6 | 15/15 · 14/14 | 4/4 · 6/6 | sót 8 px |
Bắt 4–6 px (không bắt buộc): 2D 6/6 + 6/6, Blender 4/6 + 6/6 (τ0 6). Bờ lấn 8 px nhỏ nhất ở đáp án Blender đo được sâu 10 px (ngưỡng 6). Ca 2D có phản chiếu AI tự vẽ (render không có): trượt 4/4 mỗi nửa — **đúng thiết kế** (không miễn).

**Ảnh thật** (`do/a1-thuc.json`, `do/a1_thuc.py`):
| Tấm | T9b nước→đất (1.17.4) | T9c đoạn bờ lấn · sâu nhất · giữa nước | Render ↔ chính nó |
|---|---|---|---|
| T6-l1 | 42,24 % | 14 · 30 px · 0,31 % → TRƯỢT | ĐẠT |
| **T6-l2 (D11)** | **2,42 %** | **12 · 22 px · 0,34 % → TRƯỢT** (bờ bắc x 336–935) | ĐẠT |
| T6-l3 | 15,02 % | 14 · 58 px · 2,81 % → TRƯỢT | ĐẠT |
| look2 (mặt nạ suy, chỉ báo) | 0,9–80,5 % | Gemini M1-trung l1/l3 (T9b 80,5 / 34,3 %) **ĐẠT**; còn lại trượt — gồm thuyền/cầu lớp (a) chưa ghép trên ảnh thô và mép mặt nạ suy | — |
Ghi chú đo: mặt nạ phải đúng độ phân giải khung — mặt nạ thu 960×540 rồi phóng lệch bờ 1 px làm ca âm Blender ô-liu trượt (đã thấy khi làm fixture).

## 3. A3 — lớp sống cộng hiệu: **LỖI LUẬT, sửa**
T6 + khói bếp tổng hợp (14 cột, 1,38 % khung) — `do/a3a4.json`, selftest:
| Cách ghép lớp sống | (i) trong (a) | (i-s) sai lớn nhất ngoài vùng bảo vệ | Kết quả |
|---|---|---|---|
| cộng hiệu render có/không (V3 a) | 0 | **0/255** | ĐẠT |
| dán nguyên điểm render (cách T6) | 0 | 8–72/255 | TRƯỢT (e) |
| lớp sống lệch 6 px | 0 | 38–50/255 | TRƯỢT (e) |
| nửa cường độ | 0 | 18–22/255 | TRƯỢT (e) |
| AI vẽ khói lên tấm nền + cộng hiệu | 50 (trong (a)) | 0 | (e) đạt; khói AI trên `nen` → mô hình (iv) soi `nen` |
Mô hình nhìn soi `nen` khi khai `song` (khoá bộ đệm theo `nen.png` — selftest). Không tái hiện được ca (iv) M1-rong-oai-l3h (tấm ghép ở `/var/tmp` phiên LOOK); số LOOK cho thấy biến thể "nhà xa lớp (c)" 0 báo (iv) → (iv) do quầng (A4), không do khói.

## 4. A4 — khớp màu cục bộ vòng bảo vệ: **không phải lỗi mã K; cần sửa chữ Kinh thánh**
- (i) 1.17.0–1.17.4 chỉ đo `max |ghép − render-khớp|` TRONG mặt nạ (a) — không đo vòng nở 1/3 px; ràng buộc "vùng bảo vệ = render" là chữ §15 (a) mà phía dựng làm đúng → sinh quầng khi tông tấm lệch render.
- K thêm phép kiểm được (d) (khai `khop_mau_cuc_bo: true`): vòng = render-khớp + MỘT độ lệch màu/vật (phần dư ≤ 1/255, |lệch| ≤ 40). T6 l1/l2/l3: khớp cục bộ giữ (i) 0/255, phần dư vòng ≤ 1. **Lợi ích chưa đo được trong phiên:** T6 không có quầng như M1-rong (ΔE vòng+viền ↔ ảnh AI 8,1 / 8,1 / 8,5 trước → 8,1 / 8,4 / 9,4 sau — chênh do nội dung AI khác, không phải tông). Cần đo lại trên M1-rong khi có mặt nạ (K1175-D3, D6).

## 5. A5 — BE-MAT-NHA (phương án B): **luật mới, đạt một phần**
### 5.1 (a) Hình khối — thước và hiệu chuẩn
Cạnh HÌNH HỌC = biên nhà ∪ biên mặt phẳng (mã ID), thấy được ở render VÀ pass bóng (gradient ≥ 3); đỡ = tỷ lệ điểm cạnh có cạnh màu ảnh ghép trong 1,5 px; dời tốt nhất trong ±4 m. Lượt đầu (cạnh render thường) cho nhà chỉ đổi bề mặt đỡ p5 = 0,08–0,15 (cạnh MÀU giữa hai nhà kề mất khi sơn lại) → thêm pass bóng. Đáp án: 34 biến thể Blender (bề mặt đổi đồng thời — mat_seed + bảng màu khác) + 2 ảnh AI thật (`ai/BMN-*-l1-ai.jpg`, OpenAI edits, lệnh "chỉ phủ bề mặt nhà"; AI giữ bố cục nhưng thêm đầu hồi/mái ở dãy trước — nhìn thấy). Đặc trưng (`do/a5-feat-v4.json.gz`):
| Nhãn | Nửa A (P1, px/m TV 1,9, điểm cạnh TV 19): đỡ p5 / TV | Nửa B (TRUNG, px/m TV 3,1, điểm cạnh TV 24): đỡ p5 / TV |
|---|---|---|
| chỉ đổi bề mặt (âm) | 0,71 / 1,00 (p1 0,44) | 0,75 / 1,00 (p1 0,41) |
| dời 2 m (dời chiếu ≥ 3 px) | 0,58 / 0,93 | 0,11 / 0,70 |
| dời 5 m | 0,34 / 0,65 | 0,08 / 0,60 |
| đổi mái (hông/bằng/xoay) | 0,35–0,67 / 0,80–1,00 | 0,39–0,64 / 0,68–0,86 |
| thêm tầng | 0,26 / 0,54 | 0,17 / 0,58 |
| xoá nhà | 0,63 / 0,73 | **0,11 / 0,17** |
| gộp 2 nhà (đỡ vách ngăn riêng) | 0,30 (1 vách) | 0,43 (1 vách); âm: p1 0–0,25 |
**Điểm vận hành** (nửa B, ≥ 3 px/m, ≥ 40 điểm cạnh): bắt 100 % (16 nhà đổi) ↔ **3,4 %** nhà không đổi bị báo (≈ 6–10 nhà/khung); 0,67 % báo nhầm ↔ bắt 75 %. Mức khung: 2,7–5,1 % nhà bị cờ ở MỌI biến thể kể cả ảnh AI thật và bề mặt-thuần → tổng hợp theo khung cũng không tách. Dời theo chiều sâu ở P1: 2 m chỉ còn ≈ 0,7 px (co ngắn) — không thước ảnh nào đo được.
**Luật đặt (§6):** Chặn khi đỡ < 0,20 (≥ 2 px/m, ≥ 40 điểm cạnh): **0 / 4 248** nhà không đổi, **0 / 263** nhà ảnh AI thật, bắt xoá 3/3 — dời 0/11, đổi mái 0/9, thêm tầng 0/3. Cảnh báo (w) khi đỡ < 0,45 hoặc dời ≥ 1,5 m với đỡ tăng ≥ 0,30 (in IoU từng nhà). Nhà không đo được → phải giữ render (b). **Yêu cầu 100 % của lệnh không đạt** → K1175-D5.
### 5.2 (b)(c)(d)(e)
| Phép | Đáp án | Kết quả |
|---|---|---|
| (b) khoá 0/255 | đổi 200 điểm nền; dán AI vào nhà không đo được | bắt (b) 6–166/255 lệch; ghép đúng → 0 |
| (c) thời đại (lời nhắc `bmn-v2`, năm bắt buộc) + q_thoi_dai | ảnh AI thật TRUNG + vẽ thêm 3 điều hoà, 1 mảng kính lam, 1 biển "SHOP" | **5/5** bởi cả GPT và Claude (năm 1700–1950) + q_thoi_dai 2 mới → (c); lời nhắc v1 (năm tuỳ chọn): GPT liệt kê đủ nhưng không năm → chỉ (w), q_thoi_dai 2 → (c) |
| (c) ảnh sạch | 2 ảnh AI thật (P1, TRUNG) ghép theo mặt nạ | **0** (c), 0 THIẾU (v2); v1 có 1 lượt Claude không đọc đủ ảnh → THIẾU (đúng thiết kế) |
| (d) quỹ đạo sáng (6 khung, nắng 18→43°) | dựng lại đúng · khử sáng tỉ số · dán tĩnh · nhiễu σ 4 mỗi khung | nhà lệch > 0,10: **0,08 / 0,29 %** (A/B) · 0 / 0 · **97,4 / 95,8 %** · 0,3 / 0,4 % |
| (d) nhấp nháy bề mặt (ngưỡng 0,012, chọn nửa A) | như trên | 0,007 / 0,008 · 0,003 · 0,056 / 0,061 · **0,018 / 0,019** |
| (e) khung 0 chiếu 3D (ΔE TB ≤ 4, p95 ≤ 12) | chiếu không khử sáng (sáng chồng 2 lần) | ΔE TB **12,1 / 12,4**, p95 18,9 / 18,6 → trượt; đúng → 0 (PNG), 2,8 / 9,1 (mã hoá mp4v trong selftest) |

## 6. Luật đổi / mới (1.17.5)
| Hàng | Tệp | Trường đọc | Ngưỡng | Mức |
|---|---|---|---|---|
| N2P-3 (iii) nước→đất = **T9c** | `q_k1175.t9c`, `q_n2p.do_tam/tong_tam` | `n2p.tam[]` {render, ghep, mat_na} như cũ | (c) bờ lấn sâu ≥ 6 px @1080 & dài ≥ 12 px; (d) giữa nước > 2 %; τ0 6, τ = max(6, 3σ) | Chặn G2 / Cảnh báo animatic (như N2P-3) |
| N2P-3 (a) đất→nước | không đổi | — | T9b ≤ 2 % | như cũ |
| **N2P-1 (e) lớp sống** | `q_k1175.kiem_song`, `q_n2p.kiem_tam` | tấm `song: {render_co, render_khong, nen}` | ≤ 1/255 ngoài vùng bảo vệ; thiếu tệp → THIẾU; mô hình soi `nen` | Chặn G2 / Cảnh báo animatic |
| **N2P-1 (d) vòng khớp màu cục bộ** | `q_k1175.kiem_vong` | tấm `khop_mau_cuc_bo: true` | phần dư ≤ 1/255; \|lệch\| ≤ 40 | Chặn G2 / Cảnh báo animatic — chỉ khi chủ dự án duyệt D3 |
| **BE-MAT-NHA** (mới) | `q_k1175.be_mat_nha`, `k2check.py`, `cap112.py` | tấm `be_mat_nha_ai: true`, `mat_na_nha`, `mat_na_mat`, `bong`, `nha` [{id, lo, px_m}], `nen_ai`, `be_mat_nha_video {ghep, render, cach, tam}`, lớp `nha_thuong` (215,215,215) | (a) ≥ 2 px/m, ≥ 100 px, ≥ 40 điểm cạnh; đỡ < 0,20 Chặn, < 0,45 / dời ≥ 1,5 m Cảnh báo · (b) 0/255 · (c) 0 lỗi có năm · (d) ≤ 2 % nhà e > 0,10; nhấp nháy ≤ 0,012 · (e) ΔE ≤ 4 / p95 ≤ 12 | Chặn (a)–(e) G2 / Cảnh báo animatic; (w) luôn Cảnh báo |
| — | `cinecheck/__init__.py`, `RULES-LL.md` (mục 1.17.5), `k2check.py` (hàng mới, chữ ngưỡng N2P), `cap112.py` | — | VERSION 1.17.5 | — |

## 7. Cách khai cho phía dựng (tên trường)
- **Mọi tấm N2+ (không đổi):** `n2p.tam[]` {id, shot, render (render-khớp), ghep (PNG), mat_na (PNG đúng độ phân giải khung), nam}. **Bắt buộc lưu mặt nạ + tấm ghép vào git/LFS** (bài học phiên này: look2 không tái hiện được).
- **Lớp sống (khói bếp…):** `song: {render_co: <render có lớp sống>, render_khong: <render không>, nen: <tấm đã ghép lớp (a), chưa cộng lớp sống>}`; ghép = clip(nen + (render_co − render_khong)) ngoài vùng bảo vệ.
- **Khớp màu cục bộ (chỉ khi D3 duyệt):** `khop_mau_cuc_bo: true`; mỗi vật: vòng bảo vệ = render-khớp + độ lệch (trung vị AI − trung vị render-khớp ở dải ngoài).
- **BE-MAT-NHA:** tấm `be_mat_nha_ai: true` + `mat_na_nha` (PNG 24 bit), `mat_na_mat` (PNG mã mặt phẳng — three.js: ghi mã tam giác/mặt), `bong` (cùng máy/giờ, vật liệu xám đều 0,6, không vân), `nha` (JSON [{id, lo, px_m}] — px_m = độ dài chiếu 1 m ngang ở tâm nhà), lớp `nha_thuong` trong mặt nạ lớp; `nen_ai: true` nếu tấm cũng là tấm nền N2+; timelapse: `be_mat_nha_video: {ghep: mp4, render: mp4, cach: anh_tinh | chieu_3d, tam: <tấm AI đã duyệt> (chieu_3d)}`. Ghép: AI chỉ trong nhà ĐO ĐƯỢC (nở 1 px); nhà khác giữ render.

## 8. Selftest + LOCK
- `checks/ll/selftest_k1175.py` **52/52** (không mạng/API; ≈ 50 s; fixtures 0,9 MB): T9c 14 (render↔chính nó; xám/ô-liu; T9b đối chứng 91,1 %; tong_tam; bờ lấn 8/16/40 px; T6 l2 thật; Blender phản chiếu vật lý ×3 + bờ lấn; phản chiếu AI tự vẽ) · (e) 8 · (d) 6 · BE-MAT-NHA (a) 3, (b) 3, (c) 4, (d)(e) 5, cấp 3 + 2, áp dụng 3. Mỗi luật đổi/mới ≥ 1 ca đạt + ≥ 1 ca trượt.
- Selftest cũ trên cây đã khoá (`do/selftest-sau-khoa.txt`): k112 75/75 · k1121 48/48 · k1122 37/37 · k113 64/64 · k114 126/126 · k115 105/105 · k116 144/144 · k117 130/130 · k1172 74/74 · k1173 42/42 · k1174 91/91 · k2 129/129 · ll 317/317 — **không kỳ vọng cũ nào đổi** (k117 N2P-3 4/4 giữ với T9c).
- **LOCK:** cũ 1.17.4 `08486eb21dc55749115849e9691a4321458ecf8411e0562b141506f77227dd6d` → **mới 1.17.5 `c7630b4a6b8f4f8e7a2bcfc593b59e35df76e21ab404b0d532c595c2d06ea10a`** (DATE_UTC 2026-10-24T01:52:26Z); `python3 -I checks/lock.py` không cờ: đúng một lần; `--verify` KHỚP (ngay sau khoá, mọi commit/push, hàng LOCK k2check cuối).
- Tệp đổi trong `checks/`: `LOCK`, `cinecheck/__init__.py`, `ll/RULES-LL.md`, `ll/cap112.py`, `ll/k2check.py`, `ll/q_n2p.py`; mới `ll/q_k1175.py`, `ll/selftest_k1175.py`, `ll/fixtures/k1175/` (8 tệp).

## 9. So k2check 1.17.4 ↔ 1.17.5 trên bản cuối T3
Đầu vào như K-1.17.4 §7: `git archive origin/main channel-k2/k2c-t3-01 reports/animatic-t3-v2 AUTHORSHIP.md RIGHTS.md` (thư mục tạm), timeline tổng hợp (`reports/k1172/do/mk_tl.py`, 761,9998 s), log chữ tổng hợp (`reports/k1173/do/mk_log_chu.py`), master thật LFS `release-k2-t3-g2` (tải qua media.githubusercontent.com với UA CineLab-research; SHA-256 `5b9f0bcc…` khớp; một lần đứt kết nối, nối tiếp `curl -C -`). Lệnh: `k2check.py <tạm>/…/cuoi/episode.yaml --tl timeline.json --master <tuyệt đối>/k2-t3-v1-master.mp4 --cap --no-asr`. 1.17.4 chạy từ worktree `origin/checks-1-17-4` (LOCK 1.17.4 KHỚP) — **trùng hệt bảng K-1.17.4** (`reports/k1174/do/k2check-1.17.4-t3.md`) ở mọi dòng trừ tiêu đề. Bảng đủ: `do/k2check-1.17.4-t3.md`, `do/k2check-1.17.5-t3.md`.
| Hàng | 1.17.4 | 1.17.5 | Lý do |
|---|---|---|---|
| 55 hàng chung (Q26b … Q37, NHIP-K2, BIEN-CO-V, N2P-1…6 "KHÔNG ÁP", MINH-HOA, EO-DAT-R1…R4, 1.17.4 (T4), LOCK, A1–A13) | — | **giống hệt** (kết quả + giá trị + danh sách lỗi) | — |
| **1.17.5 (T4)** (mới) | — | KHÔNG ÁP (tập trước T4 — không hồi tố) | luật 1.17.5 chỉ tập từ T4 |
Mã thoát cả hai: 1 (TRƯỢT như K-1.17.4 — Q37 (a)(c)(d), EO-DAT-R3 (a), XEM-CAM, K-LAI-2 (d), BIEN-CO-V). Thời gian: 10 m 43 s (1.17.4) · 11 m 59 s (1.17.5).

## 10. Chỉ số trong ±5 % quanh ngưỡng (luật cứng — nêu tên)
- Không chỉ số phim nào trong ±5 % (phiên không sửa phim). Trên khung đáp án: selftest BE-MAT-NHA nhà 20 dời 2,5 m — đỡ cạnh **0,44 so ngưỡng Cảnh báo 0,45 (−2,2 %)** (dữ liệu tổng hợp); τ0 = 6 cách điểm hỏng (5) một nấc lưới.
- Xa ngưỡng (ghi để rõ): bờ lấn 8 px nhỏ nhất đo sâu 10 px (ngưỡng 6, +67 %); (d) nhấp nháy đúng 0,0076 so 0,012 (−37 %); (e) mã hoá mp4v 2,8 so 4 (−30 %).

## 11. Chi phí thật
| Khoản | Số |
|---|---|
| OpenAI | **$0,343** = ảnh gpt-image-2.5 edits 2 × $0,0756 (sổ AI `reports/k1175/so-ai.jsonl`) + mô hình nhìn gpt-6.1-sol 5 lần $0,192 |
| Claude API | **$0,497** = mô hình nhìn claude-sonnet-5-5 5 lần $0,259 + q_thoi_dai (O2) 5 khung duy nhất $0,239 |
| Gemini / ElevenLabs / RunPod / YouTube | 0 |
| Giờ máy | ≈ 2,9 h đồng hồ container (23:40 → ≈ 02:35): Blender ≈ 80 cảnh (≈ 1,7 h CPU nền, ≤ 2 tiến trình nặng), đánh giá A1 ≈ 25 phút, A5 ≈ 15 phút, selftest 2 lượt ≈ 20 phút, k2check 3 lượt ≈ 28 phút (1.17.4 hỏng 5,5 + 10,7; 1.17.5 12,0) |
| Băng thông | master T3 1,79 GB (LFS `release-k2-t3-g2`, SHA `5b9f0bcc…` khớp) |
| Token phiên chính | không đo được từ container |

## 12. Quyết định đề xuất (chủ dự án)
| # | Đề xuất | Phương án | Ưu | Nhược | Tác động | Rủi ro | Khuyến nghị |
|---|---|---|---|---|---|---|---|
| **K1175-D1** | Phản chiếu trên tấm nền (A1) | A: chỉ phản chiếu có trong render 3D (đối chứng render giữ tự động); lệnh AI "không vẽ phản chiếu". B: miễn phản chiếu AI bằng thước gương | A: đúng vật lý, theo timelapse, đo được 100 %. B: tấm đẹp hơn ngay | A: phải dựng phản chiếu trong 3D (look2.js) nếu muốn. B: **trái lệnh** — thước 0 lọt chỉ miễn ≈ 48 % (2D), 0 % vật lý | mọi tấm có sông | B: bờ lấn lọt | **A** |
| **K1175-D2** | Duyệt T9c thay T9b chiều nước→đất (τ0 6, sâu ≥ 6 px, dài ≥ 12 px, giữa nước ≤ 2 %) | A: duyệt. B: giữ T9b | A: Gemini/OpenAI đổi sắc nước không còn trượt oan; bắt 100 % bờ lấn ≥ 8 px. B: không đổi | A: đòi mặt nạ đúng độ phân giải. B: Gemini 0/12 tấm | T4 N2+ | A: thước mới chưa thử trên tấm look2 có mặt nạ thật | **A** + phiên LOOK đo lại tấm look2 bằng T9c |
| **K1175-D3** | Sửa §15 (a): cho phép khớp màu cục bộ vòng bảo vệ (một độ lệch/vật), K kiểm (d) | A: duyệt. B: giữ chữ hiện tại (V4 a) hoặc V4 (c) nhà xa ngoài hộp → lớp (c) | A: hết quầng mà mép vật giữ nguyên cấu trúc (đo được). B: an toàn | A: lợi ích chưa có số đo trên M1-rong. B: (iv) trượt vì quầng | 1666 toàn cảnh | A: thấp (phần dư ≤ 1/255 bắt vẽ lại mép) | **A**, kèm đo lại M1-rong-oai-l3h khi có mặt nạ |
| **K1175-D4** | Lớp sống cộng hiệu (V3 a) + khai `song` | A: duyệt. B: lớp sống dán nguyên (cách T6) | A: đúng điểm ảnh render, (i-s) 0/255 | — | mọi tấm có khói bếp | thấp | **A** |
| **K1175-D5** | Phương án B (AI phủ bề mặt nhà) với (a) hình khối chưa đạt 100 % | A: chỉ dùng ở nhà ĐO ĐƯỢC (≥ 2 px/m, ≥ 40 điểm cạnh — chủ yếu khung trung/cận), (a) Chặn phần thô + Cảnh báo người đọc + mô hình nhìn `hinh_khoi`; nhà xa giữ render. B: như A nhưng cho cả nhà không đo được (bỏ khoá (b) cho nhà) . C: chờ một vòng K phát triển thước hình khối khác (điều khiển hình học: ControlNet độ sâu/pháp tuyến, hoặc AI chỉ làm nguồn vật liệu theo mặt phẳng) trước khi dùng B. D: dồn lực phương án A (nâng 3D) cho T4 | A: dùng được ngay ở khung gần, rủi ro đo được. B: phủ cả toàn cảnh (nơi "đồ chơi" rõ nhất). C: chặt. D: không rủi ro dữ kiện | A: toàn cảnh P1 gần như không được phủ (nhà ~15 px không đo được). B: dời 2–5 m, đổi mái ở nhà xa **không kiểm được**. C: trễ. D: không giải "đồ chơi" bằng AI | T4 look | B: lỗi hình khối lọt; A: người đọc phải soi danh sách (w) | **A + D** (B cho khung trung/cận, A nâng 3D cho toàn cảnh); C nếu chủ dự án muốn B ở toàn cảnh |
| **K1175-D6** | Mặt nạ ID + tấm ghép + JSON kiểm của mọi tấm N2+/BMN phải vào git/LFS (≤ 5 MB nén) | A: duyệt (thêm vào quy ước PLAN). B: giữ ở /var/tmp | A: K tái hiện được (phiên này không tái hiện được look2) | A: dung lượng repo | mọi phiên tấm nền | thấp | **A** |
| **K1175-D7** | Lời nhắc BMN v2 (năm bắt buộc) + q_thoi_dai cho (c) | A: duyệt. B: v1 | A: 5/5 vật hiện đại thành Chặn | chi phí ≈ $0,2/khung | — | thấp | **A** |

## 13. Dòng sổ đề xuất (P ghi — phiên này không sửa sổ)
- **COST-LEDGER:** 24/10 K-1.17.5 — OpenAI $0,343 (2 ảnh edits $0,151 + nhìn $0,192), Claude API $0,497 (nhìn $0,259 + O2 $0,239), Gemini $0, giờ máy ≈ 2,9 h, tải LFS 1,79 GB.
- **AUTHORSHIP:** ghi khi chủ dự án trả lời K1175-D1…D7 (nguyên văn + giờ). Quyết định 24/10/2026 06:21 "1. Chọn phương án A+B theo khuyến nghị" và K1174-D1 = A (24/10).
- **RIGHTS:** 2 ảnh AI (OpenAI, `reports/k1175/ai/`) — đầu vào là render Blender của K (không tài sản ngoài), chỉ dùng làm khung đáp án kiểm, không dùng trong phim. Không nhạc/SFX/giọng/font mới.
- **BAI-HOC-K2 (đề xuất):** (1) `pkill -f` khớp chính shell — LẶP lần 3 (LL #24/#41, K-1.17.4): chỉ dừng theo PGID; (2) cất `checks/` bằng stash khi selftest đang chạy nền → có thể làm hỏng lượt đó — đẩy WIP khi không có lượt chạy, hoặc chạy từ worktree; (3) mặt nạ/tấm ghép để ở /var/tmp làm phiên K không tái hiện được — lưu vào git/LFS; (4) mặt nạ phải đúng độ phân giải khung (thu/phóng lệch bờ 1 px); (5) Blender `world_to_camera_view` cần `view_layer.update()` sau khi đặt máy.

## 14. Việc chờ chủ dự án
1. Trả lời **K1175-D1…D7** (§12) — khuyến nghị: D1 A, D2 A, D3 A, D4 A, D5 A + D, D6 A, D7 A.
2. Phiên P: merge `checks-1-17-5` khi duyệt (nhánh này **không** merge); ghi sổ theo §13; nếu D3 = A: sửa chữ Kinh thánh §15 (a).
3. Phiên LOOK/sản xuất: đo lại 24 tấm look2 bằng T9c (mặt nạ của họ), lưu mặt nạ + tấm ghép vào git/LFS (D6); khai `song` cho khói bếp; BE-MAT-NHA khai theo §7.
4. (Nếu D5 = C) một phiên K phát triển thước hình khối có điều khiển hình học.
