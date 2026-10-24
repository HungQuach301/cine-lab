#!/opt/cine/bin/python
"""GIONG-T4 · kiểm ASR toàn tập T4 (theo reports/kl42/kiem_tap.py), 2 cách nghe như GIỌNG-CHỐT (M = medium.en beam 5, S = small.en beam 1, không hotwords), trên stem thô từng chương.
Theo TỪNG CÂU (mốc từ moc.json, cửa sổ ±0,4 s quanh câu theo dấu thời gian từ của ASR):
 - số/năm: mọi giá trị trong câu khoá (asr.nums_of) phải nghe ra (kiem_lib.num_ok);
 - tên: mục từ điển có trong câu (khớp mờ ≥ 0,75 với chữ viết hoặc alias) + từ viết hoa giữa câu (khớp mờ ≥ 0,75);
 ĐÚNG = cả hai cách nghe; NGHI = một cách; SAI = không cách nào. Câu chưa ĐÚNG được nghe lại TÁCH RIÊNG (±0,3 s);
 mỗi cách nghe tính đạt nếu đạt ở cửa sổ cả chương hoặc ở câu tách (ghi cả hai: muc_ca_chuong, muc). Thêm tỷ lệ từ đúng toàn chương + chỗ lệch.
gl_kiem_tap.py [chương…] → kiem-tap.json (gộp các chương đã kiểm)."""
import difflib, json, re, subprocess, sys, unicodedata
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gl_lib as K
DOAN = {c: [dict(shot=s, khoa=t) for s, t in ss] for c, ss in K.doan()}
sys.path.insert(0, str(K.R / 'reports/casting-giong')); import kiem_lib as KL   # noqa: E402
import asr as A   # noqa: E402
TDM = {d['viet']: d for d in K.td()}; W = 0.6
LA = {'iii': 'the third', 'v': 'the fifth', 'ii': 'the second'}   # ASR viết số hiệu vua bằng chữ La Mã
THUONG = {'the', 'its', 'and', 'but', 'by', 'in', 'on', 'at', 'as', 'for', 'a', 'an', 'it', 'he', 'she', 'they', 'that', 'this', 'from', 'to', 'of', 'our', 'read', 'so', 'we', 'his', 'her', 'their', 'there', 'then', 'now', 'only', 'even', 'every', 'none', 'look', 'today', 'within', 'across', 'around', 'among', 'instead', 'slowly', 'just', 'nineteen', 'sir', 'lord', 'people', 'king', 'city'}


def ten_cau(c):
    out = [v for v in TDM if TDM[v]['loai'] not in ('năm', 'ngày', 'thập niên') and re.search(r'(?<![\w-])' + re.escape(v) + r'(?![\w])', c)]
    cov = ' '.join(out)
    for w in c.split()[1:]:
        x = re.sub(r"[^A-Za-zÀ-ÿ'’-]", '', w).replace('’', "'")
        if x[:1].isupper() and len(x) > 2 and x.lower() not in THUONG and x.replace("'s", '') not in cov: out.append(x.replace("'s", ''))
    return sorted(set(out))


def chuan(h):
    h = re.sub(r'(\d) ,(\d)', r'\1,\2', h)                       # "15 ,000" → "15,000" (cách faster-whisper tách token)
    return re.sub(r'\b(III|II|V)\b', lambda m: LA[m.group(1).lower()], h)


def bo_dau(t): return ''.join(c for c in unicodedata.normalize('NFD', t.lower()) if unicodedata.category(c) != 'Mn')


def ten_ok(t, hyp):
    """khớp mờ ≥ 0,75 (kiem_lib.name_ok, chữ viết hoặc alias) — thêm cách so bỏ dấu + bỏ khoảng trắng/gạch ("fête-à-com-pli" ↔ "fait accompli")"""
    s = KL.name_ok(t, hyp, TDM.get(t, {}).get('doc'))
    if s >= 0.75: return s
    H = re.sub(r'[^a-z]', '', bo_dau(hyp)); best = s
    for c in [t] + ([TDM[t]['doc']] if t in TDM else []):
        a = re.sub(r'[^a-z]', '', bo_dau(c)); n = len(a)
        for k in range(max(1, n - 3), n + 4):
            for i in range(0, max(1, len(H) - k + 1)): best = max(best, difflib.SequenceMatcher(None, a, H[i:i + k]).ratio())
    return round(best, 3)


def cua_so(ws, a, b): return chuan(' '.join(w['w'].strip() for w in ws if w['s'] >= a - W and w['e'] <= b + W))


def kiem_cau(c, hyp):
    so = sorted(A.nums_of(c)); ten = ten_cau(c)
    return dict(so_sai=[v for v in so if not KL.num_ok(v, hyp)], ten_sai=[t for t in ten if ten_ok(t, hyp) < 0.75], so=so, ten=ten)


def asr_cache(wav, name, beam):
    """ASR có cache theo SHA tệp (ngoài git, $KL_OUT/asr/)"""
    import hashlib
    h = hashlib.sha256(open(wav, 'rb').read()).hexdigest()[:16]; p = K.OUT / 'asr' / f'{h}-{name}-b{beam}.json'; p.parent.mkdir(exist_ok=True)
    if p.exists(): return json.loads(p.read_text())
    _, ws = KL.transcribe(wav, name, beam); ws = [dict(w=x.word, s=x.start, e=x.end) for x in ws]; p.write_text(json.dumps(ws)); return ws


if __name__ == '__main__':
    M = json.loads((K.OUT / 'stem/moc.json').read_text()); P = K.G / 'kiem-tap.json'
    R = json.loads(P.read_text()) if P.exists() else dict(ghi='ASR M=medium.en beam5, S=small.en beam1, không hotwords; theo câu ±0,4 s', chuong={})
    want = sys.argv[1:]
    for ch in M['chuong']:
        cid = ch['chuong']
        if want and cid[:2] not in want: continue
        wav = str(K.OUT / 'stem' / f'{cid[:2]}.wav'); khoa = ' '.join(d['khoa'] for d in DOAN[cid]); rc = dict(nghe={}, cau=[])
        res = {}
        for name, beam in KL.NGHE:
            ws = asr_cache(wav, name, beam); txt = ' '.join(x['w'].strip() for x in ws); w = KL.wer(khoa, chuan(txt)); res[name] = ws
            rc['nghe'][name] = dict(asr=txt, tu_dung=w['tu_dung'], loi=w['loi'], so_tu=w['so_tu'], cho_lech=w['cho_lech'])
        for d in ch['doan']:
            for i, c in enumerate(d['cau']):
                kq = {n: kiem_cau(c['khoa'], cua_so(res[n], c['bd'], c['kt'])) for n, _ in KL.NGHE}
                n0, n1 = [n for n, _ in KL.NGHE]
                muc = [('so', v) for v in kq[n0]['so']] + [('ten', t) for t in kq[n0]['ten']]
                tt = {}
                for k, v in muc:
                    bad = [v in kq[n][f'{k}_sai'] for n in (n0, n1)]
                    tt[f'{k}:{v:g}' if k == 'so' else f'{k}:{v}'] = 'SAI' if all(bad) else ('NGHI' if any(bad) else 'DUNG')
                row = dict(shot=d['shot'], i=i, khoa=c['khoa'], bd=c['bd'], kt=c['kt'], muc=tt, nghe={n: cua_so(res[n], c['bd'], c['kt']) for n, _ in KL.NGHE})
                if any(v != 'DUNG' for v in tt.values()):   # nghe lại câu TÁCH RIÊNG (±0,3 s) — ASR cả chương đổi theo ngữ cảnh dù âm thanh câu không đổi
                    clip = str(K.OUT / 'asr' / f"cau-{cid[:2]}-{d['shot']}-{i}.wav")
                    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', wav, '-ss', f"{max(0, c['bd'] - 0.3):.3f}", '-to', f"{c['kt'] + 0.3:.3f}", clip], check=True)
                    kc = {}
                    for n, b in KL.NGHE:
                        h = chuan(' '.join(x['w'].strip() for x in asr_cache(clip, n, b))); kc[n] = dict(asr=h, **kiem_cau(c['khoa'], h))
                    tt2 = {}
                    for k, v in muc:
                        key = f'{k}:{v:g}' if k == 'so' else f'{k}:{v}'
                        bad = [v in kq[n][f'{k}_sai'] and v in kc[n][f'{k}_sai'] for n in (n0, n1)]   # đạt ở cả chương HOẶC câu tách
                        tt2[key] = 'SAI' if all(bad) else ('NGHI' if any(bad) else 'DUNG')
                    row.update(muc_ca_chuong=tt, muc=tt2, nghe_cau_tach={n: v['asr'] for n, v in kc.items()})
                rc['cau'].append(row)
        allm = [s for c in rc['cau'] for s in c['muc'].values()]
        rc['tong'] = dict(muc=len(allm), dung=allm.count('DUNG'), nghi=allm.count('NGHI'), sai=allm.count('SAI'))
        R['chuong'][cid] = rc; json.dump(R, open(P, 'w'), ensure_ascii=False, indent=1)
        print(cid, rc['tong'], {n: v['tu_dung'] for n, v in rc['nghe'].items()}, flush=True)
        for c in rc['cau']:
            bad = {k: v for k, v in c.get('muc_ca_chuong', c['muc']).items() if v != 'DUNG'}
            if bad: print('  ', c['shot'], c['i'], 'cả chương', bad, '→ sau câu tách', {k: c['muc'][k] for k in bad}, '|', c.get('nghe_cau_tach', c['nghe']), flush=True)
