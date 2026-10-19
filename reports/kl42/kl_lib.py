"""KL42 · thư viện thu G1 cả tập T3 (lời v4.2). Khoá do proxy gắn cho api.elevenlabs.io — không đọc, không in. Không đưa email vào header/URL/payload.
- tts(): POST /v1/text-to-speech/<G1>/with-timestamps (mp3_44100_192 — gói Creator không có PCM), seed cố định, previous_text/next_text trong chương;
  cache theo băm (đã thu = 0 ký tự); CHẶN cứng trước khi gửi nếu tổng ký tự gửi của phiên chạm 18 000 (lệnh KL42).
- Nhật ký: nhat-ky-ky-tu.jsonl (mỗi lệnh: ký tự text gửi + ký tự ngữ cảnh), bo-dem.jsonl (bộ đếm tài khoản trước/sau mỗi lượt)."""
import base64, hashlib, json, os, re, subprocess, sys, time, urllib.request
from pathlib import Path
H = Path(__file__).resolve().parent; R = H.parents[1]; EP = R / 'channel-k2/k2c-t3-01'
OUT = Path(os.environ.get('KL_OUT', '/var/tmp/cine-out/kl42')); (OUT / 'raw').mkdir(parents=True, exist_ok=True)
API = 'https://api.elevenlabs.io'; UA = 'CineLab-research (+https://github.com/HungQuach301/cine-lab)'
G1 = 'VDLncRBHDjLHBqLhQ1Qt'; MODEL = 'eleven_multilingual_v2'
SET = dict(stability=0.5, similarity_boost=0.75, speed=1.03)   # bản 1.03-B, chủ dự án duyệt 19/10 12:45
SEED = 19102026                                               # seed của lượt B GIỌNG-CHỐT (bản 1.03-B)
CHAN, MOC = 18000, 14000
LOG, BODEM = H / 'nhat-ky-ky-tu.jsonl', H / 'bo-dem.jsonl'
TD = json.loads((EP / 'khoa-loi/phat-am/tu-dien.json').read_text())['muc']


def alias(t):
    for d in sorted(TD, key=lambda x: -len(x['viet'])): t = re.sub(r'(?<![\w-])' + re.escape(d['viet']) + r'(?![\w])', d['doc'], t)
    return t


def call(path, body=None, accept='application/json', timeout=300):
    req = urllib.request.Request(API + path, data=None if body is None else json.dumps(body).encode(), method='POST' if body is not None else 'GET',
                                 headers={'Content-Type': 'application/json', 'Accept': accept, 'User-Agent': UA})
    return urllib.request.urlopen(req, timeout=timeout).read()


def counter(wait=0):
    if wait: time.sleep(wait)
    return json.loads(call('/v1/user/subscription'))['character_count']


def da_gui():
    return sum(json.loads(l)['ky_tu'] for l in open(LOG) if l.strip()) if LOG.exists() else 0


def tts(text, tag, prev=None, nxt=None, seed=SEED, settings=None):
    """→ (mp3, alignment dict, ký tự gửi lần này). Ký tự gửi = len(text) (ngữ cảnh ghi riêng)."""
    s = dict(settings or SET)
    body = dict(text=text, model_id=MODEL, voice_settings=s, seed=seed)
    if prev: body['previous_text'] = prev
    if nxt: body['next_text'] = nxt
    key = hashlib.sha1(json.dumps([G1, body], sort_keys=True).encode()).hexdigest()[:16]
    mp3, al = OUT / 'raw' / f'{key}.mp3', OUT / 'raw' / f'{key}.align.json'
    if mp3.exists() and al.exists(): return str(mp3), json.loads(al.read_text()), 0
    if da_gui() + len(text) > CHAN: raise SystemExit(f'CHẶN: {da_gui()} + {len(text)} > {CHAN} ký tự gửi (lệnh KL42)')
    for k in range(3):
        try:
            r = json.loads(call(f'/v1/text-to-speech/{G1}/with-timestamps?output_format=mp3_44100_192', body)); break
        except Exception as e:   # lỗi mạng: thử lại tối đa 3 lần (luật dừng: cùng lỗi ≥ 3 lần)
            print('lỗi', tag, type(e).__name__, str(e)[:200], file=sys.stderr)
            if k == 2: raise
            time.sleep(5 * (k + 1))
    mp3.write_bytes(base64.b64decode(r['audio_base64'])); al.write_text(json.dumps(r['alignment']))
    with open(LOG, 'a') as f:
        f.write(json.dumps(dict(viec='tts-ts', tag=tag, model=MODEL, seed=seed, speed=s['speed'], ky_tu=len(text), ngu_canh=len(prev or '') + len(nxt or ''),
                                tep=mp3.name, luc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())), ensure_ascii=False) + '\n')
    return str(mp3), r['alignment'], len(text)


def ghi_bodem(luot, gui, c0, c1):
    rec = dict(luot=luot, gui=gui, dem_truoc=c0, dem_sau=c1, tang=c1 - c0, ty_le=round((c1 - c0) / gui, 3) if gui else None, tong_gui_phien=da_gui(),
               luc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
    with open(BODEM, 'a') as f: f.write(json.dumps(rec, ensure_ascii=False) + '\n')
    return rec


def dur(p):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)], capture_output=True, text=True).stdout)


def doan_v42():
    """Lời v4.2 theo chương → [(chương, [(shot, chữ khoá)])]; kiểm nối lại đúng loi-khoa.txt."""
    md = (EP / 'script-v4.2-KHOA.md').read_text(); C = []
    for line in md.splitlines():
        m = re.match(r'^\[(\d\d \w+)\]', line)
        if m: C.append((m.group(1), [])); continue
        m = re.match(r'^‹([^›]+)›\s*(.*)', line)
        if m:
            t = re.sub(r'\s*\{[^}]*\}', '', m.group(2)).replace('‹Our read› ', '').replace('[IM LẶNG]', '').strip()
            if t: C[-1][1].append((m.group(1), t))
    L = []
    for c, ss in C: L += ['', f'[{c}]'] + sum([['', t] for _, t in ss], [])
    assert '\n'.join(L).strip() + '\n' == (EP / 'loi-khoa.txt').read_text()
    return C


def doan_v42_dict():
    return {c: [dict(shot=s, khoa=t) for s, t in ss] for c, ss in doan_v42()}
