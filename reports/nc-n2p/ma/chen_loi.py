#!/opt/cine/bin/python -I
"""NC-N2P · KIỂM CÓ ĐÁP ÁN: chèn CỐ Ý 6 lỗi vào khung thử (render cổng 'cang', cách A, 1920×1080) — 3 lỗi thời đại + 2 vật lớp (a) + 1 người trên tấm tĩnh.
Mỗi vật: một lệnh OpenAI images/edits (mặt nạ = hộp chữ nhật được sửa) → chỉ lấy điểm ảnh TRONG HỘP và NGOÀI lớp (a) (viền mềm 4 px) dán lên render;
mọi điểm ảnh khác của khung thử = render (đáp án sạch). Ra: khung thử + dap-an.json (hộp, loại lỗi mong đợi).
  chen_loi.py --out <thư mục>"""
import argparse, json, subprocess, sys
from pathlib import Path
import cv2, numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
import n2p_lib as L  # noqa: E402

BASE = L.REPO / 'reports/nc-cpu/khung/A/cong-cang.jpg'; ID = L.N2P / 'o1/mat-na/id-cang.png'
VAT = [
 dict(id='L1', loai_loi='thoi_dai', hop=[1300, 120, 1560, 260], p='a modern white twin-engine passenger airliner flying in the sky, seen from the side, realistic, small in the distance'),
 dict(id='L2', loai_loi='thoi_dai', hop=[150, 230, 330, 330], p='a modern red hatchback car parked on the rocky hillside, realistic, correct scale for the distance'),
 dict(id='L3', loai_loi='thoi_dai', hop=[200, 120, 330, 270], p='a tall steel electricity pylon (transmission tower) with power lines on the hillside, realistic, correct scale'),
 dict(id='L4', loai_loi='lop_a', hop=[700, 640, 900, 800], p='one 18th-century three-masted sailing warship with white sails on the water, realistic, correct scale for the distance'),
 dict(id='L5', loai_loi='lop_a', hop=[480, 300, 540, 370], p='one tall wooden flagpole with a large red-and-white flag flying, on the hillside, realistic, correct scale'),
 dict(id='L6', loai_loi='dong_bang', hop=[330, 610, 400, 680], p='one man in 18th-century clothes walking on the grass, realistic, correct scale for the distance'),
]
PROMPT = ('This is a frame from our own 3D reconstruction of Gibraltar in January 1780. Add exactly this, inside the transparent area of the mask only: {p}. '
          'Match the lighting, haze and scale of the scene. Do not change anything outside the transparent area.')


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', required=True); a = ap.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    R = cv2.imread(str(BASE)); H, W = R.shape[:2]; Lb = L.idmap(ID, (W, H)); A = L.lop_mask(Lb, L.LOP_A); X = R.copy(); dap = []
    for v in VAT:
        x0, y0, x1, y1 = v['hop']; m = np.zeros((H, W, 4), np.uint8); m[..., 3] = 255; m[y0:y1, x0:x1, 3] = 0
        mp = out / f"mask-{v['id']}.png"; cv2.imwrite(str(mp), m); pf = out / f"lenh-{v['id']}.txt"; pf.write_text(PROMPT.format(p=v['p']) + '\n')
        ai = out / f"{v['id']}-ai.jpg"
        if not ai.exists():
            subprocess.run([sys.executable, '-I', str(Path(__file__).parent / 'oai_edit.py'), '--img', str(BASE), '--mask', str(mp), '--prompt-file', str(pf), '--tag', v['id'], '--out', str(out)], check=True)
        P = cv2.resize(cv2.imread(str(ai)), (W, H), interpolation=cv2.INTER_AREA)
        box = np.zeros((H, W), np.uint8); box[y0:y1, x0:x1] = 1
        al = cv2.GaussianBlur((box & ~A).astype(np.float32), (0, 0), 1.5) * (box & ~A)
        X = np.clip(X.astype(np.float32) * (1 - al[..., None]) + P.astype(np.float32) * al[..., None], 0, 255).astype(np.uint8)
        dap.append(dict(v, hop_chuan=[x0 / W, y0 / H, x1 / W, y1 / H], dE_tb=round(float(np.abs(P.astype(int) - R.astype(int))[y0:y1, x0:x1].mean()), 1)))
    X[A] = R[A]
    cv2.imwrite(str(out / 'khung-thu.png'), X); cv2.imwrite(str(out / 'khung-thu.jpg'), X, [cv2.IMWRITE_JPEG_QUALITY, 95])
    json.dump(dict(base=str(BASE.relative_to(L.REPO)), sha_base=L.sha_file(BASE), sha_khung_thu=L.sha_file(out / 'khung-thu.png'), vat=dap), open(out / 'dap-an.json', 'w'), ensure_ascii=False, indent=1)
    print('xong', [d['id'] for d in dap])


if __name__ == '__main__': main()
