# G1b-T3 · VIỆC 7 — PHỤC CHẾ ẢNH CHỤP 1940s CÓ ĐÁP ÁN (Kinh thánh §12.3)

> Phiên con G1b-T3, 18/10/2026. Chỉ dùng ẢNH CHỤP: NARA RG 342-FH, 3 ảnh Gibraltar ngày 2/10/1943, không có tranh hay bản khắc. Mã chạy: `phuc_che.py` (venv CPU ngoài git `/var/tmp/g6w/venv`, torch CPU 2 luồng, `nice 15`).

## 1. Ảnh gốc: tải bản gốc, SHA khớp sổ tài sản
| Ảnh (NAID) | Tệp | px | SHA-256 tải lại 18/10 | Khớp `tai-san-vay-ham.json` / `licenses/nara-204918833.txt` |
|---|---|---|---|---|
| 204918833 (C-47 dỡ hàng, Rock) | 342-FH_000757.jpg | 4532×3532 | `c3b81b1904a4fbbf55e9f858a5b9d2c645f382e864ca8dafa2e821fd228cb47e` | **KHỚP** |
| 204918836 (C-47 "Superman") | 342-FH_000759.jpg | 4512×3516 | `f5812d275dd70f5fc17474d435e124a8722ebd14cec7467c4e296ec3a051a5e6` | **KHỚP** |
| 204918839 (biên giới) | 342-FH_000761.jpg | 4504×3502 | `cc2ab128a513301c0c99e7d9e82319e3e9524720f2bb13288a6326b5932c2a40` | **KHỚP** |

Bản gốc để ngoài git ở `/var/tmp/cine-out/g1b/phuc-che/goc/`. Quyền: NARA "Unrestricted", là tác phẩm liên bang (PD), như sổ đã ghi.

## 2. Công cụ và giấy phép (`giay-phep/GIAY-PHEP.md`, kèm tệp nguyên văn)
- **Swin2SR classical ×2** (`caidas/swin2SR-classical-sr-x2-64`):
  - Thẻ mô hình ghi `license: apache-2.0`; mã mv-lab ghi Apache-2.0; chạy qua transformers (Apache-2.0).
  - Trọng số safetensors: SHA `a5159558…c4fb`.
- **Real-ESRGAN x2plus**:
  - Mã: "BSD 3-Clause License". Trọng số lấy từ bản phát hành v0.2.1, SHA `49fafd45…6abb`.
  - Kiến trúc RRDBNet viết lại tối giản để nạp trọng số, `strict=True`.
- **Mốc so:** bicubic.
- **Loại, không tải:** CodeFormer, SUPIR, GFPGAN, Depth Pro, Depth Anything V2 Base/Large.
- **Rủi ro ghi nhận:** cả hai mô hình huấn luyện trên DIV2K/Flickr2K. Điều khoản dữ liệu huấn luyện không nằm trong giấy phép trọng số → chủ dự án quyết định có chấp nhận hay không.

## 3. Kiểm có đáp án (`kiem.json`, tờ so `to-so-kiem-dap-an.jpg`)
**Cách làm:**
- Mỗi ảnh cắt 8 ô 512×512 (hạt 20261018, độ lệch chuẩn > 20); mỗi ô là một đáp án.
- Thu nhỏ ×0,5 (INTER_AREA) rồi phục chế ×2, so với đáp án.
- **Cạnh mới** = tỉ lệ điểm cạnh Canny (60/150) của bản phục chế mà đáp án không có cạnh nào trong vòng 2 px.

| Ảnh | Công cụ | PSNR (dB) | SSIM | Cạnh mới TB | Cạnh mới ô xấu nhất | s/ô (CPU dùng chung) | Kết luận (> 5 % → LOẠI) |
|---|---|---|---|---|---|---|---|
| 000757 | bicubic (mốc) | 47,68 | 0,9877 | 3,95 % | 16,74 % | 0 | — |
| 000757 | **Swin2SR ×2** | **48,10** | 0,9881 | **3,72 %** | 19,81 % | 46,4 | **ĐẠT** |
| 000757 | Real-ESRGAN x2plus | 32,60 | 0,9170 | **50,09 %** | 98,16 % | 5,7 | **LOẠI** |
| 000759 | bicubic (mốc) | 48,05 | 0,9876 | 6,40 % | 19,02 % | 0 | — |
| 000759 | Swin2SR ×2 | 48,32 | 0,9878 | **8,64 %** | 24,23 % | 69,4 | **LOẠI** |
| 000759 | Real-ESRGAN x2plus | 33,77 | 0,9288 | **50,66 %** | 75,29 % | 20,4 | **LOẠI** |
| 000761 | bicubic (mốc) | 47,42 | 0,9898 | 5,21 % | 15,67 % | 0 | — |
| 000761 | Swin2SR ×2 | 48,13 | 0,9904 | **6,34 %** | 11,81 % | 61,0 | **LOẠI** |
| 000761 | Real-ESRGAN x2plus | 28,70 | 0,8775 | **49,06 %** | 75,63 % | 16,0 | **LOẠI** |

**Đọc số:**
- **Real-ESRGAN bịa nét rõ.** Khoảng một nửa số cạnh là cạnh mới. Ảnh mất hạt phim, tương phản và tông đổi, vân bề mặt (đường băng, thân máy bay) bị vẽ lại; PSNR thấp hơn bicubic 14–19 dB. → **LOẠI cho cả 3 ảnh.**
- **Swin2SR:**
  - Chỉ hơn bicubic **+0,27 đến +0,71 dB**. Cạnh mới bằng hoặc cao hơn bicubic tới 2,2 điểm.
  - 000757 đạt (3,72 %). 000759 (8,64 %) và 000761 (6,34 %) **trượt ngưỡng 5 %**.
- **Ngay bicubic cũng có 3,95–6,40 % cạnh mới** (000761 là 5,21 %, nằm trong ±5 % quanh ngưỡng tương đối — xem §5).
  - Lý do: Canny bắt hạt phim và vết bụi, nên thước "cạnh mới" có nền nhiễu khoảng 4–6 % trên ảnh 1940s nhiều hạt.
  - Đề nghị K cân nhắc đo "cạnh mới **so với bicubic**", hoặc làm mượt σ ≈ 1 px trước Canny (ghi vào khiếu nại nếu K khoá luật).

## 4. Phục chế bản gốc (chỉ ảnh qua kiểm: 000757 · Swin2SR)
- **Cách làm (×1):** chạy mô hình ×2 rồi thu về đúng cỡ gốc (INTER_AREA). Ô 384 px, chồng 32 px, hoà bằng cửa sổ Hann. Đây là khử nhiễu/làm nét, **không phóng**: bản quét đã 4,5k px nên không cần ×2 (NC-AI §3.2).
- **Phạm vi:** chạy cả ảnh mất khoảng **3–4 giờ CPU** trên máy 4 nhân dùng chung (46–69 s mỗi ô 256 px khi phiên chính đang dựng). Vì vậy chỉ phục chế **vùng người + C-47** (x 1000–3048, y 2300–3068, 2048×768 px) để chứng minh quy trình. Kết quả ở §4b.
- **Đề xuất:** **không dùng phục chế AI cho 3 ảnh này trong T3.** Lợi ích đo được rất nhỏ (+0,4 dB so bicubic). Hai trên ba ảnh trượt. Bản gốc 4,5k px đã dư cho 1080p/4K. Muốn bớt hạt thì dùng khử nhiễu cổ điển (NLM/BM3D, không sinh nét) và kiểm cùng thước.

### 4b. Kết quả vùng 000757
| Mục | Số đo |
|---|---|
| Vùng | x 1000–3048, y 2300–3068 (2048×768): người, xe, càng C-47 |
| Thời gian | **2 249 s** (37,5 phút; CPU dùng chung, phiên chính đang dựng) |
| Cạnh mới so với bản gốc (kiểm lần hai, cả vùng) | **0,30 %** |
| PSNR so với bản gốc | 60,18 dB |
| Lệch điểm ảnh | TB **0,06** mức xám · p99 1 · max 3 |
| Tệp | `342-FH_000757_swin2sr_x1_vung.png` — 664 984 byte, SHA-256 `34cb9e2973b44d07b3ac8c054f2c6d4736d0a39c1a51a765c866e7ea12827341`. Bản gốc cùng vùng ở `/var/tmp/cine-out/g1b/phuc-che/…_goc.png` |
| Tờ so | `to-so-truoc-sau.jpg` (272 KB): gốc · phục chế · lệch ×10 |

**Kết luận:**
- Ở ×1, Swin2SR **gần như là phép đồng nhất**: lệch trung bình 0,06 mức xám, mắt thường không thấy khác.
- Mô hình classical-SR không được huấn luyện để khử hạt, nên ×1 không làm sạch ảnh. Còn ×2 thì không cần, vì bản gốc đã 4,5k px.
- → **Không có ảnh nào nên thay bằng bản phục chế AI.** Dùng bản gốc. Quy trình kiểm (`phuc_che.py`) vẫn để lại, dùng được cho ảnh chụp độ phân giải thấp về sau.

## 5. Chỉ số trong ±5 % quanh ngưỡng (luật cứng)
- **Swin2SR · 000757: cạnh mới 3,72 %** so với ngưỡng 5 %, cách ngưỡng 25,6 %. Không nằm trong ±5 %.
- **Bicubic · 000761: 5,21 %** (cách ngưỡng +4,2 %). Đây là mốc so, không phải công cụ được xét. Ghi lại vì nó cho thấy thước có nền nhiễu sát ngưỡng.

## 6. Chi phí, giờ máy
- API: **0 $**.
- Giờ máy:
  - Kiểm có đáp án: 29,4 phút.
  - Phục chế vùng: 37,5 phút.
  - Một lượt phục chế cả ảnh đã chạy rồi **dừng chủ động** (ước 3–4 h, lợi ích không đáng).
- Đĩa (ngoài kho): venv khoảng 1,5 GB; trọng số 115 MB.

## 7. Tệp
`phuc_che.py`, `kiem.json`, `to-so-kiem-dap-an.jpg` (166 KB), `to-so-truoc-sau.jpg`, `342-FH_000757_swin2sr_x1_vung.png` (665 KB), `giay-phep/` (GIAY-PHEP.md + 4 tệp nguyên văn).
