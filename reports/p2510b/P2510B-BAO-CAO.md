Nhánh thật: **`ccr-d463992e-9fq13a`**. Harness buộc tên này; lệnh ghi `p-2510b`. Gốc `origin/main` @`2a49e3ca`, đúng gốc lệnh. `main` được cập nhật bằng fast-forward lên đỉnh nhánh này (commit "… DỪNG chờ chủ dự án").

# P-2510b — Kinh thánh và sổ cho gói "50 % tiết kiệm" + phiếu NC-T4 P1–P10, gộp NC-T4 vào main. BÁO CÁO. DỪNG chờ chủ dự án

## §0 Điều lệ phiên và tóm tắt
| Trường | Lệnh | Thực tế |
|---|---|---|
| Nhánh | `p-2510b` từ origin/main @2a49e3ca | harness buộc `ccr-d463992e-9fq13a` (ghi ở dòng đầu); gốc đúng 2a49e3ca |
| Song song | ANIMATIC-T4-V2, K-1.17.7: không đụng | không fetch, không đọc, không sửa nhánh của họ. Diff phiên không chạm `checks/`, `checks-appeal.md`, `scripts/`, `design/`, `tools/` |
| Vùng sửa | docs/BIBLE-KENH2.md, AUTHORSHIP.md, RIGHTS.md, COST-LEDGER.csv, channel-k2/BAI-HOC-K2.md, QUYET-DINH-TREO (chỉ thêm mục cuối), reports/p2510b/**, main | đúng. Ngoài merge, phiên đổi 6 tệp sổ/Kinh thánh + `reports/p2510b/**` (`git diff --name-only 2a49e3ca HEAD` trừ phần merge). `channel-k2/k2c-t4-02/nc/**`, `scripts/k2ldn/nc/**`, `reports/nc-t4/**` chỉ đổi qua merge |
| Chi phí | API 0; giờ máy mốc 1,5 h | Claude API / OpenAI / Gemini / ElevenLabs / RunPod / YouTube **$0**, không gọi lần nào. 0 tác tử phụ. Không tải LFS, không gọi mạng ngoài git. Giờ máy ≈ **0,3 h** (02:33 → ≈ 03:00 UTC), phần lớn là selftest |
| Preflight | `set -o pipefail`; chỉ commit khi có "— ĐẠT" | `reports/p2510b/cam_commit.sh` chỉ commit khi có cả "— ĐẠT" và "PREFLIGHT ĐẠT"; hook pre-commit chạy lại. Mọi commit ĐẠT |
| Hook | cài trước lần đẩy đầu | `pre-commit` + `pre-push` → `tools/preflight.sh`, cài 02:33 UTC; lần đẩy đầu 02:36 UTC |
| Force / amend | không | 0 force, 0 amend |
| Email / UA / khoá | che; không đưa email chủ dự án vào tệp | git dùng noreply. Diff `2a49e3ca..HEAD` có **0** chuỗi email chủ dự án. Không gọi HTTP nên không có UA; không đọc, không in khoá |
| `lock.py` | chỉ `--verify` | chỉ `python3 -I checks/lock.py --verify` (trực tiếp và qua preflight); mọi lần **KHỚP 1.17.6 `513c9442…`** |
| Tiến trình nền | PGID, một vòng nặng một lúc, P ≤ 2, RAM ≥ 5 GB, kiểm đĩa | selftest chạy nền bằng `setsid nohup` (PGID 1953; tệp `st1.pgid` trong scratchpad ghi nhầm PID 1951 của subshell — phiên kiểm lại bằng `ps -eo pid,pgid`); chờ bằng vòng `grep "== tổng"`; không `pgrep/pkill -f`. 1 lượt nặng duy nhất. RAM trống 15 GB, đĩa trống 15 GB |
| Đẩy ≤ 30 phút + CHECKPOINT | bắt buộc | đẩy 02:36, ≈ 02:41 và lần cuối; `reports/p2510b/CHECKPOINT.md` |
| Đầu vào ở /var/tmp | không chỉ để ở đó | phiên không tạo tệp ở /var/tmp. Phát hiện: đầu vào NC-T4 ở /var/tmp đã mất (§3 K79) |
| Lệnh bổ sung | ghi vào CHECKPOINT | không có |
| Đã đọc | — | BAI-HOC-LL (khởi động), P2510-BAO-CAO (khuôn), NC-T4-BAO-CAO, PHIEU-NC-T4, NHAN-VAT-ANH, TU-LIEU-1940 §3, §6, FOOTAGE-2026 §1, §3–§6, `loi-moi-nhap.json`, `nhan-vat-anh.json`, `tu-lieu-1940.json`, `footage-2026.json`, `nguon/web/footage-licence-webfetch.txt`, Kinh thánh §13, §15, §19, QUYET-DINH-TREO mục F. Không đọc mã trong `checks/` |

**Tóm tắt**
1. **Merge `--no-ff` NC-T4, 0 xung đột.** Đỉnh `origin/k2c-t4-02-nc` trùng SHA lệnh `d2279bbb`. LOCK **1.17.6 `513c9442…` KHỚP**; selftest 15/15 bộ đạt, trong đó **k1176 62/62, k2 129/129, ll 317/317** (§1).
2. **Kinh thánh `dbafce00…` → `08cc1da9…`** (+5 / −1 dòng): §15 (d) gói 50 % (góc cao ≥ 50 % + 5 chốt, Gemini $55/$50, kiểm 2 mức, 720p không dự trữ, 1 clip/2 shot); §15 (f) nới hẹp P2 (b); §19 (c) T4 ≤ 20 % + lớp THAT + footage không share-alike + LOẠI Mason/phim 1940. Luật kiểm trỏ tới RULES-LL 1.17.7 (đang làm) (§2).
3. **Sổ (chỉ thêm, xoá 0 dòng):** AUTHORSHIP +5, RIGHTS +66 (mục NC-T4), COST-LEDGER +2 (NC-T4, P-2510b), BAI-HOC-K2 K76–K80, QUYET-DINH-TREO mục G (§3).
4. **Phát hiện khi ghi RIGHTS:** NC-T4 viết rằng bằng chứng giấy phép nguyên văn nằm ở `nc/licenses/<id>.json` cho 21 tệp ảnh, nhưng **0/21 tệp đó có trong git**. Gốc ở `/var/tmp/nc-t4/` đã mất cùng container. Câu giấy phép, URL và SHA gốc còn trong `reports/nc-t4/nhan-vat-anh.json`, và RIGHTS tạm trỏ về tệp này. Trước bản cuối cần tải lại bằng `scripts/k2ldn/nc/tai_nc.py` (K79, QUYET-DINH-TREO G).
5. **main `2a49e3ca` → đỉnh nhánh** bằng fast-forward. Ngay trước khi đẩy, phiên fetch lại và kiểm main vẫn ở 2a49e3ca; không force (§4).

## §1 Merge
| Nhánh @SHA (khớp lệnh) | Commit merge | Số tệp | Vùng | LOCK sau merge | selftest |
|---|---|---|---|---|---|
| `origin/k2c-t4-02-nc` @`d2279bbb` (NC-T4) | `79cfe7ad` | 95 (+18 916 / −0) | reports/nc-t4 (66), channel-k2/k2c-t4-02/nc (24: 21 ảnh + SHA256-NC + 2 trang Hooke), scripts/k2ldn/nc (5). Không chạm checks/ | **1.17.6 `513c9442fe1cb9950bdf01c3be4dc93b32c4413d9260109c86f0f5d90e5b8ec3` KHỚP** | 15/15 bộ (`selftest-1.txt`) |

Kết quả selftest: k112 75/75 · k1121 48/48 · k1122 37/37 · k113 64/64 · k114 126/126 · k115 105/105 · k116 144/144 · k117 130/130 · k1172 74/74 · k1173 42/42 · k1174 91/91 · k1175 52/52 · **k1176 62/62** · **k2 129/129** · **ll 317/317**. Mọi bộ thoát mã 0; số khớp lượt P-2510.

## §2 Kinh thánh `docs/BIBLE-KENH2.md`
- **SHA-256 trước:** `dbafce006693054069019ccb6597ca787d15a6c03bedb7a4ffedb55a82b6772a` (main @2a49e3ca).
- **SHA-256 sau:** `08cc1da97abfc9c364e1a0fe1ae3ff9b72768aa8667774b74c02b2daafb0b6be` (commit `f05c05b0`), +5 / −1 dòng. Dòng duy nhất bị đổi là dòng tiêu đề.
- Diff đủ ở `reports/p2510b/bible-diff.txt`. Script `reports/p2510b/sua_bible.py` kiểm mỗi neo xuất hiện đúng 1 lần trước khi chèn.
- Mỗi đoạn mới ghi "(duyệt 25/10/2026 09:15, nguyên văn; căn cứ 08:15, 08:21, 09:08)". Phần luật đo chỉ trỏ tới `checks/ll/RULES-LL.md` mục **1.17.7 (đang làm)**; tới khi LOCK 1.17.7 khoá, bộ kiểm hiện hành vẫn là 1.17.6. Kinh thánh không chép luật.

| Chỗ | Thay đổi |
|---|---|
| Tiêu đề | thêm "; sửa §15 (d)(f), §19 (c) theo gói "50 % tiết kiệm" + phiếu NC-T4 P1–P10 (duyệt 25/10/2026 09:15) (P-2510b)" |
| §15 (d) | thêm dòng "(d) cập nhật 25/10/2026 09:15 — gói "50 % tiết kiệm"":<br>(1) **Góc cao T4 ≥ 50 %** (thay 60 %) + 5 chốt: (i) chương mở/kết góc cao; (ii) P1 tái xuất mỗi hồi; (iii) ≤ 2 shot thấp/cận/M-d/ảnh thật liền nhau; (iv) mỗi chương ≥ 40 %; (v) TL-1 mục tiêu 60 %. Phân bổ ≈ 80 s = 25 s ảnh/tư liệu thật + 15 s 3D tầm phố + 40 s Omni. Ghi lý do 09:08.<br>(2) **Gemini T4 $55 / mốc $50** (khai `ngan_sach_gemini_moc_usd: 50`).<br>(3) **Kiểm 2 mức:** ĐỦ ≤ 3 lượt (công trình/nhân vật có tên, chân trời, dữ kiện); NỀN = Flash + soi khung, ≤ 2 lượt, bỏ qua lỗi nhỏ hậu cảnh; **không bỏ lỗi lớp dữ kiện (a)**.<br>(4) 720p chỉ sinh lại lệnh đã đạt ở 360p, không dự trữ.<br>(5) 1 clip M-d dùng tối đa cho 2 shot. |
| §15 (f) | thêm dòng "(f) nới hẹp từ T4 — nhân vật lịch sử có tên (P2 = (b))":<br>- dựng được ở khung trung/xa, không cận mặt;<br>- trang phục/tóc giả/dáng theo chân dung thật làm tham chiếu, không đưa mặt vào lệnh;<br>- chủ dự án duyệt từng clip;<br>- Hooke chỉ thẻ chữ; Bludworth, Barbon, Allen, Holden, Holford, Matthews cũng chỉ thẻ chữ (không có bản sạch quyền);<br>- phần còn lại của (f) giữ; clip loại này kiểm mức ĐỦ. |
| §19 (c) | thêm đoạn "(c) cập nhật 25/10/2026 09:15 — T4 tư liệu + ảnh/footage thật":<br>(1) T4 trần TL + khắc + thẻ + THAT **≤ 20 %** (`tu_lieu_tran_pct: 20`);<br>(2) lớp THAT không tính AI/góc cao;<br>(3) ảnh thật toàn khung có chuyển động máy là shot hợp lệ; ảnh chồng góc giữ góc của shot nền;<br>(4) không ghép liền Omni;<br>(5) footage hiện đại chỉ giấy phép không share-alike, có bằng chứng ở `licenses/`; T4 chỉ 1 clip đêm H5-07a;<br>(6) ảnh MoI Crown chú thích đúng năm 1941–44; LOẠI "St Paul's Survives" và không dựng lại bằng AI; không dùng phim 1940;<br>"Luật kiểm ở RULES-LL 1.17.7 (đang làm)". |

Ghi chú diễn giải (chủ dự án xem lại nếu chưa đúng ý):
- "TL-1 mục tiêu 60 %": phiên ghi đây là **đích hướng tới, không phải sàn**. §19 (a) luật 4 vẫn còn câu "≥ 75 % … góc cao/toàn cảnh". Với T4, câu này hiểu theo gói: sàn 50 %, mục tiêu 60 %. Phiên **không xoá** câu 75 % cũ; K-1.17.7 sẽ định nghĩa hàng kiểm.
- Dòng "Hàng kiểm mới từ T4 … GOC-CAO-60" ở §13 giữ nguyên. Tên hàng mới do K đặt.

## §3 Sổ đã ghi (chỉ thêm, xoá 0 dòng; commit `9b069ff2`, dòng P-2510b của COST-LEDGER ở commit cuối)

**`AUTHORSHIP.md` (+5 dòng).** Mỗi dòng có nguyên văn, giờ, nghĩa, đóng góp biểu đạt của chủ dự án và phần do AI đề xuất.
- (1) **08:15:** hỏi về ngưỡng 60 %.
- (2) **08:21:** "Nếu giảm hẳn về 50% thì sao". Chủ dự án tự nêu mức 50 %.
- (3) **09:08:** tiêu chí chi phí và độ chân thực. Đây là căn cứ cho kiểm 2 mức.
- (4) **09:15:** duyệt gói và P1–P10, mỗi mục ghi nghĩa (P8 sửa thành 20 %, P10 ≈ $50–52).
- (5) **P3 + P5:** chủ dự án chọn 15 điểm nhấn, và 9 câu lời nguyên văn tiếng Anh cùng câu bỏ N7. Nguồn nháp: `loi-moi-nhap.json`, SHA `7d8e7a03…`, 868 ký tự.

**`RIGHTS.md` (+1 mục, 66 dòng).** Sinh bằng `reports/p2510b/ghi_rights.py` từ 3 tệp JSON của NC-T4.
- **21 dòng `T4-NC-*`** (6 chân dung, 15 ảnh/bản vẽ 1850–1930). Mỗi dòng có:
  - câu giấy phép nguyên văn và URL;
  - SHA gốc và SHA bản thu trong git.
- **Chờ duyệt riêng:** Pepys, James, Churchill.
- **5 dòng ảnh MoI Crown C01–C05:** chưa tải, chú thích phải ghi đúng năm (1940/1941/1/1942/1944).
- **LOẠI:**
  - Mason: C12, C13, C14;
  - ảnh ghép C06;
  - phim 1940: *London Can Take It!*, *Christmas Under Fire*;
  - footage CC BY-SA: C4, C5, C6, C7, C9.
- **Footage ứng viên cho H5-07a:** X1 (Pixabay, ứng viên chính), P3 và P4 (Pexels), C3 (Commons CC BY 3.0, giấy phép đã được bot xác nhận). C1 chỉ tham chiếu (skyline 2016).
- **Pexels/Pixabay ghi rõ "CHƯA ĐỐI CHIẾU BẢN GỐC"** (curl 403, chỉ có trích qua WebFetch). Chủ dự án lưu PDF vào `licenses/` trước khi chọn clip.
- Văn bản nguồn chỉ dùng làm dữ kiện, kèm ghi chú lỗi ngày của trang St Paul's.

**`COST-LEDGER.csv` (+2 dòng).**
- **NC-T4:** Claude API $0 (mốc $2); tác tử phụ ≈ 603 nghìn token trong phiên; các nhà cung cấp khác $0; giờ máy ≈ 0,9 h (§11 của báo cáo NC-T4).
- **P-2510b:** API 0; giờ máy ≈ 0,3 h.

**`channel-k2/BAI-HOC-K2.md` (K76–K80).**
- **K76:** kiểm câu trích bằng máy, 43/43.
- **K77:** trang 403/429 không vượt rào; tài sản dựa trên trang chưa đối chiếu chỉ lên hình sau khi có PDF.
- **K78:** nguồn cơ quan cũng có lỗi ngày. St Paul's "Our timeline" ghi "September 3rd 1666"; ngoài ra lệch 1708/1710 và lệch người đặt viên đá năm 1675.
- **K79 (mới):** bằng chứng được nhắc trong báo cáo nhưng không vào git (0/21).
- **K80 (điều phối):** quyết ngưỡng theo chi phí: lấp chỗ trống bằng tư liệu thật miễn phí trước, rồi 3D có sẵn, AI sau cùng.

**`reports/k1173/QUYET-DINH-TREO.md` (mục G, chỉ thêm ở cuối).**
- **Đã quyết:** gói 50 %, P1–P10, và dòng NC-T4 còn treo ở mục F.
- **Còn treo:**
  - K-1.17.7;
  - ANIMATIC-T4-V2;
  - duyệt từng clip nhân vật có tên;
  - chân dung duyệt riêng;
  - PDF giấy phép footage;
  - 21 JSON bằng chứng;
  - tải ảnh Crown;
  - đo lại BMN ≥ 4 px/m và hiệu chuẩn BIEN-CO-V trước bản cuối;
  - Đ5;
  - LUAN-2, LOOK-T9c, KN THU-B (giữ như mục F).

## §4 main
- Trước: `origin/main` @`2a49e3ca78899a981237c949e39dd1df0fb76732`.
- Sau: đỉnh `ccr-d463992e-9fq13a`, tức commit cuối "P-2510b: báo cáo … — DỪNG chờ chủ dự án".
- Cách đẩy: `git push origin HEAD:main` (fast-forward, không force). Ngay trước khi đẩy, phiên `git fetch origin main` và kiểm `origin/main` vẫn là `2a49e3ca` và là tổ tiên của HEAD. Nếu main đã đổi, phiên sẽ DỪNG và không ép.
- SHA sau được ghi trong tin nhắn cuối phiên. Báo cáo này nằm trong chính commit đó nên không tự ghi được SHA của mình.

## §5 Chỉ số trong ±5 % quanh ngưỡng (luật cứng)
Phiên P không đo chỉ số hình hay âm. Các số sát ngưỡng dưới đây lấy từ phiên nguồn hoặc từ gói:
- **Thời lượng** (NC-T4 §12): 760,0 s / 780 s.
- **Omni:** 27,98 % / 28 %.
- **M-d mỗi clip:** 8 s / 8 s.
- **Lời mới:** 10 / 10 câu chạm tới.
- **Gemini T4:** ước theo gói ≈ $50–52 so với mốc mới $50 → **sát/vượt mốc theo dõi** (dưới trần $55, 91–95 % trần). Ước $44,81 cũ của NC-T4 tính dự trữ 30 % cho 720p; gói bỏ dự trữ nhưng thêm ≈ 40 s Omni. ANIMATIC-T4-V2 tính lại.
- **Góc cao:** sàn mới 50 %. Ước bố trí A cũ 61,24 % chưa tính 80 s giải phóng. Bố trí mới do ANIMATIC-T4-V2 đo.
- **Trần tư liệu + THAT 20 %:** ước cũ 13,49 % + ≈ 25 s ảnh thật (≈ 3,3 % của 760 s) → ≈ 16,8 %, chưa sát ngưỡng.

## §6 Việc chờ chủ dự án
1. **Duyệt từng clip M-d có nhân vật có tên** (Charles II, James, Pepys, Evelyn, Wren) khi ANIMATIC-T4-V2 trình (§15 (f) nới hẹp).
2. **Chân dung cần duyệt riêng:** Pepys (sau 1685), James (năm chưa rõ), Churchill (1943; câu Churchill đã bỏ nên có thể không cần thẻ).
3. **Mở tay và lưu PDF** trang giấy phép Pexels và Pixabay vào `licenses/`; xem khung X1/P3/P4/C3 rồi chọn 1 clip đêm cho H5-07a.
4. **21 JSON bằng chứng NC:** giao một phiên (xưởng hoặc NC) tải lại bằng `scripts/k2ldn/nc/tai_nc.py` trước bản cuối (K79). Hiện RIGHTS trỏ tạm về `nhan-vat-anh.json`.
5. **Trước bản cuối:** đo lại tấm BMN ≥ 4 px/m (và chiếu 3D sau khi sửa) và hiệu chuẩn BIEN-CO-V trên animatic T4 (K-1.17.7 / phiên K đo lại).
6. Đang chạy song song: **K-1.17.7** (luật cho gói 50 %, THAT 20 %, P2 b, P9) và **ANIMATIC-T4-V2**. Chờ kết quả để P gộp.
7. **Đ5:** quyền giọng G1 cho bản phát hành. Lời mới P5 sẽ thu bằng G1.
8. Diễn giải "TL-1 mục tiêu 60 %" (§2 ghi chú): xác nhận hoặc sửa.

**DỪNG chờ chủ dự án.**
