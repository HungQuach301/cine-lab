"""BAN-CUOI-T3 (việc 6) · GÓI SFX BẢN CUỐI — bản sao reports/sfx-t3/cong-cu/goi.py (SFX-T3, không sửa tệp gốc), neo lại theo bảng shot BẢN CUỐI (channel-k2/k2c-t3-01/cuoi/),
mức "tối giản dưới lời" như gói đề xuất; thêm HOAMAI-1 (chỉ phần sau 2,85 s), CHIM-1 (đoạn 5–33 s của s2573), giữ MAYBAY-1, COI-1 (lệnh 22/10). Ra: <ra>/su-kien-cuoi.json.
  cuoi_sfx.py <ra.json>
(gốc:) SFX-T3 · gói SFX đề xuất cho bản cuối T3
Mỗi sự kiện NEO tương đối (để áp lại khi bảng shot V2 đổi máy, nhịp lời B không đổi):
  neo 'shot'      : giây tính từ đầu shot (nền: phủ shot, dốc ở ranh shot)
  neo 'khe:<dòng>#k': đầu khe lời sau câu thứ k (1-based) của dòng lời — điểm nhấn không trùng từ
  neo 'moc:<giá trị>': thời điểm bộ đếm/giờ trong shot đạt giá trị (log-shot.json → thoi_gian, nội suy tuyến tính)
Hai đoạn trộn thử (móc 0–45 s, pin 321–358 s) lấy NGUYÊN sự kiện đã trộn (su-kien/moc.json, pin.json), quy về neo 'shot'."""
import json, os, re, datetime as dt
import sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, '../..'); D = os.path.join(R, 'reports/sfx-t3')
BS = json.load(open(os.path.join(R, 'channel-k2/k2c-t3-01/cuoi/bang-shot.json'))); LG = {(s.get('ma') or s['shot']): s for s in json.load(open(os.path.join(R, 'channel-k2/k2c-t3-01/cuoi/log-shot.json')))}
NH = {s['id']: s for s in json.load(open(os.path.join(R, 'reports/kl42/nhip-that.json')))['shot']}; SH = {s['ma']: s for s in BS}
UV = json.load(open(os.path.join(D, 'ung-vien/ung-vien.json')))
IM = {'KB1943', 'KA2026', 'PP1', 'PP2'}
KY = {'P': {'GIO', 'SONG', 'CHIM', 'DONG', 'BUOC', 'NGUA', 'THUYEN', 'CO', 'PXA', 'PGAN', 'HOAMAI', 'NO', 'LUAL', 'LUAN', 'DAO', 'DEM', 'NUOC'}}
KY['M1'] = KY['P'] | {'MAYBAY', 'COI'}; KY['M2'] = KY['M1'] | {'PHO'}
def nam(v):
    if isinstance(v, (int, float)): return float(v)
    if re.fullmatch(r'-?\d+(\.\d+)?', v): return float(v)
    d = dt.datetime.strptime(v, '%Y-%m-%d %H:%M'); y0 = dt.datetime(d.year, 1, 1); return d.year + (d - y0).total_seconds() / (dt.datetime(d.year + 1, 1, 1) - y0).total_seconds()
def moc(ma, v):
    tg = LG[ma]['thoi_gian']; x = nam(v)
    for a, b in zip(tg, tg[1:]):
        ya, yb = nam(a['at']), nam(b['at'])
        if min(ya, yb) <= x <= max(ya, yb) and ya != yb: return SH[ma]['t0'] + a['t'] + (x - ya) / (yb - ya) * (b['t'] - a['t'])
    raise SystemExit(f'{ma}: không có mốc {v}')
def khe(dong, k):
    c = NH[dong]['cau']; return c[k - 1]['kt_phim']
def nam_tai(t):   # năm (thời kỳ) ở giây phim t, theo shot chứa t
    for s in BS:
        if s['t0'] <= t < s['t1'] and LG.get(s['ma'], {}).get('thoi_gian'):
            tg = LG[s['ma']]['thoi_gian']; u = t - s['t0']
            for a, b in zip(tg, tg[1:]):
                if a['t'] <= u <= b['t']: return nam(a['at']) if b['t'] == a['t'] else nam(a['at']) + (u - a['t']) / (b['t'] - a['t']) * (nam(b['at']) - nam(a['at']))
            return nam(tg[-1]['at'])
    return None
def ky(y): return 'P' if y < 1900 else ('M1' if y < 1946 else 'M2')
E = []
def ev(ma, uv, neo, off, muc, **k):
    s = SH[ma]; t = s['t0'] + off if neo == 'shot' else (khe(*neo[4:].split('#')[0:1], int(neo.split('#')[1])) + off if neo.startswith('khe:') else moc(ma, neo[4:]) + off)
    E.append(dict(shot=ma, uv=uv, neo=neo, lech=round(off, 3), t=round(t, 3), muc=muc, **k))
def nen(ma, uv, muc, vao=0.0, a=0.0, b=0.0, fi=1.5, fo=2.0, **k):   # nền phủ shot [t0+a, t1+b]
    s = SH[ma]; ev(ma, uv, 'shot', a, muc, vao=vao, dai=round(s['dur'] - a + b, 3), fi=fi, fo=fo, lap=True, **k)
def khe_(ma, dong, k, uv, muc, off=0.05, **kk): ev(ma, uv, f'khe:{dong}#{k}', off, muc, **kk)
# ---- móc + pin: lấy nguyên sự kiện đã trộn thử
for f in ('moc', 'pin'):
    for e in json.load(open(os.path.join(D, f'su-kien/{f}.json')))['su_kien']:
        if f == 'moc' and e['t'] < 12.0: continue   # BAN-CUOI-T3: H1 làm lại bên dưới (ngày → M5 → đêm, câu đảo)
        ma = next(s['ma'] for s in BS if s['t0'] <= e['t'] < s['t1'] or (e['t'] < 0.001 and s['t0'] == 0))
        E.append(dict(e, shot=ma, neo='shot', lech=round(e['t'] - SH[ma]['t0'], 3), tu_tron_thu=f))
# ---- BAN-CUOI-T3: H1 ngày 15:00 → M5 bước chân trên vạch đường băng (4,5–9,5) → đêm 3D (9,5–12); lời đảo (0,5 · 3,76 · 9,75 s)
ev('H1', 'PHO-1', 'shot', 0.0, -43, dai=4.8, fi=1.5, fo=0.8, ghi='phố + đường xa ban ngày 2026'); ev('H1', 'GIO-1', 'shot', 0.0, -43, dai=12.0, fi=1.5, fo=1.0)
ev('H1', 'BUOC-1', 'shot', 4.5, -38, dai=5.0, fi=0.2, fo=0.6, ghi='M5: bước chân qua vạch đường băng (cận)'); ev('H1', 'CHIM-1', 'shot', 0.2, -45, dai=4.4, fi=1.2, fo=1.0, ghi='mòng biển xa ban ngày')
ev('H1', 'DEM-1', 'shot', 9.6, -42, dai=2.4, fi=0.6, fo=0.3, ghi='đêm biên giới'); ev('H1', 'PHO-3', 'shot', 9.5, -44, dai=2.5, fi=0.5, fo=0.3, ghi='đường xa ban đêm')
# ---- các shot còn lại (mức: N1 −41, N2 −36, nhấn trong khe −29, nhấn dưới lời −36; LUFS trước master, lời −17)
N1, N2, K3, DL = -41, -36, -29, -36
nen('N1.1', 'SONG-1', N2, a=1.2); nen('N1.1', 'GIO-1', N1, vao=2.0); nen('N1.1', 'THUYEN-2', -43, a=2.0, b=-2.0); khe_('N1.1', '1a', 1, 'SONG-3', -38, dai=6.6)
nen('N1.2', 'SONG-2', N1); nen('N1.2', 'DONG-3', -45, lp=1200, ghi='phố trong tường, không rõ chữ')
for i, t in enumerate([2.0, 9.5, 11.6, 13.4, 15.0, 16.1, 17.9, 19.3, 21.0, 22.4, 24.1]): ev('N1.2', ['PXA-1', 'PXA-2', 'PXA-3'][i % 3], 'shot', t, DL if t > 10 else -38, lp=2000, pan=[-0.6, 0.5, -0.2, 0.3, -0.5, 0.6][i % 6], fo=0.8, ghi='hạm đội bắn phá, dày dần ở 1d')
khe_('N1.2', '1d', 2, 'PXA-2', K3, pan=-0.3)
ev('N1.2', 'HOAMAI-1', 'shot', 18.6, -40, vao=2.85, lp=2500, pan=-0.4, fo=0.2, ghi='hoả mai xa (chỉ phần sau 2,85 s — không lời hô)'); ev('N1.2', 'HOAMAI-1', 'shot', 20.4, -42, vao=2.85, lp=2500, pan=0.3, fo=0.2)
nen('N1.3', 'GIO-2', N2); ev('N1.3', 'CO-1', 'shot', 0.5, -35, vao=8.0, dai=8.0, fi=0.5, fo=1.5, ghi='Borgoña hạ, Union kéo'); nen('N1.3', 'BUOC-2', -44, a=4.0, b=-3.0, ghi='lính vào lâu đài')
nen('N1.4', 'GIO-1', N2); nen('N1.4', 'DONG-3', -46, lp=900, ghi='dòng dân rời phố, rất xa'); nen('N1.4', 'BUOC-2', -44, vao=4.0); nen('N1.4', 'SONG-1', -44)
nen('N1.5', 'GIO-2', N2, b=0.0); nen('N1.5', 'SONG-1', N1, vao=8.0); ev('N1.5', 'PHO-1', 'moc:2015.5', 0.0, -42, dai=3.6, fi=0.3, fo=1.5, ghi='2015: phố + đường băng')
for t in [0.8, 2.6, 4.1, 7.3, 8.6, 10.2]: ev('N1.6', 'PXA-1' if t < 6 else 'PXA-3', 'shot', t, DL, lp=1800, pan=0.4, fo=0.8, ghi='vây 1704–05 / 1727')
nen('N1.6', 'GIO-1', N1); ev('N1.6', 'DAO-2', 'moc:1730.0', 0.5, -40, dai=14.0, fi=1.0, fo=2.0, lap=True, ghi='Línea mọc 1730–35'); ev('N1.6', 'DAO-1', 'moc:1730.0', 3.0, -42, dai=11.0, fi=1.0, fo=2.0)
nen('C1', 'DONG-3', -44, lp=1500, ghi='trại TBN 1779'); nen('C1', 'NGUA-1', -40, a=3.0); nen('C1', 'LUAN-1', -42); nen('C1', 'GIO-2', N1); nen('C1', 'CO-2', -44)
nen('C2', 'SONG-1', N2); nen('C2', 'THUYEN-1', -39, a=3.0, b=-1.0, ghi='thuyền châu Phi'); nen('C2', 'GIO-1', N1); ev('C2', 'SONG-3', 'shot', 8.0, -40, dai=4.0)
nen('C3', 'GIO-2', N2); nen('C3', 'CO-2', -42, a=1.0, b=-6.0); nen('C3', 'SONG-2', -43, a=6.0)
ev('C4', 'THUYEN-2', 'shot', 0.0, -38, dai=6.2, fi=0.4, fo=1.0, ghi='đoàn Rodney vào vịnh: dây/gỗ tàu gần máy'); ev('C4', 'SONG-1', 'shot', 0.0, -38, dai=6.2, fi=0.4, fo=1.0)
nen('C4', 'SONG-2', N2); nen('C4', 'THUYEN-1', -40, a=3.0); nen('C4', 'THUYEN-2', -43); nen('C4', 'DONG-3', -45, lp=1500, a=4.0, ghi='người khiêng thùng')
for t, m in [(3.62, K3), (4.4, DL), (5.2, DL), (6.1, DL)]: ev('C5', ['PXA-2', 'PXA-1', 'PXA-3', 'PXA-2'][int(t) % 4], 'shot', t, m, pan=-0.3, fo=0.8, ghi='pháo TBN bắn vào phố (sau neo)')
ev('C5', 'LUAL-1', 'moc:1781-04-12 15:00', 0.0, -36, dai=5.6, fi=1.5, fo=2.0, ghi='phố cháy đêm'); ev('C5', 'DONG-3', 'moc:1781-04-14 02:30', 0.0, -45, lp=1200, dai=3.0, fi=1.0, fo=1.5, ghi='dân chạy về nam'); nen('C5', 'GIO-2', N1)
nen('N2.6', 'GIO-2', N1); nen('N2.6', 'LUAN-1', -43); ev('N2.6', 'DAO-2', 'shot', 7.0, -40, dai=6.0, fi=0.5, fo=1.5, ghi='phố sập dần')
for t in [1.5, 4.0, 9.8, 12.6]: ev('N2.6', 'PXA-3', 'shot', t, -38, lp=1600, pan=0.5, fo=0.8)
khe_('N2.6', '2h', 1, 'PXA-1', K3 - 2, lp=2500)
nen('KA1782', 'GIO-1', N2); ev('KA1782', 'PXA-1', 'shot', 6.0, -40, lp=1200, pan=0.6, fo=1.0, ghi='một phát rất xa'); ev('KA1782', 'SONG-3', 'shot', 0.5, -42, dai=6.6)
nen('N2.10', 'DAO-1', -38); nen('N2.10', 'DAO-2', -42, vao=5.0); nen('N2.10', 'GIO-1', N1); khe_('N2.10', '2p', 1, 'NO-2', K3, lp=2500, ghi='nổ lỗ thông hơi')
nen('N2.7', 'GIO-2', N1); ev('N2.7', 'LUAL-3', 'shot', 3.0, -36, dai=11.42, fi=2.0, fo=2.0, ghi='công sự TBN cháy')
for t in [0.6, 2.2, 3.8, 5.9, 8.0]: ev('N2.7', 'PXA-2', 'shot', t, DL, pan=0.3, fo=0.8, ghi='đạn nung từ Rock')
khe_('N2.7', '2j', 1, 'PXA-1', K3)
nen('N2.8', 'SONG-1', N2, b=-6.0); nen('N2.8', 'THUYEN-2', -43, b=-6.0); nen('N2.8', 'GIO-2', N1, b=-6.0); ev('N2.8', 'SONG-3', 'shot', 4.0, -40, dai=6.6)
ev('N2.11', 'HOAMAI-1', 'shot', 2.6, -42, vao=2.85, lp=3000, pan=0.4, fo=0.2, ghi='hoả mai từ công sự (phần sau 2,85 s)'); ev('N2.11', 'HOAMAI-2', 'shot', 4.9, -42, lp=3000, pan=-0.2)
nen('N2.11', 'GIO-1', N2, a=3.0); nen('N2.11', 'SONG-2', N1, a=3.0); khe_('N2.11', '2q', 2, 'PXA-1', -31, off=0.02, lp=2500, fo=1.5, ghi='"the last shot was fired" — phát cuối, sau đó không pháo')
nen('N3.1', 'GIO-2', N1); nen('N3.1', 'SONG-1', -43); ev('N3.1', 'NO-2', 'moc:1810-02-14 08:00', 0.3, -38, lp=1500, pan=-0.3, ghi='San Felipe nổ'); khe_('N3.1', '3b', 1, 'NO-1', K3, off=0.02, vao=0.1, dai=5.0, lp=1800, fo=3.0, ghi='Santa Bárbara nổ')
nen('N3.2', 'GIO-1', N1); nen('N3.2', 'SONG-2', -43); ev('N3.2', 'CHIM-1', 'shot', 0.6, -42, vao=8.0, dai=7.4, fi=1.0, fo=1.5, ghi='mòng biển cảng 1810–60')
nen('N3.1', 'NGUA-2', -44, a=1.0, b=-11.0, ghi='xe ngựa trên lối đất (bậc 5)'); nen('N3.4', 'NGUA-2', -45, a=7.0, b=-2.0, ghi='xe ngựa trên lối đất')
nen('N3.3', 'DONG-1', -45, lp=1500, ghi='La Línea thế kỷ 19, không rõ chữ'); nen('N3.3', 'NGUA-1', -42, a=2.0); nen('N3.3', 'GIO-2', N1)
nen('KC1910', 'DONG-1', -39, lp=3500, ghi='phố La Línea 1910, tiếng TBN'); nen('KC1910', 'NGUA-1', -38, vao=10.0); nen('KC1910', 'BUOC-2', -43)
nen('N3.4', 'GIO-2', N2); nen('N3.4', 'DONG-1', -47, lp=1000, vao=10.0)
nen('N3.5', 'GIO-1', N2); ev('N3.5', 'MAYBAY-1', 'moc:1934.0', 0.0, -43, lp=1500, fi=1.5, fo=1.5, pan=0.4, ghi='cánh quạt xa, một lượt')
nen('N4.1', 'GIO-2', N1); nen('N4.1', 'DAO-2', -41, a=3.0); nen('N4.1', 'DAO-1', -43, a=6.0); ev('N4.1', 'MAYBAY-1', 'moc:1941.0', 0.0, -42, lp=1500, fi=1.5, fo=1.5)
nen('N4.2', 'SONG-2', N1); nen('N4.2', 'DAO-2', -41); khe_('N4.2', '4c', 1, 'NO-2', K3, lp=2500, ghi='nổ mìn vách bắc'); ev('N4.2', 'MAYBAY-1', 'shot', 18.0, -43, lp=1500, fi=1.5, fo=1.5)
nen('N4.3', 'GIO-1', N1); ev('N4.3', 'MAYBAY-1', 'shot', 0.5, -42, lp=1500, fi=1.0, fo=1.5); ev('N4.3', 'SONG-3', 'shot', 1.5, -42, dai=6.6)
nen('N4.4', 'SONG-1', N2, b=-0.6, fo=2.5); nen('N4.4', 'GIO-2', N1, b=-0.6, fo=2.5); ev('N4.4', 'COI-1', 'shot', 1.2, -38, lp=4000, fi=0.3, fo=2.0, ghi='tàu sơ tán rời cảng 5/1940 (khe đầu SM3)')
ev('N4.4', 'MAYBAY-1', 'shot', 8.2, -38, lp=2500, fi=1.0, fo=1.5); ev('N4.4', 'MAYBAY-1', 'shot', 11.5, -33, lp=3000, dai=5.2, fi=1.0, fo=3.0, ghi='4g không lời: máy bay tụ dần, TẮT trước 550,6 (KB1943)')
nen('N4.5', 'MAYBAY-1', -40, lp=2500, fi=1.0); nen('N4.5', 'SONG-1', N1, fi=1.0); nen('N4.5', 'GIO-2', -43, fi=1.0)
nen('N5.1', 'GIO-2', N1); ev('N5.1', 'DONG-2', 'shot', 0.0, -40, lp=2500, dai=3.8, fi=1.5, fo=0.6, ghi='dòng người qua cổng 1946–69'); ev('N5.1', 'BUOC-1', 'shot', 0.0, -40, dai=3.8, fi=1.5, fo=0.6)
ev('N5.1', 'DONG-2', 'shot', 4.9, -41, lp=2000, dai=4.6, fi=0.6, fo=1.2, ghi='8/6/1969: đám đông dừng ở rào chắn, rì rầm (không rõ chữ)'); ev('N5.1', 'DONG-2', 'moc:1985.0', 0.0, -40, lp=2500, dai=2.86, fi=1.0, fo=1.5, ghi='1985: người qua lại trở lại'); ev('N5.1', 'BUOC-1', 'moc:1985.0', 0.0, -40, dai=2.86, fi=1.0, fo=1.5)
nen('KB2026', 'PHO-2', -39); nen('KB2026', 'PHO-1', -42); ev('KB2026', 'CHIM-1', 'shot', 1.0, -42, dai=8.0, fi=1.0, fo=1.5, ghi='mòng biển ở cảng (CHIM-1, đoạn 5–33 s)')
nen('N5.2', 'BUOC-1', -38); nen('N5.2', 'DONG-2', -42, lp=3000); nen('N5.2', 'PHO-1', -43)
nen('KC2026', 'PHO-1', -39); nen('KC2026', 'DONG-1', -41, lp=4000)
nen('N5.3', 'BUOC-1', -42); nen('N5.3', 'DONG-2', -44, lp=3000); nen('N5.3', 'PHO-1', -43); nen('N5.3', 'GIO-2', -43)
nen('N5.4', 'DONG-2', -43, lp=3000); nen('N5.4', 'PHO-1', -43); nen('N5.4', 'GIO-2', N1)
nen('N5.5', 'SONG-1', N2, b=-0.4, fo=2.5); nen('N5.5', 'GIO-1', N1, b=-0.4, fo=2.5); ev('N5.5', 'SONG-3', 'shot', 2.0, -41, dai=6.6)
nen('N5.6', 'GIO-2', N1, b=0.0, fi=1.0); ev('N5.6', 'PHO-1', 'moc:2026-10-18 13:00', 0.0, -43, dai=4.9, fi=0.5, fo=0.8); ev('N5.6', 'DEM-1', 'moc:2026-10-18 19:30', 0.0, -42, dai=6.6, fi=1.5, fo=2.5); ev('N5.6', 'PHO-3', 'moc:2026-10-18 19:30', 0.0, -43, dai=6.6, fi=1.5, fo=2.5)
# ---- kiểm: tấm im lặng, thời kỳ, tệp
loi = []
for e in E:
    a, b = e['t'], e['t'] + (e.get('dai') or UV[e['uv']]['dai_s'] - e.get('vao', 0))
    for s in BS:
        if s['ma'] in IM and a < s['t1'] and b > s['t0']: loi.append(f"{e['shot']} {e['uv']} {a:.1f}–{b:.1f} chạm tấm/ thẻ {s['ma']}")
    lo = UV[e['uv']]['loai']; y = nam_tai(e['t'] + 0.05)
    if y is not None and lo not in KY[ky(y)]: loi.append(f"{e['shot']} {e['uv']} ({lo}) ở {e['t']:.1f} s = năm {y:.1f} ({ky(y)}): sai thời kỳ")
E.sort(key=lambda e: e['t'])
T1 = max(x['t1'] for x in BS)
json.dump(dict(t0=0.0, t1=T1, doan='ca-phim-cuoi', mo_ta='BAN-CUOI-T3 gói SFX bản cuối (neo theo cuoi/bang-shot.json)', so_su_kien=len(E), tep=sorted(set(e['uv'] for e in E)), kiem=dict(loi=loi), su_kien=E), open(sys.argv[1], 'w'), ensure_ascii=False, indent=0)
print(len(E), 'sự kiện;', len(set(e['uv'] for e in E)), 'tệp; lỗi kiểm:', len(loi)); [print('  ', l) for l in loi[:30]]
