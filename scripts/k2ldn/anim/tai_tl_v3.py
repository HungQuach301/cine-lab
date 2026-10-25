#!/opt/cine/bin/python -I
"""ANIMATIC-T4-V2 · việc 5 — tải ảnh/footage thật từ Wikimedia Commons (P6/P7 theo NC-T4: TU-LIEU-1940.md, FOOTAGE-2026.md) + lưu bằng chứng giấy phép (extmetadata nguyên văn, SHA).
Giãn cách khi 429 (Commons giới hạn IP proxy); UA nghiên cứu, không email. Không chỉnh nội dung ảnh (chỉ thu kích thước ≤ 2000 px để vào git ≤ 5 MB).
  tai_tl_v3.py <khoá> …   khoá: d6418 | c3"""
import hashlib, json, re, sys, time, urllib.parse, urllib.request, urllib.error
from pathlib import Path
R = Path(__file__).resolve().parents[3]; O = R / 'channel-k2/k2c-t4-02/animatic2/tu-lieu'; LIC = O / 'giay-phep'; GOC = Path('/var/tmp/anim/tl-goc'); GOC.mkdir(parents=True, exist_ok=True); LIC.mkdir(parents=True, exist_ok=True)
UA = 'CineLab-research (+https://github.com/HungQuach301/cine-lab)'; API = 'https://commons.wikimedia.org/w/api.php'
F = {'d6418': ('commons-iwm-d6418', 'File:Bomb Damage in London, England, January 1942 D6418.jpg', 'anh'),
     'c3': ('footage-h5-07a-goc', 'File:London Timelapse 4K.webm', 'video')}
EMAIL = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')


def get(u, tries=14):
    for k in range(tries):
        try: return urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA}), timeout=600).read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and k < tries - 1: w = min(600, 60 * (k + 1)); print(f'{e.code} — chờ {w} s', flush=True); time.sleep(w); continue
            raise


for key in sys.argv[1:]:
    ten, title, kind = F[key]
    q = {'action': 'query', 'titles': title, 'format': 'json', 'prop': 'imageinfo' + ('|videoinfo' if kind == 'video' else ''), 'iiprop': 'url|size|sha1|extmetadata|mime'}
    if kind == 'video': q.update(viprop='derivatives|url|size')
    J = json.loads(get(API + '?' + urllib.parse.urlencode(q))); pg = list(J['query']['pages'].values())[0]; ii = pg['imageinfo'][0]
    meta = {k: v.get('value') for k, v in ii['extmetadata'].items()}
    rec = {'khoa': key, 'title': title, 'trang': 'https://commons.wikimedia.org/wiki/' + urllib.parse.quote(title.replace(' ', '_')), 'url_goc': ii['url'], 'sha1_commons': ii.get('sha1'),
           'kich_thuoc': [ii.get('width'), ii.get('height')], 'giay_phep': meta.get('LicenseShortName'), 'usage_terms': meta.get('UsageTerms'), 'tac_gia': meta.get('Artist'), 'credit': meta.get('Credit'),
           'ngay': meta.get('DateTimeOriginal'), 'mo_ta': meta.get('ImageDescription'), 'license_url': meta.get('LicenseUrl'), 'ngay_doc': '2026-10-25', 'extmetadata': ii['extmetadata']}
    if kind == 'video':
        der = [d for d in pg.get('videoinfo', [{}])[0].get('derivatives', [])]; rec['derivatives'] = [{k: d.get(k) for k in ('src', 'type', 'width', 'height', 'transcodekey')} for d in der]
        pick = sorted([d for d in der if (d.get('height') or 0) <= 1080 and 'webm' in (d.get('type') or '')], key=lambda d: -(d.get('height') or 0))
        src = pick[0]['src'] if pick else ii['url']; b = get(src); p = GOC / (ten + '.webm'); p.write_bytes(b); rec['tai'] = {'src': src, 'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b), 'tep': str(p)}
    else:
        b = get(ii['url']); p = GOC / (ten + Path(ii['url']).suffix.lower()); p.write_bytes(b); rec['tai'] = {'src': ii['url'], 'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b), 'tep': str(p)}
        from PIL import Image
        im = Image.open(p).convert('RGB'); im.thumbnail((2000, 2000), Image.LANCZOS); q_ = O / f'{ten}.jpg'; im.save(q_, quality=90); rec['git'] = {'tep': str(q_.relative_to(R)), 'sha256': hashlib.sha256(q_.read_bytes()).hexdigest(), 'px': list(im.size)}
    s = EMAIL.sub('[email-đã-che]', json.dumps(rec, ensure_ascii=False, indent=1)); (LIC / f'{ten}.json').write_text(s)
    print(key, rec['giay_phep'], re.sub('<[^>]+>', '', str(rec['tac_gia']))[:80], rec['ngay'], rec['tai']['bytes']); time.sleep(5)
