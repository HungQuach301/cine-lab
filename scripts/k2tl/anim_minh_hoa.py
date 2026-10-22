#!/opt/cine/bin/python
"""ANIMATIC-T3-V2 · CHÈN ĐOẠN MINH HOẠ N2 (Omni image-to-video, đã qua bộ kiểm) vào khung cảnh đinh — sau bước dựng cảnh đinh, TRƯỚC render đoạn (như anim_lan.py).
Mỗi mục minh_hoa của log-shot.json (shot, t0, t1): khung f ∈ [t0·24, t1·24) của cảnh đinh thay bằng khung clip đã CHỌN reports/animatic-t3-v2/omni/chon/<M>.mp4
(nếu chưa có / bị loại → GIỮ bản 3D, ghi lý do). Clip lấy từ giây 0 (khung đầu = render của chính shot) hoặc từ giây ss ghi trong omni/chon/<M>.json; dài hơn thì cắt, ngắn hơn thì kéo chậm đều.
Khớp màu (Lab, TB + độ lệch chuẩn, mức k = 0,7) về khung 3D của chính shot quanh đoạn (tông LOOK-1). Chuyển: đầu đoạn CẮT (theo nhịp lời / cắt góc), cuối đoạn HOÀ 0,5 s
về khung 3D nếu shot còn khung 3D sau đoạn, không thì cắt sang shot sau. Nhãn "Illustration" góc dưới PHẢI suốt đoạn (bộ đếm góc dưới trái do render đoạn vẽ, chạy tiếp).
Giữ bản gốc ở <dir>/goc-minh-hoa/ (chạy lại được). Ghi log ra JSON: minh_hoa: true, nguồn, bậc, SHA clip.
  anim_minh_hoa.py <timeline.json của build> <log ra.json> [--chi M1,M3]"""
import json, shutil, subprocess, sys
from pathlib import Path
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
REPO = Path(__file__).resolve().parents[2]; CHON = REPO / 'reports/animatic-t3-v2/omni/chon'
TL = json.loads(Path(sys.argv[1]).read_text()); LOGP = Path(sys.argv[2]); CHI = set(sys.argv[sys.argv.index('--chi') + 1].split(',')) if '--chi' in sys.argv else None
LOG = json.loads((REPO / 'channel-k2/k2c-t3-01/animatic/log-shot.json').read_text())
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'   # RIGHTS C4-F1


def lab_stats(ims):
    L = np.concatenate([cv2.cvtColor(im, cv2.COLOR_BGR2LAB).reshape(-1, 3).astype(np.float32) for im in ims]); return L.mean(0), L.std(0) + 1e-6


def khop(im, ref, k=0.7):
    a = cv2.cvtColor(im, cv2.COLOR_BGR2LAB).astype(np.float32); m, s = a.reshape(-1, 3).mean(0), a.reshape(-1, 3).std(0) + 1e-6
    b = (a - m) * (ref[1] / s) + ref[0]; return cv2.cvtColor(np.clip(a * (1 - k) + b * k, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)


def nhan(im):
    p = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB)); g = ImageDraw.Draw(p, 'RGBA'); W, H = p.size; fs = max(12, int(H * 0.030)); f = ImageFont.truetype(FONT, fs)
    t = 'Illustration'; w = g.textlength(t, font=f); x, y = W - w - int(W * 0.035), H - fs - int(H * 0.055)
    g.rounded_rectangle([x - fs * 0.45, y - fs * 0.25, x + w + fs * 0.45, y + fs * 1.2], radius=fs * 0.3, fill=(0, 0, 0, 120)); g.text((x, y), t, font=f, fill=(255, 255, 255, 235))
    return cv2.cvtColor(np.array(p), cv2.COLOR_RGB2BGR)


out = []
for sh in LOG:
    for m in sh.get('minh_hoa') or []:
        if CHI and m['ma'] not in CHI: continue
        clip = CHON / f"{m['ma']}.mp4"; rec = dict(ma=m['ma'], shot=sh['ma'], t0=m['t0'], t1=m['t1'], minh_hoa=True)
        if not clip.exists(): rec.update(chen=False, ly_do='chưa có clip đạt kiểm (giữ bản 3D đã sửa)'); out.append(rec); print('GIỮ 3D', m['ma']); continue
        H = TL['heroes']['anim_' + sh['shot']]; d = Path(H['dir']); W, Hh = H['size']
        fr = sorted(p for p in d.iterdir() if p.suffix in ('.jpg', '.png') and p.stem.isdigit()); f0, f1 = int(round(m['t0'] * 24)), min(len(fr), int(round(m['t1'] * 24))); n = f1 - f0
        bk = d / 'goc-minh-hoa'; bk.mkdir(exist_ok=True)
        for p in fr[f0:f1]:
            if not (bk / p.name).exists(): shutil.copy2(p, bk / p.name)
        src = lambda i: cv2.imread(str(bk / fr[i].name)) if (bk / fr[i].name).exists() else cv2.imread(str(fr[i]))
        tmp = Path('/var/tmp/cine-out/k2c-t3-anim/minh-hoa') / m['ma']; shutil.rmtree(tmp, ignore_errors=True); tmp.mkdir(parents=True)
        cfg = json.loads(clip.with_suffix('.json').read_text()) if clip.with_suffix('.json').exists() else {}; ss = float(cfg.get('ss', 0.0))   # ss: bỏ phần đầu clip (vd. Omni tự cắt cảnh sau khung đầu)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{ss:.3f}', '-i', str(clip), '-vf', f'scale={W}:{Hh}:flags=lanczos', '-q:v', '2', str(tmp / '%05d.jpg')], check=True)
        cf = sorted(tmp.glob('*.jpg')); cfps = float(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=r_frame_rate', '-of', 'csv=p=0', str(clip)], capture_output=True, text=True).stdout.strip().split('/')[0]) / \
            float((subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=r_frame_rate', '-of', 'csv=p=0', str(clip)], capture_output=True, text=True).stdout.strip().split('/') + ['1'])[1])
        need = n / 24.0; have = len(cf) / cfps; sp = min(1.0, have / need)   # clip ngắn hơn đoạn → kéo chậm đều (ghi lại)
        ref_ims = [src(i) for i in ([f0 - 1] if f0 > 0 else []) + ([f1] if f1 < len(fr) else [])] or [src(f0)]
        ref = lab_stats(ref_ims); after = f1 < len(fr); nb = 12 if after else 0
        for i in range(n):
            ci = min(len(cf) - 1, int((i / 24.0) * sp * cfps)); im = khop(cv2.imread(str(cf[ci])), ref)
            if nb and i >= n - nb:   # hoà 0,5 s về khung 3D sau đoạn
                a = (i - (n - nb) + 1) / (nb + 1); im = cv2.addWeighted(im, 1 - a, src(f1), a, 0)
            cv2.imwrite(str(fr[f0 + i]), nhan(im), [cv2.IMWRITE_JPEG_QUALITY, 95]) if fr[f0 + i].suffix == '.jpg' else cv2.imwrite(str(fr[f0 + i]), nhan(im))
        rec.update(chen=True, khung=[f0, f1 - 1], clip=str(clip.relative_to(REPO)), clip_sha=__import__('hashlib').sha256(clip.read_bytes()).hexdigest(), clip_giay=round(have, 3), doan_giay=round(need, 3),
                   toc_do=round(sp, 3), bo_dau_clip_s=ss, hoa_cuoi_khung=nb, khop_mau='Lab TB+độ lệch chuẩn k=0,7 về khung 3D quanh đoạn', nhan='Illustration (góc dưới phải, suốt đoạn)',
                   nguon='Gemini Omni gemini-omni-1.1-flash image-to-video (sổ reports/animatic-t3-v2/so-ai-gemini.jsonl)', bac='minh hoạ N2 §14.1 c — không mang dữ kiện vị trí; dữ kiện do lời')
        out.append(rec); print('CHÈN', m['ma'], sh['ma'], f0, f1, f'clip {have:.2f} s / đoạn {need:.2f} s')
LOGP.write_text(json.dumps(out, ensure_ascii=False, indent=1)); print('MINH-HOA-XONG', sum(1 for r in out if r.get('chen')), '/', len(out))
