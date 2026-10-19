#!/opt/cine/bin/python
"""G1b-T3 · việc 6.2 — BẢN THỬ NHỎ: rút chu kỳ đi từ BVH mocap (100STYLE CC BY 4.0) thành hệ số Fourier cho các khớp của people.js
(hông, gối, vai, khuỷu — góc trong mặt phẳng dọc hướng đi), để thay sin đơn trong shader bằng đường cong thật mà KHÔNG cần khung xương/skinning.
  mocap_gait.py <tệp.bvh> [<tệp2.bvh> …]  → in JSON {clip: {chu_ky_s, khop: {ten: {tb, a1, p1, a2, p2, min, max}}}}"""
import sys, json, os, numpy as np

def parse(p):
    L = open(p).read().split('\n'); joints, stack, chans, i = [], [], [], 0
    while not L[i].strip().startswith('MOTION'):
        t = L[i].split()
        if t and t[0] in ('ROOT', 'JOINT'): joints.append({'name': t[1], 'parent': stack[-1] if stack else -1}); cur = len(joints) - 1
        elif t and t[0] == 'End': joints.append({'name': joints[stack[-1]]['name'] + '_end', 'parent': stack[-1], 'end': True}); cur = len(joints) - 1
        elif t and t[0] == '{': stack.append(cur)
        elif t and t[0] == '}': stack.pop()
        elif t and t[0] == 'OFFSET': joints[cur]['off'] = np.array([float(x) for x in t[1:4]])
        elif t and t[0] == 'CHANNELS': joints[cur]['ch'] = t[2:]; joints[cur]['c0'] = sum(len(j.get('ch', [])) for j in joints[:cur])
        i += 1
    dt = float(L[i + 2].split()[-1]); M = np.array([[float(x) for x in l.split()] for l in L[i + 3:] if l.strip()])
    return joints, dt, M

def R(ax, a):
    c, s = np.cos(a), np.sin(a); n = len(a); m = np.zeros((n, 3, 3)); m[:, 0, 0] = m[:, 1, 1] = m[:, 2, 2] = 1
    i, j = {'X': (1, 2), 'Y': (2, 0), 'Z': (0, 1)}[ax]; m[:, i, i] = c; m[:, j, j] = c; m[:, i, j] = -s; m[:, j, i] = s; return m

def fk(joints, M):
    n = len(M); P = {}; Rw = {}
    for k, j in enumerate(joints):
        rot = np.tile(np.eye(3), (n, 1, 1)); pos = np.tile(j.get('off', np.zeros(3)), (n, 1)); c = j.get('c0', 0)
        for q, ch in enumerate(j.get('ch', [])):
            v = M[:, c + q]
            if ch.endswith('position'): pos = pos + 0  # vị trí gốc: bỏ (chỉ cần góc)
            else: rot = rot @ R(ch[0], np.radians(v))
        if j['parent'] < 0: Rw[k] = rot; P[k] = np.zeros((n, 3))
        else: pr = j['parent']; P[k] = P[pr] + np.einsum('nij,nj->ni', Rw[pr], pos); Rw[k] = Rw[pr] @ rot
    return P

def main(paths):
    out = {}
    for p in paths:
        J, dt, M = parse(p); P = fk(J, M); ix = {j['name']: k for k, j in enumerate(J)}
        fwd = P[ix['LeftHip']] - P[ix['RightHip']]; up = P[ix['Neck']] - P[ix['Hips']]
        up /= np.linalg.norm(up, axis=1, keepdims=True); side = fwd / np.linalg.norm(fwd, axis=1, keepdims=True); f = np.cross(side, up)   # hướng trước (theo thân)
        def ang(a, b, ref=None):   # góc đoạn a→b so với "xuống" trong mặt phẳng dọc (trước +)
            v = P[ix[b]] - P[ix[a]]; return np.degrees(np.arctan2((v * f).sum(1), -(v * up).sum(1)))
        A = {'hong_trai': ang('LeftHip', 'LeftKnee'), 'hong_phai': ang('RightHip', 'RightKnee'),
             'goi_trai': ang('LeftHip', 'LeftKnee') - ang('LeftKnee', 'LeftAnkle'), 'vai_trai': ang('LeftShoulder', 'LeftElbow'),
             'khuyu_trai': ang('LeftElbow', 'LeftWrist') - ang('LeftShoulder', 'LeftElbow')}
        h = A['hong_trai'] - A['hong_trai'].mean(); sp = np.abs(np.fft.rfft(h)); fr = np.fft.rfftfreq(len(h), dt); k0 = 1 + np.argmax(sp[1:len(sp) // 4])
        T = 1 / fr[k0]
        # pha cục bộ (Hilbert trên dải quanh tần số cơ bản) — clip có quay đầu/đổi tốc, pha cố định khớp kém; bỏ đoạn biên độ thấp (đứng/quay)
        Hf = np.fft.rfft(h); band = (fr > fr[k0] * 0.6) & (fr < fr[k0] * 1.6); Hf[~band] = 0; full = np.zeros(len(h), complex); full[:len(Hf)] = Hf * 2; full[0] = 0
        an = np.fft.ifft(full); ph = np.angle(an); keep = np.abs(an) > 0.5 * np.median(np.abs(an))
        A = {k: v[keep] for k, v in A.items()}; ph = ph[keep]
        res = {}
        for name, a in A.items():   # bình phương tối thiểu: a ≈ tb + a1 sin(φ + p1) + a2 sin(2φ + p2) (φ = pha hông trái)
            X = np.stack([np.ones_like(ph), np.sin(ph), np.cos(ph), np.sin(2 * ph), np.cos(2 * ph)], 1); c = np.linalg.lstsq(X, a, rcond=None)[0]
            res[name] = {'tb': round(float(c[0]), 1), 'a1': round(float(np.hypot(c[1], c[2])), 1), 'p1': round(float(np.arctan2(c[2], c[1])), 2),
                         'a2': round(float(np.hypot(c[3], c[4])), 1), 'p2': round(float(np.arctan2(c[4], c[3])), 2), 'min': round(float(np.percentile(a, 2)), 1), 'max': round(float(np.percentile(a, 98)), 1),
                         'r2': round(float(1 - ((X @ c - a) ** 2).sum() / ((a - a.mean()) ** 2).sum()), 2)}
        out[os.path.basename(p)] = {'khung': len(M), 'khung_dung': int(keep.sum()), 'dt': dt, 'chu_ky_s': round(float(T), 3), 'khop_do': res}
    print(json.dumps(out, indent=1, ensure_ascii=False))

if __name__ == '__main__':
    main(sys.argv[1:])
