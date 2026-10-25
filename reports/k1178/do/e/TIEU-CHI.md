# LUẬT E — đáp án và tiêu chí (đặt TRƯỚC khi đọc kết quả mô hình nhìn; K-1.17.8, 25/10/2026 ≈ 17:45 UTC)

Khung: render V2 P9-2026 (`@1a911a01 channel-k2/k2c-t4-02/animatic2/tam-nen/P9-2026/render.png`, SHA `04cc8142…`), mặt nạ V2 → mặt nạ E (`matna-e.png`
`a5cc7608…`: nhà thường 215, công trình có tên 235 = mái vòm St Paul's + 7 toà tháp City nhô khỏi chân trời, hộp lập bằng mắt), mã công trình `matna-ct.png`
(`fb77ad7a…`), bản đêm tổng hợp `render-dem.png` (`7c8a13b8…`, giảm sáng từ render ngày — KHÔNG phải render đêm V2). Ảnh AI (OpenAI gpt-image-2.5,
toàn khung, không mặt nạ): `ai/P9-2026-E-{ngay,dem,xau}-ai.jpg` (lệnh `lenh-*.txt`). Ghép: `ghep_e.py` (AI + lớp (a)-E từ render nở 1 px).
Tái tạo: `chuan_bi.py` → `oai_e.py` (đã chạy, ảnh trong git) → `ghep_e.py` (+ `--bien`) → `chay_e.py`.

| Tấm | Đáp án (bằng mắt / theo cách dựng) | Phải |
|---|---|---|
| ngay | ghép đúng: toà có tên = render; AI vẽ lại nhà thường | N2P-1 (a) 0/255; (f1) 0; (f2) không báo; (g) không chữ |
| dem | ghép đúng, đêm | như ngay; (g) không chữ (cửa sổ sáng KHÔNG phải chữ) |
| xau | ghép đúng NHƯNG ảnh AI có ≥ 2 tháp bịa cao hơn hẳn toà có tên + ≥ 6 biển quảng cáo có chữ thương hiệu | (f2) báo; chữ báo (ngày → (w)) |
| ngay-thap_bia | tháp bịa (toa_1 phóng 1,9×) ở x 1180, đỉnh y ≈ 400 (cao hơn toa_2/toa_3 ≈ 80 px) | (f2) báo |
| ngay-thap_thap | tháp bịa 0,55× — thấp hơn mốc gần | (f2) KHÔNG báo |
| ngay-chu / dem-chu | 3 chữ dán (HOTEL, BANK, CAFE 24) trên mặt nhà thường | chữ báo; dem-chu → (g) lỗi |
| ngay-xoa_toa / ngay-doi_toa | toa_3 bị xoá / dời 30 px | N2P-1 (a) + (f1) lỗi |
| ngay-thuyen | thuyền dán trên sông | N2P-1 (a) lỗi |

Tiêu chí máy (đặt trước lượt đo đầy đủ): (f2) bắt xau + thap_bia, 0 báo ở ngay, dem, thap_thap; (g) máy: 0 chữ Latin ở ngay, dem, render; bắt ≥ 1 chữ ở
xau và ở chu (chữ nhỏ có thể sót — mô hình nhìn là lưới thứ hai). Tiêu chí mô hình nhìn (≥ 1 trong 2 mô hình, do_tin ≥ 0,5): tháp bịa ở xau và
thap_bia; không ở ngay, dem, thap_thap; chữ ở xau, dem-chu; không chữ ở ngay, dem; toà có tên `co_mat` ở mọi tấm (đã ghép lại) — báo mất/nhân đôi
ở tấm đúng là báo nhầm, ghi rõ. Mô hình không đạt tiêu chí → ghi số, KHÔNG sửa đề bài sau khi xem (một lượt), mức (f2) giữ Cảnh báo.

Minh bạch: ngưỡng máy (f2) THAP_GX chọn trên CHÍNH các tấm này (thử 1,0 / 2,0 / 3,0 — cả ba cùng tách đúng; chọn 2,0 ở giữa dải làm được), máy (g)
dùng ngưỡng sẵn có của PP-OCRv4 (textdet.py) — không phải kiểm độc lập; mô hình nhìn chạy MỘT lượt với đề bài viết trước khi xem kết quả.
