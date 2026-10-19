# Bảng giãn shot theo lời thu thật — K2C-T3-01 lời v4.2, G1 speed 1,03 (KL42, 19/10/2026)

> CHỈ ĐỀ XUẤT — không sửa `vay-ham/treatment.json`. Thay bảng GIỌNG-CHỐT §5 (bảng đó ước lời theo số từ; bảng này dùng mốc thật của bản thu). Số liệu đầy đủ (mốc từng câu/shot trong bản thu và trên trục phim): `nhip-that.json` (B, đề xuất) và `nhip-that-A.json` (A). Công cụ: `nhip.py`, `lam_bang.py`.

**Thứ tự shot theo lời v4.2:** ‹2o›, ‹2p› đứng ngay sau ‹KA1782›, trước ‹2j› (`treatment.json` vẫn theo thứ tự cũ: G1b/V7 dời 2 shot này khi dựng).

**Luật** (giữ khung GIỌNG-CHỐT §5 đã được duyệt): mỗi shot chứa lời của nó + 0,4 s; lời chảy sang shot kế tối đa 0,5 s, nhưng không chảy vào tấm im lặng và không chảy ra ngoài shot cuối; khi có lời chảy sang, lời của shot kế bắt đầu sau phần chảy + 0,4 s. Shot giãn được là shot 3D không phải khung neo, mốc đinh, cú liên hoàn hay 0c. Thẻ, ảnh, tranh, bản đồ giãn tới trần của loại; footage (2p) tạm lấy trần 12 s. Không giãn tấm im lặng, không cắt lời. Bậc 1/24 s.
- **A, chỉ giãn:** 721,167 → **751,500 s** (+30,333), 12 shot giãn.
- **B, giãn + trần đuôi (đề xuất):** sau A, mỗi shot giãn được hoặc thẻ/ảnh/bản đồ có lời giữ tối đa **1,37 s hình sau lời** (khung neo, mốc đinh, cú liên hoàn, 0c và tấm im lặng giữ nguyên). Kết quả **745,000 s**: 12 shot giãn, 13 shot rút.
- Để so: kéo nhịp lời ×1,02 sau thu → 745,583 s; ×1,03 → 743,417 s (chỉ giãn, không rút). Phải nghe tệp kéo nhịp trước khi chọn.
- Kiểm cả hai phương án: không có lời nào cách lời kế < 0,4 s, không có lời rơi vào tấm im lặng (KB1943, KA2026), không có lời tràn ra cuối phim. Tổng lời theo shot là 666,308 s.

## Shot đổi thời lượng

| Shot | Loại | Kiểu | Lời thật (s) | Chảy vào (s) | Dur cũ | **B (đề xuất)** | A | GIỌNG-CHỐT §5 (ước) |
|---|---|---|---|---|---|---|---|---|
| 0d | thẻ số | tran | 6,873 | 0,233 | 7,500 | **7,500** (+0,000) | 7,500 | 8,000 |
| 0g | 3D phố | gian | 4,273 | 0,000 | 6,000 | **5,667** (-0,333) | 6,000 | 6,000 |
| 0h | 3D vùng | gian | 3,762 | 0,000 | 5,500 | **5,167** (-0,333) | 5,500 | 5,500 |
| 1a | 3D vùng | gian | 2,903 | 0,000 | 5,000 | **4,292** (-0,708) | 5,000 | 5,000 |
| 1d | 3D phố | gian | 15,847 | 0,000 | 13,500 | **16,250** (+2,750) | 16,250 | 13,500 |
| 1i | 3D vùng | gian | 12,154 | 4,550 | 13,000 | **17,125** (+4,125) | 17,125 | 17,625 |
| 1j | 3D vùng | gian | 10,519 | 0,000 | 10,000 | **10,958** (+0,958) | 10,958 | 10,000 |
| 2h | ảnh | tran | 8,046 | 0,000 | 7,000 | **8,458** (+1,458) | 8,458 | 7,000 |
| 2o | 3D phố | gian | 9,056 | 0,000 | 12,500 | **10,458** (-2,042) | 12,500 | 18,500 |
| 2p | footage | tran | 6,536 | 0,000 | 8,000 | **7,917** (-0,083) | 8,000 | 8,000 |
| 2j | 3D phố | gian | 13,978 | 0,000 | 12,500 | **14,417** (+1,917) | 14,417 | 12,500 |
| 2q | 3D vùng | gian | 11,633 | 3,575 | 11,000 | **15,625** (+4,625) | 15,625 | 11,000 |
| 3a | 3D vùng | gian | 11,262 | 5,072 | 12,000 | **16,750** (+4,750) | 16,750 | 13,875 |
| 3d | 3D phố | gian | 8,290 | 0,259 | 10,000 | **9,958** (-0,042) | 10,000 | 10,000 |
| 3h | 3D vùng | gian | 7,268 | 0,694 | 9,500 | **9,333** (-0,167) | 9,500 | 9,500 |
| 4c | 3D vùng | gian | 6,409 | 4,208 | 9,000 | **11,042** (+2,042) | 11,042 | 13,042 |
| 4d | 3D phố | gian | 8,452 | 0,000 | 10,500 | **9,833** (-0,667) | 10,500 | 10,500 |
| 4f | bản đồ lịch sử | tran | 6,827 | 0,000 | 9,000 | **8,208** (-0,792) | 9,000 | 9,000 |
| 4g | 3D vùng | gian | 0,000 | 8,492 | 5,500 | **8,917** (+3,417) | 8,917 | 6,417 |
| 4h | ảnh | tran | 9,846 | 0,000 | 11,500 | **11,250** (-0,250) | 11,500 | 11,500 |
| 4i | 3D vùng | gian | 14,558 | 0,000 | 16,000 | **15,958** (-0,042) | 16,000 | 16,000 |
| 5a | 3D phố | gian | 15,313 | 0,000 | 14,000 | **15,750** (+1,750) | 15,750 | 14,000 |
| 5d | 3D phố | gian | 1,509 | 0,000 | 4,500 | **4,000** (-0,500) | 4,500 | 4,500 |
| 5e | thẻ số | tran | 6,594 | 2,858 | 6,417 | **8,000** (+1,583) | 8,000 | 7,375 |
| 5h | 3D phố | gian | 13,920 | 0,167 | 16,000 | **15,458** (-0,542) | 16,000 | 17,000 |
| 5j | 3D vùng | gian | 16,475 | 2,548 | 18,500 | **19,458** (+0,958) | 19,458 | 20,375 |
| 5k | 3D phố | gian | 19,365 | 0,000 | 20,000 | **20,000** (+0,000) | 20,000 | 21,167 |

## Theo chương

| Chương | Dur cũ | B | A |
|---|---|---|---|
| 0 | 44,500 | 43,833 | 44,500 |
| 1 | 122,125 | 129,250 | 129,958 |
| 2 | 203,625 | 209,500 | 211,625 |
| 3 | 84,500 | 89,042 | 89,250 |
| 4 | 110,500 | 114,208 | 115,958 |
| 5 | 155,917 | 159,167 | 160,208 |
| **Tổng** | 721,167 | **745,000** | 751,500 |

## Ghi chú cho G1b/V7
- **2o (mặt cắt hầm, M11):** ở v4.2, 2o không còn hứng 5,4 s lời chảy từ chuỗi 2k–2n như bảng GIỌNG-CHỐT, nên không cần +6 s. Ở B, 2o rút 2,04 s (12,5 → 10,458).
- **Lời chảy từ chuỗi 2k–2n** (thẻ 2n chạm trần, cú liên hoàn 2m cố định) nay được hấp thụ ở **2q** (3D vùng), +4,6 s.
- **4g:** hấp thụ phần chảy 8,5 s của SM3, trước tấm im lặng KB1943. Lời SM3 kết thúc trước KB1943 ≥ 0,4 s.
- **5j:** +0,96 s; lời 5j kết thúc trước KA2026 ≥ 0,4 s (lỗi lời tràn từ KHOA-LOI-41 không còn).
- Vị trí đặt lời: `nhip-that.json` → `shot[].loi_bd_phim / loi_kt_phim` (giây trên trục phim theo phương án), `shot[].cau[]` (từng câu), `shot[].ban_thu` (mốc trong stem `T3-loi-G1-v42-14LUFS.wav` và trong từng chương). Mốc lấy theo alignment ký tự của ElevenLabs.
