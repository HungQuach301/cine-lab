#!/opt/cine/bin/python -I
"""NC-N2P · GHÉP lớp (a) cho VIDEO AI (Omni) theo mặt nạ ID TỪNG KHUNG + xuất bản so.
Mỗi khung t: ra Omni (24 fps) → căn về khung nguồn bằng do_v2v.align (ECC affine trên độ lớn gradient, NC-V2V, không sửa) → [tuỳ chọn khớp màu Reinhard về nguồn
trên lớp (c), một bộ hệ số cho CẢ clip, tránh nhấp nháy] → ghép (n2p_lib.ghep: vùng (a) = điểm ảnh nguồn, viền mềm 3 px ra ngoài).
  ghep_video.py --src <thư mục rgb/*.jpg> --id <thư mục id/*.png> --f0 <khung đầu> --n 240 --ai <omni.mp4> --out <ghep.mp4> [--khop-mau] [--json <đo.json>]
Ra thêm: <out>.nguon.mp4 (nguồn mã hoá cùng tham số, để đo so), <out>.ai-can.mp4 (Omni đã căn, chưa ghép)."""
import argparse, glob, importlib.util, json, os, subprocess, sys
from pathlib import Path
import cv2, numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
import n2p_lib as L  # noqa: E402
sp = importlib.util.spec_from_file_location('d', str(L.REPO / 'design/k2v/v2v/do_v2v.py')); D = importlib.util.module_from_spec(sp); sp.loader.exec_module(D)


def writer(path, w, h):
    return subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{w}x{h}', '-r', '24', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '16',
                             '-pix_fmt', 'yuv420p', str(path)], stdin=subprocess.PIPE)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--src', required=True); ap.add_argument('--id', required=True); ap.add_argument('--f0', type=int, required=True); ap.add_argument('--n', type=int, default=240)
    ap.add_argument('--ai', required=True); ap.add_argument('--out', required=True); ap.add_argument('--khop-mau', action='store_true'); ap.add_argument('--json')
    a = ap.parse_args()
    O = D.frames(a.ai); n = min(a.n, len(O)); W, H = 1280, 720
    wo, wn, wa = writer(a.out, W, H), writer(a.out + '.nguon.mp4', W, H), writer(a.out + '.ai-can.mp4', W, H)
    stat, coef = [], None
    if a.khop_mau:   # hệ số Reinhard từ 5 khung rải đều (một bộ cho cả clip)
        acc_a, acc_r = [], []
        for t in np.linspace(0, n - 1, 5).astype(int):
            s = cv2.imread(os.path.join(a.src, f'{a.f0 + t:05d}.jpg')); o = cv2.resize(O[t], (W, H)); Lb = L.idmap(os.path.join(a.id, f'{a.f0 + t:05d}.png'), (W, H)); C = ~L.lop_mask(Lb, L.LOP_A)
            acc_a.append(cv2.cvtColor(o, cv2.COLOR_BGR2LAB)[C].astype(np.float32)); acc_r.append(cv2.cvtColor(s, cv2.COLOR_BGR2LAB)[C].astype(np.float32))
        A_, R_ = np.concatenate(acc_a), np.concatenate(acc_r); coef = (A_.mean(0), A_.std(0) + 1e-6, R_.mean(0), R_.std(0) + 1e-6)
    for t in range(n):
        s = cv2.imread(os.path.join(a.src, f'{a.f0 + t:05d}.jpg')); o = cv2.resize(O[t], (W, H), interpolation=cv2.INTER_AREA)
        oa = align_full(s, o)   # căn ở 1280×720: ECC trên ảnh thu 1/2 (cùng ý do_v2v.align) rồi phóng ma trận
        if coef is not None:
            lab = cv2.cvtColor(oa, cv2.COLOR_BGR2LAB).astype(np.float32); lab = (lab - coef[0]) * (coef[3] / coef[1]) + coef[2]; oa = cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
        Lb = L.idmap(os.path.join(a.id, f'{a.f0 + t:05d}.png'), (W, H)); A = L.lop_mask(Lb, L.LOP_A)
        g, _ = L.ghep(s, oa, A, 3)
        dif = np.abs(g.astype(np.int16) - s.astype(np.int16)).max(-1)
        stat.append(dict(t=t, max_trong_a=int(dif[A].max()) if A.any() else 0, a_pct=round(float(A.mean() * 100), 2)))
        wo.stdin.write(g.tobytes()); wn.stdin.write(s.tobytes()); wa.stdin.write(oa.tobytes())
    for w in (wo, wn, wa): w.stdin.close(); w.wait()
    R = dict(ai=a.ai, sha_ai=L.sha_file(a.ai), out=a.out, sha_out=L.sha_file(a.out), n=n, khop_mau=bool(a.khop_mau), max_trong_a_moi_khung=max(x['max_trong_a'] for x in stat),
             ghi_chu='max_trong_a đo TRƯỚC mã hoá H.264 (sau mã hoá lệch do nén, không phải do AI)')
    if a.json: json.dump(R, open(a.json, 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(R, ensure_ascii=False))


def align_full(s, o):
    """căn khung Omni về nguồn ở 1280×720: ECC affine trên độ lớn gradient (thu 1/2), loại nghiệm phi lý (|tỉ lệ − 1| > 5 %, dịch > 40 px) → giữ nguyên."""
    def gm(b):
        g = cv2.cvtColor(cv2.resize(b, (640, 360), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY).astype(np.float32)
        return cv2.GaussianBlur(np.hypot(cv2.Sobel(g, cv2.CV_32F, 1, 0), cv2.Sobel(g, cv2.CV_32F, 0, 1)), (0, 0), 1.5)
    M = np.eye(2, 3, dtype=np.float32)
    try:
        _, M = cv2.findTransformECC(gm(s), gm(o), M, cv2.MOTION_AFFINE, (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 60, 1e-5), None, 5)
    except cv2.error:
        return o
    sc = np.sqrt(abs(np.linalg.det(M[:, :2])))
    if abs(sc - 1) > 0.05 or np.abs(M[:, 2]).max() > 20: return o
    M2 = M.copy(); M2[:, 2] *= 2
    return cv2.warpAffine(o, M2, (s.shape[1], s.shape[0]), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REFLECT)


if __name__ == '__main__': main()
