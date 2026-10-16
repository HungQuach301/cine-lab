"""V5b-1 · căn góc then/now TỪ ĐIỂM KHỐNG CHẾ (port tổng quát của lab/timelapse/calib_photo.py).
Vào JSON: {"image": {"w", "h"}, "points": [{"name", "uv": [u, v], "enu": [E, N, U]}, …] (≥ 6 điểm), "eye_h": null | số (cố định cao mắt), "init": {"E","N","yaw_deg"}}.
Ẩn: vị trí máy (E, N, U — hoặc U cố định), yaw, pitch, roll, tiêu cự f (px). Bình phương tối thiểu (scipy least_squares), nhiều điểm khởi đầu.
Ra: pose {cam_enu, look_enu, up_enu, fov_v_deg} + sai số chiếu lại từng điểm + RMS (px, % rộng ảnh).
Bài học R&D (§6.6): RMS thấp KHÔNG chứng minh đúng góc → luôn xuất ảnh chồng 50 % (render.js --override với pose) cho người kiểm."""
import argparse, json, sys
import numpy as np
from scipy.optimize import least_squares

def rot(yaw, pitch, roll):   # thế giới E, N, U; máy: x phải, y lên, nhìn theo fwd
    fwd = np.array([np.sin(yaw) * np.cos(pitch), np.cos(yaw) * np.cos(pitch), np.sin(pitch)])
    right = np.array([np.cos(yaw), -np.sin(yaw), 0.0]); up = np.cross(right, fwd); c, s = np.cos(roll), np.sin(roll)
    return fwd, c * right + s * up, -s * right + c * up

def project(P, cam, yaw, pitch, roll, f, w, h):
    fwd, right, up = rot(yaw, pitch, roll); d = np.asarray(P, float) - cam; z = d @ fwd
    return np.stack([w / 2 + f * (d @ right) / z, h / 2 - f * (d @ up) / z], -1), z

def solve(spec):
    pts = spec["points"]
    if len(pts) < 6: raise SystemExit(f"cần ≥ 6 điểm khống chế (có {len(pts)})")
    w, h = spec["image"]["w"], spec["image"]["h"]; UV = np.array([p["uv"] for p in pts], float); P = np.array([p["enu"] for p in pts], float)
    eye = spec.get("eye_h"); ini = spec.get("init", {})
    def unpack(v):
        cam = np.array([v[0], v[1], eye if eye is not None else v[6]]); return cam, v[2], v[3], v[4], v[5]
    def res(v):
        cam, yaw, pitch, roll, f = unpack(v); uv, z = project(P, cam, yaw, pitch, roll, f, w, h)
        return np.concatenate([(uv - UV).ravel(), np.where(z < 1, 1e3, 0)])
    best = None; c0 = P.mean(0)
    for dE in (-150, 0, 150):
        for dN in (-150, 0, 150):
            for dy in (-60, 0, 60):
                E0, N0 = ini.get("E", c0[0] + dE), ini.get("N", c0[1] + dN)
                yaw0 = np.radians(ini.get("yaw_deg", np.degrees(np.arctan2(c0[0] - E0, c0[1] - N0)))) + np.radians(dy)
                v0 = [E0, N0, yaw0, 0.0, 0.0, max(w, h)] + ([] if eye is not None else [c0[2] + 20])
                try: s = least_squares(res, v0, loss="soft_l1", f_scale=3.0)
                except Exception: continue
                if best is None or s.cost < best.cost: best = s
    cam, yaw, pitch, roll, f = unpack(best.x); uv, _ = project(P, cam, yaw, pitch, roll, f, w, h)
    err = np.hypot(*(uv - UV).T); fwd, _, up = rot(yaw, pitch, roll)
    return dict(method=f"điểm khống chế ({len(pts)} điểm) + bình phương tối thiểu (scipy, soft_l1)", cam_enu=cam.tolist(), look_enu=(cam + 100 * fwd).tolist(), up_enu=up.tolist(),
                fov_v_deg=float(np.degrees(2 * np.arctan(h / 2 / f))), f_px=float(f), yaw_deg=float(np.degrees(yaw)), pitch_deg=float(np.degrees(pitch)), roll_deg=float(np.degrees(roll)),
                reproj_px={p.get("name", str(i)): round(float(e), 2) for i, (p, e) in enumerate(zip(pts, err))}, rms_px=float(np.sqrt(np.mean(err ** 2))),
                rms_pct_width=float(100 * np.sqrt(np.mean(err ** 2)) / w), n_points=len(pts))

if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("spec"); a.add_argument("--out"); o = a.parse_args()
    r = solve(json.load(open(o.spec))); s = json.dumps(r, ensure_ascii=False, indent=1); print(s)
    if o.out: open(o.out, "w").write(s)
