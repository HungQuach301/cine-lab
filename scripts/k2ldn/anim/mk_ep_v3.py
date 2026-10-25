#!/opt/cine/bin/python
"""ANIMATIC-T4-V2 (bản v3 của mk_ep.py) · việc 7 — khai cho k2check 1.17.6 chế độ animatic: channel-k2/k2c-t4-02/animatic2/{episode.yaml, log-shot.json, timeline.json, so-ai-*-t4.jsonl, log-may/}.
Nguồn: BANG-SHOT-v3.json, lời dựng v3 (animatic/loi-dung-moc-v3.json), ghep_v3 (THE/DEM/KHAC theo mốc câu). Shot TL (ảnh/tư liệu thật toàn khung) khai type tu_lieu + lop (THAT/KHAC).
Gốc: ANIMATIC-T4 · việc 8 — khai cho k2check 1.17.4 (Kinh thánh §13.6 "Cách khai T4", K1174 §5): channel-k2/k2c-t4-02/animatic/{episode.yaml, log-shot.json, timeline.json, so-ai-*-t4.jsonl, log-may/*.json}.
episode.yaml: kenh2_tu_t4, animatic, ngan_sach_gemini_usd 35 / moc 30 (chủ dự án 23/10/2026 23:45), so_ai_gemini (gộp sổ Gemini T4: tiền kỳ + LOOK-T4-V2 + phiên này, mỗi dòng `usd` thật),
so_ai / so_ai_openai (gộp OpenAI T4), sha_tu_lieu (licenses/SHA256-TU-LIEU.txt + -LOOK), goc_toa_do [532000, 180800], log_shot. Log shot từng shot: cu_may, log_may (log.json render_look.js,
giữ trong git — K1174-D4), tieu_diem_en, khop_voi/diem_neo/hoa_s, lo_ra, lop, ai_nen, minh_hoa, goc, tl, chuong. Timeline: một đoạn mỗi shot (cách mk_tl.py của K-1.17.2), speech = mốc câu lời dựng."""
import gzip, json, shutil
from pathlib import Path
import yaml
REPO = Path(__file__).resolve().parents[3]; EP = REPO / 'channel-k2/k2c-t4-02'; AN = EP / 'animatic2'; AN1 = EP / 'animatic'


def gop(paths, loc, ra):
    n = 0
    with open(ra, 'w') as f:
        for p in paths:
            if not p.exists(): continue
            for l in p.read_text().splitlines():
                if not l.strip(): continue
                r = json.loads(l)
                if loc(r): r.setdefault('so_goc', str(p.relative_to(REPO))); f.write(json.dumps(r, ensure_ascii=False) + '\n'); n += 1
    return n


def main():
    B = json.loads((EP / 'BANG-SHOT-v3.json').read_text()); M = json.loads((AN1 / 'loi-dung-moc-v3.json').read_text())
    for c in M['cau']: c.setdefault('bo', False)
    LG = AN / 'log-may'; LG.mkdir(exist_ok=True)
    for gz in LG.glob('*.json.gz'):   # log.json đầy đủ (không nén) — mỗi tệp < 1 MB; bản .gz cũ bỏ
        j = LG / gz.name[:-3]
        if not j.exists() or gz.stat().st_mtime > j.stat().st_mtime: j.write_bytes(gzip.decompress(gz.read_bytes()))   # shot dựng lại → log mới thay log cũ
        gz.unlink()
    for d in Path('/var/tmp/anim/r3').iterdir():
        if d.is_dir() and (AN / 'may' / f'{d.name}.json').exists() and (d / 'log.json').exists() and (not (LG / f'{d.name}.json').exists() or (d / 'log.json').stat().st_mtime > (LG / f'{d.name}.json').stat().st_mtime): shutil.copy(d / 'log.json', LG / f'{d.name}.json')
    for j in LG.glob('*.json'):   # MAY-19 đọc cam theo hệ cảnh (x = E − 532000, y = h, z = −(N − 180800); như log T3 và look2.js); bản [E, N, h] giữ ở cam_en
        L = json.loads(j.read_text())
        if L.get('he_toa_do') == 'canh': continue
        sc = lambda e: [round(e[0] - 532000, 3), round(e[2], 3), round(-(e[1] - 180800), 3)]
        for f in L['frames']: c = f['cam']; f['cam_en'] = dict(c); f['cam'] = dict(c, p=sc(c['p']), l=sc(c['l']))
        L['he_toa_do'] = 'canh'; L['goc_toa_do'] = [532000, 180800]; j.write_text(json.dumps(L))
    ls = []
    for r in B['shot']:
        x = {k: r[k] for k in ('ma', 't0', 't1', 'dur', 'chuong', 'goc', 'tl', 'cu_may', 'lop', 'ai_nen', 'minh_hoa', 'vai', 'tieu_diem_en', 'diem_may')}; x['shot'] = r['ma']
        x['thoi_gian'] = r['thoi_gian']; x['cau'] = [{'t': round(c['bd'] - r['t0'], 3), 'cau': c['khoa']} for c in M['cau'] if not c['bo'] and r['t0'] <= c['bd'] < r['t1']]
        if r['cu_may'] == 'KHOP':
            a, b = LG / f"{r['ma']}-a.json", LG / f"{r['ma']}-b.json"
            if a.exists() and b.exists():
                A, Bq = json.loads(a.read_text()), json.loads(b.read_text()); cut = r['thoi_gian'][3]; na = int(round((cut - 0.5) * 24))
                A['frames'] = A['frames'][:na] + [dict(f, f=na + i) for i, f in enumerate(Bq['frames'])]; (LG / f"{r['ma']}.json").write_text(json.dumps(A))
            x.update(khop_voi=r['khop_voi'], diem_neo=r['diem_neo'], hoa_s=r['hoa_s'])
        if r['cu_may'] == 'KEO': x['lo_ra'] = r['lo_ra']
        if (LG / f"{r['ma']}.json").exists(): x['log_may'] = f"log-may/{r['ma']}.json"
        if r['minh_hoa']: x['md_moc'] = r['md_moc']; x['ai_image'] = True
        if r['minh_hoa']:
            tg = (AN / 'omni/chon' / f"{r['ma']}.txt"); tag = tg.read_text().strip() if tg.exists() else r.get('md_clip')
            kp = (f"omni/kiem2/{tag}-kiem.json" if (AN / 'omni/kiem2' / f'{tag}-kiem.json').exists() else (f"omni/kiem-mat.json#{tag}" if tg.exists() else f"../animatic/omni/kiem2/{tag}-kiem.json")) if tag else None
            x['kiem'] = kp; x['muc_kiem'] = r.get('muc_kiem') if tg.exists() else 'v1 (2 tầng ANIMATIC-T4)'; x['nhan_vat_ten'] = r.get('nhan_vat_ten') or []
            if tag: x['minh_hoa'] = [{'ma': r['ma'], 't0': 0.0, 't1': r['dur'], 'luot': tag, 'kiem': kp, 'so_ai': 'so-ai-gemini-t4.jsonl'}]
            if x['nhan_vat_ten']:
                MC = json.loads((AN / 'omni/lenh/muc-luc.json').read_text()).get(r['ma'], {}); import hashlib
                x['chan_dung_tham_chieu'] = [{'tep': p_, 'sha256': hashlib.sha256((REPO / p_).read_bytes()).hexdigest()} for p_ in MC.get('tham_chieu', [])]
        if r['cu_may'] == 'TL':
            x['tu_lieu_toan_khung'] = {'anh': r['tl_anh'], 'lop': r['lop_tl'], 'chu': r['them']['chu'], 'chuyen_dong': '2D chậm (Ken Burns) — không AI chạm', 'ghi_cong': 'ghi-cong.json'}   # mục đoạn (K1172: kiem/so_ai/luot đọc ở mục đoạn)
        if r['ai_nen']:
            k = {'H5-05a': 'P9-2026-oai-l2'}.get(r['ma'])
            x['n2p'] = {'tam': [{'tag': k, 'kiem': f'../animatic/tam-nen/do/{k}-kiem.json', 'ghep': f'../animatic/tam-nen/do/{k}-ghep.json', 'v': f"tam-nen/do/{r['ma']}-v.json", 'khoang_s': r['them']['tam_nen']}]}
        x['tu_lieu_chong_sau_ai'] = False; x['ai_image'] = bool(r['minh_hoa']); x['noi'] = 'minh_hoa' if r['cu_may'] == 'MD' else r['diem_may']
        ls.append(x)
    (AN / 'log-shot.json').write_text(json.dumps(ls, ensure_ascii=False, indent=1))
    R = REPO / 'reports'
    ng = gop([R / 'tien-ky-t4/so-ai-gemini.jsonl', R / 'look-t4-v2/so-ai.jsonl', R / 'animatic-t4/so-ai-gemini.jsonl', R / 'animatic-t4-v2/so-ai-gemini.jsonl'], lambda r: 'gemini' in json.dumps(r.get('model_req', '') + str(r.get('nha', ''))).lower(), AN / 'so-ai-gemini-t4.jsonl')
    no = gop([R / 'tien-ky-t4/so-ai.jsonl', R / 'look-t4-v2/so-ai.jsonl', R / 'animatic-t4/so-ai.jsonl', R / 'animatic-t4-v2/so-ai.jsonl'], lambda r: r.get('nha') == 'openai', AN / 'so-ai-openai-t4.jsonl')
    sha = AN / 'sha-tu-lieu-t4.txt'; sha.write_text((EP / 'licenses/SHA256-TU-LIEU.txt').read_text() + (EP / 'licenses/SHA256-TU-LIEU-LOOK.txt').read_text() + (EP / 'nc/licenses/SHA256-NC.txt').read_text()
                   + ''.join(f"{json.loads(q.read_text())['tai']['sha256']}  {q.stem}  ({json.loads(q.read_text())['tai']['src']})\n" for q in sorted((AN / 'tu-lieu/giay-phep').glob('*.json'))))
    import importlib.util as IU
    spec = IU.spec_from_file_location('ghep_v3', str(Path(__file__).parent / 'ghep_v3.py')); G = IU.module_from_spec(spec); spec.loader.exec_module(G)
    NOI = {'P1': 'bo_nam_bankside', 'P2': 'cau_london', 'P3': 'thanh_pho_dong', 'P4': 'fleet_street', 'P4b': 'ludgate', 'P5': 'thanh_pho_bac', 'P6': 'song', 'P7': 'thien_dinh', 'P8': 'tower_hill', 'P9': 'bo_nam_bankside'}
    chon = {q.stem: q.read_text().strip() for q in (AN / 'omni/chon').glob('*.txt')}
    for r in B['shot']:
        if r['cu_may'] == 'MD' and r['ma'] not in chon and r.get('md_clip'): chon[r['ma']] = r['md_clip']
    G.THE, G.DEM = G.lich(B, M)
    ch_t0 = {}
    for r in B['shot']: ch_t0.setdefault(r['phan'], r['t0'])
    G.CHUONG = G.GH.CHUONG
    def cau1(r):   # câu lời trùng nhiều nhất với khoảng shot (đúng nguyên văn một câu)
        best, bo = None, 0.0
        for c in M['cau']:
            if c['bo']: continue
            ov = min(c['kt'], r['t1']) - max(c['bd'], r['t0'])
            if ov > bo: best, bo = c['khoa'], ov
        return best
    segs = []; nhip = []
    for r in B['shot']:
        tp = {'MD': 'minh_hoa', 'PP': 'card', 'TL': 'tu_lieu'}.get(r['cu_may'], 'scene3d')
        s = {'id': r['ma'], 'part': r['chuong'], 'chuong': r['chuong'], 'dur': r['dur'], 'fadeIn': 0, 'fadeOut': 0,
             'moc_loi': [{'t': round(c['bd'] - r['t0'], 3), 's': c['khoa'][:28]} for c in M['cau'] if not c['bo'] and r['t0'] <= c['bd'] < r['t1']],
             'shots': [{'at': 0, 'type': tp, 'tpl': 'plate', 'p': {'sach': True, 'tl': r['tl']}, 'cau': ' '.join(r['cau_loi'])[:300]}]}
        sh = s['shots'][0]; sh['noi'] = 'minh_hoa' if r['cu_may'] == 'MD' else NOI.get(r['diem_may'], 'thanh_pho'); c1 = cau1(r)
        if c1: sh['cau'] = c1
        if r['minh_hoa'] and r['ma'] in chon: s['kiem'] = next(x['kiem'] for x in ls if x['ma'] == r['ma']); sh['kiem'] = s['kiem']
        if r['cu_may'] == 'TL': sh['p']['tu_lieu'] = {'anh': r['tl_anh'], 'lop': r['lop_tl'], 'chu': r['them']['chu']}; sh['noi'] = 'tu_lieu'
        sh['ai_image'] = bool(r['minh_hoa'])
        bt = [{'t': 0.0, 'k': 'cut', 's': r['ma']}]
        if r['phan'] in G.CHUONG and abs(ch_t0[r['phan']] - r['t0']) < 1e-6:
            y, ph = G.CHUONG[r['phan']]; sh['p']['the_chuong'] = {'s': f'{y} — {ph}', 'at': 0.5, 'dur': 3.0}; sh['p']['chuong'] = sh['p']['the_chuong']; bt.append({'t': 0.5, 'k': 'the_chuong', 's': f'{y} — {ph}'})
        for (t0_, d_, n1, n2, th) in G.THE:
            if r['t0'] <= t0_ < r['t1']: bt.append({'t': round(t0_ - r['t0'], 3), 'k': 'the_nhan_vat', 's': n1})
        for (t0_, d_, n1, n2) in G.DEM:
            if r['t0'] <= t0_ < r['t1']: bt.append({'t': round(t0_ - r['t0'], 3), 'k': 'bo_dem', 's': f'{n1} {n2}'.strip()})
        if r['ma'] in G.KHAC: bt.append({'t': G.KHAC[r['ma']][2], 'k': 'tu_lieu', 's': G.KHAC[r['ma']][1]})
        if r['cu_may'] == 'TL': bt.append({'t': 0.0, 'k': 'tu_lieu', 's': r['them']['chu']})
        s['beats'] = sorted(bt, key=lambda x: x['t'])
        if r['cu_may'] == 'PP':
            PPd = json.loads((AN1 / 'the-phuong-phap.json').read_text())['the']
            for j, c in enumerate(PPd):
                segs.append({'id': f'PP{j + 1}', 'part': r['chuong'], 'chuong': r['chuong'], 'dur': c['giay'], 'fadeIn': 0, 'fadeOut': 0, 'moc_loi': [], 'beats': [{'t': 0.0, 'k': 'cut', 's': f'PP{j + 1}'}],
                             'title': c['tieu_de'] or 'How this film was made', 'the_phuong_phap': True,
                             'shots': [{'at': 0, 'type': 'card', 'tpl': 'card', 'role': 'the_phuong_phap', 'id': 'PP', 'title': c['tieu_de'] or '', 'dong': c['dong'], 'chu': ' '.join(([c['tieu_de']] if c['tieu_de'] else []) + c['dong']), 'text': ' '.join(c['dong']), 'lines': c['dong'], 'p': {'sach': True, 'tl': False, 'card': {'type': 'list', 'title': c['tieu_de'] or 'How this film was made', 'items': [{'s': d, 'at': 0.3 + 0.5 * i} for i, d in enumerate(c['dong'])]}}}]})   # chữ thẻ theo khuôn T3 (p.card.items)
            continue
        segs.append(s)
        if c1: nhip.append({'id': r['ma'], 'chinh': True, 'cau': c1[:40], 'vat': ([{'loai': 'the_chuong', 'shot': r['ma']}] if any(x['k'] == 'the_chuong' for x in bt) else []) + [{'loai': 'su_kien', 'shot': r['ma']}]})
    E = {'id': 'k2c-t4-02-anim3', 'title': 'London — T4 animatic v3 (whole episode, 640×360, G1 narration v3)', 'brand': 'MOVING PARTS', 'channel': 'k2', 'out': '/var/tmp/cine-out/k2c-t4-02-anim',
         'music': [], 'sources': {}, 'numbers': {}, 'khung_sach': True, 'kenh2_tu_t4': True, 'animatic': True,
         'ngan_sach_gemini_usd': 55, 'ngan_sach_gemini_moc_usd': 50, 'tu_lieu_tran_pct': 15,
         'tu_lieu_tran_ghi_chu': 'chủ dự án duyệt 20 % (25/10/2026 09:15, gói 50 % tiết kiệm: tư liệu + khắc + thẻ + ảnh/footage thật ≤ 20 %) — chờ K-1.17.7; khai 15 % theo checks 1.17.6',
         'goc_cao_san_pct': 50, 'goc_cao_ghi_chu': 'gói 50 % (chủ dự án 25/10/2026 09:15) — chờ K-1.17.7; 1.17.6 còn GOC-CAO-60', 'so_ai_gemini': 'so-ai-gemini-t4.jsonl', 'so_ai': 'so-ai-openai-t4.jsonl', 'so_ai_openai': 'so-ai-openai-t4.jsonl',
         'sha_tu_lieu': 'sha-tu-lieu-t4.txt', 'goc_toa_do': [532000, 180800], 'loi_khoa': '../loi-khoa-v3.txt', 'log_shot': 'log-shot.json', 'nhip_vat': 'nhip-vat.json', 'segments': segs}
    if (AN / 'xem-cam.json').exists(): E['xem_cam'] = 'xem-cam.json'
    (AN / 'nhip-vat.json').write_text(json.dumps({'nhip': nhip}, ensure_ascii=False, indent=1))
    (AN / 'episode.yaml').write_text('# TỆP SINH TỰ ĐỘNG bởi scripts/k2ldn/anim/mk_ep_v3.py (ANIMATIC-T4-V2). Đừng sửa tay.\n' + yaml.safe_dump(E, allow_unicode=True, sort_keys=False, width=200))
    tl = {'id': E['id'], 'title': E['title'], 'music': [], 'segments': [], 'heroes': {}}; t = 0.0
    for s in segs:
        d = float(s['dur']); S = {k: v for k, v in s.items() if k != 'shots'}
        S.update(t0=round(t, 4), t1=round(t + d, 4), frames=int(round(d * 24)), sfx=[], speech=[[round(c['bd'] - t, 3), round(c['kt'] - t, 3)] for c in M['cau'] if not c['bo'] and t <= c['bd'] < t + d])
        S['shots'] = [dict(x, t0=0.0, t1=d) for x in s['shots']]; tl['segments'].append(S); t += d
    tl['tong_s'] = round(t, 4); tl['tong_khung'] = int(round(t * 24)); (AN / 'timeline.json').write_text(json.dumps(tl, ensure_ascii=False))
    print(json.dumps({'shot': len(ls), 'co_log_may': sum(1 for x in ls if 'log_may' in x), 'so_ai_gemini': ng, 'so_ai_openai': no, 'tong_s': tl['tong_s']}, ensure_ascii=False))


if __name__ == '__main__': main()
