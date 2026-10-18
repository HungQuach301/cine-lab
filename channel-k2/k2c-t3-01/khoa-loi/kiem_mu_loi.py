#!/opt/cine/bin/python
"""T3 khoá lời · KIỂM MÙ LỜI (3 vai) + REVIEWER (Kinh thánh §3: "kiểm chứng giữ nguyên chuẩn hiện hành — claims, nguồn, kiểm mù, REVIEWER tối đa 3 vòng").
Giao thức như k2c-t2-01 (bien-kich_v*-R1..R3 / REVIEWER) và g1/mo_dau_panel.py: `claude -p` GHIM model, KHÔNG công cụ, thư mục tạm trống;
ẩn tác giả (không nói ai viết, kênh nào, có AI hay không). Người đọc mù chỉ nhận lời đọc + chữ trên hình (không mã claim, không ghi chú tiếng Việt).
REVIEWER nhận lời CÓ mã claim + bảng claim được gắn (claim_en, nguồn, trích nguyên văn, trạng thái, ghi chú) để soi lỗi dữ kiện.
Soi (lệnh T3 khoá lời mục 3): claim sai/thiếu nguồn · câu thiên vị một phía · số thương vong không nói ai đếm · câu khó hiểu · chỗ chán.
Sổ chi phí khoa-loi/kiem-mu/cost.jsonl; trần lệnh $3 (cả phiên), dừng ở $2,6.
  kiem_mu_loi.py blind <script.md> <nhãn>      → kiem-mu/<nhãn>-R{1,2,3}.json (song song)
  kiem_mu_loi.py review <script.md> <nhãn>     → kiem-mu/<nhãn>-REVIEWER.json
  kiem_mu_loi.py text <script.md>              → in văn bản người đọc mù nhận"""
import json, os, re, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent; EP = HERE.parent; OUT = HERE / 'kiem-mu'; LOG = OUT / 'cost.jsonl'
BLIND_MODEL, REVIEW_MODEL, STOP = 'claude-sonnet-5-5', 'claude-opus-5-5', 2.6
TITLE = 'Why Gibraltar Was Besieged 14 Times'
RATERS = {
    'R1': "You are a general YouTube viewer in your 30s who watches 10-15 minute history explainers on a phone and leaves when a stretch drags, gets confusing, or feels like homework.",
    'R2': "You are a Spanish history teacher from Algeciras who reads English well. You know the Gibraltar story from Spanish sources and you notice when an English-language video tilts toward the British side, uses loaded words, or counts casualties without saying who counted.",
    'R3': "You are a British fact-checker for a history magazine with a background in 18th-century military history. You flag any claim that sounds wrong, overstated or unsourced, any number without a stated counter, and any wording that tilts toward the Spanish side or sneers at Britain.",
}
BLIND = """{persona}

Below is the complete narration script of a documentary YouTube video titled "{title}" (about 11 minutes, English narration, animated maps and 3D reconstructions). Lines in [On screen: ...] are text shown on screen at that moment; [silent shot] means picture and music only. Read all of it as yourself and answer honestly. Do not be polite; you have no stake in who made it.

Check especially: (a) factual claims that seem wrong, overstated or missing a source; (b) sentences that favour one side (British or Spanish) by wording, emphasis or omission; (c) any casualty or loss number that does not say who counted it; (d) sentences that are hard to understand when heard once; (e) stretches where you would get bored or leave.

Return ONLY this JSON (no other text). In every "quote", copy the exact words from the script (a short exact phrase is fine):
{{"main_message": "<one sentence>",
 "would_keep_watching_after_30s": true|false, "hook_1to10": n, "trust_1to10": n, "balance_1to10": n, "overall_1to10": n,
 "claims_doubted": [{{"chapter": "<chapter title>", "quote": "...", "why": "..."}}],
 "one_sided": [{{"chapter": "...", "quote": "...", "favours": "British|Spanish", "why": "..."}}],
 "casualty_counter_missing": [{{"chapter": "...", "quote": "...", "why": "..."}}],
 "hard_to_follow": [{{"chapter": "...", "quote": "...", "why": "..."}}],
 "boring_or_slow": [{{"chapter": "...", "from_quote": "...", "why": "..."}}],
 "top3_fixes": ["<concrete>", "<concrete>", "<concrete>"]}}

=== SCRIPT ===
{script}"""
REVIEW = """You are the REVIEWER for a history documentary script before it is locked for voice recording. You did not write it. Channel rules: every sentence must rest on a cited claim; status XÁC MINH = verified; status MÂU THUẪN = verified quotes exist but sources disagree on a detail (a number, date or version) — it MAY be used only if the sentence attributes the disputed detail to its source or uses the safe wording in ghi_chu ("Lời dẫn an toàn"); status CHƯA XÁC MINH must never be used; facts about pictures (a map's date or maker) come from the asset register, not claims — do not flag them; casualty numbers always say who counted them, and both sides' counts are given when they differ; no moral adjectives for either side; sovereignty positions are stated as each side's position, never as fact; current-affairs facts carry an "as of" date (lock date 18 October 2026); direct quotes shown on screen must match the stored source quote; the episode must be fair to British and Spanish sources alike.

Below: (1) the script; each shot starts with ‹id›, narration follows, claim ids in {{…}} after the sentence they support, [TRÊN HÌNH] = on-screen text, [IM LẶNG] = silent shot; (2) the claims those ids point to (claim_en = what the claim supports; trich_nguyen_van = stored verbatim quote; ghi_chu = researcher notes, may be in Vietnamese).

Check every sentence against its claims. Report ONLY real problems: a sentence saying more than or different from its claims (dates, numbers, who, wording), a sentence with no supporting claim, an unverified claim used, a casualty/loss number without its counter, one-sided wording, a quote on screen that does not match, a date/"as of" problem, or a sentence a listener will misunderstand. For each, give the minimal fix in exact replacement words that stay within the claims and do not lengthen the sentence by more than a few words. Do not suggest new facts that need new sources; do not restyle sentences that are correct. Sentences marked LOCKED BY THE AUTHOR (SM1, SM3, the opening 0a–0e, the closing 5k) may be flagged only for a factual error. Report at most 15 issues, most severe first; keep each field short.

Return ONLY JSON:
{{"verdict": "lock|lock_with_fixes|do_not_lock",
 "issues": [{{"shot": "<id>", "severity": "block|major|minor", "type": "fact|unsupported|unverified|casualty_counter|one_sided|quote_mismatch|as_of|clarity", "quote": "<exact words from script>", "claims": ["<id>"], "problem": "...", "fix": "<exact replacement words>"}}]}}

=== (1) SCRIPT ===
{script}

=== (2) CLAIMS ===
{claims}"""


def spent():
    return sum(json.loads(l)['usd'] for l in LOG.read_text().splitlines()) if LOG.exists() else 0.0


def parse(md):
    rows, ch = [], None
    for line in md.splitlines():
        m = re.match(r'^\[(\d\d) (\w+)\]\s*(.*)', line)
        if m: ch = m.group(3); rows.append(('ch', ch)); continue
        m = re.match(r'^‹([^›]+)›\s*(.*)', line)
        if m: rows.append(('shot', m.group(1), m.group(2))); continue
        if line.startswith('[TRÊN HÌNH]'): rows.append(('th', line[len('[TRÊN HÌNH]'):].strip()))
    return rows


def blind_text(md):
    L = []
    for r in parse(md):
        if r[0] == 'ch': L.append(f'\n## {r[1]}')
        elif r[0] == 'shot':
            t = re.sub(r'\s*\{[^}]*\}', '', r[2]).replace('‹Our read› ', '').strip()
            if '[IM LẶNG]' in t: L.append('[silent shot]')
            elif t: L.append(t)
        else:
            t = re.sub(r'^\([^)]*\)\s*', '', r[1]).replace('thẻ số:', 'number card:').replace('thẻ:', 'number card:').replace('thẻ "', 'number card "')
            L.append(f'[On screen: {t}]')
    s = '\n'.join(L).strip()
    assert not re.search(r'[ạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹđ]', s), 'còn chữ tiếng Việt trong bản mù'
    return s


def claims_for(md):
    ids = sorted(set(re.findall(r'\{([A-Z]+\d+[a-z]?)\}', md)))
    C = {}
    for f in (EP / 'vay-ham/claims-vay-ham.json', EP / 'tienky/claims.json', EP / 'tuyen/claims-tuyen.json', EP / 'g1/claims-g1.json'):
        for c in json.loads(f.read_text())['claims']: C[c['id']] = c
    keep = ('claim_en', 'nguon', 'trich_nguyen_van', 'as_of', 'phia', 'status', 'nhay_cam', 'ghi_chu')
    def row(i):
        d = {'id': i, **{k: C[i].get(k) for k in keep if C[i].get(k)}}
        if d.get('ghi_chu'): d['ghi_chu'] = d['ghi_chu'][:600]
        dc = [dict(nguon=x.get('nguon'), trich_nguyen_van=x.get('trich_nguyen_van')) for x in C[i].get('nguon_doi_chieu', []) if x.get('trich_nguyen_van')]
        if dc: d['nguon_doi_chieu'] = dc
        return json.dumps(d, ensure_ascii=False)
    return '\n'.join(row(i) for i in ids)


def run(prompt, model, tag, out):
    if spent() > STOP: raise SystemExit(f'dừng: đã tiêu ${spent():.2f}')
    env = dict(os.environ, ANTHROPIC_API_KEY=os.environ['CONSOLE_API_KEY'])
    with tempfile.TemporaryDirectory() as cwd:
        for _ in range(3):
            r = subprocess.run(['claude', '-p', '--model', model, '--output-format', 'json', '--allowedTools', ''], input=prompt, capture_output=True, text=True, env=env, cwd=cwd, timeout=1800)
            try: d = json.loads(r.stdout)
            except Exception: continue
            u = d.get('usage', {})
            with open(LOG, 'a') as f: f.write(json.dumps({'tag': tag, 'model': model, 'served': sorted(d.get('modelUsage', {})), 'usd': d.get('total_cost_usd', 0),
                                                         'in': u.get('input_tokens', 0) + u.get('cache_creation_input_tokens', 0) + u.get('cache_read_input_tokens', 0), 'out': u.get('output_tokens', 0)}) + '\n')
            out.with_suffix('.raw.txt').write_text(d.get('result', ''))
            m = re.search(r'\{.*\}', d.get('result', ''), re.S)
            if m:
                try:
                    j = json.loads(m.group(0)); j['_model'] = model; j['_prompt'] = prompt
                    out.write_text(json.dumps(j, indent=1, ensure_ascii=False)); return tag, True
                except Exception: pass
    return tag, False


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    cmd, md = sys.argv[1], Path(sys.argv[2]).read_text()
    if cmd == 'text': print(blind_text(md))
    elif cmd == 'blind':
        lab = sys.argv[3]; txt = blind_text(md)
        jobs = [(BLIND.format(persona=p, title=TITLE, script=txt), BLIND_MODEL, f'mu:{lab}-{rk}', OUT / f'{lab}-{rk}.json') for rk, p in RATERS.items()]
        with ThreadPoolExecutor(3) as ex: print(list(ex.map(lambda a: run(*a), jobs)))
    elif cmd == 'review':
        lab = sys.argv[3]
        print(run(REVIEW.format(script=re.sub(r'^>.*\n', '', md, flags=re.M), claims=claims_for(md)), REVIEW_MODEL, f'review:{lab}', OUT / f'{lab}-REVIEWER.json'))
    print(f'chi phí luỹ kế ${spent():.3f}')
