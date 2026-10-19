#!/opt/cine/bin/python -I
"""NC-V2V · tạo trang dựng mặt nạ ID TẠM: bản sao design/k2v/tl/page.js của máy V7B (đọc từ worktree tạm, không sửa) + idmask.js nối cuối.
   mk_page.py <worktree V7B> <thư mục ra> → <ra>/page-id.js (import trỏ về /k2v/tl/…)."""
import hashlib, re, sys
from pathlib import Path
wt, out = Path(sys.argv[1]), Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
src = (wt / 'design/k2v/tl/page.js').read_text()
s = re.sub(r"from '\./", "from '/k2v/tl/", src).replace("import(`./scenes/", "import(`/k2v/tl/scenes/").replace("import('./export6.js')", "import('/k2v/tl/export6.js')")
s = s.replace('window.ready = true;', '')
s += '\n// ===== NC-V2V idmask.js =====\n' + (Path(__file__).parent / 'idmask.js').read_text() + '\nwindow.ready = true;\n'
(out / 'page-id.js').write_text(s)
print('page.js sha256', hashlib.sha256(src.encode()).hexdigest()[:16], '→', out / 'page-id.js')
