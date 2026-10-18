"""T3 · gói TUYẾN · kiểm lại độc lập: mọi câu trích trong claims-tuyen.json (nguồn chính + đối chiếu) có trong tệp thô có ĐÚNG SHA-256.
Dùng: /opt/cine/bin/python -I channel-k2/k2c-t3-01/tuyen/verify_quotes_tuyen.py   (mã thoát 1 nếu có trích không khớp hoặc SHA lệch)"""
import hashlib, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import tim  # noqa: E402

d = json.loads((HERE / 'claims-tuyen.json').read_text())
files = {n['sha256']: Path(n['file']) for n in d['nguon_da_tai']}
bad, n = [], 0
for c in d['claims']:
    for s in [c] + c['nguon_doi_chieu']:
        n += 1
        f = files.get(s['file_sha256'])
        if f is None or not f.exists() or hashlib.sha256(f.read_bytes()).hexdigest() != s['file_sha256']:
            bad.append((c['id'], 'SHA', s['nguon'][:50])); continue
        ok, fr, L, pg = tim.locate(f, s['trich_nguyen_van'])
        if not ok: bad.append((c['id'], fr, s['trich_nguyen_van'][:60]))
print(f'trích đã kiểm: {n}; lỗi: {len(bad)}')
for b in bad: print('  LỖI', *b)
sys.exit(1 if bad else 0)
