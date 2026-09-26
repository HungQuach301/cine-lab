# CINE LAB — KHUNG SẢN XUẤT VÀ CỔNG KIỂM CHỨNG CHẤT LƯỢNG ĐIỆN ẢNH (v0.1, 26/09/2026)

Trạng thái: **bản đề xuất, chờ chủ dự án duyệt**. Ngưỡng ghi "nội bộ" là đề xuất ban đầu, sẽ hiệu chuẩn sau bài thử 2–3 phút.

## 0. Mục tiêu và định nghĩa vận hành

- Mục tiêu: phim đạt chất lượng ở mức điện ảnh cao nhất. **Không nhằm tranh giải.** Quy chế Oscar (`claude/CINE-LAB-CHUAN-OSCAR.md`) chỉ dùng để tham khảo chuẩn kỹ thuật, không phải ràng buộc.
- "Chất lượng điện ảnh cao nhất" được định nghĩa để đo được như sau:

> **Người xem mù (không biết quy trình), xem một lần ở tốc độ thường, đánh giá phim của Cine Lab ngang với phim ngắn hoạt hình chuyên nghiệp cùng thể loại được chọn làm tham chiếu.**

- Do đó cần **3–5 phim tham chiếu**: phim ngắn hoạt hình phong cách hoá, 8–15 phút, do studio hoặc tác giả chuyên nghiệp làm, xem công khai được. Chủ dự án chọn. Phim tham chiếu chỉ dùng để xem và chấm so sánh, không sao chép.

## 1. Mô hình chất lượng 3 lớp

| Lớp | Đo cái gì | Ai / công cụ | Kiểu kết quả | Vai trò |
|---|---|---|---|---|
| **L1 Kỹ thuật** | File, âm lượng, khung hình, màu, chữ, lời có đủ | Máy (phiên K viết, khoá SHA) | Đạt / trượt | Điều kiện cần. Lỗi L1 là lỗi **Chặn** |
| **L2 Nghề** | Từng khía cạnh nghề: truyện, nhân vật, hình, hoạt hình, dựng, âm | Máy (phần đo được) + người chấm theo rubric | Điểm 1–5 kèm bằng chứng | Chất lượng tay nghề |
| **L3 Khán giả** | Hiểu truyện, giữ chú ý, cảm xúc đúng chỗ, so với phim tham chiếu | Người xem mù | Tỷ lệ, bản đồ chú ý | **Thước đo cuối cùng** |

**Thứ tự ưu tiên khi các tiêu chuẩn xung đột** (theo "Rule of Six" của Walter Murch cho dựng phim, mở rộng cho toàn phim): cảm xúc > truyện > nhịp > đường mắt > bố cục mặt phẳng > không gian 3D. Một tiêu chuẩn kỹ thuật ở lớp dưới không được bắt hy sinh cảm xúc hay truyện, trừ lỗi L1 Chặn.

**Nguyên tắc chống Goodhart** (rút từ BRIEF-D):
1. Đo từ file đã render, không từ bản khai.
2. Không đặt chỉ tiêu số lượng cho kỹ thuật nghệ thuật. Số lượng chỉ là cảnh báo; mỗi kỹ thuật phải có lý do.
3. Mỗi luật máy có test tự chứng minh (mẫu phải trượt, mẫu phải sạch).
4. Luật được hiệu chuẩn với L3: luật không phân biệt được bản tốt và bản kém thì hạ cấp.
5. Phân cấp **Chặn / Chính / Tham khảo**.

## 2. Vai trò

| Vai trò | Người/phiên | Quyền |
|---|---|---|
| Tác giả – đạo diễn | Chủ dự án | Quyết định sáng tạo then chốt; duyệt mọi cổng; phán quyết khiếu nại. Ghi đóng góp biểu đạt vào AUTHORSHIP.md |
| Đội sản xuất | Opus – phiên D | Biên kịch hỗ trợ, thiết kế, dựng, hoạt hình, render, âm thanh; không sửa luật |
| Kiểm định | Opus – phiên K (phiên riêng) | Viết, khoá và chạy luật L1/L2 máy; chấm từ file |
| Người xem mù | ≥ 3 người (đích 5) nói tiếng Anh | Chấm L3; không biết quy trình |

## 3. Khung sản xuất: 11 cổng

Nguyên tắc chung:
- Mỗi cổng có đầu ra bắt buộc, tiêu chí qua và người duyệt.
- **Trượt cổng thì quay lại cổng trước**, không đi tiếp.
- Sửa ở cổng càng sớm càng rẻ. Vì vậy **truyện phải chốt ở cổng Animatic**, trước khi tốn công dựng hình (cách làm chuẩn của studio hoạt hình).

### Cổng 0 — Năng lực và hạ tầng (bài thử 2–3 phút là phiên bản mở rộng của cổng này)
- Đầu ra: báo cáo đo tốc độ render theo phong cách đã chọn; thử giọng ElevenLabs cho 1 cảnh cảm xúc khó; thử dựng cùng nhân vật ở 2 phiên khác nhau; công cụ kiểm L1 chạy được.
- Qua khi:
  - render ≤ ngưỡng giây/giây phim (nội bộ đề xuất ≤ 60; phim 15 phút tương đương ≤ 15 giờ render);
  - cảnh cảm xúc khó được ≥ 3/5 người nghe mù đánh giá "tin được";
  - nhân vật ở 2 phiên sai lệch tỷ lệ ≤ ngưỡng C3.
- Dừng khi: không đạt ngưỡng render → đổi phong cách hình trước khi viết truyện.

### Cổng 1 — Ý tưởng
- Đầu ra: logline 1 câu; chủ đề 1 câu; câu hỏi phim đặt ra; thể loại và tông; 3–5 phim tham chiếu; trang ý đồ đạo diễn.
- Qua khi: đọc logline cho 3 người, ≥ 2 người kể lại đúng và muốn xem (L3 sớm). Chủ dự án là tác giả logline và chủ đề.

### Cổng 2 — Kịch bản
- Đầu ra: beat sheet theo sequence (4–6 sequence cho 10–15 phút); kịch bản; table read bằng giọng tạm; danh sách chỗ sửa.
- Qua khi: đạt tiêu chuẩn nhóm A, B (mục 4); đọc mù đạt ngưỡng.

### Cổng 3 — Thiết kế
- Đầu ra: model sheet nhân vật; world bible (luật thế giới, bối cảnh, đạo cụ); color script theo sequence; **5–8 style frame** chất lượng cuối cùng làm "hợp đồng hình ảnh".
- Qua khi: đạt nhóm C, D; chủ dự án ký style frame. Mọi cảnh về sau được đo sai lệch màu so với style frame.

### Cổng 4 — Animatic (story reel) — CỔNG QUAN TRỌNG NHẤT
- Đầu ra: toàn phim ở dạng storyboard có định thời, kèm giọng tạm, nhạc và hiệu ứng tạm, đúng độ dài.
- Qua khi: **chiếu thử L3 trên animatic**; người xem mù tóm tắt đúng truyện; bản đồ chú ý không có "hố" dài hơn ngưỡng; cảm xúc đúng ở các beat chính.
- Dừng khi: trượt → sửa kịch bản hoặc animatic, **không được chuyển sang dựng**.

### Cổng 5 — Layout và dàn cảnh
- Đầu ra: máy quay và bố cục cuối cho từng shot; blocking nhân vật; continuity sheet cho từng cảnh.
- Qua khi: đạt nhóm E, F, O.

### Cổng 6 — Hoạt hình
- Đầu ra: rough (tư thế then chốt, timing) → duyệt → polish.
- Qua khi: đạt nhóm H.

### Cổng 7 — Ánh sáng, render, composite
- Qua khi: đạt nhóm G; sai lệch so với style frame trong ngưỡng; không lỗi L1 về hình.

### Cổng 8 — Giọng, nhạc, âm thanh, mix
- Qua khi: đạt nhóm J, K, L, M.

### Cổng 9 — Hoàn thiện và master
- Đầu ra: master YouTube, master lưu trữ chất lượng cao, phụ đề, credit, sổ quyền, AUTHORSHIP.md.
- Qua khi: đạt toàn bộ L1 (nhóm N, P, Q).

### Cổng 10 — Chiếu thử cuối và phát hành
- Qua khi: đạt ngưỡng L3 cuối (mục 5), gồm so cặp mù với phim tham chiếu.

## 4. Bộ tiêu chuẩn cụ thể theo khía cạnh

Ký hiệu: **M** = máy, **N** = người chấm theo rubric, **K** = khán giả mù. Cấp: **C** = Chặn, **Ch** = Chính, **T** = Tham khảo. Ngưỡng không ghi nguồn là ngưỡng nội bộ đề xuất.

### A. Truyện và chủ đề (Cổng 1, 2, 4)
| Mã | Tiêu chuẩn | Kiểm chứng | Loại | Cấp |
|---|---|---|---|---|
| A1 | Chủ đề nói được trong 1 câu; mọi sequence phục vụ chủ đề | Bảng ánh xạ sequence → chủ đề | N | Ch |
| A2 | **Mỗi cảnh xoay chuyển một giá trị** (ví dụ an toàn → nguy hiểm); cảnh không xoay giá trị bị cắt | Beat sheet ghi giá trị đầu/cuối từng cảnh; người chấm xác nhận | M (đủ trường) + N | Ch |
| A3 | Có sự kiện khởi đầu, bước ngoặt giữa phim, cao trào, kết; nhân vật chính lựa chọn ở cao trào | Beat sheet + N | N | Ch |
| A4 | Người xem hiểu truyện | ≥ 4/5 người xem mù tóm tắt đúng mạch chính sau 1 lần xem | K | C |
| A5 | Kết có dư âm: người xem nêu được ý nghĩa, không chỉ sự kiện | Câu hỏi mở sau chiếu | K | Ch |

### B. Kịch bản và thoại (Cổng 2)
| Mã | Tiêu chuẩn | Kiểm chứng | Loại | Cấp |
|---|---|---|---|---|
| B1 | Không thoại giải thích điều hình đã cho thấy | Người chấm đánh dấu từng câu | N | Ch |
| B2 | Mỗi nhân vật có cách nói riêng | Che tên người nói, người đọc đoán đúng ≥ 80% câu | K | Ch |
| B3 | Có ẩn ý: điều nhân vật muốn ≠ điều nhân vật nói ở các cảnh then chốt | Người chấm | N | T |
| B4 | Table read trước khi dựng; mọi chỗ sửa được ghi | File audio + danh sách sửa | M | C |

### C. Nhân vật (Cổng 3, 6)
| Mã | Tiêu chuẩn | Kiểm chứng | Loại | Cấp |
|---|---|---|---|---|
| C1 | Mỗi nhân vật chính có mong muốn, nhu cầu thật, điểm yếu, và thay đổi qua phim | Hồ sơ nhân vật + N | N | Ch |
| C2 | **Đọc được qua silhouette**: tô đen đặc, vẫn nhận ra ai và đang làm gì | ≥ 90% tư thế then chốt được người xem nhận ra; máy đo khác biệt hình dạng giữa các nhân vật | M + K | Ch |
| C3 | Đúng model qua mọi cảnh | Tỷ lệ các bộ phận so với model sheet lệch ≤ 3% (nội bộ) | M | C |
| C4 | Phân biệt được các nhân vật ở thang xám và khi mô phỏng mù màu | Mô phỏng deuteranopia, protanopia, grayscale | M | Ch |

### D. Thế giới và thiết kế (Cổng 3)
| Mã | Tiêu chuẩn | Kiểm chứng | Loại | Cấp |
|---|---|---|---|---|
| D1 | World bible khoá SHA; mọi bối cảnh và đạo cụ có trong bible | Đối chiếu danh sách tài sản | M | Ch |
| D2 | Ngôn ngữ hình thống nhất: hình khối, bảng màu, chất liệu | Người chấm so với style frame | N | Ch |
| D3 | Thiết kế phục vụ truyện: màu và hình khối đổi theo color script | So từng sequence với color script | M + N | Ch |

### E. Đạo diễn và dàn cảnh (Cổng 5)
| Mã | Tiêu chuẩn | Kiểm chứng | Loại | Cấp |
|---|---|---|---|---|
| E1 | Mỗi shot có mục đích kể chuyện ghi trong shot list | Đủ trường | M | Ch |
| E2 | Blocking rõ ràng: người xem biết ai ở đâu, nhìn đâu | Người chấm + L3 (không bối rối không gian) | N + K | Ch |
| E3 | Quy tắc 180° và hướng màn hình giữ nhất quán, trừ khi phá có chủ ý (ghi lý do) | Máy theo vị trí nhân vật giữa các cú cắt | M | Ch |

### F. Máy quay và bố cục (Cổng 5)
| Mã | Tiêu chuẩn | Kiểm chứng | Loại | Cấp |
|---|---|---|---|---|
| F1 | **Thumbnail test**: thu khung hình còn 10%, chủ thể chính vẫn nhận ra | Máy phát hiện vùng nổi bật + người xem | M + K | Ch |
| F2 | Cấu trúc sáng tối (value) đọc được ở thang xám | Grayscale + phân tích histogram vùng | M | Ch |
| F3 | Chuyển động máy có quán tính, không tuyến tính; mỗi chuyển động có lý do | Đường cong camera + shot list | M | Ch |
| F4 | Cỡ cảnh và tiêu cự giả lập đa dạng theo ý đồ | Phân bố cỡ cảnh (cảnh báo, không quota) | M | T |

### G. Ánh sáng và màu (Cổng 3, 7)
| Mã | Tiêu chuẩn | Kiểm chứng | Loại | Cấp |
|---|---|---|---|---|
| G1 | Mỗi cảnh có sơ đồ ánh sáng có nguồn gốc (key/fill/rim) | Có file; người chấm | M + N | Ch |
| G2 | Màu bám style frame và color script | ΔE trung bình so với style frame ≤ ngưỡng (hiệu chuẩn ở cổng 3) | M | Ch |
| G3 | Không banding trên gradient; grain cố định | Đo trên vùng tối | M | C |
| G4 | Chữ tương phản ≥ 4,5:1 (mức WCAG AA) | Đo điểm ảnh | M | C |

### H. Hoạt hình (Cổng 6) — dựa 12 nguyên lý hoạt hình (Thomas & Johnston)
| Mã | Tiêu chuẩn | Kiểm chứng | Loại | Cấp |
|---|---|---|---|---|
| H1 | Không có chuyển động tuyến tính ở bộ phận nhân vật, trừ máy móc có chủ ý | Đường cong transform của rig | M | C |
| H2 | Khớp chuyển động theo cung, không theo đường thẳng | Độ lệch quỹ đạo so với đường thẳng | M | Ch |
| H3 | Không có "giữ chết": mọi lần đứng yên > 12 khung có chuyển động phụ (thở, chớp mắt) | Đo chuyển động điểm ảnh vùng nhân vật | M | Ch |
| H4 | Lấy đà, theo đà, chồng lớp, dẻo co giãn giữ thể tích | Người chấm từng cảnh | N | Ch |
| H5 | Diễn xuất: cảm xúc đọc được qua dáng và nhịp khi tắt tiếng | Người xem mù đoán cảm xúc khi tắt tiếng ≥ 70% đúng | K | Ch |
| H6 | Khẩu hình khớp âm vị ±1 khung | Forced alignment so với hình miệng | M | C |

### I. Dựng và nhịp (Cổng 4, 9)
| Mã | Tiêu chuẩn | Kiểm chứng | Loại | Cấp |
|---|---|---|---|---|
| I1 | Đường mắt liền mạch qua cú cắt: điểm nhìn chính không nhảy xa, trừ khi có chủ ý | Vùng nổi bật trước/sau cắt | M | Ch |
| I2 | Cắt đúng điểm hành động hoặc đúng phách | Phát hiện cắt từ file, so với sự kiện | M | T |
| I3 | Bản đồ chú ý không có "hố" | Người xem bấm khi mất tập trung; không đoạn nào > 20% người xem bấm | K | C |
| I4 | Nhịp căng–chùng khớp thiết kế | Đo từ file (tốc độ cắt, mật độ âm) so với bản thiết kế | M | Ch |

### J. Giọng và diễn xuất giọng (Cổng 0, 8)
| Mã | Tiêu chuẩn | Kiểm chứng | Loại | Cấp |
|---|---|---|---|---|
| J1 | Mọi từ trong kịch bản nghe rõ **trên bản mix cuối** | ASR trên mix cuối so với kịch bản: 100% từ bắt buộc, WER ≤ 5% (nội bộ) | M | C |
| J2 | Giọng tin được, đúng cảm xúc | Người nghe mù: ≥ 4/5 "tin được" ở mỗi cảnh cảm xúc | K | Ch |
| J3 | Giãn thời gian ≤ 10%; không méo | Đo tỉ lệ giãn + phổ | M | C |

### K. Nhạc (Cổng 8)
| Mã | Tiêu chuẩn | Kiểm chứng | Loại | Cấp |
|---|---|---|---|---|
| K1 | Leitmotif gắn nhân vật hoặc ý, biến tấu theo truyện | Cue sheet + người nghe | N | Ch |
| K2 | Nhạc phục vụ cảnh, không kể thay | Người chấm | N | Ch |
| K3 | Có giấy phép dùng cho phim và bán phim | Sổ quyền | M | C |

### L. Thiết kế âm thanh (Cổng 8)
| Mã | Tiêu chuẩn | Kiểm chứng | Loại | Cấp |
|---|---|---|---|---|
| L1 | Mỗi cảnh có ambience/room tone; không có "im số" ngoài ý muốn | Đo sàn nhiễu theo cảnh | M | C |
| L2 | Âm đặt đúng vị trí và chiều sâu (pan theo x, reverb theo chiều sâu) | Tương quan pan–vị trí | M | Ch |
| L3 | Khoảng lặng có chủ ý tại beat cảm xúc | Cue sheet + người chấm | N | T |

### M. Mix và master (Cổng 8, 9)
| Mã | Tiêu chuẩn | Kiểm chứng | Loại | Cấp |
|---|---|---|---|---|
| M1 | Master YouTube: −14 LUFS ±1, true peak ≤ −1 dBTP (thực hành phổ biến cho YouTube) | ITU-R BS.1770 | M | C |
| M2 | Master lưu trữ/bán: dải động rộng hơn, tham chiếu −27 LKFS đo theo lời, TP −2 dBTP (spec Netflix, nguồn thứ cấp) | BS.1770 dialog-gated | M | Ch |
| M3 | Lời luôn nghe rõ trên nhạc; tương thích mono | Phổ, tương quan pha | M | C |

### N. Kỹ thuật file (Cổng 9)
| Mã | Tiêu chuẩn | Kiểm chứng | Loại | Cấp |
|---|---|---|---|---|
| N1 | 24 fps CFR; không rơi hay lặp khung theo PTS | ffprobe | M | C |
| N2 | BT.709 đủ 3 trường; dải limited | ffprobe | M | C |
| N3 | Master lưu trữ chất lượng cao (intermediate); bản YouTube bitrate cao | Kiểm codec, bitrate | M | C |
| N4 | Tuỳ chọn: bản 4K cho YouTube (nén tốt hơn) — chỉ khi Cổng 0 chứng minh render chịu được | Quyết định ở Cổng 0 | — | T |

### O. Liên tục và nhất quán (Cổng 5–7)
| Mã | Tiêu chuẩn | Kiểm chứng | Loại | Cấp |
|---|---|---|---|---|
| O1 | Continuity sheet mỗi cảnh: đạo cụ, trang phục, thời điểm, vị trí, thương tích | Đủ trường | M | Ch |
| O2 | Cảnh kề nhau khớp continuity sheet | Máy so đặc trưng + người rà | M + N | C |
| O3 | Mọi tài sản lấy từ thư viện có SHA; không tạo lại nhân vật hay bối cảnh ngoài thư viện | Đối chiếu SHA | M | C |

### P. Chữ, tiêu đề, phụ đề (Cổng 9)
| Mã | Tiêu chuẩn | Kiểm chứng | Loại | Cấp |
|---|---|---|---|---|
| P1 | Không chữ đè chữ, tính theo điểm ảnh nét chữ | Luật bài C nâng cấp | M | C |
| P2 | Phụ đề khớp 100% lời thoại; ≤ 42 ký tự/dòng, ≤ 2 dòng; có bản SDH mô tả âm thanh | Đối chiếu kịch bản | M | C |
| P3 | Title sequence và credit được thiết kế như một phần của phim; credit đủ theo sổ quyền | Người chấm + đối chiếu | M + N | Ch |

### Q. Quyền và tác giả (xuyên suốt)
| Mã | Tiêu chuẩn | Kiểm chứng | Loại | Cấp |
|---|---|---|---|---|
| Q1 | Sổ quyền: mọi tài sản có nguồn, giấy phép, phạm vi dùng | Đủ trường | M | C |
| Q2 | AUTHORSHIP.md ghi đóng góp biểu đạt của chủ dự án ở mọi cổng | Đủ mục mỗi cổng | M | C |
| Q3 | Không giống IP có sẵn (nhân vật, thiết kế, nhạc) | Người rà | N | C |

## 5. Ngưỡng L3 cuối (Cổng 10) — nội bộ, hiệu chuẩn sau bài thử

| Chỉ số | Ngưỡng |
|---|---|
| Tóm tắt đúng mạch truyện | ≥ 4/5 người xem |
| Hố chú ý | Không đoạn nào > 20% người xem bấm "mất tập trung" |
| Cảm xúc đúng ở beat chính | ≥ 70% người xem |
| Muốn xem phim khác của cùng tác giả | ≥ 3/5 |
| **So cặp mù với phim tham chiếu** (xem 2 phim, chọn phim thích hơn; không biết phim nào do AI làm) | Phim Cine Lab được chọn ≥ 40% (tức gần ngang phim chuyên nghiệp) |

## 6. Rubric người chấm (L2) — mẫu thang 1–5
- **1:** lỗi thấy ngay, người xem bị kéo ra khỏi phim.
- **3:** đúng nghề nhưng không đáng nhớ; người xem không để ý tới.
- **5:** ngang phim tham chiếu; phục vụ cảm xúc và truyện một cách chủ động.

Phiên K sẽ viết mô tả mức 1/3/5 cho từng mã N ở mục 4, kèm ví dụ trích từ phim tham chiếu (mốc thời gian).

## 7. Áp vào bài thử 2–3 phút
- Chạy đủ Cổng 0 → 10 ở quy mô nhỏ để kiểm chứng **chính khung này**: cổng nào thừa, luật nào không phân biệt được tốt/xấu, tốn bao nhiêu thời gian và chi phí mỗi cổng.
- Sau bài thử: hiệu chuẩn ngưỡng, phát hành khung v1.0, rồi mới làm phim 10–15 phút.

## Nguồn tham chiếu
- Walter Murch, *In the Blink of an Eye* — "Rule of Six" (tóm tắt: https://nofilmschool.com/2016/11/6-rules-good-cutting-according-oscar-winning-editor-walter-murch)
- Frank Thomas & Ollie Johnston, *The Illusion of Life* — 12 nguyên lý hoạt hình
- Robert McKee, *Story* — mỗi cảnh xoay chuyển một giá trị
- ITU-R BS.1770 (đo âm lượng); WCAG 2.x (tương phản 4,5:1)
- Netflix loudness (thứ cấp): https://www.production-expert.com/production-expert-1/understanding-loudness-part-4-creating-loudness-compliant-mixes-for-broadcast-and-netflix
- Các file Cine Lab: CINE-LAB-HANDOFF.md, claude/CINE-LAB-BAI-HOC-BRIEF-D.md, claude/CINE-LAB-KHOANG-TRONG.md, claude/CINE-LAB-CHUAN-OSCAR.md
