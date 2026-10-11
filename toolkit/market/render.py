"""Viết hồ sơ cầu (markdown) và bảng cột Cầu/Khoảng trống/Câu hỏi cho hàng đợi — chỉ từ summary() (an toàn cho repo)."""
import json, re
from core import LABEL_SELF

WEIGHT_NOTE = ("Trọng số nhãn cầu trong quyết định đề tài: **TẠM** — chốt sau `channel-k2/CALIBRATION.md` (phiên k2, 12/10) "
               "và sau 3 tập có dự đoán (`reports/m3/KHAN-GIA-SO.md`).")


def profile_md(s, pack):
    yt = lambda i: f"[{i}](https://youtu.be/{i})"
    L = [f"# Hồ sơ cầu — {s['title']}", "",
         f"Gói kênh `{pack['name']}` · đề tài `{s['slug']}` · **Làm mới: {s['made']}** (làm lại khi > 30 ngày; Việc 0 của tập).",
         f"Sinh bằng `toolkit/market/market.py topic {s['slug']} --pack {pack['name']}`. Số liệu thô ở `$MARKET_DATA` (ngoài git, "
         f"xoá > 30 ngày). Mọi nhãn, dải và chỉ số: **{LABEL_SELF}**. Câu hỏi, hoàn cảnh, điểm yếu: model diễn đạt lại từ bình "
         "luận đã lọc (không tên người, không trích nguyên văn) — máy viết, có thể sai.",
         "> Dữ liệu chọn và định hướng; KHÔNG quyết định nội dung hay hình. Nguyên tắc tối cao (chất lượng) đứng trên.", "",
         "| Mục | Nhãn | Cách tính (tự tính) |", "|---|---|---|",
         f"| Cầu hiện hành | **{s['current']}** | video ≥ 8 phút đăng 90 ngày qua {len(s['queries'])} câu hỏi khán giả: {s['n_cur_on']} video đối thủ trực tiếp ≥ 50 nghìn lượt (≥ 2 Mạnh · 1 Yếu · 0 Không); {s['n_cur_long']} video dài trong mẫu |",
         f"| Cầu bền | **{s['durable']}** | top video dài toàn thời gian ({len(s['durable_queries'])} câu): có video đúng đề tài ≥ 500 nghìn lượt |",
         f"| Khoảng trống | **{s['gap']}** | {s['gap_real']} video đầu bảng có dấu hiệu số liệu thật có nguồn (≤ 1/5 → Có) |",
         f"| Dải thời lượng thắng | **{s['band']}** | tứ phân vị 25–75 % số phút của {s['n_band']} video đúng đề tài ≥ 50 nghìn |",
         "", WEIGHT_NOTE, "", "## 3 video vượt trội cùng đề tài (cho dòng G1; xem, không chép)"]
    L += [f"- {o['ch']} — {yt(o['id'])} — {o['min']} phút — {o['ratio']} trung vị kênh — {o['views']}" for o in s["outliers"]] \
        or ["- chưa có video ≥ 3× trung vị kênh trong mẫu"]
    L += ["", f"## 5 câu hỏi khán giả (xếp theo trọng số like + phản hồi; {s['n_comments']} bình luận, loại {s['kinds']})"]
    L += [f"{i}. {q['q_en']} — trọng số {q.get('weight', '?')}" for i, q in enumerate(s["questions"], 1)]
    L += ["", "## Ba hoàn cảnh điển hình (tổng hợp, không phải người thật)"]
    L += [f"- {x['vi']}" for x in s["situations"]]
    L += ["", "## Điểm yếu đối thủ (không nêu tên kênh trong phim)"]
    L += [f"- {w['vi']} ({w.get('evidence', '?')})" for w in s["weaknesses"]]
    L += ["", "## Video đối thủ đầu bảng", "", "| Kênh | Video | Phút | Bậc lượt xem | Vượt trội | Số liệu có nguồn |", "|---|---|---|---|---|---|"]
    L += [f"| {c['ch']} | {yt(c['id'])} | {c['min']} | {c['views']} | {c['ratio']} | {'có' if c['real_data'] else 'không'} |" for c in s["competitors"]]
    L += ["", "## Mẫu tiêu đề (khuôn trừu tượng, không chép)"] + [f"- {t}" for t in s["title_patterns"]]
    if s["keywords"]:
        L += ["", "## Cụm tìm kiếm (cho tiêu đề/mô tả)", ", ".join(s["keywords"])]
    if s["requests"]:
        L += ["", "## Khán giả yêu cầu (→ hàng đợi nếu chưa có)"] + [f"- {r['vi']}" for r in s["requests"]]
    wd = ", ".join(f"{k} {v}" for k, v in sorted(s["weekdays_et"].items(), key=lambda kv: -kv[1])) or "chưa đủ mẫu"
    L += ["", "## Giờ đăng (gợi ý G3)", f"- Thứ đăng (giờ New York) của video đúng đề tài ≥ 50 nghìn: {wd}. Chỉ là gợi ý; "
          "mặc định kênh giữ nhịp HUONG-DAN-DANG (thứ Ba–Năm 9:00–11:00 ET) trừ khi ≥ 3 tập có số đo khác.",
          "", "## Câu hỏi đã tìm", "- 90 ngày: " + " · ".join(f"`{q}`" for q in s["queries"]),
          "- toàn thời gian: " + " · ".join(f"`{q}`" for q in s["durable_queries"]), ""]
    return "\n".join(L)


QUEUE_START, QUEUE_END = "<!-- market:queue:start -->", "<!-- market:queue:end -->"


def queue_block(labels, pack):
    L = [QUEUE_START, f"| Đề tài | Cầu (hiện hành / bền) | Khoảng trống | Câu hỏi khán giả (câu 1) | Dải thắng | Làm mới |", "|---|---|---|---|---|---|"]
    for slug, t in pack["topics"].items():
        if t.get("episode"):                     # đề tài đã làm thành tập: không thuộc hàng đợi (nhãn hồi tố ở KHAN-GIA-SO)
            continue
        s = labels.get(slug)
        if s:
            L.append(f"| `{slug}` | {s['current']} / {s['durable']} | {s['gap']} ({s['gap_real']}) | {s['questions'][0]['q_en']} | {s['band']} | {s['made']} |")
        else:
            L.append(f"| `{slug}` | chưa đo | chưa đo | — | — | — |")
    L += ["", f"Máy sinh (`market.py queue --pack {pack['name']}`), {LABEL_SELF}. {WEIGHT_NOTE}", QUEUE_END]
    return "\n".join(L)


def replace_block(text, block):
    if QUEUE_START in text:
        return re.sub(re.escape(QUEUE_START) + ".*?" + re.escape(QUEUE_END), lambda m: block, text, flags=re.S)
    return text.rstrip() + "\n\n" + block + "\n"


# Kiểm luật dữ liệu trên văn bản sắp ghi vào repo: không một số thô nào của kênh khác (lượt xem, like, bình luận, người đăng ký
# ≥ 1 000 đã thu ở lượt chạy) xuất hiện, ở mọi kiểu viết (12345 · 12,345 · 12.345 · 12 345). `guard` = các số thô đó.
def _forms(n):
    s = f"{n:,}"
    return {str(n), s, s.replace(",", "."), s.replace(",", " "), s.replace(",", " "), s.replace(",", " ")}


def assert_repo_safe(text, guard=()):
    hits = []
    for n in guard:
        for f in _forms(n):
            if re.search(r"(?<![\w.,-])" + re.escape(f) + r"(?![\w-]|[.,]\d)", text):
                hits.append(f)
                break
    if hits:
        from core import MarketError
        raise MarketError(f"văn bản cho repo có số thô kênh khác {hits[:5]} — luật dữ liệu: dùng nhãn/dải")
    return True


def verbatim(texts, sources, n=8):
    """Câu AI viết có chép nguyên ≥ n từ liền của bình luận/tiêu đề nguồn không (luật: diễn đạt lại, không trích)."""
    sh = set()
    for s in sources:
        w = re.findall(r"[\w']+", s.lower())
        sh.update(" ".join(w[i:i + n]) for i in range(len(w) - n + 1))
    bad = []
    for t in texts:
        w = re.findall(r"[\w']+", t.lower())
        if any(" ".join(w[i:i + n]) in sh for i in range(len(w) - n + 1)):
            bad.append(t)
    return bad
