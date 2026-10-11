"""Bộ điều phối quota YouTube Data API (một project/khoá chung cho mọi phiên của môi trường).

Luật ở `quota-policy.json` (repo, phiên P/M sửa khi chủ dự án đổi phân bổ):
- `daily_units` (10 000), ngày quota theo giờ Thái Bình Dương (`reset_tz`), `reserve_floor`: dừng khi phần còn lại < mức này.
- `priority`: thứ tự ưu tiên phiên. Phần `reserve_units` của phiên đứng TRƯỚC (còn hiệu lực tới `until`) bị trừ khỏi hạn mức
  của phiên đứng sau.
- `holds`: phương thức bị giữ cho một phiên (vd `search` dành cho k2 tới hết 12/10), giới hạn phương thức/đơn vị của một phiên.
Mỗi lệnh: ước đơn vị TRƯỚC khi chạy (`plan`), từ chối nếu vượt; trong khi chạy, mỗi lượt gọi không trúng cache xin
`charge()` và dừng ngay khi chạm trần lượt chạy hoặc trần ngày. Sổ đơn vị: `$MARKET_DATA/quota/<ngày PT>.jsonl` (chỉ biết
phần của container này; phần phiên khác khai qua `--used-elsewhere`, không biết thì ghi 0 và dựa vào `reserve_units`).
"""
import datetime as dt, json, math, time
from zoneinfo import ZoneInfo
from core import HERE, MarketError, data_root

COST = {"search": 100}                    # mọi phương thức đọc khác 1 đơn vị


def load_policy(path=None):
    p = json.loads((path or HERE / "quota-policy.json").read_text())
    for k in ("daily_units", "reset_tz", "reserve_floor", "priority", "reservations", "holds"):
        if k not in p:
            raise MarketError(f"quota-policy.json thiếu '{k}'")
    return p


def quota_day(policy, now=None):
    now = now or dt.datetime.now(dt.timezone.utc)
    return now.astimezone(ZoneInfo(policy["reset_tz"])).date()


def _active(rule, day):
    return "until" not in rule or day <= dt.date.fromisoformat(rule["until"])


class Quota:
    def __init__(self, session, cap, used_elsewhere=0, policy=None, now=None, dry=False):
        self.policy = policy or load_policy()
        self.session, self.cap, self.elsewhere, self.dry = session, int(cap), int(used_elsewhere), dry
        if session not in self.policy["priority"]:
            raise MarketError(f"phiên '{session}' không có trong priority của quota-policy.json — dừng")
        self.day = quota_day(self.policy, now)
        self.ledger = data_root() / "quota" / f"{self.day.isoformat()}.jsonl"
        self.run_units = 0

    # --- sổ ---
    def used_local(self):
        if not self.ledger.exists():
            return 0
        return sum(json.loads(l)["units"] for l in self.ledger.read_text().splitlines() if l.strip())

    def holds(self):
        return [h for h in self.policy["holds"] if _active(h, self.day)]

    def reserved_ahead(self):
        pr = self.policy["priority"]
        me = pr.index(self.session)
        return sum(r["units"] for r in self.policy["reservations"]
                   if _active(r, self.day) and r["session"] in pr[:me])

    def room(self):
        """Đơn vị phiên này còn được dùng hôm nay (đã trừ dự phòng, phần giữ cho phiên ưu tiên hơn, phần đã dùng)."""
        lim = [self.policy["daily_units"] - self.policy["reserve_floor"] - self.reserved_ahead()
               - self.used_local() - self.elsewhere]
        for h in self.holds():
            if h.get("session") == self.session and "max_units_per_day" in h:
                lim.append(h["max_units_per_day"] - self.used_local_session())
        return min(lim)

    def used_local_session(self):
        if not self.ledger.exists():
            return 0
        return sum(r["units"] for r in map(json.loads, filter(str.strip, self.ledger.read_text().splitlines()))
                   if r.get("session") == self.session)

    def method_ok(self, method):
        for h in self.holds():
            if method in h.get("reserved_methods", []) and h.get("session") != self.session:
                return False, f"{method} đang giữ cho phiên {h['session']} tới hết {h['until']} (quota-policy.json)"
            if h.get("session") == self.session and "methods" in h and method not in h["methods"]:
                return False, f"phiên {self.session} chỉ được gọi {h['methods']} tới hết {h['until']}"
        return True, ""

    # --- trước khi chạy ---
    def check_plan(self, plan):
        """plan = {phương thức: số lượt ước}. In ước, từ chối nếu vượt trần lượt chạy hoặc phần còn lại hôm nay."""
        units = sum(COST.get(m, 1) * n for m, n in plan.items())
        for m, n in plan.items():
            ok, why = self.method_ok(m)
            if n and not ok:
                raise MarketError(f"ước trước khi chạy: {why}")
        room = self.room()
        msg = (f"ước {units} đơn vị ({', '.join(f'{m}×{n}' for m, n in plan.items() if n)}); trần lượt {self.cap}; "
               f"còn được dùng hôm nay ≈ {room} (ngày quota {self.day}, đã trừ dự phòng {self.policy['reserve_floor']} "
               f"và phần giữ cho phiên ưu tiên hơn {self.reserved_ahead()})")
        if units > self.cap or units > room:
            raise MarketError("dừng trước khi chạy: " + msg)
        return units, msg

    # --- trong khi chạy ---
    def charge(self, method):
        if self.dry:
            raise MarketError(f"chạy khô (--dry): không gọi {method}")
        ok, why = self.method_ok(method)
        if not ok:
            raise MarketError(why)
        c = COST.get(method, 1)
        if self.run_units + c > self.cap:
            raise MarketError(f"chạm trần lượt chạy {self.cap} đơn vị (đã dùng {self.run_units}) — dừng")
        if c > self.room():
            raise MarketError(f"phần quota còn lại hôm nay < {c} sau dự phòng — dừng")
        self.run_units += c
        self.ledger.parent.mkdir(parents=True, exist_ok=True)
        with open(self.ledger, "a") as f:
            f.write(json.dumps({"t": time.time(), "session": self.session, "method": method, "units": c}) + "\n")


def topic_plan(n_questions, n_durable, n_channels=10, n_comment_videos=5):
    """Ước cho `market topic`: mỗi câu 1 search + 1 videos; kênh: 1 channels + 2/kênh (uploads + videos); bình luận."""
    return {"search": n_questions + n_durable, "videos": n_questions + n_durable + n_channels,
            "channels": math.ceil(n_channels / 50), "playlistItems": n_channels, "commentThreads": n_comment_videos}
