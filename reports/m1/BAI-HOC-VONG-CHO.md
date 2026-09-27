# Bài học vận hành: vòng chờ tiến trình nền tự khớp chính nó

Phiên P, M1 (27/09/2026). Áp dụng cho mọi phiên P, K, xưởng từ M2.

## Chuyện gì đã xảy ra
Phiên P chờ render nền bằng:
```bash
while pgrep -f "run_final.sh" >/dev/null; do sleep 15; done
```
`pgrep -f` so chuỗi với **toàn bộ dòng lệnh** của mọi tiến trình. Dòng lệnh của chính vòng `while` (tiến trình `bash -c "... while pgrep -f run_final.sh ..."`) cũng chứa chuỗi đó, nên `pgrep` luôn tìm thấy ít nhất một tiến trình, là **chính nó**. Vòng chờ không bao giờ thoát.

Hậu quả đo được:
- 5 vòng chờ treo cùng lúc, lâu nhất 7 giờ 40 phút (vòng chờ render `b-3d-mb8-dither.mp4` của buổi sáng).
- Render Cổng 3 v2 thật ra xong lúc 07:10 (khoảng 30 phút), nhưng phiên P không biết, và chủ dự án thấy "hơn 2 giờ".
- Tốn hạn mức và gây hiểu sai tiến độ.

Một biến thể cũng sai: `until [ -s file ]` với file do chính lệnh ghi (vd. `df` ghi dòng đầu), nên vòng thoát **quá sớm**.

## Cách làm đúng
1. **Chờ theo PID** (tốt nhất): lấy PID ngay khi khởi chạy.
   ```bash
   nohup ./run_final.sh > log 2>&1 & PID=$!
   while kill -0 $PID 2>/dev/null; do sleep 15; done
   ```
2. Nếu buộc phải dùng `pgrep -f`, dùng **mẫu có ngoặc vuông** để mẫu không khớp chính nó:
   ```bash
   while pgrep -f "[r]un_final.sh" >/dev/null; do sleep 15; done
   ```
   Regex `[r]un_final.sh` khớp chuỗi `run_final.sh` của tiến trình thật, nhưng không khớp chuỗi `[r]un_final.sh` trong dòng lệnh của vòng chờ.
3. Trước khi mở vòng chờ mới, **liệt kê vòng chờ cũ và dừng** những vòng không còn cần:
   `ps -eo pid,etime,cmd | grep -E "[w]hile (pgrep|kill)"`.
4. **Không chạy song song nhiều vòng chờ** cho cùng một việc. Một việc nền, một cách chờ.
5. Mọi vòng chờ phải có **hạn giờ** (`timeout 3600 bash -c '...'`), để lỗi logic không biến thành treo vô hạn.
6. Kiểm kết quả bằng **dấu vết thật** (file đầu ra, mốc thời gian, log "xong"), không tin vào việc vòng chờ đã thoát.
