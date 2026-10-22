"""SFX-T3 · bản đồ âm theo shot (43 shot + 2 thẻ) → ../ban-do-am.json + ../ban-do-am.md.
Mức so lời (Kinh thánh §4: lời trên NỀN = nhạc + SFX, p10 ≥ 15 dB / min ≥ 12 dB):
  N0 = im (không SFX) · N1 = nền xa, dưới lời ≥ 24 dB (trước duck; ≈ −41 LUFS khi lời −17) · N2 = nền rõ, dưới lời ≥ 20 dB
  N3 = điểm nhấn trong khe lời (không trùng từ), đỉnh ngắn hạn ≤ mức lời − 6 dB · N4 = điểm nhấn được phép ngang nhạc (chỉ khi không lời).
Thời kỳ: P = trước 1900 (không động cơ, không đường phố hiện đại, không tiếng Anh/Pháp nói rõ) · M1 = 1900–1945 (máy bay cánh quạt từ 1934,
  tàu hơi nước/động cơ đốt trong) · M2 = 1946–2026 (xe, máy bay hiện đại)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
B = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../channel-k2/k2c-t3-01/animatic/bang-shot.json')))
# mã lớp âm
L = dict(GIO='gió', SONG='sóng/biển', CHIM='chim biển', DONG='đám đông/tiếng người xa', BUOC='bước chân', NGUA='ngựa/xe ngựa',
         THUYEN='thuyền: mái chèo, dây, gỗ kẽo kẹt', CO='cờ bay', PXA='pháo xa', PGAN='pháo gần/loạt pháo', HOAMAI='súng hoả mai',
         NO='nổ lớn (kho thuốc, pháo đài, nổ mìn)', LUAL='lửa lớn', LUAN='lửa nhỏ/bếp trại', DAO='đào/đá/xây', MAYBAY='máy bay cánh quạt 1930–40s',
         PHO='phố/xe 2026', DEM='đêm yên (côn trùng)', COI='còi tàu 1940')
M = {  # ma: (thời kỳ, [(lớp, mức, ghi)], im/ghi chung)
 'H1': ('M2', [('DEM', 'N1', 'đêm 23:52 → bình minh 08:20'), ('PHO', 'N1', 'xe xa đêm, không còi/còi báo'), ('BUOC', 'N2', 'người đi bộ qua đường băng'), ('GIO', 'N1', '')], 'vào 0,0 s cùng lời: dốc 1,5 s'),
 'H2': ('P', [('PXA', 'N2', 'cuộn pháo xa dưới bộ đếm 14 lần vây (15,4–19,9 s)'), ('CO', 'N2', 'cờ 4/8/1704 hạ–kéo (20,0–22,4 s)'), ('PXA', 'N3', 'pin nổi khai hoả (25,4–27,7 s), một phát trong khe 22,1–22,5'), ('LUAL', 'N1', 'pin nổi bốc cháy 27,0–28,0')], '2026 15:10 → 1782: 12,0–15,3 s chỉ gió (giờ 2026 chiều)'),
 'H2T': ('P', [('LUAL', 'N2', 'pin nổi cháy, nhìn từ vịnh'), ('SONG', 'N1', 'sóng vỗ nhẹ (vịnh)'), ('NO', 'N3', 'nổ xa trong khe 31,9–33,0')], ''),
 'H3': ('M1→M2', [('MAYBAY', 'N1', '1939–43 (33,0–38,0 s): cánh quạt xa'), ('PHO', 'N1', '2026 từ 39,0 s'), ('GIO', 'N1', '')], 'không động cơ trước 1939'),
 'N1.1': ('P', [('SONG', 'N2', 'biển mở, eo biển'), ('GIO', 'N2', ''), ('THUYEN', 'N1', 'dây buồm, gỗ kẽo kẹt'), ('CHIM', 'N1', '')], 'hạm đội 1704'),
 'N1.2': ('P', [('PXA', 'N2', 'bắn phá từ vịnh, dày dần ở 1d (73–89 s)'), ('DONG', 'N1', 'phố trong tường, rất xa'), ('SONG', 'N1', '')], ''),
 'N1.3': ('P', [('CO', 'N2', 'Borgoña hạ, Union kéo'), ('GIO', 'N2', ''), ('BUOC', 'N1', 'lính vào lâu đài')], 'không trống/kèn (không có nguồn sạch)'),
 'N1.4': ('P', [('DONG', 'N1', 'dòng dân rời phố, tiếng người rất xa, lọc thấp'), ('BUOC', 'N1', 'bước trên cát'), ('GIO', 'N2', 'eo đất trống'), ('SONG', 'N1', '')], 'không tiếng Pháp/Anh rõ chữ'),
 'N1.5': ('P→M2', [('GIO', 'N2', '1713 eo đất trống'), ('SONG', 'N2', 'biển đông'), ('PHO', 'N1', 'chỉ từ 25,5 s (2015)')], 'bước năm 1729 → 2015 ở 25,4 s: đổi nền tại cú bước'),
 'N1.6': ('P', [('PXA', 'N2', 'vây 1704–05 (0–6 s) và 1727 (6,1–10,9 s)'), ('DAO', 'N1', 'Línea mọc 1730–35 (11–25 s): đá, xẻng'), ('GIO', 'N1', '')], ''),
 'C1': ('P', [('DONG', 'N1', 'trại TBN, tiếng người rất xa'), ('NGUA', 'N2', 'ngựa kỵ binh'), ('LUAN', 'N1', 'bếp trại'), ('GIO', 'N1', ''), ('CO', 'N1', 'vải lều')], ''),
 'C2': ('P', [('SONG', 'N2', ''), ('THUYEN', 'N2', 'mái chèo thuyền châu Phi'), ('GIO', 'N1', ''), ('CHIM', 'N1', '')], ''),
 'C3': ('P', [('GIO', 'N2', 'cận người hái rau'), ('CO', 'N1', 'Union'), ('CHIM', 'N1', ''), ('SONG', 'N1', 'khi cần cẩu lên')], ''),
 'C4': ('P', [('SONG', 'N2', 'sóng vỗ Old Mole'), ('THUYEN', 'N2', 'mái chèo, dây'), ('DONG', 'N1', 'người khiêng thùng'), ('CHIM', 'N1', '')], ''),
 'C5': ('P', [('PGAN', 'N3', 'pháo TBN bắn vào phố từ 3,6 s (≈ 238,8)'), ('LUAL', 'N2', 'phố cháy đêm 13→14/4 (7,4–12,5 s)'), ('DONG', 'N1', 'dân chạy về nam')], ''),
 'N2.6': ('P', [('PXA', 'N2', 'khói pháo hai phía 1781–82'), ('DAO', 'N1', 'nhà sập (đá rơi)'), ('DONG', 'N1', 'lính phá kho, rất xa')], ''),
 'KA1782': ('P', [('GIO', 'N2', 'phố đổ nát'), ('PXA', 'N1', '1 phát rất xa'), ('CHIM', 'N1', '')], 'khung neo có lời'),
 'N2.10': ('P', [('DAO', 'N2', 'đào hầm vách bắc'), ('NO', 'N3', 'nổ lỗ thông hơi 2p (khe 283,3–…)'), ('GIO', 'N1', '')], ''),
 'N2.7': ('P', [('PGAN', 'N3', 'đạn nung bắn từ Rock'), ('LUAL', 'N2', 'công sự TBN cháy'), ('GIO', 'N1', '')], ''),
 'N2.8': ('P', [('SONG', 'N2', ''), ('THUYEN', 'N1', 'hạm đội neo'), ('GIO', 'N1', ''), ('CHIM', 'N1', '')], ''),
 'N2.9': ('P', [('PXA', 'N2', 'garrison bắn khi pin vào vị trí (331–)'), ('PGAN', 'N3', '≈ 400 khẩu khai hoả — loạt lớn trong khe 342,9–344,2'), ('LUAL', 'N2', 'đêm cháy (346,5–353)'), ('NO', 'N3', 'pin nổ (khe 348,1–348,5; 352–355 dưới lời 2n ở N2)'), ('SONG', 'N1', '')], 'ĐOẠN TRỘN THỬ 2'),
 'N2.11': ('P', [('GIO', 'N2', 'mùa đông'), ('SONG', 'N1', ''), ('PXA', 'N3', 'MỘT phát cuối ngay sau "the last shot was fired" (370,2)')], 'sau phát cuối: không pháo nữa'),
 'N3.1': ('P', [('GIO', 'N1', ''), ('SONG', 'N1', ''), ('NO', 'N3', '14/2/1810 hai pháo đài nổ: khe 405,9–406,7 + dưới lời N2')], ''),
 'N3.2': ('P', [('GIO', 'N1', ''), ('SONG', 'N1', ''), ('CHIM', 'N1', '')], ''),
 'N3.3': ('P', [('DONG', 'N1', 'phố La Línea thế kỷ 19, rất xa'), ('NGUA', 'N1', 'xe ngựa'), ('GIO', 'N1', '')], 'không xe máy'),
 'KC1910': ('M1', [('DONG', 'N2', 'phố La Línea 1910, tiếng Tây Ban Nha xa'), ('NGUA', 'N2', 'ngựa/xe ngựa'), ('BUOC', 'N1', '')], 'không ô tô'),
 'N3.4': ('M1', [('GIO', 'N2', 'dải trung lập'), ('DONG', 'N1', 'hai phố xa')], 'hàng rào 1909: không có tiếng dựng rào sạch → không thêm'),
 'N3.5': ('M1', [('GIO', 'N2', 'dải cỏ'), ('MAYBAY', 'N1', 'cánh quạt xa 1934–36, một lượt')], ''),
 'N4.1': ('M1', [('DAO', 'N1', 'làm đường băng: đá, xẻng'), ('MAYBAY', 'N1', ''), ('GIO', 'N1', '')], 'không tiếng máy xúc hiện đại (bíp lùi)'),
 'N4.2': ('M1', [('NO', 'N3', 'nổ mìn vách bắc (bụi đá)'), ('DAO', 'N1', 'đá đổ xuống vịnh'), ('SONG', 'N1', ''), ('MAYBAY', 'N1', '')], ''),
 'N4.3': ('M1', [('MAYBAY', 'N1', ''), ('GIO', 'N1', ''), ('CHIM', 'N1', '')], ''),
 'N4.4': ('M1', [('COI', 'N3', 'tàu sơ tán rời cảng 5/1940 (khe đầu 4g)'), ('SONG', 'N2', ''), ('MAYBAY', 'N2', '1941–42 máy bay tụ dần'), ('GIO', 'N1', '')], '4g (541,7–550,6) không lời: SFX lên N2–N4 rồi TẮT HẾT trước 550,6 (tấm im lặng)'),
 'KB1943': ('M1', [], 'TẤM IM LẶNG §11.2 — CHỈ HÌNH + NHẠC (B8 Echoes): KHÔNG SFX'),
 'N4.5': ('M1', [('MAYBAY', 'N2', 'động cơ chạy thử dọc đường băng'), ('SONG', 'N1', ''), ('GIO', 'N1', '')], 'vào lại sau tấm im lặng bằng dốc 1 s; không còi tàu (đoàn tàu tắt đèn)'),
 'N5.1': ('M2', [('DONG', 'N2', 'dòng người qua cổng 1946–69'), ('BUOC', 'N2', ''), ('PHO', 'N1', 'xe 1950–80s')], 'cổng đóng 6/1969 (3,6 s ≈ 589,4): người và bước TẮT, chỉ còn gió đến 1985 (20,9 s ≈ 606,7)'),
 'KB2026': ('M2', [('PHO', 'N2', 'quảng trường hôm nay'), ('DONG', 'N1', ''), ('CHIM', 'N1', '')], 'khung neo có lời'),
 'N5.2': ('M2', [('BUOC', 'N2', 'giờ cao điểm qua đường băng'), ('DONG', 'N1', ''), ('PHO', 'N1', '')], ''),
 'KC2026': ('M2', [('PHO', 'N2', 'phố La Línea hôm nay, tiếng TBN'), ('DONG', 'N1', '')], ''),
 'N5.3': ('M2', [('BUOC', 'N1', ''), ('DONG', 'N1', ''), ('PHO', 'N1', ''), ('GIO', 'N1', '')], ''),
 'N5.4': ('M2', [('DONG', 'N1', 'người qua cổng không xếp hàng'), ('PHO', 'N1', ''), ('GIO', 'N1', '')], 'gỡ rào: không có tiếng kim loại sạch phù hợp → không thêm'),
 'N5.5': ('P→M2', [('SONG', 'N2', ''), ('GIO', 'N2', ''), ('CHIM', 'N1', '')], 'kéo lùi: chỉ nền biển–gió; KHÔNG chèn tiếng theo từng năm (nhạc Hiraeth dâng)'),
 'KA2026': ('M2', [], 'TẤM IM LẶNG §11.2 — GIỮ PHƯƠNG ÁN ĐÃ DUYỆT (nhạc A): KHÔNG SFX'),
 'N5.6': ('P→M2', [('GIO', 'N1', ''), ('DEM', 'N1', 'nửa đêm 2026 (13,3–20 s)'), ('PHO', 'N1', 'chỉ đoạn 2026')], 'đoạn 1730/1783 (0–4,7; 9,8–13,3 s): chỉ gió'),
 'PP1': ('—', [], 'thẻ phương pháp: không SFX'), 'PP2': ('—', [], 'thẻ phương pháp: không SFX'),
}
rows = []
for i, s in enumerate(B, 1):
    tk, lop, ghi = M[s['ma']]
    rows.append(dict(stt=i, ma=s['ma'], lời=s['dong'], phim=[s['t0'], s['t1']], thoi_ky=tk, lop=[dict(ma=a, ten=L[a], muc=b, ghi=c) for a, b, c in lop], ghi=ghi, im=not lop))
D = os.path.dirname(os.path.abspath(__file__)) + '/..'
json.dump(dict(chu_giai_muc=__doc__, lop=L, shot=rows), open(D + '/ban-do-am.json', 'w'), ensure_ascii=False, indent=1)
with open(D + '/ban-do-am.md', 'w') as f:
    f.write('| # | Mã | Phim (s) | Thời kỳ | Lớp âm (mức) | Ghi |\n|---|---|---|---|---|---|\n')
    for r in rows:
        lop = '; '.join(f"{l['ten']} **{l['muc']}**" + (f" ({l['ghi']})" if l['ghi'] else '') for l in r['lop']) or '**N0 — im**'
        f.write(f"| {r['stt']} | {r['ma']} | {r['phim'][0]:.1f}–{r['phim'][1]:.1f} | {r['thoi_ky']} | {lop} | {r['ghi']} |\n")
print(len(rows), sum(r['im'] for r in rows))
