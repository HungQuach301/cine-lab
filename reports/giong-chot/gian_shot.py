#!/opt/cine/bin/python
"""GIỌNG-CHỐT · Đ2 (c): đề xuất giãn bảng shot T3 theo nhịp G1 — CHỈ ĐỌC vay-ham/treatment.json + g1/kiem-chu.json, KHÔNG sửa.
gian_shot.py <lời T3 ước, giây> [nhãn] → in bảng; ghi gian-shot-<nhãn>.json
Mô hình: lời shot i = L × (từ nói của shot i / tổng từ nói) (nhịp G1 đã gồm ngừng giữa câu); lời chảy tuần tự, mỗi shot cần lời + 0,4 s (luật G1).
Luật giãn (lệnh): ưu tiên shot 3D có máy chạy; KHÔNG giãn tấm im lặng; KHÔNG cắt lời; KHÔNG rút shot đang dư.
 - giãn được: 3D phố/vùng không phải khung neo, mốc đinh, cú liên hoàn; và không phải shot cố định 0c (NC-H2 3 s).
 - thẻ/ảnh/tranh/bản đồ: giãn trong trần loại (thẻ số 8 · ảnh, tranh, bản đồ lịch sử 12 · bản đồ chiến lược 8 — fit_khoa.py), phần vượt trần chảy sang shot giãn được KẾ TIẾP.
 - khung neo, mốc đinh, cú liên hoàn, 0c: giữ nguyên; phần lời dư chảy sang shot giãn được kế tiếp.
 - phần chảy không được rơi vào tấm im lặng: shot đứng trước tấm phải chứa hết lời của nó (+0,4 s), giãn cả khi vượt trần loại."""
import json, sys
from pathlib import Path
H = Path(__file__).resolve().parent; EP = H.parents[1] / 'channel-k2/k2c-t3-01'
T = json.loads((EP / 'vay-ham/treatment.json').read_text())['shots']; KC = {s['id']: s for s in json.loads((EP / 'g1/kiem-chu.json').read_text())['shots']}
CAP = {'thẻ số': 8, 'ảnh': 12, 'tranh Ken Burns': 12, 'bản đồ chiến lược': 8, 'bản đồ lịch sử': 12}; FIX = {'0c'}; PAD = 0.4   # 0c cố định 3 s (NC-H2); 4g (3D, giữ phần chảy của SM3) được giãn
L = float(sys.argv[1]); nhan = sys.argv[2] if len(sys.argv) > 2 else f'{L:.0f}'
TU = sum(KC[s['id']]['tu'] for s in T)
def loai(s):
    if KC[s['id']]['im_lang']: return 'im_lang'
    if s.get('neo') or s.get('moc_dinh') or s.get('cu') or s['id'] in FIX: return 'giu'
    if s['loai'].startswith('3D'): return 'gian'
    return 'tran'
TOL = 0.5   # lời được chảy ≤ 0,5 s sang shot kế (bảng hiện tại đã có chảy tới 5,2 s; kiem_loi cảnh báo > 1,5 s) — không chảy vào tấm im lặng
rows, carry = [], 0.0
for i, s in enumerate(T):
    k = loai(s); l = L * KC[s['id']]['tu'] / TU; d0 = s['dur']; c_in = carry
    ke_im = i + 1 < len(T) and loai(T[i + 1]) == 'im_lang'; tol = 0.0 if (ke_im or i + 1 == len(T)) else TOL   # shot cuối: không chảy ra ngoài phim
    het = l + c_in                                   # lời (gồm phần chảy từ shot trước) tính từ đầu shot
    if k == 'im_lang': d1, carry = d0, 0.0
    elif het == 0 or het + PAD <= d0: d1, carry = d0, 0.0
    elif het - d0 <= tol: d1, carry = d0, max(0.0, het - d0)                       # chảy nhẹ, không giãn
    elif k == 'gian': d1, carry = het + PAD, 0.0
    elif k == 'tran': d1 = max(d0, min(het + PAD, CAP.get(s['loai'], 99))); carry = max(0.0, het - d1)
    else: d1, carry = d0, max(0.0, het - d0)                                       # giu: khung neo / mốc đinh / cú liên hoàn / 0c / 4g
    rows.append(dict(id=s['id'], ch=s['ch'], loai=s['loai'], kieu=k, may=(s.get('may') or '')[:60], dur=d0, loi=round(l, 2), chay_vao=round(c_in, 2), dur_moi=d1, chay_sang=round(carry, 2)))
    if ke_im and carry > 0:          # không để lời rơi vào tấm im lặng: giãn chính shot đứng trước tấm (kể cả khi vượt trần loại) và ghi chú
        rows[i]['dur_moi'] += carry + PAD; rows[i]['truoc_tam_im_lang'] = round(carry + PAD, 2); rows[i]['chay_sang'] = 0.0; carry = 0.0
for r in rows: r['dur_moi'] = round(r['dur_moi'] * 24 + 0.4999) / 24 if r['dur_moi'] > r['dur'] + 1e-9 else r['dur']   # làm tròn lên bậc khung hình 24 fps
for r in rows: r['them'] = round(r['dur_moi'] - r['dur'], 3)
t0, t1 = sum(r['dur'] for r in rows), sum(r['dur_moi'] for r in rows)
out = dict(L=L, nhan=nhan, tong_cu=round(t0, 3), tong_moi=round(t1, 3), them=round(t1 - t0, 3), du_cuoi=round(carry, 2),
           so_shot_gian=sum(1 for r in rows if r['them'] > 0), gian=[r for r in rows if r['them'] > 0], tat_ca=rows)
json.dump(out, open(H / f'gian-shot-{nhan}.json', 'w'), ensure_ascii=False, indent=1)
print(f"L={L} → tổng {t0:.1f} → {t1:.1f} s (+{t1 - t0:.1f}); {out['so_shot_gian']} shot giãn; dư cuối {carry:.2f}")
for r in out['gian']: print(f"  {r['id']:7} vào {r['chay_vao']:.1f} {r['loai']:16} {r['kieu']:5} {r['dur']:6.2f} → {r['dur_moi']:6.2f} (+{r['them']:.2f}) lời {r['loi']:.1f}{' (trước tấm im lặng)' if r.get('truoc_tam_im_lang') else ''}")
