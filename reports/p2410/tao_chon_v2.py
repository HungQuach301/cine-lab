# P-2410: sinh channel-k2/k2c-t4-02/look/CHON-V2.json từ lựa chọn của chủ dự án (24/10 06:21 "Lấy cột theo khuyến nghị") + V5/V6 (24/10, "Duyệt V1–V7 … theo khuyến nghị").
import hashlib, json, os
R = os.path.dirname(os.path.abspath(__file__)) + '/../..'
def sha(p): return hashlib.sha256(open(os.path.join(R, p), 'rb').read()).hexdigest()
MAY = 'channel-k2/k2c-t4-02/look/may-v2'
KH = 'reports/look-t4-v2/khung'
P1 = [532330, 180250, 230]
chon = {'M1-rong': 'v2-3d', 'M1-trung': 'v2-3d', 'M2-ngay': 'v2-3d', 'M2-dem': 'v2-3d', 'M3-rong': 'v2-3d',
        'M3-trung': 'v2-3d', 'M4-rong': 'v2-openai', 'M4-trung': 'v2-3d'}
hang = []
for i, (h, c) in enumerate(chon.items(), 1):
    m = f'{MAY}/{h}.json'; d = json.load(open(os.path.join(R, m))); k = d['keys'][0]
    e = {'hang': i, 'khung': h, 'vai': d.get('vai'), 'cot': c, 'o_1080p': f'{KH}/{h}-{c}.jpg', 'o_1080p_sha256': sha(f'{KH}/{h}-{c}.jpg'),
         'may': m, 'may_sha256': sha(m), 'diem_may': k['p'], 'nhin': k['l'], 'fov_tep': k['fov'],
         'look': {'lut': d['look']['lut'], 'suong_sigma_per_m': d['look']['haze'][0], 'kieu': 'A + ấm kiểu C' if (h == 'M2-ngay' or h.startswith('M3')) else ('A + khói than dày kiểu B' if h == 'M2-dem' else 'A')},
         'p1': k['p'] == P1}
    if e['p1']:
        e['v5_fov_san_xuat'] = 36
        hep = f'{MAY}/{h}-hep.json'
        if os.path.exists(os.path.join(R, hep)): e['may_fov36'] = hep; e['may_fov36_sha256'] = sha(hep); e['o_fov36'] = f'{KH}/{h}-p1-hep36.jpg'
        else: e['may_fov36'] = None; e['ghi_chu_fov36'] = 'chưa có tệp máy fov 36° cho hàng này (LOOK-T4-V2 chỉ dựng M1-rong, M3-rong, M4-rong hẹp); sản xuất đặt fov 36° cùng vị trí/hướng'
    if c == 'v2-openai':
        e['tam_nen'] = {'cong_cu': 'OpenAI gpt-image-2.5-sunburst-2026-09-08 (edits, không mặt nạ, high)', 'tam': 'M4-rong-oai-l3',
                        'anh_ai': 'channel-k2/k2c-t4-02/ai/goc-v2/M4-rong-oai-l3-ai.jpg', 'anh_ai_sha256': sha('channel-k2/k2c-t4-02/ai/goc-v2/M4-rong-oai-l3-ai.jpg'),
                        'timelapse_may': f'{MAY}/tl-M4-rong.json', 'cong_i_v': 'ĐẠT (LOOK-T4-V2 §3)', 'so_ai': 'reports/look-t4-v2/so-ai.jsonl',
                        'luu_y': 'tấm thử dựng ở fov 50°; theo V5 (fov 36°) bản sản xuất phải làm lại tấm nền và qua lại cổng (i)–(v). Tấm nền chỉ cho cảnh 2026 ban ngày (V1 = d + b).'}
    hang.append(e)
out = {'tap': 'K2C-T4-02 London', 'vong': 'LOOK-T4-V2 (nhánh k2c-t4-02-look2 @c4079595)', 'ghi_boi': 'P-2410',
       'can_cu': ['24/10/2026 06:21 (Asia/Saigon) "1. Chọn phương án A+B theo khuyến nghị 2. Lấy cột theo khuyến nghị"',
                  '24/10/2026 (tin nhắn ngay trước lệnh P-2410) "Duyệt V1–V7 và K1174-D1…D6 theo khuyến nghị"',
                  '23/10/2026 23:27 "1. xác nhận look hợp nhất Quyết L2–L6 (gồm L5 = bỏ GPU sau khi xem clip M2): “theo khuyến nghị”"'],
       'phieu': 'reports/look-t4-v2/PHIEU-LOOK-V2.md', 'to_so': 'reports/look-t4-v2/to-so-v2.jpg', 'hang': hang,
       'V5': {'quyet': '(b) P1 fov 36° cùng vị trí/hướng', 'diem_may_P1': P1, 'nhin_P1': [532420, 180980, 15], 'fov_cu': 50, 'fov_moi': 36,
              'so_do': 'vòm St Paul\'s 46 px (fov 50°) → 67 px (fov 36°), ngưỡng ≥ 60 px (LOOK-T4-V2 §1); Monument/Tower vẫn ngoài khung P1',
              'kinh_thanh': '§14.7 Look T4; §19 (a) luật 3 (điểm máy xương sống)'},
       'V6': {'quyet': '(b) sương phối cảnh σ = 1/10 km (look.haze[0] = 1e-4 /m)', 'ap': 'mọi khung look A và ấm kiểu C (ngày 1666, 1940, 2026)',
              'ngoai_le': 'M2-dem (đêm cháy 1666, kiểu B) giữ sương σ 1/6 km + lớp khói than σ 1/4,2 km như LOOK-T4 B',
              'cu': 'σ 1/16 km (A gốc LOOK-T4)'}}
p = os.path.join(R, 'channel-k2/k2c-t4-02/look/CHON-V2.json')
json.dump(out, open(p, 'w'), ensure_ascii=False, indent=1); open(p, 'a').write('\n')
print('ghi', p, sha('channel-k2/k2c-t4-02/look/CHON-V2.json'))
