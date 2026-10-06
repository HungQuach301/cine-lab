# PLAN — Bảng điều phối (phiên P duy trì)

## Trạng thái hiện tại (06/10/2026)
- **Kênh:** Last Lamplighters. Chuẩn: `reports/m3/CHUAN-KENH-LL.md`. Bài học: `reports/m3/BAI-HOC-LL.md` (đọc khi khởi động).
- **Nhánh làm việc:** `ccr-8a2b38d7-rk5x31` (từ `claude/modest-volta-7w7y40` f11e729). Nhánh phát hành: `release-ll-ep0N-v1` (Git LFS).
- **Lô tập 3–5: XONG** (G1 `reports/m3/LO-3-5-G1.md`; tổng kết `reports/m3/LO-3-5-TONG-KET.md`). Chờ lệnh lô tiếp theo (tập 6 "The Hand That Drew It") và định nghĩa trần token.

| Tập | Trạng thái | Kế hoạch tập |
|---|---|---|
| 2 "Hello, Central" | G3: chủ dự án đăng | `reports/m3/HUONG-DAN-DANG-TAP2.md` |
| 3 "The Teller's Window" | G3: chủ dự án tự đăng (`reports/m3/HUONG-DAN-DANG-TAP3.md`) | `reports/m3/ep03/PLAN.md` |
| 4 "The Typing Pool" | G3: chủ dự án tự đăng (`reports/m3/HUONG-DAN-DANG-TAP4.md`) | `reports/m3/ep04/PLAN.md` |
| 5 "The Claims Desk" | G3: chủ dự án tự đăng (`reports/m3/HUONG-DAN-DANG-TAP5.md`) | `reports/m3/ep05/PLAN.md` |

## Luật làm việc
- 3 cổng (G1 kịch bản, G2 bản cuối, G3 phát hành). Ngoại lệ phải hỏi: CHUAN-KENH §7.
- qc nhà máy Q1–Q22 (Q21 gán nguồn, Q22 chữ tràn khung từ 06/10/2026). Thư viện tự thu cỡ chữ phủ trên khung từ tập 6.
- Mẫu lệnh cho phiên: `playbook/prompts/` (P-G1-LO, P-SAN-XUAT, P-G3). Mẫu kế hoạch tập: `playbook/PLAN-TAP-MAU.md`.
- Video > 30 MB: đẩy lên nhánh git, không gửi qua giao diện. Chỉ P merge vào `main`.

## Lịch sử
- Trước 05/10/2026 (M0–M2, Cổng 1–6, tập thử, Mốc B, tập 2): `reports/archive/PLAN-LICH-SU-2026-10-05.md`.
