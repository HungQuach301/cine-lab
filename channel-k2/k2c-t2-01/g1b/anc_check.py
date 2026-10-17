import json, yaml, os, glob, sys
S = yaml.safe_load(open(sys.argv[2] if len(sys.argv) > 2 else '/home/user/cine-lab/channel-k2/k2c-t2-01/g1b/tokhung.yaml'))
base = sys.argv[1] if len(sys.argv) > 1 else '/var/tmp/cine-out/k2v-shots/t2-tokhung'   # đo tỉ lệ khung có điểm neo trong vùng an toàn (x 4–96 %, y 6–80 %)
for gi, sg in enumerate(S['segments']):
    d = glob.glob(f'{base}/hero{gi}-*')
    if not d or not os.path.exists(d[0] + '/anchors.json'): continue
    A = json.load(open(d[0] + '/anchors.json')); f0 = sg['shots'][0]['p'].get('frame0', 0)
    p = sg['shots'][0]['p']; want = set()
    for k in ('tags', 'places', 'stickers', 'labels'):
        for x in p.get(k) or []:
            if x.get('a'): want.add(x['a'])
    out = []
    for a in sorted(want):
        fr = [A[str(f)].get(a) for f in range(f0, f0 + 144) if str(f) in A]
        fr = [v for v in fr if v]
        if not fr: out.append(f'{a}:KHÔNG-CÓ'); continue
        vis = [v for v in fr if v[2] and 0.04 < v[0] < 0.96 and 0.06 < v[1] < 0.80]
        out.append(f'{a}:{100*len(vis)//len(fr)}%')
    print(sg['id'], p.get('hero'), ' '.join(out))
