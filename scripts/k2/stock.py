#!/opt/cine/bin/python
"""KÊNH 2 · tìm + tải footage/ảnh Pexels và Pixabay qua API (QUAN-TRI-RUI-RO.md §6). Không in khoá; khoá đọc từ môi trường:
  PEXELS_API_KEY (ảnh /v1/search, video /v1/videos/search), PIXABAY_API_KEY (ảnh /api/), PIXABAY_VIDEO_API_KEY (video /api/videos/; thiếu thì dùng PIXABAY_API_KEY).
Điều khoản API (đọc 12/10/2026): Pexels 200 yêu cầu/giờ, 20 000/tháng, hiện liên kết tới Pexels + ghi công tác giả khi có thể, không sao chép chức năng lõi;
Pixabay 100 yêu cầu/60 s, kết quả tìm phải cache 24 giờ, không hotlink lâu dài (tải về máy mình), hiện nguồn khi hiển thị kết quả tìm.
Giấy phép nội dung: §6.2 (không bán bản chưa sửa; người nhận diện không đặt vào thế xấu; Pixabay có logo/nhãn hiệu → không dùng thương mại).

  stock.py search <pexels|pixabay> <photo|video> "<từ khoá>" [--n 10]     in bảng kết quả (id, cỡ, thời lượng, tác giả, trang); cache 24 giờ
  stock.py get <pexels|pixabay> <photo|video> <id> --ep <thư mục tập> [--people co|khong] [--logo co|khong]
        tải bản lớn nhất ≤ 1080p qua CDN → /var/tmp/k2-footage/<tập>/<nguồn>-<id>.<đuôi>, SHA-256, thêm dòng vào <tập>/SOURCES-FOOTAGE.csv
  stock.py ping                                                           một lượt gọi mỗi khoá, chỉ in HTTP status
Người nhận diện/logo: người dùng phải xem clip và khai --people/--logo (máy không tự kết luận); 'co' thì ghi chú cách xử lý trong sổ.
"""
import csv, datetime, hashlib, json, os, sys, time, urllib.parse, urllib.request

CACHE = os.path.join(os.environ.get('K2V_CACHE', '/var/tmp/cine-out/k2v-cache'), 'stock-search')
MEDIA = '/var/tmp/k2-footage'
UA = 'cine-lab/1.0 (channel research)'
LIC = {'pexels': 'Pexels License https://www.pexels.com/license/', 'pixabay': 'Pixabay Content License https://pixabay.com/service/license-summary/'}


def key(name):
    v = os.environ.get(name)
    if not v: raise SystemExit(f'thiếu biến môi trường {name}')
    return v


def http(url, headers=None):
    req = urllib.request.Request(url, headers={'User-Agent': UA, **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=60) as r: return r.status, r.read()
    except urllib.error.HTTPError as e: return e.code, b''


def endpoint(src, kind, q, n=10, page=1):
    if src == 'pexels':
        base = 'https://api.pexels.com/v1/videos/search' if kind == 'video' else 'https://api.pexels.com/v1/search'
        return base + '?' + urllib.parse.urlencode({'query': q, 'per_page': n, 'page': page, 'orientation': 'landscape'}), {'Authorization': key('PEXELS_API_KEY')}
    k = os.environ.get('PIXABAY_VIDEO_API_KEY') or key('PIXABAY_API_KEY') if kind == 'video' else key('PIXABAY_API_KEY')
    base = 'https://pixabay.com/api/videos/' if kind == 'video' else 'https://pixabay.com/api/'
    prm = {'key': k, 'q': q[:100], 'per_page': max(3, n), 'page': page, 'safesearch': 'true'}
    if kind == 'photo': prm.update(image_type='photo', orientation='horizontal')
    return base + '?' + urllib.parse.urlencode(prm), {}


def search(src, kind, q, n=10):
    os.makedirs(CACHE, exist_ok=True)
    ck = os.path.join(CACHE, hashlib.sha1(json.dumps([src, kind, q, n]).encode()).hexdigest() + '.json')
    if os.path.exists(ck) and time.time() - os.path.getmtime(ck) < 24 * 3600: return json.load(open(ck))   # Pixabay: cache 24 giờ (áp chung)
    url, hd = endpoint(src, kind, q, n); st, body = http(url, hd)
    if st != 200: raise SystemExit(f'{src} {kind}: HTTP {st}')
    d = json.loads(body); json.dump(d, open(ck, 'w')); return d


def items(src, kind, d):
    out = []
    if src == 'pexels':
        for x in d.get('videos' if kind == 'video' else 'photos', []):
            if kind == 'video':
                fs = sorted([f for f in x['video_files'] if (f.get('height') or 0) <= 1080 and f.get('file_type') == 'video/mp4'], key=lambda f: -(f.get('height') or 0))
                out.append(dict(id=x['id'], page=x['url'], dl=fs[0]['link'] if fs else None, w=fs[0]['width'] if fs else 0, h=fs[0]['height'] if fs else 0, dur=x.get('duration'), author=x['user']['name']))
            else:
                out.append(dict(id=x['id'], page=x['url'], dl=x['src'].get('large2x') or x['src']['original'], w=x['width'], h=x['height'], dur=None, author=x.get('photographer')))
    else:
        for x in d.get('hits', []):
            if kind == 'video':
                v = next((x['videos'][k] for k in ('large', 'medium', 'small', 'tiny') if x['videos'].get(k, {}).get('url') and x['videos'][k].get('height', 0) <= 1080), x['videos'].get('medium'))
                out.append(dict(id=x['id'], page=x['pageURL'], dl=v['url'], w=v['width'], h=v['height'], dur=x.get('duration'), author=x.get('user')))
            else:
                out.append(dict(id=x['id'], page=x['pageURL'], dl=x.get('largeImageURL') or x['webformatURL'], w=x['imageWidth'], h=x['imageHeight'], dur=None, author=x.get('user')))
    return out


def get(src, kind, iid, ep, people='khong', logo='khong'):
    # tìm lại item theo id (Pexels có endpoint theo id; Pixabay dùng tham số id)
    if src == 'pexels':
        url = f'https://api.pexels.com/v1/videos/videos/{iid}' if kind == 'video' else f'https://api.pexels.com/v1/photos/{iid}'
        st, body = http(url, {'Authorization': key('PEXELS_API_KEY')}); d = {('videos' if kind == 'video' else 'photos'): [json.loads(body)]} if st == 200 else None
    else:
        u, _ = endpoint(src, kind, '', 3); u = u.replace('q=&', f'id={iid}&'); st, body = http(u); d = json.loads(body) if st == 200 else None
    if not d: raise SystemExit(f'{src} {kind} {iid}: HTTP {st}')
    it = items(src, kind, d)[0]; ext = '.mp4' if kind == 'video' else '.jpg'
    tep = os.path.basename(os.path.normpath(ep)); dst = os.path.join(MEDIA, tep, f'{src}-{iid}{ext}'); os.makedirs(os.path.dirname(dst), exist_ok=True)
    st, blob = http(it['dl'])
    if st != 200: raise SystemExit(f'tải CDN: HTTP {st}')
    open(dst, 'wb').write(blob); sha = hashlib.sha256(blob).hexdigest()
    sf = os.path.join(ep, 'SOURCES-FOOTAGE.csv'); new = not os.path.exists(sf)
    with open(sf, 'a', newline='') as f:
        w = csv.writer(f)
        if new: w.writerow(['clip_id', 'url_trang', 'url_tai', 'ngay_tai_utc', 'giay_phep', 'yeu_cau_ghi_cong', 'sha256', 'timecode_dung', 'nguoi_nhan_dien', 'logo'])
        w.writerow([f'{src}-{iid}', it['page'], it['dl'], datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), LIC[src],
                    f'không bắt buộc; ghi "{"Video" if kind == "video" else "Photo"} by {it["author"]} on {src.capitalize()}" trong mô tả', sha, '', people, logo])
    print(json.dumps(dict(file=dst, bytes=len(blob), sha256=sha, w=it['w'], h=it['h'], dur=it['dur'], author=it['author'], page=it['page']), ensure_ascii=False))


def ping():
    for name, url, hd in [('PEXELS_API_KEY ảnh', *endpoint('pexels', 'photo', 'steel', 1)), ('PEXELS_API_KEY video', *endpoint('pexels', 'video', 'steel', 1)),
                          ('PIXABAY_API_KEY ảnh', *endpoint('pixabay', 'photo', 'steel', 3)), ('PIXABAY_VIDEO_API_KEY video', *endpoint('pixabay', 'video', 'steel', 3))]:
        print(name, http(url, hd)[0])


if __name__ == '__main__':
    a = sys.argv; arg = lambda k, d=None: a[a.index('--' + k) + 1] if '--' + k in a else d
    if a[1] == 'ping': ping()
    elif a[1] == 'search':
        for it in items(a[2], a[3], search(a[2], a[3], a[4], int(arg('n', 10)))):
            print(f"{it['id']:>10}  {it['w']}×{it['h']}  {str(it['dur'] or ''):>4}s  {it['author'][:24]:<24} {it['page']}")
        print(f"Nguồn: {a[2].capitalize()} ({'https://www.pexels.com' if a[2] == 'pexels' else 'https://pixabay.com'})")
    elif a[1] == 'get': get(a[2], a[3], a[4], arg('ep'), arg('people', 'khong'), arg('logo', 'khong'))
    else: print(__doc__)
