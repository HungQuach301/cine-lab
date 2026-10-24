#!/opt/cine/bin/python
"""GIONG-T4 · tải một trang nguồn (HTML/PDF), lưu bản chữ + SHA-256 của tệp gốc để trích nguyên văn kiểm được.
   tai_nguon.py <mã> <url>  → reports/giong-t4/nguon/<mã>.txt (dòng đầu: URL, ngày đọc UTC, SHA gốc, cỡ)
   Gốc HTML/PDF để ngoài git ở /var/tmp/cine-out/giong-t4/nguon/ (tái tạo = chạy lại lệnh; trang có thể đã đổi → so SHA)."""
import sys, os, re, hashlib, subprocess, datetime, html
from html.parser import HTMLParser
UA = "CineLab-research (+https://github.com/HungQuach301/cine-lab)"
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
GOC = "/var/tmp/cine-out/giong-t4/nguon"; RA = os.path.join(REPO, "reports/giong-t4/nguon")

class T(HTMLParser):
    BO = {"script", "style", "noscript", "svg", "head"}
    KHOI = {"p", "div", "li", "h1", "h2", "h3", "h4", "h5", "tr", "br", "section", "article", "blockquote", "td", "dd", "dt", "figcaption"}
    def __init__(s): super().__init__(); s.o = []; s.bo = 0
    def handle_starttag(s, t, a):
        if t in s.BO: s.bo += 1
        if t in s.KHOI: s.o.append("\n")
    def handle_endtag(s, t):
        if t in s.BO and s.bo: s.bo -= 1
        if t in s.KHOI: s.o.append("\n")
    def handle_data(s, d):
        if not s.bo: s.o.append(d)

def main(ma, url):
    os.makedirs(GOC, exist_ok=True); os.makedirs(RA, exist_ok=True)
    goc = os.path.join(GOC, ma + ".bin")
    r = subprocess.run(["curl", "-sS", "-L", "--max-time", "60", "-A", UA, "-o", goc, "-w", "%{http_code} %{content_type}", url],
                       capture_output=True, text=True)
    code, _, ct = r.stdout.partition(" ")
    if code != "200": sys.exit(f"{ma}: HTTP {code} {r.stderr.strip()}")
    b = open(goc, "rb").read(); sha = hashlib.sha256(b).hexdigest()
    if b[:4] == b"%PDF":
        chu = subprocess.run(["pdftotext", "-layout", goc, "-"], capture_output=True, text=True).stdout
    else:
        p = T(); p.feed(b.decode("utf-8", "replace")); chu = html.unescape("".join(p.o))
        chu = re.sub(r"[ \t\r\f\v]+", " ", chu); chu = re.sub(r"\n\s*\n+", "\n\n", chu)
    chu = re.sub(r"[\w.+-]+@[\w-]+(\.[\w-]+)+", "[email đã che]", chu)   # che email (luật phiên); SHA gốc vẫn là của tệp tải về
    ngay = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    with open(os.path.join(RA, ma + ".txt"), "w") as f:
        f.write(f"# {url}\n# đọc {ngay} · SHA-256 gốc {sha} · {len(b)} byte · {ct}\n\n{chu.strip()}\n")
    print(f"{ma}: {len(b)} byte sha {sha[:12]} → reports/giong-t4/nguon/{ma}.txt ({len(chu)} ký tự)")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
