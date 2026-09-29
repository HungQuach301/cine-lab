# Báo cáo phiên K — checks v1.5

Ngày: 29/09/2026 · Nhánh: `checks/v1.5` (từ `main` cce7fb2) · Phạm vi sửa: `checks/`, `checks-appeal.md`, `reports/checks-v1.5/`.
LOCK cũ: `289c6916…d4f2` (v1.4.0) → **LOCK mới: `8d55b6ad…`** (v1.5.0).

## 1. Tóm tắt

| Việc | Kết quả |
|---|---|
| 1. P0 báo nhầm nhân vật thành chữ (2 khiếu nại, chủ dự án chấp nhận) | Đã sửa. Hai khung khiếu nại hết báo nhầm; chữ thật ≥ 4 ký tự trên áo, "56" trên tường, "56" chạm mép đầu và mặt nạ giả đều vẫn TRƯỢT |
| 2. C3 trục đầu lật (Cas 'bl' 0°/180°) | Đã sửa bằng trường khai `c3_head_axis` trong model sheet: `"doc"` đo đầu theo trục dọc thân, không lật; mặc định `"pca"` giữ đúng v1.4 |
| Phát hiện thêm | Đầu **Ida 'bl'** cũng rộng hơn cao ở cả 8 góc: `c3_views` Ida đang khoá là số theo **bề ngang** đầu. Cần chủ dự án quyết (Q-C3h) |
| Selftest | **142/142 khớp** (121 ca cũ + 21 ca mới); chạy đầu–cuối qua run.py: ĐẠT, LOCK khớp (toàn bộ ca cũ giữ kết quả) |
| Chạy thử layout-v15 | P0: 0 → 0 vùng. C3: v1.4 và v1.5 giống hệt từng mẫu (298 mẫu đo được) |
| Ngưỡng | Không đổi ngưỡng nào đã có. Ngưỡng mới đều nội bộ, nêu ở mục 2.3 |

## 2. Việc 1 — P0: nhân vật bị đọc thành chữ

### 2.1 Tái tạo lỗi

- Lấy lại đúng hai video có khiếu nại từ git: `8a707d7` (Cổng 5 v1, SHA `9c7f847a…`) và `44a469a` (Cổng 5 v2 bản cuối, SHA `78e662d1…`).
- Máy v1.4 báo đúng như P mô tả: khung 2775 hộp [469, 196, 494, 208] "56" độ tin 0,84; khung 1980 hộp [351, 288, 616, 452] "MA" độ tin 0,86.
- `layout-v15.mp4` hiện tại **không** còn báo nhầm (P0 ĐẠT ở cả v1.4). Vì vậy selftest dùng hai khung thật, cắt ra không mất dữ liệu (x264 qp 0): giải mã **khớp 0 điểm ảnh khác** với bản gốc. Mã hoá lại thông thường (CRF 8) làm mất báo nhầm, nên không dùng được.
- `X.parts/` hiện chỉ có mặt nạ C3 của **Ida** (một bên người). Khung 2775 là mắt **Cas**: mặt nạ hiện có không che được. Cần mặt nạ bóng mọi nhân vật.

### 2.2 Cách sửa

Vùng chữ không matte được **miễn** khi đủ cả năm điều kiện:

| # | Điều kiện | Ngưỡng | Nguồn ngưỡng |
|---|---|---|---|
| 1 | Chuỗi đọc được ngắn | ≤ 3 ký tự, không kể khoảng trắng | chủ dự án |
| 2 | Khung có mặt nạ nhân vật trong `X.parts/` | `silhouettes` (mới) và/hoặc mặt nạ C3 của đúng khung | — |
| 3 | Mặt nạ chạm hộp chữ | mặt nạ nới 2 px có điểm trong hộp | nội bộ |
| 4 | Mặt nạ khớp hình **ngay quanh hộp chữ** | độ khớp biên cục bộ (hộp nới 16 px, cách tính như C3) ≥ 1,5, ≥ 20 điểm biên | 1,5 = FID_MIN của C3; 16 px, 20 điểm: nội bộ |
| 5 | Phản chứng: thứ bị đọc thành chữ nằm trên nhân vật | xoá nhân vật (inpaint Telea, bán kính 5) rồi đọc lại đúng hộp: **không còn** chữ Latin | tiêu chí đọc chữ như cũ |

- Trường mới **`silhouettes`** trong `parts.json` (RUN.md 3.6.3): `{khung: PNG}`, bóng mọi nhân vật, không gồm đạo cụ cầm tay. P0 lấy mẫu ở khung khác C3 (layout 3 372 khung → bước 15), nên cần bóng cho đúng các khung P0.
- `run.py` tự đưa `X.parts/` vào P0.
- Báo cáo P0 liệt kê vùng được miễn (`vung_nhan_vat_mien`), chữ ngắn ở khung chưa có mặt nạ (`chu_ngan_khong_mat_na`), và danh sách khung lấy mẫu (`ds_khung_lay_mau`).
- Chống lạm dụng: `silhouettes` nằm trong SHA bộ mặt nạ của kiểm toán; phiếu kiểm toán chọn thêm 1 khung ngẫu nhiên trong các khung chỉ có bóng; khung được chọn phải render lại `silhouette.png`.
- Công cụ tham chiếu cho P: `reports/checks-v1.5/dryrun/k_sil.js` (render bóng từ chính trang render three.js; không sửa `design/`).

**Không chọn** đề xuất (b) của P (nâng độ tin cho chuỗi số ≤ 2 ký tự): không phân biệt được mắt với số thật. **Không chọn** (c) (vùng loại trừ khai tay): không kiểm được bằng máy.

### 2.3 Điểm lệch khỏi câu chữ phán quyết (cần chủ dự án xác nhận)

Phán quyết viết: "vùng OCR nằm **phần lớn** trong mặt nạ nhân vật". Đo thật khung s33:

| Cách đo "phần lớn" | Tỷ lệ nằm trong mặt nạ hai nhân vật (nới 0–3 px) |
|---|---|
| Diện tích hộp OCR | 16–22% |
| Vùng xác suất chữ của máy dò | 29–38% |
| Năng lượng cạnh trong hộp | 26–48% |

Hộp "MA" phần lớn là **tường giữa hai người**. Mọi ngưỡng diện tích > 50% đều giữ nguyên báo nhầm. Nhưng xoá hai nhân vật thì máy đọc lại được chuỗi rỗng (độ tin 0), tức chính hai dáng người là thứ bị đọc thành "M" và "A". K vì vậy hiểu "nằm phần lớn trong mặt nạ" là **"thứ máy đọc thành chữ nằm trên nhân vật"**, đo bằng phản chứng (điều kiện 5), kèm điều kiện 3 và 4. Khung s42a: hộp nằm 100% trong mặt nạ.

### 2.4 Selftest P0 (mới, 11 ca)

| Ca | Kỳ vọng | Kết quả | Vì sao |
|---|---|---|---|
| (a) s42a khung 2775, không mặt nạ (đối chứng) | TRƯỢT | TRƯỢT | mẫu tái tạo đúng báo nhầm "56" |
| (a) s42a khung 2775, có bóng nhân vật | ĐẠT | ĐẠT | "56" được miễn: độ khớp cục bộ 2,32; đọc lại rỗng |
| (a) s33 khung 1980, không mặt nạ (đối chứng) | TRƯỢT | TRƯỢT | tái tạo "MA" |
| (a) s33 khung 1980, có bóng nhân vật | ĐẠT | ĐẠT | "MA" được miễn: độ khớp cục bộ 1,61; đọc lại rỗng |
| (b) "BAKERY" in trên áo Cas | TRƯỢT | TRƯỢT | 6 ký tự; hộp nằm ≥ 90% trong mặt nạ |
| (b) "CAFE" in trên áo Cas (sát giới hạn 4) | TRƯỢT | TRƯỢT | 4 ký tự |
| (c) "56" trên tường ngoài nhân vật | TRƯỢT | TRƯỢT | hộp không chạm mặt nạ |
| (c) "56" chạm mép đầu Cas | TRƯỢT | TRƯỢT | xoá nhân vật vẫn đọc ra "56" (độ tin 1,0) |
| (c) "56" trên tường + mặt nạ giả vẽ thêm che chữ | TRƯỢT | TRƯỢT | độ khớp biên cục bộ 1,04 < 1,5 |
| Giới hạn đã biết: "56" in trên áo | ĐẠT | ĐẠT | ≤ 3 ký tự trên nhân vật được miễn theo phán quyết; có trong danh sách miễn |
| run.py tự dùng `X.parts/` cho P0 | ĐẠT | ĐẠT | lệnh duy nhất |

Ca "mặt nạ giả" ban đầu **lọt** khi K dùng độ khớp biên toàn khung (2,59, vì phần còn lại của mặt nạ là nhân vật thật). K đổi sang độ khớp cục bộ quanh hộp chữ; ca này nay TRƯỢT.

## 3. Việc 2 — C3: trục đầu

### 3.1 Số đo thật

K chạy lại chính công cụ turnaround của P (`c3_cas.py` ở nhánh layout, `c3_bl.py` ở main): số trục chính **khớp số của P** ở cả 8 góc (Cas: `CAS_c3_bl.json`; Ida: `ida.json` c3_views, ±0,002).

| Góc | Cas: đầu rộng × cao (px mặt nạ) | Cas thân/đầu 'pca' | Cas thân/đầu 'doc' | Ida: đầu rộng × cao | Ida thân/đầu 'pca' (= sheet) | Ida thân/đầu 'doc' |
|---|---|---|---|---|---|---|
| 0° | 782 × 481 | 1,379 | 2,241 | 527 × 350 | 2,272 | 3,404 |
| 45° | 652 × 482 | 1,711 | 2,334 | 492 × 362 | 2,219 | 3,044 |
| −45° | 651 × 482 | 1,715 | 2,336 | 494 × 372 | 2,216 | 2,953 |
| 90° | 581 × 482 | 1,724 | 2,105 | 508 × 389 | 2,033 | 2,558 |
| −90° | 577 × 482 | 1,732 | 2,102 | 508 × 393 | 2,069 | 2,580 |
| 135° | 543 × 456 | 1,811 | 2,165 | 454 × 330 | 2,381 | 3,355 |
| −135° | 625 × 447 | 1,821 | 2,180 | 452 × 331 | 2,353 | 3,344 |
| 180° | 782 × 395 | 1,370 | 2,713 | 527 × 267 | 2,130 | 4,202 |

- Trục chính đầu lệch trục dọc > 45° (lật) ở **8/8 góc Ida** và 6/8 góc Cas. Cas ±135°: trục chính lệch **42°**, sát chỗ nhảy bậc 45°.
- Layout-v15: 180/194 khung có đầu Ida lật; 14 khung không lật (so bề dọc/chéo với số bề ngang của sheet).
- Số đầy đủ: `dryrun/k_cas_doc.json`, `dryrun/k_ida_doc.json` (tham khảo cho P; K không ghi vào sheet hay `bible/`).

### 3.2 Hai cách K đã thử và bỏ

1. **Chọn trục riêng gần trục dọc nhất** (thay vì trục chính): hỏng ở Cas 135°, trục riêng nằm chéo, đầu đo được 344 px trong khi cao 456 px.
2. **Lai** (giữ trục chính khi lệch ≤ 45°, đổi sang trục dọc khi > 45°): nhảy bậc đúng ở Cas ±135° (42°): 607 px ↔ 508 px, tức 19%.
3. Trục dọc lấy từ **trục chính của mặt nạ thân** kèm ngưỡng thuôn 1,5: thân Cas chỉ thuôn 1,16 (0°/180°) và 1,51–1,55 (góc khác), sát ngưỡng. Bỏ; dùng vectơ tâm thân → tâm đầu, không cần ngưỡng.

### 3.3 Cách sửa (RUN.md 3.6.1)

- Model sheet khai `"c3_head_axis"`:
  - `"doc"`: độ dài đầu = bề dài chiếu mặt nạ đầu lên **trục dọc thân** (vectơ đơn vị từ tâm mặt nạ thân tới tâm mặt nạ đầu cùng khung; thiếu thân thì phương dọc ảnh) + 1 px. Liên tục, không lật, đi theo nhân vật khi máy nghiêng.
  - `"pca"` (mặc định khi không khai): như v1.4.
  - Giá trị khác: THIẾU (sai định dạng).
- `c3_views` phải đo bằng đúng cách đã khai. Kiểm toán dùng cùng cách đo.
- Báo cáo C3 liệt kê khung có đầu lật (`dau_rong_hon_cao`); với `"pca"` có ghi chú khuyên đo lại theo `"doc"`.
- Vì sao không đổi thẳng cách đo: `ida.json` đã khoá đo theo bề ngang. Đổi thẳng thì sheet Ida lệch 30–50% so với số đo shot, trượt oan mọi shot.

### 3.4 Selftest C3 (mới, 10 ca, gồm kiểm toán)

| Ca | Kỳ vọng | Kết quả |
|---|---|---|
| Đầu rộng 1,63 × cao 1 H ở 0° (tỷ lệ Cas 0°), sheet 'doc' | ĐẠT | ĐẠT (đầu lật được ghi nhận) |
| Cùng mặt nạ, sheet không khai (như v1.4) — đối chứng | TRƯỢT | TRƯỢT (trục lật, có ghi chú) |
| Đầu rộng, 'doc', thân +20% | TRƯỢT | TRƯỢT |
| Đầu rộng, cả nhân vật nghiêng 20° trong khung, 'doc' | ĐẠT | ĐẠT (trục dọc thân nghiêng theo) |
| `c3_head_axis` = 'vertical' | THIẾU | THIẾU, thông báo rõ |
| Kiểm toán 'doc' + `silhouettes`, render lại khớp | ĐẠT | ĐẠT |
| Kiểm toán: thiếu `silhouette.png` render lại | TRƯỢT | TRƯỢT |
| Kiểm toán: sửa bóng sau khi phát yêu cầu | TRƯỢT | TRƯỢT |
| Kiểm toán: bóng ở khung ngoài C3 → phiếu có 1 khung bóng, render lại khớp | ĐẠT | ĐẠT |
| Kiểm toán: khung bóng được chọn không render lại | TRƯỢT | TRƯỢT |

"Các ca C3 cũ vẫn giữ kết quả": mọi ca C3 của v1–v1.4 chạy lại với mã v1.5 cho đúng kết quả cũ (mục 4).

## 4. Selftest toàn bộ

- **142/142 ca đơn khớp kỳ vọng**: 121 ca của v1–v1.4 giữ nguyên kỳ vọng và kết quả (gồm mọi ca C3 cũ và 4 ca P0 cũ, trong đó ca hồi quy M0 "88:18"), cộng 21 ca mới (11 P0, 10 C3).
- Chạy đầu–cuối 16 luật bằng `run.py` (profile youtube): mẫu sạch ĐẠT (exit 0), LOCK khớp; mẫu bẩn exit 1 như kỳ vọng.
- Thời gian: 19 phút 32 giây (4 vCPU).

Kết quả đầy đủ: `reports/checks-selftest/selftest.md` và `.json`.

## 5. Chạy thử trên `design/cong5/layout/out/layout-v15.mp4` (SHA `8a5ebf01…`)

Kịch bản: `reports/checks-v1.5/dryrun/dryrun.py` (v1.4 lấy từ `checks/` ở cce7fb2, chạy tiến trình riêng). Số thô: `dryrun/dryrun.json`. Thời gian: 15 phút 55 giây.

### 5.1 P0

| Video | v1.4 | v1.5, `X.parts/` của P (Ida) | v1.5 + bóng K render |
|---|---|---|---|
| layout-v15 (233 khung mẫu, 52 shot) | ĐẠT, 0 vùng | ĐẠT, 0 vùng | ĐẠT, 0 vùng, 0 miễn |
| layout Cổng 5 v1 (`8a707d7`) | TRƯỢT, 1 vùng (s42a khung 2775 "56") | TRƯỢT, 1 vùng (báo "chữ ngắn ở khung chưa có mặt nạ") | ĐẠT, 0 vùng; 1 miễn (độ khớp cục bộ 2,32) |
| layout Cổng 5 v2 (`44a469a`) | TRƯỢT, 1 vùng (s33 khung 1980 "MA") | TRƯỢT, 1 vùng (như trên) | ĐẠT, 0 vùng; 1 miễn (độ khớp cục bộ 1,61) |

Theo shot: layout-v15 cả 52 shot 0 → 0 vùng. Hai video cũ: s42a 1 → 0, s33 1 → 0; mọi shot khác 0 → 0.
Bóng nhân vật K render cho 233 khung mẫu của layout-v15 (`dryrun/sil/layout-v15/`): 107 khung có cả Ida và Cas, 85 chỉ Ida, 12 chỉ Cas, 29 không nhân vật.

### 5.2 C3 (mặt nạ C3 Ida của P, kiểm toán như run.py)

- **v1.4 và v1.5 (ida.json nguyên trạng = 'pca') cho kết quả giống hệt từng mẫu**: 54 trượt chắc chắn, 45 không chứng minh được, 22 shot CẦN NGƯỜI XEM, độ khớp biên thấp nhất 0,7691, kết luận TRƯỢT. Khác duy nhất: v1.5 ghi thêm 180 khung đầu lật và ghi chú khuyên đo lại.
- Cột "giả định 'doc'": ida.json khai 'doc' với `c3_views` K đo lại theo 'doc' (không kiểm toán, vì đổi parts.json đổi SHA bộ mặt nạ). Chỉ để chủ dự án thấy tác động nếu chuyển.

| Shot | v1.4 = v1.5: đạt / trượt / KCM, lệch lớn nhất | Giả định 'doc': đạt / trượt / KCM, lệch lớn nhất |
|---|---|---|
| s02 | 0 / 6 / 10, 18,8% | 0 / 10 / 6, 17,4% |
| s07 | 0 / 6 / 2, 10,9% | 0 / 8 / 0, 11,4% |
| s11 | 0 / 4 / 0, 14,7% | 0 / 4 / 0, 11,9% |
| s13 | 0 / 2 / 0, 12,8% | **2 / 0 / 0, 0,96%** |
| s15 | 0 / 1 / 1, 9,9% | 0 / 0 / 2, 3,05% |
| s19 | 0 / 5 / 5, 29,8% | 0 / 5 / 5, 32,8% |
| s23 | 0 / 1 / 2, 13,9% | 0 / 1 / 2, 22,1% |
| s27 | 0 / 6 / 0, 7,9% | 0 / 6 / 0, 6,2% |
| s30 | 1 / 3 / 0, 13,8% | 0 / 4 / 0, 12,7% |
| s32 | 0 / 6 / 0, 26,3% | 0 / 6 / 0, 5,7% |
| s33 | 0 / 0 / 8, 3,7% | 0 / 0 / 8, 6,3% |
| s35 | 0 / 0 / 7, 5,7% | 0 / 0 / 7, 4,1% |
| s37w | 0 / 0 / 6, 2,7% | 0 / 6 / 0, 7,6% |
| s40w | 0 / 0 / 4, 0,96% | 0 / 4 / 0, 15,7% |
| s42a | 0 / 4 / 0, 8,6% | 0 / 4 / 0, 8,9% |
| s42 | 4 / 10 / 0, 14,4% | 0 / 14 / 0, 22,4% |
| Tổng | 5 / 54 / 45 | 2 / 72 / 30 |

Đọc bảng: 'doc' **không** làm Ida tốt lên đồng loạt. Shot cận (s13, s32) sát sheet hơn nhiều; shot nhân vật nhỏ hoặc có che/cúi (s37w, s40w, s42) lệch hơn. Nguyên nhân khả dĩ: chiều cao đầu nhìn thấy dưới mũ (267–407 px mặt nạ ở turnaround) nhạy với cúi/ngẩng và vành mũ hơn bề ngang. K **không** khuyến nghị chuyển Ida sang 'doc' khi chưa có thêm bằng chứng; với Cas 'bl' (chưa khoá) 'doc' tránh được nhảy bậc ở ±135°.

## 6. Chỉ số trong ±5% quanh ngưỡng

- P0, s33 khung 1980: độ khớp biên cục bộ **1,61** so với ngưỡng 1,5 (+7,3%, ngoài ±5% nhưng gần; nêu để người duyệt biết). Nếu render lại bóng làm số này xuống < 1,5 thì "MA" lại TRƯỢT.
- C3 layout-v15: như báo cáo P trước (hệ số mặt nạ 4 = ngưỡng 4; 4 ≥ 3,98). Không có chỉ số mới sát ngưỡng.
- Selftest: không có ca mới nào có chỉ số v1.5 trong ±5% quanh ngưỡng; các ca sát giới hạn là chủ ý ("CAFE" đúng 4 ký tự).

## 7. LOCK

- Cũ: `289c6916363f44f2c7a11967b8cd67a3b3aadcb100577f632cf518252d3ad4f2` (v1.4.0).
- **Mới: `8d55b6ad389dcbd2c40366bb16eed730106edef3ffee6c565e5ce786bd2aa65b`** (v1.5.0). Kiểm: `/opt/cine/bin/python checks/lock.py --verify`.
- File đổi trong `checks/`: `RULES.md`, `RUN.md`, `audit.py`, `cinecheck/__init__.py`, `cinecheck/audit.py`, `cinecheck/registry.py`, `cinecheck/rule_c3.py`, `cinecheck/rule_p0.py`, `run.py`, `selftest/run_selftest.py`; mới: `selftest/cases_v15.py`, 4 file mẫu trong `selftest/fixtures/` (2 khung khiếu nại 204–241 KB, 2 bóng nhân vật).

## 8. Token

Ước tính theo bộ đếm ngữ cảnh của phiên: khoảng 389000 token đã dùng (từ 15 triệu còn 14 611 000). Đây là số của bộ đếm phiên, không phải hoá đơn API. Phần nặng là đọc mã luật, chạy công cụ và đọc kết quả; render (bóng nhân vật 233 khung: 4 phút 37 giây; turnaround Cas, Ida: 2 phút 32 giây mỗi nhân vật) và chạy thử (15 phút 55 giây) tốn thời gian máy, không tốn token.

## 9. Việc đang chờ chủ dự án

1. **Duyệt checks v1.5** (nhánh `checks/v1.5`, LOCK `8d55b6ad…`). P merge sau khi duyệt. K dừng ở đây.
2. **Q-P0c**: xác nhận cách hiểu "vùng OCR nằm phần lớn trong mặt nạ" = phản chứng (xoá nhân vật thì hết chữ) + mặt nạ chạm hộp + khớp hình cục bộ (mục 2.3). Nếu chủ dự án muốn tỷ lệ diện tích thì khiếu nại "MA" không sửa được.
3. **Q-C3h**: Ida giữ 'pca' (sheet khoá hiện tại, kết quả không đổi) hay P đo lại `ida.json` theo 'doc' (phải khoá lại sheet, tác động theo shot ở mục 5.2)? Khuyến nghị của K: **giữ 'pca' cho Ida lúc này**; Cas v1.6 đo `c3_views` theo 'doc' trước khi khoá.
4. Việc cho P khi v1.5 được duyệt: xuất `silhouettes` cho khung P0 (công cụ tham chiếu `k_sil.js`); `checks/audit.py show` giờ in cả khung bóng cần render lại.
