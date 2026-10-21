#!/opt/cine/bin/python
"""P-2010b · việc 1 bước 1: tải audio lịch sử ElevenLabs (CHỈ GET, 0 ký tự) đúng 8 phần chương + 3 câu `issmus` đã chọn của KL42.
Chọn mục theo (bộ đếm trước → sau) ghi trong reports/kl42/bo-dem.jsonl + độ dài chữ + đầu chữ — không đoán: mỗi đích phải khớp đúng 1 mục, chữ lịch sử
phải bằng chữ KL42 đã gửi (thu.py tách phần + alias của từ điển tại commit thu; câu thay: thay.json `gui`). Bộ đếm đọc trước/sau.
→ $P_OUT/lich-su/<tên>.mp3, reports/p2010b/lich-su-tai.json"""
import hashlib, json, os, subprocess, sys, urllib.request
from pathlib import Path
H = Path(__file__).resolve().parent; R = H.parents[1]
OUT = Path(os.environ.get('P_OUT', '/var/tmp/cine-out/p2010b')) / 'lich-su'; OUT.mkdir(parents=True, exist_ok=True)
API = 'https://api.elevenlabs.io'; UA = 'CineLab-research (+https://github.com/HungQuach301/cine-lab)'


def get(path, accept='application/json'):
    req = urllib.request.Request(API + path, method='GET', headers={'Accept': accept, 'User-Agent': UA})
    r = urllib.request.urlopen(req, timeout=300); return r.read(), r.headers.get('Content-Type')


def counter(): return json.loads(get('/v1/user/subscription')[0])['character_count']


LS = json.loads((H / 'lich-su-g1-1910.json').read_text())['muc']
THAY = json.loads((R / 'reports/kl42/thay.json').read_text())
# đích: (tên, bộ đếm trước, độ dài chữ gửi, đầu chữ) — bộ đếm theo bo-dem.jsonl (chương 02 và 05 gửi 2 phần song song cùng mốc trước)
DICH = [('00-HOOK-p0', 136226, 589, 'Midnight at the Gibraltar frontier.'), ('01-ROCK-p0', 136485, 1740, 'Austria, England'),
        ('02-SIEGE-p0', 137251, 1737, 'Half a century later'), ('02-SIEGE-p1', 137251, 1180, 'Four days later'),
        ('03-NEUTRAL-p0', 138534, 1085, 'Which leaves a question'), ('04-RUNWAY-p0', 139011, 1472, 'Why build an airfield'),
        ('05-GATE-p0', 139659, 1812, 'After the war'), ('05-GATE-p1', 139659, 269, 'In seventeen thirty, Spain')]
for t in [t for t in THAY if t['chon']]:   # câu chọn: thứ tự trong thay.json ↔ lượt 2 của bo-dem (140793 → 140827 → 140844)
    DICH.append((f"01-thay-{t['shot']}-{t['i']}", None, len(t['gui']), t['gui']))
BD = [json.loads(l) for l in open(R / 'reports/kl42/bo-dem.jsonl')]
THU_LAI = [b for b in BD if b['luot'].startswith('thu lại')]
CHON_BD = [b['dem_truoc'] for b in THU_LAI[3:6]]   # lượt 2 = 3 dòng thứ 4–6 (gửi 78/38/128 = chữ `issmus`)
c0 = counter(); out = []
for k, (ten, dem, n, dau) in enumerate(DICH):
    if dem is None: dem = CHON_BD[k - 8]
    m = [x for x in LS if x['ky_tu_truoc'] == dem and len(x['text']) == n and x['text'].startswith(dau)]
    if len(m) != 1: print('KHÔNG XÁC ĐỊNH', ten, len(m)); out.append(dict(ten=ten, tim_thay=len(m))); continue
    m = m[0]; f = OUT / f'{ten}.mp3'
    if not f.exists():
        b, ct = get(f"/v1/history/{m['id']}/audio", 'audio/*'); f.write_bytes(b)
    else: ct = 'audio/mpeg (đã tải)'
    pr = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=format_name,duration,bit_rate:stream=codec_name,sample_rate,channels,bit_rate',
                                    '-of', 'json', str(f)], capture_output=True, text=True).stdout)
    out.append(dict(ten=ten, id=m['id'], luc=m['luc'], model=m['model'], ky_tu=len(m['text']), dem=[m['ky_tu_truoc'], m['ky_tu_sau']], settings=m['settings'],
                    text=m['text'], content_type=ct, byte=f.stat().st_size, sha256=hashlib.sha256(f.read_bytes()).hexdigest(),
                    codec=pr['streams'][0]['codec_name'], sr=int(pr['streams'][0]['sample_rate']), kenh=pr['streams'][0]['channels'],
                    kbps=round(int(pr['format']['bit_rate']) / 1000, 1), giay=round(float(pr['format']['duration']), 3)))
    print(ten, m['id'], m['luc'], out[-1]['codec'], out[-1]['sr'], out[-1]['kbps'], 'kb/s', out[-1]['giay'], 's', out[-1]['sha256'][:12], flush=True)
c1 = counter()
json.dump(dict(ghi='P-2010b: tải audio lịch sử ElevenLabs (GET /v1/history/{id}/audio), 0 ký tự', dem_truoc=c0, dem_sau=c1, muc=out),
          open(H / 'lich-su-tai.json', 'w'), ensure_ascii=False, indent=1)
print('bộ đếm', c0, '→', c1)
