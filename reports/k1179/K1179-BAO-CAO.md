**Nhánh thật: `ccr-196e0bda-gcj9iw`** (harness buộc tên này; lệnh ghi `checks-1-17-9`). Gốc origin/main **@41de7ce3** (đỉnh đúng như lệnh; LOCK 1.17.8 `045b7bb7…` KHỚP). Không merge, không đụng `main`, P-2610c, `docs/`, sổ, `channel-k2/**`, `scripts/`, `design/`, `tools/` hay nhánh khác. Đầu vào A @bc1693b5 chỉ ĐỌC (`git archive` → `/var/tmp/k1179/in`).

# Phiên K-1.17.9 — xét khiếu nại BAN-CUOI-T4-A (KN-1, KN-2, KN-4…KN-7; KN-3 rút) + KN-8 (điều phối) — BÁO CÁO

> Phiên K, 26/10/2026 03:12 → {{GIO_KET}} UTC (10:12 → {{GIO_KET_VN}} Asia/Saigon). Mọi số là số đo thật trong phiên; tệp số đo ở `reports/k1179/do/`.
> Căn cứ (nguyên văn, Asia/Saigon): chủ dự án 26/10 07:39 chọn hướng (a) cho H3-05b (→ KN-7); chủ dự án dán lệnh phiên này = **"Duyệt PHIẾU-A theo khuyến nghị điều phối"** — giờ dán ghi theo giờ mở phiên: **26/10 ≈ 10:12 Asia/Saigon (03:12 UTC)**; 26/10 00:07 "Chọn hướng cho cảnh hiện đại: A+B+E (khuyến nghị)"; 25/10 09:08 "…các vấn đề khác đều có thể nới…".
> Phiên K KHÔNG có văn bản "khuyến nghị điều phối" cho PHIẾU-A (không nằm trong đầu vào được giao) → không suy ra lựa chọn E1/Q-A… nào đã duyệt; mọi ngoại lệ trong phiên là **khai thử**, không phải duyệt thật (§2 KN-1).
> Email chủ dự án không có trong tệp, commit, header, URL, payload hay User-Agent nào (UA `CineLab-research (+https://github.com/HungQuach301/cine-lab)`). Không in/ghi khoá (proxy gắn khoá).

## 0. Khối điều lệ và tóm tắt
| Trường | Lệnh | Thực tế |
|---|---|---|
| Nhánh | `checks-1-17-9` từ origin/main @41de7ce3 | harness buộc `ccr-196e0bda-gcj9iw` (dòng đầu); gốc đúng @41de7ce3 |
| Vùng sửa | `checks/**`, `checks-appeal.md`, `reports/k1179/**` | đúng |
| Khiếu nại trước phán quyết | — | chép nguyên văn KN-1…KN-7 + KN-8 vào `checks-appeal.md` commit `747ab420` 03:17 UTC, trước mọi phán |
| Preflight / hook | `set -o pipefail`; commit chỉ khi "— ĐẠT"; hook trước lần đẩy đầu | hook pre-commit + pre-push cài 03:13 (lần đẩy đầu 03:17); `day.sh` kiểm "— ĐẠT" + "PREFLIGHT ĐẠT" trước commit |
| `lock.py` không `--verify` | đúng một lần, bước khoá | **đúng một lần** 03:54:51 UTC → `9eddaf24…`; preflight quét `checks/` trước khoá (bắt 1 email giả trong selftest — sửa trước khoá) |
| Đẩy ≤ 30 phút + CHECKPOINT | bắt buộc | {{DAY}} |
| Force/amend/dừng hỏi | không | không |
| Chi phí | Claude mốc $3 (chặn $8), OpenAI mốc $2 (chặn $5), Gemini 0, không sinh ảnh/video | **OpenAI $0,313 · Claude API $0,699 · Gemini 0 · 0 ảnh/video sinh** (§11) |

**Tóm tắt phán quyết:**
| KN | Phán | Một dòng |
|---|---|---|
| KN-1 | **MỘT PHẦN — LỖI LUẬT** | `ngoai_le` + `duyet_chu_du_an` hạ báo MÔ HÌNH "bờ" xuống (w) khi máy sạch; máy không miễn |
| KN-2 | **MỘT PHẦN** | beats `bien_co_tl` tự khai GIỮ LUẬT; LỖI LUẬT nhỏ: cộng biến cố ĐO từ log máy (mặt trời, pha máy) — Q37 vẫn trượt vì **nhịp thật** (39 khoảng > 6 s) |
| KN-4 | **LỖI MÃ** (cat_clip) · GIỮ LUẬT (lọc trời) | H1-15b trong `cat_clip` 0,062 → hết (a) |
| KN-5 | **LỖI LUẬT** | "toà có tên" = tháp ≥ 75 m ODN / lịch sử (`nguon_lich_su`) / St Paul's |
| KN-6 | **MỘT PHẦN** (chấp nhận có điều kiện) | đẩy/trượt 2D ≤ 1,5 %/s = MỘT phép 2D cả khung; (a)-E khác quỹ đạo → (h) |
| KN-7 | **CHẤP NHẬN** (chặt thêm: tính cả hộp 0,60–0,75) | H3-05b: YuNet 0,070, 4 nơi đã tra, AUTHORSHIP 00:12 → miễn (k) |
| KN-8 | **MỘT PHẦN** (sửa cách giữ bờ; T9c không làm thước) | nước AI + bờ PHÍA ĐẤT; dải ±8 px cả hai phía → viền xanh; mô hình bắt 2/2 ca âm, 0 nhầm |

LOCK **1.17.8 `045b7bb7…` → 1.17.9 `9eddaf24e8c5276b6017af172e7c8185ba21831a7b6e842cc17094fd5c66fc34`**, `--verify` KHỚP. Selftest {{ST}}. T3 1.17.8 ↔ 1.17.9: {{T3}}.

{{THAN}}
