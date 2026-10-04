"""Phụ đề tiếng Anh (.srt) từ timeline + align ElevenLabs (mốc ký tự), kể cả thoại Ida và phần B đoạn 19.
python srt_ep01.py <timeline.json> <ra.srt>   — mỗi khối ≤ 2 dòng × 42 ký tự, 1–7 s, cắt ở dấu câu/khoảng trắng."""
import json, re, sys, subprocess
TL = json.load(open(sys.argv[1])); MAXL, MAXC = 42, 84
def dur(p): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout)
def wrap(s):
    if len(s) <= MAXL: return s
    best = min((abs(i - len(s) / 2), i) for i, c in enumerate(s) if c == ' ')[1]
    return s[:best] + '\n' + s[best + 1:]
cues = []
for d in TL['doan']:
    for il in d.get('ida') or []:
        a = d['t0'] + il['at']; cues.append((a, a + max(1.2, dur(il['file'])), wrap('IDA: ' + il['txt']), d['n']))
    if not d.get('vo_file'): continue
    al = json.load(open(d['vo_file'].replace('.mp3', '.align.json')))
    ch, cs, ce = al['characters'], al['character_start_times_seconds'], al['character_end_times_seconds']
    a0 = d['t0'] + d['vo_offset']; tach = d.get('tach')
    def T(i, end=False):
        t = (ce if end else cs)[i]
        if tach and cs[i] >= tach['cat_tai_giay_trong_take']: t += tach['chen_lang_s']
        return a0 + t
    txt = ''.join(ch); i = 0; n = len(txt)
    while i < n:
        while i < n and txt[i].isspace(): i += 1
        if i >= n: break
        # lấy tới hết câu/mệnh đề sao cho ≤ MAXC
        j = i; last_ok = None
        while j < n and j - i < MAXC:
            if txt[j] in '.?!' and (j + 1 == n or txt[j + 1].isspace()): last_ok = j + 1; break
            if txt[j] in ',;:—' and j - i > 25: last_ok = j + 1
            j += 1
        if last_ok is None:
            if j >= n: last_ok = n
            else: last_ok = txt.rfind(' ', i, j) if txt.rfind(' ', i, j) > i else j
        seg = txt[i:last_ok].strip()
        k1 = last_ok - 1
        while txt[k1].isspace(): k1 -= 1
        cues.append((T(i), T(k1, True), wrap(re.sub(r"\s+", " ", seg)), d["n"]))
        i = last_ok
cues.sort()
out = []
for k, (a, b, s, nn) in enumerate(cues):
    b = max(b + 0.25, a + 1.0)
    if k + 1 < len(cues): b = min(b, cues[k + 1][0] - 0.04)
    f = lambda t: '%02d:%02d:%02d,%03d' % (t // 3600, t % 3600 // 60, int(t % 60), round((t % 1) * 1000) % 1000)
    out.append(f'{k + 1}\n{f(a)} --> {f(b)}\n{s}\n')
open(sys.argv[2], 'w').write('\n'.join(out)); print(len(cues), 'khối')
