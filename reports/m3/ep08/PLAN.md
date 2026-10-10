# PLAN tập 08 — The Translator's Desk  (≤ 1 trang; P cập nhật sau mỗi bước)

**Trạng thái:** G2 DUYỆT có điều kiện 10/10/2026; điều kiện đã làm (T01, Q31 vòng 3, chỉ Short S2). Phát hành `release-ll-ep08-v1` @ `67bfc2e` (9/9 SHA OK). Chờ G3.
**Đã làm (sau G1 v2):** 1. đặc tả v2 (map, heroes, numbers, anchors `w250`/`frey`/`it_chg`) + `design/ll-hero/ep08.js` (6 cảnh đinh); 2. kiểm trước build: `ll.py check` (Q26b), `tests/run.sh`, `node --check`, `hero.js --only`; 3. bộ đếm ElevenLabs → thu giọng → bộ đếm; 4. nháp 960×540, một lượt sửa; 5. 1080p một lần; 6. QC Q1–Q31 + Q26b + LOCK, Q27 chính thức; 7. G2.
**Quyết định đã có (chủ dự án):** 06/10/2026 — lệnh lô 6–8 (HÌNH v2 từ đầu, Q14–Q22 bắt buộc, kiểm mù 1 subagent 3 vai, trần token theo đầu vào mới + sinh ra). Chi tiết ở AUTHORSHIP.md.
**Trần:** token 1,5 triệu/tập sản xuất trọn (đầu vào mới + sinh ra, đo từ log phiên; > 25 % thì dừng hỏi) · đĩa trống ≥ 1,5 × mức cần
**Tiêu đề (chủ dự án duyệt G1 v2):** "From Headphones to Machine Drafts: How Translators' Work Changed".

**Luật mới từ G2 tập 7 (chủ dự án, 09/10/2026) — áp ngay từ đặc tả tập 8:**
- Không bối cảnh 3D nào > 25 % thời lượng hay > 90 s liên tục; nửa sau phim có ≥ 2 bối cảnh khác nhau (ban ngày / cận cảnh / nơi người mới học nghề) — BAI-HOC #96.
- Nội thất chi tiết hơn, ít khối thô và tối (vân vật liệu, đồ vật, ánh sáng có nguồn, tương phản, chiều sâu) — BAI-HOC #97.
- ElevenLabs: kiểm bộ đếm trước/sau mỗi build (tập 7 lệch 1 814 ký tự không giải thích được) — BAI-HOC #98.
- Prep bản cuối (có ASR) chạy riêng một lần, kiểm `el_sent` = 0 trước khi dựng cảnh đinh — BAI-HOC #95.

**Phiên sau đọc (≤ 8 tệp):**
1. `reports/m3/BAI-HOC-LL.md`
2. `reports/m3/CHUAN-KENH-LL.md` (§3, §5, §7–9)
3. `reports/m3/ep08/episode.yaml`
4. `reports/m3/ep08/NGUON-TAP8.md`
5. `reports/m3/ep08/PLAN.md` (tệp này)
6. `scripts/ll/README.md`
7. `reports/m3/LO-6-8-G1.md`

## Cải thiện hình
Lý do: Q27 tập 7 đạt sát ngưỡng (5,68 vs 5,64, chênh +0,04). Người chấm mù ở mọi lần đều trừ điểm nội thất 3D khối thô, tối và thẻ giấy dựng dở.
- **Nội thất 3D chi tiết hơn, sáng hơn:**
  - vân vật liệu (gỗ, ô sàn, thảm), đồ vật trên bàn;
  - ánh sáng có nguồn (cửa sổ, đèn bàn), tương phản rõ, chiều sâu;
  - tránh vùng tối đặc;
  - làm từ cảnh đầu tiên, không đợi chấm mù (BAI-HOC #97).
- **Không bối cảnh nào > 25 % thời lượng hay > 90 s liên tục** (Q26b, checks LL v3 1.8.1). Kiểm ở đặc tả trước khi dựng nháp. Tập 7 bản cuối: tower 139,1 s, pool 104,3 s, TRƯỢT nếu áp (BAI-HOC #96).
- **Nửa sau phim có ≥ 3 bối cảnh khác nhau** (ban ngày / cận cảnh / nơi người mới học nghề …).
- **Thay thẻ giấy dựng dở bằng cảnh hoàn chỉnh:** không để khung nào là thẻ trống hoặc biểu đồ đang vẽ dở. Số đặt trên cảnh vật chất đã đẹp (BAI-HOC #87).
