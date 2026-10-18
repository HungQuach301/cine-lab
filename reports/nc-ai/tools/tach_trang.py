"""NC-AI · cắt trang nguyên văn theo bang-trang.json (ranh dòng dò bằng mắt). Kiểm SHA-256 tệp trước khi cắt.
Dùng: python3 -I tach_trang.py <bang-trang.json> <thu_muc_tep_tho> <thu_muc_ra>
Tệp thô đặt tên <nguon_id>.txt. Không sửa chữ nào."""
import sys, os, json, hashlib
bang, raw_dir, out = sys.argv[1:4]
B = json.load(open(bang)); os.makedirs(out, exist_ok=True); rep = []
for nid, m in B['nguon'].items():
    raw = open(os.path.join(raw_dir, nid + '.txt'), 'rb').read()
    sha = hashlib.sha256(raw).hexdigest(); ok = sha == m['sha256']
    if not ok: sys.exit(f'{nid}: SHA LỆCH {sha}')
    L = raw.decode('utf-8').split('\n')
    for pg, (a, b) in m['trang'].items():
        t = '\n'.join(L[a - 1:b]).strip() + '\n'
        open(os.path.join(out, f'{nid}-p{int(pg):03d}.txt'), 'w').write(t)
        rep.append({'nguon': nid, 'trang': pg, 'dong': [a, b], 'so_tu': len(t.split())})
print(json.dumps({'sha_khop': True, 'trang': rep}, ensure_ascii=False))
