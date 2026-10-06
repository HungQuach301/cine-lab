#!/opt/cine/bin/python
"""Q26 đa dạng hình (chủ dự án, 06/10/2026; CHUAN-KENH §11.2). Luật làm việc của P cho tới khi K khoá.

  diversity.py <video> [<video> …] [--json ra.json] [--tl timeline.json]
      nhiều video = các phần nối tiếp của một tập (bản xem p1/p2/p3).

Đo đúng định nghĩa của chủ dự án:
  - mẫu 1 khung mỗi 3 s (giữa mỗi ô 3 s), thu về 32×18 xám (0–255);
  - gộp khung nhìn: một mẫu thuộc khung nhìn đã có nếu chênh trung bình tuyệt đối với đại diện của khung nhìn đó < 12/255
    (đại diện = mẫu đầu tiên của khung nhìn; xét theo thứ tự thời gian, gán vào khung nhìn gần nhất thoả ngưỡng);
  - KHUNG NHÌN = số cụm; TỶ LỆ LỚN NHẤT = số mẫu của cụm lớn nhất / tổng mẫu (≈ % thời lượng);
  - CẢNH LIỀN CÙNG BỐ CỤC: dãy mẫu gộp thành "cảnh" (mẫu liền nhau cùng cụm); bố cục = cụm ở ngưỡng lỏng 24/255;
    đếm chuỗi dài nhất các cảnh liền nhau có cùng bố cục (luật: ≤ 2).
Ngưỡng Q26: khung nhìn ≥ 40; tỷ lệ lớn nhất ≤ 20 %; cảnh liền cùng bố cục ≤ 2.
Có --tl: in thêm đoạn/shot ứng với cụm lớn nhất (để biết sửa ở đâu).
"""
import json, subprocess, sys
import numpy as np

STEP, W, H, TOL, TOL_LAYOUT = 3.0, 32, 18, 12.0, 24.0
MIN_VIEWS, MAX_SHARE, MAX_RUN = 40, 20.0, 2


def frames(path):
    """mẫu 1 khung/3 s (khung ở giữa mỗi ô) → mảng (n, 18, 32) xám"""
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(STEP / 2), '-i', path, '-vf', f'fps=1/{STEP},scale={W}:{H}:flags=area,format=gray',
                          '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)


def cluster(F, tol):
    reps, lab = [], []
    for f in F:
        d = [np.abs(f - r).mean() for r in reps]
        if d and min(d) < tol: lab.append(int(np.argmin(d)))
        else: reps.append(f); lab.append(len(reps) - 1)
    return np.array(lab), len(reps)


def measure(F):
    lab, n = cluster(F, TOL)
    cnt = np.bincount(lab); big = int(cnt.argmax()); share = 100.0 * cnt.max() / len(lab)
    lay, _ = cluster(F, TOL_LAYOUT)
    scenes = [0] + [i for i in range(1, len(lab)) if lab[i] != lab[i - 1]]   # chỉ số mẫu bắt đầu mỗi cảnh
    sl = [lay[i] for i in scenes]; run = best = 1; at = 0
    for i in range(1, len(sl)):
        run = run + 1 if sl[i] == sl[i - 1] else 1
        if run > best: best, at = run, scenes[i - run + 1]
    return dict(mau=len(lab), khung_nhin=n, ty_le_lon_nhat=round(share, 1), cum_lon_nhat=big, mau_cum_lon_nhat=[i for i in range(len(lab)) if lab[i] == big],
                canh=len(scenes), canh_lien_cung_bo_cuc=best, chuoi_bat_dau_s=round(at * STEP, 1),
                dat=bool(n >= MIN_VIEWS and share <= MAX_SHARE and best <= MAX_RUN))


def where(t, TL):
    for s in TL['segments']:
        if s['t0'] <= t < s['t1']:
            lt = t - s['t0']; sh = next((x for x in s['shots'] if x['t0'] <= lt < x['t1']), None)
            return f"{s['id']}/{sh['tpl'] if sh else '?'}"
    return '?'


if __name__ == '__main__':
    a = sys.argv[1:]; js = a[a.index('--json') + 1] if '--json' in a else None; tl = a[a.index('--tl') + 1] if '--tl' in a else None
    vids = [x for i, x in enumerate(a) if not x.startswith('--') and (i == 0 or a[i - 1] not in ('--json', '--tl'))]
    F = np.concatenate([frames(v) for v in vids]); R = measure(F)
    print(f"Q26 {'ĐẠT' if R['dat'] else 'TRƯỢT'} · khung nhìn {R['khung_nhin']} (≥ {MIN_VIEWS}) · lớn nhất {R['ty_le_lon_nhat']} % (≤ {MAX_SHARE:.0f} %) · "
          f"cảnh liền cùng bố cục {R['canh_lien_cung_bo_cuc']} (≤ {MAX_RUN}, từ {R['chuoi_bat_dau_s']} s) · {R['mau']} mẫu, {R['canh']} cảnh")
    if tl:
        TL = json.load(open(tl)); from collections import Counter
        c = Counter(where(i * STEP + STEP / 2, TL) for i in R['mau_cum_lon_nhat'])
        print('  cụm lớn nhất nằm ở:', ', '.join(f'{k} ×{v}' for k, v in c.most_common(8)))
    R.pop('mau_cum_lon_nhat')
    if js: json.dump(R, open(js, 'w'), indent=1, ensure_ascii=False)
    sys.exit(0 if R['dat'] else 1)
