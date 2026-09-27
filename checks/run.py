"""Cine Lab — chạy toàn bộ luật L1 trên một file đã render. Cách dùng: xem checks/RUN.md."""
import argparse
import json
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from cinecheck import VERSION  # noqa: E402
from cinecheck.common import FAIL, MISSING, NA, PASS, missing, not_applicable, result  # noqa: E402
from cinecheck.lockhash import read_lock, tree_hash  # noqa: E402
from cinecheck.registry import CHAN, ORDER, RULES  # noqa: E402
from cinecheck.report import write_reports  # noqa: E402

ERROR = "ERROR"
EXIT = {"ĐẠT": 0, "TRƯỢT": 1, "THIẾU DỮ LIỆU": 2, "LUẬT KHÔNG KHỚP LOCK": 3}


def sidecar(video, suffix):
    p = video.with_name(video.stem + suffix)
    return p if p.exists() else None


def run_rule(code, fn, *args):
    t = time.time()
    try:
        r = fn(*args)
    except Exception as e:  # lỗi chạy luật = không chứng minh được là sạch
        r = result(code, ERROR, notes=[f"Lỗi khi đo: {type(e).__name__}: {e}"],
                   evidence={"traceback": traceback.format_exc()[-3000:]})
    r["seconds"] = round(time.time() - t, 2)
    return r


def main(argv=None):
    ap = argparse.ArgumentParser(description="Cine Lab L1 checks")
    ap.add_argument("video")
    ap.add_argument("--profile", choices=["shot", "youtube", "archive"], default="shot")
    ap.add_argument("--script", help="kịch bản thoại (mặc định <video>.script.txt)")
    ap.add_argument("--text", help="thư mục matte chữ (mặc định <video>.text/)")
    ap.add_argument("--motion", help="dữ liệu chuyển động bake (mặc định <video>.motion.json)")
    ap.add_argument("--assets", help="danh sách tài sản dùng (mặc định <video>.assets.json)")
    ap.add_argument("--stems", help="thư mục stem thoại + nền (mặc định <video>.stems/)")
    ap.add_argument("--parts", help="thư mục mặt nạ bộ phận nhân vật (mặc định <video>.parts/)")
    ap.add_argument("--library", help="thư viện tài sản (mặc định <repo>/assets/LIBRARY.json)")
    ap.add_argument("--repo", default=str(HERE.parent), help="gốc repo (mặc định cha của checks/)")
    ap.add_argument("--out", help="thư mục báo cáo (mặc định <repo>/reports/checks/<tên file>/)")
    ap.add_argument("--only", help="chỉ chạy các mã này, cách nhau dấu phẩy (chỉ để gỡ lỗi)")
    a = ap.parse_args(argv)

    video = Path(a.video).resolve()
    if not video.is_file():
        print(f"Không thấy file: {video}", file=sys.stderr)
        return 4
    repo = Path(a.repo).resolve()
    script = Path(a.script) if a.script else sidecar(video, ".script.txt")
    text = Path(a.text) if a.text else sidecar(video, ".text")
    motion = Path(a.motion) if a.motion else sidecar(video, ".motion.json")
    assets = Path(a.assets) if a.assets else sidecar(video, ".assets.json")
    stems = Path(a.stems) if a.stems else sidecar(video, ".stems")
    parts = Path(a.parts) if a.parts else sidecar(video, ".parts")
    library = Path(a.library) if a.library else repo / "assets" / "LIBRARY.json"
    only = set(a.only.split(",")) if a.only else None
    prof = a.profile

    from cinecheck.rule_c3 import check_c3
    from cinecheck.rule_g3 import check_g3
    from cinecheck.rule_g3b import check_g3b
    from cinecheck.rule_h1b import check_h1b
    from cinecheck.rule_j1b import check_j1b
    from cinecheck.rule_p0 import check_p0
    from cinecheck.rule_h1 import check_h1
    from cinecheck.rule_j1 import check_j1
    from cinecheck.rule_o3 import check_o3
    from cinecheck.rules_audio import check_m1, check_m3
    from cinecheck.rules_file import check_n1, check_n2, check_n3
    from cinecheck.rules_text import check_g4, check_p1

    def need(code, path, what, fn, *extra, probe_file=None):
        if path is None or not Path(probe_file or path).exists():
            return missing(code, what)
        return run_rule(code, fn, video, prof, path, *extra)

    plan = {
        "N1": lambda: run_rule("N1", check_n1, video, prof),
        "N2": lambda: run_rule("N2", check_n2, video, prof),
        "N3": lambda: run_rule("N3", check_n3, video, prof),
        "P0": lambda: run_rule("P0", check_p0, video, prof, text, script if script and Path(script).exists() else None),
        "P1": lambda: need("P1", text, f"{video.stem}.text/elements.json", check_p1,
                           probe_file=text and text / "elements.json"),
        "G4": lambda: need("G4", text, f"{video.stem}.text/elements.json", check_g4,
                           probe_file=text and text / "elements.json"),
        "G3": lambda: run_rule("G3", check_g3, video, prof),
        "G3b": lambda: run_rule("G3b", check_g3b, video, prof),
        "M1": lambda: run_rule("M1", check_m1, video, prof),
        "M3": lambda: run_rule("M3", check_m3, video, prof),
        "J1": lambda: need("J1", script, f"{video.stem}.script.txt", check_j1, stems),
        "J1b": lambda: need("J1b", stems, f"{video.stem}.stems/ (dialogue.* + stem nền)", check_j1b),
        "H1": lambda: need("H1", motion, f"{video.stem}.motion.json", check_h1),
        "H1b": lambda: need("H1b", motion, f"{video.stem}.motion.json", check_h1b),
        "C3": lambda: need("C3", parts, f"{video.stem}.parts/parts.json", check_c3, repo, True, assets,
                           probe_file=parts and parts / "parts.json"),
        "O3": lambda: (missing("O3", f"thư viện {library}") if not library.exists() else
                       need("O3", assets, f"{video.stem}.assets.json", check_o3, library, repo)),
    }
    if text is not None:
        text = text if text.is_dir() else None
    results = []
    for code in ORDER:
        if only and code not in only:
            continue
        if prof not in RULES[code]["profiles"]:
            r = not_applicable(code, f"Không áp cho profile '{prof}'.")
        else:
            r = plan[code]()
        results.append(r)
        print(f"[{r['status']:>7}] {code} {r['title']}", file=sys.stderr)

    lock_want, lock_got = read_lock(HERE), tree_hash(HERE)
    blocking = [r for r in results if r["level"] == CHAN]
    if lock_want != lock_got:
        verdict = "LUẬT KHÔNG KHỚP LOCK"
    elif any(r["status"] in (FAIL, ERROR) for r in blocking):
        verdict = "TRƯỢT"
    elif any(r["status"] == MISSING for r in blocking):
        verdict = "THIẾU DỮ LIỆU"
    else:
        verdict = "ĐẠT"
    near = [dict(code=r["code"], metric=m["name"], value=m["value"], threshold=m["threshold"])
            for r in results for m in r["metrics"] if m.get("near")]
    report = dict(
        tool=f"cinecheck {VERSION}", created_utc=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        file=str(video), profile=prof, verdict=verdict,
        lock=dict(expected=lock_want, actual=lock_got, match=lock_want == lock_got),
        inputs=dict(script=str(script) if script else None, text=str(text) if text else None,
                    stems=str(stems) if stems else None, parts=str(parts) if parts else None,
                    motion=str(motion) if motion else None, assets=str(assets) if assets else None,
                    library=str(library)),
        counts={s: sum(r["status"] == s for r in results) for s in (PASS, FAIL, MISSING, NA, ERROR)},
        near_threshold=near, results=results)
    out = Path(a.out) if a.out else repo / "reports" / "checks" / video.stem
    jp, mp = write_reports(report, out, video.stem)
    print(f"VERDICT: {verdict}\nJSON: {jp}\nMD:   {mp}")
    return EXIT[verdict]


if __name__ == "__main__":
    sys.exit(main())
