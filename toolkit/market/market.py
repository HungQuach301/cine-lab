#!/usr/bin/env python3
"""toolkit/market — nhà máy dữ liệu thị trường dùng chung (gói kênh: `packs/<tên>.json`). README.md cùng thư mục.

  market.py purge                                        xoá số liệu thô > 30 ngày (mọi lệnh cũng tự chạy)
  market.py quota  --session S [--pack P] [--plan topic SLUG|own|niche KEY]   ước đơn vị + phần còn được dùng hôm nay
  market.py topic SLUG --pack P --session S [--cap N]    hồ sơ cầu → <out.profiles>/SLUG.md + labels.json
  market.py queue --pack P                               cột Cầu/Khoảng trống/Câu hỏi vào <out.queue>
  market.py own --pack P --session S [--cap N]           lượt xem công khai kênh mình → KHAN-GIA-SO.md
  market.py predict SLUG --ep EP --pack P                dòng DỰ ĐOÁN cho G1 (ghi predictions.json)
  market.py niche KEY --pack P --session S [--cap N]     thước "kênh mới bật được không"
Cờ chung: --used-elsewhere N (đơn vị phiên khác đã dùng hôm nay), --dry (không gọi mạng; ước và dừng).
Fail closed: mọi lỗi → "DỪNG:" + mã 2, không ghi đầu ra dở. Chỉ số: tự tính, không phải chỉ số YouTube.
"""
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from core import REPO, MarketError, load_pack, purge, write_atomic
import quota as Q


def _quota(a):
    return Q.Quota(a.session, a.cap, a.used_elsewhere, dry=a.dry)


def labels_path(pack):
    return REPO / pack["out"]["profiles"] / "labels.json"


def load_labels(pack):
    f = labels_path(pack)
    return json.loads(f.read_text()) if f.exists() else {}


def cmd_topic(a, pack):
    import demand, render
    if a.slug not in pack["topics"]:
        raise MarketError(f"đề tài {a.slug} chưa có trong gói {pack['name']} (thêm title + 2–6 câu hỏi khán giả)")
    t = pack["topics"][a.slug]
    q = _quota(a)
    units, msg = q.check_plan(Q.topic_plan(len(t["questions"]), len(t.get("durable_questions", t["questions"][:3]))))
    print(msg, flush=True)
    if a.dry:
        return
    raw = demand.build(pack, q, a.slug)
    demand.save_raw(pack, raw)
    s = demand.summary(raw)
    md = render.profile_md(s, pack)
    render.assert_repo_safe(md, raw["guard"])
    labels = load_labels(pack)
    labels[a.slug] = s
    lj = json.dumps(labels, ensure_ascii=False, indent=1)
    render.assert_repo_safe(lj, raw["guard"])
    write_atomic(REPO / pack["out"]["profiles"] / f"{a.slug}.md", md)
    write_atomic(labels_path(pack), lj + "\n")
    print(f"{a.slug}: cầu {s['current']} / bền {s['durable']} · khoảng trống {s['gap']} · dải {s['band']} · "
          f"đã dùng {q.run_units} đơn vị")


def cmd_queue(a, pack):
    import render
    f = REPO / pack["out"]["queue"]
    if not f.exists():
        raise MarketError(f"không có tệp hàng đợi {f}")
    block = render.queue_block(load_labels(pack), pack)
    write_atomic(f, render.replace_block(f.read_text(), block))
    print(block)


def cmd_own(a, pack):
    import own
    q = _quota(a)
    n = len([e for e in pack["own"]["episodes"].values() if e.get("video_id")])
    ok, _ = q.method_ok("playlistItems")
    units, msg = q.check_plan({"channels": 1, "playlistItems": int(ok), "videos": 1 + len(pack["own"]["episodes"]) // 50})
    print(msg, flush=True)
    if a.dry:
        return
    rows, meta = own.fetch(pack, q)
    snaps = own.merged_snaps(pack, rows)
    md, c = own.report_md(pack, snaps, own.load_preds(pack), meta)       # tính xong hết rồi mới ghi
    write_atomic(REPO / pack["own"]["snapshots"], own.snaps_text(snaps))
    write_atomic(REPO / pack["own"]["report"], md)
    print(f"ảnh chụp {len(rows)} tập (kênh {meta['channel_videos']} video; tìm qua uploads {meta['discovered']}) · "
          f"hiệu chỉnh: {c['verdict']} · đã dùng {q.run_units} đơn vị")


def cmd_predict(a, pack):
    import own
    lab = load_labels(pack).get(a.slug)
    cur = lab["current"] if lab else "chưa đo"
    dur = lab["durable"] if lab else "chưa đo"
    pr = own.predict(pack, own.load_snaps(pack), cur)
    preds = own.load_preds(pack)
    preds[a.ep] = dict(slug=a.slug, label=cur, durable=dur, made=lab["made"] if lab else None, **pr)
    write_atomic(REPO / pack["own"]["predictions"], json.dumps(preds, ensure_ascii=False, indent=1) + "\n")
    print(own.g1_line(cur, dur, pr))


def cmd_niche(a, pack):
    import niche
    if a.key not in pack.get("niches", {}):
        raise MarketError(f"gói {pack['name']} không có ngách {a.key}")
    q = _quota(a)
    units, msg = q.check_plan(niche.plan(pack, a.key))
    print(msg, flush=True)
    if not a.dry:
        print(json.dumps(niche.run(pack, q, a.key), ensure_ascii=False))


def cmd_quota(a, pack):
    q = Q.Quota(a.session, a.cap, a.used_elsewhere, dry=True)
    print(f"ngày quota {q.day} · sổ container này {q.used_local()} đơn vị · còn được dùng ≈ {q.room()} · "
          f"giữ hiện hành: {[h['why'] for h in q.holds()]}")
    if a.plan:
        kind = a.plan[0]
        if kind in ("topic", "niche") and (len(a.plan) < 2 or a.plan[1] not in pack.get(kind + "s", {})):
            raise MarketError(f"--plan {kind} cần tên có trong gói {pack['name']}")
        if kind == "topic":
            t = pack["topics"][a.plan[1]]
            plan = Q.topic_plan(len(t["questions"]), len(t.get("durable_questions", t["questions"][:3])))
        elif kind == "niche":
            import niche
            plan = niche.plan(pack, a.plan[1])
        else:
            plan = {"channels": 1, "playlistItems": int(q.method_ok("playlistItems")[0]), "videos": 1}
        try:
            print(q.check_plan(plan)[1], "→ CHẠY ĐƯỢC")
        except MarketError as e:
            print(e, "→ KHÔNG CHẠY")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["purge", "quota", "topic", "queue", "own", "predict", "niche"])
    ap.add_argument("arg", nargs="?")
    ap.add_argument("--pack", default="ll")
    ap.add_argument("--session")
    ap.add_argument("--cap", type=int, default=1000)
    ap.add_argument("--used-elsewhere", type=int, default=0)
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--ep")
    ap.add_argument("--plan", nargs="+")
    a = ap.parse_args(argv)
    try:
        gone = purge()
        if a.cmd == "purge":
            print(f"đã xoá {len(gone)} tệp thô > 30 ngày"); return 0
        pack = load_pack(a.pack)
        if a.cmd in ("quota", "topic", "own", "niche") and not a.session:
            raise MarketError("thiếu --session (tên phiên trong quota-policy.json: priority)")
        a.slug = a.key = a.arg
        if a.cmd in ("topic", "predict", "niche") and not a.arg:
            raise MarketError(f"{a.cmd} cần đối số")
        if a.cmd == "predict" and not a.ep:
            raise MarketError("predict cần --ep (khoá tập trong own.episodes, vd ep09)")
        {"topic": cmd_topic, "queue": cmd_queue, "own": cmd_own, "predict": cmd_predict,
         "niche": cmd_niche, "quota": cmd_quota}[a.cmd](a, pack)
        return 0
    except MarketError as e:
        print(f"DỪNG: {e}", file=sys.stderr)
        return 2
    except Exception as e:                       # lỗi không lường: vẫn dừng hẳn, không ghi đầu ra dở
        print(f"DỪNG (lỗi không lường): {type(e).__name__}: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
