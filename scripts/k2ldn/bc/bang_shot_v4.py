#!/opt/cine/bin/python
"""BAN-CUOI-T4-A · việc 6 — BẢNG SHOT v4 (channel-k2/k2c-t4-02/ban-cuoi/BANG-SHOT-v4.{md,json}) sinh từ đặc tả v4 (ban-cuoi/dac-ta-v4/, dac_ta_v4.py)
+ BẢNG SHOT v3 (điểm máy, thời gian) — v1…v3 giữ nguyên. Lớp mỗi shot: D 3D (look3 cờ d) / D 3D look2d tầm phố / B (AI bề mặt nhà ≥ 4 px/m — đề xuất) / E (tấm AI toàn khung 2026)
/ Omni (M-d) / THAT (ảnh thật) / TL (tư liệu toàn khung) / PP (thẻ phương pháp). In tự kiểm (lệnh việc 6).   bang_shot_v4.py"""
import json, os
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
EP = f'{REPO}/channel-k2/k2c-t4-02'; D4 = f'{EP}/ban-cuoi/dac-ta-v4'
LS = json.load(open(f'{D4}/log-shot.json')); DOI = json.load(open(f'{D4}/doi-v3-v4.json')); B3 = {x['ma']: x for x in json.load(open(f'{EP}/BANG-SHOT-v3.json'))['shot']}
LC = json.load(open(f'{D4}/log-chu-khoang.json'))['muc']
B_DE_XUAT = {'H5-06': 'B-H5-06', 'H2-12': 'B-H2-12b'}
P1_LAI = []   # shot P1 phải dựng lại nếu dời điểm đứng (việc 2) — chỉ ghi, điểm hiện tại giữ
rows = []
for L in LS:
    ma = L['shot']; cm = L.get('cu_may'); lop = L.get('lop') or {}
    if cm == 'MD': lp = 'Omni (M-d)'
    elif cm == 'PP': lp = 'PP (thẻ)'
    elif cm in ('TL', 'THAT'): lp = 'THAT (ảnh thật)' if 'THAT' in lop else 'TL (tư liệu toàn khung)'
    elif ma == 'H5-05a': lp = 'E (tấm AI toàn khung 2026, CODINH)'
    elif B3.get(ma, {}).get('trang') == 'look2d': lp = 'D 3D look2d tầm phố'
    else: lp = 'D 3D (look3 cờ d)' + (' + B đề xuất' if ma in B_DE_XUAT else '')
    if L.get('diem_may') == 'P1': P1_LAI.append((ma, L['dur']))
    rows.append(dict(ma=ma, t0=L['t0'], dur=L['dur'], chuong=L['chuong'], diem_may=L.get('diem_may'), cu_may=cm, goc=L.get('goc'), lop_shot=lp, lop=lop, vung=L.get('vung'),
                     vai=L.get('vai', ''), md=(L.get('minh_hoa') or [{}])[0].get('luot') if cm == 'MD' else None, tu_lieu_lan=L.get('tu_lieu_lan'),
                     nhan_vat_ten=L.get('nhan_vat_ten') or [], doi=[d[1] for d in DOI if d[0] == ma]))
    mh0 = (L.get('minh_hoa') or [{}])[0] if cm == 'MD' else {}
    if mh0.get('chan_dung'):   # lệnh bổ sung #1: nhân vật có tên không chân dung (H3-05b)
        rows[-1].update({k: mh0[k] for k in ('chan_dung', 'chan_dung_nguon_da_tra', 'mat_yunet', 'duyet_chu_du_an')})
T = round(sum(r['dur'] for r in rows), 3); than = round(sum(r['dur'] for r in rows if r['cu_may'] != 'PP'), 3)
s = lambda f: round(sum(r['dur'] for r in rows if f(r)), 3)
cao = s(lambda r: r['goc'] == 'cao' and r['cu_may'] not in ('MD', 'TL', 'THAT'))
omni = s(lambda r: r['cu_may'] == 'MD'); that = s(lambda r: 'THAT' in r['lop_shot']); tl = s(lambda r: r['lop_shot'].startswith('TL'))
chong = round(sum(v for r in rows if r['cu_may'] not in ('TL', 'THAT') for k, v in r['lop'].items() if k in ('THE', 'KHAC', 'TL')), 3)
tu_lieu_pct = round(100 * (chong + that + tl) / than, 2); E_s = s(lambda r: r['lop_shot'].startswith('E'))
map_pct = round(100 * sum(v for r in rows for k, v in r['lop'].items() if k in ('MAP', 'MAP3D')) / than, 2); thap = s(lambda r: r['goc'] == 'thap')
K = []
def ck(ten, gt, tran=None, san=None, ghi=''):
    ok = (tran is None or gt <= tran) and (san is None or gt >= san); ng = tran if tran is not None else san
    gan = isinstance(gt, (int, float)) and ng not in (None, 0) and abs(gt - ng) / abs(ng) <= 0.05
    K.append(dict(chi_so=ten, gia_tri=gt, tran=tran, san=san, dat=ok, trong_5pct=gan, ghi=ghi))
ck('Thời lượng ≤ 780 s', T, tran=780)
ck('Góc cao / thân phim % (≥ 50)', round(100 * cao / than, 2), san=50, ghi='ước theo điểm máy; số đo thật: k2check theo log khung ở bản dựng')
ck('Omni (M-d) % thân phim', round(100 * omni / than, 2), ghi='không có sàn/trần cứng (Q2); chỉ ghi')
ck('Tư liệu + khắc + thẻ + THẬT % (≤ 20)', tu_lieu_pct, tran=20)
ck('Bản đồ MAP + MAP3D % (≤ 12)', map_pct, tran=12)
ck('THAP % (≤ 12)', round(100 * thap / than, 2), tran=12)
ck('Tổng AI % (M-d + E; ≤ 70)', round(100 * (omni + E_s) / than, 2), tran=70)
ck('M-d mỗi clip ≤ 8 s', max(r['dur'] for r in rows if r['cu_may'] == 'MD'), tran=8.0)
# ≤ 2 shot liền nhóm thấp/cận/M-d/ảnh thật
nhom = lambda r: r['goc'] == 'thap' or r['cu_may'] == 'MD' or 'THAT' in r['lop_shot']
dai = cur = 0; kt = None
for r in rows:
    if r['cu_may'] == 'PP': cur = 0; continue
    cur = cur + 1 if nhom(r) else 0
    if cur > dai: dai, kt = cur, r['ma']
ck('Chốt 3: ≤ 2 shot thấp/M-d/ảnh thật liền', dai, tran=2, ghi=f'dài nhất kết ở {kt}')
CH = []
for r in rows:
    if r['cu_may'] == 'PP': continue
    if not CH or CH[-1][0] != r['chuong']: CH.append((r['chuong'], []))
    CH[-1][1].append(r)
for ch, rs in CH:
    caoc = lambda r: r['goc'] == 'cao' and r['cu_may'] not in ('MD', 'TL', 'THAT')
    ck(f'Chốt 1 {ch}: mở và kết bằng góc cao', f"{rs[0]['ma']} / {rs[-1]['ma']}", ghi='' if caoc(rs[0]) and caoc(rs[-1]) else 'TRƯỢT'); K[-1]['dat'] = caoc(rs[0]) and caoc(rs[-1])
    ck(f'Chốt 4 {ch}: góc cao ≥ 40 %', round(100 * sum(r['dur'] for r in rs if caoc(r)) / sum(r['dur'] for r in rs), 2), san=40)
    if ch != 'MÓC':
        p1 = [r['ma'] for r in rs if r['diem_may'] == 'P1' or (r['cu_may'] == 'KHOP' and r['diem_may'] == 'P1')]
        ck(f'Chốt 2 {ch}: P1 tái xuất', ', '.join(p1) or '—'); K[-1]['dat'] = bool(p1)
    loai = {r['cu_may'] for r in rs if r['cu_may'] not in ('MD', 'TL', 'THAT', 'PP')}
    ck(f'{ch}: số loại cú máy ≥ 4', len(loai), san=4)
J = dict(tap='K2C-T4-02', phien='BAN-CUOI-T4-A', ngay='2026-10-26', nguon='ban-cuoi/dac-ta-v4 (dac_ta_v4.py) + BANG-SHOT-v3.json', loi='v3 (khoá, không đổi)', shot=rows,
         tong=dict(thoi_luong_s=T, than_phim_s=than, so_shot=len(rows), omni_s=omni, omni_pct=round(100 * omni / than, 2), E_s=E_s, THAT_s=that, TL_toan_khung_s=tl, chong_s=chong,
                   tu_lieu_that_pct=tu_lieu_pct, goc_cao_s=cao, goc_cao_pct=round(100 * cao / than, 2), md_clip=sum(1 for r in rows if r['cu_may'] == 'MD')),
         kiem=K, doi_v3_v4=DOI, p1_shot=P1_LAI, log_chu=LC)
json.dump(J, open(f'{EP}/ban-cuoi/BANG-SHOT-v4.json', 'w'), ensure_ascii=False, indent=1)
M = ['# BẢNG SHOT v4 — K2C-T4-02 London (BAN-CUOI-T4-A, 26/10/2026)', '',
     '> Sinh bằng `scripts/k2ldn/bc/bang_shot_v4.py` từ đặc tả v4 (`ban-cuoi/dac-ta-v4/`, `scripts/k2ldn/bc/dac_ta_v4.py`). Bản máy đọc: `BANG-SHOT-v4.json`. v1…v3 giữ nguyên. Lời v3 khoá (không đổi, không thu thêm).',
     '> Lớp: **D 3D** = look3 cờ d (bản cuối, LOOK-T4-8) · **E** = tấm AI toàn khung 2026 máy cố định (LUẬT E) · **B** = AI phủ bề mặt nhà thường ≥ 4 px/m (đề xuất, chờ duyệt) · **Omni** = M-d · **THAT**/**TL** = ảnh thật/tư liệu toàn khung · **PP** = thẻ phương pháp.', '',
     '| Mã | t | Dài (s) | Chương | Máy | Cú máy | Góc | Lớp shot | Vùng | Lớp chồng (s) | Vai | Đổi so v3 |', '|---|---|---|---|---|---|---|---|---|---|---|---|']
for r in rows:
    m, sx = divmod(r['t0'], 60); ch = ', '.join(f'{k} {v:g}' for k, v in r['lop'].items() if k not in ('A', 'MD'))
    M.append(f"| {r['ma']} | {int(m)}:{sx:04.1f} | {r['dur']:.3f} | {r['chuong']} | {r['diem_may'] or '—'} | {r['cu_may']} | {r['goc']} | {r['lop_shot']}{' · ' + r['md'] if r['md'] else ''} | {r['vung']} | {ch} | {r['vai'][:110]} | {'; '.join(r['doi'])} |")
M += ['', '## Tổng + tự kiểm', '', f"- Thời lượng **{T} s** · {len(rows)} shot · thân phim {than} s · Omni {omni} s ({J['tong']['omni_pct']} %, {J['tong']['md_clip']} clip) · E {E_s} s · THAT {that} s · TL toàn khung {tl} s · lớp chồng {chong} s.", '',
      '| Chỉ số | Giá trị | Trần | Sàn | Đạt | ±5 % quanh ngưỡng | Ghi |', '|---|---|---|---|---|---|---|']
for k in K: M.append(f"| {k['chi_so']} | {k['gia_tri']} | {k['tran'] if k['tran'] is not None else ''} | {k['san'] if k['san'] is not None else ''} | {'ĐẠT' if k['dat'] else '**TRƯỢT**'} | {'**CÓ**' if k['trong_5pct'] else ''} | {k['ghi']} |")
M += ['', '## Shot điểm máy P1 (phải dựng lại nếu chủ dự án chọn dời điểm đứng — việc 2; hiện giữ điểm cũ)', '', ', '.join(f'{a} ({b:g} s)' for a, b in P1_LAI) + f" — **{len(P1_LAI)} shot, {round(sum(b for _, b in P1_LAI), 3)} s**",
      '', '## Nhân vật có tên trong M-d', '', '| Mã | Nhân vật | Chân dung | Mặt lớn nhất (YuNet) | Duyệt chủ dự án |', '|---|---|---|---|---|']
M += [f"| {r['ma']} | {', '.join(r['nhan_vat_ten'])} | {'**khong_co** — đã tra: ' + '; '.join(r['chan_dung_nguon_da_tra']['noi']) + ' (' + r['chan_dung_nguon_da_tra']['ngay'] + ')' if r.get('chan_dung') == 'khong_co' else 'chân dung tham chiếu (khai)'} | "
      f"{(str(r['mat_yunet']['mat_lon_nhat']) + ' khung (khung ' + str(r['mat_yunet']['khung']) + ', điểm ' + str(r['mat_yunet']['diem']) + '; trần 0.125)') if r.get('mat_yunet') else '—'} | {r.get('duyet_chu_du_an') or ('A1 phiếu xem v2 (26/10 00:12)' if r['ma'] in ('H1-05a', 'H1-15b') else 'CHỜ — clip mới BAN-CUOI-T4-A (PHIẾU-A)')} |" for r in rows if r['nhan_vat_ten']]
M += ['', '## Lớp chữ (log_chu khoảng, giây phim)', '', '| t0 | t1 | Vai | Chữ |', '|---|---|---|---|'] + [f"| {m['t0']} | {m['t1']} | {m['role']} | {m['s']} |" for m in LC]
open(f'{EP}/ban-cuoi/BANG-SHOT-v4.md', 'w').write('\n'.join(M) + '\n')
print(json.dumps(J['tong'], ensure_ascii=False)); [print(('ĐẠT ' if k['dat'] else 'TRƯỢT ') + k['chi_so'], k['gia_tri']) for k in K if not k['dat'] or k['trong_5pct']]
