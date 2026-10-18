"""G1 T3 · dựng vay-ham/treatment.json bản G1 từ g1/treatment-sau-tuyen.json (= bảng shot gốc + tuyen/treatment-patch.json):
  (1) chèn 6 KHUNG NEO của g1/neo.json (loại '3D phố', neo: true, ai_image theo tấm C, im_lang cho tấm im lặng);
  (2) đặt lại thời lượng theo lời v1 (g1/dur-g1.json: shot → dur, kèm lý do) — 'chốt ở G1 theo lời thật' (TIEN-KY-VAY-HAM §4.1).
Sau đó chạy vay-ham/tu_kiem.py. Dùng: /opt/cine/bin/python -I channel-k2/k2c-t3-01/g1/ap_g1.py"""
import copy, json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent; VH = HERE.parent / 'vay-ham'


def main():
    tr = json.loads((HERE / 'treatment-sau-tuyen.json').read_text()); shots = tr['shots']
    N = json.loads((HERE / 'neo.json').read_text())
    for k in N['khung']:
        v = N['vi_tri'][k['vi_tri']]
        s = dict(id=k['id'], ch=k['ch'], dur=k['dur'], loai='3D phố', noi='thanh_pho', vung=v['vung'], goc=v['goc'], moc_nam=k['moc_nam'],
                 agl_km=k['agl_km'], agl_max_km=k['agl_max_km'], claims=k['claims'], vai='he-qua', may='KHUNG NEO: máy cố định tầm mắt 2–3 m, không chuyển động máy; bộ đếm năm; ' + k['ngay_dem'],
                 du_lieu_nha=v['nguon_bo_cuc'][k['moc_nam']], hero=v['ten'], engine='M9 + phim trường Cycles (PT2)', mo_ta=k['ly_do'],
                 neo=True, ai_image=k['ai_image'], im_lang=k['im_lang'], pt2=k['pt2'], bo_dem=k['bo_dem'], nguoi=k['nguoi'], vat_dong=k['vat_dong'])
        i = next(j for j, x in enumerate(shots) if x['id'] == k['ref_truoc']); shots.insert(i, s)
    D = json.loads((HERE / 'dur-g1.json').read_text())
    for sid, d in {**N.get('doi_dur', {}), **D['dur']}.items():
        x = next(x for x in shots if x['id'] == sid); x['dur_t3b'] = x.get('dur_t3b', x['dur']); x['dur'] = d
    tr['note'] = tr['note'] + ' | G1 18/10: + 6 khung neo (g1/neo.json) + thời lượng theo lời v1 (g1/dur-g1.json; dur_t3b = giá trị cũ).'
    (VH / 'treatment.json').write_text(json.dumps(tr, ensure_ascii=False, indent=1) + '\n')
    print(len(shots), 'shot;', round(sum(s['dur'] for s in shots), 1), 's')
    return subprocess.run([sys.executable, '-I', str(VH / 'tu_kiem.py')], capture_output=True, text=True).returncode


if __name__ == '__main__':
    sys.exit(main())
