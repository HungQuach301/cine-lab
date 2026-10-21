#!/opt/cine/bin/python -I
"""NC-N2P · chấm KIỂM CÓ ĐÁP ÁN: so kết luận của kiem_n2p.py (+ q_thoi_dai.py) với dap-an.json.
Một lỗi chèn được BẮT khi bộ kiểm báo đúng NHÓM luật (thoi_dai → (ii); lop_a → (i); dong_bang → (iv)) với hộp có tâm nằm trong hộp đáp án nở 40 px (hoặc ngược lại).
Báo: bắt/6 theo từng mô hình và hợp hai mô hình; báo thừa (cảnh báo không ứng với lỗi chèn nào) theo nhóm.
  cham_dap_an.py <dap-an.json> <dap-an-kiem.json> [<q_thoi_dai ra.json>] > ket-qua"""
import json, sys

W, H, PAD = 1920, 1080, 40


def hit(box_n, hop):
    x0, y0, x1, y1 = box_n[0] * W, box_n[1] * H, box_n[2] * W, box_n[3] * H; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    a0, b0, a1, b1 = hop[0] - PAD, hop[1] - PAD, hop[2] + PAD, hop[3] + PAD
    return (a0 <= cx <= a1 and b0 <= cy <= b1) or (x0 <= (hop[0] + hop[2]) / 2 <= x1 and y0 <= (hop[1] + hop[3]) / 2 <= y1)


def main():
    D = json.load(open(sys.argv[1])); K = json.load(open(sys.argv[2])); Q = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else None
    nhom = {'thoi_dai': K['ii_thoi_dai']['loi'], 'lop_a': K['i_lop_a']['vat_lop_a'], 'dong_bang': K['iv_dong_bang']['loi']}
    q = []
    if Q:
        for kh in Q.get('khung', Q.get('frames', [])) if isinstance(Q, dict) else []:
            for x in kh.get('nghi_van', []):
                if x.get('toa_do_px'): b = x['toa_do_px']; q.append(dict(mh='q_thoi_dai', toa_do=[b[0] / W, b[1] / H, b[2] / W, b[3] / H]))
    R = {'vat': [], 'tong': {}}
    for mh in ('gpt', 'claude', 'hop'):
        R['tong'][mh] = 0
    for v in D['vat']:
        r = dict(id=v['id'], loai_loi=v['loai_loi'], bat={})
        for mh in ('gpt', 'claude'):
            r['bat'][mh] = any(x['mh'] == mh and hit(x['toa_do'], v['hop']) for x in nhom[v['loai_loi']])
        r['bat']['hop'] = r['bat']['gpt'] or r['bat']['claude']
        if v['loai_loi'] == 'thoi_dai' and q: r['bat']['q_thoi_dai'] = any(hit(x['toa_do'], v['hop']) for x in q)
        for mh in ('gpt', 'claude', 'hop'): R['tong'][mh] += int(r['bat'][mh])
        R['vat'].append(r)
    thua = {}
    for g, xs in nhom.items():
        for x in xs:
            if not any(hit(x['toa_do'], v['hop']) and v['loai_loi'] == g for v in D['vat']):
                thua.setdefault(g, []).append(dict(mh=x['mh'], loai=x.get('loai'), mo_ta=x.get('mo_ta'), cung_vat_chen_khac=any(hit(x['toa_do'], v['hop']) for v in D['vat'])))
    R['bao_thua'] = thua; R['n'] = len(D['vat'])
    if q: R['tong']['q_thoi_dai_bat_thoi_dai'] = sum(1 for v in R['vat'] if v['bat'].get('q_thoi_dai')); R['tong']['q_thoi_dai_so_nghi_van'] = len(q)
    print(json.dumps(R, ensure_ascii=False, indent=1))


if __name__ == '__main__': main()
