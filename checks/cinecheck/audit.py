"""Kiểm toán ngẫu nhiên mặt nạ C3 (v1.3, quyết định Q-C3c = B của chủ dự án).

Quy trình:
1. Phiên P (không phải phiên xưởng) chạy `checks/audit.py issue <video>` SAU khi xưởng nộp video + <video>.parts/.
   Máy lấy hạt giống ngẫu nhiên từ hệ điều hành (secrets), chọn 1–2 khung trong các khung mẫu của parts.json,
   ghi <video>.audit/request.json: hạt giống, khung, thời điểm, SHA-256 của video và của bộ mặt nạ đã nộp.
2. Phiên xưởng render lại mặt nạ bộ phận đúng các khung đó từ file cảnh đã khoá, cùng cách render mặt nạ đã
   nộp, ghi vào <video>.audit/rerender/<khung 5 chữ số>/<bộ phận>.png, kèm <video>.audit/render.log.
3. C3 (run.py) đối chiếu. TRƯỢT khi: thiếu yêu cầu kiểm toán (THIẾU), bộ mặt nạ hoặc video đổi sau khi phát
   yêu cầu, thiếu log hoặc log thiếu mục bắt buộc, SHA file cảnh trong log khác file trên đĩa, thiếu mặt nạ
   render lại, hoặc mặt nạ nộp lệch mặt nạ render lại vượt dải nhiễu (tỷ lệ) hay vượt ngưỡng khớp điểm ảnh.
4. v1.4: parts.json có 'views' (góc nhìn, gập, che, độ sâu) thì xưởng xuất lại views của các khung được chọn vào
   <video>.audit/rerender/<khung 5 chữ số>/views.json (cùng lược đồ một mục của 'views'); lệch bản nộp → TRƯỢT.

Log bắt buộc (mỗi mục một dòng, thêm dòng tự do được):
  SCENE <đường dẫn file cảnh tính từ gốc repo> SHA256 <64 hex>
  FRAME <khung> CMD <lệnh render đã chạy>          (một dòng cho mỗi khung được chọn)
"""
import hashlib
import json
import re
import secrets
from datetime import datetime, timezone
from pathlib import Path

import cv2
import numpy as np

N_FRAMES = (1, 2)          # số khung được chọn (ngẫu nhiên 1 hoặc 2)
XOR_MAX = 0.02             # điểm ảnh khác nhau / điểm ảnh biên của mặt nạ render lại (nội bộ)
VIEWS_TOL = dict(goc=1.0, ty_le=0.005)  # v1.4: views render lại lệch bản nộp (nội bộ; render tất định ≈ 0)


def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def parts_digest(parts_dir):
    """SHA-256 của parts.json và mọi mặt nạ nó trỏ tới (sắp theo đường dẫn)."""
    parts_dir = Path(parts_dir)
    spec = json.loads((parts_dir / "parts.json").read_text(encoding="utf-8"))
    files = {"parts.json"}
    for fr in spec.get("frames", {}).values():
        files.update(fr.values())
    lines = [f"{sha256_file(parts_dir / f)}  {f}" for f in sorted(files)]
    return hashlib.sha256("".join(l + "\n" for l in lines).encode()).hexdigest()


def audit_dir(video):
    video = Path(video)
    return video.with_name(video.stem + ".audit")


def issue(video, parts_dir, issued_by="P", seed=None):
    """Chọn khung ngẫu nhiên và ghi request.json. Không ghi đè yêu cầu đã có."""
    parts_dir = Path(parts_dir)
    spec = json.loads((parts_dir / "parts.json").read_text(encoding="utf-8"))
    if spec.get("no_character") is True:
        raise ValueError("parts.json khai báo no_character: không có mặt nạ để kiểm toán.")
    cands = sorted(int(k) for k, v in spec.get("frames", {}).items() if "head" in v)
    if not cands:
        raise ValueError("parts.json không có khung nào có mặt nạ đầu.")
    seed = secrets.randbits(64) if seed is None else int(seed)
    rng = np.random.default_rng(seed)
    k = min(len(cands), int(rng.integers(N_FRAMES[0], N_FRAMES[1] + 1)))
    frames = sorted(int(x) for x in rng.choice(cands, size=k, replace=False))
    ad = audit_dir(video)
    req = ad / "request.json"
    if req.exists():
        raise FileExistsError(f"{req} đã có. Không phát lại yêu cầu kiểm toán (xoá phải có lý do, ghi vào git).")
    ad.mkdir(parents=True, exist_ok=True)
    body = dict(version=1, seed=str(seed), frames=frames, candidates=len(cands), issued_by=issued_by,
                issued_utc=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                video=Path(video).name, video_sha256=sha256_file(video), parts_sha256=parts_digest(parts_dir))
    req.write_text(json.dumps(body, indent=1, ensure_ascii=False), encoding="utf-8")
    return body


def parse_log(p):
    scenes, cmds = [], {}
    for line in Path(p).read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(r"\s*SCENE\s+(\S+)\s+SHA256\s+([0-9a-fA-F]{64})\s*$", line)
        if m:
            scenes.append((m.group(1), m.group(2).lower()))
            continue
        m = re.match(r"\s*FRAME\s+(\d+)\s+CMD\s+(\S.*)$", line)
        if m:
            cmds.setdefault(int(m.group(1)), []).append(m.group(2).strip())
    return scenes, cmds


def _boundary(m):
    return int((m ^ cv2.erode(m.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)).sum())


def verify(video, parts_dir, repo, spec, load_mask, length_px, uncertainty, assets=None):
    """Đối chiếu kiểm toán. Trả (metrics_rows, notes, evidence, có_yêu_cầu)."""
    from .common import metric
    ad = audit_dir(video)
    req_p = ad / "request.json"
    if not req_p.is_file():
        return [], [f"Chưa có yêu cầu kiểm toán ngẫu nhiên ({req_p.name}): phiên P chạy "
                    f"`checks/audit.py issue {Path(video).name}`."], {}, False
    req = json.loads(req_p.read_text(encoding="utf-8"))
    frames = [int(f) for f in req.get("frames", [])]
    ms, notes, ev = [], [f"Kiểm toán ngẫu nhiên: hạt giống {req.get('seed')}, khung {frames}, phát bởi "
                         f"{req.get('issued_by')} lúc {req.get('issued_utc')}."], dict(yeu_cau=req)
    ms.append(metric("kiểm toán: video không đổi sau khi phát yêu cầu", sha256_file(video) == req.get("video_sha256"),
                     "==", True))
    ms.append(metric("kiểm toán: bộ mặt nạ nộp không đổi sau khi phát yêu cầu",
                     parts_digest(parts_dir) == req.get("parts_sha256"), "==", True))
    ms.append(metric("kiểm toán: có khung được chọn", len(frames), ">=", 1, near_check=False))
    # log
    log = ad / "render.log"
    scenes, cmds = parse_log(log) if log.is_file() else ([], {})
    ms.append(metric("kiểm toán: có render.log", log.is_file() and log.stat().st_size > 0, "==", True))
    scene_ok, scene_rows = bool(scenes), []
    declared = None
    if assets is not None and Path(assets).is_file():
        declared = set(json.loads(Path(assets).read_text(encoding="utf-8")).get("scene_files", []))
    for path, h in scenes:
        f = Path(repo) / path
        on_disk = sha256_file(f) if f.is_file() else None
        ok = on_disk == h and (declared is None or path in declared)
        scene_rows.append(dict(file=path, sha_log=h, sha_dia=on_disk, trong_scene_files=None if declared is None
                               else path in declared, khop=ok))
        scene_ok &= ok
    ms.append(metric("kiểm toán: log có dòng SCENE, SHA-256 khớp file cảnh trên đĩa", scene_ok, "==", True))
    ms.append(metric("kiểm toán: khung được chọn không có dòng FRAME … CMD trong log",
                     sum(1 for f in frames if f not in cmds), "<=", 0))
    ev.update(log_scene=scene_rows, log_lenh={str(k): v for k, v in cmds.items()})
    # đối chiếu mặt nạ
    missing, worst_ratio, worst_xor, rows = 0, 0.0, 0.0, []
    for f in frames:
        sub = spec["frames"].get(str(f), {})
        for part, rel in sub.items():
            rp = ad / "rerender" / f"{f:05d}" / f"{part}.png"
            if not rp.is_file():
                missing += 1
                rows.append(dict(khung=f, bo_phan=part, ket_qua="thiếu mặt nạ render lại"))
                continue
            ms_, mr = load_mask(parts_dir / rel), load_mask(rp)
            if ms_.shape != mr.shape:
                missing += 1
                rows.append(dict(khung=f, bo_phan=part, ket_qua=f"khác kích thước {ms_.shape} vs {mr.shape}"))
                continue
            b = max(_boundary(mr), 1)
            xr = float((ms_ ^ mr).sum()) / b
            worst_xor = max(worst_xor, xr)
            rows.append(dict(khung=f, bo_phan=part, khac_diem_anh_tren_bien=round(xr, 4)))
        if "head" in sub and all((ad / "rerender" / f"{f:05d}" / f"{p}.png").is_file() for p in sub):
            hs, hr = length_px(load_mask(parts_dir / sub["head"])), length_px(load_mask(ad / "rerender" / f"{f:05d}" / "head.png"))
            for part, rel in sub.items():
                if part == "head" or hs is None or hr is None:
                    continue
                ls_ = length_px(load_mask(parts_dir / rel))
                lr = length_px(load_mask(ad / "rerender" / f"{f:05d}" / f"{part}.png"))
                if ls_ is None or lr is None:
                    continue
                d = abs((ls_ / hs) / (lr / hr) - 1)
                u = uncertainty(lr, hr)
                worst_ratio = max(worst_ratio, d / u)
                rows.append(dict(khung=f, bo_phan=part, lech_ty_le_pct=round(100 * d, 3), U_pct=round(100 * u, 3)))
    # v1.4: parts.json có 'views' thì render lại phải xuất lại số liệu góc nhìn/tư thế của khung đó và khớp bản nộp
    if isinstance(spec.get("views"), dict):
        v_bad, v_worst = 0, dict(goc=0.0, ty_le=0.0)
        for f in frames:
            vp = ad / "rerender" / f"{f:05d}" / "views.json"
            sub = spec["views"].get(str(f))
            try:
                got = json.loads(vp.read_text(encoding="utf-8")) if vp.is_file() else None
                pairs = [("goc", sub["view_deg"], got["view_deg"], True), ("goc", sub["elev_deg"], got["elev_deg"], False)]
                for part, q in sub["parts"].items():
                    g = got["parts"][part]
                    pairs += [("ty_le", q["foreshorten"], g["foreshorten"], False), ("ty_le", q["hidden"], g["hidden"], False),
                              ("ty_le", q["depth"], g["depth"], False)]
                loc = dict(goc=0.0, ty_le=0.0)
                for key, x, y, circ in pairs:
                    dd = abs(float(x) - float(y))
                    if circ:
                        dd = abs((dd + 180.0) % 360.0 - 180.0)
                    loc[key] = max(loc[key], dd)
                for key in loc:
                    v_worst[key] = max(v_worst[key], loc[key])
                rows.append(dict(khung=f, views_render_lai="khớp" if all(
                    loc[k_] <= VIEWS_TOL[k_] for k_ in VIEWS_TOL) else "lệch", views_lech=loc))
            except (TypeError, KeyError, ValueError, AttributeError):
                v_bad += 1
                rows.append(dict(khung=f, views_render_lai="thiếu hoặc sai định dạng views.json"))
        ms.append(metric("kiểm toán: views.json render lại thiếu hoặc sai định dạng", v_bad, "<=", 0))
        ms.append(metric("kiểm toán: views render lại lệch bản nộp — góc nhìn, góc ngẩng (lớn nhất)",
                         round(v_worst["goc"], 3), "<=", VIEWS_TOL["goc"], "°"))
        ms.append(metric("kiểm toán: views render lại lệch bản nộp — foreshorten, hidden, depth (lớn nhất)",
                         round(v_worst["ty_le"], 4), "<=", VIEWS_TOL["ty_le"]))
    ms.append(metric("kiểm toán: mặt nạ render lại thiếu hoặc khác kích thước", missing, "<=", 0))
    ms.append(metric("kiểm toán: lệch tỷ lệ nộp/render lại, tính theo dải nhiễu U (lớn nhất)", worst_ratio, "<=", 1.0,
                     "×U"))
    ms.append(metric("kiểm toán: điểm ảnh khác nhau / điểm ảnh biên (lớn nhất)", worst_xor, "<=", XOR_MAX))
    ev["doi_chieu"] = rows[:200]
    return ms, notes, ev, True
