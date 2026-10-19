# CHỌN GIỌNG — series "Contested Places" (K2C, từ T3 Gibraltar)

Chủ dự án chọn G1 (A2, Voice Design) qua nghe mù 18/10/2026 23:31; chọn lại G1 (M2) qua nghe mù CASTING-MỸ 19/10/2026 06:07

| Trường | Giá trị |
|---|---|
| Mã | G1 (gói CASTING-GIỌNG) = A2 biến thể 3 (`reports/casting-giong/thiet-ke.json`) = M2 = DC-G1 (gói CASTING-MỸ) |
| `voice_id` | `VDLncRBHDjLHBqLhQ1Qt` |
| `generated_voice_id` | `VDLncRBHDjLHBqLhQ1Qt` (biến thể 3 của lệnh Voice Design) |
| Model tạo giọng | `eleven_multilingual_ttv_v2` (Voice Design) |
| Mô tả thiết kế (nguyên văn `thiet-ke.json`) | "An older male narrator with a low register, in the style of a BBC historical documentary. Calm authority, precise diction, grave and steady, neutral southern English accent. Clean studio recording." |
| Chữ thử lúc thiết kế | "The thirteenth of September seventeen eighty-two. That morning, the batteries moved into position under the garrison's fire. At ten twenty-five, by the Spanish account, the attackers' guns, some four hundred, opened fire together. By the next afternoon, all ten batteries were lost. Over two thousand attackers were lost, by a British estimate that includes prisoners, and by a Spanish one; the British rescued three hundred and fifty-seven." |
| Máy chọn biến thể | từ đúng 0.9855 (thấp nhất 2 cách nghe), F0 trung vị 80.3 Hz |
| Đã LƯU vào tài khoản? | **Có.** `GET /v1/voices/VDLncRBHDjLHBqLhQ1Qt` (19/10/2026, phiên GIỌNG-CHỐT) trả `name` = `CINE-CastingGiong-A2-v3`, `category` = `generated`, `created_at_unix` = 1792338201 (18/10/2026, phiên CASTING-GIỌNG lưu bằng `luu_thiet_ke.py` qua `POST /v1/text-to-voice`), nhãn `project=cine-lab`, `use=casting-giong-contested-places`; có trong `GET /v2/voices?search=CINE` (6 giọng CINE-*). Không phải bản tạo tạm → phiên này không lưu lại, không đổi tên (0 ký tự) |
| Cấu hình đọc khi chọn | `eleven_multilingual_v2`, stability 0,5, similarity 0,75, speed 1,0 |

Ghi chú: mô tả thiết kế nói "neutral southern English accent" (giọng Anh), dù lần chọn lại diễn ra trong gói "giọng Mỹ" — G1 có mặt ở đó với vai đối chứng và thắng 4 giọng Mỹ mới.
Ghi vào `AUTHORSHIP.md` là việc của phiên P (phiên này không sửa ngoài vùng được giao).
