"""NC-AI · AI-B lượt đọc 1 (OpenAI Responses API, khoá do proxy gắn — mã KHÔNG đọc biến khoá).
Trích danh sách vật / hoạt động / trang phục / mật độ người cho Gibraltar tháng 9/1782 từ các trang nguyên văn (OCR djvu).
Dùng: python3 -I aib_doc.py <model> <thu_muc_trang> <glob_tien_to> <tep_ra.json> <cost.jsonl>"""
import sys, os, json, glob, time, urllib.request
model, pdir, pref, out, cost = sys.argv[1:6]; BIEN = sys.argv[6] if len(sys.argv) > 6 else 'gib1782'
PRICE = {'gpt-6.1-sol': (2.0, 10.0), 'gpt-6-astra': (10.0, 50.0), 'gpt-6-luna': (0.1, 0.5)}  # $/MTok vào/ra — developers.openai.com/api/docs/models đọc 18/10/2026
pages = sorted(glob.glob(os.path.join(pdir, pref + '*.txt')))
doc = '\n\n'.join(f'=== PAGE {os.path.basename(p)[:-4]} ===\n' + open(p).read() for p in pages)
INSTR = """You are a careful archival research assistant. Below are OCR transcriptions (with OCR errors, long-s printed as 'f') of printed pages about the siege of Gibraltar, 1782.
Task: list every piece of evidence about life INSIDE Gibraltar (garrison town, batteries, streets) in SEPTEMBER 1782 that a 3D film-maker could use, in four categories:
- "object": physical things present (buildings, works, vessels, guns, tents, carts, stores, property...)
- "activity": what people were doing (work, carrying, firing, parading, moving property...)
- "clothing": what people wore (uniform, dress, equipment carried on the body)
- "crowd_density": how many people were where (numbers of men on guard/work, inhabitants moving, crowds)
RULES: (1) Every item MUST quote an exact contiguous substring copied character-for-character from the page text (keep OCR errors and 'f' for s; you may span line breaks — then copy the words separated by single spaces, and remove a trailing hyphen at line end only if the word continues). (2) Give the page id exactly as in the PAGE header. (3) Give the date if the text ties the item to a specific day of September 1782, else null. (4) If a category has no evidence, return no items for it — do NOT infer from general knowledge. (5) Items about the ENEMY camp/lines (Spanish/French) must set side="enemy"; garrison/town side="garrison". (6) description_en: one plain sentence restating ONLY what the quote says."""
if BIEN == 'london1666':  # cùng luật, đổi nơi/thời; trang = mục ngày 'pNNN' = 9/NN (902 = 2/9/1666); trần ≤ 20 mục (lệnh AI-B b)
    INSTR = INSTR.replace('OCR transcriptions (with OCR errors, long-s printed as \'f\') of printed pages about the siege of Gibraltar, 1782', 'diary entries (modern transcription) about the Great Fire of London, 2-7 September 1666; page id pNNN means the entry for September NN-900')
    INSTR = INSTR.replace('life INSIDE Gibraltar (garrison town, batteries, streets) in SEPTEMBER 1782', 'life in the STREETS of London and on the river in 2-7 SEPTEMBER 1666').replace('(5) Items about the ENEMY camp/lines (Spanish/French) must set side="enemy"; garrison/town side="garrison".', '(5) side="garrison" for everything (field kept for schema compatibility). (7) Return AT MOST 20 items, prioritising the most concrete visual evidence.')
schema = {"type": "object", "additionalProperties": False, "required": ["items"], "properties": {"items": {"type": "array", "items": {"type": "object", "additionalProperties": False,
  "required": ["category", "side", "description_en", "quote", "page", "date"], "properties": {
  "category": {"type": "string", "enum": ["object", "activity", "clothing", "crowd_density"]}, "side": {"type": "string", "enum": ["garrison", "enemy", "unclear"]},
  "description_en": {"type": "string"}, "quote": {"type": "string"}, "page": {"type": "string"}, "date": {"type": ["string", "null"]}}}}}}
body = {"model": model, "input": [{"role": "system", "content": INSTR}, {"role": "user", "content": doc}],
        "text": {"format": {"type": "json_schema", "name": "evidence", "schema": schema, "strict": True}}, "reasoning": {"effort": "medium"}, "stream": True}
req = urllib.request.Request('https://api.openai.com/v1/responses', data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'})
t0 = time.time(); r = None
# stream SSE: đường truyền proxy cắt lệnh chờ > ~30 s (bài học PT §15.2) → đọc đến sự kiện response.completed
with urllib.request.urlopen(req, timeout=900) as fh:
    for line in fh:
        line = line.decode().strip()
        if line.startswith('data: ') and line[6:] != '[DONE]':
            ev = json.loads(line[6:])
            if ev.get('type') == 'response.completed': r = ev['response']
            elif ev.get('type') in ('response.failed', 'error'): sys.exit(json.dumps(ev)[:500])
dt = time.time() - t0
txt = ''.join(c.get('text', '') for o in r['output'] if o.get('type') == 'message' for c in o['content'])
u = r['usage']; pi, po = PRICE[model]; usd = u['input_tokens'] / 1e6 * pi + u['output_tokens'] / 1e6 * po
json.dump({'model': model, 'served': r.get('model'), 'pages': [os.path.basename(p) for p in pages], **json.loads(txt)}, open(out, 'w'), ensure_ascii=False, indent=1)
open(cost, 'a').write(json.dumps({'tag': f'aib-doc1:{BIEN}:{pref}', 'model': model, 'served': r.get('model'), 'in': u['input_tokens'], 'out': u['output_tokens'], 'usd': round(usd, 5), 's': round(dt, 1)}) + '\n')
print(r.get('model'), u['input_tokens'], u['output_tokens'], round(usd, 4), round(dt, 1), 'items', len(json.loads(txt)['items']))
