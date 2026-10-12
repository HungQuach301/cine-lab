#!/opt/cine/bin/python
"""K2C-T1-06 G1a · kiểm mù lời + REVIEWER bằng `claude -p` (ghim model, thư mục trống, không subagent).
Dựa trên k2g-ep01/ai.py; đổi vai đọc và luật cho tập T1 zoning (mức VÀNG).
  ai.py blind <script.md> <tag>      3 người đọc mù (claude-sonnet-5-5), song song
  ai.py review <script.md> <tag>     REVIEWER (claude-opus-5-5): luật kênh + luật G §3/§5 + QUAN-TRI-RUI-RO §1 + claims.md
Trần API $40 (chủ dự án 12/10/2026), dừng ở $36. Khoá: ANTHROPIC_API_KEY lấy từ $CONSOLE_API_KEY trong môi trường
tiến trình con, không in, không ghi. Ghi kiem-mu/<tag>-*.json (nguyên văn) + kiem-mu/cost.jsonl (model yêu cầu, model chạy, USD)."""
import json, os, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "kiem-mu"; OUT.mkdir(exist_ok=True)
LOG = OUT / "cost.jsonl"
CAP, STOP = 40.0, 36.0

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
            with open(LOG, "a") as f:
                f.write(json.dumps({"tag": tag, "model": model, "served": sorted(d.get("modelUsage", {})),
                                    "usd": d.get("total_cost_usd", 0)}) + "\n")
            (OUT / f"{tag}.raw.txt").write_text(d.get("result", ""))
            m = re.search(r"\{.*\}", d.get("result", ""), re.S)
            if m:
                try:
                    j = json.loads(m.group(0)); (OUT / f"{tag}.json").write_text(json.dumps(j, indent=1, ensure_ascii=False)); return j
                except Exception:
                    pass
    return {}

def clean(script):
    """Lời thuần cho người đọc mù: bỏ dòng tài liệu (#, >), bỏ mã claim [C..], giữ nhãn đoạn [NN]."""
    t = Path(script).read_text()
    t = "\n".join(l for l in t.splitlines() if not l.startswith(("#", ">")))
    t = re.sub(r"\s*\{C[0-9, C]+\}", "", t)
    return re.sub(r"\[(\d\d) [^\]]+\]", r"[\1]", t).strip()

READERS = {
    "R1": "You are a curious general YouTube viewer (30s, renter, no planning or economics background) who watches explainer videos in the evening.",
    "R2": "You are a politically alert YouTube viewer who reads comment sections and quickly notices when a video about housing or cities leans left or right, preaches, blames a group of people, or pushes an agenda (pro-development OR anti-development).",
    "R3": "You are a viewer who works in U.S. housing development (zoning, building codes, project finance) and is quick to notice oversimplification, wrong code references, or factual slips.",
}
BLIND_Q = """{persona}

Below is the full narration script of a 12-16 minute YouTube explainer (narrated over 3D animation, maps, charts and archival photos; you only get the words). Segment labels like [03] mark sections. Read it as if watching. Answer honestly from your persona; do not be polite.

Return ONLY JSON:
{{"main_message": "<1-2 sentences: what the video is really telling you>",
 "hook_strength_1to10": <int>, "would_keep_watching_after_15s": true|false, "why_hook": "<short>",
 "mechanisms_build_on_each_other_1to10": <int>, "mechanisms_in_your_words": "<list the causes the video gives>",
 "ending_answers_opening_question": true|false, "ending_comment": "<short>",
 "boring_or_slow": [{{"seg": "NN", "why": "<short>"}}],
 "confusing": [{{"seg": "NN", "quote": "<few words>", "why": "<short>"}}],
 "felt_biased_or_one_sided": [{{"seg": "NN", "quote": "<few words>", "direction": "<toward whom/what>", "why": "<short>"}}],
 "political_lean_detected": "none|left|right|pro-development|anti-development", "lean_detail": "<short>",
 "blames_a_group_of_people": true|false, "blame_detail": "<short or empty>",
 "felt_like_advice_about_your_own_rent_or_home_purchase": true|false,
 "claims_you_doubt": [{{"seg": "NN", "quote": "<few words>", "why": "<short>"}}],
 "questions_left_unanswered": ["<short>"],
 "trust_1to10": <int>, "best_moment": "<seg + why>",
 "top3_fixes": ["<concrete>", "<concrete>", "<concrete>"]}}

SCRIPT:
{script}"""

REVIEW_Q = """You are REVIEWER for a faceless YouTube documentary channel about the economic machinery of cities. Review the candidate narration script below against the channel's content rules, the risk rules, and the claims/sources table. You cannot browse; judge from the documents. Be strict and specific. This episode is risk level YELLOW (zoning): all 6 YELLOW conditions apply.

Check, segment by segment:
1. Sources (rules §1-§2): every number and factual statement maps to a claim with a source in the table; flag any number/fact NOT in the claims table; opinions marked ("our read"); channel calculations labelled "our calculation" with assumptions; cross-basis comparisons (different definitions, years, units, geographies) flagged.
2. Causality: causal claims only where a source states them; "at the same time" otherwise. Correlation presented as cause = major.
3. Sides (risk YELLOW condition 5; rules §8): where research or stakeholders disagree (effects of upzoning, single-stair safety, local control), both sides presented with their own sources and fair wording. One-sided framing = major.
4. Political neutrality (rules §8; YELLOW condition 6): no party framing, no campaign words, no blame on a group of people (race, generation, homeowners, residents of an area); subjects are named bodies, documents, decisions with dates.
5. Race/redlining (rules §8): mentioned only if needed, neutral, official sources; no moral adjectives.
6. Crux boundary (rules §7): nothing reads as advice about the viewer's own rent, home purchase, mortgage or money.
7. Time markers (rule G §5; YELLOW condition 2): ongoing matters (laws, lawsuits, implementation) carry "as of"; no predictions; projections labelled.
8. Living people / operating organizations (rule G §6): quotes attributed and dated; no motives guessed.
9. Myth vs record beats (rule G §3): myth stated neutrally and actually common; record answers narrowly; 1-3 beats.
10. Hook: a question with two sourced numbers; ending answers it.

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

if __name__ == "__main__":
    mode, script, tag = sys.argv[1], sys.argv[2], sys.argv[3]
    if mode == "blind":
        s = clean(script)
        with ThreadPoolExecutor(3) as ex:
            res = dict(zip(READERS, ex.map(lambda k: ai(BLIND_Q.format(persona=READERS[k], script=s), f"{tag}-{k}", "claude-sonnet-5-5"), READERS)))
        print(json.dumps({k: bool(v) for k, v in res.items()}))
    elif mode == "review":
        root = HERE.parent
        risk = (root / "QUAN-TRI-RUI-RO.md").read_text()
        risk = risk[:risk.index("### 1.2")]
        g = (root / "LUAT-NOI-DUNG-G.md").read_text()
        g = g[g.index("## 1."):g.index("## 7.")]
        p = REVIEW_Q.format(rules=(root / "LUAT-NOI-DUNG.md").read_text(), rules_g=g, risk=risk,
                            claims=(HERE / "claims.md").read_text(), script=Path(script).read_text())
        print(bool(ai(p, f"{tag}-REVIEWER", "claude-opus-5-5")))
    print(f"chi phí lũy kế ${spent():.2f} / trần ${CAP}")
