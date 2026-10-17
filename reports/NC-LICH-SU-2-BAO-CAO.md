# NC-LS2 — Đề tài ĐỎ/VÀNG đậm "có kiểm soát" cho series lịch sử: BÁO CÁO NGHIÊN CỨU

> Phiên nghiên cứu NC-LS2, 17/10/2026, theo lệnh chủ dự án 17/10 (khung XX1–XX2 đã duyệt). Nhánh `nc-lich-su-2` tạo từ `origin/nc-lich-su` @ `a30af04`. **Chỉ tài liệu. Không merge. DỪNG chờ chủ dự án.**
> Lượt xem, số bình luận là **số công khai YouTube Data API, đọc 17/10/2026 (UTC)**. Mọi trung vị, điểm chấm, số đếm bình luận, tỷ lệ là **tự tính, không phải chỉ số YouTube**. Ước tính ghi **(ước)**. Chỗ chưa kiểm bằng nguồn gốc ghi **(chưa kiểm)**.
> Không tải video, khung hình, thumbnail. Repo không chứa tiêu đề, mô tả, lời hay bình luận nguyên văn của kênh khác: chỉ có số đo và nhận xét viết lại bằng lời của phiên. Văn bản gốc nằm ngoài git (`~/.cache/nc-ls2/`).
> **Không phải tư vấn pháp lý.** Mọi mục "pháp lý" ở §3 là tóm tắt từ nguồn công khai, **chưa tư vấn luật**.

## Khối điều lệ (lệnh + thực tế)
| Trường | Lệnh | Thực tế |
|---|---|---|
| Loại phiên | Nghiên cứu (chỉ tài liệu) | đúng |
| Nhánh | `nc-lich-su-2` từ `origin/nc-lich-su` | đúng (@ `a30af04`); đẩy `nc-lich-su-2`, không merge |
| Tệp được sửa | CHỈ `reports/NC-LICH-SU-2-BAO-CAO.md` + `reports/nc-lich-su-2/*.csv\|json` ≤ 1 MB | đúng: báo cáo + 4 tệp JSON (`de-tai-cau.json`, `binh-luan-dem.json`, `cham-diem.json`, `cost.json`), tổng ≈ 60 KB. Không sửa main, nhánh tập, `checks/`, `scripts/`, `design/`, `docs/`. Không ghi RIGHTS/AUTHORSHIP/COST-LEDGER (ngoài vùng; dòng đề xuất ở §9) |
| Trần | Claude API ≤ $1 (ghim) · YouTube ≤ 2 500 đv · ElevenLabs 0 · giờ máy ≤ 1 h | **$0** (không gọi) · **1 434 đv** · **0 ký tự** · **≈ 0,1 h** |
| Preflight | bắt buộc; che email | `verify.sh`: 9 PASS, 4 FAIL không liên quan việc tài liệu (three.js lock, tifffile/pyshp, k2v node_modules, Freesound 403 tuỳ chọn). Hook pre-commit/pre-push cài đầu phiên. Kết quả `tools/preflight.sh` ở §10. 0 email trong tệp ghi |
| Điều kiện dừng | xong → đẩy → dừng; không dừng hỏi giữa chừng | (1) xong việc. Câu hỏi không chặn đã tự quyết, ghi ở §11 |

---

## 0. Tóm tắt cho chủ dự án (đọc 2 phút)

1. **Có 13 ứng viên.** Lệnh nêu 9: Jerusalem 1099 và 1187 tính là 2. Phiên thêm 4 ứng viên ĐỎ/VÀNG đậm có cầu lớn: **Berlin 1945, Warsaw 1944, Hiroshima 1945, Nanjing 1937** (lý do ở §1.2).
2. **Bốn đề tài bị loại theo (c):** Jerusalem 1099 và Jerusalem 1187 (không đo), Stalingrad và Derry 1689 (đo để tham khảo). Phiên đặt phép thử (c) đo được: **(c1)** nơi đó hoặc các phe đang có chiến sự hay bạo lực vũ trang có tổ chức, **VÀ (c2)** sự kiện được dùng trực tiếp làm biểu tượng trong xung đột đó (§1.3).
3. **Đo cầu theo đúng §3.1 NC-LS** cho 11 đề tài (1 `search.list` + `videos.list` mỗi đề tài, dài ≥ 8 phút, loại tay 24 video lạc đề). **Cầu rất lớn ở phần lớn đề tài.** Hiroshima có video dài lớn nhất 13,4 triệu và 14 video dài ≥ 1 triệu. Berlin có 8,17 triệu và Short 12,6 triệu. Stalingrad có 6,81 triệu. **Khoảng trống thì hẹp:** chỉ Dresden, Berlin, Warsaw, Nanjing và Tenochtitlan đạt ≥ 3.
4. **Theo XX1(a): chỉ 2/10 đề tài được chấm đạt cả ba điều kiện** (/25 ≥ 20, cầu ≥ 4, khoảng trống ≥ 3):
   - **Dresden 1945: 20/25**, đúng ngưỡng.
   - **Berlin 1945: 21/25**, khoảng trống đúng ngưỡng 3.
   - Trượt sát ngưỡng: Warsaw 21 (cầu 3), Hiroshima 20 (khoảng trống 2), Vienna 20 (khoảng trống 1). Constantinople và Tenochtitlan đều 19.
5. **Ràng buộc nhịp đã kiểm trên nhánh tiền kỳ:** T3 Gibraltar VÀNG, T4 Las Vegas XANH, T5 Zürich XANH, **T6 Detroit VÀNG**. Luật "không liền VÀNG" làm **T7 không được là ĐỎ**. Vị trí ĐỎ sớm nhất là **T8**, kế đó là **T12**.
6. **Đề xuất:**
   - **T8 = Dresden 1945, khung "cháy và dựng lại"** (1945 → đống đổ nát Frauenkirche để nguyên tới 1994 → dựng lại 2005). Khung này khớp thẳng lời hứa L1 *"rise, burn and rebuild"*.
   - **Berlin 1945 vào hàng đợi có điều kiện ở T12**, chỉ khi Dresden qua chỉ số sau đăng ở §5.4.
   - **Để sau:** Warsaw, Hiroshima, Constantinople, Tenochtitlan.
   - **Giữ ở luồng VÀNG của NC-LS:** Vienna, Malta. Hai đề tài này không phải ĐỎ, nên không chiếm suất ĐỎ.
   - **Bỏ:** Nanjing, Stalingrad, Jerusalem ×2, Derry.
7. **Rủi ro chính sách YouTube đọc nguyên văn (§3.1):**
   - Thứ đe doạ cả series là **"denial or minimization of a well-documented, major violent event"** (hate speech). Bối cảnh giáo dục **phải nằm trong hình hoặc tiếng của chính video**.
   - Về quảng cáo, **"footage of war with graphic depictions of injury, death, or suffering in any context"** không được quảng cáo. Khoản chiến tranh Ukraina (23/03/2022) vẫn ghi trên trang. Đây là thêm một lý do loại Stalingrad.
8. **Bình luận đối thủ** (2 075 bình luận, 21 video, đếm tay):
   - Mỗi đề tài có kiểu gây chuyện riêng. Nanjing có 18 bình luận tranh cãi phủ nhận/xin lỗi, Dresden có 8 bình luận "tội ác hay chính đáng", Warsaw có 7 bình luận kéo sang thời sự (5 về Gaza). Malta và Vienna có khẩu hiệu thập tự chinh, Derry có khẩu hiệu giáo phái và tranh tên gọi. Berlin có meme về Hitler (3 006 like).
   - Có một tín hiệu tốt: ở Hiroshima, khán giả **thưởng cho cách kể "không biện minh, không đổ lỗi"** (2 bình luận, 2 653 và 1 430 like).
9. **Khung chung thành quy trình đo được (§5):**
   - **G0** gồm 12 mục ĐÚNG/SAI.
   - **G1-R** gồm 11 mục trình chủ dự án.
   - **9 luật K đề xuất** (K-R1…K-R9), đo được bằng regex trên `.srt`/log chữ, manifest tài sản có thẻ biểu tượng, manifest lớp bản đồ và bảng thứ tự tập.
   - **7 chỉ số sau đăng**, có ngưỡng dừng nhịp ĐỎ.
10. **Chi phí thật:** YouTube **1 434/2 500 đv**; Claude API **$0**; ElevenLabs **0**; giờ máy **≈ 0,1 h**; WebSearch 7 lượt; 8 trang chính sách đọc bằng `curl`.

### Bảng quyết định đề xuất (chờ chủ dự án duyệt)
| # | Đề xuất | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|---|
| R1 | **T8 = Dresden 1945 (ĐỎ-K), khung "cháy và dựng lại"**: tập trung vào nơi chốn (Altmarkt, Frauenkirche, Zwinger, sông Elbe) từ 1930s → 13–15/2/1945 → đống đổ nát 1945–1994 → dựng lại 1994–2005 → hôm nay | Khớp lời hứa L1 tốt nhất trong mọi ứng viên. 0/5 video đầu có nguồn. Không ai dựng nơi chốn 3D qua cả ba giai đoạn. Có con số thương vong được một uỷ ban chính thức chốt (Historikerkommission 2010: tối đa 25 000), nên kiểm soát được tranh cãi số. Dữ liệu Sachsen/Dresden mở **(chưa kiểm)** | Điểm 20 đúng ngưỡng. Cầu (4) thấp hơn Berlin: dài lớn nhất 669 578, 9 video ≥ 100 nghìn. Tranh luận "tội ác chiến tranh" chiếm bình luận (8/200). Cực hữu Đức dùng sự kiện này làm biểu tượng | Cần tiền kỳ rủi ro riêng (≥ 2 truyền thống), luật câu chữ §4.1, chấm mù 3 góc. Dùng lại mô-đun khói/lửa M7 và nhà theo năm M9 của V6 (NC-LS §5) | Bị trích cắt làm tuyên truyền "Bombenholocaust" → cấm cụm này trong lời kênh, cấm mọi con số ngoài khoảng có nguồn, không hình thi thể. **Luật Đức §130(5) StGB (chưa tư vấn luật)** |
| R2 | **Berlin 1945 vào hàng đợi CÓ ĐIỀU KIỆN, sớm nhất T12**, chỉ khi Dresden qua §5.4 | Cầu lớn nhất trong nhóm đạt (8,17 triệu; 22 video ≥ 100 nghìn; Short 12,6 triệu). Dữ liệu Berlin mở rất tốt **(chưa kiểm)**. Hero mạnh (Reichstag cháy 1933 → bị đánh chiếm 1945 → mái vòm 1999) | Khoảng trống chỉ 3 (đúng ngưỡng). Rủi ro biểu tượng Quốc xã. Luật Nga 354.1 về "thông tin sai về hoạt động của Liên Xô". Bình luận có meme tôn vinh | Cần kết quả thật của Dresden trước khi mở tiền kỳ | Gần (c): ký ức chiến thắng 1945 được Nga dùng trong tuyên truyền thời chiến → khung thuần nơi chốn, không lời phán xét chính trị hiện tại. Nếu chiến sự leo thang hoặc có điểm nối trực tiếp mới → chuyển sang BỎ |
| R3 | **Để sau: Warsaw 1944** (21, trượt vì cầu 3) | Khoảng trống lớn nhất (5). Câu chuyện nơi chốn đặc biệt: Phố Cổ dựng lại một phần nhờ tranh thế kỷ 18 của Bellotto, UNESCO ghi nhận **(chưa kiểm)** | Cầu chỉ 3 (5 video ≥ 100 nghìn). Tìm bổ sung góc "dựng lại" cho thấy cầu vừa (dài lớn nhất 219 720) | Không chiếm suất | Bình luận kéo sang Gaza/NATO (7/199). Luật IPN Ba Lan |
| R4 | **Để sau: Hiroshima** (20, trượt vì khoảng trống 2) | Cầu khổng lồ (14 video dài ≥ 1 triệu). Dữ liệu 3D mở **(chưa kiểm)** | Đã có video 3D chi tiết (1,97 triệu) và góc "thành phố hồi sinh" (11,9 triệu). Video dẫn đầu dùng footage không che | Chỉ xét lại khi có góc chưa ai làm (ví dụ tàu điện Hiroden chạy lại 3 ngày sau, quy hoạch 1949) | Ad: footage thương tích không quảng cáo. Tranh luận "đáng/không đáng" |
| R5 | **Để sau: Constantinople 1453, Tenochtitlan 1521** (19 – sát ngưỡng −5 %) | Cầu lớn (Constantinople 4,05 triệu; Short 8,82 triệu). Tenochtitlan có góc "hồ bị tát cạn → thành phố lún" | Constantinople: khoảng trống 2, đã có tái dựng AI. Tenochtitlan: cầu 3 | Đo lại sau 2 tập ĐỎ-K | Constantinople: Hy Lạp–Thổ (bình luận 8 366 like dự báo "chiến tranh trong bình luận"), Hagia Sophia 2020 |
| R6 | **Giữ ở luồng VÀNG NC-LS: Vienna, Malta**. Không chiếm suất ĐỎ-K | Đã có trong hàng đợi NC-LS (Malta #5, Vienna cuối) | Khoảng trống thấp (1 và 2) | Không đổi | Khung văn minh/tôn giáo: 5/20 (Vienna) và 4/20 (Malta) tiêu đề đối thủ dùng. Áp luật câu chữ §4 của báo cáo này |
| R7 | **Bỏ: Nanjing 1937, Stalingrad, Jerusalem 1099/1187, Derry 1689** | Tránh rủi ro không kiểm soát được | Mất cầu lớn (Stalingrad 6,81 triệu; Nanjing Short 6,49 triệu) | Không | Nanjing: luật Trung Quốc về anh hùng liệt sĩ, tranh cãi phủ nhận ở Nhật, 12/14 tiêu đề đối thủ khung kinh dị, không có tư liệu hình dùng được ngoài ảnh thảm sát |
| R8 | **Đổi tên mức "ĐỎ có kiểm soát" thành "ĐỎ-K"** | `QUAN-TRI-RUI-RO.md` §1 đang định nghĩa **ĐỎ = "Cấm, không ngoại lệ"**. Dùng cùng chữ sẽ làm K và P hiểu sai | Thêm một nhãn | P sửa QUAN-TRI-RUI-RO §1: thêm hàng "ĐỎ-K" | Không |
| R9 | **Duyệt quy trình §5** (G0, G1-R, K-R1…K-R9, chỉ số sau đăng và ngưỡng dừng) | Biến 9 kiểm soát XX1 thành bảng ĐÚNG/SAI đo được | Thêm công tiền kỳ (≈ 4–8 h người/tập **(ước)**) và 3 lượt REVIEWER Opus (≈ $1–3/tập **(ước)**) | K viết 9 luật. P thêm G1-R vào mẫu G1 | Ngưỡng sau đăng là đề xuất, chưa có số kênh → hiệu chỉnh sau Dresden |

**Chỉ số trong ±5 % quanh ngưỡng (nêu tên):**
- **Ngưỡng /25 = 20:**
  - Dresden **20 (0 %)** và Hiroshima **20 (0 %)**. Vienna 20 (0 %) nhưng trượt vì khoảng trống.
  - Berlin **21 (+5 %)**, Warsaw **21 (+5 %)**.
  - Constantinople **19 (−5 %)**, Tenochtitlan **19 (−5 %)**.
  - Thước là phiên tự chấm, sai ±1 điểm là bình thường. Vì vậy **Dresden và Berlin không vượt ngưỡng một cách chắc chắn**.
- **Ngưỡng khoảng trống = 3:** Berlin **3 (0 %)**, Dresden **3 (0 %)**, Tenochtitlan 3 (0 %).
- **Ngưỡng cầu = 4:** Dresden **4 (0 %)**, Nanjing 4 (0 %).
- **Ngưỡng lượt xem** (video dài, trừ khi ghi Short):
  - 100 nghìn: Malta — Battle Chronicles 102 930 (+2,9 %); Stalingrad — EpicWar 95 090 (−4,9 %). Short: Malta 97 699 (−2,3 %), Nanjing 99 555 (−0,4 %), Tenochtitlan 104 527 (+4,5 %).
  - 500 nghìn: Stalingrad — Disturban History 501 694 (+0,3 %); Dresden — The Operations Room 520 400 (+4,1 %) → Dresden có 2 video ≥ 500 nghìn, có thể thành 1 tuỳ ngày đo. Berlin — Flashback History 480 610 (−3,9 %) và EASTERN FRONT 477 422 (−4,5 %).
  - 1 triệu: Constantinople — Reply History 1 044 405 (+4,4 %) và Chronicle 989 235 (−1,1 %); Vienna — History & Weapon 1 030 239 (+3,0 %); Hiroshima — BBC News Urdu 1 039 304 (+3,9 %) và Timeline 1 009 029 (+0,9 %); Tenochtitlan — Kings and Generals 973 723 (−2,6 %). Short ≥ 1 triệu: Constantinople, Vienna, Stalingrad, Hiroshima, mỗi đề tài có 1 video sát ngưỡng (`de-tai-cau.json` → `sat_nguong_5pct`).

**Việc chờ chủ dự án:** §11.

---

## 1. Ứng viên và lọc (c)

### 1.1 Ánh xạ khung XX1
| Điều kiện XX1 | Cách đo trong phiên |
|---|---|
| (a) /25 ≥ 20, cầu ≥ 4, khoảng trống ≥ 3 | Thước NC-LS (§2), số ở `cham-diem.json` |
| (b) khép lại trước ~1950 | năm kết thúc sự kiện chính |
| (c) không gắn trực tiếp chiến sự/bạo lực đang diễn ra | **c1:** nơi đó hoặc các phe đang có chiến sự hay bạo lực vũ trang có tổ chức (tính tới 10/2026). **c2:** chính sự kiện được dùng trực tiếp làm biểu tượng trong xung đột đó (phát ngôn của lãnh đạo nhà nước, nghi lễ thường kéo theo bạo lực, tuyên truyền của nhóm vũ trang). **Vi phạm (c) = c1 VÀ c2.** Có c1 mà không có c2 → "cảnh báo gần (c)" |

**Giới hạn:** phiên **không xác nhận được qua web trạng thái chiến sự tháng 10/2026** (tìm kiếm chỉ trả tin ≤ 2025). Ở c1, phiên dùng tình trạng đã biết tới giữa 2026 và chọn phương án thận trọng (§11).

### 1.2 Bốn ứng viên phiên thêm (vì sao chọn)
| Ứng viên | Vì sao |
|---|---|
| **Berlin 1945** | Cầu cực lớn (8,17 triệu dài; Short 12,6 triệu). Nơi chốn đổi mạnh theo thời gian (1933 → 1945 → Bức tường → 1999). Dữ liệu thành phố mở thuộc loại tốt nhất châu Âu **(chưa kiểm)** |
| **Warsaw 1944** | Ca "phá huỷ có chủ đích → dựng lại theo tranh" hiếm có. Đúng lõi lời hứa "rise, burn and rebuild" |
| **Hiroshima 1945** | Cầu lớn nhất mẫu. Thành phố bị xoá rồi quy hoạch lại (Luật Thành phố Tưởng niệm Hoà bình 1949 **(chưa kiểm)**) |
| **Nanjing 1937** | Kiểm giới hạn trên của khung: cầu lớn (Short 6,49 triệu), nhưng là thảm sát dân thường và đang bị phủ nhận. Đưa vào để có một ca "ĐỎ không kiểm soát được" làm mốc so sánh |

Đã cân nhắc nhưng không đưa vào (giới hạn 4): Baghdad 1258 (Iraq còn bạo lực vũ trang, c1), Smyrna 1922 (Hy Lạp–Thổ, cầu chưa đo), Masada (gần Israel–Palestine, c1), Leningrad (c như Stalingrad).

### 1.3 Kết quả lọc (c)
| Đề tài | c1 | c2 | Kết luận |
|---|---|---|---|
| **Jerusalem 1099** | có: xung đột Israel–Palestine còn bạo lực, Jerusalem là trung tâm | có: khung "thập tự chinh/thánh địa" được dùng trong diễn ngôn các phe | **LOẠI**, không đo |
| **Jerusalem 1187** | có | có: Saladin/Hattin được dùng làm biểu tượng trong diễn ngôn xung đột hiện nay | **LOẠI**, không đo |
| **Stalingrad 1942–43** | có: Nga đang trong chiến sự với Ukraina (trạng thái 10/2026 chưa kiểm; thận trọng) | có: nguyên thủ Nga dùng Stalingrad trực tiếp để nói về cuộc chiến hiện nay (bài phát biểu tại Volgograd 02/2023 — **kiến thức của phiên, chưa kiểm nguồn gốc**) | **LOẠI** (đã đo, số giữ để tham khảo) |
| **Derry 1689** | có: nhóm bán vũ trang cộng hoà ly khai còn hoạt động; rối loạn và bom xăng quanh lễ diễu hành tưởng niệm cuộc vây ở Derry (2019, kiểm qua tin địa phương) | có: cuộc vây là biểu tượng trung tâm của một phe, và lễ diễu hành hằng năm là điểm nóng | **LOẠI** (đã đo: cầu cũng chỉ 1/5, trượt (a) kể cả nếu không loại) |
| Berlin 1945 | có (phía Nga) | một phần: chiến thắng 1945 nói chung được dùng trong tuyên truyền, nhưng nơi chốn không có chiến sự | ĐẠT, **cảnh báo gần (c)** |
| Warsaw 1944 | không (Ba Lan không có chiến sự) | — | ĐẠT |
| Dresden, Hiroshima, Nanjing, Constantinople, Vienna, Malta, Tenochtitlan | không có chiến sự hay bạo lực vũ trang có tổ chức gắn với nơi/phe | — | ĐẠT. Ghi chú: Dresden có tuần hành cực hữu ngày 13/2. Đó là biểu tình, không phải bạo lực vũ trang có tổ chức → không đạt c1 |

Mọi đề tài còn lại đều đạt (b): sự kiện chính kết thúc trước 1950.

---

## 2. Cầu và khoảng trống

### 2.1 Cách đo (đúng §3.1 NC-LS)
- Mỗi đề tài **1 lượt `search.list`** (type=video, relevance, 50, regionCode=US, relevanceLanguage=en, không giới hạn ngày) + `videos.list`. Dài ≥ 480 s, Short ≤ 180 s.
- **Loại tay** video lạc đề (chỉ duyệt video dài ≥ 20 nghìn và Short ≥ 100 nghìn), tổng **24 video**:
  - Vienna: trận 1529, trận Párkány, trailer phim.
  - Malta: 3 video về cuộc vây 1940–42.
  - Constantinople: tiểu sử Mehmed, lịch sử Istanbul tổng quát.
  - Stalingrad: sách nói 14 giờ.
  - Dresden: 3 video về cả chiến dịch ném bom chiến lược.
  - Warsaw: khởi nghĩa Ghetto 1943 (sự kiện khác), Short về 1939, Short nhạc.
  - Hiroshima: "quả bom thứ ba", "vì sao không ném Tokyo".
  - Berlin: 3 video về cả mặt trận 1945.
  - Nanjing: toàn chiến tranh Trung–Nhật.
- So với NC-LS: Vienna và Malta đo lại cùng truy vấn. Kết quả search thay đổi theo ngày, và lần này loại tay chặt hơn: Vienna ≥ 100 nghìn **15** (NC-LS: 20), Malta **15** (NC-LS: 17).
- 2 lượt tìm **bổ sung** cho góc "dựng lại" (Warsaw, Dresden) **không vào thước**, chỉ để đọc khoảng trống.

### 2.2 Bảng cầu (đọc 17/10/2026)
| Đề tài | Dài ≥ 8' | Dài lớn nhất | ≥ 100 k | ≥ 500 k | ≥ 1 tr | Trung vị 10 dài lớn nhất | Short lớn nhất | Dài trong 90 ngày (lớn nhất) | Top 5 có nguồn | Dài nhắc AI | Kênh lớn đã làm |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Hiroshima 1945 | 25 | **13 408 216** | **24** | **17** | **14** | **3 734 468** | 3 036 371 | 2 (287 242) | 1/5 | 0 | War Stories, Kyle Hill, The Operations Room (3D), Infographics Show, Mark Felton, IWM, BBC |
| Berlin 1945 | 30 | 8 166 613 | 22 | 12 | 8 | 2 980 711 | **12 642 692** | 1 (53 503) | 3/5 | 3 | Mark Felton, Armchair Historian, Real Time History, Battle Guide, IWM |
| Stalingrad *(loại (c))* | 33 | 6 806 440 | 25 | 16 | 12 | 3 407 421 | 9 305 570 | 4 (260 355) | 2/5 | 1 | History Hit, Armchair Historian, IWM, Kings and Generals, TimeGhost |
| Constantinople 1453 | 20 | 4 048 324 | 11 | 7 | 6 | 1 089 292 | 8 822 384 (AI) | 1 (rất nhỏ) | 3/5 | **4** | Kings and Generals, SandRhoman, Infographics, 2 kênh tái dựng AI |
| Vienna 1683 | 28 | 3 051 746 | 15 | 9 | 8 | 1 681 957 | 969 982 | 2 (rất nhỏ) | 1/5 | 3 | Extra History (4 video), SandRhoman, HistoryMarche, Armchair |
| Tenochtitlan 1521 | 15 | 2 415 485 (về thành phố) | 4 | 3 | 2 | 9 302 | 104 527 | 5 (rất nhỏ) | 3/5 | 3 | Invicta, Armchair Historian, Kings and Generals |
| Warsaw 1944 | 18 | 2 264 069 | 5 | 1 | 1 | 102 431 | 290 353 | 2 (49 050) | 2/5 | 0 | Extra History, TimeGhost, Sabaton History |
| Nanjing 1937 | 14 | 2 154 926 | 8 | 5 | 3 | 615 799 | 6 489 390 | 1 (rất nhỏ) | 2/5 | 0 | Into the Shadows, Simple History, Captivating History (không có K&G, Armchair) |
| Malta 1565 | 32 | 1 339 767 | 15 ⚠ | 3 | 2 | 319 496 | 157 950 | 3 (380 646) | 1/5 | 2 | Kings and Generals, SandRhoman, History Hit, History Mapped Out (09/2026) |
| Dresden 1945 | 25 | 669 578 | 9 | 2 ⚠ | 0 | 317 221 | 1 217 763 (Pathé) | 2 (55 379) | **0/5** | 1 | TIKhistory, The Operations Room (hoạt hình), HardThrasher |
| Derry 1689 *(loại (c))* | 22 | 338 958 | 1 | 0 | 0 | 2 175 | 22 023 | 1 (0) | 0/5 | 1 | không có kênh lớn (BBC đăng lại) |
⚠ = có video sát ngưỡng ±5 % (§0).

**Tìm bổ sung góc "dựng lại" (không vào thước):**
- **Dresden:** 1 video dài 560 197 (kênh kiến trúc, "phá huỷ và dựng lại"); Megaprojects 130 120; 1 Short then/now 211 086.
- **Warsaw:** Megaprojects 219 720; Short then/now 570 580 và 262 977.
- Đọc: góc "dựng lại" **đã có người làm bằng ảnh 2D/then-now**. **Chưa có ai** dựng nơi chốn 3D đúng năm nối trận đánh với tái thiết.

### 2.3 Khoảng trống (đọc từ bảng + khung tiêu đề + bình luận)
| Đề tài | Khung tiêu đề đối thủ (20 video dài lớn nhất, đếm) | Khoảng trống của mình |
|---|---|---|
| Dresden | 7/20 khung kinh dị, **4/20 đặt câu phán xét** ("tội ác hay chính đáng") | Không ai kể **nơi chốn qua ba giai đoạn** (phố cổ → cháy → đống đổ nát 50 năm → dựng lại) bằng 3D đúng năm, có nguồn. 0/5 video đầu có nguồn → **"every date sourced" là khác biệt thật** |
| Berlin | 2/20 kinh dị, 1/20 phán xét | Then/now đã có dạng đi bộ (1 kênh "No AI" 66 400; 1 kênh 432 772). Thiếu: **bản đồ 3D thành phố theo ngày 16/4–2/5/1945 nối với Reichstag 1933/1999** |
| Warsaw | 4/18 kinh dị | **Lớn nhất:** chưa video dài nào nối khởi nghĩa → phá huỷ có kế hoạch → dựng lại theo tranh Bellotto |
| Hiroshima | 2/20 kinh dị; video lớn nhất dùng footage không che | Hẹp: đã có mô hình 3D (1,97 triệu) và góc khoa học "thành phố hồi sinh" (11,9 triệu) |
| Constantinople | 3/20 tái dựng AI | Hẹp: tái dựng AI đã chiếm góc "nơi chốn" |
| Vienna / Malta | **5/20 và 4/20 khung văn minh/tôn giáo** | Hẹp (NC-LS: 1 và 2). Nếu làm, khoảng trống duy nhất là **không dùng khung tôn giáo** |
| Tenochtitlan | 0 | Vừa: góc "hồ bị tát cạn → thành phố lún" chưa thấy trong mẫu |
| Nanjing | **12/14 khung kinh dị** | Có khoảng trống về độ phủ, nhưng không có cách kể nơi chốn mà không lấy cái chết làm trung tâm → không dùng được |

---

## 2.4 Chấm /25 (thước NC-LS: cầu · khoảng trống · dữ liệu timelapse · bản đồ/tranh có quyền · hero)
Chỗ chưa kiểm giấy phép bị chấm **tối đa 4** (chặt hơn NC-LS, nơi một số ô chưa kiểm được 5).

| # | Đề tài | Cầu | KT | Dữ liệu | Bản đồ/tranh | Hero | **/25** | (a) | (b) | (c) | Mức |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **Berlin 1945** | 5 | 3 | 4 | 4 | 5 | **21** | ĐẠT | ĐẠT | ĐẠT, cảnh báo | ĐỎ-K |
| 2 | **Warsaw 1944** | 3 | 5 | 4 | 4 | 5 | **21** | TRƯỢT (cầu) | ĐẠT | ĐẠT | ĐỎ-K |
| 3 | **Dresden 1945** | 4 | 3 | 4 | 4 | 5 | **20** | **ĐẠT (đúng ngưỡng)** | ĐẠT | ĐẠT | ĐỎ-K |
| 4 | Hiroshima 1945 | 5 | 2 | 4 | 4 | 5 | 20 | TRƯỢT (KT) | ĐẠT | ĐẠT | ĐỎ-K |
| 5 | Vienna 1683 | 5 | 1 | 4 | 5 | 5 | 20 | TRƯỢT (KT) | ĐẠT | ĐẠT | VÀNG (NC-LS) |
| 6 | Constantinople 1453 | 5 | 2 | 3 | 4 | 5 | 19 | TRƯỢT | ĐẠT | ĐẠT | ĐỎ-K |
| 7 | Tenochtitlan 1521 | 3 | 3 | 4 | 4 | 5 | 19 | TRƯỢT | ĐẠT | ĐẠT | VÀNG đậm |
| 8 | Malta 1565 | 5 | 2 | 3 | 3 | 5 | 18 | TRƯỢT | ĐẠT | ĐẠT | VÀNG (NC-LS) |
| 9 | Nanjing 1937 | 4 | 4 | 3 | 2 | 4 | 17 | TRƯỢT | ĐẠT | ĐẠT | ĐỎ (không kiểm soát được) |
| 10 | Stalingrad | 5 | 2 | 2 | 3 | 5 | 17 | TRƯỢT | ĐẠT | **TRƯỢT** | loại |
| — | Derry 1689 | 1 | — | — | — | — | — | TRƯỢT | ĐẠT | **TRƯỢT** | loại |
| — | Jerusalem 1099 / 1187 | không đo | | | | | | | | **TRƯỢT** | loại |

**Ghi chú chấm (dữ liệu và quyền, đều chưa tải tệp):**
- **Dresden:**
  - Dữ liệu: geodata mở của bang Sachsen (mô hình nhà LoD2, bản đồ lịch sử) với giấy phép dl-de **(chưa kiểm)**. Phố trước 1945 phải dựng **ghost** từ bản đồ PD.
  - Hình: ảnh không quân Mỹ (tác phẩm chính phủ Mỹ, PD); ảnh RAF (bản quyền Hoàng gia đã hết hạn **(chưa kiểm từng mục)**); Deutsche Fotothek (nhiều mục CC BY-SA **(chưa kiểm điều khoản chia sẻ lại với video)**).
  - **Loại ảnh của nhiếp ảnh gia còn bản quyền** (ví dụ loạt ảnh nổi tiếng chụp từ tháp toà thị chính: tác giả mất 1977, bảo hộ tới 2047).
  - Hero: Frauenkirche (nguyên → đống đổ nát → dựng lại), Altmarkt, Zwinger, Semperoper.
- **Berlin:**
  - Dữ liệu: bản đồ tuổi nhà của Umweltatlas Berlin, mô hình 3D LoD2, giấy phép dl-de/zero **(chưa kiểm)**.
  - Hình: Bundesarchiv CC BY-SA; ảnh quân đội Mỹ PD. Ảnh cắm cờ trên Reichstag của nhiếp ảnh gia Xô viết **còn bản quyền theo luật Nga (chưa kiểm) → không dùng**.
- **Warsaw:**
  - Dữ liệu: mô hình nhà 3D quốc gia Ba Lan và ảnh hàng không 1945 trên geoportal **(chưa kiểm)**.
  - Hình: tranh Bellotto (PD); ảnh NAC **(điều khoản chưa kiểm)**.
- **Hiroshima:**
  - Dữ liệu: mô hình 3D PLATEAU (giấy phép mở, **chưa kiểm** phạm vi thương mại); bản đồ USSBS 1946 (PD).
  - Hình: ảnh của nhiếp ảnh gia Nhật còn bản quyền → không dùng.
- **Nanjing:**
  - Hình: tư liệu hình gần như toàn là cảnh thảm sát. Phim của John Magee **(quyền chưa kiểm)** → không dùng được ở khung "không thi thể".

---

## 3. Hồ sơ rủi ro từng đề tài

### 3.1 Chính sách YouTube (đọc bằng `curl`, `hl=en`, 17/10/2026; trích nguyên văn ngắn)
| Trang | Đoạn liên quan | Áp vào |
|---|---|---|
| Hate speech — `support.google.com/youtube/answer/2801939` | *"Denial or minimization of a well-documented, major violent event or the victimhood of such an event."* · *"For educational, documentary, scientific, or artistic content that includes hate speech, this context must appear in the images or audio of the video itself. Providing it in the title or description is insufficient."* · cho phép *"Historical footage of an event, like WWII, which doesn't promote violence or hatred."* | Mọi đề tài thảm sát/ném bom: **không hạ thấp số nạn nhân**. Dùng khoảng số có nguồn; bối cảnh nằm trong lời và hình |
| Violent extremist or criminal organizations — `answer/9229472` | cấm *"insignia, logos, or symbols of violent extremist … organizations in order to praise or promote them"*; *"Glorifying violence against civilians"* | Berlin, Dresden, Nanjing: không biểu tượng Quốc xã / quân kỳ Đế quốc Nhật trong khung và thumbnail; không câu nào tôn vinh |
| Violent or graphic content — `answer/2802008` | luật áp cả *"video descriptions, thumbnails, comments"*; nội dung hợp luật nhưng không hợp mọi khán giả bị *"age-restricted … under 18 years of age or signed out"* | Bình luận cũng thuộc phạm vi → **lọc bình luận là nghĩa vụ**, không phải tuỳ chọn |
| Advertiser-friendly — `answer/6162278` | đủ quảng cáo: *"Non-graphic educational coverage or discussion of war and/or conflict"*; hạn chế: *"Dead bodies with obvious injury or damage in educational or documentary settings"*; không quảng cáo: *"Footage of war with graphic depictions of injury, death, or suffering in any context"* · sự kiện nhạy cảm gồm *"conflict, or mass acts of violence. This policy applies even if the content contains no graphic imagery"* · *"March 23, 2022: Due to the war in Ukraine, content that exploits, dismisses, or condones the war is ineligible for monetization until further notice."* · *"Content that is gratuitously incendiary, inflammatory, or demeaning may not be suitable for advertising."* · cấm *"Using keywords related to a sensitive event to attempt to drive additional traffic."* | Luật hình NC-LS §7.5 áp nguyên. Khoản Ukraina là lý do phụ để loại Stalingrad. Không nhồi từ khoá |

Trang `answer/10834785` (Misinformation) không có điều riêng về sự kiện lịch sử. Phần đã trích ở `QUAN-TRI-RUI-RO.md` §2 (footage cũ gán sai) vẫn áp.

### 3.2 Hồ sơ từng đề tài
Cột "bình luận gây chuyện" = số đếm tay trong mẫu ≈ 200 bình luận cấp 1/đề tài (`binh-luan-dem.json`). Loại: **A** đối đầu dân tộc/tôn giáo · **B** phủ nhận/biện minh/tranh cãi tội ác · **C** nối chiến sự hiện tại · **D** tôn vinh/meme cực đoan · **E** tranh cãi số thương vong · **F** tranh cãi tên gọi/ghi công.

| Đề tài | Nhóm/quốc gia có thể phản ứng | Điểm tranh cãi sử học chính | Rủi ro chính sách YouTube | Pháp lý đã biết (**chưa tư vấn luật**) | Bình luận gây chuyện (mẫu) |
|---|---|---|---|---|---|
| **Dresden 1945** | cực hữu Đức (dùng làm biểu tượng); cựu binh/người Anh; người Đức ở Dresden; nhóm chống phát xít | **số người chết**: tuyên truyền thời chiến và cực hữu thổi lên hàng trăm nghìn; Uỷ ban Sử gia Dresden 2010 chốt **tối đa 25 000**. Dresden là mục tiêu quân sự hay không; "tội ác chiến tranh"; cách gọi "terror bombing" | hate speech (thổi phồng số nạn nhân có thể bị dùng để hạ thấp Holocaust: tranh cãi về "Bombenholocaust"); ad: ảnh thi thể đường phố | Đức: **§130 StGB** (kích động thù hận; từ 2022 có khoản 5 về phủ nhận/hạ thấp nghiêm trọng diệt chủng, tội ác chiến tranh); **§86a** (biểu tượng tổ chức vi hiến) | B 8 · D 1 · 2 video dài tắt bình luận |
| **Berlin 1945** | Nga (nhà nước, khán giả); Ukraina, Ba Lan; Đức; cộng đồng tân Quốc xã (meme) | vai Hồng quân (giải phóng hay chiếm đóng); **bạo lực tình dục hàng loạt của binh lính Xô viết** (Nga phủ nhận về chính trị); số thương vong; sự kết thúc của Hitler | biểu tượng cực đoan (chữ vạn, SS); tôn vinh (meme); ad | Đức §86a, §130; **Nga Điều 354.1 BLHS** (phục hồi chủ nghĩa Quốc xã, gồm "thông tin sai cố ý về hoạt động của Liên Xô trong Thế chiến II"; từ 2021 có tình tiết qua Internet; 2022 có luật hành chính cấm đánh đồng mục tiêu Liên Xô với Đức Quốc xã **(chưa kiểm văn bản gốc)**) | D 2 (meme Hitler 3 006 like) · B 1 · 1 bình luận 762 like khen kênh **không** dùng Thập tự Sắt |
| **Warsaw 1944** | Ba Lan; Nga; Đức; cộng đồng Do Thái (dễ lẫn với khởi nghĩa Ghetto 1943) | Hồng quân dừng bên kia sông Vistula; quyết định khởi nghĩa có đúng không; số dân thường chết (thảm sát Wola); vai các đơn vị cộng tác | ad (footage); hate speech nếu hạ thấp nạn nhân | **Ba Lan, Luật IPN**: Điều 55 (phủ nhận tội ác Quốc xã và cộng sản); Điều 55a 2018 (gán trách nhiệm cho "Dân tộc Ba Lan") bị sửa trong năm, thành trách nhiệm dân sự hay bãi bỏ **nguồn mâu thuẫn, chưa kiểm**; vụ dân sự 2021 với hai sử gia | C 7 (Gaza 5, NATO 2) · F 3 · A 1 |
| **Hiroshima 1945** | Nhật (hibakusha, thành phố); Mỹ (cựu binh); Hàn, Trung (nạn nhân Nhật) | có cần ném bom không (Alperovitz vs Frank); số chết (City of Hiroshima: ~140 000 tới cuối 1945 **(chưa kiểm)**); nạn nhân Hàn | ad: footage thương tích; giới hạn tuổi | không biết luật riêng | B 1 · khán giả khen cách kể trung tính |
| **Constantinople 1453** | Hy Lạp, Thổ; Chính thống giáo; dân tộc chủ nghĩa Thổ | "chinh phục" (Fetih) vs "sụp đổ" (Άλωση); cướp phá 3 ngày; Hagia Sophia 1453/1934/2020; quy mô quân | hate speech khi khung tôn giáo; ad thấp | Thổ: **Điều 301 TCK** (hạ nhục dân tộc Thổ); YouTube từng bị chặn ở Thổ (2008–10, 2014) **(chưa kiểm)**. Hy Lạp: **Luật 4285/2014** (phủ nhận diệt chủng được công nhận; không trực tiếp với 1453) | A 1 · F 1 · bình luận dự báo "chiến tranh Hy–Thổ trong bình luận" có 8 366 like |
| **Vienna 1683** | Thổ; cực hữu châu Âu (dùng 1683 làm biểu tượng chống Hồi giáo; tuyên ngôn của kẻ tấn công Oslo/Utøya 2011 nhắc 1683 **(chưa kiểm)**); Ba Lan (tranh công Sobieski) | "cứu châu Âu/Kitô giáo"; ngày 11–12/9 | hate speech khi khung tôn giáo | không biết luật riêng | A 3 · F 2 · 5/20 tiêu đề khung văn minh |
| **Malta 1565** | Malta; Thổ; cực hữu (khẩu hiệu thập tự chinh) | số quân hai bên; cách gọi tù binh | như Vienna | không biết | A 4 (khẩu hiệu thập tự chinh ×3) |
| **Tenochtitlan 1521** | Mexico; cộng đồng bản địa; Tây Ban Nha | "chinh phục" hay "liên minh bản địa lật Mexica"; hiến tế người dùng để biện minh; số chết do dịch bệnh | hate speech (khái quát hoá "man rợ") | không biết luật riêng | B 3 ("đáng bị", 891 like) · F 2 |
| **Nanjing 1937** | Trung Quốc (nhà nước, khán giả); Nhật (nhóm dân tộc chủ nghĩa); Đài Loan | **số nạn nhân** (Trung Quốc chính thức 300 000; giới sử học Nhật từ vài chục nghìn tới ~200 000; báo cáo nghiên cứu chung Nhật–Trung 2010 ghi khoảng khác nhau **(chưa kiểm)**); phủ nhận | **hate speech: phủ nhận/hạ thấp** — mọi con số thấp đều bị một phía xem là hạ thấp | **Trung Quốc: Luật Bảo vệ Anh hùng Liệt sĩ 2018; BLHS Điều 299-1 (2021)**; quy định địa phương Nam Kinh về cấm phủ nhận (dự thảo 2018, bản cuối chưa kiểm) | **B 18** · A 3 · 12/14 tiêu đề khung kinh dị |
| Stalingrad *(loại)* | Nga, Ukraina, Đức | số chết; vai lệnh "Không lùi một bước" | khoản Ukraina 23/03/2022 | Nga 354.1 | C 1 · bình luận lớn nhất là người Volgograd (13 349 like) |
| Derry *(loại)* | cộng đồng hợp nhất/dân tộc chủ nghĩa Bắc Ireland | tên gọi Derry/Londonderry; diễu hành | — | Anh/Bắc Ireland: luật trật tự công cộng về kích động thù hận **(chưa kiểm)** | A 3 · F 6 (tranh tên 5) |
| Jerusalem ×2 *(loại, không đo)* | — | — | — | — | — |

**Đọc bảng:** mỗi đề tài có **một kiểu gây chuyện trội**, nên có thể **thiết kế lọc theo kiểu** thay vì một danh sách chung:
- Dresden: B (tội ác hay chính đáng).
- Warsaw: C (nối thời sự).
- Berlin: D (meme tôn vinh).
- Vienna/Malta: A (khẩu hiệu thập tự chinh).
- Nanjing: B (phủ nhận).

**Hạn chế mẫu:** sắp theo `relevance` đẩy bình luận nhiều like lên đầu. Tranh cãi gay gắt thường nằm ở **trả lời**, mà phiên không đo. Số thật vì vậy có thể cao hơn.

---

## 4. Bộ kiểm soát cụ thể từng đề tài
Chi tiết đủ cho 2 đề tài vào hàng đợi (§4.1, §4.2). Các đề tài để sau dùng bảng gọn ở §4.3.

### 4.1 Dresden 1945 (T8 đề xuất)
**Nguồn (≥ 2 truyền thống sử học, mỗi claim nhạy cảm cần ≥ 1 nguồn mỗi phía):**
| Truyền thống | Tác giả / tác phẩm / lưu trữ |
|---|---|
| Đức (học thuật, chính thức) | **Rolf-Dieter Müller, Nicole Schönherr, Thomas Widera (chủ biên), *Die Zerstörung Dresdens 13. bis 15. Februar 1945*, 2010** (báo cáo Uỷ ban Sử gia Dresden); Götz Bergander, *Dresden im Luftkrieg* (1977, bản mở rộng 1994); Stadtarchiv Dresden; Bundesarchiv |
| Anh / Đồng minh | Frederick Taylor, *Dresden: Tuesday, 13 February 1945* (2004); Sinclair McKay, *Dresden: The Fire and the Darkness* (2020); Webster & Frankland, *The Strategic Air Offensive against Germany 1939–1945* (lịch sử chính thức, 1961); UK National Archives (hồ sơ AIR) |
| Mỹ | USAF Historical Division, *Historical Analysis of the 14–15 February 1945 Bombings of Dresden* (1953); AFHRA |
| **Nguồn CẤM dùng** | David Irving, *The Destruction of Dresden* (1963) và mọi con số bắt nguồn từ đó: bản án Irving v. Penguin & Lipstadt (2000) xác định ông bóp méo số liệu Dresden **(chưa kiểm văn bản bản án ở phiên này)**; tài liệu "Tagesbefehl 47" (con số giả) |

**Quy ước tên gọi:**
- "RAF Bomber Command and the US Eighth Air Force". Không dùng "the Allies destroyed…" chung chung.
- "Dresden" (không có địa danh kép).
- Gọi sự kiện là "the bombing of Dresden" / "the Dresden firestorm".

**Câu chữ:**
| Cấm (lời kênh, chữ trên hình, tiêu đề, mô tả, thumbnail) | Dùng thay |
|---|---|
| "Bombenholocaust", "Dresden holocaust", mọi so sánh với Holocaust | không so sánh |
| mọi con số người chết > 25 000 do kênh tự nói ("hundreds of thousands") | "up to 25,000 people, according to the city's historians' commission (2010)". Nếu nhắc con số tuyên truyền: "Nazi propaganda inflated the toll tenfold" + nguồn |
| "terror bombing" (giọng kênh), "war crime" / "justified" (kết luận của kênh) | "Historians still argue about whether…" + hai phía, mỗi phía một nguồn |
| "innocent city", "the Florence on the Elbe was murdered" | "a rail hub and industrial city, and also one of Europe's great baroque centres" (2 claim) |
| "the Allies' revenge" | không quy động cơ khi không có nguồn |

**Không đưa lên hình:**
- Thi thể, giàn hoả thiêu ở Altmarkt (ảnh nổi tiếng), người cháy.
- Chữ vạn, cờ Đức Quốc xã (kể cả trên toà nhà 1930s, nên dựng mặt đứng **không cờ**). Cờ Anh/Mỹ làm điểm nhấn.
- Tuần hành 13/2 hiện nay.
- Biên giới hiện đại: không cần.
- Lửa thể hiện bằng **vùng cháy theo giờ trên mái** (M7, sprite trung tính), không có người.

**Chấm mù nhạy cảm 3 góc** (REVIEWER Opus × 3 vai, độc lập, không thấy điểm của nhau; đầu vào: lời + bảng hình theo câu + 3 thumbnail):
| Vai | Câu hỏi | Ngưỡng đạt |
|---|---|---|
| G1 — sử gia Đức, hiểu văn hoá ký ức Đức và cách cực hữu dùng Dresden | (1) Có câu/hình nào có thể bị cắt ra làm tuyên truyền "nạn nhân Đức" không? (2) Con số và cách gọi có khớp báo cáo 2010? (3) Có hạ thấp tội ác Quốc xã bằng cách cân bằng giả? | **0 cờ "không chấp nhận"**; điểm "công bằng với góc của tôi" ≥ 4/5 |
| G2 — sử gia Anh về không chiến, quen hồ sơ Bomber Command | (1) Lý do quân sự (đầu mối đường sắt, Yalta, yêu cầu Liên Xô) có được trình bày đúng? (2) Có giọng kết tội tổ bay? | như trên |
| G3 — chuyên viên giám sát nội dung cực đoan/bài Do Thái (theo hướng dẫn của tổ chức giám sát) | (1) Có từ khoá, biểu tượng, cách đóng khung nào trùng mã của cực hữu? (2) Bình luận nào có thể bị kích hoạt? | 0 cờ; danh sách từ khoá lọc bình luận được G3 bổ sung |
Đạt khi **cả 3 vai đạt**. Một vai trượt → sửa → chấm lại vai đó (tối đa 3 vòng như REVIEWER). Ba vai là **đại diện mô phỏng, không phải cộng đồng thật** → đề xuất chủ dự án cân nhắc thêm **1 người đọc thật** có nền Đức (§11).

**Thumbnail an toàn:**
- (A) Frauenkirche ghép đôi: nửa trái đống đổ nát (dựng 3D từ ảnh PD, không người), nửa phải nhà thờ dựng lại; chữ "50 YEARS A RUIN". Số có trong claims.
- (B) Mặt bằng phố cổ nhìn từ trên, vùng cháy cam theo giờ, không chữ.
- Không máy bay ném bom làm tiêu điểm, không lửa có người, không cờ.

**Kế hoạch bình luận:**
- YouTube Studio: bật **giữ bình luận có thể không phù hợp để duyệt, mức nghiêm** (tên mục cụ thể trong Studio **chưa kiểm**).
- Danh sách từ chặn: cụm "Bombenholocaust" và các biến thể, "88", "1488", tên tác giả phủ nhận, các khẩu hiệu cực hữu Đức.
- Bình luận ghim: nguồn (≥ 2 truyền thống) + 1 câu chính sách: "Comments that deny or minimise any wartime atrocity, or praise any side's violence, will be removed."
- Không trả lời bình luận loại B/D. Xoá loại A/B/D vi phạm.
- 48 giờ đầu: chủ dự án duyệt hàng chờ 2 lần/ngày.

### 4.2 Berlin 1945 (T12, có điều kiện)
**Nguồn:**
- Anh/Mỹ: Antony Beevor, *Berlin: The Downfall 1945* (2002); Cornelius Ryan, *The Last Battle* (1966); Tony Le Tissier, *Race for the Reichstag* (1999).
- Đức: Militärgeschichtliches Forschungsamt, *Das Deutsche Reich und der Zweite Weltkrieg*, tập 10/1 (2008); Landesarchiv Berlin; Bundesarchiv.
- Xô viết/Nga: Hồi ký G. K. Zhukov (1969); V. I. Chuikov, *The End of the Third Reich*; A. V. Isaev, *Berlin 45-go* (2007).
- Lưu trữ TsAMO hạn chế truy cập → ghi rõ trong mục "the honest part".
- Bạo lực tình dục của binh lính: dùng nguồn học thuật có khoảng ước tính (ví dụ Miriam Gebhardt, *Als die Soldaten kamen*, 2015, **(chưa kiểm số)**). Một câu, không hình.

**Tên gọi:**
- "the Red Army" / "Soviet forces" (không "the Russians"). "German forces" / "the Wehrmacht" (không "the Nazis" cho mọi người lính).
- Cặp động từ "captured Berlin" (không "liberated" hay "conquered" làm kết luận).
- Địa danh dùng tên năm 1945 + tên hiện nay khi khác.

**Câu chữ:**
- Cấm: "the Nazis' last heroic stand", "brave defenders of the Reich", chơi chữ meme, "denazification" (thuật ngữ đang dùng trong tuyên truyền thời chiến hiện nay).
- Cấm mọi so sánh với chiến tranh hiện nay.
- Khuyên: "Historians estimate… (source); Soviet and Russian accounts put it at… (source)".

**Không đưa lên hình:**
- Chữ vạn, cờ SS, Thập tự Sắt làm biểu tượng phe. Phe Đức dùng **màu mã cố định**, không biểu tượng.
- Hitler: không chân dung làm tiêu điểm. Hầm Führerbunker chỉ là một chấm địa danh.
- Ảnh cắm cờ Reichstag: quyền chưa rõ, và đã thành biểu tượng tuyên truyền.
- Biên giới hiện đại Nga–Ukraina: không vẽ (không cần cho đề tài).
- Thi thể.

**Chấm mù 3 góc:**
- G1: sử gia Đức.
- G2: sử gia Nga/Xô viết, đọc theo góc nhìn ký ức chiến thắng.
- G3: chuyên viên giám sát nội dung cực đoan.
- Thêm câu hỏi riêng: "Có câu nào có thể bị cắt làm tuyên truyền cho chiến sự hiện nay của bất kỳ phía nào?"
- Ngưỡng như Dresden.

**Thumbnail:**
- Reichstag 3D theo 3 năm (1933 cháy · 1945 đổ nát · 1999 mái vòm), chữ "3 LIVES".
- Không cờ, không vũ khí, không người.

**Bình luận:**
- Như Dresden. Danh sách chặn thêm meme về Hitler, khẩu hiệu "có thể làm lại", tên đơn vị SS.
- Theo dõi riêng loại C: liên hệ chiến sự hiện nay.

### 4.3 Đề tài để sau / luồng VÀNG — bộ kiểm soát gọn
| Đề tài | Nguồn ≥ 2 truyền thống | Tên gọi | Cấm / khuyên | Không lên hình | Chấm mù 3 góc | Thumbnail |
|---|---|---|---|---|---|---|
| **Warsaw 1944** | Ba Lan: W. Borodziej, *The Warsaw Uprising of 1944*; Muzeum Powstania Warszawskiego; hồ sơ Biuro Odbudowy Stolicy (tái thiết). Anh: N. Davies, *Rising '44* (2003). Đức: H. von Krannhals, *Der Warschauer Aufstand 1944* (1962). Nga: tài liệu giải mật Bộ Quốc phòng Nga **(chưa kiểm)** | "Warsaw Uprising (1944)", luôn phân biệt với "Warsaw Ghetto Uprising (1943)"; "German-occupied Poland" | Cấm "Polish death camps", "the Poles collaborated" (khái quát). Khuyên: hai cách giải thích việc Hồng quân dừng, mỗi cách một nguồn | thi thể, thảm sát Wola; biên giới hiện đại phía đông | Ba Lan · Nga · Do Thái/giám sát bài Do Thái | Phố Cổ: tranh Bellotto ↔ 1945 ↔ hôm nay |
| **Hiroshima 1945** | Mỹ: USSBS, *The Effects of Atomic Bombs on Hiroshima and Nagasaki* (1946); R. B. Frank, *Downfall* (1999). Nhật: City of Hiroshima & Nagasaki (biên soạn), *Hiroshima and Nagasaki: The Physical, Medical, and Social Effects of the Atomic Bombings* (1981); Bảo tàng Tưởng niệm Hoà bình. Ba phía: T. Hasegawa, *Racing the Enemy* (2005) | "atomic bombing of Hiroshima"; "hibakusha" | Cấm "deserved", "justified" / "war crime" do kênh kết luận | người bị bỏng, thi thể, footage không che; quân kỳ Đế quốc; biên giới Kuril/Takeshima | Nhật · Mỹ · Hàn/Trung | A-Bomb Dome 1945 ↔ hôm nay; tàu điện |
| **Constantinople 1453** | Byzantine/Hy Lạp: Sphrantzes, Doukas, Kritoboulos; Venice: nhật ký Nicolò Barbaro. Ottoman: Tursun Beg, Aşıkpaşazade; F. Emecen, *İstanbul'un Fethi Olayı ve Meseleleri* (2003). Hiện đại: S. Runciman (1965); M. Philippides & W. Hanak (2011) | "the 1453 siege and capture of Constantinople (today's Istanbul)"; "Eastern Roman (Byzantine) Empire"; "Ottoman" (không "the Turks"); "Hagia Sophia (Ayasofya)" | Cấm "fall of Christendom", "Muslim conquest" (khung tôn giáo), mọi nhận định về quyết định 2020 | thánh giá vs trăng lưỡi liềm như biểu tượng đối đầu; biên giới biển Aegean/Síp | Hy Lạp · Thổ · giám sát khung tôn giáo | Tường Theodosius + thuyền qua đất liền (Galata) |
| **Tenochtitlan 1521** | Tây Ban Nha: thư Cortés; Bernal Díaz. Nahua: Florentine Codex quyển XII (Sahagún và cộng sự Nahua); M. León-Portilla, *Visión de los vencidos*. Hiện đại: M. Restall, *When Montezuma Met Cortés* (2018); R. Hassig (1994) | "Mexica" (Aztec), "Tenochtitlan (today's Mexico City)", "the Spanish and their Indigenous allies (Tlaxcalteca and others)" | Cấm "savages", "they had it coming", dùng hiến tế để biện minh | thi thể, hiến tế, dịch bệnh có người | Mexico bản địa · Tây Ban Nha · Mexico hiện đại | Hồ → thành phố lún (đường nước theo năm) |
| **Vienna 1683 / Malta 1565** (VÀNG) | Vienna: J. Stoye (1964), T. Barker (1967); Ottoman: biên niên Silahdar Fındıklılı Mehmed Ağa; nhật ký viên quan nghi lễ của Kara Mustafa (bản dịch Kreutel). Malta: nhật ký F. Balbi di Correggio (1568); A. Cassola, *The 1565 Ottoman Malta Campaign Register* (1998); S. C. Spiteri (thành luỹ) | "Ottoman army", "Habsburg–Polish relief army", "Knights Hospitaller (Order of St John)" | Cấm "saved Europe/Christendom", "Deus vult", "infidels", nhấn ngày 11/9 | thánh giá vs trăng lưỡi liềm; cờ | Thổ · Áo–Ba Lan / Malta · giám sát chống Hồi giáo | thành luỹ + glacis / Valletta mọc từ 1566 |

### 4.4 Đề tài bỏ: lý do kiểm soát không đủ
- **Nanjing:**
  - Mọi con số đều bị một phía coi là phủ nhận hoặc thổi phồng. Hai luật quốc gia kéo theo hai hướng trái nhau.
  - Hình nơi chốn không tách được khỏi cảnh thảm sát. 12/14 tiêu đề đối thủ khung kinh dị cho thấy cầu đến từ yếu tố ghê rợn.
  - Kết luận: không có phiên bản "ĐỎ-K" nào giữ được cả chất lượng lẫn an toàn.
- **Stalingrad:** đạt (b) nhưng trượt (c), và khoản Ukraina trên trang quảng cáo làm rủi ro kiếm tiền khó dự đoán.
- **Derry, Jerusalem:** trượt (c).

---

## 5. Khung chung "ĐỎ-K" thành quy trình đo được

### 5.1 G0 — bảng kiểm trước tiền kỳ (P làm, ĐÚNG/SAI; 1 SAI → không mở tiền kỳ)
| # | Mục | Đo bằng |
|---|---|---|
| G0-1 | /25 ≥ 20, cầu ≥ 4, khoảng trống ≥ 3; số trong ±5 % ngưỡng nêu tên | `cham-diem.json` của đề tài |
| G0-2 | Sự kiện khép lại trước ~1950 | năm kết thúc |
| G0-3 | Phép thử (c): không có (c1 VÀ c2); tra tin 30 ngày gần nhất | ghi 3 nguồn tin + ngày tra |
| G0-4 | Nhịp: trong mọi cửa sổ 4 tập liền có ≤ 1 ĐỎ-K; tập trước và sau không phải VÀNG; không ở T3–T5 | bảng thứ tự tập (`HANG-DOI.md`) |
| G0-5 | Có ≥ 2 truyền thống sử học tiếp cận được (sách/lưu trữ có thật, đã định vị) | danh sách nguồn |
| G0-6 | Câu "Why" không chứa phán xét đạo đức và không chứa từ cấm | regex K-R1 |
| G0-7 | Hero và nhịp timelapse chính dựng được **không cần** hình bị cấm (thi thể, biểu tượng cực đoan, cờ) | bảng hero |
| G0-8 | Có ≥ 1 ý thumbnail qua K-R6 | phác thảo |
| G0-9 | Không cần vẽ biên giới hiện đại tranh chấp | danh sách lớp bản đồ |
| G0-10 | Hồ sơ pháp lý sơ bộ các quốc gia liên quan (ghi "chưa tư vấn luật") | bảng §3.2 |
| G0-11 | Mẫu bình luận đối thủ đã đếm theo A–F; xác định loại trội | `binh-luan-dem.json` |
| G0-12 | Đề tài không bị chủ dự án đưa vào danh sách bỏ | AUTHORSHIP |

### 5.2 G1-R — mục rủi ro trình chủ dự án ở G1 (chủ dự án duyệt từng mục)
1. Kết quả G0 (12 mục) kèm ngày tra (c).
2. Bảng nguồn theo truyền thống. **Mọi claim nhạy cảm có ≥ 1 nguồn mỗi phía** (đánh dấu `nhay_cam: true` trong `claims.json`).
3. Bảng tên gọi (địa danh kép, tên phe trung tính).
4. Danh sách câu chữ cấm/khuyên của tập (nạp vào K-R1).
5. Danh sách "không lên hình" của tập (nạp vào K-R2, K-R5).
6. Kết quả chấm mù 3 góc (vai, câu hỏi, điểm, cờ).
7. 3 phương án thumbnail đã qua K-R6.
8. Kế hoạch bình luận: từ chặn, bình luận ghim, lịch duyệt 48 h.
9. Hồ sơ pháp lý (chưa tư vấn luật) + quyết định có chặn khu vực nào không (mặc định: không chặn).
10. Ngưỡng dừng sau đăng (§5.4) và người chịu trách nhiệm theo dõi.
11. Dòng AUTHORSHIP: quyết định sáng tạo và rủi ro của chủ dự án.

### 5.3 Luật K đề xuất (K viết, khoá SHA; phiên này không sửa `checks/`)
| Mã | Luật | Đo bằng | Ngưỡng |
|---|---|---|---|
| **K-R1** Từ cấm | Lời (`.en.srt`), chữ trên hình (log chữ), tiêu đề, mô tả, thẻ không chứa từ trong `tu-cam-chung.txt` + `tu-cam-<tap>.txt` (regex, không phân biệt hoa thường, cả dạng số nhiều) | regex | **0 lần** |
| **K-R2** Biểu tượng trong khung | Mọi tài sản có thẻ `bieu_tuong ∈ {khong, co_lich_su, ton_giao, cuc_doan}`. `cuc_doan`: 0 khung. `ton_giao` (biểu tượng đối đầu): 0 khung. `co_lich_su`: ≤ 2 % diện tích khung, ≤ 3 s mỗi lần, ≤ 3 lần/tập | manifest tài sản + mặt nạ theo id tài sản (`hero_pct` mở rộng) | như trên |
| **K-R3** Biên giới hiện đại | Mọi lớp bản đồ có `loai ∈ {bien_gioi_lich_su(nam, nguon), bien_gioi_hien_dai}`. Lớp `bien_gioi_hien_dai` không được giao với vùng tranh chấp (Natural Earth "breakaway & disputed areas" 10m) | manifest lớp + phép giao hình học | **0 giao** |
| **K-R4** Thương vong | Mọi số đi kèm từ chết/thương vong trong lời phải nối tới claim có **khoảng** hoặc ≥ 2 nguồn khác truyền thống | regex số + `claims.json` | 100 % số có liên kết |
| **K-R5** Hình bạo lực | Tài sản có thẻ `nguoi_bi_thuong` / `thi_the` / `vu_khi_chia_nguoi`: 0 khung (đúng NC-LS §7.5) | manifest + mặt nạ | **0** |
| **K-R6** Thumbnail | Không thẻ cờ, `ton_giao`, `cuc_doan`, vũ khí chĩa người, lửa có người; chữ qua K-R1; mọi số có trong claims | manifest thumbnail | **0 vi phạm** |
| **K-R7** Nhịp | Cửa sổ 4 tập liền ≤ 1 ĐỎ-K; tập liền trước/sau ≠ VÀNG; không T3–T5 | `HANG-DOI.md` (cột mức) | đúng |
| **K-R8** Chấm mù 3 góc | Có `cham-mu-nhay-cam.json`: 3 vai, mỗi vai 0 cờ, điểm ≥ 4/5 | tệp | đủ |
| **K-R9** Mô tả + bình luận ghim | Mô tả có khối nguồn ≥ 2 truyền thống + "as of"; có tệp bình luận ghim; danh sách từ chặn đã nạp (chủ dự án xác nhận) | regex mô tả + checklist | đúng |

### 5.4 Chỉ số theo dõi sau đăng và ngưỡng dừng (7 ngày và 28 ngày)
| Chỉ số | Nguồn | Ngưỡng đề xuất **(ước — chưa có số kênh)** | Vượt thì |
|---|---|---|---|
| Tỷ lệ bình luận bị giữ + bị xoá / tổng bình luận | YouTube Studio | ≤ 10 % (7 ngày) | 10–20 %: tập ĐỎ-K kế phải siết từ chặn. > 20 %: **dừng nhịp ĐỎ-K**, chủ dự án xem lại |
| Bình luận A–F trong 100 bình luận đầu (đếm tay như phiên này) | commentThreads | ≤ mẫu đối thủ cùng đề tài (Dresden: B ≤ 8/200) | cao hơn đối thủ → cách kể đang kích động → xem lại câu chữ |
| Cảnh cáo / gậy Nguyên tắc cộng đồng, gỡ video, giới hạn độ tuổi | Studio | **0** | 1 → dừng nhịp ĐỎ-K ngay |
| Biểu tượng kiếm tiền vàng (quảng cáo hạn chế) | Studio | 0 sau duyệt lại | vàng → yêu cầu duyệt thủ công. Giữ vàng → tập ĐỎ-K kế không mở |
| Doanh thu/nghìn lượt xem (RPM) so với trung vị tập XANH | Studio | ≥ 70 % | < 70 % → cân lại lợi ích ĐỎ-K |
| CTR và thời gian xem trung bình so với trung vị tập XANH | Studio | ≥ 1,0× (lý do mở ĐỎ-K là cầu lớn hơn) | < 1,0× trên 2 tập ĐỎ-K → bỏ luồng ĐỎ-K |
| Phản ánh bên ngoài (báo chí, khiếu nại gửi kênh) | email kênh / tìm tin | 0 phản ánh có căn cứ | 1 → chủ dự án quyết đính chính / gỡ |
| **Điều kiện mở Berlin (T12)** | tổng hợp | Dresden qua **mọi** ngưỡng trên ở 28 ngày | — |

---

## 6. Xếp hạng cuối và vị trí trong hàng đợi

### 6.1 Thứ tự mức (đã kiểm trên nhánh tiền kỳ)
| Tập | Đề tài | Mức |
|---|---|---|
| T3 | Gibraltar | VÀNG |
| T4 | Las Vegas / Colorado | XANH (đề xuất) |
| T5 | Zürich | XANH |
| T6 | Detroit | VÀNG |
| **T7** | XANH bắt buộc (vì T6 VÀNG và T8 ĐỎ-K); gợi ý từ hàng đợi NC-LS: Boston 1775–76 / Vicksburg / Rotterdam / London 1666 | XANH |
| **T8** | **Dresden 1945** | **ĐỎ-K** |
| T9 | XANH bắt buộc | XANH |
| T10–T11 | tự do (không VÀNG ở T11 nếu T12 là ĐỎ-K) | — |
| **T12** | **Berlin 1945 (có điều kiện)** hoặc XANH | ĐỎ-K / XANH |

### 6.2 Quyết định từng đề tài
| Đề tài | Quyết định | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|---|
| Dresden 1945 | **Vào hàng đợi T8** | khớp lời hứa L1; 0/5 đối thủ có nguồn; số thương vong có uỷ ban chốt | điểm đúng ngưỡng (20); cầu 4 | 1 tiền kỳ rủi ro + 1 tiền kỳ số hoá phố cổ (ghost) | cực hữu, §130 → §4.1 |
| Berlin 1945 | **Có điều kiện T12** | cầu lớn nhất nhóm đạt; dữ liệu tốt | KT = 3; gần (c) | chờ số Dresden | biểu tượng, luật Nga, meme |
| Warsaw 1944 | **Để sau** (đo lại cầu bằng truy vấn góc nơi chốn sau T8) | KT 5; dựng lại theo tranh Bellotto | cầu 3 | 0 | Gaza/NATO trong bình luận, luật IPN |
| Hiroshima 1945 | **Để sau** | cầu rất lớn | KT 2 | 0 | footage, ad |
| Constantinople 1453 | **Để sau** | cầu lớn | 19 điểm, KT 2, đã có AI | 0 | Hy–Thổ |
| Tenochtitlan 1521 | **Để sau** | góc hồ → lún | cầu 3 | 0 | khung "man rợ" |
| Vienna 1683, Malta 1565 | **Giữ luồng VÀNG NC-LS** | đã có trong hàng đợi | KT thấp | không tốn suất ĐỎ-K | khung tôn giáo → luật câu chữ §4.3 |
| Nanjing 1937 | **Bỏ** | — | không kiểm soát được (§4.4) | — | — |
| Stalingrad · Derry · Jerusalem 1099 · Jerusalem 1187 | **Bỏ (trượt (c))** | — | — | — | — |

---

## 7. Hạn chế
- Thước /25 do phiên tự chấm. Dresden và Berlin nằm ở ngưỡng hoặc sát ngưỡng, nên chỉ cần lệch 1 điểm là kết luận đảo.
- Search `relevance` thay đổi theo ngày: Vienna và Malta lệch so với NC-LS (§2.1). Chỉ video dài ≥ 20 nghìn và Short ≥ 100 nghìn được duyệt tay, nên cột "Dài ≥ 8'" có thể còn video lạc đề nhỏ.
- Mẫu bình luận: 1–2 video/đề tài, chỉ bình luận cấp 1, sắp theo `relevance`. Đếm tay bởi một người chấm (phiên), không có người chấm thứ hai.
- Pháp lý: tổng hợp từ tìm kiếm công khai (Wikipedia, báo, Verfassungsblog, PONARS…). Nhiều điểm **nguồn mâu thuẫn hoặc chưa đọc văn bản gốc** (Ba Lan 55a sau 06/2018; Nga 2022; quy định Nam Kinh). **Chưa tư vấn luật.**
- Trạng thái chiến sự 10/2026 chưa xác nhận được qua web.
- Các mốc lịch sử, con số và tên sách ở §3–§4 là **kiến thức của phiên, chưa qua quy trình claims**. Đây là danh sách để phiên tiền kỳ tìm và đọc, chưa phải nguồn đã kiểm.
- Giấy phép dữ liệu và hình của mọi đề tài **chưa tải, chưa đọc từng trang**.

---

## 8. Dữ liệu (repo, ≤ 1 MB)
- `reports/nc-lich-su-2/de-tai-cau.json` — cầu 11 đề tài + 2 lượt tìm bổ sung; top 5 chỉ có tên kênh/lượt/phút/ngày (không tiêu đề); khung tiêu đề dạng số đếm; danh sách sát ngưỡng.
- `reports/nc-lich-su-2/binh-luan-dem.json` — số đếm tay A–F + regex thô, 21 video, 2 075 bình luận (không văn bản).
- `reports/nc-lich-su-2/cham-diem.json` — /25, (a)(b)(c), đề xuất; lý do loại theo (c).
- `reports/nc-lich-su-2/cost.json` — chi phí.

## 9. Chi phí thật và dòng đề xuất cho tệp dùng chung
| Hạng mục | Thực tế | Trần |
|---|---|---|
| YouTube Data API | **1 434 đơn vị**. search.list 14 × 100 = 1 400: 11 đề tài + 2 tìm bổ sung + **1 lượt thử kết nối đầu phiên (lãng phí 100 đv, ghi để minh bạch)**. videos.list 13. commentThreads.list 21 | 2 500 |
| Claude API | **$0**: không gọi; không có `cost.jsonl` | $1 |
| ElevenLabs | **0** ký tự | 0 |
| Giờ máy | **≈ 0,1 h** (script Python) | 1 h |
| WebSearch / curl trang chính sách | 7 lượt / 8 trang | — |

**Dòng đề xuất cho `COST-LEDGER.csv`** (P chép; ngoài vùng của phiên này): `NC-LS2-01, 2026-10-17, nc-lich-su-2, nghiên cứu, claude_api_usd=0, youtube_units=1434, elevenlabs_chars=0, render_h=0.1`.
**RIGHTS / AUTHORSHIP:** không có tài sản mới. Quyết định chọn đề tài ĐỎ-K ghi vào AUTHORSHIP khi chủ dự án duyệt.

**Đề xuất tệp ngoài vùng (P/K làm sau duyệt):**
1. `channel-k2/QUAN-TRI-RUI-RO.md` §1: thêm hàng **ĐỎ-K** (ai quyết: chủ dự án ở G1-R; gồm: khung XX1; điều kiện: G0 + G1-R + K-R1…R9 + §5.4).
2. `channel-k2/HANG-DOI.md`: thêm cột "Mức", ghi T7 XANH, T8 Dresden ĐỎ-K, T12 Berlin (có điều kiện).
3. K: viết K-R1…K-R9; tạo `tu-cam-chung.txt` từ §4.
4. `LUAT-NOI-DUNG-G.md`: chép luật hình NC-LS §7.5 + mục "không lên hình" §4.

## 10. Tệp và preflight
- `reports/NC-LICH-SU-2-BAO-CAO.md` (tệp này) + 4 tệp JSON ở §8.
- **Preflight:** `bash tools/preflight.sh --range origin/main..HEAD` → **PREFLIGHT ĐẠT** (6 tệp của nhánh gốc NC-LS); `--staged` (5 tệp của phiên) → **ĐẠT**; `lock.py --verify` → **KHỚP**. Lần chạy đầu báo TRƯỢT (35 mục chặn, toàn tệp `channel-k2/k2c-t1-06/`) vì ref `origin/main` cục bộ chưa được fetch, nên phạm vi so sánh kéo cả tệp của nhánh khác. Fetch `origin/main` rồi chạy lại thì ĐẠT. Ghi để phiên sau tránh: **fetch `origin/main` trước khi chạy preflight**. Hook pre-commit/pre-push chạy lại khi commit/đẩy.

## 11. Việc chờ chủ dự án
1. **Duyệt R1:** T8 = Dresden 1945 (ĐỎ-K), khung "cháy và dựng lại"; cho mở **tiền kỳ rủi ro** + **tiền kỳ số hoá phố cổ** sau khi T6 qua G1.
2. **Duyệt R2:** Berlin 1945 ở T12 **có điều kiện** (Dresden qua mọi ngưỡng §5.4 ở 28 ngày).
3. **Duyệt danh sách để sau / bỏ** (R3–R7), đặc biệt **bỏ Nanjing** dù cầu lớn.
4. **Duyệt phép thử (c) = c1 VÀ c2** (§1.1) và kết quả loại Stalingrad, Derry, Jerusalem ×2.
5. **Duyệt đổi tên "ĐỎ có kiểm soát" → "ĐỎ-K"** (R8) để không trùng nghĩa với ĐỎ = cấm trong QUAN-TRI-RUI-RO.
6. **Duyệt quy trình §5** (G0, G1-R, K-R1…K-R9, ngưỡng §5.4) và giao K viết luật.
7. **Chấm mù nhạy cảm:** đồng ý 3 vai REVIEWER Opus (≈ $1–3/tập **(ước)**). Quyết định có thêm **1 người đọc thật** từ cộng đồng liên quan cho mỗi tập ĐỎ-K hay không (chi phí, quyền riêng tư).
8. **Pháp lý:** quyết định có xin tư vấn luật Đức (§130/§86a) trước G1 Dresden hay không. Phiên chỉ tổng hợp, **chưa tư vấn luật**.
9. **T7 phải là XANH:** chọn đề tài T7 từ hàng đợi NC-LS (Boston / Vicksburg / Rotterdam / London 1666).
10. **Tự quyết của phiên (không dừng hỏi), cần chủ dự án biết:**
    - (i) Coi Jerusalem 1099 và 1187 là 2 ứng viên, và loại cả hai mà **không đo** để tiết kiệm đơn vị, đúng chữ "loại ngay".
    - (ii) Vẫn đo Stalingrad và Derry dù loại, để chủ dự án có số khi muốn xem lại.
    - (iii) Không xác nhận được trạng thái chiến sự 10/2026 → chọn phương án thận trọng ở c1.
    - (iv) Chấm chặt hơn NC-LS: chưa kiểm giấy phép thì tối đa 4.
    - (v) Thêm 2 lượt tìm bổ sung (200 đv) cho góc "dựng lại", không vào thước.
    - (vi) Không gọi Claude API: đếm bình luận bằng đọc tay + regex, giữ $0.
    - (vii) Không chép tiêu đề/bình luận đối thủ. Trích nguyên văn chỉ áp cho trang chính sách YouTube, như NC-LS và QUAN-TRI-RUI-RO.

---
*Nguồn web đã dùng cho mục pháp lý và (c) (để phiên sau kiểm lại):*
- Ngoại trừ Derry, các trang dưới đây là tổng hợp thứ cấp, chưa đọc văn bản luật gốc. Phần Ba Lan, Trung Quốc và Nam Kinh còn có nguồn mâu thuẫn hoặc chỉ có dự thảo.
- Nga: [Law Against Rehabilitation of Nazism](https://en.wikipedia.org/wiki/Law_Against_Rehabilitation_of_Nazism) · [Verfassungsblog 2023](https://verfassungsblog.de/weaponizing-russias-memory-law/) · [PONARS Eurasia](https://ponarseurasia.org/the-implications-of-russia-s-law-against-the-rehabilitation-of-nazism)
- Đức: [Bundestag/§130(5) — beck-aktuell](https://www.beck-aktuell.de/heute-im-recht/rechtspolitik-gesetzgebung/rechtsausschuss-beschliesst-ergaenzung-des-straftatbestands-der-volksverhetzung-2022-10-19)
- Ba Lan: [Act on the Institute of National Remembrance](https://en.wikipedia.org/wiki/Act_on_the_Institute_of_National_Remembrance) · [gov.pl bản tiếng Anh](https://www.gov.pl/web/sprawiedliwosc/nowelizacja-ustawy-o-ipn-wersja-w-jezyku-angielskim)
- Trung Quốc: [Xinhua 2018](https://www.xinhuanet.com/english/2018-05/01/c_137149474.htm) · [Boston Globe 2021](https://www.bostonglobe.com/2021/11/02/world/china-makes-it-crime-mock-heroes/) · [Global Times, dự thảo Nam Kinh 2018](https://www.pressreader.com/china/global-times/20180829/281586651462857)
- Hy Lạp: [JTA về Luật 4285/2014](https://jta.org/?p=907311)
- Derry: [Cool FM — bom xăng tại Memorial Hall](https://www.hellorayo.co.uk/cool-fm/local/news/petrol-bombs-thrown-at-apprentice-boys-memorial-hall-in-l-derry) · [Irish News](https://irishnews.com/news/northern-ireland/three-children-including-one-aged-10-arrested-in-connection-with-derry-disorder-YBP4IWMI3BG3PN3QTOAZD2DFIU)
