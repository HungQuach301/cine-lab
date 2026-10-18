#!/opt/cine/bin/python
"""Tự kiểm luật 1.15 (phiên K, 18/10/2026): K-LAI-1…6 + K-LAI-B (P2-2, P2-3), O2 máy soi lỗi thời đại (O2), BC2–BC4 bố cục (I3), Q37 + TL-Q1 nhận
biến cố cảnh tl / mốc dừng giờ (I8). Mỗi luật ≥ 1 ca ĐẠT + ≥ 1 ca TRƯỢT. Dữ liệu:
  fixtures/k115/ep-lai/   tập giả 60 s, shot LAI 6 s (make_fixtures.py)        fixtures/k115/pt2/     sổ THẬT PT2 (origin/pt2-lai)
  fixtures/k115/bc/       bộ timelapse giả 10 s (mặt nạ, log vật, hero)       fixtures/k115/v5b2b/   đoạn thử THẬT V5b-2b (origin/v5b2b)
  fixtures/k115/o2/       ảnh O2 + cache.json (trả lời claude-sonnet-5-5 của lượt chạy thật 18/10, PROMPT_VER o2-v2)
  fixtures/k1121/tl-gib20-v5b2a/  hero thật gib20 (BC4)  ·  fixtures/k112/tl-ams30, k1121/tl-gib20-v5b2a  TL-Q1 cũ không đổi
Không gọi mạng/API (O2 chỉ đọc bộ đệm); `--api` chạy lại O2 thật (có chi phí, ghi bộ đệm mới vào thư mục tạm). Biến thể ghi vào thư mục tạm.

  /opt/cine/bin/python checks/ll/selftest_k115.py        mã thoát 0 = mọi ca đúng kỳ vọng
"""
import copy, gzip, json, os, shutil, sys, tempfile

import cv2
import numpy as np
import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ROOT)
from checks.ll import q_lai as LA, q_thoi_dai as O2, q_bocuc as BC, q_nhip as NH, q_tl as QT, cap112  # noqa: E402

FX = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
K = os.path.join(FX, 'k115'); EL = os.path.join(K, 'ep-lai'); TMP = tempfile.mkdtemp(prefix='k115-')
R = []


def case(rule, name, got, expect_fail):
    got = list(got) if got else []
    R.append((rule, name, 'bắt lỗi' if expect_fail else 'sạch', bool(got) == expect_fail, got[:2]))


def bad(x, *muc):
    L = x['loi'] + (x.get('thieu') or [])
    return [y for y in L if not muc or any(y.startswith(f'({m})') for m in muc)]


def thieu(x): return x['thieu'] if x.get('ket_qua') == 'THIẾU' else ['không phải THIẾU: ' + str(x.get('ket_qua'))]


# ================================================================ K-LAI
E0 = yaml.safe_load(open(os.path.join(EL, 'episode.yaml')))


def lai(E=None, **over):
    E = copy.deepcopy(E or E0)
    for k, v in over.items():
        if v is None: E['lai'].pop(k, None)
        else: E['lai'][k] = v
    return LA.check(E, None, EL, None)


def tmpf(name, obj, jsonl=False):
    p = os.path.join(TMP, name)
    with open(p, 'w') as f:
        if jsonl: f.write(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in obj))
        elif name.endswith('.yaml'): f.write(yaml.safe_dump(obj, allow_unicode=True))
        else: json.dump(obj, f, ensure_ascii=False)
    return p


FR = [json.loads(l) for l in open(os.path.join(EL, 'log-khung.jsonl'))]
TX = json.load(open(os.path.join(EL, 'log-chu.json'))); KD = json.load(open(os.path.join(EL, 'kiem-du-kien.json')))
GA = [json.loads(l) for l in open(os.path.join(EL, 'goi-api.jsonl'))]; DY = yaml.safe_load(open(os.path.join(EL, 'duyet.yaml')))
x = lai(); [case(k, 'fixture ep-lai (shot LAI 6 s / 60 s, nhãn 38 px, sổ đủ, ngoại lệ X1 có duyệt)', bad(x[k]), False) for k in LA.ROWS]
case('K-LAI-2', 'nhãn đúng 38,0 px → nêu tên sát ngưỡng', [] if any('38.0' in s for s in x['K-LAI-2']['sat_nguong']) else ['không nêu'], False)
E1 = copy.deepcopy(E0); E1.pop('lai'); E1['segments'][1]['shots'][0].pop('ai_image')
case('K-LAI', 'tập không có khối lai: và không shot AI → KHÔNG ÁP', [k for k, v in LA.check(E1, None, EL).items() if v['ket_qua'] != 'KHÔNG ÁP'], False)
E2 = copy.deepcopy(E0); E2.pop('lai')
case('K-LAI', 'shot khai ai_image nhưng không có khối lai: → THIẾU (mọi hàng)', [k for k, v in LA.check(E2, None, EL).items() if v['ket_qua'] != 'THIẾU'], False)
# K-LAI-1
F1 = [dict(f, ai_image=f['f'] >= 500 and f['f'] < 864, nhan_phuong_phap=500 <= f['f'] < 864) for f in FR]
case('K-LAI-1', 'AI 15,2 s / 60 s = 25,3 % > 20 %', bad(lai(log_khung=tmpf('f1.jsonl', F1, True))['K-LAI-1']), True)
F1b = [dict(f, ai_texture=600 <= f['f'] < 720) for f in FR]
case('K-LAI-1', 'ai_texture cũng tính: 6 s + 5 s = 18,3 % ≤ 20 % → ĐẠT', bad(lai(log_khung=tmpf('f1b.jsonl', F1b, True))['K-LAI-1']), False)
F1c = [dict(f, ai_texture=583 <= f['f'] < 720) for f in FR]
r1c = lai(log_khung=tmpf('f1c.jsonl', F1c, True))['K-LAI-1']
case('K-LAI-1', f"ai 11,7 s = {100 * r1c['ty_le']:.2f} % (±5 % quanh 20 %) → ĐẠT, nêu tên", bad(r1c) or ([] if r1c['sat_nguong'] else ['không nêu']), False)
F1d = [f for f in FR if f['f'] % 2 == 0]
case('K-LAI-1', 'log thưa (mỗi 2 khung) → THIẾU', thieu(lai(log_khung=tmpf('f1d.jsonl', F1d, True))['K-LAI-1']), True)
# K-LAI-2
F2 = [dict(f, nhan_phuong_phap=f['nhan_phuong_phap'] and f['f'] < 850) for f in FR]
case('K-LAI-2', 'nhãn tắt 14 khung cuối shot LAI (a)', bad(lai(log_khung=tmpf('f2.jsonl', F2, True))['K-LAI-2'], 'a'), True)
T2 = copy.deepcopy(TX); [it.update(px1080=30.0) for fr in T2 for it in fr['text'] if it['role'] == 'method']
case('K-LAI-2', 'nhãn 30 px < 38 px (b)', bad(lai(log_chu=tmpf('t2.json', T2))['K-LAI-2'], 'b'), True)
T3 = copy.deepcopy(TX); [it.update(box=[1200, 40, 1880, 86]) for fr in T3 for it in fr['text'] if it['role'] == 'method']
case('K-LAI-2', 'nhãn ở góc trên phải (b)', bad(lai(log_chu=tmpf('t3.json', T3))['K-LAI-2'], 'b'), True)
T4 = copy.deepcopy(TX); [fr.update(text=[i for i in fr['text'] if i['role'] != 'method']) for fr in T4 if fr['f'] >= 816]
case('K-LAI-2', 'nhãn mất ở 4 mẫu cuối shot (log chữ) (b)', bad(lai(log_chu=tmpf('t4.json', T4))['K-LAI-2'], 'b'), True)
T5 = copy.deepcopy(TX); [it.update(s='Surface detail AI-generated', px1080=40) for fr in T5 for it in fr['text'] if it['role'] == 'method']
case('K-LAI-2', 'chữ nhãn khác ("AI-generated") → không nhận (b)', bad(lai(log_chu=tmpf('t5.json', T5))['K-LAI-2'], 'b'), True)
F6 = [dict(f, shot='b/0') if 700 <= f['f'] < 720 else f for f in FR]
case('K-LAI-2', '"suốt shot": 20 khung đầu shot b/0 không AI và không nhãn → (a)', bad(lai(log_khung=tmpf('f6.jsonl', F6, True))['K-LAI-2'], 'a'), True)
case('K-LAI-2', 'không có log chữ → THIẾU', thieu(lai(log_chu=None)['K-LAI-2']), True)
# K-LAI-3
def kd(fn):
    k = copy.deepcopy(KD); fn(k); return tmpf('kd.json', k)
case('K-LAI-3', 'loi_chac_cuoi = 1 (b)', bad(lai(kiem_du_kien=kd(lambda k: k['khung_neo']['k1782'].update(loi_chac_cuoi=1)))['K-LAI-3'], 'b'), True)
case('K-LAI-3', 'nghi_van_con_lai = 1 (c)', bad(lai(kiem_du_kien=kd(lambda k: k['khung_neo']['k1782'].update(nghi_van_con_lai=1)))['K-LAI-3'], 'c'), True)
case('K-LAI-3', 'sổ tổng ghi nghi_van_cuoi_nhe 1, mục tấm ghi 0 (c)', bad(lai(kiem_du_kien=kd(lambda k: k['tong'].update(nghi_van_cuoi_nhe=1)))['K-LAI-3'], 'c'), True)
case('K-LAI-3', 'ngoại lệ X1 không có duyệt (d)', bad(lai(duyet=None)['K-LAI-3'], 'd'), True)
case('K-LAI-3', 'duyệt ghi email người ký (d)', bad(lai(duyet=tmpf('dy.yaml', [dict(DY[0], nguoi_ky='chu.du.an@example.com')]))['K-LAI-3'], 'd'), True)
case('K-LAI-3', 'duyệt vai phien_p (d)', bad(lai(duyet=tmpf('dy2.yaml', [dict(DY[0], vai='phien_p')]))['K-LAI-3'], 'd'), True)
case('K-LAI-3', 'duyệt trong chính kiem-du-kien (ngoai_le_duyet) → ĐẠT', bad(lai(duyet=None, kiem_du_kien=kd(lambda k: k['khung_neo']['k1782'].update(ngoai_le_duyet=DY)))['K-LAI-3']), False)
case('K-LAI-3', 'tấm dùng không có trong sổ goi-api (a)', bad(lai(kiem_du_kien=kd(lambda k: k['khung_neo']['k1782'].update(tam_C_dung='c-khac.png')))['K-LAI-3'], 'a'), True)
case('K-LAI-3', 'bằng chứng trỏ kiem-mu/ (e)', bad(lai(kiem_du_kien=kd(lambda k: k.update(bang_chung='reports/pt2/kiem-mu/score.json')))['K-LAI-3'], 'e'), True)
case('K-LAI-3', 'cach_kiem "dùng chấm mù 3 người" (e)', bad(lai(kiem_du_kien=kd(lambda k: k.update(cach_kiem='dùng chấm mù 3 người để xác nhận')))['K-LAI-3'], 'e'), True)
case('K-LAI-3', 'không có kiem-du-kien → THIẾU', thieu(lai(kiem_du_kien=None)['K-LAI-3']), True)
# K-LAI-4
BV = os.path.join(EL, 'bao-ve'); A = cv2.imread(os.path.join(BV, 'a.png')); L0 = cv2.imread(os.path.join(BV, 'lai.png')); M = cv2.imread(os.path.join(BV, 'mat-na.png'), 0)
L1 = L0.copy(); L1[M > 127] = np.clip(L1[M > 127].astype(int) + 2, 0, 255).astype(np.uint8); cv2.imwrite(os.path.join(TMP, 'lai2.png'), L1)
bv = lambda **k: [dict(dict(lai=os.path.join(BV, 'lai.png'), a=os.path.join(BV, 'a.png'), mat_na=os.path.join(BV, 'mat-na.png'), bat_buoc=os.path.join(BV, 'bat-buoc.png')), **k)]
case('K-LAI-4', 'vùng bảo vệ lệch +2/255 (a)', bad(lai(bao_ve=bv(lai=os.path.join(TMP, 'lai2.png')))['K-LAI-4'], 'a'), True)
L3 = L0.copy(); L3[M > 127] = np.clip(L3[M > 127].astype(int) + (np.arange((M > 127).sum())[:, None] % 100 < 97), 0, 255).astype(np.uint8); cv2.imwrite(os.path.join(TMP, 'lai3.png'), L3)
r4 = lai(bao_ve=bv(lai=os.path.join(TMP, 'lai3.png')))['K-LAI-4']
case('K-LAI-4', f"lệch 1 mức ở 97 % điểm ảnh: TB {r4['val'].split(':')[1].split('/')[0].strip()}/255 < 1 → ĐẠT, nêu tên sát ngưỡng", bad(r4) or ([] if r4['sat_nguong'] else ['không nêu']), False)
cv2.imwrite(os.path.join(TMP, 'lai.jpg'), L0)
case('K-LAI-4', 'khung LAI là JPEG → (a)', bad(lai(bao_ve=bv(lai=os.path.join(TMP, 'lai.jpg')))['K-LAI-4'], 'a'), True)
BB = np.zeros_like(M); BB[150:, :40] = 255; cv2.imwrite(os.path.join(TMP, 'bb.png'), BB)
case('K-LAI-4', 'vùng bắt buộc (cờ) ngoài mặt nạ bảo vệ (b)', bad(lai(bao_ve=bv(bat_buoc=os.path.join(TMP, 'bb.png')))['K-LAI-4'], 'b'), True)
case('K-LAI-4', 'không có bao_ve → THIẾU', thieu(lai(bao_ve=None)['K-LAI-4']), True)
# K-LAI-5
def ga(rows): return tmpf('ga.jsonl', rows, True)
k2 = copy.deepcopy(KD); k2['khung_neo']['k1782b'] = dict(tam_C_dung='c-1782-d2.png', loi_chac_cuoi=0, nghi_van_con_lai=0, duoc_dung=True)
case('K-LAI-5', 'hai tấm C dùng cho cùng khung neo × mốc (a)', bad(lai(kiem_du_kien=tmpf('k2.json', k2))['K-LAI-5'], 'a'), True)
G4 = GA + [dict(GA[1], lan_thu=3, file='c3.png', sha256='c' * 64), dict(GA[1], lan_thu=4, file='c4.png', sha256='d' * 64)]
case('K-LAI-5', '4 lệnh sinh thành công (3 lần sinh lại) (b)', bad(lai(goi_api=ga(G4))['K-LAI-5'], 'b'), True)
G5 = GA + [dict(GA[1], lan_thu=3, http=502, file=None, sha256=None)]
case('K-LAI-5', 'lệnh lỗi đường truyền 502 không tính lần sinh → ĐẠT', bad(lai(goi_api=ga(G5))['K-LAI-5']), False)
G6 = [dict(g, input={'pass': 'n'}) if i == 1 else g for i, g in enumerate(GA)]
case('K-LAI-5', 'sinh C từ lượt đêm "n" (c)', bad(lai(goi_api=ga(G6))['K-LAI-5'], 'c'), True)
dA = cv2.imread(os.path.join(EL, 'dem', 'a.png')); cv2.imwrite(os.path.join(TMP, 'dem-sang.png'), np.clip(dA.astype(int) * 1.6, 0, 255).astype(np.uint8))
case('K-LAI-5', 'đêm LAI sáng ≈ 2,4× A (d)', bad(lai(dem=[dict(lai=os.path.join(TMP, 'dem-sang.png'), a=os.path.join(EL, 'dem', 'a.png'))])['K-LAI-5'], 'd'), True)
case('K-LAI-5', 'không khai cặp đêm → THIẾU (d)', thieu(lai(dem=None)['K-LAI-5']), True)
case('K-LAI-5', 'khai dem: [] (tập không có đêm) → ĐẠT', bad(lai(dem=[])['K-LAI-5']), False)
# K-LAI-6
case('K-LAI-6', 'thiếu prompt', bad(lai(goi_api=ga([dict(GA[0], prompt='')] + GA[1:]))['K-LAI-6']), True)
case('K-LAI-6', 'prompt rút gọn < 40 ký tự', bad(lai(goi_api=ga([dict(GA[0], prompt='narrow lane 1782')] + GA[1:]))['K-LAI-6']), True)
case('K-LAI-6', 'thiếu c2pa + usage', bad(lai(goi_api=ga([{k: v for k, v in GA[0].items() if k not in ('c2pa', 'usage')}] + GA[1:]))['K-LAI-6']), True)
case('K-LAI-6', 'thiếu mask.pct_duoc_sua', bad(lai(goi_api=ga([dict(GA[0], mask={'quy_uoc': 'alpha 0'})] + GA[1:]))['K-LAI-6']), True)
case('K-LAI-6', 'usd là chuỗi', bad(lai(goi_api=ga([dict(GA[0], usd='0.06')] + GA[1:]))['K-LAI-6']), True)
case('K-LAI-6', 'lệnh 502 không ảnh: không đòi c2pa/file/usage → ĐẠT', bad(lai(goi_api=ga(GA + [{k: v for k, v in GA[1].items() if k not in ('c2pa', 'file', 'sha256', 'usage', 'model_resp')} | dict(http=502, lan_thu=3)]))['K-LAI-6']), False)
# K-LAI-B
hsv = np.zeros((360, 640, 3), np.uint8); hsv[..., 0] = 15; hsv[..., 1] = int(255 * 0.52); hsv[..., 2] = 190
os.makedirs(os.path.join(TMP, 'kl'), exist_ok=True); cv2.imwrite(os.path.join(TMP, 'kl', '00000.png'), cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR))
case('K-LAI-B', 'khung LAI bão hoà 0,52 > 0,40 (vàng cam đậm như PT2 1943)', bad(lai(khung_lai=os.path.join(TMP, 'kl'))['K-LAI-B']), True)
hsv[..., 1] = int(255 * 0.39); cv2.imwrite(os.path.join(TMP, 'kl', '00000.png'), cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)); rb = lai(khung_lai=os.path.join(TMP, 'kl'))['K-LAI-B']
case('K-LAI-B', 'bão hoà 0,39 → ĐẠT, nêu tên sát ngưỡng', bad(rb) or ([] if rb['sat_nguong'] else ['không nêu']), False)
# cấp
case('cap', 'K-LAI-1 lỗi → Chặn', cap112.cap('K-LAI-1', dict(loi=['x'], thieu=[]))[1], True)
case('cap', 'K-LAI-B lỗi → chỉ Cảnh báo (không Chặn)', cap112.cap('K-LAI-B', dict(loi=['x'], thieu=[]))[1], False)
case('cap', 'O2 / BC2 / BC3 / BC4 lỗi → chỉ Cảnh báo', sum((cap112.cap(k, dict(loi=['x'], thieu=['y']))[1] for k in ('O2', 'BC2', 'BC3', 'BC4')), []), False)
# PT2 thật
P2 = os.path.join(K, 'pt2')
EP2 = dict(id='pt2', segments=[dict(id='a', dur=20.0, shots=[])], lai=dict(log_khung='log-LAI-960x540.jsonl', kiem_du_kien='kiem-du-kien.json', goi_api='goi-api.jsonl'))
RP = LA.check(EP2, None, P2)
case('K-LAI-3', 'PT2 THẬT: W5 (công-xon 1943) chờ duyệt → (d)', bad(RP['K-LAI-3'], 'd'), True)
case('K-LAI-3', 'PT2 THẬT: sổ tổng "nghi_van_cuoi_nhe 1" (W3 sót ≈ 0,05 %) mà mục tấm ghi 0 → (c)', bad(RP['K-LAI-3'], 'c'), True)
case('K-LAI-5', 'PT2 THẬT: 1 tấm/khung neo, 2 + 1 lệnh sinh, lượt d2 → (a)–(c) ĐẠT', bad(RP['K-LAI-5'], 'a', 'b', 'c'), False)
case('K-LAI-6', 'PT2 THẬT: sổ goi-api đủ trường (3 lệnh, $0,1878, C2PA 3/3)', bad(RP['K-LAI-6']), False)
case('K-LAI-1', 'PT2 THẬT: đoạn thử 20 s toàn khung LAI = 100 % > 20 % (đúng: luật đo cấp tập)', bad(RP['K-LAI-1']), True)
case('K-LAI-2', 'PT2 THẬT: 480/480 khung nhan_phuong_phap nhưng không log chữ → THIẾU', thieu(RP['K-LAI-2']), True)

# ================================================================ O2 (bộ đệm; không gọi mạng)
OD = os.path.join(K, 'o2'); HOP = json.load(open(os.path.join(OD, 'hop-co.json'))); CA = json.load(open(os.path.join(OD, 'cache.json')))
API = '--api' in sys.argv
if API: CA = {}


def o2(nm, cache=None):
    return O2.soi_khung(os.path.join(OD, nm + '.jpg'), HOP[nm]['nam'], os.path.join(TMP, 'o2'), nm, 'Gibraltar', api=API, cache=CA if cache is None else cache)


def giao(a, b): return a and b and a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


Z = {nm: o2(nm) for nm in ('co1801-1782', 'co1707-1782', 'co1801-nho-1782', 'pt-c-1782-dau', 'pt-a-1782-trua')}
co = lambda z: [x for x in z['nghi_van'] if x['muc'] == 'co']
z = Z['co1801-1782']; h = HOP['co1801-1782']['hop']
case('O2', f"ảnh tổng hợp: cờ Union 1801 (cao 90 px) ở năm 1782 → bắt, hộp giao cờ thật {h}", [] if any(giao(x['toa_do_px'], h) for x in co(z)) else [f"không bắt: {z.get('loi') or z['nghi_van']}"], False)
case('O2', 'cờ 1801 @1782: bước 2 phóng to xác nhận "no" (chưa có năm 1782)', [] if any((x.get('xac_nhan') or {}).get('da_co') == 'no' for x in co(z)) else ['bước 2 không xác nhận'], False)
z = Z['co1707-1782']
case('O2', 'ảnh tổng hợp: cờ Union 1707 ở năm 1782 → KHÔNG báo (0 nghi vấn cờ, 0 nghi vấn giao vùng cờ)',
     (co(z) + [x for x in z['nghi_van'] if giao(x['toa_do_px'], HOP['co1707-1782']['hop'])]) or ([z['loi']] if z.get('loi') else []), False)
z = Z['co1801-nho-1782']; h = HOP['co1801-nho-1782']['hop']
case('O2', f"ảnh tổng hợp: cờ 1801 nhỏ (cao 32 px) @1782 → bắt", [] if any(giao(x['toa_do_px'], h) for x in co(z)) else ['không bắt'], False)
z = Z['pt-a-1782-trua']
case('O2', 'khung THẬT PT A 1782 (cờ 1707 ≈ 20×25 px; người chấm PT gán nhầm 1801): bước 1 báo nhầm, bước 2 phóng to hạ → 0 nghi vấn',
     co(z) or ([] if any((x.get('ly_do_ha') or '').startswith('phóng to') for x in z['ghi_chu']) else ['bước 2 không chạy']), False)
case('O2', 'không có trong bộ đệm + không --api → THIẾU (không gọi mạng, không ĐẠT)',
     thieu(O2.tong_hop([O2.soi_khung(os.path.join(OD, 'co1707-1782.jpg'), 1783, os.path.join(TMP, 'o2x'), 'x', '', api=False, cache={})])), True)
TOT = O2.tong_hop([dict(v, t=None) for v in Z.values()])
case('O2', 'hàng O2 trên 5 khung: có nghi vấn → lỗi (mức Cảnh báo), ghi chi phí/khung', TOT['loi'] if TOT.get('chi_phi_tb') else [], True)
case('O2', 'lấy mẫu 60 s / 5 s + neo 12,3 s → 13 mẫu, giữa cửa sổ', [] if O2.lay_mau(60, 5, [12.3]) == [2.5, 7.5, 12.3, 12.5, 17.5, 22.5, 27.5, 32.5, 37.5, 42.5, 47.5, 52.5, 57.5] else [str(O2.lay_mau(60, 5, [12.3]))], False)
p = O2.prompt_for('/x', 1782)
case('O2', 'đề bài cố định: đủ 8 mục + năm khung + 5 ảnh', [k for k, _ in O2.MUC if f'. {k} —' not in p] + ([] if p.count('1782') >= 3 and p.count('/x/o') == 4 else ['thiếu năm/ảnh']), False)
nv, gc = O2._chuan({'nghi_van': [{'muc': 'co', 'toa_do': [0.5, 0.5, 0.55, 0.6], 'do_tin': 0.9}, {'muc': 'den', 'toa_do': [0, 0, 0.1, 0.1], 'do_tin': 0.3}]})
case('O2', 'toạ độ 0–1 → px 1920×1080; tin 0,3 < 0,5 → ghi chú', [] if nv[0]['toa_do_px'] == [960, 540, 1056, 648] and len(gc) == 1 else [str(nv), str(gc)], False)
CPF = {k: v.get('cost_usd') for k, v in Z.items()}
INFO = [f"  O2 (thông tin, không tính ca) khung THẬT PT C 1782 (cờ 1801 ≈ 20×25 px — K nhìn 1080p cũng không thấy chéo đỏ): nghi vấn {len(Z['pt-c-1782-dau']['nghi_van'])}, ghi chú "
        f"{[(x['muc'], x['toa_do_px'], x.get('do_tin')) for x in Z['pt-c-1782-dau']['ghi_chu']]} → BỎ SÓT (giới hạn điểm ảnh, RULES-LL 1.15)",
        "  O2 chi phí/khung (bộ đệm lượt thật): " + ', '.join(f'{k} ${v:.4f}' for k, v in CPF.items() if v is not None) + f" · tổng ${sum(v for v in CPF.values() if v):.3f}"]

# ================================================================ BC2–BC4
BD = os.path.join(K, 'bc'); B0 = json.load(open(os.path.join(BD, 'bo-tl.json')))
bc_ = lambda B=None, base=BD: BC.check(B or copy.deepcopy(B0), base)
x = bc_(); [case(k, 'fixture bc (nội dung 62 %, nước + trống 20 %, khối 7,5–14 px, hero có vân + pháp tuyến 35°)', bad(x[k]), False) for k in ('BC2', 'BC3', 'BC4')]
MM = json.load(open(os.path.join(BD, 'noi-dung-mask.json')))
M2 = [dict(m, content_pct=42.0) if m['f'] < 120 else m for m in MM]; B2 = dict(copy.deepcopy(B0), mat_na=tmpf('m2.json', M2))
case('BC2', 'thành phố nội dung 42 % < 50 % (a)', bad(bc_(B2)['BC2'], 'a'), True)
M3 = [dict(m, nuoc_pct=30.0, co_trong_pct=10.0) if m['f'] < 120 else m for m in MM]; B3 = dict(copy.deepcopy(B0), mat_na=tmpf('m3.json', M3))
case('BC2', 'nước 30 % + cỏ trống 10 % = 40 % > 1/3 (b)', bad(bc_(B3)['BC2'], 'b'), True)
M4 = [{k: v for k, v in m.items() if k not in ('nuoc_pct', 'co_trong_pct')} for m in MM]; B4 = dict(copy.deepcopy(B0), mat_na=tmpf('m4.json', M4))
case('BC2', 'mặt nạ không có nuoc_pct/co_trong_pct → (b) THIẾU', [y for y in bc_(B4)['BC2']['thieu'] if y.startswith('(b)')], True)
B5 = dict(copy.deepcopy(B0), noi=[dict(t=[0.0, 10.0], noi='bien')])
case('BC2', 'không shot thanh_pho → KHÔNG ÁP', [] if bc_(B5)['BC2']['ket_qua'] == 'KHÔNG ÁP' else ['áp'], False)
VB = os.path.join(K, 'v5b2b'); BV5 = json.load(open(os.path.join(VB, 'bo-tl.json'))); RV = BC.check(copy.deepcopy(BV5), VB)
case('BC2', 'V5b-2b THẬT: phố 1782 (18–26 s) nội dung trung vị 18,3 % < 50 % (a)', bad(RV['BC2'], 'a'), True)
case('BC2', 'V5b-2b THẬT: orbit King\'s Bastion (5,6–12 s) nội dung 53,0 % → không lỗi (a) shot này', [y for y in bad(RV['BC2'], 'a') if '0:05.6' in y], False)
LV = json.load(open(os.path.join(BD, 'log-vat.json')))
LV2 = [dict(f, vat=[dict(v, h_px=4.0) if v['id'] == 't1' and 48 <= f['f'] < 84 else v for v in f['vat']]) for f in LV]
case('BC3', 'tàu t1 4 px trong 1,5 s (> 0,5 s) < 6 px', bad(bc_(dict(copy.deepcopy(B0), log_vat=tmpf('lv2.json', LV2)))['BC3']), True)
LV3 = [dict(f, vat=[dict(v, h_px=None, box=[100, 500, 120, 505]) if v['id'] == 'q1' else v for v in f['vat']]) for f in LV]
case('BC3', 'khối quân từ box 5 px (không h_px) → lỗi', bad(bc_(dict(copy.deepcopy(B0), log_vat=tmpf('lv3.json', LV3)))['BC3']), True)
LV4 = [dict(f, vat=[dict(v, hien=False) if v['id'] == 'q2' else v for v in f['vat']]) for f in LV]
case('BC3', 'khối < 6 px nhưng hien: false (ẩn trong khói) → không tính', bad(bc_(dict(copy.deepcopy(B0), log_vat=tmpf('lv4.json', LV4)))['BC3']), False)
case('BC3', 'không log_vat → THIẾU', thieu(bc_(dict(copy.deepcopy(B0), log_vat=None))['BC3']), True)
sys.path.insert(0, K); import make_fixtures as MF  # noqa: E402
HD = os.path.join(TMP, 'hero'); [os.makedirs(os.path.join(HD, d), exist_ok=True) for d in ('khung', 'mat-na', 'phap-tuyen')]
rng = np.random.default_rng(3)
for f in range(130, 190, 12):
    im, m, N = MF.hero_frame(rng, False)
    cv2.imwrite(os.path.join(HD, 'khung', f'{f:05d}.jpg'), im); cv2.imwrite(os.path.join(HD, 'mat-na', f'{f:05d}.png'), m); cv2.imwrite(os.path.join(HD, 'phap-tuyen', f'{f:05d}.png'), N)
BH = dict(copy.deepcopy(B0), hero_anh=dict(khung=os.path.join(HD, 'khung'), mat_na=os.path.join(HD, 'mat-na'), phap_tuyen=os.path.join(HD, 'phap-tuyen'), hero_id=7))
rh = bc_(BH)['BC4']
case('BC4', 'hero "tấm phẳng" màu trơn: chi tiết < 16 (a) + pháp tuyến 0° (b)', bad(rh, 'a') and bad(rh, 'b'), True)
for f in range(130, 190, 12):   # có vân màu nhưng hình học phẳng → chỉ (b)
    im, _, _ = MF.hero_frame(np.random.default_rng(f), True); cv2.imwrite(os.path.join(HD, 'khung', f'{f:05d}.jpg'), im)
rh2 = bc_(BH)['BC4']
case('BC4', 'hero dán vân trên mặt phẳng: chi tiết đạt nhưng pháp tuyến 0° < 10° (b)', bad(rh2, 'b') if not bad(rh2, 'a') else ['(a) cũng báo'], True)
G20 = os.path.join(FX, 'k1121', 'tl-gib20-v5b2a'); BG = json.load(open(os.path.join(G20, 'bo-tl.json'))); rg = BC.check(copy.deepcopy(BG), G20)['BC4']
case('BC4', f"gib20 V5b-2a THẬT (hero giao lộ 1941, 14 khung): {rg['val']} → (a) tấm phẳng (chỉ báo)", bad(rg, 'a'), True)
case('BC4', 'không hero_anh → THIẾU', thieu(bc_(dict(copy.deepcopy(B0), hero_anh=None))['BC4']), True)

# ================================================================ I8: Q37 + TL-Q1 (V5b-2b thật)
EV = yaml.safe_load(open(os.path.join(VB, 'episode.yaml'))); TLB = [(copy.deepcopy(BV5), VB)]
q0 = NH.q37(EV); q1 = NH.q37(EV, tl=TLB)
case('Q37', f"V5b-2b THẬT trước I8: {q0['val']} → (b) TRƯỢT", bad(q0, 'b'), True)
case('Q37', f"V5b-2b THẬT sau I8 (pha ramp/orbit/pin/crane/reveal + đồng hồ dừng 09:45): TB {q1['bien_co']['tb']} s → (b) ĐẠT", bad(q1, 'b'), False)
case('Q37', 'V5b-2b sau I8: 7 biến cố cảnh tl (6 pha + 1 đồng hồ dừng), TB 3,33 s nêu tên sát ngưỡng 3,5', [] if len(q1['bien_co_tl']) == 7 and q1['sat_nguong'] else [str(len(q1['bien_co_tl'])), str(q1['sat_nguong'])], False)
case('Q37', 'V5b-2b sau I8: phố 1782 (18–26 s) không có biến cố → (c) 8,0 s vẫn TRƯỢT (không bịa mốc)', bad(q1, 'c'), True)
case('Q37', 'đồng hồ cảnh eo đất chạy 1 phút/s (nhãn đứng ~1 s) KHÔNG tính là dừng', [x for x in q1['bien_co_tl'] if x[1] == 'c'], False)
case('Q37', 'biến cố đo không qua (a): (a) chỉ xét beats khai', [y for y in bad(q1, 'a') if 'tl' in y], False)
BNC = copy.deepcopy(BV5); CPG = json.load(gzip.open(os.path.join(VB, 'campath.json.gz')))
CP2 = copy.deepcopy(CPG); [f.pop('canh') for f in CP2['frames']]; BNC['campath'] = tmpf('cp-nocanh.json', CP2); BNC['log_chu'] = os.path.join(VB, 'log-chu.json')
case('Q37', 'campath không có canh (gib20 cũ) → không ánh xạ, không thêm biến cố', NH.q37(EV, tl=[(BNC, VB)])['bien_co_tl'], False)
CP3 = copy.deepcopy(CPG); CP3['shots'][0]['phases'] = [dict(k='orbit', t=[2.0, 4.0])]; B3_ = dict(copy.deepcopy(BV5), campath=tmpf('cp-ph.json', CP3))
qq = NH.q37(EV, tl=[(B3_, VB)])
case('Q37', 'campath.shots[].phases (khai pha theo giây cảnh) được dùng thay frames[].phase của cảnh đó', [] if [x[2] for x in qq['bien_co_tl'] if x[1] == 'a'] == ['tl:pha orbit', 'tl:đồng hồ dừng'] else [str(qq['bien_co_tl'])], False)
T2L5 = yaml.safe_load(gzip.open(os.path.join(FX, 'k113', 't2l5-episode.yaml.gz'))); TT2 = json.load(gzip.open(os.path.join(FX, 'k113', 't2l5-timeline.json.gz')))
a_, b_ = NH.q37(T2L5, TT2), NH.q37(T2L5, TT2, tl=[(copy.deepcopy(BG), G20)])
case('Q37', 'T2 L5 + bộ gib20: kết quả giống hệt khi không có bộ (luật cũ giữ nguyên)', [] if (a_['val'], a_['loi']) == (b_['val'], b_['loi']) else [b_['val']], False)
RT0 = QT.check(copy.deepcopy(BV5), VB)['TL-Q1']
case('TL-Q1', f"V5b-2b THẬT sau I8: {RT0['val']} → (a), (e) ĐẠT", RT0['muc']['a'] + RT0['muc']['e'], False)
case('TL-Q1', 'V5b-2b: (b) chữ đồng hồ 81,2 / 56 px = 1,45× ≥ 1,4× → ĐẠT', RT0['muc']['b'], False)
CP4 = copy.deepcopy(CPG); [f.update(phase='orbit') for f in CP4['frames'] if f['phase'] == 'pin']
RT1 = QT.check(dict(copy.deepcopy(BV5), campath=tmpf('cp-nopin.json', CP4)), VB)['TL-Q1']
case('TL-Q1', 'V5b-2b bỏ pha pin (như trước I8) → 0 mốc (e)', RT1['muc']['e'], True)
CP5 = copy.deepcopy(CP4)
for f in CP5['frames']:
    f['clock'] = '13 Sep 1782 · 09:45' if 178 <= f['f'] <= 220 else f"t{f['f'] // 4}"   # đồng hồ theo khung: chạy 1 nhãn/4 khung, dừng 43 khung
RT2 = QT.check(dict(copy.deepcopy(BV5), campath=tmpf('cp-clock.json', CP5)), VB)['TL-Q1']
case('TL-Q1', f"không pha pin, có đồng hồ theo khung dừng 1,79 s → mốc dừng giờ: {RT2['val']}", RT2['muc']['a'] + RT2['muc']['e'] or ([] if RT2['moc_gio'] else ['không có mốc giờ']), False)
CP6 = copy.deepcopy(CPG); [f.update(phase='pin') for f in CP6['frames'] if 150 <= f['f'] < 178]
RT3 = QT.check(dict(copy.deepcopy(BV5), campath=tmpf('cp-pin3.json', CP6)), VB)['TL-Q1']
case('TL-Q1', 'pha pin kéo dài 2,96 s → (a) ngoài 1,5–2,0 s', RT3['muc']['a'], True)
CP7 = copy.deepcopy(CPG); [f.update(phase='orbit') for f in CP7['frames'] if f['phase'] == 'pin' and f['f'] > 195]
RT4 = QT.check(dict(copy.deepcopy(BV5), campath=tmpf('cp-pin07.json', CP7)), VB)['TL-Q1']
case('TL-Q1', 'pha pin 0,75 s < 1,0 s → không là mốc (e)', RT4['muc']['e'], True)
for nm, bp in (('ams30', os.path.join(FX, 'k112', 'tl-ams30')), ('gib20 V5b-2a', G20)):
    BB_ = json.load(open(os.path.join(bp, 'bo-tl.json'))); rr = QT.check(BB_, bp)['TL-Q1']
    case('TL-Q1', f"{nm}: mốc dừng năm giữ nguyên, 0 mốc dừng giờ thêm (không có pha pin ngoài mốc năm) — {rr['val'][:60]}", rr['moc_gio'], False)

# ================================================================ kết quả
ok = all(x[3] for x in R)
by = {}
for x in R: by.setdefault(x[0], []).append(x)
miss = [k for k, v in by.items() if k not in ('cap', 'K-LAI') and not (any(y[2] == 'sạch' for y in v) and any(y[2] == 'bắt lỗi' for y in v))]
for rule, name, kind, good, got in R:
    print(f"{'OK ' if good else 'SAI'} [{rule}] ({kind}) {name}" + ('' if good else f'  → {got}'))
print('\n'.join(INFO))
print(f"\nselftest 1.15: {sum(1 for x in R if x[3])}/{len(R)} đúng kỳ vọng · {len(by)} nhóm · " + ', '.join(f'{k} {len(v)}' for k, v in by.items())
      + f" · luật thiếu ca đạt hoặc trượt: {', '.join(miss) or 'không'}")
shutil.rmtree(TMP, ignore_errors=True)
sys.exit(0 if ok and not miss else 1)
