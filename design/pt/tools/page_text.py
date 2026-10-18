"""Lấy văn bản nguyên văn của một trang giấy phép (HTML → chữ), ghi kèm URL, mã HTTP, ngày đọc, SHA-256 của HTML gốc.
  python -I page_text.py <url> <out.txt> [chuỗi bắt đầu] [chuỗi kết thúc]"""
import sys, re, html, hashlib, datetime, urllib.request, ssl, os
url, out = sys.argv[1], sys.argv[2]; start = sys.argv[3] if len(sys.argv) > 3 else None; end = sys.argv[4] if len(sys.argv) > 4 else None
ctx = ssl.create_default_context(cafile=os.environ.get('SSL_CERT_FILE') or '/root/.ccr/ca-bundle.crt')
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (cine-lab license check)'})
try:
    r = urllib.request.urlopen(req, timeout=40, context=ctx); code = r.status; raw = r.read()
except urllib.error.HTTPError as e:
    code = e.code; raw = e.read()
t = raw.decode('utf8', 'replace')
if '<' in t[:2000]:
    t = re.sub(r'<script.*?</script>|<style.*?</style>|<noscript.*?</noscript>', '', t, flags=re.S | re.I)
    t = re.sub(r'<br\s*/?>|</p>|</li>|</h\d>|</div>|</tr>', '\n', t, flags=re.I)
    t = html.unescape(re.sub(r'<[^>]+>', '', t))
t = re.sub(r'[ \t]+', ' ', t); t = re.sub(r'\n\s*\n+', '\n', t).strip()
if start and start in t: t = t[t.index(start):]
if end and end in t: t = t[:t.index(end) + len(end)]
hdr = f"URL: {url}\nHTTP: {code}\nĐọc: {datetime.datetime.now(datetime.UTC):%Y-%m-%d %H:%M} UTC (phiên PT)\nSHA-256 HTML gốc: {hashlib.sha256(raw).hexdigest()}\n--- NGUYÊN VĂN (chữ trích từ HTML, không sửa nội dung) ---\n"
open(out, 'w').write(hdr + t + '\n'); print(code, len(t), out)
