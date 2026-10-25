#!/opt/cine/bin/python
"""ANIMATIC-T4-V2 · việc 1 — LỜI v3: áp reports/nc-t4/loi-moi-nhap.json (P5 "theo khuyến nghị": N0a, N0b, N1, N2, N3, N9 mới; N4, N5, N6 sửa; N7 bỏ câu Churchill)
lên lời DỰNG v2 (K1-C1 — animatic/loi-dung-moc.json: 115 câu dùng, 7 câu bỏ) và THU G1 chỉ các câu mới/sửa, đúng thiết lập GIONG-T4 (gl_lib: VDLncRBHDjLHBqLhQ1Qt,
eleven_multilingual_v2, stability 0,5 · similarity 0,75 · speed 1,03, seed 19102026, alias theo từ điển khoa-loi/phat-am/london-g1.pls = tu-dien.json).
Mỗi câu gửi kèm previous_text/next_text là lời v3 liền trước/sau trong chương (≤ 900 ký tự mỗi bên — ngữ cảnh không tính phí, KL42).
Sổ AI riêng phiên: reports/animatic-t4-v2/so-ai-giong.jsonl; bộ đếm: bo-dem-giong.jsonl; chặn 2 500 ký tự gửi (mốc 1 500).
ASR 2 cách nghe (medium.en beam 5 · small.en beam 1) trên từng câu thu → so từng từ (chuẩn hoá) + số/năm + tên (gl_kiem_tap.kiem_cau).
  gl_thu_v3.py van   → in lời v3 + loi-khoa-v3.txt + LOI-KHOA-v3.sha256 + reports/animatic-t4-v2/SO-LOI-V2-V3.md (không gọi API)
  gl_thu_v3.py thu   → thu + ASR → reports/animatic-t4-v2/giong-v3.json"""
import hashlib, json, re, sys, difflib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gl_lib as K
R = K.R; EP = K.EP; RP = R / 'reports/animatic-t4-v2'; RP.mkdir(parents=True, exist_ok=True)
K.LOG, K.BODEM = RP / 'so-ai-giong.jsonl', RP / 'bo-dem-giong.jsonl'; K.CHAN, K.MOC = 2500, 1500
MOC = json.loads((EP / 'animatic/loi-dung-moc.json').read_text())
NM = {c['ma']: c for c in json.loads((R / 'reports/nc-t4/loi-moi-nhap.json').read_text())['cau']}
CH = {'M': '00 HOOK', 'H1': '01 FIRE', 'H2': '02 REBUILD', 'H3': '03 DOME', 'H4': '04 BLITZ', 'H5': '05 TODAY'}
# thao tác: (mã N, kiểu, nhóm, câu neo (đầu chữ khoá v2)) — 'sau' = chèn sau câu neo · 'thay' = thay câu neo · 'bo' = bỏ câu neo · 'dau' = nhóm mới trước nhóm neo
OP = [('N0a', 'dau', 'M00', None), ('N0b', 'dau', 'M00', None),
      ('N2', 'sau', 'H1-06', 'People will not obey me'), ('N1', 'sau', 'H1-13', 'The fire climbs Ludgate Hill'), ('N3', 'sau', 'H1-15', 'At the Navy Office'),
      ('N9', 'sau', 'H2-06', 'Two hundred and two feet'), ('N4', 'thay', 'H2-10', 'The last stone of the lantern'), ('N5', 'thay', 'H3-02', 'On London Bridge, the houses'),
      ('N6', 'thay', 'H3-03', 'Between 1864 and 1870'), ('N7', 'bo', 'H4-04', 'Winston Churchill reportedly')]


def v3():
    """→ danh sách câu v3 theo thứ tự: {nhom, L, khoa, nguon: 'v2'|'moi'|'sua', N, v2_bd, v2_kt}"""
    out = [dict(nhom='M00', L=None, khoa=NM[n]['en'], nguon='moi', N=n) for n in ('N0a', 'N0b')]
    for c in MOC['cau']:
        if c['bo']: continue
        row = dict(nhom=c['nhom'], L=c['L'], khoa=c['khoa'], nguon='v2', N=None, v2_bd=c['bd'], v2_kt=c['kt'])
        hit = [o for o in OP if o[2] == c['nhom'] and o[3] and c['khoa'].startswith(o[3])]
        if hit and hit[0][1] == 'bo':
            assert c['khoa'] == NM['N7']['cu'], c['khoa']; continue
        if hit and hit[0][1] == 'thay':
            assert c['khoa'] == NM[hit[0][0]]['cu'], (c['khoa'], NM[hit[0][0]]['cu'])
            row.update(khoa=NM[hit[0][0]]['en'], nguon='sua', N=hit[0][0], cu=c['khoa'])
        out.append(row)
        if hit and hit[0][1] == 'sau': out.append(dict(nhom=c['nhom'], L=None, khoa=NM[hit[0][0]]['en'], nguon='moi', N=hit[0][0]))
    assert sorted(x['N'] for x in out if x['N']) == sorted(n for n in NM if n != 'N7'), 'thiếu câu N'
    return out


def chuong(nhom): return CH['M' if nhom.startswith('M') else nhom[:2]]


def van():
    C = v3(); txt, cur_ch, cur_g = [], None, None
    for c in C:
        ch = chuong(c['nhom'])
        if ch != cur_ch: txt += ['', f'[{ch}]']; cur_ch = ch; cur_g = None
        if c['nhom'] != cur_g: txt += ['', c['khoa']]; cur_g = c['nhom']
        else: txt[-1] += ' ' + c['khoa']
    out = '\n'.join(txt).strip() + '\n'
    (EP / 'loi-khoa-v3.txt').write_text(out)
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    tep = ['loi-khoa-v3.txt', 'khoa-loi/phat-am/london-g1.pls', 'loi-khoa.txt']
    (EP / 'LOI-KHOA-v3.sha256').write_text(''.join(f'{sha(EP / n)}  {n}\n' for n in tep))
    body = ' '.join(c['khoa'] for c in C); v2 = ' '.join(c['khoa'] for c in MOC['cau'] if not c['bo'])
    tu = lambda s: len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’\-]*", s))
    md = ['# SO LỜI v2 ↔ v3 — K2C-T4-02 London (ANIMATIC-T4-V2, 25/10/2026)', '',
          '> v2 = lời DỰNG của animatic v1 (K1-C1: `loi-khoa.txt` 645c0211… trừ 7 câu bỏ L81, L41b, L45, L38, L77, L15, L54 — `animatic/loi-dung-moc.json`). v3 = `loi-khoa-v3.txt` (lời ĐỌC trong animatic v3).',
          '> Căn cứ: chủ dự án 25/10/2026 09:15 (giờ Asia/Saigon) "Duyệt gói 50 % tiết kiệm + P1–P10 theo khuyến nghị" → P4 bỏ câu Churchill, P5 lời theo `reports/nc-t4/loi-moi-nhap.json`. Sinh bằng `scripts/k2ldn/giong/gl_thu_v3.py van`.', '',
          '| Mã | Kiểu | Nhóm (shot v2) | v2 | v3 | Ký tự thu | Nguồn |', '|---|---|---|---|---|---|---|']
    for n, k, g, _ in OP:
        x = NM[n]; kieu = {'dau': 'mới (mở lạnh)', 'sau': 'mới', 'thay': 'sửa', 'bo': 'bỏ'}[k]
        md.append(f"| {n} | {kieu} | {g} | {x.get('cu') or '—'} | {x['en'] or '— (bỏ)'} | {len(x['en'])} | {x['nguon']} |")
    md += ['', f"- v2: {sum(1 for c in MOC['cau'] if not c['bo'])} câu · {tu(v2)} từ · {len(v2)} ký tự. v3: {len(C)} câu · {tu(body)} từ · {len(body)} ký tự.",
           f"- Ký tự cần thu (câu mới + câu sửa thu lại cả câu): {sum(len(NM[n]['en']) for n, k, _, _ in OP if k != 'bo')}.", '']
    (RP / 'SO-LOI-V2-V3.md').write_text('\n'.join(md) + '\n')
    print(out[:400]); print((EP / 'LOI-KHOA-v3.sha256').read_text()); print(md[-3]); print(md[-2])
    return C


def chuan_tu(s):
    s = s.lower().replace('’', "'"); s = re.sub(r'[“”"—–,.:;!?()]', ' ', s); return [w for w in s.split() if w]


def thu(chi=None, seed=K.SEED):
    import gl_kiem_tap as KT
    C = v3(); res = []; c0 = K.counter(); gui_tong = 0
    for i, c in enumerate(C):
        if c['nguon'] == 'v2' or (chi and c['N'] not in chi): continue
        ch = chuong(c['nhom']); cung = [x for x in C if chuong(x['nhom']) == ch]; j = cung.index(c)
        prev = K.alias(' '.join(x['khoa'] for x in cung[:j]))[-900:] or None; nxt = K.alias(' '.join(x['khoa'] for x in cung[j + 1:]))[:900] or None
        gui = K.alias(c['khoa'])
        mp3, al, n = K.tts(gui, f"v3 {c['N']} {c['nhom']}" + (f' seed {seed}' if seed != K.SEED else ''), prev, nxt, seed=seed); gui_tong += n
        assert ''.join(al['characters']) == gui
        nghe = {}
        for name, beam in KT.KL.NGHE:
            ws = KT.asr_cache(mp3, name, beam); h = KT.chuan(' '.join(w['w'].strip() for w in ws))
            a, b = chuan_tu(c['khoa']), chuan_tu(h); sm = difflib.SequenceMatcher(None, a, b)
            lech = [(' '.join(a[i1:i2]), ' '.join(b[j1:j2])) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != 'equal']
            nghe[name] = dict(asr=h, tu_dung=round(sum(bl.size for bl in sm.get_matching_blocks()) / len(a), 4), cho_lech=lech, **KT.kiem_cau(c['khoa'], h))
        res.append(dict(seed=seed, N=c['N'], nhom=c['nhom'], khoa=c['khoa'], gui=gui, tep=mp3, sha256=hashlib.sha256(Path(mp3).read_bytes()).hexdigest(), ky_tu=n, giay=round(K.dur(mp3), 3),
                        bd=round(al['character_start_times_seconds'][0], 3), kt=round(al['character_end_times_seconds'][-1], 3), nghe=nghe))
        print(c['N'], n, res[-1]['giay'], {k: (v['tu_dung'], v['so_sai'], v['ten_sai'], v['cho_lech']) for k, v in nghe.items()}, flush=True)
    bd = K.ghi_bodem('ANIMATIC-T4-V2 lời v3' + (f' thu lại {chi} seed {seed}' if chi else ''), gui_tong, c0, K.counter(90)) if gui_tong else None
    P = RP / 'giong-v3.json'; old = json.loads(P.read_text()) if P.exists() else dict(cau=[], bo_dem=[])
    if isinstance(old.get('bo_dem'), dict): old['bo_dem'] = [old['bo_dem']]
    P.write_text(json.dumps(dict(thiet_lap=dict(voice=K.G1, model=K.MODEL, settings=K.SET, seed_goc=K.SEED, tu_dien='khoa-loi/phat-am/london-g1.pls (alias trong chữ gửi)'),
                                 cau=old['cau'] + res, bo_dem=old['bo_dem'] + ([bd] if bd else []), tong_gui_phien=K.da_gui()), ensure_ascii=False, indent=1))
    print('bộ đếm', bd, 'tổng gửi', K.da_gui())


if __name__ == '__main__':
    if sys.argv[1] == 'van': van()
    elif sys.argv[1] == 'thu': thu()
    elif sys.argv[1] == 'thu_lai': thu(sys.argv[3].split(','), int(sys.argv[2]))
