#!/usr/bin/env python3
"""PACKAGING-BRIEF cho một tập (CHUAN-KENH-LL §14 bước 5; học Crux `toolkit/market/brief.py` + `templates/PACKAGING-BRIEF.md`).

Nhà máy làm brief + 2–3 ảnh nền 1280×720 KHÔNG chữ; chủ dự án tự tạo thumbnail bằng công cụ ảnh theo brief.
Nhà máy KHÔNG làm thumbnail hoàn chỉnh. Mọi kiểm ở đây là **đọc, không chặn** (in CẢNH BÁO, mã thoát 0).

  /opt/cine/bin/python toolkit/market/brief.py --ep ep09 --slug <hồ sơ cầu> --video <bản 1080p> --at 12.5,301,540 \
      --titles "A?|B?|C?" --thumb-text "FOUR WORDS MAX" --objects "headphones, interpreter booth" \
      --paradox "machines arrived, the job changed instead of vanishing" --claims reports/m3/epNN/claims.txt [--pack ll]
→ reports/m3/<ep>/phat-hanh/PACKAGING-BRIEF.md + nen-1.jpg … (ảnh nền: khung cảnh đinh không phụ đề/chú thích — P chọn mốc).
`--claims`: một dòng một số/năm được phép (đúng như trên hình/lời, có nguồn). Hồ sơ cầu: reports/m3/topics/labels.json.
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


def main(argv=None):
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
