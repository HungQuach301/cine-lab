"""NC-T4: ước tỷ lệ lớp sau khi chèn điểm nhấn vào animatic v1 (log-shot.json của ANIMATIC-T4 @393c3b55).
Dùng: python -I bo_tri.py <log-shot.json> <ke-hoach.json> <ra.json>
Mỗi thao tác trong ke-hoach: {"dn","shot","loai": "tach"|"them"|"doi"|"chong"|"rut"|"xoa_loi", "lop", "s", "goc_mat"?, "ghi"}
 - tach: lấy s giây khỏi shot 3D (giảm A và góc của shot), thêm s giây lớp `lop` (thời lượng tổng không đổi)
 - them: thêm shot mới s giây lớp `lop` (thời lượng tăng s); `goc` của shot mới = "cao" nếu lop == "A_cao"
 - doi: thay nội dung clip M-d cùng độ dài (không đổi %; chỉ tính chi phí sinh lại)
 - chong: lớp chồng góc khung s giây (TL/KHAC/THE/THAT_CHONG), không đổi thời lượng hay góc
 - rut: bớt s giây khỏi shot (thời lượng giảm)
 - xoa_loi: bớt s giây do bỏ câu lời (thời lượng giảm, lấy ở shot ghi)
 - bo_n2p: bỏ s giây tấm nền N2+ (shot đổi sang cú máy chuyển động; 3D giữ nguyên)
"""
import json, sys, collections
L = json.load(open(sys.argv[1])); K = json.load(open(sys.argv[2]))
dur = {x['ma']: x['dur'] for x in L}; goc = {x['ma']: x['goc'] for x in L}
T0 = sum(dur.values()); PP = sum(x['dur'] for x in L if x['cu_may'] == 'PP')
lop = collections.Counter()
for x in L:
    for k, v in x['lop'].items(): lop[k] += v
g = collections.Counter()
for x in L: g[x['goc']] += x['dur']
T = T0; md_moi = 0.0; md_doi = 0.0; cat_them = 0
for a in K['thao_tac']:
    s = a['s']; t = a['loai']
    if t == 'tach':
        g[goc[a['shot']]] -= s; lop['A'] -= s; lop[a['lop']] += s
        g['md' if a['lop'] == 'MD' else 'that' if a['lop'].startswith('THAT') else 'khac'] += s
        cat_them += 1
        if a['lop'] == 'MD': md_moi += s
    elif t == 'them':
        T += s; lop['A' if a['lop'] in ('A_cao', 'A_thap') else a['lop']] += s
        g['cao' if a['lop'] == 'A_cao' else 'thap' if a['lop'] == 'A_thap' else 'md' if a['lop'] == 'MD' else 'that' if a['lop'].startswith('THAT') else 'khac'] += s
        if a.get('cat', 1): cat_them += 1
        if a['lop'] == 'MD': md_moi += s
    elif t == 'doi':
        md_doi += s
    elif t == 'chong':
        lop[a['lop']] += s
    elif t == 'bo_n2p':
        lop['N2P'] -= s
    elif t in ('rut', 'xoa_loi'):
        T -= s; g[goc[a['shot']]] -= s; lop['A'] -= s
than = T - PP
tl = lop['TL'] + lop['KHAC'] + lop['THE'] + lop['THAT'] + lop['THAT_CHONG']
c = K['chi_phi']
nhap = (md_moi + md_doi) * c['nhap_360p_usd_s'] * c['luot_nhap_toi_da']
cuoi = lop['MD'] * c['cuoi_720p_usd_s'] * (1 + c['ty_le_lam_lai_720p'])
r = {
  'tong_s': round(T, 3), 'than_phim_s': round(than, 3), 'phut': f"{int(T//60)}:{T%60:04.1f}",
  'md_s': round(lop['MD'], 3), 'md_pct': round(lop['MD'] / T * 100, 2),
  'goc_cao_s': round(g['cao'], 3), 'goc_cao_pct_than': round(g['cao'] / than * 100, 2),
  'thap_pct': round(g['thap'] / T * 100, 2),
  'n2p_pct': round(lop['N2P'] / T * 100, 2),
  'ai_pct': round((lop['MD'] + lop['N2P']) / T * 100, 2),
  'tu_lieu_cu_pct (TL+KHAC+THE, trần 10)': round((lop['TL'] + lop['KHAC'] + lop['THE']) / T * 100, 2),
  'that_pct (ảnh/footage thật)': round((lop['THAT'] + lop['THAT_CHONG']) / T * 100, 2),
  'tu_lieu_tong_pct (đề xuất trần 15)': round(tl / T * 100, 2),
  'ban_do_pct': round((lop['MAP'] + lop['MAP3D']) / T * 100, 2),
  'md_moi_s': md_moi, 'md_doi_s': md_doi, 'cat_them': cat_them,
  'cat_phut_uoc': round((K['cat_hien'] + cat_them) / (T / 60), 2),
  'gemini_nhap_usd_toi_da': round(nhap, 2), 'gemini_cuoi_usd': round(cuoi, 2),
  'gemini_t4_tong_usd': round(c['da_tieu_usd'] + nhap + cuoi, 2),
  'lop_s': {k: round(v, 3) for k, v in lop.items()},
}
json.dump(r, open(sys.argv[3], 'w'), ensure_ascii=False, indent=1); print(json.dumps(r, ensure_ascii=False, indent=1))
