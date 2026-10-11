#!/opt/cine/bin/python
"""K2G-01 G1 · kiểm mù kịch bản bằng `claude -p` (ghim model, không subagent). Trần $10, dừng ở $9.
  ai.py blind <script.md> <tag>      3 người đọc mù (claude-sonnet-5-5), song song
  ai.py review <script.md> <tag>     REVIEWER (claude-opus-5-5)
Khoá: ANTHROPIC_API_KEY lấy từ $CONSOLE_API_KEY trong môi trường tiến trình con, không in, không ghi.
Ghi: kiem-mu/<tag>-*.json (kết quả nguyên văn) + kiem-mu/cost.jsonl (model yêu cầu, model thực chạy, USD)."""
import json, os, re, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "kiem-mu"; OUT.mkdir(exist_ok=True)
LOG = OUT / "cost.jsonl"
CAP, STOP = 10.0, 9.0

def spent():
    return sum(json.loads(l)["usd"] for l in LOG.read_text().splitlines()) if LOG.exists() else 0.0

def ai(prompt, tag, model):
    if spent() > STOP:
        raise SystemExit(f"dừng: đã tiêu ${spent():.2f} (ngưỡng dừng ${STOP}, trần ${CAP})")
    env = dict(os.environ, ANTHROPIC_API_KEY=os.environ["CONSOLE_API_KEY"])
    with tempfile.TemporaryDirectory() as cwd:   # thư mục trống: người đọc không thấy repo
        for _ in range(3):
            r = subprocess.run(["claude", "-p", "--model", model, "--output-format", "json"], input=prompt,
                               capture_output=True, text=True, env=env, cwd=cwd, timeout=1500)
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
    """Lời thuần cho người đọc mù: bỏ tiêu đề tài liệu và ghi chú nội bộ, giữ nhãn đoạn [NN] để họ chỉ chỗ."""
    t = Path(script).read_text()
    t = "\n".join(l for l in t.splitlines() if not l.startswith(("#", ">")))
    return re.sub(r"\[(\d\d) [^\]]+\]", r"[\1]", t).strip()

READERS = {
    "R1": "You are a curious general YouTube viewer (30s, no economics background) who watches explainer videos in the evening.",
    "R2": "You are a skeptical YouTube viewer who distrusts mainstream narratives, often reads comment sections, and is alert to bias, propaganda, or hidden agendas in videos about money and power.",
    "R3": "You are a viewer who knows the steel industry and U.S. industrial history well and is quick to notice oversimplification or factual slips.",
}
BLIND_Q = """{persona}

Below is the full narration script of a 15-18 minute YouTube documentary (narrated over 3D animation; you only get the words). Segment labels like [03] mark sections. Read it as if watching. Answer honestly from your persona; do not be polite.

Return ONLY JSON:
{{"main_message": "<1-2 sentences: what the video is really telling you>",
 "hook_strength_1to10": <int>, "would_keep_watching_after_15s": true|false, "why_hook": "<short>",
 "three_layers_connected_1to10": <int>, "what_connects_layers": "<your words>",
 "ending_answers_opening_question": true|false, "ending_comment": "<short>",
 "boring_or_slow": [{{"seg": "NN", "why": "<short>"}}],
 "confusing": [{{"seg": "NN", "quote": "<few words>", "why": "<short>"}}],
 "felt_biased_or_one_sided": [{{"seg": "NN", "quote": "<few words>", "direction": "<toward whom/what>", "why": "<short>"}}],
 "felt_like_conspiracy_or_hidden_agenda": true|false, "conspiracy_detail": "<short or empty>",
 "felt_like_financial_or_investment_advice": true|false,
 "claims_you_doubt": [{{"seg": "NN", "quote": "<few words>", "why": "<short>"}}],
 "trust_1to10": <int>, "best_moment": "<seg + why>",
 "top3_fixes": ["<concrete>", "<concrete>", "<concrete>"]}}

SCRIPT:
{script}"""

REVIEW_Q = """You are REVIEWER for a faceless YouTube documentary channel. Review the candidate narration script below against the channel's content rules and the claims/sources table. You cannot browse; judge from the documents. Be strict and specific.

Check, segment by segment:
1. Conspiracy framing (rule G §1): any implied hidden plan, unsupported causality, guessing at undisclosed documents.
2. Group bias (rule G §2): motives or hidden power attributed to an ethnic/religious/national group or family; national generalizations.
3. Defamation risk for living people and operating companies (rules §1, G §6): any claim of wrongdoing, motive ("wants", "hides"), or characterization beyond the cited source; check quotes are attributed.
4. YMYL / financial (rules §5, G §4): anything that reads as financial or investment advice; disclaimer present within first 30 s; illustrative calculations labelled and caveated.
5. Sources (rule §1–2): every number and factual statement maps to a claim with a source in the table; opinion clearly marked; flag any number or fact in the script NOT in the claims table; flag cross-basis comparisons (different definitions, years, or units).
6. Time markers (rule G §5): ongoing events dated; no predictions; projections labelled.
7. Political neutrality: does the script take sides on U.S./EU/China/Japan policy or on any president?

Return ONLY JSON:
{{"verdict": "lock|lock_with_fixes|rewrite",
 "issues": [{{"seg": "NN", "rule": "<rule id>", "severity": "block|major|minor", "quote": "<exact words>", "problem": "<short>", "fix": "<exact replacement text or action>"}}],
 "missing_from_claims": ["<fact/number in script not covered>"],
 "strengths": ["<short>"]}}

=== CONTENT RULES (channel) ===
{rules}

=== CONTENT RULES (niche G add-on) ===
{rules_g}

=== CLAIMS AND SOURCES TABLE ===
{claims}

=== CANDIDATE SCRIPT ===
{script}"""

if __name__ == "__main__":
    mode, script, tag = sys.argv[1], sys.argv[2], sys.argv[3]
    s = clean(script)
    if mode == "blind":
        with ThreadPoolExecutor(3) as ex:
            res = dict(zip(READERS, ex.map(lambda k: ai(BLIND_Q.format(persona=READERS[k], script=s), f"{tag}-{k}", "claude-sonnet-5-5"), READERS)))
        print(json.dumps({k: bool(v) for k, v in res.items()}))
    elif mode == "review":
        root = HERE.parent
        p = REVIEW_Q.format(rules=(root / "LUAT-NOI-DUNG.md").read_text(), rules_g=(root / "LUAT-NOI-DUNG-G.md").read_text(),
                            claims=(HERE / "claims.md").read_text(), script=Path(script).read_text())
        print(bool(ai(p, f"{tag}-REVIEWER", "claude-opus-5-5")))
    print(f"chi phí lũy kế ${spent():.2f} / trần ${CAP}")
