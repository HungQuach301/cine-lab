"""M1 bước 2a — lưu vĩnh viễn giọng V3 (Voice Design, M0) vào tài khoản ElevenLabs.
Chọn preview t2 (generated_voice_id 59pjz3MTZdh9U1AETKfW): chủ dự án chấm 4/5/4 cho t1/t2/t3, t2 cao nhất.
Chạy: /opt/cine/bin/python reports/m1/voice/el_save_v3.py  (khoá do proxy gắn)."""
import json, os, time, requests
HERE = os.path.dirname(os.path.abspath(__file__))
API = 'https://api.elevenlabs.io'
DESC = ("An elderly English woman in her late seventies, soft and slightly hoarse, frail breath, "
        "a working woman's warmth, speaking quietly and close to the microphone, emotional, on the edge of tears.")
body = {'voice_name': 'CINE-LastRound-Lamplighter-V3', 'voice_description': DESC,
        'generated_voice_id': '59pjz3MTZdh9U1AETKfW',
        'labels': {'project': 'cine-lab', 'role': 'lamplighter', 'source': 'M0 V3 preview t2'}}
t = time.time()
r = requests.post(f'{API}/v1/text-to-voice', json=body, timeout=120)
rec = {'request': body, 'http': r.status_code, 'latency_s': round(time.time() - t, 2),
       'response': (r.json() if r.headers.get('content-type', '').startswith('application/json') else r.text[:800])}
if isinstance(rec['response'], dict):
    rec['response'].pop('preview_url', None)
json.dump(rec, open(os.path.join(HERE, 'save-v3.json'), 'w'), indent=1, ensure_ascii=False)
print(json.dumps({k: rec[k] for k in ('http', 'latency_s')}), json.dumps(rec['response'])[:800])
