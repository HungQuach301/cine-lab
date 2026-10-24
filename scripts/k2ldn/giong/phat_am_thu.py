#!/opt/cine/bin/python
"""GIONG-T4 · việc 3: nghe thử tên riêng/địa danh T4 bằng G1 (v2, speed 1,03, seed 19102026) TRƯỚC khi thu cả tập.
Mỗi mục nằm trong một câu mang ngắn; cắt đúng khoảng của mục theo alignment ký tự ElevenLabs → (a) ASR 2 cách nghe như KL42
(M = medium.en beam 5, S = small.en beam 1, không hotwords; cửa sổ ±0,35 s quanh mục) và (b) nhận dạng ÂM VỊ (am_vi.py, IPA) so với IPA chuẩn Anh–Anh.
phat_am_thu.py <lượt> → reports/giong-t4/phat-am/<lượt>.json + bản nghe channel-k2/k2c-t4-02/khoa-loi/phat-am/nghe-<lượt>.mp3 (≤ 5 MB)."""
import difflib, json, re, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent)); import gl_lib as GL   # noqa: E402
sys.path.insert(0, str(GL.R / 'reports/casting-giong')); import kiem_lib as KL   # noqa: E402  (chỉ đọc)
LUOT = json.loads((GL.G / 'phat-am/bo-thu.json').read_text())
VENV = '/var/tmp/cine-out/giong-t4/venv-am-vi/bin/python'


def ipa_sim(h, cands):
    n = lambda s: re.sub(r'[ ˈˌː.ʰ]', '', s).replace('ɚ', 'ə').replace('ɜ', 'ə').replace('ɐ', 'ə').replace('ɾ', 't').replace('ɹ', 'r')
    return round(max(difflib.SequenceMatcher(None, n(c), n(h)).ratio() for c in cands), 3)


def main(luot):
    B = LUOT[luot]; chu = '\n\n'.join(c['cau'] for c in B['cau']); ra = GL.G / 'phat-am'; ra.mkdir(exist_ok=True)
    c0 = GL.counter(); mp3, al, n = GL.tts(chu, f'phat-am-{luot}'); c1 = GL.counter(90 if n else 0)
    if n: print(GL.ghi_bodem(f'phat-am-{luot}', n, c0, c1))
    ch, st, en = al['characters'], al['character_start_times_seconds'], al['character_end_times_seconds']
    assert ''.join(ch) == chu
    muc, pos = [], 0
    for c in B['cau']:
        i0 = chu.index(c['cau'], pos); pos = i0 + len(c['cau'])
        for m in c['muc']:
            j = c['cau'].index(m['chu']) + i0; k = j + len(m['chu']) - 1
            muc.append(dict(m, bd=round(st[j], 3), kt=round(en[k], 3), cau=c['cau']))
    wav = GL.OUT / f'phat-am-{luot}.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', mp3, '-ac', '1', '-ar', '16000', str(wav)], check=True)
    vao = [dict(id=f"{i:02d}", wav=str(wav), bd=max(0, m['bd'] - 0.06), kt=m['kt'] + 0.10) for i, m in enumerate(muc)]
    (GL.OUT / f'am-vi-{luot}-vao.json').write_text(json.dumps(vao))
    subprocess.run([VENV, str(Path(__file__).parent / 'am_vi.py'), str(GL.OUT / f'am-vi-{luot}-vao.json'), str(GL.OUT / f'am-vi-{luot}-ra.json')], check=True,
                   stdout=subprocess.DEVNULL)
    ipa = {x['id']: x['ipa'] for x in json.loads((GL.OUT / f'am-vi-{luot}-ra.json').read_text())}
    nghe = {name: KL.transcribe(mp3, name, beam)[1] for name, beam in KL.NGHE}
    for i, m in enumerate(muc):
        m['ipa_nghe'] = ipa[f'{i:02d}']; m['ipa_diem'] = ipa_sim(m['ipa_nghe'], m['ipa'])
        for name, ws in nghe.items():
            h = ' '.join(w.word.strip() for w in ws if w.start >= m['bd'] - 0.35 and w.end <= m['kt'] + 0.35)
            m[f'asr_{name}'] = h; m[f'diem_{name}'] = round(KL.name_ok(m['ten'], h, m.get('alias')), 3)
    out = dict(luot=luot, chu_gui=chu, ky_tu=len(chu), tep=mp3, giay=round(GL.dur(mp3), 2), muc=muc)
    (ra / f'{luot}.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
    nghe_mp3 = GL.EP / 'khoa-loi/phat-am' / f'nghe-{luot}.mp3'; nghe_mp3.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', mp3, '-ac', '1', '-b:a', '96k', str(nghe_mp3)], check=True)
    for m in muc:
        print(f"{m['ma']:<14} {m['chu']:<22} IPA {m['ipa_nghe']:<28} ({m['ipa_diem']:.2f} vs {m['ipa'][0]})  M:{m['asr_medium.en'][:30]:<30} S:{m['asr_small.en'][:30]}")


if __name__ == '__main__':
    main(sys.argv[1])
