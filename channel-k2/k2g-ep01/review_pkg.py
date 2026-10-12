#!/opt/cine/bin/python
"""REVIEWER Opus độc lập cho gói phát hành (QUAN-TRI-RUI-RO §1 VÀNG điều kiện 3; §1.2 điểm 6): tiêu đề, chữ thumbnail, mô tả, hook + lời Short,
và 5 điểm an toàn gia tộc trên lời khoá. Qua ai.py (khoá trong tiến trình con, không in). Ghi kiem-mu/pkg-REVIEWER.json."""
import os, subprocess, yaml, json
import ai
H = ai.HERE; Q = subprocess.run(['git', 'show', 'origin/channel-k2:channel-k2/QUAN-TRI-RUI-RO.md'], capture_output=True, text=True, cwd=H).stdout
q12 = Q[Q.index('### 1.2'):Q.index('## 2.')]; q11 = Q[Q.index('### 1.1'):Q.index('### 1.2')]
E_ = yaml.safe_load(open(H / 'episode.yaml'))
pkg = f"""TITLE (main): Is American Steel Dying? What 1950 vs 2025 Really Shows
TITLE (backup, A/B test): Why Is Steel Guarded Like a Weapon? Who Controls the Path
THUMBNAIL TEXT: 1950 VS 2025 (over a frame of two ingot stacks, 1950 and 2025, U.S. share in orange)
SHORT S1 hook: {E_['shorts'][0]['hook']} | narration: {E_['shorts'][0]['vo']}
SHORT S2 hook: {E_['shorts'][1]['hook']} | narration: {E_['shorts'][1]['vo']}
DESCRIPTION:
{open(H / 'phat-hanh/description.en.txt').read()}"""
P = f"""You are REVIEWER for a faceless documentary YouTube channel. Independently review the PACKAGING (titles, thumbnail text, Shorts, description) and check the locked narration against the family-safety rules. You cannot browse. Be strict and specific.

Check:
A. Titles/thumbnail/Shorts promise only what the video delivers (video narration below); no malicious clickbait; numbers only from the narration; future questions stay questions.
B. The 5 safe-telling points of RULE 1.2 below, applied to the narration and packaging (families/people here: Carnegie, Frick, Morgan, Schwab, Gary; companies: Carnegie Steel, U.S. Steel, Nippon Steel).
C. RED list 1.1 items (false claims, conspiracy against protected groups, defamation of living people or operating companies, impersonation, misleading title/thumbnail, mass-template output, AI persona as expert).
D. Disclaimer present in first line of description and within 30 s of narration; "as of" date present.

Return ONLY JSON:
{{"verdict": "pass|pass_with_fixes|fail",
 "issues": [{{"where": "title_main|title_backup|thumbnail|short_S1|short_S2|description|narration", "rule": "<A|B1..B5|C1..C8|D>", "severity": "block|major|minor", "quote": "<exact words>", "problem": "<short>", "fix": "<exact replacement or action>"}}],
 "family_points": {{"B1_named_entities": "ok|issue", "B2_no_religion_ethnicity_as_explanation": "ok|issue", "B3_imagery": "ok|issue|cannot_check", "B4_title_thumbnail_words": "ok|issue", "B5_comment_moderation": "post_publish"}},
 "strengths": ["<short>"]}}

=== RULE 1.1 (RED list) ===
{q11}
=== RULE 1.2 (family / Rothschild-trap safety) ===
{q12}
=== PACKAGING ===
{pkg}
=== LOCKED NARRATION ===
""" + '\n\n'.join(f"[{s['id']}] {s['vo']}" for s in E_['segments'])
print(bool(ai.ai(P, 'pkg-REVIEWER', 'claude-opus-5-5')), f'chi phí lũy kế ${ai.spent():.2f}')
