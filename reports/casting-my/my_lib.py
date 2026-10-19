"""CASTING-MỸ · dùng lại thư viện casting-giong (cg_lib, kiem_lib) — chỉ đổi thư mục ngoài git và nhật ký ký tự của phiên này."""
import os, sys
os.environ.setdefault('CG_OUT', '/var/tmp/cine-out/casting-my')
H = os.path.dirname(os.path.abspath(__file__)); CG = os.path.join(os.path.dirname(H), 'casting-giong')
sys.path.insert(0, CG)
import cg_lib as L, kiem_lib as K   # noqa: E402
L.LOG = os.path.join(H, 'nhat-ky-ky-tu.jsonl')   # ký tự gửi của phiên này
CHAN, MOC = 5000, 3000                             # chặn / mốc theo dõi (lệnh 18/10 23:36)


def da_gui():
    import json
    if not os.path.exists(L.LOG): return 0
    return sum(json.loads(l)['ky_tu'] for l in open(L.LOG) if l.strip())


def tts(vid, text, tag):
    """Chặn trước khi gửi nếu vượt trần 5 000 ký tự gửi của phiên (cache theo băm: bản đã thu thì 0 ký tự)."""
    if da_gui() + len(text) >= CHAN: raise SystemExit(f'CHẶN: {da_gui()} + {len(text)} ≥ {CHAN} ký tự gửi')
    return L.tts(vid, text, tag=tag)
