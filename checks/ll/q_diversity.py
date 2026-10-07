#!/opt/cine/bin/python
"""Q26 đa dạng hình — luật khoá LL v3 (phiên K, 07/10/2026). Định nghĩa: checks/ll/RULES-LL.md.

  q_diversity.py <video> [<video> …] [--tl timeline.json] [--json ra.json]
      nhiều video = các phần nối tiếp của một tập; --tl: ranh giới shot thật (nhà máy LL).

Ba chỉ số (chủ dự án, CHUAN-KENH §11.2; ngưỡng giữ nguyên):
  KHUNG NHÌN ≥ 40 · TỶ LỆ khung nhìn lớn nhất ≤ 20 % · CẢNH LIỀN CÙNG BỐ CỤC ≤ 2.
Đo (bản khoá, khác thước P ở 3 điểm; lý do trong reports/checks-ll-v3/BAO-CAO.md):
  1. Mẫu: lưới 0,5 s (ffmpeg fps=2), thu về 32×18 xám (area). Chia lưới thành 6 PHA, mỗi pha 1 mẫu/3 s
     (đúng mật độ chủ dự án định). Khung nhìn và tỷ lệ tính trên từng pha; kết quả = pha XẤU NHẤT
     (ít khung nhìn nhất, tỷ lệ lớn nhất). Thước P dùng 1 pha nên tập 1 dao động 14–22 % chỉ vì pha.
  2. Khung nhìn = cụm LIÊN KẾT ĐẦY ĐỦ: mọi cặp mẫu trong cụm chênh trung bình tuyệt đối < 12/255 (thước P: so với mẫu
     đầu cụm, phụ thuộc thứ tự). Xám THÔ, không chuẩn hoá: cảnh tối lặp lại là lặp thật (tập 6 v1).
  3. Cảnh liền cùng bố cục: cảnh = khoảng giữa hai ranh giới shot thật (timeline: mọi đầu shot, kể cả fade);
     không có timeline thì dò chuyển cảnh toàn khung (≥ 40 % ô 16×9 đổi > 25 trong 1 s). Khung đại diện mỗi cảnh = mẫu
     trung tâm (medoid) trong [đầu + 0,75 s, cuối − 0,75 s]; cảnh ngắn hơn 1,5 s bỏ qua. Hai cảnh liền nhau CÙNG BỐ CỤC khi
     khung đại diện cùng khung nhìn (chênh < 12) SAU KHI chuẩn hoá: trừ độ sáng trung bình, nâng tương phản (độ lệch chuẩn)
     của khung tối lên sàn 40 (khung đủ tương phản giữ nguyên). Không còn gộp mọi cảnh tối thành một bố cục.
"""
import json, os, re, subprocess, sys
import numpy as np

W, H, FPS = 32, 18, 2              # mẫu 0,5 s
PHASES = 6                         # 6 pha × 0,5 s = 1 mẫu / 3 s mỗi pha
TOL_VIEW = 12.0                    # /255, chủ dự án
S0 = 40.0                          # sàn tương phản khi so bố cục
TOL_RUN = 12.0                     # cùng bố cục = cùng khung nhìn sau chuẩn hoá
EDGE = 0.75                        # bỏ vùng chuyển (fade 0,7 s) ở hai đầu cảnh
DET_LAG, DET_CELL, DET_FRAC, DET_GAP = 2, 25.0, 0.4, 1.5
MIN_VIEWS, MAX_SHARE, MAX_RUN = 40, 20.0, 2


def dur(path):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path],
                                capture_output=True, text=True, check=True).stdout)


def samples(videos):
    """→ G (n, 18, 32) float32 xám, t (n,) giây tuyệt đối, part (n,) số phần"""
    G, T, P, off = [], [], [], 0.0
    for k, v in enumerate(videos):
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', v, '-vf', f'fps={FPS},scale={W}:{H}:flags=area,format=gray', '-f', 'rawvideo', '-'],
                             capture_output=True, check=True).stdout
        g = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)
        G.append(g); T.append(off + np.arange(len(g)) / FPS); P.append(np.full(len(g), k)); off += dur(v)
    return np.concatenate(G), np.concatenate(T), np.concatenate(P), off


def mad(A):
    """ma trận chênh trung bình tuyệt đối giữa các mẫu"""
    A = A.reshape(len(A), -1); out = np.empty((len(A), len(A)), np.float32)
    for i in range(len(A)): out[i] = np.abs(A - A[i]).mean(1)
    return out


def complete_link(D, tol):
    """gom cụm liên kết đầy đủ: lặp gộp hai cụm có khoảng cách xa nhất giữa hai phần tử nhỏ nhất, khi khoảng cách đó < tol.
    Hoà: cặp (i, j) nhỏ nhất. Không phụ thuộc thứ tự mẫu. → nhãn (n,)"""
    n = len(D); C = D.astype(np.float64).copy(); np.fill_diagonal(C, np.inf)
    alive = np.ones(n, bool); lab = np.arange(n)
    while True:
        M = np.where(alive[:, None] & alive[None, :], C, np.inf)
        k = int(np.argmin(M)); i, j = divmod(k, n)
        if not M[i, j] < tol: break
        if j < i: i, j = j, i
        C[i, :] = np.maximum(C[i, :], C[j, :]); C[:, i] = C[i, :]; C[i, i] = np.inf
        alive[j] = False; lab[lab == j] = i
    _, lab = np.unique(lab, return_inverse=True)
    return lab


def phase_index(part, ph):
    return np.concatenate([np.where(part == p)[0][ph::PHASES] for p in np.unique(part)])


def views(G, part):
    out = []
    for ph in range(PHASES):
        idx = phase_index(part, ph); lab = complete_link(mad(G[idx]), TOL_VIEW); c = np.bincount(lab)
        out.append(dict(pha=ph, mau=len(idx), khung_nhin=int(len(c)), ty_le_lon_nhat=round(100.0 * c.max() / len(idx), 1), _idx=idx[lab == c.argmax()]))
    return out


def lift(X):
    m = X.mean(axis=(-2, -1), keepdims=True); s = X.std(axis=(-2, -1), keepdims=True)
    return (X - m) * np.maximum(1.0, S0 / np.maximum(s, 1.0))


def detect_cuts(G, t, part):
    """dò chuyển cảnh toàn khung khi không có timeline: ≥ 40 % ô 16×9 đổi > 25 (sau chuẩn hoá) giữa hai mẫu cách 1 s;
    lấy đỉnh cục bộ, cách nhau ≥ 1,5 s. Đối chiếu ranh giới thật tập 6: v2 bắt 50/59, đúng 50/54; v1 bắt 24/30, đúng 24/29."""
    X = lift(G); C = X.reshape(len(X), H // 2, 2, W // 2, 2).mean(axis=(2, 4)); ch = []
    for i in range(len(C) - DET_LAG):
        if part[i] != part[i + DET_LAG]: continue
        ch.append((t[i] + DET_LAG / FPS / 2, float((np.abs(C[i + DET_LAG] - C[i]) > DET_CELL).mean())))
    cuts = []
    for k, (tt, f) in enumerate(ch):
        if f >= DET_FRAC and f == max(x[1] for x in ch[max(0, k - 3):k + 4]) and (not cuts or tt - cuts[-1] >= DET_GAP): cuts.append(tt)
    bounds = set(round(float(x), 3) for x in cuts)
    for p in np.unique(part)[1:]: bounds.add(round(float(t[np.where(part == p)[0][0]]), 3))   # ranh giới phần là điểm cắt
    return sorted(bounds - {0.0})


def tl_cuts(TL):
    return sorted({round(sg['t0'] + sh['t0'], 3) for sg in TL['segments'] for sh in sg['shots']} - {0.0})


def where(t, TL):
    if not TL: return f'{int(t // 60)}:{t % 60:04.1f}'
    for s in TL['segments']:
        if s['t0'] <= t < s['t1']:
            sh = next((x for x in s['shots'] if x['t0'] <= t - s['t0'] < x['t1']), None)
            return f"{int(t // 60)}:{t % 60:04.1f} {s['id']}/{sh['tpl'] if sh else '?'}" + (f":{sh['p'].get('hero')}" if sh and sh['p'].get('hero') else '')
    return f'{int(t // 60)}:{t % 60:04.1f}'


def scene_run(G, t, cuts, T):
    B = [0.0] + list(cuts) + [T]; reps = []
    for a, b in zip(B, B[1:]):
        x = np.where((t >= a + EDGE) & (t <= b - EDGE))[0]
        if not len(x): continue
        F = lift(G[x]); D = np.abs(F[:, None] - F[None]).mean(axis=(2, 3)); reps.append((a, F[int(np.argmin(D.sum(1)))]))
    best, run, at, pairs = 1, 1, 0.0, []
    for i in range(1, len(reps)):
        d = float(np.abs(reps[i][1] - reps[i - 1][1]).mean()); pairs.append((reps[i][0], round(d, 1)))
        run = run + 1 if d < TOL_RUN else 1
        if run > best: best, at = run, reps[i - run + 1][0]
    return best, at, len(reps), pairs


def measure(G, t, part, T, TL=None):
    V = views(G, part); worst_n = min(V, key=lambda r: r['khung_nhin']); worst_s = max(V, key=lambda r: r['ty_le_lon_nhat'])
    cuts = tl_cuts(TL) if TL else detect_cuts(G, t, part)
    run, at, ns, pairs = scene_run(G, t, cuts, T)
    big = [where(float(t[i]), TL) for i in worst_s['_idx']]
    R = dict(khung_nhin=worst_n['khung_nhin'], ty_le_lon_nhat=worst_s['ty_le_lon_nhat'], canh_lien_cung_bo_cuc=run,
             chuoi_tu=where(at, TL), ranh_gioi='timeline' if TL else 'dò trên hình', so_canh=ns, so_ranh_gioi=len(cuts),
             theo_pha=[{k: v for k, v in r.items() if k != '_idx'} for r in V], cum_lon_nhat=big[:12],
             cap_cung_bo_cuc=[(where(a, TL), d) for a, d in pairs if d < TOL_RUN])
    R['ok'] = bool(R['khung_nhin'] >= MIN_VIEWS and R['ty_le_lon_nhat'] <= MAX_SHARE and run <= MAX_RUN)
    near = []
    if abs(R['khung_nhin'] - MIN_VIEWS) <= 0.05 * MIN_VIEWS: near.append(f"khung nhìn {R['khung_nhin']} (ngưỡng {MIN_VIEWS})")
    if abs(R['ty_le_lon_nhat'] - MAX_SHARE) <= 0.05 * MAX_SHARE: near.append(f"tỷ lệ lớn nhất {R['ty_le_lon_nhat']} % (ngưỡng {MAX_SHARE:.0f} %)")
    R['sat_nguong'] = near
    R['val'] = (f"khung nhìn {R['khung_nhin']} (≥ {MIN_VIEWS}) · lớn nhất {R['ty_le_lon_nhat']} % (≤ {MAX_SHARE:.0f} %) · "
                f"cảnh liền cùng bố cục {run} (≤ {MAX_RUN}, từ {R['chuoi_tu']}) · {R['so_canh']} cảnh ({R['ranh_gioi']})")
    return R


def check(videos, TL=None):
    G, t, part, T = samples(videos)
    return measure(G, t, part, T, TL)


if __name__ == '__main__':
    a = sys.argv[1:]; js = a[a.index('--json') + 1] if '--json' in a else None; tl = a[a.index('--tl') + 1] if '--tl' in a else None
    vids = [x for i, x in enumerate(a) if not x.startswith('--') and (i == 0 or a[i - 1] not in ('--json', '--tl'))]
    R = check(vids, json.load(open(tl)) if tl else None)
    print(f"Q26 {'ĐẠT' if R['ok'] else 'TRƯỢT'} · {R['val']}")
    for r in R['theo_pha']: print(f"  pha {r['pha']}: {r['mau']} mẫu · {r['khung_nhin']} khung nhìn · lớn nhất {r['ty_le_lon_nhat']} %")
    print('  cụm lớn nhất:', ', '.join(R['cum_lon_nhat']))
    if js: json.dump(R, open(js, 'w'), indent=1, ensure_ascii=False)
    sys.exit(0 if R['ok'] else 1)
