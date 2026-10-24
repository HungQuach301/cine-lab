#!/opt/cine/bin/python -I
"""ANIMATIC-T4 · KIỂM TẦNG 1 (Q3 điểm 7: Gemini Flash trước, rồi mới mô hình đắt) cho ảnh đầu và clip minh hoạ M-d.
gemini-3.8-flash nhìn ảnh (ảnh tĩnh, hoặc 3 khung 25/55/90 % của clip + ảnh đầu tham chiếu) và liệt kê: lỗi thời đại (năm xuất hiện > năm cảnh), chữ/số/biển/logo/watermark/nhãn AI,
cờ, công trình có tên/nhận ra được mới, tàu lớn, mặt/tay người méo, thi thể/máu/người trong lửa ở cận, và KHỚP LỜI (khung có minh hoạ đúng câu lời của shot không).
Kết luận máy: LOẠI nếu có mục lỗi độ tin ≥ 0,5; còn lại ĐẠT-T1 (chuyển tầng 2 = kiem_minh_hoa.py: gpt-6.1-sol + claude-sonnet-5-5 + checks/ll/q_thoi_dai.py).
Danh sách cấm: scripts/k2ldn/ai/cam_thoi_dai.json (chung trước 1850 + t4_1666 cho 1666–1700 + ai_da_bia). Sổ: gem_lib (usd thật).
  gem_kiem.py --anh a.jpg [--clip c.mp4] --nam 1666 --canh "<cảnh>" --loi "<câu lời>" --tag H1-02-a1 --out <thư mục>"""
import argparse, base64, json, sys, tempfile
from pathlib import Path
import cv2
sys.path.insert(0, str(Path(__file__).resolve().parent)); import gem_lib as G  # noqa: E402
MODEL = 'gemini-3.8-flash'
PROMPT = """You are a strict inspector for a historical documentary about London. Each image below is either a still or a frame from a short illustrative video clip.
Scene: {canh}. Year of the scene: {nam}. Narration heard over this shot: "{loi}".
{ref}
Check EVERY image (look closely at all corners and at small details) and list every problem in these categories (use only these keys for "loai"):
"thoi_dai" (object, clothing, vehicle, material, lighting or structure that did not exist in {nam}; give the year it first appeared),
"chu" (any text, letters, numbers, signs, shop names, posters, logos, watermarks, captions or AI labels),
"co" (flags, banners), "cong_trinh_ten" (identifiable famous landmark: dome, named cathedral, bridge, tower, monument) that is NOT in the reference image,
"tau_lon" (sea-going ship larger than a small rowing boat or barge), "mat_meo" (distorted or melted faces, extra or missing limbs/fingers, merged bodies),
"cam_hinh" (dead body, blood, wounded person, or a person inside flames shown close), "khong_khop" (the image contradicts the scene or the narration: wrong place, period, season, time of day or event; an image that illustrates the general situation around the narration is FINE and must not be listed), "khac" (anything else clearly wrong).
Forbidden for this year (and your own knowledge): {cam}
Ordinary period things are fine and must NOT be listed.
Answer ONLY with one JSON object: {{"mo_ta": "<one sentence>", "muc": [{{"anh": <image number starting at 1>, "loai": "<key>", "mo_ta": "<what>", "nam_xuat_hien": <year or null>, "do_tin": <0-1>}}]}}"""


def frames(clip, out, tag):
    cap = cv2.VideoCapture(str(clip)); n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); fps = cap.get(cv2.CAP_PROP_FPS) or 24; ps = []
    for u in (0.25, 0.55, 0.90):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(u * (n - 1))); ok, im = cap.read()
        if ok: p = Path(out) / f'{tag}-k{int(u * 100):02d}.jpg'; cv2.imwrite(str(p), im, [cv2.IMWRITE_JPEG_QUALITY, 92]); ps.append(p)
    return ps, n, fps


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--anh', required=True); ap.add_argument('--clip'); ap.add_argument('--nam', required=True); ap.add_argument('--canh', required=True)
    ap.add_argument('--loi', default=''); ap.add_argument('--tag', required=True); ap.add_argument('--out', required=True); a = ap.parse_args()
    G.kiem_truoc(0.05); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    C = json.loads((G.REPO / 'scripts/k2ldn/ai/cam_thoi_dai.json').read_text()); nam = float(a.nam)
    cam = (C['chung'] if nam < 1850 else []) + (C['t4_1666'] if nam < 1700 else []) + C['ai_da_bia']
    imgs = [Path(a.anh)]; ref = 'Image 1 is a still.'; meta = {}
    if a.clip:
        fr, n, fps = frames(a.clip, out, a.tag); imgs = [Path(a.anh)] + fr; meta = {'so_khung': n, 'fps': fps, 'giay': round(n / fps, 2)}
        ref = 'Image 1 is the REFERENCE first frame we supplied (anything in it is allowed). Images 2-4 are frames of the generated clip — inspect those.'
    pr = PROMPT.format(canh=a.canh, nam=int(nam), loi=a.loi.replace('"', "'"), ref=ref, cam='; '.join(cam))
    parts = [{'inline_data': {'mime_type': 'image/jpeg', 'data': base64.b64encode(cv2.imencode('.jpg', cv2.resize(cv2.imread(str(p)), (1280, 720)), [cv2.IMWRITE_JPEG_QUALITY, 90])[1].tobytes()).decode()}} for p in imgs]
    body = {'contents': [{'role': 'user', 'parts': parts + [{'text': pr}]}], 'generationConfig': {'responseMimeType': 'application/json', 'temperature': 0}}
    st, raw = G.req('POST', f'{G.API}/models/{MODEL}:generateContent', body, timeout=300)
    try: J = json.loads(raw)
    except Exception: J = {'raw': raw[:500].decode('utf8', 'replace')}
    rec = {'tag': a.tag + '-flash', 'nha': 'gemini', 'model_req': MODEL, 'muc_dich': 'kiểm tầng 1', 'prompt': pr, 'input': [{'file': str(p), 'sha256': G.sha(p.read_bytes())} for p in imgs], 'http': st}
    if st != 200:
        rec.update(loi=str(J)[:400], usd=0.0); G.log(rec); G.dung_neu_402(st, J, a.tag); sys.exit(f'LỖI {st}')
    u = J.get('usageMetadata'); rec.update(usage=u, usd=G.usd_of(MODEL, u) or 0.0, model_resp=J.get('modelVersion'))
    txt = ''.join(p.get('text', '') for p in J['candidates'][0]['content']['parts']) if J.get('candidates') else ''
    try: R = json.loads(txt)
    except Exception: R = {'mo_ta': None, 'muc': [], 'loi_doc': txt[:300]}
    G.log(rec)
    loi = [m for m in R.get('muc', []) if (m.get('do_tin') or 0) >= 0.5 and (m.get('loai') != 'thoi_dai' or (isinstance(m.get('nam_xuat_hien'), (int, float)) and m['nam_xuat_hien'] > nam) or m.get('nam_xuat_hien') is None)
           and m.get('loai') != 'khac' and not (a.clip and m.get('anh') == 1)]
    kq = {'tag': a.tag, 'tang': 1, 'model': MODEL, 'nam': nam, 'canh': a.canh, 'loi_cau': a.loi, **meta, 'mo_ta': R.get('mo_ta'), 'muc': R.get('muc', []), 'loi': loi, 'ket_luan': 'LOẠI' if loi else 'ĐẠT-T1', 'usd': rec['usd']}
    (out / f'{a.tag}-t1.json').write_text(json.dumps(kq, ensure_ascii=False, indent=1))
    print(json.dumps({k: kq[k] for k in ('tag', 'ket_luan', 'usd')} | {'loi': [f"{m.get('loai')}: {m.get('mo_ta')}" for m in loi][:6]}, ensure_ascii=False))


if __name__ == '__main__': main()
