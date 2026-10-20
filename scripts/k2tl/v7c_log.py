#!/opt/cine/bin/python
"""V7C · bổ sung log shot cho k2check 1.16.1 (K116-D9) từ số đo mặt nạ ID: trong_pct (đất trống không vật = bằng + sườn, TB shot), trong_ca_nuoc_pct, noi_dung_pct, tieu_diem_dat_pct,
goc (cao/thap theo V7B-D1 trên khung đo: AGL ≥ 120 m hoặc nhìn xuống ≥ 15° = cao; AGL < 50 m = thấp) + phần trăm khung mỗi loại; ghi xem-cam-v7c.json từ kết quả chấm.
  v7c_log.py <nhãn đo> [<nhãn xem câm> <video đã chấm>]"""
import datetime, hashlib, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]; EPD = ROOT / 'channel-k2/k2c-t3-01/v7p'; DO = ROOT / 'reports/v7c/do'
a = sys.argv[1:]; L = json.loads((EPD / 'log-shot-v7c.json').read_text())
for s in L:
    p = DO / f'bocuc-{a[0]}' / f"{s['shot']}.json"
    if not p.exists(): continue
    F = json.loads(p.read_text())['frames']; n = len(F)
    s['trong_pct'] = round(sum(r['pct']['bang'] + r['pct']['suon'] for r in F) / n, 1); s['trong_ca_nuoc_pct'] = round(sum(r['trong'] for r in F) / n, 1)
    s['noi_dung_pct'] = round(sum(r['noi_dung'] for r in F) / n, 1); s['tieu_diem_dat_pct'] = round(100 * sum(any(t.get('dat') for t in r['td']) for r in F) / n)
    s['cao_khung_pct'] = round(100 * sum(r['agl'] >= 120 or r['xuong'] >= 15 for r in F) / n); s['thap_khung_pct'] = round(100 * sum(r['agl'] < 50 for r in F) / n)
    s['do_bo_cuc'] = f'reports/v7c/do/bocuc-{a[0]}/{s["shot"]}.json'
(EPD / 'log-shot-v7c.json').write_text(json.dumps(L, ensure_ascii=False, indent=1) + '\n')
if len(a) >= 3:   # xem-cam-v7c.json (K116-D9 mục 3): 8 câu = 4 câu V7B × 2 tiêu chí (ý chính · chi tiết); mỗi người chấm 'dung' = điểm 0–8 (0/1/2 mỗi câu); chủ dự án: chờ
    sys.path.insert(0, str(Path(__file__).resolve().parent)); import v7b_cam as B
    R = json.loads((ROOT / f'reports/v7c/xem-cam/{a[1]}/r320/ket-qua.json').read_text()); vid = Path(a[2])
    cau = [f'{q} — {t}' for q in B.Q for t in ('ý chính', 'chi tiết')]
    out = dict(tat_tieng=True, cau_hoi=cau, ghi='4 câu V7B × 2 tiêu chí (0/1/2 mỗi câu = 2 mục); chuỗi 1 khung/2 s, 320×180 (sàn); bản 640×360 ở reports/v7c/xem-cam/<nhãn>/r640; chủ dự án CHƯA chấm',
               nguoi_cham=[dict(id=rk, vai='ai', dung=sum(v['diem'].values()), tong=8, ngay=datetime.date.today().isoformat()) for rk, v in R['nguoi'].items()],
               video=str(vid.relative_to(ROOT)) if str(vid).startswith(str(ROOT)) else str(vid), video_sha256=hashlib.sha256(vid.read_bytes()).hexdigest())
    (EPD / 'xem-cam-v7c.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
print('ok', len(L))
