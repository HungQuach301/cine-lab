"""Cine Lab · M2.1 ANIMATIC NHỊP — lời dẫn nháp bằng flite, quy về tốc độ giọng Bill (141,2 từ/phút), dựng dòng thời gian shot.
Nguồn: src/KICH-BAN-TAP-THU-V2.md (dòng '> ' = lời dẫn), src/BANG-SHOT-M2.md (78 shot; cột "Lời đầu shot").
Quy tắc nhịp:
 - Mỗi câu đọc riêng bằng flite (giọng kal16). Trong một đoạn: nghỉ 0,30 s giữa câu, 0,60 s giữa đoạn văn, đuôi đoạn 0,80 s.
 - Hệ số atempo của đoạn chọn sao cho (số từ) / (thời lượng phần lời, gồm nghỉ giữa câu) = 141,2 từ/phút (mức 1,00);
   mức 1,05: lời nhanh thêm 1,05 lần (≈ 148 từ/phút), các khoảng lặng kịch bản giữ nguyên.
 - Khoảng lặng kịch bản giữ nguyên: VO vào trễ "+2 s"/"+3 s"; shot "—" (thoại Ida L1/L2, nhịp lặng 10-04/10-05, 10-09, 10-10) giữ thời lượng bảng shot;
   14-03: Ida L1 xa rồi mới vào lời.
 - Shot có trích lời bắt đầu đúng ở câu đó; shot "(tiếp)" chia khoảng giữa hai mốc theo tỉ lệ thời lượng bảng shot.
python3 design/m3/animatic/nhip.py <thư mục ra>   → nhip.json (câu, đoạn, 4 phương án, shot), wav từng câu
"""
import json, os, re, subprocess, sys
import numpy as np, soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
WPM, SR = 141.2, 16000
G_SENT, G_PARA, G_TAIL = 0.30, 0.60, 0.80
IDA_L = {'L1': 2.2, 'L2': 2.9}   # thời lượng take (đo lại khi dựng âm)

def sentences(line):
    out, cur = [], ''
    for tok in line.split(' '):
        cur = (cur + ' ' + tok).strip()
        if re.search(r'[.!?:]$', tok) and not re.fullmatch(r'(?:[A-Z]\.)+', tok) and not tok.endswith('U.S.'):
            out.append(cur); cur = ''
    if cur: out.append(cur)
    return [s for s in out if re.search(r'[A-Za-z0-9]', s)]

def parse_script():
    segs, cur = [], None
    for ln in open(f'{HERE}/src/KICH-BAN-TAP-THU-V2.md', encoding='utf-8'):
        m = re.match(r'### (\d\d) · \[([^\]]+)\]', ln)
        if m: cur = None if 'bỏ' in m.group(2) else {'id': m.group(1), 'tag': m.group(2), 'paras': []}; segs.append(cur) if cur else None; continue
        if ln.startswith('## '): cur = None
        if cur is not None and ln.startswith('> '):
            t = ln[2:].strip()
            if t.startswith('*('): continue      # (beat, no narration) — nhịp lặng do shot "—" giữ
            cur['paras'].append(sentences(t.replace('*', '')))
    return segs

def parse_shots():
    rows = []
    for ln in open(f'{HERE}/src/BANG-SHOT-M2.md', encoding='utf-8'):
        c = [x.strip() for x in ln.split('|')]
        if len(c) < 10: continue
        m = re.search(r'(\d\d-\d\d)', c[1])
        if not m or not re.match(r'\d+–\d+', c[4]): continue
        rows.append({'id': m.group(1), 'seg': c[2], 'label': c[3], 'size': c[5], 'src': c[6], 'line': c[7], 'note': c[8], 'dur0': float(c[9]) if re.match(r'^\d', c[9]) else None,
                     'cat07': '[CẮT-07]' in c[1]})
    for r in rows:
        a, b = map(float, re.match(r'(\d+)–(\d+)', [x for x in open(f'{HERE}/src/BANG-SHOT-M2.md', encoding='utf-8') if r['id'] in x and '|' in x][0].split('|')[4].strip()).groups())
        r['dur0'] = b - a
    return rows

def flite(text, path):
    tf = path + '.txt'; open(tf, 'w').write(text)
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'flite=textfile={tf}:voice=kal16', '-ar', str(SR), '-ac', '1', path], check=True)
    y, _ = sf.read(path); nz = np.where(np.abs(y) > 0.01)[0]
    y = y[max(0, nz[0] - 160): nz[-1] + 160] if len(nz) else y; sf.write(path, y, SR); return len(y) / SR

def nwords(s): return len([w for w in re.split(r'\s+', s) if re.search(r'[A-Za-z0-9]', w)])

def norm(s): return re.sub(r'[^a-z0-9 ]', '', s.lower().replace('’', "'")).split()

def build(out):
    os.makedirs(out, exist_ok=True); segs = parse_script(); shots = parse_shots()
    k = 0
    for sg in segs:
        sg['sent'] = []
        for pi, para in enumerate(sg['paras']):
            for si, s in enumerate(para):
                p = f'{out}/c{k:03d}.wav'; d = flite(s, p); k += 1
                sg['sent'].append({'text': s, 'words': nwords(s), 'flite_s': round(d, 3), 'wav': os.path.basename(p), 'gap': G_TAIL if (pi == len(sg['paras']) - 1 and si == len(para) - 1) else (G_PARA if si == len(para) - 1 else G_SENT)})
        W = sum(x['words'] for x in sg['sent']); gaps = sum(x['gap'] for x in sg['sent'][:-1])
        target = W / WPM * 60.0                              # thời lượng phần lời (gồm nghỉ giữa câu) ở 141,2 từ/phút
        sg['words'] = W; sg['tempo'] = round(sum(x['flite_s'] for x in sg['sent']) / (target - gaps), 4)
        sg['flite_wpm'] = round(W / ((sum(x['flite_s'] for x in sg['sent']) + gaps) / 60), 1)
    plans = {}
    for lv in (1.00, 1.05):
        for cut in (False, True):
            tl = timeline(segs, shots, lv, cut); plans[f'{lv:.2f}{"-cat07" if cut else ""}'] = {'total_s': round(tl['total'], 2), 'segs': tl['segs']}
    json.dump({'wpm': WPM, 'segs': segs, 'shots': shots, 'plans': plans}, open(f'{out}/nhip.json', 'w'), ensure_ascii=False, indent=1)
    for k_, v in plans.items(): print(k_, v['total_s'], f"{int(v['total_s'] // 60)}:{v['total_s'] % 60:05.2f}")

def timeline(segs, shots, lv, cut07, detail=False):
    """trả tổng + bảng đoạn; detail=True: thêm mốc từng câu (vo) và từng shot"""
    T, vo, shot_out, seg_out = 0.0, [], [], {}
    for sg in segs:
        if cut07 and sg['id'] == '07': continue
        t0 = T; sl = [s for s in shots if s['seg'] == sg['id']]; ss = sg['sent']; ptr = 0; last = [-1]
        dur = lambda x: x['flite_s'] / sg['tempo'] / lv
        def anchor(s):
            m = re.findall(r'"([^"]+)"', s['line'])
            if not m or s['line'].startswith('(tiếp)') or s['line'].startswith('—'): return None
            q = norm(m[-1].strip('…').strip())[:4]
            for j in range(max(ptr, last[0] + 1), len(ss)):
                a_ = norm(ss[j]['text']); n_ = min(len(a_), len(q))
                if n_ >= 2 and a_[:n_] == q[:n_]: return j   # câu ngắn ('Forty thousand.') khớp tiền tố
            for j in range(max(ptr, last[0] + 1), len(ss)):
                if ' '.join(q) in ' '.join(norm(ss[j]['text'])): return j
            return None
        starts = []                       # (shot, t_start) cho shot có mốc / cố định; shot (tiếp) gán sau
        for i, s in enumerate(sl):
            fixed = s['line'].startswith('—')
            j = None if fixed else anchor(s)
            pre = 0.0; mm = re.search(r'\(\+(\d+) s\)|\+(\d+) s\)', s['line'])
            if mm: pre = float(mm.group(1) or mm.group(2))
            if 'IDA L1 off' in s['line']: pre = IDA_L['L1'] + 0.8
            if fixed:
                nxt = next((anchor(x) for x in sl[i + 1:] if not x['line'].startswith('—') and anchor(x) is not None), len(ss))
                while ptr < nxt: vo.append((T, ss[ptr])); T += dur(ss[ptr]) + ss[ptr]['gap']; ptr += 1
                starts.append((s, T, 'fixed')); T += s['dur0']
            elif j is not None:
                while ptr < j: vo.append((T, ss[ptr])); T += dur(ss[ptr]) + ss[ptr]['gap']; ptr += 1
                starts.append((s, T, 'anchor')); T += pre; last[0] = j
            else: starts.append((s, None, 'tiep'))
        while ptr < len(ss): vo.append((T, ss[ptr])); T += dur(ss[ptr]) + ss[ptr]['gap']; ptr += 1
        if starts and starts[0][1] is None: starts[0] = (starts[0][0], t0, 'anchor')
        # (tiếp): chia khoảng giữa hai mốc theo thời lượng bảng shot
        i = 0; res = []
        while i < len(starts):
            s, ts, kind = starts[i]; grp = [s]; j = i + 1
            while j < len(starts) and starts[j][2] == 'tiep': grp.append(starts[j][0]); j += 1
            te = starts[j][1] if j < len(starts) else T
            tot = sum(x['dur0'] for x in grp); t = ts
            for x in grp: d = (te - ts) * x['dur0'] / tot; res.append({'id': x['id'], 't0': round(t, 3), 't1': round(t + d, 3), 'kind': kind if x is s else 'tiep'}); t += d
            i = j
        shot_out += res; seg_out[sg['id']] = {'t0': round(t0, 2), 't1': round(T, 2), 'dur': round(T - t0, 2), 'words': sg['words'], 'tempo': round(sg['tempo'] * lv, 4)}
    r = {'total': T, 'segs': seg_out}
    if detail: r['vo'] = [{'t': round(t, 3), 'wav': x['wav'], 'text': x['text'], 'dur': None} for t, x in vo]; r['shots'] = shot_out
    return r

if __name__ == '__main__':
    build(sys.argv[1])
