#!/opt/cine/bin/python
"""K2C-T2-01 G1 · gọi `claude -p` (ghim model, thư mục trống, không subagent) cho các vai chạy thật của T2.
Dựa trên k2c-t1-06/ai.py; đổi vai đọc và luật cho đề tài đóng tàu (mức VÀNG: địa chính trị gần đây).
  ai.py blind <script.md> <tag>          Biên kịch: 3 người đọc mù (claude-sonnet-5-5), song song
  ai.py review <script.md> <tag>         Biên kịch: REVIEWER (claude-opus-5-5) — luật kênh + luật G §1–§6 + QUAN-TRI-RUI-RO §1 + claims.md
  ai.py titles <tag>                     Đóng gói: REVIEWER (claude-opus-5-5) rà 3 tiêu đề + 3 ý thumbnail (VÀNG điều kiện 3)
  ai.py xemtiep <hook.txt> <treatment.md> <tag>   Mốc A: 3 người chấm mù "có xem tiếp không" (claude-sonnet-5-5)
Trần API của tập T2 $11 (chủ dự án 15/10/2026), dừng ở $10. Khoá: ANTHROPIC_API_KEY lấy từ $CONSOLE_API_KEY trong môi trường tiến trình con,
không in, không ghi. Ghi kiem-mu/<tag>.json (nguyên văn) + kiem-mu/cost.jsonl (tag có tiền tố VAI "<vai>:" để vai.py cộng riêng)."""
import json, os, re, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "kiem-mu"; OUT.mkdir(exist_ok=True)
LOG = OUT / "cost.jsonl"
CAP, STOP = 11.0, 10.0

def spent():
    return sum(json.loads(l)["usd"] for l in LOG.read_text().splitlines()) if LOG.exists() else 0.0

def ai(prompt, tag, model):
    if spent() > STOP:
        raise SystemExit(f"dừng: đã tiêu ${spent():.2f} (ngưỡng dừng ${STOP}, trần ${CAP})")
    env = dict(os.environ, ANTHROPIC_API_KEY=os.environ["CONSOLE_API_KEY"])
    with tempfile.TemporaryDirectory() as cwd:   # thư mục trống: người đọc không thấy repo
        for _ in range(3):
            r = subprocess.run(["claude", "-p", "--model", model, "--output-format", "json"], input=prompt,
                               capture_output=True, text=True, env=env, cwd=cwd, timeout=1800)
            try:
                d = json.loads(r.stdout)
            except Exception:
                continue
            u = d.get("usage", {})
            with open(LOG, "a") as f:
                f.write(json.dumps({"tag": tag, "model": model, "served": sorted(d.get("modelUsage", {})), "usd": d.get("total_cost_usd", 0),
                                    "in": u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0),
                                    "out": u.get("output_tokens", 0)}) + "\n")
            name = tag.replace(":", "_")
            (OUT / f"{name}.raw.txt").write_text(d.get("result", ""))
            m = re.search(r"\{.*\}", d.get("result", ""), re.S)
            if m:
                try:
                    j = json.loads(m.group(0)); (OUT / f"{name}.json").write_text(json.dumps(j, indent=1, ensure_ascii=False)); return j
                except Exception:
                    pass
    return {}

def clean(script):
    """Lời thuần cho người đọc mù: bỏ dòng tài liệu (#, >), bỏ mã claim {C..}, giữ nhãn đoạn [NN]."""
    t = Path(script).read_text()
    t = "\n".join(l for l in t.splitlines() if not l.startswith(("#", ">")))
    t = re.sub(r"\s*\{C[0-9]+\}", "", t)
    return re.sub(r"\[(\d\d) [^\]]+\]", r"[\1]", t).strip()

READERS = {
    "R1": "You are a curious general YouTube viewer (30s, works in retail, no economics or maritime background) who watches explainer videos in the evening and quits fast when bored.",
    "R2": "You are a politically alert YouTube viewer who reads comment sections and quickly notices when a video about trade, China, South Korea, tariffs or U.S. industrial policy leans pro- or anti-administration, pro- or anti-China, protectionist or free-trade, preaches, or blames a nationality or group of people.",
    "R3": "You are a viewer who has worked in the maritime industry (shipyard planning, ship finance, Jones Act shipping) and is quick to notice oversimplification, wrong history, unit mix-ups (ship counts vs tonnage) or factual slips.",
}
BLIND_Q = """{persona}

Below is the full narration script of a 9-11 minute YouTube explainer (narrated over animated relief maps, 3D objects, archival photos and film; you only get the words). Segment labels like [03] mark sections. Read it as if watching. Answer honestly from your persona; do not be polite.

Return ONLY JSON:
{{"main_message": "<1-2 sentences: what the video is really telling you>",
 "hook_strength_1to10": <int>, "would_keep_watching_after_15s": true|false, "why_hook": "<short>",
 "story_through_people_1to10": <int>, "people_you_remember": "<names + what they wanted>",
 "mechanisms_build_on_each_other_1to10": <int>, "mechanisms_in_your_words": "<list the causes the video gives>",
 "ending_answers_opening_question": true|false, "ending_comment": "<short>",
 "boring_or_slow": [{{"seg": "NN", "why": "<short>"}}],
 "confusing": [{{"seg": "NN", "quote": "<few words>", "why": "<short>"}}],
 "felt_biased_or_one_sided": [{{"seg": "NN", "quote": "<few words>", "direction": "<toward whom/what>", "why": "<short>"}}],
 "political_lean_detected": "none|pro-administration|anti-administration|protectionist|free-trade|anti-China|pro-China", "lean_detail": "<short>",
 "blames_a_group_of_people": true|false, "blame_detail": "<short or empty>",
 "claims_you_doubt": [{{"seg": "NN", "quote": "<few words>", "why": "<short>"}}],
 "questions_left_unanswered": ["<short>"],
 "trust_1to10": <int>, "best_moment": "<seg + why>",
 "top3_fixes": ["<concrete>", "<concrete>", "<concrete>"]}}

SCRIPT:
{script}"""

REVIEW_Q = """You are REVIEWER for a faceless YouTube documentary channel about how places and industries get rich or fall behind ("with the receipts"). Review the candidate narration script below against the channel's content rules, the risk rules, and the claims/sources table. You cannot browse; judge from the documents. Be strict and specific. This episode is risk level YELLOW (recent geopolitics: U.S. fees on China-linked ships, Korea-U.S. shipbuilding deal): all 6 YELLOW conditions apply.

Check, segment by segment:
1. Sources: every number and factual statement maps to a claim with a source in the table; flag any number/fact NOT in the claims table or that goes beyond the quoted source wording; opinions marked ("our read"); channel calculations labelled; cross-basis comparisons (tonnage vs ship counts, different years, current vs constant dollars, orders vs output) flagged.
2. Causality: causal claims only where a source states them (and attributed to whom); otherwise "at the same time". Correlation presented as cause = major.
3. Sides: where stakeholders disagree (Jones Act, port fees, industrial subsidies), both sides presented with their own sources and fair wording. One-sided framing = major.
4. Political neutrality: no party framing, no campaign words, no judgment of an administration's policy as right/wrong; no blame on a nationality or group of people; subjects are named bodies, documents, decisions with dates.
5. Time markers (rule G §5): ongoing matters (fees, investments, contracts, funds) carry "as of"; no predictions; "due"/"slated" attributed.
6. Living people / operating companies (rule G §6): facts sourced and attributed; company lore labelled as lore; no motives guessed; no evaluation of companies.
7. Myth vs record beat (rule G §3): myth stated neutrally and actually common; record answers narrowly; not a straw man.
8. Hook: news -> paradox -> twist -> surprising facts -> one number -> question matching the title -> promise of a twist; the ending answers the question and returns to the opening image.
9. Story through people: each chapter centers a person or group (what they wanted, what blocked them, outcome) and the claims about them are sourced.

Return ONLY JSON:
{{"verdict": "lock|lock_with_fixes|rewrite",
 "issues": [{{"seg": "NN", "rule": "<rule id>", "severity": "block|major|minor", "quote": "<exact words>", "problem": "<short>", "fix": "<exact replacement text or action>"}}],
 "missing_from_claims": ["<fact/number in script not covered>"],
 "strengths": ["<short>"]}}

=== CONTENT RULES (channel) ===
{rules}

=== CONTENT RULES (G add-on: myth vs record, as-of; applies to all channel episodes) ===
{rules_g}

=== RISK RULES (sections 1-1.1) ===
{risk}

=== CLAIMS AND SOURCES TABLE ===
{claims}

=== CANDIDATE SCRIPT ===
{script}"""

TITLES_Q = """You are REVIEWER for a faceless YouTube documentary channel (risk level YELLOW episode: recent geopolitics). Check these 3 candidate titles and 3 thumbnail ideas against the risk rules below and against the script summary and claims: (a) the video actually answers/delivers what the title and thumbnail promise (no misleading clickbait), (b) every number on a thumbnail is in the claims table with the same basis, (c) no "secret/hidden/they don't want you to know/who really controls" framing, (d) no nationality blamed, no flags or faces or company logos as the focal point, (e) political neutrality. Return ONLY JSON {{"titles": [{{"t": "<title>", "ok": true|false, "issues": ["<short>"], "fix": "<better wording or empty>"}}], "thumbs": [{{"id": "T-A|T-B|T-C", "ok": true|false, "issues": ["<short>"], "fix": "<short>"}}], "best_title": "<t>", "best_thumb": "<id>"}}

=== RISK RULES ===
{risk}

=== TITLES AND THUMBNAILS ===
{pack}

=== CLAIMS TABLE ===
{claims}

=== SCRIPT ===
{script}"""

JUDGES = {
    "J1": "You are a 34-year-old YouTube viewer in Ohio who watches history and economics explainers a few nights a week. You leave a video in the first minute if it feels slow or like homework.",
    "J2": "You are a 52-year-old viewer who likes documentaries about industry and the world wars, and is skeptical of channels that push politics or hype.",
    "J3": "You are a 24-year-old viewer who mostly watches fast, visual explainer channels and judges a video by its first 30 seconds and how it looks.",
}
XEMTIEP_Q = """{persona}

You are deciding whether to keep watching a new YouTube video. Below are (1) the first ~45 seconds of narration, exactly as spoken, and (2) the director's treatment: what you will SEE across the whole video (visual style, recurring motif, key moments, chapter-by-chapter emotional curve). Imagine the video exactly as described. Be honest; do not be polite.

Return ONLY JSON:
{{"keep_watching": true|false, "confidence_1to10": <int>,
 "why": "<2-3 sentences>",
 "moment_you_would_leave": "<where and why, or 'none'>",
 "parts_you_would_skip_or_cut": [{{"where": "<hook line / chapter / moment>", "why": "<short>"}}],
 "best_thing": "<short>", "one_change_that_would_most_raise_your_interest": "<concrete>",
 "would_you_click_this_title": {{"title": "{title}", "click_1to10": <int>, "why": "<short>"}}}}

=== FIRST 45 SECONDS (narration) ===
{hook}

=== DIRECTOR'S TREATMENT (what you will see) ===
{treatment}"""

if __name__ == "__main__":
    mode = sys.argv[1]
    root = HERE.parent
    risk = (root / "QUAN-TRI-RUI-RO.md").read_text(); risk = risk[:risk.index("### 1.2")]
    if mode == "blind":
        script, tag = sys.argv[2], sys.argv[3]; s = clean(script)
        with ThreadPoolExecutor(3) as ex:
            res = dict(zip(READERS, ex.map(lambda k: ai(BLIND_Q.format(persona=READERS[k], script=s), f"bien-kich:{tag}-{k}", "claude-sonnet-5-5"), READERS)))
        print(json.dumps({k: bool(v) for k, v in res.items()}))
    elif mode == "review":
        script, tag = sys.argv[2], sys.argv[3]
        g = (root / "LUAT-NOI-DUNG-G.md").read_text(); g = g[g.index("## 1."):g.index("## 7.")]
        p = REVIEW_Q.format(rules=(root / "LUAT-NOI-DUNG.md").read_text(), rules_g=g, risk=risk,
                            claims=(HERE / "claims.md").read_text(), script=Path(script).read_text())
        print(bool(ai(p, f"bien-kich:{tag}-REVIEWER", "claude-opus-5-5")))
    elif mode == "titles":
        tag = sys.argv[2]
        p = TITLES_Q.format(risk=risk, pack=(HERE / "titles-thumbs.md").read_text(), claims=(HERE / "claims.md").read_text(), script=clean(HERE / "script.md"))
        print(bool(ai(p, f"dong-goi:{tag}-TITLES", "claude-opus-5-5")))
    elif mode == "xemtiep":
        hook, treat, tag = sys.argv[2], sys.argv[3], sys.argv[4]
        title = sys.argv[5] if len(sys.argv) > 5 else ""
        h, t = Path(hook).read_text(), Path(treat).read_text()
        with ThreadPoolExecutor(3) as ex:
            res = dict(zip(JUDGES, ex.map(lambda k: ai(XEMTIEP_Q.format(persona=JUDGES[k], hook=h, treatment=t, title=title), f"dong-goi:{tag}-{k}", "claude-sonnet-5-5"), JUDGES)))
        print(json.dumps({k: bool(v) for k, v in res.items()}))
    print(f"chi phí lũy kế ${spent():.2f} / trần ${CAP}")
