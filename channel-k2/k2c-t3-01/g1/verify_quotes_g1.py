"""G1 T3 · kiểm câu trích của g1/claims-g1.json với tệp thô có đúng SHA (ngoài git: /var/tmp/cine-out/g1/raw).
Dùng: /opt/cine/bin/python -I channel-k2/k2c-t3-01/g1/verify_quotes_g1.py [thư mục thô]"""
import hashlib, html, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = Path(sys.argv[1] if len(sys.argv) > 1 else '/var/tmp/cine-out/g1/raw')


def text(p):
    b = p.read_bytes()
    s = b.decode('utf-8', 'replace') if p.suffix == '.json' else b.decode('latin-1')
    if p.suffix == '.json': s = json.dumps(json.loads(s), ensure_ascii=False)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s)))


def main():
    files = {hashlib.sha256(p.read_bytes()).hexdigest(): p for p in RAW.iterdir() if p.is_file()}
    ok = n = 0
    for c in json.loads((HERE / 'claims-g1.json').read_text())['claims']:
        for src in [c] + c.get('nguon_doi_chieu', []):
            n += 1; p = files.get(src['file_sha256'])
            hit = bool(p) and src['trich_nguyen_van'] in text(p)
            ok += hit
            print(c['id'], 'KHỚP' if hit else ('THIẾU TỆP' if not p else 'LỆCH'), src['file_sha256'][:12], src['trich_nguyen_van'][:60])
    print(f'{ok}/{n} câu trích khớp')
    return 0 if ok == n else 1


if __name__ == '__main__':
    sys.exit(main())
