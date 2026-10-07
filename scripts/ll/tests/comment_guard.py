#!/opt/cine/bin/python
"""Chặn lỗi BAI-HOC #70/#76: chú thích (`//` trong JS, `#` trong Python) chèn giữa dòng nuốt mất mã phía sau.
Báo mọi dòng có chú thích mà phần chú thích chứa mã trông như câu lệnh (gọi hoặc gán có dấu chấm, kết thúc bằng `;`; với Python: `: x.append(`)."""
import re, sys, glob
bad = []
for f in glob.glob('design/ll-hero/*.js') + glob.glob('scripts/ll/*.js') + glob.glob('scripts/ll/lib/*.js'):
    for i, l in enumerate(open(f, encoding='utf-8'), 1):
        m = re.search(r'(?<![:"\'/])//(.*)$', l)
        if m and re.search(r'\b[A-Za-z_]\w*(\.\w+)+\s*(\([^()]*\)|=\s*[^;=]+);', m.group(1)): bad.append(f'{f}:{i}')
for f in glob.glob('scripts/ll/*.py'):
    for i, l in enumerate(open(f, encoding='utf-8'), 1):
        m = re.search(r'\s#\s(.*)$', l)
        if m and re.search(r':\s*[a-z_][\w.]*\.(append|extend|add)\(', m.group(1)): bad.append(f'{f}:{i}')
print('\n'.join(bad) or 'không có chú thích nuốt mã'); sys.exit(1 if bad else 0)
