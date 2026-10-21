#!/opt/cine/bin/python -I
"""NC-N2P · THỬ TIMELAPSE O1 ở MỘT điểm máy cố định qua 2 mốc: TẤM NỀN AI mỗi mốc (OpenAI sửa ảnh, không mặt nạ, khớp màu về render của mốc đó trên lớp (c))
+ LỚP DỮ KIỆN và VẬT CHUYỂN ĐỘNG từ render từng khung (mặt nạ ID từng khung: mọi lớp (a), kể cả người/đơn vị/chim) ; chuyển tấm bằng HOÀ MỜ (và bản CẮT CỨNG để so).
Đo: (1) nhấp nháy vùng tĩnh lớp (c) NGOÀI cửa sổ hoà (định nghĩa do_v2v.py: xám 160×90, vùng tĩnh = |nguồn_t − nguồn_t−1| < 0,5/255) — TB |ra_t − ra_t−1| so với render;
    (2) bước nhảy chuyển tấm = max theo khung của ΔE76 TB lớp (c) giữa hai khung liền (ra) ÷ trung vị cả clip; (3) khớp ánh sáng nền ↔ vật render = lech_vien (n2p_lib) mỗi 24 khung.
  timelapse.py --src /var/tmp/n2p/src/c4/rgb --id /var/tmp/n2p/src/c4/id --f0 144 --n 288 --p1 tam1.jpg --f1 168 --p2 tam2.jpg --f2 408 --hoa 264,312 --out <thư mục>"""
import argparse, json, os, subprocess, sys
from pathlib import Path
import cv2, numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
import n2p_lib as L  # noqa: E402


def lab(b): return cv2.cvtColor(b, cv2.COLOR_BGR2LAB).astype(np.float32) * np.array([100 / 255, 1, 1], np.float32)


def enc(frames_dir, pat, out, crf=14):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', '24', '-i', os.path.join(frames_dir, pat), '-c:v', 'libx264', '-crf', str(crf), '-pix_fmt', 'yuv420p', out], check=True)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--src'); ap.add_argument('--id'); ap.add_argument('--f0', type=int); ap.add_argument('--n', type=int)
    ap.add_argument('--p1'); ap.add_argument('--f1', type=int); ap.add_argument('--p2'); ap.add_argument('--f2', type=int); ap.add_argument('--hoa', default='264,312'); ap.add_argument('--out')
    a = ap.parse_args(); out = Path(a.out); W, H = 1280, 720; h0, h1 = map(int, a.hoa.split(','))
    rd = lambda f: cv2.imread(os.path.join(a.src, f'{f:05d}.jpg')); md = lambda f: L.idmap(os.path.join(a.id, f'{f:05d}.png'), (W, H))
    P = []
    for p, f in ((a.p1, a.f1), (a.p2, a.f2)):
        im = cv2.resize(cv2.imread(p), (W, H), interpolation=cv2.INTER_AREA); C = ~L.lop_mask(md(f), L.LOP_A); P.append(L.khop_mau(im, rd(f), C))
    res = {}
    for mode in ('hoa', 'cat'):
        d = out / mode; d.mkdir(parents=True, exist_ok=True); prev_o = prev_s = None; fl_o, fl_s, jump, viền = [], [], [], []
        for i in range(a.n):
            f = a.f0 + i; s = rd(f); Lb = md(f); A = L.lop_mask(Lb, L.LOP_A)
            w = (0.0 if f < h0 else 1.0 if f >= h1 else (f - h0) / (h1 - h0)) if mode == 'hoa' else (0.0 if f < (h0 + h1) // 2 else 1.0)
            base = np.clip(P[0].astype(np.float32) * (1 - w) + P[1].astype(np.float32) * w, 0, 255).astype(np.uint8)
            g, _ = L.ghep(s, base, A, 3); cv2.imwrite(str(d / f'{i:05d}.png'), g)
            if mode == 'hoa' and i == 0: cv2.imwrite(str(out / 'nguon-dau.jpg'), s)
            C = ~cv2.dilate(A.astype(np.uint8), np.ones((7, 7), np.uint8)).astype(bool)
            gs = cv2.resize(cv2.cvtColor(s, cv2.COLOR_BGR2GRAY), (160, 90), interpolation=cv2.INTER_AREA).astype(np.float32); go = cv2.resize(cv2.cvtColor(g, cv2.COLOR_BGR2GRAY), (160, 90), interpolation=cv2.INTER_AREA).astype(np.float32)
            Cs = cv2.resize(C.astype(np.uint8), (160, 90), interpolation=cv2.INTER_NEAREST).astype(bool)
            if prev_o is not None:
                st = (np.abs(gs - prev_s) < 0.5) & Cs
                if st.sum() > 50 and not (h0 <= f <= h1): fl_o.append(float(np.abs(go - prev_o)[st].mean())); fl_s.append(float(np.abs(gs - prev_s)[st].mean()))
                jump.append(float(np.sqrt(((lab(g) - lab(prevG)) ** 2).sum(-1))[C].mean()))
            if i % 24 == 0: viền.append(L.lech_vien(s, g, A))
            prev_o, prev_s, prevG = go, gs, g
        jm = np.array(jump); med = float(np.median(jm))
        res[mode] = dict(nhap_nhay_ra=round(float(np.mean(fl_o)), 4), nhap_nhay_render=round(float(np.mean(fl_s)), 4), nhap_nhay_ghi_chu='TB |Δ xám| /khung trên vùng tĩnh lớp (c), NGOÀI cửa sổ hoà (render tĩnh tuyệt đối → so bằng số tuyệt đối, không tỉ số)',
                         buoc_nhay_max_dE=round(float(jm.max()), 3), buoc_nhay_khung=int(a.f0 + 1 + jm.argmax()), buoc_nhay_trung_vi_dE=round(med, 3), buoc_nhay_ti_le=round(float(jm.max() / max(1e-6, med)), 1),
                         vien_dE_trung_vi=round(float(np.median([v['dE_trung_vi'] for v in viền if v.get('so_cum')])), 2), vien_dE_p90_max=round(float(max(v['dE_p90'] for v in viền if v.get('so_cum'))), 2))
        enc(str(d), '%05d.png', str(out / f'tl-{mode}.mp4'))
    json.dump(dict(f0=a.f0, n=a.n, moc=[a.f1, a.f2], hoa=[h0, h1], ket_qua=res), open(out / 'do-timelapse.json', 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(res, ensure_ascii=False))


if __name__ == '__main__': main()
