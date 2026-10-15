# CHUẨN KÊNH — Kênh 2 "Moving Parts"

> Phiên Nền tảng soạn ngày 15/10/2026 theo lệnh chủ dự án ngày 13/10 (mục 8). **Chủ dự án duyệt 15/10 (NT K2)**, ghi `AUTHORSHIP.md`.
> **Nguyên tắc tối cao (CLAUDE.md, 06/10/2026)** đứng trên mọi mục: chất lượng và sự liền mạch không bao giờ được hy sinh.

## 0. Thứ bậc tài liệu
1. **`docs/BIBLE-KENH2.md` (Kinh thánh kênh 2)** là gốc cho định vị, chọn đề tài, khuôn lời, ngữ pháp hình, gói phát hành, quy trình và thước đo. Tệp này **không chép lại** Kinh thánh; chỉ cụ thể hoá phần vận hành (gói phát hành, giới hạn ký tự, kiểm). Mâu thuẫn → Kinh thánh thắng, ghi lại để chủ dự án sửa một trong hai.
2. Luật nội dung: `channel-k2/LUAT-NOI-DUNG.md`, `channel-k2/LUAT-NOI-DUNG-G.md`; rủi ro: `channel-k2/QUAN-TRI-RUI-RO.md`; nhận diện: `channel-k2/NHAN-DIEN.md`; bài học: `channel-k2/BAI-HOC-K2.md`.
3. Luật kiểm tự động: `checks/` (chỉ phiên K sửa). Vận hành phiên: `docs/SESSION-CHARTER.md`, `docs/FILE-ZONES.md`, `docs/RUNBOOK-MOI-TRUONG.md`.

## 1. Gói phát hành (Kinh thánh §5; quyết định chủ dự án 13/10 22:17 khi G2 T1)
| Thành phần | Chuẩn |
|---|---|
| Master | 1920×1080, 24 fps, −14 LUFS, đỉnh ≤ −1 dBTP; `SHA256SUMS.txt` |
| **Short** | **đúng 1 Short** mỗi tập (1080×1920). Móc mở bằng câu hỏi/nghịch lý của tập, trả lời bằng một sự thật có nguồn trong tập. Đặc tả `shorts:` chỉ 1 mục |
| Phụ đề | `.en.srt` theo timeline thật |
| **Mô tả** | **≤ 5 000 ký tự** (giới hạn YouTube; đếm ký tự Unicode, không đếm byte). Gồm: miễn trừ, "Facts as of …" khi có luật/số đang hiệu lực, chương theo timeline thật, ghi công ngắn, câu dẫn tới bình luận ghim. Năm/số trong mô tả chỉ lấy từ lời hoặc danh sách claim (BAI-HOC-LL #53) |
| **Nguồn đầy đủ** | ở **bình luận ghim** (`nguon-binh-luan-ghim.en.txt`, ≤ 10 000 ký tự): mọi URL + ngày truy cập, bản ghi ảnh/tài liệu/footage, giấy phép. Trên hình chỉ tên nguồn ngắn ≥ 38 px (Kinh thánh §4) |
| Tiêu đề | 3 phương án (`titles.txt`), dạng nghịch lý/câu hỏi, không hứa vượt claim (QUAN-TRI-RUI-RO mục 2) |
| **PACKAGING-BRIEF** | `PACKAGING-BRIEF.md` + 2–3 ảnh nền 1280×720 **không chữ** lấy từ khung 1080p của tập: ý thumbnail (bản đồ thật, vùng tô nổi, một số hoặc 1–2 từ lớn trong hộp, tối đa 2 biểu tượng — Kinh thánh §2), chữ gợi ý ≤ 4 từ có trong video, bố cục, bảng màu đo trên ảnh nền, prompt mẫu |
| **Thumbnail** | **chủ dự án tự làm** theo brief, chọn bằng YouTube Test & Compare. Nhà máy **không** làm thumbnail hoàn chỉnh; Q12 (lề thumbnail) không áp cho gói nhà máy |
| Màn hình kết thúc | video nối trong chuỗi của kênh 2; **không** liên kết chéo sang Last Lamplighters (QUAN-TRI-RUI-RO, "Liên kết chéo") |

## 2. Kiểm gói trước G2 (đọc + máy, không thêm cổng)
- Độ dài mô tả và bình luận ghim (ký tự Unicode):
  `python3 -c "import sys;[print(f, len(open(f,encoding='utf-8').read())) for f in sys.argv[1:]]" description.en.txt nguon-binh-luan-ghim.en.txt`
  Mô tả > 5 000 → chặn, chuyển phần nguồn sang bình luận ghim. Ghi nhận: gói Steel (`release-k2g-ep01-v1`) có mô tả **5 502 ký tự** — vượt giới hạn, có trước chuẩn này; gói T1 4 585 ký tự (đạt).
- Đúng 1 tệp Short trong gói; `SHA256SUMS.txt` phủ master, Short, `.srt`, mô tả, bình luận ghim.
- Mọi footage/ảnh ngoài: dòng `SOURCES-FOOTAGE.csv` + `licenses/<clip>.txt` + `RIGHTS.md` (`tools/preflight.sh` chặn khi thiếu tệp giấy phép).
- `VERSIONS.yaml` của tập: `scripts/common/versions.py check` ở G2.
