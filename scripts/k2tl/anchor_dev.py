"""V5b-2a (K-1.12 §7.1, TL-Q4b) · lệch ĐẦU ĐƯỜNG DẪN của ảnh/thẻ/nhãn neo ↔ ĐIỂM CHIẾU 3D, đo ĐỘC LẬP với trang dựng:
chiếu lại điểm neo 3D (ENU, ghi trong log `leaders[].world`) bằng máy kim lỗ dựng từ campath.json (pos, look, fov dọc, up = +y, khung W×H)
rồi so với đầu đường dẫn đã vẽ (`leaders[].end`, điểm ảnh). Ngưỡng TL-Q4b: ≤ 1 % bề rộng khung ở MỌI khung có ảnh neo.
Dùng: anchor_dev.py <campath.json> <log.json | text-budget.json> [--out kq.json] [--role photo]"""
import argparse, json, math, sys


def proj(p, l, fov, W, H, X):
    T = lambda v: (v[0], v[1], -v[2])   # ENU → toạ độ three.js (x = Đông, y = cao, z = −Bắc)
    p, l, X = T(p), T(l), T(X)
    f = [l[i] - p[i] for i in range(3)]; n = math.sqrt(sum(v * v for v in f)); f = [v / n for v in f]
    up = (0.0, 1.0, 0.0); r = [f[1] * up[2] - f[2] * up[1], f[2] * up[0] - f[0] * up[2], f[0] * up[1] - f[1] * up[0]]; n = math.sqrt(sum(v * v for v in r)); r = [v / n for v in r]
    u = [r[1] * f[2] - r[2] * f[1], r[2] * f[0] - r[0] * f[2], r[0] * f[1] - r[1] * f[0]]
    d = [X[i] - p[i] for i in range(3)]; z = sum(d[i] * f[i] for i in range(3))
    if z <= 0: return None
    th = math.tan(math.radians(fov) / 2); a = W / H
    nx, ny = sum(d[i] * r[i] for i in range(3)) / (z * th * a), sum(d[i] * u[i] for i in range(3)) / (z * th)
    return ((nx + 1) / 2 * W, (1 - ny) / 2 * H)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("campath"); ap.add_argument("log"); ap.add_argument("--out"); ap.add_argument("--role", default=""); a = ap.parse_args()
    cp = {r["f"]: r for r in json.load(open(a.campath))["frames"]}
    L = json.load(open(a.log)); rows = L["frames"] if isinstance(L, dict) else L
    res = []
    for r in rows:
        for ld in r.get("leaders", []) or []:
            if a.role and ld["role"] != a.role or not ld.get("world"): continue
            c = cp[r["f"]]; q = proj(c["pos"], c["look"], c["fov"], ld["W"], ld["H"], ld["world"])
            dev = math.hypot(q[0] - ld["end"][0], q[1] - ld["end"][1]) if q else None
            res.append(dict(f=r["f"], role=ld["role"], s=ld["s"], end=ld["end"], proj=[round(q[0], 1), round(q[1], 1)] if q else None, dev_px=None if dev is None else round(dev, 2),
                            dev_pct_w=None if dev is None else round(100 * dev / ld["W"], 3)))
    ok = [x for x in res if x["dev_pct_w"] is not None]
    by = {}
    for x in ok: by.setdefault(x["role"], []).append(x["dev_pct_w"])
    summ = dict(leaders=len(res), frames=len({x["f"] for x in res}), dev_pct_w_max=max((x["dev_pct_w"] for x in ok), default=None),
                theo_role={k: dict(n=len(v), max_pct_w=max(v), tb_pct_w=round(sum(v) / len(v), 3)) for k, v in by.items()}, sau_camera=len(res) - len(ok), nguong_pct_w=1.0)
    summ["dat"] = summ["dev_pct_w_max"] is not None and summ["dev_pct_w_max"] <= 1.0 and summ["sau_camera"] == 0
    print(json.dumps(summ, ensure_ascii=False))
    if a.out: json.dump(dict(summary=summ, leaders=res), open(a.out, "w"), ensure_ascii=False)


if __name__ == "__main__":
    main()
