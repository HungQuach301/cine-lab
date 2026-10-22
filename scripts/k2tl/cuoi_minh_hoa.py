#!/opt/cine/bin/python
"""BAN-CUOI-T3 (việc 1f + 4) · CHÈN 4 ĐOẠN MINH HOẠ Omni 1080p vào khung cảnh đinh 1080p — bản sửa của anim_minh_hoa.py (ANIMATIC-T3-V2):
  · nguồn = reports/animatic-t3-v2/omni/goc720/<M>.mp4 (720p cứu từ video gốc, SHA trong SHA256SUMS) → phóng 1920×1080 Lanczos + làm nét nhẹ (unsharp 5:5:0,45, chỉ độ sáng):
        ffmpeg -i goc720/<M>.mp4 -vf "scale=1920:1080:flags=lanczos+accurate_rnd+full_chroma_int,unsharp=5:5:0.45:5:5:0.0" -c:v libx264 -preset slow -crf 12 /var/tmp/cine-out/omni1080/<M>.mp4
  · KHÔNG nhãn "Illustration" (quyết định chủ dự án 22/10 11:09 — công bố AI chỉ ở YouTube).
  · khớp màu Lab (TB + độ lệch chuẩn, k = 0,7) về khung 3D quanh đoạn (tông LOOK-1, §16); LUT kênh áp cả phim sau (bước ghép).
  · đầu đoạn CẮT theo nhịp lời; cuối đoạn HOÀ 0,5 s về 3D nếu shot còn khung 3D sau đoạn.
  · ss = giây trong tệp goc720 ứng với giây đầu của đoạn đã dùng ở v2 (tệp goc720 = đoạn dùng nới 0,5 s mỗi đầu): M2 0,5 · M3 0 · M4 0,5 · M5 0.
  cuoi_minh_hoa.py <timeline.json> <log-shot.json> <log ra.json>"""
import hashlib, json, shutil, subprocess, sys
from pathlib import Path
import cv2, numpy as np
REPO = Path(__file__).resolve().parents[2]; G720 = REPO / 'reports/animatic-t3-v2/omni/goc720'; O1080 = Path('/var/tmp/cine-out/omni1080')
SS = dict(M2=0.5, M3=0.0, M4=0.5, M5=0.0); LUOT = dict(M2='M2-l3', M3='M3-l1', M4='M4-l1', M5='M5-l3')
TL = json.loads(Path(sys.argv[1]).read_text()); LOG = json.loads(Path(sys.argv[2]).read_text()); LOGP = Path(sys.argv[3])
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
def lab_stats(ims):
    L = np.concatenate([cv2.cvtColor(im, cv2.COLOR_BGR2LAB).reshape(-1, 3).astype(np.float32) for im in ims]); return L.mean(0), L.std(0) + 1e-6
def khop(im, ref, k=0.7):
    a = cv2.cvtColor(im, cv2.COLOR_BGR2LAB).astype(np.float32); m, s = a.reshape(-1, 3).mean(0), a.reshape(-1, 3).std(0) + 1e-6
    b = (a - m) * (ref[1] / s) + ref[0]; return cv2.cvtColor(np.clip(a * (1 - k) + b * k, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
out = []
for sh in LOG:
    for m in sh.get('minh_hoa') or []:
        M = m['ma']; src = G720 / f'{M}.mp4'; up = O1080 / f'{M}.mp4'; rec = dict(ma=M, shot=sh['ma'], t0=m['t0'], t1=m['t1'], minh_hoa=True, luot=LUOT.get(M))
        if not src.exists(): rec.update(chen=False, ly_do='không có tệp goc720 — giữ 3D'); out.append(rec); print('GIỮ 3D', M); continue
        if not up.exists():
            O1080.mkdir(parents=True, exist_ok=True)
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(src), '-vf', 'scale=1920:1080:flags=lanczos+accurate_rnd+full_chroma_int,unsharp=5:5:0.45:5:5:0.0', '-c:v', 'libx264', '-preset', 'slow', '-crf', '12', '-pix_fmt', 'yuv420p', '-an', str(up)], check=True)
        H = TL['heroes']['anim_' + sh['shot']]; d = Path(H['dir']); W, Hh = H['size']
        fr = sorted(p for p in d.iterdir() if p.suffix in ('.jpg', '.png') and p.stem.isdigit()); f0, f1 = int(round(m['t0'] * 24)), min(len(fr), int(round(m['t1'] * 24))); n = f1 - f0
        bk = d / 'goc-minh-hoa'; bk.mkdir(exist_ok=True)
        for p in fr[f0:f1]:
            if not (bk / p.name).exists(): shutil.copy2(p, bk / p.name)
        g = lambda i: cv2.imread(str(bk / fr[i].name)) if (bk / fr[i].name).exists() else cv2.imread(str(fr[i]))
        tmp = Path('/var/tmp/cine-out/k2c-t3-cuoi/minh-hoa') / M; shutil.rmtree(tmp, ignore_errors=True); tmp.mkdir(parents=True)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{SS[M]:.3f}', '-i', str(up), '-vf', f'scale={W}:{Hh}:flags=lanczos', '-q:v', '2', str(tmp / '%05d.jpg')], check=True)
        cf = sorted(tmp.glob('*.jpg')); have = len(cf) / 24.0; need = n / 24.0; sp = min(1.0, have / need)
        ref = lab_stats([g(i) for i in ([f0 - 1] if f0 > 0 else []) + ([f1] if f1 < len(fr) else [])] or [g(f0)]); nb = 12 if f1 < len(fr) else 0
        for i in range(n):
            im = khop(cv2.imread(str(cf[min(len(cf) - 1, int(i * sp))])), ref)
            if nb and i >= n - nb: a = (i - (n - nb) + 1) / (nb + 1); im = cv2.addWeighted(im, 1 - a, g(f1), a, 0)
            cv2.imwrite(str(fr[f0 + i]), im, [cv2.IMWRITE_JPEG_QUALITY, 95])
        rec.update(chen=True, khung=[f0, f1 - 1], nguon_720=str(src.relative_to(REPO)), sha_720=sha(src), tep_1080=str(up), sha_1080=sha(up), phong='Lanczos 1280×720 → 1920×1080 + unsharp 5:5:0,45 (độ sáng), x264 crf 12',
                   bo_dau_s=SS[M], clip_giay=round(have, 3), doan_giay=round(need, 3), toc_do=round(sp, 3), hoa_cuoi_khung=nb, khop_mau='Lab TB+độ lệch chuẩn k=0,7 về khung 3D quanh đoạn', nhan=None,
                   so_ai='reports/animatic-t3-v2/so-ai-gemini.jsonl', model='gemini-omni-1.1-flash', bac='minh hoạ N2 §14.1 c — không mang dữ kiện vị trí; dữ kiện do lời')
        out.append(rec); print('CHÈN', M, sh['ma'], f0, f1, f'clip {have:.2f} s / đoạn {need:.2f} s')
LOGP.write_text(json.dumps(out, ensure_ascii=False, indent=1)); print('MINH-HOA-XONG', sum(1 for r in out if r.get('chen')), '/', len(out))
