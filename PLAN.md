# PLAN — Bảng điều phối (phiên P duy trì)

## Mốc hiện tại: M0 — Hạ tầng và Cổng 0 — **DỪNG, chờ duyệt** (báo cáo: `reports/m0/BAO-CAO-M0.md`)

## Hàng chờ chủ dự án duyệt
| # | Việc | Phương án (khuyến nghị in đậm) |
|---|---|---|
| Q1 | Nghe chấm mù giọng + nhạc | `reports/m0/NGHE-CHAM-M0.html`; gửi thêm ≥ 3–5 người nghe mù |
| Q2 | Phong cách hình | A 2D Canvas · **B 2.5D three.js (+ lớp 2D)** · C Blender |
| Q3 | Nguồn nhạc | **A ACE-Step làm nhạc chính (nếu tai đạt)** · B nhạc sinh bằng mã · C bản thu PD/CC |
| Q4 | Giọng | Chọn sau Q1; **ưu tiên giọng Voice Design lưu vào tài khoản nếu điểm ngang giọng thư viện** |
| Q5 | Số phiên song song M1–M2 | A P+K+1 · **B P+K+2 phiên cloud riêng** · C P+K+4 |
| Q6 | Allowlist mạng | **Thêm `download.pytorch.org`** (torch CPU cho ACE-Step) |
| Q7 | Dán `scripts/env/setup.sh` mới vào môi trường | — |
| Q8 | Model sheet M0 chỉ là bản thử; thiết kế nhân vật thật do chủ dự án quyết ở M1 (AUTHORSHIP.md) | — |

## Quy ước (rút từ M0)
- Worktree của subagent tạo từ `main`: P commit bible/mã chung lên `main` trước khi giao; hoặc giao kèm lệnh `git checkout <commit> -- <paths>`.
- Render nặng và ACE-Step: mỗi việc một phiên cloud riêng; không chạy chung máy.
- Video > 30 MB: đẩy lên nhánh git, không gửi qua giao diện.

## Bảng gói việc
| Gói | Phiên/agent | Nhánh | Trạng thái | Báo cáo |
|---|---|---|---|---|
| M0-W-CONS-A | subagent cine-worker (worktree) | worktree-agent-a455537e… → đã merge | Xong | shots/m0-consistency/shot-A/README.md |
| M0-W-CONS-B | subagent cine-worker (worktree) | worktree-agent-aed90748… → đã merge | Xong | shots/m0-consistency/shot-B/README.md |
| M0-W-PAR-1 | subagent cine-worker (worktree) | worktree-agent-a1476954… → đã merge | Xong | reports/m0/parallel/w1.json |
| M0-W-PAR-2 | subagent cine-worker (worktree) | worktree-agent-a96c56a4… → đã merge | Xong | reports/m0/parallel/w2.json |
