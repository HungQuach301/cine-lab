"""M1 bước 2b — xoá đúng 3 giọng thư viện ElevenLabs tự thêm vào My Voices ở M0. Không xoá giọng nào khác."""
import json, os, requests
HERE = os.path.dirname(os.path.abspath(__file__))
API = 'https://api.elevenlabs.io'
TARGETS = {'wGcFBfKz5yUQqhqr0mVy': 'V1-maria-moody', 'kkPJzQOWz2Oz9cUaEaQd': 'V2-beatrice', 'Xb3zeLrTi6F4ziIcXdwk': 'C1-austin'}
before = {v['voice_id']: (v['category'], v['name']) for v in requests.get(f'{API}/v2/voices', params={'page_size': 100}).json()['voices']}
log = []
for vid, tag in TARGETS.items():
    if vid not in before:
        log.append({'voice_id': vid, 'tag': tag, 'skip': 'không có trong My Voices'}); continue
    r = requests.delete(f'{API}/v1/voices/{vid}', timeout=60)
    log.append({'voice_id': vid, 'tag': tag, 'name': before[vid][1], 'http': r.status_code, 'body': r.text[:200]})
after = {v['voice_id']: (v['category'], v['name']) for v in requests.get(f'{API}/v2/voices', params={'page_size': 100}).json()['voices']}
out = {'deleted': log, 'count_before': len(before), 'count_after': len(after),
       'removed': sorted(set(before) - set(after)), 'non_premade_after': {k: v for k, v in after.items() if v[0] != 'premade'}}
json.dump(out, open(os.path.join(HERE, 'delete-m0-library.json'), 'w'), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
