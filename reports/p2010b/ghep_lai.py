#!/opt/cine/bin/python
"""P-2010b · việc 1 bước 3: ghép lại stem lời KL42 từ audio lịch sử ElevenLabs bằng CHÍNH reports/kl42/ghep.py (chuong(), ghep_cau(), cùng hằng số).
Lịch sử không trả alignment → căn mốc lại:
 (1) mốc câu trong chương (sau ghép) = số đo KL42 đã ghi trong git (kiem-tap.json `cau`, trùng nhip-that.json 129/129 câu — cả hai sinh từ moc.json gốc);
 (2) mốc tương đối trong phần = mốc chương − dời của phần (sh = st − off; off do trim() của ghep.py tính trên audio tải về);
 (3) hai ẩn số sổ KL42 không giữ, suy từ bản xem MP3 gốc trong git (reports/kl42/nghe/T3-loi-G1-v42-xem-{1,2}-*.mp3, cắt từ master gốc)
     bằng độ trễ theo MẪU (tích vô hướng, tìm ±10 ms) so với độ trễ của phần 1 cùng chương (độ trễ chung = limiter + giải mã MP3):
     (a) vị trí đặt phần 2 (chương 02, 05) — ghep.py tính từ alignment ký tự đầu phần 2: chọn mốc đầu phần (lưới 1 ms như moc() của thu.py) cho lệch = 0;
     (b) độ dài câu CŨ của 3 câu thay (chương 01) — ghep_cau() cắt theo nó: chỉnh (lưới 1 ms) tới khi đoạn sau câu thay lệch = đoạn trong câu thay;
     mốc trước ghép câu suy ngược bằng lặp chuong() tới khi mốc sau ghép = số KL42 (≤ 0,5 ms).
Chương cách 2,0 s như ghep.py. → $P_OUT/stem/{NN}.wav, T3-loi-tho.wav, moc.json; reports/p2010b/ghep-lai.json"""
import json, os, sys
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; R = H.parents[1]; PO = Path(os.environ.get('P_OUT', '/var/tmp/cine-out/p2010b'))
os.environ['KL_OUT'] = str(PO / 'kl'); sys.path.insert(0, str(R / 'reports/kl42'))
import kl_lib as K  # noqa: E402
import thu  # noqa: E402
import ghep as G  # noqa: E402
SR = G.SR; LS = PO / 'lich-su'; ST = PO / 'stem'; ST.mkdir(parents=True, exist_ok=True)
KT = json.loads((R / 'reports/kl42/kiem-tap.json').read_text())['chuong']
NT = json.loads((R / 'reports/kl42/nhip-that.json').read_text())
T0 = {s['ban_thu']['chuong']: round(s['ban_thu']['bd_stem'] - s['ban_thu']['bd_chuong'], 3) for s in NT['shot'] if 'ban_thu' in s}
XM = json.loads((R / 'reports/kl42/xuat.json').read_text())['ban_xem']
REF = [(G.mono(str(R / x['tep'])), x['tu']) for x in XM]


def ref_of(t_stem): return REF[0] if t_stem < REF[1][1] else REF[1]


def tre(x, t0, t, n=2.5, w=int(0.6 * SR)):
    """độ trễ (mẫu, nội suy parabol) của bản xem gốc so với x[t, t+n] (x = chương, đặt ở t0 trong stem gốc): ref[j + tre] ≈ x[j];
    tương quan chéo chuẩn hoá (FFT) trong ±w mẫu; kèm hệ số tương quan"""
    n = max(n, 0.8); assert int(t * SR) < len(x) - SR, (t, len(x) / SR); xr, tu = ref_of(t0 + t); a = x[int(t * SR):int((t + n) * SR)].astype(np.float64); j = int(round((t0 + t - tu) * SR))
    b = xr[max(0, j - w):j + w + len(a)].astype(np.float64); w0 = j - max(0, j - w)
    L = 1 << int(np.ceil(np.log2(len(a) + len(b)))); c = np.fft.irfft(np.fft.rfft(b, L) * np.conj(np.fft.rfft(a, L)), L)[:len(b) - len(a) + 1]
    e = np.sqrt(np.convolve(b ** 2, np.ones(len(a)), 'valid')) * np.sqrt((a ** 2).sum()); r = c / np.maximum(e, 1e-12); k = int(np.argmax(r))
    d = 0.0 if k in (0, len(r) - 1) else 0.5 * (r[k - 1] - r[k + 1]) / (r[k - 1] - 2 * r[k] + r[k + 1])
    return round(k - w0 + d, 2), round(float(r[k]), 4)


flat = lambda dd: [c for d in dd for c in d['cau']]
THAY = [dict(t, tep=str(LS / f"01-thay-{t['shot']}-{t['i']}.mp3")) for t in json.loads((R / 'reports/kl42/thay.json').read_text())]
# thử nghiệm (P-2010b, ghi trong báo cáo): CAT_1I0 = số mẫu giữ của tệp câu thay 1i#0 (bản gốc nghi ngắn hơn bản lịch sử); DUR0 = độ dài câu cũ 1i#0 ban đầu
if os.environ.get('CAT_1I0'):
    t = [t for t in THAY if t['chon'] and t['shot'] == '1i' and t['i'] == 0][0]; yy = G.mono(t['tep'])[:int(os.environ['CAT_1I0'])]
    t['tep'] = str(PO / f"thay-1i0-cat{os.environ['CAT_1I0']}.wav"); G.lib.write(t['tep'], yy[:, None], codec='pcm_f32le')
CHI = os.environ.get('CHI_CHUONG')
G.THAY = THAY; out = dict(ghi=__doc__.splitlines()[0], chuong=[]); full = np.zeros(0, np.float32); M = dict(chuong=[], gap_chuong=G.GAP_CH, sr=SR)
for cid, ss in K.doan_v42():
    if CHI and cid[:2] != CHI: continue
    P = thu.phan(ss); cau_kl = KT[cid]['cau']; t0 = T0[cid]; k = 0; tgt_p = []; rep = dict(chuong=cid, t0_stem=t0, phan=[])
    for i, p in enumerate(P):   # mốc chương (sau ghép) của từng phần, theo đúng cách tách phần/câu của thu.py
        doan = []
        for sid, t in p:
            cs = thu.cau(t); cc = cau_kl[k:k + len(cs)]; k += len(cs)
            assert [c['shot'] for c in cc] == [sid] * len(cs) and [c['khoa'] for c in cc] == cs, (cid, sid)
            doan.append(dict(shot=sid, khoa=t, cau=[dict(khoa=c['khoa'], bd=c['bd'], kt=c['kt']) for c in cc]))
        tep = str(LS / f"{cid.replace(' ', '-')}-p{i}.mp3"); y, off = G.trim(G.mono(tep)); tgt_p.append((tep, doan, off, len(y)))
    assert k == len(cau_kl)
    gaps = [b['cau'][0]['bd'] - a['cau'][-1]['kt'] for _, dn, _, _ in tgt_p for a, b in zip(dn, dn[1:])]; g = float(np.median(gaps))
    r0 = [None] + [None] * (len(tgt_p) - 1)   # mốc alignment đầu phần 2 (giây, trong tệp phần) — ẩn số (a)

    def dung_rec(r0):
        phan = []
        for i, (tep, dn, off, ny) in enumerate(tgt_p):
            if i == 0: sh = -off
            else: sh = dn[0]['cau'][0]['bd'] - r0[i]
            q = lambda v: round(v - sh, 3)   # mốc alignment nằm trên lưới 1 ms (moc() của thu.py làm tròn 3 số lẻ)
            phan.append(dict(tep=tep, doan=[dict(shot=d['shot'], khoa=d['khoa'], bd=q(d['cau'][0]['bd']), kt=q(d['cau'][-1]['kt']),
                                                 cau=[dict(khoa=c['khoa'], bd=q(c['bd']), kt=q(c['kt'])) for c in d['cau']]) for d in dn]))
        return dict(chuong=cid, phan=phan)
    for i in range(1, len(tgt_p)):   # ước đầu cho (a): đo vị trí phần 2 bằng độ trễ mẫu so với phần 1, với r0 giả định rồi sửa
        r0[i] = tgt_p[i][2] + 0.08
    TH = [(t['shot'], t['i'], t['kt'] - t['bd']) for t in THAY if t['chon'] and t['chuong'] == cid[:2]]
    idx = {(c['shot'], c['i']): j for j, c in enumerate(cau_kl)}; dur_cu = {(s_, i_): (float(os.environ['DUR0']) if (s_, i_) == ('1i', 0) and os.environ.get('DUR0') else d_) for s_, i_, d_ in TH}; vong = []
    rec = dung_rec(r0); tgt = [(c['bd'], c['kt']) for c in cau_kl]
    for ngoai in range(10):
        ALL = lambda: sum([flat(q['doan']) for q in rec['phan']], [])
        for it in range(12):   # lặp mốc trước ghép câu (chỉ chương có câu thay mới cần > 1 vòng)
            for (s_, i_), d_ in dur_cu.items(): cr = ALL()[idx[(s_, i_)]]; cr['kt'] = cr['bd'] + d_
            x, dd, _ = G.chuong(json.loads(json.dumps(rec)))
            got = [(c['bd'], c['kt']) for c in flat(dd)]; err = max(max(abs(a - c), abs(b - d)) for (a, b), (c, d) in zip(got, tgt))
            if err <= 0.0005 or len(tgt_p) > 1: break
            for (a, b), (c, d), cr in zip(got, tgt, ALL()): cr['bd'] -= a - c; cr['kt'] -= b - d
        c0 = cau_kl[0]; base = tre(x, t0, c0['bd'] + 0.2, min(2.5, c0['kt'] - c0['bd'] - 0.3)); sua = dict(tre_phan1=base, phan=[], thay=[])
        doi = False
        for i in range(1, len(tgt_p)):   # (a)
            c = tgt_p[i][1][0]['cau'][0]; l = tre(x, t0, c['bd'] + 0.2, min(2.5, c['kt'] - c['bd'] - 0.3)); dl = l[0] - base[0]
            sua['phan'].append(dict(phan=i, tre=l, lech_mau=round(dl, 2), r0=round(r0[i], 4)))
            if abs(dl) >= 0.5: r0[i] = round(r0[i] - dl / SR, 3) if ngoai else r0[i] - dl / SR; doi = True
            elif ngoai == 0 or round(r0[i], 3) != r0[i]: r0[i] = round(r0[i], 3); doi = True
        for s_, i_, _ in TH:   # (b)
            j = idx[(s_, i_)]; c, nx = cau_kl[j], cau_kl[j + 1]
            lA = tre(x, t0, c['bd'] + 0.3, min(2.5, c['kt'] - c['bd'] - 0.6)); lB = tre(x, t0, nx['bd'] + 0.2, min(2.5, nx['kt'] - nx['bd'] - 0.3))
            dl = lB[0] - lA[0]; sua['thay'].append(dict(cau=f'{s_}#{i_}', tre_trong=lA, tre_sau=lB, lech_mau=round(dl, 2), dur_cu=round(dur_cu[(s_, i_)], 4)))
            if abs(dl) >= 0.5: dur_cu[(s_, i_)] = round(dur_cu[(s_, i_)] - dl / SR, 3); doi = True
        vong.append(sua)
        if not doi: break
        if len(tgt_p) > 1: rec = dung_rec(r0)
    rep.update(vong_can=vong, lap_ngoai=ngoai + 1, lech_moc_max=round(err, 4), giay=round(len(x) / SR, 3), ngung_noi=round(g, 3),
               r0_phan2=[round(v, 4) for v in r0[1:]], dur_cu={f'{a}#{b}': v for (a, b), v in dur_cu.items()},
               phan=[dict(tep=Path(t).name, off=round(o, 5), giay_trim=round(n / SR, 3)) for t, _, o, n in tgt_p])
    json.dump(rec, open(ST / f'rec-{cid[:2]}.json', 'w'), ensure_ascii=False, indent=1)
    G.lib.write(str(ST / f'{cid[:2]}.wav'), x[:, None]); ts = len(full) / SR + (G.GAP_CH if len(full) else 0.0)
    full = np.concatenate([full, np.zeros(int(round((ts - len(full) / SR) * SR)), np.float32), x])
    M['chuong'].append(dict(chuong=cid, bd_stem=round(ts, 3), giay=round(len(x) / SR, 3), ngung_noi=round(g, 3), so_phan=len(tgt_p),
                            doan=[dict(d, bd_stem=round(d['bd'] + ts, 3), kt_stem=round(d['kt'] + ts, 3)) for d in dd]))
    rep.update(bd_stem=round(ts, 3), lech_t0_stem=round(ts - t0, 3)); out['chuong'].append(rep)
    print(cid, rep['giay'], 's · vòng', rep['lap_ngoai'], '· lệch mốc', rep['lech_moc_max'], '· r0', rep['r0_phan2'], '· dur_cu', rep['dur_cu'],
          '· cuối', json.dumps(vong[-1], ensure_ascii=False)[:300], flush=True)
G.lib.write(str(ST / 'T3-loi-tho.wav'), full[:, None]); M['giay_stem'] = round(len(full) / SR, 3)
json.dump(M, open(ST / 'moc.json', 'w'), ensure_ascii=False, indent=1)
out.update(giay_stem=M['giay_stem'], giay_stem_kl42=NT['stem_giay'], lech_s=round(M['giay_stem'] - NT['stem_giay'], 3), stem_sha256=G.lib.sha256(str(ST / 'T3-loi-tho.wav')),
           stem_sha256_kl42=json.loads((R / 'reports/kl42/xuat.json').read_text())['nguon_tho']['sha256'])
json.dump(out, open(H / 'ghep-lai.json', 'w'), ensure_ascii=False, indent=1)
print('stem', out['giay_stem'], 's; KL42', out['giay_stem_kl42'], '; lệch', out['lech_s'], 's; SHA', out['stem_sha256'][:16], 'KL42', out['stem_sha256_kl42'][:16])
