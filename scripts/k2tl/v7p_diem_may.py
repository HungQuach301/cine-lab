#!/opt/cine/bin/python
"""V7-PILOT · KẾ HOẠCH ĐIỂM MÁY CẢ TẬP: bảng 74 shot G1b (g1b/episode.yaml, lời khoá không đổi) → shot mới theo ngữ pháp TL-1…TL-6.
Mỗi shot mới = (điểm máy A–H, dải thời gian, các dòng lời phủ). Tính tỷ lệ thời lượng timelapse góc cao / lướt thấp / khung neo / thẻ, số cắt/phút, độ dài shot TB.
Ra: reports/v7p/diem-may.md (bảng) + reports/v7p/diem-may.json. Dùng: /opt/cine/bin/python -I scripts/k2tl/v7p_diem_may.py"""
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
E = yaml.safe_load((ROOT / 'channel-k2/k2c-t3-01/g1b/episode.yaml').read_text()); SEG = {s['id']: s for s in E['segments']}
DM = {d['id']: d['ten'] for d in json.loads((ROOT / 'design/k2v/tl/data/diem-may-v7.json').read_text())['diem']}
OLDT = {s['id']: (s['shots'][0].get('type'), s['dur']) for s in E['segments']}
# (mã shot mới, điểm máy, loại: tl = timelapse góc cao | neo = khung neo tầm mắt (TL-2) | the = thẻ phương pháp cuối, dòng lời cũ, thời gian chạy trong shot, khoảnh khắc chính)
PLAN = [
 ('H1', 'D', 'tl', ['0a', '0b'], '18/10/2026 23:52 → 19/10 08:20', 'đêm biên giới, đèn đường + đèn đường băng, người đi bộ qua đường băng; đêm → bình minh'),
 ('H2', 'B', 'tl', ['0c', '0d', '0e', '0f'], '2026 → TUA NGƯỢC 1309 → 1704 (cờ đổi) → 1779 → 13–14/9/1782 đêm', '14 nhịp vây hãm trên phố/lâu đài; phố 1704 → 1782; pin nổi cháy đêm (≤ 30 s)'),
 ('H3', 'D', 'tl', ['0g', '0h'], '1938 → 1943 → 2026', 'mặt đường băng mọc qua đường (1939–41), lấn vịnh (1941–43); dòng người qua cổng 2026'),
 ('N1.1', 'B', 'tl', ['SM1', '1a', '1b'], '2/1704 → 1/8/1704', 'hạm đội Rooke vào vịnh (thay bản đồ chiến lược SM1: lời mang ý liên minh)'),
 ('N1.2', 'C', 'tl', ['1c', '1d'], '7/1704 → 3/8/1704', 'plan 1705 phủ khớp lên phố ≤ 3 s rồi tan; phố 1704 dưới pháo hạm (khói)'),
 ('N1.3', 'C', 'tl', ['1e', '1f'], '3/8 → 6/8/1704', 'cờ Borgoña → Union trên lâu đài (4/8/1704); không tấm số "100 / 500"'),
 ('N1.4', 'A', 'tl', ['1g'], '8/1704 → 1705', 'dòng người rời phố lên bắc về San Roque dọc eo đất'),
 ('N1.5', 'G', 'tl', ['1h', '1i'], '1713 → 2015', 'từ đỉnh Rock nhìn eo đất trống (điều 10 không nhắc); 2015: ranh hiện nay hiện lên (không thẻ trích)'),
 ('N1.6', 'A', 'tl', ['1j', '1k'], '1704 → 1727 → 1730–35', 'chiến hào 1704–05, 1727; Línea mọc tây → đông 1730–35'),
 ('C1', 'A', 'tl', ['2a', '2b'], '20/6 → 28/10/1779', 'cổng đóng 21/6; trại TBN dựng (Faden 1783); thẻ chương "1779 — The Great Siege"'),
 ('C2', 'E', 'tl', ['2c'], '12/7 → 20/12/1779', 'hải đội rời Algeciras ra hàng chặn; thuyền châu Phi quay lại'),
 ('C3', 'C', 'tl', ['2d', '2e'], '14 → 15/1/1780 (ngày–đêm)', 'người hái rau dại trên sườn; đồn trú tập; vịnh bị chặn (không tấm "trứng 6 xu")'),
 ('C4', 'B', 'tl', ['SM2', '2f'], '16/1 → 30/11/1780', 'đoàn Rodney vào/ra; tàu Đan Mạch chở chanh (thay SM2)'),
 ('C5', 'C', 'tl', ['2g'], '12/4 09:20 → 14/4/1781 11:00', 'đoàn Darby thả neo 10:45, pháo TBN bắn phố, dân chạy nam, 5 nhà cháy đêm 13→14/4'),
 ('N2.6', 'C', 'tl', ['2h', '2i'], '14/4/1781 → 9/1782', 'phố sập dần thành "RUINS" (plan 1786); khói pháo hai phía (không tấm 205 328 / 258 387)'),
 ('KA1782', 'neo', 'neo', ['KA1782'], '9/1782', 'khung neo then/now phố hẹp 1782 (TL-2: vai "then/now")'),
 ('N2.7', 'G', 'tl', ['2j'], '8/9/1782 07:00 → 18:00', 'đạn nung đỏ từ pháo bắc: ụ Mahon + tuyến song song cháy (S059)'),
 ('N2.8', 'B', 'tl', ['2k', '2l'], '11 → 12/9/1782', 'hạm đội liên quân 47–50 tàu vào vịnh; 10 pin nổi rời Algeciras'),
 ('N2.9', 'B', 'tl', ['2m', '2n'], '13/9 06:45 → 14/9/1782 15:00', 'pin nổi vào vị trí → bắn → cháy đêm → nổ rạng sáng (bản dài của H2)'),
 ('N2.10', 'D', 'tl', ['2o', '2p'], '5 → 7/1782', 'vách bắc: lỗ thông hầm Ince nổ thủng (khói) — mặt cắt hầm cần M11 (D2 G1b)'),
 ('N2.11', 'A', 'tl', ['2q', '2r'], '1/1783 → 3/1783', 'phát súng cuối 5/2/1783; trại + công sự rút dần (không thẻ trích Versailles)'),
 ('N3.1', 'A', 'tl', ['3a', '3b'], '1783 → 14/2/1810', 'đất trung lập trống; Línea + 2 pháo đài nổ tung 1810'),
 ('N3.2', 'G', 'tl', ['3c'], '1810 → 1860', 'mép đất Anh tiến dần (doanh trại, vườn) — cần lớp có nguồn 1810–60'),
 ('N3.3', 'H', 'tl', ['3d'], '1849 → 1870 → 1905', 'La Línea mọc theo năm xây (Catastro)'),
 ('KC1910', 'neo', 'neo', ['KC1910'], '1910', 'khung neo phố La Línea then/now'),
 ('N3.4', 'G', 'tl', ['3e', '3f', '3g'], '1900 → 1909 → 1930', 'dải trung lập; hàng rào 1909 mọc dọc ranh; trại, vườn, trường bắn, trường đua (cần nguồn bậc 1–3)'),
 ('N3.5', 'D', 'tl', ['3h'], '1933 → 1938', 'đường băng cỏ 1934 (dải cắt cỏ) trên dải trung lập'),
 ('N4.1', 'D', 'tl', ['4a', '4b'], '3/1939 → 1941', 'phản đối 1939 (lời); mặt cứng mọc, cắt qua đường (1941)'),
 ('N4.2', 'F', 'tl', ['4c', '4d', '4e'], '1941 → 7/1943', 'đá vách bắc + đất hầm đổ ra vịnh, đường băng kéo dài (không tấm "55 km")'),
 ('N4.3', 'B', 'tl', ['4f'], '1943', 'bản đồ AMS 1943 phủ khớp lên phố ≤ 3 s rồi tan; phố 1943'),
 ('N4.4', 'G', 'tl', ['SM3', '4g'], '5/1940 → 11/1942', 'tàu sơ tán phụ nữ–trẻ em rời cảng (5/1940); máy bay tụ trên đường băng (thay SM3)'),
 ('KB1943', 'neo', 'neo', ['KB1943'], '1943', 'khung neo phố 1943 (không phụ nữ/trẻ em)'),
 ('N4.5', 'D', 'tl', ['4h', '4i'], '1942 → đêm 7/11/1942', '≥ 650 máy bay xếp đường băng ban đêm (mô hình máy bay — D3 G1b)'),
 ('N5.1', 'D', 'tl', ['5a', '5b'], '1946 → 6/1969 → 1985', 'cổng đóng: dòng người/xe dừng hẳn 1969; mở lại 1985'),
 ('KB2026', 'neo', 'neo', ['KB2026'], '2026', 'khung neo "the same square, today"'),
 ('N5.2', 'D', 'tl', ['5c', '5d'], '2026 sáng → trưa', 'dòng người qua cổng giờ cao điểm'),
 ('KC2026', 'neo', 'neo', ['KC2026'], '2026', 'khung neo phố La Línea "remember this street?"'),
 ('N5.3', 'H', 'tl', ['5e', '5f'], '2026 ngày', 'La Línea ↔ Gibraltar: dòng người sáng đi chiều về (không tấm £85 000)'),
 ('N5.4', 'D', 'tl', ['5g', '5h', '5i'], '7/2026 → 18/10/2026', 'kiểm tra dừng; hàng rào cũ gỡ, hàng mới lùi vài mét (cần nguồn vị trí); không thẻ dòng thời gian'),
 ('N5.5', 'B', 'tl', ['5j', 'KA2026'], '2026 → tua ngược 1704 → 2026', 'bookend H2: "why did everyone fight over this place?"'),
 ('N5.6', 'D', 'tl', ['5k'], '1730 → đêm 2026', 'bookend H1: Línea 1730 → đêm biên giới hôm nay'),
 ('PP', 'the', 'the', ['PP'], '—', 'thẻ "How this film was made" (§12.1 b) — không phải tấm số'),
]

def main():
    used = set(); rows = []; tot = {'tl': 0, 'neo': 0, 'the': 0}; per = {}
    for sid, d, k, L, tg, mo in PLAN:
        dur = sum(SEG[x]['dur'] for x in L); used.update(L); tot[k] += dur; per.setdefault(d, []).append((sid, dur))
        rows.append(dict(shot=sid, diem=d, loai=k, cu=L, cu_loai=[OLDT[x][0] for x in L], dur=round(dur, 2), thoi_gian=tg, khoanh_khac=mo))
    miss = [s for s in SEG if s not in used]
    if miss: raise SystemExit(f'thiếu shot cũ: {miss}')
    T = sum(tot.values()); n = len(PLAN); nshot_old = sum(1 for s in SEG if s != 'PP')
    out = dict(tong_s=round(T, 1), so_shot_moi=n, so_shot_cu=nshot_old, cat_phut=round(n / (T / 60), 2), shot_tb_s=round(T / n, 1),
               ty_le={k: round(100 * v / T, 1) for k, v in tot.items()}, luot_thap_pct=0.0, diem={k: dict(ten=DM.get(k, k), shot=[x[0] for x in v], giay=round(sum(x[1] for x in v), 1)) for k, v in per.items()}, bang=rows)
    (ROOT / 'reports/v7p/diem-may.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
    return out

if __name__ == '__main__':
    o = main(); print(json.dumps({k: v for k, v in o.items() if k not in ('bang', 'diem')}, ensure_ascii=False)); print({k: v['giay'] for k, v in o['diem'].items()})
