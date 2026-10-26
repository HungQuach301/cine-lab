#!/opt/cine/bin/python
"""BAN-CUOI-T4-A · việc 6 — đặc tả v4 (khai cho k2check 1.17.8, chế độ animatic) = khai animatic v3 (channel-k2/k2c-t4-02/animatic2/{episode.yaml, log-shot.json,
timeline.json, ghep-log.json} — đọc, không sửa) + thay đổi BAN-CUOI-T4-A, ghi ra channel-k2/k2c-t4-02/ban-cuoi/dac-ta-v4/. Clip M-d mới đọc từ ban-cuoi/omni/chon/*.txt
(không gõ tay — BAI-HOC ANIMATIC-T4-V2 sự cố 11). Thay đổi:
  (1) M00 mở lạnh: góc lửa KHÁC M03 (điểm P1b, VONG) · (2) M04 +0,5 EV (c9b) · (3) H1-15b cắt còn khung 0–110 (4,625 s; mặt > 1/8 ở khung 113–139) → H1-15h dài thêm
  (4) M-d mới đạt (H1-06x, H1-15x?, H5-02b?, H5-02s?, H5-04c, H5-05d?, H5-05b?) chèn bằng cách tách shot 3D cùng nhóm lời (lời không đổi, tổng nhóm không đổi)
  (5) H5-05a: tấm E (LUẬT E 1.17.8) — khai n2p_toan_khung_hien_dai, toa_co_ten, mat_na_ct, dem · (6) chú thích Hollar ≤ 6 từ (giữ "published 1666", không gán 1647)
  (7) `vung` mọi shot · `log_chu` khoảng · `tu_lieu_lan` mọi lớp TL/KHAC/THE/MAP trong shot 3D (cách ranh M-d ≥ 1 s) · beats (biến cố thấy được khai, D4)
  dac_ta_v4.py [--e-mat-na thap|day]"""
import copy, hashlib, json, os, sys
import yaml
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
EP = os.path.join(REPO, 'channel-k2/k2c-t4-02'); A2 = f'{EP}/animatic2'; BC = f'{EP}/ban-cuoi'; OUT = f'{BC}/dac-ta-v4'; os.makedirs(OUT, exist_ok=True)
MN = sys.argv[sys.argv.index('--e-mat-na') + 1] if '--e-mat-na' in sys.argv else 'thap'
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
E = yaml.safe_load(open(f'{A2}/episode.yaml')); LS = json.load(open(f'{A2}/log-shot.json')); GL = json.load(open(f'{A2}/ghep-log.json'))
LD = {x['shot']: x for x in LS}


def doi_duong(o):
    """đường tương đối của khai v3 (so với animatic2/) → so với dac-ta-v4/"""
    if isinstance(o, dict): return {k: doi_duong(v) for k, v in o.items()}
    if isinstance(o, list): return [doi_duong(v) for v in o]
    if isinstance(o, str) and '/' in o and not o.startswith(('http', '/')) and os.path.exists(os.path.normpath(os.path.join(A2, o))):
        return os.path.relpath(os.path.normpath(os.path.join(A2, o)), OUT)
    return o


E = doi_duong(E); LS = doi_duong(LS); LD = {x['shot']: x for x in LS}
TL3 = {x['id']: x for x in json.load(open(f'{A2}/timeline.json'))['segments']}
SEG = E['segments']
for _s in SEG: _s['speech'] = copy.deepcopy(TL3[_s['id']].get('speech', []))
SI = lambda ma: next(i for i, s in enumerate(SEG) if s['id'] == ma)


def tach(ma, a, moi, seg_moi, log_moi):
    """tách segment `ma` tại a giây: phần sau thành shot mới `moi` (đặt ngay sau)."""
    i = SI(ma); s = SEG[i]; d = s['dur']; A = copy.deepcopy(s); B = copy.deepcopy(s); A['dur'] = round(a, 4); B['dur'] = round(d - a, 4); B['id'] = moi
    A['moc_loi'] = [m for m in s.get('moc_loi', []) if m['t'] < a]; B['moc_loi'] = [dict(m, t=round(m['t'] - a, 3)) for m in s.get('moc_loi', []) if m['t'] >= a]
    if 'speech' in s:
        A['speech'] = [[x, min(y, a)] for x, y in s['speech'] if x < a]; B['speech'] = [[round(max(x, a) - a, 3), round(y - a, 3)] for x, y in s['speech'] if y > a]
    A['beats'] = [b for b in s.get('beats', []) if b['t'] < a]; B['beats'] = [dict(t=0.0, k='cut', s=moi)]
    lc = s['shots'][0].get('p', {}).get('lop_chong', [])
    if lc: A['shots'][0]['p']['lop_chong'] = [x for x in lc if x['at'] < a]
    B['shots'] = [seg_moi]; SEG[i:i + 1] = [A, B]
    L = LD[ma]; LA = copy.deepcopy(L); LA['dur'] = round(a, 4); LA['t1'] = round(L['t0'] + a, 4); LA['lop'] = {k: (round(a, 4) if k == 'A' else v) for k, v in L['lop'].items()}
    LA['cau'] = [c for c in L.get('cau', []) if c['t'] < a]
    LB = dict(log_moi, ma=moi, shot=moi, t0=LA['t1'], t1=L['t1'], dur=round(d - a, 4), chuong=L['chuong'], cau=[dict(c, t=round(c['t'] - a, 3)) for c in L.get('cau', []) if c['t'] >= a])
    j = LS.index(L); LS[j:j + 1] = [LA, LB]; LD[ma] = LA; LD[moi] = LB


def chon(ma):
    p = f'{BC}/omni/chon/{ma}.txt'; return open(p).read().strip() if os.path.exists(p) else None


ML = json.load(open(f'{BC}/omni/lenh/muc-luc.json'))
def md(ma, dur, vai, vung):
    tag = chon(ma); M = ML[ma]; rel = lambda p: os.path.relpath(os.path.join(BC, p), OUT)
    km = [rel(f'omni/kiem2/qtd-moc-{ma}-l{tag.split("-l")[1][0]}-k{u}.json') for u in (25, 55, 90)]
    mh = dict(ma=ma, t0=0.0, t1=dur, luot=tag, so_luot=int(tag.split('-l')[1][0]), clip=rel(f'omni/clip/{tag}.mp4'), so_ai=os.path.relpath(f'{REPO}/reports/ban-cuoi-t4-a/so-ai-gemini.jsonl', OUT),
              muc_kiem='day_du', kiem_t1=rel(f'omni/kiem/{tag}-t1.json'), kiem=rel(f'omni/kiem2/{tag}-kiem.json'), kiem_moc=km,
              nhan_vat_ten=M.get('nhan_vat_ten', []), cong_trinh_moc=[M['cong_trinh_moc']], chan_troi_city=False, dau=rel(f'omni/dau/{tag.split("-360p")[0]}-dau.jpg'))
    if M.get('nhan_vat_ten'):
        mh['chan_dung_tham_chieu'] = [dict(tep=os.path.relpath(f'{REPO}/{p}', OUT), sha256=sha(f'{REPO}/{p}')) for p in M['tham_chieu']]
        mh['duyet_chu_du_an'] = None   # CHỜ chủ dự án duyệt từng clip (PHIEU-A mục A1) → (u) THIẾU tới khi có dòng AUTHORSHIP
    seg = dict(at=0, type='minh_hoa', tpl='plate', p=dict(sach=True, tl=False), cau=(M.get('loi') or '')[:200], noi='minh_hoa', vung=vung, ai_image=True, kiem=mh['kiem'])
    log = dict(goc='md', tl=False, cu_may='MD', lop={'MD': dur}, ai_nen=False, minh_hoa=[mh], vai=vai, tieu_diem_en=None, diem_may='—', thoi_gian=None, ai_image=True,
               kiem=mh['kiem'], muc_kiem='day_du', nhan_vat_ten=mh['nhan_vat_ten'], tu_lieu_chong_sau_ai=False, noi='minh_hoa', vung=vung, md_moi='BAN-CUOI-T4-A')
    return seg, log


DOI = []   # nhật ký thay đổi (cho bảng shot v4)
# (1) M00 — góc lửa khác M03
P1B = json.load(open(f'{BC}/may/M00-moi-a.json'))['keys'][0]
LD['M00'].update(diem_may='P1b', cu_may='VONG', may_ban_cuoi='ban-cuoi/may/M00-moi-a.json', log_may=None,
                 vai='MỞ LẠNH: Bankside phía đông (125 m) nhìn đông bắc vào vòng lửa đầu cầu đêm 2/9/1666 — góc KHÁC M03 (hết lặp khung 0:40–0:50)')
DOI.append(('M00', 'điểm máy P1 → P1b [532560,180330,125] nhìn [532880,180760,15] fov 42°, DAY → VONG (bản cuối dựng lại)'))
LD['M04']['c9b_ev'] = 0.5; DOI.append(('M04', '+0,5 EV (C9b) ở dựng bản cuối'))
# (3) H1-15b cắt
i = SI('H1-15b'); j = SI('H1-15h'); cut = 4.625; dd = round(SEG[i]['dur'] - cut, 4)
SEG[i]['dur'] = cut; SEG[j]['dur'] = round(SEG[j]['dur'] + dd, 4)
SEG[j]['moc_loi'] = [dict(m, t=round(m['t'] + dd, 3)) for m in SEG[j].get('moc_loi', [])]
if 'speech' in SEG[j]: SEG[j]['speech'] = [[round(x + dd, 3), round(y + dd, 3)] for x, y in SEG[j]['speech']]
mo = SEG[i].get('moc_loi', []); SEG[j]['moc_loi'] = [dict(m, t=round(m['t'] - cut, 3)) for m in mo if m['t'] >= cut] + SEG[j]['moc_loi']; SEG[i]['moc_loi'] = [m for m in mo if m['t'] < cut]
L = LD['H1-15b']; L['dur'] = cut; L['t1'] = round(L['t0'] + cut, 4); L['lop'] = {'MD': cut}; L['minh_hoa'][0]['t1'] = cut; L['minh_hoa'][0]['cat_clip'] = [0, 110]
L2 = LD['H1-15h']; L2['t0'] = L['t1']; L2['dur'] = round(L2['dur'] + dd, 4); L2['lop'] = {'A': L2['dur']}
DOI.append(('H1-15b', f'7,5 → 4,625 s (clip khung 0–110; YuNet hộp > 1/8 ở khung 113–139 — báo nhầm trên trời, vẫn cắt theo A1); H1-15h +{dd} s'))
# (4) M-d mới
CH = [('H1-06', 13.5, 'H1-06x', 6.0, 'M-d DN03 sà lan hoàng gia: Charles II + James trên Thames chiều 2/9/1666 (khung xa)', 'thames_bo_bac'),
      ('H1-15h', None, 'H1-15x', 6.0, 'M-d DN04 nhà Vua + Công tước York ở tuyến chữa cháy Fleet Street 4/9/1666 (khung xa)', 'fleet_street'),
      ('H5-02', 3.875, 'H5-02b', 4.0, 'M-d tháp Barbican đang xây (1973) từ London Wall', 'london_wall'),
      ('H5-04', 4.417, 'H5-04c', 6.0, 'M-d cụm toà cao Leadenhall/Bishopsgate từ phố 2026', 'leadenhall'),
      ('H5-05c', 4.5, 'H5-05d', 6.0, 'M-d mái vòm nhìn bắc từ cầu Millennium 2026', 'bankside_st_pauls')]
for ma, a, moi, dur, vai, vung in CH:
    if not chon(moi): DOI.append((moi, 'Omni KHÔNG đạt (2 lượt) → giữ 3D, không chèn')); continue
    if a is None: a = round(SEG[SI(ma)]['dur'] - dur, 4)
    s, l = md(moi, dur, vai, vung); tach(ma, a, moi, s, l); DOI.append((moi, f'chèn M-d {dur} s (tách {ma} tại {a} s)'))
for ma, vung, dur in (('H5-02s', 'london_wall', 7.0), ('H5-05b', 'fleet_ludgate', 8.0)):
    if not chon(ma): DOI.append((ma, 'Omni KHÔNG đạt → giữ 3D tầm phố/thấp')); continue
    i = SI(ma); old = SEG[i]['dur']; s, l = md(ma, dur, LD[ma]['vai'] + ' → M-d Omni', vung)
    SEG[i]['shots'] = [s]; SEG[i]['dur'] = dur; L = LD[ma]; keep = {k: L[k] for k in ('ma', 'shot', 't0', 'chuong', 'cau')}; L.clear(); L.update(l); L.update(keep); L['dur'] = dur; L['t1'] = round(L['t0'] + dur, 4)
    if old > dur:   # phần dư sang shot 3D sau (H5-06)
        k = SI(ma) + 1; SEG[k]['dur'] = round(SEG[k]['dur'] + old - dur, 4); SEG[k]['moc_loi'] = [dict(m, t=round(m['t'] + old - dur, 3)) for m in SEG[k].get('moc_loi', [])]
        nx = LS[LS.index(L) + 1]; nx['t0'] = L['t1']; nx['dur'] = SEG[k]['dur']; nx['lop'] = {kk: (nx['dur'] if kk == 'A' else v) for kk, v in nx['lop'].items()}
    DOI.append((ma, f'3D → M-d Omni {dur} s'))
# (5) E cho H5-05a
T = os.path.relpath(f'{BC}/e/tam/E-P9-ngay', OUT); sx = '-thap' if MN == 'thap' else ''
toa = json.load(open(f'{BC}/e/tam/E-P9-ngay/toa{sx}.json'))
E['n2p']['tam'] = [dict(id=f'E-P9-ngay-l1{sx}', shot='H5-05a', render=f'{T}/render.png', ghep=f'{T}/l1{sx}/ghep.png', mat_na=f'{T}/matna{sx}.png', nam=2026, anh_tinh=True,
                        n2p_toan_khung_hien_dai=True, nam_min=2020, cu_may='CODINH', dem=False, mat_na_ct=f'{T}/mat_na_ct{sx}.png', toa_co_ten=[dict(ten=t['ten'], mau=t['mau']) for t in toa], noi='bo_nam_bankside')]
LD['H5-05a']['n2p_tam'] = E['n2p']['tam'][0]['id']; LD['H5-05a']['lop_ban_cuoi'] = 'E'; DOI.append(('H5-05a', f'tấm nền N2P cũ → tấm E (LUẬT E, mặt nạ {MN})'))
# (6) chú thích Hollar ≤ 6 từ
CAP = {'Hollar: London before the Fire (pub. 1666)': 'Hollar, pre-Fire view, published 1666', "Hollar: Old St Paul's from the east": "Old St Paul's, by Hollar"}
for sh, v in GL['khac'].items():
    if v[1] in CAP: DOI.append((sh, f'chú thích "{v[1]}" → "{CAP[v[1]]}"')); v[1] = CAP[v[1]]
# (7) vùng
VUNG = {'P1': 'bankside_city', 'P1b': 'bankside_dong_cau', 'P2': 'st_saviour', 'P3': 'monument_dong', 'P4': 'fleet_ludgate', 'P4b': 'fleet_ludgate', 'P5': 'cripplegate_bac',
        'P6': 'thames_cau', 'P6h': 'thames_cau', 'P7': 'city_tren_cao', 'P8': 'tower_hill', 'P9': 'bankside_st_pauls', 'P10': 'guildhall', 'P11': 'london_wall'}
VMD = {'H1-01a': 'pudding_lane', 'H1-01b': 'pudding_lane', 'H1-02': 'pudding_lane', 'H1-05a': 'whitehall', 'H1-05b': 'thames_cau', 'H1-06b': 'cannon_street', 'H1-07b': 'thames_cau',
       'H1-10': 'cheapside', 'H1-12': 'thames_cau', 'H1-11b': 'royal_exchange', 'H1-14': 'st_pauls_cu', 'H1-15m': 'tower_street', 'H1-15b': 'navy_office', 'H1-17a': 'moorfields',
       'H1-17b': 'moorfields', 'H2-01a': 'cheapside', 'H2-01b': 'royal_exchange', 'H2-03c': 'cliffords_inn', 'H2-04b': 'fleet_street', 'H2-07': 'pho_gach', 'H2-13': 'thames_cau',
       'H3-04b': 'hem_city', 'H3-05b': 'mai_city', 'H4-01b': 'pho_city', 'H4-03': 'thames_bo_bac', 'H4-04b': 'st_pauls_mai', 'H4-04d': 'guildhall'}
for L in LS:
    if not L.get('vung'): L['vung'] = VUNG.get(L.get('diem_may')) or VMD.get(L['shot']) or ('tu_lieu' if L.get('cu_may') in ('TL', 'THAT') else 'the_pp' if L.get('cu_may') == 'PP' else L.get('noi') or 'khac')
for s in SEG:
    for sh in s['shots']: sh.setdefault('vung', LD.get(s['id'], {}).get('vung', 'the_pp'))
# thời gian tuyệt đối + timeline
t = 0.0
for s in SEG:
    s['t0'] = round(t, 4); s['t1'] = round(t + s['dur'], 4); s['frames'] = round(s['dur'] * 24); t += s['dur']
    if s['id'] in LD: LD[s['id']]['t0'] = s['t0']; LD[s['id']]['t1'] = s['t1']; LD[s['id']]['dur'] = s['dur']
TONG = round(t, 4)
# log chữ khoảng + tu_lieu_lan (giờ ghep-log v3 theo t0 shot v3 → shot v4 cùng mã; giữ khoảng tương đối trong shot)
T3 = {x['shot']: x['t0'] for x in json.load(open(f'{A2}/log-shot.json'))}
def doi_t(tt):
    """giờ v3 → v4 qua shot chứa nó (khoảng tương đối giữ nguyên)"""
    for x in json.load(open(f'{A2}/log-shot.json')):
        if x['t0'] - 1e-6 <= tt < x['t1']: return LD[x['shot']]['t0'] + (tt - x['t0']), x['shot']
    return tt, None
muc = []
for tt, du, a, b, *_ in GL['the']:
    t4, sh = doi_t(tt); muc.append(dict(t0=round(t4, 3), t1=round(t4 + du, 3), role='the_nhan_vat', s=a + (' · ' + b if b else ''), shot=sh))
for tt, du, a, b in GL['dem']:
    t4, sh = doi_t(tt); muc.append(dict(t0=round(t4, 3), t1=round(t4 + du, 3), role='bo_dem_so', s=f'{a} {b}'.strip(), shot=sh))
for sh, (rid, cap, a, du, kieu) in GL['khac'].items():
    if sh in LD: muc.append(dict(t0=round(LD[sh]['t0'] + a, 3), t1=round(LD[sh]['t0'] + a + du, 3), role='chu_thich_tu_lieu', s=cap, shot=sh))
# ranh M-d ≥ 1 s: cửa sổ trong shot 3D sát M-d → dời/cắt cho cách ranh ≥ 1 s (ghi nhật ký)
MDR = [(L['t0'], L['t1']) for L in LS if L.get('cu_may') == 'MD']
for m in muc:
    if LD.get(m['shot'], {}).get('cu_may') == 'MD': continue   # thẻ chữ trên chính clip M-d (không phải tư liệu ảnh) — giữ như v3
    for a, b in MDR:
        if a - 1.0 < m['t1'] <= a + 1e-6 and m['t0'] < a: n1 = round(a - 1.0, 3); DOI.append((m['shot'], f'lớp chữ "{m["s"]}" kết {m["t1"]} → {n1} (cách M-d ≥ 1 s)')); m['t1'] = n1
        if b - 1e-6 <= m['t0'] < b + 1.0 and m['t1'] > b: n0 = round(b + 1.0, 3); DOI.append((m['shot'], f'lớp chữ "{m["s"]}" mở {m["t0"]} → {n0} (cách M-d ≥ 1 s)')); m['t0'] = n0
muc = [m for m in muc if m['t1'] - m['t0'] >= 1.0]
for L in LS:
    if L.get('cu_may') in ('MD',): L.pop('tu_lieu_lan', None); continue
    w = [dict(t0=m['t0'], t1=m['t1'], lop='THE' if m['role'] in ('the_nhan_vat', 'bo_dem_so') else 'KHAC') for m in muc if L['t0'] - 1e-6 <= m['t0'] < L['t1']]
    if L.get('cu_may') in ('TL', 'THAT'): w = [dict(t0=L['t0'], t1=L['t1'], lop=(L.get('lop') and list(L['lop'])[0]) or 'TL')]
    for k in ('MAP', 'MAP3D', 'TL'):
        if (L.get('lop') or {}).get(k) and L.get('cu_may') not in ('TL', 'THAT'): w.append(dict(t0=L['t0'], t1=round(L['t0'] + L['lop'][k], 3), lop=k))
    if w: L['tu_lieu_lan'] = w
json.dump(dict(fmt='khoang', muc=[{k: v for k, v in m.items() if k != 'shot'} for m in muc]), open(f'{OUT}/log-chu-khoang.json', 'w'), ensure_ascii=False, indent=1)
# beats: cắt + câu lời + lớp chữ + biến cố timelapse thấy được mỗi ≤ 5 s trong shot 3D có thời gian chạy (D4: biến cố đo T4 không cộng — khai)
for s in SEG:
    L = LD.get(s['id'], {}); b = {(round(x['t'], 2), x['k']) for x in s.get('beats', [])}
    for m in s.get('moc_loi', []): s.setdefault('beats', []).append(dict(t=m['t'], k='loi', s=m['s'][:28])) if (round(m['t'], 2), 'loi') not in b else None
    for m in muc:
        if s['t0'] <= m['t0'] < s['t1']: s.setdefault('beats', []).append(dict(t=round(m['t0'] - s['t0'], 3), k=m['role'], s=m['s'][:28]))
    if L.get('tl') and L.get('cu_may') not in ('MD', 'TL', 'THAT', 'PP') and L.get('thoi_gian'):
        x = 4.0
        while x < s['dur'] - 0.5: s['beats'].append(dict(t=x, k='bien_co_tl', s=f"timelapse {L['thoi_gian'][0]}: thời gian/lửa/ánh sáng đổi")); x += 4.0
    s['beats'] = sorted(s.get('beats', []), key=lambda z: z['t'])
E['log_chu'] = 'log-chu-khoang.json'; E['id'] = 'k2c-t4-02-dac-ta-v4'; E['title'] = 'London — T4 đặc tả v4 (BAN-CUOI-T4-A; chưa dựng — kiểm đặc tả)'
E['so_ai_gemini'] = os.path.relpath(f'{REPO}/reports/ban-cuoi-t4-a/so-ai-gemini-t4-gop.jsonl', OUT)
with open(f'{REPO}/reports/ban-cuoi-t4-a/so-ai-gemini-t4-gop.jsonl', 'w') as f:
    for p in ('reports/tien-ky-t4/so-ai-gemini.jsonl', 'reports/look-t4-v2/so-ai.jsonl', 'reports/animatic-t4/so-ai-gemini.jsonl', 'reports/animatic-t4-v2/so-ai-gemini.jsonl', 'reports/ban-cuoi-t4-a/so-ai-gemini.jsonl'):
        q = f'{REPO}/{p}'
        if os.path.exists(q):
            for l in open(q):
                if l.strip():
                    r = json.loads(l)
                    if 'gemini' in str(r.get('model_req') or r.get('model') or r.get('nha') or '').lower(): r.setdefault('so_goc', p); f.write(json.dumps(r, ensure_ascii=False) + '\n')
E2 = copy.deepcopy(E); E2['segments'] = [{k: v for k, v in x.items() if k not in ('speech', 't0', 't1', 'frames')} for x in SEG]
yaml.safe_dump(E2, open(f'{OUT}/episode.yaml', 'w'), allow_unicode=True, sort_keys=False, width=200)
json.dump(LS, open(f'{OUT}/log-shot.json', 'w'), ensure_ascii=False, indent=1)
TL = dict(id=E['id'], title=None, music=[], segments=[{k: v for k, v in s.items()} | {'shots': [dict(id=s['id'], at=0.0, tpl=s['shots'][0].get('tpl', 'plate'), t0=0.0, t1=s['dur'])], 'sfx': s.get('sfx', []), 'speech': s.get('speech', [])} for s in SEG],
          heroes={}, tong_s=TONG, tong_khung=sum(s['frames'] for s in SEG))
json.dump(TL, open(f'{OUT}/timeline.json', 'w'), ensure_ascii=False)
json.dump(DOI, open(f'{OUT}/doi-v3-v4.json', 'w'), ensure_ascii=False, indent=1)
print('tổng', TONG, 's ·', len(SEG), 'segment ·', len(LS), 'shot ·', len(muc), 'lớp chữ ·', len(DOI), 'thay đổi')
