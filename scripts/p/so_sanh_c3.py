"""Phiên P — so kết quả C3 THEO SHOT giữa hai lần chạy luật (vd. layout-v15 và layout-v16).
Dùng: python3 scripts/p/so_sanh_c3.py v15 v16   → in shot đổi kết quả + tổng; ghi reports/checks/layout-<mới>/so-sanh-C3-theo-shot.json
Kết quả shot: TRƯỢT nếu có mẫu "trượt chắc chắn"; KCM nếu có mẫu "không chứng minh được"; ĐẠT nếu mọi mẫu đạt.
Shot không có mẫu đo được không có trong bảng (luật ghi "cần người xem").
Lưu ý (29/09/2026): export_c3.js xuất MỘT nhân vật mỗi khung (Ida) → C3 hiện chỉ đo Ida (sheet ida.json)."""
import json, subprocess, sys, os
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
cu, moi = sys.argv[1], sys.argv[2]
EV = json.loads(subprocess.run(['node', os.path.join(REPO, 'design/cong5/layout/render_film.js'), '--events', '--out', '/tmp'], capture_output=True, text=True, check=True).stdout)
bounds, t = [], 0.0
for sid, dur, _ in EV['ORDER']:
    f0 = round(t * 24); t += dur; bounds.append((sid, f0, round(t * 24) - 1))
shot = lambda f: next((s for s, a, b in bounds if a <= f <= b), None)
def per(v):
    d = json.load(open(os.path.join(REPO, f'reports/checks/layout-{v}/layout-{v}.checks.json')))
    c = [r for r in d['results'] if r['code'] == 'C3'][0]; out = {}
    for m in c['evidence']['do']:
        o = out.setdefault(shot(m['khung']), [0, 0, 0, 0.0]); k = m['ket_qua']
        o[0 if k.startswith('đạt') else 1 if k.startswith('trượt') else 2] += 1; o[3] = max(o[3], abs(m['lech_pct']))
    return out
vd = lambda o: '—' if o is None else ('TRƯỢT' if o[1] else 'KCM' if o[2] else 'ĐẠT')
A, B = per(cu), per(moi)
rows = [[s, vd(A.get(s)), vd(B.get(s)), A.get(s), B.get(s)] for s, _, _ in bounds if s in A or s in B]
for r in rows:
    if r[1] != r[2]: print('ĐỔI', r[0], r[1], '→', r[2])
tot = lambda o: [sum(v[i] for v in o.values()) for i in range(3)]
print('mẫu đạt/trượt chắc/KCM:', cu, tot(A), '|', moi, tot(B))
json.dump({'rows': rows, 'tot_' + cu: tot(A), 'tot_' + moi: tot(B)}, open(os.path.join(REPO, f'reports/checks/layout-{moi}/so-sanh-C3-theo-shot.json'), 'w'), ensure_ascii=False, indent=1)
