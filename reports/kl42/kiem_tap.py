#!/opt/cine/bin/python
"""KL42 · kiểm ASR toàn tập, 2 cách nghe như GIỌNG-CHỐT (M = medium.en beam 5, S = small.en beam 1, không hotwords), trên stem thô từng chương.
Theo TỪNG CÂU (mốc từ moc.json, cửa sổ ±0,4 s quanh câu theo dấu thời gian từ của ASR):
 - số/năm: mọi giá trị trong câu khoá (asr.nums_of) phải nghe ra (kiem_lib.num_ok);
 - tên: mục từ điển có trong câu (khớp mờ ≥ 0,75 với chữ viết hoặc alias) + từ viết hoa giữa câu (khớp mờ ≥ 0,75);
 ĐÚNG = cả hai cách nghe; NGHI = một cách; SAI = không cách nào. Thêm tỷ lệ từ đúng toàn chương + chỗ lệch.
kiem_tap.py [chương…] → kiem-tap.json (gộp các chương đã kiểm)."""
import json, re, sys
import kl_lib as K
sys.path.insert(0, str(K.R / 'reports/casting-giong')); import kiem_lib as KL   # noqa: E402
import asr as A   # noqa: E402
TDM = {d['viet']: d for d in K.TD}; W = 0.4
THUONG = {'the', 'its', 'and', 'but', 'by', 'in', 'on', 'at', 'as', 'for', 'a', 'an', 'it', 'he', 'she', 'they', 'that', 'this', 'from', 'to', 'of', 'our', 'read'}


def ten_cau(c):
    out = [v for v in TDM if TDM[v]['loai'] not in ('năm', 'ngày') and re.search(r'(?<![\w-])' + re.escape(v) + r'(?![\w])', c)]
    cov = ' '.join(out)
    for w in c.split()[1:]:
        x = re.sub(r"[^A-Za-zÀ-ÿ'’-]", '', w).replace('’', "'")
        if x[:1].isupper() and len(x) > 2 and x.lower() not in THUONG and x.replace("'s", '') not in cov: out.append(x.replace("'s", ''))
    return sorted(set(out))


def cua_so(ws, a, b): return ' '.join(w.word.strip() for w in ws if w.start >= a - W and w.end <= b + W)


def kiem_cau(c, hyp):
    so = sorted(A.nums_of(c)); ten = ten_cau(c)
    return dict(so_sai=[v for v in so if not KL.num_ok(v, hyp)], ten_sai=[t for t in ten if KL.name_ok(t, hyp, TDM.get(t, {}).get('doc')) < 0.75], so=so, ten=ten)


if __name__ == '__main__':
    M = json.loads((K.OUT / 'stem/moc.json').read_text()); P = K.H / 'kiem-tap.json'
    R = json.loads(P.read_text()) if P.exists() else dict(ghi='ASR M=medium.en beam5, S=small.en beam1, không hotwords; theo câu ±0,4 s', chuong={})
    want = sys.argv[1:]
    for ch in M['chuong']:
        cid = ch['chuong']
        if want and cid[:2] not in want: continue
        wav = str(K.OUT / 'stem' / f'{cid[:2]}.wav'); khoa = ' '.join(d['khoa'] for d in K.doan_v42_dict()[cid]); rc = dict(nghe={}, cau=[])
        res = {}
        for name, beam in KL.NGHE:
            txt, ws = KL.transcribe(wav, name, beam); w = KL.wer(khoa, txt); res[name] = ws
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
                rc['cau'].append(dict(shot=d['shot'], i=i, khoa=c['khoa'], bd=c['bd'], kt=c['kt'], muc=tt, nghe={n: cua_so(res[n], c['bd'], c['kt']) for n, _ in KL.NGHE}))
        allm = [s for c in rc['cau'] for s in c['muc'].values()]
        rc['tong'] = dict(muc=len(allm), dung=allm.count('DUNG'), nghi=allm.count('NGHI'), sai=allm.count('SAI'))
        R['chuong'][cid] = rc; json.dump(R, open(P, 'w'), ensure_ascii=False, indent=1)
        print(cid, rc['tong'], {n: v['tu_dung'] for n, v in rc['nghe'].items()}, flush=True)
        for c in rc['cau']:
            bad = {k: v for k, v in c['muc'].items() if v != 'DUNG'}
            if bad: print('  ', c['shot'], c['i'], bad, '|', c['nghe'], flush=True)
