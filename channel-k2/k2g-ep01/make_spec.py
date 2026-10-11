#!/opt/cine/bin/python
"""Ghép đặc tả tập: ep-src.yaml (hình, nguồn, số) + lời khoá v3.7 NGUYÊN VĂN từ vo-skel.yaml (đúng chuỗi đã thu ElevenLabs, khoá cache) → episode.yaml."""
import os, yaml
H = os.path.dirname(os.path.abspath(__file__))
src = yaml.safe_load(open(f'{H}/ep-src.yaml')); skel = {s['id']: s['vo'] for s in yaml.safe_load(open(f'{H}/vo-skel.yaml'))['segments']}
for s in src['segments']:
    if s.get('vo') == '@skel': s['vo'] = skel[s['id']]
assert all(s['vo'] == skel[s['id']] for s in src['segments'])
hd = '# TỆP SINH TỰ ĐỘNG bởi make_spec.py từ ep-src.yaml + vo-skel.yaml (lời khoá v3.7). Sửa ep-src.yaml, không sửa tệp này.\n'
open(f'{H}/episode.yaml', 'w').write(hd + yaml.safe_dump(src, allow_unicode=True, sort_keys=False, width=4000))
print('episode.yaml', len(src['segments']), 'đoạn,', sum(len(s['shots']) for s in src['segments']), 'shot,', len(src['heroes']), 'cảnh 3D')
