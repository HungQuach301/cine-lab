#!/opt/cine/bin/python
"""KL42 · bước 4: nhịp thật → đề xuất bảng giãn shot (CHỈ ĐỌC vay-ham/treatment.json + g1/kiem-chu.json; KHÔNG sửa treatment.json).
- Lời từng shot/câu = mốc thật của bản thu G1 (alignment ElevenLabs, stem/moc.json), không ước theo số từ như GIỌNG-CHỐT §5.
- Thứ tự shot theo lời v4.2: ‹2o›, ‹2p› dời lên ngay sau ‹KA1782›, trước ‹2j› (treatment.json vẫn thứ tự cũ — G1b/V7 cập nhật).
- Luật giãn giữ như gian_shot.py (GIỌNG-CHỐT, chủ dự án duyệt khung): mỗi shot chứa lời của nó + 0,4 s (luật G1); lời chảy sang shot kế ≤ 0,5 s,
  không chảy vào tấm im lặng, không chảy ra ngoài shot cuối; giãn được = 3D không phải khung neo/mốc đinh/cú liên hoàn/0c; thẻ/ảnh/tranh/bản đồ
  giãn tới trần loại (thẻ số 8 · ảnh, tranh, bản đồ lịch sử 12 · bản đồ chiến lược 8), phần vượt chảy sang shot giãn được kế tiếp; không giãn tấm
  im lặng; không cắt lời; không rút shot đang dư; làm tròn lên bậc khung hình 24 fps.
  Khác gian_shot.py: khi lời chảy sang shot kế, lời shot kế bắt đầu sau phần chảy + 0,4 s (giữ khoảng ngừng tối thiểu giữa hai đoạn).
  'footage' (2p) không có trần trong fit_khoa.py → coi như trần 12 s (như ảnh) — ghi rõ trong bảng.
Phương án: A = chỉ giãn; B = A + rút phần dư (rut()) tới ≤ 745 s; C102/C103 = kéo nhịp lời ×1,02/×1,03 sau thu (chỉ để so).
→ nhip-that.json (mốc câu/shot theo bản thu + vị trí lời trên trục phim theo phương án chọn, mặc định A) + in bảng. Dùng: nhip.py [A|B|C102|C103]"""
import json
import kl_lib as K
EP = K.EP; T0 = json.loads((EP / 'vay-ham/treatment.json').read_text())['shots']; KC = {s['id']: s for s in json.loads((EP / 'g1/kiem-chu.json').read_text())['shots']}
CAP = {'thẻ số': 8, 'ảnh': 12, 'tranh Ken Burns': 12, 'bản đồ chiến lược': 8, 'bản đồ lịch sử': 12, 'footage': 12}; FIX = {'0c'}; PAD, TOL = 0.4, 0.5
M = json.loads((K.OUT / 'stem/moc.json').read_text())
ids = [s['id'] for s in T0]; blk = ids[ids.index('2o'):ids.index('2o') + 2]; assert blk == ['2o', '2p']
ids = [i for i in ids if i not in blk]; j = ids.index('2j'); assert ids[j - 1] == 'KA1782'; ids = ids[:j] + blk + ids[j:]
TS = {s['id']: s for s in T0}; T = [TS[i] for i in ids]
D = {d['shot']: dict(d, chuong=c['chuong']) for c in M['chuong'] for d in c['doan']}
loi_ids = [d['shot'] for c in M['chuong'] for d in c['doan']]
assert [i for i in ids if i in D] == loi_ids, 'thứ tự shot có lời ≠ thứ tự lời v4.2'
assert all((i in D) == (KC[i]['tu'] > 0) for i in ids)


def loai(s):
    if KC[s['id']]['im_lang']: return 'im_lang'
    if s.get('neo') or s.get('moc_dinh') or s.get('cu') or s['id'] in FIX: return 'giu'
    return 'gian' if s['loai'].startswith('3D') else 'tran'


def plan(keo=1.0):
    rows, carry = [], 0.0
    for i, s in enumerate(T):
        k = loai(s); d = D.get(s['id']); l = (d['kt'] - d['bd']) / keo if d else 0.0; d0 = s['dur']; c_in = carry
        ke_im = i + 1 < len(T) and loai(T[i + 1]) == 'im_lang'; tol = 0.0 if (ke_im or i + 1 == len(T)) else TOL
        het = l + c_in                                   # mốc hết lời (gồm phần chảy vào) tính từ đầu shot
        if k == 'im_lang' or (l == 0 and c_in == 0): d1 = d0
        elif het + PAD <= d0 or het - d0 <= tol: d1 = d0                                  # vừa, hoặc chảy nhẹ ≤ 0,5 s
        elif k == 'gian': d1 = het + PAD
        elif k == 'tran': d1 = max(d0, min(het + PAD, CAP.get(s['loai'], 99)))
        else: d1 = d0                                                                      # giu: khung neo / mốc đinh / cú liên hoàn / 0c
        r = dict(id=s['id'], ch=s['ch'], loai=s['loai'], kieu=k, may=(s.get('may') or '')[:70], dur=d0, loi=round(l, 3), chay_vao=round(c_in, 3), dur_moi=d1)
        if k != 'im_lang' and het > 0 and ke_im and het + PAD > d1: r['truoc_tam_im_lang'] = round(het + PAD - d1, 3); r['dur_moi'] = d1 = het + PAD
        if k != 'im_lang' and het > 0 and i + 1 == len(T) and het + PAD > d1: r['dur_moi'] = d1 = het + PAD
        r['chay_sang'] = round(max(0.0, het - d1), 3) if k != 'im_lang' else 0.0
        rows.append(r); carry = max(0.0, het + PAD - d1) if (k != 'im_lang' and het > 0) else 0.0   # lời shot kế bắt đầu sau lời shot này + 0,4 s
    return rows


def rut(rows, dich, min_dur=4.0):
    """Phương án B: TRẦN ĐUÔI — mỗi shot giãn được/thẻ-ảnh-bản đồ có lời (không đụng tấm im lặng, khung neo, mốc đinh, cú liên hoàn, 0c) giữ tối đa X s
    hình sau lời (đuôi = dur − phần chảy vào − lời), X là giá trị lớn nhất (bậc 0,01 s) cho tổng ≤ dich; không dưới 1,2 s (= 0,4 s luật G1 + 0,8 s), shot ≥ min_dur.
    Shot có đuôi < X không đổi. Bậc 1/24 s (làm tròn lên)."""
    ung = [r for r in rows if r['kieu'] in ('gian', 'tran') and r['loi'] > 0]
    def ap(X):
        return {r['id']: max(math.ceil(max(r['chay_vao'] + r['loi'] + X, min_dur) * 24 - 1e-6) / 24, 0) for r in ung if r['dur_moi'] - r['chay_vao'] - r['loi'] > X}
    tong0 = sum(r['dur_moi'] for r in rows); X = 6.0
    while X > 1.2:
        new = ap(X); tong = tong0 - sum(r['dur_moi'] - new[r['id']] for r in ung if r['id'] in new and new[r['id']] < r['dur_moi'])
        if tong <= dich: break
        X = round(X - 0.01, 2)
    for r in ung:
        if r['id'] in new and new[r['id']] < r['dur_moi']: r['rut'] = round(r['dur_moi'] - new[r['id']], 4); r['dur_moi'] = new[r['id']]
    rows[0]['tran_duoi_X'] = X
    return rows


def tron(rows):
    for r in rows: r['dur_moi'] = round(r['dur_moi'] * 24 + 0.4999) / 24 if r['dur_moi'] > r['dur'] + 1e-9 else r['dur']
    return rows


import math, sys   # noqa: E402
PA = {'A': plan(), 'C102': plan(1.02), 'C103': plan(1.03)}
for k in PA: tron(PA[k])
PA['B'] = rut(tron(plan()), 745.0)
CHON = sys.argv[1] if len(sys.argv) > 1 else 'A'
rows = PA[CHON]
TOM = {k: dict(tong=round(sum(r['dur_moi'] for r in v), 3), them=round(sum(r['dur_moi'] - r['dur'] for r in v), 3), shot_gian=sum(r['dur_moi'] > r['dur'] + 1e-9 for r in v),
               shot_rut=[(r['id'], r['rut']) for r in v if r.get('rut')], tran_duoi=v[0].get('tran_duoi_X')) for k, v in PA.items()}
t = 0.0
for r in rows:
    r['them'] = round(r['dur_moi'] - r['dur'], 4); r['bd_phim'] = round(t, 3); d = D.get(r['id'])
    if d:
        a = t + r['chay_vao']; r['loi_bd_phim'] = round(a, 3); r['loi_kt_phim'] = round(a + r['loi'], 3)
        r['cau'] = [dict(khoa=c['khoa'], bd_phim=round(a + c['bd'] - d['bd'], 3), kt_phim=round(a + c['kt'] - d['bd'], 3), bd_chuong=c['bd'], kt_chuong=c['kt']) for c in d['cau']]
        r['ban_thu'] = dict(chuong=d['chuong'], bd_chuong=d['bd'], kt_chuong=d['kt'], bd_stem=d['bd_stem'], kt_stem=d['kt_stem'])
    t += r['dur_moi']; r['kt_phim'] = round(t, 3)
t0, t1 = sum(r['dur'] for r in rows), sum(r['dur_moi'] for r in rows)
# kiểm: lời không đè nhau, không rơi vào tấm im lặng, không ra ngoài phim
L = [r for r in rows if 'loi_bd_phim' in r]
chong = [(a['id'], b['id'], round(b['loi_bd_phim'] - a['loi_kt_phim'], 3)) for a, b in zip(L, L[1:]) if b['loi_bd_phim'] - a['loi_kt_phim'] < PAD - 2e-3]
im = [(r['id'], x['id']) for r in L for x in rows if x['kieu'] == 'im_lang' and r['loi_kt_phim'] > x['bd_phim'] + 1e-6 and r['loi_bd_phim'] < x['kt_phim']]
tong_loi = sum(r['loi'] for r in L)
CH = {}
for r in rows: c = CH.setdefault(r['ch'], dict(cu=0.0, moi=0.0, shot_gian=0)); c['cu'] += r['dur']; c['moi'] += r['dur_moi']; c['shot_gian'] += r['them'] > 0
out = dict(ghi=__doc__.split('\n')[0], phuong_an_chon=CHON, phuong_an=TOM, thu_tu_v42=ids, tong_cu=round(t0, 3), tong_moi=round(t1, 3), them=round(t1 - t0, 3), so_shot_gian=sum(r['them'] > 0 for r in rows),
           tong_loi_shot=round(tong_loi, 3), stem_giay=M['giay_stem'], chuong={k: {kk: round(vv, 3) for kk, vv in v.items()} for k, v in CH.items()},
           kiem=dict(loi_cach_duoi_04s=chong, loi_vao_tam_im_lang=im, du_cuoi=rows[-1]['chay_sang']), shot=rows)
json.dump(out, open(K.H / 'nhip-that.json', 'w'), ensure_ascii=False, indent=1)
print(f"phim {t0:.3f} → {t1:.3f} s (+{t1 - t0:.3f}); {out['so_shot_gian']} shot giãn; tổng lời (theo shot) {tong_loi:.1f} s; stem {M['giay_stem']} s; kiểm {out['kiem']}")
for r in rows:
    if r['them'] != 0: print(f"  {r['id']:7} {r['loai']:18} {r['kieu']:5} vào {r['chay_vao']:.2f} lời {r['loi']:.2f}  {r['dur']:.3f} → {r['dur_moi']:.3f} (+{r['them']:.3f}){' trước tấm im lặng' if r.get('truoc_tam_im_lang') else ''}")
print({k: (round(v['cu'], 2), round(v['moi'], 2), v['shot_gian']) for k, v in CH.items()}); print(json.dumps(TOM, ensure_ascii=False))
