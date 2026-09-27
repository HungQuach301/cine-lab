"""Ghép model sheet Ida/Cas + bảng silhouette C2 và đo chỉ số silhouette bằng máy.
Chạy: /opt/cine/bin/python design/cong3/model-sheet/assemble.py (sau khi render vào model-sheet/render/).
Chỉ số máy (đại diện, KHÔNG thay kiểm C2 bằng khán giả):
  - IoU giữa hai silhouette sau khi chuẩn hoá (cùng chân đế, cùng chiều cao): thấp = hai tư thế khác nhau rõ.
  - Tỷ lệ chi tách khối = phần diện tích bị mất khi mở hình thái học (opening) bằng đĩa bán kính 0,3 H (≈ nửa bề rộng thân hẹp nhất; 0,5 H làm mất cả thân gầy của Cas): phần chi/đạo cụ
    vươn ra khỏi khối thân — càng cao, hành động càng dễ đọc trong silhouette.
"""
import json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, 'render')
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font = lambda s, b=False: ImageFont.truetype(FB if b else F, s)
PAPER, INK = (236, 231, 222), (40, 36, 34)

def sil_mask(name):
    a = np.asarray(Image.open(os.path.join(R, f'sil_{name}.png')).convert('L')) < 128
    return a

def normalize(m, size=400):
    ys, xs = np.nonzero(m); y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    crop = m[y0:y1 + 1, x0:x1 + 1]; h = y1 - y0 + 1
    s = size / h; w = max(1, int(round(crop.shape[1] * s)))
    im = Image.fromarray((crop * 255).astype(np.uint8)).resize((w, size), Image.NEAREST)
    canvas = np.zeros((size, size * 2), bool); off = size - w // 2
    canvas[:, max(0, off):max(0, off) + w] = np.asarray(im)[:, : size * 2 - max(0, off)] > 127
    return canvas

def iou(a, b): return float((a & b).sum() / max(1, (a | b).sum()))

def limb_ratio(m, head_px):
    r = max(2, int(head_px * 0.3)); yy, xx = np.mgrid[-r:r + 1, -r:r + 1]; disk = xx ** 2 + yy ** 2 <= r * r
    opened = ndimage.binary_opening(m, structure=disk)
    return float((m & ~opened).sum() / max(1, m.sum()))

def main():
    ida = json.load(open(os.path.join(HERE, 'ida.json'))); cas = json.load(open(os.path.join(HERE, 'cas.json')))
    out = {}
    for who, sheet, poses in (('ida', ida, ['walk_ladder', 'warm_hands', 'crouch_lantern', 'look_shadows']),
                              ('cas', cas, ['shadow_bird', 'look_lantern', 'hold_ladder', 'warm_hands_copy', 'half_raised'])):
        # đầu cao bao nhiêu px trong khung (camera trực giao 2,15 m cho 1000 px)
        head_px = sheet['H_m'] * 1000 / 2.15
        masks = {p: sil_mask(f'{who}_pose_{p}') for p in poses}
        norms = {p: normalize(m) for p, m in masks.items()}
        pair = {f'{a}~{b}': round(iou(norms[a], norms[b]), 3) for i, a in enumerate(poses) for b in poses[i + 1:]}
        limbs = {p: round(limb_ratio(m, head_px), 3) for p, m in masks.items()}
        out[who] = {'iou_giua_tu_the': pair, 'iou_lon_nhat': max(pair.values()), 'ty_le_chi_tach_khoi': limbs}
    # khác biệt giữa hai nhân vật ở cùng loại tư thế đứng (turnaround chưa render silhouette → dùng look_shadows vs half_raised)
    a, b = normalize(sil_mask('ida_pose_look_shadows')), normalize(sil_mask('cas_pose_half_raised'))
    out['ida_vs_cas_dung'] = round(iou(a, b), 3)
    json.dump(out, open(os.path.join(HERE, 'c2-silhouette-metrics.json'), 'w'), indent=1, ensure_ascii=False)

    def sheet_img(who, sheet, poses, fname):
        cw, ch = 350, 500
        cols = max(4, len(poses)); W = cw * cols + 40; Hh = 90 + ch + 50 + ch + 50 + 260
        im = Image.new('RGB', (W, Hh), PAPER); d = ImageDraw.Draw(im)
        d.text((20, 18), f"MODEL SHEET — {sheet['name']} ({sheet['age']})  ·  {sheet['id']}", font=font(30, True), fill=INK)
        d.text((20, 58), 'Cổng 3 vòng 1 · đề xuất của Claude, chưa duyệt · ánh sáng studio trung tính (không phải ánh sáng phim)', font=font(17), fill=(110, 100, 95))
        y = 90
        for k, v in enumerate(['front', 'q34', 'side', 'back']):
            t = Image.open(os.path.join(R, f'{who}_{v}.png')).resize((cw, ch), Image.LANCZOS); im.paste(t, (20 + k * cw, y))
            d.text((30 + k * cw, y + ch + 8), {'front': 'Chính diện', 'q34': '3/4', 'side': 'Nghiêng', 'back': 'Sau lưng'}[v], font=font(18, True), fill=INK)
        y += ch + 50
        for k, p in enumerate(poses):
            t = Image.open(os.path.join(R, f'{who}_pose_{p}.png')).resize((cw, ch), Image.LANCZOS); im.paste(t, (20 + k * cw, y))
            lab = sheet['poses'][p]['label']; d.text((30 + k * cw, y + ch + 8), lab.split(' — ')[0] + ' — ' + lab.split(' — ')[1].split('(')[0].split(',')[0][:30], font=font(15, True), fill=INK)
        y += ch + 50
        # bảng tỷ lệ + màu
        P = sheet['parts']; d.text((20, y), 'Tỷ lệ (H = chiều cao đầu, đo giữa hai tâm khớp) — dữ liệu cho luật C3:', font=font(18, True), fill=INK)
        items = [(k, P[k]['length']) for k in sheet['measured_parts']]
        d.text((20, y + 30), '   '.join(f'{k} {v:.2f}' for k, v in items) + f"   ·  cao {sheet['total_height_H']:.2f} H = {sheet['total_height_H'] * sheet['H_m']:.2f} m", font=font(17), fill=INK)
        d.text((20, y + 64), 'Nét silhouette: ' + ' · '.join(sheet['silhouette_keys'][:3]), font=font(15), fill=(80, 72, 68))
        d.text((20, y + 88), '                        ' + ' · '.join(sheet['silhouette_keys'][3:]), font=font(15), fill=(80, 72, 68))
        x = 20
        for k, v in sheet['local_colors'].items():
            if k.startswith('_'): continue
            d.rectangle((x, y + 130, x + 60, y + 190), fill=v, outline=(60, 60, 60)); d.text((x, y + 196), k, font=font(13), fill=INK); d.text((x, y + 214), v, font=font(12), fill=(90, 90, 90)); x += 110
        im.save(os.path.join(HERE, fname), optimize=True)

    sheet_img('ida', ida, ['walk_ladder', 'warm_hands', 'crouch_lantern', 'look_shadows'], 'MS-ida.png')
    sheet_img('cas', cas, ['shadow_bird', 'look_lantern', 'hold_ladder', 'warm_hands_copy', 'half_raised'], 'MS-cas.png')

    # bảng silhouette C2
    names = [('ida', p) for p in ['walk_ladder', 'warm_hands', 'crouch_lantern', 'look_shadows']] + [('cas', p) for p in ['shadow_bird', 'look_lantern', 'hold_ladder', 'warm_hands_copy', 'half_raised']]
    cw, ch = 300, 430; im = Image.new('RGB', (cw * 5 + 40, 80 + 2 * (ch + 70)), 'white'); d = ImageDraw.Draw(im)
    d.text((20, 18), 'KIỂM SILHOUETTE (C2) — tô đen đặc từng tư thế then chốt', font=font(28, True), fill=INK)
    for k, (who, p) in enumerate(names):
        r, c = divmod(k, 5) if k < 5 else (1, k - 4) if False else divmod(k, 5)
        t = Image.open(os.path.join(R, f'sil_{who}_pose_{p}.png')).convert('L').resize((cw, ch), Image.LANCZOS)
        x, y = 20 + c * cw, 70 + r * (ch + 70); im.paste(t, (x, y))
        sheet = ida if who == 'ida' else cas; lab = sheet['poses'][p]['label'].split(' — ')
        d.text((x + 6, y + ch + 4), lab[0] + ' — ' + lab[1].split('(')[0].split(',')[0][:28], font=font(14, True), fill=INK)
        d.text((x + 6, y + ch + 24), f"chi tách khối {out[who]['ty_le_chi_tach_khoi'][p]:.2f}", font=font(13), fill=(90, 90, 90))
    im.save(os.path.join(HERE, 'C2-silhouettes.png'), optimize=True)
    print(json.dumps(out, indent=1, ensure_ascii=False))

if __name__ == '__main__':
    main()
