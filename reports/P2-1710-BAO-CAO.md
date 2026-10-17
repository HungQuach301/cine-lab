# PHIÊN P2-1710: cập nhật main + ghi sổ quyết định 17/10 (ZZ1–ZZ6, D1–D10, WW1–WW8, XX1–XX2, YY1–YY6). BÁO CÁO. DỪNG chờ chủ dự án

```text
ĐIỀU LỆ PHIÊN P2-1710                                       | thực tế
Loại phiên:        P (điều phối)                             | đúng
Nhánh:             main (ZZ1)                                | main ff + 3 merge + 1 commit sổ + commit báo cáo
Tệp KHÔNG sửa:     checks/ · scripts/ · design/ ·            | không sửa; checks/ chỉ chạy lock/selftest, không đọc mã
                   docs/BIBLE-KENH2.md                       |
Trần chi phí:      Claude API $0 · ElevenLabs 0 · YouTube 0  | $0 · 0 ký tự · 0 đơn vị
                   · giờ máy ≤ 0,5 h                         | ≈ 0,1 h
Preflight:         BẮT BUỘC; che email                       | ĐẠT (staged 7 tệp; range 114 tệp); 0 email trong tệp ghi
Merge:             KHÔNG merge checks/v1.13                  | không merge
```

## 0. Tóm tắt

### 0.1 main trước → sau
| Bước | Commit | Ghi chú |
|---|---|---|
| Trước | `7255aa42` | main cũ (NT 15/10) |
| ZZ1 ff `origin/p-1710` | **`b240b521`** | `merge --ff-only` thành công (117 commit), `git push origin main` thành công |
| merge `origin/nc-lich-su` (`a30af04e`) | `fc39bbce` | `--no-ff`; chỉ thêm 6 tệp |
| merge `origin/nc-lich-su-2` (`396327a0`) | `4ddc697e` | `--no-ff`; thêm 5 tệp còn lại (11 tệp so với main trước merge, gồm 6 của NC-LS) |
| merge `origin/k2c-t3-tienky-b` (`ffeff7ea`) | `a69a7aeb` | `--no-ff`; chỉ thêm 96 tệp trong `channel-k2/k2c-t3-01/` |
| commit ghi sổ | `0d3a58d2` | 7 tệp sổ (§0.2); đẩy main `b240b521..0d3a58d2` |
| commit báo cáo | commit chứa tệp này | "DỪNG chờ chủ dự án" |

- Cả ba nhánh chỉ thêm tệp (`git diff --name-status` toàn `A`), không xung đột.
- **Không** merge `checks/v1.13` (K đang chạy).

### 0.2 Sổ đã ghi (commit `0d3a58d2`)
| Sổ | Nội dung |
|---|---|
| `AUTHORSHIP.md` | Dòng **QQ5** sửa thành nguyên văn lệnh (08:40). Thêm 5 dòng: **WW1–WW8** (series "Contested Places", cổng sau 3 tập; L1; T3 Gibraltar vây hãm; lịch T3 → T4 London 1666 → T5 Boston 1775–76 → cổng; V5b-2b + V6; K 1.13; luật hình chiến tranh; đo giọng), **XX1–XX2** (khung ĐỎ có kiểm soát), **YY1–YY6** (Dresden = ĐỎ-K đầu tiên ở T7; Berlin có điều kiện; Stalingrad xét có điều kiện sau Dresden và Berlin; bỏ Jerusalem, Derry, Nanjing; đổi tên ĐỎ-K; (c) = c1 ∧ c2; tư vấn luật/người đọc quyết ở G0 Dresden), **ZZ1–ZZ6**, **D1–D10 T3b** (duyệt D1–D8, D10; D9 KHÔNG làm; D4 ngoại lệ hồ sơ thật 20,7 % cho tập lịch sử; D5 số hoá do phiên Claude SH) |
| `channel-k2/HANG-DOI.md` | Mục "CẬP NHẬT 17/10" của P-1710 thay bằng **LỊCH HIỆU LỰC 17/10 (WW4)**: T2 không phát hành; T3 Gibraltar vây hãm (VÀNG, trước 14/12); T4 London 1666 (XANH); T5 Boston 1775–76 (XANH); cổng; T6 XANH; T7 Dresden 1945 (ĐỎ-K). Las Vegas, Zürich, Detroit, thành phố cổ lùi sau cổng (tiền kỳ giữ); hàng đợi NC-LS (Vicksburg, Rotterdam, Antwerp, Malta, Halifax, Zürich 1799, Leiden; Vienna cuối); Berlin có điều kiện; Stalingrad xét có điều kiện; danh sách bỏ. Bảng 12/10 bên dưới giữ nguyên |
| `channel-k2/QUAN-TRI-RUI-RO.md` §1 | Thêm hàng **ĐỎ-K**: định nghĩa XX1, phép thử (c) = c1 ∧ c2, quy trình G0 / G1-R / K-R1…R9 / chỉ số sau đăng theo `reports/NC-LICH-SU-2-BAO-CAO.md` §5, chủ dự án quyết ở G1-R, nhịp ≤ 1 ĐỎ-K/4 tập, không liền VÀNG, không trong T3–T5. Hàng **ĐỎ = cấm** giữ nguyên; ghi rõ ĐỎ-K không nới danh sách 1.1 |
| `COST-LEDGER.csv` | **NC-LS-01** (YouTube 2 124 đv, giờ máy 0,1), **NC-LS2-01** (1 434 đv, 0,1), **T3b-01** (200 đv, 0,15 ước), cả ba API $0, ElevenLabs 0; số chép từ dòng đề xuất cuối từng báo cáo |
| `channel-k2/.gitignore` | `!k2c-t3-01/vay-ham/*.json` (kiểm: `git check-ignore` không còn chặn `vay-ham/treatment.json`) |
| `tools/lfs-allow.txt` | ghi chú ZZ4: bản 1080p V5b-1 khi đẩy LFS phải tên `gib20-1080p.mp4`; không thêm mẫu gạch dưới (mẫu `*-1080p.mp4` có sẵn đã khớp) |
| `reports/P-1710-BAO-CAO.md` | thêm **§2 "Sau duyệt 17/10"**: ZZ1–ZZ6 (RR2 đóng, giữ LFS; VERSIONS T2 giữ nguyên) |

**Điểm P tự đọc, cần chủ dự án biết:**
- Lệnh chỉ nêu nội dung ZZ1, ZZ4, "RR2 đóng, giữ LFS", "VERSIONS T2 giữ nguyên" và nguyên văn QQ5. P ánh xạ ZZ2 = QQ5, ZZ3 = việc chờ 3 (COST-LEDGER K2C-T2-01), ZZ5 = RR2, ZZ6 = VERSIONS T2 theo thứ tự "Việc chờ" của P-1710 §1. **ZZ3 không có nguyên văn**: P giữ dòng sổ `K2C-T2-01` ($15,16) như đã ghi, không đổi số.
- Chi tiết từng mục WW/YY/D trong AUTHORSHIP lấy từ bảng đề xuất của ba báo cáo đã merge (NC-LS §0, §8; NC-LS2 §0, §5; TIEN-KY-VAY-HAM §0). Hai điểm chủ dự án quyết khác đề xuất được ghi rõ: Dresden ở **T7** (đề xuất T8); Stalingrad **xét có điều kiện** (đề xuất bỏ); Boston thành T5 (đề xuất là dự phòng T4).
- Mã thư mục `k2c-t4-01` (Las Vegas), `k2c-t5-01` (Zürich), `k2c-t6-01` (Detroit) không đổi tên; HANG-DOI ghi rõ thứ tự phát mới theo bảng, không theo mã thư mục.
- Kinh thánh (`docs/BIBLE-KENH2.md`): D4, L1, luật hình chiến tranh **chưa** ghi vào vì lệnh cấm sửa tệp này ở phiên P2 → việc chờ 3.

### 0.3 Kiểm sau cùng
| Kiểm | Kết quả |
|---|---|
| `checks/lock.py --verify` | **KHỚP** 1.12.2 `81789fad2e7a986a092cd2c0659a1cb93b3b5f9e87e4cfc79f7a93e316506e93` |
| `checks/ll/selftest_k1122.py` | **37/37** ca đúng kỳ vọng |
| `tools/preflight.sh` (staged, commit sổ) | **ĐẠT**: 7 tệp, lock KHỚP |
| `tools/preflight.sh --range b240b521..HEAD` (3 merge + sổ) | **ĐẠT**: 114 tệp, lock KHỚP |
| `scripts/env/verify.sh` | đầu phiên 10 PASS / 3 FAIL → cài `tifffile pyshp` (pip) → **11 PASS / 2 FAIL**. Hai FAIL còn lại (three.js `design/cong3/shared`, k2v `design/k2v` node_modules) cần `npm ci` trong `design/`; không chạy vì lệnh cấm chạm `design/` và việc ghi sổ không cần |

- Hook pre-commit: lệnh cài liên kết hook bị bộ phân loại quyền của phiên từ chối; P chạy `tools/preflight.sh` bằng tay trước commit (ĐẠT) và theo khoảng commit trước khi viết báo cáo. Không dùng `--no-verify`.
- Email: 0 địa chỉ email trong tệp ghi (preflight kiểm).

### 0.4 Chi phí
| Mục | Trần | Thực tế |
|---|---|---|
| Claude API (gọi từ script) | $0 | **$0** |
| ElevenLabs | 0 | **0** ký tự |
| YouTube Data API | 0 | **0** |
| Giờ máy | ≤ 0,5 h | **≈ 0,1 h** (fetch/merge, selftest_k1122, preflight, verify.sh ×2, pip) |
| Token | trần mềm | không đo được trong phiên |

**Chỉ số trong ±5 % quanh ngưỡng:** không có.

**Dòng đề xuất cho `COST-LEDGER.csv`** (ghi ở lần P kế, để commit báo cáo không sửa sổ sau khi đã kiểm): `P2-1710, cập nhật main + ghi sổ 17/10, P, 2026-10-17, claude_api_usd=0, elevenlabs_chars=0, youtube_units=0, render_h=0.1`.

## 1. Việc chờ chủ dự án
1. **ZZ3:** cho nguyên văn nếu khác "giữ dòng K2C-T2-01 $15,16" (P đã giữ nguyên).
2. **Merge `checks/v1.13`** khi phiên K xong và chủ dự án duyệt (K 1.13 = WW6).
3. **Kinh thánh (`docs/BIBLE-KENH2.md`):** chỉ định phiên ghi lời hứa L1, ngoại lệ hồ sơ thật D4 cho tập lịch sử, luật hình chiến tranh (WW7) và CS1–CS10 (D7) vào `LUAT-NOI-DUNG-G.md` (đề xuất ở NC-LS §8.5, TIEN-KY-VAY-HAM §9).
4. **Mở phiên:** V5b-2b (tích hợp + P0/P1/P2 cho T3), V6 "Chiến trường", Claude SH (số hoá ghost D5), G1 T3 Gibraltar (hạn phát hành 14/12).
5. **RIGHTS.md** cho tư liệu T3b: ghi khi tài sản được dùng thật ở G1 (đề xuất T3b §9.2), kèm dòng OSM ODbL.
6. **`npm ci`** trong `design/cong3/shared` và `design/k2v` (verify.sh FAIL) ở phiên được phép chạm `design/`.
