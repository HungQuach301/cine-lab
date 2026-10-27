#!/opt/cine/bin/python
"""BAN-CUOI-T4-B2a · (bản sao qtd_soi_b1.py) q_thoi_dai LỚP CÔNG TRÌNH MỐC trên khung 3D năm biên (Kinh thánh §19 (d), D-A4 (i)) — chỉ CHẠY checks/ll/q_thoi_dai.py (không đọc mã).
Ảnh gửi: ô cắt quanh công trình mốc (theo mặt nạ 2, 1280×720) nếu khung có mã công trình; không có → nguyên khung (1280×720).
Chuỗi --moc theo năm (§19 (d)). Sổ: reports/ban-cuoi-t4-b2a/so-ai-claude.jsonl (usd từ dòng kết quả) + sua/soi/qtd-<máy>-k<khung>.json.
  qtd_soi_b1.py            qtd_soi_b2a.py [<json cắt> <tiền tố> <hậu tố>] (mặc định /var/tmp/bc/soi-crop-b2a.json, khung /var/tmp/bc/r/soi-<máy>/; usd: dòng kết quả, thiếu → tổng total_cost_usd trong JSON ra)"""
import json, os, re, subprocess, cv2
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(REPO, 'reports/ban-cuoi-t4-b2a/soi'); SO = os.path.join(REPO, 'reports/ban-cuoi-t4-b2a/so-ai-claude.jsonl'); os.makedirs(OUT, exist_ok=True)


def moc(y):
    a = []
    if y < 1671: a.append('no Monument column yet (the Monument was begun in 1671)')
    elif y < 1677: a.append('the Monument under construction (1671-1677): a fluted Doric column, incomplete at the top')
    else: a.append('the Monument (completed 1677): fluted Doric column with a gilded flaming urn on top')
    if y < 1675.5: a.append("no new St Paul's Cathedral (begun 1675); only the ruins of Old St Paul's")
    elif y < 1708: a.append("the new St Paul's Cathedral under construction (begun 1675): NO completed dome and lantern yet (completed 1708)")
    elif y < 1711: a.append("St Paul's with its completed dome and lantern (1708); the cathedral being finished (completed 1711)")
    else: a.append("St Paul's Cathedral completed (1711): dome, lantern, two west towers")
    return '; '.join(a)


import sys
NG, TIEN, HAU = (sys.argv[1:4] + ['/var/tmp/bc/soi-crop-b2a.json', 'soi', ''][len(sys.argv[1:4]):])   # lần soi lại: <json cắt> soi2 -lan2
for s in json.load(open(NG)):
    cm, f = s['may'], s['khung']; js = f'{OUT}/qtd-{cm}-k{f}{HAU}.json'
    if os.path.exists(js): continue
    im = cv2.imread(f'/var/tmp/bc/r/{TIEN}-{cm}/{f:05d}.jpg')
    if s.get('khung_cat') and s['px']: X, Y, w, h = s['khung_cat']; im = im[Y:Y + h, X:X + w]
    p = f'/var/tmp/bc/qmoc-soi/{cm}-k{f}.jpg'; os.makedirs(os.path.dirname(p), exist_ok=True); cv2.imwrite(p, cv2.resize(im, (1280, 720), interpolation=cv2.INTER_CUBIC), [cv2.IMWRITE_JPEG_QUALITY, 92])
    nam = int(s['nam']); mc = moc(s['nam'])
    c = ['/opt/cine/bin/python', 'checks/ll/q_thoi_dai.py', '--anh', p, '--nam', str(nam), '--noi', 'London', '--out', '/var/tmp/bc/qmoc-soi/o', '--api', '--lop-moc', '--moc', mc, '--json', js]
    r = subprocess.run(c, cwd=REPO, capture_output=True, text=True); last = (r.stdout.strip().splitlines() or [''])[-1]
    usd = re.search(r'chi phí \$([0-9.]+)', last); usd = float(usd.group(1)) if usd else None
    if usd is None and os.path.exists(js):
        def _sum(o): return sum(_sum(v) for v in o.values()) if isinstance(o, dict) and not any(k in o for k in ('total_cost_usd',)) else (float(o.get('total_cost_usd') or 0) if isinstance(o, dict) else sum(_sum(v) for v in o) if isinstance(o, list) else 0.0)
        usd = round(_sum(json.load(open(js))), 6)
    with open(SO, 'a') as fo: fo.write(json.dumps(dict(nha='anthropic', model=(re.findall(r'claude-[a-z0-9-]+', last) or [''])[-1], cong_cu='checks/ll/q_thoi_dai.py (claude -p)', lenh=' '.join(c[1:]), tep=os.path.relpath(js, REPO), anh_sha256=__import__('hashlib').sha256(open(p, 'rb').read()).hexdigest(), usd=usd, rc=r.returncode, nguon='B2a soi niên đại năm biên (§19 (d)) trước dựng 1080p', val=last), ensure_ascii=False) + '\n')
    print(cm, f, s['nam'], '|', last, flush=True)
