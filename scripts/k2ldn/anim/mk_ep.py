#!/opt/cine/bin/python
"""ANIMATIC-T4 · việc 8 — khai cho k2check 1.17.4 (Kinh thánh §13.6 "Cách khai T4", K1174 §5): channel-k2/k2c-t4-02/animatic/{episode.yaml, log-shot.json, timeline.json, so-ai-*-t4.jsonl, log-may/*.json}.
episode.yaml: kenh2_tu_t4, animatic, ngan_sach_gemini_usd 35 / moc 30 (chủ dự án 23/10/2026 23:45), so_ai_gemini (gộp sổ Gemini T4: tiền kỳ + LOOK-T4-V2 + phiên này, mỗi dòng `usd` thật),
so_ai / so_ai_openai (gộp OpenAI T4), sha_tu_lieu (licenses/SHA256-TU-LIEU.txt + -LOOK), goc_toa_do [532000, 180800], log_shot. Log shot từng shot: cu_may, log_may (log.json render_look.js,
giữ trong git — K1174-D4), tieu_diem_en, khop_voi/diem_neo/hoa_s, lo_ra, lop, ai_nen, minh_hoa, goc, tl, chuong. Timeline: một đoạn mỗi shot (cách mk_tl.py của K-1.17.2), speech = mốc câu lời dựng."""
import gzip, json, shutil
from pathlib import Path
import yaml
REPO = Path(__file__).resolve().parents[3]; EP = REPO / 'channel-k2/k2c-t4-02'; AN = EP / 'animatic'


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
    B = json.loads((EP / 'BANG-SHOT-v2.json').read_text()); M = json.loads((AN / 'loi-dung-moc.json').read_text())
    LG = AN / 'log-may'; LG.mkdir(exist_ok=True)
    for gz in LG.glob('*.json.gz'):   # log.json đầy đủ (không nén) — mỗi tệp < 1 MB; bản .gz cũ bỏ
        j = LG / gz.name[:-3]
        if not j.exists(): j.write_bytes(gzip.decompress(gz.read_bytes()))
        gz.unlink()
    for d in Path('/var/tmp/anim/r').iterdir():
        if (AN / 'may' / f'{d.name}.json').exists() and (d / 'log.json').exists() and not (LG / f'{d.name}.json').exists(): shutil.copy(d / 'log.json', LG / f'{d.name}.json')
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
        x['tu_lieu_chong_sau_ai'] = False
        ls.append(x)
    (AN / 'log-shot.json').write_text(json.dumps(ls, ensure_ascii=False, indent=1))
    R = REPO / 'reports'
    ng = gop([R / 'tien-ky-t4/so-ai-gemini.jsonl', R / 'look-t4-v2/so-ai.jsonl', R / 'animatic-t4/so-ai-gemini.jsonl'], lambda r: 'gemini' in json.dumps(r.get('model_req', '') + str(r.get('nha', ''))).lower(), AN / 'so-ai-gemini-t4.jsonl')
    no = gop([R / 'tien-ky-t4/so-ai.jsonl', R / 'look-t4-v2/so-ai.jsonl', R / 'animatic-t4/so-ai.jsonl'], lambda r: r.get('nha') == 'openai', AN / 'so-ai-openai-t4.jsonl')
    sha = AN / 'sha-tu-lieu-t4.txt'; sha.write_text((EP / 'licenses/SHA256-TU-LIEU.txt').read_text() + (EP / 'licenses/SHA256-TU-LIEU-LOOK.txt').read_text())
    segs = []
    for r in B['shot']:
        tp = {'MD': 'minh_hoa', 'PP': 'card'}.get(r['cu_may'], 'scene3d')
        s = {'id': r['ma'], 'part': r['chuong'], 'chuong': r['chuong'], 'dur': r['dur'], 'fadeIn': 0, 'fadeOut': 0,
             'moc_loi': [{'t': round(c['bd'] - r['t0'], 3), 's': c['khoa'][:28]} for c in M['cau'] if not c['bo'] and r['t0'] <= c['bd'] < r['t1']],
             'shots': [{'at': 0, 'type': tp, 'tpl': 'plate', 'p': {'sach': True, 'tl': r['tl']}, 'cau': ' '.join(r['cau_loi'])[:300]}]}
        if r['cu_may'] == 'PP': s['shots'][0].update(role='the_phuong_phap', id='PP'); s['title'] = 'How this film was made'; s['the_phuong_phap'] = True
        segs.append(s)
    E = {'id': 'k2c-t4-02-anim', 'title': 'London — T4 animatic (whole episode, 640×360, G1 v2 narration, K1-C1)', 'brand': 'MOVING PARTS', 'channel': 'k2', 'out': '/var/tmp/cine-out/k2c-t4-02-anim',
         'music': [], 'sources': {}, 'numbers': {}, 'khung_sach': True, 'kenh2_tu_t4': True, 'animatic': True,
         'ngan_sach_gemini_usd': 35, 'ngan_sach_gemini_moc_usd': 30, 'so_ai_gemini': 'so-ai-gemini-t4.jsonl', 'so_ai': 'so-ai-openai-t4.jsonl', 'so_ai_openai': 'so-ai-openai-t4.jsonl',
         'sha_tu_lieu': 'sha-tu-lieu-t4.txt', 'goc_toa_do': [532000, 180800], 'loi_khoa': '../loi-khoa.txt', 'log_shot': 'log-shot.json', 'segments': segs}
    (AN / 'episode.yaml').write_text('# TỆP SINH TỰ ĐỘNG bởi scripts/k2ldn/anim/mk_ep.py (ANIMATIC-T4). Đừng sửa tay.\n' + yaml.safe_dump(E, allow_unicode=True, sort_keys=False, width=200))
    tl = {'id': E['id'], 'title': E['title'], 'music': [], 'segments': [], 'heroes': {}}; t = 0.0
    for s in segs:
        d = float(s['dur']); S = {k: v for k, v in s.items() if k != 'shots'}
        S.update(t0=round(t, 4), t1=round(t + d, 4), frames=int(round(d * 24)), sfx=[], speech=[{'t0': round(c['bd'] - t, 3), 't1': round(c['kt'] - t, 3), 'text': c['khoa']} for c in M['cau'] if not c['bo'] and t <= c['bd'] < t + d])
        S['shots'] = [dict(x, t0=0.0, t1=d) for x in s['shots']]; tl['segments'].append(S); t += d
    tl['tong_s'] = round(t, 4); tl['tong_khung'] = int(round(t * 24)); (AN / 'timeline.json').write_text(json.dumps(tl, ensure_ascii=False))
    print(json.dumps({'shot': len(ls), 'co_log_may': sum(1 for x in ls if 'log_may' in x), 'so_ai_gemini': ng, 'so_ai_openai': no, 'tong_s': tl['tong_s']}, ensure_ascii=False))


if __name__ == '__main__': main()
