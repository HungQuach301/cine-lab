#!/opt/cine/bin/python
"""Người chấm mù qua Claude API (phiên K, 1.9.0, chủ dự án duyệt 11/10/2026): thay subagent cho Q27, Q31 và kiểm mù kịch bản G1.

Mỗi người chấm là MỘT lần gọi `claude -p` không giao diện, khoá bằng ANTHROPIC_API_KEY="$CONSOLE_API_KEY" (khoá không bao giờ in ra log,
không ghi vào tệp), mô hình ghim MODEL (không để mặc định), chạy trong thư mục bộ ảnh (ngoài repo) với:
  --bare        không CLAUDE.md, không hook, không bộ nhớ: người chấm không thấy ngữ cảnh sản xuất
  --restricted  không có công cụ chạy lệnh; công cụ đọc tệp chỉ đọc được trong thư mục bộ ảnh
  --tools Read  chỉ một công cụ: đọc tệp; không MCP (--strict-mcp-config), không lưu phiên
  HOME tạm, môi trường bỏ mọi biến CLAUDE*/ANTHROPIC* của phiên gọi.
Đề bài: nguyên văn (Q27/Q31: PROMPT-Rk.txt dựng từ đề bài khoá; G1: tệp đề bài của P). Ghi lại: bản chép đầy đủ (stream-json, không có
khoá) ở <thư mục>/run/Rk.jsonl, mô hình thực chạy (modelUsage), chi phí (total_cost_usd), số lượt, tệp đã đọc; tóm tắt vào manifest.json.
FAIL CLOSED: thiếu khoá, gọi thử hỏng, lỗi API, hết credit, quá trần, mô hình khác MODEL, trả lời không đọc được, không đọc đủ tệp đề bài
nêu → KHÔNG ghi Rk.json (bộ chấm TRƯỢT với lý do ghi trong manifest), không bỏ qua bước chấm.
"""
import datetime, hashlib, json, os, re, shutil, subprocess, tempfile, time

MODEL = 'claude-sonnet-5-5'
CAP_USD = {'Q27': 1.50, 'Q31': 1.50, 'G1': 0.60}   # trần chi phí MỘT người chấm (--max-budget-usd); vượt là lỗi, không có điểm
PROBE_CAP = 0.05
TIMEOUT = 1800
RETRY = 1          # gọi lại tối đa 1 lần khi lỗi API hoặc trả lời KHÔNG đọc được (không có điểm nào để chọn); không bao giờ gọi lại vì
                   # điểm, mô hình sai hay đọc thiếu tệp; mọi lần gọi đều ghi vào manifest


class JudgeError(Exception):
    pass


def _env(home):
    if not os.environ.get('CONSOLE_API_KEY'): raise JudgeError('thiếu biến CONSOLE_API_KEY (khoá Claude API của chủ dự án)')
    e = {k: v for k, v in os.environ.items() if not k.upper().startswith(('CLAUDE', 'ANTHROPIC', 'CCR_PRELOAD_CLAUDE'))}
    e.update(HOME=home, ANTHROPIC_API_KEY=os.environ['CONSOLE_API_KEY'], CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC='1', DISABLE_AUTOUPDATER='1')
    return e


def _scrub(s):
    k = os.environ.get('CONSOLE_API_KEY') or ''
    return s.replace(k, '<KHOÁ>') if len(k) >= 8 else s


def cli_version():
    try: return subprocess.run(['claude', '--version'], capture_output=True, text=True, timeout=60).stdout.strip()
    except Exception as e: return f'không đọc được ({e})'


def call(prompt, cwd, cap):
    """một lần gọi; trả về dict(result, cost_usd, model_usage, num_turns, reads, denials, is_error, error, transcript)"""
    home = tempfile.mkdtemp(prefix='judge-home-')
    cmd = ['claude', '-p', '--bare', '--restricted', '--model', MODEL, '--tools', 'Read', '--allowedTools', 'Read', '--strict-mcp-config',
           '--no-session-persistence', '--permission-mode', 'dontAsk', '--output-format', 'stream-json', '--verbose', '--max-budget-usd', f'{cap:.2f}']
    t0 = time.time()
    try:
        p = subprocess.run(cmd, input=prompt, cwd=cwd, env=_env(home), capture_output=True, text=True, timeout=TIMEOUT)
        out, err, rc = p.stdout, p.stderr, p.returncode
    except subprocess.TimeoutExpired as e:
        out, err, rc = (e.stdout or b'').decode() if isinstance(e.stdout, bytes) else (e.stdout or ''), 'quá thời gian', -1
    finally: shutil.rmtree(home, ignore_errors=True)
    out, err = _scrub(out), _scrub(err)
    ev = []
    for ln in out.splitlines():
        try: ev.append(json.loads(ln))
        except Exception: pass
    res = next((x for x in reversed(ev) if x.get('type') == 'result'), None)
    reads = [b['input'].get('file_path') for x in ev if x.get('type') == 'assistant' for b in (x.get('message') or {}).get('content') or []
             if isinstance(b, dict) and b.get('type') == 'tool_use' and b.get('name') == 'Read']
    r = dict(secs=round(time.time() - t0, 1), rc=rc, transcript=out, reads=reads)
    if not res:
        r.update(is_error=True, error=f'không có kết quả (mã {rc}): {err.strip()[-300:] or out.strip()[-300:]}', cost_usd=None, model_usage={}, result=None)
        return r
    r.update(is_error=bool(res.get('is_error')) or res.get('subtype') != 'success', error=None if res.get('subtype') == 'success' else f"{res.get('subtype')}: {str(res.get('result') or res.get('errors') or '')[:300]}",
             result=res.get('result'), cost_usd=res.get('total_cost_usd'), model_usage=res.get('modelUsage') or {}, num_turns=res.get('num_turns'),
             denials=[(d.get('tool_input') or {}).get('file_path') for d in res.get('permission_denials') or []], session_id=res.get('session_id'))
    if r['is_error'] and not r['error']: r['error'] = str(res.get('result'))[:300]
    return r


def model_errors(mu):
    """mô hình thực chạy phải đúng MODEL và chỉ MODEL"""
    if not mu: return ['không có modelUsage']
    o = sorted(set(mu) - {MODEL})
    return ([f'mô hình khác {MODEL}: {o}'] if o else []) + ([] if MODEL in mu else [f'không có {MODEL} trong modelUsage'])


def probe():
    """gọi thử trước khi chấm: chạy được, đúng mô hình. Hỏng → JudgeError (dừng, báo)"""
    d = tempfile.mkdtemp(prefix='judge-probe-')
    try: r = call('Reply with only the word OK.', d, PROBE_CAP)
    finally: shutil.rmtree(d, ignore_errors=True)
    e = ([r['error']] if r['is_error'] else []) + model_errors(r['model_usage'])
    if e or 'OK' not in str(r.get('result') or ''): raise JudgeError('gọi thử Claude API hỏng: ' + '; '.join(e or [f"trả lời {str(r.get('result'))[:80]!r}"]))
    return dict(cost_usd=r['cost_usd'], model_usage=r['model_usage'], secs=r['secs'])


def parse_json(txt):
    """đối tượng JSON trong câu trả lời (bỏ rào ```json nếu có); không đọc được → None"""
    if not isinstance(txt, str): return None
    t = re.sub(r'^\s*```(?:json)?\s*|\s*```\s*$', '', txt.strip())
    for cand in (t, t[t.find('{'):t.rfind('}') + 1] if '{' in t else ''):
        try:
            x = json.loads(cand)
            if isinstance(x, dict): return x
        except Exception: pass
    return None


def _need_reads(prompt, out):
    """tệp đề bài bắt người chấm đọc: mọi đường dẫn tuyệt đối dưới thư mục bộ ảnh nêu trong đề bài (F01…F60 viết tắt bằng "…" thì
    lấy theo danh sách ảnh của manifest)"""
    return sorted(set(re.findall(re.escape(out) + r'/[A-Za-z0-9_.\-]+', prompt)))


def run_rater(rule, r, prompt, out, need, parse=True):
    """chấm một người; trả về (trả lời đã kiểm hoặc None, bản ghi cho manifest)"""
    os.makedirs(os.path.join(out, 'run'), exist_ok=True); tries = []
    for k in range(RETRY + 1):
        x = call(prompt, out, CAP_USD[rule])
        open(os.path.join(out, 'run', f'{r}-lan{k + 1}.jsonl'), 'w').write(x['transcript'])
        e = []
        if x['is_error']: e.append(f"lỗi API: {x['error']}")
        e += model_errors(x['model_usage'])
        rep = parse_json(x['result']) if parse else (x['result'] if isinstance(x['result'], str) and x['result'].strip() else None)
        if not x['is_error'] and rep is None: e.append('trả lời không đọc được' + (' (không phải JSON)' if parse else ''))
        miss = sorted(set(need) - set(x['reads']))
        if not x['is_error'] and miss: e.append(f'không đọc đủ tệp đề bài nêu: thiếu {len(miss)} ({", ".join(os.path.basename(m) for m in miss[:5])}…)')
        tries.append(dict(lan=k + 1, secs=x['secs'], cost_usd=x['cost_usd'], model_usage=x['model_usage'], num_turns=x.get('num_turns'),
                          reads=len(x['reads']), denials=x.get('denials') or [], session_id=x.get('session_id'), loi=e,
                          transcript=f'run/{r}-lan{k + 1}.jsonl', transcript_sha256=hashlib.sha256(x['transcript'].encode()).hexdigest()))
        api_fail = x['is_error'] or x['result'] is None or rep is None
        if not e: return rep, tries
        if not api_fail or (not x['is_error'] and (model_errors(x['model_usage']) or miss)): break   # mô hình sai, đọc thiếu: không gọi lại
    return None, tries


def now(): return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
