#!/opt/cine/bin/python
"""BAN-CUOI-T4-A · tệp máy cho phần thử (ghi vào channel-k2/k2c-t4-02/ban-cuoi/may/*.json) + danh sách việc dựng (ban-cuoi/may/viec-*.json) cho dung_bc.py.
Nguồn: máy animatic v3 (channel-k2/k2c-t4-02/animatic2/may/*.json — đọc, không sửa); P1 hiện tại = LOOK-T4-4 + C6 xoay 4° (đọc lại từ M01/M03…, §19 (a) luật 3).
  may_bc.py      (tất định)"""
import copy, json, os
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
A2 = os.path.join(REPO, 'channel-k2/k2c-t4-02/animatic2/may'); OUT = os.path.join(REPO, 'channel-k2/k2c-t4-02/ban-cuoi/may'); os.makedirs(OUT, exist_ok=True)
REL = 'channel-k2/k2c-t4-02/ban-cuoi/may/'
ld = lambda n: json.load(open(os.path.join(A2, n + '.json')))
V = {}


def ghi(ten, sh): json.dump(sh, open(os.path.join(OUT, ten + '.json'), 'w'), ensure_ascii=False, indent=1); return REL + ten + '.json'


def tinh(base, ki=0, ten=None, dur=1 / 24, **ghide):
    """khung tĩnh: lấy khoá ki của tệp máy v3, 1 khung"""
    sh = ld(base); k = copy.deepcopy(sh['keys'][ki if ki >= 0 else len(sh['keys']) + ki]); k['t'] = 0.0; k.update(ghide)
    sh['keys'] = [k]; sh['dur'] = dur; sh['W'], sh['H'] = 1920, 1080; sh['nguon_may'] = f'animatic2/may/{base}.json khoá {ki}'
    return sh


def viec(nhom, ten, shot, **kw): V.setdefault(nhom, []).append(dict(ten=ten, shot=shot, **kw))


def mat_na(nhom, ten, p):
    viec(nhom, ten + '-m1', p, lk='look3d/', mask=1)              # lớp: nha_thuong 215 / nha 235 / nước / trời …
    viec(nhom, ten + '-m2', p, lk='look3d/', mask=2)              # mã công trình mốc (mái vòm St Paul's …)
    viec(nhom, ten + '-m3e', p, lk='look3e/', mask=3)             # mã toà OSM có tên (hinh_hoc_e.py)


D = {'d': True}
# ---- việc 1: E (2026, CODINH) — render ngày/đêm + mặt nạ, 1080p
for ten, base, ki in (('E-P9-ngay', 'H5-05a', 0), ('E-P9-dem', 'H5-07a', 0), ('E-P1-ngay', 'H5-04', -1)):
    p = ghi(ten, tinh(base, ki)); viec('e', ten, p, lk='look3d/', key=D, png=1, spp=24); mat_na('e', ten, p)
# video N2P-5: 3 s 640×360 máy CODINH (H5-05a khoá 0 → 0,1 h nắng; H5-07a khoá 0 cố định máy)
for ten, base in (('E-P9-ngay-tl', 'H5-05a'), ('E-P9-dem-tl', 'H5-07a')):
    sh = ld(base); k0 = copy.deepcopy(sh['keys'][0]); k1 = copy.deepcopy(k0); k1['t'] = 3.0
    if 'date' in k1: k1['date'] = k1['date'][:3] + [k1['date'][3] + 0.05]
    sh['keys'] = [k0, k1]; sh['dur'] = 3.0; sh['W'], sh['H'] = 640, 360; sh['cu_may'] = 'CODINH'
    p = ghi(ten, sh); viec('etl', ten, p, lk='look3d/', key=D, png=1, w=640, h=360); viec('etl', ten + '-m1', p, lk='look3d/', mask=1, w=640, h=360, only=[0])

# ---- việc 2: điểm đứng P1 — hiện tại / tây 60 m / tây 80 m (dời cả điểm nhìn: giữ hướng nhìn và fov 36°)
for ten, base, ki in (('P1-M03', 'M03', 0), ('P1-H4-05', 'H4-05', 0), ('P1-M01', 'M01', 0)):
    for dx in (0, 60, 80):
        sh = tinh(base, ki); k = sh['keys'][0]; k['p'][0] -= dx; k['l'][0] -= dx; sh['p1_doi_tay_m'] = dx
        p = ghi(f'{ten}-w{dx}', sh); viec('p1', f'{ten}-w{dx}', p, lk='look3d/', key=D, png=1, spp=16)
        viec('p1', f'{ten}-w{dx}-m2', p, lk='look3d/', mask=2)

# ---- việc 3: mẫu 1080p bản cuối (D: look3 cờ d) — 12 khung liên tiếp quanh giữa shot, spp sản xuất 4 (đo giờ/khung)
for base in ('M01', 'H1-08b', 'H2-10', 'H3-05', 'H4-04a', 'H5-08'):
    sh = ld(base); sh['W'], sh['H'] = 1920, 1080; p = ghi('mau-' + base, sh); n = round(sh['dur'] * 24); a = n // 2 - 6
    viec('mau', 'mau-' + base, p, lk='look3d/', key=D, png=1, spp=4, only=list(range(a, a + 12)))
# B (BE-MAT-NHA, máy cố định): H5-06 (P3 2026) và H2-12-b (P2 1711) — khung 0, render + mặt nạ + bóng + mã nhà/mặt phẳng
for ten, base in (('B-H5-06', 'H5-06'), ('B-H2-12b', 'H2-12-b')):
    p = ghi(ten, tinh(base, 0)); viec('b', ten, p, lk='look3d/', key=D, png=1, spp=24)
    for mk in (1, 3, 4, 6): viec('b', f'{ten}-m{mk}', p, lk='look3d/', mask=mk)
    viec('b', ten + '-bong', p, lk='look3d/', key={'d': True, 'bong': True, 'chim': False}, png=1, spp=24)
    viec('b', ten + '-v2', p, page='look2', lk='look2/', png=1, spp=24)

for nhom, L in V.items(): json.dump(L, open(os.path.join(OUT, f'viec-{nhom}.json'), 'w'), ensure_ascii=False, indent=1)
print({k: len(v) for k, v in V.items()})
