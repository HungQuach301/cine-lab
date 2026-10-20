#!/opt/cine/bin/python -I
"""NC-V2V3 · trang dựng TẠM: bản sao design/k2v/tl/page.js của máy V7B (worktree đọc-chỉ, không sửa) + ../v2v/idmask.js (NC-V2V, nguyên văn) + depth.js nối cuối.
   mk_page3.py <worktree V7B> <thư mục ra> → <ra>/page-v2v3.js"""
import hashlib, re, sys
from pathlib import Path
wt, out = Path(sys.argv[1]), Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True); here = Path(__file__).parent
src = (wt / 'design/k2v/tl/page.js').read_text()
s = re.sub(r"from '\./", "from '/k2v/tl/", src).replace("import(`./scenes/", "import(`/k2v/tl/scenes/").replace("import('./export6.js')", "import('/k2v/tl/export6.js')")
s = s.replace('window.ready = true;', '')
s += '\n// ===== NC-V2V idmask.js =====\n' + (here / '../v2v/idmask.js').read_text() + '\n// ===== NC-V2V3 depth.js =====\n' + (here / 'depth.js').read_text() + '\nwindow.ready = true;\n'
(out / 'page-v2v3.js').write_text(s)
print('page.js sha256', hashlib.sha256(src.encode()).hexdigest()[:16], '→', out / 'page-v2v3.js')
