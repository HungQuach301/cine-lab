#!/opt/cine/bin/python
"""K2C-T2-01 · v3.3 → v3.4 (chủ dự án duyệt G2-BAO-CAO §8, 16/10): CẮT D7 + D13 + D10 và DỜI D5 (lời mời đăng ký) xuống cuối phim,
bằng CẮT/CHÈN ÂM Ở RANH CÂU trên bản thu đã có (cách A, 0 ký tự ElevenLabs) — không thu mới.
- Điểm nối đặt ở GIỮA khoảng nghỉ trước và sau câu bỏ (giữ độ dài nghỉ tự nhiên), hoà 25 ms (âm lặng → không tiếng tách).
- Căn chữ (align.json) bỏ ký tự của câu (kèm một khoảng trắng) và dời mốc phía sau đúng bằng độ dài âm đã cắt/chèn.
- Chữ ký cache vo/<đoạn>.txt tính lại cho toàn văn mới (cùng công thức ll.tts / prep.tts_k2) → prep dùng bản đã sửa, không gọi API.
- script.md + loi-khoa.txt sửa cùng chữ; LOI-KHOA.sha256 tính lại. Bản gốc v3.3 giữ ở vo/v3.3/ và script-v3.3-KHOA.md.
  sua_loi.py apply      (chạy một lần; dừng nếu đã áp)
  sua_loi.py joins      → in giây (theo đoạn) của mọi điểm nối để nghe thử + ASR"""
import hashlib, json, os, re, shutil, subprocess, sys, tempfile
import numpy as np, yaml
H = os.path.dirname(os.path.abspath(__file__)); VO = os.path.join(H, 'vo'); KEY = 'k2c-t2-01'; SR = 44100; XF = 0.025
REMOVE = [('03', 'So the record says something narrower than "wages": wages are one factor it lists; the lack of exports, and the scale that comes with them, is another.'),   # D7
          ('04', "The sources we used don't say how much of that went to Hyundai's yard."),                                                                            # D10
          ('06', 'Supporters, like the American Maritime Partnership, make their case on jobs and security.'),                                                         # D13 (1/2)
          ('06', 'Critics, like Senator Lee and Representative McClintock, make theirs on higher prices for Americans.')]                                              # D13 (2/2)
MOVE = ('02', '06', "If you're finding this useful, subscribing is how you'll catch the next one.", 'No source we found measures how much each factor counts.')   # D5: sau câu chốt, trước "Back in Richmond"


def pcm(f):
    return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True, check=True).stdout, np.float32).copy()


def join(a, b):   # hoà XF giây ở điểm nối
    n = int(XF * SR); r = np.linspace(0, 1, n, dtype=np.float32)
    return np.concatenate([a[:-n], a[-n:] * (1 - r) + b[:n] * r, b[n:]])


def load(seg):
    t = open(f'{VO}/{KEY}-{seg}.txt').read().split('\n'); al = json.load(open(f'{VO}/{KEY}-{seg}.align.json'))
    assert ''.join(al['characters']) == t[1], f'căn chữ ≠ chữ ở đoạn {seg}'
    return dict(text=t[1], al=al, pcm=pcm(f'{VO}/{KEY}-{seg}.mp3'))


def span(D, s):   # (i0, i1) ký tự của câu; (t0, t1) giây của câu; e_prev, s_next
    i0 = D['text'].index(s); i1 = i0 + len(s); A = D['al']
    t0, t1 = A['character_start_times_seconds'][i0], A['character_end_times_seconds'][i1 - 1]
    e_prev = A['character_end_times_seconds'][i0 - 2] if i0 >= 2 else 0.0
    s_next = A['character_start_times_seconds'][i1 + 1] if i1 + 1 < len(D['text']) else None
    return i0, i1, t0, t1, e_prev, s_next


def remove(D, s):
    i0, i1, t0, t1, ep, sn = span(D, s); A = D['al']
    ca = (ep + t0) / 2; cb = (t1 + sn) / 2 if sn is not None else t1   # câu cuối đoạn: giữ đuôi lặng sau câu
    if sn is None: i0 -= 1   # bỏ khoảng trắng TRƯỚC câu cuối
    else: i1 += 1            # bỏ khoảng trắng SAU câu
    x = D['pcm']
    if sn is None:   # câu cuối đoạn: cắt tại giữa khoảng nghỉ trước câu, tắt dần 25 ms, giữ đuôi lặng ≥ 0,3 s như bản gốc
        n = int(XF * SR); keep = x[:int(ca * SR)].copy(); keep[-n:] *= np.linspace(1, 0, n, dtype=np.float32)
        tail = max(0.3, len(x) / SR - t1); D['pcm'] = np.concatenate([keep, np.zeros(int(tail * SR), np.float32)]); d = len(x) / SR - len(D['pcm']) / SR
    else: d = cb - ca; D['pcm'] = join(x[:int(ca * SR)], x[int(cb * SR):])
    for k in A: A[k] = A[k][:i0] + ([v - d for v in A[k][i1:]] if k != 'characters' else A[k][i1:])
    D['text'] = D['text'][:i0] + D['text'][i1:]
    return dict(cat=round(d, 3), noi_s=round(ca, 3))


def insert(D, src, s, after):
    i0, i1, t0, t1, ep, sn = span(src, s); A0 = src['al']
    clip = src['pcm'][int(((ep + t0) / 2) * SR):int((t1 + 0.12) * SR)]; c0 = (ep + t0) / 2
    j0, j1, u0, u1, _, un = span(D, after); m = (u1 + un) / 2; A = D['al']; dur = len(clip) / SR
    x = D['pcm']; D['pcm'] = join(join(x[:int(m * SR)], clip), x[int(m * SR):])
    ch = list(s) + [' ']; st = [v - c0 + m for v in A0['character_start_times_seconds'][i0:i1]] + [m + dur]; en = [v - c0 + m for v in A0['character_end_times_seconds'][i0:i1]] + [m + dur]
    p = j1 + 1   # sau khoảng trắng theo câu chốt
    A['characters'] = A['characters'][:p] + ch + A['characters'][p:]
    A['character_start_times_seconds'] = A['character_start_times_seconds'][:p] + st + [v + dur for v in A['character_start_times_seconds'][p:]]
    A['character_end_times_seconds'] = A['character_end_times_seconds'][:p] + en + [v + dur for v in A['character_end_times_seconds'][p:]]
    D['text'] = D['text'][:p] + s + ' ' + D['text'][p:]
    return dict(chen=round(dur, 3), noi_s=[round(m, 3), round(m + dur, 3)])


def sig(text):
    v = yaml.safe_load(open(f'{H}/episode.yaml'))['voice']
    return hashlib.sha1(json.dumps([text, v], sort_keys=True).encode()).hexdigest()[:12]


def apply():
    if os.path.isdir(f'{VO}/v3.3'): raise SystemExit('đã áp (có vo/v3.3) — dừng')
    for seg in ('02', '03', '04', '06'):   # chữ ký cũ phải khớp công thức (kiểm trước khi sửa)
        assert open(f'{VO}/{KEY}-{seg}.txt').read().split('\n')[0] == sig(open(f'{VO}/{KEY}-{seg}.txt').read().split('\n')[1]), f'công thức chữ ký lệch ở {seg}'
    os.makedirs(f'{VO}/v3.3'); log = {}
    D = {s: load(s) for s in ('02', '03', '04', '06')}
    for seg in D:
        for x in ('mp3', 'align.json', 'txt'): shutil.copy(f'{VO}/{KEY}-{seg}.{x}', f'{VO}/v3.3/')
    for seg, s in REMOVE: log.setdefault(seg, []).append(dict(bo=s[:60], **remove(D[seg], s)))
    src = load('02'); log.setdefault('06', []).append(dict(cau=MOVE[2][:60], **insert(D['06'], src, MOVE[2], MOVE[3])))
    log.setdefault('02', []).append(dict(bo=MOVE[2][:60], **remove(D['02'], MOVE[2])))
    for seg, d in D.items():
        assert ''.join(d['al']['characters']) == d['text']
        with tempfile.NamedTemporaryFile(suffix='.wav') as w:
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', w.name], input=d['pcm'].tobytes(), check=True)
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', w.name, '-c:a', 'libmp3lame', '-b:a', '128k', '-ar', str(SR), f'{VO}/{KEY}-{seg}.mp3'], check=True)
        json.dump(d['al'], open(f'{VO}/{KEY}-{seg}.align.json', 'w')); open(f'{VO}/{KEY}-{seg}.txt', 'w').write(sig(d['text']) + '\n' + d['text'] + '\n')
    # lời khoá: script.md + loi-khoa.txt
    shutil.copy(f'{H}/script.md', f'{H}/script-v3.3-KHOA.md') if not os.path.exists(f'{H}/script-v3.3-KHOA.md') else None
    for fn in ('script.md', 'loi-khoa.txt'):
        t = open(f'{H}/{fn}').read()
        for _, s in REMOVE: assert t.count(s) == 1, (fn, s); t = t.replace(' ' + s, '', 1) if ' ' + s in t else t.replace(s + ' ', '', 1)
        t = t.replace(MOVE[2] + '\n\n', '', 1); assert MOVE[2] not in t
        t = t.replace(' {C47} {C48} {C36}', ' {C36}')   # D13: chương 06 không còn nêu C47/C48 (vẫn nêu ở chương 02)
        i = t.index(MOVE[3]) + len(MOVE[3]); j = t.index('\n', i); t = t[:j] + '\n\n' + MOVE[2] + t[j:]
        if fn == 'script.md':
            t = t.replace('lời KHOÁ v3.3 (G1 duyệt 15/10, J1–J6)', 'lời KHOÁ v3.4 (G1 duyệt 15/10, J1–J6; G2 §8 duyệt 16/10)', 1)
            t = t.replace('\n> v3.2 → v3.3 (KHOÁ)', '\n> v3.3 → v3.4 (KHOÁ, chủ dự án 16/10, G2-BAO-CAO §8): CẮT D7 (câu nhắc lại vòng lặp, chương 03), D13 (ủng hộ/phản đối lặp ở phần kết; vẫn nêu ở chương 02), D10 (câu "nguồn không nói" thứ nhất, chương 04); DỜI D5 (lời mời đăng ký) từ cuối chương 02 xuống cuối phim, sau câu chốt, trước "Back in Richmond". Âm cắt/chèn ở ranh câu từ bản thu đã có (`sua_loi.py`, 0 ký tự ElevenLabs). Bản v3.3: `script-v3.3-KHOA.md`, `vo/v3.3/`.\n> v3.2 → v3.3 (KHOÁ)', 1)
        open(f'{H}/{fn}', 'w').write(t)
    open(f'{H}/LOI-KHOA.sha256', 'w').write(''.join(f"{hashlib.sha256(open(f'{H}/{f}', 'rb').read()).hexdigest()}  {f}\n" for f in ('script.md', 'loi-khoa.txt')))
    json.dump(log, open(f'{VO}/sua-v3.4.json', 'w'), indent=1, ensure_ascii=False); print(json.dumps(log, indent=1, ensure_ascii=False))


if __name__ == '__main__':
    if sys.argv[1] == 'apply': apply()
    elif sys.argv[1] == 'joins': print(json.dumps(json.load(open(f'{VO}/sua-v3.4.json')), indent=1, ensure_ascii=False))
