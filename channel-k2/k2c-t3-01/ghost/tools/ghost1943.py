"""SH · ghost 1943 = OSM hôm nay làm nền, sửa theo AMS M981 (1943) đã nắn.
  ghost1943.py <gcp-1943-ams.json> <ảnh AMS (Princeton, chỉ nắn)> <out.geojson> <out-dir-kiem> [E0,N0,E1,N1 ...]
Mỗi toà OSM: tỷ lệ phủ mực "khối xây" AMS trong đa giác → có 1943 (≥ 0,45 cao · 0,25–0,45 vừa) / không có (bỏ, tính là xây sau 1943).
Khối xây AMS không trùng toà OSM được giữ (≥ 80 m², mực đặc, độ đặc ≥ 0,7, lấp chữ nhật bao ≥ 0,6, không chồng > 50 % lên tim đường OSM ±3 m hay nghĩa trang, cạnh ngắn ≥ 5 m, tỷ lệ ≤ 6 (≤ 15 nếu tô đặc ≥ 85 %), mực gốc ≥ 0,7, trong 40 m quanh toà 1943 đã xác nhận hoặc ở dải North Front) → toà đã phá sau 1943, vẽ từ AMS (do_tin vừa). Khối phố = hợp các toà 1943 (nở 3 m, co 3 m)."""
import json, os, sys
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(__file__))
from ghost import zones, utm, utm_inv, ring_area, OSM  # noqa: E402

MPP = 0.5


def main(gpath, img, out, kdir, *boxes):
    G = json.load(open(gpath)); z = zones(G)['pho']
    boxes = [tuple(map(float, b.split(','))) for b in boxes] or [(287950, 4001300, 288750, 4002850)]
    E0, N0 = min(b[0] for b in boxes), min(b[1] for b in boxes); E1, N1 = max(b[2] for b in boxes), max(b[3] for b in boxes)
    W, H = int((E1 - E0) / MPP), int((N1 - N0) / MPP)
    ee, nn = np.meshgrid(E0 + (np.arange(W) + .5) * MPP, N1 - (np.arange(H) + .5) * MPP)
    q = z['inv'](np.c_[ee.ravel(), nn.ravel()]).astype(np.float32)
    src = cv2.imread(img); gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY); b, g, r = [src[..., i].astype(int) for i in range(3)]
    ink = ((gray < 120) & (np.abs(r - b) < 60)).astype(np.uint8)          # mực đen/nâu (không lấy lưới xanh, nước)
    INK = cv2.remap(ink, q[:, 0].reshape(H, W), q[:, 1].reshape(H, W), cv2.INTER_LINEAR).astype(np.float32)
    dens = cv2.blur(INK, (9, 9))                                            # mật độ trong cửa sổ 4,5 m
    mass = (dens > 0.38).astype(np.uint8)
    mass = cv2.morphologyEx(mass, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    inbox = np.zeros((H, W), np.uint8)
    for b0 in boxes: inbox[int((N1 - b0[3]) / MPP):int((N1 - b0[1]) / MPP), int((b0[0] - E0) / MPP):int((b0[2] - E0) / MPP)] = 1
    T = lambda en: np.c_[(en[:, 0] - E0) / MPP, (N1 - en[:, 1]) / MPP].round().astype(np.int32)
    d = json.load(open(OSM)); feats = []; occ = np.zeros((H, W), np.uint8); keep = np.zeros((H, W), np.uint8)
    st = dict(osm_toa=0, co_1943_cao=0, co_1943_vua=0, khong_1943=0, chi_ams=0)
    for wid, (p, t) in d['ways'].items():
        if not t.get('building') or len(p) < 4: continue
        e, n = utm(np.array([a for a, _ in p]), np.array([c for _, c in p])); en = np.c_[e, n]; c = en.mean(0)
        if not any(b0[0] <= c[0] <= b0[2] and b0[1] <= c[1] <= b0[3] for b0 in boxes): continue
        st['osm_toa'] += 1
        m = np.zeros((H, W), np.uint8); cv2.fillPoly(m, [T(en)], 1); a = m.sum()
        if a < 4: continue
        cov = float((mass * m).sum() / a); cv2.fillPoly(occ, [T(en)], 1)
        if cov < 0.25: st['khong_1943'] += 1; continue
        dt = 'cao' if cov >= 0.45 else 'vua'; st['co_1943_' + dt] += 1; cv2.fillPoly(keep, [T(en)], 1)
        lv = t.get('building:levels'); tang = None
        try: tang = int(float(lv)) if lv else None
        except ValueError: tang = None
        feats.append(dict(type='Feature', geometry=dict(type='Polygon', coordinates=[[[round(float(x), 7), round(float(y), 7)] for x, y in zip(*utm_inv(en[:, 0], en[:, 1]))]]),
                          properties=dict(id='N1943-w' + wid, moc=1943, nguon_id='osm+pu-ams-m981-gibraltar-1943', loai='nha', do_tin=dt,
                                          so_tang_uoc=tang if tang else 3,
                                          cach_uoc_tang='OSM building:levels (hiện nay; giả định không đổi từ 1943)' if tang else 'tầng chuẩn mốc 1943: 3 (khoảng 2–5); AMS không ghi tầng, OSM không có building:levels',
                                          nguon_hinh='OSM way/' + wid + ' (ODbL)', phu_ams=round(cov, 2), dien_tich_m2=round(ring_area(en)))))
    # khối xây AMS không trùng toà OSM nào → toà đã phá sau 1943
    solid = cv2.morphologyEx((INK > 0.5).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))   # mực đặc gốc (toà tô đen), không làm mờ
    road = np.zeros((H, W), np.uint8)
    for wid, (p, t) in d['ways'].items():
        if len(p) < 2 or not (t.get('highway') or t.get('landuse') == 'cemetery' or t.get('amenity') == 'grave_yard'): continue
        e, n_ = utm(np.array([a for a, _ in p]), np.array([c for _, c in p])); qq = T(np.c_[e, n_])
        if t.get('highway'): cv2.polylines(road, [qq], False, 1, int(6 / MPP))
        else: cv2.fillPoly(road, [qq], 1)
    k = 0; why = {}
    near = cv2.dilate(keep, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (161, 161)))   # ≤ 40 m quanh toà 1943 đã xác nhận (OSM ∩ AMS)
    near[: int((N1 - 4002850) / MPP), :] = 1 if N1 > 4002850 else 0   # dải North Front (bắc 4 002 850 N): không có nền phố, xét toàn dải
    rest0 = solid & inbox & (1 - cv2.dilate(keep, np.ones((7, 7), np.uint8)))
    for ker in (19, 11):   # lượt 1: lõi toà lớn (rộng ≥ 9,5 m) tách khỏi nét bờ/đường dính vào; lượt 2: toà nhỏ còn lại
      rest = cv2.morphologyEx(rest0 & (1 - cv2.dilate(keep, np.ones((5, 5), np.uint8))), cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ker, ker)))
      n, lab, sts, _ = cv2.connectedComponentsWithStats(rest, 8)
      for i in range(1, n):
          a = sts[i, cv2.CC_STAT_AREA] * MPP * MPP
          if a < 80: continue
          cm = (lab == i).astype(np.uint8); cs, _ = cv2.findContours(cm, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE); c = max(cs, key=cv2.contourArea)
          if cv2.contourArea(c) / max(cv2.contourArea(cv2.convexHull(c)), 1) < 0.7: why['dac'] = why.get('dac', 0) + 1; continue    # bỏ nét thưa (chữ, gạch núi)
          (_, _), (rw, rh), _ = cv2.minAreaRect(c); sh, lo = min(rw, rh) * MPP, max(rw, rh) * MPP
          inkf = float((INK > 0.5)[lab == i].mean())
          if cv2.contourArea(c) / max(rw * rh, 1) < 0.6 or sh < 5 or lo / max(sh, 1e-3) > (15 if inkf >= 0.85 else 6): why['hinh'] = why.get('hinh', 0) + 1; continue   # dạng toà: rộng ≥ 6 m, không dài như đường/lối
          if inkf < 0.7: why['muc'] = why.get('muc', 0) + 1; continue   # nét đôi (lối, tường) sau đóng nét có lõi trắng
          if float(near[lab == i].mean()) < 0.5: why['xa'] = why.get('xa', 0) + 1; continue   # sườn núi xa phố: nét tường/lối
          if float(road[lab == i].mean()) > 0.5: why['duong'] = why.get('duong', 0) + 1; continue   # nằm trên tim đường/lối OSM (±3 m) hoặc trong nghĩa trang → nét đường, không phải toà
          c = cv2.approxPolyDP(c, 1.5 / MPP, True).reshape(-1, 2)
          if len(c) < 3: continue
          en = np.c_[E0 + (c[:, 0] + .5) * MPP, N1 - (c[:, 1] + .5) * MPP]; k += 1; cv2.fillPoly(keep, [T(en)], 1)
          feats.append(dict(type='Feature', geometry=dict(type='Polygon', coordinates=[[[round(float(x), 7), round(float(y), 7)] for x, y in zip(*utm_inv(en[:, 0], en[:, 1]))] + [[round(float(x), 7), round(float(y), 7)] for x, y in zip(*utm_inv(en[:1, 0], en[:1, 1]))]]),
                            properties=dict(id='N1943-a%03d' % k, moc=1943, nguon_id='pu-ams-m981-gibraltar-1943', loai='nha', do_tin='vua', so_tang_uoc=3,
                                            cach_uoc_tang='tầng chuẩn mốc 1943: 3 (khoảng 2–5); AMS không ghi tầng',
                                            ghi_chu='chỉ có trên AMS 1943, không có toà OSM hôm nay (đã phá/đổi) — vẽ từ mặt nạ mực AMS đã nắn', dien_tich_m2=round(a))))
    st['chi_ams'] = k; st['ung_vien_loai'] = why
    # khối phố
    blk = cv2.morphologyEx(keep, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13)))
    cs, _ = cv2.findContours(blk, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE); kb = 0; barea = 0
    for c in sorted(cs, key=lambda c: -cv2.contourArea(c)):
        a = cv2.contourArea(c) * MPP * MPP
        if a < 150: continue
        c = cv2.approxPolyDP(c, 1.5 / MPP, True).reshape(-1, 2); en = np.c_[E0 + (c[:, 0] + .5) * MPP, N1 - (c[:, 1] + .5) * MPP]; kb += 1; barea += a
        ll = [[round(float(x), 7), round(float(y), 7)] for x, y in zip(*utm_inv(en[:, 0], en[:, 1]))]
        feats.append(dict(type='Feature', geometry=dict(type='Polygon', coordinates=[ll + [ll[0]]]),
                          properties=dict(id='K1943-%03d' % kb, moc=1943, nguon_id='osm+pu-ams-m981-gibraltar-1943', loai='khoi_pho', do_tin='cao', so_tang_uoc=3,
                                          cach_uoc_tang='tầng chuẩn mốc 1943: 3 (khoảng 2–5); toà con mang tầng riêng', dien_tich_m2=round(a))))
    st.update(so_khoi=kb, dien_tich_khoi_m2=round(barea), vung=[list(b0) for b0 in boxes])
    meta = dict(moc=1943, crs='EPSG:4326', nan=dict(bien_doi='affine', so_diem=z['n'], rms_m=round(z['rms'], 1), loo_rms_m=round(z['loo'], 1)),
                nguon={'pu-ams-m981-gibraltar-1943': 'U.S. Army Map Service, Spain 1:10,000 Gibraltar City Plan, A.M.S. M981, 1st ed. 1943 (copied from British Admiralty Chart 144 corr. 1942; revised from RAF aerial photographs). Bản quét Princeton chỉ dùng để nắn/đối chiếu (D8).',
                       'osm': 'OpenStreetMap, API /map đọc 17/10/2026'},
                giay_phep='AMS M981: tác phẩm chính phủ Mỹ (PD); bản quét Princeton chỉ làm bằng chứng/nắn (D8). Hình học toà N1943-w* lấy từ OpenStreetMap — ODbL 1.0 (licenses/osm-odbl-attribution.txt); dữ liệu dẫn xuất KHÔNG phát hành (phim = Produced Work).',
                ghi_cong='Building footprints © OpenStreetMap contributors (ODbL), filtered against U.S. Army Map Service M981 (1943). https://www.openstreetmap.org/copyright',
                thong_ke=st, tao_boi='channel-k2/k2c-t3-01/ghost/tools/ghost1943.py')
    json.dump(dict(type='FeatureCollection', name='ghost-1943', ghost=meta, features=feats), open(out, 'w'), ensure_ascii=False, separators=(',', ':'))
    print(json.dumps(st, ensure_ascii=False))
    # ảnh kiểm: (a) ghost 50 % lên AMS nắn; (b) lên OSM hôm nay (toà bỏ = xám, giữ = cam, chỉ AMS = đỏ)
    amsw = cv2.remap(src, q[:, 0].reshape(H, W), q[:, 1].reshape(H, W), cv2.INTER_LINEAR, borderValue=(255, 255, 255))
    osm = np.full((H, W, 3), 255, np.uint8); osm[occ > 0] = (200, 200, 200)
    for base, nm in ((amsw, '1943-tren-ban-do.jpg'), (osm, '1943-tren-osm.jpg')):
        lay = base.copy()
        for f in feats:
            if f['properties']['loai'] != 'nha': continue
            en = np.array(f['geometry']['coordinates'][0]); e, n_ = utm(en[:, 0], en[:, 1]); cv2.fillPoly(lay, [T(np.c_[e, n_])], (40, 40, 220) if '-a' in f['properties']['id'] else (40, 120, 240))
        o = cv2.addWeighted(lay, 0.5, base, 0.5, 0)
        for f in feats:
            if f['properties']['loai'] == 'khoi_pho':
                en = np.array(f['geometry']['coordinates'][0]); e, n_ = utm(en[:, 0], en[:, 1]); cv2.polylines(o, [T(np.c_[e, n_])], True, (150, 30, 120), 2)
        if 'osm' in nm: cv2.putText(o, 'Map data (c) OpenStreetMap contributors, ODbL', (10, H - 14), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (60, 60, 60), 2)
        o = cv2.resize(o, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        cv2.imwrite(os.path.join(kdir, nm), o, [cv2.IMWRITE_JPEG_QUALITY, 78])


if __name__ == '__main__':
    main(*sys.argv[1:])
