# Hàng đợi khiếu nại cho phiên K kế (P-1710, 17/10/2026)

> Phiên P-1710 soạn theo lệnh chủ dự án 17/10 (mục 5). P **không sửa và không đọc mã** `checks/`; mọi mục dưới đây là hiện tượng đo được, vì sao nêu và đề nghị. Cách đo cuối cùng do K quyết, viết selftest có ca ĐẠT và ca TRƯỢT, rồi chủ dự án duyệt.
> Đầu vào: `channel-k2/k2c-t2-01/G2-BAO-CAO.md` §13–§14 (TT5), `reports/K-1.12.2-BAO-CAO.md`, `channel-k2/BAI-HOC-K2.md` K13–K17. LOCK hiện hành: **1.12.2** `81789fad2e7a986a092cd2c0659a1cb93b3b5f9e87e4cfc79f7a93e316506e93`.

| # | Luật | Nguồn | Tóm tắt | Ưu tiên |
|---|---|---|---|---|
| KN-1 | Q7/Q8 (QC LL) | TT5 (i) | nhận `kind: estimate` của kênh 2 | cao: TRƯỢT áp nhầm ở mọi tập kênh 2 có ước tính |
| KN-2 | Q36(b) (k2check) | TT5 (ii) | câu miễn trừ một lần trong 0:00–0:15 không bị tính lỗi | cao |
| KN-3 | Q33 / Q33-K2 (pHash) | lệnh 17/10 | bỏ lớp chữ cố định (chip nơi dựng, tấm chữ) trước khi băm | vừa |
| KN-4 | `versions.py` | G2 §12.3, §13.7 | miễn trừ `served_models` đã duyệt | vừa (ghi chú: tệp ở `scripts/common/`, vùng Nền tảng) |
| KN-5 | Q37 / `scripts/k2/rhythm.py` | lệnh 17/10 | đo khung tĩnh trên điểm ảnh, không chỉ trên đặc tả | vừa |
| KN-6 | **luật mới VV2** | chủ dự án duyệt 17/10 | thành phố phải có nhà/phố đúng thời kỳ; địa cầu/độ cao lớn ≤ 1 lần/tập, ≤ 3 s | cao: áp cho T3–T6 |

## KN-1 · Q7/Q8 nhận `kind: estimate` cho kênh 2
- **Hiện tượng (T2 L4–L5):** `qc.py` Q7 đòi nhãn ESTIMATE nhưng không nhận nhãn ở thẻ, còn Q8 chỉ nhận `kind ∈ {actual, projection}`. Hai luật mâu thuẫn với k2check Q35 ("ESTIMATE bắt buộc" cho số ước tính), nên Q7, Q8 TRƯỢT ở cả L4 và L5 (G2 §14.5).
- **Vì sao nêu:** kênh 2 có chủ đích dùng loại số `estimate` (số tự tính, "our read"). Luật LL viết khi chỉ có actual/projection.
- **Đề nghị:** với tập kênh 2 (đặc tả dưới `channel-k2/` hoặc mã tập bắt đầu bằng `k2`, giống cách 1.11.0 nhận diện cho Q14–Q18):
  - Q8 nhận `kind ∈ {actual, projection, estimate}`;
  - Q7 coi nhãn ESTIMATE là đạt dù ở **nhãn góc hay trên thẻ**, miễn đúng một nhãn mỗi số (không trùng nhãn góc và thẻ, như O5).
  - Tập LL giữ nguyên.
- **Selftest đề nghị:** T2 r03_tanker (ESTIMATE ở thẻ) ĐẠT; cùng số bỏ nhãn TRƯỢT; tập LL đội lốt `estimate` vẫn TRƯỢT Q8.

## KN-2 · Q36(b) đếm câu miễn trừ một lần trong 0:00–0:15
- **Hiện tượng:** câu "This video explains… Facts as of…" chỉ hiện **một lần** (shot g00_share, 0:05.6–0:12.0). Q36(b) vẫn đếm 1 lỗi vì shot không dẫn nguồn `loai: luat/chinh_sach/quy_dinh` (G2 §14.5).
- **Vì sao nêu:** chủ dự án đã duyệt O3 = B (1.11.1): "Facts as of" được một lần trong 0:00–0:15 khi khai `mien_tru: true`. Đòi thêm nguồn luật cho câu miễn trừ là áp chồng hai điều kiện.
- **Đề nghị:** shot có `mien_tru: true`, nằm trọn trong 0:00–0:15 và là lần duy nhất thì Q36(b) **không đòi** nguồn `loai` luật. Lần thứ hai trở đi, hoặc ngoài 0:00–0:15, đo như cũ. Đồng thời sửa thông báo "thiếu log cỡ chữ" (45 dòng) vì đó là lỗi công cụ (G2 §14.5).
- **Selftest:** một lần trong 0:05–0:12 ĐẠT; hai lần TRƯỢT; một lần ở 0:20 TRƯỢT; thiếu `mien_tru` TRƯỢT.

## KN-3 · Q33 pHash bỏ lớp chữ cố định
- **Hiện tượng:** từ SS1/TT1, mọi shot bản đồ có **chip nơi dựng** ở góc trên phải và ảnh/footage có **hai tấm chữ gọn**. Các lớp chữ này giống nhau giữa các shot, nên kéo pHash của các cảnh khác nhau lại gần nhau. Vì vậy golden t1 lệch (P-1710 §0.6), và Q33 có thể báo lặp giả.
- **Đề nghị (theo thứ tự ưu tiên):**
  1. băm trên **khung lớp 3D trước khi ghép chữ** (nhà máy có sẵn JPG của từng cảnh và `anchors.json`), nếu K chấp nhận lấy đầu vào từ thư mục dựng;
  2. hoặc băm master sau khi **che hộp chữ** đọc từ log lớp chữ (toạ độ chip, tấm chữ, nhãn) bằng màu trung bình của vùng 3D quanh hộp;
  3. tối thiểu thì che cố định vùng chip (góc trên phải, theo hằng số bố cục `k2.js`) và dải đáy.
- θ_L = 16 tính lại trên băm mới; selftest giữ cặp "bờ Tây xiên" (`m_calif2` ↔ `m_oregon`) là ca biên.

## KN-4 · `versions.py` miễn trừ `served_models` đã duyệt
- **Hiện tượng:** `versions.py check` CHẶN `episode.served_models` vì `claude-haiku-5-5` (CLI tự dùng Haiku cho tác vụ phụ khi `claude -p`), dù chủ dự án đã duyệt (G2 §12.3). BÁO `claude_cli` (tự cập nhật trong phiên).
- **Đề nghị:** `VERSIONS.yaml` có khoá `served_models_duyet: [{model, ngay, nguon}]`. Model nằm trong danh sách thì `check` hạ từ CHẶN xuống BÁO, kèm dẫn nguồn duyệt. `claude_cli` giữ BÁO.
- **Ghi chú vùng:** `scripts/common/versions.py` thuộc vùng Nền tảng, không thuộc `checks/`. P đưa vào hàng đợi này theo lệnh; nếu K không giữ tệp này thì chuyển phiên NT.

## KN-5 · Q37 / `rhythm.py` đo khung tĩnh trên điểm ảnh
- **Hiện tượng:** ở T2, đoạn tĩnh 14,08 s (r06_score2, 9:48) và 6:54.9 (g05_china) chỉ lộ ra khi xem khung thật. Đặc tả khai có chuyển động máy nhưng khoảng dịch quá nhỏ (52 → 46 km), hoặc sticker chỉ hiện ở giây 9,8.
- **Đề nghị cách đo:**
  - trên master (hoặc bản 540p cùng khung): thu nhỏ còn 64×36 luma;
  - lệch tuyệt đối trung bình giữa khung t và t−12 (0,5 s) **sau khi che hộp chữ** (như KN-3);
  - "tĩnh" = chuỗi liên tục có lệch < ε, với ε hiệu chỉnh trên Steel/T1 (cảnh đã duyệt) để không báo nhầm chuyển động máy chậm có chủ đích;
  - TRƯỢT khi chuỗi > 6 s (Kinh thánh §4); báo kèm thời điểm và tên cảnh.
- Giữ phép đo theo đặc tả làm **cảnh báo sớm** trước dựng; phép đo điểm ảnh là phép đo quyết định ở G2.
- **Selftest:** r06_score2 L3 (tĩnh 14,08 s) TRƯỢT; L4 ĐẠT; khung chỉ đổi chữ (nhãn hiện dần) vẫn tính là tĩnh.

## KN-6 · Luật mới VV2 (chủ dự án duyệt 17/10) — đề xuất cách đo
**VV2-a. Nơi có thành phố phải có nhà/phố đúng thời kỳ.**
- **Khai trong đặc tả (nhà máy, ngoài `checks/`):**
  - mỗi shot có `p.where` (chip nơi dựng đã có từ SS1) và `p.nam` (năm/khoảng năm câu lời đang nói);
  - mỗi lớp hình khai `lop` ∈ {dia_hinh, anh_hang_khong, nha_pho_3d, anh_pho, footage_pho, ban_do_phang};
  - tài sản nhà/phố khai `nam_tu`–`nam_den` (năm xây/ảnh chụp).
- **Danh sách nơi là thành phố:** gazetteer cố định trong fixture K (ví dụ Natural Earth populated places, dân số ≥ 50 nghìn ở năm đang nói) hoặc khai `noi: thanh_pho`; đặc tả không tự khai để né.
- **Phép đo:**
  - với mỗi thành phố xuất hiện ≥ 5 s cộng dồn trong tập, phải có ≥ 1 shot lớp `nha_pho_3d`/`anh_pho`/`footage_pho` chiếm ≥ 25 % diện tích khung (đo từ log hộp lớp hoặc mặt nạ);
  - **đúng thời kỳ:** khoảng năm của tài sản giao với `p.nam` ± 10 năm. Nhà hiện đại cho câu 1943 là TRƯỢT.
- **Báo thêm:** tỉ lệ thời lượng thành phố "chỉ địa hình" (T2: Richmond, Philadelphia gần như 100 %).
- **Selftest:** T2 L5 TRƯỢT (Richmond 1943 chỉ DEM + NAIP 2022); ca giả có ảnh phố 1943 ĐẠT; ca ảnh phố 2022 cho câu 1943 TRƯỢT.

**VV2-b. Địa cầu/độ cao lớn ≤ 1 lần/tập, mỗi lần ≤ 3 s.**
- **Nguồn đo:** log máy quay theo khung của `hero.js` (khoảng cách tới tâm/độ cao, đơn vị km hoặc bán kính Trái Đất). Nếu thiếu log thì dùng shot `map/globe` và thời lượng khai, đánh dấu "ước".
- **Định nghĩa "độ cao lớn":** máy cao > 1 500 km **hoặc** thấy độ cong Trái Đất (khung phủ > 30° vĩ độ). K hiệu chỉnh ngưỡng trên Steel/T1/T2 để địa cầu tô Texas của T1 (đã duyệt, 8,00 điểm) và g05_china T2 được phân loại đúng.
- **Phép đo:**
  - đếm **đoạn liên tục** ở độ cao lớn trong master: ≤ 1 đoạn/tập, mỗi đoạn ≤ 3,0 s (72 khung ở 24 fps);
  - Short đếm riêng (đề nghị ≤ 1 đoạn, ≤ 2 s);
  - đoạn chuyển cảnh (zoom từ địa cầu vào) chỉ tính phần trên ngưỡng.
- **Selftest:** T2 g05_china (30 → 18 → 22 bán kính) TRƯỢT nếu > 3 s; T1 địa cầu Texas một lần ≤ 3 s ĐẠT; hai lần TRƯỢT.

**Ưu:** biến bài học T2 (K13–K15) thành phép đo máy trước khi chấm mù. **Nhược:** cần nhà máy ghi thêm log lớp và log máy quay (việc của V/NT, ngoài K). **Tác động:** T3 Gibraltar khung lại quanh các cuộc vây hãm sẽ cần tài sản phố/thành theo thời kỳ (1704, 1779–83). **Rủi ro:** gazetteer bỏ sót thị trấn nhỏ; ngưỡng độ cao đặt sai có thể chặn cảnh định vị hợp lý → K hiệu chỉnh trên ba tập đã có và để CHỈ BÁO tới khi chủ dự án duyệt áp.
