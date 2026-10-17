#!/usr/bin/env python3
"""PACKAGING-BRIEF cho một tập (CHUAN-KENH-LL §14 bước 5; học Crux `toolkit/market/brief.py` + `templates/PACKAGING-BRIEF.md`).

Nhà máy làm brief + 2–3 ảnh nền 1280×720 KHÔNG chữ; chủ dự án tự tạo thumbnail bằng công cụ ảnh theo brief.
Nhà máy KHÔNG làm thumbnail hoàn chỉnh. Mọi kiểm ở đây là **đọc, không chặn** (in CẢNH BÁO, mã thoát 0).

  /opt/cine/bin/python toolkit/market/brief.py --ep ep09 --slug <hồ sơ cầu> --video <bản 1080p> --at 12.5,301,540 \
      --titles "A?|B?|C?" --thumb-text "FOUR WORDS MAX" --objects "headphones, interpreter booth" \
      --paradox "machines arrived, the job changed instead of vanishing" --claims reports/m3/epNN/claims.txt [--pack ll]
→ reports/m3/<ep>/phat-hanh/PACKAGING-BRIEF.md + nen-1.jpg … (ảnh nền: khung cảnh đinh không phụ đề/chú thích — P chọn mốc).
`--claims`: một dòng một số/năm được phép (đúng như trên hình/lời, có nguồn). Hồ sơ cầu: reports/m3/topics/labels.json.

BRIEF THUMBNAIL A/B (mẫu TEARDOWN-FON §9, phiên V5a 15/10/2026) — 2 phương án KHÁC Ý ĐỒ cho Test & Compare:
  /opt/cine/bin/python toolkit/market/brief.py ab --ep k2c-t3-01 --title "Why …?" --claims <tệp> [--colors "A=#2e8b57,B=#c0392b"] \
      --a-subject "…" --a-text "2 WORDS" --a-contrast "vạch chia: …" [--a-ref "…"] [--a-text-colors "#ffffff/#111111"] \
      --b-subject "…" [--b-text ""] --b-contrast "quá khứ ↔ hiện tại: …" [--b-ref "…"] [--out <thư mục>]
→ <out>/THUMBNAIL-BRIEF-AB.md (mặc định reports/m3/<ep>/phat-hanh/). [A] BẢN ĐỒ TƯƠNG PHẢN · [B] CƠ CHẾ LỘ RA (không chữ khuyến nghị).
Mỗi phương án: chủ thể, chữ ≤ 4 từ, tương phản (thủ pháp + tỉ lệ tương phản chữ khi khai màu), tham chiếu ngách. Kiểm đọc, không chặn.
"""
import argparse, json, re, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from core import REPO, MarketError, load_pack, write_atomic

# Học từ tập 6 trên kênh: tiêu đề dạng câu hỏi tìm kiếm ("Will AI Replace Graphic Designers? History Has a Clue")
# 129 lượt/4 ngày so với 4–10 lượt các tập khác (KHAN-GIA-SO 11/10; một tập, chưa phải bằng chứng thống kê).
FORBIDDEN = [r"\byour job is next\b", r"\bwill (?:definitely|surely)\b", r"\bguarantee", r"\bshocking\b", r"\bdestroy",
             r"\bend of\b", r"\bnobody\b", r"\beveryone\b", r"\bsecret\b"]
# Cụm cấm RIÊNG từng gói (gói ll không đổi). k2: QUAN-TRI-RUI-RO.md §1.2 điểm 4 (bẫy "who really controls…"); chủ dự án duyệt 12/10/2026 (D7, tập K2G-01).
FORBIDDEN_PACK = {"k2": [r"\bwho (?:really )?controls\b"]}
SAFE = 0.05          # lề an toàn 5 % mỗi cạnh (như thumb.py, BAI-HOC #9)
TIMESTAMP_BOX = "góc dưới phải ~ 18 % × 12 % (YouTube phủ thời lượng)"


def num_tokens(t):
    return re.findall(r"\d[\d,.]*%?", t)


def check_title(t, allowed, extra=()):
    w = []
    if len(t) > 70:
        w.append(f"dài {len(t)} ký tự (> 70, bị cắt trên di động)")
    if "?" not in t:
        w.append("không ở dạng câu hỏi tìm kiếm")
    for n in num_tokens(t):
        if n.rstrip(".,") not in allowed:
            w.append(f"số '{n}' không có trong danh sách claim được phép")
    for p in FORBIDDEN:
        if re.search(p, t, re.I):
            w.append(f"cụm hứa vượt claim/giật gân: /{p}/")
    for p in extra:
        if re.search(p, t, re.I):
            w.append(f"cụm cấm của gói (QUAN-TRI-RUI-RO §1.2): /{p}/")
    return w


def check_thumb_text(t, allowed, extra=()):
    w = []
    if len(t.split()) > 4:
        w.append(f"{len(t.split())} từ (> 4)")
    for n in num_tokens(t):
        if n.rstrip(".,") not in allowed:
            w.append(f"số '{n}' không có trong danh sách claim được phép")
    for p in FORBIDDEN:
        if re.search(p, t, re.I):
            w.append(f"cụm hứa vượt claim: /{p}/")
    for p in extra:
        if re.search(p, t, re.I):
            w.append(f"cụm cấm của gói (QUAN-TRI-RUI-RO §1.2): /{p}/")
    return w


def frames(video, ats, outdir):
    """Ảnh nền 1280×720 không chữ từ bản 1080p ở các mốc P chọn (cảnh đinh không phụ đề). Trả (tên tệp, bảng màu hex)."""
    from PIL import Image
    for old in outdir.glob("nen-*.jpg"):              # không bao giờ dùng lại khung cũ
        old.unlink()
    out = []
    for i, t in enumerate(ats, 1):
        f = outdir / f"nen-{i}.jpg"
        r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t}", "-i", str(video), "-frames:v", "1",
                            "-vf", "scale=1280:720:flags=lanczos", "-q:v", "2", str(f)], capture_output=True, text=True)
        if r.returncode or not f.exists():
            for g in outdir.glob("nen-*.jpg"):
                g.unlink()
            raise MarketError(f"ffmpeg không lấy được khung ở {t}s: {r.stderr.strip()[:200]}")
        im = Image.open(f).convert("RGB")
        if im.size != (1280, 720):
            raise MarketError(f"{f.name} không phải 1280×720")
        pal = im.resize((128, 72)).quantize(colors=5, method=Image.Quantize.MEDIANCUT).convert("RGB")
        cols = sorted(pal.getcolors(128 * 72), reverse=True)[:5]
        out.append((f.name, ["#%02x%02x%02x" % c for _, c in cols]))
    return out


def build(a):
    pack = load_pack(a.pack)
    try:                                               # kiểm mọi đầu vào TRƯỚC khi ghi gì
        ats = [float(x) for x in a.at.split(",")] if a.video else []
    except ValueError:
        raise MarketError(f"--at phải là các mốc giây cách nhau dấu phẩy, đang là {a.at!r}")
    if a.video and not 2 <= len(ats) <= 3:
        raise MarketError("cần 2–3 ảnh nền (--at t1,t2[,t3])")
    if a.video and not Path(a.video).is_file():
        raise MarketError(f"không có tệp video {a.video}")
    if a.claims and not Path(a.claims).is_file():
        raise MarketError(f"không có tệp claim {a.claims}")
    lab = json.loads((REPO / pack["out"]["profiles"] / "labels.json").read_text()).get(a.slug) \
        if (REPO / pack["out"]["profiles"] / "labels.json").exists() else None
    allowed = {l.strip() for l in Path(a.claims).read_text().splitlines() if l.strip() and not l.startswith("#")} if a.claims else set()
    titles = [t.strip() for t in a.titles.split("|") if t.strip()]
    if len(titles) != 3:
        raise MarketError("cần đúng 3 phương án tiêu đề (--titles \"A|B|C\")")
    outdir = REPO / "reports/m3" / a.ep / "phat-hanh"
    outdir.mkdir(parents=True, exist_ok=True)
    fr = frames(Path(a.video), ats, outdir) if a.video else []
    extra = FORBIDDEN_PACK.get(a.pack, ())
    warn = {f"Tiêu đề {chr(65 + i)}": check_title(t, allowed, extra) for i, t in enumerate(titles)}
    warn["Chữ thumbnail"] = check_thumb_text(a.thumb_text, allowed, extra)
    pats = lab["title_patterns"] if lab else ["(chưa có hồ sơ cầu — dùng dạng câu hỏi tìm kiếm của tập 6)"]
    qs = [q["q_en"] for q in lab["questions"]] if lab else []
    kw = lab.get("keywords", []) if lab else []
    L = [f"# PACKAGING-BRIEF — {a.ep} · {titles[0]}", "",
         "Máy sinh (`toolkit/market/brief.py`, CHUAN-KENH-LL §14 bước 5). Nhà máy **không** làm thumbnail hoàn chỉnh: chủ dự án tự tạo "
         "2–3 thumbnail bằng công cụ ảnh theo brief này, rồi bật **YouTube Test & Compare**; CTR bản thắng ghi vào "
         f"`reports/m3/{a.ep}/KHAN-GIA.md`. Kiểm dưới đây là **đọc, không chặn**.", "",
         "## 1. Tiêu đề — 3 phương án dạng câu hỏi tìm kiếm",
         f"Khuôn thắng (hồ sơ cầu `{a.slug}`): " + " · ".join(pats),
         ("Cụm tìm kiếm (đặt sớm trong tiêu đề và 2 dòng đầu mô tả): " + ", ".join(kw)) if kw else "Cụm tìm kiếm: chưa có hồ sơ cầu.",
         ("Câu hỏi khán giả tập trả lời: " + " · ".join(qs[:3])) if qs else "", ""]
    L += [f"{chr(65 + i)}. **{t}** ({len(t)} ký tự)" for i, t in enumerate(titles)]
    L += ["", "## 2. Thumbnail (chủ dự án tạo)",
          f"- **Ý:** {a.objects} — đúng tên gọi trong lời; một ý duy nhất, đọc được ở cỡ điện thoại (168×94).",
          f"- **Cảm xúc / nghịch lý cần thể hiện:** {a.paradox}.",
          f"- **Chữ (≤ 4 từ):** `{a.thumb_text}`.",
          f"- **Bố cục:** vật thể trung tâm lệch trái theo 1/3; chữ khối lớn bên phải; mọi chữ trong vùng an toàn {int(SAFE * 100)} % mỗi cạnh, "
          f"tránh {TIMESTAMP_BOX}; không mặt người, không logo, không ảnh người thật, không mũi tên dự báo.",
          "- **Bảng màu:** lấy từ ảnh nền (đo trên khung, không đoán): " + (" · ".join(f"{n}: {' '.join(c)}" for n, c in fr) or "chưa có ảnh nền") +
          ". Kiểu được chấm mù cao nhất qua các tập: cảnh đêm/chạng vạng có nguồn sáng ấm (TAP8-G2, Q27).",
          "- **Ảnh nền (1280×720, không chữ, từ cảnh đinh 1080p):** " + (", ".join(f"`{n}`" for n, _ in fr) or "chưa lấy (thiếu --video)"),
          "", "### Prompt mẫu (dán vào công cụ tạo ảnh, đính kèm một ảnh nền)", "```",
          f"YouTube thumbnail, 1280x720. Use the attached frame as the background and keep its stylized low-poly 3D look, lighting and colours. "
          f"Make {a.objects} the single clear focal point. Mood: {a.paradox}. Add the text \"{a.thumb_text}\" in large bold sans-serif, "
          f"high contrast (at least 4.5:1), inside a 5% safe margin, not in the bottom-right corner. No faces, no logos, no real photos, "
          f"no arrows, no extra text, no numbers other than those in the text.", "```",
          "", "## 3. Kiểm (đọc, không chặn)"]
    for k, w in warn.items():
        L.append(f"- {k}: " + ("ĐẠT" if not w else "CẢNH BÁO — " + "; ".join(w)))
    L += ["- Chữ trên thumbnail chủ dự án tạo: P đọc ảnh — chữ trong vùng an toàn 5 %, không ở góc thời lượng, không số ngoài claim. "
          "Ghi kết quả vào HUONG-DAN-DANG của tập.",
          f"- Claim được phép: {', '.join(sorted(allowed)) or '(chưa nạp --claims: mọi số trong tiêu đề/chữ bị cảnh báo)'}", ""]
    write_atomic(outdir / "PACKAGING-BRIEF.md", "\n".join(L))
    return outdir / "PACKAGING-BRIEF.md", warn


# ---- BRIEF THUMBNAIL A/B (TEARDOWN-FON §9) -------------------------------------------------------------------------------
# Tham chiếu ngách = công thức tả bằng lời (TEARDOWN-FON §4), KHÔNG chép hình/chữ của kênh khác.
AB = {
    "A": dict(ten="BẢN ĐỒ TƯƠNG PHẢN", contrast=("vạch chia", "mũi tên"), max_words_goi_y=2,
              ref="ngữ pháp kênh địa lý–kinh tế thắng (TEARDOWN-FON §4, FoN): bản đồ nổi thật + 1–2 vùng tô bão hoà viền trắng + "
                  "hộp tối 1–2 từ hoặc số + 1 từ; video lớn nhất có ít yếu tố nhất",
              nen="bản đồ nổi thật của chính tập (render relief của mình), bảng màu tự nhiên; tầm vùng nhận ra hình dạng nơi chốn ở 168×94 px",
              them="1–2 vùng tô theo MÃ MÀU CỐ ĐỊNH của tập, viền trắng, quầng sáng ≤ 0,2; ≤ 2 sticker vật 3D của bộ k2v đặt đúng chỗ"),
    "B": dict(ten="CƠ CHẾ LỘ RA", contrast=("mặt cắt", "quá khứ", "trước"), max_words_goi_y=0,
              ref="ngữ pháp kênh công trình thắng (TEARDOWN-FON §4, GoDocs): không chữ, mặt cắt/đối lập quá khứ–hiện tại lộ cơ chế dưới "
                  "một vật nổi tiếng trên mặt đất; hình tự dựng, không dáng AI",
              nen="một vật/nơi nổi tiếng của tập: render 3D tự dựng hoặc ảnh tài sản công đã kiểm giấy phép",
              them="không mặt người làm tiêu điểm; không hình dáng AI tả thực nơi có thật (nếu có → nhãn AI theo QUAN-TRI-RUI-RO §2)"),
}
STOP = {"the", "a", "an", "of", "and", "to", "in", "is", "it", "why", "how", "so", "its", "it's", "not", "just", "does", "do", "did", "what", "this"}


def hex_rgb(h):
    h = h.strip().lstrip("#")
    if not re.fullmatch(r"[0-9a-fA-F]{6}", h):
        raise MarketError(f"màu phải dạng #rrggbb, đang là {h!r}")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def contrast_ratio(c1, c2):
    """tỉ lệ tương phản WCAG 2.x giữa hai màu #rrggbb."""
    def lum(c):
        v = [x / 255 for x in hex_rgb(c)]
        v = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in v]
        return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]
    a, b = sorted((lum(c1), lum(c2)), reverse=True)
    return round((a + 0.05) / (b + 0.05), 2)


def words(t): return [w for w in re.findall(r"[\w$%.,'’]+", t or "") if re.search(r"\w", w)]


def check_ab_option(k, o, title, allowed, extra=()):
    """cảnh báo (đọc, không chặn) cho một phương án."""
    spec, w = AB[k], []
    n = len(words(o["text"]))
    if n > 4:
        w.append(f"chữ {n} từ (> 4)")
    elif n > spec["max_words_goi_y"]:
        w.append(f"chữ {n} từ — TEARDOWN §9 gợi ý " + ("tối đa 2 từ hoặc 1 số + 1 từ" if k == "A" else "KHÔNG chữ cho ngữ pháp B"))
    if k == "A" and n == 0:
        w.append("ngữ pháp A cần 1 hộp chữ (1–2 từ hoặc số + từ)")
    if not o["subject"].strip():
        w.append("thiếu chủ thể")
    if not any(c in o["contrast"].lower() for c in spec["contrast"]):
        w.append(f"thủ pháp tương phản nên là một trong: {', '.join(spec['contrast'])} (đang là {o['contrast']!r})")
    for x in num_tokens(o["text"]):
        if x.rstrip(".,") not in allowed:
            w.append(f"số '{x}' không có trong danh sách claim được phép")
    for p in FORBIDDEN + list(extra):
        if re.search(p, o["text"], re.I):
            w.append(f"cụm cấm/hứa vượt claim: /{p}/")
    tw = {x.lower().strip(".,?") for x in words(title)} - STOP
    rep = [x for x in words(o["text"]) if x.lower().strip(".,?") in tw]
    if rep:
        w.append(f"chữ lặp tiêu đề ({', '.join(rep)}) — tiêu đề hỏi, thumbnail cho thấy")
    if o.get("text_colors"):
        fg, bg = o["text_colors"].split("/")
        r = contrast_ratio(fg, bg); o["ratio"] = r
        if r < 4.5:
            w.append(f"tương phản chữ {r}:1 < 4,5:1")
        elif r < 4.5 * 1.05:
            w.append(f"tương phản chữ {r}:1 sát ngưỡng 4,5:1 (±5 %)")
    elif n:
        w.append("chưa khai màu chữ/nền hộp (--a-text-colors \"#fff/#111\") — không đo được tương phản")
    return w


def check_ab_title(t, allowed, extra=()):
    w = []
    if len(t) > 60:
        w.append(f"dài {len(t)} ký tự (> 60, TEARDOWN §6)")
    if not t.lower().startswith("why"):
        w.append("không mở bằng \"Why\" (công thức TEARDOWN §6)")
    if re.search("[\U0001F300-\U0001FAFF\u2600-\u27BF]", t):
        w.append("có emoji")
    for x in num_tokens(t):
        if x.rstrip(".,") not in allowed:
            w.append(f"số '{x}' không có trong danh sách claim được phép")
    for p in FORBIDDEN + list(extra) + [r"\bhidden\b", r"\binsane\b", r"\bimpossible\b"]:
        if re.search(p, t, re.I):
            w.append(f"cụm cấm/giật gân: /{p}/")
    return w


def build_ab(a):
    if a.claims and not Path(a.claims).is_file():
        raise MarketError(f"không có tệp claim {a.claims}")
    allowed = {l.strip() for l in Path(a.claims).read_text().splitlines() if l.strip() and not l.startswith("#")} if a.claims else set()
    opts = {k: dict(subject=getattr(a, f"{k.lower()}_subject"), text=getattr(a, f"{k.lower()}_text") or "",
                    contrast=getattr(a, f"{k.lower()}_contrast"), ref=getattr(a, f"{k.lower()}_ref") or AB[k]["ref"],
                    text_colors=getattr(a, f"{k.lower()}_text_colors")) for k in AB}
    for k, o in opts.items():
        if o["text_colors"] and o["text_colors"].count("/") != 1:
            raise MarketError(f"--{k.lower()}-text-colors phải dạng \"#chữ/#nền\"")
    if opts["A"]["subject"].strip().lower() == opts["B"]["subject"].strip().lower():
        raise MarketError("hai phương án trùng chủ thể — A/B phải khác ý đồ")
    cols = dict(x.split("=", 1) for x in a.colors.split(",")) if a.colors else {}
    for c in cols.values():
        hex_rgb(c)
    pack = FORBIDDEN_PACK.get(a.pack, ())
    warn = {"Tiêu đề": check_ab_title(a.title, allowed, pack)}
    for k, o in opts.items():
        warn[f"Phương án {k}"] = check_ab_option(k, o, a.title, allowed, pack)
    if opts["A"]["text"].strip() and opts["A"]["text"].strip().lower() == opts["B"]["text"].strip().lower():
        warn["Phương án B"].append("chữ trùng phương án A — biến thể chữ là bản thứ 3 của Test & Compare, không phải B")
    L = [f"# THUMBNAIL BRIEF — {a.ep}", "",
         "Máy sinh (`toolkit/market/brief.py ab`, mẫu TEARDOWN-FON §9). Chủ dự án tự làm thumbnail theo brief; nhà máy không làm thumbnail hoàn chỉnh. "
         "Kiểm dưới đây là **đọc, không chặn**.", "",
         f"Tiêu đề kèm: **{a.title}** ({len(a.title)} ký tự)",
         "Ngữ pháp chọn: [A] BẢN ĐỒ TƯƠNG PHẢN | [B] CƠ CHẾ LỘ RA (không chữ) — Test & Compare chạy A vs B (+ bản 3 = A với chữ khác: số ↔ từ).",
         "Mã màu hai phía: " + (" · ".join(f"{k} {v}" for k, v in cols.items()) if cols else "(chưa khai --colors — lấy MÃ MÀU CỐ ĐỊNH của tập)"), ""]
    for k, o in opts.items():
        s = AB[k]
        L += [f"## [{k}] {s['ten']}", "",
              "| Mục | Nội dung |", "|---|---|",
              f"| Chủ thể | {o['subject']} |",
              f"| Chữ (≤ 4 từ) | {('`' + o['text'] + '`') if o['text'].strip() else 'KHÔNG CHỮ'} ({len(words(o['text']))} từ) |",
              f"| Tương phản | thủ pháp: {o['contrast']}" + (f"; chữ/nền hộp {o['text_colors']} = **{o['ratio']}:1** (≥ 4,5:1)" if o.get('ratio') else "") + " |",
              f"| Tham chiếu ngách | {o['ref']} |",
              f"| Nền | {s['nen']} |",
              f"| Thêm | {s['them']} |", ""]
    L += ["## Chung (kiểm đọc, không chặn)",
          "- Tiêu đề: “Why …” + tên nơi + nghịch lý/cặp tương phản, ≤ 60 ký tự, không emoji, không từ cấm.",
          "- Thumbnail không lặp chữ của tiêu đề; tiêu đề hỏi, thumbnail cho thấy.",
          f"- Lề an toàn {int(SAFE * 100)} %; tránh {TIMESTAMP_BOX}; đọc được ở 168×94.",
          "- Không logo công ty, không cờ làm điểm nhấn, không bạch tuộc/con rối/tay khổng lồ.",
          "- Mọi hình và số trên thumbnail có trong video (QUAN-TRI-RUI-RO §4 mục 2).",
          "- Ghi: ảnh nền (tệp/khung), nguồn ảnh tài sản công (ID LoC/NARA), mã màu hai phía.",
          "- Test & Compare: 3 bản = A, B, và A với chữ khác (số ↔ từ); ghi kết quả vào SO-LIEU-7-NGAY.md của tập.", "",
          "## Kết quả kiểm"]
    for k, w in warn.items():
        L.append(f"- {k}: " + ("ĐẠT" if not w else "CẢNH BÁO — " + "; ".join(w)))
    L += [f"- Claim được phép: {', '.join(sorted(allowed)) or '(chưa nạp --claims: mọi số bị cảnh báo)'}", ""]
    outdir = Path(a.out) if a.out else REPO / "reports/m3" / a.ep / "phat-hanh"
    outdir.mkdir(parents=True, exist_ok=True)
    write_atomic(outdir / "THUMBNAIL-BRIEF-AB.md", "\n".join(L))
    return outdir / "THUMBNAIL-BRIEF-AB.md", warn


def main_ab(argv):
    ap = argparse.ArgumentParser(prog="brief.py ab", description="Brief thumbnail A/B theo TEARDOWN-FON §9")
    ap.add_argument("--ep", required=True); ap.add_argument("--title", required=True); ap.add_argument("--pack", default="k2")
    ap.add_argument("--claims"); ap.add_argument("--colors"); ap.add_argument("--out")
    for k in ("a", "b"):
        ap.add_argument(f"--{k}-subject", required=True); ap.add_argument(f"--{k}-text", default="")
        ap.add_argument(f"--{k}-contrast", required=True); ap.add_argument(f"--{k}-ref"); ap.add_argument(f"--{k}-text-colors")
    a = ap.parse_args(argv)
    try:
        f, warn = build_ab(a)
    except MarketError as e:
        print(f"DỪNG: {e}", file=sys.stderr); return 2
    n = sum(len(w) for w in warn.values())
    print(f"{f.relative_to(REPO) if f.is_relative_to(REPO) else f} · cảnh báo {n} (đọc, không chặn)")
    return 0


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv and argv[0] == "ab":
        return main_ab(argv[1:])
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ep", required=True); ap.add_argument("--slug", required=True); ap.add_argument("--pack", default="ll")
    ap.add_argument("--video"); ap.add_argument("--at", default="")
    ap.add_argument("--titles", required=True); ap.add_argument("--thumb-text", required=True)
    ap.add_argument("--objects", required=True); ap.add_argument("--paradox", required=True); ap.add_argument("--claims")
    a = ap.parse_args(argv)
    try:
        f, warn = build(a)
    except MarketError as e:
        print(f"DỪNG: {e}", file=sys.stderr); return 2
    except Exception as e:                             # đầu vào hỏng (labels.json…): dừng gọn, không traceback
        print(f"DỪNG (lỗi không lường): {type(e).__name__}: {e}", file=sys.stderr); return 2
    n = sum(len(w) for w in warn.values())
    print(f"{f.relative_to(REPO)} · cảnh báo {n} (đọc, không chặn)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
