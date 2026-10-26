#!/opt/cine/bin/python
"""K-1.17.9 · dựng fixture THẬT cỡ nhỏ cho checks/ll/selftest_k1179.py từ đầu vào A (@bc1693b5, CHỈ ĐỌC) — 640×360 (render/AI INTER_AREA, mặt nạ NEAREST),
câu trả lời thô của GPT (E-P9-ngay-l1-thap), toa-thap.json, 2 clip Omni 360p (nguyên tệp), log máy rút gọn (f, sun_el, cam.p, cam.l) của H1-08b, H1-16, H2-03b.
Ghi SHA-256 nguồn vào fixtures/k1179/NGUON.json."""
import hashlib, json, os, shutil, cv2
IN = '/var/tmp/k1179/in/channel-k2/k2c-t4-02'; O = '/home/user/cine-lab/checks/ll/fixtures/k1179'; os.makedirs(O, exist_ok=True)
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest(); NG = {}
E = f'{IN}/ban-cuoi/e'
for k, luot, mn, tag in (('E-P9-ngay', 'l1', 'matna-thap', 'p9'), ('E-P1-ngay', 'l2', 'matna-thap', 'p1')):
    for src, dst, it in ((f'{E}/tam/{k}/render.png', f'{tag}_render.png', cv2.INTER_AREA), (f'{E}/ai/{k}-{luot}.jpg', f'{tag}_ai.png', cv2.INTER_AREA),
                         (f'{E}/tam/{k}/{mn}.png', f'{tag}_matna.png', cv2.INTER_NEAREST), (f'{E}/tam/{k}/mat_na_ct-thap.png', f'{tag}_ct.png', cv2.INTER_NEAREST)):
        im = cv2.imread(src)
        if 'ai' in dst: im = cv2.resize(im, (1920, 1080), interpolation=cv2.INTER_AREA)   # như ghep_e_bc: AI 2560×1440 → 1080p rồi mới thu nhỏ
        cv2.imwrite(f'{O}/{dst}', cv2.resize(im, (640, 360), interpolation=it), [cv2.IMWRITE_PNG_COMPRESSION, 9]); NG[dst] = dict(nguon=src.replace(IN, 'channel-k2/k2c-t4-02'), sha256=sha(src))
    shutil.copy(f'{E}/tam/{k}/toa-thap.json', f'{O}/{tag}_toa.json'); NG[f'{tag}_toa.json'] = dict(nguon=f'channel-k2/k2c-t4-02/ban-cuoi/e/tam/{k}/toa-thap.json', sha256=sha(f'{E}/tam/{k}/toa-thap.json'))
g = f'{E}/kiem/E-P9-ngay-l1-thap/vision/E-P9-ngay-l1-thap-gpt.raw.txt'; t = open(g).read(); json.dump(json.loads(t[t.index('{'):t.rindex('}') + 1]), open(f'{O}/p9_gpt.json', 'w'), ensure_ascii=False, indent=0)
NG['p9_gpt.json'] = dict(nguon=g.replace(IN, 'channel-k2/k2c-t4-02'), sha256=sha(g))
for c in ('H3-05b-l1-360p', 'H1-15b-l1-360p'):
    p = f'{IN}/animatic2/omni/clip/{c}.mp4'; shutil.copy(p, f'{O}/{c}.mp4'); NG[f'{c}.mp4'] = dict(nguon=p.replace(IN, 'channel-k2/k2c-t4-02'), sha256=sha(p))
for s in ('H1-08b', 'H1-16', 'H2-03b'):
    p = f'{IN}/animatic2/log-may/{s}.json'; L = json.load(open(p))
    json.dump(dict(shot=dict(fps=L['shot']['fps']), frames=[dict(f=x['f'], sun_el=round(x['sun_el'], 4), year=x.get('year'), fire=x.get('fire'), cam=dict(p=x['cam']['p'], l=x['cam']['l'])) for x in L['frames']]),
              open(f'{O}/log-{s}.json', 'w'), separators=(',', ':'))
    NG[f'log-{s}.json'] = dict(nguon=p.replace(IN, 'channel-k2/k2c-t4-02') + ' (rút gọn: f, sun_el, year, fire, cam.p, cam.l)', sha256=sha(p))
json.dump(dict(goc='origin/claude/k2c-t4-02-final-a-0pb0bh @bc1693b5 (BAN-CUOI-T4-A)', tep=NG), open(f'{O}/NGUON.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(NG, ensure_ascii=False)[:300])
