#!/opt/cine/bin/python
"""K-1.17.4 · K117-D8 — HIỆU CHUẨN thước biến cố video (checks/ll/q_bcv.py) trên master T3 bản cuối (SHA 5b9f0bcc…).
Tham chiếu (không tự khai — đều từ đặc tả/timeline đã khoá):
  CẮT   = ranh shot (timeline tổng hợp từ đặc tả) ∪ ranh góc máy `goc_may[].t0` > 0 (log shot bản cuối) ∪ beat `cut` khớp mốc đặc tả ±0,3 s
  BEAT  = beat khai (không phải `cut`) KHỚP mốc đặc tả 1.17.3 ±0,3 s (đúng phần Q37 (a) nhận)
  MỐC   = mốc đặc tả 1.17.3 (spec_times tl_moc) — chỉ để báo độ chính xác (mốc không phủ đổi liên tục giữa hai mốc)
  TĨNH  = quãng khung tĩnh theo khung neo Q37 (1.13) (mọi khung khác khung đầu < 2/255) ≥ 2 s VÀ tĩnh THEO Ô: mọi ô 8 × 6 (xám 160×90) lệch TB so khung
          đầu < 3/255 suốt quãng → mọi biến cố bên trong là báo NHẦM. (Đo 23/10: chỉ 2/25 quãng tĩnh Q37 (1.13) là tĩnh theo ô; 23 quãng kia có ô đổi
          tới 52/255 — đổi cục bộ thật mà trung bình toàn khung không thấy, nên không dùng làm chuẩn "không biến cố".)
  TỔNG HỢP = 6 khung T3 làm clip 10 s chỉ có máy đi (trượt 2 %/s + phóng 1,5 %/s + quay 0,5°/s, H.264 CRF 18): báo nhầm; cùng clip có
             một vật đổi cục bộ (ô 5 % bề ngang lấy từ khung khác) ở 5,0 s: phải bắt trong ±0,25 s.
Tiêu chí ĐẠT (đặt TRƯỚC khi đo, ghi ở q_bcv.HC_*; sửa một lần trước lượt đo đầy đủ — xem báo cáo): R cắt ≥ 95 % · R beat ≥ 70 % · sai số giờ
trung vị ≤ 0,25 s · báo nhầm ≤ 1/phút trong quãng TĨNH và 0 trên clip chỉ máy đi · bắt 6/6 vật đổi tổng hợp. Độ chính xác so MỐC chỉ báo.
Chọn (θ, k) trên NỬA ĐẦU (t < T/2), kiểm trên NỬA SAU; báo cả hai.
  hieu_chuan_bcv.py <master.mp4> <episode.yaml> <timeline.json> <log-shot.json> <thư mục ra> [--song-song 3]"""
import json, os, subprocess, sys, itertools, multiprocessing as mp
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')); sys.path.insert(0, ROOT)
from checks.ll import q_bcv as B, q_nhip as N, base  # noqa: E402

LUOI = list(itertools.product((4.0, 6.0, 8.0, 12.0), (1.5, 2.0, 3.0)))
FR_T = (20.0, 140.0, 260.0, 380.0, 500.0, 620.0)
TINH_O = 3.0


def tham_chieu(E, TL, LS):
    V = N.view(E, TL); moc, beat, cat, t_abs = [], [], set(B.ranh_shot(TL)), 0.0
    for sid, dur, HZ, shots, BT in V:
        T = N.spec_times(HZ, shots, dur, True); moc += [t_abs + x for x in T if x < dur]
        for b in BT or []:
            t = N.num(b.get('t'))
            if t is None or not any(abs(t - x) <= N.TOL for x in T): continue
            (cat.add(round(t_abs + t, 3)) if b.get('k') == 'cut' else beat.append(round(t_abs + t, 3)))
        t_abs += dur
    SP = {s['id']: float(s['t0']) for s in TL['segments']}
    for x in LS:
        a = SP.get(x.get('shot'), x.get('t0'))
        for g in x.get('goc_may') or []:
            t0 = N.num(g.get('t0', g.get('t')))
            if a is not None and t0 and t0 > 0: cat.add(round(float(a) + t0, 3))
    cat = sorted(cat); C = []
    for c in cat:
        if c > 0.05 and (not C or c - C[-1] > 0.1): C.append(c)
    return sorted(set(round(m, 3) for m in moc)), sorted(set(beat)), C, t_abs


def _clip(master, t, out, doi=False):
    import cv2, numpy as np
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', master, '-frames:v', '1', '-vf', 'scale=1280:720', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], capture_output=True, check=True).stdout
    F = np.frombuffer(raw, np.uint8).reshape(720, 1280, 3)
    raw2 = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t + 97.0), '-i', master, '-frames:v', '1', '-vf', 'scale=1280:720', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], capture_output=True, check=True).stdout
    F2 = np.frombuffer(raw2, np.uint8).reshape(720, 1280, 3)
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', '1280x720', '-r', '24', '-i', '-', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    s = 64; x0, y0 = 760, 300   # ô đổi 64 px = 5 % bề ngang
    for f in range(240):
        tt = f / 24; G = F.copy()
        if doi and tt >= 5.0: G[y0:y0 + s, x0:x0 + s] = F2[y0:y0 + s, x0:x0 + s]
        M = cv2.getRotationMatrix2D((640, 360), 0.5 * tt, 1.0 + 0.015 * tt); M[0, 2] += -0.02 * 1280 * tt
        p.stdin.write(cv2.warpAffine(G, M, (1280, 720), borderMode=cv2.BORDER_REFLECT).tobytes())
    p.stdin.close(); p.wait(); return out


def _chay(args):
    mp4, th, k, out = args
    f = os.path.join(out, f'ev-{th:g}-{k:g}-{os.path.basename(mp4)}.json')
    if not os.path.exists(f):
        R = B.do_video(mp4, th, k); json.dump(dict(su_kien=R['su_kien'], cat=R['cat'], n_khung=R['n_khung'], thong_so=R['thong_so']), open(f, 'w'))
    return f


def danh_gia(ev, cat, moc, beat, tinh, a, b):
    E = [e[0] for e in ev if a <= e[0] < b]; U = B.gop(E)
    C = [c for c in cat if a <= c < b]; BT = [x for x in beat if a <= x < b]; M = [m for m in moc if a <= m < b]
    _, nc, dc = B.khop(U, C); _, nb, db = B.khop(U, BT); pm, _, _ = B.khop(U, M + C + BT)
    sh = [B.khop([u + d for u in U], M + C + BT)[0] / max(1, len(U)) * 100 for d in (1.1, -1.3, 1.7, -2.3, 2.9)]
    fp, tl = 0, 0.0
    for L, s0 in tinh:
        if a <= s0 < b and L >= 2.0:
            tl += L - 0.5; fp += sum(1 for u in U if s0 + 0.25 < u < s0 + L - 0.25)
    import statistics
    return dict(n=len(U), R_cat=round(100 * nc / max(1, len(C)), 1), n_cat=len(C), R_beat=round(100 * nb / max(1, len(BT)), 1), n_beat=len(BT),
                dt_tv=round(statistics.median(dc + db), 3) if dc + db else None, P_moc=round(100 * pm / max(1, len(U)), 1), P_ngau_nhien=round(sum(sh) / len(sh), 1),
                tinh_s=round(tl, 1), bao_nham_tinh=fp, bao_nham_phut=round(fp / (tl / 60), 2) if tl else 0.0)


def main():
    a = sys.argv[1:]; master, ep, tlp, lsp, out = a[:5]; os.makedirs(out, exist_ok=True)
    nj = int(a[a.index('--song-song') + 1]) if '--song-song' in a else 3
    E = base.load(ep); TL = json.load(open(tlp)); LS = json.load(open(lsp)); LS = LS.get('shots', LS) if isinstance(LS, dict) else LS
    moc, beat, cat, T = tham_chieu(E, TL, LS)
    import numpy as np
    G = N.gray160(master); tinh = []
    for L, s0 in N.static_anchor(G):
        f0 = int(round(s0 * 24)); f1 = f0 + int(round(L * 24))
        if L >= 2.0 and float(np.abs(G[f0:f1] - G[f0]).reshape(f1 - f0, 6, 15, 8, 20).mean(axis=(2, 4)).max()) < TINH_O: tinh.append((L, s0))
    N._G.clear()
    syn = [(_clip(master, t, os.path.join(out, f'syn-{int(t)}.mp4')), _clip(master, t, os.path.join(out, f'syn-{int(t)}-doi.mp4'), True)) for t in FR_T]
    jobs = [(master, th, k, out) for th, k in LUOI] + [(c, th, k, out) for th, k in LUOI for pair in syn for c in pair]
    with mp.Pool(nj) as P: P.map(_chay, jobs, chunksize=1)
    KQ = []
    for th, k in LUOI:
        R = json.load(open(os.path.join(out, f'ev-{th:g}-{k:g}-{os.path.basename(master)}.json')))
        h1 = danh_gia(R['su_kien'], cat, moc, beat, tinh, 0.0, T / 2); h2 = danh_gia(R['su_kien'], cat, moc, beat, tinh, T / 2, T + 1)
        ca = danh_gia(R['su_kien'], cat, moc, beat, tinh, 0.0, T + 1)
        sn, sb = 0, 0
        for c0, c1 in syn:
            e0 = json.load(open(os.path.join(out, f'ev-{th:g}-{k:g}-{os.path.basename(c0)}.json')))['su_kien']
            e1 = json.load(open(os.path.join(out, f'ev-{th:g}-{k:g}-{os.path.basename(c1)}.json')))['su_kien']
            sn += len(B.gop([e[0] for e in e0])); sb += int(any(abs(e[0] - 5.0) <= 0.25 for e in e1))
        def dat(h): return (h['R_cat'] >= B.HC_R_CAT and h['R_beat'] >= B.HC_R_BEAT and (h['dt_tv'] or 9) <= B.HC_DT and h['bao_nham_phut'] <= 1.0)
        KQ.append(dict(theta=th, k=k, nua_dau=h1, nua_sau=h2, ca_phim=ca, tong_hop=dict(bao_nham_chi_may=sn, bat_vat_doi=f'{sb}/{len(syn)}'),
                       dat_nua_dau=dat(h1) and sn == 0 and sb == len(syn), dat_nua_sau=dat(h2) and sn == 0 and sb == len(syn)))
    ung = [x for x in KQ if x['dat_nua_dau']]
    chon = min(ung, key=lambda x: (x['nua_dau']['bao_nham_tinh'], -x['nua_dau']['R_beat'], -x['theta'])) if ung else None
    ra = dict(master_sha='5b9f0bccd88830ab212a6747259ac597328ae87bb964addc953bf1928fd7b682', tong_s=T, so_tham_chieu=dict(cat=len(cat), beat=len(beat), moc=len(moc), tinh=len(tinh)),
              tieu_chi=dict(R_cat=B.HC_R_CAT, R_beat=B.HC_R_BEAT, dt_tv=B.HC_DT, bao_nham_tinh_phut=1.0, bao_nham_chi_may=0, bat_vat_doi='6/6'),
              luoi=KQ, chon=dict(theta=chon['theta'], k=chon['k'], dat_nua_sau=chon['dat_nua_sau']) if chon else None)
    json.dump(ra, open(os.path.join(out, 'hieu-chuan-bcv.json'), 'w'), ensure_ascii=False, indent=1)
    for x in KQ: print(x['theta'], x['k'], 'đầu', x['nua_dau'], '\n   sau', x['nua_sau'], x['tong_hop'], x['dat_nua_dau'], x['dat_nua_sau'])
    print('CHỌN', ra['chon'])


if __name__ == '__main__':
    main()
