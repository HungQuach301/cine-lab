#!/opt/cine/bin/python
"""Kiểm đọc 5 luật máy của LUAT-NOI-DUNG-G §7 (đề xuất cho K, chưa khoá) trên lời, tiêu đề, mô tả, chữ trên hình của đặc tả. In JSON; mã thoát 0."""
import json, re, yaml, os
H = os.path.dirname(os.path.abspath(__file__)); E = yaml.safe_load(open(f'{H}/episode.yaml'))
vo = {s['id']: s['vo'] for s in E['segments']}; sh = {s['id']: s['vo'] for s in E['shorts']}
desc = open(f'{H}/phat-hanh/description.en.txt').read(); titles = open(f'{H}/phat-hanh/titles.txt').read()
onscreen = []
def walk(x):
    if isinstance(x, dict):
        for k, v in x.items():
            if k in ('s', 'sub', 't', 'title', 'q', 'kicker', 'big', 'unit', 'tag') and isinstance(v, str): onscreen.append(v)
            else: walk(v)
    elif isinstance(x, list): [walk(v) for v in x]
walk(E['segments']); walk(E['shorts'])
ALL = {'loi': ' '.join(vo.values()), 'shorts': ' '.join(sh.values()), 'tieu_de': titles, 'mo_ta': desc, 'tren_hinh': ' | '.join(onscreen)}
B1 = ["people who really run", "hidden hand", "don't want you to know", "secret meeting", "puppet master", "they don't want", "behind the scenes", "pulling the strings"]
R2 = re.compile(r"\bthe \w+ family (controls|owns|runs|rules)\b|\b(chinese|japanese|americans|europeans|swedes|bankers|jews|muslims|christians)\s+(want|plan|control|secretly)\b", re.I)
R = {}
R['§1 cụm âm mưu'] = [(k, p) for k, t in ALL.items() for p in B1 if p in t.lower()]
R['§2 gán động cơ nhóm'] = [(k, m.group(0)) for k, t in ALL.items() for m in R2.finditer(t)]
first_desc = desc.strip().splitlines()[0]
R['§4 miễn trừ'] = {'lời đoạn 01 (≤ 30 s)': "isn't financial or investment advice" in vo['01'], 'dòng đầu mô tả': 'not financial' in first_desc.lower() or "isn't financial" in first_desc.lower()}
R['§5 "will" với thực thể chính trị/công ty'] = [s.strip() for t in vo.values() for s in re.split(r'(?<=[.?!])\s', t) if re.search(r"\bwill\b", s, re.I)]
R['§5 dòng as-of trên hình'] = sorted({x for x in onscreen if re.search(r'as of', x, re.I)})
R['§3 cặp huyền thoại/hồ sơ'] = sum(1 for x in onscreen if x.upper().startswith('MYTH VS. RECORD') or x.upper() in ('TWO OPPOSITE CLAIMS',))
print(json.dumps(R, ensure_ascii=False, indent=1))
