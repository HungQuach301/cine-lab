# BÁO CÁO PHIÊN ÂM THANH — Mốc C (xưởng Hollywood), 15/10/2026

## 0. Khối điều lệ (lệnh giao) + thực tế
```text
ĐIỀU LỆ PHIÊN AM   (tiền tố mới "AM" = Âm thanh — chưa có trong FILE-ZONES §3, đề xuất P thêm)
Loại phiên:        xưởng (luồng âm thanh)
Nhánh:             am-thanh, tạo từ origin/main @ 7255aa4   | thực tế: am-thanh + bản sao claude/gallant-cannon-fg606b (nhánh harness giao), cùng commit
Tệp được sửa:      scripts/audio/ (mới), scripts/k2/ + scripts/ll/ CHỈ phần dựng/ghép âm thanh, docs/AUDIO-*.md, assets/audio/ (tài sản giấy phép rõ)
                   | thực tế: scripts/audio/* (mới), scripts/ll/mix.py (+9 dòng, cờ --stems, không đổi bản mix), scripts/k2/build.sh (MIX=audio, mặc định giữ mix.py),
                   docs/AUDIO-PHAT-AM.md, docs/AUDIO-THUOC-DO.md, assets/audio/ (14 mẫu SFX + giấy phép), reports/AM-THANH-BAO-CAO.md, reports/am-thanh/*.json
Tệp KHÔNG được sửa: checks/, design/, channel-k2/k2c-t2-*/ | thực tế: không đụng; không đọc mã checks/
Tệp dùng chung:    RIGHTS.md (+AM-01…04), COST-LEDGER.csv (+1 dòng AM) — chỉ ghi thêm
Trần chi phí:      Claude API $3 (ghim model) · ElevenLabs ≤ 15 000 ký tự | thực tế: Claude API $0 (không gọi) · ElevenLabs 11 969 ký tự gửi (bộ đếm +5 266)
Preflight:         bắt buộc trước mỗi push | thực tế: ĐẠT, lock.py --verify KHỚP (hook pre-commit + chạy tay trước push)
Merge:             không merge; dừng chờ chủ dự án (merge sau khi T2 qua G2)
Điều kiện dừng thực tế: (1) xong việc và nộp báo cáo
```
Tài liệu đã đọc: `docs/SESSION-CHARTER.md`, `docs/FILE-ZONES.md`, `docs/BIBLE-KENH2.md` (§4 âm thanh), `docs/RUNBOOK-MOI-TRUONG.md`, `reports/m3/BAI-HOC-LL.md`. **Không tìm thấy** `claude/CINE-LAB-KE-HOACH-NANG-CAP.md` trong repo (mọi nhánh đã fetch) — làm theo nội dung lệnh giao. `scripts/env/verify.sh`: 10 PASS, 3 FAIL (three.js, tifffile/pyshp, k2v node_modules — không dùng cho âm thanh, không cài).

## 1. Tóm tắt
| Việc | Kết quả |
|---|---|
| 1. Đo hiện trạng 3 master | Cả 3: **−14,0 LUFS, −1,6 dBTP**, LRA 2,1–2,8 LU, lời trên nhạc p10 17,3–18,9 dB (min 13,8–16,4), 0 lặng bất thường, 0 chạm trần. Đạt Kinh thánh; I nằm **đúng mép −14,0** (§11) |
| 2. Chuỗi hoàn thiện `master.py` | Lời: lọc 70 Hz + khử xì + nén 2,5:1; ducking **thích ứng** (cơ bản −12 dB như cũ, hạ thêm tới khi SMR ≥ 15 dB); fade; loudnorm 2 lượt **tuyến tính**; đỉnh thật kiểm **sau AAC**; báo JSON |
| 3. Nhạc theo chương `music.py` | Khai cue theo chương; giao bài **tâm tại vạch ô nhịp**, phách mạnh bài mới trùng điểm giao; đổi cường độ trong cùng bài; không lặp (Q28). Chỉ dùng nhạc đã có trong RIGHTS (Kevin MacLeod CC BY 4.0) |
| 4. SFX gắn hình `sfx.py` | 4 loại (xu rơi, phiếu rơi, máy lặn/trượt, chuyển bảng màu), 14 mẫu: Kenney **CC0** + whoosh/shimmer **tự tổng hợp**; tự suy biến cố từ cảnh 3D + khai tay theo mốc "@từ" |
| 5. Từ điển phát âm | `phat-am.yaml` + `phat_am.py`; 20 câu khó T1/T2 × 2 cách nghe ASR: **số đúng 148/152 → 152/152**; lượt đúng trọn câu 32/35 → 34/35; respell tên **làm xấu đi** → bỏ, tên để nguyên chữ |
| 6. Mẫu giọng | 3 bản móc T2 (Eric v2 hiện tại · Brian v2 · Eric eleven_v4), cùng −16 LUFS, ngoài git, có SHA. T2 **không đổi giọng** |
| 7. Thước chấm | `docs/AUDIO-THUOC-DO.md`: 13 chỉ số máy (A1–A13) + 2 chỉ báo chưa hiệu chuẩn; 6 mục tai người |
| 8. Áp thử T1 | Chuỗi mới: −14,0 LUFS, −1,5 dBTP sau AAC, SMR p10 **18,6 → 19,6 dB**, min **14,0 → 17,2 dB**; loudnorm tuyến tính; A/B 60 s có hình |

## 2. Số đo hiện trạng (đọc âm master qua LFS như `golden.py`)
Cách lấy: href LFS ký sẵn → `ffmpeg -map 0:a:0 -c:a copy` (chỉ luồng âm; 73 s / 104 s / 136 s cho LL08 / Steel / T1). Lời–nhạc đo trên **stem dựng lại**: prep offline (proxy chặn, như `golden.py`) → `scripts/ll/mix.py --stems`. Kiểm bản dựng lại khớp master: phần dư T1 −38…−43 dB, Steel −28…−42 dB (tương quan chéo 5 s ở 4 điểm) → stem đáng tin. JSON: `reports/am-thanh/hien-trang-*.json`.

| Chỉ số | Steel (k2g-ep01) | T1 (k2c-t1-06) | LL ep08 | Mục tiêu |
|---|---|---|---|---|
| Thời lượng | 1 030,1 s | 941,1 s | 608,0 s | — |
| I (LUFS) | −14,0 | −14,0 | −14,0 | −15 … −14 |
| Đỉnh thật (dBTP, sau AAC) | −1,6 | −1,6 | −1,6 | ≤ −1 |
| LRA (LU) | 2,3 | 2,1 | 2,8 | (báo) |
| Lời trên nhạc — trung vị / p10 / min (dB) | 20,9 / 18,9 / 16,4 | 20,9 / 18,6 / 14,0 | 21,2 / 17,3 / 13,8 | p10 ≥ 15 |
| % cửa sổ 3 s dưới 15 dB | 0,0 | 0,3 | 0,9 | — |
| Tỉ lệ lặng (< −50 LUFS tức thời) | 0,0 % | 0,0 % | 0,15 % | — |
| Lặng bất thường ≥ 1 s giữa phim | 0 | 0 | 0 | 0 |
| Chạm trần (≥ 3 mẫu ≥ 0,999) | 0 | 0 | 0 | 0 |
| Chồng lời | 0 | 0 | 0 | 0 |
| Tỉ lệ thời gian có lời | 86,4 % | 93,2 % | 90,0 % | — |
| Quãng không lời dài nhất | 1,8 s | 1,8 s | 4,2 s | — |

Phát hiện phụ: `mix.py` cũ làm luồng âm trễ **1,0 ms** (48 mẫu — độ nhìn trước của `alimiter` ở 192 kHz); dưới 1 khung (41,7 ms), không ảnh hưởng khớp hình, ghi vào thước A13. Phép "chiếu" lời gốc lên master để ước SMR khi không có stem **không dùng được** (ra ≈ 3 dB, sai) vì lời đã qua nén phi tuyến — đã bỏ khỏi công cụ.

## 3. Công cụ + API (`scripts/audio/`)
| Tệp | Việc |
|---|---|
| `lib.py` | giải mã/ghi PCM; lọc K BS.1770-4 tự tính (lệch ffmpeg ≤ 0,05 LU, đã kiểm); `ebur128`, `loudnorm` đo; gộp khoảng lời |
| `measure.py` | đo một tệp → JSON: I, LRA, TP, lặng, lặng bất thường, chạm trần, chồng lời, quãng không lời, SMR từ stem |
| `master.py` | chuỗi hoàn thiện (§1 việc 2). Tham số: `--smr 15 --duck -12 --I -14 --tp -1 --fade-in --fade-out --aac`. Vòng ≤ 4: hạ trần limiter nếu đỉnh sau AAC vượt; bù tuyến tính nếu I (ebur128) lệch > 0,1 LU (loudnorm đo lệch 0,6 LU trên Short 15 s — đã sửa) |
| `music.py` | nhạc theo chương (API ở §4); `grid` in tempo/ô nhịp (librosa, cache) |
| `sfx.py` | thư viện + biến cố SFX (API ở §4); `lib` dựng lại thư viện |
| `compose.py` | dựng tiếng cả tập/Short từ timeline: lời + `music.py` + SFX timeline + `sfx.py` + `master.py` → `mix.wav` + `mix.json` |
| `phat_am.py` + `phat-am.yaml` | từ điển phát âm (§5) |
| `asr_phat_am.py` + `cau-kho.yaml` | phép thử ASR trước/sau; `rescore` chấm lại không tốn ký tự |
| `mau_giong.py` | mẫu giọng (§6) |
| `test_audio.py` | 4 kiểm nhanh (số→chữ, loudness khớp ffmpeg, chuỗi master trên tín hiệu tổng hợp, gộp khoảng) — **4/4 ĐẠT** |

Nối vào nhà máy: `MIX=audio bash scripts/k2/build.sh <episode.yaml> mix` (và bước `shorts`) gọi `compose.py`; **mặc định vẫn `scripts/ll/mix.py`** nên tập đang dựng (T2) không đổi tiếng. `scripts/ll/mix.py --stems <dir>` ghi stem để đo (không đổi bản mix khi không có cờ).

Ví dụ khai trong đặc tả tập:
```yaml
music:
- {file: assets/k2/music/Half-Mystery.mp3, from: '00', ss: 0, gain_db: -1}
- {file: assets/k2/music/Beauty-Flow.mp3, from: '02', xfade: 3, intensity: mid}      # giao đúng ô nhịp (align: bar mặc định)
- {file: assets/k2/music/Beauty-Flow.mp3, from: '03', continue: true, intensity: low}  # cùng bài, hạ cường độ ở vạch ô nhịp
sfx_events:
- {seg: '03', at: '@ships+0.05', kind: coin_drop, n: 4}
- {seg: '05', at: '@fees', kind: paper_drop}
```

## 4. Nhạc theo chương, SFX gắn hình, giấy phép
**Nhạc.** Tempo lấy từ RIGHTS (`scripts/audio/music-meta.yaml`) làm gợi ý cho bộ dò phách; bộ dò ra Beauty Flow 107,7 (RIGHTS 108), Half Mystery/Tyrant/Sincerely 71,8 (RIGHTS 72) — khớp. Không gợi ý thì Half Mystery bị dò **gấp đôi** (143,6) → luôn dùng gợi ý. "Lightless Dawn" (ambient, RIGHTS không ghi bpm, dò 51,7 — không tin) đặt `align: none` → giao theo giây như mix.py cũ. Vạch ô nhịp = 4 phách, pha chọn theo năng lượng dải trầm — **ước**, tai chủ dự án xác nhận. Trên T1 (6 cue): điểm giao lệch ranh giới chương −0,38 / +1,02 / +0,19 / 0 / 0 s, dài giao 3,34 / 2,23 / 3,34 / 3,0 / 3,0 s (`reports/am-thanh/t1-chuoi-moi.json` → `nhac`). Không thêm nhạc mới: thư viện hiện có đủ cho T1/T2; thêm bài sau phải có dòng RIGHTS + trang giấy phép.

**SFX.** Thư viện `assets/audio/sfx/` (364 KB, `LIBRARY.yaml` có SHA từng mẫu):
| Loại | Mẫu | Nguồn | Giấy phép |
|---|---|---|---|
| `coin_drop` | coin-1…4 | Kenney "Impact Sounds" (impactMetal_light) + "RPG Audio" (handleCoins2) | CC0 1.0 |
| `paper_drop` | paper-1…4 | Kenney "Casino Audio" (card-place) | CC0 1.0 |
| `camera_move` | whoosh-1…3 (0,9 / 1,4 / 2,0 s) | tự tổng hợp: nhiễu hồng qua lọc dải quét 250→2 600→500 Hz | thuộc dự án |
| `palette_shift` | shimmer-1…3 | tự tổng hợp: hợp âm sin 5 bậc + nhiễu khí | thuộc dự án |
License.txt của 3 gói Kenney lưu nguyên ở `assets/audio/licenses/kenney-cc0.txt` kèm SHA-256 zip (029d734a… / 6dbeaf85… / f3625076…). Gói zip gốc ở ngoài git (`/var/tmp/cine-out/am-thanh/dl/`). RIGHTS: **AM-01…AM-04**. Freesound API trả 401 khi không có khoá — không dùng.

Tự suy biến cố (đổi giây-trong-cảnh → giây phim qua shot đang hiện): chồng xu `cols kind:coins` → `coin_drop` rải ≤ 6 tiếng nhanh dần; `sepia|natural: [t0,t1]` → `palette_shift`; mốc máy quay đổi độ cao ≥ 2,5× trong ≤ 3 s (hoặc ≥ 4× trong ≤ 6 s) → `camera_move`. Thử trên cuộn K2V4: 12 biến cố (8 xu, 3 lặn máy, 1 bảng màu); T1: 2 lặn máy (Euclid 112,0 s; Colorado 183,7 s); Steel: 0. Mức: whoosh ≈ 10 LU dưới lời (đo tại 112 s và 184 s), còn bị hạ ½ mức duck khi có lời. **"Phiếu rơi" chỉ khai tay** (không có tham số cảnh nào biểu diễn phiếu rơi).

## 5. Từ điển phát âm + kết quả ASR
Luật và cách dùng: `docs/AUDIO-PHAT-AM.md`. Áp khi **khoá lời** (không áp ngầm trong `ll.tts`, để phụ đề và mốc `@từ` không lệch).

Phép thử: 20 câu nguyên văn (15 từ lời T2 v3.2 @e2a9709, 5 từ T1 script-v2), giọng Eric `eleven_multilingual_v2` (như T1/T2). Mỗi câu thu TRƯỚC (nguyên văn) và SAU (đã áp); câu từ điển đổi chữ (16/19) thu **2 lượt** mỗi bản. Nghe bằng **2 cách**: faster-whisper medium.en beam 5 và small.en beam 1 (BAI-HOC-LL #86). Một lượt ĐÚNG khi mọi số (theo giá trị) và mọi tên (khớp mờ ≥ 0,75) có trong bản nghe **ở cả 2 cách**.

| | Trước | Sau |
|---|---|---|
| Số nghe đúng (×2 cách nghe) | 148/152 = 97,4 % | **152/152 = 100 %** |
| Tên nghe ra đúng chữ | 103/104 | 103/104 |
| Lượt đúng trọn câu | 32/35 | **34/35** |
| Câu đúng mọi lượt (19 câu chấm máy) | 17 | 18 |

- Lỗi thật duy nhất của bản gốc: **"4,440" → "4,040"** ở 2/2 lượt × 2 cách nghe; bản áp từ điển đúng 2/2.
- Respell tên (lượt thử đầu) làm ASR nghe sai: "Liva Knows", "Hanhwa", "Moon-Sub" → **bỏ toàn bộ alias tên**; tên để nguyên chữ nghe ra đúng.
- Còn lại 1 lượt sai ở cả hai bản: "Munseob" với small.en (medium.en đúng) — cần tai chủ dự án.
- 1 câu loại khỏi chấm máy: "500-won" (ASR ra "501" — không tách được won/one), chấm bằng tai. "Pew"↔"Pugh" là đồng âm, bộ chấm chấp nhận.
- Mp3 các lượt (ngoài git): `/var/tmp/cine-out/am-thanh/asr/`; SHA từng tệp trong `reports/am-thanh/asr-phat-am.json`.

## 6. Mẫu giọng (móc T2 v3.2, 79 từ, 478 ký tự; KHÔNG đổi giọng T2)
Tệp ngoài git, cùng chuẩn −16 LUFS (so công bằng), mp3 192 kb/s, `stability 0,5 · similarity 0,75 · speed 1,0`:
| Bản | Cấu hình | Dài | Nhịp | ASR medium.en | SHA-256 |
|---|---|---|---|---|---|
| A | Eric · `eleven_multilingual_v2` (hiện tại) — `/var/tmp/cine-out/am-thanh/mau-giong/A-eric-v2-hien-tai.mp3` | 33,9 s | 140 từ/phút | số đúng, lỗi từ thô 1,3 % | `ff61b903cfa386e1cc011e8a90a89ae3b63e9c4d1b08c8c03c87e4d7a31fc843` |
| B | Brian ("Deep, Resonant and Comforting") · `eleven_multilingual_v2` — `/var/tmp/cine-out/am-thanh/mau-giong/B-brian-v2.mp3` | 30,6 s | 155 từ/phút | số đúng, 1,3 % | `d9d53eea03cb010d075682a2a3dc1141b2ad9c4c12dd91be3e01c57657b13f56` |
| C | Eric · `eleven_v4` — `/var/tmp/cine-out/am-thanh/mau-giong/C-eric-v4.mp3` | 34,3 s | 138 từ/phút | số đúng, 1,3 % | `5b9749a0b7fac71a4467787e93b3c00e7dbd2c7f2800b675bf9e62e4dbcaceab` |
Lý do chọn: B đổi **giọng** giữ model (giọng premade gợi ý cho narration); C giữ **giọng** (liền mạch với T1) đổi **model**. Máy chỉ xác nhận cả 3 đều nghe rõ như nhau — chọn giọng là việc của tai. `eleven_v4`: **chưa kiểm** có thuộc "Beta Services" (giấy phép thương mại) — phải kiểm trước khi dùng cho phim. Container tạm thời: tệp mất khi container bị thu hồi; chạy lại `mau_giong.py /var/tmp/cine-out/am-thanh/hook-t2-v3.2.txt` cần 1 431 ký tự.

## 7. Đề xuất luật cho K (chi tiết `docs/AUDIO-THUOC-DO.md`)
| # | Luật đề xuất | Ngưỡng | Ghi chú |
|---|---|---|---|
| A1 | Loudness tích hợp trên luồng âm master | −15,0 ≤ I ≤ −14,0 LUFS, dung sai đo ±0,2 | 3/3 tập đúng mép −14,0 |
| A2 | Đỉnh thật sau AAC | ≤ −1,0 dBTP | |
| A4 | Lời trên nhạc (stem) | p10 ≥ 15 dB, min ≥ 12 dB | 3/3 đạt; T1 cũ min 14,0, LL08 13,8 |
| A5 | Lặng bất thường | 0 đoạn ≥ 1 s < −50 LUFS giữa phim | |
| A7 | Chạm trần | 0 | |
| A8 | Chồng lời | 0 | |
| A9 | Đọc đúng ASR | 100 % đoạn, **hai** cách nghe | câu "mơ hồ ASR" chấm tai |
| A11 | Giao nhạc | lệch ≤ 1 ô nhịp; không lặp | nhật ký `compose.py` |
| A12 | Loudnorm | `normalization_type = linear` | chặn nén động ẩn |
| A3, A6, A10, A13 | báo, không chặn | | |
JSON cho K đọc: `mix.json` cạnh `mix.wav` (khoá `dau_ra`, `smr`, `dat`, `loudness`, `duck`, `nhac`, `sfx`), hoặc `measure.py --json`.

## 8. Áp thử trên master T1 (bản sao ngoài git)
Dựng lại tiếng T1 từ chất liệu gốc (lời ElevenLabs trong `channel-k2/k2c-t1-06/vo/`, nhạc + SFX theo timeline, prep offline). Hai biến thể để tách tác động:
| Chỉ số | Master gốc (mix.py) | Chỉ thay chuỗi hoàn thiện (stem cũ) | Chuỗi mới đầy đủ (`compose.py`) |
|---|---|---|---|
| I (LUFS) | −14,0 | −14,0 | −14,0 |
| Đỉnh thật sau AAC (dBTP) | −1,6 | −1,5 | −1,5 |
| LRA (LU) | 2,1 | 2,2 | 2,2 |
| SMR trung vị / p10 / min (dB) | 20,9 / 18,6 / 14,0 | 21,6 / 19,6 / 17,8 | 21,6 / 19,6 / 17,2 |
| % cửa sổ dưới 15 dB | 0,3 | 0,0 | 0,0 |
| Lặng bất thường / chạm trần | 0 / 0 | 0 / 0 | 0 / 0 |
| Loudnorm | (một lượt gain + limiter) | tuyến tính | tuyến tính |
| Duck: trung vị / sâu nhất (dB) | −12 cố định | −12,2 / −17,7 | −12,1 / −17,6 (16/29 khoảng hạ thêm) |
| Nhạc | giao 3 s theo giây | như cũ | giao theo ô nhịp (§4) |
| SFX | 31 cue timeline | như cũ | 31 + 2 whoosh tự suy |
Dựng lại 2 lần cho cùng SHA `mix-v2.wav` = `c03ee524…` (tất định). Short S1 (15,3 s): −14,0 LUFS, −2,0 dBTP sau AAC 192k, SMR p10 18,5 dB.

**A/B 60 s** (T1 176–236 s: móc đoạn 02, lặn máy Colorado 183,7 s, giao Beauty Flow → Sincerely 223,0 s), hình 720p giống hệt, tiếng A = mix gốc dựng lại, B = chuỗi mới; loudness đoạn −14,3 / −14,2 LUFS (so công bằng):
| Tệp (ngoài git, `/var/tmp/cine-out/am-thanh/t1-moi/`) | Cỡ | SHA-256 |
|---|---|---|
| `ab-A-cu.mp4` | 11,5 MB | `35b5755e9f7381ba64183851adda87d1c217f79c127a4000a8fee06acec75b0e` |
| `ab-B-moi.mp4` | 11,4 MB | `23f25c82e6dc66c2c3a43e1e6a40913568a750e32815e87c27279592891221ed` |
| `ab-A-cu.m4a` | 1,9 MB | `abe68ae0e7650eb2dcd5575e9a03ba3c49adc8bcdcfddbb463179160637c789c` |
| `ab-B-moi.m4a` | 1,9 MB | `8d8baa9f726990cbbba748ad989d1f100532ffc71cfa48f1cf312fc4a734edf2` |
| `k2c-t1-06-am-thanh-v2.m4a` (cả tập, AAC 256k) | 30,3 MB | `0f7ef697713bf877141d37177ad60aa56a95dd81620a737f346051f6abed1059` |
Master T1 phát hành **không đổi**.

## 9. Chi phí
| Mục | Số |
|---|---|
| Claude API | **$0** (không gọi; không cần `cost.jsonl`) |
| ElevenLabs gửi | **11 969 ký tự** (ASR lượt 1: 63 + 5 239; lượt 2: 5 236; mẫu giọng: 1 431) — trần 15 000 |
| Bộ đếm tài khoản | 100 232 → 105 498 (**+5 266**, ≈ 0,44 ký tự/ký tự gửi, khớp RUNBOOK §5) |
| Giờ máy | ≈ 1,6 giờ (cộng theo nhật ký lệnh: đọc âm LFS 5 phút, dựng stem 3 tập 7,4 phút, đo 3 tập ≈ 6 phút, ASR 2 lượt ≈ 45 phút, dựng T1 chuỗi mới 3 lần + biến thể 3 lần ≈ 35 phút, A/B 3 phút) |
| LFS | đọc luồng âm 3 master (ffmpeg đọc theo dải, không tải cả tệp) + 2 lần 60 s hình T1 (≈ 230 MB) |
| Token phiên | chưa đo (chủ dự án đọc trang Usage) |

## 10. Tệp đã sửa, preflight, ghép thử
- Commit `9843309` (mã + tài sản + tài liệu) và commit báo cáo; nhánh `am-thanh` + `claude/gallant-cannon-fg606b`.
- Preflight: `PREFLIGHT ĐẠT`, `lock.py --verify: KHỚP` (42 tệp ở commit mã; chạy lại trên `origin/main..HEAD` trước push).
- Ghép thử với `origin/main` @7255aa4: **sạch**.
- Ghép thử với `origin/k2c-t2` @efb74c2 (T2 đã sang G1b): **xung đột 2 tệp dùng chung** — `RIGHTS.md` (hai phiên cùng ghi thêm cuối tệp; giải: giữ cả hai khối theo thứ tự thời gian, SESSION-CHARTER §4.4) và `AUTHORSHIP.md` (**có sẵn** giữa main và k2c-t2, phiên này không sửa AUTHORSHIP). Không xung đột mã: T2 không sửa `scripts/ll/mix.py`, `scripts/k2/build.sh`, `scripts/audio/`.

## 11. Chỉ số nằm trong ±5 % quanh ngưỡng
- **I = −14,0 LUFS** ở cả 3 master và mọi bản chuỗi mới — đúng mép trên của −15…−14 (mục tiêu dựng là −14,0, khớp chuẩn chuẩn hoá YouTube).
- **LRA T1 = 2,1 LU** — trong 5 % quanh mức báo đề xuất 2,0 LU (chỉ báo, không chặn).
- Không chỉ số chặn nào khác trong ±5 %: TP −1,5/−1,6 vs −1,0; SMR p10 ≥ 17,3 vs 15; min ≥ 13,8 vs 12.

## 12. Hạn chế, rủi ro
- Vạch ô nhịp là **ước** (librosa không cho phách mạnh); bài ambient không có phách tin được → giao theo giây.
- Whoosh/shimmer tự tổng hợp: an toàn quyền, nhưng gu là việc tai; có thể thay bằng ghi âm CC0 nếu chủ dự án thấy "rẻ".
- Từ điển áp khi khoá lời → phụ đề hiện số bằng chữ ("nineteen forty-three"). Đề xuất cho P: `ll.py` sinh `.srt` từ bản viết gốc (ánh xạ từ) — ngoài vùng tệp của phiên này, chưa làm.
- `master.py` bản đầu dùng 11,6 GB RAM với T1 (15:41) và bị OOM khi chạy song song ASR; đã chuyển float32 + giải phóng mảng, sau đó chạy được cùng lúc ASR (2,4 GB). Tránh chạy cùng dựng hình 3D trên máy 15 GB.
- ASR không đo được đọc đúng âm bản ngữ; ElevenLabs không tất định (2 lượt/câu là ít — đủ để thấy xu hướng, chưa đủ cho tỉ lệ chính xác).

## 13. Việc chờ chủ dự án
1. **Nghe A/B T1** (`ab-A-cu.mp4` vs `ab-B-moi.mp4`): chọn giữ chuỗi cũ hay bật `MIX=audio` từ tập sau T2.
2. **Nghe 3 mẫu giọng** (A/B/C §6): giữ Eric v2, hay thử Brian / Eric v4 cho T3 (T2 giữ Eric v2). Nếu chọn v4: cho phép kiểm điều khoản Beta.
3. **Duyệt từ điển phát âm** và cách áp "khi khoá lời" (§5); quyết việc phụ đề số bằng chữ hay giao P làm ánh xạ `.srt` (§12).
4. **Nghe 4 loại SFX** (`assets/audio/sfx/`) — đặc biệt whoosh/shimmer tự tổng hợp.
5. **Giao phiên K** biến A1–A13 thành luật (`docs/AUDIO-THUOC-DO.md`) — gồm chọn mục tiêu −14,0 (hiện tại, mép trên) hay −14,5 (giữa khoảng Kinh thánh).
6. **P:** thêm tiền tố phiên "AM" vào `docs/FILE-ZONES.md` §3; giải xung đột ghi thêm `RIGHTS.md` khi merge; merge nhánh `am-thanh` **sau khi T2 qua G2**.
7. Ghi chú: `claude/CINE-LAB-KE-HOACH-NANG-CAP.md` không có trong repo — nếu cần đối chiếu Mốc C, đưa tệp vào repo.
