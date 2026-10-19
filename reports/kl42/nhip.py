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
→ nhip-that.json (mốc câu/shot theo bản thu + vị trí lời trên trục phim đề xuất) + in bảng."""
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


rows, carry = [], 0.0
for i, s in enumerate(T):
    k = loai(s); d = D.get(s['id']); l = (d['kt'] - d['bd']) if d else 0.0; d0 = s['dur']; c_in = carry
    ke_im = i + 1 < len(T) and loai(T[i + 1]) == 'im_lang'; tol = 0.0 if (ke_im or i + 1 == len(T)) else TOL
    het = l + c_in
    if k == 'im_lang' or l == 0: d1, ov = d0, max(0.0, c_in - d0)
    elif het + PAD <= d0: d1, ov = d0, 0.0
    elif het - d0 <= tol: d1, ov = d0, het - d0
    elif k == 'gian': d1, ov = het + PAD, 0.0
    elif k == 'tran': d1 = max(d0, min(het + PAD, CAP.get(s['loai'], 99))); ov = max(0.0, het - d1)
    else: d1, ov = d0, max(0.0, het - d0)
    r = dict(id=s['id'], ch=s['ch'], loai=s['loai'], kieu=k, may=(s.get('may') or '')[:70], dur=d0, loi=round(l, 3), chay_vao=round(c_in, 3), dur_moi=d1, chay_sang=round(ov, 3))
    if ke_im and ov > 0: r['dur_moi'] += ov + PAD; r['truoc_tam_im_lang'] = round(ov + PAD, 3); r['chay_sang'] = 0.0; ov = 0.0
    rows.append(r); carry = ov + PAD if ov > 0 else 0.0
for r in rows: r['dur_moi'] = round(r['dur_moi'] * 24 + 0.4999) / 24 if r['dur_moi'] > r['dur'] + 1e-9 else r['dur']
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
chong = [(a['id'], b['id'], round(b['loi_bd_phim'] - a['loi_kt_phim'], 3)) for a, b in zip(L, L[1:]) if b['loi_bd_phim'] - a['loi_kt_phim'] < PAD - 1e-6]
im = [(r['id'], x['id']) for r in L for x in rows if x['kieu'] == 'im_lang' and r['loi_kt_phim'] > x['bd_phim'] + 1e-6 and r['loi_bd_phim'] < x['kt_phim']]
tong_loi = sum(r['loi'] for r in L)
CH = {}
for r in rows: c = CH.setdefault(r['ch'], dict(cu=0.0, moi=0.0, shot_gian=0)); c['cu'] += r['dur']; c['moi'] += r['dur_moi']; c['shot_gian'] += r['them'] > 0
out = dict(ghi=__doc__.split('\n')[0], thu_tu_v42=ids, tong_cu=round(t0, 3), tong_moi=round(t1, 3), them=round(t1 - t0, 3), so_shot_gian=sum(r['them'] > 0 for r in rows),
           tong_loi_shot=round(tong_loi, 3), stem_giay=M['giay_stem'], chuong={k: {kk: round(vv, 3) for kk, vv in v.items()} for k, v in CH.items()},
           kiem=dict(loi_cach_duoi_04s=chong, loi_vao_tam_im_lang=im, du_cuoi=round(carry, 3)), shot=rows)
json.dump(out, open(K.H / 'nhip-that.json', 'w'), ensure_ascii=False, indent=1)
print(f"phim {t0:.3f} → {t1:.3f} s (+{t1 - t0:.3f}); {out['so_shot_gian']} shot giãn; tổng lời (theo shot) {tong_loi:.1f} s; stem {M['giay_stem']} s; kiểm {out['kiem']}")
for r in rows:
    if r['them'] > 0: print(f"  {r['id']:7} {r['loai']:18} {r['kieu']:5} vào {r['chay_vao']:.2f} lời {r['loi']:.2f}  {r['dur']:.3f} → {r['dur_moi']:.3f} (+{r['them']:.3f}){' trước tấm im lặng' if r.get('truoc_tam_im_lang') else ''}")
print({k: (round(v['cu'], 2), round(v['moi'], 2), v['shot_gian']) for k, v in CH.items()})
