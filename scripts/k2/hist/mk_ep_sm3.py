#!/opt/cine/bin/python
"""V5b-2c · ghép ĐẶC TẢ SM3 (1940–42, 7 s) — chỉ để chấm mù ĐỘ RÕ riêng (lệnh E-SM3), từ sm3-spec.json (sm3_spec.py). Không lời; nhạc như đoạn thử SM2.
  mk_ep_sm3.py --spec <sm3-spec.json> --out <episode-sm3.yaml>
V5b-2d · SM3 TÁCH (sm3_spec.py --tach → sm3-spec-a.json, sm3-spec-b.json): nhiều --spec → MỘT tập nhiều đoạn (a = SM3a 1940, b = SM3b 1942, …),
  mỗi đoạn một cảnh đinh relief/map riêng (sm3a, sm3b), dài theo trường `dur` của đặc tả; mờ vào 6 khung ở đoạn đầu, mờ ra 8 khung ở đoạn cuối, CẮT THẲNG giữa các đoạn.
  mk_ep_sm3.py --spec sm3-spec-a.json sm3-spec-b.json --out <episode-sm3-tach.yaml> [--id v5b2d-sm3] [--out-dir /var/tmp/cine-out/v5b2d-sm3]
  Một --spec (không `dur`) → đúng tập 7 s của V5b-2c như cũ."""
import argparse, json, yaml

LABEL = {'a': 'SM3a 1940 — evacuation of civilians', 'b': 'SM3b 1942 — Operation Torch'}


def main():
    a = argparse.ArgumentParser(); a.add_argument('--spec', required=True, nargs='+'); a.add_argument('--out', required=True)
    a.add_argument('--id'); a.add_argument('--out-dir'); A = a.parse_args()
    SS = [json.load(open(p)) for p in A.spec]
    if len(SS) == 1 and 'dur' not in SS[0]:
        S = SS[0]
        E = dict(id=A.id or 'v5b2c-sm3', title='V5b-2c SM3 clarity test (1940–42)', brand='MOVING PARTS', channel='k2', out=A.out_dir or '/var/tmp/cine-out/v5b2c-sm3',
                 music=[dict(file='assets/k2/music/Tyrant.mp3', **{'from': 'a'}, ss=2.55, gain_db=-3)], sources={}, numbers={},
                 heroes=dict(sm3=dict(hero='relief/map', opt=S['hero_opt'])),
                 segments=[dict(id='a', part='TEST', chuong='4', dur=7.0, fadeIn=6, fadeOut=8, beats=[dict(t=0.0, k='cut', s='SM3 1940–42')],
                                shots=[dict(tpl='plate', type='strategic', at=0, noi='bien', p=dict(hero='sm3', **S['p']))])])
        head = '# SM3 (1940–42) — chỉ để chấm mù ĐỘ RÕ riêng (lệnh V5b-2c); sinh bằng scripts/k2/hist/mk_ep_sm3.py từ sm3-spec.json — đừng sửa tay\n'
    else:
        ids = [chr(ord('a') + i) for i in range(len(SS))]; n = len(SS)
        heroes, segs = {}, []
        for i, (sid, S) in enumerate(zip(ids, SS)):
            hk = f'sm3{sid}'; heroes[hk] = dict(hero='relief/map', opt=S['hero_opt'])
            segs.append(dict(id=sid, part='TEST', chuong='4', dur=float(S.get('dur', 3.5)), fadeIn=6 if i == 0 else 0, fadeOut=8 if i == n - 1 else 0,
                             beats=[dict(t=0.0, k='cut', s=LABEL.get(sid, f'SM3{sid}'))],
                             shots=[dict(tpl='plate', type='strategic', at=0, noi='bien', p=dict(hero=hk, **S['p']))]))
        E = dict(id=A.id or 'v5b2d-sm3', title='V5b-2d SM3 split (SM3a 1940 | SM3b 1942)', brand='MOVING PARTS', channel='k2', out=A.out_dir or '/var/tmp/cine-out/v5b2d-sm3',
                 music=[dict(file='assets/k2/music/Tyrant.mp3', **{'from': 'a'}, ss=2.55, gain_db=-3)], sources={}, numbers={}, heroes=heroes, segments=segs)
        head = f"# SM3 TÁCH (V5b-2d, C2-4): {' | '.join(LABEL.get(s, s) for s in ids)}; sinh bằng scripts/k2/hist/mk_ep_sm3.py từ {', '.join(A.spec)} — đừng sửa tay\n"
    open(A.out, 'w').write(head + yaml.safe_dump(E, allow_unicode=True, sort_keys=False, width=200))
    print('ghi', A.out, 'đoạn', [s['id'] for s in E['segments']])


if __name__ == '__main__':
    main()
