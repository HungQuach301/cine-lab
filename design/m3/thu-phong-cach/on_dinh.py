"""Cine Lab · M3 THỬ PHONG CÁCH — đo độ ổn định theo thời gian (nhấp nháy) của kết cấu/mảng sáng.
Chênh lệch tuyệt đối trung bình giữa hai khung liên tiếp (mã 8 bit, luma), trên vùng KHÔNG có chuyển động (mặt nạ: điểm ảnh mà chênh lệch
giữa khung đầu và khung cuối < 6 mã ở CẢ hai bản) → phần còn lại chủ yếu là grain chung của đường ống + nhấp nháy do hậu kỳ.
/opt/cine/bin/python design/m3/thu-phong-cach/on_dinh.py <a.mp4> <b.mp4> ...
"""
import subprocess, sys
import numpy as np

def frames(p):
    w, h = map(int, subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout.strip().split(','))
    raw = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-i', p, '-vf', 'scale=480:270', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, 270, 480).astype(np.float32)

vids = sys.argv[1:]; F = [frames(v) for v in vids]
still = np.ones_like(F[0][0], bool)
for f in F: still &= np.abs(f[-1] - f[0]) < 6
for v, f in zip(vids, F):
    d = np.abs(np.diff(f, axis=0))[:, still]
    print(f'{v}: vùng tĩnh {still.mean()*100:.0f} % khung · chênh lệch khung liên tiếp TB {d.mean():.2f} mã · p99 {np.percentile(d, 99):.1f} mã')
