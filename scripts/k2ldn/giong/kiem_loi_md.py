#!/opt/cine/bin/python
"""GIONG-T4 · sinh reports/giong-t4/KIEM-LOI.md từ reports/giong-t4/kiem-loi.json; KIỂM BẰNG MÁY mọi trích dẫn có trong tệp nguồn đã lưu
(reports/giong-t4/nguon/<mã>.txt hoặc reports/nc-n2p/nguon/<tệp> cho Pepys/Evelyn), so sau khi gộp khoảng trắng và chuẩn hoá nháy. Lệch → dừng."""
import json, re, sys
from pathlib import Path
R = Path(__file__).resolve().parents[3]; G = R / 'reports/giong-t4'
SO = {'pepys': R / 'reports/nc-n2p/nguon/pg4167.txt', 'evelyn': R / 'reports/nc-n2p/nguon/pg42081.txt', 'authorship': R / 'AUTHORSHIP.md'}
nz = lambda s: re.sub(r'\s+', ' ', s.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')).strip()
K = json.loads((G / 'kiem-loi.json').read_text()); SUA = {s['L']: s for s in json.loads((R / 'channel-k2/k2c-t4-02/khoa-loi/sua-v2.json').read_text())}
NHAP = {x['L']: x for x in json.loads((R / 'channel-k2/k2c-t4-02/khoa-loi/so-nhap-khoa.json').read_text())}
hong = []; dong = []
for k in K:
    nguon = []
    for n in k['nguon']:
        p = SO.get(n['ma'], G / 'nguon' / f"{n['ma']}.txt"); t = nz(p.read_text())
        if nz(n['trich']) not in t: hong.append((k['L'], n['ma'], n['trich'][:60]))
        dau = p.read_text().splitlines()[:2] if p.parent.name == 'nguon' and p.parent.parent.name == 'giong-t4' else []
        url = dau[0][2:] if dau else f'`{p.relative_to(R)}` (repo @c6a4772b)'
        ngay = re.search(r'đọc (\S+)', dau[1]).group(1) if dau else 'trong repo'
        nguon.append(f"{n['ten']} — {url} (đọc {ngay}) — *\"{n['trich']}\"* — **{n['bac']}**")
    s = SUA[k['L']]
    dong.append(f"| {k['L']} | {NHAP[k['L']]['nhap']} | {'<br>'.join(nguon)} | **{k['ket_luan']}**: {NHAP[k['L']]['khoa'] if k['ket_luan'] != 'GIỮ' else '(giữ nguyên)'} · {s['ma']} — {s['ly_do']} |")
if hong: sys.exit('TRÍCH KHÔNG KHỚP NGUỒN: ' + json.dumps(hong, ensure_ascii=False))
hdr = ['# KIỂM LỜI — 22 mục [cần kiểm] của LOI-NHAP-v1.md (GIONG-T4, 23–24/10/2026)', '',
       '> Sinh bằng `scripts/k2ldn/giong/kiem_loi_md.py` từ `kiem-loi.json`; **mọi trích dẫn đã được máy kiểm khớp nguyên văn** trong bản chữ của trang đã tải (`reports/giong-t4/nguon/<mã>.txt`: dòng đầu = URL, ngày đọc UTC, SHA-256 tệp gốc) hoặc Pepys/Evelyn trong `reports/nc-n2p/nguon/` (SHA ở LOI-NHAP-v1.md).',
       '> Bậc: **bậc 2** = văn bản thời đó (§12.2); **TC-cq** = thứ cấp của cơ quan có thẩm quyền (bảo tàng, nhà thờ, Corporation, lưu trữ, đại học); **TC-bc** = báo chí/hiệp hội. Thang 5 bậc §12.2 là thang dựng hình; với lời, câu dựa TC theo chuẩn kiểm chứng hiện hành (§3). Không thêm khẳng định mới ngoài nguồn.',
       '> Kết luận: **GIỮ** · **SỬA CHỮ** (ý giữ, chữ theo nguồn) · **BỎ VẾ** (bỏ phần không kiểm được) · **VIẾT LẠI AN TOÀN**. Không mục nào bỏ cả câu; không mục nào đổi nghĩa chính của đoạn.', '',
       '| L | Câu nháp | Nguồn (URL · ngày đọc · trích nguyên văn · bậc) | Kết luận → câu khoá |', '|---|---|---|---|']
(G / 'KIEM-LOI.md').write_text('\n'.join(hdr + dong) + '\n')
from collections import Counter
print(len(K), 'mục, trích khớp hết;', dict(Counter(k['ket_luan'] for k in K)))
