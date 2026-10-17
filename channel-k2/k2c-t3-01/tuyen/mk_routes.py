"""T3 · gói TUYẾN · dựng tuyen/routes.geojson + kiểm "tuyến biển không cắt đất" (Natural Earth 1:10m land + minor islands, đệm 5 km quanh cảng).
- Điểm mốc (waypoint) mang claim id; toạ độ lấy từ gazetteer (OSM Nominatim, lưu thô ngoài git, SHA trong gazetteer.json) + độ dời ra khơi ghi rõ.
- Điểm điều khiển (`dieu_khien: true`) KHÔNG phải sự kiện có nguồn: chỉ giữ nét spline trên biển; đoạn giữa hai điểm có claim luôn `approx: true`.
- Tuyến thiếu claim cảng đi → bắt đầu từ mép khung (`vao_tu_mep: true`), nhãn "from England" (hoặc không nhãn nơi đi).
Dùng: /opt/cine/bin/python -I channel-k2/k2c-t3-01/tuyen/mk_routes.py  → routes.geojson, gazetteer.json, kiem-dat.json (in bảng số đo)"""
import hashlib, json, math, sys
from pathlib import Path

import shapefile
from pyproj import Transformer
from shapely.geometry import LineString, Point, Polygon, box, mapping, shape
from shapely.ops import transform, unary_union

HERE = Path(__file__).resolve().parent
RAW = Path('/var/tmp/cine-out/tuyen')
NE = [RAW / 'ne/land/ne_10m_land.shp', RAW / 'ne/minor/ne_10m_minor_islands.shp']
NE_ZIP = {'ne_10m_land.zip': 'e547d749445eaa0964aba76738090ec88f5e63c4585122170f98c67a7ea922dc',
          'ne_10m_minor_islands.zip': '47c0b3ce26df7b4dbabdbb251023918cb2f5c83462a426288f1f253da7284db2'}
BUF_CANG_KM = 5.0
FWD = Transformer.from_crs('EPSG:4326', 'EPSG:3035', always_xy=True).transform   # LAEA châu Âu, mét
INV = Transformer.from_crs('EPSG:3035', 'EPSG:4326', always_xy=True).transform

# Gazetteer: khoá → (khoá tệp thô Nominatim, độ dời ra khơi (dlat, dlon) hoặc None, ghi chú)
GZ = {
 'st_helens':   ('st_helens_iow', None, 'làng St Helens (Isle of Wight); neo "St Helen\'s Roads" ngoài khơi ≤ 3 km → coi là cảng (đệm 5 km)'),
 'spithead':    ('spithead', None, 'Spithead (locality trên mặt nước)'),
 'lisbon':      ('lisbon', None, 'Lisboa (cảng sông Tagus)'),
 'off_lagos':   ('lagos_pt', (-0.075, 0.0), 'ngoài khơi Lagos: dời 8,3 km về nam'),
 'off_tetuan':  ('martil', (0.025, 0.055), 'ngoài khơi Martil (cảng của Tétouan): dời ≈ 5,7 km về đông bắc'),
 'gib_bay':     ('bay_gibraltar', None, 'Bahía de Algeciras / Bay of Gibraltar (natural/bay)'),
 'algeciras_anch': ('algeciras', (0.004, 0.027), 'neo "between the Orange Grove and Algeziras": dời 2,4 km về đông từ tâm Algeciras (ra mặt vịnh)'),
 'strait_west': (None, None, 'cửa tây eo biển = trung điểm Tarifa–Cap Spartel (tính)'),
 'off_st_vincent': ('cape_st_vincent', (-0.05, -0.05), 'ngoài khơi mũi St Vincent: dời ≈ 7 km về tây nam'),
 'off_cork':    ('cobh', (-0.09, 0.045), 'ngoài cửa cảng Cork: dời ≈ 10 km về nam–đông nam từ Cobh'),
 'off_spartel': ('cap_spartel', (0.03, -0.075), 'ngoài khơi Cap Spartel: dời ≈ 7,5 km về tây bắc'),
 'off_fuengirola': ('fuengirola', (-0.06, 0.07), 'ngoài khơi Fuengirola: dời ≈ 9 km về đông nam'),
 'casablanca':  ('casablanca', None, 'Casablanca (cảng)'),
 'mohammedia':  ('mohammedia', None, 'Mohammédia = Fedala 1942 (cảng)'),
 'oran':        ('oran', None, 'Oran (cảng)'),
 'algiers':     ('algiers', None, 'Alger (cảng)'),
 'tafraoui':    ('tafraoui', None, 'Tafraoui — sân bay Tafaraoui 1942 (điểm đến đường không)'),
 'funchal':     ('funchal', None, 'Funchal, Madeira (cảng)'),
 'gibraltar':   ('gibraltar', None, 'Gibraltar (cảng; điểm trên đất liền, trong đệm cảng)'),
 'thames':      (None, None, 'cửa Thames (điểm cuối biểu trưng cho "London"; tính: 51.48 N, 0.90 E — không phải sự kiện có nguồn)'),
}
# Điểm điều khiển (chỉ giữ nét trên biển; KHÔNG có nguồn sự kiện)
CTL = {
 'c_channel_w': (49.95, -2.2), 'c_ushant': (48.55, -5.9), 'c_finisterre': (43.0, -10.2), 'c_roca': (38.75, -9.75), 'c_porto_off': (41.2, -9.7),
 'c_lizard': (49.8, -5.3), 'c_scilly_s': (49.6, -6.6), 'c_biscay': (46.0, -9.0), 'c_ireland_s': (51.2, -8.0), 'c_gulf_cadiz': (36.65, -7.2),
 'c_strait_mid': (35.95, -5.60), 'c_europa_s': (36.03, -5.30), 'c_alboran_w': (36.25, -4.95), 'c_trafalgar_off': (36.12, -6.15),
 'c_madeira_n': (34.5, -13.0), 'c_dover': (51.0, 1.45), 'c_alboran_e': (36.1, -2.5), 'c_oran_off': (35.85, -0.75),
 'c_algiers_off': (36.97, 2.80), 'c_algiers_bay': (36.82, 3.13), 'c_off_rabat': (34.3, -7.3),
 'c_wight_e': (50.655, -0.94), 'c_wight_s': (50.42, -1.3), 'c_tagus': (38.665, -9.30), 'c_strait_w': (35.90, -5.85), 'c_strait_e': (35.99, -5.42),
 'c_ceuta_n': (35.955, -5.27), 'c_ceuta_e': (35.86, -5.17), 'c_bay_mouth': (36.06, -5.38), 'c_foreland': (51.42, 1.62), 'c_thames_mouth': (51.52, 1.15),
 'c_madeira_e': (32.665, -16.62), 'c_funchal_off': (32.60, -16.86), 'c_fedala_off': (33.82, -7.45), 'c_cork_app': (51.55, -8.05),
}
# Mép khung (vao_tu_mep / ra_mep): điểm ngoài khung đích, chỉ để định hướng mũi tên
EDGE = {'e_west_portugal': (41.9, -11.0), 'e_west_strait': (35.6, -19.0), 'e_west_morocco': (33.3, -19.0), 'e_west_jamaica': (33.0, -20.0)}   # ngoài bbox SM2 (-11,5…5 / 34…41,5) và SM3 (-17,5…6 / 31…49,5)


def load_gz():
    raw = json.loads((RAW / 'gaz/_all.json').read_text())
    out = {}
    for k, (rk, dd, note) in GZ.items():
        if k == 'strait_west':
            a, b = raw['tarifa']['hits'][0], raw['cap_spartel']['hits'][0]
            lat, lon = (a['lat'] + b['lat']) / 2, (a['lon'] + b['lon']) / 2; src = 'tính từ Nominatim tarifa + cap_spartel'
            sh = raw['tarifa']['sha256'][:16] + '+' + raw['cap_spartel']['sha256'][:16]
        elif k == 'thames':
            lat, lon, src, sh = 51.48, 0.90, 'điểm biểu trưng (không phải gazetteer)', ''
        else:
            h = raw[rk]['hits'][0]; lat, lon = h['lat'], h['lon']; src = f"OSM Nominatim {h['osm']} ({h['type']})"; sh = raw[rk]['sha256']
            if dd: lat, lon = lat + dd[0], lon + dd[1]
        out[k] = {'lat': round(lat, 5), 'lon': round(lon, 5), 'nguon_toa_do': src, 'sha256_tho': sh, 'ghi_chu': note}
    return out


# Tuyến: id → thuộc tính + danh sách điểm (khoá điểm, claim[], loai: cang|moc|dieu_khien|mep, nhãn ngày)
R = [
 {'id': 'R1704-LIS', 'shot': ['SM1'], 'mode': 'sea', 'phe': 'grand-alliance', 'ten': 'Anglo-Dutch fleet with "Charles III" to Lisbon', 'nam': '1704', 'ngay': '1704-02-12/1704-02-25 (O.S.)',
  'nhan': 'Feb 1704', 'pts': [('st_helens', ['T001'], 'cang', '12 Feb (O.S.)'), ('c_wight_e', [], 'dieu_khien', ''), ('c_wight_s', [], 'dieu_khien', ''), ('c_channel_w', [], 'dieu_khien', ''), ('c_ushant', [], 'dieu_khien', ''), ('c_biscay', [], 'dieu_khien', ''),
  ('c_finisterre', [], 'dieu_khien', ''), ('c_porto_off', [], 'dieu_khien', ''), ('c_roca', [], 'dieu_khien', ''), ('c_tagus', [], 'dieu_khien', ''), ('lisbon', ['T001'], 'cang', '25 Feb (O.S.)')]},
 {'id': 'R1704-GIB', 'shot': ['SM1'], 'mode': 'sea', 'phe': 'grand-alliance', 'ten': 'Rooke\'s fleet: Algarve → off Tetuan → Bay of Gibraltar', 'nam': '1704', 'ngay': '1704-06-16/1704-07-21 (O.S.) = 1704-08-01 (N.S.)',
  'nhan': 'Jun–Aug 1704', 'pts': [('off_lagos', ['T002'], 'moc', '16 Jun (O.S.)'), ('c_gulf_cadiz', [], 'dieu_khien', ''), ('c_trafalgar_off', [], 'dieu_khien', ''), ('c_strait_w', [], 'dieu_khien', ''), ('c_strait_mid', [], 'dieu_khien', ''), ('c_ceuta_n', [], 'dieu_khien', ''), ('c_ceuta_e', [], 'dieu_khien', ''),
  ('off_tetuan', ['T003'], 'moc', '17 Jul (O.S.)'), ('c_ceuta_e', [], 'dieu_khien', ''), ('c_ceuta_n', [], 'dieu_khien', ''), ('c_europa_s', [], 'dieu_khien', ''), ('gib_bay', ['S012'], 'cang', '21 Jul (O.S.) / 1 Aug (N.S.)')]},
 {'id': 'R1780-PATROL', 'shot': ['SM2'], 'mode': 'sea', 'phe': 'spain', 'ten': 'Spanish cruising line, Strait ↔ Cape St Vincent', 'nam': '1780', 'ngay': '1780-01 (trước 16/1)', 'tuan_tra': True,
  'nhan': 'Spanish patrol, Jan 1780', 'pts': [('strait_west', ['T008'], 'moc', ''), ('c_strait_w', [], 'dieu_khien', ''), ('c_trafalgar_off', [], 'dieu_khien', ''), ('c_gulf_cadiz', [], 'dieu_khien', ''), ('off_st_vincent', ['T008'], 'moc', '')]},
 {'id': 'R1780-RODNEY', 'shot': ['SM2'], 'mode': 'sea', 'phe': 'britain', 'ten': 'Relief 1: Rodney', 'nam': '1780', 'ngay': '1779-12-27/1780-01-18', 'vao_tu_mep': True,
  'nhan': 'from England', 'pts': [('e_west_portugal', ['T009', 'T010'], 'mep', 'sailed 27 Dec 1779'), ('c_roca', [], 'dieu_khien', ''), ('off_st_vincent', ['T011'], 'moc', '16 Jan 1780'),
  ('c_gulf_cadiz', [], 'dieu_khien', ''), ('c_trafalgar_off', [], 'dieu_khien', ''), ('c_strait_w', [], 'dieu_khien', ''), ('c_strait_mid', [], 'dieu_khien', ''), ('c_strait_e', [], 'dieu_khien', ''), ('c_europa_s', [], 'dieu_khien', ''), ('gib_bay', ['S054'], 'cang', '18 Jan 1780')]},
 {'id': 'R1781-DARBY', 'shot': ['SM2'], 'mode': 'sea', 'phe': 'britain', 'ten': 'Relief 2: Darby', 'nam': '1781', 'ngay': '1781-03 (13/3 theo nguồn Anh; ~28/3 theo Fernández Duro)/1781-04-12',
  'nhan': 'from England', 'pts': [('st_helens', ['T013'], 'cang', 'Mar 1781'), ('c_wight_e', [], 'dieu_khien', ''), ('c_wight_s', [], 'dieu_khien', ''), ('c_channel_w', [], 'dieu_khien', ''), ('c_lizard', [], 'dieu_khien', ''), ('c_ireland_s', [], 'dieu_khien', ''), ('c_cork_app', [], 'dieu_khien', ''), ('off_cork', ['T014'], 'moc', ''), ('c_cork_app', [], 'dieu_khien', ''),
  ('c_scilly_s', [], 'dieu_khien', ''), ('c_biscay', [], 'dieu_khien', ''), ('c_finisterre', [], 'dieu_khien', ''), ('c_roca', [], 'dieu_khien', ''), ('off_st_vincent', [], 'dieu_khien', ''), ('c_gulf_cadiz', [], 'dieu_khien', ''),
  ('off_spartel', ['T014'], 'moc', '11 Apr 1781'), ('c_strait_w', [], 'dieu_khien', ''), ('c_strait_mid', [], 'dieu_khien', ''), ('c_strait_e', [], 'dieu_khien', ''), ('c_europa_s', [], 'dieu_khien', ''), ('gib_bay', ['S055', 'S062'], 'cang', '12 Apr 1781')]},
 {'id': 'R1782-HOWE', 'shot': ['SM2'], 'mode': 'sea', 'phe': 'britain', 'ten': 'Relief 3: Howe (swept into the Mediterranean, then back; action 20 Oct)', 'nam': '1782', 'ngay': '1782-09-11/1782-10-20',
  'nhan': 'from England', 'pts': [('spithead', ['T015'], 'cang', '11 Sep 1782'), ('c_wight_e', [], 'dieu_khien', ''), ('c_wight_s', [], 'dieu_khien', ''), ('c_channel_w', [], 'dieu_khien', ''), ('c_ushant', [], 'dieu_khien', ''), ('c_biscay', [], 'dieu_khien', ''), ('c_finisterre', [], 'dieu_khien', ''),
  ('c_roca', [], 'dieu_khien', ''), ('off_st_vincent', ['T016'], 'moc', '8 Oct 1782'), ('c_gulf_cadiz', [], 'dieu_khien', ''), ('c_trafalgar_off', [], 'dieu_khien', ''), ('c_strait_w', [], 'dieu_khien', ''), ('c_strait_mid', ['T016', 'S056'], 'moc', '11 Oct 1782'), ('c_strait_e', [], 'dieu_khien', ''),
  ('c_europa_s', [], 'dieu_khien', ''), ('c_alboran_w', [], 'dieu_khien', ''), ('off_fuengirola', ['T016'], 'moc', '13 Oct 1782'), ('c_alboran_w', [], 'dieu_khien', ''), ('c_europa_s', [], 'dieu_khien', ''),
  ('gib_bay', ['S056'], 'cang', '18 Oct 1782'), ('c_europa_s', [], 'dieu_khien', ''), ('c_strait_e', [], 'dieu_khien', ''), ('c_strait_mid', [], 'dieu_khien', ''), ('c_strait_w', [], 'dieu_khien', ''), ('off_spartel', ['T017'], 'moc', '20 Oct 1782 (action, zone)')]},
 {'id': 'R1782-ALLIED', 'shot': ['SM2'], 'mode': 'sea', 'phe': 'france-spain', 'ten': 'Combined French–Spanish fleet enters the bay', 'nam': '1782', 'ngay': '1782-09-12',
  'nhan': '12 Sep 1782', 'pts': [('strait_west', ['T018'], 'moc', 'morning 12 Sep'), ('c_strait_mid', [], 'dieu_khien', ''), ('c_strait_e', [], 'dieu_khien', ''), ('c_bay_mouth', [], 'dieu_khien', ''), ('algeciras_anch', ['T018', 'S065'], 'cang', 'afternoon 12 Sep')]},
 {'id': 'R1940-EV-CASA', 'shot': ['SM3'], 'mode': 'sea', 'phe': 'civilians', 'ten': 'Civilian evacuation to French Morocco', 'nam': '1940', 'ngay': '1940-05-22/1940-06-24',
  'nhan': 'to Casablanca', 'pts': [('gibraltar', ['S114', 'S115'], 'cang', 'from 22 May 1940'), ('c_europa_s', [], 'dieu_khien', ''), ('c_strait_e', [], 'dieu_khien', ''), ('c_strait_mid', [], 'dieu_khien', ''), ('strait_west', [], 'dieu_khien', ''), ('off_spartel', [], 'dieu_khien', ''),
  ('c_off_rabat', [], 'dieu_khien', ''), ('casablanca', ['S115'], 'cang', '')]},
 {'id': 'R1940-EV-LON', 'shot': ['SM3'], 'mode': 'sea', 'phe': 'civilians', 'ten': 'Civilian evacuation to London', 'nam': '1940', 'ngay': '1940-07/1940-08-20',
  'nhan': 'to London', 'pts': [('gibraltar', ['S114', 'S117'], 'cang', 'Jul–Aug 1940'), ('c_europa_s', [], 'dieu_khien', ''), ('c_strait_e', [], 'dieu_khien', ''), ('c_strait_mid', [], 'dieu_khien', ''), ('strait_west', [], 'dieu_khien', ''), ('c_gulf_cadiz', [], 'dieu_khien', ''),
  ('off_st_vincent', [], 'dieu_khien', ''), ('c_roca', [], 'dieu_khien', ''), ('c_finisterre', [], 'dieu_khien', ''), ('c_biscay', [], 'dieu_khien', ''), ('c_ushant', [], 'dieu_khien', ''), ('c_channel_w', [], 'dieu_khien', ''),
  ('c_dover', [], 'dieu_khien', ''), ('c_foreland', [], 'dieu_khien', ''), ('c_thames_mouth', [], 'dieu_khien', ''), ('thames', ['S114', 'S116'], 'cang', 'London')]},
 {'id': 'R1940-EV-MAD', 'shot': ['SM3'], 'mode': 'sea', 'phe': 'civilians', 'ten': 'Civilian evacuation to Madeira', 'nam': '1940', 'ngay': '1940-07/1940-08',
  'nhan': 'to Madeira', 'pts': [('gibraltar', ['S117', 'S120'], 'cang', ''), ('c_europa_s', [], 'dieu_khien', ''), ('c_strait_e', [], 'dieu_khien', ''), ('c_strait_mid', [], 'dieu_khien', ''), ('strait_west', [], 'dieu_khien', ''), ('c_madeira_n', [], 'dieu_khien', ''), ('c_madeira_e', [], 'dieu_khien', ''), ('c_funchal_off', [], 'dieu_khien', ''),
  ('funchal', ['S117', 'S120'], 'cang', '')]},
 {'id': 'R1940-EV-JAM', 'shot': ['SM3'], 'mode': 'sea', 'phe': 'civilians', 'ten': 'Civilian evacuation to Jamaica', 'nam': '1940', 'ngay': '1940-10-09 (Neuralia) / 1940-10-31 (Thysville)', 'ra_mep': True,
  'nhan': 'to Jamaica', 'pts': [('gibraltar', ['S118'], 'cang', 'Oct 1940'), ('c_europa_s', [], 'dieu_khien', ''), ('c_strait_e', [], 'dieu_khien', ''), ('c_strait_mid', [], 'dieu_khien', ''), ('strait_west', [], 'dieu_khien', ''), ('e_west_jamaica', ['S118'], 'mep', 'to Jamaica')]},
 {'id': 'R1942-AIR-ORAN', 'shot': ['SM3'], 'mode': 'air', 'phe': 'allies', 'ten': 'Twelfth Air Force Spitfires, Gibraltar → Tafaraoui', 'nam': '1942', 'ngay': '1942-11-08',
  'nhan': '8 Nov 1942', 'pts': [('gibraltar', ['T024', 'S122', 'S123'], 'cang', '8 Nov 1942'), ('tafraoui', ['T024'], 'cang', '16:30')]},
 {'id': 'R1942-SEA-WEST', 'shot': ['SM3'], 'mode': 'sea', 'phe': 'allies', 'ten': 'Torch landings, French Morocco', 'nam': '1942', 'ngay': '1942-11-08', 'vao_tu_mep': True,
  'nhan': 'Allied landings', 'pts': [('e_west_morocco', ['T025'], 'mep', ''), ('c_fedala_off', [], 'dieu_khien', ''), ('mohammedia', ['T023'], 'cang', '8 Nov 1942')]},
 {'id': 'R1942-SEA-ORAN', 'shot': ['SM3'], 'mode': 'sea', 'phe': 'allies', 'ten': 'Torch landings, Oran', 'nam': '1942', 'ngay': '1942-11-08', 'vao_tu_mep': True,
  'nhan': 'Allied landings', 'pts': [('e_west_strait', ['T025'], 'mep', ''), ('c_trafalgar_off', [], 'dieu_khien', ''), ('c_strait_w', [], 'dieu_khien', ''), ('c_strait_mid', [], 'dieu_khien', ''), ('c_strait_e', [], 'dieu_khien', ''), ('c_europa_s', [], 'dieu_khien', ''), ('c_alboran_e', [], 'dieu_khien', ''),
  ('c_oran_off', [], 'dieu_khien', ''), ('oran', ['T023'], 'cang', '8 Nov 1942')]},
 {'id': 'R1942-SEA-ALG', 'shot': ['SM3'], 'mode': 'sea', 'phe': 'allies', 'ten': 'Torch landings, Algiers', 'nam': '1942', 'ngay': '1942-11-08', 'vao_tu_mep': True,
  'nhan': 'Allied landings', 'pts': [('e_west_strait', ['T025'], 'mep', ''), ('c_trafalgar_off', [], 'dieu_khien', ''), ('c_strait_w', [], 'dieu_khien', ''), ('c_strait_mid', [], 'dieu_khien', ''), ('c_strait_e', [], 'dieu_khien', ''), ('c_europa_s', [], 'dieu_khien', ''), ('c_alboran_e', [], 'dieu_khien', ''),
  ('c_algiers_off', [], 'dieu_khien', ''), ('c_algiers_bay', [], 'dieu_khien', ''), ('algiers', ['T023'], 'cang', '8 Nov 1942')]},
]
# Vùng (sự kiện có vị trí MÂU THUẪN → vẽ vùng, không vẽ điểm)
Z = [
 {'id': 'Z1780-MOONLIGHT', 'shot': ['SM2'], 'claims': ['T012'], 'ten': 'Moonlight Battle, 16 Jan 1780 (approx.)', 'tam': [(36.82, -9.00), (36.90, -7.89)], 'ban_kinh_km': 22,
  'ghi_chu': 'Elip bao điểm Beatson (mũi St Vincent ở bắc 4 league ≈ 22 km → 36,82 N 9,00 W) và ngoài khơi mũi Santa María (Fernández Duro/Ancell/Montero).'},
 {'id': 'Z1782-SPARTEL', 'shot': ['SM2'], 'claims': ['T017'], 'ten': 'Cape Spartel action, 20 Oct 1782 (approx.)', 'tam': [(35.85, -6.10), (36.40, -6.55)], 'ban_kinh_km': 22,
  'ghi_chu': 'Elip bao "á la vista de Cabo Espartel" (Fernández Duro) và "al oeste de Cádiz" (Montero/Córdoba).'},
 {'id': 'Z1779-BLOCKADE', 'shot': ['SM2'], 'claims': ['T006', 'T007', 'S042'], 'ten': 'Spanish blockade 1779–83 (Algeciras · Cabrita Point · Ceuta)', 'tam': [(36.13, -5.42), (35.92, -5.33)], 'ban_kinh_km': 10,
  'ghi_chu': 'Vòng phong toả biểu trưng, nét đứt: căn cứ Algeciras (T006), trạm Punta Carnero/Cabrita (T007), Ceuta (T006, Drinkwater). Không vẽ đường tàu.'},
]


def catmull(pts, step_m=4000, alpha=0.5):
    """Catmull–Rom hướng tâm (centripetal, alpha 0,5 — không vọt/không nút ở chỗ quay đầu), lấy mẫu ~step_m (mét)."""
    P = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    def tj(ti, a, b): return ti + max(math.dist(a, b), 1e-6) ** alpha
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        if math.dist(p1, p2) < 1: continue
        if math.dist(p0, p1) < 1: p0 = tuple(2 * p1[j] - p2[j] for j in (0, 1))
        if math.dist(p2, p3) < 1: p3 = tuple(2 * p2[j] - p1[j] for j in (0, 1))
        t0 = 0; t1 = tj(t0, p0, p1); t2 = tj(t1, p1, p2); t3 = tj(t2, p2, p3)
        n = max(2, int(math.dist(p1, p2) / step_m))
        for k in range(n):
            t = t1 + (t2 - t1) * k / n
            A1 = [((t1 - t) * p0[j] + (t - t0) * p1[j]) / (t1 - t0) for j in (0, 1)]
            A2 = [((t2 - t) * p1[j] + (t - t1) * p2[j]) / (t2 - t1) for j in (0, 1)]
            A3 = [((t3 - t) * p2[j] + (t - t2) * p3[j]) / (t3 - t2) for j in (0, 1)]
            B1 = [((t2 - t) * A1[j] + (t - t0) * A2[j]) / (t2 - t0) for j in (0, 1)]
            B2 = [((t3 - t) * A2[j] + (t - t1) * A3[j]) / (t3 - t1) for j in (0, 1)]
            out.append(tuple(((t2 - t) * B1[j] + (t - t1) * B2[j]) / (t2 - t1) for j in (0, 1)))
    out.append(tuple(pts[-1]))
    return out


def load_land(bb):
    polys = []
    for f in NE:
        r = shapefile.Reader(str(f))
        for s in r.shapes():
            g = shape(s.__geo_interface__)
            if g.intersects(bb): polys.append(g.intersection(bb))
    return transform(FWD, unary_union(polys))


def ellipse(a, b, r_km):
    pa, pb = Point(FWD(a[1], a[0])), Point(FWD(b[1], b[0]))
    return LineString([pa, pb]).buffer(r_km * 1000)


def main():
    for z, h in NE_ZIP.items():
        assert hashlib.sha256((RAW / 'ne' / z).read_bytes()).hexdigest() == h, z
    gz = load_gz()
    allp = {k: (v['lat'], v['lon']) for k, v in gz.items()} | CTL | EDGE
    land = load_land(box(-25, 25, 12, 58))
    feats, kiem = [], []
    for r in R:
        keys = [p[0] for p in r['pts']]
        xy = [FWD(allp[k][1], allp[k][0]) for k in keys]
        line = LineString(catmull(xy))
        # đệm 5 km quanh điểm loại "cang" (đầu/cuối tuyến ở cảng)
        ports = unary_union([Point(xy[i]).buffer(BUF_CANG_KM * 1000) for i, p in enumerate(r['pts']) if p[2] == 'cang'])
        if r['mode'] == 'sea':
            cut = line.difference(ports).intersection(land)
            km_dat = cut.length / 1000
            rest = line.difference(ports); dmin = (land.distance(rest) / 1000) if not rest.is_empty else None
        else:
            km_dat, dmin = None, None
        kiem.append({'tuyen': r['id'], 'mode': r['mode'], 'dai_km': round(line.length / 1000, 1), 'cat_dat_km': None if km_dat is None else round(km_dat, 3),
                     'gan_bo_nhat_km': None if dmin is None else round(dmin, 2), 'dat': (km_dat == 0) if km_dat is not None else 'không áp (đường không)'})
        # waypoint có claim + đoạn
        wps, segs = [], []
        claimed = [i for i, p in enumerate(r['pts']) if p[1]]
        for i, (k, cl, loai, nh) in enumerate(r['pts']):
            if loai != 'dieu_khien':
                wps.append({'diem': k, 'lon': allp[k][1], 'lat': allp[k][0], 'claims': cl, 'loai': loai, 'nhan_ngay': nh})
        for a, b in zip(claimed, claimed[1:]):
            segs.append({'tu': r['pts'][a][0], 'den': r['pts'][b][0], 'approx': True, 'so_diem_dieu_khien': b - a - 1})
        geo = transform(INV, line)
        props = {k: v for k, v in r.items() if k != 'pts'} | {'waypoints': wps, 'doan': segs, 'vao_tu_mep': r.get('vao_tu_mep', False), 'ra_mep': r.get('ra_mep', False),
                 'diem_dieu_khien': [k for k, cl, loai, nh in r['pts'] if loai == 'dieu_khien'], 'kiem_dat': kiem[-1]}
        feats.append({'type': 'Feature', 'geometry': {'type': 'LineString', 'coordinates': [[round(x, 4), round(y, 4)] for x, y in geo.coords]}, 'properties': props})
    for z in Z:
        g = transform(INV, ellipse(*z['tam'], z['ban_kinh_km']).simplify(500))
        feats.append({'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [[[round(x, 4), round(y, 4)] for x, y in g.exterior.coords]]},
                      'properties': {'id': z['id'], 'loai': 'vung', 'shot': z['shot'], 'claims': z['claims'], 'ten': z['ten'], 'approx': True, 'ghi_chu': z['ghi_chu']}})
    fc = {'type': 'FeatureCollection', 'name': 'T3 routes (gói TUYẾN 17/10/2026)',
          'note': 'Toạ độ WGS84. Waypoint mang claim id (T… = claims-tuyen.json; S… = vay-ham/claims-vay-ham.json). Điểm điều khiển chỉ giữ nét trên biển, KHÔNG phải sự kiện. Mọi đoạn giữa hai điểm có claim là approx. Gazetteer: © OpenStreetMap contributors (ODbL), xem gazetteer.json. Bờ biển kiểm: Natural Earth 1:10m (PD).',
          'features': feats}
    (HERE / 'routes.geojson').write_text(json.dumps(fc, ensure_ascii=False, indent=1) + '\n')
    (HERE / 'gazetteer.json').write_text(json.dumps({'note': 'Toạ độ điểm mốc (OSM Nominatim 17/10/2026, ODbL; tệp thô ngoài git /var/tmp/cine-out/tuyen/gaz/). Độ dời ra khơi ghi ở ghi_chu.', 'diem': gz,
                                                    'dieu_khien': {k: {'lat': v[0], 'lon': v[1]} for k, v in CTL.items()}, 'mep': {k: {'lat': v[0], 'lon': v[1]} for k, v in EDGE.items()}}, ensure_ascii=False, indent=1) + '\n')
    # kiểm điểm điều khiển/waypoint biển không nằm trên đất
    pts_dat = [k for k, (la, lo) in (CTL | EDGE).items() if land.contains(Point(FWD(lo, la)))]
    pts_dat += [k for k, v in gz.items() if k.startswith('off_') or k in ('strait_west', 'gib_bay', 'algeciras_anch') if land.contains(Point(FWD(v['lon'], v['lat'])))]
    out = {'nguon_bo': 'Natural Earth 1:10m land + minor islands (v5.1.1)', 'dem_cang_km': BUF_CANG_KM, 'tuyen': kiem, 'diem_bien_nam_tren_dat': pts_dat,
           'dat': all(k['dat'] is True or k['mode'] == 'air' for k in kiem) and not pts_dat}
    (HERE / 'kiem-dat.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
    for k in kiem: print(k)
    print('điểm biển trên đất:', pts_dat, '| KIỂM ĐẤT:', 'ĐẠT' if out['dat'] else 'TRƯỢT')
    return 0 if out['dat'] else 1


if __name__ == '__main__':
    sys.exit(main())
