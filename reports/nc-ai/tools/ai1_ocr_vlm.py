"""NC-AI · AI-1 chép trang bằng mô hình nhìn (OpenAI Responses, khoá do proxy gắn). Dùng: python3 -I ai1_ocr_vlm.py <model> <anh.jpg> <ra.txt> <cost.jsonl>"""
import sys, json, base64, time, urllib.request
model, img, out, cost = sys.argv[1:5]; PRICE = {'gpt-6.1-sol': (2.0, 10.0), 'gpt-6-luna': (0.1, 0.5)}
P = ("Transcribe the main body text of this 1784 printed page EXACTLY as printed, diplomatic transcription: keep long s as ſ, keep old spellings, "
     "keep line-end hyphens, do not modernise, do not correct, do not add anything not visible. Skip the page number and the margin dates. Output only the text.")
b = base64.b64encode(open(img, 'rb').read()).decode()
body = {"model": model, "input": [{"role": "user", "content": [{"type": "input_text", "text": P}, {"type": "input_image", "image_url": f"data:image/jpeg;base64,{b}"}]}], "stream": True}
req = urllib.request.Request('https://api.openai.com/v1/responses', data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'})
t0 = time.time(); r = None
with urllib.request.urlopen(req, timeout=600) as fh:
    for line in fh:
        line = line.decode().strip()
        if line.startswith('data: ') and line[6:] != '[DONE]':
            ev = json.loads(line[6:])
            if ev.get('type') == 'response.completed': r = ev['response']
txt = ''.join(c.get('text', '') for o in r['output'] if o.get('type') == 'message' for c in o['content']); open(out, 'w').write(txt)
u = r['usage']; pi, po = PRICE[model]; usd = u['input_tokens'] / 1e6 * pi + u['output_tokens'] / 1e6 * po
open(cost, 'a').write(json.dumps({'tag': f'ai1-ocr-vlm:{img.split("/")[-1]}', 'model': model, 'served': r.get('model'), 'in': u['input_tokens'], 'out': u['output_tokens'], 'usd': round(usd, 5), 's': round(time.time() - t0, 1)}) + '\n')
print(r.get('model'), round(usd, 4), round(time.time() - t0, 1))
