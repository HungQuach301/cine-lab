# COST-LEDGER — sổ chi phí mỗi phiên (hướng dẫn)

> Phiên Nền tảng soạn ngày 15/10/2026. Sổ: `COST-LEDGER.csv` (gốc repo, tệp dùng chung, **chỉ ghi thêm**). Mốc gốc T1, Steel, V1–V4 điền từ báo cáo có sẵn (cột `nguon` ghi tệp:dòng).

## 1. Khi nào ghi
- **Cuối mỗi phiên, hoặc mỗi cổng của một tập** (G1, G1b, G2, G3): một dòng. Phiên tập ghi một dòng cho mỗi cổng.
- Không sửa dòng cũ. Ghi sai thì thêm dòng mới, `ghi_chu` = "sửa dòng <phien>/<cong>: …".

## 2. Cột
| Cột | Nghĩa | Lấy từ đâu |
|---|---|---|
| `phien` | tiền tố phiên (`docs/FILE-ZONES.md` §3): `T2`, `V4`, `NT`, `P-K2C`… | lệnh giao |
| `tap_hoac_moc`, `cong`, `ngay` | tập hoặc mốc; cổng (G1/G1b/G2/G3/V…); ngày nộp (YYYY-MM-DD) | — |
| `quota_pct` | % hạn mức gói Claude của chủ dự án mà phiên dùng | chủ dự án đọc trên trang Usage (máy không đọc được) — để trống nếu chưa có |
| `tok_sinh_M`, `tok_cache_ghi_M`, `tok_cache_doc_M` | triệu token sinh ra / đầu vào mới (ghi cache) / đọc cache **của phiên** (gồm subagent) | trường `usage` trong log phiên, khử trùng theo mã tin nhắn (BAI-HOC-LL #56); không ước theo cảm giác |
| `claude_api_usd`, `tran_api_usd`, `model_ghim` | $ Claude API dự án trả (`claude -p`, kiểm mù, REVIEWER), trần lệnh giao, model ghim | tổng `usd` trong `cost.jsonl` của phiên |
| `el_ky_tu_gui`, `el_ky_tu_bo_dem` | ký tự gửi ElevenLabs; chênh bộ đếm tài khoản trước/sau | log thu giọng; `GET /v1/user/subscription` trước/sau |
| `gio_render` | giờ máy dựng (nháp + 1080p + sửa), đồng hồ thật | `build.log`, `measure-*.json` |
| `gio_lich_tu_cong_truoc` | giờ lịch từ lúc chủ dự án duyệt cổng trước tới lúc nộp cổng này | dấu giờ duyệt trong `AUTHORSHIP.md` |
| `cham_chu_du_an` | số lần chủ dự án phải can thiệp trong khoảng này (duyệt cổng + lệnh/xác nhận giữa chừng) | báo cáo cổng |
| `thoi_luong_s`, `ty_le_relief_pct` | độ dài sản phẩm (giây), % thời lượng là cảnh relief | timeline |
| `nguon`, `ghi_chu` | tệp:dòng của số liệu; ghi chú ngắn, không dấu phẩy kép | — |

## 3. Luật
- Số đo thật thắng số tự khai. Không có số thì để trống, không đoán. Cột trống được tính là "chưa đo" khi so tập.
- Dấu thập phân là dấu chấm (CSV), số không có dấu phân cách nghìn.
- So T2 với T1 (Kinh thánh §8: "giờ render và token/tập ≤ T1; chủ dự án ≤ 3 lần chạm") bằng tổng các dòng của từng tập.
