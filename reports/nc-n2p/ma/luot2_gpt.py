#!/opt/cine/bin/python -I
"""NC-N2P · LƯỢT ĐỌC THỨ HAI bằng mô hình KHÁC (gpt-6.1-sol; lượt 1 = phiên P, Claude) cho danh mục (a)/(b) (§12.3): mỗi mục gửi câu trích + 6 dòng ngữ cảnh quanh dòng
khớp (từ tệp có SHA) + mô tả/ngày/loại mà phiên gán → mô hình chấm: dung | sai_loai (đứng yên ↔ chuyển động, hoặc không phải vật) | sai_ngay | hieu_qua (mô tả vượt câu trích) | khong_co.
  luot2_gpt.py <danh-muc.json> → <danh-muc>.luot2.json"""
import json, sys, time, urllib.request
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import n2p_lib as L  # noqa: E402
from vision_kiem import log_cost  # noqa: E402

P = """You are checking a research catalogue built from primary sources on the Great Fire of London (dates are Old Style, September 1666).
For each item you get: the catalogue description (in Vietnamese), the claimed date, the claimed kind ("dung_yen" = a motionless object that may appear in a still picture;
"chuyen_dong" = something that moves; "su_kien/ranh" = a fact about the fire's extent or a landmark), the verbatim quotation and the surrounding source lines.
Judge each item ONLY from the quotation and its context. Verdicts: "dung" (correct), "sai_loai" (wrong kind), "sai_ngay" (the context shows a different date),
"hieu_qua" (the description claims more than the quotation supports), "khong_co" (the quotation does not say this).
Answer ONLY a JSON object: {"muc": [{"id": "...", "ket_luan": "dung|sai_loai|sai_ngay|hieu_qua|khong_co", "ly_do": "<short>"}]}

ITEMS:
"""


def main():
    f = Path(sys.argv[1]); D = json.load(open(f)); K = {r['id']: r for r in json.load(open(f.with_suffix('.kiem.json')))['muc']}; items = []
    for m in D['muc']:
        if not m.get('trich'): continue
        tl = (L.REPO / D['nguon'][m['nguon']]['tep']).read_text(errors='replace').splitlines(); dg = K[m['id']]['dong'] or 1
        ctx = '\n'.join(tl[max(0, dg - 4):dg + 3])[:1800]
        items.append(dict(id=m['id'], mo_ta=m['vat'], ngay=m.get('ngay_ap', m.get('ngay')), loai=m.get('loai', 'su_kien/ranh'), trich=m['trich'], ngu_canh=ctx))
    body = {'model': 'gpt-6.1-sol', 'input': P + json.dumps(items, ensure_ascii=False), 'stream': True, 'reasoning': {'effort': 'medium'}}
    rq = urllib.request.Request('https://api.openai.com/v1/responses', data=json.dumps(body).encode(), headers={'Content-Type': 'application/json', 'User-Agent': L.UA})
    txt, usage, model = '', {}, None
    with urllib.request.urlopen(rq, timeout=900) as r:
        for line in r:
            line = line.decode().strip()
            if not line.startswith('data:'): continue
            ev = json.loads(line[5:].strip())
            if ev.get('type') == 'response.output_text.delta': txt += ev.get('delta', '')
            if ev.get('type') == 'response.completed': usage = ev['response'].get('usage', {}); model = ev['response'].get('model')
    usd = round(usage.get('input_tokens', 0) * 2e-6 + usage.get('output_tokens', 0) * 10e-6, 4)
    log_cost({'tag': 'luot2-' + f.stem, 'model': 'gpt-6.1-sol', 'served': model, 'usd': usd, 'in': usage.get('input_tokens', 0), 'out': usage.get('output_tokens', 0), 'date_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())})
    j = json.loads(txt[txt.find('{'):txt.rfind('}') + 1]); out = f.with_suffix('.luot2.json')
    json.dump(dict(model=model, usd=usd, ket_qua=j['muc']), open(out, 'w'), ensure_ascii=False, indent=1)
    from collections import Counter
    print(f.name, Counter(x['ket_luan'] for x in j['muc']), usd)
    for x in j['muc']:
        if x['ket_luan'] != 'dung': print(' ', x['id'], x['ket_luan'], x['ly_do'][:160])


if __name__ == '__main__': main()
