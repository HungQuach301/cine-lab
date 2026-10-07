#!/opt/cine/bin/python
"""Last Lamplighters · hồ sơ quyền tư liệu phạm vi công cộng (chủ dự án 05/10/2026, mục C3; CHUAN-KENH §9).

  rights_check.py <episode.yaml>      mã thoát 1 nếu thiếu hồ sơ (qc Q19 dùng hàm check)

Mỗi shot `archive` phải có `rid` khớp một dòng bảng tư liệu trong RIGHTS.md:
  - URL nguồn thuộc danh sách trắng: loc.gov (Library of Congress) hoặc tên miền chính phủ Mỹ (*.gov, gồm archives.gov / NARA);
  - tình trạng quyền ghi nguyên văn có "No known restrictions" (LoC) hoặc "public domain" / "U.S. government work" / "17 U.S.C. §105";
  - ngày tải YYYY-MM-DD; tệp ảnh tồn tại trong repo.
Tổng thời lượng shot `archive` ≤ 20 % thời lượng tập (nếu đã có timeline).
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__)); import ll

WL = re.compile(r'https?://([a-z0-9.-]+\.)?(loc\.gov|[a-z0-9-]+\.gov)(/|\b)', re.I)
OKQ = re.compile(r'no known restrictions|public domain|u\.s\. government work|17 u\.s\.c\. ?§ ?105', re.I)


def rows():
    R = {}
    for ln in open(os.path.join(ll.REPO, 'RIGHTS.md')):
        c = [x.strip() for x in ln.strip().strip('|').split('|')]
        if len(c) >= 5 and re.fullmatch(r'[A-Z]+-[\w.-]+', c[0] or ''): R[c[0]] = c
    return R


def check(E, TL=None):
    R, bad, arch = rows(), [], 0.0
    for sg in E.get('segments', []) + E.get('shorts', []):
        for sh in sg.get('shots', []):
            if sh.get('tpl') != 'archive': continue
            p = sh.get('p', {}); rid = p.get('rid'); ctx = f"{sg['id']}/archive"
            if not rid or rid not in R: bad.append(f'{ctx}: thiếu dòng RIGHTS cho rid={rid}'); continue
            c = R[rid]; line = ' | '.join(c)
            if not WL.search(line): bad.append(f'{ctx}: {rid} nguồn ngoài danh sách trắng')
            if not OKQ.search(line): bad.append(f'{ctx}: {rid} không ghi tình trạng quyền hợp lệ')
            if not re.search(r'\b20\d\d-\d\d-\d\d\b', line): bad.append(f'{ctx}: {rid} thiếu ngày tải')
            if not p.get('img') or not os.path.exists(os.path.join(ll.REPO, p['img'])): bad.append(f'{ctx}: không thấy tệp ảnh {p.get("img")}')
            if not p.get('credit'): bad.append(f'{ctx}: thiếu dòng ghi nguồn trên hình (credit)')
    if TL:
        arch = sum(sh['t1'] - sh['t0'] for s in TL['segments'] for sh in s['shots'] if sh['tpl'] == 'archive')
        if TL['tong_s'] and arch / TL['tong_s'] > 0.20: bad.append(f'tư liệu {100 * arch / TL["tong_s"]:.1f} % > 20 % thời lượng')
    return bad, arch


if __name__ == '__main__':
    E = ll.load(sys.argv[1]); tl = os.path.join(E['out'], 'timeline.json')
    b, a = check(E, json.load(open(tl)) if os.path.exists(tl) else None)
    print('\n'.join(b) or f'ĐẠT (tư liệu {a:.1f} s)'); sys.exit(1 if b else 0)
