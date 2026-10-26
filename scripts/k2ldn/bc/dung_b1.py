#!/opt/cine/bin/python
"""BAN-CUOI-T4-B1 · hàng dựng sản xuất 1080p (P ≤ 2 tiến trình, chờ RAM ≥ 5 GB trước mỗi việc) — như dung_bc.py (dùng lại hàm lenh()), thêm:
mỗi việc XONG → ngay lập tức `bash scripts/k2ldn/bc/xong_b1.sh <tên>` (mã hoá D-B1 → SHA256SUMS + KHUNG → log máy vào git → commit → git lfs push → git push; khoá flock).
xong_b1.sh trả mã ≠ 0 (LFS/đẩy hỏng) → ghi /var/tmp/bc/DUNG-B1 và DỪNG nhận việc mới (lệnh D-B1: không dựng tiếp khi khung không giữ được).
  dung_b1.py <P> <viec.json> [ten …]       (BC_R mặc định /var/tmp/bc/r; tiến độ: $BC_R/tien-do-b1.jsonl)"""
import json, os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dung_bc as DB    # noqa: E402
R = DB.R; REPO = DB.REPO; STOP = '/var/tmp/bc/DUNG-B1'


def ghi_td(**kw):
    with open(f'{R}/tien-do-b1.jsonl', 'a') as f: f.write(json.dumps(dict(kw, gio=time.strftime('%H:%M:%S', time.gmtime())), ensure_ascii=False) + '\n')


def main():
    P = int(sys.argv[1]); V = json.load(open(sys.argv[2])); chon = set(sys.argv[3:])
    J = [j for j in V if not chon or j['ten'] in chon]; run = []
    def xong(p, j, t0):
        rc = p.returncode; w = time.time() - t0
        try: lj = json.load(open(f"{R}/{j['ten']}/log.json")); spf = lj.get('s_per_frame'); setup = lj.get('setup_s'); n = len(lj['frames'])
        except Exception: spf = setup = n = None
        json.dump(dict(ten=j['ten'], rc=rc, wall_s=round(w, 1), s_per_frame=spf, setup_s=setup, khung=n, song_song=P), open(f"{R}/{j['ten']}.time.json", 'w'))
        ghi_td(ten=j['ten'], rc=rc, khung=n, s_khung=spf, wall_s=round(w, 1), setup_s=setup)
        print('XONG' if rc == 0 else 'LỖI', j['ten'], rc, round(w, 1), 's', spf, flush=True)
        if rc == 0:
            r2 = subprocess.run(['bash', os.path.join(REPO, 'scripts/k2ldn/bc/xong_b1.sh'), j['ten']], cwd=REPO)
            ghi_td(ten=j['ten'], xong_b1=r2.returncode)
            if r2.returncode != 0: open(STOP, 'w').write(f"xong_b1.sh {j['ten']} rc={r2.returncode} {time.strftime('%H:%M:%S', time.gmtime())}\n")
    for j in J:
        if os.path.exists(STOP): print('DỪNG (DUNG-B1):', open(STOP).read().strip(), flush=True); break
        if os.path.exists(f"{R}/{j['ten']}/log.json"): print('ĐÃ CÓ', j['ten']); continue
        while True:
            for x in [x for x in run if x[0].poll() is not None]: run.remove(x); xong(*x)
            if len(run) < P: break
            time.sleep(3)
        if os.path.exists(STOP): break
        while DB.ram_mb() < 5000: time.sleep(10)
        subprocess.run(['rm', '-rf', f"{R}/{j['ten']}"]); c = DB.lenh(j)
        lg = open(f"{R}/{j['ten']}.log", 'w'); p = subprocess.Popen(c, stdout=lg, stderr=subprocess.STDOUT, env=dict(os.environ, LDN_DATA=os.environ.get('LDN_DATA', '/var/tmp/ldn')))
        run.append((p, j, time.time())); ghi_td(ten=j['ten'], chay=True, khung_dat=len(j.get('only') or []))
        print('CHẠY', j['ten'], time.strftime('%H:%M:%S'), flush=True); time.sleep(5)
    while run:
        for x in [x for x in run if x[0].poll() is not None]: run.remove(x); xong(*x)
        time.sleep(3)
    print('DUNG-B1-XONG', flush=True)


if __name__ == '__main__': main()
