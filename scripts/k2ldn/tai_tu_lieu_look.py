#!/opt/cine/bin/python
"""LOOK-T4 · tải tư liệu MỚI cho look (Old St Paul's theo Dugdale 1658 — D6; St Paul's của Wren) + lưu bằng chứng giấy phép nguyên văn.
  tai_tu_lieu_look.py [id ...]
Dùng lại hàm tải của tai_tu_lieu.py (không sửa tệp đó). Gốc: $LDN_SRC (ngoài git; SHA trong licenses/SHA256-TU-LIEU-LOOK.txt).
Trong git: channel-k2/k2c-t4-02/licenses/<id>.json (nguyên văn nơi giữ) · channel-k2/k2c-t4-02/look/tu-lieu/<id>-<j>.jpg (bản thu ≤ 2400 px, ≤ 2 MB)."""
import datetime, hashlib, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tai_tu_lieu as T
TL = os.path.join(T.REPO, 'channel-k2/k2c-t4-02/look/tu-lieu'); os.makedirs(TL, exist_ok=True)
ITEMS = {
  'met-336039': (T.met, 336039, "Hollar, Saint Paul's, South side (Ecclesiae Cathedralis S. Pauli a Meridie Prospectus), Dugdale 1658", 'thấp'),
  'met-336038': (T.met, 336038, "Hollar, Saint Paul's from the South showing the Spire (trước 1561), Dugdale 1658", 'thấp'),
  'met-757299': (T.met, 757299, "Dugdale, The History of St. Paul's Cathedral in London (1658) — sách", 'thấp'),
}
def main(ids):
    today = datetime.date.today().isoformat()
    for k in ids or ITEMS:
        fn, arg, desc, risk = ITEMS[k]
        r = fn(arg); out = []
        for j, u in enumerate(r['img'][:6]):
            p = os.path.join(T.SRC, f'{k}-{j}.jpg')
            if not os.path.exists(p): b = T.get(u); open(p, 'wb').write(b); time.sleep(3)
            sha = hashlib.sha256(open(p, 'rb').read()).hexdigest(); prev = os.path.join(TL, f'{k}-{j}.jpg'); T.thu(p, prev)
            out.append({'url': u, 'tep': os.path.basename(p), 'bytes': os.path.getsize(p), 'sha256': sha, 'ban_thu_git': os.path.relpath(prev, T.REPO)})
        rec = {'id': k, 'mo_ta': desc, 'rui_ro': risk, 'trang': r['page'], 'giay_phep': r['license'], 'tieu_de': r['title'], 'nam': r['date'], 'tac_gia': r['artist'],
               'ngay_tai': today, 'anh': out, 'meta_nguyen_van': r['meta']}
        json.dump(rec, open(os.path.join(T.LIC, f'{k}.json'), 'w'), ensure_ascii=False, indent=1)
        print('OK', k, r['license'][:90], [o['bytes'] for o in out], flush=True)
    with open(os.path.join(T.LIC, 'SHA256-TU-LIEU-LOOK.txt'), 'w') as f:
        for k in ITEMS:
            p = os.path.join(T.LIC, f'{k}.json')
            if os.path.exists(p):
                for o in json.load(open(p))['anh']: f.write(f"{o['sha256']}  {o['tep']}  {o['url']}\n")
if __name__ == '__main__': main(sys.argv[1:])
