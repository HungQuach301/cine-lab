# ĐIỀU LỆ PHIÊN — mẫu bắt buộc cho mọi phiên Claude Code trên repo

> Phiên Nền tảng soạn ngày 15/10/2026, theo lệnh chủ dự án ngày 13/10 (phiên Nền tảng). **Chờ chủ dự án duyệt** trước khi áp. Nguyên tắc tối cao (CLAUDE.md, 06/10) đứng trên mọi mục dưới đây.
> Đọc kèm: `docs/FILE-ZONES.md` (vùng tệp của từng loại phiên) và `docs/RUNBOOK-MOI-TRUONG.md` (môi trường, nguồn tư liệu, giờ máy).

## 1. Cách dùng
- Phiên P (hoặc chủ dự án) dán khối §2 vào **đầu lệnh giao** cho mỗi phiên mới và điền đủ các trường.
- Phiên nhận lệnh chép khối đã điền vào đầu báo cáo cuối phiên, thêm cột "thực tế" (chi phí thật, tệp thật đã sửa, điều kiện dừng thật).
- Trường nào để trống thì lấy giá trị mặc định ở §3. Muốn khác mặc định phải ghi rõ trong lệnh.

## 2. Khối điều lệ (chép nguyên khối, điền vào chỗ `<…>`)
```text
ĐIỀU LỆ PHIÊN <tiền tố>  (ví dụ T2, V5, NT, K, P, M, LL09)
Loại phiên:        <P | K | tập (xưởng) | V (bộ công cụ hình) | M (dữ liệu thị trường) | NT (nền tảng)>  — vùng tệp: docs/FILE-ZONES.md
Nhánh:             <tên nhánh>, tạo từ <origin/main | commit/nhánh cụ thể> @ <SHA 7 ký tự>
Tệp được sửa:      <danh sách thư mục/tệp; mọi chỗ khác chỉ đọc>
Tệp KHÔNG được sửa: checks/ (trừ K) · bible/ · tài sản đã khoá · vùng của phiên khác đang chạy: <liệt kê>
Tệp dùng chung:    AUTHORSHIP.md, RIGHTS.md, reports/m3/BAI-HOC-LL.md, channel-k2/BAI-HOC-K2.md, COST-LEDGER.csv — CHỈ GHI THÊM ở cuối, mã dòng <tiền tố>-<số>
Trần chi phí:      Claude API $<n> (ghim model <claude-…>, ghi cost.jsonl) · ElevenLabs <n> ký tự · giờ render <n> · token: trần mềm (Nguyên tắc tối cao)
Đầu vào bắt buộc:  <tài liệu phải đọc trước khi làm>
Đầu ra:            <báo cáo + tệp/commit cụ thể>
Điều kiện dừng:    (1) xong việc và nộp báo cáo; (2) chạm trần chi phí cứng (Claude API $, ElevenLabs); (3) lỗi chặn không tự gỡ được
                   (quyền, mạng, dữ liệu nguồn sai, luật K mâu thuẫn); (4) cuối mốc/cổng có quy định DỪNG.
KHÔNG dừng hỏi lại giữa chừng. Câu hỏi không chặn thì tự chọn phương án an toàn nhất cho chất lượng, ghi lý do vào báo cáo,
và đưa vào mục "Việc chờ chủ dự án".
Merge:             <phiên này KHÔNG merge | P merge sau duyệt, chỉ giữa hai tập>
```

## 3. Mặc định khi lệnh không ghi
| Trường | Mặc định |
|---|---|
| Nhánh | nhánh riêng của phiên, tạo từ `origin/main`; không đẩy lên nhánh khác |
| Tệp được sửa | đúng vùng của loại phiên trong `docs/FILE-ZONES.md` |
| Trần Claude API | $3 mỗi phiên, model ghim theo lệnh; không ghim được → không gọi API |
| ElevenLabs | 0 ký tự (chỉ phiên tập được thu giọng, trần ghi trong G1) |
| Giờ render | theo ước ở G1 + 30 %; vượt thì vẫn làm nếu cần cho chất lượng, ghi số đo thật |
| Token | trần mềm: vượt để giữ chất lượng thì làm và báo cáo |
| Merge | phiên không merge; chỉ P merge vào `main`, và chỉ trong khoảng giữa hai tập (không merge khi một tập đang dựng) |

## 4. Luật chạy phiên
1. **Đầu phiên:** `bash scripts/env/verify.sh`; đọc các tài liệu ghi trong "Đầu vào bắt buộc"; phiên P đọc `reports/m3/BAI-HOC-LL.md` (CLAUDE.md).
2. **Không dừng hỏi giữa chừng.** Chỉ dừng ở 4 điều kiện của khối §2. Câu hỏi không chặn → tự quyết theo chất lượng, ghi lý do, đưa vào "Việc chờ chủ dự án".
3. **Tệp ngoài vùng:** cần sửa tệp ngoài "Tệp được sửa" → không sửa; ghi đề xuất (đường dẫn, nội dung, lý do) vào báo cáo. Khiếu nại luật K → `checks-appeal.md`.
4. **Tệp dùng chung chỉ ghi thêm.** Không sửa, không xoá, không sắp lại dòng của phiên khác. Mỗi dòng mới có mã `<tiền tố>-<số>` tăng dần trong phiên (ví dụ `NT-01`, `T2-03`). Bảng có cột "#" thì ghi mã vào cột đó. Hai phiên cùng ghi thêm vào cuối một tệp sẽ xung đột khi merge; xung đột kiểu này P giải bằng cách giữ cả hai khối, theo thứ tự thời gian.
5. **Chi phí:** mỗi lần gọi Claude API ghi một dòng vào `<thư mục việc>/cost.jsonl` (`model`, `served`, `tag`, `usd`). Cuối phiên ghi **một dòng** vào `COST-LEDGER.csv` (`docs/COST-LEDGER-HUONG-DAN.md`).
6. **Đóng băng phiên bản (phiên tập):** ghi `VERSIONS.yaml` lúc G1 (`scripts/common/versions.py record`), kiểm lúc G2 (`versions.py check`). Lệch → nêu tên trong báo cáo G2, không tự ghi đè.
7. **Trước mỗi lần đẩy:** `bash tools/preflight.sh --range origin/main..HEAD` phải ĐẠT (hoặc cài hook, xem đầu tệp `tools/preflight.sh`).
8. **Media:** tệp > 30 MB không gửi qua giao diện; media trung gian, footage, ảnh gốc, trọng số ở ngoài git, chỉ ghi SHA. LFS chỉ cho gói phát hành (`tools/lfs-allow.txt`).
9. **Cuối phiên:** commit → đẩy nhánh của phiên → báo cáo tiếng Việt gồm: kết quả, số đo thật, chỉ số trong ±5 % quanh ngưỡng, chi phí thật, tệp đã sửa, xung đột khi ghép thử với `main` và các nhánh đang chạy, **việc chờ chủ dự án**.
10. **Tiến trình nền:** chạy bằng công cụ chạy nền của harness, không dùng `&`; dừng tiến trình bằng PID, không dùng `pkill -f` (BAI-HOC-LL #24, #38, #41).
