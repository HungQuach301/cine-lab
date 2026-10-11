"""toolkit/market — test bằng dữ liệu giả (fixtures/market/*.json + router giả), KHÔNG gọi mạng, KHÔNG gọi AI thật.
Chạy: /opt/cine/bin/python -m unittest toolkit/tests/test_market.py -v
"""
import datetime as dt, json, os, re, shutil, sys, tempfile, time, unittest
from pathlib import Path

MK = Path(__file__).resolve().parents[1] / "market"
FX = Path(__file__).resolve().parent / "fixtures" / "market"
sys.path.insert(0, str(MK))
import core, quota as Q, ai, demand, render, own, market  # noqa: E402

NOW = dt.datetime.now(dt.timezone.utc)
iso = lambda d: (NOW - dt.timedelta(days=d)).strftime("%Y-%m-%dT%H:%M:%SZ")


class World:
    """YouTube giả: dựng từ fixtures/market/world.json (tuổi tính theo ngày so với lúc chạy test)."""
    def __init__(self, fail=None):
        w = json.loads((FX / "world.json").read_text())
        self.v = {x["id"]: x for x in w["videos"]}
        self.c = {x["id"]: x for x in w["channels"]}
        self.fail, self.calls = fail or {}, []

    def vitem(self, x):
        return {"id": x["id"], "snippet": {"channelId": x["ch"], "channelTitle": self.c[x["ch"]]["name"], "title": x["title"],
                                         "description": x.get("desc", ""), "publishedAt": iso(x["age_d"])},
                "contentDetails": {"duration": f"PT{x['min']}M"}, "statistics": {"viewCount": str(x["views"]), "likeCount": "3", "commentCount": "2"}}

    def __call__(self, url, p):
        ep = url.rsplit("/", 1)[-1]
        self.calls.append(ep)
        if ep in self.fail:
            return self.fail[ep], "{}"
        if ep == "search":
            ids = [i for i, x in self.v.items() if not x.get("own")]
            if "publishedAfter" in p:
                ids = [i for i in ids if self.v[i]["age_d"] <= 90]
            return 200, json.dumps({"items": [{"id": {"videoId": i}} for i in ids]})
        if ep == "videos":
            return 200, json.dumps({"items": [self.vitem(self.v[i]) for i in p["id"].split(",") if i in self.v]})
        if ep == "channels":
            ids = [i for i, c in self.c.items() if c.get("handle") == p["forHandle"]] if "forHandle" in p else p["id"].split(",")
            return 200, json.dumps({"items": [{"id": i, "snippet": {"title": self.c[i]["name"], "publishedAt": iso(self.c[i]["age_d"]),
                                                                  "description": ""},
                                               "statistics": {"subscriberCount": str(self.c[i]["subs"]), "videoCount": str(sum(v["ch"] == i for v in self.v.values()))},
                                               "contentDetails": {"relatedPlaylists": {"uploads": "UU" + i}}} for i in ids if i in self.c]})
        if ep == "playlistItems":
            ch = p["playlistId"][2:]
            return 200, json.dumps({"items": [{"snippet": {"title": x["title"], "publishedAt": iso(x["age_d"])},
                                               "contentDetails": {"videoId": i, "videoPublishedAt": iso(x["age_d"])}}
                                              for i, x in self.v.items() if x["ch"] == ch]})
        if ep == "commentThreads":
            return 200, json.dumps({"items": [{"id": f"c{p['videoId']}{k}", "snippet": {"totalReplyCount": k, "topLevelComment": {
                "snippet": {"textDisplay": t, "likeCount": 5 - k}}}} for k, t in enumerate(json.loads((FX / "comments.json").read_text()))]})
        return 404, "{}"


def fake_ai(off_topic=("vidAAAAAAA3",), drop_ids=()):
    def run(model, prompt, cwd, budget):
        ids = [l.split(" | ")[0] for l in prompt.splitlines() if " | " in l]
        if '"on_topic"' in prompt:
            r = {i: {"on_topic": i not in off_topic} for i in ids if i not in drop_ids}
        elif '"real_data"' in prompt:
            r = {i: {"real_data": i == ids[0]} for i in ids}
        elif '"k":' in prompt:
            kinds = ["question", "situation", "rebuttal", "request", "drop"]
            r = {i: {"k": kinds[n % 5], "gist": "paraphrased point"} for n, i in enumerate(ids)}
        else:
            r = json.loads((FX / "synth.json").read_text())
        return {"result": "```json\n" + json.dumps(r) + "\n```", "total_cost_usd": 0.01, "modelUsage": {model: {}}}
    return run


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.data, self.repo = self.tmp / "data", self.tmp / "repo"
        os.environ["MARKET_DATA"] = str(self.data)
        for d in ("reports/m3/topics", "topics", "reports/m3/khan-gia"):
            (self.repo / d).mkdir(parents=True)
        (self.repo / "topics/queue.md").write_text("# Hàng đề tài\n\nbảng cũ giữ nguyên\n")
        self._saved = (core.REPO, market.REPO, own.REPO, core.http_get, ai._run, Q.load_policy, market.load_pack)
        core.REPO = market.REPO = own.REPO = self.repo
        self.world = World()
        core.http_get = self.world
        ai._run = fake_ai()
        self.pack = core.load_pack("ll")
        self.policy = json.loads((FX / "policy.json").read_text())
        Q.load_policy = lambda path=None: self.policy

    def tearDown(self):
        core.REPO, market.REPO, own.REPO, core.http_get, ai._run, Q.load_policy, market.load_pack = self._saved
        os.environ.pop("MARKET_DATA", None)
        shutil.rmtree(self.tmp)

    def q(self, session="ll", cap=1000, **kw):
        return Q.Quota(session, cap, policy=self.policy, **kw)


class TestCore(Base):
    def test_purge_30_days_keeps_ledger(self):
        d = core.pack_dir(self.pack)
        old, new, led = d / "api_old.json", d / "api_new.json", d / "ai-ledger.jsonl"
        for f in (old, new, led):
            f.write_text("{}")
        t = time.time() - 31 * 86400
        os.utime(old, (t, t)); os.utime(led, (t, t))
        gone = core.purge()
        self.assertEqual(gone, [old])
        self.assertTrue(new.exists() and led.exists())

    def test_data_inside_git_refused(self):
        os.environ["MARKET_DATA"] = str(MK / "_data_in_repo")
        try:
            with self.assertRaises(core.MarketError):
                core.data_root()
        finally:
            shutil.rmtree(MK / "_data_in_repo", ignore_errors=True)

    def test_pack_requires_pinned_models(self):
        bad = json.loads((MK / "packs/ll.json").read_text())
        bad["name"] = "_t"; bad["models"]["judge"] = "sonnet"
        f = MK / "packs/_t.json"
        f.write_text(json.dumps(bad))
        try:
            with self.assertRaisesRegex(core.MarketError, "ghim"):
                core.load_pack("_t")
        finally:
            f.unlink()

    def test_both_packs_load(self):
        for p in ("ll", "k2"):
            core.load_pack(p)


class TestQuota(Base):
    def test_search_held_for_k2(self):
        with self.assertRaisesRegex(core.MarketError, "k2"):
            self.q("ll").check_plan({"search": 1})
        self.q("k2", cap=5000).check_plan({"search": 3})

    def test_session_m_limits(self):
        q = self.q("m", cap=1000)
        self.assertEqual(q.room(), 50)
        with self.assertRaises(core.MarketError):
            q.check_plan({"playlistItems": 1})
        with self.assertRaises(core.MarketError):
            q.check_plan({"videos": 51})
        q.check_plan({"videos": 2, "channels": 1})

    def test_reservation_and_floor(self):
        self.assertEqual(self.q("ll").room(), 10000 - 500 - 9000)
        self.assertEqual(self.q("k2").room(), 10000 - 500)
        self.assertEqual(self.q("ll", used_elsewhere=450).room(), 50)
        with self.assertRaises(core.MarketError):
            Q.Quota("ai-la", 10, policy=self.policy)

    def test_charge_stops_at_cap_and_logs(self):
        q = self.q("ll", cap=2)
        q.charge("videos"); q.charge("videos")
        with self.assertRaisesRegex(core.MarketError, "trần lượt"):
            q.charge("videos")
        self.assertEqual(q.used_local(), 2)
        with self.assertRaises(core.MarketError):
            self.q("ll", dry=True).charge("videos")

    def test_expired_hold_releases(self):
        later = dt.datetime(2100, 1, 2, 12, tzinfo=dt.timezone.utc)
        q = self.q("ll", now=later)
        q.check_plan({"search": 3})
        self.assertEqual(q.room(), 9500)


class TestAI(Base):
    def test_cap_stops_before_call(self):
        (core.pack_dir(self.pack) / "ai-ledger.jsonl").write_text(json.dumps({"usd": 4.6}) + "\n")
        with self.assertRaisesRegex(core.MarketError, "trần"):
            ai.ask(self.pack, "judge", "x", "t")

    def test_ledger_records_served_model(self):
        ai.ask(self.pack, "judge", "Planned episode", "t")
        row = json.loads((core.pack_dir(self.pack) / "ai-ledger.jsonl").read_text())
        self.assertEqual(row["model"], "claude-sonnet-5-5")
        self.assertEqual(row["served"], ["claude-sonnet-5-5"])

    def test_missing_labels_fail_closed(self):
        ai._run = fake_ai(drop_ids={"vidAAAAAAA1"})
        p = 'Return ONLY JSON {"<videoId>": {"on_topic": true}}\nvidAAAAAAA1 | t | d\nvidAAAAAAA2 | t | d'
        with self.assertRaisesRegex(core.MarketError, "phủ nhãn"):
            ai.ask_cover(self.pack, "judge", p, "rel", ["vidAAAAAAA1", "vidAAAAAAA2"])

    def test_no_json_fail_closed(self):
        ai._run = lambda *a: {"result": "sorry", "total_cost_usd": 0}
        with self.assertRaises(core.MarketError):
            ai.ask(self.pack, "judge", "x", "t")


class TestTopic(Base):
    def run_topic(self, *extra):
        return market.main(["topic", "t3-drafters", "--pack", "ll", "--session", "k2", "--cap", "2000", *extra])

    def test_profile_end_to_end(self):
        self.assertEqual(self.run_topic(), 0)
        md = (self.repo / "reports/m3/topics/t3-drafters.md").read_text()
        lab = json.loads((self.repo / "reports/m3/topics/labels.json").read_text())["t3-drafters"]
        self.assertEqual(lab["current"], "Mạnh")       # 2 video ≥ 50 nghìn đúng đề tài trong 90 ngày (1 lạc đề bị loại)
        self.assertEqual(lab["durable"], "Có")
        self.assertEqual(lab["gap"], "Có")              # 1/5 có số liệu thật
        self.assertEqual(len(lab["questions"]), 5)
        self.assertTrue(lab["outliers"] and lab["outliers"][0]["ratio"] in ("≥ 3×", "≥ 5×"))
        for sec in ("Cầu hiện hành", "Cầu bền", "Khoảng trống", "3 video vượt trội", "5 câu hỏi khán giả",
                    "Điểm yếu đối thủ", "Dải thời lượng thắng", "Mẫu tiêu đề", "tự tính, không phải chỉ số YouTube", "TẠM"):
            self.assertIn(sec, md)
        self.assertNotRegex(md, r"\b(1 ?234 ?567|2 ?000 ?000|1,200,000)\b")   # không số lượt xem thô kênh khác
        raw = json.loads((core.pack_dir(self.pack) / "topic_t3-drafters.json").read_text())
        self.assertIn(600000, raw["guard"])
        self.assertTrue(render.assert_repo_safe(md, raw["guard"]))
        self.assertTrue((core.pack_dir(self.pack) / "topic_t3-drafters.json").exists())   # thô ở ngoài repo
        self.assertEqual(self.world.calls.count("search"), 6)

    def test_http_error_fail_closed_no_output(self):
        core.http_get = World(fail={"videos": 403})
        self.assertEqual(self.run_topic(), 2)
        self.assertFalse((self.repo / "reports/m3/topics/t3-drafters.md").exists())

    def test_quota_refuses_before_any_call(self):
        self.assertEqual(market.main(["topic", "t3-drafters", "--pack", "ll", "--session", "ll", "--cap", "2000"]), 2)
        self.assertEqual(self.world.calls, [])

    def test_queue_block_idempotent(self):
        self.run_topic()
        market.main(["queue", "--pack", "ll"]); market.main(["queue", "--pack", "ll"])
        t = (self.repo / "topics/queue.md").read_text()
        self.assertEqual(t.count(render.QUEUE_START), 1)
        self.assertIn("bảng cũ giữ nguyên", t)
        self.assertIn("| `t3-drafters` | Mạnh / Có |", t)
        self.assertIn("| `t4-apprentices` | chưa đo |", t)

    def test_repo_safe_catches_raw(self):
        for t in ("video đầu 4,830,000 lượt", "4 830 000 views", "(4830000)", "4.830.000"):
            with self.assertRaises(core.MarketError):
                render.assert_repo_safe(t, [4830000])
        ok = "[x-48300001](https://youtu.be/x-48300001) ≥ 500 nghìn, 2026-10-11, 1,000 words, 14830000"
        self.assertTrue(render.assert_repo_safe(ok, [4830000]))

    def test_verbatim_blocked(self):
        src = ["I was a draftsman for 30 years and the change hit hard"]
        self.assertTrue(render.verbatim(["A former draftsman for 30 years and the change hit hard indeed"], src))
        self.assertFalse(render.verbatim(["Người từng vẽ kỹ thuật chuyển sang CAD"], src))

    def test_ai_served_mismatch_stops(self):
        ai._run = lambda m, p, c, b: {"result": "{}", "total_cost_usd": 0.01, "modelUsage": {"claude-haiku-5-5": {}}}
        with self.assertRaisesRegex(core.MarketError, "khác model ghim"):
            ai.ask(self.pack, "judge", "x", "t")

    def test_comments_disabled_continues(self):
        """403 commentsDisabled → coi như không có bình luận, hồ sơ vẫn sinh (tổng hợp chỉ từ tiêu đề)."""
        w = World()
        core.http_get = lambda u, p: (403, '{"error":{"errors":[{"reason":"commentsDisabled"}]}}') if u.endswith("commentThreads") else w(u, p)
        self.assertEqual(self.run_topic(), 0)

    def test_comment_403_quota_fails_closed(self):
        core.http_get = World(fail={"commentThreads": 403})
        self.assertEqual(self.run_topic(), 2)


class TestOwn(Base):
    def snaps(self, ep, pts):
        return [dict(ep=ep, age_h=a, views=v, vid="x", dur_s=600) for a, v in pts]

    def test_milestones(self):
        s = self.snaps("ep01", [(30, 100), (200, 400), (700, 900)])
        self.assertEqual(own.milestone(s, "ep01", 168)[0], "đúng mốc")
        self.assertEqual(own.milestone(s, "ep01", 48), ("nội suy", round(100 + 300 * 18 / 170), 48))
        self.assertEqual(own.milestone(s, "ep01", 672)[0], "đúng mốc")
        self.assertEqual(own.milestone(self.snaps("ep02", [(500, 50)]), "ep02", 48)[0], "lỡ mốc")
        self.assertEqual(own.milestone(self.snaps("ep03", [(20, 5)]), "ep03", 168)[0], "chờ")

    def test_calibration_rule(self):
        s = (self.snaps("a", [(170, 900)]) + self.snaps("b", [(170, 300)]) + self.snaps("c", [(170, 100)]))
        good = {"a": {"label": "Mạnh"}, "b": {"label": "Yếu"}, "c": {"label": "Không"}}
        self.assertIn("giữ", own.calibrate(self.pack, s, good)["verdict"])
        bad = {"a": {"label": "Không"}, "b": {"label": "Yếu"}, "c": {"label": "Mạnh"}}
        self.assertIn("KHÔNG", own.calibrate(self.pack, s, bad)["verdict"])
        self.assertIn("chưa đủ", own.calibrate(self.pack, s, {"a": {"label": "Mạnh"}})["verdict"])

    def test_calibration_needs_signal_and_release(self):
        s = (self.snaps("ep06", [(170, 129)]) + self.snaps("ep07", [(170, 10)]) + self.snaps("ep08", [(170, 5)])
             + self.snaps("ep02", [(170, 900)]))
        preds = {e: {"label": l} for e, l in (("ep06", "Mạnh"), ("ep07", "Yếu"), ("ep08", "Không"), ("ep02", "Mạnh"))}
        c = own.calibrate(self.pack, s, preds)
        self.assertIn("chưa đủ tín hiệu", c["verdict"])
        self.assertEqual(sorted(p[0] for p in c["pts"]), ["ep06", "ep07", "ep08"])   # ep02 không phát hành bị loại; < 100 vẫn giữ làm điểm
        s2 = s + self.snaps("ep01", [(170, 150)]) + self.snaps("ep09", [(170, 400)])
        p2 = dict(preds, ep01={"label": "Yếu"}, ep09={"label": "Mạnh"})
        self.assertNotIn("tín hiệu", own.calibrate(self.pack, s2, p2)["verdict"])   # 3 tập ≥ 100 → áp luật trên mọi điểm
        md, _ = own.report_md(self.pack, s, {}, {})
        self.assertIn("ep02", md); self.assertIn("không phát hành", md)

    def test_predict_needs_history(self):
        s = self.snaps("a", [(170, 100)])
        self.assertIsNone(own.predict(self.pack, s, "Mạnh")["7d"]["range"])
        s += self.snaps("b", [(170, 300)]) + self.snaps("c", [(170, 900)]) + self.snaps("d", [(170, 500)])
        lo, hi = own.predict(self.pack, s, "Mạnh")["7d"]["range"]
        self.assertEqual(hi, 900); self.assertGreater(lo, 100)

    def test_own_run_session_m(self):
        """Phiên M: chỉ videos/channels ≤ 50 → không gọi playlistItems, dùng video_id trong gói (ep01 ở fixture)."""
        pack = core.load_pack("ll")
        for e in pack["own"]["episodes"].values():
            e["video_id"] = None
        pack["own"]["episodes"]["ep01"]["video_id"] = "ownAAAAAAA1"
        market.load_pack = lambda name: pack
        self.assertEqual(market.main(["own", "--pack", "ll", "--session", "m", "--cap", "20"]), 0)
        self.assertNotIn("playlistItems", self.world.calls)
        rep = (self.repo / "reports/m3/KHAN-GIA-SO.md").read_text()
        self.assertIn("ownAAAAAAA1", rep)
        self.assertIn("Analytics API", rep)
        self.assertEqual(len(own.load_snaps(pack)), 1)

    def test_own_discover_orphans_and_dedupe(self):
        """Phiên ll được dò uploads: video dài kênh mình không khớp tiêu đề nào → liệt kê để gán tay; chạy lại không nhân đôi ảnh chụp."""
        pack = core.load_pack("ll")
        for e in pack["own"]["episodes"].values():
            e["video_id"] = None; e["yt_title"] = None
        pack["own"]["episodes"]["ep01"]["title"] = "Something Else"
        pack["own"]["discover"] = True                     # gói ll tắt dò (chủ dự án 11/10); test bật để kiểm cơ chế
        market.load_pack = lambda name: pack
        self.assertEqual(market.main(["own", "--pack", "ll", "--session", "ll", "--cap", "20"]), 0)
        self.assertEqual(market.main(["own", "--pack", "ll", "--session", "ll", "--cap", "20"]), 0)
        self.assertIn("playlistItems", self.world.calls)
        self.assertIn("chưa gán tập", (self.repo / "reports/m3/KHAN-GIA-SO.md").read_text())
        self.assertEqual(own.load_snaps(pack), [])


class TestBrief(Base):
    def test_brief_frames_and_checks(self):
        import brief, subprocess
        vid = self.tmp / "v.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "testsrc=size=1920x1080:rate=24:duration=3",
                        "-pix_fmt", "yuv420p", str(vid)], check=True)
        claims = self.tmp / "claims.txt"; claims.write_text("1954\n")
        old = brief.REPO; brief.REPO = self.repo; self.addCleanup(setattr, brief, "REPO", old)
        rc = brief.main(["--ep", "ep09", "--slug", "t3-drafters", "--video", str(vid), "--at", "0.5,1.5,2.5",
                         "--titles", "Will AI Replace Drafters? History Has a Clue|In 1954, Drafting Changed. Then What?|Who Draws the Plans Now? 73% Say",
                         "--thumb-text", "WHO DRAWS IT NOW TODAY", "--objects", "a drawing board", "--paradox", "the tool changed, the job stayed",
                         "--claims", str(claims)])
        self.assertEqual(rc, 0)                                         # đọc, không chặn
        out = self.repo / "reports/m3/ep09/phat-hanh"
        from PIL import Image
        for i in (1, 2, 3):
            self.assertEqual(Image.open(out / f"nen-{i}.jpg").size, (1280, 720))
        md = (out / "PACKAGING-BRIEF.md").read_text()
        self.assertIn("Tiêu đề A: ĐẠT", md); self.assertIn("Tiêu đề B: ĐẠT", md)
        self.assertIn("Tiêu đề C: CẢNH BÁO", md)                          # 73% không có trong claim
        self.assertIn("Chữ thumbnail: CẢNH BÁO", md)                      # 5 từ
        self.assertIn("Test & Compare", md); self.assertIn("Prompt mẫu", md)


if __name__ == "__main__":
    unittest.main()
