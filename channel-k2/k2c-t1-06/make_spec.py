#!/opt/cine/bin/python
"""K2C-T1-06 · ghép đặc tả tập: ep-src.yaml (hình, nguồn, số) + lời khoá ứng viên v8.1 NGUYÊN VĂN từ script.md → episode.yaml.
Lời mỗi đoạn = phần văn bản sau nhãn [NN PART] trong script.md, bỏ mã claim {Cnn}, gộp đoạn văn bằng một khoảng trắng (đúng chuỗi gửi ElevenLabs, khoá cache).
Shorts: lời lấy nguyên văn từ các câu của script.md (`vo_from: [đoạn, câu đầu, câu cuối]` trong ep-src.yaml) — không thêm thông tin mới."""
import os, re, sys, yaml
H = os.path.dirname(os.path.abspath(__file__))


def script_vo():
    txt = open(f'{H}/script.md').read(); segs = {}; cur = None; buf = []
    for line in txt.split('\n'):
        m = re.match(r'^\[(\d\d) [A-Z0-9 \-]+\]\s*$', line.strip())
        if m:
            if cur: segs[cur] = buf
            cur, buf = m.group(1), []; continue
        if cur is not None: buf.append(line)
    if cur: segs[cur] = buf
    out = {}
    for k, L in segs.items():
        s = ' '.join(x.strip() for x in L if x.strip() and not x.startswith('>') and not x.startswith('#'))
        s = re.sub(r'\s*\{C\d+\}', '', s); s = re.sub(r'\s+', ' ', s).strip(); out[k] = s
    return out


def sentences(s):
    return [x for x in re.split(r'(?<=[.?!])\s+(?=[A-Z"“])', s) if x]


if __name__ == '__main__':
    VO = script_vo(); src = yaml.safe_load(open(f'{H}/ep-src.yaml'))
    src['heroes'] = yaml.safe_load(open(f'{H}/ep-src-heroes.yaml'))['heroes']
    SG = yaml.safe_load(open(f'{H}/ep-src-segs.yaml')); src['segments'] = SG['segments']; src['shorts'] = SG.get('shorts', [])
    for s in src['segments']:
        if s.get('vo') == '@script': s['vo'] = VO[s['id']]
    assert [s['id'] for s in src['segments']] == sorted(VO), (sorted(VO), [s['id'] for s in src['segments']])
    for sh in src.get('shorts', []):
        f = sh.pop('vo_from', None)
        if f:
            S = sentences(VO[f[0]]); i0 = next(i for i, x in enumerate(S) if x.startswith(f[1])); i1 = next(i for i, x in enumerate(S) if x.startswith(f[2]))
            sh['vo'] = ' '.join(S[i0:i1 + 1])
    hd = '# TỆP SINH TỰ ĐỘNG bởi make_spec.py từ ep-src.yaml + script.md (lời khoá ứng viên v8.1). Sửa ep-src.yaml, không sửa tệp này.\n'
    open(f'{H}/episode.yaml', 'w').write(hd + yaml.safe_dump(src, allow_unicode=True, sort_keys=False, width=4000))
    n = sum(len(s['vo'].split()) for s in src['segments'])
    print('episode.yaml', len(src['segments']), 'đoạn,', sum(len(s['shots']) for s in src['segments']), 'shot,', len(src['heroes']), 'cảnh,', n, 'từ lời,', sum(len(s['vo']) for s in src['segments']), 'ký tự')
