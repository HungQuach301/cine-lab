#!/opt/cine/bin/python
"""Q27 / Q31 (chủ dự án 06/10/2026, CHUAN-KENH §11.2) — chuẩn bị bộ xem mù cho subagent. Luật làm việc của P cho tới khi K khoá.

  blind_set.py q27 <thư mục ra> --new <video…> --ref <video…> [--n 10] [--seed 6]
      lấy n khung ngẫu nhiên (tránh 1 s đầu/cuối mỗi phần) của bản mới và n khung của bản tham chiếu (tập 1),
      trộn, đặt tên ẩn F01…F20 (1280×720 JPG); khoá giải mã ghi riêng ở <ra>/key.json (không đưa cho subagent).
  blind_set.py q31 <thư mục ra> --tl timeline.json --video <master.mp4>
      mỗi chuyển đoạn: dải 6 khung (−2,5 … +2,5 s quanh điểm cắt) + lời 6 s quanh điểm cắt; thêm một dải 1 khung/4 s cả tập.
      Subagent nhận ảnh + lời, không nhận đặc tả, mã, hay bản đồ liền mạch.
"""
import json, os, random, subprocess, sys


def grab(v, t, out, w=1280):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', v, '-frames:v', '1', '-vf', f'scale={w}:-2', '-q:v', '3', out], check=True)


def dur(v): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', v], capture_output=True, text=True).stdout)


def pick(vids, n, R):
    L = [(v, dur(v)) for v in vids]; tot = sum(d - 2 for _, d in L); out = []
    for _ in range(n):
        x = R.uniform(0, tot)
        for v, d in L:
            if x < d - 2: out.append((v, 1 + x)); break
            x -= d - 2
    return out


def q27(O, new, ref, n, seed):
    R = random.Random(seed); items = [('new', v, t) for v, t in pick(new, n, R)] + [('ref', v, t) for v, t in pick(ref, n, R)]
    R.shuffle(items); key = {}
    for i, (k, v, t) in enumerate(items, 1):
        name = f'F{i:02d}.jpg'; grab(v, t, os.path.join(O, name)); key[name] = dict(set=k, video=os.path.basename(v), t=round(t, 2))
    json.dump(key, open(os.path.join(O, 'key.json'), 'w'), indent=1)


def q31(O, tl, video):
    T = json.load(open(tl)); segs = T['segments']; words = []
    import ll
    REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    for s in segs:
        if s.get('vo_file'):
            al = json.load(open(os.path.join(REPO, s['vo_file'].replace('.mp3', '.align.json'))))
            words += [(s['t0'] + s['vo_offset'] + w[1], w[3]) for w in ll.words(al)]
    txt = []
    for k, (a, b) in enumerate(zip(segs, segs[1:]), 1):
        c = b['t0']; names = []
        for j, dt in enumerate((-2.5, -1.5, -0.5, 0.5, 1.5, 2.5)):
            nm = f'T{k:02d}_{j}.jpg'; grab(video, max(0, c + dt), os.path.join(O, nm), 640); names.append(nm)
        subprocess.run(['ffmpeg', '-v', 'error', '-y'] + sum([['-i', os.path.join(O, x)] for x in names], []) + ['-filter_complex', f'hstack={len(names)}', os.path.join(O, f'T{k:02d}.jpg')], check=True)
        for x in names: os.remove(os.path.join(O, x))
        said = ' '.join(w for t, w in words if c - 2.5 <= t <= c + 2.5)   # đúng cửa sổ khung (bài học Q31 tập 6 v2: ±6 s làm người xem tưởng lời rơi vào khung khác)
        txt.append(f'T{k:02d} (cut at {int(c // 60)}:{c % 60:04.1f}; frames at −2.5, −1.5, −0.5, +0.5, +1.5, +2.5 s): narration spoken within ±2.5 s of the cut: "{said}"')
    D = T['tong_s']; strip = []
    for i, t in enumerate(range(2, int(D), 4)):
        nm = f'S{i:03d}.jpg'; grab(video, t, os.path.join(O, nm), 320); strip.append(nm)
    rows = [strip[i:i + 8] for i in range(0, len(strip), 8)]   # 8 khung một dải
    for i, row in enumerate(rows):
        if len(row) < 8:   # độn bằng khung đen, không lặp khung cuối (lặp khung bị đọc thành 'cảnh đứng')
            blk = os.path.join(O, 'BLACK.jpg'); subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'color=black:s=320x180', '-frames:v', '1', blk], check=True)
            while len(row) < 8: row.append('BLACK.jpg')
        subprocess.run(['ffmpeg', '-v', 'error', '-y'] + sum([['-i', os.path.join(O, x)] for x in row], []) + ['-filter_complex', 'hstack=8', os.path.join(O, f'R{i:02d}.jpg')], check=True)
    for x in strip + (['BLACK.jpg'] if os.path.exists(os.path.join(O, 'BLACK.jpg')) else []): os.remove(os.path.join(O, x))
    open(os.path.join(O, 'transitions.txt'), 'w').write('\n'.join(txt) + f'\n\nOverview strips R00…R{len(rows) - 1:02d}: one frame every 4 s from 0:02, 8 frames per strip, left to right, strips in order.\n')


if __name__ == '__main__':
    a = sys.argv[1:]; mode, O = a[0], a[1]; os.makedirs(O, exist_ok=True)
    def lst(flag):
        if flag not in a: return []
        i = a.index(flag) + 1; out = []
        while i < len(a) and not a[i].startswith('--'): out.append(a[i]); i += 1
        return out
    if mode == 'q27': q27(O, lst('--new'), lst('--ref'), int((lst('--n') or [10])[0]), int((lst('--seed') or [6])[0]))
    else: sys.path.insert(0, os.path.dirname(__file__)); q31(O, lst('--tl')[0], lst('--video')[0])
