#!/opt/cine/bin/python
"""CASTING-GIỌNG · Voice Design: mỗi mô tả → 1 lần gọi /v1/text-to-voice/design (3 biến thể, cùng chữ thử);
lưu MP3 biến thể ngoài git + thiet-ke.json (mô tả, model, generated_voice_id, ký tự). Chọn biến thể ở chon_bien_the.py."""
import base64, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import cg_lib as L
H = os.path.dirname(os.path.abspath(__file__))
TTV = 'eleven_multilingual_ttv_v2'   # cùng họ với model đọc của kênh (eleven_multilingual_v2)
MO_TA = {
 'A1': "A deep, older British male in his sixties. Measured documentary narrator with a warm gravel in the voice, unhurried pacing and received pronunciation. Close studio microphone, perfect audio quality.",
 'A2': "An older male narrator with a low register, in the style of a BBC historical documentary. Calm authority, precise diction, grave and steady, neutral southern English accent. Clean studio recording.",
 'A3': "A mature man in his late fifties with a deep, resonant mid-Atlantic voice. Thoughtful history documentary storyteller, warm and serious, slight rasp, slow and deliberate delivery. High quality studio recording.",
}
# chữ thử biến thể: 2m + 2n của lời khoá (đã áp alias), 100–1000 ký tự theo API
CHU = json.load(open(f'{H}/doan-thu.json'))['doan'][1]['gui'].split('The thirteenth of September', 1)[1]
CHU = 'The thirteenth of September' + CHU
P = f'{H}/thiet-ke.json'; S = json.load(open(P)) if os.path.exists(P) else {}
for k, mt in MO_TA.items():
    if k in S: continue
    r = json.loads(L.call('/v1/text-to-voice/design', dict(voice_description=mt, model_id=TTV, text=CHU, guidance_scale=5, should_enhance=False, seed=18102026)))
    bt = []
    for i, p in enumerate(r['previews']):
        f = f'{L.OUT}/thiet-ke-{k}-{i + 1}.mp3'; open(f, 'wb').write(base64.b64decode(p['audio_base_64']))
        bt.append(dict(bien_the=i + 1, generated_voice_id=p['generated_voice_id'], tep=f, giay=p.get('duration_secs')))
    S[k] = dict(mo_ta=mt, model=TTV, chu_thu=CHU, ky_tu=len(CHU), bien_the=bt)
    with open(L.LOG, 'a') as fo: fo.write(json.dumps(dict(viec='voice-design', tag=k, model=TTV, ky_tu=len(CHU)), ensure_ascii=False) + '\n')
    json.dump(S, open(P, 'w'), ensure_ascii=False, indent=1); print(k, [b['giay'] for b in bt])
