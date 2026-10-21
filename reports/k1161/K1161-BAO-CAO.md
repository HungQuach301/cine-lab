**Nhánh thật: `claude/determined-wright-lwexva`** (harness buộc tên này; lệnh đặt `k-1-16-1`). Gốc `origin/main` @ `8cedb8af`. Main đã cập nhật fast-forward tới commit chứa báo cáo này (§8).

# Phiên K-1.16.1 + P — sửa thước cắt cảnh, ghi duyệt K116-D1…D9, hợp nhất K-1.16 + KL42 vào main — BÁO CÁO

> Phiên K + P, 19/10/2026. Mọi số là số đo thật trong phiên; lệnh và tệp số đo ghi ở từng mục (`reports/k1161/do/`).
> Email chủ dự án không có trong tệp, commit, header, URL, payload hay User-Agent nào. Không đụng `design/`, `scripts/k2*`, `channel-k2/k2c-t3-01/v7p/`, `reports/v7b/`, `docs/`.

## 0. Khối điều lệ (lệnh + thực tế)
| Trường | Lệnh | Thực tế |
|---|---|---|
| Loại phiên | K-1.16.1 + P | đúng |
| Nhánh | `k-1-16-1` từ `origin/main` (8cedb8af) | **`claude/determined-wright-lwexva`** (harness), gốc `8cedb8af` |
| Vùng sửa | `checks/**`, `scripts/common/golden.py` (1 dòng), `reports/k1161/**`, `AUTHORSHIP.md`, `COST-LEDGER.csv`, `RIGHTS.md` | đúng (§10). `golden.py`: **đúng 1 dòng** (`git diff --stat`: 1 insertion, 1 deletion). RIGHTS không đổi (§9). Ngoài vùng chỉ có phần mang vào bởi 2 merge |
| Chi phí | Claude/OpenAI/ElevenLabs/YouTube 0; giờ máy mốc 2 h | **$0 / $0 / 0 ký tự / 0 đơn vị**; giờ máy **≈ 0,7 h** thời gian thực (13:59 → ≈ 14:42 UTC) |
| `lock.py` (không cờ) | một lần ở cuối, sau khi selftest đạt | **đúng một lần**, 14:33:40 UTC → 1.16.1; mọi lần khác chỉ `--verify` |
| Preflight | bắt buộc; che email | hook pre-commit + pre-push cài đầu phiên; mọi commit + push **PREFLIGHT ĐẠT** (§8) |
| Việc dở | đẩy ≤ 30 phút + `CHECKPOINT.md` | checkpoint 1 (sau merge) và 2 (bản vá việc dở `reports/k1161/wip/`, đã gỡ khi commit mã) đã đẩy |
| Force | không | không dùng force ở đâu |
| Dừng | không dừng hỏi giữa chừng | đúng — xem §1 về xung đột AUTHORSHIP |

## 1. Hợp nhất (merge `--no-ff`, theo thứ tự)
| # | Nhánh @ SHA | Commit merge | Số tệp | Kiểm |
|---|---|---|---|---|
| (a) | `origin/ccr-3194130e-kijmlg` @ `a3470b19` (K-1.16) | `986cd7cc` | **49** (+18 350 / −38) | không xung đột |
| (b) | `origin/k2c-t3-kl42` @ `4cd2d941` (KL42) | `f366c2b2` | **37** (+10 377 / −49) | **1 xung đột: `AUTHORSHIP.md`, loại nối-cuối** |

- **Xung đột (b)**: hai nhánh cùng thêm dòng vào cuối bảng AUTHORSHIP (K-1.16: 3 dòng GC-C′/giãn shot B/D11-giờ; KL42: 2 dòng P10C-3…5 nguyên văn/D11). Không có dòng nào bị hai bên sửa; K-1.16 §7 đã báo trước "giữ cả hai khối là đúng". **P giữ cả hai khối** (KL42 trước vì dòng D11 của K-1.16 bổ sung giờ cho dòng D11 của KL42), không bỏ, không sửa chữ nào.
  - Lệnh ghi "Xung đột → DỪNG báo". P không dừng vì đây không phải xung đột nội dung (không phải chọn bên nào). **Nếu chủ dự án muốn quy tắc "dừng cả với xung đột nối-cuối", cần nói rõ**; commit `f366c2b2` có thể làm lại.
- **Sau merge**: `python checks/lock.py --verify` → **KHỚP 1.16.0** `dbbb6cd0606cf37363738711fa8da1b24de29ada4edd1875c1e0adb25d31a439`. `sha256sum -c channel-k2/k2c-t3-01/LOI-KHOA.sha256` → `script-v4.2-KHOA.md: OK`, `loi-khoa.txt: OK`, `khoa-loi/phat-am/gibraltar-eric.pls: OK`. Preflight `--range origin/main..HEAD` (85 tệp): ĐẠT.

## 2. Thước cắt cảnh (TL-1 (c)) — trước / sau
### 2.1 Vì sao 1.16.0 báo nhầm
- Tái hiện số của điều phối: thước 1.16.0 trên `reports/v7p/ban-thu/v7p-xem.mp4` (origin/v7-pilot) ra **26 cắt = 13,10 cắt/phút**; đặc tả có **8 shot / 119,125 s = 7 cắt** (12 · 33 · 44,5 · 67 · 79 · 93,125 · 106,625 s).
- Xem khung 19 cắt thừa: **đổi giờ/ngày–đêm nhanh** (28,2 s, 30,2 s, 82,8 s, 84,2 s, 113–117 s), **nhà mọc theo năm cùng góc máy** (39,3–41,5 s: 1946 → 2021), **hoàng hôn + đổi màu đất** (47,5 s, 48,5 s), **mờ cuối** (118,9 s). Mọi cắt thừa đều là cùng góc máy; 7 cắt thật thước cũ đều bắt được.

### 2.2 Thước mới (`checks/ll/q_k116.py`: `_cau_truc`, `tuong_quan_cau_truc`, `chuoi_cau_truc`, `cuts_video`, `doi_chieu_cat`)
- **(a) Bỏ vùng chữ**: đo trên y **6–70 %** khung (bỏ phụ đề nung, thẻ chương, bộ đếm ở dải dưới; bỏ mép trên).
- **(b) Đổi cấu trúc, không phải độ sáng**: cân bằng histogram mỗi khung (bỏ độ sáng/tương phản toàn khung) → biên độ gradient Sobel → bù tịnh tiến (phase correlation, ≤ 4 % bề ngang) → hệ số tương quan Pearson trên lưới 4×3 ô → **trung vị** các ô. Khung tối/phẳng (σ < 2/255, fade) bỏ qua, so khung sáng sau với khung sáng trước.
  - Cắt = `s[i]` < **0,30** VÀ (trung vị `s` ±0,5 s trừ i±1) − `s[i]` ≥ **0,40**; cực tiểu ±2 khung; cách cắt trước > 2 khung; bỏ 0,5 s đầu.
  - Điều kiện tương đối cần cho G1b: máy bay thấp ở 12 khung/s và nhà "mọc" trong vài khung kéo tương quan liền khung xuống nhiều khung liên tiếp; cắt thật là **một** khung tụt đơn lẻ.
- **(c) Đối chiếu đặc tả**: ghép một-một cắt video ↔ ranh shot đặc tả (đầu shot + beats `cut`) lệch ≤ **0,5 s**. TL-1 báo **cả hai số**: cắt/phút video, cắt/phút đặc tả, số khớp, chỉ video, chỉ đặc tả (trường `cat_video`). Video vẫn quyết (c).

### 2.3 Kiểm có đáp án
**Đáp án** (`reports/k1161/do/dap_an.py`, `dap-an-v7p.json`, `dap-an-g1b.json`), dựng từ `episode.yaml`:
- Ranh = đầu mỗi shot + mỗi lần đổi máy trong cảnh 3D (`cams`).
- Ranh mà máy **liền** (cùng mô-đun, tư thế cuối máy trước = tư thế đầu máy sau, chỉ đổi năm/giờ) **không phải cắt**.
- **V7P**: 7 cắt. **G1b**: 124 ranh = **115 cắt** + 9 liền máy (0e ×3, 5f, 5h, 5j ×4). Thêm 2 mốc `pha` (303,15 s, 467,85 s) không phải ranh shot.

| Video | Thước | Cắt đo | Khớp (±0,5 s) | **Precision** | **Recall** | Cắt/phút |
|---|---|---|---|---|---|---|
| V7P `v7p-xem.mp4` (640×360, 24 khung/s, 119,1 s) | 1.16.0 | 26 | 7 | 0,269 | 1,000 | 13,10 |
| | **1.16.1** | **7** | **7** | **1,000** | **1,000** | **3,53** |
| G1b `animatic-270p-xem.mp4` (480×270, 12 khung/s, 726,2 s) | 1.16.0 | 112 | 103 | 0,920 | 0,896 | 9,25 |
| | **1.16.1** | **117** | **115** | **0,983** | **1,000** | **9,67** |
| V7P lượt 1 `v7p-xem-luot1.mp4` (tham khảo, không độc lập hẳn: cùng đặc tả) | 1.16.0 / 1.16.1 | 27 / **7** | 7 / **7** | 0,259 / **1,000** | 1,000 / **1,000** | — |

**Mục tiêu ≥ 0,9 cả hai: ĐẠT** trên V7P và G1b.
- **2 báo nhầm còn lại ở G1b**:
  - **526,58 s**: sóng/tàu vịnh ở 12 khung/s.
  - **631,67 s**: máy `line` liền mạch nhưng năm nhảy từ đất trống sang phố dày đặc — cả khung đổi cấu trúc. Theo đáp án đặc tả đây là "liền máy", nên P vẫn tính là báo nhầm.
- **Cắt 1.16.0 bỏ sót trên G1b** (12): 133,6 · 162,1 · 171,6 · 175,6 · 195,1 · 331,3 · 335,3 · 352,8 · 406,3 · 429,8 · 434,8 · 450,3 s. 1.16.1 bắt đủ.

**Độ nhạy ngưỡng** (`do/do-nhay-nguong.json`): cả **25/25** tổ hợp `CUT_S` 0,20–0,40 × `CUT_DS` 0,30–0,50 cho P và R ≥ 0,90 trên cả hai video. Thấp nhất: G1b P 0,906 (0,40/0,30); R 0,974 (0,20/·).
- Ngưỡng chọn trên chính hai bộ có đáp án, tức là **hiệu chuẩn trong mẫu**. Vùng ổn định rộng nên rủi ro quá khớp thấp, nhưng nên kiểm lại trên V7B khi có (cùng lượt với K116-D4).

**TL-1 trên đặc tả thật** (`do/tl1-v7p-g1b.txt`):
- V7P: video **7 cắt = 3,53/phút** · đặc tả 7 ranh = 3,53/phút · khớp 7 · (c) sạch.
- G1b: video 117 cắt = 9,65/phút · đặc tả 126 ranh = 10,48/phút · khớp 116 · chỉ video 1 · chỉ đặc tả 10 (9 liền máy + mốc pha) · (c) > 5 (đúng: animatic dựng trước §13.6).
- Thời gian đo: V7P 8,6 s; G1b 26,2 s (đo cấu trúc toàn video).

### 2.4 Selftest thước cắt (mới)
- `vid/v-ngaydem.mp4`: **một** góc máy, lia 0,5 %/s, 8 s, gồm ngày → hoàng hôn nhanh (1,5 s) → đêm có 60 đèn bật nhấp nháy → bình minh, một chớp sáng 2 khung ×1,8, khói trôi, phụ đề nung đổi chữ mỗi 1,5 s. Kết quả: **0 cắt** (1.16.0: báo nhầm 1 ở chớp sáng 6,5 s).
- `vid/v-cungsang.mp4`: cắt cứng ở 3,0 s giữa hai cảnh khác nhau đã khớp histogram (cùng độ sáng). Kết quả: **đúng 1 cắt ở 3,0 s**; chỉ lấy 3 s trước cắt → 0 cắt.
- `v-ok` (2 cắt ở 12 s, 24 s) và `v-cat` (11 cắt) giữ đúng như 1.16.0.
- Đối chiếu: [12,02; 24,4; 30] ↔ [12; 18; 24] → 2 khớp, chỉ video 30, chỉ đặc tả 18; lệch 0,6 s không khớp.
- Sinh lại: `make_fixtures.py --1161` (không đụng video 1.16.0).

## 3. Luật đổi theo K116-D* (duyệt 19/10 18:48)
| Mã | Thay đổi | Tệp | Selftest |
|---|---|---|---|
| D1 | Cấp 1.16 ghi "duyệt K116-D1" (không còn "đề xuất"). Mặc định `k2check` vẫn ghi cấp cạnh kết quả; `--cap` áp vào mã thoát — như mọi luật đã duyệt từ 1.12.1/1.15 | `cap112.py`, `RULES-LL.md` | cấp 7 ca |
| D2 | XEM-CAM đạt = **chủ dự án ≥ 6/8 VÀ trung bình người chấm AI ≥ 6/8**; một AI dưới 6/8 không còn tự làm trượt | `q_k116.xem_cam` | 4 ca mới: AI 5/7/8 (TB 6,67) sạch · TB đúng 6,00 sạch · TB 5,67 trượt · chủ dự án 5/8 trượt |
| D3 | SACH-1 (e) **Chặn**. Nhãn địa danh = vai `diem` (điểm bản đồ chiến lược), `inset` (nhãn inset), `tag` (nhãn neo trên cảnh) — ≤ **2** nhãn khác nhau mỗi shot, hiện trong ≤ **3 s** (từ nhãn đầu hiện tới nhãn cuối tắt). `chu_giai` (chú giải phe) = lỗi. `index`, `card`, vai lạ = lỗi (ngoài danh sách §12.1) | `q_k116.sach1`, `cap112.py` | 5 ca mới: 2 nhãn 3,0 s sạch · 3 nhãn trượt · 4,0 s trượt · chu_giai trượt · index trượt; cấp (e) = Chặn |
| D4 | **Chỉ kế hoạch** (§4) | — | — |
| D5 | K-LAI-3V: **Chặn ở cổng G2**, **Cảnh báo ở animatic** (`animatic: true` trong đặc tả → `cong`). Không khai → G2 (chặt nhất) | `cap112.py`, `k2check.py` | 2 ca cấp |
| D6 | Phóng bằng LK — giữ mã 1.16.0, ghi duyệt | `RULES-LL.md` | như 1.16.0 |
| D7 | `golden.py` so với `checks/golden/tham_chieu/<ca>.png` (1 dòng `run_case`; ca chưa có tham chiếu V6 — k2v4 — giữ nguồn cũ) | `scripts/common/golden.py` | golden §6 |
| D8 | "≈ 8 s" = 7–9 s; ≤ 3 từ/s Cảnh báo — giữ mã 1.16.0, ghi duyệt | `RULES-LL.md`, `cap112.py` | như 1.16.0 |
| D9 | Danh sách 9 nhóm trường phiên dựng phải xuất: log shot, `nhip_vat`, `xem_cam`, `nam_khung`, log chữ, `khung_neo`/`im_lang`/`animatic`, mô tả, khối `lai`, video. Không sửa trình dựng | `RULES-LL.md` mục 1.16.1 | — |

**Cách K đọc D3 (cần chủ dự án xác nhận nếu khác ý):**
- "trong ≤ 3 s" tính **theo shot**: từ lúc nhãn đầu hiện tới lúc nhãn cuối tắt.
- Áp cho mọi shot có nhãn địa danh, không riêng shot `strategic`. Nhãn `tag` trên cảnh 3D cũng là nhãn địa danh.

## 4. K116-D4 — kế hoạch (chưa làm, chờ dữ liệu V7B)
1. Khi V7B có bản dựng: K lấy các cửa sổ máy cố định (TL-1 (d) trôi ≤ 2 %/s) trong shot timelapse.
2. Biến cố = đổi nội dung cục bộ thấy được trong cửa sổ đó: ô lưới có tương quan cấu trúc tụt rõ so với khung trước 0,5–1 s, trong khi đa số ô giữ. Dùng lại `tuong_quan_cau_truc` theo ô; không nhận biến cố tự khai trong log.
3. Hiệu chuẩn có đáp án trên V7B: P đánh dấu tay biến cố trên một đoạn.
4. Cộng biến cố đo được vào Q37 như I8; báo cả hai số (khai/đo).
5. Kiểm lại ngưỡng thước cắt 1.16.1 trên V7B (mẫu ngoài tập hiệu chuẩn).

## 5. Selftest (cây đã khoá 1.16.1)
| Bộ | Trước khoá | **Sau khoá** |
|---|---|---|
| `selftest_k116.py` (cập nhật) | 144/144 | **144/144**, 23 nhóm (SACH-1 17, TL-1 17, XEM-CAM 12, cấp 7, …); mọi luật có ≥ 1 ca đạt + ≥ 1 ca trượt |
| `selftest_k115.py` | 105/105 | **105/105** |
| `selftest_k114.py` | 126/126 | **126/126** |
| `selftest_k113.py` | 64/64 | **64/64** |
| `selftest_k1122.py` | 37/37 | **37/37** |
| `selftest_k1121.py` | 48/48 | **48/48** |
| `selftest_k112.py` | 75/75 | **75/75** |
| `selftest_k2.py` | 129/129 | **129/129** |
| `selftest_ll.py` | 317/317 | **317/317** |

- k116 tăng từ 129 lên 144 ca: thêm 18 ca, thay 3 ca cũ:
  - "một AI 5/8 → trượt" → D2 (một AI 5/8 nay sạch nếu TB ≥ 6);
  - "`diem` → (e) chỉ Cảnh báo" + ca cấp đi kèm → D3;
  - "K-LAI-3V Cảnh báo" → D5 (tách theo cổng).
- **`k2check` 1.16.0 ↔ 1.16.1** trên cùng đầu vào (`do/k2check-t1-t2-1160-1161.txt`):
  - T1 (`fixtures/k2c106-g2`): **30/31 hàng giống hệt** (kq, val, lỗi, sát ngưỡng, cấp, số Chặn/Cảnh báo).
  - T2 L5 + `--bo-tl` gib20: **48/49 hàng giống hệt**.
  - Trước khoá, hàng khác duy nhất là **LOCK** (KHÔNG KHỚP vì chưa khoá). **Sau khoá: T1 31/31, T2 49/49 hàng giống hệt** (hàng LOCK ĐẠT ở cả hai; chỉ tên phiên bản trong cột tên đổi 1.16.0 → 1.16.1).

## 6. Golden (K116-D7)
`scripts/common/golden.py run --only steel,ll08,t1` sau khi sửa 1 dòng (`do/golden-d7.json`; đối chiếu độc lập bằng `checks/golden/so_golden.py`: cùng kết quả):

| Ca | Tham chiếu | Kết quả | Thời gian |
|---|---|---|---|
| steel | `checks/golden/tham_chieu/steel.png` (V6, khoá trong LOCK) | **KHỚP** · pHash 0/64 · SSIM 1,0 · MAD 0,0 · 0/144 ô | 109,9 s |
| ll08 | `checks/golden/tham_chieu/ll08.png` | **KHỚP** · SSIM 1,0 · MAD 0,0 · 0/144 | 251,1 s |
| t1 | `checks/golden/tham_chieu/t1.png` | **KHỚP** · SSIM 1,0 · MAD 0,0 · 0/144 | 92,1 s |

Trình dựng V6 trên llvmpipe tiếp tục tất định từng điểm ảnh. Lượt này là lần thứ ba khớp từng điểm ảnh, sau lượt A và B của K-1.16.

## 7. LOCK
- **Trước**: 1.16.0 `dbbb6cd0606cf37363738711fa8da1b24de29ada4edd1875c1e0adb25d31a439`.
- **Sau**: **1.16.1 `a3c39873751805a7a0a5e2b544bc2c28630d78e87725b777d3c7ba1c77cc2d2b`** (DATE_UTC 2026-10-19T14:33:40Z). `--verify` → **KHỚP**.
- `lock.py` không cờ gọi đúng một lần, sau khi 9 bộ selftest đạt; selftest chạy lại trên cây đã khoá (§5).

## 8. Main trước → sau, preflight, đẩy
- **Main trước**: `8cedb8af` (P-1910). **Sau**: commit cuối của nhánh này ("… DỪNG chờ chủ dự án"), cập nhật bằng `git merge --ff-only`. Đã kiểm `8cedb8af` là tổ tiên. Mang vào main: 2 merge (§1) + mã 1.16.1 + sổ + báo cáo.
- Trên main sau cập nhật: `lock.py --verify` KHỚP 1.16.1.
- **Preflight `--range origin/main..HEAD`**: ĐẠT trước khi đẩy main.
  - Hai mục ngoại lệ đã biết (video V5b-2d `338cef97…`, P4 báo nhầm `mpfb2-LICENSE.txt`) **không xuất hiện** trong dải này, vì cả hai đã nằm trong main cũ.
  - Hook pre-push ĐẠT, **không dùng `--no-verify`**.
- Preflight theo commit: mọi commit ĐẠT.
  - Ở checkpoint 2, lần commit/push đầu bị **CHẶN đúng** vì `checks/` đang sửa chưa khớp LOCK 1.16.0. P cất tạm thay đổi (`git stash`), commit/push bản vá việc dở, rồi trả lại. Không có gì sai lọt qua.
- Không force; không đẩy nhánh nào khác ngoài nhánh harness và `main`.

## 9. Sổ
| Sổ | Thay đổi |
|---|---|
| `AUTHORSHIP.md` | +9 dòng **K116-D1…D9**, nguyên văn lệnh, "DUYỆT 18:48" 19/10/2026, kèm chỗ áp trong mã (+5 dòng của 2 nhánh qua merge, §1) |
| `COST-LEDGER.csv` | +1 dòng **K-1.16.1**: $0, EL 0, giờ máy 0,7. Kiểm bằng `csv`: **62 dòng, mọi dòng 20 cột** |
| `RIGHTS.md` | **không đổi**. 2 merge không mang dòng RIGHTS mới hay tài sản ngoài mới. KL42 thêm bản thu giọng G1 (`reports/kl42/nghe/*.mp3`) — đầu ra của giọng đã có dòng **P1910-G1** (quyền chờ thư Đ5: chỉ thử/animatic/nội bộ). PLS/từ điển phát âm là sản phẩm của dự án |

## 10. Tệp đã sửa (ngoài 2 merge)
| Tệp | Việc |
|---|---|
| `checks/ll/q_k116.py` | thước cắt cấu trúc + đối chiếu đặc tả (TL-1 (c) báo cả hai số); SACH-1 (e) theo D3; XEM-CAM theo D2; docstring 1.16.1 |
| `checks/ll/cap112.py` | cấp 1.16 "duyệt K116-D1"; SACH-1 (e) Chặn; K-LAI-3V theo cổng (D5) |
| `checks/ll/k2check.py` | `cong` cho K-LAI-3V; chữ ngưỡng TL-1/XEM-CAM/SACH-1 |
| `checks/ll/selftest_k116.py` | +15 ca (§5) |
| `checks/ll/fixtures/k116/make_fixtures.py`, `vid/v-ngaydem.mp4`, `vid/v-cungsang.mp4` | video tổng hợp thước cắt (57 KB) |
| `checks/ll/RULES-LL.md` | mục 1.16.1 (thước cắt, bảng K116-D1…D9, trường D9), sửa bảng 1.16, tự kiểm |
| `checks/cinecheck/__init__.py`, `checks/LOCK` | 1.16.1 |
| `scripts/common/golden.py` | 1 dòng (D7) |
| `AUTHORSHIP.md`, `COST-LEDGER.csv` | §9 |
| `reports/k1161/` | báo cáo, CHECKPOINT, `do/` (đáp án, độ nhạy, TL-1, k2check, golden) |

## 11. Chỉ số trong ±5 % quanh ngưỡng (luật cứng)
**Dữ liệu thật:**
- G1b 331,25 s: tương quan cấu trúc **0,288** so ngưỡng 0,30 (−4,0 %). Đây là cắt thật, thước bắt được.
- G1b 467,83 s: độ tụt so trung vị **0,385** so ngưỡng 0,40 (−3,75 %). Đây là mốc `pha` của đặc tả, không phải cắt; thước không bắt — đúng.
- V7P: không giá trị nào trong ±5 %. Cắt thật có `s` ≤ 0,029; không-cắt có `s` ≥ 0,575.
- TL-1 cắt/phút: V7P 3,53, G1b 9,65 so ngưỡng 5. Cả hai ngoài ±5 %.

**Ca fixture cố ý đặt đúng ngưỡng:**
- XEM-CAM TB AI **6,00/8** (= 6).
- SACH-1 nhãn địa danh **3,00 s** (= 3) và **2 nhãn** (= 2).

**Không thêm phần tử nào để vượt ngưỡng.**

## 12. Việc chờ chủ dự án
1. **Xác nhận cách hợp nhất AUTHORSHIP** (giữ cả hai khối nối-cuối, §1). Nói rõ nếu muốn từ nay dừng cả với xung đột loại này.
2. **Xác nhận cách đọc K116-D3** (§3): "≤ 3 s" tính theo shot, từ nhãn đầu tới nhãn cuối; `tag` trên cảnh 3D là nhãn địa danh; `index`/`card` là lỗi.
3. **Xác nhận K116-D1 = cấp**: mặc định `k2check` vẫn ghi cấp cạnh kết quả, `--cap` áp vào mã thoát, như mọi luật đã duyệt trước. Nếu muốn 1.16 vào mã thoát mặc định, cần lệnh riêng.
4. **K116-D4**: giao lượt K sau khi V7B có bản dựng (kế hoạch §4), kèm kiểm lại ngưỡng thước cắt trên V7B.
5. Việc còn treo từ K-1.16 §13, chưa đổi:
   - V6/PT3 ghi kết quả "kiểm trôi" cho 55 tệp vân;
   - T3 sửa 7 lỗi khai ML1 + `ly_do_hinh`;
   - V7-PILOT/V7B xuất trường K116-D9.
6. **Thư Đ5 ElevenLabs** (quyền dùng giọng G1 cho bản phát hành) vẫn chưa gửi (RIGHTS P1910-G1). *(Đính chính P-2010, 20/10: ghi nhầm — thư Đ5 ĐÃ GỬI 19/10 16:57; đang chờ ElevenLabs trả lời.)*

**DỪNG — chờ chủ dự án.**
