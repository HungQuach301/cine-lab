"""Dựng trang nghe chấm mù (một file HTML tự chứa, audio nhúng base64): reports/m0/NGHE-CHAM-M0.html"""
import base64, json, os
HERE = os.path.dirname(os.path.abspath(__file__)); M0 = os.path.join(HERE, '..')
key = json.load(open(os.path.join(HERE, 'blind-key.json')))
def src(code):
    p = key[code]; p = os.path.join(HERE, p) if p.startswith('takes/') else os.path.join(M0, p)
    return 'data:audio/mpeg;base64,' + base64.b64encode(open(p, 'rb').read()).decode()
LINE = "That's the last one, then. Goodnight, old street. Forty years, every single night. You'll be brighter now. Just don't forget how warm we were."
KID = "Please, could you light the old one? The new ones hurt my eyes."
def card(code, kind):
    q = ('<label><input type="radio" name="{c}-b" value="tin"> Tin được</label>'
         '<label><input type="radio" name="{c}-b" value="khong"> Không tin</label>') if kind != 'M' else \
        ('<label><input type="radio" name="{c}-b" value="dung"> Đúng "buồn lặng, có hy vọng"</label>'
         '<label><input type="radio" name="{c}-b" value="sai"> Không đúng</label>')
    return f'''<div class="card" data-code="{code}"><div class="code">{code}</div>
<audio controls preload="none" src="{src(code)}"></audio>
<div class="row">{q.format(c=code)}</div>
<div class="row">Điểm 1–5: {''.join(f'<label><input type="radio" name="{code}-s" value="{i}">{i}</label>' for i in range(1,6))}</div>
<input class="note" name="{code}-n" placeholder="Ghi chú (tuỳ chọn)"></div>'''
body = ''.join(card(c, 'A') for c in key if c.startswith('A'))
kid = ''.join(card(c, 'B') for c in key if c.startswith('B'))
mus = ''.join(card(c, 'M') for c in key if c.startswith('M'))
html = f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Nghe chấm M0</title><style>
:root{{--bg:#faf8f5;--fg:#1d1a17;--mut:#6b645c;--card:#fff;--bd:#e3ddd5;--acc:#b5651d}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#161413;--fg:#ece7e1;--mut:#a39a90;--card:#211e1c;--bd:#38332f;--acc:#e0954f}}}}
:root[data-theme="dark"]{{--bg:#161413;--fg:#ece7e1;--mut:#a39a90;--card:#211e1c;--bd:#38332f;--acc:#e0954f}}
body{{background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,sans-serif;margin:0;padding:16px;max-width:760px;margin-inline:auto}}
h1{{font-size:1.4rem;margin:.2em 0}} h2{{font-size:1.1rem;margin-top:1.6em;color:var(--acc)}}
.line{{font-style:italic;color:var(--mut)}} .card{{background:var(--card);border:1px solid var(--bd);border-radius:10px;padding:12px;margin:10px 0}}
.code{{font-weight:700}} audio{{width:100%;margin:6px 0}} .row{{display:flex;flex-wrap:wrap;gap:10px;margin:4px 0}}
.note{{width:100%;box-sizing:border-box;padding:6px;border:1px solid var(--bd);border-radius:6px;background:transparent;color:inherit}}
button{{background:var(--acc);color:#fff;border:0;border-radius:8px;padding:10px 14px;font-size:1rem}} textarea{{width:100%;height:9em;box-sizing:border-box;background:transparent;color:inherit;border:1px solid var(--bd)}}
details{{margin-top:2em;color:var(--mut)}}</style></head><body>
<h1>Nghe chấm mù — Cổng 0</h1>
<p>Nghe bằng tai nghe, âm lượng vừa. Chấm từng bản độc lập, <b>đừng mở phần "Khoá mã" trước khi chấm xong</b>. Xong bấm "Chép kết quả" và dán vào chat.</p>
<p>Tiêu chí Cổng 0: cảnh cảm xúc khó "tin được" với ≥ 3/5 người nghe mù. Người chấm thứ nhất là chủ dự án; có thể gửi file này cho bạn bè (mỗi người một bản).</p>
<h2>A. Bà lão thắp đèn chào con phố lần cuối (nói khẽ, nghẹn)</h2><p class="line">"{LINE}"</p>{body}
<h2>B. Đứa trẻ sợ ánh đèn trắng</h2><p class="line">"{KID}"</p>{kid}
<h2>C. Nhạc chủ đề 60 s (buồn lặng, có hy vọng) — ACE-Step trên CPU</h2>{mus}
<p><button id="cp">Chép kết quả</button></p><textarea id="out" readonly></textarea>
<details><summary>Khoá mã (chỉ mở sau khi chấm)</summary><pre>{json.dumps(key, indent=1)}</pre></details>
<script>
const K='nghe-cham-m0';
function collect(){{const o={{}};document.querySelectorAll('.card').forEach(c=>{{const k=c.dataset.code;
const b=c.querySelector(`input[name="${{k}}-b"]:checked`),s=c.querySelector(`input[name="${{k}}-s"]:checked`),n=c.querySelector('.note').value;
o[k]=[b?b.value:'-',s?s.value:'-',n].join(' | ');}});return o;}}
function save(){{try{{localStorage.setItem(K,JSON.stringify(collect()))}}catch(e){{}}}}
function load(){{let o;try{{o=JSON.parse(localStorage.getItem(K)||'{{}}')}}catch(e){{return}}
for(const k in o){{const [b,s,n]=o[k].split(' | ');const c=document.querySelector(`[data-code="${{k}}"]`);if(!c)continue;
const rb=c.querySelector(`input[name="${{k}}-b"][value="${{b}}"]`);if(rb)rb.checked=true;const rs=c.querySelector(`input[name="${{k}}-s"][value="${{s}}"]`);if(rs)rs.checked=true;c.querySelector('.note').value=n||'';}}}}
document.addEventListener('change',save);document.addEventListener('input',save);load();
document.getElementById('cp').onclick=()=>{{const o=collect();const t='KẾT QUẢ NGHE CHẤM M0\\n'+Object.entries(o).map(([k,v])=>k+': '+v).join('\\n');
const ta=document.getElementById('out');ta.value=t;ta.select();try{{navigator.clipboard.writeText(t)}}catch(e){{}}}};
</script></body></html>'''
open(os.path.join(M0, 'NGHE-CHAM-M0.html'), 'w').write(html)
print(os.path.getsize(os.path.join(M0, 'NGHE-CHAM-M0.html')) / 1e6, 'MB')
