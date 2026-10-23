#!/opt/cine/bin/python
"""LOOK-T4 · tải vân Poly Haven (CC0) cho look London → $LDN_DATA/tex/<id>_{diff,nor}_1k.jpg (ngoài git) + sổ SHA/giấy phép trong git:
  channel-k2/k2c-t4-02/look/van-cc0.json (id, lớp dùng, cỡ thật m theo API, URL, SHA-256, giấy phép CC0 theo api.polyhaven.com/info).
  tai_van.py"""
import hashlib, json, os, time, urllib.request
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(os.environ.get('LDN_DATA', '/var/tmp/ldn'), 'tex'); os.makedirs(OUT, exist_ok=True)
UA = 'CineLab-research (+https://github.com/HungQuach301/cine-lab)'
def get(u): return urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA}), timeout=120).read()
LAYERS = [  # (id, vai)
 ('plastered_wall_02', 'tường trát nhà khung gỗ 1666'), ('medieval_wood', 'khung gỗ, cửa hàng, cầu tàu'), ('brick_wall_02', 'gạch đỏ nhà 1667+'),
 ('clay_roof_tiles_02', 'ngói đất nung 1666–1700'), ('roof_slates_02', 'mái đá phiến thế kỷ 19–20'), ('old_stone_wall', 'đá thô Trung cổ (nhà thờ, tường thành, Tower)'),
 ('white_sandstone_bricks', 'đá Portland ghép khối (Wren, Monument)'), ('concrete_wall_008', 'bê tông/đá toà 2026'), ('metal_plate', 'mái chì/kim loại'),
 ('cobblestone_floor_01', 'phố lát sỏi/đá 1666–1900'), ('brown_mud_02', 'bùn bãi sông, sân đất'), ('aerial_asphalt_01', 'đường nhựa 2026 (nhìn trên cao)'),
 ('granite_tile', 'vỉa hè + tường Embankment'), ('leafy_grass', 'cỏ, vườn'), ('old_planks_02', 'sàn cầu tàu gỗ'), ('brick_wall_006', 'gạch London (Victoria)')]
rec = []
for aid, vai in LAYERS:
    info = json.loads(get(f'https://api.polyhaven.com/info/{aid}')); F = json.loads(get(f'https://api.polyhaven.com/files/{aid}'))
    row = {'id': aid, 'vai': vai, 'trang': f'https://polyhaven.com/a/{aid}', 'giay_phep': 'CC0 1.0 (Poly Haven: "All assets are CC0")',
           'co_that_m': info.get('dimensions'), 'tac_gia': list((info.get('authors') or {}).keys()), 'tep': []}
    for kind, key in (('diff', 'Diffuse'), ('nor', 'nor_gl')):
        u = F[key]['1k']['jpg']['url']; p = os.path.join(OUT, f'{aid}_{kind}_1k.jpg')
        if not os.path.exists(p): open(p, 'wb').write(get(u)); time.sleep(0.5)
        row['tep'].append({'url': u, 'tep': os.path.basename(p), 'sha256': hashlib.sha256(open(p, 'rb').read()).hexdigest()})
    rec.append(row); print('OK', aid, row['co_that_m'], flush=True)
json.dump({'ngay_tai': time.strftime('%Y-%m-%d'), 'nguon': 'api.polyhaven.com', 'lop': rec}, open(os.path.join(REPO, 'channel-k2/k2c-t4-02/look/van-cc0.json'), 'w'), ensure_ascii=False, indent=1)
