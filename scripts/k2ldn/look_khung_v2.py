#!/opt/cine/bin/python
"""LOOK-T4-V2 · khai máy/giờ/tham số cho tờ so V2 → channel-k2/k2c-t4-02/look/may-v2/*.json.
  look_khung_v2.py
Cùng điểm máy + giờ với 8 hàng LOOK-T4 (look_khung.py: KHUNG, HERO — đọc lại đúng tham số, §19 (a) luật 3). Look hợp nhất (chủ dự án 23/10/2026 23:27):
biến thể A làm chuẩn; cháy ngày 1666 (M2-ngay) và toàn cảnh 1940 (M3-*) ấm kiểu C; đêm cháy 1666 (M2-dem) sương/khói than dày kiểu B.
Nâng V2 (chống 'đồ chơi', ghi trong báo cáo): sương phối cảnh khí quyển σ 1/16 km → 1/10 km (ban ngày) — chiều sâu không khí giữa máy và City; toy = 1 (mái/tường phong hoá trong look2.js).
Thêm: hàng đo công trình P1 (mặt nạ mã công trình) và hai hàng đề xuất 'P1 ống hẹp' (fov 36°, cùng vị trí/hướng) để đo ngưỡng px."""
import json, os, copy
import look_khung as K0
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, 'channel-k2/k2c-t4-02/look/may-v2'); os.makedirs(OUT, exist_ok=True)
BAKE = {'M1': '1666.6', 'M2': '1666.6', 'M3': '1940.98', 'M4': '2026.7'}
A, B, C = K0.LOOK['A'], K0.LOOK['B'], K0.LOOK['C']


def look_v2(k):
    L = K0.look_for('A', k); L['ten'] = 'V2 (A + điều chỉnh theo mốc)'; L['toy'] = 1
    L['haze'] = [1 / 10000] + L['haze'][1:]
    if k in ('M2-ngay',) or k.startswith('M3'):                    # ấm kiểu C (ánh sáng, trời, sương) — LUT kênh A giữ nguyên
        for f in ('sunTint', 'skyTop', 'skyHor', 'cloudCol'): L[f] = list(C[f])
        L['haze'] = [1 / 10000] + list(C['haze'][1:]); L['hazeH'] = C['hazeH']; L['water'] = list(C['water']); L['smokeTint'] = list(C['smokeTint'])
    if k == 'M2-dem':                                              # sương + lớp khói than dày kiểu B
        L['haze'] = list(B['haze']); L['hazeH'] = B['hazeH']; L['coal'] = list(B['coal']); L['smokeK'] = B['smokeK']; L['chim'] = B['chim']
    return L


def shot(k, key, extra=None):
    sh = {'fps': 24, 'dur': 0.0417, 'W': 1920, 'H': 1080, 'spp': 24, 'look': look_v2(k), 'keys': [key], 'hero_EN': K0.HERO[k], 'vai': K0.KHUNG[k]['vai'],
          'bake': {'url': '/data/look2/bake_%s.png' % BAKE[k[:2]], 'box': [530800, 179700, 534000, 182000]}}
    if extra: sh.update(extra)
    return sh


def main():
    n = 0
    for k, Kd in K0.KHUNG.items():
        key = {kk: vv for kk, vv in Kd.items() if kk != 'vai'}; key['t'] = 0
        json.dump(shot(k, key), open(os.path.join(OUT, f'{k}.json'), 'w'), ensure_ascii=False, indent=1); n += 1
        if k in ('M1-rong', 'M4-rong', 'M3-rong'):                 # đề xuất P1 ống hẹp (cùng vị trí + điểm nhìn, fov 36°)
            k2 = dict(key); k2['fov'] = 36
            json.dump(shot(k, k2, {'de_xuat': 'P1 ống hẹp fov 36° (cùng vị trí/hướng)'}), open(os.path.join(OUT, f'{k}-hep.json'), 'w'), ensure_ascii=False, indent=1); n += 1
    print(n, 'tệp máy V2 →', OUT)


if __name__ == '__main__': main()
