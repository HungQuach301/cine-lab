#!/opt/cine/bin/python -I
"""NC-V2V · (iii) ĐƯỜNG NỐI clip 4: hai đoạn ra A (giây 0–10) và B (giây 10–20) ghép tại khung 240.
  noi.py --src <nguồn 20 s.mp4> --a <ra A.mp4> --b <ra B.mp4> [--ab <ra nối liền 20 s.mp4>] --json <ra.json>
Số đo ở 640×360: ΔE76 TB (Lab) giữa khung cuối A và khung đầu B; cùng số trên nguồn (khung 239 ↔ 240) và trung vị ΔE khung kề TRONG đoạn (nền);
bước nhảy chi tiết = |Laplace| TB khung đầu B / khung cuối A; bước nhảy bão hoà / colorfulness / độ sáng; tỉ số bước nhảy ÷ nền (> 3 → nối thấy được)."""
import argparse, json
import cv2, numpy as np
import importlib.util, os
sp = importlib.util.spec_from_file_location('d', os.path.join(os.path.dirname(__file__), 'do_v2v.py')); d = importlib.util.module_from_spec(sp); sp.loader.exec_module(d)


def lab(b):
    x = cv2.cvtColor(b, cv2.COLOR_BGR2LAB).astype(np.float32); x[..., 0] *= 100 / 255; x[..., 1:] -= 128; return x


dE = lambda a, b: float(np.sqrt(((lab(a) - lab(b)) ** 2).sum(-1)).mean())


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--src'); ap.add_argument('--a'); ap.add_argument('--b'); ap.add_argument('--ab'); ap.add_argument('--json'); a = ap.parse_args()
    S = d.frames(a.src)
    if a.ab: X = d.frames(a.ab); A, B = X[:240], X[240:480]
    else: A, B = d.frames(a.a)[:240], d.frames(a.b)[:240]
    base = [dE(A[i], A[i + 1]) for i in range(len(A) - 13, len(A) - 1)] + [dE(B[i], B[i + 1]) for i in range(0, 12)]
    j = dE(A[-1], B[0]); js = dE(S[239], S[240]); la, lb = d.look(A[-1]), d.look(B[0]); sa, sb = d.look(S[239]), d.look(S[240])
    # màu TB 1 s mỗi bên (độ lệch màu bền, không phải nhiễu một khung)
    m = lambda F: lab(np.mean(np.stack(F), 0).astype(np.uint8)).reshape(-1, 3).mean(0)
    dm = float(np.linalg.norm(m(A[-24:]) - m(B[:24]))); dms = float(np.linalg.norm(m(S[216:240]) - m(S[240:264])))
    R = dict(dE_noi=round(j, 2), dE_nguon_cung_cho=round(js, 2), dE_nen_trung_vi=round(float(np.median(base)), 2), ti_so_noi_nen=round(j / max(1e-3, float(np.median(base))), 2),
             dE_mau_1s=round(dm, 2), dE_mau_1s_nguon=round(dms, 2),
             chi_tiet=dict(a_cuoi=round(la[2], 2), b_dau=round(lb[2], 2), ti_so=round(lb[2] / max(1e-3, la[2]), 3), nguon_ti_so=round(sb[2] / max(1e-3, sa[2]), 3)),
             bao_hoa=dict(a_cuoi=round(la[0], 3), b_dau=round(lb[0], 3)), colorful=dict(a_cuoi=round(la[1], 1), b_dau=round(lb[1], 1)))
    json.dump(R, open(a.json, 'w'), ensure_ascii=False, indent=1); print(json.dumps(R, ensure_ascii=False))


if __name__ == '__main__': main()
