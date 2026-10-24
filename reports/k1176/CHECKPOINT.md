# CHECKPOINT — phiên K-1.17.6 (nhánh `checks-1-17-6`, gốc origin/main @df317915, LOCK 1.17.5 c7630b4a…)

Nhánh harness gợi ý: `claude/beautiful-turing-rqkp8c` — không dùng để đẩy công việc. Nhánh thật theo lệnh: `checks-1-17-6`.

## Trạng thái
| Giờ UTC | Việc | Trạng thái |
|---|---|---|
| 08:20 | Đọc CLAUDE.md, BAI-HOC-LL (đầu), K1175-BAO-CAO, khieu-nai-K.md (THU-B @353d0f0c), mã q_n2p.py / q_k1175.py | xong |
| 08:30 | `git archive` THU-B (thu-b/, reports/thu-b-t4/) → /var/tmp/k1176/thub (207 MB, không sửa) | xong |
| 08:34 | Nhánh `checks-1-17-6` từ origin/main @df317915; hook pre-commit + pre-push (tools/preflight.sh) cài trước lần đẩy đầu; `lock.py --verify` KHỚP | xong |
| 08:40 | checks-appeal.md: KN-1…KN-6 chép nguyên văn (sha256 nguồn 7a76f249…) + yêu cầu kèm theo — TRƯỚC khi phán | xong |
| 08:42–09:05 | Dữ liệu nền LOOK dựng lại trong bản sao tạm `/var/tmp/k1176/src` (git archive THU-B: design/k2v, design/cong3/shared, scripts, channel-k2/k2c-t4-02, LUT T3) để tái tạo video kiểm không mất (video-sha.json); lượt 1 thiếu pyproj → cài pyproj/tifffile/pyshp, chạy lại | đang chạy |
| 08:55–09:10 | Mã: `q_k1176.py` (mới), q_k1175 (T9c đủ khoá; (d) theo điểm ảnh; (e) độ phân giải video; px/m theo tập; KN-3), q_n2p (KN-1, KN-2), q_n2p_vision (KN-3) — bản vá WIP `reports/k1176/wip/checks-wip.patch` | đang làm |
| 09:10 | KN-1 tái hiện bằng 1.17.5 trên kiem/M4-l12, B3-l2: KeyError 'so_doan_lan' (B3: nước 213 px < 0,2 % khung → T9c trả sớm thiếu khoá). Bản sửa: 3 hàng N2P chạy, T9c KHÔNG ÁP. KN-2: M1/B3/M4 (a) sau trừ vùng BMN 0/255 (trước: 218/224/183) | xong (số đo) |

## Lệnh bổ sung đã áp
- 08:35: `git worktree add` toàn nhánh THU-B làm đầy đĩa (≈ 6 GB, còn 9,5 GB) → dừng theo PGID, xoá; thay bằng `git archive` chỉ thư mục cần (≈ 280 MB).
- 08:40: vòng chờ `until ! pgrep -f "git reset …"` khớp chính dòng lệnh của nó (lặp bài học K-1.17.5 (1)) → dừng theo PGID; từ đây chờ bằng PID cụ thể (`kill -0 <pid>`), không `pgrep -f` với chuỗi có trong lệnh chờ.
