#!/opt/cine/bin/python
"""BAN-CUOI-T4-B1 · hình học look3d (THU-B D, chạy hinh_hoc_thub.py d như bc/hinh_hoc_e.py) + SỬA NIÊN ĐẠI TOÀ OSM cho cảnh 1950s–70s (PHIẾU-A Q-A5 (a), D-A4 (vi)).
Lỗi đo được ở BAN-CUOI-T4-A (§4, K94): (1) hinh_hoc_look.toa_start ép mọi toà > 120 m về năm ≥ 1995 → ba tháp Barbican (123 m, xây 1973–1976) VẮNG trong cảnh 1973–1976;
(2) toà thiếu start_date nhận năm ngẫu nhiên 1950–2020 → toà kính đời 2000s đứng trong cảnh London Wall 1976, lô đất trống chỗ khác.
Sửa (không đổi chuỗi ngẫu nhiên chung — mọi năm mới lấy từ băm id toà, không gọi RNG):
  (a) bảng năm xây có nguồn cho toà đã biết (BANG_NAM, nguồn ở cột 3);
  (b) Barbican Estate (khối ở apartments/residential trong hộp E 532000–532520, N 181690–182000, thiếu năm): 1965–1976 (Barbican Estate xây 1965–1976);
  (c) hành lang London Wall (Route 11, E 531950–532760, N 181440–181700), toà thiếu năm: dựng lại 1985–2020 (các khối Route 11 thập niên 1960 đã bị thay 1980s–2010s);
  (d) vùng bom 1940 (BLITZ_M), toà thiếu năm có năm dựng > 1962: thêm KHỐI TIỀN NHIỆM hậu chiến (bê tông/đá, mái bằng, 1953–1961 → năm dựng toà hiện nay),
      cao 0,55 × cao toà, kẹp 15–55 m — City dựng lại 1950s–60s trên nền bom trước khi thay bằng toà nay;
  (e) START_R (raster năm dựng nhỏ nhất) vẽ lại sau khi đổi năm (khối Victoria ngoài vùng bom chết theo raster này).
Toà kính rèm (mt 7) dựng trước 1985 đọc thành văn phòng bê tông ở trang dựng (design/k2v/ldn/bc/look3-b1.js, theo tl.x) — không đổi hình học.
Ra: $LDN_DATA/look3d/* (như hinh_hoc_e.py) + look3d/nid.f32 (= mã toà OSM có tên, để trang dựng phân biệt toà tháp có tên) + look3e/* (liên kết, hid = mã có tên)
   + $LDN_DATA/look3d/nam_b1.json (mọi toà đổi năm + khối tiền nhiệm, để soi/ghi báo cáo).
  hinh_hoc_b1.py"""
import json, os, sys, zlib
sys.argv = [sys.argv[0], 'd']
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'thu-b'))
import hinh_hoc_thub as T          # noqa: E402
import numpy as np, cv2            # noqa: E402
HL = T.HL

# (a) năm HOÀN THÀNH có nguồn — id OSM hoặc tên OSM → (năm, ghi chú/nguồn); lớp 4 mọc trong 2,5 năm (look3.js gw) → năm xuất hiện = hoàn thành − 2,5
BANG_NAM = {
    'Cromwell Tower': (1973.0, 'Barbican Estate — tháp hoàn thành 1973 (Wikipedia "Barbican Estate"; City of London Corporation)'),
    'Lauderdale Tower': (1974.0, 'Barbican Estate — 1974 (Wikipedia "Barbican Estate")'),
    '34038683': (1976.0, 'Shakespeare Tower (OSM không tên) — 1976 (Wikipedia "Barbican Estate")'),
    '208935491': (1967.0, 'City Point = Britannic House 1967, ốp lại 2000 (Wikipedia "CityPoint")'),
    '2 London Wall Place': (2017.0, 'London Wall Place 2017 (Wikipedia)'),
    '5 Aldermanbury Square': (2007.0, '5 Aldermanbury Square 2007 (Wikipedia)'),
    '20 Ropemaker': (2021.0, '20 Ropemaker Street 2021'),
}
for _i in range(1485996625, 1485996630): BANG_NAM[str(_i)] = (2017.0, 'phần của London Wall Place (2017)')
BARB = (532000, 181690, 532520, 182000); LWALL = (531950, 181440, 532760, 181700)
inbox = lambda c, B: B[0] < c[0] < B[2] and B[1] < c[1] < B[3]
hb = lambda s, salt: (zlib.crc32(f'{s}|{salt}'.encode()) % 100000) / 100000.0
DOI = []; TIEN = {}

_ts, _toa = HL.toa_start, HL.toa


def toa_start_b1():
    _ts()                                              # giữ nguyên chuỗi rs của bản gốc
    S = HL.START
    for b in HL.R['toa']:
        if b['id'] not in S: continue
        r = np.array(b['r'], float); c = r.mean(0); st0 = S[b['id']]; known = None
        try: known = float(int(str(b.get('start') or '')[:4]))
        except Exception: pass
        st = st0; why = None
        for key in (b['id'], b.get('name')):
            if key in BANG_NAM: st, why = BANG_NAM[key][0] - 2.5, BANG_NAM[key][1] + ' — năm HOÀN THÀNH; toà lớp 4 mọc 2,5 năm nên năm xuất hiện = hoàn thành − 2,5'; break
        if why is None and known is None:
            if inbox(c, BARB) and b.get('b') in ('apartments', 'residential') and (b['h'] or 0) < 60: st, why = 1965.0 + 11.0 * hb(b['id'], 'barb'), 'Barbican Estate 1965–1976 (quy tắc b)'
            elif inbox(c, LWALL): st, why = 1985.0 + 35.0 * hb(b['id'], 'lw'), 'hành lang London Wall dựng lại 1985–2020 (quy tắc c)'
        if why: S[b['id']] = max(st, 1667.5); DOI.append(dict(id=b['id'], ten=b.get('name'), E=round(c[0]), N=round(c[1]), h=b['h'], cu=round(st0, 1), moi=round(S[b['id']], 1), ly_do=why))
        if known is None and why not in (None,) and 'Barbican' in why: continue
        if known is None and b['id'] not in [k for k in BANG_NAM] and HL.at(HL.BLITZ_M, c) and S[b['id']] > 1962.0 and not b['part']:
            TIEN[b['id']] = 1953.0 + 8.0 * hb(b['id'], 'tn')
    # (e) vẽ lại raster năm dựng nhỏ nhất (đúng phép của bản gốc)
    HL.START_R[:] = 9999.0
    for b in sorted([b for b in HL.R['toa'] if not b['part'] and b['id'] in S], key=lambda b: -S[b['id']]):
        cv2.fillPoly(HL.START_R, [np.round(HL.to_g(np.array(b['r'], float)) * 4).astype(np.int32)], float(min(S[b['id']], TIEN.get(b['id'], 9999.0))), shift=2)


def toa_b1(m):
    n = _toa(m); k = 0
    for b in HL.R['toa']:
        if b['id'] not in TIEN: continue
        r = np.array(b['r'], float)
        if len(r) > 3 and np.allclose(r[0], r[-1]): r = r[:-1]
        if len(r) < 3: continue
        c = r.mean(0)
        if not (HL.BB[0] + 30 < c[0] < HL.BB[2] - 30 and HL.BB[1] + 30 < c[1] < HL.BB[3] - 30): continue
        area = 0.5 * abs(np.dot(r[:, 0], np.roll(r[:, 1], 1)) - np.dot(r[:, 1], np.roll(r[:, 0], 1)))
        if area < 40: continue
        g = HL.Hg(*c); h = float(np.clip(0.55 * (b['h'] or 30.0), 15.0, 55.0)); ring = [HL.L(*p) for p in r]
        sa = sum(ring[i][0] * ring[(i + 1) % len(ring)][1] - ring[(i + 1) % len(ring)][0] * ring[i][1] for i in range(len(ring)))
        if sa < 0: ring = ring[::-1]
        u = hb(b['id'], 'mau'); mt = 8 if u < 0.7 else 6
        col = tuple(int(v * (0.92 + 0.12 * hb(b['id'], 'sang'))) for v in ((176, 172, 162) if mt == 8 else HL.PORTLAND))
        tl = (TIEN[b['id']], HL.START[b['id']], g, -1.0)
        m.prism(ring[::-1], g, g + h, g, col, (104, 104, 102), tl, 4, mt, 12, 8); k += 1
        DOI.append(dict(id=b['id'], ten=b.get('name'), E=round(c[0]), N=round(c[1]), h=round(h, 1), tien_nhiem=[round(TIEN[b['id']], 1), round(HL.START[b['id']], 1)], ly_do='khối tiền nhiệm hậu chiến (quy tắc d)'))
    n['tien_nhiem_b1'] = k; return n


HL.toa_start = toa_start_b1; HL.toa = toa_b1

T.HL.main()
J = os.path.join(T.HL.OUT, 'ldn2.json'); meta = json.load(open(J)); meta['phien_ban'] = 'look-v2 + cong-trinh-v2 (LOOK-T4-V2) — bản THU-B d + niên đại toà B1'; json.dump(meta, open(J, 'w'), ensure_ascii=False, indent=1)
T.sau_main()
# mã toà OSM có tên (như hinh_hoc_e.py) → look3e/hid.f32 + look3d/nid.f32
H = T.ARR['H']; K = T.ARR['K']; Ht = H[::3]; Kt = K[::3]
named = T.ten_toa(); ten = []; hid2ma = {}
for hid, inf in T.INFO.items():
    if inf['k'] != 4 or 'ring' not in inf: continue
    rr = np.array(inf['ring'], np.float32).reshape(-1, 1, 2)
    for (a, b, nm, oid) in named:
        if cv2.pointPolygonTest(rr, (float(a), float(b)), False) >= 0:
            ma = len(ten) + 1; hid2ma[hid] = ma
            ten.append(dict(ma=ma, ten=nm, osm_id=oid, E=round(inf['x'] + T.HL.E0, 1), N=round(-inf['z'] + T.HL.N0, 1), y1=round(inf['y1'], 1))); break
ids = np.zeros(len(Ht), np.float64)
sel = (Kt == 4) & np.isin(Ht, np.array(sorted(hid2ma), np.int64))
ids[sel] = [hid2ma[h] for h in Ht[sel]]
E = os.path.join(T.HL.H0.DATA, 'look3e'); os.makedirs(E, exist_ok=True)
for f in os.listdir(T.HL.OUT):
    if f in ('hid.f32', 'nid.f32'): continue
    d = os.path.join(E, f)
    if os.path.lexists(d): os.remove(d)
    os.symlink(os.path.join(T.HL.OUT, f), d)
nid = np.repeat(ids, 3).astype(np.float32); nid.tofile(os.path.join(E, 'hid.f32')); nid.tofile(os.path.join(T.HL.OUT, 'nid.f32'))
json.dump(ten, open(os.path.join(E, 'ten.json'), 'w'), ensure_ascii=False, indent=1)
json.dump(DOI, open(os.path.join(T.HL.OUT, 'nam_b1.json'), 'w'), ensure_ascii=False, indent=1)
print(json.dumps(dict(toa_co_ten=len(ten), tam_giac_co_ten=int(sel.sum()), doi_nam=sum(1 for d in DOI if 'moi' in d), tien_nhiem=sum(1 for d in DOI if 'tien_nhiem' in d)), ensure_ascii=False))
