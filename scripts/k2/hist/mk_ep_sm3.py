#!/opt/cine/bin/python
"""V5b-2c · ghép ĐẶC TẢ SM3 (1940–42, 7 s) — chỉ để chấm mù ĐỘ RÕ riêng (lệnh E-SM3), từ sm3-spec.json (sm3_spec.py). Không lời; nhạc như đoạn thử SM2.
  mk_ep_sm3.py --spec <sm3-spec.json> --out <episode-sm3.yaml>"""
import argparse, json, yaml


def main():
    a = argparse.ArgumentParser(); a.add_argument('--spec', required=True); a.add_argument('--out', required=True); A = a.parse_args()
    S = json.load(open(A.spec))
    E = dict(id='v5b2c-sm3', title='V5b-2c SM3 clarity test (1940–42)', brand='MOVING PARTS', channel='k2', out='/var/tmp/cine-out/v5b2c-sm3',
             music=[dict(file='assets/k2/music/Tyrant.mp3', **{'from': 'a'}, ss=2.55, gain_db=-3)], sources={}, numbers={},
             heroes=dict(sm3=dict(hero='relief/map', opt=S['hero_opt'])),
             segments=[dict(id='a', part='TEST', chuong='4', dur=7.0, fadeIn=6, fadeOut=8, beats=[dict(t=0.0, k='cut', s='SM3 1940–42')],
                            shots=[dict(tpl='plate', type='strategic', at=0, noi='bien', p=dict(hero='sm3', **S['p']))])])
    open(A.out, 'w').write('# SM3 (1940–42) — chỉ để chấm mù ĐỘ RÕ riêng (lệnh V5b-2c); sinh bằng scripts/k2/hist/mk_ep_sm3.py từ sm3-spec.json — đừng sửa tay\n' + yaml.safe_dump(E, allow_unicode=True, sort_keys=False, width=200))
    print('ghi', A.out)


if __name__ == '__main__':
    main()
