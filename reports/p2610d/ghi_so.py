#!/usr/bin/env python3
# P-2610d: ghi sổ (chỉ thêm ở cuối tệp) theo K1179-D1…D7. Dùng: /opt/cine/bin/python -I reports/p2610d/ghi_so.py
import csv, io

NV = "Nguyên văn: \"Duyệt K1179-D1…D7 theo khuyến nghị điều phối\" — **giờ dán lệnh P-2610d 26/10/2026 13:02 (Asia/Saigon; 2026-10-26T06:02:14Z, giờ tạo phiên P-2610d) ghi làm giờ duyệt** (`reports/k1179/K1179-BAO-CAO.md` §12). Nghĩa (điều phối): "
C = "| 2026-10-26 | Kênh 2 T4 London — luật K-1.17.9, {d} (13:02 = giờ dán lệnh P-2610d; P-2610d ghi) | "


def them(p, s):
    t = open(p, encoding="utf-8").read()
    if not t.endswith("\n"):
        t += "\n"
    open(p, "w", encoding="utf-8").write(t + s)


AU = [
    ("K1179-D1", "**Duyệt luật 1.17.9** (LOCK 1.17.9 `9eddaf24e8c5276b6017af172e7c8185ba21831a7b6e842cc17094fd5c66fc34`, thay 1.17.8 `045b7bb7…`): ngoại lệ mô hình tấm E có duyệt (KN-1), biến cố đo từ log máy cho Q37 (KN-2), `cat_clip` (KN-4), toà có tên (KN-5), đẩy 2D (KN-6), miễn (k) không chân dung (KN-7), nước AI (KN-8). Kinh thánh §13.6 (hàng kiểm 1.17.9). Ghi chú giờ: báo cáo K-1.17.9 ghi giờ dán PHIẾU-A \"≈ 10:12\" theo giờ mở phiên K — **giờ duyệt PHIẾU-A chính thức là 10:08** (dòng AUTHORSHIP P-2610c D-A1…D-A9); không sửa dòng cũ", "Chủ dự án duyệt bộ luật kiểm áp cho T4", "Phán quyết, số đo, mã luật do phiên K đề xuất"),
    ("K1179-D2", "**Duyệt `ngoai_le` \"bờ\"** cho tấm **E-P9-ngay-l1**, mặt nạ \"tháp\", shot **H5-05a**: hộp **[0.0, 0.96, 0.09, 1.0]**, hàng N2P-1 (b) + N2P-3 (b); khai theo khuôn `reports/k1179/K1179-BAO-CAO.md` §4 (`duyet_chu_du_an: {nguoi_ky: \"Chủ dự án (tác giả – đạo diễn)\", vai: chu_du_an, ngay: \"2026-10-26\", ket_luan: chap_nhan}`). Máy không được miễn. Kinh thánh §15 (k) cập nhật 13:02 (2)", "Chủ dự án chấp nhận mép kè/nước AI ở góc dưới trái tấm nền H5-05a (0,09 % khung)", "Hộp, lý do, khuôn khai do phiên K đề xuất", ),
    ("K1179-D3", "**Q37 nhịp T4 giữ Chặn ở G2.** Nhịp thật sửa ở khâu dựng **sau khi chủ dự án xem bản xem 1080p**: rút ngắn/cắt xen shot dài bằng khung đã dựng (không dựng lại) hoặc thêm biến cố CÓ NGHĨA (§13.2) ở shot chủ dự án chỉ ra; **miễn có duyệt cho ≤ 3 shot \"đứng có chủ ý\"** do chủ dự án chọn khi xem (mỗi shot một dòng AUTHORSHIP). K hiệu chuẩn BIEN-CO-V T4 trên master 1080p sau phiên B (K1178-D4 giữ). Kinh thánh §13.6 cập nhật 13:02", "Chủ dự án giữ chuẩn nhịp và tự chỉ shot chậm khi xem; tự chọn ≤ 3 shot đứng có chủ ý", "Số đo 39 khoảng > 6 s, phương án A/B/C do phiên K đề xuất"),
    ("K1179-D4", "**\"Toà có tên\" cho LUẬT E** = tháp đỉnh ≥ 75 m ODN + công trình lịch sử có `nguon_lich_su` + St Paul's (mặt nạ \"tháp\"); **\"Guildhall Art Gallery\" không tính là lịch sử nếu không có nguồn**. Kinh thánh §15 (k) cập nhật 13:02 (1)", "Chủ dự án chọn định nghĩa theo chữ 26/10 00:07 \"toà THÁP có tên\"", "Ngưỡng 75 m, số đo (a)-E do phiên K/A đề xuất"),
    ("K1179-D5", "**Cho phép đẩy/trượt 2D ≤ 1,5 %/s trên tấm E** — một phép 2D cho cả khung ghép, máy 3D CODINH; **dùng theo tờ so, chủ dự án duyệt ở phiếu bản cuối**. Kinh thánh §15 (k) cập nhật 13:02 (3)", "Chủ dự án mở chuyển động máy 2D cho tấm E; giữ quyền duyệt từng lần dùng", "Ngưỡng, điều kiện, số đo do phiên K đề xuất"),
    ("K1179-D6", "**Cho phép nước AI trên tấm E** (`nuoc_ai`, giữ bờ phía đất) — **duyệt từng tấm qua tờ so**; **trước khi dùng phải sửa** thuyền render elip đen + bóng cầu AI lệch. Kinh thánh §15 (k) cập nhật 13:02 (4)", "Chủ dự án mở nước AI cho tấm E, giữ quyền duyệt từng tấm, đặt điều kiện sửa trước", "Cách ghép bờ phía đất, tờ so KN-8, đề bài mô hình do phiên K đề xuất"),
    ("K1179-D7", "**Giữ H3-05b** (Godfrey Allen; miễn (k) theo 1.17.9: YuNet ≤ 0,070, 4 nơi đã tra, AUTHORSHIP 2026-10-26 00:12); **tra thêm NPG, St Paul's, Wikimedia Commons, Historic England trước gói phát hành**; H3-05c chỉ là dự phòng. Kinh thánh §15 (f) cập nhật 13:02", "Chủ dự án giữ clip nhân vật có tên đã chọn 26/10 00:12 và đặt việc tra chân dung trước phát hành", "Số đo YuNet, danh sách nơi tra do phiên K đề xuất"),
]
au = "".join(C.format(d=d) + NV + y + " | " + h + " | " + ai + " | Chủ dự án |\n" for d, y, h, ai in AU)
them("AUTHORSHIP.md", au)

# COST-LEDGER: dòng K-1.17.9 (nguyên văn lệnh + ghi chú điều phối)
row = ["K-1.17.9",
       "Luật 1.17.9: xét khiếu nại BAN-CUOI-T4-A KN-1, KN-2, KN-4…KN-7 (KN-3 rút) + KN-8 (điều phối) — ngoại lệ mô hình tấm E, biến cố log máy Q37, cat_clip, toà có tên, đẩy 2D, miễn (k) không chân dung, nước AI; selftest_k1179 50/50; LOCK 1.17.8 045b7bb7 → 1.17.9 9eddaf24",
       "K", "2026-10-26", "", "", "", "", "0.699", "8",
       "claude-sonnet-5-5 (mô hình nhìn KN-8, q_thoi_dai O2); gpt-6.1-sol (mô hình nhìn KN-8)",
       "0", "0", "1.9", "", "1", "", "",
       "reports/k1179/K1179-BAO-CAO.md §10, §13 (nhánh ccr-196e0bda-gcj9iw @a7dc969f); sổ AI reports/k1179/so-ai.jsonl (20 dòng, mọi dòng có usd)",
       "2026-10-26 · K-1.17.9 · OpenAI $0,313 · Claude API $0,699 · Gemini 0 · ≈ 1,9 h máy · tải LFS 1,79 GB — Ghi chú điều phối (P-2610d cộng sổ `reports/k1179/so-ai.jsonl` bằng máy): OpenAI gpt-6.1-sol 6 lệnh $0,3132 (mô hình nhìn KN-8; mốc $2, chặn $5); Claude API claude-sonnet-5-5 14 lệnh $0,6991 (mô hình nhìn $0,421 + q_thoi_dai O2 $0,278; mốc $3, chặn $8) — khớp báo cáo; ElevenLabs/RunPod/YouTube 0; 0 ảnh/video sinh; tải LFS master T3 1,79 GB (SHA khớp); giờ máy ≈ 1,9 h (03:12 → ≈ 05:05 UTC 26/10; P ≤ 2); lock.py không cờ gọi 1 lần; chủ dự án duyệt K1179-D1…D7 26/10 13:02 (giờ dán lệnh P-2610d); ghi sổ bởi P-2610d"]
b = io.StringIO(); csv.writer(b, lineterminator="\n").writerow(row)
them("COST-LEDGER.csv", b.getvalue())

BH = """
## K101–K105 · K-1.17.9 và điều phối P-2610d (P-2610d ghi 26/10/2026)
| # | Bài học | Số đo | Nguyên nhân | Luật hiện hành |
|---|---|---|---|---|
| K101 | Đổi lớp được bảo vệ (nước render → nước AI) thì phải đổi đề bài mô hình nhìn; chạy đối chứng tấm sạch trước | K-1.17.9 §2 KN-8, §11 (2): lượt 1 dùng đề bài E cũ → GPT báo nhầm "sông được bảo vệ đổi" @[0; 0,686; 1; 1] ($0,24); đề bài `n2p-e-v2-nuoc` → 2 tấm sạch 0 Chặn, 2/2 ca âm bắt | đề bài E coi sông là phần bảo vệ | Đề bài `n2p-e-v2-nuoc` cho tấm `nuoc_ai` (RULES-LL 1.17.9); chạy tấm sạch đối chứng trước khi tin báo mô hình |
| K102 | `pkill -f <tên script>` trong lệnh có chứa chính tên đó giết shell của phiên | K-1.17.9 §11 (4): `pkill -f e_sau_khoa.sh` tự giết lệnh shell (không mất dữ liệu) | mẫu khớp chính dòng lệnh shell | dừng theo PGID/PID ghi ra tệp (LL #112); xem K105 |
| K103 | Nền đổi màu (nước AI) thì giữ dải bảo vệ PHÍA ĐẤT, không dải ±8 px hai phía | K-1.17.9 §2 KN-8: dải ±8 px giữ màu nước render → viền xanh quanh bờ, cầu, thuyền trên nước AI nâu; bờ phía đất → liền mạch; (a)-E E-P1 "tháp" 28,41 → 8,20 % (±8) / **6,38 %** (phía đất) | dải bảo vệ đối xứng mang màu nền cũ sang nền mới | Kinh thánh §15 (k) cập nhật 26/10 13:02 (4); ghép `reports/k1179/do/ghep_kn8.py … bo_dat` |
| K104 | Thước đối chứng render (T9c) không áp cho vùng AI vẽ lại toàn phần | K-1.17.9 §2 KN-8: tấm nước AI sạch báo 7 đoạn bờ lấn tới 70 px (1 thật); 4 ca âm tổng hợp ngang hoặc thấp hơn tấm sạch | T9c so với render, mà nước AI không còn là render | T9c trên nước AI chỉ in (RULES-LL 1.17.9); dựa mô hình nhìn + người đọc tờ so |
| K105 | **Bài học điều phối — `pkill -f`/`pgrep -f` tự khớp chính lệnh đã lặp ≥ 6 lần dù đã có bài học → phải chặn bằng công cụ** | LL #24, #41, #112; K46 (K-1.17.4, LOOK-T4), K54 (K-1.17.5, GIONG-T4), K61 (ANIMATIC-T4), K75 (K-1.17.6), K85 (K-1.17.7, ANIMATIC-T4-V2), BAN-CUOI-T4-A (§11 (12) một lần `pgrep -f`), K-1.17.9 (K102); mọi lệnh phiên từ P-2610 đã ghi "Không dùng `pgrep -f`/`pkill -f`" | luật chỉ bằng lời trong lệnh và bài học; không có gì chặn lúc chạy | **Giao phiên Nền tảng**: chặn bằng công cụ (vd hook PreToolUse của harness từ chối lệnh Bash chứa `pkill -f`/`pgrep -f`, hoặc hàm `dung_pgid`/`dem_pgid` trong `scripts/common/`), kèm thử ca âm; tới khi có: dừng/đếm theo PGID ghi ra tệp |
"""
them("channel-k2/BAI-HOC-K2.md", BH.lstrip("\n") if open("channel-k2/BAI-HOC-K2.md", encoding="utf-8").read().endswith("\n\n") else BH)

QD = """
## K. Cập nhật 26/10/2026 sau K-1.17.9 (P-2610d ghi)

**Đã quyết** — chủ dự án "Duyệt K1179-D1…D7 theo khuyến nghị điều phối", **26/10 13:02 Asia/Saigon (giờ dán lệnh P-2610d)**; nguyên văn + nghĩa từng mục: `AUTHORSHIP.md`, 7 dòng P-2610d. Nhánh K-1.17.9 `ccr-196e0bda-gcj9iw` @a7dc969f đã merge vào main (P-2610d). Mục J "KN-1, KN-2, KN-4, KN-5, KN-6, KN-7, KN-8" → **đã quyết** như bảng dưới.

| # | Quyết định | Khi nào (Asia/Saigon) | Áp ở |
|---|---|---|---|
| K1179-D1 | duyệt luật 1.17.9 (LOCK `9eddaf24…`) | 26/10 13:02 | Kinh thánh §13.6 (hàng kiểm 1.17.9, cách khai) |
| K1179-D2 (KN-1) | `ngoai_le` "bờ" cho E-P9-ngay-l1 "tháp" (H5-05a), hộp [0.0, 0.96, 0.09, 1.0], khuôn K1179 §4 → H5-05a dùng mặt nạ "tháp" (D-A1 hết nhánh "K bác") | 26/10 13:02 | §15 (k) cập nhật 13:02 (2) |
| K1179-D3 (KN-2) | Q37 T4 giữ Chặn ở G2; sửa nhịp thật ở khâu dựng sau khi chủ dự án xem bản xem 1080p; miễn ≤ 3 shot "đứng có chủ ý" | 26/10 13:02 | §13.6 cập nhật 13:02 |
| K1179-D4 (KN-5) | toà có tên = tháp ≥ 75 m ODN + lịch sử có `nguon_lich_su` + St Paul's; Guildhall Art Gallery không tính nếu không có nguồn | 26/10 13:02 | §15 (k) cập nhật 13:02 (1) |
| K1179-D5 (KN-6) | đẩy/trượt 2D ≤ 1,5 %/s trên tấm E (một phép 2D cả khung, máy 3D CODINH); dùng theo tờ so, duyệt ở phiếu bản cuối | 26/10 13:02 | §15 (k) cập nhật 13:02 (3) |
| K1179-D6 (KN-8) | nước AI trên tấm E (`nuoc_ai`, bờ phía đất), duyệt từng tấm; sửa thuyền elip đen + bóng cầu AI lệch trước | 26/10 13:02 | §15 (k) cập nhật 13:02 (4) |
| K1179-D7 (KN-7) | giữ H3-05b (miễn (k) theo 1.17.9); H3-05c dự phòng | 26/10 13:02 | §15 (f) cập nhật 13:02 |
| KN-4 | `cat_clip` (lỗi mã, đã sửa ở 1.17.9) — không cần quyết riêng | 26/10 13:02 (cùng D1) | RULES-LL 1.17.9 |

**Còn treo:**

| # | Nội dung | Căn cứ | Chặn gì |
|---|---|---|---|
| Hiệu chuẩn BIEN-CO-V T4 | K hiệu chuẩn trên master 1080p **sau phiên B** (K1178-D4 giữ); tới lúc đó BIEN-CO-V T4 chỉ Cảnh báo | K1179-D3; Kinh thánh §13.6 | Q37/TL-3 đo video ở G2 |
| Chọn shot nhịp (D3) | chủ dự án xem bản xem 1080p, chỉ shot chậm + chọn ≤ 3 shot "đứng có chủ ý" | K1179-D3 | Q37 ở G2 |
| Tra thêm chân dung Godfrey Allen | NPG, St Paul's, Wikimedia Commons, Historic England — trước gói phát hành | K1179-D7 | gói phát hành T4 (H3-05b) |
| Đ5 quyền giọng G1 | quyền phát hành giọng G1 (ElevenLabs) vẫn chờ | mục G, I, J | phát hành T4 |
| Phiếu bản cuối: đẩy 2D (D5), nước AI từng tấm (D6) | chủ dự án duyệt qua tờ so khi phiên B dùng | K1179-D5, D6 | M01/H5-05a (đẩy 2D), E-P1 |
| Chặn `pkill -f`/`pgrep -f` bằng công cụ | đề xuất giao phiên Nền tảng (BAI-HOC-K2 K105; trước đó K85) | P-2610d | vận hành |
| Giữ từ mục I/J (không đổi ở P-2610d) | XEM CÂM Q2/Q3/Q4/Q6 chấm trên bản cuối; các mục giữ từ G/H | mục I, J | như mục I |
"""
them("reports/k1173/QUYET-DINH-TREO.md", QD)
print("xong")
