"""Cổng 2 bước 4 — table read "Last Round": đọc 5 câu của Ida bằng giọng đã chốt (voice_id 59pjz3MTZdh9U1AETKfW, eleven_v3),
đặt mỗi câu vào đúng mốc thời gian của kịch bản trên nền im lặng dài bằng phim (165 s), xuất WAV 48 kHz + MP3 để nghe.
Nếu một câu dài hơn khoảng trống trước câu sau, câu sau bị đẩy lùi (tối thiểu cách 1,0 s) và ghi rõ trong cue.json.
Chạy: /opt/cine/bin/python reports/m1/cong2/tableread/make_tableread.py  (khoá do proxy gắn)."""
import io, json, os, subprocess, time, requests
import numpy as np, soundfile as sf, librosa

HERE = os.path.dirname(os.path.abspath(__file__))
API = 'https://api.elevenlabs.io'
VOICE = '59pjz3MTZdh9U1AETKfW'
SR = 48000
FILM_S = 165.0
SCENES = [('1 The Round', 0, 30), ('2 Switch-on', 30, 55), ('3 The Race', 55, 85),
          ('4 The Wall', 85, 115), ('5 The Last Lamp', 115, 145), ('6 The Window', 145, 165)]
LINES = [  # (mã, mốc trong kịch bản giây, câu sạch, câu có thẻ diễn xuất eleven_v3)
    ('L1', 10.0, "Evening, old street.", "[softly] Evening, old street."),
    ('L2', 72.0, "Not yet... not yet.", "[under her breath, strained] Not yet... not yet."),
    ('L3', 104.0, "Go on, then.", "[gently] Go on, then."),
    ('L4', 122.0, "That's the last one, then. Goodnight, old street. You'll be brighter now. Just... keep a little dark for the ones who need it.",
     "[softly] That's the last one, then. [sighs] Goodnight, old street. [voice breaking] You'll be brighter now. [whispers] Just... keep a little dark for the ones who need it."),
    ('L5', 139.5, "Warm your hands first. Three counts.", "[warmly, quietly] Warm your hands first. Three counts."),
]

def tts(text, seed=101, stab=0.5):
    r = requests.post(f'{API}/v1/text-to-speech/{VOICE}', params={'output_format': 'mp3_44100_128'},
                      json={'text': text, 'model_id': 'eleven_v3', 'seed': seed,
                            'voice_settings': {'stability': stab, 'similarity_boost': 0.75}}, timeout=180)
    r.raise_for_status()
    return r.content, r.headers.get('x-character-count')

def trim(y, sr, db=-45):
    idx = np.nonzero(np.abs(y) > 10 ** (db / 20))[0]
    if not len(idx): return y
    a, b = max(0, idx[0] - int(0.05 * sr)), min(len(y), idx[-1] + int(0.15 * sr))
    return y[a:b]

mix = np.zeros(int(FILM_S * SR), np.float32)
cues, prev_end = [], 0.0
os.makedirs(os.path.join(HERE, 'lines'), exist_ok=True)
for code, t_script, clean, tagged in LINES:
    t0 = time.time(); fp = os.path.join(HERE, 'lines', f'{code}.mp3')
    if os.path.exists(fp):   # dùng lại take đã sinh (không tốn ký tự); xoá file để sinh lại
        mp3, chars = open(fp, 'rb').read(), 'cached'
    else:
        mp3, chars = tts(tagged); open(fp, 'wb').write(mp3)
    y, _ = librosa.load(io.BytesIO(mp3), sr=SR, mono=True)
    y = trim(y, SR)
    start = max(t_script, prev_end + 1.0)
    i = int(start * SR); mix[i:i + len(y)] += y[: len(mix) - i]
    dur = len(y) / SR; prev_end = start + dur
    scene = next(n for n, a, b in SCENES if a <= start < b)
    cues.append({'code': code, 'scene': scene, 'script_cue_s': t_script, 'placed_s': round(start, 2),
                 'shifted_s': round(start - t_script, 2), 'dur_s': round(dur, 2), 'end_s': round(prev_end, 2),
                 'text_clean': clean, 'text_sent': tagged, 'character_cost': chars, 'latency_s': round(time.time() - t0, 2),
                 'fits_scene': prev_end <= next(b for n, a, b in SCENES if n == scene)})
    print(json.dumps(cues[-1], ensure_ascii=False))
peak = np.abs(mix).max(); mix *= 10 ** (-3 / 20) / peak   # đỉnh mẫu −3 dBFS (bản nghe tạm, chưa master)
wav = os.path.join(HERE, 'last-round-tableread.wav')
sf.write(wav, np.stack([mix, mix], 1), SR, subtype='PCM_24')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', wav, '-c:a', 'libmp3lame', '-b:a', '192k', wav[:-4] + '.mp3'], check=True)
json.dump({'voice_id': VOICE, 'model': 'eleven_v3', 'stability': 0.5, 'seed': 101, 'film_s': FILM_S, 'scenes': SCENES,
           'normalize': 'peak -3 dBFS', 'cues': cues}, open(os.path.join(HERE, 'cue.json'), 'w'), indent=1, ensure_ascii=False)
