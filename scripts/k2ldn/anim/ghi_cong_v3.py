#!/opt/cine/bin/python
"""ANIMATIC-T4-V2 · việc 5 — GHI CÔNG đầy đủ cho mô tả YouTube: channel-k2/k2c-t4-02/animatic2/ghi-cong.json (+ ghi-cong-youtube.txt).
Gom từ: BANG-SHOT-v3 (shot TL toàn khung, thẻ có chân dung), ghep_v3.KHAC (tranh khắc góc khung), nc/licenses/*.json (NC-T4, tải lại theo lệnh bổ sung 10:05),
animatic2/tu-lieu/giay-phep/*.json (Commons), licenses/*.json + RIGHTS.md (tư liệu T4 cũ), am-cue (nhạc), sfx (CC0/PD), sổ AI (mô hình). Chỉ ghi mục THẬT SỰ có trong animatic v3."""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
REPO = Path(__file__).resolve().parents[3]; EP = REPO / 'channel-k2/k2c-t4-02'; AN2 = EP / 'animatic2'
TL_CU = {   # tư liệu T4 có sẵn (RIGHTS.md T4-TL-*, T4-AN-*; licenses/*.json)
 'met-360649-1': ('Wenceslaus Hollar, prospect of London before the Fire (etching, published 1666)', 'The Metropolitan Museum of Art, 17.50.101', 'CC0 (Met Open Access)', 'https://www.metmuseum.org/art/collection/search/360649'),
 'met-360649-0': ('Wenceslaus Hollar, prospect of London after the Fire (etching, 1666)', 'The Metropolitan Museum of Art, 17.50.100', 'CC0 (Met Open Access)', 'https://www.metmuseum.org/art/collection/search/360649'),
 'met-395057-0': ("Wenceslaus Hollar, Old St Paul's Cathedral seen from the East (etching, 1656–58)", 'The Metropolitan Museum of Art, 2010.529', 'CC0 (Met Open Access)', 'https://www.metmuseum.org/art/collection/search/395057'),
 'ycba-40597-0': ('General View of London during the Great Fire of 1666 (print)', 'Yale Center for British Art, B1977.14.17854', 'Public domain (YCBA open access)', 'https://manifests.collections.yale.edu/ycba/obj/40597'),
 'rijks-luyken-0': ('Jan Luyken, The Great Fire of London, 1666 (etching, 1698)', 'Rijksmuseum, RP-P-1896-A-19368-1507', 'Public Domain Mark', 'https://www.rijksmuseum.nl/en/collection/RP-P-1896-A-19368-1507'),
 'rijks-monument-0': ('View of the Monument, London (engraving, after 1676)', 'Rijksmuseum, RP-P-2018-836', 'Public Domain Mark', 'https://www.rijksmuseum.nl/en/collection/RP-P-2018-836'),
 'loc-wren-plan-0': ("A Plan for rebuilding the City of London after the Great Fire in 1666, designed by Sir Christopher Wren (engraving, 1767)", 'Library of Congress', 'No known restrictions on publication', 'https://www.loc.gov/'),
 'nga-wren-0': ('John Smith after Godfrey Kneller, Sir Christopher Wren (mezzotint)', 'National Gallery of Art, Washington, 2001.118.55', 'CC0 (NGA Open Access)', 'https://www.nga.gov/'),
 'rijks-doornick-0': ('Marcus Willemsz Doornick, Platte Grondt der Verbrande Stadt London (map, Amsterdam 1666)', 'Rijksmuseum, RP-P-OB-82.345', 'Public Domain Mark', 'https://www.rijksmuseum.nl/en/collection/RP-P-OB-82.345'),
}


def nc(k):
    p = EP / 'nc/licenses' / f'{k}.json'
    if not p.exists(): return None
    j = json.loads(p.read_text()); t = ', '.join(x for x in [j.get('creator') if j.get('creator') and 'không ghi' not in str(j.get('creator')) else None, j.get('title'), j.get('date')] if x)
    return (t, j.get('holder'), j.get('licence'), j.get('source_url'))


def commons(k):
    p = AN2 / 'tu-lieu/giay-phep' / f'{k}.json'
    if not p.exists(): return None
    j = json.loads(p.read_text()); clean = lambda s: re.sub(r'<[^>]+>', '', str(s or '')).strip()
    return (f"{clean(j.get('tac_gia'))}, {clean(j.get('mo_ta'))[:160]} ({clean(j.get('ngay'))})", 'Wikimedia Commons' + (f" — {clean(j.get('credit'))[:120]}" if j.get('credit') else ''), clean(j.get('giay_phep')), j['trang'])


def main():
    import ghep_v3 as G
    B = json.loads((EP / 'BANG-SHOT-v3.json').read_text()); dung = {}
    def them(k, shot, vai):
        dung.setdefault(k, {'shot': [], 'vai': set()}); dung[k]['shot'].append(shot); dung[k]['vai'].add(vai)
    for r in B['shot']:
        if r['cu_may'] == 'TL': them(r['tl_anh'], r['ma'], 'toàn khung (ảnh/tư liệu thật, chuyển động 2D)')
        if r['ma'] in G.KHAC: them(G.KHAC[r['ma']][0], r['ma'], 'góc khung ≤ 1/3')
        for n, a in (r['them'].get('the_anh') or {}).items(): them(a, r['ma'], 'ảnh thẻ nhân vật')
        if r['them'].get('ban_do') or r['them'].get('ban_do_chong'): them('rijks-doornick-0', r['ma'], 'bản đồ hoạt hoá')
    muc = []
    for k, v in dung.items():
        info = TL_CU.get(k) or nc(k) or commons(k) or commons(k.replace('-h5-07a', '-h5-07a-goc'))
        muc.append({'id': k, 'shot': v['shot'], 'cach_dung': sorted(v['vai']), 'tac_pham': info[0] if info else None, 'noi_giu': info[1] if info else None, 'giay_phep': info[2] if info else 'THIẾU — chưa có bằng chứng', 'url': info[3] if info else None})
    cue = json.loads((AN2 / 'am-cue.json').read_text()) if (AN2 / 'am-cue.json').exists() else {}
    nhac = sorted({c['tep'] for c in cue.get('nhac', [])})
    out = {'tap': 'K2C-T4-02 London', 'ban': 'animatic v3 (ANIMATIC-T4-V2, 25/10/2026)', 'tu_lieu_hinh': muc,
           'nhac': [{'tep': n, 'tac_gia': 'Scott Buckley', 'giay_phep': 'CC BY 4.0', 'url': 'https://www.scottbuckley.com.au'} for n in nhac],
           'sfx': [{'nguon': 'BigSoundBank (Joseph Sardin)', 'giay_phep': 'CC0'}, {'nguon': 'OpenGameArt', 'giay_phep': 'CC0'}, {'nguon': 'U.S. National Park Service sound library', 'giay_phep': 'public domain (U.S. federal work)'}],
           'ai': [{'cong_cu': 'OpenAI gpt-image-2.5 (first frames for illustrative clips)'}, {'cong_cu': 'Google Gemini Omni (illustrative video clips, SynthID)'}, {'cong_cu': 'ElevenLabs (narration voice)'}],
           'ghi_chu': 'Nhãn AI không có trong hình (§15); mô tả YouTube nêu cảnh minh hoạ AI. Bản đồ/khối 3D dựng từ OSM (ODbL) + EA LiDAR (OGL v3).'}
    (AN2 / 'ghi-cong.json').write_text(json.dumps(out, ensure_ascii=False, indent=1))
    L = ['Archive images and footage:']
    for m in muc: L.append(f"- {m['tac_pham']} — {m['noi_giu']} ({m['giay_phep']}) {m['url'] or ''}".strip())
    L += ['', 'Music: Scott Buckley (CC BY 4.0) — ' + ', '.join(Path(n).stem.replace('sb_', '').replace('_', ' ') for n in nhac), 'Sound effects: BigSoundBank & OpenGameArt (CC0); U.S. National Park Service (public domain).',
          'Map and 3D city data: © OpenStreetMap contributors (ODbL); Environment Agency LiDAR (Open Government Licence v3).',
          'Some illustrative scenes were generated with AI (OpenAI image model; Google Gemini Omni video) and checked for historical accuracy; narration voice by ElevenLabs.']
    (AN2 / 'ghi-cong-youtube.txt').write_text('\n'.join(L) + '\n'); print(len(muc), 'mục tư liệu;', sum(1 for m in muc if 'THIẾU' in str(m['giay_phep'])), 'thiếu bằng chứng')


if __name__ == '__main__': main()
