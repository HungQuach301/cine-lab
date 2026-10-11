"""Đối chiếu lượt xem thật của kênh mình (`market own`, `market predict`, hiệu chỉnh).

- Đọc lượt xem CÔNG KHAI (viewCount) của video kênh mình đã đăng: channels.list (1 đơn vị) + videos.list (1 đơn vị/50 video);
  playlistItems (1 đơn vị) chỉ khi quota-policy cho phép, không thì dùng danh sách video_id trong gói kênh.
- Mỗi lần chạy ghi một ảnh chụp/tập vào `own.snapshots` (repo; số kênh mình, dạng tổng hợp theo video). Mốc 48 giờ / 7 ngày /
  28 ngày: ảnh chụp trong cửa sổ [mốc, mốc + max(24 giờ, 25 %)) → "đúng mốc"; có ảnh trước và sau → "nội suy"; tuổi < mốc →
  "chờ"; còn lại "lỡ mốc" (ghi số gần nhất kèm tuổi, không dùng để hiệu chỉnh).
- Dự đoán G1 (`predict`, công thức TẠM): dải theo lịch sử kênh ở cùng mốc, dịch theo nhãn cầu hiện hành.
- Hiệu chỉnh sau mỗi 3 tập có nhãn: Spearman(nhãn cầu, lượt xem 7 ngày). ρ > 0 → giữ; ρ ≤ 0 → sửa công thức hoặc giảm trọng.
Lượt xem/ngày, dải, ρ: tự tính, không phải chỉ số YouTube. viewCount là số công khai YouTube trả về lúc đọc.
"""
import datetime as dt, json, statistics as st
from pathlib import Path
from core import REPO, MarketError, get, pubdt, dur, write_atomic, LABEL_SELF

MILESTONES = (("48h", 48), ("7d", 168), ("28d", 672))
SCORE = {"Mạnh": 2, "Yếu": 1, "Không": 0}


def norm(t):
    return " ".join(t.lower().replace("’", "'").split())


def _path(pack, key):
    return REPO / pack["own"][key]


def load_snaps(pack):
    f = _path(pack, "snapshots")
    return [json.loads(l) for l in f.read_text().splitlines() if l.strip()] if f.exists() else []


def fetch(pack, quota, now=None):
    """Thu ảnh chụp lượt xem công khai hiện tại cho mọi tập của gói. Trả danh sách dòng ảnh chụp."""
    now = now or dt.datetime.now(dt.timezone.utc)
    own = pack["own"]
    ch = get(pack, quota, "channels", ttl_s=3600, part="snippet,statistics,contentDetails", forHandle=own["handle"])
    if not ch.get("items"):
        raise MarketError(f"không thấy kênh {own['handle']}")
    ch = ch["items"][0]
    eps = own["episodes"]
    known = {e["video_id"]: k for k, e in eps.items() if e.get("video_id")}
    found, unassigned = {}, []
    ok, _ = quota.method_ok("playlistItems")
    if ok and own.get("discover", True):
        j = get(pack, quota, "playlistItems", ttl_s=3600, part="snippet,contentDetails",
                playlistId=ch["contentDetails"]["relatedPlaylists"]["uploads"], maxResults=50)
        bytitle = {norm(t): k for k, e in eps.items() for t in (e["title"], e.get("yt_title") or e["title"])}
        for it in j.get("items", []):
            vid = it["contentDetails"]["videoId"]
            k = bytitle.get(norm(it["snippet"]["title"]))
            if k:
                found[vid] = k
            elif vid not in known:
                unassigned.append(vid)
    ids = list(dict.fromkeys(list(known) + list(found) + unassigned))
    rows, orphans = [], []
    items = []
    for i in range(0, len(ids), 50):
        items += get(pack, quota, "videos", ttl_s=3600, part="snippet,contentDetails,statistics",
                     id=",".join(ids[i:i + 50]), maxResults=50).get("items", [])
    if items:
        for v in items:
            k = known.get(v["id"]) or found.get(v["id"])
            if not k:                                    # video kênh mình chưa gán tập (đổi tiêu đề trên YouTube?)
                if dur(v["contentDetails"].get("duration")) >= pack["long_min_s"]:
                    orphans.append(dict(vid=v["id"], yt_title=v["snippet"]["title"]))
                continue
            age = (now - pubdt(v["snippet"]["publishedAt"])).total_seconds() / 3600
            if v["snippet"]["channelId"] != ch["id"]:
                raise MarketError(f"video {v['id']} không thuộc kênh {own['handle']} — sửa video_id trong gói")
            s = v.get("statistics", {})
            rows.append(dict(at=now.isoformat(timespec="minutes"), ep=k, vid=v["id"], pub=v["snippet"]["publishedAt"],
                             age_h=round(age, 1), views=int(s.get("viewCount", 0)), likes=int(s.get("likeCount", 0)),
                             comments=int(s.get("commentCount", 0)), dur_s=dur(v["contentDetails"].get("duration")),
                             yt_title=v["snippet"]["title"]))
    meta = dict(at=now.isoformat(timespec="minutes"), channel_videos=int(ch["statistics"].get("videoCount", 0)),
                n_found=len(rows), n_eps=len(eps), discovered=len(found), orphans=orphans,
                discover=("có" if ok and own.get("discover", True) else "không (quota-policy chặn playlistItems)"))
    return rows, meta


def milestone(snaps, ep, hours, now_age=None):
    """(trạng thái, lượt xem, tuổi giờ) của một tập ở một mốc."""
    s = sorted([x for x in snaps if x["ep"] == ep], key=lambda x: x["age_h"])
    if not s:
        return ("chưa có ảnh chụp", None, None)
    win = hours + max(24, 0.25 * hours)
    hit = [x for x in s if hours <= x["age_h"] < win]
    if hit:
        return ("đúng mốc", hit[0]["views"], hit[0]["age_h"])
    lo = [x for x in s if x["age_h"] < hours]
    hi = [x for x in s if x["age_h"] >= win]
    if lo and hi:
        a, b = lo[-1], hi[0]
        v = a["views"] + (b["views"] - a["views"]) * (hours - a["age_h"]) / (b["age_h"] - a["age_h"])
        return ("nội suy", round(v), hours)
    if s[-1]["age_h"] < hours:
        return ("chờ", None, None)
    return ("lỡ mốc", s[0]["views"], s[0]["age_h"]) if hi else ("chờ", None, None)


def rank(xs):
    o = sorted(range(len(xs)), key=lambda i: xs[i]); r = [0.0] * len(xs); i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and xs[o[j + 1]] == xs[o[i]]:
            j += 1
        for k in range(i, j + 1):
            r[o[k]] = (i + j) / 2
        i = j + 1
    return r


def spearman(a, b):
    ra, rb = rank(a), rank(b)
    ma, mb = st.mean(ra), st.mean(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** .5
    return round(num / den, 2) if den else None


def load_preds(pack):
    f = _path(pack, "predictions")
    return json.loads(f.read_text()) if f.exists() else {}


def calibrate(pack, snaps, preds):
    """Luật hiệu chỉnh sau mỗi 3 tập có nhãn cầu + số 7 ngày đúng mốc/nội suy."""
    pts = []
    for ep, p in preds.items():
        stt, v, _ = milestone(snaps, ep, 168)
        if p.get("label") in SCORE and stt in ("đúng mốc", "nội suy"):
            pts.append((ep, p["label"], v))
    n = len(pts)
    if n < 3:
        return dict(n=n, verdict=f"chưa đủ mẫu ({n}/3 tập có nhãn cầu + số 7 ngày đúng mốc)", rho=None, pts=pts)
    use = pts[: n - n % 3]                     # chỉ xét theo bội số 3 tập
    rho = spearman([SCORE[l] for _, l, _ in use], [v for *_, v in use])
    hi = [v for _, l, v in use if l == "Mạnh"]; lo = [v for _, l, v in use if l != "Mạnh"]
    if len(set(l for _, l, _ in use)) < 2:
        verdict = "mọi tập cùng một nhãn — chưa kiểm được thứ hạng; giữ trọng số TẠM"
    elif rho is not None and rho > 0 and (not hi or not lo or st.median(hi) > st.median(lo)):
        verdict = f"nhãn cầu xếp hạng đúng chiều (ρ = {rho}) — giữ công thức"
    else:
        verdict = f"nhãn cầu KHÔNG xếp hạng đúng (ρ = {rho}) — sửa công thức (demand.py) hoặc giảm trọng; ghi lý do ở đây"
    return dict(n=len(use), verdict=verdict, rho=rho, pts=use)


def predict(pack, snaps, label, n_min=3):
    """Dải TẠM cho 7 và 28 ngày: lịch sử kênh ở cùng mốc (chỉ số đúng mốc/nội suy), dịch theo nhãn cầu."""
    out = {}
    for key, h in (("7d", 168), ("28d", 672)):
        hist = sorted(v for ep in {x["ep"] for x in snaps}
                      for stt, v, _ in [milestone(snaps, ep, h)] if stt in ("đúng mốc", "nội suy"))
        if len(hist) < n_min:
            out[key] = dict(range=None, n=len(hist), note=f"chưa đủ lịch sử ({len(hist)}/{n_min} tập đúng mốc)")
            continue
        q = st.quantiles(hist, n=4, method="inclusive")
        lo, hi = {"Mạnh": (q[1], max(hist)), "Yếu": (q[0], q[2]), "Không": (min(hist), q[1])}.get(label, (q[0], q[2]))
        out[key] = dict(range=[round(lo), round(hi)], n=len(hist), note="lịch sử kênh, dịch theo nhãn cầu (TẠM)")
    return out


def g1_line(label_cur, label_dur, pr):
    f = lambda d: f"{d['range'][0]:,}–{d['range'][1]:,}".replace(",", " ") if d["range"] else d["note"]
    return (f"DỰ ĐOÁN (TẠM, `market.py predict`): nhãn cầu {label_cur} / bền {label_dur}; lượt xem 7 ngày {f(pr['7d'])}; "
            f"28 ngày {f(pr['28d'])} ({LABEL_SELF}). Đối chiếu ở `reports/m3/KHAN-GIA-SO.md`.")


def report_md(pack, snaps, preds, meta):
    eps = dict(pack["own"]["episodes"])
    for ep, p in preds.items():                    # tập có dự đoán G1 nhưng chưa vào gói: vẫn hiện, nhắc gán video
        eps.setdefault(ep, dict(title=f"({p.get('slug', '?')}) — chưa có trong own.episodes của gói", video_id=None))
    L = ["# KHÁN GIẢ THEO SỐ — Last Lamplighters (dự đoán G1 so với lượt xem thật)", "",
         "Máy sinh: `toolkit/market/market.py own --pack ll` (Việc 0 mỗi tập tự chạy). Nguồn: viewCount công khai qua YouTube Data "
         "API videos.list (1 đơn vị/50 video) — số của **kênh mình**, commit dạng tổng hợp theo video. Lượt xem/ngày, dải dự đoán, "
         f"ρ: **{LABEL_SELF}**. Ảnh chụp thô: `{pack['own']['snapshots']}`.",
         "> Dữ liệu chọn và định hướng; không quyết định nội dung hay hình. Sau 3 tập, phần nào của quy trình dữ liệu không có số đo "
         "chứng minh hiệu quả thì bỏ (CHUAN-KENH §14).", "",
         f"Lần đọc gần nhất: {meta.get('at', '—')} · kênh có {meta.get('channel_videos', '?')} video công khai (cả Shorts) · "
         f"tìm thấy {meta.get('n_found', 0)}/{meta.get('n_eps', len(eps))} tập trong gói · dò uploads: {meta.get('discover', '?')}.",
         *([f"- Video dài của kênh chưa gán tập (thêm `video_id`/`yt_title` vào gói): "
            + "; ".join(f"{o['vid']} \"{o['yt_title']}\"" for o in meta['orphans'])] if meta.get("orphans") else []), "",
         "| Tập | Video | Phút | Dự đoán G1 (nhãn · 7 ngày · 28 ngày) | 48 giờ | 7 ngày | 28 ngày | Lượt xem/ngày (gần nhất) | Trong dải 7 ngày? |",
         "|---|---|---|---|---|---|---|---|---|"]
    for ep, e in eps.items():
        s = sorted([x for x in snaps if x["ep"] == ep], key=lambda x: x["age_h"])
        p = preds.get(ep)
        pcell = "chưa có (tập trước luật dự đoán)" if not p else (
            f"{p['label']}/{p.get('durable', '?')} · " + " · ".join(
                (f"{d['range'][0]}–{d['range'][1]}" if d.get("range") else "chưa đủ lịch sử") for d in (p["7d"], p["28d"])))
        cells = []
        for name, h in MILESTONES:
            stt, v, age = milestone(snaps, ep, h)
            cells.append(f"{v} ({stt})" if stt in ("đúng mốc", "nội suy") else
                         f"lỡ mốc ({v} ở {age / 24:.0f} ngày)" if stt == "lỡ mốc" else stt)
        last = s[-1] if s else None
        vpd = f"{last['views'] / max(last['age_h'] / 24, 0.5):.1f} ({last['age_h'] / 24:.0f} ngày)" if last else "—"
        ins = "—"
        stt7, v7, _ = milestone(snaps, ep, 168)
        if p and p["7d"].get("range") and stt7 in ("đúng mốc", "nội suy"):
            lo, hi = p["7d"]["range"]
            ins = "trong" if lo <= v7 <= hi else ("trên" if v7 > hi else "dưới")
        vid = f"[{last['vid']}](https://youtu.be/{last['vid']})" if last else (e.get("video_id") or "chưa thấy trên kênh")
        mins = f"{last['dur_s'] / 60:.1f}" if last else "—"
        ytt = f"<br>YouTube: “{last['yt_title']}”" if last and last.get("yt_title") and last["yt_title"] != e["title"] else ""
        L.append(f"| {ep} {e['title']}{ytt} | {vid} | {mins} | {pcell} | {cells[0]} | {cells[1]} | {cells[2]} | {vpd} | {ins} |")
    c = calibrate(pack, snaps, preds)
    L += ["", "## Hiệu chỉnh nhãn cầu (sau mỗi 3 tập có nhãn)", f"- Kết luận hiện tại: **{c['verdict']}**.",
          "- Luật: Spearman(nhãn cầu hiện hành Mạnh 2 · Yếu 1 · Không 0, lượt xem 7 ngày đúng mốc/nội suy) trên bội số 3 tập; "
          "ρ > 0 và trung vị nhóm Mạnh > nhóm còn lại → giữ; ngược lại → sửa công thức `demand.py` hoặc giảm trọng nhãn cầu trong "
          "chọn đề tài, ghi lý do bên dưới. Trọng số hiện TẠM, chốt sau `channel-k2/CALIBRATION.md` (12/10).",
          "- Nhãn hồi tố 8 tập đầu: chờ `channel-k2/calib.py` (phiên k2, cần search.list) — khi có, ghi vào "
          f"`{pack['own']['predictions']}` với `\"retro\": true` (dùng để hiệu chỉnh, không tính là dự đoán G1).",
          "", "### Lần sửa công thức", "- (chưa có)", "",
          "## Phương án tuỳ chọn: YouTube Analytics API (CHƯA LÀM)",
          "- Cho CTR lượt hiển thị, thời lượng xem trung bình, giữ chân theo giây, nguồn lưu lượng (tìm kiếm/đề xuất/Shorts).",
          "- Cần OAuth 2.0 của chủ kênh (scope `yt-analytics.readonly`), refresh token lưu ngoài repo (bí mật môi trường), "
          "proxy hiện chỉ gắn khoá Data API → phải thêm luồng OAuth. Quota riêng, không trừ vào 10 000 đơn vị Data API.",
          "- Ưu: số giữ chân/CTR thật thay ảnh chụp Studio thủ công. Nhược: thiết lập OAuth một lần, rủi ro lộ token. "
          "Tác động: hiệu chỉnh theo giữ chân thay vì chỉ lượt xem. Chỉ làm khi chủ dự án yêu cầu (không phải việc chờ của quy trình tập).", ""]
    return "\n".join(L), c


def merged_snaps(pack, rows):
    """Ảnh chụp cũ + mới (một ảnh chụp/video/giờ: chạy lại trúng cache 1 giờ không nhân đôi). Chưa ghi đĩa."""
    old = load_snaps(pack)
    seen = {(x["vid"], x["at"][:13]) for x in old}
    return old + [r for r in rows if (r["vid"], r["at"][:13]) not in seen]


def snaps_text(snaps):
    return "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in snaps)
