"""GIONG-T4 · thư viện thu G1 cho T4 London (theo reports/kl42/kl_lib.py). Khoá do proxy gắn cho api.elevenlabs.io — không đọc, không in.
Không đưa email vào header/URL/payload; UA = CineLab-research. Cache theo băm (đã thu = 0 ký tự).
CHẶN cứng trước khi gửi nếu tổng ký tự gửi của phiên chạm 18 000 (lệnh GIONG-T4; mốc theo dõi 14 000).
Sổ AI (reports/giong-t4/so-ai.jsonl): mỗi lệnh gọi = model, giọng, thiết lập, seed, CHỮ GỬI NGUYÊN VĂN, SHA vào/ra, ký tự, ngữ cảnh, giá (trong gói Creator).
Bộ đếm tài khoản trước/sau mỗi lượt: reports/giong-t4/bo-dem.jsonl."""
import base64, hashlib, json, os, re, subprocess, sys, time, urllib.request
from pathlib import Path
R = Path(__file__).resolve().parents[3]; EP = R / 'channel-k2/k2c-t4-02'; G = R / 'reports/giong-t4'
OUT = Path(os.environ.get('GL_OUT', '/var/tmp/cine-out/giong-t4')); (OUT / 'raw').mkdir(parents=True, exist_ok=True)
API = 'https://api.elevenlabs.io'; UA = 'CineLab-research (+https://github.com/HungQuach301/cine-lab)'
G1 = 'VDLncRBHDjLHBqLhQ1Qt'; MODEL = 'eleven_multilingual_v2'
SET = dict(stability=0.5, similarity_boost=0.75, speed=1.03)   # bản 1.03-B (Kinh thánh §4 dòng âm thanh; như KL42)
SEED = 19102026                                               # seed lượt B GIỌNG-CHỐT, dùng ở KL42
CHAN, MOC = 18000, 14000
LOG, BODEM = G / 'so-ai.jsonl', G / 'bo-dem.jsonl'
TDP = EP / 'khoa-loi/phat-am/tu-dien.json'


def td():
    return json.loads(TDP.read_text())['muc'] if TDP.exists() else []


def alias(t, muc=None):
    for d in sorted(muc if muc is not None else td(), key=lambda x: -len(x['viet'])):
        t = re.sub(r'(?<![\w-])' + re.escape(d['viet']) + r'(?![\w])', d['doc'], t)
    return t


def call(path, body=None, timeout=300):
    req = urllib.request.Request(API + path, data=None if body is None else json.dumps(body).encode(), method='POST' if body is not None else 'GET',
                                 headers={'Content-Type': 'application/json', 'Accept': 'application/json', 'User-Agent': UA})
    return urllib.request.urlopen(req, timeout=timeout).read()


def counter(wait=0):
    if wait: time.sleep(wait)
    return json.loads(call('/v1/user/subscription'))['character_count']


def da_gui():
    return sum(json.loads(l).get('ky_tu', 0) for l in open(LOG) if l.strip()) if LOG.exists() else 0


def tts(text, tag, prev=None, nxt=None, seed=SEED, settings=None):
    """→ (mp3, alignment, ký tự gửi lần này). Ký tự gửi = len(text) (ngữ cảnh ghi riêng — KL42: không bị tính phí)."""
    s = dict(settings or SET)
    body = dict(text=text, model_id=MODEL, voice_settings=s, seed=seed)
    if prev: body['previous_text'] = prev
    if nxt: body['next_text'] = nxt
    key = hashlib.sha1(json.dumps([G1, body], sort_keys=True).encode()).hexdigest()[:16]
    mp3, al = OUT / 'raw' / f'{key}.mp3', OUT / 'raw' / f'{key}.align.json'
    if mp3.exists() and al.exists(): return str(mp3), json.loads(al.read_text()), 0
    if da_gui() + len(text) > CHAN: raise SystemExit(f'CHẶN: {da_gui()} + {len(text)} > {CHAN} ký tự gửi (lệnh GIONG-T4)')
    loi = []
    for k in range(3):
        try:
            r = json.loads(call(f'/v1/text-to-speech/{G1}/with-timestamps?output_format=mp3_44100_192', body)); break
        except Exception as e:   # cùng lỗi ≥ 3 lần → dừng, đổi cách
            loi.append(f'{type(e).__name__}: {str(e)[:160]}'); print('lỗi', tag, loi[-1], file=sys.stderr)
            if k == 2: raise
            time.sleep(5 * (k + 1))
    b = base64.b64decode(r['audio_base64']); mp3.write_bytes(b); al.write_text(json.dumps(r['alignment']))
    rec = dict(viec='tts-with-timestamps', tag=tag, model=MODEL, voice=G1, settings=s, seed=seed, output_format='mp3_44100_192',
               chu_gui=text, previous_text=prev or '', next_text=nxt or '', sha_vao=hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest(),
               sha_ra=hashlib.sha256(b).hexdigest(), tep=mp3.name, ky_tu=len(text), ngu_canh=len(prev or '') + len(nxt or ''),
               gia='trong gói ElevenLabs Creator (tính bằng bộ đếm ký tự; không phát sinh $)', loi_thu_lai=loi,
               luc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
    with open(LOG, 'a') as f: f.write(json.dumps(rec, ensure_ascii=False) + '\n')
    return str(mp3), r['alignment'], len(text)


def ghi_bodem(luot, gui, c0, c1):
    rec = dict(luot=luot, gui=gui, dem_truoc=c0, dem_sau=c1, tang=c1 - c0, ty_le=round((c1 - c0) / gui, 3) if gui else None, tong_gui_phien=da_gui(),
               luc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
    with open(BODEM, 'a') as f: f.write(json.dumps(rec, ensure_ascii=False) + '\n')
    return rec


def dur(p):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)], capture_output=True, text=True).stdout)


def doan():
    """lời khoá theo chương → [(chương, [(shot, chữ đoạn)])] từ khoa-loi/loi-v2-KHOA.md; kiểm nối lại đúng loi-khoa.txt."""
    C = []
    for line in (EP / 'khoa-loi/loi-v2-KHOA.md').read_text().splitlines():
        m = re.match(r'^\[(\d\d \w+)\]', line)
        if m: C.append((m.group(1), [])); continue
        m = re.match(r'^‹([^›]+)›\s*(.*)', line)
        if m: C[-1][1].append((m.group(1), re.sub(r'\s*\{[^}]*\}', '', m.group(2)).strip()))
    L = []
    for c, ss in C: L += ['', f'[{c}]'] + sum([['', t] for _, t in ss], [])
    assert '\n'.join(L).strip() + '\n' == (EP / 'loi-khoa.txt').read_text()
    return C
