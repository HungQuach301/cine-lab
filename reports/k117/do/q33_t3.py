#!/opt/cine/bin/python
"""K-1.17 · chạy riêng 3 hàng Q33 (Q33, Q33-K2, Q33 (1.13)) trên animatic T3 với bản xem ghép 8 chương (640×360, 761,15 s) thay master ngoài git.
  q33_t3.py <episode.yaml> <timeline.json> <video.mp4> [--k117]"""
import json, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from checks.ll import base, q_scene, q_k2var, q_k116, q_k117  # noqa: E402
E = base.load(sys.argv[1]); E['_path'] = os.path.abspath(sys.argv[1]); TL = json.load(open(sys.argv[2])); mv = sys.argv[3]
NL = q_k117.nam_log(q_k116.log_shot(E, os.path.dirname(E['_path']))[0]) if '--k117' in sys.argv else None
for ten, fn in (('Q33', lambda: q_scene.q33(E, TL, video=mv, nam_log=NL)), ('Q33-K2', lambda: q_k2var.q33_k2(E, TL, mv, nam_log=NL)), ('Q33 (1.13)', lambda: q_scene.q33(E, TL, video=mv, k2=True, nam_log=NL))):
    x = fn(); print(ten, 'ĐẠT' if x['ok'] else 'TRƯỢT', '·', x['val']); [print('  ', y) for y in (x['loi'] + (x.get('thieu') or []))[:12]]
