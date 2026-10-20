"""NC-GPU · đóng gói dữ liệu cú lặn cho pod, KHỬ TRÙNG LẶP theo SHA-256 (các bản xuất mốc chung phần lớn bộ đệm: địa hình, cây…):
tệp duy nhất vào cas/<sha>, danh sách liên kết lien.txt (<đường> <sha>); pod: tar -x rồi `while read p h; do mkdir -p $(dirname $p); ln cas/$h $p; done < lien.txt`.
  python dive_pack.py <thư mục dive (exp/, lf/, cam.json)> <tệp tar ra>"""
import sys, os, hashlib, tarfile, json
D, OUT = sys.argv[1], sys.argv[2]; seen = {}; links = []; tot = 0; uniq = 0
with tarfile.open(OUT, 'w') as T:
    for r, _, fs in os.walk(D):
        for f in sorted(fs):
            p = os.path.join(r, f); rel = os.path.relpath(p, D)
            if rel.startswith('tmp'): continue
            h = hashlib.sha256(open(p, 'rb').read()).hexdigest(); n = os.path.getsize(p); tot += n
            if h not in seen: seen[h] = 1; uniq += n; T.add(p, arcname='cas/' + h)
            links.append(f'dive/{rel} {h}')
    lp = OUT + '.lien.txt'; open(lp, 'w').write('\n'.join(links) + '\n'); T.add(lp, arcname='lien.txt')
print(json.dumps({'tep': len(links), 'goc_MB': round(tot / 1e6, 1), 'duy_nhat_MB': round(uniq / 1e6, 1)}))
