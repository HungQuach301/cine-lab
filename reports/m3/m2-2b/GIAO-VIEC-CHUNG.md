# Animatic v3 — quy ước chung cho 3 xưởng (P giao, 01/10/2026)

## Ràng buộc
- KHÔNG đọc hay sửa `checks/`. KHÔNG sửa `bible/` hay tài sản khoá. KHÔNG gọi ElevenLabs (P đã thu đủ giọng). KHÔNG push nhánh nào.
- Trong worktree của bạn:
  - tạo nhánh cục bộ `ep01-<gói>` từ `lat-cat-m22a` (commit 3f69e79, mã lát cắt đã duyệt làm chuẩn kênh);
  - mã mới đặt ở `design/m3/ep01/<gói>/`;
  - liên kết `ln -s /home/user/cine-lab/design/cong3/shared/node_modules design/cong3/shared/node_modules` (không commit liên kết).
- **Commit cục bộ sau MỖI đoạn xong.** Ghi tiến độ vào `/var/tmp/cine-out/ep01/<gói>/TIEN-DO.md` (container có thể khởi động lại; đĩa còn).
- Cuối gói xuất bản vá: `git diff lat-cat-m22a HEAD --binary > /var/tmp/cine-out/ep01/<gói>/ma-<gói>.patch`.
- **Render dài:**
  - chạy `setsid nohup … > log 2>&1 < /dev/null & disown`;
  - chờ bằng `timeout 580 tail --pid=<pid> -f /dev/null` (lệnh Bash tối đa 10 phút; lặp lại nếu cần);
  - tối đa **2 tiến trình render** cùng lúc mỗi gói (máy 4 vCPU dùng chung 3 gói).
- Có thể không ghi được tệp .md trong repo: trả toàn bộ báo cáo trong lời trả về.

## Đầu vào
- **Dòng thời gian thật:** `/home/user/cine-lab/reports/m3/m2-2b/timeline-v3.json`.
  - Mỗi đoạn có `t0`, `dur`, `khung` = [khung0, khung1), `vo_file`, `vo_offset`, `ida`.
  - Mốc câu tuyệt đối = `t0` + `vo_offset` + mốc ký tự trong `*.align.json`.
  - Đoạn 19 có phần B lùi thêm `chen_lang_s`.
  - Khối 10–13 dùng align của lát cắt, lệch +1,0 s.
- **Lời dẫn và mốc ký tự:** `/home/user/cine-lab/reports/m3/m2-2b/vo/bill-NN.mp3` + `.align.json`; văn bản `v31-loi-dan.json`.
- **Kịch bản v3.1:** `/home/user/cine-lab/reports/m3/KICH-BAN-TAP-THU-V3.md`. Dùng các mục: §3 Visual/Data từng đoạn; §6 bảng số (§6.1 HSUS); §9.1 tài sản; §12 sửa v3.1.
- **Chuẩn kênh (LUẬT CỨNG):** `/home/user/cine-lab/reports/m3/CHUAN-KENH-LL.md`. Đọc hết §3 luật so sánh 6 điểm, §5 chuẩn kỹ thuật, các luật mới ở §5.1.
- **Mã chuẩn kênh (lát cắt M2.2a, đã duyệt):** `design/m3/lat-cat/` trên nhánh `lat-cat-m22a`:
  - `dohoa.js` + `dohoa_render.js`: canvas2D vẽ lại mỗi khung, FFV1, motion blur khung con, giấy B3, ánh rọi, bụi;
  - `story_shot.js`: shot three.js br10 (sương, quầng rung, hạt);
  - `tuong_phan.py`.
- Báo cáo lát cắt: `/home/user/cine-lab/reports/m3/M2-2A-LAT-CAT.md`.
- Khung mẫu: `/home/user/cine-lab/reports/m3/m2-2a/khung/*.jpg`.
- **Giữ đúng ngôn ngữ hình của lát cắt.**

## Hợp đồng đầu ra
- **Mỗi đoạn một tệp** `/var/tmp/cine-out/ep01/sec/<NN>.mkv`:
  - FFV1, 1920×1080, 24 fps, không tiếng;
  - **đúng số khung** khung1 − khung0 của đoạn;
  - kèm `<NN>.timing.json` (giây/khung).
- **Chuyển đoạn:** clip tự làm 4–8 khung đầu và cuối (mờ từ/về nền tối, hoặc biến hình liền). **Không được có ≥ 2 khung giống hệt nhau** ở bất kỳ đâu, kể cả khung đen.
  - Tự chạy `python3 /home/user/cine-lab/scripts/p/judder.py <NN>.mkv`. Mục tiêu `loi == 0` **và** `giu_co_y_ge_1s == 0`. Nếu buộc phải đứng yên ≥ 1 s thì khai lý do.
- **SFX:** đặt cue vào `/var/tmp/cine-out/ep01/sfx/<NN>.json`, dạng danh sách `{file: đường dẫn tuyệt đối, src_ss, dur, at_abs (giây tuyệt đối trong tập), gain_db, fade_ms, rights}`.
  - Dùng lại M2-SFX-1/2/3 (`/var/tmp/cine-out/m22a/sfx/{320149,159386,470189}.mp3`).
  - SFX mới CHỈ CC0 do người làm (Freesound preview HQ). Mở trang, xác nhận "Creative Commons 0", ghi số/tên/tác giả/URL/SHA-256.
  - P mix, không cần bạn mix.

## Luật hình (kiểm từng khung số)
1. Luật so sánh 6 điểm.
   - Thực tế: nét liền, nhãn ACTUAL. Dự báo: gạch chéo + viền nét đứt + PROJECTION + kỳ.
   - Không chung trục số London với số BLS. Trục từ 0.
2. **Không khung đồ hoạ nào đứng trống quá 3 s khi lời dẫn đang nói.** Mỗi câu có hình gắn đúng nội dung câu.
3. **Hình không đi trước lời:** phần tử gắn với một từ xuất hiện từ mốc bắt đầu từ đó trở đi (sớm tối đa 0,1 s).
4. **Số trên hình khớp lời đọc**, cùng gốc, cùng phân loại.
   - Chuỗi thang máy (lỗi L2): theo bảng §6.1, **ngắt đường ở chỗ đổi phân loại và ghi chú** ("1960 classification" / "1970 classification").
   - Phải hiện được gốc 94k cho phép so 1950–60 (−18 %) của đoạn 14, và 97k khi lời nói "nearly a hundred thousand by 1950".
   - Áp nhất quán ở đoạn 08, khối 10–13 (G1) và đoạn 14.
5. Nhãn, thẻ chữ không đè ô thu nhỏ hay mép biểu đồ (L3). Ghép hai đợt dự báo: vạch ngăn rõ + nhãn đợt + 2 dòng nguồn (L4).
6. Tương phản chữ ≥ 4,5:1; đo trên chính clip.
7. **An toàn mù màu:** không mã hoá nhóm chỉ bằng màu. Dùng thêm gạch chéo hoặc nét, nhãn chữ, vị trí.
8. Không cận mặt người. Chữ trên hình tiếng Anh. Font DejaVu (C4-F1, M2-F-*).
9. Đồ hoạ: 24 khung/giây thật, easing, toạ độ điểm ảnh con, motion blur khi nhanh, giấy lay, ánh rọi, bóng; không dán phẳng.

## Báo cáo trả về
- Danh sách đoạn đã xong, số khung khớp hay không, judder từng đoạn, tương phản thấp nhất.
- Giây render/khung (mean/max) tách cảnh truyện và đồ hoạ.
- Chữ trên hình mới do bạn đặt (kịch bản chưa có), để chủ dự án duyệt.
- Dòng RIGHTS đề xuất.
- Chỉ số trong ±5 % quanh ngưỡng.
- Token tự ước; commit cuối.
