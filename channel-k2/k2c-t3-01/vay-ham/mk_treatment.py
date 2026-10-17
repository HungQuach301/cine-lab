# Sinh vay-ham/treatment.json từ bảng gọn (một dòng một shot). Cột:
# id | ch | dur | loai | noi | vung | goc | moc | agl_km | agl_max | claims | vai | may/preset | du_lieu_nha | hero | engine | mo_ta (VN, không phải lời)
import json, sys
R = open(__import__('pathlib').Path(__file__).with_name('treatment-rows.txt')).read()
shots = []
for line in R.strip().splitlines():
    f = [x.strip() for x in line.split('|')]
    sid, ch, dur, loai, noi, vung, goc, moc, agl, aglm, cl, vai, may, nha, hero, eng, mota = f
    s = dict(id=sid, ch=int(ch), dur=float(dur), loai=loai, noi=noi, vung=vung, goc=goc, moc_nam=moc, agl_km=float(agl), agl_max_km=float(aglm),
             claims=[c for c in cl.split(',') if c], vai=vai, may=may, du_lieu_nha=('' if nha == '—' else nha), hero=hero, engine=eng, mo_ta=mota)
    if loai in ('3D phố','3D vùng','bản đồ lịch sử','tranh Ken Burns') and sid not in ('0c','4b') and ch != '0':
        s['dur'] = round(s['dur'] * 1.25 * 2) / 2   # giãn theo lời (đích 9–11 phút, Kinh thánh §3); thẻ/ảnh giữ ≤ 8 s (Q32b)
    if 'MỐC ĐINH' in mota: s['moc_dinh'] = mota.split('MỐC ĐINH')[1].split(':')[0].strip()
    if 'LIÊN HOÀN #1' in may: s['cu'] = 'lien-hoan-1-gib20-1941'
    if 'LIÊN HOÀN #2' in may: s['cu'] = 'lien-hoan-2-vinh-1782'
    if sid == '0c': s['s_tren_50km'] = 2.5; s['s_tren_60km'] = 2.5; s['s_tren_3km'] = 3.0
    if sid == '4b': s['s_tren_3km'] = 1.5
    if sid == '2m': s['s_tren_3km'] = 0
    if s['agl_max_km'] > 3 and s['agl_km'] <= 3: s.setdefault('s_tren_3km', round(s['dur'] * 0.25, 1))
    shots.append(s)
json.dump({"note": "Bảng shot T3b (tiền kỳ, KHÔNG phải lời). Thời lượng ước theo treatment, chốt ở G1 theo lời thật. claims: S.. = claims-vay-ham.md; C.. = tienky/claims.json.", "shots": shots}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(shots), sum(s['dur'] for s in shots))
