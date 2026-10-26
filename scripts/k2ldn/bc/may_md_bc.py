#!/opt/cine/bin/python
"""BAN-CUOI-T4-A · máy ẢNH ĐẦU M-d (việc 4): render 3D CÙNG NĂM tại chỗ sự kiện (tầm người/thuyền, khung trung/xa) → OpenAI chỉnh (oai_bc.py) → Omni.
Look/bake mượn từ máy animatic v3 cùng thời kỳ (đọc, không sửa). Ra channel-k2/k2c-t4-02/ban-cuoi/may/md-*.json + viec-md.json (1920×1080 look3 cờ d; bản xem nhanh 640).
  may_md_bc.py"""
import copy, json, os
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
A2 = os.path.join(REPO, 'channel-k2/k2c-t4-02/animatic2/may'); OUT = os.path.join(REPO, 'channel-k2/k2c-t4-02/ban-cuoi/may'); REL = 'channel-k2/k2c-t4-02/ban-cuoi/may/'
ld = lambda n: json.load(open(os.path.join(A2, n + '.json')))
#   mã: (máy v3 mượn look/bake, p [E,N,h], l [E,N,h], fov, ghi đè khoá thời gian, vai)
M = {
 'H1-06x': ('H1-06', [532330, 180655, 4], [532760, 180760, 12], 40, {'hour': 14.0}, 'sà lan hoàng gia trên Thames chiều 2/9/1666: bờ bắc cháy (Three Cranes → cầu)'),
 'H1-15x': ('H1-15', [531540, 181171, 17], [531900, 181140, 28], 42, {'hour': 63.0}, 'Fleet Street 4/9/1666 chiều: tuyến chữa cháy, lửa và Old St Paul\'s phía đông'),
 'H2-02b': ('H2-00', [531420, 181080, 30], [532100, 181150, 18], 40, {}, 'tầm nhìn qua cửa sổ phía tây: City cháy trụi 9/1666 (nền cửa sổ cho bàn bản vẽ)'),
 'H2-06b': ('H2-06', [532880, 180690, 9], [532935, 180800, 45], 44, {'year': 1675.3, 'date': [1675, 9, 1, 15.0]}, 'chân Monument đang xây 1675 (Fish Street Hill), nhìn bắc — không thấy St Paul\'s'),
 'H2-09x': ('H2-09', [531965, 181136, 21], [532110, 181148, 24], 44, {'year': 1675.45, 'date': [1675, 9, 1, 15.0]}, 'Ludgate Hill 1675: nền nhà thờ mới, tàn tích Old St Paul\'s dọn dần'),
 'H2-10b': ('H2-10', [532165, 181110, 138], [532300, 180800, 0], 50, {'year': 1708.8, 'date': [1708, 10, 1, 14.0]}, 'đỉnh đèn lồng 1708 nhìn xuống City + sông + cầu London cũ (đông nam)'),
 'H5-02b': ('H5-02', [532300, 181558, 30], [532300, 181870, 75], 50, {'year': 1973.0, 'date': [1973, 9, 1, 14.0]}, 'tháp Barbican đang xây (1973) nhìn bắc từ London Wall'),
 'H5-02s': ('H5-02s', [532180, 181556, 16], [532600, 181566, 19], 45, {}, 'London Wall 1976 tầm người'),
 'H5-04c': ('H5-04', [533350, 181124, 16], [533150, 181220, 150], 55, {'year': 2026.667, 'date': [2026, 9, 2, 14.0]}, 'cụm toà cao Leadenhall/Bishopsgate từ phố (ngửa)'),
 'H5-05d': ('H5-05a', [531450, 180520, 8], [532118, 181150, 90], 30, {}, 'tầm nhìn bảo vệ tới mái vòm từ bờ nam / Waterloo (ven sông)'),
 'H5-05b': ('H5-05b', [531300, 181160, 15], [532118, 181150, 95], 32, {}, 'Fleet Street 2026 tầm người nhìn đông lên mái vòm, nền trời'),
}
V = []
for ma, (base, p, l, fov, gd, vai) in M.items():
    sh = ld(base); k = copy.deepcopy(sh['keys'][0]); k.update(t=0.0, p=p, l=l, fov=fov)
    for a, b in gd.items():
        if b is None: k.pop(a, None)
        else: k[a] = b
    sh['keys'] = [k]; sh['dur'] = 1 / 24; sh['W'], sh['H'] = 1920, 1080; sh['vai_md'] = vai; sh['nguon_may'] = f'animatic2/may/{base}.json (look/bake)'
    if base in ('H5-02s', 'H5-05b'): sh['page'] = 'look2'
    json.dump(sh, open(os.path.join(OUT, f'md-{ma}.json'), 'w'), ensure_ascii=False, indent=1)
    V.append(dict(ten=f'md-{ma}-xem', shot=REL + f'md-{ma}.json', lk='look3d/', key={'d': True}, w=640, h=360, png=1, spp=8))
    V.append(dict(ten=f'md-{ma}', shot=REL + f'md-{ma}.json', lk='look3d/', key={'d': True}, png=1, spp=24))
json.dump(V, open(os.path.join(OUT, 'viec-md.json'), 'w'), ensure_ascii=False, indent=1); print(len(V))
