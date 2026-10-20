#!/opt/cine/bin/python -I
"""NC-V2V3 · ghép đầu ra Wan-VACE + dựng video để đo / xem (CPU).
  ghep3.py ra   <ctrl dir> <ra AI dir> <thư mục đích> [--b]     → <đích>/khung/%05d.png (chế độ B: ghép lại nguồn trên vùng giữ theo alpha/) + <đích>.mp4 (24 fps, crf 12)
  ghep3.py nguon <ctrl dir> <đích.mp4>                          → video nguồn cửa sổ (crf 12) + <đích>-dc.mp4 bản ĐỐI CHỨNG KHÔNG AI (cách NC-V2V: phóng 2 %, dịch 5/3 px, sáng +0,04, bão hoà ×1,15, mờ σ 0,8, nén crf 23)
Đầu ra AI có thể khác cỡ (bội 16) → đưa về đúng cỡ nguồn bằng lanczos trước khi ghép. Ghi kiểm K-LAI-4: sai khác TB |ra − nguồn| (8 bit) trên vùng giữ."""
import glob, json, os, subprocess, sys
import cv2, numpy as np


def mp4(pattern, out, crf=12, extra=()):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', '24', '-i', pattern, *extra, '-c:v', 'libx264', '-preset', 'slow', '-crf', str(crf), '-pix_fmt', 'yuv420p', out], check=True)


def ra(ctrl, aid, dst, b):
    os.makedirs(os.path.join(dst, 'khung'), exist_ok=True); fs = sorted(glob.glob(os.path.join(aid, '*.png'))); kl = []
    for i, f in enumerate(fs):
        o = cv2.imread(f, cv2.IMREAD_COLOR); s = cv2.imread(os.path.join(ctrl, 'src', f'{i:05d}.png'), cv2.IMREAD_COLOR)
        if o.shape != s.shape: o = cv2.resize(o, (s.shape[1], s.shape[0]), interpolation=cv2.INTER_LANCZOS4)
        if b:
            a = cv2.imread(os.path.join(ctrl, 'alpha', f'{i:05d}.png'), cv2.IMREAD_GRAYSCALE).astype(np.float32)[..., None] / 255
            o = np.clip(s.astype(np.float32) * (1 - a) + o.astype(np.float32) * a + 0.5, 0, 255).astype(np.uint8)
            keep = a[..., 0] == 0; kl.append(float(np.abs(o.astype(np.int16) - s.astype(np.int16))[keep].mean()) if keep.any() else 0.0)
        cv2.imwrite(os.path.join(dst, 'khung', f'{i:05d}.png'), o)
    mp4(os.path.join(dst, 'khung', '%05d.png'), dst.rstrip('/') + '.mp4')
    J = dict(n=len(fs), b=b, klai4_tb_vung_giu_png=max(kl) if kl else None); json.dump(J, open(dst.rstrip('/') + '.json', 'w')); print(J)


def nguon(ctrl, out):
    p = os.path.join(ctrl, 'src', '%05d.png'); mp4(p, out)
    s = cv2.imread(os.path.join(ctrl, 'src', '00000.png')); h, w = s.shape[:2]; W2, H2 = int(round(w * 1.02 / 2) * 2), int(round(h * 1.02 / 2) * 2)
    vf = f'scale={W2}:{H2}:flags=bicubic,crop={w}:{h}:{(W2 - w) // 2 + 5}:{(H2 - h) // 2 + 3},eq=brightness=0.04:saturation=1.15,gblur=sigma=0.8'
    mp4(p, out.replace('.mp4', '-dc.mp4'), crf=23, extra=('-vf', vf))


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'ra': ra(a[1], a[2], a[3], '--b' in a)
    elif a[0] == 'nguon': nguon(a[1], a[2])
