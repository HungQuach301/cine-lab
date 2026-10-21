#!/opt/cine/bin/python
"""ANIMATIC-T3 · bảng shot người đọc: channel-k2/k2c-t3-01/animatic/bang-shot.json (sinh bởi mk_ep_anim.py) → bang-shot.md
  anim_bang.py"""
import json
from pathlib import Path
D = Path(__file__).resolve().parents[2] / 'channel-k2/k2c-t3-01/animatic'
B = json.loads((D / 'bang-shot.json').read_text())
def mm(t): return f'{int(t // 60)}:{t % 60:04.1f}'
H = ['# BẢNG SHOT ANIMATIC — K2C-T3-01 Gibraltar (cả tập, 43 shot + 2 thẻ phương pháp, 761,0 s)', '',
     '> Sinh tự động từ `bang-shot.json` (`mk_ep_anim.py` → `scripts/k2tl/anim_bang.py`). Thời lượng = nhịp thật phương án B 745,0 s (`reports/kl42/nhip-that.json`) + 2 thẻ × 8 s.',
     '> Gốc: bảng 42 shot `reports/v7p/diem-may.md` §2; khác: N2.10 đứng sau KA1782 (thứ tự lời v4.2), KA2026 tách khỏi N5.5 thành khung neo riêng (ghép cặp với KA1782) → 43 shot.',
     '> Kiểu khung (LOOK-2): **lai** = có trời + sương, nhìn xuống 12–25°; **chat** = khung chặt có vai (cờ, người, vách); **dem** = đêm lửa (LOOK-3); **neo** = khung neo tầm mắt (TL-2); **lai+lan** = lai rồi cắt sang cú lặn giữ chỗ.',
     '> Nhìn xuống (°) và AGL (m) đo tại các khoá máy (đầu → cuối). Nguồn/bậc từng vật: cột ghi + meta lớp của cảnh trong log dựng.', '',
     '| # | Mã | Lời | Phim (s) | Dài | Điểm máy | Kiểu | Nhìn xuống ° | AGL m | Lightmap | Thời gian chạy trong shot | Vai | Vật mang nghĩa (§13.2) | Nguồn / bậc / ghi |',
     '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
for i, b in enumerate(B):
    nx = ' → '.join(f'{x:.0f}' for x in (b.get('nhin_xuong') or [])[::max(1, len(b.get('nhin_xuong') or []) - 1)]) if b.get('nhin_xuong') else '—'
    ag = ' → '.join(f'{x:.0f}' for x in (b.get('agl') or [])[::max(1, len(b.get('agl') or []) - 1)]) if b.get('agl') else '—'
    H.append(f"| {i + 1} | **{b['ma']}** | {', '.join(b['dong']) or '—'} | {mm(b['t0'])} → {mm(b['t1'])} | {b['dur']:.2f} | {b['diem']} | {b['kieu']} | {nx} | {ag} | {', '.join(b.get('lightmap') or []) or '—'} | "
             f"{b.get('thoi_gian', '—')} | {b['vai']} | {'; '.join(b['vat'])} | {b['ghi']} |")
(D / 'bang-shot.md').write_text('\n'.join(H) + '\n'); print(len(B), 'dòng')
