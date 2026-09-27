"""M0 bước 3 — sinh take ElevenLabs cho câu cảm xúc khó (lời tạm biệt khẽ, nghẹn của bà lão thắp đèn).
Chạy: /opt/cine/bin/python reports/m0/voice/el_takes.py
Khoá do proxy gắn cho api.elevenlabs.io; script không chứa khoá.
Ghi: reports/m0/voice/takes/*.mp3 và reports/m0/raw/voice-takes.json (tham số, thời gian, số ký tự tính phí)."""
import base64, json, os, time, requests

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'takes'); os.makedirs(OUT, exist_ok=True)
RAW = os.path.join(HERE, '..', 'raw'); os.makedirs(RAW, exist_ok=True)
API = 'https://api.elevenlabs.io'

# Câu thử (tiếng Anh). Bản sạch dùng để kiểm đủ từ; bản có thẻ âm thanh [..] đưa vào eleven_v3.
LINE_CLEAN = ("That's the last one, then. Goodnight, old street. Forty years, every single night. "
              "You'll be brighter now. Just don't forget how warm we were.")
LINE_V3 = ("[softly] That's the last one, then. [sighs] Goodnight, old street. "
           "[voice breaking] Forty years... every single night. [whispers] You'll be brighter now. "
           "Just... don't forget how warm we were.")
CHILD_CLEAN = "Please, could you light the old one? The new ones hurt my eyes."
CHILD_V3 = "[timidly] Please... could you light the old one? [whispers] The new ones hurt my eyes."

# Giọng thư viện chia sẻ (dùng trực tiếp theo voice_id; không thêm vào tài khoản).
VOICES = [
    ('V1-maria-moody', 'wGcFBfKz5yUQqhqr0mVy', 'Maria Moody - Grandmotherly Storykeeper (old, female, American; notice 730 ngày)'),
    ('V2-beatrice', 'kkPJzQOWz2Oz9cUaEaQd', 'Beatrice - Mature, Gentle and Engaging (old, female, British; notice 730 ngày)'),
]
CHILD = ('C1-austin', 'Xb3zeLrTi6F4ziIcXdwk', 'Austin - Timid and Casual (young male, American; "timid orphan boy"; notice 730 ngày)')
TAKES = [  # (tên take, stability, seed) — eleven_v3: 0.0 Creative, 0.5 Natural
    ('t1-natural', 0.5, 101), ('t2-creative', 0.0, 202), ('t3-creative', 0.0, 303)]

log = []

def tts(tag, voice_id, text, stab, seed, clean):
    t = time.time()
    r = requests.post(f'{API}/v1/text-to-speech/{voice_id}', params={'output_format': 'mp3_44100_128'},
                      json={'text': text, 'model_id': 'eleven_v3', 'seed': seed,
                            'voice_settings': {'stability': stab, 'similarity_boost': 0.75}}, timeout=180)
    rec = {'file': f'takes/{tag}.mp3', 'voice_id': voice_id, 'model': 'eleven_v3', 'stability': stab, 'seed': seed,
           'text_sent': text, 'text_clean': clean, 'http': r.status_code, 'latency_s': round(time.time() - t, 2),
           'character_cost': r.headers.get('x-character-count'), 'request_id': r.headers.get('request-id')}
    if r.ok:
        open(os.path.join(OUT, f'{tag}.mp3'), 'wb').write(r.content)
    else:
        rec['error'] = r.text[:500]
    log.append(rec); print(json.dumps(rec, ensure_ascii=False))

for vtag, vid, desc in VOICES:
    for ttag, stab, seed in TAKES:
        tts(f'{vtag}_{ttag}', vid, LINE_V3, stab, seed, LINE_CLEAN)

# Giọng thứ 3: Voice Design (giọng do mô tả tạo ra; bản preview đọc đúng câu thoại, không lưu giọng vào tài khoản).
t = time.time()
desc3 = ("An elderly English woman in her late seventies, soft and slightly hoarse, frail breath, "
         "a working woman's warmth, speaking quietly and close to the microphone, emotional, on the edge of tears.")
r = requests.post(f'{API}/v1/text-to-voice/design', params={'output_format': 'mp3_44100_128'},
                  json={'voice_description': desc3, 'text': LINE_V3, 'model_id': 'eleven_ttv_v3', 'seed': 7}, timeout=300)
rec = {'kind': 'voice_design', 'description': desc3, 'text_clean': LINE_CLEAN, 'http': r.status_code,
       'latency_s': round(time.time() - t, 2), 'character_cost': r.headers.get('x-character-count')}
if r.ok:
    for i, p in enumerate(r.json().get('previews', [])[:3], 1):
        fn = f'V3-designed_t{i}-preview.mp3'
        open(os.path.join(OUT, fn), 'wb').write(base64.b64decode(p['audio_base_64']))
        rec.setdefault('files', []).append({'file': f'takes/{fn}', 'generated_voice_id': p.get('generated_voice_id'),
                                            'duration_s': p.get('duration_secs')})
else:
    rec['error'] = r.text[:500]
log.append(rec); print(json.dumps(rec, ensure_ascii=False))

ctag, cid, cdesc = CHILD
for ttag, stab, seed in TAKES:
    tts(f'{ctag}_{ttag}', cid, CHILD_V3, stab, seed, CHILD_CLEAN)

json.dump({'voices': VOICES + [CHILD], 'takes': log}, open(os.path.join(RAW, 'voice-takes.json'), 'w'), indent=1, ensure_ascii=False)
