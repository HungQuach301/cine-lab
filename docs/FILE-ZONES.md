# VÙNG TỆP — loại phiên nào được sửa tệp nào

> Phiên Nền tảng soạn ngày 15/10/2026. **Chủ dự án duyệt 15/10 (NT K2).** Bảng tổng hợp từ CLAUDE.md (mục "Vai trò"), KE-HOACH mục 5.3 và cách các phiên đã làm tới 14/10. Khi lệnh giao ghi khác, lệnh thắng, nhưng phải ghi rõ trong khối điều lệ (`docs/SESSION-CHARTER.md`).

## 1. Ký hiệu
- **S** = được sửa · **+** = chỉ ghi thêm ở cuối, mã dòng `<tiền tố>-<số>` · **R** = chỉ đọc · **✗** = không đọc mã (chỉ chạy công cụ) · `<tập>` = thư mục của tập được giao.

## 2. Bảng vùng
| Đường dẫn | P (điều phối) | K (kiểm định) | Tập / xưởng (T2, LL09…) | V (bộ công cụ hình) | M (thị trường) | NT (nền tảng) |
|---|---|---|---|---|---|---|
| `checks/` | R, chạy | **S** (chỉ K; khoá SHA `checks/LOCK`) | ✗ (chỉ chạy) | ✗ (chỉ chạy) | ✗ | R, chạy `lock.py --verify` |
| `checks-appeal.md` | + | S (trả lời) | + | + | + | + |
| `bible/`, `docs/BIBLE-KENH2.md` | S khi chủ dự án duyệt nguyên văn | R | R | R | R | R |
| `PLAN.md`, `PLAN-HANDOFF-P.md`, bảng shot | **S** (chỉ P) | R | R | R | R | R |
| `AUTHORSHIP.md` | + | + | + | + | + | + |
| `RIGHTS.md` | + | R | + | + | + | + |
| `reports/m3/BAI-HOC-LL.md`, `channel-k2/BAI-HOC-K2.md` | + | + | + | + | + | + |
| `COST-LEDGER.csv` | + | + | + | + | + | + |
| `channel-k2/<tập>/`, `reports/m3/<tập>/` | R (S khi gom/khép tập) | R | **S** (chỉ tập được giao) | R | R | R |
| `channel-k2/k2v*-mau/` (cuộn mẫu) | R | R | R | **S** | R | R |
| `scripts/k2/`, `design/k2v/` | R | ✗ | R (sửa phải được giao trong lệnh) | **S** | R | R (đo, không đổi mã dựng) |
| `design/ll-hero/<tập>.js` | R | ✗ | **S** (cảnh của tập mình) | R | R | R |
| `design/ll-hero/kit.js`, `k2page.js`, `page.js`, `design/cong3/shared/` | R | ✗ | R (sửa phải được giao) | S khi được giao | R | R |
| `scripts/ll/` | S (nhà máy LL) | ✗ | R | R | R | R |
| `toolkit/market/`, `market-k2/` | R | R | R | R | **S** | R |
| `scripts/common/`, `tools/` | R | R | R | R | R | **S** |
| `docs/` (trừ `BIBLE-KENH2.md`), `RUNBOOK-*`, `CHUAN-KENH-*` | S | R | R | R | R | **S** |
| `scripts/env/` | S | R | R | R | R | S khi được giao |
| `assets/` (nhạc, font, SFX đã có quyền) | S | R | + (thêm tài sản mới kèm dòng RIGHTS) | + | R | R |
| `CLAUDE.md` | chỉ chủ dự án | — | — | — | — | — |

## 3. Luật đi kèm
1. **Một tệp — một chủ ở một thời điểm.** Hai phiên chạy song song không được cùng có quyền **S** trên một tệp. P kiểm khi giao lệnh. Tệp dùng chung (**+**) là ngoại lệ duy nhất.
2. **Ghi thêm không sửa:** dòng mới đặt ở cuối bảng/mục của mình, mang mã `<tiền tố>-<số>`. Sửa dòng cũ (vd đổi cột "luật hiện hành" của BAI-HOC) là việc của P, sau khi chủ dự án duyệt.
3. **Tiền tố phiên** (dùng trong mã dòng, tên nhánh gợi ý, `COST-LEDGER.csv`): `P` điều phối · `K` kiểm định · `T<n>` tập kênh 2 · `LL<nn>` tập Last Lamplighters · `V<n>` bộ công cụ hình · `M` thị trường · `NT` nền tảng · `C` tra nguồn (Cowork).
4. **Sửa ngoài vùng** → không sửa; ghi đề xuất trong báo cáo, P giao lại cho đúng loại phiên.
5. **Merge:** chỉ P merge vào `main`, và chỉ giữa hai tập (không merge vào lúc một phiên tập đang dựng trên `main` cũ), để bộ công cụ không đổi dưới chân một tập. `VERSIONS.yaml` của tập bắt các lệch còn sót.
