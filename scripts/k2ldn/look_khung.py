#!/opt/cine/bin/python
"""LOOK-T4 · khai 8 KHUNG LOOK (4 mốc × 2) × 3 BIẾN THỂ + 4 CLIP 8 s → channel-k2/k2c-t4-02/look/may/*.json (nguồn thật của máy/giờ/tham số look).
  look_khung.py
Cùng hình học/máy/giờ trong một hàng; biến thể chỉ đổi ánh sáng–màu–khí quyển–mật độ chi tiết (f.look) + LUT xuất (look_lut.py).
Điểm máy theo BANG-SHOT-v1 (P1 Bankside cao; P2 St Saviour's; P6 sông–cầu; P4 Fleet Street/Ludgate)."""
import json, os
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, 'channel-k2/k2c-t4-02/look/may'); os.makedirs(OUT, exist_ok=True)
LMT = -0.098 / 15                                   # giờ địa phương trung bình London (1666): UTC = LMT − kinh độ/15
P1 = dict(p=[532330, 180250, 230], l=[532420, 180980, 15], fov=50)
P2 = dict(p=[532690, 180290, 70], l=[532727, 180990, 20], fov=60)   # bắc: cầu (bắc) ở 1/3 phải, Old St Paul's 1/3 trái — góc Hollar Long View
P6 = dict(p=[533250, 180480, 35], l=[532300, 180850, 30], fov=45)
P4 = dict(p=[531300, 181160, 40], l=[532100, 181140, 60], fov=35)
# mốc: năm (thập phân), ngày giờ (lịch Gregory UTC qua tz) hoặc giờ cháy 1666 (kể từ 2/9 00:00 Julius) / 1940 (kể từ 29/12/1940 18:00)
KHUNG = {
 'M1-rong': dict(P1, year=1666.666, date=[1666, 9, 11, 15.5], tz=LMT, leaf=1, wind=[0.6, -0.8], vai='1666 trước cháy, ngày 1/9 (J.) chiều — toàn cảnh xương sống từ Bankside (chỗ Pepys)'),
 'M1-trung': dict(P2, year=1666.666, date=[1666, 9, 11, 16.0], tz=LMT, leaf=1, wind=[0.6, -0.8], vai='H1-03: góc Hollar từ tháp St Saviour — cầu London có nhà, bờ bắc, Old St Paul\'s'),
 'M2-ngay': dict(P1, year=1666.67, hour=39.0, smokeSky=0.55, leaf=1, wind=[-1.0, 0.12], vai='3/9/1666 15:00 — ngày khói: cột khói theo gió đông, Cheapside/Cornhill cháy'),
 'M2-dem': dict(P6, year=1666.67, hour=23.0, leaf=1, wind=[-1.0, 0.12], moon=0.25, vai='2/9/1666 23:00 — đêm lửa từ giữa sông: bờ bắc cháy quanh cầu, phản chiếu sông'),
 'M3-rong': dict(P1, year=1940.99, h40=3.5, date=[1940, 12, 29, 21.5], tz=0, leaf=0, wind=[0.3, -1.0], vai='29/12/1940 21:30 — mưa bom cháy, nhiều đám cháy quanh St Paul\'s (ranh ƯỚC LƯỢNG, D15)'),
 'M3-trung': dict(P4, year=1940.99, h40=4.5, date=[1940, 12, 29, 22.5], tz=0, leaf=0, wind=[0.3, -1.0], vai='H4-04: mái vòm giữa khói lửa từ Fleet Street/Ludgate, 22:30 (dựng 3D, không ảnh Mason)'),
 'M4-rong': dict(P1, year=2026.67, date=[2026, 9, 2, 15.0], tz=1, leaf=1, wind=[0.7, 0.7], vai='2026 ngày — chân trời City: St Paul\'s + cụm tháp phía đông'),
 'M4-trung': dict(P4, year=2026.67, date=[2026, 9, 2, 16.5], tz=1, leaf=1, wind=[0.7, 0.7], vai='H5-05: từ Fleet Street — Leadenhall vát, mái vòm còn nền trời (tầm nhìn bảo vệ)'),
}
# BIẾN THỂ (3D thuần; chỉ ánh sáng–màu–khí quyển–mật độ chi tiết). A theo LOOK-1 T3 (sương σ = 1/16 km, màu chân trời [0,66 0,74 0,84], LUT kênh v0,30).
LOOK = {
 'A': dict(ten='T3 kênh', haze=[1 / 16000, 0.66, 0.74, 0.84], hazeH=700, coal=[0, 0.5, 0.46, 0.40, 70], sunK=3.0, hemiK=0.62, sunTint=[1, 1, 1], skyTop=[0.20, 0.38, 0.74], skyHor=[0.62, 0.72, 0.86],
           cloud=0.32, cloudCol=[1.0, 0.99, 0.96], water=[0.040, 0.050, 0.042], texK=1.0, chim=0.30, smokeK=0.85, smokeTint=[1, 1, 1], exposure=0.95, lut='k2c-t3-kenh-v030.cube'),
 'B': dict(ten='London sương', haze=[1 / 6000, 0.60, 0.63, 0.66], hazeH=420, coal=[1 / 4200, 0.46, 0.43, 0.39, 90], sunK=2.1, hemiK=0.78, sunTint=[0.96, 0.97, 1.02], skyTop=[0.42, 0.48, 0.58], skyHor=[0.66, 0.68, 0.70],
           cloud=0.78, cloudCol=[0.86, 0.87, 0.89], water=[0.036, 0.042, 0.040], texK=0.9, chim=0.85, smokeK=1.25, smokeTint=[0.92, 0.92, 0.95], exposure=1.0, lut='look-B-lanh.cube'),
 'C': dict(ten='tranh khắc ấm', haze=[1 / 10500, 0.84, 0.76, 0.62], hazeH=520, coal=[0, 0.5, 0.46, 0.40, 70], sunK=2.6, hemiK=0.72, sunTint=[1.06, 0.97, 0.84], skyTop=[0.40, 0.50, 0.64], skyHor=[0.88, 0.80, 0.66],
           cloud=0.50, cloudCol=[1.0, 0.94, 0.84], water=[0.046, 0.046, 0.036], texK=0.85, chim=0.45, smokeK=1.0, smokeTint=[1.04, 0.98, 0.90], exposure=0.95, lut='look-C-am.cube'),
}
# 2026: không khói than (Clean Air Act 1956) → B giữ sương lạnh, bỏ lớp than (bậc 1 cho luật; mức sương bậc 5)
def look_for(v, k):
    L = dict(LOOK[v])
    if k.startswith('M4'): L['coal'] = [0, 0.5, 0.46, 0.40, 70]; L['chim'] = 0
    if k.startswith('M3') and v == 'B': L['coal'] = [1 / 6000, 0.40, 0.38, 0.36, 120]      # 1940: khói than + khói cháy (ước lượng)
    return L
HERO = {'M1-rong': [532118, 181150, 40], 'M1-trung': [532118, 181150, 40], 'M2-ngay': [532118, 181150, 40], 'M2-dem': [532870, 180505, 15],
        'M3-rong': [532102, 181122, 70], 'M3-trung': [532102, 181122, 70], 'M4-rong': [532102, 181122, 70], 'M4-trung': [532102, 181122, 70]}
def main():
    rows = {}
    for k, K in KHUNG.items():
        key = {kk: vv for kk, vv in K.items() if kk != 'vai'}; key['t'] = 0
        for v in LOOK:
            sh = {'fps': 24, 'dur': 0.0417, 'W': 1920, 'H': 1080, 'spp': 24, 'look': look_for(v, k), 'keys': [key], 'hero_EN': HERO[k], 'vai': K['vai'], 'bien_the': v,
                  'bake': {'url': '/data/look/bake_%s.png' % {'M1': '1666.6', 'M2': '1666.6', 'M3': '1940.98', 'M4': '2026.7'}[k[:2]], 'box': [530800, 179700, 534000, 182000]}}
            json.dump(sh, open(os.path.join(OUT, f'{k}-{v}.json'), 'w'), ensure_ascii=False, indent=1)
        rows[k] = K['vai']
    # CLIP 8 s (biến thể A, 640×360): cú máy theo §19 đề xuất (vòng cung ≤ 3°/s, đẩy vào tiêu điểm ≤ 1,5 %/s), thời gian chạy trong khung
    import math
    def arc(P, deg, n=5):
        cx, cy = P['l'][0], P['l'][1]; dx, dy = P['p'][0] - cx, P['p'][1] - cy; r = math.hypot(dx, dy); a0 = math.atan2(dy, dx); out = []
        for i in range(n):
            a = a0 + math.radians(-deg / 2 + deg * i / (n - 1)); out.append([cx + r * math.cos(a), cy + r * math.sin(a), P['p'][2]])
        return out
    def push(P, frac, n=5):
        return [[P['p'][j] + (P['l'][j] - P['p'][j]) * frac * i / (n - 1) for j in range(3)] for i in range(n)]
    CLIP = {
     'M1': dict(base='M1-rong', pts=arc(P1, 18.0), date0=[1666, 9, 11, 15.0], date1=[1666, 9, 11, 16.5], cu='VÒNG CUNG 18° / 8 s = 2,25°/s quanh City; thời gian chạy 15:00 → 16:30'),
     'M2': dict(base='M2-ngay', pts=push(P1, 0.16), hour=[36.0, 42.0], cu='ĐẨY VÀO 16 % quãng tới tiêu điểm / 8 s; giờ cháy 3/9 12:00 → 18:00 (khói lớn dần)'),
     'M3': dict(base='M3-rong', pts=push(P1, 0.14), h40=[2.0, 5.0], cu='ĐẨY VÀO chậm; 29/12/1940 20:00 → 23:00 (đám cháy lan)'),
     'M4': dict(base='M4-rong', pts=arc(P1, 16.0), date0=[2026, 9, 2, 14.0], date1=[2026, 9, 2, 19.5], cu='VÒNG CUNG 16° / 8 s = 2°/s; 14:00 → 19:30 (chiều → hoàng hôn, cửa sổ sáng dần)'),
    }
    for m, C in CLIP.items():
        K = dict(KHUNG[C['base']]); K.pop('vai'); keys = []
        for i, p in enumerate(C['pts']):
            u = i / (len(C['pts']) - 1); k = dict(K); k['t'] = 8.0 * u; k['p'] = p
            if 'date0' in C: k['date'] = [a + (b - a) * u for a, b in zip(C['date0'], C['date1'])]
            if 'hour' in C: k['hour'] = C['hour'][0] + (C['hour'][1] - C['hour'][0]) * u
            if 'h40' in C: k['h40'] = C['h40'][0] + (C['h40'][1] - C['h40'][0]) * u
            keys.append(k)
        sh = {'fps': 24, 'dur': 8.0, 'W': 640, 'H': 360, 'spp': 4, 'smooth': True, 'easeKeys': False, 'look': look_for('A', C['base']), 'keys': keys, 'hero_EN': HERO[C['base']], 'cu_may': C['cu'],
              'bake': {'url': '/data/look/bake_%s.png' % {'M1': '1666.6', 'M2': '1666.6', 'M3': '1940.98', 'M4': '2026.7'}[m], 'box': [530800, 179700, 534000, 182000]}}
        json.dump(sh, open(os.path.join(OUT, f'clip-{m}.json'), 'w'), ensure_ascii=False, indent=1)
    json.dump({'khung': rows, 'bien_the': {v: LOOK[v]['ten'] for v in LOOK}}, open(os.path.join(OUT, 'muc-luc.json'), 'w'), ensure_ascii=False, indent=1)
    print(len(KHUNG) * len(LOOK), 'khung +', len(CLIP), 'clip')
if __name__ == '__main__': main()
