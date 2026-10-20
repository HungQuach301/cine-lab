#!/opt/cine/bin/python -I
"""NC-V2V3 · CHẾ ĐỘ C: nối c4A + c4B thành 20 s (khung 0–480 của C1a V7B) bằng chế độ tốt nhất (B2) theo CỬA SỔ NỐI TIẾP:
cửa sổ k dài 81 khung bắt đầu ở 72k (k = 0…5) và 400 (cửa sổ cuối); OV khung đầu mỗi cửa sổ k ≥ 1 là NGỮ CẢNH = khung ĐÃ RA (đã ghép) của cửa sổ trước,
mặt nạ 0 (giữ nguyên) ở cả hai lớp điều khiển và làm khung khởi; chuẩn hoá độ sâu CỐ ĐỊNH cho cả 20 s. Khung cuối = phần mới của mỗi cửa sổ.
  noi_c3.py <thư mục dung3 hợp nhất c4full> <thư mục làm việc> --disp lo,hi [--tu k]"""
import argparse, glob, json, os, shutil, subprocess, sys, time
import cv2, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); PY = '/opt/cine/bin/python'
STARTS, N = [0, 72, 144, 216, 288, 360, 400], 81


def sh(*a, **k): print('$', ' '.join(a)[:200], flush=True); return subprocess.run(list(a), check=True, **k)


def pod(*a): return sh(PY, os.path.join(HERE, 'pod3.py'), *a, capture_output=True, text=True).stdout


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('src'); ap.add_argument('wd'); ap.add_argument('--disp', required=True); ap.add_argument('--tu', type=int, default=0)
    a = ap.parse_args(); FIN = os.path.join(a.wd, 'final'); os.makedirs(FIN, exist_ok=True); log = open(os.path.join(a.wd, 'noi.jsonl'), 'a')
    for k, s in enumerate(STARTS):
        if k < a.tu: continue
        ov = 0 if k == 0 else STARTS[k - 1] + N - s; C = os.path.join(a.wd, f'w{k}'); lab = f'c4C-w{k}'
        if os.path.exists(C): shutil.rmtree(C)
        sh(PY, '-I', os.path.join(HERE, 'ctrl3.py'), a.src, C, '--s', str(s), '--n', str(N), '--disp', a.disp)
        os.makedirs(os.path.join(C, 'srcj'), exist_ok=True)
        for i in range(N):
            if i < ov:   # ngữ cảnh: khung đã ra của cửa sổ trước, giữ nguyên toàn khung
                prev = cv2.imread(os.path.join(FIN, f'{s + i:05d}.png'))
                for d in ('bdepth', 'bcanny'): cv2.imwrite(os.path.join(C, d, f'{i:05d}.jpg'), prev, [cv2.IMWRITE_JPEG_QUALITY, 95])
                cv2.imwrite(os.path.join(C, 'mask', f'{i:05d}.png'), np.zeros(prev.shape[:2], np.uint8)); cv2.imwrite(os.path.join(C, 'alpha', f'{i:05d}.png'), np.zeros(prev.shape[:2], np.uint8))
                cv2.imwrite(os.path.join(C, 'src', f'{i:05d}.png'), prev); cv2.imwrite(os.path.join(C, 'srcj', f'{i:05d}.jpg'), prev, [cv2.IMWRITE_JPEG_QUALITY, 95])
            else: cv2.imwrite(os.path.join(C, 'srcj', f'{i:05d}.jpg'), cv2.imread(os.path.join(C, 'src', f'{i:05d}.png')), [cv2.IMWRITE_JPEG_QUALITY, 95])
        tar = C + '.tar'; sh('tar', 'cf', tar, '-C', a.wd, *[f'w{k}/{d}' for d in ('mask', 'bdepth', 'bcanny', 'srcj')])
        pod('put', tar, f'ctrl/c4C/w{k}.tar'); pod('run', f'cd /w/ctrl/c4C && tar xf w{k}.tar', '--cho')
        jf = os.path.join(a.wd, f'{lab}.json'); sh(PY, os.path.join(HERE, 'mk_job3.py'), f'c4C/w{k}', 'B2', lab, jf, capture_output=True)
        pod('put', jf, f'jobs/{lab}.json'); t0 = time.time()
        out = pod('run', f'bash /w/v2v3/pod_batch.sh /w/jobs/{lab}.json; tail -n 1 /w/jobs/{lab}.log', '--cho')
        sh(PY, '-I', os.path.join(HERE, 'keo3.py'), f'ra/{lab}', os.path.join(a.wd, 'ra', lab), str(N))
        sh(PY, '-I', os.path.join(HERE, 'ghep3.py'), 'ra', C, os.path.join(a.wd, 'ra', lab), os.path.join(a.wd, 'g', lab), '--b')
        for i in range(ov, N): shutil.copy(os.path.join(a.wd, 'g', lab, 'khung', f'{i:05d}.png'), os.path.join(FIN, f'{s + i:05d}.png'))
        # ngữ cảnh bị mô hình vẽ lại? đo lệch TB |ra − ngữ cảnh| trên OV khung đầu (0 = giữ đúng)
        dv = [float(np.abs(cv2.imread(os.path.join(a.wd, 'g', lab, 'khung', f'{i:05d}.png')).astype(np.int16) - cv2.imread(os.path.join(C, 'src', f'{i:05d}.png')).astype(np.int16)).mean()) for i in range(ov)]
        rec = dict(k=k, start=s, ov=ov, nhan=lab, s_gpu=round(time.time() - t0, 1), ket=out.strip().splitlines()[-2:] if out else None, lech_ngu_canh_tb=round(float(np.mean(dv)), 3) if dv else None)
        log.write(json.dumps(rec, ensure_ascii=False) + '\n'); log.flush(); print(rec, flush=True)
    sh('ffmpeg', '-v', 'error', '-y', '-framerate', '24', '-i', os.path.join(FIN, '%05d.png'), '-c:v', 'libx264', '-preset', 'slow', '-crf', '12', '-pix_fmt', 'yuv420p', os.path.join(a.wd, 'c4C-B2-20s.mp4'))


if __name__ == '__main__': main()
