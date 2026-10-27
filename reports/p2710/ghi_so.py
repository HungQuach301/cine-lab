#!/usr/bin/env python3
# P-2710: ghi sổ theo D-B1 + B1-Q1…Q5 (chỉ thêm cuối tệp). Dùng: /opt/cine/bin/python -I reports/p2710/ghi_so.py
import csv, io, json

B1 = "`reports/ban-cuoi-t4-b1/BAN-CUOI-T4-B1-BAO-CAO.md`"
NV = "\"Duyệt B1-Q1…Q5 theo khuyến nghị điều phối\""
GIO = ("**giờ dán lệnh P-2710 27/10/2026 07:24 (Asia/Saigon; 2026-10-27T00:24:07Z, giờ tạo phiên P-2710) ghi làm giờ duyệt** (" + B1 + " §9; lệnh P-2710)")


def them(p, s):
    t = open(p, encoding="utf-8").read()
    if not t.endswith("\n"):
        t += "\n"
    open(p, "w", encoding="utf-8").write(t + s)


# ---------- AUTHORSHIP ----------
A = []
A.append("| 2026-10-26 | Kênh 2 T4 London — bản cuối BAN-CUOI-T4-B1, D-B1 (10:42 = giờ dán lệnh BAN-CUOI-T4-B1; P-2710 ghi) | Nguyên văn: \"Đã Duyệt D-B1 bằng cách dán lệnh BAN-CUOI-T4-B1 vào một phiên mới.\" — **giờ dán 26/10/2026 10:42 (Asia/Saigon; 10:41:56 = 2026-10-26T03:41:56Z, giờ tạo phiên B1) ghi làm giờ duyệt** (" + B1 + " đầu báo cáo). Nghĩa (điều phối): **bản dựng trung gian 1080p từng shot của bản cuối T4 được vào LFS** theo đúng một mẫu `channel-k2/k2c-t4-02/ban-cuoi/dung/*-1080p.mp4` (`.gitattributes` + `tools/lfs-allow.txt`; SHA ở `ban-cuoi/dung/SHA256SUMS`) — ngoại lệ cho câu \"chỉ master phát hành vào LFS\"; B1 dùng ≈ 1,03 GB (27 tệp). Kinh thánh §14.7 Look T4 cập nhật 27/10 07:24 (2) | Chủ dự án mở LFS cho bản dựng trung gian để không mất giờ máy khi container dừng | Mẫu đường dẫn, cách đẩy LFS sau mỗi shot do điều phối/phiên B1 đề xuất | Chủ dự án |")
NGHIA = {
    "B1-Q1": ("**Nâng máy mở chương M00 (P1b) và H1-01h lên ≈ 160 m** để GOC-CAO nhận là góc cao; H1-01h dựng lại 72 khung ở B2a; M00 dựng ở B2a với máy nâng, **giữ hướng, cú VONG và giờ của khung P1b đã duyệt (D-A8)**. Kinh thánh §14.7 Look T4 cập nhật 27/10 07:24 (B1-Q) (1)",
              "Chủ dự án chọn đổi độ cao máy mở chương (thay khiếu nại K), giữ nguyên khung P1b đã chọn", "Độ cao 160 m, thử GOC-CAO trên bản sao do phiên B1 đề xuất"),
    "B1-Q2": ("**Chia phần dựng còn lại thành B2a** (MÓC + H2-00…H2-05), **B2b** (H2-05s…H2-14 + HỒI 4 + sửa H3-03), **B3** (HỒI 5 + E H5-05a + B + Omni 720p + âm + ghép + xuất + G2); **mỗi phiên ≤ 12 h máy**. Kinh thánh §14.7 Look T4 cập nhật 27/10 07:24 (B1-Q) (2)",
              "Chủ dự án chọn chia phiên để giữ trần giờ máy mỗi phiên (không đổi phạm vi dựng)", "Cách chia và số khung/giờ ước do phiên B1 đề xuất (thông lượng đo 11,6 s/khung)"),
    "B1-Q3": ("**H5-02b, H5-02s giữ 3D** (niên đại toà đã sửa) **+ ảnh thật H5-02t; không thêm lượt Omni**. Kinh thánh §15 (k) cập nhật 27/10 07:24",
              "Chủ dự án chọn dừng thử AI cho hai shot 1970s, giữ 3D đúng niên đại", "Hai lượt Omni + kiểm 2 tầng do phiên B1 chạy và đề xuất"),
    "B1-Q4": ("(điều phối) **H3-03** (1860–1871, nhìn xuống): ≈ 1/2 khung là nền đường xám không nhà ở Southwark/Westminster → **B2b lấp khối nhà thời kỳ cho vùng ngoài City trong khung** (từ nền OSM, chiều cao/màu nhà Victoria, **không công trình có tên mới**) rồi **dựng lại H3-03 (227 khung)**; không đạt → **chuyển H3-03 thành lớp MAP3D cả shot** (kiểu bản đồ có chủ ý). Kinh thánh §14.7 Look T4 cập nhật 27/10 07:24 (B1-Q) (3)",
              "Chủ dự án duyệt sửa khung trống thay vì giữ, đặt phương án dự phòng bản đồ có chủ ý", "Phát hiện và hai phương án do điều phối (P) đề xuất khi soi tờ khung HỒI 3"),
    "B1-Q5": ("(điều phối) **H1-01h/H1-02h** (đêm 1666, độ sáng TB ≈ 15/255) và **H1-13a/H1-13c** (lửa ngày tầm phố, quầng sáng mạnh) **chấp nhận ở bản dựng**; chỉnh ở khâu màu/ghép B3 (`nang_toi`, tông lửa); **chủ dự án chấm lại khi xem bản xem 1080p** (cùng vòng nhịp K1179-D3). Kinh thánh §14.7 Look T4 cập nhật 27/10 07:24 (B1-Q) (4)",
              "Chủ dự án giữ quyền chấm độ sáng/tông bằng mắt trên bản xem 1080p", "Số đo độ sáng và đề xuất chỉnh ở khâu màu do điều phối (P) đưa ra"),
}
for k, (n, ng, ai) in NGHIA.items():
    A.append(f"| 2026-10-27 | Kênh 2 T4 London — bản cuối BAN-CUOI-T4-B1, {k} (07:24 = giờ dán lệnh P-2710; P-2710 ghi) | Nguyên văn: {NV} — {GIO}. Nghĩa (điều phối): {n} | {ng} | {ai} | Chủ dự án |")
them("AUTHORSHIP.md", "\n".join(A) + "\n")

# ---------- RIGHTS ----------
O = "channel-k2/k2c-t4-02/ban-cuoi/omni-b1"
R = f"""
## T4 London — bản cuối BAN-CUOI-T4-B1 (P-2710 ghi 27/10/2026)
Theo {B1} §8. **Không tài sản mới dùng trên phim** từ B1: 4 ảnh AI và 3 clip Omni dưới đây chỉ là thử/kiểm (B1-Q3: H5-02b, H5-02s giữ 3D). Bản dựng 1080p `ban-cuoi/dung/` là render của dự án (không phải tài sản ngoài). Đầu vào (`{O}/vao/*-render.jpg`) là render 3D của dự án.

### Ảnh AI (OpenAI) — ảnh đầu M-d H5-02b/H5-02s — CHỈ THỬ, KHÔNG DÙNG TRÊN PHIM
| Mã | Tài sản | Loại | Nguồn | Tác giả | Giấy phép / điều khoản | Được dùng: YouTube / bán phim / LHP | Ghi công | SHA-256 (gốc theo sổ · bản 720 trong git) | Ngày thêm |
|---|---|---|---|---|---|---|---|---|---|
| T4-BC-B1-DAU | 4 ảnh đầu M-d (OpenAI edits trên render 3D cùng năm: H5-02b 1973, H5-02s 1976): `{O}/goc/H5-02b-a1.jpg`, `H5-02b-a2.jpg`, `H5-02s-a1.jpg` (LOẠI — tháp Barbican vẽ sai), `H5-02s-a2.jpg`; bản chuẩn hoá cỡ cho Omni `goc/*-720.jpg` = `dau/H5-02b-l1-dau.jpg`, `dau/H5-02b-l2-dau.jpg`, `dau/H5-02s-a1-LOAI.jpg`, `dau/H5-02s-l2-dau.jpg` | Ảnh AI | OpenAI `gpt-image-2.5-sunburst-2026-09-08` (`POST /v1/images/edits`, không mặt nạ); lệnh nguyên văn trong `reports/ban-cuoi-t4-b1/so-ai.jsonl` (4 dòng, 26/10/2026 21:43–21:48 UTC, HTTP 200, $0,0763 mỗi lệnh) + `{O}/lenh/` | dự án (sinh bằng AI) | điều khoản OpenAI (nguyên văn `reports/pt/giay-phep/openai.md`, như dòng P1810-AI); đầu vào là render của dự án; C2PA `trainedAlgorithmicMedia` có trong sổ (`c2pa`) | **Không / Không / Không** (chỉ làm ảnh đầu cho clip thử; clip đều trượt) | — | a1 440a05183a44ea2c8c4b9db36035c8d93827e75335aa7ba003c0d7407de323d3 · a55473badab2e108240303f3959e6dd7ace84aaf7d2c4c05f6bd2f3d2dca20c5; a2 e4ec7f346a4a84e475d5c4a3acaf3894165a5cf009a5266bbacbffd5250eeba8 · c124213fa0d109970985772eb4fbed66fb759f707b886a6fdd7fcd8eaea83afb; H5-02s a1 befc00d31d1b0cd4f8c9defae57220bf75fef7a6f39af9254f689527b4efaedd · 211c4f38f63a536e717bfa7f6813964b2bdbef197c392279ee67d6316a9158fc; H5-02s a2 786856a97e71d9262220fd2229dc384d95240ce53e5e02c171e9b26db2afc537 · e93b974b569b7ca3feacca443e1bfe9d340951aa6aab6e207e688e04cc8f31aa (gốc trong git `goc/` = `output.sha256` của sổ, P-2710 kiểm 4/4) | 2026-10-27 |

### Clip AI Omni (Gemini) 360p — TRƯỢT, KHÔNG DÙNG TRÊN PHIM
| Mã | Tài sản | Loại | Nguồn | Tác giả | Giấy phép / điều khoản | Được dùng: YouTube / bán phim / LHP | Ghi công | SHA-256 (gốc theo sổ = `goc/` · bản `clip/`) | Ngày thêm |
|---|---|---|---|---|---|---|---|---|---|
| T4-BC-B1-OMNI-H5-02b-l1-360p | `{O}/clip/H5-02b-l1-360p.mp4` (gốc `{O}/goc/H5-02b-l1-360p.mp4`) — H5-02b lượt 1; TRƯỢT Flash clip (tháp cao "hiện đại" chân trời phải) | Video sinh bằng AI (Google `gemini-omni-1.1-flash`) | sổ `reports/ban-cuoi-t4-b1/so-ai-gemini.jsonl` dòng `H5-02b-l1-360p` (2026-10-26T21:45:02+00:00, HTTP 200, $0,14289) | sinh bởi mô hình Google theo lệnh phiên BAN-CUOI-T4-B1 | Gemini API Additional Terms of Service, mục "Use of Generated Content" (nguyên văn ở dòng T3-AI-M2); C2PA `trainedAlgorithmicMedia` + SynthID | **Không / Không / Không** (hồ sơ kiểm) | — | 2afee6577e866b5e015745820cc14c83e638ada905546a999425a07a131f8fea · de2ed5937817525fefb90234c4c8b00b1d75dfc18bd05da77989f9be8a7d778f | 2026-10-27 |
| T4-BC-B1-OMNI-H5-02b-l2-360p | `{O}/clip/H5-02b-l2-360p.mp4` (gốc `{O}/goc/H5-02b-l2-360p.mp4`) — H5-02b lượt 2; TRƯỢT Flash clip (xe hơi trắng khí động học hiện đại; khối tháp tối mép phải) | như trên | sổ dòng `H5-02b-l2-360p` (2026-10-26T21:46:41+00:00, HTTP 200, $0,14264) | như trên | như trên | **Không / Không / Không** | — | 347b1d4f24fe9e0673e40a12d87fd3ea80878c01405b48cfe9d93685425d6713 · 9564b1b8a25982a85acb8af2416808274f744f8823e32550d665752d5fdb14a7 | 2026-10-27 |
| T4-BC-B1-OMNI-H5-02s-l2-360p | `{O}/clip/H5-02s-l2-360p.mp4` (gốc `{O}/goc/H5-02s-l2-360p.mp4`) — H5-02s lượt 2; Flash ĐẠT, lớp mốc 3/3 ĐẠT, **tầng 2 LOẠI** | như trên | sổ dòng `H5-02s-l2-360p` (2026-10-26T21:49:22+00:00, HTTP 200, $0,24345) | như trên | như trên | **Không / Không / Không** | — | ac1357be88a6f5eafdb2dd0eb1b0b456d2fb8cf8dd1184289d8b915110e21009 · 7a9f553363e95c4d3365d02c2f2b6268c432eb39c0eee490900ba56205d37310 | 2026-10-27 |
- Bản `clip/` khác SHA gốc (bản xử lý của phiên B1 cho kiểm); gốc theo sổ có trong git ở `goc/` (P-2710 kiểm 3/3 khớp `output.sha256`).
"""
them("RIGHTS.md", R)

# ---------- COST-LEDGER ----------
H = ["phien", "tap_hoac_moc", "cong", "ngay", "quota_pct", "tok_sinh_M", "tok_cache_ghi_M", "tok_cache_doc_M", "claude_api_usd", "tran_api_usd", "model_ghim", "el_ky_tu_gui", "el_ky_tu_bo_dem", "gio_render", "gio_lich_tu_cong_truoc", "cham_chu_du_an", "thoi_luong_s", "ty_le_relief_pct", "nguon", "ghi_chu"]
hdr = open("COST-LEDGER.csv", encoding="utf-8").readline().strip().split(",")
assert hdr == H, hdr
GHI_B1 = ("2026-10-26 · BAN-CUOI-T4-B1 · Gemini $0,581 (Omni 360p 3 lệnh $0,529; Flash 7 lệnh $0,052) → T4 tổng $19,16 · OpenAI $0,390 · Claude API ≥ $0,806 · ElevenLabs 0 · RunPod 0 · ≈ 18,5 h máy (vượt mốc 14 h) · LFS ≈ 1,03 GB"
          " — Ghi chú điều phối (P-2710 cộng sổ bằng máy): **9/32 dòng sổ Claude `so-ai-claude.jsonl` thiếu `usd`** (6 dòng q_thoi_dai soi năm biên lớp mốc: H2-05s k0, H2-06 k0, H2-06 k414, H2-09 k239, H2-09 k239 lần 2, H3-01 k71 — trường `model` rỗng; 3 dòng q_thoi_dai tầng 2 H5-02s-l2 — `model` \"claude (q_thoi_dai)\") dù lệnh B1 nêu và báo cáo B1 §5 ghi \"có usd từng lệnh\" → **số Claude thật cao hơn $0,806 (ước thêm ≤ $0,3 — chưa đo)**; 23 dòng có usd (claude-sonnet-5-5) cộng $0,8060 khớp báo cáo; "
          "Gemini `so-ai-gemini.jsonl` 10 dòng = Omni 360p 3 lệnh $0,5290 + Flash 7 lệnh $0,0521 (khớp); OpenAI = gpt-image-2.5 4 lệnh $0,3052 (`so-ai.jsonl`) + gpt-6.1-sol tầng 2 3 lệnh $0,0847 (`cost.jsonl`) = $0,3899 (khớp); ElevenLabs/RunPod/YouTube 0; "
          "giờ máy ≈ 18,5 h (03:42 → ≈ 22:10 UTC 26/10) **vượt mốc 14 h ≈ 4,5 h (+32 %)** — thông lượng dựng đo 11,6 s/khung (P = 2) so ước 8,58 từ mẫu ngày (×1,35) + dựng lại H1-13a/c ≈ 1 h; LFS 27 tệp `ban-cuoi/dung/*-1080p.mp4` ≈ 1,03 GB (D-B1); chủ dự án duyệt D-B1 26/10 10:42, B1-Q1…Q5 27/10 07:24 (giờ dán lệnh P-2710); ghi sổ bởi P-2710")
row_b1 = {k: "" for k in H}
row_b1.update(phien="BAN-CUOI-T4-B1", tap_hoac_moc="K2C-T4-02 bản cuối phần B1: sửa 3D chung D-A4 (i)–(vi) (niên đại công trình mốc, thuyền, nước đêm + lửa M00, vật liệu St Paul's/toà/đêm, MAY-19, niên đại toà 1960s–70s + thử lại Omni H5-02b/H5-02s), dựng 1080p HỒI 1 + HỒI 3 + H3-05c (27 tệp, 4 818 khung, LFS D-B1), k2check 1.17.8 đặc tả v5, ước B2/B3",
              cong="xưởng", ngay="2026-10-26", claude_api_usd="0.806", tran_api_usd="8",
              model_ghim="gemini-omni-1.1-flash + gemini-3.8-flash (kiểm); gpt-image-2.5-sunburst-2026-09-08; gpt-6.1-sol (kiểm tầng 2); claude-sonnet-5-5 (q_thoi_dai lớp mốc, tầng 2)",
              el_ky_tu_gui="0", el_ky_tu_bo_dem="0", gio_render="18.5", cham_chu_du_an="1",
              nguon="reports/ban-cuoi-t4-b1/BAN-CUOI-T4-B1-BAO-CAO.md §5, §8 (nhánh claude/k2c-t4-02-final-b1-t9ekhx @6f6c2636); sổ AI reports/ban-cuoi-t4-b1/so-ai.jsonl, cost.jsonl, so-ai-gemini.jsonl, so-ai-claude.jsonl",
              ghi_chu=GHI_B1)
buf = io.StringIO()
w = csv.DictWriter(buf, fieldnames=H, lineterminator="\n")
w.writerow(row_b1)
them("COST-LEDGER.csv", buf.getvalue())

# ---------- BAI-HOC-K2 ----------
K = """
## K106–K112 · BAN-CUOI-T4-B1 và điều phối P-2710 (P-2710 ghi 27/10/2026)
| # | Bài học | Số đo | Nguyên nhân | Luật hiện hành |
|---|---|---|---|---|
| K106 | Công trình mốc đang xây phải "mọc" bằng mặt cắt dâng theo lịch từng phần, không bóp dẹt cả khối; soi lớp mốc ở năm biên bắt được cả lỗi "gần xong đọc thành xong" | B1 §1 (i): look3 bóp dẹt → vỏ vòm 74 % ở 1709,5 (H2-10 không vòm, K99), bầu Monument xong 1678,4; lịch vỏ vòm lần 1 (1705 → 1708) để H2-09 1707,86 đọc "vòm hoàn chỉnh" → dời 1707,3 → 1708,0; soi năm biên 24 khung: 20 ĐẠT, 4 ghi | mọc 1,5 năm cho mọi phần lớp 5 bằng bóp dẹt; lịch thô theo công trình, không theo phần | Kinh thánh §19 (d) cập nhật 27/10 07:24 (lịch từng phần + mặt cắt dâng + soi năm biên); `design/k2v/ldn/bc/look3-b1.js` |
| K107 | RT phản chiếu phải giữ phần phát sáng cộng (alpha 0) | B1 §1 (iii): M00 không có vệt lửa phản chiếu; ánh lửa cộng thẳng bản đồ mờ rộng → mặt sông phẳng màu cát; sau sửa: vệt lửa + sóng/Fresnel, ánh lửa nước giảm ≈ 4 lần | lửa/tàn/quầng cộng với alpha 0 bị RT phản chiếu bỏ | giữ phần phát sáng trong RT phản chiếu (`bc/look3-b1.js`); §15 (b) phản chiếu chỉ lấy từ 3D |
| K108 | Đo giờ dựng trên shot đêm/lửa trước khi chia phiên | B1 §2: mỗi tiến trình 15,0–33,1 s/khung (đêm/lửa 20–33; mẫu ngày 14–19); thông lượng 11,6 s/khung P = 2; giờ máy 18,5 / 14 h | ước từ mẫu ngày | xem K112; B1-Q2 chia B2a/B2b/B3 ≤ 12 h (Kinh thánh §14.7 Look T4 cập nhật 27/10 07:24) |
| K109 | `pipefail` + `grep -q` sau ống dẫn cho lỗi giả | B1 §6 (1): `git lfs ls-files \\| grep -q` báo lỗi (SIGPIPE) ở shot đầu dù LFS + đẩy đã thành công; hàng dừng ≈ 1 phút | `grep -q` thoát sớm → lệnh trước nhận SIGPIPE → `pipefail` trả mã ≠ 0 | lưu đầu ra vào biến/tệp trước rồi mới `grep` |
| K110 | Quy tắc gán năm toà theo vùng phải loại trừ công trình lịch sử có tên | B1 §1 (vi), §6 (3): quy tắc hành lang London Wall gán nhầm năm cho St Giles, St Alban, St Botolph và hội quán; hình học dựng 3 lần (≈ 7–10 phút/lần); 323 toà đổi năm | quy tắc vùng áp lên mọi toà thiếu năm | Kinh thánh §19 (d) cập nhật 27/10 07:24 (niên đại toà hiện đại: năm xuất hiện = hoàn thành − 2,5; loại trừ công trình lịch sử có tên) |
| K111 | **Bài học điều phối — sổ Claude của q_thoi_dai phải có `usd` từng dòng** | B1: **9/32 dòng `so-ai-claude.jsonl` thiếu `usd`** (6 dòng soi năm biên lớp mốc, `model` rỗng; 3 dòng tầng 2 H5-02s) dù lệnh B1 nêu và báo cáo B1 §5 ghi "có usd từng lệnh"; số Claude thật > $0,806 (ước thêm ≤ $0,3, chưa đo) | dòng sổ ghi từ lần gọi qua `claude -p` không trả usage; phiên không kiểm sổ bằng máy trước khi báo | trước khi báo chi phí, đếm bằng máy số dòng có `usd` = số lệnh; thiếu thì ghi "≥" và nêu số dòng thiếu (như COST-LEDGER dòng B1) |
| K112 | **Bài học điều phối — ước giờ dựng từ mẫu ngày thấp hơn thực tế ×1,35** | ước phiên A 8,58 s/khung (mẫu ngày) → đo B1 11,6 s/khung (P = 2) | mẫu đo không gồm shot đêm/lửa (nặng nhất) | **ước phiên dựng phải dùng số đo shot đêm/lửa** (B1 §2: 20–33 s/khung/tiến trình) hoặc thông lượng đo của B1 (11,6 s/khung) cho phần tương tự |
"""
them("channel-k2/BAI-HOC-K2.md", K)

# ---------- QUYET-DINH-TREO ----------
T = """
## L. Cập nhật 27/10/2026 sau BAN-CUOI-T4-B1 (P-2710 ghi)

**Đã quyết** — nguyên văn + nghĩa từng mục: `AUTHORSHIP.md`, 6 dòng P-2710. Nhánh B1 `claude/k2c-t4-02-final-b1-t9ekhx` @6f6c2636 đã merge vào main (P-2710).

| # | Quyết định | Khi nào (Asia/Saigon) | Áp ở |
|---|---|---|---|
| D-B1 | LFS bản dựng trung gian 1080p `ban-cuoi/dung/*-1080p.mp4` ("Đã Duyệt D-B1 bằng cách dán lệnh BAN-CUOI-T4-B1 vào một phiên mới.") | 26/10 10:42 (giờ dán lệnh B1) | Kinh thánh §14.7 Look T4 cập nhật 27/10 07:24 (2) |
| B1-Q1 | nâng máy M00 (P1b) và H1-01h ≈ 160 m (GOC-CAO); H1-01h dựng lại 72 khung + M00 dựng ở B2a; giữ hướng, VONG, giờ P1b (D-A8) | 27/10 07:24 (giờ dán lệnh P-2710) | §14.7 Look T4 cập nhật 27/10 07:24 (B1-Q) (1) |
| B1-Q2 | chia B2a (MÓC + H2-00…H2-05) / B2b (H2-05s…H2-14 + HỒI 4 + sửa H3-03) / B3 (HỒI 5 + E H5-05a + B + Omni 720p + âm + ghép + xuất + G2); ≤ 12 h máy/phiên | 27/10 07:24 | (B1-Q) (2) |
| B1-Q3 | H5-02b, H5-02s giữ 3D + ảnh thật H5-02t; không thêm lượt Omni | 27/10 07:24 | §15 (k) cập nhật 27/10 07:24 |
| B1-Q4 (điều phối) | H3-03: B2b lấp khối nhà thời kỳ ngoài City (OSM, nhà Victoria, không công trình có tên mới) + dựng lại 227 khung; không đạt → MAP3D cả shot | 27/10 07:24 | (B1-Q) (3) |
| B1-Q5 (điều phối) | H1-01h/H1-02h (tối) + H1-13a/H1-13c (quầng lửa) chấp nhận ở bản dựng; chỉnh màu/ghép B3 (`nang_toi`, tông lửa); chủ dự án chấm lại trên bản xem 1080p | 27/10 07:24 | (B1-Q) (4) |

**Còn treo:**

| # | Nội dung | Căn cứ | Chặn gì |
|---|---|---|---|
| Hiệu chuẩn BIEN-CO-V T4 | K hiệu chuẩn trên **master 1080p, sau B3** (thay "sau phiên B" của mục K vì B chia thành B1/B2a/B2b/B3); tới lúc đó BIEN-CO-V T4 chỉ Cảnh báo | K1179-D3, K1178-D4; B1-Q2 | Q37/TL-3 đo video ở G2 |
| Đ5 quyền giọng G1 | quyền phát hành giọng G1 (ElevenLabs) vẫn chờ | mục G, I, J, K | phát hành T4 |
| Tra thêm chân dung Godfrey Allen | NPG, St Paul's, Wikimedia Commons, Historic England — trước gói phát hành | K1179-D7 | gói phát hành T4 (H3-05b) |
| Vòng xem nhịp 1080p (K1179-D3) | chủ dự án xem bản xem 1080p: chỉ shot chậm + chọn ≤ 3 shot "đứng có chủ ý"; **cùng vòng chấm lại độ sáng/tông H1-01h/H1-02h, H1-13a/H1-13c (B1-Q5)** | K1179-D3; B1-Q5 | Q37 ở G2; màu B3 |
| Giữ từ mục K (không đổi ở P-2710) | phiếu bản cuối đẩy 2D (D5) và nước AI từng tấm (D6); chặn `pkill -f`/`pgrep -f` bằng công cụ (Nền tảng, K105); mục I/J | mục K | như mục K |
"""
them("reports/k1173/QUYET-DINH-TREO.md", T)
print("xong sổ")
