#!/opt/cine/bin/python
"""V5b-2c · ghép ĐẶC TẢ ĐOẠN THỬ (episode.yaml) cho dây chuyền kênh 2 từ sm2-spec.json (sm2_spec.py) — không gõ tay toạ độ tuyến/ranh.
Đoạn a: SM2 strategic (M13-lite, 6,5 s + hoà 0,5 s) → cảnh 3D vịnh 1782 (tl/vinh1782, có inset B4 ở cú bay đầu).
Đoạn b: SM2 DỰ PHÒNG NC-BD §2.4 (relief/map: bờ + tuyến + nhãn + ≤ 3 vùng), cùng nội dung — để chấm mù so.
Đoạn c–f: cảnh V0 nâng hình (phố 1782 dày, toàn cảnh đông người, eo đất vây hãm, khung neo PT).
  mk_ep_v5b2c.py --spec <sm2-spec.json> --out <episode.yaml>"""
import argparse, json, yaml


def main():
    a = argparse.ArgumentParser(); a.add_argument('--spec', required=True); a.add_argument('--out', required=True); A = a.parse_args()
    S = json.load(open(A.spec)); B = S['ban_do']
    COLS = {'Britain': ('britain', '#b03a2e'), 'Spain': ('spain', '#c9a227'), 'France': ('france', '#2e5c8a')}
    KB = dict(nghieng=max(B['nghieng']), be_ngang_km=B['be_ngang_km'], dong=[dict(d, id=i) for d, i in zip(B['dong'], ['R1780-RODNEY+R1781-DARBY+R1782-HOWE', 'Z1779-BLOCKADE'])],
              chu_giai=[dict(faction_id=COLS[n][0], mau=COLS[n][1], nhan=n) for n in B['chu_giai']], chi_toi=['Bay of Gibraltar'], lop=[B['lop']], nam=B['nam'], tuyen=B['tuyen'], claims=B['claims'])   # định dạng K-1.14 (fixture ep-bd: khai trong p)
    strat = dict(tpl='plate', type='strategic', at=0, noi='bien', p=dict(dict(hero='sm2', **S['p']), **KB))
    vin = lambda at, noi, f0, extra=None: dict(tpl='plate', type='scene3d', at=at, noi=noi, p=dict(dict(hero='a_vinh', kind='', frame0=f0, where='Bay of Gibraltar'), **(extra or {})))
    ins = dict(inset=dict(t=0.6, dur=3.0), inset_map='eo-gib', inset_labels=[dict(s='Gibraltar', ll=[-5.353, 36.14], dx=24, dy=8), dict(s='Strait of Gibraltar', ll=[-5.75, 35.93], dx=-120, dy=34)],
               inset_ly_do='B4: góc trên trái; vào nơi mới sau bản đồ chiến lược')
    shots_a = [strat, dict(vin(6.5, 'bien', 0, ins), **{'in': dict(type='dissolve', d=0.5)}), vin(12.1, 'thanh_pho', 134.4, dict(ghost='ghost-1782', city=True)), vin(18.5, 'vung', 288)]
    E = dict(id='v5b2c-t', title='V5b-2c-T — strategic map SM2 → Gibraltar 1782 + V0 uplift', brand='MOVING PARTS', channel='k2', out='/var/tmp/cine-out/v5b2c-t',
             music=[dict(file='assets/k2/music/Tyrant.mp3', **{'from': 'a'}, ss=2.55, gain_db=-3)], sources={}, numbers={},
             ban_do=dict(lop='bd/lop-ranh.json', tuyen='bd/routes-ve.geojson', inset='bd/inset.log.json', claims='bd/claims.json'),
             heroes=dict(sm2=dict(hero='relief/map', opt=S['hero_opt']), sm2fb=dict(hero='relief/map', opt=S['fallback_opt']),
                         a_vinh=dict(hero='tl/vinh1782', cam='lien-hoan', opt=dict(pack='gib', cau='lien-hoan')), c_pho=dict(hero='tl/pho1782', opt=dict(pack='gib', cau='fly-pho')),
                         d_toan=dict(hero='tl/toan1782', opt=dict(pack='gib', cau='push-in')), e_eo=dict(hero='tl/eo1782', opt=dict(pack='gib', cau='lateral-parallax')),
                         f_neo=dict(hero='tl/neo1782', opt=dict(pack='gib', cau='neo'))),
             segments=[dict(id='a', part='TEST', chuong='2', dur=24.5, fadeIn=6, beats=[dict(t=0.0, k='cut', s='strategic map: three relief convoys'), dict(t=6.5, k='dissolve', s='into the bay, 1782')], shots=shots_a),
                       dict(id='b', part='TEST', chuong='2-du-phong', dur=7.0, beats=[dict(t=0.0, k='cut', s='fallback map (coast + routes + labels)')], shots=[dict(tpl='plate', type='map', at=0, noi='bien', p=dict(hero='sm2fb', **S['fallback_p']))]),
                       dict(id='c', part='TEST', chuong='v0', dur=8.0, beats=[dict(t=0.0, k='cut', s='Main Street 1782, estimated infill')], shots=[dict(tpl='plate', type='scene3d', at=0, noi='thanh_pho', p=dict(hero='c_pho', kind='', ghost='ghost-1782', city=True))]),
                       dict(id='d', part='TEST', chuong='v0', dur=6.0, beats=[dict(t=0.0, k='cut', s='garrison town panorama')], shots=[dict(tpl='plate', type='scene3d', at=0, noi='thanh_pho', p=dict(hero='d_toan', kind='', ghost='ghost-1782', city=True))]),
                       dict(id='e', part='TEST', chuong='v0', dur=4.0, beats=[dict(t=0.0, k='cut', s='Spanish lines and the north face')], shots=[dict(tpl='plate', type='scene3d', at=0, noi='eo_dat', p=dict(hero='e_eo', kind=''))]),
                       dict(id='f', part='TEST', chuong='v0', dur=8.0, fadeOut=8, beats=[dict(t=0.0, k='cut', s='fixed view, one day (PT anchor)')], shots=[dict(tpl='plate', type='scene3d', at=0, noi='thanh_pho', p=dict(hero='f_neo', kind='', ghost='ghost-1782', city=True))])])
    hdr = ('# ĐOẠN THỬ V5b-2c-T (sinh bằng scripts/k2/hist/mk_ep_v5b2c.py từ sm2-spec.json — đừng sửa tay toạ độ): a = SM2 bản đồ chiến lược M13-lite → hoà 0,5 s → vịnh 1782 (inset B4);\n'
           '# b = SM2 dự phòng NC-BD §2.4 (relief/map hiện có) cùng nội dung; c–f = cảnh V0 nâng hình. Không lời (ElevenLabs 0); nhạc có dòng RIGHTS K2-MUS.\n')
    open(A.out, 'w').write(hdr + yaml.safe_dump(E, allow_unicode=True, sort_keys=False, width=200))
    print('ghi', A.out)


if __name__ == '__main__':
    main()
