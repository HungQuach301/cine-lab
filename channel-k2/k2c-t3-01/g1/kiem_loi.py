"""G1 T3 · kiểm chữ lời v1 (Kinh thánh §3, §10.6; lệnh G1 mục 5).
- Tách script-v1.md theo mã ‹shot›; bỏ mã claim {…}, dòng [TRÊN HÌNH], chú thích; đọc số thành chữ (năm kiểu Anh: 1704 → seventeen oh-four).
- Đếm TỪ NÓI (tách cả gạch nối — cùng cách đếm gói TUYẾN), ước giây ở 2,5 từ/s; so cửa sổ shot (dur trong treatment), cộng dồn theo chương; câu chảy sang shot sau.
- Kiểm: claim id có trong 4 bộ claim; claim CHƯA XÁC MINH không được gắn; từ cấm §10.6 / CS1–CS10; câu có số thương vong phải nói ai đếm.
Ghi g1/kiem-chu.json + in bảng. Dùng: /opt/cine/bin/python -I channel-k2/k2c-t3-01/g1/kiem_loi.py [script.md] [treatment.json]"""
import json, re, sys, unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent; EP = HERE.parent
WPS = 2.5
ONES = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split()
TENS = 'zero ten twenty thirty forty fifty sixty seventy eighty ninety'.split()


def n2w(n):
    if n < 20: return ONES[n]
    if n < 100: return TENS[n // 10] + ('-' + ONES[n % 10] if n % 10 else '')
    if n < 1000: return ONES[n // 100] + ' hundred' + (' and ' + n2w(n % 100) if n % 100 else '')
    for d, w in ((10 ** 9, 'billion'), (10 ** 6, 'million'), (1000, 'thousand')):
        if n >= d: return n2w(n // d) + ' ' + w + ((' and ' if n % d < 100 else ' ') + n2w(n % d) if n % d else '')


def year(n):
    if n % 1000 < 10 and n >= 2000: return n2w(n)                       # 2000–2009
    hi, lo = divmod(n, 100)
    if lo == 0: return n2w(hi) + ' hundred'
    return n2w(hi) + ' ' + ('oh-' + ONES[lo] if lo < 10 else n2w(lo))


def speak(t):
    t = re.sub(r'\b(1[0-9]{3}|20[0-9]{2})\b', lambda m: year(int(m.group(1))), t)
    t = re.sub(r'\b\d{1,3}(?:,\d{3})+\b|\b\d+\b', lambda m: n2w(int(m.group(0).replace(',', ''))), t)
    return t


def words(t): return [w for w in re.split(r"[\s\-–—]+", re.sub(r"[^\w\s\-–—'’]", ' ', t)) if re.search(r'\w', w)]


def load_claims():
    ids = {}
    for f, key in ((EP / 'vay-ham/claims-vay-ham.json', 'claims'), (EP / 'tienky/claims.json', 'claims'), (EP / 'tuyen/claims-tuyen.json', 'claims'), (HERE / 'claims-g1.json', 'claims')):
        for c in json.loads(f.read_text())[key]: ids[c['id']] = c['status']
    return ids


CAM = [  # (mẫu, luật) — §10.6 + TIEN-KY-VAY-HAM §6.1 CS1–CS10
    (r'\boccup', 'CS1 occupied/occupation (chỉ được trong câu trích có ghi ai nói, hoặc sự kiện không về chủ quyền Gibraltar)'),
    (r'\bstole|\bcolon(y|ial)|\busurp|\breconquer', 'CS1 (chỉ trong trích có ghi nguồn)'),
    (r'\bhero|\bglorious|\bcrush|\bhumiliat|\bbrave|\bcoward|\bcruel|\bbarbar|\bvaliant', 'CS2/§10.6 tính từ đạo đức cho phe'),
    (r'\bimpregnable|\bunbreakable|\binvincible', 'CS9'),
    (r'\buseless|\bridiculous|\bfoolish|\babsurd', 'CS10'),
    (r'\brevenge|\bpunish', 'CS3/CS7 suy động cơ'),
    (r'fifteen(th)? siege|15 sieges', 'CS5'),
    (r'land grab|perfectly legal|\billegal', 'CS8 (illegal chỉ trong trích)'),
    (r'\bthe (Spanish|British|English|French)\b(?! (crown|king|government|count|account|records|side|historian|batteries|works|forts|camp|army|squadron|estimate|Crown))', 'CS3 dân tộc như một khối (xem ngữ cảnh)'),
]
THUONG_VONG = r'\b(killed|dead|died|lost|losses|casualt|wounded|rescued|pulled)\b'
AI_DEM = r"count|record|return|account|estimate|historian|by both|by the|Montero|own"


def norm(t):
    t = ''.join(ch for ch in unicodedata.normalize('NFD', t.replace('ſ', 's').replace('’', "'").lower()) if unicodedata.category(ch) != 'Mn')
    t = re.sub(r'(\w)- (\w)', r'\1\2', t)
    return re.sub(r'[^a-z0-9]+', '', t.replace('f', 's'))


def load_quotes():
    Q = []
    for f in (EP / 'vay-ham/claims-vay-ham.json', EP / 'tienky/claims.json', EP / 'tuyen/claims-tuyen.json', HERE / 'claims-g1.json'):
        for c in json.loads(f.read_text())['claims']:
            for src in [c] + c.get('nguon_doi_chieu', []):
                if src.get('trich_nguyen_van'): Q.append((c['id'], norm(src['trich_nguyen_van'])))
    return Q


def parse(md):
    shots, ch = [], None
    for line in md.splitlines():
        m = re.match(r'^\[(\d\d) (\w+)\]\s*(.*)', line)
        if m: ch = (m.group(1), m.group(3)); continue
        m = re.match(r'^‹([^›]+)›\s*(.*)', line)
        if m: shots.append(dict(id=m.group(1), ch=ch, text=m.group(2), tren_hinh=[])); continue
        if line.startswith('[TRÊN HÌNH]') and shots: shots[-1]['tren_hinh'].append(line[len('[TRÊN HÌNH]'):].strip())
    return shots


def main():
    sp = Path(sys.argv[1]) if len(sys.argv) > 1 else EP / 'script-v1.md'
    tp = Path(sys.argv[2]) if len(sys.argv) > 2 else EP / 'vay-ham/treatment.json'
    S = parse(sp.read_text()); T = {s['id']: s for s in json.loads(tp.read_text())['shots']}
    ids = load_claims(); out = dict(script=str(sp.name), wps=WPS, shots=[], loi=[], canh_bao=[], cau_nhay_cam=[])
    order = [s['id'] for s in json.loads(tp.read_text())['shots']]
    assert [s['id'] for s in S] == order, ('lệch thứ tự shot', [s['id'] for s in S if s['id'] not in T], [i for i in order if i not in {x['id'] for x in S}])
    Q = load_quotes(); out['trich_tren_hinh'] = []
    for s in S:
        for th in s['tren_hinh']:
            for q in re.findall(r'«(.*?)»', th):
                parts = [norm(x) for x in q.split('…') if norm(x)]
                hit = sorted({cid for cid, src in Q if all(p in src for p in parts)})
                out['trich_tren_hinh'].append(dict(shot=s['id'], trich=q, claim=hit))
                if not hit: out['loi'].append(f'{s["id"]}: trích trên hình không khớp nguồn: «{q[:60]}»')
    carry = 0.0; t = 0.0
    for s in S:
        raw = s['text']; cl = re.findall(r'\{([A-Z]+\d+[a-z]?)\}', raw)
        silent = '[IM LẶNG]' in raw
        say = re.sub(r'\{[^}]*\}', '', raw).replace('‹Our read›', '').replace('[IM LẶNG]', '').strip()
        spoken = speak(say); w = words(spoken); need = len(w) / WPS
        wr = len(words(say)) if say else 0
        dur = T[s['id']]['dur']; start = carry; end = start + need
        spill = max(0.0, end - dur)
        row = dict(id=s['id'], ch=s['ch'][0], dur=dur, t0=round(t, 1), tu=len(w), tu_viet=wr, uoc_s=round(need, 1), bat_dau_tre_s=round(start, 1), tran_s=round(spill, 1),
                   im_lang=silent, claims=cl, so_doc=[(a, speak(a)) for a in re.findall(r'\b\d[\d,]*\b', say)])
        out['shots'].append(row); t += dur; carry = spill
        for c in cl:
            if c not in ids: out['loi'].append(f'{s["id"]}: claim {c} không có')
            elif ids[c].startswith('CHƯA'): out['loi'].append(f'{s["id"]}: claim {c} CHƯA XÁC MINH')
        if not cl: out['loi'].append(f'{s["id"]}: không có claim')
        if silent and say: out['loi'].append(f'{s["id"]}: tấm im lặng có lời')
        for sent in re.split(r'(?<=[.?!:])\s+', say):
            for pat, luat in CAM:
                if re.search(pat, sent, re.I): out['cau_nhay_cam'].append(dict(shot=s['id'], luat=luat, cau=sent))
            if re.search(THUONG_VONG, sent, re.I) and re.search(r'\d|hundred|thousand|sixteen|two', speak(sent)) and not re.search(AI_DEM, sent, re.I):
                out['loi'].append(f'{s["id"]}: số thương vong không nói ai đếm: "{sent}"')
        if spill > 1.5: out['canh_bao'].append(f'{s["id"]}: lời tràn {spill:.1f} s sang shot sau')
    chs = {}
    for r in out['shots']:
        c = chs.setdefault(r['ch'], dict(dur=0.0, uoc=0.0, tu=0)); c['dur'] += r['dur']; c['uoc'] += r['uoc_s']; c['tu'] += r['tu']
    out['chuong'] = {k: dict(dur=round(v['dur'], 1), uoc_s=round(v['uoc'], 1), tu=v['tu'], ty_le=round(v['uoc'] / v['dur'], 3)) for k, v in chs.items()}
    out['tong'] = dict(dur=round(t, 1), tu=sum(r['tu'] for r in out['shots']), tu_viet=sum(r['tu_viet'] for r in out['shots']), uoc_s=round(sum(r['uoc_s'] for r in out['shots']), 1))
    out['tong']['uoc_eric_s'] = round(out['tong']['tu_viet'] / (151.2 / 60), 1)   # T2 đo thật: Eric 151,2 từ viết/phút
    out['tong']['tu_phut_tren_phim'] = round(out['tong']['tu'] / (t / 60), 1)
    (HERE / 'kiem-chu.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
    for r in out['shots']:
        print(f"{r['id']:7} {r['dur']:5.1f} tu {r['tu']:3d} uoc {r['uoc_s']:5.1f} vao+{r['bat_dau_tre_s']:4.1f} tran {r['tran_s']:4.1f}{'  IM' if r['im_lang'] else ''}")
    print(json.dumps(dict(chuong=out['chuong'], tong=out['tong']), ensure_ascii=False))
    for q in out['trich_tren_hinh']: print('TRÍCH', q['shot'], q['claim'], q['trich'][:70])
    print('LỖI:', out['loi']); print('CẢNH BÁO:', out['canh_bao'])
    for c in out['cau_nhay_cam']: print('NHẠY CẢM', c['shot'], c['luat'][:30], '|', c['cau'][:110])
    return 1 if out['loi'] else 0


if __name__ == '__main__':
    sys.exit(main())
