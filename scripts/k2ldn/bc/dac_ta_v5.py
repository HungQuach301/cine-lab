#!/opt/cine/bin/python
"""BAN-CUOI-T4-B1 · đặc tả kiểm v5 (ban-cuoi/dac-ta-v5/) = bản sao dac-ta-v4 (BAN-CUOI-T4-A; v4 KHÔNG sửa) + LOG KHUNG của bản dựng 1080p B1 cho MAY-19 / GOC-CAO:
  · shot HỒI 1/HỒI 3 đã dựng: log.json thật của render 1080p (ban-cuoi/dung/log-may/<tệp>.json.gz) → hệ cảnh (như mk_ep_v3.py: cam theo x = E − 532000, y = h, z = −(N − 180800); bản EN ở cam_en);
    KHOP: ghép -a/-b như mk_ep_v3.py (cắt tại thoi_gian[3] − 0,5 s); H1-15h2: khung 152…278 của máy H1-15h đánh số lại từ 0;
  · H2-10, H5-05b (máy v5, MAY-19 (a)) và M00 (VONG P1b): log TÍNH từ tệp máy (may_b1.py — không dựng);
  · shot chưa dựng (B2/B3): giữ log animatic v3 như v4.
Không đổi lời, thời lượng, thứ tự shot. Ghi danh sách nguồn log vào dac-ta-v5/nguon-log-v5.json.
  dac_ta_v5.py"""
import gzip, json, os, shutil
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BC = os.path.join(REPO, 'channel-k2/k2c-t4-02/ban-cuoi'); V4 = f'{BC}/dac-ta-v4'; V5 = f'{BC}/dac-ta-v5'; LG = f'{V5}/log-may'; os.makedirs(LG, exist_ok=True)
for f in os.listdir(V4):
    if os.path.isfile(f'{V4}/{f}') and not f.startswith('k2check'): shutil.copy(f'{V4}/{f}', f'{V5}/{f}')
y = open(f'{V5}/episode.yaml').read().replace('id: k2c-t4-02-dac-ta-v4', 'id: k2c-t4-02-dac-ta-v5').replace('title: London — T4 đặc tả v4 (BAN-CUOI-T4-A; chưa dựng — kiểm đặc tả)', 'title: London — T4 đặc tả v5 (BAN-CUOI-T4-B1; log khung 1080p HỒI 1 + HỒI 3)')
open(f'{V5}/episode.yaml', 'w').write(y)
sc = lambda e: [round(e[0] - 532000, 3), round(e[2], 3), round(-(e[1] - 180800), 3)]


def canh(L):
    if L.get('he_toa_do') == 'canh': return L
    for f in L['frames']: c = f['cam']; f['cam_en'] = dict(c); f['cam'] = dict(c, p=sc(c['p']), l=sc(c['l']))
    L['he_toa_do'] = 'canh'; L['goc_toa_do'] = [532000, 180800]; return L


def doc(p): return json.loads(gzip.open(p).read()) if p.endswith('.gz') else json.load(open(p))


LS = json.load(open(f'{V5}/log-shot.json')); NG = {}
DUNG = f'{BC}/dung/log-may'; TINH = {'H2-10': f'{BC}/may/b1/H2-10-v5-log-may.json.gz', 'H5-05b': f'{BC}/may/b1/H5-05b-v5-log-may.json.gz', 'M00': f'{BC}/may/b1/M00-log-may.json.gz'}
for s in LS:
    ma = s['ma']; L = None
    if s['cu_may'] == 'KHOP' and os.path.exists(f'{DUNG}/{ma}-a.json.gz') and os.path.exists(f'{DUNG}/{ma}-b.json.gz'):
        A, B = canh(doc(f'{DUNG}/{ma}-a.json.gz')), canh(doc(f'{DUNG}/{ma}-b.json.gz')); na = int(round((s['thoi_gian'][3] - 0.5) * 24))
        A['frames'] = A['frames'][:na] + [dict(f, f=na + i) for i, f in enumerate(B['frames'])]; L = A; NG[ma] = 'dựng 1080p B1 (-a + -b, cắt như mk_ep_v3)'
    elif os.path.exists(f'{DUNG}/{ma}.json.gz'):
        L = canh(doc(f'{DUNG}/{ma}.json.gz')); f0 = L['frames'][0]['f']
        if f0: L['frames'] = [dict(f, f=f['f'] - f0) for f in L['frames']]
        NG[ma] = 'dựng 1080p B1' + (f' (khung máy {f0}… đánh số lại từ 0)' if f0 else '')
    elif ma in TINH and os.path.exists(TINH[ma]):
        L = canh(doc(TINH[ma])); NG[ma] = 'tính từ tệp máy v5 (không dựng): ' + os.path.relpath(TINH[ma], BC)
    if L is not None:
        open(f'{LG}/{ma}.json', 'w').write(json.dumps(L)); s['log_may'] = f'log-may/{ma}.json'
    elif s.get('log_may'): NG[ma] = 'giữ log animatic v3 (chưa dựng ở B1)'
json.dump(LS, open(f'{V5}/log-shot.json', 'w'), ensure_ascii=False, indent=1)
json.dump(NG, open(f'{V5}/nguon-log-v5.json', 'w'), ensure_ascii=False, indent=1)
print({k: sum(1 for v in NG.values() if v.startswith(k)) for k in ('dựng', 'tính', 'giữ')})
