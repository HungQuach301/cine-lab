# TỪ ĐIỂN PHÁT ÂM TTS — số, năm, tên riêng, viết tắt

> Phiên Âm thanh soạn 15/10/2026 (Mốc C). Tệp máy đọc: `scripts/audio/phat-am.yaml`. Công cụ: `scripts/audio/phat_am.py`. Phép đo: `scripts/audio/asr_phat_am.py` + `scripts/audio/cau-kho.yaml`. Số đo đầy đủ: `reports/AM-THANH-BAO-CAO.md` §5.

## 1. Dùng thế nào
| Việc | Lệnh |
|---|---|
| Xem một câu sẽ gửi TTS ra sao | `phat_am.py apply "Over 2,710 Liberty ships were built between 1941 and 1945."` |
| Xem mọi chỗ lời một tập sẽ đổi + mốc `@từ` sẽ gãy | `phat_am.py diff <episode.yaml>` |
| Chặn lời còn chữ số / viết tắt lạ | `phat_am.py check <episode.yaml>` (mã thoát 1 khi còn) |

**Áp ở đâu:** áp khi **khoá lời** (biên kịch dán bản đã áp vào `vo:` của đặc tả), không áp ngầm trong `ll.tts`. Lý do: chữ gửi TTS chính là chữ của alignment → phụ đề `.srt` và mốc `@từ` lấy theo đó; đổi ngầm sẽ làm gãy mốc `@1943` và làm phụ đề lệch tiếng. `diff` liệt kê các mốc phải sửa trước khi thu.

## 2. Luật (theo thứ tự áp)
1. **Tên riêng (alias):** chỉ thêm khi **đo thấy đọc sai** (ASR hoặc tai người), ghi số đo và nguồn cách đọc. Hiện **rỗng** — xem §3.
2. **Viết tắt:** đánh vần (`USTR` → `U.S.T.R.`) hoặc đọc như từ (`NATO`). Danh sách trong YAML là **đề xuất chưa đo**; tập đầu tiên dùng phải kiểm ASR.
3. **Tiền:** `$5 billion` → `five billion dollars`; `$100 million` → `one hundred million dollars`.
4. **Phần trăm:** `5%` → `five percent`.
5. **Số + đơn vị nối gạch:** `500-won` → `five-hundred-won`.
6. **Thập niên / năm:** `1970s` → `nineteen seventies`; `1943` → `nineteen forty-three`; `2005` → `two thousand five`; `2026` → `twenty twenty-six`; `1905` → `nineteen oh-five`. Số 4 chữ số đứng ngay trước danh từ đếm (`ships`, `people`, `homes`…) **không** coi là năm.
7. **Ngày:** `June 12` → `June twelfth`.
8. **Số thứ tự:** `21st` → `twenty-first`.
9. **Số còn lại:** `2,710` → `two thousand seven hundred ten`; `4.5` → `four point five` (kiểu Mỹ, không "and").

## 3. Kết quả đo 15/10 (giọng Eric, `eleven_multilingual_v2`, 20 câu khó T1/T2, 2 cách nghe ASR)
| | Trước (nguyên văn) | Sau (đã áp từ điển) |
|---|---|---|
| Số (theo giá trị) nghe đúng, cộng cả 2 cách nghe | 148/152 (97,4 %) | **152/152 (100 %)** |
| Tên riêng nghe ra đúng chữ | 103/104 | 103/104 |
| Lượt đọc đúng trọn câu (19 câu chấm máy; câu từ điển đổi chữ thu 2 lượt) | 32/35 | **34/35** |
Chi tiết: `reports/am-thanh/asr-phat-am.json`; báo cáo `reports/AM-THANH-BAO-CAO.md` §5.
- **Số có dấu phẩy nghìn là chỗ sai thật:** "New York City's **4,440**" — bản gốc ASR nghe "4,040" ở **2/2 lượt, cả hai cách nghe**; bản đã áp nghe đúng 2/2. Khớp bài học cũ (RUNBOOK §5, commit `96da659`).
- **Năm viết bằng chữ số** (1943, 1972, 2024…) và "2,710", "747", "702,000" được Eric đọc đúng cả khi chưa áp; từ điển vẫn đổi sang chữ để tất định (không phụ thuộc lượt thu).
- **Tên Hàn/Hy Lạp:** để nguyên chữ thì ASR nghe ra đúng (Chung Ju-yung, Park Chung Hee, Ulsan, Hanwha, Korea JoongAng Daily, George Livanos). Thử respell ở lượt đầu **làm xấu đi**: "Lee-vah-nos" → ASR "Liva Knows"; "Hahn-hwah" → "Hanhwa"; "Moon-sub" → "Moon-Sub" ⇒ bỏ mọi alias tên. Lỗi tên còn lại duy nhất: "Munseob" — small.en (tham lam) nghe "Mun-Sae-Aub"/"Moon Se-ab" ở 1/2 lượt mỗi bản (medium.en đúng) → **tai chủ dự án** xác nhận cách đọc. Đọc **đúng giọng bản ngữ** ASR không đo được.
- **Giới hạn của máy chấm:** "five hundred **won**" ↔ "501" (ASR không tách won/one) — câu này chấm bằng tai; "fifteen and a half" ASR viết "15 and a half" — bộ chấm quy về 15,5; "Pew" ↔ "Pugh" (đồng âm, medium.en viết "Pugh" ở 2/2 lượt bản sau) — bộ chấm chấp nhận đồng âm khai trong `cau-kho.yaml`.
- ElevenLabs **không tất định**: cùng chữ, hai lượt có thể khác nhau ở tên lạ. Câu nào từ điển đổi chữ được thu **2 lượt** mỗi bản.

## 4. Thêm mục mới
1. Thu câu chứa từ khó (≤ 200 ký tự), chạy `asr_phat_am.py` với câu đó trong một tệp `--cau` riêng.
2. ASR nghe sai ở ≥ 1/2 lượt với **cả hai** cách nghe → thử alias; giữ alias chỉ khi lượt sau đúng 2/2 và **không** làm tên lệch chính tả trên phụ đề (phụ đề hiện tên viết đúng — sửa tay `.srt` nếu alias đổi chữ).
3. Ghi dòng vào `phat-am.yaml` kèm ngày + số đo; ghi ký tự ElevenLabs vào `COST-LEDGER.csv`.
