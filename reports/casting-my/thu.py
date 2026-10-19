#!/opt/cine/bin/python
"""thu.py <ma_noi_bo> <voice_id> — thu 2 đoạn thử (doan-thu.json) bằng một giọng, cấu hình kênh (cg_lib.SET/MODEL);
chặn nếu tổng ký tự gửi của phiên chạm 5 000; in ký tự gửi + bộ đếm trước/sau."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import my_lib as M
L = M.L; ma, vid = sys.argv[1], sys.argv[2]
D = json.load(open(f'{M.H}/doan-thu.json'))['doan']
c0 = L.counter(); sent = 0; files = []
for d in D:
    p, n = M.tts(vid, d['gui'], tag=f'{ma}:{d["doan"]}'); sent += n; files.append(p)
c1 = L.counter()
json.dump(dict(ma=ma, voice_id=vid, tep=files), open(f'{L.OUT}/{ma}.json', 'w'))
print(json.dumps(dict(ma=ma, gui=sent, dem_truoc=c0, dem_sau=c1, dem_tang=c1 - c0, tong_gui_phien=M.da_gui())))
