# Kiểm mù W2 vòng 2 — 10 dải khung + 2 đối chứng (30/09/2026)

Nguồn: `design/cong5/layout/out/layout-v18.mp4` (W2 vòng 2, có phụ đề). **Cùng 10 shot như vòng 1** (s37, s37b, s39, s40, s41, s42a, s45 + 3 shot theo hạt giống cũ `a443c83796f0d4e6`: s32, s34, s42b) để so được hai vòng. Cùng công cụ (`kiem_mu.py dai`), cùng 2 dải đối chứng Sprite Fright (không commit), cùng câu hỏi nguyên văn. s42b nay có Ida trong khung → câu hỏi "Những người…".
Mỗi dải một subagent MỚI (general-purpose). Nguyên văn: `NGUYEN-VAN.md`; bảng tên mù `map.tsv`; dải `dai_*.jpg`. Token subagent 44 231–45 623 mỗi dải (12 dải ≈ 537 nghìn).
Cách chấm: AUTHORSHIP "Cổng 6 — diễn hoạt" (29–30/09/2026), **không đổi ngưỡng**.

## 1. Đếm máy (`kiem_mu.py dem`)
| Dải | Từ khoá | Chỉ vào | Cột | Vòng 1 |
|---|---|---|---|---|
| s39 (CU nghiêng, câu cuối L4) | "con rối" | mặt Ida: "chỉ có hàm cử động… lông mày, mắt, má và đầu gần như đứng yên suốt 4 giây… khuôn mặt trông cứng, giống con rối" | HÌNH (mặt) — cũng là diễn | 0 |
| s41 (WS trao đèn) | "đồ chơi" | cả hai nhân vật: "trông như tượng gỗ hay đồ chơi, không có chi tiết mặt" | HÌNH | 0 |
| doichung-332 (Victoria) | "ma-nơ-canh" | bàn tay nhân vật đối chứng (lặp y như vòng 1) | HÌNH | 1 |
| s32, s34 | **0** | — | — | **"mặt nạ" ×2 mỗi dải** |
| 6 dải còn lại + doichung-104 | 0 | — | — | 0 |

## 2. Chấm
| Tiêu chí | Kết quả | |
|---|---|---|
| ≤ 1/10 dải có từ khoá (HÌNH + TƯ THẾ) | **2/10** (s39, s41) | **TRƯỢT** |
| Không lời chê cùng một chỗ lặp ≥ 2 dải (từ khoá) | s39 = mặt Ida cận, cứng khi nói; s41 = hai nhân vật cỡ rộng, không chi tiết mặt → **khác chỗ** | ĐẠT (theo từ khoá). *Ghi chú:* lời "đứng im như tượng" (không thuộc danh sách từ khoá) lặp ở s41, s42a, s34 |
| Dải s37 kể ra cả "cười" lẫn "buồn/tiếc" | Nhịp 1 (s37): "buồn lặng, cam chịu, hơi luyến tiếc… Đến khung 3,0 s, khoé miệng có vẻ hơi nhếch lên, giống **một nụ cười buồn** hoặc tự giễu, **nhưng rất khó chắc chắn**" → có cả hai, **sát biên** (người xem tự nói chưa chắc). Nhịp 2 (s37b): "trìu mến pha chút buồn… khoé miệng hơi nhếch lên thành **một nụ cười nhẹ, buồn mà dịu dàng**" → đủ | **ĐẠT, nhịp 1 sát biên** |
| **Kết luận** | | **TRƯỢT** (2/10 > 1/10) |

**Nhiễu nền đối chứng:** dải Victoria trúng "ma-nơ-canh" lần thứ 2 liên tiếp (cùng câu về bàn tay). Cộng dồn **4/24 = 16,7 %** (vòng 1: 3/22). P không tự đổi ngưỡng.

## 3. So với vòng 1
| Vấn đề vòng 1 | Vòng 2 |
|---|---|
| s32, s34 mặt Ida đọc "mặt nạ" (lặp 2 dải) | **Hết** "mặt nạ". Còn: Ida ở cỡ rộng vẫn bị đọc là **"ông cụ / người đàn ông"** ở 3/4 dải cỡ rộng (s32, s34, s41; s42b đọc đúng "phụ nữ lớn tuổi"); s34 "ông cụ mờ và nhạt… như hồn ma" |
| s37 nhịp 1 thiếu "cười" | **Có** "nụ cười buồn" (sát biên) |
| s39 "miệng hầu như không động" | Miệng động, nhưng **"miệng khi nói méo… hàm dưới như bị rách hoặc biến dạng"** (1,0; 2,5; 3,0 s) và "chỉ có hàm cử động" → **"con rối"** |
| s41 "bất động, như hình nộm" | Vẫn "gần như không có chuyển động… như tượng gỗ hay **đồ chơi**" (WS, nhân vật ~1/6 khung) |
| s42a "đứng im như tượng" | Bà đọc được "dịu dàng… chìa tay"; **Cas "đứng im như tượng"** |
| s45 quay đầu 90° trong 0,5 s | **Vẫn**: "cú quay đầu quá đột ngột… giống bị giật" (1,0 → 1,5 s); tay "hơi giống móng vuốt" |
| s42b Cas dịch chuyển tức thời, trong suốt | Hết "dịch chuyển tức thời"; **còn** "ở 1,0 s gần như thành một bóng đen… ở 1,5 s mũ trắng và bông đỏ như biến mất" (= continuity M5) và vệt tối lan dần trên vòm |
| s40 cổ gập, mũ lơ lửng | Mới: **"bước nhảy đột ngột giữa 1,5 và 2,0 s… nhân vật bị dời sang trái và thấp xuống"**; **"chỗ lẽ ra là khuôn mặt lại là một khối trắng có vân như len… đây là điểm lạ và gây rợn nhất"** (bà quay gáy ra máy lúc L11 tắt) |
| — | Mới s37b: "vệt tối trên môi trên… dễ bị đọc nhầm thành ria"; s37 "có thể phân vân đây là đàn ông" |

## 4. Ghi nhận không có từ khoá (đọc đúng ý)
s37b "hoài niệm và lưu luyến… nụ cười bình thản, chấp nhận"; s39 "buồn và dịu dàng xin điều gì đó cho người khác"; s45 "trầm tư, buồn và hoài niệm"; s40 "lặng lẽ khép lại một ngày… cô đơn"; s42a bà "quan tâm, dịu dàng"; s32 "không khí ấm áp… trò chơi bóng tay trên tường"; s42b "đứa trẻ tò mò pha chút sợ… người phụ nữ lặng lẽ theo dõi".
