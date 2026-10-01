# Animatic v3 · xưởng TODAY — báo cáo (P lưu từ lời trả về của xưởng, 01/10/2026)

- **Nhánh:** cục bộ `ep01-today`, commit cuối `82cdc61`. Bản vá: `reports/m3/m2-2b/ma/ma-today-82cdc61.patch`.
- **Token:** harness **249,3 nghìn** so với hạn 180 nghìn (+38 %). Xưởng tự ước ≈ 240 nghìn. Lý do: rà khung mẫu và hai lần sửa luồng ghi đĩa sau sự cố 12:38.

## Kết quả (P đo lại trên chính clip trung gian H.264 crf 10 yuv444p)
| Đoạn | Khung cần / thật | judder loi / giữ ≥ 1 s | Tương phản thấp nhất (xưởng đo) | Dung lượng |
|---|---|---|---|---|
| 10–13 | 2 250 / 2 250 | 0 / 0 | 5,96:1 | 322 MB |
| 14 | 1 508 / 1 508 | 0 / 0 | 6,18:1 | 164 MB |
| 15 | 523 / 523 | 0 / 0 | 6,66:1 | 53 MB |
| 16 | 1 140 / 1 140 | 0 / 0 | 6,80:1 | 131 MB |
| 17 | 808 / 808 | 0 / 0 | 6,83:1 | 97 MB |
| 18 | 531 / 531 | 0 / 0 | 5,83:1 | 66 MB |

- **Render đồ hoạ:** 0,61–0,86 s/khung trung bình, tối đa 2,83 s. Máy tải ≈ 12–18 trên 4 vCPU.
- **Ghép cảnh G0** (tấm nền br10 + sương + chấm hổ phách): 1,84 s/khung.
- **Trung gian:** ≈ 147 MB/phút.

## Sửa L1–L4 (khối 10–13; mốc giây tính trong khối)
- **L1, quãng 1 (13,4–24,4 s):**
  - bìa báo cáo BLS cắt giấy hiện ở 13,45 s ("Bureau");
  - năm dòng trống hiện ở 15,41 s ("a list");
  - thẻ PROJECTION 2025–35 hiện ở 17,72 s ("projects"). Lát cắt cho thẻ hiện ở 14,7 s, trước lời; đã dời;
  - tiêu đề hiện ở 18,53 s ("shrink fastest"). Lát cắt cho hiện ở 14,2 s, trước lời; đã dời;
  - dải 2025 → 2035 chạy từ 20,21 đến 21,72 s.
- **L1, quãng 2 (45,65–58,62 s):**
  - dải 2023 → 2033 hiện ở 49,10 s;
  - thẻ trích MLR chữ lớn hiện từng cụm đúng lúc lời đọc, từ 51,97 đến 57,33 s;
  - thẻ thu về thành dòng trích nhỏ lúc 58,2–58,8 s.
- **Rà thêm:** câu "one task, repeated…" (41,67–44,98 s) trước đây có chỗ hở; đã thêm vòng lặp và bánh răng.
- **L2:**
  - 1950 hiện cả 97k (vòng rỗng, "1950 classification") và 94k (chấm đặc);
  - đoạn A 94k → 77k ("1960 classification");
  - ngắt ở 1960;
  - đoạn B 77k → 37k ("1970 classification").
  - Đoạn 14 dùng cùng gốc.
- **L3:** thẻ end / change / new nằm ở dải trống riêng, có mũi tên ngắn, không đè ô thu nhỏ hay mép biểu đồ.
- **L4:** vạch ngăn nét đứt giữa hai đợt; mỗi đợt có nhãn riêng; hai dòng nguồn có tiền tố "2023–33:" và "2025–35:".

## Chữ trên hình mới (chờ chủ dự án duyệt)
- **14:**
  - "history" / "forecast";
  - "94k → 77k", "77k → 37k", "1960/1970 classification";
  - "(persons)" / "(jobs)" trong dòng nguồn;
  - "writing / answering / checking / coding", thẻ "AI", "call centres / insurance offices / law firms".
- **15:**
  - "U.S. Bureau of Labor Statistics";
  - "PROJECTION 2025–35 · BLS · jobs";
  - "— U.S. BLS, Employment Projections 2025–35";
  - "Office & administrative support", "All U.S. jobs".
- **16:**
  - "about 270 occupations · U.S. census 1950–2010 · Bessen";
  - "Jobs that change";
  - "PROJECTION 2023–33 · BLS · jobs";
  - "all occupations / +4.0%".
- **17:**
  - "Stanford Digital Economy Lab · Aug 2026";
  - "employment index · expected = 100";
  - "about 19% below", "mostly fewer hires", "more experienced workers: no such gap".
- **18:** "Bars: U.S. BLS projections 2025–35 and 2023–33 (as in sections 11–13)".
- **10–13:**
  - chữ trên bìa BLS;
  - "2025"/"2035", "2023"/"2033";
  - "— U.S. BLS, Monthly Labor Review, Feb 2025";
  - "97k", "94k", nhãn phân loại;
  - chú thích G1 nối dài.

## Quyết định sáng tạo chờ chủ dự án
1. Đoạn 14: cột Telephone operators −28 % hiện ở 20,58 s, như phần phụ của nhóm dự báo. Lời dẫn đoạn 14 không nhắc nghề này.
2. Đoạn 16: bàn tay cách điệu gạch sửa dòng 5 của tờ văn bản. Ô thang máy trong lưới 270 để trống, giống đoạn 08.
3. Đoạn 18 thêm ba chi tiết:
   - cột đèn thứ tư để trống ("nobody has a name for yet");
   - trường chấm sáng, có một chấm được khoanh rồi tan;
   - chiếc thang và ô danh sách trống.
4. Đoạn 17: thanh "expected" vẽ viền nét đứt, nền nhạt; thanh "actual" đặc. "actual" hiện trước "expected", đúng theo thứ tự lời.
5. Đoạn 15: hai cột dự báo hai màu, cùng có gạch chéo và nhãn chữ nên vẫn an toàn mù màu.

## Đĩa
- Hai render FFV1 đầu hỏng vì đĩa đầy lúc 12:38. Sau đó xưởng render FFV1 tạm vào /dev/shm, chuyển sang H.264 crf 10 rồi xoá FFV1.
- Đĩa trống thấp nhất trong gói: 9,2 GB. Chưa lúc nào dưới 6 GB.
- P đã dừng 2 tiến trình render treo từ lúc đĩa đầy (đoạn 14 thử, đoạn 15; chạy 1 giờ 25 phút, không còn ghi tệp), gỡ worktree, xoá tấm nền br10 (0,6 GB).

## SFX
Cue ở `sfx/{10-13,14,15,16,17,18}.json`. Chỉ dùng lại M2-SFX-1/2/3; không có SFX mới.
