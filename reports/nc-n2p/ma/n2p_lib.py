"""NC-N2P · thư viện chung: mặt nạ ID (bảng màu V7C idmask_v7c.js), lớp N2+, ghép lớp (a), sổ AI (K-LAI), giá.
Lớp N2+ trên cảnh Gibraltar thử (T4 London chưa có cảnh): (a) DỮ KIỆN = phố, nhà, trại, công sự, tàu, cờ, pin nổi, lửa, người (lớp sống dựng từ nguồn), khác (xe, đèn);
(c) NỀN = trời, nước, đất bằng, sườn, đá/vách, cây (mặt nạ V7C xếp cây instanced vào 'nước' — sửa ở idmap: cụm 'nước' nhỏ tách khỏi biển → 'cây').
(b) MINH HOẠ = không có trên render; AI chỉ được thêm vào vùng (c)."""
import datetime, hashlib, json, os
from pathlib import Path
import cv2, numpy as np

REPO = Path(__file__).resolve().parents[3]
N2P = REPO / 'reports/nc-n2p'
SO_AI = N2P / 'so-ai.jsonl'
UA = 'CineLab-research (+https://github.com/HungQuach301/cine-lab)'
PAL = {'troi': (40, 80, 200), 'nuoc': (0, 170, 190), 'bang': (200, 170, 90), 'suon': (150, 120, 70), 'da': (110, 100, 95), 'pho': (255, 200, 220), 'nha': (235, 235, 235),
       'trai': (245, 225, 160), 'congsu': (170, 150, 120), 'tau': (255, 0, 0), 'co': (255, 255, 0), 'pin': (255, 0, 255), 'lua': (255, 128, 0), 'nguoi': (0, 255, 0),
       'khac': (128, 128, 128), 'cay': (60, 140, 60)}
NAMES = list(PAL)
LOP_A = ['pho', 'nha', 'trai', 'congsu', 'tau', 'co', 'pin', 'lua', 'nguoi', 'khac']
LOP_C = ['troi', 'nuoc', 'bang', 'suon', 'da', 'cay']
DAT = ['bang', 'suon', 'da', 'pho']          # đất (cho T9)
# bảng màu V2V (do_v2v.py NC-V2V) để gọi bộ đo cũ không sửa
V2V = {'troi': (40, 80, 200), 'nuoc': (0, 170, 190), 'dat': (140, 105, 60), 'nha': (235, 235, 235), 'tau': (255, 0, 0), 'co': (255, 255, 0), 'pin': (255, 0, 255),
       'lua': (255, 128, 0), 'nguoi': (0, 255, 0), 'khac': (128, 128, 128)}
TO_V2V = {'troi': 'troi', 'nuoc': 'nuoc', 'bang': 'dat', 'suon': 'dat', 'da': 'dat', 'cay': 'dat', 'pho': 'nha', 'nha': 'nha', 'trai': 'nha', 'congsu': 'nha', 'tau': 'tau',
          'co': 'co', 'pin': 'pin', 'lua': 'lua', 'nguoi': 'nguoi', 'khac': 'khac'}


def sha(b): return hashlib.sha256(b).hexdigest()


def sha_file(p): return sha(Path(p).read_bytes())


def idmap(png, size=None, cay_max=0.003):
    """PNG mặt nạ V7C → mảng nhãn (chỉ số NAMES). Cụm 'nước' nhỏ (< cay_max diện tích) không chạm cụm nước lớn nhất → 'cay'."""
    im = cv2.imread(str(png))[:, :, ::-1]
    if size and (im.shape[1], im.shape[0]) != size: im = cv2.resize(im, size, interpolation=cv2.INTER_NEAREST)
    pal = np.array([PAL[n] for n in NAMES], np.int32)
    d = ((im[:, :, None, :].astype(np.int32) - pal[None, None]) ** 2).sum(-1)
    L = d.argmin(-1).astype(np.uint8)
    w = (L == NAMES.index('nuoc')).astype(np.uint8)
    n, cc, st, _ = cv2.connectedComponentsWithStats(w, 8)
    if n > 1:
        big = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])); amax = cay_max * L.size
        small = [i for i in range(1, n) if i != big and st[i, cv2.CC_STAT_AREA] < amax]
        if small: L[np.isin(cc, small)] = NAMES.index('cay')
    return L


def lop_mask(L, names): return np.isin(L, [NAMES.index(n) for n in names])


def to_v2v_png(L, out, size=(640, 360)):
    rgb = np.zeros(L.shape + (3,), np.uint8)
    for i, n in enumerate(NAMES): rgb[L == i] = V2V[TO_V2V[n]]
    rgb = cv2.resize(rgb, size, interpolation=cv2.INTER_NEAREST); cv2.imwrite(str(out), rgb[:, :, ::-1])


def ghep(render, ai, A, feather=3):
    """GHÉP lớp (a): trong vùng A = điểm ảnh render nguyên vẹn (sai khác 0); viền mềm ra NGOÀI vùng ≤ feather px; ngoài nữa = AI."""
    if ai.shape != render.shape: ai = cv2.resize(ai, (render.shape[1], render.shape[0]), interpolation=cv2.INTER_AREA)
    d = cv2.distanceTransform((~A).astype(np.uint8), cv2.DIST_L2, 3)
    al = np.clip(1.0 - d / float(feather + 1), 0, 1); al[A] = 1.0
    out = render.astype(np.float32) * al[..., None] + ai.astype(np.float32) * (1 - al[..., None])
    out = np.clip(np.rint(out), 0, 255).astype(np.uint8); out[A] = render[A]
    return out, al


def so_ai(rec):
    rec.setdefault('date_utc', datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'))
    SO_AI.parent.mkdir(parents=True, exist_ok=True)
    with open(SO_AI, 'a') as f: f.write(json.dumps(rec, ensure_ascii=False) + '\n')


def tong_usd(nha=None):
    if not SO_AI.exists(): return 0.0
    s = 0.0
    for l in SO_AI.read_text().splitlines():
        if not l.strip(): continue
        r = json.loads(l)
        if nha is None or r.get('nha') == nha: s += float(r.get('usd') or 0)
    return s


def c2pa_of(b):
    """dò manifest C2PA trong tệp (JPEG APP11/JUMBF hoặc MP4 uuid) — chỉ báo có/không + chuỗi digitalSourceType nếu đọc được"""
    has = b'c2pa' in b
    dst = None
    for k in (b'trainedAlgorithmicMedia', b'compositeWithTrainedAlgorithmicMedia', b'algorithmicMedia'):
        if k in b: dst = k.decode(); break
    return {'co_manifest': has, 'digitalSourceType': dst, 'synthid_text': (b'SynthID' in b)}


def khop_mau(ai, render, vung):
    """khớp màu kiểu Reinhard (Lab, TB + độ lệch chuẩn) của ảnh AI về thống kê render trên vùng 'vung' (lớp (c)) — chỉ đổi điểm ảnh AI, không chạm lớp (a)."""
    a = cv2.cvtColor(ai, cv2.COLOR_BGR2LAB).astype(np.float32); r = cv2.cvtColor(render, cv2.COLOR_BGR2LAB).astype(np.float32)
    for c in range(3):
        ma, sa = a[..., c][vung].mean(), a[..., c][vung].std() + 1e-6; mr, sr = r[..., c][vung].mean(), r[..., c][vung].std() + 1e-6
        a[..., c] = (a[..., c] - ma) * (sr / sa) + mr
    return cv2.cvtColor(np.clip(a, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)


def lech_vien(render, ghep, A, amin=400):
    """độ khớp ánh sáng nền ↔ vật render: với mỗi cụm (a) ≥ amin px, ΔE76 giữa màu TB vòng NGOÀI (4–12 px) của khung ghép và của render
    (= nền quanh vật đổi bao nhiêu so với nền render mà vật được chiếu sáng cùng). Trả trung vị + p90 (theo cụm) + số cụm."""
    n, cc, st, _ = cv2.connectedComponentsWithStats(A.astype(np.uint8), 8)
    lr = cv2.cvtColor(render, cv2.COLOR_BGR2LAB).astype(np.float32) * np.array([100 / 255, 1, 1], np.float32)
    lg = cv2.cvtColor(ghep, cv2.COLOR_BGR2LAB).astype(np.float32) * np.array([100 / 255, 1, 1], np.float32)
    K4, K12 = np.ones((9, 9), np.uint8), np.ones((25, 25), np.uint8); vals = []
    big = [i for i in range(1, n) if st[i, 4] >= amin]
    for i in big[:400]:
        x, y, w, h = st[i, :4]; x0, y0, x1, y1 = max(0, x - 14), max(0, y - 14), min(A.shape[1], x + w + 14), min(A.shape[0], y + h + 14)
        m = (cc[y0:y1, x0:x1] == i).astype(np.uint8); ring = (cv2.dilate(m, K12) > 0) & ~(cv2.dilate(m, K4) > 0) & ~A[y0:y1, x0:x1]
        if ring.sum() < 20: continue
        vals.append(float(np.linalg.norm(lg[y0:y1, x0:x1][ring].mean(0) - lr[y0:y1, x0:x1][ring].mean(0))))
    if not vals: return dict(so_cum=0)
    return dict(so_cum=len(vals), dE_trung_vi=round(float(np.median(vals)), 2), dE_p90=round(float(np.percentile(vals, 90)), 2))
