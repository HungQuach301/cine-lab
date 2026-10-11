#!/usr/bin/env python3
"""`claude` giả cho selftest judge.py (không gọi mạng). Chế độ theo biến FAKE_MODE:
ok (đọc đủ ảnh, trả JSON), credit (hết credit), model (chạy mô hình khác), leak (in khoá trong trả lời), partial (đọc thiếu ảnh), fence (JSON trong rào ```),
twojson (hai khối JSON: người chấm tự sửa giữa chừng), twojson1 (hai khối JSON ở lần gọi đầu, lần sau đúng)."""
import json, os, re, sys

if '--version' in sys.argv: print('0.0.0 (fake)'); sys.exit(0)
mode = os.environ.get('FAKE_MODE', 'ok'); prompt = sys.stdin.read(); cwd = os.getcwd()
model = sys.argv[sys.argv.index('--model') + 1]
ev = lambda **k: print(json.dumps(k))
if 'Reply with only the word OK.' in prompt:
    ev(type='result', subtype='success', is_error=False, result='OK', total_cost_usd=0.001, num_turns=1, modelUsage={model: {'outputTokens': 1}}); sys.exit(0)
if mode == 'credit':
    ev(type='result', subtype='success', is_error=True, result='Credit balance is too low', total_cost_usd=0, num_turns=1, modelUsage={}); sys.exit(1)
imgs = sorted(f for f in os.listdir(cwd) if re.fullmatch(r'F\d\d\.jpg', f))
if mode == 'partial': imgs = imgs[:-1]
ev(type='assistant', message=dict(content=[dict(type='tool_use', name='Read', input=dict(file_path=os.path.join(cwd, f))) for f in imgs]))
rep = {'scores': {f[:3]: {'beauty': 5, 'detail': 5, 'light': 5} for f in imgs}, 'notes': os.environ.get('ANTHROPIC_API_KEY', '') if mode == 'leak' else 'ok'}
txt = json.dumps(rep)
if mode == 'fence': txt = '```json\n' + txt + '\n```'
if mode == 'twojson' or (mode == 'twojson1' and not os.path.exists(os.path.join(cwd, '.fake_lan1'))):
    open(os.path.join(cwd, '.fake_lan1'), 'w').write('1'); txt = txt + '\n\nCorrection: the JSON above is wrong.\n\n' + txt
mu = {model: {'outputTokens': 100}}
if mode == 'model': mu = {'claude-haiku-5-5': {'outputTokens': 100}}
ev(type='result', subtype='success', is_error=False, result=txt, total_cost_usd=0.01, num_turns=len(imgs) + 1, modelUsage=mu, session_id='fake')
