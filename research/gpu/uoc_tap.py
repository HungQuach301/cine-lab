"""GPU-RD · ước giờ máy + chi phí một tập 10 phút (14 400 khung) cho các phương án. Số đo ghi nguồn; số GPU là (ước).
Dùng: python3 research/gpu/uoc_tap.py [--out research/gpu/do/uoc-tap.json]"""
import argparse, json
N = 14400
MIX = {4: 0.05, 1: 0.15, 2: 0.80}                      # kịch bản 2/3 V5b-1 §5.3: SPP4 5 %, SPP1 15 %, SPP2 80 %
SS = {1: 3.34, 2: 5.83, 4: 11.57}                       # SwiftShader máy C, V5B1B §7.2 (đo)
LP = {1: 0.764, 2: 1.110, 4: 1.829}                     # llvmpipe máy này (≈ C), trọn gib20 480 khung 16/10 (đo, do/llvmpipe-gib20-480khung.json)
RELIEF_SS = 1.98                                        # relief/2.5D SwiftShader (NT 15/10, RUNBOOK §7, đo)
SLOW = 1.41                                             # máy chậm B / máy C (V5B1B §7.1, đo trên SwiftShader; áp cho llvmpipe là (ước))
FLOOR = 0.153                                           # phần KHÔNG phải dựng GL mỗi khung (JS + ghép 2D + đọc lại + JPEG + IPC), đo profile-swiftshader.json
GL_FRAC = 0.974                                         # phần dựng GL trong khung SPP2 SwiftShader (5 746 / 5 899 ms, đo)
GPU_K = {"thấp": 10, "giữa": 30, "cao": 100}           # tăng tốc phần dựng GL của GPU thật so với SwiftShader 4 vCPU (ước; llvmpipe CPU đã 5,3×)
PRICE = {"AWS g4dn.xlarge T4 spot": 0.287, "GCP g2-standard-4 L4 spot": 0.4028, "RunPod L4 community": 0.44, "AWS g4dn.xlarge T4 theo yêu cầu": 0.526,
         "RunPod L4 secure": 0.59, "GCP g2-standard-4 L4 theo yêu cầu": 0.7068, "DigitalOcean RTX 4000 Ada": 0.76}
SETUP_H = 0.5                                           # dựng môi trường + chép gói cảnh/khung mỗi tập (ước; lần đầu ≈ 1 h)


def mix(t): return sum(MIX[k] * t[k] for k in MIX)


def gpu(s_cpu, k): return FLOOR + s_cpu * GL_FRAC / k


rows = []
ss3d = mix(SS); lp3d = mix(LP)
for name, share3d in (("100 % 3D (kịch bản 2)", 1.0), ("70 % 3D + 30 % relief (kịch bản 3)", 0.7)):
    r = dict(kich_ban=name)
    r["CPU SwiftShader (máy C / máy chậm)"] = [round(N * (share3d * ss3d + (1 - share3d) * RELIEF_SS) / 3600 * f, 1) for f in (1, SLOW)]
    r["CPU llvmpipe, relief giữ SwiftShader (máy C / chậm ước)"] = [round(N * (share3d * lp3d + (1 - share3d) * RELIEF_SS) / 3600 * f, 1) for f in (1, SLOW)]
    r["CPU llvmpipe 2 tiến trình (÷1,2 đo)"] = round(r["CPU llvmpipe, relief giữ SwiftShader (máy C / chậm ước)"][0] / 1.2, 1)
    for lab, k in GPU_K.items():
        r[f"GPU {lab} ×{k} (ước)"] = round(N * (share3d * gpu(ss3d, k) + (1 - share3d) * gpu(RELIEF_SS, k)) / 3600, 2)
    rows.append(r)
cost = {}
for lab in GPU_K:
    h = rows[1][f"GPU {lab} ×{GPU_K[lab]} (ước)"] + SETUP_H
    cost[lab] = dict(gio_thue=round(h, 2), usd={p: round(h * v, 2) for p, v in PRICE.items()})
out = dict(s_khung_3d=dict(swiftshader=round(ss3d, 3), llvmpipe=round(lp3d, 3), gpu={l: round(gpu(ss3d, k), 3) for l, k in GPU_K.items()}), bang=rows, chi_phi_gpu_kich_ban3=cost)
ap = argparse.ArgumentParser(); ap.add_argument("--out"); a = ap.parse_args()
print(json.dumps(out, ensure_ascii=False, indent=1))
if a.out: open(a.out, "w").write(json.dumps(out, ensure_ascii=False, indent=1))
