# Footage và ảnh nguồn ngoài — luật Q32 (checks LL v3 bản 1.10.0, phiên K, 12/10/2026)

Áp cho **Last Lamplighters** (`reports/m3/epXX/`) và **kênh 2** (`channel-k2/<tập>/`). Quyết định đầu vào: chủ dự án 12/10/2026 cho phép dùng footage/ảnh nguồn ngoài, ưu tiên miễn phí.
Bảng luật rút gọn ở `RULES-LL.md` (dòng Q32). Phiên xưởng đọc tệp này và `RULES-LL.md`, **không đọc** `q_footage.py`.

## 1. Nguồn cho phép
| Nguồn | Tên miền trang (`url_trang`) | Giấy phép nhận |
|---|---|---|
| Library of Congress | `loc.gov` | PD, CC0 |
| NARA | `archives.gov` | PD, CC0 |
| NASA | `nasa.gov` (images.nasa.gov) | PD, CC0 (không dùng insignia/logotype NASA) |
| Internet Archive (Prelinger) | `archive.org` | PD, CC0, CC BY, CC BY-SA (kiểm `licenseurl` từng item) |
| Wikimedia Commons | `commons.wikimedia.org/wiki/File:…` (trang của **đúng tệp**) | PD, CC0, CC BY, CC BY-SA (kiểm từng file) |
| Pexels | `pexels.com` | Pexels |
| Pixabay | `pixabay.com` | Pixabay |
| Nguồn khác | — | **Chủ dự án duyệt trước**, ghi `AUTHORSHIP.md`; sau đó phiên K thêm tên miền vào `DUYET_THEM` và khoá lại. Chưa có thì Q32a TRƯỢT |

Giấy phép có NC hoặc ND: luôn TRƯỢT (CLAUDE.md, luật cứng).

## 2. Sổ nguồn: `SOURCES-FOOTAGE.csv` cạnh `episode.yaml`
- LL: `reports/m3/epXX/SOURCES-FOOTAGE.csv`. Kênh 2: `channel-k2/<tập>/SOURCES-FOOTAGE.csv`.
- UTF-8, dấu phẩy, đúng 10 cột theo thứ tự (trùng mẫu `channel-k2/SOURCES-FOOTAGE.template.csv`):
```
clip_id,url_trang,url_tai,ngay_tai_utc,giay_phep,yeu_cau_ghi_cong,sha256,timecode_dung,nguoi_nhan_dien,logo
```
| Cột | Nội dung | Ví dụ |
|---|---|---|
| `clip_id` | mã duy nhất trong sổ, `[A-Za-z0-9][\w.-]*` | `LOC-01` |
| `url_trang` | trang của item (nơi ghi giấy phép) | `https://www.loc.gov/pictures/item/2017878800/` |
| `url_tai` | URL đã tải file | `https://tile.loc.gov/…/8b17067r.jpg` |
| `ngay_tai_utc` | ISO 8601 UTC, kết thúc bằng `Z` | `2026-10-12T08:32:00Z` |
| `giay_phep` | **bắt đầu bằng** PD / CC0 / CC BY / CC BY-SA / Pexels / Pixabay, sau đó tuỳ ý (phiên bản, URL, nguyên văn quyền) | `PD — LoC: No known restrictions on publication` · `CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0/` |
| `yeu_cau_ghi_cong` | câu ghi công **nguyên văn** sẽ đặt trong mô tả YouTube (bắt buộc với CC BY, CC BY-SA) | `Photo: "Langley computers" by Jane Doe, CC BY-SA 4.0, via Wikimedia Commons.` |
| `sha256` | SHA-256 của **file gốc đã tải và đã dùng khi render** (64 hex) | |
| `timecode_dung` | các đoạn dùng trong **bản cuối phim chính**: `m:ss.xx-m:ss.xx`, nhiều đoạn cách nhau `;` (phần sau dấu chấm là phần thập phân của giây; SMPTE `hh:mm:ss:ff` 24 khung/s cũng nhận). Các shot cùng clip kề nhau ghi thành **một** đoạn | `0:07.78-0:11.12;4:01.50-4:05.00` |
| `nguoi_nhan_dien` | `co` hoặc `khong`, có thể thêm ghi chú sau dấu `:`. Đã làm mờ/cắt để không còn nhận ra: ghi rõ ("co: đã làm mờ mặt") | `co: hai nhân viên văn phòng, mặt rõ` |
| `logo` | như trên cho logo/nhãn hiệu | `co: nhãn tủ máy, đã làm mờ` |

## 3. Khai trong EDL (đặc tả → timeline)
Đoạn footage = shot `tpl: footage` **hoặc** shot bất kỳ có `p.clip`. Tham số:
- `p.clip`: `clip_id` trong sổ (bắt buộc).
- `p.file`: đường dẫn file đã dùng khi render (**ngoài repo**). Không khai thì Q32 tìm `<clip_id>.*` trong `/var/tmp/k2-footage/<id tập>/`, `/var/tmp/ll-footage/<id tập>/`, `<out>/footage/`.
- `p.setting`: bối cảnh **theo nội dung hình** cho Q26b. Footage quay cùng nơi với một cảnh đinh 3D thì ghi khoá hoặc tên cảnh đinh (`heroes.<khoá>`); nơi khác ghi nhãn `ft/<nơi>` (ví dụ `ft/steel-mill`). Cùng một nơi thì cùng nhãn, dù nhiều clip.
- Footage là cảnh toàn khung (Q16) và hình vật chất (Q29), giống `archive`.

## 4. Luật Q32 (TRƯỢT khi…)
| Mục | TRƯỢT khi |
|---|---|
| a | Đoạn footage không có dòng sổ; sổ sai định dạng (cột, URL, ngày, SHA, giấy phép ngoài danh sách/NC/ND, nguồn ngoài danh sách, giấy phép không hợp nguồn, Wikimedia không trỏ trang `File:`); **SHA-256 file đã dùng ≠ sổ** hoặc không thấy file; `timecode_dung` không khớp đoạn dùng trong EDL phim chính (hai chiều, dung sai 0,05 s) |
| b | Footage + ảnh tư liệu (`archive`) **> 40 %** thời lượng tập (mỗi Short tính riêng); một clip hiện **liên tục > 8 s** (shot cùng clip cách nhau ≤ 1 khung gộp thành một lần) |
| c | Giấy phép CC BY / CC BY-SA mà `yeu_cau_ghi_cong` trống, hoặc câu đó không có nguyên văn trong mô tả YouTube (`<thư mục tập>/phat-hanh/*description*.txt`; bỏ khác biệt khoảng trắng, hoa/thường) |
| d | Người nhận diện được (`nguoi_nhan_dien=co`, không ghi làm mờ/cắt) hoặc logo rõ nét (`logo=co`, không ghi làm mờ/cắt) trong **ngữ cảnh tiêu cực**: lời đọc trong [đầu clip − 1 s, cuối clip + 1 s] hoặc chú thích của shot có từ thuộc danh sách tiêu cực (crime, fraud, bankrupt, addiction, scandal, failed/failure, layoffs, death, homeless, poverty, greed…). **Pixabay có logo rõ nét: luôn TRƯỢT** (giấy phép cấm dùng thương mại) |
| e | Cây git (mọi tệp đang theo dõi) có tệp media nằm trong thư mục có chữ `footage`, hoặc có tệp trùng SHA-256 với một dòng của **bất kỳ** sổ `SOURCES-FOOTAGE.csv` nào (bắt cả khi đổi tên/đuôi). Repo public: chỉ commit sổ CSV, không commit file |
| f | Đoạn footage không khai `p.setting` (Q26b gộp chúng vào `ft/(chưa khai)`) |
Sát ngưỡng ±5 % quanh 40 % và 8 s được nêu tên. Danh sách từ tiêu cực là luật thô: không thay rà của người; tình huống nhạy cảm vẫn theo `QUAN-TRI-RUI-RO.md` của kênh 2 và CHUAN-KENH-LL.

## 5. Chạy
- LL: `bash scripts/ll/qc.sh <episode.yaml>` (dòng **Q32**, mọi tập).
- Kênh 2 (hoặc chạy riêng): `/opt/cine/bin/python checks/ll/q_footage.py channel-k2/<tập>/episode.yaml [--tl <timeline.json>] [--desc <mô tả>]`; Q26b có footage: `checks/ll/q_setting.py <timeline.json>`. Mã thoát 1 = TRƯỢT.

## 6. Giấy phép Pexels và Pixabay — K đọc lại ngày 12/10/2026
**Cách đọc và giới hạn (nêu rõ):**
- 09:07:53 UTC: `curl` (User-Agent trình duyệt) tới `https://www.pexels.com/license/`, `https://pixabay.com/service/license-summary/`, `https://pixabay.com/service/terms/` → **HTTP 403** (5,6 KB, trang chặn bot).
- 09:08–09:10 UTC: Chromium headless (Playwright) → trang thử thách "Just a moment..." (Cloudflare), không qua được. Wayback Machine: 429 / ngắt kết nối từ proxy.
- ~09:12 UTC: đọc bằng công cụ WebFetch, yêu cầu trích nguyên văn. Công cụ này chuyển trang qua một mô hình nhỏ, nên chữ dưới đây là **nguyên văn theo WebFetch**, chưa đối chiếu bằng mắt. Với Pixabay, công cụ cắt 3 câu dài bằng "…" (giới hạn 125 ký tự). Không trang nào hiện ngày cập nhật.
- **Việc chờ chủ dự án:** mở hai trang bằng trình duyệt thường, đối chiếu chữ, ghi kết quả vào `AUTHORSHIP.md` trước tập đầu tiên dùng Pexels/Pixabay. Các trích dẫn này khớp với bản phiên P đọc ngày 12/10 08:30–08:40 UTC (`channel-k2/QUAN-TRI-RUI-RO.md` §6.2).

### Pexels — https://www.pexels.com/license/ (đọc 12/10/2026)
> "Legal Simplicity"
> "All photos and videos on Pexels can be downloaded and used for free."
> "What is allowed? 👌"
> "All photos and videos on Pexels are free to use."
> "Attribution is not required. Giving credit to the photographer or Pexels is not necessary but always appreciated."
> "You can modify the photos and videos from Pexels. Be creative and edit them as you like."
> "What is not allowed? 👎"
> "Identifiable people may not appear in a bad light or in a way that is offensive."
> "Don't sell unaltered copies of a photo or video, e.g. as a poster, print or on a physical product without modifying it first."
> "Don't imply endorsement of your product by people or brands on the imagery."
> "Don't redistribute or sell the photos and videos on other stock photo or wallpaper platforms."
> "Don't use the photos or videos as part of your trade-mark, design-mark, trade-name, business name or service mark."

### Pixabay — https://pixabay.com/service/license-summary/ (đọc 12/10/2026)
> "Use Content for free"
> "Use Content without having to attribute the author (although giving credit is always appreciated by our community!)"
> "Modify or adapt Content into new works"
> "You cannot sell or distribute Content (either in digital or physical form) on a Standalone basis."
> "Standalone means where no creative effort has been applied to the Content and it remains in substantially the same form..." *(bị công cụ cắt)*
> "If Content contains any recognisable trademarks, logos or brands, you cannot use that Content for commercial purposes..." *(bị công cụ cắt)*
> "In particular, you cannot print that Content on merchandise or other physical products for sale."
> "You cannot use Content in any immoral or illegal way, especially Content which features recognisable people."
> "You cannot use Content in a misleading or deceptive way."
> "You cannot use any of the Content as part of a trade-mark, design-mark, trade-name, business name or service mark."

### Luật rút ra (đã cài vào Q32)
| Câu giấy phép | Luật |
|---|---|
| Pexels "Identifiable people may not appear in a bad light…"; Pixabay "…immoral or illegal way, especially Content which features recognisable people" | Q32d: người nhận diện được không đặt cạnh lời/chữ tiêu cực (áp cho **mọi** nguồn, chặt hơn giấy phép) |
| Pixabay "If Content contains any recognisable trademarks, logos or brands, you cannot use that Content for commercial purposes" | Q32d: clip Pixabay có logo rõ nét luôn TRƯỢT (kênh kiếm tiền = dùng thương mại) |
| Pexels "Don't imply endorsement of your product by people or brands on the imagery" | Không đo được bằng máy; rà ở bảng kiểm trước đăng (kênh 2: `QUAN-TRI-RUI-RO.md` mục 4) |
| Không bắt buộc ghi công (cả hai) | Q32c không đòi ghi công cho Pexels/Pixabay; kênh vẫn nên ghi nguồn trong mô tả |
| Pixabay "misleading or deceptive"; YouTube "Misattributed content" | Không đo bằng máy; footage lưu trữ ghi năm trên hình (kênh 2 §6.5) |

## 7. Tương thích với luật cũ
- Shot `archive` (ảnh LoC/NARA của LL) vẫn theo **Q19** (RIGHTS.md, ≤ 20 %, ảnh nằm trong repo như bản đã duyệt). Q32 chỉ **cộng** thời lượng `archive` vào trần 40 %; Q32e không bắt ảnh `archive` đã commit vì chúng không có dòng trong sổ footage. Đây là điểm chủ dự án cần quyết (xem báo cáo 1.10.0): ảnh Q19 có phải chuyển sang sổ và bỏ khỏi git hay không.
- Footage được thêm vào nhóm cảnh toàn khung của Q16 và hình vật chất của Q29; Q26b gán bối cảnh theo `p.setting`. Tập không có footage: kết quả mọi luật cũ không đổi (selftest các tập 2–8 giữ nguyên).
