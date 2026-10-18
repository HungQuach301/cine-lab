#!/opt/cine/bin/python
"""thu.py <ma_noi_bo> <voice_id> — thu 3 đoạn thử (doan-thu.json) + bảng phát âm (phat-am-thu.json) bằng một giọng; in ký tự gửi + bộ đếm trước/sau."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import cg_lib as L
ma, vid = sys.argv[1], sys.argv[2]
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'doan-thu.json')))['doan']
c0 = L.counter(); sent = 0; files = []
for d in D:
    p, n = L.tts(vid, d['gui'], tag=f'{ma}:{d["doan"]}'); sent += n; files.append(p)
PA = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'phat-am-thu.json')))
pa, n = L.tts(vid, PA['gui'], tag=f'{ma}:phat-am'); sent += n
c1 = L.counter()
json.dump(dict(ma=ma, voice_id=vid, tep=files, phat_am=pa), open(f'{L.OUT}/{ma}.json', 'w'))
print(json.dumps(dict(ma=ma, gui=sent, dem_truoc=c0, dem_sau=c1, dem_tang=c1 - c0)))
