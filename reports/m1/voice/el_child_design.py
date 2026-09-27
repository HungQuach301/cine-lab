"""M1 bước 2c — thiết kế 3 giọng trẻ em (8–10 tuổi, rụt rè, tiếng Anh) bằng Voice Design; mỗi giọng 2 take cùng một câu.
Quy trình mỗi giọng:
  1. POST /v1/text-to-voice/design (eleven_ttv_v3) với mô tả + đoạn thoại thiết kế (>=100 ký tự) -> 3 preview.
  2. Chọn preview có F0 trung vị cao nhất (đo bằng librosa.pyin) — tiêu chí khách quan chống "giọng trưởng thành" (lỗi của Austin ở M0).
  3. Lưu preview đó thành giọng (POST /v1/text-to-voice), nhãn 'candidate' (xoá giọng trượt sau khi chủ dự án chọn).
  4. Sinh 2 take câu thử bằng eleven_v3 (t1 Natural 0.5 seed 101, t2 Creative 0.0 seed 202 — giống cách làm M0).
Khoá do proxy gắn. Ghi reports/m1/voice/child-takes.json."""
import base64, io, json, os, time, requests
import numpy as np, librosa, soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'takes'); os.makedirs(OUT, exist_ok=True)
PRE = os.path.join(HERE, 'previews'); os.makedirs(PRE, exist_ok=True)
API = 'https://api.elevenlabs.io'

CHILD_CLEAN = "Please, could you light the old one? The new ones hurt my eyes."
CHILD_V3 = "[timidly] Please... could you light the old one? [whispers] The new ones hurt my eyes."
DESIGN_TEXT = ("[timidly] Um... excuse me? Sorry. I didn't mean to follow you. It's just... the new lamps are so bright, "
               "and I can't sleep, and yours is the only warm one left.")
NOT_ADULT = " A real child's voice, not an adult imitating a child."
VOICES = [
    ('C2', "A shy eight-year-old girl with a light English accent. Small, thin, high voice; hesitant, soft, a little breathy, "
           "with small pauses, nervous but polite." + NOT_ADULT),
    ('C3', "A timid nine-year-old boy, neutral British English. Soft high voice that has not broken yet; quiet and unsure, "
           "trailing off at the ends of phrases." + NOT_ADULT),
    ('C4', "A withdrawn ten-year-old girl with a soft Northern English accent. Quiet, whispery, low energy, speaking close "
           "and carefully as if afraid of being told off." + NOT_ADULT),
]
TAKES = [('t1-natural', 0.5, 101), ('t2-creative', 0.0, 202)]

def f0_median(mp3_bytes):
    y, sr = librosa.load(io.BytesIO(mp3_bytes), sr=16000, mono=True)
    f0, vflag, _ = librosa.pyin(y, fmin=80, fmax=600, sr=sr)
    v = f0[vflag & ~np.isnan(f0)]
    return float(np.median(v)) if len(v) else None

log = {'line_clean': CHILD_CLEAN, 'line_v3': CHILD_V3, 'design_text': DESIGN_TEXT, 'voices': []}
for tag, desc in VOICES:
    rec = {'tag': tag, 'description': desc}
    t = time.time()
    r = requests.post(f'{API}/v1/text-to-voice/design', params={'output_format': 'mp3_44100_128'},
                      json={'voice_description': desc, 'text': DESIGN_TEXT, 'model_id': 'eleven_ttv_v3', 'seed': 11}, timeout=300)
    rec['design_http'] = r.status_code; rec['design_latency_s'] = round(time.time() - t, 2)
    if not r.ok:
        rec['design_error'] = r.text[:600]; log['voices'].append(rec); print(json.dumps(rec)); continue
    cands = []
    for i, p in enumerate(r.json().get('previews', [])[:3], 1):
        b = base64.b64decode(p['audio_base_64'])
        fn = f'{tag}_design-preview{i}.mp3'; open(os.path.join(PRE, fn), 'wb').write(b)
        cands.append({'i': i, 'file': f'previews/{fn}', 'generated_voice_id': p['generated_voice_id'],
                      'duration_s': p.get('duration_secs'), 'f0_median_hz': f0_median(b)})
    rec['previews'] = cands
    best = max(cands, key=lambda c: c['f0_median_hz'] or 0)
    rec['chosen_preview'] = best['i']
    s = requests.post(f'{API}/v1/text-to-voice', json={
        'voice_name': f'CINE-LastRound-Child-{tag}', 'voice_description': desc,
        'generated_voice_id': best['generated_voice_id'],
        'labels': {'project': 'cine-lab', 'role': 'child', 'status': 'candidate'}}, timeout=120)
    rec['save_http'] = s.status_code
    if not s.ok:
        rec['save_error'] = s.text[:600]; log['voices'].append(rec); print(json.dumps(rec)); continue
    vid = s.json()['voice_id']; rec['voice_id'] = vid; rec['takes'] = []
    for ttag, stab, seed in TAKES:
        t = time.time()
        q = requests.post(f'{API}/v1/text-to-speech/{vid}', params={'output_format': 'mp3_44100_128'},
                          json={'text': CHILD_V3, 'model_id': 'eleven_v3', 'seed': seed,
                                'voice_settings': {'stability': stab, 'similarity_boost': 0.75}}, timeout=180)
        tr = {'file': f'takes/{tag}_{ttag}.mp3', 'stability': stab, 'seed': seed, 'http': q.status_code,
              'latency_s': round(time.time() - t, 2), 'character_cost': q.headers.get('x-character-count')}
        if q.ok:
            open(os.path.join(OUT, f'{tag}_{ttag}.mp3'), 'wb').write(q.content)
            tr['f0_median_hz'] = f0_median(q.content)
        else:
            tr['error'] = q.text[:500]
        rec['takes'].append(tr)
    log['voices'].append(rec); print(json.dumps(rec, ensure_ascii=False)[:1500])
json.dump(log, open(os.path.join(HERE, 'child-takes.json'), 'w'), indent=1, ensure_ascii=False)
