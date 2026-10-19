#!/opt/cine/bin/python
"""CASTING-MỸ · Voice Design: 2 mô tả giọng nam Mỹ lớn tuổi, trầm, kịch tính vừa đủ; mỗi mô tả 1 lần gọi /v1/text-to-voice/design.
API trả 3 biến thể cho cùng một lần tính phí; theo lệnh chỉ xét biến thể 1–2 (bản 3 lưu ngoài git, không xét).
Chữ thử ngắn (101 ký tự, 2 câu nguyên văn của 2m/2n) để giữ trần 5 000 ký tự gửi. Chọn biến thể ở chon_bien_the.py."""
import base64, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import my_lib as M
L = M.L; H = M.H
TTV = 'eleven_multilingual_ttv_v2'   # như casting-giong (cùng họ với model đọc của kênh)
MO_TA = {
 'A1': "A deep, older American male narrator in his sixties for a cinematic historical documentary. Dramatic yet measured, rich low voice with a slight gravel. Credible and grounded, never a movie-trailer announcer. Clean studio recording.",
 'A2': "An older American man with a deep, resonant voice. Serious war-documentary narrator with controlled intensity, unhurried and grave, General American accent. Not exaggerated, not an advertisement. High quality studio recording.",
}
CHU = 'The thirteenth of September seventeen eighty-two. By the next afternoon, all ten batteries were lost.'
assert 100 <= len(CHU) <= 1000
P = f'{H}/thiet-ke.json'; S = json.load(open(P)) if os.path.exists(P) else {}
os.makedirs(L.OUT, exist_ok=True)
for k, mt in MO_TA.items():
    if k in S: continue
    if M.da_gui() + len(CHU) >= M.CHAN: raise SystemExit('CHẶN trần ký tự')
    r = json.loads(L.call('/v1/text-to-voice/design', dict(voice_description=mt, model_id=TTV, text=CHU, guidance_scale=5, should_enhance=False, seed=18102026)))
    with open(L.LOG, 'a') as fo: fo.write(json.dumps(dict(viec='voice-design', tag=k, model=TTV, ky_tu=len(CHU)), ensure_ascii=False) + '\n')
    bt = []
    for i, p in enumerate(r['previews']):
        f = f'{L.OUT}/thiet-ke-{k}-{i + 1}.mp3'; open(f, 'wb').write(base64.b64decode(p['audio_base_64']))
        bt.append(dict(bien_the=i + 1, generated_voice_id=p['generated_voice_id'], tep=f, giay=p.get('duration_secs'), xet=i < 2))
    S[k] = dict(mo_ta=mt, model=TTV, seed=18102026, guidance_scale=5, chu_thu=CHU, ky_tu=len(CHU), bien_the=bt)
    json.dump(S, open(P, 'w'), ensure_ascii=False, indent=1); print(k, [b['giay'] for b in bt])
