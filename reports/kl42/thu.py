#!/opt/cine/bin/python
"""KL42 · bước 3: thu G1 cả tập T3 theo chương. thu.py <chương …|all>   (chương = 00 … 05)
- Mỗi chương tách thành phần ≤ 1 900 ký tự ở ranh giới đoạn (proxy cắt lệnh ElevenLabs dài ~30 s — prep.py K2C-T2), mỗi phần một lệnh (≤ 10 000 ký tự),
  gửi kèm previous_text/next_text trong chương (≤ 900 ký tự mỗi bên), cùng seed 19102026, speed 1,03; alias thay vào chữ (tu-dien.json Đ3 + GC-C).
- Đoạn = một shot ‹id› của script-v4.2-KHOA.md; câu tách theo dấu câu; mốc thời gian lấy từ alignment ký tự của ElevenLabs (tương đối với phần).
- Bộ đếm tài khoản đọc trước/sau MỖI chương (chờ 90 s) → bo-dem.jsonl. Chỉ mục: $KL_OUT/thu/<chương>.json."""
import json, re, sys
import kl_lib as K
PMAX, CTX = 1900, 900
SPLIT = re.compile(r'(?<=[.?!])\s+(?=[A-Z"“‘])|(?<=[.?!]["”’])\s+(?=[A-Z"“‘])')


def cau(t):
    s = SPLIT.split(t); assert ' '.join(s) == t; return s


def phan(ss):
    P, cur = [], []
    for sid, t in ss:
        if cur and len(' '.join(K.alias(x) for _, x in cur + [(sid, t)])) > PMAX: P.append(cur); cur = []
        cur.append((sid, t))
    return P + [cur]


def moc(al, a, b):
    ch, st, en = al['characters'], al['character_start_times_seconds'], al['character_end_times_seconds']
    idx = [i for i in range(a, b) if not ch[i].isspace()]
    return round(st[idx[0]], 3), round(en[idx[-1]], 3)


def thu_chuong(cid, ss):
    P = phan(ss); gtxt = [' '.join(K.alias(t) for _, t in p) for p in P]; rec = dict(chuong=cid, phan=[]); gui = 0
    for i, p in enumerate(P):
        prev = ' '.join(gtxt[:i])[-CTX:] or None; nxt = ' '.join(gtxt[i + 1:])[:CTX] or None
        mp3, al, n = K.tts(gtxt[i], f'{cid}-p{i}', prev, nxt); gui += n
        assert ''.join(al['characters']) == gtxt[i], 'alignment không khớp chữ gửi'
        pos, doan = 0, []
        for sid, t in p:
            cs = cau(t); ga = [K.alias(c) for c in cs]; assert ' '.join(ga) == K.alias(t), (sid, 'alias theo câu ≠ alias theo đoạn')
            a0 = pos; cau_r = []
            for c, g in zip(cs, ga):
                s0, s1 = moc(al, pos, pos + len(g)); cau_r.append(dict(khoa=c, gui=g, bd=s0, kt=s1)); pos += len(g) + 1
            s0, s1 = moc(al, a0, pos - 1); doan.append(dict(shot=sid, khoa=t, bd=s0, kt=s1, cau=cau_r))
        rec['phan'].append(dict(tep=mp3, ky_tu=len(gtxt[i]), ngu_canh_truoc=len(prev or ''), ngu_canh_sau=len(nxt or ''), giay=round(K.dur(mp3), 3), doan=doan))
        print(f'{cid} p{i}: {len(gtxt[i])} ký tự, {len(p)} đoạn, {K.dur(mp3):.1f} s, gửi {n}', flush=True)
    return rec, gui


if __name__ == '__main__':
    C = K.doan_v42(); want = sys.argv[1:]; (K.OUT / 'thu').mkdir(exist_ok=True)
    for cid, ss in C:
        if 'all' not in want and cid[:2] not in want: continue
        c0 = K.counter(); rec, gui = thu_chuong(cid, ss)
        rec['bo_dem'] = K.ghi_bodem(f'chuong {cid}', gui, c0, K.counter(90)) if gui else None
        json.dump(rec, open(K.OUT / 'thu' / f'{cid[:2]}.json', 'w'), ensure_ascii=False, indent=1)
        print(rec['bo_dem'], '· tổng gửi phiên', K.da_gui(), flush=True)
        if K.da_gui() >= K.MOC: print(f'VƯỢT MỐC THEO DÕI {K.MOC}', flush=True)
