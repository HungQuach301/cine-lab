"""Phiên K — chạy thử checks v1.5 so với v1.4 (P0 và C3, theo shot), không sửa design/.

P0:
  - layout-v15.mp4 (SHA 8a5ebf01…): v1.4; v1.5 với <video>.parts/ của P (mặt nạ C3 Ida, không có 'silhouettes');
    v1.5 thêm 'silhouettes' do K render (k_sil.js, mọi nhân vật, đúng 233 khung mẫu P0) trong thư mục tạm.
  - hai bản layout.mp4 có khiếu nại (lấy từ git: 8a707d7 = Cổng 5 v1, "56" khung 2775; 44a469a = Cổng 5 v2 bản cuối
    SHA 78e662d1…, "MA" khung 1980): v1.4; v1.5 với 'silhouettes' do K render cho đúng khung khiếu nại.
C3 (layout-v15, mặt nạ C3 Ida của P, kiểm toán như run.py):
  - v1.4 (checks/ ở cce7fb2) và v1.5 (checks/ nhánh này) với ida.json nguyên trạng (không khai c3_head_axis = 'pca').
  - Giả định (không kiểm toán, vì đổi parts.json làm đổi SHA bộ mặt nạ): ida.json khai 'doc' với c3_views đo lại
    theo 'doc' từ turnaround Ida 'bl' (k_ida_doc.json; cùng công cụ c3_bl.py của P, độ dài theo cinecheck v1.5).
Dùng: /opt/cine/bin/python reports/checks-v1.5/dryrun/dryrun.py   (ghi dryrun.json cạnh file này)
"""
import json
import os
import subprocess
import sys
import tempfile
from collections import OrderedDict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
OUT = REPO / "design/cong5/layout/out"
V15 = OUT / "layout-v15.mp4"
OLD = {"v1_8a707d7": ("8a707d7", "sil/v1_8a707d7"), "v2_44a469a": ("44a469a", "sil/v2_44a469a")}


def shot_of(frames_stat):
    """khung → id shot thiết kế, từ bảng (khung, shot) của công cụ xuất (mỗi 12 khung) và k_sil (khung P0)."""
    m = {}
    for r in frames_stat:
        m[int(r["f"])] = r["shot"]
    keys = sorted(m)

    def f(k):
        lo = max([x for x in keys if x <= k], default=keys[0])
        return m[lo]
    return f


def worker(mode, checks_dir, tmp):
    """Chạy trong tiến trình riêng (hai phiên bản cinecheck không chung một tiến trình)."""
    sys.path.insert(0, str(checks_dir))
    from cinecheck.rule_c3 import check_c3
    from cinecheck.rule_p0 import check_p0
    tmp = Path(tmp)
    res = {}
    if mode.startswith("p0"):
        vids = {"layout-v15": V15, **{k: tmp / f"{k}.mp4" for k in OLD}}
        for name, v in vids.items():
            text, script = v.with_name("layout-v15.text" if name == "layout-v15" else f"{name}.text"), None
            if name == "layout-v15":
                script = OUT / "layout-v15.script.txt"
            parts = None
            if mode == "p0_v15_parts" and name == "layout-v15":
                parts = OUT / "layout-v15.parts"
            if mode == "p0_v15_sil":
                parts = tmp / f"{name}.parts"
            args = (v, "shot", text if text.is_dir() else None, script if script and script.exists() else None)
            r = check_p0(*args, parts) if mode != "p0_v14" else check_p0(*args)
            ev = r["evidence"]
            res[name] = dict(status=r["status"], metrics=[(m["name"], m["value"]) for m in r["metrics"]],
                             khong_matte=ev.get("chu_khong_matte", []), mien=ev.get("vung_nhan_vat_mien", []),
                             ngan_khong_mat_na=ev.get("chu_ngan_khong_mat_na", []),
                             khung_co_mat_na=ev.get("khung_co_mat_na_nhan_vat"), khung_lay_mau=ev.get("khung_lay_mau"),
                             notes=r["notes"])
    else:
        parts = OUT / "layout-v15.parts" if mode != "c3_v15_doc" else tmp / "layout-v15.doc.parts"
        audit = mode != "c3_v15_doc"
        r = check_c3(V15, "shot", parts, REPO, audit, OUT / "layout-v15.assets.json")
        ev = r["evidence"]
        res = dict(status=r["status"], metrics=[(m["name"], m["value"], m["ok"]) for m in r["metrics"]],
                   do=ev.get("do", []), khong_do_duoc=len(ev.get("khong_do_duoc", [])),
                   dau_rong_hon_cao=len(ev.get("dau_rong_hon_cao", []) or []), notes=r["notes"])
    json.dump(res, sys.stdout, ensure_ascii=False, default=str)


def prepare(tmp):
    tmp = Path(tmp)
    for name, (commit, sil) in OLD.items():
        v = tmp / f"{name}.mp4"
        with open(v, "wb") as fh:
            subprocess.run(["git", "-C", str(REPO), "show", f"{commit}:design/cong5/layout/out/layout.mp4"], stdout=fh,
                           check=True)
        # thư mục chữ của đúng bản đó (matte phụ đề) để P0 chạy như lúc P kiểm
        td = tmp / f"{name}.text"
        td.mkdir()
        ls = subprocess.run(["git", "-C", str(REPO), "ls-tree", "--name-only", f"{commit}:design/cong5/layout/out/layout.text"],
                            capture_output=True, text=True, check=True).stdout.split()
        for f in ls:
            with open(td / f, "wb") as fh:
                subprocess.run(["git", "-C", str(REPO), "show", f"{commit}:design/cong5/layout/out/layout.text/{f}"],
                               stdout=fh, check=True)
        pd = tmp / f"{name}.parts"
        pd.mkdir()
        sj = json.loads((HERE / sil / "sil.json").read_text())
        for k, rel in sj.items():
            os.symlink(HERE / sil / rel, pd / Path(rel).name)
        (pd / "parts.json").write_text(json.dumps({"silhouettes": {k: Path(rel).name for k, rel in sj.items()}}))
    # layout-v15: parts.json của P + 'silhouettes' của K (thư mục tạm, mặt nạ C3 là liên kết mềm)
    for tag in ("", ".doc"):
        pd = tmp / f"layout-v15{tag}.parts"
        pd.mkdir()
        for sub in (OUT / "layout-v15.parts").iterdir():
            if sub.is_dir():
                os.symlink(sub, pd / sub.name)
        spec = json.loads((OUT / "layout-v15.parts/parts.json").read_text())
        if tag == "":
            sj = json.loads((HERE / "sil/layout-v15/sil.json").read_text())
            (pd / "sil").mkdir()
            for k, rel in sj.items():
                os.symlink(HERE / "sil/layout-v15" / rel, pd / "sil" / Path(rel).name)
            spec["silhouettes"] = {k: f"sil/{Path(rel).name}" for k, rel in sj.items()}
        else:
            sheet = json.loads((REPO / spec["model_sheet"]).read_text())
            sheet["c3_head_axis"] = "doc"
            doc = json.loads((HERE / "k_ida_doc.json").read_text())
            sheet["c3_views"] = {k: {p: x for p, x in row.items() if not p.startswith("_")} for k, row in doc.items()}
            for part, x in sheet["c3_views"]["0°"].items():  # độ dài cấp gốc phải khớp góc 0° (RUN.md 3.6.1)
                for blk in (sheet, sheet.get("parts") or {}):
                    if isinstance(blk.get(part), dict) and "length" in blk[part] and x is not None:
                        blk[part]["length"] = x
            (pd / "ida.doc.json").write_text(json.dumps(sheet, ensure_ascii=False))
            spec["model_sheet"] = "ida.doc.json"
        (pd / "parts.json").write_text(json.dumps(spec))


def per_shot_c3(rows, shot):
    agg = OrderedDict()
    for r in rows:
        s = shot(r["khung"])
        a = agg.setdefault(s, dict(dat=0, truot=0, kcm=0, thieu=0, max_lech=0.0))
        k = r.get("ket_qua", "")
        if k == "đạt":
            a["dat"] += 1
        elif k == "trượt chắc chắn":
            a["truot"] += 1
        elif k == "không chứng minh được":
            a["kcm"] += 1
        else:
            a["thieu"] += 1
        if "lech_pct" in r:
            a["max_lech"] = max(a["max_lech"], abs(r["lech_pct"]))
    return agg


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--worker":
        return worker(sys.argv[2], sys.argv[3], sys.argv[4])
    tmp = Path(tempfile.mkdtemp(prefix="k-v15-dry-"))
    v14 = tmp / "checks_v14"
    v14.mkdir()
    tar = subprocess.run(["git", "-C", str(REPO), "archive", "cce7fb2", "checks"], capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", str(v14)], input=tar, check=True)
    prepare(tmp)
    runs = {"p0_v14": v14 / "checks", "p0_v15_parts": REPO / "checks", "p0_v15_sil": REPO / "checks",
            "c3_v14": v14 / "checks", "c3_v15": REPO / "checks", "c3_v15_doc": REPO / "checks"}
    out = {}
    for mode, cdir in runs.items():
        p = subprocess.run([sys.executable, __file__, "--worker", mode, str(cdir), str(tmp)], capture_output=True, text=True)
        if p.returncode:
            print(p.stderr[-3000:], file=sys.stderr)
            raise SystemExit(f"{mode} lỗi")
        out[mode] = json.loads(p.stdout)
        print(mode, "xong", flush=True)
    stat = json.loads((OUT / "c3_export_stat.json").read_text())
    stat += json.loads((HERE / "sil/layout-v15/stat.json").read_text())
    shot = shot_of(stat)
    out["c3_theo_shot"] = {m: per_shot_c3(out[m]["do"], shot) for m in ("c3_v14", "c3_v15", "c3_v15_doc")}
    for m in ("p0_v14", "p0_v15_parts", "p0_v15_sil"):
        for name, r in out[m].items():
            f = shot if name == "layout-v15" else (lambda k, n=name: {"v1_8a707d7": "s42a", "v2_44a469a": "s33"}[n]
                                                   if k in (2775, 1980) else "?")
            r["theo_shot"] = {}
            for x in r["khong_matte"]:
                r["theo_shot"].setdefault(f(x["khung"]), [0, 0])[0] += 1
            for x in r["mien"]:
                r["theo_shot"].setdefault(f(x["khung"]), [0, 0])[1] += 1
    (HERE / "dryrun.json").write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str))


if __name__ == "__main__":
    main()
