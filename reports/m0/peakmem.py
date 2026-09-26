#!/opt/cine/bin/python
"""Chạy lệnh, lấy mẫu RSS toàn cây tiến trình mỗi 0,25 s; ghi thời gian thực và RSS đỉnh (MB) ra file JSON.
Dùng: peakmem.py OUT.json -- cmd args..."""
import json, subprocess, sys, time, psutil
out, cmd = sys.argv[1], sys.argv[sys.argv.index('--') + 1:]
t0 = time.time(); p = subprocess.Popen(cmd); pp = psutil.Process(p.pid); peak = 0; cpu = []
while p.poll() is None:
    try:
        procs = [pp] + pp.children(recursive=True)
        peak = max(peak, sum(x.memory_info().rss for x in procs if x.is_running()))
    except psutil.Error: pass
    time.sleep(0.25)
res = {'cmd': ' '.join(cmd), 'exit': p.returncode, 'wall_s': round(time.time() - t0, 2), 'peak_rss_mb': round(peak / 2**20, 1)}
json.dump(res, open(out, 'w'), indent=1); print(json.dumps(res), file=sys.stderr); sys.exit(p.returncode)
