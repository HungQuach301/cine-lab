#!/opt/cine/bin/python
"""CASTING-MỸ · đối chứng G1 (= A2 casting-giong, giọng đã chọn): DÙNG LẠI bản thu trong casting-giong/nghe-mu/G1.mp3, không thu lại (0 ký tự).
Tệp đó = đoạn 1 + 0,8 s lặng + đoạn 2 + 0,8 s lặng + đoạn 3 (đã −14 LUFS, stereo 112 kb/s). Ranh giới tìm bằng ASR (dấu thời gian từ) + silencedetect:
đoạn 1 kết thúc trong khoảng lặng 26,87–27,85 s; đoạn 2 kết thúc "…three hundred and fifty-seven" 89,54 s, lặng 90,25–91,12 s, "Here's the twist" bắt đầu 91,16 s.
Cắt: đoạn 1 = 0–27,30 s; đoạn 2 = 27,30–90,40 s (bản giải mã WAV, dùng cho máy kiểm); bản nghe = 0–90,40 s (xem nghe_mu.py).
Khác biệt đã biết so với 4 ứng viên: chữ gửi đoạn 2 của G1 dùng alias cũ "dar-SOHN" (ứng viên: "dar-sohn"); còn lại trùng từng ký tự."""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import my_lib as M
L = M.L; SRC = os.path.join(os.path.dirname(M.H), 'casting-giong/nghe-mu/G1.mp3'); CUT = [(0.0, 27.30), (27.30, 90.40)]
files = []
for i, (a, b) in enumerate(CUT, 1):
    f = f'{L.OUT}/DC-G1-doan{i}.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', SRC, '-ss', str(a), '-to', str(b), '-ac', '1', '-c:a', 'pcm_s24le', f], check=True); files.append(f)
json.dump(dict(ma='DC-G1', voice_id='VDLncRBHDjLHBqLhQ1Qt', tep=files, nguon=SRC, cat=CUT), open(f'{L.OUT}/DC-G1.json', 'w'))
print(files)
