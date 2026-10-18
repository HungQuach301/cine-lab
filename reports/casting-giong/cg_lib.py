"""CASTING-GIỌNG · thư viện chung: gọi ElevenLabs (khoá do proxy gắn — không đọc/in khoá), cache theo băm, bộ đếm tài khoản."""
import hashlib, json, os, urllib.request
OUT = os.environ.get('CG_OUT', '/var/tmp/cine-out/casting-giong'); os.makedirs(OUT + '/raw', exist_ok=True)
API = 'https://api.elevenlabs.io'
SET = dict(stability=0.5, similarity_boost=0.75, speed=1.0)   # cấu hình kênh (Eric T1/T2) — giữ nguyên cho mọi giọng để so công bằng
MODEL = 'eleven_multilingual_v2'                             # model kênh (BIBLE-KENH2 §4)
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nhat-ky-ky-tu.jsonl')


def call(path, body=None, method=None, accept='application/json'):
    req = urllib.request.Request(API + path, data=None if body is None else json.dumps(body).encode(), method=method or ('POST' if body is not None else 'GET'),
                                 headers={'Content-Type': 'application/json', 'Accept': accept})
    return urllib.request.urlopen(req, timeout=300).read()


def counter():
    return json.loads(call('/v1/user/subscription'))['character_count']


def tts(voice_id, text, model=MODEL, settings=SET, tag=''):
    key = hashlib.sha1(json.dumps([voice_id, text, model, settings], sort_keys=True).encode()).hexdigest()[:16]
    p = f'{OUT}/raw/{key}.mp3'
    if os.path.exists(p): return p, 0
    audio = call(f'/v1/text-to-speech/{voice_id}?output_format=mp3_44100_192', dict(text=text, model_id=model, voice_settings=settings), accept='audio/mpeg')
    open(p, 'wb').write(audio)
    with open(LOG, 'a') as f: f.write(json.dumps(dict(viec='tts', tag=tag, model=model, ky_tu=len(text), tep=os.path.basename(p)), ensure_ascii=False) + '\n')
    return p, len(text)
