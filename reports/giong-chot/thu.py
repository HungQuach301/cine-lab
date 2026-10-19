#!/opt/cine/bin/python
"""GIỌNG-CHỐT · thu G1. thu.py <lượt> … ; lượt: bang | moc (speed 1,00/1,03/1,06, v2) | moc-b (lượt B, cùng seed) | pin-v2 (speed 1,0) | pin-v4 (eleven_v4, không có Speed)
Đọc bộ đếm tài khoản trước/sau MỖI lượt (chờ 90 s cho bộ đếm cập nhật — lượt moc 20 s thấy bộ đếm trễ) → bo-dem.jsonl. Bản thô: $CG_OUT/raw/<băm>.mp3; chỉ mục: $CG_OUT/thu.json."""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import gc_lib as G
D = json.load(open(f'{G.H}/doan.json')); IDX = f'{G.L.OUT}/thu.json'
idx = json.load(open(IDX)) if os.path.exists(IDX) else {}
LUOT = {'bang': [('bang', D['bang']['gui'], G.V2, 1.0)],
        'moc': [(f'moc-{s:.2f}', D['moc']['gui'], G.V2, s) for s in (1.00, 1.03, 1.06)],
        'pin-v2': [('pin-v2', D['pin']['gui'], G.V2, 1.0)],
        'pin-v4': [('pin-v4', D['pin']['gui'], G.V4, None)],
        'moc-b': [(f'mocb-{s:.2f}', D['moc']['gui'], G.V2, s) for s in (1.00, 1.03, 1.06)]}   # lượt B: cùng seed SEED_B cho cả 3 mức
SEED_B = 19102026
def dem(): time.sleep(90); return G.sub()['character_count']
for l in sys.argv[1:]:
    c0 = G.sub()['character_count']; gui = 0
    for tag, text, model, sp in LUOT[l]:
        st = dict(stability=0.5, similarity_boost=0.75) if sp is None else dict(stability=0.5, similarity_boost=0.75, speed=sp)
        p, n = G.tts_seed(text, tag, SEED_B, model=model, settings=st) if tag.startswith('mocb') else G.tts(text, tag, model=model, settings=st); gui += n
        idx[tag] = dict(tep=p, model=model, settings=st, ky_tu=len(text), **({'seed': SEED_B} if tag.startswith('mocb') else {})); json.dump(idx, open(IDX, 'w'), indent=1); print(tag, p, n, flush=True)
    c1 = dem()
    rec = dict(luot=l, gui=gui, dem_truoc=c0, dem_sau=c1, tang=c1 - c0, ty_le=round((c1 - c0) / gui, 3) if gui else None, luc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
    open(f'{G.H}/bo-dem.jsonl', 'a').write(json.dumps(rec, ensure_ascii=False) + '\n'); print(rec, flush=True)
print('tổng gửi phiên:', G.da_gui())
