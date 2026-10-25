#!/opt/cine/bin/python
"""ANIMATIC-T4 · việc 5 — TẤM NỀN N2+ 2026 ban ngày ở fov sản xuất (V1, V5, V7): dùng nguyên đường ống LOOK-T4-V2 `scripts/k2ldn/tam_nen_v2.py` (prep → ghép lớp (a) → cổng (i)–(iv) → (v) nhấp nháy)
với thư mục riêng ($V2_DIR=/var/tmp/anim/tn; khung 1080p spp 24 + mặt nạ ID ở $V2_DIR/r/<khung>/) và sổ AI reports/animatic-t4 (N2P_DIR). Ảnh AI: OpenAI gpt-image-2.5-sunburst-2026-09-08 edits,
không mặt nạ (§15 b), ≤ 3 lượt/tấm (lệnh). Timelapse (v): dãy khung THẬT của shot (640×360) — tl/<khung> trỏ tới khung dựng của shot.
  tn.py prep|ghep|kiem|tl <khung> [tag] [ai]   (khung: P1-2026 | P9-2026 | P3-2026)"""
import os, sys
from pathlib import Path
os.environ.setdefault('V2_DIR', '/var/tmp/anim/tn'); os.environ.setdefault('N2P_DIR', str(Path(__file__).resolve().parents[3] / 'reports/animatic-t4'))
os.environ.setdefault('OAI_CHAN', '10'); os.environ.setdefault('CLAUDE_CHAN', '15')
sys.path.insert(0, str(Path(__file__).resolve().parents[1])); import tam_nen_v2 as T  # noqa: E402
T.NAM.update({'P1-2026': 2026, 'P9-2026': 2026, 'P3-2026': 2026})
if __name__ == '__main__':
    c, k = sys.argv[1], sys.argv[2]
    if c == 'prep': T.prep(k)
    elif c == 'ghep': T.ghep(k, sys.argv[3], sys.argv[4])
    elif c == 'kiem': T.kiem(k, sys.argv[3])
    elif c == 'tl': T.tl(k, sys.argv[3])
