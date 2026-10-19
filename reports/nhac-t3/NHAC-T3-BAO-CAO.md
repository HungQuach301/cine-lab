**Nhánh thật: `nhac-t3`**, tạo từ `origin/main` @ `8cedb8af`, đúng tên lệnh. Harness gợi ý nhánh `claude/clever-pasteur-6yokrn`, nhưng lệnh cho phép đẩy lên nhánh của lệnh, nên phiên đẩy lên `nhac-t3`. **Không merge.**

# NHẠC-T3 — phương án nhạc cho T3 Gibraltar (bản có lời G1 + bản không lời §11.2) — DỪNG chờ chủ dự án

> Phiên NHẠC-T3, 19/10/2026 (UTC 14:00 → 14:55). Phiên chỉ nghiên cứu, đề xuất và làm gói nghe mù. **Chưa trộn bản phát hành.**
> **Vùng sửa:** chỉ `reports/nhac-t3/**`, tổng 4,5 MB, không dùng LFS. Không sửa `assets/`, `channel-*/`, `scripts/`, `design/`, `checks/`, `docs/`, các sổ (`RIGHTS.md`, `AUTHORSHIP.md`…) hay nhánh khác.
> **Đã đọc:**
> - `reports/m3/BAI-HOC-LL.md`.
> - `docs/BIBLE-KENH2.md` §4, §10, §11.2, §12.5, §13.
> - `RIGHTS.md`, các dòng K2-MUS-1…5 và P1910-MUS-TAM.
> - `channel-k2/k2c-t3-01/loi-khoa.txt`, và `script-v4.1-KHOA.md` cho các dòng `[IM LẶNG]`.
> - `docs/AUDIO-THUOC-DO.md` (thước A1–A13).
> - Mã của `scripts/audio/master.py` và `music.py`: chỉ đọc để dùng đúng chuỗi trộn của kênh, không sửa.
> - Từ nhánh `k2c-t3-kl42` (**chưa merge vào main**, đọc bằng `git archive`, không sửa nhánh đó): `KL42-BAO-CAO.md`, `bang-gian-shot.md`, `nhip-that.json`, `xuat.json` và 2 MP3 xem.
> **Môi trường:** `verify.sh` cho 11 ĐẠT, 4 TRƯỢT (OpenEXR, three.js, tifffile/pyshp, k2v node_modules), giống KL42. Phiên không dùng mục nào trong 4 mục trượt.

## Khối điều lệ
| Trường | Lệnh | Thực tế |
|---|---|---|
| Nhánh | `nhac-t3` từ origin/main | đúng; 3 commit (2 việc dở + 1 cuối), đã đẩy, không merge |
| Vùng sửa | `reports/nhac-t3/**` ≤ 15 MB, không LFS | **4,5 MB**, tệp lớn nhất 1,09 MB. Không có tệp LFS |
| Chi phí | không mua nhạc, không đăng ký dịch vụ trả phí | **0**. Mọi bản đều tải tự do theo CC BY 4.0 |
| Claude | theo dõi $3; chặn $10 hoặc cùng lỗi ≥ 3 lần | Claude API **$0** (không gọi `claude -p`); 0 subagent. Token phiên chính không đo được trong phiên, nên không tự khai. Không lỗi nào lặp ≥ 3 lần (có 2 lỗi mã, mỗi lỗi 1 lần, §4.5) |
| OpenAI / ElevenLabs / YouTube | 0 | **0 / 0 / 0**. Không dùng nhạc AI. Lời là bản thu sẵn của KL42, nên 0 ký tự ElevenLabs. Mục ElevenLabs của `verify.sh` chỉ kiểm khoá, không gọi TTS |
| Preflight / email / UA | bắt buộc | hook `pre-commit` + `pre-push` đã cài; mọi commit **ĐẠT**, `lock.py --verify` **KHỚP**. Không có email trong tệp, header, URL hay payload. Mọi lệnh tải dùng UA `CineLab-research (+https://github.com/HungQuach301/cine-lab)` |
| Đẩy việc dở | ≤ 30 phút | đẩy lúc 14:06, 14:38 và lúc kết thúc; có `CHECKPOINT.md` |
| Dừng hỏi | không dừng giữa chừng | đúng |

---

## 0. Tóm tắt (đọc 2 phút)
1. **Giới hạn phải nói trước:** phiên này **không nghe được bằng tai**.
   - Việc chọn bài dựa trên 3 thứ: mô tả của tác giả; đặc tính đo bằng máy (loudness theo 5 s, tỉ lệ năng lượng ở dải lời 300–3 400 Hz, mật độ onset, tempo, `dac-tinh-cue.json`); và số đo trộn thật với lời G1.
   - "Hợp thể loại" và "cảm xúc đúng đoạn" là việc của chủ dự án, chấm qua gói nghe mù (§5).
2. **Bản đồ cảm xúc (§1):** lời phủ **≈ 89 % phim** (666,3 s lời trên 745,0 s).
   - Nhạc chỉ có 7 chỗ "thở" ≥ 1,5 s. Hai chỗ trong đó là tấm im lặng: **KB1943** (549,80–558,62 s, 8,8 s) và **KA2026** (716,57–725,00 s, 8,4 s).
   - Hệ quả: nhạc gần như luôn nằm dưới lời, nên phải thưa ở dải lời. Riêng hai tấm im lặng là chỗ nhạc phải tự gánh.
3. **Ứng viên (§2):**
   - (a) **5 bản có sẵn** (K2-MUS-1…5, Kevin MacLeod, CC BY 4.0). Cả 5 đều là synth; Tyrant và Half Mystery gần như phẳng (LRA ≈ 0,4–1,0 LU).
   - (b) **8 bản mới, cùng một tác giả: Scott Buckley**, CC BY 4.0, cho phép thương mại, YouTube kiếm tiền và phim phân phối ngoài mạng. Không có NC/ND/SA. Điều khoản nguyên văn ở `giay-phep/`, SHA ở `nguon-moi.json`.
   - Đã sàng 13 bản, loại 5. Không dùng nhạc cổ điển phạm vi công cộng (lý do ở §2.3).
4. **Hai cue sheet (§3), cả hai phủ liên tục 0 → 761 s, không lặp đoạn bài:**
   - **A:** 9 cue / 5 bản có sẵn.
   - **B:** 13 cue / 8 bản mới + Lightless Dawn.
   - 761 s = phương án B 745,0 s + 2 thẻ phương pháp × 8 s (D6). **Đây là giả định**, chờ phiên P xác nhận.
5. **Luật lời trên nhạc §4 (p10 ≥ 15 dB / min ≥ 12 dB): ĐẠT ở cả hai phương án**, đo thật trên bản trộn cả phim với lời G1 bằng chuỗi `master.py` của kênh:
   - Duck thích ứng (chuỗi chuẩn): **A p10 18,97 / min 17,30 dB**; **B p10 19,58 / min 18,23 dB**.
   - Duck cố định −12 dB (xem nhạc có tự hợp lời không, chưa hạ thêm): A p10 17,34 / **min 10,91 dB (trượt min ở 2m–2n)**; B p10 16,58 / min 13,93 dB (đạt).
   - Duck sâu nhất cần: A **−20,5 dB** (ở 2m, có nguy cơ nghe "bơm"); B −16,5 dB.
6. **Gói nghe mù (§5):** `nghe-mu/`, 4 cặp X/Y (móc, pin nổi, KB1943 chỉ nhạc, KA2026 chỉ nhạc). Khoá ở `khoa.json`.
   - Cặp có lời: −14,0 LUFS, đỉnh thật ≤ −1,8 dBTP, đo trên chính tệp MP3.
   - Cặp im lặng: cùng −17,0 LUFS, gần mức trong phim.
7. **Đề xuất (§8): chọn B, sau nghe mù.** Lý do: B đúng thể loại hơn (dàn dây/cello điện ảnh so với synth), có cung kịch tính thật cho đỉnh 2m, cần duck nông hơn và đều hơn, và có motif "cổng" mở/đóng vòng.
   - Rủi ro chính là **Content ID**: thư viện Scott Buckley có hệ "Smart Content ID". Hệ này tự claim nếu mô tả video thiếu ghi công, nên phải ghi công đúng mẫu trong mô tả.
   - Bài mới phải vào `RIGHTS.md` và `assets/` trước khi trộn thật. Việc đó thuộc phiên P, phiên này không sửa sổ.
8. **Bản không lời (§6):** đề xuất 7 motif / 8 "chương nhạc" theo mốc đinh, LRA đích 6–9 LU, không duck, tấm im lặng là chỗ nhạc nhỏ nhất. Có 2 phương án hình (giữ 745 s, hoặc cắt còn ≈ 636 s).

**Chỉ số nằm trong ±5 % quanh ngưỡng:**
| Chỉ số | Đo | Ngưỡng | Lệch |
|---|---|---|---|
| Loudness 4 trộn thử (WAV, `master.py`) | −13,9 LUFS | dải −15,0…−13,8, đích −14,0 | cách cận trên 0,1 LU (0,7 %) |
| Loudness cả phim A và B | −14,0 LUFS | dải −15,0…−13,8 | cách cận trên 0,2 LU (1,4 %) |
| Loudness tệp nghe mù, cặp có lời | −14,0 / −14,1 LUFS | đích −14,0 ± 0,1 | 0–0,7 % |
| SMR p10, A, duck cố định −12, đoạn 2j–2n | 15,39 dB | ≥ 15 dB | **+2,6 %** (chỉ số chẩn đoán; chuỗi chuẩn cho 20,19) |
| SMR p10, B, duck cố định −12, đoạn 2j–2n | 15,87 dB | ≥ 15 dB | +5,8 % (ngay ngoài dải) |
| SMR p10, A, duck cố định, đoạn ch3 / 4h–4i | 16,34 / 16,40 dB | ≥ 15 | +8,9 % / +9,3 % (ngoài dải; ghi để so) |
| Thời lượng nhạc | 761 s (giả định thẻ phương pháp 2 × 8 s) | — | chờ P xác nhận |
| Đỉnh thật trộn thử, sau AAC | −1,3 … −1,5 dBTP | ≤ −1,0 | đạt, dư 0,3–0,5 dB |

---

## 1. Bản đồ cảm xúc T3 (theo nhịp thật KL42, phương án B 745,0 s)
- **Mốc thời gian:** lấy từ `nhip-that.json` (B), trục phim.
- **"Mức nhạc so lời":** mức của nền nhạc khi trộn theo chuỗi kênh: lời −17 LUFS, nhạc chuẩn −24 LUFS mỗi cue, duck cơ bản −12 dB trong khoảng lời. Nhạc dưới lời vì vậy thấp hơn lời ≈ 19 LU.
- **"Thở":** khe không lời ≥ 1,5 s (đo trên mốc câu). Lời phủ ≈ 89 % thời lượng; ngoài 7 khe này, nhạc chỉ nhô lên giữa các câu (khe 0,4–1,4 s).

| # | Đoạn (shot) | Phim (s) | Nội dung | Cảm xúc cần | Mức nhạc so lời | Nhạc thở |
|---|---|---|---|---|---|---|
| M1 | **Móc** 0a–0c | 0,00–15,00 | nửa đêm ở cổng biên giới; "no routine checks"; Rock ở cửa Địa Trung Hải | đêm, tò mò, hơi bất an; **nhạc vào từ giây 0** (TL-5) | dưới lời, thưa, không giai điệu | — |
| M2 | Móc 0d–0f | 15,00–33,00 | 14 cuộc vây 1309–1783; "both sides' records"; 10 pin nổi 1782 | sức nặng lịch sử, lời hứa của phim | dày lên nhẹ, vẫn dưới lời | — |
| M3 | Móc 0g–0h | 33,00–43,83 | đường băng 1941; câu hỏi "paperwork and payrolls?" | lật ngược; nhạc **treo, không giải quyết**, thu hẹp trước ch1 | dưới lời | rút trước 43,83 |
| C1a | ch1 SM1–1e | 43,83–98,88 | 1704: Đại Liên minh, hạm đội Anh–Hà Lan, ~15 000 phát, chiếm thành | căng kiểu quân sự nhưng nhìn từ xa (bản đồ, tranh) | dưới lời | **95,31–98,88 (3,6 s): MỐC ĐINH 4/8/1704**, nhạc nhấn/ngân |
| C1b | 1f–1h | 98,88–130,50 | quân số hai phía; dân rời sang San Roque; Utrecht 1713 | trầm, mất mát; giọng văn bản | dưới lời, mỏng | — |
| C1c | 1i | 130,50–147,62 | eo đất: hai lập trường hôm nay | bất định, **trung tính** (không nghiêng phe) | dưới lời | — |
| C1d | 1j–1k | 147,62–173,08 | vây 1705, 1727; tuyến đá 1730; "La Línea" | cứng, dựng tường; khép chương | dưới lời | — |
| C2a | ch2 2a–2c | 173,08–207,58 | 21/6/1779 Madrid cắt đường; phong toả từ Algeciras | **siết**, lạnh, đều | dưới lời | — |
| C2b | 2d–2f | 207,58–235,21 | 1/1780 ăn cây dại; Eliott; 3 đoàn tiếp tế; scurvy, tàu chanh | **đói / kiệt**: thưa tầng, không bi luỵ | thấp nhất ch2 | — |
| C2c | 2g–2i | 235,21–262,17 | 12/4/1781 phố cháy, cướp kho; 400 000+ phát | **cháy lần 1**: dày lên, gấp hơn | dưới lời | — |
| C2d | KA1782 (khung neo) | 262,17–270,17 | 9/1782 quân số | **chờ**, giữ | dưới lời | **267,39–270,17 (2,8 s)** |
| C2e | 2o–2p | 270,17–288,54 | đào hầm vách bắc; lỗ thông khí | bền bỉ, lao động, nhịp đều | dưới lời | — |
| C2f | 2j | 288,54–302,96 | đạn nung đỏ; 8/9 | nóng lên, dựng căng | dưới lời | — |
| C2g | 2k–2l | 302,96–326,96 | hạm đội Pháp–TBN tụ; d'Arçon; pin nổi bị từ chối thử | **căng tột độ**, chờ đòn | dưới lời, mức cao dần | — |
| C2h | **2m** CÚ LIÊN HOÀN #2 | 326,96–346,96 | 13/9/1782, 10:25 tấn công | **cháy, đỉnh của phim** | cao nhất dưới lời; duck thích ứng giữ ≥ 15 dB | — |
| C2i | 2n | 346,96–354,96 | 10 → 0 pin nổi; > 2 000 người mất | sau cơn: nhạc rút, tắt dần | giảm | — |
| C2j | 2q–2r | 354,96–382,58 | phong toả không buộc được đầu hàng; hoà ước 1783; đếm người chết hai phía | kiệt, lặng | thấp | — |
| C3 | **ch3** 3a–3h | 382,58–471,62 | dải trung lập "bò" dần; 1810 nổ pháo đài; La Línea; hàng rào 1909; sân cỏ 1934; lời mời đăng ký (3h) | **chờ, mơ hồ**, chậm; không kịch tính | dưới lời, ambient | **431,97–435,29 (KC1910)**; **453,95–457,29 (rào 1909)** |
| C4a | ch4 4a–4f | 471,62–533,71 | 1939 sân bay trên đất tranh chấp; đường băng lấn vịnh; hầm ~55 km; bản đồ 1943 | toan tính, kỹ thuật, u ám | dưới lời | — |
| C4b | SM3 → 4g | 533,71–549,80 | 5/1940 sơ tán phụ nữ, trẻ em; "non-belligerent"; Bắc Phi | mất mát, tản ra | dưới lời | — |
| **S1** | **KB1943 (tấm im lặng)** | 549,80–558,62 (lời ngừng 8,8 s) | khung neo phố 1943: không phụ nữ, trẻ em | **vắng** — nhạc kể bằng khoảng trống | **nhạc gánh**: ≈ −16…−18 LUFS (thấp hơn đoạn có lời ≈ 3–5 LU, không thành "hố") | toàn bộ |
| C4c | 4h–4i | 558,62–585,83 | TBN phản đối vùng nước, không phản đối sân bay; đêm 7/11/1942, 650 máy bay | khối lượng chiến tranh, đà | dưới lời | — |
| C5a | ch5 5a–5b | 585,83–609,58 | 6/1969 đóng cổng hoàn toàn; 4 600 lao động; 1985 mở lại | lạnh, đóng | dưới lời | — |
| C5b | KB2026 → KC2026 | 609,58–641,58 | quảng trường hôm nay; người đi bộ qua đường băng; La Línea 28,6 % thất nghiệp | con người, nặng | dưới lời | **629,09–631,58 (2,5 s)** |
| C5c | 5e–5i | 641,58–697,54 | "Here's the twist": GDP/người; hiệp ước 2026; "as of 18 October 2026" | **bế tắc giấy tờ hiện đại**: nhịp máy, trung tính, không kịch | dưới lời | — |
| C5d | 5j | 697,54–716,57 | "So why did everyone fight…"; "A wall… a line… a fence… a runway" | dâng, gom lại | dưới lời, dâng | — |
| **S2** | **KA2026 (tấm im lặng)** | 716,57–725,00 (8,4 s) | khung neo phố 2026 | **lắng trước câu kết**: đỉnh cảm xúc cuối | nhạc gánh ≈ −16…−18 LUFS | toàn bộ |
| C5e | 5k | 725,00–745,00 | quay về hình nửa đêm; "The last siege ended in 1783. The argument didn't." | đóng vòng, **treo** | dưới lời | sau 744,37 |
| T | Thẻ phương pháp × 2 | 745–761 (giả định) | "How this film was made" | hạ, đuôi | chỉ nhạc, fade 4 s | toàn bộ |

**Lưu ý cho phiên trộn thật:**
- Hai tấm im lặng là quãng không lời > 8 s, nên thước **A10** sẽ báo. Phải khai hai tấm này là "khoảnh khắc nhạc".
- Không có quãng lặng bất thường (A5 = 0 ở cả hai bản trộn).

---

## 2. Ứng viên

### 2.1 (a) Thư viện có sẵn trong repo (Kevin MacLeod, CC BY 4.0, RIGHTS K2-MUS-1…5)
Đặc tính đo bằng `cong-cu/do_cue.py` (`so-do/dac-tinh-cue.json`):
- **I** là loudness tích hợp của bài.
- **Dải lời** là phần năng lượng rơi vào 300–3 400 Hz. Càng cao càng dễ đè lời.

| Bản | Dài | I | LRA≈ | Tempo / giọng (ước) | Dải lời | Hợp đoạn nào | Hạn chế |
|---|---|---|---|---|---|---|---|
| Half Mystery (K2-MUS-1) | 7:09 | −25,0 | 1,0 | 72 bpm (RIGHTS) / C thứ | 51–59 % đều | móc + kết (motif chủ đề kênh từ T1) | rất phẳng; synth, không mang không khí thế kỷ 18 |
| Beauty Flow (K2-MUS-2) | 7:13 | −17,8 | 1,2 | 108 bpm / E thứ | 11–16 % | ch5 kinh tế, giấy tờ ("nhịp máy" arpeggio) | đều suốt bài; dễ thành nhạc doanh nghiệp |
| Tyrant (K2-MUS-3) | 5:42 | −12,8 | **0,4** | 72 bpm / — | 38–41 % | ch1, ch4 (căng tối) | **phẳng nhất**: BAI-HOC-LL "nhạc một bản đều"; là nhạc tạm của animatic, nên chủ dự án đã quen tai |
| Sincerely (K2-MUS-4) | 6:15 | −13,3 | 3,4 | 72 bpm / E thứ | **3–6 %** | ch3 chờ; 5j | ấm, gần như không đè lời; thiếu độ căng cho đoạn chiến sự |
| Lightless Dawn (K2-MUS-5) | 6:20 | −24,3 | 8,9 | ambient / D thứ | 0–64 %; **đoạn 180–345 s chỉ 0–29 %** | ch2 phong toả/đói; ch3; tấm im lặng | có dốc lên ở 165–175 s; đặt dưới 2m–2n thì đè lời (§4.2) |

### 2.2 (b) Tám bản mới (Scott Buckley, CC BY 4.0)
- **Nguồn:** `https://www.scottbuckley.com.au/library/`, đọc ngày **19/10/2026**.
- **Người sáng tác và biểu diễn:** Scott Buckley (Buckley Collective Pty. Ltd.). Tác giả làm dàn nhạc bằng thư viện mẫu. Trang không ghi là có AI; tác giả tự mô tả là "my usual orchestra / modern orchestral template".
- **ISRC:** không có trong thẻ ID3, trang cũng không ghi.
- **Tệp:** 8 MP3 tải về vùng tạm ngoài git, SHA ở `nguon-moi.json`. **Chưa đưa vào `assets/`**, chờ duyệt.
- **Loại sau khi sàng:**
  - Anabasis I, Anabasis II, Decoherence: dải lời 47–97 %, lấn lời.
  - The Long Dark: trùng vai với Undertow.
  - Desperation: tiêu đề và chất "solo recorder" dễ thành nhạc minh hoạ; dải lời 33–99 %.

| ID | Bản (trang) | Dài | I | Dải lời (đoạn dùng) | Vai trong B | Mô tả của tác giả (nguyên văn, rút gọn) |
|---|---|---|---|---|---|---|
| NT3-1 | **Intervention — No Melody Alt Mix** (`/library/intervention/`) | 4:18 | −14,6 | 11–22 % | motif "cổng/hôm nay": móc + ch5 | "Darker ambient piano – subtle thriller vibes … a 'no melody' alternative mix." |
| NT3-2 | **Signal to Noise — No Piano Melody** (`/library/signal-to-noise/`) | 5:54 | −16,3 | 22–63 % | ch1 1704–1730 | "mysterious, cinematic neo-classical … solo cello & piano … ominous low strings. Dark and melancholy, but also hopeful." |
| NT3-3 | **The Weight of Air – Katabasis I** (`/library/katabasis-i/`, 25/9/2026) | 9:50 | −19,6 | 23–54 % | ch2 phong toả → đói → cháy → hầm | "slow, languid classical work for string orchestra – quite dark and textural, with low strings acting as the spine of the work." |
| NT3-4 | **Juggernaut** (`/library/juggernaut/`) | 3:42 | −14,8 | 4–65 % | 2j–2n (dựng → đỉnh → tắt); 4h–4i | "Chugging, malevolent strings, brass and percussion, building up into a marauding epic force." |
| NT3-5 | **Never Dying** (`/library/never-dying/`) | 6:42 | −14,7 | 6–12 % | 2q–2r sau cơn | "ambient orchestral … synth and string orchestra – full of bittersweet tension." |
| NT3-6 | **Undertow** (`/library/undertow/`) | 4:10 | −14,5 | 11–33 % | ch4 1939–1940 | "A sombre, ebbing piano/string/synth track." |
| NT3-7 | **Echoes** (`/library/echoes/`) | 6:04 | −15,3 | (không lời) | tấm im lặng KB1943 (cello độc tấu vào) | "An atmospheric, bittersweet work for solo cello and strings." |
| NT3-8 | **Hiraeth** (`/library/hiraeth/`) | 5:46 | −14,0 | 12–47 % | 5j + KA2026 + kết | "'Hiraeth' means a longing for a home you can't return to … yearning solo cello." |

**Điều khoản (nguyên văn), cùng một câu trên trang của cả 8 bài** (`giay-phep/scottbuckley-tung-bai.txt`):
> "This work is licensed under a Creative Commons Attribution 4.0 International License ; meaning it's free for use in any project (including commercial) as long as I'm credited. For YouTube videos, credits must appear in the video description."

**Trang "Using This Music"** (`giay-phep/scottbuckley-using-this-music.txt`):
> "The music (mp3 downloads) found on scottbuckley.com.au is made available under the Creative Commons 'Attribution 4.0 International' (CC BY 4.0) License (unless stated otherwise). … [Music by] or [Additional Music by] or [Track Title] by Scott Buckley – released under CC-BY 4.0. www.scottbuckley.com.au … this means that the music in this library is FREE, even for commercial use, as long as attribution is given. … Credits must be provided in the video description (not in the video itself). If you don't do this, you will likely get a copyright claim on the video … My music cannot be resold in isolation, or redistributed/reuploaded to music streaming platforms, and must be synchronised with other media (e.g. film)."

**Trang "Licensing"** (`giay-phep/scottbuckley-licensing.txt`; bảng dựng lại từ HTML, ✓/✗ là ảnh dấu tích):
- Ở cột **CC-BY (with credit)**:
  - "Online Multimedia – YouTube, Vimeo & Social Media, … Animation, Film etc." ✓.
  - "**Film – other than online only (i.e. cinema distribution)** ✓".
  - "Software – games, apps, CD/DVD/BLURAY multimedia" ✓.
- Vậy **YouTube kiếm tiền và bán phim (kể cả phân phối ngoài mạng) đều nằm trong CC BY khi có ghi công**.
- Hạn chế áp cho mình: không bán riêng bản nhạc, không đưa lên dịch vụ phát nhạc hay dịch vụ nhận dạng âm thanh.

**Ghi công đề xuất** (mô tả YouTube + credit cuối phim), mỗi bài một dòng:
> "Katabasis I" by Scott Buckley – released under CC-BY 4.0. www.scottbuckley.com.au (edited)

- Chữ "(edited)" đáp ứng CC BY 4.0 §3(a)(1)(B) (phải nêu nếu đã sửa đổi): phim cắt, ghép, fade và duck nhạc.
- Với Kevin MacLeod, incompetech nói "There is no need to mention if you cut and splice". Thêm cũng không hại, nhưng không bắt buộc.

### 2.3 Nhạc cổ điển phạm vi công cộng: đã xét, không đề xuất trong T3
- **Ưu thế về đề tài:** có nhạc đúng thời kỳ (Boccherini viết ở triều đình Madrid, khoảng 1780).
- **Vướng 1 — giấy phép bản thu:**
  - Musopen bị proxy chặn (403), không đọc được trang giấy phép nên không dùng.
  - Wikimedia Commons: bản thu Boccherini tìm thấy là bản nghiệp dư "violin and synthesizer". Nhiều bản trên Commons mang CC BY-SA. Với CC 4.0, ghép nhạc vào phim là tác phẩm phái sinh, nên SA buộc phim cũng phải cấp CC BY-SA. Điều đó không hợp với bán phim.
- **Vướng 2 — Content ID:** bản thu cổ điển là loại bị đăng ký Content ID nhầm nhiều nhất (nhiều hãng thu cùng một tác phẩm).
- **Vướng 3 — trung tính:** quốc ca hay hành khúc phe ("Heart of Oak", "Marcha Real") không dùng. Lý do giống luật không dùng cờ/biểu tượng làm màu tô (§11.1).
- **Kết luận:** chỉ xét lại khi có bản thu chuyên nghiệp CC0 hoặc CC BY có nguồn rõ.

---

## 3. Cue sheet hai phương án
- **Quy ước nền nhạc:** dựng lại tối giản theo `scripts/audio/music.py`.
  - Mỗi nhóm cue chuẩn về −24 LUFS, đo trên toàn bộ đoạn bài nhóm dùng. Các đoạn cắt ghép cùng nhóm (B4a–c) dùng chung hệ số, nên giữ động học nội tại.
  - Giao bài crossfade công suất bằng nhau, tâm tại "phim vào/ra".
  - `tang` = nâng nhạc trong tấm im lặng, dốc 1 s nằm trong khe, không chạm lời.
- **Tệp máy đọc:** `cue/cue-A.json`, `cue/cue-B.json`.
- **Khi trộn thật**, phiên âm thanh nắn điểm giao về vạch ô nhịp bằng `music.py` (`align: bar`). Phiên này chỉ nắn theo phách ở 3 đoạn Juggernaut (IBI 0,952 s).

### A — chỉ thư viện có sẵn (K2-MUS-1…5)

| Cue | Bản | Đoạn trong bản (s) | Phim vào → ra (s) | Dài (s) | Giao vào / ra (s) | Mức | Khớp đoạn | Ghi chú |
|---|---|---|---|---|---|---|---|---|
| A1 | Half Mystery (K2-MUS-1) | 0,00 → 43,83 | 0,00 → 43,83 | 43,83 | 0,30 / 2,00 | mid | M1–M3 móc 0a–0h | motif chủ đề kênh (mở vòng) |
| A2 | Tyrant (K2-MUS-3) | 0,00 → 129,25 | 43,83 → 173,08 | 129,25 | 2,00 / 2,00 | mid | C1 ch1 1704–1730 | |
| A3 | Lightless Dawn (K2-MUS-5) | 0,00 → 181,88 | 173,08 → 354,96 | 181,88 | 2,00 / 2,00 | mid | C2a–C2i ch2 2a–2n | dốc lên của bài (165–175 s) rơi vào 2m (≈ phim 338–348) |
| A4 | Sincerely (K2-MUS-4) | 0,00 → 116,66 | 354,96 → 471,62 | 116,66 | 2,00 / 2,00 | mid | C2j + C3 | |
| A5 | Tyrant (K2-MUS-3) | 130,00 → 208,18 | 471,62 → 549,80 | 78,18 | 2,00 / 1,50 | mid | C4a–C4b ch4 4a–SM3 | đoạn bài khác A2, không lặp |
| A6 | Lightless Dawn (K2-MUS-5) | 328,00 → 364,03 | 549,80 → 585,83 | 36,03 | 1,50 / 2,00 | mid + **4,0 dB** 549,85–558,60 | **S1 KB1943** + C4c | đoạn bài không trùng A3 |
| A7 | Beauty Flow (K2-MUS-2) | 0,00 → 111,71 | 585,83 → 697,54 | 111,71 | 2,00 / 2,00 | mid | C5a–C5c ch5 5a–5i | |
| A8 | Sincerely (K2-MUS-4) | 120,00 → 147,46 | 697,54 → 725,00 | 27,46 | 2,00 / 1,50 | mid + **4,5 dB** 716,60–725,00 | C5d + **S2 KA2026** | đoạn bài không trùng A4 |
| A9 | Half Mystery (K2-MUS-1) | 44,00 → 80,00 | 725,00 → 761,00 | 36,00 | 1,50 / 4,00 | mid | C5e kết + T | motif đóng vòng; không trùng A1 |

- **Tổng phủ nhạc: 761,00 s**, liên tục, không lặp đoạn bài.
- **5 bản:** Half Mystery 79,8 s · Tyrant 207,4 s · Lightless Dawn 217,9 s · Sincerely 144,1 s · Beauty Flow 111,7 s.
- **Luật §4:** **ước được và đo được: ĐẠT** (§4).
  - Nhạc dưới 2m–2n cần duck tới −20,5 dB.
  - Với duck cố định −12 dB, min chỉ 10,9 dB, tức trượt min.

### B — có sẵn + bản mới

| Cue | Bản | Đoạn trong bản (s) | Phim vào → ra (s) | Dài (s) | Giao vào / ra (s) | Mức | Khớp đoạn | Ghi chú |
|---|---|---|---|---|---|---|---|---|
| B1 | Intervention — No Melody (NT3-1) | 0,00 → 43,83 | 0,00 → 43,83 | 43,83 | 0,30 / 2,00 | mid | M1–M3 móc | motif "cổng/hôm nay" (mở vòng) |
| B2 | Signal to Noise — No Piano Melody (NT3-2) | 20,00 → 149,25 | 43,83 → 173,08 | 129,25 | 2,00 / 2,00 | mid | C1 ch1 | tránh đoạn cello độc tấu 150–195 s (dải lời 97–100 %) |
| B3 | Katabasis I (NT3-3) | 180,00 → 295,46 | 173,08 → 288,54 | 115,46 | 2,00 / 1,00 | mid | C2a–C2e (phong toả → đói → cháy phố → KA1782 → hầm) | |
| B4a | Juggernaut (NT3-4) | 29,81 → 68,23 | 288,54 → 326,96 | 38,42 | 1,00 / 0,95 | mid (nhóm JUG2) | C2f–C2g 2j–2l | dựng |
| B4b | Juggernaut (NT3-4) | 160,38 → 180,38 | 326,96 → 346,96 | 20,00 | 0,95 / 0,95 | mid (JUG2) | **C2h 2m tấn công** | cắt ghép đúng phách tại ranh shot 2l→2m; đỉnh của bài |
| B4c | Juggernaut (NT3-4) | 204,52 → 215,56 | 346,96 → 358,00 | 11,04 | 0,95 / 3,00 | mid (JUG2) | C2i 2n | đuôi tắt của bài; chồng có chủ ý 3,04 s với B5 |
| B5 | Never Dying (NT3-5) | 0,00 → 27,62 | 354,96 → 382,58 | 27,62 | 3,00 / 2,00 | mid | C2j 2q–2r | |
| B6 | Lightless Dawn (K2-MUS-5) | 180,00 → 269,04 | 382,58 → 471,62 | 89,04 | 2,00 / 2,00 | mid | C3 ch3 | đoạn dải lời 1–29 % |
| B7 | Undertow (NT3-6) | 10,00 → 88,18 | 471,62 → 549,80 | 78,18 | 2,00 / 1,20 | mid | C4a–C4b | |
| B8 | Echoes (NT3-7) | 14,00 → 22,82 | 549,80 → 558,62 | 8,82 | 1,20 / 1,20 | high + **1,5 dB** | **S1 KB1943** | cello độc tấu vào ở ≈ 15 s bài |
| B9 | Juggernaut (NT3-4) | 0,00 → 27,21 | 558,62 → 585,83 | 27,21 | 1,20 / 2,00 | mid (nhóm JUG4) | C4c 4h–4i | đoạn mở thấp; không trùng B4 |
| B10 | Intervention — No Melody (NT3-1) | 45,00 → 156,71 | 585,83 → 697,54 | 111,71 | 2,00 / 2,00 | mid | C5a–C5c ch5 | motif cổng trở lại; nhịp piano dày lên ở 120–150 s bài (≈ 5f–5h, giấy tờ) |
| B11 | Hiraeth (NT3-8) | 31,00 → 94,46 | 697,54 → 761,00 | 63,46 | 2,00 / 4,00 | mid + **4,5 dB** 716,60–725,00 | C5d + **S2 KA2026** + C5e + T | KA2026 rơi vào 50–58 s bài (dâng) |

- **Tổng phủ nhạc:** 761,00 s trục phim (tổng các cue là 764,04 s vì chồng 3,04 s có chủ ý ở B4c/B5). Liên tục, không lặp đoạn bài.
- **9 bản:** Intervention NM 155,5 s · Signal to Noise NM 129,3 · Katabasis I 115,5 · Juggernaut 96,7 · Never Dying 27,6 · Lightless Dawn 89,0 · Undertow 78,2 · Echoes 8,8 · Hiraeth 63,5.
- **Luật §4:** **ước được và đo được: ĐẠT** (§4); duck sâu nhất −16,5 dB.

**Mức cân bằng ở tấm im lặng.** Bản trộn đầu chưa có `tang`: nhạc ở hai tấm im lặng chỉ −21,1…−21,5 LUFS, thấp hơn đoạn có lời ngay trước (≈ −13…−14) tới ≈ 8 LU, nghe thành "hố". Đã nâng nhạc ở cả hai phương án để so công bằng:

| | KB1943 | KA2026 | Đoạn có lời 11 s trước |
|---|---|---|---|
| A | −17,8 LUFS | −16,7 | −13,0 / −13,7 |
| B | −16,3 LUFS | −17,2 | −13,0 / −13,8 |

---

## 4. Số đo trộn thử
**Cách trộn:**
- Công cụ `cong-cu/tron.py` gọi **nguyên** `scripts/audio/master.py finish()`, không sửa:
  - lời: lọc 70 Hz → khử xì → nén 2,5:1 → −17 LUFS;
  - duck thích ứng cơ bản −12 dB, sàn −30;
  - loudness 2 lượt tuyến tính về −14 LUFS, trần −1 dBTP, kiểm sau AAC 256k.
- **SMR theo A4:** stem lời đã xử lý so với nền đã duck, cửa sổ 3 s bước 1 s nằm trọn trong khoảng lời (gộp nghỉ < 0,55 s), lọc K. Có ghi từng cửa sổ theo giây phim (`so-do/tron-ca-phim-*.json → cua_so_smr`).
- **Lời:** dựng lại trên trục phim B từ **2 MP3 xem của KL42** (`cong-cu/dat_loi.py`). Mỗi shot lấy khoảng `[bd_stem, kt_stem]` đặt tại `loi_bd_phim`.
  - Stem WAV/FLAC của KL42 nằm ngoài git và **đã mất theo container**, đúng như KL42 §6 đã cảnh báo.
  - MP3 96 kb/s đã qua alimiter, nên SMR đo ở đây là **ước gần đúng**. Phải đo lại trên stem FLAC khi có.

### 4.1 Cả phim 0–761 s (`so-do/smr-ca-phim.json`)
| | I / LRA / TP (sau AAC) | SMR p10 | SMR min | SMR trung vị | cửa sổ < 15 dB | Duck trung vị / sâu nhất | Khoảng phải hạ quá −12 |
|---|---|---|---|---|---|---|---|
| **A, chuỗi chuẩn** | −14,0 / 3,1 / −1,4 | **18,97** | **17,30** | 20,25 | 0 / 439 | −12,8 / **−20,5** dB | 43 / 56 |
| **B, chuỗi chuẩn** | −14,0 / 3,1 / −1,3 | **19,58** | **18,23** | 21,95 | 0 / 439 | −13,95 / −16,5 dB | 45 / 56 |
| A, duck cố định −12 (chẩn đoán) | −14,0 / 3,2 / −1,4 | 17,34 | **10,91 ✗** | 19,10 | 4 (345–348 s, 2m→2n) | −12 | 0 |
| B, duck cố định −12 (chẩn đoán) | −14,0 / 3,1 / −1,4 | 16,58 | 13,93 | 19,59 | 4 (87 s; 173,6–174,6 s giao ch1→ch2; 350 s) | −12 | 0 |

- Cả hai đều đạt A1, A2, A5 (0 quãng lặng bất thường), A7 (0 chạm trần) và A12 (loudnorm tuyến tính).
- Hai tấm im lặng là quãng không lời > 8 s (A10), nên phải khai "khoảnh khắc nhạc" (§1).

### 4.2 Theo đoạn (chuỗi chuẩn | duck cố định −12): SMR p10 / min (dB), duck trung vị / sâu nhất (dB)
| Đoạn | A chuẩn | A cố định | B chuẩn | B cố định | Nhận xét |
|---|---|---|---|---|---|
| móc 0a–0h | 19,1 / 18,3 · −13,0 / −13,8 | 17,4 / 16,9 | 20,0 / 19,1 · −12,2 / −13,8 | 19,3 / 17,3 | B thưa hơn ở dải lời (Intervention NM, 15–24 %) |
| ch1 ROCK | 18,7 / 17,6 · −12,4 / −13,1 | 18,2 / 17,0 | 19,9 / 18,7 · −15,1 / −16,5 | 16,4 / 15,0 | B dày hơn (low strings), cần hạ thêm ≈ 3 dB |
| ch2 2a–2i | 20,2 / 17,4 · −13,3 / −14,3 | 18,3 / 17,0 | 19,4 / 18,2 · −14,8 / −15,4 | 16,1 / **13,9** | B min sát ở chỗ giao S2N→Katabasis (173,6 s): nên giao ngắn hơn hoặc sớm hơn 1 ô nhịp |
| ch2 KA1782–2p | 22,4 / 22,1 | 21,3 / 20,7 | 19,4 / 19,2 | 17,2 / 16,9 | |
| **ch2 2j–2n** | 20,2 / 19,1 · −15,4 / **−20,5** | **15,4 / 10,9 ✗** | 19,6 / 18,8 · −15,1 / −16,5 | 15,9 / 14,8 | A: dốc lên của Lightless Dawn rơi đúng câu 2m–2n, nên phải hạ 20,5 dB (nguy cơ "bơm"). B: cao trào được thiết kế bằng cắt ghép, cần ít hơn 4 dB |
| ch2 2q–2r | 19,6 / 18,9 · −14,6 | 16,4 / 16,2 | 19,6 / 19,4 · −15,5 | 16,1 / 15,9 | |
| ch3 NEUTRAL | 19,4 / 18,6 · −14,1 / −15,7 | 16,3 / 15,6 | 19,5 / 19,3 · −13,8 / −15,9 | 16,6 / 15,5 | |
| ch4 4a–SM3 | 18,8 / 18,1 · −12,0 / −12,5 | 18,5 / 17,8 | 19,7 / 18,6 · −14,0 / −14,7 | 17,4 / 16,3 | |
| ch4 4h–4i | 18,9 / 17,3 · −15,0 / −16,9 | 16,4 / 15,5 | 19,4 / 18,9 · −13,5 / −13,8 | 17,6 / 17,1 | |
| ch5 5a–5i | 19,3 / 17,9 · −13,3 / −14,9 | 17,6 / 16,5 | 19,5 / 18,4 · −14,2 / −15,6 | 16,9 / 15,9 | |
| ch5 5j–5k | 19,7 / 19,4 · −13,0 / −13,1 | 17,4 / 17,3 | 19,6 / 19,6 · −14,7 / −15,0 | 17,2 / 16,6 | |

**Đọc số:**
- Chuỗi chuẩn kéo mọi đoạn về p10 ≈ 19–20 dB, vì nó hạ nhạc đến mức cần.
- Phân biệt hai phương án là **độ sâu và độ đều của duck**:
  - A phần lớn chỉ cần mức cơ bản, nhưng có một chỗ phải hạ rất sâu (−20,5 dB, 2m–2n).
  - B cần hạ thêm đều 2–3 dB suốt phim, vì dàn dây duy trì dày hơn synth thưa. Đổi lại, B không có chỗ nào phải hạ sâu bất thường.
- **Mức −24 LUFS mỗi cue là mức chung.** Khi trộn thật có thể đặt B ở `intensity: low` cho ch1–ch2 (−5 dB + lọc 2,5 kHz) để bớt hạ. Việc này để tai chủ dự án quyết sau nghe mù.

### 4.3 Bốn đoạn trộn thử cho gói nghe (WAV từ `master.py`, trước MP3)
| Đoạn | I | TP sau AAC | SMR p10 / min | Duck trung vị / sâu nhất |
|---|---|---|---|---|
| A móc 0–34 s | −13,9 | −1,4 | 19,01 / 18,34 | −12,0 / −13,2 |
| B móc 0–34 s | −13,9 | −1,5 | 20,01 / 19,17 | −12,0 / −13,3 |
| A pin nổi 302–356,5 s | −13,9 | −1,5 | 20,27 / 19,51 | −16,9 / **−20,5** |
| B pin nổi 302–356,5 s | −13,9 | −1,5 | 19,51 / 19,20 | −15,9 / −16,5 |

### 4.4 Tệp MP3 nghe mù (đo trên chính MP3 160 kb/s; BAI-HOC-LL #69)
Cả 8 tệp: I = đích ± 0,1 LU (−14,0 / −14,1 cho cặp 1–2; −17,0 cho cặp 3–4). Đỉnh thật −1,8 … −5,0 dBTP (≤ −1). Hai bản trong cùng cặp có kích thước bằng nhau, nên không lộ phương án qua kích thước tệp. SHA ở `khoa.json`.

### 4.5 Sự cố trong phiên (mỗi lỗi 1 lần, đã sửa)
1. `dat_loi.py`: shot 0a có `bd_stem − 0,12 < 0`, nên lát mảng rỗng. Đã kẹp về 0.
2. Hai vòng chờ dùng `pgrep -f` tự khớp với chính lệnh của nó, nên chờ thừa ≈ 10 phút đồng hồ. Không ảnh hưởng kết quả: các bản trộn đã xong lúc 14:24 và được kiểm lại theo PID.
3. Bản gói nghe đầu ra −14,4 LUFS (limiter lặp lại trên tệp đã giới hạn), và hai bản tấm im lặng lệch nhau 1,5 LU. Đã sửa `goi_nghe.py`: bù tuyến tính tới đích ± 0,1, cặp im lặng cùng −17,0. Bản đầu đã bị xoá, không đẩy.

---

## 5. Gói nghe mù — `reports/nhac-t3/nghe-mu/` (4,2 MB)
| Cặp | Tệp X / Y | Phim | Nội dung |
|---|---|---|---|
| 1 | `1-moc-X.mp3`, `1-moc-Y.mp3` (34 s) | 0,0–34,0 s | móc 0a–0f, lời G1 + nhạc |
| 2 | `2-pin-noi-X.mp3`, `2-pin-noi-Y.mp3` (54,5 s) | 302,0–356,5 s | 2k–2n pin nổi, lời G1 + nhạc |
| 3 | `3-KB1943-X.mp3`, `3-KB1943-Y.mp3` (9,3 s) | 549,3–558,6 s | **chỉ nhạc**, tấm im lặng KB1943 |
| 4 | `4-KA2026-X.mp3`, `4-KA2026-Y.mp3` (8,9 s) | 716,1–725,0 s | **chỉ nhạc**, tấm im lặng KA2026 (thêm ngoài lệnh, vì đây là tấm im lặng cuối, nơi nhạc gánh câu kết) |

- **Khoá:** `nghe-mu/khoa.json`, gán ngẫu nhiên từng cặp bằng `secrets.randbelow(2)`. **Phiên không ghi ánh xạ X/Y vào báo cáo.**
- **Hướng dẫn và phiếu chấm:** `nghe-mu/HUONG-DAN-NGHE.md`. Tiêu chí: hợp thể loại, không lấn lời, cảm xúc đúng đoạn, không "nhạc quảng cáo", và (tuỳ chọn) trung tính giữa các phía.
- **Thiên lệch đã biết:** Tyrant (A, ch1/ch4) là nhạc tạm animatic mà chủ dự án đã nghe.
  - Bốn đoạn trong gói gần như không có Tyrant: A dùng Half Mystery, Lightless Dawn và Sincerely.
  - Ngoại lệ: ≈ 1,2 s đầu của cặp 3 là đuôi giao ra của Tyrant (A5, A) hoặc Undertow (B7, B).
  - Hai bản đều mở bằng đuôi bài trước như trong phim, nên vẫn công bằng.

---

## 6. Bản không lời (§11.2) — đề xuất cấu trúc nhạc (chưa làm)
**Mục tiêu:** nhạc + bộ đếm năm + chữ tối thiểu phải gánh nhịp kể. Theo §13, hình mang mạch chính; nhạc chỉ cho biết **lúc nào chuyển thời kỳ, lúc nào căng, lúc nào mất**.

**Hai phương án hình (phiên P / đạo diễn chọn):**
| | K1: giữ hình phương án B (745 s + thẻ) | K2: dựng lại ≈ 636 s |
|---|---|---|
| Cách làm | dùng nguyên hình bản chính, bỏ lời, bật nhạc trần | bỏ 9 thẻ số (66,2 s) và 4 ảnh văn bản trích dẫn (1h, 2r, 4h, 5g ≈ 43 s), vì các shot này sống nhờ lời |
| Ưu | 0 render thêm; bộ đếm khớp sẵn | nhịp chặt hơn; không có khung "chờ lời" |
| Nhược | ≈ 15 % thời lượng là thẻ/ảnh văn bản không còn lời đi kèm | phải dựng lại và cue lại |
| Rủi ro | khán giả rời ở các thẻ | lệch với bản chính |

**Cấu trúc nhạc đề xuất (cho K1; với K2 thì co theo shot):**
| "Chương nhạc" | Phim (K1) | Motif | Cung | Điểm nhấn bắt buộc (đồng bộ hình) | Bài gợi ý (từ B) |
|---|---|---|---|---|---|
| I Mở — "cổng hôm nay" | 0–44 | M-Cổng (piano ticking) | đêm → hé mở | bộ đếm nhảy 2026 → 1943 ở 0e; thẻ pin nổi 0f | Intervention (bản **có giai điệu**: không lời thì được dùng giai điệu) |
| II Rock 1704–1730 | 44–173 | M-Pháo đài (low strings, cello) | căng xa → chiếm → mất dân → tường đá | **4/8/1704** (1e) hit + ngân 3 s; tuyến 1730 mọc (1k) | Signal to Noise (bản đủ, có piano) |
| III Vây 1779–1782 (a) | 173–289 | M-Vây (dây trầm, đều) | siết → đói (mỏng còn 1–2 tầng) → cháy phố 1781 | 21/6/1779 bộ đếm ngày bắt đầu; 12/4/1781 lửa | Katabasis I |
| III Vây (b) | 289–355 | M-Đòn (chugging) | dựng → **đỉnh 2m** → sập | lò đạn đỏ 2j; **13/9/1782 10:25** (2m) đỉnh LRA; 10 → 0 pin nổi (2n) cắt về đơn tuyến | Juggernaut (cắt ghép như B4a–c) |
| IV Sau cơn + trung lập | 355–472 | M-Chờ (ambient, không nhịp) | kiệt → bò chậm | 1810 nổ pháo đài (3b) một tiếng trầm; **hàng rào 1909** (3f) nốt treo | Never Dying → Lightless Dawn |
| V Đường băng + chiến tranh | 472–586 | M-Máy (ebbing → chugging thấp) | toan tính → sơ tán → **vắng** → khối lượng | đường băng lấn vịnh (4c); SM3 sơ tán; **KB1943 = chỗ nhỏ nhất của phim** (cello độc tấu); 7/11/1942 | Undertow → Echoes → Juggernaut (mở) |
| VI Cổng 1969–2026 | 586–698 | M-Cổng trở lại | đóng (lạnh) → người qua lại → giấy tờ (pulse máy) | **6/1969 chắn hạ** (5a) cắt nhạc còn 1 nốt; 1985 mở; hiệp ước 2026 | Intervention (giai điệu trở lại) |
| VII Kết | 698–761 | M-Nhớ (cello) + M-Cổng | gom các tuyến → **KA2026** → quay về nửa đêm | 5j chồng tuyến 1704/1730/1909/1941: mỗi tuyến một nhịp | Hiraeth; 4 nốt M-Cổng ở 5k để đóng vòng |

**Luật đề xuất cho bản không lời** (để K xem nếu thành luật):
- Không duck. LRA đích 6–9 LU (bản có lời: 3,1).
- Đoạn nhỏ nhất ≥ −24 LUFS-S, để không phạm A5 (< −50).
- Mỗi ≤ 90 s phải đổi kết cấu (tầng, nhịp hoặc nhạc cụ), tránh lặp lại bài học "nhạc một bản đều".
- Mọi **thẻ chương §13.3** rơi vào phách mạnh, có pre-lap 1 ô nhịp.
- Mọi **mốc đinh** có một biến cố nhạc trong ±0,5 s.
- **Không lặp đoạn bài** (Q28). Với K1, B đã đủ độ dài: tổng đoạn dùng 764 s; Juggernaut có 3 đoạn không chồng.
- **Lớp âm thanh môi trường** (sóng, gió, pháo xa, máy bay; Freesound CC0, §11.5) đặt dưới nhạc 6–10 LU, gánh "nơi chốn". Thuộc phiên âm thanh.

**Rủi ro riêng của bản không lời:**
- Bản này chỉ có nhạc trên hình, nên hệ Smart Content ID của Scott Buckley khớp rất mạnh. Ghi công trong mô tả là bắt buộc (§7).
- Thời lượng nghe nhạc trần dài làm lộ chỗ giao bài: phải nắn theo vạch ô nhịp, không giao theo giây.

---

## 7. Rủi ro Content ID và giấy phép
| Nguồn | Giấy phép | Content ID | Biện pháp |
|---|---|---|---|
| Kevin MacLeod (K2-MUS-1…5) | CC BY 4.0 (incompetech: "No charge. Requires that you credit the music."; FAQ: "for YouTube videos? Yes, AND you can monetize the videos. Be sure to credit me.") | Có ISRC (K2-MUS-1…4; K2-MUS-5 chưa tra). Rủi ro chính là **bên thứ ba claim nhầm**. FAQ incompetech: ISRC dùng để "respond with this number to show where the track came from". Phiên không đọc được trang "YouTube Content ID" của incompetech, nên **không khẳng định** MacLeod có hay không đăng ký Content ID | ghi công đúng mẫu RIGHTS; giữ ISRC; tranh chấp claim nhầm |
| Scott Buckley (NT3-1…8) | CC BY 4.0, thương mại + phim ngoài mạng ✓ (bảng Licensing) | **CÓ đăng ký.** "I have implemented a 'Smart Content ID' system … This system scans the description of videos using my music looking for a credit. If no credit is found, the system places a copyright claim on the video." Claim đúng mang tên "We Are Era Music BV, claimed on behalf of Scott Buckley". Đã biết có claim nhầm từ "Sentric Music Publishing" | (1) ghi công **trong mô tả** trước khi đăng, có chuỗi "Scott Buckley" đúng chính tả; (2) bị claim thì dùng "Claim Release Form" (≤ 1 ngày làm việc) và tranh chấp trong Content ID để giữ doanh thu tạm; (3) Sentric thì chọn đúng mục trong form |
| Bản không lời | như trên | rủi ro claim **cao hơn** (nhạc trần) | như trên; kiểm claim 24 h sau đăng |
| Bán phim (ngoài YouTube) | CC BY cho phép (Film – other than online ✓) | không có cơ chế Content ID; rủi ro nằm ở ghi công | ghi công trong credit cuối phim + trang bán |
| Ràng buộc lên kênh | Buckley: "cannot be submitted to audio fingerprinting services … via music distribution services" | — | **không đưa nhạc phim, bản không lời hay soundtrack lên DistroKid, Spotify…**; không đăng ký Content ID cho video có nhạc này |

- Không bài nào có NC, ND hay SA.
- Không dùng YouTube Audio Library.
- Không dùng nhạc AI.

---

## 8. Quyết định đề xuất
**Đề xuất: B, sau khi chủ dự án nghe mù xác nhận.** Nếu cặp 2 (pin nổi) hoặc cặp 1 nghiêng về A thì giữ A cho đoạn đó (B là khung, có thể thay từng cue).

| | **A — chỉ thư viện có sẵn** | **B — có sẵn + 8 bản Scott Buckley** |
|---|---|---|
| Ưu | 0 việc giấy tờ mới (đã có RIGHTS, assets); quen tay quy trình; Content ID ít rủi ro hơn (không có hệ quét tự động đã biết); Half Mystery giữ motif kênh từ T1 | đúng thể loại tài liệu lịch sử hơn (dàn dây, cello, kèn đồng so với synth); có **cung kịch tính thiết kế** cho đỉnh 2m (dựng → đỉnh → tắt, cắt ghép đúng phách); motif "cổng" mở/đóng vòng khớp kết cấu lời (0a ↔ 5k); hai tấm im lặng có nhạc cụ độc tấu (cello) thay vì pad; duck đều, sâu nhất −16,5 dB; một tác giả nên âm sắc liền mạch |
| Nhược | 5 bài synth cho 1704–1942 dễ nghe "hiện đại/công nghệ"; Tyrant phẳng (LRA 0,4) chiếm 207 s; đỉnh 2m phải hạ nhạc 20,5 dB (nguy cơ bơm), và duck cố định thì trượt min (10,9 dB); Beauty Flow ở ch5 có nguy cơ thành "nhạc doanh nghiệp" | cần hạ thêm 2–3 dB suốt phim (dàn dây dày): có thể giảm bằng `intensity: low` khi trộn thật; 9 bài, trong đó 8 bài cần dòng RIGHTS mới và đường lưu tệp (≈ 110 MB MP3 gốc; xem cách lưu dưới bảng); Echoes chỉ dùng 8,8 s |
| Tác động | trộn thật ngay được bằng `music.py` | phiên P thêm RIGHTS (NT3-1…8 → K2-MUS-6…13) + assets; music.py dùng được ngay sau đó; mô tả YouTube thêm 8 dòng ghi công |
| Rủi ro | khán giả đánh giá nhạc "rẻ" hoặc lệch thời kỳ; nhạc một bản đều (BAI-HOC-LL lô 6–8) | **Content ID tự động**: quên ghi công là bị claim ngay → biện pháp bắt buộc §7; claim nhầm Sentric; tác giả đổi giấy phép về sau (CC BY 4.0 không thu hồi được với bản đã tải; giữ bản trang giấy phép trong `giay-phep/` + SHA tệp) |

**Hai việc nhỏ nên làm khi trộn thật (cả A và B):**
1. Nắn mọi điểm giao về vạch ô nhịp (`music.py align: bar`). Với B, dời giao S2N → Katabasis ở 173,08 s sớm hơn 1 ô nhịp, để bỏ cửa sổ 13,9 dB khi duck cố định.
2. Giữ `tang` ở hai tấm im lặng (nhạc ≈ −16…−18 LUFS). Khai A10 "khoảnh khắc nhạc".

**Về kích thước assets:** 8 MP3 Buckley ≈ 110 MB (8,9–23,6 MB mỗi tệp).
- `assets/k2/music/*.mp3` hiện có (13–17 MB) nằm trong **git thường, không LFS** (`git check-attr`: filter unspecified). Các tệp này được commit trước khi có luật.
- Hiện nay preflight chặn tệp > 5 MB ngoài LFS cho phép, và LFS đã vượt hạn miễn phí (§11.6).
- Phiên P cần chọn một trong ba cách:
  - (a) chỉ lưu **đoạn bài dùng**, mã hoá lại ≤ 5 MB/tệp (B dùng tổng 764 s; mỗi đoạn ≤ 156 s ≈ 3,7 MB ở 192 kb/s). Ghi rõ là bản trích, kèm SHA của tệp gốc.
  - (b) giữ tệp gốc ngoài git, ghi SHA + URL; tải lại khi dựng.
  - (b′) thêm vào `tools/lfs-allow.txt`: tốn LFS.
- Đề xuất **(a)**.

---

## 9. Việc chờ chủ dự án
1. **Nghe mù 4 cặp** trong `reports/nhac-t3/nghe-mu/` (≈ 2 phút 15 giây, cả X lẫn Y), chấm theo `HUONG-DAN-NGHE.md`, **rồi mới mở** `khoa.json`.
2. **Chọn A, B, hay trộn** (B làm khung, thay từng cue). Ghi vào `AUTHORSHIP.md`, kèm đóng góp biểu đạt: lựa chọn cảm xúc từng đoạn và bài cho từng đoạn.
3. **Nếu chọn B:** duyệt đưa 8 bài Scott Buckley vào `RIGHTS.md` (đề xuất mã K2-MUS-6…13) và `assets/k2/music/`. Duyệt mẫu ghi công có "(edited)" (§2.2) và cam kết ghi công trong mô tả trước khi đăng (§7).
4. **Xác nhận thời lượng thẻ phương pháp** (giả định 2 × 8 s sau 745,0 s), hoặc chuyển câu hỏi này cho phiên P.
5. **Bản không lời:** chọn K1 (giữ hình 745 s) hay K2 (≈ 636 s), khi tới lượt làm (§6).
6. **Việc của phiên P (không phải chủ dự án):**
   - lưu bền stem FLAC lời G1 (KL42 §6, đã mất ở container KL42; cần thu lại hoặc lấy từ nơi lưu nếu có), rồi đo lại SMR trên stem thật;
   - merge `k2c-t3-kl42` trước khi phiên trộn dùng `nhip-that.json`;
   - merge `nhac-t3` khi chủ dự án duyệt.

## 10. Tệp (`reports/nhac-t3/`)
- **Hồ sơ:** `NHAC-T3-BAO-CAO.md`, `CHECKPOINT.md`.
- **Cue sheet:** `cue/cue-A.json`, `cue/cue-B.json`.
- **Ứng viên và giấy phép:** `nguon-moi.json` (8 bài: URL, SHA-256, điều khoản, ghi công, Content ID; 5 bài loại + SHA); `giay-phep/scottbuckley-using-this-music.txt`, `scottbuckley-licensing.txt`, `scottbuckley-copyright-claims-release.txt`, `scottbuckley-tung-bai.txt`, `incompetech-faq.txt` (trích văn bản trang, ngày đọc 19/10/2026).
- **Số đo:** `so-do/dac-tinh-cue.json` (18 bài × hồ sơ 5 s), `so-do/smr-ca-phim.json`, `so-do/tron-ca-phim-{A,B}.json`, `so-do/tron-ca-phim-{A,B}-duck-co-dinh.json`, `so-do/tron-{A,B}-{moc,pin}.json`.
- **Gói nghe:** `nghe-mu/` (8 MP3, `khoa.json`, `HUONG-DAN-NGHE.md`).
- **Công cụ:** `cong-cu/do_cue.py`, `dat_loi.py`, `tron.py` (gọi `scripts/audio/master.py`, không sửa), `bang_so.py`, `goi_nghe.py`.
- **Ngoài git** (vùng tạm, mất khi container thu hồi; tạo lại được bằng công cụ trên nếu có MP3 nguồn):
  - 13 MP3 Buckley tải về; SHA trong `nguon-moi.json`, tải lại được từ URL;
  - 6 WAV trộn thử (2 bản cả phim × 2 kiểu duck + 4 đoạn).
