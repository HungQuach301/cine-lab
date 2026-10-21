#!/opt/cine/bin/python -I
"""NC-V2V · chuẩn hoá sổ AI (so-ai.jsonl, ghi lúc gọi) → so-ai-klai.json theo trường K-LAI-6: model (req + resp), prompt nguyên văn, mask.pct_duoc_sua,
usage, usd, c2pa (đọc thẳng manifest JUMBF trong tệp ra: có/không, digitalSourceType, hành động), date_utc, file + sha256 vào/ra. Lệnh lỗi (502/402): không đòi phần ảnh."""
import hashlib, json, re, sys
from pathlib import Path
src, out = Path(sys.argv[1]), Path(sys.argv[2]); rows = []
for l in src.read_text().splitlines():
    r = json.loads(l); o = r.get('output') or {}; c2 = None
    if o.get('file') and Path(o['file']).exists():
        b = Path(o['file']).read_bytes(); assert hashlib.sha256(b).hexdigest() == o['sha256'], o['file']; h = b[:20000]
        c2 = dict(co=b'c2pa.claim' in h, digitalSourceType=sorted(set(m.decode() for m in re.findall(rb'digitalsourcetype/([a-zA-Z]+?Media)', h))),
                  hanh_dong=sorted(set(m.decode() for m in re.findall(rb'c2pa\.(created|edited|opened|converted)', h))), synthid_trong_manifest=b'SynthID' in h, ky_boi='Google C2PA Media Services' if b'Google C2PA Media Services' in h else None)
    rows.append(dict(tag=r['tag'], model_req=r['model_req'], model_resp=r.get('model_resp'), date_utc=r['date_utc'], prompt=r['prompt'], res=r.get('res'), prev=r.get('prev'), task=r.get('task'),
                     input=[dict(file=Path(i['file']).name, sha256=i['sha256'], bytes=i['bytes']) for i in r['input']], http=r['http'], loi=r.get('loi'),
                     output=dict(file=Path(o['file']).name, sha256=o['sha256'], bytes=o['bytes']) if o else None, usage=r.get('usage'), usd=r.get('usd'),
                     mask=dict(pct_duoc_sua=100.0, ghi_chu='Omni sửa TOÀN KHUNG (không có mặt nạ vùng)') if o else None, c2pa=bool(c2 and c2['co']), c2pa_chi_tiet=c2, synthid=True if o else None, wall_s=r.get('wall_s'), id=r.get('id')))
tot = round(sum(x['usd'] or 0 for x in rows), 4)
json.dump(dict(nguon_gia='ai.google.dev/gemini-api/docs/pricing (đọc 19/10/2026): vào $1,50/1M token (văn bản/ảnh/video), ra $17,50/1M token video, $9/1M token văn bản + suy nghĩ; 5 792 token/giây video 720p',
               tong_usd_uoc=tot, so_lenh=len(rows), thanh_cong=sum(1 for x in rows if x['output']), lenh=rows), open(out, 'w'), ensure_ascii=False, indent=1)
print(tot, len(rows), sum(1 for x in rows if x['output']))
