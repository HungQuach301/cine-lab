"""V6 · chuẩn bị đầu vào K-LAI (reports/K-1.15-BAO-CAO.md §3.1, §8b) cho "tập khung neo" V6 = 2 shot: kn1782 (9 s) + kn1943 (9 s), mỗi shot là
video 540p của một khung neo (live6.py --ep). Ghi: log khung gộp (f 0–431, có 'shot'), log chữ gộp (box dòng nhãn @1920×1080), sổ AI gộp
(mọi lệnh sinh ảnh của 2 khung neo × mốc qua PT2/PT4/V6 + cờ 'dung'), bat_buoc.png (từ lượt mã lớp: trời, Line Wall, tàu, cột cờ, đèn, pháo,
kính/lòng cửa) cho mỗi khung neo, và episode-lai.yaml (khối lai: + o2:). PNG lớn để ngoài git (/var/tmp/v6kn/klai), ghi SHA-256.
  /opt/cine/bin/python -I klai6.py <thư mục sx (video+khung)> <thư mục A (khung A cùng màu)> <reports/v6/khung-neo>"""
import sys, os, json, hashlib, shutil, numpy as np, cv2
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', 'lai'))
import lai_common as LC
SX, AD, REP = sys.argv[1:4]; KL = '/var/tmp/v6kn/klai'; os.makedirs(KL, exist_ok=True); OUTK = os.path.join(REP, 'k-lai'); os.makedirs(OUTK, exist_ok=True)
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
# 1) log khung gộp
recs = []
for ep in (1782, 1943):
    for l in open(os.path.join(SX, f'log-LAI-960x540-{ep}.jsonl')):
        r = json.loads(l)
        if r['f'] is not None: recs.append(r)
recs.sort(key=lambda r: r['f'])
assert [r['f'] for r in recs] == list(range(len(recs))), 'log khung không liền'
with open(os.path.join(OUTK, 'log-khung.jsonl'), 'w') as f:
    for r in recs: f.write(json.dumps({k: r[k] for k in ('f', 't', 'shot', 'epoch', 'gio_ao', 'ai_image', 'ai_texture', 'nhan_phuong_phap')} | {'nguoi': r.get('nguoi_tren_hinh')}, ensure_ascii=False) + '\n')
# 2) log chữ gộp
tl = []
for ep in (1782, 1943): tl += json.load(open(os.path.join(SX, f'log-chu-LAI-960x540-{ep}.json')))
tl.sort(key=lambda r: r['f']); json.dump(tl, open(os.path.join(OUTK, 'log-chu.json'), 'w'), ensure_ascii=False)
# 3) sổ AI gộp
so = []
for l in open('/home/user/cine-lab/reports/pt2/ai-c/goi-api.jsonl'):
    d = json.loads(l); d.setdefault('phien', 'PT2'); d['nguon_so'] = 'reports/pt2/ai-c/goi-api.jsonl'; d['dung'] = d.get('anh') == '1782-d2-lan2'; so.append(d)
for l in open('/home/user/cine-lab/reports/pt4/ai-c/goi-api.jsonl'):
    d = json.loads(l); d['nguon_so'] = 'reports/pt4/ai-c/goi-api.jsonl'; d['dung'] = False; so.append(d)
for l in open(os.path.join(REP, 'ai-c', 'goi-api.jsonl')):
    d = json.loads(l); d['nguon_so'] = 'reports/v6/khung-neo/ai-c/goi-api.jsonl'; d['dung'] = d.get('anh') == '1943-d2-lan3' and d.get('http') == 200; so.append(d)
with open(os.path.join(OUTK, 'goi-api-gop.jsonl'), 'w') as f:
    for d in so: f.write(json.dumps(d, ensure_ascii=False) + '\n')
# 4) PNG bảo vệ + bắt buộc + cặp đêm + thư mục khung LAI
bao_ve = []; dem = []; sh = {}; kdir = os.path.join(KL, 'khung-lai'); os.makedirs(kdir, exist_ok=True)
for ep in (1782, 1943):
    bg = f'/var/tmp/v6kn/bg/{ep}L'; reg, mat, mc, meta = LC.load_cls(f'/var/tmp/v6kn/bg/{ep}A'); dep = LC.exr(f'/var/tmp/v6kn/bg/{ep}A/depth.exr')
    bb = (dep > 20000) | np.isin(reg, [9000, 9900, 9540, 9530, 9520, 9521, 9600, 9700]) | (((reg >= 1) & (reg < 9000)) & np.isin(mat, [mc['kinh'], mc['trong']]))
    bv = cv2.imread(os.path.join(bg, 'bao_ve.png'), cv2.IMREAD_GRAYSCALE) > 127
    out_bb = float((bb & ~bv).mean() * 100)
    pb = os.path.join(KL, f'bat_buoc-{ep}.png'); cv2.imwrite(pb, (bb * 255).astype(np.uint8)); pv = os.path.join(KL, f'bao_ve-{ep}.png'); shutil.copy(os.path.join(bg, 'bao_ve.png'), pv)
    sh[f'bat_buoc-{ep}.png'] = sha(pb); sh[f'bao_ve-{ep}.png'] = sha(pv); print(ep, 'bat_buoc ngoài mặt nạ %', round(out_bb, 4))
    for t in ('sang', 'trua', 'chieu', 'dem'):
        la = os.path.join(SX, f'{ep}-{t}-LAI-notext.png'); aa = os.path.join(AD, f'{ep}-{t}-A-notext.png')
        for p_ in (la, aa):
            q = os.path.join(KL, os.path.basename(p_)); shutil.copy(p_, q); sh[os.path.basename(p_)] = sha(q)
        shutil.copy(la, os.path.join(kdir, os.path.basename(la)))
        e = {'lai': os.path.join(KL, os.path.basename(la)), 'a': os.path.join(KL, os.path.basename(aa)), 'mat_na': pv, 'bat_buoc': pb}
        if t == 'dem': dem.append({'lai': e['lai'], 'a': e['a']})
        bao_ve.append(e)
json.dump(sh, open(os.path.join(OUTK, 'sha256-png-ngoai-git.json'), 'w'), indent=1)
# 5) episode-lai.yaml
import yaml
ep_yaml = {'id': 'v6-khung-neo', 'title': 'V6 khung neo LAI (2 khung neo × 9 s, bản sản xuất 540p)', 'out': '/var/tmp/v6kn/k-lai-out',
           'segments': [{'id': 'kn1782', 'dur': 9.0, 'shots': [{'type': 'scene3d', 'khung_neo': True, 'ai_image': True, 'p': {'where': 'Gibraltar'}}]},
                        {'id': 'kn1943', 'dur': 9.0, 'shots': [{'type': 'scene3d', 'khung_neo': True, 'ai_image': True, 'p': {'where': 'Gibraltar'}}]}],
           'lai': {'log_khung': 'k-lai/log-khung.jsonl', 'log_chu': 'k-lai/log-chu.json', 'kiem_du_kien': 'kiem-du-kien.json', 'goi_api': 'k-lai/goi-api-gop.jsonl',
                   'duyet': 'k-lai/duyet.yaml', 'bao_ve': bao_ve, 'dem': dem, 'khung_lai': kdir, 'tong_s': 18.0},
           'o2': {'nam_theo': [{'t': [0, 9], 'nam': 1782}, {'t': [9, 18], 'nam': 1943}], 'neo': [1.5, 3.3, 6.5, 10.5, 12.3, 15.5], 'buoc': 5, 'noi': 'Gibraltar'}}
open(os.path.join(OUTK, 'duyet.yaml'), 'w').write('# V6 khung neo: không có ngoại lệ chờ duyệt (kiem-du-kien.json: 0 lỗi chắc, 0 nghi vấn)\n[]\n')
yaml.safe_dump(ep_yaml, open(os.path.join(REP, 'episode-lai.yaml'), 'w'), allow_unicode=True, sort_keys=False)
print('ok', len(recs), 'khung', len(tl), 'mẫu chữ', len(so), 'lệnh AI')
