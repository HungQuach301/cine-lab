#!/opt/cine/bin/python
"""KÊNH 2 · trang văn bản DỰNG LẠI CHỮ cho module photo/doc (K2C-T1-06, 13/10/2026): khi không nên chụp trang gốc (văn bản luật xây dựng có bản quyền ICC,
trang web eCFR), dựng một trang giấy chỉ chứa đoạn trích nguyên văn (đã đối chiếu nguồn), kèm dòng ghi chú "re-typeset excerpt, not a facsimile".
Ra cùng định dạng với `k2v_assets.py doc`: <cache>/<id>-p1.png + <id>-p1.json {img, page, aspect, hl:[{find, rects:[[x0,y0,x1,y1] chuẩn hoá]}]}.
  textpage.py <spec.json>     spec: {id, lines: [{s, size, bold, center, gap, hl (chỉ số highlight), col: [[s, x], ...] (dòng bảng)}], note}"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont
CACHE = os.environ.get('K2V_CACHE', '/var/tmp/cine-out/k2v-cache')
SERIF = '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'; SERIFB = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'


def main():
    S = json.load(open(sys.argv[1])); W, H = 1700, 2200; M = 150
    im = Image.new('RGB', (W, H), (246, 242, 232)); g = ImageDraw.Draw(im); y = M; hl = {}
    for L in S['lines']:
        f = ImageFont.truetype(SERIFB if L.get('bold') else SERIF, L.get('size', 34)); y += L.get('gap', 0)
        if L.get('col'):
            boxes = []
            for s, x in L['col']:
                xx = M + x * (W - 2 * M); g.text((xx, y), s, font=f, fill=(28, 26, 24)); b = g.textbbox((xx, y), s, font=f); boxes.append(b)
            b = (min(q[0] for q in boxes), min(q[1] for q in boxes), max(q[2] for q in boxes), max(q[3] for q in boxes)); h = max(q[3] for q in boxes) - y
        else:
            words = L['s'].split(); lines = []; cur = ''
            for w in words:
                t = (cur + ' ' + w).strip()
                if g.textlength(t, font=f) > W - 2 * M and cur: lines.append(cur); cur = w
                else: cur = t
            lines.append(cur); bs = []
            for ln in lines:
                x = (W - g.textlength(ln, font=f)) / 2 if L.get('center') else M
                g.text((x, y), ln, font=f, fill=(28, 26, 24)); bs.append(g.textbbox((x, y), ln, font=f)); y += int(f.size * 1.42)
            b = None; h = 0
            if 'hl' in L: hl.setdefault(L['hl'], []).extend([[round(q[0] / W, 4), round((q[1] - 4) / H, 4), round(q[2] / W, 4), round((q[3] + 4) / H, 4)] for q in bs])
            continue
        if 'hl' in L: hl.setdefault(L['hl'], []).append([round(b[0] / W, 4), round((b[1] - 4) / H, 4), round(b[2] / W, 4), round((b[3] + 4) / H, 4)])
        y += int(h * 1.6)
    if S.get('note'):
        f = ImageFont.truetype(SERIF, 26); g.text((M, H - M), S['note'], font=f, fill=(110, 104, 96))
    out = os.path.join(CACHE, f"{S['id']}-p1"); im.save(out + '.png')
    meta = dict(img=out + '.png', page=1, aspect=round(W / H, 5), hl=[dict(find=f'hl{k}', rects=v) for k, v in sorted(hl.items())], source=S.get('source'), retypeset=True)
    json.dump(meta, open(out + '.json', 'w'), indent=1, ensure_ascii=False); print(out + '.json')


if __name__ == '__main__':
    main()
