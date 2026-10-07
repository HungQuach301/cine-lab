#!/usr/bin/env python3
"""Đo judder (giật hình) trong video 24 fps — chuẩn kênh Last Lamplighters (CHUAN-KENH-LL §5.2).

Định nghĩa:
  - "Đoạn giữ khung" = chuỗi >= 2 khung liên tiếp giống hệt nhau (framemd5 của khung giải mã).
  - "Đứng hình giữa chuyển động" (lỗi) = đoạn giữ dài 2..12 khung (mặc định), KHÔNG nằm trong vùng
    tĩnh có chủ ý. Đoạn >= 24 khung (>= 1 s) coi là cố ý đứng yên; 13..23 khung báo riêng ("giữ ngắn").
  - Vùng tĩnh có chủ ý khai thêm bằng --tinh t0-t1 (giây), lặp được, hoặc --tinh-file (mỗi dòng "t0 t1").
  - --tol X: thay so khớp tuyệt đối bằng so gần đúng (ảnh xám 192x108, |chênh| trung bình <= X mức 0..255),
    để bắt khung "gần như đứng" do nén. Mặc định tuyệt đối (framemd5), đúng định nghĩa của chuẩn.
Ngoài ra đo "nhịp cập nhật": số khung khác khung trước trong từng giây; báo giây có nhịp thấp nhất
(bỏ giây hoàn toàn tĩnh).

Mục tiêu: loi == 0.

Dùng: python3 scripts/p/judder.py <video> [--min 2 --max 12] [--tinh 0-3.5 ...] [--tol 0.5] [--json out.json]
Mã thoát: 0 nếu loi == 0, 1 nếu có lỗi.
"""
import argparse, json, subprocess, sys


def ffprobe_fps(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                          'stream=r_frame_rate', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout.strip()
    n, d = out.split('/')
    return float(n) / float(d)


def hashes_exact(path):
    out = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-map', '0:v:0', '-f', 'framemd5', '-'],
                         capture_output=True, text=True, check=True).stdout
    hs = []
    for line in out.splitlines():
        if line.startswith('#') or not line.strip():
            continue
        hs.append(line.split(',')[-1].strip())
    return [hs[i] == hs[i - 1] for i in range(1, len(hs))], len(hs)


def hashes_tol(path, tol):
    import numpy as np
    w, h = 192, 108
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-map', '0:v:0', '-vf', f'scale={w}:{h},format=gray',
                          '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
    a = np.frombuffer(raw, dtype=np.uint8).reshape(-1, h, w).astype(np.int16)
    d = np.abs(np.diff(a, axis=0)).mean(axis=(1, 2))
    return [bool(x <= tol) for x in d], a.shape[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('video')
    ap.add_argument('--min', type=int, default=2)
    ap.add_argument('--max', type=int, default=12)
    ap.add_argument('--tinh', action='append', default=[], help='vùng tĩnh có chủ ý t0-t1 (giây)')
    ap.add_argument('--tinh-file')
    ap.add_argument('--tol', type=float, default=None)
    ap.add_argument('--json')
    ap.add_argument('--liet-ke', type=int, default=15, help='số đoạn lỗi in ra')
    a = ap.parse_args()

    fps = ffprobe_fps(a.video)
    same, n = hashes_tol(a.video, a.tol) if a.tol is not None else hashes_exact(a.video)
    zones = []
    for z in a.tinh:
        t0, t1 = z.split('-')
        zones.append((float(t0), float(t1)))
    if a.tinh_file:
        for line in open(a.tinh_file):
            p = line.split()
            if len(p) >= 2 and not line.startswith('#'):
                zones.append((float(p[0]), float(p[1])))

    # runs: chuỗi khung giống nhau; run gồm khung [s, e] (e bao gồm), dài L = e - s + 1
    runs, i = [], 0
    while i < len(same):
        if same[i]:
            j = i
            while j + 1 < len(same) and same[j + 1]:
                j += 1
            runs.append((i, j + 1))  # khung i..j+1
            i = j + 1
        else:
            i += 1

    def in_zone(s, e):
        t0, t1 = s / fps, (e + 1) / fps
        return any(t0 >= z0 - 1e-6 and t1 <= z1 + 1e-6 for z0, z1 in zones)

    loi, ngan, dai, trong_vung = [], [], [], []
    for s, e in runs:
        L = e - s + 1
        if in_zone(s, e):
            trong_vung.append((s, e)); continue
        if a.min <= L <= a.max:
            loi.append((s, e))
        elif a.max < L < round(fps):
            ngan.append((s, e))
        elif L >= round(fps):
            dai.append((s, e))

    # nhịp cập nhật mỗi giây (số khung mới trong giây), bỏ giây tĩnh hoàn toàn
    sec = int(round(fps))
    rates = []
    for k in range(0, n - 1, sec):
        seg = same[k:k + sec]
        if len(seg) < sec // 2:
            break
        moi = sum(1 for x in seg if not x)
        if moi > 0:
            rates.append((k / fps, moi * sec / len(seg)))
    rates_sorted = sorted(rates, key=lambda r: r[1])
    hist = {}
    for s, e in loi:
        L = e - s + 1
        hist[L] = hist.get(L, 0) + 1
    loi_khung = sum(e - s + 1 for s, e in loi)
    kq = {
        'video': a.video, 'fps': fps, 'so_khung': n, 'thoi_luong_s': round(n / fps, 3),
        'che_do': 'framemd5' if a.tol is None else f'tol {a.tol}',
        'nguong_loi_khung': [a.min, a.max],
        'loi': len(loi), 'loi_khung': loi_khung, 'loi_ty_le_thoi_luong': round(loi_khung / n, 4),
        'loi_histogram': dict(sorted(hist.items())),
        'giu_ngan_13_23': len(ngan), 'giu_co_y_ge_1s': len(dai), 'trong_vung_tinh_khai': len(trong_vung),
        'nhip_cap_nhat_thap_nhat': [{'t': round(t, 2), 'khung_moi_moi_giay': round(r, 1)} for t, r in rates_sorted[:5]],
        'giay_nhip_duoi_12': sum(1 for _, r in rates if r < 12),
        'loi_dau': [{'t0': round(s / fps, 3), 'khung': e - s + 1} for s, e in loi[:a.liet_ke]],
    }
    print(json.dumps(kq, ensure_ascii=False, indent=1))
    if a.json:
        json.dump(kq, open(a.json, 'w'), ensure_ascii=False, indent=1)
    sys.exit(0 if not loi else 1)


if __name__ == '__main__':
    main()
