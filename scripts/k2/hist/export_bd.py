#!/opt/cine/bin/python
"""V5b-2c · XUẤT ĐẦU VÀO K-1.14 §9 (khối `ban_do:` của episode.yaml, đường dẫn TƯƠNG ĐỐI thư mục tập) — từ dữ liệu thật, không gõ tay:
  bd/lop-ranh.json   {W, lop: [manifest hist_borders (lop-ranh.json của /cache/hist/<lớp>) + shot 'a/0', t]}
  bd/routes-ve.geojson  tuyến ĐÃ VẼ (ve_tuyen của sm2-spec, sau cắt/thưa) — id, mode, claims, cang (Gibraltar); vùng phong toả mode 'vung'
  bd/claims.json     claim T0xx (gói TUYẾN @434a90f, git show) + S0xx (claims-vay-ham.json) — chỉ id + claim_en + status
  bd/inset.log.json  {W, H, inset: [{id, t (giây phim), box, inset_goc, ly_do, foot_px, vong_dinh_vi}]} từ log 2D của đoạn (render.js .log.json, LL.inset)
  export_bd.py --spec sm2-spec.json --hist <cache/hist/sm2-1782> --tl <out>/timeline.json --sec <out>/sec --dir reports/v5b2c/doan-thu"""
import argparse, json, os, subprocess
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
TUYEN = '434a90f'
# claim theo tuyến (claims-tuyen.json nhóm tiep-te-17xx + S05x của vay-ham, id_goc khớp treatment SM2)
RCLAIMS = {'R1780-RODNEY': ['T009', 'T011', 'S054'], 'R1781-DARBY': ['T013', 'T014', 'S055'], 'R1782-HOWE': ['T015', 'T016', 'S056'], 'Z1779-BLOCKADE': ['T006', 'T007']}
GIB = [-5.3915, 36.1294]


def main():
    a = argparse.ArgumentParser()
    for k in ('spec', 'hist', 'tl', 'sec', 'dir'): a.add_argument('--' + k, required=True)
    A = a.parse_args(); S = json.load(open(A.spec)); D = os.path.join(A.dir, 'bd'); os.makedirs(D, exist_ok=True)
    TL = json.load(open(A.tl)); seg = [s for s in TL['segments'] if s['id'] == 'a'][0]; sh = [x for x in seg['shots'] if x.get('type') == 'strategic'][0]
    t0 = seg.get('t0', seg.get('start', 0.0)); dur = (sh.get('t1') or 6.5) - (sh.get('t0') or 0.0)
    M = json.load(open(os.path.join(A.hist, 'lop-ranh.json')))
    M.update(shot=['a/0'], t=[round(t0 + (sh.get('t0') or 0.0), 3), round(t0 + (sh.get('t0') or 0.0) + dur, 3)], hinh=None)
    M.pop('hinh')
    json.dump(dict(W=1920, lop=[M]), open(os.path.join(D, 'lop-ranh.json'), 'w'), ensure_ascii=False, indent=1)
    F = []
    for rid, pts in S['ve_tuyen'].items():
        if rid.startswith('Z'):
            F.append(dict(type='Feature', properties=dict(id=rid, mode='vung', claims=RCLAIMS[rid]), geometry=dict(type='Polygon', coordinates=[pts])))
        else:
            F.append(dict(type='Feature', properties=dict(id=rid, mode='sea', claims=RCLAIMS[rid], cang=[GIB], vao_tu_mep=True, nguon='channel-k2/k2c-t3-01/tuyen/routes.geojson @' + TUYEN),
                          geometry=dict(type='LineString', coordinates=pts)))
    json.dump(dict(type='FeatureCollection', features=F), open(os.path.join(D, 'routes-ve.geojson'), 'w'), indent=1)
    C = json.loads(subprocess.run(['git', '-C', REPO, 'show', f'{TUYEN}:channel-k2/k2c-t3-01/tuyen/claims-tuyen.json'], capture_output=True, text=True, check=True).stdout)['claims']
    C += json.load(open(os.path.join(REPO, 'channel-k2/k2c-t3-01/vay-ham/claims-vay-ham.json')))['claims']
    need = {c for v in RCLAIMS.values() for c in v} | set(S['ban_do']['claims'])
    out = [dict(id=c['id'], claim_en=c.get('claim_en'), status=c.get('status')) for c in C if c['id'] in need]
    json.dump(dict(nguon=f'claims-tuyen.json @{TUYEN} + channel-k2/k2c-t3-01/vay-ham/claims-vay-ham.json', claims=out), open(os.path.join(D, 'claims.json'), 'w'), ensure_ascii=False, indent=1)
    I = []
    for s in TL['segments']:
        lp = os.path.join(A.sec, s['id'] + '.mkv.log.json')
        if not os.path.exists(lp): continue
        L = json.load(open(lp)); s0 = s.get('t0', s.get('start', 0.0)); smp = [x for x in L.get('inset') or [] if x.get('box')]
        if not smp: continue
        f0, f1 = smp[0]['f'], smp[-1]['f']; last = smp[-1]
        sh = [x for x in s['shots'] if isinstance(x.get('p', {}).get('inset'), (dict, bool))][0]; cfg = sh['p']['inset'] if isinstance(sh['p']['inset'], dict) else {}
        ti = max(0.0, cfg.get('t', 0.6)); dur = min(4.0, max(2.5, cfg.get('dur', 3.0)))   # như k2.js insetLayer (khung mẫu chỉ là mẫu mỗi SAMPLE khung)
        I.append(dict(id=f"{s['id']}-inset", t=[round(s0 + sh['t0'] + ti, 3), round(s0 + sh['t0'] + ti + dur, 3)], t_khung_mau=[round(s0 + f0 / 24, 3), round(s0 + f1 / 24, 3)], box=[round(v) for v in smp[len(smp) // 2]['box']], inset_goc=str(last.get('inset_goc', 'tren_trai')).replace('-', '_'),
                      ly_do=last.get('ly_do'), area_pct=max(x.get('area_pct', 0) for x in smp), foot_px=last.get('foot_px'), vong_dinh_vi=any(x.get('vong_dinh_vi') for x in smp), n_khung_mau=len(smp)))
    json.dump(dict(W=1920, H=1080, inset=I), open(os.path.join(D, 'inset.log.json'), 'w'), ensure_ascii=False, indent=1)
    print('lop 1 · tuyến', len(F), '· claims', len(out), '/', len(need), '· inset', I)


if __name__ == '__main__':
    main()
