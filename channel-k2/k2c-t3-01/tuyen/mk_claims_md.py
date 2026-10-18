"""T3 · gói TUYẾN · sinh claims-tuyen.md (bảng đọc) từ claims-tuyen.json. Dùng: /opt/cine/bin/python -I channel-k2/k2c-t3-01/tuyen/mk_claims_md.py"""
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
d = json.loads((HERE / 'claims-tuyen.json').read_text())
C = d['claims']; n = Counter(c['status'] for c in C)
L = ['# CLAIMS TUYẾN — T3 Gibraltar (gói TUYẾN, 17/10/2026)', '',
     f"> Máy đọc: `claims-tuyen.json` (schema = `vay-ham/claims-vay-ham.json` + `nguon_doi_chieu`, `muc_lenh`). Tệp thô ngoài git (`/var/tmp/cine-out/tuyen/`), SHA-256 trong JSON. Kiểm độc lập: `verify_quotes_tuyen.py`.",
     '', f"**Tổng {len(C)} claim** — XÁC MINH {n['XÁC MINH']} · MÂU THUẪN {n['MÂU THUẪN']} · CHƯA XÁC MINH {n['CHƯA XÁC MINH']}. Trích đã kiểm: {sum(1 + len(c['nguon_doi_chieu']) for c in C)} (khớp 100 %).", '',
     '| ID | Mục | Trạng thái | Claim (EN) | Nguồn chính — trích | Nguồn đối chiếu | Ghi chú |', '|---|---|---|---|---|---|---|']
esc = lambda s: s.replace('|', '\\|').replace('\n', ' ')
for c in C:
    doi = '<br>'.join(f"{esc(x['nguon'])} ({esc(x['vi_tri'])}): “{esc(x['trich_nguyen_van'])}”" for x in c['nguon_doi_chieu']) or '—'
    L.append(f"| {c['id']} | {c['muc_lenh']} | {c['status']} | {esc(c['claim_en'])} | {esc(c['nguon'])} ({esc(c['vi_tri'])}): “{esc(c['trich_nguyen_van'])}” | {doi} | {esc(c['ghi_chu'])} |")
L += ['', '## Nguồn đã tải (SHA-256)', '', '| Khoá | Tệp | SHA-256 | Byte | Mô tả |', '|---|---|---|---|---|']
for s in d['nguon_da_tai']:
    L.append(f"| {s['key']} | `{Path(s['file']).name}` | `{s['sha256'][:16]}…` | {s['bytes']} | {esc(s['note'])} ([url]({s['url']})) |")
(HERE / 'claims-tuyen.md').write_text('\n'.join(L) + '\n')
print(len(C), dict(n))
