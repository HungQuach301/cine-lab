#!/opt/cine/bin/python
"""NỀN TẢNG · quét trước commit/push (gọi qua tools/preflight.sh; phiên Nền tảng 15/10/2026).

  preflight_scan.py --staged                 # tệp đang stage (hook pre-commit)
  preflight_scan.py --range <base>..<head>   # tệp đổi trong khoảng commit (hook pre-push, kiểm tay trước khi đẩy)
  preflight_scan.py --all                    # mọi tệp git theo dõi (kiểm định kỳ; chậm hơn)

Mục kiểm (CHẶN = mã thoát 1; BÁO = in ra, không chặn):
  (P1, P2, P4: chỉ dòng THÊM MỚI trong khoảng mới CHẶN; nội dung có sẵn trong tệp đổi → BÁO. --all: mọi nội dung → CHẶN.)
  P1 CHẶN  email trong nội dung tệp (trừ noreply@anthropic.com, *@users.noreply.github.com, example.*) và trong tác giả/người commit
  P2 CHẶN  khoá bí mật: sk-ant-…, AKIA…, ghp_/gho_/github_pat_…, hf_…, xi-api-key: <giá trị>, khối PRIVATE KEY, biến *_API_KEY=/…TOKEN= có giá trị
  P3 CHẶN  tệp > 5 MB không phải con trỏ LFS; con trỏ LFS ngoài vùng LFS cho phép (tools/lfs-allow.txt)
  P4 CHẶN  dấu xung đột merge (<<<<<<< , >>>>>>> , ======= đứng một dòng) trong tệp văn bản
  P5 CHẶN  mỗi dòng SOURCES-FOOTAGE.csv / SOURCES-NGOAI-SO.csv đổi trong khoảng phải có tệp giấy phép: đường dẫn licenses/… ghi trong cột
           giay_phep tồn tại, hoặc licenses/<clip_id viết thường>.txt cạnh sổ (licenses/… nằm trong URL không tính là đường dẫn)
  P6 BÁO   ảnh mới (jpg/png/tif/webp) ở vùng tư liệu (assets/, */photo/, */nguon/, */footage/, design/k2v/cutouts/ ảnh gốc) mà SHA-256 hoặc
           tên tệp không xuất hiện trong RIGHTS.md, SOURCES-*.csv, licenses/*.txt hay sổ *.json cùng tập
(lock.py --verify chạy trong tools/preflight.sh.)"""
import csv, fnmatch, hashlib, io, os, re, subprocess, sys

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
MAXB = 5 * 1024 * 1024
EMAIL = re.compile(rb'[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)*\.[A-Za-z]{2,}')
EMAIL_OK = re.compile(rb'^(noreply@anthropic\.com|.*@users\.noreply\.github\.com|.*@example\.(com|org|net)|git@github\.com)$', re.I)
SECRETS = [(n, re.compile(p)) for n, p in [
    ('Anthropic', rb'sk-ant-[A-Za-z0-9_\-]{20,}'), ('AWS', rb'AKIA[0-9A-Z]{16}'), ('GitHub', rb'(ghp|gho|ghs|ghu)_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}'),
    ('HuggingFace', rb'\bhf_[A-Za-z0-9]{30,}'), ('ElevenLabs header', rb'(?i)xi-api-key["\']?\s*[:=]\s*["\']?[A-Za-z0-9_\-]{20,}'),
    ('Khoá riêng', rb'-----BEGIN (RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----'),
    ('Biến khoá có giá trị', rb'(?im)^\s*(export\s+)?[A-Z0-9_]*(API_KEY|SECRET|TOKEN)\s*=\s*["\']?[A-Za-z0-9_\-/+]{16,}')]]
FAKE = re.compile(rb'(?i)SELFTEST|KHOA-GIA|EXAMPLE|xxxxxxxx|<[a-z_]+>')   # khoá giả trong bộ tự kiểm/ví dụ
CONFLICT = re.compile(rb'^(<{7} |>{7} |={7}$)', re.M)
TEXT_EXT = {'.md', '.py', '.js', '.json', '.yaml', '.yml', '.txt', '.csv', '.sh', '.srt', '.html', '.css', '.toml', '.cfg', '.fountain', ''}
IMG_EXT = {'.jpg', '.jpeg', '.png', '.tif', '.tiff', '.webp'}
SRC_ZONES = ['assets/*', '*/photo/*', '*/nguon/*', '*/footage/*']
SELF_MADE = ['*to-khung*', '*kiem-mu/*', '*/khung/*', '*sheet*', '*thumb*', '*/nen-*', '*/stickers/*', '*-mask.png', '*-bg.jpg', 'design/*/cong*', 'reports/*']


def git(*a, binary=False):
    r = subprocess.run(['git', *a], cwd=REPO, capture_output=True)
    return r.stdout if binary else r.stdout.decode('utf-8', 'replace')


def changed(mode, rng):
    if mode == 'staged': out = git('diff', '--cached', '--name-only', '--diff-filter=ACMR')
    elif mode == 'range': out = git('diff', '--name-only', '--diff-filter=ACMR', rng)
    else: out = git('ls-files')
    return [f for f in out.splitlines() if f]


def blob(mode, rng, f):
    if mode == 'staged': return git('show', f':{f}', binary=True)
    if mode == 'range': return git('show', f'{rng.split("..")[-1] or "HEAD"}:{f}', binary=True)
    p = os.path.join(REPO, f); return open(p, 'rb').read() if os.path.isfile(p) else b''


def added(mode, rng, f):
    """dòng THÊM MỚI của tệp trong khoảng (để nội dung có sẵn trên tệp dùng chung không chặn nhầm phiên khác; có sẵn → BÁO)."""
    if mode == 'all': return None
    d = git('diff', '-U0', '--no-color', *(['--cached'] if mode == 'staged' else [rng]), '--', f, binary=True)
    return b'\n'.join(l[1:] for l in d.split(b'\n') if l.startswith(b'+') and not l.startswith(b'+++'))


# P5: đường dẫn licenses/… đứng riêng (đầu ô, sau khoảng trắng/dấu câu, hoặc ./licenses/…); KHÔNG bắt licenses/… nằm trong URL
# (vd http://creativecommons.org/licenses/publicdomain/ của archive.org) — trước đây URL bị coi là tệp giấy phép và chặn nhầm (V5a, 15/10).
LIC_REF = re.compile(r'(?<![\w/.:\-])(?:\./)?(licenses/[\w.\-]+)')


def license_refs(cell): return LIC_REF.findall(cell)


def is_lfs_ptr(b): return b.startswith(b'version https://git-lfs.github.com/spec/v1')


def lfs_allow():
    p = os.path.join(REPO, 'tools', 'lfs-allow.txt')
    return [l.strip() for l in open(p, encoding='utf-8') if l.strip() and not l.startswith('#')] if os.path.exists(p) else []


def main():
    a = sys.argv[1:]; mode = 'staged' if '--staged' in a else 'range' if '--range' in a else 'all' if '--all' in a else 'staged'
    rng = a[a.index('--range') + 1] if mode == 'range' else None
    files = changed(mode, rng); block, warn = [], []
    if mode == 'range':
        for e in sorted(set(git('log', '--format=%ae%n%ce', rng).split())):
            if not EMAIL_OK.match(e.encode()): block.append(f'P1 email tác giả/người commit trong {rng}: {e}')
    allow = lfs_allow(); known = None
    for f in files:
        b = blob(mode, rng, f); ext = os.path.splitext(f)[1].lower()
        if f.startswith('checks/') and mode != 'all': pass   # vẫn quét (email/khoá), chỉ phiên K sửa checks/
        ptr = is_lfs_ptr(b)
        if ptr:
            if not any(fnmatch.fnmatch(f, g) for g in allow): block.append(f'P3 con trỏ LFS ngoài vùng cho phép (tools/lfs-allow.txt): {f}')
        elif len(b) > MAXB: block.append(f'P3 tệp {len(b) / 1048576:.1f} MB > 5 MB không qua LFS: {f}')
        if ptr or (ext not in TEXT_EXT) or len(b) > MAXB: continue
        ad = added(mode, rng, f); new = b if ad is None else ad
        def hit(where, msg):   # dòng mới → CHẶN; chỉ có trong nội dung sẵn có → BÁO
            (block if where else warn).append(msg if where else msg + ' (nội dung có sẵn, không do khoảng này thêm)')
        for m in set(EMAIL.findall(b)):
            if not EMAIL_OK.match(m): hit(m in new, f'P1 email trong {f}: {m.decode(errors="replace")}')
        for n, rx in SECRETS:
            real = lambda t: any(not FAKE.search(m.group(0)) for m in rx.finditer(t))
            if real(b): hit(real(new), f'P2 nghi khoá bí mật ({n}) trong {f}')
        if CONFLICT.search(b) and not f.endswith('preflight_scan.py'): hit(bool(CONFLICT.search(new)), f'P4 dấu xung đột merge trong {f}')
        if os.path.basename(f) in ('SOURCES-FOOTAGE.csv', 'SOURCES-NGOAI-SO.csv'):
            d = os.path.dirname(f)
            for row in csv.DictReader(io.StringIO(b.decode('utf-8', 'replace'))):
                cid = (row.get('clip_id') or row.get('id') or '').strip()
                if not cid: continue
                refs = license_refs(row.get('giay_phep', '') or '')
                cand = [os.path.join(d, r) for r in refs] or [os.path.join(d, 'licenses', cid.lower() + '.txt')]
                if not any(os.path.exists(os.path.join(REPO, c)) for c in cand):
                    block.append(f'P5 thiếu tệp giấy phép cho {cid} ({f}): cần {cand[0]}')
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext not in IMG_EXT or not any(fnmatch.fnmatch(f, g) for g in SRC_ZONES) or any(fnmatch.fnmatch(f, g) for g in SELF_MADE): continue
        if known is None:
            parts = []
            for g in ['RIGHTS.md'] + [x for x in git('ls-files').splitlines() if re.search(r'(SOURCES-[\w-]+\.csv|licenses/.*\.txt|\.json)$', x) and not x.startswith('checks/')]:
                p = os.path.join(REPO, g)
                if os.path.isfile(p) and os.path.getsize(p) < 4 * MAXB: parts.append(open(p, 'rb').read())
            known = b'\n'.join(parts)
        b = blob(mode, rng, f); sha = hashlib.sha256(b).hexdigest().encode(); stem = os.path.splitext(os.path.basename(f))[0].encode()
        if sha not in known and sha[:8] not in known and stem not in known: warn.append(f'P6 ảnh tư liệu chưa thấy trong RIGHTS/SOURCES/licenses/sổ: {f}')
    for x in warn: print('BÁO ', x)
    for x in block: print('CHẶN', x)
    print(f'preflight: {len(files)} tệp ({mode}{" " + rng if rng else ""}) — ' + ('ĐẠT' if not block else f'TRƯỢT ({len(block)} mục chặn)') + (f', {len(warn)} mục báo' if warn else ''))
    sys.exit(1 if block else 0)


if __name__ == '__main__':
    main()
