"""T3 · gói TUYẾN · dựng tuyen/ranh-gioi.json: ranh giới 3 mốc (1704, 1780–82, 1941) theo NC-BD §2.1 (B1) + chỉnh tay theo claim + màu phe B6.
Đo ΔE (CIE76, CIELAB D65) giữa các màu phe — thường và mô phỏng deuteranopia (Machado et al. 2009, mức 1,0) — để kiểm đề xuất "ΔE ≥ 20" của NC-BD §3.3.7.
Dùng: /opt/cine/bin/python -I channel-k2/k2c-t3-01/tuyen/mk_ranh.py"""
import itertools, json
from pathlib import Path

HERE = Path(__file__).resolve().parent

MAU = {'britain': '#b03a2e', 'spain': '#c9a227', 'france': '#2e5c8a', 'neutral': '#a89f8a', 'civilians': '#efe6cf'}
# Đồng minh "nhỏ" (không có màu cố định của series) = màu phe dẫn đầu pha 85 % với nền giấy + gạch chéo 45° (xem `de_xuat_dong_minh`; mức 85 % chọn theo ΔE deuteranopia, bảng `do_mau`)
NHAT = 0.85


def hex2rgb(h): return tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
def lin(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def delin(c): c = max(0.0, min(1.0, c)); return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def lab(rgb):
    r, g, b = (lin(c) for c in rgb)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047; y = 0.2126 * r + 0.7152 * g + 0.0722 * b; z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    return (116 * f(y) - 16, 500 * (f(x) - f(y)), 200 * (f(y) - f(z)))


def deuter(rgb):   # Machado 2009, deuteranopia severity 1.0, trên RGB tuyến tính
    M = ((0.367322, 0.860646, -0.227968), (0.280085, 0.672501, 0.047413), (-0.011820, 0.042940, 0.968881))
    l = [lin(c) for c in rgb]
    return tuple(delin(sum(M[i][j] * l[j] for j in range(3))) for i in range(3))


def tint(h, a):   # pha với trắng giấy bản đồ (#f4efe4) theo tỉ lệ a của màu
    p = hex2rgb('#f4efe4'); c = hex2rgb(h)
    return '#' + ''.join(f'{round((a * c[i] + (1 - a) * p[i]) * 255):02x}' for i in range(3))


def de(a, b): return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def do_delta():
    cols = dict(MAU) | {'britain_ally_tint': tint(MAU['britain'], NHAT)}
    out = []
    for (ka, ha), (kb, hb) in itertools.combinations(cols.items(), 2):
        a, b = hex2rgb(ha), hex2rgb(hb)
        out.append({'cap': f'{ka} ↔ {kb}', 'dE76': round(de(lab(a), lab(b)), 1), 'dE76_deuteranopia': round(de(lab(deuter(a)), lab(deuter(b))), 1)})
    return cols, out


MOC = [
 {'moc': '1704', 'shot': ['SM1'], 'ngay_ranh': '1704-08 (N.S.)', 'nhan_tren_hinh': 'approx. borders c. 1704 — OpenHistoricalMap, IGN',
  'nguon_chinh': {'ten': 'OpenHistoricalMap (OHM)', 'giay_phep': 'CC0; nhiều đường mang CC BY 4.0 (CNIG/IGN) → ghi công bắt buộc', 'ly_do': 'NC-BD §2.1/B1: OHM theo NGÀY; quan hệ "Spain" bắt đầu 1704-08-04 (ngày Gibraltar đổi chủ)'},
  'nguon_doi_chieu': {'ten': 'Cliopatria v0.2.1 (Seshat)', 'giay_phep': 'CC BY 4.0', 'khoang': '1702–1705'},
  'thuc_the': [
   {'ten_tren_hinh': 'England', 'ohm': 'Kingdom of England', 'cliopatria': 'Kingdom of England', 'phe': 'grand-alliance', 'mau': MAU['britain'], 'kieu': 'đặc', 'claims': ['T004']},
   {'ten_tren_hinh': 'Dutch Republic', 'ohm': 'Republic of the Seven United Netherlands', 'cliopatria': 'Dutch Republic', 'phe': 'grand-alliance', 'mau': MAU['britain'], 'kieu': f'pha {int(NHAT*100)} % với nền + gạch 45°', 'claims': ['T004']},
   {'ten_tren_hinh': 'Portugal (allied from 1703)', 'ohm': 'Kingdom of Portugal', 'cliopatria': 'Kingdom of Portugal', 'phe': 'grand-alliance', 'mau': MAU['britain'], 'kieu': f'pha {int(NHAT*100)} % với nền + gạch 45°', 'claims': ['T005']},
   {'ten_tren_hinh': 'France', 'ohm': 'Kingdom of France', 'cliopatria': 'Kingdom of France', 'phe': 'bourbon', 'mau': MAU['france'], 'kieu': 'đặc', 'claims': ['T004']},
   {'ten_tren_hinh': 'Spain (Philip V)', 'ohm': 'Spain (España, từ 1704-08-04)', 'cliopatria': 'Kingdom of Spain + Pro-Habsburg Spain (GỘP)', 'phe': 'bourbon', 'mau': MAU['spain'], 'kieu': 'đặc', 'claims': ['T004', 'S012', 'S017']},
   {'ten_tren_hinh': 'Gibraltar', 'ohm': '— (điểm)', 'cliopatria': '—', 'phe': 'grand-alliance (từ 1/8/1704 N.S., nhân danh "Charles III")', 'mau': MAU['britain'], 'kieu': 'ĐIỂM vòng tròn viền trắng (< 8 px)', 'claims': ['S012', 'S013', 'S017']},
   {'ten_tren_hinh': 'Morocco', 'ohm': 'Alawi Sultanate', 'cliopatria': 'Morocco', 'phe': 'không tham chiến', 'mau': MAU['neutral'], 'kieu': 'đặc', 'claims': []},
   {'ten_tren_hinh': '(Holy Roman Empire — ngoài khung/viền)', 'ohm': 'Holy Roman Empire', 'cliopatria': '—', 'phe': 'grand-alliance', 'mau': MAU['britain'], 'kieu': f'pha {int(NHAT*100)} % với nền + gạch 45° nếu lọt khung', 'claims': ['T004']},
  ],
  'chinh_tay': [
   'BỎ tách "Pro-Habsburg Spain" của Cliopatria (sai thời điểm, NC-BD bẫy d): gộp vào một thực thể "Spain (Philip V)". Không tô phe trong lòng Tây Ban Nha.',
   'Gibraltar = ĐIỂM, xuất hiện màu Đại Liên minh đúng lúc bộ đếm qua 1 Aug 1704 (N.S.); nhãn phụ "taken in the name of \'Charles III\'" (S012; S017 MÂU THUẪN → chỉ dùng phần đã xác minh).',
   'Bồ Đào Nha tô màu đồng minh (T005, 5/1703) — Cliopatria/OHM không mang thông tin liên minh, phải tô theo claim.',
   'Lệch diện tích Tây Ban Nha OHM↔Cliopatria 1704 = 5,0 % do tách Pro-Habsburg (NC-BD) → sau khi gộp phải đo lại (việc của V5b-2c).',
  ],
  'chu_giai': ['Grand Alliance (England & allies)', 'France', 'Spain (Philip V)'],
 },
 {'moc': '1780–82', 'shot': ['SM2'], 'ngay_ranh': '1780-01 → 1782-10 (đổi theo bộ đếm)', 'nhan_tren_hinh': 'approx. borders c. 1782 — Cliopatria (Seshat)',
  'nguon_chinh': {'ten': 'Cliopatria v0.2.1 (Seshat)', 'giay_phep': 'CC BY 4.0', 'ly_do': 'NC-BD §2.1/B1: khái quát vừa tầm châu lục'},
  'nguon_doi_chieu': {'ten': 'OpenHistoricalMap', 'giay_phep': 'CC0 + CC BY 4.0', 'ghi_chu': 'theo ngày; Spain 1782-01-05 (SAI so T020)'},
  'thuc_the': [
   {'ten_tren_hinh': 'Great Britain', 'cliopatria': 'Kingdom of Great Britain', 'phe': 'britain', 'mau': MAU['britain'], 'kieu': 'đặc', 'claims': []},
   {'ten_tren_hinh': 'Gibraltar', 'cliopatria': '— (điểm)', 'phe': 'britain', 'mau': MAU['britain'], 'kieu': 'ĐIỂM (< 8 px)', 'claims': ['S040', 'S042']},
   {'ten_tren_hinh': 'Spain', 'cliopatria': 'Kingdom of Spain (1781–1795) / (Spanish Empire)', 'phe': 'spain', 'mau': MAU['spain'], 'kieu': 'đặc', 'claims': ['T006']},
   {'ten_tren_hinh': 'France', 'cliopatria': 'Kingdom of France', 'phe': 'france (đồng minh của TBN, giữ màu riêng)', 'mau': MAU['france'], 'kieu': 'đặc', 'claims': ['T018']},
   {'ten_tren_hinh': 'Minorca', 'cliopatria': 'trong "Kingdom of Spain" từ 1781 (SAI cho 1780–5/2/1782)', 'phe': 'britain → spain ĐÚNG 1782-02-05', 'mau': f"{MAU['britain']} → {MAU['spain']}", 'kieu': 'đặc — Menorca dài 49,1 km × 23,3 km (đo trên NE 1:10m) ≈ 38 × 18 px ở khung 2 500 km (≈ 1,3 km/px) → vẽ polygon, không phải điểm', 'claims': ['T020']},
   {'ten_tren_hinh': 'Portugal', 'cliopatria': 'Kingdom of Portugal', 'phe': 'không tham chiến', 'mau': MAU['neutral'], 'kieu': 'đặc', 'claims': []},
   {'ten_tren_hinh': 'Morocco', 'cliopatria': 'Morocco', 'phe': 'không tham chiến', 'mau': MAU['neutral'], 'kieu': 'đặc', 'claims': []},
  ],
  'chinh_tay': [
   'Minorca: tô ANH cho mọi khung trước 1782-02-05 (đoàn Rodney 1/1780, Darby 4/1781), đổi sang TBN đúng 1782-02-05 khi bộ đếm đi qua (T020: cờ trắng 4/2, đầu hàng 5/2/1782; Fernández Duro + Schomberg). Cliopatria (1781) và OHM (1782-01-05) đều sai → sửa tay.',
   'Gibraltar = ĐIỂM màu Anh; không vẽ polygon, không vẽ biên trên eo đất (NC-BD bẫy a/b).',
   'Vòng phong toả (Z1779-BLOCKADE) và hai vùng trận (Z1780-MOONLIGHT, Z1782-SPARTEL) vẽ ĐÈ, không đổi màu ranh.',
   'Không tô Đan Mạch/Hà Lan (ngoài khung); nếu khung lọt Hà Lan (chiến tranh với Anh từ 12/1780) → CHƯA có claim → tô trung tính, không nhãn phe.',
  ],
  'chu_giai': ['Britain', 'Spain', 'France'],
 },
 {'moc': '1941', 'shot': ['SM3'], 'ngay_ranh': '1941 (SM3 kể 1940 → 11/1942)', 'nhan_tren_hinh': 'approx. borders c. 1941 — Cliopatria (Seshat)',
  'nguon_chinh': {'ten': 'Cliopatria v0.2.1 (Seshat)', 'giay_phep': 'CC BY 4.0', 'ly_do': 'NC-BD §2.1/B1: có vùng chiếm đóng 1941'},
  'nguon_doi_chieu': {'ten': 'OpenHistoricalMap', 'giay_phep': 'CC0 + CC BY 4.0', 'ghi_chu': 'thiếu vùng chiếm đóng ("French State" cả nước) → chỉ đối chiếu phần Tây Ban Nha/Bồ Đào Nha'},
  'thuc_the': [
   {'ten_tren_hinh': 'Britain', 'cliopatria': 'Kingdom of Great Britain (tên Cliopatria) → nhãn "Britain"', 'phe': 'britain', 'mau': MAU['britain'], 'kieu': 'đặc', 'claims': []},
   {'ten_tren_hinh': 'Gibraltar', 'cliopatria': '— (điểm)', 'phe': 'britain', 'mau': MAU['britain'], 'kieu': 'ĐIỂM (< 8 px)', 'claims': ['S122', 'T024']},
   {'ten_tren_hinh': 'Spain (non-belligerent)', 'cliopatria': 'Francoist Spain', 'phe': 'spain (giữ màu thực thể; trạng thái bằng nhãn)', 'mau': MAU['spain'], 'kieu': 'đặc', 'claims': ['T021']},
   {'ten_tren_hinh': 'Tangier (Spanish-occupied since June 1940)', 'cliopatria': 'Tangier International Zone (SAI cho 1941)', 'phe': 'spain', 'mau': MAU['spain'], 'kieu': 'gạch 45° màu TBN trên nền trung tính', 'claims': ['T022']},
   {'ten_tren_hinh': 'Vichy France', 'cliopatria': 'Vichy France', 'phe': 'france (giữ màu thực thể)', 'mau': MAU['france'], 'kieu': 'đặc', 'claims': ['T026']},
   {'ten_tren_hinh': 'German-occupied France', 'cliopatria': 'phần "Nazi Germany" phủ miền bắc/tây Pháp', 'phe': 'vùng chiếm đóng', 'mau': MAU['neutral'], 'kieu': 'gạch chéo xám-nâu, nhãn chữ; KHÔNG dùng màu/biểu tượng chế độ', 'claims': ['T026']},
   {'ten_tren_hinh': 'Portugal', 'cliopatria': 'Estado Novo → nhãn "Portugal"', 'phe': 'không tham chiến', 'mau': MAU['neutral'], 'kieu': 'đặc', 'claims': []},
   {'ten_tren_hinh': 'French Morocco · Algeria', 'cliopatria': 'French Africa', 'phe': 'france', 'mau': MAU['france'], 'kieu': f'pha {int(NHAT*100)} % với nền (thuộc địa)', 'claims': ['T023', 'S114']},
   {'ten_tren_hinh': 'Spanish Morocco', 'cliopatria': '(kiểm: có thể nằm trong "Francoist Spain")', 'phe': 'spain', 'mau': MAU['spain'], 'kieu': f'pha {int(NHAT*100)} % với nền', 'claims': ['T022 (gián tiếp: "Spanish High Commissioner at Tetuan")']},
  ],
  'chinh_tay': [
   'Tangier: đổi từ "International Zone" sang "Spanish-occupied since June 1940" (T022: 14/6/1940, FRUS + Hansard); KHÔNG ghi năm kết thúc (chưa có claim).',
   'Đặt tên đúng: "German-occupied France" / "Vichy France" (T026); vùng chiếm đóng tô xám-nâu gạch, không tô màu Đức, không biểu tượng (K-R2, NC-BD §3.3.7).',
   'Tây Ban Nha giữ màu thực thể (vàng đất) suốt tập — trạng thái 1940–41 thể hiện bằng nhãn "Spain (non-belligerent)" (T021), không đổi sang xám: một thực thể một màu (NC-BD §3.3.7), tránh khán giả hiểu nhầm là "nước khác".',
   'Đổi nhãn tên Cliopatria sang tên khán giả hiểu: "Francoist Spain" → "Spain", "Estado Novo" → "Portugal", "Kingdom of Great Britain" (Cliopatria 1941) → "Britain".',
   'Vichy ở Bắc Phi: KHÔNG có claim cho chữ "Vichy" ở Maroc/Algérie → nhãn "French Morocco", "Algeria" (T023 Hansard dùng "French Morocco").',
  ],
  'chu_giai': ['Britain & Allies', 'Spain (non-belligerent)', 'France: Vichy / German-occupied (hatched)'],
 },
]


def main():
    cols, dl = do_delta()
    doc = {'note': 'Ranh giới lịch sử cho 3 shot strategic T3 (gói TUYẾN 17/10/2026). Nguồn theo NC-BD §2.1 (B1, chủ dự án duyệt 17/10); màu theo B6. Claim T… = claims-tuyen.json; S… = vay-ham/claims-vay-ham.json.',
           'mau_phe_B6': MAU | {'_ghi_chu': 'civilians = kem trung tính (B6 "dân thường kem"); mã kem đề xuất #efe6cf (B6 không ghi mã)'},
           'de_xuat_dong_minh': {
             'chon': 'PHƯƠNG ÁN A — đồng minh "nhỏ" (không có màu cố định của series) dùng màu phe dẫn đầu, pha 85 % với nền giấy + gạch chéo 45° (nét trắng ngà); đồng minh có màu cố định của series (Pháp ↔ Tây Ban Nha 1779–83) GIỮ màu riêng.',
             'ly_do': ['Chú giải ≤ 3 phe/shot (B2/§3.1): gộp Hà Lan, Bồ Đào Nha, Đế quốc La Mã Thần thánh vào một mục "Grand Alliance" không tốn thêm mục chú giải.',
                       'Một thực thể một màu suốt tập (NC-BD §3.3.7): Pháp và Tây Ban Nha đã có màu series → không nhuộm Pháp sang vàng hay ngược lại; khán giả đã học hai màu này từ SM1.',
                       'Gạch chéo phân biệt được cả khi in đen trắng/mù màu (không chỉ dựa vào sắc độ).'],
             'phuong_an_B': 'màu riêng cho từng đồng minh (Hà Lan cam, Bồ Đào Nha xanh lục…) — nhược: vượt 3 mục chú giải ở SM1; thêm màu phải khoá cho cả series; ΔE với đỏ Anh dưới mô phỏng deuteranopia khó đạt.',
             'tac_dong': 'M13-lite cần kiểu tô "nhạt + gạch" (pattern fill) — V5b-2c.',
             'rui_ro': 'gạch dày ở khung nhỏ gây nhiễu (moiré) khi nén YouTube → gạch ≥ 6 px, góc 45°, độ tương phản thấp; kiểm ở G1b.'},
           'moc': MOC, 'do_mau': {'mau': cols, 'cap': dl, 'nguong_de_xuat': 'ΔE ≥ 20 dưới deuteranopia giữa hai phe đối địch (NC-BD §3.3.7, chưa phải luật K)'},
           'nhan_nguon_luat_B5': '"approx. borders c. YYYY — <nguồn ngắn>", ≥ 38 px (SRCPX 16:9), góc dưới trái, suốt lúc hiện ranh; nguồn đầy đủ + giấy phép ở mô tả.',
           'ghi_cong_mo_ta': ['Borders: Cliopatria v0.2.1 (Seshat Global History Databank), CC BY 4.0', 'Borders: OpenHistoricalMap contributors (CC0); includes data © Instituto Geográfico Nacional (CNIG), CC BY 4.0',
                              'Coastline: Natural Earth (public domain)', 'Place coordinates: © OpenStreetMap contributors (ODbL)']}
    (HERE / 'ranh-gioi.json').write_text(json.dumps(doc, ensure_ascii=False, indent=1) + '\n')
    for d in dl: print(d)


if __name__ == '__main__':
    main()
