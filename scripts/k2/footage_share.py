#!/opt/cine/bin/python
"""KÊNH 2 · kiểm FOOTAGE THẬT theo Kinh thánh §4 (F3, chủ dự án duyệt 14/10/2026 22:11; phiên V4).
  footage_share.py <spec.yaml> [--licenses <thư mục>] [--json out.json]
Đo trên đặc tả (định dạng episode kênh 2):
  (1) tỷ lệ thời lượng shot type: footage / tổng ≤ 20 %;
  (2) mỗi shot footage có p.clip (mã clip) + p.setting (luật K Q32) và hero footage/clip có opt.sha256;
  (3) mỗi mã clip có tệp giấy phép đã lưu: <licenses>/<mã viết thường>.txt, trong tệp có đúng SHA-256 của clip;
  (4) mỗi shot footage ≤ 8 s (QUAN-TRI-RUI-RO §6, như T1).
Mã thoát 1 nếu trượt một mục."""
import json, os, sys
import yaml

MAX_SHARE, MAX_CLIP = 0.20, 8.0


def arg(k, d=None):
    return sys.argv[sys.argv.index('--' + k) + 1] if '--' + k in sys.argv else d


def main():
    spec = sys.argv[1]; E = yaml.safe_load(open(spec)); lic = arg('licenses') or os.path.join(os.path.dirname(os.path.abspath(spec)), 'licenses')
    tot = 0.0; ft = 0.0; clips = []; bad = []
    for sg in E['segments']:
        dur = float(sg['dur']); tot += dur; ats = [float(s.get('at', 0)) for s in sg['shots']]
        for i, sh in enumerate(sg['shots']):
            if sh.get('type') != 'footage': continue
            d = (ats[i + 1] if i + 1 < len(ats) else dur) - ats[i]; ft += d; p = sh.get('p') or {}; h = (E.get('heroes') or {}).get(p.get('hero')) or {}; o = h.get('opt') or {}
            cid = p.get('clip'); sha = o.get('sha256'); lf = os.path.join(lic, f'{cid}.txt'.lower()) if cid else None
            c = dict(doan=sg['id'], shot=i, clip=cid, setting=p.get('setting'), giay=round(d, 2), sha256=sha, giay_phep=os.path.relpath(lf) if lf else None)
            if not cid or not p.get('setting'): bad.append(f'{sg["id"]}/{i}: thiếu p.clip hoặc p.setting')
            if not sha: bad.append(f'{sg["id"]}/{i}: hero footage thiếu opt.sha256')
            if not lf or not os.path.exists(lf): bad.append(f'{sg["id"]}/{i}: không có tệp giấy phép {lf}')
            elif sha and sha not in open(lf).read(): bad.append(f'{sg["id"]}/{i}: tệp giấy phép không ghi SHA {sha[:12]}…')
            if d > MAX_CLIP: bad.append(f'{sg["id"]}/{i}: clip {d:.2f} s > {MAX_CLIP} s')
            clips.append(c)
    share = ft / tot if tot else 0
    if share > MAX_SHARE: bad.append(f'footage {100 * share:.1f} % > {100 * MAX_SHARE:.0f} %')
    R = dict(tong_s=round(tot, 2), footage_s=round(ft, 2), ty_le_pct=round(100 * share, 1), nguong_pct=100 * MAX_SHARE, clip=clips, loi=bad, ket_qua='ĐẠT' if not bad else 'TRƯỢT')
    if arg('json'): json.dump(R, open(arg('json'), 'w'), indent=1, ensure_ascii=False)
    print(json.dumps(R, ensure_ascii=False, indent=1)); sys.exit(0 if not bad else 1)


if __name__ == '__main__':
    main()
