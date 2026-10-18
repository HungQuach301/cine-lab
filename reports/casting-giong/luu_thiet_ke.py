#!/opt/cine/bin/python
"""CASTING-GIỌNG · lưu biến thể đã chọn của mỗi mô tả thành giọng trong tài khoản (/v1/text-to-voice) → voice_id (ghi thiet-ke.json)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import cg_lib as L
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'thiet-ke.json'); S = json.load(open(P))
for k, v in S.items():
    if v.get('voice_id'): continue
    b = v['bien_the'][v['chon'] - 1]
    r = json.loads(L.call('/v1/text-to-voice', dict(voice_name=f'CINE-CastingGiong-{k}-v{v["chon"]}', voice_description=v['mo_ta'], generated_voice_id=b['generated_voice_id'],
                                                   labels={'project': 'cine-lab', 'use': 'casting-giong-contested-places'})))
    v['voice_id'] = r['voice_id']; print(k, r['voice_id'])
json.dump(S, open(P, 'w'), ensure_ascii=False, indent=1)
