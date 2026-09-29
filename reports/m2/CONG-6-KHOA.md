# CỔNG 6 — KHOÁ characters v1.5.1 + v1.6, LAYOUT-v16, MERGE MAIN. **DỪNG chờ chủ dự án quyết mở W1/W2**

Ngày 29/09/2026. Quyết định gốc: AUTHORSHIP "Cổng 6 — nhân vật" (duyệt khoá sau khi xem ảnh W4T3; ghi sai lệch đã chấp nhận).

## 0. Tóm tắt
- **Đã khoá v1.5.1 (Ida) và v1.6 (Cas), một lần.** LOCK-THIẾT-KẾ **34/34 tệp** (trước 28).
- **Mặc định mới:** Ida 'bl' v1.5.1; Cas 'bl', thân MPFB, tay MPFB.
- **layout-v16 đã render đủ 52 shot**, có silhouettes cho mọi khung P0 lấy mẫu. Luật checks v1.5 (LOCK `8d55b6ad…` KHỚP) có kiểm toán.
  - **P0 ĐẠT**; kiểm toán ĐẠT.
  - C3, H1b, G3b **TRƯỢT như v15**. Không shot nào đổi kết quả C3.
- **Main = `3c40f03`.** Worktree sạch tạo từ main thấy đủ tài sản: dò s24c, s42a được 6 ảnh nhỏ, lệch 0 px so với nhánh P.
- **Hai phát hiện cần chủ dự án biết:**
  1. C3 trên layout **chỉ đo Ida**, chưa đo Cas.
  2. Worktree mới **thiếu `node_modules`** (không nằm trong git), nên phải liên kết trước khi render.
- Kế hoạch W1/W2 đã soạn: `reports/m2/cong6/KE-HOACH-W1-W2.md`. **W1/W2 CHƯA mở.**

## 1. SHA
| Mục | SHA |
|---|---|
| **main** (merge nhánh P) | **`3c40f03876ab8c48317a9bb40dfaead3680f16b2`** |
| Nhánh P tại lúc merge | `7cbe52e` |
| Commit khoá | `2f05a4b` |
| `design/cong3/LOCK-THIET-KE.sha256` (34 tệp) | `95d6a347baadd7f5…` |
| checks LOCK (`lock.py --verify` trên main) | `8d55b6ad…` KHỚP |
| layout-v16.mp4 (44 841 753 byte) | `9a429b22…` |

**Tệp mới vào khoá** (SHA-256 16 ký tự đầu; đủ trong `assets/LIBRARY.json`):

| Tệp | SHA | Quyền |
|---|---|---|
| `ida_bl_v151.glb` | `d15eec30dff49276` | W4-MPFB-A |
| `ida_bl_v151.json` | `ca06762082994c9b` | W4-MPFB-A |
| `cas_bl.glb` | `fb48ef1cfb6a6d91` | W4-MPFB-A2 |
| `cas_bl.json` | `d279ec78f2ba25a7` | W4-MPFB-A2 |
| `cas_body_bl.json` | `51aeac44fabaf620` | W4-MPFB-A4 |
| `hands_bl.json` | `51400d38d79aae8f` | W4-MPFB-A3 |
| `ida.json` (v1.5.1) | `a322e3e61af01bb9` | — |
| `cas.json` (v1.6) | `604bd3392b2448b7` | — |

Tệp v1.5 (`ida_bl.glb`, `ida_bl.json`) giữ nguyên trong khoá.

**Nội dung khoá:**
- `bible/characters.md`:
  - hàng v1.5.1 (mắt, mũ ngồi thấp 0,025 H, tay MPFB);
  - hàng v1.6 (Cas MPFB: đầu, thân, cổ lật cao, quần ống thẳng, gấu 2,17 H, tay theo tỷ lệ MPFB);
  - bảng C3 Cas v1.6 theo 'doc';
  - dòng sai lệch đã chấp nhận.
- `cas.json`:
  - `c3_head_axis: "doc"`, `c3_views` theo W4T3;
  - độ dài cấp gốc 0°: thân 2,618 · tay trên 1,564 · cẳng tay 1,051 · đùi 1,604 · cẳng chân 1,464;
  - `measured_parts` thêm tay trên;
  - khớp tay 0,7643 / 0,7009 H.
- `ida.json`: `_v1_5_1`. `c3_views` giữ nguyên (đo lại lệch ≤ 0,14 %).
- `cast3d.js`: `HANDS_STYLE`, `CAS_STYLE`, `CAS_BODY` = `'bl'`.
- `build_cas_body_bl.py`: đặt `HEM_DROP` = 0 vì sheet đã ghi 2,17 H. Dựng lại được đúng từng đỉnh.

## 2. Luật checks v1.5 trên layout-v16 (`reports/checks/layout-v16/`)
| Luật | v15 | **v16** | Ghi chú |
|---|---|---|---|
| N1, N2, P1, G4, G3, M3, J1, J1b, H1, O3 | ĐẠT | **ĐẠT** | — |
| **P0** | ĐẠT | **ĐẠT** | 233 khung lấy mẫu; chữ không matte 0; 37 vùng chữ trong matte; **436 khung có mặt nạ nhân vật** (204 silhouettes + mặt nạ C3). **Vùng phải miễn theo mặt nạ nhân vật: 0** |
| **C3** | TRƯỢT | **TRƯỢT** | Mẫu: đạt 5 · trượt chắc 54 · không chứng minh được 46 (v15: 5 · 54 · 45). 23 shot có nhân vật mà không mẫu nào đo được (cần người xem) |
| **H1b** | TRƯỢT | **TRƯỢT** | Track tệ nhất khớp 0 %; track không đo được **3** (v15: 5); 113 track, 354 cặp khung |
| **G3b** | TRƯỢT | **TRƯỢT** | σ grain nhỏ nhất 0,735 (ngưỡng ≥ 0,8); **CV lớn nhất 0,216** (ngưỡng ≤ 0,2; v15 0,201); σ lớn/nhỏ 2,93 (≤ 1,3); tương quan grain 0,887 (≤ 0,5) |
| N3, M1 | N/A | N/A | — |

**P0, theo dõi s33 (khớp biên 1,61, ngưỡng 1,5):**
- Ở v16, máy dò **không còn vùng nghi chữ nào nằm trên nhân vật** (`vung_nhan_vat_mien` = 0), nên chỉ số khớp biên cục bộ của s33 không phát sinh. Không có số mới để so với 1,5.
- Không sửa hình để lách.

**Kiểm toán (RUN.md 3.7, v1.5):**
- Khung C3 được chọn: 2388. Khung chỉ có bóng: 1395.
- Render lại mặt nạ, views và `silhouette.png`: khác 0 %.
- Log có SCENE và FRAME. **ĐẠT mọi mục.**

**C3 theo shot so với v15** (`so-sanh-C3-theo-shot.json`):
- **Không shot nào đổi kết quả.**
- TRƯỢT 12 shot: s02, s07, s11, s13, s15, s19, s23, s27, s30, s32, s42a, s42.
- KCM 4 shot: s33 (3,7 %), s35, s37w, s40w.
- **Phát hiện:**
  - Mọi số sheet trong C3 đều từ **ida.json**. Bộ xuất mặt nạ C3 xuất **một nhân vật mỗi khung**, nên **Cas chưa được C3 đo** ở cả v15 lẫn v16. `c3_views` 'doc' của Cas v1.6 chưa được luật dùng tới.
  - Máy còn nhắc: 180/194 khung đầu Ida rộng hơn cao, "nên đo lại theo 'doc'". Chủ dự án đã quyết Ida giữ 'pca' (Q-C3h).
  - Việc này ghi vào kế hoạch (mục 12a): K xác nhận, hoặc P sửa bộ xuất cho hai nhân vật. Chủ dự án quyết.

**Chỉ số trong ±5 % quanh ngưỡng:**
- C3 hệ số mặt nạ lớn nhất 4,0 (ngưỡng ≤ 4,0, đúng ngưỡng).
- C3 hệ số khi đầu nhỏ 4,0 (ngưỡng ≥ 3,98, +0,5 %).
- G3b CV 0,216 **ra ngoài dải** (+8 %). v15 là 0,201, nằm trong dải.

## 3. Merge và kiểm worktree sạch
- Merge `--no-ff` nhánh P vào main → `3c40f03`. Main là tổ tiên của nhánh P, nên không có xung đột.
- Trên main: LOCK-THIẾT-KẾ 34/34 OK; `checks/lock.py --verify` KHỚP.
- **Worktree mới tạo từ `origin/main`:**
  - có `cas_body_bl.json`, `ida_bl_v151.glb`…;
  - dò `s24c, s42a` mặc định: **6 ảnh nhỏ, lệch 0 px** so với cùng lệnh ở nhánh P. Hình có Ida v1.5.1 và Cas MPFB mới.
- **Lưu ý:** worktree mới **không có `design/cong3/shared/node_modules`** (three.js, không nằm trong git). Phải liên kết trước khi render. Đã ghi vào kế hoạch W1/W2.
- Báo cáo này và kế hoạch W1/W2 nằm trên nhánh P, commit sau merge. Lần merge tới sẽ đưa lên main.

## 4. Kế hoạch W1/W2 (tóm tắt; đủ ở `reports/m2/cong6/KE-HOACH-W1-W2.md`)
- **Tổ chức:**
  - W1: s01–s24c (Ida);
  - W2: s25–s48 (Cas, hai người, PA1, cảnh 6);
  - P: ghép, luật, kiểm;
  - kiểm mù: mỗi khung một subagent mới, kèm đối chứng.
- **Cách chấm mới:**
  - ≥ 6 khung + 2 đối chứng; tách cột HÌNH và TƯ THẾ;
  - đạt khi tỉ lệ khung có từ khoá (cột HÌNH) ≤ nhiễu nền (10 %) và không có lời chê cùng chỗ lặp ≥ 2 khung.
  - **P tính (không tự đổi luật):** với 6 khung, ngưỡng 10 % nghĩa là 0/6. Nhân vật tốt thật mà nhiễu 10 % thì chỉ đạt 53 %. Với 10 khung (cho phép 1 khung), xác suất đạt là 74 %. **Đề xuất 10 khung mỗi lần**; chủ dự án quyết.
- **Việc W1/W2:**
  - tư thế đứng;
  - các shot cầm nắm theo tay mới: đo được 10 shot, thêm 2 shot chưa đo, tổng 12 (chủ dự án ghi 11);
  - khoảng cách Cas–Ida ở s41; Ida nhìn xuống Cas ở s42a;
  - dàn dựng lại PA1 s36–s39; s22 3/4; s40 chìm tối khi L11 tắt;
  - nhịp cười buồn trên clip có tiếng; mắt cận chính diện; van đồng PA1;
  - các sai lệch đã chấp nhận; tồn đọng Cổng 5.
- **Việc Cổng 7:** đèn lồng chiếu sáng xung quanh; bóng tiếp đất; người/bóng X = 2,0; các mục G có sẵn.
- **Ước tính token** (số đo thật của Cổng 5 và 6):

  | Gói | Ước tính |
  |---|---|
  | W1 | khoảng 1,0 triệu |
  | W2 | khoảng 1,3–1,5 triệu |
  | P | khoảng 0,4 triệu |
  | Kiểm | khoảng 1,0–1,4 triệu |
  | **Tổng** | **khoảng 3,7–4,3 triệu** |

  Rủi ro: mỗi vòng kiểm mù trượt tốn thêm 0,4–0,6 triệu.

## 5. Thời gian, token, hàng đợi
- **Token phiên P** cho chỉ thị này: **khoảng 120 nghìn** (khoá, pipeline, merge, kế hoạch, báo cáo).
- **Hàng đợi**, 10 việc làn nặng, chờ 0 s, **chạy tổng 11 272 s**:

  | Việc | Thời gian chạy | So với v15 |
  |---|---|---|
  | Render toàn phim | **8 386 s** | 4 325 s, **+94 %** (da CPU thân + tay MPFB) |
  | Ghép | 487 s | — |
  | Đóng gói | 195 s | — |
  | Mặt nạ C3 | 1 085 s | 556 s |
  | Bóng nhân vật | 537 s | mới |
  | Kiểm toán | 27 s | — |
  | Luật | 439 s | — |
  | Dò worktree sạch, dò nhánh P | 60 s + 58 s | — |

- **Thời gian thực:** 08:17–11:31 UTC. Pipeline 3 giờ 7 phút.

## 6. Việc đang chờ chủ dự án
1. **Quyết mở W1/W2** theo kế hoạch.
2. **Số khung mỗi lần kiểm mù:** 6 hay 10 (mục 4).
3. **C3 cho Cas:** giữ như hiện nay (C3 chỉ đo Ida) hay sửa bộ xuất cho hai nhân vật / hỏi K.
4. G3b (grain) vẫn trượt từ Cổng 5: layout chưa có khâu grain, việc của Cổng 7 (CONG-5-V3). Chỉ ghi lại, không làm gì.
