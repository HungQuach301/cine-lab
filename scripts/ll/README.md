# Nhà máy Last Lamplighters (Mốc B)

Mỗi tập là **một tệp đặc tả** `episode.yaml`. Một lệnh dựng, một lệnh kiểm:

```bash
bash scripts/ll/build.sh reports/m3/ep02/episode.yaml          # prep → render → mix → ghep → shorts
bash scripts/ll/qc.sh    reports/m3/ep02/episode.yaml          # bảng ĐẠT/TRƯỢT → <out>/qc.md
/opt/cine/bin/python scripts/ll/ll.py check <episode.yaml>     # chỉ kiểm đặc tả (nguồn, số, mốc), không gọi mạng
```

Bước lẻ: `bash scripts/ll/build.sh <yaml> render` (chỉ đoạn có đặc tả đổi được render lại), `ONLY="03 05"`, `J=3` (số đoạn song song), `V=v2`.
Xem nhanh khung: `node scripts/ll/render.js --tl <out>/timeline.json --seg 03 --out x.mkv --only 0,120,240 --jpgdir <thư mục>`.
Ví dụ dùng mọi mẫu, không lời: `scripts/ll/examples/demo.yaml`.

## Tệp
| Tệp | Việc |
|---|---|
| `ll.py` | kiểm đặc tả; thu lời Bill qua ElevenLabs (cache theo băm văn bản); giải mốc `@từ`; ghi `timeline.json`, phụ đề `.srt`, cue SFX tự sinh |
| `render.js` | Chromium + canvas2D, 24 fps tất định → trung gian H.264 crf 10 yuv444p + `.log.json` (hoạt động, máy, chữ, tương phản đo trên điểm ảnh) |
| `mix.py` | lời −17 LUFS, nhạc hạ 12 dB khi có lời, SFX; master −14 LUFS / TP ≤ −1 dBTP (tập hoặc `--short`) |
| `build.sh` | một lệnh; ghép master crf 16 + 3 phần 720p ≤ 90 MB cắt ở ranh giới đoạn gần 1/3, 2/3; Shorts 1080×1920 |
| `qc.sh`, `qc.py` | 11 mục kiểm (đầu `qc.py`) |
| `lib/core.js` | giấy B3, ánh rọi, bụi, chữ (cỡ tối thiểu theo trạng thái), thẻ, nhãn ACTUAL/PROJECTION, biểu tượng, bóng người |
| `lib/charts.js` | `bars`, `line`, `compare`, `quote`, `bignum`, `text` |
| `lib/map.js` | `map`: London, New York (hoặc thành phố tự khai); phố không qua nước, chỉ cầu có năm ≤ năm bản đồ |
| `lib/scenes.js` | `street` (phố đèn + người thắp đèn), `office`, `rows` (tổng đài / phòng đánh máy), `endcard` |
| `lib/shot.js` | ghép shot trong đoạn; chuyển `slide` / `flip` (giấy) / `fade` / `cut`; dòng hook cho Shorts |

## Đặc tả (tóm tắt)
```yaml
id: ll-ep02
out: /var/tmp/cine-out/ll-ep02            # ngoài git
voice: {id: pqHfZKP75CvOlQylNhV4, model: eleven_multilingual_v2}
music: [{file: ..., from: "00"}, {file: ..., from: "13", xfade: 3}]
sources:  {FG: {short: "...", url: "...", read: fulltext, pages: "...", accessed: 2026-10-04}}
numbers:  {op1930: {v: 182040, text: "182,040", kind: actual, unit: people, src: FG, say: "one hundred eighty-two thousand"}}
segments:
  - id: "03"
    part: HISTORY                          # STORY | HISTORY | TODAY → tỷ lệ tự tính
    vo: "…"                                # lời Bill; thời lượng đoạn = vo_offset + lời + tail (hoặc min_dur / dur)
    shots:
      - {tpl: line, at: 0, p: {...}}
      - {tpl: bars, at: "@peak-0.3", in: slide, p: {bars: [{label: "1930", num: op1930, at: "@1930"}]}}
shorts:
  - {id: S1, hook: "…", vo: "…", shots: [...]}   # 0,6 s đầu + thẻ kết 1,5 s tự thêm
```
- Mốc thời gian: số giây cục bộ của đoạn, hoặc `"@từ"`, `"@từ#2"` (lần thứ 2), `"@từ+0.4"`. Hình không đi trước lời: neo hình vào từ.
- `num:` lấy giá trị, chữ, loại (actual/projection) và nguồn; dòng nguồn tự sinh. `echo: true` khi nhắc lại số không có trong lời đoạn.
- Luật chặn trước render: nguồn không Wikipedia, đọc toàn văn; số dự báo có `period`; `compare` cùng đơn vị; `say` có trong lời.

## Việc tồn tập 1 đã sửa trong mẫu
- Cỡ chữ tối thiểu ở mọi trạng thái: `text()` đọc ma trận biến đổi, tự nâng cỡ khi tấm giấy thu nhỏ; qc đo lại trên khung.
- Phố/sông đúng lịch sử: mạng phố không vượt nước; chỉ vẽ cầu có năm xây ≤ năm bản đồ (London: London Bridge 1209, Westminster 1750, Blackfriars 1769, Battersea 1771, Vauxhall 1816, Waterloo 1817, Southwark 1819, Tower 1894).
- Shorts: cùng mẫu chạy khổ 9:16 (chữ ≥ 42 px); SFX tự sinh ở mỗi chuyển thẻ; qc Q11 bắt chữ đứng > 3 s.

## Bổ sung khi dựng tập 2 (05/10/2026)
- `beats: [{s, at}]` trên mọi thẻ có tựa (và `text`, `quote`): dòng phụ đề đổi theo lời, neo vào từ. Dùng để lấp khung trống bằng chữ gắn đúng lời, không phải phần tử trang trí.
- `rv()` = nội dung (đánh dấu khung "có dữ liệu"); `rvH()` = khung sườn (tựa, trục, nguồn, biểu tượng). qc Q11 bản dài đo khung trống theo `fill` trong log render; Shorts đo chữ đứng theo `act`.
- `bignum` lấy loại số (ACTUAL/PROJECTION) từ `nums` khi không khai `kind`.
- `build.sh` dừng hẳn nếu một đoạn render lỗi (không ghép trên trung gian cũ).
- Bẫy mốc: `"@many"` khớp lần xuất hiện ĐẦU TIÊN của từ (kể cả "Many" ở câu trước); dùng `#2` hoặc từ khác.

## Bổ sung sau G2 tập 2 (05/10/2026)
- `bignum` với **khoảng số** (`range: true`, `value: [a, b]`, hoặc `text` dạng "50–80…"): không đếm qua số trung gian, hiện thẳng chữ (hoà vào 0,5 s).
- `thumb.py`: thumbnail 1280×720 từ một khung nền + các dòng chữ; tự thu cỡ để mọi hộp chữ nằm trong **lề an toàn 5 %** mỗi cạnh; ghi `<ảnh>.boxes.json`. Ví dụ dùng: `reports/m3/ep02/phat-hanh/make_thumb.py`.
- qc **Q12**: mọi thumbnail (`thumbs:` trong đặc tả, hoặc `phat-hanh/*thumb*.jpg` cạnh đặc tả) phải 1280×720 và không có hộp chữ chạm/vượt lề 5 %.

## Bổ sung lô tập 3–5 (05/10/2026)
- `ll.py est <yaml>`: ước **trước khi thu lời** (không gọi mạng): thời lượng từng đoạn và tỷ lệ STORY/HISTORY/TODAY theo **tốc độ đọc thật của Bill** (`BILL_WPS` = 2,214 từ/s, đo 1 062 từ / 479,6 s trên 15 đoạn tập 2; thử lại trên tập 2: ước 9:03,2, thật 9:01,4). Giải thử mọi mốc `@từ` (bắt lỗi mốc trước khi tốn ký tự ElevenLabs).
- Cùng lệnh báo **khung đồ hoạ có thể đứng trống > 3 s**: shot `bars/line/compare/bignum/text/quote` mà nội dung gắn lời đầu tiên (`at`, `beats`, `noteAt`…) đến sau đầu shot hơn 2,5 s (ngưỡng 3 s trừ sai số ước 0,5 s). qc Q11 vẫn là phép đo thật sau render.
- Hai bài học khác của tập 2 đã có sẵn trong mẫu từ G3 tập 2: `bignum` khoảng số hiện thẳng; `thumb.py` + qc Q12 lề an toàn 5 %.
