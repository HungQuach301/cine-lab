#!/opt/cine/bin/python
"""CASTING-MỸ · lưu biến thể đã chọn thành giọng trong tài khoản (/v1/text-to-voice, 0 ký tự) → voice_id (ghi thiet-ke.json)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import my_lib as M
L = M.L; P = f'{M.H}/thiet-ke.json'; S = json.load(open(P))
for k, v in S.items():
    if v.get('voice_id'): continue
    b = v['bien_the'][v['chon'] - 1]
    r = json.loads(L.call('/v1/text-to-voice', dict(voice_name=f'CINE-CastingMy-{k}-v{v["chon"]}', voice_description=v['mo_ta'], generated_voice_id=b['generated_voice_id'],
                                                   labels={'project': 'cine-lab', 'use': 'casting-my-contested-places'})))
    v['voice_id'] = r['voice_id']; print(k, r['voice_id'])
json.dump(S, open(P, 'w'), ensure_ascii=False, indent=1)
