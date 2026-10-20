"""NC-GPU · máy chủ tệp + chạy lệnh TỐI THIỂU trên pod RunPod (chỉ thư viện chuẩn Python), sau proxy HTTPS của RunPod (https://<pod>-8888.proxy.runpod.net).
Không khoá dịch vụ nào lên pod: chỉ một mã ngẫu nhiên dùng một lần (biến môi trường TOK, sinh tại máy điều khiển khi tạo pod) để chặn người lạ.
  PUT  /f/<đường>?off=<byte>      ghi khúc (≤ 64 MB/khúc, qua giới hạn thân yêu cầu của proxy) vào /w/<đường> tại vị trí off
  GET  /f/<đường>[?off=&n=]       đọc (cả tệp hoặc một khúc)
  GET  /sha/<đường>               SHA-256 + cỡ
  POST /run  (thân = lệnh bash)   chạy nền → {id}; GET /log/<id>?tail=N → {xong, ma, log}
  GET  /ls/<thư mục>              liệt kê
Khởi động (dockerStartCmd): python3 -c "import os,base64;exec(base64.b64decode(os.environ['SRV']))" """
import os, sys, json, hashlib, subprocess, threading, urllib.parse
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
TOK = os.environ.get('TOK', ''); ROOT = '/w'; os.makedirs(ROOT, exist_ok=True); JOBS = {}

def safe(p):
    q = os.path.normpath(os.path.join(ROOT, urllib.parse.unquote(p)))
    if not q.startswith(ROOT): raise ValueError('đường ngoài /w')
    return q

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def ok(self, code=200, body=b'', ctype='application/json'):
        self.send_response(code); self.send_header('Content-Type', ctype); self.send_header('Content-Length', str(len(body))); self.end_headers(); self.wfile.write(body)
    def auth(self):
        if not TOK or self.headers.get('X-Tok') != TOK: self.ok(403, b'{"loi":"tok"}'); return False
        return True
    def parts(self):
        u = urllib.parse.urlparse(self.path); return u.path, dict(urllib.parse.parse_qsl(u.query))
    def do_GET(self):
        p, q = self.parts()
        if p == '/ping': return self.ok(200, b'{"ok":1}')
        if not self.auth(): return
        try:
            if p.startswith('/f/'):
                f = safe(p[3:]); off = int(q.get('off', 0)); n = int(q.get('n', os.path.getsize(f) - off))
                with open(f, 'rb') as fh: fh.seek(off); b = fh.read(n)
                return self.ok(200, b, 'application/octet-stream')
            if p.startswith('/sha/'):
                f = safe(p[5:]); h = hashlib.sha256()
                with open(f, 'rb') as fh:
                    for c in iter(lambda: fh.read(1 << 22), b''): h.update(c)
                return self.ok(200, json.dumps({'sha': h.hexdigest(), 'n': os.path.getsize(f)}).encode())
            if p.startswith('/ls/'):
                d = safe(p[4:]); out = []
                for r, _, fs in os.walk(d):
                    for x in fs: fp = os.path.join(r, x); out.append([os.path.relpath(fp, d), os.path.getsize(fp)])
                return self.ok(200, json.dumps(out).encode())
            if p.startswith('/log/'):
                j = JOBS[p[5:]]; t = int(q.get('tail', 4000)); lg = open(j['log'], 'rb').read()[-t:].decode('utf-8', 'replace')
                return self.ok(200, json.dumps({'xong': j['p'].poll() is not None, 'ma': j['p'].poll(), 'log': lg}).encode())
        except Exception as e: return self.ok(500, json.dumps({'loi': repr(e)}).encode())
        self.ok(404, b'{}')
    def do_PUT(self):
        p, q = self.parts()
        if not self.auth(): return
        try:
            f = safe(p[3:]); os.makedirs(os.path.dirname(f), exist_ok=True); n = int(self.headers['Content-Length']); off = int(q.get('off', 0))
            mode = 'r+b' if os.path.exists(f) and off > 0 else 'wb'
            with open(f, mode) as fh:
                fh.seek(off); left = n
                while left:
                    b = self.rfile.read(min(left, 1 << 20))
                    if not b: break
                    fh.write(b); left -= len(b)
            self.ok(200, json.dumps({'n': n - left}).encode())
        except Exception as e: self.ok(500, json.dumps({'loi': repr(e)}).encode())
    def do_POST(self):
        p, q = self.parts()
        if not self.auth(): return
        if p == '/run':
            cmd = self.rfile.read(int(self.headers['Content-Length'])).decode(); jid = str(len(JOBS)); lg = f'{ROOT}/job{jid}.log'
            JOBS[jid] = {'p': subprocess.Popen(['bash', '-c', cmd], stdout=open(lg, 'wb'), stderr=subprocess.STDOUT, cwd=ROOT), 'log': lg}
            return self.ok(200, json.dumps({'id': jid}).encode())
        self.ok(404, b'{}')

ThreadingHTTPServer(('0.0.0.0', 8888), H).serve_forever()
