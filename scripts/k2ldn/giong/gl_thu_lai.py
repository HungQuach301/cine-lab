#!/opt/cine/bin/python
"""GIONG-T4 · thu lại RIÊNG một câu (theo reports/kl42/thu_lai.py; ≤ 2 lượt/câu theo lệnh) (BIBLE §10.1: mục ASR sai → thu lại câu đó). gl_thu_lai.py <NN chương> <shot> <câu i> <seed>
Gửi đúng câu đó (alias thay vào chữ), kèm previous_text/next_text là lời chương trước/sau câu (≤ 900 ký tự), seed khác bản gốc, cùng speed/model.
ASR 2 cách nghe trên bản thu lại; ghi vào thay.json (chon=false — chọn bằng cờ --chon sau khi so). gl_ghep.py ghép đè câu đã chọn."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gl_lib as K
from gl_thu import moc
import gl_kiem_tap as KT
cid, shot, i, seed = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
ALT = sys.argv[5].split('=>') if len(sys.argv) > 5 else None   # thử alias khác: 'iss-muss=>issmus' (thay trong chữ gửi + ngữ cảnh)
alt = (lambda t: t.replace(ALT[0], ALT[1]) if t else t) if ALT else (lambda t: t)
rec = json.loads((K.OUT / 'thu' / f'{cid}.json').read_text())
cs = [(d['shot'], j, c) for p in rec['phan'] for d in p['doan'] for j, c in enumerate(d['cau'])]
k = [n for n, (s, j, _) in enumerate(cs) if s == shot and j == i]; assert len(k) == 1; k = k[0]
c = cs[k][2]; gui = alt(c['gui']); prev = alt(' '.join(x[2]['gui'] for x in cs[:k]))[-900:] or None; nxt = alt(' '.join(x[2]['gui'] for x in cs[k + 1:]))[:900] or None
c0 = K.counter(); mp3, al, n = K.tts(gui, f'thu-lai {cid} {shot}#{i} seed {seed}' + (f' alias {ALT[1]}' if ALT else ''), prev, nxt, seed=seed)
bd, kt = moc(al, 0, len(gui))
nghe = {}
for name, beam in KT.KL.NGHE:
    ws = KT.asr_cache(mp3, name, beam); h = KT.chuan(' '.join(w['w'].strip() for w in ws)); nghe[name] = dict(asr=h, **KT.kiem_cau(c['khoa'], h))
T = json.loads((K.G / 'thay.json').read_text()) if (K.G / 'thay.json').exists() else []
T.append(dict(chuong=cid, shot=shot, i=i, khoa=c['khoa'], gui=gui, alias_thu=ALT, seed=seed, tep=mp3, bd=bd, kt=kt, ky_tu=n, nghe=nghe, chon=False))
json.dump(T, open(K.G / 'thay.json', 'w'), ensure_ascii=False, indent=1)
if n: print(K.ghi_bodem(f'thu lại {cid} {shot}#{i}', n, c0, K.counter(90)))
print(json.dumps(T[-1], ensure_ascii=False, indent=1))
