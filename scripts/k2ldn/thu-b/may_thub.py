#!/opt/cine/bin/python
"""THU-B-T4 · khai máy/giờ cho vòng thử → channel-k2/k2c-t4-02/thu-b/may/*.json (đọc lại đúng tham số V2 trong look/may-v2/, §19 (a) luật 3; KHÔNG sửa tệp V2).
  may_thub.py
Khung (B): M1-trung (1666, tháp St Saviour), M4-trung (2026, Fleet St), B3-p4-1938 (H3-05 BANG-SHOT-v1: P4 Fleet St/Ludgate 40 m, 1937–1938, ngày — lý do ở báo cáo §1).
Khung (D): M1-rong-hep, M4-rong-hep (P1 fov 36°, LOOK-T4-4).
Timelapse nắng đổi 3 s 640×360 spp 4, máy CODINH, khung 0 = đúng giờ khung V2, chạy tới +2 h (bóng quét rõ): tl-<khung>.json. 1666: thêm bản không khói bếp (ảnh vào AI; khói bếp = lớp sống)."""
import json, os, copy
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
V2 = os.path.join(REPO, 'channel-k2/k2c-t4-02/look/may-v2'); OUT = os.path.join(REPO, 'channel-k2/k2c-t4-02/thu-b/may'); os.makedirs(OUT, exist_ok=True)
ld = lambda k: json.load(open(os.path.join(V2, k + '.json')))
def dump(k, d): json.dump(d, open(os.path.join(OUT, k + '.json'), 'w'), ensure_ascii=False, indent=1)

def tl(sh, h_cong=2.0, dur=3.0):
    """timelapse CODINH: khung 0 = giờ của khung tĩnh; khung cuối = +h_cong giờ; 640×360 spp 4"""
    t = copy.deepcopy(sh); k0 = copy.deepcopy(sh['keys'][0]); k0['t'] = 0.0; k1 = copy.deepcopy(k0); k1['t'] = dur
    k1['date'] = list(k0['date']); k1['date'][3] = round(k0['date'][3] + h_cong, 4)
    t.update(dur=dur, W=640, H=360, spp=4, shadow=3072, easeKeys=False, keys=[k0, k1], cu_may='CODINH (máy cố định, thời gian chạy — nắng đổi)'); return t

n = 0
for k in ('M1-trung', 'M4-trung', 'M1-rong-hep', 'M4-rong-hep'):
    sh = ld(k); sh['nguon_may'] = f'look/may-v2/{k}.json'; dump(k, sh); n += 1
    t = tl(sh); dump('tl-' + k, t); n += 1
    if k.startswith('M1'):
        s2 = copy.deepcopy(sh); s2['keys'][0]['chim'] = False; s2['vai'] = k + ' KHÔNG khói bếp (ảnh vào AI; khói bếp = lớp sống, ghép cộng hiệu)'; dump(k + '-khongkhoi', s2); n += 1
        t2 = copy.deepcopy(t); [kk.__setitem__('chim', False) for kk in t2['keys']]; dump('tl-' + k + '-khongkhoi', t2); n += 1
# B3: H3-05 (BANG-SHOT-v1) — P4 FLEET-STREET/LUDGATE [531300, 181160, 40] → [532100, 181140, 60], FOV dọc 35°; 1938 (cuối mốc 1937–1938), 2/9 15:00 BST; look A V2 (như M4: sương 1/10 km, toy 1)
sh = ld('M4-trung'); sh['keys'][0].update(p=[531300, 181160, 40], l=[532100, 181140, 60], fov=35, year=1938.67, date=[1938, 9, 2, 15.0], tz=1)
sh['hero_EN'] = [532100, 181140, 60]; sh['vai'] = 'B3 = H3-05 (BANG-SHOT-v1): P4 Fleet St/Ludgate 40 m, 1938 ngày — mái vòm + phố Ludgate Hill (khối Victoria–Edward ước lượng)'
sh['bake'] = {'url': '/data/look2/bake_1938.7.png', 'box': [530800, 179700, 534000, 182000]}; sh['nguon_may'] = 'BANG-SHOT-v1 H3-05 (P4) + look/may-v2/M4-trung.json (look A V2)'
dump('B3-p4-1938', sh); n += 1; dump('tl-B3-p4-1938', tl(sh)); n += 1
print(n, 'tệp máy →', OUT)
