"""Gọi AI headless: `claude -p --model <ghim>` với ANTHROPIC_API_KEY="$CONSOLE_API_KEY" (không in khoá).
- Không subagent, không công cụ (`--tools ""`), không MCP (`--strict-mcp-config`), chạy ở thư mục số liệu (ngoài repo).
- Sổ chi `$MARKET_DATA/<gói>/ai-ledger.jsonl` (giữ qua purge): mỗi lượt ghi tag, model ghim, model thực chạy, USD.
- Trần chi theo gói (`ai_cap_usd`): dừng TRƯỚC lượt gọi khi đã chi ≥ 90 % trần; mỗi lượt còn bị `--max-budget-usd` chặn.
- Fail closed: CLI hỏng/không ra JSON sau 3 lần → MarketError (không trả {} để đi tiếp với nhãn thiếu).
"""
import json, os, re, subprocess, time
from core import MarketError, pack_dir

STOP_FRAC = 0.9
PER_CALL_MAX = 1.0
AUX = "claude-haiku-5-5"      # CLI dùng Haiku cho tác vụ phụ nội bộ (channel-k2 REPORT vòng 2 §1); model khác → dừng


def ledger(pack):
    return pack_dir(pack) / "ai-ledger.jsonl"


def spent(pack):
    f = ledger(pack)
    if not f.exists():
        return 0.0
    return sum(json.loads(l).get("usd", 0) for l in f.read_text().splitlines() if l.strip())


def _run(model, prompt, cwd, budget):
    """Một lượt CLI; trả dict JSON của --output-format json. Tests thay hàm này."""
    if not os.environ.get("CONSOLE_API_KEY"):
        raise MarketError("thiếu CONSOLE_API_KEY trong môi trường — không gọi AI")
    env = dict(os.environ, ANTHROPIC_API_KEY=os.environ["CONSOLE_API_KEY"])
    r = subprocess.run(["claude", "-p", "--model", model, "--output-format", "json", "--tools", "",
                        "--strict-mcp-config", "--no-session-persistence", "--max-budget-usd", f"{budget:.2f}"],
                       input=prompt, capture_output=True, text=True, env=env, cwd=str(cwd), timeout=900)
    return json.loads(r.stdout)


def ask(pack, role, prompt, tag):
    """Trả JSON (dict/list) đầu tiên trong câu trả lời của model vai `role` của gói."""
    model = pack["models"][role]
    cap = float(pack["ai_cap_usd"])
    for _ in range(3):
        s = spent(pack)
        if s >= STOP_FRAC * cap:
            raise MarketError(f"sổ chi AI gói {pack['name']}: ${s:.2f} ≥ {int(STOP_FRAC * 100)} % trần ${cap:.2f} — dừng")
        budget = min(PER_CALL_MAX, cap - s)
        try:
            d = _run(model, prompt, pack_dir(pack), budget)
        except (json.JSONDecodeError, subprocess.TimeoutExpired):
            with open(ledger(pack), "a") as f:            # không biết chi thật: ghi trần lượt (ước dư, an toàn cho trần)
                f.write(json.dumps({"t": time.time(), "tag": tag, "model": model, "served": [], "usd": budget, "est": True}) + "\n")
            continue
        with open(ledger(pack), "a") as f:
            f.write(json.dumps({"t": time.time(), "tag": tag, "model": model,
                                "served": sorted(d.get("modelUsage", {})), "usd": d.get("total_cost_usd", 0)}) + "\n")
        served = set(d.get("modelUsage") or {})
        if model not in served or served - {model, AUX}:
            raise MarketError(f"AI {tag}: model thực chạy {sorted(served)} khác model ghim {model} (+ {AUX} phụ) — dừng")
        m = re.search(r"[\{\[].*[\}\]]", d.get("result", ""), re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except json.JSONDecodeError:
                pass
    raise MarketError(f"AI {tag}: không ra JSON sau 3 lần — dừng")


def ask_cover(pack, role, prompt, tag, ids, min_cov=1.0):
    """Như ask() nhưng bắt buộc phủ nhãn cho mọi id (gắn lại 1 lượt cho phần sót); thiếu → dừng."""
    out = {k: v for k, v in ask(pack, role, prompt, tag).items() if k in ids}
    miss = [i for i in ids if i not in out]
    if miss:
        out.update({k: v for k, v in ask(pack, role, prompt + "\n\nONLY these ids were missing, label them: "
                                         + ", ".join(miss), tag + "-retry").items() if k in ids})
    cov = sum(i in out for i in ids)
    if ids and cov < min_cov * len(ids):
        raise MarketError(f"AI {tag}: phủ nhãn {cov}/{len(ids)} < {int(min_cov * 100)} % — dừng")
    return out
