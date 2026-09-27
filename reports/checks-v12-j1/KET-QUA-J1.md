# J1 v1.2 trên table read Cổng 2 của P (phiên K)

- Luật: `checks/` trên nhánh `checks/v1.2`, VERSION 1.2.0, LOCK `0196187b7af0523e9b2bc23ce68d5d95addd098f42a18de42b8afb8d4e2e76ff`. Mọi báo cáo ghi LOCK khớp.
- Nguồn: `reports/m1/cong2/tableread-d2/` (nháp 2) và `reports/m1/cong2/tableread/` (nháp 1, bản bị khiếu nại), nhánh `claude/cine-lab-m1-last-round-f1667s`. Chạy J1 trên file `.mp4` cùng `.script.txt` đi kèm.
- Tái lập: `bash reports/checks-v12-j1/run_j1.sh`.

| Bản | v1.1 | v1.2 | Chữ bị bỏ vì nằm trong im lặng số | Chèn ngoài câu |
|---|---|---|---|---|
| Nháp 2 (4 câu, 33 từ) | TRƯỢT: 96,97% từ, WER 15,15% | **ĐẠT: 100% từ, WER 0%** | 'Great.' 38,82–40,22 s; 'You' 137,68–139,08 s | 0 |
| Nháp 1 (5 câu, 39 từ) | TRƯỢT: 94,87% từ, WER 10,26% | **ĐẠT: 100% từ, WER 0%** | 'you' 56,8–58,2 s | 0 |

- **Nháp 2 ở v1.1** trượt vì:
  - "goodnight" bị tính 1 thay + 1 chèn;
  - chữ bịa "Thank you." (14,14–16,14 s) và "You" (134–136 s).
  - Theo mốc đoạn của v1.1, vùng 134–136 s là im lặng số tuyệt đối (RMS −200 dBFS).
- **v1.2 bật mốc từng chữ.** Lượt toàn file giải mã hơi khác, nên chữ bịa đổi vị trí. Cả hai chữ bịa đều nằm trọn trong im lặng số và bị bỏ; báo cáo liệt kê. Không còn chữ bịa nào ở vùng có tiếng.
- **Nháp 1:** "warm" (câu 5) nay nghe đúng. Cửa sổ câu 137,53–144,34 s chứa trọn chữ này (khởi âm 139,45 s).
- **Chỉ số trong ±5% quanh ngưỡng:** không có (100% / 0%).
