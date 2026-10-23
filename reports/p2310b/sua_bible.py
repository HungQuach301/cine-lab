"""P-2310b · sửa Kinh thánh kênh 2 theo quyết định chủ dự án 23/10/2026 17:42 (G1 T4: D5, D9, D10, D11).
Mỗi chuỗi gốc phải xuất hiện đúng 1 lần trước khi thay. §19 lấy nguyên văn khối trích dẫn trong
reports/tien-ky-t4/DE-XUAT-BIBLE-19.md (bỏ dấu trích "> " đầu dòng; dòng tiêu đề in đậm thành tiêu đề "## 19.").
Chạy: python3 -I reports/p2310b/sua_bible.py <repo>"""
import hashlib, sys, pathlib

repo = pathlib.Path(sys.argv[1])
bible = repo / "docs/BIBLE-KENH2.md"
de_xuat = (repo / "reports/tien-ky-t4/DE-XUAT-BIBLE-19.md").read_text(encoding="utf-8")
s = bible.read_text(encoding="utf-8")
print("SHA trước:", hashlib.sha256(s.encode()).hexdigest())

DUYET = "chủ dự án duyệt 23/10/2026 17:42 (G1 T4, D9)"


def thay(cu, moi):
    global s
    n = s.count(cu)
    assert n == 1, f"chuỗi gốc xuất hiện {n} lần: {cu[:70]!r}"
    s = s.replace(cu, moi)


# 0. Tiêu đề
thay("sửa §14–§15 + §17 + §18 — 22/10/2026)\n",
     "sửa §14–§15 + §17 + §18 — 22/10/2026; §19 + sửa §13.6, §15 — 23/10/2026)\n")

# 1. §13.6: một dòng trỏ §19 cho tập từ T4
thay("- TL-6 Thẻ chương theo §13.3.\n",
     "- TL-6 Thẻ chương theo §13.3.\n"
     "- Từ T4: máy trong shot theo §19 (a) (thay TL-1 \"cố định hoặc trôi ≤ 2 %/s\"; CODINH vẫn bắt buộc cho shot có tấm nền N2+); "
     "bản đồ cổ và tranh khắc theo §19 (b)(c) (thay TL-4) — " + DUYET + ".\n")

# 2. §15 (d): kế hoạch N2+ ≤ 15 % tới khi K xét phép (iii)
thay("video AI chỉ cho minh hoạ M-d.\n",
     "video AI chỉ cho minh hoạ M-d. T4: tấm nền N2+ lập kế hoạch ≤ 15 % thời lượng tới khi phiên K xét phép (iii) "
     "(D11, chủ dự án 23/10/2026 17:42); trần 50 % giữ nguyên làm trần luật.\n")

# 3. §15 (f): khoảnh khắc M-d (6)
thay("(6) nổ nhà bằng thuốc súng Tower Street;",
     "(6) người cứu đồ lên xe ở Cheapside sáng 3/9 (thay \"nổ nhà bằng thuốc súng Tower Street\": nổ nhà là lớp dữ kiện "
     "theo LUAT-N2P-T4 b34 → dựng 3D; D10, chủ dự án 23/10/2026 17:42);")

# 4. §19 (mới), nguyên văn khối trích dẫn của đề xuất
dong = de_xuat.split("\n")
dau = next(i for i, d in enumerate(dong) if d.startswith("> **§19."))
cuoi = next(i for i in range(dau, len(dong)) if dong[i] == "---")
khoi = dong[dau:cuoi]
while khoi and khoi[-1] == "":
    khoi.pop()
assert all(d == ">" or d.startswith("> ") for d in khoi), "khối trích dẫn có dòng lạ"
khoi = [d[2:] if d.startswith("> ") else "" for d in khoi]
tieu_de = khoi[0]
goc = "(áp từ T4; chủ dự án duyệt …/10/2026).**"
assert tieu_de.count(goc) == 1
tieu_de = tieu_de.replace(goc, f"(áp từ T4; {DUYET}).**")
assert tieu_de.startswith("**§19. ") and tieu_de.endswith(".**")
tieu_de = "## 19. " + tieu_de[len("**§19. "):-len(".**")]
than = "\n".join(khoi[1:]).strip("\n")

pham_vi = (
    "**Phạm vi và quan hệ với luật cũ (" + DUYET + "):**\n"
    "- Áp từ T4; T3 và các tập trước giữ §13.6 như cũ.\n"
    "- §19 (a) thay TL-1 \"cố định (hoặc trôi ≤ 2 % khung/giây)\" cho tập từ T4; CODINH vẫn bắt buộc cho shot có tấm nền N2+. "
    "Bản thử T4 vượt ≤ 3°/s (vòng cung, cẩu) do nén đoạn 3 s; sản xuất giữ ≤ 3°/s (D9).\n"
    "- §19 (b)(c) thay TL-4 cho bản đồ cổ và tranh khắc từ T4. Trần: bản đồ (cổ + 3D kiểu bản đồ) ≤ 12 % thời lượng; "
    "tư liệu + tranh khắc + thẻ ≤ 10 % thời lượng.\n"
    "- Lửa/khói T4 (D5): lửa/khói cách A (atlas nướng sẵn) cho cảnh rộng; Cycles GPU chỉ 3–4 cận đêm (≈ 30–40 s); "
    "không ghép A↔B trong một cú máy (§14.2); nếu Cycles ngày không sửa được mép thể tích → chỉ A.\n"
)

assert s.endswith("\n") and "## 19." not in s
s = s + "\n" + tieu_de + "\n\n" + than + "\n\n" + pham_vi

bible.write_text(s, encoding="utf-8")
print("SHA sau:  ", hashlib.sha256(s.encode()).hexdigest())
