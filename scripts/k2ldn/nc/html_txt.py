"""NC-T4: HTML → văn bản thuần để trích nguyên văn (dùng: python -I html_txt.py vao.html ra.txt)."""
import sys, re, html
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(s): super().__init__(); s.o=[]; s.skip=0
    def handle_starttag(s,t,a):
        if t in('script','style','noscript','svg'): s.skip+=1
        if t in('p','br','div','li','h1','h2','h3','h4','tr','section'): s.o.append('\n')
    def handle_endtag(s,t):
        if t in('script','style','noscript','svg') and s.skip: s.skip-=1
    def handle_data(s,d):
        if not s.skip: s.o.append(d)
t=open(sys.argv[1],encoding='utf-8',errors='replace').read()
p=P(); p.feed(t); x=html.unescape(''.join(p.o))
x=re.sub(r'[ \t\r\f\v]+',' ',x); x=re.sub(r'\n\s*\n+','\n',x)
x=re.sub(r'[\w.+-]+@[\w-]+\.[\w.]+','[email-đã-che]',x)
open(sys.argv[2],'w').write(x.strip()+'\n')
