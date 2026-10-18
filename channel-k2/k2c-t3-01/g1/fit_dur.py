"""G1 T3 · đặt thời lượng shot theo lời (đọc g1/kiem-chu.json do kiem_loi.py ghi trên treatment-sau-tuyen + neo) → g1/dur-g1.json.
Luật: cần = từ nói/2,5 + 0,4 s thở; dur = max(⌈cần⌉₀,₅, sàn) với sàn = dur cũ cho mốc đinh, cú liên hoàn, khung neo; móc (ch 0) sàn 3 s (móc ≤ 45 s); còn lại sàn = min(dur cũ, cần + 0,5 s), ≥ 4 s.
Trần theo loại: thẻ số 8 · ảnh/tranh/bản đồ lịch sử 12 (có máy trượt/tô dòng) · strategic 8 · khung neo 10; cố định 4b = 15 (gib20 đã dựng), 0c = 3 (NC-H2).
Dùng: kiem_loi.py g1/../script-v1.md g1/treatment-sau-tuyen+neo (tạm) rồi fit_dur.py"""
import json, math
from pathlib import Path
HERE = Path(__file__).resolve().parent
K = json.loads((HERE / 'kiem-chu.json').read_text())
T = {x['id']: x for x in json.loads((HERE / 'treatment-sau-tuyen.json').read_text())['shots']}
N = {k['id']: k for k in json.loads((HERE / 'neo.json').read_text())['khung']}
CAP = {'thẻ số': 8, 'ảnh': 12, 'tranh Ken Burns': 12, 'bản đồ chiến lược': 8, 'bản đồ lịch sử': 12}
FIX = {'4b': 15.0, '0c': 3.0, '4g': 5.5}   # 4g: câu SM3 (cố định) chảy sang 4g — mũi tên sơ tán khớp "women and children away"
dur, cap_hit = {}, []
for r in K['shots']:
    sid = r['id']; x = T.get(sid); old = x['dur'] if x else N[sid]['dur']
    need = r['uoc_s'] + 0.4; up = math.ceil(need * 2) / 2
    keep = (x is None) or x.get('moc_dinh') or x.get('cu')
    floor = old if keep else (3.0 if x['ch'] == 0 else max(4.0, min(old, math.ceil((need + 0.5) * 2) / 2)))
    new = max(up, floor)
    cap = 10 if x is None else CAP.get(x['loai'], 30)
    new = FIX.get(sid, min(new, cap))
    if new + 1e-9 < need: cap_hit.append([sid, new, round(need, 1)])
    if abs(new - old) > 1e-9: dur[sid] = new
(HERE / 'dur-g1.json').write_text(json.dumps({'note': __doc__.splitlines()[1] + ' ' + __doc__.splitlines()[2], 'dur': dur, 'tran_chan': cap_hit}, ensure_ascii=False, indent=1) + '\n')
print(len(dur), 'shot đổi; chặn trần:', cap_hit)
