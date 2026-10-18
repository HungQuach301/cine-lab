"""Khoá lời v4.1 · kiểm độc lập G003: tách chữ lại từ tệp thô (ngoài git /var/tmp/cine-out/t3-k41/raw/, đúng SHA), so mọi câu trích sau khi bỏ dấu/khoảng trắng và nối gạch ngắt dòng.
Dùng: /opt/cine/bin/python -I channel-k2/k2c-t3-01/khoa-loi/verify_g003.py"""
import hashlib, json, re, subprocess, unicodedata
from pathlib import Path
RAW = Path('/var/tmp/cine-out/t3-k41/raw'); HERE = Path(__file__).resolve().parent
F = {'5caf6820741488cc05ea44c9339f2e2c9d2efb60f9ef7749f9268adec4afc843': 'closure.bin', '80579430181af6a774728a91dedfe43290799bc55d00415157bb8c73aef240ab': 'ehu1336.bin',
     '383f723c5c1e34912f1fb595b605a7bf36763120b9be972ac576a079a1ced73d': 'ehu1338.bin', '89d34a4006a0d9801ad4306f3e376ab16b6f2ef642ec634f18a7d8856bfadcfc': 'aportes885.bin'}
def norm(t):
    t = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', t.replace('’', "'"))
    return re.sub(r'[^a-z0-9]', '', ''.join(c for c in unicodedata.normalize('NFD', t.lower()) if unicodedata.category(c) != 'Mn'))
c = next(x for x in json.loads((HERE.parent / 'g1/claims-g1.json').read_text())['claims'] if x['id'] == 'G003'); ok = True
for s in [c] + c['nguon_doi_chieu']:
    f = RAW / F[s['file_sha256']]; assert hashlib.sha256(f.read_bytes()).hexdigest() == s['file_sha256']
    txt = subprocess.run(['pdftotext', '-layout', str(f), '-'], capture_output=True, text=True).stdout
    hit = norm(s['trich_nguyen_van']) in norm(txt); ok &= hit; print('KHỚP' if hit else 'LỆCH', f.name, s['trich_nguyen_van'][:70])
raise SystemExit(0 if ok else 1)
