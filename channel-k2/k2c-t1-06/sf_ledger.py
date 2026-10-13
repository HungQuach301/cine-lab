#!/opt/cine/bin/python
"""K2C-T1-06 · chuẩn hoá sổ SOURCES-FOOTAGE.csv theo FOOTAGE.md §2 (13/10/2026) và điền timecode_dung từ timeline phim chính.
  sf_ledger.py [timeline.json]      (mặc định /var/tmp/cine-out/k2c-t1-06/timeline.json)
- timecode_dung: mọi shot của phim chính (không tính Short) có hero dùng tệp của dòng sổ (ảnh/trang văn bản qua opt.img/opt.page, footage qua p.clip);
  shot cùng dòng kề nhau (cách ≤ 1 khung) gộp thành một đoạn; dạng m:ss.xx-m:ss.xx, nối bằng ';'.
- url_tai, sha256 = tệp GỐC đã dùng khi render (ghim ở scripts/k2/k2v-assets.sha.json; footage: sha256 trong opt của hero).
- Dòng không có tệp media ngoài trong phim (trang văn bản dựng lại chữ; clip dự phòng không dùng) chuyển sang SOURCES-NGOAI-SO.csv kèm lý do."""
import csv, json, os, re, subprocess, sys, yaml
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(f'{H}/../..')
TL = sys.argv[1] if len(sys.argv) > 1 else '/var/tmp/cine-out/k2c-t1-06/timeline.json'
COLS = 'clip_id,url_trang,url_tai,ngay_tai_utc,giay_phep,yeu_cau_ghi_cong,sha256,timecode_dung,nguoi_nhan_dien,logo'.split(',')
PIN = json.load(open(f'{ROOT}/scripts/k2/k2v-assets.sha.json'))


def asset_of(img):
    b = os.path.basename(img); b = re.sub(r'-p\d+\.json$', '', b); return re.sub(r'\.(jpg|png|json)$', '', b)


def clip_of_asset(a):
    m = re.match(r'k2c106-loc-(det|fsa|habs)-(\d+)$', a)
    if m: return f'LOC-{m.group(1).upper()}-{m.group(2)}'
    return {'loc-det-07-tif': 'LOC-DET-07', 'loc-hoover-1928': 'WM-HOOVER-1928', 'loc-sutherland-1937': 'WM-SUTHERLAND-1937',
            'k2c106-px-7180335': 'PXP-7180335', 'sszea-1926-ia': 'DOC-SSZEA', 'usrep-272-365': 'DOC-EUCLID'}.get(a)


def pin_time(key):
    """thời điểm ghim SHA lần đầu (commit đưa khoá vào k2v-assets.sha.json), đổi sang UTC …Z"""
    out = subprocess.run(['git', '-C', ROOT, 'log', '--reverse', '--format=%ct', '-S', f'"{key}"', '--', 'scripts/k2/k2v-assets.sha.json'], capture_output=True, text=True).stdout.split()
    import datetime
    t = int(out[0]) if out else int(os.path.getmtime(f'{ROOT}/scripts/k2/k2v-assets.sha.json'))
    return datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def mmss(t):
    m, s = divmod(t, 60); return f'{int(m)}:{s:05.2f}'


def main():
    EP = yaml.safe_load(open(f'{H}/episode.yaml')); HE = EP['heroes']; T = json.load(open(TL))
    use = {}; asset = {}
    for sg in T['segments']:
        for sh in sg['shots']:
            p = sh.get('p') or {}; cid = p.get('clip')
            if not cid:
                o = (HE.get(p.get('hero')) or {}).get('opt', {}); src = o.get('img') or o.get('page')
                if src: a = asset_of(src); cid = clip_of_asset(a); asset[cid] = a
            if cid: use.setdefault(cid, []).append([round(sg['t0'] + sh['t0'], 3), round(sg['t0'] + sh['t1'], 3)])
    rows = list(csv.DictReader(open(f'{H}/SOURCES-FOOTAGE.csv')))   # đọc cả sổ ngoài (lần chạy trước) để chạy lặp lại được
    if os.path.exists(f'{H}/SOURCES-NGOAI-SO.csv'): rows += [{k: r[k] for k in COLS} for r in csv.DictReader(open(f'{H}/SOURCES-NGOAI-SO.csv'))]
    keep, out = [], []
    for r in rows:
        c = r['clip_id']
        if c not in use:
            out.append(dict(r, ly_do='Không có trong phim chính: ' + ('trang văn bản dựng lại chữ (textpage.py), không có tệp ảnh/quét nguồn ngoài; trích dẫn ghi ở RIGHTS.md' if c.startswith('DOC-') else 'tệp dự phòng (clip/ảnh), không dùng trong bản cuối')))
            continue
        segs = sorted(use[c]); mg = [segs[0]]
        for a, b in segs[1:]:
            if a - mg[-1][1] <= 1 / 24 + 1e-6: mg[-1][1] = max(mg[-1][1], b)
            else: mg.append([a, b])
        r['timecode_dung'] = ';'.join(f'{mmss(a)}-{mmss(b)}' for a, b in mg)
        a = asset.get(c)
        if a and a in PIN:
            r['url_tai'] = PIN[a]['url']; r['sha256'] = PIN[a]['sha256']
            if not r['ngay_tai_utc'].endswith('Z') or c.startswith('DOC-') or r['url_tai'].endswith('u.tif'): r['ngay_tai_utc'] = pin_time(a)
        keep.append(r)
    with open(f'{H}/SOURCES-FOOTAGE.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, COLS); w.writeheader(); [w.writerow({k: r[k] for k in COLS}) for r in keep]
    with open(f'{H}/SOURCES-NGOAI-SO.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, COLS + ['ly_do']); w.writeheader(); [w.writerow({k: r.get(k, '') for k in COLS + ['ly_do']}) for r in out]
    for r in keep: print(r['clip_id'], r['timecode_dung'])
    print('ngoài sổ:', [r['clip_id'] for r in out])


if __name__ == '__main__':
    main()
