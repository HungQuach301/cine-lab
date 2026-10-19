"""GIỌNG-CHỐT · dùng lại thư viện casting-giong (cg_lib, kiem_lib): thư mục ngoài git, nhật ký ký tự, trần ký tự của phiên này.
Khoá do proxy gắn cho api.elevenlabs.io — không đọc, không in. Không đưa email vào header/URL/payload."""
import hashlib, json, os, sys
os.environ.setdefault('CG_OUT', '/var/tmp/cine-out/giong-chot')
H = os.path.dirname(os.path.abspath(__file__)); CG = os.path.join(os.path.dirname(H), 'casting-giong')
sys.path.insert(0, CG)
import cg_lib as L, kiem_lib as K   # noqa: E402
L.LOG = os.path.join(H, 'nhat-ky-ky-tu.jsonl')
CHAN, MOC = 6000, 3000                       # chặn / mốc theo dõi (lệnh GIỌNG-CHỐT 19/10)
G1 = 'VDLncRBHDjLHBqLhQ1Qt'                  # G1 = casting-giong A2 biến thể 3 (thiet-ke.json; khoa-ten.json G1; casting-my M2 = DC-G1)
V2, V4 = 'eleven_multilingual_v2', 'eleven_v4'


def da_gui():
    if not os.path.exists(L.LOG): return 0
    return sum(json.loads(l)['ky_tu'] for l in open(L.LOG) if l.strip())


def tts(text, tag, model=V2, speed=1.0, settings=None):
    """Chặn trước khi gửi nếu chạm trần 6 000 ký tự gửi của phiên. Cache theo băm (đã thu = 0 ký tự)."""
    s = dict(settings or dict(stability=0.5, similarity_boost=0.75, speed=speed))
    key = hashlib.sha1(json.dumps([G1, text, model, s], sort_keys=True).encode()).hexdigest()[:16]
    if not os.path.exists(f'{L.OUT}/raw/{key}.mp3') and da_gui() + len(text) >= CHAN:
        raise SystemExit(f'CHẶN: {da_gui()} + {len(text)} ≥ {CHAN} ký tự gửi')
    return L.tts(G1, text, model=model, settings=s, tag=tag)


def sub():
    d = json.loads(L.call('/v1/user/subscription'))
    return dict(character_count=d['character_count'], character_limit=d['character_limit'], next_reset_unix=d.get('next_character_count_reset_unix'), tier=d.get('tier'))


def tts_seed(text, tag, seed, model=V2, settings=None):
    """Như tts() nhưng gửi thêm `seed` (cùng seed cho mọi mức speed → tách tác dụng của speed khỏi biến thiên giữa các lượt thu)."""
    s = dict(settings or dict(stability=0.5, similarity_boost=0.75, speed=1.0))
    key = hashlib.sha1(json.dumps([G1, text, model, s, seed], sort_keys=True).encode()).hexdigest()[:16]; p = f'{L.OUT}/raw/{key}.mp3'
    if os.path.exists(p): return p, 0
    if da_gui() + len(text) >= CHAN: raise SystemExit(f'CHẶN: {da_gui()} + {len(text)} ≥ {CHAN} ký tự gửi')
    audio = L.call(f'/v1/text-to-speech/{G1}?output_format=mp3_44100_192', dict(text=text, model_id=model, voice_settings=s, seed=seed), accept='audio/mpeg')
    open(p, 'wb').write(audio)
    with open(L.LOG, 'a') as f: f.write(json.dumps(dict(viec='tts', tag=tag, model=model, seed=seed, ky_tu=len(text), tep=os.path.basename(p)), ensure_ascii=False) + '\n')
    return p, len(text)
