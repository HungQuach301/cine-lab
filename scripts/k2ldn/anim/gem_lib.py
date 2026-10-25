#!/opt/cine/bin/python
"""ANIMATIC-T4 · thư viện Gemini chung (Omni + Flash kiểm) — sổ AI Gemini reports/animatic-t4/so-ai-gemini.jsonl, mỗi dòng có `usd` giá thật theo usage × bảng giá.
Ngân sách T4 (chủ dự án 23/10/2026 23:45; lệnh ANIMATIC-T4): $35, mốc theo dõi $30; đã tiêu trước phiên này = sổ tiền kỳ + sổ LOOK-T4-V2 (cộng từ tệp, không gõ tay).
Chặn: tổng T4 + dự phòng lượt > $35 → từ chối; HTTP 402 / hết hạn mức → ghi DUNG-GEMINI, từ chối mọi lệnh sau; cùng lỗi ≥ 3 lần liên tiếp → dừng.
Giá (https://ai.google.dev/gemini-api/docs/pricing, tải 24/10/2026, SHA d80f45c5…): Omni vào $1,50/1M, ra video $17,50/1M, chữ/suy nghĩ $9,00/1M;
gemini-3.8-flash vào $0,75/1M, ra $3,75/1M (tới 31/12/2026). Khoá do proxy gắn — mã KHÔNG đọc/đặt/in khoá; UA nghiên cứu, không email."""
import datetime, hashlib, json, sys, time, urllib.error, urllib.request
from pathlib import Path
REPO = Path(__file__).resolve().parents[3]; D = REPO / 'reports/animatic-t4'; SO = D / 'so-ai-gemini.jsonl'; STOP = D / 'DUNG-GEMINI'
TRUOC = [REPO / 'reports/tien-ky-t4/so-ai-gemini.jsonl', REPO / 'reports/look-t4-v2/so-ai.jsonl']
API = 'https://generativelanguage.googleapis.com/v1beta'; UA = 'CineLab-research (+https://github.com/HungQuach301/cine-lab)'
NGAN_SACH, MOC = 35.0, 30.0
GIA = {'gemini-omni-1.1-flash': (1.50e-6, 9.00e-6, 17.50e-6), 'gemini-3.8-flash': (0.75e-6, 3.75e-6, 0)}


def sha(b): return hashlib.sha256(b).hexdigest()
def rows(p):
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def da_tieu_truoc():
    t = 0.0
    for p in TRUOC:
        for r in rows(p):
            if 'gemini' in str(r.get('model_req') or r.get('model') or r.get('nha') or '').lower() or r.get('nha') == 'gemini':
                t += float(r.get('usd') or 0)
    return round(t, 4)


def tong_t4(): return round(da_tieu_truoc() + sum(float(r.get('usd') or 0) for r in rows(SO)), 4)


def kiem_truoc(du_phong):
    if STOP.exists(): sys.exit('DỪNG Gemini: ' + STOP.read_text())
    if tong_t4() + du_phong > NGAN_SACH: sys.exit(f'CHẶN: tổng Gemini T4 {tong_t4():.2f} + dự phòng {du_phong} > ${NGAN_SACH}')
    R = rows(SO); n, last = 0, None
    for r in reversed(R):
        if r.get('http') == 200: break
        k = (r.get('http'), json.dumps(r.get('loi'))[:120])
        if last is None or k == last: n, last = n + 1, k
        else: break
    if n >= 3: sys.exit(f'DỪNG: cùng lỗi {n} lần liên tiếp {last}')


def req(method, url, body=None, timeout=600):
    r = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None, method=method, headers={'User-Agent': UA, 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(r, timeout=timeout) as f: return f.status, f.read()
    except urllib.error.HTTPError as e: return e.code, e.read()
    except Exception as e: return 599, json.dumps({'loi_mang': str(e)[:300]}).encode()


def usd_of(model, u):
    if not u: return None
    gi, gt, gv = GIA[model]
    tin = u.get('total_input_tokens') or u.get('input_tokens') or u.get('promptTokenCount') or 0
    out = u.get('total_output_tokens') or u.get('output_tokens') or u.get('candidatesTokenCount') or 0
    th = u.get('total_thought_tokens') or u.get('thoughtsTokenCount') or 0; vid = 0
    for k in ('output_tokens_by_modality', 'total_output_tokens_by_modality'):
        for m in u.get(k) or []:
            if str(m.get('modality', '')).lower() == 'video': vid = m.get('tokens') or 0
    return round(tin * gi + vid * gv + (max(0, out - vid) + th) * gt, 5)


def log(rec):
    D.mkdir(parents=True, exist_ok=True); rec.setdefault('date_utc', datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'))
    with open(SO, 'a') as f: f.write(json.dumps(rec, ensure_ascii=False) + '\n')
    t = tong_t4()
    if t >= MOC: print(f'GEMINI T4 ${t:.2f} — VƯỢT MỐC THEO DÕI ${MOC:.0f}', file=sys.stderr)


def dung_neu_402(st, J, tag):
    s = json.dumps(J).lower()
    if st == 402 or 'prepay' in s or 'insufficient' in s or ('quota' in s and st == 429 and 'billing' in s):
        STOP.write_text(f'HTTP {st} ở {tag}: {s[:400]}\n'); sys.exit(f'DỪNG NGAY: HTTP {st} (nạp tiền do chủ dự án)')
