#!/opt/cine/bin/python
"""REVIEWER Opus độc lập cho tiêu đề + chữ thumbnail (QUAN-TRI-RUI-RO §1 VÀNG điều kiện 3). Qua ai.py (khoá trong tiến trình con)."""
import ai
from pathlib import Path
H = ai.HERE
P = f"""You are REVIEWER for a faceless documentary YouTube channel. Independently review the TITLE CANDIDATES and THUMBNAIL TEXT for this episode against the locked narration and the rules. You cannot browse. Be strict.
Check: (a) each title and the thumbnail text promise only what the narration delivers (no malicious clickbait, no exaggeration of numbers: the narration says about 1% of new homes in 2025, not zero); (b) question form is answered by the video; (c) banned words: "secret", "hidden", "who (really) controls", "they don't want you to know", "afford", "buy a home", "your rent", "save"; (d) no party framing, no group blame; (e) numbers only from narration.
Return ONLY JSON: {{"items": [{{"text": "<title or thumb>", "verdict": "ok|fix|reject", "severity": "none|minor|major|block", "problem": "<short>", "fix": "<text>"}}], "best_title": "<one>"}}
TITLES:
1. Why Did America Almost Stop Building Apartments Like This?
2. What Happened to America's Small Apartment Buildings?
3. Why Are Small Apartment Buildings So Rare in New US Homes?
THUMBNAIL TEXT (over a frame of the 3D corner building from the video): ONLY 1 IN 100
=== RISK RULES (sections 1-1.1) ===
{(H.parent / 'QUAN-TRI-RUI-RO.md').read_text().split('### 1.2')[0]}
=== CONTENT RULES §7 (Crux boundary) ===
{(H.parent / 'LUAT-NOI-DUNG.md').read_text().split('## 7.')[1].split('## 8.')[0]}
=== LOCKED NARRATION ===
{(H / 'script.md').read_text()}"""
print(ai.ai(P, "titles-REVIEWER", "claude-opus-5-5"))
print(f"chi phí lũy kế ${ai.spent():.2f}")
