#!/opt/cine/bin/python
"""ÂM THANH · đo tỉ lệ đọc đúng trước/sau từ điển phát âm bằng ASR (phiên Âm thanh, Mốc C, 15/10/2026).

  asr_phat_am.py run [--cau scripts/audio/cau-kho.yaml] [--out /var/tmp/cine-out/am-thanh/asr] [--takes 2] [--dry]
  asr_phat_am.py rescore [--out …]       → chấm lại từ bản ASR đã lưu (sau khi sửa luật chấm/cau-kho.yaml; không thu, không nghe lại)
      --dry: chỉ in số ký tự sẽ gửi ElevenLabs (không gọi API).

Mỗi câu thu 2 bản bằng đúng giọng T1/T2 (Eric cjVigY5qzO86Huf0OWal, eleven_multilingual_v2, stability 0,5, similarity 0,75):
  TRƯỚC = nguyên văn lời; SAU = phat_am.apply(lời). Cache theo băm (giọng + chữ gửi) → chạy lại không tốn ký tự.
Nghe lại bằng faster-whisper 2 cách (BAI-HOC-LL #86): medium.en beam 5 và small.en beam 1 (tham lam).
Câu nào từ điển ĐỔI chữ thì thu --takes lượt mỗi bản (ElevenLabs không tất định). Một lượt ĐÚNG khi mọi số (so theo giá trị, scripts/ll/asr.py nums_of) có trong bản ASR và mọi tên ("ten") khớp mờ ≥ 0,75
(so với cụm cùng số từ giống nhất trong bản ASR, sau khi bỏ dấu và gạch nối) — ở CẢ HAI cách nghe.
Giới hạn: ASR đo "nghe ra đúng chữ", không đo "đọc đúng giọng bản ngữ" (tên Hàn): phần đó cần tai người (docs/AUDIO-THUOC-DO.md).
"""
import base64, difflib, hashlib, json, os, re, sys, time, urllib.request
import yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'll'))
import lib, phat_am

VOICE = dict(id='cjVigY5qzO86Huf0OWal', model='eleven_multilingual_v2', stability=0.5, similarity=0.75)


def arg(k, d=None):
    return sys.argv[sys.argv.index('--' + k) + 1] if '--' + k in sys.argv else d


def key_of(text, take=0, voice=VOICE):
    return hashlib.sha1(json.dumps([text, voice] + ([take] if take else []), sort_keys=True).encode()).hexdigest()[:16]


def tts(text, out, take=0, voice=VOICE):
    p = os.path.join(out, key_of(text, take, voice) + '.mp3')
    if os.path.exists(p): return p, 0
    body = dict(text=text, model_id=voice['model'], voice_settings=dict(stability=voice['stability'], similarity_boost=voice['similarity'], speed=1.0))
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{voice['id']}?output_format=mp3_44100_128", data=json.dumps(body).encode(),
                                 headers={'Content-Type': 'application/json', 'Accept': 'audio/mpeg'})
    open(p, 'wb').write(urllib.request.urlopen(req, timeout=300).read()); open(p[:-4] + '.txt', 'w').write(text + '\n')
    return p, len(text)


def nrm(s):
    return re.sub(r'[^a-z0-9 ]', ' ', s.lower().replace('-', ' ')).split()


def name_ok(name, hyp):
    a = ' '.join(nrm(name)); H = nrm(hyp); n = len(a.split()); best = 0.0
    for k in (n - 1, n, n + 1):
        if k < 1: continue
        for i in range(0, max(1, len(H) - k + 1)):
            best = max(best, difflib.SequenceMatcher(None, a, ' '.join(H[i:i + k])).ratio())
    return round(best, 3)


def judge(item, hyp):
    import asr as A   # scripts/ll/asr.py
    # ASR viết "15 and a half" bằng chữ số → nums_of chỉ thấy 15: đổi về giá trị trước khi so (lỗi của bộ chấm, không phải của TTS)
    hyp2 = re.sub(r'(\d+) and a half', lambda m: str(int(m.group(1)) + 0.5), hyp)
    want = A.nums_of(item['text']); got = A.nums_of(hyp2)
    miss_n = sorted(x for x in want if x not in got)
    names = {n: max([name_ok(n, hyp)] + [name_ok(h, hyp) for h in (item.get('dong_am') or {}).get(n, [])]) for n in item.get('ten', [])}
    miss_t = [n for n, r in names.items() if r < 0.75]
    # "five hundred won": ASR không phân biệt "won" với "one" (ra "501") — câu đánh dấu mo_ho_asr chấm bằng tai người, không tính vào tỉ lệ máy
    return dict(ok=not miss_n and not miss_t, thieu_so=miss_n, thieu_ten=miss_t, ten=names, mo_ho_asr=bool(item.get('mo_ho_asr')), so_can=len(want), ten_can=len(names))


def summary(rows, M):
    may = [r for r in rows if not r['mo_ho_asr']]; tok = {}
    for side in ('truoc', 'sau'):
        so = [0, 0]; ten = [0, 0]
        for r in may:
            for L in r[side]['luot']:
                for mk in M:
                    x = L[mk]; so[0] += x['so_can'] - len(x['thieu_so']); so[1] += x['so_can']; ten[0] += x['ten_can'] - len(x['thieu_ten']); ten[1] += x['ten_can']
        tok[side] = dict(so_dung=f'{so[0]}/{so[1]}', ten_dung=f'{ten[0]}/{ten[1]}')
    for r in rows:
        for side in ('truoc', 'sau'): r[side]['ok_moi_luot'] = all(L['ok'] for L in r[side]['luot']); r[side]['dung'] = sum(L['ok'] for L in r[side]['luot']); r[side]['so_luot'] = len(r[side]['luot'])
    return dict(so_cau=len(rows), so_cau_cham_may=len(may), cau_doi_chu=sum(1 for r in may if not r['giong_nhau']),
                cau_dung_moi_luot=dict(truoc=sum(r['truoc']['ok_moi_luot'] for r in may), sau=sum(r['sau']['ok_moi_luot'] for r in may)),
                luot_doc_dung=dict(truoc=f"{sum(r['truoc']['dung'] for r in may)}/{sum(r['truoc']['so_luot'] for r in may)}", sau=f"{sum(r['sau']['dung'] for r in may)}/{sum(r['sau']['so_luot'] for r in may)}"),
                tu_khoa_x_2_cach_nghe=tok)


def rescore(out):
    C = {c['id']: c for c in yaml.safe_load(open(arg('cau', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cau-kho.yaml'))))}
    p = os.path.join(out, 'asr-phat-am.json'); S = json.load(open(p)); M = ('medium.en/b5', 'small.en/b1')
    for r in S['cau']:
        c = C[r['id']]; r['mo_ho_asr'] = bool(c.get('mo_ho_asr'))
        for side in ('truoc', 'sau'):
            for L in r[side]['luot']:
                for mk in M: L[mk] = dict(asr=L[mk]['asr'], **judge(c, L[mk]['asr']))
                L['ok'] = all(L[mk]['ok'] for mk in M)
    S.update(summary(S['cau'], M)); S['cham_lai_utc'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()); json.dump(S, open(p, 'w'), ensure_ascii=False, indent=1)
    for r in S['cau']: print(f"{r['id']}: trước {r['truoc']['dung']}/{r['truoc']['so_luot']} · sau {r['sau']['dung']}/{r['sau']['so_luot']}{'  (mơ hồ ASR)' if r['mo_ho_asr'] else ''}")
    print(json.dumps({k: S[k] for k in ('so_cau', 'so_cau_cham_may', 'cau_doi_chu', 'cau_dung_moi_luot', 'luot_doc_dung', 'tu_khoa_x_2_cach_nghe')}, ensure_ascii=False))


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == 'rescore': return rescore(arg('out', '/var/tmp/cine-out/am-thanh/asr'))
    if len(sys.argv) < 2 or sys.argv[1] != 'run': sys.exit(__doc__)
    C = yaml.safe_load(open(arg('cau', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cau-kho.yaml'))))
    out = arg('out', '/var/tmp/cine-out/am-thanh/asr'); os.makedirs(out, exist_ok=True)
    pairs = [(c, c['text'], phat_am.apply(c['text'])) for c in C]; T = int(arg('takes', 2))
    # lượt 2 trở đi chỉ cho câu mà từ điển ĐỔI chữ (nơi so trước/sau có nghĩa); ElevenLabs không tất định nên một lượt là ít
    jobs = [(c, side, txt, k) for c, a, b in pairs for k in range(T if a != b else 1) for side, txt in (('truoc', a), ('sau', b))]
    need = sum(len(t) for t in {(txt, k): txt for c, side, txt, k in jobs if not os.path.exists(os.path.join(out, key_of(txt, k) + '.mp3'))}.values())
    print(f'ký tự sẽ gửi ElevenLabs (chưa có cache): {need}')
    if '--dry' in sys.argv: return
    from faster_whisper import WhisperModel
    M = {'medium.en/b5': (WhisperModel('medium.en', device='cpu', compute_type='int8'), 5), 'small.en/b1': (WhisperModel('small.en', device='cpu', compute_type='int8'), 1)}
    sent = 0; R = {c['id']: dict(id=c['id'], truoc=dict(text=a, luot=[]), sau=dict(text=b, luot=[]), giong_nhau=a == b, mo_ho_asr=bool(c.get('mo_ho_asr'))) for c, a, b in pairs}
    asr_cache = {}
    for c, side, txt, k in jobs:
        p, n = tts(txt, out, k); sent += n; L = dict(mp3=p, sha256=lib.sha256(p), luot=k)
        if p not in asr_cache:
            asr_cache[p] = {}
            for mk, (m, beam) in M.items():
                segs, _ = m.transcribe(lib.dec(p, 1, sr=16000)[:, 0].astype('float32'), beam_size=beam, language='en', condition_on_previous_text=False)
                asr_cache[p][mk] = ' '.join(s.text.strip() for s in segs)
        for mk in M: L[mk] = dict(asr=asr_cache[p][mk], **judge(c, asr_cache[p][mk]))
        L['ok'] = all(L[mk]['ok'] for mk in M); R[c['id']][side]['luot'].append(L)
    rows = list(R.values())
    S = dict(utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), giong=VOICE, ky_tu_gui_lan_nay=sent, **summary(rows, M), cau=rows)
    for r in rows: print(f"{r['id']}: trước {r['truoc']['dung']}/{r['truoc']['so_luot']} · sau {r['sau']['dung']}/{r['sau']['so_luot']}{'  (mơ hồ ASR)' if r['mo_ho_asr'] else ''}", flush=True)
    json.dump(S, open(os.path.join(out, 'asr-phat-am.json'), 'w'), ensure_ascii=False, indent=1)
    print(json.dumps({k: S[k] for k in ('so_cau', 'so_cau_cham_may', 'cau_doi_chu', 'ky_tu_gui_lan_nay', 'cau_dung_moi_luot', 'luot_doc_dung', 'tu_khoa_x_2_cach_nghe')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
