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
    # G2: chuỗi gửi ElevenLabs phải trùng loi-khoa.txt (SHA ở LOI-KHOA.sha256), từng đoạn, sau khi gộp khoảng trắng
    got = hashlib.sha256(open(f'{H}/loi-khoa.txt', 'rb').read()).hexdigest()
    if got != want['loi-khoa.txt']: raise SystemExit(f'LỜI KHOÁ ĐỔI: loi-khoa.txt {got[:12]} ≠ LOI-KHOA.sha256')
    Lk = re.split(r'^\[(\d\d) [^\]]+\]\s*$', open(f'{H}/loi-khoa.txt').read(), flags=re.M); LK = {Lk[i]: re.sub(r'\s+', ' ', Lk[i + 1]).strip() for i in range(1, len(Lk), 2)}
    bad = [k for k in VO if VO[k] != LK.get(k)]
    if bad: raise SystemExit(f'script.md ≠ loi-khoa.txt ở đoạn {bad}')
    E['heroes'] = yaml.safe_load(open(f'{H}/ep-src-heroes.yaml'))['heroes']
    SG = yaml.safe_load(open(f'{H}/ep-src-segs.yaml')); E['segments'] = SG['segments']; E['shorts'] = SG.get('shorts', [])
    for s in E['segments']:
        if s.get('vo') == '@script': s['vo'] = VO[s['id']]
    def sentences(t): return re.split(r'(?<=[.?!])\s+(?=[A-Z])', t)
    for sh in E['shorts']:   # Short: lời = các câu NGUYÊN VĂN của lời khoá, vo_from [[đoạn, câu đầu, câu cuối], …]
        R = sh.pop('vo_from', None)
        if R:
            out = []
            for sid, a, b in R:
                S = sentences(VO[sid]); i0 = next(i for i, x in enumerate(S) if x.startswith(a)); i1 = next(i for i, x in enumerate(S) if x.startswith(b)); out += S[i0:i1 + 1]
            sh['vo'] = ' '.join(out)
    assert [s['id'] for s in E['segments']] == sorted(VO), (sorted(VO), [s['id'] for s in E['segments']])
    # mốc số ở lớp 2D (p.places/tags/stickers/labels/cap/year/title .at) là giây TRONG ĐOẠN (k2.js); ở shot không mở đoạn, nguồn ghi số = giây SAU ĐẦU SHOT
    # → đổi thành mốc lời của shot cộng bù (vd shot "@June-0.3", at 0.3 → "@June+0.00"), để vật hiện đúng lúc trong shot thay vì đã có sẵn khi cắt vào. Mục có seg: true giữ giây trong đoạn (câu miễn trừ 0:03–0:12 vắt qua hai shot đầu).
    def rel(v, base):
        m = re.match(r'^(@.+?)([+-]\d+(?:\.\d+)?)?$', base); o = float(m.group(2) or 0) + v
        return f'{m.group(1)}{o:+.2f}'
    for s in E['segments']:
        for sh in s['shots']:
            if not isinstance(sh.get('at'), str): continue
            p = sh['p']
            for k in ('places', 'tags', 'stickers', 'labels', 'cap'):
                for x in p.get(k) or []:
                    if isinstance(x.get('at'), (int, float)) and not x.get('seg'): x['at'] = rel(x['at'], sh['at'])
            for k in ('year', 'title'):
                if isinstance(p.get(k), dict) and isinstance(p[k].get('at'), (int, float)): p[k]['at'] = rel(p[k]['at'], sh['at'])
    try: aerial_bbox(E['heroes'])
    except FileNotFoundError as e: print('CẢNH BÁO: chưa có ảnh hàng không —', e, file=sys.stderr)
    out = sys.argv[1] if len(sys.argv) > 1 else f'{H}/episode.yaml'
    with open(out, 'w') as f:
        f.write('# TỆP SINH TỰ ĐỘNG bởi make_spec.py từ ep-src*.yaml + script.md (lời KHOÁ v3.3, SHA ở LOI-KHOA.sha256). Sửa ep-src*.yaml, không sửa tệp này.\n')
        yaml.safe_dump(E, f, allow_unicode=True, sort_keys=False, width=200)
    print(out, len(E['segments']), 'đoạn', sum(len(s['shots']) for s in E['segments']), 'shot', len(E['heroes']), 'cảnh')
