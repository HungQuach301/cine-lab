#!/opt/cine/bin/python
"""GIONG-T4 · khoá lời T4 London (K2C-T4-02) từ LOI-NHAP-v1.md + khoa-loi/sua-v2.json + khoa-loi/doan-shot.json.
Sinh: loi-khoa.txt (khuôn T3: đầu chương [NN NAME], mỗi shot một đoạn, chỉ chữ đọc) · khoa-loi/loi-v2-KHOA.md (kịch bản có mã shot + mã câu Lnn)
· khoa-loi/so-nhap-khoa.json (từng câu: nháp ↔ khoá) · LOI-KHOA.sha256 (khuôn T3; gồm PLS nếu đã có).
Kiểm: câu không có trong sua-v2.json phải GIỮ NGUYÊN chữ nháp; mọi L01–L86 dùng đúng một lần, đúng thứ tự. KHÔNG gọi ElevenLabs.
Dùng: /opt/cine/bin/python -I scripts/k2ldn/giong/lam_loi_khoa.py"""
import hashlib, json, re
from pathlib import Path
R = Path(__file__).resolve().parents[3]; EP = R / 'channel-k2/k2c-t4-02'; KL = EP / 'khoa-loi'
NGAY = '23/10/2026'
md = (EP / 'LOI-NHAP-v1.md').read_text()
NHAP = {m.group(1): re.sub(r'\s*⟦THẺ⟧', '', m.group(2)).strip() for m in re.finditer(r'^\*\*(L\d\d)\*\* (.+)$', md, re.M)}
assert len(NHAP) == 86, len(NHAP)
SUA = {s['L']: s for s in json.loads((KL / 'sua-v2.json').read_text())}
KHOA = {}
for l, t in NHAP.items():
    s = SUA.get(l)
    if s and s.get('tach'):
        assert ' '.join(s['tach']) == t, (l, 'tách phải giữ nguyên chữ')
        for i, c in enumerate(s['tach']): KHOA[l + 'ab'[i]] = c
    else:
        KHOA[l] = s['sau'] if s and s.get('sau') else t
DS = json.loads((KL / 'doan-shot.json').read_text())['chuong']
thu_tu = [c for _, sh in DS for _, cs in sh for c in cs]
assert thu_tu == list(KHOA), 'thứ tự câu lệch'          # dùng đủ, đúng thứ tự, mỗi câu một lần
txt, kb = [], [f'# LỜI KHOÁ v2 — K2C-T4-02 London (GIONG-T4, {NGAY}) — sinh bằng scripts/k2ldn/giong/lam_loi_khoa.py; KHÔNG sửa tay', '',
              '> Mỗi dòng ‹shot› = một đoạn của loi-khoa.txt. {Lnn} = mã câu nháp (LOI-NHAP-v1.md); ✎ = câu đổi/tách (khoa-loi/sua-v2.json).', '']
for ch, shots in DS:
    txt += ['', f'[{ch}]']; kb += ['', f'[{ch}]']
    for shot, cs in shots:
        txt += ['', ' '.join(KHOA[c] for c in cs)]
        kb.append(f'‹{shot}› ' + ' '.join(f'{KHOA[c]} {{{c}{" ✎" if c[:3] in SUA and SUA[c[:3]].get("sau") or len(c) > 3 else ""}}}' for c in cs))
out = '\n'.join(txt).strip() + '\n'
assert '⟦' not in out and '{' not in out
(EP / 'loi-khoa.txt').write_text(out); (KL / 'loi-v2-KHOA.md').write_text('\n'.join(kb) + '\n')
so = [dict(L=l, nhap=NHAP[l], khoa=' '.join(v for k, v in KHOA.items() if k[:3] == l), doi=SUA.get(l, {}).get('ma')) for l in NHAP]
(KL / 'so-nhap-khoa.json').write_text(json.dumps(so, ensure_ascii=False, indent=1) + '\n')
body = '\n'.join(x for x in out.splitlines() if x and not x.startswith('['))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
tep = ['khoa-loi/loi-v2-KHOA.md', 'loi-khoa.txt'] + [str(p.relative_to(EP)) for p in sorted((KL / 'phat-am').glob('*.pls'))]
(EP / 'LOI-KHOA.sha256').write_text(''.join(f'{sha(EP / n)}  {n}\n' for n in tep))
tu = len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’\-]*", body))
print(f'loi-khoa.txt: {tu} từ, {len(body)} ký tự, {sum(1 for x in so if x["doi"])} câu đổi/tách / 86; đoạn {sum(len(s) for _, s in DS)}')
print((EP / 'LOI-KHOA.sha256').read_text())
