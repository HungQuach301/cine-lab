#!/opt/cine/bin/python
"""K2C-T2-01 · ghép đặc tả tập: ep-src.yaml + ep-src-heroes.yaml + ep-src-segs.yaml + lời KHOÁ v3.3 NGUYÊN VĂN (script.md) → episode.yaml.
Lời mỗi đoạn = văn bản sau nhãn [NN PART] trong script.md, bỏ mã claim {Cnn}, gộp đoạn bằng một khoảng trắng (đúng chuỗi gửi ElevenLabs).
Kiểm SHA lời khoá với LOI-KHOA.sha256 trước khi ghép (lời đổi → dừng). Ảnh hàng không: bbox lấy từ $K2V_CACHE/aerial/<tên>/meta.json."""
import hashlib, json, os, re, sys, yaml
H = os.path.dirname(os.path.abspath(__file__))
CACHE = os.environ.get('K2V_CACHE', '/var/tmp/cine-out/k2v-cache')


def script_vo():
    segs, cur, buf = {}, None, []
    for line in open(f'{H}/script.md').read().split('\n'):
        m = re.match(r'^\[(\d\d) [A-Z0-9 \-]+\]\s*$', line.strip())
        if m:
            if cur: segs[cur] = buf
            cur, buf = m.group(1), []; continue
        if cur is not None: buf.append(line)
    if cur: segs[cur] = buf
    out = {}
    for k, L in segs.items():
        s = ' '.join(x.strip() for x in L if x.strip() and not x.startswith(('>', '#')))
        out[k] = re.sub(r'\s+', ' ', re.sub(r'\s*\{C\d+\}', '', s)).strip()
    return out


def aerial_bbox(H_):
    for h in H_.values():
        for a in (h.get('opt') or {}).get('aerial') or []:
            if a.get('bbox') == 'auto':
                m = re.match(r'/cache/aerial/([^/]+)/t(\d+)\.png', a['img']); meta = json.load(open(os.path.join(CACHE, 'aerial', m.group(1), 'meta.json')))
                T = meta['tiers'][int(m.group(2))]; a['bbox'] = T.get('bbox') or T.get('bbox_deg')


if __name__ == '__main__':
    want = {l.split()[1]: l.split()[0] for l in open(f'{H}/LOI-KHOA.sha256') if l.strip()}
    got = hashlib.sha256(open(f'{H}/script.md', 'rb').read()).hexdigest()
    if got != want['script.md']: raise SystemExit(f'LỜI KHOÁ ĐỔI: script.md {got[:12]} ≠ LOI-KHOA.sha256 {want["script.md"][:12]}')
    VO = script_vo(); E = yaml.safe_load(open(f'{H}/ep-src.yaml'))
    E['heroes'] = yaml.safe_load(open(f'{H}/ep-src-heroes.yaml'))['heroes']
    SG = yaml.safe_load(open(f'{H}/ep-src-segs.yaml')); E['segments'] = SG['segments']; E['shorts'] = SG.get('shorts', [])
    for s in E['segments']:
        if s.get('vo') == '@script': s['vo'] = VO[s['id']]
    assert [s['id'] for s in E['segments']] == sorted(VO), (sorted(VO), [s['id'] for s in E['segments']])
    try: aerial_bbox(E['heroes'])
    except FileNotFoundError as e: print('CẢNH BÁO: chưa có ảnh hàng không —', e, file=sys.stderr)
    out = sys.argv[1] if len(sys.argv) > 1 else f'{H}/episode.yaml'
    with open(out, 'w') as f:
        f.write('# TỆP SINH TỰ ĐỘNG bởi make_spec.py từ ep-src*.yaml + script.md (lời KHOÁ v3.3, SHA ở LOI-KHOA.sha256). Sửa ep-src*.yaml, không sửa tệp này.\n')
        yaml.safe_dump(E, f, allow_unicode=True, sort_keys=False, width=200)
    print(out, len(E['segments']), 'đoạn', sum(len(s['shots']) for s in E['segments']), 'shot', len(E['heroes']), 'cảnh')
