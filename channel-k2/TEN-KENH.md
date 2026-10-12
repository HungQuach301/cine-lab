# Tên kênh (mốc 1, bước 6)

> Đề xuất, chờ chủ dự án chọn. Kiểm ngày 11/10/2026 bằng YouTube Data API v3 (`collect.py names`): **3 search.list** (`type=channel`, `regionCode=US`, 10 kết quả/tên), `channels.list` đọc số người đăng ký, và `channels.list?forHandle=` kiểm handle (1 đơn vị/lượt). Số người đăng ký là số công khai API trả về, làm tròn theo YouTube.
> **Giới hạn:** API không cho biết handle có *đặt được* hay không (handle bị giữ, bị cấm, hoặc kênh ẩn không hiện). "Chưa thấy kênh" nghĩa là `forHandle` không trả kênh nào. Tôi **chưa kiểm nhãn hiệu (USPTO)** và tên miền.

## Định vị mới 12/10/2026: "cơ chế kinh tế của thành phố và ngành" (thay đề xuất bên dưới)
- **Kiểm ngày 12/10:** 2 search.list mới (`collect.py names2`, `type=channel`, US, 10 kết quả) + 4 lượt `forHandle`. "Moving Parts" dùng số kiểm 11/10 (bảng dưới), không tìm lại.
- Số người đăng ký là số công khai API trả về. **Chưa kiểm nhãn hiệu (USPTO) và tên miền.**

| Tên | Hợp định vị mới? | Kênh trùng/gần trùng lớn nhất (search.list) | Handle |
|---|---|---|---|
| **Moving Parts** (đề xuất 1) | **Còn hợp:** thành phố và ngành đều là "cỗ máy nhiều bộ phận", và tên không khoá kênh vào nhà máy. Nghiêng nhẹ về máy móc/ngành | (11/10) Không có kênh lớn cùng mảng; vài kênh trùng tên rất nhỏ (7 và 4 người đăng ký); ban nhạc "Tiny Moving Parts" | `@movingpartsecon` chưa thấy kênh (11/10) |
| **Main Street Machine** | Hợp nhất với T1: "Main Street" là thành phố/thị trấn, "Machine" là cơ chế | Không có kênh nào tên này; kết quả là các kênh lớn khác mảng (xe độ 4,86 triệu, nhạc), một kênh nhỏ "Santiago Street Machine" (52) | `@mainstreetmachine` **đã có kênh** · `@mainstreetmachineecon` chưa thấy kênh |
| **Townworks** | Hợp T1 ("town" + "works" = cách thị trấn vận hành), kém hợp T2 | Trùng gần với thương hiệu tuyển dụng Nhật **"タウンワーク" (Townwork)**: kênh chính thức 19,5 nghìn người đăng ký | `@townworks`, `@townworksecon` chưa thấy kênh |

- **Moving Parts**
  - *Ưu:* đã kiểm sạch, trung tính giữa T1 và T2; nếu thí điểm cho T2 thắng, tên vẫn đúng.
  - *Nhược:* không gợi thành phố; cụm từ phổ thông.
  - *Tác động:* dòng mô tả kênh cần nói rõ "cities and industries".
  - *Rủi ro:* nhãn hiệu chưa kiểm.
- **Main Street Machine**
  - *Ưu:* nói thẳng trụ chính T1, dễ nhớ.
  - *Nhược:* handle gốc đã có chủ; "street machine" là thuật ngữ giới xe độ ở Mỹ/Úc, nên tìm kiếm tên có thể lẫn với xe; dài hơn.
  - *Tác động:* phải dùng handle có hậu tố.
  - *Rủi ro:* nếu T2 thắng thí điểm, tên lệch trụ.
- **Townworks**
  - *Ưu:* ngắn, handle trống.
  - *Nhược và rủi ro:* gần trùng thương hiệu "Townwork" của một tập đoàn tuyển dụng Nhật, rủi ro nhãn hiệu và nhầm lẫn cao nhất; kém hợp T2.
- **Đề xuất:** giữ **Moving Parts** (`@movingpartsecon`), dự phòng **Main Street Machine**. Trước khi tạo kênh, chủ dự án kiểm handle trực tiếp và tra USPTO lớp 41.

## (Đề xuất 11/10, giữ để đối chiếu)

## Tiêu chí
- Nói được lời hứa "cơ chế phía sau" (`HIEN-CHUONG.md`), không gợi tư vấn tài chính (`LUAT-NOI-DUNG.md` §4).
- Ngắn, dễ đọc với khán giả Mỹ, không chứa tên công ty hay IP có sẵn.
- Không trùng kênh lớn trong cùng mảng.

## Ba tên
| Tên | Handle đề xuất | Kênh trùng/gần trùng lớn nhất (search.list) | Handle |
|---|---|---|---|
| **Moving Parts** (đề xuất 1) | `@movingpartsecon` | Không có kênh lớn cùng mảng. Kênh trùng tên đều rất nhỏ: "Moving Parts" `@movingpartsvideo` (7 người đăng ký), "Moving Parts" `@movingpartexplained` (4). Kênh lớn nhất trong kết quả là kênh khác mảng (79,3 nghìn, tên khác) và trang "Topic" của một ban nhạc tên "Tiny Moving Parts" | `@movingpartsecon`, `@movingpartsfilms`: chưa thấy kênh |
| **Throughput** | `@throughputecon` | Không có kênh nào tên "Throughput". Search trả về kênh "performance" không liên quan, lớn nhất 419 | `@throughputecon`, `@throughputfilms`: chưa thấy kênh |
| **Load Bearing** | `@loadbearingecon` | Nhiều kênh nhỏ dùng cụm này: "Load Bearing Ribbon" (4,38 nghìn), "Load Bearing Wall Pros" (3,45 nghìn), podcast "Load Bearing" (189), "Load-Bearing History" (43) | `@loadbearingecon`: chưa thấy kênh · `@loadbearingfilms`: **đã có kênh** |

## Ưu, nhược, tác động, rủi ro
- **Moving Parts**
  - *Ưu:* nói thẳng lời hứa "các bộ phận đang chạy phía sau một ngành"; hợp hình sa bàn 3D có chuyển động; dễ nhớ, dễ đọc.
  - *Nhược:* cụm từ phổ thông, có kênh nhỏ trùng tên, trong đó một kênh dạng "explained" (4 người đăng ký). Tìm kiếm tên kênh lúc đầu sẽ lẫn với ban nhạc "Tiny Moving Parts".
  - *Tác động:* cần hậu tố handle (`econ`) để tách biệt.
  - *Rủi ro:* nhầm với kênh nhỏ trùng tên nếu kênh đó lớn lên; nhãn hiệu chưa kiểm.
- **Throughput**
  - *Ưu:* sạch nhất trên YouTube (không kênh trùng); là thuật ngữ đúng của vận hành và điểm nghẽn (T1), hợp cả dòng tiền (T3).
  - *Nhược:* thuật ngữ kỹ thuật, khán giả phổ thông Mỹ có thể không hiểu ngay; khó gợi cảm xúc.
  - *Tác động:* cần dòng mô tả kênh rõ ("How industries really work") để bù độ khó.
  - *Rủi ro:* là từ phổ biến trong phần mềm và logistics; nhãn hiệu B2B có thể trùng.
- **Load Bearing**
  - *Ưu:* ẩn dụ mạnh ("thứ chịu lực" của nền kinh tế); hợp T1 và T2.
  - *Nhược:* trùng với nhiều kênh nhỏ khác mảng; handle `@loadbearingfilms` đã có chủ.
  - *Tác động:* phải dùng handle `@loadbearingecon`.
  - *Rủi ro:* dễ lẫn thương hiệu nhất trong ba tên.

**Đề xuất:** **Moving Parts** (`@movingpartsecon`), dự phòng **Throughput**. Trước khi tạo kênh, chủ dự án kiểm handle trực tiếp trên YouTube và tra USPTO TESS cho nhóm dịch vụ giải trí/giáo dục (lớp 41).

## Phép thử F1
Toàn bộ là phần riêng gói kênh. Không dùng gì từ lõi LL, trừ luật ghi nguồn và nhãn "tự tính".
