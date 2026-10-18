"""NC-AI · AI-2(a) thử ước tư thế MediaPipe Pose Landmarker full (Apache-2.0, chạy CPU) trên footage tư liệu công
NARA ARC 37058 "The story of Hoover Dam" (IA gov.archives.arc.37058, licenseurl CC0; bản 512kb.mp4).
B1: mẫu 1 khung / 3 s → % khung có ≥ 1 người, số người TB. B2: đoạn 8 s liên tục (24 fps) quanh khung mẫu có nhiều người nhất
→ rung: trung vị |gia tốc| khớp hông/gối/cổ chân (px/khung², quy về chiều cao người) và % khung mất dấu.
Dùng: <venv>/python -I ai2_pose.py <video> <pose_landmarker_full.task> <ra_dir>"""
import sys, json, time, subprocess, cv2, numpy as np, mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions
vid, task, out = sys.argv[1:4]
def lm(mode, n=6): return vision.PoseLandmarker.create_from_options(vision.PoseLandmarkerOptions(base_options=BaseOptions(model_asset_path=task), running_mode=mode, num_poses=n, min_pose_detection_confidence=0.5))
cap = cv2.VideoCapture(vid); fps = cap.get(cv2.CAP_PROP_FPS); N = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); W, H = int(cap.get(3)), int(cap.get(4))
L = lm(vision.RunningMode.IMAGE); samp = []; t0 = time.time()
for f in range(0, N, int(fps * 3)):
    cap.set(cv2.CAP_PROP_POS_FRAMES, f); ok, fr = cap.read()
    if not ok: break
    r = L.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)))
    samp.append((f, len(r.pose_landmarks)))
tB1 = time.time() - t0; cnt = np.array([s[1] for s in samp])
best = max(range(len(samp)), key=lambda i: sum(cnt[max(0, i - 1):i + 2]))  # cụm 3 mẫu liền nhiều người nhất
f0 = max(0, samp[best][0] - int(4 * fps)); L2 = lm(vision.RunningMode.VIDEO, 1)
cap.set(cv2.CAP_PROP_POS_FRAMES, f0); tr = []; frames = []
for k in range(int(8 * fps)):
    ok, fr = cap.read()
    if not ok: break
    r = L2.detect_for_video(mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)), int(k * 1000 / fps))
    if r.pose_landmarks:
        p = np.array([[q.x * W, q.y * H, q.visibility] for q in r.pose_landmarks[0]]); tr.append(p)
        if k % int(fps) == 0:
            for (x, y, v) in p:
                if v > 0.5: cv2.circle(fr, (int(x), int(y)), 3, (0, 0, 255), -1)
            frames.append(fr)
    else: tr.append(None)
miss = sum(t is None for t in tr) / max(1, len(tr))
J = [23, 24, 25, 26, 27, 28]; acc = []
for a, b, c in zip(tr, tr[1:], tr[2:]):
    if a is None or b is None or c is None: continue
    hgt = max(1.0, np.ptp(b[[0, 27, 28], 1]))
    acc += list(np.linalg.norm(a[J, :2] - 2 * b[J, :2] + c[J, :2], axis=1) / hgt)
if frames: cv2.imwrite(f'{out}/doan-8s-moi-giay.jpg', np.hstack([cv2.resize(f, (W // 2, H // 2)) for f in frames[:6]]), [cv2.IMWRITE_JPEG_QUALITY, 80])
S = {'video': {'fps': round(fps, 3), 'khung': N, 'px': [W, H], 'phut': round(N / fps / 60, 1)}, 'mau_3s': {'so_mau': len(samp), 'pt_khung_co_nguoi': round(float((cnt > 0).mean() * 100), 1),
     'nguoi_tb_khi_co': round(float(cnt[cnt > 0].mean()) if (cnt > 0).any() else 0, 2), 'giay_moi_khung': round(tB1 / len(samp), 3)},
     'doan_8s': {'bat_dau_s': round(f0 / fps, 1), 'pt_khung_mat_dau': round(miss * 100, 1), 'rung_trung_vi_gia_toc_theo_chieu_cao': round(float(np.median(acc)), 4) if acc else None,
     'rung_p95': round(float(np.percentile(acc, 95)), 4) if acc else None}}
json.dump(S, open(f'{out}/ket-qua.json', 'w'), ensure_ascii=False, indent=1); print(json.dumps(S, ensure_ascii=False))
