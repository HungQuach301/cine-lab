#!/opt/cine/bin/python -I
"""ANIMATIC-T3-V2 · BỘ KIỂM ĐOẠN MINH HOẠ N2 (toàn khung AI, image-to-video) — dựng trên bộ kiểm NC-N2P (vision_kiem.py: HAI MÔ HÌNH NHÌN KHÁC NHAU gpt-6.1-sol + claude-sonnet-5-5,
cùng đề bài + cùng ảnh toàn khung 1568×882 + 4 ô phóng 1,5×; danh sách CẤM cam_thoi_dai.json) + checks/ll/q_thoi_dai.py của K (chỉ CHẠY, không đọc mã).
Khác NC-N2P: đoạn minh hoạ là ẢNH MỚI toàn khung (không ghép lớp (a)) → câu hỏi không là "thêm/bớt so với render" mà là:
  (1) LỖI THỜI ĐẠI có năm xuất hiện > năm khung (máy kết luận; không kèm năm → "nghi vấn" cho người);
  (2) VẬT BỊA MANG DỮ KIỆN (luật N2 + lệnh 21/10): cờ/biểu ngữ, công trình nhận ra được/có tên, tàu lớn đi biển, chữ/số/biển hiệu/logo — MỚI so với ảnh đầu (render của ta) → LỖI;
  (3) cấm hình: thi thể, máu, người trong khói/lửa ở cận → LỖI.
Mỗi lượt: 3 khung (25 %, 55 %, 90 % độ dài clip). Máy kết luận ĐẠT/LOẠI; người đọc tờ so vẫn bắt buộc.
Chặn chi phí phiên: OpenAI tổng ≥ $15 → dừng; Claude tổng ≥ $30 → dừng (sổ reports/tien-ky-t4/cost.jsonl).
  kiem_minh_hoa.py --dau dau.png --clip ra.mp4 --nam 1780 --canh "<mô tả cảnh>" --tag M1-l1 --out <thư mục> [--mo-hinh gpt,claude] [--qtd 1]"""
import argparse, json, subprocess, sys, tempfile, time
from pathlib import Path
import cv2
sys.path.insert(0, str(Path(__file__).resolve().parent))
import n2p_lib as L  # noqa: E402
import vision_kiem as VK  # noqa: E402
REPO = L.REPO
LOAI = {'co': 'flag, banner, ensign or pennant', 'cong_trinh_ten': 'identifiable or famous landmark building, tower, church, castle, lighthouse, bridge or monument',
        'tau_lon': 'sea-going ship (any vessel larger than a rowing boat or small fishing boat)', 'chu': 'text, letters, numbers, sign, plaque, logo, watermark',
        'thoi_dai': 'object, clothing, vehicle, material or structure that did not exist in the given year', 'cam_hinh': 'dead body, blood, wounded person, or a person inside smoke or flames shown close',
        'khac': 'anything else that looks wrong for the scene'}
PROMPT = """You are a strict inspector for a historical documentary. The film uses short AI-generated ILLUSTRATION clips (labelled "Illustration" on screen) that must carry NO historical facts by themselves.
The scene: {canh}. Place: {noi}. Year: {nam}.
Read ALL the image files below with the Read tool before answering (paths are absolute):
REFERENCE = the first frame we supplied (our own 3D render; whatever is in it is allowed):
{dau}
FRAME = a frame of the AI clip (full frame + 4 enlarged quarters: q1 top-left, q2 top-right, q3 bottom-left, q4 bottom-right):
{khung}
List every item in FRAME that falls in one of these categories, using ONLY these keys for "loai": {loai}.
For each item say whether the SAME object is already visible in REFERENCE ("co_trong_dau": true/false).
For anachronisms give the year the thing first appeared ("nam_xuat_hien"), and check against this list of forbidden things (and your own knowledge):
{cam}
Ignore ordinary things that fit the year (period clothing, barrels, crates, sacks, small rowing boats, carts, stone walls without identity, rocks, vegetation, smoke from chimneys or distant guns).
Give each item's bounding box in FULL-frame normalized coordinates [x0, y0, x1, y1] (convert from quarters: full = quarter offset + 0.5 x quarter coordinate).
Answer with ONLY one JSON object, no other text:
{{"mo_ta": "<one sentence: what the frame shows>", "muc": [{{"loai": "<key>", "mo_ta": "<what>", "co_trong_dau": true|false, "toa_do": [x0, y0, x1, y1], "nam_xuat_hien": <year or null>, "do_tin": <0-1>}}]}}"""


def tong(prefix): return VK.spent(prefix)


def ket_luan(items, nam):
    loi, nghi = [], []
    for it in items:
        if (it.get('do_tin') or 0) < 0.5: continue
        k = it.get('loai'); moi = not it.get('co_trong_dau')
        if k == 'thoi_dai':
            y = it.get('nam_xuat_hien')
            if isinstance(y, (int, float)) and y > float(nam): loi.append(it)
            elif y is None: nghi.append(it)
        elif k in ('co', 'cong_trinh_ten', 'tau_lon', 'chu') and moi: loi.append(it)
        elif k == 'cam_hinh': loi.append(it)
        elif k == 'khac': nghi.append(it)
    return loi, nghi


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--dau', required=True); ap.add_argument('--clip', required=True); ap.add_argument('--nam', required=True); ap.add_argument('--canh', required=True)
    ap.add_argument('--noi', default='Gibraltar'); ap.add_argument('--tag', required=True); ap.add_argument('--out', required=True); ap.add_argument('--mo-hinh', default='gpt,claude'); ap.add_argument('--qtd', default='1')
    ap.add_argument('--chi-qtd', action='store_true', help='giữ kết quả 2 mô hình đã có trong <tag>-kiem.json, chỉ chạy lại q_thoi_dai')
    a = ap.parse_args(); out = Path(a.out).resolve(); out.mkdir(parents=True, exist_ok=True); a.clip = str(Path(a.clip).resolve()); a.dau = str(Path(a.dau).resolve())
    if tong('gpt') >= 15: sys.exit('CHẶN OpenAI $15');
    if tong('claude') >= 25: sys.exit('CHẶN Claude $25')
    cap = cv2.VideoCapture(a.clip); n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); fps = cap.get(cv2.CAP_PROP_FPS) or 24; fr = []
    for u in (0.25, 0.55, 0.90):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(u * (n - 1))); ok, im = cap.read()
        if ok: p = out / f'{a.tag}-k{int(u * 100):02d}.png'; cv2.imwrite(str(p), im); fr.append((u, p))
    C = json.load(open(Path(__file__).parent / 'cam_thoi_dai.json')); cam = (C['chung'] if float(a.nam) < 1850 else []) + C['ai_da_bia']
    cu = json.loads((out / f'{a.tag}-kiem.json').read_text()) if a.chi_qtd and (out / f'{a.tag}-kiem.json').exists() else None
    res = dict(tag=a.tag, clip=a.clip, clip_sha=L.sha_file(a.clip), dau=a.dau, dau_sha=L.sha_file(a.dau), nam=a.nam, canh=a.canh, so_khung=n, fps=fps, prompt_sha=L.sha(PROMPT.encode()), khung=[])
    for u, p in fr:
        K = dict(u=u, anh=str(p), mo_hinh={})
        old = [k for k in (cu or {}).get('khung', []) if k['u'] == u]
        if old: K['mo_hinh'] = old[0]['mo_hinh']
        else:
          with tempfile.TemporaryDirectory() as td:
              d = Path(td); T = VK.tiles(a.dau, d, 'reference')[:1]; S = VK.tiles(p, d, 'frame')
              pr = PROMPT.format(canh=a.canh, noi=a.noi, nam=a.nam, dau='\n'.join(f'- {x}' for x in T), khung='\n'.join(f'- {x}' for x in S), cam='\n'.join(f'- {x}' for x in cam),
                                 loai=', '.join(f'"{k}" ({v})' for k, v in LOAI.items()))
              for mh in a.mo_hinh.split(','):
                  t0 = time.time()
                  if mh == 'gpt': txt, meta = VK.call_gpt(pr.replace('Read ALL the image files below with the Read tool before answering (paths are absolute):', 'The images are attached in this order:'), T + S, f'{a.tag}-k{int(u * 100)}-gpt')
                  else: txt, meta = VK.call_claude(pr, T + S, f'{a.tag}-k{int(u * 100)}-claude')
                  (out / f'{a.tag}-k{int(u * 100):02d}-{mh}.raw.txt').write_text(txt or ''); J = VK.parse(txt) or {}
                  lo, ng = ket_luan(J.get('muc', []), a.nam)
                  K['mo_hinh'][mh] = dict(meta=meta, secs=round(time.time() - t0, 1), mo_ta=J.get('mo_ta'), muc=J.get('muc', []), loi=lo, nghi_van=ng, doc_duoc=bool(J))
        if a.qtd == '1':
            q = out / f'qtd-{a.tag}-k{int(u * 100):02d}.json'
            r = subprocess.run([sys.executable, str(REPO / 'checks/ll/q_thoi_dai.py'), '--anh', str(p), '--nam', str(int(float(a.nam))), '--noi', a.noi, '--out', str(out / f'qtd-{a.tag}'), '--api', '--json', str(q)],
                               capture_output=True, text=True, cwd=str(REPO))
            K['q_thoi_dai'] = json.loads(q.read_text()) if q.exists() else {'loi': (r.stderr or r.stdout)[-400:]}
        res['khung'].append(K)
    loi = [(k['u'], mh, x) for k in res['khung'] for mh, v in k['mo_hinh'].items() for x in v['loi']]
    qn = []
    for k in res['khung']:
        q = k.get('q_thoi_dai') or {}
        for f in (q.get('khung') or q.get('frames') or []):
            for x in (f.get('nghi_van') or []): qn.append((k['u'], x))
        if isinstance(q.get('nghi_van'), list): qn += [(k['u'], x) for x in q['nghi_van']]
    doc = all(v['doc_duoc'] for k in res['khung'] for v in k['mo_hinh'].values())
    qthieu = sum(1 for k in res['khung'] if a.qtd == '1' and not ((k.get('q_thoi_dai') or {}).get('ok') and not (k.get('q_thoi_dai') or {}).get('thieu')))
    res['ket_luan_may'] = dict(loi_mo_hinh=len(loi), q_thoi_dai_nghi_van=len(qn), mo_hinh_doc_duoc=doc, q_thoi_dai_thieu=qthieu, ket_qua='LOẠI' if (loi or qn) else ('THIẾU' if (qthieu or not doc) else 'ĐẠT'),
                               chi_tiet=[dict(u=u, mo_hinh=mh, loai=x.get('loai'), mo_ta=x.get('mo_ta'), nam=x.get('nam_xuat_hien')) for u, mh, x in loi] + [dict(u=u, mo_hinh='q_thoi_dai', mo_ta=json.dumps(x, ensure_ascii=False)[:200]) for u, x in qn])
    (out / f'{a.tag}-kiem.json').write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(a.tag, res['ket_luan_may']['ket_qua'], 'lỗi mô hình', len(loi), 'q_thoi_dai', len(qn), 'đọc được', doc)


if __name__ == '__main__': main()
