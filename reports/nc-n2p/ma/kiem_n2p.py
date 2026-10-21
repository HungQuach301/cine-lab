#!/opt/cine/bin/python -I
"""NC-N2P · BỘ KIỂM N2+ cho một KHUNG (ảnh tĩnh O1 hoặc khung mẫu của video). Máy kết luận theo luật; mô hình nhìn (vision_kiem.py) chỉ liệt kê vật.
  (i)   LỚP (a) sau ghép: max |ghép − render| trong mặt nạ (a) (đạt khi < 1/255 ⇔ 0 ở 8 bit) · viền mềm ≤ 3 px · VẬT MỚI ở dải 20 px quanh vùng (a):
        (1) máy: thành phần ΔE76 ≥ 30 (ảnh mờ σ 1,5, so render) ≥ 80 px trong dải → số cụm + hộp (để người đọc tờ so); (2) mô hình: vật THÊM/BỚT/ĐỔI loại lớp (a)
        (cờ, công trình, công sự, tàu lớn, chữ, đèn, lửa lớn) — ở BẤT KỲ đâu = LỖI; nằm trong dải 20 px thì ghi 'dải (a)'.
  (ii)  LỖI THỜI ĐẠI: vật THÊM có thoi_dai_sai = true (do_tin ≥ 0,5) VÀ (năm xuất hiện mô hình nêu > năm khung, hoặc loại máy bay/xe máy) ở ÍT NHẤT MỘT trong hai
        mô hình (gpt-6.1-sol, claude-sonnet-5-5) → LỖI; cờ không kèm năm → 'nghi_van_khong_nam' (người đọc; sửa sau khi đo: mô hình gắn cờ cho vật 'bịa' không lỗi thời đại).
        (+ q_thoi_dai.py của K chạy riêng — xem báo cáo.)
  (iii) ĐỔI LOẠI VÙNG (T9 NC-V2V3): 'màu nước' HSV H 85–130, S ≥ 40, V ≥ 30; đất→nước = % điểm đất (bằng/sườn/đá/phố, mặt nạ) màu nước ở ghép mà render không;
        nước→đất = % điểm nước-màu-nước của render mất màu nước ở ghép; đạt khi mỗi chiều ≤ 2 % + mô hình không báo đổi vùng (do_tin ≥ 0,5) → báo.
  (iv)  ĐÓNG BĂNG (chỉ ẢNH TĨNH): vật THÊM loại chuyển động (người, động vật, chim, thuyền nhỏ, xe chạy, khói, lửa trại, máy bay, xe máy) ở ít nhất một mô hình → LỖI.
  kiem_n2p.py --render <render.jpg> --ai <ai.jpg> --id <mặt nạ V7C png> --nam 1780 --tag <nhãn> --out <thư mục> [--anh-tinh 1] [--khong-goi]"""
import argparse, json, subprocess, sys
from pathlib import Path
import cv2, numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
import n2p_lib as L  # noqa: E402

LOAI_A = {'co', 'cong_trinh', 'cong_su', 'tau_lon', 'chu', 'den', 'lua_lon'}
LOAI_DONG = {'nguoi', 'dong_vat', 'chim', 'thuyen_nho', 'xe_chay', 'khoi', 'lua_trai', 'may_bay', 'xe_may'}
TIN = 0.5
NAM = 0.0
LOAI_HIEN_DAI = {'may_bay', 'xe_may'}   # (ii) LỖI khi mô hình nêu năm xuất hiện > năm khung, hoặc loại vốn hiện đại; cờ thời đại KHÔNG kèm năm → 'nghi_van_khong_nam' (người đọc)


def lab(b): return cv2.cvtColor(b, cv2.COLOR_BGR2LAB).astype(np.float32) * np.array([100 / 255, 1, 1], np.float32) - np.array([0, 128, 128], np.float32)


def blue(bgr):
    h = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV); return (h[..., 0] >= 85) & (h[..., 0] <= 130) & (h[..., 1] >= 40) & (h[..., 2] >= 30)


def may(render, ghep, Lb):
    A = L.lop_mask(Lb, L.LOP_A)
    dif = np.abs(ghep.astype(np.int16) - render.astype(np.int16)).max(-1)
    k1 = dict(max_trong_a=int(dif[A].max()) if A.any() else 0, diem_lech_trong_a=int((dif[A] > 0).sum()), dien_tich_a_pct=round(float(A.mean() * 100), 2))
    band = (cv2.dilate(A.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41))) > 0) & ~A
    dE = np.sqrt(((lab(cv2.GaussianBlur(ghep, (0, 0), 1.5)) - lab(cv2.GaussianBlur(render, (0, 0), 1.5))) ** 2).sum(-1))
    m = (dE >= 30) & band; n, cc, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
    cum = sorted([dict(hop=[int(st[i, 0]), int(st[i, 1]), int(st[i, 0] + st[i, 2]), int(st[i, 1] + st[i, 3])], px=int(st[i, 4])) for i in range(1, n) if st[i, 4] >= 80], key=lambda x: -x['px'])
    k1.update(dai20_pct=round(float(band.mean() * 100), 2), dai20_cum_dE30=len(cum), dai20_cum_lon=cum[:15])
    D = L.lop_mask(Lb, L.DAT); Wt = Lb == L.NAMES.index('nuoc')
    br, bg = blue(render), blue(ghep)
    d2n = float((D & bg & ~br).sum() / max(1, D.sum()) * 100); n2d = float((Wt & br & ~bg).sum() / max(1, (Wt & br).sum()) * 100)
    # T9b (NC-N2P, sau khi đọc tờ so 'cang'): bỏ điểm LOÉ nắng (V ≥ 0,85, S ≤ 0,25 — mặt nước loé không phải đất) và dải ≤ 8 px quanh đường bờ của mặt nạ
    # (bọt sóng, mép bãi dời vài px); số gốc T9 vẫn ghi để so NC-V2V3.
    hs = cv2.cvtColor(ghep, cv2.COLOR_BGR2HSV); loe = (hs[..., 2] >= 217) & (hs[..., 1] <= 64)
    bo = cv2.dilate((cv2.morphologyEx(Wt.astype(np.uint8), cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)) > 0).astype(np.uint8), np.ones((17, 17), np.uint8)) > 0
    d2n_b = float((D & bg & ~br & ~bo).sum() / max(1, D.sum()) * 100); n2d_b = float((Wt & br & ~bg & ~loe & ~bo).sum() / max(1, (Wt & br).sum()) * 100)
    k3 = dict(dat_thanh_nuoc_pct=round(d2n, 2), nuoc_thanh_dat_pct=round(n2d, 2), t9b_dat_thanh_nuoc_pct=round(d2n_b, 2), t9b_nuoc_thanh_dat_pct=round(n2d_b, 2),
              dat=bool(d2n_b <= 2 and n2d_b <= 2))
    return k1, k3, band, A


def in_band(box, band):
    H, W = band.shape; x0, y0, x1, y1 = [int(round(v * s)) for v, s in zip(box, (W, H, W, H))]
    x0, y0 = max(0, x0), max(0, y0); x1, y1 = min(W, max(x1, x0 + 1)), min(H, max(y1, y0 + 1))
    return bool(band[y0:y1, x0:x1].any())


def ket_luan(V, band, A, anh_tinh):
    L1, L2, L2b, L4, VUNG = [], [], [], [], []
    for mh, r in (V or {}).items():
        j = r.get('json') or {}
        for x in j.get('them', []):
            if (x.get('do_tin') or 0) < TIN: continue
            b = x.get('toa_do') if isinstance(x.get('toa_do'), list) and len(x.get('toa_do')) == 4 else [0, 0, 1, 1]
            it = dict(mh=mh, loai=x.get('loai'), mo_ta=x.get('mo_ta'), toa_do=b, dai_a=in_band(b, band) or in_band(b, A))
            if x.get('loai') in LOAI_A: L1.append(dict(it, kieu='THÊM vật lớp (a)'))
            if x.get('thoi_dai_sai'):
                ny = x.get('nam_xuat_hien'); co_nam = isinstance(ny, (int, float)) and ny > NAM
                (L2 if (co_nam or x.get('loai') in LOAI_HIEN_DAI) else L2b).append(dict(it, ly_do=x.get('ly_do_thoi_dai'), nam=ny))
            if anh_tinh and x.get('loai') in LOAI_DONG: L4.append(it)
        for x in j.get('bot_doi', []):
            if (x.get('do_tin') or 0) < TIN: continue
            b = x.get('toa_do') if isinstance(x.get('toa_do'), list) and len(x.get('toa_do')) == 4 else [0, 0, 1, 1]
            if x.get('loai') in LOAI_A: L1.append(dict(mh=mh, loai=x.get('loai'), mo_ta=x.get('mo_ta'), toa_do=b, dai_a=in_band(b, band) or in_band(b, A), kieu='BỚT/ĐỔI vật lớp (a)'))
        for x in j.get('doi_loai_vung', []):
            if (x.get('do_tin') or 0) >= TIN: VUNG.append(dict(mh=mh, mo_ta=x.get('mo_ta'), toa_do=x.get('toa_do')))
    return L1, L2, L2b, L4, VUNG


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--render', required=True); ap.add_argument('--ai', required=True); ap.add_argument('--id', required=True); ap.add_argument('--nam', required=True)
    ap.add_argument('--tag', required=True); ap.add_argument('--out', required=True); ap.add_argument('--anh-tinh', type=int, default=1); ap.add_argument('--khong-goi', action='store_true')
    ap.add_argument('--da-ghep', action='store_true', help='--ai đã là khung ghép (không ghép lại)'); ap.add_argument('--noi', default='Gibraltar'); ap.add_argument('--t4', action='store_true'); ap.add_argument('--khop-mau', action='store_true', help='khớp màu AI về render trên lớp (c) trước khi ghép')
    a = ap.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    R = cv2.imread(a.render); AI = cv2.imread(a.ai); AI = cv2.resize(AI, (R.shape[1], R.shape[0]), interpolation=cv2.INTER_AREA) if AI.shape != R.shape else AI
    Lb = L.idmap(a.id, (R.shape[1], R.shape[0])); A = L.lop_mask(Lb, L.LOP_A)
    if a.khop_mau and not a.da_ghep: AI = L.khop_mau(AI, R, ~A)
    G = AI if a.da_ghep else L.ghep(R, AI, A, 3)[0]
    pg = out / f'{a.tag}-ghep.png'; cv2.imwrite(str(pg), G); cv2.imwrite(str(out / f'{a.tag}-ghep.jpg'), G, [cv2.IMWRITE_JPEG_QUALITY, 93])
    k1, k3, band, A = may(R, G, Lb); k1['khop_anh_sang_vien'] = L.lech_vien(R, G, A); k1['khop_mau'] = bool(a.khop_mau)
    vj = out / f'{a.tag}-vision.json'
    if not a.khong_goi and not vj.exists():
        cmd = [sys.executable, '-I', str(Path(__file__).parent / 'vision_kiem.py'), '--truoc', a.render, '--sau', str(out / f'{a.tag}-ghep.jpg'), '--nam', str(a.nam), '--noi', a.noi, '--tag', a.tag, '--out', str(out)]
        if a.t4: cmd.append('--t4')
        subprocess.run(cmd, check=False)
    V = json.load(open(vj))['ket_qua'] if vj.exists() else {}
    global NAM; NAM = float(a.nam)
    L1, L2, L2b, L4, VUNG = ket_luan(V, band, A, a.anh_tinh)
    dong2 = lambda xs: sorted({x['mh'] for x in xs})
    R_ = dict(tag=a.tag, render=a.render, ai=a.ai, ghep=str(pg), sha_ghep=L.sha_file(pg), nam=a.nam,
              i_lop_a=dict(k1, dat_ghep=k1['max_trong_a'] == 0, vat_lop_a=L1, dat=k1['max_trong_a'] == 0 and not L1),
              ii_thoi_dai=dict(loi=L2, mo_hinh_bao=dong2(L2), nghi_van_khong_nam=L2b, dat=not L2),
              iii_doi_vung=dict(k3, mo_hinh_bao=VUNG, dat=k3['dat'] and not VUNG),
              iv_dong_bang=dict(ap_dung=bool(a.anh_tinh), loi=L4, mo_hinh_bao=dong2(L4), dat=not L4))
    R_['dat_ca'] = all(R_[k]['dat'] for k in ('i_lop_a', 'ii_thoi_dai', 'iii_doi_vung', 'iv_dong_bang'))
    json.dump(R_, open(out / f'{a.tag}-kiem.json', 'w'), ensure_ascii=False, indent=1)
    print(a.tag, 'viền', k1['khop_anh_sang_vien'], '(i)', 'ĐẠT' if R_['i_lop_a']['dat'] else f"LỖI max={k1['max_trong_a']} vat={len(L1)}", '| dải20 cụm', k1['dai20_cum_dE30'],
          '| (ii)', 'ĐẠT' if not L2 else f'LỖI {len(L2)}', '| (iii)', k3, len(VUNG), '| (iv)', 'ĐẠT' if not L4 else f'LỖI {len(L4)}')


if __name__ == '__main__': main()
