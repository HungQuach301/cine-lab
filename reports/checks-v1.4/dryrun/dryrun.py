"""Phiên K — chạy thử C3 v1.4 trên 8 file Cổng 3 A2+ của P (mặt nạ 4× thật, model sheet B1 có c3_views).
Hai lần đo cho mỗi file, đều bằng checks/ v1.4:
  (1) 'khong_views': parts.json của P nguyên trạng (không có 'views') — so mọi mẫu với góc 0° như v1.3;
  (2) 'co_views': cùng mặt nạ, thêm 'views' do K tính từ chính trang render của P (k_views.js).
Không sửa design/: bản (2) dựng trong thư mục tạm, mặt nạ là liên kết mềm tới file của P.
Kiểm toán ngẫu nhiên không chạy lại ở đây (audit=False): bộ mặt nạ không đổi nên kết quả kiểm toán mặt nạ của v1.3
(8/8 khớp) giữ nguyên; phần kiểm toán 'views' mới cần P xuất views.json khi render lại.
Dùng: /opt/cine/bin/python reports/checks-v1.4/dryrun/dryrun.py
"""
import json
import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "checks"))
from cinecheck.rule_c3 import check_c3  # noqa: E402

A2P = REPO / "design/cong3/v2/out/a2p"
FILES = ["a_close_ida", "b_cas_bird", "c_s5_medium", "c_s5_wide", "d_s6_alley", "e_ending", "walk", "walk_cas"]


def slim(v):
    return {k: dict(view_deg=e["view_deg"], elev_deg=e["elev_deg"],
                    parts={p: {x: q[x] for x in ("foreshorten", "hidden", "depth")} for p, q in e["parts"].items()})
            for k, e in v.items()}


def summary(r):
    ev = r["evidence"]
    bad = [m["name"] for m in r["metrics"] if not m["ok"]]
    return dict(status=r["status"], chi_so_truot=bad, theo_shot=ev.get("theo_shot"),
                do=[{k: x.get(k) for k in ("khung", "bo_phan", "goc_tham_chieu", "ty_le", "sheet", "lech_pct", "U_pct",
                                           "ket_qua")} for x in ev.get("do", [])],
                khong_do_duoc=ev.get("khong_do_duoc"), ghi_chu=r["notes"])


def main():
    out = {}
    tmp = Path(tempfile.mkdtemp(prefix="k-c3-dry-"))
    for n in FILES:
        video, pd = A2P / f"{n}.mp4", A2P / f"{n}.parts"
        r0 = check_c3(video, "shot", pd, REPO)
        spec = json.loads((pd / "parts.json").read_text())
        views = slim(json.loads((HERE / f"{n}.views.json").read_text()))
        spec["views"] = {k: views[k] for k in spec["frames"]}
        d = tmp / f"{n}.parts"
        d.mkdir()
        for sub in pd.iterdir():
            if sub.is_dir():
                os.symlink(sub, d / sub.name)
        (d / "parts.json").write_text(json.dumps(spec))
        r1 = check_c3(video, "shot", d, REPO)
        out[n] = dict(khong_views=summary(r0), co_views=summary(r1), views=spec["views"])
        print(n, r0["status"], "→", r1["status"], flush=True)
    (HERE / "dryrun.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
