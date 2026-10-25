#!/opt/cine/bin/python
"""K-1.17.8 · LUẬT E — chạy q_n2p.check (1.17.8, chưa khoá) trên các tấm đáp án P9-2026; --vision gọi 2 mô hình nhìn (đề bài PROMPT_E).
Bộ đệm <out>/n2p-vision-cache.json; chi phí <out>/n2p-cost.jsonl. In bảng + ghi ra.json.   chay_e.py <thư mục e> <out> [--vision] [--chi a,b,…]"""
import json, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))
from checks.ll import q_n2p as N  # noqa: E402

TAM = (('ngay', 'render.png', False), ('dem', 'render-dem.png', True), ('xau', 'render.png', False), ('ngay-thap_bia', 'render.png', False),
       ('ngay-thap_thap', 'render.png', False), ('ngay-chu', 'render.png', False), ('dem-chu', 'render-dem.png', True), ('ngay-xoa_toa', 'render.png', False),
       ('ngay-doi_toa', 'render.png', False), ('ngay-thuyen', 'render.png', False))


def main():
    a = sys.argv[1:]; d, out = a[0], a[1]; os.chdir(d)
    chi = a[a.index('--chi') + 1].split(',') if '--chi' in a else [x[0] for x in TAM]
    toa = json.load(open('toa.json')); T = [dict(ten=t['ten'], mau=t['mau']) for t in toa]
    tam = [dict(id=g, shot='H5-04', render=rd, ghep=f'g/{g}.png', mat_na='matna-e.png', mat_na_ct='matna-ct.png', toa_co_ten=T, nam=2026, dem=dm,
                n2p_toan_khung_hien_dai=True, cu_may='CODINH', noi='London') for g, rd, dm in TAM if g in chi]
    E = dict(id='dap-an-e', kenh2_tu_t4=True, n2p=dict(noi='London', t4=False, tam=tam), out=out)
    R = N.check(E, None, '.', [dict(shot='H5-04', cu_may='CODINH', ai_nen=True, dur=10)], vision='--vision' in a)
    json.dump(R, open(os.path.join(out, 'ra.json'), 'w'), ensure_ascii=False, indent=1, default=str)
    for k, v in R.items():
        print(k, v.get('ket_qua') or ('ĐẠT' if v['ok'] else 'TRƯỢT'), '·', v['val'][:400])
        for x in (v['loi'] + (v.get('thieu') or [])): print('   ', x[:260])


if __name__ == '__main__':
    main()
