#!/opt/cine/bin/python
"""K-1.17.7 việc 6: hiệu chuẩn lớp công trình mốc của q_thoi_dai (đề bài o2-v3-moc) trên khung H2-13 v1 (phải bắt) + 3 khung đúng (không báo).
Chạy: /opt/cine/bin/python -I reports/k1177/do/moc/chay_moc.py  (gọi Claude qua judge.call — có chi phí; sổ: reports/k1177/so-ai.jsonl)"""
import hashlib, json, os, sys, time
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')); sys.path.insert(0, R)
from checks.ll import q_thoi_dai as Q
K = os.path.join(R, 'channel-k2/k2c-t4-02/animatic/omni/kiem')
SP = "St Paul's Cathedral with Wren's dome (completed 1710), dominating the City skyline"
MAU = [dict(id='H2-13-l2-k25', anh=f'{K}/H2-13-l2-360p-k25.jpg', nam=1711, moc=[SP], dap_an='bat'),
       dict(id='H2-13-l2-k55', anh=f'{K}/H2-13-l2-360p-k55.jpg', nam=1711, moc=[SP], dap_an='bat'),
       dict(id='H2-13-l2-k90', anh=f'{K}/H2-13-l2-360p-k90.jpg', nam=1711, moc=[SP], dap_an='bat'),
       dict(id='H3-04b-l1-k55', anh=f'{K}/H3-04b-l1-360p-k55.jpg', nam=1935, moc=["St Paul's Cathedral, Wren's dome (completed 1710)"], dap_an='khong'),
       dict(id='H4-01b-l1-k55', anh=f'{K}/H4-01b-l1-360p-k55.jpg', nam=1940, moc=["St Paul's Cathedral, Wren's dome (completed 1710)"], dap_an='khong'),
       dict(id='H2-01a-l1-k55', anh=f'{K}/H2-01a-l1-360p-k55.jpg', nam=1666,
            moc=["Old St Paul's Cathedral, gutted by the Great Fire of September 1666: roofless stone shell with its square central tower (spire lost in 1561); no dome yet"], dap_an='khong')]
OUT = '/var/tmp/k1177/moc'; os.makedirs(OUT, exist_ok=True)
SO = os.path.join(R, 'reports/k1177/so-ai.jsonl'); KQ = []
for m in MAU:
    sha_in = hashlib.sha256(open(m['anh'], 'rb').read()).hexdigest()
    k = Q.soi_khung(m['anh'], m['nam'], OUT, m['id'], 'London', api=True, cache=None, moc=m['moc'])
    bat = any(x['muc'] == 'cong_trinh_moc' for x in k['nghi_van'])
    KQ.append(dict(id=m['id'], nam=m['nam'], dap_an=m['dap_an'], bat_moc=bat, nghi_van=k['nghi_van'], ghi_chu=k['ghi_chu'], loi=k['loi'], cost_usd=k['cost_usd'], prompt_ver=k.get('prompt_ver')))
    mu = k.get('model_usage') or {}
    dong = dict(ts=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), phien='K-1.17.7', viec='6 hiệu chuẩn lớp công trình mốc', model=Q.MODEL,
                lenh='claude -p --bare --restricted --model ' + Q.MODEL + ' --tools Read (checks/ll/judge.call) · đề bài q_thoi_dai.prompt_for(nam, "London", moc) ' + Q.PROMPT_VER_MOC,
                prompt_sha=hashlib.sha256(Q.prompt_for(os.path.join(OUT, m['id']), m['nam'], 'London', m['moc']).encode()).hexdigest(), moc=m['moc'],
                sha_vao=sha_in, sha_ra=hashlib.sha256((k.get('tra_loi') or '').encode()).hexdigest(), usage={kk: {x: v.get(x) for x in ('inputTokens', 'outputTokens', 'cacheReadInputTokens', 'cacheCreationInputTokens')} for kk, v in mu.items()},
                usd=k.get('cost_usd'), id=m['id'], ket_qua=dict(bat_moc=bat, so_nghi_van=len(k['nghi_van']), loi=k['loi']))
    open(SO, 'a').write(json.dumps(dong, ensure_ascii=False) + '\n')
    print(m['id'], m['nam'], 'đáp án', m['dap_an'], '→ bắt mốc' if bat else '→ không báo mốc', f"${k['cost_usd']}", k['loi'] or '', [(x['muc'], x['do_tin'], x['mo_ta'][:90]) for x in k['nghi_van']], flush=True)
json.dump(KQ, open(os.path.join(os.path.dirname(__file__), 'ket-qua-moc.json'), 'w'), ensure_ascii=False, indent=1)
