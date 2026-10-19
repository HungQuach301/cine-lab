"""Đáp án ranh shot từ episode.yaml: [(t, loai, mo_ta)] loai = 'cat' (đổi góc/nguồn hình) | 'lien' (cùng máy, đổi năm/giờ)"""
import sys, json, yaml
sys.path.insert(0, '/home/user/cine-lab')
from checks.ll import q_k116 as q

def pose_end(c):
    k = c.get('k')
    if k == 'push': return ('push', tuple(c['to']), tuple(c['look']), c.get('fov'))
    if k == 'neo': return ('neo', json.dumps(c['pose'], sort_keys=True))
    d = {kk: v for kk, v in c.items() if kk not in ('dur', 'hold')}
    if k == 'orbit': d['a'] = d.pop('a1'); d.pop('a0')
    if k == 'top': d['hh'] = d.pop('h1'); d.pop('h0'); d['yy'] = d.pop('yaw1'); d.pop('yaw0')
    if k == 'line': d['s'] = d.pop('s1'); d.pop('s0')
    return (k, json.dumps(d, sort_keys=True))

def pose_start(c):
    k = c.get('k')
    if k == 'push': return ('push', tuple(c['from']), tuple(c['look']), c.get('fov'))
    if k == 'neo': return ('neo', json.dumps(c['pose'], sort_keys=True))
    d = {kk: v for kk, v in c.items() if kk not in ('dur', 'hold')}
    if k == 'orbit': d['a'] = d.pop('a0'); d.pop('a1')
    if k == 'top': d['hh'] = d.pop('h0'); d.pop('h1'); d['yy'] = d.pop('yaw0'); d.pop('yaw1')
    if k == 'line': d['s'] = d.pop('s0'); d.pop('s1')
    return (k, json.dumps(d, sort_keys=True))

def elements(E):
    H = E.get('heroes') or {}; out = []
    for z in q.shot_list(E, None):
        sh = z['spec']; p = sh.get('p') or {}; hk = p.get('hero'); h = H.get(hk) or {}
        cams = (h.get('opt') or {}).get('cams') or []
        mod = h.get('hero')
        if z['ty'] in ('scene3d', 'timelapse') and cams:
            t = z['t0']
            for j, c in enumerate(cams):
                if t >= z['t1'] - 1e-6: break
                out.append(dict(t=t, mod=mod, ps=pose_start(c), pe=pose_end(c), id=f"{z['seg']}/{z['i']}/cam{j}"))
                t += float(c.get('dur') or 0)
        elif z['ty'] in ('scene3d', 'timelapse') and mod and str(mod).startswith('tl/'):
            out.append(dict(t=z['t0'], mod=mod, ps=('fixed', hk), pe=('fixed', hk), id=f"{z['seg']}/{z['i']}"))
        else:
            out.append(dict(t=z['t0'], mod=z['ty'], ps=('flat', hk or z['seg']), pe=('flat', hk or z['seg']), id=f"{z['seg']}/{z['i']}"))
    return out

def truth(E):
    el = elements(E); out = []
    for a, b in zip(el, el[1:]):
        if b['t'] < 0.05: continue
        same = a['mod'] == b['mod'] and a['pe'] == b['ps']
        out.append((round(b['t'], 3), 'lien' if same else 'cat', f"{a['id']}→{b['id']}"))
    return out

if __name__ == '__main__':
    E = yaml.safe_load(open(sys.argv[1])); T = truth(E)
    print(len(T), sum(x[1] == 'cat' for x in T), sum(x[1] == 'lien' for x in T))
    cs = q.cut_times_spec(E, None); ts = [x[0] for x in T]
    print('spec cuts not in truth:', [round(c, 2) for c in cs if min(abs(c - t) for t in ts) > 0.05])
    print('truth not in spec cuts:', [x for x in T if min(abs(c - x[0]) for c in cs) > 0.05])
    json.dump(T, open(sys.argv[2], 'w'), ensure_ascii=False, indent=0)
