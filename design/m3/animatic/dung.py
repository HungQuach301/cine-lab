"""Cine Lab · M2.1 — dựng animatic nhịp 960×540, 24 fps: khung tĩnh b3v3 / thẻ dữ liệu / placeholder theo dòng thời gian của nhip.py,
lời dẫn flite (atempo về 141,2 từ/phút × mức), thoại Ida L1/L2 (C4-D1), nhạc tạm CC0 (M2-MUS-1) hạ thấp + né lời, phụ đề tiếng Anh cháy vào hình.
/opt/cine/bin/python design/m3/animatic/dung.py <nhip.json> <thư mục nhịp (wav câu)> <thư mục still> <thư mục thẻ> <thư mục làm việc> <ra.mp4> [mức=1.00] [cat07=1]
"""
import glob, json, os, re, subprocess, sys
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nhip
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
SR, FPS, W, H = 48000, 24, 960, 540
def run(*a): subprocess.run(list(a), check=True)

# shot → khung Last Round (b3v3) + nhãn tạm cho dàn dựng chưa làm
STILL = {'01-01': 's01', '01-02': 's02', '01-03': 's03', '01-04': 's05', '01-05': 's04', '01-06': 's07', '01-07': 's08', '01-08': 's01', '02-07': 'lp20',
 '03-01': 's03', '03-02': 's24', '03-04': 's40', '03-05': 's05', '03-06': 's07', '03-07': 's01', '05-01': 's09', '05-02': 's09w', '05-05': 's10e', '05-06': 's10',
 '05-07': 's19', '05-08': 's22', '05-09': 's12', '05-10': 's09w', '05-11': 's15', '06-05': 's27', '10-01': 's35', '10-02': 's37w', '10-03': 's38', '10-04': 's40',
 '10-05': 's40w', '10-06': 's41', '10-07': 's42b', '10-08': 's43', '10-09': 's46', '10-10': 's48', '14-02': 's43', '14-03': 's44'}
TAG = {'01-07': 'TEMP: add Cas silhouette far (s24c)', '01-08': 'TEMP: dusk grade, slow push', '02-07': 'TEMP: lp20 frame', '03-01': 'TEMP: new camera back-right',
 '03-02': 'TEMP: new side camera', '03-04': 'TEMP: dawn grade', '03-05': 'TEMP: new pose, wiping the glass', '03-06': 'TEMP: add rain / fog layer',
 '03-07': 'TEMP: cloned anonymous silhouettes', '06-05': 'TEMP: electric light from s27, no post in frame', '10-03': 'TEMP: new camera from behind',
 '14-02': 'TEMP: add modern city layer', '05-10': 'TEMP: alternate crop'}

def frame_img(sid, still, cards, work):
    if os.path.exists(f'{cards}/{sid}.png'): return Image.open(f'{cards}/{sid}.png').convert('RGB').resize((W, H), Image.LANCZOS), False
    src = STILL[sid]; p = sorted(glob.glob(f'{still}/{src}_f*.png'))[0]; im = Image.open(p).convert('RGB')
    if sid == '05-10': im = im.crop((160, 90, 800, 450)).resize((W, H), Image.LANCZOS)
    if sid in TAG:
        d = ImageDraw.Draw(im); f = ImageFont.truetype(FONT, 18); b = d.textbbox((12, 10), TAG[sid], font=f); d.rectangle([b[0] - 6, b[1] - 4, b[2] + 6, b[3] + 4], fill=(0, 0, 0)); d.text((12, 10), TAG[sid], font=f, fill=(255, 210, 120))
    return im, True

def main(nj, nd, still, cards, work, out, lv=1.0, cut=True):
    os.makedirs(work, exist_ok=True); D = json.load(open(nj)); segs, shots = D['segs'], D['shots']
    tl = nhip.timeline(segs, shots, lv, cut, detail=True); T = tl['total']; segof = {s['id']: s['seg'] for s in shots}
    # ---------- hình: mỗi shot một clip (khớp khung nguyên), ảnh 3D có pan/zoom nhẹ, thẻ đứng yên; nhúng đen 8 khung ở ranh giới đoạn
    lst, fcur = [], 0
    for i, s in enumerate(tl['shots']):
        f1 = round(s['t1'] * FPS); n = f1 - fcur; fcur = f1
        im, kb = frame_img(s['id'], still, cards, work); ip = f'{work}/{s["id"]}.png'; im.save(ip)
        first = i == 0 or segof[tl['shots'][i - 1]['id']] != segof[s['id']]; last = i == len(tl['shots']) - 1 or segof[tl['shots'][i + 1]['id']] != segof[s['id']]
        vf = (f"scale=1056:594,crop={W}:{H}:x='48*n/{max(n, 1)}':y='27*n/{max(n, 1)}'" if kb else 'null')
        if first: vf += ',fade=in:0:8'
        if last: vf += f',fade=out:{max(0, n - 8)}:8'
        cp = f'{work}/{s["id"]}.mp4'
        run('ffmpeg', '-nostdin', '-v', 'error', '-y', '-loop', '1', '-framerate', str(FPS), '-i', ip, '-frames:v', str(n), '-vf', vf + ',format=yuv420p', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-r', str(FPS), cp)
        lst.append(f"file '{cp}'"); s['frames'] = n
    open(f'{work}/list.txt', 'w').write('\n'.join(lst)); run('ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{work}/list.txt', '-c', 'copy', f'{work}/video.mp4')
    # ---------- tiếng: lời dẫn (atempo theo đoạn × mức), Ida, nhạc
    N = int((fcur / FPS + 0.5) * SR); vo = np.zeros(N); sub = []
    tempo = {sg['id']: sg['tempo'] for sg in segs}; sent_seg = {x['wav']: sg['id'] for sg in segs for x in sg['sent']}
    for v in tl['vo']:
        r = tempo[sent_seg[v['wav']]] * lv; tmp = f'{work}/t.wav'
        run('ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', f'{nd}/{v["wav"]}', '-af', f'atempo={r:.5f},aresample={SR}', '-ac', '1', tmp)
        y, _ = sf.read(tmp); a = int(v['t'] * SR); vo[a:a + len(y)] += 0.9 * y[: max(0, N - a)]; sub.append((v['t'], v['t'] + len(y) / SR, v['text']))
    ida = np.zeros(N); st = {s['id']: s for s in tl['shots']}
    def put(code, t, gain=1.0, far=False):
        tmp = f'{work}/ida.wav'; af = f'aresample={SR}' + (',lowpass=f=2500,highpass=f=300,aecho=0.8:0.6:120:0.3' if far else '')
        run('ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', f'{ROOT}/reports/m1/cong2/tableread-d2/lines/{code}.mp3', '-af', af, '-ac', '1', tmp)
        y, _ = sf.read(tmp); a = int(t * SR); ida[a:a + len(y)] += gain * y[: max(0, N - a)]; return len(y) / SR
    sub_ida = []
    for sid, code, off, g, far, txt in [('01-04', 'L1', 1.0, 1.0, False, 'IDA: Evening, old street.'), ('05-08', 'L2', 0.8, 1.0, False, 'IDA: Not yet… not yet.'), ('14-03', 'L1', 0.3, 0.35, True, 'IDA (distant): Evening, old street.')]:
        t = st[sid]['t0'] + off; d = put(code, t, g, far); sub_ida.append((t, t + d, txt))
    run('ffmpeg', '-nostdin', '-v', 'error', '-y', '-stream_loop', '-1', '-i', f'{os.path.dirname(os.path.abspath(__file__))}/audio/freesound-496757-erokia-ambient-wave-48.mp3',
        '-t', f'{N / SR:.3f}', '-af', f'aresample={SR},afade=t=in:d=3,afade=t=out:st={N / SR - 4:.3f}:d=4', '-ac', '1', f'{work}/mus.wav')
    mus, _ = sf.read(f'{work}/mus.wav'); mus = np.pad(mus, (0, max(0, N - len(mus))))[:N]
    env = np.abs(vo) + np.abs(ida); k = int(0.25 * SR); act = np.convolve((env > 0.01).astype(float), np.ones(k), 'same') > 0
    duck = np.where(act, 10 ** (-10 / 20), 1.0); duck = np.convolve(duck, np.ones(int(0.3 * SR)) / int(0.3 * SR), 'same')
    mix = vo + ida + mus * 10 ** (-20 / 20) * duck
    mix = mix / max(1e-9, np.abs(mix).max()) * 10 ** (-1 / 20); sf.write(f'{work}/mix.wav', mix, SR)
    # ---------- phụ đề (SRT), cháy vào hình: chữ trắng trên hộp đen 75 %
    def ts(x): return f'{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(round((x % 1) * 1000)) % 1000:03d}'
    allsub = sorted(sub + sub_ida); L = []
    for i, (a, b, t) in enumerate(allsub):
        words, line, lines = t.split(' '), '', []
        for w in words:
            if len(line) + len(w) > 52: lines.append(line); line = w
            else: line = (line + ' ' + w).strip()
        lines.append(line); L.append(f'{i + 1}\n{ts(a)} --> {ts(b + 0.15)}\n' + '\n'.join(lines) + '\n')
    open(f'{work}/sub.srt', 'w').write('\n'.join(L))
    style = "FontName=DejaVu Sans,FontSize=15,PrimaryColour=&H00FFFFFF,OutlineColour=&H40000000,BackColour=&H40000000,BorderStyle=3,Outline=6,Shadow=0,MarginV=26"   # MarginV 26 (≈ 49 px ở 540): hộp phụ đề nằm trên dòng nguồn của thẻ dữ liệu
    run('ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', f'{work}/video.mp4', '-i', f'{work}/mix.wav', '-vf', f"subtitles={work}/sub.srt:force_style='{style}'",
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '22', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', out)
    json.dump({'level': lv, 'cut07': cut, 'total_s': T, 'frames': fcur, 'segs': tl['segs'], 'shots': tl['shots'], 'subs': len(allsub)}, open(f'{work}/thuc-te.json', 'w'), ensure_ascii=False, indent=1)
    print('xong', out, f'{fcur / FPS:.2f} s', len(tl['shots']), 'shot')

if __name__ == '__main__':
    a = sys.argv[1:]; main(*a[:6], lv=float(a[6]) if len(a) > 6 else 1.0, cut=(a[7] != '0') if len(a) > 7 else True)
