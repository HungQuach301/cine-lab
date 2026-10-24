# CHECKPOINT — GIONG-T4 (K2C-T4-02 M2: khoá lời + thu G1 + mốc câu)

**Nhánh thật:** `claude/k2c-t4-02-giong-a24udn` (harness buộc; lệnh ghi `k2c-t4-02-giong`). Gốc `origin/main` @ `c6a4772b`. Không merge.

## Trạng thái
- [x] verify.sh (10 ĐẠT, 5 TRƯỢT không dùng tới: OpenEXR, three.js, tifffile/pyshp, k2v node_modules, Freesound) · hook pre-commit/pre-push đã cài
- [x] Đọc BAI-HOC-LL, KL42, PHIEU-G1 + AUTHORSHIP dòng 397 (D3 = GIỮ "burned to the ground twice"), Kinh thánh §3, §12, §14, §19
- [x] Nguồn web cho 22 mục [cần kiểm]: `reports/giong-t4/nguon/*.txt` (bản chữ + SHA gốc; gốc ngoài git `/var/tmp/cine-out/giong-t4/nguon/`, tái tạo: `scripts/k2ldn/giong/tai_nguon.py <mã> <url>`)
- [x] Lời v2: `khoa-loi/sua-v2.json` (27 mục), `doan-shot.json`, `scripts/k2ldn/giong/lam_loi_khoa.py` → `loi-khoa.txt` (1 553 từ)
- [x] KIEM-LOI.md (22 mục; trích máy kiểm khớp)
- [x] Thử phát âm 3 lượt (2 061 ký tự): chỉ Evelyn → alias 'Eevlin'; PLS `london-g1.pls` 6e11cae0…; LOI-KHOA.sha256 3/3 OK
- [x] Thu G1 cả tập: 6 chương, 8 lệnh, 9 061 ký tự (tổng phiên 11 122); bộ đếm 151 745 → 155 731; gốc mp3 + alignment trong git `am-thanh/nguon/` (SHA256SUMS)
- [x] Ghép stem (`gl_ghep.py`): 681,0 s; lời theo shot 633,1 s
- [ ] ASR toàn tập: chạy nền PID 7625 (`gl_kiem_tap.py`, log /var/tmp/cine-out/giong-t4/kiem.log; ASR có cache theo SHA)
- [x] Giãn shot (`gl_gian_shot.py`): K0 ≥ 782 s; K1-C1 (bỏ 7 câu + rút shot nối) 730 s → PHIẾU
- [ ] master · mốc JSON · GIAN-SHOT.md · PHIEU · báo cáo

## Lệnh bổ sung đã áp
- Sự cố: `pkill -f` trong một lệnh dọn đã giết chính shell gọi (BAI-HOC #112) — không mất dữ liệu; từ đó chỉ dừng theo PID ghi ra tệp.
