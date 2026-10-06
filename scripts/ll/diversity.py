#!/opt/cine/bin/python
"""Q26 đa dạng hình (chủ dự án, 06/10/2026; CHUAN-KENH §11.2). Luật làm việc của P cho tới khi K khoá.

  diversity.py <video> [<video> …] [--json ra.json] [--tl timeline.json]
      nhiều video = các phần nối tiếp của một tập (bản xem p1/p2/p3).

Đo đúng định nghĩa của chủ dự án:
  - mẫu 1 khung mỗi 3 s (giữa mỗi ô 3 s), thu về 32×18 xám (0–255);
  - gộp khung nhìn: một mẫu thuộc khung nhìn đã có nếu chênh trung bình tuyệt đối với đại diện của khung nhìn đó < 12/255
    (đại diện = mẫu đầu tiên của khung nhìn; xét theo thứ tự thời gian, gán vào khung nhìn gần nhất thoả ngưỡng);
  - KHUNG NHÌN = số cụm; TỶ LỆ LỚN NHẤT = số mẫu của cụm lớn nhất / tổng mẫu (≈ % thời lượng);
  - CẢNH LIỀN CÙNG BỐ CỤC: "cảnh" = khoảng giữa hai điểm cắt thật (ffmpeg scdet, ngưỡng 4 trên khung 160×90 (đo trên tập 1: 52 điểm cắt); dissolve chậm có thể
    không bắt được); bố cục của cảnh = cụm (ngưỡng lỏng 24/255) chiếm đa số trong các mẫu của cảnh; cảnh < 3 s không có mẫu thì bỏ qua.
    Đếm chuỗi dài nhất các cảnh liền nhau cùng bố cục (luật: ≤ 2).
    Ghi thêm số đo cũ "chuỗi mẫu" (cảnh = các mẫu liền nhau cùng cụm 12/255) để so với chuẩn gốc đã báo cáo (06/10/2026).
Ngưỡng Q26: khung nhìn ≥ 40; tỷ lệ lớn nhất ≤ 20 %; cảnh liền cùng bố cục ≤ 2.
Có --tl: in thêm đoạn/shot ứng với cụm lớn nhất (để biết sửa ở đâu).
"""
import json, re, subprocess, sys
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


def cuts(path):
    """điểm cắt (giây) bằng ffmpeg scdet"""
    r = subprocess.run(['ffmpeg', '-v', 'info', '-nostats', '-i', path, '-vf', 'scale=160:90,scdet=threshold=4', '-an', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return [float(x) for x in re.findall(r'lavfi\.scd\.time: ([\d.]+)', r)]


def dur(path):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout)


def scene_run(lay, C, T):
    """chuỗi dài nhất các cảnh (khoảng giữa điểm cắt) liền nhau cùng bố cục"""
    edges = [0.0] + sorted(C) + [T]; seq = []
    for a, b in zip(edges, edges[1:]):
        idx = [i for i in range(len(lay)) if a <= i * STEP + STEP / 2 < b]
        if idx: seq.append((np.bincount([lay[i] for i in idx]).argmax(), a))
    best, run, at = 1, 1, 0.0
    for i in range(1, len(seq)):
        run = run + 1 if seq[i][0] == seq[i - 1][0] else 1
        if run > best: best, at = run, seq[i - run + 1][1]
    return best, at, len(seq)


def measure(F, C=None, T=None):
    lab, n = cluster(F, TOL)
    cnt = np.bincount(lab); big = int(cnt.argmax()); share = 100.0 * cnt.max() / len(lab)
    lay, _ = cluster(F, TOL_LAYOUT)
    scenes = [0] + [i for i in range(1, len(lab)) if lab[i] != lab[i - 1]]   # chỉ số mẫu bắt đầu mỗi cảnh
    sl = [lay[i] for i in scenes]; run = best = 1; at = 0
    for i in range(1, len(sl)):
        run = run + 1 if sl[i] == sl[i - 1] else 1
        if run > best: best, at = run, scenes[i - run + 1]
    R = dict(mau=len(lab), khung_nhin=n, ty_le_lon_nhat=round(share, 1), cum_lon_nhat=big, mau_cum_lon_nhat=[i for i in range(len(lab)) if lab[i] == big],
             chuoi_mau=best, chuoi_mau_tu_s=round(at * STEP, 1))
    if C is not None:
        r2, at2, ns = scene_run(lay, C, T); R.update(canh=ns, diem_cat=len(C), canh_lien_cung_bo_cuc=r2, chuoi_bat_dau_s=round(at2, 1))
    else: R.update(canh=len(scenes), canh_lien_cung_bo_cuc=best, chuoi_bat_dau_s=round(at * STEP, 1))
    R['dat'] = bool(n >= MIN_VIEWS and share <= MAX_SHARE and R['canh_lien_cung_bo_cuc'] <= MAX_RUN)
    return R


def where(t, TL):
    for s in TL['segments']:
        if s['t0'] <= t < s['t1']:
            lt = t - s['t0']; sh = next((x for x in s['shots'] if x['t0'] <= lt < x['t1']), None)
            return f"{s['id']}/{sh['tpl'] if sh else '?'}"
    return '?'


if __name__ == '__main__':
    a = sys.argv[1:]; js = a[a.index('--json') + 1] if '--json' in a else None; tl = a[a.index('--tl') + 1] if '--tl' in a else None
    vids = [x for i, x in enumerate(a) if not x.startswith('--') and (i == 0 or a[i - 1] not in ('--json', '--tl'))]
    F, C, off = [], [], 0.0
    for v in vids:
        f = frames(v); F.append(f); C += [off + c for c in cuts(v)]; d = dur(v)
        if off > 0: C.append(off)   # nối phần: ranh giới phần là điểm cắt
        off += d
    F = np.concatenate(F); R = measure(F, C, off)
    print(f"Q26 {'ĐẠT' if R['dat'] else 'TRƯỢT'} · khung nhìn {R['khung_nhin']} (≥ {MIN_VIEWS}) · lớn nhất {R['ty_le_lon_nhat']} % (≤ {MAX_SHARE:.0f} %) · "
          f"cảnh liền cùng bố cục {R['canh_lien_cung_bo_cuc']} (≤ {MAX_RUN}, từ {R['chuoi_bat_dau_s']} s) · {R['mau']} mẫu, {R['canh']} cảnh, {R.get('diem_cat')} điểm cắt"
          f" · [đo cũ: chuỗi mẫu {R['chuoi_mau']}]")
    if tl:
        TL = json.load(open(tl)); from collections import Counter
        c = Counter(where(i * STEP + STEP / 2, TL) for i in R['mau_cum_lon_nhat'])
        print('  cụm lớn nhất nằm ở:', ', '.join(f'{k} ×{v}' for k, v in c.most_common(8)))
    R.pop('mau_cum_lon_nhat')
    if js: json.dump(R, open(js, 'w'), indent=1, ensure_ascii=False)
    sys.exit(0 if R['dat'] else 1)
