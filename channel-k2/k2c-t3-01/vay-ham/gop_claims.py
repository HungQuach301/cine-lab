"""T3b · gộp claims của 3 gói tra nguồn (ngoài git, scratchpad) thành vay-ham/claims-vay-ham.json + ../claims-vay-ham.md.
Mã S001… theo thứ tự chương; 'id_goc' giữ mã gói. Kết quả kiểm độc lập câu trích (verify_quotes.py của phiên P) ghi ở 'kiem_doc_lap'.
Dùng: python3 -I gop_claims.py <a1.json> <a2.json> <a3.json> <kiem.json>"""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ORDER = ['so-lan-vay', 'chien-luoc', '1704', 'utrecht', 'eo-dat', 'boi-canh', 'ngay', 'chi-huy', 'hau-can', 'dan-do', 'pho-chay-1781',
         'tan-cong-1782', 'thuong-vong', 'duong-ham-1782', 'eo-dat-1930s', 'duong-bang', 'tbn', 'duong-ham-wwii', 'so-tan', 'wwii-can-cu']
TEN = {'so-lan-vay': 'Số lần bị vây', 'chien-luoc': 'Vì sao Rock có giá', '1704': '1704 — chiếm Rock', 'utrecht': 'Utrecht 1713, Điều X',
       'eo-dat': 'Eo đất, chiến tuyến, La Línea, hàng rào', 'boi-canh': 'Great Siege — bối cảnh, hiệp ước', 'ngay': 'Great Siege — ngày bắt đầu/kết thúc',
       'chi-huy': 'Great Siege — chỉ huy', 'hau-can': 'Great Siege — hậu cần (lương thực, thuốc súng, tiếp tế)', 'dan-do': 'Great Siege — đạn nung đỏ, lò',
       'pho-chay-1781': 'Great Siege — phố bị bắn cháy 1781', 'tan-cong-1782': 'Great Siege — tổng công kích, pin nổi 13/9/1782',
       'thuong-vong': 'Great Siege — quân số, thương vong cả cuộc vây', 'duong-ham-1782': 'Great Siege — đường hầm 1782, bệ pháo Koehler',
       'eo-dat-1930s': 'Eo đất trước sân bay', 'duong-bang': 'Đường băng 1934–1955–nay; lập trường hai phía', 'tbn': 'Tây Ban Nha trong Thế chiến II (Felix)',
       'duong-ham-wwii': 'Đường hầm Thế chiến II', 'so-tan': 'Sơ tán dân thường 1940', 'wwii-can-cu': 'Căn cứ Thế chiến II (Torch)'}
a = [json.load(open(p)) for p in sys.argv[1:4]]
kiem = json.load(open(sys.argv[4]))
allc = [c for d in a for c in d['claims']]
for i, c in enumerate(allc): c['_n'] = i
allc.sort(key=lambda c: (ORDER.index(c['nhom']), c['_n']))
for i, c in enumerate(allc, 1):
    c['id_goc'] = c.pop('id'); c['id'] = f'S{i:03d}'; c['kiem_doc_lap'] = kiem.get(c['id_goc'], '')
out = {'note': 'Claims vây hãm T3b (17/10/2026). Trích nguyên văn từ tệp tải bằng curl (ngoài git: /var/tmp/cine-out/t3b/a1–a3), SHA-256 ở file_sha256.',
       'claims': [{k: c.get(k) for k in ['id', 'id_goc', 'nhom', 'claim_en', 'trich_nguyen_van', 'lang', 'nguon', 'loai_nguon', 'url', 'file_sha256', 'vi_tri', 'as_of', 'phia', 'status', 'nhay_cam', 'ghi_chu', 'kiem_doc_lap']} for c in allc],
       'dem_so_lan_vay': a[0]['dem_so_lan_vay'], 'so_hai_phia': a[1]['so_hai_phia'], 'lich_su_kien': a[1]['lich_su_kien'],
       'so_do_duong_bang': a[2]['so_do_duong_bang'], 'duong_ham_wwii': a[2]['duong_ham'],
       'nguon_da_tai': a[0]['nguon_da_tai'] + a[1]['nguon_da_tai'] + a[2]['nguon_da_tai'],
       'khong_tim_duoc': {'a1': a[0]['khong_tim_duoc'], 'a2': a[1]['khong_tim_duoc'], 'a3': a[2]['khong_tim_duoc']}}
idmap = {c['id_goc']: c['id'] for c in out['claims']}
for k in ('lich_su_kien',):
    for e in out[k]: e['claim'] = idmap.get(e.get('claim'), e.get('claim'))
(HERE / 'claims-vay-ham.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
(HERE / 'idmap.json').write_text(json.dumps(idmap, indent=0) + '\n')

from collections import Counter
st = Counter(c['status'] for c in out['claims'])
L = ['# CLAIMS VÂY HÃM — T3b Gibraltar "vì sao ai cũng tranh giành Rock" (K2C-T3-01)', '',
     '> Phiên tiền kỳ T3b, 17/10/2026. Bổ sung cho `tienky/claims.json` (C01–C35, hiệp ước 2026 + kinh tế — giữ nguyên, không sửa).',
     '> Mọi câu trích là **nguyên văn** từ tệp tải bằng curl (ngoài git: `/var/tmp/cine-out/t3b/a1…a3/`), SHA-256 ở cột nguồn. Lỗi OCR giữ nguyên trong trích, chú giải ở "ghi chú".',
     '> **Kiểm độc lập** (phiên P, `verify_quotes.py` ngoài git): so lại mọi câu trích với văn bản tách từ tệp có đúng SHA. "khớp nguyên khối" = toàn câu có trong tệp (bỏ dấu câu/khoảng trắng, ſ/f); "khớp theo mảnh" = mọi mảnh trừ một mảnh do ngắt dòng/OCR → **đối chiếu ảnh trang trước khi đưa lên hình**.',
     '> Máy đọc: `vay-ham/claims-vay-ham.json` (cùng nội dung + bảng số hai phía, lịch sự kiện, số đo đường băng/đường hầm).', '',
     f'**Tổng: {len(out["claims"])} claim** — ' + ' · '.join(f'{k} {v}' for k, v in st.most_common()) +
     f' · kiểm độc lập: khớp nguyên khối {sum(1 for c in out["claims"] if c["kiem_doc_lap"].startswith("khớp nguyên"))}, khớp theo mảnh {sum(1 for c in out["claims"] if c["kiem_doc_lap"].startswith("khớp theo"))}.', '',
     '## 0. Số lần bị vây (bắt buộc kiểm)', '']
d = out['dem_so_lan_vay']
L += ['| Số | Nguồn | Cách đếm | Danh sách |', '|---|---|---|---|']
for x in d['cac_cach_dem']:
    L.append(f"| {x['so']} | {x['nguon']} | {x['cach_dem']} | {', '.join(x['danh_sach'])} |")
L += ['', f"**Khuyến nghị cho lời:** {d['khuyen_nghi']}", '', '## 0b. Số hai phía (Great Siege) — dùng trong lời theo cột "cách nói"', '',
      '| Chỉ số | Phía Anh | Phía Tây Ban Nha / Pháp | Cách nói |', '|---|---|---|---|']
for x in out['so_hai_phia']:
    L.append(f"| {x['chi_so']} | {x['anh']['so']} ({x['anh']['nguon']}) | {x['tbn_phap']['so']} ({x['tbn_phap']['nguon']}) | {x['cach_noi']} |")
L += ['', '## 0c. Lịch sự kiện (cho bộ đếm ngày/giờ M6)', '', '| Ngày | Sự kiện | Claim |', '|---|---|---|']
for e in out['lich_su_kien']: L.append(f"| {e['ngay']} | {e['su_kien']} | {e.get('claim','')} |")
dd = out['so_do_duong_bang']
L += ['', '## 0d. Số đo cho hero (đường băng, đường hầm)', '', '| Mốc | Chiều dài | Nguồn |', '|---|---|---|']
for m in dd['chieu_dai_cac_moc']: L.append(f"| {m['nam']} | {m.get('m')} m {('× ' + str(m['rong_m']) + ' m') if m.get('rong_m') else ''} ({m.get('goc', m.get('mo_ta',''))}) | {m['nguon']} |")
L.append(f"| lấn vịnh | {dd['lan_vinh_m']['gia_tri']} m ({dd['lan_vinh_m']['goc']}) | {dd['lan_vinh_m']['nguon']} — {dd['lan_vinh_m']['trang_thai']} |")
L.append(f"| diện tích lấn | — | {dd['dien_tich_ghi_chu']} |")
L.append(f"| vật liệu lấp | — | {dd['vat_lieu']} |")
dh = out['duong_ham_wwii']
for t in dh['tong_km']: L.append(f"| hầm (tổng) | {t['so']} {t['don_vi']} — {t['cach_dem']} | {t['nguon']} |")
for k, v in dh['kich_thuoc_3d'].items(): L.append(f'| hầm: {k} | {v} | |')
L.append(f"| hầm: sức chứa | {dh['suc_chua']['nguoi']}; thời gian: {dh['suc_chua']['thoi_gian']} | |")
L += ['', '## 1. Claims theo nhóm', '']
for g in ORDER:
    cs = [c for c in out['claims'] if c['nhom'] == g]
    if not cs: continue
    L += [f'### {TEN[g]}', '']
    for c in cs:
        L += [f"**{c['id']}** · {c['status']} · phía: {c['phia']} · nhạy cảm: {c['nhay_cam']} · as of: {c['as_of'] or 'đọc 2026-10-17'} · (gói: {c['id_goc']})",
              f"- Claim (EN): {c['claim_en']}",
              f"- Trích nguyên văn ({c['lang']}): > {c['trich_nguyen_van']}",
              f"- Nguồn: {c['nguon']} [{c['loai_nguon']}] · {c['vi_tri']} · {c['url']} · SHA-256 `{(c['file_sha256'] or '')[:16]}…`",
              f"- Kiểm độc lập: {c['kiem_doc_lap']}"]
        if c['ghi_chu']: L.append(f"- Ghi chú: {c['ghi_chu']}")
        L.append('')
L += ['## 2. Chưa tìm được / nguồn bị chặn', '']
for k, v in out['khong_tim_duoc'].items():
    for x in v: L.append(f'- ({k}) ' + (x if isinstance(x, str) else json.dumps(x, ensure_ascii=False)))
L += ['', '## 3. Nguồn đã tải (SHA-256; tệp ngoài git)', '', '| URL | SHA-256 | Ghi chú |', '|---|---|---|']
seen = set()
for n in out['nguon_da_tai']:
    if n['sha256'] in seen: continue
    seen.add(n['sha256']); L.append(f"| {n['url']} | `{n['sha256']}` | {n.get('note') or n.get('mo_ta') or ''} |")
(HERE.parent / 'claims-vay-ham.md').write_text('\n'.join(L) + '\n')
print(len(out['claims']), dict(st))
