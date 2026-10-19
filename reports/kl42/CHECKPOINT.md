# KL42 — CHECKPOINT (việc dở, để phiên sau tiếp tục nếu container bị thu hồi)
- Nhánh `k2c-t3-kl42` (từ main @ 8cedb8af). Bước 0 xong (main đã đẩy 5253ba2b → 8cedb8af).
- Bước 1 xong: lời v4.2 khoá (`loi-khoa.txt` 51d1c773…, `script-v4.2-KHOA.md` d1921114…). Bước 2 xong: GC-C, PLS 8242b87b…; kiểm 47 mục ở speed 1,03 → `kiem47.json`.
- Bước 3: đã thu đủ 6 chương (11 064 ký tự gửi gồm 1 180 kiểm 47 mục); ASR toàn tập 254 ĐÚNG · 5 NGHI · 0 SAI (kiem-tap.json). Đang thử alias isthmus (thu_lai.py, thay.json).
  Ký tự gửi: xem `nhat-ky-ky-tu.jsonl`; bộ đếm: `bo-dem.jsonl`. Trần cứng 18 000 trong `kl_lib.py`.
- Tiếp: `ghep.py` → `kiem_tap.py` → (thu lại câu sai nếu có) → `xuat.py` → `nhip.py` → báo cáo.
